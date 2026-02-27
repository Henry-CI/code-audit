# Pass 4 Code Quality — Agent A54
**Audit run:** 2026-02-26-01
**Agent:** A54
**Date:** 2026-02-27

---

## Section 1: Reading Evidence

### File 1: DriversActivity.java
**Path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/DriversActivity.java`
**Lines:** 1–18

**Class:** `DriversActivity extends FleetActivity`

**Methods:**
| Method | Line |
|---|---|
| `onCreate(Bundle)` | 13 |

**Types / Constants / Interfaces defined:** none

**Imports:**
- `android.os.Bundle` (used)
- `au.com.collectiveintelligence.fleetiq360.R` (used)
- `au.com.collectiveintelligence.fleetiq360.ui.common.FleetActivity` (used)
- `au.com.collectiveintelligence.fleetiq360.ui.fragment.DriverListFragment` (used)
- `au.com.collectiveintelligence.fleetiq360.ui.fragment.EquipmentListFragment` (**not referenced in body**)

**Body summary:** `onCreate` calls `setContentView(R.layout.activity_drivers)` then `showFragmentWithoutStack(...)` with a `DriverListFragment`. `EquipmentListFragment` is imported but never used. No `initKeyboard()` call.

---

### File 2: EquipmentActivity.java
**Path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/EquipmentActivity.java`
**Lines:** 1–23

**Class:** `EquipmentActivity extends FleetActivity`

**Methods:**
| Method | Line |
|---|---|
| `onCreate(Bundle)` | 15 |

**Types / Constants / Interfaces defined:** none

**Imports:**
- `android.content.Intent` (**not referenced in body**)
- `android.os.Bundle` (used)
- `android.support.v4.app.Fragment` (**not referenced in body**)
- `au.com.collectiveintelligence.fleetiq360.R` (used)
- `au.com.collectiveintelligence.fleetiq360.model.TakePhotoPathPrefs` (used)
- `au.com.collectiveintelligence.fleetiq360.ui.common.FleetActivity` (used)
- `au.com.collectiveintelligence.fleetiq360.ui.fragment.EquipmentListFragment` (used)

**Body summary:** `onCreate` calls `setContentView(R.layout.activity_equipment)`, then `showFragmentWithoutStack(...)` with an `EquipmentListFragment`, then `TakePhotoPathPrefs.clearImages()`. No `initKeyboard()` call.

---

