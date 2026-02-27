# Pass 2 — Test Coverage: rtls package
**Agent:** A17
**Date:** 2026-02-25
**Repo:** fleetfocus (branch: release/UAT_RELEASE_FLEETFOCUS_Production)

## Test Infrastructure Assessment

| Criterion | Status |
|---|---|
| Test directories (`test/`, `src/test/`) | **None found** |
| Test framework dependencies (JUnit, TestNG) | **None found** |
| Build system (pom.xml, build.gradle, build.xml) | **None found** |
| Test files (`*Test.java`, `*Spec.java`) | **None found** |
| Any `@Test` annotations in codebase | **None found** |
| CI/CD test configuration | **Not assessed (no build files)** |

**Conclusion:** The repository has **zero test infrastructure**. There are no unit tests, no integration tests, no test framework dependencies, and no build system configuration. Every class in the `rtls` package has **0% test coverage**.

---

## Reading Evidence

All files reside under `WEB-INF/src/com/torrent/surat/fms6/rtls/`.

### 1. GridCluster.java (76 lines)

**Class:** `GridCluster`
**Purpose:** Grid-based spatial clustering of Points with weight accumulation and standard-deviation threshold calculation.

| Visibility | Method Signature | Line |
|---|---|---|
| private | `Points simplePoints(Points points, double mod)` | 13 |
| public | `HashMap<Points, Double> reducePoints(ArrayList<Points> arrPoints, String density)` | 21 |
| public | `String calculateStdev(HashMap<Points, Double> hashPoints)` | 47 |

**Callers:** `RTLSHeatMapReport.java` (lines 456, 517).

### 2. LonLatConverter.java (123 lines)

**Class:** `LonLatConverter`
**Purpose:** Converts local Cartesian (x, y) coordinates to geodetic (longitude, latitude) using the Vincenty direct formula on the WGS-84 ellipsoid.

| Visibility | Method Signature | Line |
|---|---|---|
| public | `double getOringin_lat()` | 19 |
| public | `void setOringin_lat(double oringin_lat)` | 23 |
| public | `double getOringin_lon()` | 27 |
| public | `void setOringin_lon(double oringin_lon)` | 31 |
| public | `double getLon()` | 35 |
| public | `void setLon(double lon)` | 39 |
| public | `double getLat()` | 43 |
| public | `void setLat(double lat)` | 47 |
| public | `void computerThatLonLat(double x, double y)` | 56 |
| private | `double rad(double d)` | 106 |
| private | `double deg(double x)` | 111 |
| public | `double getBrng(double x, double y)` | 115 |
| public | `double getDistance(double x, double y)` | 119 |

**Ellipsoid constants (instance fields, lines 9-11):**
- `a = 6378137` (semi-major axis, metres)
- `b = 6356752.3142` (semi-minor axis, metres)
- `f = 1 / 298.2572236` (flattening)

**Hard-coded origin (public instance fields, lines 13-14):**
- `oringin_lon = 150.95866482248996`
- `oringin_lat = -33.922175999995076`

**Callers:** `RTLSHeatMapReport.java` (line 444), `RTLSImpactReport.java` (line 860).

### 3. MovingAverage.java (24 lines)

**Class:** `MovingAverage`
**Purpose:** Computes a simple moving average over a sliding window of the last N values.

| Visibility | Method Signature | Line |
|---|---|---|
| public | `MovingAverage(int size)` | 12 |
| public | `double next(double val)` | 16 |

**Callers:** `RTLSImpactReport.java` (lines 1172, 1197) -- always instantiated with window size 4.

### 4. Points.java (88 lines)

**Class:** `Points`
**Purpose:** 2D point data structure with x/y coordinates, weight, timestamp, and a `centralpoints` flag. Used as HashMap key (provides `hashCode`/`equals`).

