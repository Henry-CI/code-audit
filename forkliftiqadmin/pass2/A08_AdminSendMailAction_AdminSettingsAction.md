# Pass 2 Test-Coverage Audit Report
**Audit Run:** 2026-02-26-01
**Agent ID:** A08
**Date:** 2026-02-26
**Scope:** AdminSendMailAction, AdminSettingsAction

---

## 1. Source Files Examined

| # | File | Lines |
|---|------|-------|
| 1 | `src/main/java/com/action/AdminSendMailAction.java` | 122 |
| 2 | `src/main/java/com/action/AdminSettingsAction.java` | 81 |

---

## 2. Reading-Evidence Block

### 2.1 AdminSendMailAction

**Class:** `com.action.AdminSendMailAction` extends `org.apache.struts.action.Action`

**Fields / Constants:**

| Name | Type | Initializer | Line |
|------|------|-------------|------|
| `driverDao` | `DriverDAO` | `DriverDAO.getInstance()` | 31 |

**Methods:**

| Method | Signature | Return | Lines | Notes |
|--------|-----------|--------|-------|-------|
| `execute` | `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | `ActionForward` | 33–75 | throws Exception; Struts entry point |
| `sendMail` | `sendMail(String subject, String mBody, String rName, String rEmail, String sName, String sEmail)` | `boolean` | 77–109 | throws AddressException, MessagingException; public |
| `isValidEmailAddress` | `isValidEmailAddress(String email)` | `boolean` | 111–120 | public |

**Key logic branches in `execute`:**
- Line 43: `if (accountAction.equalsIgnoreCase("send_mail"))`
  - Line 47: `if (!isValidEmailAddress(sendMailForm.getEmail()))` → forward "failure", sets `result=failed`
  - Line 55: `if (sendMail(...))` → forward "success" or "failure"
- Line 68: else branch → loads `arrAdminDriver` list via DAO, forwards "failure"

**Key logic branches in `sendMail`:**
- Line 89–94: inner try/catch on `setRecipients` — exception swallowed via `System.out.println`
- Line 99–103: inner try/catch on `Transport.send` — exception swallowed via `System.out.println`
- Line 105–107: outer catch on `Throwable` — stack trace printed, method still returns `true`
- Line 108: always returns `true` (never returns `false`)

**Key logic branches in `isValidEmailAddress`:**
- Line 112: blank/null check via `StringUtils.isBlank`
- Line 116–119: regex match

---

### 2.2 AdminSettingsAction

**Class:** `com.action.AdminSettingsAction` extends `org.apache.struts.action.Action`

**Fields / Constants:** None declared at class level.

**Methods:**

| Method | Signature | Return | Lines | Notes |
|--------|-----------|--------|-------|-------|
| `execute` | `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | `ActionForward` | 22–80 | throws Exception; Struts entry point; only method |

**Key logic branches in `execute`:**
- Line 30–31: `sessCompId` null-guard (defaults to `""`)
- Line 32: `sessUserId` null-guard (defaults to `0`)
- Line 38–40: null-guards for `redImpactAlert`, `redImpactSMSAlert`, `driverDenyAlert` (default to `""`)
- Line 41: `sessionToken` null-guard (defaults to `""`)
- Line 43: `DateFormatDAO.getAll()` always called
- Line 45: early-return guard: `if (!action.equalsIgnoreCase("savesettings")) return mapping.findForward("adminsettings")`
- Line 48: `dao.getCompanyContactsByCompId(...)` — `.get(0)` called directly on result; throws `IndexOutOfBoundsException` if empty
- Line 53: `Integer.parseInt(timezone)` — throws `NumberFormatException` if non-numeric
- Line 63–67: RedImpactAlert subscription add/delete logic (three-state: "on"+"no existing", "", other)
- Line 68–72: RedImpactSMSAlert subscription add/delete logic (same three-state pattern)
- Line 73–77: DriverDenyAlert subscription add/delete logic (same three-state pattern)
- Line 79: `dao.updateCompSettings(company)` result determines forward ("success" / "failure")

---

## 3. Test Coverage Search — Grep Results

**Search targets:** `AdminSendMailAction`, `AdminSettingsAction`
**Search path:** `src/test/java/`

```
Result: No matches found
```

**Existing test files (4 total):**

| File | Classes Covered |
|------|----------------|
| `com/calibration/UnitCalibrationImpactFilterTest.java` | `UnitCalibrationImpactFilter` |
| `com/calibration/UnitCalibrationTest.java` | `UnitCalibration` |
| `com/calibration/UnitCalibratorTest.java` | `UnitCalibrator` |
| `com/util/ImpactUtilTest.java` | `ImpactUtil` |

