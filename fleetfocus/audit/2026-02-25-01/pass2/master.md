# Pass 2 -- Test Coverage: master package
**Agent:** A15
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

---

## Test Infrastructure Assessment

| Aspect | Status |
|---|---|
| Test framework (JUnit/TestNG) | **ABSENT** -- no JUnit or TestNG dependencies detected |
| Test source directories (`test/`, `src/test/`) | **ABSENT** -- no test directories exist |
| Test files in codebase | **ZERO** -- one file named `EncryptTest.java` exists but is a decompiled utility class with no test annotations or assertions |
| Test runner configuration (Maven Surefire, Gradle test) | **ABSENT** -- no build tool test configuration found |
| Mocking libraries (Mockito, EasyMock) | **ABSENT** |
| Integration test infrastructure | **ABSENT** |
| Code coverage tools (JaCoCo, Cobertura) | **ABSENT** |

**Conclusion:** The repository has absolutely zero automated tests. Every public method, every code path, every error condition in all 7 assigned files is completely untested. The overall test coverage for this package is **0%**.

---

## Reading Evidence

### 1. Databean_customer.java (3,009 lines)

**Full path:** `WEB-INF/src/com/torrent/surat/fms6/master/Databean_customer.java`
**Class:** `public class Databean_customer`
**Purpose:** Data access bean for customer/user management. Called directly from JSP pages via `query(String op_code)` dispatcher.

**Key public methods (non-getter/setter):**

| Line | Signature | Description |
|---|---|---|
| 331 | `public void query(String op_code)` | Main dispatcher -- connects to DB, routes to sub-queries based on op_code string comparison |
| 547 | `public void Query_Viewable_Battery() throws SQLException` | Queries viewable battery menu items |
| 578 | `public void Query_Viewable_Settings() throws SQLException` | Queries viewable settings menu items |
| 600 | `public void Query_Viewable_Reports() throws SQLException` | Queries viewable reports menu |
| 634 | `public void Query_Viewable_Menu() throws SQLException` | Queries viewable dashboard menu |
| 725 | `public void Query_User_Form_Menu() throws SQLException` | Queries user form menu permissions |
| 804 | `public void queryBlacklist() throws SQLException` | Queries driver blacklist |
| 871 | `public void querySupervisorList() throws SQLException` | Queries supervisor list by site/dept |
| 957 | `public void Query_User_Access_Restriction() throws SQLException` | Queries vehicle access mapper |
| 1029 | `public void Query_All_Models_By_Cus_Loc_Dept() throws SQLException` | Queries models filtered by customer/location/dept |
| 1163 | `public void Query_All_Models_By_Cus_Loc_Dept_va() throws SQLException` | Variant for vehicle access view |
| 1246 | `public void Query_Current_Alert() throws SQLException` | Queries current alert detail |
| 1289 | `public void Query_Alerts() throws SQLException` | Queries all alerts with vehicle conditions |
| 1387 | `public void Query_Groups_By_Cust() throws SQLException` | Queries access groups by customer |
| 1430 | `public void Query_Access_Groups() throws SQLException` | Queries all access groups |
| 1472 | `public void Query_Current_User() throws SQLException` | Queries current user details (dual AU/non-AU paths) |
| 1696 | `public void Query_All_Models() throws SQLException` | Queries all vehicle models for customer |
| 1713 | `public void Query_Driver_License() throws SQLException` | Queries driver license expiry |
| 1745 | `public void Query_Driver_License_au() throws SQLException` | AU-specific driver license query |
| 1763 | `public void Query_CustomersUsers() throws SQLException` | Queries customers filtered by access level |
| 1792 | `public void Query_Customers() throws SQLException` | Queries customers with search |
| 1835 | `public void Query_all_Customers() throws SQLException` | Queries all customers |
| 1871 | `public void Query_Locations() throws SQLException` | Queries locations for customer |
| 1937 | `public void Query_Locations_Old() throws SQLException` | Legacy location query |
| 1967 | `public void QueryEditUserDepartments() throws SQLException` | Queries departments for user edit |
| 1992 | `public void Query_Departments() throws SQLException` | Queries departments with filters |
| 2028 | `public void Query_User() throws SQLException` | Queries single user |
| 2049 | `public void Query_Permits() throws SQLException` | Queries form permissions |
| 2078 | `public void Query_Users() throws SQLException` | Queries paginated user list |
| 2327 | `public void Query_Users_xls() throws SQLException` | Queries users for Excel export |
| 2567 | `public void Query_My_profile() throws SQLException` | Queries current user profile |
| 2600 | `public void Query_Customer_Data() throws SQLException` | Queries full customer data |
| 2960 | `public void Query_Bonus_Module() throws SQLException` | Queries bonus modules |

