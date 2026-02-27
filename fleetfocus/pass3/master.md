# Pass 3 -- Documentation Audit: `master` Package

**Auditor:** A15
**Date:** 2026-02-25
**Branch:** `release/UAT_RELEASE_FLEETFOCUS_Production`
**Base path:** `WEB-INF/src/com/torrent/surat/fms6/master/`

---

## 1. Databean_customer.java (3,009 lines)

### 1.1 Reading Evidence

| # | Public Method | Line | Has Javadoc |
|---|---|---|---|
| 1 | `getCurrent_User_Site_Name()` | 189 | No |
| 2 | `getCurrent_User_Dept_Name()` | 193 | No |
| 3 | `getLicense_document_url()` | 197 | No |
| 4 | `setLicense_document_url(ArrayList)` | 200 | No |
| 5 | `getCurrent_User_Dept_Cds()` | 205 | No |
| 6 | `setCurrent_User_Dept_Cds(ArrayList)` | 209 | No |
| 7 | `getCurrent_User_Dept_Names()` | 213 | No |
| 8 | `setCurrent_User_Dept_Names(ArrayList)` | 217 | No |
| 9 | `getLicenceFile()` | 229 | No |
| 10 | `setLicenceFile(String)` | 232 | No |
| 11 | `getDriverType()` | 236 | No |
| 12 | `setDriverType(String)` | 240 | No |
| 13 | `query(String op_code)` | 331 | No |
| 14 | `getView_Batt_Name()` | 542 | No |
| 15 | `getView_Batt_Desc()` | 543 | No |
| 16 | `getView_Batt_CD()` | 544 | No |
| 17 | `getReskinPathB()` | 545 | No |
| 18 | `Query_Viewable_Battery()` | 547 | No |
| 19 | `getView_Settings_Name()` | 573 | No |
| 20 | `getView_Settings_Desc()` | 574 | No |
| 21 | `getView_Settings_CD()` | 575 | No |
| 22 | `getReskinPathDS()` | 576 | No |
| 23 | `Query_Viewable_Settings()` | 578 | No |
| 24 | `Query_Viewable_Reports()` | 600 | No |
| 25 | `getView_Report_Name()` | 617 | No |
| 26 | `getView_Report_Desc()` | 618 | No |
| 27 | `getView_Report_CD()` | 619 | No |
| 28 | `getReskinPath()` | 620 | No |
| 29 | `Query_Viewable_Menu()` | 634 | No |
| 30 | `getView_Dashmenu_CD()` | 704 | No |
| 31 | `getView_Dashmenu_Name()` | 705 | No |
| 32 | `getView_Dashmenu_Desc()` | 706 | No |
| 33 | `getView_Dashmenu_Icon()` | 707 | No |
| 34 | `getView_Dashmenu_FCD()` | 708 | No |
| 35 | `getUser_Form_Menu_CD()` | 717 | No |
| 36 | `getUser_Form_Menu_Name()` | 718 | No |
| 37 | `getUser_Form_Menu_View()` | 719 | No |
| 38 | `getUser_Form_Menu_Edit()` | 720 | No |
| 39 | `getUser_Form_Menu_Delete()` | 721 | No |
| 40 | `getUser_Form_Menu_Print()` | 722 | No |
| 41 | `getFormPath()` | 723 | No |
| 42 | `Query_User_Form_Menu()` | 725 | No |
| 43 | `getUserDepMap()` | 773 | No |
| 44 | `setUserDepMap(Map)` | 776 | No |
| 45 | `getUserModMap()` | 779 | No |
| 46 | `setUserModMap(Map)` | 782 | No |
| 47 | `getUserVehMap()` | 785 | No |
| 48 | `setUserVehMap(Map)` | 788 | No |
| 49 | `getVam_ctr()` | 791 | No |
| 50 | `setVam_ctr(int)` | 794 | No |
| 51 | `getVehCdList()` | 800 | No |
| 52 | `queryBlacklist()` | 804 | No |
| 53 | `getSupervisor_user_cds()` | 831 | No |
| 54 | `getSupervisor_user_names()` | 834 | No |
| 55 | `getSupervisor_slot_nos()` | 837 | No |
| 56 | `isCurrent_User_Is_Supervisor()` | 840 | No |
| 57 | `getSupervisor_List_user_cds()` | 844 | No |
| 58 | `setSupervisor_List_user_cds(ArrayList)` | 848 | No |
| 59 | `getSupervisor_List_user_names()` | 853 | No |
| 60 | `setSupervisor_List_user_names(ArrayList)` | 857 | No |
| 61 | `getSupervisor_List_slot_nos()` | 862 | No |
| 62 | `setSupervisor_List_slot_nos(ArrayList)` | 866 | No |
| 63 | `querySupervisorList()` | 871 | No |
| 64 | `Query_User_Access_Restriction()` | 957 | No |
| 65 | `getUnder_Dept_Cd()` | 1016 | No |
| 66 | `setUnder_Dept_Cd(ArrayList)` | 1019 | No |
| 67 | `getUnder_Dept_Nm()` | 1022 | No |
| 68 | `setUnder_Dept_Nm(ArrayList)` | 1025 | No |
| 69 | `Query_All_Models_By_Cus_Loc_Dept()` | 1029 | No |
| 70 | `Query_All_Models_By_Cus_Loc_Dept_va()` | 1163 | No |
| 71 | `Query_Current_Alert()` | 1246 | No |
| 72 | `Query_Alerts()` | 1289 | No |
| 73 | `Query_Groups_By_Cust()` | 1387 | No |
| 74 | `Query_Access_Groups()` | 1430 | No |
| 75 | `getCurrent_User_Weig_Id()` | 1465 | No |
| 76 | `setCurrent_User_Weig_Id(String)` | 1468 | No |
| 77 | `Query_Current_User()` | 1472 | No |
| 78 | `Query_All_Models()` | 1696 | No |
| 79 | `Query_Driver_License()` | 1713 | No |
| 80 | `getLicenceNumber()` | 1739 | No |
| 81 | `setLicenceNumber(String)` | 1742 | No |
| 82 | `Query_Driver_License_au()` | 1745 | No |
| 83 | `Query_CustomersUsers()` | 1763 | No |
| 84 | `Query_Customers()` | 1792 | No |
| 85 | `Query_all_Customers()` | 1835 | No |
| 86 | `Query_Locations()` | 1871 | No |
| 87 | `Query_Locations_Old()` | 1937 | No |
| 88 | `QueryEditUserDepartments()` | 1967 | No |
| 89 | `Query_Departments()` | 1992 | No |
| 90 | `Query_User()` | 2028 | No |
| 91 | `Query_Permits()` | 2049 | No |
| 92 | `getPermits_Form_Cd()` | 2071 | No |
| 93 | `getPermit_Edit_Count()` | 2072 | No |
| 94 | `getPermits_View()` | 2073 | No |
| 95 | `getPermits_Edit()` | 2074 | No |
| 96 | `getPermits_Delete()` | 2075 | No |
| 97 | `getPermits_Export()` | 2076 | No |
| 98 | `Query_Users()` | 2078 | No |
| 99 | `Query_Users_xls()` | 2327 | No |
| 100 | `Query_My_profile()` | 2567 | No |
| 101 | `Query_Customer_Data()` | 2600 | No |
| 102 | `setUser_cd(String)` | 2715 | No |
| -- | ~80 additional getter/setter methods | 2717-2998 | No |
| 103 | `Query_Bonus_Module()` | 2960 | No |
| 104 | `getCust_cd()` | 2991 | No |
| 105 | `setCust_cd(String)` | 2994 | No |
| 106 | `getCurrent_User_is_technician()` | 2998 | No |
| 107 | `getCurrent_User_is_transport()` | 3001 | No |

