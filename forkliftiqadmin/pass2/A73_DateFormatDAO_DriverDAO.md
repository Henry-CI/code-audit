# Pass 2 – Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A73
**Date:** 2026-02-26
**Source Files Audited:**
- `src/main/java/com/dao/DateFormatDAO.java`
- `src/main/java/com/dao/DriverDAO.java`
**Test Directory:** `src/test/java/`

---

## Test Directory Contents (complete inventory)

Only four test files exist in the entire test tree:

```
src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java
src/test/java/com/calibration/UnitCalibrationTest.java
src/test/java/com/calibration/UnitCalibratorTest.java
src/test/java/com/util/ImpactUtilTest.java
```

Grep for `DateFormatDAO` across all test files: **0 matches**
Grep for `DriverDAO` across all test files: **0 matches**

Neither class under audit has any test coverage whatsoever.

---

## File 1 – DateFormatDAO.java

**Source path:** `src/main/java/com/dao/DateFormatDAO.java`

### Reading Evidence

**Class name:** `DateFormatDAO`

**Fields:**

| Field | Line | Type |
|---|---|---|
| `log` | 12 | `private static Logger` |

**Methods:**

| Method | Line | Signature |
|---|---|---|
| `getAll` | 14 | `public static List<DateFormatBean> getAll() throws SQLException` |

**SQL used:**
- Line 15: `SELECT format_value FROM date_formats`

**Dependencies:** `DBUtil.queryForObjects`, `DateFormatBean.builder()`, `InfoLogger`, `log4j Logger`

---

## File 2 – DriverDAO.java

**Source path:** `src/main/java/com/dao/DriverDAO.java`

### Reading Evidence

**Class name:** `DriverDAO`

**Fields:**

| Field | Line | Type / Purpose |
|---|---|---|
| `log` | 35 | `private static Logger` |
| `DEFAULT_DATE_FORMAT` | 36 | `private static final String` – `"dd/mm/yyyy"` |
| `NB_DAYS_WARNING_TRAINING_EXPIRATION` | 37 | `private static final int` – `30` |
| `UPDATE_EMAIL_SUBS_INFO_SQL` | 39–40 | `private static final String` |
| `INSERT_EMAIL_SUBS_INFO_SQL` | 41–42 | `private static final String` |
| `UPDATE_ACCESS_EMAIL_SQL` | 43–44 | `private static final String` |
| `UPDATE_ACCESS_PWD_SQL` | 45–46 | `private static final String` |
| `UPDATE_ACCESS_PWD_USER_SQL` | 47–48 | `private static final String` (declared, never used in any method body) |
| `UPDATE_DRIVER_LICENSE_SQL` | 49–50 | `private static final String` |
| `UPDATE_GENERAL_INFO_SQL` | 51–52 | `private static final String` |
| `UPDATE_DRIVER_INFO_SQL` | 53–54 | `private static final String` |
| `UPDATE_USER_INFO_SQL` | 55–56 | `private static final String` (declared, never used in any method body) |
| `INSERT_DRIVER_INFO_SQL` | 57–58 | `private static final String` |
| `DELETE_DRIVER_BY_ID` | 60 | `private static final String` |
| `DELETE_USER_BY_ID` | 62 | `private static final String` |
| `DELETE_USER_COGNITO_BY_ID` | 64 | `private static final String` |
| `DELETE_USER_ROLE_REL` | 66 | `private static final String` |
| `INSERT_PERMISSION_SQL` | 68–69 | `private static final String` |
| `QUERY_USER_BY_COMP` | 71–74 | `private static final String` |
| `QUERY_DRIVER_BY_COMP` | 76–77 | `private static final String` |
| `QUERY_DRIVER_BY_NAME` | 79–83 | `private static final String` |
| `QUERY_EXPIRING_TRAININGS` | 85–95 | `private static final String` |
| `QUERY_EXPIRED_TRAININGS` | 97–107 | `private static final String` |
| `QUER_ALL_EXPIRED_TRAININGS` | 109–120 | `private static final String` |
| `QUER_EXPIRED_TRAININGS_COMPLST` | 122–133 | `private static final String` |
| `QUER_EXPIRING_TRAININGS_COMPLST` | 135–146 | `private static final String` |
| `QUERY_DRIVER_BY_LICENCE` | 149–152 | `private static final String` |
| `QUERY_DRIVER_BY_ID` | 154–157 | `private static final String` |
| `QUERY_USER_BY_ID` | 159–160 | `private static final String` |
| `QUERY_DRIVER_EMAILS_BY_DRIVER_ID` | 162 | `private static final String` |
| `QUERY_CURRENT_TIME` | 164 | `private static final String` |
| `COGNITO_USERNAME_BY_ID` | 166 | `private static final String` |
| `instance` | 168 | `private static DriverDAO` (singleton) |

