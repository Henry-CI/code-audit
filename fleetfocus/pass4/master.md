# Pass 4 — Code Quality: master package
**Agent:** A15
**Date:** 2026-02-25
**Repo:** fleetfocus
**Branch:** `release/UAT_RELEASE_FLEETFOCUS_Production`
**Base path:** `WEB-INF/src/com/torrent/surat/fms6/master/`

---

## Reading Evidence

### Databean_customer.java
- **Class:** `Databean_customer` (3,009 lines, line 30) — no `implements Serializable`
- **Public methods:**
  - `getCurrent_User_Site_Name()` (line 189), `getCurrent_User_Dept_Name()` (line 193)
  - `getLicense_document_url()` (line 197), `setLicense_document_url(ArrayList)` (line 200)
  - `getCurrent_User_Dept_Cds()` (line 205), `setCurrent_User_Dept_Cds(ArrayList)` (line 209)
  - `getCurrent_User_Dept_Names()` (line 213), `setCurrent_User_Dept_Names(ArrayList)` (line 217)
  - `getLicenceFile()` (line 229), `setLicenceFile(String)` (line 232)
  - `getDriverType()` (line 236), `setDriverType(String)` (line 240)
  - `query(String op_code)` (line 331)
  - `getView_Batt_Name()` (line 542), `getView_Batt_Desc()` (line 543), `getView_Batt_CD()` (line 544), `getReskinPathB()` (line 545)
  - `Query_Viewable_Battery()` (line 547)
  - `getView_Settings_Name()` (line 573), `getView_Settings_Desc()` (line 574), `getView_Settings_CD()` (line 575), `getReskinPathDS()` (line 576)
  - `Query_Viewable_Settings()` (line 578)
  - `Query_Viewable_Reports()` (line 600)
  - `getView_Report_Name()` (line 617), `getView_Report_Desc()` (line 618), `getView_Report_CD()` (line 619), `getReskinPath()` (line 620)
  - `Query_Viewable_Menu()` (line 634)
  - `getView_Dashmenu_CD()` (line 704), `getView_Dashmenu_Name()` (line 705), `getView_Dashmenu_Desc()` (line 706), `getView_Dashmenu_Icon()` (line 707), `getView_Dashmenu_FCD()` (line 708)
  - `getUser_Form_Menu_CD()` (line 717), `getUser_Form_Menu_Name()` (line 718), `getUser_Form_Menu_View()` (line 719), `getUser_Form_Menu_Edit()` (line 720), `getUser_Form_Menu_Delete()` (line 721), `getUser_Form_Menu_Print()` (line 722), `getFormPath()` (line 723)
  - `Query_User_Form_Menu()` (line 725)
  - `getUserDepMap()` (line 773), `setUserDepMap(Map)` (line 776)
  - `getUserModMap()` (line 779), `setUserModMap(Map)` (line 782)
  - `getUserVehMap()` (line 785), `setUserVehMap(Map)` (line 788)
  - `getVam_ctr()` (line 791), `setVam_ctr(int)` (line 794)
  - `getVehCdList()` (line 800)
  - `queryBlacklist()` (line 804)
  - `getSupervisor_user_cds()` (line 831), `getSupervisor_user_names()` (line 834), `getSupervisor_slot_nos()` (line 837)
  - `isCurrent_User_Is_Supervisor()` (line 840)
  - `getSupervisor_List_user_cds()` (line 844), `setSupervisor_List_user_cds(ArrayList)` (line 848)
  - `getSupervisor_List_user_names()` (line 853), `setSupervisor_List_user_names(ArrayList)` (line 857)
  - `getSupervisor_List_slot_nos()` (line 862), `setSupervisor_List_slot_nos(ArrayList)` (line 866)
  - `querySupervisorList()` (line 871)
  - `Query_User_Access_Restriction()` (line 957)
  - `getUnder_Dept_Cd()` (line 1016), `setUnder_Dept_Cd(ArrayList)` (line 1019)
  - `getUnder_Dept_Nm()` (line 1022), `setUnder_Dept_Nm(ArrayList)` (line 1025)
  - `Query_All_Models_By_Cus_Loc_Dept()` (line 1029), `Query_All_Models_By_Cus_Loc_Dept_va()` (line 1163)
  - `Query_Current_Alert()` (line 1246), `Query_Alerts()` (line 1289)
  - `Query_Groups_By_Cust()` (line 1387), `Query_Access_Groups()` (line 1430)
  - `getCurrent_User_Weig_Id()` (line 1465), `setCurrent_User_Weig_Id(String)` (line 1468)
  - `Query_Current_User()` (line 1472)
  - `Query_All_Models()` (line 1696)
  - `Query_Driver_License()` (line 1713), `getLicenceNumber()` (line 1739), `setLicenceNumber(String)` (line 1742)
  - `Query_Driver_License_au()` (line 1745)
  - `Query_CustomersUsers()` (line 1763), `Query_Customers()` (line 1792), `Query_all_Customers()` (line 1835)
  - `Query_Locations()` (line 1871), `Query_Locations_Old()` (line 1937)
  - `QueryEditUserDepartments()` (line 1967), `Query_Departments()` (line 1992)
  - `Query_User()` (line 2028), `Query_Permits()` (line 2049)
  - `getPermits_Form_Cd()` (line 2071), `getPermit_Edit_Count()` (line 2072), `getPermits_View()` (line 2073), `getPermits_Edit()` (line 2074), `getPermits_Delete()` (line 2075), `getPermits_Export()` (line 2076)
  - `Query_Users()` (line 2078), `Query_Users_xls()` (line 2327)
  - `Query_My_profile()` (line 2567), `Query_Customer_Data()` (line 2600)
  - `setUser_cd(String)` (line 2715)
  - ~80 additional getter/setter methods (lines 2717–2998)
  - `Query_Bonus_Module()` (line 2960)
  - `getCust_cd()` (line 2991), `setCust_cd(String)` (line 2994)
  - `getCurrent_User_is_technician()` (line 2998), `getCurrent_User_is_transport()` (line 3001)
- **Commented-out code blocks:** Lines 353, 382–383, 388, 412, 443–444, 456, 603, 637–650, 671, 728, 736, 754, 1083–1088, 1105, 1121, 1129, 1150, 1154, 1157, 1231, 1242, 1419, 1542, 1619, 1658, 1778, 1817, 1823, 1910, 1911–1918, 1984, 2082, 2119, 2240, 2330, 2636, 2647, 2705

