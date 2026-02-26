# Pass 2 — Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A103
**Date:** 2026-02-26
**Scope:** CharsetEncodingFilter, CompanySessionSwitcher, DateUtil

---

## Test Directory Grep Summary

| Class Name | Matches in `src/test/java/` |
|---|---|
| `CharsetEncodingFilter` | 0 |
| `CompanySessionSwitcher` | 0 |
| `DateUtil` | 0 |

**Result:** No test class or import reference for any of the three audited classes exists anywhere under the test source root. The only test files present are:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

---

## Source File Evidence

### 1. CharsetEncodingFilter
**File:** `src/main/java/com/util/CharsetEncodingFilter.java`

**Fields:**

| Field | Line |
|---|---|
| `config` (private FilterConfig) | 7 |
| `defaultEncode` (private String, default "UTF-8") | 8 |

**Methods:**

| Method | Line |
|---|---|
| `init(FilterConfig config)` | 10 |
| `destroy()` | 16 |
| `doFilter(ServletRequest, ServletResponse, FilterChain)` | 19 |

**Deployment context:** Registered in `web.xml` mapped to `/*` (all requests). No `init-param` for `Charset` is configured in `web.xml` — the default `"UTF-8"` path is always exercised at runtime.

---

### 2. CompanySessionSwitcher
**File:** `src/main/java/com/util/CompanySessionSwitcher.java`

**Fields:** None (stateless utility class).

**Methods:**

| Method | Line |
|---|---|
| `UpdateCompanySessionAttributes(CompanyBean, HttpServletRequest, HttpSession)` | 17 |

**Session attributes set (lines 27–44):**

| Attribute Key | Value Source | Line |
|---|---|---|
| `sessCompId` | `company.getId()` | 27 |
| `currentCompany` | `company.getId()` | 29 |
| `sessCompName` | `company.getName()` | 30 |
| `sessDateTimeFormat` | `company.getDateFormat()` | 31 |
| `sessDateFormat` | `DateUtil.getDateFormatFromDateTimeFormat(dateTimeFormat)` | 32 |
| `timezoneId` | `tzone.getId()` | 33 |
| `sessTimezone` | `tzone.getZone()` | 34 |
| `arrUnit` | `UnitDAO.getInstance().getUnitNameByComp(comp_id, true)` | 35 |
| `accountAction` | hardcoded `"update"` | 42 |
| `isDealer` | `LoginDAO.isAuthority(comp_id, RuntimeConf.ROLE_DEALER)` | 43 |
| `arrComp` | `CompanyDAO.getInstance().getCompanyByCompId(comp_id)` | 44 |

**Request attributes set (lines 37–41):**

| Attribute Key | Value Source | Line |
|---|---|---|
| `totalDriver` | `DriverDAO.getTotalDriverByID(comp_id, true, tzone.getZone())` | 37 |
| `totalUnit` | `UnitDAO.getTotalUnitByID(comp_id, true)` | 38 |
| `totalFleetCheck` | `ReportService.getInstance().countPreOpsCompletedToday(...)` | 39 |
| `arrExpiringTrainings` | `DriverDAO.getInstance().getExpiringTrainings(comp_id, dateFormat)` | 40 |
| `totalImpactToday` | `ReportService.getInstance().countImpactsToday(...)` | 41 |

**Callers:** `LoginAction.java:68`, `SwitchCompanyAction.java:38`

---

### 3. DateUtil
**File:** `src/main/java/com/util/DateUtil.java`

**Fields:**

| Field | Line |
|---|---|
| `log` (private static Logger) | 27 |

**Methods:**

