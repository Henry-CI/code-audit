# Pass 2 -- Test Coverage: bean package (A-D)
**Agent:** A01
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

---

## Test Infrastructure Assessment

The FleetFocus repository has **zero test infrastructure**:

- No `test/` or `src/test/` directory exists anywhere in the project.
- No JUnit or TestNG dependencies are present.
- No files import `org.junit`, `org.testng`, or use `@Test` annotations.
- The only file with "Test" in its name is `WEB-INF/src/com/torrent/surat/fms6/util/EncryptTest.java`, which is a **decompiled production encryption utility** (decompiled by DJ v3.9.9.91, dated 2006-01-25) containing `encrypt()` and `decrypt()` methods -- it is NOT a test file.
- A comprehensive grep for test-related references to all 14 assigned classes returned zero results.

**Conclusion:** There is absolutely no automated test coverage for any class in this package.

---

## Reading Evidence

### 1. BatteryBean.java
- **Full path:** `WEB-INF/src/com/torrent/surat/fms6/bean/BatteryBean.java`
- **Class:** `com.torrent.surat.fms6.bean.BatteryBean implements Serializable`
- **serialVersionUID:** `477363925476952636L` (line 10)
- **Fields (lines 11-33):** `batteryId`, `unit_nm`, `unit_serial`, `unit_cd`, `charge_tm`, `bef_bat_id`, `bef_veh_nm`, `bef_dri_nm`, `bef_soc`, `bef_hm`, `bef_tm`, `aft_bat_id`, `aft_veh_nm`, `aft_dri_nm`, `aft_soc`, `aft_hm`, `aft_tm`, `duration`, `isTruck1120` (boolean), `bef_bat_fleet_num`, `aft_bat_fleet_num`, `bat_fleet_num`
- **Public methods:**
  - `getUnit_serial()` / `setUnit_serial(String)` (lines 35-40)
  - `getBatteryId()` / `setBatteryId(String)` (lines 41-46)
  - `getCharge_tm()` / `setCharge_tm(String)` (lines 47-52)
  - `getBef_veh_nm()` / `setBef_veh_nm(String)` (lines 53-58)
  - `getBef_dri_nm()` / `setBef_dri_nm(String)` (lines 59-64)
  - `getBef_soc()` / `setBef_soc(String)` (lines 65-70)
  - `getBef_hm()` / `setBef_hm(String)` (lines 71-76)
  - `getAft_veh_nm()` / `setAft_veh_nm(String)` (lines 77-82)
  - `getAft_dri_nm()` / `setAft_dri_nm(String)` (lines 83-88)
  - `getAft_soc()` / `setAft_soc(String)` (lines 89-94)
  - `getAft_hm()` / `setAft_hm(String)` (lines 95-100)
  - `getUnit_nm()` / `setUnit_nm(String)` (lines 101-106)
  - `getBef_tm()` / `setBef_tm(String)` (lines 107-112)
  - `getAft_tm()` / `setAft_tm(String)` (lines 113-118)
  - `getBef_bat_id()` / `setBef_bat_id(String)` (lines 119-124)
  - `getAft_bat_id()` / `setAft_bat_id(String)` (lines 125-130)
  - `getUnit_cd()` / `setUnit_cd(String)` (lines 131-136)
  - `getDuration()` / `setDuration(String)` (lines 137-142)
  - `isTruck1120()` / `setTruck1120(boolean)` (lines 143-148)
  - `getBef_bat_fleet_num()` / `setBef_bat_fleet_num(String)` (lines 149-154)
  - `getAft_bat_fleet_num()` / `setAft_bat_fleet_num(String)` (lines 155-160)
  - `getBat_fleet_num()` / `setBat_fleet_num(String)` (lines 161-166)
- **Test references found:** None

---

### 2. BroadcastmsgBean.java
- **Full path:** `WEB-INF/src/com/torrent/surat/fms6/bean/BroadcastmsgBean.java`
- **Class:** `com.torrent.surat.fms6.bean.BroadcastmsgBean implements Serializable`
- **serialVersionUID:** `1426963314759419124L` (line 10)
- **Fields (lines 12-21):** `text`, `type`, `disp_timestamp`, `resp_timestamp`, `response`, `driver`, `unit`, `product_type`, `sent_timestamp`, `veh_id`
- **Public methods:**
  - `getSent_timestamp()` / `setSent_timestamp(String)` (lines 23-28)
  - `getText()` (line 29) / `setText(String)` (line 50)
  - `getType()` (line 32) / `setType(String)` (line 53)
  - `getDisp_timestamp()` (line 35) / `setDisp_timestamp(String)` (line 56)
  - `getResp_timestamp()` (line 38) / `setResp_timestamp(String)` (line 59)
  - `getResponse()` (line 41) / `setResponse(String)` (line 62)
  - `getDriver()` (line 44) / `setDriver(String)` (line 65)
  - `getUnit()` (line 47) / `setUnit(String)` (line 68)
  - `getProduct_type()` (line 71) / `setProduct_type(String)` (line 74)
  - `getVeh_id()` (line 77) / `setVeh_id(String)` (line 80)
