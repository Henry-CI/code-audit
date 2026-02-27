# Pass 4 -- Code Quality Audit: excel/reports/beans (A-D)

**Auditor:** A13
**Date:** 2026-02-25
**Repository:** C:\Projects\cig-audit\repos\fleetfocus
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Package:** `com.torrent.surat.fms6.excel.reports.beans`
**Scope:** 15 files (BaseFilterBean through DynUnitReportBean)

---

## 1. Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 1 |
| HIGH     | 6 |
| MEDIUM   | 8 |
| LOW      | 5 |
| INFO     | 3 |

All 15 files are plain Java bean / POJO classes with no business logic. They serve as data-transfer objects for Excel report generation. The codebase exhibits systematic code-quality issues: pervasive use of raw generic types, inconsistent naming conventions, exact code duplication, an empty base class, package-private field visibility throughout, and zero use of Java annotations or standard `Object` method overrides.

---

## 2. File-by-File Findings

### 2.1 BaseFilterBean.java (55 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/BaseFilterBean.java`

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 1 | MEDIUM | **Package-private fields** -- All 7 fields (`cust`, `site`, `dept`, `startTime`, `endTime`, `includeZLinde`, `searchCrit`) declared without access modifier, making them package-private instead of `private`. | Lines 5-11: `String cust = "";` etc. -- no `private` keyword. |
| 2 | LOW | **Inconsistent `this.` usage** -- Some getters use `this.` prefix (lines 14, 20, 26, 32, 38) while others do not (lines 44, 50). | `return this.cust;` vs `return includeZLinde;` |
| 3 | LOW | **No `Serializable` implementation** -- Bean may be placed in HTTP session or serialized but does not implement `Serializable`. | Class declaration, line 3. |
| 4 | INFO | **No `toString()` / `equals()` / `hashCode()` overrides** -- Standard object contract methods are absent; debugging difficulty. | Entire file -- no such methods. |
| 5 | MEDIUM | **Not extended by any bean in scope** -- Despite the `Base` prefix suggesting a base class pattern, `BaseFilterBean` is never extended. It is only used by composition in `BaseResultBean` and instantiated in `Databean_dyn_reports`. The naming is misleading. | Grep for `extends BaseFilterBean` returns zero results. Used via `new BaseFilterBean()` in `Databean_dyn_reports.java:4937` and as a field type in `BaseResultBean.java:6`. |

---

### 2.2 BaseItemResultBean.java (5 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/BaseItemResultBean.java`

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 6 | HIGH | **Empty class -- dead code candidate** -- The class body is completely empty (no fields, no methods). It serves only as a marker type for `OperationalStatusReportItemResultBean extends BaseItemResultBean`, which gains nothing from this inheritance. | Lines 1-5: entire file is `public class BaseItemResultBean { }`. The sole subclass `OperationalStatusReportItemResultBean` inherits zero functionality. |

---

### 2.3 BaseResultBean.java (15 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/BaseResultBean.java`

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 7 | MEDIUM | **Package-private field** -- `appliedFilterBean` is package-private. | Line 6: `BaseFilterBean appliedFilterBean;` -- no access modifier. |
| 8 | MEDIUM | **Unused base class by audited beans** -- Only `OperationalStatusReportResultBean` (outside this audit scope) extends `BaseResultBean`. None of the 12 concrete report beans in scope (Battery, Cimplicity*, Curr*, Daily*, Driver*, Dyn*) extend it, despite many of them conceptually being "result beans." | Grep for `extends BaseResultBean` returns only `OperationalStatusReportResultBean.java`. |
| 9 | LOW | **Extra blank line** -- Line 3 is an unnecessary blank line between the package declaration and class declaration. | Line 3 is empty. |

---

### 2.4 BatteryReportBean.java (51 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/BatteryReportBean.java`

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 10 | HIGH | **Raw `ArrayList` types** -- All 5 ArrayList fields use raw types without generics, producing compiler warnings and disabling compile-time type safety. | Lines 6-10: `ArrayList vunit_name = new ArrayList();` etc. |
| 11 | MEDIUM | **Package-private fields** -- All 6 fields lack `private` modifier. | Lines 6-11. |
| 12 | HIGH | **Snake_case field and method naming** -- Field names (`vunit_name`, `vdriver_name`, `model_name`) and corresponding getter/setter names (`getVunit_name`, `setModel_name`) violate Java camelCase naming conventions. | Lines 6-11, 13-48. |
| 13 | INFO | **Does not extend BaseResultBean** -- Despite being a report result bean, it does not use the base class hierarchy. | Class declaration, line 5: `public class BatteryReportBean {`. |

