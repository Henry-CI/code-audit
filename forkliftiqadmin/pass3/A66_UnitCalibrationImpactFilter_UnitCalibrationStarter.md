# Pass 3 Documentation Audit — A66
**Audit run:** 2026-02-26-01
**Agent:** A66
**Files:**
- `src/main/java/com/calibration/UnitCalibrationImpactFilter.java`
- `src/main/java/com/calibration/UnitCalibrationStarter.java`

---

## Reading Evidence

### UnitCalibrationImpactFilter.java

**Class:**
| Name | Kind | Line | Visibility |
|---|---|---|---|
| `UnitCalibrationImpactFilter` | class | 5 | package-private |

**Fields:** none declared.

**Methods:**
| Name | Return Type | Line | Visibility | Parameters |
|---|---|---|---|---|
| `filterImpacts` | `List<Integer>` | 6 | package-private | `List<CalibrationImpact> impacts` |
| `splitImpactsBy15MinutesOfSession` | `List<List<Integer>>` | 16 | private | `List<CalibrationImpact> impacts` |
| `compareImpacts` | `int` | 45 | private | `CalibrationImpact i1, CalibrationImpact i2` |
| `getLargestImpact` | `Integer` | 50 | private | `List<Integer> impacts` |

---

### UnitCalibrationStarter.java

**Type:**
| Name | Kind | Line | Visibility |
|---|---|---|---|
| `UnitCalibrationStarter` | interface | 5 | public |

**Fields:** none.

**Methods:**
| Name | Return Type | Line | Visibility | Parameters | Throws |
|---|---|---|---|---|---|
| `startCalibration` | `void` | 6 | public | `long unitId` | `SQLException` |

---

## Findings

### A66-1 — LOW — No class-level Javadoc on `UnitCalibrationImpactFilter`

**File:** `UnitCalibrationImpactFilter.java`, line 5

`UnitCalibrationImpactFilter` has no class-level Javadoc comment. A brief description of the class's purpose (filtering calibration impact readings by 15-minute session windows and retaining only those above an 80,000 threshold) would aid maintainers.

```java
// line 5 — no Javadoc above
class UnitCalibrationImpactFilter {
```

---

### A66-2 — MEDIUM — Undocumented non-trivial package-private method `filterImpacts`

**File:** `UnitCalibrationImpactFilter.java`, line 6

`filterImpacts` is a non-trivial package-private method with no Javadoc. It orchestrates splitting impacts into 15-minute sections and retaining only sections whose largest impact value meets or exceeds 80,000. The threshold value, the sectioning strategy, and the meaning of the return value (a list of qualifying peak impact values, one per section) are not documented anywhere.

```java
// line 6 — no Javadoc
List<Integer> filterImpacts(List<CalibrationImpact> impacts) {
```

---

### A66-3 — HIGH — Incorrect reference-equality comparison on `Date` objects in `compareImpacts`

**File:** `UnitCalibrationImpactFilter.java`, line 46

`compareImpacts` uses the `!=` operator to compare two `Date` field values (`i1.sessionStart` and `i2.sessionStart`). `!=` tests object reference identity, not value equality. Two `Date` objects representing the same instant but held as distinct instances will compare as `!=`, causing the comparator to fall into the `i1.sessionStart.compareTo(i2.sessionStart)` branch even when the session starts are logically equal. Conversely, two references to the *same* object will compare as `==` and skip the branch, hiding any ordering differences within that session.

This means the sort in `splitImpactsBy15MinutesOfSession` (line 18) produces incorrect ordering whenever `CalibrationImpact` objects carry equal-valued but non-identical `sessionStart` instances, which is the common case (e.g., objects deserialized or constructed separately). The downstream sectioning logic then produces incorrect sections and the filtered output is corrupted.

The correct test is `.compareTo()` returning non-zero (already available) or `.equals()`:

```java
// line 45-48 — current (incorrect)
private int compareImpacts(CalibrationImpact i1, CalibrationImpact i2) {
    if (i1.sessionStart != i2.sessionStart) return i1.sessionStart.compareTo(i2.sessionStart);
    return i1.time.compareTo(i2.time);
}

// correct form
private int compareImpacts(CalibrationImpact i1, CalibrationImpact i2) {
    int cmp = i1.sessionStart.compareTo(i2.sessionStart);
    if (cmp != 0) return cmp;
    return i1.time.compareTo(i2.time);
}
```

