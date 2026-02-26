# Pass 2 Test Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A66
**Source files audited:**
- `src/main/java/com/calibration/UnitCalibrationImpactFilter.java`
- `src/main/java/com/calibration/UnitCalibrationStarter.java`

**Test file examined:**
- `src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java`

---

## Section 1: Reading Evidence

### 1.1 UnitCalibrationImpactFilter.java

**Class:** `UnitCalibrationImpactFilter` (package-private, line 5)

**Fields:** None declared on the class itself. Local variables only.

**Constants/Enums:** None.

**Methods:**

| Method | Visibility | Line | Signature |
|--------|-----------|------|-----------|
| `filterImpacts` | package-private | 6 | `List<Integer> filterImpacts(List<CalibrationImpact> impacts)` |
| `splitImpactsBy15MinutesOfSession` | private | 16 | `List<List<Integer>> splitImpactsBy15MinutesOfSession(List<CalibrationImpact> impacts)` |
| `compareImpacts` | private | 45 | `int compareImpacts(CalibrationImpact i1, CalibrationImpact i2)` |
| `getLargestImpact` | private | 50 | `Integer getLargestImpact(List<Integer> impacts)` |

**Key logic branches in `splitImpactsBy15MinutesOfSession` (lines 16-43):**
- Line 24: `if (impact.sessionStart.compareTo(sessionStart) != 0)` — new session detected
- Line 33: `if (impact.time.after(sectionEnd.getTime()))` — impact falls in a new 15-minute window
- Line 40: `Objects.requireNonNull(currentSection).add(impact.value)` — impact added to current section

**Key logic branches in `filterImpacts` (lines 6-14):**
- Line 11: `if (largest >= 80000)` — threshold filter; impacts at exactly 80000 are included, below 80000 are excluded

**Key logic in `getLargestImpact` (lines 50-56):**
- Returns `0` (Integer) when the list is empty (initial value never exceeded)

**Key logic in `compareImpacts` (lines 45-47):**
- Line 46: Uses reference inequality (`!=`) rather than `.equals()` for `sessionStart` Date comparison, then falls back to `.compareTo()`
- Line 47: Falls back to `i1.time.compareTo(i2.time)` for same-session ordering

---

### 1.2 UnitCalibrationStarter.java

**Type:** `public interface UnitCalibrationStarter` (line 5)

**Fields/Constants:** None.

**Methods:**

| Method | Visibility | Line | Signature |
|--------|-----------|------|-----------|
| `startCalibration` | public | 6 | `void startCalibration(long unitId) throws SQLException` |

---

### 1.3 Indirect Coverage Search Results

**Grep for `UnitCalibrationImpactFilter` in test directory:**
- Matches found only in `UnitCalibrationImpactFilterTest.java` (lines 11, 12, 16).

**Grep for `UnitCalibrationStarter` in test directory:**
- No matches found in any test file.

**Grep for method names (`filterImpacts`, `splitImpactsBy15`, `compareImpacts`, `getLargestImpact`) in test directory:**
- `filterImpacts` matched only in `UnitCalibrationImpactFilterTest.java` line 37.
- No matches for any private method names.

**Grep for `startCalibration` in test directory:**
- No matches found.

**Conclusion:** No indirect test coverage exists for either class beyond `UnitCalibrationImpactFilterTest.java`.

---

## Section 2: Test Coverage Analysis

### 2.1 What the Existing Test Covers

`UnitCalibrationImpactFilterTest` contains one test method:
- `returnsLargestImpactPer15MinutesOfSessionIfAbove80000`

This single test exercises `filterImpacts` with a fixed list of 8 impacts all belonging to a single session. The test verifies:
- The list is split into 15-minute windows within a session.
- The largest impact per window is selected.
- Only values >= 80000 are returned.
- The returned list contains `[91234, 101234]` for the given input.

---

## Section 3: Findings

### UnitCalibrationImpactFilter

---

**A66-1 | Severity: HIGH | `filterImpacts` — null input list not tested**

`filterImpacts(null)` is not covered. Passing `null` flows into `splitImpactsBy15MinutesOfSession`, where `impacts.sort(...)` at line 18 will throw a `NullPointerException`. There is no null guard. No test exercises this path.

---

**A66-2 | Severity: HIGH | `filterImpacts` — empty list input not tested**

`filterImpacts(Collections.emptyList())` is not covered. The loop in `splitImpactsBy15MinutesOfSession` never executes, `sections` is empty, `filtered` is empty, and an empty list is returned. The behaviour is likely correct but is completely untested. An empty return is a meaningful boundary result that should be asserted.

---

**A66-3 | Severity: HIGH | `splitImpactsBy15MinutesOfSession` — multiple sessions in one list not tested**

