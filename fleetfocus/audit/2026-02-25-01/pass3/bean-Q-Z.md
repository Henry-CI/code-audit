# Pass 3 -- Documentation Audit: bean package (Q-Z)

**Audit ID:** 2026-02-25-01
**Agent:** A03
**Pass:** 3 (Documentation)
**Date:** 2026-02-25
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Base Path:** `WEB-INF/src/com/torrent/surat/fms6/bean/`

---

## Summary

| Metric | Count |
|---|---|
| Files audited | 20 |
| Total public methods catalogued | 330 |
| Missing class-level Javadoc | 20 |
| Missing method-level Javadoc (all) | 330 |
| TODO / FIXME / HACK / XXX markers | 2 |
| Misleading / inaccurate comments | 1 |
| Findings (HIGH) | 1 |
| Findings (MEDIUM) | 6 |
| Findings (LOW) | 20 |
| Findings (INFO) | 3 |

---

## File-by-File Analysis

---

### 1. QuestionBean.java (126 lines)

**Class:** `QuestionBean` (line 3)
**Class-level Javadoc:** NONE
**Implements/Extends:** (none)

**Public Methods:**

| # | Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `String getUser_cd()` | 22 | NONE |
| 2 | `void setUser_cd(String)` | 25 | NONE |
| 3 | `String getLoc_cd()` | 28 | NONE |
| 4 | `void setLoc_cd(String)` | 31 | NONE |
| 5 | `String getDept_cd()` | 34 | NONE |
| 6 | `void setDept_cd(String)` | 37 | NONE |
| 7 | `String getVeh_typ_cd()` | 40 | NONE |
| 8 | `void setVeh_typ_cd(String)` | 43 | NONE |
| 9 | `String getQuestion()` | 46 | NONE |
| 10 | `void setQuestion(String)` | 49 | NONE |
| 11 | `String getAns_type()` | 52 | NONE |
| 12 | `void setAns_type(String)` | 55 | NONE |
| 13 | `String getExp_ans()` | 58 | NONE |
| 14 | `void setExp_ans(String)` | 61 | NONE |
| 15 | `String getCrit_ans()` | 64 | NONE |
| 16 | `void setCrit_ans(String)` | 67 | NONE |
| 17 | `String getCustCd()` | 70 | NONE |
| 18 | `void setCustCd(String)` | 73 | NONE |
| 19 | `String getAccess_level()` | 76 | NONE |
| 20 | `void setAccess_level(String)` | 79 | NONE |
| 21 | `String getAccess_cust()` | 82 | NONE |
| 22 | `void setAccess_cust(String)` | 85 | NONE |
| 23 | `String getAccess_site()` | 88 | NONE |
| 24 | `void setAccess_site(String)` | 91 | NONE |
| 25 | `String getAccess_dept()` | 94 | NONE |
| 26 | `void setAccess_dept(String)` | 97 | NONE |
| 27 | `String getQuestion_id()` | 100 | NONE |
| 28 | `void setQuestion_id(String)` | 103 | NONE |
| 29 | `String getQuestionSpa()` | 107 | NONE |
| 30 | `void setQuestionSpa(String)` | 110 | NONE |
| 31 | `String getQuestionTha()` | 113 | NONE |
| 32 | `void setQuestionTha(String)` | 116 | NONE |
| 33 | `boolean isExcludeRandom()` | 120 | NONE |
| 34 | `void setExcludeRandom(boolean)` | 123 | NONE |

**TODO/FIXME/HACK/XXX:** None
**Misleading Comments:** None

**Findings:**

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| QB-01 | LOW | 3 | No class-level Javadoc. Purpose of bean (pre-op question configuration?) is unclear from class name alone. |
| QB-02 | LOW | 22-125 | All 34 getter/setter methods lack Javadoc. Abbreviated field names (exp_ans, crit_ans, questionSpa, questionTha) have no documentation explaining their meaning. |

---

### 2. RestrictedAccessUsageBean.java (101 lines)

**Class:** `RestrictedAccessUsageBean` (line 3)
**Class-level Javadoc:** NONE
**Implements/Extends:** (none)

**Public Methods:**

| # | Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `RestrictedAccessUsageBean()` | 7 | NONE |
| 2 | `String getFleetNo()` | 11 | NONE |
| 3 | `String getSerialNo()` | 15 | NONE |
| 4 | `String getHourStart()` | 19 | NONE |
| 5 | `String getHourFinish()` | 23 | NONE |
| 6 | `String getServHoursFrom()` | 27 | NONE |
| 7 | `String getTotalUsage()` | 31 | NONE |
| 8 | `void setFleetNo(String)` | 35 | NONE |
| 9 | `void setSerialNo(String)` | 39 | NONE |
| 10 | `void setHourStart(String)` | 43 | NONE |
| 11 | `void setHourFinish(String)` | 47 | NONE |
| 12 | `void setServHoursFrom(String)` | 51 | NONE |
| 13 | `void setTotalUsage(String)` | 55 | NONE |
| 14 | `String getDriverList()` | 59 | NONE |
| 15 | `void setDriverList(String)` | 63 | NONE |
| 16 | `String getTotalAccHours()` | 67 | NONE |
| 17 | `void setTotalAccHours(String)` | 71 | NONE |
| 18 | `String getHourlyRate()` | 75 | NONE |
| 19 | `void setHourlyRate(String)` | 79 | NONE |
| 20 | `String getMaxMonthlyRate()` | 83 | NONE |
| 21 | `void setMaxMonthlyRate(String)` | 87 | NONE |
| 22 | `String getTotalCharge()` | 91 | NONE |
| 23 | `void setTotalCharge(String)` | 95 | NONE |

**TODO/FIXME/HACK/XXX:**
- Line 8: `// TODO Auto-generated constructor stub` -- IDE-generated placeholder left in place.

**Misleading Comments:** None

**Findings:**

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| RAUB-01 | LOW | 3 | No class-level Javadoc. Bean purpose (restricted-access usage tracking/billing) not documented. |
| RAUB-02 | LOW | 7-97 | All 23 public methods lack Javadoc. |
| RAUB-03 | INFO | 8 | Stale `TODO Auto-generated constructor stub` left from IDE scaffolding. Constructor body is empty. |

---

### 3. SFTPSettings.java (61 lines)

**Class:** `SFTPSettings` (line 3)
**Class-level Javadoc:** NONE
**Implements/Extends:** (none)

**Public Methods:**

| # | Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `int getCustomerCd()` | 16 | NONE |
| 2 | `String getSftpAddress()` | 19 | NONE |
| 3 | `String getSftpUser()` | 22 | NONE |
| 4 | `String getSftpPass()` | 25 | NONE |
| 5 | `String getSftpDir()` | 28 | NONE |
| 6 | `String getLastUpdateBy()` | 31 | NONE |
| 7 | `String getLastUpdate()` | 34 | NONE |
| 8 | `void setCustomerCd(int)` | 37 | NONE |
| 9 | `void setSftpAddress(String)` | 40 | NONE |
| 10 | `void setSftpUser(String)` | 43 | NONE |
| 11 | `void setSftpPass(String)` | 46 | NONE |
| 12 | `void setSftpDir(String)` | 49 | NONE |
| 13 | `void setLastUpdateBy(String)` | 52 | NONE |
| 14 | `void setLastUpdate(String)` | 55 | NONE |

**TODO/FIXME/HACK/XXX:** None
**Misleading Comments:** None

