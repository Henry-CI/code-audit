# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A62
**Files audited:**
- `src/main/java/com/calibration/CalibrationImpact.java`
- `src/main/java/com/calibration/CalibrationJob.java`

---

## 1. Reading-Evidence Blocks

### 1.1 CalibrationImpact.java

**Class:** `com.calibration.CalibrationImpact`
**Modifier:** package-private (no `public`)
**Annotation:** `@lombok.Builder`

| Element | Kind | Line(s) |
|---------|------|---------|
| `value` | field (`int`) | 9 |
| `time` | field (`java.sql.Timestamp`) | 10 |
| `sessionStart` | field (`java.sql.Timestamp`) | 11 |
| `CalibrationImpact(int value, Timestamp time, Timestamp sessionStart)` | constructor (package-private) | 13-17 |

Lombok `@Builder` synthesises at compile time:
- `CalibrationImpact.builder()` — static factory returning `CalibrationImpact.CalibrationImpactBuilder`
- `CalibrationImpactBuilder.value(int)`
- `CalibrationImpactBuilder.time(Timestamp)`
- `CalibrationImpactBuilder.sessionStart(Timestamp)`
- `CalibrationImpactBuilder.build()` — delegates to the explicit constructor

No getters, setters, `equals`, `hashCode`, or `toString` are declared or generated (`@Builder` alone does not generate those).

---

### 1.2 CalibrationJob.java

**Class:** `com.calibration.CalibrationJob`
**Modifier:** `public`
**Implements:** `org.quartz.Job`

| Element | Kind | Line(s) |
|---------|------|---------|
| `execute(JobExecutionContext)` | method (public, `@Override`) | 11-13 |
| `calibrateAllUnits()` | method (public) | 15-24 |

**`execute` body (line 12):**
Spins up a brand-new, unbounded `Executors.newSingleThreadExecutor()` and submits `this::calibrateAllUnits` to it. The executor is never shut down.

**`calibrateAllUnits` body (lines 16-23):**
- Instantiates `UnitCalibrationGetterInDatabase` (concrete, hardcoded — no injection)
- Instantiates `UnitCalibrationEnderInDatabase` (concrete, hardcoded — no injection)
- Constructs `UnitCalibrator(getter, ender)`
- Calls `calibrator.calibrateAllUnits()`
- Catches `SQLException` and prints the stack trace (swallows the exception)

---

## 2. Indirect Coverage Search Results

Grep across `src/test/java/` for `CalibrationImpact` and `CalibrationJob`:

### CalibrationImpact — indirect hits

| Test file | Lines | Nature of reference |
|-----------|-------|---------------------|
| `UnitCalibrationImpactFilterTest.java` | 24, 26, 42, 51, 53 | Inner factory class `CalibrationImpactFactory` builds `CalibrationImpact` instances via `.builder()` and passes them to `UnitCalibrationImpactFilter.filterImpacts()`. The builder path (`value`, `time`, `sessionStart`) is exercised indirectly. |

`CalibrationImpact` is **not** referenced in:
- `UnitCalibrationTest.java`
- `UnitCalibratorTest.java`
- `ImpactUtilTest.java`

### CalibrationJob — indirect hits

**Zero references** in any test file. The class does not appear in any test source anywhere in `src/test/java/`.

`CalibrationJob` is exercised at runtime only through:
- `CalibrationJobScheduler` (Quartz `JobDetail` registration — integration path, no test)
- `CalibrationAction.execute()` (Struts action — no test exists in the test tree)

---

## 3. Coverage Gap Analysis

### 3.1 CalibrationImpact

#### 3.1.1 Explicit constructor never directly tested

The package-private constructor `CalibrationImpact(int, Timestamp, Timestamp)` is exercised only via Lombok's generated builder. There is no direct `new CalibrationImpact(...)` call in any test. Because the constructor is package-private and `@Builder` delegates to it, the execution path does run when the builder is used in `UnitCalibrationImpactFilterTest`. However, the contract of the constructor itself (field assignment) is never asserted — tests only observe downstream filtering behaviour.

#### 3.1.2 No dedicated unit tests for the class

No test class targets `CalibrationImpact` directly. Builder field-by-field assignment is never verified (e.g. that `value`, `time`, and `sessionStart` are stored correctly).

#### 3.1.3 Null field combinations

No test verifies behaviour when any of the three fields is `null`:
- `value` is a primitive (`int`) so it cannot be null; however, the builder can be called without setting it (defaults to `0`) — the zero-value path is never asserted.
- `time = null` — not tested.
- `sessionStart = null` — not tested. This is particularly significant because `UnitCalibrationImpactFilter` computes time differences using `sessionStart`; a null there would cause a `NullPointerException` in the filter, but no test guards that entry point.

#### 3.1.4 Builder partial-build paths

Lombok `@Builder` allows calling `.build()` without setting any fields. The zero-value object (`value=0, time=null, sessionStart=null`) is never tested as an explicit case.

---

### 3.2 CalibrationJob

#### 3.2.1 `execute()` — zero test coverage

`execute(JobExecutionContext)` is completely untested. No test:
- Confirms the method submits work to a new thread.
- Verifies `calibrateAllUnits()` is eventually called.
- Verifies the `JobExecutionContext` parameter is ignored (as it currently is).

#### 3.2.2 `calibrateAllUnits()` — zero test coverage

`calibrateAllUnits()` is completely untested. No test:
- Confirms the method constructs the correct concrete collaborators.
- Confirms `UnitCalibrator.calibrateAllUnits()` is invoked.

Because collaborators are hardcoded (`new UnitCalibrationGetterInDatabase()`, `new UnitCalibrationEnderInDatabase()`), the method is not injectable and cannot be unit-tested without refactoring or a database connection.

