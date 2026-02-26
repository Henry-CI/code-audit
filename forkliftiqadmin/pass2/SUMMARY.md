# Pass 2: Test Coverage Audit — SUMMARY
**Audit Run:** 2026-02-26-01
**Date:** 2026-02-26
**Scope:** All Java source files (287 classes across `com.action`, `com.actionform`, `com.servlet`, `com.bean`, `com.calibration`, `com.cognito.bean`, `com.dao`, `com.json`, `com.pdf`, `com.quartz`, `com.querybuilder`, `com.report`, `com.service`, `com.util`) and all JSP view files (81 files)

---

## Coverage Infrastructure

The project contains exactly **4 test files** covering an estimated 287 Java source classes and 81 JSP view files:

| Test File | Classes Covered | Methods Covered |
|---|---|---|
| `UnitCalibrationImpactFilterTest.java` | `UnitCalibrationImpactFilter` | 3 of 9 methods (partially) |
| `UnitCalibrationTest.java` | `UnitCalibration` (data class) | Limited bean tests |
| `UnitCalibratorTest.java` | `UnitCalibrator` | 4 of ~8 methods |
| `ImpactUtilTest.java` | `ImpactUtil` | 3 of 5 methods (boundary gaps remain) |

**Effective test coverage: < 2%** of the codebase by class count; 0% for every Action, DAO, Service, Servlet, Quartz, QueryBuilder, PDF, Report, and JSP class.

---

## Agent Report Index

115 agents produced 119 report files (4 supplemental passes from duplicate dispatches). See individual files for reading evidence and per-finding detail.

| Agent Range | Package / Area | Report Files |
|---|---|---|
| A01–A28 | `com.action` (58 classes) | A01–A28_*.md |
| A29–A40 | `com.actionform` (36 classes) | A29–A40_*.md |
| A41 | `com.servlet.PreFlightActionServlet` | A41_*.md |
| A42–A61 | `com.bean` (53 classes) | A42–A61_*.md |
| A62–A67 | `com.calibration` (12 classes) | A62–A67_*.md |
| A68–A71 | `com.cognito.bean` (10 classes) | A68–A71_*.md |
| A72–A81 | `com.dao` (23 classes) | A72–A81_*.md |
| A82–A86 | `com.json` (15 classes — vendored org.json) | A82–A86_*.md |
| A87 | `com.pdf` (2 classes) | A87_*.md |
| A88–A89 | `com.quartz` (6 classes) | A88–A89_*.md |
| A90–A98 | `com.querybuilder` (26 classes) | A90–A98_*.md |
| A99 | `com.report` (3 classes) | A99_*.md |
| A100–A101 | `com.service` (6 classes) | A100–A101_*.md |
| A102–A106 | `com.util` (13 classes) | A102–A106_*.md |
| B01–B09 | JSP view files (81 files) | B01–B09_*.md |

---

## Severity Summary (Approximate Totals)

Totals aggregated from agent completion reports. Exact per-finding counts are in individual files.

| Severity | Approximate Total | Key Driver |
|---|---|---|
| **CRITICAL** | ~200 | SQL injection in all DAOs; XSS in JSPs; no auth on API endpoint; broken auth mechanisms |
| **HIGH** | ~600 | NPE on session attributes; broken singletons; exception swallowing; missing test classes; resource leaks |
| **MEDIUM** | ~350 | Missing edge-case tests; boundary conditions; concurrency risks; configuration issues |
| **LOW** | ~200 | Documentation gaps; naming issues; dead code; minor defects |
| **INFO** | ~100 | Suggestions; vendored library staleness; architectural notes |
| **TOTAL** | **~1,450** | Across ~287 Java classes + 81 JSPs |

---

## Critical Findings — Most Severe Issues

### 1. SQL Injection (CRITICAL × 30+) — All DAO Classes
Every DAO class builds SQL queries by string concatenation of user-controlled or session-derived values. No class uses parameterised queries for dynamic filters. Affected classes include (non-exhaustive):
- `AdvertismentDAO`, `CompanyDAO` — 10 confirmed CRITICAL SQL injection points (A72)
- `GPSDao.getGPSLocations()`, `ImpactReportDAO` — direct parameter injection (A75)
- `JobsDAO.getJobList()`, `getJobListByJobId()` — SQL injection + non-atomic ID generation (A76)
- `ManufactureDAO`, `MenuDAO`, `QuestionDAO` — 14 CRITICAL across three classes (A78)
- `UnitDAO` — 6 SQL injection methods, 32 untested methods total (A81)
- `unit.gps.jsp` — calls `GPSDao.getGPSLocations()` which has confirmed SQL injection (B01)

