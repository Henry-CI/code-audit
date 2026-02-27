# Pass 4 – Code Quality Audit
**Agent:** A08
**Audit run:** 2026-02-26-01
**Date:** 2026-02-27
**Files reviewed:**
1. `LibCommon/src/main/java/com/yy/libcommon/SignatureDialog.java`
2. `LibCommon/src/main/java/com/yy/libcommon/SquareImageView.java`
3. `LibCommon/src/main/java/com/yy/libcommon/SubFragPermission.java`

---

## Step 1: Reading Evidence

### File 1: `SignatureDialog.java`

**Class:** `SignatureDialog` — extends `BaseDialog` (which extends `DialogFragment`)

**Constants:**
- `BLOB_REF_KEY` (private static final String, line 26)

**Fields:**
- `mRootView` (private ViewGroup, line 29)
- `mDrawingView` (private DrawingView, line 30)
- `mClearButton` (private Button, line 31)
- `mCancelButton` (private Button, line 32)
- `mSaveButton` (private Button, line 33)
- `filePath` (package-private String — no access modifier, line 36)
- `mSignatureCallback` (private SignatureCallback, line 37)

**Methods (exhaustive):**
| Line | Method | Visibility |
|------|--------|------------|
| 40 | `onCreateView(LayoutInflater, ViewGroup, Bundle)` | `@Override public` |
| 55 | `newInstance(String path)` | `public static` |
| 63 | `setCallback(SignatureCallback)` | `public` |
| 68 | `onActivityCreated(Bundle)` | `@Override public` |
| 76 | `init()` | `public` |
| 80 | `findViews()` | `public` |
| 87 | `setupViews()` | `public` |
| 93 | `setUpViewListeners()` | `private` |
| 114 | `onSavePress()` | `private` |
| 157 | `onCancelPress()` | `private` |
| 161 | `saveSignature(Bitmap)` | `private` |
| 193 | `updateImageView(String)` | `private` |

**Nested types:**
- `SignatureCallback` (public interface, line 207) — single method `callBack(String filePath)`

---

### File 2: `SquareImageView.java`

**Class:** `SquareImageView` — extends `ImageView`

**Methods (exhaustive):**
| Line | Method | Visibility |
|------|--------|------------|
| 13 | `SquareImageView(Context)` | `public` |
| 17 | `SquareImageView(Context, AttributeSet)` | `public` |
| 21 | `SquareImageView(Context, AttributeSet, int)` | `public` |
| 25 | `onDraw(Canvas)` | `protected` |
| 30 | `onMeasure(int, int)` | `@Override protected` |

No constants, fields, or nested types.

---

### File 3: `SubFragPermission.java`

**Class:** `SubFragPermission` — extends `BaseSubFragment`

**Constants / Fields:**
| Line | Name | Visibility | Type |
|------|------|------------|------|
| 25 | `FILE_EDIT_NOTIFY` | package-private final | String |
| 26 | `CAMERA_NOTIFY` | package-private final | String |
| 28 | `cameraPendingRunnable` | public | Runnable |
| 29 | `filePendingRunnable` | public | Runnable |
| 87 | `broadcastReceiver` | package-private | BroadcastReceiver (anonymous) |
| 178 | `REQUEST_FILE_PERMISSION` | `final public static int` | int (100) |
| 179 | `REQUEST_CAMERA_PERMISSION` | `final public static int` | int (200) |

**Methods (exhaustive):**
| Line | Method | Visibility |
|------|--------|------------|
| 32 | `SubFragPermission(BaseActivity, BaseController)` | `public` |
| 37 | `onCameraFeatureEnabled()` | `public` |
| 50 | `onCameraFeatureDisabled()` | `public` |
| 61 | `onFileFeatureEnabled()` | `public` |
| 74 | `onFileFeatureDisabled()` | `public` |
| 87 | `broadcastReceiver` (anonymous BroadcastReceiver / `onReceive`) | package-private field |
| 114 | `onActive()` | `public` |
| 123 | `onHidden()` | `public` |
| 128 | `onDestroy()` | `public` |
| 132 | `checkCameraPermissionWithRun(Runnable)` | `public` |
| 150 | `isFilePermissionEnabled(Context)` | `public static` |
| 159 | `checkFilePermissionWithRun(Runnable)` | `public` |
| 180 | `requestFilePermission()` | `public` |
| 191 | `requestCameraPermission()` | `public` |
| 202 | `onRequestPermissionsResult(int, String[], int[])` | `public` |