**Public getter/setter count:** ~170+ getter/setter methods for ArrayLists and String fields (lines 189-3003)

---

### 2. Databean_getter.java (5,469 lines)

**Full path:** `WEB-INF/src/com/torrent/surat/fms6/master/Databean_getter.java`
**Class:** `public class Databean_getter`
**Purpose:** Large data access bean for vehicle, location, department, and device management queries. Follows same JSP-called pattern.

**Key public methods (non-getter/setter -- sampled from grep output):**

| Line | Signature | Description |
|---|---|---|
| 160 | `public String getType()` | Vehicle type getter |
| 196 | `public Boolean getFms_Vechile_Data_MK3_Version()` | MK3 version flag |
| 397 | `public ArrayList getFms_Vehicle_List_CCID()` | CCID list getter |
| ~450+ | Multiple `public void Query_*()` methods | Various database query methods similar to Databean_customer |

**Note:** Due to file size (5,469 lines), this file contains hundreds of public getter/setter methods and numerous `Query_*` database access methods, all following the same string-concatenated SQL pattern.

---

### 3. Databean_getuser.java (10,675 lines)

**Full path:** `WEB-INF/src/com/torrent/surat/fms6/master/Databean_getuser.java`
**Class:** `public class Databean_getuser`
**Purpose:** Largest data access bean. Handles user, vehicle, alert, checklist, firmware, service, and override data retrieval.

**Key public methods:**

| Line | Signature | Description |
|---|---|---|
| 464 | `public void clear_variables()` | Clears all ArrayLists to avoid stale data |
| 990 | `public ArrayList getP_id()` | Process ID list |
| 5383 | `public void Query_Current_User() throws SQLException` | Queries current user customer/site/dept |
| 5199 (Frm_saveuser) | -- | -- |

**Key private query methods (sampled):** `Fetch_opchk_quest()`, `Fetch_opchk_unsyncquest()`, `Fetch_sel_quest()` and many more.

**Public getter/setter count:** ~300+ getter/setter methods across 10,675 lines.

---

### 4. Databean_user.java (45 lines)

**Full path:** `WEB-INF/src/com/torrent/surat/fms6/master/Databean_user.java`
**Class:** `public class Databean_user`
**Purpose:** Empty shell class with imports and field declarations but no methods.

**Public methods:** NONE -- class body is empty (lines 29-45).

**Fields declared:** `Connection conn`, `Statement stmt/stmt1/stmt2`, `ResultSet rset/rset1/rset2`, `String methodName`, `String query`, `String queryString`.

---

### 5. FirmwareverBean.java (255 lines)

**Full path:** `WEB-INF/src/com/torrent/surat/fms6/master/FirmwareverBean.java`
**Class:** `public class FirmwareverBean`
**Purpose:** Value bean for firmware version parsing and display. Converts hex firmware version strings into human-readable format.

**Public methods:**

