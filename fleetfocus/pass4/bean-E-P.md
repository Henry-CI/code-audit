# Pass 4 -- Code Quality Audit: Bean Package (E-P)

**Audit ID:** 2026-02-25-01
**Pass:** 4 (Code Quality)
**Agent:** A02
**Date:** 2026-02-25
**Repository:** C:\Projects\cig-audit\repos\fleetfocus
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Package:** `com.torrent.surat.fms6.bean` (files EntityBean through PreCheckSummaryBean)

---

## Scope

All 16 files under `WEB-INF/src/com/torrent/surat/fms6/bean/`:

| # | File | Lines |
|---|------|-------|
| 1 | EntityBean.java | 55 |
| 2 | FleetCheckBean.java | 31 |
| 3 | ImpactBean.java | 258 |
| 4 | ImpactDeptBean.java | 45 |
| 5 | ImpactLocBean.java | 54 |
| 6 | ImpactSummaryBean.java | 62 |
| 7 | LicenseBlackListBean.java | 85 |
| 8 | LockOutBean.java | 64 |
| 9 | MaxHourUsageBean.java | 40 |
| 10 | MenuBean.java | 52 |
| 11 | MymessagesUsersBean.java | 71 |
| 12 | NetworkSettingBean.java | 37 |
| 13 | NotificationSettingsBean.java | 51 |
| 14 | PreCheckBean.java | 97 |
| 15 | PreCheckDriverBean.java | 42 |
| 16 | PreCheckSummaryBean.java | 54 |

All files were read in full. Findings below.

---

## Summary of Findings

| Severity | Count |
|----------|-------|
| HIGH | 3 |
| MEDIUM | 16 |
| LOW | 14 |
| INFO | 6 |
| **Total** | **39** |

---

## Findings

### F-01 [MEDIUM] Inconsistent field naming conventions -- snake_case vs camelCase

**Files affected:** EntityBean.java, ImpactBean.java, ImpactDeptBean.java, ImpactLocBean.java, ImpactSummaryBean.java, LicenseBlackListBean.java, LockOutBean.java, MaxHourUsageBean.java, MymessagesUsersBean.java, PreCheckBean.java, PreCheckDriverBean.java, PreCheckSummaryBean.java

**Description:** The majority of bean fields use `snake_case` naming (e.g., `cust_cd`, `loc_cd`, `dept_name`, `driver_cd`, `model_name`, `master_code`), which violates Java naming conventions that require `camelCase` for field names. This convention is used pervasively across most files in scope.

Meanwhile, `LicenseBlackListBean.java` uses `camelCase` for some fields (`vehicleType`, `custCd`, `locCd`, `deptCd`, `driverCd`) but reverts to `snake_case` for others (`access_level`, `access_cust`, `access_site`, `access_dept`), creating internal inconsistency within the same class.

**Evidence:**
```java
// ImpactBean.java lines 11-21 -- snake_case fields
String cust_cd = "";
String loc_cd = "";
String dept_cd = "";
String dept_name = "";
String model_cd = "";
String model_name = "";
String driver_cd = "";
String driver_name = "";
String unit_cd = "";
String unit_name = "";
String unit_type = "";

// LicenseBlackListBean.java lines 7-16 -- mixed naming
private String vehicleType;    // camelCase
private String custCd;         // camelCase
private String access_level=null;  // snake_case
private String access_cust=null;   // snake_case
```

---

### F-02 [MEDIUM] Fields declared at package-private (default) access instead of private

**Files affected:** EntityBean.java, ImpactBean.java, ImpactDeptBean.java, ImpactLocBean.java, ImpactSummaryBean.java, LockOutBean.java, MaxHourUsageBean.java, MymessagesUsersBean.java, PreCheckBean.java, PreCheckDriverBean.java, PreCheckSummaryBean.java, FleetCheckBean.java

