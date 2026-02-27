# Pass 4 Code Quality — Agent A52
**Audit run:** 2026-02-26-01
**Agent:** A52
**Date:** 2026-02-27

---

## Section 1: Reading Evidence

### File 1: `app/src/main/java/au/com/collectiveintelligence/fleetiq360/session/SessionTimeouter.java`

**Class:** `SessionTimeouter` (public, no interface, no enum)

**Constants / static fields:**
- `private static SessionTimeouter instance` (line 27) — singleton backing field
- `private static HashMap<Activity, SessionTimeouterReceiver> registrations` (line 102) — static map, initialised in a static block (lines 104-106)

**Instance fields:**
- `private boolean warningDisplayed` (line 28)

**Methods (exhaustive):**

| Line | Visibility | Signature |
|------|------------|-----------|
| 30 | `public static` | `getInstance()` |
| 36 | `public` | `start(Context context)` |
| 42 | `public` | `cancel(Context context)` |
| 47 | `private` | `restart()` |
| 53 | `private` | `preEndSession()` |
| 62 | package-private | `endSession()` |
| 86 | `private` | `onSessionEnded()` |
| 108 | `public static` | `register(Activity activity)` |
| 114 | `public static` | `unregister(Activity activity)` |
| 120 | package-private | `showSessionTimeoutWarningDialog(Context context)` |
| 159 | package-private static | `showSessionTimeoutWarningDialog()` (no-arg overload) |
| 165 | `private static` | `getContext()` |

**Imports used:** `Activity`, `AlertDialog`, `Context`, `DialogInterface`, `IntentFilter`, `CountDownTimer`, `Fragment`, `Log`, `WebApi`, `WebListener`, `WebResult`, `SessionEndParameter`, `SessionEndResult`, `SessionResult`, `SessionDb`, `FleetActivity`, `FleetFragment`, `HashMap`, `Iterator`, `List`, `Locale`

---

### File 2: `app/src/main/java/au/com/collectiveintelligence/fleetiq360/session/SessionTimeouterReceiver.java`

**Class:** `SessionTimeouterReceiver` (package-private, extends `BroadcastReceiver`)

**Fields:**
- `private Context context` (line 9)

**Methods (exhaustive):**

| Line | Visibility | Signature |
|------|------------|-----------|
| 11 | package-private | `SessionTimeouterReceiver(Activity activity)` (constructor) |
| 16 | `@Override public` | `onReceive(Context context, Intent intent)` |

---

### File 3: `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/ActionActivity.java`

**Class:** `ActionActivity` (public, extends `FleetActivity`)

**Fields:** none declared beyond inheritance

**Methods (exhaustive):**

| Line | Visibility | Signature |
|------|------------|-----------|
| 12 | `@Override protected` | `onCreate(Bundle savedInstanceState)` |

**Imports used:** `Bundle`, `R`, `FleetActivity`, `SavedReportFragment`, `SetupEmailFragment`

---

## Section 2 & 3: Findings

---

### A52-1 — HIGH: Singleton `getInstance()` is not thread-safe

**File:** `SessionTimeouter.java`, lines 30-34

```java
public static SessionTimeouter getInstance() {
    if (instance == null)
        instance = new SessionTimeouter();
    return instance;
}
```

The lazy-initialisation check is not synchronised. Two threads arriving simultaneously when `instance` is `null` can each construct a separate instance, causing split state (e.g., `warningDisplayed` on one instance, `registrations` on the shared static field). The `registrations` map is also accessed from multiple contexts without synchronisation, compounding the risk.

---

### A52-2 — HIGH: `NullPointerException` risk — unguarded `getIntent().getStringExtra()` in `ActionActivity`

**File:** `ActionActivity.java`, lines 18-19

```java
String action = getIntent().getStringExtra("action");
if (action.equals("setup")) {
```

`getStringExtra()` returns `null` when the key is absent. Calling `.equals()` on a `null` reference throws `NullPointerException`. There is no null check, no default value, and no else/fallthrough handler for unknown action values. If the activity is launched without the `"action"` extra (e.g., via a deep link, notification, or test) the app will crash.

---

### A52-3 — HIGH: `CountDownTimer` in `showSessionTimeoutWarningDialog` is never explicitly cancelled on dialog dismissal via the buttons

**File:** `SessionTimeouter.java`, lines 144-156

```java
new CountDownTimer(1000 * 60 * 5, 1000) {
    @Override
    public void onTick(long millisUntilFinished) {
        if(alert.isShowing() == false)
            cancel();
    }
    @Override
    public void onFinish() {
        alert.dismiss();
        endSession();
    }
}.start();
```

