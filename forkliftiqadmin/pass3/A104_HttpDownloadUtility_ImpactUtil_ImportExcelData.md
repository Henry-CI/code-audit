# Pass 3 – Documentation Audit
**Agent:** A104
**Audit run:** 2026-02-26-01
**Files audited:**
- `src/main/java/com/util/HttpDownloadUtility.java`
- `src/main/java/com/util/ImpactUtil.java`
- `src/main/java/com/util/ImportExcelData.java`

---

## 1. Reading Evidence

### 1.1 HttpDownloadUtility.java

| Element | Kind | Line |
|---|---|---|
| `HttpDownloadUtility` | class | 21 |
| `log` | `static Logger` | 23 |
| `BUFFER_SIZE` | `static final int` | 25 |
| `saveFilePath` | `static String` | 26 |
| `downloadFile(String fileName, String fileURL, String saveDir)` | `public static void` | 35 |
| `sendPost(String fileName, String input, String saveDir)` | `public static int` | 88 |
| `getSaveFilePath()` | `public static String` | 186 |
| `setSaveFilePath(String saveFilePath)` | `public static void` | 190 |

### 1.2 ImpactUtil.java

| Element | Kind | Line |
|---|---|---|
| `ImpactUtil` | class | 5 |
| `G_FORCE_COEFFICIENT` | `static final double` | 6 |
| `BLUE_IMPACT_COEFFICIENT` | `static final double` | 7 |
| `AMBER_IMPACT_COEFFICIENT` | `static final double` | 8 |
| `RED_IMPACT_COEFFICIENT` | `static final double` | 9 |
| `calculateGForceOfImpact(long impactValue)` | `public static double` | 11 |
| `calculateGForceRequiredForImpact(double impactThreshold, ImpactLevel impactLevel)` | `public static double` | 15 |
| `getImpactLevelCoefficient(ImpactLevel impactLevel)` | `private static double` | 19 |
| `getCSSColor(ImpactLevel impactLevel)` | `public static String` | 32 |
| `calculateImpactLevel(int impactValue, int impactThreshold)` | `public static ImpactLevel` | 45 |
| `UnhandledImpactLevelException` | inner class (package-private) | 52 |
| `UnhandledImpactLevelException(ImpactLevel impactLevel)` | constructor (package-private) | 53 |

### 1.3 ImportExcelData.java

| Element | Kind | Line |
|---|---|---|
| `ImportExcelData` | class | 27 |
| `savePath` | `String` (instance field) | 29 |
| `upload(FormFile formFile)` | `public boolean` | 32 |
| `read(String fileName)` | `public List<ArrayList<String>>` | 47 |
| `getSavePath()` | `public String` | 75 |
| `setSavePath(String savePath)` | `public void` | 79 |
| `checkFileExits()` | `public boolean` | 83 |

---

## 2. Findings

### A104-1 [LOW] HttpDownloadUtility — Missing class-level Javadoc

**File:** `util/HttpDownloadUtility.java`, line 21
**Description:** The class `HttpDownloadUtility` has no class-level Javadoc comment. There is no description of the class purpose, authorship, or usage contract.
**Standard:** Every public class should carry a `/** ... */` block directly above its declaration.

---

### A104-2 [MEDIUM] HttpDownloadUtility.downloadFile — Javadoc present but @param tag for `fileName` is missing

**File:** `util/HttpDownloadUtility.java`, lines 29–36
**Existing Javadoc:**
```java
/**
 * Downloads a file from a URL
 * @param fileURL HTTP URL of the file to be downloaded
 * @param saveDir path of the directory to save the file
 * @throws IOException
 */
public static void downloadFile(String fileName, String fileURL, String saveDir)
```
**Description:** The method signature has three parameters — `fileName`, `fileURL`, and `saveDir` — but the Javadoc documents only `fileURL` and `saveDir`. The `@param fileName` tag is absent entirely. There is also no `@return` tag, though the method is `void` so that is acceptable.

---

### A104-3 [MEDIUM] HttpDownloadUtility.downloadFile — Inaccurate comment: `BUFFER_SIZE` comment claims "Max file size 4MB" but it is a read-buffer size, not a file-size limit

**File:** `util/HttpDownloadUtility.java`, line 25
```java
private static final int BUFFER_SIZE = 4096; // Max file size 4MB.
```
**Description:** `BUFFER_SIZE` is the I/O read buffer length in bytes (4 096 bytes = 4 KB, not 4 MB). The comment `// Max file size 4MB.` is incorrect on two counts: (a) the unit is KB not MB, and (b) the constant controls chunk size, not any file-size ceiling — there is no upper bound enforced on the file being downloaded. This comment is technically inaccurate and could mislead a developer into believing there is an enforced size limit.

---

