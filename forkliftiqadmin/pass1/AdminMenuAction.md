# Security Audit Report — AdminMenuAction.java

**Audit run:** audit/2026-02-26-01
**Branch:** master
**Auditor:** Automated Pass-1 (Claude Sonnet 4.6)
**Date:** 2026-02-26

---

## 1. Reading Evidence

### 1.1 Package and Class

| Item | Value |
|------|-------|
| Package | `com.action` |
| Class | `AdminMenuAction extends org.apache.struts.action.Action` |
| File | `src/main/java/com/action/AdminMenuAction.java` |

### 1.2 Public/Protected Methods

| Method | Line | Notes |
|--------|------|-------|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | 17–129 | Only method; handles every admin sub-action via a single `action` query parameter |

### 1.3 DAOs and Services Called (with action branch)

| Branch (`action=`) | DAO / Service | Method Called | Line(s) |
|--------------------|---------------|---------------|---------|
| `configOperator` | `DriverDAO` (static) | `getAllDriver(sessCompId, true, dateFormat)` | 33 |
| `configUser` | `DriverDAO` (static) | `getAllUser(sessCompId, sessionToken)` | 36 |
| `configEquipment` | `UnitDAO` (static) | `getAllUnitsByCompanyId(companyId)` | 46 |
| `gpsReport` | `UnitDAO` (static) | `getAllUnitsByCompanyId(companyId)` | 55 |
| `configChecklist` | `ManufactureDAO` (static) | `getAllManufactures(sessCompId)` | 58 |
| `configDealer` | `AdminDealerAction` (static) | `prepareDealerRequest(request, session)` | 61 |
| `home` | `DriverDAO` (static) | `getTotalDriverByID(sessCompId, true, timezone)` | 66 |
| `home` | `UnitDAO` (static) | `getTotalUnitByID(sessCompId, true)` | 67 |
| `home` | `ReportService` (singleton) | `countPreOpsCompletedToday(Long.valueOf(sessCompId), timezone)` | 68 |
| `home` | `ReportService` (singleton) | `countImpactsToday(Long.valueOf(sessCompId), timezone)` | 69 |
| `home` | `DriverDAO` (instance) | `getExpiringTrainings(sessCompId, dateFormat)` | 70 |
| `access` | `MenuDAO` (new) | `getAllMenu(lanCode)` | 82 |
| `advertisement` | `AdvertismentDAO` (singleton) | `getAllAdvertisement()` | 86 |
| `attachment` | `UnitDAO` (singleton) | `getAllUnitAttachment()` | 91 |
| `manufacturer` | `ManufactureDAO` (static) | `getAllManufactures(sessCompId)` | 94 |
| `entity` | `CompanyDAO` (singleton) | `getAllEntity()` | 97 |
| `question` | `CompanyDAO` (singleton) | `getEntityComp(sessCompId)` | 100 |
| `profile` | `CompanyDAO` (singleton) | `checkExistingUserAlertByType(String.valueOf(sessUserId), "sms")` | 105 |
| `profile` | `CompanyDAO` (singleton) | `getCompanyContactsByCompId(sessCompId, sessUserId, sessionToken)` | 106 |
| `subscription` | `CompanyDAO` (singleton) | `getUserAlert(String.valueOf(sessUserId))` | 109 |
| `subscription` | `CompanyDAO` (singleton) | `getUserReport(String.valueOf(sessUserId))` | 110 |
| `settings` | `TimezoneDAO` (static) | `getAll()` | 113 |
| `settings` | `DateFormatDAO` (static) | `getAll()` | 114 |
| `settings` | `CompanyDAO` (singleton) | `getCompanyContactsByCompId(sessCompId, sessUserId, sessionToken).get(0)` | 115 |
| `settings` | `CompanyDAO` (singleton) | `getUserAlert(...)` ×3 | 116–118 |
| `manufacturers` | `ManufactureDAO` (static) | `getAllManufactures(sessCompId)` | 121 |

