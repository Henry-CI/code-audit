# Pass 2 — Test Coverage: bean package (E-P)
**Agent:** A02
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

## Test Infrastructure Assessment

The repository contains **zero test infrastructure**. There is no `test/` or `src/test/` directory. No JUnit, TestNG, or any other testing framework dependency was found. A search for `@Test` annotations, `junit`, and `testng` references across the entire `WEB-INF/src` tree returned no results. The only file matching `*Test*.java` is `EncryptTest.java` under `util/`, which is a decompiled encryption utility class (not a test class). There is no `pom.xml` or `build.gradle` declaring test dependencies. **Test coverage for all files in this audit is 0%.**

---

## Reading Evidence

### EntityBean.java
- **Class:** `com.torrent.surat.fms6.bean.EntityBean` implements `Serializable`
- **Fields/Constants:**
  - `serialVersionUID` = -2293212649217825945L (line 10)
  - `String id` (line 12), `String name` (line 13), `double totalno` (line 14), `String attribute` (line 15), `String locs` (line 16), `String depts` (line 17)
- **Public methods:**
  - `getId()` (line 19)
  - `setId(String id)` (line 22)
  - `getName()` (line 25)
  - `setName(String name)` (line 28)
  - `getTotalno()` (line 31)
  - `setTotalno(double totalno)` (line 34)
  - `getAttribute()` (line 37)
  - `setAttribute(String attribute)` (line 40)
  - `getLocs()` (line 43)
  - `setLocs(String locs)` (line 46)
  - `getDepts()` (line 49)
  - `setDepts(String depts)` (line 52)
- **Lines:** 55 total
- **Complexity:** Pure getter/setter bean. No business logic.

---

### FleetCheckBean.java
- **Class:** `com.torrent.surat.fms6.bean.FleetCheckBean` (no Serializable)
- **Fields/Constants:**
  - `String unitName` (line 7), `String avg_completion_time` = "N/A" (line 8), `ArrayList<String> frequent_failed_question` (line 9)
- **Public methods:**
  - `getAvg_completion_time()` (line 11)
  - `setAvg_completion_time(String avg_completion_time)` (line 14)
  - `getFrequent_failed_question()` (line 18)
  - `setFrequent_failed_question(ArrayList<String> frequent_failed_question)` (line 21)
  - `getUnitName()` (line 25)
  - `setUnitName(String unitName)` (line 28)
- **Lines:** 31 total
- **Complexity:** Pure getter/setter bean. Default value "N/A" for avg_completion_time is notable.

---

### ImpactBean.java
- **Class:** `com.torrent.surat.fms6.bean.ImpactBean` implements `Serializable`
- **Fields/Constants:**
  - `serialVersionUID` = -3410929526546378632L (line 10)
  - `String cust_cd` (line 11), `String loc_cd` (line 12), `String dept_cd` (line 13), `String dept_name` (line 14), `String model_cd` (line 15), `String model_name` (line 16), `String driver_cd` (line 17), `String driver_name` (line 18), `String unit_cd` (line 19), `String unit_name` (line 20), `String unit_type` (line 21)
  - `int year` (line 22), `int month` (line 23), `int impact_no` (line 24)
  - `int[] blueshock = new int[8]` (line 26), `int[] ambershock = new int[8]` (line 27), `int[] redshock = new int[8]` (line 28)
  - `int blueimpact` (line 29), `int amberimpact` (line 30), `int redimpact` (line 31), `int iotime` (line 32)
  - `int[][] blueshockShift = new int[8][3]` (line 34), `int[][] ambershockShift = new int[8][3]` (line 35), `int[][] redshockShift = new int[8][3]` (line 36)
  - `String usagePercentage` (line 38)
  - `int[] impacts = null` (line 41), `int total` (line 42)
  - `HashMap<Integer, Integer> impactMap` (line 45)