### A104-4 [MEDIUM] HttpDownloadUtility.sendPost — Undocumented non-trivial public method

**File:** `util/HttpDownloadUtility.java`, line 88
```java
public static int sendPost(String fileName, String input, String saveDir) throws Exception {
```
**Description:** `sendPost` has no Javadoc at all. The method is non-trivial: it overrides `fileName` with a hardcoded value (`"pandora-usage-dashboard"`), constructs a URL from `RuntimeConf.APIURL`, sends a JSON POST with a hardcoded `X-AUTH-TOKEN`, saves the response body to disk, and returns the HTTP response code. The lack of documentation conceals this overriding behaviour and the hardcoded token from callers.

---

### A104-5 [MEDIUM] HttpDownloadUtility.sendPost — Hardcoded auth token in source with misleading comment

**File:** `util/HttpDownloadUtility.java`, lines 101–105
```java
//add reuqest header
con.setDoOutput(true);
con.setDoInput(true);
con.setRequestMethod("POST");
con.setRequestProperty("X-AUTH-TOKEN", "noCwHkr7lofpFL0ZAL2EzynUBLKN1Krcs8bSunismUE");
```
**Description:** A secret authentication token is hardcoded directly in source. The inline comment `//add reuqest header` (note: misspelled "reuqest") gives no indication that a credential is being embedded, which is misleading by omission. While primarily a security concern, it is raised here as an inaccurate/incomplete comment finding (severity MEDIUM).

---

### A104-6 [LOW] HttpDownloadUtility.getSaveFilePath / setSaveFilePath — Undocumented trivial accessors

**File:** `util/HttpDownloadUtility.java`, lines 186–192
**Description:** `getSaveFilePath()` and `setSaveFilePath(String)` are public static accessors with no Javadoc. As getter/setter equivalents this is LOW severity, but the `static` nature and shared mutable state are noteworthy.

---

### A104-7 [LOW] ImpactUtil — Missing class-level Javadoc

**File:** `util/ImpactUtil.java`, line 5
**Description:** The class `ImpactUtil` has no class-level Javadoc comment. Given the domain-specific nature of the G-force calculations and the significance of the coefficient value, a class-level description is particularly valuable here.

---

### A104-8 [MEDIUM] ImpactUtil.calculateGForceOfImpact — Undocumented non-trivial public method

**File:** `util/ImpactUtil.java`, line 11
```java
public static double calculateGForceOfImpact(long impactValue) {
    return G_FORCE_COEFFICIENT * Math.sqrt(impactValue);
}
```
**Description:** No Javadoc. The method applies the formula `G = 0.00388 * sqrt(impactValue)` to convert a raw sensor reading to G-force. The physical units, the origin of the coefficient, and the expected range of `impactValue` are entirely undocumented.

---

### A104-9 [MEDIUM] ImpactUtil.calculateGForceRequiredForImpact — Undocumented non-trivial public method

**File:** `util/ImpactUtil.java`, line 15
```java
public static double calculateGForceRequiredForImpact(double impactThreshold, ImpactLevel impactLevel) {
```
**Description:** No Javadoc. The method scales `impactThreshold` by an `ImpactLevel`-specific coefficient before applying the G-force formula. The interaction between `impactThreshold`, `ImpactLevel`, and the returned G-force value is non-trivial and completely undocumented.

---

### A104-10 [MEDIUM] ImpactUtil.getCSSColor — Undocumented non-trivial public method

**File:** `util/ImpactUtil.java`, line 32
```java
public static String getCSSColor(ImpactLevel impactLevel) {
```
**Description:** No Javadoc. Returns a CSS colour string for a given `ImpactLevel`. Notable behaviours that should be documented: `AMBER` returns the hex string `"#FFBF00"` (not the word `"amber"`), while `BLUE` and `RED` return their English names. The inconsistency between literal name strings and a hex string is undocumented. Additionally, the method throws `UnhandledImpactLevelException` on an unrecognised level but there is no `@throws` tag.

---

### A104-11 [MEDIUM] ImpactUtil.calculateImpactLevel — Undocumented non-trivial public method; returns null without documentation

**File:** `util/ImpactUtil.java`, line 45
```java
public static ImpactLevel calculateImpactLevel(int impactValue, int impactThreshold) {
```
**Description:** No Javadoc. The method returns `null` when `impactValue` does not exceed `impactThreshold * BLUE_IMPACT_COEFFICIENT` (i.e., no impact level is triggered), but this nullable return is entirely undocumented. Any caller unaware of the null return risks a `NullPointerException`. This is an inaccuracy-by-omission with real correctness risk.

---

### A104-12 [LOW] ImportExcelData — Missing class-level Javadoc

