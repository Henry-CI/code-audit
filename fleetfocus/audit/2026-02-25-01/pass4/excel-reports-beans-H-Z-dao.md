# Pass 4 -- Code Quality Audit: excel/reports/beans (H-Z) + dao
**Agent:** A14
**Date:** 2026-02-25
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Scope:** 15 files (13 beans under `beans/`, 2 DAOs under `dao/`)

---

## 1. File Inventory

| # | File | Path (relative to `WEB-INF/src/com/torrent/surat/fms6/excel/reports/`) | Lines |
|---|------|------------------------------------------------------------------------|-------|
| 1 | HireDehireReportBean.java | beans/ | 63 |
| 2 | ImpactReportBean.java | beans/ | 120 |
| 3 | KeyHourUtilBean.java | beans/ | 171 |
| 4 | OperationalStatusReportItemResultBean.java | beans/ | 63 |
| 5 | OperationalStatusReportResultBean.java | beans/ | 17 |
| 6 | PreOpCheckFailReportBean.java | beans/ | 93 |
| 7 | PreOpCheckReportBean.java | beans/ | 95 |
| 8 | SeatHourUtilBean.java | beans/ | 171 |
| 9 | ServMaintenanceReportBean.java | beans/ | 142 |
| 10 | SuperMasterAuthReportBean.java | beans/ | 21 |
| 11 | UnitUnlockReportBean.java | beans/ | 79 |
| 12 | UtilWowReportBean.java | beans/ | 75 |
| 13 | UtilisationReportBean.java | beans/ | 169 |
| 14 | CustomerDAO.java | dao/ | 206 |
| 15 | DriverAccessAbuseDAO.java | dao/ | 65 |

---

## 2. Findings

### F-01 [HIGH] Exact Duplicate Beans -- `PreOpCheckReportBean` and `PreOpCheckFailReportBean`

**Files:**
- `beans/PreOpCheckReportBean.java`
- `beans/PreOpCheckFailReportBean.java`

**Evidence:** The two classes declare identical field sets, identical field types, identical accessor methods, and identical default values. Side-by-side comparison:

`PreOpCheckReportBean` fields (lines 7-18):
```java
ArrayList po_dnm = new ArrayList();
ArrayList po_did = new ArrayList();
ArrayList po_sttm = new ArrayList();
ArrayList po_comp = new ArrayList();
ArrayList po_dur = new ArrayList();
ArrayList po_fail = new ArrayList();
ArrayList po_machine = new ArrayList();
ArrayList po_veh_id = new ArrayList();
ArrayList po_model = new ArrayList();
String tot_dur = "";
ArrayList q_type = new ArrayList();
ArrayList<String> preOpCheckCommentList = new ArrayList<String>();
```

`PreOpCheckFailReportBean` fields (lines 7-18):
```java
ArrayList po_dnm = new ArrayList();
ArrayList po_did = new ArrayList();
ArrayList po_sttm = new ArrayList();
ArrayList po_comp = new ArrayList();
ArrayList po_dur = new ArrayList();
ArrayList po_fail = new ArrayList();
ArrayList po_machine = new ArrayList();
ArrayList po_veh_id = new ArrayList();
ArrayList po_model = new ArrayList();
String tot_dur = "";
ArrayList q_type = new ArrayList();
ArrayList<String> preOpCheckCommentList = new ArrayList<String>();
```

Every field, every getter, every setter is byte-for-byte identical in structure. The only difference is the class name. This is a textbook code duplication. One class should be eliminated and the other reused, or a common base class should be extracted.

---

### F-02 [HIGH] Near-Exact Duplicate Beans -- `KeyHourUtilBean` and `SeatHourUtilBean`

**Files:**
- `beans/KeyHourUtilBean.java` (171 lines)
- `beans/SeatHourUtilBean.java` (171 lines)

**Evidence:** Both classes have exactly 171 lines, identical field declarations, identical field names, identical types, identical getter/setter methods, and identical default initializations. Full field list in both:

