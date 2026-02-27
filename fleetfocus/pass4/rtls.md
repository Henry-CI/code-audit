# Pass 4 -- Code Quality Audit: `rtls` Package

**Audit ID:** A17
**Date:** 2026-02-25
**Pass:** 4 (Code Quality)
**Package:** `com.torrent.surat.fms6.rtls`
**Branch:** `release/UAT_RELEASE_FLEETFOCUS_Production`
**Base path:** `WEB-INF/src/com/torrent/surat/fms6/rtls/`

---

## Files Audited

| # | File | Lines |
|---|------|-------|
| 1 | GridCluster.java | 76 |
| 2 | LonLatConverter.java | 123 |
| 3 | MovingAverage.java | 24 |
| 4 | Points.java | 88 |
| 5 | SessionBean.java | 48 |
| 6 | ShockBean.java | 52 |
| 7 | SpeedBean.java | 41 |
| 8 | Tags.java | 27 |

---

## Findings

### CQ-RTLS-01 -- Misspelled identifier: `computerThatLonLat`

| Field | Value |
|-------|-------|
| **File** | `LonLatConverter.java` |
| **Line** | 56 |
| **Severity** | Medium |
| **Category** | Naming / Typo |

**Evidence:**
```java
public void computerThatLonLat(double x, double y) {
```

**Description:** The method name `computerThatLonLat` is misspelled. The intended name is almost certainly `computeThatLonLat` (or `computeLonLat`). The word "computer" (noun) is used where "compute" (verb) was intended. This method is the core Vincenty direct-formula solver for the class, so the misspelling propagates to every call site.

---

### CQ-RTLS-02 -- Misspelled identifier: `oringin`

| Field | Value |
|-------|-------|
| **File** | `LonLatConverter.java` |
| **Lines** | 13, 14, 19, 23, 27, 31, 66, 101 |
| **Severity** | Medium |
| **Category** | Naming / Typo |

**Evidence:**
```java
public  double oringin_lon = 150.95866482248996;   // line 13
public  double oringin_lat = -33.922175999995076;   // line 14
public double getOringin_lat() {                     // line 19
public void setOringin_lat(double oringin_lat) {     // line 23
public double getOringin_lon() {                     // line 27
public void setOringin_lon(double oringin_lon) {     // line 31
```

**Description:** The word "origin" is misspelled as `oringin` throughout the file -- in two field names, four getter/setter method names, and two internal usages (lines 66, 101). The correct spelling is `origin`. Because these are public fields and public methods, the misspelling is part of the API contract and propagates to all callers.

---

### CQ-RTLS-03 -- Misspelled identifier: `treshold`

| Field | Value |
|-------|-------|
| **File** | `GridCluster.java` |
| **Lines** | 53, 69, 73 |
| **Severity** | Low |
| **Category** | Naming / Typo |

**Evidence:**
```java
double treshold = 0;          // line 53
treshold = stdev + mean;      // line 69
return df.format(treshold);   // line 73
```

**Description:** The local variable `treshold` is misspelled. The correct English spelling is `threshold`. Although this is a local variable (not public API), it still hurts readability.

---

### CQ-RTLS-04 -- Magic numbers in geodetic constants

| Field | Value |
|-------|-------|
| **File** | `LonLatConverter.java` |
| **Lines** | 9-11, 73-74, 80, 94 |
| **Severity** | Medium |
| **Category** | Magic Numbers |

**Evidence:**
```java
private double a = 6378137;              // line 9
private double b = 6356752.3142;         // line 10
private double f = 1 / 298.2572236;      // line 11
...
double A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)));  // line 73
double B = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)));           // line 74
...
while (Math.abs(sigma - sigmaP) > 1e-12) {   // line 80
...
double C = f / 16 * cosSqAlpha * (4 + f * (4 - 3 * cosSqAlpha));  // line 94
```

**Description:** The WGS-84 ellipsoid parameters (`a`, `b`, `f`) are assigned as bare numeric literals with no documentation. The field names are single-letter and non-descriptive. Additionally, the Vincenty formula coefficients (16384, 4096, 768, 320, 175, 1024, 256, 128, 74, 47) appear as raw numbers with no explanatory comments. The convergence tolerance `1e-12` is also a magic number. These values are standard geodetic constants from Vincenty's formulae, but without named constants or comments they are opaque to any future maintainer.

---

