# Pass 4 — Code Quality Audit
**Agent:** A67
**Audit Run:** 2026-02-26-01
**Date:** 2026-02-27

---

## Section 1: Reading Evidence

### File 1: `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/SignupFragment.java`

**Class:** `SignupFragment extends FleetFragment implements View.OnClickListener`

**Constants defined:**
| Constant | Type | Value | Line |
|---|---|---|---|
| `TYPE_DRIVER` | `private final static String` | `"DRIVER"` | 86 |
| `TYPE_COMPANY` | `private final static String` | `"COMPANY"` | 87 |

**Fields:**
| Field | Type | Visibility | Line |
|---|---|---|---|
| `activity` | `SignupActivity` | package-private | 31 |
| `firstNameET` | `EditText` | private | 32 |
| `lastNameET` | `EditText` | private | 32 |
| `emailAddressET` | `EditText` | private | 32 |
| `mobileNumET` | `EditText` | private | 32 |
| `passwordET` | `EditText` | private | 32 |
| `confirmPWET` | `EditText` | private | 32 |
| `sign_up_group_choice_id` | `TextView` | private | 33 |

**Methods:**
| Method | Visibility | Line |
|---|---|---|
| `onCreateView(LayoutInflater, ViewGroup, Bundle)` | public (override) | 36 |
| `onActivityCreated(Bundle)` | public (override) | 43 |
| `initViews()` | public | 50 |
| `showGroupType()` | private | 89 |
| `register()` | private | 112 |
| `onClick(View)` | public (override) | 204 |

---

### File 2: `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/SignupLoadingFragment.java`

**Class:** `SignupLoadingFragment extends FleetFragment implements View.OnClickListener`

**Fields:**
| Field | Type | Visibility | Line |
|---|---|---|---|
| `activity` | `LoginActivity` | package-private | 24 |
| `loadingIV` | `ImageView` | private | 25 |
| `loadingResIds` | `int[]` | private | 47 |
| `loginFinished` | `static boolean` | private | 51 |
| `runTime` | `static int` | private | 52 |

**Methods:**
| Method | Visibility | Line |
|---|---|---|
| `onCreateView(LayoutInflater, ViewGroup, Bundle)` | public (override) | 28 |
| `onActivityCreated(Bundle)` | public (override) | 35 |
| `initViews()` | public | 41 |
| `timerHandle()` | private | 54 |
| `onLoginSucceed()` | private | 79 |
| `loadingLoginHandle()` | private | 85 |
| `showDashboard()` | private | 111 |
| `onResume()` | public (override) | 122 |
| `onStop()` | public (override) | 129 |
| `onDestroy()` | public (override) | 134 |
| `onClick(View)` | public (override) | 139 |

---

### File 3: `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/UniversityGuideFragment.java`

**Class:** `UniversityGuideFragment extends FleetFragment`

**Fields:** none declared.

**Methods:**
| Method | Visibility | Line |
|---|---|---|
| `onCreateView(LayoutInflater, ViewGroup, Bundle)` | public (override) | 21 |
| `initViews()` | public | 26 |
| `onResume()` | public (override) | 49 |
| `onPause()` | public (override) | 54 |

---

## Section 2 & 3: Findings

---

### A67-1 — HIGH: Mutable `static` fields used for per-instance animation state cause cross-instance data corruption

**File:** `SignupLoadingFragment.java`, lines 51–52

```java
private static boolean loginFinished = false;
private static int runTime = 0;
```

