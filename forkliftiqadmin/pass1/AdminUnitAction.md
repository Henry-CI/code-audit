# Security Audit Report: AdminUnitAction.java
**Audit run:** audit/2026-02-26-01
**Pass:** 1
**Date:** 2026-02-26
**Auditor:** CIG Automated Security Audit
**Stack:** Apache Struts 1.3.10 (not Spring), PostgreSQL backend, PreFlightActionServlet auth gate

---

## 1. Reading Evidence

### 1.1 Package and Class
- **File:** `src/main/java/com/action/AdminUnitAction.java`
- **Package:** `com.action`
- **Class:** `AdminUnitAction extends org.apache.struts.action.Action`

### 1.2 Public / Protected Methods (with line numbers)

| Method | Lines | Notes |
|---|---|---|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | 27–219 | Single entry point; dispatches via `action` request parameter |

### 1.3 DAOs and Services Called

| DAO / Service | Methods Invoked | Lines |
|---|---|---|
| `UnitDAO` (singleton) | `getUnitById(equipId)` | 45, 65 |
| `UnitDAO` (singleton) | `getUnitMaxId()` | 49 |
| `UnitDAO` (singleton) | `delUnitById(equipId)` | 58 |
| `UnitDAO` (static) | `getAllUnitsByCompanyId(companyId)` | 59, 211 |
| `UnitDAO` (singleton) | `getServiceByUnitId(equipId)` | 102 |
| `UnitDAO` (static) | `getAssignments(sessCompId, equipId, dateFormat)` | 186 |
| `UnitDAO` (singleton) | `getChecklistSettings(equipId)` | 190 |
| `UnitDAO` (singleton) | `getAllUnitSearch(sessCompId, true, searchUnit)` | 213 |
| `ManufactureDAO` (static) | `getAllManufactures(sessCompId)` | 42 |
| `JobsDAO` (instance) | `getJobList(equipId)` | 64 |
| `JobsDAO` (instance) | `addJob(jobdetails)` | 80 |
| `JobsDAO` (instance) | `editJob(jobdetails)` | 95 |
| `CompanyDAO` (static) | `getSubCompanies(sessCompId)` | 185 |
| `UnitCalibrationGetterInDatabase` (instance) | `getUnitCalibration(Long.valueOf(equipId))` | 173 |

### 1.4 Form Class
The `/adminunit` action mapping in `struts-config.xml` does **not** declare a `name` attribute; no ActionForm is bound to this action. All input arrives via raw `request.getParameter()` calls. There is no Struts validator wired to this action.

### 1.5 Struts-Config Mapping Details
**Source:** `src/main/webapp/WEB-INF/struts-config.xml` lines 246–256

```xml
<action
    path="/adminunit"
    type="com.action.AdminUnitAction">
    <forward name="unitedit"     path="UnitEditDefinition"/>
    <forward name="unitlist"     path="adminEquipmentDefinition"/>
    <forward name="unitadd"      path="UnitEditDefinition"/>
    <forward name="unitfailure"  path="adminEquipmentDefinition"/>
    <forward name="unitservice"  path="UnitServiceDefinition"/>
    <forward name="unitimpact"   path="UnitImpactDefinition"/>
    <forward name="unitassignment" path="UnitAssignmentDefinition"/>
    <forward name="joblist"      path="adminJobDefinition"/>
</action>
```

| Attribute | Value | Security Implication |
|---|---|---|
| `name` (form bean) | **absent** | No ActionForm; no Struts validator can fire |
| `scope` | **absent** | No form scope defined |
| `validate` | **absent** (defaults to `true` in Struts 1.3, but without a form bean this is a no-op) | Validation effectively disabled |
| `roles` | **absent** | No declarative role check |
| `input` | **absent** | No input page for validation errors |

---

## 2. Findings

---

### FINDING-01 — CRITICAL: SQL Injection in `delUnitById` via `equipId` Parameter

**Severity:** CRITICAL
**File:** `src/main/java/com/dao/UnitDAO.java`, line 349
**Triggered from:** `src/main/java/com/action/AdminUnitAction.java`, line 58

**Description:**
`delUnitById` builds a SQL UPDATE statement by string-concatenating the `id` parameter directly into the query with no parameterisation, quoting, or numeric validation:

