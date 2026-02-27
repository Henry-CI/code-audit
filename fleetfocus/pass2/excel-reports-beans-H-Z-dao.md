# Pass 2 -- Test Coverage: excel/reports/beans (H-Z) + excel/reports/dao
**Agent:** A14
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

---

## Test Infrastructure Assessment

| Aspect | Status |
|--------|--------|
| Test directory (`test/`, `src/test/`) | **ABSENT** -- no test source root exists anywhere in the repository |
| JUnit dependency | **ABSENT** -- no `import org.junit` found in any `.java` file |
| TestNG dependency | **ABSENT** -- no `import org.testng` found in any `.java` file |
| `@Test` annotations | **ZERO** occurrences across entire codebase |
| Build-tool test config (Maven Surefire, Gradle test task) | **ABSENT** -- no `pom.xml` or `build.gradle` in repository root |
| CI/CD test stage | **UNKNOWN** -- no evidence of test execution in repository |
| Mocking frameworks (Mockito, EasyMock) | **ABSENT** |
| Sole "Test" file | `EncryptTest.java` is a decompiled utility class (encrypt/decrypt), not a test |

**Conclusion:** The repository has **zero automated tests**. Every file audited below has **0% test coverage**.

---

## Reading Evidence

### 1. HireDehireReportBean.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/HireDehireReportBean.java`
- **Lines:** 1-63
- **Class:** `HireDehireReportBean` (plain POJO, no superclass)
- **Fields:** 8 raw-typed `ArrayList` fields (veh_serial, veh_gmtp, veh_hire, hire_time, dehire_time, cust_name, loc_nm, dep_nm) -- all private, all uninitialized (default null)
- **Public methods:**

| # | Method Signature | Line |
|---|-----------------|------|
| 1 | `ArrayList getVeh_serial()` | 14 |
| 2 | `void setVeh_serial(ArrayList)` | 17 |
| 3 | `ArrayList getVeh_gmtp()` | 20 |
| 4 | `void setVeh_gmtp(ArrayList)` | 23 |
| 5 | `ArrayList getVeh_hire()` | 26 |
| 6 | `void setVeh_hire(ArrayList)` | 29 |
| 7 | `ArrayList getHire_time()` | 32 |
| 8 | `void setHire_time(ArrayList)` | 35 |
| 9 | `ArrayList getDehire_time()` | 38 |
| 10 | `void setDehire_time(ArrayList)` | 41 |
| 11 | `ArrayList getCust_name()` | 44 |
| 12 | `void setCust_name(ArrayList)` | 47 |
| 13 | `ArrayList getLoc_nm()` | 50 |
| 14 | `void setLoc_nm(ArrayList)` | 53 |
| 15 | `ArrayList getDep_nm()` | 57 |
| 16 | `void setDep_nm(ArrayList)` | 59 |

---

### 2. ImpactReportBean.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/ImpactReportBean.java`
- **Lines:** 1-120
- **Class:** `ImpactReportBean` (plain POJO, no superclass)
- **Fields:** 11 `ArrayList` fields (7 uninitialized/null-default, 4 initialized to `new ArrayList()`), 1 `String fileName` (null-default), 1 `int photoTotal`, 1 `boolean rtlsEnabled`
- **Public methods:**

| # | Method Signature | Line |
|---|-----------------|------|
| 1 | `ArrayList getVimp_shock_id()` | 23 |
| 2 | `ArrayList getVimp_rtlsjson()` | 26 |
| 3 | `boolean isRtlsEnabled()` | 29 |
| 4 | `void setVimp_shock_id(ArrayList)` | 32 |
| 5 | `void setVimp_rtlsjson(ArrayList)` | 35 |
| 6 | `void setRtlsEnabled(boolean)` | 38 |
| 7 | `ArrayList getVtmp_imp_data()` | 41 |
| 8 | `void setVtmp_imp_data(ArrayList)` | 44 |
| 9 | `ArrayList getMachineId()` | 48 |
| 10 | `ArrayList getModel()` | 51 |
| 11 | `ArrayList getDriverName()` | 54 |
| 12 | `ArrayList getCardNo()` | 57 |
| 13 | `ArrayList getDtImpact()` | 60 |
| 14 | `ArrayList getSeverityLvl()` | 63 |
| 15 | `String getFileName()` | 66 |
| 16 | `void setMachineId(ArrayList)` | 69 |
| 17 | `void setModel(ArrayList)` | 72 |
| 18 | `void setDriverName(ArrayList)` | 75 |
| 19 | `void setCardNo(ArrayList)` | 78 |
| 20 | `void setDtImpact(ArrayList)` | 81 |
| 21 | `void setSeverityLvl(ArrayList)` | 84 |
| 22 | `void setFileName(String)` | 87 |
| 23 | `int getPhotoTotal()` | 90 |
| 24 | `void setPhotoTotal(int)` | 93 |
| 25 | `ArrayList getVimp_img()` | 96 |
| 26 | `void setVimp_img(ArrayList)` | 99 |
| 27 | `ArrayList getMeterDetails()` | 102 |
| 28 | `void setMeterDetails(ArrayList)` | 105 |
| 29 | `ArrayList getVehId()` | 108 |
| 30 | `void setVehId(ArrayList)` | 111 |

---

