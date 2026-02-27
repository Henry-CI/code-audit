# Pass 4 — Code Quality: A01

## Reading Evidence

### APIDAO.java
- **Interface:** `APIDAO` (line 8)
- **Methods:**
  - `checkKey(String APIkey)` — line 10
  - `findByName(String username)` — line 11
- **Types/Constants:** imports `Driver` model
- **Blank lines:** lines 2-5 (excessive blank lines after package declaration)

### APIDAOImpl.java
- **Class:** `APIDAOImpl extends JdbcDaoSupport implements APIDAO` (line 18)
- **Annotations:** `@Component("apiDao")`, `@Transactional(readOnly = true)` (lines 16-17)
- **Methods:**
  - `setDbDataSource(DataSource)` — line 24 (autowired datasource setter)
  - `checkKey(String key)` — line 28
  - `findByName(String username)` — line 36
- **Types/Constants:** `Logger logger` (line 20)
- **Imports:** `DataSource`, `Logger`, `LoggerFactory`, `Autowired`, `Qualifier`, `Driver`, `JdbcDaoSupport`, `Component`, `Transactional`
- **Commented-out code:** line 30

### CompanyDAO.java
- **Class:** `CompanyDAO extends JdbcDaoSupport` (line 25)
- **Annotation:** `@Repository` (line 24)
- **Fields:**
  - `Configuration configuration` (line 28, autowired)
- **Methods:**
  - `setDbDataSource(DataSource)` — line 32
  - `save(Company, int, String, String)` — line 36
  - `findById(Long)` — line 62
  - `findAllByDriverId(Long)` — line 74
  - `findAllByKeyword(String)` — line 87
  - `mapCompany(ResultSet)` — line 160 (private static)
- **Inner Classes:**
  - `CompaniesResultResetExtractor` — line 98 (private static)
  - `CompanyResultResetExtractor` — line 136 (private static)
- **Types/Constants:** `BASE_QUERY_COMPANY` (line 52, private static final String)
- **Imports:** `Company`, `Driver`, `Permissions`, `Roles`, `Configuration`, `DataSource`, `DataAccessException`, `BeanPropertyRowMapper`, `JdbcTemplate`, `ResultSetExtractor`, `JdbcDaoSupport`, `Repository`, `ResultSet`, `SQLException`, `ArrayList`, `List`, `Optional`

## Findings

### A01-1: APIDAO and APIDAOImpl are dead code — never referenced — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/APIDAO.java` (entire file), `src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java` (entire file)
**Line(s):** All
**Description:** Neither `APIDAO` nor `APIDAOImpl` nor the Spring bean `apiDao` is referenced anywhere outside these two files. No controller, service, or other component injects or uses them. The `@Component("apiDao")` bean is registered in the Spring context but never consumed. These classes appear to be leftover scaffolding or abandoned prototype code and should be removed to reduce confusion and context-scan noise.

### A01-2: `checkKey()` is a stub that always returns true — CRITICAL
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java`
**Line(s):** 28-34
**Description:** The `checkKey` method logs the provided key and unconditionally returns `true` without performing any actual key validation. It contains a commented-out SQL INSERT statement that is unrelated to key-checking logic. If this method were ever wired into an authentication or authorization flow, it would accept any API key. Even though the class is currently dead code (see A01-1), the stub implementation is a security risk if the class is ever integrated.

### A01-3: Commented-out code left in `checkKey` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java`
**Line(s):** 30
**Description:** Line 30 contains a commented-out SQL INSERT statement: `//String sql = "INSERT INTO CUSTOMER (CUST_ID, NAME, AGE) VALUES (?, ?, ?)";`. This appears to be copied from a tutorial/example (the table name `CUSTOMER` and columns `CUST_ID, NAME, AGE` are typical JournalDev tutorial artifacts) and has no relevance to the method. Commented-out code adds noise and should be removed.

### A01-4: Misleading log message in `findByName` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java`
**Line(s):** 37
**Description:** The log message reads `"Start checkKey for : {}"` but the method is `findByName`. This is a copy-paste error from `checkKey()` that would make log analysis confusing when debugging. The message should reference `findByName`.

### A01-5: `queryForObject` with `Driver.class` will fail at runtime — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java`
**Line(s):** 40
**Description:** `getJdbcTemplate().queryForObject(sql, Driver.class, username)` uses the `queryForObject(String, Class<T>, Object...)` overload which expects a `SingleColumnRowMapper`. Since `Driver` is a complex bean (not a simple type like String, Integer, etc.), Spring will throw an `IncorrectResultSetColumnCountException` at runtime. A `BeanPropertyRowMapper<>(Driver.class)` or custom `RowMapper` is required. Although this class is currently dead code, if integrated it would produce a runtime exception.

### A01-6: `findByName` queries by MD5 of email, not by name — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java`
**Line(s):** 38
**Description:** The method is named `findByName` and accepts a parameter called `username`, but the SQL query is `select * from tblusers where md5(email) = ?`. This is semantically misleading — it finds a user by MD5 hash of their email, not by name. The interface declares `findByName(String username)` further propagating the mismatch. Method naming should reflect what the query actually does.

### A01-7: `@Transactional(readOnly = true)` on class with no actual database reads — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java`
**Line(s):** 17
**Description:** The class-level `@Transactional(readOnly = true)` annotation applies to all methods, but `checkKey()` does not interact with the database at all, and `findByName()` queries `tblusers` which is a different table/view than what `CompanyDAO` uses. The transactional annotation is not harmful but is a style inconsistency — the class is annotated `@Component` while similar DAOs in the project use `@Repository`.

### A01-8: Unused imports in CompanyDAO — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java`
**Line(s):** 11-12
**Description:** `BeanPropertyRowMapper` (line 11) and `JdbcTemplate` (line 12) are imported but never used directly in the file. `JdbcTemplate` access comes through the inherited `getJdbcTemplate()` method from `JdbcDaoSupport`, and `BeanPropertyRowMapper` is not used anywhere. These unused imports will produce compiler warnings and should be removed.

### A01-9: NullPointerException in `CompanyResultResetExtractor.extractData` when result set is empty — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java`
**Line(s):** 139-157, specifically line 154
**Description:** In `CompanyResultResetExtractor.extractData()`, if the `ResultSet` is empty (no rows), the `while` loop never executes, `cie` remains `null`, and line 154 (`cie.setArrRoles(roles)`) will throw a `NullPointerException`. This method is invoked by `findById()` (line 66), and the result is wrapped in `Optional.ofNullable()` at line 70, suggesting the caller expects a possible null — but the extractor crashes before returning null. The extractor should guard against `cie == null` before calling `setArrRoles`.

### A01-10: `CompaniesResultResetExtractor` loses roles for the last company if only one company in result — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java`
**Line(s):** 98-134, specifically 108-126
**Description:** In `CompaniesResultResetExtractor`, when the result set contains only one company, `previousCompanyId` starts as `null` and `companyId != previousCompanyId` is always `true` on the first row (due to Long object comparison via `!=`). For subsequent rows of the same company, `companyId != previousCompanyId` compares two `Long` objects by reference, not by value. For company IDs > 127 (outside the Long cache range), this comparison will incorrectly evaluate to `true`, causing the same company to be added multiple times to the list and roles to be incorrectly partitioned. The comparison should use `!companyId.equals(previousCompanyId)`.

### A01-11: `save()` method stores password as MD5 hash — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java`
**Line(s):** 41
**Description:** The SQL `insert into company ... md5(?)` uses the PostgreSQL `md5()` function to hash the password. MD5 is cryptographically broken and unsuitable for password storage. Modern password hashing should use bcrypt, scrypt, or Argon2. Additionally, this is done in the SQL layer with no salting, making it vulnerable to rainbow table attacks.

### A01-12: `save()` method lacks transactional annotation — multi-statement insert without atomicity — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java`
**Line(s):** 36-50
**Description:** The `save()` method performs four distinct database operations (sequence fetch, company insert, role-relation inserts in a loop, permission insert). If any statement after the first insert fails, the database will be left in an inconsistent state with a partially created company. The class lacks `@Transactional` and the method is not annotated either. The related `CompanyController` or service layer should be checked to see if a transaction is managed upstream, but at the DAO level this is a gap.

### A01-13: Deprecated `new Object[]{}` parameter style in JdbcTemplate calls — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java`
**Line(s):** 42, 47, 67, 80, 92
**Description:** Multiple calls use the `new Object[] { ... }` form to pass parameters to JdbcTemplate methods (e.g., `getJdbcTemplate().update(sql, new Object[] {...})`). Since Spring Framework 5, the varargs overloads are preferred and the `Object[]` variants are deprecated. This will produce deprecation warnings during compilation.

### A01-14: Inner class names contain typo "Reset" instead of "Result" — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java`
**Line(s):** 98, 136
**Description:** The inner classes are named `CompaniesResultResetExtractor` and `CompanyResultResetExtractor`. The word "Reset" appears to be a typo for "Result" (as in "ResultSet Extractor"). While functionally harmless, this naming error reduces readability and suggests the code was not thoroughly reviewed.

### A01-15: Mixed column-index and column-name access in `mapCompany` — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java`
**Line(s):** 160-195, specifically 183-189 vs 163-172
**Description:** The `mapCompany` method accesses `Driver` fields by column name (e.g., `rs.getString("first_name")`) but accesses `Company` fields by column index (e.g., `rs.getLong(1)`, `rs.getString(2)`). This inconsistency makes the code fragile — if the query column order ever changes, the Company mapping will silently return wrong data, while the Driver mapping would still work correctly. All accesses should use named columns for maintainability.
# Pass 4 — Code Quality: A02

## Reading Evidence

### DriverDAO.java
- **Interface:** `DriverDAO` (line 11)
- **Package:** `com.journaldev.spring.jdbc.DAO`
- **Methods:**
  - `isDriverExist(String email)` — line 12, returns `boolean`
  - `findByID(int userId)` — line 13, returns `Driver`, throws `EntityNotFoundException`
  - `findAllByCompanyOwner(int ownerId)` — line 14, returns `List<Driver>`
  - `findAllTraining(int driverId)` — line 15, returns `List<DriverTraining>`
  - `save(Driver user)` — line 16, returns `int`
  - `update(Driver user)` — line 17, returns `Driver`, throws `SQLException`
  - `updateLastLoginTime(Driver driver)` — line 18, returns `Driver`, throws `SQLException`
  - `updatePassword(String email, String password)` — line 19, returns `void`, throws `SQLException`
  - `findByEmailAndPassword(String email, String password)` — line 22, returns `Optional<Driver>`, annotated `@Deprecated`
- **Imports:** `Driver`, `DriverTraining`, `EntityNotFoundException`, `java.sql.SQLException`, `java.util.List`, `java.util.Optional`
- **Annotations:** `@Deprecated` on `findByEmailAndPassword`

### DriverDAOImpl.java
- **Class:** `DriverDAOImpl` (line 22), extends `JdbcDaoSupport`, implements `DriverDAO`
- **Package:** `com.journaldev.spring.jdbc.DAO`
- **Annotations:** `@Repository`, `@Slf4j`
- **Constants:**
  - `BASE_QUERY_DRIVER` — line 23-28, `private static final String`
  - `UPDATE_PASSWORD` — line 90, `private static final String`
- **Fields:**
  - `configuration` — line 31, `@Autowired Configuration`
- **Methods:**
  - `setDbDataSource(DataSource dataSource)` — line 35, `@Autowired @Qualifier("dataSource")`
  - `isDriverExist(String email)` — line 40, `@Override`
  - `save(Driver user)` — line 48, `@Override`
  - `update(Driver driver)` — line 63, `@Override`
  - `updateLastLoginTime(Driver driver)` — line 77, `@Override`
  - `updatePassword(String email, String password)` — line 93, `@Override`
  - `findByID(int userId)` — line 102, `@Override`
  - `findByEmailAndPassword(String email, String password)` — line 120, `@Override`
  - `findAllByCompanyOwner(int ownerId)` — line 138, `@Override`
  - `findAllTraining(int driverId)` — line 151, `@Override`
- **Imports:** `Driver`, `DriverTraining`, `EntityNotFoundException`, `Configuration`, `lombok.extern.slf4j.Slf4j`, Spring JDBC classes (`JdbcDaoSupport`, `BeanPropertyRowMapper`, `EmptyResultDataAccessException`), `javax.sql.DataSource`, `java.sql.SQLException`, `java.util.List`, `java.util.Optional`
- **Exception handling:** `EmptyResultDataAccessException` caught in `findByID` (rethrown as `EntityNotFoundException`) and `findByEmailAndPassword` (swallowed, returns `Optional.empty`)

### EmailLayoutDAO.java
- **Class:** `EmailLayoutDAO` (line 11), plain class (no Spring annotation, no interface)
- **Package:** `com.journaldev.spring.jdbc.DAO`
- **Fields:**
  - `jdbcTemplate` — line 12, `private JdbcTemplate`
  - `logger` — line 13, `private static final Logger` (SLF4J)
- **Methods:**
  - `EmailLayoutDAO(DataSource dataSource)` — line 16, constructor
  - `getEmailLayoutByType(String type)` — line 21, returns `EmailLayout`
- **Imports:** `javax.sql.DataSource`, `org.slf4j.Logger`, `org.slf4j.LoggerFactory`, `org.springframework.jdbc.core.JdbcTemplate`, `com.journaldev.spring.jdbc.model.EmailLayout`

---

## Findings

### A02-1: Likely wrong column name `iduser` in `update()` SQL — CRITICAL
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java`
**Line(s):** 66
**Description:** The `update()` method's SQL WHERE clause references `iduser` (`where iduser = ?`), while every other method in the class and the table's schema (inferred from `save()` at line 55 and `updateLastLoginTime()` at line 80) use `id` as the primary key column name. A codebase-wide search confirms `iduser` appears only on this single line. This almost certainly means `update()` will fail at runtime with a SQL error or silently match zero rows (triggering the `SQLException` on line 70), making the method non-functional. This is a latent bug.

### A02-2: `getEmailLayoutByType` is an unimplemented stub returning empty object — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/EmailLayoutDAO.java`
**Line(s):** 21-28
**Description:** The method accepts a `type` parameter but never uses it. It creates a `new EmailLayout()`, executes no query, populates no fields, and returns the empty object. Any caller receives an object with `id=0` and all String fields `null`. The `jdbcTemplate` field (line 12) and `logger` field (line 13) are both unused. This is dead code shipped into production — the entire class body is non-functional.

### A02-3: Deprecated `findByEmailAndPassword` lacks `@Deprecated` annotation attributes and Javadoc migration guidance — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAO.java`
**Line(s):** 21-22
**Description:** The interface method is annotated `@Deprecated` but provides no `since` or `forRemoval` attributes (Java 9+), no `@deprecated` Javadoc tag, and no indication of the replacement API. The implementation in `DriverDAOImpl` (line 120) does not repeat the `@Deprecated` annotation. Callers (e.g., `DriverService.java` line 54) continue to use this method with no compiler deprecation warning from the implementation side. This makes it difficult to plan the removal.

### A02-4: Redundant `p.enabled = true` predicate in `findAllByCompanyOwner` — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java`
**Line(s):** 27, 142
**Description:** `BASE_QUERY_DRIVER` already includes `inner join permission p on p.driver_id = d.id and p.enabled = true` (line 27). The `findAllByCompanyOwner` method appends an additional `where p.enabled = true` (line 142), creating a redundant predicate. While the database optimizer will likely eliminate the duplicate, it is a code smell indicating the developer did not realize the base query already filtered on this column. It also increases the risk of future inconsistencies if one clause is updated but not the other.

### A02-5: Deprecated `new Object[]{}` varargs pattern used throughout — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java`
**Line(s):** 110, 130, 146, 157
**Description:** Multiple calls to `getJdbcTemplate().queryForObject()` and `getJdbcTemplate().query()` use the explicit `new Object[]{...}` form (e.g., line 110: `new Object[]{url, userId}`). Since Spring Framework 5.x, the `Object[]` overloads of `JdbcTemplate.queryForObject` and `query` are deprecated in favor of varargs alternatives. This pattern generates compiler deprecation warnings and should be migrated to the varargs form or the newer `queryForObject(sql, rowMapper, args...)` signature.

### A02-6: `EmailLayoutDAO` is not Spring-managed and has inconsistent logging style — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/EmailLayoutDAO.java`
**Line(s):** 11-13
**Description:** Unlike `DriverDAOImpl` which uses `@Repository` and Lombok `@Slf4j`, `EmailLayoutDAO` is a plain class with manual `LoggerFactory.getLogger()`. It has no Spring stereotype annotation (`@Repository`, `@Component`), no interface, and manually creates a `JdbcTemplate` in its constructor rather than using Spring's `JdbcDaoSupport` or dependency injection. This inconsistency means it cannot be autowired and does not participate in Spring's exception translation. The `logger` field is declared but never used.

### A02-7: Misleading log message in `findAllTraining` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java`
**Line(s):** 152
**Description:** The log message reads `"Start findAllByCompanyOwner for ownerId : {}"` but the method is `findAllTraining` and the parameter is `driverId`. This is a copy-paste error from `findAllByCompanyOwner` (line 139). It will produce misleading log output in production, making debugging harder.

### A02-8: Interface declares checked `SQLException` but this leaks JDBC implementation detail — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAO.java`
**Line(s):** 17-19
**Description:** The `DriverDAO` interface methods `update`, `updateLastLoginTime`, and `updatePassword` declare `throws SQLException`. This leaks the JDBC implementation detail into the interface contract. Spring's DAO pattern specifically wraps checked `SQLException` into unchecked `DataAccessException` subclasses. The implementation manually throws `new SQLException(...)` (lines 70, 84, 97) rather than using Spring's exception hierarchy, which is inconsistent with the framework conventions and forces callers to handle checked exceptions unnecessarily.

### A02-9: Inconsistent parameter naming between interface and implementation — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAO.java`, `src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java`
**Line(s):** DriverDAO.java:16-17 vs DriverDAOImpl.java:48,63
**Description:** The interface declares `save(Driver user)` and `update(Driver user)` with the parameter name `user`, but the implementation uses `user` for `save` (line 48) and `driver` for `update` (line 63). While this does not affect functionality, it signals inconsistent naming conventions and makes the API harder to reason about — a `Driver` entity is sometimes referred to as `user`.

### A02-10: `isDriverExist` method name is grammatically incorrect — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAO.java`
**Line(s):** 12
**Description:** The method is named `isDriverExist` but the conventional Java naming would be `doesDriverExist` or `isDriverExisting` or simply `driverExists`. This is a minor naming convention issue but appears in the public interface contract.
# Pass 4 — Code Quality: A03

## Reading Evidence

### EquipmentDAO.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAO.java`
- **Interface:** `EquipmentDAO`
- **Methods:**
  - `getEquipmentByUser(int userId)` — line 9
  - `getEquipmentIdByMacAddress(String macAddress)` — line 10
  - `getEquipmentByMacAddress(String macAddress)` — line 11
- **Types/Constants:** None
- **Imports:** `DriverEquipment`, `Equipment`, `java.util.List`

### EquipmentDAOImpl.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java`
- **Class:** `EquipmentDAOImpl extends JdbcDaoSupport implements EquipmentDAO`
- **Annotation:** `@Component("equipmentDAO")`
- **Fields:**
  - `private static final Logger logger` (SLF4J) — line 20
  - `private Configuration configuration` (@Autowired) — line 39
- **Constants:**
  - `QUERY_DRIVER_EQUIPMENT` — lines 22-32
  - `QUERY_EQUIPMENT_ID_BY_MAC_ADDRESS` — line 34
  - `QUERY_EQUIPMENT_BY_MAC_ADDRESS` — line 36
- **Methods:**
  - `setDbDataSource(DataSource dataSource)` — line 43
  - `getEquipmentByUser(int uid)` — line 47 (missing `@Override`)
  - `getEquipmentIdByMacAddress(String macAddress)` — line 53 (`@Override`)
  - `getEquipmentByMacAddress(String macAddress)` — line 58 (`@Override`)
- **Imports:** `DriverEquipment`, `Equipment`, `Roles` (UNUSED), `Configuration`, `Logger`, `LoggerFactory`, `Autowired`, `Qualifier`, `BeanPropertyRowMapper`, `JdbcDaoSupport`, `Component`, `DataSource`, `java.util.List`

### ImpactDAO.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java`
- **Class:** `ImpactDAO extends JdbcDaoSupport` (no interface)
- **Annotation:** `@Repository`
- **Fields:**
  - `private Configuration configuration` (@Autowired) — line 26
  - `private CognitoService cognitoService` (@Autowired) — line 35
- **Constants:**
  - `QUERY_FOR_EXISTING_IMPACT` — line 52
  - `QUERY_FOR_IMPACT_NOTIFICATIONS` — lines 57-63
- **Methods:**
  - `setDbDataSource(DataSource dataSource)` — line 30
  - `save(Long equipmentId, Impact impact)` — line 37
  - `isImpactRecorded(Impact impact)` — line 53
  - `sendImpactNotification(Equipment equipment, Impact impact)` — line 64
- **Imports:** `Equipment`, `Impact`, `ImpactNotification`, `UserResponse`, `CognitoService`, `DriverService` (UNUSED), `Configuration`, `DateUtil`, `SendEmail`, `SendMessage`, `Autowired`, `Qualifier`, `BeanPropertyRowMapper`, `JdbcDaoSupport`, `Repository`, `DataSource`, `java.sql.SQLException`

---

## Findings

### A03-1: Unused import `Roles` in EquipmentDAOImpl — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java`
**Line(s):** 5
**Description:** The import `com.journaldev.spring.jdbc.model.Roles` is never referenced in the class body. This is dead code that generates compiler warnings and clutters the import section. It should be removed.

### A03-2: Missing `@Override` annotation on `getEquipmentByUser` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java`
**Line(s):** 47
**Description:** The method `getEquipmentByUser(int uid)` implements `EquipmentDAO.getEquipmentByUser(int userId)` but lacks the `@Override` annotation, while the other two interface methods at lines 52-53 and 57-58 do have it. This is a style inconsistency and omits compile-time safety that `@Override` provides against accidental method signature changes.

### A03-3: Inconsistent indentation style (tabs vs. spaces) in EquipmentDAOImpl — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java`
**Line(s):** 57-60 vs. 47-50
**Description:** The `getEquipmentByMacAddress` method (lines 57-60) uses tab indentation while `getEquipmentByUser` (lines 47-50) and `getEquipmentIdByMacAddress` (lines 52-55) use space indentation. This inconsistency suggests the code was merged from different authors or editors without a consistent formatting standard.

### A03-4: Deprecated `new Object[]{}` usage for query parameters — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java`
**Line(s):** 54, 59
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java`
**Line(s):** 54, 65
**Description:** The `queryForObject(String sql, Object[] args, ...)` overload has been deprecated in Spring Framework 5.3+ in favor of varargs alternatives. Using `new Object[]{...}` is verbose and triggers deprecation warnings. The recommended approach is to use the varargs overload directly (e.g., `queryForObject(sql, Long.class, macAddress)`). This affects four call sites across these two files.

### A03-5: Unused import `DriverService` in ImpactDAO — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java`
**Line(s):** 8
**Description:** The import `com.journaldev.spring.jdbc.service.DriverService` is never referenced in the class. This is dead import code that should be removed.

### A03-6: `ImpactDAO.sendImpactNotification` violates single-responsibility — mixing DAO with notification logic — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java`
**Line(s):** 64-93
**Description:** The `sendImpactNotification` method performs email sending (`SendEmail.sendMail`) and SMS sending (`SendMessage.init`) directly from within a DAO class. A DAO's responsibility should be limited to data access. Sending notifications involves external I/O with side effects that are unrelated to data persistence. This is a leaky abstraction: notification logic is tightly coupled to the data layer, making it difficult to test, maintain, or change notification mechanisms independently. This method should be extracted to a service layer class.

### A03-7: `ImpactDAO` is a concrete class with no interface — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java`
**Line(s):** 24
**Description:** Unlike `EquipmentDAOImpl` which implements the `EquipmentDAO` interface, `ImpactDAO` is a concrete class with no corresponding interface. This is inconsistent with the project's established pattern and prevents easy mocking/substitution in unit tests. It also makes it harder to follow dependency inversion principles.

### A03-8: Magic number 80000 as impact threshold — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java`
**Line(s):** 39
**Description:** The value `80000` is used as a hard-coded threshold to determine whether an impact event should be saved. This magic number has no documentation or named constant explaining what it represents. It should be extracted to a named constant (e.g., `RED_IMPACT_THRESHOLD`) or made configurable, especially since the threshold value is a business rule that may need adjustment.

### A03-9: `queryForObject` can throw `EmptyResultDataAccessException` without handling — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java`
**Line(s):** 54, 59
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java`
**Line(s):** 54
**Description:** `JdbcTemplate.queryForObject()` throws `EmptyResultDataAccessException` when the query returns zero rows, and `IncorrectResultSizeDataAccessException` when it returns more than one row. In `getEquipmentIdByMacAddress` (line 54), `getEquipmentByMacAddress` (line 59), and `isImpactRecorded` (line 54), there is no handling for the case where a MAC address does not match any active equipment. If an invalid or unknown MAC address is passed, the application will throw an unhandled runtime exception. The callers would need to catch this or the DAO should use `query()` with result checking instead.

### A03-10: `SELECT *` in QUERY_EQUIPMENT_BY_MAC_ADDRESS — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java`
**Line(s):** 36
**Description:** The query `QUERY_EQUIPMENT_BY_MAC_ADDRESS` uses `select *` which couples the query to the table schema. If columns are added or removed from the `unit` table, this could silently break `BeanPropertyRowMapper` mappings or return unnecessary data. Explicit column listing is preferred for maintainability and performance clarity.

### A03-11: String concatenation used in logger calls inside lambda — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java`
**Line(s):** 75, 77
**Description:** The `logger.info(...)` calls use string concatenation (`"Start Sending Email to " + userResponse.getEmail()`). The `logger` inherited from `DaoSupport` is a Commons Logging `Log` instance which does not support SLF4J-style parameterized messages. While this works, string concatenation is performed regardless of whether the log level is enabled. If logging volume is high, using `logger.isInfoEnabled()` guard would prevent unnecessary string allocation.

### A03-12: Inconsistent stereotype annotations — `@Component` vs `@Repository` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java` (line 18), `ImpactDAO.java` (line 23)
**Line(s):** EquipmentDAOImpl:18, ImpactDAO:23
**Description:** `EquipmentDAOImpl` is annotated with `@Component("equipmentDAO")` while `ImpactDAO` is annotated with `@Repository`. Both are DAO classes. `@Repository` is the semantically correct annotation for DAOs as it also provides automatic exception translation from JDBC exceptions to Spring's `DataAccessException` hierarchy. The `@Component` annotation on `EquipmentDAOImpl` misses this exception translation benefit and is inconsistent with the pattern used by `ImpactDAO`.

### A03-13: `sendImpactNotification` uses `throws SQLException` but never throws it — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java`
**Line(s):** 64
**Description:** The method `sendImpactNotification` declares `throws SQLException` in its signature, but the method body does not contain any code that throws `SQLException`. The `JdbcTemplate.query()` call throws unchecked `DataAccessException`, not `SQLException`. The `throws` clause is misleading and forces callers to handle a checked exception that will never be thrown from this method.

### A03-14: `configuration` field in ImpactDAO is injected but never used — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java`
**Line(s):** 25-26
**Description:** The `Configuration` field is `@Autowired` but never referenced in any method of `ImpactDAO`. This is dead code / unused dependency injection that should be removed.

### A03-15: Potential `NullPointerException` in notification lambda — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java`
**Line(s):** 66-86
**Description:** In the `sendImpactNotification` lambda, `cognitoService.getUser(notification.getEmail())` could return null if the user is not found in Cognito, but the result `userResponse` is used without null checking on lines 67-86 (e.g., `userResponse.getName()`, `userResponse.getEmail()`). A null return would cause a `NullPointerException` inside the lambda, which would be wrapped in an opaque exception. Additionally, `notification.getSubscription_name()` could be null if the database column is nullable, which would cause NPE on line 67's `.equalsIgnoreCase()` call.

### A03-16: SLF4J Logger shadows inherited Commons Logging `logger` in EquipmentDAOImpl — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java`
**Line(s):** 20
**Description:** `EquipmentDAOImpl` declares its own `private static final Logger logger` (SLF4J) on line 20, which shadows the `protected final Log logger` inherited from `DaoSupport` (via `JdbcDaoSupport`). While this works and SLF4J is generally preferred over Commons Logging, it creates a field shadowing situation. In `ImpactDAO`, conversely, the inherited Commons Logging `logger` is used directly (lines 75, 77). This is an inconsistency in logging approach across the DAO layer.
# Pass 4 — Code Quality: A04

## Reading Evidence

### ManufacturerDAO.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/DAO/ManufacturerDAO.java`
- **Interface:** `ManufacturerDAO` (line 7)
- **Methods:**
  - `getManufacturersForUser(String username)` — line 8
- **Types/Constants:** None
- **Imports:** `com.journaldev.spring.jdbc.model.Manufacturer`, `java.util.List`

### ManufacturerDAOImpl.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/DAO/ManufacturerDAOImpl.java`
- **Class:** `ManufacturerDAOImpl extends JdbcDaoSupport implements ManufacturerDAO` (line 16)
- **Annotations:** `@Component("manufacturerDAO")` (line 15)
- **Methods:**
  - `setDbDataSource(DataSource dataSource)` — line 21 (`@Autowired @Qualifier("dataSource")`)
  - `getManufacturersForUser(String username)` — line 26 (`@Override`)
- **Types/Constants:**
  - `logger` — `private static final Logger` (line 17)
- **Imports:** `Manufacturer`, `Logger`, `LoggerFactory`, `Autowired`, `Qualifier`, `BeanPropertyRowMapper`, `JdbcDaoSupport`, `Component`, `DataSource`, `List`

### UserDAO.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java`
- **Class:** `UserDAO extends JdbcDaoSupport` (line 22)
- **Annotations:** `@Component`, `@Transactional` (lines 20-21)
- **Methods:**
  - `setDbDataSource(DataSource dataSource)` — line 27 (`@Autowired @Qualifier("dataSource")`)
  - `findByName(String name)` — line 33
  - `findByAuthority(String authority)` — line 61
- **Types/Constants:**
  - `logger` — `private static final Logger` (line 23)
  - `QUERY_USER_BY_NAME` — `private static final String` (line 31)
  - `QUERY_ROLE_BY_AUTHORITY` — `private static final String` (line 60)
- **Imports:** `Roles`, `User`, `Logger`, `LoggerFactory`, `Autowired`, `Qualifier`, `Value` (unused), `BeanPropertyRowMapper`, `JdbcDaoSupport`, `Component`, `Transactional`, `DataSource`, `Optional`

---

## Findings

### A04-1: Missing SQL whitespace causes syntax error in production query — CRITICAL
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/ManufacturerDAOImpl.java`
**Line(s):** 29-33
**Description:** The SQL query is constructed via string concatenation across multiple lines, but there are missing whitespace gaps between concatenated segments. Specifically:

- Line 31 ends with `?))"` and line 32 begins with `"or company_id in"` — the closing parenthesis `)` is immediately followed by `or` with no space, producing `...?))"or company_id in"` which concatenates to `...?))or company_id in`.
- Line 32 ends with `"(select id from company where email = ?)"` and line 33 begins with `"or company_id is null..."` — similarly, the `)` is followed directly by `or` with no space, producing `...?)or company_id`.

This results in the SQL fragment `...?))or company_id in(select id from company where email = ?)or company_id is null...`. While PostgreSQL may in some contexts tolerate `)or` as a token boundary (since `)` is a delimiter), this is at minimum a serious readability defect and may cause SQL parse failures depending on the database engine or version. The query should have explicit spaces: `") or company_id in "` and `") or company_id is null..."`.

### A04-2: UserDAO does not implement a DAO interface — inconsistent design pattern — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java`
**Line(s):** 22
**Description:** `ManufacturerDAOImpl` follows the pattern of implementing a separate interface (`ManufacturerDAO`), which is consistent with several other DAOs in the project (e.g., `EquipmentDAO`/`EquipmentDAOImpl`, `DriverDAO`/`DriverDAOImpl`, `APIDAO`/`APIDAOImpl`). However, `UserDAO` is a concrete class with no corresponding interface. This breaks the interface-segregation pattern used by the rest of the codebase, makes it harder to mock in unit tests, and creates a tight coupling to the concrete implementation for any consumers.

### A04-3: Unused import `@Value` in UserDAO — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java`
**Line(s):** 10
**Description:** The import `org.springframework.beans.factory.annotation.Value` is declared but never used anywhere in the class. This will generate a compiler warning (the project's `pom.xml` enables `-Xlint:all` and `showWarnings=true` at line 307-308), contributing to build noise.

### A04-4: `queryForObject` may throw EmptyResultDataAccessException — not handled — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java`
**Line(s):** 62
**Description:** The `findByAuthority` method uses `getJdbcTemplate().queryForObject(...)` which throws `EmptyResultDataAccessException` when no rows are returned. The code on line 64 checks `roles == null ? Optional.empty() : Optional.of(roles)` — but this null check is dead code because `queryForObject` never returns null; it throws an exception instead. If no role matches the given authority, the method will throw an uncaught `EmptyResultDataAccessException` rather than returning `Optional.empty()` as the signature implies. This is a semantic correctness bug: callers will get an unexpected exception rather than an empty Optional.

### A04-5: Inconsistent stereotype annotations across DAO classes — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/ManufacturerDAOImpl.java`, `src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java`
**Line(s):** ManufacturerDAOImpl:15, UserDAO:20
**Description:** `ManufacturerDAOImpl` uses `@Component("manufacturerDAO")` while `UserDAO` uses `@Component` (no qualifier). Meanwhile, other DAOs in the same package (e.g., `CompanyDAO`) use `@Repository`. The Spring `@Repository` annotation is the idiomatic stereotype for DAO classes and provides automatic exception translation from JDBC exceptions to Spring's `DataAccessException` hierarchy. Using `@Component` instead of `@Repository` means these classes do not benefit from that translation, and the inconsistency across the package makes the codebase harder to reason about.

### A04-6: Logging parameter `username` may contain PII — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/ManufacturerDAOImpl.java`
**Line(s):** 27
**Description:** The `getManufacturersForUser` method logs the `username` parameter at INFO level: `logger.info("getManufacturersForUser. username={}", username)`. The username value (which is an email address based on the SQL `where email = ?`) is personally identifiable information (PII). Logging PII at INFO level means it will appear in production log aggregation systems (Splunk is configured for this project) and may violate data privacy requirements. Consider logging at DEBUG level or masking the value.

### A04-7: `UserDAO` logger field is declared but never used — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java`
**Line(s):** 23
**Description:** The `logger` field is initialized at line 23 but is never referenced in any method of `UserDAO`. Neither `findByName` nor `findByAuthority` log anything. This is dead code that will generate a warning under `-Xlint:all`. It also represents a missed opportunity — the DAO performs database queries but has no logging for debugging or auditing.

### A04-8: SQL query references table `manufacture` (singular) — potential table name mismatch — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/ManufacturerDAOImpl.java`
**Line(s):** 29
**Description:** The SQL query selects from `manufacture` (singular), while the Java model class is named `Manufacturer` and the DAO is `ManufacturerDAO`. This asymmetry between the table name and the Java class names is unusual. If this is intentional (i.e., the database table is indeed named `manufacture`), this is purely informational. If the table was intended to be `manufacturer`, it would be a runtime SQL error. Flagged for verification.

### A04-9: Extra blank lines inside lambda in `findByName` — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java`
**Line(s):** 51-53
**Description:** There are three consecutive blank lines (lines 51-53) inside the `ResultSetExtractor` lambda in the `findByName` method, between the while-loop body and the `return user` statement. This is a minor formatting inconsistency that deviates from the rest of the codebase style.

### A04-10: `@Transactional` on DAO class with only read operations — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java`
**Line(s):** 21
**Description:** `UserDAO` is annotated with `@Transactional` at the class level, but both methods (`findByName` and `findByAuthority`) are read-only queries. Applying `@Transactional` to read-only operations without `readOnly = true` incurs unnecessary overhead: Spring will create a read-write transaction for every method call, acquiring and holding a database connection from the pool with a higher isolation level than needed. At minimum, this should be `@Transactional(readOnly = true)`. More broadly, since `UserDAO` contains no write operations, the class-level `@Transactional` may be a leftover from copy-paste. No other DAO in the scanned set uses `@Transactional`.

### A04-11: SQL query uses `md5()` for user lookup — security concern — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java`
**Line(s):** 31
**Description:** The `QUERY_USER_BY_NAME` query includes `md5(u.name) = ?` as an alternative lookup condition: `where u.active = true and (u.name = ? or md5(u.name) = ?)`. This means the system accepts an MD5 hash of the username as a valid lookup key. MD5 is cryptographically broken and trivially vulnerable to collision attacks. If any external consumer can pass an MD5 hash instead of a real username to authenticate or look up user data, this creates a weak authentication path. An attacker who cannot guess the username directly could potentially exploit MD5 collisions or precomputation tables. The purpose of this `md5()` fallback should be reviewed and, if not strictly necessary, removed.
# Pass 4 — Code Quality: A05

## Reading Evidence

### APKUpdaterController.java
- **Class/Interface:** `APKUpdaterController` (concrete, annotated `@Controller`, `@Slf4j`)
- **Methods:**
  - `getURLBase(HttpServletRequest, String)` — line 28 (private helper, returns String, throws MalformedURLException)
  - `getAvailablePackage(HttpServletRequest, String, String)` — line 38 (`@RequestMapping GET /rest/apk/{pkgname}/update`, `@ResponseBody`, returns `PackageEntry`)
  - `downloadPackage(String, String)` — line 56 (`@RequestMapping GET /rest/apk/{pkgname}`, returns `ResponseEntity<Resource>`)
- **Types/Constants referenced:** `PackageEntry`, `APKUpdaterService`, `Resource`, `HttpHeaders`, `HttpStatus`, `MediaType`, `MalformedURLException`, `URL`, `StringUtils`
- **Annotations:** `@Controller`, `@Slf4j`, `@Autowired`, `@RequestMapping`, `@ResponseBody`, `@PathVariable`, `@RequestParam`

### CompanyController.java
- **Class/Interface:** `CompanyController extends ConfigurationController` (concrete, annotated `@Controller`)
- **Methods:**
  - `getCompany(Long)` — line 37 (`@RequestMapping GET`, `@ResponseBody`, returns `List<Company>`)
  - `getCompanyDrivers(int)` — line 44 (`@RequestMapping GET`, `@ResponseBody`, returns `List<Driver>`)
  - `searchCompany(String)` — line 53 (`@RequestMapping GET`, `@ResponseBody`, returns `List<Company>`)
  - `addCompany(Permissions)` — line 62 (`@RequestMapping POST`, `@ResponseBody`, returns `ResponseEntity<Permissions>`)
  - `companyAcceptWeb(String)` — line 121 (`@RequestMapping GET`, `@ResponseBody`, returns `ResponseEntity<Results>`)
  - `companyAccept(int)` — line 148 (`@RequestMapping PUT`, `@ResponseBody`, returns `ResponseEntity<Results>`)
  - `companyDelete(int)` — line 163 (`@RequestMapping PUT`, `@ResponseBody`, returns `ResponseEntity<Results>`)
- **Types/Constants referenced:** `CompanyDAO`, `DriverDAO`, `Company`, `Driver`, `Permissions`, `Results`, `RuntimeConfig`, `RestURIConstants`, `SendEmail`, `JdbcTemplate`, `BeanPropertyRowMapper`, `HttpStatus`, `ResponseEntity`, `Logger`, `LoggerFactory`
- **Fields:** `logger` (line 27), `driverDAO` (line 30), `companyDAO` (line 33)

### ConfigurationController.java
- **Class/Interface:** `ConfigurationController` (abstract, annotated `@Controller`)
- **Methods:** None (no methods defined)
- **Fields:**
  - `configuration` — line 20 (`@Autowired`, protected, type `Configuration`)
  - `dataSource` — line 23 (`@Autowired`, `@Qualifier("dataSource")`, protected, type `DataSource`)
- **Types/Constants referenced:** `Configuration`, `DataSource`

---

## Findings

### A05-1: Hardcoded API Keys and Credentials in RuntimeConfig — CRITICAL
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java` (referenced by `CompanyController.java`)
**Line(s):** 14, 19, 20
**Description:** `RuntimeConfig` contains hardcoded secrets in plain-text static fields: a GCM API key (`GCMKEY = "key=AIzaSyDDuQUYLcXkutyIxRToLAeBPHBQNLfayzs"`), Clickatell SMS credentials (`USERNAME`, `PASSWORD`), and an SMS API ID. These are committed to source control in a public-facing Java file. This is a critical security deficiency. All secrets should be externalized to environment variables, a secrets manager, or at minimum Spring property files excluded from version control.

### A05-2: Raw SQL Queries Inline in Controller (Leaky Abstraction / Architectural Violation) — CRITICAL
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java`
**Line(s):** 64-117 (addCompany), 124-142 (companyAcceptWeb), 151-158 (companyAccept), 166-173 (companyDelete)
**Description:** The controller directly instantiates `JdbcTemplate` and executes raw SQL queries (SELECT, INSERT, UPDATE, DELETE) within HTTP handler methods. This completely bypasses the DAO layer, violates separation of concerns, and makes the code untestable in isolation. The controller already has `companyDAO` and `driverDAO` injected but only uses them in simpler GET methods. All data-access logic should be moved to the DAO/repository layer.

### A05-3: SQL Injection Risk via MD5 Token Scheme — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java`
**Line(s):** 97-98, 127-128, 131-132
**Description:** The permission acceptance mechanism relies on an MD5 hash of a timestamp concatenated with an ID (`md5(to_char(createdat, 'DDMMYYYYHH12MI:SS')||id)`), computed in SQL. While parameterized queries are used (mitigating direct SQL injection), the MD5-based token scheme is cryptographically weak. MD5 is broken for security purposes, and the token's entropy is very low (it is derived from predictable data: a sequential ID and a timestamp). An attacker who knows or can guess the permission ID and creation time can forge the acceptance token. A cryptographically secure random token (e.g., `UUID` or `SecureRandom`) should be stored and compared instead.

### A05-4: Misuse of HTTP Status Code BAD_GATEWAY (502) for Business Logic Errors — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java`
**Line(s):** 112, 116, 141
**Description:** The `addCompany` and `companyAcceptWeb` methods return `HttpStatus.BAD_GATEWAY` (502) for business-logic conditions such as "permission already exists" or "self-association attempted" or "token not found/already used." HTTP 502 means "the server, acting as a gateway, received an invalid response from an upstream server," which is semantically incorrect. Appropriate status codes would be `409 CONFLICT` for duplicates, `400 BAD_REQUEST` for invalid input, or `404 NOT_FOUND` for missing tokens.

### A05-5: DELETE Operation Mapped to HTTP PUT — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java`
**Line(s):** 162
**Description:** The `companyDelete` method executes `DELETE FROM permission WHERE id = ?` but is mapped to `RequestMethod.PUT`. This violates RESTful conventions where destructive deletion should use `RequestMethod.DELETE`. Using PUT for a delete operation is misleading and will confuse API consumers and tooling (e.g., API documentation generators, security scanners).

### A05-6: No Authorization Check on companyAccept and companyDelete — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java`
**Line(s):** 148-158, 162-174
**Description:** The `companyAccept` and `companyDelete` endpoints take a permission ID directly as a path variable and execute UPDATE/DELETE without any authentication or authorization check. Any caller who can guess or enumerate permission IDs can accept or delete permissions for any company. There is no validation that the caller owns or is authorized to modify the referenced permission.

### A05-7: Null Return from getAvailablePackage with No Error Signaling — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java`
**Line(s):** 44, 49
**Description:** `getAvailablePackage` returns `null` both when the service returns an empty Optional (line 44, `.orElse(null)`) and when a `MalformedURLException` occurs (line 49). Returning `null` from a `@ResponseBody` method typically results in an HTTP 200 with an empty body, providing no indication to the client that an error occurred or that the package was not found. A `ResponseEntity` with appropriate status codes (404 for not found, 500 for internal error) should be used instead.

### A05-8: TODO Comment Left in Production Code — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java`
**Line(s):** 48
**Description:** A `// TODO Handle error` comment exists in the catch block for `MalformedURLException`. This indicates known incomplete error handling that was never addressed. The method silently swallows the exception (after logging) and returns null. This TODO should be resolved with proper error-response handling.

### A05-9: No Null/Error Handling in downloadPackage — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java`
**Line(s):** 61-67
**Description:** The `downloadPackage` method calls `apkUpdaterService.loadPackageAsResource(pkgname, version)` and immediately calls `resource.getFilename()` on the result (line 65) without null-checking. If the service returns null or the resource does not exist, this will throw a `NullPointerException` resulting in an unhandled 500 error. There is no try-catch or validation of the resource.

### A05-10: Inconsistent Logging Approach Across Controllers — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java`, `src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java`
**Line(s):** APKUpdaterController:5,21 vs CompanyController:8-9,27
**Description:** `APKUpdaterController` uses Lombok's `@Slf4j` annotation (which generates a `log` field), while `CompanyController` manually declares `private static final Logger logger = LoggerFactory.getLogger(...)`. This results in inconsistent logging variable names (`log` vs `logger`) and different approaches to the same concern across controllers in the same package. The codebase should standardize on one approach.

### A05-11: String Concatenation in Log Statement — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java`
**Line(s):** 46, 103, 105
**Description:** Line 46 uses parameterized logging (`logger.info("Start Sending Email to " + email)` on lines 103 and 105) which performs string concatenation regardless of whether the log level is enabled. This is inconsistent with the parameterized style used on line 38 (`logger.info("Start getCompany for {}", uid)`). All log statements should use parameterized placeholders (`{}`) to avoid unnecessary string concatenation overhead.

### A05-12: Abstract Class Annotated with @Controller — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ConfigurationController.java`
**Line(s):** 16-17
**Description:** `ConfigurationController` is declared `abstract` but is annotated with `@Controller`. While Spring will not instantiate an abstract class, the `@Controller` annotation is misleading and unnecessary on an abstract base class. It serves only as a common field holder for `configuration` and `dataSource`. This would be better modeled without the `@Controller` annotation, or the shared dependencies could be provided through a different mechanism (e.g., a configuration bean or constructor injection in subclasses).

### A05-13: Protected Field Injection Instead of Constructor Injection — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ConfigurationController.java`
**Line(s):** 19-24
**Description:** Both `configuration` and `dataSource` use field injection (`@Autowired` on protected fields) and are exposed to subclasses via `protected` access. This pattern makes dependencies invisible in constructors, prevents immutability (fields are not `final`), and complicates unit testing (requires reflection or Spring context to inject mocks). Constructor injection is the recommended approach by the Spring team.

### A05-14: Misleading Javadoc Comment — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java`
**Line(s):** 20-22
**Description:** The Javadoc states "Handles requests for the Employee JDBC Service," but this class handles Company-related operations, not Employee operations. This appears to be a copy-paste artifact from a template or another controller.

### A05-15: JdbcTemplate Instantiated Per Request Instead of Being Injected — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java`
**Line(s):** 64, 124, 151, 166
**Description:** Multiple methods create `new JdbcTemplate(dataSource)` as a local variable on every request. While functionally harmless (JdbcTemplate is thread-safe and lightweight), it is wasteful and unconventional. A `JdbcTemplate` should be created once (e.g., as a bean or initialized in a `@PostConstruct` method) and reused.

### A05-16: Inconsistent Parameter Types for Same Semantic Concept — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java`
**Line(s):** 37 vs 44
**Description:** `getCompany` accepts `@PathVariable("uid") Long uid` (boxed Long), while `getCompanyDrivers` accepts `@PathVariable("uid") int uid` (primitive int) for what appears to be the same kind of identifier. This inconsistency can cause confusion and unexpected behavior (e.g., null handling differences between `Long` and `int`).

### A05-17: Wildcard Import of Model Package — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java`
**Line(s):** 6
**Description:** `import com.journaldev.spring.jdbc.model.*` uses a wildcard import. While not an error, wildcard imports can obscure which classes are actually used, may pull in unintended types, and make it harder to track dependencies during code review. Explicit imports are preferred for clarity.

### A05-18: Inconsistent Indentation Style — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java`
**Line(s):** Throughout (e.g., lines 54, 64-117)
**Description:** The file uses inconsistent indentation, mixing tabs and varying levels of indentation. For example, `searchCompany` body has extra leading whitespace compared to `getCompany`. The deeply nested `addCompany` method has multiple indentation levels that are inconsistent. This hampers readability and suggests no code formatter is enforced.

### A05-19: APKUpdaterController Does Not Extend ConfigurationController — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java`
**Line(s):** 22
**Description:** Unlike most other controllers in this package (CompanyController, DriverController, LocationController, etc.), `APKUpdaterController` does not extend `ConfigurationController`. This is not necessarily a problem (it may not need `dataSource` or `configuration`), but it represents an architectural inconsistency worth noting. The controller uses its own service layer (`APKUpdaterService`) which is a better pattern than direct JDBC access.
# Pass 4 — Code Quality: A06

## Reading Evidence

### DatabaseCleanupException.java
- **Class/Interface:** `DatabaseCleanupException extends RuntimeException` (line 7)
- **Annotations:** `@ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)` (line 6)
- **Methods:**
  - `DatabaseCleanupException(String message)` — constructor, line 8
- **Types/Constants:** None
- **Imports:** `HttpStatus`, `ResponseStatus`

### DatabaseController.java
- **Class/Interface:** `DatabaseController extends ConfigurationController` (line 16)
- **Annotations:** `@Slf4j` (line 14), `@Controller` (line 15)
- **Methods:**
  - `cleanup()` — line 64 (public, `@RequestMapping POST /rest/db/cleanup`)
  - `deleteCompanies(JdbcTemplate, int, List<Long>, List<Long>)` — line 84 (private, recursive)
- **Types/Constants:**
  - `QUERY_COMPANIES_TO_DELETE` — `private static final String`, lines 18-60
- **Imports:** `Slf4j`, `HttpStatus`, `JdbcTemplate`, `Controller`, `RequestMapping`, `RequestMethod`, `ResponseStatus`, `ArrayList`, `List`

### DriverController.java
- **Class/Interface:** `DriverController extends ConfigurationController` (line 42)
- **Annotations:** `@Controller` (line 40), `@Slf4j` (line 41)
- **Fields:**
  - `fileStorageService` — `FileStorageService`, `@Autowired @Qualifier("localFileStorage")`, line 46
  - `driverService` — `DriverService`, `@Autowired`, line 49
  - `driverDAO` — `DriverDAO`, `@Autowired`, line 52
  - `gson` — `Gson`, package-private (no access modifier), line 54
- **Methods:**
  - `getLoginAuth(Driver)` — line 59 (`@Deprecated`, POST, returns `ResponseEntity<List<Driver>>`)
  - `registerDrivers(Driver)` — line 77 (POST, returns `ResponseEntity<Driver>`)
  - `resetPassword(Driver)` — line 91 (POST, returns `ResponseEntity<Results>`)
  - `acceptDrivers(int[])` — line 108 (PUT, returns `int`)
  - `declineDriver(int[])` — line 120 (DELETE, returns `int`)
  - `uploadProfile(int, MultipartFile, String)` — line 132 (POST multipart, returns `ResponseEntity<Results>`)
  - `uploadProfileAPP(int, MultipartFile)` — line 163 (POST multipart, returns `ResponseEntity<Results>`)
  - `saveEmails(DriverEmails)` — line 187 (POST, returns `ResponseEntity<Results>`)
  - `getEmails(int)` — line 209 (GET, returns `ResponseEntity<DriverEmails>`)
  - `getDriver(int)` — line 228 (GET, returns `List<Driver>`)
  - `saveLicence(Driver)` — line 235 (POST, returns `ResponseEntity<Driver>`)
  - `updateDrivers(Driver)` — line 253 (POST, returns `ResponseEntity<Results>`)
- **Types/Constants:** References `RestURIConstants.*`, `RuntimeConfig.*`

---

## Findings

### A06-01: Recursive method passes cleared list as both `errors` and `companies` — CRITICAL
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/DatabaseController.java`
**Line(s):** 94-97
**Description:** In `deleteCompanies()`, when a retry pass is triggered, `errors.clear()` is called on line 96, and then `errors` is passed as both the `errors` parameter and the `companies` parameter on line 97: `deleteCompanies(jdbcTemplate, ++pass, errors, errors)`. Since `errors` was just cleared, the `companies` list in the recursive call is now empty, meaning the retry pass will iterate over zero elements and never actually re-attempt deletion. This completely defeats the purpose of the multi-pass retry logic.

### A06-02: NullPointerException if company query fails — CRITICAL
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/DatabaseController.java`
**Line(s):** 66-77
**Description:** On line 66, `companies` is initialized to `null`. If the query on line 69 throws an exception, the catch block on lines 71-73 only logs an error but does not return or rethrow. Execution continues to line 77 where `deleteCompanies()` is called with `companies` still `null`. Inside `deleteCompanies()` on line 86, `companies.forEach(...)` will throw a `NullPointerException`.

### A06-03: Hardcoded email addresses and MAC addresses in source code — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/DatabaseController.java`
**Line(s):** 18-60
**Description:** The `QUERY_COMPANIES_TO_DELETE` constant embeds 14 email addresses and 22 MAC addresses directly in the source code. This is a maintenance burden (any change requires a code deployment), leaks PII/internal data into the codebase, and represents a brittle cleanup mechanism. These values should be externalized to configuration, a database table, or at minimum a properties file.

### A06-04: Missing `serialVersionUID` on serializable exception — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/DatabaseCleanupException.java`
**Line(s):** 7
**Description:** `DatabaseCleanupException` extends `RuntimeException` (which implements `Serializable`) but does not declare a `serialVersionUID` field. This will generate a compiler warning and could cause deserialization issues if the class structure changes between JVM versions.

### A06-05: Misuse of `HttpStatus.BAD_GATEWAY` for client/application errors — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java`
**Line(s):** 71, 83, 99, 157, 181
**Description:** Multiple endpoints return `HttpStatus.BAD_GATEWAY` (502) for authentication failures (line 71), registration errors (line 83), password reset failures (line 99), and file upload IO errors (lines 157, 181). HTTP 502 means the server, acting as a gateway, received an invalid response from an upstream server. These are application-level errors that should use `400 BAD_REQUEST`, `401 UNAUTHORIZED`, `409 CONFLICT`, or `500 INTERNAL_SERVER_ERROR` as appropriate. Returning 502 misleads clients and monitoring systems.

### A06-06: Sensitive data logged via `Gson` serialization of request bodies — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java`
**Line(s):** 60, 78, 92, 188, 236, 254
**Description:** Multiple methods log the full JSON serialization of `Driver` objects using `gson.toJson(driverExample)`. The `Driver` object likely contains passwords (line 60 logs the authentication request including password), emails, personal addresses, and security numbers. This logs sensitive PII/credentials to application logs, violating security best practices.

### A06-07: `e.printStackTrace()` instead of proper logging — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java`
**Line(s):** 154
**Description:** In `uploadProfile()`, the `IOException` catch block uses `e.printStackTrace()` which writes to `System.err` rather than using the SLF4J logger (`log`) that is available via the `@Slf4j` annotation. This bypasses structured logging, making it harder to correlate errors in log aggregation systems.

### A06-08: Deprecated `org.springframework.security.crypto.codec.Base64` usage — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java`
**Line(s):** 18, 142
**Description:** The import `org.springframework.security.crypto.codec.Base64` on line 18 references a class that has been deprecated in Spring Security since version 4.x in favor of `java.util.Base64` (available since Java 8). This will generate deprecation warnings at compile time and the class may be removed in future Spring Security versions.

### A06-09: `Gson` field has package-private visibility, not `private` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java`
**Line(s):** 54
**Description:** The `gson` field is declared without an access modifier (`Gson gson = new Gson();`), giving it package-private visibility. This breaks encapsulation. It should be `private` (and ideally `private static final` since `Gson` instances are thread-safe and reusable).

### A06-10: Repeated `new JdbcTemplate(dataSource)` instantiation in every method — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java`
**Line(s):** 111, 123, 135, 165, 190, 212, 237, 256
**Description:** Eight methods in `DriverController` (and one in `DatabaseController` line 65) create a new `JdbcTemplate` instance on every request via `new JdbcTemplate(dataSource)`. While `JdbcTemplate` is thread-safe and designed to be a shared singleton, creating it per-request is wasteful and inconsistent with Spring idioms. It should be a `@Bean` or an `@Autowired` field, or initialized once in a `@PostConstruct` method.

### A06-11: Inline SQL throughout controller layer — leaky abstraction — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java`
**Line(s):** 113, 125, 146, 171, 193, 196, 199, 213, 241, 245, 260
**Description:** The controller layer directly constructs and executes raw SQL queries in at least 11 locations. This violates separation of concerns — SQL and data access logic should reside in DAO/Repository classes, not in controllers. The controller already has `DriverDAO` and `DriverService` injected but uses them inconsistently, falling back to raw JDBC for many operations.

### A06-12: Resource leak — `InputStream` not closed in all paths — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java`
**Line(s):** 139-148, 168-173
**Description:** In `uploadProfile()`, the `BufferedInputStream` created on line 139 may be replaced by a `ByteArrayInputStream` on line 142, but the original `BufferedInputStream` is never closed in that branch. Additionally, `fis.close()` on line 148 is outside the try-with-resources pattern; if `fileStorageService.saveImage()` or `jdbcTemplate.update()` throws, the stream will not be closed. The same pattern occurs in `uploadProfileAPP()` lines 168-173. Both should use try-with-resources.

### A06-13: Deprecated method `getLoginAuth` still active and exposed — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java`
**Line(s):** 58-73
**Description:** The `getLoginAuth()` method is annotated `@Deprecated` but is still mapped to an active REST endpoint (`/rest/appuser/validate`). There is no documentation indicating when it will be removed or what replaces it. The `RestURIConstants` file has a comment `//unused` near `ACCEPT_USRS`/`DECLINE_USRS` (lines 4-6) but not near `VALIDATE_USR`, creating confusion about which endpoints are actually deprecated.

### A06-14: Log message says "saveEmails" in `getEmails` method — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java`
**Line(s):** 210
**Description:** The `getEmails()` method logs `"Start saveEmails."` which is a copy-paste error. It should log `"Start getEmails."`.

### A06-15: Typo in log message "delineUsers" should be "declineUsers" — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java`
**Line(s):** 121
**Description:** The log message reads `"Start delineUsers."` which should be `"Start declineUsers."` or `"Start declineDriver."` to match the method name.

### A06-16: Deprecated `new Object[]{}` usage with `JdbcTemplate.query()` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java`
**Line(s):** 215
**Description:** The call `jdbcTemplate.query(query, new Object[]{uid}, ...)` uses the deprecated `query(String, Object[], RowMapper)` overload. Modern Spring versions prefer the varargs form: `jdbcTemplate.query(query, new BeanPropertyRowMapper<>(...), uid)`. This generates deprecation warnings.

### A06-17: SQL injection risk in `deleteCompanies` via string concatenation — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/DatabaseController.java`
**Line(s):** 88
**Description:** The SQL statement `"select delete_company("+ c +")"` concatenates the company ID directly into the SQL string. Although `c` is a `Long` (not user-supplied string input), this is a bad practice that bypasses parameterized queries. If the data type or source of `c` were ever to change, this would become a direct SQL injection vector. Parameterized queries should be used consistently.
# Pass 4 — Code Quality: A07

## Reading Evidence

### EquipmentController.java
- **Class/Interface:** `EquipmentController extends ConfigurationController` (line 23), annotated `@Controller`
- **Methods:**
  - `getEquipmentByUser(@PathVariable int uid)` — line 36, GET
  - `addEquipment(@RequestBody Equipment equipment)` — line 44, POST
  - `getManufactureList(Authentication authentication)` — line 78, GET
  - `getTypeList(@PathVariable int mid)` — line 86, GET
  - `getFuelTypeList(@PathVariable int manuId, @PathVariable int typeID)` — line 105, GET
  - `getService(@PathVariable int uid)` — line 123, GET
  - `SaveService(@RequestBody Services services)` — line 142, POST
- **Types/Constants referenced:** `DriverEquipment`, `Equipment`, `Manufacturer`, `Types`, `FuelType`, `Services`, `Results`, `RuntimeConfig.MSGID_SUCCESS`, `RuntimeConfig.MSGID_LOGICERRORR`, `RuntimeConfig.ERRORMSG_LOGICERRORR`, `RestURIConstants.*`
- **Fields:** `EquipmentDAO equipmentDAO` (line 27), `ManufacturerDAO manufacturerDAO` (line 30), `Gson gson` (line 32)
- **Imports:** `Gson`, `EquipmentDAO`, `ManufacturerDAO`, `model.*`, `Logger/LoggerFactory`, Spring annotations, `JdbcTemplate`, `BeanPropertyRowMapper`, `Authentication`, `UserDetails`, `@Transactional` (unused)

### ImageController.java
- **Class/Interface:** `ImageController` (line 23), annotated `@Controller @Slf4j` — does NOT extend `ConfigurationController`
- **Methods:**
  - `downloadFile(@PathVariable String fileName)` — line 30, GET
- **Types/Constants referenced:** `FileStorageService`, `Resource`, `HttpHeaders`, `MediaType`, `URLConnection`
- **Fields:** `FileStorageService fileStorageService` (line 27), qualified `"localFileStorage"`

### ImpactController.java
- **Class/Interface:** `ImpactController extends ConfigurationController` (line 43), annotated `@Controller`
- **Javadoc:** "Handles requests for the Employee JDBC Service." (line 41) — stale/incorrect Javadoc
- **Methods:**
  - `saveIncident(@RequestBody Incidents incident)` — line 59, POST
  - `saveImpactIMAGE(@PathVariable int impId, @RequestParam MultipartFile imageFile, @RequestParam String signatureFile)` — line 83, POST multipart
  - `saveImpactIMAGEAPP(@PathVariable int impId, @PathVariable String type, @RequestParam MultipartFile imageFile)` — line 117, POST multipart
  - `saveImpactData(@RequestBody ImpactList impactList)` — line 152, POST
- **Types/Constants referenced:** `Incidents`, `ImpactList`, `Results`, `Equipment`, `RuntimeConfig.MSGID_SUCCESS`, `RuntimeConfig.MSGID_CODEERRORR`, `RuntimeConfig.ERRORMSG_CODEERRORR`, `RuntimeConfig.MSGID_CODEE_DUPLICATE_VEHICLE`, `RestURIConstants.*`
- **Fields:** `FileStorageService awsFileStorageService` (line 48, qualified `"awsFileStorage"`), `ImpactDAO impactDAO` (line 51), `EquipmentDAO equipmentDAO` (line 54), `Gson gson` (line 56)
- **Logger misconfiguration:** Logger initialized with `ConfigurationController.class` instead of `ImpactController.class` (line 44)

---

## Findings

### A07-1: Logger initialized with wrong class — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java`
**Line(s):** 44
**Description:** The logger is created with `LoggerFactory.getLogger(ConfigurationController.class)` instead of `LoggerFactory.getLogger(ImpactController.class)`. All log statements in this controller will be attributed to `ConfigurationController` in log output, making debugging and log filtering incorrect and misleading. This is a copy-paste error that directly impacts operational observability.

### A07-2: Unused import — `@Transactional` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java`
**Line(s):** 17
**Description:** `org.springframework.transaction.annotation.Transactional` is imported but never used anywhere in the class. No method or class-level `@Transactional` annotation exists. This is dead code in the import section and will produce a compiler/IDE warning.

### A07-3: Direct `JdbcTemplate` instantiation in controller methods bypasses Spring management — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java`
**Line(s):** 46, 89, 108, 126, 144
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java`
**Line(s):** 61, 88, 122
**Description:** Multiple methods create `new JdbcTemplate(dataSource)` locally instead of using a Spring-managed `@Autowired JdbcTemplate` bean or delegating to a DAO. This pattern: (a) creates a new `JdbcTemplate` instance on every request, which is wasteful; (b) bypasses any Spring transaction management since the template is not Spring-managed; (c) violates the layered architecture — controllers should not contain raw SQL. The DAO pattern is already used for some operations (e.g., `equipmentDAO`, `impactDAO`) but is inconsistently applied; many methods still embed raw SQL directly in the controller.

### A07-4: Raw SQL queries embedded in controller layer — leaky abstraction — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java`
**Line(s):** 50, 59, 64, 93, 96-97, 112, 115, 127-135, 146, 152, 155, 160, 163, 168, 172
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java`
**Line(s):** 63, 67-68, 98-99, 129, 133
**Description:** Controllers contain extensive raw SQL (SELECT, INSERT, UPDATE) with string concatenation. This is a leaky abstraction that couples the controller layer directly to the database schema. Database logic should be encapsulated in DAO/repository classes. Some DAOs already exist (`EquipmentDAO`, `ImpactDAO`, `ManufacturerDAO`) but are not used consistently. This makes the codebase harder to test, maintain, and refactor.

### A07-5: `Gson` field is package-private and non-final — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java`
**Line(s):** 32
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java`
**Line(s):** 56
**Description:** `Gson gson = new Gson()` is declared with default (package-private) access and is not `final`. Since `Gson` instances are thread-safe and immutable, this should be declared `private static final` to clearly communicate its intent, prevent accidental reassignment, and avoid unnecessary per-instance allocation.

### A07-6: Deprecated `org.springframework.security.crypto.codec.Base64` usage — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java`
**Line(s):** 18, 92
**Description:** `org.springframework.security.crypto.codec.Base64` has been deprecated since Spring Security 4.x. The recommended replacement is `java.util.Base64` (available since Java 8). Using deprecated APIs risks removal in future Spring Security upgrades and generates compiler deprecation warnings.

### A07-7: InputStream resources not closed in `finally` / not using try-with-resources — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java`
**Line(s):** 89-102 (saveImpactIMAGE), 123-137 (saveImpactIMAGEAPP)
**Description:** In `saveImpactIMAGE`, `imagfis` and `sigfis` are opened but only closed in the happy path (lines 101-102). If `awsFileStorageService.saveImage()` or the DB update throws an exception, the streams leak. Similarly in `saveImpactIMAGEAPP` (line 137). These should use try-with-resources blocks to ensure proper cleanup.

### A07-8: `e.printStackTrace()` used instead of logger — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java`
**Line(s):** 108, 142
**Description:** Exception handling in `saveImpactIMAGE` and `saveImpactIMAGEAPP` uses `e.printStackTrace()` which writes to `System.err` instead of the configured logging framework. This bypasses log aggregation, formatting, and rotation. Should use `logger.error("message", e)` instead.

### A07-9: Stale/incorrect Javadoc — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java`
**Line(s):** 39-41
**Description:** The class-level Javadoc reads "Handles requests for the Employee JDBC Service." This is clearly a leftover from a template or copy-paste and does not describe the actual purpose of the `ImpactController`, which handles impact event and incident data.

### A07-10: Commented-out code block — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java`
**Line(s):** 73-80
**Description:** A block of commented-out HTTP request documentation (multipart form-data boundary example) is left in the source. While it may have served as developer notes, commented-out code/specs should be removed or moved to proper API documentation to keep the source clean.

### A07-11: Method naming convention violation — `SaveService` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java`
**Line(s):** 142
**Description:** The method `SaveService` starts with an uppercase letter, violating Java method naming conventions (camelCase). All other methods in the same file correctly use lowercase-first naming (e.g., `getService`, `addEquipment`). Should be `saveService`.

### A07-12: Raw type usage — `ResponseEntity` without type parameter — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java`
**Line(s):** 180, 185, 191
**Description:** In `saveImpactData`, `new ResponseEntity(results, ...)` is used without the generic type parameter (raw type). This produces unchecked type warnings at compile time. Should be `new ResponseEntity<>(results, ...)` or `new ResponseEntity<Results>(results, ...)` to match the method return type `ResponseEntity<Results>`.

### A07-13: `HttpStatus.BAD_REQUEST` returned for empty result set — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java`
**Line(s):** 39
**Description:** `getEquipmentByUser` returns `HttpStatus.BAD_REQUEST` when the equipment list is empty. An empty result set is not a client error — it is a valid response. Returning 400 is semantically incorrect; `HttpStatus.OK` with an empty list or `HttpStatus.NOT_FOUND` (204/404) would be more appropriate.

### A07-14: Potential `NullPointerException` on `contentType` in ImageController — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ImageController.java`
**Line(s):** 35-44
**Description:** `URLConnection.guessContentTypeFromStream()` can return `null` if it cannot determine the type. While the `catch` block sets a fallback to `"application/octet-stream"`, the normal (non-exception) path does not handle a null return from `guessContentTypeFromStream`. If the method returns `null` without throwing, `contentType` remains `null` and `MediaType.parseMediaType(null)` will throw `InvalidMediaTypeException`. The fallback assignment should also cover the `null` return case outside the catch block.

### A07-15: Inconsistent logging style across controllers — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java` (SLF4J Logger + string concatenation)
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ImageController.java` (Lombok `@Slf4j`)
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java` (SLF4J Logger + string concatenation, but some uses of parameterized `{}` style on line 158)
**Line(s):** Various
**Description:** Three different logging approaches are used across the three controllers: manual `LoggerFactory.getLogger()` with string concatenation in EquipmentController/ImpactController, Lombok `@Slf4j` in ImageController, and parameterized `{}` placeholder style (line 158 of ImpactController) mixed with string concatenation (line 60, 84, etc.). The codebase should standardize on one approach, preferably Lombok `@Slf4j` with `{}` parameterized messages to avoid unnecessary string concatenation overhead.

### A07-16: Misleading log message in `SaveService` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java`
**Line(s):** 143
**Description:** The log message reads `"Start addEquipment."` but the method is `SaveService`. This is a copy-paste error from the `addEquipment` method. It will mislead anyone reviewing logs to diagnose service-related issues.

### A07-17: Misleading log message in `getTypeList` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java`
**Line(s):** 87
**Description:** The log message reads `"Start getFuelTypeList."` but the method is `getTypeList`. This is a copy-paste error from the `getFuelTypeList` method below it. The actual `getFuelTypeList` method at line 106 also logs `"Start getFuelTypeList."`, making log output ambiguous for the two different endpoints.

### A07-18: `HttpStatus.BAD_GATEWAY` used for business logic error — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java`
**Line(s):** 71
**Description:** When a duplicate equipment record is detected, the response returns `HttpStatus.BAD_GATEWAY` (502). HTTP 502 means the server, acting as a gateway, received an invalid response from an upstream server. For a duplicate/conflict business error, `HttpStatus.CONFLICT` (409) or `HttpStatus.UNPROCESSABLE_ENTITY` (422) would be semantically correct.

### A07-19: Wildcard import of model package — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java`
**Line(s):** 6
**Description:** `import com.journaldev.spring.jdbc.model.*` uses a wildcard import. While functional, this reduces code clarity by hiding which specific model classes are used. Explicit imports (as done in ImpactController) are preferred for maintainability and to avoid potential class name collisions.

### A07-20: No input validation on path variables and request bodies — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java`
**Line(s):** 36, 44, 86, 105, 123, 142
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java`
**Line(s):** 59, 83, 117, 152
**Description:** None of the `@RequestBody` parameters use Bean Validation (`@Valid`/`@Validated`) and none of the `@PathVariable` parameters are validated for range/sanity. For example, `addEquipment` directly uses user-supplied data in SQL queries, `saveIncident` inserts all fields without validation. While parameterized queries prevent SQL injection, lack of validation allows malformed or empty data to reach the database, potentially violating constraints or causing unexpected behavior.
# Pass 4 — Code Quality: A08

## Reading Evidence

### LocationController.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java`
- **Class:** `LocationController extends ConfigurationController` (lines 27-93)
- **Annotations:** `@Controller` (line 27)
- **Fields:**
  - `logger` — `private static final Logger` (line 30)
  - `gson` — `Gson` (package-private, line 32)
- **Methods:**
  - `getGPSLocation(@PathVariable int uid)` — line 35, returns `List<GPS>`, GET mapped to `RestURIConstants.GET_GPS_LOC`
  - `saveGPSLocation(@RequestBody GPS gps)` — line 53, returns `ResponseEntity<Results>`, POST mapped to `RestURIConstants.SAVE_GPS_LOC`
  - `saveGPSLocations(@RequestBody GPSList gpsList)` — line 72, returns `ResponseEntity<Results>`, POST mapped to `RestURIConstants.SAVE_GPS_LOCS`
- **Types/Dependencies:** `GPS`, `GPSList`, `Results`, `DateUtil`, `Gson`, `JdbcTemplate`, `BeanPropertyRowMapper`, `RuntimeConfig.MSGID_SUCCESS`
- **Javadoc comment on line 25-26:** `/** Not in Use */`

### ReportAPI.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java`
- **Class:** `ReportAPI` (lines 6-105, plain class, not a controller/component)
- **Imports:**
  - `com.journaldev.spring.jdbc.util.HttpDownloadUtility` (line 3)
  - `com.journaldev.spring.jdbc.util.Util` (line 4)
- **Fields (all `protected`):**
  - `subject` — `String` (line 7)
  - `title` — `String` (line 8)
  - `content` — `String` (line 10)
  - `sEmail` — `String` (line 11)
  - `rEmail` — `String` (line 12)
  - `fileURL` — `String` (line 13)
  - `name` — `String` (line 14)
  - `input` — `String` (line 15)
- **Constructor:** `ReportAPI(String name, String input)` — line 17
- **Methods:**
  - `downloadPDF()` — line 25, returns `String`, throws `Exception`
  - `getExportDir(String dirctory)` — line 34, returns `String`, throws `Exception`
  - `getSubject()` — line 47
  - `setSubject(String)` — line 51
  - `getTitle()` — line 55
  - `setTitle(String)` — line 59
  - `getContent()` — line 64
  - `setContent(String)` — line 68
  - `getsEmail()` — line 72
  - `setsEmail(String)` — line 76
  - `getrEmail()` — line 80
  - `setrEmail(String)` — line 84
  - `getFileURL()` — line 88
  - `setFileURL(String)` — line 92
  - `getName()` — line 96
  - `setName(String)` — line 100

### RestURIConstants.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/controller/RestURIConstants.java`
- **Class:** `RestURIConstants` (lines 2-62, plain class)
- **Constants (all `public static final String`):**
  - `ACCEPT_USRS` — line 5 (comment: "unused", but actually used in DriverController)
  - `DECLINE_USRS` — line 6 (comment: "unused", but actually used in DriverController)
  - `CREATE_APPUSR` — line 10
  - `RESET_PASSWORD` — line 11
  - `VALIDATE_USR` — line 12
  - `SAVE_EMAILS` — line 13
  - `GET_EMAILS` — line 14
  - `UPLOAD_PROFILE` — line 16
  - `UPLOAD_PROFILE_APP` — line 17
  - `GET_USR` — line 18
  - `UPDATE_USERS` — line 20
  - `GET_EQUIPMENT` — line 21
  - `SAVE_LICENCE` — line 22
  - `GET_COMPANY` — line 23
  - `GET_COMPANY_DRIVERS` — line 24
  - `SEARCH_COMPANY` — line 26
  - `ADD_COMPANY` — line 27
  - `COMPANY_ACCEPT` — line 28
  - `COMPANY_ACCEPT_WEB` — line 29
  - `COMPANY_DELETE` — line 30
  - `ADD_EQUIPMENT` — line 32
  - `GET_MANUFACTURER` — line 33
  - `GET_TYPE` — line 34
  - `GET_FUELTYPE` — line 35
  - `GET_QUESTION` — line 36
  - `GET_FORMS` — line 37
  - `SEARCH_FORMS` — line 38
  - `SAVE_RESULT` — line 39
  - `DRIVRR_ACCESS` — line 40
  - `START_SESSION` — line 41
  - `END_SESSION` — line 42
  - `SAVE_OFFLINE` — line 43
  - `ABORT_SESSION` — line 44
  - `SAVE_INCIDENT` — line 45
  - `SAVE_IMPACT` — line 46
  - `SAVE_IMPACTIMAGE` — line 47
  - `SAVE_IMPACTIMAGE_APP` — line 48
  - `GET_SERVICE` — line 49
  - `GET_SERVICEDTL` — line 50
  - `SAVE_SERVICE` — line 51
  - `RESUME_EQUIPMENT` — line 52
  - `RESUME_DRIVER` — line 53
  - `GET_REPORT` — line 54
  - `GENERATE_REPORT` — line 55
  - `SEND_REPORT` — line 56
  - `GET_GPS_LOC` — line 57
  - `SAVE_GPS_LOC` — line 58
  - `SAVE_GPS_LOCS` — line 59

---

## Findings

### A08-1: Entire LocationController is dead code still registered as a Spring controller — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java`
**Line(s):** 24-93 (entire file)
**Description:** The Javadoc on line 25 explicitly states `/** Not in Use */`, and grep confirms LocationController is not referenced anywhere in the source code. However, the class is annotated with `@Controller` and maps three REST endpoints (`GET_GPS_LOC`, `SAVE_GPS_LOC`, `SAVE_GPS_LOCS`). Because Spring component scanning will still register this controller, these endpoints remain live and reachable at runtime. Dead code that is still actively wired into the web layer increases the attack surface and maintenance confusion. The controller should either be removed or, at minimum, have its `@Controller` annotation removed to prevent endpoint registration.

### A08-2: JdbcTemplate instantiated per-request instead of being injected — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java`
**Line(s):** 38, 55, 74
**Description:** Each request handler creates `new JdbcTemplate(dataSource)` on every invocation. While functionally correct, `JdbcTemplate` is a thread-safe, reusable object designed to be a singleton. Creating a new instance per request is wasteful and contrary to Spring best practices. It should be a field initialized once (e.g., via `@Autowired` or in a `@PostConstruct` method).

### A08-3: SQL operations not wrapped in a transaction (update + insert race condition) — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java`
**Line(s):** 59-63, 80-84
**Description:** Both `saveGPSLocation` and `saveGPSLocations` perform a two-step SQL operation: first UPDATE all rows to set `current_location = false`, then INSERT a new row with `current_location = true`. These two statements are not wrapped in a `@Transactional` boundary. If the application fails between the UPDATE and INSERT (or a concurrent request interleaves), the data will be left in an inconsistent state with no current location for that unit. The `saveGPSLocations` method is especially vulnerable since it loops over multiple GPS entries without any transaction, meaning a mid-loop failure leaves partial writes.

### A08-4: Duplicated GPS save logic between saveGPSLocation and saveGPSLocations — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java`
**Line(s):** 57-64 vs 78-85
**Description:** The update-then-insert SQL pattern is copy-pasted between `saveGPSLocation` (single GPS) and `saveGPSLocations` (batch). The only difference is the `gps_time` column value (`now()` vs `DateUtil.parseDateTimeIso`). This duplication means a bug fix in one path could easily be missed in the other. The shared logic should be extracted into a common private method or service.

### A08-5: Unused import of `com.journaldev.spring.jdbc.util.Util` in ReportAPI — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java`
**Line(s):** 4
**Description:** The `Util` class is imported but never used in active code. The only reference is inside commented-out code on line 37 (`Util.nthOccurrence`). This generates a compiler warning and is dead code debris.

### A08-6: Commented-out code block in getExportDir — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java`
**Line(s):** 36-38
**Description:** Three lines of code are commented out within `getExportDir`. The original logic for parsing the classpath directory is commented out and replaced by a different approach, but the old code remains as noise. Commented-out code should be removed; version control preserves history.

### A08-7: Dead code path — `dir` variable is computed but immediately overwritten — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java`
**Line(s):** 35, 43
**Description:** In `getExportDir`, line 35 computes `dir` from the class's code source location via `getProtectionDomain().getCodeSource().getLocation()` and performs a `substring(6)`. However, this value is never used because line 43 unconditionally reassigns `dir = "/" + dirctory`. The classpath-based computation on line 35 is entirely dead code that executes uselessly on every call, wasting resources and confusing readers about the method's intent.

### A08-8: Misspelled parameter name `dirctory` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java`
**Line(s):** 34
**Description:** The parameter is named `dirctory` instead of `directory`. While this has no runtime impact, it signals rushed or careless coding and reduces readability. Since `ReportAPI` is used by `ResumeController`, renaming would require coordinated changes but is straightforward.

### A08-9: Misleading `//unused` comment on ACCEPT_USRS and DECLINE_USRS constants — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/RestURIConstants.java`
**Line(s):** 4-6
**Description:** The comment `//unused` on line 4 suggests `ACCEPT_USRS` and `DECLINE_USRS` are not referenced. However, both are actively used in `DriverController.java` (lines 106 and 118 respectively). This misleading comment could lead a developer to delete these constants during cleanup, breaking the application.

### A08-10: Dead constant `GET_SERVICEDTL` with misspelled URL path — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/RestURIConstants.java`
**Line(s):** 50
**Description:** The constant `GET_SERVICEDTL` maps to URL `/rest/sericedetail/get/{userid}` (note: "serice" instead of "service"). A grep across the source tree confirms this constant is never referenced by any controller or other class, making it dead code. The misspelling in the URL path compounds the issue — if this endpoint were ever wired up, clients would need to use the misspelled URL.

### A08-11: Multiple typos in URI constant names and paths — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/RestURIConstants.java`
**Line(s):** 35, 40, 52
**Description:** Several constants contain spelling errors in both names and URL paths:
- Line 35: `GET_FUELTYPE` maps to `/rest/fuletype/get/...` ("fuletype" instead of "fueltype")
- Line 40: `DRIVRR_ACCESS` — name contains "DRIVRR" instead of "DRIVER"
- Line 52: `RESUME_EQUIPMENT` maps to path with `{frequencey}` instead of `{frequency}`
These are actively used (verified via grep for `DRIVRR_ACCESS` and `GET_FUELTYPE`), so the typos are baked into the API contract. Fixing them now would be a breaking change for existing clients, but they should be noted as technical debt.

### A08-12: RestURIConstants is not a utility class — lacks private constructor — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/RestURIConstants.java`
**Line(s):** 3
**Description:** `RestURIConstants` is a constants-only class with all `public static final` fields. It can be instantiated (`new RestURIConstants()`) even though doing so is meaningless. By Java convention, utility/constant classes should have a `private` constructor to prevent instantiation, and ideally should be declared `final`.

### A08-13: ReportAPI fields are protected but class is not abstract — design smell — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java`
**Line(s):** 7-15
**Description:** All eight fields (`subject`, `title`, `content`, `sEmail`, `rEmail`, `fileURL`, `name`, `input`) are declared `protected`, suggesting the class is designed for inheritance. However, no subclass of `ReportAPI` exists in the codebase (verified via grep for `extends ReportAPI`). The class is only used via direct instantiation in `ResumeController`. The `protected` visibility is unnecessarily permissive — these fields should be `private` with access through the existing getters/setters.

### A08-14: `downloadPDF()` mutates `name` field as a side effect — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java`
**Line(s):** 27-31
**Description:** The `downloadPDF()` method calls `HttpDownloadUtility.sendPost(name, input, ...)` using the current value of `this.name`, then immediately overwrites `this.name` with `HttpDownloadUtility.getFileName()` on line 29. This mutation of instance state as a side effect of what appears to be a download operation is surprising and error-prone. If `downloadPDF()` is called twice, the second call uses a different `name` than what was passed to the constructor. The method also relies on static state in `HttpDownloadUtility` (via `getFileName()` and `getSaveFilePath()`), which is not thread-safe.

### A08-15: Logging entire GPS payload with Gson serialization — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java`
**Line(s):** 73
**Description:** `saveGPSLocations` logs `gson.toJson(gpsList)` at INFO level, serializing the entire GPS list payload on every request. This can generate excessive log volume and may expose location data in log files. Additionally, the `gson` field on line 32 is package-private (no access modifier) rather than `private`.

### A08-16: String concatenation in logger.info calls instead of parameterized logging — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java`
**Line(s):** 36, 54, 73, 77
**Description:** All logging statements use string concatenation (e.g., `"Start getGPSLocation." + " UID:" + uid`). SLF4J supports parameterized messages (`logger.info("Start getGPSLocation. UID:{}", uid)`) which avoid string concatenation overhead when the log level is disabled and are the idiomatic pattern.

### A08-17: `getExportDir` uses `getProtectionDomain()` — fragile in containerized/cloud environments — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java`
**Line(s):** 35
**Description:** The method `getExportDir` calls `this.getClass().getProtectionDomain().getCodeSource().getLocation()` to determine a directory path. This approach is fragile: `getCodeSource()` can return `null` when running inside certain application servers, containers, or when loaded by non-standard classloaders, causing a `NullPointerException`. Although the result is currently overwritten (see A08-7), this code still executes and could throw before reaching line 43.
# Pass 4 — Code Quality: A09

## Reading Evidence

### ResumeController.java
- **Class/Interface:** `ResumeController extends ConfigurationController` (line 30), annotated `@Controller`
- **Methods:**
  - `getResumeDriver(@PathVariable("uid") int uid)` — line 35, returns `List<Reports>`
  - `getResumeEquipment(@PathVariable("uid") int uid, @PathVariable("frequencey") String frequencey)` — line 120, returns `List<Charts>`
  - `getReportList(@PathVariable("uid") int uid)` — line 262, returns `List<ReportLists>`
  - `generateReport(@PathVariable("uid") int uid, @PathVariable("rid") int rid)` — line 283, returns `ResponseEntity<Results>`
  - `sendReportList(@PathVariable("freq") String frq)` — line 369, returns `ResponseEntity<Results>`
- **Types/Constants referenced:** `Reports`, `Charts`, `Usage`, `ReportLists`, `ReportAPI`, `Results`, `Permissions`, `DriverEmails`, `DateUtil`, `Util`, `RuntimeConfig`, `RestURIConstants`, `BigDecimal`, `BeanPropertyRowMapper`, `JdbcTemplate`
- **Logger:** `LoggerFactory.getLogger(ResumeController.class)` — line 31

### RuntimeConfig.java
- **Class/Interface:** `RuntimeConfig` (line 3), plain class (no annotations, not a Spring bean)
- **Methods:** None (no methods defined)
- **Fields/Constants (all `public static String`, non-final):**
  - `host` = `"localhost"` — line 5
  - `port` = `"25"` — line 6
  - `sfport` = `"25"` — line 7
  - `sfclass` = `"javax.net.ssl.SSLSocketFactory"` — line 8
  - `mailFrom` = `"info@forkliftiq360.com"` — line 9
  - `emailContent` = `""` — line 10
  - `GCMSERVER` = `"https://gcm-http.googleapis.com/gcm/send"` — line 13
  - `GCMKEY` = `"key=AIzaSyDDuQUYLcXkutyIxRToLAeBPHBQNLfayzs"` — line 14
  - `production_database` = `"jdbc/PreStartDB"` — line 16
  - `LOCATION` = `"https://api.clickatell.com"` — line 17
  - `USERNAME` = `"ciclickatell"` — line 18
  - `PASSWORD` = `"OVLOaICXccaNUS"` — line 19
  - `SMSFROM` = `"13234862361"` — line 20
  - `API_ID` = `"3629505"` — line 21
  - `MSGID_SUCCESS` = `"1"` — line 23
  - `MSGID_CODEERRORR` = `"2"` — line 24
  - `MSGID_CODEE_DUPLICATE_VEHICLE` = `"3"` — line 25
  - `ERRORMSG_CODEERRORR` = `"Code throws exceptions"` — line 26
  - `MSGID_LOGICERRORR` = `"3"` — line 27
  - `ERRORMSG_LOGICERRORR` = `"Result already exists."` — line 28
  - `APIURL` = `"http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/"` — line 30
  - `file_type` = `".pdf"` — line 31
  - `PDF_FOLDER` = `"temp/"` — line 32

### SessionController.java
- **Class/Interface:** `SessionController extends ConfigurationController` (line 51), annotated `@Controller`
- **Fields:**
  - `logger` — `LoggerFactory.getLogger(ConfigurationController.class)` — line 53 (NOTE: wrong class passed to logger factory)
  - `fileStorageService` — `@Autowired @Qualifier("localFileStorage") FileStorageService` — line 55-57
  - `gson` — `new Gson()` — line 59, package-private, not injected
- **Methods:**
  - `driverAccess(@PathVariable("sid") int sid, @PathVariable("imageno") int imageno, @RequestParam("file") MultipartFile file)` — line 63, returns `ResponseEntity<Driver>`
  - `getQuestion(@PathVariable("eid") int eid)` — line 97, returns `ResponseEntity<List<Questions>>`
  - `getForm(@PathVariable("qid") int qid, @PathVariable("type") String type)` — line 138, returns `List<FormDtl>`
  - `searchForm(@PathVariable("uid") int uid, @PathVariable("type") String type, @PathVariable("keyword") String keyword)` — line 154, returns `List<FormDtl>`
  - `saveResults(@RequestBody Result result)` — line 172, returns `ResponseEntity<Results>`
  - `startSessions(@RequestBody Sessions session)` — line 229, returns `ResponseEntity<Sessions>`
  - `toString(Serializable o)` — line 289, private, returns `String`
  - `endSessions(@RequestBody Sessions session)` — line 299, returns `ResponseEntity<Results>`, throws `IOException`
  - `abortSessions(@PathVariable("sid") int sid)` — line 353, returns `ResponseEntity<Results>`
  - `createSession(Sessions session, JdbcTemplate jdbcTemplate)` — line 366, private, returns `int`
  - `saveOffline(@RequestBody OfflineSessions offlineSession)` — line 379, returns `ResponseEntity<Sessions>`
- **Types/Constants referenced:** `Sessions`, `OfflineSessions`, `Result`, `Results`, `Answers`, `Questions`, `Equipment`, `FormDtl`, `Driver`, `DateUtil`, `RuntimeConfig`, `BeanPropertyRowMapper`, `JdbcTemplate`, `Gson`, `FileStorageService`, `ExceptionUtils` (Apache Tika), `BigDecimal`, `Base64`
- **Unused imports:** `java.util.Date` is used only in `Date startTime = ...`. `java.io.ObjectOutputStream`, `java.io.ByteArrayOutputStream`, `java.io.Serializable`, `java.util.Base64` are used only by the private `toString` method.

---

## Findings

### A09-1: Hardcoded Credentials in RuntimeConfig — CRITICAL
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java`
**Line(s):** 14, 18-21, 30
**Description:** The file contains multiple hardcoded credentials and API keys in plain text:
- Line 14: Google GCM API key (`GCMKEY = "key=AIzaSyDDuQUYLcXkutyIxRToLAeBPHBQNLfayzs"`)
- Line 18: Clickatell username (`USERNAME = "ciclickatell"`)
- Line 19: Clickatell password (`PASSWORD = "OVLOaICXccaNUS"`)
- Line 21: Clickatell API ID (`API_ID = "3629505"`)

These credentials are committed to source control and are visible to anyone with repository access. They should be externalized to environment variables, a secrets manager, or at minimum a Spring configuration properties file excluded from source control.

### A09-2: Hardcoded Admin Credentials in Report Generation — CRITICAL
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java`
**Line(s):** 322, 410
**Description:** Admin credentials are hardcoded directly in JSON strings used for report API calls:
- Line 322: `"admin_password\":\"ciiadmin\", \"username\": \"hui\""`
- Line 410: `"admin_password\":\"ciiadmin\", \"username\": \"hui\""`

The admin password `ciiadmin` and username `hui` are embedded in source code. The `input` string containing these credentials is also logged at INFO level (lines 323 and 411), which means the password will appear in log files.

### A09-3: Sensitive Credentials Logged at INFO Level — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java`
**Line(s):** 323, 411
**Description:** The report API input payload, which includes `admin_password` and `username`, is logged at INFO level: `logger.info("Input URL is:" + input)`. This means credentials will be written to production log files, making them accessible to anyone who can read logs.

### A09-4: Non-final Mutable Public Static Fields in RuntimeConfig — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java`
**Line(s):** 5-32 (all fields)
**Description:** Every field in `RuntimeConfig` is declared `public static` but not `final`. This means any code in the application can modify these "configuration" values at runtime, leading to unpredictable behavior. Constants like `MSGID_SUCCESS`, `ERRORMSG_CODEERRORR`, etc. should be declared `final`. Fields that are intended as configurable should be managed via Spring's property injection mechanism rather than mutable statics.

### A09-5: Logger Initialized with Wrong Class in SessionController — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java`
**Line(s):** 53
**Description:** The logger is initialized as `LoggerFactory.getLogger(ConfigurationController.class)` instead of `LoggerFactory.getLogger(SessionController.class)`. All log entries from SessionController will appear under the `ConfigurationController` logger name, making it difficult to filter and diagnose issues specific to SessionController. This is a common copy-paste error.

### A09-6: Broken SQL Syntax in searchForm Method — CRITICAL
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java`
**Line(s):** 163
**Description:** The SQL query on line 163 contains syntactically broken SQL: `" where u. l.question_id = question_id = ? and type ilike ?) "`. The fragment `u. l.question_id = question_id = ?` appears to be garbled -- there is a stray `u.` with a space before `l.question_id`, and `= question_id = ?` is a double-equals comparison that is invalid SQL. This endpoint will throw a runtime SQL exception on every invocation, meaning the `SEARCH_FORMS` feature is completely non-functional.

### A09-7: Stale TODO Comments from 2017 — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java`
**Line(s):** 116, 143, 152, 170, 187, 229
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java`
**Line(s):** 151
**Description:** Multiple TODO comments dated from June-July 2017 are scattered through the code, e.g., `// TODO inserted [15 Jun 2017,4:32:27 pm]` and `// TODO [19 Jun 2017,9:06:09 pm]`. These have been present for approximately 9 years with no apparent resolution. They appear to be auto-generated markers rather than actionable work items. They add noise and should either be resolved or removed.

### A09-8: Commented-Out Code Block in startSessions — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java`
**Line(s):** 246-251
**Description:** A block of commented-out code exists in the `startSessions` method, preceded by the comment `//No need ot check other driver uses it`. This dead code checks whether another driver is using the same unit. It should be removed entirely rather than left commented out; the comment explains the rationale, which should be preserved as a plain comment if needed.

### A09-9: JdbcTemplate Created Per-Request Instead of Injected — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java`
**Line(s):** 38, 123, 265, 288, 374
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java`
**Line(s):** 65, 100, 141, 157, 174, 231, 301, 355, 385
**Description:** Every controller method creates a new `JdbcTemplate` instance via `new JdbcTemplate(dataSource)`. JdbcTemplate is designed to be thread-safe and reusable; Spring best practice is to create it once (typically via `@Autowired` or in a `@PostConstruct` method) and reuse the same instance. Creating a new instance per request introduces unnecessary object creation overhead and goes against the framework's intended usage pattern.

### A09-10: Wildcard Import for Model Package — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java`
**Line(s):** 4
**Description:** Line 4 uses a wildcard import: `import com.journaldev.spring.jdbc.model.*`. This obscures which model classes are actually used by the controller and can cause unexpected compilation issues if new classes are added to the model package. Explicit imports (as used in SessionController) are preferred for clarity.

### A09-11: `e.printStackTrace()` Instead of Logger-Based Error Logging — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java`
**Line(s):** 353, 421
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java`
**Line(s):** 89
**Description:** Exception handling uses `e.printStackTrace()` which writes to standard error rather than the application's configured logging framework. This means error information will not appear in log files, will not be subject to log rotation, and cannot be filtered or monitored. The exceptions should be logged via `logger.error("message", e)` instead.

### A09-12: Duplicate Constant Values in RuntimeConfig — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java`
**Line(s):** 25, 27
**Description:** `MSGID_CODEE_DUPLICATE_VEHICLE` (line 25) and `MSGID_LOGICERRORR` (line 27) both have the value `"3"`. This creates ambiguity in error handling since the same message ID maps to two different error conditions. Additionally, the constant names contain typos: `CODEE` (double E), `CODEERRORR` (double R), `LOGICERRORR` (double R).

### A09-13: Misspelled URL Path Variable "frequencey" — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java`
**Line(s):** 120
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/RestURIConstants.java` (line 52)
**Description:** The path variable and parameter are consistently named `frequencey` (with a stray 'e') instead of `frequency`. While consistent misspelling does not cause a runtime bug, it propagates a spelling error into the public REST API path (`/rest/driverresume/get/{uid}/frequencey/{frequencey}`), which becomes part of the API contract and is harder to fix later.

### A09-14: Repeated Email-Sending Logic (addr1 through addr4) — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java`
**Line(s):** 332-350
**Description:** The `generateReport` method contains four near-identical blocks checking and sending emails to `email_addr1` through `email_addr4`. This repetition violates DRY (Don't Repeat Yourself) and is error-prone -- any change to the email-sending logic must be replicated in four places. The addresses should be collected into a list and iterated.

### A09-15: HTTP Used for API URL Instead of HTTPS — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java`
**Line(s):** 30
**Description:** The `APIURL` field uses plain HTTP: `"http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/"`. This URL is used for report generation API calls that include admin credentials in the payload. Transmitting credentials over unencrypted HTTP exposes them to network-level interception.

### A09-16: Deprecated Google GCM Reference — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java`
**Line(s):** 13-14
**Description:** `GCMSERVER` references `https://gcm-http.googleapis.com/gcm/send`, which is Google Cloud Messaging. GCM was officially deprecated by Google in April 2018 and shut down in May 2019. The server URL and API key (`GCMKEY`) are pointing to a non-functional service. If push notifications are still needed, the code must be migrated to Firebase Cloud Messaging (FCM).

### A09-17: Class Javadoc Does Not Match Class Purpose — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java`
**Line(s):** 27-28
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java`
**Line(s):** 47-49
**Description:** ResumeController's Javadoc says "Handles requests for the Product JDBC Service" and SessionController's says "Handles requests for the Employee JDBC Service." Neither description matches the actual content of the respective controller. These appear to be leftover boilerplate from the original project template (journaldev tutorials).

### A09-18: Unused `keyword` Parameter in searchForm — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java`
**Line(s):** 154
**Description:** The `searchForm` method accepts a `@PathVariable("keyword") String keyword` parameter, but this variable is never used in the query or passed as a parameter to `jdbcTemplate.query()` on line 165. The query uses `uid` and `type` only. Since the SQL itself is also broken (see A09-6), this compounds the issue -- even if the SQL were fixed, the keyword search would not function without binding `keyword` to the query.

### A09-19: `toString(Serializable)` Method Shadows `Object.toString()` Semantically — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java`
**Line(s):** 289-295
**Description:** The private `toString(Serializable o)` method serializes an object to Base64. While it does not technically override `Object.toString()` (different signature), the name is confusing and misleading. It is only called once (line 343) to serialize a `Sessions` object for error logging. A name like `serializeToBase64` would be clearer. Additionally, if the Sessions object is not fully serializable (e.g., transient dependencies), this could throw an unexpected exception inside the catch block of `endSessions`, silently losing the original error context.

### A09-20: GET Endpoint Used for State-Changing Operations — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java`
**Line(s):** 281 (generateReport), 367 (sendReportList)
**Description:** Both `generateReport` and `sendReportList` are mapped as `RequestMethod.GET` but perform state-changing side effects: they generate PDF reports and send emails. Using GET for operations with side effects violates HTTP semantics (GET should be safe and idempotent). This means the operations could be triggered unintentionally by browser prefetch, web crawlers, caching proxies, or retry mechanisms.

### A09-21: No Input Validation on Path Variables — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java`
**Line(s):** 35, 120, 262, 283
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java`
**Line(s):** 63, 97, 138, 154, 353
**Description:** None of the controller methods validate their path variable inputs. For example, `uid`, `eid`, `sid`, `qid`, and `rid` are used directly in SQL queries without checking for valid ranges (e.g., positive integers). While parameterized queries prevent SQL injection, invalid or negative IDs could cause `EmptyResultDataAccessException` or `NullPointerException` from `queryForObject` returning null, leading to unhandled 500 errors.

### A09-22: Potential NullPointerException in endSessions — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java`
**Line(s):** 316
**Description:** In `endSessions`, `queryForObject` on line 316 retrieves `acc_hour` as `BigDecimal`. If the session's `finish_time - start_time` produces NULL (e.g., if the update on line 312-313 sets a null finish_time), `queryForObject` can return null, and subsequent operations on `acc_hour` will throw `NullPointerException`. The `EmptyResultDataAccessException` catch on line 342 would not catch a NPE, causing an unhandled 500 response.

### A09-23: Inconsistent Error HTTP Status Code Usage — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java`
**Line(s):** 90, 108, 221
**Description:** `HttpStatus.BAD_GATEWAY` (502) is used for application-level errors such as "equipment not found" (line 108), "IOException during file upload" (line 90), and "duplicate result" (line 221). HTTP 502 indicates that the server, while acting as a gateway or proxy, received an invalid response from an upstream server. These conditions are actually client errors (400-level) or internal errors (500-level). Using 502 misleads monitoring tools and API consumers.
# Pass 4 — Code Quality: A10

## Reading Evidence

### UserController.java
- **Class/Interface:** `UserController` (line 17), annotated `@Controller`
- **Methods:**
  - `getUserByEmail(String email)` — line 23, returns `ResponseEntity<User>`, annotated `@RequestMapping(value = "/rest/admin/user", method = RequestMethod.GET)` and `@ResponseBody`
- **Types/Constants:**
  - Field: `UserDAO userDao` (line 20, `@Autowired`)
  - Import: `UserDAO`, `User`, Spring annotations, `java.util.Optional`
- **Observations:**
  - Total lines: 33
  - Uses `@Controller` + `@ResponseBody` instead of `@RestController`
  - Method parameter named `email` but DAO method called is `findByName(email)` — semantic mismatch
  - Returns `HttpStatus.BAD_GATEWAY` (502) when user is not found

### APIConnections.java
- **Class/Interface:** `APIConnections implements Serializable` (line 5)
- **Methods:**
  - `getIDAPIConnection()` — line 18, returns `int`
  - `setIDAPIConnection(int iDAPIConnection)` — line 21
  - `getAPIConnectionKey()` — line 24, returns `String`
  - `setAPIConnectionKey(String aPIConnectionKey)` — line 27
- **Types/Constants:**
  - `serialVersionUID = 4127356077977670047L` (line 12)
  - Field: `int IDAPIConnection` (line 15)
  - Field: `String APIConnectionKey` (line 16)
- **Observations:**
  - Total lines: 33
  - Empty Javadoc comment block (lines 9-11)
  - Fields violate Java naming conventions (uppercase start)
  - Setter parameter names start with lowercase abbreviation (`iDAPIConnection`, `aPIConnectionKey`) — auto-generated with odd casing
  - Setter bodies assign without `this.` qualifier, relying on parameter name differing from field name
  - Multiple consecutive blank lines (lines 7-8, 30-32)

### Answers.java
- **Class/Interface:** `Answers implements Serializable` (line 5)
- **Methods:**
  - `getId()` — line 16, returns `int`
  - `setId(int id)` — line 19
  - `getAnswer()` — line 22, returns `String`
  - `setAnswer(String answer)` — line 25
  - `getQuestion_id()` — line 29, returns `int`
  - `setQuestion_id(int question_id)` — line 32
- **Types/Constants:**
  - `serialVersionUID = -2642278162514242302L` (line 10)
  - Field: `int id` (line 12)
  - Field: `String answer` (line 13)
  - Field: `int question_id` (line 14)
- **Observations:**
  - Total lines: 36
  - Empty Javadoc comment block (lines 7-9)
  - Field `question_id` uses snake_case — violates Java camelCase convention
  - Getter/setter `getQuestion_id` / `setQuestion_id` also use snake_case

---

## Findings

### A10-1: Incorrect HTTP Status Code for "Not Found" — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/UserController.java`
**Line(s):** 30
**Description:** When a user is not found by email, the controller returns `HttpStatus.BAD_GATEWAY` (502). HTTP 502 indicates a server acting as a gateway received an invalid response from an upstream server — it has no semantic relationship to "entity not found." The correct status would be `HttpStatus.NOT_FOUND` (404) or potentially `HttpStatus.NO_CONTENT` (204). Returning 502 will mislead API consumers and monitoring systems, potentially triggering false infrastructure alerts for what is a normal application-level condition.

### A10-2: Semantic Mismatch Between Parameter Name and DAO Method — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/UserController.java`
**Line(s):** 23-25
**Description:** The controller method parameter is named `email` and the request parameter annotation is `@RequestParam("email")`, but the DAO method invoked is `userDao.findByName(email)`. The method name `findByName` suggests a search by user name, not by email. This is either a naming bug in the DAO (method should be `findByEmail`) or a logic bug in the controller (wrong DAO method called). This mismatch makes the code confusing and error-prone for maintainers.

### A10-3: Use of @Controller + @ResponseBody Instead of @RestController — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/UserController.java`
**Line(s):** 16, 23
**Description:** The class uses `@Controller` at class level and `@ResponseBody` on the method return type. The idiomatic Spring approach since Spring 4.0 is to use `@RestController` which combines both annotations, reducing boilerplate and making the intent clearer. This is a minor style inconsistency with modern Spring conventions.

### A10-4: Java Naming Convention Violations in Field Names — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/APIConnections.java`
**Line(s):** 15-16
**Description:** Fields `IDAPIConnection` and `APIConnectionKey` start with uppercase letters, violating the Java naming convention that instance fields should begin with a lowercase letter (e.g., `idApiConnection`, `apiConnectionKey`). This causes the auto-generated setter parameters to have awkward names (`iDAPIConnection`, `aPIConnectionKey`) and will produce non-standard JavaBean property names, potentially causing issues with serialization frameworks, JSON mappers, and ORM tools that rely on standard JavaBean conventions.

### A10-5: Setter Methods Do Not Use `this` Qualifier — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/APIConnections.java`
**Line(s):** 21-22, 27-28
**Description:** The setter methods in `APIConnections` assign to the field without using the `this.` qualifier (e.g., `IDAPIConnection = iDAPIConnection`). This only works because the parameter names differ in casing from the field names due to the naming convention violations. This is fragile — if the field names are ever corrected to follow conventions, these setters would silently self-assign without `this.`, becoming no-ops. Consistent use of `this.` in setters is a defensive best practice.

### A10-6: Snake_case Field and Method Names in Java Model — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Answers.java`
**Line(s):** 14, 29, 32
**Description:** The field `question_id` and its getter/setter (`getQuestion_id`, `setQuestion_id`) use snake_case, which violates Java naming conventions. The field should be `questionId` with methods `getQuestionId()` and `setQuestionId()`. Snake_case in Java fields suggests this was mapped directly from a database column name without proper naming translation. This may cause issues with JSON serialization libraries that derive JSON keys from JavaBean property names, and is inconsistent with the other fields in the same class.

### A10-7: Empty Javadoc Comment Blocks — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/APIConnections.java`, `src/main/java/com/journaldev/spring/jdbc/model/Answers.java`
**Line(s):** APIConnections.java:9-11, Answers.java:7-9
**Description:** Both model classes contain empty Javadoc comment blocks (just `/** */` with no content) above `serialVersionUID`. These are auto-generated Eclipse-style suppressions for the serialization warning and provide no documentation value. They add visual noise without conveying information.

### A10-8: Class Named as Plural When Representing a Single Entity — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Answers.java`, `src/main/java/com/journaldev/spring/jdbc/model/APIConnections.java`
**Line(s):** Answers.java:5, APIConnections.java:5
**Description:** Both model classes use plural names (`Answers`, `APIConnections`) but each instance represents a single entity (one answer, one API connection). Java convention for model/entity classes is to use singular names (`Answer`, `APIConnection`). Plural names are typically reserved for collection utilities or service classes. This can mislead developers into thinking the class represents a collection.

### A10-9: Field Injection via @Autowired — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/controller/UserController.java`
**Line(s):** 19-20
**Description:** The `userDao` dependency is injected using field injection (`@Autowired` on a private field). Constructor injection is the recommended approach in modern Spring as it makes dependencies explicit, supports immutability, simplifies testing (no reflection needed), and allows the compiler to enforce required dependencies. The Spring team has officially recommended constructor injection since Spring 4.x.
# Pass 4 — Code Quality: A11

## Reading Evidence

### AuthenticationRequest.java
- **Class/Interface:** `AuthenticationRequest` (class, implements `Serializable`)
- **Annotations:** `@Data`, `@NoArgsConstructor`, `@Builder` (on constructor)
- **Fields:**
  - `serialVersionUID` (line 16): `private static final long` = `152396558777730489L`
  - `username` (line 17): `private String`
  - `password` (line 18): `private String`
  - `newPassword` (line 19): `private String`
  - `accessToken` (line 20): `private String`
- **Methods:**
  - `AuthenticationRequest(String, String, String, String)` (line 23): private constructor with `@Builder`
- **Imports:** `java.io.Serializable`, `lombok.Builder`, `lombok.Data`, `lombok.NoArgsConstructor`

### AuthenticationResponse.java
- **Class/Interface:** `AuthenticationResponse` (class, extends `ResponseWrapper`)
- **Annotations:** `@Data`, `@EqualsAndHashCode(callSuper=true)`, `@NoArgsConstructor`, `@JsonInclude(JsonInclude.Include.NON_NULL)`
- **Fields:**
  - `serialVersionUID` (line 17): `private static final long` = `408336884318011949L`
  - `accessToken` (line 18): `private String`
  - `sessionToken` (line 19): `private String`
  - `expiresIn` (line 20): `private String`
  - `actualDate` (line 21): `private String`
  - `expirationDate` (line 22): `private String`
  - `userData` (line 23): `private UserResponse`
  - `username` (line 24): `private String`
  - `message` (line 25): `private String`
- **Methods:** None explicitly defined (Lombok-generated via `@Data`)
- **Imports:** `com.fasterxml.jackson.annotation.JsonInclude`, `lombok.Data`, `lombok.EqualsAndHashCode`, `lombok.NoArgsConstructor`

### Charts.java
- **Class/Interface:** `Charts` (class, implements `Serializable`)
- **Annotations:** None
- **Fields:**
  - `serialVersionUID` (line 14): `private static final long` = `-2487058812368828477L`
  - `unit_id` (line 16): `private int`
  - `unit` (line 17): `private String`
  - `total` (line 18): `private BigDecimal`
  - `usageList` (line 19): `private List<Usage>`, initialized to `new ArrayList<Usage>()`
- **Methods:**
  - `getUnit()` (line 21): returns `String`
  - `setUnit(String)` (line 24): void
  - `getTotal()` (line 27): returns `BigDecimal`
  - `setTotal(BigDecimal)` (line 30): void
  - `getUsageList()` (line 33): returns `List<Usage>`
  - `setUsageList(List<Usage>)` (line 36): void
  - `addUsageList(Usage)` (line 40): void
  - `getUnit_id()` (line 43): returns `int`
  - `setUnit_id(int)` (line 46): void
- **Imports:** `java.io.Serializable`, `java.math.BigDecimal`, `java.util.ArrayList`, `java.util.List`

---

## Findings

### A11-1: Inconsistent code style -- Charts.java uses manual getters/setters while sibling models use Lombok — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Charts.java`
**Line(s):** 9-51 (entire class)
**Description:** `AuthenticationRequest` and `AuthenticationResponse` both use Lombok `@Data` to auto-generate getters, setters, `toString`, `equals`, and `hashCode`. In contrast, `Charts.java` manually defines all getters and setters without any Lombok annotations. This is a style inconsistency within the same model package. It also means `Charts` lacks `toString()`, `equals()`, and `hashCode()` implementations, which could cause subtle bugs in collections or logging. The class should either use `@Data` (consistent with the rest of the codebase) or, at minimum, implement `equals`/`hashCode` to honour the `Serializable` contract.

### A11-2: Snake_case field naming violates Java conventions in Charts.java — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Charts.java`
**Line(s):** 16, 43, 46
**Description:** The field `unit_id` and its corresponding accessors `getUnit_id()` / `setUnit_id(int)` use snake_case naming, which violates the standard Java camelCase naming convention (should be `unitId`, `getUnitId()`, `setUnitId()`). This will also cause issues with frameworks that rely on JavaBean conventions (e.g., Jackson will serialize it as `unit_id` rather than `unitId` unless a `@JsonProperty` annotation is used). Sibling fields like `usageList` and `accessToken` in other classes correctly use camelCase.

### A11-3: Mutable internal list exposed via getter in Charts.java — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Charts.java`
**Line(s):** 33-34, 36-38
**Description:** `getUsageList()` returns a direct reference to the internal `ArrayList`. External callers can mutate the list without going through the class API, bypassing the `addUsageList()` method. This is a leaky abstraction. A defensive copy or an unmodifiable view (`Collections.unmodifiableList(usageList)`) should be returned if the intent of `addUsageList()` is to control list modification. Alternatively, if using Lombok `@Data`, the `@Singular` annotation on a builder could manage this properly.

### A11-4: Sensitive credential fields lack serialization protection in AuthenticationRequest — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/model/AuthenticationRequest.java`
**Line(s):** 17-20
**Description:** The `password` and `newPassword` fields are plain `String` fields with no `@JsonIgnore` on output, no `transient` keyword, and no `@ToString.Exclude` annotation. Since the class uses Lombok `@Data`, the auto-generated `toString()` method will include `password` and `newPassword` in its output. Any logging statement that prints this object (e.g., `log.debug("Request: {}", authRequest)`) will leak credentials into log files. At minimum, `@ToString.Exclude` should be applied to `password` and `newPassword`. Ideally, these fields should also be marked `@JsonIgnore` for response serialization contexts or marked `transient` to prevent unintended serialization.

### A11-5: Empty Javadoc comments on serialVersionUID fields — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/AuthenticationRequest.java`, `AuthenticationResponse.java`, `Charts.java`
**Line(s):** AuthenticationRequest:13-15, AuthenticationResponse:14-16, Charts:11-13
**Description:** All three files contain empty Javadoc-style comment blocks (`/** * */`) directly above the `serialVersionUID` field. These are auto-generated IDE placeholders that provide no value and add noise. They should either be removed or replaced with meaningful documentation.

### A11-6: AuthenticationResponse.message field duplicates ResponseWrapper.errors purpose — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/AuthenticationResponse.java`
**Line(s):** 25
**Description:** `AuthenticationResponse` extends `ResponseWrapper` which already contains a `List<ErrorMessage> errors` field for communicating error/status information. The `message` field in `AuthenticationResponse` may serve a similar purpose, creating ambiguity about which field consumers should check for status information. This is a potential design smell. If `message` is for success messages, consider documenting it clearly; if it duplicates error messaging, it should be consolidated.

### A11-7: String types used for temporal fields in AuthenticationResponse — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/AuthenticationResponse.java`
**Line(s):** 20-22
**Description:** `expiresIn`, `actualDate`, and `expirationDate` are all declared as `String`. Using `String` for date/time values loses type safety, allows invalid date strings, and requires manual parsing at every usage site. Prefer `java.time.Instant`, `java.time.LocalDateTime`, or at minimum `java.util.Date` with appropriate Jackson serialization configuration. This is flagged as LOW because these values may originate from an external API (e.g., Cognito) and may be intentionally stored as-is.

### A11-8: Unused @Builder import retained despite @Builder only on constructor in AuthenticationRequest — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/AuthenticationRequest.java`
**Line(s):** 5, 22-28
**Description:** The `@Builder` annotation is applied to the private all-args constructor rather than at the class level. While this is a valid pattern that works correctly, it is atypical -- the more common approach is `@Builder` at the class level (or combined with `@AllArgsConstructor(access = AccessLevel.PRIVATE)`). The current approach works but may confuse maintainers. This is informational only; the code compiles and functions correctly.
# Pass 4 — Code Quality: A12

## Reading Evidence

### Company.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/Company.java`
- **Class:** `Company implements Serializable` (lines 13-51)
- **Annotations:** `@Data`, `@NoArgsConstructor` (Lombok)
- **Constants:** `serialVersionUID = 8023991868841881837L` (line 18)
- **Fields:**
  - `Long id` (line 20)
  - `String name` (line 21)
  - `String email` (line 22)
  - `String password` (line 23)
  - `List<Roles> arrRoles` (line 24)
  - `Permissions permission` (line 25)
  - `Integer timezone` (line 26)
  - `String dateFormat` (line 27)
  - `Integer maxSessionLength` (line 28)
  - `Driver contactDriver` (line 30)
- **Methods:**
  - `Company(Long, String, String, String, Integer, String, Integer, List<Roles>, Permissions, Driver)` — private builder constructor (line 33)
- **Imports:** `lombok.Builder`, `lombok.Data`, `lombok.NoArgsConstructor`, `lombok.Singular`, `java.io.Serializable`, `java.util.List`
- **Types referenced:** `Roles`, `Permissions`, `Driver`

### Driver.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/Driver.java`
- **Class:** `Driver implements Serializable` (lines 15-87)
- **Annotations:** `@Data`, `@NoArgsConstructor`, `@EqualsAndHashCode(onlyExplicitlyIncluded = true)` (Lombok)
- **Constants:** `serialVersionUID = -100229563698950401L` (line 16)
- **Fields:**
  - `Long id` (line 18)
  - `String first_name` (line 19)
  - `String last_name` (line 20)
  - `String email` (line 23, `@EqualsAndHashCode.Include`)
  - `String password` (line 25)
  - `String phone` (line 26)
  - `String licno` (line 27)
  - `String expirydt` (line 28)
  - `String addr` (line 29)
  - `String securityno` (line 30)
  - `String photo_url` (line 31)
  - `boolean contactperson` (line 32)
  - `String ranking` (line 33)
  - `Long comp_id` (line 34)
  - `boolean driver_based` (line 35)
  - `String date_format` (line 36)
  - `Integer max_session_length` (line 37)
  - `String compliance_date` (line 38)
  - `Integer gps_frequency` (line 39)
  - `List<Driver> drivers` (line 41)
  - `List<DriverTraining> arrDriverTrainings` (line 43)
- **Methods:**
  - `Driver(Long, String, String, String, String, String, String, String, String, String, String, boolean, String, Long, boolean, String, Integer, String, List<DriverTraining>, Integer)` — private builder constructor (line 47)
- **Imports:** `lombok.Builder`, `lombok.Data`, `lombok.EqualsAndHashCode`, `lombok.NoArgsConstructor`, `lombok.Singular`, `java.io.Serializable`, `java.util.List`
- **Types referenced:** `DriverTraining`

### DriverEmails.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/DriverEmails.java`
- **Class:** `DriverEmails implements Serializable` (lines 5-59)
- **Annotations:** None
- **Constants:** `serialVersionUID = 2730515601304224328L` (line 10)
- **Fields:**
  - `int id` (line 12)
  - `int driver_id` (line 13)
  - `String email_addr1` (line 14)
  - `String email_addr2` (line 15)
  - `String email_addr3` (line 16)
  - `String email_addr4` (line 17)
- **Methods:**
  - `getId()` (line 20)
  - `setId(int)` (line 23)
  - `getDriver_id()` (line 26)
  - `setDriver_id(int)` (line 29)
  - `getEmail_addr1()` (line 32)
  - `setEmail_addr1(String)` (line 35)
  - `getEmail_addr2()` (line 38)
  - `setEmail_addr2(String)` (line 41)
  - `getEmail_addr3()` (line 44)
  - `setEmail_addr3(String)` (line 47)
  - `getEmail_addr4()` (line 50)
  - `setEmail_addr4(String)` (line 53)
- **Imports:** `java.io.Serializable`

---

## Findings

### A12-1: Sensitive fields (password, securityno) exposed via Lombok @Data with no serialization protection — CRITICAL
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Driver.java`
**Line(s):** 25, 30
**Description:** The `Driver` class uses `@Data` which generates public `getPassword()` and `getSecurityno()` getters/setters. There are no `@JsonIgnore`, `@ToString.Exclude`, or similar annotations on the `password` or `securityno` fields. When a `Driver` object is serialized to JSON (e.g., in REST responses), these sensitive values will be included in the output by default. The `securityno` field name suggests a social security number or similar PII. The `password` field is present as a plain `String` without any indication it is hashed. The `@Data`-generated `toString()` will also include these values, risking exposure in log statements. The same issue applies to `Company.java` (line 23) where `password` is similarly unprotected.

### A12-2: Sensitive field (password) exposed in Company model with no serialization exclusion — CRITICAL
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Company.java`
**Line(s):** 23
**Description:** The `password` field on `Company` is a plain `String` exposed via Lombok `@Data` getters/setters and `toString()`. There is no `@JsonIgnore` or `@ToString.Exclude` annotation. This field is also overwritten from `contactDriver.getPassword()` at line 48, propagating sensitive data from one model to another without protection.

### A12-3: Builder constructor silently overrides explicitly-set name/email/password when contactDriver is non-null — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Company.java`
**Line(s):** 44-49
**Description:** The builder constructor first sets `this.name`, `this.email`, and `this.password` from the explicit parameters (lines 35-37), then immediately overwrites them if `contactDriver` is not null (lines 46-48). This is a leaky abstraction: a caller using `Company.builder().name("Custom").email("custom@x.com").contactDriver(driver).build()` would have their explicit values silently discarded. The override logic embedded inside the constructor is not discoverable from the builder API. This conditional mutation in a constructor also makes the object harder to reason about and test.

### A12-4: Self-referential List<Driver> field in Driver model not included in Builder — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Driver.java`
**Line(s):** 41
**Description:** The `drivers` field (`List<Driver>`) is declared as an instance field (line 41) but is not included as a parameter in the `@Builder` constructor (lines 47-65). This means the Builder pattern cannot set this field; it can only be set via the Lombok-generated `setDrivers()`. This is an inconsistent construction pattern -- some fields are set via builder, others only via setters. More critically, a `Driver` containing a `List<Driver>` creates a recursive/self-referential data structure. If serialized (JSON, `toString()`, or logging), this can cause infinite recursion or `StackOverflowError` if any driver in the list also has a non-null `drivers` list. There is no `@JsonManagedReference`/`@JsonBackReference` or cycle-breaking annotation.

### A12-5: Style inconsistency -- DriverEmails uses manual getters/setters while sibling models use Lombok — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/DriverEmails.java`
**Line(s):** 5-59
**Description:** `DriverEmails` manually defines all getters and setters (12 methods for 6 fields), while the sibling classes `Company` and `Driver` in the same package both use Lombok `@Data` to auto-generate them. This inconsistency creates unnecessary boilerplate and increases maintenance burden. The class also lacks `@NoArgsConstructor`, `@Data`, or any Lombok annotations, making it stylistically out of step with the rest of the model layer. It also lacks `equals()`/`hashCode()`/`toString()` implementations.

### A12-6: Repeated email fields (email_addr1 through email_addr4) instead of a collection — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/DriverEmails.java`
**Line(s):** 14-17
**Description:** The `DriverEmails` class models multiple email addresses as four distinct fields (`email_addr1` through `email_addr4`) rather than using a `List<String>` or similar collection. This is a rigid design that hard-codes a maximum of 4 email addresses. Any logic that processes all email addresses must individually reference each field rather than iterating over a collection, leading to repetitive and fragile code. This is a code smell indicative of a denormalized database column mapping leaking into the domain model without abstraction.

### A12-7: Java field naming uses snake_case instead of camelCase convention — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Driver.java`
**Line(s):** 19-20, 28-39
**Description:** Multiple fields in `Driver` use snake_case naming (`first_name`, `last_name`, `photo_url`, `comp_id`, `driver_based`, `date_format`, `max_session_length`, `compliance_date`, `gps_frequency`). Standard Java naming convention uses camelCase for fields. With Lombok `@Data`, the generated getter/setter names become `getFirst_name()` / `setFirst_name()`, which violates JavaBean conventions and can cause issues with frameworks that rely on standard property naming (e.g., Jackson, Spring BeanPropertyRowMapper). The same issue exists in `DriverEmails.java` (lines 13-17) with `driver_id`, `email_addr1` etc.

### A12-8: Date/time fields stored as String instead of proper temporal types — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Driver.java`
**Line(s):** 28, 38
**Description:** The fields `expirydt` (line 28) and `compliance_date` (line 38) represent dates but are declared as `String`. This loses type safety, makes date comparisons/arithmetic require parsing, and allows invalid date values to be stored in the model. Java's `LocalDate`, `LocalDateTime`, or `java.util.Date` should be used for date fields. Similarly, `dateFormat` in `Company.java` (line 27) stores a date format pattern as a String, which is acceptable, but the `timezone` field (line 26) is an `Integer` rather than `java.time.ZoneId` or `java.util.TimeZone`.

### A12-9: Unused import — lombok.Singular in Company.java used only on builder parameter — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Company.java`
**Line(s):** 6
**Description:** The `lombok.Singular` import is used on the `@Singular` annotation on the builder constructor parameter `arrRoles` (line 33). While technically used, the `@Singular` annotation on a manually-written `@Builder` constructor parameter is a non-standard pattern. Normally `@Singular` is placed on the field declaration when `@Builder` is at the class level. Placed only on the constructor parameter, its behavior depends on the Lombok version and may not generate the expected singular-add builder methods (`arrRole(Roles r)` in addition to `arrRoles(List<Roles>)`). This should be verified.

### A12-10: Empty Javadoc comment on serialVersionUID — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Company.java`, `src/main/java/com/journaldev/spring/jdbc/model/DriverEmails.java`
**Line(s):** Company.java:15-17, DriverEmails.java:7-9
**Description:** Both `Company.java` and `DriverEmails.java` have empty Javadoc comments (`/** */`) above the `serialVersionUID` field. These appear to be IDE-generated placeholders that were never filled in. They add visual noise without providing any documentation value and should either be removed or populated with meaningful content.

### A12-11: Primitive int used for id/driver_id in DriverEmails vs Long/Integer in sibling models — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/DriverEmails.java`
**Line(s):** 12-13
**Description:** `DriverEmails` uses primitive `int` for `id` and `driver_id`, while `Company` and `Driver` use `Long` for their `id` fields. Using primitives means these fields cannot represent null (e.g., for unsaved entities), defaulting to 0 instead. This is inconsistent with the rest of the model layer and could cause subtle bugs when checking whether an entity has been persisted.

### A12-12: @EqualsAndHashCode based solely on email in Driver may cause collisions — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Driver.java`
**Line(s):** 14, 22-23
**Description:** The `@EqualsAndHashCode(onlyExplicitlyIncluded = true)` annotation restricts equality to only the `email` field (line 23). While email is often unique, if two Driver instances have the same email but different `id` values (e.g., during a migration or data merge scenario), they would be considered equal. Including `id` in the equality check (or using `id` alone) would be more robust for entity identity.
# Pass 4 — Code Quality: A13

## Reading Evidence

### DriverEquipment.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/DriverEquipment.java`
- **Class:** `DriverEquipment extends Equipment` (line 10)
- **Annotations:** `@Data` (line 7), `@NoArgsConstructor` (line 8), `@EqualsAndHashCode(callSuper = false)` (line 9)
- **Fields:**
  - `serialVersionUID: long` (line 11) — constant: `-2200458485098129108L`
  - `hours: Integer` (line 13)
  - `trained: Boolean` (line 14)
- **Methods:** None explicitly defined (Lombok-generated via `@Data`)
- **Imports:** `lombok.Data`, `lombok.EqualsAndHashCode`, `lombok.NoArgsConstructor`

### DriverTraining.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java`
- **Class:** `DriverTraining implements Serializable` (line 14)
- **Annotations:** `@Data` (line 12), `@NoArgsConstructor` (line 13)
- **Fields:**
  - `serialVersionUID: long` (line 17) — constant: `3211228421130022712L`
  - `id: int` (line 19)
  - `manufacture_id: int` (line 20)
  - `type_id: int` (line 21)
  - `fuel_type_id: int` (line 22)
  - `training_date: String` (line 23)
  - `expiration_date: String` (line 24)
- **Methods:**
  - `DriverTraining(int, int, int, int, String, String)` — private Builder constructor (line 27)
- **Imports:** `java.io.Serializable`, `java.util.Date`, `com.journaldev.spring.jdbc.model.Roles.RolesBuilder`, `lombok.Builder`, `lombok.Data`, `lombok.NoArgsConstructor`

### EmailLayout.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/EmailLayout.java`
- **Class:** `EmailLayout implements Serializable` (line 5)
- **Fields:**
  - `serialVersionUID: long` (line 10) — constant: `7681377636404716362L`
  - `id: int` (line 12)
  - `subject: String` (line 13)
  - `message: String` (line 14)
  - `type: String` (line 15)
- **Methods:**
  - `getId(): int` (line 17)
  - `setId(int): void` (line 20)
  - `getSubject(): String` (line 23)
  - `setSubject(String): void` (line 26)
  - `getMessage(): String` (line 29)
  - `setMessage(String): void` (line 32)
  - `getType(): String` (line 35)
  - `setType(String): void` (line 38)
- **Imports:** `java.io.Serializable`

---

## Findings

### A13-1: @EqualsAndHashCode(callSuper = false) excludes parent fields from equality — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/DriverEquipment.java`
**Line(s):** 9-10
**Description:** `DriverEquipment` extends `Equipment` which contains 17 fields including `id`, `name`, `serial_no`, and `mac_address`. The annotation `@EqualsAndHashCode(callSuper = false)` means that `equals()` and `hashCode()` only consider the two subclass fields (`hours` and `trained`), completely ignoring all parent-class identity fields. Two `DriverEquipment` instances with different `id`, `name`, or `serial_no` values but the same `hours`/`trained` will be considered equal. This is almost certainly incorrect behavior for a domain model used in collections and comparisons. Lombok itself generates a warning for this configuration: "Generating equals/hashCode implementation but without a call to superclass... you are advised to set callSuper to true." This should use `callSuper = true` instead.

### A13-2: Unused import — Roles.RolesBuilder in DriverTraining — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java`
**Line(s):** 6
**Description:** `import com.journaldev.spring.jdbc.model.Roles.RolesBuilder` is imported but never referenced anywhere in the `DriverTraining` class. This is likely a copy-paste artifact from another model class. It generates a compiler warning and reduces readability by implying a dependency that does not exist.

### A13-3: Unused import — java.util.Date in DriverTraining — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java`
**Line(s):** 4
**Description:** `import java.util.Date` is imported but never used. The `training_date` and `expiration_date` fields are declared as `String` rather than `Date`. This unused import generates a compiler warning and suggests the developer may have originally intended to use proper date types but switched to `String` without cleaning up.

### A13-4: Date fields stored as String instead of proper date types — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java`
**Line(s):** 23-24
**Description:** `training_date` and `expiration_date` are declared as `String` rather than `java.util.Date`, `java.time.LocalDate`, or another temporal type. Storing dates as strings prevents type-safe date comparisons, date arithmetic, and timezone handling. It shifts parsing and formatting responsibility to every consumer of this class and makes it easy to introduce format inconsistencies. The unused `java.util.Date` import on line 4 suggests the developer originally intended to use proper date typing.

### A13-5: Snake_case field naming violates Java conventions — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java`
**Line(s):** 20-24
**Description:** Fields `manufacture_id`, `type_id`, `fuel_type_id`, `training_date`, and `expiration_date` use snake_case naming, which violates standard Java naming conventions (camelCase). Lombok's `@Data` generates getters/setters based on field names, so the generated methods will be `getManufacture_id()`, `setManufacture_id()`, etc. While `BeanPropertyRowMapper` in Spring JDBC can handle underscore-to-camelCase mapping, the non-standard naming creates confusing API surfaces. This is a project-wide pattern (also seen in `Equipment.java`) but should still be noted as a quality concern.

### A13-6: Formatting defect — class declaration merged with Javadoc comment — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java`
**Line(s):** 14
**Description:** The class declaration and the serialVersionUID Javadoc comment are merged on the same line: `public class DriverTraining implements Serializable {/**`. The opening brace of the class body runs directly into the `/**` Javadoc open tag with no line break. This makes the code harder to read and suggests the file was hastily edited without formatting review.

### A13-7: Style inconsistency — manual getters/setters vs. Lombok in model layer — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/EmailLayout.java`
**Line(s):** 5-40
**Description:** `EmailLayout` uses manually written getter/setter boilerplate (8 methods across lines 17-39), while sibling model classes in the same package (`DriverEquipment`, `DriverTraining`, `Equipment`, `Roles`, `Driver`, etc.) use Lombok's `@Data` annotation to auto-generate these same methods. This inconsistency within the model layer increases maintenance burden and creates divergent patterns for the same concern. The class should use `@Data` to be consistent with the rest of the project.

### A13-8: Excessive trailing blank lines in EmailLayout — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/EmailLayout.java`
**Line(s):** 41-45
**Description:** There are 4 unnecessary blank lines at the end of the class body before the closing brace. While functionally harmless, this is a minor formatting issue that suggests the file was not cleaned up.

### A13-9: EmailLayout has no @Builder or constructor beyond default — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/EmailLayout.java`
**Line(s):** 5-46
**Description:** Unlike `DriverTraining` and `Equipment` which provide a `@Builder` pattern, `EmailLayout` only has the default no-arg constructor and setters. This is consistent with how it is used in `EmailLayoutDAO` (where a new instance is created and presumably populated), but it does represent an inconsistency in construction patterns across model classes. Noted for awareness; the DAO that uses this class (`EmailLayoutDAO.getEmailLayoutByType`) appears to be a stub that returns an empty object and never actually queries the database, so the builder pattern may be premature until the DAO is implemented.

### A13-10: DriverEquipment lacks @Builder despite parent having one — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/DriverEquipment.java`
**Line(s):** 10-15
**Description:** `DriverEquipment` extends `Equipment` which has a `@Builder` constructor, but `DriverEquipment` does not define its own `@Builder`. This means there is no builder that can set both the parent fields (`id`, `name`, etc.) and the subclass fields (`hours`, `trained`) in a single fluent call. Consumers must either use the no-arg constructor with setters or use the parent builder (which cannot set `hours`/`trained`). For a subclass that adds fields, a `@SuperBuilder` annotation on both parent and child would be the idiomatic Lombok approach.
# Pass 4 — Code Quality: A14

## Reading Evidence

### Equipment.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/Equipment.java`
- **Class:** `Equipment implements Serializable` (line 11)
- **Annotations:** `@Data` (line 9), `@NoArgsConstructor` (line 10), `@Builder` on constructor (line 33)
- **Imports:** `lombok.Builder`, `lombok.Data`, `lombok.NoArgsConstructor`, `java.io.Serializable`
- **Fields (lines 12-31):**
  - `serialVersionUID: long` (line 12)
  - `id: int` (line 14)
  - `name: String` (line 15)
  - `type_id: int` (line 16)
  - `comp_id: int` (line 17)
  - `active: boolean` (line 18)
  - `manu_id: int` (line 19)
  - `fuel_type_id: int` (line 20)
  - `attachment_id: int` (line 21)
  - `type: String` (line 22)
  - `manu: String` (line 23)
  - `fuel_type: String` (line 24)
  - `comp: String` (line 25)
  - `serial_no: String` (line 26)
  - `mac_address: String` (line 27)
  - `url: String` (line 28)
  - `impact_threshold: long` (line 29)
  - `alert_enabled: boolean` (line 30)
  - `driver_based: boolean` (line 31)
- **Methods:**
  - `Equipment(...)` all-args constructor (lines 34-56)
- **Lombok-generated (via @Data):** getters, setters, `toString()`, `equals()`, `hashCode()`

### EquipmentType.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/EquipmentType.java`
- **Class:** `EquipmentType implements Serializable` (line 5)
- **Imports:** `java.io.Serializable`
- **Fields:**
  - `serialVersionUID: long` (line 10)
  - `id: int` (line 11)
  - `name: String` (line 12)
  - `icon: String` (line 13)
- **Methods:**
  - `getId(): int` (line 16)
  - `setId(int): void` (line 19)
  - `getName(): String` (line 22)
  - `setName(String): void` (line 25)
  - `getIcon(): String` (line 28)
  - `setIcon(String): void` (line 31)

### ErrorMessage.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/ErrorMessage.java`
- **Class:** `ErrorMessage implements Serializable` (line 10)
- **Annotations:** `@Data` (line 8), `@NoArgsConstructor` (line 9)
- **Imports:** `java.io.Serializable`, `lombok.Data`, `lombok.NoArgsConstructor`
- **Fields:**
  - `serialVersionUID: long` (line 15)
  - `message: String` (line 16)
  - `code: String` (line 17)
  - `detail: String` (line 18)
- **Methods (Lombok-generated via @Data):** getters, setters, `toString()`, `equals()`, `hashCode()`

---

## Findings

### A14-1: EquipmentType class is dead code (never referenced) — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/EquipmentType.java`
**Line(s):** 1-35 (entire file)
**Description:** `EquipmentType` is not imported or referenced anywhere else in the codebase. A project-wide search for "EquipmentType" returns only its own class declaration. This is dead code that increases maintenance burden. It should either be removed or wired into relevant services/DAOs if it was intended to be used. The `Equipment` model already carries a `type` (String) and `type_id` (int) field, suggesting this class may have been an early design artifact that was never integrated.

### A14-2: Inconsistent Lombok usage across model classes — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/EquipmentType.java`
**Line(s):** 5, 16-33
**Description:** `EquipmentType` uses manually written getters and setters, while the sibling models `Equipment` and `ErrorMessage` (and every other model in the package) use Lombok `@Data` to generate them. This is a style inconsistency within the same package. It also means `EquipmentType` lacks `toString()`, `equals()`, and `hashCode()` implementations, which all Lombok `@Data` classes in the package receive automatically. If this class were ever used in collections or logging, the missing `equals`/`hashCode`/`toString` would cause subtle bugs.

### A14-3: Equipment field naming uses snake_case instead of Java camelCase — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Equipment.java`
**Line(s):** 16-17, 19-21, 24, 26-27, 29-31
**Description:** Java convention (and the project's own Lombok-generated accessor convention) requires camelCase for field names. The fields `type_id`, `comp_id`, `manu_id`, `fuel_type_id`, `attachment_id`, `fuel_type`, `serial_no`, `mac_address`, `impact_threshold`, `alert_enabled`, and `driver_based` all use snake_case. With `@Data`, Lombok generates getters/setters like `getType_id()` / `setType_id()` which violate JavaBean naming conventions. This can cause issues with Jackson serialization, Spring data binding, and any framework relying on standard JavaBean property resolution. The proper fix is to rename fields to camelCase (e.g., `typeId`, `compId`, `fuelTypeId`) and use `@JsonProperty` or column-mapping annotations if needed for database/JSON mapping.

### A14-4: Equipment.builder() is never used in the codebase — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Equipment.java`
**Line(s):** 3, 33
**Description:** The `@Builder` annotation is imported and placed on the all-args constructor, but a project-wide search for `Equipment.builder` returns zero matches. The builder pattern was added but is never invoked. While not harmful, it adds unused complexity. This is a minor dead-code concern.

### A14-5: Mixed indentation (spaces vs. tabs) in Equipment.java — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Equipment.java`
**Line(s):** 14-31 vs. 34-56
**Description:** The field declarations (lines 14-31) use 4-space indentation, while the constructor body (lines 34-56) uses tab indentation. This inconsistency suggests different contributors or editor configurations were used. It does not affect compilation but harms readability and causes noisy diffs when auto-formatting is applied.

### A14-6: Empty Javadoc comment in EquipmentType.java — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/EquipmentType.java`
**Line(s):** 7-9
**Description:** There is an empty Javadoc comment block (`/** * */`) above `serialVersionUID`. This is auto-generated boilerplate from Eclipse's "Add generated serial version ID" action. It adds visual noise with no informational value and should be removed.

### A14-7: Primitive int used for ID fields risks default-value ambiguity — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Equipment.java`
**Line(s):** 14, 16-17, 19-21
**Description:** Using primitive `int` for ID and foreign-key fields (`id`, `type_id`, `comp_id`, `manu_id`, `fuel_type_id`, `attachment_id`) means they default to `0` rather than `null`. This makes it impossible to distinguish between "ID not set" and "ID is 0" in validation or persistence logic. Using `Integer` (boxed type) would allow null-checking for unset IDs. The same applies to `EquipmentType.id` (line 11).

### A14-8: ErrorMessage has no parameterized constructor or builder — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/ErrorMessage.java`
**Line(s):** 8-19
**Description:** Unlike `Equipment` and other models in the package which provide `@Builder` and all-args constructors, `ErrorMessage` only has the Lombok-generated no-args constructor. Consumers must create the object and then call setters individually, which prevents immutable-style usage and makes construction less readable. This is a minor design inconsistency -- not a defect, but worth noting for consistency.

### A14-9: Missing space before opening brace in EquipmentType class declaration — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/EquipmentType.java`
**Line(s):** 5
**Description:** The class declaration reads `implements Serializable{` with no space before the opening brace. Standard Java style requires a space: `implements Serializable {`. This is a minor formatting issue.
# Pass 4 — Code Quality: A15

## Reading Evidence

### FormDtl.java
- **Class/Interface:** `FormDtl implements Serializable` (line 5)
- **Fields:**
  - `private static final long serialVersionUID = 1718755713311858420L` (line 10)
  - `private int id` (line 11)
  - `private String input_type` (line 12)
  - `private String input_label` (line 13)
  - `private String input_value` (line 14)
  - `private String input_image` (line 15)
  - `private int input_order` (line 16)
  - `private String expected_answer` (line 17)
- **Methods:**
  - `getId()` — line 20
  - `getInput_type()` — line 23
  - `setInput_type(String)` — line 26
  - `getInput_value()` — line 29
  - `setInput_value(String)` — line 32
  - `setId(int)` — line 35
  - `getInput_label()` — line 38
  - `setInput_label(String)` — line 41
  - `getInput_image()` — line 44
  - `setInput_image(String)` — line 47
  - `getInput_order()` — line 50
  - `setInput_order(int)` — line 53
  - `getExpected_answer()` — line 56
  - `setExpected_answer(String)` — line 59
- **Types/Constants:** `serialVersionUID` (long constant)

### FuelType.java
- **Class/Interface:** `FuelType implements Serializable` (line 5)
- **Fields:**
  - `private static final long serialVersionUID = 8705969780919933138L` (line 10)
  - `private int id` (line 12)
  - `private String name` (line 13)
- **Methods:**
  - `getId()` — line 16
  - `setId(int)` — line 19
  - `getName()` — line 22
  - `setName(String)` — line 25
- **Types/Constants:** `serialVersionUID` (long constant)

### GCMData.java
- **Class/Interface:** `GCMData` (line 3, plain class, no interfaces)
- **Fields:**
  - `protected String to` (line 5)
- **Methods:**
  - `getTo()` — line 7
  - `setTo(String)` — line 11
- **Types/Constants:** None

---

## Findings

### A15-1: Naming convention violation — snake_case field and method names in FormDtl — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java`
**Line(s):** 12-17, 23-61
**Description:** All field names use snake_case (`input_type`, `input_label`, `input_value`, `input_image`, `input_order`, `expected_answer`) and the corresponding getter/setter methods follow the same pattern (e.g., `getInput_type()`, `setInput_value()`). Java convention mandates camelCase for fields and methods (e.g., `inputType`, `getInputType()`). This violates standard Java naming conventions, will trigger warnings in most static analysis tools (Checkstyle, PMD, SonarQube), and complicates JSON serialization where frameworks like Jackson expect camelCase by default. If database column mapping drives the naming, `@Column` annotations or Jackson `@JsonProperty` annotations should be used instead of leaking DB naming into Java code.

### A15-2: Abbreviated and unclear class name — FormDtl — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java`
**Line(s):** 5
**Description:** The class name `FormDtl` uses a non-standard abbreviation for "Detail." Java naming conventions favor full, readable names (e.g., `FormDetail`). This reduces readability and discoverability.

### A15-3: Missing `equals()`, `hashCode()`, and `toString()` — FormDtl — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java`
**Line(s):** 5-63 (entire class)
**Description:** The model class implements `Serializable` but does not override `equals()`, `hashCode()`, or `toString()`. If instances are placed in collections (e.g., `HashSet`, `HashMap`), the default identity-based `equals`/`hashCode` from `Object` will produce incorrect behavior. Missing `toString()` makes debugging and logging opaque.

### A15-4: Missing `equals()`, `hashCode()`, and `toString()` — FuelType — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/FuelType.java`
**Line(s):** 5-30 (entire class)
**Description:** Same issue as A15-3. `FuelType` is a `Serializable` model but lacks `equals()`, `hashCode()`, and `toString()` overrides.

### A15-5: Empty Javadoc comment on serialVersionUID — FormDtl, FuelType — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java`, `src/main/java/com/journaldev/spring/jdbc/model/FuelType.java`
**Line(s):** FormDtl lines 7-9; FuelType lines 7-9
**Description:** Both files contain an auto-generated empty Javadoc block (`/** * */`) above `serialVersionUID`. These serve no documentation purpose and are dead comment noise, likely left by IDE template generation. They should be removed or replaced with meaningful documentation.

### A15-6: GCMData does not implement Serializable — inconsistency with sibling models — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GCMData.java`
**Line(s):** 3
**Description:** Both `FormDtl` and `FuelType` in the same package implement `Serializable`, but `GCMData` does not. If model objects in this package are expected to be serializable (e.g., for session storage, caching, or message passing), this inconsistency could cause a `NotSerializableException` at runtime. If serialization is not needed for `GCMData`, this is purely an INFO-level consistency note.

### A15-7: Field visibility is `protected` instead of `private` in GCMData — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GCMData.java`
**Line(s):** 5
**Description:** The field `to` is declared `protected` rather than `private`. Since the class provides a public getter and setter, the field should be `private` to maintain proper encapsulation. Using `protected` exposes the field to all classes in the same package and to subclasses, bypassing the setter and any validation it might enforce. This is a leaky abstraction unless the class is explicitly designed for inheritance, which is not indicated.

### A15-8: GCMData uses deprecated Google Cloud Messaging terminology — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GCMData.java`
**Line(s):** 3
**Description:** The class name `GCMData` references Google Cloud Messaging (GCM), which was deprecated by Google in April 2018 and shut down in May 2019, fully replaced by Firebase Cloud Messaging (FCM). If the application has migrated to FCM, this class name is misleading. If GCM is still referenced in actual push notification calls elsewhere, this is a more serious concern (see separate audit passes for service layer).

### A15-9: Missing `equals()`, `hashCode()`, and `toString()` — GCMData — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GCMData.java`
**Line(s):** 3-17 (entire class)
**Description:** `GCMData` lacks `equals()`, `hashCode()`, and `toString()` overrides. While this is a simpler model, the absence still hinders debugging and collection usage.

### A15-10: Getter/setter ordering inconsistency in FormDtl — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java`
**Line(s):** 20-61
**Description:** The getter for `id` appears at line 20, but its setter does not appear until line 35. Meanwhile, `input_type`'s getter/setter pair is at lines 23-28, and `input_value`'s pair at lines 29-34. This non-sequential ordering makes the class harder to read and maintain. Getter/setter pairs should be grouped together or fields and accessors should follow a consistent order.

### A15-11: Primitive `int` used for `id` fields — potential null-handling issue — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java`, `src/main/java/com/journaldev/spring/jdbc/model/FuelType.java`
**Line(s):** FormDtl line 11; FuelType line 12
**Description:** The `id` field is declared as primitive `int` (default value 0) rather than `Integer`. If a model instance has not yet been persisted to the database, `id` will silently be 0 instead of `null`, making it impossible to distinguish between "not yet assigned" and "assigned as 0." Using `Integer` would allow null to represent an unset ID.
# Pass 4 — Code Quality: A16

## Reading Evidence

### GCMDataPermission.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/GCMDataPermission.java`
- **Class:** `GCMDataPermission extends GCMData implements Serializable` (line 5)
- **Fields:**
  - `private static final long serialVersionUID = -6506991783027460200L` (line 10)
  - `private Permissions data` (line 12)
- **Methods:**
  - `getData()` — line 14
  - `setData(Permissions data)` — line 18
- **Types/Constants:** References `Permissions`, `GCMData`, `Serializable`
- **Imports:** `java.io.Serializable`

### GCMEntity.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/GCMEntity.java`
- **Class:** `GCMEntity` (line 7)
- **Javadoc:** "Send back message type to the clients via GCM" (lines 3-6)
- **Fields:**
  - `protected String msg_type` (line 8)
- **Methods:**
  - `getMsg_type()` — line 10
  - `setMsg_type(String msg_type)` — line 14
- **Types/Constants:** None beyond `String`
- **Imports:** None

### GCMResponse.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/GCMResponse.java`
- **Class:** `GCMResponse implements Serializable` (line 6)
- **Fields:**
  - `private static final long serialVersionUID = -4626028651245615847L` (line 10)
  - `private String multicast_id` (line 11)
  - `private String success` (line 12)
  - `private String failure` (line 13)
  - `private String canonical_ids` (line 14)
  - `private List<Results> results` (line 15)
- **Methods:**
  - `getMulticast_id()` — line 17
  - `setMulticast_id(String multicast_id)` — line 20
  - `getSuccess()` — line 23
  - `setSuccess(String success)` — line 26
  - `getFailure()` — line 29
  - `setFailure(String failure)` — line 32
  - `getCanonical_ids()` — line 35
  - `setCanonical_ids(String canonical_ids)` — line 38
  - `getResults()` — line 41
  - `setResults(List<Results> results)` — line 44
- **Types/Constants:** References `Results`, `List`, `Serializable`
- **Imports:** `java.io.Serializable`, `java.util.List`

---

## Findings

### A16-1: GCMEntity is completely unused (dead code) — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GCMEntity.java`
**Line(s):** 1-19 (entire file)
**Description:** `GCMEntity` is never imported, extended, or referenced anywhere in the codebase. No other class extends it (confirmed by grep), it does not appear in any XML/YAML/properties configuration, and it is not used via reflection patterns. This is dead code. The Javadoc references "GCM" (Google Cloud Messaging), which was deprecated by Google in April 2018 and shut down in May 2019. The class appears to be a leftover from a legacy push notification implementation that was never cleaned up. Dead code increases maintenance burden and cognitive overhead.

### A16-2: GCMResponse is completely unused (dead code) — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GCMResponse.java`
**Line(s):** 1-52 (entire file)
**Description:** `GCMResponse` is never imported or referenced anywhere else in the codebase. No controller, service, or DAO class uses it. Like `GCMEntity`, this appears to be a remnant of a deprecated Google Cloud Messaging integration. The class models a GCM push notification response structure that is no longer called upon by any active code path.

### A16-3: GCMDataPermission is completely unused (dead code) — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GCMDataPermission.java`
**Line(s):** 1-23 (entire file)
**Description:** `GCMDataPermission` is never imported or referenced anywhere in the codebase outside its own definition. Its parent class `GCMData` is likewise only referenced by `GCMDataPermission` itself. The entire `GCMData`/`GCMDataPermission` inheritance chain is dead code related to the defunct GCM integration.

### A16-4: Non-standard Java naming conventions (snake_case fields and accessors) — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GCMEntity.java`
**Line(s):** 8, 10, 14
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GCMResponse.java`
**Line(s):** 11, 14, 17, 20, 35, 38
**Description:** All three files use `snake_case` for field names and getter/setter method names (e.g., `msg_type`, `getMsg_type()`, `multicast_id`, `getMulticast_id()`, `canonical_ids`, `getCanonical_ids()`). Standard Java convention dictates `camelCase` for fields and methods (e.g., `msgType`, `getMsgType()`). This is likely done to match JSON property names from the GCM API, but the proper approach would be to use `camelCase` in Java with `@JsonProperty` annotations for serialization mapping. This pattern makes the code inconsistent with Java norms and can trigger IDE/linter warnings.

### A16-5: GCMEntity does not implement Serializable despite being a parent-like model — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GCMEntity.java`
**Line(s):** 7
**Description:** `GCMEntity` does not implement `Serializable`, while other model classes in the same package (`GCMDataPermission`, `GCMResponse`, `Permissions`, `Results`) do. If `GCMEntity` were ever used as a base class for a `Serializable` subclass or passed through a serialization boundary, this omission would cause issues. This is an inconsistency within the model package, though the practical impact is muted by the fact that `GCMEntity` is dead code.

### A16-6: GCMData parent class does not implement Serializable, creating inconsistency with Serializable child — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GCMDataPermission.java`
**Line(s):** 5
**Description:** `GCMDataPermission` declares `implements Serializable`, but its parent class `GCMData` does not implement `Serializable`. While Java allows this, it means the `to` field inherited from `GCMData` will be serialized using the default mechanism only if `GCMData` has a no-arg constructor (which it does, implicitly). However, the inherited `to` field will NOT be serialized by the default Java serialization mechanism because `GCMData` itself is not `Serializable` — only the subclass is. During deserialization, the `to` field would be re-initialized via `GCMData`'s no-arg constructor rather than restored from the serialized stream. This is a subtle serialization bug: the `to` field would be `null` after deserialization even if it had a value before serialization.

### A16-7: Mutable List exposed via getter without defensive copy in GCMResponse — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GCMResponse.java`
**Line(s):** 41-42
**Description:** `getResults()` returns the internal `List<Results>` reference directly. Callers can modify the internal state of `GCMResponse` by adding/removing elements from the returned list. For a model/DTO class this is common in practice, but it does represent a leaky abstraction. A defensive copy (`Collections.unmodifiableList(results)` or `new ArrayList<>(results)`) would be more robust.

### A16-8: Empty Javadoc comment block on serialVersionUID — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GCMDataPermission.java`
**Line(s):** 7-9
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GCMResponse.java`
**Line(s):** 7-9
**Description:** Both files contain an auto-generated empty Javadoc comment (`/** * */`) above the `serialVersionUID` field. This is boilerplate noise generated by the IDE and provides no documentation value. It should either be removed or replaced with meaningful documentation.

### A16-9: Excessive trailing blank lines in GCMResponse — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GCMResponse.java`
**Line(s):** 47-51
**Description:** The file has four consecutive blank lines before the closing brace. Standard style guides (Google Java Style, Sun conventions) recommend at most one blank line between members and no excessive trailing whitespace inside a class body. This is a minor style issue.
# Pass 4 — Code Quality: A17

## Reading Evidence

### GPS.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/GPS.java`
- **Class/Interface:** `GPS implements Serializable` (line 5)
- **Fields:**
  - `private static final long serialVersionUID = 6498381626018130193L` (line 10)
  - `private int id` (line 12)
  - `private int unit_id` (line 13)
  - `private Float longitude` (line 14)
  - `private Float latitude` (line 15)
  - `private String gps_time` (line 16)
  - `private boolean current_location` (line 17)
  - `private String unit_name` (line 18)
- **Methods:**
  - `getId()` (line 20)
  - `setId(int)` (line 23)
  - `getUnit_id()` (line 26)
  - `setUnit_id(int)` (line 29)
  - `getLongitude()` (line 32)
  - `setLongitude(Float)` (line 35)
  - `getLatitude()` (line 38)
  - `setLatitude(Float)` (line 41)
  - `getGps_time()` (line 44)
  - `setGps_time(String)` (line 47)
  - `isCurrent_location()` (line 50)
  - `setCurrent_location(boolean)` (line 53)
  - `getUnit_name()` (line 56)
  - `setUnit_name(String)` (line 59)
- **Types/Constants:** `serialVersionUID` constant; boxed `Float` for longitude/latitude; primitive `int` for id/unit_id; `String` for gps_time.

### GPSList.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/GPSList.java`
- **Class/Interface:** `GPSList implements Serializable` (line 7)
- **Fields:**
  - `private static final long serialVersionUID = 3101512981283324426L` (line 9)
  - `List<GPS> gpsList = new ArrayList<GPS>()` (line 12) — package-private access
- **Methods:**
  - `getGpsList()` (line 15)
  - `setGpsList(List<GPS>)` (line 20)
- **Types/Constants:** `serialVersionUID` constant; `List<GPS>` collection.

### Impact.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/Impact.java`
- **Class/Interface:** `Impact implements Serializable` (line 12), annotated with `@Data`, `@NoArgsConstructor`
- **Fields:**
  - `private static final long serialVersionUID = -6059977226530435320L` (line 14)
  - `private long impact_value` (line 16)
  - `private String impact_time` (line 17)
  - `private String mac_address` (line 18)
- **Methods:**
  - `Impact(long, String, String)` — private constructor annotated with `@Builder` (line 20-25)
  - Lombok-generated: `getImpact_value()`, `setImpact_value(long)`, `getImpact_time()`, `setImpact_time(String)`, `getImpact_value()`, `getMac_address()`, `setMac_address(String)`, `equals()`, `hashCode()`, `toString()`, `canEqual()`
- **Types/Constants:** `serialVersionUID` constant; Lombok annotations `@Data`, `@NoArgsConstructor`, `@Builder`.
- **Imports:** `java.util.Date` (line 8) — unused.

---

## Findings

### A17-1: Unused import `java.util.Date` in Impact.java — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Impact.java`
**Line(s):** 8
**Description:** The import `java.util.Date` is declared but never referenced. The `impact_time` field is typed as `String`, not `Date`. This generates a compiler warning and indicates either leftover code from a refactoring or a missed type migration. Should be removed to eliminate the build warning.

### A17-2: Inconsistent style — GPS.java uses manual getters/setters while Impact.java uses Lombok — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GPS.java` (entire file) vs `Impact.java`
**Line(s):** GPS.java lines 5-63; Impact.java lines 10-11
**Description:** `Impact.java` leverages Lombok `@Data` and `@NoArgsConstructor` to auto-generate getters, setters, `equals()`, `hashCode()`, and `toString()`. In contrast, `GPS.java` manually defines all getters and setters and lacks `equals()`, `hashCode()`, and `toString()` entirely. Within the same model package, this creates an inconsistent developer experience. The same inconsistency applies to `GPSList.java`. Newer model classes in this codebase (Driver, Equipment, Company, User, etc.) all use Lombok. `GPS` and `GPSList` should be migrated to Lombok for consistency and to gain the missing `equals`/`hashCode`/`toString` implementations.

### A17-3: GPS.java missing `equals()`, `hashCode()`, and `toString()` — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GPS.java`
**Line(s):** 5-63
**Description:** The `GPS` class implements `Serializable` and is used as a model object returned from REST endpoints and stored in lists, but it does not override `equals()`, `hashCode()`, or `toString()`. This makes debugging harder (no meaningful `toString()` output), and any collection operations that rely on equality semantics (e.g., `contains()`, `Set` usage, deduplication) will use object identity rather than value equality. This is a correctness risk if GPS objects are ever compared or placed into hash-based collections.

### A17-4: GPSList.java missing `equals()`, `hashCode()`, and `toString()` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GPSList.java`
**Line(s):** 7-26
**Description:** Same as A17-3 but for `GPSList`. The class is a thin wrapper around `List<GPS>` and is used as a `@RequestBody` parameter. Missing `equals`/`hashCode`/`toString` makes debugging and testing more difficult.

### A17-5: Field `gpsList` in GPSList.java has package-private access — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GPSList.java`
**Line(s):** 12
**Description:** The field `List<GPS> gpsList` is declared without an access modifier, giving it package-private visibility. While `getGpsList()` and `setGpsList()` provide encapsulated access, the field itself is directly accessible from any class in the same package, which weakens encapsulation. It should be declared `private` to match standard JavaBean conventions and align with how fields are declared in `GPS.java` and `Impact.java`.

### A17-6: Temporal data stored as `String` instead of proper date/time types — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GPS.java` (line 16), `src/main/java/com/journaldev/spring/jdbc/model/Impact.java` (line 17)
**Line(s):** GPS.java:16, Impact.java:17
**Description:** Both `gps_time` in `GPS` and `impact_time` in `Impact` represent temporal values but are typed as `String`. Callers must manually parse these strings via `DateUtil.parseDateTimeIso()` at every usage site (confirmed in `LocationController.java` line 84 and `ImpactDAO.java` lines 43, 54). This is error-prone — any caller that forgets to parse could introduce a bug. Using `java.time.Instant`, `java.time.LocalDateTime`, or even `java.util.Date` with a Jackson deserializer would provide type safety and eliminate repeated manual parsing. The unused `Date` import in `Impact.java` (finding A17-1) suggests this migration was considered but not completed.

### A17-7: Use of boxed `Float` for latitude/longitude risks precision loss — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GPS.java`
**Line(s):** 14-15
**Description:** Latitude and longitude are stored as `Float` (boxed wrapper of 32-bit IEEE 754 float). A 32-bit float provides approximately 7 significant decimal digits of precision, which corresponds to roughly 1.1 meters of positional accuracy at the equator. For many GPS applications this may be marginal. More critically, the downstream code in `LocationController.java` (lines 57, 78) compares these `Float` values using `!=0`, which performs auto-unboxing and floating-point equality comparison — both of which are fragile. If the `Float` is `null` (which is possible since it is a boxed type), `gps.getLatitude()!=0` will throw a `NullPointerException` due to auto-unboxing. Using `Double` (or primitive `double`) would be safer and more precise. If `null` is a valid business state, explicit null checks should be added.

### A17-8: `NullPointerException` risk from auto-unboxing of nullable `Float` fields — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GPS.java`
**Line(s):** 14-15
**Description:** The `longitude` and `latitude` fields are declared as boxed `Float` (nullable). In `LocationController.java` lines 57 and 78, they are compared with `!=0` which triggers auto-unboxing. If a GPS object is deserialized from a JSON payload that omits `latitude` or `longitude` (or sets them to `null`), the boxed `Float` will be `null`, and `gps.getLatitude()!=0` will throw a `NullPointerException`. This is a runtime crash risk on a REST endpoint. Either the fields should be changed to primitive `float` (if null is not a valid state) or null-safe comparison should be used in the controller.

### A17-9: Field naming uses `snake_case` instead of Java `camelCase` convention — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GPS.java` (lines 13, 16-18), `src/main/java/com/journaldev/spring/jdbc/model/Impact.java` (lines 16-18)
**Line(s):** GPS.java:13,16,17,18; Impact.java:16,17,18
**Description:** Fields like `unit_id`, `gps_time`, `current_location`, `unit_name`, `impact_value`, `impact_time`, and `mac_address` use `snake_case` naming, violating standard Java naming conventions (`unitId`, `gpsTime`, `currentLocation`, etc.). This also produces non-standard getter/setter names (e.g., `getUnit_id()`, `getGps_time()`) that do not follow JavaBean conventions. While this pattern is used broadly across the codebase (likely to auto-map database column names via `BeanPropertyRowMapper`), the proper approach would be to use `camelCase` field names with `@JsonProperty` or `@Column` annotations for mapping. This is flagged as LOW because it is a pervasive codebase-wide convention rather than an isolated mistake.

### A17-10: Duplicate `serialVersionUID` value across GPSList and ImpactList — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GPSList.java` (line 9), `src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java` (line 13)
**Line(s):** GPSList.java:9, ImpactList.java:13
**Description:** Both `GPSList` and `ImpactList` share the identical `serialVersionUID` value `3101512981283324426L`. While `serialVersionUID` only needs to be unique within a class hierarchy for serialization compatibility, sharing the exact same value across unrelated classes suggests a copy-paste origin. This is not a functional bug but could cause confusion during debugging of serialization issues and indicates careless code duplication.

### A17-11: Empty Javadoc comment block for `serialVersionUID` — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GPS.java`
**Line(s):** 7-9
**Description:** An empty Javadoc block (`/** */`) precedes the `serialVersionUID` field declaration. This is auto-generated IDE boilerplate that adds no value and should be removed for cleanliness. The same empty comment is present in `ImpactList.java` (which follows the same `GPSList` template).

### A17-12: GPSList is a thin wrapper that could be replaced by typed collection — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/GPSList.java`
**Line(s):** 7-26
**Description:** `GPSList` is a trivial wrapper around `List<GPS>` with only a getter and setter, created solely to work around Java type erasure for JSON deserialization of `@RequestBody List<GPS>`. While functional, modern approaches (e.g., using `TypeReference` in Jackson or directly using `List<GPS>` with Spring's generic type resolution) can eliminate the need for such wrapper classes. The same pattern exists with `ImpactList`. This is purely informational as the wrapper approach works correctly.
# Pass 4 — Code Quality: A18

## Reading Evidence

### ImpactList.java
- **Class/Interface:** `ImpactList implements Serializable` (line 8)
- **Fields:**
  - `serialVersionUID: long` (line 13) — `3101512981283324426L`
  - `impactList: List<Impact>` (line 16) — package-private, initialized to `new ArrayList<Impact>()`
- **Methods:**
  - `getImpactList()` — line 19
  - `setImpactList(List<Impact>)` — line 23
- **Imports:** `java.io.Serializable`, `java.util.ArrayList`, `java.util.List`

### ImpactNotification.java
- **Class/Interface:** `ImpactNotification` (line 9) — annotated with `@Data`, `@NoArgsConstructor`
- **Fields:**
  - `driver_name: String` (line 11)
  - `unit_name: String` (line 12)
  - `manufacturer_name: String` (line 13)
  - `company_name: String` (line 14)
  - `impact_time: String` (line 15)
  - `subscription_name: String` (line 16)
  - `email: String` (line 17)
  - `mobile: String` (line 18)
- **Methods:**
  - Constructor with `@Builder` annotation (line 20-31) — all-args constructor
  - (All getters/setters/equals/hashCode/toString generated by `@Data`)
- **Imports:** `lombok.Builder`, `lombok.Data`, `lombok.NoArgsConstructor`

### Incidents.java
- **Class/Interface:** `Incidents implements Serializable` (line 5)
- **Fields:**
  - `serialVersionUID: long` (line 10) — `-2471804810130016124L`
  - `id: int` (line 12)
  - `signature: byte[]` (line 13)
  - `image: byte[]` (line 14)
  - `injury_type: String` (line 15)
  - `witness: String` (line 16)
  - `location: String` (line 17)
  - `injury: Boolean` (line 18)
  - `near_miss: Boolean` (line 19)
  - `incident: Boolean` (line 20)
  - `driver_id: int` (line 21)
  - `unit_id: int` (line 22)
  - `description: String` (line 43)
  - `report_time: String` (line 44)
  - `event_time: String` (line 45)
  - `job_number: String` (line 46)
- **Methods:**
  - `getDriver_id()` — line 24
  - `setDriver_id(int)` — line 27
  - `getUnit_id()` — line 30
  - `setUnit_id(int)` — line 33
  - `getIncident()` — line 37
  - `setIncident(Boolean)` — line 40
  - `getJob_number()` — line 49
  - `setJob_number(String)` — line 52
  - `getNear_miss()` — line 55
  - `setNear_miss(Boolean)` — line 58
  - `getWitness()` — line 61
  - `setWitness(String)` — line 64
  - `getId()` — line 67
  - `setId(int)` — line 70
  - `getSignature()` — line 73
  - `setSignature(byte[])` — line 76
  - `getImage()` — line 79
  - `setImage(byte[])` — line 82
  - `getInjury_type()` — line 85
  - `setInjury_type(String)` — line 88
  - `getLocation()` — line 91
  - `setLocation(String)` — line 94
  - `getInjury()` — line 97
  - `setInjury(Boolean)` — line 100
  - `getDescription()` — line 103
  - `setDescription(String)` — line 106
  - `getReport_time()` — line 109
  - `setReport_time(String)` — line 112
  - `getEvent_time()` — line 115
  - `setEvent_time(String)` — line 118
- **Imports:** `java.io.Serializable`

---

## Findings

### A18-1: Duplicate serialVersionUID shared with GPSList — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java`
**Line(s):** 13
**Description:** `ImpactList` uses `serialVersionUID = 3101512981283324426L`, which is identical to the value used in `GPSList.java` (line 9). This was likely copy-pasted. While the two classes are unrelated in inheritance and this will not cause a runtime collision under normal Java serialization (the UID is scoped to the class), it is a code smell indicating careless copy-paste and could cause confusion during debugging of serialization issues. Each Serializable class should have its own unique UID.

### A18-2: Package-private field visibility in ImpactList — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java`
**Line(s):** 16
**Description:** The field `List<Impact> impactList` is declared with default (package-private) access instead of `private`. All other model classes in this codebase use `private` for their fields. This allows any class in the same package to bypass the getter/setter and directly access or reassign the list, breaking encapsulation. The field should be declared `private`.

### A18-3: Mutable internal list exposed via getter in ImpactList — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java`
**Line(s):** 19-21
**Description:** `getImpactList()` returns a direct reference to the internal mutable `ArrayList`. Callers can modify the list (add, remove, clear) without going through the owning object. For a simple DTO used in controller deserialization this is functionally acceptable, but it is a leaky abstraction. Returning an unmodifiable view or a defensive copy would be safer.

### A18-4: Style inconsistency — ImpactList uses manual getters/setters while sibling Impact uses Lombok — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java`
**Line(s):** 1-28
**Description:** `ImpactList` manually defines getters and setters and does not use Lombok, while its closely related sibling class `Impact` (which it wraps in a list) uses `@Data` and `@NoArgsConstructor`. `ImpactNotification` in the same package also uses Lombok. This inconsistency increases maintenance burden. `ImpactList` should either use Lombok `@Data` or the decision to not use Lombok should be applied consistently.

### A18-5: ImpactList does not implement equals/hashCode/toString — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java`
**Line(s):** 8-28
**Description:** The class implements `Serializable` and is used as a `@RequestBody` parameter in the controller, but does not override `equals()`, `hashCode()`, or `toString()`. This makes debugging and logging harder and can cause subtle issues if instances are ever compared or placed in collections.

### A18-6: snake_case field naming violates Java naming conventions — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/ImpactNotification.java`
**Line(s):** 11-18
**Description:** All fields use `snake_case` naming (`driver_name`, `unit_name`, `manufacturer_name`, etc.) instead of Java-standard `camelCase`. This is likely done to match database column names directly when used with `BeanPropertyRowMapper`, but it violates Java naming conventions and causes Lombok-generated getters/setters to have non-standard names (e.g., `getDriver_name()`). The proper approach is to use `camelCase` fields with `@Column` annotations or a custom `RowMapper` to handle the mapping. This same issue affects `Incidents.java` (fields on lines 15-16, 18-22, 44-46) and is systemic across the codebase.

### A18-7: ImpactNotification does not implement Serializable — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/ImpactNotification.java`
**Line(s):** 9
**Description:** Unlike `ImpactList`, `Impact`, and `Incidents` which all implement `Serializable`, `ImpactNotification` does not. While this class is only used transiently in the DAO notification flow, the inconsistency means it cannot be cached or transmitted via any mechanism that requires serialization without modification.

### A18-8: Empty Javadoc comments on serialVersionUID — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java`, `src/main/java/com/journaldev/spring/jdbc/model/Incidents.java`
**Line(s):** ImpactList:10-12, Incidents:7-9
**Description:** Both files contain empty Javadoc comment blocks (`/** */`) above the `serialVersionUID` field. These are IDE-generated placeholders that serve no documentation purpose and should either be removed or replaced with meaningful content.

### A18-9: Disorganized field and method ordering in Incidents — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Incidents.java`
**Line(s):** 12-46
**Description:** Field declarations are split into two groups separated by getter/setter methods. Fields `id` through `unit_id` are declared on lines 12-22, then getters/setters for `driver_id`, `unit_id`, and `incident` appear on lines 24-42, followed by more field declarations (`description`, `report_time`, `event_time`, `job_number`) on lines 43-46, and then more getters/setters. This interleaving of fields and methods makes the class difficult to read and maintain. Standard Java convention is to declare all fields first, then all constructors, then all methods.

### A18-10: Mutable byte arrays exposed directly via getters in Incidents — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Incidents.java`
**Line(s):** 73-84
**Description:** The `getSignature()` and `getImage()` methods return direct references to internal `byte[]` arrays, and the setters store the passed references without copying. This means callers can mutate the internal state of the `Incidents` object without going through the setter, which is a well-known defensive-copying violation. For arrays holding security-sensitive data like signatures, this is particularly concerning. The getter should return `Arrays.copyOf(signature, signature.length)` and the setter should store a copy.

### A18-11: Incidents uses Boolean wrapper types for primitive boolean semantics — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Incidents.java`
**Line(s):** 18-20
**Description:** The fields `injury`, `near_miss`, and `incident` are declared as `Boolean` (wrapper type) rather than `boolean` (primitive). This introduces the possibility of `NullPointerException` when the fields are used in boolean expressions without null-checking. If the database column is non-nullable, primitive `boolean` would be safer. If nullable semantics are intended, this should be documented and callers must perform null-checks.

### A18-12: Inconsistent indentation in Incidents field declarations — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Incidents.java`
**Line(s):** 15-22
**Description:** Some fields use tab indentation (e.g., `signature` on line 13, `image` on line 14) while others use space indentation (e.g., `injury_type` on line 15, `witness` on line 16). Additionally, line 36 uses inconsistent leading whitespace compared to surrounding methods. This mixed indentation style can cause diff noise and merge conflicts.

### A18-13: Incidents class named as plural — suggests entity/table naming leak — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Incidents.java`
**Line(s):** 5
**Description:** The class is named `Incidents` (plural) but represents a single incident record (the controller parameter is `@RequestBody Incidents incident`). Java class naming convention for entity/model classes is singular (e.g., `Incident`). The plural name likely leaked from the database table name `incidents`. This is also true for other model classes in the project (e.g., `Answers`, `Charts`), so it is a systemic convention choice, but it conflicts with standard Java naming.

### A18-14: Incidents class should use Lombok to reduce boilerplate — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Incidents.java`
**Line(s):** 5-122
**Description:** The `Incidents` class has 16 fields and 32 manual getter/setter methods spanning 122 lines. The sibling classes `Impact` and `ImpactNotification` in the same package use Lombok `@Data` to eliminate this boilerplate. Using Lombok here would reduce the class to approximately 25 lines and eliminate the risk of getter/setter implementation bugs.

### A18-15: Incidents.signature and Incidents.image fields are not used in controller insert — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Incidents.java`
**Line(s):** 13-14
**Description:** The `signature` and `image` fields (both `byte[]`) are defined in the `Incidents` model class, but the `saveIncident` method in `ImpactController.java` (line 67-68) does not include them in the INSERT statement. These fields appear to be handled separately via a multipart file upload endpoint (commented code at line 73-79 of the controller). The fields in the model class may be vestigial or exist for a read path not evident in this controller. This is not necessarily dead code, but it is worth verifying that these fields are actually used somewhere in the codebase.
# Pass 4 — Code Quality: A19

## Reading Evidence

### Manufacturer.java
- **Class/Interface:** `Manufacturer implements Serializable` (line 5)
- **Fields:**
  - `private static final long serialVersionUID = 9130860210979786961L` (line 10)
  - `private int id` (line 12)
  - `private String name` (line 26)
- **Methods:**
  - `getId()` — line 14
  - `setId(int id)` — line 17
  - `getName()` — line 20
  - `setName(String name)` — line 23
- **Types/Constants:** `serialVersionUID` (long)
- **Imports:** `java.io.Serializable`

### OfflineSessions.java
- **Class/Interface:** `OfflineSessions implements Serializable` (line 5)
- **Fields:**
  - `private static final long serialVersionUID = -8930449759197168463L` (line 10)
  - `private Sessions sessions` (line 11)
  - `private Result results` (line 12)
- **Methods:**
  - `getSessions()` — line 14
  - `setSessions(Sessions sessions)` — line 17
  - `getResults()` — line 20
  - `setResults(Result results)` — line 23
- **Types/Constants:** `serialVersionUID` (long); references `Sessions`, `Result`
- **Imports:** `java.io.Serializable`

### PackageEntry.java
- **Class/Interface:** `PackageEntry implements Comparable<PackageEntry>` (line 15)
- **Annotations:** `@Data`, `@NoArgsConstructor` (lines 13-14)
- **Fields:**
  - `private String name` (line 17)
  - `private String fileName` (line 18)
  - `private String url` (line 19)
  - `private int major` (line 20)
  - `private int minor` (line 21)
  - `private int patch` (line 22)
  - `private String env` (line 23)
  - `@JsonIgnore private Pattern pattern` (lines 25-26)
- **Methods:**
  - Constructor `PackageEntry(String fileName, String name, String version, String baseUrl)` (annotated `@Builder`) — line 29
  - `initVersion(String version)` — line 36
  - `compareTo(PackageEntry o)` — line 57
- **Types/Constants:** `Pattern` (compiled regex)
- **Imports:** `com.fasterxml.jackson.annotation.JsonIgnore`, `lombok.Builder`, `lombok.Data`, `lombok.NoArgsConstructor`, `org.apache.commons.lang3.StringUtils`, `org.apache.commons.lang3.builder.CompareToBuilder`, `java.util.regex.Matcher`, `java.util.regex.Pattern`

---

## Findings

### A19-1: Field declared after its getter/setter methods — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Manufacturer.java`
**Line(s):** 26 (field `name`), 20-25 (getter/setter for `name`)
**Description:** The field `name` is declared at line 26, after its getter `getName()` (line 20) and setter `setName()` (line 23). Standard Java convention places field declarations at the top of the class before any methods. This harms readability and violates the structural ordering convention followed by the `id` field in the same class. All fields should be grouped together before methods.

### A19-2: Missing equals/hashCode/toString on Manufacturer — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Manufacturer.java`
**Line(s):** 5-28
**Description:** `Manufacturer` is a `Serializable` model class with `id` and `name` fields but does not override `equals()`, `hashCode()`, or `toString()`. If instances are ever placed in collections, compared for equality, or logged, default `Object` identity semantics will apply, which is rarely the intended behavior for a data model. Other model classes in this codebase (e.g., `PackageEntry`) use Lombok `@Data` to generate these; this class uses manual getters/setters with no such override.

### A19-3: Missing equals/hashCode/toString on OfflineSessions — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/OfflineSessions.java`
**Line(s):** 5-30
**Description:** Same as A19-2. `OfflineSessions` implements `Serializable` and contains two domain object fields (`Sessions`, `Result`) but does not override `equals()`, `hashCode()`, or `toString()`. This is inconsistent with the Lombok-based approach used in `PackageEntry` within the same package.

### A19-4: Empty Javadoc block on serialVersionUID — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Manufacturer.java`
**Line(s):** 7-9
**Description:** The Javadoc comment block `/** * */` above `serialVersionUID` is empty and provides no documentation value. This appears to be an IDE-generated placeholder. The same pattern appears in `OfflineSessions.java` (lines 7-9). These should either be removed or filled with meaningful content.

### A19-5: Inconsistent coding style across model package — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Manufacturer.java`, `OfflineSessions.java`, `PackageEntry.java`
**Line(s):** All files
**Description:** The model package has a significant style inconsistency: `PackageEntry` uses Lombok annotations (`@Data`, `@NoArgsConstructor`, `@Builder`) and 4-space indentation, while `Manufacturer` and `OfflineSessions` use hand-written getters/setters and tab indentation. This mixed approach within the same package creates maintenance overhead, makes it harder for developers to know which pattern to follow, and produces inconsistent JSON serialization behavior (Lombok `@Data` generates `equals`/`hashCode`/`toString`; the manual classes do not).

### A19-6: Missing space before opening brace in class declaration — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/OfflineSessions.java`
**Line(s):** 5
**Description:** The class declaration `public class OfflineSessions implements Serializable{` is missing a space before the opening brace `{`. Standard Java formatting convention requires a space: `Serializable {`. This is a minor style issue but would be flagged by common linters (Checkstyle, etc.).

### A19-7: Trailing blank lines in OfflineSessions — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/OfflineSessions.java`
**Line(s):** 27-29
**Description:** There are three unnecessary blank lines at the end of the class body (lines 27-29) before the closing brace. This is a minor style issue that adds visual noise.

### A19-8: Non-static mutable Pattern field in PackageEntry — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java`
**Line(s):** 25-26
**Description:** The `Pattern` object is compiled as an instance field on every `PackageEntry` object. Since the regex `"(\\d*)\\.?(\\d*)?\\.?(\\d*)?\\-(\\w*)"` is a constant, the compiled `Pattern` should be a `private static final` field to avoid recompilation on every instantiation and reduce memory overhead. Additionally, because `@Data` (Lombok) generates `equals()`, `hashCode()`, and `toString()` for all non-static fields, this `Pattern` field will be included in those methods despite the `@JsonIgnore` annotation (which only affects Jackson serialization). This could cause unexpected behavior in equality checks and hash-based collections. The `@JsonIgnore` prevents serialization but does not exclude it from Lombok-generated methods; `@EqualsAndHashCode.Exclude` and `@ToString.Exclude` or making the field `static` would be needed.

### A19-9: No null-safety on initVersion parameter — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java`
**Line(s):** 36-54
**Description:** The `initVersion(String version)` method passes `version` directly to `pattern.matcher(version)` at line 38 without a null check. If the `@Builder`-constructed `PackageEntry` receives a `null` version, a `NullPointerException` will be thrown. While the builder caller is expected to provide a valid version, there is no defensive check or documented precondition. The `url` field at line 33 would also embed the literal string `"null"` via `String.format` if version is null.

### A19-10: Regex allows empty capture groups leading to NumberFormatException — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java`
**Line(s):** 26, 40
**Description:** The regex pattern `(\\d*)\\.?(\\d*)?\\.?(\\d*)?\\-(\\w*)` uses `\\d*` (zero or more digits) for the first capture group. If the first group matches zero digits (an empty string), `Integer.parseInt(matcher.group(1))` at line 40 will throw a `NumberFormatException`. Unlike groups 2 and 3 which are guarded by `StringUtils.isNotBlank()` checks, group 1 is parsed unconditionally. A version string like `-dev` would match the pattern (empty first group, empty second/third groups, "dev" as fourth group) and crash at line 40. The regex should use `\\d+` for the mandatory major version group, or a blank check should be added before parsing.

### A19-11: compareTo inconsistent with equals — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java`
**Line(s):** 57-68
**Description:** The `compareTo` method compares only `major`, `minor`, and `patch` fields, but Lombok's `@Data` annotation generates `equals()` using all fields (including `name`, `fileName`, `url`, `env`, and the `Pattern` instance). This violates the `Comparable` contract which strongly recommends that `compareTo` be consistent with `equals` (i.e., `compareTo(x) == 0` should imply `x.equals(y)`). Two `PackageEntry` objects with the same version numbers but different names/URLs would be considered equal by `compareTo` but not by `equals`, potentially causing unexpected behavior in sorted collections like `TreeSet`.
# Pass 4 — Code Quality: A20

## Reading Evidence

### Permissions.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/Permissions.java`
- **Class:** `Permissions implements Serializable` (lines 13-39)
- **Annotations:** `@Data`, `@NoArgsConstructor`, `@EqualsAndHashCode(onlyExplicitlyIncluded = true)` (lines 10-12)
- **Constants:** `serialVersionUID = 1871252602934566751L` (line 15)
- **Fields:**
  - `Long id` (line 17)
  - `Long driver_id` with `@EqualsAndHashCode.Include` (lines 19-20)
  - `String driver_name` (line 22)
  - `Long comp_id` with `@EqualsAndHashCode.Include` (lines 24-25)
  - `String enabled` (line 27)
  - `String gsm_token` (line 28)
- **Methods:**
  - `Permissions(Long, Long, String, Long, String, String)` — `@Builder` constructor (lines 30-38)
  - All getters/setters generated by `@Data`

### Questions.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/Questions.java`
- **Class:** `Questions implements Serializable` (lines 5-37)
- **Constants:** `serialVersionUID = 1443419827915092612L` (line 10)
- **Fields:**
  - `int id` (line 12)
  - `String content` (line 13)
  - `String expectedanswer` (line 14)
- **Methods:**
  - `getId()` — line 17
  - `setId(int)` — line 20
  - `getContent()` — line 23
  - `setContent(String)` — line 26
  - `getExpectedanswer()` — line 29
  - `setExpectedanswer(String)` — line 32

### ReportLists.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java`
- **Class:** `ReportLists implements Serializable` (lines 5-51)
- **Constants:** `serialVersionUID = 583659787962286000L` (line 11)
- **Fields:**
  - `int id` (line 13)
  - `String name` (line 14)
  - `String file_name` (line 15)
  - `String frequency` (line 16)
  - `int comp_id` (line 17)
- **Methods:**
  - `getComp_id()` — line 19
  - `setComp_id(int)` — line 22
  - `getFrequency()` — line 25
  - `setFrequency(String)` — line 28
  - `getFile_name()` — line 31
  - `setFile_name(String)` — line 34
  - `getId()` — line 37
  - `setId(int)` — line 40
  - `getName()` — line 43
  - `setName(String)` — line 46
- **Comment:** `// subscription table` (line 10)

---

## Findings

### A20-1: `enabled` field type mismatch with database schema — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Permissions.java`
**Line(s):** 27
**Description:** The `enabled` field is declared as `String`, but the database schema (`V1__create_baseline_schema.sql`, line 1499) defines `permission.enabled` as `boolean DEFAULT false`. All SQL queries in the codebase use `p.enabled IS TRUE` or `p.enabled = true`, confirming the column is boolean. In `CompanyDAO.java` (line 179), it is read via `rs.getString("permission_enable")`, which works but is a lossy representation that forces consumers to do string comparison (`"true"` / `"false"`) instead of a proper boolean check. This should be `boolean` (or `Boolean`) for type safety and clarity.

### A20-2: Inconsistent Lombok usage — `Questions` and `ReportLists` use manual boilerplate while `Permissions` uses `@Data` — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Questions.java`, `src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java`
**Line(s):** Questions 17-34, ReportLists 19-47
**Description:** The project has a clear pattern (visible in `Permissions.java`, `Driver.java`, `Company.java`) of using Lombok `@Data` to generate getters, setters, `toString`, `equals`, and `hashCode`. However, `Questions` and `ReportLists` both use hand-written getters and setters and have no Lombok annotations at all. This creates maintenance burden and inconsistency within the model package. Both classes are also missing `toString()`, `equals()`, and `hashCode()` implementations entirely.

### A20-3: Missing `equals()` and `hashCode()` in `Questions` and `ReportLists` — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Questions.java`, `src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java`
**Line(s):** Questions 5, ReportLists 5
**Description:** Both classes implement `Serializable` and are used in `List` collections (e.g., `List<Questions>` in `SessionController.java`, `List<ReportLists>` in `ResumeController.java`), but neither overrides `equals()` or `hashCode()`. This means they rely on `Object`'s identity-based defaults. If these objects are ever placed in a `Set`, used as `Map` keys, or compared with `.equals()`, behavior will be incorrect. The Lombok-annotated models (e.g., `Permissions` with `@Data`) do not have this problem.

### A20-4: `Questions` uses primitive `int` for `id` field — cannot represent null — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Questions.java`
**Line(s):** 12
**Description:** The `id` field is declared as `int` (primitive). In the database, `question.id` is an auto-generated integer. When `BeanPropertyRowMapper` maps a row, a null database value for `id` would default to 0, which is a valid but ambiguous value. The project convention (visible in `Permissions.java` and `Driver.java`) is to use `Long` for ID fields. Using `Integer` or `Long` here would be more consistent and null-safe.

### A20-5: `ReportLists` uses primitive `int` for `id` and `comp_id` — cannot represent null — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java`
**Line(s):** 13, 17
**Description:** Same issue as A20-4. Both `id` and `comp_id` are declared as primitive `int`, while the project convention for similar model classes (`Permissions`, `Driver`, `Company`) is to use boxed `Long` or `Integer`. Primitive types silently default to 0 on null, which can mask data issues. Additionally, the SQL query in `ResumeController` (line 267) does not select `comp_id`, so when `BeanPropertyRowMapper` instantiates `ReportLists`, `comp_id` will always be 0, which may be misleading.

### A20-6: snake_case field names violate Java naming conventions — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Permissions.java`, `src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java`
**Line(s):** Permissions: 20, 25, 28; ReportLists: 15, 17
**Description:** Fields like `driver_id`, `comp_id`, `gsm_token`, `driver_name` (in Permissions) and `file_name`, `comp_id` (in ReportLists) use snake_case, which violates standard Java naming conventions (camelCase). While this matches database column names and works with `BeanPropertyRowMapper` (which is case-insensitive and strips underscores), it produces non-standard getter names like `getDriver_id()` and `getComp_id()`. The project is split on this: `Company.java` uses camelCase (`dateFormat`, `maxSessionLength`) while `Driver.java` and `Permissions.java` use snake_case. This is a project-wide inconsistency, but should be documented and ideally standardized.

### A20-7: Empty Javadoc comment block — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Questions.java`, `src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java`
**Line(s):** Questions 7-9, ReportLists 7-9
**Description:** Both files contain an empty Javadoc comment block (`/** */`) above `serialVersionUID`, which appears to be auto-generated IDE boilerplate. This adds no value and should be removed for cleanliness.

### A20-8: Misleading class name `ReportLists` maps to `subscription` table — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java`
**Line(s):** 5, 10
**Description:** The class is named `ReportLists` but the comment on line 10 says `// subscription table` and queries in `ResumeController.java` (line 268) show it maps to the `subscription` table. The class name is also grammatically unusual (plural "Lists"). A name like `Subscription` or `ReportSubscription` would more accurately reflect the domain model. The existing name is a leaky abstraction that obscures the actual data source.

### A20-9: `ReportLists` missing `toString()` — hampers debugging — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java`
**Line(s):** 5-51
**Description:** No `toString()` method is defined. When `ReportLists` instances appear in logs (as they do in `ResumeController`), only the default `Object.toString()` (class name + hash) is shown, providing no useful information for debugging. The same applies to `Questions`.

### A20-10: `Permissions.driver_name` is a derived/computed field not backed by a database column — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Permissions.java`
**Line(s):** 22
**Description:** The `driver_name` field does not exist in the `permission` database table. In `CompanyDAO.java` (line 177), it is populated by concatenating `first_name` and `last_name` from a joined query: `.driver_name(rs.getString("first_name") + " " + rs.getString("last_name"))`. This is a computed/derived field living in a model that otherwise represents the `permission` table. While functional, this blurs the boundary between the entity and a DTO/view-model. If this class is ever used for writes or in other contexts, the `driver_name` field would be null or stale.

### A20-11: Missing space before opening brace in class declaration — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java`
**Line(s):** 5
**Description:** The class declaration reads `public class ReportLists implements Serializable{` (no space before `{`). Standard Java style requires a space before the opening brace: `Serializable {`. This is a minor formatting inconsistency compared to the other model files which have the correct spacing.
# Pass 4 — Code Quality: A21

## Reading Evidence

### Reports.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/Reports.java`
- **Class:** `Reports implements Serializable` (line 5)
- **Constants:** `serialVersionUID = -328199895252518312L` (line 10)
- **Fields:**
  - `private String field` (line 12)
  - `private String object` (line 13)
  - `private String value` (line 14)
- **Methods:**
  - `getField()` — line 16
  - `setField(String)` — line 19
  - `getObject()` — line 22
  - `setObject(String)` — line 25
  - `getValue()` — line 28
  - `setValue(String)` — line 31

### ResponseWrapper.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/ResponseWrapper.java`
- **Class:** `ResponseWrapper implements Serializable` (line 13), annotated with `@Data`, `@NoArgsConstructor`, `@JsonInclude(JsonInclude.Include.NON_NULL)`
- **Constants:** `serialVersionUID = 3136054157198689395L` (line 16)
- **Fields:**
  - `private Object data` (line 18)
  - `private Object metadata` (line 19)
  - `private List<ErrorMessage> errors` (line 20)
- **Methods:** Generated by Lombok `@Data` (getters, setters, toString, equals, hashCode)
- **Imports:** `java.io.Serializable`, `java.util.List`, `com.fasterxml.jackson.annotation.JsonInclude`, `lombok.Data`, `lombok.NoArgsConstructor`

### Result.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/Result.java`
- **Class:** `Result implements Serializable` (line 6)
- **Constants:** `serialVersionUID = -631947915399380621L` (line 11)
- **Fields:**
  - `private int id` (line 13)
  - `private String comment` (line 14)
  - `private String start_time` (line 15)
  - `private String finish_time` (line 16)
  - `private int session_id` (line 17)
  - `private ArrayList<Answers> arrAnswers = new ArrayList<Answers>()` (line 18)
- **Methods:**
  - `getId()` — line 19
  - `setId(int)` — line 22
  - `getComment()` — line 26
  - `setComment(String)` — line 29
  - `getStart_time()` — line 32
  - `setStart_time(String)` — line 35
  - `getFinish_time()` — line 38
  - `setFinish_time(String)` — line 41
  - `getSession_id()` — line 44
  - `setSession_id(int)` — line 47
  - `getArrAnswers()` — line 50
  - `setArrAnswers(ArrayList<Answers>)` — line 53
- **Imports:** `java.io.Serializable`, `java.util.ArrayList`

---

## Findings

### A21-1: Inconsistent use of Lombok across model classes — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Reports.java`, `src/main/java/com/journaldev/spring/jdbc/model/Result.java`
**Line(s):** Reports.java:5-36, Result.java:6-58
**Description:** The codebase uses Lombok `@Data` on many model classes (e.g., `ResponseWrapper`, `AuthenticationResponse`, `Driver`, `Company`, `Equipment`, `ErrorMessage`, and at least 15 others), but `Reports` and `Result` use manually written getters and setters. This inconsistency increases maintenance burden, makes the codebase harder to reason about, and increases the likelihood of bugs when fields are added but getters/setters are forgotten. Both classes should adopt `@Data` and `@NoArgsConstructor` to match the project convention.

### A21-2: `ResponseWrapper` uses `Object` type for `data` and `metadata` fields — erasing type safety — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/ResponseWrapper.java`
**Line(s):** 18-19
**Description:** The fields `data` and `metadata` are declared as `Object`, which completely erases type information. This is a leaky abstraction: consumers must cast the returned data, which bypasses compile-time type checking and can cause `ClassCastException` at runtime. A generic type parameter (e.g., `ResponseWrapper<T>`) for at least the `data` field would provide type safety. Notably, the codebase also never calls `setData()` or `getData()` in any file searched, raising the question of whether these fields are actively used or are dead code on `ResponseWrapper` itself (the subclass `AuthenticationResponse` adds its own typed fields instead).

### A21-3: `ResponseWrapper` class declaration has malformed Javadoc comment on same line — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/ResponseWrapper.java`
**Line(s):** 13-15
**Description:** The class declaration and Javadoc open on the same line: `public class ResponseWrapper implements Serializable {/**`. The empty Javadoc block (`/** */`) is merged directly onto the class opening brace line, then the serialVersionUID follows. This is a formatting defect — the Javadoc is syntactically attached to `serialVersionUID` rather than the class, and the brace-Javadoc collision is confusing. The Javadoc block should either be removed (since it is empty) or moved above the class declaration with proper formatting.

### A21-4: Java naming convention violation — snake_case field names in `Result` — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Result.java`
**Line(s):** 15-17, 32-48
**Description:** Fields `start_time`, `finish_time`, and `session_id` use snake_case, which violates the Java naming convention (camelCase). The corresponding getter/setter methods (`getStart_time()`, `setStart_time()`, `getFinish_time()`, `setFinish_time()`, `getSession_id()`, `setSession_id()`) also follow snake_case, producing non-standard method names. This is a widespread pattern in the codebase (also seen in `Results.java`, `ReportLists.java`), but it generates non-idiomatic JSON keys and can cause issues with Jackson's default property naming strategy. If the database columns use snake_case, use `@JsonProperty` annotations to map between conventions rather than encoding database naming into Java field names.

### A21-5: Concrete `ArrayList` used in field declaration and method signatures instead of `List` interface — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Result.java`
**Line(s):** 18, 50, 53
**Description:** The field `arrAnswers` is declared as `ArrayList<Answers>` and the getter/setter use `ArrayList<Answers>` rather than the `List<Answers>` interface. Programming to the implementation rather than the interface couples callers to `ArrayList` unnecessarily. The field type, getter return type, and setter parameter type should all use `List<Answers>`. The diamond operator (`new ArrayList<>()`) should also be used instead of `new ArrayList<Answers>()` to reduce redundancy (Java 7+).

### A21-6: `Reports` and `Result` lack `toString()`, `equals()`, and `hashCode()` implementations — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Reports.java`, `src/main/java/com/journaldev/spring/jdbc/model/Result.java`
**Line(s):** Reports.java:5-36, Result.java:6-58
**Description:** Neither `Reports` nor `Result` override `toString()`, `equals()`, or `hashCode()`. This means they inherit `Object`'s identity-based implementations, which makes debugging harder (no meaningful string representation) and prevents correct behavior in collections that rely on value equality (e.g., `HashSet`, `HashMap`). The Lombok-annotated classes in this project get these methods automatically via `@Data`. These two classes should either adopt Lombok or add explicit implementations.

### A21-7: Empty Javadoc blocks on `serialVersionUID` in all three files — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Reports.java`, `src/main/java/com/journaldev/spring/jdbc/model/ResponseWrapper.java`, `src/main/java/com/journaldev/spring/jdbc/model/Result.java`
**Line(s):** Reports.java:7-9, ResponseWrapper.java:13-15, Result.java:8-10
**Description:** All three files contain an empty Javadoc block (`/** */`) above the `serialVersionUID` field. These appear to be IDE-generated placeholder comments that were never filled in. They add no value and should be removed to reduce noise.

### A21-8: Class name `Reports` uses plural form for a single-instance model object — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Reports.java`
**Line(s):** 5
**Description:** The class `Reports` represents a single report entry with fields `field`, `object`, and `value`. However, the plural name `Reports` suggests a collection. Usage in `ResumeController.java` confirms individual instances are created (e.g., `Reports failedreport = new Reports()`). A more accurate name would be `Report` or `ReportEntry`. This is consistent with a broader naming issue in the codebase (`Results`, `Answers`, `Incidents` are also pluralized for single-entity models), but it hinders readability.

### A21-9: `ResponseWrapper.data` and `metadata` fields may be dead code on the base class — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/ResponseWrapper.java`
**Line(s):** 18-19
**Description:** A search across the entire `src` directory for calls to `setData()`, `getData()`, `setMetadata()`, or `getMetadata()` returned zero results. The only subclass `AuthenticationResponse` defines its own typed fields (`accessToken`, `sessionToken`, `userData`, etc.) rather than using the inherited `data`/`metadata` fields. This suggests the `data` and `metadata` fields on `ResponseWrapper` are dead code — defined but never populated or read. If confirmed, they should be removed to avoid confusion.

### A21-10: Generic field names in `Reports` class reduce self-documentation — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Reports.java`
**Line(s):** 12-14
**Description:** The field names `field`, `object`, and `value` are extremely generic and do not convey domain meaning. In particular, `object` shadows the concept of `java.lang.Object`, which can be confusing in code review and IDE autocompletion. More descriptive names (e.g., `reportField`, `entityName`, `reportValue` or domain-specific terms) would improve readability and maintainability.
# Pass 4 — Code Quality: A22

## Reading Evidence

### Results.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/Results.java`
- **Class/Interface:** `Results implements Serializable` (line 6)
- **Fields:**
  - `private static final long serialVersionUID = 1460020432004206866L` (line 12)
  - `private String message_id` (line 13)
  - `private String error` (line 14)
- **Methods:**
  - `getMessage_id()` — line 16
  - `setMessage_id(String)` — line 19
  - `getError()` — line 23
  - `setError(String)` — line 27
- **Types/Constants:** serialVersionUID
- **Comment:** Line 5 — `//for the web service return return` (typo: duplicated "return")

### Roles.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/Roles.java`
- **Class/Interface:** `Roles implements Serializable` with `@Data`, `@NoArgsConstructor` (lines 9-11)
- **Fields:**
  - `private static final long serialVersionUID = 3861900430744018177L` (line 16)
  - `private Long id` (line 18)
  - `private String name` (line 19)
  - `private String authority` (line 20)
  - `private String description` (line 21)
- **Methods:**
  - `Roles(Long, String, String, String)` — `@Builder` constructor (line 24)
- **Inner enum:** `RoleId` (line 31)
  - Constant: `ROLE_COMPANY_GROUP("ROLE_COMPANY_GROUP")` (line 32)
  - Field: `private String id` (line 34)
  - Methods: `RoleId(String)` constructor (line 36), `getId()` (line 40), `fromId(String)` (line 44)
- **Types/Constants:** serialVersionUID, RoleId enum

### Services.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/Services.java`
- **Class/Interface:** `Services implements Serializable` (line 6)
- **Fields:**
  - `private static final long serialVersionUID = -1720582328491174646L` (line 11)
  - `private int unit_id` (line 13)
  - `private String unit_name` (line 14)
  - `private String service_type` (line 15)
  - `private BigDecimal acc_hours` (line 16)
  - `private BigDecimal service_due` (line 17)
  - `private int last_serv` (line 18)
  - `private int next_serv` (line 19)
  - `private int serv_duration` (line 20)
  - `private int driver_id` (line 21)
- **Methods:**
  - `getDriver_id()` — line 23, `setDriver_id(int)` — line 26
  - `getAcc_hours()` — line 29, `setAcc_hours(BigDecimal)` — line 32
  - `getService_due()` — line 35, `setService_due(BigDecimal)` — line 38
  - `getUnit_id()` — line 41, `setUnit_id(int)` — line 44
  - `getLast_serv()` — line 47, `setLast_serv(int)` — line 50
  - `getNext_serv()` — line 53, `setNext_serv(int)` — line 56
  - `getServ_duration()` — line 59, `setServ_duration(int)` — line 62
  - `getService_type()` — line 65, `setService_type(String)` — line 68
  - `getUnit_name()` — line 71, `setUnit_name(String)` — line 74
- **Types/Constants:** serialVersionUID

---

## Findings

### A22-1: Inconsistent Lombok usage across model classes — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Results.java`, `src/main/java/com/journaldev/spring/jdbc/model/Services.java`
**Line(s):** Results.java:6, Services.java:6
**Description:** The `Roles` class uses Lombok annotations (`@Data`, `@NoArgsConstructor`, `@Builder`) to auto-generate getters, setters, `equals`, `hashCode`, and `toString`. However, `Results` and `Services` in the same package use manually written getter/setter boilerplate without Lombok. 16 out of 43 model classes in this package use Lombok while the rest do not. This inconsistency makes the codebase harder to maintain: developers must mentally track which pattern applies to which class. Additionally, the manual classes lack `equals()`, `hashCode()`, and `toString()` implementations that `@Data` would provide, causing inconsistent behavior when objects are logged, compared, or placed into collections.

### A22-2: Non-camelCase field and method naming convention — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Results.java`, `src/main/java/com/journaldev/spring/jdbc/model/Services.java`
**Line(s):** Results.java:13,16,19; Services.java:13-21,23-76
**Description:** Fields and methods use `snake_case` naming (e.g., `message_id`, `getMessage_id()`, `unit_id`, `getUnit_id()`, `acc_hours`, `service_due`, `last_serv`, `next_serv`, `serv_duration`, `driver_id`). This violates the standard Java naming convention of camelCase for fields and methods. It also breaks JavaBeans conventions, because `BeanPropertyRowMapper` (used in `EquipmentController.java` line 137 to populate `Services`) maps based on column-to-property name translation and will work correctly with underscore-separated names, but the non-standard naming can confuse developers and static analysis tools. Standard Java convention would use `messageId`, `getMessageId()`, `unitId`, `getUnitId()`, etc.

### A22-3: Typo in class-level comment — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Results.java`
**Line(s):** 5
**Description:** The comment reads `//for the web service return return` with the word "return" duplicated. This is a minor copy-paste typo. The comment also lacks proper Javadoc format and provides minimal value.

### A22-4: Missing `equals()`, `hashCode()`, and `toString()` in Results and Services — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Results.java`, `src/main/java/com/journaldev/spring/jdbc/model/Services.java`
**Line(s):** Results.java:6, Services.java:6
**Description:** Both `Results` and `Services` implement `Serializable` and are used as data transfer objects but lack `equals()`, `hashCode()`, and `toString()` overrides. `Results` is used as a REST response body in at least 8 controller classes (SessionController, EquipmentController, CompanyController, ImpactController, LocationController, DriverController, ResumeController). Without `toString()`, logging these objects will produce unhelpful default output (e.g., `Results@3a1b2c4d`). Without `equals()` and `hashCode()`, objects cannot be reliably compared or stored in hash-based collections. The sibling class `Roles` already has these via `@Data`.

### A22-5: Missing space before opening brace in class declaration — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Services.java`
**Line(s):** 6
**Description:** The class declaration `public class Services implements Serializable{` is missing a space before the opening brace `{`. The other two files (`Results.java` line 6 and `Roles.java` line 11) have the correct formatting with a space before `{`. This is a minor formatting inconsistency.

### A22-6: RoleId enum contains only a single constant — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Roles.java`
**Line(s):** 31-53
**Description:** The `RoleId` enum currently contains only one constant (`ROLE_COMPANY_GROUP`), yet the `fromId()` method iterates over `values()` and throws `IllegalArgumentException` for unrecognized names. The spring-security configuration in `spring-security.xml` references at least three other role strings (`ROLE_DRIVER`, `ROLE_SYS_ADMIN`, `ROLE_CLIENT`) that are not represented in this enum. If the intent is to have a type-safe enum of roles, it is incomplete. If only `ROLE_COMPANY_GROUP` needs programmatic lookup, the enum adds unnecessary abstraction for a single value. The `fromId()` method is never called in the current codebase (only `ROLE_COMPANY_GROUP.getId()` is used in `DriverService.java`), making `fromId()` potentially dead code.

### A22-7: `fromId()` method in RoleId enum is unused — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Roles.java`
**Line(s):** 44-52
**Description:** A search across the entire `src` directory reveals no call sites for `Roles.RoleId.fromId()`. The only usage of the `RoleId` enum is the static import of `ROLE_COMPANY_GROUP` and its `getId()` method in `DriverService.java` (line 22 and 74). The `fromId()` method appears to be dead code. Dead methods increase maintenance burden and may mislead developers into thinking this code path is exercised.

### A22-8: Inconsistent indentation style between Roles.java and other files — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Roles.java`
**Line(s):** 18-21 vs builder constructor 24-29
**Description:** `Roles.java` uses a mix of tab-based indentation (matching the rest of the codebase) and space-based indentation within the `@Builder` constructor parameter alignment. However, this is minor and follows what appears to be auto-generated formatting from an IDE. The sibling class `Equipment.java` exhibits the same mixed pattern (spaces for field declarations, tabs for constructor body), so this is a codebase-wide inconsistency rather than specific to `Roles.java`.

### A22-9: Empty Javadoc blocks for serialVersionUID — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Results.java`, `src/main/java/com/journaldev/spring/jdbc/model/Roles.java`, `src/main/java/com/journaldev/spring/jdbc/model/Services.java`
**Line(s):** Results.java:9-11, Roles.java:13-15, Services.java:8-10
**Description:** All three files contain empty Javadoc comment blocks (`/** */`) immediately above the `serialVersionUID` field. These appear to be IDE-generated placeholders that were never filled in. They add visual noise without providing any documentation value. This pattern is consistent across the codebase (also seen in `Result.java`) and appears to be an IDE default that was never cleaned up.

### A22-10: RoleId enum field `id` should be `final` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Roles.java`
**Line(s):** 34
**Description:** The `id` field in the `RoleId` enum is declared as `private String id` without the `final` modifier. Since enum constants are inherently immutable singletons, their fields should be `final` to prevent accidental mutation. The field is assigned only in the constructor and never modified, so adding `final` would be a safe improvement that communicates immutability intent.

### A22-11: Plural class names for non-collection models — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Results.java`, `src/main/java/com/journaldev/spring/jdbc/model/Roles.java`, `src/main/java/com/journaldev/spring/jdbc/model/Services.java`
**Line(s):** Results.java:6, Roles.java:11, Services.java:6
**Description:** All three model classes use plural names (`Results`, `Roles`, `Services`) even though each instance represents a single entity (one result, one role, one service record). Standard Java convention uses singular names for entity/model classes. For example, `Results` holds a single `message_id` and `error` (a single API response), `Roles` represents one role with one `authority`, and `Services` represents one service record. There is already a `Result.java` class in the same package (representing a different concept with different fields), which makes `Results` vs `Result` confusing. This is a codebase-wide convention issue rather than specific to these files and would be a large refactor to address.
# Pass 4 — Code Quality: A23

## Reading Evidence

### Sessions.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/Sessions.java`
- **Class:** `Sessions implements Serializable` (line 5)
- **Constants:** `serialVersionUID = -631947915399380621L` (line 10)
- **Fields:**
  - `int id` (line 12)
  - `int driver_id` (line 13)
  - `int unit_id` (line 14)
  - `String start_time` (line 15)
  - `String finish_time` (line 16)
  - `String photo_left_url` (line 17)
  - `String photo_right_url` (line 18)
  - `String photo_front_url` (line 19)
  - `String photo_back_url` (line 20)
  - `boolean prestart_required` (line 21)
- **Methods:**
  - `isPrestart_required()` — line 23
  - `setPrestart_required(boolean)` — line 26
  - `getId()` — line 29
  - `setId(int)` — line 32
  - `getDriver_id()` — line 35
  - `setDriver_id(int)` — line 38
  - `getUnit_id()` — line 41
  - `setUnit_id(int)` — line 44
  - `getStart_time()` — line 47
  - `setStart_time(String)` — line 50
  - `getFinish_time()` — line 53
  - `setFinish_time(String)` — line 56
  - `getPhoto_left_url()` — line 59
  - `setPhoto_left_url(String)` — line 62
  - `getPhoto_right_url()` — line 65
  - `setPhoto_right_url(String)` — line 68
  - `getPhoto_front_url()` — line 71
  - `setPhoto_front_url(String)` — line 74
  - `getPhoto_back_url()` — line 77
  - `setPhoto_back_url(String)` — line 80

### Types.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/Types.java`
- **Class:** `Types implements Serializable` (line 5)
- **Constants:** `serialVersionUID = 1060134076107695415L` (line 10)
- **Fields:**
  - `int id` (line 12)
  - `String name` (line 13)
  - `String url` (line 14)
- **Methods:**
  - `getId()` — line 16
  - `setId(int)` — line 19
  - `getName()` — line 22
  - `setName(String)` — line 25
  - `getUrl()` — line 28
  - `setUrl(String)` — line 31

### Usage.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/Usage.java`
- **Class:** `Usage implements Serializable` (line 6)
- **Constants:** `serialVersionUID = -2424248938396693587L` (line 11)
- **Fields:**
  - `String time` (line 13)
  - `BigDecimal usage = new BigDecimal(0)` (line 14)
- **Methods:**
  - `getTime()` — line 16
  - `setTime(String)` — line 19
  - `getUsage()` — line 22
  - `setUsage(BigDecimal)` — line 25

---

## Findings

### A23-1: Non-standard Java naming convention (snake_case fields and accessors) — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Sessions.java`
**Line(s):** 13-21, 23-82
**Description:** All field names and their corresponding getter/setter methods use snake_case (`driver_id`, `unit_id`, `start_time`, `finish_time`, `photo_left_url`, `photo_right_url`, `photo_front_url`, `photo_back_url`, `prestart_required`) instead of the standard Java camelCase convention (`driverId`, `unitId`, `startTime`, etc.). This produces non-standard JavaBean property names such as `getDriver_id()` and `isPrestart_required()`. While this works with Spring's `BeanPropertyRowMapper` (which maps underscored DB column names to underscored property names), it violates the JavaBeans specification and standard Java coding conventions. This pattern is pervasive across the codebase (observed in `Driver`, `DriverTraining`, `Charts`, `GPS`, etc.), indicating a systematic convention rather than an isolated mistake.

### A23-2: Temporal values stored as String instead of proper date/time types — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Sessions.java`
**Line(s):** 15-16
**Description:** The `start_time` and `finish_time` fields are typed as `String` rather than `java.time.LocalDateTime`, `java.time.Instant`, `java.sql.Timestamp`, or similar temporal types. This loses type safety: there is no compile-time guarantee that these fields contain valid date/time values, no ability to perform temporal arithmetic without parsing, and no protection against format mismatches between producers and consumers. The same issue applies to `Usage.time` (line 13 of Usage.java).

### A23-3: Temporal value stored as String in Usage model — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Usage.java`
**Line(s):** 13
**Description:** The `time` field is typed as `String` rather than an appropriate date/time type. Same concern as A23-2. This is used by `BeanPropertyRowMapper` in `ResumeController` to map query results, so the database layer is returning time values as strings with no type enforcement.

### A23-4: `new BigDecimal(0)` should be `BigDecimal.ZERO` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Usage.java`
**Line(s):** 14
**Description:** The field initializer `new BigDecimal(0)` creates a new object each time a `Usage` instance is constructed. The preferred idiom is `BigDecimal.ZERO`, which reuses the existing constant. This is a minor inefficiency and style issue. Notably, `ResumeController` already uses `BigDecimal.ZERO` for comparisons (lines 141, 185, 227), making this inconsistent within the same logical flow.

### A23-5: Missing `toString()`, `equals()`, and `hashCode()` methods — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Sessions.java`, `Types.java`, `Usage.java`
**Line(s):** All files
**Description:** None of the three model classes override `toString()`, `equals()`, or `hashCode()`. No model class in the entire `model` package (43 classes examined) overrides any of these methods. While these models are primarily used as DTOs for JSON serialization and JDBC row mapping, the absence of `toString()` makes debugging and logging harder (default `Object.toString()` produces only class name and hash), and the absence of `equals()`/`hashCode()` means collections cannot properly detect duplicates. This is a codebase-wide pattern rather than an omission specific to these three files.

### A23-6: Plural class name `Sessions` represents a single entity — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Sessions.java`
**Line(s):** 5
**Description:** The class name `Sessions` (plural) represents a single session entity, not a collection. Usage in `SessionController` confirms this: `ResponseEntity<Sessions>` returns one session, and `List<Sessions>` is used for collections. The conventional Java naming would be `Session` (singular) for the entity. The same plural naming pattern is seen in `Types.java` (line 5) — `Types` represents a single equipment type, not a collection. This is a codebase-wide pattern (e.g., `Answers`, `Reports`, `Incidents`, `Results`, `Questions`, `Permissions`, `Roles`, `Services`).

### A23-7: Plural class name `Types` represents a single entity — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Types.java`
**Line(s):** 5
**Description:** Same issue as A23-6. `Types` represents a single equipment type (with `id`, `name`, `url` fields). In `EquipmentController`, it is used as `List<Types>` for collections, confirming the class models an individual record. The conventional name would be `Type` or `EquipmentType` (the latter already exists as a separate class in the model package, creating potential confusion).

### A23-8: Overly generic class name `Types` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Types.java`
**Line(s):** 5
**Description:** The name `Types` is extremely generic and provides no domain context about what kind of type it represents. Reviewing its usage in `EquipmentController`, it represents equipment types associated with manufacturers. A more descriptive name such as `ManufacturerType` or `EquipmentModel` would improve readability. Additionally, `Types` shadows the concept of Java types and could be confused with `java.lang.reflect.Type` in code review or search.

### A23-9: Empty Javadoc comment on `serialVersionUID` — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Sessions.java`, `Types.java`, `Usage.java`
**Line(s):** Sessions.java lines 7-9, Types.java lines 7-9, Usage.java lines 8-10
**Description:** All three files contain an empty block Javadoc comment (`/** * */`) immediately above the `serialVersionUID` field. This is auto-generated boilerplate by IDE tooling (Eclipse) and carries no informational value. It adds visual noise without documenting anything.

### A23-10: Inconsistent formatting — missing space before opening brace in class declaration — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Types.java`, `Usage.java`
**Line(s):** Types.java line 5, Usage.java line 6
**Description:** `Types.java` and `Usage.java` declare `class Types implements Serializable{` and `class Usage implements Serializable{` with no space before the opening brace. `Sessions.java` correctly uses `class Sessions implements Serializable {` with a space. This is a minor formatting inconsistency. The pattern is split across the broader codebase as well.

### A23-11: Primitive `int` used for database ID fields — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/model/Sessions.java`, `Types.java`
**Line(s):** Sessions.java lines 12-14, Types.java line 12
**Description:** The `id`, `driver_id`, and `unit_id` fields in `Sessions`, and `id` in `Types`, use primitive `int` rather than `Integer`. Primitives default to `0` rather than `null`, which means it is impossible to distinguish between "ID not set" and "ID is zero." For model objects that are deserialized from JSON or mapped from database rows, `Integer` (nullable) is generally preferred to avoid silent default-value bugs, particularly for foreign key references (`driver_id`, `unit_id`) where `0` is likely not a valid value.
# Pass 4 — Code Quality: A24

## Reading Evidence

### User.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/User.java`
- **Class:** `User implements Serializable` (lines 13-44)
- **Annotations:** `@Data`, `@NoArgsConstructor`, `@EqualsAndHashCode(onlyExplicitlyIncluded = true)`, `@ToString(onlyExplicitlyIncluded = true)` (lines 9-12)
- **Fields:**
  - `serialVersionUID: long` (line 15)
  - `id: Long` (line 17)
  - `name: String` (line 19) — `@ToString.Include`
  - `email: String` (line 23) — `@EqualsAndHashCode.Include`, `@ToString.Include`
  - `password: String` (line 25)
  - `active: boolean` (line 28) — `@ToString.Include`
  - `roles: Set<Roles>` (line 30) — initialized to `new HashSet<>()`
- **Methods:**
  - `User(Long, String, String, String, boolean)` — `@Builder`, private constructor (line 33)
  - `addRoles(Roles)` — void (line 41)
- **Types/Constants:** `serialVersionUID = 2514353078919159376L`
- **Indentation:** 4 spaces

### UserResponse.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/model/UserResponse.java`
- **Class:** `UserResponse implements Serializable` (line 13)
- **Annotations:** `@Data`, `@NoArgsConstructor`, `@JsonInclude(JsonInclude.Include.NON_NULL)` (lines 10-12)
- **Fields:**
  - `serialVersionUID: long` (line 18)
  - `username: String` (line 19)
  - `email: String` (line 20)
  - `userCreateDate: String` (line 21)
  - `userStatus: String` (line 22)
  - `lastModifiedDate: String` (line 23)
  - `name: String` (line 24)
  - `lastname: String` (line 25)
  - `phoneNumber: String` (line 26)
- **Methods:** None (pure data class via Lombok `@Data`)
- **Types/Constants:** `serialVersionUID = 894041507646078302L`
- **Indentation:** Tabs

### APKUpdaterException.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterException.java`
- **Class:** `APKUpdaterException extends RuntimeException` (line 4)
- **Methods:**
  - `APKUpdaterException(String)` — constructor (line 5)
  - `APKUpdaterException(String, Throwable)` — constructor (line 9)
- **Types/Constants:** None
- **Indentation:** 4 spaces

---

## Findings

### A24-1: Password field exposed in JSON serialization — CRITICAL
**File:** `src/main/java/com/journaldev/spring/jdbc/model/User.java`
**Line(s):** 25
**Description:** The `password` field has no `@JsonIgnore` annotation and Lombok's `@Data` generates a public getter for it. The `UserController` (line 28) directly returns a `ResponseEntity<User>` to the client, meaning the password value is serialized into the JSON response body. This is a serious security vulnerability — credentials are leaked over the wire to any caller of `/rest/admin/user`. The field must be annotated with `@com.fasterxml.jackson.annotation.JsonIgnore` or `@JsonProperty(access = Access.WRITE_ONLY)`, or the controller should return a DTO that excludes the password.

### A24-2: Wildcard Lombok import — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/User.java`
**Line(s):** 3
**Description:** The import `lombok.*` is a wildcard import. This obscures which Lombok annotations are actually in use (`@Data`, `@NoArgsConstructor`, `@EqualsAndHashCode`, `@ToString`, `@Builder`) and can hide unused-import warnings. It is inconsistent with `UserResponse.java` (lines 7-8), which uses explicit individual Lombok imports. Prefer explicit imports for clarity and to avoid pulling in unintended symbols.

### A24-3: Inconsistent indentation — tabs vs. spaces across model classes — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/UserResponse.java`
**Line(s):** 15-27
**Description:** `UserResponse.java` uses tab indentation while `User.java` and `APKUpdaterException.java` use 4-space indentation. Mixing tabs and spaces within the same package causes diff noise in version control and can produce misaligned code in editors with different tab-width settings. The project should standardize on one style (the majority appears to be 4 spaces).

### A24-4: Empty Javadoc comment on serialVersionUID — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/UserResponse.java`
**Line(s):** 15-17
**Description:** There is an empty Javadoc block (`/** */`) above `serialVersionUID`. This is auto-generated IDE boilerplate that adds no informational value. It should either be removed or replaced with a meaningful comment.

### A24-5: Missing space before opening brace in class declaration — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/UserResponse.java`
**Line(s):** 13
**Description:** The class declaration reads `implements Serializable{` with no space before the opening brace. Standard Java formatting requires a space: `implements Serializable {`. This is a minor style inconsistency.

### A24-6: Date fields stored as String instead of temporal types — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/UserResponse.java`
**Line(s):** 21, 23
**Description:** `userCreateDate` and `lastModifiedDate` are declared as `String`. Using `String` for date/time values loses type safety — callers cannot perform date arithmetic, comparison, or formatting without first parsing these strings. These should be `java.time.Instant`, `java.time.LocalDateTime`, or `java.util.Date` with appropriate Jackson serialization annotations (e.g., `@JsonFormat`). This is a design smell that leads to scattered date-parsing logic and potential format mismatches.

### A24-7: Builder does not initialize the roles collection — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/model/User.java`
**Line(s):** 30, 32-39
**Description:** The `roles` field is initialized to `new HashSet<>()` at declaration (line 30), but the `@Builder` constructor (lines 32-39) does not accept or set `roles`. When using `User.builder().build()`, Lombok's generated builder will call the `@Builder`-annotated constructor, which never touches the `roles` field. Because the field initializer `new HashSet<>()` runs before the constructor body, the set will still be initialized in this case. However, this creates a subtle coupling: if the class is later refactored to use `@Builder` on the class level or if the `@AllArgsConstructor` pattern is introduced, `roles` could silently become `null`. Adding `@Builder.Default` on the `roles` field would make the intent explicit and protect against future regressions.

### A24-8: Method naming — addRoles takes a single role — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/model/User.java`
**Line(s):** 41
**Description:** The method `addRoles(Roles role)` takes a single `Roles` parameter but uses the plural name `addRoles`. The conventional naming would be `addRole(Role role)`. The underlying type `Roles` is also plural, which compounds the confusion — a single role entity should be named `Role`, and the method should be `addRole(Role role)`.

### A24-9: APKUpdaterException missing serialVersionUID — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterException.java`
**Line(s):** 4
**Description:** `APKUpdaterException` extends `RuntimeException` (which is `Serializable`) but does not declare a `serialVersionUID`. This will generate a compiler warning and could cause deserialization failures if the class changes between JVM versions. Other Serializable classes in this codebase (`User`, `UserResponse`, `Roles`) all declare explicit `serialVersionUID` values.

### A24-10: APKUpdaterException in wrong package — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterException.java`
**Line(s):** 1
**Description:** `APKUpdaterException` resides in the `service` package alongside `APKUpdaterService`. While this is not incorrect, exception classes are often placed in a dedicated `exception` package or alongside the model layer for better separation. This is noted for organizational awareness only and is consistent with the project's current flat structure, so no change is strictly needed.
# Pass 4 — Code Quality: A25

## Reading Evidence

### APKUpdaterService.java
- **Class:** `APKUpdaterService` (line 19), annotated `@Service`
- **Fields:**
  - `packageDir` (line 22): `String`, injected via `@Value("${packageDir}")`
  - `pattern` (line 25): `Pattern`, compiled regex for APK filenames
- **Methods:**
  - `getAvailablePackage(String baseUrl, String pkgName, String currentVersion)` — line 28, returns `Optional<PackageEntry>`
  - `loadPackageAsResource(String pkgname, String version)` — line 54, returns `Resource`
- **Types/Errors referenced:** `PackageEntry`, `APKUpdaterException`, `FileNotFoundException`, `Resource`, `UrlResource`, `IOException`
- **Constants:** Regex pattern `"(\\w*)-(\\d*\\.?\\d*?\\.?\\d*?\\.?-\\w*)\\.apk"` (line 25)

### AWSFileStorageService.java
- **Class:** `AWSFileStorageService` (line 24), extends `AbstractFileStorageService`, annotated `@Service("awsFileStorage")`, `@Slf4j`
- **Fields:**
  - `cloudImagedDir` (line 26): `String`, injected via `@Value("${cloudImagedDir}")`
  - `bucketName` (line 29): `String`, injected via `@Value("${bucketName}")`
  - `credentials` (line 31): `static AWSCredentials`, hardcoded `BasicAWSCredentials`
- **Methods:**
  - `saveImage(InputStream inputStream)` — line 38, returns `String` (overrides parent)
  - `loadImageAsResource(String fileName)` — line 45, returns `Resource` (overrides parent, returns `null`)
  - `connectAWSS3()` — line 50, returns `AmazonS3` (private)
  - `uploadObject(String key_name, String file_path)` — line 62, returns `void` (private)
- **Types/Errors referenced:** `AmazonServiceException`, `AWSCredentials`, `BasicAWSCredentials`, `AWSStaticCredentialsProvider`, `AmazonS3`, `AmazonS3ClientBuilder`, `CannedAccessControlList`, `PutObjectRequest`, `File`

### AbstractFileStorageService.java
- **Class:** `AbstractFileStorageService` (line 23), abstract, package-private, implements `FileStorageService`, annotated `@Slf4j`
- **Fields:**
  - `uploadDir` (line 26): `String`, protected, `@Value("${uploadDir}")`
  - `imageDir` (line 29): `String`, protected, `@Value("${imageDir}")`
  - `imagePrefix` (line 32): `String`, private, `@Value("${imagePrefix}")`
  - `imageStorageLocation` (line 34): `Path`, protected
  - `targetLocation` (line 36): `Path`, protected
  - `fileName` (line 38): `String`, protected
  - `imageExt` (line 40): `String`, protected, initialized to `".jpg"`
- **Methods:**
  - `initialize()` — line 43, `@PostConstruct`, returns `void`
  - `saveImage(InputStream inputStream)` — line 53, returns `String` (overrides interface)
- **Types/Errors referenced:** `FileStorageService`, `FileStorageException`, `MimeType`, `MimeTypes`, `MimeTypeException`, `URLConnection`, `Util`, `IOException`

---

## Findings

### A25-1: Hardcoded AWS Credentials in Source Code — CRITICAL
**File:** `src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java`
**Line(s):** 31-34
**Description:** AWS access key ID (`AKIA**REDACTED**`) and secret access key (`****REDACTED****`) are hardcoded as a static field. This is a severe security vulnerability: credentials are committed to version control, cannot be rotated without a code change and redeployment, and violate AWS security best practices. AWS credentials should be supplied via environment variables, IAM roles, AWS Secrets Manager, or the default credential provider chain. This also applies to the SMTP credentials found in `Util.java` (line 66), which is referenced by `AbstractFileStorageService`.

### A25-2: S3 Object Uploaded with Public-Read ACL — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java`
**Line(s):** 73-74
**Description:** Every uploaded file is given `CannedAccessControlList.PublicRead` permission, making all uploaded objects publicly accessible on the internet. If these are user-uploaded images or operational data, this could expose sensitive content. The ACL should be set to private unless there is an explicit, documented business requirement for public access.

### A25-3: Thread-Safety Issue — Mutable Instance State in Singleton Service — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java`
**Line(s):** 36-40
**Description:** The fields `targetLocation`, `fileName`, and `imageExt` are protected mutable instance fields on a Spring singleton bean. In `saveImage()`, these fields are written (lines 58, 65, 67) and then read by `AWSFileStorageService.saveImage()` (line 39-40) after the `super.saveImage()` call. If two threads call `saveImage()` concurrently, one thread's `fileName`/`targetLocation` can be overwritten by another thread before it is used, leading to data corruption (wrong file uploaded to S3, wrong filename returned). These should be local variables returned/passed rather than shared mutable state.

### A25-4: `loadImageAsResource` Returns Null Instead of Throwing or Implementing — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java`
**Line(s):** 44-47
**Description:** The `loadImageAsResource` override returns `null` unconditionally. This is a contract violation of the `FileStorageService` interface. Any caller invoking this method will receive `null` and likely encounter a `NullPointerException` downstream. This should either throw `UnsupportedOperationException` with a descriptive message or be properly implemented to load resources from S3.

### A25-5: S3 Upload Failure Silently Swallowed — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java`
**Line(s):** 75-77
**Description:** The `AmazonServiceException` in `uploadObject` is caught and only logged. The method returns normally, and `saveImage()` returns the filename as if the upload succeeded. The caller has no indication that the S3 upload failed. This can lead to broken image references in the system. The exception should be propagated or the method should return a success/failure indicator.

### A25-6: `doesBucketExist` Is Deprecated and Auto-Creating Buckets Is Dangerous — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java`
**Line(s):** 67-70
**Description:** `AmazonS3.doesBucketExist(String)` has been deprecated in favor of `doesBucketExistV2`. More importantly, automatically creating an S3 bucket at upload time is a dangerous pattern: it can create buckets with incorrect permissions, in the wrong region, or without required encryption/logging policies. Bucket creation should be handled by infrastructure provisioning (e.g., Terraform/CloudFormation), not application code.

### A25-7: New S3 Client Created on Every Upload — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java`
**Line(s):** 50-56, 65
**Description:** `connectAWSS3()` builds a new `AmazonS3` client on every call to `uploadObject`. The `AmazonS3Client` is designed to be created once and reused; it manages its own internal HTTP connection pool. Creating a new client per request wastes resources and can cause connection pool exhaustion under load. The client should be initialized once (e.g., in a `@PostConstruct` method or as a `@Bean`).

### A25-8: APKUpdaterException Constructed Without Cause on Line 66 — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java`
**Line(s):** 66
**Description:** In the `catch (IOException e)` block at line 65-67, the `APKUpdaterException` is constructed with only a message string but not the caught `IOException` cause. This discards the original stack trace, making debugging significantly harder. Compare with line 50 where the cause is correctly passed. The constructor call should be `new APKUpdaterException("...", e)`.

### A25-9: Inconsistent Alignment/Indentation in Builder Calls — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java`
**Line(s):** 39-43
**Description:** The builder chain inside the lambda has inconsistent indentation. `.fileName(filename)` (line 40), `.baseUrl(baseUrl)` (line 41), `.version(version)` (line 42), and `.name(name)` (line 43) each have different indentation levels. This reduces readability. Builder method chains should be aligned consistently.

### A25-10: Typo in Method Name Referenced: `generateRadomName` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java`
**Line(s):** 65
**Description:** The method `Util.generateRadomName()` contains a typo ("Radom" instead of "Random"). While this is technically a finding in `Util.java`, the call site is in `AbstractFileStorageService`. This misspelling makes the API less discoverable and appears unprofessional. It should be renamed to `generateRandomName()`.

### A25-11: `pattern` Field Should Be `static final` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java`
**Line(s):** 25
**Description:** The `Pattern` object is compiled from a constant regex string and is immutable/thread-safe. It should be declared as `private static final Pattern PATTERN = ...` rather than an instance field. This avoids recompiling the pattern for each service instance (though Spring singleton means typically one instance) and follows Java conventions for constants.

### A25-12: Potential `NullPointerException` on Null Map Result — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java`
**Line(s):** 46-47
**Description:** The lambda in the `map()` call returns `null` when the filename does not match the pattern (line 46). While the subsequent `.filter(p -> p != null ...)` guards against the null, returning `null` from a `map()` operation is an anti-pattern in Java streams. It would be cleaner to use `flatMap` with `Optional` to avoid null values in the stream entirely.

### A25-13: Missing `serialVersionUID` on `APKUpdaterException` — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java` (references `APKUpdaterException.java`)
**Line(s):** N/A (APKUpdaterException.java:4)
**Description:** `APKUpdaterException` extends `RuntimeException` (which is `Serializable`) but does not declare a `serialVersionUID`. This will generate a compiler warning and can cause deserialization issues if the class structure changes. Compare with `FileStorageException` which correctly declares `serialVersionUID`.

### A25-14: `imageExt` Field Reset in `saveImage` Has Side Effects on Default — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java`
**Line(s):** 40, 58
**Description:** The field `imageExt` is initialized to `".jpg"` at line 40. If `saveImage` successfully determines the MIME type, it overwrites `imageExt` at line 58. However, since this is an instance field on a singleton, the default `".jpg"` is effectively only used for the first call where type detection fails. Subsequent calls where detection fails will use whatever extension was set by the last successful detection, not `".jpg"`. This is a subtle bug compounding the thread-safety issue in A25-3.
# Pass 4 — Code Quality: A26

## Reading Evidence

### BootstrapService.java
- **Class/Interface:** `BootstrapService` (public class, annotated `@Configuration`) — line 16
- **Inner Class:** `FlywayBean` (public non-static inner class) — line 40
- **Fields:**
  - `DataSource dataSource` (`@Autowired`) — line 18-19
  - `boolean baseline` (`@Value("${flyway.baseline}")`) — line 21-22
  - `boolean enabled` (`@Value("${flyway.enabled}")`) — line 24-25
- **Methods:**
  - `FlywayBean getFlyway()` — line 28 (`@Bean(initMethod = "migrate")`)
  - `FlywayBean()` (no-arg constructor) — line 44
  - `FlywayBean(Flyway flyway)` — line 47
  - `int migrate()` — line 51
- **Types/Constants:** `Flyway`, `FlywayException`, `DataSource`
- **Imports:** `org.flywaydb.core.Flyway`, `org.flywaydb.core.api.FlywayException`, SLF4J Logger/LoggerFactory (lines 5-6), Spring `@Autowired`, `@Value`, `@Bean`, `@Configuration`

### CognitoService.java
- **Class/Interface:** `CognitoService` (public class, annotated `@Service`, `@Slf4j`) — line 25
- **Fields:**
  - `Configuration configuration` (`@Autowired`) — line 27-28
- **Methods:**
  - `UserResponse getUser(String username)` — line 30
  - `AuthenticationResponse authenticationRequest()` — line 69
- **Types/Constants:** `AuthenticationRequest`, `AuthenticationResponse`, `UserResponse`, `Configuration`, `RestTemplate`, `HttpHeaders`, `HttpEntity`, `HttpMethod`, `HttpStatus`, `MediaType`, `ResponseEntity`, `URI`
- **Imports:** `java.net.URI`, `java.util.ArrayList`, Spring HTTP classes, model classes, `lombok.extern.slf4j.Slf4j`

### DriverAlreadyExistException.java
- **Class/Interface:** `DriverAlreadyExistException` (public class, extends `DriverServiceException`) — line 3
- **Methods:**
  - `DriverAlreadyExistException(String message)` — line 5
  - `DriverAlreadyExistException(String message, Throwable cause)` — line 9
- **Types/Constants:** none
- **Parent:** `DriverServiceException extends RuntimeException` (confirmed in separate file)

---

## Findings

### A26-1: Deprecated Flyway API — `new Flyway()` constructor removed in Flyway 6+ — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/service/BootstrapService.java`
**Line(s):** 30-33
**Description:** The code uses `new Flyway()` and then calls `flyway.setBaselineOnMigrate()`, `flyway.setDataSource()`, and `flyway.setLocations()`. This programmatic-setter API was deprecated in Flyway 5.x and removed entirely in Flyway 6+. The project currently pins Flyway to version 5.1.4 (pom.xml line 17), so the code compiles today, but any upgrade to Flyway 6+ will break this class. The modern approach uses `Flyway.configure().dataSource(...).baselineOnMigrate(...).locations(...).load()`. This is a known upgrade-blocker.

### A26-2: `System.out.println` used instead of logger — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/service/BootstrapService.java`
**Line(s):** 55
**Description:** The `migrate()` method in the inner `FlywayBean` class uses `System.out.println("Flyway is disabled, database migration ignored...")` instead of the SLF4J logger. The enclosing class imports `org.slf4j.Logger` and `org.slf4j.LoggerFactory` (lines 5-6) but never instantiates a logger instance, making both imports unused. The `System.out` call bypasses structured logging, meaning this message will not appear in log aggregation systems, will lack timestamps/context, and cannot be filtered by log level.

### A26-3: Unused SLF4J imports in BootstrapService — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/BootstrapService.java`
**Line(s):** 5-6
**Description:** `Logger` and `LoggerFactory` are imported but never used anywhere in the class. No logger field is declared. These unused imports will generate compiler warnings and indicate dead code.

### A26-4: Non-static inner class `FlywayBean` holds implicit reference to enclosing `BootstrapService` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/BootstrapService.java`
**Line(s):** 40
**Description:** `FlywayBean` is declared as a public non-static inner class. This means every `FlywayBean` instance holds a hidden reference to the enclosing `BootstrapService` instance, preventing the `BootstrapService` (and its `DataSource`) from being garbage-collected as long as the `FlywayBean` Spring bean is alive. Since `FlywayBean` does not reference any members of `BootstrapService`, it should be declared `static` (or extracted to a top-level class).

### A26-5: Access token passed as URL query parameter — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java`
**Line(s):** 48
**Description:** In `getUser()`, the access token is appended directly to the URL as a query parameter: `"...&accessToken="+accessToken`. Tokens in URLs are logged by web servers, proxies, and browser history, and appear in `Referer` headers. The access token should be passed in an `Authorization` header (e.g., `Bearer <token>`) instead. Additionally, the `username` parameter is not URL-encoded, which could cause breakage or injection if a username contains special characters.

### A26-6: `e.printStackTrace()` used alongside logger — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java`
**Line(s):** 62, 101
**Description:** Both `getUser()` and `authenticationRequest()` call `e.printStackTrace()` before logging the error with SLF4J. `printStackTrace()` writes to `System.err`, which bypasses the logging framework, produces unstructured output, and duplicates the error information. The `log.error()` calls also only log `e.getMessage()` without the stack trace (the throwable should be passed as the second argument to `log.error()`). The `printStackTrace()` calls should be removed and replaced with `log.error(method + " error:", e)` to include the full stack trace in the structured log.

### A26-7: `RestTemplate` instantiated on every method call — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java`
**Line(s):** 36, 77
**Description:** Both `getUser()` and `authenticationRequest()` create a new `RestTemplate` instance on each invocation. `RestTemplate` is thread-safe and designed to be reused. Creating it on every call wastes resources (the underlying HTTP connection pool is not shared) and prevents configuring timeouts, interceptors, or error handlers in a centralized way. It should be injected as a Spring bean or at minimum declared as a class-level field.

### A26-8: Broad exception catching swallows all errors silently — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java`
**Line(s):** 60, 99
**Description:** Both methods catch `Exception` (the broadest checked+unchecked type), log the message, and then return a default-constructed empty response object. This means callers of `getUser()` and `authenticationRequest()` receive what appears to be a valid (but empty) response with no indication that an error occurred. Authentication failures, network timeouts, deserialization errors, and even `NullPointerException` are all swallowed identically. At minimum, authentication failures in `authenticationRequest()` should propagate to callers, since `getUser()` unconditionally calls `authResponse.getSessionToken()` (line 34) on the potentially empty result, which could return null and lead to `"null"` being embedded in the URL.

### A26-9: Hardcoded `localhost` URL for Cognito API — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java`
**Line(s):** 48, 89
**Description:** Both methods construct URLs using `"http://localhost:"` hardcoded as the host. While the port is configurable via `configuration.getCognitoAPIPort()`, the host and protocol (`http` vs `https`) are not. This means the service cannot point to a remote Cognito API in deployed environments without code changes, and it forces plaintext HTTP communication. The full base URL should be externalized to configuration.

### A26-10: Constructed `HttpHeaders` not used in `getUser()` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java`
**Line(s):** 38-42
**Description:** In `getUser()`, an `ArrayList<MediaType>` and `HttpHeaders` object are created and configured (lines 38-42), but `headers` is never passed to the `RestTemplate` call on line 50 (`restTemplate.getForEntity(uri, UserResponse.class)` does not accept headers). This is dead code — the headers have no effect on the request. Either the request should use `exchange()` with an `HttpEntity` wrapping the headers (as `authenticationRequest()` does), or the header setup should be removed.

### A26-11: Manual method-name logging pattern instead of using SLF4J MDC or `@Slf4j` method reference — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java`
**Line(s):** 32, 71
**Description:** Both methods manually construct a `String method` variable via `this.getClass().getName() + " : methodName "` and prepend it to every log message. This is verbose, error-prone (the string can drift from the actual method name), and is the exact problem that SLF4J's `Logger` naming convention (one logger per class, named after the class) already solves. With `@Slf4j`, the class name is automatically included in every log line by the logging framework's pattern layout.

### A26-12: Typo "Succuss" in log messages — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java`
**Line(s):** 54, 93
**Description:** Both `getUser()` and `authenticationRequest()` log `"HttpStatus Succuss"` instead of `"HttpStatus Success"`. While this does not affect functionality, it makes log searching and monitoring unreliable if anyone searches for the correctly spelled word.

### A26-13: Missing `serialVersionUID` on exception classes — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/DriverAlreadyExistException.java`
**Line(s):** 3
**Description:** `DriverAlreadyExistException` (and its parent `DriverServiceException`) extend `RuntimeException` (which is `Serializable`) but do not declare a `serialVersionUID`. This generates a compiler warning and could cause deserialization failures if the class structure changes between versions. Other exception classes in the same package (e.g., `FileStorageException`) do declare `serialVersionUID`.

### A26-14: Inconsistent naming — "Exist" vs "Exists" — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/service/DriverAlreadyExistException.java`
**Line(s):** 3
**Description:** The class name `DriverAlreadyExistException` is grammatically awkward; the standard English and Java convention would be `DriverAlreadyExistsException` (third-person singular). The usage site in `DriverService.java` line 69 also uses the message `"Driver already exist in database"` with the same grammatical error. This is a minor naming inconsistency.

### A26-15: Mixed indentation style — tabs vs spaces — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java`
**Line(s):** throughout
**Description:** `CognitoService.java` uses a mix of tabs and spaces for indentation. For example, the class-level field declaration (line 28) uses spaces, while method bodies (lines 31-67) predominantly use tabs. `BootstrapService.java` consistently uses spaces. This inconsistency across files in the same package suggests the project lacks an enforced code formatter. Mixed indentation causes noisy diffs and makes code harder to read.
# Pass 4 — Code Quality: A27

## Reading Evidence

### DriverService.java
- **Class:** `DriverService` (public, `@Service`, `@Transactional`, `@Slf4j`) — Line 27
- **Constants:**
  - `PASSWORD_GEN_RULES` (`CharacterRule[]`, private static final) — Line 29
  - `PASSWORD_LENGTH` (`int`, value 8, private static final) — Line 37
- **Fields (all `@Autowired`):**
  - `userDAO` (`UserDAO`) — Line 40
  - `companyDAO` (`CompanyDAO`) — Line 43
  - `configuration` (`Configuration`) — Line 46
  - `driverDAO` (`DriverDAO`) — Line 49
- **Methods:**
  - `authenticate(String, String)` : `Optional<Driver>` (`@Deprecated`) — Line 52
  - `registerDriver(Driver)` : `Driver` — Line 66
  - `resetPassword(Driver)` : `void` (throws `DriverServiceException`) — Line 99
  - `generateRandomPassword()` : `String` (private) — Line 119
- **Imports:** `CompanyDAO`, `DriverDAO`, `UserDAO`, `Company`, `Driver`, `Roles`, `Configuration`, `SendEmail`, `CharacterRule`, `EnglishCharacterData`, `PasswordGenerator`, `SQLException`, `Optional`, `ROLE_COMPANY_GROUP`
- **Exceptions thrown:** `DriverServiceException` (lines 59, 115), `DriverAlreadyExistException` (line 69)

### DriverServiceException.java
- **Class:** `DriverServiceException` extends `RuntimeException` (public) — Line 3
- **Constructors:**
  - `DriverServiceException(String message)` — Line 5
  - `DriverServiceException(String message, Throwable cause)` — Line 9
- **No fields, no constants, no annotations.**

### EntityNotFoundException.java
- **Class:** `EntityNotFoundException` extends `RuntimeException` (public, `@ResponseStatus(HttpStatus.NOT_FOUND)`) — Line 7
- **Constructors:**
  - `EntityNotFoundException(String message)` — Line 9
- **Imports:** `HttpStatus`, `ResponseStatus`

---

## Findings

### A27-1: Deprecated `new Long(int)` constructor — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/service/DriverService.java`
**Line(s):** 79
**Description:** `driver.setComp_id(new Long(compId))` uses the `Long(int)` constructor, which was deprecated in Java 9 and removed in Java 16+. This will cause a compilation failure if the project is built against JDK 16 or later. The correct replacement is `Long.valueOf(compId)`, which also benefits from the JVM's Long cache for small values.

### A27-2: Commented-out code block (dead SMS sending logic) — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/service/DriverService.java`
**Line(s):** 88-93
**Description:** A six-line block of commented-out code exists in `registerDriver()`. It appears to be remnant SMS-sending logic (`SendMessage.sendMail`). Commented-out code degrades readability and creates ambiguity about intended behavior. If the feature is planned, it should be tracked in a ticket; otherwise it should be removed.

### A27-3: Inconsistent logging style — string concatenation vs. parameterized placeholders — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/DriverService.java`
**Line(s):** 85-87 vs 110-112
**Description:** In `registerDriver()` (lines 85, 87) the code correctly uses SLF4J parameterized logging: `log.info("Start Sending Email to {}", email)`. However, in `resetPassword()` (lines 110, 112) the same logical messages use string concatenation instead: `log.info("Start Sending Email to " + email)`. This is inconsistent within the same class. String concatenation forces the String to be built even when the log level is disabled, creating unnecessary allocation overhead. All log statements should use parameterized `{}` placeholders.

### A27-4: Plain-text password sent via email in `resetPassword` — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/service/DriverService.java`
**Line(s):** 108
**Description:** The reset password is embedded in a plain-text email message string: `"Your ForkliftIQ360 Account Password is reset to " + pass`. The generated password is transmitted in cleartext via email, which is a security anti-pattern. Modern password reset flows should use a time-limited token/link rather than sending the actual password. Additionally, the password string lingers in memory as a `String` object (not cleared). This is flagged as a code quality / design concern.

### A27-5: Static method call to `SendEmail.sendMail()` — leaky abstraction / untestable — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/service/DriverService.java`
**Line(s):** 86, 111
**Description:** `SendEmail.sendMail(...)` is a static utility call. This makes the `DriverService` class impossible to unit-test in isolation without a real email subsystem (or bytecode-level mocking via PowerMock/Mockito inline). The email-sending capability should be abstracted behind an interface and injected, consistent with the Spring DI pattern already used for `userDAO`, `companyDAO`, etc.

### A27-6: Field injection (`@Autowired` on private fields) instead of constructor injection — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/service/DriverService.java`
**Line(s):** 39-49
**Description:** All four dependencies (`userDAO`, `companyDAO`, `configuration`, `driverDAO`) use field injection via `@Autowired`. The Spring team and wider community recommend constructor injection because it: (a) makes dependencies explicit, (b) enables immutability (`final` fields), (c) allows the class to be instantiated in tests without a Spring context, and (d) prevents the class from being in a partially-constructed state. With Lombok `@Slf4j` already present, `@RequiredArgsConstructor` could be added trivially.

### A27-7: `authenticate()` anti-pattern — Optional unwrap then re-wrap — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/DriverService.java`
**Line(s):** 54-63
**Description:** The `authenticate` method calls `driverDAO.findByEmailAndPassword(email, password).orElse(null)` to extract the value, performs a null check, and then re-wraps in `Optional.ofNullable(driver)`. This defeats the purpose of `Optional`. The idiomatic approach is to use `Optional.ifPresent()` or `Optional.map()` to perform the side-effect (updating last login time) and return the Optional directly, e.g.:
```java
Optional<Driver> opt = driverDAO.findByEmailAndPassword(email, password);
opt.ifPresent(d -> { try { driverDAO.updateLastLoginTime(d); } ... });
return opt;
```

### A27-8: Missing `serialVersionUID` on all three exception classes — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/DriverServiceException.java`, `EntityNotFoundException.java`
**Line(s):** entire files
**Description:** `DriverServiceException` and `EntityNotFoundException` both extend `RuntimeException` (which is `Serializable`), but neither declares a `serialVersionUID`. Other exception classes in the same package (e.g., `FileStorageException`, `SaveFileInfo`) do declare it. Omitting `serialVersionUID` means the JVM will auto-generate one, which can change between compiler versions and break serialization compatibility. This also produces a compiler/IDE warning.

### A27-9: `EntityNotFoundException` couples service layer to HTTP via `@ResponseStatus` — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/service/EntityNotFoundException.java`
**Line(s):** 6
**Description:** `EntityNotFoundException` resides in the `service` package and is thrown from the DAO layer (`DriverDAOImpl`), yet it carries `@ResponseStatus(HttpStatus.NOT_FOUND)` — a Spring Web annotation. This couples the domain/persistence layer to the HTTP transport layer. A service-layer exception should be transport-agnostic; the mapping to HTTP status codes should be handled by a `@ControllerAdvice` or at the controller level.

### A27-10: `EntityNotFoundException` missing cause-chain constructor — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/EntityNotFoundException.java`
**Line(s):** 9
**Description:** `EntityNotFoundException` only provides a single-argument constructor `(String message)`. It lacks a `(String message, Throwable cause)` constructor, unlike `DriverServiceException` which provides both. Without a cause-chain constructor, the original exception context (e.g., the `EmptyResultDataAccessException` from the DAO) is lost when this exception is thrown. This makes debugging harder in production.

### A27-11: `PASSWORD_LENGTH` of 8 is below modern security recommendations — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/DriverService.java`
**Line(s):** 37
**Description:** The generated password length is 8 characters. While the password does include upper, lower, digit, and special character rules, NIST SP 800-63B and OWASP guidelines recommend a minimum of 12-15 characters for randomly generated passwords/passphrases. Given that this password is auto-generated (not user-chosen), increasing the length carries no usability cost.

### A27-12: Class-level `@Transactional` on `DriverService` may be overly broad — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/service/DriverService.java`
**Line(s):** 26
**Description:** The `@Transactional` annotation is applied at the class level, meaning every public method (including `authenticate`, which is read-only, and `generateRandomPassword`, which touches no data) will open a transaction. Consider using `@Transactional(readOnly = true)` at the class level and overriding with `@Transactional` on mutating methods, or applying `@Transactional` only on methods that require it.
# Pass 4 — Code Quality: A28

## Reading Evidence

### FileNotFoundException.java
- **Class/Interface:** `FileNotFoundException` (class, extends `FileStorageException`)
- **Annotations:** `@ResponseStatus(HttpStatus.NOT_FOUND)`
- **Methods:**
  - `FileNotFoundException(String message)` — line 9 (constructor)
- **Types/Constants:** None
- **Imports:** `org.springframework.http.HttpStatus`, `org.springframework.web.bind.annotation.ResponseStatus`
- **Lines:** 1-13

### FileStorageException.java
- **Class/Interface:** `FileStorageException` (class, extends `RuntimeException`)
- **Methods:**
  - `FileStorageException(String message)` — line 7 (constructor)
  - `FileStorageException(String message, Throwable cause)` — line 11 (constructor)
- **Types/Constants:**
  - `serialVersionUID = 8988464861907090725L` — line 5
- **Lines:** 1-15

### FileStorageService.java
- **Class/Interface:** `FileStorageService` (interface)
- **Methods:**
  - `saveImage(InputStream inputStream)` — line 8 (returns `String`)
  - `loadImageAsResource(String fileName)` — line 10 (returns `Resource`)
- **Types/Constants:** None
- **Imports:** `org.springframework.core.io.Resource`, `java.io.InputStream`
- **Lines:** 1-12

## Findings

### A28-1: Missing `serialVersionUID` in `FileNotFoundException` — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/service/FileNotFoundException.java`
**Line(s):** 7
**Description:** `FileNotFoundException` extends `FileStorageException` (which itself extends `RuntimeException`), making it `Serializable`. The parent `FileStorageException` correctly declares `serialVersionUID` (line 5 of that file), but this subclass does not. While runtime exceptions are rarely serialized intentionally, the JVM will auto-generate a `serialVersionUID` at runtime, which is fragile and can cause `InvalidClassException` if the class structure changes between serialization and deserialization (e.g., across distributed systems or session stores). The Java serialization specification and most static analysis tools (SpotBugs, IntelliJ inspections) flag this as a warning, so it will produce build warnings in projects that enable such checks.

### A28-2: Custom `FileNotFoundException` shadows `java.io.FileNotFoundException` — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/service/FileNotFoundException.java`
**Line(s):** 7
**Description:** The custom class `com.journaldev.spring.jdbc.service.FileNotFoundException` shares the simple name `FileNotFoundException` with `java.io.FileNotFoundException`. This creates a naming collision that can lead to developer confusion and accidental import of the wrong type. Any file in the same package that needs to reference `java.io.FileNotFoundException` would require a fully-qualified name. This is a well-known anti-pattern. Consider renaming to something more descriptive such as `FileResourceNotFoundException` or `StorageFileNotFoundException` to avoid ambiguity.

### A28-3: Missing cause-chaining constructor in `FileNotFoundException` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/FileNotFoundException.java`
**Line(s):** 9-11
**Description:** `FileNotFoundException` only provides a single-argument `(String message)` constructor, while its parent `FileStorageException` provides both `(String message)` and `(String message, Throwable cause)` constructors. This means callers cannot wrap an underlying cause when throwing a `FileNotFoundException`. While current usage sites (in `LocalFileStorageService` line 24 and `APKUpdaterService` line 62) do not pass a cause, the asymmetry with the parent class reduces flexibility and violates the common Java exception design convention of providing at least the message+cause constructor.

### A28-4: `FileStorageService` interface lacks Javadoc — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/FileStorageService.java`
**Line(s):** 7-11
**Description:** The `FileStorageService` interface defines the public contract for file storage operations but has no Javadoc on the interface itself or on either method. Since this interface has multiple implementations (`LocalFileStorageService`, `AWSFileStorageService` via `AbstractFileStorageService`), documentation of the expected behavior, return values, and exception semantics is important for maintainability. For example, it is not documented what `saveImage` returns (a filename? a path? a URL?), what happens on failure, or whether `loadImageAsResource` may return `null` (it does in `AWSFileStorageService`).

### A28-5: `@ResponseStatus` on exception only works without `@ExceptionHandler` — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/service/FileNotFoundException.java`
**Line(s):** 6
**Description:** The `@ResponseStatus(HttpStatus.NOT_FOUND)` annotation on `FileNotFoundException` relies on Spring's `DefaultHandlerExceptionResolver` to translate the exception into an HTTP 404 response. A codebase search confirmed there is no `@ControllerAdvice` or `@ExceptionHandler` that would intercept this exception, so the annotation works as intended. However, this mechanism is fragile: if a global exception handler is added in the future, it will silently override the `@ResponseStatus` behavior unless it explicitly checks for the annotation. This is noted as an informational observation, not a current defect.

### A28-6: Exception class located in `service` package rather than a dedicated exceptions package — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/service/FileNotFoundException.java`, `src/main/java/com/journaldev/spring/jdbc/service/FileStorageException.java`
**Line(s):** N/A (package-level concern)
**Description:** Both exception classes reside in `com.journaldev.spring.jdbc.service` alongside service interfaces and implementations. A more conventional package structure would place custom exceptions in a dedicated package (e.g., `com.journaldev.spring.jdbc.exception`). The current placement means the `service` package mixes concerns: domain exceptions, service interfaces, and service implementations. This is a minor structural concern but worth noting for future refactoring.

### A28-7: `FileStorageException` extends `RuntimeException` — unchecked by design — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/service/FileStorageException.java`
**Line(s):** 3
**Description:** `FileStorageException` extends `RuntimeException`, making it an unchecked exception. This is an intentional design choice consistent with Spring conventions (Spring generally favors unchecked exceptions). Callers are not forced to handle this exception, which is appropriate for infrastructure failures (e.g., "could not create upload directory") but means file-not-found scenarios also propagate unchecked. The `@ResponseStatus` annotation on the subclass `FileNotFoundException` compensates for this at the HTTP layer. No action needed; documented for awareness.
# Pass 4 — Code Quality: A29

## Reading Evidence

### LocalFileStorageService.java
- **Class:** `LocalFileStorageService` (extends `AbstractFileStorageService`, which implements `FileStorageService`)
- **Annotations:** `@Service("localFileStorage")`, `@Slf4j`
- **Methods:**
  - `loadImageAsResource(String fileName)` — line 16 (`@Override`)
- **Types/Constants referenced:**
  - `Resource` (org.springframework.core.io.Resource)
  - `UrlResource` (org.springframework.core.io.UrlResource)
  - `Path` (java.nio.file.Path)
  - `MalformedURLException` (java.net.MalformedURLException)
  - `FileNotFoundException` (custom, same package)
  - `FileStorageException` (custom, same package)
  - `imageStorageLocation` (inherited protected field from `AbstractFileStorageService`)

### SaveFileInfo.java
- **Class:** `SaveFileInfo` (implements `Serializable`)
- **Annotations:** `@Data`, `@Builder`
- **Methods:** None explicitly declared (Lombok generates getters, setters, equals, hashCode, toString, builder)
- **Fields/Constants:**
  - `serialVersionUID` (long) = `6183703080165788038L` — line 12
  - `fileName` (String) — line 14
  - `fileDownloadUri` (String) — line 15
  - `fileType` (String) — line 16
  - `size` (long) — line 17

### UserDetailsServiceImpl.java
- **Class:** `UserDetailsServiceImpl` (implements `UserDetailsService`)
- **Annotations:** `@Service("userDetailsService")`
- **Fields:**
  - `dao` (UserDAO) — line 23, `@Autowired`
- **Methods:**
  - `loadUserByUsername(String username)` — line 26 (`@Transactional(readOnly = true)`)
  - `buildUserFromUserEntity(User userEntity)` — line 34 (private)
- **Types/Constants referenced:**
  - `UserDAO` (com.journaldev.spring.jdbc.DAO.UserDAO)
  - `Roles` (com.journaldev.spring.jdbc.model.Roles)
  - `User` (com.journaldev.spring.jdbc.model.User)
  - `GrantedAuthority`, `SimpleGrantedAuthority` (Spring Security)
  - `UserDetails`, `UserDetailsService`, `UsernameNotFoundException` (Spring Security)
  - `DataAccessException` (org.springframework.dao)
  - `ArrayList`, `Collection` (java.util)

---

## Findings

### A29-1: Missing `@Override` on `loadUserByUsername` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java`
**Line(s):** 26
**Description:** The `loadUserByUsername` method implements the `UserDetailsService` interface but does not use the `@Override` annotation. While `@Override` is not strictly required for interface method implementations, it is a widely adopted best practice that enables compile-time verification that the method signature matches the interface contract. Every other overridden method in the audited codebase (e.g., `LocalFileStorageService.loadImageAsResource`) uses `@Override`. This is an inconsistency in annotation usage across the service layer.

### A29-2: `DataAccessException` declared in throws clause but never thrown explicitly — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java`
**Line(s):** 27
**Description:** The method signature declares `throws UsernameNotFoundException, DataAccessException`, but the `DataAccessException` is a Spring unchecked exception (extends `RuntimeException`) and does not need to be declared. The original `UserDetailsService` interface method signature only declares `throws UsernameNotFoundException`. Declaring an additional unchecked exception in the throws clause is misleading because it implies a checked exception contract. This could propagate to callers who add unnecessary try-catch blocks. While the DAO layer may indeed throw `DataAccessException` at runtime, declaring it here has no functional benefit and creates noise.

### A29-3: Hardcoded `enabled = true` bypasses potential account-disable logic — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java`
**Line(s):** 38
**Description:** In `buildUserFromUserEntity`, the `enabled` flag is hardcoded to `true` rather than being derived from the `User` entity. The `User` entity has an `active` field (used on line 42 for `accountNonLocked`), but there is no separate `enabled` field being read. This means there is no way to fully disable a user account through the `enabled` mechanism in Spring Security; the only control is via `accountNonLocked`. If the intent is to use `active` for account disabling, the semantics are inverted: `accountNonLocked` (line 42) is being used for what is typically an `enabled` check, while `enabled` is unconditionally `true`. This is a potential security concern if an admin expects "deactivating" a user to fully disable login, but the `enabled` flag still returns `true`.

### A29-4: Hardcoded `accountNonExpired` and `credentialsNonExpired` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java`
**Line(s):** 40-41
**Description:** Both `accountNonExpired` and `credentialsNonExpired` are hardcoded to `true`. These flags exist in Spring Security's `User` constructor to support account expiration and credential rotation policies. While it is common to hardcode these when such policies are not implemented, these represent dead parameters -- they are declared as local variables solely to be passed as constructor arguments. If account/credential expiration is never planned, these could be inlined directly in the constructor call (line 49) to reduce variable clutter, or alternatively a comment should explain why they are always true.

### A29-5: Fully-qualified class name used unnecessarily in method parameter and body — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java`
**Line(s):** 34, 49
**Description:** On line 34, the method parameter type is `com.journaldev.spring.jdbc.model.User` (fully qualified) even though `User` is already imported at line 5. On line 49, `org.springframework.security.core.userdetails.User` is used fully qualified. The naming collision between the domain `User` model and Spring Security's `User` class forces this pattern. However, a cleaner approach would be to alias the Spring Security class via a local variable or rename the domain model class reference. As-is, the mixed use of short and fully-qualified names within the same class reduces readability.

### A29-6: `filePath.toString()` in exception message is redundant — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/service/LocalFileStorageService.java`
**Line(s):** 24
**Description:** The call `filePath.toString()` inside the string concatenation is redundant. Java's string concatenation with `+` automatically calls `toString()` on objects. This can be simplified to just `filePath`. This is a minor style nit with no functional impact.

### A29-7: Lombok `@Builder` without `@AllArgsConstructor` may cause issues with deserialization — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/SaveFileInfo.java`
**Line(s):** 8-10
**Description:** The class uses `@Data` and `@Builder` together. `@Builder` generates an all-args constructor and makes it package-private, while `@Data` generates a no-args constructor only if no other constructors exist. Since `@Builder` creates an all-args constructor, Lombok will NOT generate a no-args constructor. This means deserialization frameworks (Jackson, etc.) that rely on a no-args constructor may fail when trying to deserialize `SaveFileInfo` objects. The class implements `Serializable`, which strongly suggests it is meant to be serialized/deserialized. Adding `@NoArgsConstructor` and `@AllArgsConstructor` alongside `@Builder` would ensure compatibility.

### A29-8: `SaveFileInfo` uses primitive `long` for `size` field — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/service/SaveFileInfo.java`
**Line(s):** 17
**Description:** The `size` field uses primitive `long` while all other fields are reference types (String). With `@Builder`, the `size` field will default to `0` if not explicitly set, which could mask missing data. Using `Long` (boxed) would allow `null` to represent "not set" and would be more consistent with the other fields. This is a minor design consideration.

### A29-9: Thread-safety concern in parent class `AbstractFileStorageService` affects `LocalFileStorageService` — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/service/LocalFileStorageService.java`
**Line(s):** 13 (class declaration, inheriting from `AbstractFileStorageService`)
**Description:** `LocalFileStorageService` is a Spring `@Service` (singleton by default) and inherits mutable instance fields from `AbstractFileStorageService`: `targetLocation` (line 36), `fileName` (line 38), and `imageExt` (line 40). These fields are written during `saveImage()` execution (lines 58, 65, 67-68 of the parent class). In a concurrent web server environment, multiple threads calling `saveImage()` simultaneously will overwrite each other's `fileName`, `targetLocation`, and `imageExt` values, leading to race conditions where files could be saved with wrong names or extensions, or one thread could return another thread's filename. These fields should be local variables within `saveImage()`, not instance fields. This is a data corruption risk under concurrent load.

### A29-10: Field injection via `@Autowired` instead of constructor injection — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java`
**Line(s):** 22-23
**Description:** The `dao` field uses field injection (`@Autowired` on a private field). Modern Spring best practice recommends constructor injection, which makes dependencies explicit, supports immutability (`final` fields), simplifies testing (no reflection needed to inject mocks), and enables compile-time dependency validation. This is a style/maintainability concern rather than a functional bug.

### A29-11: `new ArrayList<GrantedAuthority>()` uses explicit type argument — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java`
**Line(s):** 44
**Description:** The collection is instantiated as `new ArrayList<GrantedAuthority>()` rather than using the diamond operator `new ArrayList<>()`. Since Java 7+, the diamond operator is preferred as it reduces verbosity. This is a minor modernization opportunity with no functional impact.

### A29-12: Line 49 exceeds reasonable line length — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java`
**Line(s):** 49
**Description:** The Spring Security `User` construction on line 49 is a single line with 7 constructor arguments spanning well beyond 120 characters. This harms readability. The constructor call should be broken across multiple lines for clarity.
# Pass 4 — Code Quality: A30

## Reading Evidence

### Configuration.java
- **Class/Interface:** `Configuration` (public class, lines 11-43)
- **Annotations:** `@Component`, `@Getter` (Lombok)
- **Methods:** None explicitly defined; Lombok `@Getter` generates getters for all fields.
- **Fields (all `private String`, injected via `@Value`):**
  - `userSetupMsg` (line 14)
  - `userSetupSubject` (line 17)
  - `passResetSubject` (line 20)
  - `imageURL` (line 23)
  - `systemImageURL` (line 26)
  - `acceptURL` (line 29)
  - `driverRequestSubject` (line 32)
  - `cognitoAPIPort` (line 35)
  - `cognitoAPIUsername` (line 38)
  - `cognitoAPIPassword` (line 41)
- **Imports:**
  - `lombok.Getter` (line 3) -- used
  - `org.simpleframework.xml.Element` (line 4) -- **UNUSED**
  - `org.simpleframework.xml.Root` (line 5) -- **UNUSED**
  - `org.springframework.beans.factory.annotation.Value` (line 6) -- used
  - `org.springframework.stereotype.Component` (line 7) -- used

### DateUtil.java
- **Class/Interface:** `DateUtil` (public class, lines 10-77)
- **Methods:**
  - `parseDate(String, String)` -- private static, line 11
  - `formatDate(Date, String)` -- private static, line 25
  - `parseDateIso(String)` -- public static, line 35
  - `parseDateTimeIso(String)` -- public static, line 39
  - `parseDateTimeWithSlashes(String)` -- public static, line 43
  - `getStartDate(Date, String)` -- public static, line 49
  - `getCurrentDate()` -- public static, line 64
  - `getYesterdayDateString()` -- public static, line 68
  - `dateToString(Date)` -- public static, line 74
- **Types/Constants:**
  - Uses `java.text.SimpleDateFormat`, `java.util.Calendar`, `java.util.Date`
  - Uses `org.springframework.util.StringUtils`
  - Date format strings: `"yyyy-MM-dd"`, `"yyyy-MM-dd HH:mm:ss"`, `"MM/dd/yyyy HH:mm:ss"`, `"dd/MM/yyyy HH:mm:ss"`

### HttpDownloadUtility.java
- **Class/Interface:** `HttpDownloadUtility` (public class, lines 16-178)
- **Constants:**
  - `BUFFER_SIZE` = 4096 (private static final int, line 18)
- **Fields (mutable static):**
  - `saveFilePath` -- private static String, line 19
  - `fileName` -- private static String, line 20
- **Methods:**
  - `downloadFile(String, String, String)` -- public static, line 29
  - `sendPost(String, String, String)` -- public static, line 98
  - `getSaveFilePath()` -- public static, line 158
  - `setSaveFilePath(String)` -- public static, line 162
  - `getFileName()` -- public static, line 167
  - `setFileName(String)` -- public static, line 172
- **Imports:**
  - `java.io.File`, `java.io.FileOutputStream`, `java.io.IOException`, `java.io.InputStream`, `java.io.OutputStream` -- `OutputStream` is **UNUSED**
  - `java.net.HttpURLConnection`, `java.net.URL`
  - `javax.net.ssl.HttpsURLConnection` -- **UNUSED** (only referenced in commented-out code on line 102)
  - `com.journaldev.spring.jdbc.controller.RuntimeConfig` -- used
- **External dependencies:** `RuntimeConfig.APIURL`, `RuntimeConfig.file_type`, `Util.generateRadomName()`

---

## Findings

### A30-1: Hardcoded Authentication Token in Source Code -- CRITICAL
**File:** `src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java`
**Line(s):** 109
**Description:** The `sendPost` method sets a hardcoded `X-AUTH-TOKEN` header value (`"w6_zaejLjssvw02XqIiKdVmv7kP6nOHAw2Ve5mj-qug"`). Embedding secrets directly in source code is a critical security and code quality issue. This token is committed to version control and cannot be rotated without a code change and redeployment. It should be externalized to configuration (e.g., Spring `@Value` injection, environment variable, or a secrets manager).

---

### A30-2: Mutable Static Fields Cause Thread-Safety and State-Leakage Bugs -- HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java`
**Line(s):** 19-20, 52-58, 72, 130-131
**Description:** The class uses `private static String saveFilePath` and `private static String fileName` as shared mutable state across all callers. Both `downloadFile` (line 52-58, 72) and `sendPost` (line 130-131) write to these static fields. In a multi-threaded server environment (e.g., concurrent HTTP requests in a Spring application), concurrent calls will race on these fields, leading to one caller reading the file path produced by another caller. The `downloadFile` method additionally receives `fileName` as a parameter but then overwrites it with the static field (line 29 parameter shadows line 20 field, but lines 52-58 write to the parameter which is a local shadow -- however the intent to set the static field via `getSaveFilePath` at line 72 still uses the static). This design is fundamentally unsafe for concurrent use. These should be local variables or returned in a result object.

---

### A30-3: Resource Leak -- Streams Not Closed in Finally Block or Try-With-Resources -- HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java`
**Line(s):** 69-87 (downloadFile), 127-148 (sendPost)
**Description:** In both `downloadFile` and `sendPost`, `InputStream` and `FileOutputStream` are opened inside a try block but are closed with explicit `.close()` calls in the happy path only. If an exception occurs between opening and closing (e.g., during `read()` or `write()`), the streams will not be closed, resulting in file handle and connection leaks. Modern Java (7+) provides try-with-resources which guarantees cleanup. Additionally, `outputStream.close()` is called before `inputStream.close()` -- if `outputStream.close()` throws, the input stream leaks. The `OutputStream os` in `sendPost` (lines 113-116) is similarly not in a try-with-resources block.

---

### A30-4: Silent Exception Swallowing with `e.printStackTrace()` -- HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java`
**Line(s):** 84-87, 145-148
**Description:** Both `downloadFile` and `sendPost` catch `Exception` broadly and call only `e.printStackTrace()`. This swallows all exceptions silently from the caller's perspective: the method completes normally, `"File downloaded"` is printed (line 89/150), and the caller has no indication that the file write failed. The catch blocks should at minimum re-throw a meaningful exception or use a logging framework. The broad `catch (Exception e)` also catches unchecked exceptions (e.g., `NullPointerException`, `SecurityException`) that may indicate programming errors and should propagate.

---

### A30-5: `System.out.println` Used Instead of Logging Framework -- MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java`
**Line(s):** 61-64, 73, 89, 91, 120-122, 133, 150, 152
**Description:** The class uses `System.out.println` extensively for diagnostic output. In a Spring/server application, stdout output bypasses the logging framework, cannot be filtered by log level, has no timestamps or contextual metadata, and may interleave unpredictably with other output. This should use SLF4J or the project's configured logging framework. Some of these statements also print potentially sensitive information (e.g., the full POST JSON payload on line 121 with `"Post jason data : " + input`).

---

### A30-6: Unused Imports -- `org.simpleframework.xml.Element` and `org.simpleframework.xml.Root` -- MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/util/Configuration.java`
**Line(s):** 4-5
**Description:** The imports `org.simpleframework.xml.Element` and `org.simpleframework.xml.Root` are present but neither `@Element` nor `@Root` annotations appear anywhere in the class. These are likely remnants from an earlier XML serialization design. They add an unnecessary dependency on the Simple XML framework, produce compiler warnings, and clutter the code. They should be removed.

---

### A30-7: Unused Import -- `javax.net.ssl.HttpsURLConnection` -- MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java`
**Line(s):** 12
**Description:** `HttpsURLConnection` is imported but never used in active code. Its only reference is in commented-out code on line 102. This produces a compiler warning and should be removed along with the commented-out line.

---

### A30-8: Unused Import -- `java.io.OutputStream` -- LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java`
**Line(s):** 8
**Description:** `java.io.OutputStream` is imported but never used. The variable `os` on line 113 is typed as the concrete `OutputStream` returned by `getOutputStream()`, but the declared import is for the abstract class which is redundant since `FileOutputStream` (already imported) is the concrete type used elsewhere. This produces a compiler warning and should be removed.

---

### A30-9: Commented-Out Code Left in Production Source -- MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java`
**Line(s):** 42-45, 97, 102
**Description:** Several blocks of commented-out code remain:
- Lines 42-45: Commented-out debug notes (`//Content-Type = application/pdf`, etc.) that appear to be leftover from development/debugging.
- Line 97: `// HTTP POST request` -- this is a comment, not commented-out code, but line 102 is: `//	HttpsURLConnection con = (HttpsURLConnection) obj.openConnection();` -- this is commented-out code that was replaced by the `HttpURLConnection` cast on line 103. This indicates a previous HTTPS implementation was removed, which is concerning from both a code cleanliness and security perspective. Commented-out code should be removed and tracked through version control history if needed.

---

### A30-10: `parseDateTimeWithSlashes` Contains Suspicious Double-Parse Logic -- MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/util/DateUtil.java`
**Line(s):** 43-47
**Description:** The method `parseDateTimeWithSlashes` parses the input string with format `"MM/dd/yyyy HH:mm:ss"`, then immediately reformats the resulting `Date` with `"dd/MM/yyyy HH:mm:ss"`, then parses that reformatted string again. This effectively swaps the month and day fields. For example, input `"03/15/2024 10:00:00"` would parse as March 15, then reformat as `"15/03/2024 10:00:00"`, then parse that back -- but the second parse with `"dd/MM/yyyy"` would produce the same March 15 result. This means the double-parse is a no-op for valid dates where the day is <= 12 (since the swap is symmetric), but for days > 12 it still works correctly. The logic is confusing and misleading -- the intermediate format-and-reparse is unnecessary and should be simplified to a single parse. This strongly suggests a bug or a misunderstanding during development.

---

### A30-11: `SimpleDateFormat` Created Per Call -- Not Thread-Safe but Wasteful -- LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/util/DateUtil.java`
**Line(s):** 12, 26
**Description:** `SimpleDateFormat` is instantiated on every call to `parseDate` and `formatDate`. While this avoids the well-known thread-safety issue of shared `SimpleDateFormat` instances, it is unnecessarily wasteful. In modern Java (8+), `java.time.format.DateTimeFormatter` is both thread-safe and immutable, and the entire `DateUtil` class could be modernized to use `java.time` APIs (`LocalDate`, `LocalDateTime`) instead of the legacy `java.util.Date` and `Calendar` APIs.

---

### A30-12: Deprecated `StringUtils.isEmpty` Usage -- LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/util/DateUtil.java`
**Line(s):** 3, 14
**Description:** `org.springframework.util.StringUtils.isEmpty(Object)` is deprecated as of Spring Framework 5.3. The recommended replacement is `ObjectUtils.isEmpty` or `!StringUtils.hasLength(String)`. If the project uses Spring 5.3+, this will produce a deprecation warning at compile time.

---

### A30-13: Inconsistent Indentation -- Mixed Tabs and Spaces -- LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/util/Configuration.java`
**Line(s):** 13-41
**Description:** The `@Value` annotations use tab indentation while the field declarations use space indentation. For example, line 13 (`@Value`) uses a tab while line 14 (`private String userSetupMsg`) uses spaces. This inconsistency is present throughout the file and indicates no enforced code formatter. It does not affect functionality but reduces readability and produces noisy diffs.

---

### A30-14: Inconsistent Indentation and Formatting -- Mixed Tabs and Spaces -- LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java`
**Line(s):** Throughout (e.g., 23-94 vs 98-156)
**Description:** The `downloadFile` method body (lines 29-94) uses primarily space-based indentation, while `sendPost` (lines 98-156) uses tab-based indentation. The Javadoc block (lines 23-28) has no leading indentation relative to the class body. Brace placement for catch blocks is also inconsistent: `}catch(Exception e)` on line 84 vs standard style elsewhere. The file mixes multiple indentation styles throughout, suggesting code from different authors or copy-paste origins. A consistent formatter should be applied.

---

### A30-15: Cognito API Password Stored as Plaintext in Spring Configuration -- MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/util/Configuration.java`
**Line(s):** 40-41
**Description:** The `cognitoAPIPassword` field is injected via `@Value("${cognitoAPIPassword}")`. While the value itself is externalized (better than hardcoding), this design stores the Cognito API password as a plain `String` in a Spring bean that lives for the entire application lifecycle. This means the password is held in heap memory indefinitely and can appear in heap dumps, debug inspections, or actuator endpoints. Sensitive credentials should be retrieved on-demand from a secrets manager, or at minimum the property source should be encrypted (e.g., using Jasypt or Spring Cloud Vault).

---

### A30-16: `sendPost` Throws Overly Broad `throws Exception` -- LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java`
**Line(s):** 98
**Description:** The `sendPost` method declares `throws Exception`, which is the broadest possible checked exception signature. This forces callers to either catch `Exception` broadly or propagate it, losing the ability to handle specific failure modes. The method should declare specific exceptions (e.g., `throws IOException, MalformedURLException`) to communicate the actual failure modes.

---

### A30-17: Typo in Comment -- "reuqest" -- INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java`
**Line(s):** 105
**Description:** The comment reads `//add reuqest header` instead of `//add request header`. Minor typo.

---

### A30-18: Typo in Debug Output -- "jason" Instead of "JSON" -- INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java`
**Line(s):** 121
**Description:** The debug output reads `"Post jason data : "` instead of `"Post JSON data : "`. This is a typo that would appear in logs/stdout.

---

## Summary Table

| ID | Severity | File | Title |
|----|----------|------|-------|
| A30-1 | CRITICAL | HttpDownloadUtility.java | Hardcoded authentication token in source |
| A30-2 | HIGH | HttpDownloadUtility.java | Mutable static fields cause thread-safety bugs |
| A30-3 | HIGH | HttpDownloadUtility.java | Resource leak -- no try-with-resources |
| A30-4 | HIGH | HttpDownloadUtility.java | Silent exception swallowing with printStackTrace |
| A30-5 | MEDIUM | HttpDownloadUtility.java | System.out.println instead of logging framework |
| A30-6 | MEDIUM | Configuration.java | Unused imports (simpleframework.xml) |
| A30-7 | MEDIUM | HttpDownloadUtility.java | Unused import (HttpsURLConnection) |
| A30-8 | LOW | HttpDownloadUtility.java | Unused import (java.io.OutputStream) |
| A30-9 | MEDIUM | HttpDownloadUtility.java | Commented-out code in production source |
| A30-10 | MEDIUM | DateUtil.java | Suspicious double-parse logic in parseDateTimeWithSlashes |
| A30-11 | LOW | DateUtil.java | SimpleDateFormat created per call; legacy Date API |
| A30-12 | LOW | DateUtil.java | Deprecated StringUtils.isEmpty usage |
| A30-13 | LOW | Configuration.java | Inconsistent indentation (mixed tabs/spaces) |
| A30-14 | LOW | HttpDownloadUtility.java | Inconsistent indentation and formatting |
| A30-15 | MEDIUM | Configuration.java | Cognito password as plaintext String in long-lived bean |
| A30-16 | LOW | HttpDownloadUtility.java | Overly broad throws Exception |
| A30-17 | INFO | HttpDownloadUtility.java | Typo: "reuqest" |
| A30-18 | INFO | HttpDownloadUtility.java | Typo: "jason" instead of "JSON" |
# Pass 4 — Code Quality: A31

## Reading Evidence

### RuntimeConf.java
- **Class/Interface:** `RuntimeConf` (public class)
- **Methods:** None
- **Types/Constants:**
  - `public static String database` = `"jdbc/PreStartDB"` (line 4)
- **Lines of code:** 5 (lines 1-5)

### SMTPAuthenticator.java
- **Class/Interface:** `SMTPAuthenticator` extends `javax.mail.Authenticator` (public class)
- **Methods:**
  - `getPasswordAuthentication()` -> `PasswordAuthentication` (line 7)
- **Types/Constants:**
  - Local `String username` = `"AKIA**REDACTED**"` (line 9)
  - Local `String password` = `"****REDACTED****"` (line 10)
- **Imports:** `javax.mail.PasswordAuthentication` (line 3)
- **Lines of code:** 14 (lines 1-14)

### SendEmail.java
- **Class/Interface:** `SendEmail` (public class)
- **Methods:**
  - `sendMail(String subject, String msg, String mailTo)` -> `void` (static, line 14)
- **Types/Constants:** None
- **Imports:**
  - `java.util.*` (line 4)
  - `javax.mail.*` (line 6)
  - `javax.mail.internet.*` (line 7)
  - `javax.naming.Context` (line 8)
  - `javax.naming.InitialContext` (line 9)
  - `com.journaldev.spring.jdbc.controller.RuntimeConfig` (line 11)
- **Lines of code:** 57 (lines 1-57)

---

## Findings

### A31-1: Hardcoded AWS SMTP Credentials in Source Code — CRITICAL
**File:** `src/main/java/com/journaldev/spring/jdbc/util/SMTPAuthenticator.java`
**Line(s):** 9-10
**Description:** AWS AKIAJ-prefixed access key ID and secret key are hardcoded directly in the source file as plaintext strings. The username (`AKIA**REDACTED**`) follows the pattern of an AWS IAM access key and the password (`****REDACTED****`) follows the pattern of an AWS IAM secret key. Credentials committed to version control are a severe security vulnerability: they can be harvested from repository history even after removal, and they enable unauthorized access to AWS SES or other AWS services. Credentials must be externalized to environment variables, AWS Secrets Manager, SSM Parameter Store, or a JNDI resource configured in the application server.

### A31-2: SMTPAuthenticator Class Is Entirely Unused (Dead Code) — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/util/SMTPAuthenticator.java`
**Line(s):** 1-14
**Description:** A codebase-wide search for `SMTPAuthenticator` returns only its own class declaration. No other file imports or references this class. The `SendEmail` class obtains its `Session` via JNDI lookup (`envCtx.lookup("mail/Session")`) and does not use `SMTPAuthenticator` at all. This class is dead code that exists solely to hold hardcoded credentials. It should be deleted entirely, and the credentials should be rotated immediately since they have been exposed in version control history.

### A31-3: RuntimeConf Class Is Entirely Unused (Dead Code) — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/util/RuntimeConf.java`
**Line(s):** 1-5
**Description:** A codebase-wide search for `RuntimeConf` (excluding `RuntimeConfig`) returns only its own class declaration. The codebase uses `RuntimeConfig` (in the `controller` package) instead, which contains a duplicate field `production_database` with the same JNDI value `"jdbc/PreStartDB"`. This class is dead code that creates confusion with the similarly-named `RuntimeConfig`. It should be removed.

### A31-4: Confusing Naming — RuntimeConf vs. RuntimeConfig — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/util/RuntimeConf.java` and `src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java`
**Line(s):** RuntimeConf.java:3-4, RuntimeConfig.java:3,16
**Description:** Two classes with nearly identical names exist in different packages: `RuntimeConf` (in `util`) and `RuntimeConfig` (in `controller`). Both contain a JNDI database reference string with the value `"jdbc/PreStartDB"`. `RuntimeConf.database` and `RuntimeConfig.production_database` serve the same purpose. This naming collision is a maintenance hazard and a source of developer confusion. Since `RuntimeConf` is unused, the immediate remedy is to delete it. If both were in use, they should be consolidated.

### A31-5: Exception Handling Swallows Errors with Only printStackTrace — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/util/SendEmail.java`
**Line(s):** 32-34, 47-49, 50-51, 52-54
**Description:** The `sendMail` method has four exception catch blocks, and all of them handle errors by either calling `e.printStackTrace()` or `System.out.println()`. None of them rethrow, log to a proper logging framework, or return a status indicator. This means: (a) email send failures are silently lost from the caller's perspective, (b) the calling code has no way to know if the email was actually sent, and (c) stack traces go only to stdout/stderr which may not be captured in production environments. This should use a proper logging framework (e.g., SLF4J/Logback) and either rethrow a checked exception or return a boolean success indicator.

### A31-6: Catching Throwable Is Overly Broad — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/util/SendEmail.java`
**Line(s):** 52-54
**Description:** The outer try-catch catches `Throwable`, which includes `Error` subclasses such as `OutOfMemoryError` and `StackOverflowError`. Catching these is almost never appropriate because they indicate unrecoverable JVM-level problems. The catch block should be narrowed to `Exception` at most, and the caught `MessagingException` on line 50 already covers the mail-specific case.

### A31-7: Wildcard Imports — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/util/SendEmail.java`
**Line(s):** 4, 6, 7
**Description:** The file uses wildcard imports (`java.util.*`, `javax.mail.*`, `javax.mail.internet.*`). Wildcard imports reduce code clarity by making it impossible to see at a glance which specific classes are used, and they can cause ambiguous type resolution if classes with the same simple name exist in multiple imported packages. Explicit imports should be preferred.

### A31-8: Redundant Fully-Qualified Superclass in Class Declaration — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/util/SMTPAuthenticator.java`
**Line(s):** 5
**Description:** The class declaration uses `extends javax.mail.Authenticator` with a fully-qualified name, despite `javax.mail.PasswordAuthentication` being imported on line 3. The import of `javax.mail.Authenticator` is missing, so the author worked around it with inline qualification. This is a minor style inconsistency; the fix is to add `import javax.mail.Authenticator;` and use the simple name in the `extends` clause.

### A31-9: Public Mutable Static Fields Used as Configuration — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/util/RuntimeConf.java`
**Line(s):** 4
**Description:** `RuntimeConf.database` is a `public static` non-final field. Any code in the application can reassign this value at any time, creating unpredictable behavior and making the system hard to reason about. If this is intended to be a constant, it should be declared `public static final`. If it is intended to be mutable configuration, it should be accessed through a method with appropriate synchronization or encapsulated in a proper configuration management pattern. The same issue applies broadly to `RuntimeConfig` (which holds numerous public mutable static fields), but that file is outside this agent's scope.

### A31-10: Inner Exception Catch Block Masks Outer Exception Handling — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/util/SendEmail.java`
**Line(s):** 29-34
**Description:** The `setRecipients` call on line 30-31 is wrapped in its own try-catch that catches `Exception` broadly and only prints to stdout. If the recipient address is malformed, execution continues and attempts to send the message anyway (with no recipients set), which will fail at `Transport.send()` with a different error. The inner catch block should either rethrow or abort the method to avoid the cascading failure.
# Pass 4 — Code Quality: A32

## Reading Evidence

### SendMessage.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java`
- **Class:** `SendMessage` (public, non-final, no interface)
- **Fields:**
  - `logger` — `private static final Logger` (line 27)
  - `conn` — `Connection` package-private (line 29)
  - `stmt` — `Statement` package-private (line 30)
  - `rset` — `ResultSet` package-private (line 31)
  - `query` — `String` package-private (line 32)
- **Methods:**
  - `init(String msg, String mobile_no)` — public, void (line 36)
  - `send_sms_message(String msg, String mobile_no)` — private, void (line 90)
  - `readLines(String url)` — private, `String[]` (line 154)
- **Types/Constants:** Uses `RuntimeConfig.production_database`, `RuntimeConfig.LOCATION`, `RuntimeConfig.USERNAME`, `RuntimeConfig.PASSWORD`, `RuntimeConfig.API_ID`, `RuntimeConfig.SMSFROM`
- **Imports:** `java.net.URL`, `java.net.URLEncoder`, `java.sql.Connection`, `java.sql.ResultSet`, `java.sql.SQLException`, `java.sql.Statement`, `javax.naming.Context`, `javax.naming.InitialContext`, `javax.sql.DataSource`, `org.slf4j.Logger`, `org.slf4j.LoggerFactory`, `com.journaldev.spring.jdbc.controller.RuntimeConfig`, `java.io.*`, `java.util.ArrayList`, `java.util.List`

### Util.java
- **File:** `src/main/java/com/journaldev/spring/jdbc/util/Util.java`
- **Class:** `Util` (public, non-final, no interface)
- **Fields:**
  - `logger` — `private static final Logger` (line 25, never used)
- **Methods:**
  - `generateRadomName()` — public static, `String` (line 27)
  - `sendMail(String subject, String mBody, String rName, String rEmail, String sName, String sEmail, String attachment, String attachmentName)` — public static, `boolean` (line 36)
- **Types/Constants:** None beyond the logger
- **Imports:** `java.text.SimpleDateFormat`, `java.util.Calendar`, `java.util.Date`, `java.util.Properties`, `java.util.UUID`, `javax.activation.DataHandler`, `javax.activation.FileDataSource`, `javax.mail.Message`, `javax.mail.Multipart`, `javax.mail.PasswordAuthentication`, `javax.mail.Session`, `javax.mail.Transport`, `javax.mail.internet.InternetAddress`, `javax.mail.internet.MimeBodyPart`, `javax.mail.internet.MimeMessage`, `javax.mail.internet.MimeMultipart`, `org.slf4j.Logger`, `org.slf4j.LoggerFactory`

---

## Findings

### A32-1: Hardcoded AWS SES SMTP Credentials in Source Code — CRITICAL
**File:** `src/main/java/com/journaldev/spring/jdbc/util/Util.java`
**Line(s):** 65-66
**Description:** AWS SES SMTP credentials (AKIA**REDACTED** / ****REDACTED****) are hardcoded directly in the `getPasswordAuthentication()` method. This is a severe security vulnerability: credentials are exposed in version control history, cannot be rotated without a code change and redeployment, and violate every credentialing best practice. These credentials should be externalized to environment variables, AWS Secrets Manager, or Spring configuration with encrypted property support, and the existing credentials should be rotated immediately since they are already committed to the repository.

### A32-2: Hardcoded SMS API Credentials Referenced from RuntimeConfig — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java`
**Line(s):** 112
**Description:** The SMS sending URL is constructed by concatenating `RuntimeConfig.USERNAME`, `RuntimeConfig.PASSWORD`, and `RuntimeConfig.API_ID` directly into a query string. These values are hardcoded as public static fields in `RuntimeConfig.java` (lines 18-21 of that file: username="ciclickatell", password="OVLOaICXccaNUS", api_id="3629505"). Credentials in plaintext source code are a security risk. Additionally, constructing authentication URLs via string concatenation without proper encoding of all parameters is fragile.

### A32-3: sendMail Always Returns True Regardless of Outcome — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/util/Util.java`
**Line(s):** 119
**Description:** The `sendMail` method always returns `true` even when `Transport.send()` throws an exception (caught and printed at line 112-114) or when any other `Throwable` is caught (line 116-118). Callers have no way to detect mail delivery failure. The return type `boolean` implies success/failure semantics, but the method never returns `false`. This is a logic defect that silently swallows mail failures.

### A32-4: Use of Deprecated DataInputStream.readLine() — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java`
**Line(s):** 163
**Description:** `DataInputStream.readLine()` has been deprecated since JDK 1.1 because it does not properly convert bytes to characters. The Java documentation states it "does not properly convert bytes to characters." This will produce compiler deprecation warnings and may corrupt non-ASCII text. Should be replaced with `BufferedReader(new InputStreamReader(is, StandardCharsets.UTF_8))`.

### A32-5: JDBC Resources as Instance Fields Create Thread-Safety and Leak Risks — HIGH
**File:** `src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java`
**Line(s):** 29-32
**Description:** `Connection`, `Statement`, `ResultSet`, and `query` are declared as instance fields with package-private (default) access. These JDBC resources should be local variables within the `init()` method. Storing them as instance fields means: (a) the object is not thread-safe, (b) if `init()` is called multiple times on the same instance, prior resources may be leaked before being reassigned, (c) the `query` field is never used anywhere. Furthermore, `rset` is checked for null in the finally block (line 58) but is never assigned anywhere in the code, meaning that null-check is dead code.

### A32-6: Exception Handling Uses printStackTrace and System.out Instead of Logger — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java`
**Line(s):** 54, 61, 66, 71
**File:** `src/main/java/com/journaldev/spring/jdbc/util/Util.java`
**Line(s):** 81, 113, 117
**Description:** Both classes declare an SLF4J `logger` but then use `e.printStackTrace()` and `System.out.println()` for error reporting in catch blocks. This bypasses the logging framework entirely, sending output to stdout/stderr which may not be captured in production log aggregation. In `SendMessage.java`, the finally block uses `System.out.println` for three close-failure messages. In `Util.java`, `System.out.println` is used at line 81 and `e.printStackTrace()` at lines 113 and 117. All of these should use `logger.error(...)` with the exception as the second argument.

### A32-7: Wildcard Import `java.io.*` — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java`
**Line(s):** 20
**Description:** The wildcard import `java.io.*` is used instead of explicit imports. This hides the actual dependencies of the class (which are `InputStream`, `DataInputStream`, `BufferedInputStream`, and `IOException`), can cause ambiguous class resolution if multiple packages export the same name, and violates standard Java style guides. Explicit imports should be used.

### A32-8: Javadoc Comment Documents Wrong Method Signature (PHP-Style Parameters) — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java`
**Line(s):** 78-88
**Description:** The Javadoc block above `send_sms_message` uses PHP-style parameter annotations (`@param integer $id`, `@param string $mobile_no`, `@param string $event_name`, etc.) that do not correspond to the actual method parameters `(String msg, String mobile_no)`. The documentation describes 7 parameters when the method only accepts 2. This is misleading copy-paste residue from a PHP codebase and the Javadoc comment describes a completely different method ("sending out email" when it sends SMS).

### A32-9: Inconsistent Naming Conventions — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java`
**Line(s):** 36, 90, 97
**File:** `src/main/java/com/journaldev/spring/jdbc/util/Util.java`
**Line(s):** 27
**Description:** Java naming conventions are violated in multiple places. Method names use snake_case (`send_sms_message`, `init`) instead of camelCase. Parameter names use snake_case (`mobile_no`, `array_mobile_no`). The method `generateRadomName` has a typo — "Radom" should be "Random". Since this method is called externally by `HttpDownloadUtility` and `AbstractFileStorageService`, renaming it would require coordinated changes, but the typo degrades readability.

### A32-10: No Resource Cleanup in readLines on Exception — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java`
**Line(s):** 154-168
**Description:** The `readLines` method opens a URL stream and wraps it in a `DataInputStream`, but if an exception occurs between `openStream()` (line 161) and `dis.close()` (line 166), the stream is leaked. There is no try-with-resources or try/finally to ensure cleanup. Additionally, only `dis` is closed, not the underlying `is` `InputStream` — although `DataInputStream.close()` should cascade, relying on this without explicit structure is fragile.

### A32-11: Hardcoded SMTP Server Configuration — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/util/Util.java`
**Line(s):** 46-58
**Description:** The SMTP host (`email-smtp.us-east-1.amazonaws.com`), port (`465`), and all connection properties are hardcoded. This makes it impossible to change email configuration (e.g., switching regions, using a different provider, or moving to a test environment) without modifying source code and redeploying. These values should be externalized to application configuration.

### A32-12: Catching Throwable Instead of Exception — MEDIUM
**File:** `src/main/java/com/journaldev/spring/jdbc/util/Util.java`
**Line(s):** 116
**Description:** The outer catch block in `sendMail` catches `Throwable` rather than `Exception`. This will catch `Error` subclasses like `OutOfMemoryError` and `StackOverflowError`, which should generally be allowed to propagate. The catch should target `Exception` (or more specific mail-related exceptions) instead.

### A32-13: Unused Field `query` — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java`
**Line(s):** 32
**Description:** The `String query` field is declared but never assigned or read anywhere in the class. This is dead code and should be removed.

### A32-14: Unused Logger in Util.java — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/util/Util.java`
**Line(s):** 25
**Description:** The `logger` field is declared but never used in any method of `Util.java`. All error handling goes through `System.out.println` and `e.printStackTrace()` instead. Either the logger should be used (replacing the stdout/stderr calls) or removed to eliminate the dead field and its import.

### A32-15: Unused `rName` and `sName` Parameters in sendMail — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/util/Util.java`
**Line(s):** 36-37
**Description:** The `sendMail` method accepts `rName` (recipient name) and `sName` (sender name) parameters, but neither is used in the method body. The message `From` is set using only `sEmail` and the `To` is set using only `rEmail`. These unused parameters add confusion to the API and callers pass dummy values like `"unknown"`.

### A32-16: NullPointerException Risk on attachment Parameter — LOW
**File:** `src/main/java/com/journaldev/spring/jdbc/util/Util.java`
**Line(s):** 98
**Description:** The `attachment` parameter is checked using `attachment.equalsIgnoreCase("")` but if `attachment` is null, this will throw a `NullPointerException`. A null-safe check such as `attachment != null && !attachment.isEmpty()` should be used.

### A32-17: Commented-Out Code in Util.java — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/util/Util.java`
**Line(s):** 39-41
**Description:** Three lines of JNDI-based session lookup code are commented out. This appears to be a remnant of a prior implementation where the mail session was configured via the application server's JNDI context. Commented-out code should be removed; version control preserves history if it is ever needed again.

### A32-18: Inconsistent Indentation and Brace Style — INFO
**File:** `src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java`
**Line(s):** 1-169 (throughout)
**Description:** The file uses a mix of tabs and spaces for indentation, and indentation levels are inconsistent throughout. The `init` method body is indented with mixed tab widths. The `for` loop body inside `send_sms_message` (lines 105-145) has inconsistent indentation making the control flow difficult to follow — for example, the loop body statements (`to = array_mobile_no[i]` at line 108) are at the same level as the `for` statement. Brace placement also varies: Egyptian style in some places, next-line in others.
# Pass 4 — Code Quality: ACFG

## Reading Evidence

### pom.xml
- **Coordinates:** groupId=`com.collectiveintelligence`, artifactId=`fleetiq360ws`, version=`1.0.0`, packaging=`war`
- **Properties:**
  - `java-version`: 1.8
  - `org.springframework-version`: 3.2.14.RELEASE
  - `org.aspectj-version`: 1.7.4
  - `org.slf4j-version`: 1.7.5
  - `jackson.databind-version`: 2.6.7
  - `project.build.sourceEncoding`: UTF-8
  - `flyway.version`: 5.1.4
- **Profiles (4):**
  - `local` (activeByDefault=false): flyway.url=`jdbc:postgresql://127.0.0.1/PreStart` (line 27), then REDEFINED on line 30 as `jdbc:postgresql://localhost:5432/fleetiq360`; flyway.user defined twice (lines 28, 31); flyway.password defined twice (lines 29, 32); splunk.host/port defined
  - `dev` (activeByDefault=false): flyway.url to Azure host, flyway.user=`fleetiq360`, flyway.password=`fleetiq360`, tomcat.url and tomcat.server defined, splunk.host/port defined
  - `prod` (activeByDefault=false): flyway.url=`jdbc:postgresql://localhost:5432/postgres`, tomcat.url=EMPTY, flyway.user/flyway.password NOT DEFINED, splunk.host/port defined
  - `uat` (activeByDefault=**true**): flyway.url to AWS RDS, flyway.user=`dev_admin`, flyway.password=`C!1admin`, tomcat.url/tomcat.server defined, splunk.host/port defined
- **Repository:** `splunk-artifactory` at `http://splunk.jfrog.io/splunk/ext-releases-local` (HTTP, not HTTPS)
- **Dependencies (28):**
  - spring-jdbc 3.2.14.RELEASE, spring-context 3.2.14.RELEASE (excludes commons-logging), spring-webmvc 3.2.14.RELEASE
  - jackson-databind 2.6.7
  - aspectjrt 1.7.4
  - slf4j-api 1.7.5, jcl-over-slf4j 1.7.5 (runtime)
  - logback-classic 1.2.3, logback-core 1.2.3
  - javax.inject 1
  - servlet-api 2.5 (provided), jsp-api 2.1 (provided), jstl 1.2
  - commons-io 1.3.2 (org.apache.commons groupId — note: canonical groupId is `commons-io`)
  - jaxb-api 2.3.1, jaxb-core 2.3.0.1, jaxb-impl 2.3.1
  - javax.activation 1.1.1
  - javax.mail 1.4.7 (provided)
  - commons-fileupload 1.3.1
  - lombok 1.18.0
  - tika-core 1.18
  - passay 1.3.1
  - guava 27.0-jre
  - junit 4.7 (test)
  - spring-security-web **3.1.1.RELEASE**, spring-security-config **3.1.1.RELEASE** (different from spring-framework 3.2.14)
  - spring-security-oauth2 **1.0.0.RELEASE**
  - simple-xml 2.7.1
  - braintree-java 2.53.0
  - flyway-core 5.1.4
  - splunk-library-javalogging 1.6.2
  - commons-lang3 3.7
  - aws-java-sdk 1.11.163 (full SDK, not individual modules)
- **Build:**
  - finalName=`fleetiq360ws`
  - Resource filtering enabled from `environment.${env}.properties`
  - maven-eclipse-plugin 2.9
  - maven-compiler-plugin 2.5.1 (source/target 1.8, -Xlint:all, showWarnings, showDeprecation)
  - maven-war-plugin 3.2.2
  - flyway-maven-plugin 5.1.4 with embedded postgresql 9.1-901.jdbc3 dependency
  - tomcat7-maven-plugin 2.2

### settings.xml
- **Servers (2):**
  - `TomcatServerUat`: username=`maven`, password=`C!1admin`
  - `TomcatServerAzure`: username=`maven`, password=`pyx1s!96`
- Plaintext credentials committed to source control

### environment.dev.properties
- **Properties (16):**
  - imageURL: `https://forklift360.canadaeast.cloudapp.azure.com:8443/fleetiq360ws/image/`
  - systemImageURL: same as imageURL
  - uploadDir: `/var/local/pandora/upload`
  - imageDir: `image`
  - packageDir: `/var/local/pandora/apk`
  - logDir: `/var/local/pandora/logs`
  - flyway.baseline: `false`
  - flyway.enabled: `true`
  - splunk.host: `127.0.0.1`
  - splunk.port: `15000`
  - imagePrefix: `dev-`
  - cloudImagedDir: `image/`
  - bucketName: `forkliftiq360`
  - cognitoAPIPort: `9090`
  - cognitoAPIUsername: `ciiadmin`
  - cognitoAPIPassword: `ciiadmin`

### environment.prod.properties
- **Properties (16):**
  - imageURL: `https://ec2-54-86-82-22.compute-1.amazonaws.com:8443/fleetiq360ws/image/`
  - systemImageURL: same as imageURL
  - uploadDir: `/var/local/tomcat8/upload`
  - imageDir: `image`
  - packageDir: `/var/local/tomcat8/upload/apk`
  - logDir: `/var/log/pandora`
  - flyway.baseline: `false`
  - flyway.enabled: `false`
  - splunk.host: `127.0.0.1`
  - splunk.port: `15000`
  - imagePrefix: `uat-` (appears to be a copy-paste error; should likely be `prod-`)
  - cloudImagedDir: `image/`
  - bucketName: `forkliftiq360`
  - cognitoAPIPort: `9090`
  - cognitoAPIUsername: `ciiadmin`
  - cognitoAPIPassword: `ciiadmin`

### environment.uat.properties
- **Properties (16):** Byte-for-byte identical to `environment.prod.properties`
  - All values are the same including imageURL, uploadDir, packageDir, logDir, imagePrefix=`uat-`, cognitoAPIUsername, cognitoAPIPassword

### src/main/resources/fleetiq360ws.properties
- **Properties (18):** Acts as a passthrough template using Maven resource filtering `${...}` tokens
  - Hardcoded: userSetupMsg, userSetupSubject, passResetSubject, driverRequestSubject, acceptURL
  - Filtered: imageURL, systemImageURL, uploadDir, imageDir, packageDir, flyway.baseline, flyway.enabled, imagePrefix, cloudImagedDir, bucketName, cognitoAPIPort, cognitoAPIUsername, cognitoAPIPassword
  - `acceptURL` is hardcoded to `https://pandora.fleetiq360.com/pandora/acceptDriver?token=` (not environment-variable-driven)
  - `logDir` is NOT listed here (it is used by logback.xml directly from the build filter)

### src/main/resources/logback.xml
- **Appenders (2):**
  - `FILE`: RollingFileAppender, file=`${logDir}/fleetiq360ws.log`, TimeBasedRollingPolicy, pattern=`${logDir}/fleetiq360ws.%d.log`, totalSizeCap=3GB, encoder pattern=`%d%-4relative [%thread] %-5level %logger{0} - %msg%n`
  - `socket`: TcpAppender (Splunk), RemoteHost=`${splunk.host}`, Port=`${splunk.port}`, PatternLayout
- **Loggers:**
  - `com.journaldev.spring` at INFO -> FILE (line 16)
  - `com.journaldev.spring.jdbc.controller.APKUpdaterController` at **DEBUG** (line 22, comment: "Temporary enable DEBUG to resolve issue in production environment")
  - `com.journaldev.spring` at INFO with additivity=false -> socket (line 43)
- **Root loggers (2):**
  - First root (line 28): level=INFO -> FILE
  - Second root (line 47): level=INFO -> socket
- **Commented-out config:** lines 26-27 (comment about root level), line 83 of spring-security (InMemoryTokenStore)
- **Style issues:** duplicate root element definitions (logback allows this but second overrides first), inconsistent indentation, blank lines in odd places

### src/main/resources/META-INF/context.xml
- Single element: `<context antiJARLocking="true" path="/fleetiq360ws"/>`
- No JNDI DataSource `<Resource>` defined (must be at Tomcat server level)
- `antiJARLocking` is deprecated in Tomcat 8+ (removed in Tomcat 8.0.9)

### src/main/webapp/WEB-INF/web.xml
- **Servlet version:** 2.5
- **Servlet:** `appServlet` (DispatcherServlet), contextConfigLocation=`/WEB-INF/spring/appServlet/servlet-context.xml`, load-on-startup=1
- **Servlet mapping:** `appServlet` mapped to `/`
- **Context params:** contextConfigLocation=`/WEB-INF/spring/appServlet/servlet-context.xml /WEB-INF/spring/spring-security.xml`
- **Listener:** ContextLoaderListener
- **Filter:** springSecurityFilterChain (DelegatingFilterProxy), mapped to `/*`
- **Resource-ref:** `jdbc/PreStartDB`, javax.sql.DataSource, Container auth
- **Security constraint:** all URLs (`/*`), transport-guarantee=CONFIDENTIAL
- **Note:** `servlet-context.xml` is loaded BOTH by the DispatcherServlet AND by the root ContextLoaderListener context-param; this causes duplicate bean creation

### src/main/webapp/WEB-INF/spring/appServlet/servlet-context.xml
- **Namespace:** mvc, jee, beans, context
- **Property placeholder:** `classpath:fleetiq360ws.properties`
- **Annotation-driven:** enabled
- **Static resources:** `/resources/**` -> `/resources/`
- **Beans:**
  - InternalResourceViewResolver: prefix=`/WEB-INF/views/`, suffix=`.jsp`
  - RequestMappingHandlerAdapter: with jsonMessageConverter
  - MappingJackson2HttpMessageConverter (id=jsonMessageConverter)
  - CommonsMultipartResolver (id=multipartResolver): maxUploadSize=20971520 (20MB), maxInMemorySize=1048576 (1MB)
  - JndiObjectFactoryBean (id=dataSource): jndiName=`java:comp/env/jdbc/PreStartDB`
- **Component scan:** `com.journaldev.spring.jdbc`

### src/main/webapp/WEB-INF/spring/spring-security.xml
- **Schema versions:** spring-beans-3.1, spring-security-3.1, spring-security-oauth2-1.0
- **HTTP blocks:**
  - `/oauth/cache_approvals` and `/oauth/uncache_approvals`: security=none (comment: "Just for testing...")
  - `/oauth/token`: stateless, clientAuthenticationManager, BASIC_AUTH + clientCredentialsTokenEndpointFilter
  - `/rest/**`: no session, OAuth2-protected; `/rest/db/**` requires ROLE_SYS_ADMIN, `/rest/apk/**` requires ROLE_CLIENT, `/rest/**` requires ROLE_DRIVER,ROLE_COMPANY_GROUP,ROLE_SYS_ADMIN,ROLE_CLIENT
- **Authentication managers:**
  - `clientAuthenticationManager` using clientDetailsUserService
  - `authenticationManager` using userDetailsService with **password-encoder hash="md5"** (line 74)
- **Token store:** JdbcTokenStore using dataSource (commented-out InMemoryTokenStore on line 83)
- **Token services:** DefaultTokenServices, supportRefreshToken=true
- **OAuth clients (2):**
  - client-id=`987654321`, secret=`8752361E593A573E86CA558FFD39E`, access-token-validity=0 (never expires), grants=password,authorization_code,implicit
  - client-id=`fleetiq360`, secret=`rihah8eey4faibuengaixo6leiL1awii`, access-token-validity=300, refresh-token-validity=300, grants=password,authorization_code,refresh_token,implicit
- **Global method security:** pre-post-annotations enabled, proxy-target-class=true

---

## Findings

### ACFG-1: Plaintext Credentials Committed in settings.xml — CRITICAL
**File:** `settings.xml`
**Line(s):** 9, 14
**Description:** The Maven `settings.xml` file contains plaintext server passwords for `TomcatServerUat` (`C!1admin`) and `TomcatServerAzure` (`pyx1s!96`). This file is committed to source control and should not be. Maven `settings.xml` belongs in `~/.m2/settings.xml` (user home) and should never be checked into a project repository. Anyone with read access to the repository obtains deployment credentials for UAT and dev Tomcat manager endpoints.

### ACFG-2: Plaintext Database Credentials in pom.xml Profiles — CRITICAL
**File:** `pom.xml`
**Line(s):** 29, 32, 46, 76
**Description:** Flyway database passwords are hardcoded in plaintext inside Maven profiles: `gmtp-postgres` (local, line 29), `fleetiq360` (local, line 32; dev, line 46), and `C!1admin` (UAT, line 76). These credentials are committed to version control. Database credentials should be externalized to environment variables or a secrets manager and injected at build time, not stored in `pom.xml`.

### ACFG-3: Plaintext Cognito API Credentials in Environment Property Files — HIGH
**File:** `environment.dev.properties`, `environment.prod.properties`, `environment.uat.properties`
**Line(s):** 15-16 (all three files)
**Description:** All three environment property files contain `cognitoAPIUsername=ciiadmin` and `cognitoAPIPassword=ciiadmin` in plaintext. All environments use identical credentials, and the password is trivially guessable (same as username). These should be externalized via a secrets manager or environment variables, and the prod/UAT environments should use distinct, strong credentials.

### ACFG-4: OAuth Client Secrets Hardcoded in spring-security.xml — CRITICAL
**File:** `src/main/webapp/WEB-INF/spring/spring-security.xml`
**Line(s):** 113-117
**Description:** OAuth2 client secrets are hardcoded in the Spring Security configuration: client `987654321` with secret `8752361E593A573E86CA558FFD39E` and client `fleetiq360` with secret `rihah8eey4faibuengaixo6leiL1awii`. These are committed to source control. OAuth secrets should be externalized or stored in a database with hashing, not in XML config files.

### ACFG-5: MD5 Password Encoder Used for Authentication — CRITICAL
**File:** `src/main/webapp/WEB-INF/spring/spring-security.xml`
**Line(s):** 74
**Description:** The authentication manager uses `<password-encoder hash="md5"/>`. MD5 is a cryptographically broken hash function unsuitable for password storage. It is vulnerable to collision attacks, has no salting mechanism in this configuration, and can be brute-forced quickly with modern hardware. The application should use bcrypt, scrypt, or Argon2 for password hashing.

### ACFG-6: Duplicate Flyway Property Definitions in Local Profile — MEDIUM
**File:** `pom.xml`
**Line(s):** 27-32
**Description:** The `local` Maven profile defines `flyway.url`, `flyway.user`, and `flyway.password` twice. Lines 27-29 set them to `jdbc:postgresql://127.0.0.1/PreStart` with user `postgres` and password `gmtp-postgres`. Lines 30-32 redefine them to `jdbc:postgresql://localhost:5432/fleetiq360` with user `fleetiq360` and password `fleetiq360`. Maven will use the last-defined value, making the first set dead code. This is confusing and suggests an incomplete migration from a prior database (`PreStart`) to the current one (`fleetiq360`).

### ACFG-7: Prod Profile Missing flyway.user and flyway.password — MEDIUM
**File:** `pom.xml`
**Line(s):** 57-64
**Description:** The `prod` Maven profile defines `flyway.url` but omits `flyway.user` and `flyway.password`. If the Flyway migration plugin is invoked with the `prod` profile, it will use unresolved `${flyway.user}` and `${flyway.password}` properties (no default in the top-level `<properties>` block), resulting in a build failure or authentication error. Either explicitly define these properties or add a comment explaining that Flyway is not intended to run in the prod profile.

### ACFG-8: UAT Profile Is activeByDefault — Risks Accidental UAT Deployment — MEDIUM
**File:** `pom.xml`
**Line(s):** 69
**Description:** The `uat` profile has `<activeByDefault>true</activeByDefault>`. Running `mvn` without explicitly specifying a profile will use UAT settings, including the UAT database URL and credentials. This is a risk because a developer who forgets to specify `-Plocal` or `-Pdev` will inadvertently point Flyway migrations or Tomcat deployments at the UAT environment. A safer default would be `local` or no default profile, requiring explicit activation.

### ACFG-9: environment.prod.properties and environment.uat.properties Are Identical — HIGH
**File:** `environment.prod.properties`, `environment.uat.properties`
**Line(s):** All lines (1-16)
**Description:** These two files are byte-for-byte identical. Both use `imageURL` pointing to `ec2-54-86-82-22.compute-1.amazonaws.com`, the same upload/package/log paths, and critically `imagePrefix=uat-` in both files. If prod is genuinely a separate environment, this is a configuration defect: prod shares UAT infrastructure URLs, UAT image prefixes, and identical credentials. If they intentionally share infrastructure, this should be documented with a comment in each file.

### ACFG-10: Prod imagePrefix Set to "uat-" — HIGH
**File:** `environment.prod.properties`
**Line(s):** 11
**Description:** The `imagePrefix` property in the prod environment file is set to `uat-` instead of an expected `prod-` prefix. This means production-uploaded images will be prefixed with `uat-`, making them indistinguishable from UAT images in the S3 bucket (`forkliftiq360`). This is almost certainly a copy-paste error from the UAT properties file.

### ACFG-11: Splunk Repository Uses HTTP Instead of HTTPS — MEDIUM
**File:** `pom.xml`
**Line(s):** 88
**Description:** The Splunk artifact repository is configured with `http://splunk.jfrog.io/splunk/ext-releases-local` (plain HTTP). Maven dependency downloads over HTTP are vulnerable to man-in-the-middle attacks that could inject malicious artifacts. Maven 3.8.1+ blocks HTTP repositories by default. This should be changed to `https://`.

### ACFG-12: Spring Security Version Mismatch With Spring Framework — MEDIUM
**File:** `pom.xml`
**Line(s):** 12, 231, 236
**Description:** The Spring Framework version is `3.2.14.RELEASE` but Spring Security is `3.1.1.RELEASE`. The Spring Security 3.1.x line is designed for Spring Framework 3.1.x, not 3.2.x. While this may work due to backward compatibility, it is an inconsistency that can cause subtle classpath issues. Spring Security should be updated to 3.2.x to match the framework, or at minimum the version mismatch should be managed via a property variable for consistency.

### ACFG-13: OAuth2 Token Never Expires for Client 987654321 — HIGH
**File:** `src/main/webapp/WEB-INF/spring/spring-security.xml`
**Line(s):** 114
**Description:** The OAuth2 client `987654321` has `access-token-validity="0"`, which means tokens never expire. A non-expiring access token is a security risk: if a token is compromised, it remains valid indefinitely. This client also lacks a `refresh-token` grant type, meaning the only remediation for a compromised token is server-side revocation (which must be implemented manually). This should have a reasonable expiry period.

### ACFG-14: Unsecured Test Endpoints in spring-security.xml — MEDIUM
**File:** `src/main/webapp/WEB-INF/spring/spring-security.xml`
**Line(s):** 13-14
**Description:** The endpoints `/oauth/cache_approvals` and `/oauth/uncache_approvals` are configured with `security="none"` and accompanied by the comment `<!-- Just for testing... -->`. If these endpoints are present in the deployed application, they bypass all authentication and authorization. Test-only endpoints should be removed from production configuration or protected behind an admin role.

### ACFG-15: Duplicate Root Logger Definition in logback.xml — LOW
**File:** `src/main/resources/logback.xml`
**Line(s):** 28-30, 47-49
**Description:** The logback configuration defines two `<root>` elements. The first (line 28) attaches the `FILE` appender, and the second (line 47) attaches the `socket` appender. Logback processes these sequentially with the second overriding the first, so the FILE appender on the root logger is effectively discarded. If the intent is for the root logger to output to both FILE and socket, both `<appender-ref>` elements should be under a single `<root>` element. The current structure is misleading and indicates a configuration error.

### ACFG-16: Temporary DEBUG Logger Left in Production Config — LOW
**File:** `src/main/resources/logback.xml`
**Line(s):** 21-24
**Description:** A DEBUG-level logger for `com.journaldev.spring.jdbc.controller.APKUpdaterController` is explicitly left in with the comment "Temporary enable DEBUG to resolve issue in production environment." This temporary debug setting has not been reverted and will produce verbose debug output for that controller in all environments. Temporary debugging configuration should be removed after the issue is resolved.

### ACFG-17: Duplicate Logger Name in logback.xml — LOW
**File:** `src/main/resources/logback.xml`
**Line(s):** 16, 43
**Description:** The logger name `com.journaldev.spring` is defined twice: once on line 16 (level=INFO, appender=FILE) and again on line 43 (level=INFO, additivity=false, appender=socket). Logback will use the last definition, so the FILE appender assignment for this logger is silently overridden. This should be consolidated into a single logger definition with both appender-refs if both outputs are desired.

### ACFG-18: servlet-context.xml Loaded in Both Servlet and Root Application Contexts — MEDIUM
**File:** `src/main/webapp/WEB-INF/web.xml`
**Line(s):** 9, 19
**Description:** The file `servlet-context.xml` is referenced both as the DispatcherServlet's `contextConfigLocation` (line 9) and in the root context's `contextConfigLocation` (line 19). This causes all beans defined in `servlet-context.xml` (including the dataSource, component-scan, Jackson converters, multipart resolver) to be instantiated twice -- once in the root ApplicationContext and once in the servlet ApplicationContext. This wastes resources, can cause subtle bugs with singleton beans, and is a well-known Spring anti-pattern. The root context should load only shared infrastructure beans (security, data source), while the servlet context should load MVC-specific beans.

### ACFG-19: acceptURL Hardcoded to a Specific Domain — LOW
**File:** `src/main/resources/fleetiq360ws.properties`
**Line(s):** 10
**Description:** The `acceptURL` property is hardcoded to `https://pandora.fleetiq360.com/pandora/acceptDriver?token=` and is not parameterized via Maven resource filtering like other URL properties. This means the same URL is used in all environments (dev, UAT, prod). If different environments use different frontend domains, this creates a cross-environment leak where driver acceptance links in dev/UAT emails point to the production domain.

### ACFG-20: context.xml antiJARLocking Deprecated in Tomcat 8+ — LOW
**File:** `src/main/resources/META-INF/context.xml`
**Line(s):** 2
**Description:** The `antiJARLocking="true"` attribute on the `<context>` element was deprecated in Tomcat 7.0.x and removed in Tomcat 8.0.9. If the application is deployed on Tomcat 8+, this attribute is silently ignored. The attribute should be removed to avoid confusion, or replaced with the current equivalent if JAR locking avoidance is still needed.

### ACFG-21: JNDI Name "PreStartDB" Is a Legacy Artifact — LOW
**File:** `src/main/webapp/WEB-INF/web.xml` (line 30), `src/main/webapp/WEB-INF/spring/appServlet/servlet-context.xml` (line 57)
**Line(s):** web.xml:30, servlet-context.xml:57
**Description:** The JNDI DataSource name `jdbc/PreStartDB` does not correspond to the application name (`fleetiq360ws`) and is a leftover from a prior project called "PreStart" (also visible in the duplicated local profile flyway.url on pom.xml line 27). This naming inconsistency is confusing for developers joining the project and should either be renamed or documented with an explanatory comment.

### ACFG-22: aws-java-sdk Full Bundle Instead of Individual Modules — LOW
**File:** `pom.xml`
**Line(s):** 269-272
**Description:** The project depends on `com.amazonaws:aws-java-sdk:1.11.163`, which is the full AWS SDK bundle containing hundreds of service modules. The application appears to use only S3 (for image storage) and possibly Cognito. Using the full SDK greatly inflates the WAR file size. The dependency should be replaced with specific module dependencies such as `aws-java-sdk-s3` and `aws-java-sdk-cognitoidp`.

### ACFG-23: commons-io Uses Wrong GroupId — LOW
**File:** `pom.xml`
**Line(s):** 167-170
**Description:** The `commons-io` dependency uses groupId `org.apache.commons` with version `1.3.2`. The canonical groupId for Commons IO is `commons-io` (not `org.apache.commons`). While version 1.3.2 does exist under `org.apache.commons`, it is very old (2007) and the project migrated its groupId to `commons-io` starting with version 2.x. This may cause confusion or classpath conflicts if another dependency transitively pulls in `commons-io:commons-io`.

### ACFG-24: Commented-Out InMemoryTokenStore With Stale Comment — INFO
**File:** `src/main/webapp/WEB-INF/spring/spring-security.xml`
**Line(s):** 82-83
**Description:** Line 83 contains a commented-out `InMemoryTokenStore` bean with the surrounding comment (line 82) still referencing "currently an in memory implementation" despite the active configuration using `JdbcTokenStore`. This stale comment is misleading. The commented-out line and the inaccurate comment should both be removed.

### ACFG-25: Inconsistent Indentation and Formatting Across Config Files — INFO
**File:** Multiple (logback.xml, servlet-context.xml, spring-security.xml)
**Line(s):** Various
**Description:** Configuration files show inconsistent indentation styles: `logback.xml` mixes 4-space and 3-space indentation; `servlet-context.xml` mixes tabs and spaces (tab-indented bean definitions next to space-indented multipart resolver); `spring-security.xml` mixes tabs and spaces. While not functionally impactful, inconsistent formatting reduces readability and increases the chance of merge conflicts.

### ACFG-26: Flyway Plugin Depends on Obsolete PostgreSQL JDBC Driver — MEDIUM
**File:** `pom.xml`
**Line(s):** 335-338
**Description:** The Flyway Maven plugin embeds `postgresql:postgresql:9.1-901.jdbc3`, which uses the old `postgresql` groupId (replaced by `org.postgresql` since 2014) and targets JDBC 3 for PostgreSQL 9.1. This driver is severely outdated and does not support modern PostgreSQL features or security patches. If Flyway migrations run against a PostgreSQL 10+ server, there may be compatibility issues. The dependency should be updated to `org.postgresql:postgresql` with a current version.

### ACFG-27: No Default Profile Produces Build Failure Without Explicit Activation — MEDIUM
**File:** `pom.xml`
**Line(s):** 60-61
**Description:** The `prod` profile defines an empty `<tomcat.url></tomcat.url>` (line 61) and does not define `flyway.user` or `flyway.password`. If a build is executed with `-Pprod` and Flyway migration goal is triggered, it will fail due to missing credentials. The `tomcat.url` being empty means `tomcat7:deploy` will also fail. If these operations are intentionally disabled for prod, a Maven skip property or conditional execution would be clearer than empty/missing values.

---

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 4     |
| HIGH     | 3     |
| MEDIUM   | 7     |
| LOW      | 7     |
| INFO     | 2     |
| **Total**| **23**|

The most urgent issues are the plaintext credentials committed to source control (settings.xml, pom.xml profiles, environment property files, spring-security.xml) and the use of MD5 for password hashing. The configuration also exhibits signs of incomplete migration from a prior project ("PreStart"), environment property files that appear to be copy-pasted without differentiation (prod = UAT), and structural issues in the Spring context loading that cause duplicate bean instantiation.