```java
ArrayList veh_cd = new ArrayList();
ArrayList veh_nm = new ArrayList();
ArrayList veh_id = new ArrayList();
ArrayList veh_typ_nm1 = new ArrayList();
ArrayList vutil1..vutil8 = new ArrayList();
ArrayList vutilt = new ArrayList();
ArrayList vutilpt= new ArrayList();
String util1..util8;
String utilt;
```

These two classes are 100% structurally identical. They should be consolidated into a single parameterized bean or one should inherit from the other.

---

### F-03 [HIGH] SQL Injection Vulnerability -- `CustomerDAO`

**File:** `dao/CustomerDAO.java`

**Evidence:** All five query methods concatenate user-supplied parameters directly into SQL strings without using `PreparedStatement` or any sanitization:

Line 32 (`getCustomerName`):
```java
String sql = "select \"USER_NAME\" from \"FMS_CUST_MST\" where \"USER_CD\" = " + cust_cd;
```

Line 70 (`getLocationName`):
```java
String sql = "select \"NAME\" from \"FMS_LOC_MST\" where \"LOCATION_CD\" = " + loc_cd;
```

Line 107 (`getDepartmentName`):
```java
String sql = "select \"DEPT_NAME\" from \"FMS_DEPT_MST\" where \"DEPT_CD\" = " + dept_cd;
```

Line 144 (`getModelName`):
```java
String sql = "select \"VEHICLE_TYPE\" from \"FMS_VEHICLE_TYPE_MST\" where \"VEHICLE_TYPE_CD\" = " + model_cd;
```

Line 180-181 (`getFormName`):
```java
String query = "select \"FORM_NAME\"  from "+RuntimeConf.form_table+" where \"FORM_CD\"='"
        + form_cd + "' ";
```

All five methods use `Statement` instead of `PreparedStatement`, enabling SQL injection attacks if any of these code parameters originate from user input.

---

### F-04 [HIGH] Logic Bug -- Wrong Variable Tested in `getFormName`

**File:** `dao/CustomerDAO.java`, lines 177-179

**Evidence:**
```java
String formName = "unknown report";
if (!formName.equalsIgnoreCase("")
        && !formName.equalsIgnoreCase("0")
        && !formName.equalsIgnoreCase("all") && !form_cd.equalsIgnoreCase("")) {
```

The guard condition tests `formName` (which was just set to `"unknown report"`) instead of `form_cd`. The first three sub-conditions (`!formName.equalsIgnoreCase("")`, `!formName.equalsIgnoreCase("0")`, `!formName.equalsIgnoreCase("all")`) will always be `true` since `formName` is `"unknown report"`. This means only the last condition (`!form_cd.equalsIgnoreCase("")`) has any filtering effect. The intent was clearly to validate `form_cd`, not `formName`. Compare with the other four methods in the same class, which correctly validate their input parameter (e.g., `!cust_cd.equalsIgnoreCase("")`).

---

### F-05 [MEDIUM] Dead Fields in `DriverAccessAbuseDAO`

**File:** `dao/DriverAccessAbuseDAO.java`, lines 18-31

**Evidence:** The class declares 13 instance-level `ArrayList` fields:
```java
ArrayList a_driv_cd = new ArrayList();
ArrayList a_driv_nm = new ArrayList();
ArrayList a_driv_id = new ArrayList();
ArrayList a_veh_cd = new ArrayList();
ArrayList a_veh_nm = new ArrayList();
ArrayList a_veh_typ_cd = new ArrayList();
ArrayList a_veh_typ_nm = new ArrayList();
ArrayList a_veh_srno = new ArrayList();
ArrayList a_st_tm = new ArrayList();
ArrayList a_end_tm = new ArrayList();
ArrayList a_date = new ArrayList();
ArrayList<String> a_ol_start_list = new ArrayList();
ArrayList<String> a_ol_end_list = new ArrayList();
```

None of these fields are read or written anywhere in the class. The single method `getAbuseBean()` (line 33) uses local variables and the `Databean_report` object exclusively; it never touches any instance field. All 13 fields are dead code that allocates memory on every DAO instantiation for no purpose.

