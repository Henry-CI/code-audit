# Pass 4 -- Code Quality Audit: `security` Package

**Auditor:** A18
**Date:** 2026-02-25
**Branch:** `release/UAT_RELEASE_FLEETFOCUS_Production`
**Package:** `WEB-INF/src/com/torrent/surat/fms6/security/`

---

## Files Audited

| # | File | Approx. Lines | Extends |
|---|------|--------------|---------|
| 1 | `Databean_security.java` | ~600 | (plain class) |
| 2 | `Frm_customer.java` | ~9,000+ | `HttpServlet` |
| 3 | `Frm_login.java` | 161 | `HttpServlet` |
| 4 | `Frm_security.java` | ~4,100+ | `HttpServlet` |
| 5 | `Frm_vehicle.java` | ~16,000+ | `HttpServlet` |
| 6 | `GetGenericData.java` | 94 | `HttpServlet` |

---

## 1. God Classes

| File | Severity | Evidence |
|------|----------|----------|
| **Frm_vehicle.java** | **CRITICAL** | Approximately 16,000+ lines in a single servlet class. Contains 30+ methods handling vehicle editing, deletion, hiring/de-hiring, checklist management, sync operations, broadcast, reboot, firmware management, spare swap, network settings, RTLS settings, and access rights templates. This is an extreme god class that violates the Single Responsibility Principle. |
| **Frm_customer.java** | **CRITICAL** | Approximately 9,000+ lines. Handles customer/location/department queries, driver listing, weigand card calculations, user management, and supervisory master operations. Far too many responsibilities in one class. |
| **Frm_security.java** | **HIGH** | Approximately 4,100+ lines. Handles login authentication, password management, form/module CRUD, mail group management, email configuration, subscriptions, dashboard subscriptions, notification settings, and access rights. Multiple distinct domains combined. |
| **Databean_security.java** | **MEDIUM** | ~600 lines acting as a combined data-access bean for forms, modules, mail groups, mail configuration, permissions, and monthly report subscriptions -- too many concerns for one data bean. |

---

## 2. Naming Conventions

| Finding | Severity | Files | Evidence |
|---------|----------|-------|----------|
| Snake-case class names | **MEDIUM** | All `Frm_*`, `Databean_security`, `GetGenericData` | Java convention requires PascalCase (`FrmSecurity`, `DatabeanSecurity`). Every class in this package violates this. |
| Snake-case method names | **MEDIUM** | All files | Examples: `save_form()`, `chk_login()`, `del_mail_lst()`, `mail_group_add()`, `save_idle_timer()`, `dehire_vehicle()`, `Query_Customer_Relations()`, `Fetch_mail_conf_rpt()`. Java convention requires camelCase. |
| Mixed naming styles | **LOW** | `Frm_customer.java` | Some methods use PascalCase (`Query_Customer_Relations`, `Fetch_cust_dept_grp`) while others use snake_case -- inconsistent within the same file. |
| Abbreviated / cryptic variable names | **LOW** | All files | Variables such as `set_op_code`, `set_gp_cd`, `vdep_cd`, `vdep_nm`, `fnm`, `lnm`, `tm`, `sno`, `gmtp`, `fssx`, `fsss_multi` reduce readability. |
| Raw-type `ArrayList` (no generics) | **MEDIUM** | `Databean_security.java`, `Frm_customer.java`, `Frm_vehicle.java` | 215 occurrences of `new ArrayList()` without type parameters across these files. Example: `ArrayList VCustomers_Id = new ArrayList();` (Frm_customer.java:108). |

---

## 3. Thread Safety (Servlet Instance Variables)

