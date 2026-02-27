# Pass 4 — Code Quality Audit
**Agent:** A65
**Audit run:** 2026-02-26-01
**Files reviewed:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/ServiceEditFragment.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/ServiceRecordFragment.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/ServiceRecordListAdapter.java`

---

## Step 1: Reading Evidence

### File 1: ServiceEditFragment.java

**Class:** `ServiceEditFragment extends FleetFragment`
**Package:** `au.com.collectiveintelligence.fleetiq360.ui.fragment`

**Fields:**
| Name | Type | Visibility | Line |
|---|---|---|---|
| `TAG` | `static String` | `private` | 39 |
| `mRecordItems` | `ArrayList<ServiceRecordItem>` | package-private | 41 |
| `mCurrentIndex` | `int` | package-private | 42 |
| `mServiceRecordItem` | `ServiceRecordItem` | package-private | 43 |
| `status_text` | `TextView` | package-private | 45 |
| `hours_to_next_service` | `TextView` | package-private | 46 |
| `accumulate_hour` | `TextView` | package-private | 47 |
| `toggle_by_hours` | `RadioImageButton` | package-private | 48 |
| `toggle_by_interval` | `RadioImageButton` | package-private | 49 |
| `service_at` | `EditText` | package-private | 50 |
| `service_interval` | `EditText` | package-private | 51 |
| `service_title` | `TextView` | package-private | 52 |
| `previous_record` | `View` | package-private | 53 |
| `next_record` | `View` | package-private | 54 |
| `equipment_name` | `TextView` | package-private | 55 |
| `fromProfile` | `boolean` | `public` | 56 |

**Methods:**
| Line | Signature |
|---|---|
| 58 | `public static ServiceEditFragment createInstance(ArrayList<ServiceRecordItem> recordItems, int currentIndex)` |
| 67 | `@Override public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)` |
| 73 | `public void initViews()` |
| 137 | `void setData()` |
| 177 | `void initNaviButton()` |
| 197 | `void onNext()` |
| 208 | `void onPrevious()` |
| 218 | `void updateServiceTitle()` |
| 231 | `ServiceRecordItem getCurrentRecordItem()` |
| 241 | `@Override public void onMiddleButton(View view)` |
| 248 | `@Override public void onRightButton(View view)` |
| 345 | `void onServiceEdited()` |

**Commented-out imports:**
- Line 30–31: `/* import static android.support.v7.recyclerview.R.styleable.RecyclerView; */`

---

### File 2: ServiceRecordFragment.java

**Class:** `ServiceRecordFragment extends FleetFragment`
**Package:** `au.com.collectiveintelligence.fleetiq360.ui.fragment`

**Constants:**
| Name | Type | Visibility | Line |
|---|---|---|---|
| `TYPE_SET_HOURS` | `final static String` = `"setHrs"` | package-private | 35 |
| `TYPE_SET_INTERVAL` | `final static String` = `"setDur"` | package-private | 36 |
| `STATUS_NORMAL` | `private static final int` = `0` | `private` | 39 |
| `STATUS_DUE` | `private static final int` = `1` | `private` | 40 |
| `STATUS_OVERDUE` | `private static final int` = `2` | `private` | 41 |
| `STATUS_NOT_SET` | `private static final int` = `3` | `private` | 42 |
| `SERVICE_DUE_HOURS` | `private static final int` = `25` | `private` | 43 |

**Fields:**
| Name | Type | Visibility | Line |
|---|---|---|---|
| `listAdapter` | `ServiceRecordListAdapter` | `private` | 32 |
| `listData` | `ArrayList<ServiceRecordItem>` | `private` | 33 |
| `mChart` | `PieChart` | `private` | 37 |
| `fromProfile` | `boolean` = `true` | package-private | 45 |
| `serviceRecordResultArray` | `ServiceRecordResultArray` | `private` | 46 |

**Methods:**
| Line | Signature |
|---|---|
| 48 | `static int getStatus(ServiceRecordItem recordItem)` |
| 76 | `static int getColorForStatus(int status)` |
| 95 | `static String getTextForStatus(Context context, int status)` |
| 115 | `private static String getLabelForStatus(int status)` |
| 137 | `@Override public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)` |
| 142 | `public void initViews()` |
| 170 | `private void showServiceDetail(int position)` |
| 176 | `private void loadData()` |
| 198 | `@Override public void onMiddleButton(View view)` |
| 205 | `private void onData(ServiceRecordResultArray result)` |
| 225 | `private void initServiceChart()` |
| 231 | `private ArrayList<Integer> getColorForPieEntry(ArrayList<PieEntry> pieEntries)` |
| 247 | `private ArrayList<PieEntry> getServicePieData()` |
| 304 | `private void setData()` |

---

### File 3: ServiceRecordListAdapter.java

**Class:** `ServiceRecordListAdapter extends ArrayAdapter<ServiceRecordItem>`
**Package:** `au.com.collectiveintelligence.fleetiq360.ui.fragment`

**Inner class:** `static class ListHolder` (line 71)
- Fields: `TextView name` (line 72), `View status_bar` (line 73), `TextView status_text` (line 74)

**Fields:**
| Name | Type | Visibility | Line |
|---|---|---|---|
| `context` | `Context` | `private` | 18 |
| `mData` | `ArrayList<ServiceRecordItem>` | `private` | 19 |

**Methods:**
| Line | Signature |
|---|---|
| 21 | `ServiceRecordListAdapter(Context context, ArrayList<ServiceRecordItem> data)` (package-private) |
| 29 | `@Override @NonNull public View getView(int position, View convertView, @NonNull ViewGroup parent)` |
| 62 | `@Override public int getCount()` |
| 67 | `@Override public ServiceRecordItem getItem(int i)` |

---

## Step 2 & 3: Findings

---

### A65-1 — HIGH: `Integer.valueOf()` null-check is logically dead; `NumberFormatException` is the real crash risk

**File:** `ServiceEditFragment.java`
**Lines:** 254–270

```java
Integer lastService = Integer.valueOf(sa);
if(null == lastService) {
    showToast("Please enter a valid number for the hours of last service");
    return;
}