### 3. KeyHourUtilBean.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/KeyHourUtilBean.java`
- **Lines:** 1-170
- **Class:** `KeyHourUtilBean` (plain POJO, no superclass)
- **Fields:** 14 package-private `ArrayList` fields (all initialized), 9 package-private `String` fields (null-default)
- **Public methods:**

| # | Method Signature | Line |
|---|-----------------|------|
| 1 | `ArrayList getVeh_cd()` | 32 |
| 2 | `void setVeh_cd(ArrayList)` | 35 |
| 3 | `ArrayList getVeh_nm()` | 38 |
| 4 | `void setVeh_nm(ArrayList)` | 41 |
| 5 | `ArrayList getVeh_typ_nm1()` | 44 |
| 6 | `void setVeh_typ_nm1(ArrayList)` | 47 |
| 7 | `ArrayList getVutil1()` | 50 |
| 8 | `void setVutil1(ArrayList)` | 53 |
| 9 | `ArrayList getVutil2()` | 56 |
| 10 | `void setVutil2(ArrayList)` | 59 |
| 11 | `ArrayList getVutil3()` | 62 |
| 12 | `void setVutil3(ArrayList)` | 65 |
| 13 | `ArrayList getVutil4()` | 68 |
| 14 | `void setVutil4(ArrayList)` | 71 |
| 15 | `ArrayList getVutil5()` | 74 |
| 16 | `void setVutil5(ArrayList)` | 77 |
| 17 | `ArrayList getVutil6()` | 80 |
| 18 | `void setVutil6(ArrayList)` | 83 |
| 19 | `ArrayList getVutil7()` | 86 |
| 20 | `void setVutil7(ArrayList)` | 89 |
| 21 | `ArrayList getVutil8()` | 92 |
| 22 | `void setVutil8(ArrayList)` | 95 |
| 23 | `ArrayList getVutilt()` | 98 |
| 24 | `void setVutilt(ArrayList)` | 101 |
| 25 | `ArrayList getVutilpt()` | 104 |
| 26 | `void setVutilpt(ArrayList)` | 107 |
| 27 | `String getUtil1()` | 110 |
| 28 | `void setUtil1(String)` | 113 |
| 29 | `String getUtil2()` | 116 |
| 30 | `void setUtil2(String)` | 119 |
| 31 | `String getUtil3()` | 122 |
| 32 | `void setUtil3(String)` | 125 |
| 33 | `String getUtil4()` | 128 |
| 34 | `void setUtil4(String)` | 131 |
| 35 | `String getUtil5()` | 134 |
| 36 | `void setUtil5(String)` | 137 |
| 37 | `String getUtil6()` | 140 |
| 38 | `void setUtil6(String)` | 143 |
| 39 | `String getUtil7()` | 146 |
| 40 | `void setUtil7(String)` | 149 |
| 41 | `String getUtil8()` | 152 |
| 42 | `void setUtil8(String)` | 155 |
| 43 | `String getUtilt()` | 158 |
| 44 | `void setUtilt(String)` | 161 |
| 45 | `ArrayList getVeh_id()` | 164 |
| 46 | `void setVeh_id(ArrayList)` | 167 |

---

### 4. OperationalStatusReportItemResultBean.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/OperationalStatusReportItemResultBean.java`
- **Lines:** 1-62
- **Class:** `OperationalStatusReportItemResultBean extends BaseItemResultBean` (BaseItemResultBean is an empty marker class)
- **Fields:** 8 package-private `String` fields, all initialized to `""`
- **Public methods:**

| # | Method Signature | Line |
|---|-----------------|------|
| 1 | `String getEquipNo()` | 14 |
| 2 | `void setEquipNo(String)` | 17 |
| 3 | `String getSerialNo()` | 20 |
| 4 | `void setSerialNo(String)` | 23 |
| 5 | `String getModel()` | 26 |
| 6 | `void setModel(String)` | 29 |
| 7 | `String getTriggerType()` | 32 |
| 8 | `void setTriggerType(String)` | 35 |
| 9 | `String getStatus()` | 38 |
| 10 | `void setStatus(String)` | 41 |
| 11 | `String getInitiatedBy()` | 44 |
| 12 | `void setInitiatedBy(String)` | 47 |
| 13 | `String getSetTime()` | 50 |
| 14 | `void setSetTime(String)` | 53 |
| 15 | `String getNote()` | 56 |
| 16 | `void setNote(String)` | 59 |

---

### 5. OperationalStatusReportResultBean.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/OperationalStatusReportResultBean.java`
- **Lines:** 1-17
- **Class:** `OperationalStatusReportResultBean extends BaseResultBean`
- **Fields:** 1 `List<OperationalStatusReportItemResultBean>` field (initialized to empty `ArrayList`)
- **Inherited from BaseResultBean:** `BaseFilterBean appliedFilterBean` with getter/setter
- **Public methods:**

| # | Method Signature | Line |
|---|-----------------|------|
| 1 | `List<OperationalStatusReportItemResultBean> getItemResultBeanList()` | 10 |
| 2 | `void setItemResultBeanList(List<OperationalStatusReportItemResultBean>)` | 13 |

**Note:** `getItemResultBeanList()` has a null-guard: returns `new ArrayList<>()` if `itemResultBeanList` is null (line 11).

---