### Databean_getter.java
- **Class:** `Databean_getter` (5,470 lines, line 41) — no `implements Serializable`
- **Public methods:**
  - `getType()` (line 160), `setType(String)` (line 164)
  - `getFms_Vehicle_Data_CAN_UNITS()` (line 168), `setFms_Vehicle_Data_CAN_UNITS(String)` (line 172)
  - `getFms_Vechile_Data_CANRULE()` (line 186), `setFms_Vechile_Data_CANRULE(String)` (line 190)
  - `getFms_Vechile_Data_MK3_Version()` (line 196), `setFms_Vechile_Data_MK3_Version(Boolean)` (line 200)
  - `getFms_Vehicle_NETWORK_Setttings()` (line 206), `setFms_Vehicle_NETWORK_Setttings(ArrayList)` (line 210)
  - `getFms_Vehicle_DATA_LOW_UTIL()` (line 216), `setFms_Vehicle_DATA_LOW_UTIL(String)` (line 220)
  - `getFms_Vehicle_Data_ON_HIRE()` (line 224), `setFms_Vehicle_Data_ON_HIRE(String)` (line 228)
  - `getFms_Vehicle_Data_hourly_rate()` (line 232), `setFms_Vehicle_Data_hourly_rate(String)` (line 236)
  - `getFms_Vehicle_Data_max_monthly_rate()` (line 240), `setFms_Vehicle_Data_max_monthly_rate(String)` (line 244)
  - `getFms_Vehicle_Dehire_Time()` (line 341), `setFms_Vehicle_Dehire_Time(ArrayList)` (line 345)
  - `getFms_Vehicle_Hire_Time()` (line 351), `setFms_Vehicle_Hire_Time(ArrayList)` (line 355)
  - `getFms_Vehicle_Lockout()` (line 359), `setFms_Vehicle_Lockout(ArrayList)` (line 363)
  - `getFms_Vehicle_List_CCID()` (line 397), `setFms_Vehicle_List_CCID(ArrayList)` (line 401)
  - `getFms_Vehicle_List_Last_Session()` (line 406), `getFms_Vehicle_List_Color()` (line 410), `getFms_Vehilce_List_Sm_enabled()` (line 414)
  - `getFms_Vehicle_List_MK3_Version()` (line 423), `setFms_Vehicle_List_MK3_Version(ArrayList)` (line 427)
  - `getFms_Vehicle_List_Product_Type()` (line 431), `setFms_Vehicle_List_Product_Type(ArrayList)` (line 435)
  - `getFrms_Vechile_List_CAN()` (line 440), `setFrms_Vechile_List_CAN(ArrayList)` (line 444)
  - `query(String op_code)` (line 474)
  - `Query_Vehicle_Diagnostic()` (line 872), `queryVehicleCanbusDataDetails()` (line 1097)
  - `getSpareModules()` (line 1179), `setSpareModules(ArrayList)` (line 1183)
  - `getSpareModulesHistory()` (line 1187), `setSpareModulesHistory(ArrayList)` (line 1191)
  - `Query_Spare_Modules()` (line 1196), `Query_Spare_Modules_Form()` (line 1248)
  - `getFms_Spare_Modules_Cd()` (line 1289), `setFms_Spare_Modules_Cd(String)` (line 1293)
  - `getFms_Spare_Status_Cd()` (line 1297), `setFms_Spare_Status_Cd(ArrayList)` (line 1301)
  - `getFms_Spare_Status()` (line 1305), `setFms_Spare_Status(ArrayList)` (line 1309)
  - `getSpareModule()` (line 1313), `setSpareModule(SpareModuleBean)` (line 1317)
  - `Query_All_Spare_Modules_Status()` (line 1321), `Query_All_Spare_Modules()` (line 1332), `Query_Spare_Modules_History()` (line 1350)
  - `getShow_assigned()` (line 1382), `setShow_assigned(String)` (line 1386)
  - `getUser_Form_Menu_CD()` (line 1437) through `getFormPath()` (line 1443)
  - `getBlue_scale()` (line 1497), `setBlue_scale(double)` (line 1501)
  - `getAmber_scale()` (line 1505), `setAmber_scale(double)` (line 1509)
  - `getRed_scale()` (line 1513), `setRed_scale(double)` (line 1517)
  - `getVs_status()` (line 1536), `setVs_status(String)` (line 1540)
  - Various `getVehicle_Complete_*` methods (lines 1616–1640)
  - `getMcDriverMap()` (line 2034), `getsMcDriverMap()` (line 2037), `setMcDriverMap(Map)` (line 2042)
  - `getCan_setting_id()` (line 3309), `setCan_setting_id(ArrayList)` (line 3313)
  - `getCan_setting_desc()` (line 3317), `setCan_setting_desc(ArrayList)` (line 3321)
  - `getFimwarearraylist()` (line 3327), `setFimwarearraylist(ArrayList)` (line 3331)
  - Various `getFirmware_*` / `setFirmware_*` methods (lines 3456–3486)
  - `getFirm_ver()` (line 3565), `setFirm_ver(String)` (line 3569)
  - `getFirm_vers()` (line 3573), `setFirm_vers(ArrayList)` (line 3577)
  - `getFirm_ver_mk3()` (line 3582), `setFirm_ver_mk3(String)` (line 3586)
  - `Query_Customers_Locations()` (line 3865), `Query_Departments()` (line 3948)
  - `Query_Vehicle_Types()` (line 4013), `Query_Vehicle_Tags()` (line 4042)
  - `Query_Vehicle_Rel()` (line 4097), `Query_Vehicle_Data()` (line 4126)
  - `Query_Pbh_Data()` (line 4259)
  - `getPBH_hourly_rate()` (line 4278), `setPBH_hourly_rate(ArrayList)` (line 4282)
  - `getPBH_max_monthly_rate()` (line 4286), `setPBH_max_monthly_rate(ArrayList)` (line 4290)
  - `Query_Vehicle_Network_Data()` (line 4294)
  - `Query_Checklist()` (line 4320), `Query_Questions()` (line 4416), `Query_By_Cd_Questions()` (line 4511)
  - `Query_Permits()` (line 4544)
  - `getPermits_Form_Cd()` (line 4571) through `getPermits_Export()` (line 4576)
  - `gettesting()` (line 4580)
  - ~100+ getter/setter methods (lines 4585–4990)
  - `clearVectors()` (line 4991)
  - `Query_All_Drivers_By_Cus_Loc_Dept()` (line 5172)
  - `getSpecialUsers()` (line 5243)
  - Remaining getter/setters (lines 5284–5466)
- **Commented-out code blocks:** Lines 78, 611, 614, 617, 632–633, 644–648, 670, 729, 898, 1224, 1260, 1546, 1556, 1564–1565, 1789, 1802–1819, 1835, 1850–1852, 1858–1865, 1969, 2289, 2685, 2699, 2929–2931, 2961–2963, 3047, 3231, 3386, 4113, 4256, 4346, 4413, 4439, 4530, 4547, 5185, 5278