- **Public methods:**
  - `addImactMap(int month, int impact_no)` (line 47) -- **NOTE: method name typo "addImactMap" (missing 'p')**
  - `getModel_name()` (line 52), `setModel_name(String)` (line 55)
  - `getModel_cd()` (line 58), `setModel_cd(String)` (line 60)
  - `getDept_name()` (line 64), `setDept_name(String)` (line 67)
  - `getDept_cd()` (line 70), `setDept_cd(String)` (line 73)
  - `getDriver_name()` (line 76), `setDriver_name(String)` (line 79)
  - `getDriver_cd()` (line 82), `setDriver_cd(String)` (line 85)
  - `getYear()` (line 88), `setYear(int)` (line 91)
  - `getCust_cd()` (line 94), `setCust_cd(String)` (line 97)
  - `getLoc_cd()` (line 100), `setLoc_cd(String)` (line 103)
  - `getImpactMap()` (line 106), `setImpactMap(HashMap<Integer, Integer>)` (line 109)
  - `getMonth()` (line 112), `setMonth(int)` (line 116)
  - `getImpact_no()` (line 120), `setImpact_no(int)` (line 124)
  - `getBlueshock()` (line 128), `setBlueshock(int[])` (line 132)
  - `getAmbershock()` (line 136), `setAmbershock(int[])` (line 140)
  - `getRedshock()` (line 144), `setRedshock(int[])` (line 148)
  - `getUnit_cd()` (line 152), `setUnit_cd(String)` (line 156)
  - `getUnit_name()` (line 160), `setUnit_name(String)` (line 164)
  - `getBlueimpact()` (line 168), `setBlueimpact(int)` (line 172)
  - `getAmberimpact()` (line 176), `setAmberimpact(int)` (line 180)
  - `getRedimpact()` (line 184), `setRedimpact(int)` (line 188)
  - `getIotime()` (line 192), `setIotime(int)` (line 196)
  - `getUsagePercentage()` (line 200), `setUsagePercentage(String)` (line 204)
  - `getImpacts()` (line 208), `setImpacts(int[])` (line 212)
  - `getTotal()` (line 216), `setTotal(int)` (line 220)
  - `getUnit_type()` (line 224), `setUnit_type(String)` (line 228)
  - `getBlueshockShift()` (line 232), `getAmbershockShift()` (line 236), `getRedshockShift()` (line 240)
  - `setBlueshockShift(int[][])` (line 244), `setAmbershockShift(int[][])` (line 248), `setRedshockShift(int[][])` (line 252)
- **Lines:** 258 total
- **Complexity:** Primarily getter/setter but contains `addImactMap()` which mutates internal HashMap state. Fixed-size arrays (int[8], int[8][3]) represent business data structures for shock/impact reporting. This is the most complex bean in this batch.

---

### ImpactDeptBean.java
- **Class:** `com.torrent.surat.fms6.bean.ImpactDeptBean` implements `Serializable`
- **Fields/Constants:**
  - `serialVersionUID` = 907377188489186366L (line 10)
  - `String dept_cd` (line 12), `String dept_name` (line 13)
  - `ArrayList<ImpactSummaryBean> arrImpactSummryBean` (line 14)
  - `int total` (line 15)
- **Public methods:**
  - `getDept_cd()` (line 18), `setDept_cd(String)` (line 21)
  - `getDept_name()` (line 24), `setDept_name(String)` (line 27)
  - `getArrImpactSummryBean()` (line 30), `setArrImpactSummryBean(ArrayList<ImpactSummaryBean>)` (line 33)
  - `getTotal()` (line 37), `setTotal(int)` (line 40)
- **Lines:** 45 total
- **Complexity:** Pure getter/setter bean. Aggregation container for ImpactSummaryBean list.

---

### ImpactLocBean.java
- **Class:** `com.torrent.surat.fms6.bean.ImpactLocBean` implements `Serializable`
- **Fields/Constants:**
  - `serialVersionUID` = 4253198288627637842L (line 11)
  - `String loc_cd` (line 13), `String loc_name` (line 14)
  - `ArrayList<ImpactDeptBean> arrImpactDeptBean` (line 15)
  - `int index` (line 16), `int total` (line 17)
- **Public methods:**
  - `getLoc_cd()` (line 19), `setLoc_cd(String)` (line 22)
  - `getLoc_name()` (line 25), `setLoc_name(String)` (line 28)
  - `getArrImpactDeptBean()` (line 31), `setArrImpactDeptBean(ArrayList<ImpactDeptBean>)` (line 34)
  - `getIndex()` (line 37), `setIndex(int)` (line 40)
  - `getTotal()` (line 43), `setTotal(int)` (line 46)
  - `addArrImpactDeptBean(ImpactDeptBean impactDeptBean)` (line 50)
- **Lines:** 54 total
- **Complexity:** Getter/setter bean with one convenience add method.

---

