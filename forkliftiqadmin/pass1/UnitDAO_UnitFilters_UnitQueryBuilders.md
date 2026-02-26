# Security Audit Report: UnitDAO, UnitFuelTypeBean, UnitManufactureFilter, UnitManufactureFilterHandler, UnitsByCompanyIdQuery, UnitsByIdQuery

**Date:** 2026-02-26
**Auditor:** Automated pass1 audit
**Branch:** master
**Severity key:** CRITICAL > HIGH > MEDIUM > LOW > INFO

---

## Files Audited

| File | Lines |
|---|---|
| `src/main/java/com/dao/UnitDAO.java` | 966 |
| `src/main/java/com/bean/UnitFuelTypeBean.java` | 29 |
| `src/main/java/com/querybuilder/filters/UnitManufactureFilter.java` | 5 |
| `src/main/java/com/querybuilder/filters/UnitManufactureFilterHandler.java` | 30 |
| `src/main/java/com/querybuilder/unit/UnitsByCompanyIdQuery.java` | 77 |
| `src/main/java/com/querybuilder/unit/UnitsByIdQuery.java` | 66 |

Supporting files read for context: `StringContainingFilterHandler.java`, `StatementPreparer.java`

---

## Findings

---

### CRITICAL: SQL Injection via serial_no string concatenation — getUnitBySerial()

**File:** `UnitDAO.java` (lines 199–240)

**Description:**
The method `getUnitBySerial(String serial_no, Boolean activeStatus)` builds a SQL query by directly concatenating the caller-supplied `serial_no` parameter into the query string, executed through a raw `Statement` (not a `PreparedStatement`). No sanitisation, escaping, or parameterisation is applied.

```java
// UnitDAO.java line 212
String sql = "select id,comp_id from unit where serial_no = '" + serial_no + "'";
if (activeStatus) {
    sql += " and active = true";
}
rs = stmt.executeQuery(sql);
```

A crafted value such as `' OR '1'='1` dumps all unit records. A value such as `'; DROP TABLE unit; --` or a stacked-query payload executes arbitrary DML/DDL depending on the JDBC driver and PostgreSQL configuration. Because the method returns `id` and `comp_id`, a successful injection can also be used to enumerate cross-tenant unit IDs without any `comp_id` predicate in place (see IDOR finding below).

The outer catch block re-throws a `new SQLException(e.getMessage())` which strips the original stack trace type, constituting partial exception swallowing.

**Risk:** Full database read/write/delete for any authenticated user who can reach any action that calls this method. Cross-tenant data exposure is a secondary consequence.

**Recommendation:** Replace `Statement` with `PreparedStatement`:
```java
String sql = "SELECT id, comp_id FROM unit WHERE serial_no = ?";
if (activeStatus) sql += " AND active = true";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setString(1, serial_no);
rs = ps.executeQuery();
```

---

### CRITICAL: SQL Injection via company list string concatenation into IN() clause — getUnitNameByComp()

**File:** `UnitDAO.java` (lines 293–338)

**Description:**
`getUnitNameByComp(String compId, Boolean activeStatus)` calls `cDAO.getSubCompanyLst(compId)` when the company is a dealer role, then splices the returned string directly into an `IN()` clause executed through a raw `Statement`.

```java
// UnitDAO.java lines 308–317
if (LoginDAO.isAuthority(compId, RuntimeConf.ROLE_DEALER)) {
    compLst = cDAO.getSubCompanyLst(compId);
}
String sql = "select id,name from unit where comp_id in (" + compLst + ")";
if (activeStatus) {
    sql += " and active is true";
}
rs = stmt.executeQuery(sql);
```

This is a **second-order injection** pattern. The `compLst` string is assembled by `CompanyDAO.getSubCompanyLst()` from database-stored company IDs. If those stored IDs can be influenced by an attacker (e.g., via a separate company name/metadata injection, or if `compId` is attacker-supplied and the dealer lookup itself is injectable), the resulting string is injected verbatim into the query without any validation. Even if the list is currently numeric, the method accepts `compId` directly from the session but there is zero runtime enforcement that the concatenated string is purely numeric before use.

Additionally, when the authenticated user is **not** a dealer, `compLst` is set to the raw `compId` parameter (line 301: `String compLst = compId;`), meaning a non-dealer authenticated user passing a crafted `compId` can inject directly if the caller does not validate the parameter before invocation.

**Risk:** Cross-tenant enumeration of all unit names; with a crafted payload, full SQL injection into a SELECT query (UNION-based data exfiltration, blind timing attacks).

