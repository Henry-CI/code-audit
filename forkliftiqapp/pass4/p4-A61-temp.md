# Pass 4 — Code Quality Audit
**Audit run:** 2026-02-26-01
**Agent:** A61
**Date executed:** 2026-02-27

---

## Section 1: Reading Evidence

### File 1: DriverStatsFragment3.java
**Full path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/DriverStatsFragment3.java`
**Class:** `DriverStatsFragment3` extends `FleetFragment`

**Fields:**
| Line | Field | Type | Visibility |
|------|-------|------|------------|
| 38 | `mChart` | `LineChart` | private |
| 39 | `info_layout_1` | `LinearLayout` | private |
| 39 | `info_layout_2` | `LinearLayout` | private |
| 40 | `driverStatsResultArray` | `EquipmentStatsResultArray` | private |
| 41 | `arrayList` | `ArrayList<EquipmentStatsItem>` | public |
| 50 | `selectedType` | `int` | private |
| 233 | `mColors` | `int[]` | private static final |

**Methods:**
| Line | Method | Visibility |
|------|--------|------------|
| 44 | `onCreateView(LayoutInflater, ViewGroup, Bundle)` | public (override) |
| 52 | `initViews()` | public |
| 102 | `getUserDetail()` | private |
| 107 | `onWeekView()` | private |
| 112 | `onMonthView()` | private |
| 117 | `onYearView()` | private |
| 122 | `loadData()` | private |
| 145 | `setUserData()` | private |
| 156 | `onData(EquipmentStatsResultArray)` | private |
| 167 | `showInfo()` | private |
| 205 | `showItem(int, EquipmentStatsItem, View)` | private |
| 214 | `initChar()` | private |
| 251 | `clearChartData()` | private |
| 257 | `initChartData(EquipmentStatsResultArray)` | private |
| 292 | `getColumnLabels(EquipmentStatsResultArray)` | private |
| 309 | `getXAixsFormatter(EquipmentStatsResultArray)` | private |

**Inner classes/interfaces:**
| Line | Name | Kind |
|------|------|------|
| 316 | `MyValueFormatter` | public inner class, implements `IValueFormatter` |
| 324 | `MyAxisValueFormatter` | public static inner class, implements `IAxisValueFormatter` |

---

### File 2: DriverStatsListAdapter.java
**Full path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/DriverStatsListAdapter.java`
**Class:** `DriverStatsListAdapter` extends `ArrayAdapter<DriverStatsItem>`

**Fields:**
| Line | Field | Type | Visibility |
|------|-------|------|------------|
| 20 | `context` | `Context` | private |
| 21 | `mData` | `ArrayList<DriverStatsItem>` | private |
| 30 | `JOYFUL_COLORS` | `int[]` | private static final |
| 39 | `colors` | `ArrayList<Integer>` | private |
| 48 | `maxValue` | `float` | private |

**Methods:**
| Line | Method | Visibility |
|------|--------|------------|
| 23 | `DriverStatsListAdapter(Context, ArrayList<DriverStatsItem>)` | package-private (constructor) |
| 41 | `initColors()` | private |
| 50 | `initData()` | private |
| 61 | `getItemRatio(DriverStatsItem)` | private |
| 70 | `getColor(int)` | private |
| 76 | `getView(int, View, ViewGroup)` | public (override) |
| 124 | `getCount()` | public (override) |
| 129 | `getItem(int)` | public (override) |

**Inner classes:**
| Line | Name | Kind |
|------|------|------|
| 133 | `ListHolder` | package-private static class (ViewHolder) |

**ListHolder fields:** `name` (TextView), `status_bar` (View), `status_bar_layout` (View), `stub` (View), `status_text` (TextView)

---

