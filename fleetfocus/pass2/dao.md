# Pass 2 — Test Coverage: dao package
**Agent:** A07
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

---

## Test Infrastructure Assessment

| Criterion | Status |
|---|---|
| Test source directory (`test/`, `src/test/`) | **ABSENT** |
| Test files (`*Test.java`, `*Spec.java`) | **NONE FOUND** |
| JUnit dependency in pom.xml | **NOT PRESENT** |
| TestNG dependency in pom.xml | **NOT PRESENT** |
| Mockito / mock framework | **NOT PRESENT** |
| CI test execution config | **NOT FOUND** |

**Conclusion:** The repository has **ZERO automated tests**. No test framework, no test directory structure, and no test files exist anywhere in the codebase. Every DAO file in scope has **0% test coverage**. All 10 assigned DAO files execute raw SQL against a live database with no mocking layer available.

---

## Reading Evidence

### BatteryDAO.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/dao/BatteryDAO.java`
- **Class:** `BatteryDAO`
- **Lines:** 420

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ArrayList<BatteryBean> getBatteryCharge(String cust_cd, String loc_cd, String dept_cd, String from, String to) throws SQLException` | 16 |
| 2 | `public ArrayList<BatteryBean> getBatteryChange(String cust_cd, String loc_cd, String dept_cd, String from, String to) throws SQLException` | 74 |
| 3 | `public ArrayList<BatteryBean> calculateBatteryChange(String cust_cd, String loc_cd, String dept_cd, String from, String to) throws SQLException` | 134 |
| 4 | `public ArrayList<BatteryBean> calculateBatteryCharge(String cust_cd, String loc_cd, String dept_cd, String from, String to) throws SQLException` | 250 |
| 5 | `public String getDuration(String sttime, String endtime) throws SQLException` | 351 |
| 6 | `public String getDept_prefix(String vcd) throws SQLException` | 386 |

---

### DriverDAO.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/dao/DriverDAO.java`
- **Class:** `DriverDAO`
- **Lines:** 569

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ArrayList<EntityBean> getArrayDriver(String cust_cd, String loc_cd, String dept_cd) throws SQLException` | 20 |
| 2 | `public void checkExpiry(String cust_cd) throws SQLException` | 76 |
| 3 | `public void sendIDDENY(String usercd, String weigand, String vehtype, HashMap<String, Boolean> statusMap) throws SQLException` | 141 |
| 4 | `public String getDriverlst(String cust_cd, String loc_cd, String dept_cd) throws SQLException` | 249 |
| 5 | `public ArrayList<EntityBean> getArrayDriverImpact(String cust_cd, String loc_cd, String dept_cd) throws SQLException` | 298 |
| 6 | `public String getDriverImpactLst(String cust_cd, String loc_cd, String dept_cd) throws SQLException` | 352 |
| 7 | `public void checkValidLicence(String userId, String newRevewDate, String expiryAlert) throws SQLException` | 402 |
| 8 | `public String getDriverFulllst(String cust_cd, String loc_cd, String dept_cd) throws SQLException` | 489 |
| 9 | `public String getDriverNameById(String driver_id) throws SQLException` | 538 |

---

### DriverImportDAO.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/dao/DriverImportDAO.java`
- **Class:** `DriverImportDAO`
- **Lines:** 1208

| # | Method Signature | Line |
|---|---|---|
| 1 | `public boolean checkDriverByNm(String compId, String fname, String lname, String id, boolean status) throws SQLException` | 17 |
| 2 | `public boolean checkDriverByLic(String compId, String licence, String id, boolean status) throws Exception` | 71 |
| 3 | `public ArrayList<DriverImportBean> getDriverByNm(String compId, String fname, String lname, boolean status) throws Exception` | 122 |
| 4 | `public ArrayList<DriverImportBean> getDriverByFullNm(String compId, String fname, boolean status) throws Exception` | 179 |
| 5 | `public ArrayList<DriverImportBean> getAllDriver(String compId, boolean status) throws Exception` | 235 |
| 6 | `public ArrayList<DriverImportBean> getAllDriverLinde(String compId) throws Exception` | 293 |
| 7 | `public ArrayList<DriverImportBean> getAllDriverLinde(String compId, boolean status) throws Exception` | 342 |
| 8 | `public ArrayList<DriverImportBean> getDriverLicence(String compId, boolean status) throws Exception` | 401 |
| 9 | `public ArrayList<DriverImportBean> getDriverById(String id) throws Exception` | 460 |
| 10 | `public boolean saveDriverInfo(DriverImportBean DriverImportBean) throws Exception` | 511 |
| 11 | `public String saveLicenseExpiryBlackListInfo(LicenseBlackListBean bean) throws Exception` | 559 |
| 12 | `public boolean updateDriverInfo(DriverImportBean DriverImportBean) throws Exception` | 924 |
| 13 | `public Boolean delDriverById(String id) throws Exception` | 973 |
| 14 | `public String getTotalDriverByID(String id, boolean status) throws Exception` | 1009 |
| 15 | `public String getDriverName(String id) throws Exception` | 1055 |
| 16 | `public String getDriverNameLinde(String id) throws Exception` | 1098 |
| 17 | `public Boolean uploadLicence(String licenceid, String url) throws Exception` | 1141 |
| 18 | `public Boolean uploadLicenceAU(String uid, String url) throws Exception` | 1174 |

---