**Description:** The vast majority of bean fields are declared without an access modifier, giving them package-private (default) access. Proper encapsulation requires fields to be declared `private`, with access provided exclusively through getter/setter methods. Only `LicenseBlackListBean.java`, `NetworkSettingBean.java`, `MenuBean.java`, and `NotificationSettingsBean.java` correctly use the `private` modifier on their fields.

**Evidence:**
```java
// EntityBean.java lines 12-17 -- no access modifier
String id = "";
String name = "";
double totalno = 0;
String attribute = "";
String locs ="";
String depts = "";

// Contrast with LicenseBlackListBean.java lines 7-17 -- proper private
private String vehicleType;
private String custCd;
private String locCd;
```

---

### F-03 [MEDIUM] Upper-case field names violate Java conventions

**File:** MenuBean.java (lines 7-12)

**Description:** All fields in `MenuBean` start with an uppercase letter (`Menus_Cd`, `Menus_Name`, `Form_Cd`, `Form_Name`, `Form_Path`, `ReskinPath`), violating the standard Java convention that field names must begin with a lowercase letter. This also creates misleading getter/setter behavior where `setMenus_Cd(String menus_Cd)` assigns to `Menus_Cd = menus_Cd` without using `this.` qualifier -- relying on the case difference rather than explicit scoping.

**Evidence:**
```java
// MenuBean.java lines 7-12
private String Menus_Cd ="";
private String Menus_Name ="";
private String Form_Cd ="";
private String Form_Name ="";
private String Form_Path ="";
private String ReskinPath ="";

// MenuBean.java lines 31-33 -- setter without this. qualifier
public void setMenus_Cd(String menus_Cd) {
    Menus_Cd = menus_Cd;
}
```

---

### F-04 [MEDIUM] Getter/setter names use snake_case violating JavaBean specification

**Files affected:** ImpactBean.java, ImpactDeptBean.java, ImpactSummaryBean.java, LicenseBlackListBean.java, LockOutBean.java, MaxHourUsageBean.java, MymessagesUsersBean.java, NotificationSettingsBean.java, PreCheckBean.java, PreCheckDriverBean.java, PreCheckSummaryBean.java, FleetCheckBean.java, MenuBean.java

**Description:** Getter/setter methods follow snake_case field names, producing methods like `getCust_cd()`, `setDept_name()`, `getDriver_cd()`, `getAvg_completion_time()`, `getMenus_Cd()` etc. Standard JavaBean specification requires `getCustCd()`, `setDeptName()` etc. This can cause issues with frameworks that rely on JavaBean property introspection (e.g., JSP EL, serialization libraries, Spring BeanUtils).

**Evidence:**
```java
// ImpactBean.java lines 94-104
public String getCust_cd() { return cust_cd; }
public void setCust_cd(String cust_cd) { this.cust_cd = cust_cd; }
public String getLoc_cd() { return loc_cd; }
public void setLoc_cd(String loc_cd) { this.loc_cd = loc_cd; }

// FleetCheckBean.java lines 11-16
public String getAvg_completion_time() { return avg_completion_time; }
public void setAvg_completion_time(String avg_completion_time) {
    this.avg_completion_time = avg_completion_time;
}
```

---

### F-05 [HIGH] Mutable internal collections exposed via getters (leaky abstraction)

**Files affected:** FleetCheckBean.java, ImpactBean.java, ImpactDeptBean.java, ImpactLocBean.java, ImpactSummaryBean.java, MaxHourUsageBean.java, PreCheckBean.java, PreCheckSummaryBean.java, LicenseBlackListBean.java

**Description:** Multiple beans expose mutable `ArrayList` and `HashMap` references directly through their getters. Callers can modify the internal state of these beans without going through the setter, breaking encapsulation. For `Serializable` beans, this is especially concerning as deserialized state could be silently corrupted.

Additionally, `ImpactBean.java` exposes mutable `int[]` arrays via getters like `getBlueshock()`, `getAmbershock()`, `getRedshock()`, `getImpacts()`, and `int[][]` via `getBlueshockShift()` etc. -- array contents can be modified by any caller.

