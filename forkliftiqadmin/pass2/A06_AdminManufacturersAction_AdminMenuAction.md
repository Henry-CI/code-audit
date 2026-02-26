# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A06
**Date:** 2026-02-26
**Files audited:**
- `src/main/java/com/action/AdminManufacturersAction.java`
- `src/main/java/com/action/AdminMenuAction.java`

---

## 1. Reading-Evidence Blocks

### 1.1 AdminManufacturersAction

**File:** `src/main/java/com/action/AdminManufacturersAction.java`
**Package:** `com.action`
**Class:** `AdminManufacturersAction`
**Extends:** `PandoraAction` (which extends `org.apache.struts.action.Action`)
**Annotation:** `@Slf4j` (Lombok — injects `private static final Logger log`)

**Fields / Constants defined:** None declared explicitly in the class body. The `@Slf4j` annotation injects a `log` field at compile time.

**Methods:**

| # | Method | Lines | Visibility | Notes |
|---|--------|-------|------------|-------|
| 1 | `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | 18-52 | `public` | Entry point; dispatches on `action` form field |
| 2 | `returnManufacturersJson(HttpServletResponse, String)` | 54-59 | `private` | Builds and writes JSON list of all manufacturers |
| 3 | `returnBooleanJson(HttpServletResponse, Boolean)` | 61-66 | `private` | Builds and writes JSON boolean value |

**Dispatch branches inside `execute`:**

| Branch | Condition | Lines | Effect |
|--------|-----------|-------|--------|
| add | `action.equals("add")` | 26-32 | Saves new manufacturer; calls `returnManufacturersJson`; returns `null` |
| edit | `action.equals("edit")` | 33-39 | Updates manufacturer; calls `returnManufacturersJson`; returns `null` |
| delete | `action.equals("delete")` | 40-43 | Deletes manufacturer; calls `returnManufacturersJson`; returns `null` |
| isVehicleAssigned | `action.equals("isVehicleAssigned")` | 44-47 | Checks vehicle assignment; calls `returnBooleanJson`; returns `null` |
| default (list) | else | 48-51 | Loads all manufacturers into request attribute; forwards to `"manufacturerlist"` |

---

### 1.2 AdminMenuAction

**File:** `src/main/java/com/action/AdminMenuAction.java`
**Package:** `com.action`
**Class:** `AdminMenuAction`
**Extends:** `org.apache.struts.action.Action` (directly, NOT PandoraAction)
**Annotation:** None

**Fields / Constants defined:** None.

**Methods:**

| # | Method | Lines | Visibility | Notes |
|---|--------|-------|------------|-------|
| 1 | `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | 17-129 | `public` | Single large dispatcher; 23 named branches + 1 default error branch |

**Dispatch branches inside `execute` (action parameter, case-insensitive):**

