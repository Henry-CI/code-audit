# Pass 1 Audit — FilterHandler / FleetcheckAction / FleetcheckActionForm

**Files:**
- `src/main/java/com/querybuilder/filters/FilterHandler.java`
- `src/main/java/com/action/FleetcheckAction.java`
- `src/main/java/com/actionform/FleetcheckActionForm.java`

**Date:** 2026-02-26

---

## Summary

The three files under review form the driver-facing pre-operations (fleetcheck) submission pipeline. `FilterHandler` is a clean interface that enforces parameterized query design across the query-builder subsystem. `FleetcheckActionForm` is a pure data-binding bean with no validation whatsoever. `FleetcheckAction` is the most critical file: it performs session dereference before null-guarding, has no CSRF token check, performs no ownership validation of the submitted vehicle or question IDs (IDOR), feeds unsanitized `faulttext` user input into an HTML email body, and dispatches the submission to `ResultDAO.saveResult()`, which itself contains multiple SQL injection vectors on the `question_id` value that flows through from the form. The DAO layer findings are recorded here because their root cause is the absence of validation in `FleetcheckActionForm` and `FleetcheckAction`. The `struts-config.xml` entry for `/fleetcheck` carries no `validate="true"` attribute, meaning the ActionForm's `validate()` method (which does not exist in any case) is never called.

---

## Findings

---

### CRITICAL: Null Pointer Dereference on `getSession(false)` Before Null Check

**File:** FleetcheckAction.java (line 47–48)

**Description:**
`request.getSession(false)` is called at line 47 and the result is assigned to `session`. Immediately at line 48, `session.getAttribute("sessCompId")` is called without first checking whether `session` is null. `getSession(false)` returns `null` when no session exists (e.g., after session expiry, on a direct request with no cookie, or during concurrent session invalidation). `PreFlightActionServlet` does check `sessCompId != null` but only after it already calls `session.getAttribute(...)` on a potentially null session itself (lines 56 and 62 of PreFlightActionServlet.java). A race condition between session expiry and the servlet's forward can bypass the guard. The NPE in `FleetcheckAction` would produce an unhandled 500 error, potentially leaking stack-trace information.

```java
// Line 47–48 — FleetcheckAction.java
HttpSession session = request.getSession(false);
String sessCompId = (String) (session.getAttribute("sessCompId") == null ? "" ...
//                             ^^^^^^^ session can be null here
```

**Risk:** Application crash (DoS) on session expiry; stack trace disclosure in non-production error pages; potential security-control bypass if the 500 response is not caught by the servlet filter.

**Recommendation:** Guard immediately after `getSession(false)`: `if (session == null) { return mapping.findForward("expired"); }`. Apply the same pattern to every attribute cast from session.

---

### CRITICAL: SQL Injection via `question_id` Array Elements (ResultDAO / QuestionDAO)

**File:** FleetcheckAction.java (lines 96, 104) — root cause; ResultDAO.java (lines 65, 74, 91) — exploitation site; QuestionDAO.java (lines 42, 85, 275) — additional exploitation sites

**Description:**
`FleetcheckActionForm.getId()` returns a raw `String[]` whose elements are submitted directly by the browser as HTTP request parameters (`id[]`). `FleetcheckActionForm` performs no validation on these values. `FleetcheckAction.saveResult()` passes them without transformation into `ResultDAO.saveResult()`. Inside `ResultDAO.saveResult()`, each element is used in at least three concatenated SQL strings:

```java
// ResultDAO.java line 65 — direct concatenation into Statement.executeQuery
sql = "select content from question_content where lan_id = " + lanId
    + " and question_id = " + answer.getQuesion_id();

// ResultDAO.java line 74 — injected into a PreparedStatement template string
sql = "insert into answer (...) select ?,?,?,'" + content + "',..."
    + "from question where id = ?";
// The id parameter at ps.setInt(5, Integer.parseInt(answer.getQuesion_id()))
// would throw NumberFormatException, but line 65's Statement path executes first.

// ResultDAO.java line 91 — direct concatenation
sql = "select answer_type.name from question,answer_type where question.id ="
    + answer.getQuesion_id() + " and ...";
```

