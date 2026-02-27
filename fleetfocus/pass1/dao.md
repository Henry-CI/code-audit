# DAO Security Audit Report
**Audit ID:** A05
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Date:** 2026-02-25
**Auditor:** A05 (automated pass)
**Scope:** All DAO and Repository Java files in the FleetFocus codebase

---

## Files Audited

| # | File Path | Class |
|---|-----------|-------|
| 1 | `WEB-INF/src/com/torrent/surat/fms6/dao/BatteryDAO.java` | `com.torrent.surat.fms6.dao.BatteryDAO` |
| 2 | `WEB-INF/src/com/torrent/surat/fms6/dao/DriverDAO.java` | `com.torrent.surat.fms6.dao.DriverDAO` |
| 3 | `WEB-INF/src/com/torrent/surat/fms6/dao/DriverImportDAO.java` | `com.torrent.surat.fms6.dao.DriverImportDAO` |
| 4 | `WEB-INF/src/com/torrent/surat/fms6/dao/ImpactDAO.java` | `com.torrent.surat.fms6.dao.ImpactDAO` |
| 5 | `WEB-INF/src/com/torrent/surat/fms6/dao/ImportDAO.java` | `com.torrent.surat.fms6.dao.ImportDAO` |
| 6 | `WEB-INF/src/com/torrent/surat/fms6/dao/LockOutDAO.java` | `com.torrent.surat.fms6.dao.LockOutDAO` |
| 7 | `WEB-INF/src/com/torrent/surat/fms6/dao/MessageDao.java` | `com.torrent.surat.fms6.dao.MessageDao` |
| 8 | `WEB-INF/src/com/torrent/surat/fms6/dao/PreCheckDAO.java` | `com.torrent.surat.fms6.dao.PreCheckDAO` |
| 9 | `WEB-INF/src/com/torrent/surat/fms6/dao/RegisterDAO.java` | `com.torrent.surat.fms6.dao.RegisterDAO` |
| 10 | `WEB-INF/src/com/torrent/surat/fms6/dao/UnitDAO.java` | `com.torrent.surat.fms6.dao.UnitDAO` |
| 11 | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/dao/CustomerDAO.java` | `com.torrent.surat.fms6.excel.reports.dao.CustomerDAO` |
| 12 | `WEB-INF/src/com/torrent/surat/fms6/excel/reports/dao/DriverAccessAbuseDAO.java` | `com.torrent.surat.fms6.excel.reports.dao.DriverAccessAbuseDAO` |
| 13 | `WEB-INF/src/com/torrent/surat/fms6/repository/FmsChklistLangSettingRepo.java` | `com.torrent.surat.fms6.repository.FmsChklistLangSettingRepo` |

---

## Summary of Findings

| ID | Severity | Category | File | Brief Description |
|----|----------|----------|------|-------------------|
| A05-1 | CRITICAL | SQL Injection | BatteryDAO.java | All 5 methods concatenate `from`/`to` date strings and `cust_cd`/`vcd` into SQL |
| A05-2 | CRITICAL | SQL Injection | DriverDAO.java | 7 methods concatenate `cust_cd`, `loc_cd`, `dept_cd`, `userId`, `usercd`, `vehtype` into SQL |
| A05-3 | CRITICAL | SQL Injection | DriverImportDAO.java | 10+ methods concatenate `fname`, `lname`, `licence`, `compId`, `id`, `url` into SQL |
| A05-4 | CRITICAL | SQL Injection | ImpactDAO.java | All methods concatenate `cust_cd`, `loc_cd`, `dept_cd`, `from`, `to` into SQL |
| A05-5 | CRITICAL | SQL Injection | ImportDAO.java | `saveQuestions`, `saveQuestionsTab`, `saveDriverInfo`, `removePreviousChecklist` concatenate bean fields into SQL |
| A05-6 | CRITICAL | SQL Injection | MessageDao.java | `init()` concatenates `fid` into SQL with no sanitization |
| A05-7 | CRITICAL | SQL Injection | PreCheckDAO.java | `getChecks`, `getCheckSummary` concatenate date strings and entity IDs into SQL |
| A05-8 | CRITICAL | SQL Injection | RegisterDAO.java | `checkDupComp` concatenates `cname` into SQL via ILIKE |
| A05-9 | CRITICAL | SQL Injection | UnitDAO.java | Multiple methods concatenate all filter parameters directly into SQL |
| A05-10 | CRITICAL | SQL Injection | CustomerDAO.java | 5 lookup methods concatenate ID parameters directly into SQL |
| A05-11 | CRITICAL | SQL Injection | FmsChklistLangSettingRepo.java | All 3 query methods concatenate parameters directly into SQL |
| A05-12 | HIGH | Multi-tenancy / Authorization | DriverImportDAO.java | `getDriverById(id)` fetches a driver record by ID with no customer filter |
| A05-13 | HIGH | Multi-tenancy / Authorization | DriverImportDAO.java | `getDriverName(id)`, `getDriverNameLinde(id)` look up any user by ID with no tenant check |
| A05-14 | HIGH | Multi-tenancy / Authorization | MessageDao.java | `init()` queries `mnt_msg` by `fid` with no customer/tenant scoping |
| A05-15 | HIGH | Multi-tenancy / Authorization | DriverDAO.java | `getDriverNameById(driver_id)` returns any user's name with no tenant check |
| A05-16 | MEDIUM | Credential Exposure | RegisterDAO.java | `checkAuthority()` embeds `RuntimeConf.username` and `RuntimeConf.password` in a SQL query string that is logged/printed on exception |
| A05-17 | MEDIUM | Resource Leak | DriverImportDAO.java | `saveLicenseExpiryBlackListInfo` — `stmt1`, inner `stmt`, `stmt2` and multiple `ResultSet` objects are not closed in a `finally` block; the `finally` block is entirely commented out |
| A05-18 | MEDIUM | Resource Leak | ImportDAO.java | `saveQuestions(QuestionBean)` — `ps` is declared but never used; opened `rs` handles are closed inline but not guarded against earlier-exit paths |
| A05-19 | LOW | Error Handling / Info Leakage | Multiple files | SQL query strings are printed to stdout/stderr on exception via `e.printStackTrace()` and `System.out.println("---> queryString = " + queryString)`, leaking full SQL to logs |

---

## Detailed Findings

---

### A05-1 — CRITICAL — SQL Injection — BatteryDAO.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/BatteryDAO.java`

