# Pass 1 Audit — DriverJobDetailsAction / DriverJobDetailsActionForm

**Files:**
- `src/main/java/com/action/DriverJobDetailsAction.java`
- `src/main/java/com/actionform/DriverJobDetailsActionForm.java`
- `src/main/java/com/dao/JobsDAO.java` (referenced for SQL analysis)

**Date:** 2026-02-26

---

## Summary

`DriverJobDetailsAction` handles three sub-actions (`details`, `assign`, `assign_driver`) that expose job details and driver assignment functionality. The action reads `equipId` and `job_no` directly from request parameters without any validation against the session company, creating a textbook Insecure Direct Object Reference (IDOR) vulnerability. The `details` sub-action passes both raw parameters directly into a SQL query constructed with string concatenation in `JobsDAO.getJobListByJobId`, producing a critical SQL injection vulnerability. No CSRF protection exists on the state-changing `assign_driver` sub-action. The `DriverJobDetailsActionForm` is a plain data-transfer object with no `validate()` override, providing zero input validation. Two dead-code logic bugs also exist that cause the action routing to silently malfunction.

---

## Findings

### CRITICAL: SQL Injection via equipId and job_no in getJobListByJobId

**File:** `DriverJobDetailsAction.java` (line 52) / `JobsDAO.java` (line 123)

**Description:**
The `details` sub-action passes the raw, user-controlled request parameters `equipId` and `job_no` directly to `JobsDAO.getJobListByJobId()`:

```java
// DriverJobDetailsAction.java line 37-38, 52
String equipId = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
String jobNo   = request.getParameter("job_no")  == null ? "" : request.getParameter("job_no");
...
ArrayList<JobDetailsBean> jobs = jobsDAO.getJobListByJobId(equipId, jobNo);
```

Inside the DAO, these values are concatenated directly into a SQL string executed via a `Statement` (not a `PreparedStatement`):

```java
// JobsDAO.java line 123
String sql = "select j.id, j.unit_id, ja.driver_id, j.description, ..."
           + " and j.unit_id = " + equipId
           + " and j.job_no = '" + jobNo + "'"
           + " order by js.start_time";
stmt = conn.createStatement(...);
rs   = stmt.executeQuery(sql);
```