### 2. Reflected XSS (CRITICAL) — Multiple JSPs
Request parameters written directly into HTML `value` attributes without escaping:
- `adminUnit.jsp`: `request.getParameter("searchUnit")` → `value="<%=searchUnit %>"` (B01/B02)
- `adminUser.jsp`: `request.getParameter("searchDriver")` → `value="<%=searchDriver %>"` (B01/B02)
- `adminOperator.jsp`: `request.getParameter("searchDriver")` → `value="<%=searchDriver %>"` (B01)
- `adminJob.jsp`: `request.getParameter("equipId")` and `action` → unencoded hidden inputs + DOM `innerHTML` write (B01)
- `resetpass.jsp`: `request.getParameter("username")` → `value="<%=username %>"` in password reset form (B05)

### 3. Stored XSS (CRITICAL) — Multiple JSPs
Database-sourced content written to HTML without encoding or with insufficient encoding context:
- `adsleft.inc.jsp`, `adsright.inc.jsp`: `AdvertisementBean.pic`/`text` via `<bean:write>` into HTML (B08)
- `formBuilder.jsp`: `FormElementBean` fields (`lable`, `value`, `style`, `type`) injected into JavaScript string literals (B04)
- `manufacturers.jsp`: `elem.name` concatenated via `innerHTML` in JavaScript (B06)
- `incidentReport.jsp` (reports/): unencoded `description`, `location`, `witness` free-text fields (B05)

### 4. XML/JSON Injection (CRITICAL) — AJAX Endpoints
- `getAjax.jsp`: `XmlBean.getId()`/`getName()` concatenated into XML without encoding (B04)
- `getDriverName.jsp`: driver `first_name`/`last_name` concatenated into XML without encoding (B04)
- `apiXml.jsp`: unit names, driver names, attachment names directly into XML; `>` escape branch has copy-paste bug escaping `<` instead (B02)

### 5. Unauthenticated API Access (CRITICAL) — `PreFlightActionServlet`
`/api.do` is listed in the excluded-path set, bypassing the session check entirely. The `AppAPIAction` handler behind this endpoint is entirely commented out, meaning every request throws NPE on `request.getAttribute("method")`. (A41, B02)

### 6. Authentication Bypass — Register Endpoint
`/adminRegister.do` is also excluded from session authentication in `PreFlightActionServlet`, allowing unauthenticated creation of company accounts. (B02)

### 7. MD5 Password Hashing (CRITICAL) — `LoginDAO.checkLogin()` (A77)
Passwords are hashed with unsalted MD5 before database comparison. MD5 is cryptographically broken for password storage; rainbow tables cover most common passwords. No migration path exists.

### 8. MD5 Client-Side Password Hashing — `driver/general.jsp` (B07)
PIN/password is hashed client-side with MD5 in JavaScript before transmission. MD5 is cryptographically broken; transmission of a hash rather than the plaintext does not add security if the hash is what's stored.

### 9. `CompanyDAO.saveUsers()` SQL Block Commented Out (CRITICAL) — A72
The SQL that inserts user rows in `saveUsers()` is entirely commented out. The method returns `true` indicating success while silently performing no user creation. This is a live data-loss defect in all code paths that call `saveUsers()`.

### 10. `IncidentReportDAO.getInstance()` Synchronises on Wrong Lock (CRITICAL) — A76
The method synchronises on `ImpactReportDAO.class` instead of `IncidentReportDAO.class`. Under concurrent access, two `IncidentReportDAO` singletons can be created, leading to race conditions in all DAO operations.

### 11. `UnitManufactureFilterHandler` Zero-Field Constructor SQL Corruption (CRITICAL) — A94
Calling the handler with a zero-field constructor triggers `StringBuilder.delete()` with negative indices, producing `" A"` as the SQL fragment instead of a valid WHERE clause. Untested; occurs silently.

### 12. `ImpactLevelFilterHandler.ignoreFilter()` Returns Active Filter (CRITICAL) — A92
When `filter` is null, `ignoreFilter()` returns `true` but `getQueryFilter()` then emits `" AND impact_value > unit_threshold "` — an active filter, not a no-op. All other handlers emit `""` on ignore. This semantic inversion silently changes query results.

### 13. `NullPointerException` on Session Attributes — Universal Pattern
`session.getAttribute(...)` return values are cast and dereferenced without null checks across:
- All 58+ Action classes (pattern: `session.getSession(false)` then immediate `.getAttribute()` cast)
- JSPs: `home.jsp`, `impact.jsp`, all report JSPs (`sessDateFormat`, `isDealer`, `isSuperAdmin`), `assignment.jsp`, etc.
An expired or partial session causes uncaught NPE producing a 500 error with a stack trace.

