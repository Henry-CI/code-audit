# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A11
**Date:** 2026-02-26
**Scope:** AdminUnitEditAction, AdminUnitImpactAction

---

## 1. Source Files Examined

| # | File | Lines |
|---|------|-------|
| 1 | `src/main/java/com/action/AdminUnitEditAction.java` | 91 |
| 2 | `src/main/java/com/action/AdminUnitImpactAction.java` | 39 |

Supporting files read for context:
- `src/main/java/com/actionform/AdminUnitEditForm.java`
- `src/main/java/com/actionform/AdminUnitImpactForm.java`
- `src/main/java/com/dao/UnitDAO.java`
- `src/main/java/com/bean/ImpactBean.java`

---

## 2. Reading-Evidence Blocks

### 2.1 AdminUnitEditAction

**Class:** `com.action.AdminUnitEditAction extends org.apache.struts.action.Action`
**File:** `src/main/java/com/action/AdminUnitEditAction.java`

**Fields / Constants:**

| Name | Type | Line | Notes |
|------|------|------|-------|
| `unitDao` | `UnitDAO` (instance field) | 20 | Initialised via `UnitDAO.getInstance()` at field declaration; not injected — untestable without static mocking |

**Methods:**

| Method | Visibility | Return | Line | Throws |
|--------|-----------|--------|------|--------|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | `public` | `ActionForward` | 22–70 | `Exception` |
| `writeJsonResponse(HttpServletResponse, Boolean)` | `private` | `void` | 72–76 | `IOException` |
| `validate(String, AdminUnitEditForm, UnitBean)` | `private` | `String` | 78–90 | `Exception` |

**Branches inside `execute` (line 36–69):**

| Branch ID | Condition | Lines |
|-----------|-----------|-------|
| E-B1 | `opCode` non-empty AND equals `"unitnameexists"` (case-insensitive) | 36–39 |
| E-B2 | `opCode` non-empty AND equals `"serialnoexists"` (case-insensitive) | 40–43 |
| E-B3 | `opCode` non-empty AND equals `"macaddressexists"` (case-insensitive) | 44–47 |
| E-B4 (else) | All other `opCode` values (including null/empty) → full save path | 48–69 |
| E-B4a | Validation returns non-null → forward `"failure"` | 50–57 |
| E-B4b | `saveUnitInfo` returns `true` → forward `"success"` | 59–62 |
| E-B4c | `saveUnitInfo` returns `false` → forward `"globalfailure"` | 63–68 |

**Branches inside `validate` (line 79–89):**

| Branch ID | Condition | Lines |
|-----------|-----------|-------|
| V-B1 | `checkUnitByNm` returns `true` → return `"error.duplicateName"` | 79–80 |
| V-B2 | `checkUnitBySerial` returns `true` → return `"error.duplicateSerial"` | 82–83 |
| V-B3 | `macAddr` is not blank AND `checkUnitByMacAddr` returns `true` → return `"error.duplicateMacAddr"` | 85–87 |
| V-B4 | `macAddr` is blank → MAC check skipped | 86 |
| V-B5 | All checks pass → return `null` | 89 |

---

### 2.2 AdminUnitImpactAction

**Class:** `com.action.AdminUnitImpactAction extends org.apache.struts.action.Action`
**File:** `src/main/java/com/action/AdminUnitImpactAction.java`

**Fields / Constants:**

| Name | Type | Line | Notes |
|------|------|------|-------|
| `log` | `static Logger` | 18 | `InfoLogger.getLogger(...)` — private, not injectable |

**Methods:**

| Method | Visibility | Return | Line | Throws |
|--------|-----------|--------|------|--------|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | `public` | `ActionForward` | 20–38 | `Exception` |

**Branches inside `execute`:**

| Branch ID | Condition | Lines |
|-----------|-----------|-------|
| I-B1 | `request.getParameter("action")` is `null` → default to `""` | 21 |
| I-B2 | `request.getParameter("equipId")` is `null` → default to `""` | 22 |
| I-B3 | `action` is null or empty after parameter check → fall back to `impactForm.getAction()` | 26–28 |
| I-B4 | `action.equalsIgnoreCase("reset_calibration")` is `true` → call `resetCalibration`, forward `"success"` | 30–34 |
| I-B5 | Any other action value → forward `"success"` (else branch) | 35–37 |

**Logic defect noted (not a coverage gap, but evidence):**
Line 26: `if (action == null || action.equals(""))` — `action` can never be `null` at this point because line 21 already guarantees a non-null default of `""`. The `null` arm of this guard is dead code.

---

## 3. Test-Directory Coverage Confirmation

### 3.1 Existing test files (all 4)

