# Pass 3 Documentation Audit — Agent A87
**Audit Run:** 2026-02-26-01
**Files Assigned:**
- `com/pdf/FleetCheckPDF.java`
- `com/pdf/PreStartPDF.java`

---

## 1. Reading Evidence

### 1.1 FleetCheckPDF.java

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/pdf/FleetCheckPDF.java`

**Class declaration:**
- `FleetCheckPDF` (line 28) — extends `PreStartPDF`

**Fields:**

| Field | Type | Line |
|-------|------|------|
| `log` | `static Logger` | 29 |
| `pdfurl` | `String` | 30 |
| `unitDAO` | `UnitDAO` | 31 |
| `driverDao` | `DriverDAO` | 32 |

**Methods:**

| Method | Visibility | Line |
|--------|-----------|------|
| `FleetCheckPDF(String compId, Date from, Date to, String docRoot)` | `public` (constructor) | 34 |
| `createTable(Document document)` | `public` | 47 |

---

### 1.2 PreStartPDF.java

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/pdf/PreStartPDF.java`

**Class declaration:**
- `PreStartPDF` (line 28)

**Fields:**

| Field | Type | Line |
|-------|------|------|
| `result` | `protected String` | 29 |
| `title` | `protected String` | 30 |
| `image` | `protected String` | 31 |
| `from` | `protected Date` | 32 |
| `to` | `protected Date` | 33 |
| `compId` | `protected String` | 34 |
| `catFont` | `protected static Font` | 35 |
| `redFont` | `protected static Font` | 36 |
| `subFont` | `protected static Font` | 37 |
| `hrFont` | `protected static Font` | 38 |
| `hdFont` | `protected static Font` | 39 |
| `smallBold` | `protected static Font` | 40 |

**Methods:**

| Method | Visibility | Line |
|--------|-----------|------|
| `PreStartPDF(String compId, Date from, Date to)` | `public` (constructor) | 42 |
| `createPdf()` | `public` | 54 |
| `addContent(Document document)` | `private` | 68 |
| `createTable(Document document)` | `public` | 77 |
| `addMetaData(Document document)` | `private` | 98 |
| `addTitlePage(Document document)` | `private` | 105 |
| `addFooter(Document document)` | `private` | 116 |
| `createList(Section subCatPart)` | `private` | 125 |
| `addEmptyLine(Paragraph paragraph, int number)` | `private` | 133 |
| `addImage(Document document)` | `private` | 139 |
| `getImage()` | `public` | 149 |
| `setImage(String image)` | `public` | 153 |
| `getResult()` | `public` | 157 |
| `setResult(String result)` | `public` | 161 |
| `getTitle()` | `public` | 165 |
| `setTitle(String title)` | `public` | 169 |
| `getFrom()` | `public` | 173 |
| `setFrom(Date from)` | `public` | 177 |
| `getTo()` | `public` | 181 |
| `setTo(Date to)` | `public` | 185 |

---

## 2. Findings

### A87-1 [LOW] — FleetCheckPDF: No class-level Javadoc

**File:** `FleetCheckPDF.java`, line 28
**Severity:** LOW

The class `FleetCheckPDF` has no class-level Javadoc comment. There is no `/** ... */` block above the `public class FleetCheckPDF` declaration.

```java
// line 28 — no preceding /** */ block
public class FleetCheckPDF extends PreStartPDF {
```

---

### A87-2 [MEDIUM] — FleetCheckPDF.createTable: Javadoc `@return` tag is inaccurate (method returns void)

**File:** `FleetCheckPDF.java`, lines 41–47
**Severity:** MEDIUM

The Javadoc on `createTable` declares `@return our first table`, but the method signature is `public void createTable(Document document)` — it returns nothing. The return value annotation is incorrect and misleading. Additionally, the `@param document` parameter is not documented at all.

```java
/**
 * Creates our first table
 *
 * @return our first table          // WRONG: method is void
 * @throws DocumentException
 */
public void createTable(Document document) throws DocumentException {
```

---

### A87-3 [LOW] — FleetCheckPDF.createTable: Missing `@param` for `document` parameter

**File:** `FleetCheckPDF.java`, lines 41–47
**Severity:** LOW

The existing Javadoc block on `createTable` omits a `@param document` tag for the `Document document` parameter.

---

### A87-4 [MEDIUM] — FleetCheckPDF constructor: Undocumented non-trivial public constructor

**File:** `FleetCheckPDF.java`, lines 34–39
**Severity:** MEDIUM

The public constructor `FleetCheckPDF(String compId, Date from, Date to, String docRoot)` has no Javadoc. The constructor performs non-trivial work: it calls the superclass constructor, sets the report title, constructs a dynamic file path for the PDF output using a random name, and constructs the banner image path. None of this behaviour is documented.

```java
// lines 34–39 — no preceding /** */ block
public FleetCheckPDF(String compId, Date from, Date to, String docRoot) {
    super(compId, from, to);
    setTitle("FleetCheck Report");
    setResult(docRoot + RuntimeConf.PDF_FOLDER + Util.generateRadomName() + ".pdf");
    setImage(docRoot + "/" + RuntimeConf.IMG_SRC + "/banner.jpg");
}
```

---

### A87-5 [LOW] — PreStartPDF: No class-level Javadoc

**File:** `PreStartPDF.java`, line 28
**Severity:** LOW

The class `PreStartPDF` has no class-level Javadoc comment. There is no `/** ... */` block above the `public class PreStartPDF` declaration.

```java
// line 28 — no preceding /** */ block
public class PreStartPDF {
```

---

### A87-6 [MEDIUM] — PreStartPDF.createPdf: Javadoc `@param` is inaccurate (describes a non-existent parameter)

