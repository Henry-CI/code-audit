# Pass 4 – Code Quality Audit
**Agent:** A56
**Audit run:** 2026-02-26-01
**Files assigned:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/ProfileActivity.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/SessionActivity.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/SignupActivity.java`

---

## Step 1: Reading Evidence

### File 1 — ProfileActivity.java

**Class:** `ProfileActivity` (extends `FleetActivity`)

**Methods:**

| Method | Line |
|--------|------|
| `onCreate(Bundle)` | 11 |

**Types / Constants / Interfaces defined:** None.

**Summary:** Minimal shell activity. Inflates `R.layout.activity_profile` and immediately delegates to `ProfileFragment` via `showFragmentWithoutStack`.

---

### File 2 — SessionActivity.java

**Class:** `SessionActivity` (extends `FleetActivity`)

**Methods:**

| Method | Line |
|--------|------|
| `onCreate(Bundle)` | 24 |
| `onBackPressed()` | 76 |
| `onExitSessionActivity()` | 90 |
| `abortSession(SessionResult)` | 118 |

**Anonymous inner classes / Runnables defined inline:**
- `Runnable runnableToJob` (line 50) — navigates to `JobsFragment`
- `Runnable runnableToPreStart` (line 58) — navigates to `EquipmentPrestartFragment`
- `YesNoDialog.Callback` in `onExitSessionActivity()` (lines 97–113)
- `AbortSessionCallback` in `abortSession()` (lines 126–138)
- `YesNoDialog.Callback` in `abortSession()` / `onSessionStopFailed` (lines 144–158)

**Imports:**
- `android.support.v4.app.Fragment` (line 4) — old Support Library

**Types / Constants / Interfaces defined:** None within this file (references `FleetActivity.AbortSessionCallback` from parent).

---

### File 3 — SignupActivity.java

**Class:** `SignupActivity` (extends `FleetActivity`)

**Methods:**

| Method | Line |
|--------|------|
| `onCreate(Bundle)` | 10 |

**Types / Constants / Interfaces defined:** None.

**Summary:** Minimal shell activity. Inflates `R.layout.activity_signup` and delegates to `SignupFragment` via `showFragmentWithoutStack`.

---

## Step 2 & 3: Findings

---

### A56-1 — HIGH — Logic Bug: Early Return Leaves Activity in Blank State

**File:** `SessionActivity.java`, line 38–40

```java
if (MyCommonValue.currentEquipmentItem == null) {
    MyCommonValue.currentEquipmentItem = SessionDb.readRunningEquipmentItem();
    return;   // <-- returns without showing any fragment or finishing
}
```

When `MyCommonValue.currentEquipmentItem` is null at the time `onCreate` runs, the code reads the equipment item from the database and then immediately returns. No fragment is shown and `finish()` is not called. The activity is left in a fully blank, non-interactive state. The pattern on line 32–35 correctly calls `finish()` when the session itself is missing; this branch inconsistently does not. This is a correctness defect disguised as a defensive null-check: the intent appears to be to populate the global then continue processing, but the `return` statement prevents any further navigation.

---

### A56-2 — HIGH — Public Mutable Field Used as Fragment Configuration (`autoConnect`)

**File:** `SessionActivity.java`, line 47; cross-reference `EquipmentConnectFragment.java`, line 44

```java
// SessionActivity.java
EquipmentConnectFragment fragment = new EquipmentConnectFragment();
fragment.autoConnect = true;
showFragmentWithoutStack(..., fragment);
```

```java
// EquipmentConnectFragment.java
public boolean autoConnect = false;
```

Fragment configuration is being passed via a raw `public` instance field instead of a `Bundle` argument (the standard Android idiom). This leaks internal state management into callers, breaks the Fragment contract (arguments set via `setArguments()` survive process death and recreation; bare field assignments do not), and couples `SessionActivity` directly to the internal implementation of `EquipmentConnectFragment`.

---

### A56-3 — MEDIUM — Deprecated Support Library Import (`android.support.v4.app.Fragment`)

**File:** `SessionActivity.java`, line 4

```java
import android.support.v4.app.Fragment;
```

The project's other activity files (`ProfileActivity`, `SignupActivity`) do not import any Support Library classes directly, and AndroidX has been the replacement since 2018. The `android.support.*` namespace is fully deprecated and unsupported on modern `compileSdkVersion` targets. At minimum this generates a build warning; on newer Gradle/AGP versions with `android.enableJetifier=false` it can cause build failures. The inconsistency is also a style issue: the other two assigned files have no such import.

---

### A56-4 — MEDIUM — Hardcoded String Literals in Dialog Construction

**File:** `SessionActivity.java`, lines 91–95 and 143–144

```java
// onExitSessionActivity()
YesNoDialog.newInstance(
    "WARNING!",          // hardcoded
    ...
    getString(R.string.proceed),
    getString(R.string.cancel),
    ...

// abortSession() / onSessionStopFailed
YesNoDialog.newInstance("Error!", getString(R.string.session_abort_retry),
    "Retry", "Exit", 0, ...
```

Several strings passed to `YesNoDialog.newInstance` are hardcoded literals (`"WARNING!"`, `"Error!"`, `"Retry"`, `"Exit"`) while adjacent strings are correctly resolved from resources (`getString(R.string.proceed)`, `getString(R.string.cancel)`). This is inconsistent style within the same method calls, prevents localisation, and would generate lint warnings under `HardcodedText`.

---

### A56-5 — MEDIUM — `onExitSessionActivity()` is `public` — Leaky Abstraction

**File:** `SessionActivity.java`, line 90

```java
public void onExitSessionActivity() { ... }
```

This method exists solely to be called from `onBackPressed()` and the inner `Runnable` callbacks within `SessionActivity` itself. Declaring it `public` exposes session-abort logic to any external caller (e.g., other activities or fragments that obtain a reference via a cast). The method triggers a `YesNoDialog` and starts an abort flow; accidental external invocation would be destructive. It should be `private` or at most package-private. Contrast with `abortSession()` (line 118), which is `public` for a documented reason (called from inner callbacks), but `onExitSessionActivity()` has no such requirement.

---

### A56-6 — MEDIUM — Inconsistent Fragment Container ID Between Sister Activities

**Files:** `ProfileActivity.java` line 15, `SessionActivity.java` line 48 / 53 / 61, `SignupActivity.java` line 13

```java
// ProfileActivity
showFragmentWithoutStack(R.id.fragment_container, ...);

// SessionActivity
showFragmentWithoutStack(R.id.fragment_container, ...);

// SignupActivity
showFragmentWithoutStack(R.id.login_framelayout_id, ...);
```

`SignupActivity` uses a different fragment container ID (`R.id.login_framelayout_id`) compared to the `R.id.fragment_container` used consistently by `ProfileActivity` and `SessionActivity`. If `SignupActivity` ever transitions to the same layout as the others (or a developer tries to reuse the pattern), this divergence is a latent confusion and style inconsistency. At minimum the naming is inconsistent with no documentation explaining why the signup screen uses a distinct ID name.

---

### A56-7 — LOW — `abortSession()` is `public` but `onExitSessionActivity()` Already Exists as Entry Point

**File:** `SessionActivity.java`, line 118

```java
public void abortSession(final SessionResult sessionResult) { ... }
```

`abortSession` is `public` and takes a `SessionResult` parameter that callers must construct correctly. Exposing this method publicly (and requiring the caller to pass a `SessionResult` obtained from `WebData.instance().getSessionResult()`) creates a leaky API: callers need knowledge of `WebData` internals to use it. Internally it is only called from `onExitSessionActivity()` (line 103) and recursively from the retry dialog callback (line 147). Making it `private` would not reduce functionality.

---

### A56-8 — LOW — Typo in API Method Name Propagated Throughout Codebase

**File:** `SessionActivity.java`, lines 77 and 81

```java
Fragment fragment = findFramentByTag(...);   // "Frament" missing 'g'
Fragment conFragment = findFramentByTag(...);
```

The method name `findFramentByTag` (missing the second 'g' in "Fragment") is defined in `LibCommon/FragmentInterface.java` and `BaseActivity.java` and is used in at least three locations across the codebase. While the bug is in the library and not this file, `SessionActivity` actively perpetuates the typo. This makes the API harder to discover via IDE autocomplete and is an ongoing maintenance debt. It is noted here as it directly appears in the assigned file.

---

### A56-9 — LOW — Inline `Runnable` Instead of Lambda (Java 8+ available)

**File:** `SessionActivity.java`, lines 50–64

```java
Runnable runnableToJob = new Runnable() {
    @Override
    public void run() {
        showFragmentWithoutStack(...);
    }
};

Runnable runnableToPreStart = new Runnable() {
    @Override
    public void run() {
        showFragmentWithoutStack(...);
    }
};
```

The project targets a `minSdkVersion` that supports Java 8 language features via `desugaring`. The same pattern in `abortSession()` at line 129 uses an anonymous `Runnable` for `MyApplication.runLater(...)`. Lambda syntax (`() -> showFragmentWithoutStack(...)`) would reduce boilerplate and improve readability. This is a style inconsistency if lambdas are used elsewhere in the codebase, but a low-severity finding on its own.

---

### A56-10 — INFO — `ProfileActivity` and `SignupActivity` Are Structurally Identical Shell Activities

**Files:** `ProfileActivity.java` (17 lines), `SignupActivity.java` (15 lines)

Both classes are identical in structure: override `onCreate`, call `setContentView`, then call `showFragmentWithoutStack`. Neither adds any unique behavior. This pattern is repeated across many activities in the project. It is not a defect per se but represents an opportunity to eliminate the redundant subclasses (e.g., via a generic single-fragment host activity parameterised by the fragment class). No action required for this finding.

---

## Summary Table

| ID | Severity | File | Line(s) | Issue |
|----|----------|------|---------|-------|
| A56-1 | HIGH | SessionActivity.java | 38–40 | Early `return` after null-check leaves activity blank (no fragment shown, no finish) |
| A56-2 | HIGH | SessionActivity.java | 47 | Public mutable field used as Fragment configuration instead of `Bundle` arguments |
| A56-3 | MEDIUM | SessionActivity.java | 4 | Deprecated `android.support.v4.app.Fragment` import instead of AndroidX |
| A56-4 | MEDIUM | SessionActivity.java | 91, 143–144 | Hardcoded string literals mixed with resource-resolved strings in dialog calls |
| A56-5 | MEDIUM | SessionActivity.java | 90 | `onExitSessionActivity()` unnecessarily `public`; should be `private` |
| A56-6 | MEDIUM | SignupActivity.java | 13 | Inconsistent fragment container ID (`login_framelayout_id` vs `fragment_container`) |
| A56-7 | LOW | SessionActivity.java | 118 | `abortSession()` unnecessarily `public`; exposes session-abort API to external callers |
| A56-8 | LOW | SessionActivity.java | 77, 81 | Perpetuates `findFramentByTag` typo from base library |
| A56-9 | LOW | SessionActivity.java | 50–64 | Verbose anonymous `Runnable` where lambdas could be used |
| A56-10 | INFO | ProfileActivity.java, SignupActivity.java | — | Both are identical shell activities; potential for consolidation |
