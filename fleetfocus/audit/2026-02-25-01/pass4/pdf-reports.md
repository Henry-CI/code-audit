# Pass 4 -- Code Quality Audit: pdf + reports

**Auditor:** A16
**Date:** 2026-02-25
**Branch:** `release/UAT_RELEASE_FLEETFOCUS_Production`
**Scope:** 13 files across `WEB-INF/src/com/torrent/surat/fms6/pdf/` and `WEB-INF/src/com/torrent/surat/fms6/reports/`

---

## File Inventory

| # | File | Lines | Package |
|---|------|------:|---------|
| 1 | `MonthlyPDFRpt.java` | 173 | pdf |
| 2 | `ReportPDF.java` | 236 | pdf |
| 3 | `Databean_cdisp.java` | 1,747 | reports |
| 4 | `Databean_dyn_reports.java` | 10,015 | reports |
| 5 | `Databean_report.java` | 21,854 | reports |
| 6 | `Databean_report1.java` | 818 | reports |
| 7 | `Databean_reports.java` | 128 | reports |
| 8 | `LinderReportDatabean.java` | 1,935 | reports |
| 9 | `RTLSHeatMapReport.java` | 525 | reports |
| 10 | `RTLSImpactReport.java` | 1,262 | reports |
| 11 | `Reports.java` | 608 | reports |
| 12 | `UtilBean.java` | 71 | reports |
| 13 | `UtilModelBean.java` | 65 | reports |

**Total lines audited: ~39,437**

---

## CQ-01 God Classes / Excessive Size

### Finding CQ-01-A: `Databean_report.java` -- 21,854 lines (CRITICAL)

**Severity:** CRITICAL
**Evidence:**
- 21,854 lines in a single class with no inheritance hierarchy.
- ~409 ArrayList field declarations (vast majority raw/unparameterized).
- ~648 calls to `stmt.executeQuery()` -- all SQL execution lives in this one class.
- ~88 commented-out code statements of type `query/rset/stmt/if/for/while/String/int`.
- ~1,086 calls to `.equalsIgnoreCase()` throughout the file.
- The `init()` method (line 18511) is a monolithic dispatcher spanning ~1,500 lines of if-else chains that route ~40+ opcode strings to private methods. Each branch follows a nearly identical boilerplate pattern: `Fetch_division()`, `Fetch_group_customers()`, `Fetch_cust_locations()`, `Fetch_cust_dept()`, then a data-fetch method.
- Class directly mixes concerns: JNDI lookup, SQL execution, chart generation, PDF creation, email subscriptions, GPS data, battery reports, driver licences, impact data, service maintenance, hour-meter data, fleet check, utilisation, and more.
- This is approximately 20x the recommended maximum class size (1,000 lines).

**Affected lines:** Entire file (lines 1-21854).

### Finding CQ-01-B: `Databean_dyn_reports.java` -- 10,015 lines (HIGH)

**Severity:** HIGH
**Evidence:**
- 10,015 lines with ~160+ raw ArrayList field declarations (lines 88-186).
- ~216 calls to `stmt.executeQuery()`.
- The `init()` method (line 7767) spans ~500 lines dispatching ~20 opcodes with repeated boilerplate identical to `Databean_report.java`.
- Mixes JNDI lookup, SQL, filtering logic, and report data assembly.

**Affected lines:** Entire file (lines 1-10015).

### Finding CQ-01-C: `Databean_cdisp.java` -- 1,747 lines (MODERATE)

**Severity:** MODERATE
**Evidence:**
- 1,747 lines with ~47 calls to `stmt.executeQuery()`.
- Same monolithic `init()` pattern with single-connection single-statement JNDI lookup.
- All data processing, SQL, and presentation logic in one class.

**Affected lines:** Entire file.

### Finding CQ-01-D: `LinderReportDatabean.java` -- 1,935 lines (MODERATE)

**Severity:** MODERATE
**Evidence:**
- 1,935 lines, ~36 calls to `stmt.executeQuery()`.
- Mixes JNDI connection management with SQL queries for utilisation, impact, pre-op check, and supervisor unlock data.
- Same monolithic `init()` pattern at line 63.

