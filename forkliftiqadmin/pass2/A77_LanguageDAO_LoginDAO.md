# Pass 2 Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A77
**Date:** 2026-02-26
**Source Files Audited:**
- `src/main/java/com/dao/LanguageDAO.java`
- `src/main/java/com/dao/LoginDAO.java`

---

## Test Directory Search Results

**Test files present in** `src/test/java/`:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

**Grep result for `LanguageDAO` in test directory:** No matches found.
**Grep result for `LoginDAO` in test directory:** No matches found.

Both classes have **zero test coverage**.

---

## File 1: LanguageDAO.java

### Reading Evidence

**Class name:** `LanguageDAO`
**Package:** `com.dao`
**Full path:** `src/main/java/com/dao/LanguageDAO.java`

**Fields:**

| Field | Line | Type | Modifier |
|-------|------|------|----------|
| `log` | 17 | `Logger` | `private static` |
| `instance` | 19 | `LanguageDAO` | `private static` |

**Methods:**

| Method | Line | Modifier | Notes |
|--------|------|----------|-------|
| `getInstance()` | 21 | `public static` | Double-checked locking singleton |
| `LanguageDAO()` (constructor) | 32 | `private` | No-op |
| `getAllLan()` | 36 | `public` | Returns `ArrayList<LanguageBean>`, throws `Exception` |

---

### LanguageDAO Findings

**A77-1 | Severity: CRITICAL | No test class exists for LanguageDAO**
There is no test file in `src/test/java/` that references `LanguageDAO`. The entire class — singleton factory, database query logic, result mapping, exception propagation, and resource cleanup — is untested.

**A77-2 | Severity: HIGH | `getAllLan()` has no test for empty result set**
When the `language` table contains no rows, `getAllLan()` returns an empty `ArrayList`. There is no test verifying that an empty list (not null) is returned, and that callers handle it without a NullPointerException or silent data loss.

**A77-3 | Severity: HIGH | `getAllLan()` exception-handling path is untested**
The catch block at line 62 catches all `Exception`, logs it, prints the stack trace, and then re-throws as `new SQLException(e.getMessage())`. The re-throw loses the original cause chain (`initCause` is not set), and there is no test verifying that a database failure propagates correctly or that resources are closed in that path.

**A77-4 | Severity: HIGH | `getAllLan()` uses `Statement` (non-parameterized) with a fully static SQL string**
The SQL `select id,name from language` (line 50) is static and carries no injection risk itself, but the use of `ResultSet.TYPE_SCROLL_SENSITIVE` on line 48 is unnecessarily expensive for a forward-only read. No test verifies correct result mapping or that column indices (1, 2) correspond to `id` and `name` rather than using column names, making the query fragile to column-order changes.

**A77-5 | Severity: MEDIUM | Singleton `getInstance()` is untested for thread-safety correctness**
The double-checked locking pattern (lines 22–29) is implemented without a `volatile` keyword on `instance` (line 19). Without `volatile`, the Java Memory Model does not guarantee that the partially constructed object is not visible to another thread. No test exercises concurrent access to `getInstance()`.

**A77-6 | Severity: MEDIUM | `getAllLan()` result mapping uses column indices instead of column names**
Lines 57–58 call `rs.getString(1)` and `rs.getString(2)`. If the column order in the database view or table changes, the mapping silently produces wrong data. No test pins the expected mapping of `id` and `name` to the correct fields.

**A77-7 | Severity: MEDIUM | `finally` block does not handle `ResultSet.close()` or `Statement.close()` exceptions**
Lines 69–71: each `close()` call is made separately. If `rs.close()` throws, `stmt.close()` and `DBUtil.closeConnection(conn)` will still be called (since they are separate statements), but any exception from `rs.close()` is silently swallowed. No test verifies resource cleanup under failure conditions.

**A77-8 | Severity: LOW | Log message at line 42 incorrectly identifies the class as `TimezoneDAO`**
`log.info("Inside TimezoneDAO Method : getAllLan")` is a copy-paste error. The method belongs to `LanguageDAO`. No test detects or checks log output, so this mislabelling will persist undetected in production logs.

