# Security Audit Report: AdvertismentDAO.java

**Repository:** forkliftiqadmin
**Branch:** master
**Audit Run:** audit/2026-02-26-01
**File:** `src/main/java/com/dao/AdvertismentDAO.java`
**Auditor:** CIG Automated Security Audit (Pass 1)
**Date:** 2026-02-26
**Stack:** Apache Struts 1.3.10 / JDBC (no ORM)

---

## 1. Reading Evidence

### Package and Class

- **Package:** `com.dao`
- **Class:** `AdvertismentDAO` (note: class name misspells "Advertisement")
- **Pattern:** Double-checked locking singleton (`getInstance()`)

### Public Methods

| Line | Signature |
|------|-----------|
| 22 | `public static AdvertismentDAO getInstance()` |
| 37 | `public ArrayList<AdvertisementBean> getAllAdvertisement() throws Exception` |
| 77 | `public ArrayList<AdvertisementBean> getAdvertisementById(String id) throws Exception` |
| 119 | `public Boolean delAdvertisementById(String id) throws Exception` |
| 149 | `public boolean saveAdvertisement(AdvertisementBean advertisementBean) throws Exception` |
| 206 | `public boolean updateAdvertisement(AdvertisementBean advertisementBean) throws Exception` |

### SQL Queries and Statement Types

| Method | Line | Statement Type | SQL |
|--------|------|----------------|-----|
| `getAllAdvertisement` | 50 | `Statement` (no user input) | `select id,pic,text,order_no from advertisment order by order_no` |
| `getAdvertisementById` | 91 | `Statement` + **string concatenation** | `select id,pic,text,order_no from advertisment where id = `**+id+**` order by order_no` |
| `delAdvertisementById` | 131 | `Statement` + **string concatenation** | `delete from advertisment where id=`**+id** |
| `saveAdvertisement` | 165 | `Statement` (static) then `PreparedStatement` (parameterized) | SELECT: static; INSERT: `insert into advertisment (pic,text,order_no) values (?,?,?)` |
| `updateAdvertisement` | 223/230 | `PreparedStatement` (parameterized) | Two branches: `update advertisment set text=? where id=?` / `update advertisment set pic=?,text=? where id=?` |

---

## 2. Findings

### SQL Injection

---

#### FINDING-01 — CRITICAL

**Severity:** CRITICAL
**File:** `src/main/java/com/dao/AdvertismentDAO.java`
**Line:** 91
**Category:** SQL Injection

**Description:**
`getAdvertisementById(String id)` constructs a SELECT query by directly concatenating the caller-supplied `id` parameter into the SQL string using a raw `Statement`. No sanitization, validation, or type conversion is performed on the input before it is embedded in the query.

**Evidence:**
```java
// Line 89-93
stmt=conn.createStatement(ResultSet.TYPE_SCROLL_SENSITIVE,ResultSet.CONCUR_READ_ONLY);
String sql = "select id,pic,text,order_no from advertisment where id = "+id+" order by order_no";
log.info(sql);
rs=stmt.executeQuery(sql);
```

A caller passing `id = "1 OR 1=1"` would produce:
```sql
select id,pic,text,order_no from advertisment where id = 1 OR 1=1 order by order_no
```
A caller passing `id = "1; DROP TABLE advertisment--"` (on a permissive DB configuration) could execute arbitrary DDL.

**Recommendation:**
Replace the `Statement` with a `PreparedStatement` and bind `id` as a typed parameter:
```java
String sql = "select id,pic,text,order_no from advertisment where id = ? order by order_no";
ps = conn.prepareStatement(sql);
ps.setInt(1, Integer.parseInt(id));
rs = ps.executeQuery();
```
Input should also be validated as a positive integer before the DAO is called.

---

#### FINDING-02 — CRITICAL

**Severity:** CRITICAL
**File:** `src/main/java/com/dao/AdvertismentDAO.java`
**Line:** 131
**Category:** SQL Injection

**Description:**
`delAdvertisementById(String id)` constructs a DELETE statement by directly concatenating the caller-supplied `id` parameter into the SQL string using a raw `Statement`. A DELETE with an injected `WHERE` clause can destroy arbitrary rows or the entire table; with stacked-query support it can execute further statements.

**Evidence:**
```java
// Line 131-133
String sql = "delete from advertisment where id="+id;
log.info(sql);
stmt.executeUpdate(sql);
```

A caller passing `id = "1 OR 1=1"` would produce:
```sql
delete from advertisment where id=1 OR 1=1
```
wiping every row in the table.

**Recommendation:**
Replace with a `PreparedStatement`:
```java
String sql = "delete from advertisment where id = ?";
ps = conn.prepareStatement(sql);
ps.setInt(1, Integer.parseInt(id));
ps.executeUpdate();
```
Additionally validate that `id` is a positive integer before invoking the DAO.

