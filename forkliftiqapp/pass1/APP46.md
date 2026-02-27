# Pass 1 Security Audit — Agent APP46

**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Agent ID:** APP46

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy noted:** The checklist states `Branch: main`; the actual branch is `master`. Audit proceeds on `master`.

---

## Reading Evidence

### File 1: EquipmentStatsActivity.java

**Path:** `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/EquipmentStatsActivity.java`

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.activity.EquipmentStatsActivity`

**Superclass:** `FleetActivity` (which extends `BaseActivity`)

**Fields/constants:** None declared at class level.

**Public methods:**

| Method | Line |
|--------|------|
| `protected void onCreate(Bundle savedInstanceState)` | 10 |

**Activity in AndroidManifest.xml:**
```xml
<activity
    android:name=".ui.activity.EquipmentStatsActivity"
    android:configChanges="orientation|keyboardHidden|screenSize"
    android:screenOrientation="portrait"/>
```
No `android:exported` attribute set; no `<intent-filter>`. On API < 31 this defaults to `false` (not exported).

**Behaviour summary:** On create, displays `R.layout.activity_common` and loads `DriverStatsFragment3` into the fragment container. No keyboard initialisation distinct from base class; calls inherited `initKeyboard()`.

---

### File 2: IncidentActivity.java

**Path:** `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/IncidentActivity.java`

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.activity.IncidentActivity`

**Superclass:** `FleetActivity`

**Fields/constants declared at class level:**

| Field | Type | Visibility | Line |
|-------|------|------------|------|
| `impactParameter` | `ImpactParameter` | `public` | 12 |
| `impactResult` | `SaveImpactResult` | `public` | 13 |
| `signaturePath` | `String` | `public` | 14 |
| `mCurrentPhotoPath` | `String` | `public` | 15 |
| `injuryTypes` | `String[]` | `public` | 16 |

**Public methods:**

| Method | Line |
|--------|------|
| `protected void onCreate(Bundle savedInstanceState)` | 19 |
| `public void onBackPressed()` | 36 |

**Activity in AndroidManifest.xml:**
```xml
<activity
    android:name=".ui.activity.IncidentActivity"
    android:configChanges="orientation|keyboardHidden|screenSize"
    android:screenOrientation="portrait"/>
```
No `android:exported` attribute set; no `<intent-filter>`. Defaults to not exported.

**Behaviour summary:** On create, initialises an `ImpactParameter` with `incident = true`, `injury = false`, loads the first entry from `R.array.injury_type`, then loads `IncidentFragment`. On back press, if `impactResult` is non-null (incident has been saved), it calls `finish()` instead of the back stack behaviour, preventing re-submission.

**ImpactParameter fields (referenced type):** `injury_type`, `description`, `witness`, `report_time`, `event_time`, `injury` (boolean), `near_miss` (boolean), `incident` (boolean), `location`, `driver_id` (int), `unit_id` (int). Implements `Serializable`.

**SaveImpactResult fields (referenced type):** `id`, `signature`, `image`, `injury_type`, `witness`, `location`, `injury`, `near_miss`, `description`, `report_time`, `event_time`, `job_number`. Implements `Serializable`.

---

### File 3: JobsActivity.java

**Path:** `/c/Projects/cig-audit/repos/forkliftiqapp/app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/activity/JobsActivity.java`

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.ui.activity.JobsActivity`

**Superclass:** `FleetActivity`

**Fields/constants:** None declared at class level.

**Public methods:**

| Method | Line |
|--------|------|
| `protected void onCreate(Bundle savedInstanceState)` | 10 |

**Activity in AndroidManifest.xml:**
```xml
<activity
    android:name=".ui.activity.JobsActivity"
    android:configChanges="orientation|keyboardHidden|screenSize"
    android:screenOrientation="portrait"/>
