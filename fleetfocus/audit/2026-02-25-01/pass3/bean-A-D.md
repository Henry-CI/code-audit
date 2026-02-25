# Pass 3 -- Documentation: bean package (A-D)
**Agent:** A01
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

---

## Reading Evidence

### BatteryBean.java
- **Class:** `com.torrent.surat.fms6.bean.BatteryBean` (implements Serializable)
- **Class Javadoc:** Absent -- no class-level Javadoc comment (only an empty serialVersionUID Javadoc block at line 7-9)
- **Fields (package-private):** `batteryId`, `unit_nm`, `unit_serial`, `unit_cd`, `charge_tm`, `bef_bat_id`, `bef_veh_nm`, `bef_dri_nm`, `bef_soc`, `bef_hm`, `bef_tm`, `aft_bat_id`, `aft_veh_nm`, `aft_dri_nm`, `aft_soc`, `aft_hm`, `aft_tm`, `duration`, `isTruck1120`, `bef_bat_fleet_num`, `aft_bat_fleet_num`, `bat_fleet_num`
- **Constants:** `serialVersionUID` (line 10)
- **Public methods:**
  - `getUnit_serial()` (line 35) -- Javadoc: Absent
  - `setUnit_serial(String)` (line 38) -- Javadoc: Absent
  - `getBatteryId()` (line 41) -- Javadoc: Absent
  - `setBatteryId(String)` (line 44) -- Javadoc: Absent
  - `getCharge_tm()` (line 47) -- Javadoc: Absent
  - `setCharge_tm(String)` (line 50) -- Javadoc: Absent
  - `getBef_veh_nm()` (line 53) -- Javadoc: Absent
  - `setBef_veh_nm(String)` (line 56) -- Javadoc: Absent
  - `getBef_dri_nm()` (line 59) -- Javadoc: Absent
  - `setBef_dri_nm(String)` (line 62) -- Javadoc: Absent
  - `getBef_soc()` (line 65) -- Javadoc: Absent
  - `setBef_soc(String)` (line 68) -- Javadoc: Absent
  - `getBef_hm()` (line 71) -- Javadoc: Absent
  - `setBef_hm(String)` (line 74) -- Javadoc: Absent
  - `getAft_veh_nm()` (line 77) -- Javadoc: Absent
  - `setAft_veh_nm(String)` (line 80) -- Javadoc: Absent
  - `getAft_dri_nm()` (line 83) -- Javadoc: Absent
  - `setAft_dri_nm(String)` (line 86) -- Javadoc: Absent
  - `getAft_soc()` (line 89) -- Javadoc: Absent
  - `setAft_soc(String)` (line 92) -- Javadoc: Absent
  - `getAft_hm()` (line 95) -- Javadoc: Absent
  - `setAft_hm(String)` (line 98) -- Javadoc: Absent
  - `getUnit_nm()` (line 101) -- Javadoc: Absent
  - `setUnit_nm(String)` (line 104) -- Javadoc: Absent
  - `getBef_tm()` (line 107) -- Javadoc: Absent
  - `setBef_tm(String)` (line 110) -- Javadoc: Absent
  - `getAft_tm()` (line 113) -- Javadoc: Absent
  - `setAft_tm(String)` (line 116) -- Javadoc: Absent
  - `getBef_bat_id()` (line 119) -- Javadoc: Absent
  - `setBef_bat_id(String)` (line 122) -- Javadoc: Absent
  - `getAft_bat_id()` (line 125) -- Javadoc: Absent
  - `setAft_bat_id(String)` (line 128) -- Javadoc: Absent
  - `getUnit_cd()` (line 131) -- Javadoc: Absent
  - `setUnit_cd(String)` (line 134) -- Javadoc: Absent
  - `getDuration()` (line 137) -- Javadoc: Absent
  - `setDuration(String)` (line 140) -- Javadoc: Absent
  - `isTruck1120()` (line 143) -- Javadoc: Absent
  - `setTruck1120(boolean)` (line 146) -- Javadoc: Absent
  - `getBef_bat_fleet_num()` (line 149) -- Javadoc: Absent
  - `setBef_bat_fleet_num(String)` (line 152) -- Javadoc: Absent
  - `getAft_bat_fleet_num()` (line 155) -- Javadoc: Absent
  - `setAft_bat_fleet_num(String)` (line 158) -- Javadoc: Absent
  - `getBat_fleet_num()` (line 161) -- Javadoc: Absent
  - `setBat_fleet_num(String)` (line 164) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

---