**Methods:**

| Method | Line | Signature |
|---|---|---|
| `getInstance` | 170 | `public synchronized static DriverDAO getInstance()` |
| `DriverDAO` (constructor) | 176 | `private DriverDAO()` |
| `checkDriverByNm` | 179 | `public boolean checkDriverByNm(String compId, String firstName, String lastName, Long id, boolean status) throws SQLException` |
| `checkDriverByLic` | 196 | `public static boolean checkDriverByLic(String compId, String licence, Long id, boolean status) throws SQLException` |
| `getDriverByNm` | 213 | `public List<DriverBean> getDriverByNm(String compId, String firstName, String lastName, boolean status) throws Exception` |
| `getDriverByFullNm` | 252 | `public List<DriverBean> getDriverByFullNm(String compId, String fullName, boolean status) throws Exception` |
| `getAllDriver` (1-arg dateFormat omitted) | 289 | `public static List<DriverBean> getAllDriver(String compId, boolean status) throws Exception` |
| `getAllDriver` (with dateFormat) | 293 | `public static List<DriverBean> getAllDriver(String compId, boolean status, String dateFormat) throws Exception` |
| `getAllUser` | 315 | `public static List<DriverBean> getAllUser(String compId, String sessionToken) throws Exception` |
| `getAllDriverSearch` | 352 | `public static List<DriverBean> getAllDriverSearch(String compId, boolean status, String search, String dateFormat, String timezone) throws Exception` |
| `getAllUserSearch` | 391 | `public static List<DriverBean> getAllUserSearch(String compId, String search) throws Exception` |
| `getDriverById` | 419 | `public static DriverBean getDriverById(Long id) throws Exception` |
| `getUserById` | 449 | `public static DriverBean getUserById(Long id, String sessionToken) throws Exception` |
| `getSubscriptionByDriverId` | 480 | `public static EmailSubscriptionBean getSubscriptionByDriverId(Long id) throws Exception` |
| `addDriverInfo` | 502 | `public static boolean addDriverInfo(DriverBean driverbean) throws SQLException` |
| `saveDriverInfo` | 540 | `public boolean saveDriverInfo(DriverBean driverbean, String dateFormat) throws Exception` |
| `updateGeneralInfo` | 577 | `public static boolean updateGeneralInfo(DriverBean driverbean) throws SQLException` |
| `updateGeneralUserInfo` | 603 | `public static UserUpdateResponse updateGeneralUserInfo(DriverBean driverbean) throws SQLException` |
| `updateDriverLicenceInfo` | 630 | `public static boolean updateDriverLicenceInfo(LicenceBean licencebean, String dateFormat) throws SQLException` |
| `updateEmailSubsInfo` | 649 | `public static boolean updateEmailSubsInfo(EmailSubscriptionBean emailSubscriptionBean) throws Exception` |
| `delDriverById` | 690 | `public static void delDriverById(Long id, String comp_id) throws Exception` |
| `delUserById` | 702 | `public static void delUserById(Long id, String sessionToken) throws Exception` |
| `getTotalDriverByID` | 732 | `public static String getTotalDriverByID(String id, boolean status, String timezone) throws Exception` |
| `getServerTime` | 765 | `private static Timestamp getServerTime() throws Exception` |
| `getDriverName` | 773 | `public String getDriverName(Long id) throws Exception` |
| `getExpiringTrainings` (with dateFormat) | 798 | `public List<DriverTrainingBean> getExpiringTrainings(String companyId, String dateFormat) throws SQLException` |
| `getExpiringTrainings` (no dateFormat) | 813 | `public List<DriverTrainingBean> getExpiringTrainings(String companyId) throws SQLException` |
| `getExpiredTrainigs` | 828 | `public List<DriverTrainingBean> getExpiredTrainigs(String companyId) throws SQLException` |
| `getNextDriverId` | 843 | `public static Long getNextDriverId() throws SQLException` |
| `getNextUserId` | 848 | `public static Long getNextUserId() throws SQLException` |
| `saveDriverCompRel` | 853 | `private static boolean saveDriverCompRel(Connection conn, Long driverId, String compId, String dept, String loc) throws SQLException` |
| `saveDefaultEmails` | 869 | `private static boolean saveDefaultEmails(Connection conn, Long driverId) throws SQLException` |
| `getALLExpiredTrainigs` | 883 | `public static List<DriverTrainingBean> getALLExpiredTrainigs() throws SQLException` |
| `revokeDriverAccessOnTrainingExpiry` | 902 | `public static void revokeDriverAccessOnTrainingExpiry() throws SQLException` |
| `getExpiredTrainigsComp` | 920 | `public List<UserCompRelBean> getExpiredTrainigsComp() throws SQLException` |
| `getExpiringTrainigsComp` | 932 | `public List<UserCompRelBean> getExpiringTrainigsComp() throws SQLException` |

