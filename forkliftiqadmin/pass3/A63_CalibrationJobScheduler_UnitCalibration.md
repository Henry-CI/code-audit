# Pass 3 Documentation Audit — A63
**Audit run:** 2026-02-26-01
**Agent:** A63
**Files:**
- `src/main/java/com/calibration/CalibrationJobScheduler.java`
- `src/main/java/com/calibration/UnitCalibration.java`

---

## 1. Reading Evidence

### CalibrationJobScheduler.java

**Class:** `CalibrationJobScheduler` — line 14
Implements: `ServletContextListener`

**Methods:**

| Method | Line | Visibility | Notes |
|---|---|---|---|
| `contextInitialized(ServletContextEvent)` | 16 | public | `@Override` from `ServletContextListener` |
| `contextDestroyed(ServletContextEvent)` | 36 | public | `@Override` from `ServletContextListener` |

**Fields:** None declared.

---

### UnitCalibration.java

**Class:** `UnitCalibration` — line 11
Annotations: `@Builder`, `@Getter`

**Fields:**

| Field | Type | Line |
|---|---|---|
| `unitId` | `long` | 12 |
| `resetCalibrationDate` | `Timestamp` | 13 |
| `calibrationDate` | `Timestamp` | 14 |
| `threshold` | `int` | 15 |
| `impacts` | `List<Integer>` | 16 |

**Methods:**

| Method | Line | Visibility | Notes |
|---|---|---|---|
| `UnitCalibration(long, Timestamp, Timestamp, int, List<Integer>)` | 18 | package-private | Constructor (Lombok `@Builder` target) |
| `isCalibrated()` | 30 | public | Non-trivial logic |
| `unitCalibrationNeverReset()` | 36 | private | — |
| `unitCalibrationDateAndThresholdSet()` | 40 | private | — |
| `calibrationDone()` | 44 | private | — |
| `getCalculatedThreshold()` | 48 | package-private | Non-trivial computation |
| `average()` | 53 | private | — |
| `standardDeviation(double)` | 59 | private | — |
| `calibrationPercentage()` | 65 | public | Non-trivial logic |

---

## 2. Findings

### A63-1 [LOW] — No class-level Javadoc on `CalibrationJobScheduler`

**File:** `CalibrationJobScheduler.java`, line 14

The class declaration has no Javadoc comment. There is no description of the class's purpose (registering a Quartz cron scheduler on servlet context initialization), nor of the cron schedule it installs (`0 0 * * * ?` — top of every hour).

```java
public class CalibrationJobScheduler implements ServletContextListener {
```

---

### A63-2 [MEDIUM] — `contextInitialized` is undocumented and non-trivial

**File:** `CalibrationJobScheduler.java`, line 16

No Javadoc is present. The method constructs a Quartz `JobDetail` and `CronTrigger`, obtains a scheduler from `StdSchedulerFactory`, schedules the job, and starts the scheduler. This is non-trivial behaviour that warrants at minimum a description of what job is scheduled and at what interval. Missing `@param` for `servletContextEvent` as well.

```java
@Override
public void contextInitialized(ServletContextEvent servletContextEvent) {
```

---

### A63-3 [MEDIUM] — `contextDestroyed` is undocumented and contains misleading/incorrect behaviour

**File:** `CalibrationJobScheduler.java`, line 36

No Javadoc is present. More importantly, the implementation does not shut down the Quartz scheduler — it merely constructs a `ServletException` and calls `printStackTrace()` on it without throwing or logging it properly. A reader or maintainer has no way to know from any comment that the scheduler is intentionally (or unintentionally) left running on context destruction. The absence of any documentation on this behaviour makes the situation more dangerous since the method's name implies a clean shutdown lifecycle.

```java
@Override
public void contextDestroyed(ServletContextEvent servletContextEvent) {
    new ServletException("Application Stopped").printStackTrace();
}
```

Note: This finding is documentation-severity MEDIUM (no Javadoc on a non-trivial public method). The implementation concern (no scheduler shutdown, spurious stack trace) is flagged here for awareness but scored only against the documentation gap.

---

### A63-4 [LOW] — No class-level Javadoc on `UnitCalibration`

**File:** `UnitCalibration.java`, line 11

