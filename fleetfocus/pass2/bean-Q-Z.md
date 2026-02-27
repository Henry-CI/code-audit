# Pass 2 — Test Coverage: bean package (Q-Z)
**Agent:** A03
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

---

## Test Infrastructure Assessment

| Aspect | Status |
|---|---|
| Test framework (JUnit/TestNG) | **NONE** -- no dependency declared, no pom.xml/build.xml found |
| Test source directory (`test/`, `src/test/`) | **NONE** -- does not exist |
| Test files in scope | **0 of 20 files have any test coverage** |
| Build tool | **NONE** detected (no Maven, Gradle, or Ant config) |
| CI/CD test stage | **NONE** detected |
| Overall coverage | **0 %** |

The single file named `EncryptTest.java` in the `util` package is a decompiled utility class, not an actual test.

---

## Reading Evidence

### 1. QuestionBean.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/QuestionBean.java`
- **Class:** `QuestionBean` (plain POJO, no interfaces, no superclass)
- **Lines:** 126
- **Fields (all private):**
  - `String user_cd` (L4), `String loc_cd` (L5), `String dept_cd` (L6), `String veh_typ_cd` (L7), `String question` (L8), `String ans_type` (L9), `String exp_ans` (L10), `String crit_ans` (L11), `String custCd` (L12), `String access_level` (L13), `String access_cust` (L14), `String access_site` (L15), `String access_dept` (L16), `String question_id` (L17), `String questionSpa` (L18), `String questionTha` (L19), `boolean excludeRandom` (L20)
- **Public methods:** Getter/setter pairs for each field (17 getters, 17 setters). All trivial.
- **Complexity:** LOW -- pure data-holder bean.

### 2. RestrictedAccessUsageBean.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/RestrictedAccessUsageBean.java`
- **Class:** `RestrictedAccessUsageBean` (plain POJO)
- **Lines:** 101
- **Fields (all private):**
  - `String fleetNo, serialNo, hourStart, hourFinish, servHoursFrom, totalUsage, driverList, totalAccHours, hourlyRate, maxMonthlyRate, totalCharge` (L5)
- **Public methods:** Default constructor (L7), 11 getters + 11 setters. All trivial.
- **Complexity:** LOW -- pure data-holder bean.
- **Note:** `hourlyRate`, `maxMonthlyRate`, `totalCharge` are stored as String rather than numeric types -- financial values as strings.

### 3. SFTPSettings.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/SFTPSettings.java`
- **Class:** `SFTPSettings` (plain POJO)
- **Lines:** 61
- **Fields (all private):**
  - `int customerCd` (L5), `String sftpAddress` (L6), `String sftpUser` (L7), `String sftpPass` (L8), `String sftpDir` (L9), `String lastUpdateBy` (L10), `String lastUpdate` (L11)
- **Public methods:** 7 getters + 7 setters. All trivial.
- **Complexity:** LOW -- pure data-holder bean.
- **Security note:** `sftpPass` is stored as plain-text String with no encryption or masking.

### 4. ServiceDueFlagBean.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java`
- **Class:** `ServiceDueFlagBean` (complex bean with DB access, business logic)
- **Lines:** 1003
- **Imports:** `java.sql.*`, `javax.naming.*`, `javax.servlet.http.HttpServletRequest`, `javax.sql.DataSource`, and application service/util classes
- **Fields (selected critical ones):**
  - `String opCode` (L31), `String set_cust_cd` (L32), `Connection conn` (L66), `Statement stmt` (L67), `Statement stmt1` (L68), `ResultSet rset` (L69), `String query` (L70)
  - 15+ ArrayList fields (raw-typed, no generics) for various service data lists
  - `HttpServletRequest request` (L65), `Boolean is_user_admin` (L86), `Boolean is_user_lmh` (L87), `String access_cust` (L88)
- **Public methods with business logic:**
  - `void init()` (L104) -- JNDI lookup, DB connection, dispatch to opCode-based methods
  - `void clearVariables()` (L168) -- clears all ArrayLists
  - `void testQueries(int count)` (L543) -- executes raw SQL in a loop with string concatenation
  - `String getHrAtLastServ(String vehicle_cd, String end_dt)` (L886) -- DB query with string concatenation
  - `String getDept_prefix(String vcd)` (L966) -- DB query with string concatenation
