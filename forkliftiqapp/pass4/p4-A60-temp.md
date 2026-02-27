# Pass 4 Code Quality — Agent A60
**Audit run:** 2026-02-26-01
**Agent:** A60
**Date:** 2026-02-27

## Assigned Files
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/DriverListFragment.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/DriverStatsFragment1.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/DriverStatsFragment2.java`

---

## Step 1: Reading Evidence

### File 1: DriverListFragment.java

**Class:** `DriverListFragment extends FleetFragment implements AbsRecyclerAdapter.OnItemClickListener`

**Fields:**
- `private SelectDriverAdapter adapter` (line 25)

**Methods (exhaustive):**

| Method | Line |
|---|---|
| `onCreate(Bundle savedInstanceState)` | 28 |
| `onCreateView(@NonNull LayoutInflater, ViewGroup, Bundle)` | 33 |
| `initViews()` | 38 |
| `onItemClick(View v, int position)` | 55 |
| `updateDriverList(List<User> drivers)` | 61 |
| `onRightButton(View view)` | 66 |
| `onMiddleButton(View view)` | 70 |

**Types/constants/interfaces:** None defined within the class.

**Imports used:** `ComponentName`, `Intent`, `Bundle`, `NonNull`, `LinearLayoutManager`, `RecyclerView`, `LayoutInflater`, `View`, `ViewGroup`, `R`, `SelectDriverPresenter`, `DashboardActivity`, `AbsRecyclerAdapter`, `SelectDriverAdapter`, `FleetFragment`, `CurrentUser`, `User`, `List`, `Objects`.

---

### File 2: DriverStatsFragment1.java

**Class:** `DriverStatsFragment1 extends FleetFragment`

**Fields:**
- `private final static String STATS_KEY_USAGE = "usage"` (line 23)
- `private DriverStatsListAdapter listAdapter` (line 24)
- `private ArrayList<DriverStatsItem> listServiceStatsData` (line 25)
- `private GetDriverStatsResultArray driverStatsResultArray` (line 26)

**Methods (exhaustive):**

| Method | Line |
|---|---|
| `onCreateView(@NonNull LayoutInflater, ViewGroup, Bundle)` | 30 |
| `initViews()` | 35 |
| `getUserDetail()` | 54 |
| `loadData()` | 59 |
| `setUserData()` | 81 |
| `onData(GetDriverStatsResultArray resultArray)` | 92 |
| `onRightButton(View view)` | 124 |

**Types/constants/interfaces:**
- Constant: `STATS_KEY_USAGE = "usage"` (line 23, `private final static String`)

**Imports used:** `Bundle`, `NonNull`, `Nullable`, `LayoutInflater`, `View`, `ViewGroup`, `ImageView`, `ListView`, `TextView`, `R`, wildcard `au.com.collectiveintelligence.fleetiq360.WebService.*`, `FleetFragment`, `CurrentUser`, `User`, `ArrayList`, `Collections`, `Comparator`.

---

### File 3: DriverStatsFragment2.java

**Class:** `DriverStatsFragment2 extends FleetFragment`

**Fields:**
- `private ServiceStatsListAdapter listAdapter` (line 25)
- `private ArrayList<DriverStatsItem> listServiceStatsData` (line 26)
- `private float preStartFailed = 0.0f` (line 27)
- `private float preStartIncomplete = 0.0f` (line 28)
- `private TextView user_name` (line 30)
- `boolean fromProfile = true` (line 31) — package-private
- `private GetDriverStatsResultArray driverStatsResultArray` (line 32)
- `private ArrayList<TextView> views = new ArrayList<>()` (line 97) — initialized inline and again in `initEquipmentViews()`
- `private PieChart mChart` (line 160)
- `private final String LABEL_FAILED = "FAILED"` (line 176)
- `private final String LABEL_INCOMPLETE = "INCOMPLETE"` (line 177)
- `private final String LABEL_COMPLETED = "COMPLETED"` (line 178)

**Methods (exhaustive):**

| Method | Line |
|---|---|
| `onCreateView(@NonNull LayoutInflater, ViewGroup, Bundle)` | 36 |
| `initViews()` | 41 |
| `setUserData()` | 66 |
| `getUserDetail()` | 70 |
| `loadData()` | 75 |
| `initEquipmentViews()` | 99 |
| `setUserEquipments()` | 109 |
| `onData(GetDriverStatsResultArray resultArray)` | 126 |
| `initServiceChart()` | 162 |
| `getColorForPieEntry(ArrayList<PieEntry> pieEntries)` | 180 |
| `getServicePieData()` | 198 |
| `setData()` | 218 |
| `onRightButton(View view)` | 243 |

**Types/constants/interfaces:**
- `LABEL_FAILED = "FAILED"` (line 176, `private final String`)
- `LABEL_INCOMPLETE = "INCOMPLETE"` (line 177, `private final String`)
- `LABEL_COMPLETED = "COMPLETED"` (line 178, `private final String`)

**Imports used:** `Bundle`, `NonNull`, `Nullable`, `LayoutInflater`, `View`, `ViewGroup`, `ImageView`, `ListView`, `TextView`, `R`, wildcard `au.com.collectiveintelligence.fleetiq360.WebService.*`, `FleetFragment`, `CurrentUser`, `PieChart`, `PieData`, `PieDataSet`, `PieEntry`, `PercentFormatter`, `ArrayList`.

---

## Step 2 & 3: Code Quality Findings

---

### A60-1 — HIGH — Duplicated `getUserDetail()` / `setUserData()` call in `initViews()` (DSF1 and DSF2)

**File:** `DriverStatsFragment1.java` lines 36–52; `DriverStatsFragment2.java` lines 41–64

In both fragments, `initViews()` calls `setUserData()` directly (DSF1 line 82 via `getUserDetail()`, and DSF2 line 54), and then immediately calls `getUserDetail()` (DSF1 line 51, DSF2 line 63). `getUserDetail()` in turn calls `UserPhotoFragment.showUserPhoto(...)` and `setUserData()` again — meaning `setUserData()` executes **twice** on every `initViews()` call, and `UserPhotoFragment.showUserPhoto(...)` also executes twice.

DSF1 `initViews()` (lines 36–52):
```java
UserPhotoFragment.showUserPhoto(...)  // line 36 — first call
...
loadData();
getUserDetail();  // line 51 — calls showUserPhoto() and setUserData() a second time
```

DSF1 `getUserDetail()` (lines 54–57):
```java
private void getUserDetail() {
    UserPhotoFragment.showUserPhoto((ImageView) mRootView.findViewById(R.id.user_photo));
    setUserData();
}
```

DSF1 `initViews()` also sets `user_name` directly at line 43:
```java
TextView user_name = mRootView.findViewById(R.id.user_name);
user_name.setText(CurrentUser.get().definedName());
```
Then `setUserData()` (line 82) sets the same `R.id.user_name` again via `findViewById`. This is three redundant setText calls on the same view per `initViews()`.

The same pattern is present in DSF2 `initViews()` (line 54 calls `setUserData()`, line 63 calls `getUserDetail()` which calls `setUserData()` again).

**Impact:** Wasted UI work on every navigation to these fragments; indicates copy-paste error and the `getUserDetail()` method has no purpose distinct from calling `setUserData()`.

---

### A60-2 — HIGH — Wildcard import of entire `WebService` package

**File:** `DriverStatsFragment1.java` line 13; `DriverStatsFragment2.java` line 13

```java
import au.com.collectiveintelligence.fleetiq360.WebService.*;
```

Wildcard imports make it impossible to determine at a glance which classes from the package are actually consumed, prevent tooling from detecting unused imports, and create a risk of silent name collisions if new classes are added to the package. Neither `DriverListFragment.java` (which uses specific imports) nor the Android project convention supports wildcard imports. This is a style inconsistency across the three assigned files.

---

### A60-3 — HIGH — `Double.valueOf(s)` result compared against `null` is always non-null or throws

**File:** `DriverStatsFragment2.java` lines 137–150

```java
Double d = Double.valueOf(s);
if (d != null) {
    preStartFailed = d.floatValue();
} else {
    preStartFailed = 0.0f;
}
```

`Double.valueOf(String)` never returns `null`; it either returns a boxed `Double` or throws `NumberFormatException`. The `null` guard is therefore dead code — the `else` branch is unreachable. If `s` is not a parseable number, an uncaught `NumberFormatException` will propagate and crash the fragment. The pattern in `DriverStatsFragment1` for analogous parsing (`Float.valueOf` inside a try/catch with `ignored`) is correct but is inconsistent with this handling. The same issue appears twice in `onData()` — once for `STATS_KEY_PRE_START_FAILED` (lines 136–142) and once for `STATS_KEY_PRE_START_INCOMPLETE` (lines 143–150).

---

### A60-4 — MEDIUM — String constants defined as local variables instead of class-level constants

**File:** `DriverStatsFragment2.java` lines 130–132

```java
String STATS_KEY_PRE_START_INCOMPLETE = "incompleted";
String STATS_KEY_PRE_START_FAILED = "failed";
String STATS_KEY_SERVICE = "service";
```

These three string keys are declared as local variables inside `onData()`, which is called potentially multiple times (once from `loadData()` on cache hit, once from the network callback). Declaring them as local variables on every call is wasteful and unconventional. By contrast, `DriverStatsFragment1` correctly defines `STATS_KEY_USAGE` as a `private final static String` class-level constant (line 23). This is a direct style inconsistency between the two sibling fragments.

---

### A60-5 — MEDIUM — `views` field double-initialised: inline initializer overwritten immediately in `initEquipmentViews()`

**File:** `DriverStatsFragment2.java` lines 97 and 100

```java
private ArrayList<TextView> views = new ArrayList<>();   // line 97 — inline init