**Conclusion:** Zero test coverage — direct or indirect — exists for either `AdminSendMailAction` or `AdminSettingsAction`. No test file references either class name, any of their methods, or their companion action forms (`AdminSendMailActionForm`, `AdminSettingsActionForm`).

---

## 4. Coverage Gap Findings

---

### A08-1 | Severity: CRITICAL | AdminSendMailAction.execute — zero test coverage

No test exists for the Struts `execute` method of `AdminSendMailAction`. None of its three distinct branches (valid email + send succeeds, valid email + send fails, non-send_mail action) are exercised. All business logic, session access, and forward resolution are completely untested.

**File:** `src/main/java/com/action/AdminSendMailAction.java`, lines 33–75

---

### A08-2 | Severity: CRITICAL | AdminSettingsAction.execute — zero test coverage

No test exists for the Struts `execute` method of `AdminSettingsAction`. All subscription management logic, session attribute mutation, timezone lookup, company update, and forward resolution are completely untested.

**File:** `src/main/java/com/action/AdminSettingsAction.java`, lines 22–80

---

### A08-3 | Severity: CRITICAL | sendMail always returns true — defect masked by absent tests

`sendMail` is hard-coded to `return true` on line 108 regardless of whether `InitialContext` lookup fails, `setRecipients` throws, or `Transport.send` throws. The outer `catch (Throwable t)` at line 105 silently prints a stack trace and falls through to the `return true` statement. The `execute` method's branch at line 60 (`} else { ... return mapping.findForward("failure")`) can therefore never be reached through `sendMail` returning `false`. This logical defect is invisible without a test.

**File:** `src/main/java/com/action/AdminSendMailAction.java`, lines 99–108

---

### A08-4 | Severity: HIGH | isValidEmailAddress — no unit tests

`isValidEmailAddress` is a public method containing standalone logic (blank check + regex) that is directly testable without Struts infrastructure. No test covers it for any of the following cases:
- null input
- empty string input
- valid well-formed email
- email missing `@`
- email with IP-literal domain (the regex supports `[x.x.x.x]` form)
- email with special characters in local part
- email with TLD shorter than 2 characters

**File:** `src/main/java/com/action/AdminSendMailAction.java`, lines 111–120

---

### A08-5 | Severity: HIGH | execute — null session guard missing (AdminSendMailAction)

`request.getSession(false)` at line 36 may return `null` if no session exists (the `false` argument suppresses creation). The immediately following line 37 calls `session.getAttribute(...)` unconditionally, which will throw a `NullPointerException`. No test covers this path.

**File:** `src/main/java/com/action/AdminSendMailAction.java`, lines 36–37

---

### A08-6 | Severity: HIGH | execute — null session guard missing (AdminSettingsAction)

`request.getSession(false)` at line 27 may return `null`. Lines 30, 32, and 41 call `session.getAttribute(...)` unconditionally immediately after. A `NullPointerException` would be thrown on any unauthenticated or expired-session request. No test covers this path.

**File:** `src/main/java/com/action/AdminSettingsAction.java`, lines 27–41

---

### A08-7 | Severity: HIGH | execute — NullPointerException when accountAction is null (AdminSendMailAction)

`sendMailForm.getAccountAction()` at line 40 may return `null` (the form field is initialized to `null` in `AdminSendMailActionForm`). Line 43 calls `.equalsIgnoreCase("send_mail")` directly on this value without a null check, which will throw a `NullPointerException`. No test covers this path.

**File:** `src/main/java/com/action/AdminSendMailAction.java`, lines 40, 43

---

### A08-8 | Severity: HIGH | execute — IndexOutOfBoundsException on empty company result (AdminSettingsAction)

Line 48 calls `dao.getCompanyContactsByCompId(...).get(0)` without checking whether the returned list is empty. If the company ID stored in the session does not match any record — e.g., after a data deletion or corrupt session — this throws `IndexOutOfBoundsException` unchecked. No test covers this path.

**File:** `src/main/java/com/action/AdminSettingsAction.java`, line 48

---

### A08-9 | Severity: HIGH | execute — NumberFormatException on non-numeric timezone (AdminSettingsAction)