---

## Findings

### DateFormatDAO – Findings

---

**A73-1 | Severity: CRITICAL | DateFormatDAO.getAll() – zero test coverage**

`getAll()` has no test class of any kind. The method performs a database query and returns the full contents of the `date_formats` table. There are no tests for the happy path, empty result set, or `SQLException` propagation. This is a complete absence of coverage for the only public method in the class.

---

**A73-2 | Severity: HIGH | DateFormatDAO.getAll() – empty result set not tested**

When `date_formats` contains no rows, `DBUtil.queryForObjects` should return an empty list. There is no test verifying that the caller receives an empty `List<DateFormatBean>` (not null) in that scenario, and no test confirming the log message is emitted before the query.

---

**A73-3 | Severity: HIGH | DateFormatDAO.getAll() – SQLException propagation not tested**

The method signature declares `throws SQLException`. If `DBUtil.queryForObjects` throws, the exception should propagate to the caller unchanged. No test mocks a database failure to confirm this contract.

---

**A73-4 | Severity: MEDIUM | DateFormatDAO.getAll() – null or blank format_value in ResultSet not tested**

The `ResultSet` mapper calls `rs.getString("format_value")` and passes the result directly to `DateFormatBean.builder().format(...)`. No test verifies behavior when the column value is `NULL` or an empty string (which is a plausible data quality condition in this table).

---

**A73-5 | Severity: LOW | DateFormatDAO – class itself has no test class file**

Beyond individual method gaps, there is no `DateFormatDAOTest.java` file anywhere under `src/test/java/`. The class is completely outside the testing boundary established for this project.

---

### DriverDAO – Findings

---

**A73-6 | Severity: CRITICAL | DriverDAO – zero test coverage across all 33 methods**

No test file references `DriverDAO`. All 33 public and private methods, including multiple write operations, delete operations, and external Cognito service integrations, are completely untested.

---

**A73-7 | Severity: CRITICAL | DriverDAO.addDriverInfo() – transactional rollback path not tested**

`addDriverInfo` (line 502) manually manages a `Connection` with `autoCommit=false`, calls `conn.rollback()` in the `catch` block, and throws on both missing generated key (line 521) and failed sub-operations (lines 524–528). None of these rollback scenarios are covered. A bug in the rollback path could result in silent data corruption or connection leak.

