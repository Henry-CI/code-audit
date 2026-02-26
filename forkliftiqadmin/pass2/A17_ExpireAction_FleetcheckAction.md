# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A17
**Date:** 2026-02-26
**Auditor model:** claude-sonnet-4-6

**Source files audited:**
- `src/main/java/com/action/ExpireAction.java`
- `src/main/java/com/action/FleetcheckAction.java`

**Test directory:** `src/test/java/`

---

## 1. Reading Evidence

### 1.1 ExpireAction.java

**Class:** `com.action.ExpireAction` (extends `org.apache.struts.action.Action`)
**File:** `src/main/java/com/action/ExpireAction.java`

**Fields / Constants:**

| Name | Type | Line | Notes |
|------|------|------|-------|
| `log` | `static Logger` | 30 | `InfoLogger.getLogger("com.action.ExpireAction")` |

**Methods:**

| Method | Signature | Lines | Notes |
|--------|-----------|-------|-------|
| `execute` | `ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 32–50 | Only method; the entire action logic |

**Imports used (runtime dependencies):**
- `SwitchLanguageAction.getCookie(request, "ckLanguage")` — static call to sibling action (line 40)
- `SwitchLanguageAction.getLocale(cookie.getValue())` — static call (line 43)
- `AdvertismentDAO.getInstance().getAllAdvertisement()` — singleton DAO, live DB call (line 47)
- `mapping.findForward("logout")` — Struts forward (line 49)

---

### 1.2 FleetcheckAction.java

**Class:** `com.action.FleetcheckAction` (extends `org.apache.struts.action.Action`)
**File:** `src/main/java/com/action/FleetcheckAction.java`

**Fields / Constants:**

| Name | Type | Line | Notes |
|------|------|------|-------|
| `log` | `static Logger` | 42 | `InfoLogger.getLogger("com.action.FleetcheckAction")` |

**Methods:**

| Method | Signature | Lines | Notes |
|--------|-----------|-------|-------|
| `execute` | `ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 44–116 | Three branches: "faulty", "restart", default submit |
| `saveResult` | `public int saveResult(String, String[], String[], String[], String, Long, Timestamp, String) throws Exception` | 119–139 | Builds and persists `ResultBean`; delegates to `ResultDAO.saveResult()` |
| `saveResultBarcode` | `public int saveResultBarcode(String, Map<String,String>, String, String, Timestamp, String) throws Exception` | 142–160 | Barcode-variant of result save; uses `Long.parseLong(driverId)` |
| `sendFleetCheckAlert` | `public Boolean sendFleetCheckAlert(PropertyMessageResources, String, int, CompanyBean, String[]) throws Exception` | 162–191 | Checks subscription, builds and sends alert email |

**Runtime dependencies:**
- `QuestionDAO`, `ResultDAO`, `SubscriptionDAO` — all make live DB calls
- `FleetCheckAlert` — builds HTML email content via additional DB calls
- `Util.sendMail(...)` — live SMTP call
- `RuntimeConf.EMAIL_DIGANOSTICS_TITLE`, `RuntimeConf.emailFrom` — mutable static fields
- `DateUtil.getLocalTime(...)`, `DateUtil.getLocalTimestamp(...)` — timezone-aware date utilities
- `StringUtils.isNotBlank(...)` — Apache Commons

---

## 2. Test Coverage Confirmation

### 2.1 Existing test files (full project)

| File | Package | Subject |
|------|---------|---------|
| `UnitCalibrationImpactFilterTest.java` | `com.calibration` | `UnitCalibrationImpactFilter` |
| `UnitCalibrationTest.java` | `com.calibration` | `UnitCalibration` |
| `UnitCalibratorTest.java` | `com.calibration` | `UnitCalibrator` |
| `ImpactUtilTest.java` | `com.util` | `ImpactUtil` |

### 2.2 Grep results for class names in test directory

Grep for `ExpireAction`, `FleetcheckAction`, `Fleetcheck` across all four test files: **zero matches**.

