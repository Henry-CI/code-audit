# Pass 4 – Code Quality Audit
**Audit run:** 2026-02-26-01
**Agent:** A01
**Date written:** 2026-02-27
**Files reviewed:**
1. `LibCommon/src/main/java/com/yy/libcommon/BaseActivity.java`
2. `LibCommon/src/main/java/com/yy/libcommon/BaseController.java`
3. `LibCommon/src/main/java/com/yy/libcommon/BaseDialog.java`

---

## Section 1 – Reading Evidence

### 1.1 BaseActivity.java

**Class:** `BaseActivity` (extends `AppCompatActivity`, implements `BaseController`, `FragmentInterface.FragmentHandle`)

**Fields:**
| Line | Visibility | Name | Type |
|------|-----------|------|------|
| 30 | private static final | TAG | String |
| 31 | private | mFragment | Fragment |
| 32 | private | manager | FragmentManager |
| 33 | protected | isStarted | boolean |
| 34 | protected | isResumed | boolean |
| 37 | protected | mCustomProgressDialog | CustomProgressDialog |
| 38 | protected | subFragPermission | SubFragPermission |

**Methods (exhaustive):**
| Line | Signature |
|------|-----------|
| 40 | `public int getScreenWidth()` |
| 48 | `public void backToHome()` |
| 56 | `@Override public void onBackPressed()` |
| 75 | `@Override public void addFragment(@IdRes int containerViewId, Fragment fragment, String tag)` |
| 83 | `public void addFragment(@IdRes int containerViewId, Fragment fragment, String tag, boolean addStack)` |
| 95 | `@Override public void hideFragment(String tag)` |
| 101 | `public void removeFragment(String tag)` |
| 107 | `public Fragment findFramentByTag(String tag)` |
| 113 | `@Override public Fragment showFragment(@IdRes int containerViewId, String tag, String className)` |
| 134 | `public Fragment showFragmentWithoutStack(@IdRes int containerViewId, String tag, Fragment fragment)` |
| 149 | `public Fragment showFragmentWithStack(@IdRes int containerViewId, String tag, Fragment fragment)` |
| 164 | `public void addFragmentWithAnimation(@AnimRes int enter, @AnimRes int exit, @AnimRes int popEnter, @AnimRes int popExit, @IdRes int containerViewId, Fragment fragment, String tag, boolean addStack)` |
| 180 | `@Override public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults)` |
| 186 | `public void showDialog(String title, String msg)` |
| 196 | `protected void initKeyboard()` |
| 202 | `void showKeyboard(final View view)` |
| 213 | `@Override public boolean onCreateOptionsMenu(Menu menu)` |
| 218 | `@Override public boolean onOptionsItemSelected(MenuItem item)` |
| 229 | `@Override protected void onSaveInstanceState(Bundle outState)` |
| 233 | `void onRecover(Bundle savedInstanceState)` |
| 238 | `@Override protected void onCreate(Bundle savedInstanceState)` |
| 254 | `public void hideKeyboard(View view)` |
| 260 | `@Override protected void onStart()` |
| 267 | `@Override protected void onResume()` |
| 275 | `@Override protected void onPause()` |
| 281 | `@Override protected void onStop()` |
| 287 | `@Override protected void onDestroy()` |
| 292 | `public void runLater(final Runnable runnable, long delayMillis)` |
| 306 | `public void setBestOrientation()` |
| 323 | `public SubFragPermission getSubFragPermission()` |
| 328 | `@Override public FragmentManager getCurrentFragmentManager()` |
| 332 | `public void showToast(String msg)` |
| 338 | `public void showDialog(String title, String msg, ErrorDialog.OnErrorCallback callback)` |
| 351 | `protected void showProgressDialog()` |
| 359 | `public void showProgress(String title, String message)` |
| 367 | `public void showSavingProgress()` |
| 375 | `public void showDeletingProgress()` |
| 384 | `public void showLoadingProgress()` |
| 393 | `public void updateProgress(String message)` |
| 399 | `public void hideProgress()` |

**Types/constants defined in this file:** None beyond the class itself.

---

### 1.2 BaseController.java

**Type:** `interface BaseController`

**Author comment:** Created by steveyang on 30/11/16.

**Methods declared:**
| Line | Signature |
|------|-----------|
| 11 | `FragmentManager getCurrentFragmentManager()` |
| 12 | `boolean isDestroyed()` |
| 14 | `SubFragPermission getSubFragPermission()` |