- **Test references found:** None

---

### 3. CanruleBean.java
- **Full path:** `WEB-INF/src/com/torrent/surat/fms6/bean/CanruleBean.java`
- **Class:** `com.torrent.surat.fms6.bean.CanruleBean`
- **Fields (lines 5-17):** `src_holder`, `site_name`, `department_name`, `model_name`, `gmtp_id`, `serial_no`, `hire_no`, `canrule_name`, `custCd`, `access_level`, `access_cust`, `access_site`, `access_dept`
- **Public methods:**
  - `getSrc_holder()` / `setSrc_holder(String)` (lines 19-24)
  - `getSite_name()` / `setSite_name(String)` (lines 25-30)
  - `getDepartment_name()` / `setDepartment_name(String)` (lines 31-36)
  - `getModel_name()` / `setModel_name(String)` (lines 37-42)
  - `getGmtp_id()` / `setGmtp_id(String)` (lines 43-48)
  - `getSerial_no()` / `setSerial_no(String)` (lines 49-54)
  - `getHire_no()` / `setHire_no(String)` (lines 55-60)
  - `getCanrule_name()` / `setCanrule_name(String)` (lines 61-66)
  - `getCustCd()` / `setCustCd(String)` (lines 67-72)
  - `getAccess_level()` / `setAccess_level(String)` (lines 73-78)
  - `getAccess_cust()` / `setAccess_cust(String)` (lines 79-84)
  - `getAccess_site()` / `setAccess_site(String)` (lines 85-90)
  - `getAccess_dept()` / `setAccess_dept(String)` (lines 91-96)
- **Test references found:** None

---

### 4. CustLocDeptBean.java
- **Full path:** `WEB-INF/src/com/torrent/surat/fms6/bean/CustLocDeptBean.java`
- **Class:** `com.torrent.surat.fms6.bean.CustLocDeptBean`
- **Fields (line 4):** `custCd` (int), `locCd` (int), `deptCd` (int)
- **Public methods:**
  - `getCustCd()` / `setCustCd(int)` (lines 6-12)
  - `getLocCd()` / `setLocCd(int)` (lines 14-20)
  - `getDeptCd()` / `setDeptCd(int)` (lines 22-28)
- **Test references found:** None

---

### 5. CustomerBean.java
- **Full path:** `WEB-INF/src/com/torrent/surat/fms6/bean/CustomerBean.java`
- **Class:** `com.torrent.surat.fms6.bean.CustomerBean`
- **Fields (lines 5-7):** `id` (int), `passwordPolicy` (boolean), `active` (boolean)
- **Public methods:**
  - `isActive()` / `setActive(boolean)` (lines 9-14)
  - `getId()` / `setId(int)` (lines 15-23)
  - `isPasswordPolicy()` / `setPasswordPolicy(boolean)` (lines 18-26)
- **Test references found:** None

---

### 6. DailyUsageDeptDataBean.java
- **Full path:** `WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageDeptDataBean.java`
- **Class:** `com.torrent.surat.fms6.bean.DailyUsageDeptDataBean implements Serializable`
- **Fields (lines 8-17):** `dept_id` (String), `dept_name` (String), `modelName` (String), `data` (ArrayList<double[]>), `loc` (String), `week` (String), `wFrom` (String), `wTo` (String), `weekInt` (int), `unitTotal` (int)
- **Constructors:**
  - `DailyUsageDeptDataBean()` (line 19)
  - `DailyUsageDeptDataBean(String dept_id, String dept_name, String modelName, ArrayList<double[]> data)` (line 23)
- **Public methods:**
  - `getDept_id()` / `setDept_id(String)` (lines 31-37)
  - `getDept_name()` / `setDept_name(String)` (lines 39-45)
  - `getModelName()` / `setModelName(String)` (lines 47-53)
  - `getData()` / `setData(ArrayList<double[]>)` (lines 55-61)
  - `getLoc()` / `setLoc(String)` (lines 63-69)
  - `getWeek()` / `setWeek(String)` (lines 71-77)
  - `getwFrom()` / `setwFrom(String)` (lines 79-85)
  - `getwTo()` / `setwTo(String)` (lines 87-93)
  - `getWeekInt()` / `setWeekInt(int)` (lines 95-101)
  - `getUnitTotal()` / `setUnitTotal(int)` (lines 103-109)
- **Test references found:** None

---

### 7. DailyUsageHourBean.java
- **Full path:** `WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java`
- **Class:** `com.torrent.surat.fms6.bean.DailyUsageHourBean implements Serializable`
- **Fields (lines 10-16):** `ifCombine` (boolean), `deptList` (ArrayList<String>), `modelList` (ArrayList<String>), `deptDataList` (ArrayList<DailyUsageDeptDataBean>), `finalUtil` (ArrayList<String>), `weekList` (ArrayList<String>), `week` (String)
- **Constructors:**
  - `DailyUsageHourBean()` (line 18)
  - `DailyUsageHourBean(boolean ifCombine, ArrayList<DailyUsageDeptDataBean> deptDataList)` (line 22)