### ImpactSummaryBean.java
- **Class:** `com.torrent.surat.fms6.bean.ImpactSummaryBean` implements `Serializable`
- **Fields/Constants:**
  - No explicit serialVersionUID declared (missing!)
  - `String loc_cd` (line 8), `String loc_name` (line 9)
  - `ArrayList<ImpactBean> arrImpact` (line 10)
  - `int index` (line 11), `int total` (line 12)
  - `String driver_cd` (line 13), `String driver_name` (line 14)
- **Public methods:**
  - `getLoc_cd()` (line 16), `setLoc_cd(String)` (line 19)
  - `getLoc_name()` (line 22), `setLoc_name(String)` (line 25)
  - `getArrImpact()` (line 28), `setArrImpact(ArrayList<ImpactBean>)` (line 31)
  - `getIndex()` (line 34), `setIndex(int)` (line 37)
  - `addArrImpact(ImpactBean impactBean)` (line 40)
  - `getTotal()` (line 43), `setTotal(int)` (line 46)
  - `getDriver_cd()` (line 49), `setDriver_cd(String)` (line 52)
  - `getDriver_name()` (line 55), `setDriver_name(String)` (line 58)
- **Lines:** 62 total
- **Complexity:** Getter/setter bean with one convenience add method. **Missing serialVersionUID despite implementing Serializable.**

---

### LicenseBlackListBean.java
- **Class:** `com.torrent.surat.fms6.bean.LicenseBlackListBean` (no Serializable)
- **Fields/Constants:**
  - `String vehicleType` (line 7), `String custCd` (line 8), `String locCd` (line 9), `String deptCd` (line 10)
  - `String expiryDate` (line 11), `String driverCd` (line 12)
  - `String access_level = null` (line 13), `String access_cust = null` (line 14), `String access_site = null` (line 15), `String access_dept = null` (line 16)
  - `ArrayList<String> vehicleCds` (line 17)
- **Public methods:**
  - `getVehicleType()` (line 19), `setVehicleType(String)` (line 22)
  - `getCustCd()` (line 25), `setCustCd(String)` (line 28)
  - `getLocCd()` (line 31), `setLocCd(String)` (line 34)
  - `getDeptCd()` (line 37), `setDeptCd(String)` (line 40)
  - `getExpiryDate()` (line 43), `setExpiryDate(String)` (line 46)
  - `getDriverCd()` (line 49), `setDriverCd(String)` (line 52)
  - `getAccess_level()` (line 55), `setAccess_level(String)` (line 58)
  - `getAccess_cust()` (line 61), `setAccess_cust(String)` (line 64)
  - `getAccess_site()` (line 67), `setAccess_site(String)` (line 70)
  - `getAccess_dept()` (line 73), `setAccess_dept(String)` (line 76)
  - `getVehicleCds()` (line 79), `setVehicleCds(ArrayList<String>)` (line 82)
- **Lines:** 85 total
- **Complexity:** Pure getter/setter bean. Contains access-control-related fields (access_level, access_cust, access_site, access_dept) and blacklist/licensing data.

---

### LockOutBean.java
- **Class:** `com.torrent.surat.fms6.bean.LockOutBean` implements `Serializable`
- **Fields/Constants:**
  - `serialVersionUID` = 7995241917485082877L (line 10)
  - `String id` (line 11), `String fleetno` (line 12), `String type` (line 13)
  - `String lockouttime` (line 14), `String driver` (line 15), `String unlocktime` (line 16)
  - `String master_code` (line 17)
- **Public methods:**
  - `getId()` (line 19), `setId(String)` (line 22)
  - `getFleetno()` (line 25), `setFleetno(String)` (line 28)
  - `getLockouttime()` (line 31), `setLockouttime(String)` (line 34)
  - `getDriver()` (line 37), `setDriver(String)` (line 40)
  - `getUnlocktime()` (line 43), `setUnlocktime(String)` (line 46)
  - `getMaster_code()` (line 49), `setMaster_code(String)` (line 52)
  - `getType()` (line 55), `setType(String)` (line 58)
- **Lines:** 64 total
- **Complexity:** Pure getter/setter bean. Contains security-relevant data: `master_code` (lockout bypass code) and lockout/unlock timing.

---

### MaxHourUsageBean.java
- **Class:** `com.torrent.surat.fms6.bean.MaxHourUsageBean` implements `Serializable`
- **Fields/Constants:**
  - `serialVersionUID` = -4041017520620612211L (line 11)
  - `String model_name` (line 13), `String model_img` (line 14)
  - `ArrayList<UnitutilBean> arrUnitUtil` (line 15)