### 6. PreOpCheckFailReportBean.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/PreOpCheckFailReportBean.java`
- **Lines:** 1-92
- **Class:** `PreOpCheckFailReportBean` (plain POJO, no superclass)
- **Fields:** 10 package-private `ArrayList` fields (all initialized), 1 `String tot_dur` initialized to `""`, 1 `ArrayList<String> preOpCheckCommentList` initialized
- **Public methods:**

| # | Method Signature | Line |
|---|-----------------|------|
| 1 | `ArrayList getPo_dnm()` | 20 |
| 2 | `void setPo_dnm(ArrayList)` | 23 |
| 3 | `ArrayList getPo_did()` | 26 |
| 4 | `void setPo_did(ArrayList)` | 29 |
| 5 | `ArrayList getPo_sttm()` | 32 |
| 6 | `void setPo_sttm(ArrayList)` | 35 |
| 7 | `ArrayList getPo_comp()` | 38 |
| 8 | `void setPo_comp(ArrayList)` | 41 |
| 9 | `ArrayList getPo_dur()` | 44 |
| 10 | `void setPo_dur(ArrayList)` | 47 |
| 11 | `ArrayList getPo_fail()` | 50 |
| 12 | `void setPo_fail(ArrayList)` | 53 |
| 13 | `ArrayList getPo_machine()` | 56 |
| 14 | `void setPo_machine(ArrayList)` | 59 |
| 15 | `ArrayList getPo_model()` | 62 |
| 16 | `void setPo_model(ArrayList)` | 65 |
| 17 | `String getTot_dur()` | 68 |
| 18 | `void setTot_dur(String)` | 71 |
| 19 | `ArrayList getQ_type()` | 74 |
| 20 | `void setQ_type(ArrayList)` | 77 |
| 21 | `ArrayList getPo_veh_id()` | 80 |
| 22 | `void setPo_veh_id(ArrayList)` | 83 |
| 23 | `ArrayList<String> getPreOpCheckCommentList()` | 86 |
| 24 | `void setPreOpCheckCommentList(ArrayList<String>)` | 89 |

---

### 7. PreOpCheckReportBean.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/PreOpCheckReportBean.java`
- **Lines:** 1-94
- **Class:** `PreOpCheckReportBean` (plain POJO, no superclass)
- **Fields:** Identical field set to PreOpCheckFailReportBean: 10 package-private `ArrayList` fields, 1 `String tot_dur`, 1 `ArrayList<String> preOpCheckCommentList`
- **Public methods:**

| # | Method Signature | Line |
|---|-----------------|------|
| 1 | `ArrayList getPo_dnm()` | 20 |
| 2 | `void setPo_dnm(ArrayList)` | 23 |
| 3 | `ArrayList getPo_did()` | 26 |
| 4 | `void setPo_did(ArrayList)` | 29 |
| 5 | `ArrayList getPo_sttm()` | 32 |
| 6 | `void setPo_sttm(ArrayList)` | 35 |
| 7 | `ArrayList getPo_comp()` | 38 |
| 8 | `void setPo_comp(ArrayList)` | 41 |
| 9 | `ArrayList getPo_dur()` | 44 |
| 10 | `void setPo_dur(ArrayList)` | 47 |
| 11 | `ArrayList getPo_fail()` | 50 |
| 12 | `void setPo_fail(ArrayList)` | 53 |
| 13 | `ArrayList getPo_machine()` | 56 |
| 14 | `void setPo_machine(ArrayList)` | 59 |
| 15 | `ArrayList getPo_model()` | 62 |
| 16 | `void setPo_model(ArrayList)` | 65 |
| 17 | `String getTot_dur()` | 68 |
| 18 | `void setTot_dur(String)` | 71 |
| 19 | `ArrayList getQ_type()` | 74 |
| 20 | `void setQ_type(ArrayList)` | 77 |
| 21 | `ArrayList getPo_veh_id()` | 80 |
| 22 | `void setPo_veh_id(ArrayList)` | 83 |
| 23 | `ArrayList<String> getPreOpCheckCommentList()` | 87 |
| 24 | `void setPreOpCheckCommentList(ArrayList<String>)` | 91 |

---

### 8. SeatHourUtilBean.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/SeatHourUtilBean.java`
- **Lines:** 1-170
- **Class:** `SeatHourUtilBean` (plain POJO, no superclass)
- **Fields:** Identical structure to KeyHourUtilBean: 14 package-private `ArrayList` fields (all initialized), 9 package-private `String` fields (null-default)
- **Public methods:**

