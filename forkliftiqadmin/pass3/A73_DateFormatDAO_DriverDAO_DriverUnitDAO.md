# Pass 3 – Documentation Audit
**Agent:** A73
**Audit run:** 2026-02-26-01
**Files audited:**
- `src/main/java/com/dao/DateFormatDAO.java`
- `src/main/java/com/dao/DriverDAO.java`
- `src/main/java/com/dao/DriverUnitDAO.java`

---

## 1. Reading Evidence

### 1.1 DateFormatDAO.java

**Class:** `DateFormatDAO` — line 11

| Element | Kind | Type / Signature | Line |
|---------|------|-----------------|------|
| `log` | field | `static Logger` | 12 |
| `getAll()` | method | `public static List<DateFormatBean> getAll() throws SQLException` | 14 |

No class-level Javadoc. No method-level Javadoc on any member.

---

### 1.2 DriverDAO.java

**Class:** `DriverDAO` — line 34

**Fields:**

| Field | Type | Line |
|-------|------|------|
| `log` | `private static Logger` | 35 |
| `DEFAULT_DATE_FORMAT` | `private static final String` | 36 |
| `NB_DAYS_WARNING_TRAINING_EXPIRATION` | `private static final int` | 37 |
| `UPDATE_EMAIL_SUBS_INFO_SQL` | `private static final String` | 39 |
| `INSERT_EMAIL_SUBS_INFO_SQL` | `private static final String` | 41 |
| `UPDATE_ACCESS_EMAIL_SQL` | `private static final String` | 43 |
| `UPDATE_ACCESS_PWD_SQL` | `private static final String` | 45 |
| `UPDATE_ACCESS_PWD_USER_SQL` | `private static final String` | 47 |
| `UPDATE_DRIVER_LICENSE_SQL` | `private static final String` | 49 |
| `UPDATE_GENERAL_INFO_SQL` | `private static final String` | 51 |
| `UPDATE_DRIVER_INFO_SQL` | `private static final String` | 53 |
| `UPDATE_USER_INFO_SQL` | `private static final String` | 55 |
| `INSERT_DRIVER_INFO_SQL` | `private static final String` | 57 |
| `DELETE_DRIVER_BY_ID` | `private static final String` | 60 |
| `DELETE_USER_BY_ID` | `private static final String` | 62 |
| `DELETE_USER_COGNITO_BY_ID` | `private static final String` | 64 |
| `DELETE_USER_ROLE_REL` | `private static final String` | 66 |
| `INSERT_PERMISSION_SQL` | `private static final String` | 68 |
| `QUERY_USER_BY_COMP` | `private static final String` | 71 |
| `QUERY_DRIVER_BY_COMP` | `private static final String` | 76 |
| `QUERY_DRIVER_BY_NAME` | `private static final String` | 79 |
| `QUERY_EXPIRING_TRAININGS` | `private static final String` | 85 |
| `QUERY_EXPIRED_TRAININGS` | `private static final String` | 97 |
| `QUER_ALL_EXPIRED_TRAININGS` | `private static final String` | 109 |
| `QUER_EXPIRED_TRAININGS_COMPLST` | `private static final String` | 122 |
| `QUER_EXPIRING_TRAININGS_COMPLST` | `private static final String` | 135 |
| `QUERY_DRIVER_BY_LICENCE` | `private static final String` | 149 |
| `QUERY_DRIVER_BY_ID` | `private static final String` | 154 |
| `QUERY_USER_BY_ID` | `private static final String` | 159 |
| `QUERY_DRIVER_EMAILS_BY_DRIVER_ID` | `private static final String` | 162 |
| `QUERY_CURRENT_TIME` | `private static final String` | 164 |
| `COGNITO_USERNAME_BY_ID` | `private static final String` | 166 |
| `instance` | `private static DriverDAO` | 168 |

**Methods:**