Line 53 calls `Integer.parseInt(timezone)` where `timezone` originates from `adminSettingsActionForm.getTimezone()`, a user-supplied string. If the value is null, empty, or non-numeric, `Integer.parseInt` throws a `NumberFormatException`. The form's `validate()` method only checks for null/empty/"0" — it does not enforce numeric format. No test covers this path.

**File:** `src/main/java/com/action/AdminSettingsAction.java`, line 53

---

### A08-10 | Severity: HIGH | execute — sessCompId empty string passed to DAO (AdminSettingsAction)

When `session.getAttribute("sessCompId")` is `null`, `sessCompId` defaults to `""` (line 30–31). This empty string is then passed to `dao.getCompanyContactsByCompId(sessCompId, ...)` (line 48), where `CompanyDAO.getCompanyContactsByCompId` has an `assert StringUtils.isNotBlank(compId)` guard (line 559 of CompanyDAO). In non-debug JVM runs assertions are disabled, so the empty string reaches `Long.parseLong("")` and throws `NumberFormatException`. No test covers this path.

**File:** `src/main/java/com/action/AdminSettingsAction.java`, lines 30–31, 48

---

### A08-11 | Severity: HIGH | execute — sessCompId empty string path (AdminSendMailAction)

Similarly, when `session.getAttribute("sessCompId")` is `null` in `AdminSendMailAction`, `sessCompId` defaults to `""` (line 37). In the non-`send_mail` branch (line 68–74), `sessCompId` is passed directly to `driverDao.getAllDriver(sessCompId, true)`. No test covers behavior when `sessCompId` is blank.

**File:** `src/main/java/com/action/AdminSendMailAction.java`, lines 37, 70–71

---

### A08-12 | Severity: MEDIUM | execute — non-"send_mail" branch behavior untested (AdminSendMailAction)

The else branch at lines 68–74 loads all drivers for the company and forwards to "failure". No test verifies that `arrAdminDriver` is correctly set as a request attribute, or that the "failure" forward is returned, when `accountAction` is any value other than `"send_mail"`.

**File:** `src/main/java/com/action/AdminSendMailAction.java`, lines 68–74

---

### A08-13 | Severity: MEDIUM | execute — early-return (non-savesettings action) path untested (AdminSettingsAction)

Line 45 returns `mapping.findForward("adminsettings")` immediately whenever `action` is not `"savesettings"`. No test verifies this path — including the state of request attributes (only `dateFormats` is set before this guard) and that no side-effect DAO calls are made.

**File:** `src/main/java/com/action/AdminSettingsAction.java`, line 45

---

### A08-14 | Severity: MEDIUM | execute — alert subscription three-state logic untested (AdminSettingsAction)

Lines 63–77 contain six conditional branches across three alert types (`redImpactAlert`, `redImpactSMSAlert`, `driverDenyAlert`). Each has three possible states:

1. `"on"` and no existing subscription → `addUserSubscription` is called
2. `""` → `deleteUserSubscription` is called
3. Any other value (e.g., form delivers `"off"`, or anything non-blank non-"on") → neither add nor delete is called (silent no-op)

No test covers any of these six branches or their interactions. In particular, the silent no-op for state 3 means an existing subscription is never removed when the alert is explicitly disabled by a value other than empty string.

**File:** `src/main/java/com/action/AdminSettingsAction.java`, lines 63–77

---

### A08-15 | Severity: MEDIUM | execute — session attribute mutation after timezone lookup untested (AdminSettingsAction)

Lines 54–57 mutate four session attributes (`timezoneId`, `sessTimezone`, `sessDateTimeFormat`, `sessDateFormat`). No test asserts these attributes are set to the correct values after a successful save, or that they remain unchanged when an exception occurs mid-method.

**File:** `src/main/java/com/action/AdminSettingsAction.java`, lines 54–57

---

### A08-16 | Severity: MEDIUM | execute — company pin explicitly nulled before update (AdminSettingsAction)

Line 58 calls `company.setPin(null)`. This is a deliberate design choice to avoid persisting a PIN via the settings update path, but it is undocumented and untested. No test verifies that the pin field is null at the point `updateCompSettings` is called, nor is there a test that confirms the intent of this line.

**File:** `src/main/java/com/action/AdminSettingsAction.java`, line 58

---

### A08-17 | Severity: MEDIUM | execute — updateCompSettings failure forward untested (AdminSettingsAction)

Line 79 forwards to "failure" when `dao.updateCompSettings(company)` returns `false`. No test simulates a DAO update failure (e.g., zero rows updated) to verify the "failure" forward is returned.

**File:** `src/main/java/com/action/AdminSettingsAction.java`, line 79