| Line | Signature | Description |
|---|---|---|
| 14 | `public String getVeh_id()` | Vehicle ID getter |
| 18 | `public void setVeh_id(String veh_id)` | Vehicle ID setter |
| 22 | `public String getGmtp_id()` | GMTP ID getter |
| 26 | `public void setGmtp_id(String gmtp_id)` | GMTP ID setter |
| 30 | `public String getFirm_vers()` | Firmware version getter |
| 34 | `public void setFirm_vers(String firm_vers)` | Firmware version setter |
| 38 | `public void setCurr_ver(String version)` | **CRITICAL** -- Parses hex firmware version, routes to 32-bit or 64-bit converter |
| 51 | `public void setCurr_ver_edit(String version)` | Direct setter bypass |
| 56 | `public void setCurr_ver()` | Sets default dash value |
| 61 | `public String getRep_time()` | Report time getter |
| 65 | `public void setRep_time(String rep_time)` | Report time setter |
| 69 | `public String getHire_no()` | Hire number getter |
| 73 | `public void setHire_no(String hire_no)` | Hire number setter |
| 77 | `public String getType()` | Type getter |
| 81 | `public void setType(String type)` | Type setter |
| 85 | `public String getCurr_ver()` | Current version getter |
| 211 | `public String getType(String version)` | **CRITICAL** -- Parses hex version to extract type field |
| 245 | `public String getMk3dbg()` | MK3 debug getter |
| 249 | `public void setMk3dbg(String mk3dbg)` | MK3 debug setter |

**Private methods:**

| Line | Signature | Description |
|---|---|---|
| 89 | `private void convert32bit(String version)` | Parses 32-bit hex firmware version |
| 179 | `private void convert64bit(String version)` | Parses 64-bit hex firmware version |

---

### 6. Frm_saveuser.java (10,930 lines)

**Full path:** `WEB-INF/src/com/torrent/surat/fms6/master/Frm_saveuser.java`
**Class:** `public class Frm_saveuser extends HttpServlet implements SingleThreadModel`
**Purpose:** Servlet handling ALL save/update/delete operations for users, vehicles, customers, alerts, groups, departments, locations, checklist questions, firmware, and more. The `doPost` method dispatches to ~70+ private handler methods based on `op_code` parameter.

**Public methods:**

| Line | Signature | Description |
|---|---|---|
| 54 | `protected void doPost(HttpServletRequest req, HttpServletResponse res)` | Main servlet entry point -- dispatches to 70+ operations |
| 449 | `public void clearVectors()` | Empty method |
| 5199 | `public boolean isValidEmailAddress(String email)` | Email validation via regex |

**Private handler methods (70+ methods, key ones listed):**

| Line | Method | Description |
|---|---|---|
| 455 | `weigand_to_card_iclass(String)` | Card ID conversion |
| 466 | `weigand_to_card(String, String, String)` | Weigand card conversion |
| 718 | `card_to_weigand_iclass_even(String, String)` | Card-to-weigand even parity |
| 796 | `card_to_weigand_iclass_odd(String, String)` | Card-to-weigand odd parity |
| 875 | `card_to_weigand_smart_even(String, String)` | Smart card conversion |
| 927 | `card_to_hidiclass(String)` | HID iClass conversion |
| 938 | `card_to_weigand_chubb(String, String)` | Chubb card conversion |
| 991 | `card_to_weigand_au(String, String, String, String)` | AU card conversion |
| 1281 | `save_group(HttpServletRequest)` | Save group |
| 1334 | `save_group_rel(HttpServletRequest, HttpServletResponse)` | Save group relation |
| 1391 | `save_division(HttpServletRequest)` | Save division |
| 1447 | `save_department(HttpServletRequest)` | Save department |
| 1560 | `save_veh_type(HttpServletRequest)` | Save vehicle type |
| 1800 | `save_loc(HttpServletRequest)` | Save location |
| 1973 | `driver_setup(HttpServletRequest)` | Driver setup |
| 2300 | `conf_driv_setting_ftp(HttpServletRequest)` | Configure driver settings via FTP |
| 2864 | `driv_blacklist(HttpServletRequest)` | Driver blacklist management |
| 4108 | `save_user(HttpServletRequest)` | **CRITICAL** -- Save/update user with all fields |
| 4382 | `del_user(HttpServletRequest)` | Delete (deactivate) user |
| 4450 | `active_user(HttpServletRequest)` | Activate/deactivate user |
| 4641 | `save_driver(HttpServletRequest)` | Save driver |
| 5014 | `save_customer_new(HttpServletRequest, HttpServletResponse)` | Save new customer |
| 5207 | `save_new_vehicle(HttpServletRequest, HttpServletResponse)` | Save new vehicle |
| 5842 | `save_vehicle(HttpServletRequest)` | Save vehicle |
| 6620 | `save_cust_vehicle(HttpServletRequest)` | Save customer-vehicle relationship |
| 8004 | `upload_quest_ftp(HttpServletRequest)` | Upload checklist via FTP |
| 8934 | `del_alert(HttpServletRequest)` | Delete alert |
| 9102 | `save_alert(HttpServletRequest)` | Save alert |
| 10706 | `sendoutgoingmessage(HttpServletRequest)` | Send outgoing message |

