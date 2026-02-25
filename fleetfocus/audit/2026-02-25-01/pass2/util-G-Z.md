# Pass 2 -- Test Coverage: util package (G-Z)
**Agent:** A20
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

---

## Test Infrastructure Assessment

| Criterion | Status |
|---|---|
| Test directory exists | NO -- no `test/`, `tests/`, or `src/test/` directory anywhere in the repository |
| Test framework present | NO -- no JUnit, TestNG, Mockito, or any other test dependency detected |
| Test runner configuration | NO -- no `pom.xml` test plugins, no `build.gradle` test tasks, no Ant test targets |
| CI/CD test stage | NOT ASSESSED (out of scope for this pass) |
| **Overall test count** | **ZERO** -- 0 tests for all 24 files in scope |

**Consequence:** Every public method in every file below has **0% code coverage**. All findings below represent untested code paths with zero automated regression protection.

---

## Reading Evidence

### 1. GdprDataDelete.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/GdprDataDelete.java` (143 lines)
**Class:** `GdprDataDelete`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `void call_gdpr_delete_data() throws SQLException` | 29 | public |

**Key observations:**
- Performs irreversible DELETE operations across 6 tables: `fms_io_data_dtl`, `fms_io_data`, `fms_stat_data_dtl`, `fms_stat_data`, `fms_usage_data_dtl`, `fms_usage_data`, `op_chk_checklistanswer`, `op_chk_checklistresult`, `fms_unit_unlock_data`
- Uses string concatenation for SQL (lines 51, 65-67, 73-95) -- SQL injection vectors
- The `gdpr_data` value from the database is interpolated directly into interval expressions without validation
- `driver_cd` values inserted directly into SQL strings
- No transaction management (no commit/rollback) -- partial deletes possible
- Exception handler on line 110 references wrong method name: `send_timezone()`
- `stmte` (line 23) is created but never used for queries

---

### 2. GetHtml.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/GetHtml.java` (113 lines)
**Class:** `GetHtml`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `String getHTML(String urlToRead, String param)` | 16 | public |
| 2 | `String getHTML1(String urlToRead)` | 74 | public |
| 3 | `static String now(String dateFormat)` | 107 | public |

**Key observations:**
- URL is constructed by simple concatenation (`urlToRead+param`) without encoding (line 24) -- potential SSRF
- No input validation on URLs
- String concatenation in a loop for result building (lines 31, 93) -- performance concern
- `getHTML` does not close connection on exception; `getHTML1` disconnects but only in the success path
- 10-minute/15-minute read timeouts (lines 27, 87) without connection timeout

---

### 3. ImportFiles.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/ImportFiles.java` (~2700 lines)
**Class:** `ImportFiles extends HttpServlet`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `void doPost(HttpServletRequest, HttpServletResponse) throws ServletException, IOException` | 49 | protected |
| 2 | `void doGet(HttpServletRequest, HttpServletResponse) throws ServletException, IOException` | 2273 | protected |
| 3 | `String getFileName(Part part)` | 2315 | private |
| 4 | `boolean validateCSV(ArrayList<String>, String)` | 2375 | private |
| 5 | `boolean validateCSVIndividualD(ArrayList<String>, ArrayList<String>)` | 2398 | private |
| 6 | `String validateCSVIndividual(ArrayList<String>, ArrayList<Pattern>, boolean, boolean, boolean)` | 2427 | private |
| 7 | `String validateForMultiLangQstns(ArrayList<String>, ArrayList<Pattern>)` | 2489 | private |
| 8 | `boolean validateQuestionLenghtTab(ArrayList<String>, ArrayList<String>, String)` | 2533 | private |
| 9 | `boolean validateCSVIndividualTab(ArrayList<String>, ArrayList<String>)` | 2552 | private |
| 10 | `String normalizeDateFormatFlexible(String)` | 2621 | private |
| 11 | `String getFailingValidationValues(ArrayList<String>, ArrayList<String>)` | 2670 | private |

**Key observations:**
- Massive servlet handling multiple import types: drivers, driversUK, driversAU, questions, questions-tab, vehicles, serviceServer
- File upload path constructed from `appPath + RuntimeConf.UPLOAD_FOLDER` with no path traversal protection (line 85)
- No file-type validation -- any file extension accepted
- No file-size limit enforcement in code
- doGet hardcodes path `/media/bkupdrv/WEB01/ServiceImport/` (line 2282)
- CSV validation logic is complex with many branches -- prime candidate for unit testing

---

### 4. InfoLogger.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/InfoLogger.java` (107 lines)
**Class:** `InfoLogger`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `void writelog(String msg)` | 28 | public |

**Key observations:**
- SQL injection in line 59: `"SELECT EMP_CD FROM HR_EMP_MST WHERE EMP_NM='"+tuid+"'"` -- `tuid` is derived from parsing `msg` without sanitization
- SQL injection in line 64-65: INSERT uses string concatenation with user-supplied values (`uid`, `mid`, `rem`, `emp_cd`)
- `msg` is parsed with `indexOf` without bounds checking -- `StringIndexOutOfBoundsException` possible if format is unexpected (lines 51-56)
- File is created in a relative directory `"InfoLogs"` (line 93) -- location depends on working directory
- No log rotation or size limits
- Connection is closed in `finally` but `writer` is not closed if exception occurs between `open()` and `close()`