**Conclusion:** Neither `ExpireAction` nor `FleetcheckAction` is referenced, directly or indirectly, by any test in the project. Coverage is **0%** for both classes.

---

## 3. Coverage Gap Findings

---

### A17-1 | Severity: CRITICAL | ExpireAction.execute() — zero test coverage

`ExpireAction.execute()` (lines 32–50) is the sole method in the class and has no test of any kind. The method performs four distinct operations:
1. Constructs and saves a Struts `ActionErrors` message (`"error.expire"`).
2. Reads a `"ckLanguage"` cookie from the request.
3. If the cookie is present, resolves a `Locale` and sets it on the request as `Globals.LOCALE_KEY`.
4. Queries `AdvertismentDAO.getInstance().getAllAdvertisement()` and binds the result to the request attribute `"sessAds"`.
5. Returns the `"logout"` forward.

None of these behaviours has any automated verification.

---

### A17-2 | Severity: CRITICAL | FleetcheckAction.execute() — zero test coverage (all three branches)

`FleetcheckAction.execute()` (lines 44–116) contains three mutually exclusive execution paths selected by the `method` request parameter:

- **"faulty" branch** (lines 53–69): reads `qId` and `faulttext` parameters, fetches question and driver from session lists, constructs an HTML diagnostic email, and calls `Util.sendMail(...)`. No test exists.
- **"restart" branch** (lines 70–88): reads the company template from session, calls `QuestionDAO.getQuestionByUnitId(...)`, sets request attributes, and returns either `"single"` or `"multiple"` forward based on the template value. No test exists.
- **Default submit branch** (lines 89–115): reads form fields, calls `saveResult(...)`, conditionally calls `sendFleetCheckAlert(...)`, and returns `"success"` or `"globalfailure"`. No test exists.

---

### A17-3 | Severity: CRITICAL | FleetcheckAction.saveResult() — zero test coverage

`saveResult()` (lines 119–139) is `public` and independently callable. It:
- Iterates over parallel arrays `quesion_ids`, `anwsers`, and `faulties` to build `AnswerBean` objects.
- Conditionally sets faulty text only when `faulties != null` (line 126–128), which implies that a non-null but shorter `faulties` array will produce an `ArrayIndexOutOfBoundsException` — untested.
- Delegates to `ResultDAO.saveResult(resultBean, compId)`.
- Returns the result ID (0 on failure, positive integer on success).

No unit test exercises this method with any input combination.

---

### A17-4 | Severity: CRITICAL | FleetcheckAction.saveResultBarcode() — zero test coverage, dead-code risk

`saveResultBarcode()` (lines 142–160) is `public` but is never called from within `FleetcheckAction` itself. No caller in the project test suite exists, and the method is not exercised by any test. Additionally:
- It calls `Long.parseLong(driverId)` without null-checking or format validation, which will throw `NumberFormatException` on blank or non-numeric input.
- The `barcode` map is iterated with `barcode.keySet()` without null-checking the map — a `NullPointerException` risk.

---

### A17-5 | Severity: CRITICAL | FleetcheckAction.sendFleetCheckAlert() — zero test coverage

`sendFleetCheckAlert()` (lines 162–191) is `public` and contains significant conditional logic:
- Calls `SubscriptionDAO.checkCompFleetAlert(sessCompId)` — returns `null` if no alert subscription exists; the entire alert is skipped when `name == null`.
- Conditionally appends `subEmail` to the recipient list via `StringUtils.isNotBlank(subEmail)`.
- Iterates the optional `emails[]` array when non-null and non-empty, deduplicating against `rEmail`.
- Calls `Util.sendMail(...)` and returns the send result.
- Returns `false` (default) without calling `sendMail` when `name == null`.

None of these paths — including the skip-when-no-subscription path — is tested.

---

### A17-6 | Severity: HIGH | ExpireAction — null cookie path not tested

