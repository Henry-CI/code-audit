# Pass 4 – Code Quality Audit
**Agent:** A63
**Audit run:** 2026-02-26-01
**Date executed:** 2026-02-27
**Files assigned:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/IncidentPart2Fragment.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/JobsFragment.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/LoginFragment.java`

---

## Step 1: Reading Evidence

### File 1 — IncidentPart2Fragment.java

**Class:** `IncidentPart2Fragment extends FleetFragment`
**Package:** `au.com.collectiveintelligence.fleetiq360.ui.fragment`
**Total lines:** 278

**Fields (all private unless noted):**
| Field | Type | Line |
|---|---|---|
| `location` | `EditText` | 28 |
| `injury` | `ToggleImageButton` | 29 |
| `injury_type` | `TextView` | 30 |
| `witness` | `EditText` | 31 |
| `injury_photo` | `ImageView` | 32 |
| `signature_image` | `ImageView` | 33 |
| `incidentActivity` | `IncidentActivity` | 34 |

**Methods:**
| Method | Visibility | Line |
|---|---|---|
| `onCreateView(LayoutInflater, ViewGroup, Bundle)` | `@Override public` | 38 |
| `initViews()` | `public` | 43 |
| `initValues()` | `private` | 91 |
| `choosePhoto()` | `private` | 101 |
| `updateSignature()` | `private` | 126 |
| `updatePhoto()` | `private` | 136 |
| `onRightButton(View)` | `@Override public` | 147 |
| `setParameter()` | `private` | 188 |
| `uploadImages(int)` | `private` | 197 |
| `uploadSignature(int)` | `private` | 215 |
| `close()` | `private` | 239 |
| `showInjuryTypeDialog()` | `private` | 243 |
| `onMiddleButton(View)` | `@Override public` | 260 |
| `setInjuryType(String)` | `private` | 270 |

**Types / constants / enums defined:** None

**Notable anonymous inner classes:**
- `View.OnClickListener` at lines 58–63 (injury_photo_button)
- `View.OnClickListener` at lines 65–79 (signature_button), containing `SignatureDialog.SignatureCallback`
- `View.OnClickListener` at lines 81–86 (injury_type)
- `Runnable` at line 103 (file permission), nested `Runnable` at line 107 (camera permission), nested `AndroidImagePicker.OnImagePickCompleteListener` at line 111
- `WebListener<SaveImpactResult>` at line 171
- `ImagePostBackgroundTask.ImageUploadCallBack` at line 200 (uploadImages)
- `ImagePostBackgroundTask.ImageUploadCallBack` at line 218 (uploadSignature)
- `Runnable` at line 224 (runLater)
- `ThemedSingleListDialog.Callback<String>` at line 248

---

### File 2 — JobsFragment.java

**Class:** `JobsFragment extends FleetFragment implements AbsRecyclerAdapter.OnItemClickListener, View.OnClickListener`
**Package:** `au.com.collectiveintelligence.fleetiq360.ui.fragment`
**Total lines:** 177

**Fields:**
| Field | Type | Visibility | Line |
|---|---|---|---|
| `activity` | `JobsActivity` | package-private | 44 |
| `timerText` | `TextView` | `public` | 45 |
| `textViewSecondText` | `TextView` | `public` | 45 |
| `finishBtn` | `ImageView` | `private` | 46 |
| `presenter` | `JobsPresenter` | `public` | 47 |
| `companyDateFormatter` | `CompanyDateFormatter` | `private` | 48 |
| `serverDateFormatter` | `ServerDateFormatter` | `private` | 49 |

**Methods:**
| Method | Visibility | Line |
|---|---|---|
| `onCreateView(LayoutInflater, ViewGroup, Bundle)` | `@Override public` | 53 |
| `onActivityCreated(Bundle)` | `@Override public` | 59 |
| `setDriverInfoHeader()` | `private` | 65 |
| `logout()` | `public` | 78 |
| `initViews()` | `public` | 113 |
| `setInfo()` | `private` | 140 |
| `onSessionSaved()` | `public` | 150 |
| `onItemClick(View, int)` | `@Override public` | 155 |
| `onClick(View)` | `@Override public` | 159 |
| `onSessionEnded()` | `@Override public` | 172 |

**Types / constants / enums defined:** None

**Notable anonymous inner classes:**
- `WebListener<SessionEndResult>` at line 85 (inside `logout()`)

---

### File 3 — LoginFragment.java

**Class:** `LoginFragment extends FleetFragment implements View.OnClickListener`
**Package:** `au.com.collectiveintelligence.fleetiq360.ui.fragment`
**Total lines:** 110

**Fields:**
| Field | Type | Visibility | Line |
|---|---|---|---|
| `nameText` | `EditText` | `private` | 29 |
| `passwordText` | `EditText` | `private` | 29 |

**Methods:**
| Method | Visibility | Line |
|---|---|---|
| `onCreateView(LayoutInflater, ViewGroup, Bundle)` | `@Override public` | 33 |
| `initViews()` | `public` | 38 |
| `login()` | `private` | 67 |
| `onStop()` | `@Override public` | 79 |
| `onDestroy()` | `@Override public` | 84 |
| `onClick(View)` | `@Override public` | 89 |

**Types / constants / enums defined:** None

**Notable anonymous inner classes:**
- `TextView.OnEditorActionListener` at line 57 (passwordText IME action)
- `ThemedSingleListDialog.Callback<String>` at line 100 (user-selection dialog)

---

## Step 2 & 3: Findings

---

### A63-1 — HIGH — Unused imports in JobsFragment (dead import code)

**File:** `JobsFragment.java`, lines 3–6

```java
import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Build;
```

None of `Manifest`, `PackageManager`, or `Build` are referenced anywhere in `JobsFragment.java`. The body of the class contains no permission checks, no SDK version guards, and no `Build.VERSION` comparisons. These imports were apparently left over from a prior implementation and will produce compiler/lint warnings about unused imports.

**Impact:** Build warnings; creates noise and false impressions that permission logic lives here.

---

### A63-2 — HIGH — Leaky abstraction: Fragment directly accesses public Activity fields

**File:** `IncidentPart2Fragment.java`, multiple locations (lines 73, 92–95, 115, 127, 137, 153, 158, 163–165, 174, 177, 189–194, 217, 244–245, 274–275)

`IncidentPart2Fragment` directly reads and writes nine public fields on `IncidentActivity` (`impactParameter`, `signaturePath`, `mCurrentPhotoPath`, `impactResult`, `injuryTypes`) and even mutates sub-fields of the parameter object (`impactParameter.injury_type`, `.location`, etc.) inline. `IncidentActivity` exposes all these as bare `public` fields with no accessor methods:

```java
// IncidentActivity.java
public ImpactParameter impactParameter;
public SaveImpactResult impactResult;
public String signaturePath = null;
public String mCurrentPhotoPath;
public String[] injuryTypes;
```

The fragment thus carries intimate knowledge of the activity's internal data model, bypasses any encapsulation, and makes both classes impossible to test or refactor independently. State mutation is scattered across the fragment rather than owned by the activity or a shared ViewModel.

**Impact:** Tight coupling; any rename or type change to these activity fields requires surgical edits across multiple fragment files. Violates the single-responsibility principle.

---

### A63-3 — HIGH — Leaky abstraction: Fragment directly accesses public Activity fields (JobsFragment)

**File:** `JobsFragment.java`, line 44 and used throughout

```java
JobsActivity activity;   // package-private — no explicit modifier
```

`activity` is stored as a package-private field (no `private` modifier) set by a direct cast at line 62. `presenter` and `timerText`/`textViewSecondText` are all `public`, exposing fragment internals to any class in the same package. The `logout()` method (line 78) is public but is not part of any interface — it is a mix of network logic, intent navigation, and session management that belongs in a presenter or repository, not in a UI fragment.

**Impact:** High coupling; the fragment owns business logic that should be encapsulated in the presenter layer.

---

### A63-4 — MEDIUM — Deprecated lifecycle callback: `onActivityCreated` used without justification

**File:** `JobsFragment.java`, lines 59–63

```java
@Override
public void onActivityCreated(Bundle savedInstanceState) {
    super.onActivityCreated(savedInstanceState);
    if (getActivity() instanceof JobsActivity)
        activity = (JobsActivity) getActivity();
}
```

`Fragment.onActivityCreated()` was deprecated in API level 28 (Android P). The base class `FleetFragment` also overrides `onActivityCreated` (line 202 of `FleetFragment.java`) — the convention across the codebase, including `FleetFragment` itself, is to do view and data initialisation there. The deprecation applies to all 8 files in the project that still use it, but `JobsFragment` is among the assigned files. The activity reference lookup would be more appropriate in `onAttach(Context)` or `onViewCreated`.

**Impact:** Will produce deprecation warnings at compile time; may break on future API versions.

---

### A63-5 — MEDIUM — Style inconsistency: `onStop` and `onDestroy` are empty no-op overrides

**File:** `LoginFragment.java`, lines 79–86

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

Both lifecycle overrides contain only a `super` call and no fragment-specific logic. They are functionally identical to not overriding the methods at all. Across the wider fragment package, `DashboardFragment`, `SetUserPhotoFragment`, `SignupLoadingFragment`, and `SetupEmailFragment` have the same pattern. However, `LoginFragment` is the only one among the assigned files where no explanation (cleanup, cancellation, resource release) justifies the presence of these empty stubs.

**Impact:** Dead code; adds noise, increases maintenance burden, and may mislead readers into thinking cleanup is intentionally deferred.

---

### A63-6 — MEDIUM — Commented-out code left in production

**File:** `LoginFragment.java`, line 98

```java
//emails.add(0, "");
```

This single-line comment inside `onClick()` for the "other users" button was never removed. It suggests a UI behaviour (prepending a blank entry to the email list) that was considered and rejected, but the decision was not cleaned up.

**File:** `FleetFragment.java` (base class, encountered during cross-reference), lines 273–275:
```java
//permissionNotGranted = true;
//onLocationNotGranted();
```
(Not in an assigned file, recorded here for completeness since it was read.)

**Impact (LoginFragment):** Low functional risk but violates the "no commented-out code" convention; should be deleted or documented with a rationale comment if intentionally kept.

---

### A63-7 — MEDIUM — Unchecked null dereference on `getActivity()` result

**File:** `LoginFragment.java`, line 45

```java
InputMethodManager imm = (InputMethodManager)getActivity().getSystemService(Context.INPUT_METHOD_SERVICE);
imm.showSoftInput(passwordText, InputMethodManager.SHOW_IMPLICIT);
```

`getActivity()` can return `null` if the fragment is not attached to an activity (e.g., during configuration change or if `initViews()` is called at an unexpected time from `FleetFragment.onActivityCreated`). There is no null guard before either the `.getSystemService()` call or the subsequent `imm.showSoftInput()`. An `imm` null result from `getSystemService` is also unchecked. Contrast with `JobsFragment.java` line 61 which checks `if (getActivity() instanceof JobsActivity)` before casting.

**Impact:** Potential `NullPointerException` on fragment detach edge cases during login.

---

### A63-8 — MEDIUM — `ServerDateFormatter` instantiated per-call instead of reused

**File:** `IncidentPart2Fragment.java`, line 190
**File:** `JobsFragment.java`, line 84

```java
// IncidentPart2Fragment.java:190
incidentActivity.impactParameter.report_time = new ServerDateFormatter().formatDateTime(Calendar.getInstance().getTime());

