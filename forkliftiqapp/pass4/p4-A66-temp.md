# Pass 4 Code Quality — Agent A66
**Audit run:** 2026-02-26-01
**Auditor:** A66
**Files reviewed:** 3

---

## Section 1: Reading Evidence

### File 1 — `ServiceStatsListAdapter.java`
**Full path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/ServiceStatsListAdapter.java`

**Class:** `ServiceStatsListAdapter` (extends `ArrayAdapter<DriverStatsItem>`)

**Methods (exhaustive):**

| Method | Line |
|--------|------|
| `ServiceStatsListAdapter(Context, ArrayList<DriverStatsItem>)` (constructor) | 23 |
| `getView(int, View, ViewGroup)` | 31 |
| `getCount()` | 67 |
| `getItem(int)` | 72 |

**Inner types:**
- `static class ListHolder` (lines 76–80): fields `TextView name`, `View status_bar`, `TextView status_text`

**Constants / enums / interfaces defined:** none

---

### File 2 — `SetUserPhotoFragment.java`
**Full path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/SetUserPhotoFragment.java`

**Class:** `SetUserPhotoFragment` (extends `FleetFragment`, implements `View.OnClickListener`)

**Methods (exhaustive):**

| Method | Line |
|--------|------|
| `onCreateView(LayoutInflater, ViewGroup, Bundle)` | 31 |
| `onActivityCreated(Bundle)` | 37 |
| `initViews()` | 45 |
| `getUserDetail()` | 98 |
| `onPhotoSaved()` | 102 |
| `uploadUserPhoto()` | 115 |
| `choosePhoto()` | 148 |
| `onResume()` | 180 |
| `onStop()` | 185 |
| `onDestroy()` | 190 |
| `onClick(View)` | 195 |

**Fields:**
- `Activity activity` (package-private, line 24)
- `Bitmap mBitmap` (private, line 25)
- `ImageView user_photo` (private, line 26)
- `ImageView user_photo_none` (private, line 27)
- `boolean fromDashboard` (package-private, line 28)

**Constants / enums / interfaces defined:** none

---

### File 3 — `SetupEmailFragment.java`
**Full path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/SetupEmailFragment.java`

**Class:** `SetupEmailFragment` (extends `FleetFragment`, implements `View.OnClickListener`)

**Methods (exhaustive):**

| Method | Line |
|--------|------|
| `createInstance(boolean)` (static factory) | 35 |
| `onCreateView(LayoutInflater, ViewGroup, Bundle)` | 42 |
| `onActivityCreated(Bundle)` | 49 |
| `initViews()` | 57 |
| `loadData()` | 93 |
| `onEmailLoaded()` | 112 |
| `saveEmail()` | 124 |
| `onSaved()` | 195 |
| `onResume()` | 207 |
| `onStop()` | 212 |
| `onDestroy()` | 217 |
| `onClick(View)` | 222 |

**Fields:**
- `SignupActivity activity` (package-private, line 32)
- `boolean mFromDashboard` (private, line 33)
- `GetEmailResult getEmailResult` (private, line 91)

**Constants / enums / interfaces defined:** none

---

## Section 2: Findings

---

### A66-1 — MEDIUM — Deprecated `Integer.valueOf()` instead of `Integer.parseInt()`
**File:** `ServiceStatsListAdapter.java`, line 57

```java
v = Integer.valueOf(s);
```

`Integer.valueOf(String)` returns a boxed `Integer` object that is immediately unboxed into the primitive `int v`. The idiomatic and more efficient call is `Integer.parseInt(s)`, which returns a primitive directly. Android Lint and most static analysers flag this as a build warning. The exception type caught (`Exception`) is also overly broad; the relevant exception is `NumberFormatException`.

---

### A66-2 — MEDIUM — Dead field: `ListHolder.status_bar` is assigned but never read
**File:** `ServiceStatsListAdapter.java`, line 43 / 78

```java
holder.status_bar = row.findViewById(R.id.status_bar);
// ...
View status_bar;  // in ListHolder
```

`status_bar` is assigned in `getView()` (line 43) and declared in `ListHolder` (line 78), but it is never read anywhere. The corresponding `<View id="status_bar">` in the layout exists purely as a visual progress bar whose width is hardcoded in XML; the adapter never programmatically changes it based on the data. The field occupies memory in every `ListHolder` instance and misleads future maintainers into believing the bar is driven by data. Either the bar should be wired to the actual service count or the field and the `findViewById` call should be removed.

---

### A66-3 — HIGH — Hard-coded pluralisation: "Services" label ignores singular
**File:** `ServiceStatsListAdapter.java`, line 60

```java
String text = v + " Services";
```

The label is always "N Services", even when `v == 1`, producing grammatically incorrect output ("1 Services"). Android provides `getResources().getQuantityString()` (plurals) for exactly this purpose. The string is also built with string concatenation rather than a string resource, bypassing localisation infrastructure.

---

### A66-4 — HIGH — State stored directly on Fragment instance via factory method (survives rotation incorrectly)
**File:** `SetupEmailFragment.java`, lines 35–38

```java
public static SetupEmailFragment createInstance(boolean fromDashboard) {
    SetupEmailFragment fragment = new SetupEmailFragment();
    fragment.mFromDashboard = fromDashboard;
    return fragment;
}
```

`mFromDashboard` is set as a plain field instead of being placed into a `Bundle` argument via `setArguments()`. When the system recreates the Fragment after a configuration change (rotation, language switch), it calls the no-arg constructor and `mFromDashboard` reverts to `false`. This can silently change the fragment's behaviour (e.g., showing the signup flow instead of the dashboard save flow after rotation). The standard fix is to pack the boolean into `Bundle` via `setArguments()` and read it from `getArguments()` in `onActivityCreated`.

The same pattern is present in `SetUserPhotoFragment`: `fromDashboard` is a bare field (line 28) with no `setArguments`/`getArguments` mechanism visible in the file, making it equally vulnerable.

---

### A66-5 — HIGH — Package-private visibility on fields that should be private
**File:** `SetUserPhotoFragment.java`, lines 24, 28; `SetupEmailFragment.java`, line 32

```java
// SetUserPhotoFragment.java
Activity activity;          // line 24 — package-private
boolean fromDashboard = false; // line 28 — package-private