| File | Severity | Evidence |
|------|----------|----------|
| **Frm_vehicle.java** | **CRITICAL** | Mutable instance fields on a servlet: `private Connection dbcon;`, `private Statement stmt;`, `private ResultSet rset;`, `private Statement stmt1;`, `private ResultSet rset1;`, `private String message;`, `private String queryString;` (lines 59-66). Servlets are shared across concurrent requests. Multiple threads will overwrite these fields simultaneously, causing race conditions, corrupted queries, and data leaks between requests. The commented-out `SingleThreadModel` (line 55) suggests this was once mitigated but the mitigation was removed without refactoring to local variables. |
| **Frm_customer.java** | **CRITICAL** | Same pattern: `private Connection dbcon;`, `private String queryString;`, `private Statement stmt;`, `private ResultSet rset;`, `private Statement stmt1;`, `private ResultSet rset1;`, `private String message;`, `private String debug;` (lines 49-57). Also mutable string instance fields: `String VSite_Name`, `String S_Access_level`, `String S_Access_cust`, `String S_Access_site`, `String S_Access_dept` (lines 59-63). Commented-out `SingleThreadModel` at line 46. |
| **GetGenericData.java** | **HIGH** | Instance fields: `String url`, `String message`, `Statement stmt`, `ResultSet rset`, `Connection dbcon`, `String queryString` (lines 21-26). Same thread-safety hazard. |
| **Databean_security.java** | **HIGH** | Instance fields: `Connection conn`, `Statement stmt/stmt1/stmt2`, `ResultSet rset/rset1/rset2`, `HttpServletRequest request`, plus 20+ mutable String fields (lines 24-66). Not a servlet itself, but if shared or stored in session scope, the same concurrency issues apply. |
| **Frm_security.java** | **LOW** | Uses local variables for Connection/Statement/ResultSet in most methods. Instance field `DecimalFormat df` (line 53) is the only concern, and `DecimalFormat` is not thread-safe. |
| **Frm_login.java** | **NONE** | All JDBC resources declared as local variables inside `doPost()`. Correct pattern. |

---

## 4. Commented-Out Code

| File | Severity | Evidence |
|------|----------|----------|
| **Frm_security.java** | **HIGH** | 34 lines of commented-out code statements. Includes: commented-out `SingleThreadModel` declaration (line 46), commented-out `@SuppressWarnings("deprecation")` (line 45), large blocks of commented-out permission-loading logic (lines 1039-1048, 1143-1166), commented-out `System.out.println` debug statements throughout. The `new_login()` method (line 922) is annotated `@SuppressWarnings("unused")` indicating it may be dead code entirely. |
| **Frm_vehicle.java** | **HIGH** | 135 lines of commented-out code. Includes: commented-out `SingleThreadModel` (line 55), `@SuppressWarnings("deprecation")` (line 54), `//res.getWriter().println(queryString);` debug lines (line 230), commented-out query strings and variable declarations throughout sync methods. |
| **Frm_customer.java** | **HIGH** | 189 lines of commented-out code. Includes: commented-out `SingleThreadModel` (line 46), many commented-out `System.out.println` debug lines, commented-out SQL query blocks (e.g., lines 750-760, 820-830 area). |
| **Databean_security.java** | **LOW** | 5 lines of commented-out code, including `//System.out.println` debug statements. |
| **GetGenericData.java** | **LOW** | `// TODO Auto-generated constructor stub` placeholder at line 29. |

---

## 5. Unused Imports

| File | Severity | Evidence |
|------|----------|----------|
| **Frm_security.java** | **LOW** | `import java.util.Date;` (line 12) -- no usage of `Date` found in the class. `import javax.mail.Session;` (line 16) -- mail session is obtained through JNDI, not directly instantiated with this import in current code paths. `import com.torrent.surat.fms6.bean.UserBean` (line 35) -- not referenced. |
| **Frm_vehicle.java** | **LOW** | `import java.io.OutputStream;` (line 8), `import java.io.OutputStreamWriter;` (line 9), `import java.io.Writer;` (line 10) -- at least some of these are likely unused. `import java.util.List;` (line 24) -- only `ArrayList` is used directly. `import java.util.Map;` potentially unused in some code paths. |
| **Frm_customer.java** | **LOW** | `import java.io.PrintWriter;` (line 6), `import java.util.Set;` (line 18), `import java.util.HashSet;` (line 15) -- may be unused depending on the full file content. |

