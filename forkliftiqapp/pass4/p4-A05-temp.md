# Pass 4 – Code Quality Audit
**Agent:** A05
**Audit Run:** 2026-02-26-01
**Date:** 2026-02-27
**Files Reviewed:**
1. `LibCommon/src/main/java/com/yy/libcommon/Font/AMEditText.java`
2. `LibCommon/src/main/java/com/yy/libcommon/Font/AMRadioButton.java`
3. `LibCommon/src/main/java/com/yy/libcommon/Font/AMTextView.java`

**Supporting file read for context (not audited):**
- `LibCommon/src/main/java/com/yy/libcommon/Font/FontCache.java`

---

## Step 1: Reading Evidence

### File 1 — AMEditText.java

**Class:** `AMEditText extends EditText`
**Package:** `com.yy.libcommon.Font`

**Methods (exhaustive):**
| Line | Method |
|------|--------|
| 17 | `AMEditText(Context context)` — constructor |
| 23 | `AMEditText(Context context, AttributeSet attrs)` — constructor |
| 29 | `AMEditText(Context context, AttributeSet attrs, int defStyle)` — constructor |
| 36 | `private void applyCustomFont(Context context, AttributeSet attrs)` |

**Types/Constants/Enums/Interfaces defined:** None beyond the class itself.

**Imports used:**
- `android.content.Context`
- `android.content.res.TypedArray`
- `android.graphics.Typeface`
- `android.util.AttributeSet`
- `android.widget.EditText`
- `com.yy.libcommon.R`

---

### File 2 — AMRadioButton.java

**Class:** `AMRadioButton extends RadioButton`
**Package:** `com.yy.libcommon.Font`

**Methods (exhaustive):**
| Line | Method |
|------|--------|
| 18 | `AMRadioButton(Context context)` — constructor |
| 24 | `AMRadioButton(Context context, AttributeSet attrs)` — constructor |
| 30 | `AMRadioButton(Context context, AttributeSet attrs, int defStyle)` — constructor |
| 37 | `private void applyCustomFont(Context context, AttributeSet attrs)` |

**Types/Constants/Enums/Interfaces defined:** None beyond the class itself.

**Imports used:**
- `android.content.Context`
- `android.content.res.TypedArray`
- `android.graphics.Typeface`
- `android.util.AttributeSet`
- `android.widget.EditText`  ← unused import (class extends RadioButton)
- `android.widget.RadioButton`
- `com.yy.libcommon.R`

---

### File 3 — AMTextView.java

**Class:** `AMTextView extends TextView`
**Package:** `com.yy.libcommon.Font`

**Methods (exhaustive):**
| Line | Method |
|------|--------|
| 17 | `AMTextView(Context context)` — constructor |
| 23 | `AMTextView(Context context, AttributeSet attrs)` — constructor |
| 29 | `AMTextView(Context context, AttributeSet attrs, int defStyle)` — constructor |
| 36 | `private void applyCustomFont(Context context, AttributeSet attrs)` |

**Types/Constants/Enums/Interfaces defined:** None beyond the class itself.

**Imports used:**
- `android.content.Context`
- `android.content.res.TypedArray`
- `android.graphics.Typeface`
- `android.util.AttributeSet`
- `android.widget.TextView`
- `com.yy.libcommon.R`

---

### Supporting Context — FontCache.java (read for context only)

**Class:** `FontCache`

**Methods:**
| Line | Method |
|------|--------|
| 16 | `public static Typeface getTypeface(String fontname, Context context)` |
| 32 | `public static Typeface getTypeFace(Context context, String ttf)` |

Note: Two methods with near-identical names (`getTypeface` vs `getTypeFace`) taking parameters in opposite orders. This is relevant to the callers under audit.

---

## Step 2 & 3: Findings

---

### A05-1 — HIGH: TypedArray resource leak in all three `applyCustomFont` methods