**Affected methods (all use `Statement`, not `PreparedStatement`):**

| Method | Line(s) | Injected Parameters |
|--------|---------|---------------------|
| `getBatteryCharge` | 32–44 | `from`, `to` (date strings), `unitList` (from `getUnitLstByModel`) |
| `getBatteryChange` | 90–101 | `from`, `to`, `unitList` |
| `calculateBatteryChange` | 154–165 | `from`, `to`, `unitList` |
| `calculateBatteryCharge` | 269–279 | `from`, `to`, `unitList` |
| `getDuration` | 365 | `endtime`, `sttime` (both caller-supplied Strings) |
| `getDept_prefix` | 400 | `vcd` (vehicle code from the result of earlier queries, but itself unvalidated when passed from `calculateBatteryChange`) |

**Evidence — `getBatteryCharge` (lines 32–44):**
```java
String sql = "select d1.battery_id,to_char(d1.utc_time,'dd/mm/yyyy HH24:MI:SS')," +
             " ...
             " where d1.vehicle_cd in ("+unitList+") and d1.charge_id is not null "+
             " and d1.utc_time >= '"+from+"'::timestamp"+" and d1.utc_time<='"+to+"'::timestamp"+
             ...
rs=stmt.executeQuery(sql);
```

**Evidence — `getDuration` (line 365):**
```java
String sql = "select '"+endtime+"'::timestamp - '"+sttime+"'::timestamp";
```
`endtime` and `sttime` are themselves the results of database lookups but are passed as plain `String` parameters and concatenated without any escaping.

**Evidence — `getDept_prefix` (line 400):**
```java
String sql = "select \"DEPT_PREFIX\" from \"FMS_USR_VEHICLE_REL\" as r, \"FMS_DEPT_MST\" as d where r.\"DEPT_CD\" = d.\"DEPT_CD\" and \"VEHICLE_CD\" = " + vcd;
```
`vcd` is passed in as a `String` parameter with no validation.

**Recommendation:** Replace all `Statement` / string-concatenated SQL with `PreparedStatement` using `?` placeholders. Timestamp parameters should be bound as `java.sql.Timestamp`. The `unitList` IN-clause pattern (a comma-delimited string of IDs) should be replaced by use of a SQL `ARRAY` parameter or by validating each element is numeric before inclusion.

---

### A05-2 — CRITICAL — SQL Injection — DriverDAO.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/DriverDAO.java`

**Affected methods:**

| Method | Line(s) | Injected Parameters |
|--------|---------|---------------------|
| `getArrayDriver` | 35, 40, 45 | `cust_cd`, `loc_cd`, `dept_cd` |
| `checkExpiry` | 87, 95 | `cust_cd` |
| `sendIDDENY` | 159, 165, 178, 182, 190–191, 196, 208, 211, 218, 224 | `vehtype`, `usercd`, `vehicle_cd`, `unitGmtp`, `msg` |
| `getDriverlst` | 263, 268, 273 | `cust_cd`, `loc_cd`, `dept_cd` |
| `getArrayDriverImpact` | 313, 318, 323 | `cust_cd`, `loc_cd`, `dept_cd` |
| `getDriverImpactLst` | 367, 372, 377 | `cust_cd`, `loc_cd`, `dept_cd` |
| `checkValidLicence` | 420, 425, 428, 450, 459, 463, 470–471 | `userId`, `newRevewDate`, `unitId`, `driverId`, `driver_card`, `unitGmtp`, `msg` |
| `getDriverFulllst` | 503, 508, 513 | `cust_cd`, `loc_cd`, `dept_cd` |
| `getDriverNameById` | 550 | `driver_id` |

**Evidence — `sendIDDENY` (lines 157–159):**
```java
sql = "select v.\"VEHICLE_ID\", v.\"VEHICLE_CD\" from \"FMS_VEHICLE_MST\" as v, \"FMS_USR_VEHICLE_REL\" as vr,\"FMS_USER_DEPT_REL\" as ur " +
      " where ur.\"CUST_CD\" = vr.\"USER_CD\" and ur.\"LOC_CD\" = vr.\"LOC_CD\" and vr.\"VEHICLE_CD\" =  v.\"VEHICLE_CD\" " +
      " and v.\"VEHICLE_ID\" is not null and v.\"VEHICLE_TYPE_CD\" = "+ vehtype +" and ur.\"USER_CD\" = " + usercd;
```