---

## 6. Empty Catch Blocks

| File | Line(s) | Severity | Evidence |
|------|---------|----------|----------|
| **Frm_security.java** | 2397-2399 | **HIGH** | `catch (Exception e) { } finally{` -- completely empty catch block, exception silently swallowed with no logging. |
| **Frm_security.java** | 3571-3573 | **HIGH** | `catch (SQLException e) { }` -- empty catch block. |
| **Frm_security.java** | 3631-3633 | **HIGH** | `catch (SQLException e) { }` -- empty catch block. |
| **Frm_security.java** | 3689-3691 | **HIGH** | `catch (SQLException e) { }` -- empty catch block. |
| **Frm_vehicle.java** | 15349-15350 | **HIGH** | `catch (Exception e) { }` -- empty catch block. |
| **Frm_vehicle.java** | 15356-15357 | **HIGH** | `catch (Exception e) { }` -- empty catch block. |
| **Frm_vehicle.java** | 15363-15364 | **HIGH** | `catch (Exception e) { }` -- empty catch block. |

Total: **7 empty catch blocks** across 2 files.

---

## 7. Broad `catch (Exception e)` Usage

| File | Count | Severity | Evidence |
|------|-------|----------|----------|
| **Frm_security.java** | 37 | **HIGH** | Nearly every method catches `Exception` rather than specific types (`SQLException`, `IOException`, `MessagingException`). This masks the true failure mode and makes debugging difficult. |
| **Frm_vehicle.java** | 33 | **HIGH** | Same pattern. All methods in the dispatch chain catch generic `Exception`. |
| **Frm_customer.java** | 13 | **HIGH** | Broad catches in most methods. |
| **GetGenericData.java** | 2 | **MEDIUM** | `doGet()` catches `Exception` at lines 38-39 and 60-61. |
| **Databean_security.java** | 1 | **LOW** | One broad catch. |
| **Frm_login.java** | 1 | **MEDIUM** | `doPost()` line 110 catches `Exception`. |

Total: **87 broad catch blocks** across 6 files.

---

## 8. `e.printStackTrace()` Usage

| File | Count | Severity | Evidence |
|------|-------|----------|----------|
| **Frm_vehicle.java** | 44 | **HIGH** | `e.printStackTrace()` used in virtually every catch block. Output goes to `System.err` (Tomcat catalina.out), not the application log. Interleaved with `System.out.println` logging. |
| **Frm_security.java** | 31 | **HIGH** | Same pattern throughout all methods. |
| **Frm_customer.java** | 15 | **HIGH** | Same pattern. |
| **GetGenericData.java** | 2 | **MEDIUM** | Lines 39, 61. |
| **Frm_login.java** | 1 | **MEDIUM** | Line 112. |

Total: **93 occurrences** across 5 files.

---

## 9. `System.out.println` Usage

| File | Count | Severity | Evidence |
|------|-------|----------|----------|
| **Frm_customer.java** | 133 | **HIGH** | Extensive use of `System.out.println` for error messages and debug output, despite having a `log4j` Logger available. |
| **Frm_vehicle.java** | 98 | **HIGH** | Same anti-pattern. Example: `System.out.println("Frm_vehicle-->: "+e);` (many occurrences). |
| **Frm_security.java** | 94 | **HIGH** | Example: `System.out.println("Frm_security-->: " + e);` repeated in every method's catch block. Also: `System.out.println("rset is not close " + e);` in every finally block. |
| **Databean_security.java** | 11 | **MEDIUM** | `System.out.println` in catch blocks despite no logger being used at all. |
| **Frm_login.java** | 4 | **MEDIUM** | `System.out.println("Frm_security-->: " + e);` (line 111 -- note the misleading class name in the message), plus 3 close-error messages. |
| **GetGenericData.java** | 2 | **LOW** | Lines 46, 54. |

Total: **342 occurrences** across 6 files. All files have `log4j` Logger available (except `GetGenericData` and `Databean_security` which lack a logger entirely).