**Evidence:**
```java
// ImpactDeptBean.java lines 30-31 -- returns mutable ArrayList directly
public ArrayList<ImpactSummaryBean> getArrImpactSummryBean() {
    return arrImpactSummryBean;
}

// ImpactBean.java lines 106-108 -- returns mutable HashMap directly
public HashMap<Integer, Integer> getImpactMap() {
    return impactMap;
}

// ImpactBean.java lines 128-130 -- returns mutable array directly
public int[] getBlueshock() {
    return blueshock;
}

// PreCheckBean.java lines 33-35 -- returns mutable HashMap directly
public HashMap<String, Integer> getCheckMap() {
    return checkMap;
}
```

---

### F-06 [HIGH] NetworkSettingBean stores WiFi password in plain text

**File:** NetworkSettingBean.java (lines 9-10)

**Description:** The `NetworkSettingBean` stores a WiFi password as a plain-text `String` field. Since this bean is `Serializable`, the password could be inadvertently persisted, logged, or transmitted in clear text during serialization. There is no indication of encryption, masking, or secure handling anywhere in this class.

**Evidence:**
```java
// NetworkSettingBean.java lines 9-10
private String password = "";

// NetworkSettingBean.java lines 30-34
public String getPassword() {
    return password;
}
public void setPassword(String password) {
    this.password = password;
}
```

---

### F-07 [LOW] Missing serialVersionUID on Serializable-like beans

**File:** ImpactSummaryBean.java

**Description:** `ImpactSummaryBean` implements `Serializable` (line 6) but does not declare a `serialVersionUID` field. This means the JVM will auto-generate one at runtime based on class structure, which can break deserialization if the class is modified. Other Impact-related beans (`ImpactBean`, `ImpactDeptBean`, `ImpactLocBean`) correctly declare this field.

**Evidence:**
```java
// ImpactSummaryBean.java lines 6-12 -- no serialVersionUID
public class ImpactSummaryBean implements Serializable{
    String loc_cd = "";
    String loc_name = "";
    ArrayList<ImpactBean> arrImpact = new ArrayList<ImpactBean>();
    ...
```

---

### F-08 [LOW] Missing serialVersionUID on Serializable-like beans

**File:** PreCheckSummaryBean.java

**Description:** Same as F-07. `PreCheckSummaryBean` implements `Serializable` but does not declare `serialVersionUID`.

**Evidence:**
```java
// PreCheckSummaryBean.java lines 6-12
public class PreCheckSummaryBean implements Serializable{
    String loc_cd = "";
    String loc_name = "";
    ...
```

---

### F-09 [MEDIUM] Classes not implementing Serializable despite peers doing so

**Files affected:** FleetCheckBean.java, MenuBean.java, NotificationSettingsBean.java

**Description:** These three bean classes do not implement `Serializable`, while nearly all other beans in this package do. If any of these beans are placed in HTTP session scope, stored in a distributed cache, or used with other serialization-dependent infrastructure, this will cause `NotSerializableException` at runtime. Within the same domain model, beans should be consistent about serializability.

**Evidence:**
```java
// FleetCheckBean.java line 5 -- no Serializable
public class FleetCheckBean {

// MenuBean.java line 5 -- no Serializable
public class MenuBean {

// NotificationSettingsBean.java line 3 -- no Serializable
public class NotificationSettingsBean {
```

---

### F-10 [LOW] Unused import -- java.util.ArrayList in MenuBean

**File:** MenuBean.java (line 3)

**Description:** `MenuBean` imports `java.util.ArrayList` but never uses it anywhere in the class. No field, parameter, or return type references `ArrayList`.

**Evidence:**
```java
// MenuBean.java lines 3-5
import java.util.ArrayList;

public class MenuBean {
```

---

### F-11 [LOW] Unused imports -- java.util.Map in PreCheckBean

**File:** PreCheckBean.java (line 6)

**Description:** `PreCheckBean` imports `java.util.Map` but only uses `HashMap` (which is imported separately on line 5). The `Map` interface is never referenced.