**Files:**
- `AMEditText.java` line 42
- `AMRadioButton.java` line 43
- `AMTextView.java` line 42

**Detail:**
In all three classes, `getContext().obtainStyledAttributes(...)` returns a `TypedArray` that is stored in local variable `a` but is never recycled via `a.recycle()`. The Android framework explicitly requires that every `TypedArray` obtained via `obtainStyledAttributes` be recycled after use; failure to do so leaks a native `StyledAttributes` object for the lifetime of the process. This is flagged as a lint error (`ResourceType`) and manifests as a build warning in all three files.

```java
// AMEditText.java, lines 42–45
TypedArray a = getContext().obtainStyledAttributes(attrs, R.styleable.AMTextView);
ttf = a.getString(R.styleable.AMTextView_ttf_type);
typeface = FontCache.getTypeFace(getContext(), ttf);
// a.recycle() is never called
```

The same pattern appears identically in `AMRadioButton.java` and `AMTextView.java`.

---

### A05-2 — HIGH: Inconsistent default font fallback between `AMTextView` and the other two widget classes

**Files:**
- `AMTextView.java` lines 47–49
- `AMEditText.java` lines 46–48
- `AMRadioButton.java` lines 47–49

**Detail:**
`AMTextView.applyCustomFont` applies an explicit default font (`"medium"` / `HelveticaNeue_Medium.ttf`) when `attrs` is null or the `ttf_type` attribute resolves to a null typeface (lines 47–49). `AMEditText` and `AMRadioButton` do not — they silently leave the system default typeface in place when the attribute is absent or resolves to null. This is a behavioural inconsistency across three sibling classes intended to provide uniform custom-font support. Whether the fallback to `"medium"` is correct for all three widget types, the divergence is undocumented and is likely to cause subtle visual regressions.

```java
// AMTextView.java — has fallback
if(null == typeface){
    typeface = FontCache.getTypeFace(getContext(),"medium");
}

// AMEditText.java — no fallback (silently uses system font)
// AMRadioButton.java — no fallback (silently uses system font)
```

---

### A05-3 — MEDIUM: Unused import `android.widget.EditText` in AMRadioButton.java

**File:** `AMRadioButton.java` line 7

**Detail:**
`AMRadioButton` extends `RadioButton`, not `EditText`. The import of `android.widget.EditText` at line 7 is a leftover copy-paste artifact — the class was evidently created by duplicating `AMEditText.java`. It serves no purpose and will generate a build warning (`unused import`).

```java
import android.widget.EditText;   // line 7 — unused, class extends RadioButton
import android.widget.RadioButton; // line 8 — correct
```

---

### A05-4 — MEDIUM: Style inconsistency — all three `applyCustomFont` methods are identical except for the fallback difference, but are not shared or factored out

**Files:** All three

**Detail:**
The three `applyCustomFont` implementations are copy-pasted near-verbatim across `AMEditText`, `AMRadioButton`, and `AMTextView`. The only semantic difference is the default-font fallback in `AMTextView` (see A05-2). Because there is no shared base class or utility extracted for this logic, any future font-loading changes must be applied three times. Duplicated code increases the risk of the implementations drifting apart (as they already have, per A05-2).

The common pattern repeated verbatim in all three files:
```java
TypedArray a = getContext().obtainStyledAttributes(attrs, R.styleable.AMTextView);
ttf = a.getString(R.styleable.AMTextView_ttf_type);
typeface = FontCache.getTypeFace(getContext(), ttf);
```

---

### A05-5 — MEDIUM: `R.styleable.AMTextView` used in non-AMTextView classes — leaky abstraction / incorrect styleable reference

**Files:**
- `AMEditText.java` lines 42–43
- `AMRadioButton.java` lines 43–44