| File | Package | Classes Under Test |
|------|---------|--------------------|
| `UnitCalibrationImpactFilterTest.java` | `com.calibration` | `UnitCalibrationImpactFilter` |
| `UnitCalibrationTest.java` | `com.calibration` | `UnitCalibration` |
| `UnitCalibratorTest.java` | `com.calibration` | `UnitCalibrator` |
| `ImpactUtilTest.java` | `com.util` | `ImpactUtil` |

### 3.2 Grep results — direct class-name references in test tree

```
Pattern: AdminUnitEditAction   → 0 matches
Pattern: AdminUnitImpactAction → 0 matches
Pattern: AdminUnitEditForm     → 0 matches
Pattern: AdminUnitImpactForm   → 0 matches
Pattern: UnitDAO               → 0 matches
Pattern: ManufactureDAO        → 0 matches
Pattern: ImpactBean            → 0 matches
Pattern: sessCompId / compId / equipId → 0 matches (none in test tree)
```

**Conclusion:** Zero direct or indirect test coverage exists for either action class or any collaborator they invoke.

---

## 4. Coverage Gap Findings

---

### AdminUnitEditAction

---

**A11-1 | Severity: CRITICAL | `execute` — entire method has zero test coverage**

`AdminUnitEditAction.execute` (lines 22–70) is completely untested. This is the primary controller method handling unit create/edit operations, including three AJAX JSON dispatch paths and a full save path with validation. No test exercises any branch, happy path, or error path.

---

**A11-2 | Severity: CRITICAL | Null session causes NullPointerException — untested**

Line 27: `request.getSession(false)` returns `null` when no session exists. Line 28 immediately dereferences the result via `session.getAttribute(...)`. If the session is absent (e.g., expired or the user is unauthenticated), a `NullPointerException` is thrown with no guard and no error message. No test covers the null-session path.

---

**A11-3 | Severity: CRITICAL | `compId` empty-string causes `NumberFormatException` — untested**

Line 28: when `session.getAttribute("sessCompId")` is `null`, `compId` is set to `""`. Line 30 then calls `Integer.parseInt(compId)`, which throws `NumberFormatException` for an empty string. This crash path is entirely uncovered.

---

**A11-4 | Severity: HIGH | AJAX branch E-B1 (`unitnameexists`) — untested**

The `opCode == "unitnameexists"` path (lines 36–39) calls `UnitDAO.getInstance().checkUnitByNm(...)`, writes a JSON boolean to the raw `HttpServletResponse`, and returns `null`. No test covers: (a) `exists = true`, (b) `exists = false`, (c) DAO exception propagation, or (d) the `return null` (bypassing Struts forward) contract.

---

**A11-5 | Severity: HIGH | AJAX branch E-B2 (`serialnoexists`) — untested**

The `opCode == "serialnoexists"` path (lines 40–43) is structurally identical to E-B1. Both the true and false outcomes of `checkUnitBySerial` and the `return null` contract are uncovered.

---

**A11-6 | Severity: HIGH | AJAX branch E-B3 (`macaddressexists`) — untested**

The `opCode == "macaddressexists"` path (lines 44–47) calls `checkUnitByMacAddr` with a `null` second argument (no unit ID exclusion in AJAX context). Both result outcomes and the `return null` contract are untested.

---

**A11-7 | Severity: HIGH | Validation failure path E-B4a — untested**

When `validate()` returns a non-null error key (lines 50–56), an `ActionErrors` is saved and `"failure"` is forwarded. No test verifies the error is stored correctly, the `arrAdminUnit` attribute is set on the request, or the `"failure"` forward is returned.

---

**A11-8 | Severity: HIGH | Save-success path E-B4b — untested**

When `saveUnitInfo` returns `true` (lines 59–62), the refreshed unit list is set on the request and `"success"` is forwarded. No test covers this happy path for either a new unit (INSERT) or an existing unit (UPDATE).

---

**A11-9 | Severity: HIGH | Save-failure path E-B4c — untested**

When `saveUnitInfo` returns `false` (lines 63–68), a global error message is stored and `"globalfailure"` is forwarded. This DAO-level failure path is entirely uncovered.

---

**A11-10 | Severity: HIGH | `validate` method — all branches untested**

`validate` (lines 78–90) is `private` but its logic is completely untested through any path:
- V-B1: duplicate name detected.
- V-B2: duplicate serial detected.
- V-B3: non-blank MAC address that is a duplicate.
- V-B4: blank MAC address — skip MAC check.
- V-B5: all validations pass — return `null`.

---

**A11-11 | Severity: HIGH | `writeJsonResponse` method — untested**

`writeJsonResponse` (lines 72–76) is called by all three AJAX branches. Its behaviour — obtaining a `PrintWriter`, writing the boolean string, flushing — and any `IOException` thrown by `response.getWriter()` are completely uncovered.

---