### ImpactDAO.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/dao/ImpactDAO.java`
- **Class:** `ImpactDAO`
- **Lines:** ~1300+

| # | Method Signature | Line |
|---|---|---|
| 1 | `public HashMap<String, ArrayList<ImpactBean>> getRedImpactCache(String cust_cd, String loc_cd) throws SQLException` | 33 |
| 2 | `public HashMap<String, ArrayList<ImpactBean>> getRedImpactCacheByDriver(String cust_cd, String loc_cd) throws SQLException` | 98 |
| 3 | `public ArrayList<ImpactBean> getRedImpact(String cust_cd, String loc_cd) throws SQLException` | 178 |
| 4 | `public ArrayList<ImpactBean> getRedImpactDriver(String cust_cd, String loc_cd) throws SQLException` | 258 |
| 5 | `public ArrayList<double[]> getImpacts(String cust_cd, String loc_cd, String dept_cd, String month, String from, String to) throws SQLException` | 342 |
| 6 | `public ArrayList<ImpactBean> getImpactsNationalRpt(String cust_cd, String loc_cd, String st_dt, String end_dt) throws SQLException` | 428 |
| 7 | `public ArrayList<ImpactBean> getImpacts(String cust_cd, String loc_cd) throws SQLException` | 605 |
| 8 | `public ArrayList<UnitutilBean> getImpactsByUnit(String cust_cd, String loc_cd) throws SQLException` | 689 |
| 9 | `public ArrayList<UnitutilBean> getImpactsByDriver(String cust_cd, String loc_cd) throws SQLException` | 826 |
| 10 | `public ArrayList<ImpactSummaryBean> getImpactsByUnit(String cust_cd, String loc_cd, String dept_cd, String from, String to) throws SQLException` | 1042 |
| 11 | `public ArrayList<ImpactLocBean> getImpactsByDriver(String cust_cd, String loc_cd, String dept_cd, String from, String to) throws SQLException` | 1162 |

---

### ImportDAO.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/dao/ImportDAO.java`
- **Class:** `ImportDAO`
- **Lines:** ~4900+

| # | Method Signature | Line |
|---|---|---|
| 1 | `public boolean saveQuestions(QuestionBean qbean) throws Exception` | 30 |
| 2 | `public boolean saveQuestions(QuestionBean qbean, List<String> langChoice) throws Exception` | 199 |
| 3 | `public ArrayList<String> getCurrentCheckCd(String custCd, String locCd, String deptCd, String vehTypeCd) throws Exception` | 376 |
| 4 | `public ArrayList<String> getCurrentCheckCdTab(String custCd, String locCd, String deptCd) throws Exception` | 443 |
| 5 | `public void removePreviousChecklist(ArrayList<String> chkList) throws Exception` | 541 |
| 6 | `public String saveQuestionsTab(QuestionBean qbean) throws Exception` | 608 |
| 7 | `public String saveDriverInfo(DriverImportBean driverBean) throws SQLException` | 907 |
| 8 | `public String saveDriverInfoAU(DriverImportBean driverBean) throws SQLException` | 1389 |
| 9 | `public int saveDriverInfo1(DriverImportBean driverBean) throws Exception` | 1789 |
| 10 | `public int saveDriverInfoAu(DriverImportBean driverBean) throws Exception` | 2109 |
| 11 | `public boolean saveDriverDeptRel(int driverId, String deptId, String locId, String custId) throws Exception` | 2440 |
| 12 | `public boolean saveDriverDeptRelNew(String driverId, String deptName, String locName, String custId, String access_l, String access_s, String access_d) throws Exception` | 2481 |
| 13 | `public String saveVehicleInfo(VehicleImportBean vehBean) throws SQLException` | 2632 |
| 14 | `public String sendCanUnit(CanruleBean canBean) throws SQLException` | 3487 |
| 15 | `public Boolean saveServiceSettings(String hireno, String serviceDate) throws Exception` | 4728 |
| 16 | `public Boolean saveServiceSettingsServer(String serial, String serviceDate) throws Exception` | 4805 |

---

### LockOutDAO.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/dao/LockOutDAO.java`
- **Class:** `LockOutDAO`
- **Lines:** 145

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ArrayList<LockOutBean> getLockOutData(String cust_cd, String loc_cd) throws SQLException` | 15 |
| 2 | `public ArrayList<LockOutBean> getLockOutDataNtlRpt(String cust_cd, String loc_cd, String st_dt, String end_dt) throws SQLException` | 80 |

---

### MessageDao.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/dao/MessageDao.java`
- **Class:** `MessageDao`
- **Lines:** 113

| # | Method Signature | Line |
|---|---|---|
| 1 | `public void setOpCode(String opCode)` | 23 |
| 2 | `public String getMsg()` | 26 |
| 3 | `public void setFid(String fid)` | 30 |
| 4 | `public void setMsg(String msg)` | 34 |
| 5 | `public boolean isStatus()` | 39 |
| 6 | `public void setStatus(boolean status)` | 44 |
| 7 | `public void init()` | 48 |
| 8 | `public void selectMesssage() throws SQLException` | 105 |

---

### PreCheckDAO.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/dao/PreCheckDAO.java`
- **Class:** `PreCheckDAO`
- **Lines:** 578