| # | Method Signature | Line |
|---|-----------------|------|
| 1 | `ArrayList getVeh_cd()` | 32 |
| 2 | `void setVeh_cd(ArrayList)` | 35 |
| 3 | `ArrayList getVeh_nm()` | 38 |
| 4 | `void setVeh_nm(ArrayList)` | 41 |
| 5 | `ArrayList getVeh_typ_nm1()` | 44 |
| 6 | `void setVeh_typ_nm1(ArrayList)` | 47 |
| 7 | `ArrayList getVutil1()` | 50 |
| 8 | `void setVutil1(ArrayList)` | 53 |
| 9 | `ArrayList getVutil2()` | 56 |
| 10 | `void setVutil2(ArrayList)` | 59 |
| 11 | `ArrayList getVutil3()` | 62 |
| 12 | `void setVutil3(ArrayList)` | 65 |
| 13 | `ArrayList getVutil4()` | 68 |
| 14 | `void setVutil4(ArrayList)` | 71 |
| 15 | `ArrayList getVutil5()` | 74 |
| 16 | `void setVutil5(ArrayList)` | 77 |
| 17 | `ArrayList getVutil6()` | 80 |
| 18 | `void setVutil6(ArrayList)` | 83 |
| 19 | `ArrayList getVutil7()` | 86 |
| 20 | `void setVutil7(ArrayList)` | 89 |
| 21 | `ArrayList getVutil8()` | 92 |
| 22 | `void setVutil8(ArrayList)` | 95 |
| 23 | `ArrayList getVutilt()` | 98 |
| 24 | `void setVutilt(ArrayList)` | 101 |
| 25 | `ArrayList getVutilpt()` | 104 |
| 26 | `void setVutilpt(ArrayList)` | 107 |
| 27 | `String getUtil1()` | 110 |
| 28 | `void setUtil1(String)` | 113 |
| 29 | `String getUtil2()` | 116 |
| 30 | `void setUtil2(String)` | 119 |
| 31 | `String getUtil3()` | 122 |
| 32 | `void setUtil3(String)` | 125 |
| 33 | `String getUtil4()` | 128 |
| 34 | `void setUtil4(String)` | 131 |
| 35 | `String getUtil5()` | 134 |
| 36 | `void setUtil5(String)` | 137 |
| 37 | `String getUtil6()` | 140 |
| 38 | `void setUtil6(String)` | 143 |
| 39 | `String getUtil7()` | 146 |
| 40 | `void setUtil7(String)` | 149 |
| 41 | `String getUtil8()` | 152 |
| 42 | `void setUtil8(String)` | 155 |
| 43 | `String getUtilt()` | 158 |
| 44 | `void setUtilt(String)` | 161 |
| 45 | `ArrayList getVeh_id()` | 164 |
| 46 | `void setVeh_id(ArrayList)` | 167 |

---

### 9. ServMaintenanceReportBean.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/ServMaintenanceReportBean.java`
- **Lines:** 1-141
- **Class:** `ServMaintenanceReportBean` (plain POJO, no superclass)
- **Note:** Duplicate import of `java.util.ArrayList` on lines 3-4.
- **Fields:** 15 `ArrayList` fields (mix of package-private and private, all initialized), 1 `String t_sm_hm_s` initialized to `""`
- **Public methods:**

| # | Method Signature | Line |
|---|-----------------|------|
| 1 | `ArrayList getNextServDate()` | 29 |
| 2 | `void setNextServDate(ArrayList)` | 32 |
| 3 | `ArrayList getDateIntervalList()` | 35 |
| 4 | `void setDateIntervalList(ArrayList)` | 38 |
| 5 | `ArrayList getNextServHourLst()` | 41 |
| 6 | `void setNextServHourLst(ArrayList)` | 44 |
| 7 | `ArrayList getSm_service_from()` | 49 |
| 8 | `void setSm_service_from(ArrayList)` | 52 |
| 9 | `ArrayList getSm_ser_st()` | 55 |
| 10 | `void setSm_ser_st(ArrayList)` | 58 |
| 11 | `ArrayList getSm_ser_ed()` | 61 |
| 12 | `void setSm_ser_ed(ArrayList)` | 64 |
| 13 | `ArrayList getVmachine_cd()` | 68 |
| 14 | `void setVmachine_cd(ArrayList)` | 71 |
| 15 | `ArrayList getVmachine_nm()` | 74 |
| 16 | `void setVmachine_nm(ArrayList)` | 77 |
| 17 | `ArrayList getMachineName()` | 80 |
| 18 | `void setMachineName(ArrayList)` | 83 |
| 19 | `ArrayList getSm_ser_ed2()` | 86 |
| 20 | `void setSm_ser_ed2(ArrayList)` | 89 |
| 21 | `ArrayList getLastServDateList()` | 92 |
| 22 | `void setLastServDateList(ArrayList)` | 95 |
| 23 | `ArrayList getServHourIntervalList()` | 98 |
| 24 | `void setServHourIntervalList(ArrayList)` | 101 |
| 25 | `ArrayList getService_id()` | 104 |
| 26 | `void setService_id(ArrayList)` | 107 |
| 27 | `ArrayList getSm_hour_meter()` | 110 |
| 28 | `void setSm_hour_meter(ArrayList)` | 113 |
| 29 | `ArrayList getService_hour()` | 116 |
| 30 | `void setService_hour(ArrayList)` | 119 |
| 31 | `String getT_sm_hm_s()` | 122 |
| 32 | `void setT_sm_hm_s(String)` | 125 |
| 33 | `ArrayList getVs_no()` | 128 |
| 34 | `void setVs_no(ArrayList)` | 131 |
| 35 | `ArrayList getCustomerName()` | 135 |
| 36 | `void setCustomerName(ArrayList)` | 138 |

---

### 10. SuperMasterAuthReportBean.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/SuperMasterAuthReportBean.java`
- **Lines:** 1-20
- **Class:** `SuperMasterAuthReportBean` (plain POJO, no superclass)
- **Fields:** 1 `ArrayList<SuperMasterAuthBean>` field (initialized with raw-type `new ArrayList()`)
- **Public methods:**

| # | Method Signature | Line |
|---|-----------------|------|
| 1 | `ArrayList<SuperMasterAuthBean> getSuperMasterAuths()` | 11 |
| 2 | `void setSuperMasterAuths(ArrayList<SuperMasterAuthBean>)` | 15 |

