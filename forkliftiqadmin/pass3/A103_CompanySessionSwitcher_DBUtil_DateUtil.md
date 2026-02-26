# Pass 3 Documentation Audit — Agent A103
**Audit run:** 2026-02-26-01
**Files audited:**
- `util/CompanySessionSwitcher.java`
- `util/DBUtil.java`
- `util/DateUtil.java`

---

## 1. Reading Evidence

### 1.1 CompanySessionSwitcher.java

**Class:** `CompanySessionSwitcher` — line 15

**Fields:** none declared

**Methods:**

| Method | Line | Visibility | Static |
|---|---|---|---|
| `UpdateCompanySessionAttributes(CompanyBean, HttpServletRequest, HttpSession)` | 17 | `public` | yes |

No Javadoc present anywhere in file.

---

### 1.2 DBUtil.java

**Class:** `DBUtil` — line 21

**Fields:**

| Field | Type | Line | Visibility |
|---|---|---|---|
| `databaseName` | `String` | 22 | `private static` |

**Methods:**

| Method | Line | Visibility | Static | Notes |
|---|---|---|---|---|
| `getConnection()` | 24 | `public` | yes | |
| `getConnection(boolean autoCommit)` | 28 | `public` | yes | |
| `ensureDatabaseNameIsSet()` | 43 | `private` | yes | |
| `closeConnection(Connection conn)` | 57 | `public` | yes | `@Deprecated` |
| `queryForObjects(String, PreparedStatementHandler, ResultMapper<T>)` | 61 | `public` | yes | |
| `queryForObjectsWithRowHandler(String, PreparedStatementHandler, RowHandler<T>)` | 84 | `public` | yes | |
| `queryForObjects(Connection, String, PreparedStatementHandler, ResultMapper<T>)` | 107 | `public` | yes | overload accepting external `Connection` |
| `queryForObject(String, ResultMapper<T>)` | 128 | `public` | yes | |
| `queryForObject(String, PreparedStatementHandler, ResultMapper<T>)` | 148 | `public` | yes | |
| `queryForObject(Connection, String, PreparedStatementHandler, ResultMapper<T>)` | 172 | `public` | yes | overload accepting external `Connection` |
| `updateObject(Connection, String, PreparedStatementHandler)` | 195 | `public` | yes | |
| `updateObject(String, PreparedStatementHandler)` | 211 | `public` | yes | |
| `executeStatementWithRollback(String, PreparedStatementHandler)` | 228 | `public` | yes | |

**Nested interfaces:**

| Interface | Line |
|---|---|
| `PreparedStatementHandler` | 247 |
| `ResultMapper<T>` | 251 |
| `RowHandler<T>` | 255 |

No Javadoc present anywhere in file.

---

### 1.3 DateUtil.java

**Class:** `DateUtil` — line 26

**Fields:**

| Field | Type | Line | Visibility |
|---|---|---|---|
| `log` | `Logger` | 27 | `private static` |

**Methods:**

| Method | Line | Visibility | Static | Notes |
|---|---|---|---|---|
| `stringToDate(String, String)` | 29 | `private` | yes | |
| `stringToUTCDate(String, String)` | 55 | `public` | yes | |
| `stringToIsoNoTimezone(String, String)` | 60 | `public` | yes | |
| `getDaysDate(Date, int)` | 66 | `public` | yes | |
| `dateToString(Date)` | 71 | `public` | yes | |
| `stringToSQLDate(String, String)` | 76 | `public` | yes | |
| `sqlDateToString(java.sql.Date, String)` | 90 | `public` | yes | |
| `sqlTimestampToString(java.sql.Timestamp, String)` | 95 | `public` | yes | |
| `getStartDate(Date, String)` | 100 | `public` | yes | |
| `getLocalTimestamp(String, Locale)` | 115 | `public` | yes | |
| `getLocalTime(String, Locale)` | 131 | `public` | yes | |
| `formatDate(Date)` | 143 | `public` | yes | one-arg overload |
| `formatDate(Date, String)` | 147 | `public` | yes | two-arg overload |
| `formatDateTime(Timestamp, String)` | 153 | `public` | yes | |
| `parseDate(String)` | 159 | `public` | yes | |
| `parseDateTime(String)` | 164 | `public` | yes | |
| `stringToTimestamp(String)` | 175 | `public` | yes | |
| `StringTimeDifference(String, String, TimeUnit, String)` | 188 | `public` | yes | |
| `GetDateNow()` | 204 | `public` | yes | |
| `toDate(LocalDate)` | 210 | `public` | yes | |
| `local2utc(Date)` | 214 | `private` | yes | |
| `utc2Local(Timestamp)` | 222 | `public` | yes | |
| `utc2Local(Timestamp, String)` | 227 | `public` | yes | overload with timezone |
| `getDateFormatFromDateTimeFormat(String)` | 233 | `public` | yes | |

