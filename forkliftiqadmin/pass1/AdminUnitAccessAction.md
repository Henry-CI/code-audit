# Security Audit Report: AdminUnitAccessAction.java

**Audit Run:** audit/2026-02-26-01
**Branch:** master
**Date:** 2026-02-26
**Auditor:** Automated Pass 1
**Stack:** Apache Struts 1.3.10, PreFlightActionServlet auth gate, no Spring Security

---

## 1. Reading Evidence

### 1.1 Package and Class

| Item | Value |
|------|-------|
| Package | `com.action` |
| Class | `AdminUnitAccessAction` |
| Superclass | `com.action.PandoraAction` (extends `org.apache.struts.action.Action`) |
| File | `src/main/java/com/action/AdminUnitAccessAction.java` |

### 1.2 Public / Protected Methods

| Line | Signature |
|------|-----------|
| 17 | `public ActionForward execute(ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response) throws Exception` |

No other public or protected methods are defined in this class. Inherited helpers from `PandoraAction`: `getRequestParam`, `getLongRequestParam`, `getSessionAttribute`, `getLongSessionAttribute`, `getCompId`.

### 1.3 DAOs / Services Called

| Line | Call | Description |
|------|------|-------------|
| 27 | `UnitDAO.saveUnitAccessInfo(unitBean)` | Updates `accessible`, `access_type`, `access_id`, `keypad_reader`, `facility_code` on a unit row identified by `unitBean.getId()` |
| 29 | `UnitDAO.getUnitById(accessForm.getId()).get(0)` | Fetches a full `UnitBean` by raw user-supplied `id`; no `.get(0)` guard |
| 33 | `UnitDAO.getAllUnitsByCompanyId(companyId)` | Fetches all active units for the session company to populate a list |

### 1.4 Form Class

`com.actionform.AdminUnitAccessForm` (`src/main/java/com/actionform/AdminUnitAccessForm.java`)

Fields bound from HTTP request parameters:

| Field | Type | Notes |
|-------|------|-------|
| `id` | `String` | Unit primary-key identifier — user-controlled |
| `accessible` | `boolean` | Access flag |
| `access_type` | `String` | Free text |
| `keypad_reader` | `String` | Converted via `KeypadReaderModel.valueOf()` — can throw `IllegalArgumentException` |
| `facility_code` | `String` | Free text |
| `access_id` | `String` | Free text |

`validate()` (lines 33-37): Returns an empty `ActionErrors` with no actual checks performed.

### 1.5 Struts-Config Mapping

Source: `src/main/webapp/WEB-INF/struts-config.xml`, lines 511-519.

```xml
<action
    path="/adminunitaccess"
    name="adminUnitAccessForm"
    scope="request"
    type="com.action.AdminUnitAccessAction"
    validate="true"
    input="UnitAccessDefinition">
  <forward name="success" path="UnitAccessDefinition"/>
  <forward name="failure" path="UnitAccessDefinition"/>
</action>
```

| Attribute | Value | Security Implication |
|-----------|-------|----------------------|
| `path` | `/adminunitaccess` | Endpoint path |
| `scope` | `request` | Form bean is request-scoped (correct) |
| `validate` | `true` | Struts will call `AdminUnitAccessForm.validate()` — but that method is a no-op |
| `roles` | **not set** | No declarative role check in struts-config |
| `input` | `UnitAccessDefinition` | Validation failure redirect target |

`adminUnitAccessForm` is **not present** in `validation.xml` (which covers only `loginActionForm`, `adminRegisterActionForm`, and `AdminDriverEditForm`). Framework-level field validation is therefore entirely absent.

---

## 2. Audit Findings

---

### FINDING-01

**Severity:** CRITICAL
**Category:** Insecure Direct Object Reference (IDOR)
**File:** `src/main/java/com/action/AdminUnitAccessAction.java`
**Lines:** 26-30

**Description:**
The action accepts a unit `id` directly from user-controlled form input and uses it to both read (`getUnitById`) and write (`saveUnitAccessInfo`) unit records without ever verifying that the target unit belongs to the authenticated user's company. An attacker can supply any integer `id` to read or overwrite access-control settings (keypad reader model, facility code, access ID, accessibility flag) on units belonging to any other company in the database.

