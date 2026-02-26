# Pass 2 — Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent:** A41
**Date:** 2026-02-26
**File under audit:** `src/main/java/com/actionservlet/PreFlightActionServlet.java`
**Test directory:** `src/test/java/`

---

## 1. Reading-Evidence Block

### Class

| Class | Extends | Line |
|-------|---------|------|
| `PreFlightActionServlet` | `ActionServlet` (Struts 1.x) | 22 |

### Fields / Constants

| Name | Type | Modifier | Value | Line |
|------|------|----------|-------|------|
| `serialVersionUID` | `long` | `private static final` | `-3552000667154242244L` | 27 |
| `log` | `Logger` | `private static` | `InfoLogger.getLogger("com.actionservlet.PreFlightActionServlet")` | 29 |

### Methods

| Method | Signature | Lines |
|--------|-----------|-------|
| `doGet` | `public void doGet(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException` | 36–86 |
| `doPost` | `public void doPost(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException` | 94–96 |
| `excludeFromFilter` | `private boolean excludeFromFilter(String path)` | 98–115 |

### Key Logic Landmarks Inside `doGet`

| Line(s) | Description |
|---------|-------------|
| 37–39 | Local variable declarations: `forward = false`, `stPath = ""`, `session = null` |
| 41 | `try` block opens |
| 45 | `session = req.getSession(false)` — no-create session retrieval |
| 46 | `path = req.getServletPath()` |
| 48 | `if (excludeFromFilter(path))` — gate entry condition |
| 51–54 | Branch: `session == null` → forward to `RuntimeConf.EXPIRE_PAGE` |
| 56–60 | Branch: `sessCompId == null` or `equals("")` → forward to `RuntimeConf.EXPIRE_PAGE` |
| 62–65 | MDC population if session and `sessCompId` non-null |
| 72 | `try` block closes |
| 73–76 | `catch(Exception e)` → forward to `RuntimeConf.ERROR_PAGE` |
| 78–81 | `if (forward)` → dispatcher forward |
| 82–85 | `else` → `super.doGet(req, res)` + MDC `remoteAddr` |

### `excludeFromFilter` — Exclusion List (Lines 100–114)

| Line | Suffix matched | Returns |
|------|---------------|---------|
| 100 | `welcome.do` | `false` |
| 101 | `adminWelcome.do` | `false` |
| 102 | `login.do` | `false` |
| 103 | `logout.do` | `false` |
| 104 | `expire.do` | `false` |
| 105 | `mailer.do` | `false` |
| 106 | `api.do` | `false` |
| 107 | `adminRegister.do` | `false` |
| 108 | `switchRegister.do` | `false` |
| 109 | `swithLanguage.do` | `false` |
| 110 | `resetpass.do` | `false` |
| 111 | `goResetPass.do` | `false` |
| 112 | `loadbarcode.do` | `false` |
| 113 | `uploadfile.do` | `false` |
| 114 | (all other paths) | `true` |

### External Constants Referenced

| Constant | Value | Source |
|----------|-------|--------|
| `RuntimeConf.EXPIRE_PAGE` | `"/expire.do"` | `RuntimeConf.java:10` |
| `RuntimeConf.ERROR_PAGE` | `"/globalfailure.do"` | `RuntimeConf.java:9` |

---

## 2. Test-Coverage Confirmation

**Test files found in `src/test/java/`:**

```
com/calibration/UnitCalibrationImpactFilterTest.java
com/calibration/UnitCalibrationTest.java
com/calibration/UnitCalibratorTest.java
com/util/ImpactUtilTest.java
```

**Grep result — pattern `PreFlightActionServlet|preflight|PreFlight` across all test files:**

```
No matches found
```

**Conclusion:** `PreFlightActionServlet` has zero test coverage — no direct tests, no indirect references, no mocks, no integration stubs.

---

## 3. Coverage Gap Analysis

The following seven mandated coverage areas are entirely untested. Each maps to a distinct execution path in the servlet.

---

### A41-1 | Severity: CRITICAL | Excluded-path list — no test that any listed suffix bypasses the session check

**Gap:** `excludeFromFilter()` returns `false` for 13 explicit suffixes (lines 100–113). No test verifies that a request to any of these paths does NOT enter the `if (excludeFromFilter(path))` branch. Equally, no test verifies that a path not in the list returns `true` and does enter the session check.

**Untested paths / assertions:**

- `GET /login.do` with `session == null` → `forward` must remain `false`, `super.doGet()` must be called.
- `GET /api.do` with `session == null` → same.
- `GET /someprotected.do` with `session == null` → `forward` must be `true`, dispatcher must forward to `EXPIRE_PAGE`.
- `GET /someprotected.do` with valid session → `forward` must be `false`, `super.doGet()` must be called.

**Why it matters:** If the exclusion list is changed (entries added or removed), there is no test harness that would catch an accidental exposure or accidental lock-out. This is the complete outer boundary of the authentication gate.

