# Audit Report — Pass 4 (Code Quality)
**Agent:** A11
**Audit Run:** 2026-02-26-01
**Date:** 2026-02-27

---

## Assigned Files

1. `LibCommon/src/main/java/com/yy/libcommon/YesNoDialog.java`

---

## Step 1: Reading Evidence

### File: YesNoDialog.java

**Class name:** `YesNoDialog`
- Extends: `BaseDialog` (which extends `DialogFragment` and implements `BaseController`)
- Package: `com.yy.libcommon`

**Fields (all instance unless noted):**

| Field | Type | Visibility | Line |
|---|---|---|---|
| `mRootView` | `ViewGroup` | private | 20 |
| `mTitleTextView` | `TextView` | private | 22 |
| `mDetailsTextView` | `TextView` | private | 23 |
| `mAcceptButton` | `Button` | private | 24 |
| `mDeclineButton` | `Button` | private | 25 |
| `mTitle` | `String` | private | 27 |
| `mContent` | `String` | private | 28 |
| `mAcceptButtonText` | `String` | private | 29 |
| `mDeclineButtonText` | `String` | private | 30 |
| `countDownTimer` | `CountDownTimer` | **private static** | 31 |
| `mCallback` | `Callback` | private | 32 |

**Methods:**

| Method | Visibility | Line |
|---|---|---|
| `onCreateView(LayoutInflater, ViewGroup, Bundle)` | public (override) | 36 |
| `newInstance(String, String, String, String, int, Callback)` | public static | 45 |
| `onActivityCreated(Bundle)` | public (override) | 88 |
| `init()` | public | 95 |
| `setInitialValues()` | private | 107 |
| `setListeners()` | private | 134 |

**Interface defined within file:**

| Interface | Methods | Line |
|---|---|---|
| `Callback` | `onAcceptPress()`, `onDeclinePress()`, `onTimeOutDialog()` | 159–167 |

**Constants/Enums:** None.

---

## Step 2 & 3: Findings

---

### A11-1 — CRITICAL: Static `CountDownTimer` field causes cross-instance leakage and timer cancellation race condition

**File:** `YesNoDialog.java`, line 31, 70, 140, 150

**Evidence:**
```java
private static CountDownTimer countDownTimer;
```
`countDownTimer` is declared `static`. `newInstance()` assigns a new timer to this static field each time it is called. If two `YesNoDialog` instances are shown in the same process (even sequentially), the second call to `newInstance()` silently overwrites the reference held by the first instance. The first dialog then loses the ability to cancel its own timer — the timer continues running against the first callback — and the second dialog gets a reference to a timer that will fire the wrong callback.

Additionally, the timer's `onFinish()` callback (line 77) fires `fragment.mCallback.onTimeOutDialog()`, capturing `fragment` from the enclosing `newInstance()` call. If the fragment is destroyed before the timer fires, this is an unguarded callback into a stale object, which can produce NPE or incorrect state transitions.

This design is fundamentally unsafe. The timer should be an instance field.

---

### A11-2 — HIGH: `onCreateView` incorrectly calls `super.onCreate()` instead of `super.onCreateView()`

**File:** `YesNoDialog.java`, line 37

**Evidence:**
```java
@Override
public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);  // <-- wrong lifecycle method
    ...
}
```
`onCreateView` overrides the Fragment lifecycle method for view creation, but it calls `super.onCreate(savedInstanceState)` — the activity/fragment initialization lifecycle method — instead of `super.onCreateView(inflater, container, savedInstanceState)`. This is an incorrect lifecycle call. `BaseDialog` does not override `onCreateView`, so the intended base-class view-creation setup (if any future implementor adds it) will never be invoked. The current behaviour accidentally avoids a crash only because neither `DialogFragment.onCreateView` nor `BaseDialog.onCreateView` performs any mandatory actions that YesNoDialog depends on. This is fragile and incorrect.

---

### A11-3 — HIGH: `init()` is public but should be private — leaky abstraction

