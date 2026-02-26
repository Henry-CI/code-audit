# Security Audit Report: AdminUnitAccessForm

**Repository:** forkliftiqadmin
**Branch:** master
**Audit Run:** audit/2026-02-26-01/
**Auditor:** CIG Security Audit – Pass 1
**Date:** 2026-02-26
**Stack:** Apache Struts 1.3.10

---

## Files Examined

| File | Purpose |
|------|---------|
| `src/main/java/com/actionform/AdminUnitAccessForm.java` | Primary subject – ActionForm for unit access configuration |
| `src/main/webapp/WEB-INF/validation.xml` | Declarative validation rules |
| `src/main/java/com/action/AdminUnitAccessAction.java` | Consuming Action class |
| `src/main/java/com/bean/UnitBean.java` | Domain bean produced by getUnit() |
| `src/main/java/com/dao/UnitDAO.java` | Data layer – saveUnitAccessInfo(), getUnitById() |
| `src/main/webapp/WEB-INF/struts-config.xml` | Action mapping for /adminunitaccess |

---

## Reading Evidence

### Package and Class

```
package com.actionform;
public class AdminUnitAccessForm extends ActionForm   // line 23
```

Annotations: `@Data` (Lombok – generates getters, setters, equals, hashCode, toString) and `@NoArgsConstructor`.

### Fields

| Line | Name | Java Type | Notes |
|------|------|-----------|-------|
| 25 | `id` | `String` | Primary key of the `unit` row being operated on |
| 26 | `accessible` | `boolean` | Access-control flag |
| 27 | `access_type` | `String` | Free-form string – no enum or whitelist |
| 28 | `keypad_reader` | `String` | String representation of `KeypadReaderModel` enum; must be `valueOf`-parsed |
| 29 | `facility_code` | `String` | Physical access system facility code – security-sensitive |
| 30 | `access_id` | `String` | Access-system credential/card identifier – security-sensitive |

### validate() – lines 33–37

```java
public ActionErrors validate(ActionMapping mapping, HttpServletRequest request) {
    ActionErrors errors = new ActionErrors();
    return errors;
}
```

The method body is empty. It always returns an empty `ActionErrors` instance. **No validation logic is performed.**

### reset() – not present

No `reset()` override exists. Struts 1 resets `boolean` fields to `false` by default before each request, but String fields retain their previous state if omitted from the request. With no `reset()` override, partial-form submissions can silently carry over stale field values.

### validation.xml Coverage

The `<formset>` in `validation.xml` (lines 22–69) declares rules for exactly three forms:

- `loginActionForm`
- `adminRegisterActionForm`
- `AdminDriverEditForm`

`adminUnitAccessForm` is **absent** from `validation.xml`. No declarative field-level rules exist for this form.

### struts-config.xml Mapping (lines 510–518)

```xml
<action
    path="/adminunitaccess"
    name="adminUnitAccessForm"
    scope="request"
    type="com.action.AdminUnitAccessAction"
    validate="true"
    input="UnitAccessDefinition">
```

`validate="true"` is set, which will invoke `validate()` on the form. However, because `validate()` always returns an empty `ActionErrors`, this setting is effectively inert.

### Action-Layer Data Flow (AdminUnitAccessAction lines 17–37)

```java
String sessCompId = session.getAttribute("sessCompId") == null ? "" : (String) session.getAttribute("sessCompId");
String action = getRequestParam(request, "action", (String) null);
int companyId = Integer.parseInt(sessCompId);  // unchecked parse

AdminUnitAccessForm accessForm = (AdminUnitAccessForm) actionForm;

if ("save".equalsIgnoreCase(action)) {
    UnitBean unitBean = accessForm.getUnit(sessCompId);   // id comes from form, comp_id from session
    UnitDAO.saveUnitAccessInfo(unitBean);
} else {
    UnitBean unitBean = UnitDAO.getUnitById(accessForm.getId()).get(0);  // no cross-tenant check
    accessForm.setUnit(unitBean);
}
```

