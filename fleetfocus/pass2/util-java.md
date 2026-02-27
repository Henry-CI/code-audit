# Test Coverage Audit — util Package
**Agent:** A03
**Date:** 2026-02-25
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Package:** `com.torrent.surat.fms6.util`
**Total files audited:** 37

---

## Reading Evidence

### BeanComparator.java
**Class:** `BeanComparator` — implements `Comparator`
| Line | Method / Constructor |
|------|----------------------|
| 33 | `BeanComparator(Class<?> beanClass, String methodName)` |
| 41 | `BeanComparator(Class<?> beanClass, String methodName, boolean isAscending)` |
| 50 | `BeanComparator(Class<?> beanClass, String methodName, boolean isAscending, boolean isIgnoreCase)` |
| 81 | `public void setAscending(boolean isAscending)` |
| 89 | `public void setIgnoreCase(boolean isIgnoreCase)` |
| 97 | `public void setNullsLast(boolean isNullsLast)` |
| 106 | `public int compare(Object object1, Object object2)` |

Fields: `EMPTY_CLASS_ARRAY`, `EMPTY_OBJECT_ARRAY`, `method`, `isAscending`, `isIgnoreCase`, `isNullsLast`

---

### CustomComparator.java
**Class:** `CustomComparator` — implements `Comparator<DriverLeagueBean>`
| Line | Method |
|------|--------|
| 10 | `public int compare(DriverLeagueBean o1, DriverLeagueBean o2)` |

Note: TODO stub comment present. Sort order is descending by driver name.

---

### CftsAlert.java
**Class:** `CftsAlert` — alert scheduler
| Line | Method |
|------|--------|
| 14 | `public void checkDueDate() throws SQLException` |
| (private) | `getCustGroupList()` (called but not visible in excerpt) |

Uses `DataUtil.calculateTime()`. Sends inspection-due emails.

---

### CustomUpload.java
**Class:** `CustomUpload extends HttpServlet` — mapped to `/servlet/Import_Files`
| Line | Method |
|------|--------|
| 45 | `protected void doPost(HttpServletRequest request, HttpServletResponse response)` |
| 301 | `public static String now(String dateFormat)` |
| 307 | `private String getFileName(final Part part)` |
| 322 | `public List<ArrayList<String>> read(String fileName) throws IOException` |
| 355 | `private boolean validateCSV(ArrayList<String> innerLst, String p)` |
| 378 | `private boolean validateCSVIndividualD(ArrayList<String> innerLst, ArrayList<String> p)` |
| 407 | `private boolean validateCSVIndividual(ArrayList<String> innerLst, ArrayList<String> p)` |
| 445 | `private boolean validateQuestionLenght(ArrayList<String> innerLst, ArrayList<String> p)` |
| 465 | `private boolean validateQuestionLenghtTab(ArrayList<String> innerLst, ArrayList<String> p)` |
| 484 | `private boolean validateCSVIndividualTab(ArrayList<String> innerLst, ArrayList<String> p)` |

Important: accepts file upload, saves directly to filesystem with user-supplied filename (line 77). No file type validation. Contains hardcoded FTP credentials in a message string at line 219: `Sdh79HfkLq6`. Action `firmware` builds outgoing FTP firmware push commands.

---

### DataUtil.java
**Class:** `DataUtil` — static utility class, 1087 lines
| Line | Method |
|------|--------|
| 48 | `public static String checkedValue(String value, String dbValue)` |
| 60 | `public static String checkedValue(String value, ArrayList dbValue)` |
| 72 | `public static String checkedValue(String value, String[] dbValue)` |
| 85 | `public static String formatImpact(double value)` |
| 92 | `public static String checkedValueRadio(String value, String dbValue)` |
| 104 | `public static String checkedValueCheckbox(String value, ArrayList dbValue)` |
| 118 | `public static String getDateTime()` |
| 125 | `public static String getCurrentDate()` |
| 131 | `public static boolean checkEmptyArray(String[] array)` |
| 144 | `public static double maxArrayValue(ArrayList<double[]> data)` |
| 159 | `public static double maxValue(double[] data)` |
| 170 | `public static double maxValue(ArrayList<Double> list)` |
| 187 | `public static double sumValue(double[] data)` |
| 197 | `public static double sumValue(int[] data)` |
| 207 | `public static double sumValueShift(int[][] data)` |
| 220 | `public static double maxTotalValue(ArrayList<double[]> data)` |
| 240 | `public static String generateRadomName()` |
| 251 | `public static int[] getPreviousMonth()` |
| 263 | `public static int[] getCurrentMonth()` |
| 275 | `public static String getMonthForInt(int num)` |
| 285 | `public static String getDayForInt(int num)` |
| 295 | `public static String getDateForInt(int year, int month, int day, String format)` |
| 306 | `public static String getWeekForInt(int num)` |
| 329 | `public static void saveImage(String imageUrl, String destinationFile) throws IOException` |
| 346 | `public static String convert_time(int msec)` |
| 415 | `public static String convert_time_hhmm(int msec)` |
| 489 | `public static String convert_time(int hour1, int min1, int hour2, int min2)` |
| 509 | `public static String caculatePercentage(int data1, int data2)` |
| 528 | `public static String getRandomString(int length)` |
| 538 | `public static int nthOccurrence(String str, char c, int n)` |
| 545 | `public static String replaceSpecialCharacter(String str)` |
| 551 | `public static String formatPercentage(double percentage, int decimal)` |
| 562 | `public static String dateToString(Date date)` |
| 569 | `public static String getFileName(String from, String to, String month)` |
| 594 | `public static String formatdouble(double value)` |
| 600 | `public static String escapeSpecialCharacter(String str)` |
| 606 | `public static String convertServiceHour(long miseconds, String format)` |
| 615 | `public static String formatStringDate(String datString)` |
| 620 | `public static String formatStringDate2(String datString) throws ParseException` |
| 631 | `public static String formatdoubletoInt(double value)` |
| 636 | `public static double caculateImpPercentage(int data1, int data2)` |
| 655 | `public static String addMonthToDate(String date, int inc)` |
| 664 | `public static String calculateLastServTypeCO(String servHour, String hourAtLastServ)` |
| 682 | `public static String calculateNextServTypeDue(String servHour, String hourAtLastServ)` |
| 694 | `public static String getColourStatus(int hours)` |
| 709 | `public static String log()` |
| 716 | `public static int compareDates(String d1, String d2)` |
| 754 | `public static boolean checkDateFormat(String format)` |
| 771 | `public static String getMonthStr(int month)` |
| 776 | `public static String removeDuplicateCds(String s)` |
| 800 | `public static String getShortDayForInt(int num)` |
| 810 | `public static String convertToImpPerc(String imp)` |
| 839 | `public static String getProductType(String firVer)` |
| 862 | `public static int calculateTime(String type, String st, String end)` |
| 903 | `public static String getFileName(final Part part)` |
| 918 | `public static void uploadLicenceFile(HttpServletRequest request, Part filePart, String filename) throws IOException` |
| 936 | `public static void uploadDocumentFile(HttpServletRequest request, Part filePart, String cust_loc, String veh_cd) throws IOException` |
| 961 | `public static boolean isVehichleDurationHired(Timestamp utc_time, List<DehireBean> dehireBean)` |
| 995 | `public static boolean isVehichleDurationHired(Timestamp startDate, Timestamp endDate, List<DehireBean> dehireBean)` |
| 1052 | `public static List<String> getLocationFilter(String customer, String accessUser)` |
| 1084 | `public static boolean isForVisyLimitingLocations(String customer, String accessUser)` |