**File:** `YesNoDialog.java`, line 95

**Evidence:**
```java
public void init(){
    getDialog().getWindow().setLayout(...);
    mTitleTextView = (TextView) mRootView.findViewById(...);
    ...
}
```
`init()` directly manipulates internal view references and the dialog window layout. It is called only once, from `onActivityCreated()`, and has no semantic contract that external callers should depend on. Making it `public` exposes internal setup details as part of the class's API, allowing callers to re-run view wiring at an arbitrary time (potentially against a null window before the dialog is shown, causing NPE on `getDialog().getWindow()`). It should be `private`.

---

### A11-4 — HIGH: No null-guard on `mCallback` before invoking it in `setListeners()`

**File:** `YesNoDialog.java`, lines 139, 149

**Evidence:**
```java
mAcceptButton.setOnClickListener(new View.OnClickListener() {
    @Override
    public void onClick(View v) {
        mCallback.onAcceptPress();   // mCallback may be null
        ...
    }
});
```
`mCallback` is set in `newInstance()` only if the `callback` argument is non-null (line 66). If `newInstance()` is called with a null callback, `mCallback` remains null. Both button click listeners dereference `mCallback` without a null check, producing a `NullPointerException` at runtime when either button is pressed.

---

### A11-5 — MEDIUM: `mRootView` is declared twice — shadowing the parent class field

**File:** `YesNoDialog.java`, line 20; `BaseDialog.java`, line 26

**Evidence:**

In `BaseDialog`:
```java
protected ViewGroup mRootView;
```
In `YesNoDialog`:
```java
private ViewGroup mRootView;
```
`YesNoDialog` declares its own `private ViewGroup mRootView` which shadows the `protected ViewGroup mRootView` inherited from `BaseDialog`. This means the parent's `mRootView` is never assigned and always null in `YesNoDialog`'s context. Any future code in `BaseDialog` that references `mRootView` will see null when operating on a `YesNoDialog` instance. The child should use the inherited field rather than declaring a new one.

---

### A11-6 — MEDIUM: Style inconsistency — brace placement varies across methods

**File:** `YesNoDialog.java`, multiple lines

**Evidence — opening braces on same line (K&R style):**
```java
// line 50
if (title != null){
// line 54
if (content != null){
// line 62
if (buttonDeclineText != null){
// line 66
if (callback != null){
```

**Evidence — opening braces with preceding space (consistent K&R but not aligned with):**
```java
// line 58
if (buttonAcceptText != null) {
// line 109
if (mTitle != null){
// line 115
if (mContent != null) {
// line 121
if (mAcceptButtonText != null){
// line 127
if (mDeclineButtonText != null){
```

Some `if` blocks use `){` (no space before brace) and others use `) {` (space before brace). This is inconsistent throughout the same file and deviates from standard Android/Google Java style (which requires a space before the brace).

---

### A11-7 — MEDIUM: `setListeners()` omits braces on `if` statements — style and safety issue

**File:** `YesNoDialog.java`, lines 140–141, 150–151

**Evidence:**
```java
if(countDownTimer != null)
    countDownTimer.cancel();
```
Single-statement `if` bodies without braces. This violates the Android coding style guide (always use braces) and is a known source of accidental bugs (e.g., the "goto fail" class of error). The rest of the file consistently uses braces for `if` blocks, making this doubly inconsistent.

---

### A11-8 — MEDIUM: `onTick()` is an empty method body — potential dead code / incomplete feature

**File:** `YesNoDialog.java`, lines 72–73

**Evidence:**
```java
@Override
public void onTick(long millisUntilFinished) {
}
```
`CountDownTimer.onTick()` is intentionally empty. The `Callback` interface does not expose a tick event to callers, meaning any UI countdown display (e.g., showing remaining seconds on a button) was never implemented. This is either dead code for an abandoned feature or an oversight. A comment explaining the intentional no-op would at minimum communicate intent; the more complete fix would be to use a simpler one-shot `Handler.postDelayed()` instead of a `CountDownTimer` if ticking is never needed.

