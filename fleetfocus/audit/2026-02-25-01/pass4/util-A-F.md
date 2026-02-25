# Pass 4 -- Code Quality Audit: util A-F (13 files)

**Audit ID:** A19
**Date:** 2026-02-25
**Scope:** `WEB-INF/src/com/torrent/surat/fms6/util/` -- BeanComparator, CftsAlert, CustomComparator, CustomUpload, DBUtil, DataUtil, DateUtil, DriverExpiryAlert, DriverMedicalAlert, Dt_Checker, EncryptTest, ExcelUtil, FleetCheckFTP

---

## Summary

| # | Check                        | Files Affected | Severity |
|---|------------------------------|---------------|----------|
| 1 | Naming convention violations | 3             | Medium   |
| 2 | Style inconsistency          | 10            | Low      |
| 3 | God classes                  | 2             | High     |
| 4 | Commented-out code           | 3             | Low      |
| 5 | Unused imports               | 2             | Low      |
| 6 | Empty / broad catches        | 10            | High     |
| 7 | e.printStackTrace()          | 11            | Medium   |
| 8 | Thread safety (static SDF)   | 1             | High     |
| 9 | Resource leaks               | 4             | High     |
| 10| Dead code                    | 3             | Medium   |
| 11| Magic numbers                | 5             | Medium   |
| 12| Hardcoded credentials / paths| 3             | Critical |
| 13| SQL injection                | 6             | Critical |
| 14| Raw types                    | 4             | Low      |
| 15| Misspelled identifiers       | 3             | Low      |
| 16| Broken leap-year logic       | 1             | High     |
| 17| Weak / home-rolled encryption| 1             | Critical |

---

## 1. Naming Convention Violations

### 1a. Dt_Checker.java -- Underscore in class name
- **File:** `Dt_Checker.java`
- **Line:** 4
- **Evidence:** `public class Dt_Checker`
- **Issue:** Class name uses underscore separator (`Dt_Checker`) instead of standard Java PascalCase (`DateChecker` or `DtChecker`). Additionally, the abbreviation "Dt" is opaque -- it presumably stands for "Date" but is not immediately obvious.

### 1b. EncryptTest.java -- Misleading name
- **File:** `EncryptTest.java`
- **Lines:** 1, 9
- **Evidence:** Header comment: `// Decompiled by DJ v3.9.9.91 Copyright 2005 Atanas Neshkov  Date: 1/25/2006 5:51:12 PM`; class: `public class EncryptTest`
- **Issue:** The name `EncryptTest` suggests a unit test, but this is a production encryption/decryption utility class. It should be named something like `EncryptUtil` or `CipherHelper`. The file is also noted as **decompiled** code committed to source control.

### 1c. Method naming inconsistencies across files
- **File:** `DataUtil.java` -- Lines 240, 509, 636: `generateRadomName` (typo: should be `generateRandomName`), `caculatePercentage` (typo: should be `calculatePercentage`), `caculateImpPercentage` (same typo).
- **File:** `DateUtil.java` -- Lines 250, 257: `GetDateNow()`, `GetDate()` use PascalCase instead of camelCase for methods; line 298 `GetCalendar()` same issue.
- **File:** `Dt_Checker.java` -- Line 178: `days_Betn` uses underscore and abbreviation.

---

## 2. Style Inconsistency

| File | Issue |
|------|-------|
| BeanComparator.java | Brace on new line (Allman style), consistent within file. |
| CftsAlert.java | Mixed brace placement: some K&R (`try{`), some Allman. Inconsistent indentation. |
| CustomUpload.java | Mixed brace styles; tabs and spaces mixed. |
| DataUtil.java | Extremely inconsistent indentation in `convert_time()` (lines 346-413) -- zero indentation inside nested blocks. |
| DateUtil.java | Mixed PascalCase/camelCase method names. Mixed brace styles. |
| Dt_Checker.java | Minimal indentation, no blank lines between methods, archaic style. |
| EncryptTest.java | Decompiled code style -- no meaningful variable names (`s`, `s1`, `c`). |
| FleetCheckFTP.java | Deeply nested code (5+ levels), inconsistent spacing. |
| ExcelUtil.java | Missing access modifiers on fields (lines 20-25: package-private). |
| DriverMedicalAlert.java | Consistent within file but uses different style from DriverExpiryAlert. |

---

## 3. God Classes