---

### 5. LindeConfig.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/LindeConfig.java` (146 lines)
**Class:** `LindeConfig`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `LindeConfig()` (constructor) | 47 | public |
| 2 | `void readXMLFile()` | 52 | public |
| 3 | `static String now(String dateFormat)` | 139 | public |

**Key observations:**
- Hardcoded filesystem path `/home/gmtp/linde_config/` (line 56)
- All fields are `public static` mutable -- any code can modify global configuration
- XML parsing with no DTD/XXE protection -- `DocumentBuilderFactory` not configured to prevent XXE (lines 63-65)
- `LOGOIMG_SMAL` assigned 3 times redundantly (lines 89-91)
- `mail_from` default contains hardcoded email (line 31)
- Exception silently caught with only `printStackTrace()` (line 134-136)

---

### 6. LogicBean_filter.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter.java` (475 lines)
**Class:** `LogicBean_filter`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `void clear_variables()` | 70 | public |
| 2 | `void init()` | 180 | public |
| 3 | `void setEnd_dt(String)` | 222 | public |
| 4 | `void setSt_dt(String)` | 236 | public |
| 5 | `void setSet_gp_cd(String)` | 271 | public |
| 6 | `void setSet_user_cd(String)` | 278 | public |
| 7 | `ArrayList getGroup_cd()` | 243 | public |
| 8 | `ArrayList getGroup_nm()` | 250 | public |
| 9 | `ArrayList getUser_cd()` | 257 | public |
| 10 | `ArrayList getUser_fnm()` | 264 | public |
| 11 | `ArrayList getUser_lnm()` | 285 | public |
| 12 | `String getGet_user_fnm()` | 292 | public |
| 13 | `String getGet_user_lnm()` | 299 | public |
| 14+ | Multiple `getV*()` getter methods | 306-469 | public |

**Key observations:**
- SQL injection in `Fetch_users()` (line 122): `set_gp_cd` concatenated into query
- SQL injection in `Fetch_Data()` (lines 136, 146-150): `set_user_cd`, `st_dt`, `end_dt` concatenated
- Connection closed in `init()` (line 202) but not in `finally` block -- resource leak on exception
- Raw `ArrayList` types used throughout (no generics)

---

### 7. LogicBean_filter1.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/LogicBean_filter1.java` (782 lines)
**Class:** `LogicBean_filter1`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `void clear_variables()` | 101 | public |
| 2 | `void init()` | 369 | public |
| 3 | `void setEnd_dt(String)` | 431 | public |
| 4 | `void setSt_dt(String)` | 445 | public |
| 5 | `void setSet_gp_cd(String)` | 480 | public |
| 6 | `void setSet_user_cd(String)` | 487 | public |
| 7 | `void setSort_asc(String)` | 767 | public |
| 8 | `void setSort_by(String)` | 774 | public |
| 9+ | Multiple getter methods | 424-678 | public |

**Key observations:**
- Same SQL injection issues as `LogicBean_filter`
- `sort_by` is parsed with `Integer.parseInt` (line 185) without try-catch -- `NumberFormatException` possible
- `convert_time()` (line 293) calls `Integer.parseInt` without validation -- can throw on non-numeric input
- Connection properly closed in `finally` block (improvement over LogicBean_filter)

---

### 8. Menu_Bean.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/Menu_Bean.java` (310 lines)
**Class:** `Menu_Bean`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `void setOption(String)` | 50 | public |
| 2 | `void setemp_nm(String)` | 51 | public |
| 3 | `void setModule(String)` | 52 | public |
| 4 | `ArrayList getFormId()` | 55 | public |
| 5 | `ArrayList getApplicationPath()` | 58 | public |
| 6 | `ArrayList getFormName()` | 61 | public |
| 7 | `ArrayList getFormType()` | 64 | public |
| 8 | `ArrayList getModuleName()` | 67 | public |
| 9 | `void fetchform_rights()` | 72 | public |
| 10 | `void fetchMenuAttr1()` | 119 | public |
| 11 | `void fetchSubModule()` | 163 | public |
| 12 | `void clearVectors()` | 210 | public |
| 13 | `void init()` | 218 | public |
| 14 | `void setSet_user_cd(String)` | 303 | public |
| 15 | `ArrayList getIcon_path()` | 300 | public |
| 16 | `ArrayList getModuleDesc()` | 306 | public |

**Key observations:**
- SQL injection in `fetchform_rights()` (line 77): `set_user_cd` concatenated
- SQL injection in `fetchSubModule()` (line 175): `module` concatenated
- `form_str` built by concatenation without parameterization (lines 94-103)
- Authorization logic for menu access entirely driven by untested SQL queries