An attacker who can submit a fleetcheck form can supply a value such as `1 UNION SELECT pg_read_file('/etc/passwd')--` as a question ID. Because the delete-on-error path at line 113 uses further string concatenation (`"delete from result where id = " + result_id`), a carefully crafted payload could also cause partial data corruption. The same raw-string pattern appears in `QuestionDAO.getQuesLanId` (line 42), `getQuestionByUnitId` (line 85), and `getQuestionById` (line 275), all of which are called transitively from the fleetcheck submit path.

**Risk:** Full database read (information disclosure), potential write/delete of arbitrary records, escalation to OS-level access via PostgreSQL `COPY` or `pg_read_file` if the DB user has the necessary privileges.

**Recommendation:** Validate that every element of `question_ids[]` is a positive integer before use (reject the request if any element fails). Replace every `Statement`-based concatenated query in the call chain with `PreparedStatement` using `?` placeholders.

---

### CRITICAL: SQL Injection via `veh_id` (Vehicle ID) in Multiple DAO Paths

**File:** FleetcheckAction.java (lines 74, 95) — source; ResultDAO.java (line 47), QuestionDAO.java (line 85) — exploitation sites

**Description:**
`FleetcheckActionForm.getVeh_id()` is an unvalidated string taken directly from the HTTP request. It is passed to `ResultDAO.saveResult()` where it is used as `Integer.parseInt(resultBean.getUnit_id())` at line 47 — this parse provides a weak type barrier for the `result` INSERT itself, but the same raw `veh_id` value was already passed to `QuestionDAO.getQuestionByUnitId(veh_id, att_id, sessCompId, false)` at line 78 (restart path) and similarly in the default path via `saveResult`. Inside `getQuestionByUnitId`, the value is concatenated at line 85:

```java
" where unit.id = " + unitId + " and unit.fuel_type_id = ...
    and (question.comp_id is null or question.comp_id = " + compId + ")";
```

The `attchId` value from `getAtt_id()` is concatenated at line 89 without parsing:

```java
sql += " and (attachment_id is null or attachment_id = " + attchId + ")";
```

`att_id` is never validated anywhere in the form or action.

**Risk:** Same as the question_id injection finding: arbitrary SQL execution through the forklift submit flow.

**Recommendation:** Validate `veh_id` and `att_id` as positive integers at the `FleetcheckActionForm.validate()` layer and reject the request immediately if the check fails.

---

### HIGH: No CSRF Protection on State-Changing Fleetcheck Submission

**File:** FleetcheckAction.java (lines 44–116); struts-config.xml (lines 169–177)

**Description:**
The `/fleetcheck` action accepts POST requests that write inspection results to the database (`saveResult`) and send email alerts (`sendFleetCheckAlert`, `Util.sendMail`). The `struts-config.xml` entry does not enable `validate="true"` and does not reference any CSRF token mechanism. The `FleetcheckActionForm` contains no CSRF token field. Struts 1.x has no built-in CSRF protection. A malicious page served on any origin can submit a cross-origin form POST to `/fleetcheck.do` and the server will process it using the victim's active session cookie, forging an inspection result in the victim driver's name and triggering email dispatch to company administrators.

**Risk:** Forged inspection records (audit falsification), spam/phishing via the application's mail relay, and falsification of fleetcheck compliance history for regulatory purposes.

**Recommendation:** Implement a synchronizer token: generate a random per-session token, embed it in the form as a hidden field, and verify it server-side at the start of `execute()` before any processing. Alternatively, adopt the double-submit cookie pattern or migrate to a framework with built-in CSRF support.

---

### HIGH: Insecure Direct Object Reference — No Ownership Check on Vehicle ID or Question IDs

**File:** FleetcheckAction.java (lines 74, 78, 95, 96, 104)