### saveUnitAccessInfo SQL (UnitDAO lines 513–528)

```java
private static final String UPDATE_UNIT_ACCESS =
    "update unit set accessible = ?, access_type = ?, access_id = ?, keypad_reader = ?, facility_code = ? " +
    "where id= ?";

public static void saveUnitAccessInfo(UnitBean unitbean) throws Exception {
    ...
    stmt.setLong(6, Long.valueOf(unitbean.getId()));  // id originates from form field
}
```

The `WHERE id = ?` clause uses the unit `id` supplied by the form. `comp_id` is passed into the bean but is **not** used in the `UPDATE_UNIT_ACCESS` query predicate.

---

## Audit Findings

---

### Finding 1 – CRITICAL: No Input Validation on Any Field

**Category:** Input Validation
**Severity:** CRITICAL
**File:** `src/main/java/com/actionform/AdminUnitAccessForm.java`, lines 33–37
**Secondary:** `src/main/webapp/WEB-INF/validation.xml` (entire file)

**Description:**
The `validate()` method is completely empty – it instantiates `ActionErrors` and returns it immediately without adding any error. The form is also entirely absent from `validation.xml`. All six fields (`id`, `accessible`, `access_type`, `keypad_reader`, `facility_code`, `access_id`) are accepted from HTTP request parameters with no format, length, or content checks whatsoever.

**Evidence:**

```java
// AdminUnitAccessForm.java lines 33-37
public ActionErrors validate(ActionMapping mapping, HttpServletRequest request) {
    ActionErrors errors = new ActionErrors();
    return errors;  // always empty – no checks
}
```

`adminUnitAccessForm` does not appear in `validation.xml`. The three forms that do appear are `loginActionForm`, `adminRegisterActionForm`, and `AdminDriverEditForm`.

**Recommendation:**
Implement validation logic inside `validate()` for every field. At minimum:
- `id`: required; must match `^\d+$`; numeric range check.
- `access_type`: required when `accessible` is true; restrict to known values via whitelist.
- `keypad_reader`: must be one of the four valid `KeypadReaderModel` enum names (ROSLARE, KERI, SMART, HID_ICLASS) or blank/null; reject all other values before `valueOf()` is called.
- `facility_code` and `access_id`: enforce maximum length; reject characters inappropriate for access-system identifiers.
Add `adminUnitAccessForm` to `validation.xml` as a complementary layer.

---

### Finding 2 – CRITICAL: IDOR – Unit ID Accepted from Request with No Ownership Verification

**Category:** IDOR / Authorization
**Severity:** CRITICAL
**Files:**
- `src/main/java/com/actionform/AdminUnitAccessForm.java`, line 25 (field `id`)
- `src/main/java/com/action/AdminUnitAccessAction.java`, lines 25–31
- `src/main/java/com/dao/UnitDAO.java`, lines 513–528 (`saveUnitAccessInfo`), lines 288–291 (`getUnitById`)

**Description:**
The `id` field (line 25) is a raw HTTP request parameter that becomes the primary key used in the `WHERE id = ?` clause of `UPDATE_UNIT_ACCESS`. The `comp_id` is retrieved from the session (`sessCompId`) and is passed to `getUnit()`, but inspection of `saveUnitAccessInfo` shows that `comp_id` is **never included in the SQL predicate**. An authenticated user from company A can submit any valid unit `id` belonging to company B and overwrite that unit's access control configuration (accessible flag, access_type, access_id, keypad_reader, facility_code).

For the read path (`getUnitById`), the query (via `UnitsByIdQuery`) fetches the unit by `id` alone with no `comp_id` filter in the action layer, allowing cross-tenant unit data to be read into the form and returned to the browser.

**Evidence:**