---

### 9. Menu_Bean1.java
**File:** `WEB-INF/src/com/torrent/surat\fms6/util/Menu_Bean1.java` (293 lines)
**Class:** `Menu_Bean1`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1-16 | Same structure as Menu_Bean with slight variations | various | public |

**Key observations:**
- Near-duplicate of `Menu_Bean.java` with minor differences (adds `form_desc`, `PRIORITY` ordering)
- Line 192: debug query appended to `FormName` list -- `FormName.add(query1)` -- leaks SQL to the UI
- Same SQL injection vulnerabilities as Menu_Bean

---

### 10. MigrateMaster.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/MigrateMaster.java` (325 lines)
**Class:** `MigrateMaster`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `void callMigrateMaster() throws SQLException` | 18 | public |

**Key observations:**
- Performs mass data migration: reads all active customers, migrates vehicle override data to location/department override tables
- Uses string concatenation for all SQL statements -- SQL injection if `cust_cd` or `locations` are tainted
- No transaction boundaries -- partial migration possible on failure
- Updates `FMS_USR_MST.supervisor_access` for users (line 100) -- security-relevant operation
- 325 lines in a single method with deeply nested loops -- very high complexity, very high test priority

---

### 11. PasswordExpiryAlert.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/PasswordExpiryAlert.java` (102 lines)
**Class:** `PasswordExpiryAlert`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `void checkExpiry() throws SQLException` | 13 | public |
| 2 | `boolean isValid(String email)` | 98 | private |

**Key observations:**
- Hardcoded 3-month password expiry interval (line 31-35)
- Hardcoded 7-day pre-expiry alert window
- SQL injection in email insert (line 69): `email`, `subsject` (sic -- typo), `message` concatenated
- SQL injection in update (line 72): `userBean.getId()` concatenated
- Email validation regex on line 99 may reject valid emails (e.g., `+` in local part)
- Alert message contains hardcoded phone number `+44 (0) 1460 259 101` (line 67)
- Misspelled variable `subsject` (line 58)
- Password expiry is security-critical -- zero test coverage is high risk

---

### 12. PurgeData.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/PurgeData.java` (5 lines)
**Class:** `PurgeData`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| (none) | Empty class | -- | -- |

**Key observations:**
- Class is completely empty -- no methods, no fields
- Named `PurgeData` but performs no data purging
- Either dead code or an incomplete implementation

---

### 13. RuntimeConf.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/RuntimeConf.java` (156 lines)
**Class:** `RuntimeConf`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| (none) | No methods -- constants/configuration only | -- | -- |

**Key observations:**
- **HARDCODED CREDENTIALS** (CRITICAL):
  - `pass = "ciifirmware"` (line 20) -- firmware password
  - `firmwarepass = "Sdh79HfkLq6"` (line 30) -- firmware FTP password
  - `username = "TestK"` / `password = "testadmin"` (lines 54-55) -- test credentials
  - `PASSWORD = "fOqDVWYK"` (line 87) -- Clickatell SMS API password
  - `API_ID = "3259470"` (line 88) -- SMS API ID
- `mail_from` hardcoded (line 21)
- All fields are `public static` non-final mutable -- any code can modify these at runtime
- Contains infrastructure addresses, server names, ports in plaintext
- JNDI data source names all point to `jdbc/fms30`

---

### 14. SendMessage.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/SendMessage.java` (242 lines)
**Class:** `SendMessage`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `void init()` | 34 | public |

**Key observations:**
- Sends SMS via Clickatell API using hardcoded credentials from `RuntimeConf`
- Auth URL includes password in query string (line 180) -- credential exposure in logs
- `URLEncoder.encode(message)` on line 177 uses deprecated platform-default encoding
- SMS messages deleted from `sms_outgoing` after send (line 203) -- no audit trail
- SQL injection: `id` concatenated into DELETE query (line 132)
- `readLines()` uses deprecated `DataInputStream.readLine()` (line 236)
- No retry logic for failed SMS sends

---

### 15. SupervisorMasterHelper.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/SupervisorMasterHelper.java` (446 lines)
**Class:** `SupervisorMasterHelper`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `boolean deleteSupervisorByUser(String user, String cust_cd, String loc_cd, String dept_cd, String access_user)` | 18 | public |
| 2 | `boolean deleteSupervisor(String slot, String cust_cd, String loc_cd, String dept_cd, String access_user)` | 206 | public |
| 3 | `void deleteSuperMaster(int userCdToDeactivate, String accessUser)` | 346 | public |

**Key observations:**
- All three methods use string concatenation for SQL -- SQL injection throughout
- `deleteSupervisorByUser` resets `supervisor_access` to `'0&0&0'` (line 49) -- security-sensitive
- `deleteSuperMaster` concatenates `userCdToDeactivate` (int) and `accessUser` (String) into SQL (line 414)
- Complex multi-table operations (outgoing, outgoing_stat, FMS_LOC_OVERRIDE, FMS_DEPT_OVERRIDE)
- No transaction management -- partial deletes/inserts possible

