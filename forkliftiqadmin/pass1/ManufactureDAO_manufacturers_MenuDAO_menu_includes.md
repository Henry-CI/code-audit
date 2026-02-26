# Security Audit Report — ManufactureDAO / Manufacturers UI / MenuDAO / Menu Includes

**Date:** 2026-02-26
**Auditor:** Automated Pass 1
**Branch:** master
**Scope:** ManufactureBean, ManufactureDAO, manufacturers.jsp, manufacturersList.jsp, ManuTypeFuleRelBean, menu.inc.jsp, MenuBean, MenuDAO, menu_loginInfo.inc.jsp, menu_popup.inc.jsp, menu_print.inc.jsp, menu_register.inc.jsp, menu_systemadmin.inc.jsp

---

## Findings

---

### CRITICAL: SQL Injection — `getManufactureById` uses Statement + string concatenation

**File:** `src/main/java/com/dao/ManufactureDAO.java` (line 72)

**Description:**
The method `getManufactureById(String id)` constructs a SQL query by direct string concatenation of the caller-supplied `id` parameter without any validation or parameterisation:

```java
String sql = "select id,name from manufacture where id = " + id;
log.info(sql);
rs = stmt.executeQuery(sql);
```

The `id` value originates from HTTP request parameters (via the action form). An attacker can supply a payload such as `1 OR 1=1` or a UNION-based string to read arbitrary data from the database, or a stacked-query payload against permissive JDBC drivers to execute arbitrary SQL. The raw SQL is also written to the application log, leaking the injected string.

**Risk:** Full database read/write/delete depending on the DB user's privileges. Cross-tenant data disclosure (all manufacturer records). Potential remote code execution if the database account has FILE or xp_cmdshell privileges.

**Recommendation:** Replace `Statement` with `PreparedStatement` and bind `id` as a typed parameter, as already done in `delManufacturById`:
```java
String sql = "select id,name from manufacture where id = ?";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setInt(1, Integer.parseInt(id));
```
Validate that `id` is a non-negative integer before passing it to the DAO.

---

### CRITICAL: SQL Injection — `checkManuByNm` inlines `name` and `id` via string concatenation

**File:** `src/main/java/com/dao/ManufactureDAO.java` (lines 149–152)

**Description:**
The method `checkManuByNm(String name, String id)` embeds the unsanitised `name` parameter directly in a SQL string literal, and appends the unsanitised `id` without quoting:

```java
String sql = "select id from manufacture where name = '" + name + "'";
if (!id.equalsIgnoreCase("")) {
    sql += " and id !=" + id;
}
rs = stmt.executeQuery(sql);
```

The `name` field is a user-supplied text value from the manufacturer name input. An attacker can close the string literal and inject arbitrary SQL: `' OR '1'='1` will bypass the existence check; `'; DROP TABLE manufacture; --` could be destructive on compatible DB drivers.

The `id` concatenation (no quotes, no cast) also allows numeric injection (`1 OR 1=1`) without needing to escape a string delimiter.

**Risk:** Authentication/authorization bypass for the duplicate-name guard; arbitrary data read; potential data destruction.

**Recommendation:** Use `PreparedStatement` with `?` placeholders for both `name` and `id`:
```java
String sql = "select id from manufacture where name = ?";
// conditionally add: " and id != ?"
PreparedStatement ps = conn.prepareStatement(sql);
ps.setString(1, name);
// ps.setInt(2, Integer.parseInt(id));
```

---

### CRITICAL: SQL Injection — `getManu_type_fuel_rel` inlines `manuId` via string concatenation

**File:** `src/main/java/com/dao/ManufactureDAO.java` (line 263)

**Description:**
The method `getManu_type_fuel_rel(String manuId)` appends the caller-supplied `manuId` directly into a multi-table JOIN query:

```java
String sql = " select manu_type_fuel_rel.id,manufacture.name,type.name,fuel_type.name from manu_type_fuel_rel " +
        " left outer join type on type.id = type_id " +
        " left outer join fuel_type on fuel_type.id = fuel_type_id " +
        " left outer join manufacture on manufacture.id = manu_id " +
        " where manu_id = " + manuId;
```

This is a numeric injection point. As with `getManufactureById`, an attacker supplying a non-numeric `manuId` can enumerate all manufacturer-type-fuel relationships across all tenants, or inject subqueries to exfiltrate other tables.

**Risk:** Cross-tenant enumeration of all manu/type/fuel relationships. Data exfiltration via UNION injection.

**Recommendation:** Use `PreparedStatement`:
```java
String sql = "... where manu_id = ?";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setInt(1, Integer.parseInt(manuId));
```

---

### CRITICAL: SQL Injection — `MenuDAO.getAllMenu` inlines `lanCode` in WHERE clause