**Findings:**

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| SFTP-01 | LOW | 3 | No class-level Javadoc. Bean holds SFTP connection credentials; purpose/usage context not documented. |
| SFTP-02 | LOW | 16-57 | All 14 getter/setter methods lack Javadoc. |

---

### 4. ServiceDueFlagBean.java (1003 lines)

**Class:** `ServiceDueFlagBean` (line 29)
**Class-level Javadoc:** NONE
**Implements/Extends:** (none)

**Public Methods:**

| # | Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `void setCount(int)` | 90 | NONE |
| 2 | `void setHex(String)` | 94 | NONE |
| 3 | `void setDateS(String)` | 98 | NONE |
| 4 | `void init()` | 104 | NONE |
| 5 | `void clearVariables()` | 168 | NONE |
| 6 | `String getLastServDateEx()` | 194 | NONE |
| 7 | `void setLastServDateEx(String)` | 198 | NONE |
| 8 | `String getCurrHourMeter()` | 202 | NONE |
| 9 | `void setCurrHourMeter(String)` | 206 | NONE |
| 10 | `String getHrAtLastServ()` | 210 | NONE |
| 11 | `void setHrAtLastServ(String)` | 214 | NONE |
| 12 | `void setOpCode(String)` | 218 | NONE |
| 13 | `String getForm_cd()` | 222 | NONE |
| 14 | `void setForm_cd(String)` | 226 | NONE |
| 15 | `String getSet_ucd()` | 230 | NONE |
| 16 | `void setSet_ucd(String)` | 234 | NONE |
| 17 | `String getReportName()` | 238 | NONE |
| 18 | `void setReportName(String)` | 242 | NONE |
| 19 | `String getGet_fmod()` | 246 | NONE |
| 20 | `void setGet_fmod(String)` | 250 | NONE |
| 21 | `String getGet_fexp()` | 254 | NONE |
| 22 | `void setGet_fexp(String)` | 258 | NONE |
| 23 | `String getGet_fdel()` | 262 | NONE |
| 24 | `void setGet_fdel(String)` | 266 | NONE |
| 25 | `String getVeh_cd()` | 270 | NONE |
| 26 | `void setVeh_cd(String)` | 274 | NONE |
| 27 | `ArrayList getNextServDate()` | 278 | NONE |
| 28 | `void setNextServDate(ArrayList)` | 282 | NONE |
| 29 | `ArrayList getLastSTCO()` | 286 | NONE |
| 30 | `void setLastSTCO(ArrayList)` | 290 | NONE |
| 31 | `ArrayList getHoursAtLastServ()` | 294 | NONE |
| 32 | `void setHoursAtLastServ(ArrayList)` | 298 | NONE |
| 33 | `ArrayList getNextServiceDue()` | 302 | NONE |
| 34 | `void setNextServiceDue(ArrayList)` | 306 | NONE |
| 35 | `ArrayList getHoursToNextServ()` | 310 | NONE |
| 36 | `void setHoursToNextServ(ArrayList)` | 314 | NONE |
| 37 | `ArrayList getCurrentMeterReading()` | 318 | NONE |
| 38 | `void setCurrentMeterReading(ArrayList)` | 322 | NONE |
| 39 | `ArrayList getMachineName()` | 326 | NONE |
| 40 | `void setMachineName(ArrayList)` | 330 | NONE |
| 41 | `ArrayList getCustomerName()` | 334 | NONE |
| 42 | `void setCustomerName(ArrayList)` | 337 | NONE |
| 43 | `String getSet_cust_cd()` | 341 | NONE |
| 44 | `void setSet_cust_cd(String)` | 345 | NONE |
| 45 | `String getSet_loc_cd()` | 349 | NONE |
| 46 | `void setSet_loc_cd(String)` | 353 | NONE |
| 47 | `String getSet_dep_cd()` | 357 | NONE |
| 48 | `void setSet_dep_cd(String)` | 361 | NONE |
| 49 | `String getEnd_dt()` | 365 | NONE |
| 50 | `void setEnd_dt(String)` | 369 | NONE |
| 51 | `String getHireNo()` | 373 | NONE |
| 52 | `void setHireNo(String)` | 377 | NONE |
| 53 | `ArrayList getLastServDateList()` | 382 | NONE |
| 54 | `void setLastServDateList(ArrayList)` | 386 | NONE |
| 55 | `String getServHourInterval()` | 390 | NONE |
| 56 | `void setServHourInterval(String)` | 394 | NONE |
| 57 | `String getDateInteval()` | 398 | NONE |
| 58 | `void setDateInteval(String)` | 402 | NONE |
| 59 | `void setLastServDate(String)` | 406 | NONE |
| 60 | `String getLastServDate()` | 410 | NONE |
| 61 | `String getSt_dt()` | 414 | NONE |
| 62 | `void setSt_dt(String)` | 418 | NONE |
| 63 | `ArrayList getService_id()` | 422 | NONE |
| 64 | `void setService_id(ArrayList)` | 426 | NONE |
| 65 | `ArrayList getService_hour()` | 430 | NONE |
| 66 | `void setService_hour(ArrayList)` | 434 | NONE |
| 67 | `ArrayList getSm_hour_meter()` | 438 | NONE |
| 68 | `void setSm_hour_meter(ArrayList)` | 442 | NONE |
| 69 | `ArrayList getSm_service_from()` | 446 | NONE |
| 70 | `void setSm_service_from(ArrayList)` | 450 | NONE |
| 71 | `ArrayList getSm_ser_ed()` | 454 | NONE |
| 72 | `void setSm_ser_ed(ArrayList)` | 458 | NONE |
| 73 | `String getT_sm_hm_s()` | 462 | NONE |
| 74 | `void setT_sm_hm_s(String)` | 466 | NONE |
| 75 | `Statement getStmt()` | 471 | NONE |
| 76 | `void setStmt(Statement)` | 475 | NONE |
| 77 | `Statement getStmt1()` | 479 | NONE |
| 78 | `void setStmt1(Statement)` | 483 | NONE |
| 79 | `ArrayList getServHourIntervalList()` | 487 | NONE |
| 80 | `void setServHourIntervalList(ArrayList)` | 491 | NONE |
| 81 | `ArrayList getVmachine_cd()` | 495 | NONE |
| 82 | `void setVmachine_cd(ArrayList)` | 499 | NONE |
| 83 | `ArrayList getVs_no()` | 503 | NONE |
| 84 | `void setVs_no(ArrayList)` | 507 | NONE |
| 85 | `ArrayList getDateIntervalList()` | 511 | NONE |
| 86 | `void setDateIntervalList(ArrayList)` | 515 | NONE |
| 87 | `ArrayList getNextServHourLst()` | 519 | NONE |
| 88 | `void setNextServHourLst(ArrayList)` | 523 | NONE |
| 89 | `Boolean getIs_user_admin()` | 527 | NONE |
| 90 | `void setIs_user_admin(Boolean)` | 530 | NONE |
| 91 | `Boolean getIs_user_lmh()` | 533 | NONE |
| 92 | `void setIs_user_lmh(Boolean)` | 536 | NONE |
| 93 | `void setAccess_cust(String)` | 539 | NONE |
| 94 | `void testQueries(int)` | 543 | NONE |
| 95 | `String getHrAtLastServ(String, String)` | 886 | NONE |
| 96 | `String getDept_prefix(String)` | 966 | NONE |

