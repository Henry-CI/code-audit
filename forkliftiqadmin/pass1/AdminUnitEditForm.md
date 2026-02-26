# Security Audit: AdminUnitEditForm.java
**Repository:** forkliftiqadmin
**Branch:** master
**Audit Run:** audit/2026-02-26-01
**Pass:** 1
**Auditor:** CIG Automated Security Review
**Date:** 2026-02-26
**Stack:** Apache Struts 1.3.10

---

## Reading Evidence

### Package and Class
- **File:** `src/main/java/com/actionform/AdminUnitEditForm.java`
- **Package:** `com.actionform`
- **Class:** `AdminUnitEditForm extends ActionForm`
- **Lombok:** `@Data` (generates getters, setters, equals, hashCode, toString for all fields)

### Fields (all declared at class scope)

| Field | Java Type | Notes |
|---|---|---|
| `id` | `String` | Unit primary key — fully user-controllable via request parameter |
| `name` | `String` | Unit display name |
| `location` | `String` | Physical location |
| `department` | `String` | Department string |
| `type_id` | `String` | FK to unit type lookup |
| `active` | `String` | Active/inactive flag |
| `manu_id` | `String` | FK to manufacturer lookup |
| `size` | `String` | Decimal size value; regex-validated in `validate()` |
| `hourmeter` | `String` | Hour meter reading; no format validation |
| `serial_no` | `String` | Unit serial number |
| `fuel_type_id` | `String` | FK to fuel type lookup |
| `arrAdminUnitType` | `List` (raw) | Reference data populated in constructor |
| `arrAdminUnitFuelType` | `List` (raw) | Reference data populated in constructor |
| `arrMenufacture` | `List` (raw) | Reference data — never populated in this form |
| `mac_address` | `String` | Hardware MAC address |
| `exp_mod` | `String` | Expansion module identifier |
| `accessible` | `boolean` | Access control flag (primitive) |
| `access_type` | `String` | Access control type |
| `keypad_reader` | `String` | Maps to `UnitBean.KeypadReaderModel` enum at line 129 |
| `op_code` | `String` | Routing discriminator for AJAX sub-operations |
| `weight_unit` | `String` | Weight unit string |
| `facility_code` | `String` | Physical access facility code |
| `access_id` | `String` | Access control system ID |

### validate() Method (lines 64–108)
Checks performed:
1. `name` not empty (line 68)
2. `serial_no` not empty (line 73)
3. `manu_id` not empty (line 78)
4. `type_id` not empty (line 83)
5. `fuel_type_id` not empty (line 88)
6. `size` optional regex `^\d*\.{0,1}\d{0,2}$` — resets to `"0"` on mismatch (line 95–99)

Side-effect in `validate()`: constructs a `UnitBean` and sets `arrAdminUnit` on the request (lines 101–105). This is a logic concern — business work inside validation.

Fields with **no validation**: `id`, `location`, `department`, `active`, `manu_id` (presence only), `type_id` (presence only), `fuel_type_id` (presence only), `hourmeter`, `mac_address`, `exp_mod`, `accessible`, `access_type`, `keypad_reader`, `facility_code`, `access_id`, `op_code`, `weight_unit`.

### reset() Method
No `reset()` override exists. Struts will use the `ActionForm` default, which does not clear fields between requests. The `boolean accessible` field will default to `false` (Java primitive default) on a new form instantiation but will not be explicitly reset between form reuse within a session.

### validation.xml Coverage
The file at `src/main/webapp/WEB-INF/validation.xml` defines rules for exactly three forms:
- `loginActionForm`
- `adminRegisterActionForm`
- `AdminDriverEditForm`

**`adminUnitEditForm` has zero entries in validation.xml.** All validation is solely in the programmatic `validate()` method.

---

## Findings

---

### FINDING-01: Insecure Direct Object Reference — Unit ID Accepted from Client Without Ownership Check
**Severity:** CRITICAL
**File:** `src/main/java/com/actionform/AdminUnitEditForm.java`, line 24
**Also:** `src/main/java/com/dao/UnitDAO.java`, lines 467–495