No Javadoc present anywhere in file.

---

## 2. Findings

### A103-1 — No class-level Javadoc: CompanySessionSwitcher
**Severity:** LOW
**File:** `util/CompanySessionSwitcher.java`, line 15
**Detail:** The class `CompanySessionSwitcher` has no class-level Javadoc comment. Its purpose (populating session and request attributes when an admin switches the active company context) is non-trivial and would benefit from a description.

---

### A103-2 — Undocumented non-trivial public method: `UpdateCompanySessionAttributes`
**Severity:** MEDIUM
**File:** `util/CompanySessionSwitcher.java`, line 17
**Detail:** `public static void UpdateCompanySessionAttributes(CompanyBean, HttpServletRequest, HttpSession)` has no Javadoc whatsoever. The method performs multiple significant side-effects: it resolves a `TimezoneBean`, sets 10+ session/request attributes covering company identity, date/time format, timezone, driver counts, unit counts, fleet-check counts, impact counts, expiring-training lists, and dealer role flag. None of this is documented. Missing `@param` tags for all three parameters and missing documentation of the checked `Exception` that is declared thrown.

---

### A103-3 — No class-level Javadoc: DBUtil
**Severity:** LOW
**File:** `util/DBUtil.java`, line 21
**Detail:** The class `DBUtil` has no class-level Javadoc. It is a central database utility class used throughout the application; its design (JNDI datasource lookup, dynamic database-name resolution from JVM arguments, nested functional interfaces) warrants a class-level description.

---

### A103-4 — Undocumented non-trivial public method: `getConnection()`
**Severity:** MEDIUM
**File:** `util/DBUtil.java`, line 24
**Detail:** `public static Connection getConnection()` has no Javadoc. It delegates to `getConnection(true)`, meaning it always opens a connection with `autoCommit=true`. Callers cannot discover this default without reading the implementation. Missing `@return` and `@throws SQLException`.

---

### A103-5 — Undocumented non-trivial public method: `getConnection(boolean)`
**Severity:** MEDIUM
**File:** `util/DBUtil.java`, line 28
**Detail:** `public static Connection getConnection(boolean autoCommit)` has no Javadoc. The method performs JNDI lookup under `java:/comp/env`, wraps the raw connection in a `ConnectionSpy` (log4jdbc instrumentation), and honours the autoCommit flag. None of this behaviour is documented. Missing `@param autoCommit`, `@return`, `@throws SQLException`.

---

### A103-6 — Undocumented deprecated public method: `closeConnection`
**Severity:** LOW
**File:** `util/DBUtil.java`, line 57
**Detail:** `@Deprecated public static void closeConnection(Connection)` has no Javadoc and no `@deprecated` tag explaining the deprecation reason or what callers should use instead (i.e., `DbUtils.closeQuietly` directly). Missing `@param conn` and a `@deprecated` migration note.

---

### A103-7 — Undocumented non-trivial public method: `queryForObjects(String, PreparedStatementHandler, ResultMapper<T>)`
**Severity:** MEDIUM
**File:** `util/DBUtil.java`, line 61
**Detail:** No Javadoc. This is the primary query method; it opens its own connection, uses a caller-supplied `PreparedStatementHandler` to bind parameters, maps each row with a `ResultMapper`, swallows `SQLException` internally (printing to stderr) and returns an empty list on error. The error-swallowing is a significant behavioural contract that is completely undocumented. Missing `@param` tags for all three parameters, `@return`, `@throws` (declared but misleading — see A103-15).

---

### A103-8 — Undocumented non-trivial public method: `queryForObjectsWithRowHandler`
**Severity:** MEDIUM
**File:** `util/DBUtil.java`, line 84
**Detail:** No Javadoc. Differs from `queryForObjects` in that it delegates entire `ResultSet` traversal to a `RowHandler` rather than iterating row-by-row with a `ResultMapper`. This distinction is important for callers. Missing `@param` tags for all three parameters, `@return`, `@throws`.

---

