# Audit Report — Pass 4 (Code Quality)
**Audit Run:** 2026-02-26-01
**Agent:** A04
**Date:** 2026-02-27

---

## Section 1: Reading Evidence

### File 1: `LibCommon/src/main/java/com/yy/libcommon/ErrorDialog.java`

**Class:** `ErrorDialog` (extends `BaseDialog`)

**Fields:**
- `private TextView mTitleTextView` (line 19)
- `private TextView mErrorText` (line 20)
- `private TextView mCloseButton` (line 21)
- `private String mTitle` (line 23)
- `private String mContent` (line 24)
- `private String mCloseButtonText` (line 25)
- `private OnErrorCallback mCallback` (line 27)

**Methods:**
| Line | Signature |
|------|-----------|
| 31 | `public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)` |
| 40 | `public static ErrorDialog newInstance(String title, String content, String buttonText)` |
| 60 | `public void setOnErrorCallback(OnErrorCallback callback)` |
| 65 | `protected void setupViews()` |
| 106 | `public void onDismiss(DialogInterface dialog)` |

**Inner types:**
- `public static class OnErrorCallback` (line 113)
  - `public void onCloseButton()` (line 114) — empty body
  - `public void onDismiss()` (line 117) — empty body

---

### File 2: `LibCommon/src/main/java/com/yy/libcommon/FileManager.java`

**Class:** `FileManager` (plain class, not extending anything)

**Fields:**
- `private static FileManager ourInstance` (line 27)

**Methods:**
| Line | Signature |
|------|-----------|
| 31 | `public static FileManager instance()` |
| 38 | `public static Bitmap readBitmapFromPath(String path)` |
| 54 | `public static File createFilePath(String fileFullPath)` |
| 88 | `public static String getFileDir()` |
| 95 | `public static File createLocalImageFile(String fileName)` |
| 111 | `public static void copyFile(File sourceFile, File destFile)` |
| 147 | `public static void safeDeleteFile(Context context, final String path)` |
| 181 | `public static String getFileTypeString()` |
| 185 | `public static String getLocalFileFolder()` |
| 189 | `public static String existingLocalFilePath(int key, int fileType)` |
| 197 | `public static String getLocalFilePath(int key, int fileType)` |
| 207 | `public static File getLocalFileInstance(int key)` |
| 217 | `public static String getLocalFileDir()` |
| 226 | `public static boolean isFileExist(String filePath)` |

**Constants referenced:**
- `LibConfig.BASE_DIRECTOY` (note: typo, "DIRECTOY" not "DIRECTORY")
- `LibConfig.IMAGE_DIRECTORY`

---

### File 3: `LibCommon/src/main/java/com/yy/libcommon/Font/AMButton.java`

**Class:** `AMButton` (extends `Button`)

**Methods:**
| Line | Signature |
|------|-----------|
| 17 | `public AMButton(Context context)` |
| 23 | `public AMButton(Context context, AttributeSet attrs)` |
| 29 | `public AMButton(Context context, AttributeSet attrs, int defStyle)` |
| 36 | `private void applyCustomFont(Context context, AttributeSet attrs)` |

**Enums / interfaces / constants defined:** None.

---

## Section 2 & 3: Findings

---

### A04-1 — HIGH — `ErrorDialog.onCreateView` calls `super.onCreate` instead of `super.onCreateView`

**File:** `LibCommon/src/main/java/com/yy/libcommon/ErrorDialog.java`, line 32

**Evidence:**
```java
@Override
public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);   // line 32 — wrong super call
    ...
}
```

`onCreateView` overrides the fragment lifecycle method for creating the view hierarchy. The correct super call inside `onCreateView` is `super.onCreateView(inflater, container, savedInstanceState)`. Calling `super.onCreate(savedInstanceState)` from within `onCreateView` invokes the wrong lifecycle phase on the parent class (`DialogFragment` → `Fragment`). In practice, Android normally calls `onCreate` before `onCreateView`, so calling it a second time is at minimum redundant and may corrupt the fragment's internal state. This is a lifecycle contract violation.

---

### A04-2 — HIGH — `FileManager.copyFile` silently swallows all exceptions

**File:** `LibCommon/src/main/java/com/yy/libcommon/FileManager.java`, lines 126–128

**Evidence:**
```java
catch (Exception e){
    // empty — no logging, no rethrow
}
```