### Databean_getuser.java
- **Class:** `Databean_getuser` (10,675 lines, line 28) — no `implements Serializable`
- **Public methods:**
  - `clear_variables()` (line 464)
  - `getP_id()` (line 990), `setP_id(ArrayList)` (line 994)
  - `getBatt_id()` (line 998), `setBatt_id(ArrayList)` (line 1002)
  - `getFleet_no()` (line 1006), `setFleet_no(ArrayList)` (line 1010)
  - `getMail_grp_cd()` (line 1727), `setMail_grp_cd(ArrayList)` (line 1731)
  - `getMail_grp_nm()` (line 1735), `setMail_grp_nm(ArrayList)` (line 1739)
  - `getMail_grp_lst()` (line 1743), `setMail_grp_lst(ArrayList)` (line 1747)
  - `getMail_grp_cust()` (line 1751), `setMail_grp_cust(ArrayList)` (line 1755)
  - `getMail_grp_cust_nm()` (line 1759), `setMail_grp_cust_nm(ArrayList)` (line 1763)
  - `getMail_group_cust_nm()` (line 1767), `setMail_group_cust_nm(String)` (line 1771)
  - `getSiteHourMessage()` (line 2018), `setSiteHourMessage(String)` (line 2022)
  - `getBlockedVehList()` (line 3439), `setBlockedVehList(ArrayList<String>)` (line 3443)
  - `convertToArrayString(Object[])` (line 3447) — static
  - `gettest()` (line 4106)
  - `Query_Current_User()` (line 5383)
  - `isTechLockoutSupportFw()` (line 5634), `setTechLockoutSupportFw(boolean)` (line 5638)
  - `getVor_setting()` (line 5642), `getNote()` (line 5647), `setVor_setting(Boolean)` (line 5651)
  - `getVs_status()` (line 5655), `setVs_status(String)` (line 5659)
  - `getDangerTagStatus()` (line 5663), `setDangerTagStatus(String)` (line 5667)
  - `isDangerTagSet()` (line 5671), `setDangerTagSet(boolean)` (line 5675)
  - `getDangerTagNote()` (line 5679), `setDangerTagNote(String)` (line 5683)
  - `getFull_lockout_enabled()` (line 5850), `getFull_lockout_timeout()` (line 5854)
  - `getFms_Vehicle_DATA_LOW_UTIL()` (line 5858)
  - `setParam_Module(String)` (line 5914)
  - `getCurrent_User_Customer_Cd()` (line 5921), `setCurrent_User_Customer_Cd(String)` (line 5925)
  - `getCurrent_User_Site_Cd()` (line 5929), `setCurrent_User_Site_Cd(String)` (line 5933)
  - `getCurrent_User_Department_Cd()` (line 5937), `setCurrent_User_Department_Cd(String)` (line 5941)
  - `getParam_User()` (line 5945), `setParam_User(String)` (line 5949)
  - `setAccess_user(String)` (line 5954)
  - `getUser_Form_Menu_CD()` (line 5963) through `getFormPath()` (line 5969)
  - `Query_User_Form_Menu()` (line 5971)
  - `Query_Permits()` (line 6014), `QueryUnlkSettings()` (line 6026)
  - `getPermits_Form_Cd()` (line 6037)
  - `init()` (line 7880) — main dispatcher, ~1100 lines with 80+ branches
  - `QuerySFTPSettings()` (line 9018)
  - ~200 additional getter/setter methods (lines 9091–10675)
- **Commented-out code blocks:** Lines 771–783, 796, 810–812, 819, 837–839, 922–923, 1032–1033, 2028, 2031, 2050, 2328, 3143–3154, 3397, 3427–3431, 3631–3642, 3747–3758, 4056–4066, 4257

### Databean_user.java
- **Class:** `Databean_user` (46 lines, line 29) — no `implements Serializable`
- **Public methods:** None. Zero methods of any kind.
- **Fields (all private):** `conn`, `stmt`, `stmt1`, `stmt2`, `rset`, `rset1`, `rset2`, `methodName`, `query`, `queryString`
- **Commented-out code blocks:** None

### FirmwareverBean.java
- **Class:** `FirmwareverBean` (255 lines, line 3) — no `implements Serializable`
- **Public methods:**
  - `getVeh_id()` (line 14), `setVeh_id(String)` (line 18)
  - `getGmtp_id()` (line 22), `setGmtp_id(String)` (line 26)
  - `getFirm_vers()` (line 30), `setFirm_vers(String)` (line 34)
  - `setCurr_ver(String version)` (line 38)
  - `setCurr_ver_edit(String version)` (line 51)
  - `setCurr_ver()` (line 56) — no-arg overload
  - `getRep_time()` (line 61), `setRep_time(String)` (line 65)
  - `getHire_no()` (line 69), `setHire_no(String)` (line 73)
  - `getType()` (line 77), `setType(String)` (line 81)
  - `getCurr_ver()` (line 85)
  - `getType(String version)` (line 211) — overloaded
  - `getMk3dbg()` (line 245), `setMk3dbg(String)` (line 249)
- **Commented-out code blocks:** Lines 104–165 (large block of switch statements inside `convert32bit()`)

### Frm_saveuser.java
- **Class:** `Frm_saveuser extends HttpServlet implements SingleThreadModel` (10,931 lines, line 35) — `@SuppressWarnings("deprecation")` on line 34
- **Public methods:**
  - `doPost(HttpServletRequest, HttpServletResponse)` (line 54)
  - `clearVectors()` (line 449) — empty body
  - `isValidEmailAddress(String email)` (line 5199) — reported in pass3; confirmed accessible
- **All remaining ~70 methods are `private`** (save_group, save_division, save_department, save_new_vehicle, etc.)
- **Commented-out code blocks:** Pervasive — scattered System.out.println debug statements, alternative SQL queries, and test strings throughout

### Frm_upload.java
- **Class:** `Frm_upload extends HttpServlet` (163 lines, line 26)
- **Public methods:**
  - `init()` (line 46)
  - `doPost(HttpServletRequest, HttpServletResponse)` (line 69)
  - `clearVectors()` (line 102) — empty body
- **Commented-out code blocks:** None

---

## Findings

### A15-01 — SQL Injection: All queries use string concatenation across entire package
- **File:** All files containing SQL: `Databean_customer.java`, `Databean_getter.java`, `Databean_getuser.java`, `Frm_saveuser.java`, `Frm_upload.java`
- **Severity:** CRITICAL
- **Category:** Security > SQL Injection
- **Description:** Every SQL query across the entire `master` package is constructed via string concatenation with externally-set field values (`Param_User`, `Param_Customer`, `Param_Search`, `set_cust_cd`, `vehicle_cd`, etc.). None of the approximately 200+ queries use `PreparedStatement` with parameterized bindings. User-supplied search terms are directly interpolated into LIKE clauses. This is a systemic SQL injection vulnerability across ~30,000 lines of code.
- **Evidence:**
  ```java
  // Databean_customer.java line 551
  query = "... AND \"FMS_USR_MST\".\"USER_CD\" ='"+Param_User+"' AND ...";

  // Databean_customer.java line 2212
  query = query + " AND (\"FMS_USR_MST\".\"USER_NAME\" ilike '%"+Param_Search+"%' ...";

  // Databean_getter.java line 2377
  cond_relation = cond_relation + " r.\"VEHICLE_CD\" in ( SELECT distinct(\"VEHICLE_CD\") FROM \"FMS_VEHICLE_MST\" WHERE \"FMS_VEHICLE_MST\".\"VEHICLE_ID\" LIKE '%"+Param_Search+"%' ...";

  // Databean_getuser.java line 1890
  search_str = " and (lower(\"CONTACT_LAST_NAME\") like lower('" + set_sc + "%') ...";

  // Frm_saveuser.java line 1281+ (all save_ methods)
  query = "INSERT INTO ... VALUES ('" + request.getParameter("group_name") + "', ...)";
  ```
- **Recommendation:** Replace all `Statement` + string concatenation with `PreparedStatement` and `?` parameter placeholders. Prioritize user-facing search parameters (`Param_Search`, `set_sc`) and all `save_*` methods in `Frm_saveuser`.

