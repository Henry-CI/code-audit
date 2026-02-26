# Test Coverage Audit Report
**Audit Run:** 2026-02-26-01
**Agent ID:** A72
**Pass:** 2 (Test Coverage Audit)
**Date:** 2026-02-26

**Source Files Audited:**
1. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/dao/AdvertismentDAO.java`
2. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/dao/CompanyDAO.java`

**Test Directory Searched:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`

---

## Test Files Found in Test Directory

```
/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java
/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/com/calibration/UnitCalibrationTest.java
/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/com/calibration/UnitCalibratorTest.java
/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/com/util/ImpactUtilTest.java
```

Grep for `AdvertismentDAO`, `AdvertisementDAO`, and `CompanyDAO` across all test files returned **zero matches**. Neither class has any test coverage.

---

## File 1: AdvertismentDAO.java — Reading Evidence

### Class Name
`com.dao.AdvertismentDAO` (note: class name is misspelled — "Advertisment" missing the 'e' in "Advertisement")

### Fields
| Field | Line | Access |
|-------|------|--------|
| `log` | 18 | `private static Logger` |
| `instance` | 20 | `private static AdvertismentDAO` |

### Methods
| Method | Line | Access | Signature |
|--------|------|--------|-----------|
| `getInstance` | 22 | `public static` | `AdvertismentDAO getInstance()` |
| `AdvertismentDAO` (constructor) | 33 | `private` | `AdvertismentDAO()` |
| `getAllAdvertisement` | 37 | `public` | `ArrayList<AdvertisementBean> getAllAdvertisement() throws Exception` |
| `getAdvertisementById` | 77 | `public` | `ArrayList<AdvertisementBean> getAdvertisementById(String id) throws Exception` |
| `delAdvertisementById` | 119 | `public` | `Boolean delAdvertisementById(String id) throws Exception` |
| `saveAdvertisement` | 149 | `public` | `boolean saveAdvertisement(AdvertisementBean advertisementBean) throws Exception` |
| `updateAdvertisement` | 206 | `public` | `boolean updateAdvertisement(AdvertisementBean advertisementBean) throws Exception` |

---

## File 2: CompanyDAO.java — Reading Evidence

### Class Name
`com.dao.CompanyDAO`

### Fields (Constants and Instance Fields)
| Field | Line | Access |
|-------|------|--------|
| `log` | 36 | `private static Logger` |
| `QUERY_USR_RPT` | 38 | `private static final String` |
| `QUERY_USR_ALERT` | 40 | `private static final String` |
| `QUERY_ALERT_LST` | 42 | `private static final String` |
| `QUERY_REPORT_LST` | 44 | `private static final String` |
| `SAVE_USER_ROLE` | 46 | `private static final String` |
| `UPDATE_COMPANY_ROLE` | 50 | `private static final String` |
| `SAVE_COMPANY_DEALER_ROLE` | 56 | `private static final String` |
| `SAVE_USERS` | 60 | `private static final String` |
| `SAVE_COGNITO_USERS` | 63 | `private static final String` |
| `SAVE_USERS_COMP_REL` | 66 | `private static final String` |
| `SAVE_COMPANY_ROLE` | 69 | `private static final String` |
| `SAVE_COMP` | 73 | `private static final String` |
| `QUERY_SUBCOMPANYLST_BY_ID` | 75 | `private static final String` |
| `QUERY_COMPANY_BY_ID` | 81 | `private static final String` |
| `QUERY_SUBCOMPANY_BY_ID` | 87 | `private static final String` |
| `QUERY_COMPANY_USR_BY_ID` | 89 | `private static final String` |
| `UPDATE_USR_PIN` | 95 | `private static final String` |
| `UPDATE_USR_INFO` | 97 | `private static final String` |
| `UPDATE_COMPANY` | 99 | `private static final String` |
| `UPDATE_COMP_INFO_UPDATE_SETTINGS` | 101 | `private static final String` |
| `QUERY_USR_ALERT_BY_TYPE` | 103 | `private static final String` |
| `COGNITO_USERNAME_BY_ID` | 105 | `private static final String` |
| `theInstance` | 107 | `private static CompanyDAO` |
| `QUERY_COUNT_USR_ALERT_BY_TYPE` | 924 | `private static final String` |

### Methods
| Method | Line | Access | Signature |
|--------|------|--------|-----------|
| `getInstance` | 109 | `public synchronized static` | `CompanyDAO getInstance()` |
| `CompanyDAO` (constructor) | 117 | `private` | `CompanyDAO()` |
| `saveCompInfo` | 122 | `public` | `int saveCompInfo(CompanyBean compbean, String Role) throws Exception` |
| `saveUserRoles` | 153 | `public` | `void saveUserRoles(int userId, String role) throws Exception` |
| `saveSubCompInfo` | 161 | `public` | `int saveSubCompInfo(String sessCompId, CompanyBean compbean) throws Exception` |
| `getSubCompanies` | 177 | `public static` | `List<CompanyBean> getSubCompanies(String companyId) throws Exception` |
| `getSubCompanyLst` | 201 | `public` | `String getSubCompanyLst(String companyId) throws Exception` |
| `GetCompanyRoles` | 222 | `private` | `List<RoleBean> GetCompanyRoles(long companyId) throws SQLException` |
| `saveUsers` | 239 | `public` | `void saveUsers(int compId, UserBean userBean) throws Exception` |
| `savePermission` | 267 | `public` | `void savePermission(int driver_id, int compId) throws Exception` |
| `saveDefaultEmails` | 296 | `private` | `void saveDefaultEmails(int driver_id) throws Exception` |
| `saveCompanyRoles` | 328 | `private` | `void saveCompanyRoles(int companyId, String role) throws Exception` |
| `updateCompPrivacy` | 336 | `public` | `void updateCompPrivacy(String compId) throws Exception` |
| `checkExist` | 357 | `public` | `boolean checkExist(String name, String dbField, String compId) throws Exception` |
| `checkUserExit` | 382 | `public` | `int checkUserExit(String name, String dbField, String id) throws Exception` |
| `checkCompExist` | 396 | `public` | `String checkCompExist(CompanyBean companyBean) throws Exception` |
| `resetPass` | 435 | `public` | `boolean resetPass(String compId, String pass) throws Exception` |
| `getCompLogo` | 461 | `public` | `String getCompLogo(String compId) throws Exception` |
| `getCompanyById` | 488 | `public` | `CompanyBean getCompanyById(String companyId) throws Exception` |
| `getCompanyByCompId` | 521 | `public` | `List<CompanyBean> getCompanyByCompId(String id) throws SQLException` |
| `getCompanyContactsByCompId` | 558 | `public` | `List<CompanyBean> getCompanyContactsByCompId(String compId, int usrId, String sessionToken) throws SQLException` |
| `updateCompInfo` | 594 | `public` | `UserUpdateResponse updateCompInfo(CompanyBean compBean, int usrId, String accessToken) throws Exception` |
| `updateCompSettings` | 632 | `public` | `boolean updateCompSettings(CompanyBean compBean) throws Exception` |
| `getEntityComp` | 655 | `public` | `ArrayList<CompanyBean> getEntityComp(String entityId) throws Exception` |
| `getEntityByQuestion` | 690 | `public` | `ArrayList<EntityBean> getEntityByQuestion(String qId, String type) throws Exception` |
| `getAllEntity` | 722 | `public` | `ArrayList<EntityBean> getAllEntity() throws Exception` |
| `getAllCompany` | 770 | `public` | `ArrayList<CompanyBean> getAllCompany() throws SQLException` |
| `getAlertList` | 813 | `public static` | `List<AlertBean> getAlertList() throws Exception` |
| `convertCompanyToDealer` | 830 | `public` | `void convertCompanyToDealer(String companyId) throws Exception` |
| `getReportList` | 847 | `public static` | `List<AlertBean> getReportList() throws Exception` |
| `addUserSubscription` | 862 | `public static` | `void addUserSubscription(String userId, String alertId) throws Exception` |
| `deleteUserSubscription` | 871 | `public static` | `void deleteUserSubscription(String userId, String alertId) throws Exception` |
| `getUserAlert` (list overload) | 880 | `public` | `List<AlertBean> getUserAlert(String id) throws Exception` |
| `getUserAlert` (single overload) | 895 | `public` | `AlertBean getUserAlert(String id, String type, String file_name) throws SQLException` |
| `getUserReport` | 911 | `public` | `List<AlertBean> getUserReport(String id) throws Exception` |
| `checkExistingUserAlertByType` | 925 | `public` | `boolean checkExistingUserAlertByType(String userId, String type) throws Exception` |
| `getCompanyMaxId` | 933 | `public` | `int getCompanyMaxId() throws Exception` |
| `getUserMaxId` | 942 | `public` | `int getUserMaxId() throws Exception` |

---

## Findings

### AdvertismentDAO.java

---

**A72-1 | Severity: CRITICAL | Complete absence of test coverage for AdvertismentDAO**

No test class exists for `com.dao.AdvertismentDAO`. Grep across the entire test directory (`/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`) returned zero matches for both `AdvertismentDAO` and `AdvertisementDAO`. All five public methods (`getAllAdvertisement`, `getAdvertisementById`, `delAdvertisementById`, `saveAdvertisement`, `updateAdvertisement`) and the singleton accessor (`getInstance`) are entirely untested.

---

**A72-2 | Severity: CRITICAL | SQL injection via string concatenation in getAdvertisementById (line 91)**

The `id` parameter is concatenated directly into the SQL string at line 91:
```java
String sql = "select id,pic,text,order_no from advertisment where id = "+id+" order by order_no";
```
No test verifies rejection of malicious input (e.g., `id = "1 OR 1=1"`, `id = "1; DROP TABLE advertisment;--"`). A `PreparedStatement` is not used here despite one being imported. This path is entirely uncovered.

---

**A72-3 | Severity: CRITICAL | SQL injection via string concatenation in delAdvertisementById (line 131)**

The `id` parameter is concatenated directly into the SQL string at line 131:
```java
String sql = "delete from advertisment where id="+id;
```
No test exercises this method at all, and no test verifies input sanitization or rejection of crafted values.

---

**A72-4 | Severity: HIGH | No test for getAllAdvertisement returning empty result set**

When the `advertisment` table is empty, `getAllAdvertisement` returns an empty `ArrayList`. No test verifies that callers handle this empty list correctly and that the method itself returns a non-null empty collection rather than null.

---

**A72-5 | Severity: HIGH | No test for getAllAdvertisement SQLException path (line 62-66)**

The `catch(Exception e)` block at line 62 wraps any exception in a new `SQLException` and rethrows it. No test verifies that the method correctly propagates the exception, that `InfoLogger.logException` is invoked, and that connection/statement/resultset resources are still closed via the `finally` block when an exception occurs.

---

**A72-6 | Severity: HIGH | No test for getAdvertisementById with null or non-numeric id**

`getAdvertisementById(String id)` accepts an unvalidated string. Passing `null`, an empty string, or a non-numeric value will produce a malformed SQL statement and throw an exception. No test covers this defensive path.

---

**A72-7 | Severity: HIGH | No test for getAdvertisementById returning empty result set**

No test verifies the behavior when no advertisement matches the given `id`, i.e., when the method returns an empty `ArrayList`.

---

**A72-8 | Severity: HIGH | No test for delAdvertisementById — both true and false return paths**

`delAdvertisementById` returns `true` on successful update and rethrows a `SQLException` on failure. The return value of `stmt.executeUpdate()` is not checked — it always returns `true` if no exception is thrown even if zero rows were deleted. No test covers: (a) successful deletion, (b) deletion of a non-existent id (zero rows affected, returns `true` incorrectly), (c) the exception path.

---

**A72-9 | Severity: HIGH | No test for saveAdvertisement with null bean (line 163)**

The `else` branch at line 183 returns `false` when `advertisementBean` is `null`. No test verifies this null-guard short-circuit.

---

**A72-10 | Severity: HIGH | No test for saveAdvertisement when executeUpdate returns value != 1 (line 178)**

The check `if(ps.executeUpdate()!=1)` at line 178 returns `false` if the insert affects a row count other than 1. No test simulates or verifies this failure path.

---

**A72-11 | Severity: HIGH | No test for saveAdvertisement — max(order_no) is NULL on empty table (line 169)**

When the `advertisment` table is empty, `select max(order_no)+1` returns a SQL NULL. `rs.getInt(1)` returns 0 for a NULL column, leaving `order` at 0 (which is then overridden by the initialization to 1 only if rs.next() returns true with a non-null value). No test verifies the first-row insertion behavior when the table is empty, where `rs.getInt(1)` silently returns 0.

---

**A72-12 | Severity: HIGH | No test for updateAdvertisement with null bean (line 219)**

The `else` branch at line 244 returns `false` when `advertisementBean` is `null`. No test verifies this guard.

---

**A72-13 | Severity: HIGH | No test for updateAdvertisement — empty pic branch vs non-empty pic branch (lines 221-235)**

`updateAdvertisement` chooses between two different SQL statements depending on whether `advertisementBean.getPic()` is empty. No test covers either the "update without pic" path (line 223) or the "update with pic" path (line 230).

---

**A72-14 | Severity: HIGH | No test for updateAdvertisement when executeUpdate returns value != 1 (line 239)**

Same as A72-10 but for the update path: `if(ps.executeUpdate()!=1) return false`. No test verifies this failure branch.

---

**A72-15 | Severity: HIGH | NullPointerException risk in updateAdvertisement when getPic() returns null (line 221)**

`advertisementBean.getPic().equalsIgnoreCase("")` at line 221 will throw a `NullPointerException` if `getPic()` returns `null`. The catch block wraps it in a `SQLException`, but no test verifies this scenario.

---

**A72-16 | Severity: HIGH | Connection leak in saveAdvertisement when ps is null (lines 193-200)**

In the `finally` block of `saveAdvertisement`, `DBUtil.closeConnection(conn)` is only called inside the `if(null != ps)` block (lines 196-199). If an exception occurs before `ps` is initialized (e.g., during the `stmt.executeQuery` call), `conn` will never be closed. No test exercises this resource-leak path.

---

**A72-17 | Severity: MEDIUM | Singleton getInstance not tested for thread-safety correctness**

`getInstance` uses double-checked locking (lines 22-31). No test verifies that concurrent calls return the same instance and do not produce race conditions.

---

**A72-18 | Severity: MEDIUM | No test for resource cleanup in finally blocks under exception conditions**

No test for any method verifies that `rs.close()`, `stmt.close()`, and `DBUtil.closeConnection(conn)` are actually invoked when an exception is thrown during query execution.

---

**A72-19 | Severity: LOW | Class name misspelling "AdvertismentDAO" is untested as a naming contract**

The class is named `AdvertismentDAO` (missing the 'e' in "Advertisement"). No test documents or guards this spelling as an intentional contract, making future refactors error-prone.

---

**A72-20 | Severity: LOW | e.printStackTrace() called redundantly alongside InfoLogger.logException in multiple methods**

`getAdvertisementById` (line 106), `delAdvertisementById` (line 138), `saveAdvertisement` (line 190), and `updateAdvertisement` (line 251) call both `InfoLogger.logException` and `e.printStackTrace()`. No test verifies consistent logging behavior across the exception path in `getAllAdvertisement`, which omits `e.printStackTrace()` (line 64).

---

### CompanyDAO.java

---

**A72-21 | Severity: CRITICAL | Complete absence of test coverage for CompanyDAO**

No test class exists for `com.dao.CompanyDAO`. Grep across the entire test directory returned zero matches for `CompanyDAO`. All 32 public and package-accessible methods are entirely untested.

---

**A72-22 | Severity: CRITICAL | SQL injection via string concatenation in checkExist (lines 367-369)**

`dbField` and `name` are interpolated directly into a SQL string:
```java
String sql = "select id from company where " + dbField + " ='" + name + "'";
if (!compId.equalsIgnoreCase("")) {
    sql += " and id != " + compId;
}
```
`dbField` is a column name that cannot be parameterized, but `name` and `compId` should use `PreparedStatement`. No test verifies rejection of SQL metacharacters in `name` or `compId`.

---

**A72-23 | Severity: CRITICAL | SQL injection via string concatenation in checkUserExit (lines 385-387)**

```java
String sql = "select id from users where " + dbField + " ='" + name + "'";
if (!id.equalsIgnoreCase("")) {
    sql += " and id != " + id;
}
```
Same pattern as A72-22. No test exercises this method with any input, let alone adversarial input.

---

**A72-24 | Severity: CRITICAL | SQL injection via string concatenation in checkCompExist (lines 408-418)**

`companyBean.getName()`, `companyBean.getEmail()`, `companyBean.getQuestion()`, and `companyBean.getAnswer()` are all directly interpolated into SQL strings. No test covers this method.

---

**A72-25 | Severity: CRITICAL | SQL injection via string concatenation in getCompLogo (line 471)**

```java
String sql = "select logo from company where id = " + compId + "";
```
`compId` is a `String` concatenated directly. No test covers this method.

---

**A72-26 | Severity: CRITICAL | SQL injection via string concatenation in getEntityComp (lines 666-670)**

```java
String sql = "select company.id,name,email from company  left outer join comp_entity_rel ...";
if (!entityId.equalsIgnoreCase("1")) {
    sql += " where comp_entity_rel.entity_id = " + entityId;
}
```
`entityId` is concatenated without parameterization. No test covers this method.

---

**A72-27 | Severity: CRITICAL | SQL injection via string concatenation in getEntityByQuestion (line 702)**

```java
String sql = "select entity.id,name, email from entity, form_library where entity.id = form_library.lock_entity_id and question_id = " + qId + " and type= '" + type + "'";
```
Both `qId` and `type` are directly concatenated. No test covers this method.

---

**A72-28 | Severity: CRITICAL | SQL injection via nested string concatenation in getAllEntity (line 745)**

```java
sql = "select roles.id,name,description from roles,entity_role_rel where roles.id = entity_role_rel.role_id and entity_id = " + rs.getString(1);
```
The entity `id` read from the first result set is concatenated into a second SQL query inside the loop. No test covers this method.

---

**A72-29 | Severity: HIGH | getCompanyById throws unchecked IndexOutOfBoundsException when result is empty (line 518)**

`results.get(0)` at line 518 is called without checking whether `results` is empty. If no company exists for `companyId`, the query returns an empty list and this call throws `IndexOutOfBoundsException`. No test verifies behavior when company is not found.

---

**A72-30 | Severity: HIGH | No test for saveCompInfo — partial failure leaves orphaned database records**

`saveCompInfo` (lines 122-149) performs multiple database operations: insert company, assign company roles, get user max id, save users, save user roles. These are not wrapped in a single transaction. If any step after the initial company insert fails, the database is left in an inconsistent state. No test verifies transactional integrity or rollback behavior.

---

**A72-31 | Severity: HIGH | No test for saveSubCompInfo — partial failure leaves orphaned company_rel records**

`saveSubCompInfo` (lines 161-175) calls `saveCompInfo` then inserts into `company_rel` and updates `compnay_role_rel`. Not wrapped in a transaction. Failure after `saveCompInfo` returns leaves an orphaned company record with no relationship. No test covers this.

---

**A72-32 | Severity: HIGH | No test for updateCompInfo returning null when compBean is null or cognitoUsername is blank (lines 598-628)**

`updateCompInfo` returns `null` in two cases: when `compBean` is `null` (line 598 guard fails silently) and when `cognitoUsername` is blank (line 604 check). No test verifies that callers handle a `null` return from this method.

---

**A72-33 | Severity: HIGH | No test for updateCompSettings with null compBean**

`updateCompSettings` (lines 632-653) silently returns `true` when `compBean` is `null` because the `if (compBean != null)` guard at line 636 means no update occurs. No test verifies this misleading success return on null input.

---

**A72-34 | Severity: HIGH | No test for updateCompSettings when rowUpdated != 1 (line 644)**

The `if (rowUpdated != 1) return false` path is untested. No test simulates zero or multiple rows being affected by the update.

---

**A72-35 | Severity: HIGH | No test for resetPass — false return path when executeUpdate != 1 (line 448)**

`if (ps.executeUpdate() != 1) return false` at line 448 is untested. No test verifies behavior when the company ID does not exist or the update affects zero rows.

---

**A72-36 | Severity: HIGH | No test for getSubCompanyLst — NullPointerException risk when DBUtil returns null results**

`getSubCompanyLst` (lines 201-219) calls `results.add(Integer.parseInt(companyId))` at line 215 on the list returned by `DBUtil.queryForObjectsWithRowHandler`. If the handler returns null, a NPE occurs. No test verifies this path.

---

**A72-37 | Severity: HIGH | No test for convertCompanyToDealer — both branches untested (lines 831-844)**

`convertCompanyToDealer` has two branches: UPDATE when company already has ROLE_COMP authority, and INSERT when it does not. Neither branch is tested.

---

**A72-38 | Severity: HIGH | No test for getCompanyContactsByCompId when results list is empty**

`getCompanyContactsByCompId` (lines 558-592) calls `results.get(0)` at lines 583 and 584-587 inside the `if (!results.isEmpty())` block (line 576), so that is safe. However, no test verifies the empty-result path where the method returns an empty list without making Cognito calls.

---

**A72-39 | Severity: HIGH | No test for getCompanyContactsByCompId — Cognito REST call failure propagation**

Lines 582-588 make an external REST call via `RestClientService.getUser()`. No test verifies behavior when this call throws an exception, returns null, or returns a `UserResponse` with null fields.

---

**A72-40 | Severity: HIGH | No test for checkExist with empty compId (line 368)**

`checkExist` includes special handling when `compId` is empty (`""`): the additional `AND id != compId` clause is omitted. No test verifies both the empty-compId and non-empty-compId code paths.

---

**A72-41 | Severity: HIGH | No test for checkUserExit with empty id (line 386)**

Same pattern as A72-40 but for `checkUserExit`. No test covers either the empty-id or non-empty-id branch.

---

**A72-42 | Severity: HIGH | No test for getAllEntity — nested query loop correctness**

`getAllEntity` (lines 722-768) executes a nested query inside a `while(rs.next())` loop using a second `Statement stm`. No test verifies that: (a) entities with no roles have an empty role list, (b) entities with multiple roles accumulate all roles correctly, (c) the outer result set is not corrupted by the inner query sharing the same connection.

---

**A72-43 | Severity: HIGH | No test for addUserSubscription or deleteUserSubscription**

Both static methods (`addUserSubscription` at line 862, `deleteUserSubscription` at line 871) perform direct DB writes with no return value and no error-path test. No test verifies they throw on invalid input or succeed on valid input.

---

**A72-44 | Severity: HIGH | No test for getUserAlert (both overloads)**

`getUserAlert(String id)` (line 880) and `getUserAlert(String id, String type, String file_name)` (line 895) are both untested. The single-result overload returns `new AlertBean()` on no match (via `.orElse(new AlertBean())`). No test verifies callers distinguish a genuine empty result from a populated result.

---

**A72-45 | Severity: HIGH | No test for getCompanyMaxId or getUserMaxId**

`getCompanyMaxId` (line 933) and `getUserMaxId` (line 942) both query sequences and return `0` via `.orElse(0)` on failure. No test verifies that `0` is handled correctly by callers (e.g., `saveCompInfo` would attempt to insert a company with id=0).

---

**A72-46 | Severity: HIGH | No test for savePermission or saveDefaultEmails exception paths**

`savePermission` (line 267) and `saveDefaultEmails` (line 296) each wrap exceptions in `new SQLException(e.getMessage())` without calling `InfoLogger.logException`. No test verifies the exception is propagated and that resources are closed via `DbUtils.closeQuietly`.

---

**A72-47 | Severity: MEDIUM | No test for getAlertList or getReportList returning empty list**

`getAlertList` (line 813) and `getReportList` (line 847) are static methods with no tested empty-result behavior. No test verifies the returned list is non-null when the subscription table has no matching rows.

---

**A72-48 | Severity: MEDIUM | No test for getUserReport returning empty list**

`getUserReport` (line 911) delegates to `DBUtil.queryForObjects`. No test verifies empty-result behavior or exception propagation.

---

**A72-49 | Severity: MEDIUM | No test for checkExistingUserAlertByType with count = 0 vs count > 0**

`checkExistingUserAlertByType` (line 925) returns `true` when count > 0. No test verifies the `false` (count = 0) or `true` (count > 0) paths, or exception propagation when `userId` is non-numeric.

---

**A72-50 | Severity: MEDIUM | No test for getCompLogo when logo column is null (lines 474-477)**

`getCompLogo` returns an empty string `""` when `rs.getString(1)` is null (checked at line 475). No test verifies this null-logo defensive path or the no-row path (company not found returns `""`).

---

**A72-51 | Severity: MEDIUM | No test for getSubCompanies static method with non-numeric companyId**

`getSubCompanies(String companyId)` calls `Long.parseLong(companyId)` at line 181. Passing a null or non-numeric string throws `NumberFormatException`. No test verifies input validation.

---

**A72-52 | Severity: MEDIUM | No test for getCompanyByCompId when result is empty**

`getCompanyByCompId` (line 521) returns the results list directly without a `.get(0)` guard. Callers receive an empty list with no exception. No test verifies that an empty list is handled correctly by all callers.

---

**A72-53 | Severity: MEDIUM | CompanyDAO singleton not tested — getInstance not synchronized on double-check**

`getInstance` (line 109) uses `synchronized` on the entire method rather than a double-checked lock pattern. Under high concurrency, this creates a bottleneck. No test verifies concurrent instantiation returns a single instance.

---

**A72-54 | Severity: MEDIUM | SAVE_USERS SQL is entirely commented out (lines 247-254)**

```java
// DBUtil.updateObject(SAVE_USERS, stmt -> { ... });
```
The `SAVE_USERS` constant (line 60) defines an INSERT for the `users` table, but `saveUsers` (line 239) never executes it — only `SAVE_COGNITO_USERS` and `SAVE_USERS_COMP_REL` are used. No test documents or flags this intentional omission, making it indistinguishable from an accidental comment-out.

---

**A72-55 | Severity: MEDIUM | Dead field UPDATE_USR_PIN (line 95) and UPDATE_USR_INFO (line 97) and UPDATE_COMPANY (line 99) — never used in any method**

These three SQL constants are declared but not referenced in any method in the file. No test documents whether these are intentionally unused, deprecated, or accidentally orphaned.

---

**A72-56 | Severity: LOW | saveDefaultEmails is private and unreachable — no callers in scope**

`saveDefaultEmails` (line 296) is a private method. Grep of the source file shows no call to `saveDefaultEmails` within `CompanyDAO`. It is dead code. No test documents this or flags the dead code path.

---

**A72-57 | Severity: LOW | No test for getEntityByQuestion — returns only first matching row (line 705)**

`getEntityByQuestion` uses `if (rs.next())` (line 705) instead of `while (rs.next())`, meaning only the first matching entity is returned even if multiple match. No test verifies this deliberate (or erroneous) single-row behavior.

---

**A72-58 | Severity: LOW | Inconsistent exception logging — savePermission and saveDefaultEmails omit InfoLogger.logException**

`savePermission` (line 289) and `saveDefaultEmails` (line 318) catch exceptions and rethrow without calling `InfoLogger.logException`, unlike all other methods in the class. No test verifies exception logging behavior across any method.

---

**A72-59 | Severity: INFO | GetCompanyRoles method name violates Java naming convention (uppercase G) — line 222**

The private method is named `GetCompanyRoles` with an uppercase `G`, violating Java method naming conventions. No test documents this as intentional.

---

**A72-60 | Severity: INFO | saveUsers does not accept a UserBean with a null email for SAVE_COGNITO_USERS (line 242)**

`stmt.setString(2, userBean.getEmail())` at line 243 would insert a null email as the cognito username if `userBean.getEmail()` is null. No test validates input constraints on `saveUsers`.

---

## Summary

| Class | Total Public Methods | Tests Found | Coverage |
|-------|---------------------|-------------|----------|
| `AdvertismentDAO` | 5 public + 1 static accessor | 0 | 0% |
| `CompanyDAO` | 32 public/static | 0 | 0% |

| Severity | Count |
|----------|-------|
| CRITICAL | 10 |
| HIGH | 32 |
| MEDIUM | 10 |
| LOW | 5 |
| INFO | 3 |
| **Total** | **60** |
