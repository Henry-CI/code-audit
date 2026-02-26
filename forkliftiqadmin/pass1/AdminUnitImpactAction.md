# Security Audit Report: AdminUnitImpactAction

**Audit Run:** audit/2026-02-26-01
**Pass:** 1
**Date:** 2026-02-26
**Auditor:** Automated Security Review (Claude Sonnet 4.6)
**Repository:** forkliftiqadmin (branch: master)

---

## 1. Reading Evidence

### 1.1 Package and Class

| Item | Value |
|------|-------|
| Package | `com.action` |
| Class | `AdminUnitImpactAction` |
| Superclass | `org.apache.struts.action.Action` |
| File | `src/main/java/com/action/AdminUnitImpactAction.java` |

### 1.2 Public/Protected Methods

| Line | Signature |
|------|-----------|
| 20 | `public ActionForward execute(ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response) throws Exception` |

### 1.3 DAOs / Services Called

| Line | Call |
|------|------|
| 32 | `UnitDAO.getInstance().resetCalibration(equip)` — delegates to `UnitCalibrationStarterInDatabase.startCalibration(equipId)` |

The calibration reset issues the following parameterised UPDATE:
```sql
UPDATE unit
SET impact_threshold = 0,
    alert_enabled     = FALSE,
    reset_calibration_date = NOW(),
    calibration_date  = NULL
WHERE id = ?
```
The `id` parameter is bound via `statement.setLong(1, unitId)` (no SQL-injection risk in that query itself).

### 1.4 Form Class

`com.actionform.AdminUnitImpactForm` — fields: `id`, `unitId`, `servLast`, `servNext`, `servDuration`, `accHours`, `hourmeter`, `action`, `servType`, `servStatus`.
All numeric fields are Java primitives (`int`, `double`). The string field `action` is the only field the action actually uses from the form (line 27); the `equipId` is taken from the raw request parameter (line 22).

### 1.5 Struts-Config Mapping (struts-config.xml lines 500–509)

```xml
<action
    path="/adminunitimpact"
    name="adminUnitImpactForm"
    scope="request"
    type="com.action.AdminUnitImpactAction"
    validate="true"
    input="UnitImpactDefinition">
    <forward name="success" path="UnitImpactDefinition"/>
    <forward name="failure" path="UnitImpactDefinition"/>
</action>
```

| Attribute | Value | Notes |
|-----------|-------|-------|
| `path` | `/adminunitimpact` | Mapped as `adminunitimpact.do` |
| `name` | `adminUnitImpactForm` | Binds `com.actionform.AdminUnitImpactForm` |
| `scope` | `request` | Form lives for one request only |
| `validate` | `true` | Struts validator is invoked |
| `roles` | _not set_ | No declarative role restriction |
| `input` | `UnitImpactDefinition` | Redirect target on validation failure |

**Validation.xml coverage:** `adminUnitImpactForm` has **no entry** in `WEB-INF/validation.xml`. Despite `validate="true"`, the validator finds no rules and performs no checks. The three forms covered are `loginActionForm`, `adminRegisterActionForm`, and `AdminDriverEditForm`.

---

## 2. Findings

---

### FINDING-01 — CRITICAL: Insecure Direct Object Reference — No Ownership Check Before Calibration Reset

**Severity:** CRITICAL
**File:** `src/main/java/com/action/AdminUnitImpactAction.java`
**Lines:** 21–34
**Category:** IDOR / Broken Access Control

**Description:**
The `reset_calibration` branch accepts an `equipId` from the raw HTTP request parameter and immediately calls `UnitDAO.getInstance().resetCalibration(equip)` with no verification that the equipment identified by `equipId` belongs to the session company (`sessCompId`). Any authenticated user (of any company) can reset the impact calibration of any forklift unit in the entire database by supplying an arbitrary `equipId`.

**Evidence:**
```java
// AdminUnitImpactAction.java lines 21–34
String equipId = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
...
if (action.equalsIgnoreCase("reset_calibration")) {
    int equip = Integer.parseInt(equipId);
    UnitDAO.getInstance().resetCalibration(equip);   // no sessCompId ownership check
    request.setAttribute("impactBean", new ImpactBean());
    return mapping.findForward("success");
}
```

