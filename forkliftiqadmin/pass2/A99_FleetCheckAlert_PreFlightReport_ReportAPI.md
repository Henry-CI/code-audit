# Pass 2 Test Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A99
**Date:** 2026-02-26
**Source files audited:**
- `src/main/java/com/report/FleetCheckAlert.java`
- `src/main/java/com/report/PreFlightReport.java`
- `src/main/java/com/report/ReportAPI.java`

**Test directory searched:** `src/test/java/`

---

## Test Search Evidence

Grep results for `FleetCheckAlert` in test directory: **No matches found**
Grep results for `PreFlightReport` in test directory: **No matches found**
Grep results for `ReportAPI` in test directory: **No matches found**
Grep results for method names (`getLogo`, `appendHtmlAlertCotent`, `setContent`, `downloadPDF`, `getExportDir`, `caculatesDate`, `getDriverName`, `getUnitName`, `appendHtmlCotent`) in test directory: **No matches found**

The only test files present in the entire test directory are:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

None of these exercise any class in `com.report`.

---

## Reading Evidence

### Class 1: FleetCheckAlert

**File:** `src/main/java/com/report/FleetCheckAlert.java`
**Class name:** `FleetCheckAlert` (extends `PreFlightReport`)
**Package:** `com.report`

**Fields:**

| Field | Line |
|-------|------|
| `private static Logger log` | 18 |

(All other state fields are inherited from `PreFlightReport`.)

**Methods:**

| Method | Line |
|--------|------|
| `FleetCheckAlert(PropertyMessageResources p)` — constructor | 21 |
| `FleetCheckAlert()` — no-arg constructor | 26 |
| `getLogo(String compId)` — resolves company logo filename | 42 |
| `appendHtmlAlertCotent(String compId)` — builds full HTML alert email body | 58 |
| `setContent(int resultId)` — fetches checklist results and builds HTML table | 80 |

---

### Class 2: PreFlightReport

**File:** `src/main/java/com/report/PreFlightReport.java`
**Class name:** `PreFlightReport`
**Package:** `com.report`

**Fields:**

| Field | Line |
|-------|------|
| `protected String subject` | 17 |
| `protected String title` | 18 |
| `protected Date eDate` | 19 |
| `protected Date sDate` | 20 |
| `protected String frequency` | 21 |
| `protected String content` | 22 |
| `protected String sEmail` | 23 |
| `protected String rEmail` | 24 |
| `protected String htmlCotent` | 25 |
| `PropertyMessageResources pm` | 26 |

**Methods:**

| Method | Line |
|--------|------|
| `PreFlightReport()` — no-arg constructor | 29 |
| `PreFlightReport(PropertyMessageResources p)` — constructor | 35 |
| `PreFlightReport(Date eDate, String frequency, PropertyMessageResources p)` — constructor | 40 |
| `getPm()` | 49 |
| `setPm(PropertyMessageResources pm)` | 53 |
| `getHtmlCotent()` | 57 |
| `setHtmlCotent(String htmlCotent)` | 61 |
| `appendHtmlCotent()` — builds scheduled-report HTML email body | 65 |
| `appendHtmlAlertCotent()` — builds alert HTML email body (no-arg overload) | 77 |
| `getTitle()` | 89 |
| `setTitle(String title)` | 92 |
| `getSubject()` | 95 |
| `setSubject(String subject)` | 98 |
| `getContent()` | 101 |
| `setContent(String compId)` — stub returning 0 | 105 |
| `getFrequency()` | 110 |
| `setFrequency(String frequency)` | 113 |
| `getsEmail()` | 116 |
| `setsEmail(String sEmail)` | 119 |
| `getrEmail()` | 122 |
| `setrEmail(String rEmail)` | 125 |
| `geteDate()` | 128 |
| `seteDate(Date eDate)` | 131 |
| `getsDate()` | 134 |
| `setsDate(Date sDate)` | 137 |
| `caculatesDate()` — delegates to `DateUtil.getStartDate(eDate, frequency)` | 141 |
| `getDriverName(Long driverId)` — delegates to `DriverDAO.getInstance()` | 146 |
| `getUnitName(String unitId)` — delegates to `UnitDAO.getInstance()` | 159 |

---

### Class 3: ReportAPI

