# Pass 2 -- Test Coverage: util package (A-F)
**Agent:** A19
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

---

## Test Infrastructure Assessment

| Aspect | Status |
|---|---|
| Test directories (`test/`, `tests/`) | **None found** |
| JUnit / TestNG imports across entire repo | **None found** |
| `@Test` annotations across entire repo | **None found** |
| Test runner configuration (maven-surefire, gradle test, etc.) | **None found** |
| CI test steps | **Not assessable from repo content** |
| `EncryptTest.java` classification | **NOT a test file** -- it is a decompiled production encryption utility class (decompiled by DJ v3.9.9.91 on 2006-01-25). Contains `encrypt()` and `decrypt()` methods, no test framework imports, no assertions, no `@Test` annotations. |

**Conclusion:** The repository has **zero automated test coverage**. Every public method in every file has 0% test coverage. All findings below carry an implicit baseline of "no tests exist."

---

## Reading Evidence

### 1. BeanComparator.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/util/BeanComparator.java`
**Class:** `BeanComparator implements Comparator` (raw type)
**Lines:** 1-175

| Line | Visibility | Signature |
|------|-----------|-----------|
| 33 | public | `BeanComparator(Class<?> beanClass, String methodName)` |
| 41 | public | `BeanComparator(Class<?> beanClass, String methodName, boolean isAscending)` |
| 50 | public | `BeanComparator(Class<?> beanClass, String methodName, boolean isAscending, boolean isIgnoreCase)` |
| 81 | public | `void setAscending(boolean isAscending)` |
| 89 | public | `void setIgnoreCase(boolean isIgnoreCase)` |
| 97 | public | `void setNullsLast(boolean isNullsLast)` |
| 106 | public | `int compare(Object object1, Object object2)` |

---

### 2. CftsAlert.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/util/CftsAlert.java`
**Class:** `CftsAlert`
**Lines:** 1-323

| Line | Visibility | Signature |
|------|-----------|-----------|
| 14 | public | `void checkDueDate() throws SQLException` |
| 279 | public | `ArrayList<MymessagesUsersBean> getCustGroupList() throws SQLException` |
| 232 | private | `ArrayList<MymessagesUsersBean> getAlertlist(String cust, String loc) throws SQLException` |

---

### 3. CustomComparator.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/util/CustomComparator.java`
**Class:** `CustomComparator implements Comparator<DriverLeagueBean>`
**Lines:** 1-16

| Line | Visibility | Signature |
|------|-----------|-----------|
| 10 | public | `int compare(DriverLeagueBean o1, DriverLeagueBean o2)` |

---

### 4. CustomUpload.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java`
**Class:** `CustomUpload extends HttpServlet` (annotated `@WebServlet`, `@MultipartConfig`)
**Lines:** 1-518

| Line | Visibility | Signature |
|------|-----------|-----------|
| 45 | protected | `void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException` |
| 301 | public static | `String now(String dateFormat)` |
| 307 | private | `String getFileName(final Part part)` |
| 322 | public | `List<ArrayList<String>> read(String fileName) throws IOException` |
| 355 | private | `boolean validateCSV(ArrayList<String> innerLst, String p)` |
| 378 | private | `boolean validateCSVIndividualD(ArrayList<String> innerLst, ArrayList<String> p)` |
| 407 | private | `boolean validateCSVIndividual(ArrayList<String> innerLst, ArrayList<String> p)` |
| 445 | private | `boolean validateQuestionLenght(ArrayList<String> innerLst, ArrayList<String> p)` |
| 465 | private | `boolean validateQuestionLenghtTab(ArrayList<String> innerLst, ArrayList<String> p)` |
| 484 | private | `boolean validateCSVIndividualTab(ArrayList<String> innerLst, ArrayList<String> p)` |

---

### 5. DBUtil.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/util/DBUtil.java`
**Class:** `DBUtil` (private constructor -- utility class)
**Lines:** 1-58

| Line | Visibility | Signature |
|------|-----------|-----------|
| 20 | public static | `Connection getConnection() throws Exception` |
| 35 | public static | `Connection getMySqlConnection() throws Exception` |
| 51 | public static | `void closeConnection(final Connection conn) throws SQLException` |

---

### 6. DataUtil.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java`
**Class:** `DataUtil`
**Lines:** 1-1087