**Class declaration (line 30):** `public class Databean_customer` -- No class-level Javadoc.

### 1.2 Findings

| ID | Severity | Line(s) | Description |
|----|----------|---------|-------------|
| DC-DOC-01 | MEDIUM | 30 | **Missing class Javadoc.** `Databean_customer` is a large data-access bean (~3,009 lines) with no class-level documentation describing its purpose, usage, or responsibility. |
| DC-DOC-02 | MEDIUM | 331 | **Missing Javadoc on `query(String op_code)`.** This is the primary entry-point method (200+ lines) that dispatches to ~25 different query methods based on `op_code`. No documentation of valid `op_code` values, side effects, or expected state. |
| DC-DOC-03 | MEDIUM | 547, 578, 600, 634, 725 | **Missing Javadoc on public Query methods** (`Query_Viewable_Battery`, `Query_Viewable_Settings`, `Query_Viewable_Reports`, `Query_Viewable_Menu`, `Query_User_Form_Menu`). These execute complex SQL and populate multiple ArrayLists; their contracts are undocumented. |
| DC-DOC-04 | MEDIUM | 804, 871, 957 | **Missing Javadoc on public data-access methods** (`queryBlacklist`, `querySupervisorList`, `Query_User_Access_Restriction`). These perform multiple SQL queries with access-level branching logic. |
| DC-DOC-05 | MEDIUM | 1029, 1163 | **Missing Javadoc on `Query_All_Models_By_Cus_Loc_Dept()` and `Query_All_Models_By_Cus_Loc_Dept_va()`.** Complex methods with access-level filtering; no documentation explains difference between the two variants. |
| DC-DOC-06 | MEDIUM | 1246, 1289, 1387, 1430, 1472, 1696, 1713, 1745, 1763, 1792, 1835, 1871, 1937, 1967, 1992, 2028, 2049, 2078, 2327, 2567, 2600, 2960 | **All 22 remaining public Query/data-access methods lack Javadoc.** Each executes SQL and populates instance state; none have `@param`, `@throws`, or contract descriptions. |
| DC-DOC-07 | LOW | 2715-2998 | **~80 public getter/setter methods lack Javadoc.** Simple one-liner accessors for bean fields. |
| DC-DOC-08 | INFO | 27 | Inline comment `// Added by Leslie 11-07-2014` used instead of `@author` tag. |