### CQ-RTLS-05 -- Magic number: `density` division by 100

| Field | Value |
|-------|-------|
| **File** | `GridCluster.java` |
| **Line** | 31 |
| **Severity** | Low |
| **Category** | Magic Numbers |

**Evidence:**
```java
Points spt = simplePoints(pt, Double.parseDouble(density)/100);
```

**Description:** The divisor `100` is unexplained. It is unclear whether this converts a percentage to a fraction, or performs some other scaling. No comment or named constant documents the purpose.

---

### CQ-RTLS-06 -- Magic number in `DecimalFormat` pattern

| Field | Value |
|-------|-------|
| **File** | `GridCluster.java` |
| **Line** | 56 |
| **Severity** | Low |
| **Category** | Magic Numbers |

**Evidence:**
```java
DecimalFormat df = new DecimalFormat("#.00");
```

**Description:** The format pattern `"#.00"` is a magic string literal. Why two decimal places? This should be a named constant with a comment explaining its purpose.

---

### CQ-RTLS-07 -- Magic number: bearing offset `+ 90`

| Field | Value |
|-------|-------|
| **File** | `LonLatConverter.java` |
| **Line** | 116 |
| **Severity** | Low |
| **Category** | Magic Numbers |

**Evidence:**
```java
return Math.atan2(y,x) * 180 / Math.PI + 90;  // the angle to y up direction
```

**Description:** The `+ 90` offset rotates the angle from a mathematical convention (east = 0) to a compass convention (north = 0). While the inline comment partially explains this, a named constant (e.g., `MATH_TO_COMPASS_OFFSET`) would be clearer.

---

### CQ-RTLS-08 -- Commented-out code

| Field | Value |
|-------|-------|
| **File** | `LonLatConverter.java` |
| **Line** | 98 |
| **Severity** | Low |
| **Category** | Commented-Out Code |

**Evidence:**
```java
//double revAz = Math.atan2(sinAlpha, -tmp); // final bearing
```

**Description:** A full computation statement is commented out. This is dead code that computes the reverse azimuth (final bearing). It should either be removed or restored with an explanation of why it is needed.

---

### CQ-RTLS-09 -- Unused import: `java.sql.Timestamp`

| Field | Value |
|-------|-------|
| **File** | `ShockBean.java` |
| **Line** | 3 |
| **Severity** | Low |
| **Category** | Unused Imports |

**Evidence:**
```java
import java.sql.Timestamp;
```

**Description:** The `ShockBean` class imports `java.sql.Timestamp` but the `date_time` field is declared as `String` (line 13). The `Timestamp` type is never used anywhere in the class.

---

### CQ-RTLS-10 -- Unused import: `java.sql.Timestamp`

| Field | Value |
|-------|-------|
| **File** | `SpeedBean.java` |
| **Line** | 3 |
| **Severity** | Info |
| **Category** | Unused Imports (marginal) |

**Evidence:**
```java
import java.sql.Timestamp;
```

**Description:** This import IS used (the `at` field is of type `Timestamp`), so this is not a true unused import. No issue here -- included for completeness during review and confirmed clean.

---

### CQ-RTLS-11 -- Floating-point equality via `doubleToLongBits` in HashMap key

| Field | Value |
|-------|-------|
| **File** | `Points.java` |
| **Lines** | 61-86 |
| **Severity** | Medium |
| **Category** | Floating-Point Equality |

**Evidence:**
```java
@Override
public int hashCode() {
    final int prime = 31;
    int result = 1;
    long temp;
    temp = Double.doubleToLongBits(x);
    result = prime * result + (int) (temp ^ (temp >>> 32));
    temp = Double.doubleToLongBits(y);
    result = prime * result + (int) (temp ^ (temp >>> 32));
    return result;
}

@Override
public boolean equals(Object obj) {
    ...
    if (Double.doubleToLongBits(x) != Double.doubleToLongBits(other.x))
        return false;
    if (Double.doubleToLongBits(y) != Double.doubleToLongBits(other.y))
        return false;
    return true;
}
```

**Description:** The `Points` class is used as a `HashMap` key in `GridCluster.reducePoints()`. The `equals`/`hashCode` methods use `Double.doubleToLongBits` for exact bitwise comparison. While this is technically correct for hash map usage (it is deterministic and consistent), it means that two `Points` that differ by even 1 ULP will not match. Given that these points come from floating-point arithmetic in `simplePoints()` (which involves division and multiplication), there is a risk that rounding differences could cause logically identical grid cells to hash differently. The `simplePoints` method performs `((int)(x/mod)) * mod + mod/2` which should produce deterministic results for the same input, but any upstream floating-point variance would cause misses.

