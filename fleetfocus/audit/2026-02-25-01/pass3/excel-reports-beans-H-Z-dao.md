# Pass 3 -- Documentation Audit
## Scope: `excel/reports/beans` (H-Z) + `excel/reports/dao`
**Agent:** A14
**Date:** 2026-02-25
**Branch:** `release/UAT_RELEASE_FLEETFOCUS_Production`
**Base path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/`

---

## 1. HireDehireReportBean.java
**Path:** `beans/HireDehireReportBean.java`
**Lines:** 63

### Reading Evidence
Plain POJO/data-transfer bean. Contains 8 private `ArrayList` (raw-typed) fields: `veh_serial`, `veh_gmtp`, `veh_hire`, `hire_time`, `dehire_time`, `cust_name`, `loc_nm`, `dep_nm`. Provides getter/setter pairs for each. No business logic, no constructors beyond the implicit default.

### Class-Level Javadoc
**None.** No class-level Javadoc comment exists.

### Method-Level Javadoc
**None.** Zero methods carry Javadoc.

### Undocumented Public Methods (16)
| Method | Line |
|--------|------|
| `getVeh_serial()` | 14 |
| `setVeh_serial(ArrayList)` | 17 |
| `getVeh_gmtp()` | 20 |
| `setVeh_gmtp(ArrayList)` | 23 |
| `getVeh_hire()` | 26 |
| `setVeh_hire(ArrayList)` | 29 |
| `getHire_time()` | 32 |
| `setHire_time(ArrayList)` | 35 |
| `getDehire_time()` | 38 |
| `setDehire_time(ArrayList)` | 41 |
| `getCust_name()` | 44 |
| `setCust_name(ArrayList)` | 47 |
| `getLoc_nm()` | 50 |
| `setLoc_nm(ArrayList)` | 53 |
| `getDep_nm()` | 56 |
| `setDep_nm(ArrayList)` | 59 |

### Accuracy of Existing Documentation
N/A -- no documentation exists to evaluate.

### TODO / FIXME / HACK / XXX
None found.

---

## 2. ImpactReportBean.java
**Path:** `beans/ImpactReportBean.java`
**Lines:** 121

### Reading Evidence
Data-transfer bean for impact (shock event) reports. Contains 14 fields mixing raw `ArrayList` and primitives: `machineId`, `vehId`, `model`, `driverName`, `cardNo`, `dtImpact`, `severityLvl`, `fileName` (String), `photoTotal` (int), `Vimp_img`, `meterDetails`, `Vtmp_imp_data`, `vimp_shock_id`, `vimp_rtlsjson`, plus a `boolean rtlsEnabled` flag. Fields `Vimp_img` and `Vtmp_imp_data` use uppercase-starting names violating Java naming conventions. All fields have getter/setter pairs. No business logic.

### Class-Level Javadoc
**None.**

### Method-Level Javadoc
**None.** Zero methods carry Javadoc.

### Undocumented Public Methods (28)
| Method | Line |
|--------|------|
| `getVimp_shock_id()` | 23 |
| `getVimp_rtlsjson()` | 26 |
| `isRtlsEnabled()` | 29 |
| `setVimp_shock_id(ArrayList)` | 32 |
| `setVimp_rtlsjson(ArrayList)` | 35 |
| `setRtlsEnabled(boolean)` | 38 |
| `getVtmp_imp_data()` | 41 |
| `setVtmp_imp_data(ArrayList)` | 44 |
| `getMachineId()` | 48 |
| `getModel()` | 51 |
| `getDriverName()` | 54 |
| `getCardNo()` | 57 |
| `getDtImpact()` | 60 |
| `getSeverityLvl()` | 63 |
| `getFileName()` | 66 |
| `setMachineId(ArrayList)` | 69 |
| `setModel(ArrayList)` | 72 |
| `setDriverName(ArrayList)` | 75 |
| `setCardNo(ArrayList)` | 78 |
| `setDtImpact(ArrayList)` | 81 |
| `setSeverityLvl(ArrayList)` | 84 |
| `setFileName(String)` | 87 |
| `getPhotoTotal()` | 90 |
| `setPhotoTotal(int)` | 93 |
| `getVimp_img()` | 96 |
| `setVimp_img(ArrayList)` | 99 |
| `getMeterDetails()` | 102 |
| `setMeterDetails(ArrayList)` | 105 |
| `getVehId()` | 108 |
| `setVehId(ArrayList)` | 111 |

### Accuracy of Existing Documentation
N/A -- no documentation exists.

### TODO / FIXME / HACK / XXX
None found.

---

## 3. KeyHourUtilBean.java
**Path:** `beans/KeyHourUtilBean.java`
**Lines:** 171

### Reading Evidence
Data-transfer bean for key-hour utilisation reports. Contains 23 fields: 4 vehicle-identifying `ArrayList` fields (`veh_cd`, `veh_nm`, `veh_id`, `veh_typ_nm1`), 10 `ArrayList` utilisation-value columns (`vutil1`..`vutil8`, `vutilt`, `vutilpt`), and 9 `String` header/label fields (`util1`..`util8`, `utilt`). All fields are package-private (no access modifier). Provides getter/setter pairs for each. No business logic.

### Class-Level Javadoc
**None.**

### Method-Level Javadoc
**None.**

### Undocumented Public Methods (46)
All 23 getter/setter pairs (46 methods total, lines 32-169). Representative samples:
`getVeh_cd()`, `setVeh_cd(ArrayList)`, `getVutil1()`, `setVutil1(ArrayList)`, `getUtil1()`, `setUtil1(String)`, `getVeh_id()`, `setVeh_id(ArrayList)`, etc.

### Accuracy of Existing Documentation
N/A -- no documentation exists.

### TODO / FIXME / HACK / XXX
None found.

---

## 4. OperationalStatusReportItemResultBean.java
**Path:** `beans/OperationalStatusReportItemResultBean.java`
**Lines:** 63

### Reading Evidence
Data-transfer bean extending `BaseItemResultBean` (which is itself an empty class). Contains 8 package-private `String` fields initialised to `""`: `equipNo`, `serialNo`, `model`, `triggerType`, `status`, `initiatedBy`, `setTime`, `note`. Each has a getter/setter pair. Getters use explicit `this.` prefix. No business logic.

### Class-Level Javadoc
**None.**

### Method-Level Javadoc
**None.**

### Undocumented Public Methods (16)
| Method | Line |
|--------|------|
| `getEquipNo()` | 14 |
| `setEquipNo(String)` | 17 |
| `getSerialNo()` | 20 |
| `setSerialNo(String)` | 23 |
| `getModel()` | 26 |
| `setModel(String)` | 29 |
| `getTriggerType()` | 32 |
| `setTriggerType(String)` | 35 |
| `getStatus()` | 38 |
| `setStatus(String)` | 41 |
| `getInitiatedBy()` | 44 |
| `setInitiatedBy(String)` | 47 |
| `getSetTime()` | 50 |
| `setSetTime(String)` | 53 |
| `getNote()` | 56 |
| `setNote(String)` | 59 |

### Accuracy of Existing Documentation
N/A -- no documentation exists.

### TODO / FIXME / HACK / XXX
None found.

---

## 5. OperationalStatusReportResultBean.java
**Path:** `beans/OperationalStatusReportResultBean.java`
**Lines:** 18

### Reading Evidence
Data-transfer bean extending `BaseResultBean` (which holds one `BaseFilterBean appliedFilterBean` field). Contains a single parameterised field `List<OperationalStatusReportItemResultBean> itemResultBeanList` with getter/setter. Getter includes a null-safe fallback returning a new empty `ArrayList` if the internal list is null. This is the only bean in scope using generics on its list field. No business logic.

### Class-Level Javadoc
**None.**

### Method-Level Javadoc
**None.**

### Undocumented Public Methods (2)
| Method | Line |
|--------|------|
| `getItemResultBeanList()` | 10 |
| `setItemResultBeanList(List<OperationalStatusReportItemResultBean>)` | 13 |

### Accuracy of Existing Documentation
N/A -- no documentation exists.

### TODO / FIXME / HACK / XXX
None found.

---

## 6. PreOpCheckFailReportBean.java
**Path:** `beans/PreOpCheckFailReportBean.java`
**Lines:** 93

### Reading Evidence
Data-transfer bean for pre-operational check failure reports. Contains 12 fields: 10 raw `ArrayList` fields (`po_dnm`, `po_did`, `po_sttm`, `po_comp`, `po_dur`, `po_fail`, `po_machine`, `po_veh_id`, `po_model`, `q_type`), one `String` field (`tot_dur`, initialised to `""`), and one parameterised `ArrayList<String> preOpCheckCommentList`. All list fields are package-private. Each field has a getter/setter pair. No business logic.

### Class-Level Javadoc
**None.**

### Method-Level Javadoc
**None.**

### Undocumented Public Methods (24)
All 12 getter/setter pairs (24 methods, lines 20-91). Representative: `getPo_dnm()`, `setPo_dnm(ArrayList)`, `getTot_dur()`, `getPreOpCheckCommentList()`, etc.

### Accuracy of Existing Documentation
N/A -- no documentation exists.

### TODO / FIXME / HACK / XXX
None found.

---

## 7. PreOpCheckReportBean.java
**Path:** `beans/PreOpCheckReportBean.java`
**Lines:** 95

### Reading Evidence
Data-transfer bean for pre-operational check reports. Structurally near-identical to `PreOpCheckFailReportBean`: same 12 fields with the same names and types, same getter/setter pairs. Fields are package-private raw `ArrayList` types plus `String tot_dur` and `ArrayList<String> preOpCheckCommentList`. The two classes appear to be duplicates with only the class name differing.

### Class-Level Javadoc
**None.**

### Method-Level Javadoc
**None.**

### Undocumented Public Methods (24)
All 12 getter/setter pairs (24 methods, lines 20-93). Same method signatures as `PreOpCheckFailReportBean`.

### Accuracy of Existing Documentation
N/A -- no documentation exists.

### TODO / FIXME / HACK / XXX
None found.

---

## 8. SeatHourUtilBean.java
**Path:** `beans/SeatHourUtilBean.java`
**Lines:** 171

### Reading Evidence
Data-transfer bean for seat-hour utilisation reports. Structurally identical to `KeyHourUtilBean`: same 23 fields (4 vehicle-identifying `ArrayList`s, 10 utilisation `ArrayList`s, 9 `String` label fields) with the same names and types, same getter/setter pairs. Fields are package-private. The two classes appear to be duplicates differing only in class name.

### Class-Level Javadoc
**None.**

### Method-Level Javadoc
**None.**

### Undocumented Public Methods (46)
All 23 getter/setter pairs (46 methods, lines 32-169). Same method signatures as `KeyHourUtilBean`.

### Accuracy of Existing Documentation
N/A -- no documentation exists.

### TODO / FIXME / HACK / XXX
None found.

---

## 9. ServMaintenanceReportBean.java
**Path:** `beans/ServMaintenanceReportBean.java`
**Lines:** 142

### Reading Evidence
Data-transfer bean for service/maintenance reports. Contains 18 fields: a mix of package-private and private `ArrayList` fields covering service scheduling data (`sm_service_from`, `sm_ser_st`, `sm_ser_ed`, `vmachine_cd`, `vmachine_nm`, `vs_no`, `machineName`, `sm_ser_ed2`, `lastServDateList`, `nextServDate`, `servHourIntervalList`, `service_id`, `sm_hour_meter`, `service_hour`, `nextServHourLst`, `dateIntervalList`, `customerName`) and one `String` field (`t_sm_hm_s`). Has a duplicate import of `java.util.ArrayList` at line 4. All fields have getter/setter pairs. No business logic.

### Class-Level Javadoc
**None.**

### Method-Level Javadoc
**None.**

### Undocumented Public Methods (36)
All 18 getter/setter pairs (36 methods, lines 29-140). Representative: `getNextServDate()`, `getSm_service_from()`, `getCustomerName()`, `getT_sm_hm_s()`, etc.

### Accuracy of Existing Documentation
N/A -- no documentation exists.

### TODO / FIXME / HACK / XXX
None found.

---

## 10. SuperMasterAuthReportBean.java
**Path:** `beans/SuperMasterAuthReportBean.java`
**Lines:** 21

### Reading Evidence
Data-transfer bean wrapping a single field `ArrayList<SuperMasterAuthBean> superMasterAuths`. Imports `com.torrent.surat.fms6.bean.SuperMasterAuthBean`. Initialised with raw-type `new ArrayList()` despite the parameterised declaration. Single getter/setter pair. No business logic.

### Class-Level Javadoc
**None.**

### Method-Level Javadoc
**None.**

### Undocumented Public Methods (2)
| Method | Line |
|--------|------|
| `getSuperMasterAuths()` | 11 |
| `setSuperMasterAuths(ArrayList<SuperMasterAuthBean>)` | 15 |

### Accuracy of Existing Documentation
N/A -- no documentation exists.

### TODO / FIXME / HACK / XXX
None found.

---

## 11. UnitUnlockReportBean.java
**Path:** `beans/UnitUnlockReportBean.java`
**Lines:** 79

### Reading Evidence
Data-transfer bean for unit-lock/unlock reports. Contains 10 fields: 9 package-private raw `ArrayList` fields (`vunit_name`, `vunit_veh_id`, `vunit_loreason`, `vunit_lotm`, `vunit_lodriver`, `vunit_ultm`, `vunit_uldriver`, `vunit_unloreason`, `vunit_isImpReal`) and 1 `String filter` initialised to `""`. Each field has a getter/setter pair. No business logic.

### Class-Level Javadoc
**None.**

### Method-Level Javadoc
**None.**

### Undocumented Public Methods (20)
All 10 getter/setter pairs (20 methods, lines 18-77). Representative: `getVunit_name()`, `getVunit_isImpReal()`, `getFilter()`, etc.

### Accuracy of Existing Documentation
N/A -- no documentation exists.

### TODO / FIXME / HACK / XXX
None found.

---

## 12. UtilWowReportBean.java
**Path:** `beans/UtilWowReportBean.java`
**Lines:** 75

### Reading Evidence
Data-transfer bean for week-over-week utilisation reports. Contains 7 package-private fields: 5 `String` fields (`get_user`, `get_loc`, `get_dep`, `get_mod`, `form_nm`, `chartUrl`) and 1 raw `ArrayList util`. Each field has a getter/setter pair. No business logic.

### Class-Level Javadoc
**None.**

### Method-Level Javadoc
**None.**

### Undocumented Public Methods (14)
All 7 getter/setter pairs (14 methods, lines 16-70). Representative: `getGet_user()`, `getGet_loc()`, `getUtil()`, `getChartUrl()`, etc.

### Accuracy of Existing Documentation
N/A -- no documentation exists.

### TODO / FIXME / HACK / XXX
None found.

---

## 13. UtilisationReportBean.java
**Path:** `beans/UtilisationReportBean.java`
**Lines:** 169

### Reading Evidence
Data-transfer bean for utilisation summary reports. Contains 22 fields: 8 raw `ArrayList` fields (`group_cd`, `group_nm`, `user_cd`, `user_nm`, `location_cd`, `location_nm`, `vdep_cd`, `vdep_nm`), 1 parameterised `ArrayList<UnitUtilSummaryBean> arrUnitUtil`, and 13 `String` fields covering display names and totals (`get_gp`, `get_user_nm`, `loc_name_disp`, `dept_name_disp`, `tTotal`, `tKey`, `tKeyPer`, `tSeat`, `tSeatPer`, `tTrack`, `tTrackPer`, `tHydr`, `tHydrPer`). All fields are package-private. Has duplicate import of `java.util.ArrayList` at lines 3-4. Imports `com.torrent.surat.fms6.bean.UnitUtilSummaryBean`. All fields have getter/setter pairs. No business logic.

### Class-Level Javadoc
**None.**

### Method-Level Javadoc
**None.**

### Undocumented Public Methods (44)
All 22 getter/setter pairs (44 methods, lines 33-165). Representative: `getGroup_cd()`, `getArrUnitUtil()`, `gettTotal()`, `gettKeyPer()`, `gettHydrPer()`, etc.

### Accuracy of Existing Documentation
N/A -- no documentation exists.

### TODO / FIXME / HACK / XXX
None found.

---

## 14. CustomerDAO.java
**Path:** `dao/CustomerDAO.java`
**Lines:** 207

### Reading Evidence
Data-access class providing 5 public lookup methods, each executing a single-row SQL query and returning a `String` result (defaulting to `"All"` or `"unknown report"` when no match). Methods:
- `getCustomerName(String cust_cd)` -- queries `FMS_CUST_MST."USER_NAME"` by `USER_CD`.
- `getLocationName(String loc_cd)` -- queries `FMS_LOC_MST."NAME"` by `LOCATION_CD`.
- `getDepartmentName(String dept_cd)` -- queries `FMS_DEPT_MST."DEPT_NAME"` by `DEPT_CD`.
- `getModelName(String model_cd)` -- queries `FMS_VEHICLE_TYPE_MST."VEHICLE_TYPE"` by `VEHICLE_TYPE_CD`.
- `getFormName(String form_cd)` -- queries `RuntimeConf.form_table` `"FORM_NAME"` by `FORM_CD`.

All methods follow the same pattern: obtain a `Connection` from `DBUtil`, create a `Statement`, execute a query, read the first result, and close resources in `finally`. All use string concatenation for SQL (SQL injection risk). `getFormName` has a logic anomaly: the guard condition checks `formName` (the default value `"unknown report"`) instead of `form_cd`, meaning the `equalsIgnoreCase("")` and `equalsIgnoreCase("0")` checks against `formName` will never match -- the method always falls through to execute the query if `form_cd` is non-empty (line 177-179).

### Class-Level Javadoc
**None.**

### Method-Level Javadoc
**None.**

### Undocumented Public Methods (5)
| Method | Line |
|--------|------|
| `getCustomerName(String)` | 17 |
| `getLocationName(String)` | 55 |
| `getDepartmentName(String)` | 92 |
| `getModelName(String)` | 129 |
| `getFormName(String)` | 165 |

### Accuracy of Existing Documentation
N/A -- no documentation exists.

### TODO / FIXME / HACK / XXX
None found.

---

## 15. DriverAccessAbuseDAO.java
**Path:** `dao/DriverAccessAbuseDAO.java`
**Lines:** 65

### Reading Evidence
Data-access class for driver access-abuse reports. Contains 13 instance-level raw `ArrayList` fields (package-private), which appear to be unused within this class -- the actual data is routed through `Databean_report` and returned via a `DriverAccessAbuseBean`. Has a duplicate import of `java.util.ArrayList` (lines 7 and 10). Imports `java.sql.Connection`, `ResultSet`, `SQLException`, `Statement`, `Collections`, and `StringTokenizer` -- none of which are used within the class body. Only public method is `getAbuseBean(...)`.

The single method `getAbuseBean` takes 7 String parameters, constructs a `Databean_report`, sets its properties including opcode `"access_abuse"`, calls `dbreport.init()`, then copies results from `Databean_report` into a new `DriverAccessAbuseBean` and returns it. No direct SQL usage in this class -- all database interaction is delegated to `Databean_report.init()`.

### Class-Level Javadoc
**None.**

### Method-Level Javadoc
**None.**

### Undocumented Public Methods (1)
| Method | Line |
|--------|------|
| `getAbuseBean(String, String, String, String, String, String, String)` | 33 |

### Accuracy of Existing Documentation
N/A -- no documentation exists.

### TODO / FIXME / HACK / XXX
None found.

---

## Summary

### Documentation Coverage

| # | File | Class Javadoc | Methods Total | Methods Documented | % Documented |
|---|------|:---:|:---:|:---:|:---:|
| 1 | HireDehireReportBean.java | No | 16 | 0 | 0% |
| 2 | ImpactReportBean.java | No | 28 | 0 | 0% |
| 3 | KeyHourUtilBean.java | No | 46 | 0 | 0% |
| 4 | OperationalStatusReportItemResultBean.java | No | 16 | 0 | 0% |
| 5 | OperationalStatusReportResultBean.java | No | 2 | 0 | 0% |
| 6 | PreOpCheckFailReportBean.java | No | 24 | 0 | 0% |
| 7 | PreOpCheckReportBean.java | No | 24 | 0 | 0% |
| 8 | SeatHourUtilBean.java | No | 46 | 0 | 0% |
| 9 | ServMaintenanceReportBean.java | No | 36 | 0 | 0% |
| 10 | SuperMasterAuthReportBean.java | No | 2 | 0 | 0% |
| 11 | UnitUnlockReportBean.java | No | 20 | 0 | 0% |
| 12 | UtilWowReportBean.java | No | 14 | 0 | 0% |
| 13 | UtilisationReportBean.java | No | 44 | 0 | 0% |
| 14 | CustomerDAO.java | No | 5 | 0 | 0% |
| 15 | DriverAccessAbuseDAO.java | No | 1 | 0 | 0% |
| **Totals** | | **0 / 15** | **324** | **0** | **0%** |

### TODO / FIXME / HACK / XXX Markers
**None found** across all 15 files.

### Key Observations

1. **Zero documentation across all 15 files.** Not a single class-level Javadoc, method-level Javadoc, or inline explanatory comment exists in any of the audited files. This is the most significant finding of this pass.

2. **Bean classes are pure POJOs.** Files 1-13 are straightforward data-transfer objects containing only fields and their getter/setter pairs with no business logic. While method-level Javadoc on each accessor would be excessive, class-level Javadoc explaining the report each bean supports and the meaning of its abbreviated field names is critically missing.

3. **Duplicate/near-duplicate classes detected:**
   - `PreOpCheckReportBean` and `PreOpCheckFailReportBean` are structurally identical (same fields, same types, same method signatures).
   - `KeyHourUtilBean` and `SeatHourUtilBean` are structurally identical (same fields, same types, same method signatures).
   - Without documentation, the intended distinction between each pair is unclear.

4. **CustomerDAO.java** is the most logic-bearing file in scope with 5 public methods performing SQL queries. The complete absence of Javadoc on these methods is a higher-priority documentation gap since the methods have non-trivial parameters and database table dependencies that would benefit from being documented.

5. **DriverAccessAbuseDAO.java** declares 13 instance-level ArrayList fields and multiple unused imports. Without documentation, it is unclear whether the instance fields are legacy remnants or serve some undiscovered purpose.

6. **Cryptic field names throughout.** Abbreviated names like `po_dnm`, `vutil1`, `sm_ser_ed2`, `vunit_lotm`, `a_driv_cd` etc. are pervasive and without documentation their meaning can only be inferred from context or database column names.
