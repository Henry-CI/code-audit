# Security Audit Report — Excel / PDF / Chart Java Packages
**Audit ID:** A09
**Run:** 2026-02-25-01
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Date:** 2026-02-25
**Auditor:** Agent A09

---

## Scope

Packages audited:

| Package path | Files read |
|---|---|
| `WEB-INF/src/com/torrent/surat/fms6/excel/` | 11 Java files |
| `WEB-INF/src/com/torrent/surat/fms6/excel/reports/` | 49 Java files |
| `WEB-INF/src/com/torrent/surat/fms6/excel/reports/beans/` | 18 Java files |
| `WEB-INF/src/com/torrent/surat/fms6/excel/reports/dao/` | 2 Java files |
| `WEB-INF/src/com/torrent/surat/fms6/pdf/` | 2 Java files |
| `WEB-INF/src/com/torrent/surat/fms6/chart/` | 8 Java files |
| `WEB-INF/src/com/torrent/surat/fms6/chart/excel/` | 14 Java files |

---

## Step 3 — Class and Member Inventory (Selected Key Classes)

### `com.torrent.surat.fms6.excel.reports.dao.CustomerDAO`
**File:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/dao/CustomerDAO.java`

Imports: `java.sql.Connection`, `java.sql.ResultSet`, `java.sql.SQLException`, `java.sql.Statement`, `java.util.ArrayList`, `com.torrent.surat.fms6.util.DBUtil`, `com.torrent.surat.fms6.util.RuntimeConf`

Fields: none (stateless utility class)

Public methods:
- `String getCustomerName(String cust_cd)` — line 17
- `String getLocationName(String loc_cd)` — line 55
- `String getDepartmentName(String dept_cd)` — line 92
- `String getModelName(String model_cd)` — line 129
- `String getFormName(String form_cd)` — line 165

---

### `com.torrent.surat.fms6.excel.reports.dao.DriverAccessAbuseDAO`
**File:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/dao/DriverAccessAbuseDAO.java`

Imports: `java.sql.Connection`, `java.sql.ResultSet`, `java.sql.SQLException`, `java.sql.Statement`, `java.util.ArrayList`, `java.util.Collections`, `java.util.StringTokenizer` (duplicate `java.util.ArrayList` import — flag), `com.torrent.surat.fms6.excel.reports.beans.DriverAccessAbuseBean`, `com.torrent.surat.fms6.reports.Databean_report`, `com.torrent.surat.fms6.util.DBUtil`

Fields (package-private, raw `ArrayList` — no generics): `a_driv_cd`, `a_driv_nm`, `a_driv_id`, `a_veh_cd`, `a_veh_nm`, `a_veh_typ_cd`, `a_veh_typ_nm`, `a_veh_srno`, `a_st_tm`, `a_end_tm`, `a_date`, `a_ol_start_list`, `a_ol_end_list`

Public methods:
- `DriverAccessAbuseBean getAbuseBean(String set_cust_cd, String set_loc_cd, String set_dept_cd, String st_dt, String end_dt, String report_filter, String a_time_filter)` — line 33

---