**File:** `src/main/java/com/dao/MenuDAO.java` (lines 34–36)

**Description:**
`getAllMenu(String lanCode)` builds the query using direct string concatenation of the `lanCode` parameter, which is likely sourced from a cookie, session attribute, or user preference:

```java
String sql = "select menus.id,menus.name,description,icon,action from menus,menu_content,language" +
             " where menus.id = menu_content.menu_id and lan_id = language.id and lan_code = '"+lanCode+"'"+
             " order by id";
```

An attacker who can influence `lanCode` (e.g., by modifying a cookie or session value, or if it flows from a request parameter) can inject arbitrary SQL via the unquoted string literal.

**Risk:** Exfiltration of menu configuration data; potential for broader database reads if UNION-based injection is possible.

**Recommendation:** Parameterise with `PreparedStatement`:
```java
String sql = "select menus.id,menus.name,description,icon,action " +
             "from menus,menu_content,language " +
             "where menus.id = menu_content.menu_id and lan_id = language.id and lan_code = ? " +
             "order by id";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setString(1, lanCode);
```
Additionally validate `lanCode` against an allowlist of known language codes before calling the DAO.

---

### CRITICAL: SQL Injection — `MenuDAO.getRoleMenu` inlines `lanCode` and unsanitised role array

**File:** `src/main/java/com/dao/MenuDAO.java` (lines 79–82)

**Description:**
`getRoleMenu(ArrayList<String> arrRole, String lanCode)` inlines both the `lanCode` string literal and the output of `Util.ArraListToString(arrRole)` (a comma-separated string built from role IDs held in session) directly into the query:

```java
String sql = "select distinct(menus.id),menus.name,menu_content.description,icon,action from menus,role_menu_rel,language,menu_content" +
     " where menus.id = role_menu_rel.menu_id and role_id in("+Util.ArraListToString(arrRole)+") and language.id = menu_content.lan_id and menu_content.menu_id = menus.id " +
     " and language.lan_code = '"+lanCode+"'"+
     " order by id";
```

Although `arrRole` is drawn from session, if any upstream code allows those values to be set from user input (e.g., during login processing or a preference endpoint), injecting through the IN-list is trivially possible. The `lanCode` injection vector is identical to `getAllMenu`.

**Risk:** Privilege escalation (an attacker adding synthetic role IDs to the IN list could reveal menus for other roles); cross-tenant information disclosure; general SQL injection.

**Recommendation:** Use a `PreparedStatement` with individual `?` for each role ID and one `?` for `lanCode`. Validate each role ID is a non-negative integer before building the list. Alternatively, use a server-side allowlist of valid role IDs for the authenticated user.

---

### CRITICAL: SQL Injection — `MenuDAO.saveRoleMenu` inlines `roleId` and `menuId`

**File:** `src/main/java/com/dao/MenuDAO.java` (line 124)

**Description:**
`saveRoleMenu(String roleId, String menuId)` performs an INSERT using raw string concatenation for both IDs:

```java
String sql = "insert into role_menu_rel (role_id,menu_id) values ("+roleId+","+menuId+")";
stmt.executeUpdate(sql);
```

Both parameters are injected directly. A numeric injection (`1),(2),(3` etc.) could insert arbitrary rows into `role_menu_rel`, escalating privileges by assigning elevated menus to roles.

**Risk:** Privilege escalation; arbitrary row insertion into the role-menu mapping table.

**Recommendation:** Use `PreparedStatement` with `setInt` for both parameters after validating they are valid positive integers.

---

### CRITICAL: SQL Injection — `MenuDAO.delRoleMenu` inlines `roleId`

**File:** `src/main/java/com/dao/MenuDAO.java` (line 151)

**Description:**
`delRoleMenu(String roleId)` performs a DELETE using raw string concatenation:

```java
String sql = "delete from role_menu_rel where role_id ="+roleId;
stmt.executeUpdate(sql);
```

An attacker supplying `roleId = "1 OR 1=1"` would delete all rows from `role_menu_rel`, removing menu access for every user. A subquery injection could target arbitrary roles.

**Risk:** Denial of service (removal of all role-menu mappings); targeted privilege removal.

**Recommendation:** Use `PreparedStatement` with `setInt` after integer validation.

---

### HIGH: IDOR — `updateManufacturer` does not verify ownership by `company_id`

**File:** `src/main/java/com/dao/ManufactureDAO.java` (lines 210–244) and `src/main/java/com/action/AdminManufacturersAction.java` (lines 33–39)

**Description:**
`updateManufacturer(ManufactureBean manufactureBean)` updates a manufacturer record using only the manufacturer's primary key (`id`). The session's `sessCompId` is not included in the WHERE clause:

```java
String sql = "update manufacture set name = ?  where id = ?";
// ...
ps.setString(1, manufactureBean.getName());
ps.setInt(2, Integer.parseInt(manufactureBean.getId()));
```

The action class (`AdminManufacturersAction`, line 35–37) sets only `id` and `name` on the bean from the request; `company_id` is not set and is therefore null. Any authenticated user from any company who knows (or guesses) the numeric `id` of a manufacturer belonging to a different company can rename it. Manufacturer IDs are sequential integers, trivially enumerable.

**Risk:** Cross-tenant data tampering. A tenant can corrupt manufacturer names for all other tenants, including global (system) manufacturers (those with `company_id IS NULL`).

**Recommendation:** Add `AND company_id = ?` to the UPDATE statement and bind `sessCompId` as the third parameter. For the special case of global manufacturers (company_id IS NULL), updates should be restricted to a super-admin role with a separate code path:
```java
String sql = "update manufacture set name = ? where id = ? and company_id = ?";
ps.setString(1, manufactureBean.getName());
ps.setInt(2, Integer.parseInt(manufactureBean.getId()));
ps.setInt(3, Integer.parseInt(sessCompId));
```

---

### HIGH: IDOR — `delManufacturById` does not verify ownership by `company_id`

**File:** `src/main/java/com/dao/ManufactureDAO.java` (lines 99–135) and `src/main/java/com/action/AdminManufacturersAction.java` (lines 40–43)

**Description:**
`delManufacturById(String id)` deletes rows from `manu_type_fuel_rel` and `manufacture` using only the primary key, with no tenant check:

```java
String sql = "delete from manu_type_fuel_rel where manu_id = ?";
// ...
String sql = "delete from manufacture where id = ?";
```

The calling action passes `adminManufacturersActionForm.getManufacturerId()` directly from the HTTP request to the DAO without verifying that the manufacturer belongs to the authenticated tenant. An attacker can delete any manufacturer record, including global ones, across all tenants.

**Risk:** Cross-tenant data destruction. A malicious tenant can wipe manufacturers used by other companies, potentially disrupting fleet check configuration across the platform.

**Recommendation:** Add an ownership check before deletion. Either:
1. Add a `company_id = ?` guard to the DELETE statement; or
2. Query the manufacturer's `company_id` first and return a 403 if it does not match `sessCompId`.

---

### HIGH: IDOR — `isVehicleAssignedToManufacturer` leaks cross-tenant boolean

**File:** `src/main/java/com/dao/ManufactureDAO.java` (lines 404–432) and `src/main/java/com/action/AdminManufacturersAction.java` (lines 44–47)

**Description:**
`isVehicleAssignedToManufacturer(String manufacturerId)` queries the `unit` table for any active vehicle assigned to the given manufacturer ID, with no tenant filter:

```java
private static final String QUERY_VEHICLE_BY_MANUFACTURE_SQL =
    "select count(*) from unit where manu_id = ? and active is TRUE";
```

The action returns a JSON boolean to the client (`{value: true/false}`). An attacker who enumerates manufacturer IDs can determine whether any vehicle across any tenant is assigned to a given manufacturer, leaking fleet inventory information about other companies.

**Risk:** Cross-tenant information disclosure: reveals whether a manufacturer is in use by any company on the platform.

**Recommendation:** Join the `unit` table against the company's own vehicles:
```sql
select count(*) from unit where manu_id = ? and active is TRUE and comp_id = ?
```
Bind `sessCompId` as the second parameter.

---

### HIGH: XSS — `manufacturers.jsp` injects unescaped manufacturer `name` and `id` into HTML and JavaScript via `<bean:write>` (no `filter="true"`) and scriptlet expressions

**File:** `src/main/webapp/html-jsp/settings/manufacturers.jsp` (lines 51–70, 144–175)

**Description:**
Multiple instances of `<bean:write>` and JSP scriptlet expressions render data-bound values without HTML or JavaScript encoding:

1. **Lines 51–52:** The `id` and `name` properties of each `ManufactureBean` are written into an HTML `id` attribute and element content without escaping. `<bean:write>` in Struts 1 HTML-encodes by default only when `filter` is unspecified — however, the default behaviour of `filter` in Struts 1 `bean:write` is `true`, but the `id` is placed inside a JavaScript function call on lines 60, 65, 70 (see below), not just HTML content.

2. **Lines 54–55 and 59–70:** JSP scriptlets `<%= manufacturer.getName() %>` and `<%= manufacturer.getId() %>` are used to set HTML attribute values and inline JavaScript arguments with no escaping whatsoever:

```jsp
<input type="text" style="display:none;" class="form-control" value="<%= manufacturer.getName() %>"
       id="manufacturer-edit-<%= manufacturer.getId() %>" class="manufacturer" />
...
onclick="edit_manufacturer(<bean:write property="id" name="manufacturer"/>)">
onclick="save_manufacturer(<bean:write property="id" name="manufacturer"/>)">
onclick="delete_manufacturer(<bean:write property="id" name="manufacturer"/>)">
```

   - `manufacturer.getName()` is rendered unescaped into an HTML attribute value. A manufacturer name containing `"` or `>` breaks attribute context and enables stored XSS.
   - `manufacturer.getId()` (a database integer) is lower risk for injection but is still placed directly into JavaScript event handlers. If `id` were ever a non-integer (e.g., due to a data integrity issue), this would be exploitable.

3. **Lines 151–174 (JavaScript `prepareTable` function):** The AJAX refresh path writes server JSON fields directly into innerHTML without any sanitisation:

```javascript
html += '<tr><td><div id="manufacturer-name-' + elem.id + '">' + elem.name + '</div>'
      + ' <input type="text" style="display:none;" id="manufacturer-edit-' + elem.id + '" value="' + elem.name + '" /></td><td>';
```

`elem.name` is inserted directly into `innerHTML`. A manufacturer name stored as `<img src=x onerror=alert(1)>` will execute JavaScript in every user's browser that triggers an AJAX table refresh. This is a persistent (stored) XSS vector.

**Risk:** Stored XSS. An attacker with access to the "add manufacturer" function (or who exploits the SQL injection to insert directly) can store a malicious name and achieve script execution in the context of every admin user who views the Manufacturers settings page. Given that `manufacturers.jsp` is loaded in a modal that is part of the main admin layout, impact is scoped to authenticated admin users.

**Recommendation:**
- Replace all `<%= manufacturer.getName() %>` with `${fn:escapeXml(manufacturer.name)}` (requires JSTL `fn` taglib).
- Replace raw `innerHTML` assignment in `prepareTable` with DOM manipulation using `document.createTextNode()` or use a templating library that escapes by default.
- For the `onclick` integer argument, validate that `id` is a positive integer on the server before returning it to the client.

---

### HIGH: XSS — `menu.inc.jsp` renders `sessCompName` and company names via `<bean:write>` without `filter="true"` in an HTML attribute context

**File:** `src/main/webapp/includes/menu.inc.jsp` (lines 19, 31–36, 41)

**Description:**
The main menu include (rendered on every authenticated page) outputs company and session data:

1. **Line 19:** `<bean:write name="sessCompName"/>` — outputs the company name from session into HTML content. `<bean:write>` defaults to `filter="true"` in Struts 1, which converts `<`, `>`, `"`, `&` to HTML entities. This specific instance is lower risk for HTML content injection, but see finding on JavaScript context below.

2. **Lines 31–36:** Inside the company-switcher `<select>`, option values and text are rendered:
```jsp
<option value="<bean:write name="company" property="id"/>">
    <bean:write name="company" property="name"/>
</option>
```
`<bean:write>` in an HTML attribute value context (inside `value="..."`) with its default `filter="true"` will encode `<` and `>` but will also encode `"` as `&quot;`, which is correct for attribute context. However, the option text output is unquoted in the attribute value of the wrapping element — this is generally safe for HTML content but requires verification that `filter="true"` is genuinely the default for this version of Struts (1.3.10 confirms this is the case).

3. **Line 41 — JavaScript context (CRITICAL XSS vector):**
```jsp
$('select[name="currentCompany"]').val('<%= session.getAttribute("sessCompId") %>');
```
`sessCompId` is a session attribute (a database integer) written directly into a JavaScript string literal using a JSP scriptlet without any JavaScript encoding. While `sessCompId` is expected to be a numeric string, if it were ever tampered with (e.g., set to `'; alert(document.cookie);//`) this would execute immediately. More importantly, this pattern — a scriptlet embedding a session attribute in JS — sets a dangerous precedent and is one session attribute mutation away from persistent script execution on every page.

**Risk:** The `sessCompId` JavaScript injection would execute on every page the authenticated user visits. Even though `sessCompId` is a server-side session value (not directly user-supplied at runtime), defence in depth requires all session data to be escaped when emitted into JavaScript string contexts. An attacker who can corrupt the session (e.g., via a deserialization or session fixation attack) would achieve trivial persistent XSS across all pages.

**Recommendation:**
- Replace the scriptlet on line 41 with properly escaped output. Since `sessCompId` should be numeric, validate it is a digit-only string and use `Integer.parseInt` before storing in session. In the JSP, output it without quotes or use `fn:escapeXml`.
- Audit all other `<bean:write>` usages to confirm `filter="true"` is active; explicitly add `filter="true"` as an attribute to document intent.

---

### HIGH: XSS — `menu_loginInfo.inc.jsp` renders driver name and company name via unescaped `<bean:write>` in an older menu layout

