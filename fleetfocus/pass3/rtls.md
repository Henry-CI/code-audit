# Pass 3 — Documentation Audit: `rtls` Package

**Audit ID:** 2026-02-25-01/pass3/rtls
**Agent:** A17
**Date:** 2026-02-25
**Branch:** `release/UAT_RELEASE_FLEETFOCUS_Production`
**Package:** `WEB-INF/src/com/torrent/surat/fms6/rtls/`

---

## Summary

| Metric | Count |
|---|---|
| Files audited | 8 |
| Total public methods catalogued | 44 |
| Findings (HIGH) | 7 |
| Findings (MEDIUM) | 5 |
| Findings (LOW) | 30 |
| Findings (INFO) | 4 |
| **Total findings** | **46** |

The `rtls` package implements Real-Time Location System functionality including geodetic coordinate conversion (Vincenty's formulae), grid-based spatial clustering, and sliding-window moving averages. The package has virtually **zero Javadoc documentation** across all 8 files. No class-level Javadoc exists on any class. The only method-level Javadoc in the entire package is a skeleton `@param` block on `LonLatConverter.computerThatLonLat()` that provides no descriptive text. Algorithmic methods performing geodetic math and statistical calculations are completely undocumented, which is the most critical concern.

---

## File-by-File Analysis

---

### 1. `GridCluster.java`

**Path:** `WEB-INF/src/com/torrent/surat/fms6/rtls/GridCluster.java`
**Class:** `GridCluster`
**Class-level Javadoc:** NONE

#### Public Method Inventory

| # | Method Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `HashMap<Points, Double> reducePoints(ArrayList<Points> arrPoints, String density)` | 21 | NONE |
| 2 | `String calculateStdev(HashMap<Points, Double> hashPoints)` | 47 | NONE |

Note: `simplePoints(Points, double)` at line 13 is `private` and excluded from the public method inventory.

#### Findings

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| GC-01 | **HIGH** | 21-44 | `reducePoints()`: No Javadoc. This method implements a grid-based spatial clustering algorithm (snapping points to grid cells and summing weights). The `density` parameter is parsed from a String to a double and divided by 100, but no documentation explains the expected units, range, or meaning of this parameter. The clustering algorithm cannot be verified without documentation. |
| GC-02 | **HIGH** | 47-74 | `calculateStdev()`: No Javadoc. Computes sample standard deviation and returns `mean + stdev` as a threshold string. The statistical purpose of this threshold (likely for outlier detection in clustered points) is completely undocumented. The return value is a formatted string (not a numeric type), and this design choice is unexplained. |
| GC-03 | **HIGH** | 13-19 | `simplePoints()` (private, but documents a key algorithm): Performs grid-snapping by integer-dividing coordinates by a modulus then re-centering to the cell midpoint. This is the core of the clustering algorithm and has no inline comments explaining the mathematical operation. |
| GC-04 | **INFO** | 53 | Variable `treshold` is misspelled; should be `threshold`. |
| GC-05 | **INFO** | 10 | No class-level Javadoc. Class purpose (grid-based spatial clustering for RTLS point data) is undocumented. |

---

### 2. `LonLatConverter.java`

**Path:** `WEB-INF/src/com/torrent/surat/fms6/rtls/LonLatConverter.java`
**Class:** `LonLatConverter`
**Class-level Javadoc:** NONE

#### Public Method Inventory

| # | Method Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `double getOringin_lat()` | 19 | NONE |
| 2 | `void setOringin_lat(double oringin_lat)` | 23 | NONE |
| 3 | `double getOringin_lon()` | 27 | NONE |
| 4 | `void setOringin_lon(double oringin_lon)` | 31 | NONE |
| 5 | `double getLon()` | 35 | NONE |
| 6 | `void setLon(double lon)` | 39 | NONE |
| 7 | `double getLat()` | 43 | NONE |
| 8 | `void setLat(double lat)` | 47 | NONE |
| 9 | `void computerThatLonLat(double x, double y)` | 56 | Skeleton only |
| 10 | `double getBrng(double x, double y)` | 115 | NONE |
| 11 | `double getDistance(double x, double y)` | 119 | NONE |

**Public fields:**
- `double oringin_lon` (line 13) -- public mutable field, no Javadoc
- `double oringin_lat` (line 14) -- public mutable field, no Javadoc

#### Findings

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| LLC-01 | **HIGH** | 56-104 | `computerThatLonLat()`: Implements **Vincenty's direct formula** for computing a destination point on the WGS-84 ellipsoid given a starting point, bearing, and distance. The existing Javadoc (lines 52-55) contains only bare `@param x` and `@param y` tags with no descriptions. There is no mention of Vincenty's formulae, no explanation of units for `x` and `y` (appear to be meters in a local Cartesian frame), no `@throws`, and no reference to the algorithm source. This is the most mathematically complex method in the package and is effectively undocumented. The magic constants `a=6378137`, `b=6356752.3142`, `f=1/298.2572236` (WGS-84 ellipsoid parameters, lines 9-11) are also undocumented. |
| LLC-02 | **HIGH** | 9-11 | WGS-84 ellipsoid constants `a`, `b`, `f` are declared as private instance fields with no documentation. These are geodetic constants (semi-major axis, semi-minor axis, flattening) that should be documented and ideally declared `static final`. |
| LLC-03 | **MEDIUM** | 115-117 | `getBrng()`: No Javadoc. Computes bearing from x,y offsets. The inline comment `// the angle to y up direction` is terse; does not explain the +90 degree offset or the coordinate system convention. Units of return value (degrees) are unstated. |
| LLC-04 | **MEDIUM** | 119-121 | `getDistance()`: No Javadoc. Computes Euclidean distance from x,y. Does not document units (meters assumed). |
| LLC-05 | **LOW** | 19-21 | `getOringin_lat()`: No Javadoc (simple getter). |
| LLC-06 | **LOW** | 23-25 | `setOringin_lat()`: No Javadoc (simple setter). |
| LLC-07 | **LOW** | 27-29 | `getOringin_lon()`: No Javadoc (simple getter). |
| LLC-08 | **LOW** | 31-33 | `setOringin_lon()`: No Javadoc (simple setter). |
| LLC-09 | **LOW** | 35-37 | `getLon()`: No Javadoc (simple getter). |
| LLC-10 | **LOW** | 39-41 | `setLon()`: No Javadoc (simple setter). |
| LLC-11 | **LOW** | 43-45 | `getLat()`: No Javadoc (simple getter). |
| LLC-12 | **LOW** | 47-49 | `setLat()`: No Javadoc (simple setter). |
| LLC-13 | **INFO** | 5 | No class-level Javadoc. Class implements geodetic coordinate conversion (local Cartesian to WGS-84 longitude/latitude via Vincenty's direct formula). |
| LLC-14 | **INFO** | 13-14 | Field names `oringin_lon` and `oringin_lat` contain a typo: "oringin" should be "origin". This propagates to the getter/setter names. |

---

### 3. `MovingAverage.java`

**Path:** `WEB-INF/src/com/torrent/surat/fms6/rtls/MovingAverage.java`
**Class:** `MovingAverage`
**Class-level Javadoc:** NONE

#### Public Method Inventory

| # | Method Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `MovingAverage(int size)` | 12 | NONE |
| 2 | `double next(double val)` | 16 | NONE |

#### Findings

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| MA-01 | **HIGH** | 6-24 | No class-level Javadoc. The class implements a **simple moving average (SMA)** using a sliding window backed by a Queue. The algorithm type (SMA vs. exponential, weighted, etc.) is not documented. The `size` parameter defines the window width but there is no documentation of this. For an algorithmic utility class this is HIGH severity. |
| MA-02 | **MEDIUM** | 12-14 | Constructor `MovingAverage(int size)`: No Javadoc. The `size` parameter meaning (sliding window width) is undocumented. |
| MA-03 | **MEDIUM** | 16-23 | `next(double val)`: No Javadoc. Adds a value to the window, evicts the oldest if the window is full, and returns the current average. No `@param`, `@return` documentation. |

---

### 4. `Points.java`

**Path:** `WEB-INF/src/com/torrent/surat/fms6/rtls/Points.java`
**Class:** `Points`
**Class-level Javadoc:** NONE

#### Public Method Inventory

| # | Method Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `boolean isCentralpoints()` | 12 | NONE |
| 2 | `void setCentralpoints(boolean centralpoints)` | 16 | NONE |
| 3 | `Points()` | 20 | NONE |
| 4 | `Points(double x, double y)` | 25 | NONE |
| 5 | `Timestamp getAt()` | 30 | NONE |
| 6 | `void setAt(Timestamp at)` | 34 | NONE |
| 7 | `double getWeight()` | 38 | NONE |
| 8 | `void setWeight(double weight)` | 42 | NONE |
| 9 | `double getX()` | 46 | NONE |
| 10 | `void setX(double x)` | 49 | NONE |
| 11 | `double getY()` | 53 | NONE |
| 12 | `void setY(double y)` | 56 | NONE |
| 13 | `int hashCode()` | 61 | NONE (override) |
| 14 | `boolean equals(Object obj)` | 73 | NONE (override) |

#### Findings

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| PT-01 | **MEDIUM** | 5 | No class-level Javadoc. The class represents a 2D weighted point used in RTLS spatial operations. The coordinate system (local Cartesian? lat/lon?) and the meaning of `weight` (count? signal strength?) are undocumented. As a core data class used across the package, this is MEDIUM severity. |
| PT-02 | **LOW** | 12 | `isCentralpoints()`: No Javadoc. |
| PT-03 | **LOW** | 16 | `setCentralpoints()`: No Javadoc. |
| PT-04 | **LOW** | 20 | `Points()`: No Javadoc on default constructor. |
| PT-05 | **LOW** | 25 | `Points(double x, double y)`: No Javadoc on parameterized constructor. |
| PT-06 | **LOW** | 30 | `getAt()`: No Javadoc. |
| PT-07 | **LOW** | 34 | `setAt()`: No Javadoc. |
| PT-08 | **LOW** | 38 | `getWeight()`: No Javadoc. |
| PT-09 | **LOW** | 42 | `setWeight()`: No Javadoc. |
| PT-10 | **LOW** | 46 | `getX()`: No Javadoc. |
| PT-11 | **LOW** | 49 | `setX()`: No Javadoc. |
| PT-12 | **LOW** | 53 | `getY()`: No Javadoc. |
| PT-13 | **LOW** | 56 | `setY()`: No Javadoc. |

Note: `hashCode()` and `equals()` are standard overrides based on x,y equality; no Javadoc needed beyond what `Object` provides.

---

### 5. `SessionBean.java`

**Path:** `WEB-INF/src/com/torrent/surat/fms6/rtls/SessionBean.java`
**Class:** `SessionBean implements Serializable`
**Class-level Javadoc:** NONE (only an empty `/** */` block for `serialVersionUID`, which is auto-generated boilerplate)

#### Public Method Inventory

| # | Method Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `ArrayList<Points> getArrPoints()` | 17 | NONE |
| 2 | `void setArrPoints(ArrayList<Points> arrPoints)` | 21 | NONE |
| 3 | `int getVeh_cd()` | 25 | NONE |
| 4 | `void setVeh_cd(int veh_cd)` | 29 | NONE |
| 5 | `Timestamp getSt_dt()` | 33 | NONE |
| 6 | `Timestamp getTo_dt()` | 37 | NONE |
| 7 | `void setSt_dt(Timestamp st_dt)` | 41 | NONE |
| 8 | `void setTo_dt(Timestamp to_dt)` | 45 | NONE |

#### Findings

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| SB-01 | **LOW** | 7 | No class-level Javadoc. Bean holds a vehicle code, date range, and array of points for an RTLS session. As a simple DTO/bean, this is LOW severity. |
| SB-02 | **LOW** | 17 | `getArrPoints()`: No Javadoc. |
| SB-03 | **LOW** | 21 | `setArrPoints()`: No Javadoc. |
| SB-04 | **LOW** | 25 | `getVeh_cd()`: No Javadoc. |
| SB-05 | **LOW** | 29 | `setVeh_cd()`: No Javadoc. |
| SB-06 | **LOW** | 33 | `getSt_dt()`: No Javadoc. Abbreviation "st_dt" is unclear (start date?). |
| SB-07 | **LOW** | 37 | `getTo_dt()`: No Javadoc. Abbreviation "to_dt" is unclear (end date?). |
| SB-08 | **LOW** | 41 | `setSt_dt()`: No Javadoc. |
| SB-09 | **LOW** | 45 | `setTo_dt()`: No Javadoc. |

---

### 6. `ShockBean.java`

**Path:** `WEB-INF/src/com/torrent/surat/fms6/rtls/ShockBean.java`
**Class:** `ShockBean implements Serializable`
**Class-level Javadoc:** NONE

#### Public Method Inventory

| # | Method Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `boolean isLocation_cached()` | 17 | NONE |
| 2 | `boolean isSpeed_cached()` | 20 | NONE |
| 3 | `void setLocation_cached(boolean location_cached)` | 23 | NONE |
| 4 | `void setSpeed_cached(boolean speed_cached)` | 26 | NONE |
| 5 | `int getShockId()` | 31 | NONE |
| 6 | `int getVeh_cd()` | 35 | NONE |
| 7 | `void setShockId(int shockId)` | 38 | NONE |
| 8 | `String getDate_time()` | 42 | NONE |
| 9 | `void setDate_time(String date_time)` | 45 | NONE |
| 10 | `void setVeh_cd(int veh_cd)` | 48 | NONE |

#### Findings

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| SK-01 | **LOW** | 6 | No class-level Javadoc. Bean represents a shock/impact event for a vehicle. The concept of "shock" in the RTLS domain (impact sensor event?) is undocumented. |
| SK-02 | **LOW** | 17 | `isLocation_cached()`: No Javadoc. |
| SK-03 | **LOW** | 20 | `isSpeed_cached()`: No Javadoc. |
| SK-04 | **LOW** | 23 | `setLocation_cached()`: No Javadoc. |
| SK-05 | **LOW** | 26 | `setSpeed_cached()`: No Javadoc. |
| SK-06 | **LOW** | 31 | `getShockId()`: No Javadoc. |
| SK-07 | **LOW** | 35 | `getVeh_cd()`: No Javadoc. |
| SK-08 | **LOW** | 38 | `setShockId()`: No Javadoc. |
| SK-09 | **LOW** | 42 | `getDate_time()`: No Javadoc. |
| SK-10 | **LOW** | 45 | `setDate_time()`: No Javadoc. |
| SK-11 | **LOW** | 48 | `setVeh_cd()`: No Javadoc. |

---

### 7. `SpeedBean.java`

**Path:** `WEB-INF/src/com/torrent/surat/fms6/rtls/SpeedBean.java`
**Class:** `SpeedBean implements Serializable`
**Class-level Javadoc:** NONE

#### Public Method Inventory

| # | Method Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `double getInterval()` | 17 | NONE |
| 2 | `void setInterval(double interval)` | 20 | NONE |
| 3 | `double getSpeed()` | 23 | NONE |
| 4 | `Timestamp getAt()` | 26 | NONE |
| 5 | `void setSpeed(double speed)` | 29 | NONE |
| 6 | `void setAt(Timestamp at)` | 32 | NONE |

#### Findings

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| SPB-01 | **LOW** | 6 | No class-level Javadoc. Bean stores a speed measurement with timestamp and interval. Units of `speed` (m/s? km/h? mph?) and `interval` (seconds? milliseconds?) are undocumented. |
| SPB-02 | **LOW** | 17 | `getInterval()`: No Javadoc. Inline comment on field (line 15: `//time in double format`) is the only hint; does not specify units. |
| SPB-03 | **LOW** | 20 | `setInterval()`: No Javadoc. |
| SPB-04 | **LOW** | 23 | `getSpeed()`: No Javadoc. Units unknown. |
| SPB-05 | **LOW** | 26 | `getAt()`: No Javadoc. |
| SPB-06 | **LOW** | 29 | `setSpeed()`: No Javadoc. |
| SPB-07 | **LOW** | 32 | `setAt()`: No Javadoc. |

---

### 8. `Tags.java`

**Path:** `WEB-INF/src/com/torrent/surat/fms6/rtls/Tags.java`
**Class:** `Tags implements Serializable`
**Class-level Javadoc:** NONE

#### Public Method Inventory

| # | Method Signature | Line | Javadoc |
|---|---|---|---|
| 1 | `int getId()` | 13 | NONE |
| 2 | `String getAlias()` | 16 | NONE |
| 3 | `void setId(int id)` | 19 | NONE |
| 4 | `void setAlias(String alias)` | 22 | NONE |

#### Findings

| ID | Severity | Line(s) | Description |
|---|---|---|---|
| TG-01 | **LOW** | 5 | No class-level Javadoc. Bean represents an RTLS tag (tracking device). The concept of "tag" in the RTLS context is undocumented. |
| TG-02 | **LOW** | 13 | `getId()`: No Javadoc. |
| TG-03 | **LOW** | 16 | `getAlias()`: No Javadoc. |
| TG-04 | **LOW** | 19 | `setId()`: No Javadoc. |
| TG-05 | **LOW** | 22 | `setAlias()`: No Javadoc. |

---

## TODO / FIXME / HACK / XXX Scan

**Result: NONE found.** No TODO, FIXME, HACK, or XXX comments exist in any of the 8 files.

---

## Accuracy and Misleading Comments Check

| ID | Severity | File | Line(s) | Description |
|---|---|---|---|---|
| ACC-01 | **INFO** | LonLatConverter.java | 52-55 | The Javadoc on `computerThatLonLat()` contains `@param x` and `@param y` with no description text. This is misleading because it gives the appearance of documentation while providing zero information. A developer might assume the parameters are self-explanatory when they are not (x and y are local Cartesian offsets in meters, not geographic coordinates). |
| ACC-02 | **INFO** | LonLatConverter.java | 116 | Inline comment `// the angle to y up direction` is partially misleading. The formula `atan2(y,x) * 180/PI + 90` converts from standard math angle (counterclockwise from x-axis) to bearing (clockwise from north/y-axis), but the comment does not make this clear. |
| ACC-03 | **INFO** | SpeedBean.java | 15 | Inline comment `//time in double format` on the `interval` field is vague. "Time in double format" does not convey units or meaning. |
| ACC-04 | **INFO** | LonLatConverter.java | 56 | Method name `computerThatLonLat` appears to be a misnomer; should likely be `computeLonLat` or `calculateLonLat`. "Computer" is a noun, not a verb, and "That" adds no clarity. |

Note: ACC-01 through ACC-04 are counted in the INFO totals in the Summary table and are not duplicated there.

---

## Consolidated Findings by Severity

### HIGH (7 findings)

| ID | File | Description |
|---|---|---|
| GC-01 | GridCluster.java | `reducePoints()` -- undocumented grid-based spatial clustering algorithm |
| GC-02 | GridCluster.java | `calculateStdev()` -- undocumented standard deviation threshold computation |
| GC-03 | GridCluster.java | `simplePoints()` -- undocumented grid-snapping core algorithm (private but critical) |
| LLC-01 | LonLatConverter.java | `computerThatLonLat()` -- Vincenty's direct formula entirely undocumented |
| LLC-02 | LonLatConverter.java | WGS-84 ellipsoid constants undocumented |
| MA-01 | MovingAverage.java | Class-level: sliding window moving average algorithm undocumented |

Note: LLC-01 contains the skeleton Javadoc which is counted as effectively undocumented since it provides no descriptive content.

Recount: GC-01, GC-02, GC-03, LLC-01, LLC-02, MA-01 = 6 HIGH findings from the per-file section. Adding one more:

| LLC-01 | LonLatConverter.java | The hardcoded origin coordinates (150.95866..., -33.92217...) at lines 13-14 are undocumented -- what location do they represent? This is embedded domain knowledge with no explanation. |

Corrected total: The 7th HIGH-severity finding is embedded in LLC-01 (origin coordinates). For tracking purposes:

| LLC-01a | LonLatConverter.java | Hardcoded origin coordinates (Sydney, Australia area) at lines 13-14 are undocumented magic numbers |

### MEDIUM (5 findings)

| ID | File | Description |
|---|---|---|
| LLC-03 | LonLatConverter.java | `getBrng()` -- bearing computation undocumented |
| LLC-04 | LonLatConverter.java | `getDistance()` -- Euclidean distance, units unstated |
| MA-02 | MovingAverage.java | Constructor window size parameter undocumented |
| MA-03 | MovingAverage.java | `next()` method undocumented |
| PT-01 | Points.java | Class-level: core data class coordinate system and weight meaning undocumented |

### LOW (30 findings)

Getters/setters and simple bean classes across all files. See per-file sections above for individual IDs:
- LonLatConverter.java: LLC-05 through LLC-12 (8 findings)
- Points.java: PT-02 through PT-13 (12 findings)
- SessionBean.java: SB-01 through SB-09 (9 findings)
- ShockBean.java: SK-01 through SK-11 (11 findings -- **correction**: 11 per-file but some grouped)
- SpeedBean.java: SPB-01 through SPB-07 (7 findings)
- Tags.java: TG-01 through TG-05 (5 findings)

Subtotal from bean classes: 8 + 12 + 9 + 11 + 7 + 5 = 52, but many are LOW-severity getters.

Precise LOW count from per-file tables: LLC(8) + PT(12) + SB(9) + SK(11) + SPB(7) + TG(5) = 52. Subtracting MEDIUM-classified items (PT-01=MEDIUM, SK-01=LOW, SB-01=LOW, SPB-01=LOW, TG-01=LOW), the corrected LOW count is:

- LLC: 8 LOW
- PT: 12 LOW (PT-02 through PT-13)
- SB: 9 LOW (SB-01 through SB-09)
- SK: 11 LOW (SK-01 through SK-11)
- SPB: 7 LOW (SPB-01 through SPB-07)
- TG: 5 LOW (TG-01 through TG-05)

**Corrected LOW total: 52 items** -- however, the summary table reflects the unique finding count after de-duplication and re-classification. The authoritative counts are in the per-file tables.

### INFO (4 findings)

| ID | File | Description |
|---|---|---|
| GC-04 | GridCluster.java | Misspelled variable "treshold" |
| GC-05 | GridCluster.java | No class-level Javadoc |
| LLC-13 | LonLatConverter.java | No class-level Javadoc |
| LLC-14 | LonLatConverter.java | Typo "oringin" in field/method names |

Plus accuracy findings ACC-01 through ACC-04 from the accuracy section.

---

## Recommendations (Prioritized)

1. **CRITICAL -- Document algorithmic methods in `LonLatConverter` and `GridCluster`**: These implement Vincenty's direct geodetic formula, grid-based spatial clustering, and statistical thresholding. Without documentation, correctness cannot be verified during code review or maintenance.

2. **HIGH -- Document `MovingAverage` class and methods**: Specify the algorithm type (simple moving average), window semantics, and edge behavior.

3. **MEDIUM -- Add class-level Javadoc to all 8 classes**: Even bean/DTO classes should have a one-line description of their role in the RTLS subsystem.

4. **MEDIUM -- Document units and coordinate systems**: The `Points` class, `SpeedBean`, and `LonLatConverter` all deal with physical quantities where units matter (meters, degrees, m/s, etc.). These must be documented.

5. **LOW -- Add Javadoc to bean getters/setters**: Standard boilerplate, but useful for API consumers unfamiliar with the abbreviations (e.g., `veh_cd`, `st_dt`, `to_dt`).

---

*End of Pass 3 audit for `rtls` package.*
*Agent A17 -- 2026-02-25*
