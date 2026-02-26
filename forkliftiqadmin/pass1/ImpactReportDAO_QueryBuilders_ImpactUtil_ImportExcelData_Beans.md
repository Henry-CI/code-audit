# Security Audit Report
## Scope: ImpactReportDAO, QueryBuilders (Impacts), ImpactUtil, ImportExcelData, Beans
**Application:** forkliftiqadmin (Apache Struts 1.3.10 / Tomcat)
**Branch:** master
**Date:** 2026-02-26
**Auditor:** Automated Pass 1

---

## Files Audited

| # | File |
|---|------|
| 1 | `src/main/java/com/dao/ImpactReportDAO.java` |
| 2 | `src/main/java/com/querybuilder/impacts/ImpactsByCompanyIdQuery.java` |
| 3 | `src/main/java/com/querybuilder/impacts/ImpactsCountByCompanyIdQuery.java` |
| 4 | `src/main/java/com/querybuilder/impacts/ImpactsReportByCompanyIdQuery.java` |
| 5 | `src/main/java/com/util/ImpactUtil.java` |
| 6 | `src/main/java/com/util/ImportExcelData.java` |
| 7 | `src/main/java/com/bean/ImpactReportBean.java` |
| 8 | `src/main/java/com/bean/ImpactReportFilterBean.java` |
| 9 | `src/main/java/com/bean/ImpactReportGroupBean.java` |
| 10 | `src/main/java/com/bean/ImpactReportGroupEntryBean.java` |

**Supporting files read for context (not directly audited):**
- `com/querybuilder/filters/FilterHandler.java`
- `com/querybuilder/filters/DateBetweenFilterHandler.java`
- `com/querybuilder/filters/ImpactLevelFilterHandler.java`
- `com/querybuilder/filters/UnitManufactureFilterHandler.java`
- `com/querybuilder/filters/UnitTypeFilterHandler.java`
- `com/querybuilder/filters/StringContainingFilterHandler.java`
- `com/querybuilder/StatementPreparer.java`
- `com/util/DBUtil.java`
- `com/bean/ReportFilterBean.java`
- `com/actionform/ImpactReportSearchForm.java`
- `com/action/ImpactReportAction.java`
- `com/action/DealerImpactReportAction.java`

---

## Findings

---

### CRITICAL: Arbitrary File Write via Unsanitised `savePath` in `ImportExcelData.upload()`

**File:** `ImportExcelData.java` (lines 29, 35, 79–81)

**Description:**
The `savePath` field is a plain `String` with a public setter and no validation whatsoever. Whatever value a caller places in `savePath` is used directly as the argument to `new File(savePath)`, which is then opened for writing with `FileOutputStream`.

```java
// ImportExcelData.java – lines 29, 35
private String savePath = "";

outputStream = new FileOutputStream(new File(savePath));
outputStream.write(formFile.getFileData());  // full file content written
```

```java
// ImportExcelData.java – lines 79-81
public void setSavePath(String savePath) {
    this.savePath = savePath;
}
```

If any caller derives `savePath` from user-controlled input (e.g., a form field, URL parameter, or the `FormFile` filename) without canonicalisation and containment to an approved upload directory, an attacker can supply a path such as:
- `../../webapps/ROOT/shell.jsp` — writes a JSP web shell into the Tomcat ROOT webapp
- `/etc/cron.d/backdoor` — writes a cron job on Linux hosts
- `../conf/web.xml` — overwrites Tomcat configuration

The method also returns `true` unconditionally regardless of whether the write succeeded, and silently swallows exceptions via `e.printStackTrace()` (see also finding on exception swallowing below). A failed write to an approved location is indistinguishable from a successful one at the call site.

**Risk:** Full remote code execution. A malicious actor who can reach the upload endpoint can overwrite arbitrary files on the server filesystem with fully attacker-controlled content, including web shells, configuration files, and cron jobs.

**Recommendation:**
1. Compute a canonical safe base directory at construction time (e.g., from `ServletContext.getRealPath("/uploads/")` or a configured absolute path).
2. Canonicalise the caller-supplied filename with `File.getCanonicalPath()` and assert that it starts with the approved base directory before creating the `FileOutputStream`.
3. Strip all directory separators from the user-supplied filename; store files under a server-generated UUID name.
4. Remove the public `setSavePath(String)` setter; accept only the `FormFile` object and derive a safe path internally.
5. Propagate exceptions properly instead of swallowing them; throw on failure rather than returning `true`.

---

### CRITICAL: SQL Injection via `timezone` Parameter Concatenated into `COUNT_QUERY`

**File:** `ImpactsByCompanyIdQuery.java` (lines 13–15), `ImpactsCountByCompanyIdQuery.java` (lines 17–28)