```java
// AdminUnitAccessAction.java lines 25-31
if ("save".equalsIgnoreCase(action)) {
    UnitBean unitBean = accessForm.getUnit(sessCompId);  // comp_id from session
    UnitDAO.saveUnitAccessInfo(unitBean);                // id from form, no ownership check in SQL
} else {
    UnitBean unitBean = UnitDAO.getUnitById(accessForm.getId()).get(0);  // no tenant filter
    accessForm.setUnit(unitBean);
}

// UnitDAO.java lines 513-515
private static final String UPDATE_UNIT_ACCESS =
    "update unit set accessible = ?, access_type = ?, access_id = ?, keypad_reader = ?, facility_code = ? " +
    "where id= ?";   // comp_id NOT in predicate
```

```java
// AdminUnitAccessForm.java line 41
.id(StringUtils.isBlank(id) ? null : id)   // id flows from HTTP to UnitBean unmodified
```

**Recommendation:**
Add `comp_id = ?` to the `WHERE` clause of `UPDATE_UNIT_ACCESS` and pass `unitbean.getComp_id()` as the second predicate parameter. Verify the affected row count equals exactly 1; if 0 rows are updated, treat it as an authorization failure and return an error response. Apply the same cross-tenant guard to `getUnitById` in the action layer by verifying that the returned unit's `comp_id` matches `sessCompId` before populating the form.

---

### Finding 3 – HIGH: Unguarded `KeypadReaderModel.valueOf()` Call – Runtime Exception on Arbitrary Input

**Category:** Input Validation / Type Safety
**Severity:** HIGH
**File:** `src/main/java/com/actionform/AdminUnitAccessForm.java`, line 46

**Description:**
`KeypadReaderModel.valueOf(keypad_reader)` is called with the raw string value of the `keypad_reader` field without any prior validation that the value is a member of the enum. Any request supplying a value not in `{ROSLARE, KERI, SMART, HID_ICLASS}` will cause `java.lang.IllegalArgumentException` to be thrown by the JVM. Depending on the Struts error-handling configuration, this may produce a 500 response with a stack trace, contributing to information disclosure. A blank value is guarded by `StringUtils.isNotBlank`, but any non-blank non-member string (e.g., `"INVALID"`, `"' OR '1'='1"`) reaches `valueOf()` unguarded.

**Evidence:**

```java
// AdminUnitAccessForm.java line 46
.keypad_reader(StringUtils.isNotBlank(keypad_reader) ? UnitBean.KeypadReaderModel.valueOf(keypad_reader) : null)
```

The four valid enum members are `ROSLARE`, `KERI`, `SMART`, `HID_ICLASS` (UnitBean.java lines 67–70). No prior whitelist check is performed.

**Recommendation:**
Before calling `valueOf()`, validate against the known enum values:
```java
boolean validModel = Arrays.stream(UnitBean.KeypadReaderModel.values())
    .anyMatch(m -> m.name().equals(keypad_reader));
```
Reject the request with an `ActionError` if the value is not valid. Alternatively use a try/catch around `valueOf()` and convert the `IllegalArgumentException` to an `ActionError` rather than propagating it as a 500.

---

### Finding 4 – HIGH: Sensitive Access Control Credentials Stored as Untyped, Unbounded Strings

**Category:** Sensitive Fields / Data Integrity
**Severity:** HIGH
**File:** `src/main/java/com/actionform/AdminUnitAccessForm.java`, lines 29–30

**Description:**
`facility_code` and `access_id` represent real-world physical access control system identifiers (keypad facility codes and card/credential IDs). Both are declared as unbounded `String` with no maximum length, format pattern, or character-set restriction on the form. They are written directly to the database via prepared statements in `saveUnitAccessInfo`. An attacker who can reach the form can supply arbitrarily long or specially crafted values that may overflow column constraints at the database level, corrupt access-system integration records, or interfere with downstream physical access control hardware that consumes these values.

**Evidence:**