Furthermore, these 13 fields mirror the fields in `DriverAccessAbuseBean` exactly, suggesting a copy-paste origin where the DAO was meant to populate them but was later refactored to use `Databean_report` delegation without cleaning up the leftover fields.

---

### F-06 [MEDIUM] Duplicate Import Statements

**Files affected:**
- `beans/ServMaintenanceReportBean.java`, lines 3-4:
  ```java
  import java.util.ArrayList;
  import java.util.ArrayList;
  ```
- `beans/UtilisationReportBean.java`, lines 3-4:
  ```java
  import java.util.ArrayList;
  import java.util.ArrayList;
  ```
- `dao/DriverAccessAbuseDAO.java`, lines 7 and 10:
  ```java
  import java.util.ArrayList;
  ...
  import java.util.ArrayList;
  ```
- `beans/DriverAccessAbuseBean.java` (supporting context, not in audit scope), lines 3-4:
  ```java
  import java.util.ArrayList;
  import java.util.ArrayList;
  ```

Each of these files imports `java.util.ArrayList` twice. While this compiles without error, it indicates sloppy maintenance and IDE settings not enforcing import hygiene.

---

### F-07 [MEDIUM] Unused Imports

**File:** `dao/CustomerDAO.java`, line 7:
```java
import java.util.ArrayList;
```
`ArrayList` is never used anywhere in the class. All collections in this DAO are handled via JDBC `ResultSet`.

**File:** `dao/DriverAccessAbuseDAO.java`, lines 8-9:
```java
import java.util.Collections;
import java.util.StringTokenizer;
```
Neither `Collections` nor `StringTokenizer` is referenced anywhere in the class body.

---

### F-08 [MEDIUM] Raw Types -- Pervasive Use of Unparameterized `ArrayList`

**Files affected:** All 13 bean files, plus `DriverAccessAbuseDAO.java`

**Evidence:** Nearly every `ArrayList` declaration across the entire scope uses the raw type `ArrayList` without generics. Examples:

`HireDehireReportBean.java`, lines 6-13:
```java
private ArrayList veh_serial;
private ArrayList veh_gmtp;
private ArrayList veh_hire;
...
```

`KeyHourUtilBean.java`, lines 6-20:
```java
ArrayList veh_cd = new ArrayList();
ArrayList veh_nm = new ArrayList();
...
```

`ImpactReportBean.java`, lines 7-13:
```java
private ArrayList machineId;
private ArrayList vehId;
private ArrayList model;
...
```

Only a handful of fields use generics (e.g., `ArrayList<String> preOpCheckCommentList` in the PreOpCheck beans, `ArrayList<SuperMasterAuthBean>` in SuperMasterAuthReportBean, `List<OperationalStatusReportItemResultBean>` in OperationalStatusReportResultBean). The vast majority are raw, losing type safety and generating compiler warnings.

**Note:** Even `SuperMasterAuthReportBean` line 9 mixes generics declaration on the left with raw constructor on the right:
```java
ArrayList<SuperMasterAuthBean> superMasterAuths = new ArrayList();
```
This produces an unchecked assignment warning.

---

### F-09 [MEDIUM] Package-Private (Default) Field Visibility

**Files affected:** KeyHourUtilBean, SeatHourUtilBean, PreOpCheckReportBean, PreOpCheckFailReportBean, UnitUnlockReportBean, UtilWowReportBean, UtilisationReportBean, ServMaintenanceReportBean (partially), OperationalStatusReportItemResultBean, DriverAccessAbuseDAO

**Evidence:** Fields are declared without any access modifier, making them package-private. For bean classes that provide getter/setter methods, this exposes an uncontrolled access path alongside the accessors:

`KeyHourUtilBean.java`, lines 6-30:
```java
ArrayList veh_cd = new ArrayList();   // package-private
ArrayList veh_nm = new ArrayList();   // package-private
...
String util1;                          // package-private
```