### BroadcastmsgBean.java
- **Class:** `com.torrent.surat.fms6.bean.BroadcastmsgBean` (implements Serializable)
- **Class Javadoc:** Absent -- no class-level Javadoc comment (only an empty serialVersionUID Javadoc block at line 7-9)
- **Fields (private):** `text`, `type`, `disp_timestamp`, `resp_timestamp`, `response`, `driver`, `unit`, `product_type`, `sent_timestamp`, `veh_id`
- **Constants:** `serialVersionUID` (line 10)
- **Public methods:**
  - `getSent_timestamp()` (line 23) -- Javadoc: Absent
  - `setSent_timestamp(String)` (line 26) -- Javadoc: Absent
  - `getText()` (line 29) -- Javadoc: Absent
  - `getType()` (line 32) -- Javadoc: Absent
  - `getDisp_timestamp()` (line 35) -- Javadoc: Absent
  - `getResp_timestamp()` (line 38) -- Javadoc: Absent
  - `getResponse()` (line 41) -- Javadoc: Absent
  - `getDriver()` (line 44) -- Javadoc: Absent
  - `getUnit()` (line 47) -- Javadoc: Absent
  - `setText(String)` (line 50) -- Javadoc: Absent
  - `setType(String)` (line 53) -- Javadoc: Absent
  - `setDisp_timestamp(String)` (line 56) -- Javadoc: Absent
  - `setResp_timestamp(String)` (line 59) -- Javadoc: Absent
  - `setResponse(String)` (line 62) -- Javadoc: Absent
  - `setDriver(String)` (line 65) -- Javadoc: Absent
  - `setUnit(String)` (line 68) -- Javadoc: Absent
  - `getProduct_type()` (line 71) -- Javadoc: Absent
  - `setProduct_type(String)` (line 74) -- Javadoc: Absent
  - `getVeh_id()` (line 77) -- Javadoc: Absent
  - `setVeh_id(String)` (line 80) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

---

### CanruleBean.java
- **Class:** `com.torrent.surat.fms6.bean.CanruleBean` (does NOT implement Serializable)
- **Class Javadoc:** Absent
- **Fields (private):** `src_holder`, `site_name`, `department_name`, `model_name`, `gmtp_id`, `serial_no`, `hire_no`, `canrule_name`, `custCd`, `access_level`, `access_cust`, `access_site`, `access_dept`
- **Public methods:**
  - `getSrc_holder()` (line 19) -- Javadoc: Absent
  - `setSrc_holder(String)` (line 22) -- Javadoc: Absent
  - `getSite_name()` (line 25) -- Javadoc: Absent
  - `setSite_name(String)` (line 28) -- Javadoc: Absent
  - `getDepartment_name()` (line 31) -- Javadoc: Absent
  - `setDepartment_name(String)` (line 34) -- Javadoc: Absent
  - `getModel_name()` (line 37) -- Javadoc: Absent
  - `setModel_name(String)` (line 40) -- Javadoc: Absent
  - `getGmtp_id()` (line 43) -- Javadoc: Absent
  - `setGmtp_id(String)` (line 46) -- Javadoc: Absent
  - `getSerial_no()` (line 49) -- Javadoc: Absent
  - `setSerial_no(String)` (line 52) -- Javadoc: Absent
  - `getHire_no()` (line 55) -- Javadoc: Absent
  - `setHire_no(String)` (line 58) -- Javadoc: Absent
  - `getCanrule_name()` (line 61) -- Javadoc: Absent
  - `setCanrule_name(String)` (line 64) -- Javadoc: Absent
  - `getCustCd()` (line 67) -- Javadoc: Absent
  - `setCustCd(String)` (line 70) -- Javadoc: Absent
  - `getAccess_level()` (line 73) -- Javadoc: Absent
  - `setAccess_level(String)` (line 76) -- Javadoc: Absent
  - `getAccess_cust()` (line 79) -- Javadoc: Absent
  - `setAccess_cust(String)` (line 82) -- Javadoc: Absent
  - `getAccess_site()` (line 85) -- Javadoc: Absent
  - `setAccess_site(String)` (line 88) -- Javadoc: Absent
  - `getAccess_dept()` (line 91) -- Javadoc: Absent
  - `setAccess_dept(String)` (line 94) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

---

### CustLocDeptBean.java
- **Class:** `com.torrent.surat.fms6.bean.CustLocDeptBean` (does NOT implement Serializable)
- **Class Javadoc:** Absent
- **Fields (package-private):** `custCd` (int), `locCd` (int), `deptCd` (int)
- **Public methods:**
  - `getCustCd()` (line 6) -- Javadoc: Absent
  - `setCustCd(int)` (line 10) -- Javadoc: Absent
  - `getLocCd()` (line 14) -- Javadoc: Absent
  - `setLocCd(int)` (line 18) -- Javadoc: Absent
  - `getDeptCd()` (line 22) -- Javadoc: Absent
  - `setDeptCd(int)` (line 26) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

---

### CustomerBean.java
- **Class:** `com.torrent.surat.fms6.bean.CustomerBean` (does NOT implement Serializable)
- **Class Javadoc:** Absent
- **Fields (package-private):** `id` (int), `passwordPolicy` (boolean), `active` (boolean)
- **Public methods:**
  - `isActive()` (line 9) -- Javadoc: Absent
  - `setActive(boolean)` (line 12) -- Javadoc: Absent
  - `getId()` (line 15) -- Javadoc: Absent
  - `isPasswordPolicy()` (line 18) -- Javadoc: Absent
  - `setId(int)` (line 21) -- Javadoc: Absent
  - `setPasswordPolicy(boolean)` (line 24) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

---

