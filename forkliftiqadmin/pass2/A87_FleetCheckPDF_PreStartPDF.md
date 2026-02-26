# Pass 2 Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A87
**Date:** 2026-02-26
**Files Audited:**
- `src/main/java/com/pdf/FleetCheckPDF.java`
- `src/main/java/com/pdf/PreStartPDF.java`

---

## Test Discovery

### Grep results: `FleetCheckPDF` in test directory
No matches found in `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`.

### Grep results: `PreStartPDF` in test directory
No matches found in `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`.

### Existing test files in test directory
```
com/calibration/UnitCalibrationImpactFilterTest.java
com/calibration/UnitCalibrationTest.java
com/calibration/UnitCalibratorTest.java
com/util/ImpactUtilTest.java
```

Neither `FleetCheckPDF` nor `PreStartPDF` appear in any test file. There are no test classes for either source class.

---

## Source File Evidence

### File 1: `FleetCheckPDF.java`

**Class name:** `FleetCheckPDF`
**Package:** `com.pdf`
**Extends:** `PreStartPDF`

**Fields:**

| Field Name | Line | Type | Notes |
|---|---|---|---|
| `log` | 29 | `static Logger` | Private static, InfoLogger-backed |
| `pdfurl` | 30 | `String` | Instance-initialized via `getProtectionDomain().getCodeSource()` |
| `unitDAO` | 31 | `UnitDAO` | Singleton obtained at field init |
| `driverDao` | 32 | `DriverDAO` | Singleton obtained at field init |

**Methods:**

| Method Name | Line | Visibility | Notes |
|---|---|---|---|
| `FleetCheckPDF(String compId, Date from, Date to, String docRoot)` | 34 | `public` | Constructor; calls `super()`, sets title, result path, image path |
| `createTable(Document document)` | 47 | `public` | Overrides `PreStartPDF.createTable`; builds 6-column PDF table from DB data |

---

### File 2: `PreStartPDF.java`

**Class name:** `PreStartPDF`
**Package:** `com.pdf`

**Fields:**

| Field Name | Line | Type | Notes |
|---|---|---|---|
| `result` | 29 | `String` | `protected` |
| `title` | 30 | `String` | `protected` |
| `image` | 31 | `String` | `protected` |
| `from` | 32 | `Date` | `protected` |
| `to` | 33 | `Date` | `protected` |
| `compId` | 34 | `String` | `protected` |
| `catFont` | 35 | `static Font` | `protected static` |
| `redFont` | 36 | `static Font` | `protected static` |
| `subFont` | 37 | `static Font` | `protected static` |
| `hrFont` | 38 | `static Font` | `protected static` |
| `hdFont` | 39 | `static Font` | `protected static` |
| `smallBold` | 40 | `static Font` | `protected static` |

**Methods:**

| Method Name | Line | Visibility | Notes |
|---|---|---|---|
| `PreStartPDF(String compId, Date from, Date to)` | 42 | `public` | Constructor; assigns fields |
| `createPdf()` | 54 | `public` | Orchestrates PDF creation; returns `result` path |
| `addContent(Document document)` | 68 | `private` | Delegates to `createTable` |
| `createTable(Document document)` | 77 | `public` | Base stub table; intended to be overridden |
| `addMetaData(Document document)` | 98 | `private` | Sets PDF title, subject, author, creator |
| `addTitlePage(Document document)` | 105 | `private` | Adds title, start/end date paragraphs |
| `addFooter(Document document)` | 116 | `private` | Adds copyright paragraph |
| `createList(Section subCatPart)` | 125 | `private` | Dead code: creates a static 3-item list, never called |
| `addEmptyLine(Paragraph paragraph, int number)` | 133 | `private` | Adds N blank paragraphs |
| `addImage(Document document)` | 139 | `private` | Loads banner image from `this.image` path, scales if oversized |
| `getImage()` | 149 | `public` | Getter |
| `setImage(String image)` | 153 | `public` | Setter |
| `getResult()` | 157 | `public` | Getter |
| `setResult(String result)` | 161 | `public` | Setter |
| `getTitle()` | 165 | `public` | Getter |
| `setTitle(String title)` | 169 | `public` | Setter |
| `getFrom()` | 173 | `public` | Getter |
| `setFrom(Date from)` | 177 | `public` | Setter |
| `getTo()` | 181 | `public` | Getter |
| `setTo(Date to)` | 185 | `public` | Setter |

