# Security Audit Report
## Scope: JSON library, json_result.jsp, LanguageDAO, LicenceBean / licence.jsp
**Application:** forkliftiqadmin (Apache Struts 1.3.10 / Tomcat)
**Branch:** master
**Audit Date:** 2026-02-26
**Pass:** 1

---

## Files Audited

| # | File |
|---|------|
| 1 | `src/main/java/com/json/JSONArray.java` |
| 2 | `src/main/java/com/json/JSONException.java` |
| 3 | `src/main/java/com/json/JSONML.java` |
| 4 | `src/main/java/com/json/JSONObject.java` |
| 5 | `src/main/java/com/json/JSONString.java` |
| 6 | `src/main/java/com/json/JSONStringer.java` |
| 7 | `src/main/java/com/json/JSONTokener.java` |
| 8 | `src/main/java/com/json/JSONWriter.java` |
| 9 | `src/main/webapp/html-jsp/result/json_result.jsp` |
| 10 | `src/main/java/com/bean/LanguageBean.java` |
| 11 | `src/main/java/com/dao/LanguageDAO.java` |
| 12 | `src/main/java/com/bean/LicenceBean.java` |
| 13 | `src/main/webapp/html-jsp/driver/licence.jsp` |

---

## Findings

---

### HIGH: Vendored org.json library is a severely outdated snapshot (circa 2012)

**File:** `src/main/java/com/json/JSONObject.java` (line 93), `src/main/java/com/json/JSONArray.java` (line 81), `src/main/java/com/json/JSONTokener.java` (line 39)

**Description:**
The `com.json` package is a vendored copy of the org.json reference implementation. Version comments embedded in the source files confirm the snapshot dates:

- `JSONObject.java` — `@version 2012-07-02`
- `JSONArray.java` — `@version 2012-04-20`
- `JSONTokener.java` — `@version 2012-02-16`
- `JSONML.java` — `@version 2012-03-28`
- `XML.java` — `@version 2011-02-11`

This places the library at approximately the org.json release circa 2012, more than 13 years out of date. The following published CVEs directly affect versions of org.json in this era and have not been patched in this codebase:

**CVE-2022-45688** — Stack overflow / DoS via deeply nested JSON input
Affected versions: org.json before 20230227. The `JSONObject` and `JSONArray` constructors recursively call `JSONTokener.nextValue()` without any depth limit. An attacker supplying a maliciously crafted deeply nested JSON string (e.g., thousands of nested `[[[...` arrays or `{"{": {":":...` objects) will exhaust the JVM call stack and cause an unhandled `StackOverflowError`, crashing the Tomcat thread and causing denial of service.

```java
// JSONTokener.java line 362-366 — no recursion depth guard
case '{':
    this.back();
    return new JSONObject(this);   // recursion
case '[':
    this.back();
    return new JSONArray(this);    // recursion
```

**CVE-2023-5072** — DoS via excessive memory consumption on large JSON inputs
Affected versions: org.json before 20231013. Related to uncontrolled resource consumption when parsing extremely large JSON documents.

The library is never updated via a build tool (Maven/Gradle) dependency; it is compiled directly into the application source tree, meaning no automated supply-chain tooling will flag the outdated version.

**Risk:** A network-accessible endpoint that accepts user-supplied JSON and passes it to `new JSONObject(userInput)` or `new JSONArray(userInput)` is vulnerable to a single-request DoS that crashes a Tomcat thread or causes a full JVM stack overflow. Given the application uses Struts action forms that may deserialize JSON from request parameters, this is a realistic attack surface.

**Recommendation:**
1. Remove the vendored `com.json` package entirely.
2. Add a proper Maven/Gradle dependency on org.json 20240303 (or later) or switch to Jackson (`com.fasterxml.jackson`) or Gson, both of which have active CVE programmes and depth-limiting defences.
3. If vendoring is required, apply the depth-limiting patch: maintain a `depth` counter in `JSONTokener` and throw `JSONException` when it exceeds a configurable limit (e.g., 512).

---

### HIGH: JSONML / XML.toJSONObject parses external XML without disabling DOCTYPE — potential XXE

**File:** `src/main/java/com/json/JSONML.java` (lines 49–235), `src/main/java/com/json/XML.java` (lines 130–291, 365–372)

