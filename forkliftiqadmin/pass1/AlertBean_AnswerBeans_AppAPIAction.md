# Security Audit Report
## Files: AlertBean, AnswerBean, AnswerTypeBean, AppAPIAction
**Audit Run:** audit/2026-02-26-01/pass1
**Date:** 2026-02-26
**Auditor:** Automated Security Audit (Pass 1)
**Stack:** Apache Struts 1.3.10
**Branch:** master

---

## Files Audited

| # | File | Package / Class |
|---|------|-----------------|
| 1 | `src/main/java/com/bean/AlertBean.java` | `com.bean.AlertBean` |
| 2 | `src/main/java/com/bean/AnswerBean.java` | `com.bean.AnswerBean` |
| 3 | `src/main/java/com/bean/AnswerTypeBean.java` | `com.bean.AnswerTypeBean` |
| 4 | `src/main/java/com/action/AppAPIAction.java` | `com.action.AppAPIAction` |

Supporting files read for context:
- `src/main/webapp/WEB-INF/struts-config.xml` — confirms `/api` mapping
- `src/main/java/com/actionservlet/PreFlightActionServlet.java` — confirms `api.do` exclusion
- `src/main/webapp/html-jsp/apiXml.jsp` — API response template
- `src/main/java/com/util/RuntimeConf.java` — API action constants

---

## Reading Evidence

### AlertBean — Fields
```
private String alert_id    (line 11)
private String alert_name  (line 12)
private String alert_type  (line 13)
private String file_name   (line 14)
private String frequency   (line 15)
```
Lombok `@Data` + `@NoArgsConstructor` + `@Builder` (builder scoped `private`).

### AnswerBean — Fields
```
private String id          (line 17)
private String answer      (line 18)
private String faulty      (line 19)
private String quesion_id  (line 20)  [note: typo — "quesion" not "question"]
private String result_id   (line 21)
```
Implements `Serializable`. Lombok `@Data` + `@NoArgsConstructor`.

### AnswerTypeBean — Fields
```
private String id    (line 12)
private String name  (line 13)
```
Implements `Serializable`. Manual getters/setters.

### AppAPIAction — Methods and DAOs
- **Class:** `com.action.AppAPIAction extends org.apache.struts.action.Action`
- **Single method:** `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` (lines 42–373)
- **Entire method body is commented out** (lines 45–371 use `////` block comments)
- **Active code (lines 371–372):** `return mapping.findForward("apiXml")` — unconditionally forwards to `apiXml.jsp`
- **DAOs referenced in commented-out code (not executing):** `CompanyDAO`, `DriverDAO`, `LoginDAO`, `QuestionDAO`, `UnitDAO`
- **Struts-config mapping** (`struts-config.xml` lines 447–451):
  ```xml
  <action path="/api" scope="request" type="com.action.AppAPIAction">
      <forward name="apiXml" path="/html-jsp/apiXml.jsp"/>
  </action>
  ```
  No `name` (form bean), no `validate` attribute — no form validation configured.

### PreFlightActionServlet — api.do Exclusion Confirmation
`excludeFromFilter()` method, line 106:
```java
else if (path.endsWith("api.do")) return false;
```
`return false` means the path is **NOT subject to the session/auth check**. `api.do` is confirmed excluded from authentication enforcement.

---

## Findings

---

### FINDING 1 — CRITICAL: api.do Excluded from Authentication — Endpoint Permanently Returns Unchecked

**Severity:** CRITICAL
**File:** `src/main/java/com/actionservlet/PreFlightActionServlet.java`, line 106
**Also:** `src/main/java/com/action/AppAPIAction.java`, lines 45–373

