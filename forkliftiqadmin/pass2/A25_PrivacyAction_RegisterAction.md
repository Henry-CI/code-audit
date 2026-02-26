# Pass 2 Test-Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A25
**Date:** 2026-02-26
**Files Audited:**
- `src/main/java/com/action/PrivacyAction.java`
- `src/main/java/com/action/RegisterAction.java`

---

## 1. Reading Evidence

### 1.1 PrivacyAction.java

**Class:** `com.action.PrivacyAction` extends `org.apache.struts.action.Action`

**Fields / Constants:** None declared in this class.

**Methods:**

| Method | Line | Signature |
|--------|------|-----------|
| `execute` | 16 | `public ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` |

**Key logic inside `execute` (lines 20–25):**
- Line 20: `HttpSession session = request.getSession(false);` — obtains existing session without creating one.
- Line 21: Reads `sessCompId` from session; if attribute is `null` the ternary coalesces to `""`.
- Line 22: Obtains singleton `CompanyDAO` instance.
- Line 24: Calls `companyDAO.updateCompPrivacy(sessCompId)` — issues `UPDATE company SET privacy = false WHERE id = ?` using `Integer.parseInt(compId)`.
- Line 25: Returns hard-coded forward `"successAdmin"`.

**Imports used:** `CompanyDAO`, standard Struts, `HttpServletRequest/Response/Session`.

---

### 1.2 RegisterAction.java

**Class:** `com.action.RegisterAction` extends `org.apache.struts.action.Action`

**Fields / Constants:**

| Field | Line | Type | Description |
|-------|------|------|-------------|
| `log` | 23 | `static Logger` | Log4j logger obtained via `InfoLogger.getLogger` |
| `driverDao` | 25 | `DriverDAO` | Instance-level singleton obtained at field-initialisation time via `DriverDAO.getInstance()` |

**Methods:**

| Method | Line | Signature |
|--------|------|-----------|
| `execute` | 27 | `public ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` |

**Key logic inside `execute` (lines 30–89):**
- Line 30: `session = request.getSession(false)` — obtains existing session.
- Line 31: Casts `actionForm` to `RegisterActionForm` (unsafe cast, no guard).
- Line 32: Reads `sessCompId` via `request.getSession()` (second session acquisition; *different* call from line 30).
- Line 33: Reads `sessArrComp` from the session obtained by `getSession(false)`.
- Line 34: `sessArrComp.get(0).getTemplate()` — no null/empty-list guard.
- Lines 36–38: Reads `fname`, `lname`, `licence` from form.
- Lines 40–47: Constructs `DriverBean` and populates fields from form.
- Line 49: Branch 1 — `driverDao.checkDriverByNm(...)` returns `true` → duplicate name error → `findForward("failure")`.
- Line 57: Branch 2 — `driverDao.checkDriverByLic(...)` returns `true` → duplicate licence error → `findForward("failure")`.
- Line 65: Branch 3 — `driverDao.saveDriverInfo(driverbean, ...)` returns `true` → success path.
  - Line 66: `driverDao.getDriverByNm(...)` result stored in session as `"arrDriver"`.
  - Line 68: `new QuestionDAO()` instantiated directly (not through singleton/factory).
  - Line 69: `quesionDao.getQuestionByUnitId(...)` result stored in request as `"arrQues"`.
  - Lines 71: Stores `veh_id` in request.
  - Lines 73–79: Template branch: `"multiple"` → `findForward("multiple")`; `"single"` → `findForward("single")`; else → `findForward("multiple")` (default fallback silently treats any unknown template as multiple).
- Lines 81–88: Branch 4 — `saveDriverInfo` returns `false` → general error → `findForward("failure")`.

---

## 2. Test-Coverage Confirmation

### 2.1 Existing Test Files (complete project inventory)

```
src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java
src/test/java/com/calibration/UnitCalibrationTest.java
src/test/java/com/calibration/UnitCalibratorTest.java
src/test/java/com/util/ImpactUtilTest.java
```

### 2.2 Grep Results — Direct Coverage

Search pattern: `PrivacyAction|RegisterAction`
Result: **No matches found** in any test file.

### 2.3 Grep Results — Indirect Coverage via Dependencies