- **Public methods (with business logic):**
  - `getModelList()` (line 27) -- iterates deptDataList, extracts unique model names
  - `arrangeData(String modelName)` (line 39) -- complex data arrangement: clears lists, iterates deptDataList, matches by week and model name, builds comma-delimited strings with heading arrays
  - `isIfCombine()` / `setIfCombine(boolean)` (lines 69-75)
  - `getDeptList()` / `setDeptList(ArrayList<String>)` (lines 77-83)
  - `getDeptDataList()` / `setDeptDataList(ArrayList<DailyUsageDeptDataBean>)` (lines 85-91)
  - `getFinalUtil()` / `setFinalUtil(ArrayList<String>)` (lines 93-99)
  - `getWeekList(String model)` (line 101) -- iterates deptDataList, extracts unique week info filtered by model
  - `setWeekList(ArrayList<String>)` (line 113)
  - `setModelList(ArrayList<String>)` (line 117)
  - `setWeek(String)` (line 121)
- **Test references found:** None

---

### 8. DashboarSubscriptionBean.java
- **Full path:** `WEB-INF/src/com/torrent/surat/fms6/bean/DashboarSubscriptionBean.java`
- **Class:** `com.torrent.surat.fms6.bean.DashboarSubscriptionBean`
- **Note:** Class name has a typo -- "Dashboar" instead of "Dashboard"
- **Fields (lines 5-10):** `id` (int), `userCd` (int), `custCd` (int), `locCd` (String), `location` (String), `emailId` (String)
- **Public methods:**
  - `getId()` / `setId(int)` (lines 11-31)
  - `getUserCd()` / `setUserCd(int)` (lines 14-34)
  - `getCustCd()` / `setCustCd(int)` (lines 17-37)
  - `getLocCd()` / `setLocCd(String)` (lines 20-40)
  - `getLocation()` / `setLocation(String)` (lines 23-43)
  - `getEmailId()` / `setEmailId(String)` (lines 26-46)
- **Test references found:** None

---

### 9. DayhoursBean.java
- **Full path:** `WEB-INF/src/com/torrent/surat/fms6/bean/DayhoursBean.java`
- **Class:** `com.torrent.surat.fms6.bean.DayhoursBean implements Serializable`
- **serialVersionUID:** `-6236157294191909793L` (line 10)
- **Fields (lines 12-18):** `id` (String), `total_hours` (int, default 0), `total_mins` (int, default 0), `break_hours` (int, default 0), `break_mins` (int, default 0), `days` (int, default 0), `avail_hours` (String, default "00:00:00")
- **Public methods:**
  - `getId()` / `setId(String)` (lines 20-25)
  - `getTotal_hours()` / `setTotal_hours(int)` (lines 26-31)
  - `getTotal_mins()` / `setTotal_mins(int)` (lines 32-37)
  - `getBreak_hours()` / `setBreak_hours(int)` (lines 38-43)
  - `getBreak_mins()` / `setBreak_mins(int)` (lines 44-49)
  - `getDays()` / `setDays(int)` (lines 50-55)
  - `getAvail_hours()` / `setAvail_hours(String)` (lines 56-61)
- **Test references found:** None

---

### 10. DehireBean.java
- **Full path:** `WEB-INF/src/com/torrent/surat/fms6/bean/DehireBean.java`
- **Class:** `com.torrent.surat.fms6.bean.DehireBean`
- **Fields (lines 7-9):** `vehCd` (int), `hire_time` (java.sql.Timestamp), `dehire_time` (java.sql.Timestamp)
- **Public methods:**
  - `getVehCd()` / `setVehCd(int)` (lines 10-15)
  - `getHire_time()` / `setHire_time(Timestamp)` (lines 16-21)
  - `getDehire_time()` / `setDehire_time(Timestamp)` (lines 22-27)
- **Test references found:** None

---

### 11. DetailedReportUtil.java
- **Full path:** `WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java`
- **Class:** `com.torrent.surat.fms6.bean.DetailedReportUtil`
- **Fields (lines 8-28):** 18 raw-typed `ArrayList` fields: `vrpt_field_cd`, `vrpt_field_nm`, `vrpt_veh_typ_cd`, `vrpt_veh_typ`, `vrpt_veh_cd`, `vrpt_veh_nm`, `vrpt_veh_id`, `vrpt_veh_value_start`, `vrpt_veh_value_stop`, `vrpt_veh_value_state`, `vrpt_veh_value_stopv`, `vrpt_veh_driv_cd`, `vrpt_veh_driv_nm`, `vrpt_veh_driv_tm`, `vrpt_veh_sttm`, `vrpt_veh_endtm`, `vrpt_veh_tot`, `vrpt_veh_gtot`, `newFieldCdList`, `newFieldNameList`
- **Constructors:**
  - `DetailedReportUtil()` (line 30)
  - `DetailedReportUtil(ArrayList vrpt_field_cd, ArrayList vrpt_field_nm, ArrayList vrpt_veh_value_stop)` (line 34) -- includes `System.out.println` debug output (lines 39-41)