**Affected lines:** Entire file.

---

## CQ-02 Naming Conventions

### Finding CQ-02-A: Non-standard class names with underscores

**Severity:** MODERATE
**Files affected:**
- `Databean_cdisp` (line 40)
- `Databean_dyn_reports` (line 40)
- `Databean_report` (line 80)
- `Databean_report1` (line 17)
- `Databean_reports` (line 12)

Java class names should use PascalCase without underscores. These classes use `snake_case` naming.

### Finding CQ-02-B: Methods use mixed naming conventions

**Severity:** MODERATE
**Evidence (examples from Databean_report.java):**
- `Fetch_users()`, `Fetch_Data()`, `Fetch_cust_locations()`, `Fetch_vehicle_types1()`, `Fetch_abuse_details_au()` -- methods starting with uppercase and using underscores.
- `clear_variables()`, `get_cust_type()`, `impact_level()` -- lowercase with underscores.
- `fetchNames()`, `fetchDashBoardSubscriptions()` -- standard camelCase.

Three different conventions are used within the same classes. Java convention is camelCase for methods.

### Finding CQ-02-C: Field names use Hungarian notation / mixed styles

**Severity:** LOW
**Evidence (Databean_report.java lines 162-540):**
- Prefixes like `V` for ArrayList fields: `Viodriver_id`, `Vimp_hire_no`, `Vveh_cd`, `Vms_veh_id`.
- Inconsistent: some fields use `v` prefix (`vutil_1`, `vdriver_cd`), others use descriptive names (`location_cd`, `location_nm`).
- Fields like `sm_hour_meter`, `dsum_driver_cd` -- abbreviations and underscores.

### Finding CQ-02-D: `UtilModelBean.java` -- field name starts with uppercase

**Severity:** LOW
**File:** `UtilModelBean.java`, line 9
**Evidence:** `private String Model = "";` -- field name starts with uppercase letter.

---

## CQ-03 Commented-Out Code

### Finding CQ-03-A: `Databean_report.java` -- ~88 commented-out code statements

**Severity:** HIGH
**Evidence:** 88 instances of commented-out executable code (queries, conditional logic, variable assignments). Example patterns: `//query =`, `//rset =`, `//if(`, `//for(`, `//String`, `//int`.

### Finding CQ-03-B: `Databean_reports.java` -- Entire method body commented out

**Severity:** HIGH
**File:** `Databean_reports.java`, lines 52-125
**Evidence:** The `query(String op_code)` method is entirely within a block comment (`/* ... */`), spanning 73 lines. This makes the class effectively empty (only field declarations and an empty `clearVectors()` method remain). The class appears to be dead code.

### Finding CQ-03-C: `Databean_dyn_reports.java` -- ~14 commented-out code statements

**Severity:** MODERATE
**Evidence:** 14 instances of commented-out executable code throughout the file.

### Finding CQ-03-D: `ReportPDF.java` -- commented-out code line

**Severity:** LOW
**File:** `ReportPDF.java`, line 153
**Evidence:** `// img.scaleToFit(520, 300);` -- commented-out alternative implementation.

### Finding CQ-03-E: `MonthlyPDFRpt.java` -- commented-out code

**Severity:** LOW
**File:** `MonthlyPDFRpt.java`, line 30
**Evidence:** `//setTitle("Monthly Report");` -- old title commented out.

---

## CQ-04 Unused / Wildcard Imports

### Finding CQ-04-A: Wildcard imports

**Severity:** MODERATE
**Files and lines:**
- `Databean_report1.java`, line 6: `import java.sql.*;`
- `Databean_cdisp.java`, line 6: `import java.sql.*;`
- `Databean_cdisp.java`, line 7: `import java.util.*;`

Wildcard imports obscure dependencies and can cause name collisions.

### Finding CQ-04-B: Potentially unused imports in ReportPDF.java

