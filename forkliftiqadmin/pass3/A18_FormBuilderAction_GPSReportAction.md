# Pass 3 Documentation Audit — Agent A18
**Audit run:** 2026-02-26-01
**Files audited:**
- `src/main/java/com/action/FormBuilderAction.java`
- `src/main/java/com/action/GPSReportAction.java`

---

## 1. Reading Evidence

### 1.1 FormBuilderAction.java

**Class**
| Item | Line |
|------|------|
| `public class FormBuilderAction extends Action` | 37 |

**Fields**
| Field name | Type | Line |
|------------|------|------|
| `log` | `private static Logger` | 39 |

**Methods**
| Method name | Visibility | Return type | Line |
|-------------|------------|-------------|------|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | public | `ActionForward` | 41–115 |

---

### 1.2 GPSReportAction.java

**Class**
| Item | Line |
|------|------|
| `public class GPSReportAction extends Action` | 17 |

**Fields**
| Field name | Type | Line |
|------------|------|------|
| `reportService` | `private ReportService` | 19 |
| `manufactureDAO` | `private ManufactureDAO` | 20 |
| `unitDAO` | `private UnitDAO` | 21 |

**Methods**
| Method name | Visibility | Return type | Line |
|-------------|------------|-------------|------|
| `execute(ActionMapping, ActionForm, HttpServletRequest, HttpServletResponse)` | public | `ActionForward` | 24–44 |

---

## 2. Findings

### A18-1 — FormBuilderAction: No class-level Javadoc
**File:** `src/main/java/com/action/FormBuilderAction.java`, line 37
**Severity:** LOW
**Details:** The class `FormBuilderAction` has no Javadoc comment. There is no description of the class's purpose, responsibilities, or the Struts action workflow it implements (form data collection, email dispatch, dynamic form rendering).

---

### A18-2 — FormBuilderAction.execute: No Javadoc
**File:** `src/main/java/com/action/FormBuilderAction.java`, lines 41–115
**Severity:** MEDIUM
**Details:** The sole public method `execute` has no Javadoc whatsoever. This method is non-trivial: it reads session attributes, dispatches on an `action` request parameter, iterates over all request parameters to build an HTML email body, retrieves an entity from the database, sends a diagnostic email via `Util.sendMail`, resolves a `FormBuilderBean` from a library, sorts its elements by position, and sets several request attributes before forwarding. The complete absence of any `/** ... */` block means there are no `@param`, `@return`, or `@throws` tags. Callers and maintainers have no documented contract.

---

### A18-3 — FormBuilderAction.execute: Misleading error message references `action` variable when action is not "save"
**File:** `src/main/java/com/action/FormBuilderAction.java`, line 104
**Severity:** MEDIUM
**Details:** The error message constructed when no form library entry exists for the given `qid`/`type` pair reads:

```java
new ActionMessage("errors.detail", "There is no " + action + " against this question.");
```

When `action` is an empty string (the default when the request parameter is absent), the message becomes `"There is no  against this question."` — a grammatically broken, user-facing string that exposes the internal concept of `action` values directly. While this is partly a code quality issue, it would mislead users and is worth documenting. There is no inline comment or Javadoc explaining the intent of this error path or the expected values of `action`.

---

### A18-4 — GPSReportAction: No class-level Javadoc
**File:** `src/main/java/com/action/GPSReportAction.java`, line 17
**Severity:** LOW
**Details:** The class `GPSReportAction` has no Javadoc comment. There is no description of its purpose — i.e., that it handles GPS report display by populating units for the session's company and forwarding to the GPS report view.

---

### A18-5 — GPSReportAction.execute: No Javadoc
**File:** `src/main/java/com/action/GPSReportAction.java`, lines 24–44
**Severity:** MEDIUM
**Details:** The sole public method `execute` (annotated `@Override`) has no Javadoc block. The method is non-trivial: it validates the session company ID and throws `RuntimeException` if absent, extracts date format, datetime format, and timezone from the session, loads all units for the company via `UnitDAO.getAllUnitsByCompanyId`, and forwards to `"success"`. There are no `@param`, `@return`, or `@throws` tags documenting the `RuntimeException` that is unconditionally thrown when no valid user is logged in.

---

### A18-6 — GPSReportAction.execute: Dead/commented-out code with no explanation
**File:** `src/main/java/com/action/GPSReportAction.java`, lines 35–36, 39, 41–42
**Severity:** LOW
**Details:** Four blocks of code are commented out with no explanation:

```java
//        searchForm.setManufacturers(this.manufactureDAO.getAllManufactures(sessCompId));
//        searchForm.setUnitTypes(unitDAO.getAllUnitType());
```
```java
//        ImpactReportBean impactReport = reportService.getImpactReport(compId, searchForm.getImpactReportFilter(dateFormat), dateTimeFormat, timezone);
//        request.setAttribute("impactReport", impactReport);
```

The fields `reportService`, `manufactureDAO`, and the local variables `dateFormat`, `dateTimeFormat`, `timezone`, `compId`, and `searchForm` are all populated but either partially or fully unused at runtime due to this commented-out code. There is no documentation explaining whether this is intentional (feature disabled, work in progress, etc.). This makes the class misleading — three instance fields suggest active usage that does not occur.

---

### A18-7 — GPSReportAction: Undocumented `RuntimeException` throw
**File:** `src/main/java/com/action/GPSReportAction.java`, line 27
**Severity:** MEDIUM
**Details:** The method throws an unchecked `RuntimeException` with the message `"Must have valid user logged in here"` when `sessCompId` is null, but this behaviour is entirely undocumented. There is no `@throws` tag, no class-level explanation of preconditions, and no Javadoc on the method. Callers relying on Struts exception handling configuration may not realise this path exists.

---

## 3. Summary Table

| ID | File | Location | Severity | Description |
|----|------|----------|----------|-------------|
| A18-1 | FormBuilderAction.java | class, line 37 | LOW | No class-level Javadoc |
| A18-2 | FormBuilderAction.java | `execute`, line 41 | MEDIUM | No Javadoc on non-trivial public method; no @param/@return/@throws |
| A18-3 | FormBuilderAction.java | `execute`, line 104 | MEDIUM | Error message interpolates `action` variable; produces broken string when action is empty; no comment explaining valid values |
| A18-4 | GPSReportAction.java | class, line 17 | LOW | No class-level Javadoc |
| A18-5 | GPSReportAction.java | `execute`, line 24 | MEDIUM | No Javadoc on non-trivial public method; no @param/@return/@throws |
| A18-6 | GPSReportAction.java | `execute`, lines 35–36, 39, 41–42 | LOW | Commented-out code with no explanatory comment; three instance fields effectively unused |
| A18-7 | GPSReportAction.java | `execute`, line 27 | MEDIUM | Undocumented `RuntimeException` throw; no @throws documentation |

**Finding counts:** LOW: 3, MEDIUM: 4, HIGH: 0