### A103-9 — Undocumented non-trivial public method: `queryForObjects(Connection, String, PreparedStatementHandler, ResultMapper<T>)`
**Severity:** MEDIUM
**File:** `util/DBUtil.java`, line 107
**Detail:** No Javadoc. This overload accepts a caller-managed `Connection` (the connection is NOT closed in the `finally` block, only the statement and result set are). This non-obvious lifecycle difference versus the no-`Connection` overload (line 61) is entirely undocumented. Missing `@param` tags for all four parameters, `@return`, `@throws`.

---

### A103-10 — Undocumented non-trivial public method: `queryForObject(String, ResultMapper<T>)`
**Severity:** MEDIUM
**File:** `util/DBUtil.java`, line 128
**Detail:** No Javadoc. Returns `Optional.empty()` if no row found, throws `SQLException` with message "Unique result expected, got more than one" when more than one row is returned. The uniqueness contract is significant. Missing `@param` tags, `@return`, `@throws`.

---

### A103-11 — Undocumented non-trivial public method: `queryForObject(String, PreparedStatementHandler, ResultMapper<T>)`
**Severity:** MEDIUM
**File:** `util/DBUtil.java`, line 148
**Detail:** No Javadoc. Same uniqueness contract as A103-10. Missing `@param` tags, `@return`, `@throws`.

---

### A103-12 — Undocumented non-trivial public method: `queryForObject(Connection, String, PreparedStatementHandler, ResultMapper<T>)`
**Severity:** MEDIUM
**File:** `util/DBUtil.java`, line 172
**Detail:** No Javadoc. Same uniqueness contract. Same caller-managed connection lifecycle as A103-9 (connection not closed). Missing `@param` tags, `@return`, `@throws`.

---

### A103-13 — Undocumented non-trivial public method: `updateObject(Connection, String, PreparedStatementHandler)`
**Severity:** MEDIUM
**File:** `util/DBUtil.java`, line 195
**Detail:** No Javadoc. Returns `-1` on caught `SQLException` (which is swallowed, printed to stderr) rather than propagating the error. This silent-failure return value is undocumented. Missing `@param` tags, `@return`, `@throws`.

---

### A103-14 — Undocumented non-trivial public method: `updateObject(String, PreparedStatementHandler)`
**Severity:** MEDIUM
**File:** `util/DBUtil.java`, line 211
**Detail:** No Javadoc. Same silent-failure / `-1` return contract as A103-13. Missing `@param` tags, `@return`, `@throws`.

---

### A103-15 — Inaccurate `throws` declaration on multiple DBUtil query methods
**Severity:** MEDIUM
**File:** `util/DBUtil.java`, lines 61, 84, 107, 128, 148, 172, 195, 211
**Detail:** All these methods declare `throws SQLException` yet their `catch (SQLException e)` blocks swallow the exception (calling `e.printStackTrace()` only) and return a default value (`empty list`, `Optional.empty()`, or `-1`). Callers reading the signature will believe a `SQLException` is thrown on error, but no SQL exception is ever surfaced from these methods in practice. The `throws` clause is therefore misleading. Note that `executeStatementWithRollback` (line 228) is the exception — it correctly re-throws after rollback. This inaccuracy affects documented API contract understanding for all callers.

---

### A103-16 — Undocumented non-trivial public method: `executeStatementWithRollback`
**Severity:** MEDIUM
**File:** `util/DBUtil.java`, line 228
**Detail:** No Javadoc. This is the only DBUtil method that correctly propagates `SQLException` (all others swallow it). It opens its own connection with `autoCommit=false`, executes the update, commits, and rolls back on error before re-throwing. This transactional behaviour is undocumented. Missing `@param` tags, `@throws SQLException`.

---

### A103-17 — No class-level Javadoc: DateUtil
**Severity:** LOW
**File:** `util/DateUtil.java`, line 26
**Detail:** The class `DateUtil` has no class-level Javadoc.

---

### A103-18 — Undocumented non-trivial public method: `stringToUTCDate`
**Severity:** MEDIUM
**File:** `util/DateUtil.java`, line 55
**Detail:** No Javadoc. The method parses a date string using the supplied format then converts from the JVM's local timezone to UTC. The timezone-conversion behaviour is important for callers. Missing `@param str_date`, `@param format`, `@return`, null-return behaviour (returns `null` when `str_date` is `null`) is undocumented.

---