The `catch` block for the file copy operation is completely empty. Any `IOException`, `SecurityException`, or other failure during the copy is silently discarded. The caller has no way to detect that the copy failed. This can lead to corrupt data states (e.g., an empty destination file from `createFilePath` existing with no content) that are very difficult to diagnose. All other `catch` blocks in the same method (`finally` blocks, lines 133 and 140) do at minimum call `e.printStackTrace()`. The inconsistency is especially dangerous here because the primary operation's failure is invisible.

---

### A04-3 — HIGH — `AMButton.applyCustomFont` leaks `TypedArray` (never calls `recycle()`)

**File:** `LibCommon/src/main/java/com/yy/libcommon/Font/AMButton.java`, lines 42–44

**Evidence:**
```java
TypedArray a = getContext().obtainStyledAttributes(attrs, R.styleable.AMTextView);
ttf = a.getString(R.styleable.AMTextView_ttf_type);
typeface = FontCache.getTypeFace(getContext(),ttf);
// a.recycle() is never called
```

`TypedArray` objects obtained via `obtainStyledAttributes` must be released by calling `a.recycle()` when done. Failing to do so leaks a native resource held by the `Resources` pool. This is confirmed as a systematic defect: `AMEditText.java` and `AMRadioButton.java` have the identical pattern and also omit `recycle()`. By contrast, `RadioImageButton.java` (line 37) and `ToggleImageButton.java` (line 39) correctly call `a.recycle()` in the same codebase, confirming the project standard is to recycle. Every view inflation where `attrs` is non-null creates a new unreleased `TypedArray`.

---

### A04-4 — MEDIUM — `FileManager.instance()` singleton is unused; all methods are static

**File:** `LibCommon/src/main/java/com/yy/libcommon/FileManager.java`, lines 27–36

**Evidence:**
```java
private static FileManager ourInstance;

public static FileManager instance() {
    if(ourInstance == null){
        ourInstance = new FileManager();
    }
    return ourInstance;
}
```

A singleton accessor is defined and a private `ourInstance` field is maintained, yet every method in `FileManager` is `static` and no instance method exists on `FileManager` itself. A codebase-wide search finds zero callers of `FileManager.instance()`. The singleton machinery (`ourInstance` field and `instance()` method) is entirely dead code. Additionally, the singleton is not thread-safe (no synchronization, no double-checked locking, no `volatile`), which would be a latent race condition if it were ever actually called.

---

### A04-5 — MEDIUM — `FileManager.getFileDir()` is a trivial, unnecessary wrapper

**File:** `LibCommon/src/main/java/com/yy/libcommon/FileManager.java`, lines 88–93

**Evidence:**
```java
public static String getFileDir() {
    String storageDir = FileManager.getLocalFileDir();
    return storageDir;
}
```

`getFileDir()` does nothing but delegate to `getLocalFileDir()` and immediately return the result via a named local variable. This wrapper adds no abstraction value, no validation, and no transformation. It creates confusion about which method callers should use (two names for the same behaviour). The intermediate variable `storageDir` is also unnecessary.

---

### A04-6 — MEDIUM — `existingLocalFilePath` and `getLocalFilePath` accept `fileType` parameter that is never used

**File:** `LibCommon/src/main/java/com/yy/libcommon/FileManager.java`, lines 189–204

**Evidence:**
```java
public static String existingLocalFilePath(int key, int fileType){
    File file = FileManager.getLocalFileInstance(key);
    // fileType is not used anywhere in this method body
    ...
}

public static String getLocalFilePath(int key, int fileType){
    String s = Environment.getExternalStorageDirectory()
            + File.separator + LibConfig.BASE_DIRECTOY
            + File.separator + FileManager.getLocalFileFolder()
            + File.separator + key + FileManager.getFileTypeString();
    // fileType is not used; getFileTypeString() is always ".jpg"
    return s;
}
```

Both methods accept a `fileType` parameter that is silently ignored. The extension is hardcoded via `getFileTypeString()` which always returns `".jpg"`. This is a leaky abstraction — the public API implies multi-type support that does not exist, misleading callers.

---

### A04-7 — MEDIUM — `Environment.getExternalStorageDirectory()` deprecated API used in four places

**File:** `LibCommon/src/main/java/com/yy/libcommon/FileManager.java`, lines 162, 199, 209, 219

**Evidence:**
```java
Uri.parse("file://" + Environment.getExternalStorageDirectory()));  // line 162
String s = Environment.getExternalStorageDirectory() + ...          // line 199
File newFile = new File(Environment.getExternalStorageDirectory()   // line 209
String s = Environment.getExternalStorageDirectory() + ...          // line 219
```