| Line | Visibility | Signature |
|------|-----------|-----------|
| 48 | public static | `String checkedValue(String value, String dbValue)` |
| 60 | public static | `String checkedValue(String value, ArrayList dbValue)` |
| 72 | public static | `String checkedValue(String value, String[] dbValue)` |
| 85 | public static | `String formatImpact(double value)` |
| 92 | public static | `String checkedValueRadio(String value, String dbValue)` |
| 104 | public static | `String checkedValueCheckbox(String value, ArrayList dbValue)` |
| 118 | public static | `String getDateTime()` |
| 125 | public static | `String getCurrentDate()` |
| 131 | public static | `boolean checkEmptyArray(String[] array)` |
| 144 | public static | `double maxArrayValue(ArrayList<double[]> data)` |
| 159 | public static | `double maxValue(double[] data)` |
| 170 | public static | `double maxValue(ArrayList<Double> list)` |
| 187 | public static | `double sumValue(double[] data)` |
| 197 | public static | `double sumValue(int[] data)` |
| 207 | public static | `double sumValueShift(int[][] data)` |
| 220 | public static | `double maxTotalValue(ArrayList<double[]> data)` |
| 240 | public static | `String generateRadomName()` |
| 251 | public static | `int[] getPreviousMonth()` |
| 263 | public static | `int[] getCurrentMonth()` |
| 275 | public static | `String getMonthForInt(int num)` |
| 285 | public static | `String getDayForInt(int num)` |
| 295 | public static | `String getDateForInt(int year, int month, int day, String format)` |
| 306 | public static | `String getWeekForInt(int num)` |
| 329 | public static | `void saveImage(String imageUrl, String destinationFile) throws IOException` |
| 346 | public static | `String convert_time(int msec)` |
| 415 | public static | `String convert_time_hhmm(int msec)` |
| 489 | public static | `String convert_time(int hour1, int min1, int hour2, int min2)` |
| 509 | public static | `String caculatePercentage(int data1, int data2)` |
| 528 | public static | `String getRandomString(int length)` |
| 538 | public static | `int nthOccurrence(String str, char c, int n)` |
| 545 | public static | `String replaceSpecialCharacter(String str)` |
| 551 | public static | `String formatPercentage(double percentage, int decimal)` |
| 562 | public static | `String dateToString(Date date)` |
| 569 | public static | `String getFileName(String from, String to, String month)` |
| 594 | public static | `String formatdouble(double value)` |
| 600 | public static | `String escapeSpecialCharacter(String str)` |
| 606 | public static | `String convertServiceHour(long miseconds, String format)` |
| 615 | public static | `String formatStringDate(String datString)` |
| 620 | public static | `String formatStringDate2(String datString) throws ParseException` |
| 631 | public static | `String formatdoubletoInt(double value)` |
| 636 | public static | `double caculateImpPercentage(int data1, int data2)` |
| 655 | public static | `String addMonthToDate(String date, int inc)` |
| 664 | public static | `String calculateLastServTypeCO(String servHour, String hourAtLastServ)` |
| 682 | public static | `String calculateNextServTypeDue(String servHour, String hourAtLastServ)` |
| 694 | public static | `String getColourStatus(int hours)` |
| 709 | public static | `String log()` |
| 716 | public static | `int compareDates(String d1, String d2)` |
| 754 | public static | `boolean checkDateFormat(String format)` |
| 771 | public static | `String getMonthStr(int month)` |
| 776 | public static | `String removeDuplicateCds(String s)` |
| 800 | public static | `String getShortDayForInt(int num)` |
| 810 | public static | `String convertToImpPerc(String imp)` |
| 839 | public static | `String getProductType(String firVer)` |
| 862 | public static | `int calculateTime(String type, String st, String end)` |
| 903 | public static | `String getFileName(final Part part)` |
| 918 | public static | `void uploadLicenceFile(HttpServletRequest request, Part filePart, String filename) throws IOException` |
| 936 | public static | `void uploadDocumentFile(HttpServletRequest request, Part filePart, String cust_loc, String veh_cd) throws IOException` |
| 961 | public static | `boolean isVehichleDurationHired(Timestamp utc_time, List<DehireBean> dehireBean)` |
| 995 | public static | `boolean isVehichleDurationHired(Timestamp startDate, Timestamp endDate, List<DehireBean> dehireBean)` |
| 1052 | public static | `List<String> getLocationFilter(String customer, String accessUser)` |
| 1084 | public static | `boolean isForVisyLimitingLocations(String customer, String accessUser)` |

