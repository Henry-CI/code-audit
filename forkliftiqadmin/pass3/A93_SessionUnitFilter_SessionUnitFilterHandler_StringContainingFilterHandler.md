# Pass 3 Documentation Audit — A93
**Audit run:** 2026-02-26-01
**Agent:** A93
**Files:**
- `querybuilder/filters/SessionUnitFilter.java`
- `querybuilder/filters/SessionUnitFilterHandler.java`
- `querybuilder/filters/StringContainingFilterHandler.java`

---

## Reading Evidence

### SessionUnitFilter.java

| Element | Kind | Line |
|---------|------|------|
| `SessionUnitFilter` | interface | 3 |
| `unitId()` | public abstract method | 4 |

**Fields:** none (interface)

---

### SessionUnitFilterHandler.java

| Element | Kind | Line |
|---------|------|------|
| `SessionUnitFilterHandler` | class (implements `FilterHandler`) | 7 |
| `filter` | field — `final SessionUnitFilter` | 8 |
| `unitIdFieldName` | field — `final String` | 9 |
| `SessionUnitFilterHandler(SessionUnitFilter, String)` | public constructor | 11 |
| `getQueryFilter()` | public method (`@Override`) | 17 |
| `prepareStatement(StatementPreparer)` | public method (`@Override`) | 23 |
| `ignoreFilter()` | private method | 28 |

---

### StringContainingFilterHandler.java

| Element | Kind | Line |
|---------|------|------|
| `StringContainingFilterHandler` | class (implements `FilterHandler`) | 9 |
| `searchText` | field — `final String` | 10 |
| `fieldNames` | field — `final List<String>` | 11 |
| `StringContainingFilterHandler(String, String...)` | public constructor | 13 |
| `getQueryFilter()` | public method (`@Override`) | 19 |
| `prepareStatement(StatementPreparer)` | public method (`@Override`) | 33 |

---

## Javadoc Analysis

### SessionUnitFilter.java

- **Class-level Javadoc:** absent.
- **`unitId()` (line 4):** no Javadoc.

### SessionUnitFilterHandler.java

- **Class-level Javadoc:** absent.
- **Constructor `SessionUnitFilterHandler(SessionUnitFilter, String)` (line 11):** no Javadoc.
- **`getQueryFilter()` (line 17):** no Javadoc.
- **`prepareStatement(StatementPreparer)` (line 23):** no Javadoc.
- **`ignoreFilter()` (line 28):** private — not subject to public Javadoc requirement.

### StringContainingFilterHandler.java

- **Class-level Javadoc:** absent.
- **Constructor `StringContainingFilterHandler(String, String...)` (line 13):** no Javadoc.
- **`getQueryFilter()` (line 19):** no Javadoc.
- **`prepareStatement(StatementPreparer)` (line 33):** no Javadoc.

---

## Findings

### A93-1 — LOW — No class-level Javadoc: `SessionUnitFilter`
**File:** `querybuilder/filters/SessionUnitFilter.java`, line 3
**Detail:** The interface `SessionUnitFilter` has no class-level Javadoc comment. Its purpose (marking objects that carry a unit ID for SQL session filtering) is not documented.

---

### A93-2 — LOW — Undocumented trivial public method: `SessionUnitFilter.unitId()`
**File:** `querybuilder/filters/SessionUnitFilter.java`, line 4
**Detail:** The single interface method `unitId()` has no Javadoc. It is a simple accessor, but documenting that it returns the unit identifier to be used in query filtering would improve API clarity.

---

### A93-3 — LOW — No class-level Javadoc: `SessionUnitFilterHandler`
**File:** `querybuilder/filters/SessionUnitFilterHandler.java`, line 7
**Detail:** The class `SessionUnitFilterHandler` has no class-level Javadoc. The class applies a SQL `AND <field> = ?` clause for a unit ID obtained from a `SessionUnitFilter`; this intent is undocumented.

---

### A93-4 — MEDIUM — Undocumented non-trivial public constructor: `SessionUnitFilterHandler(SessionUnitFilter, String)`
**File:** `querybuilder/filters/SessionUnitFilterHandler.java`, line 11
**Detail:** The constructor accepts two parameters:
- `filter` — the source of the unit ID (may be `null`; a `null` filter or `null` unit ID causes the filter to be silently skipped).
- `unitIdFieldName` — the SQL column name to bind against.

The null-tolerance behaviour is non-obvious and important for callers. No Javadoc, no `@param` tags.

---