// SetupEmailFragment.java
SignupActivity activity;    // line 32 — package-private
```

These fields lack access modifiers and are therefore package-private. They are implementation details of the fragment and should be `private`. Other classes in the same package can read or mutate fragment state directly, a leaky abstraction that bypasses any encapsulation the fragment provides. The `activity` field in `SetupEmailFragment` is typed as the concrete `SignupActivity` rather than the base `Activity` or an interface, further increasing coupling.

---

### A66-6 — MEDIUM — Inconsistent null-safety style between the two fragments
**File:** `SetUserPhotoFragment.java` line 105 vs `SetupEmailFragment.java` lines 107, 197

`SetUserPhotoFragment` guards `activity` with a plain `if (activity != null)` check (line 105).
`SetupEmailFragment` uses `Objects.requireNonNull(getActivity()).finish()` (lines 107, 197), which throws a `NullPointerException` with no user-visible error handling if the activity is unexpectedly null.

The two patterns are semantically opposite: one silently does nothing on null; the other crashes. Neither approach is documented as intentional. A consistent strategy (e.g., always guard with `isAdded() && getActivity() != null`) should be applied uniformly.

---

### A66-7 — MEDIUM — Empty lifecycle overrides add noise without value
**Files:** `SetUserPhotoFragment.java` lines 180–196; `SetupEmailFragment.java` lines 207–223

Both fragments override `onResume()`, `onStop()`, `onDestroy()`, and `onClick()` with bodies that only call `super` (or are entirely empty for `onClick`). These overrides are dead code: they contribute nothing beyond what the base class already does. They inflate file length and mislead readers into expecting non-trivial teardown logic.

```java
// SetUserPhotoFragment.java
@Override
public void onResume() { super.onResume(); }   // no-op

@Override
public void onStop() { super.onStop(); }       // no-op

@Override
public void onDestroy() { super.onDestroy(); } // no-op