Key security note: `uploadLicenceFile()` line 919 hardcodes base path `/home/gmtp/fms_files/licence/` and writes with caller-supplied `filename` directly — no sanitisation. `uploadDocumentFile()` uses `cust_loc` in path construction at line 937 and `fName` from multipart header (line 951) with only space-to-underscore replacement — no traversal prevention. `escapeSpecialCharacter()` at line 600 removes `[-+.^:, ]` but does **not** strip `../` sequences.

---

### DateUtil.java
**Class:** `DateUtil` — date/time utilities
| Line | Method |
|------|--------|
| 16 | `public static Date stringToDate(String str_date)` |
| 32 | `public static Date getDaysDate(Date date, int days)` |
| 39 | `public static String dateToString(Date date)` |
| 45 | `public static java.sql.Date stringToSQLDate(String str_date)` |
| 73 | `public static Timestamp getLocalTimestamp()` |
| 80 | `public static Date getStartDate(Date date, String freqency)` |
| (further) | Additional date range/period methods |

`stringToSQLDate()` contains faulty format-detection logic (lines 53–58): if day > 12, assumes `dd/MM/yyyy`; if month > 12, also assumes `dd/MM/yyyy`. Both branches lead to the same format — the US-format fallback `MM/dd/yyyy` may be silently applied incorrectly, introducing date corruption.

---

### DBUtil.java
**Class:** `DBUtil` — database connection factory (private constructor, static-only)
| Line | Method |
|------|--------|
| 20 | `public static Connection getConnection() throws Exception` |
| 35 | `public static Connection getMySqlConnection() throws Exception` |
| 51 | `public static void closeConnection(final Connection conn) throws SQLException` |

---

### DriverExpiryAlert.java
**Class:** `DriverExpiryAlert` — email alert scheduler
| Line | Method |
|------|--------|
| 15 | `public void checkExpiry() throws SQLException` |
| (private) | `getAlertlist()` (called, not in excerpt) |

---

### DriverMedicalAlert.java
**Class:** `DriverMedicalAlert` — email alert scheduler
| Line | Method |
|------|--------|
| 18 | `public void checkInterval() throws SQLException` |
| (private) | `getAlertlist()` |

---

### Dt_Checker.java
**Class:** `Dt_Checker` — string-based date comparison utility
| Line | Method |
|------|--------|
| 11 | `public static boolean greaterThan(String dt2, String dt1)` |
| 53 | `public static boolean equalTo(String dt1, String dt2)` |
| 84 | `public static String first(String dt)` |
| 109 | `public static String last(String dt)` |
| 141 | `public static boolean isleap(int y)` |
| 153 | `public static boolean between(String dt1, String dt2, String dt3)` |
| 164 | `public static boolean conflict(String dt1, String dt2, String dt3, String dt4)` |
| 178 | `public static int days_Betn(String dt1, String dt2)` |
| 212 | `public static int daysIn(int d, int m, int y)` |
| 234 | `public void init()` |

Note: `isleap()` logic is wrong (line 143: `y%1000 == 0` returns true, but `y%400 == 0` returns false — this inverts the rule for 1000-year multiples vs 400-year multiples). All methods parse dates manually without validation — any malformed input causes `StringIndexOutOfBoundsException` or `NumberFormatException`.

---

### EncryptTest.java
**Class:** `EncryptTest` — password encryption (decompiled 2006-era code)
| Line | Method |
|------|--------|
| 12 | `public EncryptTest()` |
| 16 | `public StringBuffer encrypt(String s)` |
| 97 | `public StringBuffer decrypt(String s)` |

Algorithm: prepends a 10-character "salt" based on input length bracket (5 brackets), then shifts chars by position index (odd positions: +i+1, even positions: -i+1). `decrypt()` strips the first 10 chars then reverses the shift. **This is NOT cryptographically secure** — it is a trivially reversible Caesar-style cipher. If input is empty or null, `encrypt()` appends the length-1–4 bracket prefix and then the loop runs 0 times (empty input returns 10-char prefix only). `decrypt()` on a string shorter than 10 chars throws `StringIndexOutOfBoundsException` (line 100: `s1.substring(10)`).

---

### ExcelUtil.java
**Class:** `ExcelUtil` — reflection-based Excel report generator
| Line | Method |
|------|--------|
| 30 | `public ExcelUtil() throws Exception` |
| 34 | `public void getExcel(String rpt_name, String params, HttpServletResponse response)` |
| 61 | `public void getEmail(String rpt_name, String params, boolean isConf)` |
| 84 | `public String getPrintBody(String rpt_name, String params)` |
| 107 | `public void downloadExcel(HttpServletResponse response)` |
| 129 | `public boolean sendEmail(String subject, String mail_id)` |
| 134 | `public String getExportDir()` |

Security note: `getExcel()` and `getEmail()` use `Class.forName()` on a caller-supplied `rpt_name` without validation — potential reflection injection if `rpt_name` is derived from user input. `getExportDir()` constructs a path with `../../../../../../../../excelrpt/` — deep relative path traversal from the JAR location.

---

### fix_department.java
**Class:** `fix_department` — administrative data-fix utility
| Line | Method |
|------|--------|
| 24 | `public void show_cust_dept() throws SQLException` |

Fields: `customers`, `sites`, `departments`, `user_cds`, `loc_cds`, `dept_cds` (ArrayList members, not shown in excerpt but referenced).

---

### FleetCheckFTP.java
**Class:** `FleetCheckFTP` — FTP file push to firmware units
| Line | Method |
|------|--------|
| 24 | `public void upload_quest_ftp() throws SQLException` |

Contains class-level note (lines 18–23): "As of March 10, 2023 testing, this is not being called by the stored proc." Uses `ftp_outgoing` table that "is never existing in the live site." Builds FTP command strings with `RuntimeConf.firmwarepass = "Sdh79HfkLq6"`. Concatenates `gmtp_id` and `ftp_upld_cmd` directly into SQL (line 230–231) — SQL injection via unsanitised `gmtp_id`.

---

### GdprDataDelete.java
**Class:** `GdprDataDelete` — scheduled GDPR data deletion
| Line | Method |
|------|--------|
| 29 | `public void call_gdpr_delete_data() throws SQLException` |

Fields: `stmte`, `stmte1`, `combine`, `sEmail`, `sName`

Critical SQL injection: the `gdpr_data` value (from column `gdpr_data` in `FMS_CUST_MST`) and `driver_cd` values are interpolated directly into DELETE statements at lines 73–95. Example: `"delete from \"fms_io_data\" where ... and \"driver_cd\"='"+driver_cd.get(i)+"'"`. If `gdpr_data` or any driver code contains SQL metacharacters, this will execute malformed or malicious SQL against production data. The method permanently deletes records from six tables: `fms_io_data_dtl`, `fms_io_data`, `fms_stat_data_dtl`, `fms_stat_data`, `fms_usage_data_dtl`, `fms_usage_data`, `op_chk_checklistanswer`, `op_chk_checklistresult`, `fms_unit_unlock_data`.

---

### GetHtml.java
**Class:** `GetHtml` — internal HTTP GET utility
| Line | Method |
|------|--------|
| 16 | `public String getHTML(String urlToRead, String param)` |

Concatenates `urlToRead + param` directly (line 24) — SSRF risk if either argument is user-controlled. Timeout set to 600,000 ms (10 minutes).

---

### ImportFiles.java
**Class:** `ImportFiles extends HttpServlet` — mapped to `/servlet/Import_Files`
| Line | Method |
|------|--------|
| 49 | `protected void doPost(HttpServletRequest request, HttpServletResponse response)` |
| (private) | `getFileName(final Part part)` |
| (private) | `read(String fileName)` |
| (private) | `readQuestions(String fileName)` |
| (private) | `validateCSV(ArrayList<String> innerLst, String p)` |
| (private) | `validateCSVIndividualD(ArrayList<String> innerLst, ArrayList<String> p)` |
| (private) | `validateCSVIndividual(ArrayList<String> innerLst, ArrayList<String> p)` |
| (private) | `validateQuestionLenght(ArrayList<String> innerLst, ArrayList<String> p)` |
| (private) | `validateQuestionLenghtTab(ArrayList<String> innerLst, ArrayList<String> p)` |
| (private) | `validateCSVIndividualTab(ArrayList<String> innerLst, ArrayList<String> p)` |

