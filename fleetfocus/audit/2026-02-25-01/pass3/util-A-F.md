# Pass 3 -- Documentation Audit: util package (A-F)

**Audit ID:** 2026-02-25-01-P3-util-AF
**Agent:** A19
**Date:** 2026-02-25
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Base path:** `WEB-INF/src/com/torrent/surat/fms6/util/`

---

## Summary

| # | File | Class Javadoc | Methods Total (public) | Undocumented Public | TODO/FIXME/HACK/XXX | Findings |
|---|------|:---:|:---:|:---:|:---:|:---:|
| 1 | BeanComparator.java | YES | 6 | 0 | 0 | 2 |
| 2 | CftsAlert.java | NO | 2 | 2 | 0 | 3 |
| 3 | CustomComparator.java | NO | 1 | 1 | 1 | 3 |
| 4 | CustomUpload.java | NO | 3 | 3 | 1 | 4 |
| 5 | DBUtil.java | YES (partial) | 3 | 0 | 0 | 2 |
| 6 | DataUtil.java | NO | 50+ | 50+ | 0 | 5 |
| 7 | DateUtil.java | NO | 22 | 22 | 0 | 3 |
| 8 | DriverExpiryAlert.java | NO | 1 | 1 | 0 | 2 |
| 9 | DriverMedicalAlert.java | NO | 2 | 2 | 0 | 2 |
| 10 | Dt_Checker.java | NO | 9 | 9 | 0 | 5 |
| 11 | EncryptTest.java | NO | 2 | 2 | 0 | 3 |
| 12 | ExcelUtil.java | NO | 6 | 6 | 0 | 3 |
| 13 | FleetCheckFTP.java | NO | 1 | 1 | 0 | 2 |

**Total findings:** 39

---

## File-by-File Analysis

---

### 1. BeanComparator.java (175 lines)

**Reading evidence:** Package `com.torrent.surat.fms6.util`. Implements `Comparator` (raw type). Uses reflection to invoke a getter method on bean objects for comparison. Three constructors with progressive parameterization. Class-level Javadoc present and accurate. All public methods have non-Javadoc `/* */` comments (not proper Javadoc `/** */`).

**Class-level Javadoc:** YES -- Describes purpose (sorting on a specified field via reflection), documents three sort properties (ascending, ignoreCase, nullsLast) with defaults.

**Public methods:**
| Method | Documented | Comment Style |
|--------|:---:|:---:|
| `BeanComparator(Class, String)` | Yes | `/* */` (not Javadoc) |
| `BeanComparator(Class, String, boolean)` | Yes | `/* */` (not Javadoc) |
| `BeanComparator(Class, String, boolean, boolean)` | Yes | `/* */` (not Javadoc) |
| `setAscending(boolean)` | Yes | `/* */` (not Javadoc) |
| `setIgnoreCase(boolean)` | Yes | `/* */` (not Javadoc) |
| `setNullsLast(boolean)` | Yes | `/* */` (not Javadoc) |
| `compare(Object, Object)` | Yes | `/* */` (not Javadoc) |

**TODO/FIXME/HACK/XXX:** None.

#### Findings

| ID | Severity | Line(s) | Description |
|----|----------|---------|-------------|
| DOC-BEAN-01 | INFO | 30-104 | All method comments use `/* */` style instead of Javadoc `/** */`. These will not appear in generated Javadoc. |
| DOC-BEAN-02 | LOW | 104 | Comment says "Implement the Comparable interface" but the class implements `Comparator`, not `Comparable`. This is technically inaccurate. |

---

### 2. CftsAlert.java (323 lines)

**Reading evidence:** Package `com.torrent.surat.fms6.util`. No class-level Javadoc. Two public methods: `checkDueDate()` and `getCustGroupList()`. One private method: `getAlertlist(String, String)`. The class checks CFTS (Certificate of Thorough Examination) inspection due dates, sends email alerts for inspections due within 1 week or overdue. Uses `MymessagesUsersBean`, `DBUtil`, `DataUtil.calculateTime`.

**Class-level Javadoc:** NO

**Public methods:**
| Method | Documented |
|--------|:---:|
| `checkDueDate()` | No |
| `getCustGroupList()` | No |