The downstream `resetCalibration` call:
```java
// UnitDAO.java line 875–877
public void resetCalibration(int equipId) throws SQLException {
    new UnitCalibrationStarterInDatabase().startCalibration(equipId);
}
```

```java
// UnitCalibrationStarterInDatabase.java lines 9–16
public void startCalibration(long unitId) throws SQLException {
    String query = "UPDATE unit SET impact_threshold = 0, " +
            "alert_enabled = FALSE, " +
            "reset_calibration_date = NOW(), " +
            "calibration_date = NULL " +
            "WHERE id = ?";
    DBUtil.updateObject(query, statement -> statement.setLong(1, unitId));
}
```

The session holds `sessCompId` (checked by `PreFlightActionServlet`), but neither the action nor the DAO ever queries `WHERE id = ? AND comp_id = ?` to scope the operation to the authenticated company.

**Impact:**
- Company A's admin can zero out the impact threshold and disable impact alerting on Company B's forklifts, silently disabling safety monitoring fleet-wide for a competitor or customer.
- Conversely, a low-privilege user who has authenticated (even to a demo company) can disrupt safety-critical calibration data for any unit in the system.

**Recommendation:**
Before calling `resetCalibration`, verify the equipment belongs to the session company:
```java
String sessCompId = (String) request.getSession(false).getAttribute("sessCompId");
List<UnitBean> units = UnitDAO.getUnitById(equipId);
if (units.isEmpty() || !units.get(0).getComp_id().equals(sessCompId)) {
    return mapping.findForward("failure");
}
```
Alternatively, modify `resetCalibration` / `startCalibration` to accept a `compId` parameter and include `AND comp_id = ?` in the UPDATE predicate.

---

### FINDING-02 — HIGH: Missing CSRF Protection on Destructive State-Changing Operation

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminUnitImpactAction.java` / `src/main/webapp/WEB-INF/struts-config.xml`
**Lines:** Action line 30–34; struts-config lines 500–509
**Category:** CSRF

**Description:**
The `reset_calibration` action permanently alters unit safety configuration (zeroes `impact_threshold`, sets `alert_enabled = FALSE`, clears `calibration_date`). The endpoint accepts both GET and POST (Struts 1 `ActionServlet` handles both via `PreFlightActionServlet.doPost` → `doGet`). There is no CSRF token, `SameSite` cookie attribute, `Origin`/`Referer` header validation, or any other anti-CSRF mechanism in the stack. An attacker can forge a request to `/adminunitimpact.do?action=reset_calibration&equipId=<id>` from any page the authenticated admin visits.

**Evidence:**
- `PreFlightActionServlet.doPost` at line 94–96 calls `doGet` directly — no CSRF check.
- `struts-config.xml` mapping has no `roles` restriction and no token validation declared.
- The action class reads only `action` and `equipId` from the request; no synchronizer token is checked.

**Impact:**
A CSRF attack can trigger safety-critical calibration resets against any unit visible to the victim's session, causing forklift impact monitoring to be silently disabled across a fleet without any admin interaction beyond visiting a malicious page.

**Recommendation:**
Implement a synchronizer token pattern. In Struts 1 this can be done with `saveToken(request)` on the form-loading action and `isTokenValid(request, true)` at the start of `execute()` before processing any mutation. Alternatively, adopt a servlet filter that validates a CSRF header (e.g., `X-Requested-With`) for state-changing requests.

---

### FINDING-03 — HIGH: Missing Role/Privilege Check — No Authorization Beyond Session Existence

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminUnitImpactAction.java`
**Lines:** 20–38
**Category:** Authentication / Authorization

**Description:**
The only authentication gate for this action is `PreFlightActionServlet` checking `sessCompId != null`. There is no role-based authorization check inside `AdminUnitImpactAction.execute()`. The struts-config mapping for `/adminunitimpact` declares no `roles` attribute. Therefore any authenticated user — regardless of role (operator, driver-level user, read-only role) — can invoke the `reset_calibration` branch and permanently alter safety-critical unit calibration settings.

