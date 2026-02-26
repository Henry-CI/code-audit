# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A23
**Files audited:**
- `src/main/java/com/action/MailerAction.java`
- `src/main/java/com/action/PandoraAction.java`

---

## 1. Reading Evidence

### 1.1 MailerAction

**File:** `src/main/java/com/action/MailerAction.java`
**Package:** `com.action`
**Class declaration (line 37):** `public class MailerAction extends Action`
**Direct superclass:** `org.apache.struts.action.Action` (NOT `PandoraAction`)

**Fields / constants:**

| Name | Type | Line | Notes |
|------|------|------|-------|
| `log` | `static Logger` | 38 | Log4j logger, private static |

**Methods:**

| Method | Signature | Line | Notes |
|--------|-----------|------|-------|
| `execute` | `public ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 40–141 | Only method; entire request-handling and email-dispatch logic lives here |

**Key internal logic blocks within `execute` (line references):**

| Logic block | Lines |
|-------------|-------|
| Read `debug` param (null-safe) | 43–44 |
| Read `date` param (null-safe) | 45–46 |
| Read `frequency` param (null-safe) | 47–48 |
| Branch: explicit date supplied (`!sDate.equalsIgnoreCase("")`) | 53–57 |
| Branch: no date supplied — use current date, reformat via DateUtil | 58–67 |
| Compute `currentDayWeek` from Calendar | 71 |
| Compute `currentDayMonth` from Calendar | 72 |
| Always add "Daily" to frequencies list | 75 |
| Conditional: add explicit `frequency` param if non-empty | 76–78 |
| Conditional: add "Weekly" if Saturday (DAY_OF_WEEK == 7) | 80–82 |
| Conditional: add "Monthy" (typo) if first day of month | 84–86 |
| DAO call: `SubscriptionDAO.getAllReport(frequencies)` | 87–88 |
| Loop over subscriptions: build `input` JSON string | 91–138 |
| Inner: `DateUtil.getStartDate(dDate, freq)` per subscription | 95 |
| Inner: hardcoded credentials in JSON (`"ciiadmin"`, `"hui"`) | 102 |
| Inner: `ReportAPI.downloadPDF()` — external HTTP call | 113 |
| Inner branch: success check (`getName() != ""` && `responseCode == HTTP_OK`) | 117 |
| Inner branch: debug mode — send to `RuntimeConf.debugEmailRecipet` | 119–125 |
| Inner branch: production mode — send to subscription recipient | 126–133 |
| Inner branch: failure path — log only, no action | 135–138 |
| Return `mapping.findForward("success")` | 140 |

---

### 1.2 PandoraAction

**File:** `src/main/java/com/action/PandoraAction.java`
**Package:** `com.action`
**Class declaration (line 9):** `public abstract class PandoraAction extends Action`
**Direct superclass:** `org.apache.struts.action.Action`

**Fields / constants:**

| Name | Type | Line | Notes |
|------|------|------|-------|
| `UNDEFINED_PARAM` | `private static final String` | 11 | Value: `"undefined"` — sentinel for JS-submitted undefined values |

**Methods:**

| Method | Signature | Line | Notes |
|--------|-----------|------|-------|
| `getLongRequestParam` | `protected Long getLongRequestParam(HttpServletRequest, String)` | 13–15 | Delegates to `getRequestParam(request, name, (Long) null)` |
| `getRequestParam` (Long overload) | `protected Long getRequestParam(HttpServletRequest, String, Long)` | 17–22 | Returns `defaultValue` if param is blank or literally `"undefined"` |
| `getRequestParam` (String overload) | `protected String getRequestParam(HttpServletRequest, String, String)` | 24–27 | Returns `defaultValue` if param is null; does NOT guard against `"undefined"` |
| `getSessionAttribute` | `protected String getSessionAttribute(HttpSession, String, String)` | 29–33 | Returns `attrib.toString()` or `defaultValue` if null |
| `getLongSessionAttribute` | `protected Long getLongSessionAttribute(HttpSession, String, Long)` | 35–39 | Calls `Long.valueOf(attrib.toString())` — throws if stored value is not a parseable long |
| `getCompId` | `protected String getCompId(HttpSession)` | 41–43 | Convenience wrapper: `getSessionAttribute(session, "sessCompId", null)` |

**Known subclasses (from source tree):**

- `AdminUnitAssignAction` (line 18)
- `AdminManufacturersAction` (line 16)
- `AdminOperatorAction` (line 17)
- `AdminTrainingsAction` (line 14)
- `AdminUnitAccessAction` (line 15)

---

## 2. Test Directory Grep Results

**Grep for `MailerAction` and `PandoraAction` in `src/test/java/`:** **No matches found.**

All four test files in the project cover entirely unrelated packages:

| Test file | Package covered |
|-----------|----------------|
| `UnitCalibrationImpactFilterTest.java` | `com.calibration` |
| `UnitCalibrationTest.java` | `com.calibration` |
| `UnitCalibratorTest.java` | `com.calibration` |
| `ImpactUtilTest.java` | `com.util` (ImpactUtil only) |

**Coverage of `com.action` package: 0 %.**
Neither `MailerAction` nor `PandoraAction` is referenced directly or indirectly by any test.

---

## 3. Coverage Gaps and Findings

---

### MailerAction

**A23-1 | Severity: CRITICAL | MailerAction.execute — entire method is untested**

`MailerAction.execute` is the only method in the class and it is the entry point for the scheduled email reporting pipeline. It touches a DAO, an external PDF-generation API (`ReportAPI.downloadPDF` over HTTP), and `Util.sendMail`. Zero unit or integration tests exist for this method in any form. Any regression introduced here will be undetected until a live email run fails.

---

**A23-2 | Severity: CRITICAL | Hardcoded credentials embedded in JSON payload (line 102)**

```java
String input = "{\"admin_password\":\"ciiadmin\",\"username\": \"hui\",\"filters\":[...]}";
```

The API call to the PDF-generation service is constructed with a hardcoded admin password (`ciiadmin`) and username (`hui`) concatenated directly into a string literal. No test exercises or detects this. Beyond being a secrets-management failure, the absence of tests means there is no safety net if the credential changes or the field is removed.

---

**A23-3 | Severity: HIGH | MailerAction.execute — `date` parameter branch: invalid date string causes uncaught ParseException**

```java
dDate = DateUtil.parseDate(sDate);   // line 55
```

`DateUtil.parseDate` uses `new SimpleDateFormat("yyyy-MM-dd").parse(strDate)` and throws a checked `ParseException` (wrapped as `Exception`). If a caller supplies a malformed `date` parameter (e.g. `date=notadate`), the exception propagates out of `execute` unhandled, resulting in a 500 error page. No test covers the malformed-date input path.

---

**A23-4 | Severity: HIGH | MailerAction.execute — subscriptions loop silently swallows `sendMail` exceptions**

```java
try {
    Util.sendMail(...);
} catch (Exception e) {
    e.printStackTrace();   // lines 124, 132
}
```

Mail-send failures are caught and printed to stderr only; no counter is incremented, no error is surfaced to the caller, and the loop continues. A partial failure (some emails sent, some not) is indistinguishable from full success because the method always returns `mapping.findForward("success")` (line 140). No test verifies the error-swallowing behaviour or asserts that a forward of `"success"` is not misleadingly returned after a failed send.

---

**A23-5 | Severity: HIGH | MailerAction.execute — empty subscription list is untested**

When `SubscriptionDAO.getAllReport(frequencies)` returns an empty list, the loop body is never entered and `findForward("success")` is returned immediately. While this is arguably correct behaviour, no test confirms it, meaning any accidental change to the empty-list path (e.g. a NullPointerException from a later refactor) would go undetected.

---

**A23-6 | Severity: HIGH | MailerAction.execute — `ReportAPI.downloadPDF` failure path is untested (lines 135–138)**

```java
} else {
    log.info("Report generate failed: " + subscriptionBean.getName() + " data:" + input);
}
```

When `getName()` is empty or `responseCode != HTTP_OK`, the failure is logged but no action is taken. No test verifies:
- that an HTTP non-200 from the PDF API does not send an email
- that `getName()` being blank is correctly detected
- that the loop continues processing subsequent subscriptions after a single failure

---

**A23-7 | Severity: HIGH | MailerAction.execute — `debug` mode email routing is untested (lines 119–125)**

When `request.getParameter("debug")` equals `"t"`, email is sent to `RuntimeConf.debugEmailRecipet` instead of the real recipient. No test confirms the routing split. A defect here could silently redirect all production emails to a debug address.

---

**A23-8 | Severity: MEDIUM | MailerAction.execute — frequency branching logic is untested**

Four frequency branches exist:

| Condition | Frequency added |
|-----------|----------------|
| Always | "Daily" |
| `frequency` param non-empty | value of `frequency` param |
| `currentDayWeek == 7` (Saturday) | "Weekly" |
| `currentDayMonth == 1` (1st of month) | "Monthy" *(typo — see A23-9)* |

No test drives `execute` with a Saturday date, a first-of-month date, or an explicit `frequency` parameter to confirm the correct subscriptions are queried.

---

**A23-9 | Severity: MEDIUM | MailerAction.execute — typo `"Monthy"` in frequency string (line 85)**

```java
frequencies.add("Monthy");   // should be "Monthly"
```

The string `"Monthy"` will never match any subscription whose `frequency` column contains `"Monthly"`. Monthly email subscriptions are silently skipped on the first of each month. Because there are no tests, this typo has survived undetected. `DateUtil.getStartDate` correctly handles `"Monthly"` (line 107 of `DateUtil.java`) but `MailerAction` will never pass that string to the DAO query.

---

**A23-10 | Severity: MEDIUM | MailerAction.execute — `arrUser` list is accessed without null or bounds check (line 108)**

```java
reportAPI.setrEmail(subscriptionBean.getArrUser().get(0).getEmail());
```

If `getArrUser()` returns `null` or an empty list, this line throws a `NullPointerException` or `IndexOutOfBoundsException` respectively. The exception is unhandled at this point in the loop (the try-catch does not cover this statement), so it propagates out of `execute`. No test covers a subscription with a missing or empty user list.

---

**A23-11 | Severity: MEDIUM | MailerAction.execute — `company_id` is hardcoded to `1` in JSON payload (line 102)**

```java
{\"company_id\":1}
```

The company ID embedded in the report request is always `1` regardless of the subscription being processed. If the system hosts multiple companies, all reports will be filtered to company 1. No test covers multi-company scenarios or alerts on the hardcoded value.

---

**A23-12 | Severity: LOW | MailerAction.execute — deprecated `Calendar` constant usage (lines 71–72)**

```java
int currentDayWeek  = currentDate.get(currentDate.DAY_OF_WEEK);    // should be Calendar.DAY_OF_WEEK
int currentDayMonth = currentDate.get(currentDate.DAY_OF_MONTH);   // should be Calendar.DAY_OF_MONTH
```

Instance field access on a static constant (`currentDate.DAY_OF_WEEK` instead of `Calendar.DAY_OF_WEEK`) is a deprecated pattern flagged by modern Java linters. While functionally correct today, it is a code quality gap that tests would naturally surface via static analysis integration.

---

### PandoraAction

**A23-13 | Severity: CRITICAL | PandoraAction — zero test coverage for the base class used by 5 action classes**

`PandoraAction` is the abstract base class for `AdminUnitAssignAction`, `AdminManufacturersAction`, `AdminOperatorAction`, `AdminTrainingsAction`, and `AdminUnitAccessAction`. Its utility methods (`getLongRequestParam`, `getRequestParam`, `getSessionAttribute`, `getLongSessionAttribute`, `getCompId`) are invoked by every subclass on every request. None of these methods have any test coverage — direct or indirect. A regression in any method silently breaks all five dependent actions.

---

**A23-14 | Severity: HIGH | PandoraAction.getRequestParam (String overload, line 24) — does NOT guard against the `"undefined"` sentinel**

The Long overload (line 17) explicitly guards against the JS-submitted `"undefined"` string:

```java
// Long overload — guards against "undefined"
return StringUtils.isBlank(param) || UNDEFINED_PARAM.equalsIgnoreCase(param) ? defaultValue : Long.valueOf(param);
```

The String overload (line 24) does not:

```java
// String overload — no "undefined" guard
String param = request.getParameter(name);
return param == null ? defaultValue : param;
```

If a JavaScript client submits an undefined value for a String parameter, the literal string `"undefined"` is returned to business logic rather than `defaultValue`. This inconsistency is untested and its downstream effects in subclasses are unknown.

---

**A23-15 | Severity: HIGH | PandoraAction.getLongSessionAttribute — `Long.valueOf(attrib.toString())` throws NumberFormatException on non-numeric session values (line 38)**

```java
return attrib == null ? defaultValue : Long.valueOf(attrib.toString());
```

If any code path stores a non-numeric value in the named session attribute, `Long.valueOf` throws `NumberFormatException`, which propagates as an unhandled runtime exception. There is no test verifying the method's behaviour with a corrupt or unexpected session value.

---

**A23-16 | Severity: HIGH | PandoraAction.getCompId — returns `null` default when `sessCompId` is missing from session (line 42)**

```java
return getSessionAttribute(session, "sessCompId", null);
```

The default value is `null`. Any caller that does not null-check the return value (e.g. `AdminUnitAssignAction` line 26: `Integer.parseInt(sessCompId)`) will throw a `NullPointerException` when the session attribute is absent (e.g. unauthenticated or expired session). No test covers the missing-session-attribute path for `getCompId` or any of the five subclasses that rely on it.

---

**A23-17 | Severity: HIGH | PandoraAction — no authentication or authorisation gate in the base class**

`PandoraAction` provides no `execute` method and no session-validation hook. Authentication and authorisation are delegated entirely to subclasses and/or Struts interceptors. If a subclass forgets to validate session state before calling `getCompId` or similar helpers, unauthenticated requests proceed to business logic. Because no tests exercise any action class, this architectural gap has no safety net.

---

**A23-18 | Severity: MEDIUM | PandoraAction.getLongRequestParam — always delegates with `null` default; callers receive null without documentation (lines 13–15)**

```java
protected Long getLongRequestParam(HttpServletRequest request, String name) {
    return getRequestParam(request, name, (Long) null);
}
```

This is a convenience shorthand that always returns `null` for a missing or `"undefined"` parameter. Callers that auto-unbox the result (e.g. `long val = getLongRequestParam(...)`) will throw a `NullPointerException`. No test covers this null-unboxing failure path.

---

**A23-19 | Severity: MEDIUM | PandoraAction — `assert` statements are the only guard on blank parameter names (lines 18, 30, 36)**

```java
assert StringUtils.isNotBlank(name) : "request param name must not be blank";
```

Java `assert` statements are disabled by default at runtime unless the JVM is launched with `-ea`. In a standard Tomcat deployment, these guards are silently skipped. Passing a blank `name` to `getRequestParam` (Long overload) will call `request.getParameter("")` and potentially return an unexpected result rather than failing fast. No test confirms this guard behaviour.

---

**A23-20 | Severity: LOW | PandoraAction.getSessionAttribute — `attrib.toString()` is used rather than a cast (line 32)**

```java
return attrib == null ? defaultValue : attrib.toString();
```

This is a defensive choice (avoids `ClassCastException`), but it means that a non-String session attribute (e.g. an `Integer` stored by accident) is silently coerced to its string representation rather than raising a type error. No test confirms expected behaviour when the session attribute type is unexpected.

---

## 4. Summary Table

| Finding | Severity | File | Description |
|---------|----------|------|-------------|
| A23-1 | CRITICAL | MailerAction | `execute` method has zero test coverage |
| A23-2 | CRITICAL | MailerAction | Hardcoded credentials (`ciiadmin`/`hui`) in JSON payload, untested and undetected |
| A23-3 | HIGH | MailerAction | Invalid `date` param causes uncaught `ParseException` |
| A23-4 | HIGH | MailerAction | `sendMail` exceptions silently swallowed; method always returns success |
| A23-5 | HIGH | MailerAction | Empty subscription list path untested |
| A23-6 | HIGH | MailerAction | PDF API failure path only logs; behaviour untested |
| A23-7 | HIGH | MailerAction | Debug email routing (`debug=t`) untested |
| A23-8 | MEDIUM | MailerAction | Frequency branching logic (Weekly, Monthly, explicit param) untested |
| A23-9 | MEDIUM | MailerAction | Typo `"Monthy"` silently prevents monthly subscriptions from ever running |
| A23-10 | MEDIUM | MailerAction | No null/bounds check on `getArrUser().get(0)`; NPE or IOOBE on empty user list |
| A23-11 | MEDIUM | MailerAction | `company_id` hardcoded to `1` in every report request |
| A23-12 | LOW | MailerAction | Deprecated instance-access of `Calendar` static constants |
| A23-13 | CRITICAL | PandoraAction | Base class has zero test coverage; 5 action subclasses inherit untested utilities |
| A23-14 | HIGH | PandoraAction | String overload of `getRequestParam` does not guard against `"undefined"` sentinel |
| A23-15 | HIGH | PandoraAction | `getLongSessionAttribute` throws `NumberFormatException` on non-numeric session values |
| A23-16 | HIGH | PandoraAction | `getCompId` returns `null` default; callers risk NPE on unauthenticated sessions |
| A23-17 | HIGH | PandoraAction | No auth/authz gate in base class; unauthenticated access to subclass logic is untested |
| A23-18 | MEDIUM | PandoraAction | `getLongRequestParam` returns boxed `null`; auto-unboxing callers will NPE |
| A23-19 | MEDIUM | PandoraAction | `assert` guards disabled at runtime in standard Tomcat; blank names not enforced |
| A23-20 | LOW | PandoraAction | `attrib.toString()` silently coerces unexpected session attribute types |

**Total findings: 20**
**CRITICAL: 3 | HIGH: 8 | MEDIUM: 6 | LOW: 3**