- **Private methods with business logic:**
  - `void Fetch_report_nm()` (L564) -- SQL queries for report name and group access rights
  - `String convertServiceHour(long miseconds, String format)` (L609) -- math conversion
  - `String getColourStatus(int hours)` (L619) -- color threshold logic
  - `void Fetch_service_status_veh()` (L634) -- complex multi-query DB method
  - `void Fetch_serv_mnt_data()` (L728) -- complex multi-query DB method with loops
  - `void Fetch_service_reminder()` (L944) -- DB query
  - `String convertServiceHourAvg(long miseconds, String format, int days)` (L956) -- math conversion (potential division by zero)
- **Public getter/setter pairs:** ~50+ for all fields
- **Complexity:** VERY HIGH -- SQL injection risks, JNDI lookups, business logic, date math.

### 5. SiteConfigurationBean.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/SiteConfigurationBean.java`
- **Class:** `SiteConfigurationBean implements Serializable`
- **Lines:** 157
- **Fields (package-private):**
  - `serialVersionUID` (L10), `String id` (L11), `String module_type` (L12), `String reader_type` (L13), `String sim_supplier` (L14), `String sim_type` (L15), `String driver_base` (L16), `String time_base` (L17), `String timeslot1-4` (L18-21), `String idle_timer` (L22), `String survey_timer` (L23), `String contact_nm` (L24), `String contact_no` (L25), `String contact_email` (L26), `String comments` (L27), `String idtype` (L28), `String facility_code` (L29), `String super_card` (L30)
- **Public methods:** 19 getters + 19 setters. All trivial.
- **Complexity:** LOW -- pure data-holder bean (Serializable).

### 6. SpareModuleBean.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/SpareModuleBean.java`
- **Class:** `SpareModuleBean` (plain POJO)
- **Lines:** 120
- **Fields (all private):**
  - `int spare_modules_cd` (L5), `int spare_status_cd` (L6), `String spare_status` (L7), `String type` (L8), `String gmtp_id` (L9), `String from_serial` (L10), `String customer` (L11), `String site` (L12), `String department` (L13), `String last_updated` (L14), `String swap_date` (L15), `String ccid` (L16), `String ra_number` (L17), `String from_gmtp_id` (L18), `String tech_number` (L19), `String note` (L20)
- **Public methods:** 16 getters + 16 setters. All trivial.
- **Complexity:** LOW -- pure data-holder bean.

### 7. SpecialAccessBean.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/SpecialAccessBean.java`
- **Class:** `SpecialAccessBean` (plain POJO)
- **Lines:** 70
- **Fields (package-private):**
  - `int id` (L5), `String user_cd` (L6), `String cust_cd` (L7), `String loc_cd` (L8), `String dept_cd` (L9), `String custName` (L10), `String userName` (L11), `int module_cd` (L12), `boolean enabled` (L13)
- **Public methods:** 9 getters + 9 setters. All trivial.
- **Complexity:** LOW -- pure data-holder bean (access control related).

### 8. SubscriptionBean.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/SubscriptionBean.java`
- **Class:** `SubscriptionBean implements Serializable`
- **Lines:** 51
- **Fields (package-private):**
  - `serialVersionUID` (L12), `String id` (L14), `String cust_cd` (L15), `String loc_cd` (L16), `String dept_cd` (L17), `String month` (L18), `String email` (L19)
- **Public methods:** 5 getters + 5 setters. All trivial.
- **Complexity:** LOW -- pure data-holder bean.

### 9. SuperMasterAuthBean.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/SuperMasterAuthBean.java`
- **Class:** `SuperMasterAuthBean` (plain POJO)
- **Lines:** 69
- **Fields (all private):**
  - `String fleetNo, serialNo, authStart, authEnd, servHourFrom, superMasterCode, custName` (L5)
- **Public methods:** Default constructor (L7), 7 getters + 7 setters. All trivial.
- **Complexity:** LOW -- pure data-holder bean (auth time-window related).

