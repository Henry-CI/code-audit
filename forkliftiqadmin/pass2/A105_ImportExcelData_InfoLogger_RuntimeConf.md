# Pass 2 – Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A105
**Date:** 2026-02-26
**Source Files Audited:**
1. `src/main/java/com/util/ImportExcelData.java`
2. `src/main/java/com/util/InfoLogger.java`
3. `src/main/java/com/util/RuntimeConf.java`

**Test Directory:** `src/test/java/`

---

## Test Directory Inventory

The test directory contains exactly four test files:

| File | Package |
|------|---------|
| `com/calibration/UnitCalibrationImpactFilterTest.java` | com.calibration |
| `com/calibration/UnitCalibrationTest.java` | com.calibration |
| `com/calibration/UnitCalibratorTest.java` | com.calibration |
| `com/util/ImpactUtilTest.java` | com.util |

Grep result for `ImportExcelData` in test directory: **No matches found.**
Grep result for `InfoLogger` in test directory: **No matches found.**
Grep result for `RuntimeConf` in test directory: **No matches found.**

---

## File 1: ImportExcelData.java

### Reading Evidence

**Class name:** `ImportExcelData`
**Package:** `com.util`
**File:** `src/main/java/com/util/ImportExcelData.java`

**Fields:**

| Field | Line | Type | Access |
|-------|------|------|--------|
| `savePath` | 29 | `String` | `private` |

**Methods:**

| Method | Line | Signature |
|--------|------|-----------|
| `upload` | 32 | `public boolean upload(FormFile formFile) throws ServletException, IOException` |
| `read` | 47 | `public List<ArrayList<String>> read(String fileName) throws IOException` |
| `getSavePath` | 75 | `public String getSavePath()` |
| `setSavePath` | 79 | `public void setSavePath(String savePath)` |
| `checkFileExits` | 83 | `public boolean checkFileExits()` |

**Imports of note:**
- `org.apache.poi.hssf.usermodel.HSSFWorkbook` (imported, unused in visible code)
- `org.apache.poi.xssf.usermodel.XSSFWorkbook` (imported, unused in visible code)
- `org.apache.poi.ss.usermodel.Cell`, `Row`, `Sheet`, `Workbook` (imported, unused in visible code)
- `javax.servlet.ServletException`, `java.io.*`
- `org.apache.struts.upload.FormFile`

### Coverage Findings

**A105-1 | Severity: CRITICAL | No test class exists for ImportExcelData**
There is no test file for `ImportExcelData` anywhere in the test directory. Zero methods are tested. All five methods (`upload`, `read`, `getSavePath`, `setSavePath`, `checkFileExits`) have 0% test coverage.

**A105-2 | Severity: HIGH | `upload()` happy-path not tested**
The `upload(FormFile formFile)` method (line 32) writes raw bytes from a `FormFile` to `savePath` using `FileOutputStream`. There is no test verifying that a valid `FormFile` results in the expected bytes being written to disk and that the method returns `true`.

**A105-3 | Severity: HIGH | `upload()` exception path silently swallowed — not tested**
Lines 37–39: exceptions from `FileOutputStream` construction or `write()` are caught, `e.printStackTrace()` is called, and execution continues. The method then attempts `outputStream.close()` on a potentially null stream (guarded at line 40) and returns `true` unconditionally even when the write failed. No test verifies this silent-failure behaviour or that callers cannot detect a write error.

**A105-4 | Severity: HIGH | `upload()` always returns `true` — no test for failure semantics**
The return value is hardcoded to `true` (line 44) regardless of whether the write succeeded or an exception was caught. No test documents or validates this misleading contract.

**A105-5 | Severity: HIGH | `upload()` NullPointerException risk not tested**
If `formFile.getFileData()` returns `null`, line 36 passes `null` to `outputStream.write(byte[])`, which will throw a `NullPointerException`. That NPE will be swallowed by the catch block and `true` returned. No test covers this path.

**A105-6 | Severity: HIGH | `upload()` called with `savePath` empty string not tested**
If `savePath` is `""` (its default value, line 29), `new File("")` is valid but `new FileOutputStream(new File(""))` throws `FileNotFoundException` on most JVMs. The exception is swallowed. No test exercises the default/empty `savePath` state.