**Detail:**
Both `AMEditText` and `AMRadioButton` obtain styled attributes using `R.styleable.AMTextView` and `R.styleable.AMTextView_ttf_type`. These are the styleable names belonging to `AMTextView`, not the calling class. While this works at runtime (they share the same XML attribute), it creates a tight coupling: `AMEditText` and `AMRadioButton` are each explicitly dependent on the `AMTextView` styleable declaration in `attrs.xml`. If that declaration is renamed or removed, the other two classes break silently. Each class should declare and use its own styleable, or a shared common styleable name should be used instead.

---

### A05-6 — LOW: Unnecessary `context` parameter passed to `applyCustomFont` — parameter is never used directly

**Files:** All three

**Detail:**
In all three classes, `applyCustomFont(Context context, AttributeSet attrs)` receives a `context` parameter, but the method body uses `getContext()` exclusively rather than the passed-in `context`. The parameter is therefore dead weight. This is not a correctness issue (both should yield the same object for a View), but it misleads readers into thinking the passed context differs from `getContext()`, and it propagates through all three copies of the method.

```java
private void applyCustomFont(Context context, AttributeSet attrs) {
    // 'context' parameter is never read; getContext() is used throughout
    TypedArray a = getContext().obtainStyledAttributes(attrs, R.styleable.AMTextView);
    typeface = FontCache.getTypeFace(getContext(), ttf);
}
```

---

### A05-7 — LOW: Missing space after comma in constructor calls to `applyCustomFont`

**Files:** All three, constructors at lines 20, 26, 32 (AMEditText); 21, 27, 33 (AMRadioButton); 20, 26, 32 (AMTextView)

**Detail:**
All constructor bodies call `applyCustomFont(context,null)` and `applyCustomFont(context,attrs)` without a space after the comma. This is a minor style inconsistency with standard Java/Android conventions (`context, null`). It is a cosmetic issue but is consistent across all three files, indicating it was a project-level style choice or more likely a copy-paste artifact.

---

### A05-8 — LOW: Stale author-comment / creation date in file headers

**Files:** All three (`AMEditText.java` line 13, `AMRadioButton.java` line 13, `AMTextView.java` line 13)

**Detail:**
All three files carry a `/** Created by steve.yang on 16/11/16. */` Javadoc-style comment. These comments are not Javadoc (the class has no further Javadoc), serve no tooling purpose, and have not been updated to reflect any subsequent changes. They add no value and are considered stale metadata. Minor, but consistently present across the group.

---

### A05-9 — INFO: Trailing blank lines at end of files

**Files:**
- `AMEditText.java` lines 53–56 (3 blank lines after closing brace)
- `AMRadioButton.java` lines 54–57 (3 blank lines after closing brace)
- `AMTextView.java` lines 57–59 (2 blank lines after closing brace)

**Detail:**
All three files have multiple trailing blank lines beyond the closing class brace. Standard Java convention and Android lint tools expect at most one trailing newline. Minor style issue.

---

## Summary Table

| ID | Severity | File(s) | Description |
|----|----------|---------|-------------|
| A05-1 | HIGH | All three | `TypedArray` from `obtainStyledAttributes` is never recycled — resource leak |
| A05-2 | HIGH | AMTextView vs AMEditText/AMRadioButton | Inconsistent default font fallback — AMTextView falls back to "medium", others do not |
| A05-3 | MEDIUM | AMRadioButton.java | Unused import `android.widget.EditText` — copy-paste artifact |
| A05-4 | MEDIUM | All three | Near-identical `applyCustomFont` logic copy-pasted across three classes — not factored out |
| A05-5 | MEDIUM | AMEditText, AMRadioButton | Use `R.styleable.AMTextView` in non-AMTextView classes — tight coupling / incorrect styleable |
| A05-6 | LOW | All three | `context` parameter in `applyCustomFont` is never used; `getContext()` used instead |
| A05-7 | LOW | All three | Missing space after comma in `applyCustomFont(context,null)` calls |
| A05-8 | LOW | All three | Stale `Created by` header comments — no Javadoc content, not maintained |
| A05-9 | INFO | All three | Multiple trailing blank lines at end of each file |
