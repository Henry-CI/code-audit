# Pass 3 Documentation Audit — A77
**Audit run:** 2026-02-26-01
**Agent:** A77
**Files:** dao/LanguageDAO.java, dao/LoginDAO.java

---

## 1. Reading Evidence

### 1.1 LanguageDAO.java

**Class:** `LanguageDAO` — line 15

**Fields:**

| Name | Type | Line |
|------|------|------|
| `log` | `static Logger` | 17 |
| `instance` | `static LanguageDAO` | 19 |

**Methods:**

| Name | Visibility | Line |
|------|-----------|------|
| `getInstance()` | `public static` | 21 |
| `LanguageDAO()` (constructor) | `private` | 32 |
| `getAllLan()` | `public` | 36 |

---

### 1.2 LoginDAO.java

**Class:** `LoginDAO` — line 13

**Fields:**

| Name | Type | Line |
|------|------|------|
| `log` | `static Logger` | 15 |
| `instance` | `static LoginDAO` | 17 |

**Methods:**

| Name | Visibility | Line |
|------|-----------|------|
| `getInstance()` | `public static` | 19 |
| `LoginDAO()` (constructor) | `private` | 30 |
| `getCompanyId(String)` | `public static` | 34 |
| `getUserId(String)` | `public static` | 40 |
| `checkLogin(String, String)` | `public` | 47 |
| `isUserAuthority(int, String)` | `public static` | 59 |
| `isAuthority(String, String)` | `public static` | 71 |
| `getCompanies(Boolean, Boolean, String, String, int)` | `public` | 86 |
| `getCompanies(Boolean, Boolean, Integer)` | `public static` | 104 |
| `getSuperAdminCompanies()` | `private static` | 111 |
| `getDealerCompanies(int)` | `private static` | 186 |
| `getSimpleCompanies(int)` | `private static` | 235 |

---

## 2. Findings

### A77-1 [LOW] — LanguageDAO: missing class-level Javadoc

**File:** `dao/LanguageDAO.java`, line 15

No `/** ... */` block appears above the `public class LanguageDAO` declaration. The purpose of this class (singleton DAO for language look-ups), its threading model, and its database dependency are undocumented at the class level.

---

### A77-2 [MEDIUM] — LanguageDAO.getInstance(): undocumented non-trivial public method

**File:** `dao/LanguageDAO.java`, line 21

`getInstance()` implements a double-checked locking singleton pattern. No Javadoc is present. The threading guarantees and the lazy-initialisation behaviour are non-obvious and warrant documentation.

---

### A77-3 [MEDIUM] — LanguageDAO.getAllLan(): undocumented non-trivial public method

**File:** `dao/LanguageDAO.java`, line 36

`getAllLan()` executes a SQL query, maps results to `LanguageBean` objects, and returns an `ArrayList`. No Javadoc comment is present. Missing documentation covers: what is returned, the exception that is declared (`throws Exception`, re-thrown as `SQLException`), and the fact that the internal log message on line 42 mis-identifies the class as `TimezoneDAO` (see A77-4).

---

### A77-4 [MEDIUM] — LanguageDAO.getAllLan(): inaccurate log message (wrong class name)

**File:** `dao/LanguageDAO.java`, line 42

```java
log.info("Inside TimezoneDAO Method : getAllLan");
```

The method is inside `LanguageDAO`, not `TimezoneDAO`. This is a copy-paste error that will produce misleading log output and impede debugging. Classified MEDIUM (inaccurate comment / log string, not security-critical).

---

### A77-5 [LOW] — LoginDAO: missing class-level Javadoc

**File:** `dao/LoginDAO.java`, line 13

No `/** ... */` block is present above `public class LoginDAO`. The class's role (authentication and company-resolution DAO), its singleton pattern, and the static-method design are not documented.

---

### A77-6 [MEDIUM] — LoginDAO.getInstance(): undocumented non-trivial public method

**File:** `dao/LoginDAO.java`, line 19

Same double-checked locking singleton as in `LanguageDAO`. No Javadoc present.

---

### A77-7 [MEDIUM] — LoginDAO.getCompanyId(String): undocumented non-trivial public method

**File:** `dao/LoginDAO.java`, line 34

```java
public static Integer getCompanyId(String username) throws SQLException
```

No Javadoc. The method queries the view referenced by `RuntimeConf.v_user`, uses `DISTINCT`, and returns `0` when no row is found. The `0`-as-sentinel convention is non-obvious and should be documented. Missing `@param username` and `@return` tags.

---

### A77-8 [MEDIUM] — LoginDAO.getUserId(String): undocumented non-trivial public method

**File:** `dao/LoginDAO.java`, line 40

```java
public static Integer getUserId(String username) throws SQLException
```

No Javadoc. Same concerns as A77-7: `0`-as-sentinel return value is undocumented. Missing `@param username` and `@return` tags.

---

### A77-9 [MEDIUM] — LoginDAO.checkLogin(String, String): undocumented non-trivial public method

**File:** `dao/LoginDAO.java`, line 47

```java
public Boolean checkLogin(String username, String password) throws Exception
```