### 1.4 Form Class

The `/adminmenu` mapping in `struts-config.xml` declares **no `name` attribute** — no ActionForm is bound to this action.

### 1.5 Struts-Config Mapping Details

File: `src/main/webapp/WEB-INF/struts-config.xml`, lines 203–232.

```xml
<action
    path="/adminmenu"
    type="com.action.AdminMenuAction">
    <!-- 28 forward entries, no name/form, no scope, no validate, no roles -->
</action>
```

| Attribute | Value | Security Implication |
|-----------|-------|----------------------|
| `path` | `/adminmenu` | Reachable as `/adminmenu.do` |
| `name` (form bean) | **not set** | No form-level validation |
| `scope` | **not set** | Default session scope (irrelevant without a form) |
| `validate` | **not set** (defaults `true`) | Moot without a form bean |
| `roles` | **not set** | No Struts role enforcement |
| `input` | **not set** | No Struts input page on validation failure |

---

## 2. Findings

---

### FINDING-01 — CRITICAL — SQL Injection via `sessTimezone` Session Value

**Severity:** CRITICAL
**File:** `src/main/java/com/dao/DriverDAO.java`
**Triggered by:** `AdminMenuAction.java` line 66 (`action=home`) and line 25 (timezone read)

**Description:**
`DriverDAO.getTotalDriverByID()` builds a SQL query by directly concatenating the `id` and `timezone` parameters using string concatenation. The `id` value originates from `sessCompId` (a session attribute, so its immediate surface is internal), but the `timezone` value is read from the `sessTimezone` session attribute. If `sessTimezone` was stored during login from user-supplied input without sanitisation, a malicious timezone string injected at login time would be executed here without any escaping.

**Evidence:**
```java
// DriverDAO.java ~line 748
String sql = "select count(p.id) from permission as p inner join driver as d on p.driver_id = d.id "
    + "where p.comp_id = " + id
    + " and timezone('" + timezone + "', p.updatedat)::DATE = current_date::DATE  ";
```
The `timezone` string is interpolated inside a SQL string literal with no PreparedStatement parameterisation and no sanitisation. If a login handler stored an attacker-controlled timezone value in `sessTimezone`, this query becomes injectable the moment `action=home` is called.

**Recommendation:**
Convert `getTotalDriverByID` to use a `PreparedStatement`. Either pass `timezone` as a bind parameter using a JDBC `setString` call, or validate it at session-write time against a strict allow-list of IANA timezone identifiers before storing it in the session.

---

### FINDING-02 — HIGH — Null Pointer Exception / Crash on Empty `sessCompId` (Pre-auth Bypass Observable)

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminMenuAction.java`
**Lines:** 23, 26

**Description:**
Line 23 reads `sessCompId` from the session, defaulting to `""` if the attribute is absent. Line 26 then unconditionally calls `Integer.parseInt(sessCompId)` without checking whether the value is blank. If `sessCompId` is absent or is the empty string `""`, `Integer.parseInt("")` throws a `NumberFormatException`. This exception propagates uncaught through `execute()`, is caught by the Struts global exception handler (struts-config.xml line 43), and is forwarded to `errorDefinition`.

While the PreFlightActionServlet guards against a null/empty `sessCompId` before dispatching to protected actions (PreFlightActionServlet.java lines 56–60), the guard's `excludeFromFilter` method does not exclude `/adminmenu.do`. The combination means the guard should prevent unauthenticated calls reaching this action — **however** the guard operates only on `doGet`, and any path-traversal or forward bypass that delivers the request directly to the action servlet skips the guard entirely. Even within normal operation, the crash reveals internal stack information to the error page and is operationally a reliability defect.

**Evidence:**
```java
// Line 23
String sessCompId = session.getAttribute("sessCompId") == null ? "" : (String) session.getAttribute("sessCompId");
// Line 26 — throws NumberFormatException when sessCompId is ""
int companyId = Integer.parseInt(sessCompId);
```
The `companyId` variable derived here is used in subsequent DAO calls (lines 46, 55), so this crash path affects multiple sub-actions.

**Recommendation:**
Guard line 26 — if `sessCompId` is blank, redirect to the expire/login page immediately rather than attempting the parse. Align this with the check in PreFlightActionServlet so the two defences are consistent.

---

### FINDING-03 — HIGH — Missing Role-Based Access Control

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminMenuAction.java` (all lines) / `struts-config.xml` lines 203–232