The class declaration has no Javadoc. There is no description of what a `UnitCalibration` represents (a forklift unit's calibration state), what the `impacts` list contains, or how `threshold` relates to calibration validity.

```java
@Builder
@Getter
public class UnitCalibration {
```

---

### A63-5 [MEDIUM] — `isCalibrated()` is undocumented and non-trivial

**File:** `UnitCalibration.java`, line 30

No Javadoc is present. The method encodes three independent conditions under which a unit is considered calibrated:
1. `unitCalibrationNeverReset()` — `resetCalibrationDate == null && calibrationDate == null && threshold != 0`
2. `unitCalibrationDateAndThresholdSet()` — `calibrationDate != null && threshold != 0`
3. `calibrationDone()` — `impacts != null && impacts.size() >= 100`

These conditions are not obvious; the business rules they encode deserve explanation. Missing `@return` tag.

```java
public boolean isCalibrated() {
    return unitCalibrationNeverReset() ||
            unitCalibrationDateAndThresholdSet() ||
            calibrationDone();
}
```

---

### A63-6 [MEDIUM] — `calibrationPercentage()` is undocumented and non-trivial

**File:** `UnitCalibration.java`, line 65

No Javadoc is present. The method returns `100` if the unit is already calibrated, `0` if `impacts` is null, and otherwise `impacts.size()` capped at `100`. It is not documented that calibration progress is based purely on the count of impacts up to 100, or that the cap is `impacts.size() > 100 ? 100 : impacts.size()` (i.e., exactly 100 impacts is NOT capped — only values strictly greater than 100 are). Missing `@return` tag.

```java
public int calibrationPercentage() {
    if (isCalibrated()) return 100;
    if (impacts == null) return 0;
    return impacts.size() > 100 ? 100 : impacts.size();
}
```

---

### A63-7 [LOW] — Lombok-generated getters have no Javadoc

**File:** `UnitCalibration.java`, lines 12–16

The `@Getter` annotation causes Lombok to generate public getter methods for all five fields (`getUnitId()`, `getResetCalibrationDate()`, `getCalibrationDate()`, `getThreshold()`, `getImpacts()`). None have Javadoc. These are trivial getters so severity is LOW; however, field-level Javadoc (which Lombok can propagate) is entirely absent, leaving the meaning of each field undocumented.

---

### A63-8 [LOW] — Package-private `getCalculatedThreshold()` has no Javadoc

**File:** `UnitCalibration.java`, line 48

Although not `public`, this method is package-accessible and non-trivial: it computes the calibration threshold as `average + population standard deviation` over the `impacts` list. No Javadoc explains the formula, the units, preconditions (e.g., `impacts` must be non-null and non-empty to avoid division by zero), or return semantics. This is LOW severity because the method is not public, but it is called within the package and the formula is domain-significant.

```java
int getCalculatedThreshold() {
    double average = average();
    return (int) (average + standardDeviation(average));
}
```

---

## 3. Summary Table

| ID | File | Location | Severity | Description |
|---|---|---|---|---|
| A63-1 | `CalibrationJobScheduler.java` | Line 14 | LOW | No class-level Javadoc |
| A63-2 | `CalibrationJobScheduler.java` | Line 16 | MEDIUM | `contextInitialized` undocumented; non-trivial scheduler setup |
| A63-3 | `CalibrationJobScheduler.java` | Line 36 | MEDIUM | `contextDestroyed` undocumented; no indication scheduler is not shut down |
| A63-4 | `UnitCalibration.java` | Line 11 | LOW | No class-level Javadoc |
| A63-5 | `UnitCalibration.java` | Line 30 | MEDIUM | `isCalibrated()` undocumented; complex multi-condition logic, missing `@return` |
| A63-6 | `UnitCalibration.java` | Line 65 | MEDIUM | `calibrationPercentage()` undocumented; non-obvious cap logic, missing `@return` |
| A63-7 | `UnitCalibration.java` | Lines 12–16 | LOW | Lombok-generated getters and backing fields have no Javadoc |
| A63-8 | `UnitCalibration.java` | Line 48 | LOW | Package-private `getCalculatedThreshold()` undocumented; formula and preconditions unexplained |

**Total findings: 8** (4 MEDIUM, 4 LOW, 0 HIGH)