**Description:**
The `id` field (line 24) is a plain `String` populated directly from the HTTP request parameter named `id`. When a non-null `id` is present, `saveUnitInfo()` executes an UPDATE:
```sql
update unit set name=?,location=?,department=?,type_id=?,manu_id=?,
fuel_type_id=?,size=?,hourmeter=?,serial_no=?,mac_address=?,weight_unit=?
where id=?
```
The WHERE clause (`where id=?`) contains **no `comp_id` filter**. The `comp_id` injected by the action (from `sessCompId` in the session) is only used during the INSERT path, not the UPDATE path. An authenticated user from Company A can POST `id=<any_unit_id>` belonging to Company B and overwrite that unit's data. Ownership is never verified for the edit operation.

**Evidence:**
- `AdminUnitEditForm.java` line 24: `private String id;` — unvalidated, comes from form post.
- `AdminUnitEditForm.java` line 112: `id` passed directly into `UnitBean.builder()`.
- `AdminUnitEditAction.java` line 29: `adminUnitEditForm.getUnit(compId)` passes `compId` from session into the bean, but this is only used on INSERT.
- `UnitDAO.java` lines 467–470: UPDATE SQL has no `comp_id` predicate.
- `UnitDAO.java` line 495: `ps.setLong(12, Long.valueOf(unitbean.getId()))` — user-supplied value used as sole WHERE criterion.

**Recommendation:**
Change the UPDATE query to `where id = ? and comp_id = ?` and bind both the user-supplied `id` and the session `compId`. Verify that `executeUpdate()` returns 1; if it returns 0, the unit either does not exist or belongs to another company — treat as an authorization error, not a silent no-op. Additionally, add a pre-check: load the unit by ID, confirm `comp_id` matches session, before executing the update.

---

### FINDING-02: No Input Validation on hourmeter — Unguarded Double.valueOf() Call Causes Uncaught NumberFormatException
**Severity:** HIGH
**File:** `src/main/java/com/actionform/AdminUnitEditForm.java`, line 121

**Description:**
`hourmeter` is a `String` field with no format validation in `validate()` and no entry in `validation.xml`. At line 121, `Double.valueOf(hourmeter)` is called without any guard beyond a blank check. Any non-numeric string (e.g. `"abc"`, `"1e999"`, `"NaN"`) will throw a `NumberFormatException` at runtime. In Struts 1, an uncaught exception from `getUnit()` — which is itself called from within `validate()` at line 101 — will propagate as an unhandled server error, potentially revealing stack-trace information in a default error page.

**Evidence:**
- Line 32: `private String hourmeter;` — declared as `String`, no annotation or rule.
- Line 121: `Double.valueOf(hourmeter)` — no prior format check.
- `validate()` lines 64–108: no check on `hourmeter` format.
- `validation.xml`: no rule for `adminUnitEditForm`.

**Recommendation:**
Add a numeric format check for `hourmeter` in `validate()` mirroring the existing `size` regex check (line 93–99), or use `StringUtils.isNumeric` / a try-catch before the conversion. The regex used for `size` (`^\d*\.{0,1}\d{0,2}$`) should also be reviewed for `hourmeter` — hourmeter values could legitimately have more than two decimal places, so an appropriate pattern should be chosen.

---

### FINDING-03: Unvalidated Enum Conversion for keypad_reader — IllegalArgumentException on Arbitrary Input
**Severity:** HIGH
**File:** `src/main/java/com/actionform/AdminUnitEditForm.java`, line 129

**Description:**
`keypad_reader` is a `String` field bound directly from the HTTP request. At line 129, it is passed to `UnitBean.KeypadReaderModel.valueOf(keypad_reader)` with no prior validation that the value is one of the four valid enum constants (`ROSLARE`, `KERI`, `SMART`, `HID_ICLASS`). An attacker supplying any other value will cause an `IllegalArgumentException`. The `getUnit()` method is called from `validate()` (line 101), so this exception propagates before a response can be rendered, resulting in an HTTP 500 with potential stack trace exposure.