**File:** `src/main/webapp/includes/menu_loginInfo.inc.jsp` (lines 33, 41)

**Description:**
This include (used in a legacy page layout) renders the company name and driver names from session-backed lists directly into HTML:

```jsp
<bean:write property="name" name="compRecord"></bean:write>
...
<bean:write property="first_name" name="driverRecord"></bean:write>
<bean:write property="last_name" name="driverRecord"></bean:write>
```

`<bean:write>` without an explicit `filter` attribute relies on the Struts default of `true`, which performs HTML entity encoding. However, this default is not explicitly stated and has been a source of confusion in legacy Struts code. If any calling code sets `filter="false"` or if the taglib version differs, the company name and driver name would be rendered as raw HTML.

More critically, company names and driver names are user-supplied data entered by administrators. A stored XSS payload (e.g., a company named `<script>...`) would be rendered on every page for every user in that company. Because this file is included in every authenticated page of the legacy layout, the blast radius is the entire authenticated user population of the affected company.

**Risk:** Stored XSS on every authenticated page for all users belonging to a company whose name contains an HTML/script payload. Impact is amplified by the universal inclusion of this file.

**Recommendation:** Explicitly add `filter="true"` to all `<bean:write>` tags in this file. For new development, migrate to JSTL `${fn:escapeXml(...)}`. Validate and sanitise company names and driver names at the point of entry (save/update) to reject HTML special characters.

---

### HIGH: XSS — `menu_systemadmin.inc.jsp` renders `MenuBean.description` and `MenuBean.action` from database via `<bean:write>` into HTML attribute and content without explicit escaping

**File:** `src/main/webapp/includes/menu_systemadmin.inc.jsp` (line 40)

**Description:**
The system-admin menu include iterates over `sessMenu` (a list of `MenuBean` objects loaded from the database) and renders menu item descriptions and action strings directly:

```jsp
<li><a href="adminmenu.do?action=<bean:write property="action" name="menuRecord" />">
    <bean:write property="description" name="menuRecord" />
</a></li>
```

Two issues:
1. The `action` property is placed inside an HTML attribute value (`href="adminmenu.do?action=..."`). While `<bean:write>` encodes HTML entities by default, URL-special characters (e.g., `&`, `?`, `#`, spaces) are not URL-encoded. A menu `action` value containing `" onclick="alert(1)` would break out of the attribute context if HTML encoding were ever disabled.
2. The `description` property is rendered into HTML text content — again relying silently on the Struts default rather than an explicit `filter="true"`.

Both `action` and `description` are stored in the `menus` / `menu_content` database tables. If an attacker can insert records into those tables (e.g., via the SQL injection in `MenuDAO.saveRoleMenu`), they can inject stored XSS into the navigation menu of the system-admin layout, which is included on every admin page.

**Risk:** Stored XSS via database-driven menu content, amplified by the universal inclusion of this file. Exploitable in combination with the `saveRoleMenu` SQL injection finding.

**Recommendation:** Add explicit `filter="true"` to both `<bean:write>` tags. For the `href` attribute, additionally URL-encode the `action` value. Restrict write access to the `menus` and `menu_content` tables to privileged super-admin operations only.

---

### HIGH: XSS — `menu_systemadmin.inc.jsp` renders `EntityBean.name` unescaped

**File:** `src/main/webapp/includes/menu_systemadmin.inc.jsp` (line 53)

**Description:**
The entity (top-level organisation) name is rendered into the menu bar:

```jsp
<bean:write property="name" name="entityRecord"></bean:write>
```

Without an explicit `filter="true"`, this relies on Struts default behaviour. Entity names are admin-controlled data that would be rendered on every page in this layout. See the pattern described in the `menu_loginInfo.inc.jsp` finding.

**Risk:** Stored XSS on every page if entity name contains script payload.

**Recommendation:** Add `filter="true"` explicitly.

---

### MEDIUM: CSRF — `manufacturers.do` mutating actions lack CSRF tokens

**File:** `src/main/webapp/html-jsp/settings/manufacturers.jsp` (lines 95, 114, 130)

**Description:**
All state-changing operations (add, edit, delete manufacturer) are performed via jQuery `$.post` and `$.get` AJAX calls without any CSRF token:

```javascript
$.post('manufacturers.do', {action:'add', manufacturer:manufacturerName})
$.post('manufacturers.do', {action:'edit', manufacturer:manufacturerName, manufacturerId: id})
$.post('manufacturers.do', {action:'delete', manufacturerId: id})
```

The application uses Struts 1 which has no built-in CSRF protection. There is no evidence of a synchroniser token or `SameSite` cookie attribute in the codebase. A malicious page open in a separate tab can trigger cross-origin POST requests (the browser sends session cookies automatically with simple CORS requests for `application/x-www-form-urlencoded` content type, which these jQuery posts use by default).