**TODO/FIXME/HACK/XXX:** None
**Misleading Comments:**
- Line 106: `// Try connecting the database` -- generic comment; does not mention that `init()` also branches on `opCode` to invoke different query methods.

**Findings:**

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| SDFB-01 | MEDIUM | 29 | No class-level Javadoc on a 1003-line class that mixes data-bean responsibilities with database access (JNDI lookup, SQL queries). This is the most complex class in the batch and desperately needs architectural documentation. |
| SDFB-02 | MEDIUM | 104-165 | `init()` -- complex 60-line lifecycle method that performs JNDI lookup, obtains a DB connection, branches on `opCode`, and handles resource cleanup. Completely undocumented. |
| SDFB-03 | MEDIUM | 543-561 | `testQueries(int count)` -- public method that runs raw SQL in a loop using hex-incrementing IDs and hardcoded message parameters. No Javadoc explaining purpose, expected inputs, or why test code is in a production bean. |
| SDFB-04 | MEDIUM | 886-942 | `getHrAtLastServ(String, String)` -- 56-line public method that opens its own DB connection (separate from `init()`), runs queries, and converts results. No Javadoc. |
| SDFB-05 | MEDIUM | 966-999 | `getDept_prefix(String vcd)` -- public method that opens its own DB connection to look up department prefix. No Javadoc. |
| SDFB-06 | HIGH | 106 | Comment `// Try connecting the database` is misleading -- `init()` does far more than just connect; it dispatches to `Fetch_service_status_veh()`, `Fetch_serv_mnt_data()`, or `testQueries()` depending on `opCode`. The comment obscures this critical branching logic. |
| SDFB-07 | LOW | 90-539 | All 93 getter/setter methods (including `getStmt()/setStmt()` that expose raw `Statement` objects) lack Javadoc. |
| SDFB-08 | LOW | 168-192 | `clearVariables()` has no Javadoc. Clears 17 ArrayLists; purpose and expected lifecycle call-point not documented. |

---

### 5. SiteConfigurationBean.java (157 lines)

**Class:** `SiteConfigurationBean` (line 5)
**Class-level Javadoc:** NONE (only auto-generated serialVersionUID comment)
**Implements/Extends:** `Serializable`

**Public Methods:**

| # | Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `String getIdtype()` | 32 | NONE |
| 2 | `void setIdtype(String)` | 35 | NONE |
| 3 | `String getId()` | 39 | NONE |
| 4 | `void setId(String)` | 42 | NONE |
| 5 | `String getModule_type()` | 45 | NONE |
| 6 | `void setModule_type(String)` | 48 | NONE |
| 7 | `String getReader_type()` | 51 | NONE |
| 8 | `void setReader_type(String)` | 54 | NONE |
| 9 | `String getSim_supplier()` | 57 | NONE |
| 10 | `void setSim_supplier(String)` | 60 | NONE |
| 11 | `String getSim_type()` | 63 | NONE |
| 12 | `void setSim_type(String)` | 66 | NONE |
| 13 | `String getDriver_base()` | 69 | NONE |
| 14 | `void setDriver_base(String)` | 72 | NONE |
| 15 | `String getTime_base()` | 75 | NONE |
| 16 | `void setTime_base(String)` | 78 | NONE |
| 17 | `String getTimeslot1()` | 81 | NONE |
| 18 | `void setTimeslot1(String)` | 84 | NONE |
| 19 | `String getTimeslot2()` | 87 | NONE |
| 20 | `void setTimeslot2(String)` | 90 | NONE |
| 21 | `String getTimeslot3()` | 93 | NONE |
| 22 | `void setTimeslot3(String)` | 96 | NONE |
| 23 | `String getTimeslot4()` | 99 | NONE |
| 24 | `void setTimeslot4(String)` | 102 | NONE |
| 25 | `String getIdle_timer()` | 105 | NONE |
| 26 | `void setIdle_timer(String)` | 108 | NONE |
| 27 | `String getSurvey_timer()` | 111 | NONE |
| 28 | `void setSurvey_timer(String)` | 114 | NONE |
| 29 | `String getContact_nm()` | 117 | NONE |
| 30 | `void setContact_nm(String)` | 120 | NONE |
| 31 | `String getContact_no()` | 123 | NONE |
| 32 | `void setContact_no(String)` | 126 | NONE |
| 33 | `String getContact_email()` | 129 | NONE |
| 34 | `void setContact_email(String)` | 132 | NONE |
| 35 | `String getComments()` | 135 | NONE |
| 36 | `void setComments(String)` | 138 | NONE |
| 37 | `String getFacility_code()` | 142 | NONE |
| 38 | `void setFacility_code(String)` | 145 | NONE |
| 39 | `String getSuper_card()` | 148 | NONE |
| 40 | `void setSuper_card(String)` | 151 | NONE |

**TODO/FIXME/HACK/XXX:** None
**Misleading Comments:** None

**Findings:**

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| SCB-01 | LOW | 5 | No class-level Javadoc. Bean likely configures hardware site setup (module type, reader, SIM, timeslots, idle/survey timers) but this is not documented. |
| SCB-02 | LOW | 32-153 | All 40 getter/setter methods lack Javadoc. |

---

### 6. SpareModuleBean.java (120 lines)

**Class:** `SpareModuleBean` (line 3)
**Class-level Javadoc:** NONE
**Implements/Extends:** (none)

**Public Methods:**

| # | Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `int getSpare_modules_cd()` | 21 | NONE |
| 2 | `void setSpare_modules_cd(int)` | 24 | NONE |
| 3 | `int getSpare_status_cd()` | 27 | NONE |
| 4 | `void setSpare_status_cd(int)` | 30 | NONE |
| 5 | `String getType()` | 33 | NONE |
| 6 | `void setType(String)` | 36 | NONE |
| 7 | `String getGmtp_id()` | 39 | NONE |
| 8 | `void setGmtp_id(String)` | 42 | NONE |
| 9 | `String getFrom_serial()` | 45 | NONE |
| 10 | `void setFrom_serial(String)` | 48 | NONE |
| 11 | `String getCustomer()` | 51 | NONE |
| 12 | `void setCustomer(String)` | 54 | NONE |
| 13 | `String getSite()` | 57 | NONE |
| 14 | `void setSite(String)` | 60 | NONE |
| 15 | `String getDepartment()` | 63 | NONE |
| 16 | `void setDepartment(String)` | 66 | NONE |
| 17 | `String getLast_updated()` | 69 | NONE |
| 18 | `void setLast_updated(String)` | 72 | NONE |
| 19 | `String getSwap_date()` | 75 | NONE |
| 20 | `void setSwap_date(String)` | 78 | NONE |
| 21 | `String getCcid()` | 81 | NONE |
| 22 | `void setCcid(String)` | 84 | NONE |
| 23 | `String getRa_number()` | 87 | NONE |
| 24 | `void setRa_number(String)` | 90 | NONE |
| 25 | `String getSpare_status()` | 93 | NONE |
| 26 | `void setSpare_status(String)` | 96 | NONE |
| 27 | `String getFrom_gmtp_id()` | 99 | NONE |
| 28 | `void setFrom_gmtp_id(String)` | 102 | NONE |
| 29 | `String getTech_number()` | 105 | NONE |
| 30 | `void setTech_number(String)` | 108 | NONE |
| 31 | `String getNote()` | 111 | NONE |
| 32 | `void setNote(String)` | 114 | NONE |