**A77-9 | Severity: LOW | `getInstance()` is untested for repeated calls returning the same instance**
No test asserts that two successive calls to `LanguageDAO.getInstance()` return the identical object reference, which is a basic singleton contract test.

**A77-10 | Severity: INFO | `DBUtil.closeConnection()` is `@Deprecated` but still called**
Line 71 calls `DBUtil.closeConnection(conn)`, which is marked `@Deprecated` in `DBUtil.java` (line 57). The preferred approach is `DbUtils.closeQuietly()`. No test flags this usage.

---

## File 2: LoginDAO.java

### Reading Evidence

**Class name:** `LoginDAO`
**Package:** `com.dao`
**Full path:** `src/main/java/com/dao/LoginDAO.java`

**Fields:**

| Field | Line | Type | Modifier |
|-------|------|------|----------|
| `log` | 15 | `Logger` | `private static` |
| `instance` | 17 | `LoginDAO` | `private static` |

**Methods:**

| Method | Line | Modifier | Notes |
|--------|------|----------|-------|
| `getInstance()` | 19 | `public static` | Double-checked locking singleton |
| `LoginDAO()` (constructor) | 30 | `private` | No-op |
| `getCompanyId(String username)` | 34 | `public static` | Returns `Integer`, throws `SQLException` |
| `getUserId(String username)` | 40 | `public static` | Returns `Integer`, throws `SQLException` |
| `checkLogin(String username, String password)` | 47 | `public` | Returns `Boolean`, throws `Exception` |
| `isUserAuthority(int userId, String authority)` | 59 | `public static` | Returns `Boolean`, throws `Exception` |
| `isAuthority(String compId, String authority)` | 71 | `public static` | Returns `Boolean`, throws `Exception` |
| `getCompanies(Boolean, Boolean, String, String, int)` | 86 | `public` | Returns `List<CompanyBean>`, throws `Exception` |
| `getCompanies(Boolean, Boolean, Integer)` | 104 | `public static` | Returns `List<CompanyBean>`, throws `SQLException` |
| `getSuperAdminCompanies()` | 111 | `private static` | Returns `List<CompanyBean>`, throws `SQLException` |
| `getDealerCompanies(int companyId)` | 186 | `private static` | Returns `List<CompanyBean>`, throws `SQLException` |
| `getSimpleCompanies(int companyId)` | 235 | `private static` | Returns `List<CompanyBean>`, throws `SQLException` |

---

### LoginDAO Findings

**A77-11 | Severity: CRITICAL | No test class exists for LoginDAO**
There is no test file in `src/test/java/` that references `LoginDAO`. All authentication, authorization, and company-lookup logic is completely untested.

**A77-12 | Severity: CRITICAL | `checkLogin()` uses MD5 for password hashing (line 51)**
The query `where email = ? and password = md5(?)` hashes passwords with MD5 in the SQL layer. MD5 is cryptographically broken, does not use salting, and is trivially reversible via rainbow tables. A database breach exposes all user passwords. No test enforces or documents the expected hashing scheme, and there is no test that would catch a future secure-hash migration. This is an authentication security defect, not merely a coverage gap.

**A77-13 | Severity: CRITICAL | `getCompanies(Boolean, Boolean, String, String, int)` also uses MD5 for company password lookup (line 92–96)**
The query `select id from company where email = ? and password = md5(?)` applies the same broken MD5 hash to company credentials. This is a second independent authentication path with the same cryptographic weakness.

**A77-14 | Severity: CRITICAL | `checkLogin()` empty-result behaviour is masked — user-not-found treated as authentication exception**
At line 56, `.orElseThrow(SQLException::new)` is called on the `Optional` returned by `DBUtil.queryForObject()`. However, reviewing `DBUtil.queryForObject()` (lines 148–170): if the `count(*)` query returns a row (which `count(*)` always does, even when no users match), `rs.next()` is always true, so the `Optional` is never empty. The mapper `rs -> rs.getInt(1) > 0` returns `false` for count = 0 (user not found). This means `checkLogin()` returns `false` for a non-existent user — which is the correct observable behaviour — but the `.orElseThrow()` branch is dead code that is never exercised and never tested. This creates a dangerous false sense of security around the empty-result code path.

