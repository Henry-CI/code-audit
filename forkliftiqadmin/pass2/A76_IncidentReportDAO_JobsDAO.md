# Pass 2 — Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A76
**Date:** 2026-02-26
**Files Audited:**
1. `src/main/java/com/dao/IncidentReportDAO.java`
2. `src/main/java/com/dao/JobsDAO.java`
**Test Directory:** `src/test/java/`

---

## Section 1 — IncidentReportDAO.java

### Reading Evidence

**Class name:** `IncidentReportDAO`

**Fields (with line numbers):**

| Field | Line |
|-------|------|
| `private static IncidentReportDAO theInstance` | 14 |

**Methods (with line numbers):**

| Method | Line |
|--------|------|
| `public static IncidentReportDAO getInstance()` | 16 |
| `public IncidentReportBean getIncidentReport(int compId, IncidentReportFilterBean filter, String format, String timezone)` | 28 |

**Test grep result:** No matches for `IncidentReportDAO` anywhere in `src/test/java/`. Zero test files exist for this class.

---

### Findings — IncidentReportDAO

**A76-1 | Severity: CRITICAL | No test class exists for IncidentReportDAO**
There is no test file anywhere under `src/test/java/` that references `IncidentReportDAO`. The class has 0% test coverage. Both public methods are entirely untested.

**A76-2 | Severity: HIGH | `getInstance()` singleton uses wrong lock object**
At line 18, the double-checked locking synchronizes on `ImpactReportDAO.class` instead of `IncidentReportDAO.class`. This is a bug: two threads using two different lock objects could both pass the outer `null` check simultaneously and construct two instances. No test covers singleton correctness, thread safety, or the erroneous lock class. A test exercising concurrent `getInstance()` calls would surface this defect.

**A76-3 | Severity: HIGH | `getIncidentReport()` happy-path entirely untested**
`getIncidentReport(compId, filter, format, timezone)` (line 28) delegates directly to `IncidentReportByCompanyIdQuery.query()`. There is no test asserting that: (a) a valid `compId` returns a populated `IncidentReportBean`; (b) the `filter` object is correctly forwarded; (c) the `format` and `timezone` strings are forwarded to the query.

**A76-4 | Severity: HIGH | `getIncidentReport()` SQLException propagation untested**
The method declares `throws SQLException`. No test verifies that a `SQLException` thrown by `IncidentReportByCompanyIdQuery.query()` is correctly propagated to the caller (i.e., not swallowed or wrapped).

**A76-5 | Severity: MEDIUM | `getIncidentReport()` called with null filter — untested**
`IncidentReportByCompanyIdQuery` is constructed with the `filter` argument directly (line 32). No test exercises the case where `filter` is `null`, which would produce a `NullPointerException` inside the query builder.

**A76-6 | Severity: MEDIUM | `getIncidentReport()` called with null/empty format or timezone — untested**
`format` and `timezone` are `String` parameters with no null checks. No test exercises null, empty string, or invalid timezone/format values. Passing `null` may cause silent failures or `NullPointerException` in `DateUtil.formatDateTime`.

**A76-7 | Severity: MEDIUM | `getIncidentReport()` with zero or negative companyId — untested**
No test validates behaviour when `compId` is `0` or negative, which would result in a query returning no rows or unexpected data. The method has no guard clause.

**A76-8 | Severity: LOW | Singleton `getInstance()` not tested for repeated-call identity**
No test asserts that multiple sequential calls to `getInstance()` return the same object reference.

**A76-9 | Severity: INFO | `@NoArgsConstructor` constructor is `public` via Lombok — no test**
The Lombok `@NoArgsConstructor` generates a public no-arg constructor (line 12), allowing callers to bypass the singleton and instantiate the DAO directly. No test documents or restricts this behaviour. The singleton contract is unenforced.

---

## Section 2 — JobsDAO.java

### Reading Evidence

**Class name:** `JobsDAO`

**Fields (with line numbers):**

| Field | Line |
|-------|------|
| `private static Logger log` | 24 |
| `private DriverDAO driverDAO` | 26 |

**Methods (with line numbers):**

| Method | Line |
|--------|------|
| `public ArrayList<JobDetailsBean> getJobList(String equipId)` | 34 |
| `public ArrayList<JobDetailsBean> getJobListByJobId(String equipId, String jobNo)` | 108 |
| `public boolean addJob(JobDetailsBean jobdetails)` | 178 |
| `public boolean editJob(JobDetailsBean jobdetails)` | 261 |

**Test grep result:** No matches for `JobsDAO` anywhere in `src/test/java/`. Zero test files exist for this class.

---

### Findings — JobsDAO

**A76-10 | Severity: CRITICAL | SQL injection in `getJobList()` via `equipId` parameter (line 52)**
The query at line 52 concatenates the caller-supplied `equipId` String directly into the SQL string:
```java
"where j.unit_id = " + equipId
```
A `Statement` (not `PreparedStatement`) is used to execute this query. There is no type validation, parsing, or sanitisation of `equipId` before it is embedded. Any caller who controls `equipId` can inject arbitrary SQL. No test exercises this with a malicious payload. This is the highest-severity class of vulnerability.