Handles `src` types: `drivers`, `driversUK`, `vehicles`, `questions`, and others. File saved with original client-supplied filename. No file type enforcement — any file extension is accepted. `driversUK` format expects row index 5 as header (lines 379–388), causing `IndexOutOfBoundsException` if CSV has fewer than 6 rows.

---

### InfoLogger.java
**Class:** `InfoLogger` — security event logger
| Line | Method |
|------|--------|
| 28 | `public void writelog(String msg)` |
| 84 | `private void close()` |
| 91 | `private void open(String date)` |

SQL injection: `writelog()` parses `msg` by position (lines 51–56: `p1 = msg.indexOf('/')`, etc.) and inserts `uid`, `mid`, `rem` directly into `SEC_LOG_DETAILS` via string concatenation at line 64–66. Also queries `HR_EMP_MST` with `tuid` (line 59) without parameterisation.

---

### LindeConfig.java
**Class:** `LindeConfig` — XML-driven site configuration loader
| Line | Method |
|------|--------|
| 47 | `public LindeConfig()` |
| 52 | `public void readXMLFile()` |
| 139 | `public static String now(String dateFormat)` |

Static fields include: `siteName`, `externalURL`, `firmwareserver`, `firmwareinternerserver`, `customerLinde`, `mail_from`, `LOGOIMG`, `tab_count`, `subscriptionTable`, `reportLogo`, `reportHead`, `logoEmail`, `maxTechinician`, `LIC_TYPES[]`, `DRIV_TYPES[]`.
`readXMLFile()` parses `/home/gmtp/linde_config/settings.xml`. No DTD/XXE protection on `DocumentBuilderFactory` (line 63) — XXE vulnerability if the config file is attacker-controlled.

---

### LogicBean_filter.java
**Class:** `LogicBean_filter` — legacy report data bean
| Line | Method |
|------|--------|
| 70 | `public void clear_variables()` |
| 107 | `private void Fetch_users() throws SQLException` |
| 132 | `private void Fetch_Data() throws SQLException` |
| 180 | `public void init()` |
| 215+ | Getters/setters for all fields |

SQL injection: `Fetch_users()` line 122 interpolates `set_gp_cd` into query. `Fetch_Data()` line 136 interpolates `set_user_cd`, and line 146–150 interpolates `weig_id`, `st_dt`, `end_dt` directly.

---

### LogicBean_filter1.java
**Class:** `LogicBean_filter1` — legacy report data bean (variant)

Same structure and same SQL injection patterns as `LogicBean_filter`. Exact methods mirrored.

---

### mail.java
**Class:** `mail` — email sending utility with Excel attachment generation
| Line | Method |
|------|--------|
| 41 | `public String Ename(String userid) throws SQLException` |
| (further) | `sendMail(...)` and report-sending methods (not shown in excerpt) |

`Ename()` queries `FMS_USR_MST` by `userid` string concatenation. `mail_from` and `sName` are overridden with `LindeConfig` values regardless of DB result (lines 78–79).

---

### Menu_Bean.java
**Class:** `Menu_Bean` — menu/form access rights loader
| Line | Method |
|------|--------|
| 50 | `public void setOption(String opt)` |
| 51 | `public void setemp_nm(String empnm)` |
| 52 | `public void setModule(String mdl)` |
| 55–70 | Getters for `FormId`, `ApplicationPath`, `FormName`, `FormType`, `ModuleName` |
| 72 | `public void fetchform_rights()` |
| (further) | `init()` method |

`fetchform_rights()` line 77 interpolates `set_user_cd` into SQL without parameterisation.

---

### Menu_Bean1.java
**Class:** `Menu_Bean1` — menu/form access rights loader (variant)

Same SQL injection pattern as `Menu_Bean`. `set_user_cd` interpolated into query at line 73.

---

### MigrateMaster.java
**Class:** `MigrateMaster` — supervisor list migration scheduler
| Line | Method |
|------|--------|
| 18 | `public void callMigrateMaster() throws SQLException` |

Performs DELETEs and INSERTs to `FMS_LOC_OVERRIDE` for all active customers. Uses string interpolation for `cust_cd` and `locations.get(i)` throughout.

---

### PasswordExpiryAlert.java
**Class:** `PasswordExpiryAlert` — password expiry email scheduler
| Line | Method |
|------|--------|
| 13 | `public void checkExpiry() throws SQLException` |
| (private) | `isValid(String email)` |

---

### password_life.java
**Class:** `password_life` — login/session tracking (decompiled 2006-era)
| Line | Method |
|------|--------|
| 19 | `public password_life()` |
| 32 | `public void clear_variables()` |
| 46 | `public void setUser(String s)` |
| 50 | `public void setIp(String s)` |
| 55 | `public void setLogindate(String s)` |
| 60 | `public void setLogintime(String s)` |
| 66 | `public void loadDefaultValues() throws SQLException` |
| (further) | `init()` and other methods |

`loadDefaultValues()` line 71: calls `(new EncryptTest()).encrypt(userid)` to produce a hash stored as `s` — but `s` is never subsequently used in the visible excerpt. The query at line 76 uses `userid` directly without parameterisation.

---

### password_policy.java
**Class:** `password_policy` — password policy enforcement (decompiled 2006-era)
| Line | Method |
|------|--------|
| 16 | `public password_policy()` |
| 30 | `public void clear_variables()` |
| 43 | `public void setUser(String s)` |
| 47 | `public void setIp(String s)` |
| 52 | `public void setLogindate(String s)` |
| 57 | `public void setLogintime(String s)` |
| 64 | `public void loadDefaultValues() throws SQLException` |
| (further) | `checkPolicy(String password)` and others |

`loadDefaultValues()` line 69: calls `EncryptTest().encrypt(userid)` — result assigned to `s` but, like `password_life`, immediately unused. Query at line 74 uses raw `sysdate` (Oracle syntax) — will fail on PostgreSQL.

---

### PurgeData.java
**Class:** `PurgeData` — empty placeholder
No methods, no fields. Body is completely empty.

---

### RuntimeConf.java
**Class:** `RuntimeConf` — application-wide static configuration constants
All fields are `public static` (mutable). Key credentials and sensitive values:
| Line | Field | Value |
|------|-------|-------|
| 19 | `user` | `"firmware"` |
| 20 | `pass` | `"ciifirmware"` |
| 29 | `firmwareuser` | `"firmware"` |
| 30 | `firmwarepass` | `"Sdh79HfkLq6"` |
| 54 | `username` | `"TestK"` |
| 55 | `password` | `"testadmin"` |
| 86 | `USERNAME` | `"collintell"` (Clickatell SMS API) |
| 87 | `PASSWORD` | `"fOqDVWYK"` (Clickatell SMS API) |
| 88 | `API_ID` | `"3259470"` (Clickatell SMS API) |
| 129 | `ADMIN_EMAIL` | `"serveradmin@collectiveintelligence.com.au"` |

No methods; the class is a bag of public static mutable fields. `emailurl`, `emailExternalurl`, `externalUrl` all read from `LindeConfig.externalURL` at class initialisation time (lines 43–45). These are runtime-mutable, meaning any code anywhere can silently overwrite all credentials.

---