**A77-15 | Severity: CRITICAL | `isAuthority()` (line 71) takes `compId` as `String` and calls `Integer.parseInt(compId)` without validation (line 80)**
If `compId` is null or non-numeric, `Integer.parseInt()` throws a `NumberFormatException`, which is not caught and will propagate as an unhandled runtime exception. No test covers null, empty string, or non-numeric `compId` inputs.

**A77-16 | Severity: HIGH | `getCompanyId()` and `getUserId()` return 0 on user-not-found instead of an empty/null signal (lines 37, 43)**
Both methods call `.orElse(0)`, returning `0` when no matching record is found. `0` is a valid database primary key in some systems, creating an ambiguity between "no user found" and "user with id=0 found". No test verifies the not-found case or documents the 0-as-sentinel contract.

**A77-17 | Severity: HIGH | `checkLogin()` is an instance method while `getCompanyId()`, `getUserId()`, and `isUserAuthority()` are static methods on the same class**
The inconsistent mixing of instance and static methods on a singleton means callers can use either `LoginDAO.getInstance().checkLogin(...)` or the static forms directly. The singleton pattern is effectively bypassed for static methods. No test enforces or documents the intended call contract.

**A77-18 | Severity: HIGH | `getSuperAdminCompanies()` contains a typo in a table name: `compnay_role_rel` (lines 124, 192, 241)**
The join condition `left outer join compnay_role_rel as cr` uses the misspelled table name `compnay_role_rel`. If the actual database table is named `company_role_rel`, all three affected queries — `getSuperAdminCompanies()`, `getDealerCompanies()`, and `getSimpleCompanies()` — will silently fail or return incorrect data depending on whether the database schema also has the typo. Because `DBUtil.queryForObjectsWithRowHandler()` swallows `SQLException` (line 98–99 of DBUtil), the failure would be silent. No test catches this.

**A77-19 | Severity: HIGH | `DBUtil.queryForObjectsWithRowHandler()` silently swallows `SQLException` — all company-fetch failures are invisible**
`getSuperAdminCompanies()`, `getDealerCompanies()`, and `getSimpleCompanies()` all delegate to `DBUtil.queryForObjectsWithRowHandler()`, which catches `SQLException` and prints the stack trace but returns an empty list rather than re-throwing (DBUtil lines 98–100). A database outage, broken table reference, or bad query will silently return an empty company list, causing login to behave as if no companies exist. No test verifies error propagation from these paths.

**A77-20 | Severity: HIGH | `getCompanies(Boolean, Boolean, String, String, int)` (line 86) passes `username` and `password` in cleartext as method parameters**
The method signature exposes plaintext credentials at the Java stack level, increasing the attack surface for heap dumps, thread dumps, and logging of method arguments. The password is also used directly in an MD5 SQL hash (line 95). No test validates that password values are not logged.

**A77-21 | Severity: HIGH | `getSuperAdminCompanies()` hardcodes the authority role `RuntimeConf.ROLE_DEALER` (line 146) for all parent companies regardless of actual role data**
All parent companies returned by the super-admin query have their authority forced to `RuntimeConf.ROLE_DEALER` (line 146), overriding whatever `rl.authority` value is in the database. This is a logic defect that could grant incorrect authority levels. No test verifies the authority assignment logic.

**A77-22 | Severity: MEDIUM | `getCompanies(Boolean, Boolean, Integer)` (line 104) returns an empty list when `company` is null (line 106) without logging or error indication**
If `company` is null and `isSuperAdmin` is false, an empty `ArrayList` is silently returned. This could mask a misconfigured session where the company ID was never set. No test covers this code path.

**A77-23 | Severity: MEDIUM | Singleton `getInstance()` uses the same non-volatile double-checked locking pattern as LanguageDAO**
`instance` at line 17 is not declared `volatile`. Under the Java Memory Model, this exposes a data race where a partially initialized `LoginDAO` instance could be observed by a concurrent thread. The authentication singleton is at particular risk because correctness matters. No test exercises concurrent initialization.