**Description:**
When the action processes a fleetcheck submission (both "restart" and default branches), it uses `veh_id` and `quesion_ids[]` directly from form parameters without verifying that the vehicle belongs to the authenticated company (`sessCompId`) or that the question IDs belong to the same company's question set. An authenticated driver for Company A can submit a form with `veh_id` set to a vehicle belonging to Company B, causing inspection results to be recorded against that vehicle. Similarly, question IDs from any company's checklist can be injected into the answer set.

```java
// FleetcheckAction.java line 78 — veh_id not validated against sessCompId
ArrayList<QuestionBean> arrQues = quesionDao.getQuestionByUnitId(veh_id, att_id, sessCompId, false);

// FleetcheckAction.java line 104 — saves result with arbitrary veh_id
int resutl_id = saveResult(veh_id, quesion_ids, anwsers, faulties, comment, driverId, timestamp, sessCompId);
```

Although `getQuestionByUnitId` does filter by `sessCompId` in the SQL WHERE clause, the actual `result` INSERT uses only `veh_id` (line 47 of ResultDAO) with no company-ownership JOIN. A result record can therefore be created with a `unit_id` belonging to another company.

**Risk:** Cross-tenant data pollution; falsification of inspection records for vehicles owned by other companies; compliance fraud.

**Recommendation:** Before accepting `veh_id`, query the database to confirm that the vehicle's `comp_id` matches `sessCompId`. Reject the request if the check fails with a 403.

---

### HIGH: Email Header Injection via `faulttext` User Input

**File:** FleetcheckAction.java (lines 55, 62, 68)

**Description:**
In the `faulty` branch, the user-supplied parameter `faulttext` is read from the request without any sanitization and embedded directly into the HTML email body string:

```java
// FleetcheckAction.java lines 55, 62
String faulttext = request.getParameter("faulttext") == null ? "" : request.getParameter("faulttext");
String html = "Driver:" + driverName + "<br/>Question:" + qName
            + "<br/>Time:" + currentDate + "<br/>Faulty:" + faulttext;
```

This string is then passed to `Util.sendMail(...)` as the `mBody` parameter. Inside `Util.sendMail`, the subject is set with `message.setSubject(subject)` and the recipient address `rEmail` (which comes from `comp.getEmail()` and `comp.getSubemail()`) is set via `InternetAddress.parse(rEmail, false)`. The `false` flag disables strict RFC 2822 parsing, meaning newline characters in `rEmail` would not be rejected. While `rEmail` is database-sourced and less directly attacker-controlled, `faulttext` is fully attacker-controlled and is placed in the body without HTML escaping, enabling stored XSS in any HTML email client that renders the alert and, if the mail library performs insufficient MIME boundary enforcement, potential MIME injection.

Beyond body injection, the `faulttext` value also appears as part of the `RuntimeConf.EMAIL_DIGANOSTICS_TITLE` subject line path — the subject passed is a constant, so subject injection is not present here, but the body injection and potential MIME injection remain exploitable.

**Risk:** Cross-site scripting in HTML email clients; MIME injection enabling spoofed email sections; potential phishing of company administrators who receive the faulty-item alert.

**Recommendation:** HTML-encode all user-supplied values before embedding them in an HTML email body (use `StringEscapeUtils.escapeHtml4()` or equivalent). Validate `faulttext` against a whitelist of safe characters (alphanumeric, punctuation) and enforce a maximum length.

---

### HIGH: Unsafe Array Access — `sessArrDriver.get(0)` and `sessArrComp.get(0)` Without Null or Size Checks

**File:** FleetcheckAction.java (lines 57, 61, 63–64, 71, 92, 101, 107)

**Description:**
The action unconditionally calls `.get(0)` on `sessArrDriver` and `sessArrComp` without checking whether these lists are null or non-empty. If session state is corrupted, partially set up (e.g., a user who authenticated but whose driver/company data population failed), or deliberately cleared by concurrent session manipulation, these calls throw `NullPointerException` or `IndexOutOfBoundsException`. The same pattern appears in the "faulty" branch (lines 57, 61, 63) and the default submission branch (lines 92, 101, 107).