| Method | Visibility | Line |
|---|---|---|
| `stringToDate(String, String)` | private static | 29 |
| `stringToUTCDate(String, String)` | public static | 55 |
| `stringToIsoNoTimezone(String, String)` | public static | 60 |
| `getDaysDate(Date, int)` | public static | 66 |
| `dateToString(Date)` | public static | 71 |
| `stringToSQLDate(String, String)` | public static | 76 |
| `sqlDateToString(java.sql.Date, String)` | public static | 90 |
| `sqlTimestampToString(java.sql.Timestamp, String)` | public static | 95 |
| `getStartDate(Date, String)` | public static | 100 |
| `getLocalTimestamp(String, Locale)` | public static | 115 |
| `getLocalTime(String, Locale)` | public static | 131 |
| `formatDate(Date)` | public static | 143 |
| `formatDate(Date, String)` | public static | 147 |
| `formatDateTime(Timestamp, String)` | public static | 153 |
| `parseDate(String)` | public static | 159 |
| `parseDateTime(String)` | public static | 164 |
| `stringToTimestamp(String)` | public static | 175 |
| `StringTimeDifference(String, String, TimeUnit, String)` | public static | 188 |
| `GetDateNow()` | public static | 204 |
| `toDate(LocalDate)` | public static | 210 |
| `local2utc(Date)` | private static | 214 |
| `utc2Local(Timestamp)` | public static | 222 |
| `utc2Local(Timestamp, String)` | public static | 227 |
| `getDateFormatFromDateTimeFormat(String)` | public static | 233 |

---

## Findings

### CharsetEncodingFilter

---

**A103-1 | Severity: HIGH**
`CharsetEncodingFilter` has zero test coverage. There is no test class for this filter anywhere in the test source tree. All three lifecycle methods (`init`, `destroy`, `doFilter`) are completely untested. Given that this filter intercepts every request in the application (`url-pattern: /*`), a regression in encoding behaviour would affect all form submissions and multi-byte character handling across the entire application.

---

**A103-2 | Severity: HIGH**
The `init` method branch for a non-null `Charset` init-param (line 13: `defaultEncode = config.getInitParameter("Charset")`) is untested. The currently deployed `web.xml` does not configure this parameter, meaning only the default `"UTF-8"` path executes in production. The configurable-charset branch is therefore dead in the current deployment and entirely untested, creating a silent risk if the `web.xml` is later updated to configure an alternate charset.

---

**A103-3 | Severity: MEDIUM**
The `destroy` method (line 16) sets `config = null` but there is no test verifying that the field is actually nulled. If `doFilter` were called after `destroy` it would encounter a null `config` reference; because `doFilter` does not read `config` directly this is benign today, but the absence of a lifecycle teardown test leaves the correctness contract unverified.

---

**A103-4 | Severity: MEDIUM**
There is no test verifying that `doFilter` correctly propagates the `chain.doFilter(srequest, response)` call. A mock-based test should assert that the filter chain is invoked exactly once with the encoding-set request, and that the encoding applied to the request equals `defaultEncode`. Neither assertion is made anywhere.

---

**A103-5 | Severity: LOW**
The filter does not guard against a null or empty string value returned by `config.getInitParameter("Charset")`. If the init-param is present in `web.xml` but set to an empty string, `setCharacterEncoding("")` will be called on every request. There is no test covering this edge case.

---

### CompanySessionSwitcher

---

**A103-6 | Severity: CRITICAL**
`CompanySessionSwitcher.UpdateCompanySessionAttributes` has zero test coverage. This method is the sole code path that populates the core session identity attributes (`sessCompId`, `currentCompany`, `sessCompName`, `sessDateTimeFormat`, `sessDateFormat`, `timezoneId`, `sessTimezone`, `accountAction`, `isDealer`, `arrComp`) for every authenticated user session. It is called unconditionally from both `LoginAction` (line 68) and `SwitchCompanyAction` (line 38). A defect here silently corrupts session state for all users.

---

**A103-7 | Severity: CRITICAL**
The method writes identical data to two separate session keys — `sessCompId` (line 27) and `currentCompany` (line 29) — both sourced from `company.getId()`. There is no test asserting that both keys are set and that they hold the same value. If one of these lines were removed or the key names drifted, downstream JSPs and actions reading either key would silently receive stale or null data. The duplication itself may be an existing bug (one key is redundant), but it is not documented and is entirely untested.