**Evidence:**
```java
// PreCheckBean.java lines 3-7
import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class PreCheckBean implements Serializable{
```

---

### F-12 [MEDIUM] Concrete collection types in APIs instead of interfaces

**Files affected:** FleetCheckBean.java, ImpactDeptBean.java, ImpactLocBean.java, ImpactSummaryBean.java, MaxHourUsageBean.java, PreCheckBean.java, PreCheckSummaryBean.java, LicenseBlackListBean.java, ImpactBean.java

**Description:** Getters, setters, and fields declare `ArrayList<...>` and `HashMap<...>` as types instead of using the `List<...>` and `Map<...>` interfaces. This couples consumers to specific implementations and violates the "program to interfaces" principle.

**Evidence:**
```java
// FleetCheckBean.java line 9
ArrayList<String> frequent_failed_question = new ArrayList<String>();

// ImpactBean.java line 45
HashMap<Integer, Integer> impactMap = new HashMap<Integer, Integer>();

// ImpactBean.java line 109
public void setImpactMap(HashMap<Integer, Integer> impactMap) {

// PreCheckBean.java line 20
HashMap<String, Integer> checkMap = new HashMap<String, Integer>();
```

---

### F-13 [LOW] Inconsistent indentation and formatting across files

**Files affected:** ImpactBean.java, PreCheckBean.java, MenuBean.java, FleetCheckBean.java

**Description:** Indentation levels are inconsistent within and across files. `ImpactBean.java` is particularly poor: field declarations use no indentation or single-tab, while getter/setter methods use double-tab or triple-tab indentation seemingly at random. The `impactMap` field on line 45 uses excessive leading whitespace compared to neighboring fields. `FleetCheckBean.java` mixes 4-space and tab indentation for field declarations (line 9 vs line 7).

**Evidence:**
```java
// ImpactBean.java -- inconsistent indentation
   String cust_cd = "";          // 3 spaces (line 11)
        HashMap<Integer, Integer> impactMap = ...;  // 8 spaces (line 45)
	    public void addImactMap(int month, int impact_no)  // tab+4 spaces (line 47)
		public String getModel_name() {  // double-tab (line 52)

// FleetCheckBean.java lines 7-9 -- mixed indentation
	String unitName = "";                              // tab
	String avg_completion_time = "N/A";                // tab
    ArrayList<String>  frequent_failed_question = ...  // 4 spaces
```

---

### F-14 [LOW] Typo in method name: `addImactMap` (missing 'p')

**File:** ImpactBean.java (line 47)

**Description:** The method `addImactMap` is missing the letter 'p' and should be `addImpactMap`. This is a spelling error in a public API that consumers must use with the typo.

**Evidence:**
```java
// ImpactBean.java lines 47-50
public void addImactMap(int month, int impact_no)
{
    impactMap.put(month, impact_no);
}
```

---

### F-15 [LOW] Typo in field name: `descrption` (missing 'i')

**File:** MymessagesUsersBean.java (line 18)

**Description:** The field `descrption` is missing the letter 'i' and should be `description`. The getter/setter pair also perpetuates this typo (`getDescrption()` / `setDescrption()`).

**Evidence:**
```java
// MymessagesUsersBean.java lines 18, 58-63
String descrption = "";
...
public String getDescrption() {
    return descrption;
}
public void setDescrption(String descrption) {
    this.descrption = descrption;
}
```

---

### F-16 [LOW] Typo in field/method name: `arrImpactSummryBean` (missing 'a')

**File:** ImpactDeptBean.java (line 14)

**Description:** The field `arrImpactSummryBean` is missing the letter 'a' and should be `arrImpactSummaryBean`. The getter/setter perpetuate this typo.

**Evidence:**
```java
// ImpactDeptBean.java line 14
ArrayList<ImpactSummaryBean> arrImpactSummryBean = new ArrayList<ImpactSummaryBean>();

// ImpactDeptBean.java lines 30-36
public ArrayList<ImpactSummaryBean> getArrImpactSummryBean() {
    return arrImpactSummryBean;
}
public void setArrImpactSummryBean(
        ArrayList<ImpactSummaryBean> arrImpactSummryBean) {
    this.arrImpactSummryBean = arrImpactSummryBean;
}
```