private void initEquipmentViews() {
    views = new ArrayList<>();   // line 100 — immediately reassigned
    ...
}
```

The inline initialisation at line 97 creates an `ArrayList` that is never used because `initEquipmentViews()` is always called from `initViews()` before any access to `views`, and it unconditionally replaces it. The allocation at line 97 is pure waste and creates confusion about the field's lifecycle.

---

### A60-6 — MEDIUM — Leaky abstraction: `fromProfile` is a package-private field mutated directly by a sibling fragment

**File:** `DriverStatsFragment2.java` line 31; `ServiceRecordFragment.java` line 45; caller in `DriverStatsFragment2.java` `onRightButton()` line 246

```java
// DriverStatsFragment2.java line 31
boolean fromProfile = true;

// DriverStatsFragment2.java onRightButton — line 246
ServiceRecordFragment fragment = new ServiceRecordFragment();
fragment.fromProfile = false;   // direct field mutation
```

Both `DriverStatsFragment2` and `ServiceRecordFragment` expose `fromProfile` as a package-private field that callers mutate directly rather than passing via a factory method, constructor argument, or `Bundle` argument. This tightly couples fragment creation to their internal state and bypasses Android's recommended pattern of passing state via `Fragment.setArguments(Bundle)`, which also survives process death and recreation. The same anti-pattern exists in `ServiceRecordFragment` (confirmed at line 45 of that file).

---

### A60-7 — MEDIUM — `getResources().getColor(int)` used without a theme context (deprecated API)

**File:** `DriverStatsFragment2.java` lines 185, 188, 191, 235

```java
colorList.add(getResources().getColor(R.color.service_status_normal));   // line 185
colorList.add(getResources().getColor(R.color.service_status_due));       // line 188
colorList.add(getResources().getColor(R.color.service_status_overdue));   // line 191
data.setValueTextColor(getResources().getColor(R.color.text_black));      // line 235
```

`Resources.getColor(int)` without a `Theme` parameter has been deprecated since API 23 (Android 6.0 Marshmallow). The replacement is `ContextCompat.getColor(context, id)` or `getResources().getColor(id, getActivity().getTheme())`. This will generate build warnings on modern compileSdkVersions and may produce incorrect colours on devices using dynamic theming.

---

### A60-8 — MEDIUM — `onCreate()` in `DriverListFragment` is an empty override

**File:** `DriverListFragment.java` lines 28–30

```java
@Override
public void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
}
```

The method contains only a `super` call and performs no work of its own. It provides no value and adds visual noise. It should be removed unless future work is planned there (no TODO comment is present).

---

### A60-9 — MEDIUM — Inconsistent null-safety in `setUserData()` between DSF1 and DSF2

**File:** `DriverStatsFragment1.java` lines 82–89; `DriverStatsFragment2.java` lines 66–68

DSF1 `setUserData()` guards against a null `CurrentUser`:
```java
// DSF1 lines 84–89
User user = CurrentUser.get();
if (user != null) {
    ...
}
```
But DSF1 also calls `CurrentUser.get().definedName()` at line 82 unconditionally before that guard, which will throw a `NullPointerException` if `CurrentUser.get()` returns null:
```java
((TextView) mRootView.findViewById(R.id.user_name)).setText(CurrentUser.get().definedName());
```

DSF2 `setUserData()` has no null guard at all:
```java
// DSF2 lines 66–68
private void setUserData() {
    user_name.setText(CurrentUser.get().definedName());
}
```

Both fragments are inconsistent with each other and DSF1 is internally inconsistent (null guard on line 85 that is effectively bypassed by the NPE risk on line 82).

---

### A60-10 — LOW — Non-conventional field naming (`user_name`, `service_record_list` as snake_case)

**File:** `DriverStatsFragment2.java` line 30; `DriverStatsFragment1.java` line 45

```java
private TextView user_name;         // DSF2 line 30
ListView service_record_list = ...;  // DSF1 line 45 (local variable)
```

Java convention (Google Java Style Guide, Android conventions) requires `lowerCamelCase` for field and variable names. `user_name` and `service_record_list` use `snake_case`. `DriverListFragment` and the rest of the codebase use `lowerCamelCase` correctly. This is a style inconsistency across the assigned files.

---

### A60-11 — LOW — `onMiddleButton()` is an empty override with no indication of intent

**File:** `DriverListFragment.java` lines 70–72

```java
@Override
public void onMiddleButton(View view) {
}
```

The bottom bar for this fragment has `null` for both the middle label (line 40: `String[] sa = {"DASHBOARD", null, null}`) and passes `-1` equivalent logic, yet the override exists. Unlike `onRightButton` which also does nothing but could plausibly have future intent, the middle slot is configured as null/disabled in `initViews()`. An empty override with no comment provides no information to future maintainers.

---

### A60-12 — LOW — `initViews()` is public but should be protected or package-private

**File:** `DriverListFragment.java` line 38; `DriverStatsFragment1.java` line 35; `DriverStatsFragment2.java` line 41

All three fragments expose `initViews()` as `public`. Examination of `FleetFragment` and the base class pattern suggests this method is called from the hosting activity or a base class. However, marking it `public` exposes it to any component in the application. If it is called only by the host activity/base fragment, `protected` or package-private visibility would be more appropriate and would better encapsulate the fragment's initialization contract.

---

### A60-13 — LOW — `DriverStatsFragment1.onData()` accesses `resultArray.arrayList` as a public field

**File:** `DriverStatsFragment1.java` lines 95, and `DriverStatsFragment2.java` line 129

```java
for (DriverStatsItem driverStatsItem : resultArray.arrayList) {
```

`GetDriverStatsResultArray.arrayList` is accessed as a direct public field from both fragment classes. This is a leaky abstraction from the `WebService` layer — the internal representation of the result collection is directly exposed to UI fragment code. A getter method would encapsulate the internal structure and allow the `WebService` model to evolve without requiring changes to all consumers.

---

## Summary Table

| ID | Severity | File(s) | Description |
|---|---|---|---|
| A60-1 | HIGH | DSF1, DSF2 | `getUserDetail()` / `setUserData()` called redundantly from `initViews()` — double UI work on every load |
| A60-2 | HIGH | DSF1, DSF2 | Wildcard import of entire `WebService` package — inconsistent with DSF0 / rest of codebase |
| A60-3 | HIGH | DSF2 | `Double.valueOf(s) != null` dead guard — unreachable else branch; `NumberFormatException` unhandled |
| A60-4 | MEDIUM | DSF2 | Stats key strings declared as local variables in `onData()` instead of class-level constants (inconsistent with DSF1) |
| A60-5 | MEDIUM | DSF2 | `views` field inline-initialised then immediately replaced in `initEquipmentViews()` — wasted allocation |
| A60-6 | MEDIUM | DSF2 | `fromProfile` exposed as package-private mutable field; bypasses `Fragment.setArguments(Bundle)` pattern |
| A60-7 | MEDIUM | DSF2 | `getResources().getColor(int)` deprecated since API 23 — missing theme context; build warnings |
| A60-8 | MEDIUM | DLF | Empty `onCreate()` override with no body beyond `super` call — should be removed |
| A60-9 | MEDIUM | DSF1, DSF2 | Inconsistent null-safety for `CurrentUser.get()` — NPE risk in DSF1 line 82 despite guard at line 85; no guard in DSF2 |
| A60-10 | LOW | DSF1, DSF2 | `snake_case` field/variable names (`user_name`, `service_record_list`) violate Java/Android naming convention |
| A60-11 | LOW | DLF | `onMiddleButton()` empty override with no comment; middle slot is configured as disabled |
| A60-12 | LOW | DLF, DSF1, DSF2 | `initViews()` is `public` when `protected` or package-private would be sufficient |
| A60-13 | LOW | DSF1, DSF2 | Direct access to `GetDriverStatsResultArray.arrayList` public field from UI layer — leaky abstraction |

**File abbreviations:** DLF = DriverListFragment, DSF1 = DriverStatsFragment1, DSF2 = DriverStatsFragment2