### A93-5 — MEDIUM — Undocumented non-trivial public method: `SessionUnitFilterHandler.getQueryFilter()`
**File:** `querybuilder/filters/SessionUnitFilterHandler.java`, line 17
**Detail:** Returns an empty string when `ignoreFilter()` is true (filter is `null` or unit ID is `null`), otherwise returns ` AND <unitIdFieldName> = ? `. The silent skip-when-null behaviour is not documented. No Javadoc, no `@return` tag.

---

### A93-6 — MEDIUM — Undocumented non-trivial public method: `SessionUnitFilterHandler.prepareStatement(StatementPreparer)`
**File:** `querybuilder/filters/SessionUnitFilterHandler.java`, line 23
**Detail:** Conditionally binds `filter.unitId()` as a `Long` parameter. Like `getQueryFilter()`, it silently does nothing when the filter should be ignored. No Javadoc, no `@param` or `@throws` tag for `SQLException`.

---

### A93-7 — LOW — No class-level Javadoc: `StringContainingFilterHandler`
**File:** `querybuilder/filters/StringContainingFilterHandler.java`, line 9
**Detail:** The class `StringContainingFilterHandler` has no class-level Javadoc. The class builds an `ILIKE`-based SQL fragment for a substring search across one or more fields; this is undocumented at the class level.

---

### A93-8 — MEDIUM — Undocumented non-trivial public constructor: `StringContainingFilterHandler(String, String...)`
**File:** `querybuilder/filters/StringContainingFilterHandler.java`, line 13
**Detail:** The constructor wraps `searchText` with `%` wildcards on both sides (`"%" + searchText + "%"`) before storing it. This silent transformation is a significant side-effect that callers must be aware of — passing a value that already contains `%` would result in doubled wildcards. No Javadoc, no `@param` tags documenting this behaviour.

---

### A93-9 — MEDIUM — Undocumented non-trivial public method: `StringContainingFilterHandler.getQueryFilter()`
**File:** `querybuilder/filters/StringContainingFilterHandler.java`, line 19
**Detail:** Produces different SQL depending on whether one or multiple field names are provided:
- Single field: ` AND <field> ILIKE ? `
- Multiple fields: ` AND (<f1> ILIKE ? OR <f2> ILIKE ? ...) `

This branching logic and the use of `ILIKE` (case-insensitive, PostgreSQL-specific) are undocumented. No Javadoc, no `@return` tag.

---

### A93-10 — MEDIUM — Undocumented non-trivial public method: `StringContainingFilterHandler.prepareStatement(StatementPreparer)`
**File:** `querybuilder/filters/StringContainingFilterHandler.java`, line 33
**Detail:** Binds the pre-wrapped `searchText` once per field name (matching the number of `?` placeholders emitted by `getQueryFilter()`). The coupling between the number of bindings and the number of fields is implicit and undocumented. No Javadoc, no `@param` or `@throws` tag for `SQLException`.

---

## Summary Table

| ID | Severity | File | Location | Issue |
|----|----------|------|----------|-------|
| A93-1 | LOW | `SessionUnitFilter.java` | line 3 | No class-level Javadoc on interface |
| A93-2 | LOW | `SessionUnitFilter.java` | line 4 | Undocumented trivial interface method `unitId()` |
| A93-3 | LOW | `SessionUnitFilterHandler.java` | line 7 | No class-level Javadoc on class |
| A93-4 | MEDIUM | `SessionUnitFilterHandler.java` | line 11 | Undocumented non-trivial constructor; null-tolerance not described |
| A93-5 | MEDIUM | `SessionUnitFilterHandler.java` | line 17 | Undocumented `getQueryFilter()`; silent skip-when-null not described |
| A93-6 | MEDIUM | `SessionUnitFilterHandler.java` | line 23 | Undocumented `prepareStatement()`; conditional binding not described |
| A93-7 | LOW | `StringContainingFilterHandler.java` | line 9 | No class-level Javadoc on class |
| A93-8 | MEDIUM | `StringContainingFilterHandler.java` | line 13 | Undocumented constructor; `%`-wrapping side-effect not described |
| A93-9 | MEDIUM | `StringContainingFilterHandler.java` | line 19 | Undocumented `getQueryFilter()`; branching SQL and `ILIKE` semantics not described |
| A93-10 | MEDIUM | `StringContainingFilterHandler.java` | line 33 | Undocumented `prepareStatement()`; binding-count coupling not described |

**Total findings: 10** (3 LOW, 7 MEDIUM, 0 HIGH)