---

### 7. DateUtil.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/util/DateUtil.java`
**Class:** `DateUtil`
**Lines:** 1-360

| Line | Visibility | Signature |
|------|-----------|-----------|
| 16 | public static | `Date stringToDate(String str_date)` |
| 32 | public static | `Date getDaysDate(Date date, int days)` |
| 39 | public static | `String dateToString(Date date)` |
| 45 | public static | `java.sql.Date stringToSQLDate(String str_date)` |
| 73 | public static | `Timestamp getLocalTimestamp()` |
| 80 | public static | `Date getStartDate(Date date, String freqency)` |
| 103 | public static | `Date getNxtMthDate(Date date)` |
| 113 | public static | `Timestamp getLocalTimestamp(String timezoneName, Locale clientLocale) throws Exception` |
| 130 | public static | `String getUTCTime() throws Exception` |
| 138 | public static | `Date getLocalTime(String timezoneName, Locale clientLocale) throws Exception` |
| 154 | public static | `boolean isValidDate(String time)` |
| 171 | public static | `boolean isValidDates(String date)` |
| 189 | public static | `Timestamp stringToTimestamp(String str_date) throws Exception` |
| 208 | public static | `Timestamp stringToTimestampHM(String str_date) throws Exception` |
| 227 | public static | `long StringTimeDifference(String time1, String time2, TimeUnit timeUnit, String format)` |
| 250 | public static | `String GetDateNow()` |
| 257 | public static | `String GetDate()` |
| 264 | public static | `Boolean compareDates(String comparDates) throws ParseException` |
| 282 | public static | `Boolean compareDateTime(String Date1, String Date2) throws ParseException` |
| 298 | public static | `ArrayList<Integer> GetCalendar(String time, String format)` |
| 320 | public static | `String getDateString(String sDate, int n)` |
| 325 | public static | `String getDuration(String dateStart, String dateStop)` |

---

### 8. DriverExpiryAlert.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/util/DriverExpiryAlert.java`
**Class:** `DriverExpiryAlert`
**Lines:** 1-211

| Line | Visibility | Signature |
|------|-----------|-----------|
| 15 | public | `void checkExpiry() throws SQLException` |
| 163 | private | `ArrayList<MymessagesUsersBean> getAlertlist() throws SQLException` |

---

### 9. DriverMedicalAlert.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/util/DriverMedicalAlert.java`
**Class:** `DriverMedicalAlert`
**Lines:** 1-231

| Line | Visibility | Signature |
|------|-----------|-----------|
| 18 | public | `void checkInterval() throws SQLException` |
| 179 | public static | `String getDate(Calendar cal)` |
| 183 | private | `ArrayList<MymessagesUsersBean> getAlertlist() throws SQLException` |

**Note:** `private static SimpleDateFormat sdf` at line 16 is a shared mutable instance -- thread-safety issue.

---

### 10. Dt_Checker.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/util/Dt_Checker.java`
**Class:** `Dt_Checker`
**Lines:** 1-242

| Line | Visibility | Signature |
|------|-----------|-----------|
| 11 | public static | `boolean greaterThan(String dt2, String dt1)` |
| 53 | public static | `boolean equalTo(String dt1, String dt2)` |
| 84 | public static | `String first(String dt)` |
| 109 | public static | `String last(String dt)` |
| 141 | public static | `boolean isleap(int y)` |
| 153 | public static | `boolean between(String dt1, String dt2, String dt3)` |
| 164 | public static | `boolean conflict(String dt1, String dt2, String dt3, String dt4)` |
| 178 | public static | `int days_Betn(String dt1, String dt2)` |
| 212 | public static | `int daysIn(int d, int m, int y)` |
| 234 | public | `void init()` |

---

### 11. EncryptTest.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/util/EncryptTest.java`
**Class:** `EncryptTest` (decompiled production code, NOT a test)
**Lines:** 1-114

| Line | Visibility | Signature |
|------|-----------|-----------|
| 12 | public | `EncryptTest()` |
| 16 | public | `StringBuffer encrypt(String s)` |
| 97 | public | `StringBuffer decrypt(String s)` |

---

### 12. ExcelUtil.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/util/ExcelUtil.java`
**Class:** `ExcelUtil`
**Lines:** 1-146