---

### 11. UnitUnlockReportBean.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/UnitUnlockReportBean.java`
- **Lines:** 1-78
- **Class:** `UnitUnlockReportBean` (plain POJO, no superclass)
- **Fields:** 9 package-private `ArrayList` fields (all initialized), 1 `String filter` initialized to `""`
- **Public methods:**

| # | Method Signature | Line |
|---|-----------------|------|
| 1 | `ArrayList getVunit_name()` | 18 |
| 2 | `void setVunit_name(ArrayList)` | 21 |
| 3 | `ArrayList getVunit_loreason()` | 24 |
| 4 | `void setVunit_loreason(ArrayList)` | 27 |
| 5 | `ArrayList getVunit_lotm()` | 30 |
| 6 | `void setVunit_lotm(ArrayList)` | 33 |
| 7 | `ArrayList getVunit_lodriver()` | 36 |
| 8 | `void setVunit_lodriver(ArrayList)` | 39 |
| 9 | `ArrayList getVunit_ultm()` | 42 |
| 10 | `void setVunit_ultm(ArrayList)` | 45 |
| 11 | `ArrayList getVunit_uldriver()` | 48 |
| 12 | `void setVunit_uldriver(ArrayList)` | 51 |
| 13 | `ArrayList getVunit_unloreason()` | 54 |
| 14 | `void setVunit_unloreason(ArrayList)` | 57 |
| 15 | `ArrayList getVunit_isImpReal()` | 60 |
| 16 | `void setVunit_isImpReal(ArrayList)` | 63 |
| 17 | `ArrayList getVunit_veh_id()` | 66 |
| 18 | `void setVunit_veh_id(ArrayList)` | 69 |
| 19 | `String getFilter()` | 72 |
| 20 | `void setFilter(String)` | 75 |

---

### 12. UtilWowReportBean.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/UtilWowReportBean.java`
- **Lines:** 1-74
- **Class:** `UtilWowReportBean` (plain POJO, no superclass)
- **Fields:** 5 package-private `String` fields (null-default), 1 `String chartUrl` (null-default), 1 package-private `ArrayList util` (initialized)
- **Public methods:**

| # | Method Signature | Line |
|---|-----------------|------|
| 1 | `String getGet_user()` | 16 |
| 2 | `void setGet_user(String)` | 20 |
| 3 | `String getGet_loc()` | 24 |
| 4 | `void setGet_loc(String)` | 28 |
| 5 | `String getGet_dep()` | 32 |
| 6 | `void setGet_dep(String)` | 36 |
| 7 | `String getGet_mod()` | 40 |
| 8 | `void setGet_mod(String)` | 44 |
| 9 | `String getForm_nm()` | 48 |
| 10 | `void setForm_nm(String)` | 52 |
| 11 | `ArrayList getUtil()` | 56 |
| 12 | `void setUtil(ArrayList)` | 60 |
| 13 | `String getChartUrl()` | 64 |
| 14 | `void setChartUrl(String)` | 68 |

---

### 13. UtilisationReportBean.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/UtilisationReportBean.java`
- **Lines:** 1-168
- **Class:** `UtilisationReportBean` (plain POJO, no superclass)
- **Note:** Duplicate import of `java.util.ArrayList` on lines 3-4.
- **Fields:** 8 package-private `ArrayList` fields (initialized), 1 `ArrayList<UnitUtilSummaryBean>` (initialized), 4 `String` fields initialized to `""`, 8 `String` fields initialized to `""`
- **Public methods:**

| # | Method Signature | Line |
|---|-----------------|------|
| 1 | `ArrayList getGroup_cd()` | 33 |
| 2 | `void setGroup_cd(ArrayList)` | 37 |
| 3 | `ArrayList getGroup_nm()` | 40 |
| 4 | `void setGroup_nm(ArrayList)` | 43 |
| 5 | `ArrayList getUser_cd()` | 46 |
| 6 | `void setUser_cd(ArrayList)` | 49 |
| 7 | `ArrayList getUser_nm()` | 52 |
| 8 | `void setUser_nm(ArrayList)` | 55 |
| 9 | `ArrayList getLocation_cd()` | 58 |
| 10 | `void setLocation_cd(ArrayList)` | 61 |
| 11 | `ArrayList getLocation_nm()` | 64 |
| 12 | `void setLocation_nm(ArrayList)` | 67 |
| 13 | `ArrayList getVdep_cd()` | 70 |
| 14 | `void setVdep_cd(ArrayList)` | 73 |
| 15 | `ArrayList getVdep_nm()` | 76 |
| 16 | `void setVdep_nm(ArrayList)` | 79 |
| 17 | `String getGet_gp()` | 82 |
| 18 | `void setGet_gp(String)` | 85 |
| 19 | `String getGet_user_nm()` | 88 |
| 20 | `void setGet_user_nm(String)` | 91 |
| 21 | `String getLoc_name_disp()` | 94 |
| 22 | `void setLoc_name_disp(String)` | 97 |
| 23 | `String getDept_name_disp()` | 100 |
| 24 | `void setDept_name_disp(String)` | 103 |
| 25 | `ArrayList<UnitUtilSummaryBean> getArrUnitUtil()` | 106 |
| 26 | `void setArrUnitUtil(ArrayList<UnitUtilSummaryBean>)` | 109 |
| 27 | `String gettTotal()` | 112 |
| 28 | `void settTotal(String)` | 115 |
| 29 | `String gettKey()` | 118 |
| 30 | `void settKey(String)` | 121 |
| 31 | `String gettKeyPer()` | 124 |
| 32 | `void settKeyPer(String)` | 127 |
| 33 | `String gettSeat()` | 130 |
| 34 | `void settSeat(String)` | 133 |
| 35 | `String gettSeatPer()` | 136 |
| 36 | `void settSeatPer(String)` | 139 |
| 37 | `String gettTrack()` | 142 |
| 38 | `void settTrack(String)` | 145 |
| 39 | `String gettTrackPer()` | 148 |
| 40 | `void settTrackPer(String)` | 151 |
| 41 | `String gettHydr()` | 154 |
| 42 | `void settHydr(String)` | 157 |
| 43 | `String gettHydrPer()` | 160 |
| 44 | `void settHydrPer(String)` | 163 |