Search pattern: `CompanyDAO|DriverDAO|QuestionDAO|updateCompPrivacy|checkDriverByNm|checkDriverByLic|saveDriverInfo|getDriverByNm|getQuestionByUnitId`
Result: **No matches found** in any test file.

**Conclusion:** Both `PrivacyAction` and `RegisterAction` have **0% test coverage** — no direct tests, no indirect tests, no stubs, no mocks.

---

## 3. Coverage Gaps and Findings

---

### PrivacyAction — Findings

---

**A25-1 | Severity: CRITICAL | No test class exists for PrivacyAction**

`PrivacyAction` has zero test coverage. The sole entry point, `execute()`, is completely untested. Any regression in session handling, DAO invocation, or forward routing will go undetected.

---

**A25-2 | Severity: CRITICAL | Null session causes immediate NullPointerException — no test**

```java
// PrivacyAction.java line 20
HttpSession session = request.getSession(false);
// line 21
String sessCompId = (String) session.getAttribute("sessCompId") == null ? "" : ...
```

`request.getSession(false)` returns `null` when no session exists. The very next line dereferences `session` without a null guard, producing an unhandled `NullPointerException` at line 21. There is no test that exercises this path and no `null` guard in the code.

---

**A25-3 | Severity: CRITICAL | Empty-string compId passed to updateCompPrivacy causes NumberFormatException — no test**

```java
// PrivacyAction.java line 21 — sessCompId defaults to ""
// CompanyDAO.java line 346
ps.setInt(1, Integer.parseInt(compId)); // throws NumberFormatException when compId == ""
```

When `sessCompId` is absent from the session the ternary on line 21 resolves it to `""`. This value is then passed directly to `updateCompPrivacy`, which calls `Integer.parseInt("")` and throws a `NumberFormatException` that propagates as a checked `Exception` from `execute()`. No test covers this path.

---

**A25-4 | Severity: HIGH | DAO exception propagation is untested**

`CompanyDAO.updateCompPrivacy` wraps all failures in `throw new SQLException(e.getMessage())`. That exception propagates through `PrivacyAction.execute()` (declared `throws Exception`) to the Struts framework, which will render an uncontrolled error page. No test verifies the failure branch or confirms that an appropriate error forward (or error page) is configured.

---

**A25-5 | Severity: HIGH | Successful privacy update forward is untested**

The happy-path forward `"successAdmin"` (line 25) is never exercised by a test. If the forward name is misconfigured in `struts-config.xml` the error is only discovered at runtime.

---

**A25-6 | Severity: MEDIUM | sessCompId is the empty string when attribute is missing — silent data corruption possible**

When `sessCompId` is `null` in the session, line 21 coalesces it to `""`. As noted in A25-3 this causes a `NumberFormatException`. However, if the attribute is present but malformed (e.g. non-numeric), `Integer.parseInt` still throws. Neither case is validated before the DAO call and neither is tested.

---

**A25-7 | Severity: LOW | TODO comment on auto-generated method stub — no coverage baseline**

```java
// PrivacyAction.java line 19
// TODO Auto-generated method stub
```

The stale TODO indicates the method was never completed beyond its initial scaffolding. No test was written alongside it to define intended behaviour.

---

### RegisterAction — Findings

---

**A25-8 | Severity: CRITICAL | No test class exists for RegisterAction**

`RegisterAction` has zero test coverage. All six code paths inside `execute()` are completely untested.

---

**A25-9 | Severity: CRITICAL | Null session from getSession(false) causes NullPointerException — no test**

```java
// RegisterAction.java line 30
HttpSession session = request.getSession(false);
// line 33
ArrayList<CompanyBean> sessArrComp = (ArrayList<CompanyBean>) session.getAttribute("sessArrComp");
```

If no active session exists, `session` is `null` and line 33 throws `NullPointerException`. No test covers this path and no null guard exists.

---

**A25-10 | Severity: CRITICAL | Two separate session objects are used — consistency hazard, no test**

```java
// line 30
HttpSession session = request.getSession(false);          // may return null
// line 32
String sessCompId = (String) request.getSession().getAttribute("sessCompId");  // always creates
```

