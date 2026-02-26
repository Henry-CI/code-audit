# Pass 1 Audit — DealerCompaniesAction / DealerCompaniesActionForm

**Files:**
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/action/DealerCompaniesAction.java`
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/actionform/DealerCompaniesActionForm.java`

**Date:** 2026-02-26

---

## Summary

`DealerCompaniesAction` is a Struts 1.x action that serves a dealer's sub-company listing and an "add sub-company" form. The action is protected at the servlet level by `PreFlightActionServlet`, which verifies that `sessCompId` is non-null before routing any request to an action. However, `PreFlightActionServlet` performs **no role check** — it only confirms that a session with a company ID exists. Any authenticated user (including non-dealer `ROLE_COMPANY_GROUP` or `ROLE_SITE_ADMIN` users) can therefore reach this action.

Within the action itself there is also no role check: the code never verifies that the calling session belongs to a dealer (`ROLE_DEALER`), meaning a regular company user can invoke the dealer sub-company listing and the sub-company creation form. The action always uses the session-owned `sessCompId` for the list query, so the sub-company listing itself is correctly scoped — there is no direct IDOR in the list path. However, the "add" flow is accessible to non-dealers and contains no validation, enabling a non-dealer company to initiate sub-company creation.

The `DealerCompaniesActionForm` is entirely empty (no fields, no `validate()` override), meaning Struts performs no input validation whatsoever for any form submission routed through this action.

No CSRF protection exists anywhere in the application: `struts-config.xml` declares no token-based plugin or interceptor, and the action does not call `isTokenValid()`.

Separately, `CompanyDAO` — which is the data layer called by this action — contains multiple methods with critical SQL injection vulnerabilities (`checkExist`, `checkUserExit`, `checkCompExist`, `getCompLogo`, `getEntityByQuestion`, `getEntityComp`, `getAllEntity`). While these specific methods are not called from `DealerCompaniesAction` directly, they are part of the same DAO and are called from other actions that share this code path; they are included here because they represent material risk in the surrounding data-access layer and must be tracked.

The `getSubCompanies` method called by the action uses a parameterized `PreparedStatement` (`QUERY_SUBCOMPANYLST_BY_ID`) and is not injectable.

---

## Findings

---

### HIGH: Missing Dealer Role Check — Any Authenticated User Can Access the Dealer Sub-Company Screen

**File:** `DealerCompaniesAction.java` (lines 18–39)

**Description:**
`DealerCompaniesAction.execute()` reads `sessCompId` from the session and immediately invokes dealer-specific functionality without first verifying that the authenticated company holds the `ROLE_DEALER` role. `PreFlightActionServlet` only gates on `sessCompId != null`; it does not check roles. As a result, any user with a valid session — including `ROLE_COMPANY_GROUP` and `ROLE_SITE_ADMIN` users — can request `/dealercompanies.do` and:

1. View the dealer sub-company listing for their own company ID (unlikely to return results for non-dealers, but the endpoint is still reached).
2. Reach the "add sub-company" form (`action=add`) and submit it, potentially triggering `saveSubCompInfo` in downstream actions.

The `isDealer` flag that is propagated to the request attribute (`session.getAttribute("isDealer")`) is only used for UI rendering logic. It is not used as an access-control gate in the action itself.

```java
// DealerCompaniesAction.java lines 24-38
HttpSession session = request.getSession(false);
String action = request.getParameter("action") == null ? "" : request.getParameter("action");
String companyId = session.getAttribute("sessCompId").toString();

if (action.equalsIgnoreCase("add")) {
    // No role check — any authenticated user reaches here
    List<CompanyBean> subCompanyLst = new ArrayList<>();
    subCompanyLst.add(new CompanyBean());
    request.setAttribute("companyRecord", subCompanyLst);
    return mapping.findForward("add");
} else {
    request.setAttribute("isDealer", session.getAttribute("isDealer"));
    request.setAttribute("subCompanyLst", CompanyDAO.getSubCompanies(companyId));
    return mapping.findForward("list");
}
```

**Risk:**
A non-dealer authenticated user can access dealer-only functionality, violating the intended role separation. Combined with any downstream "add" action that also omits a role check, this is a privilege escalation path allowing an unauthorized company to create sub-companies.

**Recommendation:**
Add an explicit role check at the start of `execute()` using the server-side authority lookup pattern already used elsewhere in the codebase:

```java
Boolean isDealer = (Boolean) session.getAttribute("isDealer");
if (isDealer == null || !isDealer) {
    return mapping.findForward("failure");
}
```