---

### 14. CustomerDAO.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/dao/CustomerDAO.java`
- **Lines:** 1-206
- **Class:** `CustomerDAO` (plain class, no superclass, no interface)
- **Dependencies:** `java.sql.Connection`, `java.sql.ResultSet`, `java.sql.Statement`, `DBUtil`, `RuntimeConf`
- **Public methods:**

| # | Method Signature | Line | Description |
|---|-----------------|------|-------------|
| 1 | `String getCustomerName(String cust_cd) throws SQLException` | 17 | Queries `FMS_CUST_MST` by `USER_CD` |
| 2 | `String getLocationName(String loc_cd) throws SQLException` | 55 | Queries `FMS_LOC_MST` by `LOCATION_CD` |
| 3 | `String getDepartmentName(String dept_cd) throws SQLException` | 92 | Queries `FMS_DEPT_MST` by `DEPT_CD` |
| 4 | `String getModelName(String model_cd) throws SQLException` | 129 | Queries `FMS_VEHICLE_TYPE_MST` by `VEHICLE_TYPE_CD` |
| 5 | `String getFormName(String form_cd) throws SQLException` | 165 | Queries `RuntimeConf.form_table` by `FORM_CD` |

---

### 15. DriverAccessAbuseDAO.java
- **Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/dao/DriverAccessAbuseDAO.java`
- **Lines:** 1-64
- **Class:** `DriverAccessAbuseDAO` (plain class, no superclass, no interface)
- **Dependencies:** `DriverAccessAbuseBean`, `Databean_report`, `DBUtil`
- **Fields:** 13 instance-level `ArrayList` fields (all initialized) -- appear unused (state populated but never read; delegation goes through `Databean_report`)
- **Public methods:**

| # | Method Signature | Line | Description |
|---|-----------------|------|-------------|
| 1 | `DriverAccessAbuseBean getAbuseBean(String set_cust_cd, String set_loc_cd, String set_dept_cd, String st_dt, String end_dt, String report_filter, String a_time_filter) throws SQLException` | 33 | Delegates to `Databean_report.init()` to run queries, then maps results into `DriverAccessAbuseBean` |

---

## Findings

### A14-01 -- CRITICAL: Zero test infrastructure across entire repository
**Severity:** CRITICAL
**Scope:** All 15 files
**Current coverage:** 0%

The repository contains no test framework dependency (JUnit, TestNG), no test source directory, no test runner configuration, and no CI/CD test stage. All 15 audited files have exactly 0% automated test coverage. The single file named `EncryptTest.java` is a decompiled utility class, not a test.

**Impact:** Any regression, refactoring error, or behavioral change in these files will go undetected until runtime in production.

---

### A14-02 -- HIGH: SQL Injection in CustomerDAO -- all 5 query methods use string concatenation
**Severity:** HIGH (CRITICAL from security perspective)
**File:** `CustomerDAO.java` (lines 32, 70, 107, 144, 180-181)
**Coverage:** 0% -- no tests exist

All five public methods in `CustomerDAO` build SQL queries via string concatenation with caller-supplied parameters:

```java
// Line 32
String sql = "select \"USER_NAME\" from \"FMS_CUST_MST\" where \"USER_CD\" = " + cust_cd;

// Line 70
String sql = "select \"NAME\" from \"FMS_LOC_MST\" where \"LOCATION_CD\" = " + loc_cd;

// Line 107
String sql = "select \"DEPT_NAME\" from \"FMS_DEPT_MST\" where \"DEPT_CD\" = " + dept_cd;

// Line 144
String sql = "select \"VEHICLE_TYPE\" from \"FMS_VEHICLE_TYPE_MST\" where \"VEHICLE_TYPE_CD\" = " + model_cd;

// Line 180-181
String query = "select \"FORM_NAME\"  from "+RuntimeConf.form_table+" where \"FORM_CD\"='" + form_cd + "' ";
```

**Tests needed:**
- Parameterized injection payloads (`'; DROP TABLE --`, `1 OR 1=1`) to confirm vulnerability
- Normal lookup returning expected value
- Lookup with empty/null/zero/"all" input (boundary guard paths)
- Lookup returning no rows (default "All" return)
- Exception path (database down, invalid connection)

---

### A14-03 -- HIGH: CustomerDAO exception handling swallows errors silently
**Severity:** HIGH
**File:** `CustomerDAO.java` (lines 41-44, 78-81, 115-118, 152-155, 190-193)
**Coverage:** 0%

