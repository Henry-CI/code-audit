# Pass 3 – Documentation Audit
**Agent:** A99
**Audit run:** 2026-02-26-01
**Files audited:**
- `src/main/java/com/report/FleetCheckAlert.java`
- `src/main/java/com/report/PreFlightReport.java`
- `src/main/java/com/report/ReportAPI.java`

---

## 1. Reading Evidence

### 1.1 FleetCheckAlert.java

**Class:** `FleetCheckAlert` — line 17
Extends: `PreFlightReport`

**Fields:**
| Name | Type | Line |
|------|------|------|
| `log` | `static Logger` | 18 |

**Methods:**
| Method | Visibility | Line |
|--------|-----------|------|
| `FleetCheckAlert(PropertyMessageResources p)` | public | 21 |
| `FleetCheckAlert()` | public | 26 |
| `getLogo(String compId)` | public | 42 |
| `appendHtmlAlertCotent(String compId)` | public | 58 |
| `setContent(int resultId)` | public | 80 |

Commented-out (dead) methods (not audited for documentation):
- `getLindeLogo(String compId)` (lines 31-40)
- `appendHtmlAlertCotentLinde(String compId)` (lines 69-78)
- `setLindeContent(int resultId)` (lines 170-225)

---

### 1.2 PreFlightReport.java

**Class:** `PreFlightReport` — line 16

**Fields:**
| Name | Type | Line |
|------|------|------|
| `subject` | `protected String` | 17 |
| `title` | `protected String` | 18 |
| `eDate` | `protected Date` | 19 |
| `sDate` | `protected Date` | 20 |
| `frequency` | `protected String` | 21 |
| `content` | `protected String` | 22 |
| `sEmail` | `protected String` | 23 |
| `rEmail` | `protected String` | 24 |
| `htmlCotent` | `protected String` | 25 |
| `pm` | `PropertyMessageResources` (package-private) | 26 |

**Methods:**
| Method | Visibility | Line |
|--------|-----------|------|
| `PreFlightReport()` | public | 29 |
| `PreFlightReport(PropertyMessageResources p)` | public | 35 |
| `PreFlightReport(Date eDate, String frequency, PropertyMessageResources p)` | public | 40 |
| `getPm()` | public | 49 |
| `setPm(PropertyMessageResources pm)` | public | 53 |
| `getHtmlCotent()` | public | 57 |
| `setHtmlCotent(String htmlCotent)` | public | 61 |
| `appendHtmlCotent()` | public | 65 |
| `appendHtmlAlertCotent()` | public | 77 |
| `getTitle()` | public | 89 |
| `setTitle(String title)` | public | 92 |
| `getSubject()` | public | 95 |
| `setSubject(String subject)` | public | 98 |
| `getContent()` | public | 101 |
| `setContent(String compId)` | public | 105 |
| `getFrequency()` | public | 110 |
| `setFrequency(String frequency)` | public | 113 |
| `getsEmail()` | public | 116 |
| `setsEmail(String sEmail)` | public | 119 |
| `getrEmail()` | public | 122 |
| `setrEmail(String rEmail)` | public | 125 |
| `geteDate()` | public | 128 |
| `seteDate(Date eDate)` | public | 131 |
| `getsDate()` | public | 134 |
| `setsDate(Date sDate)` | public | 137 |
| `caculatesDate()` | public | 141 |
| `getDriverName(Long driverId)` | public | 146 |
| `getUnitName(String unitId)` | public | 159 |

---

### 1.3 ReportAPI.java

**Class:** `ReportAPI` — line 10

**Fields:**
| Name | Type | Line |
|------|------|------|
| `subject` | `protected String` | 11 |
| `title` | `protected String` | 12 |
| `content` | `protected String` | 14 |
| `sEmail` | `protected String` | 15 |
| `rEmail` | `protected String` | 16 |
| `fileURL` | `protected String` | 17 |
| `name` | `protected String` | 18 |
| `input` | `protected String` | 19 |
| `responseCode` | `protected int` | 20 |

