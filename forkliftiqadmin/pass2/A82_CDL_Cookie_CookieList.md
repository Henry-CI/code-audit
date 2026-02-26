# Pass 2 Audit Report: CDL, Cookie, CookieList
**Audit Run:** 2026-02-26-01
**Agent ID:** A82
**Date:** 2026-02-26
**Scope:** Vendored JSON library classes in `com.json` package

---

## Source Files Audited

1. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/json/CDL.java`
2. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/json/Cookie.java`
3. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/json/CookieList.java`

---

## Reading Evidence

### 1. CDL.java

**Class name:** `CDL` (package `com.json`)

**Fields:** None (utility class; all-static, no instance fields)

**Methods:**

| Method | Line | Access |
|---|---|---|
| `getValue(JSONTokener x)` | 55 | `private static` |
| `rowToJSONArray(JSONTokener x)` | 95 | `public static` |
| `rowToJSONObject(JSONArray names, JSONTokener x)` | 131 | `public static` |
| `rowToString(JSONArray ja)` | 144 | `public static` |
| `toJSONArray(String string)` | 181 | `public static` |
| `toJSONArray(JSONTokener x)` | 192 | `public static` |
| `toJSONArray(JSONArray names, String string)` | 204 | `public static` |
| `toJSONArray(JSONArray names, JSONTokener x)` | 217 | `public static` |
| `toString(JSONArray ja)` | 245 | `public static` |
| `toString(JSONArray names, JSONArray ja)` | 265 | `public static` |

**Library version indicated:** `@version 2010-12-24` (javadoc header, line 44)
**License:** JSON.org (lines 3-25), includes the non-OSI "shall be used for Good, not Evil" clause.

---

### 2. Cookie.java

**Class name:** `Cookie` (package `com.json`)

**Fields:** None (utility class; all-static, no instance fields)

**Methods:**

| Method | Line | Access |
|---|---|---|
| `escape(String string)` | 47 | `public static` |
| `toJSONObject(String string)` | 81 | `public static` |
| `toString(JSONObject jo)` | 118 | `public static` |
| `unescape(String string)` | 150 | `public static` |

**Library version indicated:** `@version 2010-12-24` (javadoc header, line 31)
**License:** JSON.org (lines 3-25)

---

### 3. CookieList.java

**Class name:** `CookieList` (package `com.json`)

**Fields:** None (utility class; all-static, no instance fields)

**Imports:** `java.util.Iterator` (line 27) — raw `Iterator` type (no generic parameter).

**Methods:**

| Method | Line | Access |
|---|---|---|
| `toJSONObject(String string)` | 49 | `public static` |
| `toString(JSONObject jo)` | 71 | `public static` |

**Library version indicated:** `@version 2010-12-24` (javadoc header, line 32)
**License:** JSON.org (lines 3-25)

---

## Test Coverage Search Results

**Test directory searched:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`

**Existing test files:**
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

**Search for "CDL" in test directory:** No matches found.
**Search for "Cookie" in test directory:** No matches found.
**Search for "CookieList" in test directory:** No matches found.

**Application usage search (non-json-package Java files referencing `com.json.CDL`, `com.json.Cookie`, `com.json.CookieList`):** No matches found in any application source file outside `src/main/java/com/json/`.

The only references to `Cookie` found in the application are to `javax.servlet.http.Cookie` (Servlet API), not to `com.json.Cookie`. These appear in `ExpireAction.java`, `LogoutAction.java`, `SwitchLanguageAction.java`, `WelcomeAction.java`, and several JSP files. None use the `com.json.Cookie` class.

---

## Findings

### CDL.java

**A82-1 | Severity: INFO | CDL is a vendored library class with zero test coverage**
`CDL` has no test class in the test directory. None of its ten methods (public or private) are exercised by any test. As a vendored third-party utility class that is not used anywhere in the application, the absence of tests is low immediate risk, but the class adds untested surface area to the codebase.

**A82-2 | Severity: INFO | CDL is not referenced by any application code**
A full-codebase search found zero imports or usages of `com.json.CDL` outside the class file itself. The class is dead code from the vendored bundle. It was never removed after vendoring the JSON.org library.