`equipId` is injected numerically (no quotes), making it trivially exploitable for UNION-based or error-based injection. `jobNo` is injected inside single quotes, exploitable with standard single-quote escaping. An attacker can dump arbitrary tables, modify data, or (depending on the database user's privileges) execute OS-level commands.

**Risk:** Complete database compromise. An unauthenticated user (or any authenticated user) can read all data from all tables, modify records, and potentially escalate to the underlying operating system.

**Recommendation:** Replace the `Statement` with a `PreparedStatement` using positional parameters. Validate that `equipId` is a non-negative integer before calling the DAO. Enforce the scope check described in the IDOR finding so that even a valid value is restricted to the session company.

---

### HIGH: IDOR — Job Details Not Scoped to Session Company

**File:** `DriverJobDetailsAction.java` (lines 37-38, 52)

**Description:**
The `details` sub-action retrieves job records using only `equipId` and `job_no`, both of which come directly from request parameters. There is no check that the requested `equipId` belongs to the company identified by `sessCompId`. Any authenticated user from any company can supply an arbitrary `equipId` and `job_no` to read job details belonging to a different company:

```java
String sessCompId = (String) session.getAttribute("sessCompId") == null ? ""
                  : (String) session.getAttribute("sessCompId");
// sessCompId is never passed to getJobListByJobId
ArrayList<JobDetailsBean> jobs = jobsDAO.getJobListByJobId(equipId, jobNo);
```

The SQL query in `JobsDAO` has no `company_id` predicate. Combined with the SQL injection finding, even the implicit ownership barrier is absent.

**Risk:** Horizontal privilege escalation. A user at Company A can read all job history for any unit belonging to any other company by enumerating `equipId` values.

**Recommendation:** Pass `sessCompId` to the DAO and add a `WHERE company_id = ?` predicate (via `PreparedStatement`). Return an authorization error if no matching rows are found for the given company.

---

### HIGH: IDOR — assign_driver Sub-Action Not Scoped to Session Company

**File:** `DriverJobDetailsAction.java` (lines 61-66)

**Description:**
The `assign_driver` sub-action represents a state-changing operation (assigning a driver to a job). It logs `form.getJobTitle()` and retrieves a driver list scoped to `sessCompId`, but it never validates that the job being modified (`equipId`, `jobNo`, or `form.getJobId()`) belongs to the session company before proceeding. The form fields `equipId`, `jobId`, `driverId`, and associated time/instruction fields are all attacker-controlled with no ownership verification.

```java
} else if (action.equalsIgnoreCase("assign_driver")) {
    System.out.println(form.getJobTitle());           // debug output to stdout
    List<DriverBean> arrDrivers = driverDao.getAllDriver(sessCompId, true);
    request.setAttribute("arrDrivers", arrDrivers);
    return mapping.findForward("successupdate");       // no actual DB write visible here,
}                                                      // but the forward name implies persistence
```

Even if the persistence call occurs elsewhere (e.g., in a JSP or interceptor), the lack of ownership validation here establishes a pattern of unprotected cross-company job modification.

**Risk:** Horizontal privilege escalation allowing a user to assign drivers to jobs belonging to other companies, or to observe the workflow state of other companies.

**Recommendation:** Resolve the target job from the database using `sessCompId` as a required predicate before permitting any modification. If no matching job is found for the session company, return an authorization error.

---

### HIGH: No CSRF Protection on State-Changing assign_driver Sub-Action

**File:** `DriverJobDetailsAction.java` (lines 61-66)

**Description:**
The `assign_driver` sub-action modifies application state (driver assignment) but there is no CSRF token validation anywhere in the action or form. Struts 1.x does not provide built-in CSRF protection. An attacker can craft a forged cross-site request that causes a logged-in user's browser to submit the `assign_driver` action without the user's knowledge.

**Risk:** An attacker who can lure an authenticated administrator to visit a malicious page can silently reassign drivers to arbitrary jobs on their behalf.

**Recommendation:** Implement a synchronizer token pattern. Generate a unique per-session (or per-form) token, store it in the session, embed it as a hidden field in the form, and verify it in the action before processing any state-changing sub-action. Struts 1.x provides `saveToken` / `isTokenValid` utilities on the `Action` base class for exactly this purpose.

---

### MEDIUM: No Input Validation in ActionForm (validate() Not Overridden)

**File:** `DriverJobDetailsActionForm.java`

**Description:**
`DriverJobDetailsActionForm` extends `ActionForm` but does not override the `validate()` method. All fields — `equipId`, `jobId`, `driverId`, `startTime`, `endTime`, `fromTime`, `toTime`, `instruct`, `jobTitle`, `description` — are accepted without any length, type, or content checks. Raw user input flows directly from the form into action logic and ultimately into DAO calls. The raw `ArrayList driverList` field uses an unchecked/raw generic type.

```java
public class DriverJobDetailsActionForm extends ActionForm {
    // No validate() override — Struts will always return null (no errors)
    private String equipId;    // Should be validated as a positive integer
    private String jobId;      // Should be validated as a positive integer
    private String driverId;   // Should be validated as a positive integer
    private String startTime;  // Should be validated as a parseable datetime
    // ...
}
```

**Risk:** Malformed, oversized, or malicious input reaches business logic and DAO layers unchecked, compounding the SQL injection and IDOR risks and increasing the attack surface for other injection types.

**Recommendation:** Override `validate()` to enforce: numeric fields (`equipId`, `jobId`, `driverId`, `id`) must be positive integers; date/time fields must match an expected format; free-text fields (`instruct`, `jobTitle`, `description`) must have maximum length constraints. Use parameterized queries in the DAO regardless, as validation alone is not sufficient.

---

### MEDIUM: Debug Output Written to stdout in Production Code

**File:** `DriverJobDetailsAction.java` (line 62)

**Description:**
The `assign_driver` branch writes form data directly to `System.out`:

```java
System.out.println(form.getJobTitle());
```

This is unstructured, uncontrolled output that bypasses the application's logging framework (`log4j` is available and used elsewhere in the class). In production environments, `System.out` output can appear in application server logs and may include sensitive data.

**Risk:** Information disclosure through server log files accessible to operators or via log management pipelines. Indicates the action was not production-hardened before deployment.

**Recommendation:** Remove the `System.out.println` call. If logging job assignment activity is desired for audit purposes, use the existing `log` instance at an appropriate level (e.g., `log.info`).

---

### LOW: Broken String Comparison Causes Silent Action Routing Failure

**File:** `DriverJobDetailsAction.java` (lines 41-43, 45-47)

**Description:**
Two consecutive conditions use the `==` operator (reference equality) to compare `String` objects, which is semantically incorrect in Java:

```java
// Line 41-43: always false for a non-null String returned from getParameter()
if (action == null || action == "") {
    action = form.getAction();
}
// Line 45-47: redundant null check that can never be reached via the prior branch
if (action == null) {
    return mapping.findForward("error");
}
```

Since `request.getParameter("action")` is already null-guarded on line 36 (it is assigned `""` rather than `null`), the `action == ""` comparison will always be `false` (different `String` instances), and `form.getAction()` will never be called as a fallback. If a caller relies on the form field rather than the request parameter to supply the action, the routing silently falls through to the `else` branch and returns `"error"`.

**Risk:** Functional defect that could mask legitimate requests as errors, but does not in itself create a security vulnerability. Noted here because silent failure in security-sensitive routing logic is a code quality concern.

**Recommendation:** Replace both comparisons with `.equals()` / `.isEmpty()`: `if (action == null || action.isEmpty())`.

---

### INFO: sessCompId Read but Not Validated as Non-Empty Before Use

**File:** `DriverJobDetailsAction.java` (line 35)

**Description:**
`sessCompId` is read from the session and defaulted to an empty string if absent:

```java
String sessCompId = (String) session.getAttribute("sessCompId") == null ? ""
                  : (String) session.getAttribute("sessCompId");
```

The framework's `PreFlightActionServlet` is stated to gate on `sessCompId != null`, but this action itself accepts an empty string as a valid company identifier. The `assign` and `assign_driver` branches pass `sessCompId` to `driverDao.getAllDriver()`, meaning an empty string would be passed to the DAO if the pre-flight check were ever bypassed or misconfigured, potentially returning drivers from all companies or causing a query error.

**Risk:** Low in isolation, but represents a defence-in-depth gap. If the pre-flight check is disabled, misconfigured, or bypassed via a URL mapping not covered by the filter, this action will silently operate with an empty company scope.

**Recommendation:** Add an explicit guard at the top of `execute()`: if `sessCompId` is null or empty, redirect to an error or login forward immediately, rather than relying solely on the filter chain.

---

### INFO: Raw/Unchecked Generic Type in ActionForm

**File:** `DriverJobDetailsActionForm.java` (lines 13, 36, 69)

**Description:**
The `driverList` field and its accessor/mutator use a raw `ArrayList` without a type parameter:

```java
private ArrayList driverList;
public ArrayList getDriverList() { return driverList; }
public void setDriverList(ArrayList driverList) { this.driverList = driverList; }
```

This suppresses compile-time type safety and generates unchecked cast warnings.

**Risk:** Negligible direct security impact, but raw types can conceal type-confusion bugs and make code review harder.

**Recommendation:** Parameterize as `ArrayList<DriverBean>` (or `List<DriverBean>`) to match the usage pattern seen in the action class.

---

## Finding Count

| Severity | Count |
|----------|-------|
| CRITICAL | 1     |
| HIGH     | 3     |
| MEDIUM   | 2     |
| LOW      | 1     |
| INFO     | 2     |
| **Total**| **9** |