sa = service_interval.getText().toString();
Integer serviceInterval = Integer.valueOf(sa);
if(null == serviceInterval) {
    ...
    return;
}
```

`Integer.valueOf(String)` never returns `null`. It either returns a valid `Integer` or throws `NumberFormatException` if the input is not a valid integer string (e.g., empty string, non-numeric text). The null-checks on lines 255 and 262 are therefore always `false` and never execute — the guard is completely non-functional. If a user enters an empty string or any non-numeric text, the app will throw an uncaught `NumberFormatException` and crash. The correct approach is to wrap the calls in a `try/catch NumberFormatException` block. This is a latent crash that can be triggered by ordinary user interaction.

---

### A65-2 — HIGH: Deprecated `Resources.getColor(int)` API used without theme context across all three files

**Files:**
- `ServiceEditFragment.java` line 145
- `ServiceRecordFragment.java` lines 235, 237, 239, 241, 322
- `ServiceRecordListAdapter.java` line 55

```java
// ServiceEditFragment.java:145
status_text.setTextColor(getResources().getColor(ServiceRecordFragment.getColorForStatus(status)));

// ServiceRecordFragment.java:322
data.setValueTextColor(getResources().getColor(R.color.text_black));

// ServiceRecordListAdapter.java:55
holder.status_bar.setBackgroundColor(getContext().getResources().getColor(color));
```

`Resources.getColor(int)` was deprecated in API 23 (Android 6.0, Marshmallow). The replacement is `ContextCompat.getColor(Context, int)` or `Resources.getColor(int, Theme)`. With `compileSdkVersion = 26`, the compiler generates a deprecation warning for every one of these calls. The deprecated variant ignores the current theme and may produce incorrect colors on API 23+ devices using themed color states. This pattern recurs in 7 call sites across 3 files and is consistently applied in the wrong direction (never using the replacement API), indicating the issue was not addressed at all during development.

---

### A65-3 — MEDIUM: Commented-out import in `ServiceEditFragment.java` is dead code

**File:** `ServiceEditFragment.java`
**Lines:** 29–31

```java
/*
import static android.support.v7.recyclerview.R.styleable.RecyclerView;
*/
```

This commented-out static import serves no purpose. The class does not use a `RecyclerView` or its styleable attributes anywhere — the list display is done via a `ListView` in the sibling adapter. The import was likely left from an experimental or abandoned implementation. Commented-out code of this kind should be deleted; it adds noise, misleads the reader about class dependencies, and may indicate an unfinished refactoring.

---

### A65-4 — MEDIUM: `onServiceEdited()` is an empty, unreachable stub — dead code

**File:** `ServiceEditFragment.java`
**Lines:** 345–347

```java
void onServiceEdited() {

}
```

`onServiceEdited()` has an empty body and is never called from any location within the codebase (confirmed by cross-file search). It is not an override of any interface or superclass method. It was never wired up in `onRightButton()` where the save logic resides, and the save callback directly calls `setData()` instead. This is either scaffolding left from an early design or a callback that was planned but never implemented. As dead code it should be removed or, if the intent was to notify the parent fragment/activity of the edit, properly implemented.

---

### A65-5 — MEDIUM: `public boolean fromProfile` field on `ServiceEditFragment` is set by direct field mutation — leaky abstraction and Fragment lifecycle hazard

**File:** `ServiceEditFragment.java` line 56; `ServiceRecordFragment.java` line 172

```java
// ServiceEditFragment.java
public boolean fromProfile;

