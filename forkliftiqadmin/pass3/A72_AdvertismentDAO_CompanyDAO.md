# Pass 3 Documentation Audit — A72
**Audit run:** 2026-02-26-01
**Agent:** A72
**Files:**
- `src/main/java/com/dao/AdvertismentDAO.java`
- `src/main/java/com/dao/CompanyDAO.java`

---

## 1. Reading Evidence

### 1.1 AdvertismentDAO.java

**Class:** `AdvertismentDAO` — line 16

**Fields:**

| Name | Type | Line |
|------|------|------|
| `log` | `static Logger` | 18 |
| `instance` | `static AdvertismentDAO` | 20 |

**Methods:**

| Method | Visibility | Line |
|--------|------------|------|
| `getInstance()` | `public static` | 22 |
| `AdvertismentDAO()` (constructor) | `private` | 33 |
| `getAllAdvertisement()` | `public` | 37 |
| `getAdvertisementById(String id)` | `public` | 77 |
| `delAdvertisementById(String id)` | `public` | 119 |
| `saveAdvertisement(AdvertisementBean advertisementBean)` | `public` | 149 |
| `updateAdvertisement(AdvertisementBean advertisementBean)` | `public` | 206 |

---

### 1.2 CompanyDAO.java

**Class:** `CompanyDAO` — line 35

**Fields (static constants):**

| Name | Type | Line |
|------|------|------|
| `log` | `static Logger` | 36 |
| `QUERY_USR_RPT` | `static final String` | 38 |
| `QUERY_USR_ALERT` | `static final String` | 40 |
| `QUERY_ALERT_LST` | `static final String` | 42 |
| `QUERY_REPORT_LST` | `static final String` | 44 |
| `SAVE_USER_ROLE` | `static final String` | 46 |
| `UPDATE_COMPANY_ROLE` | `static final String` | 50 |
| `SAVE_COMPANY_DEALER_ROLE` | `static final String` | 56 |
| `SAVE_USERS` | `static final String` | 60 |
| `SAVE_COGNITO_USERS` | `static final String` | 63 |
| `SAVE_USERS_COMP_REL` | `static final String` | 66 |
| `SAVE_COMPANY_ROLE` | `static final String` | 69 |
| `SAVE_COMP` | `static final String` | 73 |
| `QUERY_SUBCOMPANYLST_BY_ID` | `static final String` | 75 |
| `QUERY_COMPANY_BY_ID` | `static final String` | 81 |
| `QUERY_SUBCOMPANY_BY_ID` | `static final String` | 87 |
| `QUERY_COMPANY_USR_BY_ID` | `static final String` | 89 |
| `UPDATE_USR_PIN` | `static final String` | 95 |
| `UPDATE_USR_INFO` | `static final String` | 97 |
| `UPDATE_COMPANY` | `static final String` | 99 |
| `UPDATE_COMP_INFO_UPDATE_SETTINGS` | `static final String` | 101 |
| `QUERY_USR_ALERT_BY_TYPE` | `static final String` | 103 |
| `COGNITO_USERNAME_BY_ID` | `static final String` | 105 |
| `theInstance` | `static CompanyDAO` | 107 |
| `QUERY_COUNT_USR_ALERT_BY_TYPE` | `static final String` | 924 |

**Methods:**