---

### CQ-RTLS-12 -- Potential division by zero in `calculateStdev`

| Field | Value |
|-------|-------|
| **File** | `GridCluster.java` |
| **Lines** | 62, 68 |
| **Severity** | High |
| **Category** | Error Handling / Algorithm Correctness |

**Evidence:**
```java
double mean = sum/length;                    // line 62 -- division by zero if hashPoints is empty
...
stdev = Math.sqrt(stdev/(length-1));         // line 68 -- division by zero if hashPoints has exactly 1 entry
```

**Description:** If `hashPoints` is empty (`length == 0`), line 62 divides by zero. If `hashPoints` has exactly one entry (`length == 1`), line 68 divides by zero (`length - 1 == 0`). Neither case is guarded. The method returns a `String` via `DecimalFormat`, so a `NaN` or `Infinity` result would propagate as a formatted string like `"NaN"` or `"Infinity"`, which would likely break downstream consumers.

---

### CQ-RTLS-13 -- No convergence guard in Vincenty iteration loop

| Field | Value |
|-------|-------|
| **File** | `LonLatConverter.java` |
| **Lines** | 80-88 |
| **Severity** | Medium |
| **Category** | Algorithm Correctness |

**Evidence:**
```java
double sigma = dist / (b * A), sigmaP = 2 * Math.PI;
while (Math.abs(sigma - sigmaP) > 1e-12) {
    cos2SigmaM = Math.cos(2 * sigma1 + sigma);
    sinSigma = Math.sin(sigma);
    cosSigma = Math.cos(sigma);
    double deltaSigma = B * sinSigma * (...);
    sigmaP = sigma;
    sigma = dist / (b * A) + deltaSigma;
}
```

**Description:** The Vincenty iteration has no maximum-iteration guard. For nearly antipodal points, the Vincenty direct formula can fail to converge. Without a cap (e.g., `maxIterations = 200`), this loop could run indefinitely, hanging the request thread.

---

### CQ-RTLS-14 -- Public mutable fields on `LonLatConverter`

| Field | Value |
|-------|-------|
| **File** | `LonLatConverter.java` |
| **Lines** | 13, 14 |
| **Severity** | Medium |
| **Category** | Encapsulation / Style |

**Evidence:**
```java
public  double oringin_lon = 150.95866482248996;
public  double oringin_lat = -33.922175999995076;
```

**Description:** The origin coordinates are declared `public` and non-final, even though getters and setters exist (lines 19-33). This allows callers to bypass setters entirely and mutate the fields directly, defeating encapsulation. These fields should be `private`.

---

### CQ-RTLS-15 -- Non-final instance fields for WGS-84 constants

| Field | Value |
|-------|-------|
| **File** | `LonLatConverter.java` |
| **Lines** | 9-11 |
| **Severity** | Low |
| **Category** | Style / Encapsulation |

**Evidence:**
```java
private double a = 6378137;
private double b = 6356752.3142;
private double f = 1 / 298.2572236;
```

**Description:** The WGS-84 semi-major axis `a`, semi-minor axis `b`, and flattening `f` are physical constants. They should be `private static final` with descriptive names (e.g., `WGS84_SEMI_MAJOR_AXIS`). Currently they are mutable instance fields, so every `LonLatConverter` instance carries redundant copies, and they could theoretically be changed at runtime.

---

### CQ-RTLS-16 -- Underscore-prefixed field names in `MovingAverage`

| Field | Value |
|-------|-------|
| **File** | `MovingAverage.java` |
| **Lines** | 7-10 |
| **Severity** | Low |
| **Category** | Naming / Style |

**Evidence:**
```java
int _size = 0;
int _index = 0;
double _sum = 0.0;
Queue<Double> _queue = new LinkedList<Double>();
```

**Description:** Underscore-prefixed field names (`_size`, `_index`, `_sum`, `_queue`) are not standard Java naming convention. Java convention uses plain camelCase for instance fields. Additionally, all four fields have package-private (default) access rather than `private`.

---

### CQ-RTLS-17 -- Package-private fields across bean classes