| # | Method Signature | Line |
|---|---|---|
| 1 | `public ArrayList<Integer> getChecks(String cust_cd, String loc_cd, String dept_cd, String month, String from, String to) throws SQLException` | 26 |
| 2 | `public ArrayList<PreCheckBean> getChecks(String cust_cd, String loc_cd) throws SQLException` | 127 |
| 3 | `public ArrayList<FleetCheckBean> getCheckSummary(String cust_cd, String loc_cd, String dept_cd, String month, String from, String to) throws SQLException` | 181 |
| 4 | `public ArrayList<PreCheckBean> getChecksByDriver(String cust_cd, String loc_cd) throws SQLException` | 267 |
| 5 | `public ArrayList<PreCheckSummaryBean> getChecks(String cust_cd, String loc_cd, String dept_cd, String from, String to) throws SQLException` | 316 |
| 6 | `public ArrayList<PreCheckSummaryBean> getChecksByDriver(String cust_cd, String loc_cd, String dept_cd, String from, String to) throws SQLException` | 433 |

---

### RegisterDAO.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/dao/RegisterDAO.java`
- **Class:** `RegisterDAO`
- **Lines:** 535

| # | Method Signature | Line |
|---|---|---|
| 1 | `public String[] register(String fname, String lname, String email, String cname, String phone, String[] vehnm, String[] vehmodel, String[] dfname, String[] dlname) throws SQLException` | 17 |
| 2 | `public boolean checkDupComp(String cname) throws SQLException` | 460 |
| 3 | `public boolean checkAuthority(String username, String password) throws SQLException` | 498 |

---

### UnitDAO.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/dao/UnitDAO.java`
- **Class:** `UnitDAO`
- **Lines:** ~2700+

| # | Method Signature | Line |
|---|---|---|
| 1 | `public String getDepartmentLst(String cust_cd, String loc_cd) throws SQLException` | 53 |
| 2 | `public ArrayList<EntityBean> getArrayDepartment(String cust_cd, String loc_cd) throws SQLException` | 102 |
| 3 | `public String getUnitLstByModel(String cust_cd, String loc_cd, String dept_cd, String model_cd) throws SQLException` | 159 |
| 4 | `public ArrayList<EntityBean> getArrayUnitByModel(String cust_cd, String loc_cd, String dept_cd, String model_cd) throws SQLException` | 211 |
| 5 | `public ArrayList<EntityBean> getArryModel(String cust_cd, String loc_cd, String dept_cd) throws SQLException` | 267 |
| 6 | `public ArrayList<EntityBean> getArryModelImpact(String cust_cd, String loc_cd, String dept_cd) throws SQLException` | 321 |
| 7 | `public ArrayList<EntityBean> getArryModelImpactByDriver(String cust_cd, String loc_cd, String dept_cd, String driver_cd) throws SQLException` | 376 |
| 8 | `public String[] getLocById(String loc_cd) throws SQLException` | 437 |
| 9 | `public String getCustName(String cust_cd) throws SQLException` | 472 |
| 10 | `public String getLocName(String loc_cd) throws SQLException` | 507 |
| 11 | `public String getDeptName(String dept_cd) throws SQLException` | 543 |
| 12 | `public ArrayList<UnitutilBean> getUtil(String cust_cd, String loc_cd, String dept_cd, String firstDate, int duration) throws SQLException` | 581 |
| 13 | `public int[] getDays() throws SQLException` | 644 |
| 14 | `public ArrayList<EntityBean> getAllModel() throws SQLException` | 680 |
| 15 | `public ArrayList<UnusedUnitBean> getUnusedUnit(String cust_cd, String loc_cd, String dept_cd, int days) throws SQLException` | 782 |
| 16 | `public ArrayList<PreCheckBean> getArrayModelPreCheck(String cust_cd, String loc_cd, String dept_cd, Boolean isnull) throws SQLException` | 865 |
| 17 | `public int getTotalTime(String cust_cd, String loc_cd, String model_cd) throws SQLException` | 927 |
| 18 | `public ArrayList<UnitBean> getUnitSummary() throws SQLException` | 1080 |
| 19 | `public ArrayList<UnitBean> getUnitSummaryNZ() throws SQLException` | 1226 |
| 20 | `public ArrayList<UnitBean> getSimSwapSummary() throws SQLException` | 1287 |
| 21 | `public ArrayList<MaxHourUsageBean> getMaxUtilGroup(String cust_cd, ArrayList locdeptList, String from, String to)` | 1392 |
| 22 | `public ArrayList<EntityBean> getArryModelLindeGroup(String cust_cd, ...)` | 1559 |
| 23 | `public ArrayList<EntityBean> getArrayLocation(String cust_cd, String loc_cd)` | 1628 |
| 24 | `public ArrayList<EntityBean> getArrayDepartment(String cust_cd, String loc_cd, String dept_cd, boolean visible)` | 1677 |
| 25 | `public String getUnitLstByModelLinde(String cust_cd, String loc_cd, ...)` | 1738 |
| 26 | `public String getExportDir() throws Exception` | 1801 |
| 27 | `public ArrayList<MaxHourUsageBean> getMaxUtil(String cust_cd, ...)` | 1811 |
| 28 | `public ArrayList<EntityBean> getArryModelLinde(String cust_cd, ...)` | 1962 |
| 29 | `public ArrayList<String[]> getWeeks(String from, String to, int weeks)` | 2015 |
| 30 | `public String getUnitNameById(String unit_cd) throws SQLException` | 2079 |
| 31 | `public String getUnitTypeById(String unit_cd) throws SQLException` | 2115 |
| 32 | `public ArrayList<DailyUsageDeptDataBean> getUnitUtilByGroup(String cust_cd, String loc_cd, ...)` | 2152 |
| 33 | `public ArrayList<UnitutilBean> getUnitUtil(String cust_cd, String loc_cd, ...)` | 2368 |
| 34 | `public ArrayList<EntityBean> getArrayByModel(String cust_cd, String loc_cd, ...)` | 2590 |
| 35 | `public String getCustbyId(String custCd) throws SQLException` | 2645 |
| 36 | `public ArrayList<UserDriverBean> getDriversByCustSite(String custCd, String locCd) throws SQLException` | 2681 |