**A77-24 | Severity: MEDIUM | `isUserAuthority()` and `isAuthority()` both log the message "Inside LoginDAO Method : isAuthority" (lines 60, 72)**
`isUserAuthority()` uses the same log string as `isAuthority()`, making it impossible to distinguish which method was called from log output alone. No test verifies log output.

**A77-25 | Severity: MEDIUM | `getDealerCompanies()` parameter binding sets 6 parameters for a UNION ALL query (lines 207–213) — parameter index correctness is untested**
The six `stmt.setXxx()` calls must exactly correspond to the six `?` placeholders across both halves of the UNION ALL. Any off-by-one in the parameter positions would produce silently wrong results or a `SQLException`. No test verifies the parameter binding for any of the three company-fetch private methods.

**A77-26 | Severity: MEDIUM | `getCompanies(Boolean, Boolean, String, String, int)` falls back to the `comp` parameter value (line 97) when the company email/password lookup returns no row**
`.orElse(comp)` means that if no company record matches the provided credentials, the method silently continues using whatever `comp` value was passed in. This is a potential authentication bypass: a failed company credential lookup does not abort the login flow. No test verifies this fallback behaviour or documents it as intentional.

**A77-27 | Severity: LOW | `v_user` is a database view name stored in `RuntimeConf.v_user` (line 64 of RuntimeConf) and interpolated directly into SQL strings via string concatenation**
Although the interpolated value comes from a compile-time constant (`"v_cognitousers"`), the pattern of string concatenation in SQL construction (e.g., lines 35, 41, 51, 63, 74) is a structural code smell that, if `RuntimeConf.v_user` were ever made configurable at runtime, would become a SQL injection vector. No test enforces that `v_user` remains a safe, fixed constant.

**A77-28 | Severity: LOW | `getInstance()` is untested for repeated calls returning the same reference**
No test asserts the singleton contract: that two successive calls to `LoginDAO.getInstance()` return the identical object.

**A77-29 | Severity: INFO | `getDealerCompanies()` query filters on `rl.authority` in the WHERE clause while simultaneously using a CASE expression to substitute a null authority**
Lines 196 and 206: `where company.id = ? and rl.authority = ?` combined with `case when rl.authority is null then ? else rl.authority end` is logically inconsistent — the WHERE clause excludes rows where `rl.authority` is null, so the CASE's null branch is dead code. No test validates the actual row set returned.

**A77-30 | Severity: INFO | `CompanyBean` uses a Lombok-style builder pattern but no test validates that all builder fields are correctly populated from ResultSet column names**
All three private company-fetch methods construct `CompanyBean` instances using `.builder()...build()` with column-name-based `rs.getString()` calls. A column rename in the schema would cause a `SQLException` at runtime with no compile-time signal. No test catches schema/mapping mismatches.

---

## Coverage Summary

| Class | Test File Found | Methods Covered | Methods Total | Coverage |
|-------|----------------|-----------------|---------------|----------|
| `LanguageDAO` | None | 0 | 3 (excl. private constructor) | 0% |
| `LoginDAO` | None | 0 | 10 (excl. private constructor) | 0% |

---

## Finding Count by Severity

| Severity | Count |
|----------|-------|
| CRITICAL | 6 (A77-1, A77-11, A77-12, A77-13, A77-14, A77-15) |
| HIGH | 9 (A77-3, A77-4, A77-16, A77-17, A77-18, A77-19, A77-20, A77-21, A77-25) |
| MEDIUM | 9 (A77-2, A77-5, A77-6, A77-7, A77-22, A77-23, A77-24, A77-26) |
| LOW | 5 (A77-8, A77-9, A77-10, A77-27, A77-28) |
| INFO | 3 (A77-29, A77-30, A77-25 duplicate note — see A77-25) |
| **Total** | **30** |

---

*Report generated by Agent A77 — Pass 2 Test Coverage Audit — 2026-02-26-01*