`OperationalStatusReportItemResultBean.java`, lines 5-12:
```java
String equipNo = "";      // package-private
String serialNo = "";     // package-private
...
```

This mixed approach undermines encapsulation. Either all fields should be `private` with getters/setters (as done in `HireDehireReportBean` and `ImpactReportBean`), or the getters/setters should be removed to keep access consistent.

---

### F-10 [MEDIUM] Naming Convention Violations

**Files affected:** Multiple

**Evidence of underscore_case field names (violates Java camelCase convention):**
- `HireDehireReportBean`: `veh_serial`, `veh_gmtp`, `veh_hire`, `hire_time`, `dehire_time`, `cust_name`, `loc_nm`, `dep_nm`
- `KeyHourUtilBean` / `SeatHourUtilBean`: `veh_cd`, `veh_nm`, `veh_id`, `veh_typ_nm1`
- `PreOpCheckReportBean` / `PreOpCheckFailReportBean`: `po_dnm`, `po_did`, `po_sttm`, `po_comp`, `po_dur`, `po_fail`, `po_machine`, `po_veh_id`, `po_model`, `tot_dur`, `q_type`
- `ServMaintenanceReportBean`: `sm_service_from`, `sm_ser_st`, `sm_ser_ed`, `vmachine_cd`, `vmachine_nm`, `vs_no`, `sm_ser_ed2`, `service_id`, `sm_hour_meter`, `service_hour`, `t_sm_hm_s`
- `UnitUnlockReportBean`: `vunit_name`, `vunit_veh_id`, `vunit_loreason`, etc.
- `UtilisationReportBean`: `group_cd`, `group_nm`, `user_cd`, `user_nm`, `location_cd`, etc.
- `UtilWowReportBean`: `get_user`, `get_loc`, `get_dep`, `get_mod`, `form_nm`
- `CustomerDAO`: method parameters `cust_cd`, `loc_cd`, `dept_cd`, `model_cd`
- `DriverAccessAbuseDAO`: `a_driv_cd`, `a_driv_nm`, etc.

These names mirror database column names, leaking the database schema naming convention into Java code.

**Evidence of uppercase-starting field names (violates Java convention that fields start lowercase):**
- `ImpactReportBean`, line 16: `private ArrayList Vimp_img;`
- `ImpactReportBean`, line 18: `private ArrayList Vtmp_imp_data;`

**Evidence of `get` prefix on data fields (reads confusingly like accessor methods):**
- `UtilWowReportBean`: `get_user`, `get_loc`, `get_dep`, `get_mod` -- these are stored data, not accessor methods, but the `get_` prefix makes them look like method names. The generated accessors become `getGet_user()`, `getGet_loc()`, etc.
- `UtilisationReportBean`: `get_gp`, `get_user_nm` -- same issue producing `getGet_gp()`, `getGet_user_nm()`

---

### F-11 [MEDIUM] Error Handling -- `catch` Blocks Swallow Exceptions

**File:** `dao/CustomerDAO.java`

**Evidence:** All five methods use the same flawed pattern. Example from `getCustomerName` (lines 41-44):
```java
}catch(Exception e)
{
    e.printStackTrace();
    e.getMessage();
}
```

Problems:
1. `e.getMessage()` on line 44 (and equivalents at lines 81, 118, 155, 193) is a standalone expression that returns a String but the return value is discarded. It has no effect whatsoever.
2. `e.printStackTrace()` sends output to stderr which is typically lost in Tomcat deployments with no monitoring of catalina.out.
3. The broad `catch(Exception e)` silently swallows the exception, meaning the method returns the default value (`"All"` or `"unknown report"`) without the caller knowing a database error occurred.
4. The method signature declares `throws SQLException` but the catch block intercepts `Exception` (which includes `SQLException`), so the declared thrown exception is effectively unreachable by the caller except from the `finally` block's own `rs.close()` / `stmt.close()` calls.

---

### F-12 [MEDIUM] Resource Leak Risk in `finally` Blocks -- `CustomerDAO`