```java
// UnitDAO.java line 349
String sql = "update unit set active = false where id=" + id;
stmt.executeUpdate(sql);
```

The `id` value originates from `request.getParameter("equipId")` (AdminUnitAction.java line 34), which is passed to `delUnitById` at line 58 without any sanitisation or type check:

```java
// AdminUnitAction.java line 57-59
} else if (action.equalsIgnoreCase("delete")) {
    unitDAO.delUnitById(equipId);
```

An attacker can craft a request such as:
```
GET /adminunit.do?action=delete&equipId=1;DROP+TABLE+unit;--
GET /adminunit.do?action=delete&equipId=1+OR+1=1
GET /adminunit.do?action=delete&equipId=0+UNION+SELECT+...
```

The first example could execute arbitrary DDL. The second would soft-delete every active unit in the database. Boolean-blind and stacked-query injection paths are both available depending on the PostgreSQL driver and connection settings.

**Evidence:**
- `UnitDAO.java:349` — unparameterised concatenation
- `AdminUnitAction.java:34` — `equipId` taken directly from request parameter
- `AdminUnitAction.java:58` — passed raw to `delUnitById`
- No numeric guard (`Integer.parseInt`, `NumberUtils.isDigits`, etc.) applied before the call
- By contrast, the `action=add_job` branch at line 70 does call `Integer.parseInt(equipId)` before use — the `delete` branch does not

**Recommendation:**
Replace the statement in `UnitDAO.delUnitById` with a `PreparedStatement`:
```java
String sql = "UPDATE unit SET active = false WHERE id = ?";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setLong(1, Long.parseLong(id));
ps.executeUpdate();
```
Additionally, validate `equipId` as a positive integer in `AdminUnitAction.execute` before passing it to any DAO method.

---

### FINDING-02 — CRITICAL: Insecure Direct Object Reference (IDOR) — No Company Ownership Check Before Delete / Edit / View

**Severity:** CRITICAL
**File:** `src/main/java/com/action/AdminUnitAction.java`, lines 44–68, 57–61

**Description:**
Every action branch that accepts an `equipId` from the request (`edit`, `delete`, `job`, `service`, `impact`, `assignment`, `checklist`) queries or mutates the row identified by that ID without first verifying that the unit belongs to the authenticated user's company (`sessCompId`).

Concrete critical path for `delete`:
```java
// Lines 57-61
} else if (action.equalsIgnoreCase("delete")) {
    unitDAO.delUnitById(equipId);          // no ownership check
    List<UnitBean> arrUnit = UnitDAO.getAllUnitsByCompanyId(companyId);
    ...
}
```

The post-delete list is correctly scoped to `companyId`, but the delete itself is not. An authenticated user of Company A can delete units belonging to Company B simply by supplying a foreign `equipId`.

The same pattern applies to `edit` (line 45), `job` (line 64–65), `service` (line 102), `impact` (line 173), `assignment` (line 186), and `checklist` (line 190).

The `getUnitById` query (`UnitsByIdQuery`, `src/main/java/com/querybuilder/unit/UnitsByIdQuery.java`) fetches `SELECT * FROM v_units WHERE id = ?` with no company-scoped predicate, confirming there is no ownership enforcement at the DAO layer either.

**Evidence:**
- `AdminUnitAction.java:45` — `unitDAO.getUnitById(equipId)` — no company filter
- `AdminUnitAction.java:58` — `unitDAO.delUnitById(equipId)` — no company filter
- `AdminUnitAction.java:64-65` — `jobsDAO.getJobList(equipId)` / `unitDAO.getUnitById(equipId)` — no company filter
- `AdminUnitAction.java:102` — `unitDAO.getServiceByUnitId(equipId)` — no company filter
- `AdminUnitAction.java:173` — `getUnitCalibration(Long.valueOf(equipId))` — no company filter
- `AdminUnitAction.java:190` — `unitDAO.getChecklistSettings(equipId)` — no company filter
- `UnitsByIdQuery.java:14` — `SELECT * FROM v_units WHERE id = ?` — no `comp_id` predicate

**Recommendation:**
After retrieving any unit by ID, verify `unit.getComp_id().equals(sessCompId)` before returning data or performing mutations. For the delete path this check must precede the `delUnitById` call. Consider adding a `comp_id` predicate directly to `UnitsByIdQuery` and `delUnitById`.