### 10. UnitBean.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/UnitBean.java`
- **Class:** `UnitBean implements Serializable`
- **Lines:** 166
- **Fields (package-private except serialVersionUID):**
  - `serialVersionUID` (L11), `String veh_cd` (L13), `String gmtp_id` (L14), `String cust_nm` (L15), `String loc_nm` (L16), `String dept_nm` (L17), `String model` (L18), `String state` (L19), `String hire_no` (L20), `String serial_no` (L21), `Date active_date` (L22), `String cur_version` (L23), `String sim_provider` (L24), `String ccid` (L25), `String old_ccid` (L26), `String ccid_rpt_time` (L27), `String moderm_version` (L28), `String old_gmtpid` (L29), `String last_session` (L30), `String service_from` (L31), `String service_hour` (L32), `int threshold` (L33)
- **Public methods:** 22 getters + 22 setters. All trivial.
- **Complexity:** LOW -- pure data-holder bean.

### 11. UnitUtilSummaryBean.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/UnitUtilSummaryBean.java`
- **Class:** `UnitUtilSummaryBean implements Serializable`
- **Lines:** 113
- **Fields (package-private):**
  - `serialVersionUID` (L10), `String hire_no` (L12), `String serial_no` (L13), `String model_nm` (L14), `String total_hours` (L15), `String key_hours` (L16), `String keyHours_percentage` (L17), `String seat_hours` (L18), `String seatHours_percentage` (L19), `String track_hours` (L20), `String trackHours_percentage` (L21), `String hydl_hours` (L22), `String hydlHours_percentage` (L23), `String in_hours` (L24), `String inHours_percentage` (L25)
- **Public methods:** 14 getters + 14 setters. All trivial.
- **Complexity:** LOW -- pure data-holder bean.
- **Note:** Hours and percentages stored as Strings rather than numeric types.

### 12. UnitVersionInfoBean.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/UnitVersionInfoBean.java`
- **Class:** `UnitVersionInfoBean` (plain POJO)
- **Lines:** 33
- **Fields (all private):**
  - `String gmtpId` (L4), `boolean char100MaxSupported` (L5), `boolean char150MaxSupported` (L6), `boolean char150MaxMultiSupported` (L7)
- **Public methods:** 4 getters + 4 setters. All trivial.
- **Complexity:** LOW -- pure data-holder bean.

### 13. UnitutilBean.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/UnitutilBean.java`
- **Class:** `UnitutilBean implements Serializable`
- **Lines:** 189
- **Fields (package-private):**
  - `serialVersionUID` (L12), `String model_name` (L14), `HashMap<String, ArrayList<Integer>> utilMap` (L15), `HashMap<String, ImpactBean> impactMap` (L16), `ArrayList<HashMap<String, ImpactBean>> arrUtil` (L17), `String veh_cd` (L18), `String vmachine_nm` (L19), `int[] util` (L20, size 8), `int total` (L21), `String dept_cd` (L23), `String dept_name` (L24), `String loc_cd` (L25), `String loc_name` (L26), `String week` (L27), `String model_cd` (L28), `String chart_URL` (L29), `String wfrom` (L30), `String wto` (L31), `int week_int` (L32)
- **Public methods:**
  - Constructor `UnitutilBean()` (L35) -- initializes util array to zeroes
  - `void setUtil(int i, int util)` (L78) -- indexed setter (no bounds checking)
  - `void addArrUtil(HashMap<String, ImpactBean> utilMap)` (L102) -- adds to arrUtil list
  - 18 getters + 16 setters. Mostly trivial.
- **Complexity:** MEDIUM -- constructor logic, indexed array setter, complex data structures.

### 14. UnusedUnitBean.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/UnusedUnitBean.java`
- **Class:** `UnusedUnitBean implements Serializable`
- **Lines:** 90
- **Fields (package-private):**
  - `serialVersionUID` (L10), `String cust_name` (L11), `String site_name` (L12), `String fleet_no` (L13), `String serial_no` (L14), `String gmtp_id` (L15), `String ccid` (L16), `String vcd` (L17), `String last_report` (L18), `String inactive_days` (L19), `String state_name` (L20), `boolean onHire` (L22, default true)