---

### 7. Frm_upload.java (162 lines)

**Full path:** `WEB-INF/src/com/torrent/surat/fms6/master/Frm_upload.java`
**Class:** `public class Frm_upload extends HttpServlet`
**Purpose:** Servlet for file upload handling (image/logo uploads).

**Public methods:**

| Line | Signature | Description |
|---|---|---|
| 46 | `public void init()` | Servlet init -- acquires DB connection |
| 69 | `protected void doPost(HttpServletRequest req, HttpServletResponse res)` | Handles multipart file upload |
| 102 | `public void clearVectors()` | Empty method |

**Private methods:**

| Line | Signature | Description |
|---|---|---|
| 109 | `private void loadData(HttpServletRequest request)` | **CRITICAL** -- Parses multipart request, writes files to disk |

---

## Findings

### A15-01 -- SQL Injection via String Concatenation in Databean_customer.query()
**Severity:** CRITICAL
**File:** `Databean_customer.java`
**Lines:** 331-534 (dispatcher) plus all Query_* methods (547-2989)

**Detail:** The `query(String op_code)` method and every `Query_*` sub-method construct SQL statements by directly concatenating instance field values (e.g., `Param_User`, `Param_Customer`, `Param_Site`, `Param_Department`, `Param_Search`, `Param_Module`, `access_user`, `access_cust`, `access_site`, `access_dept`, `user_cd`) into query strings without parameterized queries or input sanitization.

**Examples:**
- Line 551: `...\"USER_CD\" ='"+Param_User+"' AND...`
- Line 806: `...\"USER_CD\" = " + Param_User` (no quotes)
- Line 1818: `...\"USER_NAME\" ilike '%"+Param_Search+"%' and...`
- Line 2212: `...\"USER_NAME\" ilike '%"+Param_Search+"%'...` (search parameter injected directly)

**Tests needed:**
- Parameterized query behavior with malicious input strings
- SQL injection vectors through every `setParam_*` setter
- Boundary testing on all `access_*` fields that are directly interpolated into SQL IN clauses
- Empty string, null, and special character handling for every parameter

---

### A15-02 -- SQL Injection via String Concatenation in Frm_saveuser (All 70+ Operations)
**Severity:** CRITICAL
**File:** `Frm_saveuser.java`
**Lines:** 4108-4380 (`save_user`), plus all other handler methods

**Detail:** The `save_user` method (and virtually all other private methods) construct INSERT/UPDATE/DELETE SQL statements by concatenating `request.getParameter()` values directly into SQL strings. No prepared statements are used anywhere.

**Examples:**
- Line 4234: `"select count(*) from \"FMS_USR_MST\" where \"USER_NAME\" = '"+user_nm+"'"`
- Line 4265-4270: Full INSERT statement with ~22 concatenated parameter values
- Line 4298-4305: Full UPDATE statement with all user fields concatenated
- Line 4394: `"select \"CARD_ID\" from \"FMS_USR_MST\" where \"USER_CD\" = "+uid`

**Tests needed:**
- Input validation for every request parameter
- SQL injection testing for every operation handler
- Prepared statement replacement verification
- Transaction integrity for multi-statement operations

---

### A15-03 -- SQL Injection in Databean_getuser (10,675 Lines of Concatenated SQL)
**Severity:** CRITICAL
**File:** `Databean_getuser.java`
**Lines:** Throughout (5,383-5,395 shown as example, but pervasive)

**Detail:** This is the largest file in the package (10,675 lines). All query methods use string concatenation with setter-injected values. `set_cust_cd`, `set_loc_cd`, `set_dept_cd`, `set_veh_typ_cd`, `set_ques_no`, and `Param_User` are directly interpolated into SQL.