**Risk:** An attacker can trick an authenticated admin into visiting a crafted page that deletes or renames all manufacturers for their company. Combined with the IDOR findings, a cross-tenant delete could be executed.

**Recommendation:**
- Implement the Synchroniser Token Pattern: generate a per-session CSRF token, store it in the session, embed it in all forms and AJAX requests, and validate it in the action handler.
- Set `SameSite=Strict` or `SameSite=Lax` on the session cookie to provide defence in depth.

---

### MEDIUM: CSRF — `menu_loginInfo.inc.jsp` logout form has no CSRF token

**File:** `src/main/webapp/includes/menu_loginInfo.inc.jsp` (line 46)

**Description:**
The logout form submits via POST to `logout.do` without a CSRF token:

```jsp
<form method="post" action="logout.do" name="logoutform" style='margin:0'>
<span class="logintitle"><a href="#" onclick="document.logoutform.submit();"></span>
```

An attacker can force a logout of any authenticated user via a CSRF attack (login CSRF / logout CSRF). While logout CSRF is lower severity than action CSRF, it can be used as part of a session fixation chain.

**Risk:** Forced logout of authenticated users; potential enablement of session fixation.

**Recommendation:** Add a CSRF synchroniser token to the logout form.

---

### MEDIUM: Stored XSS in AJAX Table Refresh — `manufacturers.jsp` `prepareTable` function writes JSON data into `innerHTML`

**File:** `src/main/webapp/html-jsp/settings/manufacturers.jsp` (lines 151–152)

**Description:**
This is elaborated further from the XSS finding above to separately record the AJAX-specific attack surface. When an add/edit/delete action succeeds, the server returns a JSON array of manufacturer objects and `prepareTable()` rebuilds the table DOM by setting `table.html(html)`:

```javascript
html += '<tr><td><div id="manufacturer-name-' + elem.id + '">' + elem.name + '</div>'
      + ' <input type="text" style="display:none;" id="manufacturer-edit-' + elem.id
      + '" value="' + elem.name + '" /></td><td>';
```

`elem.name` is used both as HTML content and as an HTML attribute value with no encoding. Even if the initial page load were protected, every AJAX refresh re-introduces the XSS. This means that even if the server-side add/save validated input on the way in, any future relaxation (or bypass via SQL injection) would immediately expose XSS.

**Risk:** Persistent stored XSS triggered on every manufacturer table refresh.

**Recommendation:** Use a DOM-safe method:
```javascript
var nameNode = document.createTextNode(elem.name);
var div = document.createElement('div');
div.appendChild(nameNode);
```
Or use a template library such as Mustache.js that HTML-encodes by default.

---

### MEDIUM: Information Disclosure — SQL queries logged at INFO level with user-supplied input

**File:** `src/main/java/com/dao/ManufactureDAO.java` (lines 73, 264) and `src/main/java/com/dao/MenuDAO.java` (lines 37, 84, 125, 152)

**Description:**
Raw SQL strings (including any injected content) are logged at INFO level immediately before execution:

```java
// ManufactureDAO.java line 73
String sql = "select id,name from manufacture where id = " + id;
log.info(sql);

// MenuDAO.java line 125
String sql = "insert into role_menu_rel (role_id,menu_id) values ("+roleId+","+menuId+")";
log.info(sql);
```

If an attacker injects a payload into a parameter, the full injected SQL string is written to the application log. Log files may be accessible to developers, operations staff, or via log management systems with broader access than the database. In addition, logging SQL statements at INFO level in production means routine query patterns (including multi-tenant `company_id` values) are visible in log files.

**Risk:** Injection payloads written to logs can facilitate forensic evasion awareness (attacker knows what was logged); logs with `company_id` values leak tenant enumeration data to log readers.

**Recommendation:** Remove `log.info(sql)` calls for queries that include user-supplied values, or move them to DEBUG level (disabled in production). Use parameterised queries so that no user data ever appears in the SQL string itself. Log query names/method names instead of full SQL.

---

### MEDIUM: Exception Message Forwarding — `SQLException` wraps and re-throws raw exception message

**File:** `src/main/java/com/dao/ManufactureDAO.java` (lines 53–54, 83–84) and `src/main/java/com/dao/MenuDAO.java` (lines 55, 101, 130, 159)

**Description:**
In all DAO methods, caught exceptions are wrapped and re-thrown as new `SQLException` objects, passing the original exception's message string directly:

```java
} catch (Exception e) {
    InfoLogger.logException(log, e);
    e.printStackTrace();
    throw new SQLException(e.getMessage());
}
```

If the calling action class allows this exception to propagate to the Struts framework's default error handler, the raw database error message (which may include table names, column names, SQL fragments, or JDBC driver details) could be rendered in the HTTP response or in a default Tomcat error page. This is especially dangerous in combination with the SQL injection findings, where a crafted query error message could confirm the injection point.