| Line | Visibility | Signature |
|------|-----------|-----------|
| 30 | public | `ExcelUtil() throws Exception` |
| 34 | public | `void getExcel(String rpt_name, String params, HttpServletResponse response)` |
| 61 | public | `void getEmail(String rpt_name, String params, boolean isConf)` |
| 84 | public | `String getPrintBody(String rpt_name, String params)` |
| 107 | public | `void downloadExcel(HttpServletResponse response)` |
| 129 | public | `boolean sendEmail(String subject, String mail_id)` |
| 134 | public | `String getExportDir()` |

---

### 13. FleetCheckFTP.java
**Path:** `WEB-INF/src/com/torrent/surat/fms6/util/FleetCheckFTP.java`
**Class:** `FleetCheckFTP`
**Lines:** 1-277

| Line | Visibility | Signature |
|------|-----------|-----------|
| 24 | public | `void upload_quest_ftp() throws SQLException` |

---

## Findings

### A19-01 -- CRITICAL: Zero test infrastructure across entire repository
**Severity:** CRITICAL
**Files:** ALL (repository-wide)

The repository contains no test framework dependencies (JUnit, TestNG, etc.), no test directories, no test runner configuration, and no test files. Every public method across all 13 files has 0% automated test coverage. This means:
- No regression safety net exists for any code change.
- No validation of date parsing, encryption, SQL generation, or file handling logic.
- Refactoring is high-risk without manual verification.

**Recommended priority:** Establish JUnit 5 test infrastructure with at minimum unit tests for pure-logic utility methods (DataUtil, DateUtil, Dt_Checker, BeanComparator, EncryptTest).

---

### A19-02 -- CRITICAL: DBUtil is the sole database connection gateway -- untested
**Severity:** CRITICAL
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/DBUtil.java`
**Methods:** `getConnection()` (line 20), `getMySqlConnection()` (line 35), `closeConnection()` (line 51)

DBUtil is the central connection factory used by CftsAlert, DriverExpiryAlert, DriverMedicalAlert, and FleetCheckFTP. There are no tests for:
- Connection acquisition failure handling (JNDI lookup failure, pool exhaustion).
- `closeConnection()` when given an already-closed connection (will throw).
- `getConnection()` throws raw `Exception` rather than a more specific type.
- No connection pooling validation or leak detection tests.

**Risk:** A failure in `getConnection()` cascades to every DB-dependent feature in the application.

---

### A19-03 -- CRITICAL: SQL Injection vulnerabilities in alert classes -- untested
**Severity:** CRITICAL
**Files:**
- `CftsAlert.java` -- lines 45, 79, 85, 115, 124, 147, 174, 184, 206, 248
- `DriverExpiryAlert.java` -- lines 70-86, 105, 114, 123, 134, 144
- `DriverMedicalAlert.java` -- lines 64-70, 74-80, 125, 143, 161
- `FleetCheckFTP.java` -- lines 84, 100, 221, 230-231, 235, 242-243, 246

All four classes build SQL queries via string concatenation with variables that originate from database result sets. While the immediate values come from the DB (not direct user input), this pattern is still dangerous:
- Values like `cust`, `site`, `email`, `message`, `subsject` (sic), and `gmtp_id` are concatenated directly into SQL.
- CftsAlert line 147: email addresses and message content (which may contain single quotes) are inserted into an `INSERT` statement -- any name or message containing `'` will cause SQL errors or injection.
- FleetCheckFTP line 229: FTP commands containing commas and special characters are concatenated into SQL.

**No tests exist** to verify query correctness or to catch injection vectors.

---

### A19-04 -- CRITICAL: EncryptTest encrypt/decrypt logic is untested
**Severity:** CRITICAL
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/EncryptTest.java`
**Methods:** `encrypt(String)` (line 16), `decrypt(String)` (line 97)

This class handles password/data encryption for the application. Key concerns:
- **The algorithm is a simple character-shift cipher** (add/subtract position index) -- this is not real encryption, just trivial obfuscation.
- `encrypt()` prepends a 10-character fixed prefix based on input length. `decrypt()` strips the first 10 characters then reverses the shift.
- **No round-trip tests exist** to verify `decrypt(encrypt(x)) == x`.
- **No edge-case tests:** empty string input, null input, special characters, Unicode characters, very long strings.
- The class was decompiled from a 2006 binary -- the original source may have been lost.

**Risk:** Password handling code with zero verification of correctness.

---

### A19-05 -- HIGH: Dt_Checker.isleap() has an incorrect leap year algorithm
**Severity:** HIGH
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/Dt_Checker.java`
**Method:** `isleap(int y)` (line 141)