**Evidence — `sendIDDENY` insert into outgoing (lines 177–179):**
```java
String msg = "IDDENY="+weigand;
sql="insert into \"outgoing\" (destination,message) values('"+unitGmtp+"','"+msg+"')";
stmt1.executeUpdate(sql);
```
`weigand` is a card ID read from the database (`CARD_ID` column), but it is never validated or sanitized before being embedded in a subsequent SQL INSERT. If a card ID contains a single-quote, SQL injection is achievable.

**Evidence — `checkValidLicence` (line 425):**
```java
sql = "select v.\"VEHICLE_CD\",\"VEHICLE_ID\", u.\"USER_CD\",u.\"CARD_ID\" from ... " +
      " and '"+newRevewDate+"'::timestamp >= current_date + '2 day'::interval ..."+
      " and u.\"USER_CD\" = " + userId;
```
`newRevewDate` is an externally supplied date string injected directly into SQL.

**Recommendation:** Use `PreparedStatement` throughout. `userId`, `vehtype`, `usercd`, `newRevewDate` must all be bound as typed parameters (`setInt`, `setString`, `setTimestamp`).

---

### A05-3 — CRITICAL — SQL Injection — DriverImportDAO.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/DriverImportDAO.java`

**Affected methods (all use `Statement` for the vulnerable queries):**

| Method | Line(s) | Injected Parameters |
|--------|---------|---------------------|
| `checkDriverByNm` | 29–31 | `fname`, `lname`, `compId`, `id` |
| `checkDriverByLic` | 83–84 | `licence`, `compId`, `id` |
| `getDriverByNm` | 136–138 | `fname`, `lname`, `compId` |
| `getDriverByFullNm` | 192–193 | `fname`, `compId` |
| `getAllDriver` | 248 | `compId` |
| `getAllDriverLinde(String)` | 306–307 | `compId` |
| `getAllDriverLinde(String, boolean)` | 355 | `compId` |
| `getDriverLicence` | 413–414 | `compId` |
| `getDriverById` | 472 | `id` |
| `delDriverById` | 984 | `id` |
| `getTotalDriverByID` | 1021 | `id` |
| `getDriverName` | 1069 | `id` |
| `getDriverNameLinde` | 1111 | `id` |
| `uploadLicence` | 1152 | `url`, `licenceid` |
| `uploadLicenceAU` | 1185 | `url`, `uid` |
| `saveLicenseExpiryBlackListInfo` (multiple) | 592, 607, 614, 632–634, 685–686, 738–744, 749–750, 770–773, 800, 804–810 | `bean.getLocCd()`, `bean.getDeptCd()`, `bean.getVehicleType()`, `bean.getDriverCd()`, `bean.getCustCd()`, `bean.getExpiryDate()`, `rs.getInt(1)` (used in DELETE) |

**Evidence — `checkDriverByNm` (lines 29–31):**
```java
String sql = "select id from driver where trim(both ' ' from first_name) ilike trim ( both ' ' from '"
        + fname + "')" + "  and trim(both ' ' from last_name) ilike trim ( both ' ' from '" + lname + "')"
        + "  and comp_id = " + compId;
```
`fname` and `lname` are free-text name fields — a value like `' OR '1'='1` would break out of the ILIKE expression.

**Evidence — `uploadLicence` (lines 1152–1153):**
```java
String queryString = "update driver_licence_expiry_mst set document_url='"+url+"' where id ="+licenceid;
stmt.executeUpdate(queryString);
```
`url` is a file path / URL string supplied externally and inserted directly.

**Evidence — `uploadLicenceAU` (lines 1185–1186):**
```java
String queryString = "update \"FMS_USR_MST\" set document_url='"+url+"' where \"USER_CD\" ="+uid;
stmt.executeUpdate(queryString);
```

**Evidence — `saveLicenseExpiryBlackListInfo` delete/insert (lines 738–749):**
```java
sql = "delete from \"fms_vehicle_access_mapper\" where \"user_cd\" = '"+bean.getDriverCd()+"'";
stmt1.executeUpdate(sql);
// ...
sql="insert into \"fms_vehicle_access_mapper\" (user_cd,sel_type,sel_val) values('"+bean.getDriverCd()+"','veh','"+rs.getString(1)+"')";
```

**Recommendation:** All read methods where only numeric IDs are expected should use `PreparedStatement` with `setInt`. Name-search methods that take free-text (fname, lname, licence) must use `PreparedStatement` with `setString`. URL fields must use `PreparedStatement`. The `saveLicenseExpiryBlackListInfo` method should be rewritten end-to-end with parameterised statements.

---

### A05-4 — CRITICAL — SQL Injection — ImpactDAO.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/ImpactDAO.java`

**Affected methods (all use `Statement`):**