Alternatively, delegate to `LoginDAO.isAuthority(companyId, RuntimeConf.ROLE_DEALER)` for a live database check that cannot be spoofed via session manipulation.

---

### HIGH: No CSRF Protection on State-Changing Operations

**File:** `DealerCompaniesAction.java` (lines 28–32); `struts-config.xml` (lines 536–549)

**Description:**
The action handles the `action=add` request parameter, which renders a form intended for subsequent sub-company creation. Struts 1.x provides a built-in CSRF token mechanism (`saveToken()` / `isTokenValid()`) that must be explicitly used by the developer. Neither `DealerCompaniesAction` nor its companion "add" action mapping (`/dealercompaniesAdd`) uses this mechanism. There is no token plugin, filter, or interceptor configured in `struts-config.xml` for these paths. An attacker can craft a cross-origin form that POSTs to `/dealercompanies.do?action=add` or to the downstream add-submission action from any origin while the victim's browser session is active.

**Risk:**
Cross-site request forgery against the sub-company creation workflow. An attacker can create sub-companies under a dealer's account without user interaction beyond visiting a malicious page.

**Recommendation:**
In the action that processes the sub-company creation form submission, call `saveToken(request)` before forwarding to the form view, and `isTokenValid(request, true)` (resetting the token after use) at the beginning of the POST-handling branch. Reject requests that fail token validation with an appropriate error forward.

---

### MEDIUM: NullPointerException Risk — Unguarded `.toString()` on Session Attribute

**File:** `DealerCompaniesAction.java` (line 26)

**Description:**
The action retrieves `sessCompId` from the session and immediately calls `.toString()` without a null guard:

```java
String companyId = session.getAttribute("sessCompId").toString();
```

`PreFlightActionServlet` does check for `sessCompId == null` but only for paths that return `true` from `excludeFromFilter()`. That method contains a hard-coded path-suffix exclusion list. Any misconfiguration of a new path, a URL that bypasses the suffix check (e.g., a `.do` variant not in the list), or a direct internal forward that skips the servlet would result in a `NullPointerException` at line 26. A `NullPointerException` in a Struts 1.x action is unhandled by default and will propagate as a 500 error, potentially leaking a stack trace to the client if error pages are not configured.

**Risk:**
Application error / information disclosure. Stack traces may reveal internal class names, package structure, and database details.

**Recommendation:**
Add a null check before calling `.toString()`, and return a safe forward (e.g., session-expired page) if the attribute is absent:

```java
Object sessCompIdObj = session.getAttribute("sessCompId");
if (sessCompIdObj == null) {
    return mapping.findForward("sessionExpired");
}
String companyId = sessCompIdObj.toString();
```

---

### MEDIUM: Empty ActionForm — No Input Validation

**File:** `DealerCompaniesActionForm.java` (lines 1–6)

**Description:**
`DealerCompaniesActionForm` extends `ActionForm` but declares no fields, no getter/setter methods, and no `validate()` override. The Struts `struts-config.xml` maps this form bean (`dealerCompanyForm`) to the `/dealercompanies` action with `validate="true"`. However, because `DealerCompaniesActionForm` is empty, the `validate()` method inherited from the base `ActionForm` class always returns an empty `ActionErrors` collection — meaning Struts will never reject a submission on the basis of form validation, regardless of what parameters are submitted.

Any data submitted to the action (including the `action` request parameter used to branch logic) is accessed directly from `HttpServletRequest.getParameter()` without sanitization:

```java
String action = request.getParameter("action") == null ? "" : request.getParameter("action");
```

**Risk:**
Without a concrete form with field-level validation, any future expansion of the form to include company data fields would bypass Struts declarative validation. The current `action` parameter is compared with `equalsIgnoreCase`, which is safe for the current switch, but the pattern establishes no validation discipline for the feature.

**Recommendation:**
Implement the `DealerCompaniesActionForm` with typed fields for all expected request parameters and provide a `validate()` method that enforces allowlisted values. For the `action` parameter specifically, validate it against an explicit set of known values before use.

---

### CRITICAL: SQL Injection in CompanyDAO.checkExist() — Caller-Controlled Column Name and Value

**File:** `CompanyDAO.java` (lines 357–380)

**Description:**
`CompanyDAO.checkExist()` constructs a SQL query using string concatenation of both the `dbField` column name and the `name` value, neither of which can be parameterized with a `PreparedStatement` placeholder for the column name:

```java
String sql = "select id from company where " + dbField + " ='" + name + "'";
if (!compId.equalsIgnoreCase("")) {
    sql += " and id != " + compId;
}
```

All three inputs — `dbField` (column name), `name` (column value), and `compId` — are derived from caller-supplied data without sanitization. If any caller passes a user-controlled value as `dbField` or `name`, the entire query is injectable. This method is part of the same DAO class used by the action under audit.

**Risk:**
Full SQL injection. An attacker controlling the `name` or `compId` parameter through any calling action can exfiltrate data, modify data, or (depending on database permissions) execute OS-level commands.

**Recommendation:**
Column names cannot be parameterized with `PreparedStatement`; they must be validated against a strict allowlist of known column names before being interpolated. The `name` and `compId` values must be bound via `PreparedStatement` parameters. Example:

```java
Set<String> ALLOWED_FIELDS = Set.of("email", "refnm", "refno");
if (!ALLOWED_FIELDS.contains(dbField)) throw new IllegalArgumentException("Invalid field: " + dbField);
// Then use PreparedStatement with ? placeholders for name and compId
```

---

### CRITICAL: SQL Injection in CompanyDAO.checkUserExit() — Caller-Controlled Column Name and Value

**File:** `CompanyDAO.java` (lines 382–394)

**Description:**
Identical pattern to `checkExist()`. The `dbField` column name and `name` value are concatenated directly into the SQL string:

```java
String sql = "select id from users where " + dbField + " ='" + name + "'";
if (!id.equalsIgnoreCase("")) {
    sql += " and id != " + id;
}
```

**Risk:**
Full SQL injection against the `users` table. An attacker can enumerate, extract, or modify user records.

**Recommendation:**
Same as for `checkExist()`: allowlist `dbField` values and use parameterized statements for all user-supplied data.

---

### CRITICAL: SQL Injection in CompanyDAO.checkCompExist() — Multiple Concatenated Values

**File:** `CompanyDAO.java` (lines 396–433)

**Description:**
`checkCompExist()` concatenates four `CompanyBean` fields directly into a SQL `WHERE` clause using string interpolation:

```java
String sql = "select id from company where name = '" + companyBean.getName() + "' and email = '" + companyBean.getEmail() + "'";
if (!companyBean.getQuestion().equalsIgnoreCase("")) {
    sql += " and question ilike '" + companyBean.getQuestion() + "'";
} else {
    sql += " and question is null ";
}
if (!companyBean.getAnswer().equalsIgnoreCase("")) {
    sql += " and answer = '" + companyBean.getAnswer() + "'";
} else {
    sql += " and answer is null ";
}
```

All four fields (`name`, `email`, `question`, `answer`) come from a `CompanyBean` that may be populated from HTTP request parameters via the ActionForm.

**Risk:**
Full SQL injection against the `company` table. An attacker can bypass the existence check entirely or exfiltrate company data.

**Recommendation:**
Rewrite using a `PreparedStatement` with `?` placeholders for all four fields.

---

### CRITICAL: SQL Injection in CompanyDAO.getCompLogo() — Unparameterized compId

**File:** `CompanyDAO.java` (lines 461–486)

**Description:**
The `compId` value is concatenated directly into the query string without parameterization:

```java
String sql = "select logo from company where id = " + compId + "";
```

Although `compId` originates from the session in the calling code (`FleetCheckAlert.java`), the method accepts a raw `String` parameter with no type enforcement or sanitization, making it fragile if the call site ever changes.

**Risk:**
SQL injection against the `company` table if any caller passes an unsanitized value. The column returned is `logo`, which may contain file paths or binary data, but the primary risk is blind or union-based injection allowing cross-tenant data access.

**Recommendation:**
Use `PreparedStatement` with a `?` placeholder. If the value is always numeric, parse it to `long` before use to fail fast on non-numeric input:

```java
String sql = "select logo from company where id = ?";
ps = conn.prepareStatement(sql);
ps.setLong(1, Long.parseLong(compId));
```

---

### CRITICAL: SQL Injection in CompanyDAO.getEntityByQuestion() — qId and type Concatenated

**File:** `CompanyDAO.java` (lines 690–720)

**Description:**
Both `qId` and `type` are concatenated directly into the SQL string:

```java
String sql = "select entity.id,name, email from entity, form_library where entity.id = form_library.lock_entity_id and question_id = " + qId + " and type= '" + type + "'";
```

