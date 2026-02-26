# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent:** A27
**Files audited:**
- `src/main/java/com/action/SessionReportAction.java`
- `src/main/java/com/action/SwitchCompanyAction.java`

---

## Reading Evidence

### SessionReportAction

**Class:** `com.action.SessionReportAction` (extends `org.apache.struts.action.Action`)
**File:** `src/main/java/com/action/SessionReportAction.java`

**Methods:**

| Method | Line |
|--------|------|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | 19 |

**Fields/Constants defined:** none (no instance or static fields; all variables are local to `execute`)

**Local variables of significance in `execute`:**

| Variable | Line | Source |
|----------|------|--------|
| `session` | 20 | `request.getSession(false)` |
| `sessCompId` | 21 | `(String) session.getAttribute("sessCompId")` |
| `dateFormat` | 22 | `(String) session.getAttribute("sessDateFormat")` |
| `dateTimeFormat` | 23 | `(String) session.getAttribute("sessDateTimeFormat")` |
| `timezone` | 24 | `(String) session.getAttribute("sessTimezone")` |
| `compId` | 25 | `Integer.parseInt(Objects.requireNonNull(sessCompId))` |
| `sessionReportFilter` | 27 | `(SessionReportSearchForm) form` |

**Call chain in `execute`:**

| Line | Expression |
|------|-----------|
| 25 | `Objects.requireNonNull(sessCompId)` → throws `NullPointerException` with no message if `null` |
| 25 | `Integer.parseInt(...)` → throws `NumberFormatException` if value is not a valid integer |
| 28 | `sessionReportFilter.setTimezone(timezone)` |
| 30 | `UnitDAO.getAllUnitsByCompanyId(compId)` → result set as request attribute `"vehicles"` |
| 31 | `DriverDAO.getAllDriver(sessCompId, true)` → result set as request attribute `"drivers"` |
| 33-39 | `ReportService.getInstance().getSessionReport(compId, sessionReportFilter.getSessionReportFilter(dateFormat), dateTimeFormat, timezone)` → result as request attribute `"sessionReport"` |
| 41 | `mapping.findForward("report")` — only forward; no failure forward |

**Branch structure:** Linear — no conditional branches. All control flow is sequential; the only divergence is via uncaught exceptions.

---

### SwitchCompanyAction

**Class:** `com.action.SwitchCompanyAction` (extends `org.apache.struts.action.Action`, annotated `@Slf4j`)
**File:** `src/main/java/com/action/SwitchCompanyAction.java`

**Methods:**

| Method | Line |
|--------|------|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | 20 |

**Fields/Constants defined:** none at the class level (Lombok `@Slf4j` injects a `private static final Logger log` field, but it is never used in this class body)

**Local variables of significance in `execute`:**

| Variable | Line | Source |
|----------|------|--------|
| `session` | 25 | `request.getSession(false)` |
| `loginActionForm` | 26 | `(SwitchCompanyActionForm) actionForm` |
| `isSuperAdmin` | 27 | `(Boolean) session.getAttribute("isSuperAdmin")` |
| `isDealerLogin` | 28 | `(Boolean) session.getAttribute("isDealerLogin")` |
| `loggedInCompanyId` | 29 | `(Integer) session.getAttribute("sessAccountId")` |
| `companies` | 35 | `LoginDAO.getCompanies(isSuperAdmin, isDealerLogin, loggedInCompanyId)` |
| `company` (loop var) | 36 | iteration over `companies` |

**Branch structure:**

| Lines | Condition | Outcome |
|-------|-----------|---------|
| 31–33 | `!isSuperAdmin && !isDealerLogin` is `true` | early return `mapping.findForward("failure")` |
| 35–38 | else (at least one of the flags is `true`) | fetches companies, iterates, conditionally calls `UpdateCompanySessionAttributes` |
| 37 | `company.getId().equals(loginActionForm.getCurrentCompany())` | inner match — calls `CompanySessionSwitcher.UpdateCompanySessionAttributes(company, request, session)` |
| 40 | — | sets `"isDealer"` request attribute from session |
| 41 | — | returns `mapping.findForward("successAdmin")` |

---

## Test Coverage Confirmation

Grep of `src/test/java/` for `SessionReportAction`, `SwitchCompanyAction`, `SessionReport`, and `SwitchCompany`: **no matches found**.

Existing test files in the project (all four):

| File | Subject |
|------|---------|
| `com/calibration/UnitCalibrationImpactFilterTest.java` | `UnitCalibrationImpactFilter` |
| `com/calibration/UnitCalibrationTest.java` | `UnitCalibration` |
| `com/calibration/UnitCalibratorTest.java` | `UnitCalibrator` |
| `com/util/ImpactUtilTest.java` | `ImpactUtil` |