**TODO/FIXME/HACK/XXX:** None.

#### Findings

| ID | Severity | Line(s) | Description |
|----|----------|---------|-------------|
| DOC-CFTS-01 | MEDIUM | 11 | Missing class-level Javadoc. No documentation explains that this alert checks CFTS inspection due dates and sends email notifications for upcoming or overdue inspections. |
| DOC-CFTS-02 | MEDIUM | 14 | Public method `checkDueDate()` has no Javadoc. This is the main entry point for the alert and callers have no documentation of what it does, what side-effects it has (sends emails, updates alert_status), or why it throws `SQLException`. |
| DOC-CFTS-03 | MEDIUM | 279 | Public method `getCustGroupList()` has no Javadoc. Returns customer/site groups for inspection alerts but callers have no documentation of the returned data structure. |

---

### 3. CustomComparator.java (16 lines)

**Reading evidence:** Package `com.torrent.surat.fms6.util`. Implements `Comparator<DriverLeagueBean>`. Single method `compare` that sorts by driver name in descending order (o2 compared to o1). Contains an IDE-generated TODO. No documentation at all.

**Class-level Javadoc:** NO

**Public methods:**
| Method | Documented |
|--------|:---:|
| `compare(DriverLeagueBean, DriverLeagueBean)` | No |

**TODO/FIXME/HACK/XXX:**
- Line 11: `// TODO Auto-generated method stub` -- IDE-generated placeholder left in production code.

#### Findings

| ID | Severity | Line(s) | Description |
|----|----------|---------|-------------|
| DOC-CCOMP-01 | MEDIUM | 7 | Missing class-level Javadoc. No documentation explaining that this comparator sorts `DriverLeagueBean` instances by driver name in descending order. |
| DOC-CCOMP-02 | LOW | 10-12 | Public method `compare()` has no Javadoc. While the implementation is simple, the descending sort order is not documented and could surprise callers. |
| DOC-CCOMP-03 | INFO | 11 | Residual IDE-generated `TODO Auto-generated method stub` comment left in production code. Should be removed. |

---

### 4. CustomUpload.java (518 lines)

**Reading evidence:** Package `com.torrent.surat.fms6.util`. Extends `HttpServlet`, annotated as `@WebServlet("/servlet/Import_Files")` with `@MultipartConfig`. Handles file uploads for two actions: "gmtp" (GMTP ID lookup from CSV) and "firmware" (firmware push commands). Contains `doPost`, `now`, `getFileName`, `read`, `validateCSV`, and several `validateCSV*` variants. Hardcoded email address on line 55. Hardcoded file path `/home/gmtp/csv/file.csv` on line 108.

**Class-level Javadoc:** NO

**Public methods:**
| Method | Documented |
|--------|:---:|
| `doPost(HttpServletRequest, HttpServletResponse)` | No |
| `now(String)` | No |
| `read(String)` | No |

**TODO/FIXME/HACK/XXX:**
- Line 294: `// TODO Auto-generated catch block` -- IDE-generated placeholder in `finally` block for `dbcon.close()`.

#### Findings

| ID | Severity | Line(s) | Description |
|----|----------|---------|-------------|
| DOC-CUPL-01 | MEDIUM | 38 | Missing class-level Javadoc. No documentation explains that this servlet handles CSV file uploads for GMTP ID lookups and firmware push operations. The two distinct action modes ("gmtp" and "firmware") are not documented anywhere. |
| DOC-CUPL-02 | MEDIUM | 45 | Public method `doPost()` has no Javadoc. The complex multi-action logic (gmtp vs firmware), expected request parameters (`src`, `customer`, `action`, `email`, `file`), and JSON response format are entirely undocumented. |
| DOC-CUPL-03 | MEDIUM | 322 | Public method `read(String)` has no Javadoc. It reads a CSV file into a list of row arrays but the contract (delimiter handling, character sanitization) is not documented. This is a reusable utility method. |
| DOC-CUPL-04 | INFO | 294 | Residual IDE-generated `TODO Auto-generated catch block` left in production code. |

---

### 5. DBUtil.java (58 lines)