```java
// AdminUnitAccessForm.java lines 29-30
private String facility_code;
private String access_id;

// UnitDAO.java lines 522-523
stmt.setString(3, unitbean.getAccess_id());
stmt.setString(5, unitbean.getFacility_code());
```

No length or format validation exists anywhere between the HTTP parameter and the SQL write.

**Recommendation:**
Define and enforce maximum lengths and a strict character whitelist (e.g., digits and hyphens for typical facility codes; alphanumeric for access IDs) within `validate()`. Consult the specific access-control hardware vendor specifications for the valid value ranges and encode those constraints explicitly.

---

### Finding 5 – HIGH: CSRF – No Token Protection on State-Changing Save Operation

**Category:** CSRF
**Severity:** HIGH
**File:** `src/main/java/com/actionform/AdminUnitAccessForm.java` (entire form); `src/main/webapp/WEB-INF/struts-config.xml`, lines 510–518

**Description:**
As established for this codebase, Struts 1.3.10 provides no built-in CSRF protection. The `/adminunitaccess` action with `action=save` modifies physical access control settings (accessible flag, keypad reader model, facility code, access credentials). The form contains no CSRF synchronizer token field and the `validate()` method performs no token check. A forged cross-site request from any page the authenticated admin visits will silently modify access control configuration for any unit whose `id` can be guessed or discovered.

**Evidence:**
- `validate()` (lines 33–37) is empty; no token field or token comparison is present.
- No `access_token`, `csrf_token`, or equivalent field exists among the six declared form fields (lines 25–30).
- struts-config.xml confirms the action is mapped with `scope="request"` and `validate="true"` but applies no token interceptor.

**Recommendation:**
Introduce a CSRF synchronizer token. In Struts 1 this requires a manual implementation: generate a random token per session (or per-request), store it in the session, embed it as a hidden field in the JSP form, and verify it in `validate()` by comparing the submitted token against the session-stored token. Reject requests where the tokens do not match before any business logic executes.

---

### Finding 6 – MEDIUM: No `reset()` Override – Stale Field Bleed on Partial Submissions

**Category:** Data Integrity
**Severity:** MEDIUM
**File:** `src/main/java/com/actionform/AdminUnitAccessForm.java` (absence of `reset()`)

**Description:**
Struts 1 calls `reset()` on the `ActionForm` before populating it with request parameters. The default `ActionForm.reset()` does nothing for String fields; it only resets `boolean` fields to `false` (which Struts handles implicitly for checkbox fields). Because `AdminUnitAccessForm` does not override `reset()`, all String fields (`id`, `access_type`, `keypad_reader`, `facility_code`, `access_id`) retain their previously populated values if those parameters are omitted from a subsequent request. In a request-scoped form (as configured) this is lower risk than session-scoped, but a second invocation within the same request processing chain could see stale values.

**Evidence:**
`reset()` is not declared anywhere in the class (lines 1–61). The struts-config.xml mapping uses `scope="request"` which mitigates but does not eliminate the concern in chained action scenarios.

**Recommendation:**
Override `reset()` and explicitly null or blank-initialise all String fields, and set `accessible` to `false`:
```java
@Override
public void reset(ActionMapping mapping, HttpServletRequest request) {
    id = null;
    accessible = false;
    access_type = null;
    keypad_reader = null;
    facility_code = null;
    access_id = null;
}
```

---

### Finding 7 – MEDIUM: `id` Field Has No Numeric Format or Range Validation Before DAO Use

**Category:** Input Validation / Type Safety
**Severity:** MEDIUM
**Files:**
- `src/main/java/com/actionform/AdminUnitAccessForm.java`, line 25
- `src/main/java/com/dao/UnitDAO.java`, line 290 (`Integer.parseInt(id)`) and line 526 (`Long.valueOf(unitbean.getId())`)