**File:** `dao/CustomerDAO.java`

**Evidence:** The `finally` block in all five methods follows this pattern (example from lines 46-50):
```java
finally{
    if(null != rs) {rs.close();}
    if(null != stmt) {stmt.close();}
    DBUtil.closeConnection(conn);
}
```

If `rs.close()` throws a `SQLException`, then `stmt.close()` and `DBUtil.closeConnection(conn)` are never reached, causing a connection leak. Each close operation should be wrapped in its own try-catch, or a utility method / try-with-resources should be used.

---

### F-13 [LOW] Unnecessary `ResultSet.TYPE_SCROLL_SENSITIVE` Cursor in `CustomerDAO`

**File:** `dao/CustomerDAO.java`, lines 28, 66, 103, 140, 174

**Evidence:**
```java
stmt=conn.createStatement(ResultSet.TYPE_SCROLL_SENSITIVE, ResultSet.CONCUR_READ_ONLY);
```

All five methods iterate forward-only through results using `while(rs.next())` or `if(rs.next())`. None uses scroll operations (`previous()`, `absolute()`, `relative()`). Using `TYPE_SCROLL_SENSITIVE` adds overhead by requesting the database driver to maintain a scrollable, change-sensitive cursor. The default `TYPE_FORWARD_ONLY` would be correct and more efficient.

---

### F-14 [LOW] Excessive Trailing Blank Lines

**Files:**
- `ImpactReportBean.java`, lines 115-119: Five consecutive blank lines before the closing brace.
- `UtilWowReportBean.java`, lines 72-73: Two trailing blank lines before closing brace.
- `UtilisationReportBean.java`, lines 166-167: Two trailing blank lines before closing brace.

---

### F-15 [LOW] `Serializable` Not Implemented on Bean Classes

**Files affected:** All 13 beans

**Evidence:** None of the bean classes implement `java.io.Serializable`. If these beans are stored in HTTP sessions (common in JSP/Tomcat applications), session serialization and clustering will fail silently or throw errors.

---

### F-16 [LOW] No `equals()` / `hashCode()` / `toString()` Overrides

**Files affected:** All 13 beans

**Evidence:** No bean class provides `equals()`, `hashCode()`, or `toString()` implementations. This makes debugging difficult (default `Object.toString()` produces unhelpful output like `HireDehireReportBean@1a2b3c`) and can cause subtle bugs if beans are ever placed in collections that rely on equality semantics.

---

### F-17 [LOW] Inconsistent Encapsulation Style -- `ServMaintenanceReportBean`

**File:** `beans/ServMaintenanceReportBean.java`

**Evidence:** The class mixes package-private and private fields:

Lines 9-15 (package-private):
```java
ArrayList sm_service_from = new ArrayList();
ArrayList sm_ser_st = new ArrayList();
ArrayList sm_ser_ed = new ArrayList();
ArrayList vmachine_cd = new ArrayList();
ArrayList vmachine_nm = new ArrayList();
ArrayList vs_no = new ArrayList();
```

Lines 16-26 (private):
```java
private ArrayList machineName = new ArrayList();
private ArrayList sm_ser_ed2 = new ArrayList();
private ArrayList lastServDateList = new ArrayList();
private ArrayList nextServDate = new ArrayList();
...
```

Line 47 (package-private):
```java
String t_sm_hm_s = "";
```

This suggests the private fields were added later and the original fields were never updated to match.

---

### F-18 [LOW] Null Fields vs Initialized Fields -- Inconsistent Defaults

**Files:**
- `HireDehireReportBean.java`: All ArrayList fields are `null` (no initializer). Example:
  ```java
  private ArrayList veh_serial;   // null by default
  ```
- `ImpactReportBean.java`: Mixed -- some fields are `null` (lines 7-13: `machineId`, `vehId`, etc.), others are initialized (lines 17-20: `meterDetails = new ArrayList()`, etc.)
- All other beans: Fields are initialized with `new ArrayList()`.

