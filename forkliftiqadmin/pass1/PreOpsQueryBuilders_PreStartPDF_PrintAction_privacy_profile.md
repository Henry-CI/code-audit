# Security Audit Report — Pass 1
## Files: PreOps QueryBuilders, PreStartPDF, PrintAction, privacy.jsp / PrivacyAction, profile.jsp / ProfileBean
**Application:** forkliftiqadmin (Apache Struts 1.3.10 / Tomcat)
**Branch:** master
**Audit Date:** 2026-02-26
**Auditor:** Automated static analysis

---

## Scope

| # | File |
|---|------|
| 1 | `src/main/java/com/querybuilder/preops/PreOpsByCompanyIdQuery.java` |
| 2 | `src/main/java/com/querybuilder/preops/PreOpsCountByCompanyIdQuery.java` |
| 3 | `src/main/java/com/querybuilder/preops/PreOpsReportByCompanyIdQuery.java` |
| 4 | `src/main/java/com/pdf/PreStartPDF.java` |
| 5 | `src/main/java/com/action/PrintAction.java` |
| 6 | `src/main/webapp/html-jsp/privacy.jsp` |
| 7 | `src/main/java/com/action/PrivacyAction.java` |
| 8 | `src/main/webapp/includes/privacyText.jsp` |
| 9 | `src/main/webapp/html-jsp/settings/profile.jsp` |
| 10 | `src/main/java/com/bean/ProfileBean.java` |

Supporting files inspected for context: `AdminRegisterAction.java`, `AdminRegisterActionForm.java`, `AdminMenuAction.java`, `FilterHandler.java`, `DateBetweenFilterHandler.java`, `UnitManufactureFilterHandler.java`, `UnitTypeFilterHandler.java`, `StringContainingFilterHandler.java`, `StatementPreparer.java`, `BarCode.java`, `struts-config.xml`.

---

## Findings

---

### HIGH: Unparameterized field name injection in FilterHandler SQL construction

**File:** `PreOpsReportByCompanyIdQuery.java` (lines 41–45); `DateBetweenFilterHandler.java` (lines 19–23); `UnitManufactureFilterHandler.java` (lines 17–19); `UnitTypeFilterHandler.java` (lines 17–19); `StringContainingFilterHandler.java` (lines 20–29)

**Description:**
Every `FilterHandler` implementation constructs dynamic SQL by embedding the `fieldName` argument directly into the SQL fragment via `String.format`:

```java
// DateBetweenFilterHandler.java line 22
return String.format(" AND timezone(?, %s at time zone 'UTC')::DATE BETWEEN ? AND ?", fieldName);

// UnitManufactureFilterHandler.java line 18
return String.format(" AND %s = ? ", fieldName);

// UnitTypeFilterHandler.java line 18
return String.format(" AND %s = ? ", fieldName);

// StringContainingFilterHandler.java line 21
return String.format(" AND %s ILIKE ? ", fieldNames.get(0));
```

The `fieldName` values are hardcoded at construction sites inside `PreOpsReportByCompanyIdQuery` (lines 28–32):

```java
new DateBetweenFilterHandler(filter, "check_date_time"),
new UnitManufactureFilterHandler(filter, "manu_id"),
new UnitTypeFilterHandler(filter, "type_id")
```

In these specific call sites the strings are compile-time constants, so this is **not currently exploitable via user input**. However, the `FilterHandler` interface itself places no restriction on `fieldName`, and `StringContainingFilterHandler` accepts `fieldNames` as a vararg from any caller. If any future caller (or an existing caller elsewhere in the codebase) passes a `fieldName` derived from user-controlled input, SQL injection would be immediately possible because the driver will treat the injected fragment as SQL syntax rather than a bound parameter.

The bind values for the WHERE clause filters are correctly passed via `StatementPreparer` (which wraps `PreparedStatement.setXxx` calls with auto-incremented index), so the value side is safe. The column-name side is structurally unsafe by design.

**Risk:**
If `fieldName` ever originates from user input (e.g., a sort-column or filter-field selector), an attacker can inject arbitrary SQL into the query, potentially reading, modifying, or deleting data across all tenants.