### File 3: EquipmentStatsActivity.java
**Path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/EquipmentStatsActivity.java`
**Lines:** 1–18

**Class:** `EquipmentStatsActivity extends FleetActivity`

**Methods:**
| Method | Line |
|---|---|
| `onCreate(Bundle)` | 10 |

**Types / Constants / Interfaces defined:** none

**Imports:**
- `android.os.Bundle` (used)
- `au.com.collectiveintelligence.fleetiq360.R` (used)
- `au.com.collectiveintelligence.fleetiq360.ui.common.FleetActivity` (used)
- `au.com.collectiveintelligence.fleetiq360.ui.fragment.DriverStatsFragment3` (used)

**Body summary:** `onCreate` calls `setContentView(R.layout.activity_common)`, `initKeyboard()`, then `showFragmentWithoutStack(...)` with a `DriverStatsFragment3`.

---

### Supporting context read (not assigned files, consulted for evidence)

**FleetActivity.java** (`ui/common/FleetActivity.java`) — base class for all three activities. Provides `showFragmentWithoutStack(...)`, `initKeyboard()`, and lifecycle management. Confirmed that `initKeyboard()` is a valid inherited method.

**DriverStatsActivity.java** — sibling activity hosting `DriverStatsFragment1`; uses `initKeyboard()` and `activity_common` layout — identical structure to `EquipmentStatsActivity`.

**DriverStatsFragment3.java** — fragment hosted by `EquipmentStatsActivity`. Its class name, field names (`driverStatsResultArray`, `getDriverStats`-style API call internally), and internal comment refer to driver-domain concepts while it is actually used to display equipment stats.

---

## Section 2 & 3: Findings

---

### A54-1 — MEDIUM: Unused import `EquipmentListFragment` in `DriversActivity`

**File:** `DriversActivity.java`, line 8
**Category:** Dead code / build warning

```java
import au.com.collectiveintelligence.fleetiq360.ui.fragment.EquipmentListFragment;
```

`EquipmentListFragment` is imported but never referenced in the class body. The activity instantiates `DriverListFragment` (line 16). This import is a stale leftover, likely from copy-paste from `EquipmentActivity`. It will generate an IDE/compiler unused-import warning and is misleading about the class's dependencies.

---

### A54-2 — MEDIUM: Two unused imports in `EquipmentActivity` (`Intent`, `Fragment`)

**File:** `EquipmentActivity.java`, lines 3–5
**Category:** Dead code / build warning

```java
import android.content.Intent;
import android.support.v4.app.Fragment;
```

Neither `Intent` nor `Fragment` is referenced anywhere in `EquipmentActivity`. These are stale imports, likely left from an earlier version of the class or copied from another activity. Both generate unused-import warnings. The `android.support.v4.app.Fragment` import is particularly notable because the project already has its own base layer (`FleetActivity`) and these imports suggest a prior attempt to handle fragment transactions directly that was never completed or was later removed.

---

### A54-3 — HIGH: `EquipmentStatsActivity` hosts `DriverStatsFragment3` — misleading cross-domain naming

**File:** `EquipmentStatsActivity.java`, line 6 and line 16
**Category:** Leaky abstraction / style inconsistency

```java
import au.com.collectiveintelligence.fleetiq360.ui.fragment.DriverStatsFragment3;
...
showFragmentWithoutStack(R.id.fragment_container, DriverStatsFragment3.class.getSimpleName(), new DriverStatsFragment3());
```

`EquipmentStatsActivity` is the equipment-stats screen yet it delegates to `DriverStatsFragment3`. Inside that fragment the result type is `EquipmentStatsResultArray` and the API call is `getEquipmentStats(...)`, confirming the content is equipment-related. The fragment is simply misnamed. This constitutes a leaky abstraction: the public tag stored in the fragment back-stack (and used by the fragment manager for lookup) is `"DriverStatsFragment3"`, which misleads any code that searches for fragments by tag. The class-level naming inconsistency also makes tracing the equipment stats flow unnecessarily difficult.

A parallel class, `DriverStatsActivity`, correctly hosts `DriverStatsFragment1` for the driver domain. The equipment-stats naming chain should mirror that pattern (e.g., `EquipmentStatsFragment`).

---

### A54-4 — LOW: Inconsistent `initKeyboard()` usage across activity siblings

**File:** `DriversActivity.java` (absent), `EquipmentActivity.java` (absent), `EquipmentStatsActivity.java` (line 14)
**Category:** Style inconsistency

`EquipmentStatsActivity.onCreate` calls `initKeyboard()` at line 14, following the same pattern as `DriverStatsActivity` and other activities. `DriversActivity` and `EquipmentActivity` do not call `initKeyboard()`. While this may be intentional (those screens may not contain text-input fields), the inconsistency is unacknowledged — no comment explains the omission. If the base activity performs important keyboard state management in `initKeyboard()`, omitting it in two of five activity subclasses is a latent defect. At minimum, the inconsistency should be documented.

---

### A54-5 — LOW: `DriverStatsFragment3` internal field `driverStatsResultArray` typed from `EquipmentStatsResultArray` but named with "driver" prefix

**File:** `DriverStatsFragment3.java` (supporting context), referenced via `EquipmentStatsActivity.java`
**Category:** Style inconsistency / leaky abstraction (surfaced through the assignment of `EquipmentStatsActivity`)

```java
// DriverStatsFragment3.java line 40
private EquipmentStatsResultArray driverStatsResultArray;
```

The field `driverStatsResultArray` holds an `EquipmentStatsResultArray`. The name/type mismatch is a code smell that propagates confusion from the misnamed class (A54-3) into its internals. This is noted here because it is directly traceable to the `EquipmentStatsActivity` hosting decision.

---

### A54-6 — INFO: No `@Override` annotation omissions or formatting issues detected

All `onCreate` overrides in the three assigned files carry `@Override`. No trailing whitespace, brace inconsistency, or non-standard indentation was observed in the three assigned files themselves.

---

## Summary Table

| ID | Severity | File | Line(s) | Description |
|---|---|---|---|---|
| A54-1 | MEDIUM | `DriversActivity.java` | 8 | Unused import `EquipmentListFragment` |
| A54-2 | MEDIUM | `EquipmentActivity.java` | 3–5 | Unused imports `Intent`, `Fragment` |
| A54-3 | HIGH | `EquipmentStatsActivity.java` | 6, 16 | Equipment-stats activity hosting a "Driver" fragment — misleading cross-domain naming and leaky back-stack tag |
| A54-4 | LOW | `DriversActivity.java`, `EquipmentActivity.java` | — | Inconsistent `initKeyboard()` call pattern vs. sibling activities |
| A54-5 | LOW | `DriverStatsFragment3.java` (context) | 40 | Field `driverStatsResultArray` typed as `EquipmentStatsResultArray` — name/type mismatch tracing from A54-3 |
| A54-6 | INFO | All three files | — | No `@Override` omissions or formatting issues found |