| Visibility | Method Signature | Line |
|---|---|---|
| public | `boolean isCentralpoints()` | 12 |
| public | `void setCentralpoints(boolean centralpoints)` | 16 |
| public | `Points()` | 20 |
| public | `Points(double x, double y)` | 25 |
| public | `Timestamp getAt()` | 30 |
| public | `void setAt(Timestamp at)` | 34 |
| public | `double getWeight()` | 38 |
| public | `void setWeight(double weight)` | 42 |
| public | `double getX()` | 46 |
| public | `void setX(double x)` | 49 |
| public | `double getY()` | 53 |
| public | `void setY(double y)` | 56 |
| public | `int hashCode()` | 61 |
| public | `boolean equals(Object obj)` | 73 |

### 5. SessionBean.java (48 lines)

**Class:** `SessionBean implements Serializable`
**Purpose:** DTO holding a vehicle code, start/end timestamps, and an `ArrayList<Points>` for an RTLS session.

| Visibility | Method Signature | Line |
|---|---|---|
| public | `ArrayList<Points> getArrPoints()` | 17 |
| public | `void setArrPoints(ArrayList<Points> arrPoints)` | 21 |
| public | `int getVeh_cd()` | 25 |
| public | `void setVeh_cd(int veh_cd)` | 29 |
| public | `Timestamp getSt_dt()` | 33 |
| public | `Timestamp getTo_dt()` | 37 |
| public | `void setSt_dt(Timestamp st_dt)` | 41 |
| public | `void setTo_dt(Timestamp to_dt)` | 45 |

### 6. ShockBean.java (52 lines)

**Class:** `ShockBean implements Serializable`
**Purpose:** DTO for shock/impact event data (shock ID, datetime string, vehicle code, caching flags).

| Visibility | Method Signature | Line |
|---|---|---|
| public | `boolean isLocation_cached()` | 17 |
| public | `boolean isSpeed_cached()` | 20 |
| public | `void setLocation_cached(boolean location_cached)` | 23 |
| public | `void setSpeed_cached(boolean speed_cached)` | 26 |
| public | `int getShockId()` | 31 |
| public | `int getVeh_cd()` | 35 |
| public | `void setShockId(int shockId)` | 38 |
| public | `String getDate_time()` | 42 |
| public | `void setDate_time(String date_time)` | 45 |
| public | `void setVeh_cd(int veh_cd)` | 48 |

### 7. SpeedBean.java (41 lines)

**Class:** `SpeedBean implements Serializable`
**Purpose:** DTO for speed data (speed value, timestamp, time interval).

| Visibility | Method Signature | Line |
|---|---|---|
| public | `double getInterval()` | 17 |
| public | `void setInterval(double interval)` | 20 |
| public | `double getSpeed()` | 23 |
| public | `Timestamp getAt()` | 26 |
| public | `void setSpeed(double speed)` | 29 |
| public | `void setAt(Timestamp at)` | 32 |

### 8. Tags.java (27 lines)

**Class:** `Tags implements Serializable`
**Purpose:** DTO for RTLS tag data (integer ID and string alias).

| Visibility | Method Signature | Line |
|---|---|---|
| public | `int getId()` | 13 |
| public | `String getAlias()` | 16 |
| public | `void setId(int id)` | 19 |
| public | `void setAlias(String alias)` | 22 |

---

## Findings

### A17-01 — GridCluster.reducePoints: Division by zero when density is "0" (CRITICAL)

**File:** `GridCluster.java`, line 31
**Severity:** Critical
**Code:**
```java
Points spt = simplePoints(pt, Double.parseDouble(density)/100);
```
The `density` parameter is a `String` parsed at runtime. If `density` is `"0"`, then `mod = 0.0`, and `simplePoints` divides by zero (`points.getX()/mod`), producing `Infinity` or `NaN`. No input validation exists.

**Required tests:**
- `density = "0"` -- division by zero
- `density = ""` or `null` -- `NumberFormatException` / `NullPointerException`
- Negative density values -- semantic correctness of grid snapping
- Typical positive densities with known point sets -- verify clustering output
- Empty `arrPoints` list -- should return empty map