**Evidence:**

```java
// Line 26-27 (save path): id comes from accessForm which is bound to the HTTP request
UnitBean unitBean = accessForm.getUnit(sessCompId);   // comp_id is taken from session,
UnitDAO.saveUnitAccessInfo(unitBean);                 // but id is taken from the form

// Line 29 (load path): raw form id used — no company filter
UnitBean unitBean = UnitDAO.getUnitById(accessForm.getId()).get(0);

// UnitDAO.getUnitById (UnitDAO.java line 288-291):
public static List<UnitBean> getUnitById(String id) throws SQLException {
    return UnitsByIdQuery.prepare(Integer.parseInt(id)).query();
}

// UnitsByIdQuery.java line 14: no company predicate
private static final String query = "SELECT * FROM v_units WHERE id = ?";
```

On the save path the `UnitBean` carries the session `comp_id` (line 26), but `saveUnitAccessInfo` (UnitDAO.java lines 513-527) issues:

```sql
UPDATE unit SET accessible=?, access_type=?, access_id=?, keypad_reader=?, facility_code=?
WHERE id=?
```

The `WHERE` clause uses only `id`; `comp_id` is not included. Setting `comp_id` on the bean does not constrain the UPDATE. An attacker authenticated to company A can therefore write access-control data onto a unit belonging to company B by supplying company B's unit `id`.

**Recommendation:**
1. After `getUnitById`, assert that `unitBean.getComp_id().equals(sessCompId)` before proceeding; return an error forward if they differ.
2. Modify `saveUnitAccessInfo` (or its SQL) to include `AND comp_id = ?` in the WHERE clause so the database enforces tenancy even if the Java check is bypassed.
3. Apply the same fix to the `getAllUnitsByCompanyId` list call — while that call is correctly scoped by `companyId`, its result must not be used to infer that the `id` param is valid.

---

### FINDING-02

**Severity:** HIGH
**Category:** Authentication — Null Session / NullPointerException leading to authentication bypass
**File:** `src/main/java/com/action/AdminUnitAccessAction.java`
**Lines:** 18-21

**Description:**
`request.getSession(false)` (line 18) returns `null` when no session exists. The code dereferences `session` on line 19 without a null guard, causing a `NullPointerException`. The global exception handler in struts-config.xml catches `java.lang.Exception` subtypes only for `SQLException`, `IOException`, and `ServletException`; an NPE is none of these and propagates as an unchecked `RuntimeException`. Depending on the container error-page configuration this can result in a 500 response that partially or fully reveals stack-trace information, or it may bypass the intended auth flow if the container swallows the exception and falls through to the `super.doGet` path in `PreFlightActionServlet`.

More importantly, even when a session exists, line 19 replaces a null `sessCompId` with an empty string `""`, and line 21 then calls `Integer.parseInt("")`, which throws `NumberFormatException`. This means any session that has `sessCompId` not set will produce an unhandled exception rather than a clean redirect to the login/expire page.

`PreFlightActionServlet.excludeFromFilter` (PreFlightActionServlet.java line 98-115) returns `true` for `/adminunitaccess.do`, so the servlet does check for `sessCompId != null`. However the action itself duplicates this check incorrectly: it converts null to `""` and then parses it, rather than redirecting or delegating to the global auth gate result.

**Evidence:**

```java
// Line 18: may return null
HttpSession session = request.getSession(false);

// Line 19: NPE if session is null; converts null sessCompId to ""
String sessCompId = session.getAttribute("sessCompId") == null ? "" : (String) session.getAttribute("sessCompId");

// Line 21: NumberFormatException when sessCompId is ""
int companyId = Integer.parseInt(sessCompId);
```

`PandoraAction.getCompId()` (PandoraAction.java lines 41-43) handles this correctly by returning `null` rather than `""`, but `AdminUnitAccessAction` does not use it.

**Recommendation:**
1. Use `PandoraAction.getCompId(session)` which already handles null cleanly.
2. Add an explicit null/empty guard: if `sessCompId` is null or empty, return `mapping.findForward("failure")` or redirect to the expire page before performing any business logic.
3. Guard `session` itself: if `request.getSession(false)` returns null, redirect immediately.