---

**A73-8 | Severity: CRITICAL | DriverDAO.revokeDriverAccessOnTrainingExpiry() – silently swallows SQLException**

At line 913–916, `SQLException` thrown by `DBUtil.updateObject` inside the `forEach` lambda is caught and only printed to `e.printStackTrace()`. The caller never knows that individual driver_unit deletions failed. There is no test verifying this swallowing behaviour, and there is no test that confirms the method continues processing remaining records after one failure.

---

**A73-9 | Severity: CRITICAL | DriverDAO.getDriverById() – null id guard not tested**

Line 420 throws `NullArgumentException` when `id` is null. No test exercises this null guard path. The happy-path case where `result.isPresent()` is false (driver not found) throws `EntityNotFoundException` (line 442); this path is also untested.

---

**A73-10 | Severity: CRITICAL | DriverDAO.getUserById() – null id guard and EntityNotFoundException not tested**

Lines 450–465 mirror the same null guard and not-found pattern as `getDriverById`. Additionally, `getUserById` immediately calls `RestClientService.getUser()` after the DB lookup (line 469) without any null check on the returned `UserResponse`. If the Cognito service returns null or throws, a `NullPointerException` will propagate as an untyped `Exception`. None of these paths are tested.

---

**A73-11 | Severity: HIGH | DriverDAO.getDriverByNm() – SQL injection vector not tested**

Line 226 builds the SQL string by directly concatenating `firstName`, `lastName`, and `compId` into the query string (marked with `FIXME` comment). There is no test confirming that special characters in the name fields are handled, and no security-oriented test that verifies the injection vector fails safely. The absence of any test here means the vulnerability is entirely unconstrained.

---

**A73-12 | Severity: HIGH | DriverDAO.getDriverByFullNm() – SQL injection vector not tested**

Line 264 similarly concatenates `fullName` and `compId` directly into the SQL string (also marked `FIXME`). Same analysis as A73-11 applies; no test coverage exists.

---

**A73-13 | Severity: HIGH | DriverDAO.getTotalDriverByID() – SQL injection vector not tested**

Line 748 concatenates `id` and `timezone` directly into the SQL string without parameterisation. Although `id` is typed as `String` with no sanitisation, and `timezone` comes from an external caller. No test verifies safe handling of malformed timezone strings or non-numeric id values.

---

**A73-14 | Severity: HIGH | DriverDAO.getDriverName() – SQL injection vector not tested**

Line 783 concatenates the raw `id` (Long) into the query string. No test covers this method at all, including the empty-result case where `driverName` remains `""`.

---

**A73-15 | Severity: HIGH | DriverDAO.updateGeneralInfo() – password vs. email branching not tested**

Lines 587–598 split execution into two branches: one path issues both `UPDATE_GENERAL_INFO_SQL` and `UPDATE_ACCESS_PWD_SQL` when `driverbean.getPass()` is not blank, the other issues `UPDATE_ACCESS_EMAIL_SQL`. Neither branch is tested, nor is the cumulative `rowUpdated >= 1` return value contract verified.

---

**A73-16 | Severity: HIGH | DriverDAO.updateGeneralUserInfo() – returns null without exception when cognitoUsername is blank**

Line 610 checks `!StringUtils.isBlank(cognitoUsername)` and, if blank, falls through to `return null` at line 626 without throwing. Callers may dereference the return value without a null check. No test covers the blank-username path, the successful Cognito update path, or the path where `RestClientService.updateUser()` throws.

---

**A73-17 | Severity: HIGH | DriverDAO.delUserById() – partial failure leaves data inconsistent**

`delUserById` (line 702) performs four sequential operations: Cognito delete, `DELETE_USER_BY_ID`, `DELETE_USER_COGNITO_BY_ID`, and `DELETE_USER_ROLE_REL`, all without a wrapping transaction. If any step after the Cognito call fails, the database will be left in an inconsistent state (e.g., Cognito user deleted but DB records remain, or some DB records deleted and others not). No test exercises any of these failure paths.

