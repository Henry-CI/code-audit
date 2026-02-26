# Pass 3 Documentation Audit — A76
**Audit run:** 2026-02-26-01
**Agent:** A76
**Files:**
- `dao/IncidentReportDAO.java`
- `dao/JobsDAO.java`

---

## 1. IncidentReportDAO.java

### Reading Evidence

| Element | Kind | Line |
|---------|------|------|
| `IncidentReportDAO` | class | 13 |
| `theInstance` | field — `static IncidentReportDAO` | 14 |
| `getInstance()` | method — `public static IncidentReportDAO` | 16 |
| `getIncidentReport(int, IncidentReportFilterBean, String, String)` | method — `public IncidentReportBean` | 28–33 |

No other fields (Lombok `@NoArgsConstructor` generates the constructor; `@Slf4j` generates `log`).

### Javadoc Analysis

**Class-level Javadoc:** None present.

**`getInstance()` (line 16):** No Javadoc present.

**`getIncidentReport(...)` (line 28):** No Javadoc present.

### Additional Code Issue Noted

The `getInstance()` method (line 18) synchronises on `ImpactReportDAO.class` instead of `IncidentReportDAO.class`. This is a functional bug (wrong lock class) unrelated to documentation, but is noted here because any future Javadoc added to this method would need to avoid describing the lock as correct.

---

## 2. JobsDAO.java

### Reading Evidence

| Element | Kind | Line |
|---------|------|------|
| `JobsDAO` | class | 21 |
| `log` | field — `static Logger` | 24 |
| `driverDAO` | field — `DriverDAO` | 26 |
| `getJobList(String)` | method — `public ArrayList<JobDetailsBean>` | 34 |
| `getJobListByJobId(String, String)` | method — `public ArrayList<JobDetailsBean>` | 108 |
| `addJob(JobDetailsBean)` | method — `public boolean` | 178 |
| `editJob(JobDetailsBean)` | method — `public boolean` | 261 |

No constructor declared (default constructor implied).

### Javadoc Analysis

**Class-level Javadoc:** None present.

**`getJobList(String equipId)` (line 34):**
No Javadoc. A `/* ... */` block comment (lines 28–33) precedes the method but is a plain block comment, not a Javadoc comment (`/** ... */`). It describes a modification history entry, not the method's contract, parameters, or return value.

**`getJobListByJobId(String equipId, String jobNo)` (line 108):**
No Javadoc. A `/* ... */` plain block comment (lines 102–107) describes modification history only; not a Javadoc comment.

**`addJob(JobDetailsBean jobdetails)` (line 178):**
No Javadoc. A `/* ... */` plain block comment (lines 173–177) describes creation history only.

**`editJob(JobDetailsBean jobdetails)` (line 261):**
No Javadoc. A `/* ... */` plain block comment (lines 256–260) describes creation history only.

---

## Findings

### A76-1 — LOW — IncidentReportDAO: Missing class-level Javadoc
**File:** `dao/IncidentReportDAO.java`, line 13
**Detail:** The `IncidentReportDAO` class has no class-level Javadoc comment. There is no description of the class purpose, its singleton lifecycle, or the domain it serves.

---

### A76-2 — MEDIUM — IncidentReportDAO: `getInstance()` undocumented non-trivial public method
**File:** `dao/IncidentReportDAO.java`, line 16
**Detail:** `getInstance()` is a public, non-trivial static factory method implementing a double-checked locking singleton pattern. It has no Javadoc. A reader must inspect the body to understand the threading model and lifecycle. No `@return` tag is present.

---

### A76-3 — MEDIUM — IncidentReportDAO: `getIncidentReport(...)` undocumented non-trivial public method
**File:** `dao/IncidentReportDAO.java`, line 28
**Detail:** `getIncidentReport(int compId, IncidentReportFilterBean filter, String format, String timezone)` is a public, non-trivial method that performs a parameterised database query. It has no Javadoc. The roles of `format` and `timezone` are not described anywhere. No `@param` or `@return` tags are present, and the declared `throws SQLException` is not documented with `@throws`.

---

### A76-4 — LOW — JobsDAO: Missing class-level Javadoc
**File:** `dao/JobsDAO.java`, line 21
**Detail:** The `JobsDAO` class has no class-level Javadoc comment.

---

### A76-5 — MEDIUM — JobsDAO: `getJobList(String)` undocumented non-trivial public method
**File:** `dao/JobsDAO.java`, line 34
**Detail:** `getJobList(String equipId)` executes a SQL query joining `jobs` and `job_allocation` tables, populates driver details from `DriverDAO`, and returns a list of job records. It has no Javadoc. The plain block comment above it (lines 28–33) is a change-log entry, not a method description. No `@param`, `@return`, or `@throws` tags are present.

---

### A76-6 — MEDIUM — JobsDAO: `getJobListByJobId(String, String)` undocumented non-trivial public method
**File:** `dao/JobsDAO.java`, line 108
**Detail:** `getJobListByJobId(String equipId, String jobNo)` executes a multi-table SQL query (joining `jobs`, `job_allocation`, and `job_sessions`) and also populates session event/status data. It has no Javadoc. The plain block comment above (lines 102–107) is a change-log entry only. No `@param`, `@return`, or `@throws` tags are present.

---

### A76-7 — MEDIUM — JobsDAO: `addJob(JobDetailsBean)` undocumented non-trivial public method
**File:** `dao/JobsDAO.java`, line 178
**Detail:** `addJob(JobDetailsBean jobdetails)` performs a non-atomic two-step database operation: it first selects `max(id)+1` to derive a new ID, then inserts a new jobs row using a `PreparedStatement`. It has no Javadoc. The plain block comment above (lines 173–177) is a creation-log entry only. No `@param`, `@return`, or `@throws` tags are present. The non-atomic ID generation strategy is particularly worth documenting for maintainers.

---

### A76-8 — MEDIUM — JobsDAO: `editJob(JobDetailsBean)` undocumented non-trivial public method
**File:** `dao/JobsDAO.java`, line 261
**Detail:** `editJob(JobDetailsBean jobdetails)` performs a targeted `UPDATE` against the `jobs` table updating `description` and `job_title` fields by `id`. It has no Javadoc. The plain block comment above (lines 256–260) is a creation-log entry only. No `@param`, `@return`, or `@throws` tags are present.

---

## Summary Table

| ID | Severity | File | Location | Issue |
|----|----------|------|----------|-------|
| A76-1 | LOW | IncidentReportDAO.java | line 13 | No class-level Javadoc |
| A76-2 | MEDIUM | IncidentReportDAO.java | line 16 | `getInstance()` has no Javadoc; missing `@return` |
| A76-3 | MEDIUM | IncidentReportDAO.java | line 28 | `getIncidentReport(...)` has no Javadoc; missing `@param`, `@return`, `@throws` |
| A76-4 | LOW | JobsDAO.java | line 21 | No class-level Javadoc |
| A76-5 | MEDIUM | JobsDAO.java | line 34 | `getJobList(...)` has no Javadoc; missing `@param`, `@return`, `@throws` |
| A76-6 | MEDIUM | JobsDAO.java | line 108 | `getJobListByJobId(...)` has no Javadoc; missing `@param`, `@return`, `@throws` |
| A76-7 | MEDIUM | JobsDAO.java | line 178 | `addJob(...)` has no Javadoc; missing `@param`, `@return`, `@throws` |
| A76-8 | MEDIUM | JobsDAO.java | line 261 | `editJob(...)` has no Javadoc; missing `@param`, `@return`, `@throws` |

**Total findings: 8** (2 LOW, 6 MEDIUM, 0 HIGH)
