# Pass 2 Test-Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A63
**Source Files:**
- `src/main/java/com/calibration/CalibrationJobScheduler.java`
- `src/main/java/com/calibration/UnitCalibration.java`

**Test File:**
- `src/test/java/com/calibration/UnitCalibrationTest.java`

---

## 1. Reading-Evidence Blocks

### 1.1 CalibrationJobScheduler.java

**Class:** `CalibrationJobScheduler` (line 14)
**Implements:** `javax.servlet.ServletContextListener`
**Package:** `com.calibration`

**Fields:** none declared.

**Methods:**

| Method | Lines | Access | Notes |
|---|---|---|---|
| `contextInitialized(ServletContextEvent)` | 16–33 | `public` (override) | Builds Quartz `JobDetail` and `CronTrigger` for `CalibrationJob`; obtains a `Scheduler` via `StdSchedulerFactory`; calls `scheduleJob` and `start`; catches `SchedulerException` and prints stack trace. |
| `contextDestroyed(ServletContextEvent)` | 36–38 | `public` (override) | Instantiates a `ServletException` with message "Application Stopped" and immediately calls `printStackTrace()` on it; does nothing meaningful to stop the scheduler. |

**Cron expression:** `"0 0 * * * ?"` — fires at the top of every hour.

---

### 1.2 UnitCalibration.java

**Class:** `UnitCalibration` (line 11)
**Annotations:** `@Builder`, `@Getter` (Lombok)
**Package:** `com.calibration`

**Fields:**

| Field | Type | Line | Access |
|---|---|---|---|
| `unitId` | `long` | 12 | `private final` |
| `resetCalibrationDate` | `Timestamp` | 13 | `private` |
| `calibrationDate` | `Timestamp` | 14 | `private` |
| `threshold` | `int` | 15 | `private` |
| `impacts` | `List<Integer>` | 16 | `private` |

**Constructor:** package-private all-args constructor (lines 18–28), generated matching the `@Builder` annotation.

**Methods:**

| Method | Lines | Access | Notes |
|---|---|---|---|
| `isCalibrated()` | 30–34 | `public` | Returns `true` if any of the three private helper conditions are met (OR logic). |
| `unitCalibrationNeverReset()` | 36–38 | `private` | `resetCalibrationDate == null && calibrationDate == null && threshold != 0` |
| `unitCalibrationDateAndThresholdSet()` | 40–42 | `private` | `calibrationDate != null && threshold != 0` |
| `calibrationDone()` | 44–46 | `private` | `impacts != null && impacts.size() >= 100` |
| `getCalculatedThreshold()` | 48–51 | `int` (package-private) | Returns `(int)(average() + standardDeviation(average()))` |
| `average()` | 53–57 | `private` | Sum of all impacts divided by `impacts.size()` |
| `standardDeviation(double)` | 59–63 | `private` | Population standard deviation (divides by N, not N-1). |
| `calibrationPercentage()` | 65–69 | `public` | Returns 100 if `isCalibrated()`; 0 if `impacts == null`; otherwise `impacts.size()` capped at 100. |

---

## 2. Test File — @Test Methods

**Class:** `UnitCalibrationTest` (line 13)

| # | Test Method Name | Line | What It Exercises |
|---|---|---|---|
| 1 | `returnsZeroPercentCompleteIfNoImpactsAdded` | 15 | `calibrationPercentage()` returns 0 when `UnitCalibration` built with no fields; `isCalibrated()` returns false. |
| 2 | `returnsTenPercentCompleteIfTenImpactsAdded` | 23 | `calibrationPercentage()` returns 10 with 10 impacts; `isCalibrated()` returns false. |
| 3 | `returnsHundredPercentCompleteIfMoreThanHundredImpactsAdded` | 33 | `calibrationPercentage()` returns 100 with 111 impacts; `isCalibrated()` returns true via `calibrationDone()` (size >= 100). |
| 4 | `returnsCalibratedIfCalibrationDateAndThresholdAreSet` | 43 | `isCalibrated()` true when `calibrationDate` and `threshold` set (exercises `unitCalibrationDateAndThresholdSet()`). |
| 5 | `returnsCalibratingIfCalibrationDateIsNotSet` | 54 | `isCalibrated()` false when `resetCalibrationDate` and `threshold` are set but `calibrationDate` is null; exercises false path of `unitCalibrationDateAndThresholdSet()` and false path of `unitCalibrationNeverReset()` (reset date is present). |
| 6 | `returnsCalibratingIfThresholdIsNotSet` | 65 | `isCalibrated()` false when both dates set but `threshold` is 0; exercises false paths of both date/threshold checks. |
| 7 | `returnsCalibratedIfThresholdSetAndResetCalibrationDateNotSet` | 76 | `isCalibrated()` true when only `threshold` is set (exercises `unitCalibrationNeverReset()` true path). |
| 8 | `calculatesThresholdAsAveragePlusStandardDeviation` | 87 | `getCalculatedThreshold()` with 64 real-world impact values; exercises `average()` and `standardDeviation()` indirectly. |