---

**A73-18 | Severity: HIGH | DriverDAO.updateEmailSubsInfo() – insert vs. update branch not tested**

Lines 661–679 branch on whether a `driver_emails` record already exists (`count == 0` → INSERT, else → UPDATE). Neither branch is exercised in any test, and the `SQLException` re-throw at line 684 is also untested.

---

**A73-19 | Severity: HIGH | DriverDAO.saveDriverInfo() – id-null (INSERT) vs. id-present (UPDATE) branch not tested**

Lines 546–573 branch on `driverbean.getId() == null` to choose between INSERT and UPDATE SQL. The expiry date null/empty sub-branch (lines 562–566) inside the UPDATE path is additionally untested. No test covers any of these four code paths.

---

**A73-20 | Severity: HIGH | DriverDAO.checkDriverByNm() – dynamic SQL construction not tested**

Lines 182–183 conditionally append `and d.active = true` and `and d.id != ?` to the query, and the parameter binding at line 189–191 conditionally binds a fourth parameter only when `id != null`. All four combinations of `(status=true/false, id=null/non-null)` are untested.

---

**A73-21 | Severity: HIGH | DriverDAO.checkDriverByLic() – dynamic SQL construction not tested**

Lines 199–201 apply the same conditional append pattern as `checkDriverByNm`. Same four-combination matrix is completely untested.

---

**A73-22 | Severity: HIGH | DriverDAO.getAllDriverSearch() – search parameter branching not tested**

Lines 357–373 define three distinct code paths: `search == "current_date"` (timezone-based date filter), `search` is non-blank (ILIKE filter with five bound parameters), and `search` is blank (no filter). None of these paths are tested. The `current_date` path embeds `timezone` directly into the SQL string (line 358), an additional injection concern.

---

**A73-23 | Severity: HIGH | DriverDAO.getAllUser() – empty userRequestList branch not tested**

Lines 331–346 only invoke `RestClientService.getUserList()` when `userRequestList.size() > 0`. The branch where the list is empty (no Cognito enrichment) is untested. The Cognito error path (service throws or returns mismatched results) is also untested.

---

**A73-24 | Severity: MEDIUM | DriverDAO.getExpiringTrainings() overloaded pair – no coverage for empty result or invalid companyId**

Both overloads at lines 798 and 813 delegate to `DBUtil.queryForObjects` with `Long.parseLong(companyId)`. A non-numeric `companyId` will throw `NumberFormatException` which is not declared in the method signature. Neither the empty-list return nor the malformed ID case is tested.

---

**A73-25 | Severity: MEDIUM | DriverDAO.getExpiredTrainigs() – same issues as A73-24; note method name typo**

Line 828: method is named `getExpiredTrainigs` (missing 'n'). No test exists to flag this. Same `NumberFormatException` and empty-result gaps apply.

---

**A73-26 | Severity: MEDIUM | DriverDAO.getALLExpiredTrainigs() – method name typo and zero tests**

Line 883: named `getALLExpiredTrainigs` (missing 'n', inconsistent capitalisation). The method takes no parameters and queries all companies' expired trainings without any scope restriction. There is no test verifying what happens with an empty training table or when `DateUtil.getDateFormatFromDateTimeFormat` receives a null `rs.getString(8)` value.

---

**A73-27 | Severity: MEDIUM | DriverDAO.getInstance() – singleton pattern not tested**

Line 170: `getInstance()` uses a non-double-checked locking singleton (`synchronized` on the static method). There is no test verifying that repeated calls return the same instance, and no test for concurrency behaviour. The private constructor at line 176 is also unreachable from any test.

---

**A73-28 | Severity: MEDIUM | DriverDAO.getServerTime() – private method, null return on empty result not tested**

Line 765: `getServerTime()` returns `orElse(null)` if the DB returns no rows. The only caller is `getTotalDriverByID` (line 743), which assigns the result to `now` but then never actually uses the `now` variable before executing its own raw SQL query. This dead assignment is untested and unexplored.