**TODO/FIXME/HACK/XXX:** None
**Misleading Comments:** None

**Findings:**

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| SMB-01 | LOW | 3 | No class-level Javadoc. Bean tracks spare hardware module inventory (swap dates, RA numbers, CCID). |
| SMB-02 | LOW | 21-116 | All 32 getter/setter methods lack Javadoc. |

---

### 7. SpecialAccessBean.java (70 lines)

**Class:** `SpecialAccessBean` (line 3)
**Class-level Javadoc:** NONE
**Implements/Extends:** (none)

**Public Methods:**

| # | Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `int getId()` | 14 | NONE |
| 2 | `void setId(int)` | 17 | NONE |
| 3 | `String getUser_cd()` | 20 | NONE |
| 4 | `void setUser_cd(String)` | 23 | NONE |
| 5 | `String getCust_cd()` | 26 | NONE |
| 6 | `void setCust_cd(String)` | 29 | NONE |
| 7 | `String getLoc_cd()` | 32 | NONE |
| 8 | `void setLoc_cd(String)` | 35 | NONE |
| 9 | `String getDept_cd()` | 38 | NONE |
| 10 | `void setDept_cd(String)` | 41 | NONE |
| 11 | `int getModule_cd()` | 44 | NONE |
| 12 | `void setModule_cd(int)` | 47 | NONE |
| 13 | `boolean isEnabled()` | 50 | NONE |
| 14 | `void setEnabled(boolean)` | 53 | NONE |
| 15 | `String getCustName()` | 56 | NONE |
| 16 | `void setCustName(String)` | 59 | NONE |
| 17 | `String getUserName()` | 62 | NONE |
| 18 | `void setUserName(String)` | 65 | NONE |

**TODO/FIXME/HACK/XXX:** None
**Misleading Comments:** None

**Findings:**

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| SAB-01 | LOW | 3 | No class-level Javadoc. Bean represents special access permissions per user/customer/module but no documentation exists. |
| SAB-02 | LOW | 14-67 | All 18 getter/setter methods lack Javadoc. |

---

### 8. SubscriptionBean.java (51 lines)

**Class:** `SubscriptionBean` (line 7)
**Class-level Javadoc:** NONE (only auto-generated serialVersionUID comment)
**Implements/Extends:** `Serializable`

**Public Methods:**

| # | Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `String getCust_cd()` | 21 | NONE |
| 2 | `void setCust_cd(String)` | 24 | NONE |
| 3 | `String getLoc_cd()` | 27 | NONE |
| 4 | `void setLoc_cd(String)` | 30 | NONE |
| 5 | `String getDept_cd()` | 33 | NONE |
| 6 | `void setDept_cd(String)` | 36 | NONE |
| 7 | `String getMonth()` | 39 | NONE |
| 8 | `void setMonth(String)` | 42 | NONE |
| 9 | `String getEmail()` | 45 | NONE |
| 10 | `void setEmail(String)` | 48 | NONE |

**TODO/FIXME/HACK/XXX:** None
**Misleading Comments:** None

**Findings:**

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| SUB-01 | LOW | 7 | No class-level Javadoc. Bean likely represents email subscription configuration per customer/location/department but this is undocumented. |
| SUB-02 | LOW | 21-50 | All 10 getter/setter methods lack Javadoc. |

---

### 9. SuperMasterAuthBean.java (69 lines)

**Class:** `SuperMasterAuthBean` (line 3)
**Class-level Javadoc:** NONE
**Implements/Extends:** (none)

**Public Methods:**

| # | Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `SuperMasterAuthBean()` | 7 | NONE |
| 2 | `String getFleetNo()` | 11 | NONE |
| 3 | `String getSerialNo()` | 15 | NONE |
| 4 | `String getAuthStart()` | 19 | NONE |
| 5 | `String getAuthEnd()` | 23 | NONE |
| 6 | `String getServHourFrom()` | 27 | NONE |
| 7 | `String getSuperMasterCode()` | 31 | NONE |
| 8 | `void setFleetNo(String)` | 35 | NONE |
| 9 | `void setSerialNo(String)` | 39 | NONE |
| 10 | `void setAuthStart(String)` | 43 | NONE |
| 11 | `void setAuthEnd(String)` | 47 | NONE |
| 12 | `void setServHourFrom(String)` | 51 | NONE |
| 13 | `void setSuperMasterCode(String)` | 55 | NONE |
| 14 | `String getCustName()` | 59 | NONE |
| 15 | `void setCustName(String)` | 63 | NONE |

**TODO/FIXME/HACK/XXX:**
- Line 8: `// TODO Auto-generated constructor stub` -- IDE-generated placeholder left in place.

**Misleading Comments:** None

**Findings:**

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| SMAB-01 | LOW | 3 | No class-level Javadoc. Bean relates to super-master authorization (access card auth time windows?) but purpose is undocumented. |
| SMAB-02 | LOW | 7-65 | All 15 public methods lack Javadoc. |
| SMAB-03 | INFO | 8 | Stale `TODO Auto-generated constructor stub` left from IDE scaffolding. Constructor body is empty. |

---

### 10. UnitBean.java (166 lines)

**Class:** `UnitBean` (line 6)
**Class-level Javadoc:** NONE (only auto-generated serialVersionUID comment)
**Implements/Extends:** `Serializable`

**Public Methods:**

| # | Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `int getThreshold()` | 35 | NONE |
| 2 | `void setThreshold(int)` | 38 | NONE |
| 3 | `String getVeh_cd()` | 42 | NONE |
| 4 | `void setVeh_cd(String)` | 45 | NONE |
| 5 | `String getGmtp_id()` | 48 | NONE |
| 6 | `void setGmtp_id(String)` | 51 | NONE |
| 7 | `String getCust_nm()` | 54 | NONE |
| 8 | `void setCust_nm(String)` | 57 | NONE |
| 9 | `String getLoc_nm()` | 60 | NONE |
| 10 | `void setLoc_nm(String)` | 63 | NONE |
| 11 | `String getDept_nm()` | 66 | NONE |
| 12 | `void setDept_nm(String)` | 69 | NONE |
| 13 | `String getModel()` | 72 | NONE |
| 14 | `void setModel(String)` | 75 | NONE |
| 15 | `String getState()` | 78 | NONE |
| 16 | `void setState(String)` | 81 | NONE |
| 17 | `String getHire_no()` | 84 | NONE |
| 18 | `void setHire_no(String)` | 87 | NONE |
| 19 | `String getSerial_no()` | 90 | NONE |
| 20 | `void setSerial_no(String)` | 93 | NONE |
| 21 | `Date getActive_date()` | 96 | NONE |
| 22 | `void setActive_date(Date)` | 99 | NONE |
| 23 | `String getCur_version()` | 102 | NONE |
| 24 | `void setCur_version(String)` | 105 | NONE |
| 25 | `String getSim_provider()` | 108 | NONE |
| 26 | `void setSim_provider(String)` | 111 | NONE |
| 27 | `String getCcid()` | 114 | NONE |
| 28 | `void setCcid(String)` | 117 | NONE |
| 29 | `String getOld_ccid()` | 120 | NONE |
| 30 | `void setOld_ccid(String)` | 123 | NONE |
| 31 | `String getCcid_rpt_time()` | 126 | NONE |
| 32 | `void setCcid_rpt_time(String)` | 129 | NONE |
| 33 | `String getModerm_version()` | 132 | NONE |
| 34 | `void setModerm_version(String)` | 135 | NONE |
| 35 | `String getOld_gmtpid()` | 138 | NONE |
| 36 | `void setOld_gmtpid(String)` | 141 | NONE |
| 37 | `String getLast_session()` | 144 | NONE |
| 38 | `String getService_from()` | 147 | NONE |
| 39 | `void setLast_session(String)` | 151 | NONE |
| 40 | `void setService_from(String)` | 154 | NONE |
| 41 | `String getService_hour()` | 157 | NONE |
| 42 | `void setService_hour(String)` | 160 | NONE |