### `com.torrent.surat.fms6.chart.excel.ChartsExcelDao`
**File:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartsExcelDao.java`

Imports: `java.sql.Connection`, `java.sql.ResultSet`, `java.sql.SQLException`, `java.sql.Statement`, `java.util.ArrayList`, `java.util.StringTokenizer`, `com.torrent.surat.fms6.bean.EntityBean`, `com.torrent.surat.fms6.bean.ImpactBean`, `com.torrent.surat.fms6.dao.UnitDAO`, `com.torrent.surat.fms6.master.FirmwareverBean`, `com.torrent.surat.fms6.util.DBUtil`, `com.torrent.surat.fms6.util.LindeConfig`, `com.torrent.surat.fms6.util.RuntimeConf`

Public methods:
- `String getFromDate()` — line 24
- `ArrayList<ChartMailListBean> getEmailList(String custCd, String locCd)` — line 58
- `ArrayList<CustLocBean> getCustLoc()` — line 97
- `String getAllLocations(String custCd)` — line 133
- `String getCurrDate()` — line 172
- `ArrayList<UnlockBean> getMachineUnlock(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept, String st_dt, String end_dt)` — line 207
- `ArrayList<ImpactBean> getImpacts(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept)` — line 329
- `ArrayList<UnitUtilBean> getUnitUtilisationByHour(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept, String st_dt, String end_dt)` — line 404
- `ArrayList<UnitUtilBean> getUnitUtilisationByHour(String cust_cd, String loc_cd, String st_dt, String end_dt)` — line 552
- `ArrayList<UnitUtilBean> getUnitUtilisationByHour(String cust_cd, String loc_cd, String dept_cd, String st_dt, String end_dt)` — line 693
- `ArrayList<PreopFailBean> getPreopFail(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept, String st_dt, String end_dt)` — line 849
- `ArrayList<DriverAccessAbuseBean> getAccessAbuse(String cust_cd, String loc_cd, ArrayList<EntityBean> arrDept, String st_dt, String end_dt)` — line 970

---

### `com.torrent.surat.fms6.pdf.ReportPDF`
**File:** `WEB-INF/src/com/torrent/surat/fms6/pdf/ReportPDF.java`

Imports: `java.io.File`, `java.io.FileOutputStream`, `java.io.IOException`, `java.sql.SQLException`, `java.util.Calendar`, iText library (`com.itextpdf.text.*`, `com.itextpdf.text.pdf.*`), `com.torrent.surat.fms6.util.DataUtil`, `com.torrent.surat.fms6.util.RuntimeConf`

Fields (protected): `String result`, `String title`, `String from`, `String to`, `String month`, `String cust_cd`, `String loc_cd`, `String dept_cd`, `String pdfurl`, `Document document`, `PdfWriter writer`, static Font fields (`catFont`, `redFont`, `subFont`, `hrFont`, `hdFont`, `smallBold`)

Public methods:
- `ReportPDF(String cust_cd, String loc_cd, String dept_cd, String month, String st_dt, String end_dt)` constructor — line 45
- `String createPdf()` — line 61
- `String getPdfurl()` — line 178
- `void setPdfurl(String pdfurl)` — line 182
- `String getResult()` — line 187
- `void setResult(String result)` — line 191
- `String getTitle()` — line 195
- `void setTitle(String title)` — line 199
- `String getFrom()` — line 203
- `void setFrom(String from)` — line 207
- `String getTo()` — line 211
- `void setTo(String to)` — line 215
- `String getMonth()` — line 219
- `void setMonth(String month)` — line 223
- `Document getDocument()` — line 227
- `void setDocument(Document document)` — line 231

---

### `com.torrent.surat.fms6.pdf.MonthlyPDFRpt`
**File:** `WEB-INF/src/com/torrent/surat/fms6/pdf/MonthlyPDFRpt.java`

Imports: `java.io.FileOutputStream`, `java.io.IOException`, `java.sql.SQLException`, `java.util.ArrayList`, `java.util.Calendar`, iText library, `com.torrent.surat.fms6.bean.FleetCheckBean`, `com.torrent.surat.fms6.dao.PreCheckDAO`, `com.torrent.surat.fms6.dao.UnitDAO`, `com.torrent.surat.fms6.util.DataUtil`

Extends: `ReportPDF`

Public methods:
- `MonthlyPDFRpt(String cust_cd, String loc_cd, String dept_cd, String set_month, String st_dt, String end_dt)` constructor — line 27
- `String createPdf()` — line 35

---

### `com.torrent.surat.fms6.excel.Frm_excel`
**File:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_excel.java`

No wildcard imports. Imports include Apache POI, Batik SVG transcoder, standard Java I/O and SQL, and application utilities.

Fields (protected): `String result`, `String fileName`, `String title`, `String docroot`, `String imageroot`, `String from`, `String to`, `String cust_cd`, `String loc_cd`, `String dept_cd`, `ArrayList deptCdArrayList` (raw type), `int currentRow`, `MailBase mb`, `Workbook wb`, `Map<String, CellStyle> styles`, `String[] params`, `String argS`, `String rpt_name`, `String cust_prefix`

Notable method: `setTotalDuration(String totalDuration, Cell contentCell, String style)` at line 925 uses `setCellFormula("VALUE(\""+totalDuration+"\")")`.

---

## Step 4 — Security Review

---

## Findings

---

### A09-1 — SQL Injection in CustomerDAO: Unparameterized String Concatenation