| Branch | action value | Lines | DAO/Service calls | Forward |
|--------|-------------|-------|-------------------|---------|
| 1 | `configOperator` | 32-34 | `DriverDAO.getAllDriver` | `adminoperator` |
| 2 | `configUser` | 35-37 | `DriverDAO.getAllUser` | `adminuser` |
| 3 | `configOperatoradd` | 39-44 | none | `adminoperatoradd` |
| 4 | `configEquipment` | 45-47 | `UnitDAO.getAllUnitsByCompanyId` | `adminequipment` |
| 5 | `configEquipmentadd` | 48-53 | none | `adminequipmentadd` |
| 6 | `gpsReport` | 54-56 | `UnitDAO.getAllUnitsByCompanyId` | `admingpsreport` |
| 7 | `configChecklist` | 57-59 | `ManufactureDAO.getAllManufactures` | `adminchecklist` |
| 8 | `configDealer` | 60-62 | `AdminDealerAction.prepareDealerRequest` | `admindealer` |
| 9 | `reports` | 63-64 | none | `adminreports` |
| 10 | `home` | 65-71 | `DriverDAO.getTotalDriverByID`, `UnitDAO.getTotalUnitByID`, `ReportService.countPreOpsCompletedToday`, `ReportService.countImpactsToday`, `DriverDAO.getInstance().getExpiringTrainings` | `adminhome` |
| 11 | `logout` | 72-73 | none | `adminlogout` |
| 12 | `dashboard` | 74-75 | none | `admindashboard` |
| 13 | `import` | 76-77 | none | `adminimport` |
| 14 | `access` | 78-84 | `MenuDAO.getAllMenu` | `adminaccess` |
| 15 | `advertisement` | 85-87 | `AdvertismentDAO.getInstance().getAllAdvertisement` | `adminads` |
| 16 | `comment` | 88-89 | none | `admincomment` |
| 17 | `attachment` | 90-92 | `UnitDAO.getInstance().getAllUnitAttachment` | `adminattch` |
| 18 | `manufacturer` | 93-95 | `ManufactureDAO.getAllManufactures` | `adminmanu` |
| 19 | `entity` | 96-98 | `CompanyDAO.getInstance().getAllEntity` | `adminentity` |
| 20 | `question` | 99-101 | `CompanyDAO.getInstance().getEntityComp` | `adminquestion` |
| 21 | `quit` | 102-103 | none | `adminquit` |
| 22 | `profile` | 104-107 | `CompanyDAO.getInstance().checkExistingUserAlertByType`, `CompanyDAO.getInstance().getCompanyContactsByCompId` | `adminprofile` |
| 23 | `subscription` | 108-111 | `CompanyDAO.getInstance().getUserAlert`, `CompanyDAO.getInstance().getUserReport` | `adminsubscription` |
| 24 | `settings` | 112-119 | `TimezoneDAO.getAll`, `DateFormatDAO.getAll`, `CompanyDAO.getInstance().getCompanyContactsByCompId`, `CompanyDAO.getInstance().getUserAlert` (×3) | `adminsettings` |
| 25 | `manufacturers` | 120-122 | `ManufactureDAO.getAllManufactures` | `adminmanufacturers` |
| 26 | default (error) | 123-127 | none | `globalfailure` |

---

## 2. Test-Coverage Grep Confirmation

Grep command run against `src/test/java/` for all relevant identifiers:

```
Pattern: AdminManufacturersAction|AdminMenuAction|AdminManufacturers|AdminMenu
Result:  No matches found
```

The four existing test files are:
- `com/calibration/UnitCalibrationImpactFilterTest.java` — tests `UnitCalibrationImpactFilter`
- `com/calibration/UnitCalibrationTest.java` — tests `UnitCalibration`
- `com/calibration/UnitCalibratorTest.java` — tests `UnitCalibrator`
- `com/util/ImpactUtilTest.java` — tests `ImpactUtil`

**Conclusion:** Zero test coverage exists for either audited class, directly or indirectly.

---

## 3. Coverage Gaps and Findings

---

### AdminManufacturersAction Findings

---

**A06-1 | Severity: CRITICAL | AdminManufacturersAction — Zero test coverage for entire class**

`AdminManufacturersAction` has no tests of any kind. All five execution paths (`add`, `edit`, `delete`, `isVehicleAssigned`, default list) and both private helper methods (`returnManufacturersJson`, `returnBooleanJson`) are completely untested. This class handles all CRUD mutations on the manufacturer entity and is a critical administrative data path.

---

**A06-2 | Severity: CRITICAL | AdminManufacturersAction — Null session causes NullPointerException**

Lines 23-24:
```java
HttpSession session = request.getSession(false);
String sessCompId = session.getAttribute("sessCompId") == null ? "" : (String) session.getAttribute("sessCompId");
```

`request.getSession(false)` returns `null` when no session exists. The immediately following `session.getAttribute(...)` call will throw a `NullPointerException`. There is no null check on `session` before use, no try/catch, and no test exercising this path. An unauthenticated or session-expired request will produce an unhandled server error rather than a controlled redirect or error response.

---

**A06-3 | Severity: CRITICAL | AdminManufacturersAction — Null `action` field causes NullPointerException**

Line 26:
```java
if (adminManufacturersActionForm.getAction().equals("add")) {
```

`AdminManufacturersActionForm.action` is initialized to `null` (line 16 of the form class). If the form is submitted without populating `action`, `getAction()` returns `null`, and `.equals("add")` throws a `NullPointerException`. No null guard or `Objects.equals` / `"add".equals(...)` (Yoda-style) is used. No test exercises this path.