### A15-02 — God Class: 4 of 7 files exceed 3,000 lines
- **File:** `Databean_getuser.java` (10,675 lines), `Frm_saveuser.java` (10,931 lines), `Databean_getter.java` (5,470 lines), `Databean_customer.java` (3,009 lines)
- **Severity:** CRITICAL
- **Category:** Code Quality > Architecture > God Class
- **Description:** Four classes are massive monoliths. `Databean_getuser` contains 400+ fields, 80+ `Fetch_*` methods, and a 1,100-line `init()` dispatcher with 80+ string-matching branches. `Frm_saveuser` has ~70 private `save_*` methods dispatched from a 393-line `doPost()`. `Databean_getter` has 200+ fields and 100+ methods with a 400-line `query()` dispatcher. `Databean_customer` has 100+ fields and a `query()` dispatcher with 20+ branches. Each class handles customers, users, vehicles, alerts, firmware, licensing, menus, and more.
- **Evidence:**
  ```java
  // Databean_getuser.java line 7880 — init() dispatcher
  if (set_op_code.equalsIgnoreCase("group_add")) { ... }
  if (set_op_code.equalsIgnoreCase("group_rel_add")) { ... }
  // ~80 more if-branches over 1,100 lines

  // Databean_getter.java line 474 — query() dispatcher
  if(op_code.equalsIgnoreCase("syncronize")) { ... }
  else if(op_code.equalsIgnoreCase("new_vehicle_page")) { ... }
  // ~30 more branches

  // Databean_customer.java line 331 — query() dispatcher
  if(op_code.equalsIgnoreCase("view_customer")) { ... }
  // ~20 more branches
  ```
- **Recommendation:** Decompose each class into focused domain services (e.g., `CustomerRepository`, `UserRepository`, `VehicleRepository`, `AlertService`, `FirmwareService`). Replace string-based dispatch with a strategy/command pattern or `Map<String, Runnable>`.

### A15-03 — Password exposed as package-private field and via public getter
- **File:** `Databean_customer.java`:1480,1535,2838 and `Databean_getuser.java`:226,1374
- **Severity:** CRITICAL
- **Category:** Security > Sensitive Data Exposure
- **Description:** `Databean_customer.Query_Current_User()` reads the `PASSWORD` column from the database (line 1480, column 3) and stores it in `Current_User_Password` (line 1535), then exposes it via the public getter `getCurrent_User_Password()` (line 2838). Similarly, `Databean_getuser` stores the password in the package-private field `usr_pwd` (line 226), populated from database at line 1374.
- **Evidence:**
  ```java
  // Databean_customer.java line 1480 (SQL)
  + "\"FMS_USR_MST\".\"PASSWORD\", "  // column 3

  // Databean_customer.java line 1535
  Current_User_Password = rset.getString(3);

  // Databean_customer.java line 2838
  public String getCurrent_User_Password() {return Current_User_Password;}

  // Databean_getuser.java line 226 (package-private!)
  String usr_pwd = "";
  ```
- **Recommendation:** Remove the `PASSWORD` column from all SELECT queries. Never expose passwords through bean getters or package-private fields. Delegate authentication to a dedicated security service.

### A15-04 — NullPointerException bug: `null && .equalsIgnoreCase()`
- **File:** `Databean_customer.java`:1814,1854
- **Severity:** CRITICAL
- **Category:** Code Quality > Bug
- **Description:** In both `Query_Customers()` and `Query_all_Customers()`, the null check uses `&&` instead of `||`. If `Param_Search` is null, the expression `Param_Search == null && Param_Search.equalsIgnoreCase("")` will throw a NullPointerException because the right-hand side evaluates `.equalsIgnoreCase()` on a null reference. The logic should use `||` since a value cannot simultaneously be null and equal to empty string.
- **Evidence:**
  ```java
  // Databean_customer.java line 1814
  if( Param_Search == null && Param_Search.equalsIgnoreCase("")) {
      search_query = query_customers;
  }

  // Databean_customer.java line 1854
  if( Param_Search == null && Param_Search.equalsIgnoreCase("")) {
      search_query = query_customers;
  }
  ```
- **Recommendation:** Fix to `Param_Search == null || Param_Search.isEmpty()`.

### A15-05 — Package-private field visibility across all data beans
- **File:** `Databean_customer.java`:46–316, `Databean_getter.java`:56–472, `Databean_getuser.java`:98–456
- **Severity:** HIGH
- **Category:** Code Quality > Leaky Abstractions
- **Description:** The vast majority of fields across all three data beans (estimated 600+ fields total) are declared with default (package-private) visibility. Only a handful are `private`. This exposes all mutable state — including database connections, SQL strings, user passwords, and hundreds of ArrayList collections — to any class in the same package.
- **Evidence:**
  ```java
  // Databean_customer.java lines 46-47
  String debug = "";
  String user_cd = "";

  // Databean_getter.java lines 56-58
  Boolean result = true;
  String vehicle_cd = "";

  // Databean_getuser.java lines 98-100
  ArrayList group_cd = new ArrayList();
  ArrayList group_nm = new ArrayList();

  // Databean_getuser.java line 226 — password!
  String usr_pwd = "";
  ```
- **Recommendation:** Declare all fields `private`. Expose controlled access through getters/setters only where needed.

### A15-06 — Raw type ArrayList usage: 300+ unparameterized collections
- **File:** `Databean_customer.java`:61–316, `Databean_getter.java`:87–460, `Databean_getuser.java`:98–456
- **Severity:** HIGH
- **Category:** Code Quality > Build Warnings > Raw Types
- **Description:** Over 300 `ArrayList` fields across the three data beans are declared without generic type parameters (raw types). This generates compiler warnings and defeats compile-time type safety. A handful of fields do use generics (e.g., `ArrayList<Boolean>`, `ArrayList<DayhoursBean>`), creating inconsistency.
- **Evidence:**
  ```java
  // Databean_customer.java line 61
  ArrayList Customer_Sites_Name = new ArrayList();

  // Databean_getter.java line 87
  ArrayList Linde_location_cd = new ArrayList();

  // Databean_getuser.java line 98
  ArrayList group_cd = new ArrayList();

  // Contrast with typed usage:
  // Databean_customer.java line 133
  ArrayList<Boolean> User_is_supermaster = new ArrayList();
  ```
- **Recommendation:** Add appropriate generic type parameters to all collections (e.g., `ArrayList<String>`, `List<Integer>`). Use the `List` interface instead of the concrete `ArrayList` class.

### A15-07 — Mutable internal collections returned directly from getters
- **File:** `Databean_customer.java`:197–2928, `Databean_getter.java`:341–5466, `Databean_getuser.java`:990–10675
- **Severity:** HIGH
- **Category:** Code Quality > Leaky Abstractions
- **Description:** Every getter for `ArrayList`, `HashMap`, and `Map` fields across all three data beans returns a direct reference to the internal mutable collection. External callers can add, remove, or modify entries without going through the bean's API. Estimated 200+ such getters.
- **Evidence:**
  ```java
  // Databean_customer.java line 197
  public ArrayList getLicense_document_url() { return License_document_url; }

  // Databean_getter.java line 397
  public ArrayList getFms_Vehicle_List_CCID() { return Fms_Vehicle_List_CCID; }

  // Databean_getuser.java line 990
  public ArrayList getP_id() { return P_id; }
  ```