---

## 2. Databean_getter.java (5,469 lines)

### 2.1 Reading Evidence

| # | Public Method | Line | Has Javadoc |
|---|---|---|---|
| 1 | `query(String op_code)` | 474 | No |
| 2 | `Query_Vehicle_Diagnostic()` | 872 | No |
| 3 | `Query_Customers_Locations()` | 3865 | No |
| 4 | `Query_Departments()` | 3948 | No |
| -- | ~140 additional public getter/setter methods | various | No |

**Class declaration (line 41):** `public class Databean_getter` -- No class-level Javadoc.

The file contains approximately 140+ public methods total, overwhelmingly getters/setters. The significant business-logic methods are `query(String)` (dispatches to ~30+ operation codes), `Query_Vehicle_Diagnostic()`, `Query_Customers_Locations()`, and `Query_Departments()`.

### 2.2 Findings

| ID | Severity | Line(s) | Description |
|----|----------|---------|-------------|
| DG-DOC-01 | MEDIUM | 41 | **Missing class Javadoc.** `Databean_getter` is a large data-access bean (~5,469 lines) with no class-level documentation. |
| DG-DOC-02 | MEDIUM | 474 | **Missing Javadoc on `query(String op_code)`.** This is the primary entry point (~400 lines) dispatching to 30+ private query methods based on `op_code` string values. No documentation of valid operation codes, required pre-state, or exceptions. |
| DG-DOC-03 | MEDIUM | 872, 3865, 3948 | **Missing Javadoc on public Query methods** (`Query_Vehicle_Diagnostic`, `Query_Customers_Locations`, `Query_Departments`). Complex SQL-executing methods with access-level filtering logic. |
| DG-DOC-04 | LOW | various | **~140 public getter/setter methods lack Javadoc.** All are simple accessors without documentation. |
| DG-DOC-05 | INFO | 4071, 4080, 4089 | **TODO comments:** Three identical `// TODO Auto-generated catch block` in empty catch blocks. These indicate unfinished error handling. |
| DG-DOC-06 | INFO | 812 | **Incorrect error message in catch block:** `"Exception in Databean_getuser"` in a class named `Databean_getter` -- misleading copy-paste error in the diagnostic output string. |

---

## 3. Databean_getuser.java (10,675 lines)

### 3.1 Reading Evidence