**Evidence:**
- `struts-config.xml` line 501–508: no `roles` attribute on the `/adminunitimpact` mapping.
- `AdminUnitImpactAction.java` lines 20–38: `execute()` performs zero session role checks before branching to `reset_calibration`.
- `PreFlightActionServlet.java` lines 56–60: the only check is `session.getAttribute("sessCompId") == null`.

**Recommendation:**
Add an explicit role guard at the top of `execute()`:
```java
String sessRole = (String) request.getSession(false).getAttribute("sessRole");
if (!"admin".equalsIgnoreCase(sessRole)) {
    return mapping.findForward("failure");
}
```
Additionally, add `roles="admin"` to the struts-config action mapping so the framework itself enforces access before `execute()` is reached.

---

### FINDING-04 — HIGH: Unvalidated `equipId` — No Struts Validator Rules; `NumberFormatException` on Empty/Non-Numeric Input

**Severity:** HIGH
**File:** `src/main/java/com/action/AdminUnitImpactAction.java`
**Lines:** 22, 31
**Category:** Input Validation / Application Stability

**Description:**
`equipId` is read directly from the request parameter and passed to `Integer.parseInt()` without any validation or bounds check. Although `validate="true"` is set in struts-config, the `adminUnitImpactForm` has no entry in `validation.xml`, so Struts performs no field-level validation before `execute()` is called. If `equipId` is empty, null-after-default, or non-numeric, `Integer.parseInt(equipId)` at line 31 throws an uncaught `NumberFormatException`.

Additionally, the `action` parameter is read from `request.getParameter("action")` (line 21) — a raw string compared with `equalsIgnoreCase` — so an attacker can probe action dispatch logic with arbitrary strings without any canonicalization or allowlist check.

**Evidence:**
```java
// lines 21–22
String action  = request.getParameter("action") == null ? "" : request.getParameter("action");
String equipId = request.getParameter("equipId") == null ? "" : request.getParameter("equipId");
...
// line 31 — will throw NumberFormatException if equipId is "" or non-integer
int equip = Integer.parseInt(equipId);
```

`validation.xml` contains no `<form name="adminUnitImpactForm">` entry, so the validator plugin does nothing despite `validate="true"`.

**Impact:**
- Unhandled `NumberFormatException` triggers the global `java.sql.SQLException` handler (struts-config lines 43–55) which forwards to `errorDefinition` — a generic error page that may leak stack-trace details depending on server configuration.
- No positive allowlist exists for the `action` parameter; undocumented action values silently fall through to the `else` branch and return `success` without performing any meaningful operation, which could mask logic errors.

**Recommendation:**
1. Add a `<form name="adminUnitImpactForm">` block in `validation.xml` with integer validation on `equipId` (and any other numeric fields).
2. Wrap `Integer.parseInt(equipId)` in a try/catch or pre-validate with a regex/`StringUtils.isNumeric` guard, returning `failure` on bad input.
3. Replace the open string comparison for `action` with an explicit allowlist enum or `switch` with a `default` that returns `failure`.

---