### DailyUsageDeptDataBean.java
- **Class:** `com.torrent.surat.fms6.bean.DailyUsageDeptDataBean` (implements Serializable)
- **Class Javadoc:** Absent
- **Fields (private):** `dept_id`, `dept_name`, `modelName`, `data` (ArrayList<double[]>), `loc`, `week`, `wFrom`, `wTo`, `weekInt` (int), `unitTotal` (int)
- **Public methods:**
  - `DailyUsageDeptDataBean()` constructor (line 19) -- Javadoc: Absent
  - `DailyUsageDeptDataBean(String, String, String, ArrayList<double[]>)` constructor (line 23) -- Javadoc: Absent
  - `getDept_id()` (line 31) -- Javadoc: Absent
  - `setDept_id(String)` (line 35) -- Javadoc: Absent
  - `getDept_name()` (line 39) -- Javadoc: Absent
  - `setDept_name(String)` (line 43) -- Javadoc: Absent
  - `getModelName()` (line 47) -- Javadoc: Absent
  - `setModelName(String)` (line 51) -- Javadoc: Absent
  - `getData()` (line 55) -- Javadoc: Absent
  - `setData(ArrayList<double[]>)` (line 59) -- Javadoc: Absent
  - `getLoc()` (line 63) -- Javadoc: Absent
  - `setLoc(String)` (line 67) -- Javadoc: Absent
  - `getWeek()` (line 71) -- Javadoc: Absent
  - `setWeek(String)` (line 75) -- Javadoc: Absent
  - `getwFrom()` (line 79) -- Javadoc: Absent
  - `setwFrom(String)` (line 83) -- Javadoc: Absent
  - `getwTo()` (line 87) -- Javadoc: Absent
  - `setwTo(String)` (line 91) -- Javadoc: Absent
  - `getWeekInt()` (line 95) -- Javadoc: Absent
  - `setWeekInt(int)` (line 99) -- Javadoc: Absent
  - `getUnitTotal()` (line 103) -- Javadoc: Absent
  - `setUnitTotal(int)` (line 107) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

---

### DailyUsageHourBean.java
- **Class:** `com.torrent.surat.fms6.bean.DailyUsageHourBean` (implements Serializable)
- **Class Javadoc:** Absent
- **Fields (private):** `ifCombine` (boolean), `deptList` (ArrayList<String>), `modelList` (ArrayList<String>), `deptDataList` (ArrayList<DailyUsageDeptDataBean>), `finalUtil` (ArrayList<String>), `weekList` (ArrayList<String>), `week` (String)
- **Public methods:**
  - `DailyUsageHourBean()` constructor (line 18) -- Javadoc: Absent
  - `DailyUsageHourBean(boolean, ArrayList<DailyUsageDeptDataBean>)` constructor (line 22) -- Javadoc: Absent
  - `getModelList()` (line 27) -- Javadoc: Absent -- **NOTE: contains business logic, not a simple getter**
  - `arrangeData(String modelName)` (line 39) -- Javadoc: Absent -- **NOTE: complex business logic method**
  - `isIfCombine()` (line 69) -- Javadoc: Absent
  - `setIfCombine(boolean)` (line 73) -- Javadoc: Absent
  - `getDeptList()` (line 77) -- Javadoc: Absent
  - `setDeptList(ArrayList<String>)` (line 81) -- Javadoc: Absent
  - `getDeptDataList()` (line 85) -- Javadoc: Absent
  - `setDeptDataList(ArrayList<DailyUsageDeptDataBean>)` (line 89) -- Javadoc: Absent
  - `getFinalUtil()` (line 93) -- Javadoc: Absent
  - `setFinalUtil(ArrayList<String>)` (line 97) -- Javadoc: Absent
  - `getWeekList(String model)` (line 101) -- Javadoc: Absent -- **NOTE: contains business logic, not a simple getter**
  - `setWeekList(ArrayList<String>)` (line 113) -- Javadoc: Absent
  - `setModelList(ArrayList<String>)` (line 117) -- Javadoc: Absent
  - `setWeek(String)` (line 121) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None
- **Commented-out debug code:** Lines 57-59 contain commented-out `System.out.println` debug statements

---

### DashboarSubscriptionBean.java
- **Class:** `com.torrent.surat.fms6.bean.DashboarSubscriptionBean` (does NOT implement Serializable)
- **Class Javadoc:** Absent
- **Note:** Class name contains a typo -- "Dashboar" instead of "Dashboard"
- **Fields (private):** `id` (int), `userCd` (int), `custCd` (int), `locCd` (String), `location` (String), `emailId` (String)
- **Public methods:**
  - `getId()` (line 11) -- Javadoc: Absent
  - `getUserCd()` (line 14) -- Javadoc: Absent
  - `getCustCd()` (line 17) -- Javadoc: Absent
  - `getLocCd()` (line 20) -- Javadoc: Absent
  - `getLocation()` (line 23) -- Javadoc: Absent
  - `getEmailId()` (line 26) -- Javadoc: Absent
  - `setId(int)` (line 29) -- Javadoc: Absent
  - `setUserCd(int)` (line 32) -- Javadoc: Absent
  - `setCustCd(int)` (line 35) -- Javadoc: Absent
  - `setLocCd(String)` (line 38) -- Javadoc: Absent
  - `setLocation(String)` (line 41) -- Javadoc: Absent
  - `setEmailId(String)` (line 44) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

---