**Recommendation:**
Validate `fieldName` against an explicit allowlist of permitted column names at construction time. For example, throw `IllegalArgumentException` if the name is not in a static `Set<String>` of known safe identifiers. Do not rely on call-site discipline alone — the interface contract provides no enforcement.

---

### HIGH: Unsanitized request attribute rendered directly into JavaScript in profile.jsp

**File:** `src/main/webapp/html-jsp/settings/profile.jsp` (line 110)

**Description:**
The server-side request attribute `userSmsAlertExisting` is injected directly into a JavaScript variable without any escaping:

```jsp
var smsUsrAlertExisting = <%=request.getAttribute("userSmsAlertExisting")%>;
```

`AdminMenuAction.java` (line 105) sets this attribute as follows:

```java
request.setAttribute("userSmsAlertExisting",
    CompanyDAO.getInstance().checkExistingUserAlertByType(
        String.valueOf(sessUserId), "sms"));
```

The value is expected to be a boolean (`true` / `false`) returned from `checkExistingUserAlertByType`. However, because the attribute is typed as `Object` and emitted with a raw scriptlet, any deviation — such as the DAO returning a non-boolean object whose `toString()` contains quotes or script characters, or a future refactoring of the return type — would produce a stored or reflected XSS vector directly inside a `<script>` block. Unescaped injection inside a JavaScript context is more dangerous than HTML-context injection because JavaScript encoding rules differ from HTML encoding rules; standard HTML escape functions do not protect against `</script>` injection.

Even if the current DAO return type is strictly boolean, the pattern itself violates the principle of secure-by-default: any scriptlet `<%= ... %>` emission into a JS block must be treated as a XSS risk.

**Risk:**
If the attribute value is or becomes attacker-influenced, arbitrary JavaScript executes in the victim's browser under the application's origin, enabling session hijacking, CSRF token theft, or phishing overlays.

**Recommendation:**
Replace the raw scriptlet with a safe JSON encoding. Use a JSON library (e.g., Jackson or Gson) to serialize the value server-side and assign it:

```java
// In AdminMenuAction.java
request.setAttribute("userSmsAlertExisting",
    companyDAO.checkExistingUserAlertByType(...)); // keep as Boolean
```

```jsp
<%-- In profile.jsp — use JSTL / a JSON encoder, not raw scriptlet --%>
var smsUsrAlertExisting = ${userSmsAlertExisting == true ? 'true' : 'false'};
```

Or better, pass it as a data attribute on a DOM element and read it from JavaScript without inline scriptlets.

---

### HIGH: Arbitrary file write via unsanitized barcode image filename in BarCode.java (called from PrintAction)

**File:** `src/main/java/com/util/BarCode.java` (lines 107–124); `src/main/java/com/action/PrintAction.java` (lines 56–96)

**Description:**
`PrintAction` passes user-controlled values to `BarCode.genBarCode()` as the `msg` argument:

```java
// PrintAction.java lines 62–65
barCode.genBarCode(request, questionBean.getId()+"Y"+veh_id);
barCode.genBarCode(request, questionBean.getId()+"N"+veh_id);
```

and for the driver barcode path (lines 104, 109):

```java
barCode.genBarCode(request, String.format("%08d", Integer.parseInt(div_id))+"#");
```

`veh_id` and `div_id` come directly from request parameters with no sanitization beyond a null check:

```java
// PrintAction.java lines 40–41
String veh_id = request.getParameter("veh_id")==null?"0":request.getParameter("veh_id");
String div_id = request.getParameter("div_id")==null?"":request.getParameter("div_id");
```

Inside `BarCode.genBarCode()`, when the output format is a bitmap (the default for non-SVG/EPS requests), the `msg` value after simple prefix-stripping is used directly as a filename component:

```java
// BarCode.java lines 107–124
String img = msg;
if(img.endsWith("#"))       { img = img.substring(0, img.length()-1); }
if(img.contains("$%"))      { img = img.substring(img.indexOf("%")+1); }
if(img.startsWith("%"))     { img = img.substring(1); }

String curerntDir = getClass().getProtectionDomain().getCodeSource()
                               .getLocation().getPath();
OutputStream out = new java.io.FileOutputStream(
    new File(curerntDir + "/../../../../../images/barcode/" + img + ".png"));
```

The stripping logic removes only the specific prefixes `#`, `$%`, and `%`. It does not remove path separator characters (`/`, `\`) or `..` sequences. An attacker who can control `veh_id` or the barcode message content can inject a path such as `../../webapps/ROOT/shell.jsp` to write an arbitrary file anywhere the Tomcat process has write permission.

For the `driverbarcode` path, `Integer.parseInt(div_id)` provides a numeric parse that eliminates path traversal for `div_id` specifically, but the `%08d` format produces a numeric-only string. For `veh_id`, however, there is no such sanitization. `questionBean.getId()+"Y"+veh_id` — if `veh_id` is `../../evil`, the resulting filename traverses directories.

Additionally, the path construction uses `/../../../../../images/barcode/` — five `..` hops up from the application's code location — which is itself a fragile assumption about the server layout and makes the write target predictable.

**Risk:**
An authenticated attacker (any logged-in user whose `sessCompId` is non-null) can write arbitrary content to arbitrary paths on the server filesystem, including deploying a JSP web shell. This is a remote code execution (RCE) primitive.

**Recommendation:**
1. Sanitize `veh_id` and any other inputs used in barcode generation to numeric digits only (validate with a regex such as `^\d+$` before use).
2. In `BarCode.genBarCode()`, normalize the computed `img` filename through `Paths.get(...).normalize()` and verify the resolved path starts with the intended base directory before opening the file.
3. Strongly consider not writing barcode images to disk at all: generate them in memory, stream the bytes directly to the HTTP response or store in a temp file with a server-generated UUID name, and delete after use.

---

### MEDIUM: No CSRF protection on privacy acceptance form

**File:** `src/main/webapp/html-jsp/privacy.jsp` (lines 6–16); `src/main/java/com/action/PrivacyAction.java` (lines 16–26)

**Description:**
The privacy acceptance form submits via HTTP POST to `privacy.do` with no CSRF token:

```jsp
<!-- privacy.jsp lines 6–16 -->
<form method="post" action="privacy.do" name="privacyForm">
    <textarea readonly="readonly" ...>
      <%@ include file="../includes/privacyText.jsp"%>
    </textarea>
    <input type="checkbox" onchange="enableSubmit()" name="privacy"/>
    <html:submit styleClass="btn btn-primary" disabled="true" styleId="submitBtn">
        <bean:message key="button.submit"/>
    </html:submit>
</form>
```

`PrivacyAction.execute()` reads `sessCompId` from the session and calls `companyDAO.updateCompPrivacy(sessCompId)` — it does not verify any request-origin token:

```java
// PrivacyAction.java lines 21–25
String sessCompId = (String) session.getAttribute("sessCompId") == null
    ? "" : (String) session.getAttribute("sessCompId");
CompanyDAO companyDAO = CompanyDAO.getInstance();
companyDAO.updateCompPrivacy(sessCompId);
return mapping.findForward("successAdmin");
```

A forged cross-origin POST to `privacy.do` from any site will cause the authenticated user's company privacy consent record to be updated without their knowledge. While the privacy acceptance flow itself has limited impact compared to a profile change, accepting privacy policy on behalf of an unaware user has legal/compliance implications and demonstrates that the CSRF surface is broader than just this one endpoint.

Struts 1.3 does not include built-in CSRF protection; it must be implemented manually.

**Risk:**
An attacker can send a victim a link or embed an invisible form on any website that, when loaded by the authenticated user, silently records the company's privacy acceptance. Depending on jurisdiction, this may create false legal consent records.

**Recommendation:**
Introduce a synchronizer token pattern: generate a random per-session token stored in `HttpSession`, emit it as a hidden field in all POST forms, and validate it in the action (or in a Struts `RequestProcessor` subclass) before processing. Consider applying this protection to all state-mutating actions in the application.

---

### MEDIUM: No CSRF protection on profile update form (adminRegister.do)

**File:** `src/main/webapp/html-jsp/settings/profile.jsp` (lines 14–98); `src/main/java/com/action/AdminRegisterAction.java` (lines 246–289)

**Description:**
The profile update form posts to `adminRegister.do` with `accountAction=update` and contains no CSRF token:

```jsp
<!-- profile.jsp lines 14, 19 -->
<html:form action="adminRegister.do" method="post" styleClass="ajax_mode_c">
    <input type="hidden" name="method" value="save_my_profile">
    <input type="hidden" name="user_cd" value="">
    ...
    <input class="form-control" placeholder="Password" name="pin" type="password" value="">
```

`AdminRegisterAction` for the `update` branch (lines 246–248) uses only `sessCompId` from the session to identify whose profile to update:

```java
} else if (accountAction.equalsIgnoreCase("update")) {
    companybean.setId(sessCompId);
    UserUpdateResponse userUpdateReponse = compDao.updateCompInfo(companybean, sessUserId, sessionToken);
```

A cross-site forged POST with `accountAction=update` and attacker-chosen field values will update the authenticated company's contact details, email address, and password (`pin` field) without the user's interaction.

Because the form includes a password field, CSRF here has a higher impact than the privacy endpoint: an attacker can silently change the company account's password and email, locking out the legitimate user.

**Risk:**
Account takeover: an attacker who can get an authenticated admin to visit a crafted page can overwrite the company email address and password, taking full control of the account.

**Recommendation:**
Add a per-session CSRF synchronizer token to the `adminRegister.do` form and validate it in `AdminRegisterAction` for all mutating branches (`register`, `add`, `update`). Additionally, require the user to supply their current password before allowing a password change (server-side check, not just client-side).

---

### MEDIUM: Profile update does not require current password confirmation for password change

**File:** `src/main/java/com/action/AdminRegisterAction.java` (lines 246–289); `src/main/webapp/html-jsp/settings/profile.jsp` (lines 74–83)

**Description:**
The `update` branch of `AdminRegisterAction` passes the new `pin` (password) value from the form directly to `compDao.updateCompInfo()` without verifying the user's current password:

```java
// AdminRegisterAction.java lines 246–248
} else if (accountAction.equalsIgnoreCase("update")) {
    companybean.setId(sessCompId);
    UserUpdateResponse userUpdateReponse = compDao.updateCompInfo(companybean, sessUserId, sessionToken);
```

The form presents a password field (line 75):
```jsp
<input class="form-control" placeholder="Password" name="pin" type="password" value="">
```

Client-side validation in `fnsubmitAccount()` (line 120) checks that `pass == cpassword`, but this is JavaScript only and is trivially bypassed by sending a direct HTTP request. There is no server-side check that the existing password matches before the new one is applied.

**Risk:**
Any attacker who has physical or brief logical access to an authenticated session (e.g., shared workstation, or in combination with CSRF) can change the account password without knowing the existing one. This is also an insecure direct object reference for the password field: the update is keyed only to `sessCompId`, so if IDOR were possible elsewhere, it would extend to passwords.

**Recommendation:**
Require the current password to be submitted with any password-change request and validate it server-side (via Cognito's `changePassword` API or equivalent) before applying the new password.

---

### MEDIUM: `compId` stored as String; no type enforcement protects PDF/PDF image path against injection

**File:** `src/main/java/com/pdf/PreStartPDF.java` (lines 34, 42–46, 57, 140–144)

**Description:**
`PreStartPDF` receives `compId` as a `String` in its constructor (line 42) and stores it in a field (line 34):

```java
protected String compId = "";
// ...
public PreStartPDF(String compId, Date from, Date to) {
    this.compId = compId;
    // ...
}
```

`compId` is never used in the body of `PreStartPDF` itself (the `createTable` method contains only hardcoded placeholder text), so there is no direct injection risk within this class today. However, two other issues exist:

1. **`this.image` used in `Image.getInstance()` without validation (line 140):**
```java
private void addImage(Document document) throws DocumentException, IOException {
    Image img = Image.getInstance(this.image);
```
`Image.getInstance(String)` in iText accepts both filesystem paths and URLs. If `this.image` is set via `setImage()` with a caller-supplied value, an attacker who controls the image path can trigger a server-side request forgery (SSRF) by supplying an `http://` or `file://` URL, or can read arbitrary files from the server filesystem. The calling code that invokes `setImage()` must be inspected to determine exploitability.

2. **`this.result` used in `FileOutputStream` without validation (line 57):**
```java
PdfWriter.getInstance(document, new FileOutputStream(result));
```
If `setResult()` is called with an attacker-controlled path before `createPdf()`, the generated PDF will be written to an arbitrary location, creating a write-primitive analogous to the barcode file-write issue.

Both paths depend on whether callers pass user-controlled input to `setImage()` and `setResult()`. Even if current callers are safe, the lack of validation in the class itself creates a latent vulnerability.

**Risk:**
Depending on caller behavior: SSRF, arbitrary file read (via iText image loading), or arbitrary file write (via the PDF output path).

**Recommendation:**
1. Validate `this.image` against an allowlist of permitted schemes (`file://` within a specific directory only) and canonicalize the path before passing to `Image.getInstance()`.
2. Validate `this.result` against a known safe output directory using `Paths.get(result).normalize()` and confirm it is a descendant of the expected directory.
3. Remove or properly implement the `compId` field — it is accepted but unused, which is dead code that should be cleaned up to avoid confusion.

---

### MEDIUM: `PrintAction` — `veh_id` and `att_id` passed to DAO without numeric type validation

**File:** `src/main/java/com/action/PrintAction.java` (lines 40–41, 47–48)

**Description:**
`veh_id` and `att_id` are read from request parameters as raw strings and passed directly to DAO methods:

```java
String veh_id = request.getParameter("veh_id")==null?"0":request.getParameter("veh_id");
String att_id = request.getParameter("att_id")==null?"0":request.getParameter("att_id");
// ...
ArrayList<QuestionBean> arrQues = quesionDao.getQuestionByUnitId(veh_id, att_id, sessCompId, true);
List<UnitBean> arrVeh = unitDAO.getUnitById(veh_id);
```

No numeric validation is performed on `veh_id` or `att_id` before they are forwarded to the DAO. If `getQuestionByUnitId()` or `getUnitById()` incorporates these values into SQL via string concatenation, SQL injection is possible. Even if those DAOs use prepared statements, passing a non-numeric string where an integer is expected will produce unhandled exceptions that may leak stack traces.

Additionally, there is no authorization check that the `veh_id` belongs to `sessCompId`. A user from company A could request the questions and unit details for a vehicle belonging to company B by guessing or enumerating `veh_id`.

**Risk:**
- Potential SQL injection in downstream DAOs (requires inspection of `QuestionDAO.getQuestionByUnitId()` and `UnitDAO.getUnitById()`).
- IDOR: cross-tenant access to vehicle question and unit data if DAO queries are not scoped to `sessCompId`.

**Recommendation:**
1. Parse `veh_id` and `att_id` with `Integer.parseInt()` (or `Long.parseLong()`) immediately after reading from the request, returning an error if parsing fails.
2. Ensure `getQuestionByUnitId()` and `getUnitById()` include a `comp_id = ?` predicate bound to `sessCompId` to enforce tenant isolation.

---

### MEDIUM: `PrintAction` — `driverbarcode` branch integer parse of `div_id` can throw uncaught exception

**File:** `src/main/java/com/action/PrintAction.java` (lines 104, 109)

**Description:**
```java
barCode.genBarCode(request, String.format("%08d", Integer.parseInt(div_id))+"#");
request.setAttribute("barCodeDriver", String.format("%08d", Integer.parseInt(div_id)));
```

`Integer.parseInt(div_id)` will throw `NumberFormatException` if `div_id` is empty (the default value is `""`, line 43) or non-numeric. This exception propagates uncaught through `execute()` and will produce a Tomcat 500 error page that may expose stack-trace information including class names and internal paths.

**Risk:**
Information disclosure via uncaught exception; minor denial-of-service via crafted input.

**Recommendation:**
Validate `div_id` as a numeric string before the `driverbarcode` branch is entered, or wrap `Integer.parseInt()` in a try-catch that returns a user-facing error forward rather than propagating the exception.

---

### LOW: Privacy form lacks HTTP method restriction — GET request also triggers state change

**File:** `src/main/java/com/action/PrivacyAction.java` (lines 16–26); `src/main/webapp/WEB-INF/struts-config.xml` (lines 99–102)

**Description:**
The `struts-config.xml` action mapping for `/privacy` does not restrict the HTTP method:

```xml
<action path="/privacy" type="com.action.PrivacyAction">
    <forward name="successAdmin" path="adminDefinition"/>
</action>
```

Struts 1.x routes all HTTP methods (GET, POST, PUT, etc.) to the same `execute()` method unless the mapping specifies a method constraint. `PrivacyAction` performs a state-changing database update (`updateCompPrivacy`) on any request, including GET. This means a simple hyperlink (`<a href="https://app/privacy.do">`) or an `<img src>` tag can trigger privacy acceptance without a form submission.

**Risk:**
The CSRF attack surface is expanded: even a URL-only vector (link, image, redirect) can trigger the state change. The barrier to CSRF exploitation is lower than if POST were required.

**Recommendation:**
Add a method check at the start of `PrivacyAction.execute()`:

```java
if (!"POST".equalsIgnoreCase(request.getMethod())) {
    return mapping.findForward("failure");
}
```

Additionally, implement the CSRF token described in the MEDIUM finding above.

---

### LOW: `PreStartPDF.createTable()` — hardcoded placeholder data in production class

**File:** `src/main/java/com/pdf/PreStartPDF.java` (lines 77–96)

**Description:**
The `createTable()` method, which is `public` and therefore callable by subclasses and external code, contains only the original iText tutorial placeholder content:

```java
cell = new PdfPCell(new Phrase("Cell with colspan 3"));
// ...
table.addCell("row 1; cell 1");
table.addCell("row 1; cell 2");
table.addCell("row 2; cell 1");
table.addCell("row 2; cell 2");
```

None of the actual pre-start inspection data is rendered. If `createPdf()` is called in production with the expectation of a populated table, every generated PDF will contain placeholder boilerplate instead of real data. This is a data integrity / correctness issue.

There is also a dead import (`java.net.MalformedURLException`, line 5) and dead utility methods (`createList()`, line 125) that are never called, indicating the class was never completed.

**Risk:**
Incorrect PDFs delivered to users. No direct security impact, but dead/placeholder code in production is a code-quality and maintainability risk.

**Recommendation:**
Either complete the implementation of `createTable()` with real data rendering (using `compId`, `from`, `to` fields), or mark the class as `abstract` and require subclasses to override `createTable()`. Remove dead imports and unused methods.

---

### LOW: `ProfileBean.java` — empty stub class, Lombok assessment not applicable

**File:** `src/main/java/com/bean/ProfileBean.java`

**Description:**
`ProfileBean` is an empty stub with only a no-args constructor and a TODO comment:

```java
public class ProfileBean {
    public ProfileBean() {
        // TODO Auto-generated constructor stub
    }
}
```

The class has no fields and no Lombok annotations, so the originally suspected risk of Lombok `@Data` generating a `toString()` that leaks credentials or PII does not apply. The profile page (`profile.jsp`) uses `CompanyBean` (not `ProfileBean`) for its data binding. `ProfileBean` appears to be an abandoned/unimplemented class.

**Risk:**
No immediate security impact. Dead code creates confusion and maintenance overhead.

**Recommendation:**
Remove `ProfileBean` if it has no planned purpose, or complete its implementation if it is intended to replace `CompanyBean` on the profile page.

---

### INFO: PreOps query builders — SQL injection assessment: SAFE (with caveat)

**Files:** `PreOpsByCompanyIdQuery.java`, `PreOpsCountByCompanyIdQuery.java`, `PreOpsReportByCompanyIdQuery.java`

**Description:**
The base queries in `PreOpsByCompanyIdQuery` use `?` placeholders throughout:

```java
// PreOpsByCompanyIdQuery.java lines 6–14
private static final String BASE_QUERY =
    "FROM v_preops_report WHERE (comp_id = ? OR assigned_company_id = ? OR unit_company_id = ?) ";

static final String COUNT_QUERY =
    "SELECT COUNT(DISTINCT(result_id)) " + BASE_QUERY +
    "AND timezone(?, check_date_time at time zone 'UTC')::DATE = current_date::DATE ";
```

`PreOpsCountByCompanyIdQuery.prepareStatement()` correctly binds `companyId` three times (for the three `?` slots in `BASE_QUERY`) and `timezone` once (line 24–29), all via `StatementPreparer.addLong()` / `addString()` which ultimately call `PreparedStatement.setLong()` / `setString()`.

`PreOpsReportByCompanyIdQuery` assembles filters via `FilterHandler.getQueryFilter()` (parameterized with `?` — see HIGH finding above about `fieldName`) and binds values in `prepareStatement()`.

The **value** side of all queries is parameterized correctly. The **column-name** side (for `fieldName` in filters) is not, which is documented in the HIGH finding. The `companyId` used as the primary tenant isolation predicate is a `long` sourced from `sessCompId`, which provides adequate tenant scoping for the base WHERE clause.

**Risk:**
Informational — value-side SQL injection is not present. The structural field-name issue is captured separately at HIGH severity.

**Recommendation:**
No additional action required for the value binding. Address the field-name allowlist as described in the HIGH finding.

---

### INFO: PrivacyText.jsp — static content only, no dynamic output

**File:** `src/main/webapp/includes/privacyText.jsp`

**Description:**
The file contains only static HTML paragraphs (`<p>` tags) with hardcoded privacy policy text. There are no scriptlets, EL expressions, JSTL tags, or any other dynamic content. No XSS or injection risk is present.

**Risk:**
None.

**Recommendation:**
No action required.

---

### INFO: `AdminRegisterAction` — profile update correctly uses session `sessCompId`, no IDOR on the company record itself

**File:** `src/main/java/com/action/AdminRegisterAction.java` (lines 246–248)

**Description:**
For the `update` branch, the target company ID is taken exclusively from the session:

```java
companybean.setId(sessCompId);
```

The `user_cd` hidden field in `profile.jsp` (line 20) is set to an empty string:

```java
<input type="hidden" name="user_cd" value="">
```

There is no corresponding field in `AdminRegisterActionForm`, and `AdminRegisterAction` does not read it. Therefore, the update cannot be redirected to a different company by manipulating the `user_cd` parameter. IDOR on the company identity for the profile update path is not present.

However, the account-level password-change and CSRF issues documented above remain relevant.

**Risk:**
None for IDOR on company identity. Related issues are covered in MEDIUM findings above.

**Recommendation:**
No additional IDOR mitigation needed for this path. Maintain the practice of always deriving the target entity from the authenticated session rather than from request parameters.

---

## Summary

| Severity | Count | Findings |
|----------|-------|----------|
| CRITICAL | 0 | — |
| HIGH | 3 | Unparameterized fieldName in FilterHandler SQL; XSS via raw scriptlet in profile.jsp JS block; Arbitrary file write via unsanitized barcode filename in BarCode.java |
| MEDIUM | 5 | No CSRF on privacy form; No CSRF on profile update form; No current-password check on password change; PreStartPDF image/result path not validated; PrintAction veh_id/att_id not type-validated / potential IDOR |
| LOW | 3 | Privacy action accepts GET (widens CSRF surface); PreStartPDF hardcoded placeholder in production; ProfileBean is empty dead code |
| INFO | 3 | PreOps value-side SQL parameterization is correct; privacyText.jsp is static; AdminRegisterAction profile update correctly uses session for company identity |

**CRITICAL: 0 / HIGH: 3 / MEDIUM: 5 / LOW: 3 / INFO: 3**
