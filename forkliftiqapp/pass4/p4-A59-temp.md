# Pass 4 Code Quality — Agent A59
**Audit run:** 2026-02-26-01
**Agent:** A59
**Date:** 2026-02-27

---

## Section 1: Reading Evidence

### File 1 — FleetFragment.java
**Path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/common/FleetFragment.java`
**Class:** `FleetFragment extends BaseFragment` (public)

**Methods (by line):**

| Line | Method |
|------|--------|
| 39   | `protected void showPreStartOrJobFragment()` |
| 65   | `public static void checkUsePreviousPreStart(BaseActivity activity, final SessionResult sessionResult, final Runnable runnableToJob, final Runnable runnableToPreStart)` |
| 106  | `protected void initChart()` |
| 127  | `protected void initChartExtra(PieChart mChart)` |
| 137  | `public void initBottomBar(int[] imageArray, String[] textArray, View rootView)` |
| 177  | `public void onLeftButton(View view)` |
| 181  | `public void onMiddleButton(View view)` |
| 184  | `public void onRightButton(View view)` |
| 187  | `public void showLoadingLayout()` |
| 194  | `public void hideLoadingLayout()` |
| 202  | `public void onActivityCreated(Bundle savedInstanceState)` (override) |
| 213  | `private void startConnect()` |
| 251  | `private void checkLocationPermission(Runnable runnable)` |
| 265  | `public void onRequestPermissionsResult(int requestCode, @NonNull String permissions[], @NonNull int[] grantResults)` (override) |
| 282  | `public void initViews()` |
| 285  | `public void onSessionEnded()` |

**Fields:**
- `private Runnable runnableAfterPermission` (line 263)

**Imports of note:**
- `android.os.Handler` (line 9) — imported, never used in the file body
- `com.yy.libcommon.ErrorDialog` (line 29) — imported, never used in the file body

---

### File 2 — AddEquipmentFragment.java
**Path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/AddEquipmentFragment.java`
**Class:** `AddEquipmentFragment extends FleetFragment` (public)

**Methods (by line):**

| Line | Method |
|------|--------|
| 50   | `public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)` (override) |
| 67   | `public void initViews()` (override) |
| 110  | `private void updateMacAddressVisible()` |
| 114  | `private void registerAfterMacTextChangedCallback(final EditText mMacEdit)` |
| 119  | (anonymous TextWatcher) `afterTextChanged(Editable arg0)` |
| 123  | (anonymous TextWatcher) `beforeTextChanged(CharSequence arg0, int arg1, int arg2, int arg3)` |
| 127  | (anonymous TextWatcher) `onTextChanged(CharSequence s, int start, int before, int count)` |
| 139  | (inner) `private String clearNonMacCharacters(String mac)` |
| 143  | (inner) `private String formatMacAddress(String cleanMac)` |
| 163  | (inner) `private String handleColonDeletion(String enteredMac, String formattedMac, int selectionStart)` |
| 177  | (inner) `private int colonCount(String formattedMac)` |
| 181  | (inner) `private void setMacEdit(String cleanMac, String formattedMac, int selectionStart, int lengthDiff)` |
| 196  | `private void showManu()` |
| 231  | `private void showType()` |
| 270  | `private String getKeyForFuelType(int mid, int tid)` |
| 274  | `private void showFuelType()` |
| 317  | `private void loadManu(final Runnable runnable)` |
| 337  | `private void loadType(final Runnable runnable)` |
| 362  | `private void loadFuelType(final Runnable runnable)` |
| 388  | `public void onMiddleButton(View view)` (override) |
| 420  | `public void onRightButton(View view)` (override) |
| 424  | `private void saveEquipment()` |

**Fields:**
- `private ManufactureResultArray manufactureResultArray` (line 39)
- `@SuppressLint("UseSparseArrays") private HashMap<Integer, EquipmentTypeResultArray> mapEquipmentTypesForManu` (line 42)
- `private HashMap<String, FuelTypeResultArray> mapFuelTypesForEquipmentType` (line 43)
- `private final String TYPE_TITLE = "--Type--"` (line 45) — instance field, not static
- `private final String FUEL_TITLE = "--Power--"` (line 46) — instance field, not static
- `private EditText equipment_name` (line 55)
- `private EditText equipment_no` (line 56)
- `private EditText equipment_mac_address` (line 57)
- `private TextView equipment_manufacture` (line 58)
- `private TextView equipment_type` (line 59)
- `private TextView equipment_fuel_type` (line 60)
- `private CheckBox expansion_module_checkbox` (line 61)
- `private ManufactureItem manufactureItem` (line 63)
- `private EquipmentTypeItem equipmentTypeItem` (line 64)
- `private FuelTypeItem fuelTypeItem` (line 65)