**Description:**
`api.do` is explicitly excluded from the `PreFlightActionServlet` session authentication gate (`sessCompId != null` check). This is architecturally intentional — the original design used a `compKey` API key parameter to authenticate mobile app callers rather than a session. However, the entire authentication and authorization block inside `AppAPIAction.execute()` has been commented out (all lines 45–371 use `////` block comments). The method now contains **zero active logic**: no session check, no API key check, no `compKey` validation, nothing. It unconditionally forwards to `apiXml.jsp`.

**Evidence:**
```java
// PreFlightActionServlet.java line 106 — api.do bypasses the session auth gate:
else if (path.endsWith("api.do")) return false;

// AppAPIAction.java lines 45–372 — the entire body is commented out:
////     String compKey = request.getParameter("compKey")==null?"":...
////     // 001: Invalid API CALL: Unauthorised User
////     ...
            return mapping.findForward("apiXml");   // <-- only active line
```

**Impact:**
Any unauthenticated user — with no session and no API key — can reach `api.do` and receive a response. The intended API key gating (`compKey` / `loginDao.checkLoginAPI`) is completely disabled. The endpoint is publicly accessible with no credential check of any kind.

**Recommendation:**
Either (a) restore the `compKey` authentication block and enforce it as the first check before all other logic, or (b) if the API is intentionally disabled, remove `api.do` from the PreFlightActionServlet exclusion list so that it falls under session-based auth like all other endpoints. Do not leave an unauthenticated route that forwards to a data-rendering JSP.

---

### FINDING 2 — CRITICAL: apiXml.jsp — NullPointerException / Unhandled Null Dereference Causes Information Disclosure

**Severity:** CRITICAL
**File:** `src/main/webapp/html-jsp/apiXml.jsp`, line 13

**Description:**
`apiXml.jsp` calls `method.equalsIgnoreCase(...)` on line 13 without a null check. Because `AppAPIAction.execute()` no longer sets `request.setAttribute("method", action)` (that line is commented out at line 371), the `method` variable will always be `null` at runtime. The `null.equalsIgnoreCase(...)` call will throw a `NullPointerException`. Struts' global exception handler catches `java.lang.Exception` subclasses and forwards to `errorDefinition` — potentially leaking a stack trace to the caller depending on the error page configuration.

**Evidence:**
```java
// AppAPIAction.java line 371 — commented out, "method" attribute never set:
////     request.setAttribute("method", action);
            return mapping.findForward("apiXml");

// apiXml.jsp line 11–13 — unconditional dereference:
String method = (String)request.getAttribute("method");
String error  = (String)request.getAttribute("error");
if(method.equalsIgnoreCase(RuntimeConf.API_LOGIN))  // NPE if method == null
```

**Impact:**
Every request to `api.do` will throw an unhandled NPE. If the error page exposes exception details (stack traces), this constitutes information disclosure. Even without stack trace exposure, the endpoint is completely non-functional for its intended purpose.

**Recommendation:**
Add a null guard before dereferencing `method`: `if (method != null && method.equalsIgnoreCase(...))`. More importantly, restore the commented-out `request.setAttribute("method", action)` call in `AppAPIAction`, or disable the endpoint entirely.

---

### FINDING 3 — HIGH: Entire API Functionality Disabled Without Removal of Public Route

**Severity:** HIGH
**File:** `src/main/java/com/action/AppAPIAction.java`, lines 45–373

**Description:**
The complete business logic of the API — login, driver listing, vehicle listing, attachment listing, question listing, result saving, PDF report generation — has been commented out using `////` block comments. The class is a stub that does nothing except forward to a JSP that will immediately throw a NPE (see Finding 2). This is a maintenance and architectural risk: the public, unauthenticated route (`api.do`) remains registered in `struts-config.xml` and excluded from auth in `PreFlightActionServlet`, creating an attack surface with no corresponding utility.

**Evidence:**
```java
// AppAPIAction.java lines 45–371: 327 lines of dead code
////     String compKey = request.getParameter("compKey")==null?"":...
////     CompanyDAO companyDao = new CompanyDAO();
////     if(action.equalsIgnoreCase(RuntimeConf.API_LOGIN)) { ... }
////     else if(action.equalsIgnoreCase(RuntimeConf.API_DRIVER)) { ... }
////     // ... all remaining branches ...
            return mapping.findForward("apiXml");  // only active line
```