---

## Findings

### PreStartPDF.java

**A87-1 | Severity: CRITICAL | No test class exists for PreStartPDF**
There is no test file for `PreStartPDF` anywhere in the test directory. Zero coverage. All methods — constructor, `createPdf`, `addMetaData`, `addTitlePage`, `addFooter`, `addContent`, `createTable`, `addImage`, `addEmptyLine`, and all getters/setters — are completely untested.

**A87-2 | Severity: HIGH | `createPdf()` not tested for IOException on FileOutputStream failure**
`createPdf()` at line 54 opens a `FileOutputStream(result)` without testing what happens when `result` is an invalid or unwritable path (e.g., directory does not exist, no write permission). No test exercises the `IOException` throw path.

**A87-3 | Severity: HIGH | `addImage()` not tested for missing or malformed image file**
`addImage()` at line 139 calls `Image.getInstance(this.image)`, which throws `BadElementException` or `IOException` if the file does not exist, the path is empty, or the file is corrupt. No test exercises these failure paths. The method declares `throws DocumentException, IOException` but no test verifies the thrown exception.

**A87-4 | Severity: HIGH | `addImage()` not tested: empty `image` field path**
If `setImage("")` or `setImage(null)` is called before `createPdf()`, `Image.getInstance(this.image)` at line 140 will throw a `MalformedURLException` or `NullPointerException`. No test covers this case.

**A87-5 | Severity: HIGH | `createPdf()` not tested: null/empty `result` path**
If `result` is empty (default value `""` at line 29) and `createPdf()` is called without calling `setResult()`, `new FileOutputStream("")` will throw `FileNotFoundException`. No test covers this default-state failure.

**A87-6 | Severity: MEDIUM | `addTitlePage()` not tested with null `from` or `to` date**
`addTitlePage()` at line 105 calls `DateUtil.dateToString(this.from)` and `DateUtil.dateToString(this.to)`. If either `from` or `to` is null (field default is null, since `Date` is an object), a `NullPointerException` may propagate from `DateUtil`. No test verifies null-date handling.

**A87-7 | Severity: MEDIUM | `createTable()` base implementation is a stub with no meaningful behavior**
The base `createTable()` at line 77 inserts a hardcoded placeholder table. It is `public` and can be called directly, yet no test verifies that calling it on a `PreStartPDF` instance produces a usable document or throws on a closed/null document.

**A87-8 | Severity: MEDIUM | `addEmptyLine()` not tested for zero or negative `number`**
`addEmptyLine()` at line 133 loops `for (int i = 0; i < number; i++)`. When `number` is 0 nothing is added; when `number` is negative the loop is skipped silently. No test verifies either boundary.

**A87-9 | Severity: MEDIUM | All getters and setters untested**
The six getter/setter pairs (`getResult/setResult`, `getTitle/setTitle`, `getImage/setImage`, `getFrom/setFrom`, `getTo/setTo`, and `compId` — which has no getter/setter) are untested. While individually simple, no test confirms round-trip correctness or that setting null is safe.

**A87-10 | Severity: LOW | `createList()` is dead code — private, never called**
`createList(Section subCatPart)` at line 125 is declared `private`, accepts a parameter of type `Section`, and is never invoked from anywhere in the class or its subclasses. No test can reach it. This is unreachable dead code that should be removed or wired up.

**A87-11 | Severity: LOW | Copyright string at line 118 uses a raw backslash-u escape that does not produce a Unicode character**
The footer string `"Copyright \\u00A9 2012-2018 ..."` uses `\\u00A9` (double-backslash), which means the literal text `\u00A9` is rendered in the PDF rather than the copyright symbol (c). No test verifies the content of the footer paragraph text.