---

**A73-29 | Severity: MEDIUM | DriverDAO.getSubscriptionByDriverId() – uses assert instead of thrown exception for null id**

Line 482: `assert id != null` is used for the null guard instead of an explicit `if` check with a thrown exception, meaning the guard is disabled when the JVM is run without `-ea`. No test verifies either the null-id path or the empty-result fallback (lines 494–499).

---

**A73-30 | Severity: MEDIUM | DriverDAO.delDriverById() – uses assert for null/blank guards; no test**

Lines 691–692 use `assert` for both `id != null` and `StringUtils.isNotBlank(comp_id)`. Same concern as A73-29: guards are ineffective without `-ea`. No test covers the normal delete path or the guard-violation path.

---

**A73-31 | Severity: MEDIUM | DriverDAO.getNextDriverId() and getNextUserId() – sequence exhaustion not tested**

Lines 843–851: both methods call `orElseThrow(SQLException::new)` if the sequence query returns no result (which cannot happen in normal PostgreSQL operation, but the path exists). Neither the happy path nor the exception path is tested.

---

**A73-32 | Severity: MEDIUM | DriverDAO.updateDriverLicenceInfo() – null/empty expiry date branch not tested**

Lines 636–640: the method branches on whether `licencebean.getExpiry_date()` is null or empty to decide between binding a date value or setting NULL. Neither branch is tested.

---

**A73-33 | Severity: LOW | DriverDAO – UPDATE_ACCESS_PWD_USER_SQL field (line 47) is declared but never used**

The constant `UPDATE_ACCESS_PWD_USER_SQL` is defined at line 47 (`update users set password = ? where id = ?`) but is not referenced in any method body. This dead code is untested and its presence may indicate a missing user-password-update code path.

---

**A73-34 | Severity: LOW | DriverDAO – UPDATE_USER_INFO_SQL field (line 55) is declared but never used**

The constant `UPDATE_USER_INFO_SQL` is defined at line 55 (`update users set first_name = ?,last_name = ?, mobile = ?, email = ? where id= ?`) but is not referenced in any method body. Same concern as A73-33.

---

**A73-35 | Severity: LOW | DriverDAO.addDriverInfo() – assert used as null guard for driverbean**

Line 504: `assert driverbean != null` is ineffective without `-ea`. No test passes a null `DriverBean` to verify behaviour. Same pattern as A73-29 and A73-30.

---

**A73-36 | Severity: LOW | DriverDAO.DEFAULT_DATE_FORMAT – value "dd/mm/yyyy" is incorrect for standard date formatting**

Line 36: `DEFAULT_DATE_FORMAT = "dd/mm/yyyy"` uses lowercase `mm` which conventionally represents minutes, not months. The correct month token is `MM`. No test verifies that date fields formatted with this constant actually produce correct calendar month output, meaning a month-formatting bug could exist silently across all callers of `getAllDriver(compId, status)` that rely on the default format.

---

**A73-37 | Severity: INFO | DriverDAO – no test infrastructure exists for DAO layer generally**

The four test files present in the project test only calibration and utility logic. There is no in-memory database setup (e.g., H2, Testcontainers), no mock framework configuration for `DBUtil`, and no base DAO test class. Standing up any meaningful test for either audited class would require creating this infrastructure from scratch.

---

## Coverage Summary

| Class | Methods | Methods with any test | Coverage % |
|---|---|---|---|
| DateFormatDAO | 1 public | 0 | 0% |
| DriverDAO | 33 total (28 public, 2 private, 3 private-static) | 0 | 0% |
| **Combined** | **34** | **0** | **0%** |

---

## Finding Count by Severity

| Severity | Count |
|---|---|
| CRITICAL | 5 |
| HIGH | 13 |
| MEDIUM | 10 |
| LOW | 5 |
| INFO | 1 |
| **Total** | **37** |