---

### A11-9 — MEDIUM: Deprecated support library usage — `android.support.v4.app.DialogFragment`

**File:** `YesNoDialog.java`, line 5 (via import of `BaseDialog` which imports line 7 of `BaseDialog.java`)

**Evidence:**
```java
import android.support.v4.app.DialogFragment;
```
The `android.support.*` Support Library was superseded by AndroidX (`androidx.fragment.app.DialogFragment`). Google ended active development of the Support Library in 2018. Using `android.support.v4.app.DialogFragment` is a deprecated API that cannot be mixed with AndroidX dependencies in the same project without the Jetifier flag. This affects the entire `LibCommon` module.

---

### A11-10 — LOW: `Callback` interface methods unnecessarily declare `public` modifier

**File:** `YesNoDialog.java`, lines 161–165

**Evidence:**
```java
public interface Callback{
    public void onAcceptPress();
    public void onDeclinePress();
    public void onTimeOutDialog();
}
```
Interface methods are implicitly `public abstract`. Explicitly writing `public` is redundant, generates an IDE warning in modern tooling, and is inconsistent with modern Java style (Java 8+ idioms, Android Lint). This is a style/cleanliness issue.

---

### A11-11 — LOW: `newInstance()` silently ignores null parameters rather than failing fast

**File:** `YesNoDialog.java`, lines 50–64

**Evidence:**
```java
if (title != null){
    fragment.mTitle = title;
}
// (no else — field stays null)
```
All four string parameters (`title`, `content`, `buttonAcceptText`, `buttonDeclineText`) are silently ignored when null, leaving the corresponding fields null. `setInitialValues()` then handles nulls by setting empty text. This silent-ignore pattern means callers get no feedback when they accidentally pass null for required parameters. A more defensive design would either document that null is a supported no-op or throw `IllegalArgumentException` for params that should not be null.

---

### A11-12 — LOW: `setInitialValues()` — inconsistent null fallback: `setText("")` vs `setHint("")`

**File:** `YesNoDialog.java`, lines 112, 118

**Evidence:**
```java
if (mTitle != null){
    mTitleTextView.setText(mTitle);
} else {
    mTitleTextView.setText("");      // sets text to empty string
}

if (mContent != null) {
    mDetailsTextView.setText(mContent);
} else {
    mDetailsTextView.setHint("");    // sets hint, not text
}
```
When `mTitle` is null, the title TextView is set to an empty string via `setText("")`. When `mContent` is null, the details TextView is given an empty hint via `setHint("")` rather than `setText("")`. This is inconsistent: neither the empty text nor the empty hint serves a functional purpose, but mixing the approaches is confusing and may produce different visual results depending on the view's existing state.

---

## Summary Table

| ID | Severity | Description |
|---|---|---|
| A11-1 | CRITICAL | Static `CountDownTimer` causes cross-instance timer leakage and stale callback risk |
| A11-2 | HIGH | `onCreateView` calls `super.onCreate()` instead of `super.onCreateView()` |
| A11-3 | HIGH | `init()` is `public` despite being an internal setup method (leaky abstraction) |
| A11-4 | HIGH | `mCallback` dereferenced in click listeners without null guard — NPE risk |
| A11-5 | MEDIUM | `mRootView` shadows parent class `protected` field in `BaseDialog` |
| A11-6 | MEDIUM | Inconsistent brace placement style throughout the file |
| A11-7 | MEDIUM | Missing braces on single-statement `if` blocks in `setListeners()` |
| A11-8 | MEDIUM | Empty `onTick()` body — incomplete feature or unexplained no-op |
| A11-9 | MEDIUM | Deprecated `android.support.v4` library instead of AndroidX |
| A11-10 | LOW | Redundant `public` modifier on `Callback` interface methods |
| A11-11 | LOW | Silent null-ignore for `newInstance()` string parameters instead of fail-fast |
| A11-12 | LOW | Inconsistent null fallback: `setText("")` for title vs `setHint("")` for content |