**Evidence:**
- Line 43: `private String keypad_reader;` — String, bound from request.
- Line 129: `UnitBean.KeypadReaderModel.valueOf(keypad_reader)` — no guard beyond blank check.
- `validate()` line 101: `getUnit(null)` called unconditionally.
- `validation.xml`: no constraint on this field.

**Recommendation:**
Before calling `valueOf()`, validate the string against the known enum values. A safe pattern is:
```java
try {
    UnitBean.KeypadReaderModel.valueOf(keypad_reader);
} catch (IllegalArgumentException e) {
    errors.add("keypadReader", new ActionMessage("error.invalidKeypadReader"));
}
```
Or pre-enumerate valid values in `validate()` and reject anything not in the set.

---

### FINDING-04: op_code Side-Channel Bypasses validate() Entirely — Inputs Used in Database Queries Unvalidated
**Severity:** HIGH
**File:** `src/main/java/com/action/AdminUnitEditAction.java`, lines 36–47
**Related:** `src/main/webapp/WEB-INF/struts-config.xml`, lines 352–372

**Description:**
Three action paths (`/unitnameexists`, `/serialnoexists`, `/macaddressexists`) are mapped with `validate="false"` in struts-config.xml. Additionally, within the primary `/adminunitedit` action, the `op_code` field is checked before validation is invoked — when `op_code` is set to one of these keywords, the action returns early after executing a DAO query without any field validation having occurred. The inputs `name`, `serial_no`, and `mac_address` are passed directly to DAO methods. While the DAO methods use parameterised queries for these three fields, the lack of input sanitisation means that excessively long or malformed values are never rejected at the application tier. The `mac_address` check (`checkUnitByMacAddr`) has no `comp_id` scoping, so it leaks the existence of MAC addresses across all companies.

**Evidence:**
- `struts-config.xml` lines 353–372: three mappings with `validate="false"`.
- `AdminUnitEditAction.java` lines 36–47: `op_code` handling precedes any validation.
- `UnitDAO.java` line 180: `QUERY_COUNT_UNIT_BY_MAC_ADDRESS` — no `comp_id` filter.
- `UnitDAO.java` line 45: `checkUnitByMacAddr(adminUnitEditForm.getMac_address(), null)` — `null` passed as unit ID exclusion, no company scoping.

**Recommendation:**
Add length and format validation to `name`, `serial_no`, and `mac_address` before passing to DAO methods, even on the AJAX op_code paths. Scope `checkUnitByMacAddr` to the authenticated company to prevent cross-tenant information leakage. Consider requiring company ownership context for all existence checks.

---

### FINDING-05: Missing reset() Override — boolean accessible May Retain Stale State
**Severity:** MEDIUM
**File:** `src/main/java/com/actionform/AdminUnitEditForm.java` (no reset() method present)

**Description:**
Struts 1 `ActionForm` instances may be reused within the same session when `scope="request"` is used (as configured here). The Struts default `reset()` does not zero out fields. The `accessible` field is a Java primitive `boolean` which defaults to `false` on construction but is not explicitly reset between requests. If the form bean is ever placed in session scope (by configuration change or servlet container behaviour), stale values for `accessible`, `access_type`, `keypad_reader`, `facility_code`, and `access_id` could persist from a previous request and be silently applied to a subsequent save without the user having submitted those values.

**Evidence:**
- No `reset(ActionMapping, HttpServletRequest)` method in `AdminUnitEditForm.java`.
- Line 41: `private boolean accessible;` — primitive, not a Boolean object.
- `struts-config.xml` line 335: `scope="request"` — currently request scope, but absence of `reset()` is still a defence-in-depth gap.

**Recommendation:**
Implement `reset()` to explicitly null/false-initialise all fields, particularly `accessible` and all access-control fields. This is a standard Struts 1 hardening requirement.

---

### FINDING-06: Raw List Types — Type Safety Absent for Reference Data Collections
**Severity:** MEDIUM
**File:** `src/main/java/com/actionform/AdminUnitEditForm.java`, lines 35–37