Line 32 calls `request.getSession()` (no argument), which creates a new session if none exists, while line 30 uses `getSession(false)`. If a session does not already exist, line 30 returns `null` (causing NPE at line 33) while line 32 creates a fresh empty session. Even if a session does exist, reading `sessCompId` from `request.getSession()` and `sessArrComp` from the saved `session` reference are logically equivalent but architecturally inconsistent. No test verifies these two references point to the same underlying session under all container configurations.

---

**A25-11 | Severity: CRITICAL | sessArrComp null or empty causes NullPointerException or IndexOutOfBoundsException — no test**

```java
// line 33
ArrayList<CompanyBean> sessArrComp = (ArrayList<CompanyBean>) session.getAttribute("sessArrComp");
// line 34
String template = (String) sessArrComp.get(0).getTemplate();
```

If `sessArrComp` is `null` (attribute absent), line 34 throws `NullPointerException`. If `sessArrComp` is an empty list, `get(0)` throws `IndexOutOfBoundsException`. No test covers either path and there is no defensive guard.

---

**A25-12 | Severity: CRITICAL | Unchecked cast from session attribute is untested**

```java
// line 33
ArrayList<CompanyBean> sessArrComp = (ArrayList<CompanyBean>) session.getAttribute("sessArrComp");
```

If the session attribute holds an incompatible type, this cast produces `ClassCastException` at runtime. No test validates the cast contract.

---

**A25-13 | Severity: HIGH | Duplicate driver name path (Branch 1) is untested**

```java
// lines 49–56
if (driverDao.checkDriverByNm(sessCompId, fname, lname, null, true)) {
    ...
    return mapping.findForward("failure");
}
```

The duplicate-name error path, including the construction and saving of `ActionErrors` and the `"failure"` forward, is never exercised by a test. The message key `"error.duplicateName"` is not verified against the message resources file.

---

**A25-14 | Severity: HIGH | Duplicate licence path (Branch 2) is untested**

```java
// lines 57–64
} else if (driverDao.checkDriverByLic(sessCompId, licence, null, true)) {
    ...
    return mapping.findForward("failure");
}
```

The duplicate-licence error path is untested. The message key `"error.duplcateLicence"` contains a probable typo (`duplcate` vs `duplicate`) that is undetected due to lack of tests.

---

**A25-15 | Severity: HIGH | Successful save path (Branch 3) is untested — all three template sub-branches**

```java
// lines 65–79
} else if (driverDao.saveDriverInfo(driverbean, sessArrComp.get(0).getDateFormat())) {
    ...
    if (template.equalsIgnoreCase("multiple")) {
        return mapping.findForward("multiple");
    } else if (template.equalsIgnoreCase("single")) {
        return mapping.findForward("single");
    } else {
        return mapping.findForward("multiple");  // silent default
    }
}
```

None of the three template sub-branches (`"multiple"`, `"single"`, unknown/default) is covered by any test. The silent default fallback to `"multiple"` for any unrecognised template value is particularly risky and warrants an explicit test.

---

**A25-16 | Severity: HIGH | saveDriverInfo failure path (Branch 4) is untested**

```java
// lines 81–88
} else {
    ActionErrors errors = new ActionErrors();
    ActionMessage msg = new ActionMessage("errors.general");
    errors.add("RegisterError", msg);
    saveErrors(request, errors);
    ...
    return mapping.findForward("failure");
}
```

The path where `saveDriverInfo` returns `false` is completely untested. The message key `"errors.general"` is not verified.

---

**A25-17 | Severity: HIGH | DAO exception propagation through execute() is untested**

`checkDriverByNm`, `checkDriverByLic`, `saveDriverInfo`, `getDriverByNm`, and `getQuestionByUnitId` all declare checked exceptions (`SQLException`, `Exception`). `execute()` is declared `throws Exception`, so any DAO exception propagates to the Struts framework as an unhandled error. No test verifies the error-handling behaviour under DAO failure.

---

**A25-18 | Severity: MEDIUM | QuestionDAO is instantiated with new rather than via a factory — testability gap**

```java
// line 68
QuestionDAO quesionDao = new QuestionDAO();
```