### 3a. DataUtil.java -- 1087 lines, 40+ methods
- **File:** `DataUtil.java`
- **Evidence:** Contains date formatting, HTML form helpers, math/array utilities, file I/O, image downloading, time conversion, percentage calculation, string manipulation, random generation, location filtering, and vehicle duration logic -- all in one class.
- **Impact:** Extremely high coupling. Any change risks breaking unrelated functionality. Class should be decomposed into domain-specific utilities (e.g., `HtmlFormUtil`, `MathUtil`, `FileUploadUtil`, `TimeConversionUtil`).

### 3b. CustomUpload.java -- Servlet + CSV parser + validation in one class
- **File:** `CustomUpload.java`
- **Lines:** 38-517
- **Evidence:** Single servlet class containing HTTP handling, CSV reading, 5 different CSV validation methods, file upload, email sending, database operations, firmware push, and GMTP ID lookup.
- **Impact:** Single Responsibility Principle violation. Methods `validateCSV`, `validateCSVIndividual`, `validateCSVIndividualD`, `validateCSVIndividualTab`, `validateQuestionLenght`, `validateQuestionLenghtTab` are never called within this file (see Dead Code section).

---

## 4. Commented-Out Code

| File | Lines | Evidence |
|------|-------|---------|
| CustomUpload.java | 76, 83, 117, 168, 385-386, 395, 938 | `//System.out.println("--->try...");`, `//System.out.println("---> r = "...`, `// System.out.println(headers);`, `// System.out.println(d);`, `//System.out.println("---> innerLst...`, `//System.out.println("---> ctr = "...`, `// String imgPath = ...` |
| DataUtil.java | 836-837 | Two blank lines after return statement inside `convertToImpPerc` -- dead unreachable block left behind. |
| FleetCheckFTP.java | 18-23 | Block comment explaining the code is **not called** by the stored procedure: `note as of March 10, 2023 testing, this is not being called by the store proc`. This suggests the entire class may be dead code. |

---

## 5. Unused Imports

| File | Line | Import |
|------|------|--------|
| DataUtil.java | 37 | `import java.util.ArrayList;` -- duplicate of line 17. |
| Dt_Checker.java | 2 | `import java.lang.*;` -- `java.lang` is always implicitly imported. |

---

## 6. Empty / Broad Exception Catches

### catch(Exception e) -- overly broad

| File | Lines | Context |
|------|-------|---------|
| CftsAlert.java | 217-221 | `catch(Exception e) { e.printStackTrace(); e.getMessage(); }` -- catches all exceptions, calls `e.getMessage()` with no variable capture (dead call). |
| CftsAlert.java | 264-268 | Same pattern in `getAlertlist()`. |
| CftsAlert.java | 307-311 | Same pattern in `getCustGroupList()`. |
| CustomUpload.java | 252-257 | `catch (Exception e) { e.printStackTrace(); System.out.println("---> e = " + e); }` |
| CustomUpload.java | 294 | `catch (SQLException e) { // TODO Auto-generated catch block  e.printStackTrace(); }` -- explicit TODO left in. |
| DriverExpiryAlert.java | 150-154 | `catch(Exception e) { e.printStackTrace(); e.getMessage(); }` |
| DriverExpiryAlert.java | 195-199 | Same pattern. |
| DriverMedicalAlert.java | 166-169 | Same pattern. |
| DriverMedicalAlert.java | 215-219 | Same pattern. |
| FleetCheckFTP.java | 252-254 | `catch(Exception e){ e.printStackTrace(); e.getMessage(); }` |
| ExcelUtil.java | 56-58, 79-81, 100-102, 123-126 | Four separate `catch(Exception e){ e.printStackTrace(); }` blocks. |
| DataUtil.java | 747-749, 893-895 | `catch(ParseException ex){ ex.printStackTrace(); }` and `catch (Exception e){ e.printStackTrace(); }` |
| DateUtil.java | 25, 64, 200, 219, 241, 313, 353 | Multiple `System.out.println("Exception :"+e);` -- exceptions logged to stdout only, swallowed. |

### e.getMessage() called with no effect

| File | Lines |
|------|-------|
| CftsAlert.java | 220, 267, 310 |
| DriverExpiryAlert.java | 153, 198 |
| DriverMedicalAlert.java | 169, 218 |
| FleetCheckFTP.java | 254 |

In all cases `e.getMessage()` is called as a standalone statement -- the return value is discarded, making the call a no-op.

---

## 7. e.printStackTrace()

