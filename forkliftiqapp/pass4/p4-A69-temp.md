# Pass 4 Code Quality — Agent A69
**Audit run:** 2026-02-26-01
**Agent:** A69
**Date reviewed:** 2026-02-27

---

## Section 1: Reading Evidence

### File 1: `app/src/main/java/au/com/collectiveintelligence/fleetiq360/user/UserDb.java`

**Class:** `UserDb` (public, non-final utility class with only static members)

**Methods (exhaustive):**

| Line | Signature |
|------|-----------|
| 13 | `public static void save(final User user)` |
| 32 | `public static ArrayList<String> userEmails()` |
| 45 | `public static User get(final int id)` |
| 55 | `public static User get(final String email, final String password)` |
| 65 | `static List<User> driversOfCompany(final int companyId)` — package-private |

**Constants / types defined:** None.

**Imports:**
- `android.support.annotation.NonNull` (legacy support library)
- `au.com.collectiveintelligence.fleetiq360.model.SafeRealm`
- `io.realm.Realm`, `io.realm.RealmResults`
- `java.util.ArrayList`, `java.util.Collections`, `java.util.List`

---

### File 2: `app/src/main/java/au/com/collectiveintelligence/fleetiq360/user/UserRealmObject.java`

**Class:** `UserRealmObject extends RealmObject` (public)

**Fields (exhaustive):**

| Line | Name | Type | Access |
|------|------|------|--------|
| 10 | `id` | `int` | private, `@PrimaryKey` |
| 11 | `companyId` | `int` | private |
| 12 | `firstName` | `String` | private |
| 13 | `lastName` | `String` | private |
| 14 | `email` | `String` | private |
| 15 | `password` | `String` | private |
| 16 | `phoneNumber` | `String` | private |
| 17 | `licenseNumber` | `String` | private |
| 18 | `expiryDate` | `Date` | private |
| 19 | `address` | `String` | private |
| 20 | `securityNumber` | `String` | private |
| 21 | `photoUrl` | `String` | private |
| 22 | `isContactPerson` | `boolean` | private |
| 23 | `dateFormat` | `String` | private |
| 24 | `maxSessionLength` | `int` | private |
| 25 | `complianceDate` | `Date` | private |
| 26 | `gps_frequency` | `int` | private |

**Methods (exhaustive):**

| Line | Signature |
|------|-----------|
| 28 | `public UserRealmObject()` — no-arg constructor (Realm requirement) |
| 31 | `UserRealmObject(User user)` — package-private constructor |
| 51 | `User makeUser()` — package-private |
| 71 | `String getEmail()` — package-private |
| 75 | `void setValues(User user)` — package-private |

**Constants / types defined:** None.

---

### File 3: `app/src/main/java/au/com/collectiveintelligence/fleetiq360/util/CommonFunc.java`

**Class:** `CommonFunc` (public utility class, no constructor defined — implicit public no-arg)

**Methods (exhaustive):**

| Line | Signature |
|------|-----------|
| 16 | `public static boolean isCurrentDay(DateTime dateTime)` |
| 21 | `private static boolean isSameLocalDay(DateTime dateTime, DateTime dateTime1)` |
| 32 | `private static String dateToLocalDayString(DateTime dateTime)` |
| 39 | `private static DateTimeZone getCurrentDateTimeZone()` |
| 44 | `public static Date convertUTCDatetoLocalDate(Date utcDate)` |
| 50 | `public static String SHA1(String text)` |
| 68 | `public static String MD5_Hash(String s)` |
| 85 | `public static boolean isEmailInvalid(String email)` |
| 92 | `public static boolean isPasswordValid(String password)` |

**Constants / types defined:** None.

---

## Section 2 & 3: Findings

---

### A69-1 — HIGH — Password stored and queried in plaintext in Realm database

**File:** `UserDb.java` line 59; `UserRealmObject.java` lines 15, 37, 80

**Detail:**
`UserDb.get(String email, String password)` queries Realm with a raw password value:
```java
// UserDb.java:59
UserRealmObject user = realm.where(UserRealmObject.class)
    .equalTo("email", email)
    .equalTo("password", password)
    .findFirst();
```
`UserRealmObject` persists `password` as a plain `String` field (line 15). The call site in `CurrentUser.java` (line 103) passes `loginPassword` which is an MD5 hash of the user's input — so the on-disk value is an MD5 hash, not a cleartext password. However: (a) MD5 is a broken algorithm unsuitable for password storage; (b) the hash is stored without a salt; (c) `User.getPassword()` is declared `public` (User.java line 135), exposing the credential hash to any caller outside the package; (d) `UserRealmObject.setValues()` (line 80) only updates the password field when it is non-null, creating a conditional update asymmetry with the constructor at line 37, which unconditionally copies the password — a logic inconsistency that could leave a stale hash if a null is intentionally passed.

