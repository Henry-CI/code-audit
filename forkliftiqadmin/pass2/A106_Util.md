# Pass 2 – Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A106
**Source File:** `src/main/java/com/util/Util.java`
**Test Directory:** `src/test/java/`

---

## 1. Reading Evidence

### Class Name
- `com.util.Util` (declared at line 30)

### Fields
None. The class has no instance or static fields.

### Methods (with line numbers)

| # | Signature | Line |
|---|-----------|------|
| 1 | `public static boolean sendMail(String subject, String mBody, String rName, String rEmail, String sName, String sEmail)` | 32 |
| 2 | `public static boolean sendMail(String subject, String mBody, String rName, String rEmail, String sName, String sEmail, String attachment, String attachmentName)` | 73 |
| 3 | `public static String getHTML(String urlToRead)` | 134 |
| 4 | `public static String genPass(int chars)` | 159 |
| 5 | `public static String checkedValueRadio(String value, String dbValue)` | 179 |
| 6 | `public static String checkedValueCheckbox(String value, ArrayList<String> dbValue)` | 191 |
| 7 | `@Deprecated public static String ArraListToString(ArrayList<String> arrString)` | 204 |
| 8 | `public static String selectRoleBox(String value, ArrayList<RoleBean> dbValue)` | 210 |
| 9 | `public static ArrayList<String> getBarcodeTimeLst(String time)` | 230 |
| 10 | `public static String generateRadomName()` | 258 |
| 11 | `public static int nthOccurrence(String str, char c, int n)` | 268 |

---

## 2. Test Coverage Evidence

### Test files found referencing "Util"
- `src/test/java/com/util/ImpactUtilTest.java`

### Content of ImpactUtilTest.java
`ImpactUtilTest.java` tests `com.util.ImpactUtil` (a different class). It exercises:
- `ImpactUtil.calculateGForceOfImpact`
- `ImpactUtil.calculateImpactLevel`
- `ImpactUtil.calculateGForceRequiredForImpact`
- `ImpactUtil.getCSSColor`

### Grep for Util.java method names across all test files
A grep across all 4 test files (`ImpactUtilTest.java`, `UnitCalibrationImpactFilterTest.java`, `UnitCalibrationTest.java`, `UnitCalibratorTest.java`) for: `sendMail`, `genPass`, `getHTML`, `checkedValue`, `getBarcodeTimeLst`, `generateRadomName`, `nthOccurrence`, `ArraListToString`, `selectRoleBox` returned **zero matches**.

**Conclusion: `com.util.Util` has zero test coverage. Not one method is exercised by any test.**

---

## 3. Findings

---

### A106-1 | Severity: CRITICAL | `com.util.Util` has zero test coverage across all 11 methods

No test file in `src/test/java/` references `com.util.Util`, any of its methods, or its class name. The class is entirely untested. All findings below are therefore both "untested" and "missing error paths / edge cases."

---

### A106-2 | Severity: CRITICAL | `genPass` uses MD5 for password/token generation — cryptographically broken algorithm with no test coverage

**Location:** Lines 159–175
**Detail:** `genPass` generates passwords by feeding 1024 bytes of `java.util.Random` (a non-cryptographically-secure PRNG) into an MD5 `MessageDigest`. MD5 is cryptographically broken and must not be used to generate secrets or passwords. `java.util.Random` is not a CSPRNG; its output is predictable given the seed. There are no tests verifying the output length, the character set, or that the generated value is actually usable as a password. The method also silently returns `null` (line 167) on `NoSuchAlgorithmException` without surfacing the error to callers.

---

### A106-3 | Severity: CRITICAL | `sendMail` (6-argument overload) — inconsistent return value masks delivery failures; no tests

**Location:** Lines 32–71
**Detail:** The method returns `true` (line 70) even when the outer `catch (Throwable t)` block fires (line 67), meaning JNDI lookup failures, session construction failures, or any other `Throwable` result in a `true` return indicating success. Only the two inner `try` blocks (recipient parse failure and `Transport.send` failure) return `false`. A caller relying on the boolean return value to confirm delivery cannot trust it. No tests exist for: null `sEmail`, invalid `rEmail`, JNDI unavailability, `Transport.send` failure, or the Throwable catch path.