- **Public methods:** 11 getters + 11 setters. All trivial.
- **Complexity:** LOW -- pure data-holder bean.

### 15. UserBean.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/UserBean.java`
- **Class:** `UserBean` (plain POJO)
- **Lines:** 51
- **Fields (package-private):**
  - `int id` (L5), `String username` (L6), `String firstname` (L7), `String lastname` (L8), `String email` (L9), `String lastUpdate` (L10)
- **Public methods:** 6 getters + 6 setters. All trivial.
- **Complexity:** LOW -- pure data-holder bean.

### 16. UserDriverBean.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/UserDriverBean.java`
- **Class:** `UserDriverBean` (plain POJO)
- **Lines:** 50
- **Fields (package-private):**
  - `String id` (L5), `String user_cd` (L6), `String weigand` (L7), `String veh_type` (L8), `String firstName` (L9), `String lastName` (L10)
- **Public methods:** 6 getters + 6 setters. All trivial.
- **Complexity:** LOW -- pure data-holder bean.

### 17. UserFormBean.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/UserFormBean.java`
- **Class:** `UserFormBean` (plain POJO)
- **Lines:** 59
- **Imports:** `java.util.ArrayList` (unused)
- **Fields (package-private except id):**
  - `private int id` (L7), `String userFomrCd` (L9), `String userFomrName` (L10), `String userFormMenuView` (L11), `String userFormMenuEdit` (L12), `String userFormDelete` (L13), `String userFormMenuPrint` (L14)
- **Public methods:** 7 getters + 7 setters. All trivial.
- **Complexity:** LOW -- pure data-holder bean.
- **Note:** Typo in field names: `userFomrCd`, `userFomrName` (should be `userFormCd`, `userFormName`).

### 18. VehDiagnostic.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/VehDiagnostic.java`
- **Class:** `VehDiagnostic` (plain POJO)
- **Lines:** 218
- **Fields (package-private):**
  - `int vehicleCd` (L5), `String utcTime` (L6), `String firmwareVer` (L7), `String ccid` (L8), `String timezone` (L9), `String signalStr` (L10), `String lastPreop` (L11), `String shockThreshold` (L12), `String redImpactThreshold` (L13), `String apn` (L14), `String hardwareVer` (L15), `String modemVer` (L16), `String canCRC` (L17), `String kernelBuild` (L18), `String expModVer` (L19)
  - `double currentThreshold` (L22), `long currentFSSXThreshold` (L23), `int currentTimezone` (L24), `String currentCRC` (L25)
  - `boolean thresholdSync` (L27), `boolean timezoneSync` (L28), `boolean redImpactSync` (L29), `boolean crcSync` (L30)
- **Public methods:** 23 getters + 23 setters. All trivial.
- **Complexity:** LOW -- pure data-holder bean with sync status flags.

### 19. VehNetworkSettingsBean.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/VehNetworkSettingsBean.java`
- **Class:** `VehNetworkSettingsBean` (plain POJO)
- **Lines:** 35
- **Fields (package-private):**
  - `int index` (L4), `String country` (L29), `String ssid` (L30), `String password` (L31)
- **Public methods:** 4 getters + 4 setters. All trivial.
- **Complexity:** LOW -- pure data-holder bean.
- **Security note:** `password` stored as plain-text String.