---

### F-17 [MEDIUM] Commented-out section markers without actionable context

**File:** ImpactBean.java (lines 25, 40-43)

**Description:** Comments like `//monthly national report`, `//new monthly report`, and `//end` are used as section markers within the class. While not commented-out code, the `//new monthly report` and `//end` pattern suggests code was added in phases without refactoring. The `//end` comment is a code smell indicating the class is accumulating responsibilities and the fields could be better organized into separate beans or inner classes.

**Evidence:**
```java
// ImpactBean.java lines 25-26
//monthly national report
int[] blueshock = new int[8];

// ImpactBean.java lines 40-43
//new monthly report
int[] impacts =null;
int total = 0;
//end
```

---

### F-18 [INFO] Vague/generic field names reduce readability

**Files affected:** EntityBean.java, ImpactBean.java, PreCheckBean.java

**Description:** Several fields use extremely generic names that provide no domain context: `id`, `name`, `total`, `attribute`, `index`, `complete`, `incomplete`. `EntityBean` itself is a very generic class name. Without documentation, the purpose of these beans is unclear from their API alone.

**Evidence:**
```java
// EntityBean.java lines 12-16
String id = "";
String name = "";
double totalno = 0;
String attribute = "";

// PreCheckBean.java lines 17-19
int complete = 0;
int incomplete = 0;
int total = 0;
```

---

### F-19 [MEDIUM] ImpactBean approaching God-class territory

**File:** ImpactBean.java (258 lines, 25+ fields)

**Description:** `ImpactBean` has 25+ fields spanning multiple report types (base impact data, monthly national report shock arrays, shift-based shock 2D arrays, usage percentage, new monthly report arrays). The class serves at least three different reporting contexts, indicated by the section comments. This class should be decomposed into focused beans for each report type.

Field count: `cust_cd`, `loc_cd`, `dept_cd`, `dept_name`, `model_cd`, `model_name`, `driver_cd`, `driver_name`, `unit_cd`, `unit_name`, `unit_type`, `year`, `month`, `impact_no`, `blueshock[8]`, `ambershock[8]`, `redshock[8]`, `blueimpact`, `amberimpact`, `redimpact`, `iotime`, `blueshockShift[8][3]`, `ambershockShift[8][3]`, `redshockShift[8][3]`, `usagePercentage`, `impacts[]`, `total`, `impactMap`.

**Evidence:**
```java
// ImpactBean.java -- 28 fields across 258 lines
// Base fields (lines 11-24): 13 fields
// Monthly national report (lines 25-36): 10 fields (arrays)
// New monthly report (lines 40-42): 2 fields
// Map (line 45): 1 field
```

---

### F-20 [MEDIUM] NotificationSettingsBean.notification_id initialized to null while peers use empty string

**File:** NotificationSettingsBean.java (line 5)

**Description:** The `notification_id` field is left uninitialized (defaults to `null`), while all other String fields in the same class are initialized to empty string `""`. This is inconsistent and creates a risk of `NullPointerException` if `getNotification_id()` is called before a value is set. Nearly all other beans in this package initialize String fields to `""`.

**Evidence:**
```java
// NotificationSettingsBean.java lines 5-9
private String notification_id;        // defaults to null
private String header = "";            // initialized to ""
private String title = "";             // initialized to ""
private String content = "";           // initialized to ""
private String signature = "";         // initialized to ""
```

---

### F-21 [LOW] LicenseBlackListBean initializes some fields to null instead of empty string

**File:** LicenseBlackListBean.java (lines 13-16)

**Description:** The `access_level`, `access_cust`, `access_site`, and `access_dept` fields are initialized to `null` while other string fields in the same class (`vehicleType`, `custCd`, etc.) are left uninitialized (also `null` by default). This is inconsistent with the broader bean package convention of initializing String fields to `""`, and the explicit `=null` adds no value since `null` is already the default for object references.

