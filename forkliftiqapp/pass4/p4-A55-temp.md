# Pass 4 Code Quality Audit — Agent A55
**Audit Run:** 2026-02-26-01
**Auditor:** A55
**Date:** 2026-02-27
**Files Assigned:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/IncidentActivity.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/JobsActivity.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/LoginActivity.java`

---

## Step 1: Reading Evidence

### File 1: IncidentActivity.java
**Full path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/IncidentActivity.java`
**Class:** `IncidentActivity extends FleetActivity`
**Total lines:** 43

**Fields (all public):**
| Line | Modifier | Type | Name | Initial Value |
|------|----------|------|------|---------------|
| 12 | `public` | `ImpactParameter` | `impactParameter` | (set in onCreate) |
| 13 | `public` | `SaveImpactResult` | `impactResult` | (implicit null) |
| 14 | `public` | `String` | `signaturePath` | `null` |
| 15 | `public` | `String` | `mCurrentPhotoPath` | (implicit null) |
| 16 | `public` | `String[]` | `injuryTypes` | (set in onCreate) |

**Methods:**
| Line | Modifier | Return | Name | Notes |
|------|----------|--------|------|-------|
| 19 | `@Override protected` | `void` | `onCreate(Bundle)` | Initialises fields, shows IncidentFragment |
| 36 | `@Override public` | `void` | `onBackPressed()` | Finishes if impactResult != null, else super |

**Types / constants / enums defined:** None beyond the class itself.

**Observations noted during read:**
- `impactParameter.injury = false` is set twice (lines 27 and 30); a duplicate assignment between lines 25–31.
- All five Activity-level fields are `public`, making them directly readable and writable by the hosted fragments (`IncidentFragment`, `IncidentPart2Fragment`).
- No logging, no `@SuppressWarnings`, no TODOs.

---

### File 2: JobsActivity.java
**Full path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/JobsActivity.java`
**Class:** `JobsActivity extends FleetActivity`
**Total lines:** 15

**Fields:** None.

**Methods:**
| Line | Modifier | Return | Name | Notes |
|------|----------|--------|------|-------|
| 10 | `@Override protected` | `void` | `onCreate(Bundle)` | Sets content view, shows JobsFragment |

**Types / constants / enums defined:** None.

**Observations noted during read:**
- Minimal; no issues with this file in isolation.

---

### File 3: LoginActivity.java
**Full path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/LoginActivity.java`
**Class:** `LoginActivity extends FleetActivity`
**Total lines:** 28

**Fields:** None.

**Methods:**
| Line | Modifier | Return | Name | Notes |
|------|----------|--------|------|-------|
| 14 | `@Override protected` | `void` | `onCreate(Bundle)` | Auto-redirects if user session exists; else shows LoginFragment |

**Types / constants / enums defined:** None.

**Observations noted during read:**
- `Intent.makeMainActivity(ComponentName)` is used to build the redirect intent. This is the correct API for navigating to a root task.
- The ternary `user.hasAssociatedDrivers() ? DriversActivity.class : DashboardActivity.class` is concise and readable.
- No logging, no `@SuppressWarnings`, no TODOs.

---

### Supporting files read (for context)
- `FleetActivity.java` — base class; 461 lines; contains `showDeviceDisconnectedDialog()` (dead code, call commented out at line 183), multiple commented-out `//hideProgress()` and `//showProgress()` calls, and `ProgressDialog` (deprecated API).
- `ImpactParameter.java` — plain data class; all fields `public`.
- `SaveImpactResult.java` — plain data class; all fields `public`.
- `IncidentFragment.java` — directly reads/writes `incidentActivity.impactParameter.*` (lines 145, 163–165, 198–200, 271–275).
- `IncidentPart2Fragment.java` — directly reads/writes `incidentActivity.impactParameter.*`, `incidentActivity.impactResult`, `incidentActivity.signaturePath`, `incidentActivity.mCurrentPhotoPath`, `incidentActivity.injuryTypes` (throughout file).

---

## Step 2 & 3: Findings

---

### A55-1 — MEDIUM: Duplicate field initialisation — `impactParameter.injury` set to `false` twice in `onCreate`

**File:** `IncidentActivity.java`
**Lines:** 27 and 30

```java
impactParameter.injury = false;   // line 27
impactParameter.injury_type = injuryTypes[0];  // line 29
impactParameter.injury = false;   // line 30  <-- duplicate
```

`impactParameter.injury` is assigned `false` on both line 27 and line 30. The second assignment is redundant. This is most likely a copy-paste artefact from an earlier refactor where `injury` and some other field were both being reset. While harmless at runtime (the value cannot differ between the two lines because no other code runs between them), it is misleading and implies an edit that was partially completed, or a second intention that was never filled in.

**Impact:** Confusion for future maintainers; no runtime effect.
**Recommendation:** Remove the duplicate assignment on line 30.

---

### A55-2 — HIGH: Leaky abstraction — Activity uses five `public` fields as shared mutable state for cross-fragment communication

**File:** `IncidentActivity.java`
**Lines:** 12–16

```java
public ImpactParameter impactParameter;
public SaveImpactResult impactResult;
public String signaturePath = null;
public String mCurrentPhotoPath;
public String[] injuryTypes;
```

All five fields are declared `public` and are directly read and mutated by both `IncidentFragment` and `IncidentPart2Fragment` via the pattern:

```java
incidentActivity = (IncidentActivity) getActivity();
// then e.g.:
incidentActivity.impactParameter.unit_id = equipmentItem.id;
incidentActivity.signaturePath = filePath;
incidentActivity.mCurrentPhotoPath = items.get(0).path;
incidentActivity.impactResult = result;
incidentActivity.injuryTypes   // read directly
```