None of these reference either audited class directly or indirectly. Coverage is **0%** for both action classes.

---

## Findings

### SessionReportAction

---

**A27-1 | Severity: CRITICAL | Null session causes NullPointerException — no test**

`execute()` line 20 calls `request.getSession(false)`. The `false` argument means the container returns `null` instead of creating a new session when no active session exists. Lines 21–24 immediately dereference the returned reference (`session.getAttribute(...)`). If the session has expired or the request arrives without a valid session cookie, a `NullPointerException` is thrown with no descriptive message, producing an unhandled HTTP 500 error. There is no null guard, no redirect to a login page, and no test exercising this path.

---

**A27-2 | Severity: CRITICAL | NullPointerException on null sessCompId with misleading stack trace — no test**

Line 25 calls `Objects.requireNonNull(sessCompId)`. When `sessCompId` is `null` (missing or expired session attribute), this throws `NullPointerException` with no message string. Because no message is passed to `requireNonNull`, the exception carries no indication of which attribute is absent, making diagnosis in production logs harder. There is no test covering the null-`sessCompId` path.

---

**A27-3 | Severity: CRITICAL | NumberFormatException on non-integer sessCompId — no test**

Line 25 calls `Integer.parseInt(Objects.requireNonNull(sessCompId))`. If `sessCompId` contains any non-integer value (e.g., an empty string `""`, alphabetic characters, or a floating-point string) the call throws `NumberFormatException`, which propagates uncaught through `execute`'s `throws Exception` declaration. No input validation is performed and no test covers this error path.

---

**A27-4 | Severity: HIGH | Null session attributes for dateFormat, dateTimeFormat, or timezone silently passed downstream — no test**

Lines 22–24 cast session attributes to `String` without null checks. If any of `"sessDateFormat"`, `"sessDateTimeFormat"`, or `"sessTimezone"` is absent from the session, the corresponding variable is `null`. These nulls are then passed directly into `sessionReportFilter.setTimezone(null)` (line 28) and into `ReportService.getSessionReport(..., null, null)` (lines 35–39). Whether the downstream service handles nulls gracefully is untested, and no test verifies that null timezone or format values are either rejected early or produce correct output.

---

**A27-5 | Severity: HIGH | UnitDAO.getAllUnitsByCompanyId call is entirely untested — no test**

Line 30 calls the static method `UnitDAO.getAllUnitsByCompanyId(compId)` and sets the result as the `"vehicles"` request attribute. There is no test verifying that the correct compId is passed, that the result is placed under the correct attribute name, or that a DAO exception (which propagates through `throws Exception`) is handled. Any regression in the DAO call, the attribute key, or the compId value is undetectable.

---

**A27-6 | Severity: HIGH | DriverDAO.getAllDriver call is entirely untested — no test**

Line 31 calls `DriverDAO.getAllDriver(sessCompId, true)` using the raw String form of the company ID (rather than the parsed `int compId`). This inconsistency — `compId` as `int` elsewhere, `sessCompId` as `String` here — is untested. There is also no test for DAO failure, for what happens when `sessCompId` is valid but the DAO returns an empty list, or for whether the `true` boolean argument (presumably `activeOnly`) has the expected effect.

---

**A27-7 | Severity: HIGH | ReportService.getSessionReport call is entirely untested — no test**

Lines 33–39 call `ReportService.getInstance().getSessionReport(...)` and set the result as the `"sessionReport"` request attribute. No test verifies argument correctness, attribute naming, empty-result behaviour, or exception propagation from `ReportService`.

---

**A27-8 | Severity: HIGH | Only one forward ("report") exists — no failure forward, no test**

Line 41 is the only return path that does not throw. There is no `"failure"` or `"error"` forward registered for `SessionReportAction`. Any exception thrown by the DAO or service layer propagates to the Struts framework or container, producing an uncontrolled error page. No test verifies that the `"report"` forward is returned on the happy path, nor that exception paths result in an appropriate response.

---

**A27-9 | Severity: MEDIUM | sessionReportFilter.getSessionReportFilter(dateFormat) with null dateFormat — no test**

Line 36 passes `dateFormat` (which may be `null` — see A27-4) to `SessionReportSearchForm.getSessionReportFilter(String)`. Inside that method, `DateUtil.stringToUTCDate(this.start_date, dateFormat)` is called when `start_date` is non-null (line 27 of `SessionReportSearchForm`). The behaviour of `DateUtil.stringToUTCDate` with a null format string is unknown and untested. A null format could result in a `NullPointerException`, incorrect date parsing, or a silent UTC default.