| # | Public Method | Line | Has Javadoc |
|---|---|---|---|
| 1 | `clear_variables()` | 464 | Yes (empty `/** */`) |
| 2 | `getP_id()` | 990 | No |
| 3 | `setP_id(ArrayList)` | 994 | No |
| 4 | `getBatt_id()` | 998 | No |
| 5 | `setBatt_id(ArrayList)` | 1002 | No |
| 6 | `getFleet_no()` | 1006 | No |
| 7 | `setFleet_no(ArrayList)` | 1010 | No |
| 8 | `getMail_grp_cd()` | 1727 | No |
| 9-20 | Various mail group getters/setters | 1731-1771 | No |
| 21 | `getSiteHourMessage()` | 2018 | No |
| 22 | `setSiteHourMessage(String)` | 2022 | No |
| 23 | `getBlockedVehList()` | 3439 | No |
| 24 | `setBlockedVehList(ArrayList)` | 3443 | No |
| 25 | `convertToArrayString(Object[])` | 3447 | No |
| 26 | `gettest()` | 4106 | No |
| 27 | `Query_Current_User()` | 5383 | No |
| 28 | `isTechLockoutSupportFw()` | 5634 | No |
| 29-48 | Various VOR/danger tag getters/setters | 5638-5683 | No |
| 49 | `getFull_lockout_enabled()` | 5850 | No |
| 50 | `getFull_lockout_timeout()` | 5854 | No |
| 51 | `getFms_Vehicle_DATA_LOW_UTIL()` | 5858 | No |
| 52 | `setParam_Module(String)` | 5914 | No |
| 53-62 | Various parameter getters/setters | 5921-5954 | No |
| 63 | `getUser_Form_Menu_CD()` | 5963 | No |
| 64-69 | User form menu getters | 5964-5969 | No |
| 70 | `Query_User_Form_Menu()` | 5971 | No |
| 71 | `Query_Permits()` | 6014 | No |
| 72 | `QueryUnlkSettings()` | 6026 | No |
| 73 | `getPermits_Form_Cd()` | 6037 | No |
| 74 | `init()` | 7880 | No |
| 75 | `QuerySFTPSettings()` | 9018 | No |
| -- | ~200 additional public getter/setter methods | 9091-10675 | No |

**Class declaration (line 28):** `public class Databean_getuser` -- No class-level Javadoc.

This file has approximately 250+ public methods. The only Javadoc found is an empty `/** */` block before `clear_variables()` at line 461.

### 3.2 Findings

| ID | Severity | Line(s) | Description |
|----|----------|---------|-------------|
| DGU-DOC-01 | MEDIUM | 28 | **Missing class Javadoc.** `Databean_getuser` is the largest file in the package (~10,675 lines) with no class-level documentation. |
| DGU-DOC-02 | HIGH | 461-464 | **Empty/misleading Javadoc.** The sole Javadoc comment `/** */` on `clear_variables()` contains no description, no `@param`, no `@throws`. The inline comment after the signature (`// Clears all the ArrayLists to avoid previous junk data`) provides more information but is not in the Javadoc block itself. |
| DGU-DOC-03 | MEDIUM | 7880 | **Missing Javadoc on `init()`.** This is a critical lifecycle method that sets up database connections and dispatches based on operation codes. No documentation of expected configuration, valid op_codes, or side effects. |
| DGU-DOC-04 | MEDIUM | 5383 | **Missing Javadoc on `Query_Current_User()`.** Complex SQL query method that populates user state. |
| DGU-DOC-05 | MEDIUM | 5971, 6014, 6026, 9018 | **Missing Javadoc on public data-access methods** (`Query_User_Form_Menu`, `Query_Permits`, `QueryUnlkSettings`, `QuerySFTPSettings`). |
| DGU-DOC-06 | MEDIUM | 3447 | **Missing Javadoc on `convertToArrayString(Object[])`.** A static utility method with no documented contract. |
| DGU-DOC-07 | LOW | various | **~250 public getter/setter methods lack Javadoc.** All are simple one-liner accessors. |

---

## 4. Databean_user.java (45 lines)

### 4.1 Reading Evidence

**Class declaration (line 29):** `public class Databean_user` -- No class-level Javadoc.

