# Security Audit: AdminUnitEditAction.java
**Audit run:** audit/2026-02-26-01
**Branch:** master
**Date:** 2026-02-26
**Auditor:** Pass 1 automated review

---

## 1. Reading Evidence

### Package and Class
- **File:** `src/main/java/com/action/AdminUnitEditAction.java`
- **Package:** `com.action`
- **Class:** `AdminUnitEditAction extends org.apache.struts.action.Action`

### Public / Protected Methods (with line numbers)

| Line | Visibility | Method Signature |
|------|------------|-----------------|
| 22   | public     | `ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` |
| 72   | private    | `void writeJsonResponse(HttpServletResponse, Boolean)` |
| 78   | private    | `String validate(String compId, AdminUnitEditForm, UnitBean)` |

### DAOs / Services Called

| Call site (Action line) | DAO / Method | Purpose |
|------------------------|--------------|---------|
| 20 (field init)        | `UnitDAO.getInstance()` | Singleton instance stored as field |
| 34                     | `ManufactureDAO.getInstance().getAllManufactures(compId)` | Populate manufacturer dropdown |
| 37                     | `UnitDAO.getInstance().checkUnitByNm(compId, name, null, true)` | AJAX: unit name exists check |
| 41                     | `UnitDAO.getInstance().checkUnitBySerial(serial_no, null, true, compId)` | AJAX: serial number exists check |
| 45                     | `UnitDAO.getInstance().checkUnitByMacAddr(mac_address, null)` | AJAX: MAC address exists check |
| 54                     | `unitDao.getAllUnitsByCompanyId(companyId)` | Populate list on validation failure |
| 59                     | `unitDao.saveUnitInfo(unitBean)` | INSERT or UPDATE the unit |
| 60                     | `unitDao.getAllUnitsByCompanyId(companyId)` | Populate list on success |
| 79 (validate)          | `unitDao.checkUnitByNm(compId, name, id, true)` | Duplicate name check |
| 82 (validate)          | `unitDao.checkUnitBySerial(serial_no, id, true, compId)` | Duplicate serial check |
| 86 (validate)          | `unitDao.checkUnitByMacAddr(macAddr, id)` | Duplicate MAC check |

### Form Class
- `com.actionform.AdminUnitEditForm` (form-bean: `adminUnitEditForm`)
- Fields: `id`, `name`, `location`, `department`, `type_id`, `active`, `manu_id`, `size`, `hourmeter`, `serial_no`, `fuel_type_id`, `mac_address`, `exp_mod`, `accessible`, `access_type`, `keypad_reader`, `facility_code`, `access_id`, `op_code`, `weight_unit`

### Struts-config Mapping Details

| Attribute | Value |
|-----------|-------|
| Primary path | `/adminunitedit` |
| Form bean | `adminUnitEditForm` |
| Scope | `request` |
| Validate | `true` |
| Input (on validation error) | `UnitEditDefinition` |
| roles attribute | **not present** |
| forwards | `success` → `adminEquipmentDefinition`, `failure` → `adminEquipmentDefinition` |

Additional paths that **reuse the same Action class** (all `validate="false"`):

| Path | Purpose |
|------|---------|
| `/unitnameexists` | AJAX unit-name duplicate check |
| `/serialnoexists` | AJAX serial-number duplicate check |
| `/macaddressexists` | AJAX MAC-address duplicate check |

---

## 2. Findings

---

### FINDING-01 — CRITICAL: No Role-Based Access Control on Any Mapping

**Severity:** CRITICAL
**File:** `src/main/webapp/WEB-INF/struts-config.xml`, lines 332–341 (primary) and 352–372 (AJAX paths)
**Also:** `src/main/java/com/action/AdminUnitEditAction.java` (entire execute method)

