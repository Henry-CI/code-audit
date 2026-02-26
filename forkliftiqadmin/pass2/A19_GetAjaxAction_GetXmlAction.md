# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A19
**Files audited:**
- `src/main/java/com/action/GetAjaxAction.java`
- `src/main/java/com/action/GetXmlAction.java`

---

## 1. Reading-Evidence Block

### 1.1 GetAjaxAction

**File:** `src/main/java/com/action/GetAjaxAction.java`
**Class:** `com.action.GetAjaxAction extends org.apache.struts.action.Action`

**Fields / instance variables:**

| Name | Type | Declaration line |
|------|------|-----------------|
| `unitDao` | `UnitDAO` (singleton) | 20 |

**Methods:**

| Method | Signature | Lines |
|--------|-----------|-------|
| `execute` | `public ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 22–56 |

**Action-dispatch branches inside `execute` (all at lines 29–52):**

| Branch condition | Action string | DAO / method called | Lines |
|-----------------|---------------|---------------------|-------|
| `action.equalsIgnoreCase("getType")` | `getType` | `unitDao.getType(manu_id)` | 29–32 |
| `action.equalsIgnoreCase("getPower")` | `getPower` | `unitDao.getPower(manu_id, type_id)` | 33–37 |
| `action.equalsIgnoreCase("getQcontent")` | `getQcontent` | `new QuestionDAO().getQuestionContentById(qus_id, lan_id)` | 38–43 |
| `action.equals("last_gps")` | `last_gps` | `GPSDao.getUnitGPSData(compId, unit, dateTimeFormat, timezone)` | 44–52 |
| _(implicit else / unknown action)_ | any other string | nothing (empty list forwarded) | — |

**Key local variables read from request / session (with null defaults):**

| Variable | Source | Null default | Line |
|----------|--------|--------------|------|
| `action` | `request.getParameter("action")` | `""` | 25 |
| `manu_id` | `request.getParameter("manu_id")` | `"0"` | 26 |
| `type_id` | `request.getParameter("type_id")` | `"0"` | 35 |
| `qus_id` | `request.getParameter("qus_id")` | `"0"` | 40 |
| `lan_id` | `request.getParameter("lan_id")` | `"0"` | 41 |
| `unit` | `request.getParameterValues("unit")` | _(no null guard)_ | 45 |
| `compId` | `request.getParameter("compId")` | `"0"` | 46 |
| `dateFormat` | `session.getAttribute("sessDateFormat")` | _(no null guard; cast + replaceAll)_ | 47 |
| `dateTimeFormat` | `session.getAttribute("sessDateTimeFormat")` | _(no null guard)_ | 48 |
| `timezone` | `session.getAttribute("sessTimezone")` | _(no null guard)_ | 49 |

---

### 1.2 GetXmlAction

**File:** `src/main/java/com/action/GetXmlAction.java`
**Class:** `com.action.GetXmlAction extends org.apache.struts.action.Action`

**Fields / instance variables:**

| Name | Type | Declaration line |
|------|------|-----------------|
| `driverDAO` | `DriverDAO` (singleton) | 20 |

**Methods:**

| Method | Signature | Lines |
|--------|-----------|-------|
| `execute` | `public ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 22–30 |

**Key local variables:**

| Variable | Source | Null default | Line |
|----------|--------|--------------|------|
| `session` | `request.getSession(false)` | _(no null guard)_ | 25 |
| `sessCompId` | `session.getAttribute("sessCompId")` | `""` | 26 |
| `arrDriver` | `driverDAO.getAllDriver(sessCompId, true)` | — | 27 |

---

## 2. Test-Coverage Grep Evidence

Test directory scanned: `src/test/java/`

Test files present (4 total):
```
src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java
src/test/java/com/calibration/UnitCalibrationTest.java
src/test/java/com/calibration/UnitCalibratorTest.java
src/test/java/com/util/ImpactUtilTest.java
```

Grep results for class names and related identifiers:

| Pattern searched | Matches in test directory |
|-----------------|--------------------------|
| `GetAjaxAction` | None |
| `GetXmlAction` | None |
| `getType` | None |
| `getPower` | None |
| `getQcontent` | None |
| `last_gps` | None |
| `getDriverList` | None |
| `UnitDAO` | None |
| `DriverDAO` | None |
| `GPSDao` | None |
| `QuestionDAO` | None |
| `XmlBean` | None |
| `DriverBean` | None |

**Conclusion:** Zero direct or indirect test coverage exists for either action class or the DAO methods they invoke.

---

## 3. Coverage Gaps and Findings

---

### GetAjaxAction

---

**A19-1 | Severity: CRITICAL | GetAjaxAction.execute — zero test coverage**

`GetAjaxAction.execute` (lines 22–56) has no test of any kind. The entire dispatch logic, all four action branches, all null-handling defaults, and the unconditional forward to `"success"` are completely untested. Any regression in routing logic, parameter handling, or DAO interaction will go undetected.

---

**A19-2 | Severity: CRITICAL | NullPointerException when sessDateFormat session attribute is absent (last_gps branch)**