In `execute()` lines 41–45, the code branches on `cookie != null`. When no `"ckLanguage"` cookie is present, the locale is never set and the request continues without `Globals.LOCALE_KEY`. This branch is the other half of a two-branch conditional and is equally untested. A regression here would silently produce the wrong locale for all expired-session pages.

---

### A17-7 | Severity: HIGH | ExpireAction — AdvertismentDAO failure propagates uncaught

`AdvertismentDAO.getInstance().getAllAdvertisement()` (line 47) throws `Exception` on database error. `execute()` declares `throws Exception` but provides no catch block or fallback. Any database failure during session expiry will propagate to the Struts framework as an unhandled exception, returning an error page instead of the logout page. No test exercises this error path.

---

### A17-8 | Severity: HIGH | FleetcheckAction "faulty" branch — NullPointerException on empty session driver list

In the "faulty" branch (line 57):
```java
String driverName = (sessArrDriver.get(0)).getFirst_name() + " " + (sessArrDriver.get(0)).getLast_name();
```
`sessArrDriver` is cast directly from session attribute `"arrDriver"` without null checking (line 56). If the session attribute is absent or the list is empty, `get(0)` throws `NullPointerException` or `IndexOutOfBoundsException`. No test covers this.

---

### A17-9 | Severity: HIGH | FleetcheckAction "faulty" branch — NullPointerException on empty question list

In the "faulty" branch (line 60):
```java
String qName = (arrQues.get(0)).getContent();
```
`QuestionDAO.getQuestionById(qId)` can return an empty list if `qId` is invalid or the question is deleted. Calling `.get(0)` on an empty list throws `IndexOutOfBoundsException`. No test covers this.

---

### A17-10 | Severity: HIGH | FleetcheckAction "faulty" branch — blank/null qId not validated

`qId` is read from the request parameter with a null-safe fallback to `""` (line 54), but an empty string is then passed directly to `QuestionDAO.getQuestionById("")`. The DAO will execute a SQL query with an empty or malformed `WHERE id = ''` clause, likely returning an empty result set and causing the `IndexOutOfBoundsException` described in A17-9. No input validation test exists.

---

### A17-11 | Severity: HIGH | FleetcheckAction default branch — saveResult() failure path not fully tested

In the default submit branch (lines 104–114), when `saveResult()` returns `<= 0`, the code adds a global error and forwards to `"globalfailure"`. This is the only error-handling path in the branch, and it is untested. A developer change that alters the `<= 0` condition or the error key `"errors.global"` would go undetected.

---

### A17-12 | Severity: HIGH | FleetcheckAction "restart" branch — NullPointerException when sessArrComp is null or empty

In the "restart" branch (line 71):
```java
String template = sessArrComp.get(0).getTemplate();
```
`sessArrComp` is cast from the session attribute `"sessArrComp"` at line 50 without null checking. If the session attribute is missing or the list is empty, this throws `NullPointerException` or `IndexOutOfBoundsException`. No test covers this.

---

### A17-13 | Severity: HIGH | FleetcheckAction — session.getAttribute("sessCompId") null-safe only by default-to-empty-string, never validated

Line 48:
```java
String sessCompId = (String) (session.getAttribute("sessCompId") == null ? "" : session.getAttribute("sessCompId"));
```
When `sessCompId` is empty string, it is passed downstream to `QuestionDAO.getQuestionByUnitId(...)`, `saveResult(...)`, and `sendFleetCheckAlert(...)`. These DAO methods embed `sessCompId` directly into SQL strings. An empty `compId` would produce malformed queries or return wrong results. No test validates the empty-compId path.

---

### A17-14 | Severity: MEDIUM | FleetcheckAction.saveResultBarcode() — NumberFormatException on non-numeric driverId

Line 152:
```java
resultBean.setDriver_id(Long.parseLong(driverId));
```
`driverId` is a `String` parameter with no format guard. A blank, null, or non-numeric value produces `NumberFormatException`. Since this method is public and called from external code (likely an API action), the absence of any test means this failure mode is invisible.