### SendMessage.java
**Class:** `SendMessage` — Clickatell SMS dispatcher
| Line | Method |
|------|--------|
| 34 | `public void init()` |
| 81 | `private void send_all_sms() throws SQLException, IOException` |
| 112 | `private void send_sms_message(String id, String mobile_no, ...)` |
| 227 | `private String[] readLines(String url) throws IOException` |

`send_sms_message()` at line 174 embeds `RuntimeConf.USERNAME`, `RuntimeConf.PASSWORD`, `RuntimeConf.API_ID` into the HTTP request URL in plaintext. DELETE from `sms_outgoing` at line 132 uses `id` directly interpolated — SQL injection.

---

### SupervisorMasterHelper.java
**Class:** `SupervisorMasterHelper` — supervisor slot management
| Line | Method |
|------|--------|
| 18 | `public boolean deleteSupervisorByUser(String user, String cust_cd, String loc_cd, String dept_cd, String access_user)` |
| (further) | `addSupervisor(...)`, `getSupervisorList(...)` and others (not shown in excerpt) |

All SQL queries use string concatenation with `user`, `loc_cd`, `cust_cd` directly.

---

### call_mail.java
**Class:** `call_mail` — scheduled email report sender
| Line | Method |
|------|--------|
| 40 | `public String getEmail()` |
| 44 | `public void setEmail(String email)` |
| 49 | `public String getDebug()` |
| 53 | `public void setDebug(String debug)` |
| 60 | `public String Ename(String userid)` |
| 69 | `public void call_email_au() throws SQLException` |
| (further) | `call_email()` |

---

### DateUtil.java (continued — additional methods not in initial excerpt)
Further methods include `getStartDate()`, date range calculators, and period helpers — all using string-based date parsing without null-guard on the caller's input.

---

### escapeSingleQuotes.java
**Class:** `escapeSingleQuotes` — SQL escaping utility
| Line | Method |
|------|--------|
| 4 | `public String replaceSingleQuotes(String sInput)` |