---

### FINDING-03 — CRITICAL: SQL Injection in `UnitDAO.getUnitBySerial` (Related DAO, Same File)

**Severity:** CRITICAL
**File:** `src/main/java/com/dao/UnitDAO.java`, line 212

**Description:**
Although not directly invoked by `AdminUnitAction`, this method in the same DAO concatenates user input:

```java
String sql = "select id,comp_id from unit where serial_no = '" + serial_no + "'";
```

This is documented for completeness because it is part of the DAO under review and shares the same pattern.

**Recommendation:** Use a `PreparedStatement` with a `?` placeholder.

---

### FINDING-04 — HIGH: No CSRF Protection on State-Changing Operations

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminUnitAction.java`, lines 57–99
**Config:** `src/main/webapp/WEB-INF/struts-config.xml`, lines 246–256

**Description:**
The `/adminunit.do` action mapping has no form bean and no CSRF token mechanism. State-changing operations (`delete`, `add_job`, `edit_job`) are triggered by GET or POST requests with no synchroniser token. The application uses Apache Struts 1.3.10 without a framework-level CSRF filter. There is no Spring Security CSRF protection. An attacker can construct a cross-site request that will be silently executed in the context of a logged-in user's session.

Example: a single `<img src="https://target/adminunit.do?action=delete&equipId=42">` embedded in any page the victim visits will delete unit 42.

Note: combined with FINDING-01, a CSRF attack can also deliver a SQL injection payload without any interaction beyond page visit.

**Evidence:**
- No `name` attribute in the `/adminunit` action mapping — no form bean is populated, so Struts' built-in token mechanism (`saveToken` / `isTokenValid`) is never invoked
- `validation.xml` contains no entry for any form related to `/adminunit`
- No CSRF filter or interceptor found in `PreFlightActionServlet.java` or `struts-config.xml`
- `AdminUnitAction.java` makes no call to `isTokenValid()`

**Recommendation:**
Implement Struts 1.3 synchroniser token pattern: call `saveToken(request)` when rendering each form/action link, and call `isTokenValid(request, true)` at the start of every state-changing branch in `execute()`. Consider adding a servlet filter that enforces a CSRF header (`X-Requested-With`) or custom token for all `.do` endpoints that are not in the public exclusion list.

---

### FINDING-05 — HIGH: Null Pointer Dereference / Unauthenticated Access via `session.getAttribute` Without Session Null Check

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminUnitAction.java`, lines 30–31

**Description:**
The `execute` method calls `request.getSession(false)` (line 30), which can return `null` if no session exists. The very next line unconditionally calls `session.getAttribute("sessCompId")` (line 31) without null-checking `session` first:

```java
HttpSession session = request.getSession(false);  // may return null
String sessCompId = session.getAttribute("sessCompId") == null ? ""   // NPE if session is null
    : (String) session.getAttribute("sessCompId");
```

If `PreFlightActionServlet` is bypassed — for example, via a direct internal request, a misconfigured reverse proxy forwarding to a non-`.do` path, or during servlet container restart — any request reaching `AdminUnitAction.execute` without a live session will throw a `NullPointerException` at line 31.

Additionally, if `sessCompId` resolves to the empty string `""`, the code falls through to line 40:
```java
int companyId = Integer.parseInt(sessCompId);  // NumberFormatException on empty string
```
This throws an uncaught `NumberFormatException`, which is propagated as a generic exception and will be caught by the `global-exceptions` handler, potentially leaking a stack trace to the client or log.

The `PreFlightActionServlet` gates on `sessCompId != null && !equals("")`, but the action itself provides no defensive fallback if that gate is somehow bypassed.

**Evidence:**
- `AdminUnitAction.java:30-31` — `getSession(false)` result not null-checked
- `AdminUnitAction.java:40` — `Integer.parseInt(sessCompId)` with no guard against empty string
- `PreFlightActionServlet.java:45-61` — gate logic relies on path matching; direct access to compiled servlet could bypass it

**Recommendation:**
Add an explicit null check immediately after `request.getSession(false)` and redirect to the expiry page if null. Add a non-empty numeric guard before `Integer.parseInt(sessCompId)` and reject the request explicitly rather than relying on exception propagation.