---

**A06-4 | Severity: HIGH | AdminManufacturersAction — `add` branch: empty/null manufacturer name accepted without validation**

Lines 27-31:
```java
ManufactureBean manufacture = new ManufactureBean();
manufacture.setName(adminManufacturersActionForm.getManufacturer());
manufacture.setCompany_id(sessCompId);
ManufactureDAO.saveManufacturer(manufacture);
```

`adminManufacturersActionForm.getManufacturer()` can be `null` (form default is `null`). A null or blank manufacturer name is passed directly to the DAO and inserted into the database with no validation. No test covers the null-name or empty-name path.

---

**A06-5 | Severity: HIGH | AdminManufacturersAction — `add` branch: empty `sessCompId` causes NumberFormatException in DAO**

When `session.getAttribute("sessCompId")` is `null`, `sessCompId` is set to `""` (empty string, line 24). The `add` branch then calls `ManufactureDAO.saveManufacturer`, which internally calls `Integer.parseInt(manufactureBean.getCompany_id())` (ManufactureDAO line 188). An empty string causes `NumberFormatException`, which is propagated as `SQLException` and not handled in the action. No test covers this edge case.

---

**A06-6 | Severity: HIGH | AdminManufacturersAction — `edit` branch: no validation that `manufacturerId` is non-null/non-empty**

Lines 34-38:
```java
ManufactureBean manufacture = new ManufactureBean();
manufacture.setId(adminManufacturersActionForm.getManufacturerId());
manufacture.setName(adminManufacturersActionForm.getManufacturer());
ManufactureDAO.updateManufacturer(manufacture);
```

`getManufacturerId()` defaults to `null`. Passing a null ID to `ManufactureDAO.updateManufacturer` results in `Integer.parseInt(null)` at ManufactureDAO line 224, throwing `NumberFormatException`. No test covers this path.

---

**A06-7 | Severity: HIGH | AdminManufacturersAction — `delete` branch: no validation that `manufacturerId` is non-null/non-empty**

Line 41:
```java
ManufactureDAO.delManufacturById(adminManufacturersActionForm.getManufacturerId());
```

Same issue as A06-6. A null `manufacturerId` causes `NumberFormatException` inside `delManufacturById` at ManufactureDAO line 109 (`Integer.parseInt(id)`). No test covers this path.

---

**A06-8 | Severity: HIGH | AdminManufacturersAction — `isVehicleAssigned` branch: no validation that `manufacturerId` is non-null/non-empty**

Lines 45-46:
```java
String manufacturerId = adminManufacturersActionForm.getManufacturerId();
returnBooleanJson(response, ManufactureDAO.isVehicleAssignedToManufacturer(manufacturerId));
```

`manufacturerId` can be `null`. `ManufactureDAO.isVehicleAssignedToManufacturer` calls `Integer.parseInt(manufacturerId)` (ManufactureDAO line 415), throwing `NumberFormatException`. No test covers this path.

---

**A06-9 | Severity: HIGH | AdminManufacturersAction — DAO exceptions not handled; response state is undefined**

All four mutation branches (`add`, `edit`, `delete`, `isVehicleAssigned`) call DAO methods that throw checked `Exception`. These propagate out of `execute` because the method signature declares `throws Exception`. After the response writer has already been obtained and partially written (inside `returnManufacturersJson` or `returnBooleanJson`), a DAO exception will leave the HTTP response in a partially-written, uncommitted state with no error body sent to the client. No test exercises any DAO failure scenario.

---

**A06-10 | Severity: MEDIUM | AdminManufacturersAction — `returnManufacturersJson`: response content-type never set**

Lines 54-59:
```java
private void returnManufacturersJson(HttpServletResponse response, String companyId) throws Exception {
    JSONObject returnObject = new JSONObject();
    returnObject.put("manufacturers", ManufactureDAO.getAllManufactures(companyId));
    PrintWriter out = response.getWriter();
    out.write(returnObject.toString());
}
```

