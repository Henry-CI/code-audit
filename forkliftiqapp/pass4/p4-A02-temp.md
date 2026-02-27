# Pass 4 – Code Quality Audit
**Agent:** A02
**Audit Run:** 2026-02-26-01
**Files Reviewed:**
1. `LibCommon/src/main/java/com/yy/libcommon/BaseFragment.java`
2. `LibCommon/src/main/java/com/yy/libcommon/BaseSubFragment.java`
3. `LibCommon/src/main/java/com/yy/libcommon/BaseThemedDialog.java`

---

## Step 1: Reading Evidence

### File 1: `BaseFragment.java`

**Class:** `BaseFragment extends Fragment implements BaseController`

**Constants / Fields:**
| Name | Type | Visibility | Line |
|---|---|---|---|
| `REQUEST_TAKE_PHOTO` | `int` (static final) | `public` | 33 |
| `sChildFragmentManagerField` | `Field` (static final) | `private` | 35 |
| `LOGTAG` | `String` (static final) | `private` | 36 |
| `mRootView` | `ViewGroup` | `protected` | 37 |
| `isDestroyed` | `boolean` | `public` | 38 |
| `takePictureIntent` | `Intent` | `private` | 40 |
| `tempPhotoFilePath` | `String` | `public` | 41 |
| `subFragPermission` | `SubFragPermission` | `public` | 42 |

**Methods:**
| Method | Line |
|---|---|
| `takePhoto()` | 45 |
| `getBaseActivity()` | 90 |
| `BaseFragment()` (constructor) | 94 |
| `getScreenWidth()` | 97 |
| `setSimpleSpinner(Spinner, int)` | 104 |
| `showErrDialog(String)` | 112 |
| `showToast(String)` | 116 |
| `showProgress(String, String)` | 124 |
| `showSavingProgress()` | 130 |
| `showDeletingProgress()` | 136 |
| `showLoadingProgress()` | 142 |
| `updateProgress(String)` | 148 |
| `hideProgress()` | 154 |
| `static initializer` | 160 |
| `onStart()` | 172 |
| `onActivityCreated(Bundle)` | 179 |
| `findViewById(int)` | 188 |
| `onDetach()` | 198 |
| `onDestroy()` | 212 |
| `onStop()` | 221 |
| `onResume()` | 227 |
| `onPause()` | 233 |
| `showDialog(Context, String, String)` | 237 |
| `showDialog(Context, String, String, boolean, ErrorDialog.OnErrorCallback)` | 249 |
| `showDialog(Context, String, String, ErrorDialog.OnErrorCallback)` | 263 |
| `getSubFragPermission()` | 276 |
| `isDestroyed()` | 281 |
| `getCurrentFragmentManager()` | 286 |
| `addFragment(FragmentManager, Fragment, int)` (static) | 292 |
| `addFragment(FragmentManager, Fragment, int, boolean)` (static) | 296 |
| `removeFragment(FragmentManager, int)` (static) | 305 |
| `addFragment(Fragment, int)` | 311 |
| `addFragment(Fragment, int, boolean)` | 315 |
| `removeSelfFromParent()` | 324 |

---

### File 2: `BaseSubFragment.java`

**Class:** `BaseSubFragment` (plain class, not a Fragment subclass)

**Fields:**
| Name | Type | Visibility | Line |
|---|---|---|---|
| `mRootView` | `ViewGroup` | `protected` | 13 |
| `mBaseController` | `BaseController` | `protected` | 14 |
| `mBaseActivity` | `BaseActivity` | `protected` | 15 |
| `isHidden` | `boolean` | `protected` | 16 |

**Methods:**
| Method | Line |
|---|---|
| `BaseSubFragment(BaseController, BaseActivity)` (constructor) | 18 |
| `onActive(View)` | 25 |
| `onActive()` | 30 |
| `isActive()` | 34 |
| `onHidden()` | 38 |
| `onDestroy()` | 43 |

---

### File 3: `BaseThemedDialog.java`

**Class:** `BaseThemedDialog extends BaseDialog`