**File:** `src/main/java/com/report/ReportAPI.java`
**Class name:** `ReportAPI`
**Package:** `com.report`

**Fields:**

| Field | Line |
|-------|------|
| `protected String subject` | 11 |
| `protected String title` | 12 |
| `protected String content` | 14 |
| `protected String sEmail` | 15 |
| `protected String rEmail` | 16 |
| `protected String fileURL` | 17 |
| `protected String name` | 18 |
| `protected String input` | 19 |
| `protected int responseCode` | 20 |

**Methods:**

| Method | Line |
|--------|------|
| `getResponseCode()` | 22 |
| `setResponseCode(int responseCode)` | 26 |
| `ReportAPI(String name, String input)` — constructor | 30 |
| `downloadPDF()` — calls `HttpDownloadUtility.sendPost` and returns saved file path | 38 |
| `getExportDir(String dirctory)` — returns `System.getProperty("java.io.tmpdir")` | 46 |
| `getSubject()` | 51 |
| `setSubject(String subject)` | 55 |
| `getTitle()` | 59 |
| `setTitle(String title)` | 63 |
| `getContent()` | 68 |
| `setContent(String content)` | 72 |
| `getsEmail()` | 76 |
| `setsEmail(String sEmail)` | 80 |
| `getrEmail()` | 84 |
| `setrEmail(String rEmail)` | 88 |
| `getFileURL()` | 92 |
| `setFileURL(String fileURL)` | 96 |
| `getName()` | 100 |
| `setName(String name)` | 104 |

---

## Findings

### FleetCheckAlert

---

**A99-1 | Severity: CRITICAL | FleetCheckAlert — zero test coverage: no test class exists**

No test file references `FleetCheckAlert` anywhere in `src/test/java/`. The class has no test coverage whatsoever. Every method — `getLogo`, `appendHtmlAlertCotent(String)`, `setContent(int)`, and both constructors — is completely untested.

---

**A99-2 | Severity: CRITICAL | FleetCheckAlert.setContent(int) — NullPointerException before null check on arrResult**

At line 95–103, `arrResult.get(0).getLoc()` and `arrResult.get(0).getOdemeter()` are called unconditionally before the null/size guard at line 105 (`if(arrResult!=null && arrResult.size()>0)`). If `resultDao.getChecklistResultById(resultId)` returns `null` or an empty list, a `NullPointerException` or `IndexOutOfBoundsException` is thrown and silently swallowed by the `catch(Exception e)` at line 162. No test verifies this path.

---

**A99-3 | Severity: CRITICAL | FleetCheckAlert.setContent(int) — exception is silently swallowed, count returns 0 with no caller notification**

The catch block at line 162 logs and prints the exception but does not rethrow or signal failure to the caller. The method returns `count = 0`, which is indistinguishable from "zero results found". No test covers DAO failure, and no test verifies that errors propagate or are surfaced correctly.

---

**A99-4 | Severity: HIGH | FleetCheckAlert.getLogo(String) — no test for EMPTYLOGO branch**

`getLogo` has three distinct return paths: (1) logo equals `RuntimeConf.EMPTYLOGO` ("blank.JPG") → returns "logo_email.png"; (2) logo equals empty string "" → returns "banner.jpg"; (3) any other value → returns the raw value from the DAO. None of these branches are tested. Case-insensitive comparison (`equalsIgnoreCase`) on both checks means mixed-case variants of EMPTYLOGO or empty string must also behave correctly; no test verifies this.

---

**A99-5 | Severity: HIGH | FleetCheckAlert.getLogo(String) — DAO exception not handled**

`CompanyDAO.getInstance().getCompLogo(compId)` can throw an `Exception` (the method declares `throws Exception`). If the DAO call fails, the exception propagates directly to `appendHtmlAlertCotent`, which also declares `throws Exception`. No test validates failure propagation or that a meaningful error is surfaced instead of a partial HTML email body.

---

**A99-6 | Severity: HIGH | FleetCheckAlert.appendHtmlAlertCotent(String) — hardcoded localhost HTTP fetch in HTML header**

`appendHtmlAlertCotent` calls `Util.getHTML("http://localhost:8090/"+RuntimeConf.projectTitle+"/css/bootstrap_table.css")` at line 60 to inline CSS. If that HTTP call fails in production, the CSS will be missing or the method will throw, resulting in a malformed email. No test covers the network-failure path or verifies the resulting HTML structure.

