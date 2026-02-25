# Pass 4 — Code Quality: bean package (A-D)
**Agent:** A01
**Date:** 2026-02-25
**Repo:** fleetfocus

---

## Reading Evidence

### BatteryBean.java
- **Class:** `BatteryBean implements Serializable` (169 lines)
- **Public methods:**
  - `getUnit_serial()` (line 35), `setUnit_serial(String)` (line 38)
  - `getBatteryId()` (line 41), `setBatteryId(String)` (line 44)
  - `getCharge_tm()` (line 47), `setCharge_tm(String)` (line 50)
  - `getBef_veh_nm()` (line 53), `setBef_veh_nm(String)` (line 56)
  - `getBef_dri_nm()` (line 59), `setBef_dri_nm(String)` (line 62)
  - `getBef_soc()` (line 65), `setBef_soc(String)` (line 68)
  - `getBef_hm()` (line 71), `setBef_hm(String)` (line 74)
  - `getAft_veh_nm()` (line 77), `setAft_veh_nm(String)` (line 80)
  - `getAft_dri_nm()` (line 83), `setAft_dri_nm(String)` (line 86)
  - `getAft_soc()` (line 89), `setAft_soc(String)` (line 92)
  - `getAft_hm()` (line 95), `setAft_hm(String)` (line 98)
  - `getUnit_nm()` (line 101), `setUnit_nm(String)` (line 104)
  - `getBef_tm()` (line 107), `setBef_tm(String)` (line 110)
  - `getAft_tm()` (line 113), `setAft_tm(String)` (line 116)
  - `getBef_bat_id()` (line 119), `setBef_bat_id(String)` (line 122)
  - `getAft_bat_id()` (line 125), `setAft_bat_id(String)` (line 128)
  - `getUnit_cd()` (line 131), `setUnit_cd(String)` (line 134)
  - `getDuration()` (line 137), `setDuration(String)` (line 140)
  - `isTruck1120()` (line 143), `setTruck1120(boolean)` (line 146)
  - `getBef_bat_fleet_num()` (line 149), `setBef_bat_fleet_num(String)` (line 152)
  - `getAft_bat_fleet_num()` (line 155), `setAft_bat_fleet_num(String)` (line 158)
  - `getBat_fleet_num()` (line 161), `setBat_fleet_num(String)` (line 164)
- **Commented-out code blocks:** None

### BroadcastmsgBean.java
- **Class:** `BroadcastmsgBean implements Serializable` (83 lines)
- **Public methods:**
  - `getSent_timestamp()` (line 23), `setSent_timestamp(String)` (line 26)
  - `getText()` (line 29), `setText(String)` (line 50)
  - `getType()` (line 32), `setType(String)` (line 53)
  - `getDisp_timestamp()` (line 35), `setDisp_timestamp(String)` (line 56)
  - `getResp_timestamp()` (line 38), `setResp_timestamp(String)` (line 59)
  - `getResponse()` (line 41), `setResponse(String)` (line 62)
  - `getDriver()` (line 44), `setDriver(String)` (line 65)
  - `getUnit()` (line 47), `setUnit(String)` (line 68)
  - `getProduct_type()` (line 71), `setProduct_type(String)` (line 74)
  - `getVeh_id()` (line 77), `setVeh_id(String)` (line 80)
- **Commented-out code blocks:** None

### CanruleBean.java
- **Class:** `CanruleBean` (97 lines)
- **Public methods:**
  - `getSrc_holder()` (line 19), `setSrc_holder(String)` (line 22)
  - `getSite_name()` (line 25), `setSite_name(String)` (line 28)
  - `getDepartment_name()` (line 31), `setDepartment_name(String)` (line 34)
  - `getModel_name()` (line 37), `setModel_name(String)` (line 40)
  - `getGmtp_id()` (line 43), `setGmtp_id(String)` (line 46)
  - `getSerial_no()` (line 49), `setSerial_no(String)` (line 52)
  - `getHire_no()` (line 55), `setHire_no(String)` (line 58)
  - `getCanrule_name()` (line 61), `setCanrule_name(String)` (line 64)
  - `getCustCd()` (line 67), `setCustCd(String)` (line 70)
  - `getAccess_level()` (line 73), `setAccess_level(String)` (line 76)
  - `getAccess_cust()` (line 79), `setAccess_cust(String)` (line 82)
  - `getAccess_site()` (line 85), `setAccess_site(String)` (line 88)
  - `getAccess_dept()` (line 91), `setAccess_dept(String)` (line 94)
