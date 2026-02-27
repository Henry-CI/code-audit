# Pass 3 -- Documentation Audit: DAO Package

**Audit ID:** A07
**Auditor:** A07 (Pass 3 -- Documentation)
**Date:** 2026-02-25
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Package:** `WEB-INF/src/com/torrent/surat/fms6/dao/`

---

## Reading Evidence

### 1. BatteryDAO.java (421 lines)

**Class:** `BatteryDAO` (line 13)
**Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public ArrayList<BatteryBean> getBatteryCharge(String cust_cd, String loc_cd, String dept_cd, String from, String to) throws SQLException` | 16 | NONE |
| 2 | `public ArrayList<BatteryBean> getBatteryChange(String cust_cd, String loc_cd, String dept_cd, String from, String to) throws SQLException` | 74 | NONE |
| 3 | `public ArrayList<BatteryBean> calculateBatteryChange(String cust_cd, String loc_cd, String dept_cd, String from, String to) throws SQLException` | 134 | NONE |
| 4 | `public ArrayList<BatteryBean> calculateBatteryCharge(String cust_cd, String loc_cd, String dept_cd, String from, String to) throws SQLException` | 250 | NONE |
| 5 | `public String getDuration(String sttime, String endtime) throws SQLException` | 351 | NONE |
| 6 | `public String getDept_prefix(String vcd) throws SQLException` | 386 | NONE |

**TODO/FIXME/HACK/XXX:** None found.
**Inline comments:** Line 268 has `//needs to think 5 minutes difference, time is message time or start time of session` -- this is a design consideration note left inline, somewhat vague but not misleading.

---

### 2. DriverDAO.java (569 lines)

**Class:** `DriverDAO` (line 18)
**Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public ArrayList<EntityBean> getArrayDriver(String cust_cd, String loc_cd, String dept_cd) throws SQLException` | 20 | NONE |
| 2 | `public void checkExpiry(String cust_cd) throws SQLException` | 76 | NONE |
| 3 | `public void sendIDDENY(String usercd, String weigand, String vehtype, HashMap<String, Boolean> statusMap) throws SQLException` | 141 | NONE |
| 4 | `public String getDriverlst(String cust_cd, String loc_cd, String dept_cd) throws SQLException` | 249 | NONE |
| 5 | `public ArrayList<EntityBean> getArrayDriverImpact(String cust_cd, String loc_cd, String dept_cd) throws SQLException` | 298 | NONE |
| 6 | `public String getDriverImpactLst(String cust_cd, String loc_cd, String dept_cd) throws SQLException` | 352 | NONE |
| 7 | `public void checkValidLicence(String userId, String newRevewDate, String expiryAlert) throws SQLException` | 402 | NONE |
| 8 | `public String getDriverFulllst(String cust_cd, String loc_cd, String dept_cd) throws SQLException` | 489 | NONE |
| 9 | `public String getDriverNameById(String driver_id) throws SQLException` | 538 | NONE |

**TODO/FIXME/HACK/XXX:** None found.
**Inline comments:** Line 90 has `//send IDDENY on users with expired driver licence or have no driver licence expiry date set up` -- adequate description of the subsequent logic.

---

### 3. DriverImportDAO.java (1208 lines)