**TODO/FIXME/HACK/XXX:** None
**Misleading Comments:** None

**Findings:**

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| UB-01 | LOW | 6 | No class-level Javadoc. Core unit/vehicle bean with extensive fields (GMTP ID, CCID, versions, service hours) but no documentation. |
| UB-02 | LOW | 35-162 | All 42 getter/setter methods lack Javadoc. Field `moderm_version` appears to be a typo for "modem_version" but no documentation clarifies intent. |

---

### 11. UnitUtilSummaryBean.java (113 lines)

**Class:** `UnitUtilSummaryBean` (line 5)
**Class-level Javadoc:** NONE (only auto-generated serialVersionUID comment)
**Implements/Extends:** `Serializable`

**Public Methods:**

| # | Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `String getHire_no()` | 27 | NONE |
| 2 | `void setHire_no(String)` | 30 | NONE |
| 3 | `String getSerial_no()` | 33 | NONE |
| 4 | `void setSerial_no(String)` | 36 | NONE |
| 5 | `String getModel_nm()` | 39 | NONE |
| 6 | `void setModel_nm(String)` | 42 | NONE |
| 7 | `String getKeyHours_percentage()` | 45 | NONE |
| 8 | `void setKeyHours_percentage(String)` | 48 | NONE |
| 9 | `String getTotal_hours()` | 51 | NONE |
| 10 | `void setTotal_hours(String)` | 54 | NONE |
| 11 | `String getKey_hours()` | 57 | NONE |
| 12 | `void setKey_hours(String)` | 60 | NONE |
| 13 | `String getSeat_hours()` | 63 | NONE |
| 14 | `void setSeat_hours(String)` | 66 | NONE |
| 15 | `String getSeatHours_percentage()` | 69 | NONE |
| 16 | `void setSeatHours_percentage(String)` | 72 | NONE |
| 17 | `String getTrack_hours()` | 75 | NONE |
| 18 | `void setTrack_hours(String)` | 78 | NONE |
| 19 | `String getTrackHours_percentage()` | 81 | NONE |
| 20 | `void setTrackHours_percentage(String)` | 84 | NONE |
| 21 | `String getHydl_hours()` | 87 | NONE |
| 22 | `void setHydl_hours(String)` | 90 | NONE |
| 23 | `String getHydlHours_percentage()` | 93 | NONE |
| 24 | `void setHydlHours_percentage(String)` | 96 | NONE |
| 25 | `String getIn_hours()` | 99 | NONE |
| 26 | `void setIn_hours(String)` | 102 | NONE |
| 27 | `String getInHours_percentage()` | 105 | NONE |
| 28 | `void setInHours_percentage(String)` | 108 | NONE |

**TODO/FIXME/HACK/XXX:** None
**Misleading Comments:** None

**Findings:**

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| UUSB-01 | LOW | 5 | No class-level Javadoc. Bean summarizes unit utilization (key, seat, track, hydraulic hours with percentages) but no documentation. |
| UUSB-02 | LOW | 27-110 | All 28 getter/setter methods lack Javadoc. Abbreviation "hydl" (hydraulic?) is not documented. |

---

### 12. UnitVersionInfoBean.java (33 lines)

**Class:** `UnitVersionInfoBean` (line 3)
**Class-level Javadoc:** NONE
**Implements/Extends:** (none)

**Public Methods:**

| # | Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `String getGmtpId()` | 9 | NONE |
| 2 | `void setGmtpId(String)` | 12 | NONE |
| 3 | `boolean isChar100MaxSupported()` | 15 | NONE |
| 4 | `void setChar100MaxSupported(boolean)` | 18 | NONE |
| 5 | `boolean isChar150MaxSupported()` | 21 | NONE |
| 6 | `void setChar150MaxSupported(boolean)` | 24 | NONE |
| 7 | `boolean isChar150MaxMultiSupported()` | 27 | NONE |
| 8 | `void setChar150MaxMultiSupported(boolean)` | 30 | NONE |

**TODO/FIXME/HACK/XXX:** None
**Misleading Comments:** None

**Findings:**

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| UVIB-01 | LOW | 3 | No class-level Javadoc. Bean tracks firmware/protocol version capabilities (char100Max, char150Max, char150MaxMulti) but meaning of these capability flags is undocumented. |
| UVIB-02 | LOW | 9-32 | All 8 getter/setter methods lack Javadoc. |

---

### 13. UnitutilBean.java (189 lines)

**Class:** `UnitutilBean` (line 7)
**Class-level Javadoc:** NONE (only auto-generated serialVersionUID comment)
**Implements/Extends:** `Serializable`

**Public Methods:**

| # | Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `UnitutilBean()` | 35 | NONE |
| 2 | `String getVeh_cd()` | 42 | NONE |
| 3 | `void setVeh_cd(String)` | 46 | NONE |
| 4 | `String getVmachine_nm()` | 50 | NONE |
| 5 | `void setVmachine_nm(String)` | 54 | NONE |
| 6 | `HashMap<String, ArrayList<Integer>> getUtilMap()` | 58 | NONE |
| 7 | `void setUtilMap(HashMap<String, ArrayList<Integer>>)` | 62 | NONE |
| 8 | `String getModel_name()` | 66 | NONE |
| 9 | `void setModel_name(String)` | 70 | NONE |
| 10 | `int[] getUtil()` | 74 | NONE |
| 11 | `void setUtil(int, int)` | 78 | NONE |
| 12 | `int getTotal()` | 82 | NONE |
| 13 | `void setTotal(int)` | 86 | NONE |
| 14 | `HashMap<String, ImpactBean> getImpactMap()` | 90 | NONE |
| 15 | `void setImpactMap(HashMap<String, ImpactBean>)` | 94 | NONE |
| 16 | `void setArrUtil(ArrayList<HashMap<String, ImpactBean>>)` | 98 | NONE |
| 17 | `void addArrUtil(HashMap<String, ImpactBean>)` | 102 | NONE |
| 18 | `ArrayList<HashMap<String, ImpactBean>> getArrUtil()` | 106 | NONE |
| 19 | `String getDept_cd()` | 110 | NONE |
| 20 | `void setDept_cd(String)` | 114 | NONE |
| 21 | `String getDept_name()` | 118 | NONE |
| 22 | `void setDept_name(String)` | 122 | NONE |
| 23 | `String getLoc_cd()` | 126 | NONE |
| 24 | `void setLoc_cd(String)` | 130 | NONE |
| 25 | `String getLoc_name()` | 134 | NONE |
| 26 | `void setLoc_name(String)` | 138 | NONE |
| 27 | `String getWeek()` | 142 | NONE |
| 28 | `void setWeek(String)` | 146 | NONE |
| 29 | `String getModel_cd()` | 150 | NONE |
| 30 | `void setModel_cd(String)` | 154 | NONE |
| 31 | `String getWfrom()` | 158 | NONE |
| 32 | `void setWfrom(String)` | 162 | NONE |
| 33 | `String getWto()` | 166 | NONE |
| 34 | `void setWto(String)` | 170 | NONE |
| 35 | `int getWeek_int()` | 174 | NONE |
| 36 | `void setWeek_int(int)` | 178 | NONE |
| 37 | `String getChart_URL()` | 182 | NONE |
| 38 | `void setChart_URL(String)` | 186 | NONE |