### File 3: EquipmentConnectFragment.java
**Full path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/EquipmentConnectFragment.java`
**Class:** `EquipmentConnectFragment` extends `FleetFragment`

**Fields:**
| Line | Field | Type | Visibility |
|------|-------|------|------------|
| 36 | `loadingIV` | `ImageView` | private |
| 37 | `connecting_text` | `View` | private |
| 38 | `activity` | `Activity` | package-private |
| 40–42 | `loadingResIds` | `int[]` | private |
| 44 | `autoConnect` | `boolean` | public |
| 45 | `myHandler` | `Handler` | private |
| 46 | `operationFinished` | `boolean` | private static |
| 47 | `operationSucceeded` | `boolean` | private static |
| 48 | `permissionNotGranted` | `boolean` | private static |
| 49 | `runTime` | `int` | private static |
| 65 | `updateTimerMethod` | `Runnable` | private |
| 101 | `connect_button` | `View` | private |
| 102 | `abort_button` | `View` | private |
| 206 | `stoppingSession` | `boolean` | private |
| 207 | `REQUEST_ENABLE_BT` | `int` | private |
| 284 | `runnableAfterPermission` | `Runnable` | private |

**Methods:**
| Line | Method | Visibility |
|------|--------|------------|
| 51 | `startAnimationThread()` | private |
| 55 | `stopTimer()` | private |
| 59 | `onDestroy()` | public (override) |
| 83 | `onCreateView(LayoutInflater, ViewGroup, Bundle)` | public (override) |
| 90 | `onActivityCreated(Bundle)` | public (override) |
| 104 | `initViews()` | public |
| 132 | `stopConnection()` | private |
| 138 | `enableButton(boolean)` | private |
| 147 | `setInfo()` | private |
| 157 | `onOperationDone()` | private |
| 169 | `onResume()` | public (override) |
| 179 | `startWorkHandler()` | private |
| 189 | `startConnect()` | private |
| 201 | `showNext()` | private |
| 209 | `onActivityResult(int, int, Intent)` | public (override) |
| 217 | `onConnectSucceed()` | private |
| 223 | `onConnectFailed()` | private |
| 236 | `onAbort()` | private |
| 242 | `connectEquipment(EquipmentItem)` | private |

---

## Section 2 & 3: Findings

---

### A61-1 — HIGH — Duplicate `arrayList.clear()` Call in `onData()`

**File:** `DriverStatsFragment3.java`, lines 158–161

```java
private void onData(EquipmentStatsResultArray resultArray) {
    driverStatsResultArray = resultArray;
    arrayList.clear();                              // line 158 — first clear
    if (driverStatsResultArray != null && driverStatsResultArray.arrayList != null) {
        arrayList.clear();                          // line 160 — redundant second clear
        arrayList.addAll(driverStatsResultArray.arrayList);
    }
    ...
}
```

`arrayList.clear()` is called unconditionally on line 158, then again inside the `if` block on line 160. The second call is dead code — the list is already empty. This is not a correctness bug in the current flow, but it indicates a merge or edit error and creates confusion about the intent. If the outer clear were ever removed or the if-condition were changed, incorrect list state could result.

---

### A61-2 — HIGH — Static Instance State Shared Across Fragment Instances (`EquipmentConnectFragment`)

**File:** `EquipmentConnectFragment.java`, lines 46–49

```java
private static boolean operationFinished = false;
private static boolean operationSucceeded = false;
private static boolean permissionNotGranted = true;
private static int runTime = 0;
```

All four state variables that track the lifecycle of a BLE connection operation are declared `static`. This means they are shared across all instances of `EquipmentConnectFragment` within the process lifetime. If the fragment is destroyed and recreated (back navigation, configuration change, multi-window), the previous operation's final state leaks into the new instance. For example, if `operationSucceeded = true` remains set from a prior session, `onResume()` (line 172) immediately calls `showNext()` on the new instance without ever initiating a connection. This is a genuine logic defect resulting from incorrect use of `static` for per-instance state.

---

### A61-3 — HIGH — `REQUEST_ENABLE_BT` Declared as a Non-Final Instance Variable

**File:** `EquipmentConnectFragment.java`, line 207

```java
private int REQUEST_ENABLE_BT = 100;
```

This field is named using the `ALL_CAPS_SNAKE_CASE` Java constant convention but is declared as a mutable instance variable, not `static final`. The naming implies it is a constant, but any code could accidentally mutate it. It should be `private static final int REQUEST_ENABLE_BT = 100;`. The mismatch between name and declaration type is a style defect that also creates a misleading API surface.

---

### A61-4 — HIGH — Deprecated `getResources().getColor(int)` Without Context (`DriverStatsListAdapter`)

**File:** `DriverStatsListAdapter.java`, lines 42–43

```java
colors.add(getContext().getResources().getColor(R.color.ci_green));
colors.add(getContext().getResources().getColor(R.color.ci_dark_blue));
```

`Resources.getColor(int)` was deprecated in API 23 (Android 6.0 / Marshmallow). The replacement is `ContextCompat.getColor(Context, int)` or `Resources.getColor(int, Theme)`. Since the `minSdkVersion` for this project targets devices that include API 23+, the compiler emits a deprecation warning here and the results may be incorrect on devices where dynamic theming applies to these colors.

---

### A61-5 — MEDIUM — `initData()` Called on Every `getView()` Invocation (Performance Regression)

**File:** `DriverStatsListAdapter.java`, line 78

```java
@Override
public View getView(int position, View convertView, @NonNull ViewGroup parent) {
    initData();   // recalculates maxValue on every list row render
    ...
}
```

`initData()` iterates over the entire `mData` list and recalculates `maxValue` on every single call to `getView()`. In a list with N rows this makes the adapter O(N²) in rendering cost. `initData()` is already called once in the constructor (line 27); the additional call inside `getView()` is wasteful and scales poorly. It should be removed from `getView()` and only re-invoked when the underlying data set changes.

---

### A61-6 — MEDIUM — `Float.valueOf()` Result Checked for `null` on a Primitive Autobox — Always Non-Null (`DriverStatsListAdapter`)

**File:** `DriverStatsListAdapter.java`, lines 54–56 and lines 62–64

```java
// initData():
Float v = Float.valueOf(item.value);
if (v != null) {          // dead branch — Float.valueOf never returns null
    maxValue = ...;
}