- **Recommendation:** Return unmodifiable views (`Collections.unmodifiableList(...)`) or defensive copies.

### A15-08 — Shared mutable JDBC state stored as instance fields
- **File:** `Databean_customer.java`:31–37, `Databean_getter.java`:43–53, `Databean_getuser.java`:29–35
- **Severity:** HIGH
- **Category:** Code Quality > Architecture > Thread Safety
- **Description:** All three data beans store `Connection`, `Statement` (×3), `ResultSet` (×3), and query strings as instance fields. Methods reuse and overwrite these fields across deeply nested call chains. In `Databean_getuser`, the outer loop uses `rset` and `query`, while inner loops overwrite `query` for sub-selects (e.g., line 1801). This makes the classes non-thread-safe and fragile.
- **Evidence:**
  ```java
  // Pattern identical in all three beans:
  private Connection conn;
  private Statement stmt;
  private Statement stmt1;
  private Statement stmt2;
  private ResultSet rset;
  private ResultSet rset1;
  private ResultSet rset2;
  private String query = "";
  ```
- **Recommendation:** Use local variables for all JDBC resources, ideally with try-with-resources. Never share Connection/Statement/ResultSet across method calls via instance fields.

### A15-09 — System.out.println used for error logging across all files
- **File:** `Databean_customer.java`:479–530, `Databean_getter.java`:812–863, `Databean_getuser.java`:8959–9012
- **Severity:** HIGH
- **Category:** Code Quality > Logging
- **Description:** All three data beans use `System.out.println()` in their main exception handlers and resource cleanup blocks. The error messages dump the raw SQL query string, exposing database schema, table names, and potentially parameter values to stdout.
- **Evidence:**
  ```java
  // Databean_customer.java line 479
  System.out.println(" Exception in Databean_customer In "
          + methodName + " \nquery " + query + " \nException :" + exception);

  // Databean_getter.java line 812 (wrong class name!)
  System.out.println(" Exception in Databean_getuser In "
          + methodName + " \nquery " + query + " \nException :" + e);

  // Databean_getuser.java line 8961
  System.out.println(" Exception in Databean_getuser In "
          + methodName + " \nquery " + query + " \nException :" + exception);
  ```
- **Recommendation:** Replace with a structured logging framework (SLF4J/Log4j). Do not log raw SQL queries in production. Note the copy-paste error in Databean_getter (says "Databean_getuser").

### A15-10 — SingleThreadModel usage in Frm_saveuser (deprecated since Servlet 2.4)
- **File:** `Frm_saveuser.java`:34–35
- **Severity:** HIGH
- **Category:** Code Quality > Deprecated API Usage
- **Description:** `Frm_saveuser` implements `SingleThreadModel`, which was deprecated in Servlet API 2.4 (2003) and removed in later versions. The `@SuppressWarnings("deprecation")` annotation on line 34 suppresses the compiler warning but does not fix the underlying issue. `SingleThreadModel` does not guarantee thread safety in a meaningful way per the Servlet specification.
- **Evidence:**
  ```java
  // Line 34-35
  @SuppressWarnings("deprecation")
  public  class Frm_saveuser extends HttpServlet implements SingleThreadModel {
  ```
- **Recommendation:** Remove `implements SingleThreadModel`. If thread safety is needed, use synchronized blocks or thread-safe data structures within the servlet.

### A15-11 — Pervasive snake_case and PascalCase naming violations across package
- **File:** All files in package
- **Severity:** MEDIUM
- **Category:** Code Quality > Naming Conventions
- **Description:** Class names, method names, and field names use a chaotic mix of conventions violating Java standards:
  - **Class names:** `Databean_customer`, `Databean_getter`, `Databean_getuser`, `Databean_user`, `Frm_saveuser`, `Frm_upload` all use snake_case instead of PascalCase.
  - **Method names:** `Query_Viewable_Battery()`, `Fetch_groups()`, `Query_Current_User()`, `clear_variables()` — all use PascalCase/snake_case instead of camelCase.
  - **Field names:** `Customer_Data_Name` (PascalCase), `user_cd` (snake_case), `licenseExpDate` (camelCase), `FSSX` (UPPER_CASE) — four different conventions in the same class.
  - **Misspellings:** `Fms_Vechile_Data_CANRULE` ("Vechile"), `Fms_Vehicle_NETWORK_Setttings` (triple-t), `Frms_Vechile_List_CAN` ("Frms"), `Current_Alert_Derpatment` ("Derpatment"), `currenUserIsSuperMaster` (missing "t"), `DashboarSubscriptionBean` (missing "d" — in bean package, referenced here).
- **Evidence:**
  ```java
  // Databean_getter.java line 131 — "Vechile" misspelling
  String Fms_Vechile_Data_RTLS_Cd = "";
  // Databean_getter.java line 204 — triple-t "Setttings"
  ArrayList<VehNetworkSettingsBean> Fms_Vehicle_NETWORK_Setttings = new ArrayList<>();
  // Databean_customer.java line 266 — "Derpatment"
  String Current_Alert_Derpatment = "";
  ```
- **Recommendation:** Adopt standard Java camelCase for all fields and methods, PascalCase for classes. Fix misspellings. For new code, enforce via checkstyle.

### A15-12 — Pervasive commented-out code across all data beans
- **File:** `Databean_customer.java` (30+ locations), `Databean_getter.java` (40+ locations), `Databean_getuser.java` (20+ locations), `FirmwareverBean.java` (lines 104–165)
- **Severity:** MEDIUM
- **Category:** Code Quality > Dead Code > Commented-Out Code
- **Description:** Over 90 locations across the package contain commented-out code, including: entire SQL query blocks, System.out.println debug statements, alternative method calls, test assignments (`//query = "testasdas";`), and in FirmwareverBean, a 62-line block of switch statements. These add maintenance noise and obscure active logic.
- **Evidence:**
  ```java
  // Databean_customer.java line 1910
  //query = "testasdas";

  // Databean_customer.java lines 1911-1918 — entire query block
  /*query = "select distinct(\"LOCATION_CD\")...*/

  // Databean_getter.java lines 1802-1819 — large SQL block
  /*queryString = "SELECT customer, site, department, gmtp_id...*/

  // FirmwareverBean.java lines 104-165 — 62-line switch block
  //      switch ((int) fb) {
  //      case 0: cb = "Standard"; break;
  ```
- **Recommendation:** Remove all commented-out code. Use version control history to recover if needed.

### A15-13 — Dead code: Databean_user.java is a completely empty class
- **File:** `Databean_user.java`:1–46
- **Severity:** HIGH
- **Category:** Code Quality > Dead Code > Empty Class
- **Description:** `Databean_user` declares 10 private fields (Connection, Statements, ResultSets, Strings) but has zero methods — no constructors, no getters, no setters, no business logic. It also has duplicate `import java.util.ArrayList;` (lines 8–9) and all other imports are unused. The class serves no purpose.
- **Evidence:**
  ```java
  public class Databean_user {
      private Connection conn;
      private Statement stmt;
      // ... 8 more fields
      // NO METHODS
  }
  ```