### 20. VehicleImportBean.java
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/VehicleImportBean.java`
- **Class:** `VehicleImportBean` (plain POJO)
- **Lines:** 140
- **Fields (all private):**
  - `String site_name` (L5), `String department_name` (L6), `String gmtp_id` (L7), `String equipNo` (L8), `String serial_no` (L9), `String model` (L10), `String canRule` (L11), `String surv_to` (L12), `String question_sched` (L13), `String timeslot1-4` (L14-17), `String custCd` (L18), `int servHrsInterval` (L19), `int dateInterval` (L20), `String lastServDate` (L21), `boolean canUnit` (L22), `String seat_idle` (L23)
- **Public methods:** 18 getters + 18 setters. All trivial.
- **Complexity:** LOW -- pure data-holder bean.

---

## Findings

### A03-001 — Zero test coverage across all 20 bean files
- **File:** All 20 files in scope
- **Severity:** CRITICAL
- **Category:** Test Coverage
- **Description:** None of the 20 bean files (Q-Z range) in the `com.torrent.surat.fms6.bean` package have any associated unit tests. The repository has no test framework, no test directories, no test runner configuration, and no build tool (Maven/Gradle/Ant) that would facilitate testing.
- **Evidence:** No files matching `*Test*.java` in `bean/` package; no `test/` or `src/test/` directory; no JUnit/TestNG imports anywhere in these files; the sole `EncryptTest.java` found is a decompiled utility class, not a test.
- **Recommendation:** Introduce a test framework (JUnit 4 or 5) and build tool (Maven or Gradle). Prioritize test creation for `ServiceDueFlagBean.java` (the only file with business logic and SQL access). For the remaining 19 pure POJO beans, generate basic getter/setter round-trip tests to establish a regression safety net.

### A03-002 — ServiceDueFlagBean.init() method has untested JNDI + DB dispatch logic
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java`, L104-165
- **Severity:** CRITICAL
- **Category:** Test Coverage -- Business Logic
- **Description:** The `init()` method performs JNDI context lookup, obtains a database connection, and dispatches to different private methods based on the `opCode` field value (`vehicle_serv_new`, `service_flag_new`, `test_queries`). No tests verify correct dispatch, error handling on null context, or cleanup behavior in the finally block.
- **Evidence:** L104-165: `init()` with JNDI lookup, three opCode branches, broad `catch(Exception)` with `System.out.println` error handling.
- **Recommendation:** Write integration tests with an embedded database or mocked DataSource. Test each opCode branch independently. Verify resource cleanup (Connection, Statement, ResultSet) occurs in all paths including exception paths.

### A03-003 — SQL injection in ServiceDueFlagBean via string concatenation
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java`, multiple locations
- **Severity:** CRITICAL
- **Category:** Test Coverage -- Security
- **Description:** Multiple methods construct SQL queries through string concatenation with user-controlled values. Without tests, there is no validation that input sanitization occurs upstream. Vulnerable methods include `testQueries()` (L557), `Fetch_report_nm()` (L568-592), `Fetch_service_status_veh()` (L637-660), `Fetch_serv_mnt_data()` (L735-807), `Fetch_service_reminder()` (L947), `getHrAtLastServ()` (L895-904), and `getDept_prefix()` (L980).
- **Evidence:**
  - L557: `query = "select sp_eos_message( '"+dateS+"', '2002f5b,"+hex+"'..."`
  - L568: `"...where \"FORM_CD\"='" + form_cd + "' "`
  - L580: `"...where \"USER_CD\" = '" + set_ucd + "' "`
  - L647: `"...where veh_cd='"+ veh_cd+"'"`
  - L895: `"...where veh_cd = " + vehicle_cd + " and utc_time <='"+end_dt+"'::timestamp..."`
  - L947: `query += " where cust_cd =" + set_cust_cd`
  - L980: `"...and \"VEHICLE_CD\" = " + vcd`
- **Recommendation:** Create parameterized query tests that verify SQL injection is prevented. Long-term: refactor all string-concatenated queries to use PreparedStatement.

### A03-004 — ServiceDueFlagBean.convertServiceHourAvg() has untested division-by-zero risk
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java`, L956-963
- **Severity:** HIGH
- **Category:** Test Coverage -- Edge Case
- **Description:** The private method `convertServiceHourAvg(long miseconds, String format, int days)` divides by `(36000 * days)`. If `days` is 0, this will cause an ArithmeticException or produce `Infinity`/`NaN` in the float division. No tests validate this edge case.
- **Evidence:** L961: `hour = df.format((float) miseconds / (36000 * days));` -- when `days == 0`, result is `Infinity` or `NaN`.
- **Recommendation:** Add tests for `days=0`, `days=1`, negative days, and normal values. Add a guard clause for zero days.