---

### FleetCheckPDF.java

**A87-12 | Severity: CRITICAL | No test class exists for FleetCheckPDF**
There is no test file for `FleetCheckPDF` anywhere in the test directory. Zero coverage. The constructor and `createTable` are completely untested.

**A87-13 | Severity: CRITICAL | `pdfurl` field initialization can throw NullPointerException or StringIndexOutOfBoundsException at class load time**
Line 30: `private String pdfurl = this.getClass().getProtectionDomain().getCodeSource().getLocation().toString().substring(6) + "/../../../../../temp/";`
`getProtectionDomain()` can return null in some ClassLoader configurations; `getCodeSource()` can also return null. If either returns null, `.toString()` or `.getLocation()` will throw a `NullPointerException` before any constructor body runs. Additionally, `substring(6)` assumes the URL string is at least 6 characters long. No test exercises this initialization path, and `pdfurl` is never used anywhere in the class body — making this a doubly dead and fragile field.

**A87-14 | Severity: CRITICAL | `FleetCheckPDF` constructor sets `result` path using `Util.generateRadomName()` — randomness makes PDF output path untestable and non-deterministic**
Line 37: `setResult(docRoot + RuntimeConf.PDF_FOLDER + Util.generateRadomName() + ".pdf")`. The generated file name is random on every instantiation. No test verifies the resulting path is valid, accessible, or follows an expected pattern. The random name generation is not injectable or mockable.

**A87-15 | Severity: CRITICAL | `createTable()` makes live DAO calls — untestable without database**
`createTable()` calls `driverDao.getAllDriver(compId, false)` at line 88, `new ResultDAO()` at line 99, `resultDao.getChecklistResultInc()` at line 100, `driverDao.getDriverName()` at line 108, `unitDAO.getUnitById()` at line 119, `resultDao.getOverallStatus()` at line 121, and `resultDao.printErrors()` at line 129. All DAO instances are created via singletons or `new` directly in field initializers or method bodies, making them impossible to mock without significant refactoring. There are no integration tests covering these calls either.

**A87-16 | Severity: HIGH | `createTable()` not tested: null or empty `compId`**
If `compId` is null or empty, `driverDao.getAllDriver(compId, false)` at line 88 may return null or throw an exception depending on DAO implementation. The code checks `if (arrDriver == null || arrDriver.size() == 0)` but does not handle a DAO exception from invalid input. No test verifies this path.

**A87-17 | Severity: HIGH | `createTable()` not tested: `driverDao.getAllDriver()` returns null vs empty list**
The null-check at line 90 (`arrDriver == null || arrDriver.size() == 0`) covers both cases, but the behavior diverges: when null, `emptyflag` is set to `false`; when non-null but empty, the same branch fires. The "empty company" message is added to the table only when `emptyflag` is false at the end (line 160), but `emptyflag` starts as `true` at line 89 and is only set to `false` inside the null/empty branch. This means the "No Driver is registered" message is added to the table but then the "No Fleetcheck is performed" message is also NOT added (because `emptyflag` is `false`). The logic interaction is subtle and untested.

**A87-18 | Severity: HIGH | `createTable()` not tested: `unitDAO.getUnitById()` returns empty list — causes ArrayIndexOutOfBoundsException**
Line 119: `unitDAO.getUnitById(resultBean.getUnit_id()).get(0)`. If `getUnitById()` returns an empty list (no unit found for the given ID), `.get(0)` throws `IndexOutOfBoundsException`. This is caught only by the broad `catch (Exception e)` at line 165, which silently logs and continues, potentially leaving the PDF table in an inconsistent state with missing rows. No test covers this case.

**A87-19 | Severity: HIGH | `createTable()` not tested: `resultDao.printErrors()` returns array with fewer than 2 elements**
Line 129-131: `String[] result = resultDao.printErrors(...); failures = result[0]; comment = result[1];`. If `printErrors()` returns null or a single-element array, an `ArrayIndexOutOfBoundsException` or `NullPointerException` is thrown. This is again silently swallowed by the broad catch block. No test covers this.