| Method | Visibility | Signature | Line |
|--------|------------|-----------|------|
| `getInstance()` | `public synchronized static` | `DriverDAO getInstance()` | 170 |
| `DriverDAO()` | `private` | constructor | 176 |
| `checkDriverByNm(...)` | `public` | `boolean checkDriverByNm(String compId, String firstName, String lastName, Long id, boolean status) throws SQLException` | 179 |
| `checkDriverByLic(...)` | `public static` | `boolean checkDriverByLic(String compId, String licence, Long id, boolean status) throws SQLException` | 196 |
| `getDriverByNm(...)` | `public` | `List<DriverBean> getDriverByNm(String compId, String firstName, String lastName, boolean status) throws Exception` | 213 |
| `getDriverByFullNm(...)` | `public` | `List<DriverBean> getDriverByFullNm(String compId, String fullName, boolean status) throws Exception` | 252 |
| `getAllDriver(String, boolean)` | `public static` | `List<DriverBean> getAllDriver(String compId, boolean status) throws Exception` | 289 |
| `getAllDriver(String, boolean, String)` | `public static` | `List<DriverBean> getAllDriver(String compId, boolean status, String dateFormat) throws Exception` | 293 |
| `getAllUser(...)` | `public static` | `List<DriverBean> getAllUser(String compId, String sessionToken) throws Exception` | 315 |
| `getAllDriverSearch(...)` | `public static` | `List<DriverBean> getAllDriverSearch(String compId, boolean status, String search, String dateFormat, String timezone) throws Exception` | 352 |
| `getAllUserSearch(...)` | `public static` | `List<DriverBean> getAllUserSearch(String compId, String search) throws Exception` | 391 |
| `getDriverById(...)` | `public static` | `DriverBean getDriverById(Long id) throws Exception` | 419 |
| `getUserById(...)` | `public static` | `DriverBean getUserById(Long id, String sessionToken) throws Exception` | 449 |
| `getSubscriptionByDriverId(...)` | `public static` | `EmailSubscriptionBean getSubscriptionByDriverId(Long id) throws Exception` | 480 |
| `addDriverInfo(...)` | `public static` | `boolean addDriverInfo(DriverBean driverbean) throws SQLException` | 502 |
| `saveDriverInfo(...)` | `public` | `boolean saveDriverInfo(DriverBean driverbean, String dateFormat) throws Exception` | 540 |
| `updateGeneralInfo(...)` | `public static` | `boolean updateGeneralInfo(DriverBean driverbean) throws SQLException` | 577 |
| `updateGeneralUserInfo(...)` | `public static` | `UserUpdateResponse updateGeneralUserInfo(DriverBean driverbean) throws SQLException` | 603 |
| `updateDriverLicenceInfo(...)` | `public static` | `boolean updateDriverLicenceInfo(LicenceBean licencebean, String dateFormat) throws SQLException` | 630 |
| `updateEmailSubsInfo(...)` | `public static` | `boolean updateEmailSubsInfo(EmailSubscriptionBean emailSubscriptionBean) throws Exception` | 649 |
| `delDriverById(...)` | `public static` | `void delDriverById(Long id, String comp_id) throws Exception` | 690 |
| `delUserById(...)` | `public static` | `void delUserById(Long id, String sessionToken) throws Exception` | 702 |
| `getTotalDriverByID(...)` | `public static` | `String getTotalDriverByID(String id, boolean status, String timezone) throws Exception` | 732 |
| `getServerTime()` | `private static` | `Timestamp getServerTime() throws Exception` | 765 |
| `getDriverName(...)` | `public` | `String getDriverName(Long id) throws Exception` | 773 |
| `getExpiringTrainings(String, String)` | `public` | `List<DriverTrainingBean> getExpiringTrainings(String companyId, String dateFormat) throws SQLException` | 798 |
| `getExpiringTrainings(String)` | `public` | `List<DriverTrainingBean> getExpiringTrainings(String companyId) throws SQLException` | 813 |
| `getExpiredTrainigs(String)` | `public` | `List<DriverTrainingBean> getExpiredTrainigs(String companyId) throws SQLException` | 828 |
| `getNextDriverId()` | `public static` | `Long getNextDriverId() throws SQLException` | 843 |
| `getNextUserId()` | `public static` | `Long getNextUserId() throws SQLException` | 848 |
| `saveDriverCompRel(...)` | `private static` | `boolean saveDriverCompRel(Connection conn, Long driverId, String compId, String dept, String loc) throws SQLException` | 853 |
| `saveDefaultEmails(...)` | `private static` | `boolean saveDefaultEmails(Connection conn, Long driverId) throws SQLException` | 869 |
| `getALLExpiredTrainigs()` | `public static` | `List<DriverTrainingBean> getALLExpiredTrainigs() throws SQLException` | 883 |
| `revokeDriverAccessOnTrainingExpiry()` | `public static` | `void revokeDriverAccessOnTrainingExpiry() throws SQLException` | 902 |
| `getExpiredTrainigsComp()` | `public` | `List<UserCompRelBean> getExpiredTrainigsComp() throws SQLException` | 920 |
| `getExpiringTrainigsComp()` | `public` | `List<UserCompRelBean> getExpiringTrainigsComp() throws SQLException` | 932 |