**File:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/dao/CustomerDAO.java`
**Lines:** 32, 70, 107, 144, 180–181
**Severity:** CRITICAL
**Category:** SQL Injection (CWE-89)

**Description:**

`CustomerDAO` contains five methods that construct SQL queries by direct string concatenation of caller-supplied parameters. All five use `Statement.executeQuery()` (a `java.sql.Statement`, not a `PreparedStatement`), so there is no parameterisation defence. An attacker who controls the relevant parameter can terminate the intended query and inject arbitrary SQL.

**Evidence — getCustomerName() line 32:**
```java
String sql = "select \"USER_NAME\" from \"FMS_CUST_MST\" where \"USER_CD\" = " + cust_cd;
rs=stmt.executeQuery(sql);
```
`cust_cd` is supplied directly from the caller (ultimately from a web request parameter). No quoting, casting, or validation restricts the value.

**Evidence — getLocationName() line 70:**
```java
String sql = "select \"NAME\" from \"FMS_LOC_MST\" where \"LOCATION_CD\" = " + loc_cd;
```

**Evidence — getDepartmentName() line 107:**
```java
String sql = "select \"DEPT_NAME\" from \"FMS_DEPT_MST\" where \"DEPT_CD\" = " + dept_cd;
```

**Evidence — getModelName() line 144:**
```java
String sql = "select \"VEHICLE_TYPE\" from \"FMS_VEHICLE_TYPE_MST\" where \"VEHICLE_TYPE_CD\" = " + model_cd;
```

**Evidence — getFormName() lines 180–181:**
```java
String query = "select \"FORM_NAME\"  from "+RuntimeConf.form_table+" where \"FORM_CD\"='"
        + form_cd + "' ";
```
Note: `form_table` is a server-side constant (lower risk for table-name injection), but `form_cd` is still concatenated without parameterisation.

**Recommendation:**
Replace all five `Statement` objects with `PreparedStatement`. Example for `getCustomerName`:
```java
String sql = "select \"USER_NAME\" from \"FMS_CUST_MST\" where \"USER_CD\" = ?";
PreparedStatement pstmt = conn.prepareStatement(sql);
pstmt.setString(1, cust_cd);
rs = pstmt.executeQuery();
```
The check `!cust_cd.equalsIgnoreCase("0")` provides no injection protection because it only filters the literal string "0", not SQL metacharacters.

---

### A09-2 — SQL Injection in ChartsExcelDao: Multiple Concatenated Queries

**File:** `WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartsExcelDao.java`
**Lines (representative):** 71, 145, 229, 250, 437–442, 465–466, 490–492, 498–500, 506–512, 583, 607–608, 632–634, 640–643, 648–654, 711–712, 735, 750, 763–764, 788–790, 796–799, 804–810
**Severity:** CRITICAL
**Category:** SQL Injection (CWE-89)

**Description:**

`ChartsExcelDao` is the primary data-access class for chart-generation. It uses `java.sql.Statement` exclusively throughout its 1 100+ line body and concatenates every user-supplied parameter directly into SQL strings. Parameters include `custCd`, `locCd`, `cust_cd`, `loc_cd`, `dept_cd`, `st_dt`, `end_dt`, and derived intermediate values (`tmp_cd`, `fld_cd`).

**Evidence — getEmailList() line 71:**
```java
String sql = "select user_cd,cust_cd,loc_cd,\"EMAIL_ADDR\" from "
    + LindeConfig.subscriptionTable
    + " inner join \"FMS_USR_MST\" on \"USER_CD\"=user_cd "
    + "where cust_cd="+custCd + " and loc_cd='" + locCd +"';";
```
Both `custCd` and `locCd` are injected without parameterisation. An attacker supplying `custCd = "1 OR 1=1"` would retrieve all subscription records.

**Evidence — getAllLocations() line 145:**
```java
String sql = "select \"LOC_CD\" from \"FMS_USR_CUST_REL\" where \"USER_CD\"=" + custCd+"";
```

**Evidence — getUnitUtilisationByHour() (three overloads), date arithmetic injection, lines 465–466:**
```java
sql = "select to_date('" + end_dt + "','dd/mm/yyyy') - to_date('"
    + st_dt + "','dd/mm/yyyy') +1";
```
`st_dt` and `end_dt` are report parameters flowing in directly from web request. Supplying `end_dt = "01/01/2025') OR '1'='1"` would alter the query.

**Evidence — inner loop timestamp construction, lines 490–492:**
```java
sql = "select to_date('" + st_dt
    + "','dd/mm/yyyy') + interval '" + i
    + " days' + interval '" + j + " hours'";