---

**A103-8 | Severity: CRITICAL**
`session.setAttribute("accountAction", "update")` is hardcoded (line 42). This value is set unconditionally during both login and company switch. There is no test verifying this value is present after the call, and no test verifying it does not inadvertently overwrite a previously set value from a different code path. If the consuming JSPs/actions branch on this attribute the hardcoded string becomes a correctness invariant with no automated guard.

---

**A103-9 | Severity: HIGH**
The `TimezoneDAO.getTimezone(Integer.parseInt(timezone))` call (line 26) will throw `NumberFormatException` if `company.getTimezone()` returns a non-numeric string (e.g., null, empty string, or a named timezone string). There is no null guard before `Integer.parseInt`. There is no test exercising this failure path, and the method's `throws Exception` declaration means the exception will propagate to `LoginAction`/`SwitchCompanyAction`, both of which declare `throws Exception` and thus rely on the global `web.xml` error page — a silent failure visible only as a redirect to `/error/error.html`.

---

**A103-10 | Severity: HIGH**
`DateUtil.getDateFormatFromDateTimeFormat(dateTimeFormat)` is called at line 23 with `dateTimeFormat` sourced directly from `company.getDateFormat()` (line 22). There is no null check on `dateTimeFormat` before the call. If `company.getDateFormat()` returns null, `getDateFormatFromDateTimeFormat` will throw a `NullPointerException` at `dateTimeFormat.contains(" ")` (line 234 of DateUtil). No test covers this null-propagation path from `CompanyBean` through to `UpdateCompanySessionAttributes`.

---

**A103-11 | Severity: HIGH**
Five request attributes (`totalDriver`, `totalUnit`, `totalFleetCheck`, `arrExpiringTrainings`, `totalImpactToday`) are populated via DAO and service calls (lines 37–41) that each take `comp_id` as a parameter. There is no test verifying that these attributes are present in the request after the method returns, nor that the correct `comp_id` is forwarded to each DAO call. An incorrect `comp_id` (e.g., from a session-switch race) would silently populate the dashboard with data belonging to the wrong company.

---

**A103-12 | Severity: MEDIUM**
`session.setAttribute("isDealer", LoginDAO.isAuthority(comp_id, RuntimeConf.ROLE_DEALER))` (line 43) is also copied to `request.setAttribute("isDealer", session.getAttribute("isDealer"))` in the callers (`SwitchCompanyAction.java:40`, `LoginAction.java:69`). The session attribute is set inside `UpdateCompanySessionAttributes`, then immediately read back from the session by the caller to set the request attribute. There is no test verifying the round-trip consistency of this value, nor that the correct role string (`RuntimeConf.ROLE_DEALER`) is passed to `LoginDAO.isAuthority`.

---

**A103-13 | Severity: MEDIUM**
`UnitDAO.getInstance().getUnitNameByComp(comp_id, true)` (line 35) is called with the `activeOnly` flag hardcoded to `true`. There is no test verifying that the session attribute `arrUnit` contains only active units after a company switch. A regression in this flag (e.g., if the parameter order in `getUnitNameByComp` changed) would silently expose inactive units to the session with no test catching it.

---

**A103-14 | Severity: MEDIUM**
The method is declared `public static` and accepts both `HttpServletRequest` and `HttpSession` as separate parameters rather than deriving the session from the request. There is no test verifying that the caller passes a session that is the same object as `request.getSession()`. In `SwitchCompanyAction`, the session is obtained via `request.getSession(false)` (which can return null if no session exists) and passed directly. There is no null-guard on the `session` parameter inside `UpdateCompanySessionAttributes`; a null session would throw `NullPointerException` on the first `session.setAttribute` call (line 27).

---

### DateUtil

---

**A103-15 | Severity: CRITICAL**
`DateUtil` has zero test coverage. None of its 23 methods (public or private) are exercised by any test in the project. This class is a central date/time utility invoked from DAOs, Actions, Services, and `CompanySessionSwitcher`. Date parsing and formatting logic is among the highest-risk code for silent data corruption.