---

**A99-7 | Severity: HIGH | FleetCheckAlert.setContent(int) — odemeter column display logic bug, no test to detect it**

Lines 147–154 use inconsistent guards: the location column is conditionally rendered with `if(!location.equalsIgnoreCase(""))`, but the odometer column uses `if(!location.equalsIgnoreCase("0"))` — checking `location`, not `odemeter`. This appears to be a copy-paste defect (the header guard at line 100 correctly checks `odemeter`). No test exists to detect this logic mismatch.

---

**A99-8 | Severity: HIGH | FleetCheckAlert.setContent(int) — scanner time comparison uses magic constant, no boundary test**

Line 135 computes a time difference against `RuntimeConf.DEFAULT_SCANNERTIME` ("01/01/2007 00:00:00") and appends a warning comment if the difference is less than `86400 * 365` seconds (approximately one year). The threshold is a raw literal embedded in application logic. No test verifies correct behaviour at the boundary (e.g., a result time exactly one year from DEFAULT_SCANNERTIME), or that the `DateUtil.StringTimeDifference` call does not throw on malformed time strings in `resultBean.getTime()`.

---

**A99-9 | Severity: MEDIUM | FleetCheckAlert.setContent(int) — RESULT_INCOMPLETE branch tested only by string equality, no test**

Line 117 checks `status.equalsIgnoreCase(RuntimeConf.RESULT_INCOMPLETE)`. There is no test for the INCOMPLETE path, the non-INCOMPLETE (failures/comment extraction via `resultDao.printErrors`) path, or the case where `resultDao.printErrors` returns a null or short array.

---

**A99-10 | Severity: MEDIUM | FleetCheckAlert.setContent(int) — resultBean.getComment() appended unconditionally with no null guard**

At line 128, `comment += resultBean.getComment()` is called with no null check. If `getComment()` returns `null`, the string `"null"` is silently appended to the comment cell. No test covers a null comment value.

---

### PreFlightReport

---

**A99-11 | Severity: CRITICAL | PreFlightReport — zero test coverage: no test class exists**

No test file references `PreFlightReport` anywhere in `src/test/java/`. The class has no test coverage. All 26 methods are untested.

---

**A99-12 | Severity: HIGH | PreFlightReport.caculatesDate() — null eDate or null frequency causes silent failure, no test**

`caculatesDate()` delegates directly to `DateUtil.getStartDate(this.eDate, this.frequency)` at line 143. If `eDate` is `null` (the no-arg constructor leaves it null) or `frequency` is empty/null, the behaviour depends entirely on `DateUtil`. The three-arg constructor calls `caculatesDate()` at line 44 before setting up `pm`, but after setting `eDate` and `frequency` — so a null `eDate` passed to the constructor will propagate into `DateUtil`. No test verifies any of these paths.

---

**A99-13 | Severity: HIGH | PreFlightReport.appendHtmlCotent() — hardcoded localhost HTTP fetch, no test for network failure**

`appendHtmlCotent()` at line 68 calls `Util.getHTML("http://localhost:8090/"+RuntimeConf.projectTitle+"/css/bootstrap_table.css")`. If the local application server is unreachable, the CSS will be absent or an exception thrown, resulting in a broken HTML report. No test covers this path or validates the structure of the generated HTML.

---

**A99-14 | Severity: HIGH | PreFlightReport.appendHtmlAlertCotent() — same localhost HTTP fetch defect as appendHtmlCotent, no test**

The no-arg `appendHtmlAlertCotent()` at line 79 has the identical hardcoded localhost CSS fetch. Same risk as A99-13; no test coverage.

---

**A99-15 | Severity: HIGH | PreFlightReport.getDriverName(Long) — DAO exception propagates unchecked, no test**

`getDriverName` at line 146 calls `DriverDAO.getInstance().getDriverName(driverId)` with no local error handling. A null `driverId`, an unknown driver ID, or a DAO failure will throw and propagate to `FleetCheckAlert.setContent`, where it is silently caught. No test verifies any failure path.

---

**A99-16 | Severity: HIGH | PreFlightReport.getUnitName(String) — chained call with no null guard, no test**