**A87-20 | Severity: HIGH | `createTable()` silent exception swallowing hides failures**
The `catch (Exception e)` block at line 165 calls `InfoLogger.logException` and `e.printStackTrace()` but does not rethrow or signal the error to the caller. `document.add(table)` at line 169 is outside the try block, meaning a partially-constructed table is always added to the document even after an exception. No test verifies the document state after an exception is caught.

**A87-21 | Severity: HIGH | `createTable()` not tested: `resultBean.getUnit_id()` null branch sets id to `"0"` — no test for unit-not-found result**
Lines 116-118: if `unit_id` is null it is coerced to `"0"`. `unitDAO.getUnitById("0")` is then called. The behavior when no unit has ID `"0"` (returning an empty list) leads directly to the `ArrayIndexOutOfBoundsException` described in A87-18. No test covers this specific null-to-zero coercion path.

**A87-22 | Severity: HIGH | `createTable()` not tested: `DateUtil.StringTimeDifference()` called with potentially malformed `resultBean.getTime()` string**
Line 138: `DateUtil.StringTimeDifference(resultBean.getTime(), RuntimeConf.DEFAULT_SCANNERTIME, TimeUnit.SECONDS, "dd/mm/yyyy HH:mm:ss")`. If `getTime()` returns null, an empty string, or a string in an unexpected format, `StringTimeDifference` may throw a `ParseException` or `NullPointerException`. No test verifies this date-comparison logic.

**A87-23 | Severity: MEDIUM | `createTable()` not tested: `emptyflag` logic is incorrect when all drivers have no results**
`emptyflag` is initialized to `true` at line 89. If drivers exist but none have any results (`arrResult` is null or empty for every driver), `emptyflag` remains `true` throughout the loop, and the "No Fleetcheck is performed" message is added at line 161-163. This is the correct behavior, but it is entirely untested.

**A87-24 | Severity: MEDIUM | `FleetCheckPDF` constructor not tested: null `docRoot` parameter**
If `docRoot` is null, the expression `docRoot + RuntimeConf.PDF_FOLDER + ...` at line 37 produces the string `"null/temp/..."`, and `docRoot + "/" + RuntimeConf.IMG_SRC + "/banner.jpg"` at line 38 similarly becomes `"null/images/banner.jpg"`. These silently produce nonsense paths. No test verifies constructor input validation.

**A87-25 | Severity: MEDIUM | `createTable()` contains a dead variable: `Boolean first` is never toggled before use**
Line 103: `Boolean first = true;`. Line 107: `if (first) { ... }` — this block always executes because `first` is never changed before the `if`. Line 142: `first = false;` is set inside the inner result loop, but `first` is never read again after that point. The conditional at line 107 is always true and could be removed. No test exposes this logic error.

**A87-26 | Severity: MEDIUM | `pdfurl` field is initialized but never read**
The `pdfurl` field at line 30 is set to a path derived from the code source location. It is never used anywhere in `FleetCheckPDF` — the actual output path is set via `setResult()` in the constructor using `docRoot`. This field is dead and its fragile initialization (A87-13) serves no purpose. No test verifies or flags this.

**A87-27 | Severity: LOW | Typo in column header "Vehcile" at line 58 is untested**
The PDF table header cell at line 58 reads `"Vehcile"` instead of `"Vehicle"`. No test verifies the string content of generated PDF table headers, so this user-visible defect goes undetected.

**A87-28 | Severity: LOW | Typo in failure message "*Safty Check incomplete" at line 127 is untested**
The string `"*Safty Check incomplete"` should be `"*Safety Check incomplete"`. No test verifies the content of the failures string written to the PDF.

**A87-29 | Severity: LOW | `FleetCheckPDF` constructor is used in production code (AppAPIAction.java line 357) only in a commented-out block**
A grep of the codebase shows the only non-source reference to `FleetCheckPDF` in `AppAPIAction.java` at line 357 is commented out (`////`). The class is effectively unused in the live application. Combined with zero test coverage, there is no executed path at all for this class.