No class-level Javadoc. No method-level Javadoc on any member.

---

### 1.3 DriverUnitDAO.java

**Class:** `DriverUnitDAO` — line 11

**Fields:**

| Field | Type | Line |
|-------|------|------|
| `QUERY_DRIVER_UNITS_BY_DRIVER_ID` | `private static final String` | 12 |
| `QUERY_UNITS_ASSIGNED` | `private static final String` | 13 |
| `UNASSIGN_DRIVER_UNIT` | `private static final String` | 14 |
| `ASSIGN_DRIVER_UNIT` | `private static final String` | 15 |
| `instance` | `private static DriverUnitDAO` | 17 |

**Methods:**

| Method | Visibility | Signature | Line |
|--------|------------|-----------|------|
| `getInstance()` | `public static` | `DriverUnitDAO getInstance()` | 19 |
| `DriverUnitDAO()` | `private` | constructor | 30 |
| `getDriverUnitsByCompAndDriver(...)` | `public static` | `List<DriverUnitBean> getDriverUnitsByCompAndDriver(Long compId, Long driverId) throws SQLException` | 33 |
| `saveDriverVehicle(...)` | `public` | `void saveDriverVehicle(DriverVehicleBean driverVehicle) throws SQLException` | 49 |

No class-level Javadoc. No method-level Javadoc on any member.

---

## 2. Findings

### A73-1 — No class-level Javadoc: DateFormatDAO
**Severity:** LOW
**File:** `DateFormatDAO.java`, line 11
**Description:** `DateFormatDAO` has no class-level Javadoc comment. There is no `/** ... */` block preceding the class declaration.

---

### A73-2 — Undocumented non-trivial public method: DateFormatDAO.getAll()
**Severity:** MEDIUM
**File:** `DateFormatDAO.java`, line 14
**Description:** `public static List<DateFormatBean> getAll() throws SQLException` has no Javadoc. The method executes a database query against `date_formats`, maps results to `DateFormatBean` objects, and propagates `SQLException`. This is non-trivial behaviour (DB interaction, exception contract) that warrants documentation. No `@return` or `@throws` tags are present.

---

### A73-3 — No class-level Javadoc: DriverDAO
**Severity:** LOW
**File:** `DriverDAO.java`, line 34
**Description:** `DriverDAO` has no class-level Javadoc. The class is large (944 lines), manages both the legacy `driver` table and the Cognito-backed `users` table, and implements a singleton. The absence of any class-level overview significantly hinders understanding of its dual responsibility.

---

### A73-4 — Undocumented non-trivial public method: DriverDAO.getInstance()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 170
**Description:** `public synchronized static DriverDAO getInstance()` has no Javadoc. This is the singleton accessor; the synchronization contract and the fact that the returned instance is a shared singleton are not documented. No `@return` tag.

---

### A73-5 — Undocumented non-trivial public method: DriverDAO.checkDriverByNm()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 179
**Description:** `public boolean checkDriverByNm(String compId, String firstName, String lastName, Long id, boolean status)` has no Javadoc. The semantics of `id` (used to exclude a specific driver — i.e. for duplicate checking during edit) and `status` (restricts to active drivers when `true`) are non-obvious. No `@param` or `@return` tags.

---

### A73-6 — Undocumented non-trivial public method: DriverDAO.checkDriverByLic()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 196
**Description:** `public static boolean checkDriverByLic(String compId, String licence, Long id, boolean status)` has no Javadoc. Same concerns as A73-5: `id` (nullable exclusion ID) and `status` are undocumented. No `@param` or `@return` tags.

---