---

### A08-18 | Severity: MEDIUM | sendMail — JNDI lookup failure path untested (AdminSendMailAction)

If the JNDI `InitialContext` lookup for `"java:comp/env"` or `"mail/Session"` fails at lines 81–83, the outer `catch (Throwable t)` at line 105 catches it silently, prints a stack trace, and returns `true`. No test simulates a missing JNDI mail session to verify graceful degradation or appropriate error propagation.

**File:** `src/main/java/com/action/AdminSendMailAction.java`, lines 80–108

---

### A08-19 | Severity: MEDIUM | sendMail — recipient parse exception swallowed silently (AdminSendMailAction)

Lines 89–94 catch any exception from `InternetAddress.parse(rEmail, false)` and print it to `System.out`. If recipient address parsing fails, the message is still sent — but with no recipient. No test exercises this path, and there is no test verifying the observable side-effect (i.e., a send attempt with no recipient).

**File:** `src/main/java/com/action/AdminSendMailAction.java`, lines 89–94

---

### A08-20 | Severity: MEDIUM | sendMail — Transport.send exception swallowed silently (AdminSendMailAction)

Lines 99–103 catch any exception from `Transport.send(message)` and print it to `System.out`. On send failure, `sendMail` still returns `true`, causing `execute` to set `result=success` and forward to "success" even though no email was delivered. No test covers this path.

**File:** `src/main/java/com/action/AdminSendMailAction.java`, lines 99–103

---

### A08-21 | Severity: LOW | execute — result attribute value not tested for non-send_mail branch (AdminSendMailAction)

The else branch at line 73 returns the "failure" forward but does not set `request.setAttribute("result", ...)`. The "send_mail" branches always set a `result` attribute before forwarding. The absence of a `result` attribute on the non-send_mail path is inconsistent. No test verifies this discrepancy.

**File:** `src/main/java/com/action/AdminSendMailAction.java`, lines 68–74

---

### A08-22 | Severity: LOW | isValidEmailAddress — regex does not reject consecutive dots in local part

The regex pattern at line 116 accepts strings such as `"user..name@example.com"`, which is invalid per RFC 5321. No test documents or enforces the intended validation boundary. This is a quality gap that tests would have surfaced.

**File:** `src/main/java/com/action/AdminSendMailAction.java`, lines 116–119

---

### A08-23 | Severity: LOW | sendMail — hardcoded sender address untested (AdminSendMailAction)

Line 87 hardcodes `"info@ciiquk.com"` as the From address. No test verifies this value, documents it as intentional, or confirms behaviour if this address becomes invalid in the mail server configuration.

**File:** `src/main/java/com/action/AdminSendMailAction.java`, line 87

---

### A08-24 | Severity: LOW | sendMail — sName and rName parameters unused (AdminSendMailAction)

The `sendMail` signature accepts `rName` (line 78) and `sName` (line 78) but neither parameter is used anywhere in the method body. The call site at line 55 passes empty strings for both. No test documents or enforces what these parameters are intended for.

**File:** `src/main/java/com/action/AdminSendMailAction.java`, lines 77–78, 55

---

### A08-25 | Severity: INFO | AdminSendMailActionForm — form field `id` never read in execute (AdminSendMailAction)

`AdminSendMailActionForm` declares an `id` field (line 7 of the form class) with a getter and setter, but `AdminSendMailAction.execute` never reads `sendMailForm.getId()`. No test documents or validates whether this field is intentionally unused at this layer.

**File:** `src/main/java/com/action/AdminSendMailAction.java`, line 39; `src/main/java/com/actionform/AdminSendMailActionForm.java`, line 7

---

### A08-26 | Severity: INFO | AdminSettingsAction — no dependency injection; DAO instantiated via singleton (AdminSettingsAction)

`CompanyDAO`, `TimezoneDAO`, `SubscriptionDAO`, and `DateFormatDAO` are all accessed via static factory methods or static methods inside `execute`. There is no interface or constructor injection, making it impossible to mock dependencies for unit testing without a framework such as PowerMock. This is a structural testability defect that explains — but does not excuse — the absence of tests.

**File:** `src/main/java/com/action/AdminSettingsAction.java`, lines 47, 53, 59–61, 64–76

---

### A08-27 | Severity: INFO | AdminSendMailAction — DriverDAO held as instance field but DriverDAO is a singleton (AdminSendMailAction)