- **Public methods (with business logic):**
  - `analyzeAndCombine()` (line 44) -- iterates `vrpt_field_nm`, checks for strings containing "Hydraulic", "HYDR", or "HYDL"; body of the conditional block is currently empty (lines 49-51)
  - `getVrpt_field_cd()` / `setVrpt_field_cd(ArrayList)` (lines 57-62)
  - `getVrpt_field_nm()` / `setVrpt_field_nm(ArrayList)` (lines 63-68)
  - `getVrpt_veh_typ_cd()` / `setVrpt_veh_typ_cd(ArrayList)` (lines 69-74)
  - `getVrpt_veh_typ()` / `setVrpt_veh_typ(ArrayList)` (lines 75-80)
  - `getVrpt_veh_cd()` / `setVrpt_veh_cd(ArrayList)` (lines 81-86)
  - `getVrpt_veh_nm()` / `setVrpt_veh_nm(ArrayList)` (lines 87-92)
  - `getVrpt_veh_id()` / `setVrpt_veh_id(ArrayList)` (lines 93-98)
  - `getVrpt_veh_value_start()` / `setVrpt_veh_value_start(ArrayList)` (lines 99-104)
  - `getVrpt_veh_value_stop()` / `setVrpt_veh_value_stop(ArrayList)` (lines 105-110)
  - `getVrpt_veh_value_state()` / `setVrpt_veh_value_state(ArrayList)` (lines 111-116)
  - `getVrpt_veh_value_stopv()` / `setVrpt_veh_value_stopv(ArrayList)` (lines 117-122)
  - `getVrpt_veh_driv_cd()` / `setVrpt_veh_driv_cd(ArrayList)` (lines 123-128)
  - `getVrpt_veh_driv_nm()` / `setVrpt_veh_driv_nm(ArrayList)` (lines 129-134)
  - `getVrpt_veh_driv_tm()` / `setVrpt_veh_driv_tm(ArrayList)` (lines 135-140)
  - `getVrpt_veh_sttm()` / `setVrpt_veh_sttm(ArrayList)` (lines 141-146)
  - `getVrpt_veh_endtm()` / `setVrpt_veh_endtm(ArrayList)` (lines 147-152)
  - `getVrpt_veh_tot()` / `setVrpt_veh_tot(ArrayList)` (lines 153-158)
  - `getVrpt_veh_gtot()` / `setVrpt_veh_gtot(ArrayList)` (lines 159-164)
- **Test references found:** None

---

### 12. DriverBean.java
- **Full path:** `WEB-INF/src/com/torrent/surat/fms6/bean/DriverBean.java`
- **Class:** `com.torrent.surat.fms6.bean.DriverBean implements Serializable`
- **Fields (lines 6-9):** `id` (String), `user_cd` (String), `weigand` (String), `veh_type` (String)
- **Public methods:**
  - `getUser_cd()` / `setUser_cd(String)` (lines 12-17)
  - `getId()` / `setId(String)` (lines 18-23)
  - `getWeigand()` / `setWeigand(String)` (lines 24-29)
  - `getVeh_type()` / `setVeh_type(String)` (lines 30-35)
- **Test references found:** None

---

### 13. DriverImportBean.java
- **Full path:** `WEB-INF/src/com/torrent/surat/fms6/bean/DriverImportBean.java`
- **Class:** `com.torrent.surat.fms6.bean.DriverImportBean implements Serializable`
- **serialVersionUID:** `-6234180688512824118L` (line 7)
- **Fields (lines 8-31):** `id`, `department`, `site`, `first_name`, `last_name`, `licno`, `expirydt`, `phone`, `active`, `location`, `comp_id`, `card_no`, `facility_code`, `key_reader`, `custCd`, `locCd`, `deptCd`, `cardType`, `access_level`, `access_cust`, `access_site`, `access_dept`, `licenseType` (String, default ""), `denyOnExp` (boolean, default false)
- **Public methods:**
  - `getKey_reader()` / `setKey_reader(String)` (lines 33-38)
  - `getFacility_code()` / `setFacility_code(String)` (lines 39-44)
  - `getId()` / `setId(String)` (lines 45-50)
  - `getLicno()` / `setLicno(String)` (lines 51-56)
  - `getPhone()` / `setPhone(String)` (lines 57-62)
  - `getActive()` / `setActive(String)` (lines 63-68)
  - `getLocation()` / `setLocation(String)` (lines 69-74)
  - `getDepartment()` / `setDepartment(String)` (lines 75-80)
  - `getSite()` / `setSite(String)` (lines 81-86)
  - `getComp_id()` / `setComp_id(String)` (lines 87-92)
  - `getFirst_name()` / `setFirst_name(String)` (lines 93-98)
  - `getLast_name()` / `setLast_name(String)` (lines 99-104)
  - `getExpirydt()` / `setExpirydt(String)` (lines 105-110)
  - `getCard_no()` / `setCard_no(String)` (lines 111-116)
  - `getCustCd()` / `setCustCd(String)` (lines 117-122)
  - `getLocCd()` / `setLocCd(String)` (lines 123-128)
  - `getDeptCd()` / `setDeptCd(String)` (lines 129-134)
  - `getCardType()` / `setCardType(String)` (lines 135-140)
  - `getAccess_level()` / `setAccess_level(String)` (lines 141-146)
  - `getAccess_cust()` / `setAccess_cust(String)` (lines 147-152)
  - `getAccess_site()` / `setAccess_site(String)` (lines 153-158)
  - `getAccess_dept()` / `setAccess_dept(String)` (lines 159-164)
  - `getLicenseType()` / `setLicenseType(String)` (lines 165-170)
  - `isDenyOnExp()` / `setDenyOnExp(boolean)` (lines 171-176)