**A76-11 | Severity: CRITICAL | SQL injection in `getJobListByJobId()` via both `equipId` and `jobNo` parameters (line 123)**
The single-line query at line 123 concatenates both `equipId` and `jobNo` directly into the SQL string using a `Statement`:
```java
"... and j.unit_id = " + equipId + " and j.job_no = '" + jobNo + "' ..."
```
`jobNo` is a string value wrapped in single quotes, making it trivially injectable with a payload such as `'; DROP TABLE jobs; --`. No test exercises either parameter with adversarial input. Two independent injection points exist in the same query.

**A76-12 | Severity: CRITICAL | No test class exists for JobsDAO**
There is no test file anywhere under `src/test/java/` that references `JobsDAO`. All four public methods have 0% test coverage.

**A76-13 | Severity: HIGH | `getJobList()` happy-path entirely untested**
No test verifies that `getJobList(equipId)` returns a correctly populated `ArrayList<JobDetailsBean>` for a valid equipment ID, or that it returns an empty list when no jobs exist.

**A76-14 | Severity: HIGH | `getJobList()` — NullPointerException when `driverDAO.getDriverById()` returns null (line 64)**
At line 64, `driver.getFirst_last()` is called on the return value of `driverDAO.getDriverById(rs.getLong(3))` without any null check. If no driver exists for the given `driver_id` (e.g., orphaned job_allocation row), a `NullPointerException` is thrown. The catch block at line 77 catches it and re-wraps it as a `SQLException`, silently discarding the original error type and the partially built list. No test covers this scenario.

**A76-15 | Severity: HIGH | `getJobListByJobId()` happy-path entirely untested**
No test verifies that `getJobListByJobId(equipId, jobNo)` returns a correctly populated list with session-level data (including `event` mapped to `status`), or that it returns an empty list when the job number is not found.

**A76-16 | Severity: HIGH | `getJobListByJobId()` — same NullPointerException risk from null DriverBean (line 134)**
Identical pattern to A76-14: `driver.getFirst_last()` at line 135 is called without checking whether `driverDAO.getDriverById()` returns null. No test covers this.

**A76-17 | Severity: HIGH | `addJob()` — non-atomic ID generation creates race condition (lines 195–213)**
`addJob()` first queries `max(id)+1 from jobs` in one statement, then uses that value in a subsequent `INSERT`. Between these two operations another concurrent `addJob()` call can obtain the same `max(id)+1`, resulting in a primary key conflict or a silent duplicate `job_no`. No test exercises concurrent inserts or the failure path when `executeUpdate()` returns a value other than 1.

**A76-18 | Severity: HIGH | `addJob()` — `job_id` set to `"0"` when `max(id)` query returns no rows (line 201)**
If the `jobs` table is empty, `max(id)` returns SQL `NULL`; `rs.getString(1)` returns `null` (not `"0"`), and the initialised fallback value of `"0"` is used. `Integer.parseInt("0")` succeeds, inserting `id = 0`. No test covers this edge case or validates that the first inserted job receives a sensible ID.

**A76-19 | Severity: HIGH | `addJob()` — `Integer.parseInt(job_id)` will throw `NumberFormatException` if `rs.getString(1)` returns null (line 213)**
When `max(id)` returns SQL NULL and `rs.getString(1)` is Java `null`, the fallback of `"0"` is used. However if `rs.next()` is not entered (empty result set — though unlikely for aggregate), `job_id` stays `"0"`. The real risk is if a future code change alters the fallback; the `parseInt` call is entirely untested.

**A76-20 | Severity: HIGH | `editJob()` happy-path entirely untested**
No test verifies that `editJob()` with a valid `JobDetailsBean` results in `executeUpdate()` returning 1 and the method returning `true`.

**A76-21 | Severity: HIGH | `editJob()` — no test for update affecting zero rows**
When `ps.executeUpdate()` returns 0 (job ID does not exist), the method returns `false`. No test asserts this behaviour or that the `false` return is handled correctly by callers.

**A76-22 | Severity: HIGH | `addJob()` happy-path entirely untested**
No test verifies that `addJob()` with a valid `JobDetailsBean` inserts a row and returns `true`.

**A76-23 | Severity: MEDIUM | `getJobList()` — `equipId` null or empty string — untested**
Passing `null` or `""` for `equipId` produces invalid SQL (`where j.unit_id = null` or `where j.unit_id = `). No null/empty guard exists and no test covers these inputs.

**A76-24 | Severity: MEDIUM | `getJobListByJobId()` — `jobNo` null produces invalid SQL — untested**
Concatenating `null` for `jobNo` produces the SQL fragment `j.job_no = 'null'`, which will silently return zero rows instead of raising an error. No test covers this.

**A76-25 | Severity: MEDIUM | `addJob()` — null `jobdetails` returns false silently (line 223)**
When `jobdetails` is `null`, the method returns `false` at line 224 with no exception and no log message beyond the initial entry log. No test asserts this contract.

