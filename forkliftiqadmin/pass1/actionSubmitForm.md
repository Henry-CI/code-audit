# A02 — actionSubmitForm.java
**Path:** src/main/java/com/util/actionSubmitForm.java
**Auditor:** A02
**Date:** 2026-02-26
**Branch:** master

---

## Reading Evidence

### Fully Qualified Class Name
`com.util.actionSubmitForm`

### Class Extended / Interface Implemented
| Line | Relationship | Type |
|------|-------------|------|
| 8 | extends | `org.apache.struts.taglib.html.FormTag` |

No interfaces are directly implemented in this source file; any interface implementations are inherited through `FormTag`.

### Class-Level Annotations
None. No annotations are present at class level.

### Fields
| Line | Access Modifier | Type | Name | Notes |
|------|----------------|------|------|-------|
| 9 | `private static` | `org.apache.log4j.Logger` | `log` | Initialised via `InfoLogger.getLogger("com.util.actionSubmitForm")` |

### Public Methods
None. The class defines no public methods of its own.

### Protected Methods
| Line | Return Type | Name | Parameters | Annotations |
|------|------------|------|-----------|-------------|
| 11 | `String` | `renderFormStartElement` | (none) | None |

This method overrides the parent `FormTag.renderFormStartElement()`.

### Method-Level Annotations
None.

### Constants
None.

### Additional Observations
- The source file is 37 lines total.
- Line 7 comment: `//Currently Unused because of introduce of watermaker jquery lib` — the class is flagged dead code by the original author.
- The class resides in package `com.util`, which is a Struts 1.x tag library extension, not a Spring component.
- Imports: `javax.servlet.jsp.JspException`, `org.apache.log4j.Logger`.
- `InfoLogger` is a custom logging wrapper used at lines 9 and 19.

---

## Findings

### Finding 1 — MEDIUM: Swallowed Exception with No Re-throw or Error Propagation

**Severity:** MEDIUM

**Description:**
Inside `renderFormStartElement()`, the call to `renderName(results)` is wrapped in a `try/catch` block that catches `JspException` but only logs it — no exception is re-thrown, no error flag is set, and `null` or empty form-name rendering is silently accepted. In JSP tag lifecycle code, failing to propagate a `JspException` can result in a malformed HTML form being rendered to the client without any indication that something went wrong. This can mask rendering errors and in adversarial scenarios might contribute to unexpected behaviour in downstream form processing.

**File:** `src/main/java/com/util/actionSubmitForm.java`
**Lines:** 15–20

**Evidence:**
```java
try {
    renderName(results);
} catch (JspException e) {
    // TODO Auto-generated catch block
    InfoLogger.logException(log, e);
}
```

**Recommendation:**
Re-throw the `JspException` (it is a checked exception declared on the parent method signature) so the tag lifecycle can handle the error properly, or at minimum set a flag and return an empty/safe form element instead of continuing to build a potentially broken HTML fragment. Remove the `// TODO Auto-generated catch block` comment — it indicates this handler was never reviewed after scaffolding.

---

### Finding 2 — LOW: Dead Code Committed to Repository

**Severity:** LOW

**Description:**
The class-level comment at line 7 explicitly states this class is "Currently Unused because of introduce of watermaker jquery lib." Dead code left in a production repository increases the attack surface (it may be inadvertently re-enabled in a future refactor), makes auditing harder, and can create confusion about which code paths are actually active.

**File:** `src/main/java/com/util/actionSubmitForm.java`
**Line:** 7

**Evidence:**
```java
//Currently Unused because of introduce of watermaker jquery lib
public class actionSubmitForm extends org.apache.struts.taglib.html.FormTag {
```

**Recommendation:**
Remove the class from the codebase if it is genuinely unused. If retention is required for historical reference, remove it from the compile scope and track the removal in the version control history.

---

### Finding 3 — LOW: Hardcoded JavaScript Function Name in Form Output

**Severity:** LOW

**Description:**
The `renderFormStartElement()` method writes the string `onsubmit='clearPlaceholders(this);'` directly into the rendered HTML form element. This is a hardcoded JavaScript hook that cannot be configured or overridden by the tag's callers. If a form using this tag does not have a `clearPlaceholders` function defined in scope, the form submission will fail silently or throw a JavaScript error. More relevantly from a security standpoint, this pattern prevents any per-usage customisation of the `onsubmit` attribute and also hard-codes client-side behaviour in a server-side tag — making it harder to audit what client-side validation is or is not occurring.