**Classification:** HIGH — unsalted MD5 password hash persisted to local database and exposed via public getter.

---

### A69-2 — HIGH — Wrong hash length padding in `SHA1()` — produces incorrect output for hashes >= 40 hex digits

**File:** `CommonFunc.java` lines 61–64

**Detail:**
```java
// CommonFunc.java:61-64
StringBuilder hash = new StringBuilder(new BigInteger(1, md.digest()).toString(16));
while (hash.length() < 32) {
    hash.insert(0, "0");
}
```
SHA-1 produces a 160-bit (20-byte) digest. Its correct hexadecimal representation is always exactly **40 characters**. The padding loop uses the constant `32` — the correct value for MD5 (128-bit, 16-byte). As a result:
- Any SHA-1 digest whose leading bytes happen to produce a 32-39 character hex string will be left-padded with zeros, yielding an invalid hash.
- Any digest whose hex representation is already 40 characters will not be padded, and the function returns the correct value for those cases only.

The `MD5_Hash()` method at line 79 correctly uses `< 32`. The `SHA1()` method must use `< 40`. This is a copy-paste defect where the MD5 padding threshold was not updated for SHA-1.

**Classification:** HIGH — produces cryptographically incorrect output for a significant fraction of inputs; used in BLE model path hashing (`BleModel.java:97`).

---

### A69-3 — HIGH — `MD5_Hash()` throws `NullPointerException` on `NoSuchAlgorithmException`

**File:** `CommonFunc.java` lines 68–83

**Detail:**
```java
public static String MD5_Hash(String s) {
    MessageDigest m = null;
    try {
        m = MessageDigest.getInstance("MD5");
    } catch (NoSuchAlgorithmException e) {
        e.printStackTrace();  // swallowed — m remains null
    }
    Objects.requireNonNull(m).update(s.getBytes(), 0, s.length());  // NPE if catch fired
    ...
}
```
If `NoSuchAlgorithmException` is caught, `m` remains `null`. The next statement calls `Objects.requireNonNull(m)`, which will throw `NullPointerException`. The exception message will be opaque. Compare with `SHA1()` (lines 52–57) which correctly returns an empty string on the same exception. The two methods are inconsistent in their error handling, and `MD5_Hash()` is actively dangerous — it silently swallows a checked exception and then crashes via an unchecked one.

Note: `MD5_Hash` is used in `CurrentUser.java` lines 82 and 122 as part of the login flow; a crash here logs out the user silently.

**Classification:** HIGH — inconsistent and broken exception handling causing NPE in login path.

---

### A69-4 — MEDIUM — `getBytes()` called without an explicit charset in both `SHA1()` and `MD5_Hash()`

**File:** `CommonFunc.java` lines 59 and 77

**Detail:**
```java
// SHA1(), line 59
md.update(text.getBytes(), 0, text.length());

// MD5_Hash(), line 77
Objects.requireNonNull(m).update(s.getBytes(), 0, s.length());
```
`String.getBytes()` without a charset argument uses the platform's default charset, which varies by device and Android API level. This produces non-deterministic byte arrays for any string containing non-ASCII characters, making the resulting hashes device-dependent. The second argument to `update()` should be `text.getBytes(charset).length`, not `text.length()`, because `String.length()` returns the number of `char` values, which can differ from the byte count for multi-byte encodings (e.g., UTF-8). If the byte array is shorter than `text.length()`, `ArrayIndexOutOfBoundsException` is thrown at runtime.

**Classification:** MEDIUM — potential `ArrayIndexOutOfBoundsException` for non-ASCII input; non-deterministic hashing across devices.

---

### A69-5 — MEDIUM — Style inconsistency: naming convention `gps_frequency` violates Java naming conventions throughout the user model

**Files:** `UserRealmObject.java` line 26, 48, 68, 91; `User.java` lines 28, 62, 176 (accessor `getGps_frequency()`)

**Detail:**
All other fields in `UserRealmObject` and `User` use `camelCase` (e.g., `companyId`, `firstName`, `maxSessionLength`). The field `gps_frequency` uses `snake_case`, the naming convention of the JSON API response and database column. The accessor `getGps_frequency()` is similarly non-conforming. This is the only field that was not renamed on ingestion from the network layer, creating a permanent style inconsistency visible in all public API consumers (`MyApplication.java:147` references `getGps_frequency()`).

**Classification:** MEDIUM — style inconsistency that pollutes the public API of `User` and propagates to call sites.

---