`response.setContentType("application/json")` is never called before `response.getWriter()`. The content-type header defaults to whatever the container chooses (often `text/html`). Browsers and API clients may misparse the response. The same omission exists in `returnBooleanJson` (lines 61-66). No test verifies the response content-type.

---

**A06-11 | Severity: MEDIUM | AdminManufacturersAction — `returnManufacturersJson` and `returnBooleanJson`: PrintWriter never flushed or closed**

After writing to the `PrintWriter`, `out.flush()` / `out.close()` is never called. Under buffered containers, output may not be committed to the client. No test verifies that output is actually flushed.

---

**A06-12 | Severity: MEDIUM | AdminManufacturersAction — `edit` branch: `sessCompId` not set on bean (company ownership not preserved)**

Lines 34-38: When editing, `manufacture.setCompany_id(...)` is never called. Only `id` and `name` are set. The DAO update SQL (`update manufacture set name = ? where id = ?`) does not update `company_id`, so this is not immediately a data-corruption bug at the SQL level. However, the inconsistency means the bean is incomplete relative to the add-path bean, and any future change to the update SQL that also writes `company_id` would silently clear the field. No test asserts post-edit company_id consistency.

---

**A06-13 | Severity: LOW | AdminManufacturersAction — `delete` branch: return value of `delManufacturById` ignored**

Line 41:
```java
ManufactureDAO.delManufacturById(adminManufacturersActionForm.getManufacturerId());
```

`delManufacturById` returns `Boolean` indicating whether exactly one row was deleted. The return value is discarded. A silent no-op delete (e.g., non-existent ID) is indistinguishable from a successful delete. No test verifies the outcome of the delete operation.

---

**A06-14 | Severity: LOW | AdminManufacturersAction — `add` branch: return value of `saveManufacturer` ignored**

Line 30:
```java
ManufactureDAO.saveManufacturer(manufacture);
```

`saveManufacturer` returns `boolean` indicating whether the insert affected exactly one row. The return value is silently discarded. No test asserts that a save failure is detected.

---

**A06-15 | Severity: LOW | AdminManufacturersAction — `edit` branch: return value of `updateManufacturer` ignored**

Line 37:
```java
ManufactureDAO.updateManufacturer(manufacture);
```

Same pattern as A06-14. No test covers the update-failure scenario.

---

**A06-16 | Severity: LOW | AdminManufacturersAction — Action string comparison is case-sensitive; inconsistent with AdminMenuAction**

Lines 26, 33, 40, 44 use `.equals("add")` (case-sensitive). `AdminMenuAction` uses `.equalsIgnoreCase(...)` throughout. A client submitting `"Add"` or `"ADD"` to `AdminManufacturersAction` will silently fall through to the default list path. No test exercises mixed-case action values.

---

### AdminMenuAction Findings

---

**A06-17 | Severity: CRITICAL | AdminMenuAction — Zero test coverage for entire class**

`AdminMenuAction` has no tests of any kind. All 26 dispatch branches are completely untested, including the error/default branch.

---

**A06-18 | Severity: CRITICAL | AdminMenuAction — Null session causes NullPointerException on every request**

Lines 21-27:
```java
HttpSession session = request.getSession(false);
String action = request.getParameter("action") == null ? "" : request.getParameter("action");
String sessCompId = session.getAttribute("sessCompId") == null ? "" : ...
```

`request.getSession(false)` can return `null`. `session` is used on lines 23-27 without a null check. An expired or absent session causes an immediate `NullPointerException`. No test covers the no-session path.

---

**A06-19 | Severity: CRITICAL | AdminMenuAction — `Integer.parseInt(sessCompId)` on line 26 throws NumberFormatException when sessCompId is empty**

Line 26:
```java
int companyId = Integer.parseInt(sessCompId);
```

When `session.getAttribute("sessCompId")` is `null`, `sessCompId` is set to `""`. `Integer.parseInt("")` throws `NumberFormatException`, which propagates as an unhandled exception from `execute`. This affects every single branch that reaches line 26 — i.e., all branches unconditionally — because `companyId` is computed before any branch dispatch. No test covers a missing or non-numeric `sessCompId`.

---

**A06-20 | Severity: CRITICAL | AdminMenuAction — `access` branch: NullPointerException when session Locale is null**

