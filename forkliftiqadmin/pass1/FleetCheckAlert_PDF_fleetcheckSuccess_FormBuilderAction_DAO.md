# Pass 1 Audit — FleetCheckAlert / FleetCheckPDF / fleetcheckSuccess.jsp / FormBuilderAction / FormBuilderDAO

**Files:**
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/report/FleetCheckAlert.java`
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/pdf/FleetCheckPDF.java`
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/fleetcheckSuccess.jsp`
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/action/FormBuilderAction.java`
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/dao/FormBuilderDAO.java`

**Date:** 2026-02-26

---

## Summary

This audit covers two report/output components (FleetCheckAlert, FleetCheckPDF), one success-redirect JSP (fleetcheckSuccess.jsp), and one Struts 1.x action/DAO pair (FormBuilderAction, FormBuilderDAO) responsible for building and submitting custom pre-operation forms.

The most severe findings are in FormBuilderDAO and FormBuilderAction. `FormBuilderDAO.getLib()` constructs a SQL query by direct string concatenation of the `questionId` and `type` parameters that originate from HTTP request parameters, creating a confirmed SQL injection vulnerability. `FormBuilderAction` contains no CSRF protection and an IDOR vulnerability in the `save` path: it sends a diagnostic email to an entity address looked up by the unvalidated user-supplied `qid`/`type` parameters, and it writes unescaped user-controlled values directly into the HTML email body. FleetCheckAlert renders database-retrieved values directly into HTML email content with no escaping. FleetCheckPDF has a path derivation that embeds a hardcoded internal server path fragment derived at class-load time from the JVM classpath, and the PDF output path uses `docRoot` supplied by the caller without sanitisation. The `fleetcheckSuccess.jsp` file is clean with respect to XSS and information disclosure on its own, though two minor issues are noted.

**Total findings: 14**

---

## Findings

---

### CRITICAL: SQL Injection via String Concatenation in FormBuilderDAO.getLib()

**File:** `FormBuilderDAO.java` (line 37)

**Description:**
`getLib()` builds its query by direct string concatenation of the caller-supplied `questionId` and `type` parameters, neither of which is validated or sanitised:

```java
String sql = "select id, form_object from form_library where question_id ="
             + questionId + " and type = '" + type + "'";
stmt.executeQuery(sql);
```

`FormBuilderAction` passes `qid` and `type` directly from `request.getParameter()` to this method (lines 50–51, 89):

```java
String qid  = request.getParameter("qid")==null?"0":request.getParameter("qid");
String type = request.getParameter("type")==null?"":request.getParameter("type");
...
ArrayList<FormLibraryBean> arrLib = formBuilderDAO.getLib(qid, type);
```

An attacker can supply a malicious `type` or `qid` value (e.g., `type = ' OR '1'='1`) to read, modify, or delete arbitrary rows. Because `type` is injected inside a quoted string, classic UNION or boolean-based attacks apply. `questionId` is not quoted and is directly injectable as a numeric context, allowing UNION SELECT and stacked queries depending on the database driver.

**Risk:** Complete database compromise. An authenticated attacker (session required via PreFlightActionServlet) can exfiltrate all company data, credentials, and form objects, or escalate to OS-level access via database features (e.g., `INTO OUTFILE`, `xp_cmdshell`).

**Recommendation:** Replace `Statement` + concatenation with a `PreparedStatement` with positional parameters, mirroring the pattern already used in `saveLib()` and `saveAnswerForm()`. Validate that `questionId` is a positive integer before any database call; reject or sanitise `type` against a strict allowlist of known values.

---

### CRITICAL: IDOR — Unauthenticated Cross-Tenant Form and Email Access in FormBuilderAction

**File:** `FormBuilderAction.java` (lines 50–51, 75–80, 89)

**Description:**
The action accepts `qid` (question ID) and `type` directly from request parameters and uses them without any ownership check to:

1. Query `CompanyDAO.getEntityByQuestion(qid, type)` and retrieve the `name` and `email` of the entity that owns that question.
2. Send a diagnostic email containing the submitted form values to that entity's email address.
3. Retrieve the `FormLibraryBean` for that `qid`/`type` from any company.

No check is performed to verify that the authenticated user's company owns the question identified by `qid`. An attacker with a valid session belonging to Company A can supply a `qid` that belongs to Company B, causing:
- The email alert for that submission to be sent to Company B's contact address (information disclosure / social engineering vector).
- The form definition for Company B's questions to be served to Company A's user.

**Risk:** Cross-tenant data exposure and potential for email harassment or social engineering of other tenants. In combination with the SQL injection finding above, full cross-tenant data read is achievable.

**Recommendation:** After reading the session company ID (`sessCompId`), verify that the question identified by `qid` belongs to that company before proceeding. Reject the request with a 403 if the check fails.

---

### CRITICAL: HTML/Email Injection of Unescaped User-Controlled Data in FormBuilderAction (save path)

**File:** `FormBuilderAction.java` (lines 59–72, 80)

**Description:**
When `action == "save"`, the action iterates all HTTP request parameter names and values, and concatenates them verbatim into an HTML string that is then emailed:

```java
String html = "Driver:"+driverName+"<br/>Question:"+qName+"<br/>Time:"
              + DateUtil.GetDateNow()+"<br/><table><tr><td>Items</td><td>Values</td></tr>";

