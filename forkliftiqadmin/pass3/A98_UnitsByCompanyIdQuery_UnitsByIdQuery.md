# Pass 3 Documentation Audit — A98
**Audit run:** 2026-02-26-01
**Agent:** A98
**Files reviewed:**
- `src/main/java/com/querybuilder/unit/UnitsByCompanyIdQuery.java`
- `src/main/java/com/querybuilder/unit/UnitsByIdQuery.java`

---

## 1. Reading Evidence

### 1.1 UnitsByCompanyIdQuery.java

**Class:** `UnitsByCompanyIdQuery` — line 13

**Fields:**

| Field | Type | Line |
|-------|------|------|
| `BASE_QUERY` | `private static final String` | 14 |
| `companyId` | `private int` | 19 |
| `orderBy` | `private String` | 20 |
| `activeUnitsOnly` | `private String` | 21 |
| `filter` | `private StringContainingFilterHandler` | 22 |

**Methods:**

| Method | Visibility | Line |
|--------|------------|------|
| `UnitsByCompanyIdQuery(int companyId)` (constructor) | `private` | 24 |
| `prepare(int companyId)` | `public static` | 29 |
| `orderBy(String orderBy)` | `public` | 33 |
| `activeUnitsOnly()` | `public` | 38 |
| `containing(String text)` | `public` | 43 |
| `query()` | `public` | 48 |
| `prepareStatement(PreparedStatement statement)` | `private` | 59 |
| `mapResult(ResultSet result)` | `private` | 67 |

---

### 1.2 UnitsByIdQuery.java

**Class:** `UnitsByIdQuery` — line 13

**Fields:**

| Field | Type | Line |
|-------|------|------|
| `query` | `private static final String` | 14 |
| `unitId` | `private long` | 16 |

**Methods:**

| Method | Visibility | Line |
|--------|------------|------|
| `UnitsByIdQuery(long unitId)` (constructor) | `private` | 18 |
| `prepare(int unitId)` | `public static` | 22 |
| `query()` | `public` | 26 |
| `prepareStatement(PreparedStatement statement)` | `private` | 32 |
| `getResult(ResultSet result)` | `private` | 37 |

---

## 2. Findings

### A98-1 — No class-level Javadoc on `UnitsByCompanyIdQuery`
**File:** `UnitsByCompanyIdQuery.java`, line 13
**Severity:** LOW
**Detail:** The class `UnitsByCompanyIdQuery` has no `/** ... */` Javadoc comment. The class implements a builder-style query object that retrieves units visible to a given company (by direct `comp_id` ownership or via the `unit_company` association table with date-range filtering). A class-level comment describing purpose and builder usage pattern is absent.

---

### A98-2 — Undocumented non-trivial public static factory method `prepare` in `UnitsByCompanyIdQuery`
**File:** `UnitsByCompanyIdQuery.java`, line 29
**Severity:** MEDIUM
**Detail:** `public static UnitsByCompanyIdQuery prepare(int companyId)` has no Javadoc. This is the sole entry point for constructing the query object; callers cannot discover its purpose, parameter meaning, or builder-chain idiom from the API surface alone.
Missing tags: `@param companyId`, `@return`.

---

### A98-3 — Undocumented non-trivial public method `orderBy` in `UnitsByCompanyIdQuery`
**File:** `UnitsByCompanyIdQuery.java`, line 33
**Severity:** MEDIUM
**Detail:** `public UnitsByCompanyIdQuery orderBy(String orderBy)` has no Javadoc. The method appends a raw `ORDER BY` clause to the query. Callers should be warned that the value is injected directly into the SQL string without parameterisation — this is a potential SQL-injection risk if the caller supplies untrusted input. The absence of any documentation leaves this hazard entirely invisible.
Missing tags: `@param orderBy`, `@return`.

---

### A98-4 — Undocumented non-trivial public method `activeUnitsOnly` in `UnitsByCompanyIdQuery`
**File:** `UnitsByCompanyIdQuery.java`, line 38
**Severity:** MEDIUM
**Detail:** `public UnitsByCompanyIdQuery activeUnitsOnly()` has no Javadoc. The method appends `AND active IS TRUE` to the WHERE clause; its effect on the result set is not self-evident from the name alone (e.g. it is not clear what column or table the `active` flag belongs to, or whether the default state retrieves both active and inactive units).
Missing tag: `@return`.