**Class:** `DriverImportDAO` (line 15)
**Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public boolean checkDriverByNm(String compId, String fname, String lname, String id, boolean status) throws SQLException` | 17 | NONE |
| 2 | `public boolean checkDriverByLic(String compId, String licence, String id, boolean status) throws Exception` | 71 | NONE |
| 3 | `public ArrayList<DriverImportBean> getDriverByNm(String compId, String fname, String lname, boolean status) throws Exception` | 122 | NONE |
| 4 | `public ArrayList<DriverImportBean> getDriverByFullNm(String compId, String fname, boolean status) throws Exception` | 179 | NONE |
| 5 | `public ArrayList<DriverImportBean> getAllDriver(String compId, boolean status) throws Exception` | 235 | NONE |
| 6 | `public ArrayList<DriverImportBean> getAllDriverLinde(String compId) throws Exception` | 293 | NONE |
| 7 | `public ArrayList<DriverImportBean> getAllDriverLinde(String compId, boolean status) throws Exception` | 342 | NONE |
| 8 | `public ArrayList<DriverImportBean> getDriverLicence(String compId, boolean status) throws Exception` | 401 | NONE |
| 9 | `public ArrayList<DriverImportBean> getDriverById(String id) throws Exception` | 460 | NONE |
| 10 | `public boolean saveDriverInfo(DriverImportBean DriverImportBean) throws Exception` | 511 | NONE |
| 11 | `public String saveLicenseExpiryBlackListInfo(LicenseBlackListBean bean) throws Exception` | 559 | NONE |
| 12 | `public boolean updateDriverInfo(DriverImportBean DriverImportBean) throws Exception` | 924 | NONE |
| 13 | `public Boolean delDriverById(String id) throws Exception` | 973 | NONE |
| 14 | `public String getTotalDriverByID(String id, boolean status) throws Exception` | 1009 | NONE |
| 15 | `public String getDriverName(String id) throws Exception` | 1055 | NONE |
| 16 | `public String getDriverNameLinde(String id) throws Exception` | 1098 | NONE |
| 17 | `public Boolean uploadLicence(String licenceid, String url) throws Exception` | 1141 | NONE |
| 18 | `public Boolean uploadLicenceAU(String uid, String url) throws Exception` | 1174 | NONE |

**TODO/FIXME/HACK/XXX:** None found.
**Inline comments:** Lines 893-917 contain a commented-out resource cleanup block in the `finally` of `saveLicenseExpiryBlackListInfo`. This dead code block could mislead maintainers into thinking resource cleanup is handled; only `DBUtil.closeConnection(conn)` actually executes.

---

### 4. ImpactDAO.java (approx. 1300+ lines)

**Class:** `ImpactDAO` (line 31)
**Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public HashMap<String, ArrayList<ImpactBean>> getRedImpactCache(String cust_cd, String loc_cd) throws SQLException` | 33 | NONE |
| 2 | `public HashMap<String, ArrayList<ImpactBean>> getRedImpactCacheByDriver(String cust_cd, String loc_cd) throws SQLException` | 98 | NONE |
| 3 | `public ArrayList<ImpactBean> getRedImpact(String cust_cd, String loc_cd) throws SQLException` | 178 | NONE |
| 4 | `public ArrayList<ImpactBean> getRedImpactDriver(String cust_cd, String loc_cd) throws SQLException` | 258 | NONE |
| 5 | `public ArrayList<double[]> getImpacts(String cust_cd, String loc_cd, String dept_cd, String month, String from, String to) throws SQLException` | 342 | NONE |
| 6 | `public ArrayList<ImpactBean> getImpactsNationalRpt(String cust_cd, String loc_cd, String st_dt, String end_dt) throws SQLException` | 428 | NONE |
| 7 | `public ArrayList<ImpactBean> getImpacts(String cust_cd, String loc_cd) throws SQLException` | 605 | NONE |
| 8 | `public ArrayList<UnitutilBean> getImpactsByUnit(String cust_cd, String loc_cd) throws SQLException` | 689 | NONE |
| 9 | `public ArrayList<UnitutilBean> getImpactsByDriver(String cust_cd, String loc_cd) throws SQLException` | 826 | NONE |
| 10 | `public ArrayList<ImpactSummaryBean> getImpactsByUnit(String cust_cd, String loc_cd, String dept_cd, String from, String to) throws SQLException` | 1042 | NONE |
| 11 | `public ArrayList<ImpactLocBean> getImpactsByDriver(String cust_cd, String loc_cd, String dept_cd, String from, String to) throws SQLException` | 1162 | NONE |

**TODO/FIXME/HACK/XXX:** None found.
**Inline comments:** No misleading inline comments identified.

---

### 5. ImportDAO.java (approx. 4850+ lines)