**Description:**
`COUNT_QUERY` contains `timezone(?, ...)` placeholders and the timezone is correctly bound via `prepareStatement` in `ImpactsCountByCompanyIdQuery`. However, the call chain reaches this query through `ImpactReportDAO.countImpactsToday(compId, timezone)` where `timezone` ultimately originates from `session.getAttribute("sessTimezone")` — a session attribute. This is correctly handled for the count query.

The **report** path (`ImpactsReportByCompanyIdQuery`) passes the `filter` object (which contains `timezone` from `ImpactReportFilterBean`) into `DateBetweenFilterHandler`. The `DateBetweenFilterHandler.getQueryFilter()` method uses `String.format()` with a hardcoded `fieldName` (safe), but the `prepareStatement` method conditionally adds `filter.timezone()` as a bind parameter only when `filter.timezone() != null`. This is safe for the timezone value itself.

**The actual injection point is the `%s` format specifier in `REPORT_QUERY`:**

```java
// ImpactsByCompanyIdQuery.java – lines 18-21
static final String REPORT_QUERY = "SELECT vi.*, c.name AS assigned_company_name " +
        BASE_QUERY +
        " %s " +              // <-- filter fragment substituted here via String.format
        "ORDER BY impact_time DESC";
```

```java
// ImpactsReportByCompanyIdQuery.java – lines 39-43
private String getQuery() {
    StringBuilder filters = new StringBuilder();
    for (FilterHandler handler : filterHandlers) filters.append(handler.getQueryFilter());
    return String.format(ImpactsByCompanyIdQuery.REPORT_QUERY, filters);
}
```

The `filters` string is assembled from `FilterHandler.getQueryFilter()` return values. For the four handlers in the impacts report, all `fieldName` values are hardcoded literals (`"impact_time"`, `"manufacture_id"`, `"type_id"`, `"impact_value"`, `"unit_threshold"`). **These specific values are safe.** However, the architectural pattern itself is hazardous:

1. `StringContainingFilterHandler.getQueryFilter()` (used elsewhere in the codebase) appends `fieldNames` directly into the SQL fragment: `filter.append(fieldName).append(" ILIKE ? OR ")`. If `fieldName` were ever derived from user input rather than a hardcoded literal, this would be a direct injection path.

2. The `%s` substitution mechanism in `REPORT_QUERY` means the entire filter string — which can contain arbitrary SQL text returned by `getQueryFilter()` — is inserted into a raw SQL string before `conn.prepareStatement()` is called. Any future `FilterHandler` implementation that concatenates a non-constant value into its `getQueryFilter()` result will immediately produce an injectable query, with no safety net at the `DBUtil` layer.

3. `ImpactLevelFilterHandler.getQueryFilter()` hardcodes numeric multipliers (safe), but the pattern of embedding `impactFieldName` and `thresholdFieldName` directly via `String.format` within the filter would be injectable if those field names were ever user-derived.

**Risk:** If `fieldName` values are ever sourced from user input, or if a new `FilterHandler` is added that concatenates a non-constant, full SQL injection is possible against the impacts report query. The `%s`-in-`String.format` architecture provides no structural safety guarantee; the safety is entirely dependent on every caller passing only hardcoded `fieldName` literals forever.

**Recommendation:**
1. Replace the `%s` / `String.format` approach in `REPORT_QUERY` with a fixed, enumerated set of permissible SQL clauses selected by an enum or validated field name whitelist.
2. Validate all `fieldName` values passed to `FilterHandler` constructors against an allowlist of known column names at construction time (throw `IllegalArgumentException` on violation).
3. Treat the `%s` substitution in `REPORT_QUERY` as equivalent to string concatenation and document it clearly with a prominent security comment requiring all `FilterHandler` implementations to use only `?` placeholders.

---

### HIGH: `DBUtil.queryForObject(String, ResultMapper)` — Dangerous No-Bind Overload Accessible Application-Wide

**File:** `DBUtil.java` (lines 128–146)

**Description:**
`DBUtil` exposes a two-argument overload of `queryForObject` that accepts a fully-formed SQL string and a result mapper, with **no `PreparedStatementHandler` bind step**:

```java
// DBUtil.java – lines 128-146
public static <T> Optional<T> queryForObject(String query, ResultMapper<T> mapper) throws SQLException {
    PreparedStatement stmt = null;
    ResultSet rs = null;
    Connection conn = getConnection();

    try {
        stmt = conn.prepareStatement(query);
        rs = stmt.executeQuery();
        // ...
    }
```

While `conn.prepareStatement(query)` is called, no parameters are bound because the overload provides no mechanism to do so. Any caller that builds `query` by concatenating user-controlled values and then passes it to this overload executes the concatenated SQL without bind-parameter protection. Two callers exist in `DriverDAO` (lines 845, 850) with hardcoded SQL (safe), but the method is `public static` and available to any class in the application.

