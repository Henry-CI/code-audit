# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent:** A01
**Files audited:**
- `src/main/java/com/action/AdminAddAlertAction.java`
- `src/main/java/com/action/AdminAlertAction.java`

---

## Reading Evidence

### AdminAddAlertAction

**Class:** `com.action.AdminAddAlertAction` (extends `org.apache.struts.action.Action`)
**File:** `src/main/java/com/action/AdminAddAlertAction.java`

**Methods:**

| Method | Line |
|--------|------|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | 20 |

**Fields/Constants defined:** none (all variables are local to `execute`)

**Local variables of significance in `execute`:**

| Variable | Line | Source |
|----------|------|--------|
| `session` | 21 | `request.getSession(false)` |
| `sessCompId` | 22 | `session.getAttribute("sessCompId")` cast to `String` |
| `src` | 23 | `request.getParameter("src")` |
| `sessUserId` | 24 | `session.getAttribute("sessUserId")` cast to `Integer` |
| `alertAction` | 25 | `(AdminAlertActionForm) actionForm` |

**Branch structure:**
- Line 27: `src.equalsIgnoreCase("alert")` → calls `CompanyDAO.addUserSubscription`, sets `alertList` via `getAlertList()`, forwards `adminalerts`
- Line 30: `src.equalsIgnoreCase("report")` → calls `CompanyDAO.addUserSubscription`, sets `alertList` via `getReportList()`, forwards `adminalerts`
- Line 33: else (any other/missing `src`) → adds global error, forwards `adminalerts`

---

### AdminAlertAction

**Class:** `com.action.AdminAlertAction` (extends `org.apache.struts.action.Action`)
**File:** `src/main/java/com/action/AdminAlertAction.java`

**Methods:**

| Method | Line |
|--------|------|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | 18 |

**Fields/Constants defined:** none (all variables are local to `execute`)

**Local variables of significance in `execute`:**

| Variable | Line | Source |
|----------|------|--------|
| `action` | 22 | `request.getParameter("action")` |

**Branch structure:**
- Line 24: `action.equalsIgnoreCase("alerts")` → sets `alertList` via `CompanyDAO.getAlertList()`, forwards `adminalerts`
- Line 27: `action.equalsIgnoreCase("reports")` → sets `alertList` via `CompanyDAO.getReportList()`, forwards `adminalerts`
- Line 30: else → adds global error, forwards `globalfailure`

---

## Test Coverage Confirmation

Grep of `src/test/java/` for `AdminAddAlertAction` and `AdminAlertAction`: **no matches found**.

Existing test files in the project:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

None of these reference either audited class directly or indirectly. Coverage is **0%** for both action classes.

---

## Findings

### AdminAddAlertAction

**A01-1 | Severity: CRITICAL | Null session causes NullPointerException — no test**

`execute()` line 21 calls `request.getSession(false)`, which returns `null` when no session exists. Lines 22 and 24 immediately dereference `session` without a null guard (`session.getAttribute(...)`). A request with no active session throws `NullPointerException`, producing an unhandled 500 error. There is no test exercising the null-session path.

---

**A01-2 | Severity: CRITICAL | ClassCastException on sessUserId when attribute is not Integer — no test**

Line 24 unconditionally casts `session.getAttribute("sessUserId")` to `Integer`. If the attribute was stored as any other type (e.g., `String`, `Long`) the cast throws `ClassCastException` at runtime. No test covers this path.

---

**A01-3 | Severity: HIGH | Null sessUserId converted to "0" and silently used as real user ID — no test**

When `session.getAttribute("sessUserId")` is `null`, line 24 defaults `sessUserId` to `0`. Line 28/31 then calls `CompanyDAO.addUserSubscription("0", ...)`. The value `0` is likely not a valid user ID, so a subscription is silently created for a phantom user rather than failing fast or rejecting the request. No test covers the missing-sessUserId path.

---

**A01-4 | Severity: HIGH | alert_id is never validated before DAO call — no test**

`alertAction.getAlert_id()` defaults to `null` in `AdminAlertActionForm` (line 15 of the form). Lines 28 and 31 pass this value directly to `CompanyDAO.addUserSubscription(String, String)` without any null or format check. A null or malformed alert_id will either cause a DAO-level exception or silently insert corrupt data. No test covers null or invalid alert_id.

---

**A01-5 | Severity: HIGH | No test for the "alert" branch (src == "alert")**

The `src.equalsIgnoreCase("alert")` branch (lines 27–29) — including the call to `addUserSubscription` and population of `alertList` from `getAlertList()` — has zero test coverage.

---

**A01-6 | Severity: HIGH | No test for the "report" branch (src == "report")**

The `src.equalsIgnoreCase("report")` branch (lines 30–32) — including the call to `addUserSubscription` and population of `alertList` from `getReportList()` — has zero test coverage.

---

**A01-7 | Severity: HIGH | No test for the else/unknown-src error branch**

Lines 33–37 handle any `src` value that is neither "alert" nor "report". The error-message path (`ActionErrors`, `saveErrors`) and the subsequent forward to `adminalerts` (not `globalfailure`) are untested. Notably the action still returns `adminalerts` even on error, which may be a defect in itself (see A01-12), but neither the happy-path nor the error-path forwarding is tested.

---

**A01-8 | Severity: MEDIUM | sessCompId is read but never used — no test to detect dead code regression**

Line 22 reads and stores `sessCompId` from the session. It is never referenced again in the method. No test would catch if this variable were removed or if code were added that depends on it. The dead-read itself is untested.

---