- **Recommendation:** Delete this class entirely.

### A15-14 — Dead code: Empty clearVectors() methods
- **File:** `Frm_saveuser.java`:449, `Frm_upload.java`:102
- **Severity:** MEDIUM
- **Category:** Code Quality > Dead Code > Empty Method
- **Description:** Both `Frm_saveuser.clearVectors()` and `Frm_upload.clearVectors()` have completely empty method bodies. They are called but perform no action.
- **Evidence:**
  ```java
  // Frm_saveuser.java line 449
  public void clearVectors() {
  }

  // Frm_upload.java line 102
  public void clearVectors() {
  }
  ```
- **Recommendation:** Either implement the intended vector-clearing logic or remove the methods and their call sites.

### A15-15 — Dead code: Empty Query_User() result processing
- **File:** `Databean_customer.java`:2028–2039
- **Severity:** MEDIUM
- **Category:** Code Quality > Dead Code > Empty Method Body
- **Description:** `Query_User()` executes a SQL query and calls `rset.next()` but the if-block body is completely empty. The method does nothing useful with the query results.
- **Evidence:**
  ```java
  public void Query_User() throws SQLException {
      methodName = "Query_User()";
      query = "SELECT ... FROM \"FMS_USR_MST\" WHERE \"USER_CD\" = '"+Param_User+"'";
      rset = stmt.executeQuery(query);
      if(rset.next()) {
          // empty
      }
  }
  ```
- **Recommendation:** Implement the method body or remove it if unused.

### A15-16 — Dead code: Debug artifacts left in production
- **File:** `Databean_customer.java`:350–365, `Databean_getter.java`:69,4580,4882, `Databean_getuser.java`:4084–4108
- **Severity:** MEDIUM
- **Category:** Code Quality > Dead Code > Debug Artifacts
- **Description:** Debug fields and methods are present in production code. `Databean_customer` assigns strings like `"test"`, `"test2"`, `"test3"` to a `debug` field (lines 350–365). `Databean_getter` has a `testresult` field initialized to `"O_O"` with getters `gettesting()` and `getTestresult()`. `Databean_getuser` has a `testing` field with `gettest()` that appends SQL queries (line 4098: `testing = testing + "<br>" + query`), leaking SQL to the UI.
- **Evidence:**
  ```java
  // Databean_customer.java line 350
  debug = "test";

  // Databean_getter.java line 69
  String testresult = "O_O";

  // Databean_getuser.java line 4098
  testing = testing + "<br>" + query;  // leaks SQL to UI
  ```
- **Recommendation:** Remove all debug fields, methods, and test-string assignments.

### A15-17 — Hardcoded HTML/CSS in SQL queries and business logic
- **File:** `Databean_customer.java`:2081–2132, `Databean_getter.java`:2414–2460, `Databean_getuser.java`:2293–2306
- **Severity:** MEDIUM
- **Category:** Code Quality > Architecture > Separation of Concerns
- **Description:** HTML color codes and inline CSS styles are embedded directly into SQL query result columns and business logic methods. This mixes presentation with data access.
- **Evidence:**
  ```java
  // Databean_customer.java line 2081
  String cell_color = "#FCC0B3";
  // embedded in SQL:
  "case when last_session <= current_timestamp - interval '7 day' then 'style=\"background-color:" + cell_color + "\"' else '' end "

  // Databean_getuser.java line 2295
  style = " style=\"background-color:#00FF00;color:#FFFFFF;font-weight:bold\"";
  ```
- **Recommendation:** Remove HTML from SQL queries and business logic. Return raw data; apply styling in the view layer (JSP/templates).

### A15-18 — Hardcoded customer-specific business logic
- **File:** `Databean_customer.java`:1303, `Databean_getter.java`:2382,2423,3793, `Databean_getuser.java`:3030
- **Severity:** MEDIUM
- **Category:** Code Quality > Architecture > Hardcoded Values
- **Description:** Customer-specific logic is hardcoded using string literals and magic numbers. `"James Hardie Australia"` controls alert filtering. Customer ID `"10"` is hardcoded as the LMH (Linde Material Handling) customer, controlling hire/dehire list behavior. `"Linde"` is used as a display name fallback.
- **Evidence:**
  ```java
  // Databean_customer.java line 1303
  if (!cust_name.equalsIgnoreCase("James Hardie Australia")) {
      ext = " where code != 'unauthorised_driver'";
  }

  // Databean_getter.java line 2382
  if(hire.equalsIgnoreCase("dehire") && customer_cd.equalsIgnoreCase("10")){ //LMH customer

  // Databean_getuser.java line 3030
  cust_name_disp = "Linde";
  ```
- **Recommendation:** Move customer-specific logic to configuration, database feature flags, or a strategy pattern.

### A15-19 — Test data left in production code
- **File:** `Databean_customer.java`:1708–1709
- **Severity:** MEDIUM
- **Category:** Code Quality > Dead Code > Test Data
- **Description:** After populating `Model_Cd` and `Model_Name` from the database in `Query_All_Models()`, hardcoded test entries are appended.
- **Evidence:**
  ```java
  // Databean_customer.java lines 1708-1709
  Model_Cd.add("test");
  Model_Name.add("test");
  ```
- **Recommendation:** Remove test data entries.

### A15-20 — Copy-paste error: Wrong class name in error message
- **File:** `Databean_getter.java`:812
- **Severity:** MEDIUM
- **Category:** Code Quality > Copy-Paste Error
- **Description:** The error message in `Databean_getter`'s catch block says `"Exception in Databean_getuser"` — the wrong class name. This was copied from `Databean_getuser` and never corrected. Similarly, `methodName` assignments in `Query_Master_Code_Tab()` and `getSuperMasterCode()` both incorrectly set `methodName = "Query_Master_Code()"` (lines 2174, 2207).
- **Evidence:**
  ```java
  // Databean_getter.java line 812
  System.out.println(" Exception in Databean_getuser In "
          + methodName + " \nquery " + query + " \nException :" + e);
  ```
- **Recommendation:** Fix class name references in error messages and methodName assignments.

### A15-21 — NullPointerException risk: Missing null check in finally block
- **File:** `Databean_getter.java`:818
- **Severity:** HIGH
- **Category:** Code Quality > Error Handling
- **Description:** In `Databean_getter.query()`, the `finally` block calls `rset.close()` without a null check, while `rset1`, `rset2`, `stmt`, `stmt1`, `stmt2`, and `conn` all have null checks. If an operation code path does not execute a query (e.g., the empty `customer_vehicle_rel_b` handler at line 574), `rset` remains null.
- **Evidence:**
  ```java
  // Line 818 — no null check
  try { rset.close(); } catch (SQLException e) { ... }

  // Line 823 — has null check
  if (rset1 != null) { try { rset1.close(); } ... }
  ```
- **Recommendation:** Add `if (rset != null)` before calling `rset.close()`.

### A15-22 — NullPointerException risk: File.list() without null check
- **File:** `Databean_getuser.java`:1650–1653
- **Severity:** HIGH
- **Category:** Code Quality > Error Handling
- **Description:** `Fetch_pics_sno()` calls `f.list()` and iterates over the result without checking for null. `File.list()` returns null if the path is not a directory. Other methods in the same class (e.g., `Fetch_pics_sno_model()` at line 814) do check for null, making this inconsistent.
- **Evidence:**
  ```java
  File f = new File(path);
  pic_list = f.list();
  for (int i = 0; i < pic_list.length; i++)   // NPE if pic_list is null
  ```