**Helper:** `makeImpacts(int count)` (line 102) — builds a `List<Integer>` of sequential integers 0..count-1.

---

## 3. Source-Method to Test-Method Coverage Map

### UnitCalibration

| Source Method | Covered By Test(s) | Coverage Status |
|---|---|---|
| Constructor (all-args, via builder) | All 8 tests | Covered |
| `isCalibrated()` | Tests 1, 2, 3, 4, 5, 6, 7 | Covered (multiple paths) |
| `unitCalibrationNeverReset()` (private) | Tests 5 (false), 7 (true) | Both branches exercised indirectly |
| `unitCalibrationDateAndThresholdSet()` (private) | Tests 4 (true), 5 (false), 6 (false) | Multiple paths exercised indirectly |
| `calibrationDone()` (private) | Tests 3 (true — 111 impacts), 1 & 2 (false) | Both branches exercised indirectly |
| `getCalculatedThreshold()` | Test 8 | Covered — single happy-path only |
| `average()` (private) | Test 8 | Covered — single happy-path only |
| `standardDeviation(double)` (private) | Test 8 | Covered — single happy-path only |
| `calibrationPercentage()` | Tests 1 (0%), 2 (10%), 3 (100% via isCalibrated), 4 (100% via isCalibrated) | Partially covered — see gaps |

### CalibrationJobScheduler

| Source Method | Covered By Test(s) | Coverage Status |
|---|---|---|
| `contextInitialized(ServletContextEvent)` | None | NOT COVERED |
| `contextDestroyed(ServletContextEvent)` | None | NOT COVERED |

---

## 4. Coverage Gaps and Findings

---

### A63-1 | Severity: CRITICAL | `CalibrationJobScheduler` has zero test coverage

`CalibrationJobScheduler` is a `ServletContextListener` that schedules a Quartz job on application startup. Neither `contextInitialized` nor `contextDestroyed` has any test coverage whatsoever. Failures in scheduler initialization are silently swallowed by a bare `e.printStackTrace()` (no re-throw, no logging framework, no alerting), meaning a broken scheduler could go undetected in production. There is no integration or unit test verifying that the Quartz scheduler starts, that the cron expression is valid, or that `CalibrationJob` is correctly registered.

**Untested paths:**
- Normal happy path: scheduler initializes, job is scheduled, scheduler starts.
- `SchedulerException` path: exception is caught and only printed — no test verifies recovery behavior or that the exception is at least surfaced.

---

### A63-2 | Severity: CRITICAL | `contextDestroyed` is functionally broken and untested

`contextDestroyed` (line 36–38) does not shut down the Quartz scheduler. Instead it instantiates a `new ServletException("Application Stopped")` and calls `printStackTrace()` on it, which is logically nonsensical: it treats application shutdown as an error condition, creates an exception object solely to print a stack trace as a log message, and never calls `scheduler.shutdown()`. The Quartz scheduler will continue running threads after context destruction, risking thread leaks in servlet containers. There is no test to catch this behavioral defect.

---

### A63-3 | Severity: HIGH | `getCalculatedThreshold()` is not tested with null or empty `impacts`

`getCalculatedThreshold()` calls `average()`, which iterates over `impacts` and divides by `impacts.size()`. If `impacts` is `null`, line 55 throws a `NullPointerException`. If `impacts` is an empty list (`size() == 0`), line 56 causes an `ArithmeticException` (integer divide by zero) or `Double.NaN`/`Infinity` (floating-point). The single test (Test 8) provides 64 non-zero impacts. There are no tests for:
- `impacts == null` → `NullPointerException`
- `impacts` empty list → division by zero
- `impacts` with a single element → degenerate standard deviation of 0 (valid but unchecked)