**Commented-out method declarations (lines 16-23):**
```
// void showProgress(String title,String message);
// void updateProgress(String message);
// void hideProgress();
// void showToast(String msg);
// boolean checkCameraPermissionWithRun(Runnable runnable);
// boolean checkFilePermissionWithRun(Runnable runnable);
// void requestCameraPermission();
// void requestFilePermission();
```

---

### 1.3 BaseDialog.java

**Class:** `BaseDialog` (extends `DialogFragment`, implements `BaseController`)

**Author comment:** Created by michael.carr on 18/12/2014.

**Fields:**
| Line | Visibility | Name | Type |
|------|-----------|------|------|
| 26 | protected | mRootView | ViewGroup |
| 27 | public | mGenericCallback | IDialogGenericCallback |
| 28 | public | isDestroyed | boolean |
| 30 | protected | subFragPermission | SubFragPermission |

**Methods (exhaustive):**
| Line | Signature |
|------|-----------|
| 32 | `public int getScreenWidth()` |
| 39 | `public void showProgress(String title, String message)` |
| 45 | `public void showSavingProgress()` |
| 51 | `public void showDeletingProgress()` |
| 57 | `public void showLoadingProgress()` |
| 63 | `public void updateProgress(String message)` |
| 68 | `public void hideProgress()` |
| 74 | `public BaseActivity getBaseActivity()` |
| 80 | `@Override public void onDismiss(DialogInterface dialog)` |
| 88 | `public void showToast(String msg)` |
| 97 | `@Override public void onSaveInstanceState(Bundle outState)` |
| 102 | `@Override public void onActivityCreated(Bundle savedInstanceState)` |
| 112 | `@Override public void onDestroy()` |
| 121 | `@Override public void onDetach()` |
| 125 | `protected void setupViews()` |
| 130 | `@Override public void onPause()` |
| 135 | `@Override public void onResume()` |
| 141 | `@Override public void onStart()` |
| 146 | `@Override public void onStop()` |
| 153 | `public SubFragPermission getSubFragPermission()` |
| 159 | `@Override public boolean isDestroyed()` |
| 164 | `@Override public FragmentManager getCurrentFragmentManager()` |
| 168 | `public void hideKeyboard(View view)` |
| 174 | `public static void addFragment(FragmentManager fragmentManager, Fragment fragment, int container)` |
| 178 | `public static void addFragment(FragmentManager fragmentManager, Fragment fragment, int container, boolean backStack)` |
| 189 | `public static void removeFragment(FragmentManager fragmentManager, int container)` |
| 196 | `public void addFragment(Fragment fragment, int container)` |
| 201 | `public void addFragment(Fragment fragment, int container, boolean backStack)` |
| 211 | `public void removeSelfFromParent()` |

**Types/constants defined in this file:** None beyond the class itself.

---

## Section 2 – Findings

---

### A01-1 — CRITICAL: `onRequestPermissionsResult` crashes if `subFragPermission` is null

**File:** `BaseActivity.java`, line 182
**Category:** Dead-code / null-safety bug

```java
@Override
public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
    super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    subFragPermission.onRequestPermissionsResult(requestCode, permissions, grantResults);  // line 182
}
```

`subFragPermission` is assigned in `onCreate()` (line 245). Android may deliver `onRequestPermissionsResult` before `onCreate` completes in edge-case restart scenarios, and any subclass that calls `requestPermissions` before calling `super.onCreate()` will trigger a `NullPointerException`. No null-guard is applied here, unlike every other use of `subFragPermission` in the codebase (e.g., `onDestroy()` at line 289 explicitly checks for null in `BaseDialog`). This is an inconsistency that will crash the process.

---

### A01-2 — HIGH: Commented-out method declarations in `BaseController` interface leave the contract incomplete

**File:** `BaseController.java`, lines 16–23
**Category:** Commented-out code / leaky abstraction

```java
//    void showProgress(String title,String message);
//    void updateProgress(String message);
//    void hideProgress();
//    void showToast(String msg);
//    boolean checkCameraPermissionWithRun(Runnable runnable);
//    boolean checkFilePermissionWithRun(Runnable runnable);
//    void requestCameraPermission();
//    void requestFilePermission();
```

Eight methods that constitute the primary functional surface of the controller abstraction are commented out. Both `BaseActivity` and `BaseDialog` implement every one of these methods concretely (e.g., `showProgress`, `hideProgress`, `showToast`), but they are not enforced by the interface. Any code accepting a `BaseController` reference cannot call these methods without an unchecked downcast. The interface is effectively useless as a behavioral contract. Either these declarations must be restored or the interface redesigned.

---

### A01-3 — HIGH: `isDestroyed` field in `BaseDialog` shadows and conflicts with `Fragment.isDestroyed()`