- **Recommendation:** Add `if (pic_list != null)` guard before iterating.

### A15-23 — `version.equalsIgnoreCase(null)` is always false
- **File:** `FirmwareverBean.java`:40,212
- **Severity:** HIGH
- **Category:** Code Quality > Bug
- **Description:** `String.equalsIgnoreCase(null)` always returns `false` per the Java specification. The preceding `version == null` check already handles the null case, making this clause redundant but misleading.
- **Evidence:**
  ```java
  // Line 40
  if(version == null || version.equalsIgnoreCase(null) || version.trim().equals("")) {

  // Line 212 (same pattern)
  if(version == null || version.equalsIgnoreCase(null) || version.trim().equals("")) {
  ```
- **Recommendation:** Simplify to `version == null || version.trim().isEmpty()`.

### A15-24 — Swallowed exceptions in multiple catch blocks
- **File:** `Databean_getter.java`:4529–4532,2979–2981, `Databean_customer.java`:2708–2711
- **Severity:** MEDIUM
- **Category:** Code Quality > Error Handling > Swallowed Exceptions
- **Description:** Multiple catch blocks silently swallow exceptions. In `Query_By_Cd_Questions()`, the catch block contains only a commented-out debug line. In `Query_Service_Status()`, the exception is assigned to an unused `error` variable (`error = "weird"`). In `Query_Customer_Data()`, the exception message is stored in `debug` and ignored.
- **Evidence:**
  ```java
  // Databean_getter.java line 4529
  } catch(Exception e) {
      //this.testresult = e.getMessage();
  }

  // Databean_getter.java line 2979
  } catch(Exception e){
      error = "weird";
  }

  // Databean_customer.java line 2708
  } catch(Exception e) {
      debug = e.getMessage();
  }
  ```
- **Recommendation:** Log all caught exceptions with stack traces. Never silently swallow exceptions.

### A15-25 — String comparison with `==` instead of `.equals()`
- **File:** `Databean_getter.java`:4420
- **Severity:** HIGH
- **Category:** Code Quality > Bug-Prone Code
- **Description:** Uses `==` for String comparison which checks reference identity, not value equality. This will almost always fail to match against a string literal.
- **Evidence:**
  ```java
  // Line 4420
  if (veh_typ_cd == null || veh_typ_cd == "") {
  ```
- **Recommendation:** Change to `veh_typ_cd == null || veh_typ_cd.isEmpty()`.

### A15-26 — IndexOutOfBoundsException risk: Accessing index 0 without size check
- **File:** `Databean_getter.java`:3773,3860
- **Severity:** MEDIUM
- **Category:** Code Quality > Error Handling > Missing Bounds Check
- **Description:** After populating ArrayLists from SQL queries, index 0 is accessed without verifying the list is non-empty. If the query returns no rows, this throws `IndexOutOfBoundsException`.
- **Evidence:**
  ```java
  // Databean_getter.java line 3773
  setLinde_location_cd_str( (String) Linde_location_cd.get(0) );

  // Databean_getter.java line 3860
  setCustomer_cd( (String) Fms_Usr_Mst_Cd.get(0) );
  ```
- **Recommendation:** Add `if (!list.isEmpty())` guard before accessing index 0.

### A15-27 — FTP credentials transmitted in plaintext
- **File:** `Databean_getter.java`:3603–3605, `Databean_getuser.java`:2917–2920
- **Severity:** MEDIUM
- **Category:** Security > Credential Handling
- **Description:** Both classes use `org.apache.commons.net.ftp.FTPClient` (plain FTP, not FTPS/SFTP), transmitting credentials and firmware files in cleartext.
- **Evidence:**
  ```java
  FTPClient f = new FTPClient();
  f.connect(LindeConfig.firmwareinternerserver, Integer.parseInt(LindeConfig.firmwareintport));
  f.login(RuntimeConf.firmwareuser, RuntimeConf.firmwarepass);
  ```
- **Recommendation:** Use `FTPSClient` or SFTP for encrypted credential and data transfer.

### A15-28 — Duplicate clearing in Databean_getuser.clear_variables()
- **File:** `Databean_getuser.java`:499–507
- **Severity:** LOW
- **Category:** Code Quality > Dead Code > Redundant Code
- **Description:** `user_cd.clear()`, `user_id.clear()`, `user_fnm.clear()`, and `user_lnm.clear()` are each called twice in succession within `clear_variables()`.
- **Evidence:**
  ```java
  user_cd.clear();
  user_id.clear();
  user_fnm.clear();
  user_lnm.clear();

  user_cd.clear();   // duplicate
  user_id.clear();   // duplicate
  user_fnm.clear();  // duplicate
  user_lnm.clear();  // duplicate
  ```
- **Recommendation:** Remove the duplicate `.clear()` calls.

### A15-29 — Massive code duplication across Fetch methods in Databean_getuser
- **File:** `Databean_getuser.java`: `Fetch_driver_lst()` (3290), `Fetch_driver_lst_alldept()` (3013), `Fetch_driver_lst_uk()` (3472), `Fetch_driver_lst_conf()` (3165), `Fetch_driver_lst_setup()` (3654)
- **Severity:** MEDIUM
- **Category:** Code Quality > Architecture > Code Duplication
- **Description:** Five nearly identical driver-list fetch methods share 80–90% of their code, differing only in minor filter conditions. Similarly, `Fetch_vehicle_types()` / `Fetch_vehicle_types1()` / `Fetch_vehicle_types2()` / `Fetch_vehicle_types_au()` are near-duplicates. `Fetch_cust_locations()` and `Fetch_cust_locations1()` are also copies.
- **Recommendation:** Extract common SQL and result mapping to shared private methods with filter parameters.

### A15-30 — FirmwareverBean: Dead variables `cc` and `cb` produce empty output
- **File:** `FirmwareverBean.java`:90–91,174,180–181,206
- **Severity:** LOW
- **Category:** Code Quality > Dead Code > Unused Variables
- **Description:** In both `convert32bit()` and `convert64bit()`, variables `cc` and `cb` are declared as empty strings, used in the output concatenation (`ver = check + " " + cc + " " + cb`), but the switch statements that would assign meaningful values are commented out (lines 104–165). The result is trailing whitespace in firmware version strings.
- **Evidence:**
  ```java
  String cc = "";
  String cb = "";
  // ... commented-out switches ...
  ver = check + " " + cc + " " + cb;  // produces "1.2.3  "
  ```
- **Recommendation:** Remove `cc` and `cb` or restore the code that populates them.

### A15-31 — Fragile exception recovery in FirmwareverBean
- **File:** `FirmwareverBean.java`:184–188,219–221
- **Severity:** MEDIUM
- **Category:** Code Quality > Error Handling
- **Description:** In `convert64bit()` and `getType()`, when `Long.parseLong(version, 16)` throws `NumberFormatException`, the code trims the first character and retries parsing. If the retry also fails, the exception propagates unhandled. This is fragile error recovery with no validation.
- **Evidence:**
  ```java
  try {
      current_version = Long.parseLong(version,16);
  } catch(NumberFormatException e) {
      version = version.substring(1);
      current_version = Long.parseLong(version,16); // may throw again
  }
  ```