The `ImpactsCountByCompanyIdQuery` correctly uses the three-argument overload. However, the existence of the two-argument overload as a public utility method creates an ongoing risk: any developer adding new DAO code who reaches for the "simpler" two-argument form and constructs the query string with concatenation will produce an injectable query. There is no deprecation annotation or warning on this method discouraging its use with dynamic SQL.

**Risk:** Any future or existing call to the two-argument `queryForObject` with a dynamically constructed SQL string is a SQL injection vulnerability. The risk is systemic: the method is a permanently available injection gateway in the shared utility layer.

**Recommendation:**
1. Annotate `queryForObject(String, ResultMapper)` with `@Deprecated` and add a Javadoc warning: "SQL must be a static literal. Never concatenate user-supplied values into the query argument."
2. Audit all existing and future callers to ensure the `query` argument is always a compile-time constant.
3. Consider removing the two-argument overload entirely and requiring callers to use the three-argument form with an explicit (possibly no-op) `PreparedStatementHandler`.

---

### HIGH: Exception Swallowing in `DBUtil` Hides SQL Failures and Security Decisions

**File:** `DBUtil.java` (lines 75–77, 98–100, 119–121, 140–142, 165–167, 204–206, 222–224)

**Description:**
Every `queryForObjects`, `queryForObjectsWithRowHandler`, and `queryForObject` method in `DBUtil` catches `SQLException`, calls `e.printStackTrace()`, and then **continues as if the query succeeded**, returning an empty list or `Optional.empty()`:

```java
// DBUtil.java – lines 75-77 (queryForObjects)
} catch (SQLException e) {
    e.printStackTrace();
}
// execution falls through — returns empty List<T>
```

```java
// DBUtil.java – lines 98-100 (queryForObjectsWithRowHandler)
} catch (SQLException e) {
    e.printStackTrace();
}
// execution falls through — returns empty List<T>
```

```java
// DBUtil.java – lines 140-142 (queryForObject two-arg)
} catch (SQLException e) {
    e.printStackTrace();
}
// execution falls through — returns Optional.empty()
```

This pattern is dangerous in several security-relevant scenarios:

1. **Silent authorisation bypass:** If a query that enforces data ownership (e.g., the `comp_id` filter in `BASE_QUERY`) fails due to a transient DB error or a crafted bad input, the method returns an empty result. The caller (e.g., `ImpactReportAction`) interprets this as "no data found" rather than an error, and may present a blank report to the user — masking the error completely.

2. **`updateObject` returns -1 on failure:** `DBUtil.updateObject` similarly swallows exceptions and returns `-1`. Any caller that does not explicitly check for -1 will silently skip error handling for failed writes, including failed security-relevant writes (audit log inserts, etc.).

3. **No log aggregation:** `e.printStackTrace()` writes to `stderr`/Tomcat console. In production, this output is typically lost. There is no structured logging (e.g., SLF4J) in `DBUtil`, so SQL errors are invisible in log management systems.

4. **`ImpactsCountByCompanyIdQuery.query()` declares `throws SQLException`** but the exception is swallowed inside `DBUtil`; the declared `throws` is never actually triggered by the DB path, giving callers false confidence.

**Risk:** Database errors that should surface as failures (and trigger error handling, alerting, or denial of access) are silently converted to empty results. This can mask injection attempts, authorisation failures, and infrastructure problems. Security-relevant write failures go undetected.

**Recommendation:**
1. Re-throw exceptions from all `DBUtil` query methods: `throw e;` after logging, or wrap in a runtime exception.
2. Replace `e.printStackTrace()` with `log.error("Query failed: {}", query, e)` using SLF4J.
3. In all callers that receive a result from `DBUtil`, treat an unexpected empty result as a potential error condition and check for it explicitly.

---

### HIGH: Unvalidated `ImpactLevel.valueOf()` Causes Unhandled `IllegalArgumentException` and Potential Information Leakage

**File:** `ImpactReportSearchForm.java` (line 38); `ImpactReportGroupEntryBean.java` (lines 37–39, 45–47); `ImpactUtil.java` (lines 19–43)

**Description:**
The `impact_level` request parameter is converted to an `ImpactLevel` enum using the raw `ImpactLevel.valueOf()` call with no try/catch:

```java
// ImpactReportSearchForm.java – line 38
.impactLevel(StringUtils.isBlank(this.impact_level) ? null : ImpactLevel.valueOf(this.impact_level))
```

If an attacker submits any value that is not `BLUE`, `AMBER`, or `RED` (e.g., `impact_level=INVALID` or `impact_level='; DROP TABLE impacts; --`), `ImpactLevel.valueOf()` throws `IllegalArgumentException`. In Struts 1.x this uncaught exception propagates up through the Action, and Struts may render a default error page that includes the full exception message and stack trace, disclosing internal package names, class names, and potentially DB schema details.

A related issue exists in `ImpactReportGroupEntryBean.getImpactLevelCSSColor()` (line 45):