Unlike `DriverDAO`, which uses a singleton (`DriverDAO.getInstance()`), `QuestionDAO` is constructed inline with `new`. This prevents substituting a test double and makes the success branch (Branch 3) impossible to unit-test without a live database. The field spelling (`quesionDao` rather than `questionDao`) also indicates a lack of review.

---

**A25-19 | Severity: MEDIUM | driverDao initialised at field-declaration time — cannot be mocked without reflection**

```java
// line 25
private DriverDAO driverDao = DriverDAO.getInstance();
```

The `DriverDAO` instance is captured in a `private` field with no setter or constructor injection. Unit-testing `RegisterAction` requires either Mockito's `@InjectMocks` / field-level injection via reflection or PowerMock to intercept the static `getInstance()` call. The current design makes clean unit testing unnecessarily difficult.

---

**A25-20 | Severity: MEDIUM | template comparison uses equalsIgnoreCase but unknown value silently routes to "multiple" — no test**

```java
// lines 73–79
if (template.equalsIgnoreCase("multiple")) { ... }
else if (template.equalsIgnoreCase("single")) { ... }
else { return mapping.findForward("multiple"); }
```

An empty string, `null` (which would throw NPE on `.equalsIgnoreCase`), or any unrecognised template value silently falls through to the `"multiple"` forward. A `null` template value from `CompanyBean.getTemplate()` would cause `NullPointerException` here. There is no test for any of these edge cases.

---

**A25-21 | Severity: MEDIUM | Probable typo in message key "error.duplcateLicence" is undetected — no test**

```java
// line 59
ActionMessage msg = new ActionMessage("error.duplcateLicence");
```

The key `"duplcate"` is missing the `i` from `"duplicate"`. Without a test that validates the message key resolves to a non-empty, non-key-name string from the message resources, this typo will silently render the raw key to the user in production.

---

**A25-22 | Severity: MEDIUM | sessCompId from getSession() may be null — passed without null check to DAO methods**

```java
// line 32
String sessCompId = (String) request.getSession().getAttribute("sessCompId");
```

No null check is performed on `sessCompId`. It is subsequently passed to `checkDriverByNm` (line 49), `checkDriverByLic` (line 57), `saveDriverInfo` via `driverbean.setComp_id(sessCompId)` (line 47), and `getDriverByNm` (line 66). Each of these DAO methods calls `Long.parseLong(compId)` or equivalent, producing `NumberFormatException` on null or non-numeric input. No test covers this.

---

**A25-23 | Severity: LOW | getDateFormat() on sessArrComp.get(0) is called a second time in saveDriverInfo — no test on date-format propagation**

```java
// line 65
} else if (driverDao.saveDriverInfo(driverbean, sessArrComp.get(0).getDateFormat())) {
```

The date format is read from `sessArrComp.get(0)` again (first read was `getTemplate()` at line 34). No test validates that a null or malformed date format string is handled correctly by `saveDriverInfo`, nor that the correct format is forwarded.

---

**A25-24 | Severity: LOW | arrDriver stored in session may be empty list — downstream consumers untested**

```java
// line 66–67
List<DriverBean> arrDriver = driverDao.getDriverByNm(sessCompId, fname, lname, true);
session.setAttribute("arrDriver", arrDriver);
```

`getDriverByNm` can return an empty list (the driver was just saved but lookup returned nothing). No test verifies that downstream pages consuming `arrDriver` from the session handle an empty list gracefully.

---

**A25-25 | Severity: LOW | veh_id and attachment attributes are set on request in error paths but not verified by any test**

```java
// lines 54–55, 62–63, 86–87
request.setAttribute("veh_id", registerActionForm.getVeh_id());
request.setAttribute("attachment", registerActionForm.getAttachment());
```

These attributes are set in all three failure branches to preserve form state for re-display. No test confirms the attribute names are correct or that values survive the forward round-trip to the JSP.

---

## 4. Summary Table