| Method | Visibility | Line |
|--------|------------|------|
| `getInstance()` | `public synchronized static` | 109 |
| `CompanyDAO()` (constructor) | `private` | 117 |
| `saveCompInfo(CompanyBean compbean, String Role)` | `public` | 122 |
| `saveUserRoles(int userId, String role)` | `public` | 153 |
| `saveSubCompInfo(String sessCompId, CompanyBean compbean)` | `public` | 161 |
| `getSubCompanies(String companyId)` | `public static` | 177 |
| `getSubCompanyLst(String companyId)` | `public` | 201 |
| `GetCompanyRoles(long companyId)` | `private` | 222 |
| `saveUsers(int compId, UserBean userBean)` | `public` | 239 |
| `savePermission(int driver_id, int compId)` | `public` | 267 |
| `saveDefaultEmails(int driver_id)` | `private` | 296 |
| `saveCompanyRoles(int companyId, String role)` | `private` | 328 |
| `updateCompPrivacy(String compId)` | `public` | 336 |
| `checkExist(String name, String dbField, String compId)` | `public` | 357 |
| `checkUserExit(String name, String dbField, String id)` | `public` | 382 |
| `checkCompExist(CompanyBean companyBean)` | `public` | 396 |
| `resetPass(String compId, String pass)` | `public` | 435 |
| `getCompLogo(String compId)` | `public` | 461 |
| `getCompanyById(String companyId)` | `public` | 488 |
| `getCompanyByCompId(String id)` | `public` | 521 |
| `getCompanyContactsByCompId(String compId, int usrId, String sessionToken)` | `public` | 558 |
| `updateCompInfo(CompanyBean compBean, int usrId, String accessToken)` | `public` | 594 |
| `updateCompSettings(CompanyBean compBean)` | `public` | 632 |
| `getEntityComp(String entityId)` | `public` | 655 |
| `getEntityByQuestion(String qId, String type)` | `public` | 690 |
| `getAllEntity()` | `public` | 722 |
| `getAllCompany()` | `public` | 770 |
| `getAlertList()` | `public static` | 813 |
| `convertCompanyToDealer(String companyId)` | `public` | 830 |
| `getReportList()` | `public static` | 847 |
| `addUserSubscription(String userId, String alertId)` | `public static` | 862 |
| `deleteUserSubscription(String userId, String alertId)` | `public static` | 871 |
| `getUserAlert(String id)` | `public` | 880 |
| `getUserAlert(String id, String type, String file_name)` | `public` | 895 |
| `getUserReport(String id)` | `public` | 911 |
| `checkExistingUserAlertByType(String userId, String type)` | `public` | 925 |
| `getCompanyMaxId()` | `public` | 933 |
| `getUserMaxId()` | `public` | 942 |

---

## 2. Findings

### AdvertismentDAO.java

---

**A72-1** [LOW] — No class-level Javadoc on `AdvertismentDAO`
File: `AdvertismentDAO.java`, line 16
The class `AdvertismentDAO` has no `/** ... */` Javadoc comment above its declaration. There is no description of the class's purpose, the table it targets (`advertisment`), or its singleton pattern.

---

**A72-2** [MEDIUM] — No Javadoc on `getInstance()` (AdvertismentDAO, line 22)
`getInstance()` implements a double-checked locking singleton. It is a public, non-trivial method (synchronization logic, lazy initialization) with no Javadoc, no `@return` tag describing the singleton instance returned.

---

**A72-3** [MEDIUM] — No Javadoc on `getAllAdvertisement()` (line 37)
Public method. Queries the `advertisment` table and returns all rows mapped to `AdvertisementBean` instances, ordered by `order_no`. No Javadoc, no `@return`, no `@throws`.

---

**A72-4** [MEDIUM] — No Javadoc on `getAdvertisementById(String id)` (line 77)
Public method. Fetches advertisement records matching a given ID. No Javadoc, no `@param id`, no `@return`, no `@throws`.

---

**A72-5** [MEDIUM] — No Javadoc on `delAdvertisementById(String id)` (line 119)
Public method. Deletes a record from the `advertisment` table by ID. No Javadoc, no `@param id`, no `@return`, no `@throws`.

---

**A72-6** [MEDIUM] — No Javadoc on `saveAdvertisement(AdvertisementBean advertisementBean)` (line 149)
Public method. Inserts a new advertisement record; auto-calculates `order_no` as `max(order_no)+1`. No Javadoc, no `@param advertisementBean`, no `@return`, no `@throws`.

---

**A72-7** [MEDIUM] — No Javadoc on `updateAdvertisement(AdvertisementBean advertisementBean)` (line 206)
Public method. Updates an existing advertisement; conditionally omits `pic` from the update if `pic` is blank. No Javadoc, no `@param advertisementBean`, no `@return`, no `@throws`.

---

**A72-8** [MEDIUM] — Misleading log message in `updateAdvertisement()` (line 211)
File: `AdvertismentDAO.java`, line 211
The log statement reads:
```java
log.info("Inside LoginDAO Method : updateManufacturer");
```
The actual class is `AdvertismentDAO` (not `LoginDAO`) and the method is `updateAdvertisement` (not `updateManufacturer`). This message will mislead any developer reading application logs. The same pattern of using `"Inside LoginDAO Method :"` for methods that are not in `LoginDAO` appears in other log messages in this file (lines 43, 83, 125) but those at least name the correct method. This instance names both class and method incorrectly, making it MEDIUM severity.

---

### CompanyDAO.java

---