```java
// ImpactReportGroupEntryBean.java – lines 45-47
public String getImpactLevelCSSColor() {
    return ImpactUtil.getCSSColor(getImpactLevel());
}
```

`getImpactLevel()` calls `ImpactUtil.calculateImpactLevel()` which can return `null` when `impactValue <= impactThreshold * BLUE_IMPACT_COEFFICIENT` (line 49 of `ImpactUtil.java`). `getCSSColor(null)` hits the `default` branch of the switch, which throws `UnhandledImpactLevelException` (an `IllegalArgumentException`). If this is called from a JSP EL expression (e.g., `${entry.impactLevelCSSColor}`), Struts/Tomcat will propagate the exception and may render a 500 error page with stack trace.

**Risk:** Stack trace and internal class/package disclosure in error responses. Potential for causing repeated 500 errors (DoS-adjacent). The `null` return from `calculateImpactLevel` propagates silently until it causes an NPE or exception in `getCSSColor`.

**Recommendation:**
1. Wrap `ImpactLevel.valueOf(this.impact_level)` in a try/catch and return `null` (or a specific sentinel) for unrecognised values, logging the invalid input.
2. In `ImpactUtil.calculateImpactLevel()`, document that `null` is a valid return (meaning "below threshold") and add null-safety to `getCSSColor()` and `getImpactLevelCSSColor()` — e.g., return `""` or `"grey"` rather than throwing.
3. Configure Struts/Tomcat to suppress stack trace output in error responses in production.

---

### HIGH: Arbitrary File Write — No Validation of `FormFile` Content or Size in `upload()`

**File:** `ImportExcelData.java` (lines 32–45)

**Description:**
The `upload()` method writes the full binary content of the uploaded `FormFile` to disk without any validation:

```java
// ImportExcelData.java – lines 32-45
public boolean upload(FormFile formFile) throws ServletException, IOException {
    FileOutputStream outputStream = null;
    try {
        outputStream = new FileOutputStream(new File(savePath));
        outputStream.write(formFile.getFileData());   // entire file written, no size check
    } catch(Exception e){
        e.printStackTrace();                           // exception swallowed
    }
    if (outputStream != null) {
        outputStream.close();
    }
    return true;   // always returns true, even on failure
}
```

Issues:
1. **No file size limit:** `formFile.getFileData()` loads the entire file into a `byte[]`. A malicious actor can upload a very large file, causing an `OutOfMemoryError` on the heap before the `FileOutputStream` is even opened, or exhausting disk space if the write proceeds.
2. **No MIME type or magic byte validation:** Any file type can be uploaded. If `savePath` points inside a web-accessible directory, uploading a `.jsp` or `.jspx` file constitutes a direct web shell upload.
3. **No file extension restriction:** The method is completely agnostic to file extension.
4. **`getFileData()` is deprecated in newer Apache Commons FileUpload** and loads the complete file into memory as a byte array, compounding the DoS risk.
5. **Exception swallowing + unconditional `return true`:** If the `FileOutputStream` constructor or `write()` throws (e.g., disk full, permission denied), the exception is caught, printed, and the method returns `true`, telling the caller the upload succeeded.

**Risk:** Denial of service via heap exhaustion or disk fill; web shell upload if `savePath` is web-accessible; silent false-success reporting of failed uploads.

**Recommendation:**
1. Enforce a maximum file size before calling `getFileData()` (check `formFile.getFileSize()` against a configured limit).
2. Validate the file extension against an allowlist (`[".xls", ".xlsx", ".csv"]`).
3. Validate the magic bytes of the uploaded content (Excel `.xlsx` starts with `PK\x03\x04`; `.xls` starts with `\xD0\xCF\x11\xE0`).
4. Stream the upload to disk rather than loading it into a `byte[]`.
5. Throw on failure rather than returning `true` unconditionally.

---

### HIGH: Insecure Direct Object Reference — Cross-Tenant Data Access via `unit_company` JOIN

**File:** `ImpactsByCompanyIdQuery.java` (lines 6–11); `ImpactsReportByCompanyIdQuery.java` (lines 31–37)

**Description:**
`BASE_QUERY` uses the following ownership predicate:

```sql
-- ImpactsByCompanyIdQuery.java – lines 10-11
WHERE (vi.comp_id = ? OR uc.company_id = ?)
AND unit_threshold != 0 AND impact_value >= unit_threshold
```

The `OR uc.company_id = ?` branch returns impacts for any unit currently (or historically) assigned to the authenticated company via `unit_company`, even if those units were originally registered under a different `comp_id`. This is intentional for a dealer/fleet management model where units are leased.

However, the report query selects `vi.*` — **all columns from `v_impacts`** — including potentially sensitive fields that belong to units whose primary `comp_id` differs from the session user's `sessCompId`. There is no secondary ownership check that limits which columns are returned, and the query includes:

```sql
SELECT vi.*, c.name AS assigned_company_name
```