**A82-3 | Severity: LOW | CDL.rowToString silently drops characters rather than escaping them**
`rowToString` (line 144) handles values that contain commas, newlines, or start with `"` by wrapping them in double quotes. However, the inner loop at lines 158-162 silently drops any character that is a control character (`c < ' '`) or is a double-quote character (`c == '"'`). This means embedded double-quote characters are destroyed without escaping (e.g., RFC 4180 requires `""` doubling). If any future application code relies on `CDL.toString` round-tripping JSON data that contains embedded quotes, it will produce corrupt CSV output without any error or warning. No test validates this behavior.

**A82-4 | Severity: LOW | CDL.toJSONArray(JSONArray, JSONTokener) returns null on empty input instead of empty array**
Lines 219-221 return `null` when `names` is null or zero-length, and lines 230-232 return `null` when no rows were parsed. Callers that do not null-check the return value will receive a `NullPointerException`. Because no tests exist, this null-return contract is undocumented and unverified.

**A82-5 | Severity: INFO | CDL uses StringBuffer instead of StringBuilder throughout**
All string accumulation in `CDL` uses `StringBuffer` (lines 58, 68, 145, 270). `StringBuffer` is synchronized and deprecated in favor of `StringBuilder` for single-threaded use. This is a minor performance issue inherited from the 2010-era source. No tests verify performance characteristics.