```
No `android:exported` attribute set; no `<intent-filter>`. Defaults to not exported.

**Behaviour summary:** On create, sets layout to `R.layout.activity_jobs` and loads `JobsFragment` into the `R.id.jobs_act_framelayout_id` container. Minimal shell activity; all logic delegated to the fragment.

---

## Section-by-Section Findings

### 1. Signing and Keystores

No signing configuration, keystore files, or credentials are referenced in these three Activity files. This section is not assessable from the assigned files alone.

No issues found in the assigned files — Section 1.

---

### 2. Network Security

No network calls, HTTP client usage, URL construction, or endpoint references appear in any of the three assigned files. All three activities act purely as UI shells that delegate to fragments.

No issues found in the assigned files — Section 2.

---

### 3. Data Storage

**Finding — Medium: Public fields holding incident data on `IncidentActivity`**

`IncidentActivity` declares five instance fields with `public` visibility at lines 12–16:

```java
public ImpactParameter impactParameter;   // line 12
public SaveImpactResult impactResult;     // line 13
public String signaturePath = null;       // line 14
public String mCurrentPhotoPath;          // line 15
public String[] injuryTypes;             // line 16
```

`signaturePath` and `mCurrentPhotoPath` hold filesystem paths to a signature image and a photo respectively. `impactParameter` holds incident details including `driver_id`, `unit_id`, `location`, `witness`, and `description`. `impactResult` holds the server response including a `signature` field (likely a server-side path or base64 value) and `image`.

These fields are `public`, meaning any Fragment or other object with a reference to the Activity can read or overwrite them without any accessor control. While this is a common Android pattern for passing state between an Activity and its hosted Fragments, the scope of the data — incident records containing operator IDs, unit IDs, witness names, and paths to signature files — warrants that access be restricted. If any fragment or listener class obtained an inadvertent reference to the wrong Activity instance (e.g. during a configuration change or via a static reference), it could read or corrupt incident data belonging to a different operator.

`mCurrentPhotoPath` in particular holds a filesystem path. Its value in context suggests it points to a file created via the camera intent, likely in internal storage or a `FileProvider`-accessible location. No external storage write is visible in this file alone, but the path is fully public and unvalidated at this layer.

**Recommendation:** Restrict field visibility to `package-private` or use getter/setter methods with validation. Null `signaturePath` and `mCurrentPhotoPath` explicitly when the activity is destroyed or when a new incident session begins.

No issues found related to `SharedPreferences`, external storage writes, `MODE_WORLD_READABLE`, `allowBackup`, or credentials cached in static fields within the assigned files — Section 3 (partial).

---

### 4. Input and Intent Handling

**Observation — Informational: No `android:exported` attribute set on any of the three activities**

In the `AndroidManifest.xml`, `EquipmentStatsActivity` (line 69), `IncidentActivity` (line 61), and `JobsActivity` (line 53) are declared without an explicit `android:exported` attribute and without any `<intent-filter>`. Under Android API < 31, this defaults to `exported="false"`. Under API 31+, the build will fail at compile time if `exported` is omitted on activities with intent filters; since none of these three have intent filters, the default `false` applies and no external component can start them directly. This is the correct posture.

No exported activities, implicit intents carrying sensitive data, WebView usage, JavaScript enablement, or deep link handlers are present in the three assigned files.

No issues found in the assigned files — Section 4.

---

### 5. Authentication and Session

No authentication logic, token handling, credential storage, logout paths, or session management code appears in the three assigned files. All three are thin UI shells.

No issues found in the assigned files — Section 5.

---

### 6. Third-Party Libraries

No dependency declarations or library imports beyond standard Android and internal project classes are present in the three assigned files. `ImpactParameter` and `SaveImpactResult` use only `org.json` (platform-bundled) and `java.io.Serializable`.

No issues found in the assigned files — Section 6.

---

### 7. Google Play and Android Platform

**Finding — Low: Deprecated `startActivityForResult` usage inherited from `FleetActivity`**

`IncidentActivity` inherits from `FleetActivity`, which calls `startActivityForResult(enableBtIntent, RECONNECT_REQUEST_ENABLE_BT)` at line 302 of `FleetActivity.java`. This API is deprecated as of Android API 29 in favour of the Activity Result API (`ActivityResultLauncher`). While not directly authored in the assigned files, all three activities inherit this call path.

**Finding — Low: Deprecated `onBackPressed()` override in `IncidentActivity`**

`IncidentActivity.onBackPressed()` at line 36 overrides `onBackPressed()`, which is deprecated in API 33 in favour of `OnBackPressedCallback`. The existing logic (checking `impactResult != null` before calling `finish()`) is functional on current API levels but will need migration for long-term compatibility.

No issues found regarding `targetSdkVersion`/`minSdkVersion` (not visible in these files), runtime permission requests, or overly broad ProGuard rules — Section 7 (partial).

---

## Summary of Findings

| ID | Severity | Section | File | Description |
|----|----------|---------|------|-------------|
| APP46-01 | Medium | 3 — Data Storage | IncidentActivity.java | Five public instance fields expose incident data (driver ID, unit ID, witness, location, signature path, photo path) without access control |
| APP46-02 | Low | 7 — Platform APIs | IncidentActivity.java (inherited) | `startActivityForResult` deprecated; inherited from `FleetActivity` |
| APP46-03 | Low | 7 — Platform APIs | IncidentActivity.java line 36 | `onBackPressed()` override uses deprecated API (deprecated API 33) |

---

*End of report — Agent APP46*