---

## Findings

### A07-01 — Total absence of test infrastructure for all DAO classes
- **File:** All 10 DAO files
- **Severity:** CRITICAL
- **Category:** Test Coverage
- **Description:** The entire repository lacks any test framework (JUnit, TestNG, Mockito, etc.), test directories, or test files. All 10 DAO files under audit have 0% code coverage. These DAOs contain 128+ public methods collectively that execute SQL queries directly against a production database with no unit tests, integration tests, or any other form of automated verification. This is the highest-risk category since DAOs handle all data persistence and retrieval for the application.
- **Evidence:** `find` and `glob` searches for `*Test.java`, `*Spec.java`, `test/` directories, and pom.xml dependency declarations for JUnit/TestNG/Mockito all return zero results.
- **Recommendation:** Establish a test infrastructure immediately: (1) Add JUnit 5 and Mockito to build dependencies. (2) Create `src/test/java` directory structure mirroring the main source. (3) Prioritize testing the DAO layer first due to direct database interaction. (4) Use an embedded database (H2 in PostgreSQL compatibility mode) or Mockito-based mocking of `DBUtil.getConnection()` for unit tests.

---

### A07-02 — SQL injection via string concatenation in BatteryDAO
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dao/BatteryDAO.java`
- **Severity:** CRITICAL
- **Category:** Test Coverage / Security
- **Description:** All 6 methods in BatteryDAO construct SQL queries using string concatenation with user-supplied parameters (`from`, `to`, `cust_cd`, `loc_cd`, `dept_cd`, `vcd`). Without tests, there is no verification that malicious input is sanitized. The `getDuration()` method (line 365) directly concatenates timestamp strings into SQL. The `getDept_prefix()` method (line 400) concatenates `vcd` directly into a WHERE clause.
- **Evidence:**
  - Line 42: `" and d1.utc_time >= '"+from+"'::timestamp"+" and d1.utc_time<='"+to+"'::timestamp"`
  - Line 100: `" and d1.utc_time >= '"+from+"'::timestamp"+" and d1.utc_time<='"+to+"'::timestamp"`
  - Line 163: `" and d.utc_time >= '"+from+"'::timestamp"+" and d.utc_time<='"+to+"'::timestamp"`
  - Line 365: `"select '"+endtime+"'::timestamp - '"+sttime+"'::timestamp"`
  - Line 400: `"... and \"VEHICLE_CD\" = " + vcd`
- **Recommendation:** Write parameterized-query tests that confirm PreparedStatement usage. Convert all raw concatenation to PreparedStatements. Create negative tests that pass SQL injection payloads (e.g., `'; DROP TABLE --`) and verify they are rejected.

---

### A07-03 — SQL injection via string concatenation in DriverDAO (critical security-sensitive methods)
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dao/DriverDAO.java`
- **Severity:** CRITICAL
- **Category:** Test Coverage / Security
- **Description:** DriverDAO contains 9 public methods, all using string-concatenated SQL. Two methods (`checkExpiry`, `sendIDDENY`) perform INSERT operations into the `outgoing` and `outgoing_stat` tables that send commands to physical vehicle hardware (IDDENY/IDAUTH messages). The `checkValidLicence` method (line 402) also performs INSERT operations and directly concatenates `userId` and `newRevewDate` into SQL. Without tests, there is zero validation that these security-critical data paths function correctly.
- **Evidence:**
  - Line 35: `extra += " and  \"FMS_USER_DEPT_REL\".\"CUST_CD\" = " + cust_cd;`
  - Line 87: `" and ur.\"CUST_CD\"='" + cust_cd  + "'"`
  - Line 159: `" and v.\"VEHICLE_TYPE_CD\" = "+ vehtype +" and ur.\"USER_CD\" = " + usercd`
  - Line 165: `"... \"VEHICLE_CD\" = '"+vehicle_cd+"' and \"USER_CD\" = '" + usercd + "'"`
  - Line 178: `"insert into \"outgoing\" (destination,message) values('"+unitGmtp+"','"+msg+"')"`
  - Line 420: `" and u.\"USER_CD\" = " + userId`
  - Line 550: `"  where \"USER_CD\" = "+driver_id`
- **Recommendation:** Priority 1: Test `sendIDDENY` and `checkValidLicence` methods thoroughly since they control physical access to vehicles. Verify IDDENY/IDAUTH message generation logic. Convert to PreparedStatements and write injection boundary tests.

---

### A07-04 — SQL injection in DriverImportDAO including write operations
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dao/DriverImportDAO.java`
- **Severity:** CRITICAL
- **Category:** Test Coverage / Security
- **Description:** DriverImportDAO has 18 public methods. While `saveDriverInfo` and `updateDriverInfo` correctly use PreparedStatements (lines 516, 929), query methods like `checkDriverByNm` (line 29) and `checkDriverByLic` (line 83) concatenate `fname`, `lname`, and `licence` directly into SQL. The `saveLicenseExpiryBlackListInfo` method (line 559, 920 lines long) is an extremely complex method mixing PreparedStatements with raw string concatenation (lines 738, 749, 800, 839) and has commented-out `finally` block cleanup code (lines 893-917).
- **Evidence:**
  - Line 29-30: `"select id from driver where trim(both ' ' from first_name) ilike trim ( both ' ' from '" + fname + "')" + "  and trim(both ' ' from last_name) ilike trim ( both ' ' from '" + lname + "')"`
  - Line 83: `"select id from driver where trim(both ' ' from licno) ilike trim(both ' ' from '" + licence + "')" + "  and comp_id = " + compId`
  - Line 738: `sql = "delete from \"fms_vehicle_access_mapper\" where \"user_cd\" = '"+bean.getDriverCd()+"'";`
  - Line 749: `sql="insert into \"fms_vehicle_access_mapper\" (user_cd,sel_type,sel_val) values('"+bean.getDriverCd()+"','veh','"+rs.getString(1)+"')";`
  - Lines 893-917: Commented-out resource cleanup in `finally` block of `saveLicenseExpiryBlackListInfo`
  - Line 984: `"update driver set active = false where id=" + id` (in `delDriverById`)
  - Line 1152: `"update driver_licence_expiry_mst set document_url='"+url+"' where id ="+licenceid` (in `uploadLicence`)
  - Line 1185: `"update \"FMS_USR_MST\" set document_url='"+url+"' where \"USER_CD\" ="+uid` (in `uploadLicenceAU`)