- **Public methods:**
  - `getModel_name()` (line 17), `setModel_name(String)` (line 20)
  - `getModel_img()` (line 23), `setModel_img(String)` (line 26)
  - `getArrUnitUtil()` (line 29), `setArrUnitUtil(ArrayList<UnitutilBean>)` (line 32)
  - `addArrUnitUtil(UnitutilBean unitutilBean)` (line 36)
- **Lines:** 40 total
- **Complexity:** Getter/setter bean with one convenience add method.

---

### MenuBean.java
- **Class:** `com.torrent.surat.fms6.bean.MenuBean` (no Serializable)
- **Fields/Constants:**
  - `String Menus_Cd` (line 7), `String Menus_Name` (line 8), `String Form_Cd` (line 9), `String Form_Name` (line 10), `String Form_Path` (line 11), `String ReskinPath` (line 12)
- **Public methods:**
  - `getMenus_Cd()` (line 13), `getMenus_Name()` (line 16), `getForm_Cd()` (line 19), `getForm_Name()` (line 22), `getForm_Path()` (line 25), `getReskinPath()` (line 28)
  - `setMenus_Cd(String)` (line 31), `setMenus_Name(String)` (line 34), `setForm_Cd(String)` (line 37), `setForm_Name(String)` (line 40), `setForm_Path(String)` (line 43), `setReskinPath(String)` (line 46)
- **Lines:** 52 total
- **Complexity:** Pure getter/setter bean. Stores navigation/menu configuration. Field naming convention violates Java standards (uppercase first letter for instance fields).

---

### MymessagesUsersBean.java
- **Class:** `com.torrent.surat.fms6.bean.MymessagesUsersBean` implements `Serializable`
- **Fields/Constants:**
  - `serialVersionUID` = -1903517877748793487L (line 10)
  - `String cust_cd` (line 12), `String loc_cd` (line 13), `String dept_cd` (line 14), `String threshold` (line 15)
  - `String user_id` (line 16), `String user_email` (line 17), `String descrption` (line 18) -- **NOTE: typo "descrption" (missing 'i')**
  - `String id` (line 19)
- **Public methods:**
  - `getCust_cd()` (line 22), `setCust_cd(String)` (line 25)
  - `getLoc_cd()` (line 28), `setLoc_cd(String)` (line 31)
  - `getDept_cd()` (line 34), `setDept_cd(String)` (line 37)
  - `getThreshold()` (line 40), `setThreshold(String)` (line 43)
  - `getUser_id()` (line 46), `setUser_id(String)` (line 49)
  - `getUser_email()` (line 52), `setUser_email(String)` (line 55)
  - `getDescrption()` (line 58), `setDescrption(String)` (line 61)
  - `getId()` (line 64), `setId(String)` (line 67)
- **Lines:** 71 total
- **Complexity:** Pure getter/setter bean. Contains user identity data (user_id, user_email) and notification thresholds.

---

### NetworkSettingBean.java
- **Class:** `com.torrent.surat.fms6.bean.NetworkSettingBean` implements `Serializable`
- **Fields/Constants:**
  - No explicit serialVersionUID declared (missing despite implementing Serializable)
  - `int index` (line 7), `String country` (line 8), `String ssid` (line 9), `String password` (line 10)
- **Public methods:**
  - `getIndex()` (line 12), `setIndex(int)` (line 15)
  - `getCountry()` (line 18), `setCountry(String)` (line 21)
  - `getSsid()` (line 24), `setSsid(String)` (line 27)
  - `getPassword()` (line 30), `setPassword(String)` (line 33)
- **Lines:** 37 total
- **Complexity:** Pure getter/setter bean. **Contains sensitive credential data: plaintext WiFi SSID and password fields with no encryption or masking.**

---

### NotificationSettingsBean.java
- **Class:** `com.torrent.surat.fms6.bean.NotificationSettingsBean` (no Serializable)
- **Fields/Constants:**
  - `String notification_id` (line 5), `String header` (line 6), `String title` (line 7), `String content` (line 8), `String signature` (line 9), `boolean enabled` (line 10)
- **Public methods:**
  - `getNotification_id()` (line 12), `setNotification_id(String)` (line 15)
  - `getHeader()` (line 18), `setHeader(String)` (line 21)
  - `getTitle()` (line 24), `setTitle(String)` (line 27)
  - `getContent()` (line 30), `setContent(String)` (line 33)
  - `getSignature()` (line 36), `setSignature(String)` (line 39)
  - `isEnabled()` (line 42), `setEnabled(boolean)` (line 45)