- **Test references found:** None

---

### 14. DriverLeagueBean.java
- **Full path:** `WEB-INF/src/com/torrent/surat/fms6/bean/DriverLeagueBean.java`
- **Class:** `com.torrent.surat.fms6.bean.DriverLeagueBean`
- **Fields (lines 4-12):** `id` (int), `driverName` (String), `department` (String), `truckType` (String), `redImpact` (String), `preOp` (String), `keyHour` (String), `tracHours` (String), `percActive` (String)
- **Public methods:**
  - `getId()` / `setId(int)` (lines 14-19)
  - `getDriverName()` / `setDriverName(String)` (lines 20-25)
  - `getDepartment()` / `setDepartment(String)` (lines 26-31)
  - `getTruckType()` / `setTruckType(String)` (lines 32-37)
  - `getRedImpact()` / `setRedImpact(String)` (lines 38-43)
  - `getPreOp()` / `setPreOp(String)` (lines 44-49)
  - `getKeyHour()` / `setKeyHour(String)` (lines 50-55)
  - `getTracHours()` / `setTracHours(String)` (lines 56-61)
  - `getPercActive()` / `setPercActive(String)` (lines 62-67)
- **Test references found:** None

---

## Findings

### A01-1 -- No test framework or infrastructure exists in the repository
- **File:** (repository-wide)
- **Severity:** CRITICAL
- **Category:** Test Coverage > Test Infrastructure
- **Description:** The entire FleetFocus repository contains zero test files, no test directories, no JUnit/TestNG dependencies, and no test runner configuration. This means every class in the codebase, including all 14 files in this audit scope, has 0% test coverage. No automated regression protection exists for any functionality.
- **Evidence:** `Glob` for `**/test/**/*.java` returned no results. `Grep` for `import org.junit|import org.testng|@Test` across `WEB-INF/src` returned no results. The only `*Test.java` file (`EncryptTest.java`) is a decompiled production class, not a test.
- **Recommendation:** Establish a test framework (JUnit 5 + Maven/Gradle) with a proper `src/test/java` directory structure. Configure CI to run tests on every commit. Begin with the highest-risk classes identified below.

---

### A01-2 -- DailyUsageHourBean.arrangeData() has untested business logic with data transformation
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java`:39
- **Severity:** HIGH
- **Category:** Test Coverage > Business Logic
- **Description:** The `arrangeData(String modelName)` method (lines 39-67) contains significant business logic: it clears shared state (`deptList`, `finalUtil`), performs nested iteration over `deptDataList`, filters by week and model name using `equalsIgnoreCase`, constructs comma-delimited strings from heading arrays, and uses `Arrays.toString()` with manual bracket stripping. This method has multiple potential failure modes: NullPointerException if `this.week` is null (line 49), incorrect data if `deptDataList` contains null entries, and subtle string formatting bugs.
- **Evidence:** Lines 40-41 call `deptList.clear()` and `finalUtil.clear()`, making this method stateful and non-idempotent. Line 49 calls `this.week.equals(week)` -- if `this.week` is null, a NullPointerException will be thrown. Line 60-61 builds a comma-delimited string using `Arrays.toString(...).replace("[","").replace("]","")` which is fragile.
- **Recommendation:** Write unit tests covering: (1) normal case with matching week/model, (2) case where `this.week` is null, (3) empty `deptDataList`, (4) multiple departments with same model, (5) data arrays containing edge-case doubles (NaN, Infinity, negative zero). Also test that calling `arrangeData` twice does not accumulate stale state.

---

### A01-3 -- DailyUsageHourBean.getModelList() has untested data extraction logic
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java`:27
- **Severity:** HIGH
- **Category:** Test Coverage > Business Logic
- **Description:** `getModelList()` (lines 27-36) iterates `deptDataList` to extract unique model names. This is a getter with side effects -- it modifies `modelList` on every call. Repeated calls will not re-add duplicates (due to `contains()` check) but the behavior is confusing and could mask bugs in callers.
- **Evidence:** Line 28-33: iterates `deptDataList`, creates a new `DailyUsageDeptDataBean` then immediately overwrites it with `deptDataList.get(i)`, adding model names not already in `modelList`. The unnecessary `new DailyUsageDeptDataBean()` on line 29 wastes an allocation every iteration.
- **Recommendation:** Write tests for: (1) empty `deptDataList` returns empty list, (2) single entry returns one model, (3) duplicate model names are deduplicated, (4) calling `getModelList()` multiple times yields the same result (idempotency verification).