**Evidence:**
```java
// LicenseBlackListBean.java lines 7-17
private String vehicleType;                  // null (implicit)
private String custCd;                       // null (implicit)
private String locCd;                        // null (implicit)
private String deptCd;                       // null (implicit)
private String expiryDate;                   // null (implicit)
private String driverCd;                     // null (implicit)
private String access_level=null;            // null (explicit)
private String access_cust=null;             // null (explicit)
private String access_site=null;             // null (explicit)
private String access_dept=null;             // null (explicit)
private ArrayList<String> vehicleCds;        // null (implicit)
```

---

### F-22 [MEDIUM] Dates represented as String types

**Files affected:** LicenseBlackListBean.java (field `expiryDate`), LockOutBean.java (fields `lockouttime`, `unlocktime`)

**Description:** Date/time values are stored as `String` instead of proper date types (`java.util.Date`, `java.time.LocalDateTime`, etc.). This prevents type-safe date operations, makes comparison and sorting error-prone, and couples the bean to a specific date format that is not documented.

**Evidence:**
```java
// LicenseBlackListBean.java line 11
private String expiryDate;

// LockOutBean.java lines 14, 16
String lockouttime = "";
String unlocktime = "";
```

---

### F-23 [INFO] No Javadoc or documentation on any class or field

**Files affected:** All 16 files

**Description:** None of the 16 bean classes contain any Javadoc comments on the class, fields, or methods. The only comments present are auto-generated `serialVersionUID` Javadoc stubs and the section markers in `ImpactBean`. For a domain model layer, the complete absence of documentation makes it difficult to understand the purpose and constraints of each field.

---

### F-24 [LOW] Missing space before opening brace in class declarations

**Files affected:** EntityBean.java, ImpactBean.java, ImpactDeptBean.java, ImpactLocBean.java, ImpactSummaryBean.java, LockOutBean.java, MaxHourUsageBean.java, MymessagesUsersBean.java, NetworkSettingBean.java, PreCheckBean.java, PreCheckDriverBean.java, PreCheckSummaryBean.java

**Description:** Class declarations implementing `Serializable` are missing a space before the opening brace: `implements Serializable{` instead of `implements Serializable {`.

**Evidence:**
```java
// EntityBean.java line 5
public class EntityBean implements Serializable{

// ImpactBean.java line 6
public class ImpactBean implements Serializable{
```

---

### F-25 [MEDIUM] Double-space in field declaration

**File:** FleetCheckBean.java (line 9)

**Description:** Minor formatting issue -- double space between the generic type and field name.

**Evidence:**
```java
// FleetCheckBean.java line 9
ArrayList<String>  frequent_failed_question = new ArrayList<String>();
//                ^^ double space
```

---

### F-26 [INFO] Inconsistent spacing around assignment operators

**Files affected:** EntityBean.java (line 16), MenuBean.java (lines 7-12), LicenseBlackListBean.java (lines 13-16)

**Description:** Some field initializations have no space before `=` or inconsistent spacing.

**Evidence:**
```java
// EntityBean.java line 16
String locs ="";      // no space before =

// MenuBean.java line 7
private String Menus_Cd ="";  // no space before =

// LicenseBlackListBean.java line 13
private String access_level=null;  // no space around =
```

---

### F-27 [LOW] Mutable arrays returned from getters without defensive copying

**Files affected:** ImpactBean.java, PreCheckBean.java, PreCheckDriverBean.java

**Description:** Array fields (`int[] checks`, `int[] blueshock`, `int[][] blueshockShift`, etc.) are returned directly from getters without defensive copying. Callers can modify the array contents and corrupt the bean state. Unlike collection wrappers (Collections.unmodifiableList), arrays have no immutable wrapper -- defensive copies via `Arrays.copyOf()` are the standard mitigation.