---

### 2.5 CimplicityShockReportBean.java (26 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/CimplicityShockReportBean.java`

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 14 | HIGH | **Raw `ArrayList` types** -- Both ArrayList fields use raw types. | Lines 7-8: `ArrayList vmachine_nm = new ArrayList();` |
| 15 | MEDIUM | **Package-private fields** -- Both fields lack `private`. | Lines 7-8. |
| 16 | LOW | **Snake_case naming** -- `vmachine_nm`, `vuser_nm`, `getVmachine_nm()` etc. | Lines 7-8, 11-22. |
| 17 | LOW | **Excessive trailing blank lines** -- Three blank lines at end of class body (lines 23-25). | Lines 23-25. |

---

### 2.6 CimplicityUtilReportBean.java (59 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/CimplicityUtilReportBean.java`

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 18 | HIGH | **Raw `ArrayList` types** -- All 7 ArrayList fields use raw types. | Lines 7-13. |
| 19 | MEDIUM | **Package-private fields** -- All 7 fields lack `private`. | Lines 7-13. |
| 20 | HIGH | **Uppercase-initial field names** -- Fields `Vrpt_field_cd` and `Vrpt_field_nm` start with uppercase, violating Java naming conventions and creating confusion with class names. Also mixes snake_case. | Lines 7-8: `ArrayList Vrpt_field_cd = new ArrayList();`, `ArrayList Vrpt_field_nm = new ArrayList();` |
| 21 | MEDIUM | **Inconsistent `this.` usage** -- Setters for `Vrpt_field_cd` and `Vrpt_field_nm` assign without `this.` prefix (lines 18, 24: `Vrpt_field_cd = vrpt_field_cd;`) while setters for `dsum_*` fields use `this.` (line 30: `this.dsum_veh_cd = dsum_veh_cd;`). | Compare line 18 vs line 30. |
| 22 | MEDIUM | **Field overlap with DailyVehSummaryReportBean** -- Fields `dsum_veh_cd`, `dsum_veh_nm`, `dsum_veh_typ_nm`, `dsum_key_hr`, `dsum_key_hr_nc` are identical to fields in `DailyVehSummaryReportBean`, indicating potential for shared base class or composition. | Lines 9-13 here vs lines 9, 10, 12, 13, 17 in DailyVehSummaryReportBean. |

---

### 2.7 CurrDrivReportBean.java (118 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/CurrDrivReportBean.java`

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 23 | CRITICAL | **Exact code duplication with CurrUnitReportBean** -- `CurrDrivReportBean` and `CurrUnitReportBean` are byte-for-byte identical in structure: same 15 fields, same types, same names, same getters/setters, same line count (118 lines). The only difference is the class name. This is a textbook case of duplicated code that should be a single shared class or at minimum one extending the other. | Diff of `CurrDrivReportBean.java` (lines 1-118) vs `CurrUnitReportBean.java` (lines 1-118): only `class CurrDrivReportBean` vs `class CurrUnitReportBean` differs. All 15 fields (`Vrpt_veh_typ_cd` through `Vrpt_curr_st_tm`) and 30 getters/setters are identical. |
| 24 | HIGH | **Raw `ArrayList` types** -- All 15 ArrayList fields use raw types. | Lines 7-22. |
| 25 | MEDIUM | **Package-private fields** -- All 15 fields lack `private`. | Lines 7-22. |
| 26 | HIGH | **Uppercase-initial field names** -- All 15 fields start with uppercase `V` (e.g., `Vrpt_veh_typ_cd`), violating Java conventions. Combined with snake_case. | Lines 7-22. |
| 27 | MEDIUM | **Inconsistent `this.` usage in setters** -- Setters assign to the uppercase field name directly (e.g., `Vrpt_veh_typ_cd = vrpt_veh_typ_cd;`) without `this.` -- this works only because the parameter name differs in case from the field name. | Lines 27, 33, 39, etc. |

---