---

### A01-4 -- DailyUsageHourBean.getWeekList() has untested filtering logic
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java`:101
- **Severity:** HIGH
- **Category:** Test Coverage > Business Logic
- **Description:** `getWeekList(String model)` (lines 101-111) builds a comma-delimited week info string and filters by model name. Like `getModelList()`, it has a getter-with-side-effects anti-pattern. The deduplication relies on `weekList.contains()` which compares the full comma-delimited string.
- **Evidence:** Line 105 builds `w = usageBean.getWeek() + "," + usageBean.getWeekInt() + "," + usageBean.getwFrom() + "," + usageBean.getwTo()`. Line 106 uses `equalsIgnoreCase` for model comparison but exact equality for week dedup.
- **Recommendation:** Test with: (1) multiple weeks for same model, (2) same week for different models (ensure filtering works), (3) case sensitivity on model name matching, (4) repeated calls do not duplicate entries.

---

### A01-5 -- DetailedReportUtil.analyzeAndCombine() has incomplete/no-op business logic with no tests
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java`:44
- **Severity:** MEDIUM
- **Category:** Test Coverage > Report Generation
- **Description:** `analyzeAndCombine()` (lines 44-53) iterates `vrpt_field_nm` and checks for "Hydraulic", "HYDR", or "HYDL" strings, but the conditional block body is completely empty (lines 49-51). This is either dead code or an incomplete implementation. Without tests, there is no way to verify whether this method is intended to have behavior or is a stub awaiting implementation.
- **Evidence:** Lines 48-51: `if(fldName.contains("Hydraulic") || fldName.contains("HYDR") || fldName.contains("HYDL")) { }` -- empty block, no operation performed.
- **Recommendation:** Write tests that: (1) verify the method does not throw on empty lists, (2) verify the method does not throw with matching field names, (3) document expected behavior. Also investigate whether this is dead code or an unfinished feature, and either complete the implementation or remove it.

---

### A01-6 -- DetailedReportUtil constructor outputs debug information to System.out with no tests
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java`:34
- **Severity:** MEDIUM
- **Category:** Test Coverage > Report Generation
- **Description:** The parameterized constructor (lines 34-42) writes debug output via `System.out.println` that exposes internal data sizes (`vrpt_field_cd`, `vrpt_field_nm`, `vrpt_veh_value_stop` sizes). This debug output could leak information in production and pollutes logs.
- **Evidence:** Lines 39-41: `System.out.println("vrpt_field_cd: " + vrpt_field_cd.size())`, `System.out.println("vrpt_field_nm: " + vrpt_field_nm.size())`, `System.out.println("vrpt_veh_value_stop: " + vrpt_veh_value_stop.size())`.
- **Recommendation:** Write tests that verify construction with various ArrayList sizes. A test would also document the undesirable `System.out.println` side effects, marking them for removal. Test with null ArrayLists to verify NullPointerException handling.

---

### A01-7 -- CustomerBean holds password policy flag with no tests
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/CustomerBean.java`:6
- **Severity:** HIGH
- **Category:** Test Coverage > Security-Adjacent Data
- **Description:** `CustomerBean` holds a `passwordPolicy` boolean field (line 6) and an `active` boolean field (line 7). These fields are security-adjacent: `passwordPolicy` likely governs whether password complexity rules are enforced for a customer, and `active` likely controls whether the customer account is enabled. While the bean itself is just a data holder, the fact that these security-relevant flags are carried in an untested bean means there is no validation of serialization/deserialization correctness, no verification that default values are safe, and no documentation of expected states.
- **Evidence:** Fields `passwordPolicy` (line 6) and `active` (line 7) are primitive booleans defaulting to `false`. If `passwordPolicy` defaults to `false`, password policy enforcement may be silently disabled for new CustomerBean instances.
- **Recommendation:** Write tests verifying: (1) default values of `passwordPolicy` and `active` are as expected (both default to `false`), (2) setters/getters round-trip correctly, (3) document whether `false` default for `passwordPolicy` is intentional and safe.

---