---

### A98-5 — Undocumented non-trivial public method `containing` in `UnitsByCompanyIdQuery`
**File:** `UnitsByCompanyIdQuery.java`, line 43
**Severity:** MEDIUM
**Detail:** `public UnitsByCompanyIdQuery containing(String text)` has no Javadoc. The method installs a `StringContainingFilterHandler` that filters on `name` and `serial_no` columns. The columns filtered, the matching semantics (substring / ILIKE / LIKE), and the builder-chain return value are undocumented.
Missing tags: `@param text`, `@return`.

---

### A98-6 — Undocumented non-trivial public method `query` in `UnitsByCompanyIdQuery`
**File:** `UnitsByCompanyIdQuery.java`, line 48
**Severity:** MEDIUM
**Detail:** `public List<UnitBean> query() throws SQLException` has no Javadoc. This is the terminal method of the builder chain; it executes the assembled SQL and returns a list of `UnitBean` objects. The checked exception, the return type semantics, and interaction with earlier builder state are all undocumented.
Missing tags: `@return`, `@throws SQLException`.

---

### A98-7 — No class-level Javadoc on `UnitsByIdQuery`
**File:** `UnitsByIdQuery.java`, line 13
**Severity:** LOW
**Detail:** The class `UnitsByIdQuery` has no `/** ... */` Javadoc comment. The class looks up a single unit by its numeric ID against the `v_units` view and returns a fully populated `UnitBean`.

---

### A98-8 — Undocumented non-trivial public static factory method `prepare` in `UnitsByIdQuery`
**File:** `UnitsByIdQuery.java`, line 22
**Severity:** MEDIUM
**Detail:** `public static UnitsByIdQuery prepare(int unitId)` has no Javadoc. This is the only way to construct the object; the parameter's meaning and the returned builder object are undocumented.
Missing tags: `@param unitId`, `@return`.

**Additional note (type mismatch — non-documentation issue, noted for completeness):** The parameter is declared as `int unitId` (line 22) but the backing field `unitId` is typed `long` (line 16). Widening occurs silently at the assignment in the private constructor (line 18–20). This is a latent correctness concern but not a documentation finding per the audit scope.

---

### A98-9 — Undocumented non-trivial public method `query` in `UnitsByIdQuery`
**File:** `UnitsByIdQuery.java`, line 26
**Severity:** MEDIUM
**Detail:** `public List<UnitBean> query() throws SQLException` has no Javadoc. The method executes `SELECT * FROM v_units WHERE id = ?` and returns a list (typically zero or one element). The return cardinality, the checked exception, and the fully populated nature of the returned beans are all undocumented.
Missing tags: `@return`, `@throws SQLException`.

---

## 3. Summary Table

| ID | File | Line | Element | Severity |
|----|------|------|---------|----------|
| A98-1 | UnitsByCompanyIdQuery.java | 13 | Class-level Javadoc missing | LOW |
| A98-2 | UnitsByCompanyIdQuery.java | 29 | `prepare(int)` — no Javadoc, missing @param/@return | MEDIUM |
| A98-3 | UnitsByCompanyIdQuery.java | 33 | `orderBy(String)` — no Javadoc, raw SQL injection risk undisclosed, missing @param/@return | MEDIUM |
| A98-4 | UnitsByCompanyIdQuery.java | 38 | `activeUnitsOnly()` — no Javadoc, missing @return | MEDIUM |
| A98-5 | UnitsByCompanyIdQuery.java | 43 | `containing(String)` — no Javadoc, missing @param/@return | MEDIUM |
| A98-6 | UnitsByCompanyIdQuery.java | 48 | `query()` — no Javadoc, missing @return/@throws | MEDIUM |
| A98-7 | UnitsByIdQuery.java | 13 | Class-level Javadoc missing | LOW |
| A98-8 | UnitsByIdQuery.java | 22 | `prepare(int)` — no Javadoc, missing @param/@return | MEDIUM |
| A98-9 | UnitsByIdQuery.java | 26 | `query()` — no Javadoc, missing @return/@throws | MEDIUM |

**Total findings: 9** (7 MEDIUM, 2 LOW)