### DayhoursBean.java
- **Class:** `com.torrent.surat.fms6.bean.DayhoursBean` (implements Serializable)
- **Class Javadoc:** Absent -- no class-level Javadoc comment (only an empty serialVersionUID Javadoc block at line 7-9)
- **Fields (package-private):** `id` (String), `total_hours` (int), `total_mins` (int), `break_hours` (int), `break_mins` (int), `days` (int), `avail_hours` (String, default "00:00:00")
- **Constants:** `serialVersionUID` (line 10)
- **Public methods:**
  - `getId()` (line 20) -- Javadoc: Absent
  - `setId(String)` (line 23) -- Javadoc: Absent
  - `getTotal_hours()` (line 26) -- Javadoc: Absent
  - `setTotal_hours(int)` (line 29) -- Javadoc: Absent
  - `getTotal_mins()` (line 32) -- Javadoc: Absent
  - `setTotal_mins(int)` (line 35) -- Javadoc: Absent
  - `getBreak_hours()` (line 38) -- Javadoc: Absent
  - `setBreak_hours(int)` (line 41) -- Javadoc: Absent
  - `getBreak_mins()` (line 44) -- Javadoc: Absent
  - `setBreak_mins(int)` (line 47) -- Javadoc: Absent
  - `getDays()` (line 50) -- Javadoc: Absent
  - `setDays(int)` (line 53) -- Javadoc: Absent
  - `getAvail_hours()` (line 56) -- Javadoc: Absent
  - `setAvail_hours(String)` (line 59) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

---

### DehireBean.java
- **Class:** `com.torrent.surat.fms6.bean.DehireBean` (does NOT implement Serializable)
- **Class Javadoc:** Absent
- **Fields (private):** `vehCd` (int), `hire_time` (Timestamp), `dehire_time` (Timestamp)
- **Public methods:**
  - `getVehCd()` (line 10) -- Javadoc: Absent
  - `setVehCd(int)` (line 13) -- Javadoc: Absent
  - `getHire_time()` (line 16) -- Javadoc: Absent
  - `setHire_time(Timestamp)` (line 19) -- Javadoc: Absent
  - `getDehire_time()` (line 22) -- Javadoc: Absent
  - `setDehire_time(Timestamp)` (line 25) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

---

### DetailedReportUtil.java
- **Class:** `com.torrent.surat.fms6.bean.DetailedReportUtil` (does NOT implement Serializable)
- **Class Javadoc:** Absent
- **Fields (package-private, all raw ArrayList without generics):** `vrpt_field_cd`, `vrpt_field_nm`, `vrpt_veh_typ_cd`, `vrpt_veh_typ`, `vrpt_veh_cd`, `vrpt_veh_nm`, `vrpt_veh_id`, `vrpt_veh_value_start`, `vrpt_veh_value_stop`, `vrpt_veh_value_state`, `vrpt_veh_value_stopv`, `vrpt_veh_driv_cd`, `vrpt_veh_driv_nm`, `vrpt_veh_driv_tm`, `vrpt_veh_sttm`, `vrpt_veh_endtm`, `vrpt_veh_tot`, `vrpt_veh_gtot`, `newFieldCdList`, `newFieldNameList`
- **Public methods:**
  - `DetailedReportUtil()` constructor (line 30) -- Javadoc: Absent
  - `DetailedReportUtil(ArrayList, ArrayList, ArrayList)` constructor (line 34) -- Javadoc: Absent -- **NOTE: prints to stdout in constructor**
  - `analyzeAndCombine()` (line 44) -- Javadoc: Absent -- **NOTE: contains business logic but method body is effectively empty (no-op); loop iterates but the if-block has no body**
  - `getVrpt_field_cd()` (line 57) -- Javadoc: Absent
  - `setVrpt_field_cd(ArrayList)` (line 60) -- Javadoc: Absent
  - `getVrpt_field_nm()` (line 63) -- Javadoc: Absent
  - `setVrpt_field_nm(ArrayList)` (line 66) -- Javadoc: Absent
  - `getVrpt_veh_typ_cd()` (line 69) -- Javadoc: Absent
  - `setVrpt_veh_typ_cd(ArrayList)` (line 72) -- Javadoc: Absent
  - `getVrpt_veh_typ()` (line 75) -- Javadoc: Absent
  - `setVrpt_veh_typ(ArrayList)` (line 78) -- Javadoc: Absent
  - `getVrpt_veh_cd()` (line 81) -- Javadoc: Absent
  - `setVrpt_veh_cd(ArrayList)` (line 84) -- Javadoc: Absent
  - `getVrpt_veh_nm()` (line 87) -- Javadoc: Absent
  - `setVrpt_veh_nm(ArrayList)` (line 90) -- Javadoc: Absent
  - `getVrpt_veh_id()` (line 93) -- Javadoc: Absent
  - `setVrpt_veh_id(ArrayList)` (line 96) -- Javadoc: Absent
  - `getVrpt_veh_value_start()` (line 99) -- Javadoc: Absent
  - `setVrpt_veh_value_start(ArrayList)` (line 102) -- Javadoc: Absent
  - `getVrpt_veh_value_stop()` (line 105) -- Javadoc: Absent
  - `setVrpt_veh_value_stop(ArrayList)` (line 108) -- Javadoc: Absent
  - `getVrpt_veh_value_state()` (line 111) -- Javadoc: Absent
  - `setVrpt_veh_value_state(ArrayList)` (line 114) -- Javadoc: Absent
  - `getVrpt_veh_value_stopv()` (line 117) -- Javadoc: Absent
  - `setVrpt_veh_value_stopv(ArrayList)` (line 120) -- Javadoc: Absent
  - `getVrpt_veh_driv_cd()` (line 123) -- Javadoc: Absent
  - `setVrpt_veh_driv_cd(ArrayList)` (line 126) -- Javadoc: Absent
  - `getVrpt_veh_driv_nm()` (line 129) -- Javadoc: Absent
  - `setVrpt_veh_driv_nm(ArrayList)` (line 132) -- Javadoc: Absent
  - `getVrpt_veh_driv_tm()` (line 135) -- Javadoc: Absent
  - `setVrpt_veh_driv_tm(ArrayList)` (line 138) -- Javadoc: Absent
  - `getVrpt_veh_sttm()` (line 141) -- Javadoc: Absent
  - `setVrpt_veh_sttm(ArrayList)` (line 144) -- Javadoc: Absent
  - `getVrpt_veh_endtm()` (line 147) -- Javadoc: Absent
  - `setVrpt_veh_endtm(ArrayList)` (line 150) -- Javadoc: Absent
  - `getVrpt_veh_tot()` (line 153) -- Javadoc: Absent
  - `setVrpt_veh_tot(ArrayList)` (line 156) -- Javadoc: Absent
  - `getVrpt_veh_gtot()` (line 159) -- Javadoc: Absent
  - `setVrpt_veh_gtot(ArrayList)` (line 162) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None