// JobsFragment.java:84
parameter.finish_time = new ServerDateFormatter().formatDateTime(Calendar.getInstance().getTime());
```

`JobsFragment` already has a `private ServerDateFormatter serverDateFormatter` field (line 49) that is correctly initialised in `initViews()` (line 118). However, in `logout()` (line 84), a fresh `new ServerDateFormatter()` is constructed and immediately discarded — the existing field is not used. `IncidentPart2Fragment` also instantiates a throwaway `ServerDateFormatter` in `setParameter()` when it could maintain a field. This is inconsistent with how `JobsPresenter` and `IncidentFragment` handle the same formatter (they store one instance).

**Impact:** Minor unnecessary object allocation on each call; inconsistent pattern within the same class (`JobsFragment`).

---

### A63-9 — MEDIUM — `onItemClick` is an empty method body (dead interface implementation)

**File:** `JobsFragment.java`, lines 155–157

```java
@Override
public void onItemClick(View v, int position) {
}
```

`JobsFragment` implements `AbsRecyclerAdapter.OnItemClickListener` but provides no implementation. There are no list items in the Jobs screen that would trigger this callback based on the fragment layout and presenter usage. The interface is implemented solely because of the `implements` declaration on the class, without any list adapter being wired to this fragment. Either the interface implementation should be removed or the method should be documented as intentionally empty.

**Impact:** Dead code; confuses readers into thinking item-click handling is planned or missing.

---

### A63-10 — LOW — `injury = false` assigned twice in `IncidentActivity.onCreate`

**File:** `IncidentActivity.java` (encountered during cross-reference for A63-2), lines 27 and 30

```java
impactParameter.injury = false;   // line 27
injuryTypes = getResources().getStringArray(R.array.injury_type);
impactParameter.injury_type = injuryTypes[0];
impactParameter.injury = false;   // line 30  ← duplicate
```

The same default initialisation is written twice with no intervening logic that could change the value. This is a copy-paste artefact; one line is redundant.

**Impact:** Dead code / copy-paste bug; confusing but not functionally incorrect since both assignments are identical.

---

### A63-11 — LOW — Style inconsistency: field naming convention mixes `snake_case` and `camelCase`

**File:** `IncidentPart2Fragment.java`, lines 28–33

```java
private EditText location;
private ToggleImageButton injury;
private TextView injury_type;      // snake_case
private EditText witness;
private ImageView injury_photo;    // snake_case
private ImageView signature_image; // snake_case
```

Android/Java convention for field names is `camelCase`. Three of the six view fields use `snake_case` (`injury_type`, `injury_photo`, `signature_image`), mirroring the server-side field names from `ImpactParameter`. The remaining fields in the same class (`location`, `injury`, `witness`, `incidentActivity`) use `camelCase`. This inconsistency propagates through method references throughout the file.

**Impact:** Cosmetic but measurable style debt; violates the Java naming convention and the project's own prevailing pattern.

---

### A63-12 — LOW — `switch` on `View.getId()` is deprecated in newer API targets

**File:** `JobsFragment.java`, lines 160–168

```java
@Override
public void onClick(View v) {
    switch (v.getId()) {
        case R.id.jobs_done_btn_id:
            ...
            break;
    }
}
```

Since API 26 (the project's `compileSdkVersion`), using `R.id.*` values as `case` constants in `switch` statements produces a lint warning because resource IDs are not guaranteed to be compile-time constants when using library modules. The preferred idiom is `if (v.getId() == R.id.jobs_done_btn_id)`. This is a minor build-warning issue at the current SDK level.

**Impact:** Lint warning; may become a compile error with strict resource ID configuration.

---

### A63-13 — INFO — `android.support.*` imports throughout all three files (pre-AndroidX)

**Files:** All three assigned files (lines 4–5 of each)

```java
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
```

The entire project uses the legacy `android.support` library namespace rather than `androidx`. The Support Library reached end-of-life in 2018; all new releases and bug fixes go through `androidx`. The project's `build.gradle` confirms support library v26.0.2 is in use (`com.android.support:appcompat-v7:26.0.2` etc.) — well behind the current stable AndroidX releases. This is a project-wide concern visible in all 45 files that import `android.support.*`.

**Impact:** The project cannot use any AndroidX-only API or library without migration. This is a significant technical debt item, noted here as INFO since it is architectural scope and not specific to these three files.

---

## Summary Table

| ID | Severity | File | Line(s) | Issue |
|---|---|---|---|---|
| A63-1 | HIGH | JobsFragment.java | 3–6 | Unused imports: `Manifest`, `PackageManager`, `Build` |
| A63-2 | HIGH | IncidentPart2Fragment.java | Multiple | Fragment directly reads/writes public Activity fields (leaky abstraction) |
| A63-3 | HIGH | JobsFragment.java | 44, 45, 47, 78+ | Public/package-private fields; business logic in fragment (leaky abstraction) |
| A63-4 | MEDIUM | JobsFragment.java | 59–63 | Deprecated `onActivityCreated` lifecycle callback |
| A63-5 | MEDIUM | LoginFragment.java | 79–86 | Empty `onStop`/`onDestroy` overrides (dead code) |
| A63-6 | MEDIUM | LoginFragment.java | 98 | Commented-out code: `//emails.add(0, "")` |
| A63-7 | MEDIUM | LoginFragment.java | 45–46 | Unchecked `getActivity()` null dereference |
| A63-8 | MEDIUM | IncidentPart2Fragment.java / JobsFragment.java | 190 / 84 | `ServerDateFormatter` instantiated per-call instead of reusing field |
| A63-9 | MEDIUM | JobsFragment.java | 155–157 | Empty `onItemClick` implementation (dead interface method) |
| A63-10 | LOW | IncidentActivity.java (cross-ref) | 27, 30 | `injury = false` assigned twice with no intervening logic |
| A63-11 | LOW | IncidentPart2Fragment.java | 28–33 | Field names mix `snake_case` and `camelCase` |
| A63-12 | LOW | JobsFragment.java | 160 | `switch(v.getId())` deprecated pattern |
| A63-13 | INFO | All three files | — | Legacy `android.support.*` instead of AndroidX (project-wide) |