- **Lines:** 51 total
- **Complexity:** Pure getter/setter bean. Notification template settings.

---

### PreCheckBean.java
- **Class:** `com.torrent.surat.fms6.bean.PreCheckBean` implements `Serializable`
- **Fields/Constants:**
  - `serialVersionUID` = 4412401444144316188L (line 13)
  - `String id` (line 15), `String name` (line 16), `int complete` (line 17), `int incomplete` (line 18), `int total` (line 19)
  - `HashMap<String, Integer> checkMap` (line 20)
  - `String dept_id` (line 23), `String dept_name` (line 24), `int[] checks` (line 25)
  - `ArrayList<PreCheckDriverBean> arrPreCheckDriverBean` (line 26)
- **Public methods:**
  - `addCheckMap(String drivername, int total)` (line 29)
  - `getCheckMap()` (line 33), `setCheckMap(HashMap<String, Integer>)` (line 36)
  - `getName()` (line 40), `setName(String)` (line 43)
  - `getId()` (line 46), `setId(String)` (line 49)
  - `getComplete()` (line 52), `setComplete(int)` (line 55)
  - `getIncomplete()` (line 58), `setIncomplete(int)` (line 61)
  - `getTotal()` (line 64), `setTotal(int)` (line 67)
  - `getDept_id()` (line 70), `setDept_id(String)` (line 73)
  - `getDept_name()` (line 76), `setDept_name(String)` (line 79)
  - `getChecks()` (line 82), `setChecks(int[])` (line 85)
  - `getArrPreCheckDriverBean()` (line 88), `setArrPreCheckDriverBean(ArrayList<PreCheckDriverBean>)` (line 91)
- **Lines:** 97 total
- **Complexity:** Getter/setter bean with `addCheckMap()` method for driver-total aggregation. Contains complete/incomplete tracking for pre-check compliance.

---

### PreCheckDriverBean.java
- **Class:** `com.torrent.surat.fms6.bean.PreCheckDriverBean` implements `Serializable`
- **Fields/Constants:**
  - `serialVersionUID` = 1831899764777810255L (line 10)
  - `int total` (line 12), `String driver_cd` (line 13), `String driver_name` (line 14), `int[] checks` (line 15)
- **Public methods:**
  - `getTotal()` (line 17), `setTotal(int)` (line 20)
  - `getDriver_cd()` (line 23), `setDriver_cd(String)` (line 26)
  - `getDriver_name()` (line 29), `setDriver_name(String)` (line 32)
  - `getChecks()` (line 35), `setChecks(int[])` (line 38)
- **Lines:** 42 total
- **Complexity:** Pure getter/setter bean. Data container for driver pre-check data.

---

### PreCheckSummaryBean.java
- **Class:** `com.torrent.surat.fms6.bean.PreCheckSummaryBean` implements `Serializable`
- **Fields/Constants:**
  - No explicit serialVersionUID declared (missing despite implementing Serializable)
  - `String loc_cd` (line 8), `String loc_name` (line 9)
  - `ArrayList<PreCheckBean> arrPrecheck` (line 10)
  - `int index` (line 11), `int total` (line 12)
- **Public methods:**
  - `getLoc_cd()` (line 15), `setLoc_cd(String)` (line 18)
  - `getLoc_name()` (line 21), `setLoc_name(String)` (line 24)
  - `getArrPrecheck()` (line 27), `setArrPrecheck(ArrayList<PreCheckBean>)` (line 30)
  - `addArrPrecheck(PreCheckBean preCheckBean)` (line 34)
  - `getIndex()` (line 37), `setIndex(int)` (line 40)
  - `getTotal()` (line 43), `setTotal(int)` (line 46)
- **Lines:** 54 total
- **Complexity:** Getter/setter bean with one convenience add method.

---

## Findings