---

### A17-15 | Severity: MEDIUM | FleetcheckAction "faulty" branch — email recipients not validated before send

Lines 63–68 construct `rEmail` by appending `subEmail` when non-null and non-empty, then call `Util.sendMail(...)`. There is no validation that `rEmail` is a well-formed email address. A malformed `company.email` value from the database could cause a silent send failure or exception. No test covers recipient construction.

---

### A17-16 | Severity: MEDIUM | FleetcheckAction.sendFleetCheckAlert() — emails[] deduplication logic not tested

Lines 177–183 deduplicate additional email addresses against the existing `rEmail` string using `rEmail.contains(emails[i])`. This is a substring check, not an exact email match; a short email address could be incorrectly considered a duplicate if it appears as a substring of another. No test validates this logic.

---

### A17-17 | Severity: MEDIUM | FleetcheckAction.saveResult() — parallel array length mismatch causes ArrayIndexOutOfBoundsException

In `saveResult()` lines 122–130, the loop iterates over `quesion_ids.length` but accesses `anwsers[i]` and `faulties[i]` (when non-null) with the same index. If `anwsers` or `faulties` (when non-null) is shorter than `quesion_ids`, an `ArrayIndexOutOfBoundsException` is thrown. No validation of array lengths exists and no test verifies consistent input.

---

### A17-18 | Severity: MEDIUM | FleetcheckAction "restart" branch — template value not in {"single","multiple"} falls through to "multiple" forward

Lines 84–88:
```java
if (template.equalsIgnoreCase("single")) {
    return mapping.findForward("single");
} else {
    return mapping.findForward("multiple");
}
```
Any template value other than `"single"` (including null, blank, or an unknown string) silently forwards to `"multiple"`. This implicit default is not documented and is not tested.

---

### A17-19 | Severity: MEDIUM | ExpireAction — getLocale() called with cookie.getValue() which may be null or unknown language code

`SwitchLanguageAction.getLocale()` returns `null` for any language code that is not "1", "2", "3", or "4" (including blank string). In `ExpireAction.execute()` line 44, the returned `null` locale is then set as `Globals.LOCALE_KEY` on the request:
```java
request.setAttribute(Globals.LOCALE_KEY, locale);
```
Setting a null locale could cause a `NullPointerException` later in the Struts framework when it attempts to use the locale for message resolution. No test covers this path.

---

### A17-20 | Severity: MEDIUM | FleetcheckAction — request.getSession(false) may return null

Line 47:
```java
HttpSession session = request.getSession(false);
```
`getSession(false)` returns `null` when no session exists. The very next line (48) calls `session.getAttribute(...)` without a null check. A request without an existing session will throw `NullPointerException`. This is a realistic scenario (expired session, direct URL access), and no test covers it.

---

### A17-21 | Severity: LOW | FleetcheckAction — method parameter falls through to default submit on any unrecognised value

Line 51:
```java
String fleetAction = request.getParameter("method") == null ? "" : request.getParameter("method");
```
Any value for `method` that is not `"faulty"` or `"restart"` (case-insensitive) silently routes to the default submit branch, which attempts to read form fields and save a result. A misspelled or unexpected `method` value will cause a partially constructed result to be saved. No test exercises this routing.

---

### A17-22 | Severity: LOW | ExpireAction — ActionErrors always added unconditionally

Lines 35–38 always add an `"error.expire"` error message regardless of why the action was reached. If a future caller reaches `ExpireAction` in a non-expiry context, the error will be misleading. The unconditional nature of this has never been verified by a test.

---

### A17-23 | Severity: LOW | FleetcheckAction — static mutable RuntimeConf fields used without indirection

Lines 68 (`RuntimeConf.EMAIL_DIGANOSTICS_TITLE`, `RuntimeConf.emailFrom`) and 186 (`RuntimeConf.emailFrom`) access public static non-final fields. These values can be altered at runtime by other code, making email behaviour difficult to test in isolation. No test demonstrates the expected values are stable.