### A73-7 — Undocumented non-trivial public method: DriverDAO.getDriverByNm()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 213
**Description:** `public List<DriverBean> getDriverByNm(String compId, String firstName, String lastName, boolean status)` has no Javadoc. Notably this method contains an inline `FIXME` comment on line 225 acknowledging a SQL injection vulnerability via string concatenation. The method returns at most one result despite the `List` return type (only one `rs.next()` call, not a loop), which is a behaviour that particularly needs documentation. No `@param`, `@return`, or `@throws` tags.

---

### A73-8 — Undocumented non-trivial public method: DriverDAO.getDriverByFullNm()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 252
**Description:** `public List<DriverBean> getDriverByFullNm(String compId, String fullName, boolean status)` has no Javadoc. Contains an inline `FIXME` comment on line 263 flagging SQL injection via string concatenation. Like `getDriverByNm`, the result list is populated via a single `rs.next()` call (not a loop), so at most one record is returned — a surprising contract for a `List<DriverBean>` return type. No `@param`, `@return`, or `@throws` tags.

---

### A73-9 — Undocumented non-trivial public method: DriverDAO.getAllDriver() (both overloads)
**Severity:** MEDIUM
**File:** `DriverDAO.java`, lines 289 and 293
**Description:** Both overloads of `public static List<DriverBean> getAllDriver(...)` lack Javadoc. The two-argument overload delegates to the three-argument overload using `DEFAULT_DATE_FORMAT` ("dd/mm/yyyy"); this delegation and the default format value are not documented. The `dateFormat` parameter contract (expected pattern string) is undocumented. No `@param` or `@return` tags on either overload.

---

### A73-10 — Undocumented non-trivial public method: DriverDAO.getAllUser()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 315
**Description:** `public static List<DriverBean> getAllUser(String compId, String sessionToken)` has no Javadoc. The method performs a two-phase operation: first queries local DB for Cognito usernames, then calls an external REST service to enrich each record with profile data. This integration behaviour is non-trivial. The `sessionToken` parameter purpose and the side-effect of enrichment are undocumented. No `@param` or `@return` tags.

---

### A73-11 — Undocumented non-trivial public method: DriverDAO.getAllDriverSearch()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 352
**Description:** `public static List<DriverBean> getAllDriverSearch(String compId, boolean status, String search, String dateFormat, String timezone)` has no Javadoc. The `search` parameter has a special sentinel value `"current_date"` that triggers timezone-aware date filtering instead of a text search — a non-obvious contract. No `@param` or `@return` tags.

---

### A73-12 — Undocumented non-trivial public method: DriverDAO.getAllUserSearch()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 391
**Description:** `public static List<DriverBean> getAllUserSearch(String compId, String search)` has no Javadoc. The SQL query appended in the search branch references columns `d.first_name`, `d.last_name`, `d.email`, `d.mobile` (line 396) but the base query `QUERY_USER_BY_COMP` (line 71) joins `user_comp_rel` and `users_cognito` — these columns do not exist in those tables, indicating likely dead/broken code, but regardless there is no documentation. No `@param` or `@return` tags.

---

### A73-13 — Undocumented non-trivial public method: DriverDAO.getDriverById()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 419
**Description:** `public static DriverBean getDriverById(Long id)` has no Javadoc. The method throws `EntityNotFoundException` (an unchecked exception, not declared in the `throws` clause) when no record is found, and maps password column index 9 to both `cpass` and `pass` fields with a literal `'******'` mask. These contracts are undocumented. No `@param`, `@return`, or `@throws` tags.

---

### A73-14 — Undocumented non-trivial public method: DriverDAO.getUserById()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 449
**Description:** `public static DriverBean getUserById(Long id, String sessionToken)` has no Javadoc. Performs a DB lookup then enriches the result via an external Cognito REST call using `sessionToken`. Throws `EntityNotFoundException` when not found (undeclared unchecked). No `@param`, `@return`, or `@throws` tags.

---

### A73-15 — Undocumented non-trivial public method: DriverDAO.getSubscriptionByDriverId()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 480
**Description:** `public static EmailSubscriptionBean getSubscriptionByDriverId(Long id)` has no Javadoc. Notably returns a non-null default `EmailSubscriptionBean` with empty strings when no record exists (rather than returning `null` or throwing). This "null-object" contract is important to document. No `@param` or `@return` tags.

---