**Impact:**
The mobile app clients that depend on this API (login, driver/vehicle/question/result sync) receive no usable response. The disabled API key authentication means the endpoint cannot be safely re-enabled without a full security review of the commented-out code.

**Recommendation:**
Make a deliberate decision: if the API is permanently decommissioned, remove the struts-config mapping, remove the PreFlightActionServlet exclusion, and delete or archive the action class. If it is temporarily disabled, restore the logic under a feature flag and ensure authentication is re-enabled simultaneously.

---

### FINDING 4 — HIGH: Commented-Out Code Contains Plaintext Password Parameter Handling

**Severity:** HIGH
**File:** `src/main/java/com/action/AppAPIAction.java`, lines 66–76

**Description:**
The commented-out login branch receives the `password` parameter directly from the HTTP request and passes it to `LoginDAO.checkLoginAPI(username, password)` without any evidence of hashing or encoding at the action layer. While this code is not currently executing, it represents the intended re-activation path. Credentials transmitted as plain HTTP parameters are vulnerable to interception (no TLS enforcement visible) and logging (Log4j MDC puts `sessCompId` but full request parameter logging may capture the password).

**Evidence:**
```java
////     String username = request.getParameter("username")==null?"":request.getParameter("username");
////     String password = request.getParameter("password")==null?"":request.getParameter("password");
////     LoginDAO loginDao = new LoginDAO();
////     compKey = loginDao.checkLoginAPI(username, password);
```
The `password` value flows directly from the HTTP parameter into the DAO with no transformation.

**Impact:**
If this code is re-enabled over HTTP (not HTTPS), credentials are transmitted in cleartext. Application-level request logging could also capture passwords in log files.

**Recommendation:**
Before re-enabling, verify the DAO uses a secure password comparison (bcrypt/PBKDF2, not plaintext or MD5). Enforce HTTPS at the container/load-balancer level. Ensure Log4j appenders are not configured to log raw request parameters.

---

### FINDING 5 — HIGH: No Input Validation on API Parameters in Active Code Path

**Severity:** HIGH
**File:** `src/main/java/com/action/AppAPIAction.java`, lines 42–373

**Description:**
The active (non-commented) code path performs no input validation whatsoever — because there is no active code. When and if the action logic is restored, the commented-out code shows validation only for numeric ID fields (`vehId`, `drvId`, `attId`) using `[0-9]+` regex. However, free-text fields (`loc`, `odemeter`, `ftime`, `qcoms`) have no sanitization, and the struts-config mapping declares no ActionForm (`name` attribute absent), meaning Struts form validation is entirely bypassed.

**Evidence:**
```xml
<!-- struts-config.xml lines 447–451: no form bean, no validate attribute -->
<action path="/api" scope="request" type="com.action.AppAPIAction">
    <forward name="apiXml" path="/html-jsp/apiXml.jsp"/>
</action>
```
```java
////  String loc = request.getParameter("loc")==null?"":request.getParameter("loc");
////  String odemeter = request.getParameter("odemeter")==null?"0":...
////  String[] quesComments = request.getParameterValues("qcoms");
// No sanitization of loc, odemeter, or qcoms before passing to DAO methods
```

**Impact:**
Free-text fields passed to DAO methods without validation are potential SQL injection vectors (see Finding 6) and XSS vectors in the XML response.

**Recommendation:**
Bind the `/api` action to an ActionForm with Struts validation, or implement explicit server-side input validation within the action before any DAO call. Whitelist-validate all ID fields and length-constrain all free-text fields.

---

### FINDING 6 — HIGH: Potential SQL Injection via Free-Text Parameters (Commented-Out DAO Calls)

