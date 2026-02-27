# Pass 1 Security Audit — APP44
**Agent:** APP44
**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Stack:** Android/Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

Branch confirmed as **master**. Checklist states "Branch: main" — this is a discrepancy. Audit proceeds on `master` as instructed.

---

## Step 2 — Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/ActionActivity.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/ActionClearActivity.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/DashboardActivity.java`

Supporting files read: `AndroidManifest.xml` (app module), `FleetActivity.java` (base class).

---

## Step 3 — Reading Evidence

### File 1: ActionActivity.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.activity.ActionActivity`

**Superclass:** `au.com.collectiveintelligence.fleetiq360.ui.common.FleetActivity` (which extends `com.yy.libcommon.BaseActivity`)

**Public methods:**

| Method | Line |
|---|---|
| `protected void onCreate(Bundle savedInstanceState)` | 12 |

**Fields/constants:** None declared in this class.

**Intent extras consumed:**
- `getIntent().getStringExtra("action")` at line 18 — string key `"action"`, values compared against `"setup"` and `"report"`.

**Fragments launched based on intent extra:**
- `"setup"` → `SetupEmailFragment` (line 20)
- `"report"` → `SavedReportFragment` (line 24)

**WebView usage:** None in this file. `com.yy.libcommon.WebActivity` exists in the manifest but is not launched here.

**AndroidManifest declaration (from app/src/main/AndroidManifest.xml, line 73–75):**
```xml
<activity
    android:name=".ui.activity.ActionActivity"
    android:configChanges="orientation|keyboardHidden|screenSize"
    android:screenOrientation="portrait"/>
```
No `android:exported` attribute set. On API level < 31 this defaults to `false` when no `<intent-filter>` is present. No `<intent-filter>` is declared for this activity.

---

### File 2: ActionClearActivity.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.activity.ActionClearActivity`

**Superclass:** `au.com.collectiveintelligence.fleetiq360.ui.common.FleetActivity`

**Public methods:**

| Method | Line |
|---|---|
| `protected void onCreate(Bundle savedInstanceState)` | 11 |

**Fields/constants:** None declared in this class.

**Intent extras consumed:**
- `getIntent().getStringExtra("action")` at line 17 — string key `"action"`, value compared against `"setup"`.

**Fragments launched based on intent extra:**
- `"setup"` → `SetupEmailFragment` (line 19)

**WebView usage:** None.

**AndroidManifest declaration (lines 33–37):**
```xml
<activity
    android:name=".ui.activity.ActionClearActivity"
    android:configChanges="orientation|keyboardHidden|screenSize"
    android:screenOrientation="portrait"
    android:theme="@style/AppThemeClear"/>
```
No `android:exported` attribute set. No `<intent-filter>`. Defaults to not exported on API < 31.

---

### File 3: DashboardActivity.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.activity.DashboardActivity`

**Superclass:** `au.com.collectiveintelligence.fleetiq360.ui.common.FleetActivity`

**Public methods:**

| Method | Line |
|---|---|
| `protected void onCreate(Bundle savedInstanceState)` | 14 |
| `protected void onResume()` | 22 |

**Fields/constants:** None declared in this class.

**Services started in onResume (via `MyApplication.runLater`, 2-second delay):**
- `ShockEventService.startService()` (line 29)
- `CacheService.startService()` (line 30)
- `SyncService.startService()` (line 31)

**Intent extras consumed:** None — no `getIntent()` calls in this file.

**WebView usage:** None.

**AndroidManifest declaration (lines 43–47):**
```xml
<activity
    android:name=".ui.activity.DashboardActivity"
    android:configChanges="orientation|keyboardHidden|screenSize"
    android:screenOrientation="portrait"
    android:theme="@style/AppThemeLight"/>
```
No `android:exported` attribute set. No `<intent-filter>`. Defaults to not exported on API < 31.

---

## Step 4 — Supporting Context: FleetActivity Base Class

`FleetActivity` is the abstract base class for all three activities. Relevant observations:

- Registers a `BroadcastReceiver` via `LocalBroadcastManager` in `onResume`; unregisters in `onPause`. `LocalBroadcastManager` is sandboxed to the process — not exploitable by external apps.
- Uses `startActivityForResult` (deprecated API 29+, line 302 in FleetActivity).
- Calls `SyncService.startService()` from `onCreate` (line 72 in FleetActivity).
- `RECONNECT_REQUEST_ENABLE_BT` is an instance field (not `static final`) initialized to `100` (line 328); `LOCATION_SETTINGS_REQUEST_GPS` is `public static int` initialized to `200` (line 329) — not declared as `final`.

---

## Step 5 — Findings by Checklist Section

### Section 1: Signing and Keystores

Not applicable to these three source files. No signing configuration, keystore references, or credential strings appear in `ActionActivity.java`, `ActionClearActivity.java`, or `DashboardActivity.java`.

No issues found — Section 1 (within scope of assigned files).

---

### Section 2: Network Security

Not applicable to these three source files. No HTTP client usage, URL construction, or endpoint references appear in the three activity files. Network calls are delegated to `WebApi` and service classes not within this assignment's scope.

No issues found — Section 2 (within scope of assigned files).