```
Here `i` and `j` are loop counters (integer, safe), but `st_dt` is still user-controlled string.

**Evidence — getMachineUnlock() / getPreopFail() / getAccessAbuse() — dynamic WHERE construction, lines 229–250:**
```java
cond_cust = " \"USER_CD\" = '" + cust_cd + "'";
cond_site = " and \"LOC_CD\" = '" + loc_cd + "'";
cond_dept = " and \"DEPT_CD\" = '" + bean.getId() + "'";
sql = "select \"VEHICLE_CD\" from \"FMS_USR_VEHICLE_REL\" where " + cond_cust + cond_site + cond_dept;
```
The three filter fragments are assembled without parameterisation. An attacker controlling `cust_cd` can close the single-quote, add `OR 1=1 --`, and expand the result set to all vehicles on the system.

**Evidence — getPreopFail() checklist answer query, lines 931–932:**
```java
query = "select question_text, answer, expectedanswer from op_chk_checklistanswer where checklist_result_id = '"
    + tmp_res_id + "'";
```
`tmp_res_id` originates from a previous ResultSet column but is inserted verbatim into the next query — a second-order injection vector if checklist result IDs themselves can be manipulated.

**Recommendation:**
Migrate all queries to `PreparedStatement` with `?` placeholders. For `IN (...)` clauses built from a list (e.g., `tmp_cd`), use a helper that builds `IN (?,?,?)` and calls `setString` in a loop, or use an application-level allowlist that accepts only integer vehicle codes.

---

### A09-3 — Broken Object-Level Authorization: No Customer Isolation Check in Report Export Layer

**Files:**
- `WEB-INF/src/com/torrent/surat/fms6/excel/reports/dao/CustomerDAO.java`
- `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_excel.java`
- `WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelBatteryReport.java` (representative of all 30+ Excel report classes)
- `WEB-INF/src/com/torrent/surat/fms6/chart/excel/ChartsExcelDao.java`

**Severity:** CRITICAL
**Category:** Broken Object-Level Authorization / IDOR (CWE-639, OWASP A01)

**Description:**

No class in the excel, excel/reports, chart, or pdf packages verifies that the authenticated user's session `customer_id` matches the `cust_cd` parameter used to scope the data query. The parameter flows directly from the web layer through `Frm_excel` constructors and into DAO calls without any cross-check against session state.

**Evidence — Frm_excel constructor, lines 91–100:**
```java
public Frm_excel(String cust_cd,String loc_cd,String dept_cd,String from, String to, String docRoot){
    this.cust_cd = cust_cd;
    this.loc_cd = loc_cd;
    this.dept_cd = dept_cd.equalsIgnoreCase("0")?"":dept_cd;
    ...
}
```
`cust_cd` is accepted as a plain constructor argument — no session validation.

**Evidence — ChartsExcelDao.getEmailList():**
```java
public ArrayList<ChartMailListBean> getEmailList(String custCd, String locCd)
```
`custCd` is accepted as a parameter with no verification that it belongs to the calling user.

**Evidence — Frm_unitSummary_rpt and Frm_simSwap_rpt:**
These two classes (admin-level unit summary and SIM swap reports) accept `super()` with no `cust_cd` and call `unitDAO.getUnitSummary()` / `unitDAO.getSimSwapSummary()` with no customer scoping at all, returning fleet-wide data.

**Impact:**
A regular customer user who can modify the `cust_cd` POST parameter on any report export endpoint can download another customer's fleet data (impact events, driver activity, SIM card details, vehicle serial numbers). This is a classic IDOR in a data-export context — explicitly flagged as high-risk in the audit checklist.

**Recommendation:**
1. The HTTP servlet/controller that invokes these report classes must read `cust_cd` exclusively from the authenticated session (e.g., `request.getSession().getAttribute("cust_cd")`) and never from a user-supplied parameter.
2. A server-side guard method should verify that the requested `cust_cd` / `loc_cd` / `dept_cd` combination appears in the authenticated user's access rights table before any SQL is executed.
3. Admin-only reports (`Frm_unitSummary_rpt`, `Frm_simSwap_rpt`) must enforce a role check before construction.

---

### A09-4 — Path Traversal in Output File Naming via form_cd Parameter

**File:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_excel.java`
**Lines:** 159–162
**Severity:** HIGH
**Category:** Path Traversal (CWE-22)