---

**A103-16 | Severity: CRITICAL**
`parseDateTime(String)` at line 164 uses the format pattern `"yyyy-mm-dd HH:mm:ss"` (lowercase `mm`). In `SimpleDateFormat`, lowercase `mm` means **minutes**, not months. A date string such as `"2024-07-15 10:30:00"` will parse the `07` field as minute 7 and set the month to January (month field defaults to 0). The method silently returns a wrong `Date` with no exception raised. There is no test asserting the correct month for any parsed value, so this bug is entirely undetected.

---

**A103-17 | Severity: HIGH**
`stringToDate(String, String)` (line 29, private) implements a two-attempt parsing fallback: it first tries the caller-supplied `format`, and if that throws `ParseException`, silently retries with the hardcoded format `"dd/MM/yyyy"` (line 45). This fallback is never documented and will silently succeed for dates that do not match the intended format, returning a `Date` object that is valid but incorrect for the caller's context. There is no test verifying that a date string that fails the primary format but matches the fallback returns the fallback-parsed value, nor that a string matching neither format returns null (it does — but only because the second catch swallows the exception after printing to stdout).

---

**A103-18 | Severity: HIGH**
`stringToSQLDate(String, String)` at line 76 calls `Objects.requireNonNull(date).getTime()` (line 86). If the input string fails to parse, `date` remains null and `requireNonNull` throws `NullPointerException` with no message context. There is no null guard or informative exception message. There is no test exercising invalid input to this method, meaning the NPE path is undetected.

---

**A103-19 | Severity: HIGH**
`stringToIsoNoTimezone(String, String)` at line 60 calls `DateUtil.stringToDate(date, dateFormat)`, which can return null if the input is null or unparseable (see `stringToDate` line 34). The return value is immediately passed to `df.format(dateObj)` at line 63 without a null check, which will throw `NullPointerException`. There is no test covering null or unparseable input to `stringToIsoNoTimezone`.

---

**A103-20 | Severity: HIGH**
`getDateFormatFromDateTimeFormat(String)` at line 233 does not guard against a null input. Calling `dateTimeFormat.contains(" ")` on a null string throws `NullPointerException`. This method is called from `CompanySessionSwitcher` (line 23), `AdminSettingsAction` (line 57), and three locations in `DriverDAO` (lines 824, 825, 839, 840, 894, 895). No test covers the null input path. This is the same null-propagation risk identified in A103-10 viewed from the DateUtil side.

---

**A103-21 | Severity: HIGH**
`getDateFormatFromDateTimeFormat(String)` at line 233–239 splits the datetime format string on the first space, returning only the substring to the left. If the format string contains no space (the `else` branch, line 237), the full string is returned unchanged and assumed to already be a date-only format. There is no test verifying:
- a format with exactly one space (e.g., `"dd/MM/yyyy HH:mm:ss"`) correctly returns `"dd/MM/yyyy"`;
- a format with multiple spaces (e.g., `"dd MMM yyyy HH:mm:ss"`) returns only `"dd"` — the substring to the first space — which is almost certainly wrong;
- a format with no space is returned as-is;
- an empty string input produces an empty string (not an exception).

---

**A103-22 | Severity: HIGH**
`StringTimeDifference(String, String, TimeUnit, String)` at line 188 silently returns `0` if either input string fails to parse (the `catch (ParseException)` block at line 198 only prints to stdout and leaves `diffInMillies` as 0). There is no test verifying failure-mode behaviour, and a caller receiving 0 will treat it as "no time elapsed" rather than as an error.

---

**A103-23 | Severity: HIGH**
`stringToTimestamp(String)` at line 175 uses a fixed format `"yyyy/MM/dd HH:mm:ss"` (slash-separated date). On parse failure the method returns null (timestamp remains null). There is no test exercising either the happy path or the null-return path. Callers receiving a null `Timestamp` may subsequently call methods on it without null-checking.

---