**A72-9** [LOW] — No class-level Javadoc on `CompanyDAO`
File: `CompanyDAO.java`, line 35
The class `CompanyDAO` has no `/** ... */` Javadoc comment. No description of its responsibilities, the entities it manages, or its singleton pattern.

---

**A72-10** [MEDIUM] — No Javadoc on `getInstance()` (CompanyDAO, line 109)
Public synchronized singleton accessor. Non-trivial (thread-safe). No Javadoc, no `@return`.

---

**A72-11** [MEDIUM] — No Javadoc on `saveCompInfo(CompanyBean, String)` (line 122)
Public method. Creates a company record, a company role, a first user, and assigns a site-admin role to that user — a multi-step operation. No Javadoc, no `@param compbean`, no `@param Role`, no `@return`, no `@throws`.

---

**A72-12** [MEDIUM] — No Javadoc on `saveUserRoles(int, String)` (line 153)
Public method. Inserts a user-role relationship via `SAVE_USER_ROLE`. No Javadoc, no `@param userId`, no `@param role`, no `@throws`.

---

**A72-13** [MEDIUM] — No Javadoc on `saveSubCompInfo(String, CompanyBean)` (line 161)
Public method. Creates a sub-company, links it to a parent, and updates the company role. No Javadoc, no `@param sessCompId`, no `@param compbean`, no `@return`, no `@throws`.

---

**A72-14** [MEDIUM] — No Javadoc on `getSubCompanies(String)` (line 177)
Public static method. Returns a list of `CompanyBean` objects for all sub-companies of the given parent. No Javadoc, no `@param companyId`, no `@return`, no `@throws`.

---

**A72-15** [MEDIUM] — No Javadoc on `getSubCompanyLst(String)` (line 201)
Public method. Returns a comma-separated string of company IDs including the parent. No Javadoc, no `@param companyId`, no `@return`, no `@throws`.

---

**A72-16** [MEDIUM] — No Javadoc on `saveUsers(int, UserBean)` (line 239)
Public method. The method name implies persisting a full user record, but the `SAVE_USERS` insert (which writes to the `users` table) is entirely commented out (lines 247–254). Only the Cognito user mapping (`users_cognito`) and the user-company relationship (`user_comp_rel`) are written. No Javadoc documents this discrepancy. A caller relying on the method name would assume a full user record is saved to the `users` table. No `@param compId`, no `@param userBean`, no `@throws`.

---

**A72-17** [MEDIUM] — No Javadoc on `savePermission(int, int)` (line 267)
Public method. Inserts a row into the `permission` table with timestamps and `enabled=true`. No Javadoc, no `@param driver_id`, no `@param compId`, no `@throws`.

---

**A72-18** [MEDIUM] — No Javadoc on `updateCompPrivacy(String)` (line 336)
Public method. Sets `privacy = false` for a company. No Javadoc, no `@param compId`, no `@throws`.

---

**A72-19** [MEDIUM] — No Javadoc on `checkExist(String, String, String)` (line 357)
Public method. Checks whether a company record already exists with the given value in the specified DB column, optionally excluding a specific company ID. Accepts a raw `dbField` column name and embeds it directly into SQL (SQL injection risk — outside documentation scope, but the lack of any Javadoc means the dangerous `dbField` parameter is undescribed). No Javadoc, no `@param` tags, no `@return`, no `@throws`.

---

**A72-20** [MEDIUM] — No Javadoc on `checkUserExit(String, String, String)` (line 382)
Public method. Checks for user existence by a dynamic column name. No Javadoc, no `@param` tags, no `@return`, no `@throws`. (Note also: method name `checkUserExit` is a misspelling of `checkUserExist`; this is a naming issue, not a documentation finding per se, but worth noting.)

---

**A72-21** [MEDIUM] — No Javadoc on `checkCompExist(CompanyBean)` (line 396)
Public method. Looks up a company by name, email, question, and answer. Returns the company ID string or empty string. No Javadoc, no `@param companyBean`, no `@return`, no `@throws`.

---

**A72-22** [MEDIUM] — No Javadoc on `resetPass(String, String)` (line 435)
Public method. Updates a company's password (stored as `md5(?)`). No Javadoc, no `@param compId`, no `@param pass`, no `@return`, no `@throws`.

---

**A72-23** [MEDIUM] — No Javadoc on `getCompLogo(String)` (line 461)
Public method. Returns the logo filename/path for a company, or an empty string if none. No Javadoc, no `@param compId`, no `@return`, no `@throws`.