**TODO/FIXME/HACK/XXX:** None
**Misleading Comments:**
- Line 34: `//construction` -- trivially obvious; not harmful but adds no value.

**Findings:**

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| UUB-01 | LOW | 7 | No class-level Javadoc. Bean holds unit utilization data with complex nested maps (utilMap, impactMap, arrUtil) but data model is completely undocumented. |
| UUB-02 | LOW | 35-188 | All 38 public methods lack Javadoc. `setUtil(int, int)` is a non-standard indexed setter with no documentation of the index semantics (the int[8] array maps to 8 unnamed slots). |

---

### 14. UnusedUnitBean.java (90 lines)

**Class:** `UnusedUnitBean` (line 5)
**Class-level Javadoc:** NONE (only auto-generated serialVersionUID comment)
**Implements/Extends:** `Serializable`

**Public Methods:**

| # | Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `String getCust_name()` | 24 | NONE |
| 2 | `void setCust_name(String)` | 27 | NONE |
| 3 | `String getSite_name()` | 30 | NONE |
| 4 | `void setSite_name(String)` | 33 | NONE |
| 5 | `String getFleet_no()` | 36 | NONE |
| 6 | `void setFleet_no(String)` | 39 | NONE |
| 7 | `String getSerial_no()` | 42 | NONE |
| 8 | `void setSerial_no(String)` | 45 | NONE |
| 9 | `String getLast_report()` | 48 | NONE |
| 10 | `void setLast_report(String)` | 51 | NONE |
| 11 | `String getGmtp_id()` | 54 | NONE |
| 12 | `void setGmtp_id(String)` | 57 | NONE |
| 13 | `String getCcid()` | 60 | NONE |
| 14 | `void setCcid(String)` | 63 | NONE |
| 15 | `String getVcd()` | 66 | NONE |
| 16 | `void setVcd(String)` | 69 | NONE |
| 17 | `String getInactive_days()` | 72 | NONE |
| 18 | `void setInactive_days(String)` | 75 | NONE |
| 19 | `boolean isOnHire()` | 78 | NONE |
| 20 | `void setOnHire(boolean)` | 81 | NONE |
| 21 | `String getState_name()` | 84 | NONE |
| 22 | `void setState_name(String)` | 87 | NONE |

**TODO/FIXME/HACK/XXX:** None
**Misleading Comments:** None

**Findings:**

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| UUnitB-01 | LOW | 5 | No class-level Javadoc. Bean represents units identified as unused/inactive but purpose and criteria not documented. |
| UUnitB-02 | LOW | 24-89 | All 22 getter/setter methods lack Javadoc. |

---

### 15. UserBean.java (51 lines)

**Class:** `UserBean` (line 3)
**Class-level Javadoc:** NONE
**Implements/Extends:** (none)

**Public Methods:**

| # | Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `int getId()` | 12 | NONE |
| 2 | `String getUsername()` | 15 | NONE |
| 3 | `String getFirstname()` | 18 | NONE |
| 4 | `String getLastname()` | 21 | NONE |
| 5 | `String getEmail()` | 24 | NONE |
| 6 | `void setId(int)` | 27 | NONE |
| 7 | `void setUsername(String)` | 30 | NONE |
| 8 | `void setFirstname(String)` | 33 | NONE |
| 9 | `void setLastname(String)` | 36 | NONE |
| 10 | `void setEmail(String)` | 39 | NONE |
| 11 | `String getLastUpdate()` | 42 | NONE |
| 12 | `void setLastUpdate(String)` | 45 | NONE |

**TODO/FIXME/HACK/XXX:** None
**Misleading Comments:** None

**Findings:**

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| UserB-01 | LOW | 3 | No class-level Javadoc. Simple user profile bean. |
| UserB-02 | LOW | 12-47 | All 12 getter/setter methods lack Javadoc. |

---

### 16. UserDriverBean.java (50 lines)

**Class:** `UserDriverBean` (line 3)
**Class-level Javadoc:** NONE
**Implements/Extends:** (none)

**Public Methods:**

| # | Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `String getId()` | 11 | NONE |
| 2 | `String getUser_cd()` | 14 | NONE |
| 3 | `String getWeigand()` | 17 | NONE |
| 4 | `String getVeh_type()` | 20 | NONE |
| 5 | `String getFirstName()` | 23 | NONE |
| 6 | `String getLastName()` | 26 | NONE |
| 7 | `void setId(String)` | 29 | NONE |
| 8 | `void setUser_cd(String)` | 32 | NONE |
| 9 | `void setWeigand(String)` | 35 | NONE |
| 10 | `void setVeh_type(String)` | 38 | NONE |
| 11 | `void setFirstName(String)` | 41 | NONE |
| 12 | `void setLastName(String)` | 44 | NONE |

**TODO/FIXME/HACK/XXX:** None
**Misleading Comments:** None

**Findings:**

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| UDB-01 | LOW | 3 | No class-level Javadoc. Bean links users to drivers, including Wiegand card number (field `weigand` -- likely misspelled "Wiegand"). Purpose not documented. |
| UDB-02 | LOW | 11-46 | All 12 getter/setter methods lack Javadoc. |

---

### 17. UserFormBean.java (59 lines)

**Class:** `UserFormBean` (line 5)
**Class-level Javadoc:** NONE
**Implements/Extends:** (none)

**Public Methods:**

| # | Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `int getId()` | 15 | NONE |
| 2 | `void setId(int)` | 18 | NONE |
| 3 | `String getUserFomrCd()` | 21 | NONE |
| 4 | `void setUserFomrCd(String)` | 24 | NONE |
| 5 | `String getUserFomrName()` | 27 | NONE |
| 6 | `void setUserFomrName(String)` | 30 | NONE |
| 7 | `String getUserFormMenuView()` | 33 | NONE |
| 8 | `void setUserFormMenuView(String)` | 36 | NONE |
| 9 | `String getUserFormMenuEdit()` | 39 | NONE |
| 10 | `void setUserFormMenuEdit(String)` | 42 | NONE |
| 11 | `String getUserFormDelete()` | 45 | NONE |
| 12 | `void setUserFormDelete(String)` | 48 | NONE |
| 13 | `String getUserFormMenuPrint()` | 51 | NONE |
| 14 | `void setUserFormMenuPrint(String)` | 54 | NONE |

**TODO/FIXME/HACK/XXX:** None
**Misleading Comments:** None

**Findings:**

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| UFB-01 | LOW | 5 | No class-level Javadoc. Bean maps user form access rights (view, edit, delete, print) but undocumented. Fields `userFomrCd` and `userFomrName` contain typo "Fomr" (should be "Form"). |
| UFB-02 | LOW | 15-56 | All 14 getter/setter methods lack Javadoc. |

---

### 18. VehDiagnostic.java (218 lines)

**Class:** `VehDiagnostic` (line 3)
**Class-level Javadoc:** NONE
**Implements/Extends:** (none)