**Constants / Fields:**
| Name | Type | Visibility | Line |
|---|---|---|---|
| `DIALOG_SHADOW_WIDTH` | `int` (static final) | `private` | 25 |
| `LOLLIPOP_DIALOG_SHADOW_WIDTH` | `int` (static final) | `private` | 26 |
| `VIBRATION_DURATION_MS` | `int` (static final) | `private` | 27 |
| `TITLE_BAR_HEIGHT` | `int` (static final) | `private` | 28 |
| `mLayoutView` | `ViewGroup` | `protected` | 30 |
| `layoutResource` | `int` | `protected` | 31 |
| `mMainLayout` | `RelativeLayout` | `protected` | 32 |
| `mRequests` | `ArrayList<String>` | `protected` | 33 |
| `mLayoutWidth` | `int` | `private` | 34 |
| `mVibrator` | `Vibrator` | `private` | 35 |
| `mVibrateButtons` | `ArrayList<View>` | `private` | 36 |
| `base_themed_dialog_right_text_view` | `TextView` | `public` | 37 |
| `base_themed_dialog_left_text_view` | `TextView` | `public` | 38 |
| `headerRightText` | `String` | `public` | 40 |
| `headerLeftText` | `String` | `public` | 41 |
| `base_themed_dialog_titleView` | `View` | `protected` | 43 |
| `mTitle` | `String` | `protected` | 44 |
| `isWideDialog` | `boolean` | `protected` | 46 |

**Methods:**
| Method | Line |
|---|---|
| `onLeftButton()` | 48 |
| `onRightButton()` | 52 |
| `setupViews()` | 57 |
| `onCreateView(LayoutInflater, ViewGroup, Bundle)` | 89 |
| `BaseThemedDialog()` (constructor) | 108 |
| `setLayout(int)` | 112 |
| `setTitleText(String)` | 116 |
| `inflateLayout(LayoutInflater)` | 122 |
| `onActivityCreated(Bundle)` | 156 |
| `setViewParams()` | 162 |
| `findViewById(int)` | 166 |
| `getCurrentWidth()` | 171 |
| `getCurrentHeight()` | 175 |
| `vibrateOnPress(View)` | 179 |
| `setLayoutClickable(View, boolean)` | 199 |
| `vibrate()` | 203 |
| `vibrate(int)` | 207 |
| `onPause()` | 212 |

---

## Step 2 & 3: Findings

---

### A02-1 — HIGH: Commented-out code block in `BaseFragment.java` (`takePhoto`, lines 77–80)

**File:** `BaseFragment.java`, lines 77–80

```java
//                            if(isResumed()){
                                subFragPermission.cameraPendingRunnable = null;
                                startActivityForResult(takePictureIntent, REQUEST_TAKE_PHOTO);
//                            }
```

A guard condition `if(isResumed())` has been commented out, along with its closing brace. The original intent was to prevent `startActivityForResult` from being called when the fragment is not resumed — a legitimate lifecycle safety check. Removing this guard can cause `startActivityForResult` to be invoked in an invalid state (e.g., after `onStop`), risking `IllegalStateException`. This is commented-out logic that disables a safety guard, not simply decorative dead code.

---

### A02-2 — HIGH: Duplicate initialisation block inside `inflateLayout` in `BaseThemedDialog.java` (lines 143–151)

**File:** `BaseThemedDialog.java`, lines 89–106 vs. lines 143–151

`onCreateView` (lines 89–106) already:
- Creates `mVibrator`
- Initialises `mVibrateButtons`
- Calls `getDialog().requestWindowFeature(Window.FEATURE_NO_TITLE)`
- Calls `getDialog().getWindow().setSoftInputMode(...)`
- Finds and assigns `base_themed_dialog_titleView`, `base_themed_dialog_right_text_view`, `base_themed_dialog_left_text_view`

