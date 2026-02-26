# Security Audit Report — BarCodeAction & BarCode Utility

**Repository:** forkliftiqadmin
**Branch:** master
**Audit Run:** audit/2026-02-26-01
**Pass:** 1
**Auditor:** CIG Automated Security Audit
**Date:** 2026-02-26
**Files Audited:**
- `src/main/java/com/action/BarCodeAction.java`
- `src/main/java/com/util/BarCode.java`
- `src/main/webapp/WEB-INF/struts-config.xml` (for mapping evidence)
- `src/main/java/com/actionservlet/PreFlightActionServlet.java` (for auth gate evidence)
- `src/main/java/com/util/RuntimeConf.java` (for constant values)

---

## Reading Evidence

### BarCodeAction.java

**Package / Class:** `com.action.BarCodeAction` extends `org.apache.struts.action.Action`

**Methods:** Single `execute()` override; dispatches on the `method` request parameter:

| `method` value (resolved constant) | Constant Name | Resolved Value |
|-------------------------------------|--------------|---------------|
| `"barcode"` | `RuntimeConf.API_BARCODE` | `"barcode"` |
| `"loadbarcode"` | `RuntimeConf.Load_BARCODE` | `"loadbarcode"` |
| anything else | — | forwards to `globalfailure` |

**DAOs / Services called:**
- `UnitDAO.getInstance()` — `getUnitBySerial(serial, true)`, `getUnitById(unit_id)`
- `CompanyDAO.getInstance()` — `getCompanyByCompId(compId)`
- `ResultDAO` (instantiated inline) — `checkDuplicateResult(...)`, (write operations delegated to FleetcheckAction)
- `FleetcheckAction` (instantiated inline) — `saveResult(...)`, `saveResultBarcode(...)`, `sendFleetCheckAlert(...)`

**Form class:** None. The `struts-config.xml` mapping at `/loadbarcode` declares **no `name` attribute** (no ActionForm bound). All input is read directly from `HttpServletRequest.getParameter()` and `getParameterValues()`.

**struts-config.xml mapping (lines 458–461):**
```xml
<action
    path="/loadbarcode"
    type="com.action.BarCodeAction">
    <forward name="success" path="/html-jsp/apiXml.jsp"/>
</action>
```
- No `name` (no form bean), no `validate`, no `scope`.
- Success forward renders `/html-jsp/apiXml.jsp`.

**User-controlled inputs consumed:**
- `method` — dispatch key (line 38)
- `serial` — unit serial number (line 44)
- `driver` — driver identifier, strip-leading-zeros then `Long.parseLong()` (lines 45, 52)
- `quesIds[]` / `quesAns[]` — checklist question IDs and answers (lines 46–47)
- `data` — raw barcode payload string (line 68); parsed with `indexOf`, `substring`, `split` (lines 70–84); individual fields from split tokens feed into DB writes

---

### BarCode.java

**Package / Class:** `com.util.BarCode`

**What it does:**
Generates barcode images from a caller-supplied message string using the Barcode4J library (`org.krysalis.barcode4j`). It supports three output formats determined by the `fmt` request parameter:

| Format | Handling |
|--------|----------|
| `image/svg+xml` | Rendered to `ByteArrayOutputStream` via `SVGCanvasProvider`, serialised via JAXP `Transformer`. Returned as string. |
| `application/postscript` (EPS) | Rendered to `ByteArrayOutputStream` via `EPSCanvasProvider`. Returned as string. |
| Bitmap (default, e.g. PNG) | Written directly to a **file on disk** via `FileOutputStream` (see path traversal finding below). `ByteArrayOutputStream` remains empty; method returns `""`. |

**OS Command Execution:** None. No `Runtime.exec()`, `ProcessBuilder`, or shell invocation anywhere in `BarCode.java`.

**File System Writes:** YES — in the bitmap branch (lines 123–128), a PNG file is written to the server filesystem. The path is constructed as:

```java
String curerntDir = getClass().getProtectionDomain().getCodeSource().getLocation().getPath();
OutputStream out = new java.io.FileOutputStream(
    new File(curerntDir + "/../../../../../images/barcode/" + img + ".png"));
```

where `img` is derived from the caller-supplied `msg` parameter after minimal transformations (strip trailing `#`, strip prefix up to `%`).