**Recommendation:** Validate the company list is a comma-separated integer string before use, or — better — rewrite to use the `UnitsByCompanyIdQuery` PreparedStatement-based query builder which already handles the `comp_id` filter safely.

---

### CRITICAL: SQL Injection via company list string concatenation into IN() clause — getTotalUnitByID()

**File:** `UnitDAO.java` (lines 530–571)

**Description:**
Structurally identical vulnerability to `getUnitNameByComp()`. `getTotalUnitByID(String id, Boolean activeStatus)` follows the same pattern: optionally replaces `compLst` with the output of `cDAO.getSubCompanyLst(id)`, then concatenates it into a raw `Statement` SQL string.

```java
// UnitDAO.java lines 544–552
if (LoginDAO.isAuthority(id, RuntimeConf.ROLE_DEALER)) {
    compLst = cDAO.getSubCompanyLst(id);
}
String sql = "select count(id) from unit where comp_id in (" + compLst + ")";
if (activeStatus) {
    sql += " and active = true";
}
rs = stmt.executeQuery(sql);
```

The `id` parameter is documented as a company ID but nothing prevents it being a non-numeric string. Any caller forwarding a form parameter can inject into this path.

**Risk:** Same as `getUnitNameByComp()`. The returned value is a count string, making this a potential blind injection oracle in addition to data exfiltration.

**Recommendation:** Same as `getUnitNameByComp()`. Validate the list as integers or migrate to a parameterised approach.

---

### CRITICAL: SQL Injection via manu_id concatenation — getType()

**File:** `UnitDAO.java` (lines 610–651)

**Description:**
`getType(String manu_id)` normalises an empty string to `"0"` but otherwise concatenates the raw caller-supplied `manu_id` directly into the query string and executes it with a `Statement`.

```java
// UnitDAO.java lines 622–628
if (manu_id.equalsIgnoreCase("")) {
    manu_id = "0";
}
String sql = "select distinct(type.id),name from manu_type_fuel_rel" +
        " left outer join type on type.id = manu_type_fuel_rel.type_id " +
        " where manu_id = " + manu_id +
        " order by name";
rs = stmt.executeQuery(sql);
```

`manu_id` arrives as a `String` parameter. The only guard is an equality check for the empty string — it does not validate that the value is numeric. An attacker supplying `1 OR 1=1` or `1; SELECT pg_sleep(5)--` can manipulate the query.

This method is called from the XML API endpoint `GetXmlAction` (confirmed from prior audit batch context) in response to AJAX requests populating manufacturer/type dropdowns. This endpoint is reachable without additional authentication beyond the session guard, meaning any authenticated user of any tenant can send arbitrary `manu_id` values.

**Risk:** SQL injection into a reference-data query; UNION-based exfiltration of arbitrary tables.

**Recommendation:** Parse `manu_id` to `int`/`long` before use and throw `IllegalArgumentException` on parse failure, then use a `PreparedStatement`.

---

### CRITICAL: SQL Injection via manu_id and type_id concatenation — getPower()

**File:** `UnitDAO.java` (lines 653–697)

**Description:**
`getPower(String manu_id, String type_id)` concatenates **two** unsanitised parameters into the query string.

```java
// UnitDAO.java lines 665–671
String sql = "select fuel_type.id,name from manu_type_fuel_rel" +
        " left outer join fuel_type on fuel_type.id = manu_type_fuel_rel.fuel_type_id " +
        " where manu_id = " + manu_id;

if (!type_id.equalsIgnoreCase("")) {
    sql += " and type_id= " + type_id;
}
sql += " order by name";
rs = stmt.executeQuery(sql);
```

Unlike `getType()`, there is **no default/normalisation guard** on `manu_id` in `getPower()` — if `manu_id` is an empty string the raw empty string is interpolated, producing invalid SQL and an exception. Neither parameter is validated for numeric content. Both are separately injectable.

**Risk:** Same as `getType()`. Two independent injection vectors in a single method.

**Recommendation:** Parse both parameters to `int`/`long` and use a `PreparedStatement` with two bind parameters.

---

### CRITICAL: SQL Injection + missing comp_id filter (IDOR) — delUnitById()

**File:** `UnitDAO.java` (lines 340–362)

**Description:**
`delUnitById(String id)` performs a soft-delete (sets `active = false`) by concatenating the raw `id` string into an UPDATE statement executed via a raw `Statement`.

```java
// UnitDAO.java line 349
String sql = "update unit set active = false where id=" + id;
stmt.executeUpdate(sql);
```

Two distinct vulnerabilities are present simultaneously:

1. **SQL Injection:** `id` is not validated as numeric. An authenticated user can supply `id = "1 OR 1=1"` to soft-delete every unit across all tenants, or supply a UNION/subquery payload to exfiltrate data via error messages.

2. **IDOR (missing tenant check):** The UPDATE has no `AND comp_id = <session comp_id>` predicate. The caller (`AdminUnitEditAction`) reads `equipId` from the form, reads `sessCompId` from the session, and passes only `equipId` to this method. The DAO never verifies that the unit identified by `id` belongs to the authenticated user's company. A tenant-A user who knows any integer unit ID belonging to tenant-B can soft-delete it.

**Risk:** Cross-tenant destructive write. Any authenticated user can deactivate units owned by other tenants. Combined with the injection, a single request can deactivate the entire unit table.

**Recommendation:** Add `AND comp_id = ?` to the UPDATE predicate and use a `PreparedStatement` with both `id` and `sessCompId` bound as integer parameters. Verify that `executeUpdate()` returns exactly 1 and throw an exception if not.

---

### CRITICAL: IDOR — getUnitById() fetches any unit without tenant scope

**File:** `UnitDAO.java` (line 288–291); `UnitsByIdQuery.java` (lines 14, 26–29)

**Description:**
`getUnitById(String id)` delegates unconditionally to `UnitsByIdQuery.prepare(Integer.parseInt(id)).query()`.

```java
// UnitDAO.java lines 288–291
public static List<UnitBean> getUnitById(String id) throws SQLException {
    log.info("Inside LoginDAO Method : getUnitById");
    return UnitsByIdQuery.prepare(Integer.parseInt(id)).query();
}
```

```java
// UnitsByIdQuery.java line 14
private static final String query = "SELECT * FROM v_units WHERE id = ?";
```

The underlying `UnitsByIdQuery` uses a `PreparedStatement` and parameterises the `id` bind correctly, so there is **no SQL injection** here. However, the query contains **no `comp_id` predicate**. The `v_units` view covers all tenants. Any authenticated user who can trigger a call to `getUnitById` (e.g., via `AdminUnitEditAction` which reads `equipId` from a form field) can retrieve full unit detail — including `serial_no`, `mac_address`, `access_id`, `facility_code`, `keypad_reader` — for any unit in the database regardless of tenant ownership.

The `UnitsByIdQuery` class itself has no facility to add a tenant filter; it is a structural IDOR by design.

**Risk:** Full cross-tenant read of unit records, including physical access control credentials (`access_id`, `facility_code`, `keypad_reader`).

**Recommendation:** Add a `companyId` filter to `UnitsByIdQuery` (e.g., `WHERE id = ? AND comp_id = ?`) and pass `sessCompId` from the session into every call site. Alternatively, add a post-fetch ownership assertion in `getUnitById`.

---

### HIGH: IDOR — getServiceByUnitId() fetches service record for any unit without tenant check

**File:** `UnitDAO.java` (lines 761–815)

**Description:**
`getServiceByUnitId(String unitId)` queries `unit_service` joined to `unit` using only `unit_id = ?` as the predicate.

```java
// UnitDAO.java line 771
String sql = "select us.*, u.hourmeter, ... from unit_service us left outer join unit u on us.unit_id = u.id where us.unit_id = ?";
ps.setInt(1, Integer.parseInt(unitId));
```

No `comp_id` constraint is applied. Any authenticated user who supplies a `unitId` belonging to a different tenant receives that tenant's service/maintenance schedule, including accumulated hours, last service date, service type, and next service threshold.

**Risk:** Cross-tenant disclosure of equipment maintenance schedules.

**Recommendation:** Join to `unit` and add `AND u.comp_id = ?` to the WHERE clause, binding `sessCompId` from the session.

---

### HIGH: IDOR — getImpactByUnitId() fetches calibration/impact config for any unit without tenant check

**File:** `UnitDAO.java` (lines 817–831)

**Description:**
`getImpactByUnitId(Long unitId)` uses a static parameterised query `QUERY_IMPACT_BY_UNIT` that selects from `unit` joined to `unit_service` with only `u.id = ?` as the filter.

```java
// UnitDAO.java lines 817–820
private static final String QUERY_IMPACT_BY_UNIT = "select s.acc_hours, u.alert_enabled, u.impact_threshold, u.reset_calibration_date, u.calibration_date "
        + "from unit u "
        + "left outer join unit_service s on u.id = s.unit_id "
        + "where u.id = ?";
```

No tenant scope is enforced. Any authenticated user who knows a numeric unit ID can retrieve impact alert thresholds and calibration dates for units belonging to other tenants.

