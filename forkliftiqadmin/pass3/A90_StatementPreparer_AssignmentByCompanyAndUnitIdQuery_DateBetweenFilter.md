# Pass 3 Documentation Audit — Agent A90
**Audit run:** 2026-02-26-01
**Files audited:**
- `querybuilder/StatementPreparer.java`
- `querybuilder/assignment/AssignmentByCompanyAndUnitIdQuery.java`
- `querybuilder/filters/DateBetweenFilter.java`

---

## 1. Reading Evidence

### 1.1 `StatementPreparer.java`

**Class:** `StatementPreparer` — line 7

**Fields:**

| Name | Type | Line |
|------|------|------|
| `statement` | `PreparedStatement` | 8 |
| `index` | `int` | 9 |

**Methods:**

| Name | Visibility | Line |
|------|-----------|------|
| `StatementPreparer(PreparedStatement statement)` | `public` (constructor) | 11 |
| `addDate(Date value)` | `public` | 16 |
| `addLong(long value)` | `public` | 20 |
| `addString(String value)` | `public` | 24 |
| `addInteger(int value)` | `public` | 28 |

---

### 1.2 `AssignmentByCompanyAndUnitIdQuery.java`

**Class:** `AssignmentByCompanyAndUnitIdQuery` — line 13

**Fields:**

| Name | Type | Line |
|------|------|------|
| `query` | `private static final String` | 14 |
| `companyId` | `private final long` | 20 |
| `unitId` | `private final long` | 21 |

**Methods:**

| Name | Visibility | Line |
|------|-----------|------|
| `AssignmentByCompanyAndUnitIdQuery(long companyId, long unitId)` | `public` (constructor) | 23 |
| `query(String dateFormat)` | `public` | 28 |
| `mapResults(String dateFormat, ResultSet resultSet)` | `private` | 32 |
| `prepareStatement(PreparedStatement statement)` | `private` | 42 |

---

### 1.3 `DateBetweenFilter.java`

**Type:** `interface DateBetweenFilter` — line 5

**Fields:** none

**Methods:**

| Name | Visibility | Line |
|------|-----------|------|
| `start()` | `public` (interface) | 6 |
| `end()` | `public` (interface) | 7 |
| `timezone()` | `public` (interface) | 8 |

---

## 2. Findings

### A90-1 — `StatementPreparer`: No class-level Javadoc
**Severity:** LOW
**File:** `querybuilder/StatementPreparer.java`, line 7
**Detail:** The class `StatementPreparer` has no `/** ... */` Javadoc comment. Its purpose — wrapping a `PreparedStatement` with an auto-incrementing positional index — is non-obvious and would benefit from a class-level description.

---

### A90-2 — `StatementPreparer`: Undocumented constructor
**Severity:** LOW
**File:** `querybuilder/StatementPreparer.java`, line 11
**Detail:** `public StatementPreparer(PreparedStatement statement)` has no Javadoc. The constructor initializes the internal `index` to `0` as a side-effect not visible from the signature. Missing `@param statement`.

---

### A90-3 — `StatementPreparer`: Undocumented non-trivial public method `addDate`
**Severity:** MEDIUM
**File:** `querybuilder/StatementPreparer.java`, line 16
**Detail:** `public void addDate(Date value) throws SQLException` has no Javadoc. The method converts `java.util.Date` to `java.sql.Date` before binding, which is a meaningful implementation detail (timezone/precision implications) that callers should be aware of. Missing `@param value`, `@throws SQLException`.

---

### A90-4 — `StatementPreparer`: Undocumented non-trivial public method `addLong`
**Severity:** MEDIUM
**File:** `querybuilder/StatementPreparer.java`, line 20
**Detail:** `public void addLong(long value) throws SQLException` has no Javadoc. Missing `@param value`, `@throws SQLException`.

---

### A90-5 — `StatementPreparer`: Undocumented non-trivial public method `addString`
**Severity:** MEDIUM
**File:** `querybuilder/StatementPreparer.java`, line 24
**Detail:** `public void addString(String value) throws SQLException` has no Javadoc. Missing `@param value`, `@throws SQLException`.

---