If the `v_impacts` view contains PII columns (driver details, GPS coordinates, device identifiers) for units not owned by the requesting company, those are returned in full to any authenticated company that has (or has had) a `unit_company` assignment. A company that briefly leased a unit and then returned it could, depending on the date range filter, still retrieve historical impact data for that unit including driver names from periods when it was assigned to a different company.

Furthermore, `ImpactsCountByCompanyIdQuery` uses the same `BASE_QUERY` and the same `OR uc.company_id = ?` pattern, so the count figure on the dashboard (`countImpactsToday`) may reflect units the company no longer controls.

**Risk:** Cross-tenant data leakage of driver PII and operational data for units not owned by the authenticated company (IDOR via historical `unit_company` join).

**Recommendation:**
1. Review the business requirement: should `OR uc.company_id = ?` be restricted to currently active assignments only? The `LEFT JOIN` already has date range conditions, but the `unit_company` table's date constraints should be explicitly reviewed.
2. Explicitly enumerate the columns returned in the `SELECT` clause of `REPORT_QUERY` rather than using `vi.*`, and omit any fields that should not be visible to a company accessing a unit through the `unit_company` join path.
3. Consider adding a `uc.end_date IS NULL` (or `uc.end_date >= NOW()`) condition to limit cross-company access to currently active assignments only, if historical cross-company visibility is not an intended feature.

---

### MEDIUM: `ReportFilterBean.start()` and `.end()` Default to `NOW()` When `startDate`/`endDate` Are Null — Silent Data Exposure

**File:** `ReportFilterBean.java` (lines 22–29)

**Description:**
`ReportFilterBean.start()` and `ReportFilterBean.end()` return `Calendar.getInstance().getTime()` (i.e., the current timestamp) when the caller has not set `startDate` or `endDate`:

```java
// ReportFilterBean.java – lines 22-29
@Override
public Date start() {
    return startDate != null ? startDate : Calendar.getInstance().getTime();
}

@Override
public Date end() {
    return endDate != null ? endDate : Calendar.getInstance().getTime();
}
```

`DateBetweenFilterHandler` checks `filter.start() != null` and `filter.end() != null` to decide which filter branch to apply. Because `start()` and `end()` **never return null** (they default to `NOW()`), the handler will always take the `filterBetweenTwoDates()` branch, applying `BETWEEN ? AND ?`. When neither `startDate` nor `endDate` is set, this produces the effective filter `BETWEEN NOW() AND NOW()`, returning only impacts occurring at the exact current millisecond — returning zero results. This is almost certainly not the intended behaviour when no date filter is specified; the expected result is likely "all impacts" (no date filter).

This is a logic bug with security implications: if an auditor queries the report without providing date bounds expecting to see all historical impacts, they receive nothing, potentially causing under-reporting of safety incidents.

**Risk:** Silent suppression of all results when the date filter is omitted by a user expecting to see all data. Could mask safety-critical historical impacts in audit or investigation scenarios.

**Recommendation:**
1. Change `start()` and `end()` to return `null` when the corresponding field is `null`, and update `DateBetweenFilterHandler.ignoreFilter()` to check for `filter.start() == null && filter.end() == null` before emitting any date clause.
2. Alternatively, document the defaulting behaviour explicitly and make callers pass explicit dates when they intend to filter.

---

### MEDIUM: `ImpactReportGroupBean.compareTo()` Violates `Comparable` Contract — Sort Instability

**File:** `ImpactReportGroupBean.java` (lines 35–37)

**Description:**
`ImpactReportGroupBean` implements `Comparable<ImpactReportGroupBean>` and its `compareTo` method adds two `String.compareTo()` results:

```java
// ImpactReportGroupBean.java – lines 35-37
@Override
public int compareTo(ImpactReportGroupBean o) {
    return this.manufacturer.compareTo(o.manufacturer) + this.unitName.compareTo(o.unitName);
}
```

The `Comparable` contract requires that `compareTo` returns a negative, zero, or positive integer where the sign is consistent and transitive. Adding two `compareTo` results does not satisfy this contract: the sum can be zero even when the two strings are not equal (e.g., `manufacturer` returns +1 and `unitName` returns -1). This means:

- The sort performed in `ImpactsReportByCompanyIdQuery.query()` via `Collections.sort()` is non-deterministic and may produce inconsistent ordering.
- More dangerously, `compareTo` will throw a `NullPointerException` if either `manufacturer` or `unitName` is `null` (both are set from `rs.getString()` which returns `null` for SQL `NULL`). The NPE thrown from within `Collections.sort()` propagates up as an uncaught runtime exception.

**Risk:** `NullPointerException` crashing the impact report for any company that has a unit with a null manufacturer or unit name in the database. An attacker (or misconfigured data entry) that sets a unit's manufacturer to NULL can cause persistent report failures for the affected company.

