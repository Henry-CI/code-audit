# Pass 2 Test-Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A12
**Date:** 2026-02-26
**Scope:** AdminUnitServiceAction, AppAPIAction
**Project:** forkliftiqadmin (Java / Struts 1.x / Tomcat)

---

## 1. Reading-Evidence Blocks

### 1.1 AdminUnitServiceAction

**Source file:** `src/main/java/com/action/AdminUnitServiceAction.java`
**Package:** `com.action`
**Superclass:** `org.apache.struts.action.Action`

#### Fields / Constants

| Name | Type | Scope | Line |
|------|------|-------|------|
| `log` | `Logger` | `private static` | 19 |

#### Methods

| Method Signature | Line |
|------------------|------|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 21 |

#### Internal Logic Branches Inside `execute` (lines 21-68)

| Branch | Line(s) |
|--------|---------|
| Null-safe read of `action` request parameter (ternary) | 23 |
| Cast of `actionForm` to `AdminUnitServiceForm` | 25 |
| Fallback: if `action` is null or blank, read from `serviceForm.getAction()` | 27-29 |
| `action.equalsIgnoreCase("saveservice")` — true branch | 31-64 |
| `servType` is `"setIntval"` or `"setDur"` → `serviceRemain = servDuration - accHours` | 36-37 |
| else → `serviceRemain = (double) servNext - accHours` | 39 |
| `serviceRemain < 5` → status "Service is due in less than 5 hours or service is overdue." | 44-45 |
| `serviceRemain < 25` → status "Service is due in less than 25 hours" | 46-47 |
| else → status "Service is due in more than 25 hours" | 48-50 |
| `UnitDAO.getInstance().saveService(serviceBean)` call | 61 |
| Set request attribute `"serviceBean"` | 63 |
| Return forward `"success"` (saveservice path) | 64 |
| else (action not "saveservice") — fall-through `return mapping.findForward("success")` | 65-67 |

---

### 1.2 AppAPIAction

**Source file:** `src/main/java/com/action/AppAPIAction.java`
**Package:** `com.action`
**Superclass:** `org.apache.struts.action.Action`

#### Fields / Constants

| Name | Type | Scope | Line |
|------|------|-------|------|
| `log` | `Logger` | `private static` | 40 |

#### Methods

| Method Signature | Line |
|------------------|------|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 42 |

#### Internal Logic Inside `execute` (lines 42-373)

The entire body of `execute` is commented out using `////` line-comment blocks (lines 45-371). Only two active lines remain:

| Active Line | Content | Line |
|-------------|---------|------|
| Partially uncommented `request.setAttribute("method", action)` | Commented with `//` only (still inactive) | 371 |
| `return mapping.findForward("apiXml")` | The only truly active statement | 372 |

The commented-out logic covered seven API action branches:
`API_LOGIN`, `API_DRIVER`, `API_VEHICLE`, `API_ATTACHMENT`, `API_QUESTION`, `API_RESULT`, `API_PDFRPT`, and a catch-all invalid action handler.

---

## 2. Test-Directory Coverage Confirmation

### Existing Test Files (entire project)

```
src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java
src/test/java/com/calibration/UnitCalibrationTest.java
src/test/java/com/calibration/UnitCalibratorTest.java
src/test/java/com/util/ImpactUtilTest.java
```

None of these files test any action class. All four cover calibration domain logic and impact-calculation utilities only.

### Grep Results

| Search Term | Matches in test directory |
|-------------|--------------------------|
| `AdminUnitServiceAction` | 0 |
| `AppAPIAction` | 0 |

**Conclusion:** Zero test coverage exists for either audited class — direct or indirect.

---

## 3. Struts Configuration Context

From `src/main/webapp/WEB-INF/struts-config.xml`:

**AdminUnitServiceAction** is mapped at path `/adminunitservice`, using form bean `adminUnitServiceForm` (`AdminUnitServiceForm`), with `validate="true"` and input tile `UnitServiceDefinition`. Forwards: `success` → `UnitServiceDefinition`, `failure` → `UnitServiceDefinition`.

**AppAPIAction** is mapped at path `/api`. Forward: `apiXml` → `/html-jsp/apiXml.jsp`. No form bean, no validation configured.

---

## 4. Coverage Gap Findings

---

### AdminUnitServiceAction

---

**A12-1 | Severity: CRITICAL | Zero test coverage for AdminUnitServiceAction**

The class `AdminUnitServiceAction` has no test of any kind. The single public method `execute` is the entry point for saving forklift service records to the database. No unit test, integration test, or mock-based test exists. A regression in any branch will be detected only at runtime in production.

---