**Reading evidence:** Package `com.torrent.surat.fms6.util`. Private constructor (utility class pattern). Three static methods: `getConnection()`, `getMySqlConnection()`, `closeConnection(Connection)`. All three have Javadoc. However, Javadoc uses `@param void` which is non-standard, and `@exception SQLException` is declared but both `getConnection` methods throw `Exception`, not just `SQLException`.

**Class-level Javadoc:** NO (class itself has no Javadoc comment; only methods have Javadoc)

**Public methods:**
| Method | Documented |
|--------|:---:|
| `getConnection()` | Yes (Javadoc) |
| `getMySqlConnection()` | Yes (Javadoc) |
| `closeConnection(Connection)` | Yes (Javadoc) |

**TODO/FIXME/HACK/XXX:** None.

#### Findings

| ID | Severity | Line(s) | Description |
|----|----------|---------|-------------|
| DOC-DBUT-01 | LOW | 10 | Missing class-level Javadoc. While the methods are documented, the class itself has no documentation explaining its role as the central JNDI-based connection factory. |
| DOC-DBUT-02 | HIGH | 14-19, 29-34 | Javadoc for `getConnection()` and `getMySqlConnection()` declares `@exception SQLException` but both methods actually throw `Exception` (the broader type). The `@param void` tag is also non-standard (should be omitted if there are no parameters). The Javadoc for `getMySqlConnection` is identical to `getConnection` and does not mention that it returns a MySQL connection vs the default PostgreSQL connection. This is misleading because the two methods connect to different databases. |

---

### 6. DataUtil.java (1087 lines)

**Reading evidence:** Package `com.torrent.surat.fms6.util`. Large utility class with 50+ public static methods covering: HTML form helpers (`checkedValue`, `checkedValueRadio`, `checkedValueCheckbox`), formatting (`formatImpact`, `formatPercentage`, `formatdouble`, `formatdoubletoInt`), date operations (`getDateTime`, `getCurrentDate`, `compareDates`, `checkDateFormat`, `addMonthToDate`, `calculateTime`, `formatStringDate`, `formatStringDate2`), math (`maxValue`, `maxArrayValue`, `sumValue`, `maxTotalValue`), time conversion (`convert_time`, `convert_time_hhmm`, `convertServiceHour`), string manipulation (`replaceSpecialCharacter`, `escapeSpecialCharacter`, `removeDuplicateCds`, `nthOccurrence`), random generation (`generateRadomName`, `getRandomString`), file handling (`saveImage`, `getFileName`, `uploadLicenceFile`, `uploadDocumentFile`), calendar/month helpers, colour status, logging, and business logic (`calculateLastServTypeCO`, `calculateNextServTypeDue`, `getColourStatus`, `getProductType`, `convertToImpPerc`, `isVehichleDurationHired`, `getLocationFilter`, `isForVisyLimitingLocations`). Only inline `//` comments exist on some methods; no Javadoc on any method. Duplicate import of `java.util.ArrayList` at line 37.

**Class-level Javadoc:** NO

**Undocumented public methods (complete list):**
`checkedValue` (x3 overloads), `formatImpact`, `checkedValueRadio`, `checkedValueCheckbox`, `getDateTime`, `getCurrentDate`, `checkEmptyArray`, `maxArrayValue`, `maxValue` (x2 overloads), `sumValue` (x2 overloads), `sumValueShift`, `maxTotalValue`, `generateRadomName`, `getPreviousMonth`, `getCurrentMonth`, `getMonthForInt`, `getDayForInt`, `getDateForInt`, `getWeekForInt`, `saveImage`, `convert_time` (x2 overloads), `convert_time_hhmm`, `caculatePercentage`, `getRandomString`, `nthOccurrence`, `replaceSpecialCharacter`, `formatPercentage`, `dateToString`, `getFileName` (x2 overloads), `formatdouble`, `escapeSpecialCharacter`, `convertServiceHour`, `formatStringDate`, `formatStringDate2`, `formatdoubletoInt`, `caculateImpPercentage`, `addMonthToDate`, `calculateLastServTypeCO`, `calculateNextServTypeDue`, `getColourStatus`, `log`, `compareDates`, `checkDateFormat`, `getMonthStr`, `removeDuplicateCds`, `getShortDayForInt`, `convertToImpPerc`, `getProductType`, `calculateTime`, `uploadLicenceFile`, `uploadDocumentFile`, `isVehichleDurationHired` (x2 overloads), `getLocationFilter`, `isForVisyLimitingLocations`