---

### A106-4 | Severity: CRITICAL | `sendMail` (8-argument overload with attachment) — recipient exception silently swallowed; always returns `true`; no tests

**Location:** Lines 73–131
**Detail:** Unlike the 6-argument overload, when the recipient parse throws at line 90–92, the code only prints to stdout and continues execution — the email is sent with no recipient set, or the subsequent `Transport.send` will fail silently (its exception is only printed, not returned). The method unconditionally returns `true` at line 130 regardless of any failure path. Additionally, `attachment.equalsIgnoreCase("")` at line 108 will throw a `NullPointerException` if `attachment` is `null`, with no guard. No tests exist.

---

### A106-5 | Severity: HIGH | `sendMail` methods use JNDI lookup (`java:comp/env`) — hardcoded JNDI path with no testability or configuration abstraction

**Location:** Lines 36–38 and 77–79
**Detail:** Both `sendMail` overloads hardcode the JNDI names `"java:comp/env"` and `"mail/Session"`. This couples the utility tightly to a container-managed environment, making unit testing impossible without a mock JNDI context and making the mail server configuration opaque to code reviewers. There are no tests verifying what happens when the JNDI lookup returns `null` or throws `NamingException`.

---

### A106-6 | Severity: HIGH | `getHTML` — no timeout on connect, 15-minute read timeout, swallows all exceptions; no tests

**Location:** Lines 134–155
**Detail:** `getHTML` sets `conn.setReadTimeout(900000)` (15 minutes) but sets no connect timeout, meaning a connect to a non-responsive host can block indefinitely. All exceptions are swallowed (only `e.printStackTrace()`), and the method returns an empty string on failure with no indication to the caller that an error occurred. The method is also vulnerable to SSRF (Server-Side Request Forgery) if the URL is user-supplied, as there is no URL validation or allowlist. The string accumulation via `result += line` inside a loop causes quadratic memory allocation for large responses. No tests exist for: invalid URLs, network failures, redirect handling, or large responses.

---

### A106-7 | Severity: HIGH | `getBarcodeTimeLst` — brittle string parsing with no null/format validation; multiple `ArrayIndexOutOfBoundsException` risks; no tests

**Location:** Lines 230–256
**Detail:** The method assumes `time` is in the format `"DD/MM/YYYY HH:MM"` exactly. It will throw:
- `NullPointerException` if `time` is `null`
- `ArrayIndexOutOfBoundsException` if `time` does not contain a space (missing time component), or if the date/time components don't split into the expected number of parts
- `StringIndexOutOfBoundsException` if any component (day, month, year, hours, minutes) is shorter than 2 characters

No input validation exists and no tests cover any format variation, boundary, or malformed input.

---

### A106-8 | Severity: MEDIUM | `checkedValueRadio` — NullPointerException if `value` is null; no tests

**Location:** Lines 179–188
**Detail:** `value.equalsIgnoreCase(dbValue)` will throw `NullPointerException` if `value` is `null`. The safer pattern would be `dbValue.equalsIgnoreCase(value)` or an explicit null check. No tests exist for either the happy path or null inputs.

---

### A106-9 | Severity: MEDIUM | `selectRoleBox` — iterates all roles even after match found; no tests

**Location:** Lines 210–227
**Detail:** Once a matching role ID is found, the loop continues iterating rather than breaking, which is a minor correctness issue if a later non-matching entry could overwrite `select` — though in this case `select` is only written to `"selected"` and never reset to `""`, so the logic is accidentally correct. However, the unnecessary iteration wastes cycles on large lists. More importantly, `dbValue.get(i).getId()` will throw `NullPointerException` if any `RoleBean` in the list is `null` or if `getId()` returns `null`. No tests exist.

---

### A106-10 | Severity: MEDIUM | `nthOccurrence` — returns -1 for not-found but also returns -1 when n exceeds occurrences; no tests

**Location:** Lines 268–273
**Detail:** The method returns `pos` which may be -1 either because the character was never found or because `n` exceeded the count of occurrences; callers cannot distinguish these cases. Additionally, if `str` is `null`, `str.indexOf` throws `NullPointerException`. If `n` is negative, the loop condition `n-- > 0` is immediately false, so the method returns the position of the first occurrence (index 0 of character in string) — this may be surprising. No tests cover these edge cases.

