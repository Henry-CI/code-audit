# Pass 3 Documentation Audit — A101
**Audit run:** 2026-02-26-01
**Agent:** A101
**Files audited:**
- `src/main/java/com/service/ReportService.java`
- `src/main/java/com/service/ReportServiceException.java`
- `src/main/java/com/service/RestClientService.java`

---

## 1. Reading Evidence

### 1.1 ReportService.java

**Class:** `ReportService` — line 14

**Fields:**

| Field | Type | Line |
|---|---|---|
| `resultDAO` | `ResultDAO` | 15 |
| `incidentReportDAO` | `IncidentReportDAO` | 16 |
| `impactReportDAO` | `ImpactReportDAO` | 17 |
| `theInstance` (static) | `ReportService` | 18 |

**Methods:**

| Method | Visibility | Line |
|---|---|---|
| `getInstance()` | `public static` | 20 |
| `ReportService()` (constructor) | `private` | 29 |
| `countPreOpsCompletedToday(Long compId, String timezone)` | `public` | 32 |
| `getPreOpsCheckReport(Long compId, PreOpsReportFilterBean filter, String dateFormat, String timezone)` | `public` | 41 |
| `getIncidentReport(int compId, IncidentReportFilterBean filter, String dateFormat, String timezone)` | `public` | 53 |
| `countImpactsToday(Long compId, String timezone)` | `public` | 65 |
| `getImpactReport(Long compId, ImpactReportFilterBean filter, String dateFormat, String timezone)` | `public` | 76 |
| `getSessionReport(int compId, SessionFilterBean filter, String dateFormat, String timezone)` | `public` | 90 |

---

### 1.2 ReportServiceException.java

**Class:** `ReportServiceException` — line 3 (extends `RuntimeException`)

**Methods:**

| Method | Visibility | Line |
|---|---|---|
| `ReportServiceException(String message)` | `public` | 4 |
| `ReportServiceException(String message, Throwable cause)` | `public` | 8 |

No instance fields beyond those inherited from `RuntimeException`.

---

### 1.3 RestClientService.java

**Class:** `RestClientService` — line 31

**Fields:**

| Field | Type | Line |
|---|---|---|
| `log` (static) | `Logger` | 33 |
| `COGNITO_API_PORT` (final) | `String` | 35 |

**Methods:**

| Method | Visibility | Line |
|---|---|---|
| `authenticationRequest(AuthenticationRequest authenticationRequest)` | `public` | 37 |
| `signUpRequest(UserSignUpRequest signUpRequest)` | `public` | 72 |
| `resetPassword(PasswordRequest resetPasswordRequest)` | `public` | 107 |
| `confirmResetPassword(PasswordRequest resetPasswordRequest)` | `public` | 142 |
| `getUser(String username, String accessToken)` | `public` | 177 |
| `getUserList(List<UserRequest> userRequestList, String accessToken)` | `public` | 213 |
| `updateUser(UserUpdateRequest userUpdateRequest)` | `public` | 250 |
| `deleteUser(String username, String sessionToken)` | `public` | 284 |

---

## 2. Findings

### A101-1 — LOW — ReportService: Missing class-level Javadoc

**File:** `ReportService.java`, line 14

No class-level `/** ... */` Javadoc block is present above the class declaration. The class is a singleton service that aggregates reporting queries across three DAOs (pre-ops results, incident reports, and impact reports). Its purpose, threading model, and singleton lifecycle are undocumented.

---

### A101-2 — MEDIUM — ReportService.getInstance(): Undocumented non-trivial public method

**File:** `ReportService.java`, lines 20–27

No Javadoc is present. The method implements a double-checked-locking singleton pattern, but the implementation is subtly broken: the `null` check on line 21 occurs outside the `synchronized` block while `theInstance` is not declared `volatile`. This means two threads could both observe `theInstance == null` and both enter the synchronized block, but only one creates the instance — the other is shut out after the first exits the lock, so a second instance is not created. However, without `volatile`, the first thread's write to `theInstance` may not be visible to the second thread due to JVM memory model reordering, and the non-synchronized read on line 21 is a data race. Regardless of the correctness concern, the method has no Javadoc, no `@return` tag, and the threading contract is undocumented.

---

### A101-3 — MEDIUM — ReportService.countPreOpsCompletedToday(): Undocumented non-trivial public method

**File:** `ReportService.java`, lines 32–39

No Javadoc block is present. The method delegates to `ResultDAO.countResultsCompletedToday()` and translates `SQLException` into `ReportServiceException`. Parameters `compId` and `timezone` have no description. The checked exception is not documented with `@throws`. Missing: `@param compId`, `@param timezone`, `@return`, `@throws ReportServiceException`.

---

### A101-4 — MEDIUM — ReportService.getPreOpsCheckReport(): Undocumented non-trivial public method

