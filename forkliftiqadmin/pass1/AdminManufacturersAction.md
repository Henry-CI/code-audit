# Security Audit: AdminManufacturersAction.java
**Audit Run:** audit/2026-02-26-01
**Branch:** master
**Date:** 2026-02-26
**Auditor:** CIG Automated Pass 1

---

## 1. Reading Evidence

### 1.1 Package and Class
- **File:** `src/main/java/com/action/AdminManufacturersAction.java`
- **Package:** `com.action`
- **Class:** `AdminManufacturersAction extends PandoraAction`
- **Annotations:** `@Slf4j` (Lombok logging)
- **Framework:** Apache Struts 1.3.10 — single `execute()` dispatch pattern

### 1.2 Methods (with line numbers)

| Method | Visibility | Lines | Description |
|--------|-----------|-------|-------------|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | `public` | 18–52 | Main Struts dispatch; routes on `action` parameter |
| `returnManufacturersJson(HttpServletResponse, String companyId)` | `private` | 54–59 | Fetches all manufacturers for companyId, writes JSON to response |
| `returnBooleanJson(HttpServletResponse, Boolean value)` | `private` | 61–66 | Writes boolean JSON to response |

### 1.3 DAOs / Services Called

| Call site (Action line) | DAO method | DAO file line | Uses PreparedStatement? |
|-------------------------|-----------|--------------|------------------------|
| L30 | `ManufactureDAO.saveManufacturer(ManufactureBean)` | DAO L174 | Yes |
| L37 | `ManufactureDAO.updateManufacturer(ManufactureBean)` | DAO L210 | Yes |
| L41 | `ManufactureDAO.delManufacturById(String id)` | DAO L99 | Yes |
| L46 | `ManufactureDAO.isVehicleAssignedToManufacturer(String manufacturerId)` | DAO L404 | Yes |
| L49, L56 | `ManufactureDAO.getAllManufactures(String companyId)` | DAO L40 | Yes (via DBUtil) |

Additional DAO methods present in `ManufactureDAO.java` but **not called** from this action:
- `getManufactureById(String id)` — DAO L60 — **raw `Statement` + string concatenation (SQL injection)**
- `checkManuByNm(String name, String id)` — DAO L137 — **raw `Statement` + string concatenation (SQL injection)**
- `getManu_type_fuel_rel(String manuId)` — DAO L247 — **raw `Statement` + string concatenation (SQL injection)**

These are catalogued under SQL Injection findings because they exist in the same DAO class and represent risk surface even if not directly invoked from this action.

### 1.4 Form Class
- **Form:** `com.actionform.AdminManufacturersActionForm extends ActionForm`
- **File:** `src/main/java/com/actionform/AdminManufacturersActionForm.java`
- **Fields:** `manufacturerId` (String), `manufacturer` (String), `action` (String)
- All fields default to `null`; no `validate()` override; no `reset()` override.

### 1.5 Struts-Config Mapping (struts-config.xml lines 273–283)

```xml
<action
    path="/manufacturers"
    type="com.action.AdminManufacturersAction"
    name="AdminManufacturersActionForm"
    scope="request"
    validate="false">
    <forward name="adminmanufacturers" path="/adminmenu.do?action=home"/>
    <forward name="success"            path="ManufacturersListDefinition"/>
    <forward name="failure"            path="/adminmenu.do?action=home"/>
</action>
```

Key mapping attributes:
- `scope="request"` — form bean is request-scoped (correct).
- `validate="false"` — Struts framework validation is **explicitly disabled**; `validation.xml` rules will not fire for this action.
- No `roles` attribute — no declarative role-based access control at the Struts mapping level.
- The forward name used in the action's list branch is `"manufacturerlist"` (Action L50), but the mapping defines `"success"` pointing to `ManufacturersListDefinition`. This forward name mismatch means the list/GET branch **always falls through to null** unless `"manufacturerlist"` is defined elsewhere (tiles-defs.xml); this is a latent functional bug that could mask errors.