When the user taps "Continue" or "Terminate", the dialog is dismissed but `CountDownTimer.cancel()` is not called. The timer detects this only on the *next* `onTick` (up to 1 second later). If the activity is destroyed between button press and the next tick, `alert.isShowing()` may still return `false` for the wrong reason, and `onFinish()` can subsequently call `endSession()` a second time after the user already chose "Continue", silently ending the session again.

---

### A52-4 — MEDIUM: Hard-coded, application-specific broadcast action string

**File:** `SessionTimeouter.java`, line 110

```java
activity.registerReceiver(receiver, new IntentFilter("MyApplication.INTENT_DISPLAYERROR"));
```

The intent action `"MyApplication.INTENT_DISPLAYERROR"` is a bare string literal. It is not declared as a constant anywhere in the assigned files, and the name "DISPLAYERROR" does not match the actual behaviour (showing a session-timeout warning). This is both a leaky abstraction (the internal broadcast protocol is hard-coded in a consumer) and a maintenance hazard — a rename in the sender will silently break the receiver. The intent filter is also registered with the system broadcast bus rather than `LocalBroadcastManager`, which the rest of the codebase uses for similar events (see `FleetActivity.onResume`).

---

### A52-5 — MEDIUM: `onSessionEnded()` only notifies fragments of the *first* registered activity

**File:** `SessionTimeouter.java`, lines 86-100

```java
Iterator<Activity> activities = registrations.keySet().iterator();
if (!activities.hasNext()) return;
Activity activity = activities.next();        // only first activity
...
for (Fragment fragment : fragments) {
    if (fragment instanceof FleetFragment)
        ((FleetFragment) fragment).onSessionEnded();
}
```

The `registrations` map may contain more than one activity (e.g., if an activity starts a child activity without unregistering). Only the first entry from the `HashMap`'s key-set iterator is used; all other activities' fragments are silently skipped. `HashMap` iteration order is not defined, so which activity is "first" is non-deterministic.

---

### A52-6 — MEDIUM: `SessionTimeouterReceiver` stores `Activity` as `Context`, preventing lifecycle-aware null checks

**File:** `SessionTimeouterReceiver.java`, lines 9-18

```java
private Context context;

SessionTimeouterReceiver(Activity activity) {
    context = activity;
}

public void onReceive(Context context, Intent intent) {
    abortBroadcast();
    SessionTimeouter.getInstance().showSessionTimeoutWarningDialog(this.context);
}
```

The stored `context` reference is an `Activity`. After `unregister` is called in `FleetActivity.onPause`, the receiver should not fire; however, if a broadcast arrives between `onPause` and the OS processing the unregistration (a race), `showSessionTimeoutWarningDialog` is called with a paused or destroyed activity context, which will crash when `AlertDialog.Builder` tries to show a dialog. Storing the reference typed as `Context` instead of `Activity` also suppresses any IDE warning that would otherwise flag the leaked activity reference.

---

### A52-7 — MEDIUM: Commented-out code — retry logic removed but left in place

**File:** `FleetActivity.java` (contextual reference for `SessionTimeouter` callers), lines 179-184:

*(Reported here because the direct caller chain flows through SessionTimeouter — included for completeness as it affects audit coverage of the session subsystem.)*

Within the session package's surrounding context (`FleetActivity.onBleDeviceDisconnected`):

```java
//        int connectionRetry = Objects.requireNonNull(SessionDb.readRunningSessionDb()).incrementConnectionRetry();
//        if (connectionRetry < 3) {
            onReconnectDevice(5000);
//        } else {
//            showDeviceDisconnectedDialog();
//        }
```

The retry-count logic was commented out, leaving unconditional infinite reconnection. The private method `showDeviceDisconnectedDialog()` (line 187) is now unreachable dead code as a result. This is reported here because `SessionTimeouter` and `FleetActivity` are tightly coupled and this dead method interacts with the session-end path.

---

### A52-8 — MEDIUM: `getContext()` can return `null`; callers in `restart()` do not guard against it

**File:** `SessionTimeouter.java`, lines 165-168 and 47-51

```java
private static Context getContext() {
    Iterator<Activity> activities = registrations.keySet().iterator();
    return activities.hasNext() ? activities.next() : null;
}

private void restart() {
    Context context = getContext();
    cancel(context);   // cancel() guards null
    start(context);    // start() calls SessionTimeoutJobService.schedule(context)
                       // schedule() guards null — safe
                       // BUT start() also calls preEndSession() unconditionally
}
```

`cancel()` and `schedule()` both guard against `null` context. However, if `registrations` is empty when `restart()` is called (e.g., all activities have been paused and unregistered just before the user taps "Continue"), the session timer is rescheduled with a null context — `SessionTimeoutJobService.schedule(null)` returns silently, leaving the session without a running timer and without any error being surfaced.

---

