# Security Audit: AdminManufacturersActionForm

**Audit run:** audit/2026-02-26-01/
**Branch:** master
**Stack:** Apache Struts 1.3.10
**Date:** 2026-02-26

---

## Reading Evidence

### Package and Class

- **File:** `src/main/java/com/actionform/AdminManufacturersActionForm.java`
- **Package:** `com.actionform`
- **Class:** `AdminManufacturersActionForm extends ActionForm`
- **Lombok annotations:** `@Getter`, `@Setter`, `@Slf4j`, `@NoArgsConstructor`

### Fields

| # | Name | Declared Type | Initial Value |
|---|------|--------------|---------------|
| 1 | `manufacturerId` | `String` | `null` |
| 2 | `manufacturer` | `String` | `null` |
| 3 | `action` | `String` | `null` |

### validate() / reset()

Neither `validate()` nor `reset()` is overridden. The class relies entirely on the Struts default `ActionForm` implementations, which perform no validation and perform a no-op reset.

### validation.xml Rules for this Form

`src/main/webapp/WEB-INF/validation.xml` contains rules for exactly three forms:

- `loginActionForm`
- `adminRegisterActionForm`
- `AdminDriverEditForm`

`AdminManufacturersActionForm` has **no entry** in `validation.xml`.

The struts-config action mapping at line 278 confirms `validate="false"`, so Commons Validator is never invoked for this form.

### Action Dispatch (AdminManufacturersAction.java)

The form drives four distinct database operations depending on the value of the `action` field:

| action value | Operation | Fields used |
|---|---|---|
| `add` | `ManufactureDAO.saveManufacturer()` | `manufacturer`, `sessCompId` (session) |
| `edit` | `ManufactureDAO.updateManufacturer()` | `manufacturerId`, `manufacturer` |
| `delete` | `ManufactureDAO.delManufacturById()` | `manufacturerId` |
| `isVehicleAssigned` | `ManufactureDAO.isVehicleAssignedToManufacturer()` | `manufacturerId` |
| _(anything else)_ | List page render | — |

### DAO SQL Patterns Relevant to this Form

| Method | SQL pattern | Parameterized? |
|---|---|---|
| `saveManufacturer` | `insert into manufacture (name, company_id) values (?, ?)` | Yes |
| `updateManufacturer` | `update manufacture set name = ? where id = ?` | Yes |
| `delManufacturById` | `delete from manu_type_fuel_rel where manu_id = ?` / `delete from manufacture where id = ?` | Yes |
| `isVehicleAssignedToManufacturer` | `select count(*) from unit where manu_id = ? and active is TRUE` | Yes |
| `getManufactureById` | `select id,name from manufacture where id = ` **+ id** | **No — raw concatenation** |
| `checkManuByNm` | `select id from manufacture where name = '` **+ name + `'`** | **No — raw concatenation** |
| `getManu_type_fuel_rel` | `... where manu_id = ` **+ manuId** | **No — raw concatenation** |

---

## Findings

---

### FINDING-01: No Server-Side Validation on Any Field

**Severity:** HIGH
**File:** `src/main/java/com/actionform/AdminManufacturersActionForm.java`, lines 14-16
**Also:** `src/main/webapp/WEB-INF/struts-config.xml`, line 278 (`validate="false"`)

**Description:**
`AdminManufacturersActionForm` does not override `validate()`, contains no JSR-303 / Bean Validation annotations, and is absent from `validation.xml`. The struts-config mapping sets `validate="false"`, meaning Commons Validator is explicitly disabled. All three fields (`manufacturerId`, `manufacturer`, `action`) are accepted from the HTTP request with no format, length, or content checks whatsoever before being passed to the DAO layer.

**Evidence:**
- `validation.xml` contains no `<form name="AdminManufacturersActionForm">` block.
- `struts-config.xml` line 278: `validate="false"`.
- `AdminManufacturersActionForm.java`: no `validate()` override, no annotations.