---

## Step 2 & 3: Findings

---

### A08-1 — HIGH — Duplicate broadcast action strings make `CAMERA_NOTIFY` and `FILE_EDIT_NOTIFY` indistinguishable

**File:** `SubFragPermission.java`, lines 25–26

```java
final String FILE_EDIT_NOTIFY = "com.fleetiq.fleetiq360.file";
final String CAMERA_NOTIFY    = "com.fleetiq.fleetiq360.file";
```

Both constants are assigned the identical string value `"com.fleetiq.fleetiq360.file"`. Because both actions resolve to the same string, the two `if` branches inside `broadcastReceiver.onReceive()` (lines 95–108) will both evaluate to `true` for every broadcast, regardless of which feature triggered the send. A camera-permission broadcast will also trigger the file-permission callbacks and vice versa, causing the wrong permission feature to be enabled or disabled.

---

### A08-2 — HIGH — `onActivityCreated` in `SignatureDialog` calls the overridden `setupViews()` from `BaseDialog`, then immediately calls its own `setupViews()` again, causing double execution

**File:** `SignatureDialog.java`, lines 68–74 and `BaseDialog.java` lines 102–108

`SignatureDialog.onActivityCreated` calls `super.onActivityCreated(savedInstanceState)`. `BaseDialog.onActivityCreated` (line 107) calls `setupViews()`, which — because `SignatureDialog` overrides `setupViews()` — dispatches to `SignatureDialog.setupViews()`. Control then returns to `SignatureDialog.onActivityCreated`, which explicitly calls `setupViews()` a second time on line 71. The result is that `updateImageView(filePath)` is invoked twice on startup, causing an unnecessary duplicate bitmap decode and image-view assignment.

---

### A08-3 — HIGH — `filePath` field has package-private (default) visibility instead of `private`

**File:** `SignatureDialog.java`, line 36

```java
String filePath;
```

All other instance fields in the class are explicitly `private`. This field is used internally to track the persisted path of a saved signature bitmap. Exposing it at package scope breaks encapsulation, allows uncontrolled mutation from any class in `com.yy.libcommon`, and is inconsistent with the rest of the field declarations.

---

### A08-4 — HIGH — `saveSignature` swallows `IOException` via `e.printStackTrace()` with no logging tag and no user-visible context

**File:** `SignatureDialog.java`, lines 185–187

```java
} catch (IOException e) {
    e.printStackTrace();
}
```

The codebase uses `Log.i("DEV9", ...)` (line 202) as its logging convention. The unchecked `printStackTrace()` call routes output only to `System.err` on the device, bypasses Android's logcat tag system, and makes it impossible to filter these errors in production logging. The `FileOutputStream` opened on line 177 is also not closed in the `catch` or `finally` block, leaking the file descriptor on failure.

---

### A08-5 — MEDIUM — `init()`, `findViews()`, and `setupViews()` are unnecessarily `public` in `SignatureDialog`

**File:** `SignatureDialog.java`, lines 76, 80, 87

`init()`, `findViews()`, and `setupViews()` are internal lifecycle helpers called only from `onActivityCreated`. They are not part of any interface contract. Declaring them `public` exposes internal setup details to callers outside the class and breaks the encapsulation contract. `setUpViewListeners()` (line 93) is correctly `private`. This is a naming and visibility inconsistency within the same class.

---

### A08-6 — MEDIUM — Inconsistent capitalisation: `setupViews` vs `setUpViewListeners`

**File:** `SignatureDialog.java`, lines 87, 93

The class contains two methods that follow different naming conventions for the same word "setup":

- `setupViews()` — camel-case, no separator between "set" and "up"
- `setUpViewListeners()` — capitalised "U" separating "set" and "Up"

Both methods perform analogous initialisation tasks. The inconsistency makes the API harder to read and understand. The same discrepancy is present in `onActivityCreated` where both are called consecutively (lines 71 and 73).

---

### A08-7 — MEDIUM — `SquareImageView.onDraw` is a no-op override that adds no value

**File:** `SquareImageView.java`, lines 25–27

```java
protected void onDraw(Canvas canvas) {
    super.onDraw(canvas);
}
```