- **Commented-out code blocks:** None

### CustLocDeptBean.java
- **Class:** `CustLocDeptBean` (29 lines)
- **Public methods:**
  - `getCustCd()` (line 6), `setCustCd(int)` (line 10)
  - `getLocCd()` (line 14), `setLocCd(int)` (line 18)
  - `getDeptCd()` (line 22), `setDeptCd(int)` (line 26)
- **Commented-out code blocks:** None

### CustomerBean.java
- **Class:** `CustomerBean` (29 lines)
- **Public methods:**
  - `isActive()` (line 9), `setActive(boolean)` (line 12)
  - `getId()` (line 15), `setId(int)` (line 21)
  - `isPasswordPolicy()` (line 18), `setPasswordPolicy(boolean)` (line 24)
- **Commented-out code blocks:** None

### DailyUsageDeptDataBean.java
- **Class:** `DailyUsageDeptDataBean implements Serializable` (113 lines)
- **Public methods:**
  - `DailyUsageDeptDataBean()` constructor (line 19)
  - `DailyUsageDeptDataBean(String, String, String, ArrayList<double[]>)` constructor (line 23)
  - `getDept_id()` (line 31), `setDept_id(String)` (line 35)
  - `getDept_name()` (line 39), `setDept_name(String)` (line 43)
  - `getModelName()` (line 47), `setModelName(String)` (line 51)
  - `getData()` (line 55), `setData(ArrayList<double[]>)` (line 59)
  - `getLoc()` (line 63), `setLoc(String)` (line 67)
  - `getWeek()` (line 71), `setWeek(String)` (line 75)
  - `getwFrom()` (line 79), `setwFrom(String)` (line 83)
  - `getwTo()` (line 87), `setwTo(String)` (line 91)
  - `getWeekInt()` (line 95), `setWeekInt(int)` (line 99)
  - `getUnitTotal()` (line 103), `setUnitTotal(int)` (line 107)
- **Commented-out code blocks:** None

### DailyUsageHourBean.java
- **Class:** `DailyUsageHourBean implements Serializable` (130 lines)
- **Public methods:**
  - `DailyUsageHourBean()` constructor (line 18)
  - `DailyUsageHourBean(boolean, ArrayList<DailyUsageDeptDataBean>)` constructor (line 22)
  - `getModelList()` (line 27)
  - `arrangeData(String)` (line 39)
  - `isIfCombine()` (line 69), `setIfCombine(boolean)` (line 73)
  - `getDeptList()` (line 77), `setDeptList(ArrayList<String>)` (line 81)
  - `getDeptDataList()` (line 85), `setDeptDataList(ArrayList<DailyUsageDeptDataBean>)` (line 89)
  - `getFinalUtil()` (line 93), `setFinalUtil(ArrayList<String>)` (line 97)
  - `getWeekList(String)` (line 101)
  - `setWeekList(ArrayList<String>)` (line 113)
  - `setModelList(ArrayList<String>)` (line 117)
  - `setWeek(String)` (line 121)
- **Commented-out code blocks:** Lines 57-59 (commented-out System.out.println debug statements)

### DashboarSubscriptionBean.java
- **Class:** `DashboarSubscriptionBean` (50 lines)
- **Public methods:**
  - `getId()` (line 11), `setId(int)` (line 29)
  - `getUserCd()` (line 14), `setUserCd(int)` (line 32)
  - `getCustCd()` (line 17), `setCustCd(int)` (line 35)
  - `getLocCd()` (line 20), `setLocCd(String)` (line 38)
  - `getLocation()` (line 23), `setLocation(String)` (line 41)
  - `getEmailId()` (line 26), `setEmailId(String)` (line 44)
- **Commented-out code blocks:** None

### DayhoursBean.java
- **Class:** `DayhoursBean implements Serializable` (62 lines)
- **Public methods:**
  - `getId()` (line 20), `setId(String)` (line 23)
  - `getTotal_hours()` (line 26), `setTotal_hours(int)` (line 29)
  - `getTotal_mins()` (line 32), `setTotal_mins(int)` (line 35)
  - `getBreak_hours()` (line 38), `setBreak_hours(int)` (line 41)
  - `getBreak_mins()` (line 44), `setBreak_mins(int)` (line 47)
  - `getDays()` (line 50), `setDays(int)` (line 53)
  - `getAvail_hours()` (line 56), `setAvail_hours(String)` (line 59)