---

### A17-02 — GridCluster.calculateStdev: Division by zero on empty or single-entry HashMap (CRITICAL)

**File:** `GridCluster.java`, lines 62, 68
**Severity:** Critical
**Code:**
```java
double mean = sum/length;          // line 62: length=0 when hashPoints is empty
stdev = Math.sqrt(stdev/(length-1)); // line 68: division by (length-1), so length=1 causes /0
```
When `hashPoints` is empty, `length == 0`, causing division by zero at line 62. When `hashPoints` has exactly one entry, `length - 1 == 0`, causing division by zero at line 68. Both produce `NaN` which propagates into the returned threshold string.

**Required tests:**
- Empty `HashMap<Points, Double>` input
- Single-entry HashMap input
- Two-entry HashMap (minimum for valid sample stdev)
- Large HashMap with known statistical values to verify correctness
- HashMap with all-identical values (stdev should be 0)

---

### A17-03 — GridCluster.simplePoints: Integer truncation bias for negative coordinates (HIGH)

**File:** `GridCluster.java`, lines 15-16
**Severity:** High
**Code:**
```java
double x = ((int)(points.getX()/mod)) * mod + mod/2;
double y = ((int)(points.getY()/mod)) * mod + mod/2;
```
The `(int)` cast truncates toward zero, not toward negative infinity. For negative coordinates (e.g., `x = -0.3, mod = 1.0`), `(int)(-0.3) = 0`, yielding `x = 0.5`, which snaps the point to the wrong grid cell. The correct approach would use `Math.floor()`. This produces asymmetric clustering around the origin.

**Required tests:**
- Negative x and y values
- Values near zero from both sides
- Values exactly on grid boundaries
- Very small mod values (precision loss)
- Very large coordinate values (integer overflow risk in `(int)` cast)

---

### A17-04 — LonLatConverter.computerThatLonLat: Vincenty formula with no convergence guard (CRITICAL)

**File:** `LonLatConverter.java`, lines 80-88
**Severity:** Critical
**Code:**
```java
double sigma = dist / (b * A), sigmaP = 2 * Math.PI;
while (Math.abs(sigma - sigmaP) > 1e-12) {
    // ... iterative refinement ...
    sigmaP = sigma;
    sigma = dist / (b * A) + deltaSigma;
}
```
The Vincenty direct formula iteration has **no maximum iteration count**. While the direct formula generally converges, pathological inputs (e.g., near-antipodal points, extreme distances, or `NaN`/`Infinity` inputs from upstream) could cause an infinite loop. Production geodetic libraries typically cap iterations at 100-200.

**Required tests:**
- x=0, y=0 (zero distance) -- verify no division by zero, convergence
- Very large distances (near half-circumference of Earth)
- Negative x and y values
- Very small distances (sub-millimetre)
- Known geodetic test vectors (published Vincenty examples)
- Confirm convergence within reasonable iteration count

---

### A17-05 — LonLatConverter.getBrng: Non-standard bearing calculation (HIGH)

**File:** `LonLatConverter.java`, lines 115-117
**Severity:** High
**Code:**
```java
public double getBrng(double x, double y){
    return Math.atan2(y,x) * 180 / Math.PI + 90;
}
```
This converts Cartesian angle to a bearing by adding 90 degrees, but does not normalize the result to `[0, 360)`. For certain x/y combinations (e.g., `x=1, y=-1`), the result can be negative (e.g., `45 degrees`... but `x=0, y=-1` yields `90 + (-90) = 0`, while `x=-1, y=0` yields `90 + 180 = 270`). However, `x=0, y=0` returns `90 + 0 = 90` (bearing for zero-length vector is meaningless). The lack of range normalization and zero-input handling creates incorrect bearings for negative-quadrant inputs fed into the Vincenty formula where bearing must be well-defined.