---

## 10. Inconsistent Error Handling

| Finding | Severity | Evidence |
|---------|----------|----------|
| Mixed logging strategies | **HIGH** | The same catch block often uses both `e.printStackTrace()` AND `System.out.println()` AND sometimes `log.info()`. Three different output channels for the same error. Example in Frm_security.java line 138-139: `e.printStackTrace(); System.out.println("In the Frm_security...." + e);` |
| Error messages leak to clients | **HIGH** | Frm_vehicle.java line 190: `message = "{ \"status\":\"error\", \"message\":\"" + e + "\" }";` -- the raw exception `toString()` is sent to the client, leaking internal information. |
| Misleading error origin | **MEDIUM** | Frm_login.java line 111: `System.out.println("Frm_security-->: " + e);` -- error message says "Frm_security" but the code is in `Frm_login`. Copy-paste error. |
| Inconsistent JSON vs redirect | **MEDIUM** | Within Frm_security.java, some methods respond with JSON (`res.getWriter().println(message)`), others with `res.sendRedirect(url)`, and the error handling style differs between them. No consistent error response contract. |
| `@SuppressWarnings("resource")` | **MEDIUM** | Frm_security.java line 1390: suppresses resource leak warnings on `chk_login()` instead of fixing the leak. |

---

## 11. Resource Leaks

| File | Severity | Evidence |
|------|----------|----------|
| **Frm_vehicle.java** | **CRITICAL** | Connection, Statement, and ResultSet are instance fields (lines 59-65). They are opened in `doPost()` at lines 91, 97-98 and closed in the finally block (lines 191-231). However, if an individual method (e.g., `edit()`, `locker()`, `broadcast()`) throws an exception that is caught inside the method but does not re-throw, the finally block may close resources that sub-methods have already partially consumed, or sub-methods may open additional statements without closing them. |
| **Frm_customer.java** | **CRITICAL** | Same instance-field pattern. `PreparedStatement` objects created in methods like `edit()` are never explicitly closed -- they rely on the connection close to cascade. |
| **Frm_security.java** | **HIGH** | `PreparedStatement ps` declared at line 951 of `new_login()` is never closed in the finally block. The finally block only closes `rset`, `stmt`, and `dbcon`. Multiple `ps = dbcon.prepareStatement()` calls create new PreparedStatements without closing the previous one. |
| **GetGenericData.java** | **HIGH** | `getWeigand()` method (line 67) creates a query using instance field `stmt` but the incomplete SQL (`where` with no condition) would cause an error; the ResultSet from this method is never explicitly closed as the method has no finally block. |
| **Databean_security.java** | **HIGH** | Connection obtained via `getDataConnection()` stored in instance field `conn`. Multiple methods use `stmt`, `stmt1`, `stmt2`, `rset`, `rset1`, `rset2` as instance fields. If any method fails partway through, earlier ResultSets and Statements are never closed. No try-with-resources or consistent finally blocks in data-fetch methods. |
| **Frm_login.java** | **LOW** | Properly closes resources in finally block (lines 116-139). The only issue is that `closeConnection()` could itself throw, which is handled. Correct pattern in this file. |

---

## 12. Code Duplication