**Recommendation:**
Override `validate()` in the form class to enforce:
- `action`: whitelist against the four known values (`add`, `edit`, `delete`, `isVehicleAssigned`).
- `manufacturer`: required when action is `add` or `edit`; maximum length (e.g. 255 characters); reject characters outside printable ASCII or a defined safe set; minimum length 1 after trimming.
- `manufacturerId`: required when action is `edit`, `delete`, or `isVehicleAssigned`; must match `^\d+$` before any numeric conversion.
Add a corresponding `<form>` block to `validation.xml` and set `validate="true"` in struts-config.

---

### FINDING-02: No Maximum Length Constraint on `manufacturer` — Potential DoS / Database Truncation

**Severity:** MEDIUM
**File:** `src/main/java/com/actionform/AdminManufacturersActionForm.java`, line 15
**Also:** `src/main/java/com/dao/ManufactureDAO.java`, lines 180-208 (`saveManufacturer`), lines 210-244 (`updateManufacturer`)

**Description:**
The `manufacturer` field is declared as `String` with no length bound. An authenticated user can submit an arbitrarily long string. The DAO uses a parameterized `INSERT`/`UPDATE`, so the database driver will attempt to write the full value. Depending on the column type, this either causes a silent truncation (corrupted data) or a database error that propagates as an unhandled exception. On some JDBC drivers a very large string in a PreparedStatement can also consume significant server memory.

**Evidence:**
- `AdminManufacturersActionForm.java` line 15: `private String manufacturer = null;`
- No `maxlength` validation rule exists in `validation.xml` for this form.
- `ManufactureDAO.saveManufacturer` line 187: `ps.setString(1, manufactureBean.getName())` — no truncation guard.

**Recommendation:**
Add a `maxlength` validator in `validation.xml` (or in a `validate()` override) capping `manufacturer` at the database column length (confirm with schema; typically 255). Also add `maxlength` on the HTML input at the JSP level (`manufacturers.jsp` line 24-25) as a defence-in-depth measure, though server-side enforcement is mandatory.

---

### FINDING-03: `action` Field Accepted Without Whitelist — Uncontrolled Dispatch Path

**Severity:** MEDIUM
**File:** `src/main/java/com/actionform/AdminManufacturersActionForm.java`, line 16
**Also:** `src/main/java/com/action/AdminManufacturersAction.java`, lines 26-51

**Description:**
The `action` field is user-supplied and is used as a string-switch dispatch key in `AdminManufacturersAction.execute()`. There is no whitelist check: any value other than the four known strings silently reaches the `else` branch, which renders the manufacturer list page. While the current `else` branch is benign, the absence of whitelisting means:
1. Future code changes to the `else` branch could unintentionally expose new behaviour to unauthenticated callers who can guess or fuzz the parameter.
2. If Struts path traversal or expression injection issues exist in this version, a crafted `action` value could produce unexpected routing.
3. The `action` field accepts `null` (field initialized to `null`), and `adminManufacturersActionForm.getAction().equals("add")` at line 26 will throw a `NullPointerException` if the parameter is absent from the request, potentially leaking stack trace details depending on error page configuration.

**Evidence:**
- `AdminManufacturersActionForm.java` line 16: `private String action = null;`
- `AdminManufacturersAction.java` line 26: `adminManufacturersActionForm.getAction().equals("add")` — called directly on the possibly-null getter return value; no null guard.

**Recommendation:**
- Validate `action` server-side against an explicit whitelist of `{"add", "edit", "delete", "isVehicleAssigned"}` before dispatch, returning an error for unknown values.
- Guard against null: use `"add".equals(adminManufacturersActionForm.getAction())` (literal-first style), or perform an explicit null check in `validate()`.

---

### FINDING-04: `manufacturerId` Accepted as Unvalidated String — IDOR Risk on Edit, Delete, and Vehicle-Assignment Check