@Override
public void onClick(View view) { }             // declared by interface but entirely empty
```

The empty `onClick(View)` in particular raises a concern: the class declares `implements View.OnClickListener` but all click handling is done via anonymous inner classes. The interface implementation is therefore structural dead code.

---

### A66-8 — LOW — `@SuppressLint("SetTextI18n")` suppresses a real localisation defect
**File:** `SetupEmailFragment.java`, line 56

```java
@SuppressLint("SetTextI18n")
public void initViews() {
    ...
    nextBtn.setText("Save");
    ...
    nextBtn.setText("Next");
```

The annotation silences the lint warning rather than fixing it. "Save" and "Next" are hard-coded English strings that should be string resources (e.g., `R.string.save`, `R.string.next`). Suppressing the warning hides a genuine internationalisation gap. The warning in line 137 ("Warning!") and the toast strings throughout `SetupEmailFragment` are similarly hard-coded but outside the suppression scope.

---

### A66-9 — MEDIUM — Grammatically incorrect confirmation dialog message
**File:** `SetupEmailFragment.java`, line 137

```java
"No email confirmed. Are you you want sure to skip?",
```

The string "Are you you want sure to skip?" is clearly a word-order error ("Are you sure you want to skip?"). This is a user-visible defect surfaced from a string that is hard-coded rather than managed in a string resource (where a review step during translation would have caught it).

---

### A66-10 — MEDIUM — `ImagePostBackgroundTask.ImageUploadParam` constructed but never used
**File:** `SetUserPhotoFragment.java`, lines 127–129

```java
ImagePostBackgroundTask.ImageUploadParam param = new ImagePostBackgroundTask.ImageUploadParam();
param.url = urlItem.url;
param.bitmap = mBitmap;
```

The local variable `param` is populated and then never passed anywhere. The actual upload call two lines later passes `urlItem.url` and `mBitmap` directly:

```java
ImagePostBackgroundTask.uploadImage(urlItem.url, mBitmap, ...);
```

`param` is dead code. It also imports an internal DTO (`ImagePostBackgroundTask.ImageUploadParam`) into the Fragment's logic, leaking the internal structure of the background task into the UI layer unnecessarily.

---

### A66-11 — LOW — `onActivityCreated()` is deprecated in AndroidX
**Files:** `SetUserPhotoFragment.java` line 37; `SetupEmailFragment.java` line 49

```java
@Override
public void onActivityCreated(Bundle savedInstanceState) { ... }
```

`Fragment.onActivityCreated()` was deprecated in AndroidX Fragment 1.3.0 (and above, which the project targets via the support library migration path). The recommended replacement is to perform post-view setup in `onViewCreated()` or use a `LifecycleObserver`. This will generate deprecation build warnings when the project is migrated from the legacy `android.support` library to AndroidX.

---

### A66-12 — LOW — Hard-coded crop quality constant with no explanation
**File:** `SetUserPhotoFragment.java`, line 159

```java
AndroidImagePicker.getInstance().pickAndCrop(getActivity(), true, 120, ...);
```

The magic number `120` is passed as the crop/quality parameter with no named constant, no comment, and no documentation of its units or valid range. This makes it impossible to reason about the tradeoff being made (image quality vs. upload size) without consulting the third-party library source.

---

## Section 3: Summary Table

| ID | Severity | File | Line(s) | Issue |
|----|----------|------|---------|-------|
| A66-1 | MEDIUM | ServiceStatsListAdapter.java | 57 | `Integer.valueOf()` instead of `parseInt()`; overly broad `Exception` catch |
| A66-2 | MEDIUM | ServiceStatsListAdapter.java | 43, 78 | `status_bar` field assigned but never read — dead code |
| A66-3 | HIGH | ServiceStatsListAdapter.java | 60 | Hard-coded "Services" label — always plural, no string resource |
| A66-4 | HIGH | SetupEmailFragment.java / SetUserPhotoFragment.java | 35–38 / 28 | State stored as bare field; lost on configuration change |
| A66-5 | HIGH | SetUserPhotoFragment.java / SetupEmailFragment.java | 24, 28 / 32 | Package-private fields expose fragment internals; concrete-type coupling |
| A66-6 | MEDIUM | SetUserPhotoFragment.java / SetupEmailFragment.java | 105 / 107, 197 | Inconsistent null-safety: silent ignore vs. NPE crash |
| A66-7 | MEDIUM | SetUserPhotoFragment.java / SetupEmailFragment.java | 180–196 / 207–223 | Empty/no-op lifecycle overrides and empty `onClick` interface implementation |
| A66-8 | LOW | SetupEmailFragment.java | 56–64 | `@SuppressLint("SetTextI18n")` conceals hard-coded English strings |
| A66-9 | MEDIUM | SetupEmailFragment.java | 137 | User-visible grammatical error in confirmation dialog text |
| A66-10 | MEDIUM | SetUserPhotoFragment.java | 127–129 | `ImageUploadParam` object constructed and populated but never used |
| A66-11 | LOW | SetUserPhotoFragment.java / SetupEmailFragment.java | 37 / 49 | `onActivityCreated()` is deprecated in AndroidX |
| A66-12 | LOW | SetUserPhotoFragment.java | 159 | Magic number `120` passed as crop quality — no constant or comment |