**Risk:** Cross-tenant information disclosure of safety-critical impact configuration.

**Recommendation:** Add `AND u.comp_id = ?` to the static query and pass the session company ID at every call site.

---

### HIGH: IDOR — getChecklistSettings() fetches driver-based checklist flag for any unit without tenant check

**File:** `UnitDAO.java` (lines 833–873)

**Description:**
`getChecklistSettings(String unitId)` queries `unit` using only `u.id = ?`.

```java
// UnitDAO.java lines 843–851
String sql = "select u.driver_based from unit u where u.id = ?";
ps.setInt(1, Integer.parseInt(unitId));
```

No `comp_id` constraint. An authenticated user can read `driver_based` for any unit in the system.

**Risk:** Minor cross-tenant information disclosure; also confirms the unit ID is valid, which aids enumeration.

**Recommendation:** Add `AND u.comp_id = ?` and bind `sessCompId`.

---

### HIGH: IDOR — updateChecklistSettings() updates any unit without tenant check

**File:** `UnitDAO.java` (lines 879–907)

**Description:**
`updateChecklistSettings(ChecklistBean bean)` issues `UPDATE unit SET driver_based = ? WHERE id = ?` with no `comp_id` predicate.

```java
// UnitDAO.java lines 888–892
String sql = "update unit set driver_based = ? where id = ?";
ps.setBoolean(1, bean.isDriverBased());
ps.setInt(2, bean.getEquipId());
```

Any authenticated user can flip the `driver_based` flag on any unit across all tenants by supplying an arbitrary `equipId`.

**Risk:** Cross-tenant configuration write; can disable or enable driver-based checklists on units owned by other companies, directly affecting safety-critical pre-operation inspection workflows.

**Recommendation:** Add `AND comp_id = ?` to the UPDATE predicate. Bind the `sessCompId` from session. Verify `executeUpdate() == 1`.

---

### HIGH: IDOR — saveUnitAccessInfo() updates access credentials for any unit without tenant check

**File:** `UnitDAO.java` (lines 513–528)

**Description:**
`saveUnitAccessInfo(UnitBean unitbean)` issues an UPDATE via the static constant `UPDATE_UNIT_ACCESS`:

```java
// UnitDAO.java lines 513–515
private static final String UPDATE_UNIT_ACCESS =
        "update unit set accessible = ?, access_type = ?, access_id = ?, keypad_reader = ?, facility_code = ? " +
                "where id= ?";
```

The `id` bound in position 6 is `Long.valueOf(unitbean.getId())` which is taken directly from the form bean. No `comp_id` predicate exists. An attacker can overwrite `access_id`, `facility_code`, and `keypad_reader` (RFID/keypad physical access credentials) for units belonging to other tenants.

**Risk:** Cross-tenant write to physical access control credentials. Depending on the access control hardware, this could unlock or re-configure forklifts in other companies' facilities.

**Recommendation:** Add `AND comp_id = ?` to `UPDATE_UNIT_ACCESS`. Bind `sessCompId` as an additional parameter. This is a high-severity operational safety risk beyond pure data confidentiality.

---

### HIGH: IDOR — deleteAssignment() deletes any unit_company assignment without tenant check

**File:** `UnitDAO.java` (lines 78–89)

**Description:**
`deleteAssignment(String id)` deletes a row from `unit_company` by primary key alone:

```java
// UnitDAO.java line 78
private static final String DELETE_UNIT_ASSIGNMENT = "delete from unit_company where id = ?";
```

No company scope check. Any authenticated user who enumerates or guesses an assignment `id` integer can delete assignments belonging to other tenants, immediately stripping those companies' access to their own assigned units.

**Risk:** Cross-tenant destructive write to unit assignments.

**Recommendation:** Join to `unit` or `unit_company` to enforce `company_id = <sessCompId>` in the DELETE predicate, or verify ownership before deletion.

---

### HIGH: IDOR — isAssignmentOverlapping() checks overlaps across all tenants

**File:** `UnitDAO.java` (lines 91–114)

**Description:**
`QUERY_ASSIGN_DATE_OVERLAP_CHECK` filters only by `unit_id`:

```java
// UnitDAO.java lines 91–96
private static final String QUERY_ASSIGN_DATE_OVERLAP_CHECK =
        "select count(id) from unit_company " +
                "where ((? between start_date and end_date) or " +
                "(? between start_date and end_date) or " +
                "end_date is null and start_date <= ?) and " +
                "unit_id = ? ";
```