- **Recommendation:** Write tests for all 18 methods. `saveLicenseExpiryBlackListInfo` needs particular attention -- it is ~360 lines with deeply nested logic, mixed statement types, and commented-out cleanup. Test both happy-path and error scenarios for `uploadLicence` and `uploadLicenceAU` which accept URL parameters directly into SQL (path traversal and injection risk).

---

### A07-05 — Untested error-swallowing pattern across all DAO classes
- **File:** All 10 DAO files
- **Severity:** HIGH
- **Category:** Test Coverage / Error Handling
- **Description:** A pervasive anti-pattern exists across virtually every method in all 10 DAO files: exceptions are caught with `catch(Exception e)` and only `e.printStackTrace()` and `e.getMessage()` are called. The `e.getMessage()` call on line 64 (BatteryDAO), line 65 (DriverDAO), etc. is a no-op -- its return value is never used. This means all database failures, connection errors, and SQL exceptions are silently swallowed, and the method returns an empty collection or default value. Without tests, there is no verification that callers handle these silent failures correctly.
- **Evidence (non-exhaustive, pattern repeats in every method):**
  - BatteryDAO lines 61-65, 119-123, 236-240, 338-342, 373-377, 408-412
  - DriverDAO lines 62-66, 127-131, 234-238, 285-289, 338-342, 389-393, 476-480, 525-529, 557-561
  - LockOutDAO lines 67-71, 131-135
  - PreCheckDAO lines 114-118, 168-172, 254-258, 302-306, 419-423, 566-570
  - ImpactDAO lines 85-89, 164-168, 245-249, 329-333
  - UnitDAO lines 89-93, 146-150, 197-201, 254-258, etc. (repeated in 36+ methods)
  - RegisterDAO lines 446-450, 484-488, 521-525
- **Recommendation:** Write tests that mock `DBUtil.getConnection()` to throw `SQLException` and verify correct propagation. At minimum, these methods should log the error via a proper logger and either throw or return a sentinel value that callers check. Test that callers do not treat empty results as "no data" when it actually means "query failed."

---

### A07-06 — Untested connection and resource leaks in DriverImportDAO.saveLicenseExpiryBlackListInfo
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dao/DriverImportDAO.java`
- **Severity:** HIGH
- **Category:** Test Coverage / Resource Management
- **Description:** The `saveLicenseExpiryBlackListInfo` method (lines 559-922) has a deliberately commented-out `finally` block (lines 893-917) that was supposed to close ResultSets, PreparedStatements, and Statements. Only `DBUtil.closeConnection(conn)` is called in the actual finally block (line 918). Multiple `Statement` and `ResultSet` objects created within the method body (e.g., `stmt` at line 688, `rset` at line 690, `stmt2` at line 751) are closed inline but only in the happy path. If any exception occurs mid-method, these resources leak.
- **Evidence:**
  - Lines 893-917: Entire cleanup block commented out with `/* ... */`
  - Line 576: `Statement stmt1 = conn.createStatement(...)` -- closed at line 878 only if no exception
  - Line 688: `Statement stmt = conn.createStatement(...)` -- closed locally but only in try block
  - Line 751: `Statement stmt2 = conn.createStatement(...)` -- closed locally but only in try block
- **Recommendation:** Write resource-leak tests using mock connections. Verify all JDBC resources are closed in all paths. Uncomment and fix the `finally` block. Consider try-with-resources refactoring.

---

### A07-07 — Untested connection leak in DriverImportDAO.saveDriverInfo and updateDriverInfo
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dao/DriverImportDAO.java`
- **Severity:** HIGH
- **Category:** Test Coverage / Resource Management
- **Description:** In `saveDriverInfo` (line 511) and `updateDriverInfo` (line 924), the connection is only closed inside a conditional `if (null != ps)` block within `finally`. If `ps` is never assigned (e.g., if `DriverImportBean` is null and the method returns `false` at line 540), the connection acquired at line 520 is never closed, causing a connection pool leak.
- **Evidence:**
  - Lines 547-554 (`saveDriverInfo`): `finally { if (null != ps) { ps.close(); DBUtil.closeConnection(conn); } }` -- connection close is inside the ps null-check
  - Lines 961-968 (`updateDriverInfo`): Same pattern -- `finally { if (null != ps) { ps.close(); DBUtil.closeConnection(conn); } }`
