# Pass 4 — Code Quality Audit
**Audit run:** 2026-02-26-01
**Agent:** A64
**Date:** 2026-02-27
**Files reviewed:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/ProfileFragment.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/SavedReportFragment.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/SavedReportListAdapter.java`

---

## Step 1: Reading Evidence

### File 1 — ProfileFragment.java

**Class:** `ProfileFragment` (extends `FleetFragment`, implements `View.OnClickListener`)
**Package:** `au.com.collectiveintelligence.fleetiq360.ui.fragment`

**Fields:**
- `ProfileActivity activity` (package-private, line 28)
- `private EditText lastEText, firstEText` (line 29)
- `private LinearLayout editButton` (line 30)
- `private LinearLayout saveButton` (line 31)

**Methods (exhaustive):**

| Line | Method | Visibility |
|------|--------|------------|
| 34 | `onCreateView(LayoutInflater, ViewGroup, Bundle)` | public (override) |
| 40 | `onActivityCreated(Bundle)` | public (override) |
| 46 | `setUserData()` | private |
| 59 | `initViews()` | public |
| 79 | `onLeftButton(View)` | public (override) |
| 84 | `onRightButton(View)` | public (override) |
| 89 | `onResume()` | public (override) |
| 94 | `onStop()` | public (override) |
| 99 | `onDestroy()` | public (override) |
| 103 | `saveModifiedResult()` | private |
| 122 | `updateUser(int, UpdateUserParameter)` | private |
| 147 | `onEnableEdit(boolean)` | private |
| 155 | `onClick(View)` | public (override) |

**Types/Interfaces defined:** none
**Enums/Constants defined:** none
**Static imports used:** `android.view.View.INVISIBLE`, `android.view.View.VISIBLE` (lines 24–25)

---

### File 2 — SavedReportFragment.java

**Class:** `SavedReportFragment` (extends `FleetFragment`)
**Package:** `au.com.collectiveintelligence.fleetiq360.ui.fragment`

**Fields:**
- `private SavedReportListAdapter listAdapter` (line 23)
- `private ArrayList<ReportItem> listData = new ArrayList<>()` (line 24)

**Methods (exhaustive):**

| Line | Method | Visibility |
|------|--------|------------|
| 28 | `onCreateView(LayoutInflater, ViewGroup, Bundle)` | public (override) |
| 33 | `initViews()` | public |
| 45 | `loadData()` | private |
| 65 | `onData(ReportResultArray)` | private |
| 71 | `onResend(ReportItem)` | package-private |

**Types/Interfaces defined:** none
**Enums/Constants defined:** none

**Trailing blank lines:** lines 93–97 (four empty lines after closing brace)

---

### File 3 — SavedReportListAdapter.java

**Class:** `SavedReportListAdapter` (extends `ArrayAdapter<ReportItem>`)
**Inner class:** `ListHolder` (static, line 70)
**Package:** `au.com.collectiveintelligence.fleetiq360.ui.fragment`

**Fields:**
- `private Context context` (line 18)
- `private ArrayList<ReportItem> mData` (line 19)
- `SavedReportFragment savedReportFragment` (package-private, line 20)

**Inner class fields:**
- `TextView name` (line 71, package-private)
- `View resend_report_view` (line 72, package-private)

**Methods (exhaustive):**

| Line | Method | Visibility |
|------|--------|------------|
| 22 | `SavedReportListAdapter(Context, ArrayList<ReportItem>)` | package-private |
| 30 | `getView(int, View, ViewGroup)` | public (override) |
| 61 | `getCount()` | public (override) |
| 66 | `getItem(int)` | public (override) |

**Types/Interfaces defined:**
- Static inner class `ListHolder` (line 70)

**Enums/Constants defined:** none

---

## Step 2 & 3: Findings

---

### A64-1 — MEDIUM: Empty lifecycle override methods serve no purpose

**File:** `ProfileFragment.java`
**Lines:** 79–101

```java
@Override
public void onLeftButton(View view) {
    super.onLeftButton(view);
}

@Override
public void onRightButton(View view) {
    super.onRightButton(view);
}

@Override
public void onResume() {
    super.onResume();
}

@Override
public void onStop() {
    super.onStop();
}

@Override
public void onDestroy() {
    super.onDestroy();
}
```

Five overrides — `onLeftButton`, `onRightButton`, `onResume`, `onStop`, `onDestroy` — do nothing except delegate to `super`. They add noise, inflate the class, and suggest intent to implement behaviour that was never completed. They should be deleted unless there is a specific planned use.

**Classification:** MEDIUM (dead code — stale scaffolding)

---

### A64-2 — HIGH: Package-private field `activity` on ProfileFragment creates tight coupling and is unsafe

**File:** `ProfileFragment.java`
**Line:** 28

```java
ProfileActivity activity;
```

The field is package-private (no access modifier), set by a runtime `instanceof` cast in `onActivityCreated` (line 42–43), and then used directly in `onClick` (lines 164, 167) without any null guard:

```java
case R.id.my_resume:
    activity.showFragmentWithStack(...);   // NPE if activity is null