**Methods:**
| Method | Visibility | Line |
|--------|-----------|------|
| `getResponseCode()` | public | 22 |
| `setResponseCode(int responseCode)` | public | 26 |
| `ReportAPI(String name, String input)` | public | 30 |
| `downloadPDF()` | public | 38 |
| `getExportDir(String dirctory)` | protected | 46 |
| `getSubject()` | public | 51 |
| `setSubject(String subject)` | public | 55 |
| `getTitle()` | public | 59 |
| `setTitle(String title)` | public | 63 |
| `getContent()` | public | 68 |
| `setContent(String content)` | public | 72 |
| `getsEmail()` | public | 76 |
| `setsEmail(String sEmail)` | public | 80 |
| `getrEmail()` | public | 84 |
| `setrEmail(String rEmail)` | public | 88 |
| `getFileURL()` | public | 92 |
| `setFileURL(String fileURL)` | public | 96 |
| `getName()` | public | 100 |
| `setName(String name)` | public | 104 |

---

## 2. Findings

### A99-1 [LOW] — FleetCheckAlert: No class-level Javadoc

**File:** `FleetCheckAlert.java`, line 17
**Observation:** The class declaration has no `/** ... */` Javadoc comment. There is no description of the class's purpose (fleet-check alert email generation), its relationship to `PreFlightReport`, or its overall contract.
```java
public class FleetCheckAlert extends PreFlightReport{
```

---

### A99-2 [MEDIUM] — FleetCheckAlert.getLogo: Undocumented non-trivial public method

**File:** `FleetCheckAlert.java`, lines 42-56
**Observation:** No Javadoc present. The method is non-trivial: it retrieves a company logo via DAO, falls back to `"logo_email.png"` when the logo equals `RuntimeConf.EMPTYLOGO`, and falls back again to `"banner.jpg"` when the logo is an empty string. These two fallback conditions and their semantic difference are not documented.
```java
public String getLogo(String compId) throws Exception
```

---

### A99-3 [MEDIUM] — FleetCheckAlert.appendHtmlAlertCotent(String): Undocumented non-trivial public method

**File:** `FleetCheckAlert.java`, lines 58-67
**Observation:** No Javadoc present. This method overrides the company-logo-agnostic `appendHtmlAlertCotent()` in the parent class by accepting a `compId` parameter to resolve a company-specific logo. The side effect of mutating `this.htmlCotent` is not described, nor is the difference from the parent-class method.
```java
public void appendHtmlAlertCotent(String compId) throws Exception {
```

---

### A99-4 [MEDIUM] — FleetCheckAlert.setContent(int): Undocumented non-trivial public method

**File:** `FleetCheckAlert.java`, lines 80-168
**Observation:** No Javadoc present. This is a substantive method: it queries `ResultDAO` for checklist results by ID, conditionally renders location and odometer columns based on the first row's data, evaluates result status (including an INCOMPLETE guard), appends failure descriptions and comments, checks scanner time validity, and returns a count of processed records. All of this behaviour, its side effect on `this.content`, and the meaning of the return value are undocumented.
```java
public int setContent(int resultId){
```

---

### A99-5 [MEDIUM] — FleetCheckAlert.setContent(int): Logic bug in odometer column guard is misleading relative to column header guard

**File:** `FleetCheckAlert.java`, lines 100-103 vs. lines 151-154
**Observation:** The column header is conditionally included when `odemeter != "0"` (line 100), but the per-row cell is conditionally included when `location != "0"` (line 151). The row-level guard tests the wrong field (`location` instead of `odemeter`). Because the column header and the data cell use different guard conditions, rows can render an extra `<td>` even when the header was not emitted (or vice versa), breaking the HTML table structure. No comment explains this discrepancy; a reader of the code would assume consistency. This is a substantive inaccuracy between the apparent intent (guard on odometer) and actual behaviour (guard on location).