**A105-7 | Severity: HIGH | `read()` happy-path not tested**
The `read(String fileName)` method (line 47) reads a CSV-style file and builds a `List<ArrayList<String>>`. No test verifies that it correctly tokenises rows and columns for a normal well-formed file.

**A105-8 | Severity: HIGH | `read()` file-not-found path not tested**
If `fileName` does not exist, `new FileReader(file)` at line 52 throws `FileNotFoundException`. This propagates to the caller. No test verifies the exception type or message.

**A105-9 | Severity: HIGH | `read()` BufferedReader not closed in any path — not tested**
`bufRdr` (line 52) is never closed: there is no `finally` block, no try-with-resources, and no `bufRdr.close()` call. The resource leak is never detected by a test. Under concurrent or repeated calls this will exhaust file descriptors.

**A105-10 | Severity: MEDIUM | `read()` empty file not tested**
If the file exists but contains zero bytes, the while loop is never entered and an empty list is returned. No test confirms this edge case.

**A105-11 | Severity: MEDIUM | `read()` lines with no commas not tested**
`StringTokenizer` with delimiter `","` on a line containing no commas produces a single token. No test verifies that a row with no delimiter is handled correctly (single-element `ArrayList`).

**A105-12 | Severity: MEDIUM | `read()` fields with empty tokens not tested**
`StringTokenizer` skips consecutive delimiters (e.g. `a,,b` yields two tokens, not three). No test verifies whether this is the intended behaviour or a defect.

**A105-13 | Severity: MEDIUM | `read()` unused `row` and `col` counters not tested**
Local variables `row` (line 54) and `col` (line 55) are incremented but never read or returned. No test documents that they are dead code or alerts to the possibility they were intended for validation logic.

**A105-14 | Severity: MEDIUM | `checkFileExits()` — method name typo, no test**
`checkFileExits()` (line 83) is a misspelling of `checkFileExists()`. No test covers either the `true` (file present) or `false` (file absent) return paths, and no test documents the misspelled public API name.

**A105-15 | Severity: MEDIUM | `checkFileExits()` uses `getSavePath()` implicitly — empty path not tested**
When `savePath` is `""` (default), `new File("")` refers to the current working directory. `f.exists()` will return `true` for the JVM's working directory. No test validates behaviour under the default empty-path state.

**A105-16 | Severity: LOW | Unused Apache POI imports — no test detects dead code**
`HSSFWorkbook`, `XSSFWorkbook`, `Cell`, `Row`, `Sheet`, `Workbook` are imported but never used in the class body. This suggests Excel-format reading logic (XLSX/XLS) was planned or removed. No test documents or guards the intended functionality.

**A105-17 | Severity: LOW | `getSavePath()` / `setSavePath()` accessor pair not tested**
Trivial accessors but they are the only way to set the working path. No test confirms the round-trip `setSavePath("x"); assertEquals("x", getSavePath())`.

---

## File 2: InfoLogger.java

### Reading Evidence

**Class name:** `InfoLogger`
**Package:** `com.util`
**File:** `src/main/java/com/util/InfoLogger.java`

**Fields:** None (no instance or class-level fields declared).

**Methods:**

| Method | Line | Signature |
|--------|------|-----------|
| `static initializer` | 15 | `static { PropertyConfigurator.configure(...) }` |
| `getFileURL` | 26 | `public URL getFileURL(final String s)` |
| `getLogger` | 35 | `public static Logger getLogger(final String c)` |
| `logException` | 44 | `public static void logException(Logger log, final Exception e)` |

**Note:** The static initializer at line 15 runs `PropertyConfigurator.configure(...)` using `getFileURL(...)` called on a freshly constructed `new InfoLogger()`. Any exception during class loading is silently swallowed via `e.printStackTrace()` (lines 21–23).

### Coverage Findings

**A105-18 | Severity: CRITICAL | No test class exists for InfoLogger**
There is no test file for `InfoLogger` anywhere in the test directory. All methods have 0% test coverage.

**A105-19 | Severity: HIGH | Static initializer silently swallows exceptions — not tested**
Lines 15–24: the static initializer wraps `PropertyConfigurator.configure(...)` in a try/catch that only calls `e.printStackTrace()`. If `log4j.properties` is absent from the classpath, logging is silently left unconfigured for the entire application lifetime. No test verifies the failure mode or that the application surfaces a meaningful error.