---

**A72-24** [MEDIUM] — No Javadoc on `getCompanyById(String)` (line 488)
Public method. Fetches a single `CompanyBean` by ID, populates roles, and returns `results.get(0)` — which will throw `IndexOutOfBoundsException` if no matching company exists (no guard). No Javadoc, no `@param companyId`, no `@return`, no `@throws`.

---

**A72-25** [MEDIUM] — No Javadoc on `getCompanyByCompId(String)` (line 521)
Public method. Functionally similar to `getCompanyById` but additionally maps `mobile` (column 16 from `QUERY_COMPANY_BY_ID`). `QUERY_COMPANY_BY_ID` selects only 15 columns (lines 82–85); accessing column 16 (`rs.getString(16)`) will throw a `SQLException` at runtime. No Javadoc, no `@param id`, no `@return`, no `@throws`.

---

**A72-26** [HIGH] — `getCompanyByCompId` accesses column 16 from a 15-column query
File: `CompanyDAO.java`, line 545
`QUERY_COMPANY_BY_ID` selects exactly 15 columns (lines 82–85). `getCompanyByCompId` calls `rs.getString(16)` to populate `mobile` (line 545). This will throw a `SQLException` at runtime whenever this method is invoked. No comment or Javadoc acknowledges this defect. The companion method `getCompanyContactsByCompId` uses the separate `QUERY_COMPANY_USR_BY_ID` query (which also does not include `mobile`). Severity is HIGH because the inaccuracy — the implicit claim that the code correctly retrieves company data — is dangerously wrong; the method will always fail.

---

**A72-27** [MEDIUM] — No Javadoc on `getCompanyContactsByCompId(String, int, String)` (line 558)
Public method. Fetches company and user contact data from two sources: the database and the Cognito REST service. The `sessionToken` parameter is passed to the Cognito service. No Javadoc, no `@param compId`, no `@param usrId`, no `@param sessionToken`, no `@return`, no `@throws`.

---

**A72-28** [MEDIUM] — No Javadoc on `updateCompInfo(CompanyBean, int, String)` (line 594)
Public method. Does NOT update any local database company table; it only updates the Cognito user via `RestClientService`. The method name `updateCompInfo` implies broader company-record updates than what is performed. No Javadoc clarifies the Cognito-only scope. No `@param compBean`, no `@param usrId`, no `@param accessToken`, no `@return`, no `@throws`.

---

**A72-29** [MEDIUM] — Misleading log message in `updateCompSettings()` (line 633)
File: `CompanyDAO.java`, line 633
The log statement reads:
```java
log.info("Inside CompanyDAO Method : updateCompInfo");
```
The actual method is `updateCompSettings`, not `updateCompInfo`. This will mislead any developer reading logs; `updateCompInfo` is a different method in the same class. Both severity and the fact that the wrong method name refers to another real method in the same class makes this a MEDIUM finding.

---

**A72-30** [MEDIUM] — No Javadoc on `updateCompSettings(CompanyBean)` (line 632)
Public method. Updates `date_format`, `max_session_length`, and `timezone` for a company. No Javadoc, no `@param compBean`, no `@return`, no `@throws`.

---

**A72-31** [MEDIUM] — No Javadoc on `getEntityComp(String)` (line 655)
Public method. Returns all companies optionally filtered by entity ID (skips filter when `entityId` is `"1"`). No Javadoc, no `@param entityId`, no `@return`, no `@throws`.

---

**A72-32** [MEDIUM] — No Javadoc on `getEntityByQuestion(String, String)` (line 690)
Public method. Returns entities associated with a question ID and type. No Javadoc, no `@param qId`, no `@param type`, no `@return`, no `@throws`.

---

**A72-33** [MEDIUM] — No Javadoc on `getAllEntity()` (line 722)
Public method. Returns all entities with their roles populated. No Javadoc, no `@return`, no `@throws`.

---

**A72-34** [MEDIUM] — No Javadoc on `getAllCompany()` (line 770)
Public method. Returns all companies ordered by name, with roles populated. No Javadoc, no `@return`, no `@throws`.

---

**A72-35** [MEDIUM] — No Javadoc on `getAlertList()` (line 813)
Public static method. Returns all subscription records of type `alert`. No Javadoc, no `@return`, no `@throws`.

---