`inflateLayout` (lines 143–151) unconditionally repeats all five of these operations after the `if (layoutResource > 0)` block, regardless of whether `layoutResource` is set. Because `onCreateView` calls `inflateLayout`, these assignments are executed twice in every normal flow. The double call to `requestWindowFeature` after `onCreateView` has already set up the window is wasteful; the double `getSystemService(VIBRATOR_SERVICE)` call silently replaces the first instance; and `mVibrateButtons` is reset to a new empty list, discarding any views added by subclass constructors between the two calls. This is dead initialisation that introduces subtle bugs.

---

### A02-3 — HIGH: Deprecated `Uri.fromFile` usage in `BaseFragment.java` (line 63)

**File:** `BaseFragment.java`, line 63

```java
takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, Uri.fromFile(photoFile));
```

`Uri.fromFile` is deprecated and blocked on Android 7.0+ (API 24+) when targeting apps that declare a `FileProvider`. On those API levels the OS throws a `FileUriExposedException` at runtime. The correct URI (`photoURI` from `FileProvider.getUriForFile`) is computed on line 70 and overrides `EXTRA_OUTPUT` on line 72, but the intervening line 63 still executes on every device, constituting a latent crash on API < 24 devices without `FileProvider` support configured for `Uri.fromFile`. The stale `putExtra` at line 63 should be removed entirely.

---

### A02-4 — MEDIUM: `public` visibility on mutable instance state fields in `BaseFragment.java` and `BaseThemedDialog.java`

**Files:**
- `BaseFragment.java`, lines 38, 41, 42: `isDestroyed`, `tempPhotoFilePath`, `subFragPermission`
- `BaseThemedDialog.java`, lines 37–41: `base_themed_dialog_right_text_view`, `base_themed_dialog_left_text_view`, `headerRightText`, `headerLeftText`

All of these are mutable fields exposed as `public` without accessors. Subclasses and external callers can freely mutate them, bypassing any invariants the owning class depends on. For example, `isDestroyed` being `public` means any caller can set it to `false` after `onDestroy`, breaking the lifecycle guard used in every progress-display method. `subFragPermission` being `public` allows callers to replace or null it, causing NPEs in `onStop`/`onResume`. The `TextView` fields on `BaseThemedDialog` expose internal View references publicly, creating tight coupling between the dialog internals and any code that directly manipulates them. Proper encapsulation (private/protected with accessors or protected setters) is required.

---

### A02-5 — MEDIUM: `isDestroyed` field name shadows `Fragment.isDestroyed()` method in `BaseFragment.java`

**File:** `BaseFragment.java`, lines 38, 281–283

```java
public boolean isDestroyed = false;   // field

@Override
public boolean isDestroyed() {        // interface implementation
    return isDestroyed;
}
```

`Fragment` does not declare `isDestroyed()`, but `BaseController` does. The field is named identically to the method. Within the class, `isDestroyed` always resolves to the field; however, the name collision makes it easy for a reader (or IDE auto-completion) to confuse the field access with a method call. Additionally, `Activity.isDestroyed()` (API 17+) exists in the parent chain of `BaseActivity`, and naming a public field `isDestroyed` on a Fragment that is closely associated with that Activity increases confusion. The same pattern is replicated in `BaseDialog` (not in scope but confirmed by cross-read).

---

### A02-6 — MEDIUM: Reflection-based `mChildFragmentManager` workaround in `BaseFragment.java` (lines 35–36, 160–168, 200–208)

**File:** `BaseFragment.java`, lines 35–36, 160–168, 200–208

```java
private static final Field sChildFragmentManagerField;
// ...
f = Fragment.class.getDeclaredField("mChildFragmentManager");
f.setAccessible(true);
// ...
sChildFragmentManagerField.set(this, null);
```

This is a well-known workaround for a bug in old versions of the support library (`android.support.v4.app.Fragment`) where the child `FragmentManager` was not properly reset on detach, causing crashes on re-attach. The project now targets modern Android; the support library itself is frozen (superseded by AndroidX). This reflection patch:
- Breaks on obfuscated builds (ProGuard will rename `mChildFragmentManager`).
- Will silently fail if the field is absent (caught, logged, but `sChildFragmentManagerField` is set to `null`) — the `onDetach` null-check handles this, but the workaround is completely bypassed.
- Constitutes a dependency on an internal, private field of a third-party library.