for(Enumeration e = request.getParameterNames(); e.hasMoreElements(); ) {
    ParameterNames = (String)e.nextElement();
    if(ParameterNames.contains("_")) {
        ParameterValues = request.getParameter(ParameterNames);
        ParameterNames = ParameterNames.substring(0, ParameterNames.indexOf("_"));
        html += "<tr><td>"+ParameterNames+"</td><td>"+ParameterValues+"</td></tr>";
    }
}
Util.sendMail(RuntimeConf.EMAIL_DIGANOSTICS_TITLE, html, name, email, "", RuntimeConf.emailFrom);
```

Any parameter whose name contains `_` has both its name and value embedded without HTML encoding. An attacker can inject arbitrary HTML into the email body, including hidden images that beacon to attacker-controlled infrastructure, JavaScript (in mail clients that render it), or content spoofing.

Additionally, `driverName` and `qName` are rendered without escaping: `driverName` comes from session data (lower risk) but `qName` is retrieved from the database keyed by the user-supplied `qid` — if that value was stored unsanitised, a stored XSS payload propagates into the email.

**Risk:** Email-borne HTML injection to any entity registered in the system. Can be used for phishing, data exfiltration via beacon images, and content spoofing within the email channel.

**Recommendation:** HTML-encode all user-supplied values and database-retrieved display strings before embedding them in HTML email content. Use `org.apache.commons.lang.StringEscapeUtils.escapeHtml()` or equivalent. Restrict the set of parameter names processed to a known allowlist from the form definition rather than iterating all request parameters.

---

### HIGH: SQL Injection via String Concatenation in FormBuilderDAO.getLib() — type Parameter

**File:** `FormBuilderDAO.java` (line 37)

**Description:**
This is the `type` parameter component of the SQL injection already identified as CRITICAL above, separated here to note the distinct injection context. The `type` parameter is embedded inside single quotes:

```java
"... and type = '" + type + "'"
```

This allows classic single-quote escape attacks: supplying `type = x' OR '1'='1` bypasses the `question_id` filter and returns all rows in `form_library`. Supplying `type = x'; DROP TABLE form_library; --` (where the driver permits stacked queries) could destroy data.

**Risk:** Data exfiltration and potential data destruction of the `form_library` table.

**Recommendation:** See CRITICAL finding above — use `PreparedStatement` for all parameters.

---

### HIGH: Unescaped Database Content Rendered into HTML Email Body in FleetCheckAlert

**File:** `FleetCheckAlert.java` (lines 140–154)