**Description:**

The `setParameters()` method constructs the output file name from the `form_cd` parameter by looking up the form name in the database via `CustomerDAO.getFormName()`, then using that name as the `.xlsx` filename:

```java
rpt_name = dao.getFormName(getParam("form_cd"));
this.title = rpt_name;
this.fileName = rpt_name.replace(" ", "")+".xlsx";
this.result = this.docroot+ this.fileName;
```

`getFormName()` in `CustomerDAO` queries `FMS_FORM_MST` using `form_cd` with SQL concatenation (see A09-1). If an attacker injects SQL that causes `getFormName()` to return a path-containing string such as `../../webapps/ROOT/evil`, the resulting `result` path becomes:

```
[docroot]/../../webapps/ROOT/evil.xlsx
```

The `FileOutputStream(result)` call at line 203 of `createExcel()` would then write the workbook to the attacker-chosen path.

**Evidence:**
```java
// CustomerDAO.java line 180-181 — form_cd injected, result controls file name
String query = "select \"FORM_NAME\"  from "+RuntimeConf.form_table+" where \"FORM_CD\"='"
    + form_cd + "' ";
...
// Frm_excel.java line 161-162
this.fileName = rpt_name.replace(" ", "")+".xlsx";
this.result = this.docroot+ this.fileName;
```

**Recommendation:**
1. Fix the SQL injection in `getFormName()` first (see A09-1), which closes the primary injection vector.
2. Independently validate `rpt_name` after the DB lookup: strip or reject any character that is not alphanumeric, space, hyphen, or underscore before constructing the file path.
3. Canonicalize `this.result` with `File.getCanonicalPath()` and assert that the canonical path starts with the expected `docroot` directory.

---

### A09-5 — Path Traversal Risk in MonthlyPDFRpt: Output Path Derived from cust_cd / loc_cd

**File:** `WEB-INF/src/com/torrent/surat/fms6/pdf/MonthlyPDFRpt.java`
**Lines:** 27–33
**Severity:** HIGH
**Category:** Path Traversal (CWE-22)

**Description:**

`MonthlyPDFRpt` constructs the chart file name on line 49 of `addContent()` by directly embedding `cust_cd`, `loc_cd`, and `dept_cd` into a filename:

```java
String chart_name = "Impactchart"+"_"+cust_cd+"_"+loc_cd+"_"+dept_cd+"_"+extra+".png";
fetch_chart(chart_name);
```

`fetch_chart()` calls `addImage(pdfurl+chart_name)`, which calls `Image.getInstance(image)` — resolving a file system path. If `cust_cd` or `loc_cd` contains `../`, the path resolves outside the intended chart directory. For example, `cust_cd = "../../../etc/passwd"` would cause the PDF renderer to open `/etc/passwd` as an image (the call would fail gracefully on a non-image, but the path resolution still occurs).

**Evidence:**
```java
// MonthlyPDFRpt.java lines 49-51
String chart_name = "Impactchart"+"_"+cust_cd+"_"+loc_cd+"_"+dept_cd+"_"+extra+".png";
fetch_chart(chart_name);
chart_name = "Usagechart"+"_"+cust_cd+"_"+loc_cd+"_"+dept_cd+"_"+extra+".png";
```

**Recommendation:**
Sanitise `cust_cd`, `loc_cd`, and `dept_cd` to contain only alphanumeric characters and hyphens before using them in any file path. Enforce a canonical path check to ensure the resolved path stays within the chart directory.

---

### A09-6 — XSS / HTML Injection in Email Report Bodies (MailBase)

**File:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/MailBase.java`
**Lines:** 26–60, 95–127
**Severity:** HIGH
**Category:** Cross-Site Scripting / HTML Injection in Email (CWE-80)

**Description:**

`MailBase.setMailHeader()` builds HTML email bodies by directly concatenating the parameters `st`, `et`, `cust`, `loc`, `dep`, `model`, and `rptName` into raw HTML without any HTML encoding or escaping. These values originate from customer name strings, location names, and date strings retrieved from the database:

```java
body += "... <td><b>" + cust + "</b> </td> ..."
      + "... <td><b>" + loc + "</b> </td> ..."
      + "... <td><b>" + dep + "</b> </td> ..."
      + "... <td><b>" + rptName + "</b> </td> ..."
