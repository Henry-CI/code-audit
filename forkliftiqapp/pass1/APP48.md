# Pass 1 Security Audit — APP48
**Agent ID:** APP48
**Date:** 2026-02-27
**Repository:** forkliftiqapp
**Stack:** Android/Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

Checklist specifies branch `main`. Actual branch is `master`. Discrepancy recorded. Branch is `master` — audit proceeds.

---

## Step 2 — Assigned File

1. `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/SignupActivity.java`

---

## Step 3 — Reading Evidence

### File: SignupActivity.java

**Fully Qualified Class Name:**
`au.com.collectiveintelligence.fleetiq360.ui.activity.SignupActivity`

**Superclass:**
`FleetActivity` (via `au.com.collectiveintelligence.fleetiq360.ui.common.FleetActivity`)

**Public Methods:**

| Method | Line |
|--------|------|
| `protected void onCreate(Bundle savedInstanceState)` | 10 |

**Fields / Constants:**
None declared. No instance fields, static fields, or constants are present in this file.

**Android Component Type:**
Activity (extends `FleetActivity`, which extends `AppCompatActivity` or equivalent base class).

**Fragment Loaded:**
`SignupFragment` — loaded into container `R.id.login_framelayout_id` via `showFragmentWithoutStack(...)` at line 13.

**Layout:**
`R.layout.activity_signup`

**Full Source (15 lines):**
```java
package au.com.collectiveintelligence.fleetiq360.ui.activity;

import android.os.Bundle;
import au.com.collectiveintelligence.fleetiq360.R;
import au.com.collectiveintelligence.fleetiq360.ui.common.FleetActivity;
import au.com.collectiveintelligence.fleetiq360.ui.fragment.SignupFragment;

public class SignupActivity extends FleetActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);
        showFragmentWithoutStack(R.id.login_framelayout_id, SignupFragment.class.getSimpleName(), new SignupFragment());
    }
}
```

---

## Step 4 — Checklist Findings by Section

### Section 1 — Signing and Keystores

No issues found — SignupActivity.java contains no signing configuration, keystore references, credentials, passwords, or properties file references.

---

### Section 2 — Network Security

No issues found — SignupActivity.java contains no network calls, HTTP client usage, hardcoded API endpoints, URL strings, or certificate validation code. All network behaviour, if any, is delegated to `SignupFragment` (not assigned to this agent).

---

### Section 3 — Data Storage

No issues found — SignupActivity.java contains no SharedPreferences access, file I/O, SQLite operations, external storage references, or credential caching. The activity delegates all UI and data logic to `SignupFragment`.

**Note for broader audit:** The registration flow — including any password input, credential submission, and potential local storage of tokens following successful signup — is entirely implemented in `SignupFragment`. That class is outside this agent's assigned scope and must be reviewed separately.

---

### Section 4 — Input and Intent Handling

No issues found in this file. `SignupActivity` overrides only `onCreate` and performs no intent data parsing, no implicit intents, no deep link handling, and no WebView usage.

**Note for broader audit:** The `android:exported` status of `SignupActivity` in `AndroidManifest.xml` is outside the scope of this file review. The manifest must be checked by the assigned agent to confirm whether this activity is exported and, if so, whether it can be invoked by a third-party app to bypass authentication flow. The activity's sole action is to display `SignupFragment`; no privileged operation is performed at this layer.

---

### Section 5 — Authentication and Session

No issues found — SignupActivity.java contains no authentication logic, token storage, session management, or credential handling. All such logic, if present, resides in `SignupFragment`.

---

### Section 6 — Third-Party Libraries

No issues found — SignupActivity.java imports only Android SDK classes and project-internal classes. No third-party library is imported or used in this file.

---

### Section 7 — Google Play and Android Platform

**Observation — `startActivityForResult` / deprecated APIs:** The `showFragmentWithoutStack` method is called at line 13. This is an internal helper on `FleetActivity`. Its implementation is outside this file and must be reviewed for deprecated `FragmentManager` or transaction patterns. No finding can be confirmed from this file alone.

No other deprecated API usage is present in this file.

No permissions are declared in this file.

---

## Step 5 — Summary of Findings

No security findings were identified within the assigned file `SignupActivity.java`.

The file is a thin shell Activity (15 lines) whose sole responsibility is to host `SignupFragment` inside a frame layout. It contains no credential handling, no network access, no data storage, no exported component logic in source code, and no third-party library usage. All signup-related security risk is concentrated in `SignupFragment`, `FleetActivity.showFragmentWithoutStack()`, and the `AndroidManifest.xml` declaration for this activity — none of which are within this agent's assigned scope.

**Items requiring cross-agent follow-up:**
- `SignupFragment` — all registration logic including password field handling, credential submission, and post-signup token storage.
- `FleetActivity` — base class helper methods including `showFragmentWithoutStack`.
- `AndroidManifest.xml` — confirm `android:exported` value for `SignupActivity`.

---

*Report generated by Agent APP48 — Pass 1 — 2026-02-27*