**A11-12 | Severity: HIGH | `UnitDAO` field not injectable — blocks unit testing**

`unitDao` (line 20) is initialised as `UnitDAO.getInstance()` at the field declaration site. `UnitDAO` is a singleton with a private constructor and no setter. There is no mechanism to inject a mock. Any unit test for `AdminUnitEditAction` must either use a static-mocking framework (e.g., PowerMock/Mockito inline) or refactor to constructor/setter injection. This is both a testability defect and a coverage blocker.

---

**A11-13 | Severity: MEDIUM | `ManufactureDAO.getInstance().getAllManufactures(compId)` called on every request — exception path untested**

Line 34 calls `ManufactureDAO.getInstance().getAllManufactures(compId)` before any opCode check, meaning it executes on every request including the three AJAX paths. A DAO exception here aborts the request entirely. No test exercises this failure, nor verifies that `arrManufacturers` is populated on successful calls.

---

**A11-14 | Severity: MEDIUM | Case-insensitive opCode matching edge cases — untested**

`opCode.equalsIgnoreCase(...)` is used for all three dispatch branches. Mixed-case variants (`"UnitNameExists"`, `"SERIALNOEXISTS"`, etc.) and opCode values that are neither known codes nor empty (fallthrough to save path) are untested. A value that almost matches (e.g., `"unitname_exists"`) silently falls through to the save path.

---

**A11-15 | Severity: MEDIUM | New unit (null `id`) vs. existing unit (non-null `id`) paths — untested**

`UnitDAO.saveUnitInfo` branches on `unitBean.getId() == null` to choose INSERT or UPDATE. Neither path is exercised through `AdminUnitEditAction`. The form's `getUnit(compId)` call at line 29 may produce a bean with a null or non-null id depending on form state, and neither scenario is tested.

---

**A11-16 | Severity: MEDIUM | `Integer.parseInt(compId)` on malformed compId — untested**

Line 30 calls `Integer.parseInt(compId)` without any format guard. If `sessCompId` holds a non-numeric string, a `NumberFormatException` is thrown. This is distinct from finding A11-3 (empty string) — here the session attribute exists but contains invalid data.

---

**A11-17 | Severity: LOW | `opCode` is non-empty but does not match any known code — silent fallthrough untested**

If `opCode` is set to an unrecognised non-empty string (e.g., `"unknown"`), all three `if`/`else if` branches are false and execution falls through to the save logic at E-B4. This behaviour is undocumented and untested.

---

**A11-18 | Severity: LOW | `StringUtils.isNotEmpty(opCode)` short-circuits on empty opCode — untested**

When `opCode` is empty (`""`), `StringUtils.isNotEmpty` returns `false` and the `equalsIgnoreCase` call is skipped for all three AJAX branches. This short-circuit path relies on `&&` lazy evaluation and is never explicitly tested.

---

### AdminUnitImpactAction

---

**A11-19 | Severity: CRITICAL | `execute` — entire method has zero test coverage**

`AdminUnitImpactAction.execute` (lines 20–38) is completely untested. No test exercises any code path including parameter extraction, the form fallback, the calibration reset branch, or the default forward.

---

**A11-20 | Severity: HIGH | `reset_calibration` path I-B4 — untested**

When `action` equals `"reset_calibration"` (case-insensitive), line 31 calls `Integer.parseInt(equipId)` and line 32 calls `UnitDAO.getInstance().resetCalibration(equip)`. No test covers: (a) successful calibration reset with a valid equipId, (b) `resetCalibration` throwing a `SQLException`, or (c) the resulting `ImpactBean` placed in request scope on line 33.

---

**A11-21 | Severity: HIGH | `Integer.parseInt(equipId)` on empty or malformed equipId — untested**

Line 31: if `action` is `"reset_calibration"` but `equipId` is `""` (the default from line 22 when the parameter is absent) or a non-numeric string, `Integer.parseInt(equipId)` throws `NumberFormatException`. This crash path is entirely uncovered.

---

**A11-22 | Severity: HIGH | Default/else path I-B5 — untested**

When `action` is any value other than `"reset_calibration"` (including `""`, `null` from form, or any unknown action string), the else branch at lines 35–37 is taken and `"success"` is forwarded without any state mutation. No test validates this path or confirms the absence of side-effects.

---

**A11-23 | Severity: MEDIUM | Form fallback I-B3 — untested**

Lines 26–28: when the `"action"` request parameter is absent (null/empty), `impactForm.getAction()` is used as the fallback. No test exercises the scenario where the action comes from the form rather than from the request parameter, nor whether the form value can itself be null.

---

**A11-24 | Severity: MEDIUM | Dead-code null check on `action` — untested and misleading**

