# Pass 1 Audit — driver_job_details.jsp / DyanmicBeanDAO / DynamicBean / EmailSubscriptionBean

**Files:**
- `src/main/webapp/html-jsp/vehicle/driver_job_details.jsp`
- `src/main/java/com/dao/DyanmicBeanDAO.java`
- `src/main/java/com/bean/DynamicBean.java`
- `src/main/java/com/bean/EmailSubscriptionBean.java`

**Date:** 2026-02-26

---

## Summary

Four files were audited as part of Pass 1. The JSP (`driver_job_details.jsp`) presents the most immediate risk: raw, unescaped request parameters are interpolated directly into `<html:hidden>` field `value` attributes and into `<html:form>` markup without a Struts token check, exposing the page to reflected XSS and CSRF. The DAO (`DyanmicBeanDAO.java`) executes a hard-coded, parameterless SQL query using a `Statement` object; because it accepts no external input that query is not currently injectable, but the use of `Statement` rather than `PreparedStatement` is a structural weakness that represents ongoing risk if the query is ever extended. The `DynamicBean` class is `Serializable` without a declared `serialVersionUID` and carries a field called `value` whose semantics are opaque — context-dependent risk. `EmailSubscriptionBean` uses Lombok `@Data`, which auto-generates a `toString()` that will emit all four e-mail address fields and the `op_code` field; if any log or error handler calls `toString()` on this object PII (e-mail addresses) will appear in logs. No Lombok-generated `serialVersionUID` is present despite the class participating in the Lombok builder pattern with `@NoArgsConstructor`/`@Builder`, meaning future serialization is fragile.

---

## Findings

### HIGH: Reflected XSS via Unescaped Request Parameters in Hidden Field Values

**File:** `driver_job_details.jsp` (lines 48–49)

**Description:**
The scriptlet block at the top of the page (lines 3–5) reads `equipId` and `job_id` directly from the request without any sanitisation:

```jsp
String id     = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
String jobId  = request.getParameter("job_id")  == null ? "" : request.getParameter("job_id");
```

These raw Java strings are then interpolated unescaped into `<html:hidden>` `value` attributes via JSP scriptlet expressions:

```jsp
<html:hidden property="jobId"   value="<%=jobId %>" >  <!-- line 48 -->
<html:hidden property="equipId" value="<%=id %>"    >  <!-- line 49 -->
```

In Struts 1.x the `<html:hidden>` tag HTML-encodes its `value` attribute during rendering, which mitigates the straightforward `"` injection into the attribute itself. However, the value is stored in the Struts `ActionForm` and may be echoed back to other views or propagated to JavaScript variables without encoding. More critically, the pattern establishes a precedent of putting raw parameter values into form fields. If any future developer copies this pattern with a tag that does not encode (e.g., `<html:text>`, raw scriptlet `<input value="<%=id%>">`), it becomes a direct XSS vector. The current risk is elevated because the scriptlet approach bypasses any framework-level input handling.

**Risk:**
An attacker can craft a URL such as:
```
driverjobreq.do?equipId="><script>alert(1)</script>&job_id=1
```
If the hidden-field value is ever reproduced in a non-encoding context (another JSP, an error page, a log viewer), stored XSS or reflected XSS results. The immediate reflected risk is moderate due to Struts encoding of `value`, but the structural pattern is HIGH risk.

**Recommendation:**
Replace the raw scriptlet expressions with JSTL-encoded values. Bind request parameters to the `ActionForm` through the Struts framework rather than directly injecting them as scriptlet strings. If direct injection is unavoidable, wrap with `org.apache.commons.lang.StringEscapeUtils.escapeHtml()` before passing to the tag. Do not use scriptlet expressions (`<%= %>`) for any user-controlled data.

---

### HIGH: CSRF — No Synchronizer Token on State-Changing Form

**File:** `driver_job_details.jsp` (line 14)

**Description:**
The form submits to `driverjobreq.do` via HTTP POST and assigns a driver to a job:

```jsp
<html:form method="post" action="driverjobreq.do" styleClass="ajax_mode_c assign_driver">
```

There is no Struts synchronizer token tag (`<html:resubmit>` / `saveToken` / `isTokenValid`) present anywhere in the form. The `action` field is hard-coded to `assign_driver` (line 50). Any authenticated user who is tricked into loading a crafted page will silently assign a driver to an arbitrary job on their behalf.