// ServiceRecordFragment.java – caller
ServiceEditFragment serviceEditFragment = ServiceEditFragment.createInstance(listData, position);
serviceEditFragment.fromProfile = fromProfile;
```

`fromProfile` is a `public` instance field mutated directly after construction. This exposes internal navigation state as a public concern. More critically, Fragment arguments set as fields are not preserved across system-driven Fragment re-creation (e.g., after a process death or configuration change). The Android-idiomatic solution is to use `Fragment.setArguments(Bundle)` and read from `getArguments()` in `onCreateView` or `onCreate`. The field bypasses this lifecycle contract entirely. The `fromProfile` field pattern is replicated across `ServiceRecordFragment` (package-private) and `DriverStatsFragment2`, making this a systemic issue in the navigation layer, but the `public` visibility in `ServiceEditFragment` is the most severe form.

---

### A65-6 — MEDIUM: `TYPE_SET_HOURS` and `TYPE_SET_INTERVAL` constants are package-private on `ServiceRecordFragment` but accessed cross-class — leaky abstraction

**File:** `ServiceRecordFragment.java` lines 35–36; `ServiceEditFragment.java` lines 157, 163, 287, 298

```java
// ServiceRecordFragment.java
final static String TYPE_SET_HOURS = "setHrs";
final static String TYPE_SET_INTERVAL = "setDur";

// ServiceEditFragment.java — cross-class access
parameter.service_type = ServiceRecordFragment.TYPE_SET_HOURS;
parameter.service_type = ServiceRecordFragment.TYPE_SET_INTERVAL;
```

These constants define the domain protocol for service type strings exchanged between the UI layer and the web service. They are defined on `ServiceRecordFragment` — a UI Fragment class — and directly referenced by `ServiceEditFragment` via class-qualified access (`ServiceRecordFragment.TYPE_SET_HOURS`). This tightly couples two distinct UI fragments through the UI class itself rather than through a shared domain constant, an enum, or the data model class (`ServiceRecordItem`). The constants belong in the domain or web-service layer (e.g., `ServiceRecordItem` or a dedicated constants class), not in a Fragment. The current arrangement means that `ServiceEditFragment` cannot be compiled without `ServiceRecordFragment` on its classpath.

---

### A65-7 — MEDIUM: Type mismatch — `service_due` and `acc_hours` are `double` in the model but compared and displayed as integers

**File:** `ServiceEditFragment.java` lines 146–147, 272, 279, 315–316, 324
**File:** `ServiceRecordFragment.java` lines 57–70
**Reference:** `ServiceRecordItem.java` lines 14, 16

```java
// ServiceRecordItem.java — declared as double
public double acc_hours;
public double service_due;

// ServiceEditFragment.java — compared using integer semantics
if(lastService > mServiceRecordItem.acc_hours){   // Integer vs double (implicit widening)
    ...
}
if(serviceInterval < mServiceRecordItem.acc_hours){ // Integer vs double (implicit widening)
    ...
}