All five methods catch `Exception`, call `e.printStackTrace()` and `e.getMessage()` (the latter is a no-op -- result discarded), then return a default value (`"All"` or `"unknown report"`). The caller has no way to distinguish "no data found" from "database error."

**Tests needed:**
- Verify behavior under database connection failure
- Verify behavior when `DBUtil.getConnection()` returns null
- Verify that `rs.close()` / `stmt.close()` in `finally` block do not throw when `rs` is null (they are guarded, but this needs confirmation)

---

### A14-04 -- HIGH: CustomerDAO.getFormName() has a logic bug -- checks `formName` instead of `form_cd`
**Severity:** HIGH
**File:** `CustomerDAO.java` (line 177)
**Coverage:** 0%

```java
// Line 177: formName is initialized to "unknown report" on line 170
// This condition checks formName (always "unknown report") instead of form_cd
if (!formName.equalsIgnoreCase("")
    && !formName.equalsIgnoreCase("0")
    && !formName.equalsIgnoreCase("all") && !form_cd.equalsIgnoreCase("")) {
```

The first three conditions (`formName != ""`, `formName != "0"`, `formName != "all"`) will always be `true` because `formName` is initialized to `"unknown report"`. This means the guard against empty/zero/all for `form_cd` is partially broken -- only the `!form_cd.equalsIgnoreCase("")` check is effective. The other four methods correctly check the input parameter (`cust_cd`, `loc_cd`, etc.), making this inconsistency appear to be a copy-paste bug.

**Tests needed:**
- Call `getFormName("0")` -- should return "unknown report" per pattern but currently executes the query
- Call `getFormName("all")` -- same issue
- Call `getFormName("")` -- this case IS correctly guarded

---

### A14-05 -- HIGH: DriverAccessAbuseDAO delegates all data access through Databean_report with no error handling
**Severity:** HIGH
**File:** `DriverAccessAbuseDAO.java` (lines 33-63)
**Coverage:** 0%

The `getAbuseBean()` method delegates entirely to `Databean_report.init()` (line 48) which presumably executes database queries internally. The DAO method:
- Declares `throws SQLException` but has no try/catch
- Does not validate any of the 7 string parameters for null
- Does not check the result of `dbreport.init()` for errors
- Has 13 unused instance-level `ArrayList` fields (dead code, lines 18-31)

**Tests needed:**
- Null parameter handling (any of the 7 string arguments)
- Verify `Databean_report.init()` error propagation
- Verify correct mapping of all 10 fields from `Databean_report` to `DriverAccessAbuseBean`
- Empty result set behavior
- Confirm dead instance fields are truly unused

---

### A14-06 -- MEDIUM: HireDehireReportBean fields default to null -- NullPointerException risk
**Severity:** MEDIUM
**File:** `HireDehireReportBean.java` (lines 6-13)
**Coverage:** 0%

All 8 `ArrayList` fields are declared `private` but never initialized (default `null`). Unlike most other beans in this audit which initialize fields with `new ArrayList()`, this bean will throw `NullPointerException` if any getter is called before the corresponding setter.

**Tests needed:**
- Instantiate bean, call any getter without calling setter first -- should expose NPE
- Roundtrip: set value, get value, verify equality

---

### A14-07 -- MEDIUM: ImpactReportBean has inconsistent field initialization
**Severity:** MEDIUM
**File:** `ImpactReportBean.java` (lines 7-21)
**Coverage:** 0%

Seven `ArrayList` fields (`machineId`, `vehId`, `model`, `driverName`, `cardNo`, `dtImpact`, `severityLvl`) are declared `private` without initialization (null by default). Four other `ArrayList` fields (`meterDetails`, `Vtmp_imp_data`, `vimp_shock_id`, `vimp_rtlsjson`) are initialized to `new ArrayList()`. The `String fileName` field defaults to null. Callers face inconsistent null/non-null behavior depending on which field they access.

**Tests needed:**
- Call getters on uninitialized fields -- verify NPE or null return
- Validate consistent post-setter behavior

---

### A14-08 -- MEDIUM: PreOpCheckReportBean and PreOpCheckFailReportBean are near-identical duplicates
**Severity:** MEDIUM
**Files:** `PreOpCheckReportBean.java`, `PreOpCheckFailReportBean.java`
**Coverage:** 0%

These two classes have identical field sets, identical method signatures, and identical method implementations. The only differences are the class name and minor whitespace. This code duplication means any bug fixed in one must be manually replicated in the other.

**Tests needed (for each):**
- Bean roundtrip for all 12 field pairs
- Null-safety since fields are package-private and initialized

---

### A14-09 -- MEDIUM: KeyHourUtilBean and SeatHourUtilBean are near-identical duplicates
**Severity:** MEDIUM
**Files:** `KeyHourUtilBean.java`, `SeatHourUtilBean.java`
**Coverage:** 0%

These two classes have identical field structures (14 `ArrayList` fields, 9 `String` fields), identical getter/setter signatures, and identical implementations. Same duplication risk as A14-08.

**Tests needed (for each):**
- Bean roundtrip for all 23 field pairs
- Verify String fields default to null (not initialized)

---

### A14-10 -- LOW: Pervasive use of raw-typed ArrayList across all 13 bean classes
**Severity:** LOW
**Scope:** All 13 bean files
**Coverage:** 0%