**Risk:**
An attacker who knows valid `equipId` and `job_id` values (obtainable via the application's own listing pages) can forge a cross-site POST request that assigns a driver of the attacker's choosing to any job, causing operational disruption in the fleet-management workflow.

**Recommendation:**
Add `saveToken(request)` in the `Action` class that renders this JSP, and validate with `isTokenValid(request)` (and `resetToken(request)`) in the `Action` class that processes the POST. Add `<html:hidden property="org.apache.struts.taglib.html.TOKEN"/>` to the form, or use the standard `<html:form>` token mechanism.

---

### MEDIUM: Unescaped Scriptlet Variable `action` Read from Request but Not Used in Output (Dead Code / Latent XSS)

**File:** `driver_job_details.jsp` (line 3)

**Description:**
A third request parameter, `action`, is read into a scriptlet variable:

```jsp
String action = request.getParameter("action") == null ? "" : request.getParameter("action");
```

This variable is not used anywhere visible in the current file's output. However, its presence as a raw, unsanitised string variable in the JSP scope means any future developer who references `<%=action%>` or passes it to JavaScript will introduce a direct XSS vulnerability without realising the value is attacker-controlled.

**Risk:**
Medium — not currently exploitable in isolation, but represents latent XSS risk and indicates a pattern of reading request parameters into unencoded scriptlet variables.

**Recommendation:**
Remove unused scriptlet variables. If `action` is needed, bind it through the `ActionForm` or escape it before use. Add a note in code review checklists that all `request.getParameter()` values are untrusted.

---

### MEDIUM: Missing CSRF Protection — JavaScript `fnAssign()` Submits Form Without Token Validation

**File:** `driver_job_details.jsp` (lines 108–119)

**Description:**
The "Assign" button does not use a standard `<input type="submit">` inside the form; instead it calls a JavaScript function:

```javascript
fnAssign = function(){
    $("#jobTitle").val($('.modal:nth-last-child(2) [name="name"]').val());
    $("#description").val($('.modal:nth-last-child(2) [name="description"]').val());
    $("#drivrId").val($("#name option:selected").val());
    $('.assign_driver').submit();
}
```

The variable `fnAssign` is declared without `var`/`let`/`const`, making it an implicit global. This means any other script on the page (e.g., a script injected via XSS in a parent frame or via a third-party library) can call `fnAssign()` to trigger a form submission. Combined with the missing CSRF token, this increases the attack surface.

**Risk:**
Medium — the implicit global declaration allows cross-frame/cross-script invocation of the submit function; amplifies the CSRF risk already noted above.

**Recommendation:**
Declare `fnAssign` with `const` or `var` to limit its scope. Move the function inside the `$(document).ready()` block. The underlying CSRF issue must also be addressed (see finding above).

---

### MEDIUM: `DynamicBean` Implements `Serializable` Without `serialVersionUID` and With a Generic `value` Field

**File:** `DynamicBean.java` (lines 5–30)

**Description:**
`DynamicBean` implements `Serializable` but does not declare a `serialVersionUID`:

```java
public class DynamicBean implements Serializable {
    String name  = "";
    String type  = "";
    String value = "";
    ...
}
```

Without a `serialVersionUID`, the JVM auto-generates one based on class structure. Any change to the class (adding a field, renaming a method) will silently change the ID and cause `InvalidClassException` when deserialising previously serialised objects — for example, those stored in HTTP sessions or a distributed cache.

Additionally, the field `value` is semantically opaque. If `DynamicBean` is used to carry configuration values (suggested by the DAO query `select name, type, value from dynamicbean`), and if `type` can be used to trigger behaviour (e.g., `type = "password"`), then deserialising a maliciously crafted `DynamicBean` from an untrusted source could produce unexpected application behaviour.

**Risk:**
Medium — serialisation stability issue is certain; the `value`/`type` semantic risk is context-dependent and requires tracing all callers.

**Recommendation:**
Add `private static final long serialVersionUID = 1L;`. Review all callers of `DynamicBean` to determine whether `value` can ever contain credentials or sensitive configuration. If so, add a `transient` modifier to `value` or document its sensitivity.

---

### MEDIUM: `EmailSubscriptionBean` — Lombok `@Data` Generates `toString()` That Emits PII (E-mail Addresses)

**File:** `EmailSubscriptionBean.java` (lines 7–28)

**Description:**
The class is annotated with `@Data`, which Lombok expands to generate `toString()`, `equals()`, `hashCode()`, and all getters/setters. The generated `toString()` will produce output of the form:

```
EmailSubscriptionBean(id=42, driver_id=7, email_addr1=user@example.com, email_addr2=..., email_addr3=..., email_addr4=..., op_code=...)
```

Any exception handler, logging framework, or debug statement that calls `toString()` on this object (or that logs it implicitly, e.g., `log.debug("bean: " + bean)`) will write up to four e-mail addresses and an `op_code` into log files. Depending on jurisdiction, logging e-mail addresses without necessity may violate GDPR Article 5(1)(c) (data minimisation) and Article 32 (security of processing).

**Risk:**
Medium — PII leakage into logs; potential regulatory exposure; `op_code` leakage may have operational security implications if it encodes driver operation codes.

**Recommendation:**
Override `toString()` explicitly (or use `@ToString(exclude = {"email_addr1","email_addr2","email_addr3","email_addr4","op_code"})`) to prevent PII from appearing in logs. Alternatively, replace `@Data` with individual Lombok annotations (`@Getter`, `@Setter`, `@EqualsAndHashCode`) and write a manual `toString()` that omits sensitive fields.

---

### LOW: `DyanmicBeanDAO` Uses `Statement` Instead of `PreparedStatement`

**File:** `DyanmicBeanDAO.java` (lines 24, 32–37)

**Description:**
The DAO creates a plain `Statement` object:

```java
Statement stmt = null;
...
stmt = conn.createStatement(ResultSet.TYPE_SCROLL_SENSITIVE, ResultSet.CONCUR_READ_ONLY);
String sql = "select name, type, value from dynamicbean";
rs = stmt.executeQuery(sql);
```

The current SQL string is fully hard-coded and accepts no external input, so there is no SQL injection in this specific method as written. However, using `Statement` rather than `PreparedStatement` is structurally unsafe: if the query is ever extended to include a filter clause derived from user or application input, the developer may follow the existing pattern and concatenate directly into the string, introducing SQL injection. `PreparedStatement` also benefits from query plan caching.

The use of `ResultSet.TYPE_SCROLL_SENSITIVE` is notable: this cursor type holds a server-side lock and is significantly more resource-intensive than `TYPE_FORWARD_ONLY`. For a simple full-table scan, it is unnecessary.

**Risk:**
Low (current) — no injection path exists today; structural risk is elevated if the query is extended. `TYPE_SCROLL_SENSITIVE` may cause performance and locking issues under load.

**Recommendation:**
Replace `Statement` with `PreparedStatement` even for parameterless queries, to establish the correct pattern and enable query plan caching. Change the cursor type to `ResultSet.TYPE_FORWARD_ONLY` unless scroll capability is genuinely required.

---

### LOW: `DyanmicBeanDAO` — SQL Query Logged at INFO Level

**File:** `DyanmicBeanDAO.java` (line 36)

**Description:**
The full SQL string is written to the application log at INFO level:

```java
log.info(sql);
```

For this particular static query the risk is minimal. However, the pattern of logging SQL at INFO means that if the query is ever extended to include query parameters (user IDs, filter values), those values will appear verbatim in the application log, potentially logging PII or sensitive identifiers.

**Risk:**
Low — establishes a logging pattern that becomes a PII/data-exposure risk if the query is parameterised in future.

**Recommendation:**
Log SQL at DEBUG level rather than INFO. If parameters are ever added, log only the query template (not the bound values), or use a sanitised representation.

---

### LOW: `EmailSubscriptionBean` Missing `serialVersionUID` Despite Being a Potential Session/Cache Candidate

**File:** `EmailSubscriptionBean.java` (lines 7–9)

**Description:**
`EmailSubscriptionBean` does not implement `Serializable` explicitly, so there is no `serialVersionUID` concern at the language level. However, with `@Data` and `@Builder`, the class is frequently placed into HTTP sessions, caches, or queues by Struts/Spring applications, all of which may require serialisation. If the class is ever placed into a `HttpSession` and the container performs session persistence/replication, serialisation will fail silently or throw a runtime error.

**Risk:**
Low — no immediate exploit, but a latent runtime stability issue if the bean is used in a distributed or persistent session context.

**Recommendation:**
If session storage or caching is anticipated, add `implements Serializable` and declare `private static final long serialVersionUID = 1L;`.

---

### INFO: Typo in Class Name `DyanmicBeanDAO` (Should Be `DynamicBeanDAO`)

**File:** `DyanmicBeanDAO.java` (line 16)

**Description:**
The class is named `DyanmicBeanDAO` instead of `DynamicBeanDAO`. This is a naming inconsistency that could cause confusion during code review and maintenance. The corresponding bean class is correctly named `DynamicBean`.

**Risk:**
Informational — no security impact; maintenance and readability concern.

**Recommendation:**
Rename the class to `DynamicBeanDAO` and update all references. Ensure the rename is done in a single refactoring commit to avoid broken references.

---

### INFO: Dead/Copied JavaScript (`fnsubmitAccount`) Unrelated to Driver Job Assignment

**File:** `driver_job_details.jsp` (lines 85–106)

**Description:**
The function `fnsubmitAccount()` references `adminRegActionForm`, `pin`, `cpassword`, `name`, and `email` — fields that do not exist in the driver job assignment form on this page. This function is never called from within this file. It appears to have been copied from a registration or admin form and not removed.

**Risk:**
Informational — no direct security impact, but dead code increases the attack surface for confused-deputy issues and makes the page harder to audit.

**Recommendation:**
Remove `fnsubmitAccount()` from this JSP. If it is genuinely needed elsewhere, it belongs in a shared JavaScript file, not in this page.

---

## Finding Count

| Severity | Count |
|----------|-------|
| CRITICAL | 0     |
| HIGH     | 2     |
| MEDIUM   | 4     |
| LOW      | 3     |
| INFO     | 2     |
| **Total**| **11**|