### A73-16 — Undocumented non-trivial public method: DriverDAO.addDriverInfo()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 502
**Description:** `public static boolean addDriverInfo(DriverBean driverbean)` has no Javadoc. The method performs a multi-step transactional insert (driver row, permission/company-relation row, default email subscription row) and mutates the input bean by setting the generated `id`. Mutating the input parameter is undocumented. No `@param` or `@return` tags.

---

### A73-17 — Undocumented non-trivial public method: DriverDAO.saveDriverInfo()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 540
**Description:** `public boolean saveDriverInfo(DriverBean driverbean, String dateFormat)` has no Javadoc. The method performs either an INSERT (when `driverbean.getId() == null`) or an UPDATE, determined at runtime by the presence of an ID — a branching contract that is entirely undocumented. No `@param` or `@return` tags.

---

### A73-18 — Undocumented non-trivial public method: DriverDAO.updateGeneralInfo()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 577
**Description:** `public static boolean updateGeneralInfo(DriverBean driverbean)` has no Javadoc. The method conditionally updates either email+password or email-only depending on whether `driverbean.getPass()` is blank — this conditional write behaviour is undocumented. No `@param` or `@return` tags.

---

### A73-19 — Undocumented non-trivial public method: DriverDAO.updateGeneralUserInfo()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 603
**Description:** `public static UserUpdateResponse updateGeneralUserInfo(DriverBean driverbean)` has no Javadoc. The method returns `null` when no Cognito username is found for the given driver (line 626) — a silent no-op that callers must handle. It also applies password update conditionally based on `pass_hash` (line 620), while using `pass` for the actual value — an inconsistency with no documentation. No `@param` or `@return` tags.

---

### A73-20 — Undocumented non-trivial public method: DriverDAO.updateDriverLicenceInfo()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 630
**Description:** `public static boolean updateDriverLicenceInfo(LicenceBean licencebean, String dateFormat)` has no Javadoc. No `@param` or `@return` tags.

---

### A73-21 — Undocumented non-trivial public method: DriverDAO.updateEmailSubsInfo()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 649
**Description:** `public static boolean updateEmailSubsInfo(EmailSubscriptionBean emailSubscriptionBean)` has no Javadoc. The method performs a "upsert" by first counting existing rows and branching to INSERT or UPDATE — this transaction pattern is undocumented. No `@param` or `@return` tags.

---

### A73-22 — Undocumented non-trivial public method: DriverDAO.delDriverById()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 690
**Description:** `public static void delDriverById(Long id, String comp_id)` has no Javadoc. The SQL constant `DELETE_DRIVER_BY_ID` (line 60) performs a soft-delete (`update permission set enabled = false`) — the method name "del" strongly implies a hard delete. This behavioural mismatch is undocumented and potentially misleading to callers. No `@param` tags.

---

### A73-23 — Inaccurate method name / undocumented behaviour: DriverDAO.delDriverById()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 690
**Description:** The method is named `delDriverById` but executes `UPDATE permission SET enabled = false WHERE driver_id = ? AND comp_id = ?`. This is a soft-disable of a permission record, not a deletion of a driver. The absence of Javadoc means callers reading only the method name will incorrectly assume the driver record is removed from the database.

---

### A73-24 — Undocumented non-trivial public method: DriverDAO.delUserById()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 702
**Description:** `public static void delUserById(Long id, String sessionToken)` has no Javadoc. The method performs multiple coordinated operations: Cognito user deletion via REST, soft-deletion of the `users` row (`active = false`), hard-deletion from `users_cognito`, and hard-deletion from `user_role_rel`. This mix of soft and hard deletes in a single method is a significant contract that is entirely undocumented. No `@param` tags.

---

### A73-25 — Undocumented non-trivial public method: DriverDAO.getTotalDriverByID()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 732
**Description:** `public static String getTotalDriverByID(String id, boolean status, String timezone)` has no Javadoc. The method returns a count as a raw `String` (not numeric), calls `getServerTime()` but does not use the result (lines 743–744 — dead code), and uses direct string interpolation of `id` and `timezone` in SQL (lines 748–749), which is a SQL injection risk. None of these behaviours are documented. No `@param` or `@return` tags.

---