case R.id.my_equipments:
    activity.showFragmentWithStack(...);   // NPE if activity is null
```

If the fragment is ever hosted by an activity that is not a `ProfileActivity` the field remains `null` and both click handlers throw a `NullPointerException`. Beyond the crash risk, exposing the concrete `ProfileActivity` type as a package-private field leaks the activity's implementation details into the fragment — the fragment should communicate upward via an interface or via `getActivity()` with a guard.

**Classification:** HIGH (leaky abstraction + NPE risk)

---

### A64-3 — MEDIUM: `saveModifiedResult` constructs `ServerDateFormatter` as a new instance on every save call

**File:** `ProfileFragment.java`
**Line:** 118

```java
new ServerDateFormatter().formatDate(user.getComplianceDate())
```

`ServerDateFormatter` creates two `SimpleDateFormat` instances and sets timezone in its constructor every time. This is called on every save, which creates unnecessary allocations. The formatter should be a field or a static utility method. This is a minor performance/style issue, but it is inconsistent with how the formatter is used elsewhere (e.g., `CurrentUser.java` line 59 creates it once per `createUser` call, making it clear there is no shared convention).

**Classification:** MEDIUM (style inconsistency / unnecessary allocation)

---

### A64-4 — HIGH: `onData` in `SavedReportFragment` calls `listData.addAll(resultArray.arrayList)` without null guard

**File:** `SavedReportFragment.java`
**Lines:** 65–69

```java
private void onData(ReportResultArray resultArray) {
    listData.clear();
    listData.addAll(resultArray.arrayList);   // NPE if arrayList is null
    listAdapter.notifyDataSetChanged();
}
```

The `onSucceed` callback (line 52) checks `result.arrayList == null` *after* calling `onData(result)` (line 51). `onData` therefore runs before the null check, and if `resultArray.arrayList` is null, `listData.addAll(null)` throws a `NullPointerException`. The check and the data population are in the wrong order; the data call must also guard against null internally.

**Classification:** HIGH (crash / NPE)

---

### A64-5 — MEDIUM: `onResend` is package-private, coupling adapter to fragment internals

**File:** `SavedReportFragment.java` (line 71) and `SavedReportListAdapter.java` (line 52)

```java
// SavedReportFragment.java
void onResend(ReportItem reportItem) { ... }

// SavedReportListAdapter.java
SavedReportFragment savedReportFragment;   // package-private field, line 20
...
savedReportFragment.onResend(recordItem);  // line 52
```

The adapter holds a direct reference to `SavedReportFragment` via a package-private field set by the fragment after construction (`listAdapter.savedReportFragment = this`, `SavedReportFragment.java` line 40). This is a leaky abstraction: the adapter is tightly coupled to its one consumer fragment type. The standard Android pattern is to pass a callback interface (e.g., `OnResendListener`) to the adapter constructor, breaking the reverse dependency. Currently any other fragment or test cannot use this adapter without providing a `SavedReportFragment` instance.

**Classification:** MEDIUM (leaky abstraction / tight coupling)

---

### A64-6 — LOW: `SavedReportListAdapter` constructor is package-private but `savedReportFragment` field is assigned externally

**File:** `SavedReportListAdapter.java`
**Lines:** 20, 22

```java
SavedReportFragment savedReportFragment;   // package-private

SavedReportListAdapter(Context context, ArrayList<ReportItem> data) { ... }
```

The constructor is package-private (no modifier), preventing use outside the `ui.fragment` package, which is reasonable. However, the mandatory `savedReportFragment` dependency is not injected through the constructor — it is set as a public field after construction. This means the object can exist in an incomplete state between construction and field assignment, requiring the null check on line 51. Injecting via constructor would eliminate the null check and make the dependency explicit.

**Classification:** LOW (style — constructor should inject required dependencies)

---

### A64-7 — LOW: `context` field in `SavedReportListAdapter` is redundant

**File:** `SavedReportListAdapter.java`
**Lines:** 18, 24, 34

```java
private Context context;
...
this.context = context;
...
LayoutInflater inflater = ((Activity) context).getLayoutInflater();
```

`ArrayAdapter` already holds and exposes its `Context` via `getContext()`. Storing a separate `context` field duplicates the reference and risks inconsistency. The cast `(Activity) context` on line 34 will throw a `ClassCastException` if a non-`Activity` context (e.g., `ApplicationContext`) is ever passed; using `LayoutInflater.from(context)` or `parent.getContext()` is the conventional safe pattern for adapter inflation.

**Classification:** LOW (redundant field + latent ClassCastException risk)

---

### A64-8 — MEDIUM: `mData` field in `SavedReportListAdapter` is redundant and bypasses `ArrayAdapter` internals

**File:** `SavedReportListAdapter.java`
**Lines:** 19, 25, 62–68

```java
private ArrayList<ReportItem> mData;
...
this.mData = data;
...
@Override
public int getCount() {
    return mData.size();
}