**A103-24 | Severity: MEDIUM**
`getStartDate(Date, String)` at line 100 has an implicit default branch: any frequency string that does not match `"Daily"`, `"Weekly"`, or `"Monthly"` (case-insensitive) falls through to `c.add(Calendar.DATE, -1)` — the same as `"Daily"`. There is no documented contract for what values are valid, no exception is thrown for unrecognised inputs, and no test verifies either the three named branches or the default fallback behaviour.

---

**A103-25 | Severity: MEDIUM**
`getLocalTimestamp(String, Locale)` and `getLocalTime(String, Locale)` (lines 115 and 131) both use `DateFormat.getDateTimeInstance()` without specifying a format style, which means the output format is JVM locale-dependent. The result is then parsed with the hardcoded `SimpleDateFormat("dd/MM/yyyy HH:mm:ss")`. If the default JVM locale produces a datetime string in a different format (e.g., on a US-locale server), `dateFormat.parse` will throw `ParseException` and propagate as an unhandled exception. No test exercises these methods with varying locales or timezone names.

---

**A103-26 | Severity: MEDIUM**
`getLocalTimestamp(String, Locale)` uses `RuntimeConf.DEFAUTL_TIMEZONE` (note the typo: `DEFAUTL` not `DEFAULT`) as the fallback timezone when `timezoneName` is null or empty (line 117). This constant resolves to `"Australia/Sydney"`. There is no test verifying the null-timezone fallback path, nor the empty-string fallback path. The same issue exists in `getLocalTime` at line 133.

---

**A103-27 | Severity: MEDIUM**
`getDaysDate(Date, int)` at line 66 uses millisecond arithmetic (`date.getTime() - days * MILLIS_IN_A_DAY`) to subtract days. This arithmetic does not account for daylight saving time transitions: subtracting 86,400,000 ms across a DST boundary may yield a result that is one hour off. There is no test covering DST boundary dates.

---

**A103-28 | Severity: MEDIUM**
`utc2Local(Timestamp, String)` at line 227 passes the `timezone` string directly to `TimeZone.getTimeZone(timezone).toZoneId()`. If an unrecognised timezone ID is supplied, `TimeZone.getTimeZone` silently returns GMT rather than throwing an exception. The method then converts as if the timezone were GMT, returning a silently incorrect result. No test exercises an invalid timezone ID input.

---

**A103-29 | Severity: LOW**
`dateToString(Date)` at line 71 and `stringToSQLDate`/`sqlDateToString` at lines 76 and 90 hardcode the format `"dd/MM/yyyy"` — this format appears in at least four separate methods throughout the class. If the application's locale requirement changes, each hardcoded occurrence must be individually updated. The absence of any test for these methods means format regressions would not be caught.

---

**A103-30 | Severity: LOW**
`GetDateNow()` at line 204 uses `Calendar.getInstance()` without specifying a timezone, so it returns the JVM's default system time. There is no test verifying the format of the returned string or its timezone behaviour. The method name uses PascalCase (non-standard for Java methods), inconsistent with the rest of the codebase.

---

**A103-31 | Severity: LOW**
`parseDate(String)` at line 159 declares `throws Exception` but `SimpleDateFormat.parse` only throws `ParseException` (a checked subtype of `Exception`). No test verifies both the success path and the exception path. Callers catching `Exception` are over-broad; callers that do not check for the exception silently swallow parse failures.

---

**A103-32 | Severity: INFO**
`local2utc(Date)` and the overloaded `utc2Local(Timestamp)` / `utc2Local(Timestamp, String)` rely on `ZoneId.systemDefault()` for the "local" timezone. In a containerised deployment the system timezone may not match the application's configured timezone (`RuntimeConf.DEFAUTL_TIMEZONE`). This mismatch is untestable without tests that explicitly set the JVM default timezone, and no such tests exist.

---

## Summary Table