Lines 80-81:
```java
Locale locale = (Locale) session.getAttribute(Globals.LOCALE_KEY);
String lanCode = locale.getLanguage();
```

If `session.getAttribute(Globals.LOCALE_KEY)` returns `null` (e.g., session attribute not set by Struts), `locale` is `null` and `locale.getLanguage()` throws a `NullPointerException`. No null guard is present and no test covers this path.

---

**A06-21 | Severity: CRITICAL | AdminMenuAction — `settings` branch: `getCompanyContactsByCompId(...).get(0)` throws IndexOutOfBoundsException on empty result**

Line 115:
```java
request.setAttribute("company", CompanyDAO.getInstance().getCompanyContactsByCompId(sessCompId,sessUserId,sessionToken).get(0));
```

If `getCompanyContactsByCompId` returns an empty list, `.get(0)` throws `IndexOutOfBoundsException`. No test covers the empty-list path.

---

**A06-22 | Severity: HIGH | AdminMenuAction — All DAO/service exceptions propagate unhandled from `execute`**

`execute` is declared `throws Exception`. All 25 data-loading branches invoke DAO or service methods that can throw exceptions (database connectivity failures, SQL errors, etc.). None of these are caught within the action. An infrastructure failure in any branch results in an unhandled exception propagating to Struts, which typically produces an HTTP 500 or a generic error page, with no meaningful user-facing message or logging within the action. No test covers any exception path.

---

**A06-23 | Severity: HIGH | AdminMenuAction — `home` branch: `Long.valueOf(sessCompId)` throws NumberFormatException when sessCompId is empty or non-numeric**

Lines 68-69:
```java
request.setAttribute("totalFleetCheck", ReportService.getInstance().countPreOpsCompletedToday(Long.valueOf(sessCompId),timezone));
request.setAttribute("totalImpactToday", ReportService.getInstance().countImpactsToday(Long.valueOf(sessCompId),timezone));
```

Although the early `Integer.parseInt(sessCompId)` on line 26 would already fail for an empty `sessCompId`, if `sessCompId` is somehow non-empty but still invalid for `Long.valueOf`, these calls would also fail. Additionally, any future refactoring that removes line 26 would expose these calls directly. No test covers the `home` branch at all.

---

**A06-24 | Severity: HIGH | AdminMenuAction — `question` branch writes to session (side-effect), not request**

Line 100:
```java
session.setAttribute("seesArrComp", CompanyDAO.getInstance().getEntityComp(sessCompId));
```

All other branches use `request.setAttribute`. This branch writes to the session, making the data persistent across requests and shared across tabs/requests for the same user. The attribute name `seesArrComp` appears to be a typo for `sessArrComp`. No test verifies this session-write behavior or its cross-request implications.

---

**A06-25 | Severity: HIGH | AdminMenuAction — Default (error) branch: `ActionErrors` added but no test confirms the `globalfailure` forward is actually reached for unknown actions**

Lines 123-127:
```java
ActionErrors errors = new ActionErrors();
errors.add(ActionErrors.GLOBAL_MESSAGE, new ActionMessage("errors.global"));
saveErrors(request, errors);
return mapping.findForward("globalfailure");
```

The `globalfailure` forward is the only error handling in the class. An unknown or empty `action` value silently reaches this branch. No test confirms that: (a) the branch is reachable for an unrecognized action, (b) errors are actually saved, or (c) the `globalfailure` forward is configured in struts-config.

---

**A06-26 | Severity: MEDIUM | AdminMenuAction — `subscription` branch is marked as "Not used" in a comment but remains active code**

Line 108:
```java
} else if (action.equalsIgnoreCase("subscription")) {  //Not used
```

Dead/legacy code paths present a maintenance risk: they execute DAO queries (`getUserAlert`, `getUserReport`) on a path believed to be unreachable, and they cannot be validated. No test confirms whether this branch is truly dead. The branch should be removed or documented with a deprecation notice.

---

**A06-27 | Severity: MEDIUM | AdminMenuAction — `sessUserId` silently defaults to `0` when session attribute is missing**