**Required tests:**
- All four quadrants of (x, y)
- Axis-aligned vectors: (1,0), (0,1), (-1,0), (0,-1)
- x=0, y=0 (degenerate)
- Verify output range is [0, 360)

---

### A17-06 — LonLatConverter: Hard-coded origin coordinates with no validation (MEDIUM)

**File:** `LonLatConverter.java`, lines 13-14
**Severity:** Medium
**Code:**
```java
public double oringin_lon = 150.95866482248996;
public double oringin_lat = -33.922175999995076;
```
The origin coordinates are hard-coded to a specific location (near Sydney, Australia) as **public mutable instance fields** (not constants). Callers can set them via setters, but there is no validation that longitude is in `[-180, 180]` or latitude in `[-90, 90]`. Setting `oringin_lat = 90` (a pole) would cause `Math.tan(rad(90))` to approach infinity in the Vincenty formula (line 66), likely causing numerical instability or infinite loop.

**Required tests:**
- Custom origin at various global locations
- Origin at poles (lat = +/-90)
- Origin at date line (lon = +/-180)
- Origin at equator/prime meridian (0, 0)

---

### A17-07 — MovingAverage: Off-by-one in window boundary logic (HIGH)

**File:** `MovingAverage.java`, lines 16-23
**Severity:** High
**Code:**
```java
public double next(double val) {
    _sum += val;
    _queue.offer(val);
    if (_index++ >= _size) {
        _sum -= _queue.remove();
    }
    return _sum / _queue.size();
}
```
The window allows `_size + 1` elements before it starts evicting. When `_size = 3`, the first eviction occurs when `_index` (which is post-incremented) reaches 3, meaning 4 elements are in the queue at that point. After eviction, 3 remain. However, for the first 3 calls (`_index` = 0, 1, 2), the condition is false so the queue accumulates 1, 2, 3, then on the 4th call (`_index` = 3, which is `>= _size`), it evicts, leaving 3. This means the window effectively holds `_size` elements after warm-up, but the first `_size` results are expanding-window averages rather than fixed-window averages. This is likely intentional but undocumented and untested.

Additionally:
- `_size = 0` means every call evicts immediately after adding, so the queue always has size 1 and the "average" is just the current value.
- `_size < 0` means the condition is always true from the start, but on the first call the queue only has 1 element after `offer`, so `remove()` works, but subsequent calls could produce a queue that never grows beyond 1.
- No guard against `_size <= 0`.

**Required tests:**
- `_size = 1` -- each `next()` should return the latest value
- `_size = 0` -- degenerate behavior
- `_size < 0` -- negative window
- Known sequence: e.g., `size=3`, inputs `[1, 2, 3, 4, 5]`, verify each output
- Numerical precision with very large or very small doubles
- `NaN` and `Infinity` as inputs

---

### A17-08 — MovingAverage: Accumulating floating-point drift over many calls (MEDIUM)

**File:** `MovingAverage.java`, lines 17, 20
**Severity:** Medium
**Code:**
```java
_sum += val;
// ...
_sum -= _queue.remove();
```
The running sum is maintained by incremental add/subtract. Over thousands of calls, floating-point rounding errors accumulate. For long-running RTLS data streams, the average could drift from the true value. A compensated summation (Kahan) or periodic recomputation from the queue would be needed for accuracy.

**Required tests:**
- 10,000+ sequential `next()` calls with known values, then verify accumulated drift
- Alternating large and small values to stress cancellation errors

---

### A17-09 — Points.hashCode/equals: Floating-point equality used as HashMap key (HIGH)

**File:** `Points.java`, lines 61-86
**Severity:** High
**Code:**
```java
public int hashCode() {
    // uses Double.doubleToLongBits(x) and Double.doubleToLongBits(y)
}
public boolean equals(Object obj) {
    // uses Double.doubleToLongBits(x) != Double.doubleToLongBits(other.x)
}
```
Points objects are used as `HashMap` keys in `GridCluster.reducePoints()`. The `hashCode`/`equals` implementation uses exact bitwise comparison of doubles via `Double.doubleToLongBits()`. While this is technically correct for HashMap contracts, it means that points differing by even 1 ULP (unit in last place) will hash to different buckets. Since the x/y values are computed by `simplePoints()` through division and multiplication, floating-point arithmetic may not produce bit-identical results for logically equivalent grid cells, causing duplicate entries in the cluster map.