**File:** `BaseDialog.java`, line 28 and line 159
**Category:** Style inconsistency / leaky abstraction / build warning

```java
public boolean isDestroyed = false;           // line 28 – public mutable field
...
@Override
public boolean isDestroyed() {               // line 159 – overrides Fragment method
    return isDestroyed;                      // returns the local field, not super
}
```

`Fragment` (and therefore `DialogFragment`) already has a `isDestroyed()` method managed by the framework lifecycle. Declaring a public `boolean isDestroyed` field with the same name, setting it manually in `onDestroy()`, creates three problems:

1. The field is `public` and mutable — any caller can write `dialog.isDestroyed = false` and re-open a destroyed dialog's progress paths.
2. The `@Override` annotation on `isDestroyed()` at line 159 is suppressing a name collision with the framework method rather than correctly delegating to it; the field will be `false` between construction and `onDestroy()` even if the fragment is in a detached-but-not-destroyed state.
3. `BaseController` declares `boolean isDestroyed()`. `BaseActivity` does **not** implement this method at all — it relies on the inherited `AppCompatActivity.isDestroyed()` from the Android framework. This means the two implementors of the same interface satisfy it by entirely different mechanisms, one via a custom field and one via the platform API.

---

### A01-4 — HIGH: `onBackPressed()` silently swallows commented-out exit-confirmation dialog; current behavior sends app to background unconditionally

**File:** `BaseActivity.java`, lines 57–71
**Category:** Commented-out code / dead code

```java
@Override
public void onBackPressed() {
//        new AlertDialog.Builder(this)
//                .setMessage("Are you sure you want to exit?")
//                .setPositiveButton("Yes", ...
//                .setNegativeButton("No", null)
//                .show();
    //super.onBackPressed();
    Intent setIntent = new Intent(Intent.ACTION_MAIN);
    setIntent.addCategory(Intent.CATEGORY_HOME);
    setIntent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
    startActivity(setIntent);
}
```

The exit-confirmation dialog has been completely commented out. `super.onBackPressed()` is also commented out. The replacement silently sends every Activity to the background (Home) regardless of context. This is a universal base class — every Activity in the app inherits this behavior. The commented code appears to represent an earlier design that was abandoned without removal, and the current implementation overrides back-press handling globally in a potentially undesirable way for child activities that need genuine back-stack navigation.

---

### A01-5 — HIGH: `setBestOrientation()` contains commented-out adaptive-orientation logic; hardcodes portrait unconditionally

**File:** `BaseActivity.java`, lines 306–319
**Category:** Commented-out code / dead code

```java
public void setBestOrientation() {
    setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
//        DisplayMetrics dm = getResources().getDisplayMetrics();
//        ...
//        if(screenInches >=7 ){
//            setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
//        }else {
//            setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
//        }
}
```

The tablet-landscape detection logic (roughly 12 lines) is commented out and replaced with an unconditional portrait lock. The method name (`setBestOrientation`) implies dynamic selection, which is misleading. If tablet landscape support is permanently dropped, the method should be inlined or renamed; if it is planned for reinstatement, the commented code should be tracked in version control history rather than left in source.

---

### A01-6 — MEDIUM: Inline comment on `mFragment` assignment is stale leftover artifact

**File:** `BaseActivity.java`, lines 77, 84, 167
**Category:** Commented-out code / style

```java
mFragment = fragment;//new TimerSetFragment();
```

This inline comment (`//new TimerSetFragment()`) appears at three separate call sites. It is a residue of a previous concrete class and has no informational value. It should be deleted.

---

### A01-7 — MEDIUM: Commented-out logging statement left in `showFragment`

**File:** `BaseActivity.java`, line 119
**Category:** Commented-out code

```java
//     Mylog.printf(TAG,"..............pFragment=null");
```

A debug log call referencing a class (`Mylog`) and using a string of dots as padding is left commented out inside a try block. It provides no informational value and should be deleted.

---

### A01-8 — MEDIUM: `subFragPermission.onDestroy()` called in both `onStop()` and `onDestroy()` in `BaseDialog`

**File:** `BaseDialog.java`, lines 148 and 115
**Category:** Style inconsistency / logic error

```java
@Override
public void onStop() {
    super.onStop();
    subFragPermission.onDestroy();   // line 148 — unregisters broadcast receiver
}

@Override
public void onDestroy() {
    super.onDestroy();
    if(subFragPermission != null){
        subFragPermission.onDestroy();  // line 115 — called again
    }
    isDestroyed = true;
}
```