---

### Access Control

---

#### FINDING-03 — HIGH

**Severity:** HIGH
**File:** `src/main/java/com/dao/AdvertismentDAO.java` (all methods); caller `src/main/java/com/action/AdminMenuAction.java` line 85-87
**Lines:** 37, 77, 119, 149, 206
**Category:** Access Control — Missing Role/Privilege Enforcement at DAO Layer

**Description:**
No method in `AdvertismentDAO` accepts or checks a company ID, user ID, role, or session token. Advertisement records are global. The delete and save/update mutations are administrative operations (managing what is displayed to all users of the platform), yet the DAO itself provides no guard. Authorization is deferred entirely to the calling action layer.

Examination of `AdminMenuAction` (line 85-87) shows that the `advertisement` action branch does read a `sessCompId` from session and checks `sessUserId`, but it does **not** verify whether the authenticated user holds an administrator role before calling `AdvertismentDAO.getInstance().getAllAdvertisement()`. No callers of `delAdvertisementById`, `saveAdvertisement`, or `updateAdvertisement` were found in the codebase during this audit pass, meaning those mutation methods are either called from undiscovered JSP/action paths or are dead code — either case is a risk.

Furthermore, `web.xml` contains **no security filter** for the `/adminmenu.do` path beyond a character-encoding filter. There is no servlet security-constraint or authentication filter protecting the action URL.

**Evidence:**
- `web.xml` lines 8-15: only `CharsetEncodingFilter` is registered; no `AuthenticationFilter` or `SecurityFilter` exists.
- `AdminMenuAction.java` line 85: `AdvertismentDAO.getInstance().getAllAdvertisement()` — no role check before this call.
- No callers of `delAdvertisementById`, `saveAdvertisement`, or `updateAdvertisement` found anywhere in `src/main/java`.

**Recommendation:**
1. Add a servlet filter (or Struts `RequestProcessor` subclass) that enforces authentication and admin-role authorization on all `/admin*.do` paths.
2. Confirm that `delAdvertisementById`, `saveAdvertisement`, and `updateAdvertisement` are only reachable through admin-protected action paths.
3. Consider adding a role parameter to the DAO's mutation methods so that a defense-in-depth check is possible at the DAO layer.

---

### Data Exposure

---

#### FINDING-04 — LOW

**Severity:** LOW
**File:** `src/main/java/com/dao/AdvertismentDAO.java`
**Lines:** 37-75 (`getAllAdvertisement`), 77-117 (`getAdvertisementById`)
**Category:** Data Exposure — SQL logged verbatim including full query structure

**Description:**
Every method calls `log.info(sql)` before executing the query. For the two methods that concatenate user input into SQL (lines 92 and 132), the fully-assembled query — including any injected payload — is written to the application log at INFO level. If logs are forwarded to a SIEM or accessible to non-privileged parties, injected payloads and query structures are disclosed. Additionally, the static query in `getAllAdvertisement` reveals the exact table name (`advertisment`) and column set, which aids an attacker in fingerprinting the schema.

**Evidence:**
```java
// Line 51
log.info(sql);   // getAllAdvertisement — reveals table/column names
// Line 92
log.info(sql);   // getAdvertisementById — logs potentially attacker-controlled string
// Line 132
log.info(sql);   // delAdvertisementById — logs potentially attacker-controlled string
```

**Recommendation:**
Log a static descriptor (e.g., `"executing getAdvertisementById"`) rather than the raw SQL. If SQL logging is required for debugging, use DEBUG level and ensure production deployments run at INFO or above.

---

### Error Handling

---

#### FINDING-05 — MEDIUM

**Severity:** MEDIUM
**File:** `src/main/java/com/dao/AdvertismentDAO.java`
**Lines:** 106, 138, 190, 251
**Category:** Error Handling — Stack Trace Written to Standard Output

**Description:**
Three of the four catch blocks call `e.printStackTrace()` in addition to the logger. In a production servlet container, `System.err` (the destination of `printStackTrace`) may be captured in the server console log, in container-managed log files, or — in misconfigured deployments — surfaced in HTTP responses. Stack traces reveal internal package names, class hierarchy, library versions, and line numbers, all of which directly assist an attacker in targeting exploits.

Note that `getAllAdvertisement` (line 62-66) does **not** call `e.printStackTrace()` — this is the correct pattern and the other methods should follow it.

**Evidence:**
```java
// Line 103-108 (getAdvertisementById)
}catch(Exception e){
    InfoLogger.logException(log, e);
    e.printStackTrace();            // <-- exposes stack trace to stderr
    throw new SQLException(e.getMessage());
}

// Line 135-140 (delAdvertisementById) — same pattern
// Line 187-192 (saveAdvertisement)    — same pattern
// Line 248-253 (updateAdvertisement)  — same pattern
```