The single existing test uses only one session. The branch at line 24 (`if (impact.sessionStart.compareTo(sessionStart) != 0)`) — which handles a new session being encountered — is never exercised by the test. Multi-session input (impacts from two or more distinct sessions interleaved or ordered together) is entirely untested.

---

**A66-4 | Severity: HIGH | `splitImpactsBy15MinutesOfSession` — unsorted / out-of-order input not tested**

The method sorts the input list in-place via `impacts.sort(this::compareImpacts)` at line 18, mutating the caller's list if it is mutable. The existing test passes impacts already in chronological order, so the sort has no observable effect on the test outcome. No test verifies correct behaviour when impacts are provided out of order. This also means the sort logic (and `compareImpacts`) receives no meaningful test coverage.

---

**A66-5 | Severity: MEDIUM | `filterImpacts` — threshold boundary value exactly 80000 not tested**

The filter condition is `largest >= 80000` (line 11). The existing test includes values 81234, 91234, 85432 (above), 61234, 65432, 76543 (below), 101234 (above), and 80123 (above), but never a value of exactly `80000`. The boundary value itself — which is the inclusive edge of the condition — is untested.

---

**A66-6 | Severity: MEDIUM | `filterImpacts` — threshold boundary value 79999 (just below) not tested**

The value immediately below the threshold (`79999`) is not tested. Combined with A66-5, neither the exact boundary nor its adjacent value is covered, leaving the off-by-one risk unverified.

---

**A66-7 | Severity: MEDIUM | `splitImpactsBy15MinutesOfSession` — impact time exactly at 15-minute boundary not tested**

The branch at line 33 (`if (impact.time.after(sectionEnd.getTime()))`) uses strict `after`, meaning a time exactly equal to `sectionEnd` stays in the current section. No test exercises an impact whose timestamp is exactly at the 15-minute mark. This boundary is untested.

---

**A66-8 | Severity: MEDIUM | `splitImpactsBy15MinutesOfSession` — multiple consecutive 15-minute rollovers not tested**

The existing test has impacts at minutes 4, 5, 8, 13, 19, 24, 36, 44 within one session. This creates splits at approximately minute 18 and minute 33. A gap spanning more than one 15-minute window (e.g., a jump of 30+ minutes with no intervening impact) is not tested. In that scenario `sectionEnd` advances only by 15 minutes at line 34 (not by the full gap), so impacts far apart might be incorrectly bucketed or correctly handled — either way it is untested.

---

**A66-9 | Severity: MEDIUM | `getLargestImpact` — all negative values not tested**

`CalibrationImpact.value` is typed `int` (unboxed) and can be negative. `getLargestImpact` initialises `largest = 0` (Integer). If every impact in a section has a negative value, `getLargestImpact` returns `0` rather than the actual largest (least negative) value. This represents a latent bug and is entirely untested.

---

**A66-10 | Severity: MEDIUM | `getLargestImpact` — empty section list input not tested**

`getLargestImpact` is called for each section produced by `splitImpactsBy15MinutesOfSession`. By construction, each section always has at least one element (added immediately on creation at lines 30 and 37). However, there is no direct test of `getLargestImpact` with an empty list, and the returned value of `0` in that case would survive the `>= 80000` check (being below threshold), so the result would be silently dropped. The indirectness of this path is untested.

---

**A66-11 | Severity: MEDIUM | `compareImpacts` — reference equality used instead of `.equals()` for sessionStart comparison**

At line 46, `compareImpacts` uses `i1.sessionStart != i2.sessionStart` (reference inequality) before calling `.compareTo()`. Since `CalibrationImpact.sessionStart` is a `java.sql.Timestamp` (an object), two logically equal timestamps from different instances will not be reference-equal, causing the comparator to always take the `compareTo` branch for sort ordering, even when `sessionStart` dates are equal objects from different allocations. The test uses `new Timestamp(...)` in `CalibrationImpactFactory.makeImpact`, so within the same session all impacts share the same `sessionStart` object instance — masking this bug. No test constructs two impacts with equal-but-non-identical `sessionStart` instances to expose this reference vs. value comparison defect.

---

**A66-12 | Severity: MEDIUM | `splitImpactsBy15MinutesOfSession` — `Objects.requireNonNull` on `currentSection` at line 40 is untested for the throw path**