```

If a customer, location, or department name in the database contains HTML metacharacters (e.g., a customer named `Widgets & Co. <script>alert(1)</script>`), those characters are injected verbatim into the HTML email body. Depending on the email client's rendering behaviour, this could allow script execution or visual spoofing in the email.

**Recommendation:**
HTML-encode all dynamic values before embedding them in HTML. Use a library method such as `org.apache.commons.text.StringEscapeUtils.escapeHtml4(value)` or `org.springframework.web.util.HtmlUtils.htmlEscape(value)` for each of `st`, `et`, `cust`, `loc`, `dep`, `model`, and `rptName`.

---

### A09-7 — Formula / CSV Injection via setCellFormula with User-Derived Duration String

**File:** `WEB-INF/src/com/torrent/surat/fms6/excel/Frm_excel.java`
**Lines:** 925–935
**Severity:** MEDIUM
**Category:** Formula Injection in Excel Output (CWE-1236)

**Description:**

The `setTotalDuration()` method constructs an Excel cell formula by embedding `totalDuration` (a string retrieved from database query results, ultimately derived from session data) directly into a formula string:

```java
contentCell.setCellFormula("VALUE(\""+totalDuration+"\")");
```

If `totalDuration` contains a double-quote character — for example a database value `23:59"` — the formula becomes `VALUE("23:59"")`, breaking the formula. More seriously, if the duration value can be controlled by an attacker and contains formula characters (`=`, `+`, `-`, `@`, a cell reference such as `A1`), it could turn into an active formula. While duration strings are typically in `HH:MM:SS` format and the immediate risk is low, the practice of embedding database-derived strings into Excel formulas without sanitisation is inherently unsafe.

**Evidence:**
```java
public void setTotalDuration(String totalDuration, Cell contentCell, String style){
    String[] durations = totalDuration.split(":");
    int hour = Integer.parseInt(durations[0]);
    if(hour > 10000){
        contentCell.setCellValue(totalDuration);  // safe path for large values
        ...
        return;
    }
    contentCell.setCellFormula("VALUE(\""+totalDuration+"\")");  // UNSAFE for <10000h
    contentCell.setCellValue(totalDuration);
    ...
}
```

**Recommendation:**
Validate `totalDuration` against a strict regex (e.g., `^[0-9]{1,5}:[0-5][0-9]:[0-5][0-9]$`) before constructing the formula. If validation fails, fall back to `setCellValue()` only. Do not embed arbitrary strings in Excel formula expressions.

---

### A09-8 — Resource Leak: XSSFWorkbook Never Closed Across All Report Classes

**Files:** All 70+ report generator files in `excel/` and `excel/reports/`
**Representative lines:** `Frm_excel.java` line 63; `ExcelBatteryReport.java` lines 36–40; all `Email*.java` and `Excel*.java` classes
**Severity:** MEDIUM
**Category:** Resource Management / Memory Leak (CWE-772)

**Description:**

`Frm_excel` declares the Apache POI workbook as an instance field:
```java
protected Workbook wb = new XSSFWorkbook();
```

Every report class writes the workbook with `wb.write(fileOut)` and closes `fileOut`, but none of the 70+ classes ever call `wb.close()`. The `XSSFWorkbook` implements `Closeable` and holds open package parts and temporary files on disk. Without calling `close()`, under high report-generation load, these leaked handles accumulate and can exhaust heap memory or file descriptors.

**Evidence:**
```java
// ExcelBatteryReport.java lines 36-40
FileOutputStream fileOut = new FileOutputStream(result);
wb.write(fileOut);
fileOut.close();
return result;
// wb.close() is never called
```

The same pattern repeats in every `createExcel()` / `createEmail()` / `createBody()` method across all report generator classes.

**Recommendation:**
Wrap workbook creation and write in a try-with-resources block:
```java
try (XSSFWorkbook wb = new XSSFWorkbook();
     FileOutputStream fileOut = new FileOutputStream(result)) {
    // ... build workbook ...
    wb.write(fileOut);
}
```
Because `wb` is currently a field rather than a local variable, it will require refactoring the base class constructor and `createExcel()` lifecycle. At minimum, add `wb.close()` in a `finally` block in each `createExcel()` method.

---

### A09-9 — No Runtime.exec() or ProcessBuilder in PDF Generation (Informational)

**Files:** `ReportPDF.java`, `MonthlyPDFRpt.java`
**Severity:** INFORMATIONAL
**Category:** Command Injection (CWE-78)

**Description:**

Both PDF generation classes use the iText library (`com.itextpdf.*`) natively within the JVM. No call to `Runtime.getRuntime().exec()`, `ProcessBuilder`, or any external process invocation was found in either file. The PDF audit checklist item for command injection in PDF rendering is therefore **not triggered** in this codebase.

---

### A09-10 — No Runtime.exec() or ProcessBuilder in Chart Generation (Informational)

**Files:** All files in `chart/` and `chart/excel/`
**Severity:** INFORMATIONAL
**Category:** Command Injection (CWE-78)

**Description:**

Chart generation uses JFreeChart and Apache POI natively. No external process invocations were found. The checklist item for command injection in chart generation is **not triggered**.

---

### A09-11 — Duplicate Import Statement in DriverAccessAbuseDAO (Code Quality)

**File:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/dao/DriverAccessAbuseDAO.java`
**Lines:** 7, 11
**Severity:** LOW
**Category:** Code Quality

