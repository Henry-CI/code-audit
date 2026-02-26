# Pass 2 Test-Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A28
**Date:** 2026-02-26
**Scope:** SwitchLanguageAction, SwitchRegisterAction, WelcomeAction

---

## 1. Reading Evidence

### 1.1 SwitchLanguageAction
**File:** `src/main/java/com/action/SwitchLanguageAction.java`
**Class:** `com.action.SwitchLanguageAction extends org.apache.struts.action.Action`

**Fields / Constants:**
| Name | Type | Line | Notes |
|------|------|------|-------|
| `log` | `static Logger` | 20 | Private static, initialized via `InfoLogger.getLogger` |

**Methods:**
| Method | Signature | Lines | Visibility |
|--------|-----------|-------|------------|
| `execute` | `ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 22-69 | `public` |
| `getCookie` | `static Cookie getCookie(HttpServletRequest, String)` | 71-81 | `public static` |
| `getLocale` | `static Locale getLocale(String)` | 83-109 | `public static` |

**Key logic paths in `execute` (lines 22-69):**
- Line 25: `request.getParameter("language")` — null-safe defaulting to `""`
- Lines 26: calls `getLocale(language)`
- Lines 28-35: branch on `language.equalsIgnoreCase("0")` — set browser locale vs. mapped locale in session
- Lines 38-66: branch on `language.equalsIgnoreCase("0")`:
  - `"0"` path: clear existing cookie (if present) by setting maxAge=0, value=null
  - Non-`"0"` path: update existing cookie value OR create new `ckLanguage` cookie with maxAge=86400
- Line 67: `request.setAttribute("language", language)`
- Line 68: `mapping.findForward("success")`

**Key logic paths in `getCookie` (lines 71-81):**
- Line 72: null-check on `request.getCookies()`
- Lines 73-77: linear scan for cookie by name
- Line 80: returns `null` if not found

**Key logic paths in `getLocale` (lines 83-109):**
- `"1"` → `Locale.ENGLISH`
- `"2"` → `Locale.SIMPLIFIED_CHINESE`
- `"3"` → `new Locale("tr","TR","")`
- `"4"` → `new Locale("ms","MY","")`
- Any other input (including `"0"`, `""`, `null` equivalent) → returns `null`

---

### 1.2 SwitchRegisterAction
**File:** `src/main/java/com/action/SwitchRegisterAction.java`
**Class:** `com.action.SwitchRegisterAction extends org.apache.struts.action.Action`

**Fields / Constants:**
| Name | Type | Line | Notes |
|------|------|------|-------|
| `log` | `static Logger` | 18 | Private static, initialized via `InfoLogger.getLogger` |

**Methods:**
| Method | Signature | Lines | Visibility |
|--------|-----------|-------|------------|
| `execute` | `ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 20-31 | `public` |

**Key logic paths in `execute` (lines 20-31):**
- Line 23: `request.getSession(false)` — retrieves existing session WITHOUT creating one; result stored in local variable `session` with no null-check
- Line 25: `TimezoneDAO.getInstance().getAllTimezone()` — live DB call; result stored in session attribute `"arrTimezone"`
- Line 26: `LanguageDAO.getInstance().getAllLan()` — live DB call; result stored in session attribute `"arrLanguage"`
- Line 27: `session.setAttribute("accountAction", "register")` — hardcoded string constant
- Line 29: `mapping.findForward("success")`

---

### 1.3 WelcomeAction
**File:** `src/main/java/com/action/WelcomeAction.java`
**Class:** `com.action.WelcomeAction extends org.apache.struts.action.Action`

**Fields / Constants:**
| Name | Type | Line | Notes |
|------|------|------|-------|
| `log` | `static Logger` | 35 | Private static, initialized via `InfoLogger.getLogger` |