The `requireNonNull` call at line 40 guards against `currentSection` being null. `currentSection` starts as `null` and is only assigned when a new session or new 15-minute window is encountered. If the very first impact in the sorted list has a `sessionStart` that equals the initial `new Date()` (line 20) at the moment of execution (i.e., the impact's session start time happens to match `new Date()` to the millisecond), the new-session branch at line 24 would NOT be triggered, `currentSection` would remain `null`, and line 40 would throw `NullPointerException`. This race condition / time-dependent bug is untested.

---

**A66-13 | Severity: LOW | `splitImpactsBy15MinutesOfSession` — input list mutation (in-place sort) not tested**

`impacts.sort(...)` at line 18 mutates the caller-provided list if it is a mutable `List`. The test passes `Arrays.asList(...)`, which is fixed-size but does allow element reordering — though in this case the elements are already sorted, so no mutation occurs. No test verifies the mutation behaviour or passes an unmodifiable list to exercise a potential `UnsupportedOperationException`.

---

**A66-14 | Severity: LOW | `filterImpacts` — all impacts below threshold (returns empty list) not tested**

A scenario where every section's largest value is below 80000 — resulting in `filterImpacts` returning an empty list — is not tested. The existing test always expects a non-empty result.

---

**A66-15 | Severity: LOW | `filterImpacts` — single impact per section not tested as isolated scenario**

No test isolates the case of a list containing exactly one impact. The single-impact case exercises only one code path through both the section creation and the `getLargestImpact` loop, and its result under the threshold check is never asserted in isolation.

---

**A66-16 | Severity: INFO | `filterImpacts` — list with null elements not tested**

Passing a list that contains a `null` `CalibrationImpact` element is not tested. `impacts.sort(this::compareImpacts)` at line 18 would invoke `compareImpacts(null, ...)` or `compareImpacts(..., null)`, dereferencing `i1.sessionStart` or `i2.sessionStart`, causing a `NullPointerException`.

---

### UnitCalibrationStarter

---

**A66-17 | Severity: HIGH | `UnitCalibrationStarter` — zero test coverage; no tests exist for any implementation**

No test file anywhere in the test directory references `UnitCalibrationStarter` or `startCalibration`. The interface itself has no implementation tested. Any concrete class implementing this interface has no coverage verified against the interface contract.

---

**A66-18 | Severity: MEDIUM | `startCalibration` — SQLException contract is untested**

`startCalibration` declares `throws SQLException`. No test verifies that implementations propagate or handle `SQLException` correctly, and no test uses a mock or stub that throws `SQLException` to validate caller error handling.

---

**A66-19 | Severity: MEDIUM | `startCalibration` — boundary and invalid `unitId` values not tested**

No tests exercise `startCalibration` with:
- `unitId = 0` (zero/default)
- `unitId < 0` (negative / invalid)
- `unitId = Long.MAX_VALUE` (maximum long boundary)
- `unitId = Long.MIN_VALUE` (minimum long boundary)

---

**A66-20 | Severity: INFO | `UnitCalibrationStarter` — interface contract has no specification tests**

The interface carries no Javadoc or contract annotations describing expected behaviour for invalid unit IDs, idempotency, or re-entrancy. No contract/specification test exists to document expected outcomes.

---

## Summary Table

| Finding | Severity | Target Class | Area |
|---------|----------|-------------|------|
| A66-1 | HIGH | UnitCalibrationImpactFilter | Null input |
| A66-2 | HIGH | UnitCalibrationImpactFilter | Empty input |
| A66-3 | HIGH | UnitCalibrationImpactFilter | Multi-session branch |
| A66-4 | HIGH | UnitCalibrationImpactFilter | Unsorted input / sort coverage |
| A66-5 | MEDIUM | UnitCalibrationImpactFilter | Boundary: exactly 80000 |
| A66-6 | MEDIUM | UnitCalibrationImpactFilter | Boundary: 79999 |
| A66-7 | MEDIUM | UnitCalibrationImpactFilter | Boundary: exact 15-min mark |
| A66-8 | MEDIUM | UnitCalibrationImpactFilter | Multi-window gap > 15 min |
| A66-9 | MEDIUM | UnitCalibrationImpactFilter | All-negative values (latent bug) |
| A66-10 | MEDIUM | UnitCalibrationImpactFilter | getLargestImpact with empty list |
| A66-11 | MEDIUM | UnitCalibrationImpactFilter | Reference vs. value equality bug in compareImpacts |
| A66-12 | MEDIUM | UnitCalibrationImpactFilter | requireNonNull throw path / race condition |
| A66-13 | LOW | UnitCalibrationImpactFilter | In-place list mutation |
| A66-14 | LOW | UnitCalibrationImpactFilter | All impacts below threshold |
| A66-15 | LOW | UnitCalibrationImpactFilter | Single-impact list |
| A66-16 | INFO | UnitCalibrationImpactFilter | Null list elements |
| A66-17 | HIGH | UnitCalibrationStarter | Zero test coverage |
| A66-18 | MEDIUM | UnitCalibrationStarter | SQLException contract untested |
| A66-19 | MEDIUM | UnitCalibrationStarter | unitId boundary values |
| A66-20 | INFO | UnitCalibrationStarter | No interface contract tests |

**Total findings: 20**
**CRITICAL: 0 | HIGH: 5 | MEDIUM: 10 | LOW: 3 | INFO: 2**