**External Library Calls:**
- `org.krysalis.barcode4j` (Barcode4J) — barcode rendering
- `org.apache.avalon.framework.configuration` — configuration tree construction
- JAXP `TransformerFactory` — SVG serialisation
- `org.apache.log4j` — logging

---

## Audit Findings

---

### FINDING 1 — CRITICAL: Unauthenticated Access to Data-Writing Endpoint

**Category:** Authentication
**Severity:** CRITICAL
**File:** `src/main/java/com/actionservlet/PreFlightActionServlet.java`, line 112
**Also:** `src/main/webapp/WEB-INF/struts-config.xml`, lines 458–461

**Description:**
The auth gate `PreFlightActionServlet.excludeFromFilter()` explicitly returns `false` (meaning "skip session check") for `loadbarcode.do`:

```java
else if(path.endsWith("loadbarcode.do")) return false;
```

When `excludeFromFilter` returns `false`, the session / `sessCompId` check is bypassed entirely, and the request proceeds without any authentication. This means any unauthenticated HTTP client — including an anonymous internet user — can invoke both the `barcode` and `loadbarcode` methods of `BarCodeAction`.

**Impact:**
- The `barcode` method (`method=barcode`) accepts a vehicle serial number and driver ID, looks up internal vehicle and company records, saves a pre-ops checklist result to the database, and can trigger email alerts — all without a session.
- The `loadbarcode` method (`method=loadbarcode`) bulk-inserts checklist results parsed from an arbitrary `data` payload.
An attacker can write arbitrary inspection records into the database and trigger alert emails with no credentials.

**Evidence:**
- `PreFlightActionServlet.java` line 112: `else if(path.endsWith("loadbarcode.do")) return false;`
- `struts-config.xml` lines 458–461: mapping has no `name`, `validate`, or any access-control attribute.
- `BarCodeAction.java` line 49: `unitDAO.getUnitBySerial(serial, true)` — DB lookup with unauthenticated `serial`.
- `BarCodeAction.java` line 58: `fleetcheckAction.saveResult(...)` — DB write with unauthenticated input.

**Recommendation:**
Remove `loadbarcode.do` from the exclusion list in `excludeFromFilter()`. This endpoint performs database writes and must require a valid authenticated session (`sessCompId != null`). If the endpoint legitimately needs to be called by barcode-scanner devices that cannot carry a browser session, implement a shared-secret API token scheme (validated in the action itself) rather than bypassing the session gate entirely.

---

### FINDING 2 — CRITICAL: Path Traversal via Unsanitised User Input Used in File Write

**Category:** Path Traversal / Arbitrary File Write
**Severity:** CRITICAL
**File:** `src/main/java/com/util/BarCode.java`, lines 107–124

**Description:**
In the bitmap rendering branch of `genBarCode()`, the `msg` parameter (which originates from caller-supplied request data) is used to construct a filesystem path after only two trivial transformations:

```java
String img = msg;
if (img.endsWith("#")) {
    img = img.substring(0, img.length() - 1);   // strip trailing '#'
}
if (img.contains("$%")) {
    img = img.substring(img.indexOf("%") + 1);   // strip prefix up to '%'
}
if (img.startsWith("%")) {
    img = img.substring(1);                       // strip leading '%'
}

String curerntDir = getClass().getProtectionDomain().getCodeSource().getLocation().getPath();
OutputStream out = new java.io.FileOutputStream(
    new File(curerntDir + "/../../../../../images/barcode/" + img + ".png"));
```