The fix is migration to AndroidX, where this bug does not exist. The workaround should be documented with the exact support library version it targets, or removed if the minimum SDK/support-library version has been raised past the affected range.

---

### A02-7 — MEDIUM: Deprecated `Vibrator.vibrate(long)` usage in `BaseThemedDialog.java` (line 208)

**File:** `BaseThemedDialog.java`, line 208

```java
mVibrator.vibrate(Long.valueOf(String.valueOf(duration)));
```

`Vibrator.vibrate(long)` is deprecated since API 26 (Android 8.0). The replacement is `Vibrator.vibrate(VibrationEffect)`. The boxing round-trip `Long.valueOf(String.valueOf(duration))` is also unnecessary and needlessly allocates heap objects; `(long) duration` is sufficient for the deprecated call. The method should be updated to use `VibrationEffect.createOneShot` with an API-level guard.

---

### A02-8 — MEDIUM: `vibrateOnPress` iterates full `mVibrateButtons` list on every call, re-registering listeners on previously registered views

**File:** `BaseThemedDialog.java`, lines 179–197

```java
protected void vibrateOnPress(View view){
    mVibrateButtons.add(view);
    for (final View b : mVibrateButtons){
        b.setOnTouchListener(new View.OnTouchListener() { ... });
    }
}
```

Each time `vibrateOnPress` is called with a new view, the loop iterates over all previously registered views and replaces their `OnTouchListener` with a new anonymous instance. For N calls, the first view gets its listener replaced N times. This is O(N²) listener allocations for N registered views and may cause unexpected behavior if a subclass has set a custom `OnTouchListener` on a previously registered view (it will be silently overwritten). The loop should only apply the listener to the newly added view.

---

### A02-9 — LOW: Commented-out method block in `BaseController.java` (referenced interface; lines 16–23)

**File (supporting reference):** `BaseController.java`, lines 16–23

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

Although `BaseController.java` is not in scope for this audit, it is the interface implemented by `BaseFragment` (in scope). The entire progress/permission contract that `BaseFragment` implements (methods at lines 124–158) is commented out of the interface, meaning those methods are not enforced by the contract. This is a leaky abstraction: callers who hold a `BaseController` reference cannot call `showProgress`, `hideProgress`, etc., even though every concrete class provides them. The methods should either be restored to the interface or moved to a separate interface/abstract class.

---

### A02-10 — LOW: `onStart()` and `onPause()` are no-op overrides in `BaseFragment.java` and `BaseThemedDialog.java`

**Files:**
- `BaseFragment.java`, lines 172–175 (`onStart`) and lines 233–235 (`onPause`)
- `BaseThemedDialog.java`, lines 212–214 (`onPause`)

These lifecycle methods call only `super` and have no additional logic. No-op overrides add noise without benefit, increase the maintenance surface, and mislead readers into thinking the methods contain application logic. They should be removed unless there is an explicit intention to document future extension points, in which case a comment is required.

---

### A02-11 — LOW: `mTitle` field is declared but never used in `BaseThemedDialog.java`

**File:** `BaseThemedDialog.java`, line 44

```java
protected String mTitle;
```

This field is declared `protected`, is never assigned in `BaseThemedDialog`, and is not referenced in `setTitleText` (which reads a method parameter instead). There is no setter. If subclasses rely on it they could reference it, but it has no initialisation path through the base class, making its purpose ambiguous. If no subclass uses it, it is dead code.

---

### A02-12 — LOW: `mRequests` field is declared but never used in `BaseThemedDialog.java`

**File:** `BaseThemedDialog.java`, line 33 and constructor line 109

```java
protected ArrayList<String> mRequests;
// ...
public BaseThemedDialog(){
    mRequests = new ArrayList<>();
}
```

`mRequests` is initialised in the constructor but is never read or written anywhere in `BaseThemedDialog`. No method adds to or reads from it. If no subclass uses it, this is dead code. The allocation in the constructor wastes heap on every dialog instantiation.

