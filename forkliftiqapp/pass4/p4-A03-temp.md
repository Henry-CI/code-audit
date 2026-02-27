# Pass 4 – Code Quality Audit
**Agent:** A03
**Audit run:** 2026-02-26-01
**Files assigned:**
1. `LibCommon/src/main/java/com/yy/libcommon/CommonLib/NetworkDetect.java`
2. `LibCommon/src/main/java/com/yy/libcommon/CustomProgressDialog.java`
3. `LibCommon/src/main/java/com/yy/libcommon/DrawingView.java`

---

## Step 1: Reading Evidence

### File 1: NetworkDetect.java

**Full path:** `LibCommon/src/main/java/com/yy/libcommon/CommonLib/NetworkDetect.java`

**Class:** `NetworkDetect` (package `com.yy.libcommon.CommonLib`)

**Methods (exhaustive):**
| Method | Line |
|---|---|
| `static public boolean isNetworkConnected(Context context)` | 13 |

**Types / Constants / Enums / Interfaces defined:** None.

**Imports used:**
- `android.content.Context`
- `android.net.ConnectivityManager`
- `android.net.NetworkInfo`

---

### File 2: CustomProgressDialog.java

**Full path:** `LibCommon/src/main/java/com/yy/libcommon/CustomProgressDialog.java`

**Class:** `CustomProgressDialog extends BaseThemedDialog` (package `com.yy.libcommon`)

**Methods (exhaustive):**
| Method | Line |
|---|---|
| `public CustomProgressDialog()` (constructor) | 25 |
| `public void onCreate(Bundle savedInstanceState)` | 30 |
| `public static CustomProgressDialog newInstance(String title, String details)` | 39 |
| `protected void setupViews()` | 53 |
| `public void updateText(String message)` | 77 |

**Constants defined:**
| Constant | Line | Value |
|---|---|---|
| `private static final String TITLE` | 17 | `"TITLE"` |
| `private static final String DETAILS` | 18 | `"DETAILS"` |

**Fields:**
| Field | Line | Visibility |
|---|---|---|
| `private String mTitle` | 20 | private |
| `private String mDetails` | 21 | private |
| `private TextView mDetailsTextView` | 23 | private |

**Commented-out code:** Lines 56–57 (window layout call).

---

### File 3: DrawingView.java

**Full path:** `LibCommon/src/main/java/com/yy/libcommon/DrawingView.java`

**Class:** `DrawingView extends View` (package `com.yy.libcommon`)

**Methods (exhaustive):**
| Method | Line |
|---|---|
| `public DrawingView(Context context, AttributeSet attrs)` (constructor) | 30 |
| `private void setupDrawing()` | 35 |
| `protected void onSizeChanged(int w, int h, int oldw, int oldh)` | 51 |
| `public boolean hasBeenDrawnOn()` | 64 |
| `public boolean hasImage()` | 68 |
| `protected void onDraw(Canvas canvas)` | 73 |
| `public void clear()` | 78 |
| `public void setImageBitmap(Bitmap bitmap)` | 85 |
| `public void save()` | 109 |
| `public boolean onTouchEvent(MotionEvent event)` | 114 |

**Fields:**
| Field | Line | Visibility |
|---|---|---|
| `private Path drawPath` | 20 | private |
| `private Paint drawPaint, canvasPaint` | 21 | private (two fields, one declaration) |
| `private int paintColor` | 22 | private |
| `private Canvas drawCanvas` | 23 | private |
| `public Bitmap canvasBitmap` | 24 | **public** |
| `private int mWidth` | 25 | private |
| `private int mHeight` | 26 | private |
| `private boolean hasBeenDrawnOn` | 27 | private |
| `private boolean hasImage` | 28 | private |

**Commented-out code:**
- Line 95: `//canvas.drawBitmap(canvasBitmap, 0, 0, canvasPaint);`
- Lines 96–103: Multi-line block comment containing an alternate `drawCanvas` null-check implementation.
- Line 104: `//canvasBitmap = bitmap;`

---

## Step 2 & 3: Findings

---

### A03-1 — HIGH — Deprecated API: `NetworkInfo` and `ConnectivityManager.getActiveNetworkInfo()`

**File:** `NetworkDetect.java`, lines 5, 16

`android.net.NetworkInfo` was deprecated in API level 29 (Android 10). `ConnectivityManager.getActiveNetworkInfo()` was likewise deprecated in API 29. The project targets SDK 26, so these calls compile without error today, but any future target SDK bump to 29+ will trigger lint deprecation warnings and eventually require migration to the `ConnectivityManager.registerNetworkCallback()` / `NetworkCapabilities` API. The class is actively called in five separate call sites across the app (`SyncService`, `CacheService`, `WebData`, `MyApplication` × 2), amplifying the impact of this technical debt.

**Evidence:**
```java
// NetworkDetect.java:15–17
ConnectivityManager connMgr = (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
return ((networkInfo != null) && (networkInfo.isConnected()));
```

---