No Javadoc. The method verifies credentials using MD5 hashing of the password inside SQL (`md5(?)`). The hashing detail is security-relevant and should be documented. Missing `@param username`, `@param password`, and `@return` tags.

---

### A77-10 [MEDIUM] — LoginDAO.isUserAuthority(int, String): undocumented non-trivial public method

**File:** `dao/LoginDAO.java`, line 59

```java
public static Boolean isUserAuthority(int userId, String authority) throws Exception
```

No Javadoc. Method checks whether a user row has a given `authority` column value. The internal log message on line 61 says `"Inside LoginDAO Method : isAuthority"` — missing the `User` qualifier — but this is a minor inaccuracy in a log string rather than dangerous misleading documentation. Missing `@param userId`, `@param authority`, and `@return` tags.

---

### A77-11 [MEDIUM] — LoginDAO.isAuthority(String, String): undocumented non-trivial public method

**File:** `dao/LoginDAO.java`, line 71

```java
public static Boolean isAuthority(String compId, String authority) throws Exception
```

No Javadoc. This overload checks authority at the company level (via `company`, `compnay_role_rel`, and `roles` tables), whereas `isUserAuthority` checks at the user level. The distinction between these two methods is entirely undocumented and likely to cause confusion. Missing `@param compId`, `@param authority`, and `@return` tags.

---

### A77-12 [MEDIUM] — LoginDAO.getCompanies(Boolean, Boolean, String, String, int): undocumented non-trivial public method

**File:** `dao/LoginDAO.java`, line 86

```java
public Boolean getCompanies(Boolean isSuperAdmin, Boolean isDealerLogin, String username, String password, int comp) throws Exception
```

No Javadoc. The method uses `username` and `password` to resolve the authoritative `company_id` from the database, falling back to the `comp` parameter when no database row is found (`orElse(comp)`). The fallback behaviour and the priority ordering (super-admin -> dealer -> simple) are undocumented. Missing `@param` tags for all five parameters and `@return`.

---

### A77-13 [MEDIUM] — LoginDAO.getCompanies(Boolean, Boolean, Integer): undocumented non-trivial public method

**File:** `dao/LoginDAO.java`, line 104

```java
public static List<CompanyBean> getCompanies(Boolean isSuperAdmin, Boolean isDealer, Integer company) throws SQLException
```

No Javadoc. This overload omits the credential-based DB lookup performed by the instance overload (A77-12) and returns an empty list when `company` is `null`. The differences from the other overload and the null-safety behaviour are undocumented. Missing `@param` and `@return` tags.

---

### A77-14 [MEDIUM] — LoginDAO.isAuthority / isUserAuthority: log message does not distinguish the two methods

**File:** `dao/LoginDAO.java`, lines 61 and 73

Both `isUserAuthority` (line 61) and `isAuthority` (line 73) emit the identical log string:

```java
log.info("Inside LoginDAO Method : isAuthority");
```

`isUserAuthority` should log `"isUserAuthority"` to differentiate the two methods in log output. As-is, the log is inaccurate for `isUserAuthority`. Classified MEDIUM (inaccurate log/comment rather than dangerously wrong).

---

## 3. Summary Table

| ID | Severity | File | Location | Description |
|----|----------|------|----------|-------------|
| A77-1 | LOW | LanguageDAO.java | line 15 | No class-level Javadoc |
| A77-2 | MEDIUM | LanguageDAO.java | line 21 | `getInstance()` — no Javadoc |
| A77-3 | MEDIUM | LanguageDAO.java | line 36 | `getAllLan()` — no Javadoc |
| A77-4 | MEDIUM | LanguageDAO.java | line 42 | Log string says "TimezoneDAO" instead of "LanguageDAO" |
| A77-5 | LOW | LoginDAO.java | line 13 | No class-level Javadoc |
| A77-6 | MEDIUM | LoginDAO.java | line 19 | `getInstance()` — no Javadoc |
| A77-7 | MEDIUM | LoginDAO.java | line 34 | `getCompanyId()` — no Javadoc, missing @param/@return |
| A77-8 | MEDIUM | LoginDAO.java | line 40 | `getUserId()` — no Javadoc, missing @param/@return |
| A77-9 | MEDIUM | LoginDAO.java | line 47 | `checkLogin()` — no Javadoc, missing @param/@return |
| A77-10 | MEDIUM | LoginDAO.java | line 59 | `isUserAuthority()` — no Javadoc, missing @param/@return |
| A77-11 | MEDIUM | LoginDAO.java | line 71 | `isAuthority()` — no Javadoc, missing @param/@return |
| A77-12 | MEDIUM | LoginDAO.java | line 86 | `getCompanies(5-arg)` — no Javadoc, missing @param/@return |
| A77-13 | MEDIUM | LoginDAO.java | line 104 | `getCompanies(3-arg)` — no Javadoc, missing @param/@return |
| A77-14 | MEDIUM | LoginDAO.java | lines 61, 73 | `isUserAuthority` log string says "isAuthority" (wrong method name) |

**Total findings:** 14 (2 LOW, 12 MEDIUM, 0 HIGH)