**Public Methods:**

| # | Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `int getVehicleCd()` | 33 | NONE |
| 2 | `String getUtcTime()` | 37 | NONE |
| 3 | `String getFirmwareVer()` | 41 | NONE |
| 4 | `String getCcid()` | 45 | NONE |
| 5 | `String getTimezone()` | 49 | NONE |
| 6 | `String getSignalStr()` | 53 | NONE |
| 7 | `String getLastPreop()` | 57 | NONE |
| 8 | `String getShockThreshold()` | 61 | NONE |
| 9 | `String getRedImpactThreshold()` | 65 | NONE |
| 10 | `String getApn()` | 69 | NONE |
| 11 | `String getHardwareVer()` | 73 | NONE |
| 12 | `String getModemVer()` | 77 | NONE |
| 13 | `String getCanCRC()` | 81 | NONE |
| 14 | `void setVehicleCd(int)` | 85 | NONE |
| 15 | `void setUtcTime(String)` | 89 | NONE |
| 16 | `void setFirmwareVer(String)` | 93 | NONE |
| 17 | `void setCcid(String)` | 97 | NONE |
| 18 | `void setTimezone(String)` | 101 | NONE |
| 19 | `void setSignalStr(String)` | 105 | NONE |
| 20 | `void setLastPreop(String)` | 109 | NONE |
| 21 | `void setShockThreshold(String)` | 113 | NONE |
| 22 | `void setRedImpactThreshold(String)` | 117 | NONE |
| 23 | `void setApn(String)` | 121 | NONE |
| 24 | `void setHardwareVer(String)` | 125 | NONE |
| 25 | `void setModemVer(String)` | 129 | NONE |
| 26 | `void setCanCRC(String)` | 133 | NONE |
| 27 | `boolean isThresholdSync()` | 137 | NONE |
| 28 | `boolean isTimezoneSync()` | 141 | NONE |
| 29 | `void setThresholdSync(boolean)` | 145 | NONE |
| 30 | `void setTimezoneSync(boolean)` | 149 | NONE |
| 31 | `boolean isRedImpactSync()` | 153 | NONE |
| 32 | `void setRedImpactSync(boolean)` | 157 | NONE |
| 33 | `double getCurrentThreshold()` | 161 | NONE |
| 34 | `long getCurrentFSSXThreshold()` | 165 | NONE |
| 35 | `void setCurrentThreshold(double)` | 169 | NONE |
| 36 | `void setCurrentFSSXThreshold(long)` | 173 | NONE |
| 37 | `int getCurrentTimezone()` | 177 | NONE |
| 38 | `void setCurrentTimezone(int)` | 181 | NONE |
| 39 | `String getCurrentCRC()` | 185 | NONE |
| 40 | `boolean isCrcSync()` | 189 | NONE |
| 41 | `void setCurrentCRC(String)` | 193 | NONE |
| 42 | `void setCrcSync(boolean)` | 197 | NONE |
| 43 | `String getKernelBuild()` | 201 | NONE |
| 44 | `String getExpModVer()` | 205 | NONE |
| 45 | `void setKernelBuild(String)` | 209 | NONE |
| 46 | `void setExpModVer(String)` | 213 | NONE |

**TODO/FIXME/HACK/XXX:** None
**Misleading Comments:** None

**Findings:**

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| VD-01 | MEDIUM | 3 | No class-level Javadoc on a substantial diagnostic bean (46 methods). Contains both "reported" values (from device) and "current" values (from DB config) plus sync flags, but the dual-value/sync-check pattern is not documented anywhere. |
| VD-02 | LOW | 33-215 | All 46 getter/setter methods lack Javadoc. Abbreviations "FSSX", "CRC", "APN" are domain-specific and unexplained. |

---

### 19. VehNetworkSettingsBean.java (35 lines)

**Class:** `VehNetworkSettingsBean` (line 3)
**Class-level Javadoc:** NONE
**Implements/Extends:** (none)

**Public Methods:**

| # | Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `int getIndex()` | 5 | NONE |
| 2 | `void setIndex(int)` | 8 | NONE |
| 3 | `String getCountry()` | 11 | NONE |
| 4 | `void setCountry(String)` | 14 | NONE |
| 5 | `String getSsid()` | 17 | NONE |
| 6 | `void setSsid(String)` | 20 | NONE |
| 7 | `String getPassword()` | 23 | NONE |
| 8 | `void setPassword(String)` | 26 | NONE |

**TODO/FIXME/HACK/XXX:** None
**Misleading Comments:** None

**Findings:**

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| VNSB-01 | LOW | 3 | No class-level Javadoc. Bean holds WiFi network settings (SSID, password, country) for vehicle modules but purpose undocumented. |
| VNSB-02 | LOW | 5-28 | All 8 getter/setter methods lack Javadoc. |

---

### 20. VehicleImportBean.java (140 lines)

**Class:** `VehicleImportBean` (line 3)
**Class-level Javadoc:** NONE
**Implements/Extends:** (none)

**Public Methods:**

| # | Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `String getSite_name()` | 25 | NONE |
| 2 | `void setSite_name(String)` | 28 | NONE |
| 3 | `String getDepartment_name()` | 31 | NONE |
| 4 | `void setDepartment_name(String)` | 34 | NONE |
| 5 | `String getGmtp_id()` | 37 | NONE |
| 6 | `void setGmtp_id(String)` | 40 | NONE |
| 7 | `String getSerial_no()` | 44 | NONE |
| 8 | `void setSerial_no(String)` | 47 | NONE |
| 9 | `String getEquipNo()` | 50 | NONE |
| 10 | `void setEquipNo(String)` | 53 | NONE |
| 11 | `String getModel()` | 56 | NONE |
| 12 | `void setModel(String)` | 59 | NONE |
| 13 | `String getCanRule()` | 62 | NONE |
| 14 | `void setCanRule(String)` | 65 | NONE |
| 15 | `String getSurv_to()` | 68 | NONE |
| 16 | `void setSurv_to(String)` | 71 | NONE |
| 17 | `String getSeat_idle()` | 74 | NONE |
| 18 | `void setSeat_idle(String)` | 77 | NONE |
| 19 | `String getQuestion_sched()` | 80 | NONE |
| 20 | `void setQuestion_sched(String)` | 83 | NONE |
| 21 | `String getTimeslot1()` | 86 | NONE |
| 22 | `void setTimeslot1(String)` | 89 | NONE |
| 23 | `String getTimeslot2()` | 92 | NONE |
| 24 | `void setTimeslot2(String)` | 95 | NONE |
| 25 | `String getTimeslot3()` | 98 | NONE |
| 26 | `void setTimeslot3(String)` | 101 | NONE |
| 27 | `String getTimeslot4()` | 104 | NONE |
| 28 | `void setTimeslot4(String)` | 107 | NONE |
| 29 | `String getCustCd()` | 110 | NONE |
| 30 | `void setCustCd(String)` | 113 | NONE |
| 31 | `int getServHrsInterval()` | 116 | NONE |
| 32 | `void setServHrsInterval(int)` | 119 | NONE |
| 33 | `int getDateInterval()` | 122 | NONE |
| 34 | `void setDateInterval(int)` | 125 | NONE |
| 35 | `String getLastServDate()` | 128 | NONE |
| 36 | `void setLastServDate(String)` | 131 | NONE |
| 37 | `boolean isCanUnit()` | 134 | NONE |
| 38 | `void setCanUnit(boolean)` | 137 | NONE |