### A03-2 — HIGH — Null-Pointer Dereference: `DrawingView.setImageBitmap(null)` crashes unconditionally

**File:** `DrawingView.java`, lines 87–91

`setImageBitmap` guards `hasImage = true` with a null check (line 87–89), but then calls `bitmap.copy(...)` on line 91 without any null guard. `SignatureDialog.updateImageView()` (line 201) explicitly passes `null` to clear the image. This produces an unconditional `NullPointerException` at runtime whenever the user clears an image from the signature dialog.

**Evidence:**
```java
// DrawingView.java:85–91
public void setImageBitmap(Bitmap bitmap){
    if (bitmap != null){
        hasImage = true;
    }
    canvasBitmap = bitmap.copy(bitmap.getConfig(), true);  // NPE when bitmap == null
    drawCanvas = new Canvas(canvasBitmap);
    drawCanvas.drawBitmap(canvasBitmap, 0, 0, canvasPaint);
    ...
}
```
```java
// SignatureDialog.java:201
mDrawingView.setImageBitmap(null);  // caller that triggers the crash
```

---

### A03-3 — HIGH — Dead Method with Empty Body: `DrawingView.save()`

**File:** `DrawingView.java`, lines 109–111

`public void save()` has a completely empty body. It is public, meaning it is part of the API surface of a library class. It is referenced nowhere in the codebase (search across all `.java` files confirmed zero callers). This is either an unimplemented stub that was never completed or dead code that was stripped of its implementation and forgotten. An empty public method in a library View class is a leaky abstraction — callers cannot distinguish "save did nothing" from an error condition.

**Evidence:**
```java
public void save(){

}
```

---

### A03-4 — MEDIUM — Commented-Out Code Block in `DrawingView.setImageBitmap()`

**File:** `DrawingView.java`, lines 95–104

Three separate commented-out code fragments remain in `setImageBitmap`:
- Line 95: `//canvas.drawBitmap(canvasBitmap, 0, 0, canvasPaint);` — references a variable `canvas` that does not exist in the method scope (it was a parameter name from `onDraw`), indicating this is stale copy-paste debris.
- Lines 96–103: A block-comment `/* if (drawCanvas == null) ... */` representing a discarded alternative implementation.
- Line 104: `//canvasBitmap = bitmap;` — a discarded simpler assignment.

These fragments obscure the current logic, introduce noise, and should be deleted.

**Evidence:**
```java
//canvas.drawBitmap(canvasBitmap, 0, 0, canvasPaint);
/*
if (drawCanvas == null){
    drawCanvas = new Canvas();
    drawCanvas.drawBitmap(bitmap, 0, 0, null);
} else {
    drawCanvas.drawBitmap(bitmap, 0, 0, null);
}
*/
//canvasBitmap = bitmap;
```

---

### A03-5 — MEDIUM — Commented-Out Code in `CustomProgressDialog.setupViews()`

**File:** `CustomProgressDialog.java`, lines 56–57

A call to set the dialog window dimensions is commented out:
```java
//        getDialog().getWindow().setLayout(Util.dpToPx(getResources().getDimension(R.dimen.default_dialog_width),
//                getActivity()), ViewGroup.LayoutParams.WRAP_CONTENT);
```
This is two-line functional code (not documentation) that has been disabled. Its comment contains a `ViewGroup` reference whose import (`android.view.ViewGroup`) is retained in the file's imports at line 5. Since no other code in this file uses `ViewGroup`, this import is now dead. The commented-out block should either be reinstated or deleted (and the unused import removed).

---

### A03-6 — MEDIUM — Leaky Abstraction: `DrawingView.canvasBitmap` is `public`

**File:** `DrawingView.java`, line 24

`public Bitmap canvasBitmap` exposes a mutable internal rendering field directly. Callers can replace or nullify it without going through the `onSizeChanged`/`drawCanvas` synchronization logic, creating a state divergence where `drawCanvas` points to the old bitmap while `canvasBitmap` points to a new one. There is no `getCanvasBitmap()` accessor; the only external consumer (`SignatureDialog`) accesses the bitmap via `getDrawingCache()` instead, meaning this public field is an unnecessary exposure. It should be `private` with a dedicated read-only accessor if external access is genuinely required.

**Evidence:**
```java
public Bitmap canvasBitmap;  // line 24 — no encapsulation
```

---

### A03-7 — MEDIUM — Redundant Self-Draw in `DrawingView.setImageBitmap()`

**File:** `DrawingView.java`, lines 91–93