`Environment.getExternalStorageDirectory()` was deprecated in API level 29 (Android 10). On Android 10+ with `targetSdkVersion >= 29`, apps running in scoped storage mode may not have access to this path at all. The recommended replacement is `Context.getExternalFilesDir(String)` or `Context.getExternalCacheDir()`, which do not require the `READ_EXTERNAL_STORAGE` or `WRITE_EXTERNAL_STORAGE` permissions on Android 10+.

---

### A04-8 — MEDIUM — `safeDeleteFile` sends deprecated `ACTION_MEDIA_MOUNTED` broadcast (pre-KitKat branch)

**File:** `LibCommon/src/main/java/com/yy/libcommon/FileManager.java`, lines 160–162

**Evidence:**
```java
if(Build.VERSION.SDK_INT < Build.VERSION_CODES.KITKAT) {
    context.sendBroadcast(new Intent(Intent.ACTION_MEDIA_MOUNTED,
            Uri.parse("file://" + Environment.getExternalStorageDirectory())));
}
```

`ACTION_MEDIA_MOUNTED` is a protected broadcast and sending it from a third-party application is not supported. On API 19+ (KitKat), Android blocks or ignores this broadcast from non-system applications. The guard `< KITKAT` keeps this code reachable only on API 18 and below, but KitKat was released in 2013 and the minimum SDK for this project will not be below 19 in any current build configuration. This code path is dead in any real deployment and should be removed entirely.

---

### A04-9 — MEDIUM — `SimpleDateFormat` constructed without `Locale` argument

**File:** `LibCommon/src/main/java/com/yy/libcommon/FileManager.java`, line 101

**Evidence:**
```java
String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
```

`SimpleDateFormat(String)` uses the device's default `Locale`, which causes lint warning `NewApi`/`SimpleDateFormat` and can produce inconsistent filenames on devices with non-standard locales. The project's own other `SimpleDateFormat` usages (e.g., `ServerDateFormatter.java`, `CompanyDateFormatter.java`, `AndroidImagePicker.java`) all pass an explicit `Locale`. The correct form here is `new SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US)`.

---

### A04-10 — LOW — `LibConfig.BASE_DIRECTOY` is a typo ("DIRECTOY" missing "R")

**File:** `LibCommon/src/main/java/com/yy/libcommon/LibConfig.java`, line 8
**Referenced in:** `FileManager.java`, lines 200, 210, 220

**Evidence:**
```java
public static final String BASE_DIRECTOY = "ForkIQ360";  // "DIRECTORY" misspelled
```

The constant name `BASE_DIRECTOY` is missing the letter "R". This is a cosmetic defect in a public API constant. Renaming it is a breaking change for all referencing classes, but the misspelling should be fixed with a coordinated rename.

---

### A04-11 — LOW — `ErrorDialog.setupViews` uses `setHint("")` for missing content instead of `setText("")`

**File:** `LibCommon/src/main/java/com/yy/libcommon/ErrorDialog.java`, lines 80–84

**Evidence:**
```java
if (mContent != null) {
    mErrorText.setText(mContent);
} else {
    mErrorText.setHint("");   // should be setText("") for consistency
}
```

In the `mTitle` branch (lines 74–78), when title is null the code calls `mTitleTextView.setText("")` to clear it. In the `mContent` branch, the `else` clause calls `mErrorText.setHint("")` instead. `setHint` sets placeholder text shown only when the view is empty and focused (for `EditText`), but on a `TextView` it has effectively no visual effect at runtime. The inconsistency is a style defect and could cause confusion if the view is ever replaced with an `EditText`.

---

### A04-12 — LOW — `OnErrorCallback` implemented as a concrete class with empty methods instead of an interface

**File:** `LibCommon/src/main/java/com/yy/libcommon/ErrorDialog.java`, lines 113–120

**Evidence:**
```java
public static class OnErrorCallback {
    public void onCloseButton(){
    }
    public void onDismiss(){
    }
}
```

Using a concrete class with empty method bodies as a callback type means callers must subclass it. An `interface` (or an `abstract class` when partial implementation is intentional) is the idiomatic pattern for Android callback contracts. The existing design prevents callers from using anonymous interface implementations or lambda proxies. Since both methods have empty bodies, there is no default behaviour being provided — the class pattern conveys no advantage over an interface.

---

### A04-13 — LOW — `mCloseButton` field typed as `TextView` but semantically represents a button