### 1.6 PreFlightActionServlet Auth Gate
- `src/main/java/com/actionservlet/PreFlightActionServlet.java`
- Gate: `session == null` OR `session.getAttribute("sessCompId") == null OR == ""` → redirect to EXPIRE_PAGE.
- `/manufacturers.do` is **not** in the `excludeFromFilter` list → it IS subject to the sessCompId gate.
- Gate operates on `doGet`, which is called by `doPost`. Protection applies to both HTTP methods.

### 1.7 Validation Coverage
- `src/main/webapp/WEB-INF/validation.xml` defines rules only for: `loginActionForm`, `adminRegisterActionForm`, `AdminDriverEditForm`.
- `AdminManufacturersActionForm` has **no entry** in `validation.xml`.
- Struts mapping sets `validate="false"`, confirming zero framework-level input validation for this action.

---

## 2. Security Audit Findings

---

### FINDING 1 — CRITICAL: Cross-Site Request Forgery (CSRF) — State-Mutating Operations with No Token

**Severity:** CRITICAL
**File:** `src/main/java/com/action/AdminManufacturersAction.java`, lines 26–43
**Also:** `src/main/webapp/WEB-INF/struts-config.xml`, lines 273–283

**Description:**
The `add`, `edit`, and `delete` branches all perform irreversible database mutations (insert, update, delete of manufacturer records). There is no CSRF token generated, stored in session, or verified on the incoming request at any layer. Apache Struts 1.x has no built-in CSRF protection. The `PreFlightActionServlet` only checks `sessCompId != null`; it does not verify a synchronizer token. Any page on the internet can forge a POST to `/manufacturers.do?action=delete&manufacturerId=X` and the server will execute the deletion if the victim has an active session.

**Evidence:**
- No token generation or verification code in `execute()` (Action L18–52).
- No CSRF filter in `PreFlightActionServlet.java`.
- No `roles` or token attribute in struts-config mapping (struts-config.xml L273–283).
- Stack description confirms: "CSRF = structural gap."

**Recommendation:**
Implement the Synchronizer Token Pattern. Generate a per-session (or per-form) random token, store it in the HTTP session, embed it as a hidden field in every form and as a parameter in every AJAX call, and verify it server-side at the top of `execute()` before any branch that mutates state. Reject (HTTP 403) requests where the token is absent or mismatched.

---

### FINDING 2 — HIGH: Insecure Direct Object Reference (IDOR) — Edit and Delete Without Ownership Check

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminManufacturersAction.java`, lines 33–43
**Also:** `src/main/java/com/dao/ManufactureDAO.java`, lines 210–244 (updateManufacturer), 99–135 (delManufacturById)

**Description:**
The `edit` branch (L33–39) accepts `manufacturerId` from the request form, constructs a `ManufactureBean` with that ID, and calls `ManufactureDAO.updateManufacturer()`. The `delete` branch (L40–43) similarly calls `ManufactureDAO.delManufacturById()` with the form-supplied ID. **Neither branch verifies that the manufacturer record identified by `manufacturerId` belongs to `sessCompId`.**

The `updateManufacturer` SQL (`update manufacture set name = ? where id = ?`, DAO L216) and `delManufacturById` SQL (`delete from manufacture where id = ?`, DAO L114) operate solely on the numeric `id`. An authenticated user from Company A can therefore modify or delete a manufacturer record owned by Company B simply by supplying that company's manufacturer ID in the request.

The `add` branch (L26–32) correctly assigns `sessCompId` to the new record via `manufacture.setCompany_id(sessCompId)` (Action L29), so `add` is not affected by this IDOR.

**Evidence:**
- Action L35: `manufacture.setId(adminManufacturersActionForm.getManufacturerId());` — ID from untrusted input, no ownership verified.
- Action L37: `ManufactureDAO.updateManufacturer(manufacture);` — DAO does not receive `companyId`.
- Action L41: `ManufactureDAO.delManufacturById(adminManufacturersActionForm.getManufacturerId());` — DAO does not receive `companyId`.
- DAO L216: `update manufacture set name = ? where id = ?` — no `company_id` filter in WHERE clause.
- DAO L114: `delete from manufacture where id = ?` — no `company_id` filter in WHERE clause.
- DAO L107: `delete from manu_type_fuel_rel where manu_id = ?` — cascades deletion without ownership check.

**Recommendation:**
Before calling `updateManufacturer` or `delManufacturById`, retrieve the target record and verify `company_id` equals `sessCompId`. Alternatively, add `AND company_id = ?` to the UPDATE and DELETE SQL statements in the DAO and pass `sessCompId` as a parameter. If `executeUpdate()` returns 0, reject the request.

---

### FINDING 3 — HIGH: IDOR — `isVehicleAssigned` Leaks Cross-Tenant Metadata

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminManufacturersAction.java`, lines 44–47
**Also:** `src/main/java/com/dao/ManufactureDAO.java`, lines 404–432