**A72-36** [MEDIUM] — No Javadoc on `convertCompanyToDealer(String)` (line 830)
Public method. Promotes a company to dealer role: updates role if `ROLE_COMP` authority exists, inserts dealer role otherwise. No Javadoc, no `@param companyId`, no `@throws`.

---

**A72-37** [MEDIUM] — No Javadoc on `getReportList()` (line 847)
Public static method. Returns all subscription records of type `report`. No Javadoc, no `@return`, no `@throws`.

---

**A72-38** [MEDIUM] — No Javadoc on `addUserSubscription(String, String)` (line 862)
Public static method. Inserts a user-subscription relationship. No Javadoc, no `@param userId`, no `@param alertId`, no `@throws`.

---

**A72-39** [MEDIUM] — No Javadoc on `deleteUserSubscription(String, String)` (line 871)
Public static method. Deletes a user-subscription relationship. No Javadoc, no `@param userId`, no `@param alertId`, no `@throws`.

---

**A72-40** [MEDIUM] — No Javadoc on `getUserAlert(String)` (line 880)
Public method. Returns all alert-type subscriptions for a user. No Javadoc, no `@param id`, no `@return`, no `@throws`.

---

**A72-41** [MEDIUM] — No Javadoc on `getUserAlert(String, String, String)` (line 895)
Public overload. Returns a single `AlertBean` (or empty `AlertBean` if not found) for the given user, subscription type, and file name. No Javadoc distinguishing it from the single-param overload. No `@param id`, no `@param type`, no `@param file_name`, no `@return`, no `@throws`.

---

**A72-42** [MEDIUM] — No Javadoc on `getUserReport(String)` (line 911)
Public method. Returns all report-type subscriptions for a user. No Javadoc, no `@param id`, no `@return`, no `@throws`.

---

**A72-43** [MEDIUM] — No Javadoc on `checkExistingUserAlertByType(String, String)` (line 925)
Public method. Returns `true` if the user has at least one subscription of the given type. No Javadoc, no `@param userId`, no `@param type`, no `@return`, no `@throws`.

---

**A72-44** [MEDIUM] — No Javadoc on `getCompanyMaxId()` (line 933)
Public method. Fetches the next value from the `company_id_seq` PostgreSQL sequence. No Javadoc, no `@return`, no `@throws`.

---

**A72-45** [MEDIUM] — No Javadoc on `getUserMaxId()` (line 942)
Public method. Fetches the next value from the `users_id_seq` PostgreSQL sequence. No Javadoc, no `@return`, no `@throws`.

---

**A72-46** [MEDIUM] — `saveUsers` method body does not match its implied contract (line 239)
File: `CompanyDAO.java`, lines 247–254
The `SAVE_USERS` statement (which inserts into the `users` table) is entirely commented out. The method only inserts into `users_cognito` and `user_comp_rel`. A caller expecting a row in the `users` table (as the method signature and the constant name `SAVE_USERS` imply) will not get one. There is no comment, no Javadoc, and no deprecation marker explaining this intentional omission, making the code misleading.

---

## 3. Summary Table