### A103-19 — Undocumented non-trivial public method: `stringToIsoNoTimezone`
**Severity:** MEDIUM
**File:** `util/DateUtil.java`, line 60
**Detail:** No Javadoc. Converts a date string from `dateFormat` to `yyyy-MM-dd'T'HH:mm:ss` without any timezone indicator. The name "NoTimezone" is ambiguous — it could mean the output lacks a timezone offset (correct) or that input timezone is ignored. Missing `@param date`, `@param dateFormat`, `@return`.

---

### A103-20 — Undocumented non-trivial public method: `getDaysDate`
**Severity:** MEDIUM
**File:** `util/DateUtil.java`, line 66
**Detail:** No Javadoc. Returns a `Date` that is `days` days *before* the input date (subtraction, not addition). The direction of offset is undocumented and counterintuitive from the name alone. Missing `@param date`, `@param days`, `@return`.

---

### A103-21 — Undocumented trivial public method: `dateToString`
**Severity:** LOW
**File:** `util/DateUtil.java`, line 71
**Detail:** No Javadoc. Formats a `Date` to `"dd/MM/yyyy"` with a hardcoded format. The hardcoded format is not documented. Missing `@param date`, `@return`.

---

### A103-22 — Undocumented non-trivial public method: `stringToSQLDate`
**Severity:** MEDIUM
**File:** `util/DateUtil.java`, line 76
**Detail:** No Javadoc. Will throw `NullPointerException` (via `Objects.requireNonNull`) if parsing fails — the `ParseException` is caught and printed but `date` remains `null`, causing the NPE on line 86. This is a hidden runtime failure mode. Missing `@param str_date`, `@param dateFormat`, `@return`, `@throws`.

---

### A103-23 — Undocumented trivial public method: `sqlDateToString`
**Severity:** LOW
**File:** `util/DateUtil.java`, line 90
**Detail:** No Javadoc. Returns `""` for `null` input. Missing `@param date`, `@param dateFormat`, `@return`.

---

### A103-24 — Undocumented trivial public method: `sqlTimestampToString`
**Severity:** LOW
**File:** `util/DateUtil.java`, line 95
**Detail:** No Javadoc. Returns `""` for `null` input. Missing `@param timestamp`, `@param dateTimeFormat`, `@return`.

---

### A103-25 — Undocumented non-trivial public method: `getStartDate`
**Severity:** MEDIUM
**File:** `util/DateUtil.java`, line 100
**Detail:** No Javadoc. Computes a start date by subtracting a period from `date` based on a `freqency` string (`"Daily"` → -1 day, `"Weekly"` → -7 days, `"Monthly"` → -1 month, default → -1 day). The default-fallback behaviour (silently treating unknown frequencies as daily) is not documented. Parameter name `freqency` is a typo of `frequency`. Missing `@param date`, `@param freqency`, `@return`.

---

### A103-26 — Undocumented non-trivial public method: `getLocalTimestamp`
**Severity:** MEDIUM
**File:** `util/DateUtil.java`, line 115
**Detail:** No Javadoc. Returns a `Timestamp` representing the current wall-clock time in the specified timezone, expressed as a naive (no-zone) value that appears local. Falls back to `RuntimeConf.DEFAUTL_TIMEZONE` when `timezoneName` is null or blank (note the typo in `DEFAUTL_TIMEZONE`). Missing `@param timezoneName`, `@param clientLocale`, `@return`, `@throws Exception`.

---

### A103-27 — Undocumented non-trivial public method: `getLocalTime`
**Severity:** MEDIUM
**File:** `util/DateUtil.java`, line 131
**Detail:** No Javadoc. Same timezone-lookup and fallback behaviour as `getLocalTimestamp` but returns a `Date` instead of a `Timestamp`. Missing `@param timezoneName`, `@param clientLocale`, `@return`, `@throws Exception`.

---

### A103-28 — Undocumented trivial public method: `formatDate(Date)`
**Severity:** LOW
**File:** `util/DateUtil.java`, line 143
**Detail:** No Javadoc. Single-arg overload hardcodes format `"yyyy-MM-dd"`. Missing `@param date`, `@return`.

---

### A103-29 — Undocumented trivial public method: `formatDate(Date, String)`
**Severity:** LOW
**File:** `util/DateUtil.java`, line 147
**Detail:** No Javadoc. Returns `null` for null input date. Missing `@param date`, `@param dateFormat`, `@return`.

---