**Recommendation:**
Remove all `e.printStackTrace()` calls. The `InfoLogger.logException(log, e)` call already captures the full stack trace through the logging framework where retention and access can be controlled. `getAllAdvertisement` demonstrates the correct pattern.

---

#### FINDING-06 — LOW

**Severity:** LOW
**File:** `src/main/java/com/dao/AdvertismentDAO.java`
**Lines:** 65, 107, 139, 191, 252
**Category:** Error Handling — Exception Message Wrapping Discards Type Information

**Description:**
All catch blocks wrap exceptions as `throw new SQLException(e.getMessage())`. This strips the original exception type and its cause chain. If the original exception is not a `SQLException` (e.g., it is a `NullPointerException` or a connection-pool timeout), the caller receives a misleading `SQLException` containing only the message string, making diagnosis harder and potentially masking separate bug classes. It also means callers cannot distinguish a SQL error from a programming error.

**Evidence:**
```java
// Example at line 65
throw new SQLException(e.getMessage());
```

**Recommendation:**
Preserve the cause: `throw new SQLException(e.getMessage(), e)`. Alternatively, declare a checked application-layer exception and wrap with `throw new DaoException("getAdvertisementById failed", e)`.

---

#### FINDING-07 — LOW

**Severity:** LOW
**File:** `src/main/java/com/dao/AdvertismentDAO.java`
**Lines:** 193-199 (`saveAdvertisement` finally block), 254-259 (`updateAdvertisement` finally block)
**Category:** Error Handling — Connection Leak on PreparedStatement-Only Finally Path

**Description:**
In `saveAdvertisement`, the `finally` block closes the connection only inside the `if(null != ps)` guard (lines 196-199). If `ps` is null (e.g., an exception is thrown before `conn.prepareStatement()` is called, such as in the initial `stmt.executeQuery()`), `DBUtil.closeConnection(conn)` is never reached and the connection is leaked. The same pattern exists in `updateAdvertisement` (lines 254-259).

**Evidence:**
```java
// Lines 193-200 (saveAdvertisement)
finally{
    if(null != rs)   {rs.close();}
    if(null != stmt) {stmt.close();}
    if(null != ps) {
        ps.close();
        DBUtil.closeConnection(conn);  // <-- only reached if ps != null
    }
}
```
If the `SELECT max(order_no)` at line 165-170 throws before `ps` is assigned, `conn` is never closed.

**Recommendation:**
Move `DBUtil.closeConnection(conn)` outside the `if(null != ps)` guard so it always executes:
```java
finally{
    if(null != rs)   { try { rs.close();   } catch(Exception ignore){} }
    if(null != stmt) { try { stmt.close(); } catch(Exception ignore){} }
    if(null != ps)   { try { ps.close();   } catch(Exception ignore){} }
    DBUtil.closeConnection(conn);
}
```

---

## 3. Summary Table

| ID | Severity | Category | Line(s) | Title |
|----|----------|----------|---------|-------|
| FINDING-01 | CRITICAL | SQL Injection | 91 | `getAdvertisementById` — string-concatenated SELECT |
| FINDING-02 | CRITICAL | SQL Injection | 131 | `delAdvertisementById` — string-concatenated DELETE |
| FINDING-03 | HIGH | Access Control | 37,77,119,149,206 | No role/auth guard; no callers found for mutation methods; no web.xml security constraint |
| FINDING-04 | LOW | Data Exposure | 51,92,132 | SQL queries (including user input) logged at INFO level |
| FINDING-05 | MEDIUM | Error Handling | 106,138,190,251 | `e.printStackTrace()` leaks stack traces to stderr |
| FINDING-06 | LOW | Error Handling | 65,107,139,191,252 | Exception wrapping strips original type and cause chain |
| FINDING-07 | LOW | Error Handling | 193-199, 254-259 | Connection leak when `ps` is null in finally block |

**Finding counts by severity:**

| Severity | Count |
|----------|-------|
| CRITICAL | 2 |
| HIGH | 1 |
| MEDIUM | 1 |
| LOW | 3 |
| INFO | 0 |
| **Total** | **7** |

---

## 4. Categories With No Issues

- **No issues found in this category:** There are no findings for input validation at the bean layer (AdvertisementBean carries only id/pic/text/order_no with no processing logic). The `getAllAdvertisement` method correctly uses a static, non-parameterized query with no user input, so it is free of SQL injection. The `saveAdvertisement` INSERT and both branches of `updateAdvertisement` correctly use `PreparedStatement` with bound parameters.