### A52-9 — LOW: `warningDisplayed` flag is not reset in `endSession()`

**File:** `SessionTimeouter.java`, lines 62-84

`endSession()` calls `cancel()` (which resets `warningDisplayed = false`), so the flag is technically cleared. However, the code path where `endSession()` is triggered directly from `SessionTimeoutJobService.onStartJob()` (without going through `showSessionTimeoutWarningDialog`) never sets `warningDisplayed = true`, meaning subsequent calls to `showSessionTimeoutWarningDialog` will always re-display the dialog even if one is already showing (the guard at line 121 only prevents re-display within a single dialog lifetime). The flag's semantics are therefore inconsistent across the two entry points.

---

### A52-10 — LOW: Style inconsistency — `== false` instead of `!` operator

**File:** `SessionTimeouter.java`, line 147

```java
if(alert.isShowing() == false)
```

Every other boolean check in the file uses the `!` operator (e.g., `if (!activities.hasNext())`). This single instance uses `== false`, which is inconsistent with the established style. Additionally, the `if(` has no space before the parenthesis, unlike `if (` used elsewhere.

---

### A52-11 — LOW: Package-private visibility on `endSession()` and `showSessionTimeoutWarningDialog(Context)` is an implicit API contract

**File:** `SessionTimeouter.java`, lines 62 and 120

```java
void endSession() { ... }
void showSessionTimeoutWarningDialog(Context context) { ... }
```

Both methods have no access modifier, making them package-private. `SessionTimeoutJobService` (same package) calls them directly. This is a leaky abstraction: the session-timeout trigger mechanism (the `JobService`) reaches directly into session-end logic rather than going through the public `start`/`cancel` interface. If these methods are ever made private or the package is refactored, the `JobService` call sites break silently at compile time only.

---

### A52-12 — LOW: `ActionActivity` has no handling for unknown `action` values

**File:** `ActionActivity.java`, lines 18-25

```java
String action = getIntent().getStringExtra("action");
if (action.equals("setup")) {
    ...
} else if (action.equals("report")) {
    ...
}
```

If `action` is any other non-null string, the activity displays a blank screen (an empty `activity_common` layout) with no error or user feedback. There is no `else` branch, no `finish()` call, and no log statement. This makes mis-routed intents silently produce invisible screens.

---

### A52-13 — INFO: `preEndSession()` fires on every `start()` call, including restarts

**File:** `SessionTimeouter.java`, lines 36-40 and 47-51

```java
public void start(Context context) {
    warningDisplayed = false;
    preEndSession();                  // always called
    SessionTimeoutJobService.schedule(context);
}

private void restart() {
    Context context = getContext();
    cancel(context);
    start(context);                   // calls preEndSession() again
}
```

When the user taps "Continue" in the warning dialog, `restart()` → `start()` → `preEndSession()` is called. This recalculates and overwrites `finish_time` on an already pre-ended session, which may cause the pre-end time to drift further into the future than intended on each "Continue" press. This is a logic concern rather than a pure code quality issue, but the absence of any comment explaining the intended behaviour on restart is an information gap.

---

## Summary Table

| ID | Severity | File | Description |
|----|----------|------|-------------|
| A52-1 | HIGH | SessionTimeouter.java | Non-thread-safe singleton initialisation |
| A52-2 | HIGH | ActionActivity.java | NPE on null `getStringExtra("action")` |
| A52-3 | HIGH | SessionTimeouter.java | `CountDownTimer` not cancelled on dialog button press; double `endSession()` risk |
| A52-4 | MEDIUM | SessionTimeouter.java | Hard-coded intent action string; wrong bus (system vs LocalBroadcast) |
| A52-5 | MEDIUM | SessionTimeouter.java | `onSessionEnded()` only notifies first registered activity's fragments |
| A52-6 | MEDIUM | SessionTimeouterReceiver.java | Stale activity context reference may cause dialog crash after unregister race |
| A52-7 | MEDIUM | SessionTimeouter.java (context) | Commented-out retry logic; `showDeviceDisconnectedDialog()` is dead code |
| A52-8 | MEDIUM | SessionTimeouter.java | `getContext()` returns null; `restart()` silently fails to reschedule timer |
| A52-9 | LOW | SessionTimeouter.java | `warningDisplayed` semantics inconsistent across call paths |
| A52-10 | LOW | SessionTimeouter.java | `== false` style inconsistency; missing space in `if(` |
| A52-11 | LOW | SessionTimeouter.java | Package-private methods form implicit API; leaky coupling with JobService |
| A52-12 | LOW | ActionActivity.java | Unknown `action` values produce silent blank screen |
| A52-13 | INFO | SessionTimeouter.java | `preEndSession()` called on every restart, including user-initiated "Continue" |