Every file except BeanComparator.java, CustomComparator.java, DBUtil.java, and Dt_Checker.java uses `e.printStackTrace()`. Full list:

| File | Count | Lines |
|------|-------|-------|
| CftsAlert.java | 3 | 219, 266, 309 |
| CustomUpload.java | 3 | 254, 295, 171-174 (System.out.println variant) |
| DataUtil.java | 2 | 748, 894 |
| DateUtil.java | 2 | 25 (System.out variant), 354 |
| DriverExpiryAlert.java | 2 | 152, 197 |
| DriverMedicalAlert.java | 2 | 168, 217 |
| EncryptTest.java | 0 | (no exception handling at all) |
| ExcelUtil.java | 4 | 57, 80, 101, 125 |
| FleetCheckFTP.java | 3 | 214, 222, 253 |

**Impact:** Stack traces go to stderr/stdout only, not to the application logging framework. The application uses Log4j2 (see `CustomUpload.java` line 40: `private static Logger log = ...`), but no other file in this set uses it.

---

## 8. Thread Safety -- Static SimpleDateFormat

### DriverMedicalAlert.java -- Line 16
```java
private static SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy");
```
- **Used at:** Line 180 in `getDate(Calendar cal)` which is a `public static` method.
- **Issue:** `SimpleDateFormat` is **not thread-safe**. A static instance shared across threads will produce corrupt output or throw exceptions under concurrent access.
- **Severity:** HIGH

### DataUtil.java -- Multiple methods create new SDF instances (lines 119, 126, 243, 296, 564, 620-625, 660, 724, 865)
- These are local variables, so they are thread-safe but wasteful. No static SDF issue here, but noted for completeness.

---

## 9. Resource Leaks

### 9a. DataUtil.java -- saveImage() -- Lines 329-344
```java
InputStream is = url.openStream();
OutputStream os = new FileOutputStream(destinationFile);
// ... no try-with-resources, no finally
is.close();
os.close();
```
- If an exception occurs between open and close, both streams leak.

### 9b. DataUtil.java -- uploadLicenceFile() -- Lines 918-934
```java
InputStream fileContent = filePart.getInputStream();
// ...
OutputStream outStream = new FileOutputStream(targetFile);
outStream.write(buffer);
outStream.close();
```
- `fileContent` InputStream is never closed. `outStream` not closed on exception.

### 9c. DataUtil.java -- uploadDocumentFile() -- Lines 936-959
```java
InputStream fileContent = filePart.getInputStream();
// ...
OutputStream outStream = new FileOutputStream(targetFile);
outStream.write(buffer);
```
- `outStream` is **never closed** at all. `fileContent` is never closed.

### 9d. CustomUpload.java -- read() method -- Lines 322-353
```java
BufferedReader bufRdr = new BufferedReader(new FileReader(file));
// ... reads file ...
return dataLst;
```
- `BufferedReader` is never closed. No try-with-resources or finally block.

### 9e. ExcelUtil.java -- downloadExcel() -- Lines 107-127
```java
FileInputStream fileInputStream = new FileInputStream(fileToDownload);
ServletOutputStream output = response.getOutputStream();
// ...
fileInputStream.close();
output.close();
```
- If exception occurs during read loop, `fileInputStream` is not closed (catch block only calls `e.printStackTrace()`).

---

## 10. Dead Code

### 10a. CustomUpload.java -- Unused validation methods
The following private methods are never called from within the file or externally (class is a servlet, private methods are unreachable from outside):
- `validateCSV()` -- line 355
- `validateCSVIndividual()` -- line 407
- `validateCSVIndividualD()` -- line 378
- `validateCSVIndividualTab()` -- line 484
- `validateQuestionLenght()` -- line 445 (also misspelled: "Lenght")
- `validateQuestionLenghtTab()` -- line 465

### 10b. FleetCheckFTP.java -- Entire class potentially dead
- **Evidence:** Lines 18-23, comment block: `note as of March 10, 2023 testing, this is not being called by the store proc 'ftp_fleet_question'`. The stored procedure calls the old project's version of the class, not this one.

### 10c. Dt_Checker.java -- Unused fields and empty init()
- Line 6: `static String date1,dd,mm,yy;` -- static mutable state, also written by `first()` and `last()` methods which use them (thread-unsafe). Field `beanName` on line 7 appears unused.
- Line 234: `public void init() {}` -- empty method.