---

### 16. UtilBean.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/UtilBean.java` (413 lines)
**Class:** `UtilBean`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `String getGen_dt()` | 31 | public |
| 2 | `void setGen_dt(String)` | 35 | public |
| 3 | `int getDays(int month, int year)` | 58 | public |
| 4 | `static String getLocalTime(String currentTime, String webUserCD)` | 70 | public |
| 5 | `void init()` | 135 | public |
| 6 | `static CustomerBean getCustomerSettingByUser(String userCd)` | 178 | public |
| 7 | `static CustomerBean getCustomerSetting(String custCd)` | 235 | public |
| 8 | `static CustLocDeptBean getCustLocDeptBeanByUser(String userCD)` | 290 | public |
| 9 | `String getGen_tm()` | 345 | public |
| 10 | `void setGen_tm(String)` | 349 | public |
| 11 | `String getGen_sdttm()` | 353 | public |
| 12 | `String getGen_fdttm()` | 357 | public |
| 13 | `String getGen_dt_format()` | 361 | public |
| 14 | `void setGen_dt_format(String)` | 365 | public |
| 15 | `void template()` | 369 | public |

**Key observations:**
- SQL injection in `getLocalTime()` (line 86): `webUserCD` concatenated into SQL
- SQL injection in `getCustomerSettingByUser()` (line 193-196): `userCd` concatenated
- SQL injection in `getCustomerSetting()` (line 250-251): `custCd` concatenated
- SQL injection in `getCustLocDeptBeanByUser()` (line 305): `userCD` concatenated
- `getDays()` returns `noofdays[month - 1]` -- `ArrayIndexOutOfBoundsException` if month < 1 or > 12
- Static `customer` field (line 29) shared across threads -- thread-safety issue in `getCustomerSettingByUser`/`getCustomerSetting`
- `template()` method is explicitly labeled "TEMPLATE FOR DB UTILS" -- dead code

---

### 17. call_mail.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/call_mail.java` (~1100 lines)
**Class:** `call_mail`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `String getEmail()` | 40 | public |
| 2 | `void setEmail(String)` | 45 | public |
| 3 | `String getDebug()` | 50 | public |
| 4 | `void setDebug(String)` | 55 | public |
| 5 | `String Ename(String userid)` | 60 | public |
| 6 | `void call_email_au() throws SQLException` | 69 | public |
| 7 | `void call_email() throws SQLException` | 411 | public |
| 8 | `void call_alertemail() throws SQLException` | 685 | public |
| 9 | `void calibrate_impact()` | 786 | public |
| 10 | `boolean sendMail(String, String, String, String, String, String)` | 992 | public |
| 11 | `boolean sendMail1(String, String, String, String, String, String)` | 1035 | public |
| 12 | `void callLindeReports() throws SQLException` | 1096 | public |

**Key observations:**
- Complex email-sending logic with multiple branches based on report types
- SQL queries use string concatenation throughout -- SQL injection
- `call_email_au()` and `call_email()` fetch HTML content from URLs and send as email body -- potential for stored XSS
- `calibrate_impact()` performs UPDATE operations on `FMS_VEHICLE_MST` (impact settings)
- `sendMail`/`sendMail1` use JNDI mail sessions but no TLS enforcement visible
- `debug` mode allows overriding email recipient (line 106-110) -- if debug accidentally left on, emails go to wrong recipient

---

### 18. escapeSingleQuotes.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/escapeSingleQuotes.java` (19 lines)
**Class:** `escapeSingleQuotes`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `String replaceSingleQuotes(String sInput)` | 4 | public |

**Key observations:**
- Escapes single quotes by doubling them (SQL escape)
- Does NOT provide SQL injection protection (does not handle backslashes, null bytes, or other injection vectors)
- Used as the primary SQL escaping mechanism across the codebase -- insufficient
- Does not handle `null` input properly -- returns `""` only because the loop condition checks `sInput != null`
- Class name violates Java naming conventions (lowercase)

---

### 19. fix_department.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/fix_department.java` (388 lines)
**Class:** `fix_department`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `void show_cust_dept() throws SQLException` | 24 | public |
| 2 | `void fix_dept(String user_cd, String loc_cd, String dept_cd) throws SQLException` | 97 | public |
| 3+ | Getters/setters for customers, sites, departments, etc. | 317-384 | public |

**Key observations:**
- `fix_dept()` performs mass UPDATE across 12 tables to reassign department codes
- SQL injection: `user_cd`, `loc_cd`, `dept_cd` concatenated into queries (lines 121, 156, etc.)
- No transaction management -- partial updates across 12 tables possible
- Exception handler references wrong method name: `send_timezone()` (line 276)
- Data integrity risk: if any update fails partway through the 12-table cascade, database is left inconsistent

---