#### 3.2.3 `SQLException` catch block — zero test coverage

The `catch (SQLException e)` block on line 21 only calls `e.printStackTrace()`. No test:
- Verifies the exception is caught and does not propagate.
- Verifies that a logging/alerting mechanism is triggered.
- Verifies that no partial state is left behind when the exception fires.

The swallowed exception means a database failure during scheduled calibration produces no observable signal to callers, operators, or monitoring systems.

#### 3.2.4 Executor resource leak — no regression test

`Executors.newSingleThreadExecutor()` is created inside `execute()` and never stored or shut down. Each Quartz trigger invocation leaks one thread. No test verifies executor lifecycle or guards against the accumulation of leaked threads.

#### 3.2.5 Concurrency / race-condition path — no test

`execute()` dispatches work asynchronously. If Quartz fires a second trigger before the first async run finishes, two concurrent `calibrateAllUnits()` calls can be in-flight simultaneously, both writing to the database. No test exercises or even documents this concurrent execution path.

#### 3.2.6 `CalibrationAction` integration path — no test

`CalibrationAction` (in `com.action`) calls `new CalibrationJob().calibrateAllUnits()` directly (line 18-19 of `CalibrationAction.java`). This is a second entry point into `calibrateAllUnits()` that is also untested. No `CalibrationActionTest` exists.

---

## 4. Findings

| ID | Severity | Description |
|----|----------|-------------|
| A62-1 | CRITICAL | `CalibrationJob.calibrateAllUnits()` has zero test coverage. It is the core scheduled calibration entry point and its correctness is entirely unverified. |
| A62-2 | CRITICAL | `CalibrationJob.execute(JobExecutionContext)` has zero test coverage. The Quartz-triggered code path is completely unverified. |
| A62-3 | HIGH | The `SQLException` catch block in `CalibrationJob.calibrateAllUnits()` (line 21) silently swallows the exception via `e.printStackTrace()`. No test verifies error propagation or alerting behaviour; a database failure during scheduled calibration produces no observable signal. |
| A62-4 | HIGH | `CalibrationJob.execute()` creates `Executors.newSingleThreadExecutor()` on every invocation and never shuts down the executor. This constitutes a thread-pool resource leak that accumulates on each Quartz trigger firing. No test guards this lifecycle defect. |
| A62-5 | HIGH | `CalibrationJob.calibrateAllUnits()` hardcodes `new UnitCalibrationGetterInDatabase()` and `new UnitCalibrationEnderInDatabase()`, making the method untestable in isolation without a live database. Dependency injection is absent, precluding unit testing without infrastructure. |
| A62-6 | HIGH | No `CalibrationActionTest` exists. `CalibrationAction.execute()` calls `new CalibrationJob().calibrateAllUnits()` directly, creating a second untested entry point into the calibration pipeline that bypasses Quartz scheduling entirely. |
| A62-7 | MEDIUM | `CalibrationJob.execute()` dispatches calibration asynchronously; no test verifies, documents, or guards the concurrent-execution scenario where a second Quartz trigger fires before the first async run completes, potentially producing two simultaneous database write operations. |
| A62-8 | MEDIUM | `CalibrationImpact` has no dedicated unit test class. Constructor field assignments (`value`, `time`, `sessionStart`) are never directly asserted; correctness is only inferred transitively through `UnitCalibrationImpactFilterTest`. |
| A62-9 | MEDIUM | No test covers `CalibrationImpact` construction with `null` values for `time` or `sessionStart`. Downstream code in `UnitCalibrationImpactFilter` computes time differences from these fields; a null would produce a `NullPointerException` that is not guarded by any test. |
| A62-10 | MEDIUM | The zero-value builder path for `CalibrationImpact` (`value=0, time=null, sessionStart=null`) is never constructed or asserted in any test, even though Lombok's generated builder permits it. |
| A62-11 | LOW | `CalibrationImpact` is package-private but carries no `@VisibleForTesting` or similar marker. The access modifier choice is undocumented; future refactors may inadvertently expose or restrict the class with no test to catch the change. |
| A62-12 | LOW | The Lombok `@Builder` annotation on `CalibrationImpact` generates several synthetic methods (`builder()`, `CalibrationImpactBuilder.value()`, `.time()`, `.sessionStart()`, `.build()`) that are exercised only transitively. No test explicitly validates builder chaining or confirms that missing-field defaults produce the intended zero values. |
| A62-13 | INFO | `CalibrationJob` has no fields and no constructor beyond the default. Its design conflates scheduling concerns (`execute`) with business logic (`calibrateAllUnits`), reducing testability and violating single-responsibility. No test enforces this architectural boundary. |
| A62-14 | INFO | `CalibrationJobScheduler.contextDestroyed()` calls `new ServletException("Application Stopped").printStackTrace()` rather than stopping the Quartz scheduler. This is noted as context: `CalibrationJob` will continue being scheduled even if the servlet context is stopping, but no test exists for either `CalibrationJobScheduler` or its interaction with `CalibrationJob`. |

---

## 5. Summary

| Class | Methods | Methods with any coverage | Coverage % |
|-------|---------|--------------------------|------------|
| `CalibrationImpact` | 1 explicit constructor + 5 Lombok-generated | Constructor exercised transitively via builder in 1 test; builder methods exercised transitively | ~0% direct; ~partial indirect |
| `CalibrationJob` | `execute`, `calibrateAllUnits` | 0 | **0%** |

**Overall verdict:** Both classes are effectively untested. `CalibrationJob`, as the entry point for all scheduled calibration, represents the most severe coverage gap in this audit pair. `CalibrationImpact`, while exercised transitively through the filter tests, has no direct assertions on its own construction or field-level behaviour.