| Method | Line(s) | Injected Parameters |
|--------|---------|---------------------|
| `getRedImpactCache` | 71 | `cust_cd`, `loc_cd`, `dept_cd`, `model_cd`, `year`, `n` |
| `getRedImpactCacheByDriver` | 148 | `cust_cd`, `loc_cd`, `dept_cd`, `model_cd`, `driver_cd`, `year`, `j` |
| `getRedImpact` | 203, 221–228 | `cust_cd`, `loc_cd`, `dept_cd`, `st` (date string), `unitlst` |
| `getRedImpactDriver` | 285–311 | `cust_cd`, `loc_cd`, `dept_cd`, `st`, `unitlst`, `driverlst` |
| `getImpacts(6-arg)` | 366–390 | `from`, `to`, `month`, `unitlst` |
| `getImpactsNationalRpt` | 449, 481–494 | `cust_cd`, `st_dt`, `end_dt`, `unitlst` |
| `getImpacts(2-arg)` | 633–645 | `unitlst` |
| `getImpactsByUnit(2-arg)` | 709–718 | `unitlst` |
| `getImpactsByDriver` | 847–975 | `unitlst`, `unitBean.getId()` (vehicle CD) |
| `getImpactsByUnit(6-arg)` | 1058 | `from`, `to` |

**Evidence — `getImpacts` (line 366):**
```java
extra = " and f.\"DATE_TIME\"  >= '"+from+"'::timestamp and f.\"DATE_TIME\" < '"+to+"'::timestamp + interval '1 day'";
```

**Evidence — `getImpactsByDriver` (line 879):**
```java
sql = "select \"USER_CD\",\"CONTACT_FIRST_NAME\"||' '||\"CONTACT_LAST_NAME\" as name, count(shock_id)"+
      " ...
      " where v.\"VEHICLE_CD\" = "+unitBean.getId()+
```
`unitBean.getId()` is a vehicle CD returned from a prior query, but it is a `String` that was stored in a bean and never validated to be numeric before being concatenated.

**Recommendation:** Use `PreparedStatement`. For the IN-clause `unitlst` pattern (comma-separated vehicle codes produced by `UnitDAO.getUnitLstByModel`), the entire calling chain must be fixed: `getUnitLstByModel` must return a validated numeric list and the consuming queries must use array-based IN or explicit numeric casting.

---

### A05-5 — CRITICAL — SQL Injection — ImportDAO.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/ImportDAO.java`

**Affected methods:**

| Method | Line(s) | Injected Parameters |
|--------|---------|---------------------|
| `saveQuestions(QuestionBean)` | 108, 124, 162–167 | `qbean.getVeh_typ_cd()`, `chk_cd`, `order`, `qbean.getQuestion()`, `qbean.getAns_type()`, `qbean.getExp_ans()`, `qbean.getUser_cd()`, `qbean.getLoc_cd()`, `qbean.getDept_cd()` |
| `saveQuestions(QuestionBean, List)` | 276, 292, 330–335 | same as above + `qbean.getQuestionSpa()`, `qbean.getQuestionTha()` |
| `getCurrentCheckCd` | 401–403 | `custCd`, `locCd`, `deptCd`, `vehTypeCd` |
| `getCurrentCheckCdTab` | 466–467, 478–481, 497–499 | `custCd`, `locCd`, `deptCd` |
| `removePreviousChecklist` | 563–569 | `chkCds` (built from caller-supplied list) |
| `saveQuestionsTab` | 677–700, 716, 847–852 | `qbean.getCustCd()`, `qbean.getLoc_cd()`, `qbean.getDept_cd()`, `qbean.getVeh_typ_cd()`, `qbean.getQuestion()`, `qbean.getAns_type()`, `qbean.getExp_ans()`, `qbean.getUser_cd()`, `loc_cd`, `dep_cd`, `mod_cd` |
| `saveDriverInfo` | 1001–1004, 1015–1019, 1043, 1055, 1097–1104, 1121–1127 | `driverBean.getCustCd()`, `driverBean.getSite()`, `driverBean.getDepartment()`, `user_nm`, `driverBean.getFirst_name()`, `driverBean.getLast_name()`, `loc_cd`, `dep_cd` |
| `saveDriverInfoAU` | 1473–1476, 1492–1496, 1525, 1542, 1589–1595, 1644–1650 | same as `saveDriverInfo` |

**Evidence — `saveQuestions` (lines 162–167):**
```java
queryString = "Insert into \"FMS_OPCHK_QUEST_MST\" "
        + " (\"CHK_CD\",\"VEH_TYP_CD\",\"ORDER_NO\",\"QUESTION\","
        + "\"ANS_TYP\",\"EXP_ANS\",\"CRITICAL_ANS\""
        + ",\"USER_CD\",\"LOC_CD\",\"DEPT_CD\",\"EXCLUDE_RANDOM\") "
        + "values ('"+chk_cd+"','"+qbean.getVeh_typ_cd()+"','"+order+"','"+qbean.getQuestion()+"','"+qbean.getAns_type()+"',"
        + "'"+qbean.getExp_ans()+"','"+critical_ans+"','"+qbean.getUser_cd()+"','"+qbean.getLoc_cd()+"','"+qbean.getDept_cd()+"','" + qbean.isExcludeRandom() +"')";
stmt.executeUpdate(queryString);
```
`qbean.getQuestion()` is a free-text question field — it is inserted via string concatenation. A payload of `'); DROP TABLE "FMS_OPCHK_QUEST_MST"; --` would execute as SQL.

**Evidence — `removePreviousChecklist` (lines 563–569):**
```java
for (String chkCd : chkList) {
    chkCds += ","+chkCd;
}
queryString = "DELETE FROM \"FMS_OPCHK_QUEST_MST\" where \"CHK_CD\" in ("+ chkCds +"); ";
stmt.executeUpdate(queryString);
```
`chkList` is supplied by the caller and elements are concatenated without any numeric validation.