---

### A63-4 | Severity: HIGH | `calibrationPercentage()` branch `impacts.size() > 100 ? 100 : impacts.size()` is not directly tested at the exact boundary

`calibrationPercentage()` (line 68) uses `impacts.size() > 100` to cap at 100. The existing tests use 111 impacts (over 100) and 10 impacts (under 100). The exact boundary value of exactly 100 impacts is never tested. At exactly 100, `calibrationDone()` returns `true` (size >= 100), so `isCalibrated()` returns `true`, and `calibrationPercentage()` returns 100 via the first branch (line 66) — but the `impacts.size() > 100` cap branch (line 68) is never reached with exactly 100 since `isCalibrated()` short-circuits it. This means the `> 100` vs `>= 100` discrepancy is a latent logical inconsistency: `calibrationDone()` uses `>= 100` but the cap uses `> 100`. No test covers exactly 100 impacts to expose this asymmetry.

---

### A63-5 | Severity: HIGH | `isCalibrated()` does not have a test for the composite `calibrationDone()` condition at exactly 100 impacts

`calibrationDone()` returns true when `impacts.size() >= 100`. The nearest test uses 111 impacts. There is no test confirming behavior at exactly 100 impacts, which is the advertised calibration threshold. This is especially important given the boundary inconsistency described in A63-4.

---

### A63-6 | Severity: HIGH | `unitCalibrationNeverReset()` true-path condition not fully isolated

`unitCalibrationNeverReset()` (line 36–38) requires `resetCalibrationDate == null && calibrationDate == null && threshold != 0`. Test 7 exercises this but uses a builder that also leaves `impacts` as null — so the `unitCalibrationNeverReset()` short-circuit fires before `calibrationDone()` is even evaluated. There is no test that sets `threshold != 0` but also provides exactly 99 impacts (enough to make `calibrationDone()` false but `unitCalibrationNeverReset()` true) to fully isolate the condition. More critically: the scenario where `resetCalibrationDate` is null but `calibrationDate` is non-null with `threshold != 0` is not tested. In that case `unitCalibrationNeverReset()` is false but `unitCalibrationDateAndThresholdSet()` would be true — this combination is not explicitly covered.

---

### A63-7 | Severity: MEDIUM | `calibrationPercentage()` is not tested when `isCalibrated()` is true via `unitCalibrationDateAndThresholdSet()` with no impacts

Test 4 sets `calibrationDate`, `resetCalibrationDate`, and `threshold`, and calls `isCalibrated()` — but does not also call `calibrationPercentage()` in that state. `calibrationPercentage()` returns 100 when `isCalibrated()` is true; this is exercised in Test 3 but only via the `calibrationDone()` path (111 impacts). The return-100-via-`unitCalibrationDateAndThresholdSet()` path of `calibrationPercentage()` is never directly asserted.

---

### A63-8 | Severity: MEDIUM | `standardDeviation()` is not tested with uniform (all-same) impact values

When all impacts are identical, the standard deviation is zero. `getCalculatedThreshold()` would then return exactly the mean. Test 8 uses a heterogeneous real-world data set. There is no test covering:
- All impacts equal (deviation = 0, result = average)
- A single impact (deviation = 0 by population formula)
- All impacts = 0 (average = 0, deviation = 0, threshold = 0)

These are important boundary cases for the calibration algorithm correctness.

---

### A63-9 | Severity: MEDIUM | `getCalculatedThreshold()` is not tested via a case where `isCalibrated()` is already true

`getCalculatedThreshold()` is a package-private method that can be called independently of `isCalibrated()`. The test (Test 8) builds a `UnitCalibration` with only 64 impacts — so `isCalibrated()` is false (not >= 100 impacts, no threshold, no calibrationDate). There is no test calling `getCalculatedThreshold()` on a unit already marked as calibrated (e.g., >= 100 impacts or threshold set), and there is no test verifying the interplay between `getCalculatedThreshold()` and `isCalibrated()` (i.e., confirming that the computed threshold would match the stored threshold field after calibration is applied externally).

---

### A63-10 | Severity: MEDIUM | No test for `calibrationPercentage()` when `impacts` is an empty list (not null)

