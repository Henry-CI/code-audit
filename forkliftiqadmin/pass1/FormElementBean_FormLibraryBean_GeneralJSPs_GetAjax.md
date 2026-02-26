# Security Audit Report
## Files: FormElementBean.java, FormLibraryBean.java, driver/general.jsp, users/general.jsp, getAjax.jsp
**Application:** forkliftiqadmin (pandoraAdmin) — Apache Struts 1.3.10 / Tomcat
**Audit date:** 2026-02-26
**Pass:** 1

---

## Scope

| # | File |
|---|------|
| 1 | `src/main/java/com/bean/FormElementBean.java` |
| 2 | `src/main/java/com/bean/FormLibraryBean.java` |
| 3 | `src/main/webapp/html-jsp/driver/general.jsp` |
| 4 | `src/main/webapp/html-jsp/users/general.jsp` |
| 5 | `src/main/webapp/html-jsp/getAjax.jsp` |

Supporting files read as context: `AdminDriverAddAction.java`, `AdminDriverEditAction.java`, `AdminDriverAddForm.java`, `AdminDriverEditForm.java`, `DriverBean.java`, `DriverDAO.java`, `UnitDAO.java`, `GPSDao.java`, `QuestionDAO.java`.

---

## Findings

---

### CRITICAL: Insecure Java deserialization in FormLibraryBean

**File:** `FormLibraryBean.java` (lines 69–84)

**Description:**
`FormLibraryBean.setForm_content(byte[])` feeds a raw byte array read from the database directly into `ObjectInputStream.readObject()` with no class filtering of any kind:

```java
public void setForm_content(byte[] convertObject) {
    this.form_object = getFormBuilderBean(convertObject);
}

public FormBuilderBean getFormBuilderBean(byte[] convertObject) {
    ByteArrayInputStream bais;
    ObjectInputStream ins;
    try {
        bais = new ByteArrayInputStream(convertObject);
        ins = new ObjectInputStream(bais);              // ← raw ObjectInputStream
        formBuilderBean = (FormBuilderBean) ins.readObject(); // ← unchecked
        ins.close();
    } catch (Exception e) {
        e.printStackTrace();
    }
    return formBuilderBean;
}
```

Java deserialization is exploited by feeding a gadget chain (Apache Commons Collections, Spring, etc.) into any `ObjectInputStream.readObject()` call. If an attacker can write to the column that stores this byte blob — via SQL injection in the same application, a compromised DB account, or a malicious admin — arbitrary code executes on the server inside the Tomcat JVM at the moment `setForm_content` is called.

Even without an attacker-controlled write path, the pattern itself is categorised CRITICAL under OWASP A08:2021 because the class graph reachable through Tomcat's classpath almost certainly contains a working gadget chain (Commons Collections 3.x/4.x are a common transitive dependency in legacy Struts stacks).

**Risk:** Remote Code Execution (RCE) within the Tomcat process. Full server compromise, data exfiltration, lateral movement.

**Recommendation:**
Replace `ObjectInputStream` with a filtering wrapper that uses `ObjectInputFilter` (Java 9+) or the `ValidatingObjectInputStream` from Apache Commons IO. Restrict deserializable classes to `FormBuilderBean` and `FormElementBean` only. Alternatively, replace the binary serialisation format with a structured format (JSON via Jackson, or XML with an explicit schema). Ensure the database column itself is protected so only trusted processes can write to it.

---

### CRITICAL: SQL injection in UnitDAO.getType() via manu_id (called by GetAjaxAction)

**File:** `UnitDAO.java` (lines 625–628), triggered via `GetAjaxAction.java` (line 31) and rendered by `getAjax.jsp`

**Description:**
`GetAjaxAction` reads `manu_id` directly from the HTTP request parameter and passes it to `UnitDAO.getType()`, which concatenates it unsanitised into a `Statement.executeQuery()` call:

```java
// GetAjaxAction.java line 26
String manu_id = request.getParameter("manu_id") == null ? "0" : request.getParameter("manu_id");
// ...
arrXml = unitDao.getType(manu_id);
```

```java
// UnitDAO.java lines 625-628
String sql = "select distinct(type.id),name from manu_type_fuel_rel"
    + " left outer join type on type.id = manu_type_fuel_rel.type_id "
    + " where manu_id = " + manu_id   // ← raw concatenation
    + " order by name";
stmt.executeQuery(sql);
```

A request such as `GET /getajax.do?action=getType&manu_id=0%3BUNION%20SELECT%20...` allows a second-order or direct injection. The endpoint is authenticated (session check applies) but any logged-in user of any tenant can exploit it.