**Recommendation:** The `saveQuestions` INSERT must use `PreparedStatement` with individual `setString` / `setInt` bindings for each column. The `removePreviousChecklist` method must validate that each element in `chkCds` is numeric before constructing the IN clause.

---

### A05-6 — CRITICAL — SQL Injection — MessageDao.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/MessageDao.java`

**Affected methods:**

| Method | Line(s) | Injected Parameters |
|--------|---------|---------------------|
| `init()` | 62–63 | `fid` |

**Evidence (lines 60–63):**
```java
if( opCode.equalsIgnoreCase("get_msg")){
    stmt = conn.createStatement();
    queryString = "select * from mnt_msg where \"FORM_CD\"="+fid;
    rset = stmt.executeQuery(queryString);
```
`fid` is set via the public setter `setFid(String fid)` and then concatenated directly into SQL. Any caller that supplies `fid` from an HTTP request parameter can inject arbitrary SQL.

**Additional concern:** The query uses `SELECT *`, returning all columns of `mnt_msg`, which may include sensitive fields.

**Recommendation:** Replace `Statement` with `PreparedStatement`. Bind `fid` via `setString` or `setInt`. Remove the `SELECT *` and name the specific columns required.

---

### A05-7 — CRITICAL — SQL Injection — PreCheckDAO.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/PreCheckDAO.java`

**Affected methods:**

| Method | Line(s) | Injected Parameters |
|--------|---------|---------------------|
| `getChecks(7-arg)` | 45–46, 50–51, 81 | `from`, `to`, `month`, `unitlst`, `arrId.get(i)` (checklist result IDs) |
| `getCheckSummary` | 197–202, 216, 234, 241 | `from`, `to`, `month`, `entityBean.getId()` (vehicle CD) |
| `getChecksByDriver` | 286–293 | `unitLst` |

**Evidence — `getChecks` (lines 45–46):**
```java
extra = " and starttimestamp  >= '"+from+"'::timestamp and starttimestamp < '"+to+"'::timestamp + interval '1 day'";
```

**Evidence — `getChecks` loop (line 81):**
```java
sql = "select count(id) from op_chk_checklistanswer where checklist_result_id = '" + arrId.get(i) + "' and answer <> expectedanswer";
```
`arrId` is built from results of the previous query, so the IDs are DB-sourced. However, if the `id` column contains non-integer values (e.g., due to an earlier injection), this becomes a second-order injection vector.

**Evidence — `getCheckSummary` (line 216):**
```java
sql = "select to_char(avg(finishtimestamp - starttimestamp),'HH24:MI:SS')  from op_chk_checklistresult " +
      " where driver_id != '0' and driver_cd != '2' and driver_cd is not null  " +
      " and finishtimestamp is not null and vehicle_cd = " +entityBean.getId()+
```

**Recommendation:** Use `PreparedStatement` for all queries. Validate that `from`/`to` conform to expected date formats before use. Ensure `entityBean.getId()` is parsed as an integer before inclusion.

---

### A05-8 — CRITICAL — SQL Injection — RegisterDAO.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/RegisterDAO.java`

**Affected methods:**

| Method | Line(s) | Injected Parameters |
|--------|---------|---------------------|
| `checkDupComp` | 474 | `cname` |
| `register` | 284, 294, 373, 383 | `user_nm` (derived from `dfname[i]`, `dlname[i]`, `fname`, `lname`) |

**Evidence — `checkDupComp` (line 474):**
```java
String sql = "select count(*) from  \"FMS_CUST_MST\" where trim(both ' ' from \"USER_NAME\") ilike '"+cname.trim()+"'";
```
`cname` is the company name submitted during self-registration. It is used in an ILIKE expression without escaping.

**Evidence — `register` (lines 284, 294):**
```java
sql = "select count(*) from \"FMS_USR_MST\" where \"USER_NAME\" = '"+user_nm+"'";
// ...
sql = "select count(*) from \"FMS_USR_MST\" where \"USER_NAME\" = '"+user_nm+j+"'";
```
`user_nm` is derived from name parameters passed by the caller. If a registrant supplies a name like `' OR '1'='1`, these existence-check queries are injectable.

**Note:** The `register` method itself uses `PreparedStatement` for the main INSERTs, which is correct. Only the duplicate-check `SELECT` queries above use unsafe `Statement` concatenation.

**Recommendation:** Use `PreparedStatement` for all `SELECT` queries in both methods. The ILIKE duplicate check should also use a `PreparedStatement` with a `?` placeholder.

---

### A05-9 — CRITICAL — SQL Injection — UnitDAO.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/UnitDAO.java`

**Affected methods (all methods reviewed use `Statement` with concatenation):**