**File:** `LibCommon/src/main/java/com/yy/libcommon/ErrorDialog.java`, line 21

**Evidence:**
```java
private TextView mCloseButton;
```

The field is named `mCloseButton` and its associated view resource is `error_dialog_closeTextView`. Using a `TextView` as a button is valid in Android, but the field name implies button semantics while the type says `TextView`. This inconsistency is a minor leaky abstraction — reader must examine the layout to understand the actual view type.

---

### A04-14 — LOW — `AMButton` uses `R.styleable.AMTextView` attribute set — mismatched naming

**File:** `LibCommon/src/main/java/com/yy/libcommon/Font/AMButton.java`, lines 42–43

**Evidence:**
```java
TypedArray a = getContext().obtainStyledAttributes(attrs, R.styleable.AMTextView);
ttf = a.getString(R.styleable.AMTextView_ttf_type);
```

`AMButton` reads its custom attribute from the `AMTextView` styleable. This is a leaky abstraction: the button widget depends on a styleable named after a different widget class. If `AMTextView` styleable attributes are ever renamed or refactored, `AMButton`, `AMEditText`, and `AMRadioButton` all break silently. The styleable should be named generically (e.g., `AMCustomFont` or `AMWidget`) and shared explicitly.

---

### A04-15 — INFO — `FileManager.readBitmapFromPath` deletes file on decode failure without logging

**File:** `LibCommon/src/main/java/com/yy/libcommon/FileManager.java`, lines 45–47

**Evidence:**
```java
if(mImageBitmap == null) {
    file.delete();
}
```

If `BitmapFactory.decodeFile` returns `null` (e.g., corrupted file, unsupported format, OOM), the file is silently deleted. There is no log statement, no error reporting, and no return value indicating deletion occurred. This makes debugging difficult because the evidence of what failed is destroyed.

---

### A04-16 — INFO — `createFilePath` uses `System.out.println` instead of `android.util.Log`

**File:** `LibCommon/src/main/java/com/yy/libcommon/FileManager.java`, lines 71–74

**Evidence:**
```java
System.out.println("Collateral directory "+ dir +" created");
System.out.println("Collateral directory  " + dir + " is not created");
```

`System.out.println` output is not visible in Android Logcat by default and does not carry a tag for filtering. The rest of `FileManager` uses `android.util.Log` (line 173). These two print statements should use `Log.d` or `Log.e` with an appropriate tag.

---

## Section 4: Summary Table

| ID | Severity | File | Description |
|----|----------|------|-------------|
| A04-1 | HIGH | ErrorDialog.java:32 | `onCreateView` calls `super.onCreate` — wrong lifecycle method |
| A04-2 | HIGH | FileManager.java:126 | `copyFile` silently swallows all exceptions — empty catch block |
| A04-3 | HIGH | AMButton.java:42 | `TypedArray` obtained but never recycled — resource leak |
| A04-4 | MEDIUM | FileManager.java:27 | Singleton `instance()` is dead code; all methods are static |
| A04-5 | MEDIUM | FileManager.java:88 | `getFileDir()` is a pointless wrapper around `getLocalFileDir()` |
| A04-6 | MEDIUM | FileManager.java:189,197 | `fileType` parameter accepted but never used in two methods |
| A04-7 | MEDIUM | FileManager.java:162,199,209,219 | `Environment.getExternalStorageDirectory()` deprecated in API 29 |
| A04-8 | MEDIUM | FileManager.java:160 | Deprecated `ACTION_MEDIA_MOUNTED` broadcast — dead pre-KitKat branch |
| A04-9 | MEDIUM | FileManager.java:101 | `SimpleDateFormat` constructed without explicit `Locale` |
| A04-10 | LOW | LibConfig.java:8 | `BASE_DIRECTOY` constant name is a typo (missing "R") |
| A04-11 | LOW | ErrorDialog.java:83 | `setHint("")` used inconsistently where `setText("")` is expected |
| A04-12 | LOW | ErrorDialog.java:113 | `OnErrorCallback` is a concrete class with empty bodies; should be interface |
| A04-13 | LOW | ErrorDialog.java:21 | Field `mCloseButton` typed as `TextView` — misleading naming |
| A04-14 | LOW | AMButton.java:42 | `AMButton` reads `R.styleable.AMTextView` — cross-widget styleable coupling |
| A04-15 | INFO | FileManager.java:45 | File deleted silently on bitmap decode failure — no logging |
| A04-16 | INFO | FileManager.java:71 | `System.out.println` used instead of `android.util.Log` |