**Severity upgrade to MEDIUM** (inaccurate/misleading logic rather than merely missing docs).

```java
// Header guard (line 100-103): correct field
if(!arrResult.get(0).getOdemeter().equalsIgnoreCase("0"))
{
    html += "<th>"+pm.getMessage("report.odemeter")+"</th>";
}

// Row guard (line 151-154): WRONG field — tests location, not odemeter
if(!location.equalsIgnoreCase("0"))
{
    html +="<td>"+odemeter+"</td>";
}
```

---

### A99-6 [LOW] — FleetCheckAlert constructors: No Javadoc

**File:** `FleetCheckAlert.java`, lines 21-28
**Observation:** Both public constructors lack Javadoc. The single-argument constructor's purpose (accepting a `PropertyMessageResources` for i18n) is not explained. Trivial delegation, but constructors with parameters are not purely getters/setters.

---

### A99-7 [LOW] — PreFlightReport: No class-level Javadoc

**File:** `PreFlightReport.java`, line 16
**Observation:** The class has no `/** ... */` Javadoc. The purpose (base class for pre-flight/checklist report generation including HTML content assembly, email addressing, and date-range calculation) is entirely undocumented.
```java
public class PreFlightReport {
```

---

### A99-8 [LOW] — PreFlightReport constructors: No Javadoc

**File:** `PreFlightReport.java`, lines 29-46
**Observation:** All three public constructors lack Javadoc. The three-argument constructor is non-trivial: it sets `eDate` and `frequency`, then calls `caculatesDate()` as a side effect before setting `pm`. The side-effect call to `caculatesDate()` is invisible to a caller without reading the body.

---

### A99-9 [MEDIUM] — PreFlightReport.appendHtmlCotent: Undocumented non-trivial public method

**File:** `PreFlightReport.java`, lines 65-75
**Observation:** No Javadoc present. The method constructs a full HTML email body (including an inline CSS fetch from localhost, a header table with banner image, report name, start date, and end date), appends `this.content`, and stores the result in `this.htmlCotent`. The side effect on `this.htmlCotent`, the dependency on `this.sDate`, `this.eDate`, `this.title`, and the localhost CSS URL are all undocumented.
```java
public void appendHtmlCotent() {
```

---

### A99-10 [MEDIUM] — PreFlightReport.appendHtmlAlertCotent(): Undocumented non-trivial public method

**File:** `PreFlightReport.java`, lines 77-86
**Observation:** No Javadoc present. Constructs an alert-variant HTML email body using a fixed `banner.jpg` image (no company-specific logo), assembles header and footer around `this.content`, and stores to `this.htmlCotent`. The distinction from `appendHtmlCotent()` (no date range, no UTF-8 meta tag, no width style, fixed banner) is not documented.
```java
public void appendHtmlAlertCotent() {
```

---

### A99-11 [MEDIUM] — PreFlightReport.setContent(String): Undocumented non-trivial public method

**File:** `PreFlightReport.java`, lines 105-108
**Observation:** No Javadoc present. The method signature accepts a `compId` parameter but the body ignores it entirely and always returns 0. This is a stub/placeholder for subclass overriding. Without documentation, callers cannot know this is intentionally a no-op base implementation, nor that the parameter is unused.
```java
public int setContent(String compId) {
    int count = 0;
    return count;
}
```

---

### A99-12 [MEDIUM] — PreFlightReport.caculatesDate: Undocumented non-trivial public method (and misspelled name)

**File:** `PreFlightReport.java`, lines 141-144
**Observation:** No Javadoc present. The method computes `sDate` from `eDate` and `frequency` via `DateUtil.getStartDate`. The method name is misspelled (`caculatesDate` instead of `calculatesDate`). Without Javadoc, the precondition that both `eDate` and `frequency` must be set before calling, and the side effect of mutating `sDate`, are invisible to callers.
```java
public void caculatesDate()
{
    this.sDate = DateUtil.getStartDate(this.eDate,this.frequency);
}
```