**Class:** `ImportDAO` (line 25)
**Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public boolean saveQuestions(QuestionBean qbean) throws Exception` | 30 | NONE |
| 2 | `public boolean saveQuestions(QuestionBean qbean, List<String> langChoice) throws Exception` | 199 | NONE |
| 3 | `public ArrayList<String> getCurrentCheckCd(String custCd, String locCd, String deptCd, String vehTypeCd) throws Exception` | 376 | Block comment `/*GRAB CHECK_CD of current Preop Checklist*/` (line 373) -- not Javadoc |
| 4 | `public ArrayList<String> getCurrentCheckCdTab(String custCd, String locCd, String deptCd) throws Exception` | 443 | NONE |
| 5 | `public void removePreviousChecklist(ArrayList<String> chkList) throws Exception` | 541 | Block comment `/*Remove OLD PREVIOUS CHECKLIST SETTINGS*/` (line 538) -- not Javadoc |
| 6 | `public String saveQuestionsTab(QuestionBean qbean) throws Exception` | 608 | Block comment (line 603) with author/date -- not Javadoc |
| 7 | `public String saveDriverInfo(DriverImportBean driverBean) throws SQLException` | 907 | Block comment (line 902) with author/date -- not Javadoc |
| 8 | `public String saveDriverInfoAU(DriverImportBean driverBean) throws SQLException` | 1389 | Block comment (line 1384) with author/date -- not Javadoc |
| 9 | `public int saveDriverInfo1(DriverImportBean driverBean) throws Exception` | 1789 | NONE |
| 10 | `public int saveDriverInfoAu(DriverImportBean driverBean) throws Exception` | 2109 | NONE |
| 11 | `public boolean saveDriverDeptRel(int driverId, String deptId, String locId, String custId) throws Exception` | 2440 | NONE |
| 12 | `public boolean saveDriverDeptRelNew(String driverId, String deptName, String locName, String custId, String access_l, String access_s, String access_d) throws Exception` | 2481 | NONE |
| 13 | `public String saveVehicleInfo(VehicleImportBean vehBean) throws SQLException` | 2632 | NONE |
| 14 | `public String sendCanUnit(CanruleBean canBean) throws SQLException` | 3487 | Block comment (line 3482) with author/date -- not Javadoc |
| 15 | `public Boolean saveServiceSettings(String hireno, String serviceDate) throws Exception` | 4728 | NONE |
| 16 | `public Boolean saveServiceSettingsServer(String serial, String serviceDate) throws Exception` | 4805 | NONE |

**TODO/FIXME/HACK/XXX:** None found.
**Existing Javadoc:** One Javadoc block at line 4351 for private method `normalizeTimeFormat` -- properly formatted with `@param` and `@return`. This is the only Javadoc in the entire DAO package and it is on a private method.
**Inline comments:** Numerous commented-out `System.out.println` statements. Block comments at method boundaries serve as section markers (author/date) but are not Javadoc.
**Misleading inline comment:** Line 381 in `getCurrentCheckCd` logs `"Inside ImportDAO Method : saveQuestionsTab"` -- this is misleading; it references the wrong method name.

---

### 6. LockOutDAO.java (145 lines)

**Class:** `LockOutDAO` (line 13)
**Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public ArrayList<LockOutBean> getLockOutData(String cust_cd, String loc_cd) throws SQLException` | 15 | NONE |
| 2 | `public ArrayList<LockOutBean> getLockOutDataNtlRpt(String cust_cd, String loc_cd, String st_dt, String end_dt) throws SQLException` | 80 | NONE |

**TODO/FIXME/HACK/XXX:** None found.
**Misleading inline comment / logic discrepancy:** In `getLockOutData` (line 56-58), the else clause maps unknown reason codes to `"Other"`. In `getLockOutDataNtlRpt` (line 120-123), the else clause maps unknown reason codes to `"Question"`. These are functionally different behaviors with no documenting comment explaining the discrepancy. This is a potential documentation/logic inconsistency.

---

### 7. MessageDao.java (113 lines)