**Description:**
`setContent()` builds an HTML email body by embedding database-retrieved values without HTML encoding:

```java
html += "<td align='center'><strong>"+driverName+"</strong></td>";
html += "<td>"+unitName+"</td>"+
        "<td>"+resultBean.getTime()+"</td>"+
        "<td>"+status+"</td>"+
        "<td width='30%'>"+failures+"</td>"+
        "<td>"+comment+"</td>";
```

`driverName`, `unitName`, `status`, `failures`, and `comment` are all database-sourced. `comment` additionally receives the raw scanner `resultBean.getComment()` value appended without encoding (line 128). If any of these database fields contain HTML metacharacters (intentionally or via prior injection), the email body will render attacker-controlled markup.

The parent class `PreFlightReport.appendHtmlAlertCotent()` (in `PreFlightReport.java`, line 82) also embeds `this.title` without escaping:

```java
"<tr><td><strong>"+pm.getMessage("report.name")+"</strong>"+this.title+"</td></tr>"
```

**Risk:** Stored HTML injection into outbound alert emails. Anyone who can write to the driver, unit, or comment fields in the database (e.g., via the mobile scanner application) can inject HTML payloads into emails sent to fleet managers.

**Recommendation:** HTML-encode all data-derived strings before embedding into HTML. Apply encoding at the point of assembly, not at the storage layer.

---

### HIGH: No CSRF Protection on FormBuilderAction Save Operation

**File:** `FormBuilderAction.java` (lines 41–115)

**Description:**
The action operates under Struts 1.x, which does not provide built-in CSRF tokens. The `save` action path (triggered by `action=save` in the request) performs a state-changing operation (sends an email) without any synchroniser token or `Origin`/`Referer` header validation. An attacker who can lure an authenticated user to a malicious page can craft a cross-origin POST to `formBuilder.do?action=save&qid=X&type=Y&someField_key=value` and cause a diagnostic email to be dispatched on behalf of the victim.

**Risk:** Cross-Site Request Forgery allows an unauthenticated attacker to trigger email dispatch and form submission operations on behalf of logged-in users.

**Recommendation:** Implement a synchroniser token pattern. Generate a per-session or per-request token, store it in the session, embed it as a hidden field in the form, and validate it in the action before executing any state-changing logic.

---

### HIGH: Server-Side Request Forgery Risk — CSS Fetched via Internal HTTP from RuntimeConf.projectTitle

**File:** `FleetCheckAlert.java` (line 60); inherited pattern in `PreFlightReport.java` (line 68)

**Description:**
Both `appendHtmlAlertCotent()` in `FleetCheckAlert` and `appendHtmlCotent()` in `PreFlightReport` call:

```java
Util.getHTML("http://localhost:8090/" + RuntimeConf.projectTitle + "/css/bootstrap_table.css")
```

`RuntimeConf.projectTitle` is a static field initialised to `"PreStart"`. If this value is ever made configurable (e.g., from a database or configuration file that an attacker can influence), the URL becomes partially attacker-controlled, enabling SSRF against localhost services on port 8090. Even as a hardcoded value, inlining CSS fetched at email-generation time from an internal HTTP service into outbound HTML email is an architectural anti-pattern: it creates a dependency on the application being able to reach itself on localhost:8090, introduces latency, and would expose the CSS server response verbatim in the email if the server returned unexpected content.

**Risk:** If `projectTitle` ever becomes dynamic, full SSRF against internal services. As currently coded, denial of service on the email generation path if the loopback server is unavailable.

**Recommendation:** Bundle the CSS as a static resource embedded in the email template or loaded from the classpath. Do not perform HTTP fetches to construct email content.

---

### MEDIUM: Path Traversal Risk in FleetCheckPDF Output Path

**File:** `FleetCheckPDF.java` (line 37)

**Description:**
The PDF output path is constructed as:

```java
setResult(docRoot + RuntimeConf.PDF_FOLDER + Util.generateRadomName() + ".pdf");
```