### 10d. CustomUpload.java -- Unused local variable
- Line 309: `final String partHeader = part.getHeader("content-disposition");` is assigned but never used; line 311 re-calls `part.getHeader("content-disposition")`.

---

## 11. Magic Numbers

| File | Line(s) | Value | Context |
|------|---------|-------|---------|
| CftsAlert.java | 95, 154 | `13` | `message1Week.length() > 13` -- length of prefix string "FLEET NO: \n", fragile. |
| CftsAlert.java | 77, 83 | `0`, `1`, `2`, `7` | Alert status codes and day thresholds with no named constants. |
| DataUtil.java | 349 | `10` | `(long)msec/ 10` -- division by 10 to convert "msec" to seconds is suspicious; comment says "milliseconds" but divides by 10 not 1000. |
| DataUtil.java | 354 | `86400` | Seconds in a day, should be a named constant. |
| DataUtil.java | 696-706 | `25`, `5`, `6` | Hour thresholds for colour status. |
| DataUtil.java | 815-833 | `100`, `150`, `50`, `67`, `33` | Impact percentage calculation magic numbers. |
| DataUtil.java | 1056 | `"26"`, `"166207"` | Customer/user IDs hardcoded (see also Hardcoded section). |
| ExcelUtil.java | 141 | `"../../../../../../../../excelrpt/"` | Relative path traversal with hardcoded depth. |
| FleetCheckFTP.java | 204 | `50` | Padding length for question text. |
| FleetCheckFTP.java | 113 | `3` | Substring length for directory name truncation. |

---

## 12. Hardcoded Credentials / Paths / Sensitive Data

### 12a. CustomUpload.java -- Hardcoded email and firmware credentials
- **Line 55:** `String email = request.getParameter("email")==null?"julius@collectiveintelligence.com.au":request.getParameter("email");` -- default email address hardcoded.
- **Line 108:** `PrintWriter pw = new PrintWriter(new File("/home/gmtp/csv/file.csv"));` -- hardcoded absolute path.
- **Line 163:** `"fleetfocus@lindemh.com.au"` -- hardcoded sender email.
- **Line 219:** `String message = "FTPF=fms.fleetiq360.com,211,firmware,Sdh79HfkLq6,/firmware/FW_LMII_2_10_59_GEN2_DISPLAY_AUTO_CAM/FleetMS.bin";` -- **FTP hostname, port, username ("firmware"), and password ("Sdh79HfkLq6") hardcoded in plain text.**
- **Severity:** CRITICAL -- credentials in source code.

### 12b. FleetCheckFTP.java -- Line 229
```java
String ftp_upld_cmd = "FTPF="+LindeConfig.firmwareserver+","+RuntimeConf.firmwareport+","+RuntimeConf.firmwareuser+","+RuntimeConf.firmwarepass+","+...
```
- Credentials loaded from config (better), but sent as plain-text command string to device outgoing queue. The pattern mirrors the hardcoded version in CustomUpload.

### 12c. DataUtil.java -- Hardcoded paths and customer IDs
- **Line 919:** `String base="/home/gmtp/fms_files/licence/";` -- hardcoded Linux path.
- **Line 937:** `String base="/home/gmtp/fms_files/CFTS/" + cust_loc + "/";` -- hardcoded Linux path.
- **Lines 1056, 1073-1077, 1085:** Customer ID `"26"` and user ID `"166207"` hardcoded for Visy-specific location filtering, with a comment: `quick impl: hard-coded for the meantime`.

---

## 13. SQL Injection

All SQL in the following files is built via string concatenation with user-controlled or database-derived values, without parameterized queries:

| File | Lines | Method |
|------|-------|--------|
| CftsAlert.java | 41-45, 54-67, 79, 85, 106, 115, 124, 147, 165, 174, 184, 207, 244-248, 291-295 | `checkDueDate()`, `getAlertlist()`, `getCustGroupList()` -- all use `Statement` with concatenated SQL. |
| DriverExpiryAlert.java | 70-86, 105-106, 114, 123, 134, 144, 175-179 | `checkExpiry()`, `getAlertlist()` -- all `Statement` + concatenation. |
| DriverMedicalAlert.java | 37, 74-80, 125, 143, 161, 195-199 | `checkInterval()`, `getAlertlist()` -- all `Statement` + concatenation. |
| FleetCheckFTP.java | 77-84, 99-101, 230-231, 235-236, 242-243, 246 | `upload_quest_ftp()` -- all `Statement` + concatenation. |
| CustomUpload.java | 219-223, 225-226, 234 | Lines 219-234 use `PreparedStatement` for SELECT but then use string concatenation for INSERT: `"insert into \"outgoing\" (destination,message) values('"+gmtp_id+"','"+message+"')"`. Also lines 234: `"insert into \"outgoing_stat\" ...values('"+sno+"','"+gmtp_id+"','"+message+"','"+tm+"','f')"`. |
| CftsAlert.java, DriverExpiryAlert.java, DriverMedicalAlert.java | Multiple | Email content (`message`, `subsject`) concatenated directly into INSERT SQL: `"insert into email_outgoing ... VALUES (NOW(), '"+email+"','"+subsject+"','"+ message + "')"`. If message body contains a single quote, the SQL breaks or enables injection. |

---

## 14. Raw Types (Missing Generics)

| File | Line | Evidence |
|------|------|----------|
| BeanComparator.java | 19 | `implements Comparator` -- raw type, should be `Comparator<Object>`. |
| BeanComparator.java | 69 | `Class returnClass` -- raw type. |
| DataUtil.java | 60, 104 | `ArrayList dbValue` -- raw type parameter. |
| FleetCheckFTP.java | 43-44, 58-61 | `ArrayList gmtp_ids`, `ArrayList q_ids`, `ArrayList vques`, `ArrayList vorder_no`, `ArrayList vcric_ans`, `ArrayList vques_cd` -- all raw types. |
| ExcelUtil.java | 27, 37, 65, 87 | `Class[] types`, `Class report` -- raw types. |
| CustomUpload.java | 106 | `ArrayList<String> data = new ArrayList();` -- diamond missing on right side. |

---

## 15. Misspelled Identifiers

| File | Line | Identifier | Should Be |
|------|------|-----------|-----------|
| CftsAlert.java | 142, 203 | `subsject` | `subject` |
| DriverExpiryAlert.java | 40, 141, 144 | `subsject` | `subject` |
| DataUtil.java | 240 | `generateRadomName` | `generateRandomName` |
| DataUtil.java | 509, 636 | `caculatePercentage`, `caculateImpPercentage` | `calculatePercentage`, `calculateImpPercentage` |
| CustomUpload.java | 445, 465 | `validateQuestionLenght`, `validateQuestionLenghtTab` | `validateQuestionLength`, `validateQuestionLengthTab` |
| DateUtil.java | 300 | `arrCanlendar` | `arrCalendar` |

---

## 16. Broken Leap-Year Logic -- Dt_Checker.java

### Lines 141-150
```java
public static boolean isleap(int y)
{
    if (y%1000 == 0)  // BUG: should be y%100 == 0
    { return true;}   // BUG: divisible-by-100 should return false (unless also by 400)
    if (y%400 == 0)
    { return false;}  // BUG: divisible-by-400 should return true
    if (y%4 == 0)
    { return true;}
    return false;
}
```
- **Issue:** The leap year logic is inverted and uses `1000` instead of `100`. The correct rules are:
  - Divisible by 400 => leap year (true)
  - Divisible by 100 => not leap year (false)
  - Divisible by 4 => leap year (true)
  - Otherwise => not leap year (false)
- This method checks `y%1000` (wrong threshold), returns `true` for it, then returns `false` for `y%400` -- both are backwards.
- **Impact:** Years like 1900 would be treated as leap years (they are not); year 2000 would NOT be treated as a leap year (it is one).

### Static mutable fields -- Lines 6-7
```java
static String date1,dd,mm,yy;
```
- `first()` and `last()` methods write to these static fields. If called concurrently, results corrupt.

---

## 17. Weak / Home-Rolled Encryption -- EncryptTest.java

- **File:** `EncryptTest.java` (entire file)
- **Evidence:** The `encrypt()` method uses a trivial character-shift cipher: `c = (char)(s1.charAt(i) + (i + 1))` for odd positions, `c = (char)(s1.charAt(i) - (i + 1))` for even positions, prepended with a fixed 10-character "salt" chosen by input length.
- **Issues:**
  1. This is **not encryption** -- it is a trivially reversible character substitution. The `decrypt()` method simply reverses the shift.
  2. No key, no IV, no standard algorithm.
  3. The file header reveals it was **decompiled** from a third-party tool in 2006 and committed as-is.
  4. If this is used for password storage or sensitive data, it provides no real protection.