If a getter is called before a setter on the null-default beans (`HireDehireReportBean`, partially `ImpactReportBean`), a `NullPointerException` will occur. The initialized beans return an empty list, which is safer.

---

### F-19 [LOW] Redundant Null-Check in `OperationalStatusReportResultBean`

**File:** `beans/OperationalStatusReportResultBean.java`, line 11

**Evidence:**
```java
List<OperationalStatusReportItemResultBean> itemResultBeanList = new ArrayList<OperationalStatusReportItemResultBean>();

public List<OperationalStatusReportItemResultBean> getItemResultBeanList() {
    return this.itemResultBeanList == null ? new ArrayList<OperationalStatusReportItemResultBean>() : this.itemResultBeanList;
}
```

The field is initialized to `new ArrayList<>()` on line 8, and the setter (line 13) accepts any list without null-checking. The null check in the getter is defensive but creates inconsistency: if the setter is called with `null`, the getter creates a new transient list that is not stored back, so subsequent calls create different list instances. This is a latent behavioral bug.

---

## 3. Summary Table

| ID | Severity | Category | File(s) | Short Description |
|----|----------|----------|---------|-------------------|
| F-01 | HIGH | Duplicate Code | PreOpCheckReportBean, PreOpCheckFailReportBean | 100% identical structure; two separate classes |
| F-02 | HIGH | Duplicate Code | KeyHourUtilBean, SeatHourUtilBean | 100% identical structure; two separate classes |
| F-03 | HIGH | Security | CustomerDAO | SQL injection via string concatenation in all 5 methods |
| F-04 | HIGH | Logic Bug | CustomerDAO.getFormName() | Guard tests `formName` instead of `form_cd`; first 3 conditions always true |
| F-05 | MEDIUM | Dead Code | DriverAccessAbuseDAO | 13 instance-level ArrayList fields never read or written |
| F-06 | MEDIUM | Unused Import | ServMaintenanceReportBean, UtilisationReportBean, DriverAccessAbuseDAO | Duplicate `import java.util.ArrayList` |
| F-07 | MEDIUM | Unused Import | CustomerDAO, DriverAccessAbuseDAO | Imports for ArrayList, Collections, StringTokenizer never used |
| F-08 | MEDIUM | Type Safety | All 13 beans + DriverAccessAbuseDAO | Raw `ArrayList` without generics throughout |
| F-09 | MEDIUM | Encapsulation | 8 bean files + DriverAccessAbuseDAO | Package-private fields alongside getter/setter methods |
| F-10 | MEDIUM | Naming | Nearly all files | Underscore_case fields, uppercase-starting fields, `get_` data prefixes |
| F-11 | MEDIUM | Error Handling | CustomerDAO | Exceptions swallowed; no-op `e.getMessage()`; broad catch |
| F-12 | MEDIUM | Resource Leak | CustomerDAO | `finally` block close chain can leak on intermediate exception |
| F-13 | LOW | Performance | CustomerDAO | Unnecessary scrollable cursor in all 5 methods |
| F-14 | LOW | Style | ImpactReportBean, UtilWowReportBean, UtilisationReportBean | Excessive trailing blank lines |
| F-15 | LOW | Best Practice | All 13 beans | No `Serializable` implementation |
| F-16 | LOW | Best Practice | All 13 beans | No `equals`/`hashCode`/`toString` |
| F-17 | LOW | Style | ServMaintenanceReportBean | Mixed private / package-private field visibility |
| F-18 | LOW | Correctness | HireDehireReportBean, ImpactReportBean | Null-default fields risk NPE vs initialized peers |
| F-19 | LOW | Correctness | OperationalStatusReportResultBean | Null-guard in getter creates transient list not stored back |

---

## 4. Metrics

- **Files audited:** 15
- **Total findings:** 19
- **HIGH:** 4
- **MEDIUM:** 8
- **LOW:** 7
- **Lines of code audited:** ~1,548

---

*End of Pass 4 audit -- Report only, no fixes applied.*