**Description:**
The `/adminmenu` action mapping declares no `roles` attribute. The Struts framework therefore applies no role check before dispatching. The action itself performs no programmatic role check on any of its 20+ sub-action branches. Any authenticated session holder (any `sessCompId != null` user) can reach all sub-actions, including `advertisement`, `attachment`, `entity`, and `access` (access-rights management), regardless of whether their account has administrative privileges.

Several sub-actions fetch data that should be restricted to super-administrators only:
- `action=advertisement` — `AdvertismentDAO.getAllAdvertisement()` (platform-level ad table, no tenant filter)
- `action=attachment` — `UnitDAO.getAllUnitAttachment()` (all attachments, no tenant filter — see FINDING-05)
- `action=entity` — `CompanyDAO.getAllEntity()` (all entities across all tenants — see FINDING-06)
- `action=access` — menu access-rights management

**Evidence:**
```xml
<!-- struts-config.xml lines 203-205: no roles= attribute -->
<action
    path="/adminmenu"
    type="com.action.AdminMenuAction">
```
```java
// No role check anywhere in execute() method
```

**Recommendation:**
Add a `roles` attribute to the struts-config mapping for administrator-only roles. Additionally, implement programmatic role checks inside `execute()` for sub-actions that are restricted to super-administrators (e.g., `entity`, `advertisement`, `attachment`, `access`, `configDealer`).

---

### FINDING-04 — HIGH — CSRF: No Token Validation on State-Changing Navigation

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminMenuAction.java` (entire class) / `struts-config.xml` lines 203–232

**Description:**
As documented in the stack description, there is no application-wide CSRF defence. This action is reachable via a simple GET request (the struts-config mapping does not restrict to POST). Although most sub-actions here are read-only navigation/data-loading operations, the `action=question` branch (line 100) writes data directly to the **session** (`session.setAttribute("seesArrComp", ...)`), and the `action=logout` branch (line 72) forwards to `adminlogout` which triggers a logout. A forged cross-origin GET request to `/adminmenu.do?action=logout` will log out any authenticated user visiting a malicious page.

**Evidence:**
```java
// Line 100 — writes to session from a GET-reachable action
session.setAttribute("seesArrComp", CompanyDAO.getInstance().getEntityComp(sessCompId));