### A90-6 — `StatementPreparer`: Undocumented non-trivial public method `addInteger`
**Severity:** MEDIUM
**File:** `querybuilder/StatementPreparer.java`, line 28
**Detail:** `public void addInteger(int value) throws SQLException` has no Javadoc. Missing `@param value`, `@throws SQLException`.

---

### A90-7 — `AssignmentByCompanyAndUnitIdQuery`: No class-level Javadoc
**Severity:** LOW
**File:** `querybuilder/assignment/AssignmentByCompanyAndUnitIdQuery.java`, line 13
**Detail:** The class has no `/** ... */` Javadoc comment. Its purpose — querying unit assignments filtered by both `company_id` and `parent_company_id` for a given unit — is not self-evident from the class name alone and warrants a class-level description.

---

### A90-8 — `AssignmentByCompanyAndUnitIdQuery`: Undocumented constructor
**Severity:** LOW
**File:** `querybuilder/assignment/AssignmentByCompanyAndUnitIdQuery.java`, line 23
**Detail:** `public AssignmentByCompanyAndUnitIdQuery(long companyId, long unitId)` has no Javadoc. Missing `@param companyId`, `@param unitId`.

---

### A90-9 — `AssignmentByCompanyAndUnitIdQuery`: Undocumented non-trivial public method `query`
**Severity:** MEDIUM
**File:** `querybuilder/assignment/AssignmentByCompanyAndUnitIdQuery.java`, line 28
**Detail:** `public List<UnitAssignmentBean> query(String dateFormat) throws SQLException` has no Javadoc. The `dateFormat` parameter controls how `start_date` and `end_date` are formatted on returned beans — a non-obvious contract. Missing `@param dateFormat`, `@return`, `@throws SQLException`.

---

### A90-10 — `DateBetweenFilter`: No interface-level Javadoc
**Severity:** LOW
**File:** `querybuilder/filters/DateBetweenFilter.java`, line 5
**Detail:** The interface `DateBetweenFilter` has no `/** ... */` Javadoc comment. The purpose of the filter contract and how its three methods interrelate (start/end date bounds plus timezone context) is not documented.

---

### A90-11 — `DateBetweenFilter`: Undocumented interface methods `start()`, `end()`, `timezone()`
**Severity:** LOW
**File:** `querybuilder/filters/DateBetweenFilter.java`, lines 6–8
**Detail:** All three abstract interface methods (`start()`, `end()`, `timezone()`) lack Javadoc. While names are largely self-descriptive, the expected semantics of `timezone()` (e.g., IANA zone ID string, UTC offset, or `TimeZone` display name) and the inclusive/exclusive nature of the `start()`/`end()` bounds are not specified. Missing `@return` on each method. Classified LOW rather than MEDIUM because these are interface contract methods with intuitive names; however, `timezone()` in particular warrants at minimum a `@return` describing the expected format.

---

## 3. Summary

| ID | File | Element | Severity |
|----|------|---------|----------|
| A90-1 | `StatementPreparer.java` | Class-level Javadoc missing | LOW |
| A90-2 | `StatementPreparer.java` | Constructor undocumented | LOW |
| A90-3 | `StatementPreparer.java` | `addDate` undocumented | MEDIUM |
| A90-4 | `StatementPreparer.java` | `addLong` undocumented | MEDIUM |
| A90-5 | `StatementPreparer.java` | `addString` undocumented | MEDIUM |
| A90-6 | `StatementPreparer.java` | `addInteger` undocumented | MEDIUM |
| A90-7 | `AssignmentByCompanyAndUnitIdQuery.java` | Class-level Javadoc missing | LOW |
| A90-8 | `AssignmentByCompanyAndUnitIdQuery.java` | Constructor undocumented | LOW |
| A90-9 | `AssignmentByCompanyAndUnitIdQuery.java` | `query` undocumented | MEDIUM |
| A90-10 | `DateBetweenFilter.java` | Interface-level Javadoc missing | LOW |
| A90-11 | `DateBetweenFilter.java` | `start()`, `end()`, `timezone()` undocumented | LOW |

**Total findings:** 11 (6 MEDIUM, 5 LOW, 0 HIGH)

No inaccurate or dangerously wrong comments were found (no existing Javadoc was present to be incorrect).