| Field | Value |
|-------|-------|
| **File** | `ShockBean.java` |
| **Lines** | 12-14, 16, 29 |
| **Severity** | Low |
| **Category** | Encapsulation / Style |

**Evidence:**
```java
int shockId;                     // line 12
String date_time;                // line 13
int veh_cd;                      // line 14
boolean location_cached;         // line 16
boolean speed_cached;            // line 29
```

**Description:** All five fields in `ShockBean` have default (package-private) access rather than `private`, despite having public getters and setters. This is inconsistent with `SpeedBean` and `SessionBean` where fields are properly declared `private`.

---

### CQ-RTLS-18 -- Field declared after methods in `ShockBean` and `Tags`

| Field | Value |
|-------|-------|
| **Files** | `ShockBean.java` (line 29), `Tags.java` (line 25) |
| **Severity** | Low |
| **Category** | Style |

**Evidence (ShockBean.java):**
```java
public void setSpeed_cached(boolean speed_cached) {   // line 27
    this.speed_cached = speed_cached;                  // line 28
}
boolean speed_cached;                                  // line 29 -- field declared AFTER its setter
```

**Evidence (Tags.java):**
```java
public void setAlias(String alias) {   // line 22
    this.alias = alias;                // line 23
}
private String alias;                  // line 25 -- field declared AFTER its setter
```

**Description:** Fields are declared after the methods that use them, violating the standard Java convention of fields-before-methods ordering. This makes the classes harder to scan.

---

### CQ-RTLS-19 -- Snake_case naming in bean fields and methods

| Field | Value |
|-------|-------|
| **Files** | `SessionBean.java`, `ShockBean.java` |
| **Severity** | Low |
| **Category** | Naming / Style |

**Evidence (SessionBean.java):**
```java
private int veh_cd;
private Timestamp st_dt;
private Timestamp to_dt;
public int getVeh_cd() { ... }
public void setVeh_cd(int veh_cd) { ... }
public Timestamp getSt_dt() { ... }
public void setSt_dt(Timestamp st_dt) { ... }
public Timestamp getTo_dt() { ... }
public void setTo_dt(Timestamp to_dt) { ... }
```

**Evidence (ShockBean.java):**
```java
String date_time;
int veh_cd;
boolean location_cached;
boolean speed_cached;
```

**Description:** Multiple fields and their corresponding getters/setters use `snake_case` naming (`veh_cd`, `st_dt`, `to_dt`, `date_time`, `location_cached`, `speed_cached`). Java convention requires `camelCase` for field and method names. These likely mirror database column names, but the Java bean layer should use idiomatic Java names.

---

### CQ-RTLS-20 -- `String` type used for `date_time` in `ShockBean`

| Field | Value |
|-------|-------|
| **File** | `ShockBean.java` |
| **Line** | 13 |
| **Severity** | Medium |
| **Category** | Type Safety |

**Evidence:**
```java
String date_time;
```

**Description:** The `date_time` field is stored as a `String` rather than `java.sql.Timestamp` (which is imported but unused -- see CQ-RTLS-09). This loses type safety, makes date arithmetic impossible without re-parsing, and is inconsistent with the other beans (`SessionBean`, `SpeedBean`, `Points`) which all use `Timestamp` for their date/time fields.

---

### CQ-RTLS-21 -- `Double.parseDouble` on unvalidated `String density`

| Field | Value |
|-------|-------|
| **File** | `GridCluster.java` |
| **Line** | 31 |
| **Severity** | Medium |
| **Category** | Error Handling |

**Evidence:**
```java
Points spt = simplePoints(pt, Double.parseDouble(density)/100);
```

**Description:** The `density` parameter is a `String` that is parsed to `double` inside the loop on every iteration, with no validation. If `density` is null, empty, or non-numeric, a `NumberFormatException` will be thrown. If `density` is `"0"`, the result is a division by zero in `simplePoints`. The parse should be performed once before the loop with appropriate validation.

---

### CQ-RTLS-22 -- Redundant parsing of `density` inside loop

| Field | Value |
|-------|-------|
| **File** | `GridCluster.java` |
| **Lines** | 28-31 |
| **Severity** | Low |
| **Category** | Performance / Style |

**Evidence:**
```java
for(int i=0;i< arrPoints.size();i++)
{
    Points pt = arrPoints.get(i);
    Points spt = simplePoints(pt, Double.parseDouble(density)/100);
```