The class has no public methods beyond the implicit default constructor. It declares private fields (`conn`, `stmt`, `stmt1`, `stmt2`, `rset`, `rset1`, `rset2`, `methodName`, `query`, `queryString`) but the class body is effectively empty -- no methods at all.

### 4.2 Findings

| ID | Severity | Line(s) | Description |
|----|----------|---------|-------------|
| DU-DOC-01 | LOW | 29 | **Missing class Javadoc.** `Databean_user` appears to be an empty/unused shell class (45 lines, no methods). No documentation explains its purpose or whether it is intentionally empty. |
| DU-DOC-02 | INFO | 24 | Inline comment `// Added by Leslie 11-07-2014` used instead of `@author` tag. |

---

## 5. FirmwareverBean.java (255 lines)

### 5.1 Reading Evidence

| # | Public Method | Line | Has Javadoc |
|---|---|---|---|
| 1 | `getVeh_id()` | 14 | No |
| 2 | `setVeh_id(String)` | 18 | No |
| 3 | `getGmtp_id()` | 22 | No |
| 4 | `setGmtp_id(String)` | 26 | No |
| 5 | `getFirm_vers()` | 30 | No |
| 6 | `setFirm_vers(String)` | 34 | No |
| 7 | `setCurr_ver(String version)` | 38 | No |
| 8 | `setCurr_ver_edit(String version)` | 51 | No |
| 9 | `setCurr_ver()` | 56 | No |
| 10 | `getRep_time()` | 61 | No |
| 11 | `setRep_time(String)` | 65 | No |
| 12 | `getHire_no()` | 69 | No |
| 13 | `setHire_no(String)` | 73 | No |
| 14 | `getType()` | 77 | No |
| 15 | `setType(String)` | 81 | No |
| 16 | `getCurr_ver()` | 85 | No |
| 17 | `getType(String version)` | 211 | No |
| 18 | `getMk3dbg()` | 245 | No |
| 19 | `setMk3dbg(String)` | 249 | No |

**Class declaration (line 3):** `public class FirmwareverBean` -- No class-level Javadoc.

### 5.2 Findings

| ID | Severity | Line(s) | Description |
|----|----------|---------|-------------|
| FVB-DOC-01 | MEDIUM | 3 | **Missing class Javadoc.** `FirmwareverBean` is a data bean for firmware version conversion (32-bit and 64-bit hex parsing) with no class documentation. |
| FVB-DOC-02 | MEDIUM | 38 | **Missing Javadoc on `setCurr_ver(String version)`.** This is not a simple setter -- it contains business logic that parses hex firmware versions via `convert64bit`/`convert32bit` based on string length. The contract is non-obvious and undocumented. |
| FVB-DOC-03 | MEDIUM | 211 | **Missing Javadoc on `getType(String version)`.** This overloaded method accepts a hex version string and returns a parsed type code. Its behavior (hex parsing, substring fallback on `NumberFormatException`) is complex and undocumented. |
| FVB-DOC-04 | LOW | 51, 56 | **Missing Javadoc on `setCurr_ver_edit(String)` and `setCurr_ver()` (no-arg).** These are alternate setters that bypass parsing logic; the distinction from `setCurr_ver(String)` is undocumented. |
| FVB-DOC-05 | LOW | 14-85, 245-251 | **13 simple getter/setter methods lack Javadoc.** Standard bean accessors. |

---

## 6. Frm_saveuser.java (10,930 lines)

### 6.1 Reading Evidence

| # | Public Method | Line | Has Javadoc |
|---|---|---|---|
| 1 | `doPost(HttpServletRequest, HttpServletResponse)` | 54 | No |
| 2 | `clearVectors()` | 449 | No |
| 3 | `isValidEmailAddress(String email)` | 5199 | No |

**Class declaration (line 35):** `public class Frm_saveuser extends HttpServlet implements SingleThreadModel` -- No class-level Javadoc.

The class has only 3 public methods. The `doPost` method (lines 54-447, ~393 lines) is the primary servlet entry point that dispatches to ~70 private `save_*` methods based on `op_code`. All remaining ~70 methods (e.g., `save_group`, `save_division`, `save_department`, `save_new_vehicle`, etc.) are private.