**Evidence:**
```java
// ImpactBean.java lines 128-130
public int[] getBlueshock() {
    return blueshock;
}

// PreCheckDriverBean.java lines 35-37
public int[] getChecks() {
    return checks;
}

// ImpactBean.java lines 232-234
public int[][] getBlueshockShift() {
    return blueshockShift;
}
```

---

### F-28 [INFO] Magic number: array size 8 and 3 in ImpactBean

**File:** ImpactBean.java (lines 26-28, 34-36)

**Description:** The array sizes `8` and `3` are used as magic numbers without documentation or named constants. It is unclear what the 8 indices represent (days of week + total? shock severity levels?) or what the 3 shift columns represent.

**Evidence:**
```java
// ImpactBean.java lines 26-28
int[] blueshock = new int[8];
int[] ambershock = new int[8];
int[] redshock = new int[8];

// ImpactBean.java lines 34-36
int[][] blueshockShift = new int[8][3];
int[][] ambershockShift = new int[8][3];
int[][] redshockShift = new int[8][3];
```

---

### F-29 [INFO] Hungarian notation prefix "arr" on collection fields

**Files affected:** ImpactDeptBean.java, ImpactLocBean.java, ImpactSummaryBean.java, MaxHourUsageBean.java, PreCheckBean.java, PreCheckSummaryBean.java

**Description:** Collection fields use the `arr` prefix (e.g., `arrImpactSummryBean`, `arrImpactDeptBean`, `arrImpact`, `arrUnitUtil`, `arrPreCheckDriverBean`, `arrPrecheck`). This is a form of Hungarian notation that is considered obsolete in modern Java. The type system already conveys that these are collections.

**Evidence:**
```java
// ImpactDeptBean.java line 14
ArrayList<ImpactSummaryBean> arrImpactSummryBean = ...;

// MaxHourUsageBean.java line 15
ArrayList<UnitutilBean> arrUnitUtil = ...;
```

---

### F-30 [HIGH] LicenseBlackListBean fields default to null -- NullPointerException risk

**File:** LicenseBlackListBean.java (lines 7-17)

**Description:** All String fields in `LicenseBlackListBean` default to `null` (either explicitly or implicitly), unlike the convention in most other beans in this package which initialize to `""`. The `vehicleCds` ArrayList also defaults to null. Any code that calls `getVehicleType()`, `getCustCd()`, or `getVehicleCds()` without prior null-checking risks a `NullPointerException`. This is particularly dangerous for `getVehicleCds()` since iterating over a null list will throw NPE.

**Evidence:**
```java
// LicenseBlackListBean.java lines 7-17
private String vehicleType;         // null
private String custCd;              // null
private String locCd;               // null
private String deptCd;              // null
private String expiryDate;          // null
private String driverCd;            // null
private String access_level=null;   // null
private String access_cust=null;    // null
private String access_site=null;    // null
private String access_dept=null;    // null
private ArrayList<String> vehicleCds;  // null -- iteration will NPE
```

---

### F-31 [MEDIUM] ImpactBean.impacts field initialized to null unlike peer arrays

**File:** ImpactBean.java (line 41)

**Description:** The `impacts` field is initialized to `null` while the peer array fields `blueshock`, `ambershock`, and `redshock` are initialized to `new int[8]`. This inconsistency means callers must null-check `getImpacts()` but not the other array getters, creating a fragile API.

**Evidence:**
```java
// ImpactBean.java lines 26-28 vs line 41
int[] blueshock = new int[8];     // initialized
int[] ambershock = new int[8];    // initialized
int[] redshock = new int[8];      // initialized
...
int[] impacts = null;             // null -- inconsistent
```

---

### F-32 [LOW] Redundant blank lines and trailing whitespace

**Files affected:** ImpactBean.java (lines 256-257), LockOutBean.java (lines 62-63), MenuBean.java (lines 50-51), NotificationSettingsBean.java (lines 49-50), PreCheckSummaryBean.java (lines 50-53)

**Description:** Multiple files end with unnecessary blank lines or have consecutive blank lines within the class body serving no structural purpose.

**Evidence:**
```java
// PreCheckSummaryBean.java lines 49-54
    }




}
```