This turns the Activity into a passive data bag with no encapsulation. Any fragment, or future code, can modify these fields in any order without the Activity being notified. The pattern bypasses Android's conventional inter-component communication mechanisms (ViewModel/LiveData, Bundle arguments, callbacks, or even a simple getter/setter pair).

**Impact:** Tight coupling between three classes; difficult to test fragments in isolation; mutations to shared state are invisible to the Activity; risk of stale/inconsistent state if navigation order changes.
**Recommendation:** Introduce a shared `ViewModel` (preferred) or at minimum expose controlled setter/getter methods and make the fields `private`. The multi-fragment wizard pattern (`IncidentFragment` → `IncidentPart2Fragment`) is a textbook use case for a shared `ViewModel` scoped to the Activity.

---

### A55-3 — LOW: Naming inconsistency — `mCurrentPhotoPath` uses Hungarian `m` prefix while `signaturePath`, `injuryTypes`, `impactParameter`, and `impactResult` do not

**File:** `IncidentActivity.java`
**Line:** 15

```java
public String mCurrentPhotoPath;   // Hungarian prefix
public String signaturePath;       // no prefix
public ImpactParameter impactParameter;  // no prefix
public SaveImpactResult impactResult;    // no prefix
public String[] injuryTypes;       // no prefix
```

The `m` prefix convention (Android legacy member-variable style) is applied to `mCurrentPhotoPath` but to none of the other four fields in the same class. The Android style guide deprecated the `m` prefix convention in favour of plain camelCase. Mixing both styles in the same class makes intent unclear.

**Impact:** Minor readability inconsistency; no runtime effect.
**Recommendation:** Rename `mCurrentPhotoPath` to `currentPhotoPath` (or apply the chosen convention consistently across all fields).

---

### A55-4 — LOW: `onBackPressed()` logic in `IncidentActivity` silently swallows back navigation when `impactResult` is null — no comment explains the intent

**File:** `IncidentActivity.java`
**Lines:** 36–42

```java
@Override
public void onBackPressed() {
    if (impactResult != null) {
        finish();
    } else {
        super.onBackPressed();
    }
}
```

When `impactResult` is `null` (i.e., the save has not yet completed), `super.onBackPressed()` is called, which pops the back stack through fragments. When `impactResult` is non-null, `finish()` is called, which closes the whole Activity. This asymmetric behaviour — where the button does different things depending on hidden state — is not documented with any comment. A maintainer reading this in isolation cannot tell why `finish()` is preferred over `super.onBackPressed()` once the result exists, or why the two paths differ.

**Impact:** Maintainability risk; the behaviour is correct but opaque.
**Recommendation:** Add an inline comment explaining that once the impact has been saved (`impactResult != null`) the entire wizard should close rather than stepping back through already-saved screens.

---

### A55-5 — INFO: `JobsActivity` is a near-empty pass-through — consider whether it needs to be an Activity at all

**File:** `JobsActivity.java`
**Lines:** 1–15

`JobsActivity` contains only `onCreate`, sets a layout, and immediately delegates all behaviour to `JobsFragment`. No fields, no lifecycle overrides, no navigation logic. While this is structurally consistent with the other thin activities in the project, it is worth noting that the Activity adds a navigation entry point with zero logic. If `JobsFragment` is always shown stand-alone, the Activity could be merged into a navigation graph entry (Jetpack Navigation) or the fragment could be hosted in a shared container activity. This is an architectural observation, not a defect.

**Impact:** Informational only; no runtime or quality defect.

---

### A55-6 — INFO: `LoginActivity.onCreate` performs navigation in `onCreate` without checking `savedInstanceState` — may cause double-navigation on recreation

**File:** `LoginActivity.java`
**Lines:** 14–27

```java
@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_login);

    User user = CurrentUser.get();
    if (user != null) {
        Intent intent = Intent.makeMainActivity(...);
        startActivity(intent);
        finish();
    } else {
        showFragmentWithoutStack(...);
    }
}
```

The auto-login redirect (`startActivity` + `finish()`) runs unconditionally every time `onCreate` is called, including after configuration changes if for some reason the Activity is not immediately finished (e.g., a race between `finish()` and the system recreating the Activity). The `finish()` call is present and will typically prevent recreation, but the lack of a `savedInstanceState == null` guard is inconsistent with the pattern used in other parts of the codebase (where fragment transactions are guarded by `if (savedInstanceState == null)`).

**Impact:** Low practical risk since `finish()` is called before the system can recreate the Activity; informational flag for code-review consistency.
**Recommendation:** Guard the navigation and fragment transaction with `if (savedInstanceState == null)` for defensive correctness and consistency with project conventions.

---

## Summary Table

| ID | Severity | File | Line(s) | Category | Short Description |
|----|----------|------|---------|----------|-------------------|
| A55-1 | MEDIUM | IncidentActivity.java | 27, 30 | Dead code / style | `impactParameter.injury = false` assigned twice |
| A55-2 | HIGH | IncidentActivity.java | 12–16 | Leaky abstraction | Five `public` fields used as shared mutable state across fragments |
| A55-3 | LOW | IncidentActivity.java | 15 | Style inconsistency | `mCurrentPhotoPath` uses Hungarian prefix; other fields do not |
| A55-4 | LOW | IncidentActivity.java | 36–42 | Dead code / style | `onBackPressed` asymmetric logic has no explanatory comment |
| A55-5 | INFO | JobsActivity.java | 1–15 | Architecture | Activity is an empty pass-through; informational only |
| A55-6 | INFO | LoginActivity.java | 14–27 | Style inconsistency | Navigation in `onCreate` lacks `savedInstanceState == null` guard |