- **Commented-out code blocks:** None

### DehireBean.java
- **Class:** `DehireBean` (31 lines)
- **Public methods:**
  - `getVehCd()` (line 10), `setVehCd(int)` (line 13)
  - `getHire_time()` (line 16), `setHire_time(Timestamp)` (line 19)
  - `getDehire_time()` (line 22), `setDehire_time(Timestamp)` (line 25)
- **Commented-out code blocks:** None

### DetailedReportUtil.java
- **Class:** `DetailedReportUtil` (167 lines)
- **Public methods:**
  - `DetailedReportUtil()` constructor (line 30)
  - `DetailedReportUtil(ArrayList, ArrayList, ArrayList)` constructor (line 34)
  - `analyzeAndCombine()` (line 44)
  - `getVrpt_field_cd()` (line 57), `setVrpt_field_cd(ArrayList)` (line 60)
  - `getVrpt_field_nm()` (line 63), `setVrpt_field_nm(ArrayList)` (line 66)
  - `getVrpt_veh_typ_cd()` (line 69), `setVrpt_veh_typ_cd(ArrayList)` (line 72)
  - `getVrpt_veh_typ()` (line 75), `setVrpt_veh_typ(ArrayList)` (line 78)
  - `getVrpt_veh_cd()` (line 81), `setVrpt_veh_cd(ArrayList)` (line 84)
  - `getVrpt_veh_nm()` (line 87), `setVrpt_veh_nm(ArrayList)` (line 90)
  - `getVrpt_veh_id()` (line 93), `setVrpt_veh_id(ArrayList)` (line 96)
  - `getVrpt_veh_value_start()` (line 99), `setVrpt_veh_value_start(ArrayList)` (line 102)
  - `getVrpt_veh_value_stop()` (line 105), `setVrpt_veh_value_stop(ArrayList)` (line 108)
  - `getVrpt_veh_value_state()` (line 111), `setVrpt_veh_value_state(ArrayList)` (line 114)
  - `getVrpt_veh_value_stopv()` (line 117), `setVrpt_veh_value_stopv(ArrayList)` (line 120)
  - `getVrpt_veh_driv_cd()` (line 123), `setVrpt_veh_driv_cd(ArrayList)` (line 126)
  - `getVrpt_veh_driv_nm()` (line 129), `setVrpt_veh_driv_nm(ArrayList)` (line 132)
  - `getVrpt_veh_driv_tm()` (line 135), `setVrpt_veh_driv_tm(ArrayList)` (line 138)
  - `getVrpt_veh_sttm()` (line 141), `setVrpt_veh_sttm(ArrayList)` (line 144)
  - `getVrpt_veh_endtm()` (line 147), `setVrpt_veh_endtm(ArrayList)` (line 150)
  - `getVrpt_veh_tot()` (line 153), `setVrpt_veh_tot(ArrayList)` (line 156)
  - `getVrpt_veh_gtot()` (line 159), `setVrpt_veh_gtot(ArrayList)` (line 162)
- **Commented-out code blocks:** None

### DriverBean.java
- **Class:** `DriverBean implements Serializable` (39 lines)
- **Public methods:**
  - `getUser_cd()` (line 12), `setUser_cd(String)` (line 15)
  - `getId()` (line 18), `setId(String)` (line 21)
  - `getWeigand()` (line 24), `setWeigand(String)` (line 27)
  - `getVeh_type()` (line 30), `setVeh_type(String)` (line 33)
- **Commented-out code blocks:** None