### A69-6 — MEDIUM — `UserDb.save()` uses `SafeRealm.Execute` wrapping its own nested `executeTransaction`, bypassing `SafeRealm.executeTransaction()`

**File:** `UserDb.java` lines 13–30

**Detail:**
`SafeRealm` provides a dedicated `executeTransaction()` method (SafeRealm.java line 13). `UserDb.save()` does not use it; instead it calls `SafeRealm.Execute(Action)` and then manually calls `realm.executeTransaction()` inside the action body:
```java
// UserDb.java:13-29
SafeRealm.Execute(new SafeRealm.Action() {
    @Override
    public void Execute(Realm realm) {
        realm.executeTransaction(new Realm.Transaction() {   // nested — redundant
            ...
        });
    }
});
```
This pattern is unnecessarily verbose, inconsistent with how `SafeRealm.executeTransaction` is used elsewhere in the codebase (e.g., `EquipmentDb.java:46`), and the outer `SafeRealm.Execute()` call does not close the Realm inside a `finally` block — it relies on `SafeRealm.Execute` (SafeRealm.java:10) which calls `realm.close()` unconditionally after the action, with no exception safety. The redundant nesting adds complexity with no benefit.

**Classification:** MEDIUM — style inconsistency and inconsistent use of the SafeRealm abstraction layer.

---

### A69-7 — MEDIUM — `UserDb.get(String, String)` queried with a pre-hashed password but the method signature implies plaintext

**File:** `UserDb.java` lines 55–63

**Detail:**
The method signature `get(String email, String password)` implies a raw credential lookup. In practice, the caller (`CurrentUser.java` line 103) passes `loginPassword` which has already been MD5-hashed by `setTemporaryLoginInformation()`. The method is also called with a pre-hashed `email` (MD5-hashed via `CommonFunc.MD5_Hash(loginEmail)` at line 82, but the `equalTo("email", email)` query uses the stored plain email). This is an asymmetry: the email query uses the stored (plain) value while the password query matches against the stored hash. The API of `UserDb.get(email, password)` leaks no indication of these hashing expectations — a caller who passes a plaintext password will silently fail to authenticate even when credentials are valid, with no error returned.

**Classification:** MEDIUM — leaky abstraction; method contract is unclear and inconsistent with its actual behaviour; no documentation of parameter pre-conditions.

---

### A69-8 — MEDIUM — `convertUTCDatetoLocalDate()` performs spurious round-trip through `toLocalDateTime().toDate()`

**File:** `CommonFunc.java` lines 44–48

**Detail:**
```java
public static Date convertUTCDatetoLocalDate(Date utcDate) {
    DateTime dt = new DateTime(utcDate);
    DateTime dtus = dt.withZone(getCurrentDateTimeZone());
    return dtus.toLocalDateTime().toDate();
}
```
`dtus.toLocalDateTime()` discards timezone information and creates a `LocalDateTime`, then `.toDate()` re-interprets it as the system default timezone. The intermediate `.withZone()` call is redundant because `toLocalDateTime()` extracts fields in the `DateTime`'s zone regardless. The effective behavior is equivalent to `new DateTime(utcDate).toLocalDateTime().toDate()`. The function name and the intermediate `withZone` step suggest an intent to apply an explicit conversion, but the logic does not achieve what a naive reader expects. This is a latent correctness concern if the code is refactored or the Joda-Time version changes.

**Classification:** MEDIUM — logic is misleading; intermediate timezone conversion is ineffective.

---

### A69-9 — LOW — `android.support.annotation.NonNull` imported in `UserDb.java` but only used in an anonymous inner class

**File:** `UserDb.java` line 3

**Detail:**
The import of `android.support.annotation.NonNull` is required for the anonymous `Realm.Transaction` inner class override at line 19. However, the project targets a support library version (`com.android.support:appcompat-v7:26.0.2`) that predates the migration to AndroidX. The annotation is functionally correct but the import is from the deprecated `android.support` namespace rather than `androidx.annotation.NonNull`. This import will produce a build warning when the project eventually migrates to AndroidX and is flagged as deprecated by Android Studio's lint tooling even before migration.

**Classification:** LOW — deprecated support library import; will require update on AndroidX migration.

---

### A69-10 — LOW — Style inconsistency: method name `SHA1` does not follow Java naming conventions

**File:** `CommonFunc.java` line 50

**Detail:**
Java naming convention for methods is `lowerCamelCase`. The method is named `SHA1` (all caps prefix). The companion method `MD5_Hash` at line 68 uses a different non-conforming style (`UpperCamelCase` with underscore). Neither follows the convention; they also differ from each other. All other methods in `CommonFunc` use correct `lowerCamelCase` (e.g., `isCurrentDay`, `isEmailInvalid`, `isPasswordValid`). These inconsistencies are visible in the public API of the class.

