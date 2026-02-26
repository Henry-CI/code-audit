# Pass 2 Test-Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A22
**Date:** 2026-02-26
**Files Audited:**
- `src/main/java/com/action/LoginAction.java`
- `src/main/java/com/action/LogoutAction.java`

---

## 1. Reading Evidence

### 1.1 LoginAction.java

**Class:** `com.action.LoginAction` (line 21)
- Declared `public final class LoginAction extends Action`
- Annotated `@Slf4j` (Lombok, line 20)
- No instance fields or constants defined within the class itself

**Methods:**

| Method | Modifier | Signature | Lines |
|--------|----------|-----------|-------|
| `execute` | `public` (Override) | `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 23–71 |
| `getLoggedInCompany` | `private static` | `getLoggedInCompany(List<CompanyBean>, Integer) : CompanyBean` | 73–80 |
| `loginFailure` | `private` | `loginFailure(ActionMapping, HttpServletRequest) : ActionForward` | 82–88 |

**Key logic flow within `execute` (lines 23–71):**
- Line 28: `request.getSession(false)` — obtains existing session (no creation)
- Lines 31–33: Pre-authentication session writes: `sessAds`, `arrTimezone`, `arrLanguage`
- Line 35: Pre-authentication session write: `username` stored before auth succeeds
- Lines 38–43: Builds `AuthenticationRequest`, calls `RestClientService.authenticationRequest()`
- Line 44: Extracts `sessionToken` from `AuthenticationResponse`
- Lines 47–49: Null check on `sessionToken` — returns `loginFailure` forward
- Line 51: Session write: `sessionToken`
- Lines 53–54: `LoginDAO.getCompanyId()` and `LoginDAO.getUserId()` (both throw `SQLException`)
- Lines 56–57: `LoginDAO.isUserAuthority()` and `LoginDAO.isAuthority()` (both throw `Exception`)
- Lines 58–59: Session writes: `isSuperAdmin`, `isDealerLogin`
- Line 60: `LoginDAO.getCompanies()` (throws `SQLException`)
- Lines 62–64: Empty companies guard — returns `loginFailure` forward
- Lines 65–68: Session writes: `sessAccountId`, `sessUserId`; call to `CompanySessionSwitcher.UpdateCompanySessionAttributes()`
- Lines 69–70: Request attribute set; returns `"successAdmin"` forward

**Key logic flow within `getLoggedInCompany` (lines 73–80):**
- Line 74: Null guard on `loggedInCompanyId` — returns `companies.get(0)` if null
- Lines 76–78: Linear scan for matching company by ID (String/Integer comparison via `String.valueOf`)
- Line 79: Falls back to `companies.get(0)` if no match found

**Key logic flow within `loginFailure` (lines 82–88):**
- Creates `ActionErrors`, adds `"error.login"` message, calls `saveErrors()`, returns `"failure"` forward

---

### 1.2 LogoutAction.java

**Class:** `com.action.LogoutAction` (line 28)
- Declared `public class LogoutAction extends Action`

**Fields:**

| Field | Type | Line |
|-------|------|------|
| `log` | `private static Logger` (log4j) | 30 |

**Methods:**

| Method | Modifier | Signature | Lines |
|--------|----------|-----------|-------|
| `execute` | `public` (Override) | `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse) throws Exception` | 32–50 |

**Key logic flow within `execute` (lines 32–50):**
- Line 36: `request.getSession(false)` — obtains existing session (no creation)
- Lines 37–48: `if (theSession != null)` guard block:
  - Line 39: `theSession.invalidate()` — destroys session
  - Lines 40–45: Reads `ckLanguage` cookie via `SwitchLanguageAction.getCookie()`; if present, calls `SwitchLanguageAction.getLocale()` and writes locale to the **new** session (`request.getSession()` implicitly creates a new session post-invalidation)
  - Line 47: Writes `sessAds` to the new session
- Line 49: Always returns `"logout"` forward (even when `theSession == null`)

---

## 2. Test Coverage Grep Results

**Test directory searched:** `src/test/java/`

**Existing test files (4 total):**
1. `com/calibration/UnitCalibrationImpactFilterTest.java`
2. `com/calibration/UnitCalibrationTest.java`
3. `com/calibration/UnitCalibratorTest.java`
4. `com/util/ImpactUtilTest.java`

**Grep for `LoginAction`, `LogoutAction`, `loginFailure`, `getLoggedInCompany`:** No matches found.

**Conclusion:** Zero test coverage — direct or indirect — for either `LoginAction` or `LogoutAction`.

---

## 3. Coverage Gap Findings

### LoginAction Findings

---

**A22-1 | Severity: CRITICAL | No tests exist for LoginAction — zero coverage of the authentication entry point**

`LoginAction.execute()` is the sole authentication gate for the entire admin application. There are no unit tests, integration tests, or mock-based tests of any kind. Every path through login (success, Cognito failure, empty companies, null session) is completely untested.

---

**A22-2 | Severity: CRITICAL | NullPointerException if `request.getSession(false)` returns null**

Line 28: `HttpSession session = request.getSession(false);`
Line 31: `session.setAttribute("sessAds", ...);`

`getSession(false)` returns `null` when no session exists. The result is immediately dereferenced at line 31 without a null check. If a request arrives with no pre-existing session (e.g., direct POST to the login endpoint with no prior request, expired session, or container session store miss), this throws `NullPointerException` and the exception propagates uncaught from `execute()`. No test exercises the no-session path.

---

**A22-3 | Severity: CRITICAL | Username written to session before authentication succeeds (pre-auth data leak)**

Line 35: `session.setAttribute("username", loginActionForm.getUsername());`

The username is stored in the session before the Cognito authentication call (lines 38–43) and before the `sessionToken` null-check (line 47). If authentication fails and `loginFailure` is returned, the `username` attribute persists in the session. An attacker who can observe session state (e.g., via session fixation, shared session store, or server-side session inspection) can enumerate valid usernames by probing for the presence of this attribute after a failed login. No test verifies session state after a failed authentication.

---

**A22-4 | Severity: CRITICAL | Cognito service exception swallowed — `authResponse` can be non-null with null `sessionToken`, bypassing intent but not guarded against NPE on response fields**

In `RestClientService.authenticationRequest()` (lines 51–68 of RestClientService.java), all exceptions are caught and `e.printStackTrace()` is called, after which a default empty `AuthenticationResponse` (constructed at line 50 of RestClientService) is returned. The `AuthenticationResponse` default constructor (Lombok `@NoArgsConstructor`) produces an object where all fields including `sessionToken` are `null`.

`LoginAction` line 44: `String sessionToken = authResponse.getSessionToken();`

This is safe only if `authResponse` itself is non-null, which it always is (the catch block returns the pre-allocated empty response). However:
- The Cognito connectivity failure is silently swallowed — no error is surfaced to the operator log in `LoginAction`; `loginFailure` is returned with the generic `"error.login"` message, giving the user no diagnostic indication of a Cognito outage vs. bad credentials.
- No test covers the Cognito-down path to verify that the failure forward is correctly returned and no session corruption occurs.

---

**A22-5 | Severity: CRITICAL | `authResponse` itself could be null if `RestClientService` is subclassed or mocked improperly — NPE at line 44**

Line 43: `AuthenticationResponse authResponse = restClientServce.authenticationRequest(...);`
Line 44: `String sessionToken = authResponse.getSessionToken();`

There is no null check on `authResponse`. While the current production implementation of `RestClientService.authenticationRequest()` never returns null (it returns an empty response object on exception), the absence of a null guard makes the code fragile: any future change to `RestClientService`, any subclass, or any test mock that returns null will produce an unguarded NPE. No test exercises this path.

---

**A22-6 | Severity: HIGH | `LoginDAO.getCompanyId()` returns `0` (via `orElse(0)`) for unknown users — this zero is treated as a valid company ID**

Line 53: `Integer loggedInCompanyId = LoginDAO.getCompanyId(loginActionForm.getUsername());`
`LoginDAO.getCompanyId()` returns `orElse(0)` when the user is not found in the database (line 37 of LoginDAO.java). A return of `0` is then passed to `LoginDAO.isAuthority()` (line 57), `LoginDAO.getCompanies()` (line 60), and ultimately `getLoggedInCompany()` (line 67).

An authenticated Cognito user whose username does not exist in the local `v_cognitousers` view will receive `companyId = 0`. `LoginDAO.getCompanies()` line 106 returns an empty list when `company == null`, but `0` is not null — it is a valid Integer. `getSimpleCompanies(0)` will execute a SQL query for company ID `0`, likely returning an empty list, which then triggers `loginFailure` at line 63. However, `isSuperAdmin` (line 56) is evaluated against `loggedUserId` which similarly defaults to `0` — a user ID `0` could match database records unintentionally. No test covers the "user not in DB" path.

---

**A22-7 | Severity: HIGH | `LoginDAO.getUserId()` returns `0` for unknown users — zero user ID stored in session as `sessUserId`**

Line 54: `int loggedUserId = LoginDAO.getUserId(loginActionForm.getUsername());`

If the username is not found, `getUserId()` returns `orElse(0)` (LoginDAO.java line 43). This `0` is stored at line 66 as `session.setAttribute("sessUserId", 0)` only if `companies` is non-empty. More critically, it is passed to `LoginDAO.isUserAuthority(0, ROLE_SYSADMIN)` at line 56. If any database record has `id = 0` with `authority = 'ROLE_SYS_ADMIN'`, an unrecognised user would be granted superadmin. No test covers the unknown-user path or asserts that `isSuperAdmin` is false for an unknown user.

---

**A22-8 | Severity: HIGH | `getLoggedInCompany()` called when `companies` is non-empty but `loggedInCompanyId` does not match any entry — silently falls back to `companies.get(0)`**

Lines 73–80: If `loggedInCompanyId` is non-null but does not match any `CompanyBean.getId()` in the list (note: `CompanyBean.getId()` returns a `String`, compared via `String.valueOf(loggedInCompanyId)`), the method silently returns the first company in the list. This means a user could be logged into a company context they do not belong to. No test asserts which company is selected in the no-match case.

---

**A22-9 | Severity: HIGH | Company ID comparison uses `String.valueOf(Integer)` vs `CompanyBean.getId()` (String) — type mismatch risk**

Line 77: `company.getId().equals(String.valueOf(loggedInCompanyId))`

`loggedInCompanyId` is an `Integer` returned by `LoginDAO.getCompanyId()`. `String.valueOf(0)` produces `"0"`. If the database stores company IDs as non-zero-padded strings (e.g., `"1"`, `"2"`), this works. However, if any leading/trailing whitespace, padding, or encoding difference exists between the DB-sourced string and the integer-converted string, the comparison silently fails, causing the fallback to `companies.get(0)`. No test verifies the comparison logic with various ID formats.

---

**A22-10 | Severity: HIGH | All checked exceptions from DAO calls propagate unhandled — execute() declares `throws Exception`**

Lines 53–60: `LoginDAO.getCompanyId()`, `LoginDAO.getUserId()`, `LoginDAO.isUserAuthority()`, `LoginDAO.isAuthority()`, `LoginDAO.getCompanies()` all throw `SQLException` or `Exception`. `LoginAction.execute()` declares `throws Exception` and does not catch any of these. A database failure mid-login will propagate as an unhandled exception to Struts, which will route to the global error page (`/globalfailure.do`) without any `loginFailure` error handling, and session attributes set before the exception point (including `username` and possibly `sessionToken`) will remain in the session. No test verifies DAO exception propagation behavior.

---

**A22-11 | Severity: HIGH | `CompanySessionSwitcher.UpdateCompanySessionAttributes()` is called without any guard — throws `Exception` through `execute()`**

Line 68: `CompanySessionSwitcher.UpdateCompanySessionAttributes(loggedInCompany, request, session)`

This method (CompanySessionSwitcher.java lines 17–46) performs database queries (`TimezoneDAO.getTimezone()`, `UnitDAO.getUnitNameByComp()`, `DriverDAO.getTotalDriverByID()`, `ReportService.countPreOpsCompletedToday()`, `DriverDAO.getExpiringTrainings()`, `ReportService.countImpactsToday()`, `CompanyDAO.getCompanyByCompId()`) and calls `Integer.parseInt(timezone)` which throws `NumberFormatException` if `company.getTimezone()` is null or non-numeric. The session token has already been committed to the session at this point; a failure here leaves a partially initialised session. No test covers this path.

---

**A22-12 | Severity: MEDIUM | Pre-authentication session attributes (`sessAds`, `arrTimezone`, `arrLanguage`) loaded before Cognito call — wasted DB queries on auth failure**

Lines 31–33: Three DAO calls (`AdvertismentDAO.getInstance().getAllAdvertisement()`, `TimezoneDAO.getInstance().getAllTimezone()`, `LanguageDAO.getInstance().getAllLan()`) are executed unconditionally before any credential validation. If the Cognito service is unavailable or credentials are wrong, these queries execute unnecessarily. Additionally, these DAO calls themselves can throw exceptions, which would prevent the login page from ever being reached even when the credentials are irrelevant. No test asserts loading order or verifies that a DAO failure in the pre-auth block is handled gracefully.

---

**A22-13 | Severity: MEDIUM | Successful `loginFailure` path not tested — no assertion that `ActionErrors` is populated correctly**

`loginFailure()` (lines 82–88) is invoked in two scenarios: null `sessionToken` (line 48) and empty companies list (line 63). No test verifies that calling `loginFailure` results in the `"failure"` forward being returned, that `ActionErrors` contains exactly one entry with key `"loginError"` and message key `"error.login"`, or that `saveErrors()` is called with the correct request.

---

**A22-14 | Severity: MEDIUM | No test for the successful login path — session attribute completeness unverified**

The happy path sets the following session attributes: `sessAds`, `arrTimezone`, `arrLanguage`, `username`, `sessionToken`, `isSuperAdmin`, `isDealerLogin`, `sessArrComp`, `sessAccountId`, `sessUserId`, plus all attributes set by `CompanySessionSwitcher`. No test asserts that all required attributes are present and correctly typed after a successful login, making it impossible to detect regressions where an attribute is accidentally omitted or set to the wrong value.

---

**A22-15 | Severity: MEDIUM | No test for `isSuperAdmin = true` login path**

When `LoginDAO.isUserAuthority()` returns `true`, `LoginDAO.getCompanies()` delegates to `getSuperAdminCompanies()` (LoginDAO.java line 105). The resulting `companies` list may have a different structure (interleaved dealer and subcompany entries). No test verifies that a superadmin login proceeds to `"successAdmin"` and that session attributes are correctly populated for the superadmin role.

---

**A22-16 | Severity: MEDIUM | No test for `isDealerLogin = true` login path**

When `isDealerLogin` is true, `LoginDAO.getCompanies()` delegates to `getDealerCompanies()`. No test verifies the dealer login path or that session attributes correctly reflect dealer status.

---

**A22-17 | Severity: LOW | `request.getSession(false)` never returns null in practice during a Struts form submission (container creates session for form binding) — but the code assumes a pre-existing session with no defensive check**

Struts typically creates a session before `execute()` is called (for `ActionForm` binding). However, relying on this container behavior is an implicit coupling; the code at line 28 uses `getSession(false)` which explicitly signals intent to not create a session, but the very next line dereferences the result. No test documents or validates this container-coupling assumption.

---

### LogoutAction Findings

---

**A22-18 | Severity: CRITICAL | No tests exist for LogoutAction — zero coverage of the logout and session destruction path**

`LogoutAction.execute()` is the sole session invalidation mechanism. No unit or integration tests verify any aspect of logout behavior, including session destruction, cookie handling, or the `"logout"` forward.

---

**A22-19 | Severity: CRITICAL | New session created implicitly after `invalidate()` — sensitive session data may be set on an unauthenticated new session**

Line 39: `theSession.invalidate();`
Line 44: `request.getSession().setAttribute(Globals.LOCALE_KEY, locale);`
Line 47: `request.getSession().setAttribute("sessAds", ...);`

After `invalidate()`, `request.getSession()` (without `false`) creates a **new** session. The locale from the `ckLanguage` cookie and the advertisements from `AdvertismentDAO` are written to this new unauthenticated session. This is a session fixation vector: an attacker who can predict or inject the `ckLanguage` cookie value and then triggers a logout can cause the application to create a new session with attacker-controlled locale state before the victim's next login. No test verifies whether any attributes should or should not be present in the post-logout session.

---

**A22-20 | Severity: CRITICAL | Cross-class dependency in logout: `SwitchLanguageAction.getCookie()` and `SwitchLanguageAction.getLocale()` are static methods of an action class called from another action — tight coupling prevents isolated testing**

Lines 40–44 of LogoutAction invoke `SwitchLanguageAction.getCookie()` and `SwitchLanguageAction.getLocale()`. These are static methods on a Struts `Action` subclass, creating a static dependency that cannot be mocked or stubbed in unit tests without bytecode manipulation (e.g., PowerMock). No test covers this cross-action call path, and the coupling makes the logout logic inherently difficult to test in isolation.

---

**A22-21 | Severity: HIGH | `SwitchLanguageAction.getLocale()` can return `null` for unrecognised cookie values — null locale written to session**

`SwitchLanguageAction.getLocale()` (lines 83–109 of SwitchLanguageAction.java) returns `null` if the cookie value does not match `"1"`, `"2"`, `"3"`, or `"4"`. LogoutAction line 44 writes this potentially null `Locale` directly to the session attribute `Globals.LOCALE_KEY`. Struts and JSP tag libraries that subsequently read `Globals.LOCALE_KEY` expecting a non-null `Locale` may throw `NullPointerException` on the next request. No test covers the unrecognised cookie value path.

---

**A22-22 | Severity: HIGH | `AdvertismentDAO.getInstance().getAllAdvertisement()` called unconditionally on every logout — exception propagates unhandled**

Line 47: `request.getSession().setAttribute("sessAds", AdvertismentDAO.getInstance().getAllAdvertisement());`

If `getAllAdvertisement()` throws an exception (database unavailable, connection pool exhausted), the exception propagates from `execute()` and the `"logout"` forward is never returned. The original session has already been invalidated at line 39, so the user is in an indeterminate state: their session is gone but they have not been redirected to the logout page. No test covers the DAO exception path during logout.

---

**A22-23 | Severity: HIGH | Logout forward returned unconditionally even when `theSession == null` — no distinction between "already logged out" and "active session logout"**

Line 49 is outside the `if (theSession != null)` block, so `"logout"` is always returned regardless of whether a session existed. If a user hits the logout URL without an active session (double-logout, expired session, direct URL access), the code returns the logout forward without performing any session cleanup or error indication. No test asserts behavior for the null-session case.

---

**A22-24 | Severity: MEDIUM | No test verifies that `theSession.invalidate()` is actually called — a regression could remove invalidation silently**

The sole security guarantee of `LogoutAction` is `theSession.invalidate()` at line 39. No test mocks the `HttpSession` and asserts that `invalidate()` is called exactly once on a logout request with an active session. A future refactor that accidentally removes or conditions this call would be undetectable.

---

**A22-25 | Severity: MEDIUM | No test verifies the `"logout"` ActionForward is returned**

`mapping.findForward("logout")` at line 49 relies on the `struts-config.xml` forward named `"logout"` being correctly configured. No test verifies that the correct `ActionForward` is returned (forward name, path, redirect flag). A misconfiguration would cause all logout attempts to fail silently or route to an unexpected destination.

---

**A22-26 | Severity: MEDIUM | Cookie null-check before locale write means locale is NOT reset if no `ckLanguage` cookie exists — Struts locale from previous session may persist in some container configurations**

Lines 41–45: If `cookie == null`, neither `Globals.LOCALE_KEY` nor any other locale attribute is set on the new post-invalidation session. Depending on the servlet container's session attribute inheritance behavior, a stale locale from a previous session could theoretically persist. No test verifies locale state in the new session when no cookie is present.

---

**A22-27 | Severity: LOW | `LogoutAction` uses log4j (`org.apache.log4j.Logger`) while `LoginAction` uses SLF4J via Lombok `@Slf4j` — inconsistent logging frameworks across adjacent action classes**

`LogoutAction` line 30: `private static Logger log = InfoLogger.getLogger("com.action.LogoutAction");` (log4j)
`LoginAction` line 20: `@Slf4j` (SLF4J via Lombok)

This inconsistency is not a security issue but is an indicator of organic code growth without a coding standard. Mixing logging frameworks can cause log output to be routed differently depending on the container configuration. No test catches this inconsistency.

---

**A22-28 | Severity: LOW | `LogoutAction` is not declared `final` while `LoginAction` is — subclassability of a security-critical action class**

`LoginAction` (line 21): `public final class LoginAction`
`LogoutAction` (line 28): `public class LogoutAction`

Leaving a security-sensitive action class open to subclassing creates a risk that a future developer could override `execute()` in a subclass and bypass logout logic. The `final` modifier on `LoginAction` is a correct defensive choice; `LogoutAction` should be treated the same way. No test or static analysis check enforces this constraint.

---

## 4. Summary Table

| Finding | Severity | Class | Description |
|---------|----------|-------|-------------|
| A22-1 | CRITICAL | LoginAction | Zero test coverage for authentication entry point |
| A22-2 | CRITICAL | LoginAction | NPE when `getSession(false)` returns null — no null guard before first `setAttribute` |
| A22-3 | CRITICAL | LoginAction | Username written to session before authentication — pre-auth session data leak |
| A22-4 | CRITICAL | LoginAction | Cognito exception silently swallowed in `RestClientService` — failure indistinguishable from wrong credentials |
| A22-5 | CRITICAL | LoginAction | No null guard on `authResponse` — future NPE risk at `authResponse.getSessionToken()` |
| A22-6 | HIGH | LoginAction | `getCompanyId()` returns `0` for unknown user — zero treated as valid company ID |
| A22-7 | HIGH | LoginAction | `getUserId()` returns `0` for unknown user — zero user ID could match privileged DB records |
| A22-8 | HIGH | LoginAction | `getLoggedInCompany()` silently falls back to `companies.get(0)` on ID mismatch |
| A22-9 | HIGH | LoginAction | Integer-to-String ID comparison in `getLoggedInCompany()` — silent mismatch risk |
| A22-10 | HIGH | LoginAction | DAO `SQLException`/`Exception` propagate unhandled through `execute()` — partial session state left behind |
| A22-11 | HIGH | LoginAction | `CompanySessionSwitcher.UpdateCompanySessionAttributes()` throws unhandled — partial session after token commit |
| A22-12 | MEDIUM | LoginAction | Pre-auth DAO queries execute before credential validation — wasted work and early failure path untested |
| A22-13 | MEDIUM | LoginAction | `loginFailure()` paths not tested — `ActionErrors` population unverified |
| A22-14 | MEDIUM | LoginAction | Successful login path not tested — session attribute completeness unverified |
| A22-15 | MEDIUM | LoginAction | SuperAdmin login path (`isSuperAdmin = true`) not tested |
| A22-16 | MEDIUM | LoginAction | Dealer login path (`isDealerLogin = true`) not tested |
| A22-17 | LOW | LoginAction | Implicit assumption that container provides a pre-existing session — `getSession(false)` usage not validated by tests |
| A22-18 | CRITICAL | LogoutAction | Zero test coverage for session destruction path |
| A22-19 | CRITICAL | LogoutAction | Post-`invalidate()` implicit session creation writes attacker-influenced state to new session |
| A22-20 | CRITICAL | LogoutAction | Static cross-action dependency (`SwitchLanguageAction`) prevents isolated unit testing |
| A22-21 | HIGH | LogoutAction | `getLocale()` returns null for unrecognised cookie values — null locale written to session |
| A22-22 | HIGH | LogoutAction | `AdvertismentDAO` call on logout throws unhandled — session invalidated but logout forward never returned |
| A22-23 | HIGH | LogoutAction | `"logout"` forward returned even when no session exists — null-session path behavior unverified |
| A22-24 | MEDIUM | LogoutAction | No test asserts `session.invalidate()` is called — regression risk for core security guarantee |
| A22-25 | MEDIUM | LogoutAction | No test verifies `"logout"` forward is returned correctly |
| A22-26 | MEDIUM | LogoutAction | No locale reset when no cookie present — stale locale state possible in new session |
| A22-27 | LOW | LogoutAction | Inconsistent logging framework (log4j vs SLF4J) between adjacent action classes |
| A22-28 | LOW | LogoutAction | `LogoutAction` not declared `final` — security-sensitive class open to subclassing |

**Totals:** 6 CRITICAL | 9 HIGH | 8 MEDIUM | 3 LOW | 0 INFO
**Overall test coverage for audited files:** 0%