### A73-26 — Undocumented non-trivial public method: DriverDAO.getDriverName()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 773
**Description:** `public String getDriverName(Long id)` has no Javadoc. Concatenates `id` directly into SQL (line 783) — SQL injection risk. Returns an empty string when no driver is found rather than `null` or throwing. No `@param` or `@return` tags.

---

### A73-27 — Undocumented non-trivial public method: DriverDAO.getExpiringTrainings() (both overloads)
**Severity:** MEDIUM
**File:** `DriverDAO.java`, lines 798 and 813
**Description:** Both overloads of `public List<DriverTrainingBean> getExpiringTrainings(String companyId, ...)` lack Javadoc. "Expiring" is defined by `NB_DAYS_WARNING_TRAINING_EXPIRATION` (30 days), and the no-`dateFormat` overload derives the date format from column 8 of the result set. Neither overload documents what "expiring" means, which query constant is used, or the date-format derivation difference. No `@param` or `@return` tags on either overload.

---

### A73-28 — Undocumented non-trivial public method: DriverDAO.getExpiredTrainigs()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 828
**Description:** `public List<DriverTrainingBean> getExpiredTrainigs(String companyId)` has no Javadoc. Method name contains a typo ("Trainigs" instead of "Trainings"). No `@param` or `@return` tags.

---

### A73-29 — Undocumented non-trivial public method: DriverDAO.getNextDriverId()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 843
**Description:** `public static Long getNextDriverId()` has no Javadoc. Advances `driver_id_seq` sequence — calling this has a persistent side-effect (sequence cannot be rolled back). No `@return` tag.

---

### A73-30 — Undocumented non-trivial public method: DriverDAO.getNextUserId()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 848
**Description:** `public static Long getNextUserId()` has no Javadoc. Same concerns as A73-29 for `users_id_seq`. No `@return` tag.

---

### A73-31 — Undocumented non-trivial public method: DriverDAO.getALLExpiredTrainigs()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 883
**Description:** `public static List<DriverTrainingBean> getALLExpiredTrainigs()` has no Javadoc. Method name contains a typo ("Trainigs"). Unlike `getExpiredTrainigs(String companyId)`, this overload fetches expired trainings across all companies (no company filter). This cross-company scope is critical and undocumented. No `@return` tag.

---

### A73-32 — Undocumented non-trivial public method: DriverDAO.revokeDriverAccessOnTrainingExpiry()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 902
**Description:** `public static void revokeDriverAccessOnTrainingExpiry()` has no Javadoc. This method is a scheduled-operation candidate that deletes `driver_unit` rows (hard-deletes unit assignments) for all drivers with expired trainings across all companies. The broad destructive scope is undocumented.

---

### A73-33 — Undocumented non-trivial public method: DriverDAO.getExpiredTrainigsComp()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 920
**Description:** `public List<UserCompRelBean> getExpiredTrainigsComp()` has no Javadoc. Method name contains a typo ("Trainigs"). Returns company-contact information for companies that have drivers with expired trainings today (exact expiry date). No `@return` tag.

---

### A73-34 — Undocumented non-trivial public method: DriverDAO.getExpiringTrainigsComp()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 932
**Description:** `public List<UserCompRelBean> getExpiringTrainigsComp()` has no Javadoc. Method name contains a typo ("Trainigs"). The log message at line 933 incorrectly reads `"Inside DriverDAO Method : getExpiredTrainigsComp"` (same log string as `getExpiredTrainigsComp`, line 921) — a copy-paste error. No `@return` tag.

---

### A73-35 — Inaccurate log message: DriverDAO.getExpiringTrainigsComp()
**Severity:** MEDIUM
**File:** `DriverDAO.java`, line 933
**Description:** The log statement inside `getExpiringTrainigsComp()` reads:
```java
log.info("Inside DriverDAO Method : getExpiredTrainigsComp");
```
The method name is `getExpiringTrainigsComp` (expiring, not expired). This log message will mislead any operator diagnosing issues via log analysis.

---

### A73-36 — No class-level Javadoc: DriverUnitDAO
**Severity:** LOW
**File:** `DriverUnitDAO.java`, line 11
**Description:** `DriverUnitDAO` has no class-level Javadoc.

---

### A73-37 — Undocumented non-trivial public method: DriverUnitDAO.getInstance()
**Severity:** MEDIUM
**File:** `DriverUnitDAO.java`, line 19
**Description:** `public static DriverUnitDAO getInstance()` has no Javadoc. Implements double-checked locking pattern for thread-safe singleton construction. No `@return` tag.