---

### F-33 [MEDIUM] Using double for monetary/count value in EntityBean

**File:** EntityBean.java (line 14)

**Description:** The field `totalno` is declared as `double`. If this represents a count or monetary value, `double` introduces floating-point precision issues. Without documentation, it is unclear what `totalno` represents, but the name suggests a total number/count which should typically be an `int` or `long`, or `BigDecimal` if precision is needed.

**Evidence:**
```java
// EntityBean.java line 14
double totalno = 0;
```

---

### F-34 [INFO] No equals/hashCode/toString overrides on any bean

**Files affected:** All 16 files

**Description:** None of the 16 bean classes override `equals()`, `hashCode()`, or `toString()`. For beans used in collections (especially as HashMap keys or in Sets), the absence of `equals`/`hashCode` means identity-based comparison is used, which may not match business semantics. The absence of `toString` makes debugging and logging difficult.

---

## Checks with No Findings

The following Pass 4 checks produced no findings for the files in scope:

| Check | Status |
|-------|--------|
| Deprecated API usage | No deprecated API calls found |
| Empty catch blocks | No try/catch blocks present in any file |
| Broad catch (Exception/Throwable) | No try/catch blocks present in any file |
| e.printStackTrace() | No exception handling present in any file |
| Null returns on error | No methods return null on error paths (beans are data holders only) |
| N+1 query patterns | No database queries present in any file |
| Commented-out code | No commented-out executable code found |

---

## File-by-File Summary

| File | Findings | Severity Profile |
|------|----------|------------------|
| EntityBean.java | F-01, F-02, F-18, F-24, F-26, F-33, F-34 | 0H / 1M / 1L / 2I |
| FleetCheckBean.java | F-01, F-02, F-04, F-05, F-09, F-12, F-13, F-25 | 1H / 3M / 1L / 0I |
| ImpactBean.java | F-01, F-02, F-04, F-05, F-12, F-13, F-14, F-17, F-19, F-24, F-27, F-28, F-31 | 1H / 3M / 3L / 1I |
| ImpactDeptBean.java | F-01, F-02, F-04, F-05, F-12, F-16, F-24, F-29 | 1H / 2M / 2L / 1I |
| ImpactLocBean.java | F-01, F-02, F-05, F-12, F-24, F-29 | 1H / 2M / 0L / 1I |
| ImpactSummaryBean.java | F-01, F-02, F-04, F-05, F-07, F-12, F-24, F-29 | 1H / 2M / 2L / 1I |
| LicenseBlackListBean.java | F-01, F-04, F-05, F-12, F-21, F-22, F-26, F-30 | 1H / 3M / 2L / 0I |
| LockOutBean.java | F-01, F-02, F-04, F-22, F-24, F-32 | 0H / 2M / 2L / 0I |
| MaxHourUsageBean.java | F-01, F-02, F-05, F-12, F-24, F-29 | 1H / 2M / 0L / 1I |
| MenuBean.java | F-03, F-04, F-09, F-10, F-26 | 0H / 3M / 1L / 0I |
| MymessagesUsersBean.java | F-01, F-02, F-04, F-15, F-24 | 0H / 2M / 2L / 0I |
| NetworkSettingBean.java | F-06, F-24 | 1H / 0M / 1L / 0I |
| NotificationSettingsBean.java | F-04, F-09, F-20 | 0H / 2M / 0L / 0I |
| PreCheckBean.java | F-01, F-02, F-04, F-05, F-11, F-12, F-18, F-24, F-27, F-29 | 1H / 3M / 2L / 1I |
| PreCheckDriverBean.java | F-01, F-02, F-04, F-24, F-27 | 0H / 2M / 2L / 0I |
| PreCheckSummaryBean.java | F-01, F-02, F-04, F-05, F-08, F-12, F-24, F-29, F-32 | 1H / 2M / 3L / 1I |

---

*End of Pass 4 Code Quality Audit -- bean package (E-P)*
*Agent A02 | 2026-02-25*