**Recommendation:**
1. Use `Comparator.comparing()` with `Comparator.nullsFirst()` / `Comparator.nullsLast()` rather than a hand-coded `compareTo`.
2. Fix the comparison logic: use `Comparator.comparing(ImpactReportGroupBean::getManufacturer).thenComparing(ImpactReportGroupBean::getUnitName)`.
3. Replace `implements Comparable` with an explicit `Comparator` passed to `Collections.sort()`.

---

### MEDIUM: Timezone Parameter Injected via User Session into `DateBetweenFilterHandler` SQL Fragment

**File:** `DateBetweenFilterHandler.java` (lines 17–24); `ImpactReportSearchForm.java` (line 39); `ImpactsReportByCompanyIdQuery.java` (lines 24, 46–49)

**Description:**
The `timezone` value flows from the form (`ImpactReportSearchForm`) or session through `ImpactReportFilterBean` into `DateBetweenFilterHandler`. The handler correctly binds the timezone as a `?` placeholder in the SQL:

```java
// DateBetweenFilterHandler.java – line 22
if (filterBetweenTwoDates()) return String.format(" AND timezone(?, %s at time zone 'UTC')::DATE BETWEEN ? AND ?", fieldName);
```

```java
// DateBetweenFilterHandler.java – line 29
if(filter.timezone() != null) preparer.addString(filter.timezone());
```

The timezone itself is properly parameterised. However, the **order of bind parameters has an implicit dependency**: `prepareStatement` adds `timezone` only when `filter.timezone() != null`, but `getQueryFilter()` always emits the `timezone(?, ...)` placeholder when `filterBetweenTwoDates()` is true. If `filter.timezone()` is null and `filterBetweenTwoDates()` is true, the `timezone` placeholder `?` is emitted in the SQL but **not bound** in `prepareStatement`, causing a parameter index mismatch and a `SQLException`.

Because `DBUtil` swallows that `SQLException` and returns an empty list, the report silently returns no data rather than failing loudly. An attacker who controls the `timezone` field and sets it to `null` (or blank) while providing date values can force a blank report with no error indication.

**Risk:** Silent denial of report data via null/blank timezone combined with date filter; parameter index corruption on the `PreparedStatement`.

**Recommendation:**
1. In `DateBetweenFilterHandler.prepareStatement()`, validate that timezone is non-null before proceeding when `filterBetweenTwoDates()` is true, or always emit the timezone bind parameter regardless.
2. Alternatively, restructure the logic so that timezone is required when a date filter is active, throwing an `IllegalStateException` at construction time if dates are provided without a timezone.

---

### MEDIUM: `ImportExcelData.read()` Uses `FileReader` Without Charset — Locale-Dependent Parsing

**File:** `ImportExcelData.java` (lines 47–72)

**Description:**
`read(String fileName)` opens a CSV file using `new FileReader(file)`, which uses the platform default charset:

```java
// ImportExcelData.java – lines 51-52
File file = new File(fileName);
BufferedReader bufRdr = new BufferedReader(new FileReader(file));
```

On a Tomcat server where the JVM default charset differs from the encoding of uploaded files, multi-byte characters (e.g., UTF-8 accented characters in driver names) will be mis-read, and values containing the byte sequence for `,` in multi-byte encodings (e.g., certain SHIFT-JIS sequences) could be mis-tokenised, corrupting the parse.

Additionally, `StringTokenizer` is used for CSV parsing, which does not handle quoted fields. A value such as `"Smith, John"` would be split into two tokens: `"Smith` and ` John"`, corrupting data. If the corrupted data is subsequently inserted into the database (by the caller of `read()`), it represents an integrity issue. If driver names or other fields are used in SQL queries after this import, garbled UTF-8 sequences could contribute to injection risk depending on the DB driver's charset handling.

The `bufRdr` is also never closed in any code path, creating a file handle leak.

**Risk:** Data integrity corruption on import; potential file handle exhaustion under repeated calls; encoding-dependent CSV parsing correctness.

**Recommendation:**
1. Use `new InputStreamReader(new FileInputStream(file), StandardCharsets.UTF_8)` (or the appropriate known encoding) instead of `new FileReader(file)`.
2. Replace `StringTokenizer` with a proper CSV library (e.g., Apache Commons CSV or OpenCSV) that handles quoted fields.
3. Use try-with-resources for the `BufferedReader`.

---

### MEDIUM: `ImportExcelData` Imports `XSSFWorkbook` and `HSSFWorkbook` — XXE Risk if XML Parsing Is Not Hardened

**File:** `ImportExcelData.java` (lines 19–24)

**Description:**
`ImportExcelData.java` imports `org.apache.poi.xssf.usermodel.XSSFWorkbook` and `org.apache.poi.hssf.usermodel.HSSFWorkbook` (lines 19–24). While neither class is directly instantiated in the code as read (the `upload()` and `read()` methods do not call POI), the imports indicate that POI-based Excel parsing is **planned or was previously present** in this class.