**A12-2 | Severity: HIGH | `action` parameter null-check is logically dead after the ternary**

At line 23, `action` is assigned via a ternary that substitutes `""` if the request parameter is null, making `action` non-null by construction. The subsequent guard `if (action == null || action.equals(""))` at line 27 therefore can never evaluate the `null` branch. The `null` comparison at line 27 is dead code. No test exercises the path where `action` comes from `serviceForm.getAction()` when the request parameter is absent but the form field is non-empty (e.g., `action = "saveservice"` arrives via form binding, not query string).

Specific untested paths:
- Request parameter `action` is `null` AND `serviceForm.getAction()` returns a non-blank value.
- Request parameter `action` is absent AND `serviceForm.getAction()` is also blank/null (potential NPE if form field itself is null, since `equalsIgnoreCase` is called without null guard on the result of `serviceForm.getAction()`).

---

**A12-3 | Severity: HIGH | `servType` null-dereference path untested**

At line 36, `serviceForm.getServType().equalsIgnoreCase("setIntval")` is called without a null check on `getServType()`. `AdminUnitServiceForm` initialises `servType` as `null` by default (no field initialiser). If a `saveservice` request arrives with `servType` not bound, a `NullPointerException` will be thrown and propagated as an unhandled exception. There is no test for a `saveservice` action with a missing or null `servType`.

---

**A12-4 | Severity: HIGH | All three `serviceRemain` threshold boundary conditions untested**

The service-status classification logic (lines 44-50) has three branches with defined thresholds:

| Condition | Threshold | Status String |
|-----------|-----------|---------------|
| `serviceRemain < 5` | exact at 5.0 | "due in less than 5 hours or service is overdue" |
| `serviceRemain < 25` | exact at 25.0 | "due in less than 25 hours" |
| else | >= 25 | "due in more than 25 hours" |

Not a single test covers:
- Normal case for any of the three branches.
- Exact boundary values (5.0, 4.999, 25.0, 24.999).
- Negative `serviceRemain` (overdue scenario) which correctly falls into the `< 5` branch but is semantically distinct and should be validated.
- The result string set on `serviceBean.setServStatus()` is never asserted anywhere.

---

**A12-5 | Severity: HIGH | `serviceRemain` computation branches for `servType` untested**

Two distinct formulae exist for computing `serviceRemain` (lines 36-40):

- **Branch A** (`servType` is `"setIntval"` or `"setDur"`): `serviceRemain = servDuration - accHours`
- **Branch B** (all other types): `serviceRemain = (double) servNext - accHours`

Neither branch has any test. The cast `(double) servNext` in Branch B involves an `int`-to-`double` widening cast on `servNext` (an `int` field). No test confirms correct numeric output, overflow behaviour, or that Branch A is not accidentally taken for a type that should use Branch B.

---

**A12-6 | Severity: HIGH | `UnitDAO.saveService` exception path untested**

At line 61, `UnitDAO.getInstance().saveService(serviceBean)` is called. `saveService` is declared `throws Exception` and internally rethrows as `SQLException`. If the DAO throws, `execute` propagates the exception to the Struts framework. No test:
- Exercises DAO failure (e.g., connection unavailable, constraint violation).
- Verifies the exception is propagated rather than swallowed.
- Confirms that no partial state is left in the request (e.g., `serviceBean` partially set on request scope before the exception).

---

**A12-7 | Severity: MEDIUM | Non-`saveservice` `action` fall-through path untested**

Lines 65-67: when `action` is anything other than `"saveservice"` (blank, unknown value, any other action token), the method immediately returns `mapping.findForward("success")` without any processing, logging, or error indication. No test covers this path. There is no defensive logging or error forward — an unknown action silently succeeds, which is a behavioural gap that tests would catch.

---

**A12-8 | Severity: MEDIUM | `ServiceBean` fields set on request scope never asserted in any test**

Line 63 places the populated `serviceBean` onto the request as attribute `"serviceBean"`. This attribute is consumed by the JSP view (`UnitServiceDefinition`). No test verifies that the correct bean state is present on the request after a successful save, meaning presentation-layer regressions will not be caught.

---

**A12-9 | Severity: MEDIUM | `mapping.findForward("success")` return value never verified**

Both return points in `execute` call `mapping.findForward("success")`. No test mocks `ActionMapping` to assert that the correct forward name is resolved or that the returned `ActionForward` is non-null. In Struts 1 a misconfigured forward name returns `null` at runtime, causing a `NullPointerException` in the framework dispatcher.

---

**A12-10 | Severity: LOW | Cast of `actionForm` to `AdminUnitServiceForm` untested for type mismatch**