---

### A106-11 | Severity: MEDIUM | `generateRadomName` — method name is a typo (`Radom` instead of `Random`); no tests

**Location:** Lines 258–266
**Detail:** The method name `generateRadomName` is a typo of `generateRandomName`. Because this is a public static method, renaming it would be a breaking API change. The combination of a timestamp and a UUID provides reasonable uniqueness, but there are no tests to verify the output format (e.g., that it always matches `yyyyMMddHHmmss-<uuid>`) or that it is non-null.

---

### A106-12 | Severity: MEDIUM | `genPass` — `chars` parameter can exceed MD5 hex output length (32 chars), causing `StringIndexOutOfBoundsException`; no tests

**Location:** Line 174
**Detail:** `new BigInteger(1, md.digest()).toString(16).substring(0, chars)` — an MD5 digest is 128 bits, producing at most 32 hex characters. If `chars > 32` (or if the leading zeros cause the hex representation to be shorter than `chars`), `substring` throws `StringIndexOutOfBoundsException`. There is no validation of the `chars` parameter and no test exercising boundary values.

---

### A106-13 | Severity: LOW | `ArraListToString` is `@Deprecated` but has no replacement documented and no tests

**Location:** Lines 204–207
**Detail:** The method is marked `@Deprecated` with no Javadoc indicating the preferred alternative. It is equivalent to `String.join(",", arrString)` which callers could use directly. The deprecation has not led to removal, and there are no tests to verify or protect its behavior before removal.

---

### A106-14 | Severity: LOW | `checkedValueCheckbox` — no tests for null `dbValue` list or empty list

**Location:** Lines 191–201
**Detail:** The method guards against `value == null` but not against `dbValue == null`, which would cause a `NullPointerException` on the `dbValue.contains(value)` call. No tests exist for any input combination.

---

### A106-15 | Severity: INFO | `sendMail` parameters `rName` and `sName` are accepted but never used

**Location:** Lines 32–34 and 73–74
**Detail:** Both `sendMail` overloads accept `rName` (recipient name) and `sName` (sender name) parameters that are never referenced in the method body. The sender address is set purely from `sEmail`; the human-readable name portion of the `InternetAddress` is never populated. This is a dead parameter issue that could confuse callers and indicates the API surface was never fully implemented. No tests document the expected behavior of these parameters.

---

## 4. Summary Table

| Finding | Severity | Description |
|---------|----------|-------------|
| A106-1 | CRITICAL | Zero test coverage across all 11 methods |
| A106-2 | CRITICAL | `genPass` uses MD5 + non-CSPRNG `java.util.Random` for password generation |
| A106-3 | CRITICAL | `sendMail` (6-arg) always returns `true` on Throwable; delivery failures masked |
| A106-4 | CRITICAL | `sendMail` (8-arg) always returns `true`; NPE on null attachment; recipient exception swallowed |
| A106-5 | HIGH | Hardcoded JNDI paths in `sendMail`; no testability or configuration abstraction |
| A106-6 | HIGH | `getHTML`: no connect timeout, swallows all exceptions, SSRF risk, quadratic string concat |
| A106-7 | HIGH | `getBarcodeTimeLst`: brittle parsing, multiple NPE/AIOOBE risks on malformed input |
| A106-8 | MEDIUM | `checkedValueRadio`: NPE if `value` is null |
| A106-9 | MEDIUM | `selectRoleBox`: loop does not break on match; NPE risk from null RoleBeans |
| A106-10 | MEDIUM | `nthOccurrence`: ambiguous -1 return; NPE on null str; negative-n behavior undefined |
| A106-11 | MEDIUM | `generateRadomName`: typo in method name; no format tests |
| A106-12 | MEDIUM | `genPass`: `chars > 32` causes `StringIndexOutOfBoundsException` |
| A106-13 | LOW | `@Deprecated ArraListToString` has no documented replacement and no tests |
| A106-14 | LOW | `checkedValueCheckbox`: NPE if `dbValue` is null |
| A106-15 | INFO | `rName`/`sName` parameters accepted but never used in both `sendMail` overloads |