---

### A73-38 — Undocumented non-trivial public method: DriverUnitDAO.getDriverUnitsByCompAndDriver()
**Severity:** MEDIUM
**File:** `DriverUnitDAO.java`, line 33
**Description:** `public static List<DriverUnitBean> getDriverUnitsByCompAndDriver(Long compId, Long driverId)` has no Javadoc. Queries view `v_driver_units` (not a base table). No `@param` or `@return` tags.

---

### A73-39 — Undocumented non-trivial public method: DriverUnitDAO.saveDriverVehicle()
**Severity:** MEDIUM
**File:** `DriverUnitDAO.java`, line 49
**Description:** `public void saveDriverVehicle(DriverVehicleBean driverVehicle)` has no Javadoc. The method performs a transactional diff-based sync: it fetches the current set of assigned units with a `FOR UPDATE` lock, removes assignments present in DB but not in the input, adds assignments present in the input but not in DB, and commits. The `FOR UPDATE` row-locking strategy and the diff semantics are complex and entirely undocumented. No `@param` tag. Exception handling swallows the rollback failure on line 69 (`// Ignore the error`) without documentation.

---

## 3. Summary

| Finding | File | Line(s) | Severity |
|---------|------|---------|----------|
| A73-1  | DateFormatDAO.java | 11 | LOW |
| A73-2  | DateFormatDAO.java | 14 | MEDIUM |
| A73-3  | DriverDAO.java | 34 | LOW |
| A73-4  | DriverDAO.java | 170 | MEDIUM |
| A73-5  | DriverDAO.java | 179 | MEDIUM |
| A73-6  | DriverDAO.java | 196 | MEDIUM |
| A73-7  | DriverDAO.java | 213 | MEDIUM |
| A73-8  | DriverDAO.java | 252 | MEDIUM |
| A73-9  | DriverDAO.java | 289, 293 | MEDIUM |
| A73-10 | DriverDAO.java | 315 | MEDIUM |
| A73-11 | DriverDAO.java | 352 | MEDIUM |
| A73-12 | DriverDAO.java | 391 | MEDIUM |
| A73-13 | DriverDAO.java | 419 | MEDIUM |
| A73-14 | DriverDAO.java | 449 | MEDIUM |
| A73-15 | DriverDAO.java | 480 | MEDIUM |
| A73-16 | DriverDAO.java | 502 | MEDIUM |
| A73-17 | DriverDAO.java | 540 | MEDIUM |
| A73-18 | DriverDAO.java | 577 | MEDIUM |
| A73-19 | DriverDAO.java | 603 | MEDIUM |
| A73-20 | DriverDAO.java | 630 | MEDIUM |
| A73-21 | DriverDAO.java | 649 | MEDIUM |
| A73-22 | DriverDAO.java | 690 | MEDIUM |
| A73-23 | DriverDAO.java | 690 | MEDIUM |
| A73-24 | DriverDAO.java | 702 | MEDIUM |
| A73-25 | DriverDAO.java | 732 | MEDIUM |
| A73-26 | DriverDAO.java | 773 | MEDIUM |
| A73-27 | DriverDAO.java | 798, 813 | MEDIUM |
| A73-28 | DriverDAO.java | 828 | MEDIUM |
| A73-29 | DriverDAO.java | 843 | MEDIUM |
| A73-30 | DriverDAO.java | 848 | MEDIUM |
| A73-31 | DriverDAO.java | 883 | MEDIUM |
| A73-32 | DriverDAO.java | 902 | MEDIUM |
| A73-33 | DriverDAO.java | 920 | MEDIUM |
| A73-34 | DriverDAO.java | 932 | MEDIUM |
| A73-35 | DriverDAO.java | 933 | MEDIUM |
| A73-36 | DriverUnitDAO.java | 11 | LOW |
| A73-37 | DriverUnitDAO.java | 19 | MEDIUM |
| A73-38 | DriverUnitDAO.java | 33 | MEDIUM |
| A73-39 | DriverUnitDAO.java | 49 | MEDIUM |

**Totals:** 39 findings — 4 LOW, 35 MEDIUM, 0 HIGH