**A82-6 | Severity: INFO | CDL library is pinned to a 2010 snapshot with no version management**
The `@version 2010-12-24` tag indicates this is a 15-year-old snapshot of the JSON.org library. There is no Maven/Gradle dependency declaration for it; the source is vendored directly. Any bug fixes or security patches to the upstream org.json library (e.g., [NVD CVE entries against org.json](https://nvd.nist.gov/vuln/search/results?query=org.json)) will not be automatically applied. This applies to all files in `com.json`.

---

### Cookie.java

**A82-7 | Severity: INFO | Cookie (com.json) is a vendored library class with zero test coverage**
`com.json.Cookie` has no test class. None of its four public methods (`escape`, `toJSONObject`, `toString`, `unescape`) are exercised by any test.

**A82-8 | Severity: INFO | com.json.Cookie is not used by any application code**
A full-codebase search found zero imports or usages of `com.json.Cookie` outside the `com.json` package itself (where `CookieList` delegates to it). The application uses `javax.servlet.http.Cookie` for actual HTTP cookie handling. `com.json.Cookie` is dead code.

**A82-9 | Severity: MEDIUM | Cookie.escape does not handle multi-byte Unicode characters correctly**
`Cookie.escape` (lines 47-63) operates byte-by-byte on Java `char` values using the bit-shift `(c >>> 4) & 0x0f` technique. For characters in the Basic Multilingual Plane this produces a two-hex-digit `%hh` sequence corresponding to the Java `char` value, not the UTF-8 byte sequence. For non-ASCII characters, this is semantically incorrect URL encoding (RFC 3986 requires percent-encoding of UTF-8 bytes, not UTF-16 code units). No test exercises non-ASCII input, so this defect is undetected.

**A82-10 | Severity: MEDIUM | Cookie.unescape decodes only two hex digits per sequence (%hh), not UTF-8 multi-byte sequences**
`Cookie.unescape` (lines 150-168) decodes `%hh` as a single character with value `d*16+e`. This means it cannot decode multi-byte percent-encoded UTF-8 sequences correctly (e.g., `%C3%A9` for `é`). This is consistent with `escape` but means the escape/unescape round-trip is only safe for ASCII. No test validates round-trip behavior with non-ASCII data.

**A82-11 | Severity: LOW | Cookie.toJSONObject does not validate or trim the "name" field**
In `toJSONObject` (line 86), `x.nextTo('=')` retrieves everything up to the `=` sign and stores it directly as the cookie name without trimming whitespace or validating that the name is a valid cookie token. Malformed cookie strings with whitespace in the name position will silently produce a JSONObject with a whitespace-prefixed key. No test exercises malformed input.

**A82-12 | Severity: LOW | Cookie.toString does not guard against null "name" or "value" in the JSONObject**
`toString` (lines 118-140) calls `jo.getString("name")` and `jo.getString("value")` without checking for null or missing keys. If a caller passes a JSONObject missing either field, a `JSONException` will be thrown. This is a latent risk if the method is ever called with partially constructed objects. No test validates error-path behavior.

**A82-13 | Severity: INFO | Cookie uses StringBuffer instead of StringBuilder**
Same issue as A82-5 — all `StringBuffer` usage in `escape` (line 50), `toString` (line 119), and `unescape` (line 152) should be `StringBuilder`. Inherited from the 2010-era vendor code.

---

### CookieList.java

**A82-14 | Severity: INFO | CookieList is a vendored library class with zero test coverage**
`com.json.CookieList` has no test class. Neither `toJSONObject` nor `toString` is exercised by any test.

**A82-15 | Severity: INFO | com.json.CookieList is not used by any application code**
A full-codebase search found zero imports or usages of `com.json.CookieList` anywhere outside its own source file. It is dead code.

**A82-16 | Severity: LOW | CookieList.toString uses raw Iterator type**
`toString` (line 73) declares `Iterator keys = jo.keys()` without a generic type parameter. This produces an unchecked cast warning and relies on an implicit `Object` type for `keys.next()` (which is then `.toString()`'d on line 77). While functionally correct, the raw type is a code quality issue and indicates the code predates Java 5 generics. No test validates this path.

**A82-17 | Severity: LOW | CookieList.toJSONObject does not handle missing '=' separator gracefully**
`toJSONObject` (lines 49-59) calls `x.next('=')` (line 54), which throws a `JSONException` if the character is not `=`. However, the surrounding `while (x.more())` loop does not catch this exception, meaning a malformed cookie list string (e.g., missing `=`) will propagate an unchecked exception to the caller. No test exercises malformed input.

**A82-18 | Severity: INFO | CookieList inherits non-ASCII encoding defects from Cookie.escape/unescape**
Because `CookieList.toJSONObject` calls `Cookie.unescape` and `CookieList.toString` calls `Cookie.escape`, the non-ASCII encoding defects described in A82-9 and A82-10 apply to `CookieList` as well. No tests validate this behavior in either class.

---

## Summary Table

| ID | Severity | Class | Description |
|---|---|---|---|
| A82-1 | INFO | CDL | Zero test coverage |
| A82-2 | INFO | CDL | Not referenced by application code (dead code) |
| A82-3 | LOW | CDL | `rowToString` silently drops embedded double-quote characters instead of escaping |
| A82-4 | LOW | CDL | `toJSONArray` returns null on empty/null input; no null-contract tests |
| A82-5 | INFO | CDL | Uses deprecated `StringBuffer` throughout |
| A82-6 | INFO | All three | Vendored 2010-era snapshot; no upstream patch path |
| A82-7 | INFO | Cookie | Zero test coverage |
| A82-8 | INFO | Cookie | Not referenced by application code (dead code) |
| A82-9 | MEDIUM | Cookie | `escape` produces incorrect percent-encoding for non-ASCII characters |
| A82-10 | MEDIUM | Cookie | `unescape` cannot decode multi-byte UTF-8 percent-encoded sequences |
| A82-11 | LOW | Cookie | `toJSONObject` does not validate or trim cookie name |
| A82-12 | LOW | Cookie | `toString` does not guard against missing "name"/"value" keys |
| A82-13 | INFO | Cookie | Uses deprecated `StringBuffer` throughout |
| A82-14 | INFO | CookieList | Zero test coverage |
| A82-15 | INFO | CookieList | Not referenced by application code (dead code) |
| A82-16 | LOW | CookieList | Uses raw `Iterator` type (no generics) |
| A82-17 | LOW | CookieList | `toJSONObject` does not handle missing `=` separator gracefully |
| A82-18 | INFO | CookieList | Inherits non-ASCII encoding defects from `Cookie` |

---

## Key Observations (Vendored Library Context)

1. **None of the three classes are used by any application code.** The application uses `javax.servlet.http.Cookie` for HTTP cookie handling and `com.json.JSONObject`/`com.json.JSONArray` for JSON processing. `CDL`, `Cookie` (com.json), and `CookieList` are entirely unused dead code bundled from the vendored org.json library.

2. **No application-specific modifications are present.** All three files carry the standard JSON.org copyright header with `@version 2010-12-24`. Package declaration is changed from `org.json` to `com.json` (standard for this vendored bundle), but no logic has been altered.

3. **No specific behaviors of these classes are relied upon by the application**, so there is no scenario where behavioral regression in these classes would affect the application in its current state.

4. **The primary risk** is the presence of 15-year-old, untested, dead code increasing the codebase's attack surface and maintenance burden. The most actionable remediation would be to remove all three files if CDL/Cookie/CookieList functionality is confirmed unused.