**File:** `PreStartPDF.java`, lines 48–54
**Severity:** MEDIUM

The Javadoc on `createPdf()` contains `@param filename the name of the PDF file that will be created.` However, the method signature is `public String createPdf()` — it takes no parameters. The `@param` tag refers to a parameter that does not exist. The PDF file name/path is derived from the instance field `result`, not from any method parameter. The tag is therefore factually wrong.

```java
/**
 * Creates a PDF with information about the movies
 * @param    filename the name of the PDF file that will be created.   // WRONG: no such parameter
 * @throws    DocumentException
 * @throws    IOException
 */
public String createPdf()
    throws IOException, DocumentException {
```

---

### A87-7 [LOW] — PreStartPDF.createPdf: Missing `@return` tag

**File:** `PreStartPDF.java`, lines 48–54
**Severity:** LOW

The Javadoc on `createPdf()` does not include a `@return` tag. The method returns `String` (the path of the generated PDF file, stored in `result`).

---

### A87-8 [MEDIUM] — PreStartPDF.createTable: Javadoc `@return` tag is inaccurate (method returns void)

**File:** `PreStartPDF.java`, lines 72–77
**Severity:** MEDIUM

The Javadoc on `PreStartPDF.createTable` declares `@return our first table`, but the method signature is `public void createTable(Document document)` — it returns nothing. The return value annotation is incorrect. Additionally, the `@param document` parameter is not documented.

```java
/**
 * Creates our first table
 * @return our first table          // WRONG: method is void
 * @throws DocumentException
 */
public  void createTable(Document document) throws DocumentException {
```

---

### A87-9 [LOW] — PreStartPDF.createTable: Missing `@param` for `document` parameter

**File:** `PreStartPDF.java`, lines 72–77
**Severity:** LOW

The existing Javadoc block on `PreStartPDF.createTable` omits a `@param document` tag for the `Document document` parameter.

---

### A87-10 [LOW] — PreStartPDF constructor: Undocumented non-trivial public constructor

**File:** `PreStartPDF.java`, lines 42–46
**Severity:** LOW (borderline MEDIUM — constructor is simple but sets three state fields used throughout)

The public constructor `PreStartPDF(String compId, Date from, Date to)` has no Javadoc. It initialises the three core state fields (`compId`, `from`, `to`) that govern all subsequent PDF generation. No documentation is provided for any parameter.

```java
// lines 42–46 — no preceding /** */ block
public PreStartPDF(String compId, Date from, Date to){
    this.compId = compId;
    this.from = from;
    this.to = to;
}
```

---

### A87-11 [LOW] — PreStartPDF: All public getter/setter methods are undocumented

**File:** `PreStartPDF.java`, lines 149–187
**Severity:** LOW (per finding-severity rules: undocumented trivial getter/setter)

The following ten public accessor methods have no Javadoc:

| Method | Line |
|--------|------|
| `getImage()` | 149 |
| `setImage(String image)` | 153 |
| `getResult()` | 157 |
| `setResult(String result)` | 161 |
| `getTitle()` | 165 |
| `setTitle(String title)` | 169 |
| `getFrom()` | 173 |
| `setFrom(Date from)` | 177 |
| `getTo()` | 181 |
| `setTo(Date to)` | 185 |

---

## 3. Additional Code-Quality Observations (non-documentation)

These items are noted for completeness but are outside the documentation-audit scope and carry no finding ID:

- **FleetCheckPDF.java line 58:** Column header is spelled `"Vehcile"` (should be `"Vehicle"`).
- **FleetCheckPDF.java line 127:** Misspelled string literal `"*Safty Check incomplete"` (should be `"Safety"`).
- **FleetCheckPDF.java line 160–164:** `emptyflag` logic is inverted — it is set `false` when no drivers are found (correctly showing the "No Driver" message), but the subsequent check `if (emptyflag)` would then add an additional "No Fleetcheck" row unconditionally when there are no drivers, whereas it is only cleared to `false` in that branch. The logic produces a spurious second empty-row message when no drivers are registered.
- **PreStartPDF.java line 118:** The Unicode escape `\\u00A9` in a regular string literal will not produce a copyright symbol at runtime; the literal backslash-u sequence is printed verbatim rather than being interpreted as the Unicode character U+00A9.
- **PreStartPDF.java lines 125–131:** `createList(Section subCatPart)` is a private method that is never called anywhere in the class. It appears to be dead/scaffold code.

---

## 4. Summary Table

| ID | Severity | File | Location | Description |
|----|----------|------|----------|-------------|
| A87-1 | LOW | FleetCheckPDF.java | line 28 | No class-level Javadoc |
| A87-2 | MEDIUM | FleetCheckPDF.java | lines 41–47 | `@return` tag inaccurate — method is `void` |
| A87-3 | LOW | FleetCheckPDF.java | lines 41–47 | Missing `@param document` in Javadoc |
| A87-4 | MEDIUM | FleetCheckPDF.java | lines 34–39 | Public constructor undocumented (non-trivial) |
| A87-5 | LOW | PreStartPDF.java | line 28 | No class-level Javadoc |
| A87-6 | MEDIUM | PreStartPDF.java | lines 48–54 | `@param filename` does not correspond to any real parameter |
| A87-7 | LOW | PreStartPDF.java | lines 48–54 | Missing `@return` tag on `createPdf()` |
| A87-8 | MEDIUM | PreStartPDF.java | lines 72–77 | `@return` tag inaccurate — method is `void` |
| A87-9 | LOW | PreStartPDF.java | lines 72–77 | Missing `@param document` in Javadoc |
| A87-10 | LOW | PreStartPDF.java | lines 42–46 | Public constructor undocumented |
| A87-11 | LOW | PreStartPDF.java | lines 149–187 | Ten public getters/setters undocumented |