This override does nothing beyond delegating to `super.onDraw`. It adds a non-trivial entry point to the draw path without purpose. The `@Override` annotation is also missing, leaving no compiler guard if the parent signature changes. Dead overrides mislead readers into expecting custom drawing behaviour.

---

### A08-8 — MEDIUM — `SubFragPermission.cameraPendingRunnable` and `filePendingRunnable` are `public` fields

**File:** `SubFragPermission.java`, lines 28–29

```java
public Runnable cameraPendingRunnable;
public Runnable filePendingRunnable;
```

These mutable state-carrying fields are exposed publicly. Any external caller can null them out, replace them, or run them directly, bypassing the intended permission-check flow in `checkCameraPermissionWithRun` and `checkFilePermissionWithRun`. They should be `private` with no direct public accessor.

---

### A08-9 — MEDIUM — `REQUEST_FILE_PERMISSION` and `REQUEST_CAMERA_PERMISSION` constant modifier order is non-standard

**File:** `SubFragPermission.java`, lines 178–179

```java
final public static int REQUEST_FILE_PERMISSION   = 100;
final public static int REQUEST_CAMERA_PERMISSION = 200;
```

Java convention (and the Android/Google style guide) specifies the modifier order: `public static final`. Placing `final` first is non-idiomatic, inconsistent with every other constant in the codebase, and will generate a style warning in many linters and IDE inspections.

---

### A08-10 — MEDIUM — `broadcastReceiver` in `SubFragPermission` is never unregistered when `onHidden()` is called; only `onDestroy()` unregisters it

**File:** `SubFragPermission.java`, lines 114–130

`onActive()` registers the `BroadcastReceiver` (line 119). `onHidden()` (lines 123–126) is empty — it does not unregister. Only `onDestroy()` (line 129) unregisters. Because `onActive()` may be called multiple times across hide/show cycles (e.g., fragment back-stack navigation), each call registers an additional receiver without a corresponding unregister in `onHidden`, leading to multiple duplicate registrations and redundant callback invocations.

---

### A08-11 — MEDIUM — `onHidden()` body is empty with no comment

**File:** `SubFragPermission.java`, lines 123–126

```java
public void onHidden(){


}
```

The parent class `BaseSubFragment.onHidden()` sets `isHidden = true`. `SubFragPermission.onHidden()` overrides this method but neither calls `super.onHidden()` nor provides a comment explaining the intentional omission. The result is that `isHidden` remains `false` after the fragment is hidden, making `isActive()` return incorrect results and the parent class's state inconsistent.

---

### A08-12 — MEDIUM — `isFilePermissionEnabled` uses expanded `if/else return true/return false` instead of direct boolean return

**File:** `SubFragPermission.java`, lines 150–157

```java
public static boolean isFilePermissionEnabled(Context context){
    if (ContextCompat.checkSelfPermission(context, Manifest.permission.WRITE_EXTERNAL_STORAGE)
            != PackageManager.PERMISSION_GRANTED) {
        return false;
    } else {
        return true;
    }
}
```

The condition already produces a boolean. The equivalent direct form `return ContextCompat.checkSelfPermission(...) == PackageManager.PERMISSION_GRANTED;` is cleaner. This pattern is a style inconsistency: `checkCameraPermissionWithRun` and `checkFilePermissionWithRun` return early without an `else` block, while this static helper wraps the result in an explicit two-branch if/else.

---

### A08-13 — LOW — `bundle.putSerializable` used for a `String` argument in `newInstance`

**File:** `SignatureDialog.java`, line 58

```java
bundle.putSerializable(BLOB_REF_KEY, path);
```

`String` is retrieved via `getArguments().getString(BLOB_REF_KEY)` on line 49, meaning the put/get pair is mismatched. `putString`/`getString` is the correct and type-safe API pair for `String` values. While `putSerializable` works for `String` (since `String implements Serializable`), the mismatch is inconsistent, potentially slower due to serialisation overhead, and will generate IDE warnings.

---

### A08-14 — LOW — Debug log tag `"DEV9"` left in production code

**File:** `SignatureDialog.java`, line 202

```java
Log.i("DEV9", "Clearing image");
```

The tag `"DEV9"` is a development-time debug label. Log statements with ad-hoc tags should be removed or replaced with a module-level `TAG` constant before production. The log call is inside the `else` branch for `currentPhotoPath == null`, which can occur in normal operation. This is the only `Log` statement in the file; it uses a tag inconsistent with anything else in the codebase.