**Required tests:**
- Two `Points` created by the same arithmetic path -- verify equality
- Two `Points` with mathematically identical but computationally different paths -- test if they collide
- `NaN` coordinates: `Double.doubleToLongBits(NaN)` is well-defined, but `NaN != NaN` in floating-point; verify HashMap behavior
- Points with `+0.0` vs `-0.0` (`doubleToLongBits` distinguishes them)
- Symmetry and transitivity of equals
- hashCode consistency contract

---

### A17-10 — Points.hashCode: Weight and timestamp excluded from equality (LOW)

**File:** `Points.java`, lines 61-86
**Severity:** Low

The `hashCode` and `equals` methods only consider `x` and `y`, ignoring `weight`, `at` (timestamp), and `centralpoints`. This means two Points with the same coordinates but different weights are considered equal. In `GridCluster.reducePoints()`, this is intentional (weights are accumulated), but it could cause subtle bugs if Points are used in other HashMap/HashSet contexts where weight or timestamp identity matters.

**Required tests:**
- Verify Points with same x/y but different weights are equal
- Verify HashMap correctly merges entries with same x/y
- Document intentional asymmetry between equals and field contents

---

### A17-11 — Serializable beans: Missing equals/hashCode on SessionBean, ShockBean, SpeedBean, Tags (LOW)

**Files:** `SessionBean.java`, `ShockBean.java`, `SpeedBean.java`, `Tags.java`
**Severity:** Low

These four Serializable DTOs do not override `equals()` or `hashCode()`. If they are ever placed in collections that depend on value equality (HashSets, HashMaps, deduplication), identity-based comparison will be used, which may not be the intended behavior. Since they are used in `ArrayList` and `TreeMap` (keyed by `Double`, not by bean), the immediate risk is low but worth verifying.

**Required tests:**
- Serialization round-trip: serialize and deserialize, verify field fidelity
- Collection membership behavior with equal-valued beans

---

### A17-12 — ShockBean: Package-private fields break encapsulation (LOW)

**File:** `ShockBean.java`, lines 12-16, 29
**Severity:** Low
**Code:**
```java
int shockId;
String date_time;
int veh_cd;
boolean location_cached;
boolean speed_cached;
```
All fields use default (package-private) access rather than `private`. While getters/setters exist, other classes in the same package can bypass them and directly mutate fields, creating potential maintenance hazards.

**Required tests:**
- Getter/setter round-trip for all fields
- Verify no direct field access from other package classes

---

### A17-13 — GridCluster.reducePoints: density parameter is String not double (MEDIUM)

**File:** `GridCluster.java`, line 31
**Severity:** Medium
**Code:**
```java
Points spt = simplePoints(pt, Double.parseDouble(density)/100);
```
The `density` parameter is a `String` that is parsed to `double` inside the loop body, meaning `Double.parseDouble(density)` is called on every iteration of the loop rather than once. Beyond the minor performance concern, this exposes the method to `NumberFormatException` on malformed input with no try/catch. The method signature should accept `double` or parse once outside the loop.

**Required tests:**
- Non-numeric string (e.g., "abc") -- expect `NumberFormatException`
- Empty string -- expect `NumberFormatException`
- `null` -- expect `NullPointerException`
- Strings with leading/trailing whitespace
- Locale-sensitive strings (e.g., "1,5" vs "1.5")

---

### A17-14 — LonLatConverter: Vincenty formula correctness unverified (CRITICAL)

**File:** `LonLatConverter.java`, lines 56-104
**Severity:** Critical