---

### FINDING-06 — HIGH: SQL Injection in `UnitDAO.getUnitNameByComp` via `compLst` Concatenation (Same DAO)

**Severity:** HIGH
**File:** `src/main/java/com/dao/UnitDAO.java`, line 311

**Description:**
`getUnitNameByComp` uses `compLst` — a value derived from `compId` after possible transformation via `cDAO.getSubCompanyLst(compId)` — inside a SQL `IN (...)` clause via string concatenation:

```java
String sql = "select id,name from unit where comp_id in (" + compLst + ")";
```

If `getSubCompanyLst` returns an attacker-influenced string, this constitutes a second-order SQL injection vector within the same DAO.

**Note:** `getUnitNameByComp` is not called directly from `AdminUnitAction`, but is documented here as it is part of the DAO under review. The same pattern (`compLst`) appears in `getTotalUnitByID` at line 548.

**Recommendation:** Use a parameterised query with dynamic placeholder generation for IN-list queries.

---

### FINDING-07 — MEDIUM: No Role-Based Access Control Enforced in Action

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminUnitAction.java`, lines 27–219
**Config:** `src/main/webapp/WEB-INF/struts-config.xml`, lines 246–256

**Description:**
The `/adminunit` mapping declares no `roles` attribute. Struts 1.3 supports container-managed role checking via the `roles` attribute on `<action>`, but it is not used here. The action performs no programmatic role check either. Any authenticated session (any user with a valid `sessCompId`) can access all sub-actions including `delete`, `add_job`, and `edit_job`.

In the context of an admin panel this may be intentional if all sessions at this URL are administrators, but this is not enforced anywhere visible in this action or its mapping. An operator-level user who somehow obtains a session with `sessCompId` set could reach this action.

**Evidence:**
- `struts-config.xml:246` — no `roles` attribute on `/adminunit` action
- `AdminUnitAction.java:27–219` — no session role/permission attribute checked (e.g., no check of `sessRole`, `sessAdmin`, etc.)

**Recommendation:**
Add a programmatic role check at the top of `execute()` against a session attribute that encodes the user's role, and reject requests from non-admin sessions with a redirect to the expiry/error page. Alternatively, add the `roles` attribute to the action mapping if container-managed security is configured.

---

### FINDING-08 — MEDIUM: Input Validation Absent for All Parameters Passed to DAOs

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminUnitAction.java`, lines 33–39

**Description:**
The `equipId`, `job_id`, `job_no`, `description`, `title`, and `searchUnit` parameters are read directly from the request with no validation beyond empty-string defaulting:

```java
String equipId = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
```

- `equipId` is used in numeric contexts (`Integer.parseInt`, `Long.valueOf`) in multiple branches without a prior `NumberUtils.isDigits()` guard except in `add_job` (line 70). The `delete` branch (line 58) passes it directly to the DAO without any numeric check.
- `job_description` and `job_title` are placed into `JobDetailsBean` and persisted without length or content validation (lines 73–74).
- `searchUnit` is passed to `UnitsByCompanyIdQuery.containing(searchUnit)` (line 213/963 of UnitDAO). The safety of this depends on the implementation of `containing()`, which is not checked in this review but represents a potential injection vector.
- `validation.xml` has no entry for any form associated with `/adminunit`.

**Evidence:**
- `AdminUnitAction.java:34` — `equipId` not validated as numeric before use in `delete` branch (line 58)
- `AdminUnitAction.java:35-36` — `job_description`, `job_title` set directly on bean without length/content check
- `validation.xml` — no form entry for `adminunit` or any form used by this action

**Recommendation:**
Validate `equipId` as a positive integer at the top of `execute()` before the action dispatch. Add length and character-class constraints on free-text fields. Add form definitions in `validation.xml` or move to programmatic validation at the action layer.

---