**Severity:** LOW
**File:** `ReportPDF.java`
**Evidence:**
- Line 14: `import com.itextpdf.text.List;` -- used only in `createList()` which is never called from within the class or its subclass `MonthlyPDFRpt`.
- Line 18: `import com.itextpdf.text.Section;` -- used only in `createList(Section subCatPart)` parameter, same dead method.

### Finding CQ-04-C: Potentially unused imports in Databean_report.java

**Severity:** LOW
**File:** `Databean_report.java`
**Evidence:**
- Line 33: `import javax.mail.MessagingException;`
- Line 34: `import javax.mail.internet.AddressException;`

These may not be used directly in the class (email may be handled via delegation to `com.torrent.surat.fms6.util.mail`).

---

## CQ-05 Broad / Empty Exception Catches

### Finding CQ-05-A: Broad `catch(Exception)` blocks throughout all files

**Severity:** HIGH
**Aggregate counts:**

| File | `catch(Exception)` count |
|------|------------------------:|
| Databean_report.java | 21 |
| RTLSImpactReport.java | 14 |
| LinderReportDatabean.java | 10 |
| RTLSHeatMapReport.java | 7 |
| Databean_dyn_reports.java | 6 |
| Reports.java | 5 |
| Databean_cdisp.java | 1 |
| Databean_report1.java | 1 |
| Databean_reports.java | 1 |
| MonthlyPDFRpt.java | 1 |
| **Total** | **67** |

Every database method catches `Exception` (the broadest possible type) rather than specific exceptions like `SQLException`, `NamingException`, etc. This swallows unexpected errors and makes debugging difficult.

### Finding CQ-05-B: Empty catch bodies with only TODO comments

**Severity:** HIGH
**Files:** `RTLSHeatMapReport.java`, `RTLSImpactReport.java`, `Reports.java`
**Evidence:** 70 instances of `// TODO Auto-generated catch block` in the `finally` blocks of these three files. The catch bodies contain only `e.printStackTrace()` preceded by this TODO comment, indicating auto-generated exception handling that was never properly implemented.

---

## CQ-06 `e.printStackTrace()` Usage

### Finding CQ-06-A: Massive use of `e.printStackTrace()` instead of logging

**Severity:** HIGH
**Aggregate counts:**

| File | `printStackTrace()` count |
|------|-------------------------:|
| RTLSImpactReport.java | 50 |
| Reports.java | 20 |
| RTLSHeatMapReport.java | 19 |
| Databean_report.java | 17 |
| LinderReportDatabean.java | 10 |
| Databean_dyn_reports.java | 6 |
| MonthlyPDFRpt.java | 1 |
| Databean_reports.java | 1 |
| **Total** | **124** |

All files use `e.printStackTrace()` which writes to stderr instead of using the Logger instances that are already declared in several of these classes (`RTLSHeatMapReport`, `RTLSImpactReport`, `Reports`, `Databean_report` all have `private static Logger log`). This is a direct contradiction -- the logger is available but not used for error handling.

### Finding CQ-06-B: `System.out.println()` used for error logging

**Severity:** HIGH
**Aggregate counts:**

| File | `System.out.println()` count |
|------|----------------------------:|
| Databean_report.java | 54 |
| Databean_dyn_reports.java | 32 |
| LinderReportDatabean.java | 17 |
| Databean_reports.java | 8 |
| Databean_cdisp.java | 6 |
| RTLSImpactReport.java | 4 |
| Databean_report1.java | 4 |
| RTLSHeatMapReport.java | 1 |
| **Total** | **126** |

System.out.println is used for error reporting, query logging, and exception output. These go to stdout/stderr rather than structured log files, making production debugging extremely difficult.

---

## CQ-07 Resource Leaks

### Finding CQ-07-A: `FileOutputStream` not wrapped in try-with-resources

**Severity:** HIGH
**Files:**
- `ReportPDF.java`, line 62: `writer = PdfWriter.getInstance(document, new FileOutputStream(result));`
- `MonthlyPDFRpt.java`, line 36: Same pattern.

The `FileOutputStream` is created inline and never explicitly closed. If `PdfWriter.getInstance()` or subsequent operations throw, the stream leaks.