The `computerThatLonLat` method implements the Vincenty direct formula, a complex geodetic algorithm with approximately 30 intermediate variables and multiple trigonometric operations. Without any unit tests against known geodetic reference values, there is no assurance that:
1. The formula is correctly transcribed
2. The bearing calculation at line 116 correctly maps Cartesian angles to geodetic bearings
3. Coordinate results are accurate to an acceptable tolerance
4. The longitude addition at line 101 (`this.oringin_lon + deg(L)`) handles wrap-around at +/-180

Published test vectors exist (e.g., Vincenty's 1975 paper, NGS geodetic toolkit) and should be used for verification.

**Required tests:**
- Known Vincenty direct test vectors (Vincenty 1975, Table 2)
- Short distances (< 1m) vs long distances (> 1000km)
- Conversion round-trip: convert x,y to lon/lat, then compute inverse to verify distance
- Points near the poles, equator, and date line
- Points at the hard-coded origin itself (x=0, y=0)

---

### A17-15 — LonLatConverter.getDistance: No overflow protection (LOW)

**File:** `LonLatConverter.java`, lines 119-121
**Severity:** Low
**Code:**
```java
public double getDistance(double x, double y){
    return Math.sqrt(x*x+y*y);
}
```
For very large x or y values, `x*x` could overflow to `Infinity` before `Math.sqrt` is applied. `Math.hypot(x, y)` is the standard overflow-safe alternative.

**Required tests:**
- x or y near `Double.MAX_VALUE / 2`
- x=0, y=0
- Normal values with known Pythagorean triples

---

## Summary

| ID | File | Severity | Category |
|---|---|---|---|
| A17-01 | GridCluster.java | Critical | Division by zero / missing input validation |
| A17-02 | GridCluster.java | Critical | Division by zero on empty/single-entry input |
| A17-03 | GridCluster.java | High | Integer truncation bias for negative coordinates |
| A17-04 | LonLatConverter.java | Critical | Infinite loop risk (no iteration cap) |
| A17-05 | LonLatConverter.java | High | Non-standard bearing, no range normalization |
| A17-06 | LonLatConverter.java | Medium | Hard-coded origin, no coordinate validation |
| A17-07 | MovingAverage.java | High | Off-by-one window, no guard on size <= 0 |
| A17-08 | MovingAverage.java | Medium | Floating-point drift over long streams |
| A17-09 | Points.java | High | Floating-point exact equality as HashMap key |
| A17-10 | Points.java | Low | Weight/timestamp excluded from equality |
| A17-11 | SessionBean/ShockBean/SpeedBean/Tags | Low | Missing equals/hashCode on Serializable beans |
| A17-12 | ShockBean.java | Low | Package-private fields |
| A17-13 | GridCluster.java | Medium | String density parsed in loop, no error handling |
| A17-14 | LonLatConverter.java | Critical | Vincenty formula correctness unverified |
| A17-15 | LonLatConverter.java | Low | Overflow risk in getDistance |

**Totals:** 4 Critical, 4 High, 3 Medium, 4 Low

### Priority Test Recommendations

The following classes should be the highest priority for test development due to algorithmic complexity and defect risk:

1. **LonLatConverter** -- Geodetic math (Vincenty formula) with zero validation, no convergence guard, and no verification against reference values. Any bug here silently corrupts geographic coordinates displayed on maps or used in reports.

2. **GridCluster** -- Clustering algorithm with division-by-zero paths, integer truncation bias, and unvalidated string-to-double parsing. Bugs here corrupt heat map reports.

3. **MovingAverage** -- Sliding window algorithm with off-by-one behavior and floating-point drift risk. Used to smooth speed data for impact analysis.

4. **Points** -- HashMap key class with floating-point exact equality. Underpins correctness of all GridCluster operations.

The DTO classes (SessionBean, ShockBean, SpeedBean, Tags) are low-risk getter/setter holders but should still have basic serialization round-trip tests.