`SubFragPermission.onDestroy()` calls `LocalBroadcastManager.unregisterReceiver()`. Calling it a second time in `onDestroy()` after it has already been called in `onStop()` results in a double-unregister. `LocalBroadcastManager` silently ignores a second unregister of the same receiver, but it means that `onResume()` (which re-registers via `onActive()`) is the only rebalancing point. If the dialog is stopped and re-started without being destroyed, `onStop` destroys the subscription and `onResume` re-creates it — which is correct — but `onDestroy` then fires a redundant teardown. Compare with `BaseActivity`, where `onDestroy` alone handles teardown (line 289), with no teardown in `onStop`. The two base classes are inconsistent in their lifecycle handling of the same object.

---

### A01-9 — MEDIUM: `showKeyboard()` has package-private visibility in a public base class

**File:** `BaseActivity.java`, line 202
**Category:** Style inconsistency / leaky abstraction

```java
void showKeyboard(final View view){    // package-private — no access modifier
```

All other utility methods in `BaseActivity` intended for subclass use are `public` or `protected`. `showKeyboard` is package-private (no modifier), which means subclasses in other packages (e.g., the main app module) cannot call it. Compare with `hideKeyboard()` at line 254 which is `public`. The asymmetry is almost certainly unintentional.

---

### A01-10 — MEDIUM: `onRecover()` and `onSaveInstanceState()` are empty hook stubs with no documentation

**File:** `BaseActivity.java`, lines 229–235
**Category:** Dead code / style

```java
@Override
protected void onSaveInstanceState(Bundle outState) {
    super.onSaveInstanceState(outState);
}

void onRecover(Bundle savedInstanceState){
    // empty body
}
```

`onSaveInstanceState` is overridden purely to call super — it adds no behavior and should be removed unless it is a documented extension point. `onRecover` is package-private, undocumented, and always empty; subclasses in other packages cannot override it. If these are intended lifecycle extension points for subclasses, they must be `protected` and documented; otherwise they are dead code.

---

### A01-11 — MEDIUM: `findFramentByTag` method name is a persistent typo in public API

**File:** `BaseActivity.java` line 107; `FragmentInterface.java` line 14
**Category:** Style inconsistency

```java
public Fragment findFramentByTag(String tag) {   // "Frament" — missing 'g'
```

The method name `findFramentByTag` (missing 'g' in "Fragment") is declared in `FragmentInterface.FragmentHandle` and implemented in `BaseActivity`. Because it is part of a public interface, renaming it requires coordinated changes across all callers in the codebase. The defect has been baked into the public contract.

---

### A01-12 — MEDIUM: `hideKeyboard()` in `BaseDialog` does not null-check `getContext()` result

**File:** `BaseDialog.java`, line 169–170
**Category:** Null-safety / style inconsistency

```java
public void hideKeyboard(View view){
    InputMethodManager imm = (InputMethodManager) getContext().getSystemService(Context.INPUT_METHOD_SERVICE);
    imm.hideSoftInputFromWindow(view.getWindowToken(), 0);
}
```

`getContext()` returns null when the fragment is not attached. The result is used immediately without a null check. Compare with `BaseActivity.hideKeyboard()` at line 254–256, which also lacks a null check on the `imm` result, but at least the Activity is guaranteed to have a context. `BaseDialog` is a fragment that can be detached, making this call crashable. Neither implementation guards against a null `imm` return, which can occur if the service is unavailable.

---

### A01-13 — LOW: Unused import `android.app.AlertDialog` in `BaseActivity`

**File:** `BaseActivity.java`, line 3
**Category:** Build warning / dead code

```java
import android.app.AlertDialog;
```

`AlertDialog` is not used anywhere in `BaseActivity.java`. It was presumably referenced by the commented-out exit-dialog code (lines 57–66) but was never removed when that code was commented out. Most build configurations will emit an "unused import" warning.

---

### A01-14 — LOW: Unused import `android.content.DialogInterface` in `BaseActivity`

**File:** `BaseActivity.java`, line 5
**Category:** Build warning / dead code

```java
import android.content.DialogInterface;
```

`DialogInterface` is referenced only inside the commented-out block at lines 59–64. It is not used in any active code and will generate an "unused import" build warning.

---

### A01-15 — LOW: `FragmentManager manager` is a mutable instance field used only as a local variable

**File:** `BaseActivity.java`, line 32
**Category:** Style inconsistency / design smell

```java
private FragmentManager manager;
```

This field is never read across method calls — every method that uses it reassigns it immediately via `manager = getSupportFragmentManager()` before use. It functions purely as a local variable stored as an instance field, wasting heap space and creating a false impression that state is preserved between calls. It should be a local variable inside each method.