### FINDING-05 — MEDIUM: Dual Parameter Source for `action` — Request Parameter Overrides Form Field

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminUnitImpactAction.java`
**Lines:** 21, 26–28
**Category:** Input Validation / Logic Flaw

**Description:**
The `action` value is sourced first from `request.getParameter("action")` (line 21). Only if that is null or empty does the code fall back to `impactForm.getAction()` (line 27). Because the form scope is `request`, Struts populates `impactForm` from request parameters before `execute()` is called, making both sources effectively equivalent and the fallback logic redundant. However, this pattern is fragile: it creates ambiguity about which channel is authoritative, makes it harder to apply validation (the validator covers form fields, not raw request parameters), and could yield different behavior if scope or binding changes in future.

Separately, the `action` parameter is compared using `==` for the null-check (line 26: `action == null || action.equals("")`) but the initial assignment already guards against null at line 21. The null-check at line 26 is therefore dead code, adding confusion.

**Evidence:**
```java
// line 21: raw parameter read
String action = request.getParameter("action") == null ? "" : request.getParameter("action");
...
// lines 26–28: redundant fallback — action can never be null here
if (action == null || action.equals("")) {
    action = impactForm.getAction();
}
```

**Recommendation:**
Rely solely on the form bean for all input. Remove the raw `request.getParameter("action")` read and bind `action` exclusively from `impactForm.getAction()`. This ensures Struts validation covers the field and the data origin is consistent.

---

### FINDING-06 — MEDIUM: Silent No-Op on Unrecognised Action — No Audit Trail

**Severity:** MEDIUM
**File:** `src/main/java/com/action/AdminUnitImpactAction.java`
**Lines:** 35–37
**Category:** Session Handling / Logging / Logic

**Description:**
Any request where `action` is not `"reset_calibration"` — including an empty string, a misspelling, or a deliberate probe — silently returns `success` and forwards to `UnitImpactDefinition` without logging or error feedback. The action has no logging of the incoming `action` value, the `equipId`, or the authenticated `sessCompId`. This eliminates auditability of calibration reset operations and makes it impossible to detect replay or enumeration attacks in logs.

**Evidence:**
```java
// lines 35–37
} else {
    return mapping.findForward("success");
}
```
No `log.info(...)` or `log.warn(...)` call anywhere in `execute()`. The class declares a logger (`log` at line 18) but never uses it.

**Recommendation:**
1. Log every entry to `execute()` including `sessCompId`, `action`, and `equipId` at INFO level.
2. Log calibration resets at WARN or above since they affect safety-critical state.
3. Return `failure` (or a dedicated `unknown_action` forward) for unrecognised `action` values rather than silently returning `success`.

---

### FINDING-07 — LOW: Unused Logger Field

**Severity:** LOW
**File:** `src/main/java/com/action/AdminUnitImpactAction.java`
**Line:** 18
**Category:** Code Quality / Observability

**Description:**
A `Logger` instance (`log`) is declared at line 18 but is never called anywhere in the class. This is consistent with the absence of any audit trail noted in FINDING-06 and indicates the logging infrastructure was included by template but never wired up.

**Evidence:**
```java
// line 18 — declared but never used
private static Logger log = InfoLogger.getLogger("com.action.AdminUnitImpactAction");
```

**Recommendation:**
Add appropriate log calls (see FINDING-06 recommendations) to utilise the existing logger.

---

## 3. Category Summary

| Category | Status | Findings |
|----------|--------|----------|
| Authentication (sessCompId check) | PARTIAL — `sessCompId` checked by servlet gate only; no role check in action | FINDING-03 |
| Authorization / IDOR | VULNERABLE — no ownership check before calibration reset | FINDING-01 |
| CSRF | VULNERABLE — no token, no origin validation | FINDING-02 |
| Input Validation | VULNERABLE — validator rules absent; parseInt unguarded | FINDING-04, FINDING-05 |
| SQL Injection | NO ISSUES — `resetCalibration` uses parameterised PreparedStatement with `setLong` | — |
| Session Handling | PARTIAL — session existence checked; sessCompId not used for scoping | FINDING-01, FINDING-03 |
| Data Exposure | NO ISSUES — the action does not read or return sensitive data in this flow; `new ImpactBean()` placed in request attribute is empty | — |
| Logging / Audit Trail | VULNERABLE — no logging of any operation | FINDING-06, FINDING-07 |

---

## 4. Finding Count by Severity

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 1 | FINDING-01 |
| HIGH | 3 | FINDING-02, FINDING-03, FINDING-04 |
| MEDIUM | 2 | FINDING-05, FINDING-06 |
| LOW | 1 | FINDING-07 |
| INFO | 0 | — |
| **Total** | **7** | |

---

## 5. Risk Prioritisation

The most urgent remediation path is:

1. **FINDING-01 (CRITICAL)** — Add a company-ownership guard before any `resetCalibration` call. This is a one-line WHERE-clause addition that eliminates cross-tenant safety data manipulation.
2. **FINDING-02 (HIGH)** — Add Struts synchronizer token validation to prevent CSRF-triggered calibration resets.
3. **FINDING-03 (HIGH)** — Add a role check (session attribute or struts-config `roles`) to restrict the action to admin-level users only.
4. **FINDING-04 (HIGH)** — Add validation.xml rules for `adminUnitImpactForm` and guard `Integer.parseInt` against non-numeric input.