`qId` and `type` originate from `FormBuilderAction`, which reads them from request parameters.

**Risk:**
SQL injection against the `entity` and `form_library` tables via user-supplied request parameters.

**Recommendation:**
Use `PreparedStatement` with `?` placeholders for both `qId` and `type`.

---

### HIGH: SQL Injection in CompanyDAO.getEntityComp() — entityId Concatenated Conditionally

**File:** `CompanyDAO.java` (lines 655–688)

**Description:**
When `entityId` is not equal to `"1"`, it is concatenated directly into the SQL `WHERE` clause:

```java
if (!entityId.equalsIgnoreCase("1")) {
    sql += " where comp_entity_rel.entity_id = " + entityId;
}
```

`entityId` originates from `sessCompId` in `AdminMenuAction`, which is a session value and therefore not directly user-controllable in a normal flow. However, the method accepts an arbitrary `String`, and if any other caller were to pass a request-derived value, the injection would be reachable.

**Risk:**
SQL injection against the `company` and `comp_entity_rel` tables. Current exploitability is low given the session origin of the caller, but the method's interface provides no protection against future misuse.

**Recommendation:**
Use `PreparedStatement` with a `?` placeholder. Validate that `entityId` is numeric before use.

---

### HIGH: SQL Injection in CompanyDAO.getAllEntity() — Nested Query with Concatenated Entity ID

**File:** `CompanyDAO.java` (lines 722–768)

**Description:**
Within a loop over entity records, a nested query is built by concatenating `rs.getString(1)` (the entity ID from a prior result set) directly into a new SQL string:

```java
sql = "select roles.id,name,description from roles,entity_role_rel where roles.id = entity_role_rel.role_id and entity_id = " + rs.getString(1);
rst = stm.executeQuery(sql);
```

While `rs.getString(1)` is a database-derived value rather than a direct user input, this pattern is unsafe: if the `entity` table is ever populated with attacker-controlled data, second-order SQL injection becomes possible.

**Risk:**
Second-order SQL injection. An attacker who can insert a malicious entity ID into the `entity` table can cause injection when `getAllEntity()` is later called.

**Recommendation:**
Use a `PreparedStatement` for the nested query instead of reusing the same `Statement` object with a concatenated string.

---

### INFO: CompanyBean Exposes Sensitive Fields Including Hashed Password and PIN

**File:** `CompanyBean.java` (lines 24–25); `CompanyDAO.java` (lines 75–79, 181–198)

**Description:**
`QUERY_SUBCOMPANYLST_BY_ID` selects `c.password` and `c.pin` from the `company` table, and these are mapped into `CompanyBean.password` and `CompanyBean.pin` respectively. The resulting bean is placed into the request attribute `subCompanyLst` and forwarded to the `dealerCompaniesDefinition` view. If the JSP template renders any of these fields (even inadvertently via `<bean:write>` wildcard patterns), hashed passwords and PINs will be exposed to the browser.

**Risk:**
Sensitive credential data in the view layer. Even hashed values provide an offline cracking oracle and facilitate account compromise.

**Recommendation:**
Remove `password` and `pin` columns from `QUERY_SUBCOMPANYLST_BY_ID`. Create a dedicated "list view" query that selects only the fields required for display (e.g., `id`, `name`, `address`). Ensure the `CompanyBean` returned for listing purposes never carries credential fields.

---

### INFO: Struts 1.x Framework End-of-Life

**File:** `struts-config.xml`; all action/actionform files

**Description:**
The application uses Apache Struts 1.x, which reached end-of-life on 2013-04-05. No security patches have been issued for over a decade. The framework is affected by multiple known CVEs (including the Class Loader manipulation vulnerability CVE-2014-0114) and lacks modern security features such as built-in CSRF protection, security headers, and expression language sandboxing.

**Risk:**
The underlying framework itself is a persistent attack surface. Any newly discovered Struts 1.x vulnerability will not receive an official patch.

**Recommendation:**
Plan migration to a supported framework (Spring MVC, Jakarta EE, Quarkus, etc.). In the interim, apply all available container-level mitigations and restrict the application to internal networks where possible.

---

## Finding Count

| Severity | Count |
|----------|-------|
| CRITICAL | 5     |
| HIGH     | 4     |
| MEDIUM   | 2     |
| LOW      | 0     |
| INFO     | 2     |

- CRITICAL: 5
- HIGH: 4
- MEDIUM: 2
- LOW: 0
- INFO: 2