### A01-8 -- CanruleBean carries access control fields with no tests
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/CanruleBean.java`:14
- **Severity:** HIGH
- **Category:** Test Coverage > Access Control Data
- **Description:** `CanruleBean` carries four access control fields: `access_level` (line 14), `access_cust` (line 15), `access_site` (line 16), and `access_dept` (line 17). These fields appear to govern what level of access a CAN rule configuration has across the customer/site/department hierarchy. Incorrect handling of these values could lead to authorization bypass.
- **Evidence:** All four access fields default to `null`. If consuming code does not properly handle `null` access levels, it could result in either overly permissive or overly restrictive access. The bean does not implement `Serializable`, so session replication issues may also arise.
- **Recommendation:** Write tests verifying: (1) all access fields default to null, (2) setter/getter round-trips work correctly, (3) integration tests should verify that downstream consumers properly handle null access fields.

---

### A01-9 -- DriverImportBean carries access control and license denial fields with no tests
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DriverImportBean.java`:26
- **Severity:** HIGH
- **Category:** Test Coverage > Access Control Data / Driver Safety
- **Description:** `DriverImportBean` carries access control fields (`access_level`, `access_cust`, `access_site`, `access_dept` at lines 26-29) and a safety-critical `denyOnExp` boolean (line 31) that likely controls whether a driver is denied access when their license expires. The `licenseType` (line 30) and `expirydt` (line 14) fields also relate to driver safety compliance. An incorrect default for `denyOnExp` (currently `false`) could mean expired-license drivers are not denied by default.
- **Evidence:** Line 31: `private boolean denyOnExp = false;` -- drivers are NOT denied on license expiry by default. Lines 26-29: access control fields default to `null`. Line 14: `expirydt` is stored as a String with no format validation in the bean.
- **Recommendation:** Write tests verifying: (1) `denyOnExp` defaults to `false` and document whether this is the safe default, (2) all access fields default to null, (3) serialization with `serialVersionUID` is stable, (4) all 24 fields round-trip correctly through getters/setters. Integration tests should verify that `denyOnExp=false` does not create a safety gap.

---

### A01-10 -- BatteryBean data transfer object for battery swap tracking has no tests
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/BatteryBean.java`:5
- **Severity:** LOW
- **Category:** Test Coverage > Data Transfer Object
- **Description:** `BatteryBean` is a pure getter/setter bean with 22 fields tracking battery swap events (before/after states for battery ID, vehicle name, driver name, state of charge, hour meter, timestamps). While it has no business logic, incorrect serialization (it implements `Serializable`) or field mapping could cause battery tracking data loss in a fleet management context.
- **Evidence:** All String fields default to `""` (empty string), boolean `isTruck1120` defaults to `false`. The `serialVersionUID` (line 10) is explicitly set, so serialization compatibility is intentional.
- **Recommendation:** Write basic tests verifying: (1) default field values, (2) getter/setter round-trips for all 22 fields, (3) serialization/deserialization round-trip preserves all data.

---

### A01-11 -- BroadcastmsgBean for message dispatch has no tests
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/BroadcastmsgBean.java`:5
- **Severity:** LOW
- **Category:** Test Coverage > Data Transfer Object
- **Description:** `BroadcastmsgBean` is a Serializable DTO carrying broadcast message data including text, type, timestamps (dispatch, response, sent), driver, unit, and vehicle ID. It is a pure getter/setter bean with no logic.
- **Evidence:** 10 String fields, all with implicit null defaults. Implements `Serializable` with explicit `serialVersionUID`.
- **Recommendation:** Write basic getter/setter and serialization round-trip tests.

---

### A01-12 -- CustLocDeptBean for customer/location/department mapping has no tests
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/CustLocDeptBean.java`:3
- **Severity:** LOW
- **Category:** Test Coverage > Data Transfer Object
- **Description:** `CustLocDeptBean` is a minimal 3-field bean (custCd, locCd, deptCd as ints) used for customer-location-department hierarchy mapping. Pure getter/setter with no logic. Does NOT implement `Serializable`.
- **Evidence:** 3 int fields with default value of 0. No `Serializable` implementation.
- **Recommendation:** Write basic getter/setter tests. Consider whether `Serializable` should be added for consistency with other beans.

---

### A01-13 -- DailyUsageDeptDataBean for usage reporting has no tests
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageDeptDataBean.java`:6
- **Severity:** LOW
- **Category:** Test Coverage > Data Transfer Object
- **Description:** `DailyUsageDeptDataBean` is a Serializable DTO with 10 fields used for daily usage department data reporting. It has a parameterized constructor but no business logic beyond getters/setters. The `data` field (`ArrayList<double[]>`) stores numerical data arrays that feed into `DailyUsageHourBean`'s complex logic.
- **Evidence:** Two constructors (no-arg and 4-arg at line 23). The `data` field holds `ArrayList<double[]>` which is mutable and could be externally modified after construction.
- **Recommendation:** Write tests for: (1) parameterized constructor sets all 4 fields correctly, (2) getter/setter round-trips, (3) verify that the `data` ArrayList's mutability is understood (defensive copies may be needed).

---

### A01-14 -- DashboarSubscriptionBean carries user/email subscription data with no tests
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DashboarSubscriptionBean.java`:3
- **Severity:** LOW
- **Category:** Test Coverage > Data Transfer Object
- **Description:** `DashboarSubscriptionBean` (note: typo in class name "Dashboar" vs "Dashboard") carries subscription data including `userCd`, `custCd`, `emailId`, and location info. It is a pure getter/setter bean. The `emailId` field stores user email addresses which are PII.
- **Evidence:** 6 fields. Class name contains a typo. Does NOT implement `Serializable`. `emailId` field (line 10) stores PII with no validation.
- **Recommendation:** Write getter/setter tests. Consider adding `Serializable`. Document the class name typo for potential future correction.

---

### A01-15 -- DayhoursBean for work hour tracking has no tests
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DayhoursBean.java`:5
- **Severity:** LOW
- **Category:** Test Coverage > Data Transfer Object
- **Description:** `DayhoursBean` is a Serializable DTO with 7 fields tracking work hours (total hours/mins, break hours/mins, days, available hours). Pure getter/setter bean. The `avail_hours` field has a formatted default of "00:00:00".
- **Evidence:** Fields have explicit defaults: ints default to 0, `avail_hours` defaults to "00:00:00". Implements `Serializable`.
- **Recommendation:** Write basic getter/setter and serialization tests. Verify `avail_hours` format consistency.