**TODO/FIXME/HACK/XXX:** None.

#### Findings

| ID | Severity | Line(s) | Description |
|----|----------|---------|-------------|
| DOC-DUTIL-01 | MEDIUM | 39 | Missing class-level Javadoc. This is the largest utility class in the package (1087 lines, 50+ methods) and has zero documentation explaining its scope or organization. |
| DOC-DUTIL-02 | MEDIUM | all | Every public method (50+) lacks Javadoc. This is a utility class that is widely depended upon. Key methods with non-obvious contracts include: `calculateTime` (what "type" values are accepted?), `convert_time` (what units is `msec` in -- divides by 10, not 1000), `caculateImpPercentage` (what does the formula mean?), `isVehichleDurationHired` (complex hire/dehire overlap logic), `getLocationFilter` (hard-coded customer/user filtering). |
| DOC-DUTIL-03 | HIGH | 346-413, 415-482 | `convert_time(int msec)` and `convert_time_hhmm(int msec)`: parameter name says "msec" (milliseconds) but the first operation is `secs = (long)msec / 10`, implying the input is in deciseconds (1/10th second), not milliseconds. The inline comment says "Calculates and returns the time" but does not clarify the input unit. This is misleading to any caller. |
| DOC-DUTIL-04 | HIGH | 1052-1082 | `getLocationFilter(String customer, String accessUser)`: Hard-coded Visy-specific customer ID ("26") and user ID ("166207") with hard-coded location codes. The inline comment says "quick impl: hard-coded for the meantime" but this is not flagged as a TODO or documented in any method Javadoc. Callers have no documentation of this special-case behavior. |
| DOC-DUTIL-05 | MEDIUM | 509 | Method name `caculatePercentage` is misspelled (should be "calculate"). No Javadoc to clarify the correct name or purpose. Similarly `caculateImpPercentage` on line 636 and `generateRadomName` on line 240 ("Radom" instead of "Random"). |

---

### 7. DateUtil.java (360 lines)

**Reading evidence:** Package `com.torrent.surat.fms6.util`. Contains 22 public static methods for date/time parsing, formatting, comparison, and calculation. No class-level Javadoc. No method-level Javadoc on any method. Methods include: `stringToDate`, `getDaysDate`, `dateToString`, `stringToSQLDate`, `getLocalTimestamp` (x2 overloads), `getUTCTime`, `getLocalTime`, `isValidDate`, `isValidDates`, `stringToTimestamp`, `stringToTimestampHM`, `StringTimeDifference`, `GetDateNow`, `GetDate`, `compareDates`, `compareDateTime`, `GetCalendar`, `getDateString`, `getDuration`, `getStartDate`, `getNxtMthDate`.

**Class-level Javadoc:** NO

**Undocumented public methods (all 22):**
`stringToDate`, `getDaysDate`, `dateToString`, `stringToSQLDate`, `getLocalTimestamp` (x2), `getUTCTime`, `getLocalTime`, `isValidDate`, `isValidDates`, `stringToTimestamp`, `stringToTimestampHM`, `StringTimeDifference`, `GetDateNow`, `GetDate`, `compareDates`, `compareDateTime`, `GetCalendar`, `getDateString`, `getDuration`, `getStartDate`, `getNxtMthDate`

**TODO/FIXME/HACK/XXX:** None.

#### Findings

| ID | Severity | Line(s) | Description |
|----|----------|---------|-------------|
| DOC-DTUT-01 | MEDIUM | 14 | Missing class-level Javadoc. This is a central date utility class with 22 public methods and no documentation of expected date format conventions or thread-safety considerations. |
| DOC-DTUT-02 | MEDIUM | all | All 22 public methods lack Javadoc. Critical undocumented contracts include: `stringToDate` uses "dd/MM/yy" format (2-digit year), `stringToSQLDate` has ambiguous dd/MM vs MM/dd heuristic (lines 53-58), `isValidDate` expects "yyyy/MM/dd HH:mm:ss" while `isValidDates` expects "dd/MM/yyyy" -- these naming differences are confusing without documentation. |
| DOC-DTUT-03 | HIGH | 45-71 | `stringToSQLDate`: contains an undocumented date-format heuristic that swaps between "dd/MM/yyyy" and "MM/dd/yyyy" based on whether day or month values exceed 12. This logic is ambiguous for dates where both day and month are <= 12 (e.g., "05/06/2024" could be May 6 or June 5). The absence of Javadoc explaining the expected input format and this heuristic is misleading. |