### Finding CQ-07-B: Instance-level JDBC resources shared across methods

**Severity:** HIGH
**Files:** `Databean_report.java`, `Databean_dyn_reports.java`, `Databean_cdisp.java`, `Databean_report1.java`, `LinderReportDatabean.java`
**Evidence:**
- `Databean_report.java` lines 81-92: declares `Connection conn`, `Statement stmt/stmt1/stmt2/stmt3/stmt4`, `ResultSet rset/rset1/rset2/rset3/rset4` as instance fields.
- Same pattern in all other Databean classes.
- These are shared across multiple private methods called from `init()`. If any method re-assigns `rset` before it is closed, the previous result set leaks.
- The `finally` block in `init()` only closes the last assignment to each field -- intermediate ResultSet assignments in called methods are not individually closed.
- None of these classes use try-with-resources.

### Finding CQ-07-C: `RTLSHeatMapReport` / `RTLSImpactReport` -- N+1 connection pattern

**Severity:** MODERATE
**Files:** `RTLSHeatMapReport.java` (lines 49-124), `RTLSImpactReport.java` (multiple methods)
**Evidence:** These classes open a new `Connection` in each method (via `DBUtil.getConnection()` or `DBUtil.getMySqlConnection()`), then iterate in a for-loop issuing queries per vehicle/session. The connection is properly closed in `finally`, but each method acquires and releases its own connection. Multiple methods called in sequence (e.g., `getPointsJson()` calls `getVehSession()`, `getSessionPoints()`, `addWeight()`, `getOrigin()`, `createJSON()`) each open separate connections.

---

## CQ-08 SQL Injection Vulnerabilities

### Finding CQ-08-A: Pervasive string-concatenated SQL queries (CRITICAL)

**Severity:** CRITICAL
**Aggregate counts of SQL concatenation with user-controlled variables:**

| File | Concatenated query count |
|------|------------------------:|
| Databean_report.java | 89 |
| Databean_dyn_reports.java | 30 |
| Databean_cdisp.java | 8 |
| LinderReportDatabean.java | 8 |
| Databean_report1.java | 2 |
| **Total** | **137** |

**Evidence (examples):**
- `Databean_report1.java`, line 154: `query="select \"USER_CD\" from \"FMS_USR_GRP_REL\" where \"GROUP_CD\"='"+set_gp_cd+"'"` -- direct string concat with user input.
- `Databean_report1.java`, lines 242-246: Full query with `set_user_cd`, `st_dt`, `end_dt` concatenated.
- `Databean_dyn_reports.java`, line 349: `query = "select \"LOC_CD\" from \"FMS_USR_CUST_REL\" where \"USER_CD\" = '"+set_cust_cd+"'"`.
- `Databean_report.java`: Every `Fetch_*` method uses string concatenation with `set_cust_cd`, `set_loc_cd`, `set_dept_cd`, `st_dt`, `end_dt`, etc.

**ZERO** PreparedStatement usages found in `Databean_report.java` or `Databean_dyn_reports.java` (0 matches for `PreparedStatement`). `RTLSHeatMapReport.java` and `RTLSImpactReport.java` correctly use PreparedStatement throughout.

### Finding CQ-08-B: Reports.java uses string concatenation with Statement

**Severity:** HIGH
**File:** `Reports.java`
**Evidence:**
- Line 63: `query += " where \"USER_CD\" = " + access_cust;` -- no quotes around value.
- Line 124: `" where ... \"USER_CD\" = "+set_cust_cd` -- concatenated into query.
- Line 276: `"where \"USER_CD\" = '"+set_cust_cd+"'"` -- all queries in `Fetch_customers()`, `Fetch_cust_locations()`, `Fetch_cust_depts()`, `Fetch_cust_veh()` use concatenation.

---

## CQ-09 N+1 Query Patterns

### Finding CQ-09-A: Loop-based queries in RTLSHeatMapReport