**Risk:** Database schema disclosure; JDBC driver version disclosure; confirmation of SQL injection success to an attacker.

**Recommendation:** Catch exceptions at the action layer and return a generic error message to the client. Log the full exception server-side only. Do not forward raw `e.getMessage()` to the presentation tier.

---

### MEDIUM: `ManufactureBean` annotated with Lombok `@Data` — `toString()` includes `company_id`

**File:** `src/main/java/com/bean/ManufactureBean.java` (lines 9, 14–16)

**Description:**
`ManufactureBean` is annotated with `@Data`, which generates `toString()` that includes all fields:

```java
@Data
@NoArgsConstructor
public class ManufactureBean implements Serializable {
    private String id         = null;
    private String name       = null;
    private String company_id = null;
    ...
}
```

Lombok's generated `toString()` will produce output such as: `ManufactureBean(id=42, name=Acme Forklifts, company_id=17)`. If `ManufactureBean` instances are logged anywhere (e.g., via `log.info("Manufacturer: " + manufacture)` in the action class or if the JSON serialiser calls `toString()`), the `company_id` of all tenants is included. In this multi-tenant application, `company_id` is a tenant discriminator and leaking it facilitates IDOR attacks (finding the IDs of other tenants).

The `company_id` field does not hold a credential but does hold a security-significant enumeration value.

**Risk:** Tenant ID enumeration via log files or debug output; facilitates cross-tenant IDOR.

**Recommendation:** Add `@ToString(exclude = "company_id")` to the class annotation, or replace `@Data` with `@Getter @Setter @EqualsAndHashCode` without `@ToString`. Review all call sites where `ManufactureBean` might be passed to a logger.

---

### LOW: `menu_popup.inc.jsp` is an empty file

**File:** `src/main/webapp/includes/menu_popup.inc.jsp` (0 bytes)

**Description:**
The file exists but contains no content (0 bytes as confirmed by `wc -c`). It is referenced as a menu include. An empty include is not a vulnerability in itself, but its presence may indicate that popup/modal functionality was removed without updating the include directive, or it was never fully implemented. Dead includes create maintenance confusion.

**Risk:** Low — potential confusion during future development; no immediate security impact.

**Recommendation:** Either remove the file and all `<%@ include file="menu_popup.inc.jsp" %>` directives, or document its intentionally empty state with a comment.

---

### LOW: `menu_print.inc.jsp` uses a malformed `<body>` tag (duplicate `<body>`)

**File:** `src/main/webapp/includes/menu_print.inc.jsp` (line 5)

**Description:**
The file contains:
```jsp
<body onload="print('document');window.close();"><body>
```

There are two `<body>` opening tags and no `</body>` closing tag. This is a structural HTML defect. While browsers are permissive, malformed HTML can cause unexpected rendering behaviour and may defeat certain XSS filters or WAF rules that rely on well-formed DOM structure.

**Risk:** Minor — malformed HTML; no direct security impact but indicates low code quality in security-sensitive includes.

**Recommendation:** Fix the duplicate `<body>` tag.

---

### LOW: Stray `</form>` tag in `menu_loginInfo.inc.jsp`

**File:** `src/main/webapp/includes/menu_loginInfo.inc.jsp` (line 52)

**Description:**
Line 52 contains a bare `</form>` closing tag:
```jsp
                </form>
```
There is no matching `<form>` opening tag in this file (the form opened on line 46 is `<form method="post" action="logout.do" ...>` which has its own close). This orphaned `</form>` tag can cause the browser to prematurely close a form element in the surrounding page context, potentially preventing form submissions from reaching the server or breaking CSRF token binding for forms that include this fragment.

**Risk:** Functional defect that could prevent form data (including CSRF tokens if added) from being submitted correctly; low direct security impact but may complicate CSRF remediation.

**Recommendation:** Remove the orphaned `</form>` on line 52 after verifying it does not close a form opened in a parent include.

---

### INFO: `ManuTypeFuleRelBean` has no Lombok annotations — manual boilerplate, low risk

**File:** `src/main/java/com/bean/ManuTypeFuleRelBean.java`

**Description:**
`ManuTypeFuleRelBean` uses manually written getters and setters (no Lombok annotations) and has no `toString()` override. This means there is no risk of credential or security-sensitive field leakage via an auto-generated `toString()`. The manual approach is safer in this context but creates maintenance overhead.

**Risk:** None for `toString()` leakage. No security findings on this file.

**Recommendation:** No immediate action required. Consider adding `@ToString(exclude={"manu_id"})` if Lombok is adopted for consistency, to prevent implicit logging of the tenant-linked `manu_id`.

---