---

### A01-16 -- DehireBean for vehicle dehire timestamp tracking has no tests
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DehireBean.java`:5
- **Severity:** LOW
- **Category:** Test Coverage > Data Transfer Object
- **Description:** `DehireBean` is a minimal 3-field bean with `vehCd` (int) and two `java.sql.Timestamp` fields (`hire_time`, `dehire_time`). Pure getter/setter with no logic. Does NOT implement `Serializable`.
- **Evidence:** Uses `java.sql.Timestamp` directly, coupling the bean to JDBC types. Does not implement `Serializable`.
- **Recommendation:** Write basic getter/setter tests. Consider whether `Serializable` should be added.

---

### A01-17 -- DriverBean for driver identification has no tests
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DriverBean.java`:5
- **Severity:** LOW
- **Category:** Test Coverage > Data Transfer Object
- **Description:** `DriverBean` is a Serializable DTO with 4 fields (`id`, `user_cd`, `weigand`, `veh_type`). The `weigand` field likely refers to a Wiegand access card number, which is a physical access control credential. Pure getter/setter bean.
- **Evidence:** `weigand` field (line 8) stores what appears to be a Wiegand card number -- an access control credential. All fields default to empty string.
- **Recommendation:** Write getter/setter and serialization tests. Note that `weigand` stores a credential-adjacent value and should be handled carefully in logging/display.

---

### A01-18 -- DriverLeagueBean for driver performance metrics has no tests
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DriverLeagueBean.java`:3
- **Severity:** LOW
- **Category:** Test Coverage > Data Transfer Object
- **Description:** `DriverLeagueBean` carries driver league/performance data with 9 fields including `redImpact`, `preOp`, `keyHour`, `tracHours`, and `percActive`. Pure getter/setter bean. Does NOT implement `Serializable`.
- **Evidence:** Performance-related fields stored as Strings rather than numeric types, which could cause sorting/comparison issues in consumers.
- **Recommendation:** Write basic getter/setter tests.

---

## Summary

| # | File | Severity | Category |
|---|------|----------|----------|
| A01-1 | (repo-wide) | CRITICAL | No test infrastructure |
| A01-2 | DailyUsageHourBean.java:39 | HIGH | Business logic -- arrangeData() |
| A01-3 | DailyUsageHourBean.java:27 | HIGH | Business logic -- getModelList() |
| A01-4 | DailyUsageHourBean.java:101 | HIGH | Business logic -- getWeekList() |
| A01-5 | DetailedReportUtil.java:44 | MEDIUM | Report generation -- empty analyzeAndCombine() |
| A01-6 | DetailedReportUtil.java:34 | MEDIUM | Report generation -- debug output in constructor |
| A01-7 | CustomerBean.java:6 | HIGH | Security-adjacent data -- passwordPolicy flag |
| A01-8 | CanruleBean.java:14 | HIGH | Access control data -- access level fields |
| A01-9 | DriverImportBean.java:26 | HIGH | Access control / driver safety -- denyOnExp + access fields |
| A01-10 | BatteryBean.java:5 | LOW | DTO -- battery swap tracking |
| A01-11 | BroadcastmsgBean.java:5 | LOW | DTO -- message dispatch |
| A01-12 | CustLocDeptBean.java:3 | LOW | DTO -- customer/location/dept mapping |
| A01-13 | DailyUsageDeptDataBean.java:6 | LOW | DTO -- usage department data |
| A01-14 | DashboarSubscriptionBean.java:3 | LOW | DTO -- subscription data with PII |
| A01-15 | DayhoursBean.java:5 | LOW | DTO -- work hours tracking |
| A01-16 | DehireBean.java:5 | LOW | DTO -- vehicle dehire timestamps |
| A01-17 | DriverBean.java:5 | LOW | DTO -- driver identification |
| A01-18 | DriverLeagueBean.java:3 | LOW | DTO -- driver performance metrics |

**Totals:** 1 CRITICAL, 6 HIGH, 2 MEDIUM, 9 LOW

### Priority Recommendations

1. **Immediate (CRITICAL):** Establish JUnit 5 test infrastructure with Maven/Gradle build integration.
2. **High Priority:** Write unit tests for `DailyUsageHourBean` (3 methods with business logic), `CustomerBean` (security-adjacent defaults), `CanruleBean` (access control fields), and `DriverImportBean` (access control + safety-critical `denyOnExp` flag).
3. **Medium Priority:** Write tests for `DetailedReportUtil` to document the empty `analyzeAndCombine()` method and debug output behavior.
4. **Lower Priority:** Write basic getter/setter and serialization round-trip tests for all remaining DTO beans to establish baseline regression protection.