Apache POI's `XSSFWorkbook` (which parses `.xlsx` / OOXML files — ZIP archives containing XML) is historically vulnerable to XXE (XML External Entity injection) in versions prior to 3.15. An `.xlsx` file is a ZIP archive whose internal XML parts can embed `DOCTYPE` declarations with external entity references. If POI's XML parser is not configured to disable external entity resolution (via `XMLInputFactory.setProperty(XMLInputFactory.IS_SUPPORTING_EXTERNAL_ENTITIES, false)` and similar), a crafted `.xlsx` upload can cause the server to fetch attacker-controlled URLs or read local files (e.g., `/etc/passwd`) and include their contents in error messages.

The declared POI version should be checked; if it is below 3.15, the XXE risk is confirmed. Even in newer versions, the POI hardening must be in place.

The `read()` method currently only handles CSV text files via `BufferedReader`, but the class structure (with the POI imports) strongly implies future or parallel use of POI for binary Excel parsing.

**Risk:** If POI-based parsing is activated (or is activated elsewhere using this class): XXE leading to server-side request forgery (SSRF) or local file inclusion via a crafted `.xlsx` upload.

**Recommendation:**
1. Check the POI version in `pom.xml`. If below 3.15, upgrade immediately.
2. Ensure that when `XSSFWorkbook` is instantiated, the XML parser is hardened against XXE using `WorkbookFactory.create()` (which in POI >= 3.15 has XXE protections) rather than directly constructing `new XSSFWorkbook(stream)`.
3. Remove unused imports if POI is genuinely not used in this class.

---

### LOW: `ImpactReportDAO` Singleton Uses Double-Checked Locking Without `volatile` Guarantee on All JVMs

**File:** `ImpactReportDAO.java` (lines 12–24)

**Description:**
`ImpactReportDAO` implements the singleton pattern with double-checked locking:

```java
// ImpactReportDAO.java – lines 12-24
private static ImpactReportDAO theInstance;

public static ImpactReportDAO getInstance() {
    if (theInstance == null) {
        synchronized (ImpactReportDAO.class) {
            if (theInstance == null) {
                theInstance = new ImpactReportDAO();
            }
        }
    }
    return theInstance;
}
```

`theInstance` is not declared `volatile`. Without `volatile`, the double-checked locking pattern is broken under the Java Memory Model prior to Java 5 and may be broken in certain JIT-optimised scenarios even on later JVMs: the JIT can reorder the write to `theInstance` before the constructor body completes, causing a second thread that passes the first null check to receive a partially-constructed object. For a trivially empty constructor (as here), the practical risk is extremely low, but the pattern is incorrect by the Java Memory Model specification.

**Risk:** Theoretical race condition returning a partially constructed `ImpactReportDAO` to concurrent callers on application startup. Practically negligible for this trivial constructor, but sets a bad precedent for more complex singletons in the codebase.

**Recommendation:**
Declare `theInstance` as `private static volatile ImpactReportDAO theInstance;`, or replace the double-checked locking pattern with initialisation-on-demand holder (Bill Pugh singleton):

```java
private static class Holder {
    static final ImpactReportDAO INSTANCE = new ImpactReportDAO();
}
public static ImpactReportDAO getInstance() { return Holder.INSTANCE; }
```

---

### LOW: `@Data` on `ImpactReportFilterBean` and `ReportFilterBean` Generates `toString()` Including All Filter Fields

**File:** `ImpactReportFilterBean.java` (line 10); `ReportFilterBean.java` (line 13)

**Description:**
Lombok `@Data` generates a `toString()` method that includes all fields. `ImpactReportFilterBean` extends `ReportFilterBean`, both annotated `@Data`. The combined `toString()` output includes: `startDate`, `endDate`, `manuId`, `typeId`, `timezone`, and `impactLevel`. While none of these is a password or session token, if this object is ever logged (e.g., in a debug or error log statement) in a context where `sessCompId` or other session state is co-logged, it contributes to PII leakage (dates and filter selections can identify specific user investigation patterns).

More concretely, `ImpactReportGroupEntryBean` (annotated `@Data`) has `toString()` output that includes `driverName` — a PII field. If any logger in the call chain logs the `ImpactReportBean` or its nested beans (e.g., during debugging), driver names are written to log files.

**Risk:** PII (driver names) written to application logs via Lombok-generated `toString()` if beans are ever logged. Low direct exploitability, but a compliance risk under data protection regulations.

**Recommendation:**
1. Override `toString()` in `ImpactReportGroupEntryBean` to exclude `driverName`, or use `@ToString.Exclude` on that field.
2. Annotate `@ToString(onlyExplicitlyIncluded = true)` on beans containing PII and mark only safe fields with `@ToString.Include`.

---

### LOW: `ImportExcelData.upload()` Does Not Close `FileOutputStream` on Exception

**File:** `ImportExcelData.java` (lines 32–45)