### FINDING-09 — MEDIUM: Potential NullPointerException in `service` Branch When `equipId` Is Blank

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminUnitAction.java`, lines 148–161

**Description:**
In the `else` branch of the `service` action (when `equipId` is empty), the code instantiates a `ServiceBean` and immediately calls `bean.getHrsTilNext()` without checking whether that field is initialised:

```java
// Lines 149-151
ServiceBean bean = new ServiceBean();
double servRemain = Double.parseDouble(bean.getHrsTilNext()); // NPE if getHrsTilNext() returns null
```

If `ServiceBean.getHrsTilNext()` returns `null` (the default for an uninitialised String field on a newly constructed bean), `Double.parseDouble(null)` will throw a `NumberFormatException`, not an NPE, but still represents an unhandled exceptional path. Contrast with the non-empty `equipId` path at lines 132–133, which does null-check `bean.getHrsTilNext()` before parsing.

**Evidence:**
- `AdminUnitAction.java:150` — `Double.parseDouble(bean.getHrsTilNext())` — no null guard
- `AdminUnitAction.java:132-133` — parallel path correctly guards with `if (bean.getHrsTilNext() != null)`

**Recommendation:**
Apply the same null check used at line 132 to the else branch at line 150.

---

### FINDING-10 — MEDIUM: Sensitive Equipment Data Returned Without Output Encoding to Request Scope

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminUnitAction.java`, lines 46, 55, 60, 65–67

**Description:**
Unit data including `serial_no`, `mac_address`, `location`, `department`, `access_type`, `access_id`, and `facility_code` (all visible in `UnitsByIdQuery.java:37–64`) is placed directly into request scope for rendering by JSP views:

```java
request.setAttribute("arrAdminUnit", arrUnit);
```

If the JSP tiles do not apply `<c:out>` / JSTL escaping or the Struts `<bean:write filter="true">` attribute, stored values containing HTML/JavaScript could be rendered unescaped. This is a stored XSS risk where the attacker can store a payload in a unit's `name`, `location`, or `department` field, which is then reflected back to administrators.

The risk cannot be fully assessed from this file alone (requires JSP review), but the data exposure surface includes fields that are user-editable.

**Evidence:**
- `AdminUnitAction.java:46` — `arrAdminUnit` containing raw DB strings placed in request scope
- `UnitsByIdQuery.java:39-63` — all string fields retrieved directly from DB without sanitisation

**Recommendation:**
Ensure all JSP views rendering these attributes use encoding (`<c:out value="${...}"/>` or equivalent). This should be confirmed in a subsequent JSP-layer audit pass.

---

### FINDING-11 — LOW: `getSession(false)` Return Value Discarded by `dateFormat` Attribute Without Guard

**Severity:** LOW
**File:** `src/main/java/com/action/AdminUnitAction.java`, line 32

**Description:**
`dateFormat` is retrieved from the session on line 32 and used at line 186 (`getAssignments`). If the session is null (as noted in FINDING-05), this line also throws NPE. If the session is non-null but `sessDateFormat` is null, `DateUtil.sqlTimestampToString(..., null)` at line 177 will receive a null format string. The result depends on the `DateUtil` implementation (not reviewed here) but could produce a runtime exception or silently return incorrect date strings shown to the administrator.

**Evidence:**
- `AdminUnitAction.java:32` — `dateFormat` cast without null check

**Recommendation:**
Add a null guard or provide a default date format constant when `sessDateFormat` is absent.

---

### FINDING-12 — INFO: Singleton UnitDAO Has No Thread-Safety Issue but Double-Checked Lock Is Obsolete Pattern

**Severity:** INFO
**File:** `src/main/java/com/dao/UnitDAO.java`, lines 26–35

**Description:**
The singleton pattern uses double-checked locking without declaring `theInstance` as `volatile`. In Java 5+ with the Java Memory Model guarantees, this is safe only with `volatile`. Without `volatile`, there is a theoretical risk of a thread observing a partially initialised object under heavy concurrent startup load. In practice, servlet containers initialise singletons early, so exploitation is extremely unlikely.

**Evidence:**
- `UnitDAO.java:24` — `private static UnitDAO theInstance;` — no `volatile`
- `UnitDAO.java:28-33` — double-checked lock

**Recommendation:**
Declare `theInstance` as `private static volatile UnitDAO theInstance;` or use the initialisation-on-demand holder idiom.

---

## 3. Authentication

**Gate mechanism:** `PreFlightActionServlet` checks `sessCompId != null && !equals("")` for all paths not in the exclusion list, including `/adminunit.do`. This gate fires before the Struts `ActionServlet` dispatches to `AdminUnitAction`.