**Static imports:**
- `static au.com.collectiveintelligence.fleetiq360.ui.fragment.EquipmentListFragment.equipmentChanged` (line 36)

**Annotations:**
- `@SuppressLint("UseSparseArrays")` at line 41

---

### File 3 — DashboardFragment.java
**Path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/DashboardFragment.java`
**Class:** `DashboardFragment extends FleetFragment implements View.OnClickListener` (public)

**Methods (by line):**

| Line | Method |
|------|--------|
| 39   | `public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState)` (override) |
| 44   | `private void setUserPhoto()` |
| 54   | `private void showUserName()` |
| 58   | `public void initViews()` (override) |
| 89   | `private void initMonitorSession()` |
| 98   | `private void updateRunning()` |
| 104  | `public void onSessionEnded()` (override) |
| 108  | `private void getUserDetail()` |
| 114  | `public void onResume()` (override) |
| 123  | `public void onStop()` (override) |
| 128  | `public void onDestroy()` (override) |
| 133  | `public void onClick(View view)` (override) |
| 154  | `private void showEquipmentList()` |
| 168  | `private void showProfile()` |
| 175  | `public void onLeftButton(View view)` (override) |
| 182  | `public void onMiddleButton(View view)` (override) |
| 189  | `public void onRightButton(View view)` (override) |

**Fields:**
- `static Bitmap userPhotoBitmap` (line 35) — package-private static, not private

**Types/Interfaces defined:** None beyond the class itself.

---

## Section 2 & 3: Findings

---

### A59-1 — HIGH — Wrong map queried in `loadType` cache guard (AddEquipmentFragment.java:340)

**File:** `AddEquipmentFragment.java`, line 340

**Evidence:**
```java
// Field declarations:
private HashMap<Integer, EquipmentTypeResultArray> mapEquipmentTypesForManu = new HashMap<>();   // line 42
private HashMap<String, FuelTypeResultArray>        mapFuelTypesForEquipmentType = new HashMap<>(); // line 43

// loadType method:
private void loadType(final Runnable runnable) {
    if (manufactureItem == null)
        return;
    if (mapFuelTypesForEquipmentType.get(Integer.toString(manufactureItem.id)) != null)   // line 340
        return;
    // ...
    mapEquipmentTypesForManu.put(manufactureItem.id, result);   // line 348
}
```

**Problem:** The early-return guard on line 340 queries `mapFuelTypesForEquipmentType` (the fuel-type cache, whose key is a formatted String like `"3_7"`) using `Integer.toString(manufactureItem.id)` (e.g. `"3"`). This key will never match an entry in the fuel-type map, so the guard is always false and the method always sends a network request, even when the equipment-type data is already cached in `mapEquipmentTypesForManu`. The correct check should be:
```java
if (mapEquipmentTypesForManu.get(manufactureItem.id) != null)
    return;
```
The defect causes redundant network calls every time the user opens the type picker after the first load.

---

### A59-2 — HIGH — Missing `break` in switch case for `dashboard_incident_report` (DashboardFragment.java:147–150)

**File:** `DashboardFragment.java`, lines 147–150

**Evidence:**
```java
case R.id.dashboard_incident_report:
    startActivity(new Intent(getContext(), IncidentActivity.class));
default:
    break;