**A105-20 | Severity: HIGH | `getFileURL()` returns `null` for missing resource — not tested**
`ClassLoader.getResource(s)` (line 27) returns `null` when the resource is not found on the classpath. The result is passed directly into `PropertyConfigurator.configure(null)` inside the static initializer, which throws a `NullPointerException` that is then silently caught. No test covers the null-resource path.

**A105-21 | Severity: HIGH | `logException()` double-prints stack trace — not tested**
`logException(Logger, Exception)` calls both `e.printStackTrace(new PrintWriter(sw))` (line 46) and `e.printStackTrace()` (line 47). The second call dumps the stack trace directly to `System.err` in addition to logging it. No test verifies the intended output, whether the double-print is intentional, or that the `log.error(sw)` call (line 48) actually records the full trace.

**A105-22 | Severity: HIGH | `logException()` called with null Logger not tested**
If `log` is `null`, `log.error(sw)` at line 48 will throw a `NullPointerException`. No test covers this null input.

**A105-23 | Severity: HIGH | `logException()` called with null Exception not tested**
If `e` is `null`, `e.printStackTrace(...)` at line 46 will throw a `NullPointerException`. No test covers this null input.

**A105-24 | Severity: MEDIUM | `getLogger()` wraps `Logger.getLogger()` with no added value — not tested**
`getLogger(String c)` (line 35) is a single-line delegation to `Logger.getLogger(c)`. No test confirms the returned logger is non-null, nor that passing a null or empty class name is handled.

**A105-25 | Severity: MEDIUM | `getFileURL()` for valid resource not tested**
The happy-path of `getFileURL(String s)` — where the resource exists on the classpath — is never tested. There is no assertion that the returned `URL` is non-null and points to the expected resource.

**A105-26 | Severity: LOW | Static initializer constructs a throwaway `InfoLogger` instance**
Line 17: `new InfoLogger()` is constructed solely to call `getFileURL(...)`, even though `getFileURL` accesses `this.getClass().getClassLoader()` which could equivalently be accessed statically. No test documents or validates this unnecessary instantiation pattern.

---

## File 3: RuntimeConf.java

### Reading Evidence

**Class name:** `RuntimeConf`
**Package:** `com.util`
**File:** `src/main/java/com/util/RuntimeConf.java`

**Fields (all `public static`):**

| Field | Line | Value |
|-------|------|-------|
| `projectTitle` | 4 | `"PreStart"` |
| `database` | 5 | `"jdbc/PreStartDB"` |
| `emailFrom` | 6 | `"info@forkliftiq360.com"` |
| `emailFromLinde` | 7 | `"info@fleetiq360.com"` |
| `url` | 8 | `"http://prestart.collectiveintelligence.com.au/"` |
| `ERROR_PAGE` | 9 | `"/globalfailure.do"` |
| `EXPIRE_PAGE` | 10 | `"/expire.do"` |
| `DEFAUTL_TIMEZONE` | 11 | `"Australia/Sydney"` |
| `HOUR_METER` | 12 | `"Hour Meter"` |
| `REGISTER_SUBJECT` | 13 | `"Pandora Registration Successful"` |
| `UPDATE_APP_SUBJECT` | 14 | `"APP Access Account Information"` |
| `UPGRADE_CONTENT` | 15 | `"Upgarde Request"` |
| `RECEIVER_EMAIL` | 16 | `"hui@ciifm.com"` (comment: `//live`) |
| `EMAIL_IMPORT_TITLE` | 17 | `"Company Registration Details"` |
| `EMAIL_RESET_TITLE` | 18 | `"NEW PASSWORD"` |
| `EMAIL_COMMENT_TITLE` | 19 | `"Technician Comment"` |
| `EMAIL_DIGANOSTICS_TITLE` | 20 | `"DIGANOSTICS"` |
| `API_LOGIN` | 22 | `"checklogin"` |
| `API_VEHICLE` | 23 | `"getVehlst"` |
| `API_DRIVER` | 24 | `"getDriverlst"` |
| `API_ATTACHMENT` | 25 | `"getAttlst"` |
| `API_QUESTION` | 26 | `"getQueslst"` |
| `API_RESULT` | 27 | `"saveResult"` |
| `API_PDFRPT` | 28 | `"pdfrpt"` |
| `API_BARCODE` | 29 | `"barcode"` |
| `API_INVALID` | 30 | `"invalid"` |
| `Load_BARCODE` | 31 | `"loadbarcode"` |
| `UPLOAD_FOLDER` | 32 | `"/doc/"` |
| `BROCHURE_FOLDER` | 33 | `"/doc/brochure.pdf"` |
| `XML_FOLDER` | 34 | `"configue.xml"` |
| `IMG_SRC` | 35 | `"images/"` |
| `COMP` | 36 | `"COLLECTIVE INTELLIGENCE"` |
| `PDF_FOLDER` | 37 | `"/temp/"` |
| `RESULT_FAIL` | 40 | `"Failed"` |
| `RESULT_OK` | 41 | `"OK"` |
| `RESULT_INCOMPLETE` | 42 | `"Incomplete"` |
| `ROLE_COMP` | 44 | `"ROLE_COMPANY_GROUP"` |
| `ROLE_SYSADMIN` | 45 | `"ROLE_SYS_ADMIN"` (comment: `//Super ADMIN`) |
| `ROLE_DEALER` | 46 | `"ROLE_DEALER"` |
| `ROLE_SUBCOMP` | 47 | `"ROLE_SUBCOMP"` |
| `ROLE_SITEADMIN` | 48 | `"ROLE_SITE_ADMIN"` |
| `CHECKLIST_SECONDS` | 50 | `600L` |
| `DEFAULT_SCANNERTIME` | 51 | `"01/01/2007 00:00:00"` |
| `LINDEDB` | 53 | `"fleeiq"` |
| `LINDERPTTITLE` | 54 | `"Fleet Check Alert"` |
| `EMPTYLOGO` | 55 | `"blank.JPG"` |
| `emailContent` | 57 | `"This is automaticlaly generated email..."` |
| `debugEmailRecipet` | 58 | `"hui@collectiveintelligence.com.au"` |
| `APIURL` | 60 | `"http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/"` |
| `file_type` | 61 | `".pdf"` |
| `cloudImageURL` | 62 | `"https://s3.amazonaws.com/forkliftiq360/image/"` |
| `v_user` | 64 | `"v_cognitousers"` (`public static final`) |
| `HTTP_OK` | 66 | `200` (`public static final Integer`) |