### DriverImportBean.java
- **Class:** `DriverImportBean implements Serializable` (179 lines)
- **Public methods:**
  - `getKey_reader()` (line 33), `setKey_reader(String)` (line 36)
  - `getFacility_code()` (line 39), `setFacility_code(String)` (line 42)
  - `getId()` (line 45), `setId(String)` (line 48)
  - `getLicno()` (line 51), `setLicno(String)` (line 54)
  - `getPhone()` (line 57), `setPhone(String)` (line 60)
  - `getActive()` (line 63), `setActive(String)` (line 66)
  - `getLocation()` (line 69), `setLocation(String)` (line 72)
  - `getDepartment()` (line 75), `setDepartment(String)` (line 78)
  - `getSite()` (line 81), `setSite(String)` (line 84)
  - `getComp_id()` (line 87), `setComp_id(String)` (line 90)
  - `getFirst_name()` (line 93), `setFirst_name(String)` (line 96)
  - `getLast_name()` (line 99), `setLast_name(String)` (line 102)
  - `getExpirydt()` (line 105), `setExpirydt(String)` (line 108)
  - `getCard_no()` (line 111), `setCard_no(String)` (line 114)
  - `getCustCd()` (line 117), `setCustCd(String)` (line 120)
  - `getLocCd()` (line 123), `setLocCd(String)` (line 126)
  - `getDeptCd()` (line 129), `setDeptCd(String)` (line 132)
  - `getCardType()` (line 135), `setCardType(String)` (line 138)
  - `getAccess_level()` (line 141), `setAccess_level(String)` (line 144)
  - `getAccess_cust()` (line 147), `setAccess_cust(String)` (line 150)
  - `getAccess_site()` (line 153), `setAccess_site(String)` (line 156)
  - `getAccess_dept()` (line 159), `setAccess_dept(String)` (line 162)
  - `getLicenseType()` (line 165), `setLicenseType(String)` (line 168)
  - `isDenyOnExp()` (line 171), `setDenyOnExp(boolean)` (line 174)
- **Commented-out code blocks:** None

### DriverLeagueBean.java
- **Class:** `DriverLeagueBean` (70 lines)
- **Public methods:**
  - `getId()` (line 14), `setId(int)` (line 17)
  - `getDriverName()` (line 20), `setDriverName(String)` (line 23)
  - `getDepartment()` (line 26), `setDepartment(String)` (line 29)
  - `getTruckType()` (line 32), `setTruckType(String)` (line 35)
  - `getRedImpact()` (line 38), `setRedImpact(String)` (line 41)
  - `getPreOp()` (line 44), `setPreOp(String)` (line 47)
  - `getKeyHour()` (line 50), `setKeyHour(String)` (line 53)
  - `getTracHours()` (line 56), `setTracHours(String)` (line 59)
  - `getPercActive()` (line 62), `setPercActive(String)` (line 65)
- **Commented-out code blocks:** None

---

## Findings

### A01-01 — Pervasive snake_case naming in getter/setter methods across bean package
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/BatteryBean.java` (all lines), also: `BroadcastmsgBean.java`, `CanruleBean.java`, `DailyUsageDeptDataBean.java`, `DayhoursBean.java`, `DehireBean.java`, `DetailedReportUtil.java`, `DriverBean.java`, `DriverImportBean.java`
- **Severity:** LOW
- **Category:** Code Quality > Naming Conventions
- **Description:** The vast majority of getter/setter methods across these beans use snake_case naming instead of the standard Java camelCase convention (e.g., `getUnit_serial()`, `getBef_veh_nm()`, `getCharge_tm()`, `getSent_timestamp()`, `getSrc_holder()`, `getDept_id()`, `getTotal_hours()`, `getHire_time()`, `getVrpt_field_cd()`, `getUser_cd()`, `getFirst_name()`, `getAccess_level()`). This violates Java Bean naming conventions and makes the codebase harder to navigate. This pattern is pervasive across 9 of the 14 audited files.
- **Evidence:** `BatteryBean`: `getUnit_serial()`, `getCharge_tm()`, `getBef_veh_nm()`, etc. (22 pairs); `BroadcastmsgBean`: `getSent_timestamp()`, `getDisp_timestamp()`, etc. (6 pairs); `CanruleBean`: `getSrc_holder()`, `getSite_name()`, etc. (10 pairs); and similarly in all other listed files.
- **Recommendation:** For new code, adopt camelCase naming (e.g., `unitSerial`, `befVehNm`). Retrofitting existing code would require coordinated changes with all consumers and is not recommended without comprehensive regression testing.

### A01-02 — Package-private (default) field visibility in BatteryBean, DayhoursBean, DriverBean, DetailedReportUtil
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/BatteryBean.java`:11-33
- **Severity:** MEDIUM
- **Category:** Code Quality > Leaky Abstractions
- **Description:** Fields in `BatteryBean` (lines 11-33), `DayhoursBean` (lines 12-18), `DriverBean` (lines 6-9), and `DetailedReportUtil` (lines 8-29) are declared with package-private (default) visibility instead of `private`. This means any class in the same package can bypass the getters/setters and directly access/modify these fields, breaking encapsulation.
- **Evidence:**
  - `BatteryBean.java` line 13: `String unit_nm = "";` (no access modifier)
  - `DayhoursBean.java` line 12: `String id = "";` (no access modifier)
  - `DriverBean.java` line 6: `String id = "";` (no access modifier)
  - `DetailedReportUtil.java` line 8: `ArrayList vrpt_field_cd = new ArrayList();` (no access modifier)
  - `CustomerBean.java` lines 5-7: `int id;`, `boolean passwordPolicy;`, `boolean active;` (no access modifier)
  - `CustLocDeptBean.java` line 4: `int custCd,locCd,deptCd;` (no access modifier)