**Severity:** HIGH
**File:** `RTLSHeatMapReport.java`, lines 65-87
**Evidence:** `getPoints()` iterates over `arrSession` in a for-loop (line 65), executing a separate SQL query per session:
```java
for(int i = 0; i< arrSession.size(); i++) {
    // ...
    stmt = conn.prepareStatement(query);
    rset = stmt.executeQuery();
}
```
Same pattern in `getSessionPoints()` (lines 143-170) and `getVehSession()` (lines 294-343).

### Finding CQ-09-B: Loop-based queries in RTLSImpactReport

**Severity:** HIGH
**File:** `RTLSImpactReport.java`, lines 319-330
**Evidence:** `save_impact_points()` inserts records one at a time in a loop:
```java
for(int i=0;i< arrPoints.size();i++) {
    stmt = conn.prepareStatement(query);
    stmt.executeUpdate();
}
```
Same pattern in `saveSpeed()` (lines 436-446). These could use batch inserts.

### Finding CQ-09-C: Loop-based queries in Databean_dyn_reports

**Severity:** HIGH
**File:** `Databean_dyn_reports.java`, lines 657-831 (`fetchDriverLeagueDetails()`)
**Evidence:** The outer while loop iterates over drivers (line 643), and for each driver executes 4+ separate queries (`rset1`, `rset2`) to fetch vehicle data, impact counts, duration, and pre-op check times. This is a classic N+1 pattern, potentially issuing hundreds of queries for large driver sets.

---

## CQ-10 Code Duplication

### Finding CQ-10-A: Duplicated JNDI connection boilerplate in every Databean class

**Severity:** HIGH
**Files:** `Databean_report.java` (line 18511), `Databean_dyn_reports.java` (line 7767), `Databean_cdisp.java` (line 1264), `Databean_report1.java` (line 394), `LinderReportDatabean.java` (line 63)
**Evidence:** Every class contains an identical `init()` pattern:
```java
InitialContext initialcontext = new InitialContext();
if(initialcontext == null) throw new Exception("Boom - No Context");
Context context = (Context)initialcontext.lookup("java:/comp/env");
DataSource datasource = (DataSource)context.lookup(RuntimeConf.penom_database);
if(datasource != null) {
    conn = datasource.getConnection();
    if(conn != null) { stmt = conn.createStatement(); ... }
}
```
This connection-acquisition logic is copy-pasted across all 5 classes, each with identical finally blocks for resource cleanup.

### Finding CQ-10-B: Duplicated resource-cleanup boilerplate (JDBC close pattern)

**Severity:** HIGH
**Files:** All reports classes
**Evidence:** The following pattern is duplicated in every method of `RTLSHeatMapReport.java` (7 times), `RTLSImpactReport.java` (14 times), and `Reports.java` (5 times):
```java
if (rset != null) { try { rset.close(); } catch (SQLException e) { e.printStackTrace(); } }
if (stmt != null) { try { stmt.close(); } catch (SQLException e) { e.printStackTrace(); } }
if (conn != null) { try { conn.close(); } catch (SQLException e) { e.printStackTrace(); } }
```
This represents ~400 lines of duplicated code across the RTLS and Reports classes alone. Try-with-resources would eliminate all of it.

### Finding CQ-10-C: Duplicated Fetch_cust_locations methods

**Severity:** MODERATE
**File:** `Databean_dyn_reports.java`
**Evidence:** Two nearly identical methods exist:
- `Fetch_cust_locations()` (line 336) -- with access-level filtering
- `fetchCustLocations()` (line 393) -- without access-level filtering

Similarly, `Fetch_vehicle_types1()` (line 310) and `fetchVehicleTypes()` (line 442) are near-duplicates.

### Finding CQ-10-D: Duplicated opcode dispatch boilerplate in init() methods