where `docRoot` is passed in by the caller (the constructor parameter at line 34). `RuntimeConf.PDF_FOLDER` is the string `"/temp/"`. `Util.generateRadomName()` generates a timestamp+UUID filename, which is safe. However, `docRoot` is not validated or canonicalised. If the calling code passes a `docRoot` value derived from a request parameter, session value, or other user-influenced source without stripping `../` sequences, an attacker could influence the output path to write the PDF to an arbitrary location on the filesystem (e.g., a web-accessible directory, a cron-executed script location).

The image path at line 38 presents the same issue:

```java
setImage(docRoot + "/" + RuntimeConf.IMG_SRC + "/banner.jpg");
```

**Risk:** If `docRoot` is user-influenced, path traversal could allow writing a PDF to an arbitrary filesystem location, potentially overwriting files or placing content in web-accessible directories.

**Recommendation:** Validate and canonicalise `docRoot` against an expected server base path (e.g., the servlet context real path). Reject any `docRoot` that does not begin with the expected prefix after canonicalisation.

---

### MEDIUM: Hardcoded Internal JVM Classpath Derived Path Exposed in FleetCheckPDF

**File:** `FleetCheckPDF.java` (line 30)

**Description:**
The field:

```java
private String pdfurl = this.getClass().getProtectionDomain().getCodeSource()
    .getLocation().toString().substring(6) + "/../../../../../temp/";
```

derives a filesystem path from the JVM classpath using `ProtectionDomain`. This path is computed at class-load time and embeds internal server directory structure. While `pdfurl` is declared but never referenced anywhere in the visible code (it appears to be dead code / a leftover), its presence:

1. Confirms and embeds server-side directory layout that would be valuable to an attacker if this field value were ever logged or returned in a response.
2. Relies on `substring(6)` to strip the `file://` prefix, which will silently produce a malformed path on Windows (`file:///C:/...` — `substring(6)` strips `file:/` leaving `/C:/...`) or when running from a JAR with a different URL scheme.

**Risk:** Information disclosure of server directory structure if the value is logged (it is not HTML-rendered, so not directly exploitable as-is). Silent path construction failure on non-Unix deployments.

**Recommendation:** Remove the dead `pdfurl` field. If a classpath-relative temp path is needed, use `ServletContext.getRealPath()` passed from the action layer rather than classpath introspection.

---

### MEDIUM: Unvalidated Integer Parsing of User-Supplied qid in FormBuilderAction / FormBuilderDAO

**File:** `FormBuilderAction.java` (lines 50, 54, 75); `FormBuilderDAO.java` (lines 84, 98, 112–113, 159, 172, 186)

**Description:**
`qid` from the request parameter is used as-is (as a String) in the SQL injection vector in `getLib()`. In `saveLib()` and `saveAnswerForm()`, the String is parsed with `Integer.parseInt(questionId)`. If `questionId` is not a valid integer, these calls throw a `NumberFormatException` that propagates through `saveLib()` as a `SQLException`, which is caught and re-thrown. This means a non-numeric `qid` value causes an unhandled exception path that may expose stack trace information in the response, depending on how the application's error handling is configured.

In `FormBuilderAction`, `questionDAO.getQuestionById(qid)` is called at line 54 with the raw unvalidated string, and `arrQues.get(0)` at line 55 is called with no null or empty-list check, so a `qid` that matches no question (or a SQL-injected `qid` that returns empty) will throw an `IndexOutOfBoundsException`.

**Risk:** Application errors and potential stack trace disclosure. Combined with the SQL injection finding, error responses may leak database schema information.

**Recommendation:** Validate `qid` as a positive integer at the action layer before any DAO call. Return a user-friendly error if validation fails. Add null/empty list guards before accessing `arrQues.get(0)`.

---

### MEDIUM: Diagnostic Email Sent to Entity Address Without Rate Limiting or Authorisation Check

**File:** `FormBuilderAction.java` (lines 74–80)