---

### A02-13 — LOW: `getCurrentWidth()` and `getCurrentHeight()` are private and never called in `BaseThemedDialog.java`

**File:** `BaseThemedDialog.java`, lines 171–177

```java
private int getCurrentWidth(){ ... }
private int getCurrentHeight(){ ... }
```

Both methods are `private` and have no internal callers. They are dead code. If they were intended as hooks for subclasses they should be `protected`; as private methods with no callers they should be removed.

---

### A02-14 — LOW: Inconsistent spacing on `public` modifier in `BaseFragment.java`

**File:** `BaseFragment.java`, lines 33, 45, 237, 249, 263

Several method declarations have a double space between the access modifier and the return type or the `static` keyword:

```java
public  static final int REQUEST_TAKE_PHOTO = 200;   // line 33
public  void takePhoto() {                            // line 45
public  void showDialog(...) {                        // lines 237, 249, 263
```

This is a minor but pervasive style inconsistency across the same file. The rest of the project uses single spaces.

---

### A02-15 — INFO: `BaseSubFragment` is a plain class named with "Fragment" but does not extend `Fragment`

**File:** `BaseSubFragment.java`

`BaseSubFragment` is a plain Java class (not a `Fragment` subclass) that manually manages a lifecycle via `onActive`, `onHidden`, and `onDestroy`. The name "SubFragment" implies an Android Fragment, but it operates more like a view-controller or presenter. This naming may mislead maintainers. The design is consistent within the codebase (it is used as a helper by `SubFragPermission`), but should be noted as a potential source of confusion for new contributors.

---

## Summary Table

| ID | Severity | File | Issue |
|---|---|---|---|
| A02-1 | HIGH | BaseFragment.java:77-80 | Commented-out lifecycle guard in `takePhoto`; `startActivityForResult` unprotected from non-resumed state |
| A02-2 | HIGH | BaseThemedDialog.java:143-151 | Duplicate initialisation block in `inflateLayout` re-runs `onCreateView` setup, double-calls window APIs and resets `mVibrateButtons` |
| A02-3 | HIGH | BaseFragment.java:63 | Deprecated `Uri.fromFile` remains in intent extras before being overridden; causes `FileUriExposedException` on API < 24 without FileProvider |
| A02-4 | MEDIUM | BaseFragment.java:38,41,42; BaseThemedDialog.java:37-41 | Mutable state exposed as `public` fields; bypasses lifecycle invariants |
| A02-5 | MEDIUM | BaseFragment.java:38,281 | `isDestroyed` field name shadows interface method name; confusion risk |
| A02-6 | MEDIUM | BaseFragment.java:35,160-168,200-208 | Reflection hack targeting private support-library field; breaks under ProGuard and is obsolete with AndroidX |
| A02-7 | MEDIUM | BaseThemedDialog.java:208 | Deprecated `Vibrator.vibrate(long)` with unnecessary boxing round-trip |
| A02-8 | MEDIUM | BaseThemedDialog.java:179-197 | `vibrateOnPress` re-registers listeners on all previously added views on each call; O(N²) allocations |
| A02-9 | LOW | BaseController.java (referenced interface) | Progress/permission contract methods commented out of interface, not enforced |
| A02-10 | LOW | BaseFragment.java:172,233; BaseThemedDialog.java:212 | No-op lifecycle override methods add noise without benefit |
| A02-11 | LOW | BaseThemedDialog.java:44 | `mTitle` field declared but never assigned or read in base class |
| A02-12 | LOW | BaseThemedDialog.java:33,109 | `mRequests` list allocated in constructor but never used |
| A02-13 | LOW | BaseThemedDialog.java:171-177 | `getCurrentWidth()` and `getCurrentHeight()` are private and have no callers (dead code) |
| A02-14 | LOW | BaseFragment.java:33,45,237,249,263 | Double-space after `public` modifier; style inconsistency |
| A02-15 | INFO | BaseSubFragment.java | Class named "SubFragment" is not a Fragment; potential naming confusion |