**Methods:**
| Method | Signature | Lines | Visibility |
|--------|-----------|-------|------------|
| `execute` | `ActionForward execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 37-49 | `public` |

**Key logic paths in `execute` (lines 37-49):**
- Line 40: delegates to `SwitchLanguageAction.getCookie(request, "ckLanguage")`
- Lines 41-45: if cookie is non-null, calls `SwitchLanguageAction.getLocale(cookie.getValue())` and stores result into session under `Globals.LOCALE_KEY`
- Line 47: `AdvertismentDAO.getInstance().getAllAdvertisement()` — live DB call; result stored in session attribute `"sessAds"`
- Line 48: `mapping.findForward("success")`

---

## 2. Test Coverage Grep Confirmation

**Test directory searched:** `src/test/java/`

**Existing test files (4 total):**
1. `com/calibration/UnitCalibrationImpactFilterTest.java`
2. `com/calibration/UnitCalibrationTest.java`
3. `com/calibration/UnitCalibratorTest.java`
4. `com/util/ImpactUtilTest.java`

**Grep results for class names in test directory:**
- `SwitchLanguageAction` — **0 matches**
- `SwitchRegisterAction` — **0 matches**
- `WelcomeAction` — **0 matches**

**Conclusion:** No direct or indirect test coverage exists for any of the three action classes under audit. The four existing tests cover only calibration domain objects and a utility class; they have no dependency on or reference to any action class.

---

## 3. Coverage Gap Findings

---

### SwitchLanguageAction

**A28-1 | Severity: CRITICAL | `execute` — zero test coverage for the entire method**
`execute` (lines 22-69) is the primary Struts action handler and contains all session-locale and cookie-management logic. No test exercises it under any input condition. No mock of `HttpServletRequest`, `HttpServletResponse`, `ActionMapping`, or `ActionForm` exists anywhere in the test suite.

**A28-2 | Severity: HIGH | `execute` — language parameter null path not tested**
Line 25 performs: `request.getParameter("language") == null ? "" : request.getParameter("language")`. The null branch silently substitutes an empty string. The downstream `getLocale("")` call returns `null` (no matching branch in `getLocale`), and that `null` locale is then stored into the session via `session.setAttribute(Globals.LOCALE_KEY, null)` (line 34). No test verifies this null-default behaviour or its session side-effect.

**A28-3 | Severity: HIGH | `execute` — language `"0"` (browser-locale reset) path not tested**
The `language.equalsIgnoreCase("0")` branch (lines 28-31, 39-47):
- Sets session locale to the browser's own locale (line 30)
- Clears the `ckLanguage` cookie by setting `maxAge=0` and `value=null` when the cookie exists (lines 44-46)
- Does nothing to the cookie when the cookie does not exist
None of these three sub-cases are tested.

**A28-4 | Severity: HIGH | `execute` — non-zero language with existing cookie not tested**
Lines 53-57: when `language` is not `"0"` and a `ckLanguage` cookie already exists, the existing cookie's value is overwritten. No test verifies the cookie is updated correctly.

**A28-5 | Severity: HIGH | `execute` — non-zero language with no existing cookie (new cookie creation) not tested**
Lines 61-63: when `language` is not `"0"` and no `ckLanguage` cookie exists, a new `Cookie("ckLanguage", language)` is created with `maxAge=86400` and added to the response. No test verifies cookie name, value, or max-age.

**A28-6 | Severity: HIGH | `execute` — `request.setAttribute("language", language)` not tested**
Line 67 sets a request attribute that JSP/view layers depend on. No test verifies this attribute is populated after any `execute` invocation.

**A28-7 | Severity: HIGH | `getLocale` — no test coverage for any language code**
`getLocale` is `public static` and fully testable without a servlet container. Four distinct locale-mapping branches exist:
- `"1"` → `Locale.ENGLISH`
- `"2"` → `Locale.SIMPLIFIED_CHINESE`
- `"3"` → `new Locale("tr","TR","")`
- `"4"` → `new Locale("ms","MY","")`
None are tested.

**A28-8 | Severity: HIGH | `getLocale` — unrecognised / default input returns null, not tested**
Any input that does not match `"1"`, `"2"`, `"3"`, or `"4"` (including `""`, `"0"`, `"5"`, or any arbitrary string) causes `getLocale` to return `null`. Callers (both `execute` in `SwitchLanguageAction` line 26 and `WelcomeAction` line 43) store this `null` directly into the session without a null-guard. No test covers the null-return case or its downstream effect.

**A28-9 | Severity: HIGH | `getCookie` — no test coverage for any path**
`getCookie` is `public static` and fully testable in isolation. Three distinct paths exist:
- `request.getCookies()` returns `null` → returns `null`
- Cookies present, target name found → returns the matching `Cookie`
- Cookies present, target name not found → returns `null`
None are tested.

**A28-10 | Severity: MEDIUM | `getCookie` — multiple cookies with same name not tested**
The linear scan (lines 73-76) returns the first cookie matching the name. No test verifies the behaviour when duplicate cookie names are present (which is valid per RFC 6265).

**A28-11 | Severity: MEDIUM | `execute` — forward result ("success") never asserted**
No test verifies that `mapping.findForward("success")` is invoked and that the returned `ActionForward` is non-null, leaving misconfigured Struts mappings undetected.

---

### SwitchRegisterAction

**A28-12 | Severity: CRITICAL | `execute` — zero test coverage for the entire method**
`execute` (lines 20-31) is the sole method and is completely untested. No mock of any collaborator (`TimezoneDAO`, `LanguageDAO`, `ActionMapping`, `HttpServletRequest`) exists in the test suite.

**A28-13 | Severity: CRITICAL | `execute` — NullPointerException when session does not exist**
Line 23: `request.getSession(false)` deliberately avoids creating a new session. The returned `HttpSession` reference is stored in local variable `session` with no null-check. If no active session exists (e.g., a first request with no prior session, or after session expiry), `session` is `null`. Lines 25-27 then call `session.setAttribute(...)`, resulting in an unconditional `NullPointerException`. This is a runtime crash path that no test exercises or even documents.

**A28-14 | Severity: HIGH | `execute` — `TimezoneDAO.getAllTimezone()` exception path not tested**
`TimezoneDAO.getAllTimezone()` throws `Exception` (ultimately re-thrown as `SQLException`) on DB failure. The `execute` method declares `throws Exception` and propagates all DAO exceptions to the Struts framework with no local error handling or user-facing error response. No test verifies the failure mode or what the framework presents to the user.

**A28-15 | Severity: HIGH | `execute` — `LanguageDAO.getAllLan()` exception path not tested**
Same concern as A28-14 for `LanguageDAO.getAllLan()`. Additionally, if `TimezoneDAO.getAllTimezone()` succeeds but `LanguageDAO.getAllLan()` fails, the `"arrTimezone"` session attribute is already populated while `"arrLanguage"` is never set. The partial session state is not tested.

**A28-16 | Severity: HIGH | `execute` — session attributes set with correct keys never asserted**
No test verifies that after a successful `execute` call the session contains:
- `"arrTimezone"` → non-null list
- `"arrLanguage"` → non-null list
- `"accountAction"` → exactly `"register"`

**A28-17 | Severity: MEDIUM | `execute` — forward result ("success") never asserted**
Same gap as A28-11; no test verifies the `ActionForward` returned.

---

### WelcomeAction

**A28-18 | Severity: CRITICAL | `execute` — zero test coverage for the entire method**
`execute` (lines 37-49) is the sole method and is completely untested. No mock of any collaborator (`SwitchLanguageAction` static methods, `AdvertismentDAO`, `HttpServletRequest`, `ActionMapping`) exists anywhere in the test suite.

**A28-19 | Severity: HIGH | `execute` — null locale stored in session not tested**
Lines 43-44: when a `ckLanguage` cookie exists, `SwitchLanguageAction.getLocale(cookie.getValue())` is called. As identified in A28-8, if `cookie.getValue()` is anything other than `"1"`-`"4"` (e.g., a corrupted cookie value, `"0"`, or an empty string), `getLocale` returns `null`. The returned `null` is then unconditionally stored into the session (`Globals.LOCALE_KEY`). No test covers this case or verifies that a null locale causes acceptable application behaviour vs. a downstream `NullPointerException` in Struts locale resolution.

**A28-20 | Severity: HIGH | `execute` — cookie-absent path not tested**
When no `ckLanguage` cookie is present (lines 40-45), the `if` block is skipped entirely and no locale is set in the session. The session locale state from a previous request or default Struts locale is left untouched. No test verifies this path or the resulting session state.

**A28-21 | Severity: HIGH | `execute` — `AdvertismentDAO.getAllAdvertisement()` exception path not tested**
`getAllAdvertisement()` throws `Exception` (propagated as `SQLException`) on DB failure. The action propagates the exception to Struts with no local handling. No test exercises this error path, and there is no verified fallback or error forward.

**A28-22 | Severity: HIGH | `execute` — `"sessAds"` session attribute not asserted**
No test verifies that `"sessAds"` is populated in the session after a successful execute, nor that its value is the list returned by the DAO.

**A28-23 | Severity: MEDIUM | `execute` — locale restored from cookie on every page load (no expiry guard) not tested**
Every request to `WelcomeAction` unconditionally re-reads the cookie and overwrites whatever locale is currently in the session. If the cookie holds a stale or invalid language code, the session locale is silently overwritten with `null` (see A28-19). No test covers this stateful interaction.

**A28-24 | Severity: MEDIUM | `execute` — forward result ("success") never asserted**
Same gap as A28-11 and A28-17.

---

## 4. Summary Table

| ID | Severity | Class | Method | Gap |
|----|----------|-------|--------|-----|
| A28-1 | CRITICAL | SwitchLanguageAction | `execute` | No tests exist |
| A28-2 | HIGH | SwitchLanguageAction | `execute` | Null `language` parameter defaults to `""` — untested |
| A28-3 | HIGH | SwitchLanguageAction | `execute` | Language `"0"` reset path (session locale + cookie clear) — untested |
| A28-4 | HIGH | SwitchLanguageAction | `execute` | Non-`"0"` with existing cookie — update path untested |
| A28-5 | HIGH | SwitchLanguageAction | `execute` | Non-`"0"` without existing cookie — create path untested |
| A28-6 | HIGH | SwitchLanguageAction | `execute` | `request.setAttribute("language", ...)` — untested |
| A28-7 | HIGH | SwitchLanguageAction | `getLocale` | All four locale-mapping branches untested |
| A28-8 | HIGH | SwitchLanguageAction | `getLocale` | Unrecognised input returns `null`; null stored into session — untested |
| A28-9 | HIGH | SwitchLanguageAction | `getCookie` | All three cookie-lookup paths untested |
| A28-10 | MEDIUM | SwitchLanguageAction | `getCookie` | Duplicate cookie names — first-match behaviour untested |
| A28-11 | MEDIUM | SwitchLanguageAction | `execute` | `findForward("success")` result never asserted |
| A28-12 | CRITICAL | SwitchRegisterAction | `execute` | No tests exist |
| A28-13 | CRITICAL | SwitchRegisterAction | `execute` | `getSession(false)` returns null when no session — NPE on setAttribute |
| A28-14 | HIGH | SwitchRegisterAction | `execute` | `TimezoneDAO` exception propagation — untested |
| A28-15 | HIGH | SwitchRegisterAction | `execute` | `LanguageDAO` exception / partial session state — untested |
| A28-16 | HIGH | SwitchRegisterAction | `execute` | Session attributes (`arrTimezone`, `arrLanguage`, `accountAction`) — never asserted |
| A28-17 | MEDIUM | SwitchRegisterAction | `execute` | `findForward("success")` result never asserted |
| A28-18 | CRITICAL | WelcomeAction | `execute` | No tests exist |
| A28-19 | HIGH | WelcomeAction | `execute` | Invalid cookie value yields `null` locale stored in session — untested |
| A28-20 | HIGH | WelcomeAction | `execute` | Cookie-absent path (no locale set) — untested |
| A28-21 | HIGH | WelcomeAction | `execute` | `AdvertismentDAO` exception propagation — untested |
| A28-22 | HIGH | WelcomeAction | `execute` | `"sessAds"` session attribute — never asserted |
| A28-23 | MEDIUM | WelcomeAction | `execute` | Stale cookie overwrites session locale on every load — untested |
| A28-24 | MEDIUM | WelcomeAction | `execute` | `findForward("success")` result never asserted |

**Totals:** 4 CRITICAL, 14 HIGH, 6 MEDIUM, 0 LOW, 0 INFO
**Overall line coverage for audited classes: 0%**