`loginFinished` and `runTime` are declared `static`, meaning they are shared across all instances of `SignupLoadingFragment`. Android fragments can be created multiple times (back-stack, rotation, activity re-creation). If more than one instance of this fragment exists simultaneously (e.g., during activity recreation while the previous instance's background thread is still running), both instances share the same animation counter and the same termination flag. The background thread in `timerHandle()` reads `loginFinished` (line 59) and writes `runTime` (line 71) without any synchronization. A second instance calling `loadingLoginHandle()` (line 106) resets `loginFinished = false` and `runTime = 0` while the previous thread may still be running, resulting in an infinite loop or garbled animation state.

These fields should be instance fields, not static.

---

### A67-2 — HIGH: Raw `Thread` spawned in `timerHandle()` with no lifecycle management leaks on back navigation or rotation

**File:** `SignupLoadingFragment.java`, lines 54–77

```java
private void timerHandle() {
    new Thread(new Runnable() {
        @Override
        public void run() {
            while (true) {
                if (loginFinished) return;
                ...
                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        loadingIV.setImageResource(...);
                        runTime++;
                    }
                });
            }
        }
    }).start();
}
```

A raw `Thread` is started with no reference stored and no interrupt mechanism. The only exit condition is `if (loginFinished) return;` (line 59). If the user presses back before login completes, `loginFinished` is never set to `true` (it is only set inside `HandleSuccess()` and `HandleIncorrectCredentials()`), so the thread runs indefinitely. After the fragment is destroyed, `activity.runOnUiThread(...)` (line 67) continues to post UI updates, and `loadingIV.setImageResource(...)` (line 70) is called on a detached view, producing a window leak. Additionally, `onStop()` and `onDestroy()` (lines 129–136) are empty overrides that make no attempt to stop the thread.

---

### A67-3 — HIGH: `NullPointerException` risk — `MyCommonValue.currentEquipmentItem` accessed without null check

**File:** `UniversityGuideFragment.java`, line 33

```java
intent.putExtra(WebActivity.URL_KEY, URLBuilder.urlGetUniversity(MyCommonValue.currentEquipmentItem.id).url);
```

`MyCommonValue.currentEquipmentItem` is a public static field initialized to `null` (confirmed in `MyCommonValue.java`, line 10). If the user navigates to `UniversityGuideFragment` while no equipment item is selected — or after the process is restored with cleared static state — this line will throw an unguarded `NullPointerException` at runtime. There is no null guard in `initViews()` or the click listener. The companion `MyCommonValue.java` comment dates this class to 2017, suggesting the global mutable static has been relied upon throughout the codebase.

---

### A67-4 — MEDIUM: `onClick(View)` interface method declared but left empty — dead interface implementation

**File:** `SignupFragment.java`, lines 203–205; `SignupLoadingFragment.java`, lines 139–141

```java
// SignupFragment.java
@Override
public void onClick(View view) {
}

// SignupLoadingFragment.java
@Override
public void onClick(View view) {
}
```

Both classes declare `implements View.OnClickListener` and provide an empty `onClick` implementation. Neither class passes `this` as a click listener to any view — all click listeners are registered via anonymous inner classes inside `initViews()`. The `View.OnClickListener` contract is therefore declared but never used. The `implements View.OnClickListener` clause should be removed from both class declarations, along with the empty `onClick` overrides. As dead code they create misleading surface area and suppress IDE warnings about unregistered listeners.

---

### A67-5 — MEDIUM: `onStop()` and `onDestroy()` are no-op overrides — dead code

**File:** `SignupLoadingFragment.java`, lines 129–136

```java
@Override
public void onStop() {
    super.onStop();
}

@Override
public void onDestroy() {
    super.onDestroy();
}
```

Both overrides do nothing beyond calling `super`. They add noise without contributing logic. This is especially notable given that `timerHandle()` (finding A67-2) launches an unmanaged thread that should be stopped in one of these lifecycle methods. The existence of the empty stubs suggests these were placeholder hooks that were never implemented.

---

### A67-6 — MEDIUM: `onResume()` and `onPause()` are no-op overrides — dead code

**File:** `UniversityGuideFragment.java`, lines 49–56

```java
@Override
public void onResume() {
    super.onResume();
}

@Override
public void onPause() {
    super.onPause();
}
```

Same pattern as A67-5. Both are pure pass-through overrides with no added behavior. They should be deleted.

---

### A67-7 — MEDIUM: Package-private `activity` field — leaky encapsulation

**File:** `SignupFragment.java`, line 31; `SignupLoadingFragment.java`, line 24

```java
// SignupFragment.java
SignupActivity activity;

// SignupLoadingFragment.java
LoginActivity activity;
```

The `activity` field in both fragments is package-private (no access modifier). It should be `private`. Fragment-to-activity communication via a stored typed reference is already a coupling concern, but omitting `private` exposes the field to any class in the same package without any intended API contract. The same pattern was used consistently across both files, indicating it is a systemic convention issue rather than a one-off oversight.

---

### A67-8 — MEDIUM: `register()` validates fields in non-standard order — style inconsistency and UX defect

**File:** `SignupFragment.java`, lines 121–154

The validation order in `register()` is:

1. User type (line 121)
2. Email (line 126)
3. First name (line 131)
4. Last name (line 136)
5. Mobile (line 141)
6. Password validity (line 146)
7. Password confirmation match (line 151)

The form layout (inferred from the `EditText` field order, lines 53–58) is: first name, last name, email, mobile, password, confirm password. Validating email (step 2) before first name (step 3) means the user is shown the email error before the first-name error even though first name appears first on screen. This creates a confusing UX and indicates validation logic was not aligned with field layout order.

---

### A67-9 — MEDIUM: Incorrect error message on 502 Bad Gateway response

**File:** `SignupFragment.java`, lines 177–180

```java
if (webResult.isBadGateway()) {
    hideProgress();
    showErrDialog("Email already exist");
}
```

A 502 Bad Gateway HTTP status code is a server-side proxy/gateway error and has no semantic relationship to a duplicate email address. The server API may return 502 to indicate a duplicate registration, but mapping a network-level error code to a domain-specific message is an incorrect abstraction. If the backend is documented to return 502 for duplicate emails, this is a server API design defect being silently papered over in the client. In either case, the error message "Email already exist" also contains a grammatical error (should be "Email already exists"). This is a business-logic and copy defect.

---

### A67-10 — MEDIUM: `showDashboard()` does not set `FLAG_ACTIVITY_NEW_TASK | FLAG_ACTIVITY_CLEAR_TASK` for `DashboardActivity`

**File:** `SignupLoadingFragment.java`, lines 111–119

```java
private void showDashboard() {
    Intent intent = new Intent(getContext(), DashboardActivity.class);
    if (CurrentUser.get().hasAssociatedDrivers()) {
        intent = new Intent(getContext(), DriversActivity.class);
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
    }
    startActivity(intent);
    Objects.requireNonNull(getActivity()).finish();
}
```

`Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK` is set only for `DriversActivity`. For `DashboardActivity`, no flags are set, so `LoginActivity` remains on the back stack. The user can then press Back from the dashboard and return to the loading/login screen, triggering another auto-login attempt. The `getActivity().finish()` call only removes `LoginActivity`, but depending on the task stack, previous activities may still be reachable. The inconsistency between how the two destination activities are launched is a style and behavioral defect.

---

### A67-11 — LOW: Field named after its view ID — poor naming convention

**File:** `SignupFragment.java`, line 33

```java
private TextView sign_up_group_choice_id;
```

All other `EditText` fields use camelCase with a meaningful semantic suffix (`firstNameET`, `lastNameET`, `emailAddressET`, etc.). The `sign_up_group_choice_id` field uses snake_case and copies the XML resource ID name verbatim, including the `_id` suffix which is a layout convention, not a Java naming convention. This is an inconsistency with all other field names in the same class.

---

### A67-12 — LOW: Generic anonymous class parameter names in `OnEditorActionListener`

**File:** `SignupFragment.java`, lines 62–67

```java
public boolean onEditorAction(TextView arg0, int arg1, KeyEvent arg2) {
```

The parameters are named `arg0`, `arg1`, `arg2` — IDE-generated defaults. All other anonymous listener implementations in the same file use meaningful parameter names (e.g., `view`, `object`, `index`). This is a style inconsistency.

---

### A67-13 — LOW: `isEmpty()` should be preferred over `.length() == 0`

**File:** `SignupFragment.java`, lines 131, 136, 141

```java
if (firstStr.length() == 0) { ... }
if (lastStr.length() == 0) { ... }
if (mobileStr.length() == 0) { ... }
```

`String.isEmpty()` (available since Java 6 / API 1) is the idiomatic replacement for `.length() == 0`. Using `.length() == 0` is not wrong, but it is inconsistent with modern Android Java style and requires a reader to understand the intent implicitly rather than through a named method.

---

### A67-14 — LOW: Hardcoded magic number delay of 1000 ms in `register()` response handling

**File:** `SignupFragment.java`, lines 172, 187

```java
getBaseActivity().runLater(new Runnable() { ... }, 1000);
```

The value `1000` (milliseconds) appears twice with no named constant. This is a magic number. If the delay needs to change, both occurrences must be found and updated manually, risking inconsistency. A named constant (e.g., `private static final int PROGRESS_DISMISS_DELAY_MS = 1000;`) would make the intent explicit and keep both usages in sync.

---

### A67-15 — LOW: `UserRegisterParameter` fields are all public with no encapsulation

**File:** `UserRegisterParameter.java` (supporting context), lines 14–19; used in `SignupFragment.java`, lines 193–199

```java
userRegisterParameter.first_name = firstStr;
userRegisterParameter.last_name = lastStr;
userRegisterParameter.email = emailStr;
userRegisterParameter.password = passwordStr;
userRegisterParameter.phone = mobileStr;
userRegisterParameter.contactperson = type.equals(TYPE_COMPANY);
```

All fields of `UserRegisterParameter` are public, and the caller in `SignupFragment` directly assigns to them. This is a data-class pattern common in legacy Android code but it bypasses encapsulation and prevents validation at the model level. The password field in particular is stored as a plain `String` in a public field, which conflicts with secure-coding guidance that sensitive string data should be handled as `char[]` and cleared after use.

---

### A67-16 — INFO: `android.support.*` imports — AndroidX migration not completed

**File:** `SignupFragment.java`, lines 4–5; `SignupLoadingFragment.java`, lines 5–6; `UniversityGuideFragment.java`, lines 5–6

```java
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.FragmentManager;  // UniversityGuideFragment.java
```

All three files use the legacy `android.support.*` namespace rather than `androidx.*`. The Android Support Library reached end-of-life in 2018; Google has required new Play Store apps to target AndroidX since 2020. This is noted as INFO because it is a project-wide migration concern, not a defect introduced by these three files specifically, but it means all `support.*` APIs are formally deprecated and may lack security and compatibility updates.

---

## Summary Table

| ID | Severity | File | Line(s) | Description |
|---|---|---|---|---|
| A67-1 | HIGH | SignupLoadingFragment.java | 51–52 | Static animation state fields cause cross-instance corruption |
| A67-2 | HIGH | SignupLoadingFragment.java | 54–77 | Unmanaged raw Thread leaks on back navigation / rotation |
| A67-3 | HIGH | UniversityGuideFragment.java | 33 | Unguarded access to nullable static `currentEquipmentItem` |
| A67-4 | MEDIUM | SignupFragment.java, SignupLoadingFragment.java | 203–205, 139–141 | Dead `View.OnClickListener` implementation in both classes |
| A67-5 | MEDIUM | SignupLoadingFragment.java | 129–136 | Empty `onStop()` and `onDestroy()` overrides |
| A67-6 | MEDIUM | UniversityGuideFragment.java | 49–56 | Empty `onResume()` and `onPause()` overrides |
| A67-7 | MEDIUM | SignupFragment.java, SignupLoadingFragment.java | 31, 24 | Package-private `activity` field — missing `private` modifier |
| A67-8 | MEDIUM | SignupFragment.java | 121–154 | Validation order does not match form field order |
| A67-9 | MEDIUM | SignupFragment.java | 177–180 | 502 Bad Gateway mapped to "Email already exist" (wrong code + grammar) |
| A67-10 | MEDIUM | SignupLoadingFragment.java | 111–119 | `DashboardActivity` launched without `CLEAR_TASK` flags; inconsistent with `DriversActivity` |
| A67-11 | LOW | SignupFragment.java | 33 | Field `sign_up_group_choice_id` uses snake_case copying XML ID |
| A67-12 | LOW | SignupFragment.java | 62 | `arg0/arg1/arg2` parameter names in `OnEditorActionListener` |
| A67-13 | LOW | SignupFragment.java | 131, 136, 141 | `.length() == 0` instead of `.isEmpty()` |
| A67-14 | LOW | SignupFragment.java | 172, 187 | Magic number `1000` (ms delay) repeated without named constant |
| A67-15 | LOW | SignupFragment.java | 193–199 | Password assigned to public field of `UserRegisterParameter` |
| A67-16 | INFO | All three files | various | `android.support.*` imports — AndroidX migration pending |