```java
// FleetcheckAction.java line 57
String driverName = (sessArrDriver.get(0)).getFirst_name() + " " + (sessArrDriver.get(0)).getLast_name();
// sessArrDriver could be null (getAttribute returns null) or empty
```

**Risk:** Unhandled exception resulting in a 500 error and potential stack-trace disclosure; exploitable as a DoS vector by sending requests during the window between session creation and driver-data population.

**Recommendation:** Add explicit null and `isEmpty()` guards for `sessArrDriver` and `sessArrComp` immediately after retrieval from the session. Redirect to the session-expired page if either is null or empty.

---

### HIGH: SQL Injection in `SubscriptionDAO.checkCompFleetAlert` via `sessCompId`

**File:** FleetcheckAction.java (line 165) — caller; SubscriptionDAO.java (line 99) — exploitation site

**Description:**
`sendFleetCheckAlert` passes `sessCompId` (the company ID from the session) directly to `subscriptionDAO.checkCompFleetAlert(sessCompId)`. Inside that method, the value is concatenated into a SQL string without parameterization:

```java
// SubscriptionDAO.java line 99
String sql = "select name from company_subscription as c,subscription as s "
           + "where c.subscription_id = s.id and s.file_name = 'FleetcheckAlert' "
           + "and c.comp_id ='" + comId + "'";
```

Although `sessCompId` is set from the session during authentication (making it less directly attacker-controlled), if any other vulnerability allows `sessCompId` to be set to an attacker-chosen value (e.g., a session fixation or the company-switcher functionality), this becomes a direct SQL injection vector. The quoting style (`'"` + comId + `"'`) is also inconsistent with parameterization and would not handle single-quote injection.

**Risk:** SQL injection if `sessCompId` is ever attacker-influenced; information disclosure from the `company_subscription` table.

**Recommendation:** Replace concatenation with a `PreparedStatement` using `?` placeholders.

---

### MEDIUM: No `validate()` Override in FleetcheckActionForm; `validate` Not Enabled in struts-config.xml

**File:** FleetcheckActionForm.java (entire file); struts-config.xml (line 172)

**Description:**
`FleetcheckActionForm` extends `ActionForm` but does not override the `validate()` method. The `struts-config.xml` action mapping for `/fleetcheck` does not set `validate="true"` (the attribute is absent, which in Struts 1.x defaults to `true` for form validation only when `validate` is explicitly set and an `input` path is defined — however, without an `input` attribute in this mapping, no validation redirect would occur even if `validate()` were overridden). As a consequence, no server-side input validation is performed on any of the following fields before they reach action logic: `id[]` (question IDs), `answer[]`, `faulty[]`, `comment`, `veh_id`, `att_id`, `hourmeter`. All fields that eventually reach SQL are completely unvalidated at the form layer.

**Risk:** Amplifies every SQL injection and IDOR finding above; comment and faulty fields accept arbitrary length input that could overflow database column limits.

**Recommendation:** Override `validate()` in `FleetcheckActionForm` to enforce: `veh_id` and `att_id` are positive integers; each element of `id[]` is a positive integer; `answer[]` and `faulty[]` lengths match `id[]` length; `comment` and `hourmeter` are bounded in length. Add `validate="true"` and an `input` path to the struts-config mapping.

---

### MEDIUM: Array Length Mismatch Between `quesion_ids`, `anwsers`, and `faulties` Not Checked

**File:** FleetcheckAction.java (lines 96–98, 122–129)

**Description:**
The `saveResult` method iterates over `quesion_ids` (length N) and unconditionally accesses `anwsers[i]` and `faulties[i]` at the same index:

```java
// FleetcheckAction.java lines 122–129
for (int i = 0; i < quesion_ids.length; i++) {
    answerBean.setAnswer(anwsers[i]);       // ArrayIndexOutOfBoundsException if anwsers.length < quesion_ids.length
    answerBean.setQuesion_id(quesion_ids[i]);
    if (faulties != null) {
        answerBean.setFaulty(faulties[i]);  // ArrayIndexOutOfBoundsException if faulties.length < quesion_ids.length
    }
}
```

A browser (or attacker) that submits fewer `answer[]` values than `id[]` values will cause an `ArrayIndexOutOfBoundsException` at line 124, which propagates as an unhandled exception up through the Struts dispatcher.

**Risk:** Application crash (DoS); unhandled exception potentially exposing stack trace; inconsistent partial data writes to the database before the exception is thrown.

**Recommendation:** Validate before the loop that `anwsers != null && anwsers.length == quesion_ids.length`. If `faulties != null`, validate `faulties.length == quesion_ids.length`. Reject the request with an error forward if the check fails.

---

### MEDIUM: `saveResultBarcode` Accepts `driverId` as Unsanitized String with `Long.parseLong` Only

**File:** FleetcheckAction.java (lines 142–160)

**Description:**
`saveResultBarcode` is a public method that takes `driverId` as a raw `String` and calls `Long.parseLong(driverId)` at line 152. While the parse provides a type barrier against non-numeric injection, the method accepts `veh_id` and `comment` as strings that flow into `ResultDAO.saveResult()` using the same concatenated SQL paths identified above. Additionally, `driverId` here bypasses the session-derived driver ID used in the main `execute()` path, meaning if this method is ever called from a different entry point with user-controlled input, it constitutes an IDOR on the driver ID.

**Risk:** If called from an exposed endpoint with user-controlled `driverId`, results can be attributed to any driver; chained with SQL injection via `veh_id`.

**Recommendation:** This method should derive the driver ID from the authenticated session rather than accepting it as a parameter. Validate and sanitize `veh_id` and `comment` before passing them to the DAO.

---

### MEDIUM: Unescaped User Data Rendered in HTML Email Body (Stored XSS in Email)

**File:** FleetcheckAction.java (lines 62, 68) and FleetCheckAlert.java (lines 140–155)

**Description:**
In the "faulty" branch, `faulttext` (attacker-controlled) and `qName` (from the database, but the question content itself can be attacker-influenced if an admin input contained HTML) are concatenated raw into the HTML email body. In `FleetCheckAlert.setContent()`, `driverName`, `unitName`, `status`, `failures`, `comment`, `location`, and `odemeter` are all interpolated directly into HTML table cells without escaping:

```java
// FleetCheckAlert.java lines 141–155
html += "<td align='center'><strong>"+driverName+"</strong></td>";
html += "<td>"+unitName+"</td>" + "<td>"+resultBean.getTime()+"</td>" ...
        "<td width='30%'>"+failures+"</td>" + "<td>"+comment+"</td>";
```

Any of these values that contain `<script>`, `<img onerror=...>`, or similar payloads will be rendered as active HTML in the email client of any alert recipient.

**Risk:** XSS in the email clients of company administrators; potential credential harvesting or social engineering via crafted alert emails.

**Recommendation:** Apply HTML escaping to all database-sourced and user-supplied values before interpolation into HTML strings.

---

### LOW: `FilterHandler` Interface — Design Assessment (Informational with Low-Severity Note)

**File:** FilterHandler.java (lines 1–11)

**Description:**
`FilterHandler` is a well-designed Java interface (not an abstract class) with two methods: `getQueryFilter()` returning a SQL fragment string, and `prepareStatement(StatementPreparer preparer)` accepting a `StatementPreparer` wrapper around `PreparedStatement`. This design enforces a separation between the SQL fragment construction and the bind-parameter population, which is the correct pattern for parameterized queries. The `StatementPreparer` helper class correctly uses indexed `setXxx()` calls on the underlying `PreparedStatement`.