### 20. mail.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/mail.java` (311 lines)
**Class:** `mail`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `String Ename(String userid) throws SQLException` | 41 | public |
| 2 | `boolean sendMail(String, String, String, String, String, String)` | 109 | public |
| 3 | `static boolean sendMail(String, String, String, String, String, String, String, String)` | 147 | public static |
| 4 | `static boolean sendMailAttachment(String, String, String, String, String, String)` | 205 | public static |

**Key observations:**
- SQL injection in `Ename()` (line 63): `userid` concatenated
- `Ename()` queries the database but then overrides the result with `LindeConfig.mail_from` (line 78) -- dead query
- `sendMail` always returns `true` even on exception (lines 143-144, 201-202) -- silent failure
- `sendMailAttachment` creates temp CSV files in `/tmp/doc` (line 287) -- no cleanup on send failure
- `getExcel()` parses HTML with Jsoup to extract table data for CSV attachment -- complex untested logic
- All `sendMail` variants catch `Throwable` -- overly broad exception handling

---

### 21. password_life.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/password_life.java` (187 lines)
**Class:** `password_life`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `password_life()` (constructor) | 18 | public |
| 2 | `void clear_variables()` | 32 | public |
| 3 | `void setUser(String)` | 46 | public |
| 4 | `void setIp(String)` | 51 | public |
| 5 | `void setLogindate(String)` | 56 | public |
| 6 | `void setLogintime(String)` | 61 | public |
| 7 | `void loadDefaultValues() throws SQLException` | 66 | public |
| 8 | `int getCount()` | 118 | public |
| 9 | `int getDiff()` | 123 | public |
| 10 | `String getLogin_status()` | 128 | public |
| 11 | `int getCount1()` | 133 | public |
| 12 | `int getRem()` | 138 | public |
| 13 | `void init()` | 143 | public |

**Key observations:**
- **Decompiled code** (header says "Decompiled by DJ v3.9.9.91") -- source may not match original intent
- Uses Oracle-specific SQL syntax (`nvl`, `sysdate`, `decode`, `sign`) -- not portable
- SQL injection in `loadDefaultValues()`: `userid` concatenated (lines 76, 97, 104, 108)
- SQL injection: `ip`, `logindate`, `logintime` concatenated into UPDATE (line 108)
- Password lifecycle management with zero test coverage -- CRITICAL security gap
- Uses `EncryptTest().encrypt(userid)` (line 71) but result is unused (`s` is never referenced)
- Connection closed in `init()` success path but not in `finally` -- resource leak on exception

---

### 22. password_policy.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/password_policy.java` (159 lines)
**Class:** `password_policy`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `password_policy()` (constructor) | 16 | public |
| 2 | `void clear_variables()` | 30 | public |
| 3 | `void setUser(String)` | 44 | public |
| 4 | `void setIp(String)` | 49 | public |
| 5 | `void setLogindate(String)` | 54 | public |
| 6 | `void setLogintime(String)` | 59 | public |
| 7 | `void loadDefaultValues() throws SQLException` | 64 | public |
| 8 | `int getUmin()` | 98 | public |
| 9 | `int getUmax()` | 102 | public |
| 10 | `int getPmin()` | 106 | public |
| 11 | `int getPmax()` | 110 | public |
| 12 | `void init()` | 115 | public |

**Key observations:**
- Oracle-specific SQL (`sysdate`) -- same portability issue as `password_life`
- Retrieves password policy constraints (min/max lengths for userID and password)
- `EncryptTest().encrypt(userid)` called (line 69) but result unused
- SQL injection: `userid` is set but not used in the query on line 74 -- the query does not reference userid but still has the injection setup
- Connection not closed in `finally` -- resource leak
- Password policy enforcement with zero tests -- CRITICAL security gap

---

### 23. send_timezone.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/send_timezone.java` (417 lines)
**Class:** `send_timezone`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `void call_send_timezone() throws SQLException` | 27 | public |
| 2 | `void call_send_timezone_test() throws SQLException` | 132 | public |
| 3 | `void call_send_timezone_au() throws SQLException` | 254 | public |

**Key observations:**
- `call_send_timezone()` executes the INSERT query **twice** on line 86 and 88 -- duplicate timezone messages sent
- UK DST logic checks `currentMonth == 2` (March in 0-based) and `currentMonth == 9` (October) -- correct for UK
- AU DST logic uses `firstSundayOfMonth` for October/April transitions
- `call_send_timezone_test()` has commented-out DST check (line 153) -- test method with different behavior than production
- All methods hardcode state names (`'England'`, `'NSW'`, `'VIC'`, etc.) in SQL
- Complex date/timezone logic with zero test coverage -- high risk of edge-case bugs

---

