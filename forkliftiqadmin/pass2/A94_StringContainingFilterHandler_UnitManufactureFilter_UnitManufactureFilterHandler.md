# Pass 2 Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A94
**Date:** 2026-02-26

## Source Files Audited

1. `src/main/java/com/querybuilder/filters/StringContainingFilterHandler.java`
2. `src/main/java/com/querybuilder/filters/UnitManufactureFilter.java`
3. `src/main/java/com/querybuilder/filters/UnitManufactureFilterHandler.java`

---

## Reading Evidence

### 1. StringContainingFilterHandler.java

**Class:** `StringContainingFilterHandler`
**Implements:** `FilterHandler`
**Package:** `com.querybuilder.filters`

**Fields:**
| Field | Line | Type | Modifier |
|-------|------|------|----------|
| `searchText` | 10 | `String` | `private final` |
| `fieldNames` | 11 | `List<String>` | `private final` |

**Methods:**
| Method | Line | Notes |
|--------|------|-------|
| `StringContainingFilterHandler(String searchText, String... fieldNames)` | 13 | Constructor; wraps searchText with `%...%` for ILIKE; varargs fieldNames |
| `getQueryFilter()` | 19 | Override of `FilterHandler`; single-field path returns `AND x ILIKE ?`; multi-field path builds `AND (x ILIKE ? OR y ILIKE ?)` |
| `prepareStatement(StatementPreparer preparer)` | 33 | Override of `FilterHandler`; iterates fieldNames and calls `preparer.addString(searchText)` once per field |

---

### 2. UnitManufactureFilter.java

**Type:** Interface
**Package:** `com.querybuilder.filters`

**Fields:** None

**Methods:**
| Method | Line | Notes |
|--------|------|-------|
| `manufactureId()` | 4 | Abstract interface method returning `Long` |

---

### 3. UnitManufactureFilterHandler.java

**Class:** `UnitManufactureFilterHandler`
**Implements:** `FilterHandler`
**Package:** `com.querybuilder.filters`

**Fields:**
| Field | Line | Type | Modifier |
|-------|------|------|----------|
| `filter` | 8 | `UnitManufactureFilter` | `private` (non-final) |
| `fieldName` | 9 | `String` | `private final` |

**Methods:**
| Method | Line | Notes |
|--------|------|-------|
| `UnitManufactureFilterHandler(UnitManufactureFilter filter, String fieldName)` | 11 | Constructor |
| `getQueryFilter()` | 16 | Returns `""` if `ignoreFilter()` is true; otherwise returns `AND fieldName = ?` |
| `prepareStatement(StatementPreparer preparer)` | 22 | Override; short-circuits if `ignoreFilter()`; otherwise calls `preparer.addLong(filter.manufactureId())` |
| `ignoreFilter()` | 27 | Private; returns `true` if `filter == null` OR `filter.manufactureId() == null` |

---

## Test Coverage Search Results