| Method | Line(s) | Injected Parameters |
|--------|---------|---------------------|
| `getDepartmentLst` | 68, 73 | `cust_cd`, `loc_cd` |
| `getArrayDepartment(2-arg)` | 117, 122 | `cust_cd`, `loc_cd` |
| `getUnitLstByModel` | 172, 176, 181, 186 | `cust_cd`, `loc_cd`, `dept_cd`, `model_cd` |
| `getArrayUnitByModel` | 224, 228, 233, 238 | `cust_cd`, `loc_cd`, `dept_cd`, `model_cd` |
| `getArryModel` | 282, 287, 292 | `cust_cd`, `loc_cd`, `dept_cd` |
| `getArryModelImpact` | 336, 341, 346 | `cust_cd`, `loc_cd`, `dept_cd` |
| `getArryModelImpactByDriver` | 391–406 | `cust_cd`, `loc_cd`, `dept_cd`, `driver_cd` |
| `getLocById` | 450 | `loc_cd` |
| `getCustName` | 485 | `cust_cd` |
| `getLocName` | 521 | `loc_cd` |
| `getDeptName` | 558 | `dept_cd` |

**Evidence — `getUnitLstByModel` (lines 172–191):**
```java
filters = " r.\"USER_CD\" = " + cust_cd;
if(!loc_cd.equalsIgnoreCase("")&&!loc_cd.equalsIgnoreCase("all")) {
    filters += "  and r.\"LOC_CD\" in (" + loc_cd +")";
}
if(!dept_cd.equalsIgnoreCase("")&&!dept_cd.equalsIgnoreCase("all")) {
    filters += " and r.\"DEPT_CD\" in (" + dept_cd + ")";
}
if(!model_cd.equalsIgnoreCase("")&&!model_cd.equalsIgnoreCase("all")) {
    filters += " AND t.\"REPORT_DESCRIPTION_CD\" = " + model_cd;
}
sql = "select distinct(v.\"VEHICLE_CD\") from ... where "+ filters;
rs=stmt.executeQuery(sql);
```
`getUnitLstByModel` is called by nearly every other DAO class as a building block for the `unitlst` IN-clause. Its output (a comma-delimited String of vehicle codes) is then embedded in further queries. Injecting `cust_cd` here gives an attacker access to cross-customer vehicle data in all downstream reports.

**Recommendation:** All filter parameters should be validated as numeric integers before concatenation. Ideally, rewrite using `PreparedStatement` with array-type parameters for the IN clauses (`loc_cd`, `dept_cd`). Since this method is used across many DAOs, fixing it is high-leverage.

---

### A05-10 — CRITICAL — SQL Injection — CustomerDAO.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/dao/CustomerDAO.java`

**Affected methods:**

| Method | Line(s) | Injected Parameters |
|--------|---------|---------------------|
| `getCustomerName` | 32 | `cust_cd` |
| `getLocationName` | 70 | `loc_cd` |
| `getDepartmentName` | 107 | `dept_cd` |
| `getModelName` | 144 | `model_cd` |
| `getFormName` | 180–181 | `form_cd` |

**Evidence — `getCustomerName` (line 32):**
```java
String sql = "select \"USER_NAME\" from \"FMS_CUST_MST\" where \"USER_CD\" = " + cust_cd;
```

**Evidence — `getFormName` (lines 180–181):**
```java
String query = "select \"FORM_NAME\"  from "+RuntimeConf.form_table+" where \"FORM_CD\"='"
        + form_cd + "' ";
```
`form_cd` is quoted with single quotes, making it injectable via a `'` character. `RuntimeConf.form_table` is also dynamically embedded — if this configuration value is ever attacker-influenced, it would allow table-name injection.

**Recommendation:** Use `PreparedStatement` for all five methods. The `form_table` table-name substitution cannot use a `?` placeholder; validate it against a known-good allowlist of table names.

---

### A05-11 — CRITICAL — SQL Injection — FmsChklistLangSettingRepo.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/repository/FmsChklistLangSettingRepo.java`

**Affected methods:**

| Method | Line(s) | Injected Parameters |
|--------|---------|---------------------|
| `queryLangConfigBy` | 31 | `custCd`, `locCd`, `deptCd`, `vehTypeCd` |
| `updateLanguageBy` | 54–55 | `langChoiceAsList` (toString), `custCd`, `locCd`, `deptCd`, `vehTypeCd` |
| `insertBy` | 62 | `custCd`, `locCd`, `deptCd`, `vehTypeCd`, `langChoice` |

**Evidence — `queryLangConfigBy` (line 31):**
```java
String query = "select \"lang_config\" from \"FMS_CHCKLIST_LANG_SETTING\" "
            + " where \"cust_cd\" = '" + custCd + "' and \"loc_cd\" = '" + locCd + "' and \"dept_cd\" = '" + deptCd + "' and \"veh_type_cd\" = '" + vehTypeCd + "'";
```

**Evidence — `updateLanguageBy` (lines 54–55):**
```java
String query = "Update\"FMS_CHCKLIST_LANG_SETTING\" set \"lang_config\" = '" + langChoiceAsList.toString().replace("[", "").replace("]", "").replace(" ", "") + "' "
            + " where \"cust_cd\" = '" + custCd + "' and ...";
```
The `langChoiceAsList` content (language codes derived from user input via CSV import) is sanitised only by stripping `[`, `]`, and space characters — a single-quote character in a language code value would still break out of the string literal.

**Evidence — `insertBy` (line 62):**
```java
String query = "Insert into \"FMS_CHCKLIST_LANG_SETTING\" (\"cust_cd\", \"loc_cd\", \"dept_cd\", \"veh_type_cd\", \"lang_config\") "
    + "values ('" + custCd + "', '" + locCd + "', '" + deptCd + "', '" + vehTypeCd + "', '" + langChoice + "')";
```