**Risk:** Database read (data exfiltration across all companies), potentially blind or error-based injection for schema enumeration. Depending on DB privilege level, write or OS-level operations may be possible.

**Recommendation:** Replace with a `PreparedStatement`: `"... where manu_id = ?"` and `stmt.setLong(1, Long.parseLong(manu_id))`. Validate that `manu_id` is numeric before the DAO call. Apply the same fix to `UnitDAO.getPower()` (finding below).

---

### CRITICAL: SQL injection in UnitDAO.getPower() via manu_id and type_id (called by GetAjaxAction)

**File:** `UnitDAO.java` (lines 665–672), triggered via `GetAjaxAction.java` (line 36)

**Description:**
Both `manu_id` and `type_id` arrive from HTTP request parameters and are concatenated into a raw SQL string:

```java
// GetAjaxAction.java lines 35-36
String type_id = request.getParameter("type_id") == null ? "0" : request.getParameter("type_id");
arrXml = unitDao.getPower(manu_id, type_id);
```

```java
// UnitDAO.java lines 665-672
String sql = "select fuel_type.id,name from manu_type_fuel_rel"
    + " left outer join fuel_type on fuel_type.id = manu_type_fuel_rel.fuel_type_id "
    + " where manu_id = " + manu_id;            // ← injection point 1

if (!type_id.equalsIgnoreCase("")) {
    sql += " and type_id= " + type_id;          // ← injection point 2
}
```

This is identical in pattern and severity to the `getType` finding above; it simply doubles the injection surface.

**Risk:** Same as `getType` — database exfiltration, schema enumeration, potential write access.

**Recommendation:** Use `PreparedStatement` with `?` placeholders for both `manu_id` and `type_id`, with numeric validation on the action layer.

---

### CRITICAL: SQL injection in QuestionDAO.getQuestionContentById() via qus_id and lan_id (called by GetAjaxAction)

**File:** `QuestionDAO.java` (lines 327–331), triggered via `GetAjaxAction.java` (lines 40–43)

**Description:**
`GetAjaxAction` reads `qus_id` and `lan_id` from request parameters and passes them to `QuestionDAO.getQuestionContentById()`, which concatenates both directly into SQL strings executed via `Statement`:

```java
// GetAjaxAction.java lines 40-43
String qus_id = request.getParameter("qus_id") == null ? "0" : request.getParameter("qus_id");
String lan_id = request.getParameter("lan_id") == null ? "0" : request.getParameter("lan_id");
QuestionDAO questionDAO = new QuestionDAO();
arrXml = questionDAO.getQuestionContentById(qus_id, lan_id);
```

```java
// QuestionDAO.java lines 327-331
if (lanId.equalsIgnoreCase("1")) {
    sql = "select content from question where id = " + qId;          // ← injection
} else {
    sql = "select content from question_content where question_id = " + qId
        + " and lan_id = " + lanId;                                   // ← injection
}
```

Both branches are injectable. An attacker-supplied `qus_id` or `lan_id` of `0 UNION SELECT password FROM users--` would return credential data through the XML response rendered by `getAjax.jsp`.

**Risk:** Same database exfiltration severity as above. The response is directly reflected in the XML output — making it a read-anything-from-the-database vulnerability with no output encoding barrier.

**Recommendation:** Use `PreparedStatement` with `?` placeholders. Validate that both parameters are numeric integers before the DAO call.

---

### HIGH: IDOR — getDriverById() fetches driver records without tenant ownership check

**File:** `DriverDAO.java` (lines 154–157), called from `AdminDriverEditAction.java` (lines 56, 95, 131, 184) and `AdminDriverAddAction.java` (line 98)

**Description:**
`QUERY_DRIVER_BY_ID` retrieves a driver record using only the driver's primary key; it does not join on `comp_id`:

```java
private static final String QUERY_DRIVER_BY_ID =
    "select d.id, d.first_name, d.last_name, p.location, p.department, d.phone, p.enabled, d.email,'******' "
    + "from driver d "
    + "inner join permission p on d.id = p.driver_id "
    + "where d.id = ?";    // ← no comp_id filter
```

`AdminDriverEditAction` calls this method with the `id` submitted by the client in the form field (`adminDriverEditForm.getId()`), which maps to the `driverId` request parameter. Although `sessCompId` is read from the session and set on the `DriverBean` for the *update* operation, the subsequent `getDriverById` call used to re-populate the response view is unconstrained by tenant. A user from Company A can POST `id=<any_driver_id>` and receive back that driver's data.