**Severity:** HIGH
**File:** `src/main/java/com/actionform/AdminManufacturersActionForm.java`, line 14
**Also:** `src/main/java/com/action/AdminManufacturersAction.java`, lines 35, 41, 45-46
**Also:** `src/main/java/com/dao/ManufactureDAO.java`, lines 99-135 (`delManufacturById`), lines 210-244 (`updateManufacturer`), lines 404-432 (`isVehicleAssignedToManufacturer`)

**Description:**
`manufacturerId` is a raw `String` taken directly from the HTTP request parameter. Any authenticated user of the application can supply an arbitrary integer ID, enabling:

1. **Edit IDOR:** `action=edit&manufacturerId=<any_id>&manufacturer=<new_name>` will overwrite the name of *any* manufacturer record in the database, including global (company_id IS NULL) system-level records, because `updateManufacturer` uses only `id` in its `WHERE` clause with no company-scope check.
2. **Delete IDOR:** `action=delete&manufacturerId=<any_id>` will delete *any* manufacturer record. The `delManufacturById` method likewise has no company_id ownership check.
3. **Information disclosure via isVehicleAssigned:** `action=isVehicleAssigned&manufacturerId=<any_id>` allows enumeration of whether any manufacturer ID has associated vehicles, leaking cross-tenant vehicle assignment data.

The `getAllManufactures` query used to populate the list correctly scopes to `company_id`, but the mutation operations do not enforce the same scope.

**Evidence:**
- `ManufactureDAO.updateManufacturer` (line 216): `update manufacture set name = ? where id = ?` — no `company_id` filter.
- `ManufactureDAO.delManufacturById` (line 114): `delete from manufacture where id = ?` — no `company_id` filter.
- `ManufactureDAO.isVehicleAssignedToManufacturer` (line 25): `select count(*) from unit where manu_id = ?` — no `company_id` filter.
- `AdminManufacturersAction.java` edit branch (line 35): `manufacture.setId(adminManufacturersActionForm.getManufacturerId())` — no ownership validation before calling DAO.

**Recommendation:**
- In `AdminManufacturersAction.java`, after extracting `manufacturerId`, query the manufacturer record and verify `company_id` matches `sessCompId` before permitting edit, delete, or any read operation on that record. Return a 403/error forward if the ownership check fails.
- Add `company_id` as a filter parameter to `updateManufacturer` and `delManufacturById` SQL: `WHERE id = ? AND company_id = ?`. This enforces the ownership constraint at the database layer even if the action-layer check is bypassed.
- Validate that `manufacturerId` is a positive integer in `validate()` before any database call.

---

### FINDING-05: No `reset()` Override — Stale Field Values in Reused Form Beans

**Severity:** LOW
**File:** `src/main/java/com/actionform/AdminManufacturersActionForm.java`, lines 13-17

**Description:**
The form scope is `request` (struts-config line 277), which mitigates the typical session-scope stale-value risk. However, because no `reset()` is overridden, any future change of scope to `session` would immediately allow stale `manufacturerId` or `action` values from a prior request to persist silently into a subsequent request, potentially causing unintended mutations. The absence of `reset()` is a latent defect.

**Evidence:**
- `AdminManufacturersActionForm.java`: no `reset()` method.
- `struts-config.xml` line 277: `scope="request"` (currently safe, but easily changed).

**Recommendation:**
Override `reset()` to explicitly null all three fields. This is defensive programming that removes the latent risk regardless of future scope changes.

---

### FINDING-06: SQL Injection in `ManufactureDAO` — Methods Reachable via `manufacturerId` String Field

**Severity:** CRITICAL
**File:** `src/main/java/com/dao/ManufactureDAO.java`
- `getManufactureById`: line 72
- `checkManuByNm`: lines 149-152
- `getManu_type_fuel_rel`: line 263