**Description:**
The struts-config action mappings for `/adminunitedit`, `/unitnameexists`, `/serialnoexists`, and `/macaddressexists` carry **no `roles` attribute**. Struts 1 declarative role enforcement (via `ActionMapping.getRoles()`) is therefore absent. The `AdminUnitEditAction.execute()` method itself performs **no programmatic role check** — it reads `sessCompId` from session but never reads a role or privilege attribute to confirm the caller is an administrator rather than a regular operator or a cross-tenant user.

**Evidence:**
```xml
<!-- struts-config.xml lines 332-341 -->
<action
    path="/adminunitedit"
    name="adminUnitEditForm"
    scope="request"
    type="com.action.AdminUnitEditAction"
    validate="true"
    input="UnitEditDefinition">
    <!-- no roles="" attribute -->
```
```java
// AdminUnitEditAction.java lines 27-30
HttpSession session = request.getSession(false);
String compId = (String) (session.getAttribute("sessCompId") == null ? "" : session.getAttribute("sessCompId"));
UnitBean unitBean = adminUnitEditForm.getUnit(compId);
int companyId = Integer.parseInt(compId);
// no check of sessRole, sessUserType, or equivalent
```

**Recommendation:**
Add a `roles="ADMIN"` (or the application's admin role constant) attribute to each mapping. Additionally add a programmatic guard at the top of `execute()`: read the role attribute from session (e.g., `sessUserType`) and forward to an error page if the caller is not an administrator. Use a shared helper or base class to enforce this consistently across all admin actions.

---

### FINDING-02 — CRITICAL: Null-Pointer / Integer.parseInt Exception on Empty sessCompId — Pre-Condition Reached Before Auth Guard

**Severity:** CRITICAL
**File:** `src/main/java/com/action/AdminUnitEditAction.java`, lines 28–30

**Description:**
The action reads `sessCompId` from the session with a null-coalesce that substitutes an **empty string** when the attribute is missing:

```java
String compId = (String) (session.getAttribute("sessCompId") == null ? "" : session.getAttribute("sessCompId"));
```

On the very next executable line (`Integer.parseInt(compId)`, line 30) and before any AJAX short-circuit branches are evaluated, the code calls `adminUnitEditForm.getUnit(compId)` (line 29) which passes the empty string into `UnitBean.builder().comp_id(compId)`. Shortly after, line 30 calls `Integer.parseInt("")` which throws `NumberFormatException`, causing an unhandled exception that leaks a stack trace to the caller. More critically this means that:

1. A session without `sessCompId` is **not rejected early** — instead the action proceeds into DAO calls with a potentially empty/null company ID.
2. The PreFlightActionServlet does guard `sessCompId == null` (line 56 of `PreFlightActionServlet.java`), but only for GET requests routed through it; a direct POST constructed to bypass that path would reach the action.

**Evidence:**
```java
// AdminUnitEditAction.java line 28-30
String compId = (String) (session.getAttribute("sessCompId") == null ? "" : session.getAttribute("sessCompId"));
UnitBean unitBean = adminUnitEditForm.getUnit(compId);  // empty string passed
int companyId = Integer.parseInt(compId);               // NumberFormatException if ""
```

**Recommendation:**
Explicitly validate `sessCompId` at the top of `execute()`. If it is null or blank, immediately forward to the session-expired page. Never substitute an empty string — it creates a false sense of safety while still allowing downstream errors. Example:
```java
Object rawCompId = session != null ? session.getAttribute("sessCompId") : null;
if (rawCompId == null || rawCompId.toString().isBlank()) {
    return mapping.findForward("sessionExpired");
}
String compId = rawCompId.toString();
```

---

### FINDING-03 — HIGH: CSRF — No Token Protection on Unit Create/Update

**Severity:** HIGH
**File:** `src/main/webapp/WEB-INF/struts-config.xml` lines 332–341; `src/main/java/com/action/AdminUnitEditAction.java` lines 22–70

**Description:**
The `/adminunitedit` action performs **state-changing database writes** (INSERT and UPDATE on the `unit` table via `saveUnitInfo`) using only `POST` (form submission). There is no CSRF token generated, embedded in the form, or validated before the write is executed. An attacker who can lure an authenticated admin to visit a crafted page can silently create or overwrite forklift unit records in the victim's company.

This is a structural gap acknowledged in the audit stack description — it is confirmed present for this action.

**Evidence:**
- `struts-config.xml`: no token-based `validate` plugin or custom interceptor is configured.
- `AdminUnitEditAction.java` line 59: `unitDao.saveUnitInfo(unitBean)` executes with no prior token check.
- `AdminUnitEditForm.java`: no token field present.

**Recommendation:**
Implement Struts 1 CSRF token idiom: call `saveToken(request)` when rendering the edit form and `isTokenValid(request, true)` at the start of the mutating `execute()` path. Alternatively, migrate to a framework-level CSRF filter (e.g., OWASP CSRFGuard) applied globally.

---

### FINDING-04 — HIGH: IDOR — Unit ID Not Verified Against Session Company on Update

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminUnitEditAction.java`, lines 29, 59; `src/main/java/com/dao/UnitDAO.java`, lines 467–511

**Description:**
When a unit ID is submitted in the form (`AdminUnitEditForm.id`), the action passes it directly into `unitBean.getId()` and then into `updateUnitInfo()`. The `UPDATE_UNIT` SQL (UnitDAO.java line 467–470) filters **only by `id`**, not by `comp_id`:

```sql
update unit set name = ?, location = ?, department = ?, type_id = ?, manu_id = ?,
    fuel_type_id = ?, size = ?, hourmeter = ?, serial_no = ?, mac_address = ?, weight_unit = ?
    where id = ?
```

An authenticated admin for company A can craft a POST to `/adminunitedit` with `id` set to a unit belonging to company B. The update will succeed because no ownership check is performed — neither in the action nor in the DAO. The `comp_id` is taken from session (correctly) for the new-insert path, but for the update path the `comp_id` column is not written and not verified.

**Evidence:**
```java
// AdminUnitEditAction.java line 59
if (unitDao.saveUnitInfo(unitBean)) { ... }  // unitBean.id comes unverified from form input
```
```sql
-- UnitDAO.java lines 467-470
update unit set name=?,location=?,department=?,type_id=?,manu_id=?,
    fuel_type_id=?,size=?,hourmeter=?,serial_no=?,mac_address=?,weight_unit=?
    where id=?
    -- no "and comp_id=?" clause
```

**Recommendation:**
Before invoking `saveUnitInfo` for the update path, verify that the submitted unit ID belongs to the session company. Either:
(a) Add `AND comp_id = ?` to the `UPDATE_UNIT` SQL and verify that `executeUpdate()` returns exactly 1 row (already done in terms of row-count check, but the company constraint is missing), or
(b) Call `getUnitById(id)` first and confirm the returned unit's `comp_id` matches `sessCompId` before proceeding. Option (a) is preferred.

---

### FINDING-05 — HIGH: SQL Injection in UnitDAO.getUnitBySerial (Called Indirectly)

**Severity:** HIGH
**File:** `src/main/java/com/dao/UnitDAO.java`, lines 210–217

**Description:**
`UnitDAO.getUnitBySerial()` constructs a SQL query via string concatenation using the caller-supplied `serial_no` parameter:

```java
String sql = "select id,comp_id from unit where serial_no = '" + serial_no + "'";
```

This method is not called directly from `AdminUnitEditAction`, but it is part of the same DAO that is used throughout the application, and the pattern establishes that raw string concatenation is an accepted practice in this codebase. More importantly, while the action-level paths (`checkUnitByNm`, `checkUnitBySerial`, `checkUnitByMacAddr`) themselves use `PreparedStatement` parameters, there is a real risk that future callers — or current callers elsewhere in the codebase — will pass user-controlled data into `getUnitBySerial`. The method is `public`, takes a raw `String`, and provides no sanitisation.

**Recommendation:**
Rewrite `getUnitBySerial` to use a `PreparedStatement` with `?` placeholder. Audit all other `Statement`-based methods in `UnitDAO` (`getUnitNameByComp` at line 311, `getTotalUnitByID` at line 548, `getType` at line 627, `getPower` at line 667, `delUnitById` at line 349) which also use string concatenation and are directly injectable if attacker-controlled values reach them.

---

### FINDING-06 — HIGH: SQL Injection in UnitDAO.delUnitById (Sibling Method, Same Class)

**Severity:** HIGH
**File:** `src/main/java/com/dao/UnitDAO.java`, line 349

**Description:**
`delUnitById` constructs a soft-delete UPDATE using raw string concatenation with the `id` parameter:

```java
String sql = "update unit set active = false where id=" + id;
```

Although `id` values in normal flow are numeric primary keys, the method signature accepts `String id` with no numeric validation. If an attacker controls this value (e.g., via IDOR exploitation or a separate injection surface), they can append SQL to affect arbitrary rows. This is a critical companion risk to FINDING-04.

**Recommendation:**
Replace with `PreparedStatement`: `"update unit set active = false where id = ?"` with `ps.setLong(1, Long.parseLong(id))`.

---

### FINDING-07 — MEDIUM: MAC Address Existence Check Does Not Scope to Session Company

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminUnitEditAction.java`, line 45; `src/main/java/com/dao/UnitDAO.java`, lines 179–196

**Description:**
The AJAX duplicate-check for MAC address (`opCode = "macaddressexists"`, path `/macaddressexists`) calls:

```java
Boolean exists = UnitDAO.getInstance().checkUnitByMacAddr(adminUnitEditForm.getMac_address(), null, compId);
```

However, `checkUnitByMacAddr` signature is `(String macAddr, String id)` — it does **not** accept or use `compId`. The underlying SQL (`QUERY_COUNT_UNIT_BY_MAC_ADDRESS`) searches the entire `unit` table across all companies:

```sql
select count(id) from unit u where trim(both ' ' from u.mac_address) ilike trim(both ' ' from ?) and active = true
```

This means:
1. A MAC address belonging to a unit in company B will appear as "already taken" to an admin in company A, leaking the existence of that MAC address across tenant boundaries (information disclosure).
2. It prevents legitimate reuse of a MAC address if a unit is deactivated in another company.

**Evidence:**
```java
// AdminUnitEditAction.java line 45
Boolean exists = UnitDAO.getInstance().checkUnitByMacAddr(adminUnitEditForm.getMac_address(), null);
// compId is NOT passed
```

**Recommendation:**
Add a `compId` parameter to `checkUnitByMacAddr`, add `AND comp_id = ?` to the query, and pass `compId` from the action. Determine with the business whether MAC uniqueness should span all companies (an IoT hardware constraint) or only within a tenant; document the decision if global uniqueness is intended.

---

### FINDING-08 — MEDIUM: Session Retrieved with getSession(false) but Not Null-Checked Before Attribute Access

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminUnitEditAction.java`, lines 27–28

**Description:**
`request.getSession(false)` returns `null` if no session exists. The very next line dereferences `session.getAttribute(...)` without a null guard:

```java
HttpSession session = request.getSession(false);                            // line 27 — can be null
String compId = (String) (session.getAttribute("sessCompId") == null ? "" : ...); // line 28 — NPE if session is null
```

The `PreFlightActionServlet` performs a null check before forwarding, but if the request reaches the action through any path that bypasses the preflight (e.g., a direct POST, an in-container forward, or a unit test), the action will throw a `NullPointerException`, generating an unhandled 500 error. This behaviour is also visible to users as a stack trace if `global-exceptions` mapping does not cover `NullPointerException` (the `global-exceptions` block in `struts-config.xml` only covers `SQLException`, `IOException`, and `ServletException`).

**Evidence:**
```java
HttpSession session = request.getSession(false);  // line 27
String compId = (String) (session.getAttribute("sessCompId") == null ? "" : ...);  // line 28 — NullPointerException if session==null
```
```xml
<!-- struts-config.xml lines 42-55: NullPointerException is NOT listed -->
<global-exceptions>
    <exception key="errors.global" type="java.sql.SQLException" .../>
    <exception key="errors.global" type="java.io.IOException" .../>
    <exception key="errors.global" type="javax.servlet.ServletException" .../>
</global-exceptions>
```

**Recommendation:**
Add an explicit null check immediately after `getSession(false)`. Forward to the session-expired page if `session == null`. This check belongs before any attribute access.

---

### FINDING-09 — MEDIUM: Struts Validator Not Configured for adminUnitEditForm

**Severity:** MEDIUM
**File:** `src/main/webapp/WEB-INF/validation.xml` (entire file); `src/main/webapp/WEB-INF/struts-config.xml` line 337

**Description:**
The mapping for `/adminunitedit` declares `validate="true"`, which triggers the Struts Validator framework before calling `execute()`. However, `validation.xml` contains no `<form name="adminUnitEditForm">` entry. The Validator plugin therefore performs **no declarative field-level validation** for this form.

The form class `AdminUnitEditForm.validate()` (ActionForm method) does perform some Java-side checks (empty name, empty serial_no, empty manu_id, empty type_id, empty fuel_type_id, numeric regex on `size`) but:
- Fields `location`, `department`, `hourmeter`, `mac_address`, `exp_mod`, `access_type`, `keypad_reader`, `facility_code`, `access_id`, `weight_unit` are **entirely unchecked** for length, format, or character set.
- No maximum-length constraint is enforced on any field before it reaches the database layer. A very long value (e.g., >255 characters) will either cause a database truncation error or, in a permissive schema, be stored as-is, potentially enabling stored XSS.
- `op_code` is compared case-insensitively against three known values (lines 36–47) but an unknown value silently falls through to the save path.

**Recommendation:**
Add a `<form name="adminUnitEditForm">` block to `validation.xml` with `maxlength` and (where appropriate) `mask` constraints on all user-supplied fields. At minimum constrain `name`, `serial_no`, `mac_address`, `location`, and `department`. Also add a whitelist check on `op_code` so that unexpected values are rejected rather than silently falling through.

---

### FINDING-10 — MEDIUM: Response Content-Type Not Set for JSON AJAX Responses

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminUnitEditAction.java`, lines 72–76

**Description:**
The `writeJsonResponse` helper writes a plain boolean string (`"true"` or `"false"`) to the response without setting `Content-Type`:

```java
private void writeJsonResponse(HttpServletResponse response, Boolean result) throws IOException {
    PrintWriter writer = response.getWriter();
    writer.write(result.toString());
    writer.flush();
}
```

The absence of `response.setContentType("application/json; charset=UTF-8")` means the browser will apply content-type sniffing to the response. In older or misconfigured browsers this can result in the response being interpreted as HTML, enabling a content-sniffing XSS attack if an attacker can influence the response body. The response also does not set `X-Content-Type-Options: nosniff`.

**Recommendation:**
Add `response.setContentType("application/json; charset=UTF-8")` before calling `getWriter()`. Set `response.setHeader("X-Content-Type-Options", "nosniff")` globally in a filter.

---

### FINDING-11 — LOW: UnitDAO Singleton Uses Unsafe Double-Checked Locking Without Volatile

**Severity:** LOW
**File:** `src/main/java/com/dao/UnitDAO.java`, lines 26–35

**Description:**
The double-checked locking pattern used to initialise the `UnitDAO` singleton omits the `volatile` keyword on the `theInstance` field:

```java
private static UnitDAO theInstance;   // not volatile

public static UnitDAO getInstance() {
    if (theInstance == null) {
        synchronized (UnitDAO.class) {
            if (theInstance == null) {
                theInstance = new UnitDAO();
            }
        }
    }
    return theInstance;
}
```

Without `volatile`, the Java Memory Model does not guarantee that the fully constructed object is visible to threads that see `theInstance != null` due to instruction reordering. This can result in a thread receiving a partially initialised instance. This pattern is broken in Java 1–4 and requires `volatile` to be safe in Java 5+.

**Recommendation:**
Declare `private static volatile UnitDAO theInstance;` or use an initialisation-on-demand holder idiom:
```java
private static class Holder {
    static final UnitDAO INSTANCE = new UnitDAO();
}
public static UnitDAO getInstance() { return Holder.INSTANCE; }
```

---

### FINDING-12 — LOW: Information Disclosure via Stack Traces on Exception

**Severity:** LOW
**File:** `src/main/java/com/dao/UnitDAO.java` (multiple catch blocks, e.g., lines 226, 324, 356); `src/main/java/com/action/AdminUnitEditAction.java` line 25 (`throws Exception`)

**Description:**
Multiple DAO catch blocks call `e.printStackTrace()` in addition to the logger. In a servlet container, `System.err` (used by `printStackTrace()`) may be directed to the container's log, which can end up in a response or accessible to attackers via other means. The action's `throws Exception` declaration means any unhandled exception propagates to Struts and then to the container's error-handling layer. The `global-exceptions` mapping covers only `SQLException`, `IOException`, and `ServletException` — a `RuntimeException` or `NumberFormatException` (see FINDING-02) will produce an unformatted container error page that may expose internal class names, file paths, and query fragments.

**Recommendation:**
Remove all `e.printStackTrace()` calls from DAO code; logging via the existing `InfoLogger` is sufficient. Ensure the container is configured with a custom error page for HTTP 500. Extend `global-exceptions` to cover `RuntimeException` as a catch-all fallback.

---

## 3. Category Summary

| Category | Status | Finding(s) |
|----------|--------|-----------|
| Authentication (sessCompId check) | ISSUE | FINDING-02: empty-string substitution instead of hard reject; FINDING-08: session null not checked |
| Role-Based Access Control | ISSUE | FINDING-01: no roles attribute, no programmatic role check |
| CSRF | ISSUE | FINDING-03: no token on mutating action |
| Input Validation | ISSUE | FINDING-09: no validator.xml entry; many fields unconstrained |
| SQL Injection (action-level DAO calls) | CLEAN (prepared statements used in checkUnitByNm, checkUnitBySerial, checkUnitByMacAddr, saveUnitInfo) | — |
| SQL Injection (DAO sibling methods) | ISSUE | FINDING-05 (getUnitBySerial), FINDING-06 (delUnitById) |
| IDOR | ISSUE | FINDING-04: unit ID not verified against session company on update |
| Session Handling | ISSUE | FINDING-02, FINDING-08 |
| Data Exposure / Information Disclosure | ISSUE | FINDING-07 (cross-tenant MAC leak), FINDING-10 (content-type), FINDING-12 (stack traces) |
| Concurrency / Correctness | ISSUE | FINDING-11 (singleton volatile) |

**Note on SQL Injection for action-level calls:** The four DAO methods called directly from `AdminUnitEditAction.execute()` and `validate()` — `checkUnitByNm`, `checkUnitBySerial`, `checkUnitByMacAddr`, and `saveUnitInfo`/`updateUnitInfo` — all use parameterised `PreparedStatement` calls with `?` placeholders. No SQL injection risk exists on those specific code paths. The SQL injection findings (05, 06) are raised for other methods in the same DAO class that could be reached from other actions.

---

## 4. Finding Count by Severity

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 2     | 01, 02 |
| HIGH     | 4     | 03, 04, 05, 06 |
| MEDIUM   | 4     | 07, 08, 09, 10 |
| LOW      | 2     | 11, 12 |
| INFO     | 0     | — |
| **TOTAL**| **12**| |