---

### FINDING-03

**Severity:** HIGH
**Category:** Input Validation — No-op `validate()` and absent framework validation
**Files:**
- `src/main/java/com/actionform/AdminUnitAccessForm.java` lines 33-37
- `src/main/webapp/WEB-INF/validation.xml` (entire file)
- `src/main/webapp/WEB-INF/struts-config.xml` lines 511-519

**Description:**
Although the struts-config mapping declares `validate="true"`, the `AdminUnitAccessForm.validate()` method unconditionally returns an empty `ActionErrors` object, performing zero validation. Additionally, `adminUnitAccessForm` has no corresponding `<form>` entry in `validation.xml`, so the Commons Validator plug-in also performs no checks. The following fields reach action logic completely unvalidated:

- `id` — should be a positive integer; currently any string (including SQL fragments, negative values, or empty string) is accepted.
- `access_type`, `access_id`, `facility_code` — unbounded free-text strings with no length or character-set constraints.
- `keypad_reader` — passed directly to `KeypadReaderModel.valueOf()` (AdminUnitAccessForm.java line 46), throwing an uncaught `IllegalArgumentException` on any unexpected value, resulting in an unhandled 500 error.

**Evidence:**

```java
// AdminUnitAccessForm.java lines 33-37
public ActionErrors validate(ActionMapping mapping, HttpServletRequest request) {
    ActionErrors errors = new ActionErrors();
    return errors;  // always empty; no checks
}

// AdminUnitAccessForm.java line 46 — unguarded enum conversion
.keypad_reader(StringUtils.isNotBlank(keypad_reader) ? UnitBean.KeypadReaderModel.valueOf(keypad_reader) : null)
```

```xml
<!-- validation.xml: adminUnitAccessForm is absent -->
<formset>
    <form name="loginActionForm">...</form>
    <form name="adminRegisterActionForm">...</form>
    <form name="AdminDriverEditForm">...</form>
</formset>
```

**Recommendation:**
1. Implement real validation in `AdminUnitAccessForm.validate()`: require `id` to match `\d+`, enforce maximum lengths on string fields, validate `access_type` against an allowlist.
2. Wrap `KeypadReaderModel.valueOf(keypad_reader)` in a try-catch and return a validation error rather than throwing.
3. Add a `<form name="adminUnitAccessForm">` block to `validation.xml` covering at least `id` (required, integer) and string field lengths.

---

### FINDING-04

**Severity:** HIGH
**Category:** CSRF — No token protection on state-changing operation
**File:** `src/main/java/com/action/AdminUnitAccessAction.java` lines 25-27
**File:** `src/main/webapp/WEB-INF/struts-config.xml` lines 511-519

**Description:**
The `save` path (line 25-27) modifies physical access-control settings on forklift units (keypad reader model, facility code, access card ID, and the `accessible` flag). There is no CSRF token check anywhere in this action, in `PandoraAction`, in `PreFlightActionServlet`, or in the struts-config mapping. The application uses no CSRF filter. A forged cross-site POST from any page the authenticated admin visits can silently disable keypad access on arbitrary units or overwrite access-card credentials. This is a known structural gap in the stack, confirmed by the absence of any token infrastructure.

**Evidence:**
- No `_token` or equivalent parameter checked in `AdminUnitAccessAction.execute()`.
- No `CsrfFilter` or equivalent in `PreFlightActionServlet`.
- struts-config has no CSRF plug-in.
- The operation mutates physical security hardware configuration (`accessible`, `facility_code`, `access_id`), making exploitation impact especially high.

**Recommendation:**
Implement the Synchronizer Token Pattern: generate a per-session or per-form token, embed it as a hidden field, and verify it at the top of the `execute()` method before any state mutation. As a minimum mitigation, check `Content-Type` and `Referer` headers, though these are weaker controls.

---

### FINDING-05