**Methods:** None. `RuntimeConf` is a pure static-constants holder class with no methods.

### Coverage Findings

**A105-27 | Severity: CRITICAL | No test class exists for RuntimeConf**
There is no test file for `RuntimeConf` anywhere in the test directory. No constant values are validated by any test.

**A105-28 | Severity: CRITICAL | Hardcoded production URL with no environment override — not tested**
`url` (line 8) is hardcoded to `"http://prestart.collectiveintelligence.com.au/"` using plain HTTP (not HTTPS). This is a live production URL embedded directly in source code. There is no environment-variable or properties-file override mechanism, and no test asserts or documents this value. A misconfigured build could silently target the wrong environment.

**A105-29 | Severity: CRITICAL | Hardcoded AWS EC2 instance IP URL — not tested**
`APIURL` (line 60) is hardcoded to `"http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/"` — a specific AWS EC2 public hostname using plain HTTP. This value is environment-specific, non-portable, and embedded in source without any configuration abstraction. No test validates, documents, or flags this value.

**A105-30 | Severity: CRITICAL | Hardcoded AWS S3 bucket URL — not tested**
`cloudImageURL` (line 62) is hardcoded to `"https://s3.amazonaws.com/forkliftiq360/image/"` — a specific S3 bucket URL tied to the production environment. No configuration abstraction exists and no test documents this value.

**A105-31 | Severity: HIGH | Hardcoded live production email recipient — not tested**
`RECEIVER_EMAIL` (line 16) is hardcoded to `"hui@ciifm.com"` with the inline comment `//live`, indicating the developer is aware this is a production address. No environment override exists. A test or staging deployment would send real emails to this person. No test documents or validates this value.

**A105-32 | Severity: HIGH | Hardcoded debug/internal email recipient — not tested**
`debugEmailRecipet` (line 58) is hardcoded to `"hui@collectiveintelligence.com.au"`. The field name is misspelled (`debugEmailRecipet` instead of `debugEmailRecipient`). No test documents the misspelling or the hardcoded address.