- **Recommendation:** Write tests with null DriverImportBean to trigger the early-return path and verify the connection is still closed. Move `DBUtil.closeConnection(conn)` outside the `if (null != ps)` block.

---

### A07-08 — MessageDao uses instance-level JDBC fields (non-thread-safe)
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dao/MessageDao.java`
- **Severity:** HIGH
- **Category:** Test Coverage / Thread Safety
- **Description:** Unlike all other DAOs in this package that use method-local JDBC variables, `MessageDao` stores `Connection conn`, `Statement stmt`, `ResultSet rset`, and `String queryString` as instance fields (lines 15-18). If a single `MessageDao` instance is shared across threads (common in servlet containers), concurrent requests will corrupt each other's database state. The `init()` method acquires its own DataSource connection directly via JNDI (line 54-56) rather than using `DBUtil.getConnection()`, deviating from the pattern used everywhere else. No tests exist to verify thread safety or connection management.
- **Evidence:**
  - Line 15: `Connection conn;` (instance field)
  - Line 16: `Statement stmt;` (instance field)
  - Line 17: `ResultSet rset;` (instance field)
  - Line 18: `String queryString = "";` (instance field)
  - Line 62: `queryString = "select * from mnt_msg where \"FORM_CD\"="+fid;` -- `fid` is also an instance field, SQL injection risk
  - Line 105: `selectMesssage()` uses instance `conn` and `stmt` without null-checking
- **Recommendation:** Write concurrent access tests demonstrating the race condition. Refactor to use method-local JDBC resources and `DBUtil.getConnection()`. Add SQL injection tests for the `fid` parameter.

---

### A07-09 — SQL injection in ImportDAO with extremely large attack surface
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dao/ImportDAO.java`
- **Severity:** CRITICAL
- **Category:** Test Coverage / Security
- **Description:** ImportDAO is the largest DAO (~4900+ lines) with 16 public methods, many of which perform INSERT, UPDATE, and DELETE operations. The `saveQuestions` methods (lines 30, 199) build INSERT statements by concatenating `qbean.getQuestion()` directly into SQL (lines 166, 334) -- if a question contains a single quote, the query breaks or allows injection. The `saveQuestionsTab` method (line 608) also concatenates user input into INSERT statements (line 851). The `removePreviousChecklist` method (line 541) concatenates check codes into a DELETE statement (line 569). The `saveDriverInfo` method (line 907) is ~480 lines long with 6 Statement/ResultSet pairs.
- **Evidence:**
  - Line 166-167: `"values ('"+chk_cd+"','"+qbean.getVeh_typ_cd()+"','"+order+"','"+qbean.getQuestion()+"','"+qbean.getAns_type()+"',..."`
  - Line 334: Same pattern with additional language fields concatenated
  - Line 569: `"DELETE FROM \"FMS_OPCHK_QUEST_MST\" where \"CHK_CD\" in ("+ chkCds +"); "`
  - Line 680: `" AND LOWER(l.\"NAME\") = '" + qbean.getLoc_cd().toLowerCase().trim() + "' "`
  - Line 698: `" WHERE LOWER(d.\"DEPT_NAME\") = '" + qbean.getDept_cd().toLowerCase().trim() + "' "`
  - Line 851-852: INSERT with concatenated question text
- **Recommendation:** Write injection tests for all methods, focusing on `saveQuestions` with question text containing SQL metacharacters. Convert all DML operations to PreparedStatements. Test `removePreviousChecklist` with manipulated `chkList` values.

---