Line 47:
```java
String dateFormat = ((String) request.getSession().getAttribute("sessDateFormat")).replaceAll("yyyy", "yy").replaceAll("M", "m");
```
`getAttribute("sessDateFormat")` can return `null`. The cast succeeds (casting `null` to `String` is legal in Java), but calling `.replaceAll(...)` on a null `String` reference throws `NullPointerException` at runtime. There is no null guard. No test exercises this path. This is a latent production crash for any request that arrives with a session that lacks `sessDateFormat`.

---

**A19-3 | Severity: CRITICAL | NullPointerException when session is null or session attributes are absent (last_gps branch)**

Lines 47–49 call `request.getSession()` (which always creates a session) but then cast the three session attributes (`sessDateFormat`, `sessDateTimeFormat`, `sessTimezone`) without null checks. In particular, `sessDateTimeFormat` and `sessTimezone` are stored directly into local variables that are immediately passed to `GPSDao.getUnitGPSData(...)` — if either attribute is null the downstream DAO receives null and may crash or produce malformed JSON output. No test exercises this path.

---

**A19-4 | Severity: HIGH | GetAjaxAction.execute — "last_gps" uses case-sensitive equals, inconsistent with other branches**

Lines 29, 33, 38 use `equalsIgnoreCase(...)` for the `getType`, `getPower`, and `getQcontent` branches.
Line 44 uses `action.equals("last_gps")` (case-sensitive) for the `last_gps` branch.
This inconsistency means `"Last_GPS"`, `"LAST_GPS"`, etc. silently fall through to the implicit else branch, returning an empty `arrXml` list instead of GPS data. No test verifies either the case-sensitive match or the case-mismatch fall-through.

---

**A19-5 | Severity: HIGH | GetAjaxAction.execute — unit parameter array not null-guarded before passing to GPSDao**

Line 45:
```java
String[] unit = request.getParameterValues("unit");
```
`getParameterValues` returns `null` when the parameter is absent. The value is passed directly to `GPSDao.getUnitGPSData(compId, unit, dateTimeFormat, timezone)` on line 51. While `GPSDao.getUnitGPSData` does include a null check for `unitIds` (returning an empty list), this contract is implicit and fragile. No test verifies the null-`unit` edge case, and the contract could silently break if the DAO is changed.

---

**A19-6 | Severity: HIGH | GetAjaxAction.execute — unknown/empty action value silently succeeds**

When `action` is any string other than the four recognised values (including the empty string `""` that is the null default), no branch is taken. The method sets `arrXml` to an empty `ArrayList` on request attribute `arrXml` and returns the `"success"` forward (line 55). The caller receives a 200 response with an empty list, which may silently mask a mistyped action parameter. No test verifies this fall-through behaviour.

---

**A19-7 | Severity: HIGH | getType / getPower delegate to SQL built by string concatenation — untested injection path**

`UnitDAO.getType(manu_id)` (lines 625–628 of UnitDAO) and `UnitDAO.getPower(manu_id, type_id)` (lines 665–670 of UnitDAO) build SQL by direct string concatenation of `manu_id` and `type_id`. These values originate verbatim from `request.getParameter(...)` in GetAjaxAction. There are no tests that exercise this path with adversarial or unexpected input. Although this is primarily a DAO-level concern, the absence of any action-level test means the injection surface is completely invisible to automated testing.

---

**A19-8 | Severity: MEDIUM | getQcontent branch — QuestionDAO instantiated inline, not mockable**

Line 42:
```java
QuestionDAO questionDAO = new QuestionDAO();
```
`QuestionDAO` is instantiated with `new` inside the method body. Unlike `unitDao` (a field) and `driverDAO` (a field in GetXmlAction), this prevents substitution of a mock or stub in any future test. The inline instantiation also means the DAO cannot be changed without modifying the action class.

---

**A19-9 | Severity: MEDIUM | GetAjaxAction.execute — no test for DAO exceptions propagating through throws Exception**

The method signature declares `throws Exception`. No test verifies that DAO-level `SQLException` or other exceptions thrown by `unitDao.getType`, `unitDao.getPower`, `questionDAO.getQuestionContentById`, or `GPSDao.getUnitGPSData` propagate correctly or are handled, and that the Struts framework receives them cleanly.

---

**A19-10 | Severity: LOW | getQcontent branch — qus_id and lan_id are not validated as numeric before SQL use**

Lines 40–43: `qus_id` defaults to `"0"` when null but is otherwise accepted verbatim and passed into `QuestionDAO.getQuestionContentById`, which embeds them in SQL. The null default does not prevent non-numeric strings from reaching the query. No test exercises non-numeric or empty values.

---

### GetXmlAction

---

**A19-11 | Severity: CRITICAL | GetXmlAction.execute — zero test coverage**

`GetXmlAction.execute` (lines 22–30) has no test of any kind. The session retrieval, null handling, DAO delegation, and forward are completely untested.

---

**A19-12 | Severity: CRITICAL | NullPointerException when getSession(false) returns null**

Line 25:
```java
HttpSession session = request.getSession(false);
```
`getSession(false)` returns `null` if no session exists. Line 26 immediately calls `session.getAttribute("sessCompId")` without a null check, producing a `NullPointerException` if the action is invoked without an active session (e.g., after session expiry, or in any direct API call without a session). No test exercises this path.