**Severity:** HIGH
**File:** `src/main/java/com/action/AppAPIAction.java`, lines 211–319

**Description:**
The commented-out `API_RESULT` branch passes unsanitized `loc` (location string), `odemeter`, and `quesComments[]` array elements directly to `fleetcheckAction.saveResultAPP(vehId, drvId, quesIds, quesAns, quesComments, ftimet, compId, loc, odemeter)`. Without reviewing the DAO implementation, there is no indication at the action layer that these string values are parameterized before being used in SQL. The `quesComments` array is user-supplied free text with no length or character constraints.

**Evidence:**
```java
////  String loc = request.getParameter("loc")==null?"":request.getParameter("loc");
////  String odemeter = request.getParameter("odemeter")==null?"0":request.getParameter("odemeter");
////  String[] quesComments = request.getParameterValues("qcoms");
////  ...
////  resutl_id = fleetcheckAction.saveResultAPP(
////      vehId, drvId, quesIds, quesAns, quesComments, ftimet, compId, loc, odemeter);
```
`loc` and `quesComments` have no regex validation or sanitization before passing to the DAO layer.

**Impact:**
If the underlying DAO uses string concatenation to build SQL queries, an attacker could inject arbitrary SQL through the `loc` or `qcoms` parameters. As the endpoint requires no authentication (Finding 1), the attack surface is accessible to any anonymous caller once the code is re-enabled.

**Recommendation:**
Verify and enforce that all DAO methods called from this action use `PreparedStatement` with parameterized queries. Add explicit input sanitization (length limits, character whitelisting) for `loc` and comment fields at the action layer.

---

### FINDING 7 — MEDIUM: Insecure Direct Object Reference (IDOR) Risk on Vehicle/Driver/Attachment IDs

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AppAPIAction.java`, lines 82–208

**Description:**
The commented-out code validates that `vehId`, `drvId`, and `attId` are numeric (`[0-9]+`), but performs no ownership/tenancy check at the action layer. The `compKey` is used to resolve `compId`, and the DAO calls (`getAllDriver(compId, ...)`, `getAllUnit(compId, ...)`) appear to scope queries by `compId`. However, the `API_RESULT` save path passes `vehId` and `drvId` without re-validating that those IDs belong to the company identified by `compKey`. An attacker with a valid `compKey` for Company A could potentially submit results associated with vehicle IDs belonging to Company B.

**Evidence:**
```java
////  String vehId = request.getParameter("vehId")==null?"0":request.getParameter("vehId");
////  String drvId = request.getParameter("drvId")==null?"0":request.getParameter("drvId");
////  // ... numeric validation only ...
////  resutl_id = fleetcheckAction.saveResultAPP(vehId, drvId, ...compId...);
// No check: does vehId belong to compId? Does drvId belong to compId?
```

**Impact:**
Cross-tenant data pollution: results written against another company's vehicles or drivers. Potential data integrity violations in fleet check records.

**Recommendation:**
Before saving results, verify that `vehId` and `drvId` are owned by the resolved `compId`. This check should occur in the DAO or as an explicit pre-save validation step in the action.

---

### FINDING 8 — MEDIUM: XML Response Built via String Concatenation — XSS / XML Injection in apiXml.jsp

**Severity:** MEDIUM
**File:** `src/main/webapp/html-jsp/apiXml.jsp`, lines 9–102

**Description:**
The API XML response is constructed entirely via string concatenation (`resp = resp + "<rec><id>..." + value + "..."`) without XML-encoding all dynamic values. Although `questionBean.getContent()` has partial escaping for `&`, `'`, `"`, `<`, and `>`, the implementation uses `if/else if` (not `if/if`) — only the **first** matching character type is escaped. A string containing both `&` and `<` would only have `&` escaped, leaving `<` unescaped and breaking XML well-formedness or enabling XML injection. Driver names, unit names, attachment names, and `compKey` values are written with **no escaping at all**.