**Classification:** LOW — public API naming inconsistency.

---

### A69-11 — LOW — `UserRealmObject` constructor does not guard against `null` password from `User`

**File:** `UserRealmObject.java` line 37

**Detail:**
`setValues()` (line 80) guards against `null`:
```java
if (user.getPassword() != null) password = user.getPassword();
```
The constructor (line 37) does not:
```java
password = user.getPassword();  // unconditional — can write null
```
This asymmetry means a `UserRealmObject` created via the constructor can have a null `password` field (no Realm `@Required` annotation is present on this field), while one updated via `setValues` preserves the previous non-null value. This produces inconsistent database state depending on which code path persisted the record.

**Classification:** LOW — inconsistent null-guard between constructor and update method.

---

### A69-12 — LOW — `isSameLocalDay()` only null-checks the first argument

**File:** `CommonFunc.java` lines 21–30

**Detail:**
```java
private static boolean isSameLocalDay(DateTime dateTime, DateTime dateTime1) {
    if (null == dateTime) {
        return false;
    }
    String s = dateToLocalDayString(dateTime);
    String s1 = dateToLocalDayString(dateTime1);  // NPE if dateTime1 is null
    return s.equals(s1);
}
```
The method checks `dateTime` for null but does not check `dateTime1`. The only caller, `isCurrentDay()`, passes `DateTime.now()` as `dateTime1`, which cannot be null. However, the private method's signature accepts arbitrary `DateTime` arguments, and if ever called from another context with a null second argument, `dateToLocalDayString(null)` will throw `NullPointerException` because `dateTime.withZone(...)` is called on a null reference. The defensive null-check for the first argument implies null-safety was intended for all arguments.

**Classification:** LOW — incomplete null guard; latent NPE risk if method is ever called from additional callers.

---

### A69-13 — INFO — `CommonFunc` is a non-instantiable utility class but declares no private constructor

**File:** `CommonFunc.java`

**Detail:**
`CommonFunc` contains only static methods and no instance state. Java best practice for utility classes is to declare a private no-arg constructor with an `UnsupportedOperationException` body to prevent instantiation. Without it, the implicit public no-arg constructor allows callers to write `new CommonFunc()`, which serves no purpose and creates a misleading API.

**Classification:** INFO — no private constructor on static utility class.

---

### A69-14 — INFO — `UserDb` is a non-instantiable utility class but declares no private constructor

**File:** `UserDb.java`

**Detail:**
Same pattern as A69-13. `UserDb` has only static methods. No private constructor prevents instantiation via the implicit public default constructor.

**Classification:** INFO — no private constructor on static utility class.

---

## Summary Table

| ID | Severity | File | Description |
|----|----------|------|-------------|
| A69-1 | HIGH | UserDb.java, UserRealmObject.java | Password stored as unsalted MD5 hash; exposed via public getter; conditional null asymmetry |
| A69-2 | HIGH | CommonFunc.java | SHA1() uses wrong padding length (32 instead of 40), producing incorrect output |
| A69-3 | HIGH | CommonFunc.java | MD5_Hash() throws NPE on exception instead of returning gracefully like SHA1() |
| A69-4 | MEDIUM | CommonFunc.java | getBytes() without charset; length mismatch between char count and byte count |
| A69-5 | MEDIUM | UserRealmObject.java, User.java | gps_frequency uses snake_case, violating Java naming conventions throughout the user model |
| A69-6 | MEDIUM | UserDb.java | save() nests realm.executeTransaction inside SafeRealm.Execute; bypasses SafeRealm.executeTransaction |
| A69-7 | MEDIUM | UserDb.java | get(email, password) leaks no indication that password must be pre-hashed; silent auth failure if raw value passed |
| A69-8 | MEDIUM | CommonFunc.java | convertUTCDatetoLocalDate() withZone step is ineffective; misleading logic |
| A69-9 | LOW | UserDb.java | android.support.annotation.NonNull is deprecated; should be androidx.annotation.NonNull |
| A69-10 | LOW | CommonFunc.java | SHA1 and MD5_Hash method names do not follow lowerCamelCase; differ from each other |
| A69-11 | LOW | UserRealmObject.java | Constructor does not null-guard password; setValues() does — inconsistent behaviour |
| A69-12 | LOW | CommonFunc.java | isSameLocalDay() null-checks only first argument; second can NPE |
| A69-13 | INFO | CommonFunc.java | No private constructor on static utility class |
| A69-14 | INFO | UserDb.java | No private constructor on static utility class |