**A01-9 | Severity: MEDIUM | Case-insensitive matching accepts unexpected casing variants — no boundary test**

`src.equalsIgnoreCase(...)` accepts values such as `"ALERT"`, `"Alert"`, `"REPORT"`, `"Report"`, etc. No test verifies that all expected casing variants route correctly, nor that a near-miss value (e.g., `"alerts"`, `"reporting"`) falls into the else-error branch as intended.

---

**A01-10 | Severity: MEDIUM | DAO exceptions propagate unhandled to the container — no test**

`CompanyDAO.addUserSubscription`, `getAlertList`, and `getReportList` all declare `throws Exception`. The `execute` method signature re-throws with `throws Exception`. No test verifies how Struts or the container renders a DAO failure, and no test confirms that a partial failure (e.g., `addUserSubscription` succeeds but `getAlertList` throws) leaves the system in a consistent state.

---

**A01-11 | Severity: MEDIUM | No test for empty-string src (parameter present but blank)**

When `request.getParameter("src")` returns an empty string `""`, line 23 stores `""` and line 27 falls through to the else-error branch. This is a distinct scenario from the parameter being absent (which also stores `""`). No test verifies either case.

---

**A01-12 | Severity: LOW | Error branch forwards to "adminalerts" instead of a failure forward — no test to detect wrong forward**

When `src` is unrecognized (line 33), the action adds an error but still forwards to `"adminalerts"` (line 39). `AdminAlertAction`'s error branch (see A01-17) uses a separate `"globalfailure"` forward. The inconsistency may be intentional but is undocumented and completely untested, so a regression or misconfiguration cannot be detected.

---

### AdminAlertAction

**A01-13 | Severity: HIGH | No test for the "alerts" branch (action == "alerts")**

The `action.equalsIgnoreCase("alerts")` branch (lines 24–26) — including `CompanyDAO.getAlertList()` call, `alertList` attribute assignment, and `adminalerts` forward — has zero test coverage.

---

**A01-14 | Severity: HIGH | No test for the "reports" branch (action == "reports")**

The `action.equalsIgnoreCase("reports")` branch (lines 27–29) — including `CompanyDAO.getReportList()` call, `alertList` attribute assignment, and `adminalerts` forward — has zero test coverage.

---

**A01-15 | Severity: HIGH | No test for the else/unknown-action error branch**

Lines 30–35 handle any `action` value that is neither "alerts" nor "reports". The error path (`ActionErrors`, `saveErrors`, `globalfailure` forward) is entirely untested.

---

**A01-16 | Severity: HIGH | DAO exceptions propagate unhandled to the container — no test**

`CompanyDAO.getAlertList()` and `getReportList()` declare `throws Exception`. The `execute` method re-throws. No test covers DAO failure scenarios or confirms the resulting container error behavior.

---

**A01-17 | Severity: MEDIUM | Case-insensitive matching on "action" parameter — no boundary test**

`action.equalsIgnoreCase("alerts")` and `action.equalsIgnoreCase("reports")` accept mixed-case variants. No test verifies routing for expected variants, nor that near-misses (e.g., `"alert"`, `"report"`, `"Alerts "`) correctly fall into the error branch.

---

**A01-18 | Severity: MEDIUM | No test for null or empty action parameter**

When `request.getParameter("action")` is `null`, line 22 stores `""`. When it is explicitly `""`, the same result occurs. Both cases fall through to the error branch. No test covers either scenario.

---

**A01-19 | Severity: MEDIUM | No test for empty-string action producing error forward vs. adminalerts forward**

`AdminAlertAction` routes unrecognized `action` to `"globalfailure"`, while `AdminAddAlertAction` routes unrecognized `src` to `"adminalerts"`. The behavioral asymmetry for the error case means a misconfigured `struts-config.xml` forward for either class would go undetected. No test validates either forward name.

---

**A01-20 | Severity: LOW | actionForm parameter is never used in AdminAlertAction — no test to detect dead parameter regression**

`AdminAlertAction.execute` accepts `actionForm` but never casts or uses it. No test would detect if this were accidentally removed from the signature or if code were silently added to use it. The unused parameter is a dead code smell with no regression guard.

---

## Summary Table

| Finding | Severity | Class |
|---------|----------|-------|
| A01-1  | CRITICAL | AdminAddAlertAction |
| A01-2  | CRITICAL | AdminAddAlertAction |
| A01-3  | HIGH     | AdminAddAlertAction |
| A01-4  | HIGH     | AdminAddAlertAction |
| A01-5  | HIGH     | AdminAddAlertAction |
| A01-6  | HIGH     | AdminAddAlertAction |
| A01-7  | HIGH     | AdminAddAlertAction |
| A01-8  | MEDIUM   | AdminAddAlertAction |
| A01-9  | MEDIUM   | AdminAddAlertAction |
| A01-10 | MEDIUM   | AdminAddAlertAction |
| A01-11 | MEDIUM   | AdminAddAlertAction |
| A01-12 | LOW      | AdminAddAlertAction |
| A01-13 | HIGH     | AdminAlertAction |
| A01-14 | HIGH     | AdminAlertAction |
| A01-15 | HIGH     | AdminAlertAction |
| A01-16 | HIGH     | AdminAlertAction |
| A01-17 | MEDIUM   | AdminAlertAction |
| A01-18 | MEDIUM   | AdminAlertAction |
| A01-19 | MEDIUM   | AdminAlertAction |
| A01-20 | LOW      | AdminAlertAction |

**Total findings: 20**
CRITICAL: 2 | HIGH: 9 | MEDIUM: 7 | LOW: 2