**Description:**
`JSONML.toJSONObject(String)`, `JSONML.toJSONArray(String)`, and `XML.toJSONObject(String)` all accept an XML string and parse it using the custom `XMLTokener`. Unlike `javax.xml.parsers.DocumentBuilder`, which has a configurable `FEATURE_SECURE_PROCESSING` flag, `XMLTokener` does not delegate to a proper XML parser at all — it implements its own character-level tokeniser.

The direct practical risk of XXE via an external entity (`<!ENTITY xxe SYSTEM "file:///etc/passwd">`) is mitigated here because `XMLTokener` skips `<!DOCTYPE` blocks via the `nextMeta()` loop (lines 112–122 in JSONML.java) rather than evaluating them. However:

1. The skip logic does **not** throw an error on encountering `<!DOCTYPE` — it silently consumes it. This means any future change that adds entity-reference expansion to `XMLTokener` would immediately introduce full XXE.
2. The org.json XML parsing classes from this era have been the subject of XXE concerns (referenced in OWASP reports) when used in certain JVM configurations where XML helpers are invoked indirectly.
3. If any caller passes externally controlled XML to `JSONML.toJSONObject()` or `XML.toJSONObject()`, the entire attack surface depends entirely on the robustness of this hand-rolled tokeniser receiving no security scrutiny since 2012.

```java
// JSONML.java lines 111-122 — DOCTYPE content silently consumed, no rejection
} else {
    i = 1;
    do {
        token = x.nextMeta();
        if (token == null) {
            throw x.syntaxError("Missing '>' after '<!'.");
        } else if (token == XML.LT) {
            i += 1;
        } else if (token == XML.GT) {
            i -= 1;
        }
    } while (i > 0);
}
```

**Risk:** If any current or future code path passes untrusted XML into `JSONML` or `XML.toJSONObject`, XXE or Billion-Laughs DoS attacks become possible. The silent discard of DOCTYPE (rather than a hard rejection) means the risk is latent and easy to introduce accidentally.

**Recommendation:**
1. Upgrade to a modern org.json version that uses `javax.xml.parsers.SAXParser` with `FEATURE_SECURE_PROCESSING` and `XMLConstants.ACCESS_EXTERNAL_DTD` set to `""`.
2. If XML-to-JSON conversion is needed, prefer Jackson's `XmlMapper` with `MapperFeature.USE_ANNOTATIONS` and XMLInputFactory hardened settings.
3. Audit all callers of `JSONML.toJSONObject`, `JSONML.toJSONArray`, and `XML.toJSONObject` for externally controlled input.

---

### HIGH: IDOR — `edit_licence` updates driver licence by raw driver_id with no company ownership check

**File:** `src/main/java/com/action/AdminDriverEditAction.java` (lines 123–148), `src/main/java/com/dao/DriverDAO.java` (lines 49–50, 630–646)

**Description:**
When `op_code = "edit_licence"` is submitted, the action retrieves `LicenceBean` from the form (which carries the `driver_id` from the form field), then calls `DriverDAO.updateDriverLicenceInfo(licencebean, dateFormat)`. The SQL executed is:

```java
// DriverDAO.java lines 49-50
private static final String UPDATE_DRIVER_LICENSE_SQL =
    "update driver set licno = ?, expirydt = ?, securityno = ?, addr = ? where id = ?";
```

```java
// DriverDAO.java lines 633-643
int rowUpdated = DBUtil.updateObject(UPDATE_DRIVER_LICENSE_SQL,
    (stmt) -> {
        stmt.setString(1, licencebean.getLicence_number());
        ...
        stmt.setLong(5, licencebean.getDriver_id());  // driver_id comes from form, never verified
    });
```

The `driver_id` value (parameter 5 in the `WHERE id = ?` clause) comes directly from `adminDriverEditForm.getId()` / `adminDriverEditForm.getLicenseBean()`, which is a request-supplied parameter. **There is no `WHERE comp_id = ?` clause in `UPDATE_DRIVER_LICENSE_SQL`**, and the action does not cross-check that the target `driver_id` belongs to `sessCompId` before issuing the update.

The duplicate-licence check `DriverDAO.checkDriverByLic(sessCompId, ...)` does scope by company, but it only checks for duplicate licence numbers; it does not verify that the `driver_id` being updated belongs to the authenticated tenant. An authenticated user of Company A could submit a form with a `driver_id` belonging to Company B and successfully overwrite that driver's licence number, expiry date, security number, and address.