**Description:** `Double.parseDouble(density)/100` is evaluated on every iteration of the loop. The `density` string does not change, so the parsed value should be computed once before the loop.

---

### CQ-RTLS-23 -- Missing `@Override` on `hashCode` and `equals` (style only, annotations present)

This check was performed. The `Points` class correctly includes `@Override` on both `hashCode()` (line 60) and `equals()` (line 72). No issue found.

---

### CQ-RTLS-24 -- Extra blank lines in `SpeedBean`

| Field | Value |
|-------|-------|
| **File** | `SpeedBean.java` |
| **Lines** | 36-40 |
| **Severity** | Info |
| **Category** | Style |

**Evidence:**
```java
	public void setAt(Timestamp at) {
		this.at = at;
	}






}
```

**Description:** Five lines of unnecessary whitespace at the end of the class body. Minor style issue.

---

### CQ-RTLS-25 -- Inconsistent indentation in `GridCluster`

| Field | Value |
|-------|-------|
| **File** | `GridCluster.java` |
| **Lines** | 13-19 vs 21-44 vs 47-74 |
| **Severity** | Info |
| **Category** | Style |

**Description:** The `simplePoints` method body is indented with two extra tab levels (three tabs total), while `reducePoints` uses a different indentation depth, and `calculateStdev` uses yet another mix. The loop contents in `calculateStdev` (lines 58-73) are indented with three tabs, mixing with the method body at two tabs. This inconsistency suggests copy-paste from different sources.

---

### CQ-RTLS-26 -- Logger declared non-final

| Field | Value |
|-------|-------|
| **Files** | `GridCluster.java` (line 11), `LonLatConverter.java` (line 7) |
| **Severity** | Low |
| **Category** | Style |

**Evidence:**
```java
private  static Logger log = org.apache.logging.log4j.LogManager.getLogger();
```

**Description:** The logger is `static` but not `final`. Standard practice is `private static final Logger`. Being non-final means it could be reassigned at runtime.

---

### CQ-RTLS-27 -- `simplePoints` method truncates with `(int)` cast

| Field | Value |
|-------|-------|
| **File** | `GridCluster.java` |
| **Lines** | 15-16 |
| **Severity** | Medium |
| **Category** | Algorithm Correctness |

**Evidence:**
```java
double x = ((int)(points.getX()/mod)) * mod + mod/2;
double y = ((int)(points.getY()/mod)) * mod + mod/2;
```

**Description:** The `(int)` cast truncates toward zero, not toward negative infinity. For negative coordinate values (e.g., `x = -0.3`, `mod = 1.0`), `(int)(-0.3)` is `0`, not `-1`, so the grid cell assignment would be incorrect for any points with negative coordinates. Since the origin lat in `LonLatConverter` is `-33.92...` (Southern Hemisphere), negative values are expected in the coordinate system. `Math.floor()` should be used instead of `(int)` to correctly handle negative values.

---

## Summary

| Severity | Count | IDs |
|----------|-------|-----|
| **High** | 1 | CQ-RTLS-12 |
| **Medium** | 7 | CQ-RTLS-01, 02, 04, 11, 13, 14, 20, 21, 27 |
| **Low** | 9 | CQ-RTLS-03, 05, 06, 07, 08, 15, 16, 17, 19, 22, 26 |
| **Info** | 2 | CQ-RTLS-24, 25 |
| **Total** | **19** | (CQ-RTLS-10, CQ-RTLS-23 confirmed clean) |

### Top Risks

1. **CQ-RTLS-12 (High):** `calculateStdev` will divide by zero if called with an empty or single-element map, producing `NaN`/`Infinity` strings.
2. **CQ-RTLS-27 (Medium):** `(int)` truncation in `simplePoints` causes incorrect grid-cell assignment for negative coordinates; should be `Math.floor()`.
3. **CQ-RTLS-13 (Medium):** Vincenty iteration loop has no max-iteration guard and can loop forever for pathological inputs.
4. **CQ-RTLS-21 (Medium):** Unvalidated `String` to `double` parse of `density` inside a loop, with no null/format/zero check.
5. **CQ-RTLS-01/02 (Medium):** Misspelled public API names (`computerThatLonLat`, `oringin`) baked into the public interface.

---

*Audit agent A17 -- Pass 4 complete. Report only; no fixes applied.*
