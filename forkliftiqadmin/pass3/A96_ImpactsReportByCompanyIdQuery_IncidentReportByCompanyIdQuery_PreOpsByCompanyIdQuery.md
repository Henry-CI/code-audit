# Pass 3 Documentation Audit — Agent A96
**Audit run:** 2026-02-26-01
**Files audited:**
- `querybuilder/impacts/ImpactsReportByCompanyIdQuery.java`
- `querybuilder/incidents/IncidentReportByCompanyIdQuery.java`
- `querybuilder/preops/PreOpsByCompanyIdQuery.java`

---

## File 1: ImpactsReportByCompanyIdQuery.java

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/querybuilder/impacts/ImpactsReportByCompanyIdQuery.java`

### Reading Evidence

**Class:** `ImpactsReportByCompanyIdQuery` — line 17

**Fields:**
| Name | Type | Line |
|------|------|------|
| `companyId` | `long` (final) | 18 |
| `filterHandlers` | `List<FilterHandler>` | 19 |

**Methods:**
| Name | Visibility | Line |
|------|-----------|------|
| `ImpactsReportByCompanyIdQuery(long companyId, ImpactReportFilterBean filter)` | package-private | 21 |
| `query(String timezone, String dateFormat)` | public | 31 |
| `getQuery()` | private | 39 |
| `prepareStatement(PreparedStatement statement)` | private | 45 |
| `getResults(String timezone, String dateFormat, ResultSet rs)` | private | 52 |

### Javadoc Analysis

- **Class-level Javadoc:** None present.
- **Constructor `ImpactsReportByCompanyIdQuery`** (line 21): No Javadoc. Visibility is package-private, not public.
- **`query(String timezone, String dateFormat)`** (line 31): Public method. No Javadoc present.
- **`getQuery()`** (line 39): Private — not in scope for public Javadoc audit.
- **`prepareStatement(PreparedStatement statement)`** (line 45): Private — not in scope.
- **`getResults(String timezone, String dateFormat, ResultSet rs)`** (line 52): Private — not in scope.

### Implementation Notes

`query()` executes a filtered SQL query for impacts grouped by unit for a given company. It builds grouped `ImpactReportGroupBean` objects and sorts the resulting list before wrapping in `ImpactReportBean`. The parameters `timezone` and `dateFormat` are passed through to timestamp formatting.

---

## File 2: IncidentReportByCompanyIdQuery.java

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/querybuilder/incidents/IncidentReportByCompanyIdQuery.java`

### Reading Evidence

**Class:** `IncidentReportByCompanyIdQuery` — line 21

**Fields:**
| Name | Type | Line |
|------|------|------|
| `BASE_QUERY` | `static final String` | 22 |
| `companyId` | `int` (final) | 29 |
| `filterHandlers` | `List<FilterHandler>` | 30 |

**Methods:**
| Name | Visibility | Line |
|------|-----------|------|
| `IncidentReportByCompanyIdQuery(int companyId, IncidentReportFilterBean filter)` | public | 32 |
| `query(String timezone, String dateFormat)` | public | 41 |
| `getQuery()` | private | 47 |
| `prepareStatement(PreparedStatement statement)` | private | 54 |
| `mapResult(String timezone, String dateFormat, ResultSet result)` | private | 61 |

### Javadoc Analysis

- **Class-level Javadoc:** None present.
- **Constructor `IncidentReportByCompanyIdQuery(int companyId, IncidentReportFilterBean filter)`** (line 32): Public. No Javadoc present.
- **`query(String timezone, String dateFormat)`** (line 41): Public method. No Javadoc present.
- **`getQuery()`** (line 47): Private — not in scope.
- **`prepareStatement(PreparedStatement statement)`** (line 54): Private — not in scope.
- **`mapResult(String timezone, String dateFormat, ResultSet result)`** (line 61): Private — not in scope.

### Implementation Notes

The constructor takes `int companyId` while `prepareStatement()` (line 56–57) binds it as `Long` via `preparer.addLong(companyId)`. This is a widening conversion (int -> long) and is functionally correct, but the type inconsistency between the field declaration and the binding call warrants a note.

`query()` executes the incident report SQL with filters applied, mapping each result row to an `IncidentReportEntryBean` and returning an `IncidentReportBean`. Results are ordered by `event_time DESC` in SQL.