---

### A66-4 — MEDIUM — Sliding section-end window in `splitImpactsBy15MinutesOfSession` may produce unexpected section boundaries

**File:** `UnitCalibrationImpactFilter.java`, line 33-39

When an impact falls after the current section end, the code advances `sectionEnd` by 15 minutes from its *current* value (line 34: `sectionEnd.add(Calendar.MINUTE, 15)`), not from the impact's own `time`. This means that if there is a gap larger than 15 minutes between impacts, the new section boundary is set to a time that may still be before `impact.time`, and the impact would be placed in a section window that technically does not contain it. Successive gaps compound the drift.

A correct implementation would anchor the new section end to `impact.time + 15 minutes` rather than `previousSectionEnd + 15 minutes`. There is no documentation explaining the chosen sliding-window behaviour, so it is not possible to determine whether this is intentional.

```java
// line 33-39
if (impact.time.after(sectionEnd.getTime())) {
    sectionEnd.add(Calendar.MINUTE, 15);   // <-- advances from previous boundary, not from impact.time
    currentSection = new ArrayList<>();
    sections.add(currentSection);
    currentSection.add(impact.value);
    continue;
}
```

---

### A66-5 — LOW — `getLargestImpact` initialises baseline to `0`, silently returns `0` for empty or all-negative input

**File:** `UnitCalibrationImpactFilter.java`, line 51

`getLargestImpact` initialises `largest` to `0` rather than `Integer.MIN_VALUE` or to the first element. If `impacts` is empty, the method returns `0`. The caller in `filterImpacts` (line 11) then tests `largest >= 80000`, which fails for `0`, so an empty section is not added — this is benign in the current calling context. However, if negative impact values are ever valid inputs, this method would incorrectly return `0` as the "largest" value. The behaviour is undocumented and relies on an implicit assumption about the value domain.

```java
// line 50-56
private Integer getLargestImpact(List<Integer> impacts) {
    Integer largest = 0;   // implicit assumption: all valid impacts are non-negative
    for (Integer impact : impacts) {
        if (impact > largest) largest = impact;
    }
    return largest;
}
```

---

### A66-6 — LOW — No interface-level Javadoc on `UnitCalibrationStarter`

**File:** `UnitCalibrationStarter.java`, line 5

The public interface `UnitCalibrationStarter` has no class-level Javadoc. Its purpose and expected contract (triggering a calibration process for a given unit) are not described.

```java
// line 5 — no Javadoc above
public interface UnitCalibrationStarter {
```

---

### A66-7 — MEDIUM — Undocumented public interface method `startCalibration`

**File:** `UnitCalibrationStarter.java`, line 6

The sole public method of this interface, `startCalibration`, has no Javadoc. The parameter `unitId`, the `SQLException` that can be thrown, and the side effects of calling this method are entirely undocumented. As a public interface contract, this is the primary API surface and should describe at minimum: what `unitId` identifies, what constitutes a successful invocation, and when `SQLException` is raised.

```java
// line 6 — no Javadoc
void startCalibration(long unitId) throws SQLException;
```

Required tags that are absent:
- `@param unitId`
- `@throws SQLException`

---

## Summary Table

| ID | Severity | File | Line | Description |
|---|---|---|---|---|
| A66-1 | LOW | UnitCalibrationImpactFilter.java | 5 | No class-level Javadoc |
| A66-2 | MEDIUM | UnitCalibrationImpactFilter.java | 6 | Undocumented non-trivial package-private method `filterImpacts` |
| A66-3 | HIGH | UnitCalibrationImpactFilter.java | 46 | Reference equality (`!=`) used on `Date` objects in `compareImpacts`; causes incorrect sort and corrupted output |
| A66-4 | MEDIUM | UnitCalibrationImpactFilter.java | 33–39 | Sliding section-end window may produce incorrect section boundaries on large gaps |
| A66-5 | LOW | UnitCalibrationImpactFilter.java | 51 | `getLargestImpact` baseline of `0` silently wrong for empty or all-negative input |
| A66-6 | LOW | UnitCalibrationStarter.java | 5 | No interface-level Javadoc |
| A66-7 | MEDIUM | UnitCalibrationStarter.java | 6 | Undocumented public interface method `startCalibration`; missing `@param` and `@throws` |