**Description:**
The `id` field is a `String` on the form. In `getUnitById()`, it is parsed with `Integer.parseInt(id)` (UnitDAO line 290). In `saveUnitAccessInfo()`, it is parsed with `Long.valueOf(unitbean.getId())` (UnitDAO line 526). Neither the form's `validate()` method nor any intervening layer checks that `id` is non-null, non-blank, or a valid non-negative integer before these parse calls. A blank or non-numeric submission will produce an unhandled `NumberFormatException` propagating as a 500 error. A null `id` reaches `Long.valueOf(null)` which throws `NullPointerException`.

**Evidence:**

```java
// UnitDAO.java line 290
return UnitsByIdQuery.prepare(Integer.parseInt(id)).query();

// UnitDAO.java line 526
stmt.setLong(6, Long.valueOf(unitbean.getId()));

// AdminUnitAccessForm.java line 41
.id(StringUtils.isBlank(id) ? null : id)  // passes null to DAO when blank
```

When `id` is blank, `getUnit()` sets `id = null` in the bean. `Long.valueOf(null)` then throws `NullPointerException` in `saveUnitAccessInfo`.

**Recommendation:**
In `validate()`, assert that `id` is non-blank and matches `^\d+$` before the form is accepted. Provide a user-facing error rather than allowing the exception to propagate.

---

### Finding 8 – LOW: `@Data` Lombok Annotation Exposes All Fields via Generated Setters

**Category:** Type Safety / Attack Surface
**Severity:** LOW
**File:** `src/main/java/com/actionform/AdminUnitAccessForm.java`, line 21

**Description:**
The `@Data` Lombok annotation generates public getters and setters for all fields. Struts 1 uses JavaBeans introspection to populate form fields from request parameters by matching parameter names to setter names. Because every field has a public setter, all six fields are automatically bindable from HTTP request parameters. This is the intended behaviour for form fields, but it means that the entire attack surface is public and can be targeted with crafted requests. There is no mechanism to mark any field as read-only or server-side-only at the form layer.

**Evidence:**
`@Data` at line 21 generates `setId()`, `setAccessible()`, `setAccess_type()`, `setKeypad_reader()`, `setFacility_code()`, and `setAccess_id()` — all publicly invokable by Struts' `BeanUtils` population mechanism from raw HTTP parameters.

**Recommendation:**
Review whether all six fields genuinely need to be settable via HTTP. If any fields should only be set programmatically (e.g., if `id` should be constrained to a server-side-validated path parameter), replace `@Data` with explicit `@Getter`/`@Setter` annotations and suppress the setter for those fields, or validate them rigorously in `validate()`.

---

## Category Summary

| Category | Findings | Highest Severity |
|----------|----------|-----------------|
| Input Validation | F1, F3, F7 | CRITICAL |
| IDOR / Authorization | F2 | CRITICAL |
| Type Safety | F3, F7, F8 | HIGH |
| Sensitive Fields | F4 | HIGH |
| CSRF | F5 | HIGH |
| Data Integrity | F4, F6 | HIGH |

**Categories with NO issues:** None — all five audited categories have at least one finding.

---

## Finding Count by Severity

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 2 | F1, F2 |
| HIGH | 3 | F3, F4, F5 |
| MEDIUM | 2 | F6, F7 |
| LOW | 1 | F8 |
| INFO | 0 | — |
| **Total** | **8** | |

---

## Structural Notes

1. The `validate="true"` attribute in struts-config.xml creates a false assurance — developers reading the config will assume validation is active, but the empty `validate()` body means it is not.
2. The `comp_id` session-scoping pattern used elsewhere in the application (e.g., `getAllUnitsByCompanyId` correctly uses the session value) is not applied to the `WHERE` clause of `UPDATE_UNIT_ACCESS`, creating an inconsistency that is the direct cause of the IDOR in F2.
3. The `BeanUtils` / `PropertyUtils` imports (lines 8–9) are unused in the current form implementation. Dead imports should be removed to reduce confusion about intent.