---

### 8. DriverExpiryAlert.java (211 lines)

**Reading evidence:** Package `com.torrent.surat.fms6.util`. Sends email alerts for driver licence expiry. Single public method `checkExpiry()`. One private helper `getAlertlist()`. Single-line non-Javadoc comment on line 12: `// Send email alert on driver licence expiry`. Queries driver licence expiry dates and sends alerts for expired, 1-week, 1-month, 3-month, and 6-month thresholds.

**Class-level Javadoc:** NO (only a `//` comment on line 12, not a Javadoc `/** */` comment)

**Public methods:**
| Method | Documented |
|--------|:---:|
| `checkExpiry()` | No |

**TODO/FIXME/HACK/XXX:** None.

#### Findings

| ID | Severity | Line(s) | Description |
|----|----------|---------|-------------|
| DOC-DEXP-01 | LOW | 12 | Class has an inline `//` comment instead of proper Javadoc. The comment "Send email alert on driver licence expiry" is helpful but will not appear in generated documentation. |
| DOC-DEXP-02 | MEDIUM | 15 | Public method `checkExpiry()` has no Javadoc. The method has significant side-effects (queries database, sends emails, inserts into email_outgoing table) and callers have no documentation of its behavior or the alert threshold logic. |

---

### 9. DriverMedicalAlert.java (231 lines)

**Reading evidence:** Package `com.torrent.surat.fms6.util`. Sends email alerts for driver medical certificate expiry. Two public methods: `checkInterval()` and `getDate(Calendar)`. One private helper `getAlertlist()`. Non-thread-safe static `SimpleDateFormat` on line 16. Checks for drivers expiring today, in one week, and in one month.

**Class-level Javadoc:** NO

**Public methods:**
| Method | Documented |
|--------|:---:|
| `checkInterval()` | No |
| `getDate(Calendar)` | No |

**TODO/FIXME/HACK/XXX:** None.

#### Findings

| ID | Severity | Line(s) | Description |
|----|----------|---------|-------------|
| DOC-DMED-01 | MEDIUM | 14 | Missing class-level Javadoc. No documentation explains that this alert checks driver medical certificate dates and sends email notifications for today, one-week, and one-month expiry windows. |
| DOC-DMED-02 | MEDIUM | 18 | Public method `checkInterval()` has no Javadoc. The method performs database queries, date comparisons, and email insertion but callers have no documentation of its behavior or when it should be invoked. |

---

### 10. Dt_Checker.java (242 lines)

**Reading evidence:** Package `com.torrent.surat.fms6.util`. Legacy date comparison utility. All methods are public static (except `init()`). Parses dates in "dd/mm/yyyy" format via manual string splitting. Contains a leap year calculation bug at line 143: `y%1000 == 0` should be `y%100 == 0` (century check). Methods: `greaterThan`, `equalTo`, `first`, `last`, `isleap`, `between`, `conflict`, `days_Betn`, `daysIn`, `init`. Uses static mutable fields (`date1`, `dd`, `mm`, `yy`) making it not thread-safe.

**Class-level Javadoc:** NO

**Public methods (all undocumented):**
| Method | Documented |
|--------|:---:|
| `greaterThan(String, String)` | No |
| `equalTo(String, String)` | No |
| `first(String)` | No |
| `last(String)` | No |
| `isleap(int)` | No |
| `between(String, String, String)` | No |
| `conflict(String, String, String, String)` | No |
| `days_Betn(String, String)` | No |
| `daysIn(int, int, int)` | No |

**TODO/FIXME/HACK/XXX:** None.

#### Findings