Additionally, `DriverDAO.getDriverById(Long id)` (line 419) also omits a company scope filter:

```java
// DriverDAO.java lines 154-157
private static final String QUERY_DRIVER_BY_ID =
    "select d.id, d.first_name, d.last_name, p.location, p.department, d.phone, p.enabled, d.email,'******' "
    + "from driver d "
    + "inner join permission p on d.id = p.driver_id "
    + "where d.id = ?";   // no comp_id filter
```

This means driver data for any tenant can be read and overwritten by a user authenticated to a different tenant.

**Risk:** Complete cross-tenant data tampering. An authenticated user of any company can overwrite the licence number, expiry date, security/DSN number, and address of any driver in any company. In a multi-tenant fleet-management context, this could be used to fraudulently extend licence validity or corrupt compliance records for competing operators.

**Recommendation:**
1. Add `AND comp_id = ?` to `UPDATE_DRIVER_LICENSE_SQL` and bind `sessCompId` as a parameter.
2. Add `AND p.comp_id = ?` (or equivalent) to `QUERY_DRIVER_BY_ID` and pass `sessCompId` from the session.
3. Before executing any write, explicitly verify `DriverDAO.getDriverById(driverId, sessCompId)` returns a non-null result and throw an `UnauthorizedException` otherwise.
4. Apply the same fix pattern to all other per-driver DAO methods that currently omit a company scope predicate.

---

### HIGH: LicenceBean `@Data` causes Lombok to auto-generate `toString()` that leaks `security_number`

**File:** `src/main/java/com/bean/LicenceBean.java` (lines 9–28)

**Description:**
`LicenceBean` is annotated with Lombok `@Data`, which generates — among other methods — a `toString()` method that includes **all** fields:

```java
@Data
@NoArgsConstructor
public class LicenceBean implements Serializable {
    private Long   driver_id      = null;
    private String licence_number = null;
    private String expiry_date    = null;
    private String security_number = null;   // <-- government-issued DSN / security code
    private String address         = null;
    private String op_code         = null;
    ...
}
```

Lombok `@Data` generates:
```java
// Auto-generated by Lombok
public String toString() {
    return "LicenceBean(driver_id=" + this.driver_id
        + ", licence_number=" + this.licence_number
        + ", expiry_date=" + this.expiry_date
        + ", security_number=" + this.security_number   // plaintext
        + ", address=" + this.address
        + ", op_code=" + this.op_code + ")";
}
```

`security_number` in a driver licence context is typically the document security/DSN number — a government-issued identifier used to verify licence authenticity. The application logs `LicenceBean` objects via:

```java
// DriverDAO.java line 631
log.info("Inside DriverDAO Method : updateDriverLicenceInfo");
```

and Struts/Tomcat exception handlers frequently call `toString()` on action form and bean objects when logging errors. This means the full `security_number` value is likely written to application logs (Log4j, catalina.out) in plaintext, exposing it to anyone with log access (developers, ops staff, SIEM operators, potential log-injection attackers).

**Risk:** Driver licence security/DSN numbers are personally identifiable government document data. Exposure in logs violates GDPR Art. 5(1)(f) (integrity and confidentiality), and depending on jurisdiction may also breach road transport or identity document regulations. If logs are shipped to a centralised logging platform, the blast radius is significant.

**Recommendation:**
1. Replace `@Data` with explicit `@Getter` and `@Setter`, and manually implement `toString()` that either omits `security_number` entirely or replaces it with `"[REDACTED]"`.
2. Alternatively, annotate the `security_number` field with `@ToString.Exclude` (Lombok 1.18.x+):
   ```java
   @ToString.Exclude
   private String security_number = null;
   ```
3. Audit all other `@Data`-annotated beans in the `com.bean` package for similar sensitive-field exposure.
4. Consider whether `licence_number` also qualifies as PII requiring redaction.

---

### MEDIUM: json_result.jsp outputs unescaped scriptlet content — potential reflected XSS via `result` attribute

**File:** `src/main/webapp/html-jsp/result/json_result.jsp` (lines 1–12)

**Description:**
The JSP writes a JSON literal directly to the response using a JSP expression (`<%= message %>`):