| Finding | File | Line | Severity | Description |
|---------|------|------|----------|-------------|
| A72-1 | AdvertismentDAO.java | 16 | LOW | No class-level Javadoc |
| A72-2 | AdvertismentDAO.java | 22 | MEDIUM | No Javadoc on `getInstance()` |
| A72-3 | AdvertismentDAO.java | 37 | MEDIUM | No Javadoc on `getAllAdvertisement()` |
| A72-4 | AdvertismentDAO.java | 77 | MEDIUM | No Javadoc on `getAdvertisementById()` |
| A72-5 | AdvertismentDAO.java | 119 | MEDIUM | No Javadoc on `delAdvertisementById()` |
| A72-6 | AdvertismentDAO.java | 149 | MEDIUM | No Javadoc on `saveAdvertisement()` |
| A72-7 | AdvertismentDAO.java | 206 | MEDIUM | No Javadoc on `updateAdvertisement()` |
| A72-8 | AdvertismentDAO.java | 211 | MEDIUM | Inaccurate log: wrong class name and method name |
| A72-9 | CompanyDAO.java | 35 | LOW | No class-level Javadoc |
| A72-10 | CompanyDAO.java | 109 | MEDIUM | No Javadoc on `getInstance()` |
| A72-11 | CompanyDAO.java | 122 | MEDIUM | No Javadoc on `saveCompInfo()` |
| A72-12 | CompanyDAO.java | 153 | MEDIUM | No Javadoc on `saveUserRoles()` |
| A72-13 | CompanyDAO.java | 161 | MEDIUM | No Javadoc on `saveSubCompInfo()` |
| A72-14 | CompanyDAO.java | 177 | MEDIUM | No Javadoc on `getSubCompanies()` |
| A72-15 | CompanyDAO.java | 201 | MEDIUM | No Javadoc on `getSubCompanyLst()` |
| A72-16 | CompanyDAO.java | 239 | MEDIUM | No Javadoc on `saveUsers()` |
| A72-17 | CompanyDAO.java | 267 | MEDIUM | No Javadoc on `savePermission()` |
| A72-18 | CompanyDAO.java | 336 | MEDIUM | No Javadoc on `updateCompPrivacy()` |
| A72-19 | CompanyDAO.java | 357 | MEDIUM | No Javadoc on `checkExist()` |
| A72-20 | CompanyDAO.java | 382 | MEDIUM | No Javadoc on `checkUserExit()` |
| A72-21 | CompanyDAO.java | 396 | MEDIUM | No Javadoc on `checkCompExist()` |
| A72-22 | CompanyDAO.java | 435 | MEDIUM | No Javadoc on `resetPass()` |
| A72-23 | CompanyDAO.java | 461 | MEDIUM | No Javadoc on `getCompLogo()` |
| A72-24 | CompanyDAO.java | 488 | MEDIUM | No Javadoc on `getCompanyById()` |
| A72-25 | CompanyDAO.java | 521 | MEDIUM | No Javadoc on `getCompanyByCompId()` |
| A72-26 | CompanyDAO.java | 545 | HIGH | `getCompanyByCompId` reads column 16 from a 15-column query; always throws at runtime |
| A72-27 | CompanyDAO.java | 558 | MEDIUM | No Javadoc on `getCompanyContactsByCompId()` |
| A72-28 | CompanyDAO.java | 594 | MEDIUM | No Javadoc on `updateCompInfo()`; name misleadingly implies DB update, only Cognito is updated |
| A72-29 | CompanyDAO.java | 633 | MEDIUM | Inaccurate log: `updateCompSettings` logs `updateCompInfo` |
| A72-30 | CompanyDAO.java | 632 | MEDIUM | No Javadoc on `updateCompSettings()` |
| A72-31 | CompanyDAO.java | 655 | MEDIUM | No Javadoc on `getEntityComp()` |
| A72-32 | CompanyDAO.java | 690 | MEDIUM | No Javadoc on `getEntityByQuestion()` |
| A72-33 | CompanyDAO.java | 722 | MEDIUM | No Javadoc on `getAllEntity()` |
| A72-34 | CompanyDAO.java | 770 | MEDIUM | No Javadoc on `getAllCompany()` |
| A72-35 | CompanyDAO.java | 813 | MEDIUM | No Javadoc on `getAlertList()` |
| A72-36 | CompanyDAO.java | 830 | MEDIUM | No Javadoc on `convertCompanyToDealer()` |
| A72-37 | CompanyDAO.java | 847 | MEDIUM | No Javadoc on `getReportList()` |
| A72-38 | CompanyDAO.java | 862 | MEDIUM | No Javadoc on `addUserSubscription()` |
| A72-39 | CompanyDAO.java | 871 | MEDIUM | No Javadoc on `deleteUserSubscription()` |
| A72-40 | CompanyDAO.java | 880 | MEDIUM | No Javadoc on `getUserAlert(String)` |
| A72-41 | CompanyDAO.java | 895 | MEDIUM | No Javadoc on `getUserAlert(String, String, String)` |
| A72-42 | CompanyDAO.java | 911 | MEDIUM | No Javadoc on `getUserReport()` |
| A72-43 | CompanyDAO.java | 925 | MEDIUM | No Javadoc on `checkExistingUserAlertByType()` |
| A72-44 | CompanyDAO.java | 933 | MEDIUM | No Javadoc on `getCompanyMaxId()` |
| A72-45 | CompanyDAO.java | 942 | MEDIUM | No Javadoc on `getUserMaxId()` |
| A72-46 | CompanyDAO.java | 239 | MEDIUM | `saveUsers` silently omits `users` table insert; misleading name and dead code |

**Totals:** 1 HIGH, 42 MEDIUM, 2 LOW