**Test cases needed:**

```
testExcludedPath_noSession_doesNotForward()       // login.do, api.do, etc. with null session
testExcludedPath_withSession_doesNotForward()     // same paths with valid session
testProtectedPath_noSession_forwardsToExpire()    // any non-excluded path, null session
testProtectedPath_validSession_callsSuperDoGet()  // non-excluded path, sessCompId set
```

---

### A41-2 | Severity: CRITICAL | endsWith() bypass — no test for path-suffix collision allowing unintended exclusion

**Gap:** The `endsWith()` comparisons in lines 100–113 match any path whose trailing characters equal the listed suffix — not just exact paths. A request for `/admin/fakelogin.do` satisfies `endsWith("login.do")` and is treated as public. No test exercises a crafted path that shares a suffix with an exclusion-list entry.

**Untested scenarios:**

- `GET /evil/fakelogin.do` → `excludeFromFilter` returns `false`; no session check; request falls through to `super.doGet()` even though `/evil/fakelogin.do` is not a legitimate public endpoint.
- `GET /x/fakeapi.do` → same for `api.do` suffix.

**Why it matters:** Pass 1 (finding in `PreFlightActionServlet_PreFlightReport.md`) rated the `endsWith` bypass CRITICAL. A test would have caught and documented this at development time. Without a test, any future refactor of the exclusion list cannot confirm the boundary is correct.

**Test cases needed:**

```
testEndsWith_suffixCollision_doesNotBypassAuth()
    // path = "/evil/fakelogin.do" → excludeFromFilter should NOT return false
    // (test currently fails, exposing the existing defect)
testEndsWith_exactMatchOnly_isExcluded()
    // path = "/login.do" → excluded
testEndsWith_paddedPrefix_isNotExcluded()
    // path = "/xlogin.do" → not excluded (different suffix boundary)
```

---

### A41-3 | Severity: HIGH | sessCompId null check — no test for null attribute on an existing session

**Gap:** Lines 56–60 check `session.getAttribute("sessCompId") == null`. No test creates a scenario where a session exists (`session != null`) but the `sessCompId` attribute has not been set (is `null`). This is the path a user reaches if their session was created (e.g., by a different action) but they never completed login.

**Untested branch:**

```java
else if (session.getAttribute("sessCompId") == null ...)  // line 56
{
    stPath = RuntimeConf.EXPIRE_PAGE;  // line 58
    forward = true;                    // line 59
}
```

**Test cases needed:**

```
testProtectedPath_sessionExistsButSessCompIdNull_forwardsToExpire()
    // session not null, sessCompId attribute absent → forward = true, stPath = EXPIRE_PAGE
```

---

### A41-4 | Severity: HIGH | Whitespace-only sessCompId — no test for blank but non-null attribute

**Gap:** Line 56 checks `session.getAttribute("sessCompId").equals("")` for an exact empty string. A `sessCompId` value of `"   "` (whitespace only) passes the check and is treated as a valid authenticated session. No test exercises this case.

**Untested branch:** The `else if` condition at line 56 evaluates to `false` when `sessCompId` is `"   "`, so `forward` remains `false` and `super.doGet()` is called — granting full authenticated access on a whitespace identity.

**Test cases needed:**

```
testProtectedPath_sessCompIdWhitespaceOnly_shouldForwardToExpire()
    // sessCompId = "   " → test currently passes auth check (existing defect)
    // test documents expected behaviour and captures regression if fixed
testProtectedPath_sessCompIdEmptyString_forwardsToExpire()
    // sessCompId = "" → forward = true (this branch is covered by code but has no test)
```

---

### A41-5 | Severity: HIGH | Exception-in-auth-check path — no test for catch block execution

**Gap:** Lines 73–76 catch any `Exception` thrown during the `try` block (lines 41–72) and set `forward = true`, `stPath = RuntimeConf.ERROR_PAGE` (`"/globalfailure.do"`). No test forces an exception during session attribute access to verify:

1. The catch block fires and sets the correct `stPath`.
2. The forward is to `ERROR_PAGE`, not `EXPIRE_PAGE`.
3. The exception is not silently swallowed without any observable outcome.

**Additional untested concern:** `ERROR_PAGE = "/globalfailure.do"` is itself a `.do` URL that re-enters the same servlet. A test should verify that forwarding to `globalfailure.do` does not cause a recursive forward loop — this requires an integration-level test with a real or simulated dispatcher.

**Test cases needed:**

```
testDoGet_exceptionDuringSessionCheck_forwardsToErrorPage()
    // mock session.getAttribute() to throw RuntimeException
    // assert stPath == ERROR_PAGE and forward == true

testDoGet_exceptionDuringSessionCheck_doesNotCallSuperDoGet()
    // same setup, verify super.doGet() is NOT called

testDoGet_errorPageForwardDoesNotLoop()
    // integration test: request to a path that triggers an exception
    // verify dispatcher is called exactly once, not recursively
```