`getUnitName` at line 161 calls `UnitDAO.getInstance().getUnitById(unitId).get(0).getName()` with two chained dereferences: `.get(0)` will throw `IndexOutOfBoundsException` if the DAO returns an empty list, and `.getName()` will throw `NullPointerException` if the first element is null. Neither case is guarded. The double semicolon at line 161 is also a minor style defect. No test covers the empty-result or null-element paths.

---

**A99-17 | Severity: MEDIUM | PreFlightReport.setContent(String compId) — stub method always returns 0, no test or documentation**

The base-class `setContent(String compId)` at line 105 is a no-op stub returning 0. It is overridden in `FleetCheckAlert` (by `setContent(int resultId)` — note the different parameter type, making it an overload, not an override). No test verifies this overloading relationship, and the stub is undocumented.

---

**A99-18 | Severity: MEDIUM | PreFlightReport — typo in field name `htmlCotent` is propagated throughout public API**

The field `htmlCotent` (line 25) and its accessors `getHtmlCotent()` / `setHtmlCotent()` (lines 57, 61) contain a misspelling ("Cotent" instead of "Content"). The same misspelling appears in `appendHtmlAlertCotent` method names in both `PreFlightReport` and `FleetCheckAlert`. This is a naming defect baked into the public API. No test catches the discrepancy, and any future refactoring would require coordinated search-and-replace across callers.

---

**A99-19 | Severity: LOW | PreFlightReport — three-arg constructor calls caculatesDate() before setPm(), pm is null during construction**

In the three-arg constructor (line 40–46), `caculatesDate()` is called at line 44 before `this.setPm(p)` at line 45. If a future subclass overrides `caculatesDate()` and uses `pm`, a `NullPointerException` would result. Currently safe because `caculatesDate()` does not use `pm`, but the ordering is fragile. No test documents or enforces the construction sequence.

---

**A99-20 | Severity: LOW | PreFlightReport.caculatesDate() — method name misspelled ("caculate" instead of "calculate")**

The method name `caculatesDate` (line 141) is a misspelling. It is part of the public API (referenced in the three-arg constructor and callable by subclasses). No test documents the correct name, making future renaming require coordinated change.

---

### ReportAPI

---

**A99-21 | Severity: CRITICAL | ReportAPI — zero test coverage: no test class exists**

No test file references `ReportAPI` anywhere in `src/test/java/`. Every method — including `downloadPDF`, `getExportDir`, constructors, and all accessors — is completely untested.

---

**A99-22 | Severity: CRITICAL | ReportAPI.downloadPDF() — HTTP failure path entirely untested**

`downloadPDF()` at line 38 calls `HttpDownloadUtility.sendPost(name, input, this.getExportDir(""))`. If the HTTP POST fails (network error, timeout, non-200 response), no exception handling exists in `downloadPDF()` itself; the exception propagates to the caller. The method stores the HTTP response code in `this.responseCode` but provides no mechanism to signal a failed download to the caller separately from a thrown exception. No test covers: (1) successful download, (2) HTTP non-200 response, (3) network exception, or (4) that `getSaveFilePath()` returns a valid path after a successful call.

---

**A99-23 | Severity: HIGH | ReportAPI.getExportDir(String) — unused parameter `dirctory` (misspelled), no test**

`getExportDir(String dirctory)` at line 46 declares a parameter `dirctory` (misspelled "directory") that is never used — the method always returns `System.getProperty("java.io.tmpdir")` regardless. The parameter name suggests the method was intended to accept a custom directory but the implementation ignores it. No test verifies the return value or the dead-parameter behaviour.

---

**A99-24 | Severity: HIGH | ReportAPI.downloadPDF() — return value is the static state of HttpDownloadUtility.getSaveFilePath(), no test**

`HttpDownloadUtility.getSaveFilePath()` appears to return a static/global value set as a side effect of `sendPost`. This creates a concurrency hazard: if two `ReportAPI` instances call `downloadPDF()` concurrently, the second `getSaveFilePath()` call may return the path from the first download. No test exercises concurrent use or validates that the returned path corresponds to the current download.

---

**A99-25 | Severity: HIGH | ReportAPI constructor — null name or null input not guarded, no test**

The constructor `ReportAPI(String name, String input)` at line 30 assigns `name` and `input` directly with no null checks. A null `name` or `input` passed to `HttpDownloadUtility.sendPost` in `downloadPDF()` may cause a NullPointerException or malformed HTTP request. No test verifies null-argument handling.