Nearly all `ArrayList` fields use raw types (e.g., `ArrayList` instead of `ArrayList<String>`). Only a few fields use generics (`ArrayList<String> preOpCheckCommentList`, `ArrayList<SuperMasterAuthBean>`, `ArrayList<UnitUtilSummaryBean>`, `List<OperationalStatusReportItemResultBean>`). Raw types bypass compile-time type safety and allow `ClassCastException` at runtime.

**Tests needed:**
- Type-safety tests verifying expected element types in each ArrayList
- Serialization/deserialization tests if beans are used in session/cache

---

### A14-11 -- LOW: CustomerDAO uses Statement instead of PreparedStatement
**Severity:** LOW (contributes to A14-02 SQL injection risk)
**File:** `CustomerDAO.java` (lines 28, 66, 103, 140, 174)
**Coverage:** 0%

All five methods use `conn.createStatement(ResultSet.TYPE_SCROLL_SENSITIVE, ResultSet.CONCUR_READ_ONLY)` instead of `PreparedStatement`. This requires `TYPE_SCROLL_SENSITIVE` which is more expensive than `TYPE_FORWARD_ONLY`, and the scroll capability is never used (only `rs.next()` is called, never `rs.previous()` or `rs.absolute()`).

**Tests needed:**
- Performance comparison with PreparedStatement and TYPE_FORWARD_ONLY
- Confirm scroll-sensitive is unnecessary

---

### A14-12 -- LOW: DriverAccessAbuseDAO contains 13 dead instance fields
**Severity:** LOW
**File:** `DriverAccessAbuseDAO.java` (lines 18-31)
**Coverage:** 0%

The DAO declares 13 `ArrayList` instance fields (`a_driv_cd`, `a_driv_nm`, `a_driv_id`, `a_veh_cd`, `a_veh_nm`, `a_veh_typ_cd`, `a_veh_typ_nm`, `a_veh_srno`, `a_st_tm`, `a_end_tm`, `a_date`, `a_ol_start_list`, `a_ol_end_list`) that are never read or written by any method in the class. The single public method `getAbuseBean()` uses only local variables and the `Databean_report` delegate. These appear to be remnants of a previous implementation.

**Tests needed:**
- Confirm fields are unused via static analysis
- Verify removal does not break reflection-based consumers

---

### A14-13 -- LOW: OperationalStatusReportResultBean null guard creates new list on every call
**Severity:** LOW
**File:** `OperationalStatusReportResultBean.java` (line 11)
**Coverage:** 0%

```java
return this.itemResultBeanList == null ? new ArrayList<>() : this.itemResultBeanList;
```

If `itemResultBeanList` is set to null, each call to `getItemResultBeanList()` returns a **new** empty list. Callers who add items to the returned list will lose them since the backing field remains null.

**Tests needed:**
- Set field to null, call getter, add item, call getter again -- verify item is lost
- Verify whether any caller depends on mutating the returned list

---

## Summary Table

| ID | File(s) | Severity | Category | Tests Exist |
|----|---------|----------|----------|-------------|
| A14-01 | All 15 files | CRITICAL | No test infrastructure | No |
| A14-02 | CustomerDAO.java | HIGH | SQL injection (5 methods) | No |
| A14-03 | CustomerDAO.java | HIGH | Silent error swallowing | No |
| A14-04 | CustomerDAO.java | HIGH | Logic bug in getFormName() | No |
| A14-05 | DriverAccessAbuseDAO.java | HIGH | No null checks, no error handling, dead code | No |
| A14-06 | HireDehireReportBean.java | MEDIUM | Null-default fields (NPE risk) | No |
| A14-07 | ImpactReportBean.java | MEDIUM | Inconsistent field initialization | No |
| A14-08 | PreOpCheckReportBean + PreOpCheckFailReportBean | MEDIUM | Code duplication | No |
| A14-09 | KeyHourUtilBean + SeatHourUtilBean | MEDIUM | Code duplication | No |
| A14-10 | All 13 beans | LOW | Raw-typed ArrayList | No |
| A14-11 | CustomerDAO.java | LOW | Statement vs PreparedStatement, unnecessary scroll sensitivity | No |
| A14-12 | DriverAccessAbuseDAO.java | LOW | 13 dead instance fields | No |
| A14-13 | OperationalStatusReportResultBean.java | LOW | Null-guard creates ephemeral list | No |

---

## Priority Recommendations for Test Introduction

1. **Immediate (HIGH):** `CustomerDAO.java` -- 5 public methods performing direct SQL with string concatenation. Tests should cover SQL injection vectors, null/empty parameter guards, error path behavior, and the `getFormName()` logic bug (A14-02, A14-03, A14-04).
2. **Immediate (HIGH):** `DriverAccessAbuseDAO.java` -- 1 public method with 7 unvalidated parameters delegating to `Databean_report`. Tests should cover null parameters, delegation correctness, and error propagation (A14-05).
3. **Short-term (MEDIUM):** Bean classes with null-default fields (`HireDehireReportBean`, `ImpactReportBean`) should have basic instantiation + roundtrip tests to prevent NPE regressions (A14-06, A14-07).
4. **Deferred (LOW):** Remaining bean classes are simple POJOs with getters/setters. While untested, they carry lower standalone risk. Testing priority should increase if they are used in serialization, caching, or session storage.