**Issues found:**
- FINDING-05: The action does not defensively handle a null session — it relies entirely on the servlet filter gate. A bypass of that gate (misconfiguration, direct container access) results in NPE at line 31.
- FINDING-07: No role check — any session with `sessCompId` can reach destructive operations.
- Authentication gate order is correct (session check occurs before DB calls) but the action provides no second line of defence.

---

## 4. CSRF

**Issues found:** FINDING-04 (HIGH). No CSRF token mechanism present anywhere in this action or its mapping.

---

## 5. Input Validation

**Issues found:** FINDING-08 (MEDIUM). No validation on any request parameter entering this action. No validation.xml entry. No numeric guard on `equipId` before the `delete` path reaches the DAO.

---

## 6. SQL Injection

**Issues found:**
- FINDING-01 (CRITICAL): `delUnitById` — direct concatenation of `equipId` into SQL UPDATE
- FINDING-03 (CRITICAL): `getUnitBySerial` — string concatenation of `serial_no` (same DAO, documented for completeness)
- FINDING-06 (HIGH): `getUnitNameByComp` / `getTotalUnitByID` — `compLst` concatenated into IN clause (same DAO, documented for completeness)

`getUnitById` is **not** vulnerable — it delegates to `UnitsByIdQuery` which uses a `PreparedStatement` with `?` placeholder (`UnitsByIdQuery.java:14`).

---

## 7. IDOR

**Issues found:** FINDING-02 (CRITICAL). Unit IDs are never validated against session company before any DAO operation.

---

## 8. Session Handling

**Issues found:**
- FINDING-05 (HIGH): No null check on `getSession(false)` result.
- FINDING-11 (LOW): `dateFormat` session attribute used without null guard.
- No session fixation, session regeneration post-login, or timeout configuration issues are visible in this file (would require broader review).

---

## 9. Data Exposure

**Issues found:**
- FINDING-10 (MEDIUM): Unit bean data (including `mac_address`, `facility_code`, `access_id`, `serial_no`) placed in request scope without output-encoding guarantee. JSP-layer XSS risk.
- `SQLException` details are caught and re-thrown as new `SQLException(e.getMessage())`, which may propagate DB error messages to the Struts `global-exceptions` handler and potentially into error pages visible to the user.

---

## 10. Finding Summary

| ID | Severity | Category | File : Line | Short Description |
|---|---|---|---|---|
| FINDING-01 | CRITICAL | SQL Injection | `UnitDAO.java:349` | `delUnitById` concatenates `equipId` into SQL |
| FINDING-02 | CRITICAL | IDOR | `AdminUnitAction.java:45,58,64-65,102,173,190` | No company ownership check on any unit operation |
| FINDING-03 | CRITICAL | SQL Injection | `UnitDAO.java:212` | `getUnitBySerial` concatenates `serial_no` |
| FINDING-04 | HIGH | CSRF | `AdminUnitAction.java:57-99` | No CSRF token on delete/add_job/edit_job |
| FINDING-05 | HIGH | Authentication | `AdminUnitAction.java:30-31,40` | `getSession(false)` null not checked; `parseInt("")` unguarded |
| FINDING-06 | HIGH | SQL Injection | `UnitDAO.java:311,548` | `compLst` concatenated into IN clause |
| FINDING-07 | MEDIUM | Access Control | `AdminUnitAction.java:27-219` | No role check; any session can perform all operations |
| FINDING-08 | MEDIUM | Input Validation | `AdminUnitAction.java:33-39` | No input validation on any request parameter |
| FINDING-09 | MEDIUM | Error Handling | `AdminUnitAction.java:150` | `Double.parseDouble(null)` possible in service branch |
| FINDING-10 | MEDIUM | Data Exposure / XSS | `AdminUnitAction.java:46,55,60,65-67` | Raw DB strings in request scope, XSS risk in JSP |
| FINDING-11 | LOW | Session Handling | `AdminUnitAction.java:32,177` | `dateFormat` used without null guard |
| FINDING-12 | INFO | Code Quality | `UnitDAO.java:24,28-33` | Double-checked lock without `volatile` |

**Totals by severity:**
- CRITICAL: 3
- HIGH: 3
- MEDIUM: 4
- LOW: 1
- INFO: 1
- **Total: 12**