Only escapes single quotes by doubling them. Does NOT handle other SQL metacharacters (`\`, `--`, `;`, `/*`, etc.). Null-safe (checks `sInput != null` in loop condition).

---

### send_timezone.java
**Class:** `send_timezone` — DST timezone push scheduler
| Line | Method |
|------|--------|
| 27 | `public void call_send_timezone() throws SQLException` |

Pushes `TZONE=60` or `TZONE=0` message to all active units at UK DST transitions.

---

### send_updatepreop.java
**Class:** `send_updatepreop` — pre-op checklist push scheduler
| Line | Method |
|------|--------|
| 29 | `public void updatepreop() throws SQLException` |

---

### UtilBean.java
**Class:** `UtilBean` — database-backed date/utility bean
| Line | Method |
|------|--------|
| 31 | `public String getGen_dt()` |
| 35 | `public void setGen_dt(String gen_dt)` |
| 43 | `private void find_gen_dt_and_time_gen() throws SQLException` |
| 58 | `public int getDays(int month, int year)` |
| 70 | `public static String getLocalTime(String currentTime, String webUserCD)` |
| 135 | `public void init()` |
| 178 | `public static CustomerBean getCustomerSettingByUser(String userCd)` |
| 235 | `public static CustomerBean getCustomerSetting(String custCd)` |
| 290 | `public static CustLocDeptBean getCustLocDeptBeanByUser(String userCD)` |
| 345–367 | Getters/setters for `gen_tm`, `gen_sdttm`, `gen_fdttm`, `gen_dt_format` |
| 369 | `public void template()` |

SQL injection: `getLocalTime()` line 86 interpolates `webUserCD` into SQL. `getCustomerSettingByUser()` line 196 interpolates `userCd`. `getCustomerSetting()` line 251 interpolates `custCd`. `getCustLocDeptBeanByUser()` line 305 interpolates `userCD`. All four are `public static` methods callable from JSPs.

---

## Test Search Results

Grep for test files referencing `RuntimeConf`, `UtilBean`, `GdprDataDelete`, `CustomUpload`, `EncryptTest`, `DataUtil`, `ImportFiles`:
- **Result: ZERO test files found** (grep returned only `EncryptTest.java` itself — which is a production class, not a test)
- No `*Test*.java` files exist anywhere in the repository other than `EncryptTest.java`
- No JUnit `@Test` annotations exist anywhere in the repository
- `junit-3.8.1.jar` is present in `WEB-INF/lib` but is never imported or exercised

**Test coverage: 0 of 37 files tested. 0 of approximately 120+ methods tested.**

---

## Findings

### A03-1 — CRITICAL — Credential Exposure in Source Code
**File:** `RuntimeConf.java:18-30`
**Severity:** CRITICAL
**Category:** Credential Handling
**Untested method:** All credential fields (no test verifies they are non-default, non-empty, or changed from committed values)
**Risk:** Plaintext passwords committed to version control: `pass="ciifirmware"`, `firmwarepass="Sdh79HfkLq6"`, `username="TestK"`, `password="testadmin"`, Clickatell `PASSWORD="fOqDVWYK"`. All fields are `public static` mutable — any class can overwrite them silently. A test validating credential rotation would have detected these values still being default/test values in production.
**Recommended test:** Write a configuration-validation test that asserts no credential field in `RuntimeConf` matches any of the known committed default/test values, and that no field is null or empty.

---

### A03-2 — CRITICAL — EncryptTest: Weak Algorithm, No Round-Trip Test, Null/Short Input Crashes
**File:** `EncryptTest.java:16` and `EncryptTest.java:97`
**Severity:** CRITICAL
**Category:** Encryption/Decryption Correctness
**Untested method:** `encrypt(String s)` at line 16; `decrypt(String s)` at line 97
**Risk:** The algorithm is trivially reversible (deterministic prefix + position-shift). Empty string input to `encrypt()` returns a 10-character prefix with no actual encrypted content. `decrypt()` on a string shorter than 10 characters throws `StringIndexOutOfBoundsException` at line 100 (`s.substring(10)`). A string of exactly 10 chars decrypts to an empty string silently. Null input to either method causes `NullPointerException`. The class is used directly by `password_life.loadDefaultValues()` and `password_policy.loadDefaultValues()` — crashes in production if a userid is null. No round-trip correctness is validated anywhere.
**Recommended test:**
- `testEncryptDecryptRoundTrip()`: assert `decrypt(encrypt(s).toString()).toString().equals(s)` for passwords of lengths 1, 4, 5, 7, 8, 10, 11, 14, 15+ chars.
- `testEncryptNullInput()`: assert `NullPointerException` (or define graceful null contract).
- `testEncryptEmptyString()`: assert result is the 10-char prefix only.
- `testDecryptTooShort()`: assert exception or defined behaviour on strings < 10 chars.
- `testEncryptWeakness()`: demonstrate two different inputs of the same length bracket produce same prefix — confirming the cipher provides no cryptographic guarantee.

---

### A03-3 — CRITICAL — GdprDataDelete: SQL Injection in Permanent Data Deletion
**File:** `GdprDataDelete.java:67-95`
**Severity:** CRITICAL
**Category:** SQL Injection / Data Integrity / GDPR Compliance
**Untested method:** `call_gdpr_delete_data()` at line 29
**Risk:** `gdpr_data` (line 73: interval string) and `driver_cd.get(i)` (lines 73–95) are interpolated directly into DELETE statements. A malformed `gdpr_data` value (e.g., `"1 years'; DROP TABLE fms_io_data; --"`) would execute arbitrary SQL that permanently destroys data. Nine tables are affected. There is no test confirming only the correct customer's data is deleted, no test confirming inactive-for-30-days logic is correct, and no test confirming the cascade delete order is safe.
**Recommended test:**
- `testDeletesOnlyTargetedCustomer()`: with two customers in a test DB, trigger deletion for one, assert the other's data is untouched.
- `testGdprIntervalBoundary()`: assert records exactly at the boundary (`gdpr_data` years) are deleted; records one day inside are not.
- `testSqlInjectionInGdprData()`: assert that a malicious `gdpr_data` value does not execute injected SQL (requires parameterised rewrite first).
- `testDriverCdSqlInjection()`: same for `driver_cd` column.

---

### A03-4 — CRITICAL — CustomUpload: No File Type Validation, No Size Limit, Path Uses Unsanitised Filename
**File:** `CustomUpload.java:45-299`
**Severity:** CRITICAL
**Category:** File Upload Security
**Untested method:** `doPost(...)` at line 45; `getFileName(Part)` at line 307; `read(String)` at line 322
**Risk:** The filename is taken directly from the multipart Content-Disposition header (line 315) with no extension check, no type whitelist, and no sanitisation of path separators. A filename like `../../WEB-INF/web.xml` would write to an arbitrary path under the server root. A `null` Part or missing filename header causes NPE at line 311 (`part.getHeader("content-disposition").split(";")` — if `getHeader()` returns null, this throws NPE before the null check at line 62). The firmware action (line 219) embeds a hardcoded password (`Sdh79HfkLq6`) in the FTP command string that is inserted into the database.
**Recommended test:**
- `testRejectNonCsvExtension()`: upload a `.php`, `.jsp`, or `.exe` file and assert rejection.
- `testPathTraversalFilename()`: upload with filename `../../evil.txt` and assert the file is not written outside the upload directory.
- `testNullPartHandled()`: assert graceful response when no file part is provided.
- `testLargeFileHandled()`: assert behaviour when upload exceeds expected size.

---

### A03-5 — CRITICAL — DataUtil: File Upload Methods Have No Path Traversal Prevention
**File:** `DataUtil.java:918-958`
**Severity:** CRITICAL
**Category:** Path Traversal / File Upload Security
**Untested method:** `uploadLicenceFile(HttpServletRequest, Part, String filename)` at line 918; `uploadDocumentFile(HttpServletRequest, Part, String cust_loc, String veh_cd)` at line 936
**Risk:** `uploadLicenceFile()` writes to `/home/gmtp/fms_files/licence/<filename>` where `filename` is caller-supplied with no sanitisation. `uploadDocumentFile()` constructs the path as `/home/gmtp/fms_files/CFTS/<cust_loc>/` then uses `fName` (from multipart header, with spaces replaced by underscores but no traversal check). A `cust_loc` value of `../../../etc` would write to `/etc/`. `escapeSpecialCharacter()` at line 600 (used in `FleetCheckFTP`) strips `[-+.^:, ]` but explicitly does NOT strip `/` characters, leaving `../` traversal possible.
**Recommended test:**
- `testUploadLicencePathTraversal()`: pass filename `../../../etc/passwd` and assert write is confined to the base directory.
- `testUploadDocumentCustLocTraversal()`: pass `cust_loc = "../../WEB-INF"` and assert containment.
- `testEscapeSpecialCharacterDoesNotBlockTraversal()`: assert `escapeSpecialCharacter("../../../etc")` still contains `../`.

---

### A03-6 — CRITICAL — ImportFiles: No File Type Check, `driversUK` IndexOutOfBounds Risk, CSV Injection
**File:** `ImportFiles.java:49-end`
**Severity:** CRITICAL
**Category:** File Upload Security / Data Import Integrity
**Untested method:** `doPost(...)` at line 49 for all `src` types
**Risk:** Uploaded file is written to disk with original filename before any validation occurs (line 85). `driversUK` handler at line 379 calls `dataLst.get(5).size()` — if the uploaded CSV has fewer than 6 rows, this throws `IndexOutOfBoundsException`. No file extension restriction. CSV content is not sanitised against CSV injection (formulae beginning with `=`, `+`, `-`, `@` which execute in spreadsheet applications).
**Recommended test:**
- `testDriversUKWithInsufficientRows()`: upload a CSV with 3 rows and assert a graceful error response, not 500.
- `testUploadNonCsvFile()`: upload a `.exe` file; assert rejection.
- `testCsvInjectionBlocked()`: upload a CSV where a cell starts with `=SUM(...)` and assert the value is not passed through unchecked.
- `testDriversImportRollbackOnPartialFailure()`: import a CSV where row 3 of 5 is invalid and assert no rows are persisted.

---

### A03-7 — HIGH — GdprDataDelete: No Test Confirming Correct Customer Scoping
**File:** `GdprDataDelete.java:59-101`
**Severity:** HIGH
**Category:** GDPR Compliance / Data Correctness
**Untested method:** `call_gdpr_delete_data()` — customer-scoping logic
**Risk:** The method queries all customers with `gdpr_data != 0`, then for each customer deletes data for inactive drivers older than 30 days. If the `CUST_CD` join condition is incorrect, or if `inactive_date` logic has an off-by-one, data belonging to the wrong customer could be deleted. There is no test asserting that after the job runs, Customer A's records are absent and Customer B's records are intact.
**Recommended test:** Integration test with two customers and overlapping driver sets — assert isolation post-deletion.

---

### A03-8 — HIGH — UtilBean: SQL Injection in Four Public Static Methods
**File:** `UtilBean.java:86,196,251,305`
**Severity:** HIGH
**Category:** SQL Injection
**Untested method:** `getLocalTime(String currentTime, String webUserCD)` at line 70; `getCustomerSettingByUser(String userCd)` at line 178; `getCustomerSetting(String custCd)` at line 235; `getCustLocDeptBeanByUser(String userCD)` at line 290
**Risk:** All four methods concatenate their `String` parameter directly into SQL queries without parameterisation. These are `public static` methods called from JSP pages where the parameter may originate from session or request attributes. SQL injection via `webUserCD`, `userCd`, `custCd`, or `userCD` would allow extraction of `FMS_USR_MST` credentials, `FMS_CUST_MST` settings, or arbitrary table data.
**Recommended test:**
- `testGetLocalTimeSqlInjection()`: pass `"1 OR 1=1"` as `webUserCD` and assert no unexpected data is returned.
- Same pattern for the other three methods.
- `testGetCustomerSettingByUserNullInput()`: pass null and assert graceful handling (currently would throw NPE in SQL string concatenation).

---

### A03-9 — HIGH — InfoLogger: SQL Injection in Security Log Writer
**File:** `InfoLogger.java:59-66`
**Severity:** HIGH
**Category:** SQL Injection
**Untested method:** `writelog(String msg)` at line 28
**Risk:** The `writelog()` method parses the `msg` parameter by character position to extract `uid`, `mid`, and `rem` fields (lines 51–56), then interpolates all three directly into an INSERT into `SEC_LOG_DETAILS` (line 64). An attacker controlling the log message format could inject SQL into the security audit table. The prior query on `HR_EMP_MST` (line 59) also concatenates `tuid` directly.
**Recommended test:**
- `testWritelogSqlInjection()`: pass a message containing SQL injection payload in the uid position and assert no unexpected execution.
- `testWritelogMalformedMessage()`: pass a message without `/` delimiter and assert no crash.

---

### A03-10 — HIGH — FleetCheckFTP: SQL Injection via gmtp_id
**File:** `FleetCheckFTP.java:229-244`
**Severity:** HIGH
**Category:** SQL Injection / FTP Credential Exposure
**Untested method:** `upload_quest_ftp()` at line 24
**Risk:** `gmtp_id` is retrieved from `ftp_outgoing.gmtp_id` and then directly concatenated into INSERT and SELECT statements (lines 230–244). If the `ftp_outgoing` table is writable by an attacker, injected SQL would execute with DB user privileges. The FTP command string (line 229) embeds `RuntimeConf.firmwarepass = "Sdh79HfkLq6"` in plaintext in the `outgoing` message table. Class comment itself says this method references a table that does not exist in production.
**Recommended test:**
- `testUploadQuestFtpWithInjectedGmtpId()`: verify SQL injection in `gmtp_id` is blocked.
- `testFtpPasswordNotStoredInPlaintext()`: assert outgoing message does not contain the literal firmware password.

---

### A03-11 — HIGH — SendMessage: SMS API Credentials Exposed in URL
**File:** `SendMessage.java:174-180`
**Severity:** HIGH
**Category:** Credential Exposure / External API Security
**Untested method:** `send_sms_message(...)` at line 112; `init()` at line 34
**Risk:** Clickatell API authentication at line 174 passes `RuntimeConf.USERNAME`, `RuntimeConf.PASSWORD`, and `RuntimeConf.API_ID` as plaintext HTTP query parameters. These are logged by the Clickatell server and may appear in access logs. The DELETE SQL at line 132 interpolates `id` directly. If `send_all_sms()` encounters an exception mid-loop, already-sent messages may be re-sent (no transactional boundary).
**Recommended test:**
- `testSmsNotSentWithNullUnitName()`: verify that when `unit_name` is null, no SMS is dispatched and the record is deleted.
- `testSmsDeleteSqlInjection()`: verify `id` cannot be used for SQL injection.

---

### A03-12 — HIGH — LindeConfig: No XXE Protection, XML Parsing from Filesystem
**File:** `LindeConfig.java:52-136`
**Severity:** HIGH
**Category:** XML Injection / XXE
**Untested method:** `readXMLFile()` at line 52
**Risk:** `DocumentBuilderFactory.newInstance()` at line 63 uses default settings which allow external entity expansion (XXE). If `/home/gmtp/linde_config/settings.xml` is writable by an attacker, they can inject `<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>` to read arbitrary server files. No test verifies that required configuration keys exist, have non-empty values, or that the fallback to `setting_au.xml` produces a valid configuration.
**Recommended test:**
- `testReadXMLFileXxePrevented()`: supply an XML file with an XXE payload and assert no file content is exposed.
- `testReadXMLFileMissingKey()`: supply XML missing `external_url` and assert the application does not silently use a default/empty value.

---

### A03-13 — HIGH — DataUtil: `escapeSpecialCharacter()` Does Not Prevent Path Traversal
**File:** `DataUtil.java:600-604`
**Severity:** HIGH
**Category:** Path Traversal
**Untested method:** `escapeSpecialCharacter(String str)` at line 600
**Risk:** Used in `FleetCheckFTP.upload_quest_ftp()` to sanitise `cust_name`, `loc_name`, `dept_name` before constructing filesystem paths (e.g., line 115–116 in FleetCheckFTP). The regex `[\\-\\+\\.\\s+\\^:, ]` does NOT strip `/` or `..`. An entity name like `../../../etc` would survive `escapeSpecialCharacter()` and produce a traversal path under `RuntimeConf.firmwarefolder`.
**Recommended test:**
- `testEscapeSpecialCharacterStripsSlashes()`: assert `escapeSpecialCharacter("a/../b")` does not contain `/`.
- `testEscapeSpecialCharacterNullInput()`: assert null returns null or empty without NPE.

---

### A03-14 — HIGH — DateUtil: `stringToSQLDate()` Has Broken Format Detection Logic
**File:** `DateUtil.java:45-71`
**Severity:** HIGH
**Category:** Data Integrity / Date Parsing
**Untested method:** `stringToSQLDate(String str_date)` at line 45
**Risk:** Lines 53–58: if month > 12, format is `dd/MM/yyyy` (correct). If day > 12 AND month <= 12, format switches to `MM/dd/yyyy` — then if month is also <= 12, the `dd/MM/yyyy` branch at line 56 overrides back to `dd/MM/yyyy`. The logic is effectively: always `dd/MM/yyyy` unless day <= 12 AND month <= 12 (ambiguous case), in which case `MM/dd/yyyy` is used. This means dates like `10/06/2024` (10th June) would be parsed as 6th October. If the returned SQL date is used in a `BETWEEN` filter in a report, wrong dates silently produce wrong results.
**Recommended test:**
- `testStringToSQLDateUnambiguous()`: `"15/06/2024"` must parse to 15 June, not 6 October.
- `testStringToSQLDateAmbiguous()`: `"01/02/2024"` — document and assert the intended interpretation.
- `testStringToSQLDateNullInput()`: assert null does not cause NPE (currently returns null at line 69 via catch).

---

### A03-15 — HIGH — Dt_Checker: Incorrect Leap Year Algorithm
**File:** `Dt_Checker.java:141-150`
**Severity:** HIGH
**Category:** Data Integrity / Date Logic
**Untested method:** `isleap(int y)` at line 141; all methods that call it (`last()`, `days_Betn()`, `daysIn()`)
**Risk:** The leap year rule at line 143 returns `true` for `y % 1000 == 0` (e.g., 3000) — but the actual Gregorian rule is that century years divisible by 400 are leap years, and 1000 is not a multiple of 400. Line 145 then returns `false` for `y % 400 == 0` — this inverts the correct rule, meaning year 2000, 2400 etc. are treated as NOT leap years when they are. `days_Betn()` and `daysIn()` which use `isleap()` will return wrong counts around 28 Feb in divisible-by-400 years, causing date-range errors in reports.
**Recommended test:**
- `testIsLeap2000()`: assert `isleap(2000)` returns `true` (year 2000 is a leap year).
- `testIsLeap1900()`: assert `isleap(1900)` returns `false`.
- `testIsLeap3000()`: assert `isleap(3000)` returns `false`.
- `testDaysBetnAcrossLeapDay()`: compare `days_Betn("28/02/2000", "01/03/2000")` and assert it equals 2.

---

### A03-16 — HIGH — password_life / password_policy: EncryptTest Called but Result Discarded
**File:** `password_life.java:71`; `password_policy.java:69`
**Severity:** HIGH
**Category:** Authentication Logic / Dead Code
**Untested method:** `loadDefaultValues()` in both classes
**Risk:** Both classes call `(new EncryptTest()).encrypt(userid)` and assign the result to `s`, but `s` is never used in the visible code. This implies either: (a) an original security check was removed and a raw `userid` is now compared against a cipher-encrypted value in the database (authentication bypass), or (b) the encrypt call is vestigial dead code and the query at line 76 uses the raw `userid` (SQL injection risk since `userid` is not sanitised). No test exists to confirm authentication logic is correct or that removing the encrypt usage did not create a bypass.
**Recommended test:**
- `testLoadDefaultValuesUsesEncryptedPassword()`: assert that the SQL query being issued uses the encrypted form of the userid, not the raw form.
- `testEncryptResultIsNotDiscarded()`: static analysis assertion that `s` is referenced post-assignment.

---

### A03-17 — HIGH — ExcelUtil: Reflection Class Loading with Unsanitised Input
**File:** `ExcelUtil.java:37-39`
**Severity:** HIGH
**Category:** Injection / Reflection
**Untested method:** `getExcel(String rpt_name, String params, HttpServletResponse response)` at line 34; `getEmail(String rpt_name, String params, boolean isConf)` at line 61; `getPrintBody(String rpt_name, String params)` at line 84
**Risk:** All three methods call `Class.forName("com.torrent.surat.fms6.excel.reports." + rpt_name)` without validating `rpt_name`. If `rpt_name` is user-controlled (e.g., via a report-download JSP parameter), an attacker could load unintended classes. `getExportDir()` constructs a path with `../../../../../../../../excelrpt/` — if the JAR location changes, this traversal may resolve outside the intended directory.
**Recommended test:**
- `testGetExcelRejectsUnknownReportName()`: pass an invalid `rpt_name` and assert a controlled exception, not class-loading of arbitrary classes.
- `testGetExportDirResolvesInsideWebRoot()`: assert the resolved export directory is within the expected server path.

---

### A03-18 — MEDIUM — BeanComparator: Reflection-Based Comparison with No Method Validation Beyond Name
**File:** `BeanComparator.java:33-172`
**Severity:** MEDIUM
**Category:** Robustness / Reflection
**Untested method:** `compare(Object object1, Object object2)` at line 106; all constructors
**Risk:** Constructor validates method exists but does not restrict which methods can be invoked via comparison. If `methodName` is caller-supplied (e.g., from a sort parameter), any public getter-like method could be invoked, including those with side effects. `compare()` catches `Exception` broadly at line 116 and re-throws as `RuntimeException`, which could mask real failures in sorted collections.
**Recommended test:**
- `testCompareAscendingStrings()`: assert correct ordering.
- `testCompareNullValues()`: assert nulls are sorted last by default.
- `testInvalidMethodNameThrowsIllegalArgument()`: pass a non-existent method name and assert `IllegalArgumentException`.

---

### A03-19 — MEDIUM — DataUtil: `removeDuplicateCds()` Crashes on Input `"0,0"`
**File:** `DataUtil.java:776-798`
**Severity:** MEDIUM
**Category:** Robustness / Edge Cases
**Untested method:** `removeDuplicateCds(String s)` at line 776
**Risk:** The method has a special case for `"0,0"` (line 778) but would crash on `""` (empty string) — `s.split(",")` on empty string returns a one-element array containing `""`, then `newS.substring(0, newS.length() - 1)` at line 791 would throw `StringIndexOutOfBoundsException` if `newS` is empty after the loop. Also `s.trim().equalsIgnoreCase("0,0")` comparison is brittle — `"0, 0"` (with space) would not match.
**Recommended test:**
- `testRemoveDuplicateCdsEmptyString()`: assert empty input returns empty without exception.
- `testRemoveDuplicateCdsSingleValue()`: assert `"5"` returns `"5"`.
- `testRemoveDuplicateCdsDuplicates()`: assert `"3,1,3,2"` returns `"1,2,3"`.

---

### A03-20 — MEDIUM — DataUtil: `calculateTime()` Returns -1 on Exception, Silently
**File:** `DataUtil.java:862-899`
**Severity:** MEDIUM
**Category:** Robustness / Error Handling
**Untested method:** `calculateTime(String type, String st, String end)` at line 862
**Risk:** On parse exception or invalid `type` string, returns `-1` (initialised at line 864). Callers in `CftsAlert.checkDueDate()` (line 75) use the return value in comparisons `if(days <= 0 ...)` — a return of -1 (error case) satisfies `days <= 0` and would trigger the overdue alert branch for any vehicle whose date fails to parse. This could cause spurious "overdue" emails to all customers.
**Recommended test:**
- `testCalculateTimeDaysBetween()`: known dates, assert correct day count.
- `testCalculateTimeInvalidType()`: pass `type="week"` and assert defined behaviour (not -1 silently triggering overdue logic).
- `testCalculateTimeNullDates()`: assert graceful handling.

---

### A03-21 — MEDIUM — UtilBean: `getDays()` Does Not Validate Month Range
**File:** `UtilBean.java:58-68`
**Severity:** MEDIUM
**Category:** Robustness
**Untested method:** `getDays(int month, int year)` at line 58
**Risk:** `noofdays[month - 1]` — if `month` is 0, this accesses index -1 (throws `ArrayIndexOutOfBoundsException`). If `month` is > 12, array index out of bounds. No guard on input range.
**Recommended test:**
- `testGetDaysValidMonths()`: assert February returns 28 or 29, others return correct days.
- `testGetDaysInvalidMonth()`: assert `getDays(0, 2024)` throws a defined exception, not `ArrayIndexOutOfBoundsException`.
- `testGetDaysLeapYear()`: assert February 2024 returns 29, February 2023 returns 28.

---

### A03-22 — MEDIUM — LindeConfig: Static Fields Are Public Mutable — Runtime Override Risk
**File:** `LindeConfig.java:20-45`
**Severity:** MEDIUM
**Category:** Configuration Integrity
**Untested method:** `readXMLFile()` post-parse state
**Risk:** All configuration fields (`siteName`, `externalURL`, `firmwareserver`, etc.) are `public static` (not `final`). Any class can overwrite them at runtime. `RuntimeConf.mail_from` is mutated inside `readXMLFile()` at line 97. No test verifies that after configuration load, the fields contain the expected production values for each deployment environment.
**Recommended test:**
- `testReadXMLFileUKSite()`: supply `settings.xml` with UK config and assert all fields match expected values.
- `testReadXMLFileAUSite()`: supply AU config and assert `siteCss` becomes `styles_au.css`.
- `testFieldsNotMutatedByUnrelatedCode()`: assert config fields are immutable after initial load.

---

### A03-23 — MEDIUM — escapeSingleQuotes: Incomplete SQL Escaping
**File:** `escapeSingleQuotes.java:4-17`
**Severity:** MEDIUM
**Category:** SQL Injection Defence
**Untested method:** `replaceSingleQuotes(String sInput)` at line 4
**Risk:** Only doubles single quotes. Does not escape backslash (PostgreSQL `\\` in string literals), comment sequences (`--`, `/*`), or semicolons. Callers that rely on this for full SQL injection protection are still vulnerable. No test verifies behaviour on empty string, string with only quotes, or Unicode quote characters (U+2019 RIGHT SINGLE QUOTATION MARK).
**Recommended test:**
- `testReplaceSingleQuotesDoubles()`: `"it's"` → `"it''s"`.
- `testReplaceSingleQuotesNullSafe()`: null input returns empty string.
- `testReplaceSingleQuotesNoOtherEscaping()`: assert `--` or `\\` are NOT escaped, documenting the limitation.

---

### A03-24 — MEDIUM — SupervisorMasterHelper: SQL Injection in deleteSupervisorByUser
**File:** `SupervisorMasterHelper.java:18`
**Severity:** MEDIUM
**Category:** SQL Injection
**Untested method:** `deleteSupervisorByUser(String user, String cust_cd, String loc_cd, String dept_cd, String access_user)` at line 18
**Risk:** `user`, `loc_cd`, `cust_cd` are concatenated directly into UPDATE, DELETE, and SELECT statements (lines 39, 50, 54). These values are typically supervisor user codes and location codes from session state, but if the session is compromised, injected SQL would delete arbitrary supervisor slot data.
**Recommended test:**
- `testDeleteSupervisorWithInjectedUser()`: pass `"' OR '1'='1"` as user and assert no unintended rows are modified.

---

### A03-25 — LOW — CustomComparator: `compare()` Has TODO Stub Comment
**File:** `CustomComparator.java:10-13`
**Severity:** LOW
**Category:** Code Quality
**Untested method:** `compare(DriverLeagueBean o1, DriverLeagueBean o2)` at line 10
**Risk:** The `// TODO Auto-generated method stub` comment was never removed. The implementation is a single line (descending name sort). No test verifies the sort direction or null-safety.
**Recommended test:** `testCompareReturnsDescendingOrder()`: two beans, assert ordering is correct.

---

### A03-26 — LOW — PurgeData: Empty Class — Intent Unknown
**File:** `PurgeData.java:3-5`
**Severity:** LOW
**Category:** Dead Code
**Untested method:** (none — class is completely empty)
**Risk:** Empty class suggests either planned functionality that was never implemented, or that the real purge logic lives elsewhere. If data purge was intended to be here and was accidentally omitted, data retention/compliance obligations may be unmet.
**Recommended test:** Document intent; if placeholder, remove or add a comment confirming it is intentionally empty.

---

### A03-27 — LOW — DataUtil: `generateRadomName()` Typo and Weak Uniqueness
**File:** `DataUtil.java:240-248`
**Severity:** LOW
**Category:** Code Quality
**Untested method:** `generateRadomName()` at line 240
**Risk:** Typo in method name (`Radom` instead of `Random`). The name combines a timestamp and a UUID — adequate for most purposes, but no test verifies the format or uniqueness under rapid concurrent calls (UUID v4 is statistically unique but not guaranteed).
**Recommended test:** `testGenerateRandomNameFormat()`: assert result matches expected `yyyyMMddHHmmss-<uuid>` pattern.

---

### A03-28 — LOW — DBUtil: No Connection Pool Exhaustion Guard
**File:** `DBUtil.java:20-57`
**Severity:** LOW
**Category:** Resource Management
**Untested method:** `getConnection()` at line 20; `getMySqlConnection()` at line 35; `closeConnection()` at line 51
**Risk:** `getConnection()` throws a generic `Exception` — callers must handle this correctly. No test verifies that `closeConnection(null)` is safe (it is — null check at line 53 — but uncovered). No test verifies behaviour if the JNDI datasource is unavailable.
**Recommended test:** `testCloseNullConnectionIsSafe()`: assert `closeConnection(null)` does not throw.

---

## Summary

| File | Approx. Public/Protected Methods | Tested | Untested |
|------|----------------------------------|--------|----------|
| BeanComparator.java | 7 | 0 | 7 |
| CftsAlert.java | 1 | 0 | 1 |
| CustomComparator.java | 1 | 0 | 1 |
| CustomUpload.java | 3 public, 7 private | 0 | 10 |
| DataUtil.java | ~55 | 0 | 55 |
| DateUtil.java | ~10 | 0 | 10 |
| DBUtil.java | 3 | 0 | 3 |
| DriverExpiryAlert.java | 1 | 0 | 1 |
| DriverMedicalAlert.java | 1 | 0 | 1 |
| Dt_Checker.java | 9 | 0 | 9 |
| EncryptTest.java | 2 | 0 | 2 |
| ExcelUtil.java | 6 | 0 | 6 |
| escapeSingleQuotes.java | 1 | 0 | 1 |
| fix_department.java | 1 | 0 | 1 |
| FleetCheckFTP.java | 1 | 0 | 1 |
| GdprDataDelete.java | 1 | 0 | 1 |
| GetHtml.java | 1 | 0 | 1 |
| ImportFiles.java | 1 public, 9 private | 0 | 10 |
| InfoLogger.java | 1 public, 2 private | 0 | 3 |
| LindeConfig.java | 2 | 0 | 2 |
| LogicBean_filter.java | ~20 (getters/setters + init) | 0 | 20 |
| LogicBean_filter1.java | ~20 | 0 | 20 |
| mail.java | 2+ | 0 | 2+ |
| Menu_Bean.java | ~10 | 0 | 10 |
| Menu_Bean1.java | ~10 | 0 | 10 |
| MigrateMaster.java | 1 | 0 | 1 |
| PasswordExpiryAlert.java | 1 | 0 | 1 |
| password_life.java | ~6 | 0 | 6 |
| password_policy.java | ~6 | 0 | 6 |
| PurgeData.java | 0 | 0 | 0 |
| RuntimeConf.java | 0 (all fields) | 0 | N/A |
| SendMessage.java | 1 public, 3 private | 0 | 4 |
| send_timezone.java | 1 | 0 | 1 |
| send_updatepreop.java | 1 | 0 | 1 |
| SupervisorMasterHelper.java | 3+ | 0 | 3+ |
| call_mail.java | 4+ | 0 | 4+ |
| UtilBean.java | ~10 | 0 | 10 |
| **TOTAL** | **~230+** | **0** | **~230+** |

**Test coverage: 0% across all 37 files and all methods.**

---

## Recommended Test Strategy (Ordered by Risk)

1. **[CRITICAL] EncryptTest — Round-trip, null, short-input, edge-case tests**
   Write unit tests immediately. The class is used in authentication (`password_life`, `password_policy`). A crash in `decrypt()` on short input or null would produce a login-blocking production exception. Establish a round-trip invariant before any other work.

2. **[CRITICAL] RuntimeConf — Credential rotation validation test**
   Add a configuration-validation test that fails CI if any known default/test credential (`"testadmin"`, `"ciifirmware"`, `"Sdh79HfkLq6"`, `"fOqDVWYK"`) appears in the live `RuntimeConf` fields. This catches accidental credential commits.

3. **[CRITICAL] GdprDataDelete — GDPR deletion isolation and SQL injection tests**
   The regulatory risk of deleting the wrong customer's data is severe. Write integration tests against an in-memory DB fixture with two customers, verify isolation, and enforce parameterised queries before this code is run in production again.

4. **[CRITICAL] CustomUpload — File type validation and path traversal tests**
   Add a file-extension whitelist (e.g., `.csv` only), sanitise the filename, and write tests covering `.exe`, `.jsp`, `../` traversal attempts, and the null-part NPE path.

5. **[CRITICAL] DataUtil.uploadLicenceFile / uploadDocumentFile — Path traversal tests**
   Add `canonicalPath()` containment checks and test them. The `cust_loc` path segment must be validated to contain only alphanumeric characters before constructing the target directory.

6. **[CRITICAL] ImportFiles — driversUK IndexOutOfBounds and CSV injection tests**
   Guard `dataLst.get(5)` with a size check. Test all `src` variants with minimal-row CSVs.

7. **[HIGH] UtilBean — SQL injection tests for all four static methods**
   All four methods should be refactored to use `PreparedStatement`. Write injection-resistance tests first to document the current vulnerable state, then fix.

8. **[HIGH] GdprDataDelete — Boundary and interval correctness tests**
   Test the 30-day inactivity threshold with dates at day 29, 30, and 31 to verify the interval condition.

9. **[HIGH] LindeConfig — XXE protection and required-field validation tests**
   Disable external entity processing on `DocumentBuilderFactory` and test with an XXE-payload XML. Add assertions that all required config keys are present and non-empty after load.

10. **[HIGH] DateUtil.stringToSQLDate — Format detection logic test**
    Fix the broken `MM/dd/yyyy` detection and write date-parsing tests for ambiguous (day and month both <= 12) and unambiguous cases.

11. **[HIGH] Dt_Checker.isleap — Leap year correctness tests**
    Fix the inverted `y%400 == 0` / `y%1000 == 0` logic and verify years 1900, 2000, 2100, 2400, 3000.

12. **[HIGH] password_life / password_policy — Authentication logic verification**
    Verify whether the discarded `EncryptTest.encrypt()` result represents an authentication bypass or dead code, and write tests that confirm login proceeds correctly only for the correct password.

13. **[HIGH] InfoLogger / FleetCheckFTP / SendMessage — SQL injection in secondary paths**
    All three use string-concatenated SQL. Parameterise and add injection-resistance tests.

14. **[MEDIUM] escapeSingleQuotes — Document limitations and add boundary tests**
    Test that it handles null, empty, quotes-only input. Add a comment warning that it does not provide complete SQL injection protection.

15. **[MEDIUM] DataUtil.calculateTime — Error return value test**
    Verify that a -1 return does not silently trigger overdue alerts in `CftsAlert`. Consider throwing instead of returning -1.

16. **[MEDIUM] BeanComparator / CustomComparator — Sort correctness tests**
    Test ascending, descending, null values first/last, and empty-string handling.

17. **[LOW] DataUtil.removeDuplicateCds — Edge case tests (empty, single, duplicates)**

18. **[LOW] DBUtil — Null-connection safety test**

19. **[LOW] PurgeData — Confirm intent and either implement or remove**