**Examples:**
- Line 5388: `"WHERE \"USER_CD\" = "+Param_User` (direct numeric injection)
- Line 5414: `"\"USER_CD\" = '" + set_cust_cd + "'"`
- Line 5424: `"\"LOC_CD\" = '" + set_loc_cd + "'"`
- Line 5447: `"\"VEHICLE_TYPE_CD\" = " + set_veh_typ_cd` (no quotes, numeric injection)

**Tests needed:**
- Parameterized query testing for all ~40+ private query methods
- Input validation for all setter-injected values
- Boundary testing for combined multi-field queries

---

### A15-04 -- Unrestricted File Upload in Frm_upload.loadData()
**Severity:** CRITICAL
**File:** `Frm_upload.java`
**Lines:** 109-156

**Detail:** The `loadData` method accepts file uploads with no validation of:
1. **File type/extension** -- no allowlist for permitted file types (line 137: `fitem.write(f)` writes any file)
2. **File size** -- no size limit configured on `DiskFileItemFactory` or `ServletFileUpload`
3. **File name** -- filename is derived from uploaded name with only a random prefix (lines 131-135): `ran.nextInt(1000) + "_" + fitem.getName().substring(fitem.getName().lastIndexOf('\\') + 1)` -- insufficient randomness (only 0-999), platform-specific path parsing (backslash only)
4. **Destination path** -- files are written to the web-accessible `/images/pics/` directory (line 116), enabling direct execution of uploaded scripts
5. **Filename injection** -- the uploaded filename (returned in JSON on line 150) is not sanitized and could contain path traversal characters

**Tests needed:**
- Malicious file type upload (e.g., `.jsp`, `.war`, `.exe`)
- Path traversal in filename (e.g., `../../WEB-INF/web.xml`)
- File size limits
- Filename collision (random prefix only 0-999)
- Platform-independent path separator handling
- JSON response injection via malicious filenames

---

### A15-05 -- Password Stored and Transmitted in Plaintext
**Severity:** CRITICAL
**File:** `Frm_saveuser.java` (line 4119, 4199, 4268, 4298, 4310) and `Databean_customer.java` (line 1535, 1612, 2838)
**Lines:** Multiple

**Detail:** Passwords are:
1. Read from HTTP request parameter as plaintext (line 4119: `request.getParameter("pass")`)
2. Only escape for single quotes is applied (line 4199: `password.replace("'", "''")`) -- no hashing
3. Stored directly in the database as plaintext in INSERT/UPDATE (lines 4268, 4298)
4. Retrieved from database and exposed through getter `getCurrent_User_Password()` (line 2838)

**Tests needed:**
- Password hashing before storage
- Password field not returned in query results
- Password strength validation
- Secure password comparison (constant-time)

---

### A15-06 -- Null Pointer Exception Risk in Databean_customer.Query_Customers()
**Severity:** HIGH
**File:** `Databean_customer.java`
**Line:** 1814

**Detail:** Line 1814 contains a guaranteed NPE bug: `if( Param_Search == null && Param_Search.equalsIgnoreCase(""))`. If `Param_Search` is null, the first condition is true, and then `Param_Search.equalsIgnoreCase("")` is called on a null reference, throwing NPE. This same bug exists at line 1854 in `Query_all_Customers()`.

**Tests needed:**
- Null parameter handling for `Param_Search`
- Unit tests for `Query_Customers()` with null, empty, and valid search strings
- Same test for `Query_all_Customers()`

---

### A15-07 -- NumberFormatException Risk in FirmwareverBean Version Parsing
**Severity:** HIGH
**File:** `FirmwareverBean.java`
**Lines:** 38-49, 89-177, 179-209, 211-243

**Detail:** The `setCurr_ver(String version)` method calls `Long.parseLong(version, 16)` (line 94 and line 185) which will throw `NumberFormatException` for non-hex input. While `convert64bit` has a catch for this (lines 186-188), `convert32bit` does not -- it will crash on invalid hex input. Additionally:
- Line 40: `version.equalsIgnoreCase(null)` compiles but is always false -- should be `version == null`
- Line 212: Same `version.equalsIgnoreCase(null)` bug in `getType(String version)`
- Lines 219-221, 230-234: After catching `NumberFormatException`, the code tries `version.substring(1)` then re-parses, which can throw another `NumberFormatException` or `StringIndexOutOfBoundsException` if version is a single character