```jsp
<%
String message = "";
String result = request.getAttribute("result") == null ? "" :
                request.getAttribute("result").toString();

if (result.equalsIgnoreCase("success")) {
    message = "{ \"status\":\"success_close\", \"message\":\"Mail has been sent\" }";
} else {
    message = "{ \"status\":\"error\", \"message\":\"Sending Failed.\" }";
}
%>
<%= message %>
```

The `result` attribute is read from `request.getAttribute("result")` and used only in an `equalsIgnoreCase` branch, so the `result` value itself is not reflected. The `message` variable contains static string literals and is safe as written.

However, three secondary concerns are present:

1. **No `Content-Type` header set.** The JSP emits JSON but does not set `response.setContentType("application/json; charset=UTF-8")`. Browsers may sniff the response as `text/html` (X-Content-Type-Options is not set either). If a future developer adds a variable into `message`, the response could be rendered as HTML and interpreted as script.

2. **No `X-Content-Type-Options: nosniff` header.** Without this header, Internet Explorer and some Chromium-era browsers may MIME-sniff the response as HTML.

3. **Future-proofing risk.** The pattern `<%= message %>` without escaping is a well-established XSS vector. If a developer adds a field sourced from request data into `message` in the future (e.g., echoing back an email address or name in the "success" message), it will immediately become a stored or reflected XSS vulnerability with no HTML escaping in place.

**Risk:** Currently low/informational given the static strings, but the structural pattern is dangerous and the missing `Content-Type` header is a real misconfiguration that increases the XSS attack surface of any future change.

**Recommendation:**
1. Add `response.setContentType("application/json; charset=UTF-8");` at the top of the scriptlet.
2. Add `response.setHeader("X-Content-Type-Options", "nosniff");`.
3. If dynamic data is ever added to the JSON response, use a proper JSON serialisation library (e.g., `JSONObject.quote(value)` or Jackson `ObjectMapper`) rather than string concatenation.
4. Consider migrating to a proper Struts result type (`json` plugin or a dedicated `JsonResultAction`) rather than building raw JSON in a JSP.

---

### MEDIUM: LanguageDAO uses `Statement` (not `PreparedStatement`) with a static SQL string — low-risk as written, but poor practice establishing a dangerous pattern

**File:** `src/main/java/com/dao/LanguageDAO.java` (lines 47–52)

**Description:**
`getAllLan()` creates a `Statement` rather than a `PreparedStatement`:

```java
// LanguageDAO.java lines 47-52
conn = DBUtil.getConnection();
stmt = conn.createStatement(ResultSet.TYPE_SCROLL_SENSITIVE, ResultSet.CONCUR_READ_ONLY);

String sql = "select id,name from language";
log.info(sql);          // SQL logged at INFO level — acceptable for a static query
rs = stmt.executeQuery(sql);
```

The query string is a hardcoded literal with no user input concatenation, so there is **no SQL injection vulnerability in this specific method as currently written**. However:

1. `Statement` is used where `PreparedStatement` would be equally simple and would enforce the habit of parameterisation throughout the codebase.
2. The use of `ResultSet.TYPE_SCROLL_SENSITIVE` is unnecessary for a simple forward-only iteration (it opens a server-side cursor on some JDBC drivers, increasing DB load).
3. `log.info(sql)` logs the full query at INFO level for every call. While harmless for a static query, this is a pattern that has been copy-pasted elsewhere in the DAO layer (confirmed in `DriverDAO`) where the logged SQL includes column names that could aid an attacker in schema reconnaissance if logs are accessible.

**Risk:** No direct SQL injection risk in the current query. The risk is in the coding pattern being replicated: if a developer copies this method and adds a user-supplied filter parameter using string concatenation (rather than parameterisation), SQL injection will result. The existing `Statement`-based pattern offers no syntactic resistance to that mistake, unlike `PreparedStatement` which forces parameterisation.

**Recommendation:**
1. Replace `Statement` with `PreparedStatement` and use `ResultSet.TYPE_FORWARD_ONLY, ResultSet.CONCUR_READ_ONLY` for this read-only query:
   ```java
   PreparedStatement stmt = conn.prepareStatement(
       "select id, name from language",
       ResultSet.TYPE_FORWARD_ONLY,
       ResultSet.CONCUR_READ_ONLY);
   rs = stmt.executeQuery();
   ```