| Finding | Class | Severity | Topic |
|---|---|---|---|
| A103-1 | CharsetEncodingFilter | HIGH | Zero test coverage — all methods |
| A103-2 | CharsetEncodingFilter | HIGH | `init` configurable-charset branch untested |
| A103-3 | CharsetEncodingFilter | MEDIUM | `destroy` teardown correctness unverified |
| A103-4 | CharsetEncodingFilter | MEDIUM | `doFilter` chain propagation unverified |
| A103-5 | CharsetEncodingFilter | LOW | Empty-string charset init-param not guarded or tested |
| A103-6 | CompanySessionSwitcher | CRITICAL | Zero test coverage — sole public method |
| A103-7 | CompanySessionSwitcher | CRITICAL | Duplicate session keys `sessCompId`/`currentCompany` untested |
| A103-8 | CompanySessionSwitcher | CRITICAL | Hardcoded `accountAction="update"` invariant untested |
| A103-9 | CompanySessionSwitcher | HIGH | `Integer.parseInt(timezone)` — no null/non-numeric guard or test |
| A103-10 | CompanySessionSwitcher | HIGH | Null `dateTimeFormat` propagates NPE into `getDateFormatFromDateTimeFormat` |
| A103-11 | CompanySessionSwitcher | HIGH | Request attributes populated from DAOs — not tested for correctness or wrong-company data |
| A103-12 | CompanySessionSwitcher | MEDIUM | `isDealer` session-to-request round-trip consistency untested |
| A103-13 | CompanySessionSwitcher | MEDIUM | `arrUnit` hardcoded `activeOnly=true` flag not verified by tests |
| A103-14 | CompanySessionSwitcher | MEDIUM | Null `session` parameter not guarded; `getSession(false)` can return null in caller |
| A103-15 | DateUtil | CRITICAL | Zero test coverage — all 23 methods |
| A103-16 | DateUtil | CRITICAL | `parseDateTime` uses `yyyy-mm-dd` (minutes not months) — silent wrong-month bug |
| A103-17 | DateUtil | HIGH | `stringToDate` silent two-format fallback — incorrect dates returned without exception |
| A103-18 | DateUtil | HIGH | `stringToSQLDate` — `requireNonNull` throws NPE with no context on parse failure |
| A103-19 | DateUtil | HIGH | `stringToIsoNoTimezone` — null-dereference when `stringToDate` returns null |
| A103-20 | DateUtil | HIGH | `getDateFormatFromDateTimeFormat` — no null guard; NPE on null input |
| A103-21 | DateUtil | HIGH | `getDateFormatFromDateTimeFormat` — multi-space format produces wrong date-only segment |
| A103-22 | DateUtil | HIGH | `StringTimeDifference` — parse failure silently returns 0 |
| A103-23 | DateUtil | HIGH | `stringToTimestamp` — parse failure silently returns null |
| A103-24 | DateUtil | MEDIUM | `getStartDate` — unknown frequency silently defaults to Daily |
| A103-25 | DateUtil | MEDIUM | `getLocalTimestamp`/`getLocalTime` — locale-dependent format causes parse failure on non-default JVM locale |
| A103-26 | DateUtil | MEDIUM | `getLocalTimestamp`/`getLocalTime` — null/empty timezone fallback to `DEFAUTL_TIMEZONE` untested |
| A103-27 | DateUtil | MEDIUM | `getDaysDate` — millisecond arithmetic incorrect across DST boundaries |
| A103-28 | DateUtil | MEDIUM | `utc2Local(Timestamp, String)` — invalid timezone silently returns GMT result |
| A103-29 | DateUtil | LOW | Hardcoded `"dd/MM/yyyy"` format scattered across multiple methods |
| A103-30 | DateUtil | LOW | `GetDateNow()` uses JVM default timezone; non-standard PascalCase naming |
| A103-31 | DateUtil | LOW | `parseDate` over-broad `throws Exception` — success and failure paths untested |
| A103-32 | DateUtil | INFO | `local2utc`/`utc2Local` rely on `ZoneId.systemDefault()` — untestable without explicit JVM timezone override |