---

### A17-24 | Severity: INFO | FleetcheckAction.saveResultBarcode() — never called from FleetcheckAction; possible dead code

`saveResultBarcode()` has `public` visibility and accepts a `Map<String,String>` barcode argument, unlike `saveResult()` which accepts parallel arrays. The method is not called from within `FleetcheckAction.execute()`, and no test exercises or documents its intended caller. If the API action that calls it was removed or refactored, this method would become silently dead. Recommend confirming the caller and adding a cross-reference test or removing the method.

---

### A17-25 | Severity: INFO | Test infrastructure — no Struts mock framework present

The four existing tests cover only pure-Java utility and calibration logic. There is no Struts mock framework (e.g., StrutsTestCase, Mockito-based mock HTTP layer, or Spring MockMvc equivalent) present in the project. This means integration-level tests for any Action class would require significant infrastructure investment before a single test could be written.

---

## 4. Summary Table

| Finding | Severity | Description |
|---------|----------|-------------|
| A17-1 | CRITICAL | `ExpireAction.execute()` — zero test coverage |
| A17-2 | CRITICAL | `FleetcheckAction.execute()` — zero test coverage for all three branches |
| A17-3 | CRITICAL | `FleetcheckAction.saveResult()` — zero test coverage |
| A17-4 | CRITICAL | `FleetcheckAction.saveResultBarcode()` — zero test coverage, NPE and NFE risks |
| A17-5 | CRITICAL | `FleetcheckAction.sendFleetCheckAlert()` — zero test coverage |
| A17-6 | HIGH | `ExpireAction` — null cookie branch not tested |
| A17-7 | HIGH | `ExpireAction` — `AdvertismentDAO` failure propagates uncaught through `execute()` |
| A17-8 | HIGH | `FleetcheckAction` "faulty" — NPE/IOOBE when session driver list is null or empty |
| A17-9 | HIGH | `FleetcheckAction` "faulty" — NPE/IOOBE when `getQuestionById` returns empty list |
| A17-10 | HIGH | `FleetcheckAction` "faulty" — blank `qId` not validated before DAO call |
| A17-11 | HIGH | `FleetcheckAction` default — `saveResult()` failure path (`globalfailure` forward) not tested |
| A17-12 | HIGH | `FleetcheckAction` "restart" — NPE/IOOBE when `sessArrComp` is null or empty |
| A17-13 | HIGH | `FleetcheckAction` — empty `sessCompId` passed to SQL-building DAO methods unchecked |
| A17-14 | MEDIUM | `saveResultBarcode()` — `NumberFormatException` on non-numeric `driverId` |
| A17-15 | MEDIUM | `FleetcheckAction` "faulty" — email recipients not validated before `sendMail` |
| A17-16 | MEDIUM | `sendFleetCheckAlert()` — substring-based email deduplication is incorrect |
| A17-17 | MEDIUM | `saveResult()` — parallel array length mismatch causes `ArrayIndexOutOfBoundsException` |
| A17-18 | MEDIUM | "restart" branch — unknown template value silently forwards to `"multiple"` |
| A17-19 | MEDIUM | `ExpireAction` — `getLocale()` may return `null` locale set on request |
| A17-20 | MEDIUM | `FleetcheckAction` — `getSession(false)` may return null; NPE on line 48 |
| A17-21 | LOW | Unknown `method` parameter silently routes to default submit branch |
| A17-22 | LOW | `ExpireAction` — error message added unconditionally, regardless of context |
| A17-23 | LOW | `RuntimeConf` static mutable fields make email behaviour untestable in isolation |
| A17-24 | INFO | `saveResultBarcode()` has no internal caller — possible dead code |
| A17-25 | INFO | No Struts mock framework exists; Action test infrastructure entirely absent |

**Total findings: 25**
**CRITICAL: 5 | HIGH: 8 | MEDIUM: 7 | LOW: 3 | INFO: 2**