**Description:**
Three fields use raw `List` types with no generic type parameter:
```java
private List arrAdminUnitType;
private List arrAdminUnitFuelType;
private List arrMenufacture;
```
Raw types suppress compile-time type checks. If the DAO returns unexpected types into these collections (e.g., after a DAO refactor), a `ClassCastException` will occur at runtime in the JSP/view layer rather than at the point of assignment, making the failure harder to diagnose. Additionally, `arrMenufacture` is declared but never populated by this form (the `setArrMenufacture()` setter is never called in the constructor or elsewhere in the form), so it will always be `null` when accessed by the view.

**Evidence:**
- Lines 35–37: `private List arrAdminUnitType`, `private List arrAdminUnitFuelType`, `private List arrMenufacture`.
- Constructor (lines 50–54): only `setArrAdminUnitType()` and `setArrAdminUnitFuelType()` are called; `arrMenufacture` is never initialised.
- `AdminUnitEditAction.java` line 34: manufacturer list is set on request directly via `ManufactureDAO`, so the form field is redundant but potentially confusing.

**Recommendation:**
Parameterise the List types (e.g., `List<UnitTypeBean>`). Remove or properly initialise `arrMenufacture` to avoid NPEs if the view references it.

---

### FINDING-07: Side-Effect in validate() — Business Logic Executed Unconditionally During Validation
**Severity:** MEDIUM
**File:** `src/main/java/com/actionform/AdminUnitEditForm.java`, lines 101–105

**Description:**
The `validate()` method, whose contract is to check inputs and return errors, also builds a `UnitBean` and writes it to the request attribute `arrAdminUnit` (lines 101–105):
```java
UnitBean unitBean = getUnit(null);
List<UnitBean> arrUnit = new ArrayList<>();
arrUnit.add(unitBean);
request.setAttribute("arrAdminUnit", arrUnit);
```
This is called **regardless of whether validation passes or fails**. When validation fails and the Struts framework re-renders the input page, the `arrAdminUnit` attribute will be set to a partially-constructed bean with `comp_id = null` (because `getUnit(null)` passes null). If the view layer iterates this list and attempts operations on `comp_id`, a NullPointerException or incorrect rendering may occur. The action itself also sets `arrAdminUnit` on the success path (line 60 in the action), creating a redundant and potentially conflicting code path.

**Recommendation:**
Remove the `request.setAttribute` call from `validate()`. Validation methods should be side-effect free. The action already manages `arrAdminUnit` on both success and failure paths.

---

### FINDING-08: No Validation on id Field Format — Potential for NumberFormatException on Database Operations
**Severity:** MEDIUM
**File:** `src/main/java/com/actionform/AdminUnitEditForm.java`, line 24
**Also:** `src/main/java/com/dao/UnitDAO.java`, line 495

**Description:**
The `id` field is accepted as a `String` and passed to `Long.valueOf(unitbean.getId())` in `UnitDAO.updateUnitInfo()` (line 495). No format validation on `id` is performed in `validate()` or anywhere in the form. A non-numeric `id` value (e.g., `"abc"`, `"' OR '1'='1"`) will throw a `NumberFormatException` at the DAO layer. While the DAO wraps this in a `try/catch(Exception)` that rethrows as `SQLException`, this still results in an HTTP 500 and potential stack trace exposure. A SQL-injection attempt via `id` is blocked by the parameterised query, but the application error behaviour is unnecessary and should be controlled.

**Evidence:**
- Line 24: `private String id;` — no format validation.
- `validate()` lines 64–108: no numeric check on `id`.
- `UnitDAO.java` line 495: `Long.valueOf(unitbean.getId())` — direct conversion without guard.

**Recommendation:**
Add a check in `validate()` to confirm `id` is numeric when non-blank. Use `StringUtils.isNumeric(id)` or a try-catch. This should be combined with the ownership check in FINDING-01.

---

### FINDING-09: No Validation on mac_address Format
**Severity:** LOW
**File:** `src/main/java/com/actionform/AdminUnitEditForm.java`, line 38