---

### A41-6 | Severity: HIGH | session.getSession(false) returning null — no test for null-session on protected path

**Gap:** Line 45 calls `req.getSession(false)`, which returns `null` if no session exists. Lines 51–54 test `session == null` and set `forward = true` to `EXPIRE_PAGE`. While this path appears simple, it is the most frequently traversed path for unauthenticated requests and has no test.

**Untested scenarios:**

- Request to a protected path with no session at all → must forward to `EXPIRE_PAGE`.
- Request to a protected path with a `null`-returning `getSession(false)` → `MDC.put` at line 62 must NOT be called (the guard `session != null` protects it, but no test verifies the guard).
- The `remoteAddr` MDC call at line 84 must NOT be reached when `forward == true` (it is in the `else` branch, but no test verifies this).

**Test cases needed:**

```
testProtectedPath_noSession_forwardsToExpirePage()
    // req.getSession(false) returns null
    // assert forward = true, stPath = EXPIRE_PAGE

testProtectedPath_noSession_doesNotPopulateMDC()
    // req.getSession(false) returns null
    // assert MDC does not contain sessCompId after doGet()

testProtectedPath_noSession_doesNotCallSuperDoGet()
    // req.getSession(false) returns null
    // assert super.doGet() is NOT invoked
```

---

### A41-7 | Severity: HIGH | Redirect loop — no test that ERROR_PAGE forward re-enters doGet with null session

**Gap:** When an exception is caught (line 73), the servlet forwards to `RuntimeConf.ERROR_PAGE = "/globalfailure.do"`. The `globalfailure.do` path is not in the `excludeFromFilter` exclusion list, so on a Tomcat forward (which re-invokes the servlet) the second invocation enters the `if (excludeFromFilter(path))` branch. If the session is still null (which it will be for the original unauthenticated request that caused the exception), the second pass sets `forward = true` to `EXPIRE_PAGE`. That forward may or may not loop further depending on dispatcher behaviour.

No test exercises the forward-chain:

```
exception in auth → forward to /globalfailure.do → doGet re-invoked →
session null → forward to /expire.do → doGet re-invoked →
expire.do IS in exclusion list (returns false) → no auth check → super.doGet()
```

The intermediate step (`/globalfailure.do` triggering a second auth check) is entirely untested and represents the redirect loop risk.

**Test cases needed:**

```
testDoGet_errorPageForward_secondInvocationForwardsToExpire()
    // simulate RequestDispatcher.forward() calling doGet again with path=/globalfailure.do
    // and null session; assert second call forwards to EXPIRE_PAGE, not ERROR_PAGE again

testDoGet_expirePage_isInExclusionList()
    // unit test excludeFromFilter("/expire.do") == false
    // confirms the chain terminates at expire.do rather than looping

testDoGet_globalfailurePage_isNotInExclusionList()
    // unit test excludeFromFilter("/globalfailure.do") == true
    // confirms the second invocation DOES enter the session check
```

---

## 4. Summary Table

| Finding | Severity | Branch / Method | Lines | Gap Description |
|---------|----------|-----------------|-------|-----------------|
| A41-1 | CRITICAL | `excludeFromFilter()` / `doGet` | 48, 98–115 | No test verifies which paths are excluded vs. protected |
| A41-2 | CRITICAL | `excludeFromFilter()` | 100–113 | No test for suffix-collision bypass via `endsWith` |
| A41-3 | HIGH | `doGet` | 56–60 | No test: session exists, `sessCompId` attribute is null |
| A41-4 | HIGH | `doGet` | 56 | No test: `sessCompId` is whitespace-only, passes equals("") check |
| A41-5 | HIGH | `doGet` catch block | 73–76 | No test forces exception; catch-path behaviour unverified |
| A41-6 | HIGH | `doGet` | 45, 51–54 | No test: `getSession(false)` returns null on protected path |
| A41-7 | HIGH | `doGet` / dispatcher | 73–81 | No test for redirect loop: ERROR_PAGE re-enters auth gate with null session |

**Total gaps: 7**
**CRITICAL: 2 | HIGH: 5**

---

## 5. Coverage Metrics (Estimated)

| Metric | Value |
|--------|-------|
| Test classes referencing `PreFlightActionServlet` | 0 |
| Methods with any test coverage | 0 / 3 |
| Branches with any test coverage | 0 / 8 (estimated McCabe) |
| Lines with any test coverage | 0 / ~40 executable lines |
| Estimated line coverage | 0 % |
| Estimated branch coverage | 0 % |

The servlet is the application's sole authentication gate. It intercepts every request. Its branch coverage is 0 %. All seven coverage gaps identified above represent behavioural contracts that are entirely unverified by the test suite.