**Description:**
Three DAO methods used within the same manufacturer management feature build SQL by direct string concatenation of caller-supplied values:

1. `getManufactureById` (line 72):
   ```java
   String sql = "select id,name from manufacture where id = " + id;
   ```
   `id` is derived from caller input without parameterization.

2. `checkManuByNm` (lines 149-152):
   ```java
   String sql = "select id from manufacture where name = '" + name + "'";
   if (!id.equalsIgnoreCase("")) {
       sql += " and id !=" + id;
   }
   ```
   Both `name` and `id` are concatenated directly.

3. `getManu_type_fuel_rel` (line 263):
   ```java
   " where manu_id = " + manuId
   ```
   `manuId` is concatenated directly.

Although `getManufactureById`, `checkManuByNm`, and `getManu_type_fuel_rel` are not called by `AdminManufacturersAction` directly, they reside in the same `ManufactureDAO` class and are reachable from other actions. The `manufacturerId` `String` field on the form establishes the pattern of treating numeric IDs as unvalidated strings throughout the codebase, and any future wiring of these methods to a form that accepts user input would introduce a direct SQL injection vulnerability. The finding is recorded here because the form's type design (all-String fields, no validation) is the proximate cause.

**Evidence:**
- `ManufactureDAO.java` line 72: raw string concatenation in `getManufactureById`.
- `ManufactureDAO.java` line 149: raw string concatenation of `name` in `checkManuByNm`.
- `ManufactureDAO.java` line 263: raw string concatenation of `manuId` in `getManu_type_fuel_rel`.

**Recommendation:**
Replace all raw string concatenation in `ManufactureDAO` with parameterized `PreparedStatement` queries, consistent with the pattern already used in `saveManufacturer`, `updateManufacturer`, `delManufacturById`, and `isVehicleAssignedToManufacturer`. This should be treated as a separate DAO-level remediation task but is flagged here as CRITICAL due to the SQL injection class of vulnerability.

---

### FINDING-07: Stored XSS via Unescaped `manufacturer` Name in Dynamic HTML (JSP)

**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/settings/manufacturers.jsp`, lines 151-152

**Description:**
The `prepareTable()` JavaScript function rebuilds the manufacturer table via Ajax and writes `elem.name` directly into an `innerHTML` assignment without HTML-encoding:

```javascript
html += '<tr><td><div id="manufacturer-name-' + elem.id + '">' + elem.name + '</div>'
         + ' <input type="text" style="display:none;" id="manufacturer-edit-' + elem.id + '" value="' + elem.name + '" /></td><td>';