**Search target:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`

**Existing test files in test directory:**
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

**Search results:**
| Search Term | Matches Found |
|---|---|
| `StringContainingFilterHandler` | None |
| `UnitManufactureFilter` | None |
| `UnitManufactureFilterHandler` | None |
| `FilterHandler` | None |
| `querybuilder` (package, case-insensitive) | None |

**Conclusion:** Zero test coverage exists for all three source files. No test class, no import, no indirect reference found anywhere in the test directory.

---

## Findings

### StringContainingFilterHandler

**A94-1 | Severity: CRITICAL | No test class exists for StringContainingFilterHandler**
There is no test file anywhere in `src/test/java/` that references `StringContainingFilterHandler`. The class has zero test coverage.

**A94-2 | Severity: CRITICAL | Constructor wrapping logic is untested**
The constructor at line 13–16 wraps `searchText` by prepending and appending `%` to produce the ILIKE pattern (e.g., `"foo"` becomes `"%foo%"`). There is no test verifying this transformation, including edge cases such as empty string (`""` becomes `"%%"`), a string that is already `%`-wrapped, null input (which would produce `"null%"` due to string concatenation), or strings containing SQL wildcard characters.

**A94-3 | Severity: CRITICAL | Single-field branch of getQueryFilter() is untested**
The branch at line 20–21 handles the case where exactly one `fieldName` is provided, returning `" AND fieldName ILIKE ? "`. This code path has no test coverage.

**A94-4 | Severity: CRITICAL | Multi-field branch of getQueryFilter() is untested**
The branch at lines 23–29 handles two or more `fieldNames`, constructing an `AND (x ILIKE ? OR y ILIKE ?)` clause using a `StringBuilder`. The `filter.delete()` call at line 27 removes the trailing ` OR ` from the buffer. There is no test verifying correct clause construction, correct removal of the trailing ` OR `, or correct behavior for exactly two fields, three or more fields, or zero fields (which would produce `" AND () "` with an `IndexOutOfBoundsException` from `delete` on an empty suffix).

**A94-5 | Severity: HIGH | Zero-field constructor edge case is untested**
Passing zero varargs (`fieldNames` is empty) to the constructor produces an empty `fieldNames` list. `getQueryFilter()` takes the multi-field branch (size is 0, not 1), iterates nothing, and then calls `filter.delete(filter.length() - 4, filter.length())` on the string `" AND ("`, whose length is 6, yielding `delete(2, 6)` which truncates to `" A"` rather than throwing an exception or returning a valid clause. This is a latent logic defect with no test exposing it.

**A94-6 | Severity: CRITICAL | prepareStatement() is entirely untested**
The method at lines 33–36 iterates `fieldNames` and calls `preparer.addString(searchText)` once per field, binding the `%searchText%` pattern. There is no test verifying that the correct number of bind calls are made, that the wrapped search text value is bound (not the raw `searchText`), or that `SQLException` propagation behaves correctly.

---

### UnitManufactureFilter

**A94-7 | Severity: MEDIUM | Interface UnitManufactureFilter has no tests for its contract**
Although interfaces cannot be instantiated directly, the contract of `manufactureId()` — specifically that it returns a nullable `Long` — is relied upon by `UnitManufactureFilterHandler.ignoreFilter()`. No tests exist that verify implementing classes correctly satisfy this contract. No mock or anonymous-class implementations appear in any test file.

---

### UnitManufactureFilterHandler

**A94-8 | Severity: CRITICAL | No test class exists for UnitManufactureFilterHandler**
There is no test file anywhere in `src/test/java/` that references `UnitManufactureFilterHandler`. The class has zero test coverage.

**A94-9 | Severity: CRITICAL | getQueryFilter() active-filter path is untested**
The path at line 18 — where `filter` is non-null and `manufactureId()` returns a non-null `Long` — returns `" AND fieldName = ? "`. There is no test verifying the returned string format, that the correct fieldName is interpolated, or the surrounding whitespace.

**A94-10 | Severity: CRITICAL | getQueryFilter() ignored-filter path is untested**
The path at line 17 — where `ignoreFilter()` returns `true` — returns an empty string `""`. There is no test verifying that a null filter or a filter with null `manufactureId()` causes getQueryFilter() to return `""` rather than a SQL fragment.

**A94-11 | Severity: CRITICAL | prepareStatement() active path is untested**
The path at lines 23–24 — where the filter is not ignored — calls `preparer.addLong(filter.manufactureId())`. There is no test verifying that the correct long value is bound or that `SQLException` propagation works.

**A94-12 | Severity: CRITICAL | prepareStatement() early-return path is untested**
The early-return at line 23 when `ignoreFilter()` is true means no bind call is made. There is no test verifying that when the filter is null or returns null `manufactureId()`, `prepareStatement()` does not invoke `preparer.addLong()`.

**A94-13 | Severity: CRITICAL | ignoreFilter() private method logic is untested via any public path**
The two conditions at line 28 — `filter == null` and `filter.manufactureId() == null` — are not exercised through any test. The `filter == null` branch is particularly important because the `filter` field is not `final` and has no null guard at the constructor level (though it is set by the constructor, a null value can be passed legitimately).

**A94-14 | Severity: HIGH | filter field is non-final, allowing post-construction mutation, untested**
The `filter` field at line 8 is declared without `final`. No setter exists, so mutation is not currently possible from outside the class, but the absence of `final` is a defensive-programming gap. More importantly, no test exercises passing a `null` `UnitManufactureFilter` to the constructor to confirm that `ignoreFilter()` returns `true` and both public methods handle the null gracefully.

---

## Summary Table

| ID | Severity | File | Description |
|----|----------|------|-------------|
| A94-1 | CRITICAL | StringContainingFilterHandler | No test class exists |
| A94-2 | CRITICAL | StringContainingFilterHandler | Constructor `%`-wrapping logic untested |
| A94-3 | CRITICAL | StringContainingFilterHandler | Single-field `getQueryFilter()` branch untested |
| A94-4 | CRITICAL | StringContainingFilterHandler | Multi-field `getQueryFilter()` branch untested |
| A94-5 | HIGH | StringContainingFilterHandler | Zero-field constructor/query edge case untested; latent logic defect |
| A94-6 | CRITICAL | StringContainingFilterHandler | `prepareStatement()` entirely untested |
| A94-7 | MEDIUM | UnitManufactureFilter | Interface contract not verified in any test |
| A94-8 | CRITICAL | UnitManufactureFilterHandler | No test class exists |
| A94-9 | CRITICAL | UnitManufactureFilterHandler | `getQueryFilter()` active-filter path untested |
| A94-10 | CRITICAL | UnitManufactureFilterHandler | `getQueryFilter()` ignored-filter path untested |
| A94-11 | CRITICAL | UnitManufactureFilterHandler | `prepareStatement()` active path untested |
| A94-12 | CRITICAL | UnitManufactureFilterHandler | `prepareStatement()` early-return path untested |
| A94-13 | CRITICAL | UnitManufactureFilterHandler | `ignoreFilter()` both conditions untested |
| A94-14 | HIGH | UnitManufactureFilterHandler | Non-final `filter` field; null-constructor path untested |

**Total findings:** 14
**CRITICAL:** 10
**HIGH:** 3
**MEDIUM:** 1
**LOW:** 0
**INFO:** 0