- **Recommendation:** Wrap the retry in its own try-catch, or validate input format before parsing.

### A15-32 — Typos in identifiers and string literals
- **File:** `Databean_customer.java`:266,1459, `Databean_getter.java`:490,787
- **Severity:** LOW
- **Category:** Code Quality > Naming Conventions > Typos
- **Description:** Multiple typos baked into identifiers and literals: `Current_Alert_Derpatment` → "Department" (line 266), `"Uknown Source"` → "Unknown" (line 1459), op_code `"syncronize"` → "synchronize" (line 490), double semicolons `();;` (line 787).
- **Evidence:**
  ```java
  String Current_Alert_Derpatment = "";     // "Derpatment"
  Existing_Report_Delivery.add("Uknown Source");  // "Uknown"
  if(op_code.equalsIgnoreCase("syncronize"))       // "syncronize"
  Query_All_Drivers_By_Cus_Loc_Dept();;            // double semicolon
  ```
- **Recommendation:** Fix typos in identifiers and literals.

### A15-33 — Inconsistent null handling patterns
- **File:** `Databean_getuser.java` (throughout)
- **Severity:** LOW
- **Category:** Code Quality > Style and Consistency
- **Description:** Null handling varies across methods: some check `rset.getString(x) == null`, others check `.equalsIgnoreCase("null")` (string literal "null"), some use ternary operators, and some don't check at all.
- **Evidence:**
  ```java
  // Line 1591 — checks null AND string "null"
  if (rset.getString(10) == null || rset.getString(10).equalsIgnoreCase("null")) {
  // Line 700 — ternary
  vdep_prefix.add(rset.getString(4)==null?"":rset.getString(4));
  ```
- **Recommendation:** Standardize with a utility method like `DataUtil.nullToEmpty(rset.getString(x))`.

### A15-34 — Reimplemented standard library functionality
- **File:** `Databean_getuser.java`:2942–2956,2958–3011
- **Severity:** LOW
- **Category:** Code Quality > Redundant Code
- **Description:** `toDecimal()` reimplements `Integer.parseInt(s, 2)` using a manual loop. `decode_to_bits()` reimplements hex-to-binary conversion using 16 separate if-statements instead of `Integer.toBinaryString()`. Additionally, `decode_to_bits()` declares `throws SQLException` despite performing no SQL.
- **Evidence:**
  ```java
  // Lines 2958-3010 — 16 if-blocks for hex→binary
  private String decode_to_bits(String c) throws SQLException {
      String bits = "0000";
      if (c.equalsIgnoreCase("0")) { bits = "0000"; }
      if (c.equalsIgnoreCase("1")) { bits = "0001"; }
      // ... 14 more
  }
  ```
- **Recommendation:** Replace with standard library: `String.format("%4s", Integer.toBinaryString(Integer.parseInt(c, 16))).replace(' ', '0')` and `Integer.parseInt(s, 2)`.

### A15-35 — Concrete ArrayList type used in all method signatures instead of List interface
- **File:** All files with getter/setter methods
- **Severity:** INFO
- **Category:** Code Quality > Style and Consistency
- **Description:** All 200+ getter/setter methods across the package declare `ArrayList` (the concrete class) in return types and parameters rather than the `List` interface. This tightly couples callers to the implementation.
- **Evidence:**
  ```java
  public ArrayList getLicense_document_url() { return License_document_url; }
  public void setLicense_document_url(ArrayList License_document_url) { ... }
  ```
- **Recommendation:** Use `List` interface in method signatures: `public List<String> getLicenseDocumentUrl()`.

### A15-36 — Duplicate imports across files
- **File:** `Databean_customer.java`:8,10, `Databean_user.java`:8–9
- **Severity:** INFO
- **Category:** Code Quality > Dead Code > Duplicate Imports
- **Description:** `java.util.ArrayList` is imported twice in both `Databean_customer.java` (lines 8 and 10) and `Databean_user.java` (lines 8 and 9). Additionally, both files import specific classes alongside `java.util.*`, making the specific imports redundant.
- **Recommendation:** Remove duplicate and redundant imports.

### A15-37 — Unused imports across package
- **File:** `Databean_customer.java`:3,5–6,16,19–20, `Databean_user.java`:3–27 (all imports)
- **Severity:** INFO
- **Category:** Code Quality > Dead Code > Unused Imports
- **Description:** Multiple imports appear unused: `java.io.IOException`, `java.text.DecimalFormat`, `java.text.NumberFormat`, `org.apache.commons.net.ftp.FTPClient`, `org.apache.jasper.tagplugins.jstl.core.Param`, `com.torrent.surat.fms6.util.BeanComparator` in `Databean_customer`. In `Databean_user`, all imports are unused since the class has zero methods.
- **Recommendation:** Remove all unused imports. For `Databean_user`, delete the entire file (see A15-13).

### A15-38 — Missing Serializable across all classes
- **File:** All 7 files
- **Severity:** LOW
- **Category:** Code Quality > Architecture > Inconsistent Patterns
- **Description:** None of the 7 classes in the `master` package implement `Serializable` or declare `serialVersionUID`. If any of these beans are used in HTTP session scope or passed through RMI, serialization will fail.
- **Recommendation:** Implement `Serializable` and add `serialVersionUID` if beans are used in session scope. If not needed, document that intent.

---

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 4     |
| HIGH     | 9     |
| MEDIUM   | 16    |
| LOW      | 6     |
| INFO     | 3     |
| **Total**| **38** |

**Key Themes:**

1. **Security (A15-01, A15-03, A15-27):** Systemic SQL injection across all 200+ queries via string concatenation — the single most critical security issue. Passwords exposed through public getters and package-private fields. FTP credentials transmitted in plaintext.
2. **Bugs (A15-04, A15-21, A15-22, A15-23, A15-25):** Guaranteed NullPointerException from `null && .equalsIgnoreCase()`, missing null checks in finally blocks and File.list() calls, `==` used for String comparison, `equalsIgnoreCase(null)` always false.
3. **God class / Architecture (A15-02, A15-08, A15-29):** Four files exceed 3,000 lines. Monolithic dispatchers with 80+ branches. Shared mutable JDBC state across nested call chains. Massive code duplication across near-identical fetch methods.
4. **Encapsulation failures (A15-05, A15-06, A15-07):** 600+ package-private fields, 300+ raw-type ArrayLists, 200+ getters returning mutable internal collections.
5. **Dead code (A15-12, A15-13, A15-14, A15-15, A15-16, A15-19):** Empty class, empty methods, 90+ commented-out blocks, debug artifacts with test strings, test data in production.
6. **Naming / Style (A15-11, A15-32, A15-33):** Four naming conventions mixed across the same files. Misspellings baked into identifiers. Inconsistent null handling patterns.
7. **Logging / Error handling (A15-09, A15-10, A15-24):** System.out.println for all error logging, raw SQL exposed in error output, silently swallowed exceptions, deprecated SingleThreadModel.