- **Debug statements:** Constructor at line 34 contains `System.out.println` debug output (lines 39-41)

---

### DriverBean.java
- **Class:** `com.torrent.surat.fms6.bean.DriverBean` (implements Serializable)
- **Class Javadoc:** Absent
- **Fields (package-private):** `id` (String), `user_cd` (String), `weigand` (String), `veh_type` (String)
- **Public methods:**
  - `getUser_cd()` (line 12) -- Javadoc: Absent
  - `setUser_cd(String)` (line 15) -- Javadoc: Absent
  - `getId()` (line 18) -- Javadoc: Absent
  - `setId(String)` (line 21) -- Javadoc: Absent
  - `getWeigand()` (line 24) -- Javadoc: Absent
  - `setWeigand(String)` (line 27) -- Javadoc: Absent
  - `getVeh_type()` (line 30) -- Javadoc: Absent
  - `setVeh_type(String)` (line 33) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

---

### DriverImportBean.java
- **Class:** `com.torrent.surat.fms6.bean.DriverImportBean` (implements Serializable)
- **Class Javadoc:** Absent
- **Fields (private):** `id`, `department`, `site`, `first_name`, `last_name`, `licno`, `expirydt`, `phone`, `active`, `location`, `comp_id`, `card_no`, `facility_code`, `key_reader`, `custCd`, `locCd`, `deptCd`, `cardType`, `access_level`, `access_cust`, `access_site`, `access_dept`, `licenseType`, `denyOnExp` (boolean)
- **Constants:** `serialVersionUID` (line 7)
- **Public methods:**
  - `getKey_reader()` (line 33) -- Javadoc: Absent
  - `setKey_reader(String)` (line 36) -- Javadoc: Absent
  - `getFacility_code()` (line 39) -- Javadoc: Absent
  - `setFacility_code(String)` (line 42) -- Javadoc: Absent
  - `getId()` (line 45) -- Javadoc: Absent
  - `setId(String)` (line 48) -- Javadoc: Absent
  - `getLicno()` (line 51) -- Javadoc: Absent
  - `setLicno(String)` (line 54) -- Javadoc: Absent
  - `getPhone()` (line 57) -- Javadoc: Absent
  - `setPhone(String)` (line 60) -- Javadoc: Absent
  - `getActive()` (line 63) -- Javadoc: Absent
  - `setActive(String)` (line 66) -- Javadoc: Absent
  - `getLocation()` (line 69) -- Javadoc: Absent
  - `setLocation(String)` (line 72) -- Javadoc: Absent
  - `getDepartment()` (line 75) -- Javadoc: Absent
  - `setDepartment(String)` (line 78) -- Javadoc: Absent
  - `getSite()` (line 81) -- Javadoc: Absent
  - `setSite(String)` (line 84) -- Javadoc: Absent
  - `getComp_id()` (line 87) -- Javadoc: Absent
  - `setComp_id(String)` (line 90) -- Javadoc: Absent
  - `getFirst_name()` (line 93) -- Javadoc: Absent
  - `setFirst_name(String)` (line 96) -- Javadoc: Absent
  - `getLast_name()` (line 99) -- Javadoc: Absent
  - `setLast_name(String)` (line 102) -- Javadoc: Absent
  - `getExpirydt()` (line 105) -- Javadoc: Absent
  - `setExpirydt(String)` (line 108) -- Javadoc: Absent
  - `getCard_no()` (line 111) -- Javadoc: Absent
  - `setCard_no(String)` (line 114) -- Javadoc: Absent
  - `getCustCd()` (line 117) -- Javadoc: Absent
  - `setCustCd(String)` (line 120) -- Javadoc: Absent
  - `getLocCd()` (line 123) -- Javadoc: Absent
  - `setLocCd(String)` (line 126) -- Javadoc: Absent
  - `getDeptCd()` (line 129) -- Javadoc: Absent
  - `setDeptCd(String)` (line 132) -- Javadoc: Absent
  - `getCardType()` (line 135) -- Javadoc: Absent
  - `setCardType(String)` (line 138) -- Javadoc: Absent
  - `getAccess_level()` (line 141) -- Javadoc: Absent
  - `setAccess_level(String)` (line 144) -- Javadoc: Absent
  - `getAccess_cust()` (line 147) -- Javadoc: Absent
  - `setAccess_cust(String)` (line 150) -- Javadoc: Absent
  - `getAccess_site()` (line 153) -- Javadoc: Absent
  - `setAccess_site(String)` (line 156) -- Javadoc: Absent
  - `getAccess_dept()` (line 159) -- Javadoc: Absent
  - `setAccess_dept(String)` (line 162) -- Javadoc: Absent
  - `getLicenseType()` (line 165) -- Javadoc: Absent
  - `setLicenseType(String)` (line 168) -- Javadoc: Absent
  - `isDenyOnExp()` (line 171) -- Javadoc: Absent
  - `setDenyOnExp(boolean)` (line 174) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

