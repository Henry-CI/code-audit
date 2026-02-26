# Pass 3 – Documentation Audit
**Agent:** A91
**Audit run:** 2026-02-26-01
**Files audited:**
- `src/main/java/com/querybuilder/filters/DateBetweenFilterHandler.java`
- `src/main/java/com/querybuilder/filters/FilterHandler.java`
- `src/main/java/com/querybuilder/filters/ImpactLevelFilter.java`

---

## 1. Reading Evidence

### 1.1 DateBetweenFilterHandler.java

**Class:** `DateBetweenFilterHandler` — line 7
Implements: `FilterHandler`

**Fields:**
| Name | Type | Line |
|------|------|------|
| `filter` | `DateBetweenFilter` (final) | 8 |
| `fieldName` | `String` (final) | 9 |

**Methods:**
| Name | Visibility | Line | Notes |
|------|-----------|------|-------|
| `DateBetweenFilterHandler(DateBetweenFilter, String)` | public | 11 | Constructor |
| `getQueryFilter()` | public | 17 | `@Override` from `FilterHandler` |
| `prepareStatement(StatementPreparer)` | public | 27 | `@Override` from `FilterHandler`; throws `SQLException` |
| `ignoreFilter()` | private | 34 | |
| `filterStartOnly()` | private | 38 | |
| `filterEndOnly()` | private | 42 | |
| `filterBetweenTwoDates()` | private | 46 | |

---

### 1.2 FilterHandler.java

**Type:** `interface FilterHandler` — line 7

**Fields:** none

**Methods:**
| Name | Visibility | Line | Notes |
|------|-----------|------|-------|
| `getQueryFilter()` | public (interface) | 8 | Returns `String` |
| `prepareStatement(StatementPreparer)` | public (interface) | 10 | throws `SQLException` |

---

### 1.3 ImpactLevelFilter.java

**Type:** `interface ImpactLevelFilter` — line 5

**Fields:** none

**Methods:**
| Name | Visibility | Line | Notes |
|------|-----------|------|-------|
| `impactLevel()` | public (interface) | 6 | Returns `ImpactLevel` |

---

## 2. Javadoc Analysis

### 2.1 DateBetweenFilterHandler.java

No Javadoc comment (`/** ... */`) is present anywhere in this file — not on the class, the constructor, or any method.

#### Public constructor: `DateBetweenFilterHandler(DateBetweenFilter, String)` (line 11)
- Javadoc present: **No**
- The constructor accepts two parameters whose semantics (`filter` and `fieldName`) are non-obvious in the absence of surrounding context (what SQL column `fieldName` represents, whether `filter` may be null at construction time). This is a non-trivial constructor.

#### Public method: `getQueryFilter()` (line 17)
- Javadoc present: **No**
- Non-trivial logic: builds a conditional SQL fragment, handles three distinct filter modes (start-only, end-only, between), and embeds a timezone conversion expression. There is also a commented-out alternative implementation on line 21 that is materially different from the active one.

#### Public method: `prepareStatement(StatementPreparer)` (line 27)
- Javadoc present: **No**
- Non-trivial: conditionally binds between one and three parameters (timezone string, start date, end date) depending on filter state; parameter-binding order must match `getQueryFilter()` output exactly.

---

### 2.2 FilterHandler.java

No Javadoc comment is present anywhere in this file.

#### Interface method: `getQueryFilter()` (line 8)
- Javadoc present: **No**
- Non-trivial: the interface contract is not documented — callers have no specification of the returned SQL fragment format (prefix, quoting, parameterisation).

#### Interface method: `prepareStatement(StatementPreparer)` (line 10)
- Javadoc present: **No**
- Non-trivial: the interface contract specifying the relationship between `getQueryFilter()` parameter placeholders and the order in which `prepareStatement` must bind values is entirely absent.

---

### 2.3 ImpactLevelFilter.java

No Javadoc comment is present anywhere in this file.

#### Interface method: `impactLevel()` (line 6)
- Javadoc present: **No**
- Semantically simple accessor; missing documentation is low severity.

---

## 3. Additional Observations

**Commented-out code (DateBetweenFilterHandler.java, line 21):**
```java
//        if (filterBetweenTwoDates()) return String.format(" AND %s::DATE BETWEEN ? AND ?", fieldName);
```
The active replacement on line 22 changes the parameter count from 2 to 3 (adds a timezone `?` as the first bind value) and changes the SQL from a simple date cast to a timezone-aware conversion. The commented-out line is misleading — a reader may assume either form is equivalent or that the comment is merely disabled for debugging. The absence of any explanatory comment describing why the original was replaced and what the timezone bind value represents increases maintenance risk.

---

## 4. Findings

### A91-1
**Severity:** LOW
**File:** `DateBetweenFilterHandler.java`
**Location:** Line 7 (class declaration)
**Finding:** No class-level Javadoc. The class purpose, the SQL dialect it targets, the nullability contract for constructor arguments, and the relationship between `getQueryFilter()` and `prepareStatement()` are all undocumented.

---