**Note:** This repository receives its `Statement` from the caller (`ImportDAO`), which itself does not use `PreparedStatement` for these operations.

**Recommendation:** Replace all string-concatenated queries with parameterised statements. The repository should accept a `Connection` rather than a `Statement` so it can create its own `PreparedStatement` objects.

---

### A05-12 — HIGH — Multi-tenancy / Authorization — DriverImportDAO.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/DriverImportDAO.java`

**Method:** `getDriverById(String id)` — line 472

**Evidence:**
```java
String sql = "select id,first_name,last_name as name,active,licno,to_char(expirydt,'dd/mm/yyyy'),phone,location,department from driver where id=" + id;
```

`getDriverById` takes a plain numeric ID and returns full driver details including name, licence number, phone, location, and department. There is **no customer (`comp_id`) filter**. An authenticated user of Customer A who knows (or guesses) driver IDs belonging to Customer B can retrieve Customer B's driver records by calling this method with those IDs.

**Recommendation:** Add `AND comp_id = ?` to the query and pass the session's customer ID as the second bound parameter.

---

### A05-13 — HIGH — Multi-tenancy / Authorization — DriverImportDAO.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/DriverImportDAO.java`

**Methods:** `getDriverName(String id)` (line 1069), `getDriverNameLinde(String id)` (line 1111)

**Evidence — `getDriverName` (line 1069):**
```java
String sql = "select first_name||' '||last_name as name from driver where id=" + id;
```

**Evidence — `getDriverNameLinde` (line 1111):**
```java
String sql = "select \"CONTACT_FIRST_NAME\"||' '||\"CONTACT_LAST_NAME\" as name from \"FMS_USR_MST\" where \"USER_CD\"=" + id;
```

Both methods look up a user or driver name by a bare integer ID without any customer/tenant scoping. While name-only disclosure may appear low-risk, it confirms existence of records across all customers, enables enumeration attacks, and violates data isolation.

**Recommendation:** Add a `comp_id` / `cust_cd` parameter and filter by it. The `getDriverNameLinde` variant should join through `FMS_USER_DEPT_REL` to filter by `CUST_CD`.

---

### A05-14 — HIGH — Multi-tenancy / Authorization — MessageDao.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/MessageDao.java`

**Method:** `init()` — line 62

**Evidence:**
```java
queryString = "select * from mnt_msg where \"FORM_CD\"="+fid;
rset = stmt.executeQuery(queryString);
if (rset.next()) {
    msg = rset.getString(7);
    status = rset.getBoolean(8);
}
```

The `mnt_msg` table is queried by `FORM_CD` alone with no customer or tenant filter. If this table contains messages for multiple customers, any customer can retrieve another customer's message by supplying the correct form code. The `SELECT *` also returns all columns, potentially exposing fields not intended for the caller.

**Recommendation:** Determine whether `mnt_msg` is per-customer. If so, add a customer filter. Replace `SELECT *` with explicit column names. Use `PreparedStatement`.

---

### A05-15 — HIGH — Multi-tenancy / Authorization — DriverDAO.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/DriverDAO.java`

**Method:** `getDriverNameById(String driver_id)` — line 550

**Evidence:**
```java
String sql = "select \"CONTACT_FIRST_NAME\"||' '||\"CONTACT_LAST_NAME\" "+
             "  from \"FMS_USR_MST\""+
             "  where \"USER_CD\" = "+driver_id;
```

`FMS_USR_MST` contains users from all customers. This method returns the full name of any user in the system without verifying that the `driver_id` belongs to the requesting customer's tenant scope.

**Recommendation:** Pass and filter by the requesting customer's `cust_cd` via a join to `FMS_USER_DEPT_REL`.

---

### A05-16 — MEDIUM — Credential Exposure — RegisterDAO.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/RegisterDAO.java`

**Method:** `checkAuthority(String username, String password)` — lines 511–518

**Evidence:**
```java
String sql = "select md5('"+RuntimeConf.username+"'),md5('"+RuntimeConf.password+"')";
rs=stmt.executeQuery(sql);
if(rs.next())
{
    if(rs.getString(1).equalsIgnoreCase(username) && rs.getString(2).equalsIgnoreCase(password))
    {
        result = true;
    }
}
```

`RuntimeConf.username` and `RuntimeConf.password` are plaintext credentials stored in the application configuration. They are embedded into a SQL query string, meaning:

1. The full SQL string (including the credentials in plaintext) will appear in any query log, slow-query log, or audit log on the database server.
2. The SQL string is also passed to `e.getMessage()` and `e.printStackTrace()` if an exception occurs, and the surrounding catch block does not suppress it — so the credentials will also appear in application server logs.
3. MD5 is cryptographically broken and should not be used for password comparison.

**Recommendation:** Do not transmit credentials via SQL query text. Compare credentials in application code using a constant-time comparison function after hashing with a modern algorithm (bcrypt, Argon2). Remove the SQL-based MD5 pattern entirely.

---

### A05-17 — MEDIUM — Resource Leak — DriverImportDAO.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/DriverImportDAO.java`

**Method:** `saveLicenseExpiryBlackListInfo(LicenseBlackListBean bean)` — lines 885–918