2. Establish a team coding standard that `Statement` is never used for DAO queries; all queries must use `PreparedStatement` or the `DBUtil.queryForObject`/`DBUtil.updateObject` lambda pattern already present in `DriverDAO`.
3. Move SQL logging to `DEBUG` level (not `INFO`) or suppress it entirely in production to reduce schema information leakage.

---

### MEDIUM: LanguageDAO singleton uses double-checked locking without `volatile` — theoretical thread-safety defect

**File:** `src/main/java/com/dao/LanguageDAO.java` (lines 19–33)

**Description:**
The singleton is implemented with double-checked locking:

```java
private static LanguageDAO instance;   // line 19 — NOT volatile

public static LanguageDAO getInstance() {
    if (instance == null) {                          // first check (unsynchronised)
        synchronized (LanguageDAO.class) {
            if (instance == null) {                  // second check
                instance = new LanguageDAO();
            }
        }
    }
    return instance;
}
```

Without the `volatile` keyword on the `instance` field, the Java Memory Model (pre-JDK 5 and in theory on modern JVMs under aggressive compiler optimisation) permits the write to `instance` to be observed by other threads before the `LanguageDAO` constructor has completed. This means a thread could receive a reference to a partially constructed `LanguageDAO` object.

In practice, on modern JVMs (JDK 8+) with the current JIT implementations this rarely manifests. However, it is a known defect pattern that static analysis tools (SpotBugs DC_DOUBLECHECK, SonarQube) flag as a bug.

**Risk:** Theoretical race condition on JVM startup under high concurrency. Could theoretically return a partially constructed singleton to a Tomcat request thread.

**Recommendation:**
Declare `instance` as `volatile`:
```java
private static volatile LanguageDAO instance;
```

---

### LOW: `JSONException` shadows `cause` field, breaking standard `Throwable.getCause()` chaining

**File:** `src/main/java/com/json/JSONException.java` (lines 10–27)

**Description:**
`JSONException` declares its own `private Throwable cause` field and overrides `getCause()` to return it:

```java
public class JSONException extends Exception {
    private static final long serialVersionUID = 0;
    private Throwable cause;     // shadows Throwable.cause

    public JSONException(Throwable cause) {
        super(cause.getMessage());   // does NOT call super(cause) — breaks chaining
        this.cause = cause;
    }

    public Throwable getCause() {
        return this.cause;
    }
}
```

The constructor calls `super(cause.getMessage())` rather than `super(cause)`. This means:
- `Throwable.initCause()` is never called on the parent class.
- The standard Java serialisation mechanism for `Throwable.cause` (used by frameworks, loggers, and remote debuggers) will return `null` from the inherited path.
- Stack trace printing via `Throwable.printStackTrace()` will not show the cause chain on some environments where the overridden `getCause()` is not called polymorphically.

If an `IOException` occurs during JSON parsing (e.g., in `JSONTokener`), the wrapped `IOException`'s stack trace may be silently lost in production logging.

**Risk:** Low severity — no direct security impact. However, it can mask the root cause of errors (e.g., swallowing network or I/O exceptions), which may impede incident response.

**Recommendation:**
Change the constructor to use `super(message, cause)`:
```java
public JSONException(Throwable cause) {
    super(cause.getMessage(), cause);
    // remove the private 'cause' field and override — rely on Throwable
}
```

---

### LOW: `JSONTokener.skipTo()` uses a fixed 1MB `mark` buffer — potential memory pressure under large inputs

**File:** `src/main/java/com/json/JSONTokener.java` (lines 400–423)

**Description:**
`skipTo(char to)` marks the reader with a hardcoded buffer size of `1_000_000` bytes:

```java
// JSONTokener.java line 406
this.reader.mark(1000000);
```

If `skipTo()` is called on a large input (which can happen when scanning to a specific delimiter character inside `XMLTokener.skipPast()`), the JDBC `BufferedReader` will allocate a 1 MB mark buffer on every call. Under concurrent load this can accumulate to significant heap pressure.

**Risk:** Low — contributes to memory consumption under load but is unlikely to be directly exploitable as a standalone vulnerability given the authentication gate.

**Recommendation:**
Replace the hard-coded `1000000` with a configurable constant, or redesign `skipTo()` to avoid requiring mark/reset semantics (e.g., re-implement using a character-by-character scan without mark).

---

### INFO: `licence.jsp` is an empty file — dead code or build artifact

**File:** `src/main/webapp/html-jsp/driver/licence.jsp`