No `company_id` scope. If a unit belongs to tenant-B but tenant-A knows its ID, calling `isAssignmentOverlapping` with tenant-B's `unitId` leaks whether any assignment exists for those dates. This is an information disclosure issue rather than a data modification issue.

**Risk:** Cross-tenant enumeration of unit assignment schedules.

**Recommendation:** Add `AND company_id = ?` and bind `sessCompId`.

---

### HIGH: Unsafe orderBy string injection in UnitsByCompanyIdQuery

**File:** `UnitsByCompanyIdQuery.java` (lines 33–36, 48–56)

**Description:**
The `orderBy(String orderBy)` method accepts an arbitrary string and appends it directly to the SQL query without quoting, whitelisting, or parameterisation:

```java
// UnitsByCompanyIdQuery.java lines 33–36
public UnitsByCompanyIdQuery orderBy(String orderBy) {
    this.orderBy = " order by " + orderBy;
    return this;
}
```

The constructed string is then appended verbatim to the final query in `query()` (line 53):

```java
query.append(orderBy);
```

Callers in `UnitDAO` currently pass hardcoded literals (`"name ASC"`, `"name"`), so in those specific call sites the injection surface is unexploited. However, if any call site in the wider application — or a future developer — passes a caller-controlled value (e.g., a sort parameter from a form), this becomes a direct ORDER BY injection. PostgreSQL ORDER BY injection can be used for blind data exfiltration via `CASE WHEN ... THEN field1 ELSE field2 END` payloads. The architecture encourages unsafe use.

**Risk:** Blind SQL injection if the `orderBy` parameter is ever sourced from user input, which the method signature invites.

**Recommendation:** Enforce a whitelist of permitted column names and directions (e.g., `"name ASC"`, `"name DESC"`, `"serial_no ASC"`) inside the `orderBy()` method. Throw `IllegalArgumentException` for any non-whitelisted value.

---

### MEDIUM: Singleton broken double-checked locking — non-volatile instance field

**File:** `UnitDAO.java` (lines 24–35)

**Description:**
The `UnitDAO` singleton uses double-checked locking (DCL), but the `theInstance` field is declared without the `volatile` keyword:

```java
// UnitDAO.java lines 24–35
private static UnitDAO theInstance;   // <-- NOT volatile

public static UnitDAO getInstance() {
    if (theInstance == null) {            // first check — unsynchronised read
        synchronized (UnitDAO.class) {
            if (theInstance == null) {    // second check — inside lock
                theInstance = new UnitDAO();
            }
        }
    }
    return theInstance;
}
```

Without `volatile`, the Java Memory Model does not guarantee that the write to `theInstance` in the constructor is visible to threads that read `theInstance` in the first (unsynchronised) check. Under the JMM, a thread may observe a non-null but partially initialised `UnitDAO` reference. In practice, on the HotSpot JVM with x86, the bug is rarely triggered, but it is a formal correctness defect. The same pattern has been flagged in prior batches for other DAOs in this codebase.

**Risk:** On a heavily loaded Tomcat instance or when using a JIT-aggressive JVM, a thread could receive a partially initialised singleton, leading to `NullPointerException` or corrupt state in DAO operations.

**Recommendation:** Declare `private static volatile UnitDAO theInstance;` or, preferably, use the initialization-on-demand holder idiom:
```java
private static class Holder {
    static final UnitDAO INSTANCE = new UnitDAO();
}
public static UnitDAO getInstance() { return Holder.INSTANCE; }
```

---

### MEDIUM: Exception swallowing — original exception type stripped on rethrow

**File:** `UnitDAO.java` (multiple methods)

**Description:**
Every legacy method (those using raw `Statement`) catches `Exception` and rethrows a new `SQLException` constructed from only the message string:

```java
// Pattern repeated in: getUnitBySerial() (line 229), getUnitNameByComp() (line 327),
// getTotalUnitByID() (line 560), getType() (line 639), getPower() (line 685),
// delUnitById() (line 354), getAllUnitType() (line 387), getAllUnitFuelType() (line 426),
// getAllUnitAttachment() (line 596), saveService() (line 748),
// getServiceByUnitId() (line 803), getSessionHoursCalilbration() (line 943)
} catch (Exception e) {
    InfoLogger.logException(log, e);
    e.printStackTrace();
    throw new SQLException(e.getMessage());
}
```

The `new SQLException(e.getMessage())` discards the original exception's type, cause chain, and stack trace. Callers that examine the exception type (e.g., catching `ClassCastException` separately from `SQLException`) will have their logic bypassed. Additionally, `e.printStackTrace()` writes to `stderr` (which in a containerised Tomcat deployment is typically swallowed or interleaved with other output) rather than to the structured logger that is already available (`log`).