| Finding | Severity | Class | Description |
|---------|----------|-------|-------------|
| A25-1 | CRITICAL | PrivacyAction | No test class exists |
| A25-2 | CRITICAL | PrivacyAction | Null session → NPE on line 21 |
| A25-3 | CRITICAL | PrivacyAction | Empty sessCompId → NumberFormatException in updateCompPrivacy |
| A25-4 | HIGH | PrivacyAction | DAO exception propagation untested |
| A25-5 | HIGH | PrivacyAction | Happy-path forward "successAdmin" untested |
| A25-6 | MEDIUM | PrivacyAction | Malformed/absent compId silently becomes "" before DAO call |
| A25-7 | LOW | PrivacyAction | Stale TODO comment; no baseline behaviour defined |
| A25-8 | CRITICAL | RegisterAction | No test class exists |
| A25-9 | CRITICAL | RegisterAction | Null session from getSession(false) → NPE on line 33 |
| A25-10 | CRITICAL | RegisterAction | Two different getSession() calls — consistency hazard |
| A25-11 | CRITICAL | RegisterAction | sessArrComp null or empty → NPE / IndexOutOfBoundsException |
| A25-12 | CRITICAL | RegisterAction | Unchecked session cast — ClassCastException untested |
| A25-13 | HIGH | RegisterAction | Duplicate-name failure branch (Branch 1) untested |
| A25-14 | HIGH | RegisterAction | Duplicate-licence failure branch (Branch 2) untested |
| A25-15 | HIGH | RegisterAction | Successful save path (Branch 3) — all three template sub-branches untested |
| A25-16 | HIGH | RegisterAction | saveDriverInfo false path (Branch 4) untested |
| A25-17 | HIGH | RegisterAction | DAO exception propagation through execute() untested |
| A25-18 | MEDIUM | RegisterAction | QuestionDAO constructed with new — prevents mocking |
| A25-19 | MEDIUM | RegisterAction | driverDao private field — no injection point for test doubles |
| A25-20 | MEDIUM | RegisterAction | Unknown/null template silently falls to "multiple"; null causes NPE |
| A25-21 | MEDIUM | RegisterAction | Typo in message key "error.duplcateLicence" undetected |
| A25-22 | MEDIUM | RegisterAction | sessCompId may be null — NumberFormatException in DAO calls |
| A25-23 | LOW | RegisterAction | Date-format propagation to saveDriverInfo untested |
| A25-24 | LOW | RegisterAction | Empty arrDriver list stored in session — downstream impact untested |
| A25-25 | LOW | RegisterAction | veh_id/attachment request attributes in error paths not verified |

**Total findings: 25**
- CRITICAL: 8
- HIGH: 7
- MEDIUM: 6
- LOW: 4

---

## 5. Recommended Test Scenarios

### PrivacyAction

1. `execute()` — no active session → assert framework receives the NPE or configure action to return an error forward.
2. `execute()` — session present, `sessCompId` absent (null) → assert NPE or `NumberFormatException` is handled.
3. `execute()` — session present, `sessCompId = "abc"` (non-numeric) → assert `NumberFormatException` handling.
4. `execute()` — session present, valid numeric `sessCompId`, DAO succeeds → assert `ActionForward.getName()` equals `"successAdmin"`.
5. `execute()` — session present, valid `sessCompId`, DAO throws `SQLException` → assert exception propagates correctly.

### RegisterAction

1. `execute()` — no session → assert NPE is caught / error forward returned.
2. `execute()` — `sessArrComp` null in session → assert NPE handling.
3. `execute()` — `sessArrComp` empty list → assert `IndexOutOfBoundsException` handling.
4. `execute()` — `sessCompId` null → assert `NumberFormatException` handling.
5. `execute()` — `checkDriverByNm` returns `true` → assert `"failure"` forward and correct `ActionError` key.
6. `execute()` — `checkDriverByLic` returns `true` → assert `"failure"` forward and correct `ActionError` key (verify typo resolution).
7. `execute()` — both duplicate checks false, `saveDriverInfo` returns `true`, template `"multiple"` → assert `"multiple"` forward and session/request attributes populated.
8. `execute()` — save succeeds, template `"single"` → assert `"single"` forward.
9. `execute()` — save succeeds, template `"UNKNOWN"` → assert default `"multiple"` forward.
10. `execute()` — save succeeds, template `null` → assert NPE handling.
11. `execute()` — `saveDriverInfo` returns `false` → assert `"failure"` forward and `"errors.general"` message.
12. `execute()` — any DAO method throws `SQLException` → assert exception propagation.