**Evidence:**
```java
// apiXml.jsp lines 32–34 — driver name written raw:
resp=resp+"<rec><id>"+driverBean.getId()+"</id><name>"
    + driverBean.getFirst_name()+" "+ driverBean.getLast_name()+"</name></rec>";

// apiXml.jsp lines 52–72 — question content: only first matching char is escaped:
if(content.contains("&"))      { content = content.replace("&","&amp;"); }
else if(content.contains("'")) { content = content.replace("'","&apos;"); }
// ... subsequent characters NOT escaped if first branch matched
```

**Impact:**
Malformed XML responses can crash mobile app XML parsers. A driver or vehicle name stored in the database containing XML special characters could inject arbitrary XML nodes into the response, potentially spoofing data seen by the mobile app.

**Recommendation:**
Use a proper XML serialization library (e.g., `javax.xml.stream.XMLStreamWriter` or JAXB) rather than string concatenation. Replace the `if/else if` chain in `apiXml.jsp` with a utility method that escapes all special characters unconditionally.

---

### FINDING 9 — MEDIUM: mailer.do Also Excluded from Authentication

**Severity:** MEDIUM
**File:** `src/main/java/com/actionservlet/PreFlightActionServlet.java`, line 105

**Description:**
This finding is noted as contextual information arising from reviewing the exclusion list. `mailer.do` is excluded from session authentication alongside `api.do`. This is outside the direct scope of the four audited files but is relevant context: the exclusion list contains multiple routes beyond login/logout/register, and any misconfiguration in those routes similarly bypasses the session gate.

**Evidence:**
```java
else if (path.endsWith("mailer.do")) return false;
```

**Impact:**
If `MailerAction` is exploitable (e.g., open relay, SSRF, email header injection), it is accessible without authentication.

**Recommendation:**
Review all non-authentication routes in the exclusion list (`mailer.do`, `loadbarcode.do`, `uploadfile.do`) to confirm they require no session protection. Remove any that should not be publicly accessible.

---

### FINDING 10 — LOW: AnswerBean Field Typo — `quesion_id` (Missing 't')

**Severity:** LOW
**File:** `src/main/java/com/bean/AnswerBean.java`, line 20

**Description:**
The field `quesion_id` is a misspelling of `question_id`. Lombok `@Data` generates a getter/setter named `getQuesion_id()` / `setQuesion_id()`. Any downstream code, serialization framework, or ORM column mapping that relies on the generated accessor name will perpetuate the typo, making the codebase harder to audit and maintain.

**Evidence:**
```java
// AnswerBean.java line 20:
private String quesion_id = "";
```

**Impact:**
No direct security impact. Increases maintenance burden and may cause confusion in security reviews (a reviewer might not recognize this as the question foreign key without careful examination).

**Recommendation:**
Rename to `question_id` and update all callers and column mappings.

---

### FINDING 11 — INFO: AlertBean Uses Lombok @Builder with Private Constructor — No Sensitive Fields

**Severity:** INFO
**File:** `src/main/java/com/bean/AlertBean.java`

**Description:**
`AlertBean` contains five fields: `alert_id`, `alert_name`, `alert_type`, `file_name`, `frequency`. None of these fields represent credentials, passwords, secrets, or PII beyond operational alert metadata (file name, frequency). The `@Builder` annotation is applied to a `private` constructor, which is unusual (it restricts builder usage to within the class itself or via reflection). This is a design oddity but carries no direct security implication.

**No security issues identified in AlertBean.**

---

### FINDING 12 — INFO: AnswerTypeBean Implements Serializable Without serialVersionUID Consideration

**Severity:** INFO
**File:** `src/main/java/com/bean/AnswerTypeBean.java`

**Description:**
`AnswerTypeBean` implements `Serializable` and declares an explicit `serialVersionUID = 1721165036019491023L`. The two fields (`id`, `name`) are non-sensitive. No security issues identified. The manual getter/setter pattern (vs. Lombok in sibling beans) is inconsistent but not a vulnerability.