// getItemRatio():
Float v = Float.valueOf(item.value);
if (v != null && maxValue > 0.0f) {  // null check is dead
```

`Float.valueOf(String)` either returns a non-null `Float` or throws `NumberFormatException`. It never returns `null`. The null guards on `v` are therefore unreachable dead code. If the intent was to handle parse failures, a `try/catch NumberFormatException` is needed (as is correctly done in `getView()` at line 103–106). The dead null checks silently mask potential `NumberFormatException` crashes in `initData()` and `getItemRatio()` — if `item.value` is not a valid float string, these methods throw an uncaught exception at runtime rather than falling back gracefully.

---

### A61-7 — MEDIUM — `initChar()` Assigns `mChart` via `findViewById()` After It Was Already Assigned in `initViews()`

**File:** `DriverStatsFragment3.java`, lines 58 and 214–215

```java
// initViews(), line 58:
mChart = mRootView.findViewById(R.id.equipment_stats_chart);

// initChar(), line 214–215:
private void initChar() {
    mChart = (LineChart) findViewById(R.id.equipment_stats_chart);
```

`mChart` is assigned in `initViews()` at line 58 via `mRootView.findViewById(...)`, then unconditionally overwritten inside `initChar()` at line 215 using the fragment-level `findViewById(...)`. Both resolve to the same view, making one assignment redundant. The unnecessary redundancy causes confusion about which assignment is the canonical one and also uses the fragment's `findViewById` wrapper differently from the rest of the class (which consistently uses `mRootView.findViewById`).

---

### A61-8 — MEDIUM — Method Name Typo: `initChar()` Should Be `initChart()`

**File:** `DriverStatsFragment3.java`, line 214

```java
private void initChar() {
```

The method initialises the MPAndroidChart `LineChart`. The name `initChar` is a typo for `initChart`. The base class `FleetFragment` already defines a method named `initChart()` (line 106 of `FleetFragment.java`) for a `PieChart`. The typo means there is no name collision, but it is misleading to readers who expect to find chart initialisation under `initChart`. It also makes it harder to search the codebase consistently.

---

### A61-9 — MEDIUM — `getUserDetail()` Calls `UserPhotoFragment.showUserPhoto()` Redundantly; Also Called in `initViews()`

**File:** `DriverStatsFragment3.java`, lines 52–53 and 102–104

```java
// initViews(), line 53:
UserPhotoFragment.showUserPhoto((ImageView) mRootView.findViewById(R.id.user_photo));

// getUserDetail(), lines 102–104:
private void getUserDetail() {
    UserPhotoFragment.showUserPhoto((ImageView) mRootView.findViewById(R.id.user_photo));
    setUserData();
}
```

`showUserPhoto()` is called twice on the same `ImageView` every time `initViews()` runs — once directly at line 53 and once inside `getUserDetail()` at line 103. This is a style inconsistency and redundant work. Either the direct call in `initViews()` or the call inside `getUserDetail()` should be removed.

---

### A61-10 — MEDIUM — `onWeekView()`, `onMonthView()`, `onYearView()` Are Identical — Duplicated Logic

**File:** `DriverStatsFragment3.java`, lines 107–120

```java
private void onWeekView() {
    driverStatsResultArray = null;
    loadData();
}

private void onMonthView() {
    driverStatsResultArray = null;
    loadData();
}

private void onYearView() {
    driverStatsResultArray = null;
    loadData();
}
```

All three methods have identical bodies. They exist solely because the `RadioButton.OnCheckedChangeListener` pattern requires separate callbacks for each button, but the logic could be consolidated into a single `onPeriodChanged()` method that accepts the `selectedType` as a parameter, or the listeners could set `selectedType` and directly call the shared method without three intermediate wrappers. As written, any future change to the common logic must be replicated in all three methods.

---

### A61-11 — MEDIUM — `getXAixsFormatter()` Method Name Contains Typo ("Aixs" Instead of "Axis")

**File:** `DriverStatsFragment3.java`, line 309

```java
private MyAxisValueFormatter getXAixsFormatter(EquipmentStatsResultArray resultArray) {
```

"Aixs" is a transposition of "Axis". This is a naming defect. The same misspelling appears in the call site at line 286:

```java
mChart.getXAxis().setValueFormatter(getXAixsFormatter(equipmentStatsResultArray));
```

---

### A61-12 — MEDIUM — `runnableAfterPermission` Field Declared in Both `EquipmentConnectFragment` and `FleetFragment`; Shadowed Field

**File:** `EquipmentConnectFragment.java`, line 284
**Related:** `FleetFragment.java`, line 263

```java
// EquipmentConnectFragment.java, line 284:
private Runnable runnableAfterPermission;

// FleetFragment.java, line 263:
private Runnable runnableAfterPermission;
```

Both the superclass `FleetFragment` and the subclass `EquipmentConnectFragment` declare a `private Runnable runnableAfterPermission` field. Because both are `private`, the subclass field shadows (hides) the superclass field entirely. `FleetFragment.startConnect()` assigns `FleetFragment.runnableAfterPermission` but `FleetFragment.onRequestPermissionsResult()` reads the same superclass field. `EquipmentConnectFragment.startConnect()` assigns `EquipmentConnectFragment.runnableAfterPermission` and also calls `runnableAfterPermission.run()` immediately afterward — the superclass permission-grant callback (`onRequestPermissionsResult`) would read the superclass copy, not the subclass copy. The design is confusing and the superclass `onRequestPermissionsResult` at line 270 of `FleetFragment` would execute the wrong (or stale) runnable if a permission grant arrived while the `EquipmentConnectFragment` was active.

---

### A61-13 — MEDIUM — `connectEquipment()` Directly Mutates `BleController.ble_status` Public Field (Leaky Abstraction)

**File:** `EquipmentConnectFragment.java`, line 243

```java
private void connectEquipment(EquipmentItem equipmentItem) {
    BleController.instance().ble_status = STATUS_IDLE;
    BleController.instance().startConnect(...);
```

The fragment reaches into `BleController`'s internal state field `ble_status` and writes to it directly before calling `startConnect()`. This bypasses any encapsulation that `BleController` has over its own state machine. If `BleController` ever adds logic to `startConnect()` that depends on the prior value of `ble_status`, this external reset will break that logic silently. The correct pattern is for `BleController.startConnect()` to reset its own internal status as part of its startup sequence.

---

### A61-14 — LOW — `activity` Field in `EquipmentConnectFragment` is Package-Private (Accidental Visibility)

**File:** `EquipmentConnectFragment.java`, line 38

```java
Activity activity;
```

This field lacks an access modifier and is therefore package-private. All other instance fields in this class are `private`. The broader visibility appears unintentional — nothing outside the class or package needs direct access to the `Activity` reference, and exposing it invites external mutation.

---

### A61-15 — LOW — `autoConnect` Public Field in `EquipmentConnectFragment` Should Be a Constructor Parameter or Bundle Argument

**File:** `EquipmentConnectFragment.java`, line 44

```java
public boolean autoConnect = false;
```

The `autoConnect` flag controls whether the fragment immediately initiates a connection on creation. It is exposed as a `public` mutable field rather than being passed through a `Bundle` (the standard Android pattern for fragment arguments) or set via a factory method. If the fragment is recreated by the system after a process death, `autoConnect` will revert to `false` regardless of what the caller originally set, silently altering behaviour.

---

### A61-16 — LOW — `status_bar_layout` ViewHolder Field Is Populated but Never Used

**File:** `DriverStatsListAdapter.java`, lines 89 and 136

```java
// getView(), line 89:
holder.status_bar_layout = row.findViewById(R.id.status_bar_layout);

// ListHolder, line 136:
View status_bar_layout;
```

`status_bar_layout` is found and stored in the `ListHolder` during view creation but is never read elsewhere in the adapter. It is dead code that adds unnecessary memory retention per list row.

---

### A61-17 — LOW — Commented-Out Code in `FleetFragment.onRequestPermissionsResult()` (Observed via Superclass Read)

**File:** `FleetFragment.java` (superclass of all three audited fragments), lines 274–275

```java
} else {
    //permissionNotGranted = true;
    //onLocationNotGranted();
}
```

Two lines of commented-out code remain in the `else` branch when location permission is denied. This leaves the denial case completely unhandled — no flag is set, no user feedback is provided. The comments suggest the handling was deliberately removed but never replaced, which is a logic gap observable by callers of all `FleetFragment` subclasses including the audited files.

---

### A61-18 — LOW — Duplicate Color Value in `mColors` Array

**File:** `DriverStatsFragment3.java`, lines 237 and 242

```java
private static final int[] mColors = {
    Color.rgb(53, 194, 209),
    Color.rgb(217, 80, 138),
    Color.rgb(255, 102, 0),    // index 2
    ...
    Color.rgb(255, 102, 0),    // index 7 — identical to index 2
    ...
};
```

`Color.rgb(255, 102, 0)` appears at index 2 (line 237) and again at index 7 (line 242). When there are more than 2 equipment items being charted, the third and eighth items will share the same line colour, making them visually indistinguishable on the chart. This is likely an accidental copy-paste error.

---

### A61-19 — LOW — Inner Classes `MyValueFormatter` and `MyAxisValueFormatter` Are Public but Have No Documented Purpose

**File:** `DriverStatsFragment3.java`, lines 316 and 324

```java
public class MyValueFormatter implements IValueFormatter { ... }
public static class MyAxisValueFormatter implements IAxisValueFormatter { ... }
```

Both inner classes are `public`. `MyValueFormatter` is non-static and holds an implicit reference to the enclosing `DriverStatsFragment3` instance; this prevents the fragment from being garbage-collected as long as the chart holds a reference to the formatter. It should be `static` (it uses no enclosing instance state). `MyAxisValueFormatter` is correctly `static`. The `public` visibility on both is broader than necessary — neither needs to be accessible outside the fragment.

---

### A61-20 — INFO — `IValueFormatter` and `IAxisValueFormatter` Are Deprecated MPAndroidChart Interfaces

**File:** `DriverStatsFragment3.java`, lines 31 and 30

```java
import com.github.mikephil.charting.formatter.IAxisValueFormatter;
import com.github.mikephil.charting.formatter.IValueFormatter;
```

Both `IValueFormatter` and `IAxisValueFormatter` were deprecated in MPAndroidChart 3.1.0 in favour of `ValueFormatter` (a concrete class with overridable methods). While not a build-breaking issue at the version currently in use, migration to the successor API is recommended to avoid future compatibility problems when the library is upgraded.

---

## Summary Table

| ID | Severity | File | Summary |
|----|----------|------|---------|
| A61-1 | HIGH | DriverStatsFragment3.java | Duplicate `arrayList.clear()` — dead second clear in `onData()` |
| A61-2 | HIGH | EquipmentConnectFragment.java | Static BLE state fields shared across fragment instances — state leaks between sessions |
| A61-3 | HIGH | EquipmentConnectFragment.java | `REQUEST_ENABLE_BT` named as constant but declared as mutable instance variable |
| A61-4 | HIGH | DriverStatsListAdapter.java | Deprecated `Resources.getColor(int)` without theme context |
| A61-5 | MEDIUM | DriverStatsListAdapter.java | `initData()` called on every `getView()` — O(N²) list rendering cost |
| A61-6 | MEDIUM | DriverStatsListAdapter.java | `Float.valueOf()` null checks are dead code; parse errors silently throw instead of being caught |
| A61-7 | MEDIUM | DriverStatsFragment3.java | `mChart` assigned twice — in `initViews()` and again inside `initChar()` |
| A61-8 | MEDIUM | DriverStatsFragment3.java | Method typo: `initChar()` should be `initChart()` |
| A61-9 | MEDIUM | DriverStatsFragment3.java | `showUserPhoto()` called twice per `initViews()` invocation — redundant call |
| A61-10 | MEDIUM | DriverStatsFragment3.java | Three identical one-liner methods `onWeekView/Month/YearView()` — duplicated logic |
| A61-11 | MEDIUM | DriverStatsFragment3.java | Method name typo: `getXAixsFormatter()` should be `getXAxisFormatter()` |
| A61-12 | MEDIUM | EquipmentConnectFragment.java | `runnableAfterPermission` shadows superclass private field — wrong runnable executed on permission grant |
| A61-13 | MEDIUM | EquipmentConnectFragment.java | Fragment directly writes to `BleController.ble_status` — leaky abstraction |
| A61-14 | LOW | EquipmentConnectFragment.java | `activity` field is accidentally package-private |
| A61-15 | LOW | EquipmentConnectFragment.java | `autoConnect` is a public mutable field; should be a Bundle argument |
| A61-16 | LOW | DriverStatsListAdapter.java | `status_bar_layout` in `ListHolder` is populated but never read — dead field |
| A61-17 | LOW | FleetFragment.java (superclass) | Commented-out permission-denial handling — denial case is silently ignored |
| A61-18 | LOW | DriverStatsFragment3.java | Duplicate colour value in `mColors[]` at indices 2 and 7 |
| A61-19 | LOW | DriverStatsFragment3.java | `MyValueFormatter` inner class is non-static; holds implicit fragment reference; both formatter classes are unnecessarily public |
| A61-20 | INFO | DriverStatsFragment3.java | `IValueFormatter` and `IAxisValueFormatter` are deprecated MPAndroidChart interfaces |

---

*End of report — Agent A61, Pass 4 (Code Quality)*