**Severity:** HIGH
**Category:** SQL Injection (in UnitDAO — reachable from this action's context)
**File:** `src/main/java/com/dao/UnitDAO.java`
**Lines:** 211-216, 311, 349, 548, 627-628, 667-668

**Description:**
`AdminUnitAccessAction` itself calls only parameterized methods (`getUnitById` via prepared statement, `saveUnitAccessInfo` via prepared statement, `getAllUnitsByCompanyId` via query builder). The three calls made by this action do not introduce direct SQL injection. However, `UnitDAO` contains multiple methods that concatenate user-controlled strings directly into SQL, and those methods are reachable from other actions sharing the same DAO. This finding is recorded here to document the DAO's overall risk posture as context for the access action.

Specifically within UnitDAO.java:

| Line(s) | Method | Injection Vector |
|---------|--------|-----------------|
| 211-216 | `getUnitBySerial` | `serial_no` concatenated: `"...where serial_no = '" + serial_no + "'"` |
| 311 | `getUnitNameByComp` | `compLst` (built from `getSubCompanyLst`) concatenated into `IN (...)` clause |
| 349 | `delUnitById` | `id` concatenated: `"...where id=" + id` |
| 548 | `getTotalUnitByID` | `compLst` concatenated into `IN (...)` clause |
| 627-628 | `getType` | `manu_id` concatenated |
| 667-668 | `getPower` | `manu_id`, `type_id` concatenated |

**Recommendation:**
Convert all string-concatenation SQL in UnitDAO to parameterized `PreparedStatement` calls. This is outside the direct scope of `AdminUnitAccessAction` but is a mandatory remediation for the DAO as a whole.

---

### FINDING-06

**Severity:** MEDIUM
**Category:** Error Handling / Data Exposure — Unguarded list access causes unhandled exception
**File:** `src/main/java/com/action/AdminUnitAccessAction.java`
**Line:** 29

**Description:**
`UnitDAO.getUnitById(accessForm.getId()).get(0)` will throw `IndexOutOfBoundsException` if the supplied `id` does not match any row (e.g., deleted unit, non-existent ID, or an ID belonging to a different company that was not returned). This exception is unhandled and will propagate through the Struts action chain. The global exception handler in struts-config.xml does not cover `IndexOutOfBoundsException` (it only handles `SQLException`, `IOException`, `ServletException`), so a generic container error page is shown. Depending on server configuration, this may expose a full Java stack trace to the client.

**Evidence:**

```java
// Line 29: .get(0) with no size check
UnitBean unitBean = UnitDAO.getUnitById(accessForm.getId()).get(0);
```

**Recommendation:**
Check that the returned list is non-empty before calling `.get(0)`. If empty, log a warning and return `mapping.findForward("failure")`. This also partially mitigates the IDOR read path by making non-ownership result in a clean error.

---

### FINDING-07

**Severity:** MEDIUM
**Category:** Session Handling — `sessCompId` handling inconsistency
**File:** `src/main/java/com/action/AdminUnitAccessAction.java`
**Lines:** 19, 26

**Description:**
On the save path (line 26), `sessCompId` is passed to `accessForm.getUnit(sessCompId)` and stored as `comp_id` on the `UnitBean`. However, as noted in FINDING-01, `saveUnitAccessInfo` does not include `comp_id` in its WHERE clause, so the session-derived `comp_id` provides no actual tenant isolation in the database update. Additionally, `sessCompId` is retrieved via a local null-to-empty-string conversion rather than using the tested `PandoraAction.getCompId()` helper, creating a pattern divergence that increases maintenance risk.

**Evidence:**

```java
// Line 19: local pattern, diverges from PandoraAction.getCompId()
String sessCompId = session.getAttribute("sessCompId") == null ? "" : (String) session.getAttribute("sessCompId");

// UnitDAO.java lines 513-527: comp_id not in WHERE clause
private static final String UPDATE_UNIT_ACCESS =
    "update unit set accessible = ?, access_type = ?, access_id = ?, keypad_reader = ?, facility_code = ? " +
    "where id= ?";   // <-- no AND comp_id = ?
```

**Recommendation:**
Use `PandoraAction.getCompId(session)` consistently across all actions. Add `comp_id` to the WHERE clause of `UPDATE_UNIT_ACCESS` (see also FINDING-01).

---

### FINDING-08

**Severity:** MEDIUM
**Category:** Authentication — No role-based access control
**File:** `src/main/webapp/WEB-INF/struts-config.xml` lines 511-519
**File:** `src/main/java/com/action/AdminUnitAccessAction.java` (entire execute method)

**Description:**
The struts-config mapping for `/adminunitaccess` declares no `roles` attribute. The action itself performs no programmatic role check. `PreFlightActionServlet` verifies only that `sessCompId != null`; it does not check whether the authenticated user holds an admin or unit-manager role. Any authenticated user — regardless of their privilege level within a company — can invoke this action and modify keypad access-control settings on forklift units.

**Evidence:**

```xml
<!-- struts-config.xml lines 511-519: no roles attribute -->
<action
    path="/adminunitaccess"
    name="adminUnitAccessForm"
    scope="request"
    type="com.action.AdminUnitAccessAction"
    validate="true"
    input="UnitAccessDefinition">
```

```java
// AdminUnitAccessAction.java lines 17-37: no session role attribute checked
// No: session.getAttribute("sessRole"), session.getAttribute("userRole"), etc.
```

**Recommendation:**
Check a session-stored role attribute (e.g., `sessRole`) at the top of `execute()` and return `mapping.findForward("failure")` for non-admin users. Alternatively add a `roles` attribute to the struts-config mapping if the container's security-constraint mechanism is wired to enforce it.

---

### FINDING-09

**Severity:** LOW
**Category:** Data Exposure — Sensitive hardware credentials in request-scoped form bean
**File:** `src/main/java/com/actionform/AdminUnitAccessForm.java`
**Lines:** 28-31

**Description:**
Fields `facility_code` and `access_id` represent physical access-control credentials for keypad reader systems (ROSLARE, KERI, SMART, HID_ICLASS). These are stored in a request-scoped Struts form bean, which means they are accessible as request attributes and may be logged by access-log middleware, appear in Struts error pages, or be visible in JSP EL expressions that dump the form bean. There is no masking or redaction applied anywhere in the data path.

**Recommendation:**
Treat `facility_code` and `access_id` as sensitive credentials. Avoid logging them. Ensure JSP templates render them only in contexts that require them (e.g., not in error pages or debug dumps). Consider encrypting them at rest in the database column.

---

### FINDING-10

**Severity:** INFO
**Category:** SQL Injection — Action-direct DAO calls use parameterized queries

`UnitDAO.getUnitById` (via `UnitsByIdQuery`) and `UnitDAO.saveUnitAccessInfo` both use `PreparedStatement` with positional parameters. `UnitDAO.getAllUnitsByCompanyId` delegates to `UnitsByCompanyIdQuery` which also uses parameterized queries. No SQL injection is introduced directly by the three DAO calls made within `AdminUnitAccessAction.execute()`.

---

### FINDING-11

**Severity:** INFO
**Category:** CSRF — Structural gap applies to entire application

As documented in FINDING-04, the absence of CSRF protection is an application-wide structural gap acknowledged in the audit stack description. All state-changing actions in the application share this risk. No action-specific mitigation exists for `/adminunitaccess`.

---

## 3. Category Summary

| Category | Status | Finding(s) |
|----------|--------|------------|
| Authentication (sessCompId check) | ISSUE | FINDING-02 (NPE / parse error on missing sessCompId), FINDING-08 (no role check) |
| Authentication (order vs DB calls) | ISSUE | FINDING-02 (DB calls execute before auth validation completes safely) |
| CSRF | ISSUE | FINDING-04 |
| Input Validation | ISSUE | FINDING-03 |
| SQL Injection (action-direct calls) | NO ISSUES | FINDING-10 (INFO) |
| SQL Injection (DAO — broader context) | ISSUE | FINDING-05 |
| IDOR | ISSUE | FINDING-01 (CRITICAL) |
| Session Handling | ISSUE | FINDING-07 |
| Data Exposure | ISSUE | FINDING-06 (stack trace), FINDING-09 (hardware credentials) |

---

## 4. Finding Count by Severity

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 1 | FINDING-01 |
| HIGH | 4 | FINDING-02, FINDING-03, FINDING-04, FINDING-05 |
| MEDIUM | 3 | FINDING-06, FINDING-07, FINDING-08 |
| LOW | 1 | FINDING-09 |
| INFO | 2 | FINDING-10, FINDING-11 |
| **TOTAL** | **11** | |