**File:** `ReportService.java`, lines 41–51

No Javadoc block is present. The method accepts a filter bean, date format string, and timezone string, delegates to the DAO, and wraps `SQLException`. All four parameters and the return type are undocumented. Missing: `@param compId`, `@param filter`, `@param dateFormat`, `@param timezone`, `@return`, `@throws ReportServiceException`.

---

### A101-5 — MEDIUM — ReportService.getIncidentReport(): Undocumented non-trivial public method

**File:** `ReportService.java`, lines 53–63

No Javadoc block is present. Note also that `compId` is typed as `int` (primitive) here while `countPreOpsCompletedToday` and `getImpactReport` use `Long` (boxed) — the inconsistency is undocumented and likely unintentional. Missing: `@param compId`, `@param filter`, `@param dateFormat`, `@param timezone`, `@return`, `@throws ReportServiceException`.

---

### A101-6 — MEDIUM — ReportService.countImpactsToday(): Undocumented non-trivial public method

**File:** `ReportService.java`, lines 65–74

No Javadoc block is present. The method includes a runtime `assert` enforcing a non-null `compId` precondition (line 67), which is a contract that should be documented. Missing: `@param compId`, `@param timezone`, `@return`, `@throws ReportServiceException`.

---

### A101-7 — MEDIUM — ReportService.getImpactReport(): Undocumented non-trivial public method

**File:** `ReportService.java`, lines 76–88

No Javadoc block is present. Like `countImpactsToday`, a non-null `assert` on `compId` (line 81) establishes a precondition that is invisible to callers. Missing: `@param compId`, `@param filter`, `@param dateFormat`, `@param timezone`, `@return`, `@throws ReportServiceException`.

---

### A101-8 — HIGH — ReportService.getSessionReport(): Inaccurate / dangerously wrong error message

**File:** `ReportService.java`, lines 90–99

No Javadoc is present (MEDIUM in its own right), but the more serious issue is that the exception message on line 97 reads:

```java
throw new ReportServiceException("Unable to get impact report for compId : " + compId, e);
```

This method retrieves a **session report**, not an impact report. The copy-paste error means any exception thrown here will surface a misleading diagnostic message ("Unable to get impact report") to callers and operators, making incident diagnosis significantly harder. This is dangerously inaccurate because it misdirects debugging effort to the wrong subsystem.

Additionally, `getSessionReport` declares no checked exception in its signature yet throws the unchecked `ReportServiceException`; the method signature gives callers no indication that failure is possible. Missing: class-level or method-level Javadoc, `@param` tags, `@return`, `@throws ReportServiceException`.

---

### A101-9 — LOW — ReportServiceException: Missing class-level Javadoc

**File:** `ReportServiceException.java`, line 3

No class-level `/** ... */` Javadoc block is present. The class purpose (unchecked wrapper for reporting-layer failures) is not documented.

---

### A101-10 — LOW — ReportServiceException constructors: Undocumented (trivial pass-through constructors)

**File:** `ReportServiceException.java`, lines 4–10

Both public constructors are trivial delegates to `RuntimeException` super-constructors. No Javadoc is present on either. Classified LOW as trivial pass-through constructors.

---

### A101-11 — LOW — RestClientService: Missing class-level Javadoc

**File:** `RestClientService.java`, line 31

No class-level Javadoc is present. The class wraps HTTP calls to a local Cognito authentication sidecar service on a hardcoded port (9090). The target service, authentication scheme, and error-handling strategy are undocumented at the class level.

---

### A101-12 — MEDIUM — RestClientService.authenticationRequest(): Undocumented non-trivial public method

**File:** `RestClientService.java`, lines 37–70

No Javadoc block is present. The method POSTs credentials to `/auth`, returns a default (empty) `AuthenticationResponse` on failure (silently swallowing exceptions), and logs but does not re-throw errors. The silent-failure contract is undocumented. Missing: `@param authenticationRequest`, `@return`.

---

### A101-13 — MEDIUM — RestClientService.signUpRequest(): Undocumented non-trivial public method

**File:** `RestClientService.java`, lines 72–105

No Javadoc block is present. POSTs to `/auth/SignUp`; returns a default empty response on failure without signalling the caller. Missing: `@param signUpRequest`, `@return`.

---

### A101-14 — MEDIUM — RestClientService.resetPassword(): Undocumented non-trivial public method

**File:** `RestClientService.java`, lines 107–140

No Javadoc block is present. POSTs to `/auth/ResetPassword`. Missing: `@param resetPasswordRequest`, `@return`.

---

### A101-15 — MEDIUM — RestClientService.confirmResetPassword(): Undocumented non-trivial public method

**File:** `RestClientService.java`, lines 142–175

No Javadoc block is present. POSTs to `/auth/ConfirmResetPassword`. The method is functionally identical to `resetPassword()` (same URL pattern, same parameter type, same response type) except for the endpoint path; the distinction is not documented. Missing: `@param resetPasswordRequest`, `@return`.