**Tests needed:**
- Valid hex strings of various lengths (< 15, >= 15)
- Invalid hex strings (non-hex characters)
- Empty strings, single-character strings
- Null input handling
- Boundary at length exactly 15
- Version "0.0.0" output verification
- Overflow testing for Long.parseLong

---

### A15-08 -- Connection/Resource Leak in Frm_upload
**Severity:** HIGH
**File:** `Frm_upload.java`
**Lines:** 46-67 (init), 69-100 (doPost)

**Detail:** Multiple resource management issues:
1. `init()` acquires a DB connection and creates statements as instance fields (lines 55-62), but these are never closed
2. `doPost()` acquires ANOTHER DB connection (line 80) and creates statements, potentially leaking the one from `init()`
3. `doPost()` references `stmt1` at line 90 (`stmt1.close()`) but `stmt1` is only created in `init()`, not in `doPost()` -- if `init()` failed, this is null
4. `dbcon.commit()` is called (line 92) but no transaction was explicitly started
5. If `loadData()` throws, the connection at line 80 is still closed, but the `init()` connection leaks
6. No try-with-resources or finally block for statement/connection cleanup in `doPost()`

**Tests needed:**
- Connection lifecycle testing
- Resource leak detection under error conditions
- Concurrent request handling (shared mutable state)
- Statement null-safety testing

---

### A15-09 -- Thread Safety Issues in Frm_saveuser (SingleThreadModel Deprecation)
**Severity:** HIGH
**File:** `Frm_saveuser.java`
**Line:** 35

**Detail:** The class implements `javax.servlet.SingleThreadModel` (deprecated since Servlet 2.4) and uses `@SuppressWarnings("deprecation")` to hide the warning. This interface does not guarantee thread safety in modern containers and its use is discouraged. Meanwhile, the class stores request-scoped data in instance fields (`dbcon`, `stmt`, `rset`, `op_code`, `form_cd`, `url`, `message`) -- lines 38-49 -- making it inherently unsafe for concurrent requests.

**Tests needed:**
- Concurrent request simulation
- Race condition testing on shared instance fields
- Connection pool exhaustion under concurrent load
- State leakage between requests

---

### A15-10 -- Absence of Input Validation in Frm_saveuser.save_user()
**Severity:** HIGH
**File:** `Frm_saveuser.java`
**Lines:** 4108-4380

**Detail:** The `save_user()` method reads ~25+ parameters from the HTTP request and passes them directly into SQL without any validation:
- No email format validation (email is stored directly)
- No phone number format validation
- No length checks on any field
- No character restrictions on names, descriptions, addresses
- `user_lnm.substring(0,3)` at line 4223 will throw `StringIndexOutOfBoundsException` if `user_lnm` is exactly 2 chars (the `else if` guard at line 4225 only catches `length() > 1`, but the code path at 4221 requires `length() > 2`)
- No validation of `access_cd` value (should be 1-5)
- No validation of `cust_cd`, `site_cd`, `dept_cd` as numeric

**Tests needed:**
- Every parameter with null, empty, overlength, and special character input
- Email validation
- Numeric field validation
- Username generation logic with edge case last names (0, 1, 2, 3 chars)
- Access level bounds checking

---

### A15-11 -- Hardcoded Customer Name Logic in Query_Alerts()
**Severity:** MEDIUM
**File:** `Databean_customer.java`
**Lines:** 1296-1306

**Detail:** Line 1303 contains a hardcoded check: `if (!cust_name.equalsIgnoreCase("James Hardie Australia"))`. This means the `unauthorised_driver` alert type is only excluded for a specific customer by name comparison, creating a brittle business logic dependency.

**Tests needed:**
- Alert filtering logic with various customer names
- Behavior when customer name changes
- Case sensitivity testing

---

### A15-12 -- Weak Email Validation Regex in Frm_saveuser
**Severity:** MEDIUM
**File:** `Frm_saveuser.java`
**Lines:** 5199-5205