Similarly, `AdminDriverEditAction` at line 56 calls `DriverDAO.getDriverById(driverId)` without validating that `driverId` belongs to `sessCompId`. The `UPDATE_GENERAL_INFO_SQL` itself also omits a `comp_id` predicate:

```sql
update driver set first_name = ?, last_name = ?, phone = ? where id = ?
```

This means Company A can overwrite the name and phone number of any driver owned by any other company.

**Risk:** Cross-tenant information disclosure (read PII for any driver in the database) and cross-tenant data tampering (overwrite driver records belonging to other companies). In a multi-tenant SaaS context this is a regulatory and contractual breach in addition to a technical vulnerability.

**Recommendation:** Add `AND p.comp_id = ?` to `QUERY_DRIVER_BY_ID` and bind `sessCompId`. Add `AND comp_id = ?` (bound to `sessCompId`) to `UPDATE_GENERAL_INFO_SQL`. Verify ownership before every operation that accepts a client-supplied entity ID.

---

### HIGH: IDOR — last_gps action accepts attacker-supplied compId instead of using session

**File:** `GetAjaxAction.java` (line 46)

**Description:**
For the `last_gps` action branch, the `compId` value is read directly from the HTTP request parameter rather than from the session attribute `sessCompId`:

```java
} else if (action.equals("last_gps")) {
    String[] unit = request.getParameterValues("unit");
    String compId = request.getParameter("compId") == null ? "0"
                  : request.getParameter("compId");   // ← attacker-controlled
    // ...
    request.setAttribute("arrGPSData", GPSDao.getUnitGPSData(compId, unit, ...));
}
```

Any authenticated user can supply an arbitrary `compId` and retrieve real-time GPS location data for vehicles belonging to a different company. This leaks physical location of assets to competitor tenants or hostile actors.

**Risk:** Cross-tenant disclosure of real-time GPS asset location data for the entire fleet of any company in the system.

**Recommendation:** Replace `request.getParameter("compId")` with `(String) session.getAttribute("sessCompId")`. Remove the ability for the client to influence tenant context.

---

### HIGH: Weak password hashing — MD5 used for driver PIN storage

**File:** `DriverDAO.java` (line 512), `driver/general.jsp` (line 205)

**Description:**
Driver PINs are hashed with the raw MD5 function built into PostgreSQL (`md5(?)`) before being stored:

```java
// DriverDAO.java line 511-512
stmt = conn.prepareStatement(
    "insert into driver(...,password) values (?,?,NULL,NULL,NULL,NULL,TRUE,?,?,md5(?)) RETURNING id");
```

On the client side, `driver/general.jsp` also hashes the PIN with `CryptoJS.MD5` before form submission:

```javascript
// driver/general.jsp line 205
var password = '' + CryptoJS.MD5($('input[name="pass"]').val());
$('input[name=pass_hash]').val(password);
```

MD5 is cryptographically broken for password storage. It is extremely fast and has no salt, making it trivially reversible via rainbow tables or GPU brute-force for short PINs (4–8 digits as enforced by the UI). A single-table dump yields cracked PINs in seconds. The client-side pre-hashing also reduces the effective entropy presented to the server.

**Risk:** Compromise of any database backup or SQL injection result instantly yields all driver PINs in crackable form. A 4-digit PIN hashed with MD5 can be reversed in under one millisecond using a lookup table.

**Recommendation:** Replace PostgreSQL `md5(?)` with `crypt(?, gen_salt('bf', 12))` (pgcrypto bcrypt) or perform hashing server-side with BCrypt / PBKDF2 / Argon2 (min cost factor appropriate for a PIN). Remove client-side pre-hashing entirely; it provides no security benefit and reduces server-side control.

---

### HIGH: Cleartext password transmitted to and stored via Cognito registration path

**File:** `AdminDriverAddAction.java` (lines 51–58, 88–91)

**Description:**
When creating a web-portal user (`add_general_user` op_code), the plaintext password from the form field is passed directly into both the Cognito sign-up request and the local `UserBean`:

```java
// AdminDriverAddAction.java lines 51-58
UserSignUpRequest signUpRequest = UserSignUpRequest.builder()
    .username(adminDriverAddForm.getEmail_addr())
    .password(adminDriverAddForm.getPass())   // ← raw form value
    // ...
    .build();

// lines 87-91
UserBean userBean = UserBean.builder()
    .email(adminDriverAddForm.getEmail_addr())
    .password(adminDriverAddForm.getPass())   // ← raw form value stored locally
    .build();
compDao.saveUsers(Integer.parseInt(sessCompId), userBean);
```