### A02-1 — NetworkSettingBean stores WiFi credentials in plaintext with zero test coverage
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/NetworkSettingBean.java:10`
- **Severity:** CRITICAL
- **Category:** Test Coverage > Security-Sensitive Data Bean
- **Description:** `NetworkSettingBean` stores WiFi network credentials (`ssid` and `password` fields, lines 9-10) as plaintext Strings with no encryption, masking, or access control. The `getPassword()` method (line 30) returns the raw password. There are zero tests verifying that credential data is handled securely, serialized safely, or that password values are not inadvertently logged or exposed. The class also lacks a `serialVersionUID` despite implementing `Serializable`, meaning deserialization could fail across class version changes.
- **Evidence:**
  ```java
  private String ssid = "";
  private String password = "";
  ...
  public String getPassword() {
      return password;
  }
  public void setPassword(String password) {
      this.password = password;
  }
  ```
- **Recommendation:** Write tests that verify: (1) password field is never null after construction, (2) serialization/deserialization round-trip preserves data integrity, (3) `toString()` override (if added) does not leak password. Add `serialVersionUID`. Consider encrypting password at rest. Priority: **Immediate**.

---

### A02-2 — LockOutBean exposes master_code with zero test coverage
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/LockOutBean.java:17`
- **Severity:** CRITICAL
- **Category:** Test Coverage > Security-Sensitive Data Bean
- **Description:** `LockOutBean` contains a `master_code` field (line 17) which appears to be a lockout bypass/master unlock code for fleet vehicles. The getter `getMaster_code()` (line 49) returns this sensitive security code as a plain string. There are zero tests ensuring this sensitive value is handled correctly, cannot be accidentally serialized to logs, or that lockout/unlock time integrity is maintained.
- **Evidence:**
  ```java
  String master_code = "";
  ...
  public String getMaster_code() {
      return master_code;
  }
  public void setMaster_code(String master_code) {
      this.master_code = master_code;
  }
  ```
- **Recommendation:** Write tests verifying: (1) master_code getter/setter contract, (2) serialization behavior of security-sensitive field, (3) lockouttime/unlocktime temporal relationship consistency. Consider whether master_code should be redacted from serialized output.

---

### A02-3 — LicenseBlackListBean with access control fields has zero test coverage
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/LicenseBlackListBean.java:13-16`
- **Severity:** CRITICAL
- **Category:** Test Coverage > Security/Access Control Data Bean
- **Description:** `LicenseBlackListBean` carries access-level authorization fields (`access_level`, `access_cust`, `access_site`, `access_dept`) initialized to `null` (not empty string, unlike other fields), plus blacklist/license data including driver codes and vehicle codes. This bean is a transport for authorization decisions. There are zero tests verifying: field defaults are correct, access_level combinations are valid, or that null vs. empty string semantics are consistent.
- **Evidence:**
  ```java
  private String access_level=null;
  private String access_cust=null;
  private String access_site=null;
  private String access_dept=null;
  private ArrayList<String> vehicleCds;   // initialized to null, not empty list
  ```
- **Recommendation:** Write tests verifying: (1) default null values for access fields vs. empty-string defaults for other fields, (2) vehicleCds null safety -- calling getVehicleCds() returns null unless explicitly set, which may cause NullPointerException downstream, (3) blacklist data integrity when used in access decisions.

---

### A02-4 — ImpactBean complex data structure with addImactMap mutation and zero test coverage
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/ImpactBean.java:47`
- **Severity:** HIGH
- **Category:** Test Coverage > Business Data Bean with Mutation Logic
- **Description:** `ImpactBean` is the most complex bean in this batch (258 lines, 25+ fields). It contains `addImactMap(int month, int impact_no)` (line 47) which mutates an internal `HashMap<Integer, Integer>`. The fixed-size arrays `int[8]` for blueshock/ambershock/redshock and `int[8][3]` for shift variants represent structured business data for vehicle impact monitoring. There are zero tests verifying: (1) addImactMap correctly inserts and overwrites entries, (2) array bounds are respected, (3) the interplay between individual impact counts and aggregated totals. The method name also contains a typo ("Imact" instead of "Impact").
- **Evidence:**
  ```java
  int[] blueshock = new int[8];
  int[][] blueshockShift = new int[8][3];
  HashMap<Integer, Integer> impactMap = new HashMap<Integer, Integer>();

  public void addImactMap(int month, int impact_no) {
      impactMap.put(month, impact_no);
  }
  ```
- **Recommendation:** Write tests for: (1) `addImactMap` -- add, overwrite, boundary month values (0, 12, negative, Integer.MAX_VALUE), (2) default array sizes and initial values, (3) serialization round-trip with populated arrays and maps, (4) edge case where `impacts` field is null vs. initialized.

---