```

Because the `manufacturer` form field has no validation or sanitisation (FINDING-01, FINDING-02), an attacker with access to the `add` or `edit` action can persist a manufacturer name containing a JavaScript payload (e.g. `<img src=x onerror=alert(1)>`). Every user who loads the manufacturers page will execute that payload in the context of the admin application. The initial server-rendered JSP at line 52 uses `<bean:write>` which performs HTML escaping, but the Ajax re-render path does not.

**Evidence:**
- `manufacturers.jsp` line 151-152: `elem.name` written directly into `innerHTML` via `table.html(html)`.
- `manufacturers.jsp` line 54: `value="<%= manufacturer.getName() %>"` — also unescaped in a scriptlet, injectable into the `value` attribute of an input.
- No length or character validation on `manufacturer` field.

**Recommendation:**
- HTML-encode `elem.name` and `elem.id` before inserting into the `html` string in `prepareTable()`. Use a utility such as `$('<div>').text(elem.name).html()` to encode, or a dedicated escaping library.
- Replace the JSP scriptlet at line 54 (`<%= manufacturer.getName() %>`) with `<bean:write property="name" name="manufacturer" filter="true"/>` to ensure escaping on the initial render path as well.
- Enforce server-side character whitelisting for `manufacturer` (see FINDING-01) as a defence-in-depth measure.

---

### FINDING-08: CSRF — No Token Protection on State-Mutating Requests

**Severity:** HIGH
**File:** `src/main/webapp/html-jsp/settings/manufacturers.jsp` (all `$.post` calls), `src/main/java/com/action/AdminManufacturersAction.java`

**Description:**
The `add`, `edit`, and `delete` actions are invoked via unauthenticated Ajax `POST` requests with no CSRF token. Apache Struts 1.3.10 does not include built-in CSRF protection. `PandoraAction` adds no token check. This is consistent with the known structural CSRF gap across the application. A malicious page visited by a logged-in admin can silently add, rename, or delete manufacturer records.

**Evidence:**
- `manufacturers.jsp` lines 95, 114, 130: `$.post('manufacturers.do', {...})` — no token field included.
- `AdminManufacturersAction.java`: no token validation in `execute()`.
- `PandoraAction.java`: no CSRF token helper.
- Known structural gap documented in audit stack notes.

**Recommendation:**
Implement the synchronizer token pattern: generate a per-session CSRF token, embed it in the Struts form (and pass it in the Ajax `data` objects), and validate it in `AdminManufacturersAction.execute()` before processing any mutating action. As a partial mitigation, validate the `Origin`/`Referer` header server-side. A framework-level filter applied to all mutating actions is preferred.

---

### FINDING-09: `isVehicleAssigned` Check Issued via HTTP GET — State-Altering Logic Bypassed by Client

**Severity:** LOW
**File:** `src/main/webapp/html-jsp/settings/manufacturers.jsp`, lines 124-142

**Description:**
The client-side `delete_manufacturer()` function first calls `$.get('manufacturers.do', {action:'isVehicleAssigned', ...})` and only proceeds with the `POST` delete if the server returns `false`. This guard is entirely client-enforced. An attacker (or a user with browser developer tools) can skip the `isVehicleAssigned` GET and send the `delete` POST directly, deleting a manufacturer that is still assigned to active vehicles, resulting in referential integrity violation and potentially orphaned vehicle records.

**Evidence:**
- `manufacturers.jsp` lines 124-142: the integrity check precedes `$.post` delete but is not re-evaluated server-side.
- `AdminManufacturersAction.java` delete branch (lines 40-43): calls `ManufactureDAO.delManufacturById()` with no server-side vehicle-assignment check.

**Recommendation:**
Move the `isVehicleAssigned` check into the server-side `delete` branch of `AdminManufacturersAction.execute()`. Before calling `delManufacturById`, call `isVehicleAssignedToManufacturer` and return an error response if the result is `true`. The client-side check may be retained for UX but must not be the sole gate.

---

## Category Summary

| Category | Finding(s) | Highest Severity |
|---|---|---|
| Input Validation | FINDING-01, FINDING-02, FINDING-03 | HIGH |
| Type Safety | FINDING-03 (null on action field) | MEDIUM |
| IDOR Risk | FINDING-04 | HIGH |
| Sensitive Fields | No sensitive fields present (no PII, passwords, or tokens) | NO ISSUES |
| Data Integrity | FINDING-09 (client-only delete guard) | LOW |
| SQL Injection (DAO) | FINDING-06 | CRITICAL |
| XSS | FINDING-07 | HIGH |
| CSRF | FINDING-08 | HIGH |
| Form Lifecycle | FINDING-05 | LOW |

**Sensitive Fields: NO ISSUES.** The form handles only manufacturer name and ID. No passwords, tokens, PII, or financial data are present.

---

## Finding Count by Severity

| Severity | Count | Findings |
|---|---|---|
| CRITICAL | 1 | FINDING-06 |
| HIGH | 4 | FINDING-01, FINDING-04, FINDING-07, FINDING-08 |
| MEDIUM | 2 | FINDING-02, FINDING-03 |
| LOW | 2 | FINDING-05, FINDING-09 |
| INFO | 0 | — |
| **Total** | **9** | |