The raw password is stored in the `users` table without any hashing (`saveUsers` inserts `userBean.getPassword()` as-is). This means a database breach exposes all user-account passwords in plaintext.

**Risk:** Full credential compromise for all web-portal user accounts. Enables credential-stuffing attacks because many users reuse passwords across services.

**Recommendation:** Never store the raw password. Hash with BCrypt before persisting locally. The Cognito SDK requires the plaintext for the sign-up API call, but the local database copy should be either omitted entirely (if Cognito is the sole auth provider) or stored as a properly salted hash.

---

### HIGH: Reflected XSS — unescaped `driverId` emitted into HTML attributes and JavaScript in driver/general.jsp

**File:** `src/main/webapp/html-jsp/driver/general.jsp` (lines 15–18, 43–46, 135–136, 256)

**Description:**
The `id` variable is read from the `driverId` request parameter with no sanitisation and emitted in multiple contexts:

**In anchor `href` attributes (lines 43–46):**
```jsp
<li class="active"><a class="triggerThis" href="<%=generalUrl%>">General</a></li>
<li><a href="<%=trainingUrl%>"><%=trainingtab %></a></li>
```
`generalUrl` is built as `"admindriver.do?action=edit&driverId=" + id` where `id` is the raw parameter value. A crafted `driverId` such as `"><script>alert(1)</script>` would break out of the `href` attribute.

**In a hidden form field `value` attribute (line 135):**
```jsp
<html:hidden property="id" value="<%=id %>" name="driver"/>
```
The Struts `<html:hidden>` tag does HTML-encode its `value` attribute, which mitigates this specific output point — but the href-based outputs above are unprotected.

**In an inline JavaScript string (line 256):**
```jsp
var actUrl = "<%=actionCode %>";
```
`actionCode` is set based on the `action` parameter: if `action` equals `"edit"` then `actionCode = "admindriveredit.do"` (a string literal), so this specific interpolation does not directly reflect user input. However, the pattern is dangerous boilerplate — if `actionCode` ever becomes user-influenced, this becomes a script-injection vector.

The primary exploitable path is the `href` emission of `id` on lines 43–45. If this JSP fragment is loaded via the AJAX modal triggered by a crafted link, the injected script executes in the admin's browser session.

**Risk:** Stored or reflected XSS in the driver management modal. Attacker can steal the admin's session cookie, perform actions as the admin (create/delete drivers, change passwords), or exfiltrate data.

**Recommendation:** HTML-encode all request parameters before emitting into HTML. Use `ESAPI.encoder().encodeForHTMLAttribute(id)` or `<%=StringEscapeUtils.escapeHtml(id)%>` for attribute contexts, and `ESAPI.encoder().encodeForJavaScript(id)` for JavaScript string contexts. Avoid scriptlet variable interpolation entirely; use JSTL `<c:url>` and `<c:out>` tags with the default `escapeXml="true"`.

---

### HIGH: Reflected XSS — unescaped `driverId` emitted into HTML attributes in users/general.jsp

**File:** `src/main/webapp/html-jsp/users/general.jsp` (lines 14–16, 33–34, 118–119, 206)

**Description:**
Identical pattern to the driver general JSP. The `id` parameter (bound to `driverId`) is read from the request and written unescaped into anchor `href` values and a hidden field:

```jsp
// lines 13-16
if (action.equalsIgnoreCase("edituser")) {
    generalUrl = "admindriver.do?action=edituser&driverId=" + id;
    subscriptionUrl = "admindriver.do?action=subscription&driverId=" + id;
}
// line 33
<li class="active"><a class="triggerThis" href="<%=generalUrl%>">General</a></li>
<li><a href="<%=subscriptionUrl%>">Notification</a></li>
// line 118
<html:hidden property="id" value="<%=id %>" name="driver"/>
```

The attack surface is the same: a crafted `driverId` value injected into the `href` attribute context.

**Risk:** Same as driver/general.jsp — XSS against admin users, session hijacking, privilege escalation within the application.

**Recommendation:** Same as driver/general.jsp — encode all request parameter emissions; prefer JSTL over scriptlets.

---

### HIGH: CSRF — no synchronizer token on state-changing driver and user forms

**File:** `src/main/webapp/html-jsp/driver/general.jsp` (line 48), `src/main/webapp/html-jsp/users/general.jsp` (line 38)

**Description:**
Both forms use Struts `<html:form>` with POST but neither includes a Struts synchronizer token (`saveToken` / `isTokenValid`). There is no evidence of any CSRF protection in the application (`struts-config.xml` contains no token-related configuration; no `<html:hidden property="org.apache.struts.taglib.html.TOKEN">` tag is present).