**Class:** `MessageDao` (line 14)
**Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public void setOpCode(String opCode)` | 23 | NONE |
| 2 | `public String getMsg()` | 26 | NONE |
| 3 | `public void setFid(String fid)` | 30 | NONE |
| 4 | `public void setMsg(String msg)` | 34 | NONE |
| 5 | `public boolean isStatus()` | 39 | NONE |
| 6 | `public void setStatus(boolean status)` | 44 | NONE |
| 7 | `public void init()` | 48 | NONE |
| 8 | `public void selectMesssage() throws SQLException` | 105 | NONE |

Note: `selectMesssage` has a typo in the name (triple 's'). Methods 1-6 are simple getters/setters (LOW severity). Methods 7-8 perform DB access (MEDIUM severity).

**TODO/FIXME/HACK/XXX:** None found.
**Inline comments:** No misleading inline comments.

---

### 8. PreCheckDAO.java (578 lines)

**Class:** `PreCheckDAO` (line 24)
**Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public ArrayList<Integer> getChecks(String cust_cd, String loc_cd, String dept_cd, String month, String from, String to) throws SQLException` | 26 | NONE |
| 2 | `public ArrayList<PreCheckBean> getChecks(String cust_cd, String loc_cd) throws SQLException` | 127 | NONE |
| 3 | `public ArrayList<FleetCheckBean> getCheckSummary(String cust_cd, String loc_cd, String dept_cd, String month, String from, String to) throws SQLException` | 181 | NONE |
| 4 | `public ArrayList<PreCheckBean> getChecksByDriver(String cust_cd, String loc_cd) throws SQLException` | 267 | NONE |
| 5 | `public ArrayList<PreCheckSummaryBean> getChecks(String cust_cd, String loc_cd, String dept_cd, String from, String to) throws SQLException` | 316 | Inline comment `//Quarterly report` (line 315) -- not Javadoc |
| 6 | `public ArrayList<PreCheckSummaryBean> getChecksByDriver(String cust_cd, String loc_cd, String dept_cd, String from, String to) throws SQLException` | 433 | Inline comment `//Quarterly report` (line 432) -- not Javadoc |

**TODO/FIXME/HACK/XXX:** None found.
**Inline comments:** Lines 315 and 432 have minimal `//Quarterly report` annotations. These are insufficient as documentation for complex overloaded methods that share the same name but serve substantially different purposes.

---

### 9. RegisterDAO.java (535 lines)