**Evidence (lines 892–918, the `finally` block):**
```java
finally
{
    /*if (null != rs) { rs.close(); }
    if (null != rs2) { rs2.close(); }
    if (null != ps)  { ps.close(); }
    if (null != stmt1) { stmt1.close(); }
    if (null != stmt2) { stmt2.close(); }
    */
    DBUtil.closeConnection(conn);
}
```

The entire resource-cleanup body has been **commented out**. Only the `Connection` is closed. The following resources created inside the method are never closed:

- `stmt1` (line 576) — a `Statement`
- Multiple inner `stmt` (line 688) and `stmt2` (line 751) `Statement` objects created inside loops
- Multiple `ResultSet` objects (`rs` at lines 617, 636, 656, 678, 690, 745, 775, 797, 835)
- `ps` (PreparedStatement, multiple instances)

Under sustained load (e.g., bulk imports), this will exhaust the database connection pool's available cursors and statements, causing database errors for all users.

**Recommendation:** Restore and complete the `finally` block. Use try-with-resources (`try (Statement stmt1 = ...; PreparedStatement ps = ...)`) to guarantee closure even on early returns.

---

### A05-18 — MEDIUM — Resource Leak — ImportDAO.java

**File:** `WEB-INF/src/com/torrent/surat/fms6/dao/ImportDAO.java`

**Method:** `saveQuestions(QuestionBean qbean)` — lines 162–196

**Evidence:**
```java
// ps is declared at the top of the method but never assigned or used.
PreparedStatement ps = null;
// ...
// In the finally block:
if (null != ps) { ps.close(); } // ps is always null — this is dead code
```

A `PreparedStatement ps` field is declared but never assigned. Its close call in `finally` is dead code. While this does not itself cause a leak in the current code, it indicates copy-paste maintenance issues in the class. The real concern is that `rs` is closed inline at multiple points (e.g., lines 59–62, 101–104) rather than in the `finally` block, which means an unexpected exception between inline `rs.close()` calls could leave ResultSets open.

Additionally, `saveQuestionsTab` creates inner `Statement` objects (e.g., at line 576 `stmt1`) that are only closed inline and not guaranteed to close if exceptions propagate.

**Recommendation:** Consolidate all resource cleanup into `finally` blocks or use try-with-resources. Remove the unused `ps` declaration.

---

### A05-19 — LOW — Information Leakage via Error Handling — Multiple Files

**Files:** BatteryDAO.java, DriverDAO.java, DriverImportDAO.java, ImpactDAO.java, ImportDAO.java, PreCheckDAO.java, RegisterDAO.java, UnitDAO.java, CustomerDAO.java

**Pattern (representative example from ImportDAO.java, line 874):**
```java
catch (Exception e)
{
    System.out.println("---> queryString = " + queryString);
    e.printStackTrace();
    throw new SQLException(e.getMessage());
}
```

And (representative example from RegisterDAO.java, line 487):
```java
catch(Exception e)
{
    e.printStackTrace();
    e.getMessage();
}
```

Across the codebase, full SQL query strings (which in many cases include user-supplied data and schema structure) are printed to `stdout`/`stderr` on exceptions. In a production environment, these streams typically feed into application server logs that may be accessible to operations staff or may be inadvertently exposed. The `e.getMessage()` call with no assignment is also a no-op — the exception message is silently discarded rather than being returned or logged properly.

**Recommendation:**

1. Replace `System.out.println` / `e.printStackTrace()` with structured logging (e.g., `log.error("DAO query failed", e)`).
2. Do not log the SQL string itself in production; log only a method/operation identifier and the exception type.
3. Fix the `e.getMessage()` no-op calls — either assign the result, log it, or remove the call.

---

## Appendix: Methods Using PreparedStatement Correctly

The following methods were reviewed and found to use `PreparedStatement` with bound parameters appropriately. They are noted here as a positive baseline:

| File | Method | Notes |
|------|--------|-------|
| `DriverImportDAO.java` | `saveDriverInfo(DriverImportBean)` | Full INSERT via `PreparedStatement` with `setString`, `setDate`, `setInt` |
| `DriverImportDAO.java` | `updateDriverInfo(DriverImportBean)` | UPDATE via `PreparedStatement` |
| `ImportDAO.java` | `saveDriverInfo(DriverImportBean)` (the section from line 1150) | UPDATE and INSERT use `PreparedStatement` |
| `ImportDAO.java` | `saveDriverInfoAU` (insert section) | INSERT via `PreparedStatement` |
| `RegisterDAO.java` | `register(...)` | All INSERT/UPDATE operations use `PreparedStatement` |

---

## Risk Summary

The overarching finding is that the DAO layer follows no consistent policy of using `PreparedStatement`. The majority of data retrieval and manipulation methods across all 13 files use `Statement` with direct string concatenation of externally-supplied parameters. Since these parameters flow from HTTP request parameters through service/action classes into these DAOs, the attack surface for SQL injection is extremely broad. An authenticated user could — at minimum — extract data from any customer's account and — in the worst case — execute arbitrary SQL against the database (including INSERT, UPDATE, DELETE, and DDL operations depending on the database user's privileges).

The multi-tenancy issues (A05-12 through A05-15) are compounded by the SQL injection issues: even if tenant scoping were applied correctly, it would be bypassable through injection.

---

*End of report. Total findings: 19. Critical: 11, High: 4, Medium: 3, Low: 1.*