### A03-005 — ServiceDueFlagBean.convertServiceHour() has untested math logic
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java`, L609-617
- **Severity:** HIGH
- **Category:** Test Coverage -- Business Logic
- **Description:** `convertServiceHour(long miseconds, String format)` divides milliseconds by 36000 to produce hours. This conversion factor (36000) assumes 1/10th-second units, not actual milliseconds. No tests verify the correctness of this conversion or the formatting with various inputs.
- **Evidence:** L614: `hour = df.format((float) miseconds / 36000);` -- the divisor 36000 converts centiseconds to hours (3600 seconds * 10 ticks/second). Cast to float may lose precision for large values.
- **Recommendation:** Write unit tests verifying the conversion factor and precision. Test boundary values (0, Long.MAX_VALUE, negative values).

### A03-006 — ServiceDueFlagBean.getColourStatus() has untested threshold logic
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java`, L619-632
- **Severity:** HIGH
- **Category:** Test Coverage -- Business Logic
- **Description:** The private method `getColourStatus(int hours)` returns HTML style strings based on hour thresholds (>=25 green, 6-24 orange, <=5 red). No tests verify the boundary values or the returned HTML styles.
- **Evidence:** L621-631: Three threshold branches with hardcoded color values and cutoffs at 25 and 5 hours.
- **Recommendation:** Write tests for boundary values: 0, 5, 6, 24, 25, 26, and negative hours. Verify correct HTML style output for each range.

### A03-007 — ServiceDueFlagBean.testQueries() is untested and contains raw SQL execution in a loop
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java`, L543-561
- **Severity:** HIGH
- **Category:** Test Coverage -- Security/Stability
- **Description:** `testQueries(int count)` is a public method that executes SQL in a loop `count` times, incrementing hex values and timestamps via string concatenation. No tests verify the hex parsing, date parsing, or SQL execution. The method has no upper bound on `count` and could be used for denial-of-service.
- **Evidence:** L543-559: Public method accepting unbounded `count`, parsing `hex` from instance field (potential NumberFormatException at L547), parsing dates with `SimpleDateFormat` (L550), executing raw SQL (L558).
- **Recommendation:** Add tests for: count=0, count=1, invalid hex values, invalid date strings. Add an upper bound on count parameter.

### A03-008 — ServiceDueFlagBean uses raw ArrayList types (no generics)
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java`, L44-62
- **Severity:** MEDIUM
- **Category:** Test Coverage -- Type Safety
- **Description:** All ArrayList fields use raw types without generics (e.g., `private ArrayList lastServDateList = new ArrayList()`). Without tests, there is no verification that type-correct data is being inserted and retrieved.
- **Evidence:** L44-62: 17 ArrayList fields, all using raw types. Callers can insert any object type, causing ClassCastException at runtime.
- **Recommendation:** Add generics to all ArrayList declarations. Write tests verifying type safety of list contents.

### A03-009 — ServiceDueFlagBean exposes mutable internal state via getters
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java`, L278-524
- **Severity:** MEDIUM
- **Category:** Test Coverage -- Encapsulation
- **Description:** All ArrayList getter methods return direct references to internal mutable lists (e.g., `getNextServDate()` returns `nextServDate` directly). Additionally, `getStmt()` (L471) and `getStmt1()` (L479) expose raw JDBC Statement objects. Without tests, there is no verification that external mutation does not corrupt internal state.
- **Evidence:** L278: `return nextServDate;`, L471: `return stmt;`, L479: `return stmt1;`
- **Recommendation:** Write tests demonstrating that external mutation of returned lists affects internal state. Consider returning defensive copies. Remove Statement getters/setters.

### A03-010 — ServiceDueFlagBean.Fetch_serv_mnt_data() has untested access_cust substring operation
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java`, L742
- **Severity:** HIGH
- **Category:** Test Coverage -- Edge Case
- **Description:** When `is_user_lmh` is true and `set_cust_cd` is "all", the method performs `access_cust.substring(2, access_cust.length())` without null-checking `access_cust`. If `access_cust` is null or shorter than 2 characters, a NullPointerException or StringIndexOutOfBoundsException will occur.
- **Evidence:** L742: `String ucd_str = access_cust.substring(2, access_cust.length());` -- `access_cust` is initialized to `null` at L88 and set via `setAccess_cust()` at L539.
- **Recommendation:** Add tests for null `access_cust`, empty string, single-character string, and normal values. Add null/length checks.