### A91-2
**Severity:** MEDIUM
**File:** `DateBetweenFilterHandler.java`
**Location:** Lines 11–14 (constructor)
**Finding:** Public non-trivial constructor has no Javadoc. There is no documentation of what `fieldName` represents (a SQL column identifier), whether `filter` may be `null` at construction time (though `ignoreFilter()` guards it later), or whether `fieldName` is expected to be pre-quoted/sanitised.

---

### A91-3
**Severity:** MEDIUM
**File:** `DateBetweenFilterHandler.java`
**Location:** Lines 17–24 (`getQueryFilter()`)
**Finding:** Non-trivial public `@Override` method has no Javadoc. The method produces one of four possible SQL fragments (empty string, start-only `>=`, end-only `<=`, or timezone-aware `BETWEEN`) and the selection logic is not documented. No `@return` tag describes the possible return values or their SQL semantics.

---

### A91-4
**Severity:** MEDIUM
**File:** `DateBetweenFilterHandler.java`
**Location:** Lines 27–32 (`prepareStatement(StatementPreparer)`)
**Finding:** Non-trivial public `@Override` method has no Javadoc. The method conditionally binds between one and three JDBC parameters in a specific order that must correspond to the placeholders emitted by `getQueryFilter()`. This ordering contract — timezone first, then start, then end — is undocumented. No `@param` or `@throws` tags are present.

---

### A91-5
**Severity:** MEDIUM
**File:** `DateBetweenFilterHandler.java`
**Location:** Lines 21–22 (commented-out code inside `getQueryFilter()`)
**Finding:** A commented-out alternative implementation is left without any explanatory note. The replacement silently changes the number of bound parameters from 2 to 3 and changes the casting mechanism. Without a comment explaining the reason for the change (e.g., timezone support requirement), the dead code is misleading and may cause a future maintainer to incorrectly restore it, breaking parameter binding.
**Severity rationale:** MEDIUM — the comment is not itself inaccurate documentation, but the absence of explanation alongside the retained dead code creates a maintenance hazard that borders on a documentation accuracy issue.

---

### A91-6
**Severity:** LOW
**File:** `FilterHandler.java`
**Location:** Line 7 (interface declaration)
**Finding:** No interface-level Javadoc. The contract of the interface — that implementors must produce a SQL fragment with `?` placeholders via `getQueryFilter()` and bind matching parameters in order via `prepareStatement()` — is entirely unspecified.

---

### A91-7
**Severity:** MEDIUM
**File:** `FilterHandler.java`
**Location:** Line 8 (`getQueryFilter()`)
**Finding:** Non-trivial interface method has no Javadoc. The expected format of the returned SQL string (e.g., leading `AND`, use of `?` placeholders, empty string when inactive) is not documented. No `@return` tag.

---

### A91-8
**Severity:** MEDIUM
**File:** `FilterHandler.java`
**Location:** Line 10 (`prepareStatement(StatementPreparer)`)
**Finding:** Non-trivial interface method has no Javadoc. The binding-order contract (parameters must match the `?` placeholders from `getQueryFilter()` in left-to-right order) is nowhere stated. No `@param` or `@throws` tags.

---

### A91-9
**Severity:** LOW
**File:** `ImpactLevelFilter.java`
**Location:** Line 5 (interface declaration)
**Finding:** No interface-level Javadoc. The purpose and intended implementors of this interface are undocumented.

---

### A91-10
**Severity:** LOW
**File:** `ImpactLevelFilter.java`
**Location:** Line 6 (`impactLevel()`)
**Finding:** Undocumented interface method. Although this is a simple accessor, the absence of a `@return` tag means the nullability contract (may the returned `ImpactLevel` be `null`?) is unspecified.

---

## 5. Summary Table

| ID | Severity | File | Location | Issue |
|----|----------|------|----------|-------|
| A91-1 | LOW | `DateBetweenFilterHandler.java` | Line 7 | No class-level Javadoc |
| A91-2 | MEDIUM | `DateBetweenFilterHandler.java` | Lines 11–14 | Undocumented public constructor; non-trivial semantics |
| A91-3 | MEDIUM | `DateBetweenFilterHandler.java` | Lines 17–24 | Undocumented `getQueryFilter()`; no `@return` |
| A91-4 | MEDIUM | `DateBetweenFilterHandler.java` | Lines 27–32 | Undocumented `prepareStatement()`; no `@param`/`@throws` |
| A91-5 | MEDIUM | `DateBetweenFilterHandler.java` | Lines 21–22 | Commented-out code with no explanation; silent parameter-count change |
| A91-6 | LOW | `FilterHandler.java` | Line 7 | No interface-level Javadoc |
| A91-7 | MEDIUM | `FilterHandler.java` | Line 8 | Undocumented `getQueryFilter()`; no `@return` |
| A91-8 | MEDIUM | `FilterHandler.java` | Line 10 | Undocumented `prepareStatement()`; no `@param`/`@throws` |
| A91-9 | LOW | `ImpactLevelFilter.java` | Line 5 | No interface-level Javadoc |
| A91-10 | LOW | `ImpactLevelFilter.java` | Line 6 | Undocumented `impactLevel()`; nullability unspecified |

**Totals:** 5 MEDIUM, 5 LOW, 0 HIGH