- **Recommendation:** Change all bean fields to `private` to properly encapsulate internal state.

### A01-03 — Raw type ArrayList usage throughout DetailedReportUtil
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java`:8-29
- **Severity:** MEDIUM
- **Category:** Code Quality > Deprecated API Usage / Type Safety
- **Description:** All 20 `ArrayList` fields in `DetailedReportUtil` and the constructor parameters use raw types without generics. This bypasses compile-time type safety and can lead to `ClassCastException` at runtime. The raw type `ArrayList` has been considered a code smell since Java 5 (2004).
- **Evidence:**
  ```java
  // Line 8
  ArrayList vrpt_field_cd = new ArrayList();
  // Line 34 (constructor)
  public DetailedReportUtil(ArrayList vrpt_field_cd, ArrayList vrpt_field_nm, ArrayList vrpt_veh_value_stop) {
  ```
  All 20 fields on lines 8-29 are raw `ArrayList` types. All corresponding getter/setter methods also use raw `ArrayList` in their signatures.
- **Recommendation:** Add appropriate type parameters (e.g., `ArrayList<String>`) to all collections and their associated method signatures.

### A01-04 — Raw type ArrayList usage in DailyUsageHourBean
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java`:11-15
- **Severity:** MEDIUM
- **Category:** Code Quality > Deprecated API Usage / Type Safety
- **Description:** Five `ArrayList` fields are initialized with raw-type constructors (diamond operator missing), generating unchecked warnings. While the field declarations include generics, the `new ArrayList()` on the right-hand side is raw.
- **Evidence:**
  ```java
  // Line 11
  private ArrayList<String> deptList = new ArrayList();
  // Line 12
  private ArrayList<String> modelList = new ArrayList();
  // Line 13
  private ArrayList<DailyUsageDeptDataBean> deptDataList = new ArrayList();
  // Line 14
  private ArrayList<String> finalUtil = new ArrayList();
  // Line 15
  private ArrayList<String> weekList = new ArrayList();
  ```
- **Recommendation:** Use the diamond operator: `new ArrayList<>()`.

### A01-05 — System.out.println in production constructor of DetailedReportUtil
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java`:39-41
- **Severity:** MEDIUM
- **Category:** Code Quality > Error Handling / Debug Code in Production
- **Description:** The parameterized constructor prints debug information to stdout using `System.out.println()`. This is inappropriate for production code as it pollutes logs, provides no log-level control, and can expose internal state to anyone with console access.
- **Evidence:**
  ```java
  // Lines 39-41
  System.out.println("vrpt_field_cd: " + vrpt_field_cd.size());
  System.out.println("vrpt_field_nm: " + vrpt_field_nm.size());
  System.out.println("vrpt_veh_value_stop: " + vrpt_veh_value_stop.size());
  ```
- **Recommendation:** Remove these debug statements or replace with proper logging using a framework such as SLF4J/Log4j at DEBUG level.

### A01-06 — Empty method body with stub logic in DetailedReportUtil.analyzeAndCombine()
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java`:44-53
- **Severity:** MEDIUM
- **Category:** Code Quality > Dead Code / Technical Debt
- **Description:** The `analyzeAndCombine()` method iterates over field names and checks for "Hydraulic"/"HYDR"/"HYDL" substrings, but the `if` block body is completely empty. The method does nothing -- it is dead code that appears to be a partially implemented feature or abandoned stub.
- **Evidence:**
  ```java
  // Lines 44-53
  public void analyzeAndCombine() {
      for( int i = 0; i < vrpt_field_nm.size(); i++) {
          String fldName = vrpt_field_nm.get(i).toString();
          if( fldName.contains("Hydraulic") || fldName.contains("HYDR") || fldName.contains("HYDL")) {
              // empty body
          }
      }
  }
  ```
- **Recommendation:** Either implement the intended logic or remove the method entirely. If it is intentionally deferred, add a `// TODO` comment with a tracking ticket reference.

### A01-07 — Commented-out debug code in DailyUsageHourBean.arrangeData()
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java`:57-59
- **Severity:** LOW
- **Category:** Code Quality > Dead Code / Commented-Out Code
- **Description:** Three lines of `System.out.println` debug statements are commented out within the `arrangeData()` method. Commented-out code adds noise, makes maintenance harder, and should be managed through version control rather than left in source files.
- **Evidence:**
  ```java
  // Lines 57-59
  //  System.out.println("dataCommaDelimited.add(\""+heading[0]+","+heading[1]+...
  //  +Arrays.toString(usageBean.getData().get(j)).replace("[", "").replace("]", "")+"\");");
  //
  ```
- **Recommendation:** Remove the commented-out code. It is preserved in version control history if needed again.

### A01-08 — Unused import: java.util.Arrays in DailyUsageHourBean
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java`:5
- **Severity:** INFO
- **Category:** Code Quality > Dead Code / Unused Imports
- **Description:** The `java.util.Arrays` import is used only on line 61 inside the `arrangeData()` method. Upon closer inspection, `Arrays.toString()` IS used on line 61, so this import is actually utilized. However, note that the commented-out code on lines 57-58 also references `Arrays.toString()`. If the active usage on line 61 were removed, this import would become dead.
- **Reclassification:** This finding is **withdrawn** -- the import is in active use.

### A01-09 — Redundant object instantiation pattern in DailyUsageHourBean
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java`:29-30, 43-44, 103-104
- **Severity:** LOW
- **Category:** Code Quality > Performance / Wasteful Allocation
- **Description:** In three methods (`getModelList`, `arrangeData`, `getWeekList`), a `DailyUsageDeptDataBean` object is instantiated with `new` and immediately overwritten by an assignment from the list. The freshly constructed object is discarded, creating unnecessary garbage collection work.
- **Evidence:**
  ```java
  // Lines 29-30
  DailyUsageDeptDataBean usageBean = new DailyUsageDeptDataBean();
  usageBean = deptDataList.get(i);  // new object from line 29 is discarded
  // Same pattern at lines 43-44 and 103-104
  ```
- **Recommendation:** Replace with direct assignment: `DailyUsageDeptDataBean usageBean = deptDataList.get(i);`

### A01-10 — Missing Serializable in CanruleBean, CustLocDeptBean, CustomerBean, DashboarSubscriptionBean, DehireBean, DetailedReportUtil, DriverLeagueBean
- **File:** Multiple files
- **Severity:** LOW
- **Category:** Code Quality > Architecture / Inconsistent Patterns
- **Description:** Within the audited set, `BatteryBean`, `BroadcastmsgBean`, `DailyUsageDeptDataBean`, `DailyUsageHourBean`, `DayhoursBean`, `DriverBean`, and `DriverImportBean` all implement `Serializable`. However, `CanruleBean`, `CustLocDeptBean`, `CustomerBean`, `DashboarSubscriptionBean`, `DehireBean`, `DetailedReportUtil`, and `DriverLeagueBean` do not. If these beans are ever stored in HTTP sessions, passed through RMI, or serialized for caching, the missing `Serializable` implementation will cause `NotSerializableException` at runtime. At minimum, the inconsistency indicates no clear convention exists.
- **Evidence:**
  - `CanruleBean.java` line 3: `public class CanruleBean {` (no `implements Serializable`)
  - `CustLocDeptBean.java` line 3: `public class CustLocDeptBean {`
  - `CustomerBean.java` line 3: `public class CustomerBean {`
  - `DashboarSubscriptionBean.java` line 3: `public class DashboarSubscriptionBean {`
  - `DehireBean.java` line 5: `public class DehireBean {`
  - `DetailedReportUtil.java` line 5: `public class DetailedReportUtil {`
  - `DriverLeagueBean.java` line 3: `public class DriverLeagueBean {`
- **Recommendation:** Establish a consistent policy: if beans may be serialized (e.g., placed in HTTP sessions), all should implement `Serializable` with a `serialVersionUID`. If serialization is not needed for some beans, document the rationale.

### A01-11 — Typo in class name: DashboarSubscriptionBean (missing 'd')
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DashboarSubscriptionBean.java`:3
- **Severity:** LOW
- **Category:** Code Quality > Naming Conventions
- **Description:** The class name `DashboarSubscriptionBean` is missing the letter 'd' -- it should be `DashboardSubscriptionBean`. This is a permanent misspelling baked into the file name and class name, which can cause confusion for developers and makes the class harder to discover by search.
- **Evidence:**
  ```java
  // Line 3
  public class DashboarSubscriptionBean {
  ```
  File name: `DashboarSubscriptionBean.java`
- **Recommendation:** If a rename is feasible (requires updating all references across the codebase), correct the class and file name to `DashboardSubscriptionBean`. Otherwise, add a class-level comment noting the intentional retention of the misspelling for backward compatibility.

### A01-12 — Missing serialVersionUID in DriverBean
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DriverBean.java`:5
- **Severity:** LOW
- **Category:** Code Quality > Architecture / Serialization
- **Description:** `DriverBean` implements `Serializable` but does not declare a `serialVersionUID`. Without an explicit `serialVersionUID`, the JVM auto-generates one based on class structure, and any structural change (adding/removing a field) will cause deserialization of previously serialized instances to fail with `InvalidClassException`.
- **Evidence:**
  ```java
  // Line 5
  public class DriverBean implements Serializable{
  // No serialVersionUID declared
  ```
  Compare with `BatteryBean` (line 10) and `DayhoursBean` (line 10), which both properly declare `serialVersionUID`.
- **Recommendation:** Add `private static final long serialVersionUID = <value>L;` to `DriverBean`.

### A01-13 — Inconsistent field initialization defaults: null vs. empty string
- **File:** Multiple files across the bean package
- **Severity:** LOW
- **Category:** Code Quality > Style and Consistency
- **Description:** Different beans use different default initialization strategies for String fields. Some use `""` (empty string), others use `null`. Within the same codebase, this inconsistency can lead to `NullPointerException` in some beans and silent empty-string behavior in others, depending on which bean type is used.
- **Evidence:**
  - `BatteryBean.java`: `String batteryId = "";` (empty string default, line 11)
  - `DriverBean.java`: `String id = "";` (empty string default, line 6)
  - `DayhoursBean.java`: `String id = "";` (empty string default, line 12)
  - `CanruleBean.java`: `private String src_holder = null;` (null default, line 5)
  - `DriverImportBean.java`: `private String id = null;` (null default, line 8)
  - `BroadcastmsgBean.java`: `private String text;` (implicit null, line 12)
  - Mixed within `DriverImportBean.java`: `private String licenseType = "";` (line 30) vs. `private String id = null;` (line 8)
- **Recommendation:** Adopt a consistent default initialization strategy for String fields across all beans (either always `""` or always `null`), and document the convention.

### A01-14 — Side-effect-producing getter methods in DailyUsageHourBean
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java`:27-36, 101-111
- **Severity:** MEDIUM
- **Category:** Code Quality > Architecture / Leaky Abstractions
- **Description:** `getModelList()` (line 27) and `getWeekList(String)` (line 101) are named as getters but perform computation with side effects: they iterate through `deptDataList` and mutate the internal `modelList` and `weekList` fields. Calling these getters repeatedly will add duplicate entries to the lists since they append without clearing (unlike `arrangeData()` which does clear). This violates the principle of least surprise for getter methods.
- **Evidence:**
  ```java
  // Lines 27-36 - getModelList mutates modelList field
  public ArrayList<String> getModelList(){
      for(int i=0; i<deptDataList.size(); i++){
          ...
          if(!modelList.contains(usageBean.getModelName())){
              modelList.add(usageBean.getModelName());
          }
      }
      return modelList;
  }
  ```
  ```java
  // Lines 101-111 - getWeekList mutates weekList field
  public ArrayList<String> getWeekList(String model) {
      for(int i = 0; i < deptDataList.size(); i++){
          ...
          if( !weekList.contains(w) && ...){
              weekList.add(w);
          }
      }
      return weekList;
  }
  ```
- **Recommendation:** Rename to `buildModelList()` / `buildWeekList()` to indicate mutation, or refactor to compute and return a new list without modifying internal state. If repeated calls are expected, clear the internal list at the start (as `arrangeData()` does).

### A01-15 — Business logic in bean class: DailyUsageHourBean.arrangeData()
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageHourBean.java`:39-67
- **Severity:** LOW
- **Category:** Code Quality > Architecture / Tight Coupling
- **Description:** `DailyUsageHourBean` is a data bean but contains significant business logic in `arrangeData()` (string concatenation, data transformation, filtering by model name and week). This mixes data representation with data processing, violating the single-responsibility principle. Beans in this package should ideally be pure data holders.
- **Evidence:** The `arrangeData()` method (lines 39-67) performs nested iteration, string matching, array-to-string conversion, and builds comma-delimited output strings -- all business/transformation logic.
- **Recommendation:** Extract the `arrangeData()`, `getModelList()`, and `getWeekList()` logic into a separate service or utility class, keeping `DailyUsageHourBean` as a pure data holder.

### A01-16 — DetailedReportUtil is a God class with 40+ public methods
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java`
- **Severity:** MEDIUM
- **Category:** Code Quality > Architecture / God Class
- **Description:** `DetailedReportUtil` has 20 field pairs (40 getters/setters) plus 2 constructors and 1 business method, totaling 43 public methods. It manages 20 parallel `ArrayList` fields that together represent a report's structure. The use of parallel arrays rather than a structured object model is a design smell that makes the class fragile and hard to maintain.
- **Evidence:** 20 `ArrayList` fields on lines 8-29, each with a getter and setter (lines 57-164), plus constructors at lines 30 and 34, plus `analyzeAndCombine()` at line 44. Total: 43 public members.
- **Recommendation:** Refactor the parallel arrays into a typed collection of a structured inner class (e.g., `ReportField`, `VehicleReportEntry`). This would reduce the method count dramatically and improve type safety.

### A01-17 — Mutable internal collections exposed via getters
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DetailedReportUtil.java`:57-164, `DailyUsageDeptDataBean.java`:55, `DailyUsageHourBean.java`:77-98
- **Severity:** LOW
- **Category:** Code Quality > Leaky Abstractions
- **Description:** Multiple beans return direct references to their internal mutable `ArrayList` fields via getters. External code can modify these lists without going through the bean's API, breaking encapsulation. This is especially concerning for `DetailedReportUtil` with its 20 exposed raw `ArrayList` references.
- **Evidence:**
  ```java
  // DetailedReportUtil.java line 57
  public ArrayList getVrpt_field_cd() {
      return vrpt_field_cd;  // returns mutable internal reference
  }
  // DailyUsageDeptDataBean.java line 55
  public ArrayList<double[]> getData() {
      return data;  // returns mutable internal reference
  }
  ```
- **Recommendation:** Return unmodifiable views (`Collections.unmodifiableList(...)`) or defensive copies from getters, especially for collections.

### A01-18 — Concrete ArrayList type used in method signatures instead of List interface
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/DailyUsageDeptDataBean.java`:55-60, `DailyUsageHourBean.java`:27-98, `DetailedReportUtil.java`:57-164
- **Severity:** INFO
- **Category:** Code Quality > Style and Consistency
- **Description:** All collection-typed method parameters and return types use the concrete `ArrayList` class rather than the `List` interface. This tightly couples callers to the `ArrayList` implementation and prevents substituting other `List` implementations.
- **Evidence:**
  ```java
  // DailyUsageDeptDataBean.java line 55
  public ArrayList<double[]> getData() { ... }
  // DailyUsageHourBean.java line 27
  public ArrayList<String> getModelList(){ ... }
  // DetailedReportUtil.java line 57
  public ArrayList getVrpt_field_cd() { ... }
  ```
- **Recommendation:** Use `List` interface in method signatures: `public List<String> getModelList()`.

---

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 0     |
| HIGH     | 0     |
| MEDIUM   | 6     |
| LOW      | 8     |
| INFO     | 1     |
| **Total**| **15** |

**Key Themes:**
1. **Naming conventions (A01-01, A01-11):** Pervasive snake_case naming for methods/fields violates Java conventions; a class name typo in `DashboarSubscriptionBean`.
2. **Encapsulation failures (A01-02, A01-17):** Package-private fields and direct mutable collection exposure break bean encapsulation.
3. **Type safety (A01-03, A01-04, A01-18):** Raw `ArrayList` usage and concrete types in signatures reduce compile-time safety.
4. **Dead/debug code (A01-05, A01-06, A01-07):** `System.out.println` in production, an empty method body, and commented-out code.
5. **Inconsistent patterns (A01-10, A01-12, A01-13):** Mixed `Serializable` adoption, missing `serialVersionUID`, inconsistent field defaults.
6. **Architecture concerns (A01-14, A01-15, A01-16):** Side-effecting getters, business logic in beans, and a proto-God class with parallel arrays.