**Class:** `RegisterDAO` (line 14)
**Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public String[] register(String fname, String lname, String email, String cname, String phone, String[] vehnm, String[] vehmodel, String[] dfname, String[] dlname) throws SQLException` | 17 | NONE |
| 2 | `public boolean checkDupComp(String cname) throws SQLException` | 460 | NONE |
| 3 | `public boolean checkAuthority(String username, String password) throws SQLException` | 498 | NONE |

**TODO/FIXME/HACK/XXX:** None found.
**Inline comments:** No misleading inline comments.

---

### 10. UnitDAO.java (approx. 2730+ lines)

**Class:** `UnitDAO` (line 51)
**Class-level Javadoc:** NONE

| # | Method Signature | Line | Javadoc |
|---|-----------------|------|---------|
| 1 | `public String getDepartmentLst(String cust_cd, String loc_cd) throws SQLException` | 53 | NONE |
| 2 | `public ArrayList<EntityBean> getArrayDepartment(String cust_cd, String loc_cd) throws SQLException` | 102 | NONE |
| 3 | `public String getUnitLstByModel(String cust_cd, String loc_cd, String dept_cd, String model_cd) throws SQLException` | 159 | NONE |
| 4 | `public ArrayList<EntityBean> getArrayUnitByModel(String cust_cd, String loc_cd, String dept_cd, String model_cd) throws SQLException` | 211 | NONE |
| 5 | `public ArrayList<EntityBean> getArryModel(String cust_cd, String loc_cd, String dept_cd) throws SQLException` | 267 | NONE |
| 6 | `public ArrayList<EntityBean> getArryModelImpact(String cust_cd, String loc_cd, String dept_cd) throws SQLException` | 321 | NONE |
| 7 | `public ArrayList<EntityBean> getArryModelImpactByDriver(String cust_cd, String loc_cd, String dept_cd, String driver_cd) throws SQLException` | 376 | NONE |
| 8 | `public String[] getLocById(String loc_cd) throws SQLException` | 437 | NONE |
| 9 | `public String getCustName(String cust_cd) throws SQLException` | 472 | NONE |
| 10 | `public String getLocName(String loc_cd) throws SQLException` | 507 | NONE |
| 11 | `public String getDeptName(String dept_cd) throws SQLException` | 543 | NONE |
| 12 | `public ArrayList<UnitutilBean> getUtil(String cust_cd, String loc_cd, String dept_cd, String firstDate, int duration) throws SQLException` | 581 | NONE |
| 13 | `public int[] getDays() throws SQLException` | 644 | NONE |
| 14 | `public ArrayList<EntityBean> getAllModel() throws SQLException` | 680 | NONE |
| 15 | `public String[] getDuration() throws SQLException` | 717 | NONE |
| 16 | `public String[] getDurationWeek() throws SQLException` | 749 | NONE |
| 17 | `public ArrayList<UnusedUnitBean> getUnusedUnit(String cust_cd, String loc_cd, String dept_cd, int days) throws SQLException` | 782 | NONE |
| 18 | `public ArrayList<PreCheckBean> getArrayModelPreCheck(String cust_cd, String loc_cd, String dept_cd, Boolean isnull) throws SQLException` | 865 | NONE |
| 19 | `public int getTotalTime(String cust_cd, String loc_cd, String model_cd) throws SQLException` | 927 | Inline comment `//get working hours total in muniutes` (line 926) -- not Javadoc; typo "muniutes" |
| 20 | `public int[] getWorkDays(String cust_cd, String loc_cd, String model_cd) throws SQLException` | 997 | Inline comment `//get working hours total in muniutes` (line 996) -- not Javadoc; misleading, this method returns work days not hours |
| 21 | `public ArrayList<UnitBean> getUnitSummary() throws SQLException` | 1080 | NONE |
| 22 | `public ArrayList<UnitBean> getUnitSummaryNZ() throws SQLException` | 1226 | NONE |
| 23 | `public ArrayList<UnitBean> getSimSwapSummary() throws SQLException` | 1287 | NONE |
| 24 | `public ArrayList<MaxHourUsageBean> getMaxUtilGroup(String cust_cd, ArrayList locdeptList, String from, String to)` | 1392 | NONE |
| 25 | `public ArrayList<EntityBean> getArryModelLindeGroup(String cust_cd, ...)` | 1559 | NONE |
| 26 | `public ArrayList<EntityBean> getArrayLocation(String cust_cd, String loc_cd)` | 1628 | NONE |
| 27 | `public ArrayList<EntityBean> getArrayDepartment(String cust_cd, ...)` | 1677 | NONE |
| 28 | `public String getUnitLstByModelLinde(String cust_cd, String loc_cd, ...)` | 1738 | NONE |
| 29 | `public String getExportDir() throws Exception` | 1801 | NONE |
| 30 | `public ArrayList<MaxHourUsageBean> getMaxUtil(String cust_cd, ...)` | 1811 | NONE |
| 31 | `public ArrayList<EntityBean> getArryModelLinde(String cust_cd, ...)` | 1962 | NONE |
| 32 | `public ArrayList<String[]> getWeeks(String from, String to, int weeks)` | 2015 | NONE |
| 33 | `public String getUnitNameById(String unit_cd) throws SQLException` | 2079 | NONE |
| 34 | `public String getUnitTypeById(String unit_cd) throws SQLException` | 2115 | NONE |
| 35 | `public ArrayList<DailyUsageDeptDataBean> getUnitUtilByGroup(String cust_cd, String loc_cd, ...)` | 2152 | NONE |
| 36 | `public ArrayList<UnitutilBean> getUnitUtil(String cust_cd, String loc_cd, ...)` | 2368 | NONE |
| 37 | `public ArrayList<EntityBean> getArrayByModel(String cust_cd, String loc_cd, ...)` | 2590 | NONE |
| 38 | `public String getCustbyId(String custCd) throws SQLException` | 2645 | NONE |
| 39 | `public ArrayList<UserDriverBean> getDriversByCustSite(String custCd, String locCd) throws SQLException` | 2681 | NONE |

**TODO/FIXME/HACK/XXX:** None found.
**Misleading inline comment:** Line 996 states `//get working hours total in muniutes` but precedes `getWorkDays` which returns work days, not hours. This is copy-paste from line 926 and is misleading.

---

## Findings Summary

**Total public methods across 10 files: 120**
**Public methods with Javadoc: 0** (the one Javadoc found at ImportDAO line 4351 is on a private method)
**Class-level Javadoc: 0 out of 10 classes**

---

## Findings

### A07-1 | MEDIUM | BatteryDAO.java -- All 6 public methods lack Javadoc

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/BatteryDAO.java`
**Lines:** 16, 74, 134, 250, 351, 386
**Details:** All 6 public methods (`getBatteryCharge`, `getBatteryChange`, `calculateBatteryChange`, `calculateBatteryCharge`, `getDuration`, `getDept_prefix`) are DB-access methods constructing complex SQL queries with multiple JOINs. None have any Javadoc documenting parameters, return semantics, or the SQL operations performed. Class-level Javadoc is also absent.

---

### A07-2 | MEDIUM | DriverDAO.java -- All 9 public methods lack Javadoc

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/DriverDAO.java`
**Lines:** 20, 76, 141, 249, 298, 352, 402, 489, 538
**Details:** All 9 public methods lack Javadoc. Critical methods include `checkExpiry` (sends IDDENY messages to hardware), `sendIDDENY` (inserts into outgoing message queue), and `checkValidLicence` (sends IDAUTH messages). These have significant side effects (message queue inserts, licence expiry status updates) that are entirely undocumented. Class-level Javadoc is also absent.