Line 24:
```java
int sessUserId = session.getAttribute("sessUserId") == null ? 0 : (Integer) session.getAttribute("sessUserId");
```

A user ID of `0` is a sentinel that may match a real record or produce unexpected query results in DAO calls that use `sessUserId` (e.g., `profile`, `subscription`, `settings` branches). The action provides no guard against an anonymous user reaching these branches with `sessUserId = 0`. No test exercises the null-sessUserId case.

---

**A06-28 | Severity: MEDIUM | AdminMenuAction — `sessionToken` silently defaults to empty string when missing**

Line 27:
```java
String sessionToken = session.getAttribute("sessionToken") == null ? "" : (String) session.getAttribute("sessionToken");
```

`sessionToken` is passed to `DriverDAO.getAllUser`, `CompanyDAO.getCompanyContactsByCompId`, and `CompanyDAO.getCompanyContactsByCompId` in `settings`. Passing an empty token may cause authentication failures or return incorrect data from external service calls. No test covers the missing-token scenario.

---

**A06-29 | Severity: MEDIUM | AdminMenuAction — `timezone` silently defaults to empty string; downstream TimeZone parsing may fail silently**

Line 25:
```java
String timezone = session.getAttribute("sessTimezone") == null ? "" : (String) session.getAttribute("sessTimezone");
```

`timezone` is used in `home` branch (lines 66-69) with `ReportService.countPreOpsCompletedToday` and `ReportService.countImpactsToday`. An empty timezone string may cause incorrect time-based filtering or silent errors in the service layer. No test covers the missing-timezone case.

---

**A06-30 | Severity: LOW | AdminMenuAction — `configOperatoradd` and `configEquipmentadd` branches create single-element lists wrapping empty beans**

Lines 40-43, 49-52: These branches create a `new DriverBean()` / `new UnitBean()` with all fields at their defaults and wrap it in a one-element `ArrayList`. The purpose appears to be pre-populating a form, but no test confirms that this produces a valid model for the view, or that the bean's default field values are appropriate for a "new record" form.

---

**A06-31 | Severity: LOW | AdminMenuAction — `dateFormat` session attribute used without null guard in `configOperator` branch**

Line 31:
```java
String dateFormat = (String) session.getAttribute("sessDateFormat");
```

`dateFormat` is retrieved without a null check, then passed directly to `DriverDAO.getAllDriver(sessCompId, true, dateFormat)` on line 33. If `sessDateFormat` is absent from the session, a `null` value is passed to the DAO. Whether this causes a NullPointerException depends on DAO internals. No test covers the null-dateFormat case.

---

**A06-32 | Severity: LOW | AdminMenuAction — `isDealer` session attribute set on request without null guard**

Line 30:
```java
request.setAttribute("isDealer", session.getAttribute("isDealer"));
```

If `isDealer` is not set in the session, `null` is propagated to the request attribute. Views consuming this attribute must null-guard it. No test confirms the null-propagation behavior or its downstream impact.

---

## 4. Summary Table