**Risk:** Debugging difficulty (cause chain lost), potential swallowing of non-SQL exceptions that callers might need to handle differently. Not directly exploitable, but impedes incident response.

**Recommendation:** Use `throw new SQLException(e.getMessage(), e)` to preserve the cause chain, or simply `throw` the original exception where the method signature allows. Replace `e.printStackTrace()` with `log.error("...", e)`.

---

### MEDIUM: UnitsByIdQuery returns SELECT * from v_units — overly broad column exposure

**File:** `UnitsByIdQuery.java` (line 14)

**Description:**
The base query selects all columns from the view `v_units`:

```java
private static final String query = "SELECT * FROM v_units WHERE id = ?";
```

The `getResult()` mapper maps at least 20 columns including `access_id`, `facility_code`, `keypad_reader`, `mac_address`, `serial_no`, and `acc_hours`. If the view is later extended with additional sensitive columns, all callers of `getUnitById()` will silently receive those columns without any change to the application code. Combined with the IDOR finding (no `comp_id` filter), this maximises the data exposed per cross-tenant read.

**Risk:** Any view schema change automatically exposes new sensitive fields to all callers without explicit review. Amplifies the IDOR impact.

**Recommendation:** Replace `SELECT *` with an explicit column list matching the fields required by the mapper. This also documents the data contract between the query and the mapper.

---

### MEDIUM: getUnitBySerial() returns comp_id of matched unit to caller without validating ownership

**File:** `UnitDAO.java` (lines 199–240)

**Description:**
Aside from the SQL injection vulnerability (documented above), `getUnitBySerial()` has no `comp_id` parameter and applies no tenant filter. The method is designed to look up a unit across the entire unit table by serial number. It returns both the `id` and the `comp_id` of the matched unit. The caller can use this to confirm which company owns a given serial number.

```java
String sql = "select id,comp_id from unit where serial_no = '" + serial_no + "'";
```

If an attacker knows or guesses a serial number (these are often manufacturer-assigned and predictable), they can call this endpoint to confirm the `comp_id` mapping even before exploiting the SQL injection. The method is also called from `AdminUnitEditAction` during save operations with the serial from the form field.

**Risk:** Cross-tenant serial number enumeration / tenant ID discovery. Amplifies IDOR risk across the application.

**Recommendation:** Accept and bind a `compId` parameter and add `AND comp_id = ?` to the query, or validate post-fetch that the returned `comp_id` matches `sessCompId`.

---

### MEDIUM: UnitManufactureFilterHandler injects fieldName into SQL without whitelist

**File:** `UnitManufactureFilterHandler.java` (lines 16–19)

**Description:**
`getQueryFilter()` formats the `fieldName` constructor argument directly into the SQL fragment using `String.format()`:

```java
// UnitManufactureFilterHandler.java lines 16–19
public String getQueryFilter() {
    if (ignoreFilter()) return "";
    return String.format(" AND %s = ? ", fieldName);
}
```

`fieldName` is set at construction time and in current call sites is a hardcoded literal. However, there is no enforcement at the class level that `fieldName` must be from a permitted set of column names. If any future caller (or an injected `UnitManufactureFilter` implementation) passes a crafted `fieldName` containing a SQL fragment, it will be interpolated directly into the query. This is a latent injection risk in the filter infrastructure that mirrors the same concern in `UnitsByCompanyIdQuery.orderBy()`.

**Risk:** Future SQL injection if `fieldName` is ever derived from user input.

**Recommendation:** Validate `fieldName` against a whitelist of permitted column names in the constructor and throw `IllegalArgumentException` for unknown values.

---

### LOW: StringContainingFilterHandler injects fieldNames directly into SQL

**File:** `StringContainingFilterHandler.java` (lines 19–29)

**Description:**
`getQueryFilter()` appends each element of `fieldNames` directly into the ILIKE clause:

```java
filter.append(fieldName).append(" ILIKE ? OR ");
```

Current callers pass hardcoded field names (`"name"`, `"serial_no"`), so this is not currently exploitable. The risk is the same as `UnitManufactureFilterHandler.fieldName` — the class provides no whitelist guard. The filter is used by `UnitsByCompanyIdQuery.containing()`, which is called from `UnitDAO.getAllUnitSearch()` (line 963). If `getAllUnitSearch()` ever accepts a sort/filter field name from user input, this path becomes injectable.

**Risk:** Latent SQL injection; currently unexploited because all callers use literals.

**Recommendation:** Whitelist permitted field names in the constructor.