---

### Section 3: Data Storage

Not applicable to these three source files. No `SharedPreferences`, file I/O, SQLite access, or external storage access appears in the three activity files. `DashboardActivity.onResume` starts background services that may perform storage operations, but those service implementations are outside this assignment's scope.

No issues found — Section 3 (within scope of assigned files).

---

### Section 4: Input and Intent Handling

#### Finding 4-A: Unvalidated Intent Extra Used as Control Flow Branch — Medium

**Affected files:**
- `ActionActivity.java`, line 18–24
- `ActionClearActivity.java`, line 17–21

**Detail:**

In both `ActionActivity` and `ActionClearActivity`, the incoming `Intent` extra `"action"` is retrieved and compared without null-checking before the `.equals()` call:

`ActionActivity.java`:
```java
String action = getIntent().getStringExtra("action");   // line 18
if (action.equals("setup")) {                            // line 19 — NullPointerException if "action" extra absent
```

`ActionClearActivity.java`:
```java
String action = getIntent().getStringExtra("action");   // line 17
if (action.equals("setup")) {                           // line 18 — NullPointerException if "action" extra absent
```

If no `"action"` extra is present in the intent, `getStringExtra` returns `null`. Calling `.equals()` on `null` throws a `NullPointerException`, crashing the activity. This is a denial-of-service vector if either activity is reachable by an external sender. Although neither activity declares `android:exported="true"` and neither has an `<intent-filter>`, the absence of an explicit `android:exported="false"` attribute means the exported state is determined by Android's default rules. On Android 12 (API 31)+, any activity without an explicit `android:exported` attribute and without an `<intent-filter>` defaults to `false`, but on older API levels the default also falls to `false` for activities without filters. However, relying on implicit defaults rather than explicit declarations is fragile — a future developer adding an intent-filter to either activity without also setting `android:exported="false"` would immediately expose this crash to external senders.

**Recommendation:** Null-check the extra before use (e.g., `if ("setup".equals(action))`) and add `android:exported="false"` explicitly to both activity declarations in `AndroidManifest.xml`.

#### Finding 4-B: Missing Explicit android:exported="false" on Three Activities — Low / Informational

**Affected manifest entries:** `ActionActivity`, `ActionClearActivity`, `DashboardActivity` (lines 33–37, 43–47, 73–75 of `AndroidManifest.xml`).

None of the three activities declare `android:exported`. On API 31+ Google Play enforcement requires all components to declare this attribute explicitly. The absence generates a build-time warning (or failure depending on compileSdkVersion) and represents a code-quality gap that could introduce a vulnerability if intent-filters are added during future maintenance.

**Recommendation:** Add `android:exported="false"` to all three activity declarations.

#### No Deep Link Handlers

None of the three activities contain `<intent-filter>` elements with custom `android:scheme` attributes. No deep link handling is present in these files.

No issues found — Deep link handling (Section 4).

#### No WebView Usage

None of the three activity files instantiate or configure a `WebView`. `com.yy.libcommon.WebActivity` is declared in the manifest but is not invoked from these three files.

No issues found — WebView (Section 4).

---

### Section 5: Authentication and Session

Not applicable to these three source files. `ActionActivity` and `ActionClearActivity` display email setup and report fragments; `DashboardActivity` starts background services. No credential handling, token storage, or logout logic is implemented in any of the three files. These concerns are delegated to other classes outside this assignment's scope.

No issues found — Section 5 (within scope of assigned files).

---

### Section 6: Third-Party Libraries

Not applicable to these three source files. No library-specific API calls appear in the three activity files beyond `FleetActivity` base class delegation.

No issues found — Section 6 (within scope of assigned files).

---

### Section 7: Google Play and Android Platform

#### Finding 7-A: Use of Deprecated startActivityForResult — Low / Informational

**Affected file:** `FleetActivity.java`, line 302 (base class of all three assigned activities).

`FleetActivity.onFailed` calls `startActivityForResult(enableBtIntent, RECONNECT_REQUEST_ENABLE_BT)`. This API is deprecated as of AndroidX Activity 1.2.0 / API 30. While this is defined in the base class and not in the three assigned files directly, all three assigned activities inherit this behaviour. This is an informational finding for awareness; the deprecated API still functions but will generate lint warnings.

**Recommendation:** Migrate to `ActivityResultLauncher` with `ActivityResultContracts.StartActivityForResult`.

#### No issues found — targetSdkVersion / minSdkVersion (outside scope of assigned files; covered by Gradle file assignments).

---

## Summary Table

| ID | File | Section | Severity | Title |
|---|---|---|---|---|
| 4-A | ActionActivity.java (line 18–19), ActionClearActivity.java (line 17–18) | 4 – Input/Intent Handling | Medium | Null-dereference crash on missing "action" intent extra |
| 4-B | AndroidManifest.xml (ActionActivity, ActionClearActivity, DashboardActivity entries) | 4 – Input/Intent Handling | Low | Missing explicit android:exported="false" on three activities |
| 7-A | FleetActivity.java (line 302, inherited by all three) | 7 – Google Play / Platform | Low | Deprecated startActivityForResult used in inherited base class |