---

### A99-13 [MEDIUM] — PreFlightReport.getDriverName: Undocumented non-trivial public method

**File:** `PreFlightReport.java`, lines 146-150
**Observation:** No Javadoc present. The method delegates to a DAO singleton. Notable behaviour: if `driverId` maps to no driver the return value's contract (empty string? null? exception?) is undocumented. The `throws Exception` declaration is also unexplained.
```java
public String getDriverName(Long driverId) throws Exception
```

---

### A99-14 [MEDIUM] — PreFlightReport.getUnitName: Undocumented non-trivial public method

**File:** `PreFlightReport.java`, lines 159-163
**Observation:** No Javadoc present. The method calls `UnitDAO.getInstance().getUnitById(unitId).get(0).getName()`. A double trailing semicolon on line 161 indicates copy-paste sloppiness. The method will throw `IndexOutOfBoundsException` if no unit is found (list is empty), but this is not documented. The `throws Exception` is unexplained.
```java
public String getUnitName(String unitId) throws Exception
{
    String unitName = UnitDAO.getInstance().getUnitById(unitId).get(0).getName();;
    return unitName;
}
```

---

### A99-15 [LOW] — PreFlightReport: All getters/setters lack Javadoc

**File:** `PreFlightReport.java`, lines 49-139 (multiple)
**Observation:** The following getter/setter pairs lack Javadoc. Per severity rules these are LOW as trivial accessors, but they are noted for completeness:
`getPm`/`setPm`, `getHtmlCotent`/`setHtmlCotent`, `getTitle`/`setTitle`, `getSubject`/`setSubject`, `getContent`, `getFrequency`/`setFrequency`, `getsEmail`/`setsEmail`, `getrEmail`/`setrEmail`, `geteDate`/`seteDate`, `getsDate`/`setsDate`.

Note: the field `htmlCotent` (line 25) is itself a misspelling of `htmlContent`; the misspelling is propagated into the getter/setter names.

---

### A99-16 [LOW] — ReportAPI: No class-level Javadoc

**File:** `ReportAPI.java`, line 10
**Observation:** The class has no `/** ... */` Javadoc. The purpose (wrapper that fetches a PDF report from an external API endpoint, stores it locally, and supports email dispatch) is entirely undocumented.
```java
public class ReportAPI {
```

---

### A99-17 [LOW] — ReportAPI constructor: No Javadoc

**File:** `ReportAPI.java`, lines 30-35
**Observation:** The public constructor takes `name` and `input` parameters with no Javadoc explaining their semantics. The `name` field comment on line 18 says "report name", but `input` has no inline comment and no Javadoc clarifying what it represents (appears to be POST body payload for the API call).
```java
public ReportAPI(String name,String input)
```

---

### A99-18 [LOW] — ReportAPI.downloadPDF: Existing comment is a block comment, not Javadoc; missing @return/@throws

**File:** `ReportAPI.java`, lines 37-43
**Observation:** A `/* ... */` block comment exists above `downloadPDF()` (line 37), but it is NOT a Javadoc comment (missing the leading `/**`). It will not be picked up by Javadoc tooling. Additionally, the comment text "Read the pdf file from API, store locally, send email" is partially inaccurate: the method itself does not send email — it only downloads the file and returns the path. Email dispatch must be performed separately by the caller. There is no `@return` documenting the returned file path, and no `@throws` for the declared `Exception`.

```java
/*Read the pdf file from API, store locally, send email */
public String downloadPDF() throws Exception
```

**Inaccuracy detail:** The phrase "send email" implies this method sends email, which it does not. Severity is MEDIUM for the inaccuracy (rather than just missing docs).

---

### A99-19 [LOW] — ReportAPI.getExportDir: Protected non-trivial method undocumented; misspelled parameter name