The leap year logic is wrong:
```java
if (y%1000 == 0) { return true; }   // Should be y%100==0 -> false (unless also %400)
if (y%400 == 0) { return false; }    // 400 should return TRUE, not false
if (y%4 == 0) { return true; }
return false;
```
- Year 2000: `2000 % 1000 == 0` returns `true` (correct by accident).
- Year 1900: `1900 % 1000 != 0`, `1900 % 400 != 0`, `1900 % 4 == 0` returns `true` -- **WRONG** (1900 is not a leap year).
- Year 2400: `2400 % 1000 != 0`, `2400 % 400 == 0` returns `false` -- **WRONG** (2400 is a leap year).
- Year 3000: `3000 % 1000 == 0` returns `true` -- **WRONG** (3000 is not a leap year).

This bug affects `last()`, `daysIn()`, and `days_Betn()` -- any date calculation spanning February in affected years will be incorrect.

**No tests exist** to catch this logic error. A simple parameterized test would immediately expose it.

---

### A19-06 -- HIGH: Dt_Checker uses static mutable fields -- thread-unsafe
**Severity:** HIGH
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/Dt_Checker.java`
**Line:** 6-7

```java
static String date1, dd, mm, yy;
public String methodName, beanName = "Dt_Checker";
```

The `first()` (line 84) and `last()` (line 109) methods write to the static fields `date1`, `dd`, `mm`, `yy`. In a multi-threaded Tomcat environment, concurrent calls will corrupt shared state.

**No tests exist** to verify thread safety or detect race conditions.

---

### A19-07 -- HIGH: DateUtil.stringToSQLDate ambiguous date format detection
**Severity:** HIGH
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/DateUtil.java`
**Method:** `stringToSQLDate(String)` (line 45)

The method attempts to auto-detect dd/MM/yyyy vs MM/dd/yyyy format:
```java
if(Integer.parseInt(dArray[1]) > 12){
    formatter = new SimpleDateFormat("MM/dd/yyyy");
}
if(Integer.parseInt(dArray[0]) > 12 ){
    formatter = new SimpleDateFormat("dd/MM/yyyy");
}
```
- For dates like `05/06/2024`, the method cannot distinguish 5th June from May 6th. It defaults to `dd/MM/yyyy`.
- For `13/05/2024`, the second check overrides back to `dd/MM/yyyy` (correct).
- For `05/13/2024`, the first check switches to `MM/dd/yyyy` (correct).
- For `12/12/2024`, ambiguous -- silently picks `dd/MM/yyyy`.

**No tests exist** to validate this heuristic. Edge cases (both values <= 12) will produce silent wrong results.

---

### A19-08 -- HIGH: DataUtil has 40+ pure-logic static methods with zero tests
**Severity:** HIGH
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java`

DataUtil is the largest utility class (1087 lines, 40+ public static methods). Many methods are pure functions with no external dependencies -- ideal for unit testing but completely untested. Key untested edge cases:

| Method | Line | Untested Edge Cases |
|--------|------|-------------------|
| `maxValue(double[])` | 159 | Empty array (ArrayIndexOutOfBoundsException) |
| `maxValue(ArrayList<Double>)` | 170 | Returns 0 for null/empty -- inconsistent with `double[]` overload which crashes |
| `maxArrayValue(ArrayList<double[]>)` | 144 | Empty outer list, empty inner arrays |
| `convert_time(int)` | 346 | Negative values cause infinite loop at line 354 (`while (secs < 0) secs = 86400 + secs`) when `msec` is extremely negative |
| `formatStringDate(String)` | 615 | Strings shorter than 10 chars (StringIndexOutOfBoundsException) |
| `formatStringDate2(String)` | 620 | Strings shorter than 10 chars (StringIndexOutOfBoundsException) |
| `addMonthToDate(String, int)` | 655 | Non-dd/MM/yyyy input (ArrayIndexOutOfBoundsException / NumberFormatException) |
| `getMonthStr(int)` | 771 | Index out of bounds (negative or >= 12) |
| `removeDuplicateCds(String)` | 776 | Empty string, single element, trailing commas |
| `calculateTime(String, String, String)` | 862 | Unrecognized `type` parameter returns -1 silently |
| `getRandomString(int)` | 528 | Off-by-one: loop is `i <= length` (returns length+1 characters) |
| `checkDateFormat(String)` | 754 | Regex `[20]{2}` matches "00", "02", "22" etc -- not just "20" prefix |
| `convertToImpPerc(String)` | 810 | Non-numeric string input causes NumberFormatException; depends on `LindeConfig.siteName` static field |

---

### A19-09 -- HIGH: File upload methods have no path traversal protection -- untested
**Severity:** HIGH
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java`
**Methods:**
- `uploadLicenceFile()` (line 918) -- hardcoded base path `/home/gmtp/fms_files/licence/`
- `uploadDocumentFile()` (line 936) -- constructs path from `cust_loc` parameter