**Description:**
The `isVehicleAssigned` branch (Action L44–47) accepts `manufacturerId` from the request and calls `ManufactureDAO.isVehicleAssignedToManufacturer(manufacturerId)`. The DAO query (`select count(*) from unit where manu_id = ? and active is TRUE`, DAO L25) has no `company_id` predicate. An authenticated user from any company can supply any numeric manufacturer ID and learn whether active vehicles are assigned to that manufacturer across all tenants. This is an information-disclosure IDOR — it reveals cross-tenant operational data (whether another company's manufacturer is in active use).

**Evidence:**
- Action L45–46: `manufacturerId` taken from form without validation against `sessCompId`.
- DAO L25: `QUERY_VEHICLE_BY_MANUFACTURE_SQL` has no `company_id` filter.
- DAO L415: `ps.setInt(1, Integer.parseInt(manufacturerId));` — only one bind parameter.

**Recommendation:**
Add a `company_id` join or subquery to `QUERY_VEHICLE_BY_MANUFACTURE_SQL` to restrict the count to units belonging to the requesting company, or pre-validate that `manufacturerId` belongs to `sessCompId` before calling the DAO.

---

### FINDING 4 — HIGH: Missing Input Validation — All Mutable Fields Unchecked

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminManufacturersAction.java`, lines 26–47
**Also:** `src/main/webapp/WEB-INF/struts-config.xml`, line 278 (`validate="false"`)
**Also:** `src/main/webapp/WEB-INF/validation.xml` (no entry for `AdminManufacturersActionForm`)

**Description:**
Three fields from `AdminManufacturersActionForm` flow directly into database operations with no sanitisation or length/format checks at any layer:

1. `manufacturer` (String) → inserted as manufacturer name (Action L28, DAO L187 `ps.setString(1, ...)`). No maximum length check. Oversized input can cause DB truncation errors or, depending on DB column type, silent data corruption. No character-set or pattern validation (e.g., null bytes, control characters).

2. `manufacturerId` (String) → parsed as integer in DAO (`Integer.parseInt(id)`, DAO L109, L116, L224, L415). If `manufacturerId` is null, blank, or non-numeric, `parseInt` throws `NumberFormatException`, which propagates as an unhandled exception through the action (which declares `throws Exception`). This can be triggered deliberately to cause application errors.

3. `action` (String) → compared with `.equals()` (Action L26 etc.) with no whitelist enforcement in the struts mapping; unrecognised values fall through to the list branch, but null will throw `NullPointerException` at L26 because `getAction()` can return null (form field defaults to null, no null check before `.equals()`).

The struts mapping explicitly sets `validate="false"` (struts-config.xml L278), disabling framework validation. `AdminManufacturersActionForm` has no `validate()` override and no entry in `validation.xml`.

**Evidence:**
- `AdminManufacturersActionForm.java` L14–16: all fields initialised to `null`.
- struts-config.xml L278: `validate="false"`.
- validation.xml: no `<form name="AdminManufacturersActionForm">` block.
- Action L26: `adminManufacturersActionForm.getAction().equals("add")` — NullPointerException if `action` is null.
- DAO L109: `Integer.parseInt(id)` — uncaught `NumberFormatException` if `manufacturerId` is blank/null/non-numeric.

**Recommendation:**
(a) Add a null/blank guard for `action` before the first `.equals()` call (e.g., use `"add".equals(adminManufacturersActionForm.getAction())`).
(b) Add an integer format check for `manufacturerId` before any DAO call; reject with an HTTP 400 or return an error JSON if the value is not a valid positive integer.
(c) Add a maximum-length and character-whitelist check for `manufacturer` name (e.g., max 100 chars, printable characters only).
(d) Set `validate="true"` in struts-config.xml and add a `<form name="AdminManufacturersActionForm">` block to `validation.xml` with `required` and `maxlength` rules.

---

### FINDING 5 — HIGH: SQL Injection in ManufactureDAO (Methods Reachable from Application Context)

**Severity:** HIGH
**File:** `src/main/java/com/dao/ManufactureDAO.java`

**Description:**
Three methods in `ManufactureDAO` use raw `Statement` objects with direct string concatenation, introducing classic SQL injection vulnerabilities. While these methods are not called from `AdminManufacturersAction.execute()` directly, they reside in the same DAO and are accessible from other parts of the application. They are reported here as part of the DAO surface audit required for this action file.

| Method | Line | Vulnerable SQL |
|--------|------|---------------|
| `getManufactureById(String id)` | L72 | `"select id,name from manufacture where id = " + id` |
| `checkManuByNm(String name, String id)` | L149–151 | `"select id from manufacture where name = '" + name + "'"` and `" and id !=" + id` |
| `getManu_type_fuel_rel(String manuId)` | L263 | `"... where manu_id = " + manuId` |

`checkManuByNm` (L149) is the most severe: the `name` parameter is wrapped in single quotes and concatenated without escaping, enabling classic `' OR '1'='1` or stacked-query injection depending on the JDBC driver and database configuration.

**Evidence:**
- DAO L72: `String sql = "select id,name from manufacture where id = " + id;`
- DAO L149: `String sql = "select id from manufacture where name = '" + name + "'";`
- DAO L151: `sql += " and id !=" + id;`
- DAO L263: `" where manu_id = " + manuId`
- All three use `conn.createStatement()` (DAO L70, L147, L258) — no parameterisation.

**Recommendation:**
Replace all raw `Statement` + concatenation patterns with `PreparedStatement` using `?` bind parameters, consistent with the pattern already used in `saveManufacturer`, `updateManufacturer`, `delManufacturById`, and `isVehicleAssignedToManufacturer`.

---

### FINDING 6 — MEDIUM: Weak Authentication — sessCompId Read After Action Dispatch, Empty-String Accepted

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminManufacturersAction.java`, lines 23–24

**Description:**
Two weaknesses in the sessCompId handling within the action:

**6a — Empty string accepted as valid identity.**
Action L24 reads `sessCompId` using a null-coalescing pattern that converts null to `""` (empty string):
```java
String sessCompId = session.getAttribute("sessCompId") == null ? "" : (String) session.getAttribute("sessCompId");
```
`PreFlightActionServlet` (L56) blocks requests where `sessCompId` is null **or** equals `""`. However, if the session attribute is set to any non-empty, non-null value (including a single space or a malformed value), the gate passes and this action will use that value as `companyId`. There is no downstream check that `sessCompId` is a valid positive integer before it is passed to `ManufactureDAO.getAllManufactures()` (Action L49, L56), where it is parsed with `Long.valueOf(companyId)` (DAO L47). A non-numeric `sessCompId` would cause an unhandled `NumberFormatException`.

**6b — No role check.**
The action performs no role verification. Any authenticated session (regardless of whether the user is an admin, operator, or driver) that passes the `sessCompId` gate can invoke the `add`, `edit`, and `delete` branches. The struts-config mapping has no `roles` attribute. `PandoraAction` provides no `getCompId()` call or role-checking utility that is used here. The application stack description confirms there is no Spring Security; no other role enforcement is visible in this action.

**Evidence:**
- Action L24: null-to-empty-string coalescion; empty string would fail `PreFlightActionServlet` gate but the gate check is `== null || .equals("")`, so an empty string IS blocked at the gate — however, the action's own local handling still accepts `""` and would pass it to DAO if reached via a race or misconfiguration.
- Action L18–52: no `session.getAttribute("sessRole")` or equivalent check anywhere.
- struts-config.xml L273–283: no `roles` attribute.

**Recommendation:**
(a) Replace the null-to-empty-string coalescion with a strict null check; redirect to the expire page if `sessCompId` is null or not a valid positive-integer string.
(b) Add an explicit role check at the top of `execute()` — read a `sessRole` (or equivalent) session attribute and reject requests from non-admin roles before any branch executes.

---

### FINDING 7 — MEDIUM: NullPointerException Risk — `session.getAttribute` Without Null-Safe Session Retrieval

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminManufacturersAction.java`, line 23

**Description:**
`request.getSession(false)` (Action L23) returns `null` if no session exists. The immediately following line (L24) calls `session.getAttribute(...)` without a null check on `session`. If a request reaches this action without a session (e.g., after session expiry between the `PreFlightActionServlet` check and the action invocation, or via a direct request that bypasses the filter), a `NullPointerException` will be thrown. The exception propagates to the global exception handler (`java.sql.SQLException` and `java.io.IOException` are handled in `global-exceptions`, but `NullPointerException` is a `RuntimeException` and not covered), potentially exposing an unformatted error page.

**Evidence:**
- Action L23: `HttpSession session = request.getSession(false);` — returns null if no session.
- Action L24: `session.getAttribute("sessCompId")` — dereferenced without null guard.
- struts-config.xml L42–55: `global-exceptions` handles only `SQLException`, `IOException`, `ServletException` — not `RuntimeException` / `NullPointerException`.

**Recommendation:**
Add an explicit null check: if `session == null`, redirect to the expire/login page and return null. This mirrors what `PreFlightActionServlet` does and provides defence-in-depth.

---

### FINDING 8 — MEDIUM: Response Content-Type Not Set for JSON Output

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminManufacturersAction.java`, lines 54–66

**Description:**
`returnManufacturersJson()` (L54–59) and `returnBooleanJson()` (L61–66) write JSON content directly to the `HttpServletResponse` using `response.getWriter()` but do not call `response.setContentType("application/json")` or `response.setCharacterEncoding("UTF-8")` before writing. This has two security-relevant consequences:

1. **MIME-type sniffing:** If the browser (or a proxy) does not receive `Content-Type: application/json`, it may sniff the response body. Depending on the browser and `X-Content-Type-Options` header configuration, this could allow the response to be interpreted as HTML, enabling script injection if any manufacturer name contains `<script>` tags or HTML-special characters. The JSON serialiser used (`com.json.JSONObject`) is not a well-known library; its escaping behaviour for HTML-special characters is unverified.

2. **Encoding mismatch:** Without explicit UTF-8 encoding, the container default may be ISO-8859-1, which can corrupt multi-byte manufacturer names and, in edge cases, introduce encoding-based injection vectors.

**Evidence:**
- Action L57: `PrintWriter out = response.getWriter();` — no prior `setContentType` call.
- Action L64: same pattern.
- `com.json.JSONObject` is a non-standard local class (not `org.json` or Jackson); HTML-entity escaping is unconfirmed.

**Recommendation:**
Add `response.setContentType("application/json; charset=UTF-8")` before calling `response.getWriter()` in both helper methods. Ensure `X-Content-Type-Options: nosniff` is set globally (filter or container configuration). Verify that `com.json.JSONObject.toString()` escapes `<`, `>`, `&`, and `"` for HTML contexts.

---

### FINDING 9 — LOW: Struts Forward Name Mismatch — Dead Code Path in List Branch

**Severity:** LOW
**File:** `src/main/java/com/action/AdminManufacturersAction.java`, line 50
**Also:** `src/main/webapp/WEB-INF/struts-config.xml`, lines 279–282

**Description:**
The `else` branch (Action L48–51) calls `mapping.findForward("manufacturerlist")`. The struts-config mapping for `/manufacturers` defines forwards named `"adminmanufacturers"`, `"success"`, and `"failure"` — there is no forward named `"manufacturerlist"`. `mapping.findForward("manufacturerlist")` will return `null`. Struts will interpret a `null` forward return from `execute()` as "response already committed" and take no further action. Whether the list page actually renders depends on whether a **global** forward named `"manufacturerlist"` exists in tiles-defs.xml or elsewhere. If it does not, the default GET/list branch silently fails to forward, potentially leaving the response empty or in an inconsistent state.

This is not directly a security vulnerability but it indicates that the list branch may be effectively dead, which can mask errors or lead to confusing behaviour during security testing (e.g., an attacker might use the broken state as a signal).

**Evidence:**
- Action L50: `return mapping.findForward("manufacturerlist");`
- struts-config.xml L279–282: forwards defined are `"adminmanufacturers"`, `"success"`, `"failure"`.

**Recommendation:**
Verify whether a global forward `"manufacturerlist"` exists in `tiles-defs.xml`. If not, correct the forward name in the action to match a defined forward (likely `"success"` → `ManufacturersListDefinition`).

---

### FINDING 10 — LOW: Exception Handling — Stack Traces Logged with `e.printStackTrace()`

**Severity:** LOW
**File:** `src/main/java/com/dao/ManufactureDAO.java`, lines 83, 128, 161, 234, 277 (multiple catch blocks)

**Description:**
Multiple DAO catch blocks call both `InfoLogger.logException(log, e)` and `e.printStackTrace()`. `printStackTrace()` writes to `System.err`, which in many container deployments is routed to a log file accessible outside the structured logging system, or worse, may appear in server console output. While not directly exploitable, stack traces contain class names, method names, SQL statement text, and line numbers that aid an attacker in fingerprinting the application stack and crafting further attacks.

**Evidence:**
- DAO L83, L128, L161, L234: `e.printStackTrace();` in catch blocks.

**Recommendation:**
Remove all `e.printStackTrace()` calls from production code. Rely solely on the structured logger (`InfoLogger.logException`) which controls output destination and format.

---

### FINDING 11 — INFO: Connection Not Closed on Normal Path in saveManufacturer / updateManufacturer

**Severity:** INFO
**File:** `src/main/java/com/dao/ManufactureDAO.java`, lines 196–205 (saveManufacturer finally), 231–240 (updateManufacturer finally)

**Description:**
In `saveManufacturer` and `updateManufacturer`, the `finally` block only closes the connection if `ps != null`:
```java
finally {
    if (null != ps) {
        ps.close();
        DBUtil.closeConnection(conn);
    }
}
```
If `conn.prepareStatement(sql)` throws an exception (making `ps` remain null), `conn` is never closed, creating a connection leak. This is an availability/resource issue rather than a direct confidentiality or integrity vulnerability, but connection pool exhaustion can be used as a denial-of-service vector.

**Evidence:**
- DAO L196–205: `finally` block in `saveManufacturer` — connection not closed when `ps == null`.
- DAO L231–240: same pattern in `updateManufacturer`.

**Recommendation:**
Use try-with-resources for both `Connection` and `PreparedStatement`, or restructure the finally block to close `conn` unconditionally (null-checked separately from `ps`).

---

## 3. Category Summary

| Category | Status | Finding(s) |
|----------|--------|-----------|
| Authentication (sessCompId gate) | ISSUE | Finding 6 (weak gate, no role check), Finding 7 (NPE on null session) |
| CSRF | ISSUE | Finding 1 |
| Input Validation | ISSUE | Finding 4 |
| SQL Injection | ISSUE | Finding 5 (DAO methods not invoked from this action but in same file) |
| IDOR | ISSUE | Finding 2 (edit/delete), Finding 3 (isVehicleAssigned) |
| Session Handling | ISSUE | Finding 7 (null session dereference) |
| Data Exposure | ISSUE | Finding 8 (missing Content-Type/encoding on JSON), Finding 10 (stack traces) |
| Forward/Routing | ISSUE | Finding 9 (forward name mismatch) |
| Resource Management | INFO | Finding 11 (connection leak) |

---

## 4. Finding Count by Severity

| Severity | Count | Findings |
|----------|-------|---------|
| CRITICAL | 1 | #1 (CSRF) |
| HIGH | 4 | #2 (IDOR edit/delete), #3 (IDOR isVehicleAssigned), #4 (no input validation), #5 (SQL injection in DAO) |
| MEDIUM | 3 | #6 (weak auth/no role check), #7 (null session NPE), #8 (missing Content-Type) |
| LOW | 2 | #9 (forward name mismatch), #10 (stack traces) |
| INFO | 1 | #11 (connection leak) |
| **TOTAL** | **11** | |