The low-severity note is that `getQueryFilter()` returns a raw `String` — implementations could return fragments containing concatenated values rather than only `?` placeholders. There is no enforcement mechanism at the interface level to prevent a careless implementation from returning a non-parameterized fragment. The interface design relies entirely on the discipline of implementors.

**Risk:** Low. Any `FilterHandler` implementation that embeds user data in the string returned by `getQueryFilter()` instead of using `?` and `prepareStatement()` would introduce SQL injection. A code review of all implementations is warranted.

**Recommendation:** Document in the interface Javadoc that `getQueryFilter()` MUST return only SQL fragments using `?` placeholders and that all values MUST be bound via `prepareStatement()`. Audit all implementing classes.

---

### LOW: No Role-Based Authorization Check in FleetcheckAction

**File:** FleetcheckAction.java (lines 47–115)

**Description:**
The action relies entirely on `PreFlightActionServlet`'s check that `sessCompId != null`. There is no role check within `FleetcheckAction` itself — any authenticated session with a valid `sessCompId` can submit a fleetcheck result, trigger email alerts, or invoke the "faulty" notification branch. The audit context notes that a `role` attribute may exist in the session; if so, it is not consulted here. An account that should only have read-only or reporting access can submit fleetcheck results.

**Risk:** Privilege escalation within the authenticated user population; inappropriate submission of fleetcheck data by non-driver roles.

**Recommendation:** Check the session role attribute at the start of `execute()` and verify that the caller has the driver or equivalent role before processing any branch.

---

### LOW: Weak Password Generation Using `java.util.Random` and MD5 in `Util.genPass`

**File:** Util.java (lines 159–175)

**Description:**
`Util.genPass()` uses `java.util.Random` (a non-cryptographically-secure PRNG) seeded implicitly, and MD5 (a cryptographically broken hash function) to generate passwords. While this method is not called within the three primary files under audit, it is used by other actions in the application and is in the same `Util` class reviewed in this audit.

**Risk:** Generated passwords are predictable given knowledge of the PRNG state; MD5 provides no collision resistance guarantees.

**Recommendation:** Replace `java.util.Random` with `java.security.SecureRandom` and replace MD5 with SHA-256 or use `SecureRandom.nextBytes()` with Base64 encoding directly.

---

### INFO: `Util.sendMail` Uses `InternetAddress.parse(rEmail, false)` — Lenient Parsing

**File:** Util.java (lines 47–51, 88–90)

**Description:**
Both `sendMail` overloads call `InternetAddress.parse(rEmail, false)`. The `false` flag disables strict RFC 2822 address validation, meaning malformed or injected addresses (e.g., containing newlines) may be silently accepted or ignored rather than causing an exception. This is directly relevant to the email injection risk noted for `FleetcheckAction`, where `rEmail` is assembled by concatenating multiple database-sourced email fields with commas.

**Risk:** Low in isolation; amplifies the email injection risk identified in FleetcheckAction.

**Recommendation:** Use `InternetAddress.parse(rEmail, true)` to enable strict validation, and validate each component email address individually before concatenation.

---

### INFO: SQL Logged at INFO Level Before Execution (Potential Log Injection / Data Exposure)

**File:** ResultDAO.java (lines 35, 52, 65, 83, 91, 98); QuestionDAO.java (lines 42, 85, 96, 275)

**Description:**
Every SQL string, including those containing concatenated user-supplied values, is logged at `log.info(sql)` immediately before execution. If an attacker can inject newline characters or log-forging sequences into `veh_id`, `question_id`, or `comment`, they can forge log entries. Additionally, if logs are accessible to other tenants or stored insecurely, this leaks SQL structure and data values.

**Risk:** Log injection (forged audit trails); sensitive data exposure in log files.

**Recommendation:** Log only the SQL template (not the interpolated string with user data). If values must be logged for debugging, use a log level below INFO (DEBUG or TRACE) and ensure log files are access-controlled.

---

## Finding Count

- CRITICAL: 3
- HIGH: 5
- MEDIUM: 4
- LOW: 3
- INFO: 2
