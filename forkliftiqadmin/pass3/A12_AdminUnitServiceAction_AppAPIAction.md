# Pass 3 – Documentation Audit
**Agent:** A12
**Audit run:** 2026-02-26-01
**Files audited:**
- `action/AdminUnitServiceAction.java`
- `action/AppAPIAction.java`

---

## 1. Reading Evidence

### 1.1 AdminUnitServiceAction.java

| Element | Kind | Line |
|---|---|---|
| `AdminUnitServiceAction` | class (extends `Action`) | 17 |
| `log` | field `static Logger` | 19 |
| `execute` | public method | 21–68 |

**Method signatures:**

- `public ActionForward execute(ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response) throws Exception` — line 21

**Local variables of note inside `execute`:**
- `action` (String) — line 23
- `serviceForm` (AdminUnitServiceForm) — line 25
- `serviceBean` (ServiceBean) — line 32
- `serviceRemain` (double) — line 34
- `serviceStatus` (String) — line 42

---

### 1.2 AppAPIAction.java

| Element | Kind | Line |
|---|---|---|
| `AppAPIAction` | class (extends `Action`) | 38 |
| `log` | field `static Logger` | 40 |
| `execute` | public method | 42–373 |

**Method signatures:**

- `public ActionForward execute(ActionMapping mapping, ActionForm actionForm, HttpServletRequest request, HttpServletResponse response) throws Exception` — line 42

**Body:** Lines 45–371 consist entirely of commented-out code (using `////` prefix). The only active statement inside `execute` is `return mapping.findForward("apiXml");` at line 372.

---

## 2. Findings

### A12-1 — No class-level Javadoc: AdminUnitServiceAction
**File:** `action/AdminUnitServiceAction.java`, line 17
**Severity:** LOW
**Detail:** The class `AdminUnitServiceAction` has no Javadoc comment (`/** ... */`) immediately above its declaration. There is no description of the class's purpose, the Struts action it handles, or the form/DAO it coordinates.

---

### A12-2 — Undocumented non-trivial public method: AdminUnitServiceAction.execute
**File:** `action/AdminUnitServiceAction.java`, line 21
**Severity:** MEDIUM
**Detail:** `execute` is the sole public method and contains meaningful business logic: it reads an `action` request parameter, conditionally falls back to `serviceForm.getAction()`, computes a `serviceRemain` value using two distinct formulas depending on service type (`setIntval`/`setDur` vs. other), derives a `serviceStatus` string using threshold comparisons (< 5 h, < 25 h), populates a `ServiceBean`, persists it via `UnitDAO`, and forwards to `"success"`. No Javadoc exists for this method. Missing entirely:
- Description of what the method orchestrates
- `@param mapping` — the ActionMapping
- `@param actionForm` — the bound AdminUnitServiceForm
- `@param request` — the HTTP request (source of `action` parameter)
- `@param response` — the HTTP response
- `@return` — explanation of returned `ActionForward` (always `"success"`)
- `@throws Exception` — no documentation of what exceptions may propagate

---

### A12-3 — No class-level Javadoc: AppAPIAction
**File:** `action/AppAPIAction.java`, line 38
**Severity:** LOW
**Detail:** The class `AppAPIAction` has no Javadoc comment above its declaration. There is no description of the class's intent, which is to serve as an HTTP API entry point for the mobile/external app (evident from the commented-out body).

---

### A12-4 — Undocumented non-trivial public method: AppAPIAction.execute
**File:** `action/AppAPIAction.java`, line 42
**Severity:** MEDIUM
**Detail:** `execute` is the sole public method and is entirely undocumented. Although the entire business logic body is commented out (lines 45–371), the method still performs a non-trivial action: it unconditionally returns `mapping.findForward("apiXml")` — forwarding every request regardless of any parameter or authentication — making the effectively active logic non-obvious and potentially misleading to maintainers. No Javadoc exists for this method. Missing:
- `@param mapping`
- `@param actionForm`
- `@param request`
- `@param response`
- `@return` — should note that ALL requests are unconditionally forwarded to `"apiXml"`
- `@throws Exception`

---

### A12-5 — Dead / commented-out code constitutes entire method body: AppAPIAction.execute
**File:** `action/AppAPIAction.java`, lines 45–371
**Severity:** MEDIUM
**Detail:** Approximately 327 lines of logic — covering API actions for login, driver listing, vehicle listing, attachment listing, question retrieval, result submission, and PDF report delivery — are commented out using the `////` prefix. No explanatory comment, Javadoc, or TODO accompanies the dead code to explain:
- Why the code was disabled
- Whether it is safe to remove
- Whether it is intended to be re-enabled
- What the current state of the endpoint is (it accepts all requests and always returns `"apiXml"`)

This is a documentation gap that also constitutes a significant maintainability hazard. Maintainers examining the class cannot distinguish "temporarily disabled for a release" from "permanently abandoned." While not strictly a Javadoc deficiency, it is reported here as a documentation audit finding because the absence of explanatory commentary directly obscures intent. The severity is MEDIUM because the behaviour of the live endpoint (unconditional forward) differs materially from what the commented-out code implies.

---

### A12-6 — Misspelled local variable left in dead code: `resutl_id`
**File:** `action/AppAPIAction.java`, line 302 (commented-out block)
**Severity:** LOW
**Detail:** Inside the commented-out `API_RESULT` branch, the variable is named `resutl_id` (a transposition of "result"). This is in dead code and has no runtime impact, but it indicates the dead code was never reviewed or cleaned up, and if the block were ever reinstated, the typo would carry over. Noted as a documentation/quality hygiene finding.

---

## 3. Summary Table

| ID | File | Line | Severity | Description |
|---|---|---|---|---|
| A12-1 | AdminUnitServiceAction.java | 17 | LOW | No class-level Javadoc |
| A12-2 | AdminUnitServiceAction.java | 21 | MEDIUM | Undocumented non-trivial public method `execute`; no @param/@return/@throws |
| A12-3 | AppAPIAction.java | 38 | LOW | No class-level Javadoc |
| A12-4 | AppAPIAction.java | 42 | MEDIUM | Undocumented non-trivial public method `execute`; no @param/@return/@throws |
| A12-5 | AppAPIAction.java | 45–371 | MEDIUM | 327 lines of dead code with no explanation of why it was disabled or current endpoint state |
| A12-6 | AppAPIAction.java | 302 | LOW | Misspelled variable `resutl_id` in commented-out block |

**Total findings: 6**
- HIGH: 0
- MEDIUM: 3 (A12-2, A12-4, A12-5)
- LOW: 3 (A12-1, A12-3, A12-6)