---

### A101-16 — MEDIUM — RestClientService.getUser(): Undocumented non-trivial public method; inaccurate log message

**File:** `RestClientService.java`, lines 177–211

No Javadoc block is present. The method performs a GET to `/auth/user` passing `username` and `accessToken` as raw query-string parameters (not URL-encoded) via string concatenation, which may silently produce a malformed URI for certain usernames. Additionally, the catch-block error log on line 207 reads:

```java
log.error("authenticationRequest error:"+ e.getMessage());
```

This message says `authenticationRequest` rather than `getUser`, which is a copy-paste inaccuracy that will mislead log analysis. Classified MEDIUM (inaccurate comment/log). Missing: `@param username`, `@param accessToken`, `@return`.

---

### A101-17 — MEDIUM — RestClientService.getUserList(): Undocumented non-trivial public method

**File:** `RestClientService.java`, lines 213–248

No Javadoc block is present. The method POSTs a list of `UserRequest` objects and returns a `List<UserResponse>`. On failure it returns an empty list with no indication to the caller that the request failed. Missing: `@param userRequestList`, `@param accessToken`, `@return`.

---

### A101-18 — MEDIUM — RestClientService.updateUser(): Undocumented non-trivial public method

**File:** `RestClientService.java`, lines 250–282

No Javadoc block is present. POSTs to `/auth/update`. Missing: `@param userUpdateRequest`, `@return`.

---

### A101-19 — MEDIUM — RestClientService.deleteUser(): Undocumented non-trivial public method

**File:** `RestClientService.java`, lines 284–309

No Javadoc block is present. The method issues a DELETE request to `/auth/delete_user`, passing `username` URL-encoded (line 297) and `sessionToken` as a raw query-string parameter. On any exception the method still returns the string `"Deleted"` (line 308), meaning callers have no way to distinguish a successful deletion from a failed one. This silent-success-on-failure contract is undocumented and dangerous but is a design issue rather than a documentation inaccuracy. The parameter name `sessionToken` is passed in the query parameter named `accessToken`, which is a naming mismatch undocumented for callers. Missing: `@param username`, `@param sessionToken`, `@return`.

---

## 3. Summary Table

| ID | Severity | File | Line(s) | Description |
|---|---|---|---|---|
| A101-1 | LOW | ReportService.java | 14 | Missing class-level Javadoc |
| A101-2 | MEDIUM | ReportService.java | 20–27 | `getInstance()` undocumented; broken double-checked locking (missing `volatile`) |
| A101-3 | MEDIUM | ReportService.java | 32–39 | `countPreOpsCompletedToday()` undocumented |
| A101-4 | MEDIUM | ReportService.java | 41–51 | `getPreOpsCheckReport()` undocumented |
| A101-5 | MEDIUM | ReportService.java | 53–63 | `getIncidentReport()` undocumented; inconsistent `int` vs `Long` compId type |
| A101-6 | MEDIUM | ReportService.java | 65–74 | `countImpactsToday()` undocumented; undocumented `assert` precondition |
| A101-7 | MEDIUM | ReportService.java | 76–88 | `getImpactReport()` undocumented; undocumented `assert` precondition |
| A101-8 | HIGH | ReportService.java | 90–99 | `getSessionReport()` exception message says "impact report" — dangerously wrong |
| A101-9 | LOW | ReportServiceException.java | 3 | Missing class-level Javadoc |
| A101-10 | LOW | ReportServiceException.java | 4–10 | Undocumented trivial constructors |
| A101-11 | LOW | RestClientService.java | 31 | Missing class-level Javadoc |
| A101-12 | MEDIUM | RestClientService.java | 37–70 | `authenticationRequest()` undocumented; silent-failure contract undocumented |
| A101-13 | MEDIUM | RestClientService.java | 72–105 | `signUpRequest()` undocumented |
| A101-14 | MEDIUM | RestClientService.java | 107–140 | `resetPassword()` undocumented |
| A101-15 | MEDIUM | RestClientService.java | 142–175 | `confirmResetPassword()` undocumented |
| A101-16 | MEDIUM | RestClientService.java | 177–211 | `getUser()` undocumented; log message names wrong method (`authenticationRequest`) |
| A101-17 | MEDIUM | RestClientService.java | 213–248 | `getUserList()` undocumented; silent-failure returns empty list |
| A101-18 | MEDIUM | RestClientService.java | 250–282 | `updateUser()` undocumented |
| A101-19 | MEDIUM | RestClientService.java | 284–309 | `deleteUser()` undocumented; always returns "Deleted" even on failure; `sessionToken` vs `accessToken` naming mismatch |

**Totals:** 1 HIGH, 13 MEDIUM, 5 LOW