---

### DriverLeagueBean.java
- **Class:** `com.torrent.surat.fms6.bean.DriverLeagueBean` (does NOT implement Serializable)
- **Class Javadoc:** Absent
- **Fields (private):** `id` (int), `driverName`, `department`, `truckType`, `redImpact`, `preOp`, `keyHour`, `tracHours`, `percActive`
- **Public methods:**
  - `getId()` (line 14) -- Javadoc: Absent
  - `setId(int)` (line 17) -- Javadoc: Absent
  - `getDriverName()` (line 20) -- Javadoc: Absent
  - `setDriverName(String)` (line 23) -- Javadoc: Absent
  - `getDepartment()` (line 26) -- Javadoc: Absent
  - `setDepartment(String)` (line 29) -- Javadoc: Absent
  - `getTruckType()` (line 32) -- Javadoc: Absent
  - `setTruckType(String)` (line 35) -- Javadoc: Absent
  - `getRedImpact()` (line 38) -- Javadoc: Absent
  - `setRedImpact(String)` (line 41) -- Javadoc: Absent
  - `getPreOp()` (line 44) -- Javadoc: Absent
  - `setPreOp(String)` (line 47) -- Javadoc: Absent
  - `getKeyHour()` (line 50) -- Javadoc: Absent
  - `setKeyHour(String)` (line 53) -- Javadoc: Absent
  - `getTracHours()` (line 56) -- Javadoc: Absent
  - `setTracHours(String)` (line 59) -- Javadoc: Absent
  - `getPercActive()` (line 62) -- Javadoc: Absent
  - `setPercActive(String)` (line 65) -- Javadoc: Absent
- **TODO/FIXME/HACK comments:** None

---

## Findings

### A01-P3-001 -- Missing class Javadoc on all 14 bean classes
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/BatteryBean.java:5`, `BroadcastmsgBean.java:5`, `CanruleBean.java:3`, `CustLocDeptBean.java:3`, `CustomerBean.java:3`, `DailyUsageDeptDataBean.java:6`, `DailyUsageHourBean.java:8`, `DashboarSubscriptionBean.java:3`, `DayhoursBean.java:5`, `DehireBean.java:5`, `DetailedReportUtil.java:5`, `DriverBean.java:5`, `DriverImportBean.java:5`, `DriverLeagueBean.java:3`
- **Severity:** MEDIUM
- **Category:** Documentation > Missing Class Javadoc
- **Description:** None of the 14 bean classes has a class-level Javadoc comment describing its purpose, domain context, or usage. For simple data-transfer beans this is a moderate concern, but several classes have non-obvious domain semantics (e.g., what is a "CAN rule"? what does "bef"/"aft" mean in BatteryBean? what does DailyUsageHourBean aggregate?). Without class-level documentation, developers must reverse-engineer usage from callers.
- **Evidence:** Every file's class declaration is simply `public class XxxBean` or `public class XxxBean implements Serializable` with no preceding `/** ... */` block.
- **Recommendation:** Add a Javadoc comment to each class explaining its domain purpose, what entity/report it maps to, and any key usage constraints. Prioritize DailyUsageHourBean, DetailedReportUtil, and BatteryBean due to their non-obvious field naming.

---

### A01-P3-002 -- Missing Javadoc on business logic methods in DailyUsageHourBean
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java:27` (`getModelList()`), line 39 (`arrangeData(String)`), line 101 (`getWeekList(String)`)
- **Severity:** MEDIUM
- **Category:** Documentation > Missing Method Javadoc (Business Logic)
- **Description:** Three public methods contain significant business logic but have no Javadoc:
  - `getModelList()` (line 27): iterates `deptDataList` to extract a unique list of model names. Despite the getter name, it performs computation and mutates `modelList`.
  - `arrangeData(String modelName)` (line 39): complex method that clears lists, iterates nested data structures, filters by week and model name, and builds comma-delimited strings. It returns an `ArrayList<String>` with no documentation of the format.
  - `getWeekList(String model)` (line 101): iterates `deptDataList` to extract a unique week list filtered by model. Despite the getter-like name, it takes a parameter and performs computation.