`driverDao` is declared as an instance field (line 31) initialized via `DriverDAO.getInstance()`. Because `DriverDAO` is a singleton, the field reference is effectively global state. No test documents the singleton lifecycle, and there is no way to inject a test double without reflection or a mocking framework that handles static/singleton state.

**File:** `src/main/java/com/action/AdminSendMailAction.java`, line 31

---

## 5. Summary Table

| Finding | Severity | Description |
|---------|----------|-------------|
| A08-1 | CRITICAL | AdminSendMailAction.execute — zero test coverage |
| A08-2 | CRITICAL | AdminSettingsAction.execute — zero test coverage |
| A08-3 | CRITICAL | sendMail always returns true — defect masked by absent tests |
| A08-4 | HIGH | isValidEmailAddress — no unit tests for any input case |
| A08-5 | HIGH | Null session NPE in AdminSendMailAction.execute |
| A08-6 | HIGH | Null session NPE in AdminSettingsAction.execute |
| A08-7 | HIGH | NPE when accountAction is null in AdminSendMailAction.execute |
| A08-8 | HIGH | IndexOutOfBoundsException on empty company result in AdminSettingsAction.execute |
| A08-9 | HIGH | NumberFormatException on non-numeric timezone in AdminSettingsAction.execute |
| A08-10 | HIGH | Empty sessCompId propagates to DAO causing NumberFormatException in AdminSettingsAction |
| A08-11 | HIGH | Empty sessCompId propagates to DriverDAO in AdminSendMailAction |
| A08-12 | MEDIUM | Non-"send_mail" branch in AdminSendMailAction.execute untested |
| A08-13 | MEDIUM | Early-return non-savesettings path in AdminSettingsAction.execute untested |
| A08-14 | MEDIUM | Alert subscription three-state logic in AdminSettingsAction.execute untested |
| A08-15 | MEDIUM | Session attribute mutation after timezone lookup untested |
| A08-16 | MEDIUM | company.setPin(null) intent undocumented and untested |
| A08-17 | MEDIUM | updateCompSettings failure forward untested |
| A08-18 | MEDIUM | JNDI lookup failure path in sendMail untested |
| A08-19 | MEDIUM | Recipient parse exception silently swallowed in sendMail |
| A08-20 | MEDIUM | Transport.send exception silently swallowed; false success returned |
| A08-21 | LOW | result attribute absent on non-send_mail forward path |
| A08-22 | LOW | Regex accepts invalid consecutive-dot local parts |
| A08-23 | LOW | Hardcoded sender address untested |
| A08-24 | LOW | rName and sName parameters declared but never used |
| A08-25 | INFO | AdminSendMailActionForm.id field never read in execute |
| A08-26 | INFO | No dependency injection; DAOs untestable without PowerMock |
| A08-27 | INFO | DriverDAO singleton held as instance field; no test-double path |

**Total findings: 27**
- CRITICAL: 3
- HIGH: 8
- MEDIUM: 9
- LOW: 4
- INFO: 3

---

## 6. Recommended Test Classes

```
src/test/java/com/action/AdminSendMailActionTest.java
src/test/java/com/action/AdminSettingsActionTest.java
src/test/java/com/action/AdminSendMailActionIsValidEmailTest.java
```

Key scenarios to cover per class:

**AdminSendMailAction:**
- `execute` with null session → expect NPE or graceful error
- `execute` with null `accountAction` → expect NPE or guard
- `execute` with `accountAction="send_mail"` and invalid email → result="failed", forward="failure"
- `execute` with `accountAction="send_mail"` and valid email, mail sends → result="success", forward="success"
- `execute` with `accountAction="send_mail"` and valid email, JNDI failure → result still "success" (documents the defect in A08-3)
- `execute` with any other `accountAction` → `arrAdminDriver` set, forward="failure"
- `isValidEmailAddress` with null, empty, valid, and malformed inputs
- `sendMail` with JNDI unavailable → verify returns `true` (documents A08-3)

**AdminSettingsAction:**
- `execute` with null session → expect NPE
- `execute` with `action != "savesettings"` → forward="adminsettings", no DAO writes
- `execute` with `action="savesettings"` and empty company list from DAO → expect IOOBE
- `execute` with non-numeric timezone → expect NFE
- `execute` with each alert flag combination (on/existing, on/new, empty, other)
- `execute` with `updateCompSettings` returning false → forward="failure"
- `execute` with `updateCompSettings` returning true → forward="success"
- Session attributes (`timezoneId`, `sessTimezone`, `sessDateTimeFormat`, `sessDateFormat`) set correctly