**Description:**
On every `save` action, an email is sent to the address retrieved from `companyDAO.getEntityByQuestion(qid, type)`. There is no rate limiting, throttle, or additional authorisation check on this path. An attacker with a valid session can repeatedly POST to `formBuilder.do?action=save&qid=X&type=Y` to flood the email address of any entity in the system whose question ID is known, since `qid` is fully attacker-controlled (see IDOR finding). Combined with the IDOR finding, this enables email flooding of any registered entity.

**Risk:** Email flooding / denial of service against registered entity email addresses.

**Recommendation:** Implement rate limiting on the save path. Enforce ownership validation on `qid` before sending. Consider whether the diagnostic email is intended for production use or should be gated behind a debug flag.

---

### LOW: Raw Database Content Rendered into PDF Without Encoding in FleetCheckPDF

**File:** `FleetCheckPDF.java` (lines 143–152)

**Description:**
`unitName`, `status`, `failures`, and `comment` are written directly into iText `Phrase` objects:

```java
cell = new PdfPCell(new Phrase(failures, hdFont));
cell = new PdfPCell(new Phrase(comment, hdFont));
```

iText renders these as plain text (not HTML), so standard XSS does not apply. However, if any of these strings contain special PDF control characters or very long values, they could cause rendering anomalies or PDF metadata injection. The `comment` value is additionally appended with a raw scanner time string (line 139) with no length check.

**Risk:** Low probability PDF rendering anomaly. Not directly exploitable for code execution via iText's plain-text Phrase rendering, but represents a lack of defensive coding.

**Recommendation:** Truncate comment and failure strings to a reasonable maximum length before embedding in the PDF. Sanitise any non-printable or control characters.

---

### LOW: fleetcheckSuccess.jsp Auto-Redirect Form Submits to goSearch.do Without CSRF Token

**File:** `fleetcheckSuccess.jsp` (lines 9, 44)

**Description:**
The page includes a form that auto-submits to `goSerach.do` after a 10-second countdown via JavaScript:

```javascript
function redirect() {
    document.searchForm.submit();
}
```

The form (lines 9–10) carries no hidden CSRF token. If `goSerach.do` performs any state-changing operation (query against user session, etc.), the cross-origin submit could be triggered by a third party. This is a lower risk because the redirect is a GET-equivalent navigation to a search page, not a data mutation, but the pattern is noted for consistency.

**Risk:** Low. The auto-submit appears to be a read-only redirect. If the target action is ever changed to a mutating action, the absence of a token becomes HIGH.

**Recommendation:** Add a CSRF synchroniser token to all form submissions, including navigation forms, as a baseline defence-in-depth measure.

---

### INFO: Commented-Out Linde-Specific Code Leaves Dead Code and Internal Brand Names in Source

**File:** `FleetCheckAlert.java` (lines 31–40, 69–78); `FleetCheckPDF` parent chain

**Description:**
Large blocks of commented-out code reference an alternative "Linde" brand integration, including `getLindeLogo()`, `appendHtmlAlertCotentLinde()`, and `setLindeContent()`. These blocks reference internal partner/customer brand names (`fleetiq`, `FleetIQ360`, `Linde`) and reveal that the application was forked or adapted for a named enterprise customer. Similar references appear in `RuntimeConf.java` (`LINDEDB = "fleeiq"`, `emailFromLinde`, `LINDERPTTITLE`).

While commented-out code is not directly exploitable, it constitutes information disclosure of customer relationships and deployment topology that would assist an attacker in reconnaissance.

**Risk:** Informational. Reveals internal customer branding, a secondary database schema name (`fleeiq`), and a secondary email address (`info@fleetiq360.com`).

**Recommendation:** Remove commented-out code from production source. Move customer-specific configuration to external configuration files. The `LINDEDB` constant in `RuntimeConf` is live code and should also be reviewed for whether it is still in active use.

---

## Finding Count

- CRITICAL: 3
- HIGH: 4
- MEDIUM: 4
- LOW: 2
- INFO: 1