---

### A08-15 — LOW — `SignatureDialog` inner interface method has redundant `public` modifier

**File:** `SignatureDialog.java`, line 208

```java
public interface SignatureCallback {
    public void callBack(String filePath);
}
```

All interface methods are implicitly `public abstract`. Explicitly adding `public` is redundant and inconsistent with modern Java style.

---

### A08-16 — LOW — Redundant self-imports in `SubFragPermission.java`

**File:** `SubFragPermission.java`, lines 13–15

```java
import com.yy.libcommon.BaseActivity;
import com.yy.libcommon.BaseController;
import com.yy.libcommon.BaseSubFragment;
```

`SubFragPermission` is itself in `package com.yy.libcommon`. Importing types from the same package is unnecessary, adds noise, and will generate "unnecessary import" warnings in every standard Java IDE and lint tool.

---

### A08-17 — LOW — Typo in user-facing error message string

**File:** `SignatureDialog.java`, line 130

```java
"Failed to save, , please check your internet connection and retry."
```

The string contains a doubled comma (`", ,"`) which is a copy-paste or editing error. This text is shown directly to end users in an `ErrorDialog`.

---

### A08-18 — LOW — Unused `android.content.BroadcastReceiver` import

**File:** `SubFragPermission.java`, line 7

```java
import android.content.BroadcastReceiver;
```

The anonymous `BroadcastReceiver` on line 87 is declared via the class body, not as a named import reference. Android Studio and standard linters will flag this as an unused import. (Note: the import is technically required to instantiate the anonymous subclass — this item warrants compiler verification; if the anonymous class instantiation implicitly needs it the import is valid and this finding should be closed.)

---

## Summary Table

| ID | Severity | File | Issue |
|----|----------|------|-------|
| A08-1 | HIGH | SubFragPermission.java:25–26 | Duplicate action string makes CAMERA_NOTIFY and FILE_EDIT_NOTIFY identical — cross-triggering of wrong permission callbacks |
| A08-2 | HIGH | SignatureDialog.java:68–74 | `setupViews()` called twice on startup due to `super.onActivityCreated` delegation |
| A08-3 | HIGH | SignatureDialog.java:36 | `filePath` field is package-private instead of `private` |
| A08-4 | HIGH | SignatureDialog.java:185–187 | `IOException` swallowed by `e.printStackTrace()`; `FileOutputStream` not closed on error |
| A08-5 | MEDIUM | SignatureDialog.java:76,80,87 | `init()`, `findViews()`, `setupViews()` unnecessarily `public` |
| A08-6 | MEDIUM | SignatureDialog.java:87,93 | Naming inconsistency `setupViews` vs `setUpViewListeners` |
| A08-7 | MEDIUM | SquareImageView.java:25–27 | No-op `onDraw` override missing `@Override` annotation |
| A08-8 | MEDIUM | SubFragPermission.java:28–29 | `cameraPendingRunnable` and `filePendingRunnable` publicly mutable |
| A08-9 | MEDIUM | SubFragPermission.java:178–179 | Non-standard modifier order `final public static` |
| A08-10 | MEDIUM | SubFragPermission.java:114–129 | Receiver registered multiple times; `onHidden` does not unregister |
| A08-11 | MEDIUM | SubFragPermission.java:123–126 | `onHidden()` does not call `super.onHidden()`; `isHidden` never set to `true` |
| A08-12 | MEDIUM | SubFragPermission.java:150–157 | Expanded `if/else return true/false` instead of direct boolean return |
| A08-13 | LOW | SignatureDialog.java:58 | `putSerializable` used for `String` argument; `getString` used to retrieve it |
| A08-14 | LOW | SignatureDialog.java:202 | Debug tag `"DEV9"` left in production log call |
| A08-15 | LOW | SignatureDialog.java:208 | Redundant `public` modifier on interface method |
| A08-16 | LOW | SubFragPermission.java:13–15 | Same-package imports are unnecessary |
| A08-17 | LOW | SignatureDialog.java:130 | Doubled comma typo in user-facing error message |
| A08-18 | LOW | SubFragPermission.java:7 | Potentially unused `BroadcastReceiver` import (verify with compiler) |