**File:** `ReportAPI.java`, lines 46-49
**Observation:** The method is `protected` (not public) so severity is LOW, but it is non-trivial for subclassers: it ignores its `dirctory` parameter entirely and always returns `java.io.tmpdir`. This is clearly a stub intended for override, but neither the override contract nor the ignored parameter are documented. The parameter name is also misspelled (`dirctory` instead of `directory`).
```java
protected String getExportDir(String dirctory) throws Exception
{
    return System.getProperty("java.io.tmpdir");
}
```

---

### A99-20 [LOW] — ReportAPI: All getters/setters lack Javadoc

**File:** `ReportAPI.java`, lines 22-108 (multiple)
**Observation:** The following getter/setter pairs lack Javadoc. Per severity rules these are LOW as trivial accessors:
`getResponseCode`/`setResponseCode`, `getSubject`/`setSubject`, `getTitle`/`setTitle`, `getContent`/`setContent`, `getsEmail`/`setsEmail`, `getrEmail`/`setrEmail`, `getFileURL`/`setFileURL`, `getName`/`setName`.

---

## 3. Summary Table

| ID | File | Location | Severity | Description |
|----|------|----------|----------|-------------|
| A99-1 | FleetCheckAlert.java | line 17 | LOW | No class-level Javadoc |
| A99-2 | FleetCheckAlert.java | line 42 | MEDIUM | `getLogo` undocumented non-trivial public method |
| A99-3 | FleetCheckAlert.java | line 58 | MEDIUM | `appendHtmlAlertCotent(String)` undocumented non-trivial public method |
| A99-4 | FleetCheckAlert.java | line 80 | MEDIUM | `setContent(int)` undocumented non-trivial public method |
| A99-5 | FleetCheckAlert.java | lines 100-154 | MEDIUM | Odometer column row-guard tests wrong field (`location` instead of `odemeter`); inaccurate/misleading logic |
| A99-6 | FleetCheckAlert.java | lines 21-28 | LOW | Public constructors lack Javadoc |
| A99-7 | PreFlightReport.java | line 16 | LOW | No class-level Javadoc |
| A99-8 | PreFlightReport.java | lines 29-46 | LOW | Public constructors lack Javadoc; 3-arg constructor has undocumented side effect |
| A99-9 | PreFlightReport.java | line 65 | MEDIUM | `appendHtmlCotent` undocumented non-trivial public method |
| A99-10 | PreFlightReport.java | line 77 | MEDIUM | `appendHtmlAlertCotent()` undocumented non-trivial public method |
| A99-11 | PreFlightReport.java | line 105 | MEDIUM | `setContent(String)` stub with ignored parameter; undocumented no-op base behaviour |
| A99-12 | PreFlightReport.java | line 141 | MEDIUM | `caculatesDate` undocumented; misspelled method name; undocumented preconditions and side effect |
| A99-13 | PreFlightReport.java | line 146 | MEDIUM | `getDriverName` undocumented; return contract and exception undocumented |
| A99-14 | PreFlightReport.java | line 159 | MEDIUM | `getUnitName` undocumented; silent `IndexOutOfBoundsException` risk; double semicolon |
| A99-15 | PreFlightReport.java | lines 49-139 | LOW | All getters/setters lack Javadoc; `htmlCotent` misspelling propagated into accessor names |
| A99-16 | ReportAPI.java | line 10 | LOW | No class-level Javadoc |
| A99-17 | ReportAPI.java | line 30 | LOW | Constructor lacks Javadoc; `input` parameter semantics undocumented |
| A99-18 | ReportAPI.java | lines 37-43 | MEDIUM | `downloadPDF` uses `/* */` not `/** */`; comment claims "send email" which is inaccurate; missing `@return`/`@throws` |
| A99-19 | ReportAPI.java | lines 46-49 | LOW | `getExportDir` ignores its parameter silently; no override contract; parameter name misspelled |
| A99-20 | ReportAPI.java | lines 22-108 | LOW | All getters/setters lack Javadoc |

**Totals:** 20 findings — 9 MEDIUM, 11 LOW, 0 HIGH