**A87-30 | Severity: INFO | `rowspan` is computed as `arrResult.size()` but cell is only added once for the first driver row**
Line 106: `int rowspan = arrResult.size();`. Line 111: `cell.setRowspan(rowspan)`. The driver name cell spans all result rows for that driver, which is correct iText usage. However, if `arrResult.size()` is 1, the rowspan is set to 1, which is effectively a normal cell. This works but is unnecessary. No test verifies multi-row rowspan rendering.

---

## Summary Table

| Finding | Severity | Class | Description |
|---|---|---|---|
| A87-1 | CRITICAL | PreStartPDF | No test class exists |
| A87-2 | HIGH | PreStartPDF | `createPdf()` IOException on bad result path untested |
| A87-3 | HIGH | PreStartPDF | `addImage()` missing/corrupt file error path untested |
| A87-4 | HIGH | PreStartPDF | `addImage()` null/empty image path untested |
| A87-5 | HIGH | PreStartPDF | `createPdf()` with default empty result path untested |
| A87-6 | MEDIUM | PreStartPDF | `addTitlePage()` null from/to date untested |
| A87-7 | MEDIUM | PreStartPDF | Base `createTable()` stub behavior untested |
| A87-8 | MEDIUM | PreStartPDF | `addEmptyLine()` zero/negative number boundary untested |
| A87-9 | MEDIUM | PreStartPDF | All getters and setters untested |
| A87-10 | LOW | PreStartPDF | `createList()` is dead code, unreachable |
| A87-11 | LOW | PreStartPDF | Copyright Unicode escape is literal backslash, untested |
| A87-12 | CRITICAL | FleetCheckPDF | No test class exists |
| A87-13 | CRITICAL | FleetCheckPDF | `pdfurl` field init can NPE at class load; getCodeSource() nullable |
| A87-14 | CRITICAL | FleetCheckPDF | Non-deterministic random PDF path not injectable or testable |
| A87-15 | CRITICAL | FleetCheckPDF | `createTable()` hardcodes live DAO calls; not mockable |
| A87-16 | HIGH | FleetCheckPDF | `createTable()` null/empty compId unhandled |
| A87-17 | HIGH | FleetCheckPDF | `createTable()` null vs empty driver list logic interaction untested |
| A87-18 | HIGH | FleetCheckPDF | `unitDAO.getUnitById().get(0)` throws if list is empty |
| A87-19 | HIGH | FleetCheckPDF | `printErrors()` short array causes ArrayIndexOutOfBoundsException |
| A87-20 | HIGH | FleetCheckPDF | Silent exception swallow; partial table always added to document |
| A87-21 | HIGH | FleetCheckPDF | Null unit_id coerced to "0"; leads to empty list crash path |
| A87-22 | HIGH | FleetCheckPDF | `StringTimeDifference()` with malformed time string untested |
| A87-23 | MEDIUM | FleetCheckPDF | All-drivers-no-results emptyflag path untested |
| A87-24 | MEDIUM | FleetCheckPDF | Constructor null docRoot silently produces invalid paths |
| A87-25 | MEDIUM | FleetCheckPDF | `Boolean first` variable always true; dead conditional |
| A87-26 | MEDIUM | FleetCheckPDF | `pdfurl` field initialized but never read (dead field) |
| A87-27 | LOW | FleetCheckPDF | Column header typo "Vehcile" undetected |
| A87-28 | LOW | FleetCheckPDF | Failure message typo "*Safty Check incomplete" undetected |
| A87-29 | LOW | FleetCheckPDF | Class only referenced in commented-out production code |
| A87-30 | INFO | FleetCheckPDF | Rowspan=1 edge case for single-result drivers not verified |

**Total findings: 30**
**CRITICAL: 5 | HIGH: 12 | MEDIUM: 8 | LOW: 4 | INFO: 1**