Line 26: `if (action == null || action.equals(""))` — `action` is guaranteed non-null by line 21 (ternary assigns `""` when the parameter is null). The `action == null` arm is unreachable dead code. No test documents or asserts this, leaving future readers to reason about an impossible condition.

---

**A11-25 | Severity: MEDIUM | `UnitDAO.getInstance()` not injectable — blocks unit testing**

`AdminUnitImpactAction` calls `UnitDAO.getInstance().resetCalibration(equip)` inline on line 32. Like finding A11-12, there is no dependency-injection point for `UnitDAO`, preventing unit-level isolation of the action from the DAO.

---

**A11-26 | Severity: MEDIUM | `new ImpactBean()` placed in request scope — state not tested**

Line 33 creates a default `ImpactBean` (all-zero/default fields) and sets it as the `"impactBean"` request attribute. No test asserts that this attribute is present on the request, that it has the correct type, or that its fields are in the expected initial state after a calibration reset.

---

**A11-27 | Severity: LOW | Case-insensitive action matching edge cases — untested**

`action.equalsIgnoreCase("reset_calibration")` means `"RESET_CALIBRATION"`, `"Reset_Calibration"`, etc. all trigger the calibration path. Mixed-case variants are untested, and the contract (case-insensitive) is undocumented.

---

**A11-28 | Severity: LOW | `equipId` parameter ignored in else branch — untested**

When `action` is not `"reset_calibration"`, `equipId` is extracted (line 22) but never used. No test documents or asserts this no-op behaviour for the else path.

---

## 5. Coverage Summary

| Class | Methods | Methods with any test | Branch coverage | Line coverage |
|-------|---------|----------------------|-----------------|---------------|
| `AdminUnitEditAction` | 3 | 0 | 0 % | 0 % |
| `AdminUnitImpactAction` | 1 | 0 | 0 % | 0 % |
| **Combined** | **4** | **0** | **0 %** | **0 %** |

---

## 6. Finding Index

| ID | Severity | Summary |
|----|----------|---------|
| A11-1 | CRITICAL | `AdminUnitEditAction.execute` — zero test coverage |
| A11-2 | CRITICAL | Null session dereference → `NullPointerException` uncovered |
| A11-3 | CRITICAL | Empty `compId` → `Integer.parseInt("")` → `NumberFormatException` uncovered |
| A11-4 | HIGH | AJAX branch `unitnameexists` (E-B1) untested |
| A11-5 | HIGH | AJAX branch `serialnoexists` (E-B2) untested |
| A11-6 | HIGH | AJAX branch `macaddressexists` (E-B3) untested |
| A11-7 | HIGH | Validation failure path (E-B4a) — `"failure"` forward untested |
| A11-8 | HIGH | Save-success path (E-B4b) — `"success"` forward untested |
| A11-9 | HIGH | Save-failure path (E-B4c) — `"globalfailure"` forward untested |
| A11-10 | HIGH | `validate()` all five branches untested |
| A11-11 | HIGH | `writeJsonResponse()` untested including `IOException` path |
| A11-12 | HIGH | `unitDao` field not injectable — structural testability defect |
| A11-13 | MEDIUM | `ManufactureDAO.getAllManufactures` exception path and attribute population untested |
| A11-14 | MEDIUM | Case-insensitive `opCode` edge cases and unrecognised-code fallthrough untested |
| A11-15 | MEDIUM | New unit (INSERT) vs. existing unit (UPDATE) distinction untested |
| A11-16 | MEDIUM | Malformed `compId` (non-numeric) → `NumberFormatException` uncovered |
| A11-17 | LOW | Unrecognised non-empty `opCode` → silent fallthrough to save path untested |
| A11-18 | LOW | Empty `opCode` short-circuits all AJAX branches — untested explicitly |
| A11-19 | CRITICAL | `AdminUnitImpactAction.execute` — zero test coverage |
| A11-20 | HIGH | `reset_calibration` path (I-B4) — calibration reset and request attribute untested |
| A11-21 | HIGH | Empty/malformed `equipId` → `Integer.parseInt` crash in reset path uncovered |
| A11-22 | HIGH | Default else path (I-B5) — `"success"` forward without state change untested |
| A11-23 | MEDIUM | Form-fallback for `action` parameter (I-B3) untested |
| A11-24 | MEDIUM | Dead-code `action == null` guard — unreachable and undocumented |
| A11-25 | MEDIUM | `UnitDAO.getInstance()` not injectable in impact action — testability defect |
| A11-26 | MEDIUM | Default `ImpactBean` request attribute after reset not asserted in any test |
| A11-27 | LOW | Case-insensitive `reset_calibration` matching edge cases untested |
| A11-28 | LOW | `equipId` extracted but unused in else path — no test documents this |

---

*End of report — Agent A11, audit run 2026-02-26-01*