### A02-5 — PreCheckBean with addCheckMap aggregation logic has zero test coverage
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/PreCheckBean.java:29`
- **Severity:** HIGH
- **Category:** Test Coverage > Business Data Bean with Mutation Logic
- **Description:** `PreCheckBean` contains `addCheckMap(String drivername, int total)` (line 29) which aggregates pre-check completion data by driver name into an internal `HashMap<String, Integer>`. The bean also tracks `complete`, `incomplete`, and `total` counts for fleet pre-check compliance. Zero tests exist for: (1) the addCheckMap mutation, (2) consistency between complete + incomplete = total, (3) behavior with duplicate driver names, (4) null driver name handling.
- **Evidence:**
  ```java
  HashMap<String, Integer> checkMap = new HashMap<String, Integer>();

  public void addCheckMap(String drivername, int total) {
      checkMap.put(drivername, total);
  }
  ```
- **Recommendation:** Write tests for: (1) addCheckMap with null key, duplicate keys, empty string keys, (2) complete/incomplete/total arithmetic invariants, (3) interaction between checks array and the PreCheckDriverBean list.

---

### A02-6 — MymessagesUsersBean carries user identity data with zero test coverage
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/MymessagesUsersBean.java:16-17`
- **Severity:** HIGH
- **Category:** Test Coverage > User Identity Data Bean
- **Description:** `MymessagesUsersBean` stores user identity information (`user_id`, `user_email`) and notification threshold configurations. This data is used for messaging/notification features. Zero tests verify: (1) user_email format handling, (2) threshold value semantics (stored as String, not numeric), (3) serialization of user PII data. Also contains field name typo `descrption` (line 18, missing 'i').
- **Evidence:**
  ```java
  String user_id = "";
  String user_email = "";
  String descrption = "";   // typo: should be "description"
  String threshold = "";    // stored as String, not a numeric type
  ```
- **Recommendation:** Write tests for: (1) getter/setter round-trip for all fields, (2) threshold stored as String -- verify downstream consumers parse correctly, (3) serialization of user PII.

---

### A02-7 — Impact hierarchy beans (ImpactLocBean, ImpactDeptBean, ImpactSummaryBean) untested aggregation
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/ImpactLocBean.java:50`
- **Severity:** MEDIUM
- **Category:** Test Coverage > Aggregation/Report Data Beans
- **Description:** Three beans form a hierarchical data structure for impact reporting: `ImpactLocBean` -> `ImpactDeptBean` -> `ImpactSummaryBean` -> `ImpactBean`. Each level has convenience `add` methods (`addArrImpactDeptBean` at ImpactLocBean:50, `addArrImpact` at ImpactSummaryBean:40) and `total` fields for aggregate counts. Zero tests verify: (1) the add methods correctly append to internal lists, (2) total fields are consistent with child counts, (3) the hierarchical structure integrity. `ImpactSummaryBean` is also missing `serialVersionUID` despite implementing Serializable.
- **Evidence:**
  ```java
  // ImpactLocBean.java:50
  public void addArrImpactDeptBean(ImpactDeptBean impactDeptBean) {
      this.arrImpactDeptBean.add(impactDeptBean);
  }
  // ImpactSummaryBean.java:40
  public void addArrImpact(ImpactBean impactBean) {
      this.arrImpact.add(impactBean);
  }
  ```
- **Recommendation:** Write integration-level tests that build the full hierarchy (Loc -> Dept -> Summary -> Impact), verify add methods, and check that totals at each level can be reconciled.

---

### A02-8 — PreCheck hierarchy beans (PreCheckSummaryBean, PreCheckDriverBean) untested aggregation
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/PreCheckSummaryBean.java:34`
- **Severity:** MEDIUM
- **Category:** Test Coverage > Aggregation/Report Data Beans
- **Description:** `PreCheckSummaryBean` aggregates `PreCheckBean` instances by location, with `addArrPrecheck()` (line 34) adding pre-checks. `PreCheckDriverBean` provides driver-level detail. Zero tests verify: (1) addArrPrecheck correctly builds the list, (2) totals are consistent across the hierarchy, (3) the checks int[] array in both PreCheckBean and PreCheckDriverBean is properly initialized before use (defaults to null). `PreCheckSummaryBean` is missing `serialVersionUID` despite implementing Serializable.
- **Evidence:**
  ```java
  // PreCheckSummaryBean.java
  public void addArrPrecheck(PreCheckBean preCheckBean) {
      this.arrPrecheck.add(preCheckBean);
  }
  // PreCheckDriverBean.java -- checks defaults to null
  int[] checks = null;
  ```
- **Recommendation:** Write tests for: (1) addArrPrecheck with null argument, (2) null checks array access patterns, (3) serialization with null checks field.