### A03-011 — SFTPSettings.java stores SFTP password as plain text with no test verification
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/SFTPSettings.java`, L8
- **Severity:** HIGH
- **Category:** Test Coverage -- Security
- **Description:** The `sftpPass` field stores SFTP credentials as a plain-text String. No tests exist to verify that password handling follows security best practices (encryption at rest, masking in logs, secure clearing).
- **Evidence:** L8: `private String sftpPass = "";`, L25: `public String getSftpPass() { return sftpPass; }`, L46: `public void setSftpPass(String sftpPass) { this.sftpPass = sftpPass; }`
- **Recommendation:** Create tests verifying that passwords are encrypted before storage. Consider using `char[]` instead of String for password handling, or an encryption wrapper.

### A03-012 — VehNetworkSettingsBean.java stores WiFi password as plain text
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/VehNetworkSettingsBean.java`, L31
- **Severity:** HIGH
- **Category:** Test Coverage -- Security
- **Description:** The `password` field stores network password as plain-text String. No tests verify secure handling.
- **Evidence:** L31: `String password;`, L23: `public String getPassword() { return password; }`
- **Recommendation:** Same as A03-011. Encrypt password storage. Add tests verifying encryption.

### A03-013 — RestrictedAccessUsageBean stores financial values as Strings
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/RestrictedAccessUsageBean.java`, L5
- **Severity:** MEDIUM
- **Category:** Test Coverage -- Data Integrity
- **Description:** Fields `hourlyRate`, `maxMonthlyRate`, and `totalCharge` represent monetary values but are stored as Strings. Without tests, there is no verification of numeric validity, precision, or calculation correctness.
- **Evidence:** L5: `private String ... hourlyRate, maxMonthlyRate, totalCharge;`
- **Recommendation:** Write tests verifying that financial values parse correctly as numbers. Consider using `BigDecimal` for financial fields.

### A03-014 — UnitutilBean.setUtil() has no bounds checking on array index
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/UnitutilBean.java`, L78-79
- **Severity:** MEDIUM
- **Category:** Test Coverage -- Edge Case
- **Description:** `setUtil(int i, int util)` directly indexes into `this.util[i]` (a fixed-size array of 8) without bounds checking. An index < 0 or >= 8 will throw ArrayIndexOutOfBoundsException.
- **Evidence:** L78-79: `public void setUtil(int i,int util) { this.util[i] = util; }` -- array is `int[] util = new int[8]` (L20).
- **Recommendation:** Write tests for i=-1, i=0, i=7, i=8. Add bounds checking with a meaningful error message.

### A03-015 — UnitUtilSummaryBean stores hours/percentages as Strings
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/UnitUtilSummaryBean.java`, L15-25
- **Severity:** MEDIUM
- **Category:** Test Coverage -- Data Integrity
- **Description:** All hour and percentage fields (`total_hours`, `key_hours`, `keyHours_percentage`, etc.) are stored as Strings initialized to "0". Without tests, there is no verification that these values can be safely parsed as numbers by consuming code.
- **Evidence:** L15-25: 12 String fields representing numeric values, all initialized to "0" or "" for `hydl_hours`.
- **Recommendation:** Write tests verifying round-trip numeric consistency. Consider using numeric types (double or BigDecimal).

### A03-016 — UserFormBean has typos in field names (userFomrCd, userFomrName)
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/UserFormBean.java`, L9-10
- **Severity:** LOW
- **Category:** Test Coverage -- Code Quality
- **Description:** Fields `userFomrCd` and `userFomrName` contain the typo "Fomr" instead of "Form". The corresponding getters/setters also carry this typo. Without tests, renaming these fields would have unknown blast radius.
- **Evidence:** L9: `String userFomrCd;`, L10: `String userFomrName;`, L21: `getUserFomrCd()`, L27: `getUserFomrName()`
- **Recommendation:** Before fixing the typo, add tests and search for all callers. Use IDE refactoring to rename safely. Note: the field names `userFormMenuView`, `userFormMenuEdit`, `userFormDelete`, `userFormMenuPrint` are spelled correctly, making the inconsistency more confusing.