`calibrationPercentage()` (line 67) has a `if (impacts == null) return 0` guard. But if `impacts` is an empty (non-null) list, the method falls through to line 68 and returns `impacts.size()` which is 0 — functionally the same result, but the code path is different. More importantly, `getCalculatedThreshold()` with an empty list would divide by zero. No test exercises an explicitly empty list (as opposed to a null `impacts` field).

---

### A63-11 | Severity: MEDIUM | Cron expression correctness is untested

The cron expression `"0 0 * * * ?"` in `contextInitialized` (line 23) is intended to fire at the top of every hour. It is never validated by any test. A malformed cron expression would throw a `SchedulerException` caught silently at line 30, meaning calibration jobs would simply never run. No test verifies the expression is valid or fires at the expected schedule.

---

### A63-12 | Severity: LOW | `average()` uses population standard deviation, not sample standard deviation — no test documents this design choice

`standardDeviation()` (line 62) divides by `impacts.size()` (population standard deviation, σ) rather than `impacts.size() - 1` (sample standard deviation, s). This is a deliberate algorithmic choice that significantly affects the threshold for small sample sizes. Test 8 only validates with one specific 64-element dataset; there is no test documenting or pinning the formula choice against a known-correct reference implementation, and no test checking behavior when size is 1 (where sample SD would be undefined but population SD yields 0).

---

### A63-13 | Severity: LOW | No negative or zero impact value tests for `getCalculatedThreshold()`

The `impacts` list contains `int` values. Nothing in the class prevents negative or zero impact values. With negative impacts, the average could be negative, and `standardDeviation()` would still work (squared differences are non-negative). The returned threshold could be 0 or negative, which may be semantically invalid for a calibration threshold. No test exercises this edge case.

---

### A63-14 | Severity: LOW | `threshold` field default of `0` is semantically overloaded

When `threshold` is 0 (the Java `int` default when not set via builder), it is treated as "not set" by both `unitCalibrationNeverReset()` and `unitCalibrationDateAndThresholdSet()`. There is no test that explicitly passes `threshold(0)` to document or enforce this sentinel-value contract, and no test verifies what happens if `getCalculatedThreshold()` legitimately returns 0 and is stored back as the threshold.

---

### A63-15 | Severity: INFO | `Lombok @Builder` and `@Getter` annotation-generated code is not explicitly validated

`UnitCalibration` uses Lombok's `@Builder` and `@Getter`. The tests rely on builder-pattern construction without asserting that getters return expected constructed values. While this is normally acceptable, any Lombok misconfiguration (e.g., missing Lombok in test classpath) would cause compilation failures rather than test failures, and there is no explicit test that constructs a `UnitCalibration` and then asserts the field values via getters (`getUnitId()`, `getThreshold()`, `getCalibrationDate()`, etc.).

---

## 5. Summary Table

| Finding | Severity | Category |
|---|---|---|
| A63-1 | CRITICAL | CalibrationJobScheduler — zero test coverage |
| A63-2 | CRITICAL | contextDestroyed broken behavior untested |
| A63-3 | HIGH | getCalculatedThreshold() — null/empty impacts NPE/divide-by-zero |
| A63-4 | HIGH | calibrationPercentage() — exact boundary 100 impacts untested |
| A63-5 | HIGH | isCalibrated() — calibrationDone() at exactly 100 impacts untested |
| A63-6 | HIGH | unitCalibrationNeverReset() — partial isolation, missing combinations |
| A63-7 | MEDIUM | calibrationPercentage() 100% path via date+threshold untested |
| A63-8 | MEDIUM | standardDeviation() — uniform/single/zero impact edge cases untested |
| A63-9 | MEDIUM | getCalculatedThreshold() not tested against a calibrated unit |
| A63-10 | MEDIUM | calibrationPercentage() not tested with empty (non-null) impacts list |
| A63-11 | MEDIUM | Cron expression correctness not validated |
| A63-12 | LOW | Population vs sample SD design choice not pinned by test |
| A63-13 | LOW | Negative/zero impact values not tested for getCalculatedThreshold() |
| A63-14 | LOW | threshold=0 sentinel contract not explicitly tested |
| A63-15 | INFO | Lombok-generated accessors not independently verified |

**Total findings: 15**
**Critical: 2 | High: 4 | Medium: 4 | Low: 3 | Info: 1**