After `canvasBitmap` is set via `bitmap.copy(...)`, the code immediately draws `canvasBitmap` onto itself:
```java
canvasBitmap = bitmap.copy(bitmap.getConfig(), true);
drawCanvas = new Canvas(canvasBitmap);
drawCanvas.drawBitmap(canvasBitmap, 0, 0, canvasPaint);  // draws bitmap onto itself
```
Drawing a bitmap onto itself via its own canvas is a no-op at best and undefined behaviour at worst (Android's `Canvas` documentation warns against drawing a bitmap onto a canvas that was itself constructed from that bitmap). The correct intent — visible in the commented-out block on line 95 — was presumably `canvas.drawBitmap(canvasBitmap, ...)` inside `onDraw`. The live line 93 call is a functional error left over from the refactor whose remnants appear in the commented-out code (finding A03-4).

---

### A03-8 — MEDIUM — Inconsistent `hasBeenDrawnOn` Assignment in `onTouchEvent`

**File:** `DrawingView.java`, lines 122, 126, 130

`hasBeenDrawnOn = true` is set redundantly in all three of `ACTION_DOWN`, `ACTION_MOVE`, and `ACTION_UP`. Setting it on `ACTION_DOWN` alone is sufficient (and semantically more accurate, as the user has begun drawing). The redundant assignments in `MOVE` and `UP` are low-risk but reflect inconsistency in reasoning about when the flag should be set.

---

### A03-9 — MEDIUM — Missing `@Nullable` / null-safety on `connMgr` in `NetworkDetect`

**File:** `NetworkDetect.java`, line 15

`Context.getSystemService(CONNECTIVITY_SERVICE)` can return `null` (documented by Android SDK). The result is immediately cast and used without a null check. If the service is unavailable, `connMgr.getActiveNetworkInfo()` on line 16 will throw a `NullPointerException`. Given this method is called in five critical paths (sync, cache, data fetch, and application startup), a crash here would be severe.

**Evidence:**
```java
ConnectivityManager connMgr = (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();  // NPE if connMgr == null
```

---

### A03-10 — LOW — Stale Creation Date: `NetworkDetect.java` (2015)

**File:** `NetworkDetect.java`, line 9

The Javadoc header reads `Created by steveyang on 9/07/2015`. The class has not been updated to reflect modern Android networking APIs introduced after API 21 (the current `minSdkVersion`). The date itself is not a code defect, but in conjunction with finding A03-1 it documents that this file has received zero maintenance in ~10 years despite material API deprecations.

---

### A03-11 — LOW — Style: `static public` instead of `public static`

**File:** `NetworkDetect.java`, line 13

The modifier order `static public boolean isNetworkConnected` violates the standard Java convention (`public static`). The Java Language Specification recommends the ordering: access modifier first, then `static`. Android Lint and all major style guides (Google Java Style, Oracle) flag this ordering.

**Evidence:**
```java
static public boolean isNetworkConnected (Context context) {
```

---

### A03-12 — LOW — Unused Import: `android.view.ViewGroup` in `CustomProgressDialog`

**File:** `CustomProgressDialog.java`, line 5

`ViewGroup` is imported but only referenced in the commented-out code on lines 56–57. With that code disabled, no live code in this file uses `ViewGroup`. This is a dead import that will generate an "Unused import" IDE warning.

---

### A03-13 — LOW — Package Naming Inconsistency: `CommonLib` sub-package uses mixed case

**File:** `NetworkDetect.java`, line 1

The package is `com.yy.libcommon.CommonLib`. Java package naming convention mandates all-lowercase. `CommonLib` uses PascalCase (matching a class name convention, not a package convention). All other classes in scope use `com.yy.libcommon` without a mixed-case sub-package. This inconsistency means `NetworkDetect` is physically and logically separated from its sibling utility classes for no architectural reason.

---

## Summary Table

| ID | Severity | File | Issue |
|---|---|---|---|
| A03-1 | HIGH | NetworkDetect.java | Deprecated `NetworkInfo` / `getActiveNetworkInfo()` API (deprecated API 29) |
| A03-2 | HIGH | DrawingView.java | NPE crash when `setImageBitmap(null)` called — unconditional `bitmap.copy()` |
| A03-3 | HIGH | DrawingView.java | Empty public method `save()` — dead/unimplemented API surface |
| A03-4 | MEDIUM | DrawingView.java | Three commented-out code fragments in `setImageBitmap()` |
| A03-5 | MEDIUM | CustomProgressDialog.java | Commented-out `setLayout` call; leaves `ViewGroup` import dead |
| A03-6 | MEDIUM | DrawingView.java | `public Bitmap canvasBitmap` — mutable internal field exposed publicly |
| A03-7 | MEDIUM | DrawingView.java | Self-draw: bitmap drawn onto its own canvas (no-op / undefined) |
| A03-8 | MEDIUM | DrawingView.java | `hasBeenDrawnOn = true` set redundantly in all three touch event cases |
| A03-9 | MEDIUM | NetworkDetect.java | `getSystemService()` result not null-checked before dereference |
| A03-10 | LOW | NetworkDetect.java | Stale 2015 creation date; no maintenance against API deprecations |
| A03-11 | LOW | NetworkDetect.java | `static public` modifier order — should be `public static` |
| A03-12 | LOW | CustomProgressDialog.java | Unused import `android.view.ViewGroup` |
| A03-13 | LOW | NetworkDetect.java | Package `CommonLib` uses PascalCase, violating Java package naming convention |