| Finding | Severity | Class | Description |
|---------|----------|-------|-------------|
| A06-1 | CRITICAL | AdminManufacturersAction | Zero test coverage for entire class |
| A06-2 | CRITICAL | AdminManufacturersAction | Null session → NullPointerException |
| A06-3 | CRITICAL | AdminManufacturersAction | Null `action` form field → NullPointerException |
| A06-4 | HIGH | AdminManufacturersAction | Null/blank manufacturer name accepted without validation |
| A06-5 | HIGH | AdminManufacturersAction | Empty `sessCompId` causes NumberFormatException in DAO (add branch) |
| A06-6 | HIGH | AdminManufacturersAction | Null `manufacturerId` causes NumberFormatException in DAO (edit branch) |
| A06-7 | HIGH | AdminManufacturersAction | Null `manufacturerId` causes NumberFormatException in DAO (delete branch) |
| A06-8 | HIGH | AdminManufacturersAction | Null `manufacturerId` causes NumberFormatException in DAO (isVehicleAssigned branch) |
| A06-9 | HIGH | AdminManufacturersAction | DAO exceptions not handled; response left in undefined state |
| A06-10 | MEDIUM | AdminManufacturersAction | Response content-type never set to `application/json` |
| A06-11 | MEDIUM | AdminManufacturersAction | PrintWriter never flushed or closed after write |
| A06-12 | MEDIUM | AdminManufacturersAction | Edit branch does not set `company_id` on updated bean |
| A06-13 | LOW | AdminManufacturersAction | Return value of `delManufacturById` silently ignored |
| A06-14 | LOW | AdminManufacturersAction | Return value of `saveManufacturer` silently ignored |
| A06-15 | LOW | AdminManufacturersAction | Return value of `updateManufacturer` silently ignored |
| A06-16 | LOW | AdminManufacturersAction | Case-sensitive action comparison; inconsistent with AdminMenuAction |
| A06-17 | CRITICAL | AdminMenuAction | Zero test coverage for entire class |
| A06-18 | CRITICAL | AdminMenuAction | Null session → NullPointerException on every request |
| A06-19 | CRITICAL | AdminMenuAction | `Integer.parseInt(sessCompId)` on empty string → NumberFormatException (affects all branches) |
| A06-20 | CRITICAL | AdminMenuAction | Null session Locale in `access` branch → NullPointerException |
| A06-21 | CRITICAL | AdminMenuAction | `getCompanyContactsByCompId(...).get(0)` on empty list → IndexOutOfBoundsException (`settings` branch) |
| A06-22 | HIGH | AdminMenuAction | All DAO/service exceptions propagate unhandled |
| A06-23 | HIGH | AdminMenuAction | `Long.valueOf(sessCompId)` fails on invalid value in `home` branch |
| A06-24 | HIGH | AdminMenuAction | `question` branch writes to session (not request); likely typo in attribute name |
| A06-25 | HIGH | AdminMenuAction | Default error branch not tested; `globalfailure` forward may be misconfigured |
| A06-26 | MEDIUM | AdminMenuAction | `subscription` branch is dead code (comment says "Not used") but still active |
| A06-27 | MEDIUM | AdminMenuAction | `sessUserId` defaults to `0` when missing; may match real records |
| A06-28 | MEDIUM | AdminMenuAction | `sessionToken` defaults to empty string; may cause auth failures downstream |
| A06-29 | MEDIUM | AdminMenuAction | `timezone` defaults to empty string; may cause incorrect time-based filtering |
| A06-30 | LOW | AdminMenuAction | `configOperatoradd`/`configEquipmentadd` create empty beans with no validation of defaults |
| A06-31 | LOW | AdminMenuAction | `dateFormat` passed to DAO without null guard |
| A06-32 | LOW | AdminMenuAction | `isDealer` null propagated to request attribute without guard |

---

## 5. Severity Counts

| Severity | Count |
|----------|-------|
| CRITICAL | 9 |
| HIGH | 9 |
| MEDIUM | 7 |
| LOW | 7 |
| **Total** | **32** |

---

## 6. Recommended Test Coverage Priorities

1. **Session null safety** (A06-2, A06-18): Mock `request.getSession(false)` returning `null`; assert no NullPointerException escapes.
2. **Null/invalid `action` field** (A06-3): Submit form with `action = null`; assert safe fallback behavior.
3. **Invalid `sessCompId`** (A06-5, A06-19): Session with `sessCompId = null` or `""` or `"abc"`; assert controlled error response.
4. **All five `execute` dispatch branches** (A06-1): One test per branch with mocked DAO; assert correct forward or response output.
5. **All 26 `AdminMenuAction` dispatch branches** (A06-17): One test per branch with mocked DAOs; assert correct forward and request attributes set.
6. **DAO exception propagation** (A06-9, A06-22): Force DAO to throw; assert response state is clean or a proper error is returned.
7. **`access` branch Locale null** (A06-20): Session without Globals.LOCALE_KEY; assert null-safe handling.
8. **`settings` branch empty company list** (A06-21): `getCompanyContactsByCompId` returns empty list; assert no IndexOutOfBoundsException.
9. **JSON response correctness** (A06-10, A06-11): Verify content-type header and flushed output for all JSON-returning branches.
10. **Dead code removal** (A06-26): Remove or disable `subscription` branch and add regression test confirming it is unreachable.
