# Pass 4 – Code Quality Audit
**Audit run:** 2026-02-26-01
**Agent:** A53
**Date:** 2026-02-27

---

## Section 1: Reading Evidence

### File 1 – ActionClearActivity.java
**Path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/ActionClearActivity.java`
**Class:** `ActionClearActivity extends FleetActivity`

| Method | Line |
|--------|------|
| `onCreate(Bundle)` | 11 |

Types/constants/enums defined: none.
Imports: `android.os.Bundle`, `R`, `FleetActivity`, `SetupEmailFragment`.

---

### File 2 – DashboardActivity.java
**Path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/DashboardActivity.java`
**Class:** `DashboardActivity extends FleetActivity`

| Method | Line |
|--------|------|
| `onCreate(Bundle)` | 14 |
| `onResume()` | 22 |

Types/constants/enums defined: none.
Imports: `android.os.Bundle`, `R`, `ShockEventService`, `CacheService`, `SyncService`, `MyApplication`, `FleetActivity`, `DashboardFragment`.

---

### File 3 – DriverStatsActivity.java
**Path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/DriverStatsActivity.java`
**Class:** `DriverStatsActivity extends FleetActivity`

| Method | Line |
|--------|------|
| `onCreate(Bundle)` | 10 |

Types/constants/enums defined: none.
Imports: `android.os.Bundle`, `R`, `FleetActivity`, `DriverStatsFragment1`.

---

## Section 2 & 3: Findings

---

### A53-1 — HIGH — Null-pointer dereference on unvalidated Intent extra (ActionClearActivity.java, line 17–18)

**File:** `ActionClearActivity.java`

```java
String action = getIntent().getStringExtra("action");
if (action.equals("setup")) {
```

`getStringExtra` returns `null` when the extra is absent. Calling `.equals(...)` directly on a potentially-null `String` will throw a `NullPointerException` at runtime with no guard. The companion class `ActionActivity.java` (line 18–19) has the identical defect.

This is a CRITICAL run-time crash path: any caller that omits the `"action"` extra, or any deep-link / notification intent that arrives without it, will crash the activity silently.

**Recommended fix:** use `"setup".equals(action)` (Yoda condition) or an explicit null check before comparison.

---

### A53-2 — HIGH — Duplicate code / near-identical class with no distinguishing behaviour (ActionClearActivity.java vs. ActionActivity.java)

**Files:** `ActionClearActivity.java`, `ActionActivity.java`

`ActionClearActivity` handles only the `"setup"` action via `SetupEmailFragment`.
`ActionActivity` handles both `"setup"` and `"report"` actions.
`ActionClearActivity` appears to be an older, cut-down copy of `ActionActivity` that was never removed. Both classes expose the same `"action"` extra protocol, call the same fragment for `"setup"`, and share the same null-dereference defect. Maintaining two near-identical entry points creates confusion over which one callers should use, and bugs must be fixed twice.

---

### A53-3 — HIGH — Unused/dead private method `showDeviceDisconnectedDialog` in base class triggered by commented-out code (FleetActivity.java, lines 179–184 and 187–215)

**Context for file:** Referenced from `FleetActivity.java`, which is the direct base of all three audited activities.

In `FleetActivity.onBleDeviceDisconnected` (lines 179–184) the retry/branch logic that would call `showDeviceDisconnectedDialog` has been entirely commented out:

```java
//        int connectionRetry = Objects.requireNonNull(SessionDb.readRunningSessionDb()).incrementConnectionRetry();
//        if (connectionRetry < 3) {
            onReconnectDevice(5000);
//        } else {
//            showDeviceDisconnectedDialog();
//        }
```

As a result, `showDeviceDisconnectedDialog()` (lines 187–215) is now unreachable dead code — it can never be called. The method is `private`, so the compiler cannot warn about it being unused. This is significant because the method contains meaningful UX behaviour (a yes/no dialog allowing the user to abort or reconnect). The retry counter `incrementConnectionRetry` is also completely disabled.

---

### A53-4 — MEDIUM — Unused imports in DashboardActivity.java (lines 5–7)

**File:** `DashboardActivity.java`

```java
import au.com.collectiveintelligence.fleetiq360.WebService.BLE.ShockEventService;
import au.com.collectiveintelligence.fleetiq360.model.CacheService;
import au.com.collectiveintelligence.fleetiq360.model.SyncService;
```

`ShockEventService`, `CacheService`, and `SyncService` are imported but their references appear only inside the `onResume` anonymous `Runnable`. While they are technically used inside that anonymous class, the issue is that `SyncService.startService()` is *already* called by `FleetActivity.onCreate` (the superclass, line 72 of `FleetActivity.java`) before `DashboardActivity.onResume` fires. Calling `SyncService.startService()` again in `DashboardActivity.onResume` is redundant and reflects a misunderstanding of the base-class lifecycle.

---

### A53-5 — MEDIUM — Service restart on every `onResume` without lifecycle awareness (DashboardActivity.java, lines 22–33)

**File:** `DashboardActivity.java`

```java
@Override
protected void onResume() {
    super.onResume();

    MyApplication.runLater(new Runnable() {
        @Override
        public void run() {
            ShockEventService.startService();
            CacheService.startService();
            SyncService.startService();
        }
    }, 2000);
}
```

`onResume` fires every time the activity returns to the foreground (e.g., after the user dismisses a dialog, returns from a sub-activity, or the screen unlocks). Each invocation schedules a 2-second-delayed call to all three `startService` methods. If the user repeatedly navigates away and back, multiple delayed runnables will queue up on the handler, causing repeated unnecessary service starts. There is no corresponding cancellation in `onPause`. The other activities (e.g., `ActionActivity`, `DriversActivity`) do not follow this pattern; `DashboardActivity` is the only one with custom `onResume` logic that re-fires services.

---

### A53-6 — MEDIUM — Anonymous `Runnable` instead of lambda (DashboardActivity.java, lines 25–32)

**File:** `DashboardActivity.java`

```java
MyApplication.runLater(new Runnable() {
    @Override
    public void run() {
        ShockEventService.startService();
        CacheService.startService();
        SyncService.startService();
    }
}, 2000);
```

The project targets a Java version that supports lambdas (other files in the codebase use lambdas in comparable contexts). The verbose anonymous class style here is inconsistent with the rest of the codebase and adds unnecessary boilerplate.

---

### A53-7 — MEDIUM — `DriverStatsFragment1` numeric suffix implies incomplete refactor / dead fragment variants

**File:** `DriverStatsActivity.java` (line 16); context from `DriverStatsFragment1.java` (line 125–126)

`DriverStatsActivity` loads `DriverStatsFragment1`. Three fragment classes exist: `DriverStatsFragment1`, `DriverStatsFragment2`, and `DriverStatsFragment3`. Inside `DriverStatsFragment1.onRightButton`, `DriverStatsFragment3` is loaded directly — `DriverStatsFragment2` is skipped entirely from this navigation path. The numeric suffix naming provides no semantic information about the purpose of each screen. It is unclear whether `DriverStatsFragment2` is reachable from any navigation path or is dead/unreferenced code. This warrants verification.

---

### A53-8 — LOW — Style inconsistency: `initKeyboard()` called in two of three activity `onCreate` methods but not in `DashboardActivity`

**Files:** `ActionClearActivity.java` (line 15), `DriverStatsActivity.java` (line 14), `DashboardActivity.java` (no call)

`ActionClearActivity` and `DriverStatsActivity` both call `initKeyboard()` after `setContentView`. `DashboardActivity` does not. This is likely intentional (Dashboard may not require keyboard dismissal), but the pattern is undocumented and may catch future maintainers off guard when keyboard behaviour differs between screens.

---

### A53-9 — LOW — Stale/large commented-out code block in base class `FleetActivity.java` (multiple locations)

**File:** `FleetActivity.java` (referenced as base of all three audited activities)

Multiple independent blocks of commented-out code exist throughout `FleetActivity`:

- Line 179–184: entire retry-counter branch (see A53-3 above).
- Line 255: `//showProgress(null, "Connecting...");`
- Line 263: `//                showProgress(null, "Please wait...");`
- Lines 293–294: `//                    hideProgress();`
- Lines 304–305: `//                    hideProgress();`
- Lines 310–312: `//                        hideProgress();`
- Lines 337: `//                hideProgress();`
- Lines 359, 363: `//                hideProgress();` (×2 in `onStopSessionByUser`)

These remnants suggest that a `showProgress`/`hideProgress` mechanism was recently replaced with a `ProgressDialog`-based approach but the old call sites were commented out rather than deleted. They add noise and make it harder to understand the current control flow.

---

### A53-10 — LOW — `ProgressDialog` usage is deprecated API (FleetActivity.java, lines 256–268)

**File:** `FleetActivity.java` (base of all audited activities)

```java
final ProgressDialog cancelDialog = new ProgressDialog(this);
```

`android.app.ProgressDialog` has been deprecated since API level 26 (Android 8.0 / Oreo). Using it will generate build warnings on modern SDK targets. The deprecation of `showProgress`/`hideProgress` (commented out) and the in-lined `ProgressDialog` suggests an incomplete migration away from the deprecated class.

---

### A53-11 — LOW — Inconsistent import ordering in DashboardActivity.java

**File:** `DashboardActivity.java` (lines 3–10)

```java
import android.os.Bundle;
import au.com.collectiveintelligence.fleetiq360.R;
import au.com.collectiveintelligence.fleetiq360.WebService.BLE.ShockEventService;
import au.com.collectiveintelligence.fleetiq360.model.CacheService;
import au.com.collectiveintelligence.fleetiq360.model.SyncService;
import au.com.collectiveintelligence.fleetiq360.ui.application.MyApplication;
import au.com.collectiveintelligence.fleetiq360.ui.common.FleetActivity;
import au.com.collectiveintelligence.fleetiq360.ui.fragment.DashboardFragment;
```

There are no blank-line separators between the `android.*` block and the project (`au.com.*`) blocks. Other activity files (`ActionClearActivity`, `DriverStatsActivity`) consistently have a blank line between the Android SDK imports and the project imports. This is a minor style inconsistency.

---

## Summary Table

| ID | Severity | File | Description |
|----|----------|------|-------------|
| A53-1 | HIGH | ActionClearActivity.java:17–18 | NPE on null Intent extra — `action.equals(...)` without null guard |
| A53-2 | HIGH | ActionClearActivity.java / ActionActivity.java | Near-duplicate classes; `ActionClearActivity` appears to be dead/superseded copy |
| A53-3 | HIGH | FleetActivity.java:179–215 | `showDeviceDisconnectedDialog` is unreachable dead code; retry logic fully commented out |
| A53-4 | MEDIUM | DashboardActivity.java:5–7 | `SyncService.startService()` called redundantly — already invoked in base class `onCreate` |
| A53-5 | MEDIUM | DashboardActivity.java:22–33 | Services restarted on every `onResume` with no cancellation guard in `onPause` |
| A53-6 | MEDIUM | DashboardActivity.java:25–32 | Anonymous `Runnable` instead of lambda — inconsistent with project style |
| A53-7 | MEDIUM | DriverStatsActivity.java:16 | Numeric-suffix fragment naming obscures purpose; `DriverStatsFragment2` may be unreachable |
| A53-8 | LOW | ActionClearActivity/DriverStatsActivity/DashboardActivity | `initKeyboard()` called inconsistently across the three activities |
| A53-9 | LOW | FleetActivity.java (multiple lines) | Large volume of stale commented-out code from superseded progress mechanism |
| A53-10 | LOW | FleetActivity.java:256 | Deprecated `android.app.ProgressDialog` API usage |
| A53-11 | LOW | DashboardActivity.java:3–10 | Import block missing blank-line separator between Android SDK and project imports |