---

### LOW: UnitFuelTypeBean — serialVersionUID is arbitrary, no equals/hashCode

**File:** `UnitFuelTypeBean.java` (lines 5–29)

**Description:**
`UnitFuelTypeBean` implements `Serializable` with an explicitly set `serialVersionUID = -5196370581161097760L`. The class has no `equals()` or `hashCode()` implementation. This is not a security vulnerability per se, but:

1. If beans are ever stored in an `HttpSession` and the session is serialised to disk (Tomcat's `PersistentManager`) or replicated across cluster nodes, a version mismatch caused by adding/removing fields without updating `serialVersionUID` will silently corrupt sessions.
2. The lack of `equals()`/`hashCode()` means two `UnitFuelTypeBean` instances with identical values are never equal under `List.contains()` or `Set` operations, which can lead to duplicates in collections returned from DAO methods.

**Risk:** Low probability session deserialisation issue; logical correctness defects in collection operations.

**Recommendation:** Override `equals()` and `hashCode()` based on `id`. Ensure `serialVersionUID` is updated on structural changes.

---

### LOW: getUnitMaxId() uses SELECT max(id)+1 — race condition and information disclosure

**File:** `UnitDAO.java` (lines 252–286)

**Description:**
`getUnitMaxId()` executes `SELECT max(id) FROM unit` and returns `max + 1` as a suggested next ID. This value is presumably used as a hint or pre-flight check before insertion.

```java
String sql = "select max(id) from unit";
rs = stmt.executeQuery(sql);
if (rs.next()) {
    count = rs.getInt(1) + 1;
}
```

Two issues:
1. **Race condition:** Between the SELECT and any subsequent INSERT, another thread or process may insert a row, causing a collision or an off-by-one.
2. **Information disclosure:** The maximum unit ID across the entire table (all tenants) is returned to the caller. This leaks the global unit count and the highest cross-tenant unit ID to whoever calls this method, which aids IDOR enumeration attacks.

**Risk:** Logical correctness defect (race condition); minor information disclosure that assists IDOR attacks.

**Recommendation:** Remove this method. Use database-level SERIAL/IDENTITY or `INSERT ... RETURNING id` (PostgreSQL) for ID generation, which is atomic and requires no pre-computation.

---

### INFO: Legacy Statement pattern used in multiple methods — debt inventory

**File:** `UnitDAO.java` (multiple methods)

**Description:**
A number of methods in `UnitDAO` use the legacy `Statement` + `ResultSet.TYPE_SCROLL_SENSITIVE` + `CONCUR_READ_ONLY` pattern rather than the newer `PreparedStatement`-based `DBUtil.queryForObject` / `DBUtil.queryForObjects` helpers used elsewhere in the same class and throughout the query-builder layer.

Methods using raw `Statement`:
- `getUnitBySerial()` (line 209)
- `getUnitMaxId()` (line 262)
- `getUnitNameByComp()` (line 305)
- `delUnitById()` (line 347)
- `getAllUnitType()` (line 374)
- `getAllUnitFuelType()` (line 411)
- `getTotalUnitByID()` (line 540)
- `getAllUnitAttachment()` (line 583)
- `getType()` (line 620)
- `getPower()` (line 663)

Methods using `PreparedStatement` or `DBUtil` helpers (safe pattern):
- `addAssignment()`, `deleteAssignment()`, `isAssignmentOverlapping()`, `checkUnitByNm()`, `checkUnitBySerial()`, `checkUnitByMacAddr()`, `saveUnitInfo()`, `updateUnitInfo()`, `saveUnitAccessInfo()`, `saveService()`, `getServiceByUnitId()`, `getImpactByUnitId()`, `getChecklistSettings()`, `updateChecklistSettings()`, `getSessionHoursCalilbration()`

The split suggests the legacy methods were written before the `DBUtil` helper was introduced and have not been migrated.

**Risk:** Informational. The legacy pattern itself is not a vulnerability unless strings are concatenated (which they are in the CRITICAL/HIGH findings above), but it represents technical debt that makes future injection errors more likely.

**Recommendation:** Migrate all raw-`Statement` methods to the `DBUtil.queryForObject` / `DBUtil.queryForObjects` / `DBUtil.updateObject` pattern with `PreparedStatement` bind parameters. `getAllUnitType()`, `getAllUnitFuelType()`, `getAllUnitAttachment()`, and `getUnitMaxId()` have no injection today (fixed strings) but benefit from migration for consistency and to prevent regression.

---

### INFO: ResultSet.TYPE_SCROLL_SENSITIVE used on queries that only do forward iteration

**File:** `UnitDAO.java` (lines 209, 262, 305, 347, 374, 411, 540, 583, 620, 663)

**Description:**
All legacy `Statement` instantiations use `ResultSet.TYPE_SCROLL_SENSITIVE`:

```java
stmt = conn.createStatement(ResultSet.TYPE_SCROLL_SENSITIVE, ResultSet.CONCUR_READ_ONLY);
```

However, every result set in these methods is iterated forward-only (`rs.next()` / `while (rs.next())`). `TYPE_SCROLL_SENSITIVE` causes the JDBC driver to potentially hold a server-side cursor or buffer the full result set, consuming more memory and server resources than the default `TYPE_FORWARD_ONLY`. On large `unit` tables, this could cause excessive memory consumption under load.

**Risk:** Informational / performance. No direct security impact, but excessive memory usage can degrade availability.

**Recommendation:** Use the default `conn.createStatement()` (which is `TYPE_FORWARD_ONLY`, `CONCUR_READ_ONLY`) for forward-only iteration, or migrate to `PreparedStatement` as recommended above.

---

## Summary

| # | Severity | Title | File | Line(s) |
|---|---|---|---|---|
| 1 | CRITICAL | SQLi via serial_no concatenation — getUnitBySerial() | UnitDAO.java | 212 |
| 2 | CRITICAL | SQLi via company list IN() concatenation — getUnitNameByComp() | UnitDAO.java | 311 |
| 3 | CRITICAL | SQLi via company list IN() concatenation — getTotalUnitByID() | UnitDAO.java | 548 |
| 4 | CRITICAL | SQLi via manu_id concatenation — getType() | UnitDAO.java | 627 |
| 5 | CRITICAL | SQLi via manu_id+type_id concatenation — getPower() | UnitDAO.java | 667,670 |
| 6 | CRITICAL | SQLi + IDOR (no comp_id) — delUnitById() | UnitDAO.java | 349 |
| 7 | CRITICAL | IDOR — getUnitById() no tenant scope | UnitDAO.java / UnitsByIdQuery.java | 288 / 14 |
| 8 | HIGH | IDOR — getServiceByUnitId() no tenant scope | UnitDAO.java | 771 |
| 9 | HIGH | IDOR — getImpactByUnitId() no tenant scope | UnitDAO.java | 817 |
| 10 | HIGH | IDOR — getChecklistSettings() no tenant scope | UnitDAO.java | 843 |
| 11 | HIGH | IDOR — updateChecklistSettings() no tenant scope | UnitDAO.java | 888 |
| 12 | HIGH | IDOR — saveUnitAccessInfo() no tenant scope (access credentials) | UnitDAO.java | 513 |
| 13 | HIGH | IDOR — deleteAssignment() no tenant scope | UnitDAO.java | 78 |
| 14 | HIGH | IDOR — isAssignmentOverlapping() no tenant scope | UnitDAO.java | 91 |
| 15 | HIGH | ORDER BY injection via unsanitised orderBy param — UnitsByCompanyIdQuery | UnitsByCompanyIdQuery.java | 34 |
| 16 | MEDIUM | Singleton broken DCL — non-volatile theInstance | UnitDAO.java | 24 |
| 17 | MEDIUM | Exception swallowing — cause chain stripped on rethrow (12 methods) | UnitDAO.java | multiple |
| 18 | MEDIUM | SELECT * from v_units — overly broad exposure | UnitsByIdQuery.java | 14 |
| 19 | MEDIUM | getUnitBySerial() no comp_id filter — cross-tenant serial lookup | UnitDAO.java | 212 |
| 20 | MEDIUM | UnitManufactureFilterHandler — fieldName injected without whitelist | UnitManufactureFilterHandler.java | 18 |
| 21 | LOW | StringContainingFilterHandler — fieldNames injected without whitelist | StringContainingFilterHandler.java | 21,25 |
| 22 | LOW | UnitFuelTypeBean — missing equals/hashCode, serialisation risk | UnitFuelTypeBean.java | 5 |
| 23 | LOW | getUnitMaxId() — race condition + cross-tenant ID disclosure | UnitDAO.java | 264 |
| 24 | INFO | Legacy raw-Statement pattern in 10 methods — tech debt inventory | UnitDAO.java | multiple |
| 25 | INFO | ResultSet.TYPE_SCROLL_SENSITIVE used for forward-only iteration | UnitDAO.java | multiple |

---

**CRITICAL: 7 / HIGH: 8 / MEDIUM: 5 / LOW: 3 / INFO: 2**