| ID | Severity | Line(s) | Description |
|----|----------|---------|-------------|
| DOC-DTCK-01 | MEDIUM | 4 | Missing class-level Javadoc. No documentation explains that this is a legacy date checker utility, what date format it expects (dd/mm/yyyy), or warns about thread-safety issues with static mutable fields. |
| DOC-DTCK-02 | MEDIUM | 11, 53 | `greaterThan(String, String)` and `equalTo(String, String)`: parameter order is non-obvious and undocumented. `greaterThan(dt2, dt1)` returns true if dt2 > dt1, but the parameter names reverse the natural reading order. Without Javadoc, callers cannot determine which parameter is compared to which. |
| DOC-DTCK-03 | MEDIUM | 84, 109 | `first(String)` and `last(String)`: method names are cryptic. `first` returns the first day of the next month; `last` returns the last day of the month after next. Without Javadoc, these names are entirely misleading -- "first" and "last" suggest first/last day of the current month. |
| DOC-DTCK-04 | HIGH | 141-150 | `isleap(int)`: contains a bug (`y%1000` should be `y%100`) AND has no Javadoc. The absence of documentation makes it impossible for callers to know whether the bug is intentional or accidental. A standard leap year algorithm is: divisible by 4, except centuries, except 400-year multiples. The code checks `y%1000` (millennia) instead of `y%100` (centuries). |
| DOC-DTCK-05 | MEDIUM | 153-175 | `between(String, String, String)` and `conflict(String, String, String, String)`: complex date range overlap logic with three and four string parameters respectively. Without Javadoc, the parameter order and semantics (which date is start, which is end) are unknowable. |

---

### 11. EncryptTest.java (114 lines)

**Reading evidence:** Package `com.torrent.surat.fms6.util`. File header indicates this was decompiled from bytecode by "DJ v3.9.9.91" on 1/25/2006. Contains `encrypt(String)` and `decrypt(String)` methods. The encryption is a simple character-shift cipher with a fixed 10-character prefix based on input length. Despite the name "EncryptTest", this is used as a production encryption utility, not a test class.

**Class-level Javadoc:** NO

**Public methods:**
| Method | Documented |
|--------|:---:|
| `encrypt(String)` | No |
| `decrypt(String)` | No |

**TODO/FIXME/HACK/XXX:** None.

#### Findings

| ID | Severity | Line(s) | Description |
|----|----------|---------|-------------|
| DOC-ENCT-01 | HIGH | 9 | Class name `EncryptTest` is misleading. The decompiler header (line 1-4) confirms this is decompiled code, but there is no Javadoc explaining that this is a production encryption utility (not a test), what algorithm it uses (character-shift cipher with length-based prefix), or its security characteristics. The class name alone will mislead developers into thinking it is test code. |
| DOC-ENCT-02 | MEDIUM | 16, 97 | Public methods `encrypt(String)` and `decrypt(String)` have no Javadoc. There is no documentation of the encryption algorithm, the 10-character prefix convention, or input constraints (the decrypt method assumes the input has at least 10 characters). |
| DOC-ENCT-03 | INFO | 1-4 | Decompiler header comment from 2006 is still present. This is not functional documentation and is potentially confusing as provenance metadata. |

---

### 12. ExcelUtil.java (146 lines)

**Reading evidence:** Package `com.torrent.surat.fms6.util`. Utility class for generating and downloading Excel reports. Uses reflection to dynamically instantiate report classes from `com.torrent.surat.fms6.excel.reports` package. Public methods: `getExcel` (generate and download), `getEmail` (generate for email), `getPrintBody` (generate HTML body), `downloadExcel` (stream file to response), `sendEmail` (send via `MailExcelReports`), `getExportDir` (compute export directory path). No Javadoc anywhere. The `getExportDir` method uses a fragile path computation with 8 levels of `../` traversal.

**Class-level Javadoc:** NO

**Public methods (all undocumented):**
| Method | Documented |
|--------|:---:|
| `ExcelUtil()` | No |
| `getExcel(String, String, HttpServletResponse)` | No |
| `getEmail(String, String, boolean)` | No |
| `getPrintBody(String, String)` | No |
| `downloadExcel(HttpServletResponse)` | No |
| `sendEmail(String, String)` | No |
| `getExportDir()` | No |

**TODO/FIXME/HACK/XXX:** None.

#### Findings