**A76-26 | Severity: MEDIUM | `editJob()` — null `jobdetails` returns false silently (line 290)**
Same pattern as A76-25. The `null` guard at line 277 returns `false` without logging or throwing. No test asserts this.

**A76-27 | Severity: MEDIUM | Exception type loss: `Exception` silently re-thrown as `SQLException` in all four methods**
All four methods catch `Exception` and re-throw `new SQLException(e.getMessage())`, discarding the original exception type, stack trace root cause, and structured error information. No test verifies what exception type is raised or that the message is correctly preserved.

**A76-28 | Severity: MEDIUM | Resource leak risk: `ResultSet` and `Statement` close in `finally` can themselves throw — untested**
In all four methods, `rs.close()` and `stmt.close()` in the `finally` block are called sequentially without try-catch. If `rs.close()` throws, `stmt.close()` is never called, leaking the statement. No test exercises this failure path. Using try-with-resources would eliminate the risk, but that refactor is not possible here; the gap must be documented.

**A76-29 | Severity: MEDIUM | `addJob()` — `ps.close()` declared but `ps` can be null and the close is guarded — close order risk**
In `addJob()`, `rs` and `stmt` are closed before `ps` in the `finally` block. If `rs.close()` throws (see A76-28), `ps` is never closed. No test exercises close-ordering failure.

**A76-30 | Severity: LOW | `JobsDAO` has no `getInstance()` singleton pattern — instantiation contract undocumented and untested**
Unlike most other DAOs in the package, `JobsDAO` has no `getInstance()` factory method. It is instantiated with `new JobsDAO()` by callers. The field `private DriverDAO driverDAO = DriverDAO.getInstance()` is initialised at field-declaration time (line 26), but there is no test confirming correct construction or that `driverDAO` is non-null post-construction.

**A76-31 | Severity: LOW | Unused import `com.sun.tools.xjc.Driver` (line 17)**
The import references an internal JDK class (`xjc.Driver`) that is unrelated to the class functionality, will cause compilation warnings, and may break on JDK versions that no longer export this package. No test would catch a compilation failure caused by this import being unavailable.

**A76-32 | Severity: INFO | `getJobList()` log message says "LoginDAO Method" instead of "JobsDAO Method" (line 36)**
The info log at line 36 reads `"Inside LoginDAO Method : getJobList"` — a copy-paste error from another DAO. Similarly, line 110 reads `"Inside LoginDAO Method : getJobListByJobId"`. No test verifies log output, but the mislabelled logs would hinder production debugging.

**A76-33 | Severity: INFO | `getJobListByJobId()` uses `job_allocation` via implicit inner join (INNER JOIN semantics), unlike `getJobList()` which uses LEFT OUTER JOIN**
`getJobList()` uses a `LEFT OUTER JOIN` on `job_allocation` (line 51), meaning jobs without an allocation are included. `getJobListByJobId()` at line 123 uses the comma-separated (implicit inner join) syntax for `job_allocation`, meaning jobs without an allocation are excluded. This behavioural inconsistency is not documented or tested and may produce unexpected missing-data results.

---

## Summary Table

| Finding | Severity | Class |
|---------|----------|-------|
| A76-1 | CRITICAL | IncidentReportDAO |
| A76-2 | HIGH | IncidentReportDAO |
| A76-3 | HIGH | IncidentReportDAO |
| A76-4 | HIGH | IncidentReportDAO |
| A76-5 | MEDIUM | IncidentReportDAO |
| A76-6 | MEDIUM | IncidentReportDAO |
| A76-7 | MEDIUM | IncidentReportDAO |
| A76-8 | LOW | IncidentReportDAO |
| A76-9 | INFO | IncidentReportDAO |
| A76-10 | CRITICAL | JobsDAO |
| A76-11 | CRITICAL | JobsDAO |
| A76-12 | CRITICAL | JobsDAO |
| A76-13 | HIGH | JobsDAO |
| A76-14 | HIGH | JobsDAO |
| A76-15 | HIGH | JobsDAO |
| A76-16 | HIGH | JobsDAO |
| A76-17 | HIGH | JobsDAO |
| A76-18 | HIGH | JobsDAO |
| A76-19 | HIGH | JobsDAO |
| A76-20 | HIGH | JobsDAO |
| A76-21 | HIGH | JobsDAO |
| A76-22 | HIGH | JobsDAO |
| A76-23 | MEDIUM | JobsDAO |
| A76-24 | MEDIUM | JobsDAO |
| A76-25 | MEDIUM | JobsDAO |
| A76-26 | MEDIUM | JobsDAO |
| A76-27 | MEDIUM | JobsDAO |
| A76-28 | MEDIUM | JobsDAO |
| A76-29 | MEDIUM | JobsDAO |
| A76-30 | LOW | JobsDAO |
| A76-31 | LOW | JobsDAO |
| A76-32 | INFO | JobsDAO |
| A76-33 | INFO | JobsDAO |

**Total findings: 33**
- CRITICAL: 4
- HIGH: 13
- MEDIUM: 9
- LOW: 3
- INFO: 4