### A03-017 — UserFormBean imports unused ArrayList
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/UserFormBean.java`, L3
- **Severity:** INFO
- **Category:** Code Quality
- **Description:** `import java.util.ArrayList;` is declared but never used in the class.
- **Evidence:** L3: `import java.util.ArrayList;` -- no ArrayList usage in the file.
- **Recommendation:** Remove unused import.

### A03-018 — Multiple beans use package-private fields instead of private
- **File:** SiteConfigurationBean.java, SpecialAccessBean.java, SubscriptionBean.java, UnitBean.java, UnitUtilSummaryBean.java, UnitutilBean.java, UnusedUnitBean.java, UserBean.java, UserDriverBean.java, UserFormBean.java, VehDiagnostic.java, VehNetworkSettingsBean.java
- **Severity:** MEDIUM
- **Category:** Test Coverage -- Encapsulation
- **Description:** 12 of the 20 beans declare fields with default (package-private) access instead of `private`. This allows any class in the same package to bypass getters/setters and directly access/modify fields. Without tests, there is no verification that all access goes through the public API.
- **Evidence:** Example from SiteConfigurationBean.java L11-30: `String id = "";`, `String module_type = "";`, etc. Example from UserBean.java L5-10: `int id;`, `String username;`, etc.
- **Recommendation:** Change all fields to `private`. Write tests to verify that getter/setter contracts are maintained. Search for direct field access in the same package before changing visibility.

### A03-019 — ServiceDueFlagBean exception handling uses System.out.println
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java`, L129-133, L912-916
- **Severity:** MEDIUM
- **Category:** Test Coverage -- Error Handling
- **Description:** Exception handling throughout ServiceDueFlagBean uses `System.out.println` and `printStackTrace()` instead of proper logging. Errors are swallowed silently. Without tests, there is no verification that callers are notified of failures.
- **Evidence:**
  - L130-133: `exception.printStackTrace(); System.out.println(" Exception in Databean_getuser In " + methodName...)`
  - L912-916: same pattern in `getHrAtLastServ()`
  - L139-163: multiple `System.out.println("rset is not close " + e);` in finally blocks
- **Recommendation:** Add tests that verify error propagation. Replace System.out with a logging framework. Consider re-throwing or returning error indicators rather than swallowing exceptions.

### A03-020 — ServiceDueFlagBean.testQueries() uses incorrect SimpleDateFormat pattern
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/ServiceDueFlagBean.java`, L545
- **Severity:** HIGH
- **Category:** Test Coverage -- Bug
- **Description:** The `SimpleDateFormat` pattern uses `"yyyy-MM-dd hh:mm:ss.ms"` where `hh` is 12-hour format (should be `HH` for 24-hour) and `ms` is invalid (should be `SSS` for milliseconds or `SS` for fractional seconds). The `m` in `ms` re-parses minutes, and `s` re-parses seconds, producing incorrect results.
- **Evidence:** L545: `SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.ms");`
- **Recommendation:** Write tests that verify date parsing. Fix the pattern to `"yyyy-MM-dd HH:mm:ss.SSS"` or the intended format.

---

## Summary

| Severity | Count |
|---|---|
| CRITICAL | 3 |
| HIGH | 7 |
| MEDIUM | 6 |
| LOW | 1 |
| INFO | 1 |
| **Total** | **18 unique findings (A03-001 through A03-020)** |

### Priority Recommendations

1. **Immediate (CRITICAL):** Establish a test framework (JUnit 5 + Maven/Gradle) and create a `src/test/java` tree mirroring the source structure.
2. **High Priority:** Write integration tests for `ServiceDueFlagBean.java` -- it is the only file among these 20 with business logic, DB access, and SQL construction. Focus on:
   - `init()` dispatch logic
   - SQL injection prevention
   - `convertServiceHour()` and `convertServiceHourAvg()` math
   - `getColourStatus()` boundary values
   - `testQueries()` input validation
   - `access_cust.substring()` null safety
3. **Medium Priority:** For the 19 pure POJO beans, generate basic getter/setter tests to establish baseline coverage and verify serialization for beans implementing `Serializable`.
4. **Low Priority:** Fix typos in `UserFormBean`, remove unused imports, tighten field visibility from package-private to private.