**Detail:** The `isValidEmailAddress(String email)` method uses regex pattern `^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$` which:
1. The dot after `[a-zA-Z0-9-]+` is unescaped, matching ANY character (not just literal dot)
2. Allows emails like `user@hostXcom` (where X is any character)
3. Does not validate TLD length or structure
4. A separate `isValidEmail` method (around line 5185) uses `InternetAddress.validate()` which is more robust but it is unclear which one is actually called

**Tests needed:**
- Valid email addresses (standard, subdomain, international)
- Invalid email addresses (missing @, double dots, special chars)
- The unescaped dot regex flaw
- Comparison of the two validation methods

---

### A15-13 -- Empty Databean_user Class May Indicate Dead Code or Incomplete Refactoring
**Severity:** LOW
**File:** `Databean_user.java`
**Lines:** 1-45

**Detail:** The class declares 10 fields (Connection, Statements, ResultSets, Strings) but has ZERO methods. It imports 15 packages including FTPClient, BeanComparator, DayhoursBean, and reflection -- none of which are used. This appears to be either dead code or an incomplete refactoring artifact.

**Tests needed:**
- Determine if this class is referenced anywhere in the codebase
- If referenced, test that it behaves as expected (currently does nothing)
- If unused, mark for removal

---

### A15-14 -- Shared Mutable State Across Requests in Frm_upload
**Severity:** MEDIUM
**File:** `Frm_upload.java`
**Lines:** 26-44

**Detail:** `Frm_upload` extends `HttpServlet` and stores all operational state as instance fields: `dbcon`, `stmt`, `rset`, `message`, `url`, `op_code`, `date`, `veh_typ_cd`. In a multi-threaded servlet container, concurrent requests will corrupt each other's state. Unlike `Frm_saveuser`, this class does NOT implement `SingleThreadModel` (even though that is also deprecated and inadequate).

**Tests needed:**
- Concurrent upload requests
- State isolation between requests
- Connection sharing issues

---

### A15-15 -- Insufficient Error Handling and Information Leakage
**Severity:** MEDIUM
**Files:** All files

**Detail:** Error handling across all files follows a dangerous pattern:
1. `Frm_upload.java` line 153-154: Exception message exposed to user in JSON: `e.getMessage().toString()`
2. `Databean_customer.java` line 479: Full exception printed to stdout: `System.out.println("Exception in Databean_customer...")` with query details
3. `Frm_saveuser.java` line 406-407: `e.printStackTrace()` plus `System.out.println`
4. No structured logging in Databean classes (only `Frm_saveuser` uses log4j)

**Tests needed:**
- Exception message content (should not contain SQL or stack traces)
- Error recovery and transaction rollback
- Logging adequacy and PII filtering

---

### A15-16 -- FirmwareverBean.getType(String) Missing Catch for Short Strings After NumberFormatException
**Severity:** MEDIUM
**File:** `FirmwareverBean.java`
**Lines:** 211-243

**Detail:** In `getType(String version)`, if `Long.parseLong(version, 16)` throws `NumberFormatException` (lines 219, 231), the code does `version = version.substring(1)` and then retries parsing. If the original version is a single character (e.g., `"G"`), `substring(1)` returns `""`, and `Long.parseLong("", 16)` throws another `NumberFormatException` that is NOT caught.

**Tests needed:**
- Single character non-hex input
- Empty string after substring
- Cascading exception handling

---

## Summary

| Severity | Count |
|---|---|
| CRITICAL | 5 (A15-01 through A15-05) |
| HIGH | 5 (A15-06 through A15-10) |
| MEDIUM | 5 (A15-11 through A15-15, A15-16) |
| LOW | 1 (A15-13) |
| **Total** | **16** |

**Priority test targets if tests were to be introduced:**

1. **Frm_saveuser.save_user()** -- Highest risk: direct user data persistence with zero validation and SQL injection
2. **Frm_upload.loadData()** -- Unrestricted file upload to web-accessible directory
3. **Databean_customer.query()** -- Dispatcher with SQL injection in all branches
4. **FirmwareverBean.setCurr_ver() / getType()** -- Parsing logic with multiple crash paths
5. **Frm_saveuser card conversion methods** -- Complex bitwise arithmetic with no verification