### 14. Hardcoded Live Credentials and URLs — `RuntimeConf`, `RestClientService`, `HttpDownloadUtility`
- `RuntimeConf.java`: live production HTTP URL, AWS EC2 IP, S3 bucket URL, live receiver email address — all hardcoded as `public static` non-final fields (A105)
- `RestClientService.java`: hardcoded `http://localhost:9090` in all 8 methods; port hardcoded as a field (A101)
- `HttpDownloadUtility.java`: hardcoded API authentication token (A104)
- `settings.xml`: Tomcat manager credentials committed to repository (Pass 0 finding P0-3)

### 15. Broken Double-Checked Locking — All Singletons (HIGH × 50+)
`theInstance` fields in every DAO, Service, and singleton class are not `volatile`. Under the Java memory model, the double-checked locking pattern is unsafe without `volatile`, allowing a thread to observe a partially-constructed singleton. Affects: all DAO classes, `ReportService`, `DriverService`, `CalibrationJobScheduler`, etc.

---

## Critical Defects by Package

| Package | CRITICAL Findings | Most Severe Issue |
|---|---|---|
| `com.dao` | 50+ | SQL injection in every class; MD5 auth; wrong singleton lock |
| JSP (`html-jsp/`, `includes/`, `gps/`) | 40+ | Reflected XSS; stored XSS; XML injection; NPE; auth bypass |
| `com.querybuilder` | 15+ | Parameter count mismatches; SQL fragment corruption; missing `volatile` |
| `com.action` | 15+ | NPE on session; unauthenticated endpoint; auth logic in session |
| `com.util` | 10+ | Hardcoded live config; MD5 PRNG password generation; SSRF in `getHTML` |
| `com.service` | 8+ | Hardcoded localhost; swallowed network failures; assert for null-guard |
| `com.quartz` | 8+ | Silent exception swallowing; thread leaks; wrong trigger group names |
| `com.pdf` | 5+ | Static NPE in field initialiser; UncheckedIOException silently swallowed |
| `com.report` | 6+ | NPE on empty results; hardcoded localhost CSS; swallowed exceptions |

---

## Systemic Patterns (All Classes Affected)

These patterns appear in virtually every class and every JSP:

1. **Zero test coverage** — 4 test files for ~370 files. No test infrastructure for Actions, DAOs, Services, JSPs, or integration paths.
2. **Silent exception swallowing** — `catch (Exception e) { e.printStackTrace(); }` throughout. Failures are invisible to callers.
3. **Resource leaks** — `Connection`, `PreparedStatement`, `ResultSet` opened in try blocks but never closed in `finally` blocks across all DAO classes.
4. **No CSRF protection** — No CSRF synchroniser token anywhere in the application. Every state-changing form is trivially vulnerable.
5. **Non-volatile singletons** — Every singleton uses the double-checked locking pattern without `volatile`; all are unsafe under JMM.
6. **`bean:write` without explicit `filter="true"`** — Default HTML encoding is insufficient in JavaScript, CSS, URL, and XML contexts; misused throughout JSP views.
7. **Untestable architecture** — DAO instances obtained via static factories or `new` inside methods; no dependency injection; no mockable seams.

---

## Notable Structural Observations

- **Vendored `org.json` library** (2010–2012 vintage, repackaged as `com.json`): 15 files of dead/partially-used code. Three classes (`CDL`, `JSONML`, `com.json.Cookie`) are entirely unreferenced by application code. Deprecated boxing constructors removed in Java 17. No mechanism to detect staleness.
- **`driver/licence.jsp` is 0 bytes** — referenced in navigation; renders a blank page for all users who navigate to it.
- **`mailSuccuess.jsp` is 0 bytes** — actions forward to this page on mail success; users see a blank response.
- **`menu_popup.inc.jsp` is 0 bytes** — dead placeholder.
- **Quartz trigger group names copy-pasted** — `TrainingExpiryDailyEmailJobSchedueler` and `TrainingExpiryWeeklyEmailJobScheduler` both use trigger group name `"driverAccessRevoke"` — a copy-paste error that may cause scheduler conflicts.
- **`DateUtil.parseDateTime()` uses `"yyyy-mm-dd"`** — lowercase `mm` is minutes, not months. Silent date corruption for all parsed datetimes.
- **`DateFormatDAO.DEFAULT_DATE_FORMAT = "dd/mm/yyyy"`** — same `mm` vs `MM` bug; affects all date rendering.
- **`AppAPIAction` is entirely commented out** — the backing action for `/api.do` produces NPE on every request.
- **`PreFlightActionServlet.endsWith()` path bypass** — paths are excluded using `endsWith()` without a preceding `/`, allowing bypass via path construction (A41).

---

## Pass 2 Completion Status

| Stage | Status |
|---|---|
| Java agents (A01–A106) | Complete — 106 report files written |
| JSP agents (B01–B09) | Complete — 9 report files written (4 supplemental) |
| Summary | **This file** |

All 119 report files are in `audit/2026-02-26-01/pass2/`. Pass 2 is complete.