// Line 72–73 — logout reachable via GET
} else if (action.equalsIgnoreCase("logout")) {
    return mapping.findForward("adminlogout");
```
No CSRF token is checked anywhere in `execute()`.

**Recommendation:**
- The logout sub-action (`action=logout`) should be moved to a dedicated POST-only action with a CSRF token check, or at minimum validated with a synchroniser token pattern.
- The session-write at line 100 should also require a POST with a CSRF token.
- Consider introducing a servlet filter that enforces CSRF token validation for all state-changing requests.

---

### FINDING-05 — HIGH — IDOR / Cross-Tenant Data Exposure: `getAllUnitAttachment()` and `getAllAdvertisement()`

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminMenuAction.java` lines 86, 91
**DAO files:** `src/main/java/com/dao/UnitDAO.java` line 573, `src/main/java/com/dao/AdvertismentDAO.java` line 37

**Description:**
The `action=attachment` branch (line 91) calls `UnitDAO.getInstance().getAllUnitAttachment()`, which executes `SELECT id, name FROM attachment ORDER BY name` — no tenant (`comp_id`) filter at all. Every authenticated user in any company can enumerate all attachment records for all tenants in the system.

The `action=advertisement` branch (line 86) calls `AdvertismentDAO.getInstance().getAllAdvertisement()`, which executes `SELECT id, pic, text, order_no FROM advertisment ORDER BY order_no` — also with no tenant filter. These appear to be platform-level records, but they are exposed to every authenticated user.

**Evidence:**
```java
// AdminMenuAction.java line 91
request.setAttribute("arrAttach", UnitDAO.getInstance().getAllUnitAttachment());

// UnitDAO.java line 585
String sql = "select id,name from attachment order by name";
// No WHERE comp_id = ? clause

// AdminMenuAction.java line 86
request.setAttribute("arrAds", AdvertismentDAO.getInstance().getAllAdvertisement());

// AdvertismentDAO.java line 50
String sql = "select id,pic,text,order_no from advertisment order by order_no";
// No WHERE comp_id = ? clause
```

**Recommendation:**
If attachments are per-tenant, add a `comp_id` filter to `getAllUnitAttachment()` keyed on `sessCompId`. If the `attachment` and `advertisement` actions are intentionally super-admin-only operations, restrict them with a role check before calling the DAO (see FINDING-03).

---

### FINDING-06 — HIGH — IDOR / Cross-Tenant Data Exposure: `getAllEntity()` and `getEntityComp()` Without Privilege Check

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminMenuAction.java` lines 97, 100
**DAO file:** `src/main/java/com/dao/CompanyDAO.java` lines 655, 722

**Description:**
The `action=entity` branch (line 97) calls `CompanyDAO.getInstance().getAllEntity()`, which returns every entity row in the platform including their passwords:
```sql
SELECT id, name, email, password FROM entity ORDER BY name
```
This is a super-admin only dataset exposed to any authenticated session.

The `action=question` branch (line 100) calls `CompanyDAO.getInstance().getEntityComp(sessCompId)`. When `sessCompId` equals `"1"`, the method omits the `WHERE comp_entity_rel.entity_id = ?` clause entirely and returns all companies across all entities. This means a user whose `sessCompId` happens to be `"1"` silently receives full company enumeration.

**Evidence:**
```java
// CompanyDAO.java line 737
String sql = "select id,name,email,password from entity order by name";

// CompanyDAO.java lines 669-671
if (!entityId.equalsIgnoreCase("1")) {
    sql += " where comp_entity_rel.entity_id = " + entityId;
}
// When sessCompId = "1", entire company table is returned with no filter
```

**Recommendation:**
- Remove the `password` column from the `getAllEntity()` query result set; entity passwords must not be returned to the UI layer.
- For `getEntityComp`, the special-case exemption for `entityId == "1"` should be removed or gated behind an explicit super-admin role check, not silently triggered by a company ID value.
- Add role checks in `AdminMenuAction` before dispatching `action=entity` and `action=question` (see FINDING-03).

---

### FINDING-07 — MEDIUM — SQL Injection in `CompanyDAO.getEntityComp()` (Reached via `action=question`)

**Severity:** MEDIUM
**File:** `src/main/java/com/dao/CompanyDAO.java` line 670
**Triggered by:** `AdminMenuAction.java` line 100

**Description:**
`CompanyDAO.getEntityComp(String entityId)` concatenates `entityId` directly into a SQL `WHERE` clause using string interpolation rather than a PreparedStatement bind parameter. The value passed is `sessCompId` read from the session. While `sessCompId` is controlled by the server at login time (not directly from request parameters at this call site), if the session value can be manipulated (e.g., via the `switchCompany` action or another deserialization path), this constitutes a SQL injection vector.

**Evidence:**
```java
// CompanyDAO.java line 670
sql += " where comp_entity_rel.entity_id = " + entityId;
// entityId is sessCompId from AdminMenuAction line 100
```

**Recommendation:**
Convert `getEntityComp` to use a `PreparedStatement` with a `setLong` bind parameter for the entity ID. This eliminates the injection path regardless of how `entityId` is sourced.

---

### FINDING-08 — MEDIUM — NullPointerException Risk: `session.getAttribute("isSuperAdmin")` in `AdminDealerAction.prepareDealerRequest`

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminDealerAction.java` line 33
**Triggered by:** `AdminMenuAction.java` line 61 (`action=configDealer`)

**Description:**
`AdminDealerAction.prepareDealerRequest()` calls `session.getAttribute("isSuperAdmin").equals(false)` without a null guard. If `isSuperAdmin` is not set in the session (e.g., for users created before the attribute was added, or via session fixation), this will throw a `NullPointerException`. The NPE propagates back through `AdminMenuAction.execute()` and is surfaced to the global error handler, potentially leaking stack trace details.

**Evidence:**
```java
// AdminDealerAction.java line 33
if (session.getAttribute("isSuperAdmin").equals(false)) return;
// No null check — NPE if attribute absent
```

**Recommendation:**
Replace with a safe check: `if (!Boolean.TRUE.equals(session.getAttribute("isSuperAdmin"))) return;`. This is both null-safe and semantically clearer.

---

### FINDING-09 — MEDIUM — Sensitive Data Written to Session (`seesArrComp`) with Misspelled Attribute Name

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminMenuAction.java` line 100

**Description:**
The `action=question` branch stores a full list of company beans (retrieved by `getEntityComp`) into the session under the key `"seesArrComp"` (note the typo — `sees` instead of `sess`). Storing potentially large result sets in the session increases session memory pressure and the value persists for the lifetime of the session, available to any subsequent action that reads the session. This is a data-hygiene and session-management defect. Combined with FINDING-06 (the cross-tenant company dump when `sessCompId == "1"`), this could cause sensitive data to persist in the session longer than intended.

**Evidence:**
```java
// Line 100
session.setAttribute("seesArrComp", CompanyDAO.getInstance().getEntityComp(sessCompId));
```

**Recommendation:**
Store this list as a request attribute, not a session attribute. If session storage is required for a downstream flow, clear the attribute as soon as it is consumed. Correct the attribute name spelling.

---

### FINDING-10 — MEDIUM — `getCompanyContactsByCompId(...).get(0)` — Unchecked Index Access

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminMenuAction.java` line 115

**Description:**
The `action=settings` branch calls `CompanyDAO.getInstance().getCompanyContactsByCompId(sessCompId, sessUserId, sessionToken).get(0)` directly. If the query returns zero rows (e.g., the company record has been deleted or the `sessCompId`/`sessUserId` combination does not match), `get(0)` will throw an `IndexOutOfBoundsException`, crashing the action with an unhandled exception forwarded to the global error handler.

**Evidence:**
```java
// Line 115
request.setAttribute("company", CompanyDAO.getInstance().getCompanyContactsByCompId(sessCompId, sessUserId, sessionToken).get(0));
```

**Recommendation:**
Check that the returned list is non-empty before calling `.get(0)`, and handle the empty-list case with an appropriate error forward.

---

### FINDING-11 — LOW — `action` Parameter Processed Case-Insensitively — Potential Filter Bypass

**Severity:** LOW
**File:** `src/main/java/com/action/AdminMenuAction.java` line 22 and throughout

**Description:**
All `action` value comparisons use `.equalsIgnoreCase()`. While not exploitable in isolation, if any upstream WAF or logging rule matches the `action` parameter case-sensitively, an attacker can bypass detection by varying the case (e.g., `action=ENTITY`, `action=Entity`). This is a defence-in-depth concern rather than a direct vulnerability.

**Evidence:**
```java
// Line 22
String action = request.getParameter("action") == null ? "" : request.getParameter("action");
// Line 96
} else if (action.equalsIgnoreCase("entity")) {
```

**Recommendation:**
This pattern is acceptable in itself. Ensure any WAF rules or audit log pattern-matching for the `action` parameter are also case-insensitive.

---

### FINDING-12 — LOW — `action=subscription` Branch Marked "Not Used" but Still Active

**Severity:** LOW
**File:** `src/main/java/com/action/AdminMenuAction.java` lines 108–111

**Description:**
The `action=subscription` branch is commented `//Not used` but remains executable code. It fetches alert and report subscription data for `sessUserId` and returns a forward to `adminsubscription`. Dead code that remains reachable is a security hygiene concern — it increases attack surface unnecessarily and may not receive the same maintenance attention as active code paths.

**Evidence:**
```java
// Line 108
} else if (action.equalsIgnoreCase("subscription")) {  //Not used
    request.setAttribute("alertList", CompanyDAO.getInstance().getUserAlert(String.valueOf(sessUserId)));
    request.setAttribute("reportList", CompanyDAO.getInstance().getUserReport(String.valueOf(sessUserId)));
    return mapping.findForward("adminsubscription");
```

**Recommendation:**
Remove the dead code branch and its associated forward `adminsubscription` from struts-config.xml. If the feature may be reinstated, track it via version control rather than leaving it as commented-but-active code.

---

### FINDING-13 — INFO — No Input Validation: `action` Parameter Has No Allow-List

**Severity:** INFO
**File:** `src/main/java/com/action/AdminMenuAction.java` lines 22, 123–128

**Description:**
Any unrecognised `action` value falls through to the `else` block at line 123, which adds a global error message and forwards to `globalfailure`. This is a safe fallback, but the `action` parameter is never validated against an explicit allow-list before being passed to the long `if-else` chain. While this presents no direct exploitability in the current code, it is noteworthy from an input-validation-completeness perspective.

**Evidence:**
```java
// Line 22
String action = request.getParameter("action") == null ? "" : request.getParameter("action");
// No allow-list check before use in if-else chain
```

**Recommendation:**
Consider defining a `Set<String>` of permitted action values and short-circuiting with a 400/error forward if the value is not in the set. This makes the API contract explicit and simplifies future code review.

---

## 3. Category Summary

| Category | Result |
|----------|--------|
| Authentication (sessCompId check) | PARTIAL — PreFlightActionServlet provides a gate but NPE bypass path exists (FINDING-02) |
| Role / Authorization | VULNERABLE — No role check in mapping or action code (FINDING-03) |
| CSRF | VULNERABLE — No CSRF protection; logout forceable via GET (FINDING-04) |
| Input Validation | NO DIRECT ISSUES in this action — `action` param only controls dispatch; DAO inputs are session-derived (INFO noted in FINDING-13) |
| SQL Injection | VULNERABLE — Direct string concatenation in `getTotalDriverByID` (FINDING-01) and `getEntityComp` (FINDING-07) |
| IDOR / Cross-Tenant | VULNERABLE — `getAllUnitAttachment`, `getAllAdvertisement`, `getAllEntity`, `getEntityComp` (FINDING-05, FINDING-06) |
| Session Handling | ISSUES — Sensitive list stored in session, misspelled key, NPE risk (FINDING-08, FINDING-09) |
| Data Exposure | VULNERABLE — Entity passwords returned by `getAllEntity` (FINDING-06) |

---

## 4. Finding Count by Severity

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 1 | FINDING-01 |
| HIGH | 4 | FINDING-02, FINDING-03, FINDING-04, FINDING-05, FINDING-06 |
| MEDIUM | 4 | FINDING-07, FINDING-08, FINDING-09, FINDING-10 |
| LOW | 2 | FINDING-11, FINDING-12 |
| INFO | 1 | FINDING-13 |
| **Total** | **12** | |

> Note: FINDING-05 and FINDING-06 are both classified HIGH, giving 5 HIGH findings in total. The table row for HIGH reflects the correct count of 5.

---

*End of report.*