```

**Problem:** There is no `break` after `startActivity(...)` for the `dashboard_incident_report` case. Control falls through to `default`. Although `default` is only a `break` here and produces no additional side effect at present, this is a latent defect: if any logic is ever added to `default`, tapping the incident report button will also execute it. The pattern is inconsistent with every other case in the same switch. The `break` is missing; it should appear before `default`.

---

### A59-3 — MEDIUM — Duplicate `setExtraOffsets` call in `initChart` (FleetFragment.java:110,112)

**File:** `FleetFragment.java`, lines 110 and 112

**Evidence:**
```java
mChart.setExtraOffsets(5, 10, 5, 5);      // line 110 — immediately overwritten
mChart.setExtraOffsets(20.f, 0.f, 20.f, 0.f); // line 112 — effective value
```

**Problem:** `setExtraOffsets` is called twice in immediate succession. The first call (line 110) is completely overwritten by line 112 and has no effect. This indicates either dead configuration (the (5, 10, 5, 5) values were intentional and were accidentally replaced) or a copy-paste leftover. Either way one of the two lines is dead code.

---

### A59-4 — MEDIUM — `System.out.println` used for logging (FleetFragment.java:269)

**File:** `FleetFragment.java`, line 269

**Evidence:**
```java
System.out.println("fine location permission granted");
```

**Problem:** `System.out.println` is not an appropriate logging mechanism for Android production code. It does not go through `android.util.Log` or any app-level logging abstraction, has no tag for filtering, and is not suppressible at release time. It will still emit to logcat in production builds. The project does not appear to use `System.out.println` anywhere else for logging, making this an isolated style inconsistency. It should be replaced with `Log.d(TAG, ...)` or removed.

---

### A59-5 — MEDIUM — Commented-out code left in `onRequestPermissionsResult` (FleetFragment.java:273–275)

**File:** `FleetFragment.java`, lines 273–275

**Evidence:**
```java
} else {
    //permissionNotGranted = true;
    //onLocationNotGranted();
}
```

**Problem:** Two commented-out statements remain in the permission-denied branch. The referenced variable `permissionNotGranted` and method `onLocationNotGranted()` do not exist in the class, suggesting this code was removed but the comments were not cleaned up. The permission-denied branch is effectively empty, meaning the app silently ignores a location permission denial with no user feedback. The commented lines should be deleted; if the intent was to notify the user, the functionality needs to be restored.

---

### A59-6 — MEDIUM — Realm `RealmChangeListener` registered with no corresponding deregistration (DashboardFragment.java:89–96)

**File:** `DashboardFragment.java`, lines 89–96

**Evidence:**
```java
private void initMonitorSession() {
    SessionDb.addRunningChangeListener(new RealmChangeListener<RealmResults<SessionDb>>() {
        @Override
        public void onChange(@NonNull RealmResults<SessionDb> element) {
            updateRunning();
        }
    });
}
```

**Problem:** The anonymous `RealmChangeListener` is registered in `initMonitorSession()` (called from `initViews()`, called from the inherited `onActivityCreated`). There is no corresponding removal of this listener in `onStop()`, `onDestroy()`, or `onDestroyView()`. The `onStop()` and `onDestroy()` overrides at lines 123–130 call only `super` and add no cleanup. If the fragment is detached or the activity finishes while the Realm listener is still active, this produces a Realm leak and can trigger callbacks on a detached fragment, potentially causing `NullPointerException` on `mRootView` access inside `updateRunning()`.

---

### A59-7 — MEDIUM — `static Bitmap userPhotoBitmap` is package-private and leaks Bitmap across fragment instances (DashboardFragment.java:35)

**File:** `DashboardFragment.java`, line 35

**Evidence:**
```java
static Bitmap userPhotoBitmap;
```

**Problem:** This field is `static` and has default (package-private) access. It holds a `Bitmap`, which is one of the largest heap objects in Android. Using a `static` reference for a `Bitmap` prevents garbage collection for the lifetime of the class loader. Although `setUserPhoto()` nulls it out after use (line 49), the bitmap will persist if `setUserPhoto()` is never called (e.g., `mRootView` is null, causing an early return at line 46). Additionally, being package-private makes it accessible from `AddEquipmentFragment` and other classes in the same package, violating encapsulation. It should be `private static` and ideally use a `WeakReference`.

---

### A59-8 — MEDIUM — `getUserDetail()` partially duplicates `initViews()` photo/name logic (DashboardFragment.java:108–111)

**File:** `DashboardFragment.java`, lines 44–56 vs 108–111

**Evidence:**
```java
// initViews() calls (lines 61, 73):
setUserPhoto();
showUserName();

// getUserDetail() body (lines 108–111):
private void getUserDetail() {
    showUserName();
    UserPhotoFragment.showUserPhoto((ImageView) mRootView.findViewById(R.id.user_photo));
}
```

**Problem:** `getUserDetail()` duplicates the photo-loading logic already present in `setUserPhoto()`, but calls `UserPhotoFragment.showUserPhoto()` directly rather than going through `setUserPhoto()`. This means the static bitmap hand-off (`userPhotoBitmap`) is skipped on resume. `setUserPhoto()` first applies any pending `userPhotoBitmap` before delegating to `UserPhotoFragment.showUserPhoto()`. `getUserDetail()` bypasses the first step entirely, so a bitmap set between pause and resume would not be applied. The two methods should be unified.

---

### A59-9 — LOW — `onStop()` and `onDestroy()` are empty overrides (DashboardFragment.java:123–130)

**File:** `DashboardFragment.java`, lines 123–130

**Evidence:**
```java
@Override
public void onStop() {
    super.onStop();
}