### A103-30 — Undocumented trivial public method: `formatDateTime`
**Severity:** LOW
**File:** `util/DateUtil.java`, line 153
**Detail:** No Javadoc. Returns `""` for null timestamp. Missing `@param timestamp`, `@param format`, `@return`.

---

### A103-31 — Undocumented non-trivial public method: `parseDate`
**Severity:** MEDIUM
**File:** `util/DateUtil.java`, line 159
**Detail:** No Javadoc. Parses using the hardcoded format `"yyyy-MM-dd"`. Missing `@param strDate`, `@return`, `@throws Exception`.

---

### A103-32 — Inaccurate format string in `parseDateTime`
**Severity:** HIGH
**File:** `util/DateUtil.java`, line 168
**Detail:** The format string used is `"yyyy-mm-dd HH:mm:ss"`. The second `mm` token represents *minutes*, not *months* — the correct token for months is `MM`. As a result this method silently misparses the month component of any date string, returning an incorrect `Date` (month is always January) for all valid inputs. Callers relying on this method to parse date-time strings will receive wrong results without any error or exception. The method has no Javadoc and the bug is entirely invisible from the method's public signature.

---

### A103-33 — Undocumented non-trivial public method: `parseDateTime`
**Severity:** MEDIUM
**File:** `util/DateUtil.java`, line 164
**Detail:** No Javadoc. Returns `null` on empty input or parse failure rather than throwing. Missing `@param strDate`, `@return`.

---

### A103-34 — Undocumented non-trivial public method: `stringToTimestamp`
**Severity:** MEDIUM
**File:** `util/DateUtil.java`, line 175
**Detail:** No Javadoc. Expects input strictly in `"yyyy/MM/dd HH:mm:ss"` format (using `/` as date separator). Returns `null` on parse failure (exception swallowed). Missing `@param str_date`, `@return`.

---

### A103-35 — Undocumented non-trivial public method: `StringTimeDifference`
**Severity:** MEDIUM
**File:** `util/DateUtil.java`, line 188
**Detail:** No Javadoc. Computes `time1 - time2` (not `|time1 - time2|`), so result can be negative if `time1` is earlier than `time2`. Returns `0` on parse failure (exception swallowed and `diffInMillies` remains initialised to `0`). The sign convention and silent-zero-on-error behaviour are not documented. Missing `@param time1`, `@param time2`, `@param timeUnit`, `@param format`, `@return`.

---

### A103-36 — Undocumented trivial public method: `GetDateNow`
**Severity:** LOW
**File:** `util/DateUtil.java`, line 204
**Detail:** No Javadoc. Returns current date/time in `"dd/MM/yyyy HH:mm:ss"` using the JVM's default timezone. Missing `@return`.

---

### A103-37 — Undocumented non-trivial public method: `toDate`
**Severity:** MEDIUM
**File:** `util/DateUtil.java`, line 210
**Detail:** No Javadoc. Converts `LocalDate` to `Date` at start-of-day in the JVM's default timezone. Missing `@param localDate`, `@return`.

---

### A103-38 — Undocumented non-trivial public method: `utc2Local(Timestamp)`
**Severity:** MEDIUM
**File:** `util/DateUtil.java`, line 222
**Detail:** No Javadoc. Converts a UTC `Timestamp` to the JVM's default local timezone. Missing `@param timestamp`, `@return`.

---

### A103-39 — Undocumented non-trivial public method: `utc2Local(Timestamp, String)`
**Severity:** MEDIUM
**File:** `util/DateUtil.java`, line 227
**Detail:** No Javadoc. Converts a UTC `Timestamp` to an explicit named timezone. Missing `@param timestamp`, `@param timezone`, `@return`.

---

### A103-40 — Undocumented non-trivial public method: `getDateFormatFromDateTimeFormat`
**Severity:** MEDIUM
**File:** `util/DateUtil.java`, line 233
**Detail:** No Javadoc. Extracts the date-only portion of a combined date-time format string by returning everything before the first space. If there is no space the entire string is returned unchanged. Missing `@param dateTimeFormat`, `@return`.

---

## 3. Summary Table