**A105-33 | Severity: HIGH | All `public static` (non-final) constants are globally mutable — not tested**
The majority of fields in `RuntimeConf` are `public static` but NOT `final` (e.g. `database`, `url`, `APIURL`, `RECEIVER_EMAIL`, `ROLE_SYSADMIN`, etc.). Any class in the application can mutate these values at runtime (e.g. `RuntimeConf.url = "http://attacker.com/"`). Only `v_user` (line 64) and `HTTP_OK` (line 66) are declared `final`. No test validates the immutability contract of configuration constants or detects accidental mutation.

**A105-34 | Severity: HIGH | Hardcoded JNDI datasource name — not tested**
`database` (line 5) is hardcoded to `"jdbc/PreStartDB"`. This JNDI name must match the server's `context.xml` configuration. No test verifies this value against any configuration, and no abstraction allows environment-specific overrides.

**A105-35 | Severity: HIGH | Plain HTTP used for production URLs — not tested**
Both `url` (line 8) and `APIURL` (line 60) use the `http://` scheme, exposing API calls to man-in-the-middle attacks. No test enforces or documents the expected scheme, and no test would catch a future change from HTTPS back to HTTP.

**A105-36 | Severity: MEDIUM | Multiple typos in field names and string values — not tested**
The following typos exist in public API constants that callers depend on:
- `DEFAUTL_TIMEZONE` (line 11) — should be `DEFAULT_TIMEZONE`
- `UPGRADE_CONTENT` value `"Upgarde Request"` (line 15) — should be `"Upgrade Request"`
- `EMAIL_DIGANOSTICS_TITLE` (line 20) — should be `EMAIL_DIAGNOSTICS_TITLE`
- `LINDEDB` value `"fleeiq"` (line 53) — likely should be `"fleetiq"`
- `emailContent` value contains `"automaticlaly"` (line 57) — should be `"automatically"`
- `debugEmailRecipet` (line 58) — should be `debugEmailRecipient`
- `Load_BARCODE` (line 31) — inconsistent naming convention (should be `LOAD_BARCODE`)
- `XML_FOLDER` value `"configue.xml"` (line 34) — likely should be `"configure.xml"`

No test catches any of these typos. Since all fields are `public static` non-final, any test could assert the expected string values.

**A105-37 | Severity: MEDIUM | `REGISTER_SUBJECT` references "Pandora" brand — not tested**
`REGISTER_SUBJECT` (line 13) is `"Pandora Registration Successful"`. Given the class and system are named PreStart / ForkliftIQ, the "Pandora" brand name appears to be a legacy value from a previous product. No test documents or validates this string, making stale branding invisible.

**A105-38 | Severity: MEDIUM | `DEFAULT_SCANNERTIME` hardcodes a 2007 epoch date — not tested**
`DEFAULT_SCANNERTIME` (line 51) is `"01/01/2007 00:00:00"`. This is an environment-specific sentinel date. No test validates that callers treat it correctly or that the format string matches the application's date-parsing code.

**A105-39 | Severity: MEDIUM | `CHECKLIST_SECONDS` value (600) not tested**
`CHECKLIST_SECONDS` (line 50) is `600L` (10 minutes). This business-rule constant has no test asserting its value or documenting its meaning. Changes to this value would be invisible to the test suite.

**A105-40 | Severity: MEDIUM | `HTTP_OK` duplicates `HttpURLConnection.HTTP_OK` — not tested**
`HTTP_OK` (line 66) is `200`. The standard library already provides `HttpURLConnection.HTTP_OK`. The duplication is undocumented and untested, and any accidental change to the value would not be caught.

**A105-41 | Severity: LOW | `EMPTYLOGO` references `"blank.JPG"` with uppercase extension — not tested**
`EMPTYLOGO` (line 55) is `"blank.JPG"`. The uppercase `.JPG` extension may cause case-sensitivity failures on Linux/Unix file systems. No test validates this path against actual filesystem resources.

**A105-42 | Severity: LOW | `v_user` naming convention inconsistent — not tested**
`v_user` (line 64) is the only `public static final String` that uses a lowercase, underscore-prefixed naming convention rather than the `UPPER_SNAKE_CASE` used by all other constants in the class. No test documents or enforces the intended naming convention.

---

## Summary Table