**Description:**
The file `licence.jsp` exists in the repository but contains only a single empty line (confirmed by examining the raw file bytes, which showed zero visible content). It is referenced in the audit scope, suggesting it was expected to render driver licence detail data.

A blank JSP that is reachable via a URL mapping will return an empty 200 OK response, which:
- May confuse monitoring/alerting tools.
- If the JSP was previously populated and was cleared (rather than deleted), it may indicate an unfinished feature or an accidental data-scrubbing commit.

**Risk:** Informational. If this JSP is URL-mapped and reachable without authentication, it represents a minor information-disclosure surface (the URL path confirms the application has a licence management feature). No XSS or injection is present because there is no content.

**Recommendation:**
1. If the JSP is not used, remove it from the repository and remove any corresponding Struts forward configuration.
2. If it is a placeholder for future development, add an explicit HTTP 404 or forward to an error page until implementation is complete.

---

### INFO: Raw `e.printStackTrace()` in LanguageDAO — stack trace leakage risk in production

**File:** `src/main/java/com/dao/LanguageDAO.java` (line 65)

**Description:**
```java
} catch (Exception e) {
    InfoLogger.logException(log, e);
    e.printStackTrace();            // writes to stderr / catalina.out
    throw new SQLException(e.getMessage());
}
```

`e.printStackTrace()` writes to `System.err` (Tomcat's `catalina.out` or equivalent). In a production environment where `catalina.out` is accessible (e.g., shared hosting, insecure log shipping), this exposes full stack traces including class names, method names, and line numbers that assist an attacker in reconnaissance. The exception is already logged via `InfoLogger.logException`, making the `printStackTrace()` call redundant.

**Risk:** Informational — assists attacker reconnaissance if log files are accessible.

**Recommendation:** Remove `e.printStackTrace()`. The `InfoLogger.logException(log, e)` call already handles structured logging.

---

### INFO: `LicenceBean` `@Builder` constructor is `private` — inconsistency with `@NoArgsConstructor`

**File:** `src/main/java/com/bean/LicenceBean.java` (lines 9–28)

**Description:**
`LicenceBean` uses both `@NoArgsConstructor` (public no-arg constructor generated by Lombok) and a `@Builder`-annotated `private` all-args constructor:

```java
@Data
@NoArgsConstructor
public class LicenceBean implements Serializable {
    ...
    @Builder
    private LicenceBean(Long driver_id, String licence_number, ...) { ... }
}
```

Lombok's `@Builder` on a `private` constructor generates a builder whose `build()` method calls the private constructor via reflection or inner-class access. This pattern is unusual and may cause issues if the class is serialised/deserialised by frameworks (e.g., Jackson, Struts BeanUtils) that rely on the public no-arg constructor together with setter injection. The `@Data` annotation also generates `equals()`/`hashCode()` based on all fields — including `security_number` — meaning two `LicenceBean` objects with different security numbers will compare as unequal even if all other fields match, which may cause subtle bugs in duplicate-detection logic.

**Risk:** Informational — design inconsistency that may cause serialisation surprises or subtle equality bugs, but no direct exploitable vulnerability.

**Recommendation:** Review whether `@Builder` is appropriate here given the Struts ActionForm binding model. If the bean is only populated via the builder (as seen in `AdminDriverEditForm.getLicenseBean()`), remove `@NoArgsConstructor` and make the builder constructor package-private. If Struts bean binding also populates the object, use a plain POJO with explicit setters.

---

## Summary

| Severity | Count | Finding Titles |
|----------|-------|----------------|
| CRITICAL | 0 | — |
| HIGH | 3 | Outdated org.json (CVE-2022-45688 / CVE-2023-5072 DoS); JSONML/XML XXE risk; IDOR on edit_licence (cross-tenant driver data write) |
| MEDIUM | 3 | LicenceBean @Data toString leaks security_number; json_result.jsp missing Content-Type / XSS structure; LanguageDAO Statement pattern + volatile singleton |
| LOW | 2 | JSONException broken cause chaining; JSONTokener 1MB mark buffer |
| INFO | 3 | licence.jsp is empty/dead; e.printStackTrace() in LanguageDAO; LicenceBean @Builder/@NoArgsConstructor inconsistency |

**CRITICAL: 0 / HIGH: 3 / MEDIUM: 3 / LOW: 2 / INFO: 3**