---

### A07-3 | MEDIUM | DriverImportDAO.java -- All 18 public methods lack Javadoc

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/DriverImportDAO.java`
**Lines:** 17, 71, 122, 179, 235, 293, 342, 401, 460, 511, 559, 924, 973, 1009, 1055, 1098, 1141, 1174
**Details:** All 18 public methods lack Javadoc. `saveLicenseExpiryBlackListInfo` (line 559) is an especially complex 364-line method performing blacklist management, licence expiry record insertion/update, and vehicle access mapper table manipulation. Its parameter expectations and error return semantics (returns error message string) are completely undocumented. Class-level Javadoc is also absent.

---

### A07-4 | MEDIUM | ImpactDAO.java -- All 11 public methods lack Javadoc

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/ImpactDAO.java`
**Lines:** 33, 98, 178, 258, 342, 428, 605, 689, 826, 1042, 1162
**Details:** All 11 public methods lack Javadoc. The class has heavily overloaded methods: `getImpacts` (3 overloads), `getImpactsByUnit` (2 overloads), `getImpactsByDriver` (2 overloads). Without documentation, callers cannot distinguish which overload to use without reading the implementation. `getRedImpact` vs `getRedImpactCache` semantics are also unclear. Class-level Javadoc is also absent.

---

### A07-5 | MEDIUM | ImportDAO.java -- All 16 public methods lack Javadoc

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/ImportDAO.java`
**Lines:** 30, 199, 376, 443, 541, 608, 907, 1389, 1789, 2109, 2440, 2481, 2632, 3487, 4728, 4805
**Details:** All 16 public methods in this 4850+ line file lack Javadoc. Some methods have non-Javadoc block comments with author/date which serve as section markers but provide no `@param`/`@return`/`@throws` documentation. `saveDriverInfo` vs `saveDriverInfo1` vs `saveDriverInfoAU` vs `saveDriverInfoAu` naming is confusing with no documentation to clarify the differences. Class-level Javadoc is also absent.

---

### A07-6 | HIGH | ImportDAO.java -- Misleading log message in getCurrentCheckCd

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/ImportDAO.java`
**Line:** 381
**Details:** Inside method `getCurrentCheckCd` (line 376), the log statement at line 381 reads `log.info("Inside ImportDAO Method : saveQuestionsTab")`. This incorrectly identifies the method as `saveQuestionsTab` when the actual method is `getCurrentCheckCd`. This is misleading for anyone debugging via logs and indicates a copy-paste error.

---

### A07-7 | MEDIUM | LockOutDAO.java -- Both public methods lack Javadoc

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/LockOutDAO.java`
**Lines:** 15, 80
**Details:** Both public methods (`getLockOutData`, `getLockOutDataNtlRpt`) lack Javadoc. Class-level Javadoc is also absent.

---

### A07-8 | HIGH | LockOutDAO.java -- Inconsistent else-clause behavior between getLockOutData and getLockOutDataNtlRpt undocumented

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/LockOutDAO.java`
**Lines:** 56-58 vs 120-123
**Details:** In `getLockOutData`, the else clause (line 57) maps unrecognized lockout reason codes to `"Other"`. In `getLockOutDataNtlRpt`, the else clause (line 122) maps the same unrecognized codes to `"Question"`. There is no comment or documentation explaining why these two nearly identical methods handle the default case differently. This is likely a copy-paste bug, but without documentation, intent is unclear. The lack of any comment on this discrepancy is misleading for maintainers.

---