**File:** `util/ImportExcelData.java`, line 27
**Description:** The class `ImportExcelData` has no class-level Javadoc. The class name is slightly misleading because it also handles CSV files (the `read` method uses a comma tokeniser on a plain text file, not an Excel parser), which makes a class-level description especially important.

---

### A104-13 [MEDIUM] ImportExcelData.upload — Undocumented non-trivial public method

**File:** `util/ImportExcelData.java`, line 32
```java
public boolean upload(FormFile formFile) throws ServletException, IOException {
```
**Description:** No Javadoc. The method writes the uploaded file bytes directly to the path held in `savePath`. Important behaviours that are undocumented: (a) the caller must set `savePath` before calling `upload`, otherwise the stream opens against an empty string; (b) the method always returns `true` regardless of whether the write succeeded (exceptions are swallowed by the inner `catch`); (c) `@throws ServletException` and `@throws IOException` are declared but undocumented.

---

### A104-14 [MEDIUM] ImportExcelData.read — Undocumented non-trivial public method; method name is inaccurate

**File:** `util/ImportExcelData.java`, line 47
```java
public List<ArrayList<String>> read(String fileName) throws IOException
```
**Description:** No Javadoc. The class is named `ImportExcelData` and the method is named `read`, but the implementation reads a comma-delimited plain-text file using `BufferedReader` and `StringTokenizer` — not an Excel workbook. Despite the class importing `HSSFWorkbook` and `XSSFWorkbook`, no Excel parsing takes place. The method name and enclosing class name together create a false expectation that Excel (`.xls`/`.xlsx`) files are handled. `@throws IOException` is declared but undocumented.

---

### A104-15 [LOW] ImportExcelData.getSavePath / setSavePath — Undocumented trivial accessors

**File:** `util/ImportExcelData.java`, lines 75–81
**Description:** `getSavePath()` and `setSavePath(String)` are public accessors with no Javadoc. Severity is LOW as they are simple getters/setters, but given the side-effect dependency in `upload()` (see A104-13), brief Javadoc noting this coupling would be beneficial.

---

### A104-16 [MEDIUM] ImportExcelData.checkFileExits — Undocumented method; method name is a typo

**File:** `util/ImportExcelData.java`, line 83
```java
public boolean checkFileExits()
```
**Description:** No Javadoc. Additionally, the method name is misspelled: `checkFileExits` should be `checkFileExists`. This is an inaccurate identifier (the method checks existence, not "exits") that will propagate to every call site.

---

## 3. Summary Table

| ID | Severity | File | Line | Issue |
|---|---|---|---|---|
| A104-1 | LOW | HttpDownloadUtility.java | 21 | No class-level Javadoc |
| A104-2 | MEDIUM | HttpDownloadUtility.java | 29–35 | Javadoc on `downloadFile` missing `@param fileName` |
| A104-3 | MEDIUM | HttpDownloadUtility.java | 25 | Comment claims "Max file size 4MB" — unit wrong (4 KB) and semantics wrong (buffer size, not file size limit) |
| A104-4 | MEDIUM | HttpDownloadUtility.java | 88 | `sendPost` has no Javadoc; non-trivial with hardcoded override of `fileName` |
| A104-5 | MEDIUM | HttpDownloadUtility.java | 105 | Hardcoded auth token with no warning comment; misleading inline comment |
| A104-6 | LOW | HttpDownloadUtility.java | 186–192 | `getSaveFilePath` / `setSaveFilePath` undocumented |
| A104-7 | LOW | ImpactUtil.java | 5 | No class-level Javadoc |
| A104-8 | MEDIUM | ImpactUtil.java | 11 | `calculateGForceOfImpact` undocumented; units and coefficient origin unknown |
| A104-9 | MEDIUM | ImpactUtil.java | 15 | `calculateGForceRequiredForImpact` undocumented |
| A104-10 | MEDIUM | ImpactUtil.java | 32 | `getCSSColor` undocumented; AMBER returns hex, not name; no `@throws` |
| A104-11 | MEDIUM | ImpactUtil.java | 45 | `calculateImpactLevel` undocumented; nullable return undisclosed |
| A104-12 | LOW | ImportExcelData.java | 27 | No class-level Javadoc; class name misleading (reads CSV, not Excel) |
| A104-13 | MEDIUM | ImportExcelData.java | 32 | `upload` undocumented; always returns `true`; requires pre-set `savePath` |
| A104-14 | MEDIUM | ImportExcelData.java | 47 | `read` undocumented; reads CSV despite class/method name implying Excel |
| A104-15 | LOW | ImportExcelData.java | 75–81 | `getSavePath` / `setSavePath` undocumented |
| A104-16 | MEDIUM | ImportExcelData.java | 83 | `checkFileExits` undocumented; method name is a typo (`Exits` vs `Exists`) |

**Total findings: 16**
- HIGH: 0
- MEDIUM: 10
- LOW: 6