Line 25 performs an unchecked cast: `AdminUnitServiceForm serviceForm = (AdminUnitServiceForm) actionForm`. If the Struts framework supplies a form bean of the wrong type (mis-mapped configuration), a `ClassCastException` is thrown. No test covers this path. In a properly-mapped action this would not occur, but the absence of a test means no compile-time or runtime guard is verified.

---

**A12-11 | Severity: LOW | Logger field `log` not exercised by any test**

The `private static Logger log` at line 19 is initialised by `InfoLogger.getLogger(...)`. No test verifies this initialisation succeeds or that log output occurs correctly. While low-severity on its own, a misconfigured logger can silently suppress operational diagnostics.

---

### AppAPIAction

---

**A12-12 | Severity: CRITICAL | AppAPIAction.execute is an entirely dead method (all logic commented out)**

The `execute` method body (lines 45-371) is 100% commented out using `////` four-slash block-comments. The only active statement is `return mapping.findForward("apiXml")` at line 372. This means:
- The action is live in struts-config.xml (path `/api`), reachable by any HTTP request.
- It processes no input, performs no authentication, no validation, and no business logic.
- It unconditionally forwards to `apiXml.jsp` regardless of any request parameter.
- Any mobile app or external client calling `/api` will receive an empty XML response with no error indication.
- All seven API branches (login, driver list, vehicle list, attachment list, question list, save result, PDF report) are silently non-functional.

No test exists to document or catch this complete functional absence.

---

**A12-13 | Severity: CRITICAL | No authentication check is active — API endpoint is fully open**

In the commented-out logic, authentication was enforced via `compKey` lookup (error code `001`: "Unauthorised User"). With all logic commented out, the `/api` endpoint accepts any request from any caller without any authentication check whatsoever. No test documents the intended authentication contract or detects the regression.

---

**A12-14 | Severity: HIGH | Commented-out `request.setAttribute("method", action)` is also dead**

Line 371 (`// request.setAttribute("method", action)`) is commented out with a single `//`. The `action` local variable is never declared in the active code scope. If this line were accidentally uncommented, it would cause a compile error. No test catches this latent defect.

---

**A12-15 | Severity: HIGH | Seven API operation branches are dead code with no test documentation**

The following API operations, each formerly implemented and now commented out, have no tests to document their expected behaviour or serve as executable specifications for future re-implementation:

| Error Code | Operation | RuntimeConf Constant |
|------------|-----------|----------------------|
| `checklogin` | Authenticate user, return `compKey` | `API_LOGIN` |
| `getDriverlst` | Return driver list for company | `API_DRIVER` |
| `getVehlst` | Return vehicle/unit list for company | `API_VEHICLE` |
| `getAttlst` | Return attachment list for company | `API_ATTACHMENT` |
| `getQueslst` | Return questions for unit and attachment | `API_QUESTION` |
| `saveResult` | Submit inspection result, send email alert | `API_RESULT` |
| `pdfrpt` | Generate PDF report and email it | `API_PDFRPT` |
| (catch-all) | Invalid action → error `002` | `API_INVALID` |

Without tests, there is no executable record of the validation rules, error codes, or Linde-vs-standard database branching that was implemented.

---

**A12-16 | Severity: HIGH | Error code contract (001–012) has no test coverage**

The commented-out code defined a structured error-code protocol:

| Code | Meaning |
|------|---------|
| 001 | Unauthorised user (invalid compKey) |
| 002 | Missing or invalid action parameter |
| 003 | Missing vehId |
| 004 | Missing drvId |
| 005 | Missing or mismatched qids/qans/qcoms arrays |
| 006 | vehId is empty string |
| 007 | drvId is empty string |
| 008 | attId is empty string |
| 009 | vehId is non-numeric |
| 010 | drvId is non-numeric |
| 011 | attId is non-numeric |
| 012 | Invalid date format for ftime/from/to |

None of these error paths are tested, documented, or currently active. Any consumer of this API has no reliable contract.

---

**A12-17 | Severity: HIGH | Linde vs. standard database branching logic is untested and inactive**

Throughout the commented-out code, a `db` request parameter was used to switch between Linde-specific DAO methods (e.g., `getCompIdByKeyLinde`, `getAllDriverLinde`, `saveResultAPPLinde`) and standard methods. This branching is now entirely dead. No test documents the expected behaviour, the `RuntimeConf.LINDEDB` constant value (`"fleeiq"`), or the DAO-method routing rules.

---

**A12-18 | Severity: MEDIUM | `mapping.findForward("apiXml")` return value untested**

The single active line returns `mapping.findForward("apiXml")`. No test mocks `ActionMapping` to assert the correct forward name is used or that the returned `ActionForward` is non-null. A forward-name typo or struts-config misconfiguration would cause a runtime `NullPointerException` with no test catching it.