### 6.2 Findings

| ID | Severity | Line(s) | Description |
|----|----------|---------|-------------|
| FSU-DOC-01 | MEDIUM | 35 | **Missing class Javadoc.** `Frm_saveuser` is the largest servlet in the package (~10,930 lines) implementing `SingleThreadModel`. No documentation of its purpose, the URL it maps to, or the `op_code` values it handles. |
| FSU-DOC-02 | MEDIUM | 54 | **Missing Javadoc on `doPost(HttpServletRequest, HttpServletResponse)`.** This 393-line method dispatches to ~70 different save operations. No `@param`/`@throws` documentation, no listing of valid `op_code` parameter values. |
| FSU-DOC-03 | MEDIUM | 5199 | **Missing Javadoc on `isValidEmailAddress(String email)`.** A utility method that validates email via regex. No `@param`/`@return` documentation. |
| FSU-DOC-04 | LOW | 449 | **Missing Javadoc on `clearVectors()`.** Method body is empty -- no documentation on why it exists or whether it is intentionally a no-op. |

---

## 7. Frm_upload.java (162 lines)

### 7.1 Reading Evidence

| # | Public Method | Line | Has Javadoc |
|---|---|---|---|
| 1 | `init()` | 46 | No |
| 2 | `doPost(HttpServletRequest, HttpServletResponse)` | 69 | No |
| 3 | `clearVectors()` | 102 | No |

**Class declaration (line 26):** `public class Frm_upload extends HttpServlet` -- No class-level Javadoc.

### 7.2 Findings

| ID | Severity | Line(s) | Description |
|----|----------|---------|-------------|
| FU-DOC-01 | MEDIUM | 26 | **Missing class Javadoc.** `Frm_upload` is a file-upload servlet with no class documentation describing what it uploads, security considerations, or file-size limits. |
| FU-DOC-02 | MEDIUM | 46 | **Missing Javadoc on `init()`.** Servlet lifecycle method that establishes database connections. No `@throws` documentation. |
| FU-DOC-03 | MEDIUM | 69 | **Missing Javadoc on `doPost(HttpServletRequest, HttpServletResponse)`.** Handles multipart file upload and database operations. No `@param`/`@throws` documentation. |
| FU-DOC-04 | LOW | 102 | **Missing Javadoc on `clearVectors()`.** Empty method body with no documentation. |

---

## Summary

### Findings by Severity

| Severity | Count |
|----------|-------|
| HIGH | 1 |
| MEDIUM | 26 |
| LOW | 10 |
| INFO | 4 |
| **Total** | **41** |

### Key Observations

1. **Zero meaningful Javadoc across all 7 files.** The only Javadoc comment found in the entire package is an empty `/** */` block in `Databean_getuser.java` (line 461), which provides no useful information (rated HIGH for being misleading).

2. **No class-level documentation on any file.** All 7 classes lack class-level Javadoc. For the three large data-access beans (`Databean_customer`, `Databean_getter`, `Databean_getuser`) and two servlets (`Frm_saveuser`, `Frm_upload`), this is especially problematic as they contain complex multi-thousand-line business logic.

3. **Critical dispatcher methods undocumented.** The `query(String op_code)` methods in `Databean_customer` (line 331), `Databean_getter` (line 474), and the `init()` method in `Databean_getuser` (line 7880) are the primary entry points that dispatch to dozens of private methods based on string op_codes. None document the valid values or expected state.

4. **Approximately 500+ public methods across the package lack any Javadoc.** The vast majority are simple getters/setters (rated LOW), but approximately 40+ are complex SQL-executing or business-logic methods (rated MEDIUM).

5. **No `@param`, `@return`, or `@throws` tags found anywhere in the package.** This is a complete absence of structured API documentation.

6. **TODO comments.** Three `// TODO Auto-generated catch block` comments found in `Databean_getter.java` (lines 4071, 4080, 4089) indicating unfinished error handling in empty catch blocks.

7. **No FIXME, HACK, or XXX comments found** in any of the 7 files.

8. **Misleading error string.** `Databean_getter.java` line 812 prints `"Exception in Databean_getuser"` -- a copy-paste error from a different class name.