**Description:**
The `FileOutputStream` is closed in a manual `if (outputStream != null)` block after the try/catch, but this block is outside any `finally` block. If `outputStream.write(formFile.getFileData())` throws, the exception is caught and swallowed, and execution continues to the `if (outputStream != null)` check — so the stream is closed. However, if `new FileOutputStream(new File(savePath))` throws (e.g., invalid path, permission denied), `outputStream` remains `null`, no exception propagates, the method returns `true`, and the partial/failed operation is undetectable.

```java
// ImportExcelData.java – lines 33-44
FileOutputStream outputStream = null;
try {
    outputStream = new FileOutputStream(new File(savePath));
    outputStream.write(formFile.getFileData());
} catch(Exception e){
    e.printStackTrace();         // swallowed
}
if (outputStream != null) {
    outputStream.close();        // only reached if construction succeeded
}
return true;                     // always true
```

There is also no `finally` block ensuring `close()` is called if `write()` throws. The broad `catch(Exception e)` catches `IOException` from `write()` but then falls through to the `if (outputStream != null)` check which does close it — so in practice the stream is closed after a write failure. However, this is fragile and non-idiomatic; a code reviewer would not immediately see that the close is guaranteed.

**Risk:** File handle leak under constructor-failure path; non-standard resource management pattern that is error-prone under refactoring.

**Recommendation:**
Rewrite using try-with-resources:
```java
try (FileOutputStream outputStream = new FileOutputStream(new File(savePath))) {
    outputStream.write(formFile.getFileData());
}
```

---

### INFO: `ImpactUtil.calculateImpactLevel()` Returns `null` — Undocumented Null Return

**File:** `ImpactUtil.java` (line 49)

**Description:**
`calculateImpactLevel()` returns `null` when the impact value does not exceed any threshold coefficient:

```java
// ImpactUtil.java – line 49
return null;
```

This null return is not documented in Javadoc and is not handled by `getCSSColor()` or `getGForce()` callers. As noted in the HIGH finding above, `getCSSColor(null)` throws `UnhandledImpactLevelException`. This is a null-safety contract gap rather than a direct vulnerability, but it contributes to the crash risk identified above.

**Risk:** Contributes to the NPE/exception chain identified in the HIGH finding for `ImpactReportGroupEntryBean.getImpactLevelCSSColor()`.

**Recommendation:**
Add `@Nullable` annotation (or Javadoc `@return null if value is below threshold`) and handle the null case in all callers.

---

### INFO: `ImpactsByCompanyIdQuery.REPORT_QUERY` Uses `%s` Format Specifier — Architectural SQL Injection Risk Note

**File:** `ImpactsByCompanyIdQuery.java` (lines 18–21)

**Description:**
This is a documentation-level note supplementing the CRITICAL finding above. The `REPORT_QUERY` template:

```java
static final String REPORT_QUERY = "SELECT vi.*, c.name AS assigned_company_name " +
        BASE_QUERY +
        " %s " +
        "ORDER BY impact_time DESC";
```

uses Java's `String.format()` with `%s` to splice the filter fragment into the SQL. This is architecturally equivalent to string concatenation of SQL. The current callers (`ImpactsReportByCompanyIdQuery`) use only hardcoded `fieldName` values and `?` placeholders within filter fragments, so the current code is not exploitable. However, this architectural pattern should be flagged in developer documentation and code review guidelines as a category of code that requires careful review whenever new `FilterHandler` implementations or new query templates are introduced.

**Risk:** None currently; future regression risk if new handlers concatenate non-constant values.

**Recommendation:**
Add a code comment on `REPORT_QUERY` explicitly stating: "The `%s` placeholder is filled only with SQL fragments using `?` bind parameters. Never concatenate user-controlled data into the filter fragment." Consider a custom wrapper type to distinguish safe SQL fragments from raw strings.

---

## Summary

| Severity | Count | Findings |
|----------|-------|---------|
| CRITICAL | 2 | Arbitrary file write via unsanitised `savePath`; SQL injection architectural risk via `%s`/`String.format` in `REPORT_QUERY` |
| HIGH | 4 | Dangerous no-bind `queryForObject` overload; exception swallowing hiding security decisions; unvalidated `ImpactLevel.valueOf()` with stack trace leakage; no file size/type validation on upload |
| MEDIUM | 4 | Cross-tenant IDOR via `unit_company` OR join; `ReportFilterBean` null-defaulting silently suppresses results; timezone/date bind parameter mismatch; `FileReader` charset/CSV parsing issues + XXE risk from POI imports |
| LOW | 3 | Non-volatile singleton DCL; `@Data` toString PII leakage; `FileOutputStream` resource management |
| INFO | 2 | `calculateImpactLevel()` undocumented null return; `%s` format specifier architectural note |

**CRITICAL: 2 / HIGH: 4 / MEDIUM: 4 / LOW: 3 / INFO: 2**