- **Severity:** CRITICAL if used for passwords or sensitive data.

---

## File-by-File Summary

| File | LOC | Findings | Severity |
|------|-----|----------|----------|
| BeanComparator.java | 175 | Raw type Comparator; broad catch (wraps as RuntimeException -- acceptable). | Low |
| CftsAlert.java | 322 | SQL injection (x12+), e.printStackTrace (x3), broad catch (x3), misspelling `subsject`, magic number `13`, no logging framework. | Critical |
| CustomComparator.java | 15 | Contains `// TODO Auto-generated method stub` comment (line 11). Otherwise clean. | Low |
| CustomUpload.java | 517 | God class, 6 dead private methods, hardcoded FTP credentials (CRITICAL), SQL injection, resource leak (BufferedReader), e.printStackTrace, commented-out code, System.out.println. | Critical |
| DBUtil.java | 58 | Clean. `getConnection()` and `getMySqlConnection()` throw `Exception` (too broad) instead of specific exception types. | Low |
| DataUtil.java | 1087 | God class (40+ methods), 3 misspelled method names, duplicate import, resource leaks (x3), hardcoded paths and customer IDs, magic numbers, e.printStackTrace, `convert_time` suspicious division by 10. | High |
| DateUtil.java | 359 | Multiple System.out.println for exceptions, method naming inconsistency (PascalCase), misspelling `arrCanlendar`. No logging framework. | Medium |
| DriverExpiryAlert.java | 210 | SQL injection (x8+), e.printStackTrace (x2), broad catch (x2), misspelling `subsject`. | Critical |
| DriverMedicalAlert.java | 230 | Static SimpleDateFormat (thread-unsafe), SQL injection (x6+), e.printStackTrace (x2), broad catch (x2). | Critical |
| Dt_Checker.java | 241 | Non-standard naming, broken leap-year logic (BUG), static mutable fields (thread-unsafe), unused import `java.lang.*`, empty `init()`, dead field `beanName`. | High |
| EncryptTest.java | 113 | Misleading name, decompiled code, home-rolled trivial cipher (no real security), no exception handling. | Critical |
| ExcelUtil.java | 145 | 4x broad catch with e.printStackTrace, raw types, resource leak in `downloadExcel()`, hardcoded relative path traversal (`../../../../../../../../excelrpt/`). | High |
| FleetCheckFTP.java | 276 | Potentially dead class, SQL injection (x6+), raw types (x6), e.printStackTrace (x3), deeply nested code. | High |

---

## Recommendations (Prioritized)

1. **CRITICAL -- Remove hardcoded FTP credentials** from `CustomUpload.java` line 219. Move all credentials to externalized configuration.
2. **CRITICAL -- Replace home-rolled encryption** in `EncryptTest.java` with a standard library (e.g., `javax.crypto` AES). Audit all callers.
3. **CRITICAL -- Parameterize all SQL** in CftsAlert, DriverExpiryAlert, DriverMedicalAlert, FleetCheckFTP, and CustomUpload to prevent SQL injection.
4. **HIGH -- Fix static SimpleDateFormat** in `DriverMedicalAlert.java` (use `ThreadLocal<SimpleDateFormat>` or `DateTimeFormatter`).
5. **HIGH -- Fix broken leap-year logic** in `Dt_Checker.java` or replace with `java.time` / `Calendar` API.
6. **HIGH -- Close resource leaks** in DataUtil (`saveImage`, `uploadLicenceFile`, `uploadDocumentFile`), CustomUpload (`read`), ExcelUtil (`downloadExcel`) using try-with-resources.
7. **HIGH -- Replace all e.printStackTrace()** calls with proper Log4j2 logging (`log.error("message", e)`).
8. **MEDIUM -- Decompose God classes** `DataUtil` and `CustomUpload` into focused, single-responsibility classes.
9. **MEDIUM -- Remove dead code**: 6 unused validation methods in CustomUpload; verify and remove `FleetCheckFTP` if confirmed dead; clean up `Dt_Checker` empty `init()` and unused fields.
10. **LOW -- Fix all misspelled identifiers** (`subsject`, `generateRadomName`, `caculatePercentage`, `validateQuestionLenght`, `arrCanlendar`).
11. **LOW -- Add generics** to all raw-type collections and comparators.
12. **LOW -- Remove commented-out debug code** and `// TODO Auto-generated` markers.

---

*End of Pass 4 report for util A-F.*