---

**A19-13 | Severity: HIGH | getAllDriver called with empty string sessCompId when attribute is absent**

Line 26:
```java
String sessCompId = (String) session.getAttribute("sessCompId")==null?"":(String)session.getAttribute("sessCompId");
```
When `sessCompId` is absent from the session, the empty string `""` is passed to `driverDAO.getAllDriver("", true)`. The DAO issues a query with `comp_id = ""`, which will either return zero rows or throw a database type-conversion error depending on the schema. The calling code has no special handling for this case, and no test verifies the behaviour.

---

**A19-14 | Severity: HIGH | GetXmlAction.execute — no test for DAO exceptions propagating through throws Exception**

The method signature declares `throws Exception`. No test verifies that exceptions thrown by `driverDAO.getAllDriver(...)` (e.g., `SQLException`) propagate correctly to the Struts framework.

---

**A19-15 | Severity: MEDIUM | driverDAO field not mockable — singleton acquired at field initialisation**

Line 20:
```java
private DriverDAO driverDAO = DriverDAO.getInstance();
```
`DriverDAO` is a singleton obtained at field-initialisation time. There is no constructor injection or setter, making the DAO impossible to substitute with a mock or stub in a unit test without byte-code manipulation or a test-framework extension (e.g., PowerMock). This architectural constraint also applies to `unitDao` in GetAjaxAction.

---

**A19-16 | Severity: LOW | GetXmlAction.execute — forward name "getDriverList" is not verified by any test**

Line 29 forwards to `"getDriverList"`. No test verifies that this forward name is correctly configured in the Struts configuration, meaning a misconfiguration (wrong forward name or missing JSP) would only be discovered at runtime.

---

## 4. Summary Table

| Finding | Severity | Description |
|---------|----------|-------------|
| A19-1 | CRITICAL | GetAjaxAction.execute — zero test coverage |
| A19-2 | CRITICAL | NPE when sessDateFormat session attribute is null (last_gps branch) |
| A19-3 | CRITICAL | NPE when sessDateTimeFormat or sessTimezone session attributes are null |
| A19-4 | HIGH | Inconsistent case-sensitivity: last_gps uses equals() vs equalsIgnoreCase() |
| A19-5 | HIGH | unit parameter array not null-guarded before GPSDao call |
| A19-6 | HIGH | Unknown/empty action value silently succeeds with empty response |
| A19-7 | HIGH | SQL injection surface via manu_id / type_id entirely untested |
| A19-8 | MEDIUM | QuestionDAO instantiated inline — cannot be mocked in tests |
| A19-9 | MEDIUM | DAO exceptions not tested for correct propagation (GetAjaxAction) |
| A19-10 | LOW | qus_id / lan_id not validated as numeric before DAO/SQL use |
| A19-11 | CRITICAL | GetXmlAction.execute — zero test coverage |
| A19-12 | CRITICAL | NPE when getSession(false) returns null (no session check) |
| A19-13 | HIGH | getAllDriver called with empty string when sessCompId absent |
| A19-14 | HIGH | DAO exceptions not tested for correct propagation (GetXmlAction) |
| A19-15 | MEDIUM | driverDAO / unitDao singletons not injectable — unit testing blocked |
| A19-16 | LOW | Forward name "getDriverList" not verified by any test |

**Total findings: 16**
- CRITICAL: 5 (A19-1, A19-2, A19-3, A19-11, A19-12)
- HIGH: 6 (A19-4, A19-5, A19-6, A19-7, A19-13, A19-14)
- MEDIUM: 3 (A19-8, A19-9, A19-15)
- LOW: 2 (A19-10, A19-16)

---

## 5. Recommended Test Cases (not exhaustive)

### GetAjaxAction

1. `action=getType`, valid `manu_id` — verify `arrXml` attribute set and `"success"` forward returned.
2. `action=getType`, `manu_id` null (parameter absent) — verify default `"0"` used.
3. `action=getPower`, valid `manu_id` + `type_id`.
4. `action=getPower`, `type_id` null.
5. `action=getQcontent`, valid `qus_id` + `lan_id`.
6. `action=getQcontent`, both parameters null.
7. `action=last_gps`, all session attributes set — happy path.
8. `action=last_gps`, `sessDateFormat` session attribute null — expect NPE or controlled error.
9. `action=last_gps`, `unit` parameter absent (null array) — verify empty GPS list returned.
10. `action=LAST_GPS` (upper case) — verify case-sensitive miss and empty-list fall-through.
11. `action=unknownValue` — verify empty `arrXml` and `"success"` forward.
12. DAO throws `SQLException` — verify exception propagates.

### GetXmlAction

1. Valid session with `sessCompId` set — verify `arrDriverList` attribute and `"getDriverList"` forward.
2. No session (`getSession(false)` returns null) — verify controlled error, not NPE.
3. Session exists but `sessCompId` attribute absent — verify empty-string default behaviour.
4. `driverDAO.getAllDriver` throws exception — verify propagation.
