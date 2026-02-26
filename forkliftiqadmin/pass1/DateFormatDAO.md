# Pass 1 Audit — DateFormatDAO
**File:** src/main/java/com/dao/DateFormatDAO.java
**Date:** 2026-02-26

## Summary

`DateFormatDAO` is a minimal, single-method DAO that retrieves all rows from the `date_formats` table and maps them to `DateFormatBean` objects. It accepts no user-supplied parameters, uses a fully static SQL string, and delegates execution to `DBUtil.queryForObjects`. The DAO itself contains no direct SQL injection risk. However, two inherited issues from `DBUtil` affect this class: swallowed `SQLException`s that cause the method to silently return an empty list on database failure, and a misleading `throws SQLException` declaration that is never actually thrown due to that suppression. An additional secondary concern exists in `DateFormatBean.getExample()`, which passes the `format` column value retrieved from the database into `SimpleDateFormat` without validation.

---

## Findings

### MEDIUM: Swallowed SQLException in DBUtil.queryForObjects — Silent Empty-List Return

**File:** DateFormatDAO.java (line 17) — via DBUtil.java (lines 75–77)

**Description:**
`DateFormatDAO.getAll()` delegates to `DBUtil.queryForObjects`, which catches `SQLException`, calls `e.printStackTrace()`, and then returns an empty `List`. The exception is consumed and never re-thrown. As a result, `getAll()` will return an empty list rather than throwing when the database is unreachable, the `date_formats` table is missing, or any other SQL-level failure occurs. Callers in `AdminSettingsAction` (line 43) and `AdminMenuAction` (line 114) receive an empty list and proceed without any indication of failure. This also makes the `throws SQLException` declaration on `getAll()` misleading — it is a dead declaration; the exception can never actually propagate from this call path.

**Risk:**
- Silent failure hides operational problems. A DBA dropping or renaming the table, or a connection pool exhaustion event, will cause the settings page to silently render with no date-format options rather than surfacing an error.
- Diagnostic difficulty: `printStackTrace()` writes to stderr/log but provides no structured alerting. In production environments that do not monitor stderr, failures go unnoticed.
- Masking errors during the Struts action lifecycle prevents proper error-page forwarding, so users may see a broken UI with no actionable feedback.

**Recommendation:**
Remove the `catch (SQLException e)` block inside `DBUtil.queryForObjects` (and the other analogous `catch` blocks throughout `DBUtil`) and allow the exception to propagate to callers. Alternatively, log at `ERROR` level via the structured logger and re-throw. At the call sites in `AdminSettingsAction` and `AdminMenuAction`, handle the exception explicitly and forward to an appropriate error page.

---

### LOW: Dead `throws SQLException` Declaration

**File:** DateFormatDAO.java (line 14)

**Description:**
The method signature declares `throws SQLException`, but because `DBUtil.queryForObjects` catches and swallows all `SQLExceptions` internally, this checked exception can never actually be thrown by `getAll()`. The declaration is misleading to callers, who may believe they need to handle or propagate a `SQLException` that will in practice never arrive.

**Risk:**
- Low direct security risk. Primarily a correctness and maintainability issue.
- Callers may write `try/catch (SQLException)` blocks around `DateFormatDAO.getAll()` that are dead code, creating a false sense of error handling coverage.

**Recommendation:**
Once `DBUtil` is corrected to propagate exceptions (see finding above), the declaration becomes accurate and meaningful. Until then, consider removing it to accurately reflect the actual behavior, or add a comment documenting the known suppression in `DBUtil`.

---

### LOW: Unvalidated Database-Sourced Value Passed to SimpleDateFormat

**File:** src/main/java/com/bean/DateFormatBean.java (line 30) — invoked on objects returned by DateFormatDAO.getAll()

**Description:**
`DateFormatBean.getExample()` calls `new SimpleDateFormat(format)` where `format` is the raw string retrieved from the `format_value` column of `date_formats`. There is no validation or sanitisation of this value before it is used as a `SimpleDateFormat` pattern. If the database row contains a malformed or crafted pattern string:

1. `SimpleDateFormat` will throw an unchecked `IllegalArgumentException`, which is not caught in `getExample()`. Any JSP or template invoking `${dateFormat.example}` (or the equivalent Struts EL expression) will propagate this exception, potentially causing a 500 response and exposing a stack trace.
2. An adversary with write access to the `date_formats` table (e.g., via a separate SQL injection vulnerability elsewhere in the application) could store a pattern that triggers pathological `SimpleDateFormat` behaviour.

**Risk:**
- If an attacker can write to `date_formats`, they can cause a persistent denial-of-service on any page that renders `getExample()`.
- Stack traces returned in 500 responses may leak internal class names, package structure, and server configuration details.
- Risk is conditional on a separate write path to the `date_formats` table existing; this DAO itself only reads.

**Recommendation:**
Wrap the `SimpleDateFormat` construction and `format()` call in a `try/catch (IllegalArgumentException)` inside `getExample()` and return a safe fallback string (e.g., `"(invalid format)"`) on failure. Consider validating `format_value` entries at insert/update time rather than only at render time.

---

### INFO: No User-Supplied Input — SQL Injection Not Applicable

**File:** DateFormatDAO.java (lines 15–22)

**Description:**
The SQL query `"SELECT format_value FROM date_formats"` is a fully static string with no parameters, no concatenation, and no user-controlled data. It is passed to `DBUtil.queryForObjects`, which uses a `PreparedStatement` via `conn.prepareStatement(query)`. There is no SQL injection surface in this DAO.

**Risk:** None.

**Recommendation:** No action required. The use of `PreparedStatement` via `DBUtil` is the correct pattern; document it as the approved approach for future DAO development.

---

### INFO: No Resource Leaks in DateFormatDAO Itself

**File:** DateFormatDAO.java (lines 14–23)

**Description:**
`DateFormatDAO.getAll()` does not directly manage any `Connection`, `Statement`, or `ResultSet`. All JDBC resources are opened and closed inside `DBUtil.queryForObjects`, which uses `DbUtils.closeQuietly(conn, stmt, rs)` in a `finally` block. Resource management is handled correctly at the `DBUtil` layer for this call path.

**Risk:** None within this file.

**Recommendation:** No action required for this DAO. Note that `DBUtil.queryForObject(String, ResultMapper)` (DBUtil.java lines 128–146) opens a `Connection` before the `try` block, which is a minor resource-leak risk if `getConnection()` itself throws; that is a separate DBUtil-level finding.

---

## Finding Count
- CRITICAL: 0
- HIGH: 0
- MEDIUM: 1
- LOW: 2
- INFO: 2