### 24. send_updatepreop.java
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/send_updatepreop.java` (601 lines)
**Class:** `send_updatepreop`

| # | Method Signature | Line | Visibility |
|---|---|---|---|
| 1 | `void updatepreop() throws SQLException` | 29 | public |
| 2 | `void resyncPreop(List<String> vehTCds) throws SQLException` | 154 | public |
| 3 | `byte[] intToByteArray(int a)` | 589 | public |

**Key observations:**
- `updatepreop()` builds UPDATE query (line 109-112) but never executes it -- the `stmt.executeUpdate` call is missing
- SQL injection in both methods: string concatenation throughout
- `resyncPreop()` writes binary PREOP.TXT files to filesystem (lines 385-520) -- file content integrity is critical for firmware
- FTP credentials included in outgoing messages (line 524-528): `RuntimeConf.firmwareuser`, `RuntimeConf.firmwarepass`
- `intToByteArray()` is a utility for binary encoding -- simple but untested
- Hardcoded date `'2019-04-01'` in query (line 60)

---

## Findings

### A20-01 -- CRITICAL: GDPR Data Deletion Has Zero Test Coverage
**File:** `GdprDataDelete.java`
**Severity:** CRITICAL
**Lines:** 29-140

The `call_gdpr_delete_data()` method performs irreversible DELETE operations across 6+ database tables as part of GDPR compliance. It has:
- No unit tests validating correct deletion scope
- No tests for the 30-day inactive threshold logic
- No tests for partial failure scenarios (no transaction management)
- No tests for the `gdpr_data` interval value validation
- SQL injection via string concatenation of `cust_cd`, `driver_cd`, and `gdpr_data` values

**Tests needed:**
- Correct identification of records to delete based on `gdpr_data` retention period
- Correct cascading deletes across all 6 table pairs
- Behavior when `gdpr_data` contains invalid/malicious values
- Behavior when driver has no data to delete
- Transaction rollback on partial failure
- Behavior when connection fails mid-deletion

---

### A20-02 -- CRITICAL: Password Lifecycle Management Untested
**Files:** `password_life.java`, `password_policy.java`, `PasswordExpiryAlert.java`
**Severity:** CRITICAL
**Lines:** password_life:66-116, password_policy:64-96, PasswordExpiryAlert:13-96

Three files governing password security have zero test coverage:
- `password_life.java`: Determines if passwords are expired, tracks login history
- `password_policy.java`: Enforces password length constraints
- `PasswordExpiryAlert.java`: Sends expiry alert emails with hardcoded 3-month/7-day windows

**Specific risks:**
- Password expiry bypass if `loadDefaultValues()` silently fails (caught exception, no re-throw)
- Hardcoded expiry window (3 months) cannot be configured per-customer
- Email alert SQL injection (PasswordExpiryAlert line 69)
- Oracle-specific SQL in password_life/password_policy may fail on PostgreSQL (the database used elsewhere)

**Tests needed:**
- Password expiry calculation accuracy
- Edge cases around expiry boundaries (exactly 3 months, 3 months minus 7 days)
- Behavior when `fms_password_life` table is empty
- Email validation edge cases
- Alert idempotency (sent flag prevents re-sending)

---

### A20-03 -- CRITICAL: Hardcoded Credentials in RuntimeConf.java
**File:** `RuntimeConf.java`
**Severity:** CRITICAL
**Lines:** 20, 30, 54-55, 87-88

Multiple production credentials are hardcoded in source code:
- FTP firmware password: `"Sdh79HfkLq6"` (line 30)
- Legacy firmware password: `"ciifirmware"` (line 20)
- Test credentials: `"TestK"/"testadmin"` (lines 54-55)
- SMS API credentials: `"fOqDVWYK"` / API ID `"3259470"` (lines 87-88)

While no test can directly fix this, the absence of any configuration management testing means:
- No validation that credentials are loaded from secure sources
- No tests ensuring `RuntimeConf` values are overridden by external configuration
- Credentials are committed to version control and visible to all developers

---

### A20-04 -- HIGH: SQL Injection Across All Database-Interacting Files
**Files:** All 24 files except `PurgeData.java`, `escapeSingleQuotes.java`, `RuntimeConf.java`
**Severity:** HIGH
**Lines:** Pervasive

Every file that executes SQL uses string concatenation instead of prepared statements. Key examples:
- `InfoLogger.java` line 59: `"SELECT EMP_CD FROM HR_EMP_MST WHERE EMP_NM='"+tuid+"'"`
- `PasswordExpiryAlert.java` line 69: email/subject/message concatenated into INSERT
- `SupervisorMasterHelper.java` line 39: `user` concatenated into SELECT
- `UtilBean.java` line 86: `webUserCD` concatenated into SELECT
- `LogicBean_filter.java` line 122: `set_gp_cd` concatenated into SELECT

The `escapeSingleQuotes.java` class provides only single-quote doubling, which is insufficient protection against SQL injection. No tests exist to validate any escaping or parameterization.

**Tests needed:**
- Input containing `'; DROP TABLE --` should not execute
- Unicode/multi-byte bypass attempts
- Null byte injection
- Each public method should be tested with adversarial input

---

### A20-05 -- HIGH: Email Sending Functions Always Return True
**Files:** `mail.java`, `call_mail.java`
**Severity:** HIGH
**Lines:** mail.java:109-145, 147-203, 205-259