The `img` value is not sanitised for path separator characters (`/`, `\`) or `..` sequences. An attacker supplying a crafted `msg` value such as `../../conf/malicious` could write a file to an arbitrary location on the server filesystem (within the reach of the JVM process's file permissions), for example overwriting web-accessible JSP or config files to achieve Remote Code Execution.

**Note:** `BarCode.genBarCode()` does not appear to be called from `BarCodeAction` in the audited code; however it is a `public` method and could be invoked from other actions or JSPs in the application.

**Evidence:**
- `BarCode.java` line 107: `String img = msg;` — `msg` is caller-supplied.
- `BarCode.java` line 124: `new File(curerntDir + "/../../../../../images/barcode/" + img + ".png")` — `img` concatenated directly into path.
- No `File.getCanonicalPath()` check or path component validation before the `FileOutputStream` is opened.

**Recommendation:**
1. Extract only the filename portion (e.g., `new File(img).getName()`) and reject values containing `/`, `\`, or `..`.
2. Resolve the final path via `File.getCanonicalPath()` and assert it starts with the intended base directory before opening the stream.
3. Restrict the character set of the barcode message used for naming to alphanumeric plus hyphen/underscore (allowlist).

---

### FINDING 3 — HIGH: CSRF — No Token Protection on State-Mutating Endpoint

**Category:** CSRF
**Severity:** HIGH
**File:** `src/main/webapp/WEB-INF/struts-config.xml`, lines 458–461; `src/main/java/com/action/BarCodeAction.java`

**Description:**
The application uses Apache Struts 1.3.10 which has no built-in CSRF token mechanism. The `/loadbarcode.do` endpoint performs database writes (checklist results, driver records) and triggers email alerts. There is no CSRF token generated or validated anywhere in `BarCodeAction.java` or in the struts-config mapping.

Because `loadbarcode.do` is also excluded from the auth gate (Finding 1), CSRF in the traditional sense (requiring a logged-in victim) is less relevant for this specific endpoint. However, for any future state where authentication is restored, the absence of CSRF protection would allow a forged cross-origin request from a malicious page to submit checklist results on behalf of an authenticated user.

**Evidence:**
- No CSRF token parameter referenced in `BarCodeAction.java`.
- `struts-config.xml` mapping has no token-validation interceptor.
- Struts 1.3.10 does not include automatic CSRF protection.

**Recommendation:**
Implement a synchroniser token pattern: generate a per-session token, store it in the session, embed it as a hidden field in all forms (or as a request header for AJAX calls), and validate it at the start of `execute()` before processing any state-mutating operation.

---

### FINDING 4 — HIGH: No Input Validation on `serial`, `driver`, and `data` Parameters

**Category:** Input Validation
**Severity:** HIGH
**File:** `src/main/java/com/action/BarCodeAction.java`, lines 44–46, 52, 68

**Description:**
All request parameters are consumed with no format, length, or content validation:

1. **`serial`** (line 44): Passed directly to `unitDAO.getUnitBySerial(serial, true)`. No length limit, character set restriction, or null guard beyond empty-string coercion. Depending on the DAO implementation, this may allow SQL injection (to be confirmed in a DAO-layer audit pass).

2. **`driver`** (lines 45, 52): The raw string has leading zeros stripped (`replaceFirst("^0*", "")`) then is passed to `Long.parseLong(driverId)` (line 58) without a try/catch in the outer method (only a broader catch in the `loadbarcode` branch). If `driver` is non-numeric the uncaught `NumberFormatException` will propagate through the Struts action layer.

3. **`data`** (line 68): The entire barcode payload string is parsed with `indexOf`, `substring`, and `split` without validating its length. An attacker can submit an arbitrarily large `data` value causing excessive memory allocation during repeated `split("END")` and `split("\r")` operations.

4. **`quesIds[]` / `quesAns[]`** (lines 46–47): Array parameters are passed directly to `saveResult()` with no bounds check or content validation.

**Evidence:**
- `BarCodeAction.java` line 44: `String serial = request.getParameter("serial")==null?"":...` — empty-string coercion only.
- `BarCodeAction.java` line 52: `String driverId = driver.replaceFirst("^0*", "");` — no numeric format check.
- `BarCodeAction.java` line 58: `Long.parseLong(driverId)` — can throw uncaught exception.
- `BarCodeAction.java` line 68: `String data = request.getParameter("data")==null?"":...` — unbounded string accepted.

**Recommendation:**
- Validate `serial` against an expected character set (e.g., `[A-Za-z0-9\-]+`) and a maximum length before DAO calls.
- Validate `driver` is numeric (regex `\d+`) before calling `Long.parseLong()` and wrap in a try/catch with a proper error response.
- Enforce a maximum length on `data` (e.g., 64 KB) and reject oversized payloads before parsing.
- Validate array parameter counts and individual element formats for `quesIds` and `quesAns`.

---

### FINDING 5 — HIGH: Unguarded Array Access Causes Denial of Service / Unhandled Exception

**Category:** Input Validation / Availability
**Severity:** HIGH
**File:** `src/main/java/com/action/BarCodeAction.java`, lines 49–52

**Description:**
In the `API_BARCODE` branch, the code retrieves a list of units and immediately accesses index `[0]` without checking whether the list is empty or null:

```java
ArrayList<UnitBean> arrUnit = unitDAO.getUnitBySerial(serial, true);
String vehId = arrUnit.get(0).getId();        // line 50 — IndexOutOfBoundsException if empty
String compId = arrUnit.get(0).getComp_id();  // line 51
```

If `serial` does not correspond to any unit in the database (e.g., due to a non-existent or crafted serial number), `arrUnit` will be empty and `arrUnit.get(0)` throws `IndexOutOfBoundsException`. This exception is not caught in the `API_BARCODE` branch (there is no try/catch wrapping lines 43–65). The exception propagates to the Struts action layer and will produce an unhandled error response, potentially exposing a stack trace to the caller.

The same pattern recurs at lines 53–55 (`companies.get(0)`).

**Evidence:**
- `BarCodeAction.java` lines 49–51: no null/empty check on `arrUnit` before `.get(0)`.
- `BarCodeAction.java` lines 53–55: no null/empty check on `companies` before `.get(0)`.
- No try/catch block in the `API_BARCODE` branch (lines 43–65).

**Recommendation:**
Check that the returned list is non-null and non-empty before accessing index `[0]`. Return an appropriate error response if the serial number or company is not found. Wrap the branch in a try/catch to prevent stack-trace leakage.

---

### FINDING 6 — HIGH: User-Controlled Input Passed to Barcode Generator Without Sanitisation

**Category:** Input Validation (Barcode Generator Injection)
**Severity:** HIGH
**File:** `src/main/java/com/util/BarCode.java`, lines 67–128

**Description:**
The `msg` parameter passed to `genBarCode()` is forwarded directly to the Barcode4J library's `gen.generateBarcode(provider, msg)` (lines 78, 88, 127) without any sanitisation. While Barcode4J itself does not execute OS commands, the barcode symbology (type) is also caller-controlled via the `type` request parameter (line 165 of `BarCode.java`, fed from `request.getParameter("type")`). An attacker can specify arbitrary barcode types (including types not intended for use by the application), and supply arbitrary content strings, which may trigger unexpected library behaviour, cause library-level exceptions that expose internal paths, or (in older/patched versions of Barcode4J) trigger parsing bugs.

Additionally, for the bitmap path, `msg` is used as a filename (see Finding 2), making the unsanitised value doubly dangerous.

**Evidence:**
- `BarCode.java` line 165: `String type = request.getParameter(BARCODE_TYPE);` — fully attacker-controlled.
- `BarCode.java` line 78: `gen.generateBarcode(svg, msg);` — `msg` passed to library with no validation.
- `BarCode.java` line 127: `gen.generateBarcode(provider, msg);` — same in bitmap path.

**Recommendation:**
- Allowlist accepted barcode types (`code128`, `ean13`, etc.) and reject unknown types.
- Validate and sanitise `msg` to characters valid for the selected barcode symbology before passing it to the library.

---

### FINDING 7 — MEDIUM: Silent Exception Swallowing in `loadbarcode` Branch

**Category:** Error Handling / Defence in Depth
**Severity:** MEDIUM
**File:** `src/main/java/com/action/BarCodeAction.java`, lines 240–244

**Description:**
The entire `Load_BARCODE` processing block (lines 69–244) is wrapped in a broad `catch(Exception e)` that calls `e.getMessage()` (discarding the return value) and `e.printStackTrace()` without setting an appropriate error state or returning an error response to the caller:

```java
} catch(Exception e) {
    e.getMessage();      // return value discarded
    e.printStackTrace(); // stack trace to server stderr only
}
```

After an exception, the method continues to line 251 and forwards to the `success` view, giving the caller no indication that processing failed. This means partial writes may silently occur (some records written, subsequent ones skipped due to exception), and the caller cannot detect or retry correctly.

Additionally, `e.printStackTrace()` writes a full stack trace to server stderr, which may be captured in server logs and expose internal class names, method signatures, and file paths.

**Evidence:**
- `BarCodeAction.java` lines 240–244: bare `catch(Exception e)` with no error forwarding.
- `BarCodeAction.java` line 253: `return mapping.findForward("success")` always reached even after exception.

**Recommendation:**
Set an error flag or message in the request/session, and forward to an error view when an exception occurs. Replace `e.printStackTrace()` with a structured logger call (`log.error(..., e)`). Ensure the caller receives a meaningful error code (e.g., HTTP 500 or an error XML element in the response).

---

### FINDING 8 — MEDIUM: Resolution Parameter Accepted Without Authentication, Integer Parsing Without Bounds on Arbitrary Input

**Category:** Input Validation
**Severity:** MEDIUM
**File:** `src/main/java/com/util/BarCode.java`, lines 91–105

**Description:**
The bitmap resolution parameter `res` is read from the request and parsed as an integer:

```java
String resText = request.getParameter(BARCODE_IMAGE_RESOLUTION);
int resolution = 150;
if (resText != null) {
    resolution = Integer.parseInt(resText);  // no try/catch
}
if (resolution > 2400) { throw new IllegalArgumentException(...); }
if (resolution < 10)   { throw new IllegalArgumentException(...); }
```

`Integer.parseInt(resText)` has no try/catch and will throw `NumberFormatException` for non-integer input (e.g., `res=abc`). Although the bounds checks (10–2400) are present, they are evaluated after the parse, so a non-numeric value bypasses both checks and causes an uncaught exception. The `genBarCode()` caller only catches `Exception` and `Throwable`, so the exception is logged and suppressed, but it also means a very high resolution value (e.g., `res=2399`) that passes the bounds check could trigger excessive memory allocation in the `BitmapCanvasProvider`.

**Evidence:**
- `BarCode.java` line 95: `resolution = Integer.parseInt(resText);` — no try/catch.
- No allowlist for the `res` parameter format.

**Recommendation:**
Wrap `Integer.parseInt(resText)` in a try/catch and return an error if the value is not a valid integer. Consider lowering the maximum resolution limit to a practical value for the application (e.g., 300 dpi) to reduce resource exhaustion risk.

---

### FINDING 9 — MEDIUM: IDOR — Vehicle and Company Data Fetched Using Unauthenticated Caller-Supplied Serial/Unit ID

**Category:** Insecure Direct Object Reference (IDOR)
**Severity:** MEDIUM
**File:** `src/main/java/com/action/BarCodeAction.java`, lines 44, 49–55, 197–198

**Description:**
In both the `barcode` and `loadbarcode` methods, vehicle and company records are fetched using identifiers supplied entirely by the unauthenticated caller. In the `barcode` branch, the `serial` parameter is used to look up any unit in the database; in the `loadbarcode` branch, `unit_id` values parsed from the `data` payload are used to look up units and derive company IDs. There is no verification that the caller has any relationship to (or authority over) the unit or company being accessed.

Combined with the authentication bypass in Finding 1, any external party who knows (or can guess) a valid unit serial number or unit ID can read the associated `compId` and `vehId`, effectively enumerating the customer and vehicle database.

**Evidence:**
- `BarCodeAction.java` line 49: `unitDAO.getUnitBySerial(serial, true)` — serial from unauthenticated request.
- `BarCodeAction.java` line 51: `compId = arrUnit.get(0).getComp_id()` — company ID derived from attacker-controlled serial.
- `BarCodeAction.java` line 197–198: unit and company IDs derived from attacker-controlled `data` payload.

**Recommendation:**
Restore authentication on this endpoint (Finding 1). Once authenticated, verify that the unit identified by `serial` or `unit_id` belongs to the company associated with the session's `sessCompId`. Reject requests where the unit's company does not match the session company.

---

### FINDING 10 — LOW: Hardcoded Internal Email Addresses and URLs in RuntimeConf

**Category:** Data Exposure / Configuration
**Severity:** LOW
**File:** `src/main/java/com/util/RuntimeConf.java`, lines 16, 58, 60

**Description:**
`RuntimeConf.java` contains hardcoded internal email addresses (`hui@ciifm.com`, `hui@collectiveintelligence.com.au`) and an internal AWS EC2 instance URL (`http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/`). These are compiled into the application binary. If the application is decompiled, internal infrastructure details are exposed.

**Evidence:**
- `RuntimeConf.java` line 16: `public static String RECEIVER_EMAIL = "hui@ciifm.com";`
- `RuntimeConf.java` line 58: `public static String debugEmailRecipet = "hui@collectiveintelligence.com.au";`
- `RuntimeConf.java` line 60: `public static String APIURL = "http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/";`

**Recommendation:**
Move configuration values (email addresses, service URLs) to an external properties file or environment variables loaded at startup. Do not hardcode infrastructure addresses in source code.

---

### FINDING 11 — LOW: Stack Trace Printed to Standard Error / Logs

**Category:** Data Exposure
**Severity:** LOW
**File:** `src/main/java/com/util/BarCode.java`, lines 137–140; `src/main/java/com/action/BarCodeAction.java`, line 243

**Description:**
Both files use `e.printStackTrace()` and `t.printStackTrace()` to output stack traces directly to `System.err`. In production environments this can expose internal class names, method signatures, file paths, and library versions to anyone with access to server logs. Structured logging via the already-imported `log4j` Logger should be used instead.

**Evidence:**
- `BarCode.java` lines 137–138: `e.printStackTrace()`, `t.printStackTrace()`.
- `BarCodeAction.java` line 243: `e.printStackTrace()`.

**Recommendation:**
Replace all `e.printStackTrace()` calls with `log.error("Description", e)` using the existing Log4j logger instances.

---

### FINDING 12 — INFO: No ActionForm Bound to /loadbarcode Mapping — Struts Validation Layer Bypassed

**Category:** Input Validation (Structural / Informational)
**Severity:** INFO
**File:** `src/main/webapp/WEB-INF/struts-config.xml`, lines 458–461

**Description:**
The `/loadbarcode` action mapping declares no `name` attribute and therefore no ActionForm. Struts 1's declarative validation framework (via `validation.xml` and the ValidatorPlugIn) only applies to actions that have a form bean bound. All validation for this action must therefore be done entirely in the action's `execute()` method. As documented in Findings 4 and 5, this validation is absent.

This is recorded as INFO to document the structural gap that contributes to the higher-severity findings above.

**Evidence:**
- `struts-config.xml` lines 458–461: no `name` attribute on the `/loadbarcode` action.
- `struts-config.xml` lines 586–590: `ValidatorPlugIn` is configured for the application but cannot apply to form-bean-less actions.

**Recommendation:**
Create an ActionForm subclass for barcode input parameters with declarative validation rules in `validation.xml`, and bind it to the `/loadbarcode` mapping. This ensures the Struts validation layer is engaged before `execute()` is called.

---

## Summary

| # | Severity | Category | Title |
|---|----------|----------|-------|
| 1 | CRITICAL | Authentication | `loadbarcode.do` explicitly excluded from auth gate — fully unauthenticated access |
| 2 | CRITICAL | Path Traversal / Arbitrary File Write | User-supplied `msg` used unsanitised in filesystem path for PNG write |
| 3 | HIGH | CSRF | No CSRF token on state-mutating endpoint |
| 4 | HIGH | Input Validation | No validation on `serial`, `driver`, `data`, `quesIds`, `quesAns` |
| 5 | HIGH | Input Validation / Availability | Unguarded `list.get(0)` — uncaught exception if serial/company not found |
| 6 | HIGH | Input Validation | Unsanitised `msg` and `type` passed to Barcode4J library |
| 7 | MEDIUM | Error Handling | Silent exception swallowing — partial writes, no error response, stack trace to stderr |
| 8 | MEDIUM | Input Validation | `Integer.parseInt` on `res` without try/catch; no non-numeric guard |
| 9 | MEDIUM | IDOR | Vehicle/company data fetched using unauthenticated caller-supplied identifiers |
| 10 | LOW | Data Exposure | Hardcoded internal email addresses and AWS URL in `RuntimeConf.java` |
| 11 | LOW | Data Exposure | `e.printStackTrace()` used instead of structured logger |
| 12 | INFO | Structural | No ActionForm bound — Struts declarative validation bypassed for this action |

**Finding count by severity:**
- CRITICAL: 2
- HIGH: 4
- MEDIUM: 3
- LOW: 2
- INFO: 1
- **Total: 12**