---

### A02-9 — MaxHourUsageBean and FleetCheckBean report data beans with zero test coverage
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/MaxHourUsageBean.java:36`
- **Severity:** MEDIUM
- **Category:** Test Coverage > Report Data Beans
- **Description:** `MaxHourUsageBean` aggregates unit utilization data with `addArrUnitUtil()` (line 36). `FleetCheckBean` stores fleet check results including frequently-failed questions. Both serve report generation. Zero tests verify their data contracts or the add method behavior.
- **Evidence:**
  ```java
  // MaxHourUsageBean.java:36
  public void addArrUnitUtil(UnitutilBean unitutilBean) {
      this.arrUnitUtil.add(unitutilBean);
  }
  // FleetCheckBean.java -- frequent_failed_question exposed as mutable ArrayList
  public ArrayList<String> getFrequent_failed_question() {
      return frequent_failed_question;
  }
  ```
- **Recommendation:** Write tests for: (1) addArrUnitUtil with null argument, (2) FleetCheckBean's mutable list exposure -- callers can modify internal state via the returned reference.

---

### A02-10 — MenuBean stores navigation paths with zero test coverage
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/MenuBean.java:11`
- **Severity:** MEDIUM
- **Category:** Test Coverage > Navigation/Configuration Bean
- **Description:** `MenuBean` stores menu navigation configuration including `Form_Path` and `ReskinPath` which are URL/path values used for navigation routing. Malformed or manipulated path values could lead to open redirect or path traversal issues. Zero tests verify path value handling or sanitization.
- **Evidence:**
  ```java
  private String Form_Path ="";
  private String ReskinPath ="";
  ```
- **Recommendation:** Write tests verifying: (1) getter/setter contracts, (2) path values are used downstream without modification -- document expected format.

---

### A02-11 — EntityBean simple data bean with zero test coverage
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/EntityBean.java`
- **Severity:** LOW
- **Category:** Test Coverage > Simple Data Bean
- **Description:** `EntityBean` is a simple Serializable data bean with 6 fields (id, name, totalno, attribute, locs, depts) and only getter/setter methods. Zero tests exist, but the class contains no business logic beyond property storage.
- **Evidence:** 55 lines, 12 public methods (all getters/setters), no logic.
- **Recommendation:** Low priority. Write basic round-trip getter/setter tests and serialization tests if time permits.

---

### A02-12 — NotificationSettingsBean simple data bean with zero test coverage
- **File:** `WEB-INF/src/com/torrent/surat/fms6/bean/NotificationSettingsBean.java`
- **Severity:** LOW
- **Category:** Test Coverage > Simple Data Bean
- **Description:** `NotificationSettingsBean` is a simple data bean with notification template fields and an `enabled` boolean. Zero tests exist. No complex logic.
- **Evidence:** 51 lines, 12 public methods (all getters/setters), boolean enabled field.
- **Recommendation:** Low priority. Write basic getter/setter tests and verify boolean default (false).

---

## Summary Table

| ID | File | Severity | Category |
|----|------|----------|----------|
| A02-1 | NetworkSettingBean.java | CRITICAL | Security - Plaintext Credentials |
| A02-2 | LockOutBean.java | CRITICAL | Security - Master Code Exposure |
| A02-3 | LicenseBlackListBean.java | CRITICAL | Security - Access Control Data |
| A02-4 | ImpactBean.java | HIGH | Business Logic - HashMap Mutation |
| A02-5 | PreCheckBean.java | HIGH | Business Logic - Aggregation |
| A02-6 | MymessagesUsersBean.java | HIGH | User Identity - PII Data |
| A02-7 | ImpactLocBean/DeptBean/SummaryBean | MEDIUM | Report - Hierarchy Aggregation |
| A02-8 | PreCheckSummaryBean/DriverBean | MEDIUM | Report - Hierarchy Aggregation |
| A02-9 | MaxHourUsageBean/FleetCheckBean | MEDIUM | Report - Data Beans |
| A02-10 | MenuBean.java | MEDIUM | Navigation - Path Configuration |
| A02-11 | EntityBean.java | LOW | Simple Data Bean |
| A02-12 | NotificationSettingsBean.java | LOW | Simple Data Bean |

**Total findings:** 12
**CRITICAL:** 3 | **HIGH:** 3 | **MEDIUM:** 4 | **LOW:** 2
**Overall test coverage:** 0% (zero test files exist in repository)