---

**A99-26 | Severity: MEDIUM | ReportAPI — `input` field has no getter, breaks encapsulation audit trail**

The `input` field (line 19) is set in the constructor but has no public getter method, unlike all other fields in the class. This prevents callers from inspecting the value after construction. No test documents or enforces this asymmetry, and it is likely an oversight.

---

**A99-27 | Severity: LOW | ReportAPI — `fileURL`, `content`, `subject`, `title`, `sEmail`, `rEmail` fields are set but never read internally**

Several fields (`fileURL`, `content`, `subject`, `title`, `sEmail`, `rEmail`) are defined with getters and setters but are never referenced within the class logic itself (only `name`, `input`, and `responseCode` are used by `downloadPDF` and `getExportDir`). These fields appear to be placeholders for functionality not yet implemented. No test verifies that callers are expected to use these fields via the email-sending workflow.

---

## Summary Table

| Finding | Severity | Class | Description |
|---------|----------|-------|-------------|
| A99-1 | CRITICAL | FleetCheckAlert | Zero test coverage — no test class |
| A99-2 | CRITICAL | FleetCheckAlert | NPE / IOOBE in setContent(int) before null guard on arrResult |
| A99-3 | CRITICAL | FleetCheckAlert | Exception silently swallowed in setContent(int), count=0 indistinguishable from failure |
| A99-4 | HIGH | FleetCheckAlert | getLogo branches untested (EMPTYLOGO, empty string, normal path) |
| A99-5 | HIGH | FleetCheckAlert | getLogo DAO exception not handled |
| A99-6 | HIGH | FleetCheckAlert | appendHtmlAlertCotent hardcoded localhost CSS fetch — network failure path untested |
| A99-7 | HIGH | FleetCheckAlert | Odometer column rendered using location guard (copy-paste bug), untested |
| A99-8 | HIGH | FleetCheckAlert | Scanner time boundary comparison uses magic literal, no boundary tests |
| A99-9 | MEDIUM | FleetCheckAlert | RESULT_INCOMPLETE and printErrors paths untested |
| A99-10 | MEDIUM | FleetCheckAlert | getComment() result appended without null guard |
| A99-11 | CRITICAL | PreFlightReport | Zero test coverage — no test class |
| A99-12 | HIGH | PreFlightReport | caculatesDate with null eDate/frequency causes silent failure |
| A99-13 | HIGH | PreFlightReport | appendHtmlCotent hardcoded localhost CSS fetch untested |
| A99-14 | HIGH | PreFlightReport | appendHtmlAlertCotent hardcoded localhost CSS fetch untested |
| A99-15 | HIGH | PreFlightReport | getDriverName DAO exception propagates unchecked, no test |
| A99-16 | HIGH | PreFlightReport | getUnitName chained .get(0).getName() with no null/empty guard |
| A99-17 | MEDIUM | PreFlightReport | setContent(String) is a stub returning 0 with no documentation or test |
| A99-18 | MEDIUM | PreFlightReport | Misspelled field/method name htmlCotent / appendHtmlAlertCotent in public API |
| A99-19 | LOW | PreFlightReport | Three-arg constructor calls caculatesDate() before setPm(), fragile ordering |
| A99-20 | LOW | PreFlightReport | Method name caculatesDate misspelled (should be calculatesDate) |
| A99-21 | CRITICAL | ReportAPI | Zero test coverage — no test class |
| A99-22 | CRITICAL | ReportAPI | downloadPDF HTTP failure path entirely untested |
| A99-23 | HIGH | ReportAPI | getExportDir has unused misspelled parameter `dirctory` |
| A99-24 | HIGH | ReportAPI | downloadPDF relies on static getSaveFilePath() — concurrency hazard, untested |
| A99-25 | HIGH | ReportAPI | Constructor allows null name/input with no guard |
| A99-26 | MEDIUM | ReportAPI | `input` field has no getter (asymmetric with all other fields) |
| A99-27 | LOW | ReportAPI | Several fields (fileURL, content, subject, etc.) unused internally — placeholder code |

**Total findings: 27**
**CRITICAL: 6 | HIGH: 13 | MEDIUM: 5 | LOW: 3**