**File:** `WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java`
**Method:** `doPost()` (line 45) -- uses `getFileName(filePart)` to derive file name from HTTP header

None of these methods validate that the resulting file path stays within the intended directory. A crafted filename containing `../` sequences could write files to arbitrary locations. `CustomUpload.getFileName()` at line 307 extracts the filename from the `content-disposition` header but does no sanitization beyond removing quotes.

**No tests exist** to verify path traversal protection.

---

### A19-10 -- HIGH: CustomUpload servlet has multiple untested critical paths
**Severity:** HIGH
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/CustomUpload.java`

Critical untested concerns:
1. **Hardcoded email** (line 55): `julius@collectiveintelligence.com.au` as default email recipient.
2. **Hardcoded file path** (line 108): `/home/gmtp/csv/file.csv` -- concurrent requests overwrite the same file.
3. **Hardcoded firmware path/credentials** (line 219): FTP server credentials (`Sdh79HfkLq6`) in source code.
4. **SQL injection in firmware action** (line 221): `gmtpId` and `message` concatenated into SQL.
5. **No authentication check** visible in `doPost()`.
6. **BufferedReader not closed** in `read()` method (line 327).

---

### A19-11 -- HIGH: BeanComparator reflection-based comparison is untested
**Severity:** HIGH
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/BeanComparator.java`
**Method:** `compare(Object, Object)` (line 106)

Untested scenarios:
- Method invocation throwing `IllegalAccessException` or `InvocationTargetException` (wraps in RuntimeException).
- Comparing objects that return non-Comparable, non-String types.
- Uses raw `Comparator` type -- no generic type safety.
- Null object arguments (will throw NullPointerException at line 113).

---

### A19-12 -- HIGH: ExcelUtil uses dynamic class loading with unsanitized input
**Severity:** HIGH
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/ExcelUtil.java`
**Methods:** `getExcel()` (line 34), `getEmail()` (line 61), `getPrintBody()` (line 84)

All three methods use `Class.forName("com.torrent.surat.fms6.excel.reports." + rpt_name)` where `rpt_name` comes from the caller (ultimately from HTTP parameters). If not validated upstream, this enables:
- Arbitrary class instantiation within the package.
- Denial-of-service via `ClassNotFoundException`.

`downloadExcel()` (line 107) reads files byte-by-byte (line 118: `fileInputStream.read()`) -- extremely slow for large files. No buffer is used.

**No tests exist** for any of these code paths.

---

### A19-13 -- HIGH: FleetCheckFTP combines file I/O, DB, and FTP -- completely untested
**Severity:** HIGH
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/FleetCheckFTP.java`
**Method:** `upload_quest_ftp()` (line 24)

This 250-line method:
- Queries the database for pending FTP uploads.
- Creates directory trees on the filesystem (lines 116-175).
- Writes binary `PREOP.TXT` files (lines 183-225).
- Inserts outgoing FTP commands into the database (lines 229-244).
- Deletes processed records (line 246).

All SQL uses string concatenation (injection risk). The method is monolithic with no unit-testable decomposition. The class comment (lines 18-22) notes it may not even be actively called.

**Risk:** Any change to this file is high-risk with no test safety net.

---

### A19-14 -- MEDIUM: DriverMedicalAlert uses shared mutable SimpleDateFormat
**Severity:** MEDIUM
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/DriverMedicalAlert.java`
**Line:** 16

```java
private static SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy");
```

`SimpleDateFormat` is not thread-safe. In a Tomcat environment with concurrent requests, this will produce corrupted date strings or throw `NumberFormatException`.

**No tests exist** to verify thread safety.

---

### A19-15 -- MEDIUM: CustomComparator will NPE on null driver names
**Severity:** MEDIUM
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/CustomComparator.java`
**Method:** `compare()` (line 10)

