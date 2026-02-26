# Pass 1 Audit — DateBetweenFilter / DateBetweenFilterHandler / DateFormatBean / DateUtil

**Files:**
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/querybuilder/filters/DateBetweenFilter.java`
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/querybuilder/filters/DateBetweenFilterHandler.java`
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/bean/DateFormatBean.java`
- `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/util/DateUtil.java`

**Date:** 2026-02-26

---

## Summary

These four files form the date-handling and query-filtering layer used by the application's report system (incident, impact, session, and pre-ops reports). `DateBetweenFilter` is a simple interface declaring `start()`, `end()`, and `timezone()` methods. `DateBetweenFilterHandler` builds parameterized SQL WHERE clauses and binds values via `StatementPreparer`, which wraps `PreparedStatement`. `DateFormatBean` is a Lombok-annotated bean that holds a `SimpleDateFormat` pattern string and renders an example date. `DateUtil` is a broad utility class containing date-parsing, formatting, and timezone-conversion methods used throughout the application.

**Overall risk level: MEDIUM.** The SQL query construction in `DateBetweenFilterHandler` correctly uses `PreparedStatement` placeholders (`?`) and is not vulnerable to SQL injection at this layer. However, several medium and low severity issues exist: a logic defect in `prepareStatement` that binds the timezone parameter unconditionally even in start-only and end-only branches where the SQL template does not include a timezone placeholder (causing runtime `SQLException`); multiple `ParseException` paths that swallow exceptions and silently return `null`, leading to potential `NullPointerException` propagation; unvalidated `SimpleDateFormat` patterns passed into `DateFormatBean.getExample()` and into `DateUtil.formatDate`/`formatDateTime` that could trigger `IllegalArgumentException`; and the use of the system default timezone in `local2utc` which creates environment-dependent and unpredictable date conversion behavior.

---

## Findings

### MEDIUM: Timezone Parameter Mismatch — Incorrect Placeholder Count in Start-Only and End-Only Filter Branches

**File:** `DateBetweenFilterHandler.java` (lines 19–20, 29–31)

**Description:**
`prepareStatement` always binds `filter.timezone()` as the first parameter whenever it is non-null, regardless of which branch of `getQueryFilter()` was taken:

```java
// getQueryFilter() — start-only branch (no timezone placeholder)
if (filterStartOnly()) return String.format(" AND %s >= ?", fieldName);  // 1 placeholder

// getQueryFilter() — end-only branch (no timezone placeholder)
if (filterEndOnly()) return String.format(" AND %s <= ?", fieldName);    // 1 placeholder

// getQueryFilter() — between branch (has timezone placeholder)
if (filterBetweenTwoDates()) return String.format(
    " AND timezone(?, %s at time zone 'UTC')::DATE BETWEEN ? AND ?", fieldName);  // 3 placeholders