**Description:**

```java
import java.util.ArrayList;   // line 7
...
import java.util.ArrayList;   // line 11 — duplicate
```

Not a security vulnerability, but indicates low code hygiene.

---

### A09-12 — Hardcoded HTTP URL in Email Report Body and Excel Report (Information Disclosure / Broken Link Risk)

**File:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/MailBase.java` (lines 13–25)
**File:** `WEB-INF/src/com/torrent/surat/fms6/excel/reports/ExcelImpactReport.java` (line 191)
**Severity:** LOW
**Category:** Information Disclosure / Configuration Hardcoding

**Description:**

Hardcoded production hostname and path appear in source:

```java
// MailBase.java line 13
"<link href=\"http://fleetfocus.lindemh.com.au/fms/css/alternate_rows.css\" ...>"

// ExcelImpactReport.java line 191
String tmp = "http://fleetfocus.lindemh.com.au/fms/"+ RuntimeConf.impactDir+"/"+img_link.get(j);
```

Using plain `http://` (not `https://`) for resource loading exposes email recipients to MITM attacks that could substitute CSS or images. Hardcoding the hostname prevents reuse across environments.

**Recommendation:**
Move hostnames to a configuration property. Use `https://` for all external URLs.

---

## Summary Table

| ID | File(s) | Severity | Category | Description |
|---|---|---|---|---|
| A09-1 | `CustomerDAO.java` | CRITICAL | SQL Injection | 5 methods concatenate user params into Statement queries |
| A09-2 | `ChartsExcelDao.java` | CRITICAL | SQL Injection | 10+ queries in chart DAO use Statement + string concat |
| A09-3 | All report classes, `Frm_excel.java` | CRITICAL | Broken Authorization / IDOR | No customer isolation check; cust_cd accepted from caller |
| A09-4 | `Frm_excel.java` + `CustomerDAO.java` | HIGH | Path Traversal | form_cd SQL injection can control output file path |
| A09-5 | `MonthlyPDFRpt.java` | HIGH | Path Traversal | cust_cd/loc_cd embedded in chart file path without sanitisation |
| A09-6 | `MailBase.java` | HIGH | HTML Injection in Email | Customer/location names embedded in HTML without encoding |
| A09-7 | `Frm_excel.java` | MEDIUM | Formula Injection | Duration string embedded in setCellFormula() without validation |
| A09-8 | All 70+ report classes | MEDIUM | Resource Leak | XSSFWorkbook never closed after write |
| A09-9 | `ReportPDF.java`, `MonthlyPDFRpt.java` | INFORMATIONAL | Command Injection | No external process invocation found — CLEAR |
| A09-10 | `chart/*.java` | INFORMATIONAL | Command Injection | No external process invocation found — CLEAR |
| A09-11 | `DriverAccessAbuseDAO.java` | LOW | Code Quality | Duplicate import statement |
| A09-12 | `MailBase.java`, `ExcelImpactReport.java` | LOW | Info Disclosure | Hardcoded HTTP production URL in source |

**Total findings: 12 (3 CRITICAL, 2 HIGH, 2 MEDIUM, 2 INFORMATIONAL, 2 LOW)**