---

### A01-16 — LOW: `mRootView` declared in `BaseDialog` but never assigned or used within the class

**File:** `BaseDialog.java`, line 26
**Category:** Dead code / unused field

```java
protected ViewGroup mRootView;
```

`mRootView` is never assigned or read in `BaseDialog.java`. It exists solely as a convention for subclasses to use. If it is a subclass convention, it should be documented; if it is unused everywhere, it should be removed.

---

### A01-17 — LOW: `onDetach()` and `onPause()` overrides in `BaseDialog` are empty pass-throughs

**File:** `BaseDialog.java`, lines 121–123 and 130–132
**Category:** Dead code

```java
@Override
public void onDetach() {
    super.onDetach();
}

@Override
public void onPause() {
    super.onPause();
}
```

Both overrides call only `super` and add no behavior. They are dead code and should be removed unless they are intentional extension markers — in which case they need `protected` visibility, documentation, and a body comment explaining the intent.

---

### A01-18 — LOW: `onStart()` override in `BaseDialog` is an empty pass-through

**File:** `BaseDialog.java`, lines 141–143
**Category:** Dead code

```java
@Override
public void onStart() {
    super.onStart();
}
```

Same as A01-17 — adds no behavior.

---

### A01-19 — INFO: `android.support.*` imports throughout — project uses legacy Support Library, not AndroidX

**Files:** All three files
**Category:** Build warning / deprecated API

All imports reference `android.support.v4`, `android.support.v7`, and `android.support.annotation`. The Android Support Library was superseded by AndroidX in 2018 and is no longer receiving new feature development. The project has not migrated. While not a compile error, any new dependencies that require AndroidX will conflict, and Google Play may flag the app for using deprecated APIs in future policy updates.

---

## Section 3 – Summary Table

| ID | Severity | File | Line(s) | Issue |
|----|----------|------|---------|-------|
| A01-1 | CRITICAL | BaseActivity.java | 182 | `subFragPermission` used without null check in `onRequestPermissionsResult` |
| A01-2 | HIGH | BaseController.java | 16–23 | Eight interface methods commented out, making the contract nearly empty |
| A01-3 | HIGH | BaseDialog.java | 28, 159 | Public mutable `isDestroyed` field shadows framework method; `BaseActivity` uses different mechanism for same interface |
| A01-4 | HIGH | BaseActivity.java | 57–71 | Exit-confirmation dialog and `super.onBackPressed()` commented out; back press unconditionally minimizes app |
| A01-5 | HIGH | BaseActivity.java | 306–319 | Adaptive orientation logic commented out; method name misleading |
| A01-6 | MEDIUM | BaseActivity.java | 77, 84, 167 | Stale `//new TimerSetFragment()` inline comment at three sites |
| A01-7 | MEDIUM | BaseActivity.java | 119 | Commented-out debug log with `Mylog` reference and dot-padding string |
| A01-8 | MEDIUM | BaseDialog.java | 115, 148 | `subFragPermission.onDestroy()` called in both `onStop()` and `onDestroy()`; inconsistent with BaseActivity lifecycle handling |
| A01-9 | MEDIUM | BaseActivity.java | 202 | `showKeyboard()` is package-private; asymmetric with public `hideKeyboard()` |
| A01-10 | MEDIUM | BaseActivity.java | 229–235 | Empty `onSaveInstanceState` override and package-private `onRecover()` stub |
| A01-11 | MEDIUM | BaseActivity.java / FragmentInterface.java | 107 / 14 | Typo `findFramentByTag` baked into public interface |
| A01-12 | MEDIUM | BaseDialog.java | 169–170 | `getContext()` and `imm` not null-checked in `hideKeyboard()` |
| A01-13 | LOW | BaseActivity.java | 3 | Unused import `android.app.AlertDialog` |
| A01-14 | LOW | BaseActivity.java | 5 | Unused import `android.content.DialogInterface` |
| A01-15 | LOW | BaseActivity.java | 32 | `FragmentManager manager` instance field acts only as a local variable |
| A01-16 | LOW | BaseDialog.java | 26 | `mRootView` never assigned in `BaseDialog`; undocumented convention |
| A01-17 | LOW | BaseDialog.java | 121–123, 130–132 | `onDetach()` and `onPause()` are empty pass-through overrides |
| A01-18 | LOW | BaseDialog.java | 141–143 | `onStart()` is empty pass-through override |
| A01-19 | INFO | All three files | — | Project uses legacy `android.support.*` library; not migrated to AndroidX |