**No security issues identified in AnswerTypeBean.**

---

### FINDING 13 — INFO: AnswerBean Implements Serializable — No Sensitive Fields

**Severity:** INFO
**File:** `src/main/java/com/bean/AnswerBean.java`

**Description:**
`AnswerBean` fields (`id`, `answer`, `faulty`, `quesion_id`, `result_id`) are inspection-result data. The `answer` field holds a checklist answer value (pass/fail/etc.), not a credential. No sensitive data exposure risk in the bean definition itself.

**No security issues identified in AnswerBean beyond the typo noted in Finding 10.**

---

## Summary Table

| # | Severity | File | Line(s) | Title |
|---|----------|------|---------|-------|
| 1 | **CRITICAL** | `PreFlightActionServlet.java` / `AppAPIAction.java` | 106 / 45–371 | api.do excluded from auth AND internal auth logic fully commented out |
| 2 | **CRITICAL** | `apiXml.jsp` | 13 | Unconditional NPE — `method` attribute never set, unhandled null dereference |
| 3 | **HIGH** | `AppAPIAction.java` | 45–373 | Entire API functionality disabled; public unauthenticated route left open |
| 4 | **HIGH** | `AppAPIAction.java` | 66–76 | Plaintext password parameter handling in commented-out login branch |
| 5 | **HIGH** | `AppAPIAction.java` / `struts-config.xml` | 42–373 / 447–451 | No input validation; no ActionForm bound; Struts validation bypassed |
| 6 | **HIGH** | `AppAPIAction.java` | 211–319 | Potential SQL injection via unsanitized `loc` and `qcoms` parameters |
| 7 | **MEDIUM** | `AppAPIAction.java` | 82–208 | IDOR — no ownership check that vehId/drvId belong to authenticated company |
| 8 | **MEDIUM** | `apiXml.jsp` | 9–102 | XML injection via string concatenation; partial/broken escaping logic |
| 9 | **MEDIUM** | `PreFlightActionServlet.java` | 105 | mailer.do also unauthenticated — broader exclusion list review needed |
| 10 | **LOW** | `AnswerBean.java` | 20 | Typo in field name `quesion_id` (missing 't') |
| 11 | INFO | `AlertBean.java` | — | No sensitive fields; @Builder on private constructor is unusual but safe |
| 12 | INFO | `AnswerTypeBean.java` | — | No sensitive fields; Serializable with explicit serialVersionUID |
| 13 | INFO | `AnswerBean.java` | — | No sensitive fields beyond typo noted in Finding 10 |

---

## Finding Count by Severity

| Severity | Count |
|----------|-------|
| CRITICAL | 2 |
| HIGH | 4 |
| MEDIUM | 3 |
| LOW | 1 |
| INFO | 3 |
| **TOTAL** | **13** |

---

## Key Conclusions

1. **api.do is a fully unauthenticated, broken endpoint.** The PreFlightActionServlet excludes it from session auth (confirmed, line 106), and the internal `compKey` authentication that was meant to replace session auth has been entirely commented out. Any anonymous HTTP request to `api.do` reaches the action.

2. **The endpoint currently throws a NullPointerException on every request** because `AppAPIAction` no longer sets the `method` request attribute, and `apiXml.jsp` dereferences it unconditionally.

3. **The three bean files (AlertBean, AnswerBean, AnswerTypeBean) contain no passwords, credentials, or sensitive PII** in their field definitions. They are clean from a sensitive-data-exposure perspective.

4. **If the commented-out API logic is ever re-enabled**, the following must be addressed before go-live: authentication enforcement (compKey validation as first gate), parameterized SQL for all DAO calls accepting free-text input, cross-tenant IDOR checks for vehicle/driver IDs, and proper XML serialization in the response JSP.