| Finding | File | Line(s) | Severity | Description |
|---|---|---|---|---|
| A103-1 | CompanySessionSwitcher.java | 15 | LOW | No class-level Javadoc |
| A103-2 | CompanySessionSwitcher.java | 17 | MEDIUM | `UpdateCompanySessionAttributes` undocumented |
| A103-3 | DBUtil.java | 21 | LOW | No class-level Javadoc |
| A103-4 | DBUtil.java | 24 | MEDIUM | `getConnection()` undocumented |
| A103-5 | DBUtil.java | 28 | MEDIUM | `getConnection(boolean)` undocumented |
| A103-6 | DBUtil.java | 57 | LOW | `closeConnection` deprecated without `@deprecated` note |
| A103-7 | DBUtil.java | 61 | MEDIUM | `queryForObjects(String,…)` undocumented |
| A103-8 | DBUtil.java | 84 | MEDIUM | `queryForObjectsWithRowHandler` undocumented |
| A103-9 | DBUtil.java | 107 | MEDIUM | `queryForObjects(Connection,…)` undocumented; connection lifecycle undocumented |
| A103-10 | DBUtil.java | 128 | MEDIUM | `queryForObject(String, ResultMapper)` undocumented |
| A103-11 | DBUtil.java | 148 | MEDIUM | `queryForObject(String, Handler, Mapper)` undocumented |
| A103-12 | DBUtil.java | 172 | MEDIUM | `queryForObject(Connection,…)` undocumented |
| A103-13 | DBUtil.java | 195 | MEDIUM | `updateObject(Connection,…)` undocumented; silent -1 return |
| A103-14 | DBUtil.java | 211 | MEDIUM | `updateObject(String,…)` undocumented; silent -1 return |
| A103-15 | DBUtil.java | 61,84,107,128,148,172,195,211 | MEDIUM | `throws SQLException` declared but exception is swallowed — misleading signature |
| A103-16 | DBUtil.java | 228 | MEDIUM | `executeStatementWithRollback` undocumented |
| A103-17 | DateUtil.java | 26 | LOW | No class-level Javadoc |
| A103-18 | DateUtil.java | 55 | MEDIUM | `stringToUTCDate` undocumented |
| A103-19 | DateUtil.java | 60 | MEDIUM | `stringToIsoNoTimezone` undocumented |
| A103-20 | DateUtil.java | 66 | MEDIUM | `getDaysDate` undocumented; subtracts, not adds |
| A103-21 | DateUtil.java | 71 | LOW | `dateToString` undocumented trivial method |
| A103-22 | DateUtil.java | 76 | MEDIUM | `stringToSQLDate` undocumented; hidden NPE risk |
| A103-23 | DateUtil.java | 90 | LOW | `sqlDateToString` undocumented trivial method |
| A103-24 | DateUtil.java | 95 | LOW | `sqlTimestampToString` undocumented trivial method |
| A103-25 | DateUtil.java | 100 | MEDIUM | `getStartDate` undocumented; silent default fallback |
| A103-26 | DateUtil.java | 115 | MEDIUM | `getLocalTimestamp` undocumented |
| A103-27 | DateUtil.java | 131 | MEDIUM | `getLocalTime` undocumented |
| A103-28 | DateUtil.java | 143 | LOW | `formatDate(Date)` undocumented trivial method |
| A103-29 | DateUtil.java | 147 | LOW | `formatDate(Date,String)` undocumented trivial method |
| A103-30 | DateUtil.java | 153 | LOW | `formatDateTime` undocumented trivial method |
| A103-31 | DateUtil.java | 159 | MEDIUM | `parseDate` undocumented |
| A103-32 | DateUtil.java | 168 | HIGH | `parseDateTime`: format `"yyyy-mm-dd"` uses `mm` (minutes) instead of `MM` (months) — always returns wrong month |
| A103-33 | DateUtil.java | 164 | MEDIUM | `parseDateTime` undocumented; null-on-failure undocumented |
| A103-34 | DateUtil.java | 175 | MEDIUM | `stringToTimestamp` undocumented; null-on-failure undocumented |
| A103-35 | DateUtil.java | 188 | MEDIUM | `StringTimeDifference` undocumented; sign convention and zero-on-error undocumented |
| A103-36 | DateUtil.java | 204 | LOW | `GetDateNow` undocumented trivial method |
| A103-37 | DateUtil.java | 210 | MEDIUM | `toDate` undocumented |
| A103-38 | DateUtil.java | 222 | MEDIUM | `utc2Local(Timestamp)` undocumented |
| A103-39 | DateUtil.java | 227 | MEDIUM | `utc2Local(Timestamp,String)` undocumented |
| A103-40 | DateUtil.java | 233 | MEDIUM | `getDateFormatFromDateTimeFormat` undocumented |

**Totals:** 1 HIGH, 25 MEDIUM, 14 LOW