### 2.8 CurrUnitReportBean.java (118 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/CurrUnitReportBean.java`

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 28 | -- | **Exact duplicate of CurrDrivReportBean** -- All findings from 2.7 (#23-#27) apply identically. See finding #23. | Entire file is structurally identical to CurrDrivReportBean.java. |

---

### 2.9 DailyVehSummaryReportBean.java (207 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DailyVehSummaryReportBean.java`

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 29 | HIGH | **Raw `ArrayList` types** -- All 16 ArrayList fields use raw types. | Lines 7-22: `ArrayList dsum_driver_cd = new ArrayList();` etc. |
| 30 | MEDIUM | **Package-private fields** -- All 20 fields (16 ArrayLists, 3 Strings, 1 boolean, 1 int) lack `private`. | Lines 6-36. |
| 31 | HIGH | **Snake_case naming throughout** -- All field names and getter/setter names use underscores (e.g., `dsum_driver_cd`, `getDsum_driver_cd`). | Lines 7-205. |
| 32 | INFO | **Largest bean in scope** -- At 207 lines with 20 fields and 40 getters/setters, this bean is significantly larger than peers, suggesting it may benefit from decomposition. | Line count and field count. |

---

### 2.10 DriverAccessAbuseBean.java (107 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DriverAccessAbuseBean.java`

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 33 | HIGH | **Duplicate import** -- `java.util.ArrayList` is imported twice on consecutive lines. | Lines 3-4: `import java.util.ArrayList;` appears twice. |
| 34 | HIGH | **Mixed raw and parameterized types** -- 11 fields use raw `ArrayList` (lines 8-18) while 2 fields use `ArrayList<String>` (lines 21-22). This inconsistency within the same class is particularly poor. | Lines 8-18: `ArrayList a_driv_cd = new ArrayList();` vs lines 21-22: `private ArrayList<String> a_ol_start_list = new ArrayList();` |
| 35 | MEDIUM | **Mixed access modifiers** -- 11 fields are package-private (lines 8-18), while 3 fields are `private` (lines 20-22). Inconsistent within the same class. | Line 8: ` ArrayList a_driv_cd` (package-private) vs line 20: `private String a_time_filter`. |
| 36 | MEDIUM | **Raw type on right side of parameterized declaration** -- The parameterized fields still use raw `ArrayList()` constructor on the right-hand side (diamond operator `<>` not used). | Lines 21-22: `private ArrayList<String> a_ol_start_list = new ArrayList();` -- should be `new ArrayList<>()` or `new ArrayList<String>()`. |
| 37 | LOW | **Leading space in method signatures** -- Some method signatures have a leading space before `ArrayList` (e.g., ` ArrayList getA_driv_cd()`). Inconsistent formatting. | Lines 23, 26, 29, 32, etc. |

---

### 2.11 DriverImpactReportBean.java (78 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DriverImpactReportBean.java`

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 38 | HIGH | **Raw `ArrayList` types** -- All 10 ArrayList fields use raw types. | Lines 7-16. |
| 39 | MEDIUM | **Package-private fields** -- All 10 fields lack `private`. | Lines 7-16. |
| 40 | MEDIUM | **Brace style inconsistency** -- Opening brace for class declaration is on a new line (`{` on line 6), differing from all other beans in this package which place `{` on the same line as the class declaration. | Line 5-6: `public class DriverImpactReportBean` then line 6: `{` on its own line. |

---

### 2.12 DriverLicenceExpiryBean.java (23 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DriverLicenceExpiryBean.java`

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 41 | HIGH | **Raw `ArrayList` types** -- Both ArrayList fields use raw types. | Lines 6-7: `ArrayList driver_nm = new ArrayList();` |
| 42 | MEDIUM | **Package-private fields** -- Both fields lack `private`. | Lines 6-7. |
| 43 | LOW | **Inconsistent naming suffix** -- Named `DriverLicenceExpiryBean` rather than `DriverLicenceExpiryReportBean`, inconsistent with the `*ReportBean` naming pattern used by most other beans. | Class name on line 5. |

---

### 2.13 DynDriverReportBean.java (178 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DynDriverReportBean.java`

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 44 | HIGH | **Raw `ArrayList` types** -- All 21 ArrayList fields use raw types. | Lines 8-29. |
| 45 | MEDIUM | **Package-private fields** -- All 23 fields (21 ArrayLists + 2 Strings) lack `private`. | Lines 7-30. |
| 46 | HIGH | **Uppercase-initial field names** -- 20 of 21 ArrayList fields begin with uppercase `V` (e.g., `Vrpt_veh_typ_cd`). Combined with snake_case. | Lines 8-29. |
| 47 | MEDIUM | **Significant field overlap with DynUnitReportBean** -- 19 of 21 ArrayList fields in DynDriverReportBean are identical to fields in DynUnitReportBean, indicating substantial duplication. DynUnitReportBean adds 4 extra fields (`Vrpt_veh_op_mode`, `Vrpt_vor_count`, `Vrpt_excluded_veh_cd`, `includeZLinde`) and `opMode`. | Compare field lists of both files. Shared: `Vrpt_veh_typ_cd`, `Vrpt_veh_typ`, `Vrpt_veh_cd`, `Vrpt_veh_nm`, `Vrpt_veh_id`, `Vrpt_field_cd`, `Vrpt_field_nm`, `Vrpt_veh_value_start`, `Vrpt_veh_value_stop`, `Vrpt_veh_value_state`, `Vrpt_veh_custo` (only in DynDriver), `Vrpt_veh_site` (only in DynDriver), `Vrpt_veh_driv_cd`, `Vrpt_veh_driv_nm`, `Vrpt_veh_driv_tm`, `Vrpt_veh_sttm`, `Vrpt_veh_endtm`, `Vrpt_veh_gtotal`, `Vrpt_veh_tot`, `Vrpt_veh_dep`, `Vrpt_veh_fno`, `Vrpt_veh_shutdown`, `do_list`, `searchCrit`. |

---

### 2.14 DynSeenReportBean.java (102 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DynSeenReportBean.java`

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 48 | HIGH | **Raw `ArrayList` types** -- All 12 ArrayList fields use raw types. | Lines 7-18. |
| 49 | MEDIUM | **Package-private fields** -- All 13 fields lack `private`. | Lines 7-19. |
| 50 | HIGH | **Uppercase-initial field names** -- 12 of 12 ArrayList fields begin with uppercase `V`. | Lines 7-18: `ArrayList Vrpt_veh_cd = new ArrayList();` etc. |

---

### 2.15 DynUnitReportBean.java (200 lines)

**Path:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/DynUnitReportBean.java`

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 51 | HIGH | **Raw `ArrayList` types** -- All 22 ArrayList fields use raw types. | Lines 6-28. |
| 52 | MEDIUM | **Package-private fields** -- All 26 fields (22 ArrayLists + 4 Strings) lack `private`. | Lines 6-33. |
| 53 | HIGH | **Uppercase-initial field names** -- 22 of 22 ArrayList fields begin with uppercase `V`. | Lines 6-28. |
| 54 | MEDIUM | **Significant field overlap with DynDriverReportBean** -- See finding #47 for detailed comparison. DynUnitReportBean is a superset of most DynDriverReportBean fields. | See finding #47. |
| 55 | LOW | **Leading space in method signatures** -- `getVrpt_veh_op_mode` and `setVrpt_veh_op_mode` have a leading space before `ArrayList` in the return type / parameter type. | Lines 78, 81: `public  ArrayList getVrpt_veh_op_mode()` (two spaces). |

---

## 3. Cross-Cutting Findings

### 3.1 Raw ArrayList Types (ALL 12 concrete beans)

Every concrete report bean in scope uses raw `ArrayList` without generic type parameters. This is the single most pervasive issue. Across all files, there are approximately **134 raw ArrayList declarations** (fields + getter/setter parameters).

**Affected files (all 12 concrete beans):**
BatteryReportBean (5), CimplicityShockReportBean (2), CimplicityUtilReportBean (7), CurrDrivReportBean (15), CurrUnitReportBean (15), DailyVehSummaryReportBean (16), DriverAccessAbuseBean (11 raw + 2 parameterized), DriverImpactReportBean (10), DriverLicenceExpiryBean (2), DynDriverReportBean (21), DynSeenReportBean (12), DynUnitReportBean (22).

### 3.2 Package-Private Fields (14 of 15 files)

Every file except `BaseItemResultBean` (which is empty) declares fields without explicit `private` access. This exposes internal state to any class in the same package, violating encapsulation. The only exception is `DriverAccessAbuseBean`, which has 3 `private` fields mixed with 11 package-private fields.

### 3.3 Snake_Case and Uppercase-Initial Naming Violations

Two distinct naming violations appear:

1. **Snake_case field/method names** (ALL concrete beans): `vunit_name`, `getDsum_key_hr()`, etc. Standard Java convention requires camelCase.
2. **Uppercase-initial field names** (6 beans): `Vrpt_veh_typ_cd`, `Vrpt_field_cd`, etc. This convention is reserved for class names in Java. Affected: CimplicityUtilReportBean, CurrDrivReportBean, CurrUnitReportBean, DynDriverReportBean, DynSeenReportBean, DynUnitReportBean.

### 3.4 Code Duplication Summary

| Duplication Pair | Overlap | Severity |
|-----------------|---------|----------|
| CurrDrivReportBean / CurrUnitReportBean | 100% identical (15/15 fields, all getters/setters) | CRITICAL |
| DynDriverReportBean / DynUnitReportBean | ~85% overlap (19 shared fields of 21/22) | HIGH |
| CimplicityUtilReportBean / DailyVehSummaryReportBean | 5 identical fields | MEDIUM |

### 3.5 Unused/Questionable Base Class Hierarchy

The intended base class hierarchy (`BaseFilterBean`, `BaseResultBean`, `BaseItemResultBean`) is almost entirely unused by the beans in this scope:

- **BaseFilterBean**: Never extended. Used only via composition in `BaseResultBean` and direct instantiation in `Databean_dyn_reports`. Name prefix "Base" is misleading.
- **BaseResultBean**: Extended only by `OperationalStatusReportResultBean` (outside audit scope). Zero of the 12 concrete beans in scope extend it.
- **BaseItemResultBean**: Completely empty. Extended only by `OperationalStatusReportItemResultBean` (outside audit scope), which gains nothing from the inheritance.

### 3.6 Missing Standard Java Practices

Across all 15 files:
- **No `Serializable` implementation** on any bean
- **No annotations** (`@SuppressWarnings`, `@Override`, etc.) used anywhere
- **No `toString()`** overrides (makes debugging difficult)
- **No `equals()` / `hashCode()`** overrides
- **No Javadoc** or comments of any kind
- **No constructors** (all rely on default constructor + field initializers)
- **No use of `List` interface** -- all fields are typed to the concrete `ArrayList` class rather than the `List` interface

---

## 4. Findings Tally by File

| File | CRIT | HIGH | MED | LOW | INFO |
|------|------|------|-----|-----|------|
| BaseFilterBean | 0 | 0 | 2 | 2 | 1 |
| BaseItemResultBean | 0 | 1 | 0 | 0 | 0 |
| BaseResultBean | 0 | 0 | 2 | 1 | 0 |
| BatteryReportBean | 0 | 2 | 1 | 0 | 1 |
| CimplicityShockReportBean | 0 | 1 | 1 | 2 | 0 |
| CimplicityUtilReportBean | 0 | 2 | 2 | 0 | 0 |
| CurrDrivReportBean | 1 | 2 | 2 | 0 | 0 |
| CurrUnitReportBean | (dup) | (dup) | (dup) | (dup) | (dup) |
| DailyVehSummaryReportBean | 0 | 2 | 1 | 0 | 1 |
| DriverAccessAbuseBean | 0 | 2 | 2 | 1 | 0 |
| DriverImpactReportBean | 0 | 1 | 2 | 0 | 0 |
| DriverLicenceExpiryBean | 0 | 1 | 1 | 1 | 0 |
| DynDriverReportBean | 0 | 2 | 2 | 0 | 0 |
| DynSeenReportBean | 0 | 2 | 1 | 0 | 0 |
| DynUnitReportBean | 0 | 2 | 2 | 1 | 0 |

---

## 5. Recommendations (report only -- no fixes applied)

1. **Eliminate CurrDrivReportBean/CurrUnitReportBean duplication** -- Consolidate into a single class or extract a shared parent.
2. **Add generic type parameters** to all ArrayList declarations across all 12 concrete beans (~134 declarations).
3. **Change all fields to `private`** and use `List` interface type instead of `ArrayList` concrete type.
4. **Evaluate BaseItemResultBean** for removal -- it is empty and provides no value.
5. **Standardize naming to camelCase** -- Replace all snake_case and uppercase-initial field names.
6. **Extract shared fields** between DynDriverReportBean and DynUnitReportBean into a common base class.
7. **Reevaluate "Base" naming** for BaseFilterBean since it is never used as a base class.

---

*End of Pass 4 audit for excel/reports/beans (A-D).*