| Finding | Severity | File | Description |
|---------|----------|------|-------------|
| A105-1 | CRITICAL | ImportExcelData | No test class exists; 0% method coverage |
| A105-2 | HIGH | ImportExcelData | `upload()` happy-path not tested |
| A105-3 | HIGH | ImportExcelData | `upload()` silent exception swallowing not tested |
| A105-4 | HIGH | ImportExcelData | `upload()` always returns `true` — misleading contract untested |
| A105-5 | HIGH | ImportExcelData | `upload()` NPE on null `getFileData()` not tested |
| A105-6 | HIGH | ImportExcelData | `upload()` with empty/default `savePath` not tested |
| A105-7 | HIGH | ImportExcelData | `read()` happy-path not tested |
| A105-8 | HIGH | ImportExcelData | `read()` file-not-found exception not tested |
| A105-9 | HIGH | ImportExcelData | `read()` BufferedReader resource leak not tested |
| A105-10 | MEDIUM | ImportExcelData | `read()` empty file edge case not tested |
| A105-11 | MEDIUM | ImportExcelData | `read()` lines with no commas not tested |
| A105-12 | MEDIUM | ImportExcelData | `read()` consecutive-delimiter behaviour not tested |
| A105-13 | MEDIUM | ImportExcelData | `read()` unused `row`/`col` counters — dead code untested |
| A105-14 | MEDIUM | ImportExcelData | `checkFileExits()` typo in method name; zero coverage |
| A105-15 | MEDIUM | ImportExcelData | `checkFileExits()` with default empty `savePath` not tested |
| A105-16 | LOW | ImportExcelData | Unused POI imports suggest removed functionality — no test |
| A105-17 | LOW | ImportExcelData | `getSavePath()`/`setSavePath()` round-trip not tested |
| A105-18 | CRITICAL | InfoLogger | No test class exists; 0% method coverage |
| A105-19 | HIGH | InfoLogger | Static initializer silently swallows configuration failure |
| A105-20 | HIGH | InfoLogger | `getFileURL()` returns null for missing resource — not tested |
| A105-21 | HIGH | InfoLogger | `logException()` double-prints stack trace — not tested |
| A105-22 | HIGH | InfoLogger | `logException()` with null Logger not tested |
| A105-23 | HIGH | InfoLogger | `logException()` with null Exception not tested |
| A105-24 | MEDIUM | InfoLogger | `getLogger()` null/empty class name not tested |
| A105-25 | MEDIUM | InfoLogger | `getFileURL()` happy-path not tested |
| A105-26 | LOW | InfoLogger | Static initializer constructs throwaway instance — not documented by test |
| A105-27 | CRITICAL | RuntimeConf | No test class exists; 0 constants validated |
| A105-28 | CRITICAL | RuntimeConf | Hardcoded plain-HTTP production URL `url` — no test |
| A105-29 | CRITICAL | RuntimeConf | Hardcoded AWS EC2 IP URL `APIURL` — no test |
| A105-30 | CRITICAL | RuntimeConf | Hardcoded AWS S3 bucket URL `cloudImageURL` — no test |
| A105-31 | HIGH | RuntimeConf | Hardcoded live `RECEIVER_EMAIL` with `//live` comment — no test |
| A105-32 | HIGH | RuntimeConf | Hardcoded `debugEmailRecipet` (misspelled) — no test |
| A105-33 | HIGH | RuntimeConf | All non-final `public static` constants are globally mutable — no test |
| A105-34 | HIGH | RuntimeConf | Hardcoded JNDI datasource name `database` — no test |
| A105-35 | HIGH | RuntimeConf | Plain HTTP scheme in production URLs — no test enforces HTTPS |
| A105-36 | MEDIUM | RuntimeConf | Multiple typos in field names and string values — no test |
| A105-37 | MEDIUM | RuntimeConf | `REGISTER_SUBJECT` references stale "Pandora" brand — no test |
| A105-38 | MEDIUM | RuntimeConf | `DEFAULT_SCANNERTIME` hardcodes 2007 sentinel date — no test |
| A105-39 | MEDIUM | RuntimeConf | `CHECKLIST_SECONDS` business-rule value unconstrained by any test |
| A105-40 | MEDIUM | RuntimeConf | `HTTP_OK` duplicates stdlib constant — no test |
| A105-41 | LOW | RuntimeConf | `EMPTYLOGO` uses uppercase `.JPG` — may fail on case-sensitive FS |
| A105-42 | LOW | RuntimeConf | `v_user` naming convention inconsistent with other constants |

**Total findings: 42**
**CRITICAL: 6 | HIGH: 18 | MEDIUM: 13 | LOW: 5**