```jsp
<!-- driver/general.jsp line 48 -->
<html:form method="post" action="<%=actionCode %>"
           styleClass="ajax_mode_c driver_general_form"
           styleId="adminDriverUpdateGeneral">
    <!-- no token field -->
```

An attacker who can lure an authenticated admin to a malicious page can submit a forged POST to `admindriveredit.do` or `admindriveradd.do`, creating or modifying driver/user accounts including changing passwords. The AJAX submission mechanism (`setupConfirmationPopups`) does not add CSRF headers.

**Risk:** CSRF allowing account takeover of driver PIN accounts, creation of rogue admin-level user accounts, or modification of existing users' credentials — all with no interaction beyond the admin visiting a crafted URL.

**Recommendation:** Use Struts 1.x synchronizer tokens: call `saveToken(request)` in the Action that renders the form and `isTokenValid(request, true)` in the Action that processes the POST. Alternatively, add a `SameSite=Strict` or `SameSite=Lax` attribute to the session cookie to provide defence-in-depth against CSRF.

---

### HIGH: XML injection in getAjax.jsp — database values interpolated unescaped into XML response

**File:** `src/main/webapp/html-jsp/getAjax.jsp` (lines 19–21)

**Description:**
`getAjax.jsp` constructs an XML document by string concatenation, embedding database-sourced `id` and `name` values with no XML encoding:

```java
XmlBean xmlBean = (XmlBean) arrXml.get(i);
String id   = xmlBean.getId();
String name = xmlBean.getName();
resp = resp + "<rec><code>" + id + "</code><name>" + name + "</name></rec>";
```

If any `name` value in the database contains XML special characters (`<`, `>`, `&`, `"`, `'`) — e.g., a vehicle named `"Type A & B"` or a question with HTML content — the XML document is malformed. More critically, if an attacker can influence stored data (via SQL injection or a separate write endpoint), they can inject `</name></rec></body><script>…</script>` which the consuming JavaScript will parse as extra nodes, potentially executing code if the client uses `innerHTML` to render the result.

**Risk:** XML/HTML injection via stored data, potentially leading to stored XSS in the admin UI where the AJAX response is rendered. Document structure manipulation can break client-side parsing and lead to silent data corruption.

**Recommendation:** Escape all values before building the XML string using `StringEscapeUtils.escapeXml(value)` (Apache Commons Lang) or, preferably, build the XML document using the `javax.xml.parsers.DocumentBuilder` API and serialise it properly, which handles encoding automatically.

---

### MEDIUM: Credential leakage via Lombok @Data toString() in DriverBean

**File:** `src/main/java/com/bean/DriverBean.java` (line 9)

**Description:**
`DriverBean` is annotated with `@Data`, which causes Lombok to generate a `toString()` method that includes *all* fields — including `pass`, `cpass`, `pass_hash`, `accessToken`, and `cognito_username`:

```java
@Data
@NoArgsConstructor
public class DriverBean implements Serializable {
    // ...
    private String pass     = null;
    private String cpass    = null;
    private String pass_hash = null;
    private String cognito_username = null;
    private String accessToken = null;
```

`AdminDriverAddForm.getDriverBean()` explicitly logs the bean at DEBUG level:

```java
// AdminDriverAddForm.java line 80
log.debug("driverBean : " + driverBean);
```

If the logging level for `com.actionform` is set to DEBUG (common in development, staging, or when a developer enables verbose logging to diagnose a production issue), all password and token values will appear in plaintext in Tomcat log files. Log files are often shipped to centralised aggregation systems (Splunk, ELK) where many people have read access.

**Risk:** Credential and access-token leakage to log files, log aggregation systems, and anyone with log read access. Depending on log retention policy, historical passwords may be recoverable long after they are changed.

**Recommendation:** Remove `@Data` from `DriverBean` and replace it with `@Getter @Setter`. Implement a custom `toString()` that explicitly redacts sensitive fields: `"DriverBean[id=" + id + ", email=" + email_addr + ", pass=***REDACTED***]"`. Alternatively, annotate the sensitive fields with `@ToString.Exclude` if `@Data` must be retained.

---

### MEDIUM: SQL injection in DriverDAO — getDriverByName methods use string concatenation (developer-acknowledged FIXME)

**File:** `DriverDAO.java` (lines 226–228, 264), called internally from DAO methods

**Description:**
Two internal query methods build SQL by concatenating `firstName`, `lastName`, and `fullName` using `Statement` rather than `PreparedStatement`. The source code itself contains a developer-written comment acknowledging this:

```java
// DriverDAO.java line 225: FIXME Use string constant to avoid to re-instantiating new string at every call.
// Also work with prepared statement to prevent SQL injection.
String sql = "select id,first_name,last_name,active,comp_id from driver "
    + "where trim(both ' ' from first_name) ilike trim(both ' ' from '"
    + firstName + "')  "
    + " and trim(both ' ' from last_name) ilike trim(both ' ' from '"
    + lastName + "')"
    + " and comp_id = " + compId;
```

```java
// DriverDAO.java line 264
String sql = "select id,first_name,last_name,active,comp_id,licno from driver "
    + "where first_name||' '||last_name ilike '" + fullName + "' and comp_id = " + compId;
```

While these methods appear to be called with data from existing driver records rather than raw user input in the current call graph, the pattern is exploitable if the call paths are extended or if `firstName`/`lastName` values originate from a user-controlled source anywhere in the chain.

**Risk:** SQL injection if call paths reach user-controlled input. Data exfiltration, authentication bypass.

**Recommendation:** Replace with `PreparedStatement` using `ILIKE ?` and `stmt.setString()` as the developer's own FIXME comment requests.

---

### MEDIUM: SQL injection in QuestionDAO.getQuestionByUnitId() — lanId, unitId, compId, attchId concatenated

**File:** `QuestionDAO.java` (lines 82–90)

**Description:**
The `getQuestionByUnitId` method constructs a complex query concatenating four caller-supplied strings — `lanId`, `unitId`, `compId`, and `attchId` — using `Statement`:

```java
String sql = "select question.id,question.content,... from question"
    + " left outer join question_content on question_content.question_id = question.id and lan_id = " + lanId
    + " left outer join unit on unit.type_id = question.type_id"
    + " where unit.id = " + unitId
    + " and ... and (question.comp_id is null or question.comp_id = " + compId + ")";
if (attchId.equalsIgnoreCase("0")) {
    sql += " and attachment_id is null ";
} else {
    sql += " and (attachment_id is null or attachment_id = " + attchId + ")";
}
```

While `compId` in this invocation path appears to originate from a unit lookup (not directly from user input), `unitId` and `attchId` can come from user-supplied parameters elsewhere in the application.

**Risk:** SQL injection if any caller passes user-controlled input. Cross-tenant question data disclosure.

**Recommendation:** Rewrite using `PreparedStatement` with `?` for all four parameters.

---

### MEDIUM: SQL injection in UnitDAO.getUnitNameByComp() / getTotalUnitByID() via compLst

**File:** `UnitDAO.java` (lines 311, 548)

**Description:**
Both methods build SQL `IN (...)` clauses by concatenating `compLst`, which is derived from `compId` through `CompanyDAO.getSubCompanyLst()`. If `getSubCompanyLst()` returns a value that was not originally validated as a numeric CSV string, injection is possible:

```java
// UnitDAO.java line 311
String sql = "select id,name from unit where comp_id in (" + compLst + ")";

// UnitDAO.java line 548
String sql = "select count(id) from unit where comp_id in (" + compLst + ")";
```

**Risk:** Injection through an internal data source that may carry user-influenced values. The risk is lower than direct user-input injection but still a structural defect that can be exploited if upstream data is ever tainted.

**Recommendation:** Validate that `compLst` is a numeric-CSV string before interpolation, or restructure to use a parameterised query with `UNNEST` or a repeated `?` list.

---

### MEDIUM: SQL injection in UnitDAO.delUnitById() via id parameter

**File:** `UnitDAO.java` (lines 349–351)

**Description:**
The `delUnitById` method receives a `String id` and concatenates it without validation:

```java
String sql = "update unit set active = false where id=" + id;
stmt.executeUpdate(sql);
```

While the calling context is an admin action, the `id` originates from a request parameter that is not explicitly validated as numeric before reaching this method.

**Risk:** SQL injection leading to arbitrary UPDATE/SELECT execution if `id` is not constrained at the call site.

**Recommendation:** Use `PreparedStatement` with `stmt.setLong(1, Long.parseLong(id))`, and add numeric validation at the action layer.

---

### MEDIUM: SQL injection in GPSDao.getGPSLocations() via unitList array elements

**File:** `GPSDao.java` (lines 87–88)

**Description:**
The deprecated `getGPSLocations()` method (not the parameterised `getUnitGPSData()`) concatenates each element of a `unitList` string array into a SQL WHERE clause:

```java
String sql = "select u.id,u.name,g.longitude,g.latitude,g.gps_time,g.current_location from gps as g"
    + " inner join unit as u on u.id=g.unit_id"
    + " where g.unit_id=" + unitList[i]   // ← injection
    + " order by g.gps_time desc limit 1";
```

**Risk:** SQL injection if any caller passes user-controlled unit IDs. GPS location data exfiltration.

**Recommendation:** This method appears unused in the current codebase (`getUnitGPSData` is the active equivalent). Remove `getGPSLocations()` entirely, or if it must be retained, rewrite using `PreparedStatement`.

---

### MEDIUM: JSON injection in GPSDao.getUnitGPSData() — database values embedded in raw JSON string

**File:** `GPSDao.java` (lines 64–65)

**Description:**
GPS unit data from the database (vehicle name, manufacturer, type, power) is embedded directly into a hand-constructed JSON string without JSON encoding:

```java
String gps_str = "{\"name\":\"" + unitBean.getVehName() + "\",\"status\":1,\"lat\":"
    + unitBean.getLatitude() + ",\"lon\":" + unitBean.getLongitude()
    + ",\"manufacturer\":\"" + unitBean.getManufacturer() + "\","
    // ...
    + "\"type\":\"" + unitBean.getType() + "\",\"power\":\"" + unitBean.getPower() + "\","
    + "\"ingeofence\":false,\"distance\":\"\",\"classColor\":\"\"}";
```

If any database field contains a double-quote or backslash (e.g., a vehicle named `Ford "Type A"`), the JSON is malformed. If an attacker can control stored data, they can inject arbitrary JSON keys, overriding `ingeofence`, `distance`, `classColor`, or injecting XSS payloads that the client renders.

**Risk:** JSON/XSS injection via stored vehicle metadata. In the worst case, attacker-controlled vehicle names can influence client-side behaviour.

**Recommendation:** Use a JSON library (Jackson `ObjectMapper`, Gson) to serialise the bean to JSON rather than building strings manually.

---

### LOW: FormElementBean implements Serializable with a hardcoded serialVersionUID but no readObject() protection

**File:** `FormElementBean.java` (lines 6, 11)

**Description:**
`FormElementBean` implements `Serializable` and declares a fixed `serialVersionUID`. It is embedded inside `FormBuilderBean`, which is itself the target of the insecure `ObjectInputStream.readObject()` in `FormLibraryBean`. As part of the deserialisation gadget resolution, `FormElementBean` will also be deserialised. Although `FormElementBean` itself has no dangerous `readObject()` override, its presence in the serialisable class graph is a supporting factor for the `FormLibraryBean` critical finding.

**Risk:** Low in isolation; the risk is already captured in the CRITICAL `FormLibraryBean` finding. Noted here for completeness.

**Recommendation:** If the binary serialisation format is replaced (as recommended for `FormLibraryBean`), `FormElementBean` should have the `Serializable` interface removed as well. If serialisation is retained, add a `readObject()` method that calls `defaultReadObject()` followed by explicit field validation.

---

### LOW: Stack traces printed to standard error in DAO exception handlers

**File:** `UnitDAO.java` (multiple catch blocks, e.g. lines 226, 353), `GPSDao.java` (lines 108–112), `FormLibraryBean.java` (lines 61, 79), `QuestionDAO.java` (line 49)

**Description:**
Numerous `catch` blocks call `e.printStackTrace()` in addition to or instead of structured logging:

```java
// UnitDAO.java (representative)
} catch (Exception e) {
    InfoLogger.logException(log, e);
    e.printStackTrace();   // ← writes to stderr
    throw new SQLException(e.getMessage());
}
```

```java
// FormLibraryBean.java line 61
} catch (Exception e) {
    e.printStackTrace();   // ← only this, no logger
    return byteArrayObject;
}
```

Stack traces written to `System.err` may appear in Tomcat's `catalina.out`, which is often world-readable on misconfigured servers. Stack traces reveal internal class names, package structure, SQL fragments, and file paths that aid an attacker in reconnaissance.

**Risk:** Information disclosure aiding targeted attack development.

**Recommendation:** Remove all `e.printStackTrace()` calls. Route all exception logging through the application's `InfoLogger`/log4j logger using `log.error("message", e)`, which keeps stack traces in controlled log files at an appropriate level.

---

### LOW: Missing null-check on arrXml in getAjax.jsp may cause NullPointerException

**File:** `src/main/webapp/html-jsp/getAjax.jsp` (line 12)

**Description:**
The JSP casts the request attribute `arrXml` to `ArrayList` and immediately calls `.size()` without checking for null:

```java
ArrayList arrXml = (ArrayList) request.getAttribute("arrXml");
// ...
if (arrXml.size() > 0)   // ← NullPointerException if arrXml is null
```

If `GetAjaxAction` encounters an error before setting the `arrXml` attribute, or if the JSP is accessed without going through the Action (e.g., direct URL access), `arrXml` will be null and a 500 error with a stack trace will be returned to the browser.

**Risk:** Information disclosure via stack trace in error response; denial of service via repeated triggering.

**Recommendation:** Add a null check: `if (arrXml != null && arrXml.size() > 0)`. Ensure the Action always initialises `arrXml` to an empty `ArrayList` on all code paths before forwarding.

---

### INFO: Raw, unparameterised ArrayList usage in getAjax.jsp (unchecked cast)

**File:** `src/main/webapp/html-jsp/getAjax.jsp` (lines 8, 17)

**Description:**
The JSP uses a raw `ArrayList` type and performs an unchecked cast of each element to `XmlBean`:

```java
ArrayList arrXml = (ArrayList) request.getAttribute("arrXml");
// ...
XmlBean xmlBean = (XmlBean) arrXml.get(i);
```

This is a code-quality issue that also carries a minor security implication: if any non-`XmlBean` object is ever placed into the `arrXml` attribute by a different Action (e.g., following a refactor), the cast will throw a `ClassCastException` and expose a stack trace.

**Risk:** Code robustness defect; stack trace disclosure on ClassCastException.

**Recommendation:** Parameterise the list: `List<XmlBean> arrXml = (List<XmlBean>) request.getAttribute("arrXml");` and add the null check described above.

---

### INFO: Driver PIN masked in DB query result but not enforced server-side on password change

**File:** `DriverDAO.java` (line 154)

**Description:**
`QUERY_DRIVER_BY_ID` returns the literal string `'******'` for the password column to avoid exposing the stored hash to the application layer. The edit form then pre-populates the password field with this mask. The server-side validation in `AdminDriverEditForm.validate()` checks for `"******"` and blanks out the hash if submitted unchanged:

```java
// AdminDriverEditForm.java lines 80-85
if (pass.equalsIgnoreCase("******")) {
    this.pass = "";
    this.cpass = "";
    this.pass_hash = "";
}
```

This is a reasonable approach, but the sentinel value `"******"` is client-controlled; there is no server-side indicator distinguishing a legitimate "do not change" submission from an attacker who simply submits the literal string `"******"` to prevent a password update when they want to. The current logic happens to work correctly because submitting `"******"` results in an empty hash, which `updateGeneralInfo` does not write. However, this depends on the `StringUtils.isNotBlank` guard downstream, making it fragile.

**Risk:** Informational; the current implementation is not exploitable in the obvious direction, but the approach is fragile and warrants explicit documentation or a cleaner design.

**Recommendation:** Use a dedicated boolean/flag (`changePassword=true/false`) rather than a magic sentinel string to signal intent. Document the contract between form and DAO explicitly.

---

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 4 |
| HIGH     | 7 |
| MEDIUM   | 6 |
| LOW      | 3 |
| INFO     | 2 |

**CRITICAL: 4 / HIGH: 7 / MEDIUM: 6 / LOW: 3 / INFO: 2**

---

## Priority Remediation Order

1. **FormLibraryBean deserialization (CRITICAL)** — Replace `ObjectInputStream` with a class-filtered alternative or migrate to a structured format. Exploitable by anyone who can write to the form-content DB column.
2. **SQL injection in UnitDAO.getType / getPower / QuestionDAO.getQuestionContentById (CRITICAL x3)** — All are reachable by any authenticated user via `getajax.do`. Switch to `PreparedStatement` immediately.
3. **IDOR on getDriverById / last_gps (HIGH)** — Cross-tenant data leakage and write; bind all queries to `sessCompId`.
4. **CSRF on driver and user forms (HIGH)** — Add Struts synchronizer tokens.
5. **MD5 PIN hashing / cleartext password storage (HIGH x2)** — Migrate to BCrypt; remove plaintext local password copy.
6. **XSS in both general.jsp files (HIGH x2)** — Encode all request-parameter emissions.
7. **XML injection in getAjax.jsp (HIGH)** — Escape output using an XML library.
8. **Remaining MEDIUM SQL injections** — Systematic PreparedStatement migration across DriverDAO, QuestionDAO, UnitDAO, GPSDao.
9. **DriverBean @Data credential leakage (MEDIUM)** — Add `@ToString.Exclude` or implement custom `toString()`.