// ServiceRecordFragment.java — equality check on double
if (recordItem.service_due == 0 && recordItem.acc_hours == 0) {  // floating-point equality
    return STATUS_NOT_SET;
}
```

`acc_hours` and `service_due` are stored as `double`. The `getStatus()` method in `ServiceRecordFragment` (line 57) uses `== 0` equality comparison on doubles, which is unreliable for floating-point values — a value of `0.0000001` would not trigger the check. The validation in `ServiceEditFragment.onRightButton()` compares user-entered `Integer` values directly against `double` fields via implicit widening, which may silently accept fractional edge cases (e.g., `lastService = 5` passes when `acc_hours = 5.5`). Additionally, the display on lines 146–147 converts via string concatenation (`service_due+""`, `acc_hours+""`) producing raw double representation (e.g., `"25.0"` instead of `"25"`), which is poor UX.

---

### A65-8 — MEDIUM: `Objects.requireNonNull(listData)` is redundant — `listData` is initialized at declaration and cannot be null

**File:** `ServiceRecordFragment.java` line 212

```java
if (Objects.requireNonNull(listData).size() == 0) {
```

`listData` is declared at line 33 and immediately initialized: `private ArrayList<ServiceRecordItem> listData = new ArrayList<>()`. It is never reassigned to `null` anywhere in the class. `Objects.requireNonNull()` on a field that cannot be null is misleading — it implies to a reader that null is a possible state, and it also throws `NullPointerException` rather than a more descriptive error if it ever were null. The check adds noise without defensive value. The correct pattern, if null-safety on the field were genuinely desired, would be an assertion or proper documentation.

---

### A65-9 — MEDIUM: `private static String TAG` in `ServiceEditFragment` is declared but never used

**File:** `ServiceEditFragment.java` line 39

```java
private static String TAG = ServiceEditFragment.class.getSimpleName();
```

`TAG` is declared and assigned but no call to `Log.d`, `Log.e`, `Log.w`, or any other logging method appears anywhere in the file. The field is dead. Additionally, the `TAG` field is declared as `String` (mutable) rather than the idiomatic `static final String`, which means it can be accidentally reassigned at runtime. Every other Android project convention and Android Studio's lint rule (`LogTagMismatch`) expects tag fields to be `private static final String`. This is a style inconsistency with standard Android conventions.

---

### A65-10 — LOW: `ServiceRecordListAdapter` stores a redundant `context` field

**File:** `ServiceRecordListAdapter.java` lines 18, 23, 35, 56

```java
private Context context;
...
this.context = context;
...
LayoutInflater inflater = ((Activity) context).getLayoutInflater();
...
String s = ServiceRecordFragment.getTextForStatus(getContext(), status);
```

The adapter stores a `private Context context` field (line 18) but simultaneously inherits `getContext()` from `ArrayAdapter` (used correctly on line 56). Line 35 uses the stored `context` field via a cast to `Activity` to obtain a `LayoutInflater`. The `ArrayAdapter` superclass already holds a `Context` reference accessible via `getContext()`, making the separately stored `context` field redundant. Storing it separately also risks a subtle bug: if the `Context` passed to the constructor is later destroyed (e.g., an `Activity` that finishes), the stored reference leaks the `Activity`. The `ArrayAdapter`-managed `Context` and `getContext()` should be used exclusively.

---

### A65-11 — LOW: `getColorForStatus()` and `getTextForStatus()` use `if`-chains instead of `switch` — inconsistent with `getLabelForStatus()` pattern; all four status utility methods lack `else` on final branch

**File:** `ServiceRecordFragment.java` lines 76–113, 115–133

All four status utility methods (`getStatus`, `getColorForStatus`, `getTextForStatus`, `getLabelForStatus`) follow the same sequential `if`-without-`else` pattern:

```java
if (status == STATUS_NORMAL) { return ...; }
if (status == STATUS_NOT_SET) { return ...; }
if (status == STATUS_DUE)    { return ...; }
if (status == STATUS_OVERDUE) { return ...; }
return R.color.service_status_not_set;  // fallback
```

This pattern means every branch (except the first matching one) evaluates all preceding conditions unnecessarily — a `switch` on int constants or `else if` chaining would be more idiomatic and communicate mutual exclusivity. The inconsistency is within this file itself: all methods use the same pattern, but `getStatus()` uses a structured sequence with early returns that is slightly different from the others. Minor, but across four parallel methods the inconsistency accumulates.

---

### A65-12 — LOW: `setData()` name collision between `ServiceEditFragment` and `ServiceRecordFragment` — confusing naming when both are active

**File:** `ServiceRecordFragment.java` line 304
**File:** `ServiceEditFragment.java` line 137

Both classes define a package-private method named `setData()`. In `ServiceRecordFragment`, `setData()` populates the `PieChart` (lines 304–327). In `ServiceEditFragment`, `setData()` populates all UI form fields from the current `ServiceRecordItem` (lines 137–175). The method is also called from `initServiceChart()` in `ServiceRecordFragment` (line 227), where it sits immediately after `initChart()` and `initChartExtra()` — the `setData()` name is ambiguous relative to those adjacent method calls. A more descriptive name (e.g., `populateFormFields()` and `populateChart()`) would eliminate the confusion.

---

### A65-13 — LOW: `fromProfile` field in `ServiceRecordFragment` has `true` as default but is set to `false` by the non-profile caller — inverted default

**File:** `ServiceRecordFragment.java` line 45

```java
boolean fromProfile = true;
```

The field defaults to `true`, meaning if a caller forgets to set it, the fragment will silently behave as if launched from the profile screen. Examining the codebase, the only known setter is via `DriverStatsFragment2.java` which sets `fragment.fromProfile = false` when navigating to this fragment outside the profile context. A missed assignment defaults to `fromProfile = true` rather than to the safer "no profile context" state. A default of `false` with explicit opt-in for `fromProfile = true` would be less hazardous.

---

### A65-14 — INFO: `ServiceRecordListAdapter` constructor is package-private — inconsistent with `ArrayAdapter` convention

**File:** `ServiceRecordListAdapter.java` line 21

```java
ServiceRecordListAdapter(Context context, ArrayList<ServiceRecordItem> data) {
```

The constructor has no access modifier (package-private). `ArrayAdapter` subclasses are conventionally `public` to allow instantiation from any context. While the adapter is only used within the same package (`ServiceRecordFragment.java` line 155), the lack of a modifier is likely an omission rather than an intentional encapsulation decision. If the class were ever moved to a different package or the Fragment refactored out, this would require a modifier change.

---

## Step 4: Summary Table

| ID | Severity | File | Description |
|---|---|---|---|
| A65-1 | HIGH | ServiceEditFragment.java:254–270 | `Integer.valueOf()` null-check is always false; `NumberFormatException` crash on non-numeric input is unguarded |
| A65-2 | HIGH | All three files (7 call sites) | Deprecated `Resources.getColor(int)` without theme — API 23 deprecation warning at every call site |
| A65-3 | MEDIUM | ServiceEditFragment.java:29–31 | Commented-out import (`RecyclerView` styleable) — dead code, should be deleted |
| A65-4 | MEDIUM | ServiceEditFragment.java:345–347 | `onServiceEdited()` empty body, never called — dead stub code |
| A65-5 | MEDIUM | ServiceEditFragment.java:56 / ServiceRecordFragment.java:172 | `public boolean fromProfile` set by direct field mutation — bypasses Fragment `Arguments` lifecycle contract |
| A65-6 | MEDIUM | ServiceRecordFragment.java:35–36 / ServiceEditFragment.java:157,287 | `TYPE_SET_HOURS`/`TYPE_SET_INTERVAL` owned by a Fragment but accessed cross-class — domain constants in wrong layer |
| A65-7 | MEDIUM | ServiceEditFragment.java:272,279 / ServiceRecordFragment.java:57 | `double` fields compared with `== 0` (floating-point equality) and with `Integer` values; raw double display in UI |
| A65-8 | MEDIUM | ServiceRecordFragment.java:212 | `Objects.requireNonNull(listData)` on a field that is initialized at declaration and never null — misleading and redundant |
| A65-9 | MEDIUM | ServiceEditFragment.java:39 | `TAG` declared but never used; declared as mutable `String` not `static final String` |
| A65-10 | LOW | ServiceRecordListAdapter.java:18,23,35 | Redundant `context` field — duplicates `ArrayAdapter.getContext()`; cast to `Activity` risks `ClassCastException` |
| A65-11 | LOW | ServiceRecordFragment.java:76–133 | Sequential `if` chains without `else` across four parallel status methods — `switch` or `else if` is idiomatic |
| A65-12 | LOW | ServiceEditFragment.java:137 / ServiceRecordFragment.java:304 | Both classes have a `setData()` method — ambiguous naming, different semantics |
| A65-13 | LOW | ServiceRecordFragment.java:45 | `fromProfile = true` default is inverted — missing assignment silently enables profile-context behavior |
| A65-14 | INFO | ServiceRecordListAdapter.java:21 | Constructor is package-private — likely unintentional; inconsistent with `ArrayAdapter` convention |