---

**A27-10 | Severity: MEDIUM | Filter fields vehicle_id and driver_id with zero values treated as null — no test**

`SessionReportSearchForm.getSessionReportFilter` treats `vehicle_id == 0` and `driver_id == 0` as equivalent to `null` (lines 25–26 of the form class). This means a form submission with an explicit zero value silently becomes an unfiltered query. There is no test verifying this zero-to-null conversion, nor any test confirming that the action correctly propagates these values to the service layer.

---

**A27-11 | Severity: MEDIUM | DAO and service exceptions propagate unhandled to the container — no test**

`execute` declares `throws Exception`. Exceptions from `UnitDAO`, `DriverDAO`, and `ReportService` all escape to Struts/the container. No test verifies the resulting HTTP response, error page content, or whether partial state (e.g., `"vehicles"` attribute set but `"sessionReport"` not set) causes downstream rendering failures.

---

**A27-12 | Severity: LOW | @Override annotation present but not tested for signature correctness — no test**

The `@Override` annotation on line 18 confirms that the method overrides the Struts `Action.execute` signature at compile time. However, there is no test that instantiates `SessionReportAction` and dispatches through it to verify the override is wired correctly within the Struts framework.

---

### SwitchCompanyAction

---

**A27-13 | Severity: CRITICAL | Null session causes NullPointerException — no test**

Line 25 calls `request.getSession(false)`, which returns `null` when no session exists. Lines 27–29 immediately dereference `session` (`session.getAttribute(...)`). A request without an active session throws `NullPointerException`. No null guard is present and no test covers this path.

---

**A27-14 | Severity: CRITICAL | Unboxing NullPointerException when isSuperAdmin or isDealerLogin is null — no test**

Lines 27–28 cast session attributes to `Boolean` (object type). Line 31 uses the expression `!isSuperAdmin && !isDealerLogin`, which auto-unboxes both `Boolean` references. If either attribute is absent from the session and the cast returns `null`, unboxing throws `NullPointerException`. This is a hidden crash path that no test exercises.

---

**A27-15 | Severity: CRITICAL | No test for the authorisation guard (failure branch) — no test**

Line 31 is the sole security check: if the user is neither a super-admin nor a dealer login, the action returns `mapping.findForward("failure")`. There is no test verifying that:
- a non-privileged user is denied (the guard fires correctly),
- the `"failure"` forward name is returned and not some other string,
- the guard cannot be bypassed by manipulating session attributes.

---

**A27-16 | Severity: HIGH | Null loggedInCompanyId silently returns an empty company list — no test**

`LoginDAO.getCompanies(Boolean, Boolean, Integer)` (line 106 of `LoginDAO`) returns `new ArrayList<>()` when `company` is `null`. Line 29 reads `loggedInCompanyId` from the session without a null check. If the attribute is missing, `loggedInCompanyId` is `null`, the DAO returns an empty list, the for-loop on line 36 does nothing, no session attributes are updated, and the action silently forwards to `"successAdmin"` as if the switch succeeded. There is no test covering this silent no-op path.

---

**A27-17 | Severity: HIGH | No test for the successAdmin (happy-path) branch — no test**

The path where at least one of `isSuperAdmin`/`isDealerLogin` is `true`, the company list is fetched, a matching company is found, `CompanySessionSwitcher.UpdateCompanySessionAttributes` is called, and `"successAdmin"` is returned — is entirely untested. No test verifies argument correctness, the session state after the switch, the request attribute `"isDealer"`, or the forward name.

---

**A27-18 | Severity: HIGH | No test for the case where no company in the list matches currentCompany — no test**

Line 37 tests `company.getId().equals(loginActionForm.getCurrentCompany())`. If no company in the returned list matches, the loop exits silently, no session attributes are updated, and the action still returns `"successAdmin"`. A user could submit an arbitrary company ID and receive a success response while their session remains unchanged. No test covers this no-match path.

---

**A27-19 | Severity: HIGH | CompanySessionSwitcher.UpdateCompanySessionAttributes is entirely untested through this action — no test**

When a match is found on line 37, `CompanySessionSwitcher.UpdateCompanySessionAttributes(company, request, session)` is called. This method performs 12+ session and request attribute mutations (including DAO and service calls to `TimezoneDAO`, `UnitDAO`, `DriverDAO`, `ReportService`, `LoginDAO`, `CompanyDAO`). None of these side-effects are tested through `SwitchCompanyAction`. An exception thrown inside `UpdateCompanySessionAttributes` propagates through `execute`'s `throws Exception` with no test to detect it.