**Severity:** MODERATE
**Files:** `Databean_report.java` (lines 18534-19310+), `Databean_dyn_reports.java` (lines 7789-8186)
**Evidence:** Both init() methods contain repeated if-blocks that follow the same structural pattern:
```java
if (set_opcode.equalsIgnoreCase("...")) {
    Fetch_division();
    Fetch_group_customers();
    if (set_cust_cd.equalsIgnoreCase("0")) { ... }
    else {
        if (set_cust_cd.equalsIgnoreCase("") && user_cd.size() > 0) { set_cust_cd = ...; }
        if (!set_cust_cd.equalsIgnoreCase("")) {
            Fetch_cust_locations();
            if (...) { Fetch_cust_dept(); }
        }
        ...
    }
}
```
This boilerplate is repeated 40+ times in `Databean_report.java` and 20+ times in `Databean_dyn_reports.java`.

---

## CQ-11 Dead Code

### Finding CQ-11-A: `Databean_reports.java` -- effectively dead class

**Severity:** HIGH
**File:** `Databean_reports.java` (128 lines)
**Evidence:** The entire `query()` method body is commented out (lines 52-125). The `clearVectors()` method at line 49 is empty. The class declares fields (`stmt1`, `stmt3`, `rset1`, `rset3`, multiple ArrayLists) that are never used since the only executable method is empty.

### Finding CQ-11-B: `ReportPDF.createList()` -- unreachable method

**Severity:** LOW
**File:** `ReportPDF.java`, lines 131-137
**Evidence:** The `createList(Section subCatPart)` method is a boilerplate example with hardcoded "First point", "Second point", "Third point" items. It is `protected` but never called from `ReportPDF` or its subclass `MonthlyPDFRpt`. The related `Section` and `List` imports are also unused.

### Finding CQ-11-C: `ReportPDF.createTable()` -- dead boilerplate method

**Severity:** LOW
**File:** `ReportPDF.java`, lines 81-100
**Evidence:** The `createTable()` method in the base class creates a sample table with "Cell with colspan 3" / "Cell with rowspan 2" placeholder content. This is template/example code from iText documentation, never intended for production. The subclass `MonthlyPDFRpt` overrides `addContent()` to use its own table creation.

### Finding CQ-11-D: Stale Javadoc in ReportPDF

**Severity:** LOW
**File:** `ReportPDF.java`, lines 55-60
**Evidence:** The Javadoc for `createPdf()` states "Creates a PDF with information about the movies" -- a leftover from iText sample code, irrelevant to fleet management.

---

## CQ-12 Layering Violations

### Finding CQ-12-A: Direct JNDI lookups and SQL in JSP-facing beans

**Severity:** HIGH
**Files:** All Databean classes (`Databean_report.java`, `Databean_dyn_reports.java`, `Databean_cdisp.java`, `Databean_report1.java`, `LinderReportDatabean.java`), `Reports.java`
**Evidence:** These classes are designed to be used as JSP beans (each has a public `init()` method described as "Function called from the jsp page" and an `HttpServletRequest request` field). They directly perform:
1. JNDI lookups for DataSource
2. Raw SQL query construction and execution
3. Business logic (impact level calculations, time conversions, chart generation)
4. Data formatting for display

This violates separation of concerns. Presentation-tier beans should not contain data-access logic. A proper DAO/service layer is absent for these report classes, although DAOs exist elsewhere in the codebase (`UnitDAO`, `PreCheckDAO`, `ImpactDAO`, `BatteryDAO` are imported by `Databean_report.java`).

### Finding CQ-12-B: PDF generation class calls DAO directly

**Severity:** MODERATE
**File:** `MonthlyPDFRpt.java`, lines 82-85, 126-133
**Evidence:**
- Line 82: `UnitDAO unitDAO = new UnitDAO();` -- creates DAO instance directly in `addTitlePage()`.
- Line 126: `PreCheckDAO preCheckDAO = new PreCheckDAO();` -- creates DAO instance directly in `createTable()`.

The PDF generation layer directly instantiates DAO objects instead of receiving data through a service layer.

---

## CQ-13 Raw Types / Missing Generics

### Finding CQ-13-A: Pervasive use of raw ArrayList types