@Override
public ReportItem getItem(int i) {
    return mData.get(i);
}
```

`ArrayAdapter` already manages its own internal list. The class overrides `getCount()` and `getItem()` to use the local `mData` field, bypassing `ArrayAdapter`'s own storage. This creates two parallel references to the same list object. When `notifyDataSetChanged()` is called after `listData.clear()` / `addAll()` on the owning side, both references see the same mutations only because they point to the same object. Any future code that uses `ArrayAdapter.add()`, `ArrayAdapter.insert()`, or `ArrayAdapter.remove()` will diverge from `mData` silently. Either extend `BaseAdapter` directly or rely solely on `ArrayAdapter`'s list management.

**Classification:** MEDIUM (leaky abstraction / shadow state)

---

### A64-9 — LOW: Deprecated `android.support.*` imports across all three files (pre-AndroidX)

**Files:** All three files
**Lines:** ProfileFragment.java 4–5; SavedReportFragment.java 4–5; SavedReportListAdapter.java 5

```java
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
```

The `android.support.*` namespace has been superseded by `androidx.*` since 2018. The project has not migrated to AndroidX. While this is a project-wide issue (confirmed by `build.gradle` using `com.android.support:appcompat-v7:26.0.2`), these files contribute to the technical debt. Using support-library 26.0.2 against a compileSdkVersion that is likely 28+ causes build warnings about mismatched support library and compile SDK versions.

**Classification:** LOW (deprecated API / project-wide)

---

### A64-10 — MEDIUM: `onActivityCreated(Bundle)` is deprecated in AndroidX fragments; pattern used before deprecated method arrives

**File:** `ProfileFragment.java`
**Lines:** 40–44

```java
@Override
public void onActivityCreated(Bundle savedInstanceState) {
    super.onActivityCreated(savedInstanceState);
    if (getActivity() instanceof ProfileActivity)
        activity = (ProfileActivity) getActivity();
}
```

`onActivityCreated` was deprecated in AndroidX Fragment 1.3.0. Even in the current support library, resolving the activity via `getActivity()` in `onActivityCreated` rather than storing it in `onAttach` (where the host activity is guaranteed) is fragile: `getActivity()` can theoretically return `null` here if the fragment is detached, and the `instanceof` check silently leaves `activity` null for non-`ProfileActivity` hosts rather than failing fast. The conventional correct hook is `onAttach(Activity)` / `onAttach(Context)`.

**Classification:** MEDIUM (deprecated lifecycle hook + fragile null handling)

---

### A64-11 — LOW: Trailing blank lines in SavedReportFragment.java

**File:** `SavedReportFragment.java`
**Lines:** 93–97

Four blank lines follow the closing brace of the class. This is cosmetic but indicates the file was not cleaned up after generation or editing.

**Classification:** LOW (style)

---

### A64-12 — INFO: `UpdateUserParameter` public fields use `snake_case` naming

**File:** `ProfileFragment.java` (line 129); `UpdateUserParameter.java` (lines 8–11)

```java
// UpdateUserParameter.java
public int id;
public String first_name;
public String last_name;
public String compliance_date;

// ProfileFragment.java line 129
CurrentUser.get().updateInformation(parameter.first_name, parameter.last_name, parameter.compliance_date);
```

Java naming conventions dictate `camelCase` for fields. The `snake_case` naming appears intentional to match the server JSON field names for serialization, but this means Java code directly accesses these fields using `snake_case`, which is inconsistent with all other Java field naming in the project. A `@SerializedName` annotation with a `camelCase` Java field name would be the conventional fix.

**Classification:** INFO (naming convention inconsistency — likely intentional for JSON mapping)

---

## Summary Table

| ID | Severity | File(s) | Description |
|----|----------|---------|-------------|
| A64-1 | MEDIUM | ProfileFragment | Five empty lifecycle overrides — dead scaffolding |
| A64-2 | HIGH | ProfileFragment | Package-private `activity` field with no null guard — NPE + leaky abstraction |
| A64-3 | MEDIUM | ProfileFragment | `ServerDateFormatter` instantiated per save call — unnecessary allocation |
| A64-4 | HIGH | SavedReportFragment | `onData` calls `addAll` before null check on `arrayList` — NPE |
| A64-5 | MEDIUM | SavedReportFragment + Adapter | `onResend` package-private; adapter holds direct fragment reference — tight coupling |
| A64-6 | LOW | SavedReportListAdapter | Required `savedReportFragment` dependency not injected via constructor |
| A64-7 | LOW | SavedReportListAdapter | Redundant `context` field; unsafe `(Activity)` cast |
| A64-8 | MEDIUM | SavedReportListAdapter | Shadow `mData` list bypasses `ArrayAdapter` internals |
| A64-9 | LOW | All three files | Deprecated `android.support.*` imports; support-lib 26.0.2 |
| A64-10 | MEDIUM | ProfileFragment | `onActivityCreated` deprecated; `getActivity()` can return null |
| A64-11 | LOW | SavedReportFragment | Four trailing blank lines after class closing brace |
| A64-12 | INFO | ProfileFragment / UpdateUserParameter | `snake_case` public fields on DTO accessed directly from Java |