All `sendMail` variants return `true` regardless of whether the email was actually sent:
- `sendMail()` (line 144): returns `true` even after catching `Throwable`
- `sendMail(..attachment..)` (line 202): same pattern
- `sendMailAttachment()` (line 258): same pattern

**Impact:** Callers cannot detect email delivery failures. Password reset emails, alert notifications, and report deliveries may silently fail with no indication to the system or user.

**Tests needed:**
- Verify return value on successful send
- Verify return value on transport failure
- Verify return value on invalid recipient address
- Verify attachment file cleanup after send

---

### A20-06 -- HIGH: ImportFiles Servlet Has No Authorization or Input Validation Tests
**File:** `ImportFiles.java`
**Severity:** HIGH
**Lines:** 49-2300

The `ImportFiles` servlet handles file uploads and directly modifies database records (drivers, vehicles, questions). It has:
- No authentication/authorization checks visible in the code
- No file-type validation (any file accepted)
- No file-size enforcement
- File path construction via simple concatenation (line 85) -- potential path traversal
- Complex CSV parsing and validation logic (~2700 lines) with zero test coverage
- Multiple import paths (drivers, driversUK, driversAU, questions, vehicles) each with distinct validation rules

**Tests needed:**
- CSV parsing with malformed input
- Path traversal in file names
- Oversized file handling
- Each import type's validation rules
- Authorization bypass attempts

---

### A20-07 -- HIGH: Data Migration (MigrateMaster) Has No Rollback Protection
**File:** `MigrateMaster.java`
**Severity:** HIGH
**Lines:** 18-323

`callMigrateMaster()` performs a complex multi-table data migration for all active customers without transaction boundaries. A failure mid-migration leaves the database in an inconsistent state:
- Deletes from `FMS_LOC_OVERRIDE` (line 60)
- Inserts into `FMS_LOC_OVERRIDE` (line 95)
- Updates `FMS_USR_MST.supervisor_access` (line 100)
- Similar operations for department-level (lines 277-291)

**Tests needed:**
- Successful full migration for a single customer
- Behavior when customer has no vehicles
- Behavior when database error occurs mid-migration
- Verification that `supervisor_access` is correctly set

---

### A20-08 -- HIGH: Department Fix Utility Modifies 12 Tables Without Transaction
**File:** `fix_department.java`
**Severity:** HIGH
**Lines:** 97-306

`fix_dept()` cascades department code changes across 12 database tables:
`FMS_DEPT_MST`, `FMS_CUST_DEPT_REL`, `FMS_OPCHK_QUEST_MST`, `FMS_USER_DEPT_REL`, `FMS_USR_VEHICLE_REL`, `dayhours`, `fms_can_input_settings`, `fms_impact_month_cache`, `fms_impact_month_driver_cache`, `fms_monthly_rpt_subscription`, `mymessages_users`, `FMS_EMAIL_CONF`, `site_settings_by_hour`

No transaction wrapping means a failure at any point (e.g., table 7 of 12) leaves referential integrity broken.

**Tests needed:**
- Correct duplicate detection logic
- Full cascade completion
- Rollback behavior on failure
- Edge case: department code that does not exist

---

### A20-09 -- HIGH: Timezone Commands May Be Sent Twice
**File:** `send_timezone.java`
**Severity:** HIGH
**Lines:** 86-88

In `call_send_timezone()`, the INSERT query is executed twice:
```java
stmte1.executeUpdate(query);  // line 86

stmte1.executeUpdate(query);  // line 88
```
This causes every vehicle to receive duplicate timezone messages on DST transition days.

**Tests needed:**
- Verify single message per vehicle per DST transition
- UK DST boundary detection (last Sunday of March/October)
- AU DST boundary detection (first Sunday of October/April)

---

### A20-10 -- MEDIUM: InfoLogger SQL Injection and String Parsing Vulnerability
**File:** `InfoLogger.java`
**Severity:** MEDIUM
**Lines:** 28-83

`writelog()` parses the `msg` parameter with `indexOf('/')` and `indexOf(']')` without bounds checking. If the message format deviates (no `/` or `]` character), `substring()` throws `StringIndexOutOfBoundsException`, crashing the logger. The extracted `uid`, `mid`, and `rem` values are directly inserted into SQL.

**Tests needed:**
- Messages with expected format
- Messages missing `/` delimiter
- Messages missing `]` delimiter
- Messages with SQL injection payloads in the username field

---

### A20-11 -- MEDIUM: LindeConfig XML Parsing Vulnerable to XXE
**File:** `LindeConfig.java`
**Severity:** MEDIUM
**Lines:** 63-65

`DocumentBuilderFactory` is used without disabling external entities:
```java
DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
Document doc = dBuilder.parse(fXmlFile);
```

If the XML file is tampered with, XXE attacks could read local files or perform SSRF.

**Tests needed:**
- Valid XML configuration parsing
- Missing XML file handling
- Malformed XML handling
- XXE payload rejection

---

### A20-12 -- MEDIUM: Menu_Bean1 Leaks SQL Query to UI
**File:** `Menu_Bean1.java`
**Severity:** MEDIUM
**Lines:** 192-197