**File:** `src/main/java/com/util/actionSubmitForm.java`
**Line:** 13

**Evidence:**
```java
StringBuffer results = new StringBuffer("<form onsubmit='clearPlaceholders(this);'");
```

**Recommendation:**
Note that the parent `FormTag` provides a `getOnsubmit()` / `setOnsubmit()` accessor pair (the commented-out line 27 shows it was intentionally suppressed). The custom `onsubmit` override should either delegate to the parent accessor with a fallback, or document explicitly why the attribute is unconditionally replaced. This is of low security impact in isolation but demonstrates missing input channel design.

---

### Finding 4 — INFO: Non-standard Naming Convention (Class Name)

**Severity:** INFO

**Description:**
The class is named `actionSubmitForm`, violating Java naming conventions (class names must begin with an uppercase letter by convention). While not a direct security vulnerability, non-standard naming can impede code review, static analysis tooling configuration, and automated security scanning that may key on conventional naming patterns.

**File:** `src/main/java/com/util/actionSubmitForm.java`
**Line:** 8

**Evidence:**
```java
public class actionSubmitForm extends org.apache.struts.taglib.html.FormTag {
```

**Recommendation:**
Rename to `ActionSubmitForm` in line with Java conventions, updating all Struts configuration (struts-config.xml) references accordingly.

---

### Finding 5 — INFO: Struts 1.x Framework (Legacy/End-of-Life)

**Severity:** INFO

**Description:**
This file extends `org.apache.struts.taglib.html.FormTag`, confirming the application uses Struts 1.x. Struts 1 reached end-of-life in 2013. It has received no security patches since then and has known unaddressed CVEs. This is a framework-level finding (not specific to this file) but is evidenced here.

**File:** `src/main/java/com/util/actionSubmitForm.java`
**Line:** 8

**Evidence:**
```java
public class actionSubmitForm extends org.apache.struts.taglib.html.FormTag {
```

**Recommendation:**
Plan migration away from Struts 1.x. In the interim, ensure the Struts 1.x JAR version in use is the latest available (1.3.10) and that the deployment environment compensates for known framework-level issues via WAF rules or container-level controls.

---

## Checklist Coverage

### 1. Secrets and Configuration
**Result: No findings.**
No hardcoded credentials, API keys, database connection strings, internal URLs, or Azure secrets are present in this file. The only string literals are the HTML/JavaScript form fragment at line 13 and the logger category name at line 9.

### 2. Authentication and Authorization
**Result: No findings (not applicable to this class).**
This class is a JSP tag library extension, not a controller or filter. It does not perform authentication or authorisation checks. No session interrogation, role checking, or access gating is present. This is expected for a tag rendering utility; auth enforcement must be verified elsewhere (Struts action configuration, filters).

### 3. Input Validation and Injection
**Result: No direct injection findings; design note raised.**

- **SQL injection:** No SQL queries, JdbcTemplate calls, or JDBC operations of any kind. Not applicable.
- **validate() method:** This class does not implement `ActionForm` and has no `validate()` method. Not applicable.
- **Command injection:** No `Runtime.exec()` or `ProcessBuilder` usage. Not applicable.
- **Path traversal:** No file operations. Not applicable.
- **Deserialization:** No `ObjectInputStream.readObject()` usage. Not applicable.
- **Hardcoded JavaScript:** Finding 3 (LOW) raised for the unconditional `onsubmit` hook.
- **Exception swallowing:** Finding 1 (MEDIUM) raised — swallowed `JspException` can mask rendering errors.

### 4. Session and CSRF
**Result: No findings (not applicable to this class).**
This class renders a `<form>` HTML element. It does not manage sessions and does not interact with CSRF tokens. CSRF token injection (the standard Struts token mechanism) is not handled here — this must be verified at the action and JSP template level. No CORS configuration is present.

### 5. Data Exposure
**Result: No findings.**
No operator PII, forklift telemetry data, site identifiers, or other sensitive domain data is referenced or logged in this file. The logger at line 9 is defined but only used at line 19 to log a caught `JspException` — no sensitive data is included in that log call.

### 6. Dependencies
**Result: Not applicable to this source file.**
Dependency version analysis is covered at `pom.xml` level. Note that the use of Struts 1.x (end-of-life) is flagged as Finding 5 (INFO) as it is directly evidenced by this file's import/extends.

### 7. Build and CI
**Result: Not applicable to this source file.**
Build and CI pipeline review is out of scope for an individual Java source file.