- **Evidence:** Lines 27-67 and 101-111 contain loops, conditionals, and string concatenation with no documentation explaining expected inputs, outputs, or the comma-delimited format.
- **Recommendation:** Add Javadoc with `@param`, `@return` descriptions. Document the comma-delimited format returned by `arrangeData()`, including the column order (modelName, location-department, week, wFrom, wTo, unitTotal, data...). Document that `getModelList()` and `getWeekList()` are not idempotent getters but accumulate data across calls.

---

### A01-P3-003 -- Missing Javadoc on analyzeAndCombine() stub method in DetailedReportUtil
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java:44`
- **Severity:** MEDIUM
- **Category:** Documentation > Missing Method Javadoc (Business Logic)
- **Description:** The `analyzeAndCombine()` method is the only non-getter/setter method in DetailedReportUtil and appears intended to combine hydraulic-related report fields, but its if-block body is empty (lines 49-51). The method effectively does nothing. There is no Javadoc explaining the intended behavior, whether it is a work-in-progress, or whether it is dead code. Without a comment or documentation, a developer cannot determine whether the empty body is intentional or an incomplete implementation.
- **Evidence:** Lines 44-53: the method loops over `vrpt_field_nm`, checks for "Hydraulic"/"HYDR"/"HYDL" strings, but the if-block has no body -- it is a no-op.
- **Recommendation:** Add Javadoc or an inline comment clarifying whether this is intentionally a no-op, dead code to be removed, or an unfinished implementation. If unfinished, add a `// TODO:` comment describing the intended behavior.

---

### A01-P3-004 -- Debug System.out.println in DetailedReportUtil constructor
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java:39-41`
- **Severity:** LOW
- **Category:** Documentation > Commented-out/Debug Code
- **Description:** The parameterized constructor contains three `System.out.println` statements that print list sizes. These appear to be leftover debug statements with no associated comment explaining their purpose or indicating they should be removed.
- **Evidence:** Lines 39-41: `System.out.println("vrpt_field_cd: " + vrpt_field_cd.size());` and two similar lines.
- **Recommendation:** Either remove the debug output or, if intentionally left for diagnostics, add a comment explaining why. Consider replacing with proper logging (e.g., `Logger.debug()`).

---

### A01-P3-005 -- Commented-out debug code in DailyUsageHourBean.arrangeData()
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java:57-59`
- **Severity:** LOW
- **Category:** Documentation > Commented-out Code
- **Description:** Lines 57-59 contain commented-out `System.out.println` debug statements within the `arrangeData()` method. These provide no documentation value and clutter the code.
- **Evidence:** `// System.out.println("dataCommaDelimited.add(\""+heading[0]+...`
- **Recommendation:** Remove the commented-out debug statements. If the output format needs to be documented, do so in a Javadoc comment on the method instead.

---