---

## File 3: PreOpsByCompanyIdQuery.java

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/querybuilder/preops/PreOpsByCompanyIdQuery.java`

### Reading Evidence

**Class:** `PreOpsByCompanyIdQuery` — line 5

**Fields:**
| Name | Type | Line |
|------|------|------|
| `BASE_QUERY` | `static final String` (private) | 6 |
| `COUNT_QUERY` | `static final String` (package-private) | 9 |
| `REPORT_QUERY` | `static final String` (package-private) | 13 |

**Methods:**
| Name | Visibility | Line |
|------|-----------|------|
| `report(long companyId, PreOpsReportFilterBean filter)` | public static | 16 |
| `count(long companyId, String timezone)` | public static | 20 |

### Javadoc Analysis

- **Class-level Javadoc:** None present.
- **`report(long companyId, PreOpsReportFilterBean filter)`** (line 16): Public static factory method. No Javadoc present.
- **`count(long companyId, String timezone)`** (line 20): Public static factory method. No Javadoc present.

### Implementation Notes

`PreOpsByCompanyIdQuery` is a factory class exposing two static factory methods that construct sibling query objects (`PreOpsReportByCompanyIdQuery` and `PreOpsCountByCompanyIdQuery`). The class also holds shared SQL fragment constants (`BASE_QUERY`, `COUNT_QUERY`, `REPORT_QUERY`) used by the sibling classes. The factory pattern is not documented anywhere in the class.

---

## Findings Summary

| ID | File | Location | Severity | Description |
|----|------|----------|----------|-------------|
| A96-1 | `ImpactsReportByCompanyIdQuery.java` | Class (line 17) | LOW | No class-level Javadoc. The class purpose (query impacts data for a company with filters) is not described. |
| A96-2 | `ImpactsReportByCompanyIdQuery.java` | `query()` line 31 | MEDIUM | Public method `query(String timezone, String dateFormat)` has no Javadoc. Method is non-trivial: it executes a filtered SQL query, groups results by unit, sorts groups, and returns an `ImpactReportBean`. Missing `@param` for `timezone` and `dateFormat`, and `@return` and `@throws SQLException`. |
| A96-3 | `IncidentReportByCompanyIdQuery.java` | Class (line 21) | LOW | No class-level Javadoc. The class purpose (query incident report data for a company with optional filters) is not described. |
| A96-4 | `IncidentReportByCompanyIdQuery.java` | Constructor line 32 | MEDIUM | Public constructor `IncidentReportByCompanyIdQuery(int companyId, IncidentReportFilterBean filter)` has no Javadoc. Non-trivial: it initialises three filter handlers wired to specific SQL column names. Missing `@param` for `companyId` and `filter`. |
| A96-5 | `IncidentReportByCompanyIdQuery.java` | `query()` line 41 | MEDIUM | Public method `query(String timezone, String dateFormat)` has no Javadoc. Method is non-trivial: executes filtered SQL, maps rows to beans, returns `IncidentReportBean`. Missing `@param` for `timezone` and `dateFormat`, and `@return` and `@throws SQLException`. |
| A96-6 | `PreOpsByCompanyIdQuery.java` | Class (line 5) | LOW | No class-level Javadoc. The class acts as a factory and SQL constant holder; its role and the factory pattern used are not described. |
| A96-7 | `PreOpsByCompanyIdQuery.java` | `report()` line 16 | MEDIUM | Public static factory method `report(long companyId, PreOpsReportFilterBean filter)` has no Javadoc. Purpose (create a `PreOpsReportByCompanyIdQuery`) is non-obvious from the signature alone. Missing `@param` for `companyId` and `filter`, and `@return`. |
| A96-8 | `PreOpsByCompanyIdQuery.java` | `count()` line 20 | MEDIUM | Public static factory method `count(long companyId, String timezone)` has no Javadoc. Purpose (create a `PreOpsCountByCompanyIdQuery`) is non-obvious. Missing `@param` for `companyId` and `timezone`, and `@return`. |

---

## Statistics

| Severity | Count |
|----------|-------|
| HIGH | 0 |
| MEDIUM | 5 |
| LOW | 3 |
| **Total** | **8** |