**TODO/FIXME/HACK/XXX:** None
**Misleading Comments:** None

**Findings:**

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| VIB-01 | LOW | 3 | No class-level Javadoc. Bean used for bulk vehicle import (maps spreadsheet columns to vehicle properties?) but process and expected data format not documented. |
| VIB-02 | LOW | 25-139 | All 38 getter/setter methods lack Javadoc. |

---

## Consolidated Findings Summary

### HIGH Severity

| ID | File | Line(s) | Description |
|---|---|---|---|
| SDFB-06 | ServiceDueFlagBean.java | 106 | Misleading comment `// Try connecting the database` understates `init()` which also dispatches business logic via `opCode` branching. |

### MEDIUM Severity

| ID | File | Line(s) | Description |
|---|---|---|---|
| SDFB-01 | ServiceDueFlagBean.java | 29 | No class-level Javadoc on 1003-line class mixing bean and DAO responsibilities. |
| SDFB-02 | ServiceDueFlagBean.java | 104-165 | `init()` -- complex lifecycle method with JNDI, DB, and business dispatch. Undocumented. |
| SDFB-03 | ServiceDueFlagBean.java | 543-561 | `testQueries(int)` -- public test method with hardcoded SQL in production bean. Undocumented. |
| SDFB-04 | ServiceDueFlagBean.java | 886-942 | `getHrAtLastServ(String, String)` -- 56-line public DB-accessing method. Undocumented. |
| SDFB-05 | ServiceDueFlagBean.java | 966-999 | `getDept_prefix(String)` -- public DB-accessing method. Undocumented. |
| VD-01 | VehDiagnostic.java | 3 | No class-level Javadoc on 46-method diagnostic bean with dual reported/current value pattern. |

### LOW Severity

| ID | File | Line(s) | Description |
|---|---|---|---|
| QB-01 | QuestionBean.java | 3 | No class-level Javadoc. |
| QB-02 | QuestionBean.java | 22-125 | 34 undocumented getter/setter methods. |
| RAUB-01 | RestrictedAccessUsageBean.java | 3 | No class-level Javadoc. |
| RAUB-02 | RestrictedAccessUsageBean.java | 7-97 | 23 undocumented public methods. |
| SFTP-01 | SFTPSettings.java | 3 | No class-level Javadoc. |
| SFTP-02 | SFTPSettings.java | 16-57 | 14 undocumented getter/setter methods. |
| SDFB-07 | ServiceDueFlagBean.java | 90-539 | 93 undocumented getter/setter methods. |
| SDFB-08 | ServiceDueFlagBean.java | 168-192 | `clearVariables()` undocumented. |
| SCB-01 | SiteConfigurationBean.java | 5 | No class-level Javadoc. |
| SCB-02 | SiteConfigurationBean.java | 32-153 | 40 undocumented getter/setter methods. |
| SMB-01 | SpareModuleBean.java | 3 | No class-level Javadoc. |
| SMB-02 | SpareModuleBean.java | 21-116 | 32 undocumented getter/setter methods. |
| SAB-01 | SpecialAccessBean.java | 3 | No class-level Javadoc. |
| SAB-02 | SpecialAccessBean.java | 14-67 | 18 undocumented getter/setter methods. |
| SUB-01 | SubscriptionBean.java | 7 | No class-level Javadoc. |
| SUB-02 | SubscriptionBean.java | 21-50 | 10 undocumented getter/setter methods. |
| SMAB-01 | SuperMasterAuthBean.java | 3 | No class-level Javadoc. |
| SMAB-02 | SuperMasterAuthBean.java | 7-65 | 15 undocumented public methods. |
| UB-01 | UnitBean.java | 6 | No class-level Javadoc. |
| UB-02 | UnitBean.java | 35-162 | 42 undocumented getter/setter methods. Field `moderm_version` is likely a typo. |
| UUSB-01 | UnitUtilSummaryBean.java | 5 | No class-level Javadoc. |
| UUSB-02 | UnitUtilSummaryBean.java | 27-110 | 28 undocumented getter/setter methods. |
| UVIB-01 | UnitVersionInfoBean.java | 3 | No class-level Javadoc. |
| UVIB-02 | UnitVersionInfoBean.java | 9-32 | 8 undocumented getter/setter methods. |
| UUB-01 | UnitutilBean.java | 7 | No class-level Javadoc. |
| UUB-02 | UnitutilBean.java | 35-188 | 38 undocumented public methods. |
| UUnitB-01 | UnusedUnitBean.java | 5 | No class-level Javadoc. |
| UUnitB-02 | UnusedUnitBean.java | 24-89 | 22 undocumented getter/setter methods. |
| UserB-01 | UserBean.java | 3 | No class-level Javadoc. |
| UserB-02 | UserBean.java | 12-47 | 12 undocumented getter/setter methods. |
| UDB-01 | UserDriverBean.java | 3 | No class-level Javadoc. |
| UDB-02 | UserDriverBean.java | 11-46 | 12 undocumented getter/setter methods. |
| UFB-01 | UserFormBean.java | 5 | No class-level Javadoc. Fields contain "Fomr" typo (should be "Form"). |
| UFB-02 | UserFormBean.java | 15-56 | 14 undocumented getter/setter methods. |
| VD-02 | VehDiagnostic.java | 33-215 | 46 undocumented getter/setter methods. |
| VNSB-01 | VehNetworkSettingsBean.java | 3 | No class-level Javadoc. |
| VNSB-02 | VehNetworkSettingsBean.java | 5-28 | 8 undocumented getter/setter methods. |
| VIB-01 | VehicleImportBean.java | 3 | No class-level Javadoc. |
| VIB-02 | VehicleImportBean.java | 25-139 | 38 undocumented getter/setter methods. |

### INFO Severity

| ID | File | Line(s) | Description |
|---|---|---|---|
| RAUB-03 | RestrictedAccessUsageBean.java | 8 | Stale `TODO Auto-generated constructor stub`. |
| SMAB-03 | SuperMasterAuthBean.java | 8 | Stale `TODO Auto-generated constructor stub`. |
| UUB-03 | UnitutilBean.java | 34 | Comment `//construction` is trivially obvious, adds no value. |

---

## Observations

1. **Zero Javadoc across all 20 files.** Not a single class or method in this batch has any Javadoc comment. All 330 public methods are completely undocumented.

2. **ServiceDueFlagBean.java is the critical outlier.** At 1003 lines it mixes data-bean responsibilities with direct JNDI/JDBC database access, SQL query construction, and business logic branching. It contains the only misleading comment (HIGH finding) and accounts for 5 of the 6 MEDIUM findings.

3. **Two stale IDE-generated TODO comments** remain in `RestrictedAccessUsageBean` and `SuperMasterAuthBean`, both on empty constructors that were never implemented.

4. **Domain abbreviations are pervasive and unexplained:** GMTP, CCID, FSSX, CRC, APN, Wiegand (misspelled as "weigand"), "hydl" (hydraulic?), "Fomr" (typo for "Form"), "moderm" (typo for "modem"). Without Javadoc, these remain opaque to any developer not already familiar with the fleet hardware domain.

5. **19 of 20 files are pure data beans** (getters/setters only). The documentation problem is systematic rather than isolated -- a single class-level Javadoc on each file would provide substantial value at minimal effort.