---

**A27-20 | Severity: HIGH | LoginDAO.getCompanies exception propagates unhandled — no test**

Line 35 calls `LoginDAO.getCompanies(...)` which declares `throws SQLException`. The exception propagates through `execute`'s `throws Exception` to the container. No test verifies what happens on a DAO failure: which HTTP status is returned, whether the session is left in a partial or inconsistent state, and whether Struts logs and handles the error appropriately.

---

**A27-21 | Severity: MEDIUM | currentCompany is never validated before use in equals comparison — no test**

`loginActionForm.getCurrentCompany()` (from `SwitchCompanyActionForm`) defaults to `null` (line 8 of the form class). Line 37 calls `company.getId().equals(loginActionForm.getCurrentCompany())`. Since `equals` is called on `company.getId()` (not on the potentially-null `getCurrentCompany()`), a null `currentCompany` simply never matches — the loop silently no-ops. However, no test verifies this behaviour, nor confirms that a null or empty form field is rejected rather than silently ignored.

---

**A27-22 | Severity: MEDIUM | ClassCastException when session attributes are wrong types — no test**

Lines 27–29 cast session attributes to `Boolean`, `Boolean`, and `Integer` respectively. If any of these attributes was stored as a different type (e.g., `String "true"` instead of `Boolean.TRUE`), a `ClassCastException` is thrown. No test exercises type-mismatch scenarios for any of the three attributes.

---

**A27-23 | Severity: MEDIUM | @Slf4j logger is injected but never used — no test to detect dead logger regression**

The class is annotated `@Slf4j` (line 18), which causes Lombok to generate a `private static final Logger log` field. The field is never referenced anywhere in the class body. No log statement is emitted for any path — including the security failure branch, the no-match branch, or any exception. No test would detect if the logger were accidentally used or if logging were added incorrectly in the future.

---

**A27-24 | Severity: MEDIUM | isDealer request attribute reflects post-switch session state only if a match occurred — no test**

Line 40 reads `session.getAttribute("isDealer")` and sets it as a request attribute. This attribute is updated inside `CompanySessionSwitcher.UpdateCompanySessionAttributes` (line 43 of that class) only when a matching company was found. If no match occurred (see A27-18), `"isDealer"` is read from the pre-switch session state but presented to the view as if it reflects the attempted switch. No test distinguishes the matched vs. unmatched case for this attribute.

---

**A27-25 | Severity: LOW | Only one success forward ("successAdmin") — no test to detect misconfigured forward name**

Line 41 always returns `mapping.findForward("successAdmin")` on the non-failure path, regardless of whether the company switch actually succeeded (matched) or silently no-oped. No test verifies the string `"successAdmin"`, that the forward is configured in `struts-config.xml`, or that returning it after a no-op switch does not expose data from the previous company session.

---

## Summary Table

| Finding | Severity | Class |
|---------|----------|-------|
| A27-1  | CRITICAL | SessionReportAction |
| A27-2  | CRITICAL | SessionReportAction |
| A27-3  | CRITICAL | SessionReportAction |
| A27-4  | HIGH     | SessionReportAction |
| A27-5  | HIGH     | SessionReportAction |
| A27-6  | HIGH     | SessionReportAction |
| A27-7  | HIGH     | SessionReportAction |
| A27-8  | HIGH     | SessionReportAction |
| A27-9  | MEDIUM   | SessionReportAction |
| A27-10 | MEDIUM   | SessionReportAction |
| A27-11 | MEDIUM   | SessionReportAction |
| A27-12 | LOW      | SessionReportAction |
| A27-13 | CRITICAL | SwitchCompanyAction |
| A27-14 | CRITICAL | SwitchCompanyAction |
| A27-15 | CRITICAL | SwitchCompanyAction |
| A27-16 | HIGH     | SwitchCompanyAction |
| A27-17 | HIGH     | SwitchCompanyAction |
| A27-18 | HIGH     | SwitchCompanyAction |
| A27-19 | HIGH     | SwitchCompanyAction |
| A27-20 | HIGH     | SwitchCompanyAction |
| A27-21 | MEDIUM   | SwitchCompanyAction |
| A27-22 | MEDIUM   | SwitchCompanyAction |
| A27-23 | MEDIUM   | SwitchCompanyAction |
| A27-24 | MEDIUM   | SwitchCompanyAction |
| A27-25 | LOW      | SwitchCompanyAction |

**Total findings: 25**
CRITICAL: 6 | HIGH: 9 | MEDIUM: 8 | LOW: 2