In `fetchSubModule()`, the raw SQL query string is appended to the `FormName` ArrayList:
```java
FormName.add(query1);   // line 192
FormId.add("");          // line 193
```
This means the SQL query is exposed to the JSP page rendering the menu, leaking database schema information to users.

**Tests needed:**
- Verify `FormName` does not contain SQL queries
- Verify all list entries are valid form names

---

### A20-13 -- MEDIUM: GetHtml Potential SSRF
**File:** `GetHtml.java`
**Severity:** MEDIUM
**Lines:** 16-38

`getHTML(urlToRead, param)` constructs a URL by concatenation without any validation or allow-listing:
```java
url = new URL(urlToRead+param);
```
If `urlToRead` or `param` is user-controlled, this enables Server-Side Request Forgery (SSRF) to access internal resources.

**Tests needed:**
- URL validation/allowlisting behavior
- Behavior with internal/private IP addresses
- Behavior with protocol handlers (file://, ftp://)
- Timeout handling
- Connection cleanup on error

---

### A20-14 -- MEDIUM: escapeSingleQuotes Provides Insufficient SQL Protection
**File:** `escapeSingleQuotes.java`
**Severity:** MEDIUM
**Lines:** 4-16

The `replaceSingleQuotes()` method only doubles single quotes. It does not handle:
- Backslash escaping (`\'`)
- Null byte injection
- Unicode bypass attacks
- Other SQL metacharacters

This class appears to be the primary SQL escaping utility, but it is not used consistently (most code concatenates without even calling this).

**Tests needed:**
- Single quote escaping correctness
- Backslash handling
- Null/empty input
- Unicode characters
- Multi-byte character sequences

---

### A20-15 -- MEDIUM: UtilBean Thread-Safety Issue
**File:** `UtilBean.java`
**Severity:** MEDIUM
**Lines:** 29, 178-233, 235-288

The `static CustomerBean customer` field (line 29) is shared across all threads. Both `getCustomerSettingByUser()` and `getCustomerSetting()` write to this field and then return it. In a concurrent servlet environment, one thread's result can overwrite another's.

**Tests needed:**
- Concurrent access to `getCustomerSettingByUser()` from multiple threads
- Verify correct `CustomerBean` returned for each caller

---

### A20-16 -- MEDIUM: send_updatepreop Builds But Never Executes UPDATE Query
**File:** `send_updatepreop.java`
**Severity:** MEDIUM
**Lines:** 106-116

In `updatepreop()`, the UPDATE query is built but `stmte.executeUpdate(query)` or equivalent is never called:
```java
if(!mst_questions.get(i).getQuestion().equals(ans_questions.get(i))){
    query = "update \"op_chk_checklistanswer\" set ..."  // builds query
    // NO executeUpdate() call
}
```
This means the pre-op question text correction is silently non-functional.

**Tests needed:**
- Verify that mismatched questions are actually updated
- Verify correct question text after update

---

### A20-17 -- LOW: PurgeData Class Is Empty
**File:** `PurgeData.java`
**Severity:** LOW
**Lines:** 1-5

The `PurgeData` class is completely empty -- no methods, no fields. Either it is dead code or an unfinished implementation. If data purging is required (e.g., for GDPR compliance beyond what `GdprDataDelete` does), this represents a missing feature.

---

### A20-18 -- LOW: SendMessage Uses Deprecated API Methods
**File:** `SendMessage.java`
**Severity:** LOW
**Lines:** 177, 236

- `URLEncoder.encode(message)` (line 177) uses deprecated single-arg method (platform-default encoding)
- `dis.readLine()` (line 236) -- `DataInputStream.readLine()` has been deprecated since Java 1.1

**Tests needed:**
- SMS message encoding with special characters
- Multi-line response parsing from Clickatell API

---

## Summary Statistics

| Metric | Count |
|---|---|
| Files analyzed | 24 |
| Total public methods identified | ~120+ |
| Methods with test coverage | 0 |
| Coverage percentage | 0% |
| CRITICAL findings | 3 (A20-01, A20-02, A20-03) |
| HIGH findings | 6 (A20-04 through A20-09) |
| MEDIUM findings | 7 (A20-10 through A20-16) |
| LOW findings | 2 (A20-17, A20-18) |
| **Total findings** | **18** |

## Priority Recommendations for Test Implementation

1. **FIRST:** `GdprDataDelete.java` -- GDPR compliance requires verified deletion behavior
2. **SECOND:** `PasswordExpiryAlert.java`, `password_life.java`, `password_policy.java` -- Security-critical password lifecycle
3. **THIRD:** `ImportFiles.java` -- Externally-facing servlet with file upload and complex validation
4. **FOURTH:** `MigrateMaster.java`, `fix_department.java` -- Data integrity for multi-table operations
5. **FIFTH:** `SupervisorMasterHelper.java` -- Security-relevant access control modifications
6. **SIXTH:** All remaining files -- SQL injection and error handling coverage