| Pattern | Severity | Files | Evidence |
|---------|----------|-------|----------|
| Resource cleanup boilerplate | **HIGH** | All servlet files | The exact same 20-line try-catch-finally pattern for closing `rset`, `stmt`, `dbcon` is repeated in every single method: `if (rset != null) { try { rset.close(); } catch (SQLException e) { System.out.println("rset is not close " + e); } }` etc. This appears 30+ times across Frm_security.java alone. |
| `CreateConnection()` / `closeConnection()` | **HIGH** | `Frm_login.java`, `Frm_security.java`, `GetGenericData.java` | The identical `CreateConnection()` static method is copy-pasted into 3 different files (Frm_login lines 144-155, Frm_security lines 147-157, GetGenericData lines 75-85). Same for `closeConnection()`. |
| Parameter null-check pattern | **MEDIUM** | All servlet files | `req.getParameter("x") == null ? "" : req.getParameter("x")` is repeated hundreds of times. Should be extracted to a utility method. |
| Customer/Location/Department dropdown JSON building | **HIGH** | `Frm_customer.java` | The pattern of iterating over ArrayLists to build JSON strings like `customer_result = customer_result + " { \"id\" : \"" + VCustomers_Id.get(i) + "\", ...` is repeated verbatim in at least 10 different `if/else if` branches in the `doGet()` method (lines 129-999). Massive copy-paste duplication. |
| `new_login()` vs `chk_login()` | **HIGH** | `Frm_security.java` | `new_login()` (line 922, annotated `@SuppressWarnings("unused")`) and `chk_login()` (line 1391) are two login implementations with substantially duplicated permission-loading logic. `reloadPermissions()` (line 1244) duplicates this same logic a third time. |
| `mcdrivers` / `smdrivers` / `mcdriversveh` / `mcdriversTab` | **HIGH** | `Frm_customer.java` | Four nearly identical methods (lines ~730-970) that query drivers with only minor differences in the WHERE clause. |
| `getClassURL()` and `getLoc_cd()` | **MEDIUM** | `Databean_security.java`, `Frm_security.java` | Both methods are duplicated identically between these two files (Databean_security lines 457-489, Frm_security lines 4010-4045). |

---

## 13. Dead Code

| File | Severity | Evidence |
|------|----------|----------|
| **Frm_security.java** | **HIGH** | `new_login()` method (line 922) is annotated `@SuppressWarnings("unused")` -- explicitly marked as unused. ~320 lines of dead code. |
| **Frm_security.java** | **MEDIUM** | `clearVectors()` (line 143) is called from `doPost()` but has an empty body `{ }`. It does nothing. |
| **Frm_vehicle.java** | **LOW** | `clearVectors()` (line 14976) -- present but not called from `doPost()` in this file. |
| **GetGenericData.java** | **HIGH** | `getWeigand()` method (line 67) is a private method never called from `doGet()` or anywhere else. It also contains an incomplete SQL query (`where` with no condition). The entire class appears to do nothing useful -- `doGet()` opens a connection, does nothing with it, then closes it. |
| **GetGenericData.java** | **HIGH** | The constructor (line 28) contains only `// TODO Auto-generated constructor stub` -- auto-generated placeholder. |
| **Frm_security.java** | **LOW** | `rrsubscribe()` (line 399) queries an email address, stores it in a local variable `mail_id` that is never used, then returns a hardcoded error JSON. Appears to be stub/incomplete code. |
| **Frm_customer.java** | **LOW** | Variable `debug` (line 57) is declared as an instance field but never appears to be used. |

---

## 14. Layering Violations (Security Logic Mixed with Presentation)

| Finding | Severity | Evidence |
|---------|----------|----------|
| Servlets build JSON manually | **HIGH** | Throughout all Frm_* files, JSON responses are built via string concatenation: `message = "{ \"status\":\"success\", \"message\":\"...\" }";`. No JSON library (despite Gson being imported in Frm_vehicle.java). This mixes presentation formatting with business logic. |
| SQL queries embedded in servlets | **CRITICAL** | All 6 files contain raw SQL strings directly in servlet methods. There is no DAO/repository layer separation. Frm_vehicle.java alone contains hundreds of SQL queries embedded in UI-controller methods. |
| Security logic in presentation layer | **HIGH** | `Frm_security.java` `chk_login()` (line 1391) contains authentication logic, password hashing (BCrypt), account lockout logic, session management, access-level determination, permission loading, privacy policy acceptance, and release note handling -- all in a single servlet method spanning ~650 lines. |
| HTML/URL construction in servlet | **MEDIUM** | `Frm_security.java` builds redirect URLs with query parameters: `url = "../security/frm_add_form.jsp?message=" + message + "&form_cd=" + form_cd;` -- mixing navigation/routing with business logic. |
| Weigand card calculation in servlet | **HIGH** | `Frm_customer.java` contains 7+ private methods for card-to-weigand conversion (`card_to_weigand_iclass_even`, `card_to_weigand_iclass_odd`, `card_to_weigand_smart_even`, `card_to_weigand_seos`, `card_to_hidiclass`, `card_to_weigand_chubb`, `card_to_weigand_au`, `card_to_weigand`) -- business logic that belongs in a service/utility class, not a servlet. |
| Password logging | **CRITICAL** | `Frm_login.java` line 97-99: `log.info("login failed: login:" + login + " password:" + password + " database password:" + pass_word + ...);` -- logs both the user-entered password AND the database password in cleartext. `Frm_security.java` line 66 logs passwords in the op_code dispatcher. Line 2053 logs passwords on failed login. This is a security violation that also represents a layering issue (security-sensitive data exposed through logging). |