### INFO: `MenuBean` has no Lombok annotations — no `toString()` leakage risk

**File:** `src/main/java/com/bean/MenuBean.java`

**Description:**
`MenuBean` is a plain Java bean with manual getters/setters and no `toString()`. Fields include `id`, `name`, `description`, `icon`, `action` — none of which are credentials. No security findings on this file.

**Risk:** None.

**Recommendation:** No action required.

---

### INFO: External URLs in HTML comments/help text use plain HTTP

**File:** `src/main/webapp/includes/menu.inc.jsp` (lines 116–117) and other menu includes

**Description:**
The help modal in `menu.inc.jsp` contains a link to `http://forklift-iq360.kayako.com/` using plain HTTP. If this URL is followed by users, the connection is not encrypted and is susceptible to MITM. Additionally, all `<area>` elements in menu includes reference `http://www.prestart.com.au` and `http://www.collectiveintelligence.com.au` over HTTP.

**Risk:** Low — man-in-the-middle risk for users who click those links; mixed-content warnings in modern browsers.

**Recommendation:** Update all external links to use HTTPS.

---

## Summary

| # | Severity | Title | File |
|---|----------|-------|------|
| 1 | CRITICAL | SQL Injection — `getManufactureById` | ManufactureDAO.java:72 |
| 2 | CRITICAL | SQL Injection — `checkManuByNm` | ManufactureDAO.java:149–152 |
| 3 | CRITICAL | SQL Injection — `getManu_type_fuel_rel` | ManufactureDAO.java:263 |
| 4 | CRITICAL | SQL Injection — `MenuDAO.getAllMenu` | MenuDAO.java:34–36 |
| 5 | CRITICAL | SQL Injection — `MenuDAO.getRoleMenu` | MenuDAO.java:79–82 |
| 6 | CRITICAL | SQL Injection — `MenuDAO.saveRoleMenu` | MenuDAO.java:124 |
| 7 | CRITICAL | SQL Injection — `MenuDAO.delRoleMenu` | MenuDAO.java:151 |
| 8 | HIGH | IDOR — `updateManufacturer` missing `company_id` guard | ManufactureDAO.java:210–244 |
| 9 | HIGH | IDOR — `delManufacturById` missing `company_id` guard | ManufactureDAO.java:99–135 |
| 10 | HIGH | IDOR — `isVehicleAssignedToManufacturer` no tenant filter | ManufactureDAO.java:404–432 |
| 11 | HIGH | Stored XSS — `manufacturers.jsp` unescaped name/id in HTML+JS | manufacturers.jsp:51–70 |
| 12 | HIGH | XSS — `menu.inc.jsp` `sessCompId` injected into JS string literal | menu.inc.jsp:41 |
| 13 | HIGH | XSS — `menu_loginInfo.inc.jsp` unescaped company/driver names | menu_loginInfo.inc.jsp:33,41 |
| 14 | HIGH | XSS — `menu_systemadmin.inc.jsp` unescaped menu `description`/`action` | menu_systemadmin.inc.jsp:40 |
| 15 | HIGH | XSS — `menu_systemadmin.inc.jsp` unescaped entity name | menu_systemadmin.inc.jsp:53 |
| 16 | MEDIUM | CSRF — `manufacturers.do` mutating actions no token | manufacturers.jsp:95,114,130 |
| 17 | MEDIUM | CSRF — logout form no token | menu_loginInfo.inc.jsp:46 |
| 18 | MEDIUM | Stored XSS — AJAX `prepareTable` writes to `innerHTML` | manufacturers.jsp:151–152 |
| 19 | MEDIUM | Info Disclosure — SQL logged at INFO with user-supplied input | ManufactureDAO.java:73,264 / MenuDAO.java:37,84,125,152 |
| 20 | MEDIUM | Exception message forwarding leaks DB schema | ManufactureDAO.java / MenuDAO.java (all catch blocks) |
| 21 | MEDIUM | Lombok `@Data` `toString()` includes `company_id` | ManufactureBean.java:9 |
| 22 | LOW | Empty file `menu_popup.inc.jsp` | menu_popup.inc.jsp |
| 23 | LOW | Malformed duplicate `<body>` tag | menu_print.inc.jsp:5 |
| 24 | LOW | Stray `</form>` tag | menu_loginInfo.inc.jsp:52 |
| 25 | INFO | `ManuTypeFuleRelBean` manual bean, no leakage risk | ManuTypeFuleRelBean.java |
| 26 | INFO | `MenuBean` manual bean, no leakage risk | MenuBean.java |
| 27 | INFO | External help/banner links use plain HTTP | menu.inc.jsp:116–117, menu includes |

---

CRITICAL: 7 / HIGH: 8 / MEDIUM: 6 / LOW: 3 / INFO: 3