// prepareStatement — always adds timezone first if non-null
if(filter.timezone() != null) preparer.addString(filter.timezone());  // ALWAYS bound
if (filter.start() != null)   preparer.addDate(filter.start());
if (filter.end() != null)     preparer.addDate(filter.end());
```

When `filter.timezone()` is non-null and only a start or end date is provided, the SQL template has one `?` but `prepareStatement` tries to bind two parameters (timezone string + date). This causes a `SQLException` at execution time (e.g., `ERROR: The column index is out of range`). Conversely, if the timezone is non-null but neither start nor end is provided, the filter is ignored entirely by `getQueryFilter()` but `prepareStatement` correctly returns early due to `ignoreFilter()`. The real defect affects the single-date (start-only or end-only) path.

**Risk:** In the start-only or end-only path when a timezone is passed in, every report query that uses `DateBetweenFilterHandler` will throw a `SQLException`, potentially causing a denial of service or revealing a stack trace to the end user. More significantly, if this were ever fixed by removing the timezone pre-condition, the timezone value itself could silently be bound at the wrong position, producing incorrect query results rather than an error.

**Recommendation:** The timezone parameter should only be bound in `prepareStatement` when the `filterBetweenTwoDates()` branch is active. Align the binding logic with the SQL template branches:

```java
if (filterBetweenTwoDates()) {
    if (filter.timezone() != null) preparer.addString(filter.timezone());
    preparer.addDate(filter.start());
    preparer.addDate(filter.end());
} else if (filterStartOnly()) {
    preparer.addDate(filter.start());
} else if (filterEndOnly()) {
    preparer.addDate(filter.end());
}
```

---

### MEDIUM: Silent ParseException Swallowing Leads to NullPointerException Propagation

**File:** `DateUtil.java` (lines 36–52, 76–88, 175–186)

**Description:**
Multiple parsing methods silently catch `ParseException` and return `null` or continue with a null `date` variable. The most dangerous instance is `stringToSQLDate` (lines 76–88):

```java
public static java.sql.Date stringToSQLDate(String str_date, String dateFormat) {
    DateFormat formatter = new SimpleDateFormat(dateFormat);
    Date date = null;
    try {
        date = formatter.parse(str_date);
    } catch (ParseException e) {
        System.out.println("Exception :" + e);  // swallowed to stdout only
    }
    dte = new java.sql.Date(Objects.requireNonNull(date).getTime());  // NPE if parse failed
    return dte;
}
```

When `str_date` does not match `dateFormat`, `date` remains `null`, `Objects.requireNonNull` throws a `NullPointerException`, and this propagates as an unhandled runtime exception. Similarly, `stringToDate` (lines 36–52) silently falls through both parse attempts and returns `null`, which can cause a `NullPointerException` in the calling `stringToUTCDate` method when `local2utc` receives null (handled there) but not in `stringToIsoNoTimezone` (line 63) where `df.format(dateObj)` would throw a `NullPointerException` if `dateObj` is null.

`stringToTimestamp` (lines 175–186) and `StringTimeDifference` (lines 188–202) similarly swallow exceptions to `System.out.println` rather than logging through the class's `log` instance and return potentially meaningless zero or null values, masking data errors silently in production.

**Risk:** Malformed date input from users triggers uncaught `NullPointerException` or returns incorrect default values (zero difference, null timestamps), leading to unpredictable application behavior and potential information disclosure via stack traces if exceptions propagate to the Struts error handler.

**Recommendation:** Throw checked exceptions (or return `Optional`) from parsing methods rather than returning `null`. Replace `System.out.println` exception handling with `log.error(...)`. Add a null-check guard in `stringToIsoNoTimezone` before calling `df.format(dateObj)`.

---

### MEDIUM: Unvalidated SimpleDateFormat Pattern in DateFormatBean.getExample()

**File:** `DateFormatBean.java` (lines 23–31)

**Description:**
`getExample()` constructs a `SimpleDateFormat` directly from the `format` field without any validation:

```java
public String getExample() {
    Calendar calendar = Calendar.getInstance();
    // ... calendar setup ...
    return new SimpleDateFormat(format).format(calendar.getTime());
}
```

The `format` field is populated from the database column `format_value` (via `DateFormatDAO`), which in turn is loaded from an admin-editable settings page. An administrator who can write arbitrary format strings to the database (or who exploits another vulnerability to do so) can supply a pattern that causes `SimpleDateFormat` to throw an `IllegalArgumentException` (e.g., a pattern with unquoted invalid letters), crashing the settings page. While the `format_value` source is the database and not a direct HTTP request parameter, this is still a concern when the settings page itself renders these examples.

Additionally, `DateUtil.formatDate(Date, String)` (line 147) and `DateUtil.formatDateTime(Timestamp, String)` (line 153) both pass a caller-supplied `dateFormat` string directly into `new SimpleDateFormat(dateFormat)` without validation. These `dateFormat` values originate from the session (`sessDateFormat`, `sessDateTimeFormat`) which are set from the company's `date_format` database column. While this is not direct user input at request time, the same risk applies if the database value is corrupt or tampered with.

**Risk:** A malformed format pattern causes an `IllegalArgumentException`, breaking date display across all reports and pages that use these methods until the format is corrected. This is a denial-of-service for affected features.

**Recommendation:** Validate format strings against an allowlist of known-good patterns (consistent with `DateFormatDAO.getAll()` which provides the admin's selectable options). Wrap `new SimpleDateFormat(format)` in a try/catch for `IllegalArgumentException` in both `DateFormatBean.getExample()` and the `DateUtil` formatting methods, and return a fallback value or propagate a meaningful application error.

---

### LOW: Timezone String Passed as PreparedStatement Parameter Without Format Validation

**File:** `DateBetweenFilterHandler.java` (line 29); `DateUtil.java` (lines 119, 135, 227–229)

**Description:**
The timezone string from `filter.timezone()` is bound as a `PreparedStatement` string parameter in the PostgreSQL expression `timezone(?, column at time zone 'UTC')::DATE`. Because this value is passed via a parameterized `?` placeholder, it is not vulnerable to SQL injection. However, no validation is performed on the timezone string before it is used. PostgreSQL will return an error for an unrecognized timezone name (e.g., `ERROR: time zone "Invalid/Zone" does not exist`), which propagates as a `SQLException`.

Separately, `DateUtil.getLocalTimestamp` and `DateUtil.getLocalTime` (lines 115–141) pass unvalidated timezone names to `TimeZone.getTimeZone(timezoneName)`. Java's `TimeZone.getTimeZone` silently falls back to GMT for unrecognized names rather than throwing an exception, causing silent incorrect behavior. `DateUtil.utc2Local(Timestamp, String)` (line 227) also calls `TimeZone.getTimeZone(timezone).toZoneId()`, which similarly silently returns UTC for unknown names.

The session-level timezone (`sessTimezone`) originates from `TimezoneDAO.getTimezone(int)` which performs an integer primary-key lookup, meaning it is effectively constrained to database-stored values. However, the `timezone` field in `ReportSearchForm` and its subclasses is directly read from the HTTP request via Struts binding (e.g., `ImpactReportSearchForm.timezone`). The action class for incident/impact reports overwrites this with the session value (`incidentReportSearchForm.setTimezone(timezone)`), but not all action classes do this consistently (see `PreOpsReportSearchForm` which reads `this.timezone` directly from the form).

**Risk:** Unexpected timezone names can cause silent UTC fallback in Java timezone functions, resulting in incorrect date calculations and data filtering that does not match the user's actual timezone. This is a data-integrity risk rather than a direct security risk, since the timezone value is parameterized in SQL.

**Recommendation:** Validate timezone strings against `ZoneId.getAvailableZoneIds()` before use. Ensure all action classes consistently overwrite the form's timezone with the session-stored value rather than relying on the form binding.

---

### LOW: System Default Timezone Dependency in local2utc Conversion

**File:** `DateUtil.java` (lines 214–220)

**Description:**
The private `local2utc` method (called by `stringToUTCDate`) uses `ZoneId.systemDefault()` both to interpret the input date and to define the "local" zone before converting to GMT:

```java
private static Date local2utc(Date date) {
    if (date == null) return null;
    LocalDateTime ldt = LocalDateTime.ofInstant(date.toInstant(), ZoneId.systemDefault());
    ZonedDateTime zdt = ldt.atZone(ZoneId.systemDefault());
    return Date.from(zdt.withZoneSameInstant(ZoneId.of("GMT")).toInstant());
}
```

The conversion is entirely dependent on the JVM's system default timezone at runtime. If the server's JVM timezone differs from the user's expected local timezone (which is a realistic scenario given that timezone is separately passed as a report filter parameter), date boundaries used in report filtering will be silently shifted by the difference. For example, if the server runs UTC but a user submits a date in `America/New_York`, the start/end dates passed to the query will be off by 5 hours, causing incorrect report rows to be included or excluded.

**Risk:** Incorrect date range filtering in all reports (incident, impact, session, pre-ops). Users will see data from the wrong time period. This is a data integrity and functional correctness issue.

**Recommendation:** `local2utc` should accept the user's timezone explicitly (e.g., the `timezone` string available on the filter bean) rather than relying on `ZoneId.systemDefault()`. Alternatively, date strings should be parsed assuming the user's timezone from the outset, and the UTC conversion should use that same timezone.

---

### LOW: parseDateTime Uses Incorrect Minute Format Pattern

**File:** `DateUtil.java` (line 168)

**Description:**
The `parseDateTime` method uses the format string `"yyyy-mm-dd HH:mm:ss"`:

```java
public static Date parseDateTime(String strDate) {
    ...
    final SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-mm-dd HH:mm:ss");
    return dateFormat.parse(strDate);
    ...
}
```

The pattern `mm` in `SimpleDateFormat` represents **minutes**, not months. The correct token for month-of-year is `MM`. As a result, this method cannot correctly parse a date string like `"2024-03-15 10:30:00"` — the `03` would be interpreted as minutes (within the hour), not March, and the parsed date's month field would be determined by some other mechanism (likely defaulting to January). Any consumer of this method will silently receive a `Date` object with a wrong month value, or `null` if the method catches the resulting parse error.

**Risk:** Silent data corruption for any feature that calls `parseDateTime`. Incorrect dates may be stored or used in queries, producing wrong report results.

**Recommendation:** Change the format string from `"yyyy-mm-dd HH:mm:ss"` to `"yyyy-MM-dd HH:mm:ss"`.

---

### LOW: No Date Range Validation — Start Date May Exceed End Date

**File:** `DateBetweenFilterHandler.java` (lines 38–48); action forms (all report search forms)

**Description:**
Neither `DateBetweenFilterHandler` nor any of the action form classes (`IncidentReportSearchForm`, `ImpactReportSearchForm`, `SessionReportSearchForm`, `PreOpsReportSearchForm`) validate that `start` is before or equal to `end`. The `filterBetweenTwoDates()` guard only checks for non-null values:

```java
private boolean filterBetweenTwoDates() {
    return filter.start() != null && filter.end() != null;
}
```

If a user submits a start date later than the end date, the resulting SQL `BETWEEN ? AND ?` clause with a reversed range will return zero rows on most databases (PostgreSQL `BETWEEN` requires `low <= high`), producing silently empty report results with no error message to the user.

**Risk:** Confusing user experience and potential for users to believe their report data has been deleted or is missing. Not a direct security risk, but a data-access robustness issue.

**Recommendation:** Add validation (either in the action form's `validate()` method or in `DateBetweenFilterHandler`) to ensure `start` is not after `end`, and return an appropriate user-facing error message.

---

### INFO: SQL Injection Not Present — PreparedStatement Used Correctly

**File:** `DateBetweenFilterHandler.java` (lines 17–24, 27–32)

**Description:**
All date and timezone values are bound through `PreparedStatement` parameters. The `getQueryFilter()` method inserts only the `fieldName` value into the SQL template string, and `fieldName` originates from hardcoded string literals in the query classes (`"impact_time"`, `"event_time"`, `"session_start_time"`, `"check_date_time"`), not from user input. The `StatementPreparer` wrapper correctly delegates to `PreparedStatement.setDate()` and `PreparedStatement.setString()`.

**Risk:** No SQL injection risk in this component.

**Recommendation:** No action required for this finding. Maintain this pattern throughout the codebase.

---

### INFO: Logging Inconsistency — ParseExceptions Logged to System.out Rather Than Log4j

**File:** `DateUtil.java` (lines 48, 84, 184, 199)

**Description:**
Several `catch (ParseException e)` blocks use `System.out.println("Exception :" + e)` instead of the `log` instance declared at line 27:

```java
private static Logger log = InfoLogger.getLogger("com.util.DateUtil");
```

This means parse failures are not captured by the application's logging infrastructure (Log4j), are invisible in production log aggregation tools, and cannot be filtered or monitored by operations staff.

**Risk:** Operational blind spot. Failed date parsing in production will not generate alerts or appear in logs, making diagnosis of data-related problems significantly harder.

**Recommendation:** Replace all `System.out.println` in exception handlers with `log.warn(...)` or `log.error(...)` calls.

---

## Finding Count

- CRITICAL: 0
- HIGH: 0
- MEDIUM: 3
- LOW: 4
- INFO: 2