### A07-9 | MEDIUM | MessageDao.java -- DB-access methods init() and selectMesssage() lack Javadoc

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/MessageDao.java`
**Lines:** 48, 105
**Details:** `init()` performs JNDI lookup and conditional query execution based on `opCode` field state. `selectMesssage()` queries the outgoing table. Neither has Javadoc. The method name `selectMesssage` contains a typo (triple 's'). Class-level Javadoc is also absent.

---

### A07-10 | LOW | MessageDao.java -- Simple getters/setters lack Javadoc

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/MessageDao.java`
**Lines:** 23, 26, 30, 34, 39, 44
**Details:** Six getter/setter methods (`setOpCode`, `getMsg`, `setFid`, `setMsg`, `isStatus`, `setStatus`) lack Javadoc. These are simple accessors so the severity is LOW.

---

### A07-11 | MEDIUM | PreCheckDAO.java -- All 6 public methods lack Javadoc

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/PreCheckDAO.java`
**Lines:** 26, 127, 181, 267, 316, 433
**Details:** All 6 public methods lack Javadoc. The class has 3 overloads of `getChecks` and 2 overloads of `getChecksByDriver` with different return types and parameters. The only inline annotation is `//Quarterly report` (lines 315, 432) which is inadequate for distinguishing the overloads. Class-level Javadoc is also absent.

---

### A07-12 | MEDIUM | RegisterDAO.java -- All 3 public methods lack Javadoc

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/RegisterDAO.java`
**Lines:** 17, 460, 498
**Details:** All 3 public methods lack Javadoc. `register` (line 17) is a 440-line method that creates a customer account, default location, department, user groups, access rights, pre-op check questions, vehicles, drivers, and admin users -- all in a single transaction. Its 9-parameter signature and complex multi-table insert semantics are entirely undocumented. Class-level Javadoc is also absent.

---

### A07-13 | MEDIUM | UnitDAO.java -- All 39 public methods lack Javadoc

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/UnitDAO.java`
**Lines:** 53, 102, 159, 211, 267, 321, 376, 437, 472, 507, 543, 581, 644, 680, 717, 749, 782, 865, 927, 997, 1080, 1226, 1287, 1392, 1559, 1628, 1677, 1738, 1801, 1811, 1962, 2015, 2079, 2115, 2152, 2368, 2590, 2645, 2681
**Details:** All 39 public methods in this 2730+ line file lack Javadoc. Multiple overloaded method groups exist: `getArrayDepartment` (2 overloads), `getImpactsByUnit`/`getImpactsByDriver` (called from ImpactDAO). The file contains Linde-specific variant methods (e.g., `getArryModelLinde`, `getUnitLstByModelLinde`, `getArryModelLindeGroup`) with no documentation explaining the Linde vs non-Linde distinction. Class-level Javadoc is also absent.

---

### A07-14 | HIGH | UnitDAO.java -- Misleading inline comment on getWorkDays

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/UnitDAO.java`
**Line:** 996
**Details:** The inline comment `//get working hours total in muniutes` precedes the method `getWorkDays` (line 997) which returns `int[]` representing work days, not working hours in minutes. This comment was copy-pasted from line 926 (which precedes `getTotalTime`, where it is at least somewhat accurate despite the typo "muniutes"). On `getWorkDays`, this comment is actively misleading about the method's purpose and return value.

---

### A07-15 | INFO | Package-wide -- No class-level Javadoc on any of the 10 DAO classes

**File:** All 10 files in `WEB-INF/src/com/torrent/surat/fms6/dao/`
**Details:** None of the 10 DAO classes have class-level Javadoc describing the class purpose, the database tables it interacts with, or its role in the application. For a DAO layer, class-level documentation identifying the primary tables and data domain would significantly aid maintainability.

---

### A07-16 | INFO | Package-wide -- Only Javadoc in entire package is on a private method

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/ImportDAO.java`
**Line:** 4351
**Details:** The only Javadoc block in the entire 10-file DAO package is on the private method `normalizeTimeFormat` (line 4357). While this Javadoc is well-formed (with `@param` and `@return`), none of the 120 public methods across all 10 DAO classes have any Javadoc documentation.

---

## Statistics

| Severity | Count |
|----------|-------|
| HIGH     | 3     |
| MEDIUM   | 10    |
| LOW      | 1     |
| INFO     | 2     |
| **Total** | **16** |

| Metric | Value |
|--------|-------|
| Total files audited | 10 |
| Total public methods | 120 |
| Public methods with Javadoc | 0 (0%) |
| Classes with class-level Javadoc | 0 (0%) |
| TODO/FIXME/HACK/XXX found | 0 |
| Misleading comments found | 3 (A07-6, A07-8, A07-14) |
