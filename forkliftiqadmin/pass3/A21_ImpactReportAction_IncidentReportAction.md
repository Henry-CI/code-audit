# Pass 3 Documentation Audit — A21
**Audit run:** 2026-02-26-01
**Agent:** A21
**Files:**
- `src/main/java/com/action/ImpactReportAction.java`
- `src/main/java/com/action/IncidentReportAction.java`

---

## 1. Reading Evidence

### 1.1 ImpactReportAction.java

**Class:** `ImpactReportAction` — line 17
Extends: `org.apache.struts.action.Action`

**Fields:**

| Name | Type | Line |
|---|---|---|
| `reportService` | `ReportService` | 19 |
| `manufactureDAO` | `ManufactureDAO` | 20 |
| `unitDAO` | `UnitDAO` | 21 |

**Methods:**

| Method | Visibility | Line |
|---|---|---|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | `public` (override) | 24 |

---

### 1.2 IncidentReportAction.java

**Class:** `IncidentReportAction` — line 17
Extends: `org.apache.struts.action.Action`

**Fields:** None declared (no instance fields; DAO and service are accessed via static calls inside `execute`).

**Methods:**

| Method | Visibility | Line |
|---|---|---|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | `public` (override) | 20 |

---

## 2. Findings

### A21-1 — LOW — No class-level Javadoc: `ImpactReportAction`

**File:** `ImpactReportAction.java`, line 17

No class-level `/** ... */` Javadoc block is present above the class declaration. The class purpose (handling HTTP requests for the impact report, populating form data, and forwarding to the "success" view) is undocumented.

```java
// Line 17 — no Javadoc preceding this line
public class ImpactReportAction extends Action {
```

---

### A21-2 — MEDIUM — Undocumented non-trivial public method: `ImpactReportAction#execute`

**File:** `ImpactReportAction.java`, line 24

The overridden `execute` method has no Javadoc. The method performs several non-trivial steps: session validation with a hard exception on missing `sessCompId`, retrieval of session-scoped formatting and timezone attributes, population of manufacturer and unit-type lookups on the search form, delegation to `ReportService.getImpactReport`, and forwarding to the "success" navigation outcome. None of this behaviour is documented.

```java
// Line 23-24 — no Javadoc
@Override
public ActionForward execute(ActionMapping mapping, ActionForm form, HttpServletRequest request, HttpServletResponse response) throws Exception {
```

---

### A21-3 — LOW — No class-level Javadoc: `IncidentReportAction`

**File:** `IncidentReportAction.java`, line 17

No class-level `/** ... */` Javadoc block is present above the class declaration. The class purpose (handling HTTP requests for the incident report) is undocumented.

```java
// Line 17 — no Javadoc preceding this line
public class IncidentReportAction extends Action {
```

---

### A21-4 — MEDIUM — Undocumented non-trivial public method: `IncidentReportAction#execute`

**File:** `IncidentReportAction.java`, line 20

The overridden `execute` method has no Javadoc. Like its counterpart in `ImpactReportAction`, the method performs session validation, extracts formatting/timezone attributes, populates the search form with manufacturers and unit types, calls `ReportService.getIncidentReport`, and forwards to "success". None of this behaviour is documented.

```java
// Line 19-20 — no Javadoc
@Override
public ActionForward execute(ActionMapping mapping, ActionForm form, HttpServletRequest request, HttpServletResponse response) throws Exception {
```

---

### A21-5 — MEDIUM — Type inconsistency between parallel classes: `sessCompId` parsed as `int` vs `Long`

**Files:**
- `ImpactReportAction.java`, line 32: `Long compId = Long.valueOf(sessCompId);`
- `IncidentReportAction.java`, line 31: `int compId = Integer.parseInt(sessCompId);`

The two action classes handle the same `sessCompId` session attribute differently. `ImpactReportAction` parses it as a boxed `Long`; `IncidentReportAction` parses it as a primitive `int`. This is a semantic inconsistency that may silently cause data loss or mismatched queries if `sessCompId` values exceed `Integer.MAX_VALUE` (2,147,483,647). While this is a code-quality issue rather than a pure documentation issue, it constitutes an inaccurate implicit contract between the two parallel classes that would be invisible without documentation. Flagged here because documentation is the appropriate place to surface such a contract; its absence contributes directly to the inconsistency going unnoticed.

---

### A21-6 — MEDIUM — Static vs instance DAO/Service access inconsistency between parallel classes

**Files:**
- `ImpactReportAction.java`, lines 19-21, 35-36: uses instance fields (`this.manufactureDAO`, `this.unitDAO`, `this.reportService`) obtained via `getInstance()`.
- `IncidentReportAction.java`, lines 34-35, 39: calls `ManufactureDAO.getAllManufactures(...)`, `UnitDAO.getAllUnitType()`, and `ReportService.getInstance().getIncidentReport(...)` directly as apparent static (or re-fetched singleton) calls with no instance fields declared.

These two classes are structurally inconsistent in how they obtain their collaborators. The `IncidentReportAction` appears to call `ManufactureDAO.getAllManufactures` and `UnitDAO.getAllUnitType` as if they were static methods, while `ImpactReportAction` stores singleton instances in private fields and calls them as instance methods. Without Javadoc or other documentation, this contract is invisible. Flagged as documentation-absent inaccuracy: the absence of any explanation makes it impossible to determine which pattern is authoritative.

---

## 3. Summary Table

| ID | Severity | File | Line(s) | Description |
|---|---|---|---|---|
| A21-1 | LOW | `ImpactReportAction.java` | 17 | No class-level Javadoc |
| A21-2 | MEDIUM | `ImpactReportAction.java` | 24 | `execute` has no Javadoc; non-trivial logic undocumented |
| A21-3 | LOW | `IncidentReportAction.java` | 17 | No class-level Javadoc |
| A21-4 | MEDIUM | `IncidentReportAction.java` | 20 | `execute` has no Javadoc; non-trivial logic undocumented |
| A21-5 | MEDIUM | Both files | 32 / 31 | `sessCompId` parsed as `Long` in one class, `int` in the other — silent inconsistency invisible without docs |
| A21-6 | MEDIUM | Both files | 19-21 / 34-39 | DAO/Service access pattern inconsistent (instance fields vs static-style calls) — undocumented contract |

**Total findings: 6**
- HIGH: 0
- MEDIUM: 4
- LOW: 2