**Description:**
`mac_address` is stored as a free-form `String` with no format validation (e.g., no regex enforcing `XX:XX:XX:XX:XX:XX` or similar). The existence-check in `checkUnitByMacAddr` uses `ilike` with trim for matching, so inconsistently formatted MAC addresses (e.g., with/without colons, mixed case) could fail to deduplicate correctly even though the data is present.

**Evidence:**
- Line 38: `private String mac_address;` — no validation in `validate()` or `validation.xml`.
- `UnitDAO.java` line 180: `ilike trim(both ' ' from ?)` — case/format sensitive beyond whitespace trim.

**Recommendation:**
Add a regex validation for `mac_address` format in `validate()` and normalise to a canonical form (e.g., uppercase, colon-separated) before storage.

---

### FINDING-10: No Length Constraints on Any String Fields
**Severity:** LOW
**File:** `src/main/java/com/actionform/AdminUnitEditForm.java`, lines 25–48

**Description:**
None of the `String` fields (`name`, `location`, `department`, `serial_no`, `mac_address`, `exp_mod`, `access_type`, `facility_code`, `access_id`, `weight_unit`) have maximum length validation. An attacker may submit values exceeding database column widths, causing database truncation errors or, on databases without strict mode, silent data truncation. Oversized values in `name` or `serial_no` could also cause unexpected behaviour in the `ilike` comparisons used for duplicate checking.

**Recommendation:**
Add `maxlength` validators in `validation.xml` or explicit length checks in `validate()` aligned with the database column definitions for each field.

---

### FINDING-11: Constructor Calls DAO — Exception Risk on Form Instantiation
**Severity:** LOW
**File:** `src/main/java/com/actionform/AdminUnitEditForm.java`, lines 50–58

**Description:**
The constructor `AdminUnitEditForm()` is declared `throws Exception` and calls two DAO methods (`UnitDAO.getInstance().getAllUnitType()` and `UnitDAO.getInstance().getAllUnitFuelType()`). Struts instantiates `ActionForm` objects reflectively. If either DAO call fails (database unavailable, connection pool exhausted), the form cannot be instantiated, and Struts will throw an exception before the request is processed — this may produce a generic or leaked error page. Additionally, `throws Exception` on a constructor is overly broad.

**Recommendation:**
Populate reference data in the `reset()` method or lazily (on first access), not in the constructor, and narrow the declared exception to a specific type. This makes the form more robust to transient database failures.

---

### FINDING-12: adminUnitEditForm Absent from validation.xml
**Severity:** INFO
**File:** `src/main/webapp/WEB-INF/validation.xml`

**Description:**
Per the known stack context, `validation.xml` covers only three forms. `adminUnitEditForm` has no declarative validation rules. All validation relies on the programmatic `validate()` method, which is incomplete (see FINDING-01 through FINDING-10). This is noted for completeness; the individual validation gaps are each reported separately above.

---

## Category Summary

| Category | Result |
|---|---|
| Input Validation | FINDINGS: 01 (IDOR no ownership), 02 (hourmeter format), 03 (keypad_reader enum), 08 (id format), 09 (mac_address format), 10 (no length limits) |
| Type Safety | FINDINGS: 02 (Double.valueOf), 03 (enum valueOf), 06 (raw List), 08 (Long.valueOf) |
| IDOR Risk | FINDING-01 (CRITICAL): unit id fully controllable, UPDATE has no comp_id filter |
| Sensitive Fields | FINDING-04 (mac_address existence leak cross-tenant); access_control fields (accessible, access_type, facility_code, access_id) have no validation |
| Data Integrity | FINDINGS: 05 (no reset), 07 (side-effect in validate), 11 (constructor DAO calls) |
| CSRF | Structural gap noted at stack level (Struts 1.3.10, no token framework) — not re-reported per form; no token field present in this form |

---

## Finding Count by Severity

| Severity | Count | Finding IDs |
|---|---|---|
| CRITICAL | 1 | 01 |
| HIGH | 3 | 02, 03, 04 |
| MEDIUM | 4 | 05, 06, 07, 08 |
| LOW | 3 | 09, 10, 11 |
| INFO | 1 | 12 |
| **Total** | **12** | |