| ID | Severity | Line(s) | Description |
|----|----------|---------|-------------|
| DOC-EXUT-01 | MEDIUM | 13 | Missing class-level Javadoc. No documentation explains the reflection-based report generation pattern, the expected format of `rpt_name` and `params` parameters, or the relationship to `Frm_excel` and `MailExcelReports`. |
| DOC-EXUT-02 | MEDIUM | 34, 61, 84, 107, 129, 134 | All 6 public methods lack Javadoc. Key undocumented contracts: `getExcel` dynamically loads a class by name (security implications), `params` is comma-delimited, `getExportDir` uses fragile relative path traversal. |
| DOC-EXUT-03 | MEDIUM | 134-144 | `getExportDir()` computes a directory path by navigating 8 levels up (`../../../../../../../../excelrpt/`) from the class file location. This extremely fragile path logic has no documentation explaining why this traversal depth is needed or what directory it targets. |

---

### 13. FleetCheckFTP.java (277 lines)

**Reading evidence:** Package `com.torrent.surat.fms6.util`. Generates pre-operation check question files (PREOP.TXT) in binary format and sends FTP upload commands to GMTP devices. Single public method `upload_quest_ftp()`. Contains an important block comment (lines 18-23) noting that as of March 2023, this class is not being called by the stored procedure and the actual invocation comes from the old project's FleetCheckFTP class. References `ftp_outgoing` table which the comment says "is never existing in the live site".

**Class-level Javadoc:** NO

**Public methods:**
| Method | Documented |
|--------|:---:|
| `upload_quest_ftp()` | No (has an informational block comment above it but not Javadoc) |

**TODO/FIXME/HACK/XXX:** None explicitly tagged, though the block comment on lines 18-23 functions as a warning note.

#### Findings

| ID | Severity | Line(s) | Description |
|----|----------|---------|-------------|
| DOC-FCFTP-01 | MEDIUM | 17 | Missing class-level Javadoc. The informational block comment (lines 18-23) provides critical context about this class being potentially dead code, but it uses `/* */` style rather than Javadoc, so it will not appear in generated documentation. |
| DOC-FCFTP-02 | MEDIUM | 24 | Public method `upload_quest_ftp()` has no Javadoc. The method performs a complex sequence (query FTP outgoing queue, look up vehicle/customer/site/dept hierarchy, generate binary PREOP.TXT file, insert FTP commands into outgoing table, clean up queue). This entire workflow is undocumented. |

---

## Consolidated Finding Counts by Severity

| Severity | Count | Description |
|----------|:-----:|-------------|
| HIGH | 4 | Misleading documentation: DBUtil exception mismatch, DataUtil msec unit mismatch, DataUtil hard-coded Visy filter, Dt_Checker isleap bug undocumented, EncryptTest misleading class name |
| MEDIUM | 27 | Missing Javadoc on utility methods with non-trivial contracts |
| LOW | 3 | Missing class-level Javadoc on simpler classes, minor inaccuracies |
| INFO | 5 | Non-Javadoc comment style, residual IDE TODOs, decompiler header |
| **Total** | **39** | |

---

## Key Observations

1. **Pervasive documentation absence:** 12 of 13 files lack class-level Javadoc. Only `BeanComparator.java` has a class-level doc comment.

2. **Zero Javadoc on methods in DataUtil and DateUtil:** These two files together expose 70+ public utility methods with no Javadoc at all. Given they are core utility classes used across the entire application, this is the highest-impact documentation gap in this file set.

3. **Misleading documentation is worse than missing documentation:** The four HIGH findings involve cases where existing comments or naming actively mislead: DBUtil's `@exception SQLException` when `Exception` is thrown, DataUtil's `msec` parameter name for decisecond input, Dt_Checker's buggy `isleap` with no doc, and EncryptTest's "Test" suffix on a production class.

4. **TODO debris:** Two files (CustomComparator, CustomUpload) contain IDE-generated `TODO Auto-generated method stub` / `TODO Auto-generated catch block` comments that were never addressed.

5. **Non-Javadoc comment style:** BeanComparator and FleetCheckFTP have helpful comments using `/* */` instead of `/** */`, meaning the documentation exists but is invisible to Javadoc tooling.

---

*End of Pass 3 audit for util package (A-F). Agent A19, 2026-02-25.*