@Override
public void onDestroy() {
    super.onDestroy();
}
```

**Problem:** Both overrides contain only a `super` call and no additional logic. They serve no purpose and add noise. If they were stubs intended for cleanup (e.g., deregistering the Realm listener noted in A59-6), they should contain that cleanup. Otherwise they should be removed.

---

### A59-10 — LOW — Non-standard boolean comparison style (`false == expr`) (FleetFragment.java:207)

**File:** `FleetFragment.java`, line 207

**Evidence:**
```java
if(false == MyCommonValue.isCheckLocationPermissionDone) {
```

**Problem:** Yoda-style comparison (`false == expr` instead of `!expr`) is inconsistent with standard Java and Android idiom used everywhere else in the codebase. The rest of the codebase uses conventional `!variable` form. This should be `if (!MyCommonValue.isCheckLocationPermissionDone)`.

---

### A59-11 — LOW — `Handler` and `ErrorDialog` unused imports (FleetFragment.java:9, 29)

**File:** `FleetFragment.java`, lines 9 and 29

**Evidence:**
```java
import android.os.Handler;           // line 9
import com.yy.libcommon.ErrorDialog; // line 29
```

**Problem:** Neither `Handler` nor `ErrorDialog` is referenced anywhere in the body of `FleetFragment.java`. These are unused imports that will produce compiler/IDE warnings and add unnecessary coupling to unrelated classes.

---

### A59-12 — LOW — `TYPE_TITLE` and `FUEL_TITLE` declared as instance fields instead of constants (AddEquipmentFragment.java:45–46)

**File:** `AddEquipmentFragment.java`, lines 45–46

**Evidence:**
```java
private final String TYPE_TITLE = "--Type--";
private final String FUEL_TITLE = "--Power--";
```

**Problem:** These fields are `private final` with compile-time constant values, named in `UPPER_SNAKE_CASE` (which by convention signals a `static final` constant), but are not declared `static`. A new copy is allocated with each fragment instance. They should be `private static final String`.

---

### A59-13 — LOW — Inconsistent `Intent` variable naming in `DashboardFragment` (DashboardFragment.java:169)

**File:** `DashboardFragment.java`, line 169

**Evidence:**
```java
// showProfile():
Intent intent0 = new Intent();
intent0.setClass(Objects.requireNonNull(getContext()), ProfileActivity.class);

// showEquipmentList():
Intent intent = new Intent();
intent.setClass(Objects.requireNonNull(getContext()), SessionActivity.class);

// onLeftButton():
Intent intent = new Intent(getContext(), ActionClearActivity.class);
```

**Problem:** Local `Intent` variables are named `intent0` in `showProfile()` but `intent` in all other methods. The `0` suffix is meaningless (only one Intent is created in that method) and is inconsistent with the rest of the file.

---

### A59-14 — LOW — Misspelled variable name `grouppedCharacters` (AddEquipmentFragment.java:144)

**File:** `AddEquipmentFragment.java`, line 144

**Evidence:**
```java
int grouppedCharacters = 0;
```

**Problem:** The variable name is misspelled: `grouppedCharacters` should be `groupedCharacters` (single `p`). Used consistently within the same anonymous class so it does not cause a runtime defect, but it degrades readability and would fail any spell-check or code review style gate.

---

### A59-15 — LOW — User-facing string "Select Manufacture" uses incorrect English (AddEquipmentFragment.java:209)

**File:** `AddEquipmentFragment.java`, lines 209, 233, 276, 402

**Evidence:**
```java
ThemedSingleListDialog.newInstance(list, selectedStr, "Select Manufacture", ...);
showToast("Select manufacture first");
showToast("Select manufacture first");
showToast("Please select equipment manufacture.");
```

**Problem:** The correct term is "manufacturer" (a noun referring to the company), not "manufacture" (a verb). This user-visible text appears four times with the same error. It does not affect functionality but represents a quality defect in the product UI.

---

### A59-16 — LOW — `@SuppressLint("UseSparseArrays")` suppresses a legitimate Android lint warning (AddEquipmentFragment.java:41)

**File:** `AddEquipmentFragment.java`, line 41

**Evidence:**
```java
@SuppressLint("UseSparseArrays")
private HashMap<Integer, EquipmentTypeResultArray> mapEquipmentTypesForManu = new HashMap<>();
```

**Problem:** The `UseSparseArrays` lint check exists to encourage the use of `android.util.SparseArray` over `HashMap<Integer, V>` for memory efficiency on Android. The suppression silences a valid recommendation. While `HashMap` is functionally correct, the annotation indicates a deliberate decision that was not commented or justified. If the suppression is intentional (e.g., `SparseArray` is incompatible with some iteration pattern here), a comment explaining the decision should be added.

---

### A59-17 — INFO — `onActivityCreated(Bundle)` is deprecated in modern Fragment API (FleetFragment.java:202)

**File:** `FleetFragment.java`, line 202

**Evidence:**
```java
@Override
public void onActivityCreated(Bundle savedInstanceState) {
    super.onActivityCreated(savedInstanceState);
    hideLoadingLayout();
    initViews();
    ...
}
```

**Problem:** `Fragment.onActivityCreated()` was deprecated in `androidx.fragment:fragment:1.3.0`. The project uses `android.support.*` (the pre-AndroidX support library), so deprecation of this method may or may not apply depending on the exact support library version. Recorded for awareness as a future migration concern. Eight other fragments in the codebase also override this method, so the pattern is systemic.

---

### A59-18 — INFO — Wildcard import used in AddEquipmentFragment (AddEquipmentFragment.java:25)

**File:** `AddEquipmentFragment.java`, line 25

**Evidence:**
```java
import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*;
```

**Problem:** Wildcard imports import all public types in a package, making it unclear which result classes are actually used. This is minor but inconsistent: all other imports in this file and in the other two audited files are fully-qualified. IDEs and strict code-style configurations (Checkstyle, Google Java Style) typically forbid wildcards.

---

## Summary Table

| ID    | Severity | File                        | Line(s) | Description |
|-------|----------|-----------------------------|---------|-------------|
| A59-1 | HIGH     | AddEquipmentFragment.java   | 340     | Wrong map queried in `loadType` cache guard — always misses, causes redundant network requests |
| A59-2 | HIGH     | DashboardFragment.java      | 147–150 | Missing `break` before `default` in `onClick` switch — fall-through defect |
| A59-3 | MEDIUM   | FleetFragment.java          | 110,112 | Duplicate `setExtraOffsets` call — first call is dead code |
| A59-4 | MEDIUM   | FleetFragment.java          | 269     | `System.out.println` used for logging instead of `android.util.Log` |
| A59-5 | MEDIUM   | FleetFragment.java          | 273–275 | Commented-out code in permission-denied branch; permission denial silently ignored |
| A59-6 | MEDIUM   | DashboardFragment.java      | 89–96   | Realm `RealmChangeListener` registered but never deregistered — potential leak |
| A59-7 | MEDIUM   | DashboardFragment.java      | 35      | `static Bitmap userPhotoBitmap` is package-private and risks memory leak |
| A59-8 | MEDIUM   | DashboardFragment.java      | 108–111 | `getUserDetail()` bypasses `setUserPhoto()` static bitmap hand-off on resume |
| A59-9 | LOW      | DashboardFragment.java      | 123–130 | Empty `onStop()` / `onDestroy()` overrides serve no purpose |
| A59-10| LOW      | FleetFragment.java          | 207     | Yoda-style `false ==` comparison inconsistent with codebase style |
| A59-11| LOW      | FleetFragment.java          | 9, 29   | `Handler` and `ErrorDialog` unused imports |
| A59-12| LOW      | AddEquipmentFragment.java   | 45–46   | `TYPE_TITLE` / `FUEL_TITLE` should be `static final`, not instance fields |
| A59-13| LOW      | DashboardFragment.java      | 169     | Inconsistent Intent variable name `intent0` vs `intent` |
| A59-14| LOW      | AddEquipmentFragment.java   | 144     | Misspelled variable `grouppedCharacters` (double `p`) |
| A59-15| LOW      | AddEquipmentFragment.java   | 209,233,276,402 | User-facing label "manufacture" should be "manufacturer" |
| A59-16| LOW      | AddEquipmentFragment.java   | 41      | `@SuppressLint("UseSparseArrays")` suppresses legitimate lint with no explanatory comment |
| A59-17| INFO     | FleetFragment.java          | 202     | `onActivityCreated()` is deprecated in modern Fragment API |
| A59-18| INFO     | AddEquipmentFragment.java   | 25      | Wildcard import inconsistent with all other imports in these files |