### A07-10 — Untested registration flow in RegisterDAO with multi-table transactional writes
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dao/RegisterDAO.java`
- **Severity:** CRITICAL
- **Category:** Test Coverage / Data Integrity
- **Description:** The `register` method (line 17, ~440 lines) performs over 15 sequential INSERT operations across 10+ database tables (`FMS_CUST_MST`, `FMS_LOC_MST`, `FMS_DEPT_MST`, `FMS_CUST_DEPT_REL`, `FMS_USR_CUST_REL`, `FMS_GRP_MST`, `FMS_OPCHK_QUEST_MST`, `FMS_VEHICLE_MST`, `FMS_USR_VEHICLE_REL`, `FMS_USR_MST`, `FMS_USR_GRP_REL`, `FMS_USER_DEPT_REL`) without any transaction management. If any INSERT fails mid-way (returning `null` on lines 75, 85, etc.), the database is left in a partially-created state with orphaned records. While PreparedStatements are used (good), there is no `conn.setAutoCommit(false)` / `conn.commit()` / `conn.rollback()` pattern. The error-swallowing `catch` block (lines 446-450) means partial registration failures go unnoticed.
- **Evidence:**
  - Line 17-458: Single method with 15+ INSERT operations, no transaction boundaries
  - Lines 75, 85, 107, 131, 151, 203, 246, 258, 328, 338, 350, 418, 427, 439: Each returns `null` on failure, leaving prior INSERTs committed
  - Line 284: `sql = "select count(*) from \"FMS_USR_MST\" where \"USER_NAME\" = '"+user_nm+"'"` -- SQL injection in username check
  - Line 294: Same pattern in loop
  - Line 373: Same pattern again
  - Lines 446-450: `catch(Exception e) { e.printStackTrace(); e.getMessage(); }` -- swallows all errors
- **Recommendation:** Write integration tests covering: (1) successful complete registration, (2) failure at each INSERT point to verify rollback, (3) duplicate company name detection. Add transaction management with commit/rollback. Test the `checkAuthority` method (line 498) which compares MD5 hashes of credentials stored in `RuntimeConf` -- verify timing-safe comparison.

---

### A07-11 — Untested SQL injection in LockOutDAO and PreCheckDAO date parameters
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dao/LockOutDAO.java`, `WEB-INF/src/com/torrent/surat/fms6/dao/PreCheckDAO.java`
- **Severity:** HIGH
- **Category:** Test Coverage / Security
- **Description:** LockOutDAO's `getLockOutDataNtlRpt` (line 80) and PreCheckDAO's `getChecks` (line 26) and `getCheckSummary` (line 181) concatenate date parameters (`st_dt`, `end_dt`, `from`, `to`, `month`) directly into SQL timestamp casts. Also, LockOutDAO line 122 maps unrecognized lockout reason codes to "Question" instead of "Other" (inconsistent with line 57's logic), which is a logic bug that tests would catch.
- **Evidence:**
  - LockOutDAO line 103: `" and unlocked_utc_time >= '"+st_dt+"'::timestamp and unlocked_utc_time < '"+end_dt+"'::timestamp + interval '1 day' "`
  - PreCheckDAO line 45: `" and starttimestamp  >= '"+from+"'::timestamp and starttimestamp < '"+to+"'::timestamp + interval '1 day'"`
  - PreCheckDAO line 50: `" and starttimestamp  >= '"+month+"'::timestamp and starttimestamp < '"+month+"'::timestamp + interval '1 month'"`
  - PreCheckDAO line 335: `"select EXTRACT(WEEK FROM '"+from+"'::timestamp), EXTRACT(WEEK FROM '"+to+"'::timestamp)"`
  - PreCheckDAO line 453: `"select EXTRACT(WEEK FROM '"+DataUtil.formatStringDate(from)+"'::timestamp)..."`
  - LockOutDAO lines 57-59 vs 120-123: Inconsistent mapping of reason codes ("Other" vs "Question" for else branch)
- **Recommendation:** Write tests for both DAOs with injection payloads in date parameters. Write a test specifically for LockOutDAO reason code mapping to detect the logic bug at line 122. Convert all date parameters to PreparedStatement parameters.

---

### A07-12 — Untested complex business logic in ImpactDAO with N+1 query patterns
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dao/ImpactDAO.java`
- **Severity:** HIGH
- **Category:** Test Coverage / Performance
- **Description:** ImpactDAO has 11 public methods with complex nested loops that generate O(departments x models x months) individual SQL queries per invocation. `getRedImpactCache` (line 33) iterates departments, then models, then months, firing a separate query for each combination. `getRedImpactCacheByDriver` (line 98) adds a driver dimension, creating O(depts x drivers x models x months) queries. `getImpacts` (line 342) computes impact severity levels using `RuntimeConf.RED_LEVEL`, `RuntimeConf.AMBER_LEVEL`, and `RuntimeConf.Blue_LEVEL` (note inconsistent capitalization). Without tests, these performance-critical paths and their threshold calculations are completely unverified.
- **Evidence:**
  - Lines 52-83: Triple-nested loop (depts x models x months) each executing a separate query
  - Lines 117-162: Quadruple-nested loop (depts x drivers x models x months)
  - Lines 357-425: Double loop with complex CASE WHEN threshold logic using RuntimeConf constants
  - Line 388: `RuntimeConf.Blue_LEVEL` (inconsistent casing vs `RED_LEVEL`, `AMBER_LEVEL`)
  - Lines 203-243: `getRedImpact` fires individual queries per department per month
- **Recommendation:** Write performance tests that measure query count per invocation. Write threshold logic unit tests (extract the RED/AMBER/BLUE classification into a testable pure function). Test edge cases: zero departments, zero models, year boundary crossings.

---

### A07-13 — Untested UnitDAO methods with SQL injection in 36+ methods
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dao/UnitDAO.java`
- **Severity:** CRITICAL
- **Category:** Test Coverage / Security
- **Description:** UnitDAO is the most-referenced DAO in the package (used by BatteryDAO, DriverDAO, ImpactDAO, LockOutDAO, PreCheckDAO) with 36+ public methods. Every method uses string-concatenated SQL. The `getUnitLstByModel` method (line 159) is particularly critical as its return value (a comma-separated list of vehicle codes) is embedded directly into IN clauses by calling DAOs -- creating a second-order SQL injection vector. If `getUnitLstByModel` returns corrupted data, every DAO that consumes it becomes vulnerable.
- **Evidence:**
  - Line 68: `extra += " and  \"FMS_CUST_DEPT_REL\".\"USER_CD\" = " + cust_cd;`
  - Line 172: `filters = " r.\"USER_CD\" = " + cust_cd;`
  - Line 176: `filters += "  and r.\"LOC_CD\" in (" + loc_cd +")";`
  - Line 181: `filters += " and r.\"DEPT_CD\" in (" + dept_cd + ")";`
  - Line 186: `filters += " AND t.\"REPORT_DESCRIPTION_CD\" = " + model_cd;`
  - Line 195: `idlst += ",'"+rs.getString(1)+"'";` -- builds IN-clause list, consumed by 8+ other DAO methods
  - Line 282: `extra += " \"USER_CD\" = " + cust_cd;`
  - Line 450: `"where \"LOCATION_CD\" = " +loc_cd`
  - Line 485: `"where \"USER_CD\" = " +cust_cd`
  - Line 521: `"where \"LOCATION_CD\" = " +loc_cd`
- **Recommendation:** Test `getUnitLstByModel` first since it is the foundational query method. Write tests that verify the generated ID list format. Test with empty results, single results, and large result sets. Convert to PreparedStatements with IN-clause array binding.

---

### A07-14 — RegisterDAO.checkAuthority uses MD5 and compares server credentials in database
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dao/RegisterDAO.java`
- **Severity:** HIGH
- **Category:** Test Coverage / Security
- **Description:** The `checkAuthority` method (line 498) sends `RuntimeConf.username` and `RuntimeConf.password` to the database to compute MD5 hashes via SQL (`select md5('"+RuntimeConf.username+"'),md5('"+RuntimeConf.password+"')`), then compares the results with the provided `username` and `password` parameters. This approach: (1) sends plaintext credentials over the JDBC connection, (2) uses the weak MD5 hash function, (3) concatenates `RuntimeConf` values into SQL (injection risk if they contain quotes), and (4) uses `equalsIgnoreCase` comparison which is not timing-safe. No tests verify this authentication logic.
- **Evidence:**
  - Line 511: `String sql = "select md5('"+RuntimeConf.username+"'),md5('"+RuntimeConf.password+"')";`
  - Line 515: `if(rs.getString(1).equalsIgnoreCase(username) && rs.getString(2).equalsIgnoreCase(password))`
- **Recommendation:** Write tests for authentication: valid credentials, invalid credentials, SQL-injection in RuntimeConf values, case sensitivity behavior. Replace MD5 with bcrypt/scrypt. Move hash computation to application layer. Use constant-time comparison.

---

### A07-15 — Untested N+1 query anti-pattern in PreCheckDAO.getChecks
- **File:** `WEB-INF/src/com/torrent/surat/fms6/dao/PreCheckDAO.java`
- **Severity:** HIGH
- **Category:** Test Coverage / Performance
- **Description:** The `getChecks` method at line 26 retrieves all checklist result IDs, then loops through them individually (lines 78-94), executing a separate SQL query per ID to count failed answers. For large deployments, this creates thousands of individual queries per invocation. The `getCheckSummary` method (line 181) similarly loops per unit, executing 2+ queries per unit. `getChecksByDriver` (line 433) has a quadruple nested structure: locations x departments x drivers x weeks. None of these performance-critical paths have tests.
- **Evidence:**
  - Lines 78-94: `for(int i=0;i<arrId.size();i++) { sql = "select count(id) from op_chk_checklistanswer where checklist_result_id = '" + arrId.get(i) + "'..."; }`
  - Lines 209-253: Loop per unit with 2 queries each
  - Lines 376-405: Loop per department with query per week
  - Lines 485-553: Quadruple nested loop with multiple queries per iteration
- **Recommendation:** Write load tests that measure query count and response time. Refactor N+1 patterns to use batch queries or JOINs. Test with realistic data volumes (hundreds of units, thousands of checklist results).

---

## Summary

| File | Public Methods | Test Coverage | Severity |
|---|---|---|---|
| BatteryDAO.java | 6 | 0% | CRITICAL |
| DriverDAO.java | 9 | 0% | CRITICAL |
| DriverImportDAO.java | 18 | 0% | CRITICAL |
| ImpactDAO.java | 11 | 0% | CRITICAL |
| ImportDAO.java | 16 | 0% | CRITICAL |
| LockOutDAO.java | 2 | 0% | HIGH |
| MessageDao.java | 8 | 0% | HIGH |
| PreCheckDAO.java | 6 | 0% | HIGH |
| RegisterDAO.java | 3 | 0% | CRITICAL |
| UnitDAO.java | 36 | 0% | CRITICAL |
| **TOTAL** | **115** | **0%** | **CRITICAL** |

**Total findings:** 15

| Severity | Count |
|---|---|
| CRITICAL | 8 (A07-01, A07-02, A07-03, A07-04, A07-09, A07-10, A07-13) |
| HIGH | 7 (A07-05, A07-06, A07-07, A07-08, A07-11, A07-12, A07-14, A07-15) |

### Priority Test Implementation Order
1. **UnitDAO.getUnitLstByModel** -- Foundation method used by 8+ other DAOs; second-order injection vector
2. **DriverDAO.sendIDDENY / checkValidLicence** -- Controls physical vehicle access hardware
3. **RegisterDAO.register** -- Multi-table write without transaction management
4. **ImportDAO.saveQuestions / saveDriverInfo** -- Write operations with concatenated user text
5. **DriverImportDAO.saveLicenseExpiryBlackListInfo** -- Complex 360-line method with resource leaks
6. **RegisterDAO.checkAuthority** -- Authentication bypass risk
7. **All remaining query methods** -- SQL injection in read paths