---

**A12-19 | Severity: MEDIUM | `AppAPIAction` has no test for the execute method signature itself**

No test verifies that `AppAPIAction` instantiates correctly, that the static `log` field initialises without error, or that `execute` is callable with mock parameters. Even a trivial smoke test would provide a regression safety net for refactoring.

---

**A12-20 | Severity: LOW | Unused imports remain active despite all logic being commented out**

The following imports are present and compiled (lines 4-36) but serve no active code:

```java
import java.sql.Connection;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.Date;
import org.apache.struts.Globals;
import org.apache.struts.util.PropertyMessageResources;
import com.bean.AttachmentBean;
import com.bean.CompanyBean;
import com.bean.DriverBean;
import com.bean.QuestionBean;
import com.bean.UnitBean;
import com.dao.CompanyDAO;
import com.dao.DriverDAO;
import com.dao.LoginDAO;
import com.dao.QuestionDAO;
import com.dao.UnitDAO;
import com.pdf.FleetCheckPDF;
import com.util.DBUtil;
import com.util.DateUtil;
import com.util.RuntimeConf;
import com.util.Util;
```

No test detects or warns that these imports are orphaned. They represent a maintenance hazard and obscure the true active API surface.

---

## 5. Summary Table

| Finding | Severity | Class | Description |
|---------|----------|-------|-------------|
| A12-1 | CRITICAL | AdminUnitServiceAction | Zero test coverage for entire class |
| A12-2 | HIGH | AdminUnitServiceAction | Dead null-check; `action` from form fallback path untested |
| A12-3 | HIGH | AdminUnitServiceAction | `getServType()` null-dereference on `saveservice` with unbound servType |
| A12-4 | HIGH | AdminUnitServiceAction | All three serviceRemain threshold branches and boundaries untested |
| A12-5 | HIGH | AdminUnitServiceAction | Both serviceRemain computation formulae (setIntval/setDur vs. other) untested |
| A12-6 | HIGH | AdminUnitServiceAction | DAO exception propagation path untested |
| A12-7 | MEDIUM | AdminUnitServiceAction | Non-`saveservice` action fall-through untested |
| A12-8 | MEDIUM | AdminUnitServiceAction | Request-scope `serviceBean` attribute content never asserted |
| A12-9 | MEDIUM | AdminUnitServiceAction | `findForward("success")` return value never verified |
| A12-10 | LOW | AdminUnitServiceAction | `actionForm` cast to `AdminUnitServiceForm` not tested for type mismatch |
| A12-11 | LOW | AdminUnitServiceAction | Logger initialisation untested |
| A12-12 | CRITICAL | AppAPIAction | Entire execute body commented out; method is functionally dead |
| A12-13 | CRITICAL | AppAPIAction | API endpoint is fully open — authentication check is commented out |
| A12-14 | HIGH | AppAPIAction | Commented-out `request.setAttribute("method", action)` would not compile if restored |
| A12-15 | HIGH | AppAPIAction | All seven API operation branches dead with no test documentation |
| A12-16 | HIGH | AppAPIAction | Error code contract (001-012) entirely untested and inactive |
| A12-17 | HIGH | AppAPIAction | Linde vs. standard database branching untested and inactive |
| A12-18 | MEDIUM | AppAPIAction | `findForward("apiXml")` return value never verified |
| A12-19 | MEDIUM | AppAPIAction | No smoke test for AppAPIAction instantiation or execute invocability |
| A12-20 | LOW | AppAPIAction | 20 orphaned imports with no test detecting the dead-code surface |

**Total findings: 20**
**CRITICAL: 3 | HIGH: 9 | MEDIUM: 5 | LOW: 3**

---

## 6. Notes on Test Infrastructure

The project uses JUnit 4 and Mockito (evidenced by `UnitCalibratorTest`). The existing test patterns demonstrate:
- Mockito mocking via `mock()` and `when(...).thenReturn(...)`.
- `@Before` setup methods for collaborator initialisation.
- Standard `assertEquals` / `assertTrue` / `assertFalse` assertions.

This infrastructure is sufficient to write unit tests for both action classes using mock `HttpServletRequest`, `ActionMapping`, `ActionForm`, and DAO objects. No additional test libraries are required. The primary obstacle for `AdminUnitServiceAction` is that `UnitDAO` uses a static singleton (`UnitDAO.getInstance()`), which would require either PowerMock or refactoring to an injectable dependency to enable DAO-layer mocking.

---

*Report generated by Agent A12 for audit run 2026-02-26-01.*