**Severity:** MODERATE
**Files:** `Databean_report.java`, `Databean_dyn_reports.java`, `Databean_cdisp.java`, `Databean_report1.java`, `Databean_reports.java`, `LinderReportDatabean.java`, `UtilModelBean.java`
**Evidence:**
- `Databean_report.java`: ~409 raw `ArrayList` declarations (e.g., `ArrayList group_cd = new ArrayList();` at line 163).
- `Databean_dyn_reports.java`: ~160+ raw `ArrayList` declarations (lines 88-186).
- `Databean_report1.java`: ~24 raw `ArrayList` declarations (lines 37-66).
- `UtilModelBean.java`, line 20: `private ArrayList ub = new ArrayList();`

Raw types bypass compile-time type checking and require unsafe casts at usage sites.

---

## CQ-14 Miscellaneous Issues

### Finding CQ-14-A: Hardcoded path traversal in ReportPDF.getExportDir()

**Severity:** HIGH
**File:** `ReportPDF.java`, lines 166-174
**Evidence:**
```java
dir +="/../../../../../../../excelrpt/";;
```
This uses 7 levels of `../` traversal to locate the export directory from the classfile location. This is fragile, environment-dependent, and the double semicolon `;;` at line 172 indicates careless editing.

### Finding CQ-14-B: Static Calendar field access via instance reference

**Severity:** LOW
**File:** `MonthlyPDFRpt.java`, line 74
**Evidence:** `cal.get(cal.MONTH)` and `cal.get(cal.YEAR)` -- accessing static `Calendar.MONTH` and `Calendar.YEAR` fields through instance reference. Should be `Calendar.MONTH` and `Calendar.YEAR`.

Same issue in `ReportPDF.java`, line 123: `cal.get(cal.YEAR)`.

### Finding CQ-14-C: Typo in exception message

**Severity:** LOW
**File:** `Databean_report.java`, line 18517; `Databean_dyn_reports.java`, line 7773; `Databean_report1.java`, line 401
**Evidence:** `throw new Exception("Boom - No Context");` -- unprofessional exception message used in production code. This string appears in all three files identically.

### Finding CQ-14-D: Copyright character encoding issue

**Severity:** LOW
**File:** `ReportPDF.java`, line 123
**Evidence:** `"Copyright � "` -- the copyright symbol is mangled, likely an encoding issue with the `(C)` character.

---

## Summary Statistics

| Check | Instances | Severity |
|-------|----------:|----------|
| CQ-01 God classes | 4 classes (21.8k + 10k + 1.9k + 1.7k lines) | CRITICAL / HIGH |
| CQ-02 Naming violations | 5 classes + ~100s methods | MODERATE |
| CQ-03 Commented-out code | ~175+ instances across 5 files | HIGH |
| CQ-04 Unused/wildcard imports | 3 wildcard + ~4 unused | MODERATE / LOW |
| CQ-05 Broad catches | 67 `catch(Exception)` blocks | HIGH |
| CQ-06 `printStackTrace()` | 124 instances across 8 files | HIGH |
| CQ-06b `System.out.println()` | 126 instances across 8 files | HIGH |
| CQ-07 Resource leaks | 2 FileOutputStream + 5 classes with shared JDBC | HIGH |
| CQ-08 SQL injection | ~137 concatenated queries, 0 PreparedStatement in Databeans | CRITICAL |
| CQ-09 N+1 queries | 5 distinct for-loop query patterns | HIGH |
| CQ-10 Code duplication | JNDI boilerplate x5, cleanup x26+, dispatch x60+ | HIGH |
| CQ-11 Dead code | 1 dead class + 3 dead methods | HIGH / LOW |
| CQ-12 Layering violations | All Databean classes + MonthlyPDFRpt | HIGH |
| CQ-13 Raw types | ~600+ raw ArrayList declarations | MODERATE |
| CQ-14 Miscellaneous | Path traversal, encoding, typos | HIGH / LOW |

**Overall risk assessment:** This module represents the highest-risk code in the codebase from a code quality perspective. The Databean_report.java class at 21,854 lines is an extreme God class with pervasive SQL injection vulnerabilities, no separation of concerns, and no use of parameterized queries. Immediate remediation priorities should be: (1) SQL injection via PreparedStatement migration, (2) God class decomposition, (3) proper logging framework usage.