### A01-P3-006 -- Class name typo: DashboarSubscriptionBean (missing 'd')
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DashboarSubscriptionBean.java:3`
- **Severity:** HIGH
- **Category:** Documentation > Misleading Naming
- **Description:** The class is named `DashboarSubscriptionBean` -- it is missing the letter 'd' and should be `DashboardSubscriptionBean`. This misspelling could mislead developers searching for dashboard-related classes and creates confusion about the class's purpose. All callers must also use the misspelled name, propagating the error.
- **Evidence:** Line 3: `public class DashboarSubscriptionBean {`
- **Recommendation:** Rename the class to `DashboardSubscriptionBean` and update all references. At minimum, add a class Javadoc noting the intended name if renaming is deferred due to risk.

---

### A01-P3-007 -- Missing Javadoc on all getter/setter methods across all 14 files
- **File:** All 14 files in scope
- **Severity:** LOW
- **Category:** Documentation > Missing Getter/Setter Javadoc
- **Description:** Not a single getter or setter method in any of the 14 files has a Javadoc comment. The total count of undocumented public getter/setter methods across all files is approximately 260+. While individual getters/setters are trivial, many field names use cryptic abbreviations (e.g., `bef_soc`, `aft_hm`, `bef_tm`, `vrpt_veh_sttm`, `vrpt_veh_gtot`, `gmtp_id`, `src_holder`) that make their purpose unclear without documentation.
- **Evidence:** Every public method in every file lacks a `/** ... */` Javadoc block.
- **Recommendation:** At minimum, add Javadoc to getters/setters with non-obvious names. Prioritize: BatteryBean (abbreviations like `bef_soc` = "before state of charge"?), DetailedReportUtil (all `vrpt_*` fields), CanruleBean (`src_holder`, `gmtp_id`), and DriverBean (`weigand`).

---

### A01-P3-008 -- Cryptic field names without any documentation
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/BatteryBean.java:11-33`, `DetailedReportUtil.java:8-28`, `CanruleBean.java:5-17`, `DriverBean.java:8`
- **Severity:** MEDIUM
- **Category:** Documentation > Unclear Field Naming Without Comments
- **Description:** Multiple files use heavily abbreviated field names with no inline comments or Javadoc explaining their meaning:
  - **BatteryBean**: `bef_soc`, `aft_soc` (state of charge?), `bef_hm`, `aft_hm` (hour meter?), `bef_tm`, `aft_tm` (time?), `isTruck1120` (what is 1120?)
  - **DetailedReportUtil**: All 20 fields prefixed with `vrpt_veh_` are opaque. What does `vrpt` stand for? What is `stopv` vs `stop`? What is `sttm` vs `endtm`?
  - **CanruleBean**: `src_holder`, `gmtp_id` -- what do these abbreviations stand for?
  - **DriverBean**: `weigand` -- likely "Wiegand" (access card protocol) but misspelled and undocumented.
- **Evidence:** No inline comments or field-level Javadoc exists anywhere in these files to clarify abbreviations.
- **Recommendation:** Add field-level Javadoc or inline comments defining each abbreviation. At minimum document the BatteryBean "before/after" field semantics, the DetailedReportUtil `vrpt_*` prefix meaning, and the DriverBean `weigand` field.

---

### A01-P3-009 -- Empty serialVersionUID Javadoc blocks serve no purpose
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/BatteryBean.java:7-9`, `BroadcastmsgBean.java:7-9`, `DayhoursBean.java:7-9`
- **Severity:** INFO
- **Category:** Documentation > Empty Javadoc
- **Description:** Three files contain auto-generated empty Javadoc blocks (`/** * */`) above the `serialVersionUID` constant. These provide no useful information and appear to be IDE-generated placeholders that were never filled in.
- **Evidence:** BatteryBean lines 7-9, BroadcastmsgBean lines 7-9, DayhoursBean lines 7-9 all contain identical empty `/** */` blocks.
- **Recommendation:** Either remove the empty Javadoc blocks or, if retained, add meaningful content (e.g., noting the serialization contract).

---

### A01-P3-010 -- Missing @author and @since tags on all classes
- **File:** All 14 files in scope
- **Severity:** INFO
- **Category:** Documentation > Missing Metadata Tags
- **Description:** None of the 14 classes has `@author` or `@since` tags. For a legacy codebase, knowing who authored a class and when it was introduced aids maintenance and ownership assignment.
- **Evidence:** No `@author` or `@since` tags exist in any file.
- **Recommendation:** Add `@author` and `@since` tags to class-level Javadoc when class Javadoc is added per A01-P3-001.

---

### A01-P3-011 -- getModelList() name is misleading -- performs computation, not simple retrieval
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java:27`
- **Severity:** HIGH
- **Category:** Documentation > Misleading Naming / Missing Documentation
- **Description:** The method `getModelList()` follows JavaBean getter naming conventions, which implies it simply returns the `modelList` field. However, it iterates over `deptDataList`, extracts unique model names, adds them to `modelList`, and then returns the list. Each subsequent call appends additional entries if `deptDataList` has changed, meaning the method is not idempotent. A caller trusting the "getter" convention would not expect side effects or computation. Without any documentation, this is actively misleading.
- **Evidence:** Lines 27-36: the method contains a `for` loop that mutates `modelList` before returning it.
- **Recommendation:** Either rename to `buildModelList()` / `computeModelList()` to signal computation, or add Javadoc explicitly stating that this is not a simple getter and documents its side effects. The same concern applies to `getWeekList(String)` at line 101.

---

### A01-P3-012 -- DetailedReportUtil parameterized constructor prints to stdout with no documentation
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java:34-42`
- **Severity:** MEDIUM
- **Category:** Documentation > Missing Constructor Javadoc
- **Description:** The parameterized constructor `DetailedReportUtil(ArrayList, ArrayList, ArrayList)` takes three raw `ArrayList` parameters with no documentation of what they should contain, their expected ordering, or their relationship. Additionally, it prints diagnostic output to stdout. There are no `@param` tags.
- **Evidence:** Lines 34-42: constructor accepts three unnamed-type ArrayLists and prints sizes.
- **Recommendation:** Add constructor Javadoc with `@param` tags explaining what each ArrayList contains (field codes, field names, stop values), their expected sizes/relationship, and whether null is permitted.

---

## Summary

| Severity | Count |
|----------|-------|
| HIGH     | 2     |
| MEDIUM   | 5     |
| LOW      | 3     |
| INFO     | 2     |
| **Total**| **12**|

### Key Observations

1. **Zero Javadoc exists across all 14 files.** Not a single class, method, field, or constructor has a Javadoc comment. The only `/** */` blocks are empty auto-generated placeholders on `serialVersionUID` fields in three files.

2. **Most files are simple data-transfer beans** (pure getter/setter classes), so the lack of method-level Javadoc is LOW severity for most. However, the complete absence of class-level documentation explaining the domain purpose of each bean is a MEDIUM concern.

3. **Two files contain actual business logic** -- `DailyUsageHourBean.java` and `DetailedReportUtil.java` -- and the lack of documentation on their non-trivial methods is the most significant gap. The `arrangeData()` method's output format and the `analyzeAndCombine()` stub are particularly concerning.

4. **Naming issues** (typo in `DashboarSubscriptionBean`, misleading getter names `getModelList()`/`getWeekList()`, misspelled `weigand` field) compound the documentation problem by making the code harder to discover and understand.

5. **Cryptic abbreviations** throughout BatteryBean, DetailedReportUtil, and CanruleBean are the primary barrier to understanding without external domain knowledge.