---

## 15. Additional Observations

| Finding | Severity | Evidence |
|---------|----------|----------|
| `@SuppressWarnings("null")` annotations | **MEDIUM** | `Frm_vehicle.java` lines 9295, 9473, 9524, 9565 -- suppressing null-pointer warnings rather than fixing potential null dereferences. |
| `DecimalFormat` as instance field | **LOW** | `Frm_security.java` line 53, `Frm_vehicle.java` line 74, `Frm_customer.java` line 71: `DecimalFormat df = new DecimalFormat("########.###");` -- `DecimalFormat` is not thread-safe and should not be a servlet instance field. |
| TODO comments left in production | **LOW** | `GetGenericData.java:29`: `// TODO Auto-generated constructor stub`. `Frm_vehicle.java:14723`: `//TODO: Do we sync the VOR setting...`. `Frm_vehicle.java:14789`: `//TODO: Do we sync the full lock out settings...`. `Frm_security.java:3392`: `// TODO Auto-generated catch block`. |
| Massive `if/else if` dispatch chains | **HIGH** | `Frm_vehicle.java` `doPost()` has 30+ branches. `Frm_customer.java` `doGet()` has 15+ branches. `Frm_security.java` `doPost()` has 25+ branches. These should use a command pattern or strategy pattern. |

---

## Summary

| Check | Total Findings | Highest Severity |
|-------|---------------|-----------------|
| God classes | 4 | CRITICAL |
| Naming conventions | 5 | MEDIUM |
| Thread safety (servlet instance vars) | 5 (4 affected files) | CRITICAL |
| Commented-out code | 5 | HIGH |
| Unused imports | 3 | LOW |
| Empty catch blocks | 7 | HIGH |
| Broad `catch (Exception e)` | 87 total | HIGH |
| `e.printStackTrace()` | 93 total | HIGH |
| `System.out.println` | 342 total | HIGH |
| Inconsistent error handling | 5 | HIGH |
| Resource leaks | 5 | CRITICAL |
| Code duplication | 7 patterns | HIGH |
| Dead code | 7 | HIGH |
| Layering violations | 6 | CRITICAL |

**Overall Package Risk: CRITICAL**

The `security` package has severe code quality issues. The most urgent concerns are:

1. **Thread safety** -- Three servlets (`Frm_vehicle`, `Frm_customer`, `GetGenericData`) use mutable instance fields for JDBC resources, creating data races under concurrent requests. The commented-out `SingleThreadModel` confirms this was once mitigated but the mitigation was removed without proper refactoring.

2. **God classes** -- `Frm_vehicle.java` (~16,000 lines) and `Frm_customer.java` (~9,000 lines) are unmaintainable monoliths mixing database access, business logic, presentation formatting, and security concerns.

3. **Password logging** -- Cleartext passwords are written to application logs in `Frm_login.java` and `Frm_security.java`, a direct security violation.

4. **No architectural layering** -- All six files embed raw SQL in servlet methods with no DAO, service, or repository layer. This makes testing, maintenance, and security auditing extremely difficult.