```java
return o2.getDriverName().compareTo(o1.getDriverName());
```

If either `o1`, `o2`, or their `getDriverName()` return is null, a `NullPointerException` is thrown. Unlike `BeanComparator`, this class has no null handling.

**No tests exist.**

---

### A19-16 -- MEDIUM: Alert classes swallow exceptions silently
**Severity:** MEDIUM
**Files:** `CftsAlert.java` (line 217-221), `DriverExpiryAlert.java` (line 150-154), `DriverMedicalAlert.java` (line 166-169)

All three alert classes catch `Exception`, call `e.printStackTrace()` and `e.getMessage()` (the return value of `getMessage()` is discarded), then continue execution. This means:
- Partial alert processing failures are silently ignored.
- No error is propagated to callers.
- `e.getMessage()` on line 220/153/169 is a no-op statement (return value unused).

**No tests exist** to verify error handling behavior.

---

### A19-17 -- MEDIUM: DateUtil methods return null on parse failure instead of throwing
**Severity:** MEDIUM
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/DateUtil.java`
**Methods:** `stringToDate()` (line 16), `stringToTimestamp()` (line 189), `stringToTimestampHM()` (line 208)

These methods catch `ParseException`, print to stdout, and return null. Callers who do not check for null will get `NullPointerException` at a distance from the actual error.

**No tests exist** to verify null-return behavior or to document the contract.

---

### A19-18 -- MEDIUM: DataUtil.saveImage has resource leak potential
**Severity:** MEDIUM
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java`
**Method:** `saveImage(String, String)` (line 329)

Streams `is` and `os` are closed sequentially (lines 342-343) without try-with-resources. If `os.close()` or any `os.write()` throws, `is` may not be closed. Similarly, `uploadDocumentFile()` (line 936) never closes `outStream` (missing `outStream.close()` -- only appears to be absent at line 958).

**No tests exist.**

---

### A19-19 -- LOW: DataUtil.getRandomString off-by-one error
**Severity:** LOW
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java`
**Method:** `getRandomString(int length)` (line 528)

```java
for (int i = 0; i <= length; i++) {
```

The loop condition `i <= length` generates `length + 1` characters instead of `length`. Calling `getRandomString(8)` returns a 9-character string.

**No tests exist** to catch this off-by-one.

---

### A19-20 -- LOW: DataUtil.checkDateFormat regex is incorrect
**Severity:** LOW
**File:** `WEB-INF/src/com/torrent/surat/fms6/util/DataUtil.java`
**Method:** `checkDateFormat(String)` (line 754)

The year portion regex `([20]{2}[0-9]{2})` uses a character class `[20]` meaning "any character that is '2' or '0'" -- it matches "00xx", "02xx", "22xx", "20xx". It does not enforce the prefix "20". For example, `"01/01/0099"` would match.

**No tests exist.**

---

## Summary Statistics

| Severity | Count |
|----------|-------|
| CRITICAL | 4 |
| HIGH | 10 |
| MEDIUM | 6 |
| LOW | 2 |
| **Total** | **22** |

### Priority Test Targets (highest value-to-effort ratio for new tests)

1. **Dt_Checker** -- All methods are pure static functions. Easy to test. Will immediately expose the leap year bug (A19-05) and thread-safety issue (A19-06).
2. **EncryptTest encrypt/decrypt** -- Pure functions, trivial to test round-trip correctness.
3. **DataUtil pure functions** -- `maxValue`, `convert_time`, `formatStringDate`, `addMonthToDate`, `getRandomString`, `checkDateFormat`, `calculateTime`.
4. **DateUtil parsing methods** -- `stringToDate`, `stringToSQLDate`, `isValidDate`, `isValidDates`, `stringToTimestamp`.
5. **BeanComparator** -- Reflection-based comparator, testable with simple bean classes.
6. **CustomComparator** -- Trivial one-method class, easy to cover including null case.

### Classes requiring integration test infrastructure (DB mocking)

7. **DBUtil** -- Requires JNDI mock or embedded database.
8. **CftsAlert, DriverExpiryAlert, DriverMedicalAlert** -- Require DB mocking; should also test SQL injection scenarios.
9. **FleetCheckFTP** -- Requires DB + filesystem mocking.
10. **CustomUpload** -- Requires servlet container mock (HttpServletRequest/Response).
11. **ExcelUtil** -- Requires mock HttpServletResponse and report class stubs.
