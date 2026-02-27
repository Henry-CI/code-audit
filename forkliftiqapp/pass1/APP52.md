# Security Audit — Pass 1
**Agent ID:** APP52
**Date:** 2026-02-27
**Repository:** forkliftiqapp
**Stack:** Android/Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy recorded:** The checklist states `Branch: main`. The actual branch is `master`. Audit proceeds on `master`.

---

## Step 2 — Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/AddEquipmentFragment.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/DashboardFragment.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/DriverListFragment.java`

---

## Step 3 — Reading Evidence

### File 1: AddEquipmentFragment.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.AddEquipmentFragment`

**Superclass:** `FleetFragment` (which extends Fragment)

**Fields / Constants:**
- `private ManufactureResultArray manufactureResultArray` — cached result of manufacturer list API call
- `@SuppressLint("UseSparseArrays") private HashMap<Integer, EquipmentTypeResultArray> mapEquipmentTypesForManu` — equipment types keyed by manufacturer ID
- `private HashMap<String, FuelTypeResultArray> mapFuelTypesForEquipmentType` — fuel types keyed by composite string key
- `private final String TYPE_TITLE = "--Type--"` — UI placeholder constant
- `private final String FUEL_TITLE = "--Power--"` — UI placeholder constant
- `private EditText equipment_name` (line 55)
- `private EditText equipment_no` (line 56)
- `private EditText equipment_mac_address` (line 57)
- `private TextView equipment_manufacture` (line 58)
- `private TextView equipment_type` (line 59)
- `private TextView equipment_fuel_type` (line 60)
- `private CheckBox expansion_module_checkbox` (line 61)
- `private ManufactureItem manufactureItem` (line 63)
- `private EquipmentTypeItem equipmentTypeItem` (line 64)
- `private FuelTypeItem fuelTypeItem` (line 65)

**Public methods with line numbers:**
- `public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)` — line 50 (override)
- `public void initViews()` — line 67
- `public void onMiddleButton(View view)` — line 388 (override)
- `public void onRightButton(View view)` — line 420 (override)

**Private methods with line numbers:**
- `private void updateMacAddressVisible()` — line 110
- `private void registerAfterMacTextChangedCallback(final EditText mMacEdit)` — line 114
- `private void showManu()` — line 196
- `private void showType()` — line 231
- `private String getKeyForFuelType(int mid, int tid)` — line 270
- `private void showFuelType()` — line 274
- `private void loadManu(final Runnable runnable)` — line 317
- `private void loadType(final Runnable runnable)` — line 337
- `private void loadFuelType(final Runnable runnable)` — line 362
- `private void saveEquipment()` — line 424

**Static imports:**
- `au.com.collectiveintelligence.fleetiq360.ui.fragment.EquipmentListFragment.equipmentChanged` — a mutable static boolean shared between fragments

**Notable imports:**
- `javax.net.ssl.HttpsURLConnection` — used to check HTTP_BAD_GATEWAY status code in error handling

---

### File 2: DashboardFragment.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.DashboardFragment`

**Superclass:** `FleetFragment`; implements `View.OnClickListener`

**Fields / Constants:**
- `static Bitmap userPhotoBitmap` — line 35; package-private static field holding a decoded user photo bitmap

**Public methods with line numbers:**
- `public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState)` — line 39 (override)
- `public void initViews()` — line 58
- `public void onSessionEnded()` — line 104 (override)
- `public void onResume()` — line 114 (override)
- `public void onStop()` — line 123 (override)
- `public void onDestroy()` — line 128 (override)
- `public void onClick(View view)` — line 133 (override)
- `public void onLeftButton(View view)` — line 175 (override)
- `public void onMiddleButton(View view)` — line 182 (override)
- `public void onRightButton(View view)` — line 189 (override)

**Private methods with line numbers:**
- `private void setUserPhoto()` — line 44
- `private void showUserName()` — line 54
- `private void initMonitorSession()` — line 89
- `private void updateRunning()` — line 98
- `private void getUserDetail()` — line 108
- `private void showEquipmentList()` — line 154
- `private void showProfile()` — line 168

**Notable behavior:**
- `onRightButton` (LOGOUT button): calls `WebData.instance().logout()` and starts `LoginActivity`. If a session is running, attempts `saveSessionEnd` first; falls back to offline session finish before logout.
- Intents launched: `DriverStatsActivity`, `EquipmentStatsActivity`, `IncidentActivity`, `SessionActivity`, `EquipmentActivity`, `ProfileActivity`, `ActionClearActivity`, `ActionActivity`, `LoginActivity` — all explicit.

---

### File 3: DriverListFragment.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.DriverListFragment`

**Superclass:** `FleetFragment`; implements `AbsRecyclerAdapter.OnItemClickListener`

**Fields / Constants:**
- `private SelectDriverAdapter adapter` — line 25

**Public methods with line numbers:**
- `public void onCreate(Bundle savedInstanceState)` — line 28 (override)
- `public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)` — line 33 (override)
- `public void initViews()` — line 38
- `public void onItemClick(View v, int position)` — line 55 (override)
- `public void updateDriverList(List<User> drivers)` — line 61
- `public void onRightButton(View view)` — line 66 (no-op override)
- `public void onMiddleButton(View view)` — line 71 (no-op override)

**Notable behavior:**
- `onItemClick` (line 56): calls `CurrentUser.setUser(...)` directly from the list — no authentication step. Sets the active user from a list entry, then navigates to `DashboardActivity` via `Intent.makeMainActivity`.

---

## Step 4 — Security Review by Checklist Section

### Section 1 — Signing and Keystores

No findings from these three fragment files. None reference keystore paths, passwords, signing configuration, or Gradle build scripts. Signing concerns are outside the scope of these files.

No issues found from these files — Section 1.

---

### Section 2 — Network Security

**Finding 2.1 — Medium — Error message leak via HTTP status code inspection (AddEquipmentFragment.java, line 469)**

In `saveEquipment()`, the `onFailed` callback directly inspects `webResult.getStatusCode()` and returns a user-facing message distinguishing "Equipment with the same name or serial number already saved" versus a generic failure message when `HTTP_BAD_GATEWAY` (502) is returned. While the user-facing message is not itself harmful, the pattern exposes internal API gateway behavior differences to the UI layer. More importantly, treating 502 from a gateway as a specific, actionable business error is a fragile design: a transient proxy error and a duplicate-record rejection cannot be reliably distinguished by HTTP status alone. This is a logic concern with a minor security dimension (information leakage about backend deduplication logic via error messages that enumerate valid resource states).

**Finding 2.2 — Informational — WebApi.async() not verifiable from these files**

`WebApi.async()` is called repeatedly in `AddEquipmentFragment` and `DashboardFragment` for API calls (`getManufacture`, `getEquipmentType`, `getFuelType`, `addEquipment`, `getEquipmentList`, `saveSessionEnd`). Whether these calls are made over HTTPS and whether certificate validation is correctly implemented cannot be determined from these fragment files alone. The checklist requires reviewing the HTTP client implementation. This is flagged for the agent reviewing WebApi/network layer files.

No further network issues found from these files — Section 2.

---

### Section 3 — Data Storage

**Finding 3.1 — Medium — Static Bitmap field retains user photo beyond Fragment lifecycle (DashboardFragment.java, line 35)**

`static Bitmap userPhotoBitmap` is declared as a package-private static field on `DashboardFragment`. Static fields on Fragment classes persist for the lifetime of the process, not the Fragment. A user photo (PII — biometric-adjacent) loaded here will remain in memory even after the Fragment is destroyed, across user sessions, and potentially across driver shift changes. In a multi-operator environment (the checklist explicitly calls out shift-change scenarios), this means a previous operator's photo may be retained in memory when a new operator logs in. The field is set to `null` at line 49 during `setUserPhoto()`, but only if `userPhotoBitmap != null` at that point — it is never defensively nulled at logout or Fragment destruction. `onStop()` and `onDestroy()` (lines 123–130) are empty overrides that do not clear this field.

**Finding 3.2 — Informational — CurrentUser.setUser() in DriverListFragment (line 56) — session data not reviewed**

`CurrentUser.setUser(this.adapter.getDatas().get(position))` is called when a driver is selected from the list. This sets the active user context application-wide with no apparent authentication challenge prior to the call. Whether `CurrentUser` stores the user object in SharedPreferences, in memory only, or in an encrypted store cannot be determined from this file. This is flagged for the agent reviewing the `CurrentUser` class.

No further data storage issues found from these files — Section 3.

---

### Section 4 — Input and Intent Handling

**Finding 4.1 — Low — No authentication gate before driver selection (DriverListFragment.java, lines 55–59)**

`onItemClick` sets `CurrentUser.setUser(...)` and navigates immediately to `DashboardActivity` without any credential challenge. Whoever has physical access to the device can tap any name in the driver list and gain access to that driver's dashboard. Whether this is intentional for forklift operations workflow (e.g., requiring physical device custody as the authentication factor) is a design question, but it warrants explicit documentation. If the device is unattended with the app open at the driver list screen, any person can impersonate any driver.

**Finding 4.2 — Informational — Intent extras carry action strings without validation (DashboardFragment.java, lines 177–185)**

`onLeftButton` and `onMiddleButton` launch `ActionClearActivity` and `ActionActivity` respectively with `intent.putExtra("action", "setup")` and `intent.putExtra("action", "report")`. These string-keyed extras are literal constants set inline at the call site. Since these are explicit intents between internal components (not received from external sources), there is no input-validation concern at this site. Flagged informational only.

**Finding 4.3 — No WebView usage found in these three files.**
No issues found — WebView sub-section, Section 4.

**Finding 4.4 — No deep link handlers present in these files.**
No issues found — deep link sub-section, Section 4.

**Finding 4.5 — All intents launched in DashboardFragment and DriverListFragment are explicit (fully qualified class targets).**
No issues found — implicit intent sub-section, Section 4.

---

### Section 5 — Authentication and Session

**Finding 5.1 — Medium — Logout does not guarantee clearing of static PII before re-authentication (DashboardFragment.java, line 35 + lines 198–218)**

The logout path in `onRightButton` calls `WebData.instance().logout()` and starts `LoginActivity`. The static field `DashboardFragment.userPhotoBitmap` is never cleared during logout. If a different operator logs in on the same device, the previous operator's photo may still be present in memory. While it is set to `null` during `setUserPhoto()` of the next session, this only occurs if the field was non-null at that precise moment — the window between logout and that method call represents a period where PII from the prior session is still held. This is a variant of Finding 3.1 viewed through the session-hygiene lens.

**Finding 5.2 — Medium — Driver selection bypasses authentication (DriverListFragment.java, line 56)**

`CurrentUser.setUser(adapter.getDatas().get(position))` sets the active operator from a list without credential verification. The app appears to use a model where an administrator selects a driver from a list, bypassing per-driver authentication. This is an architectural authentication concern: any operator with device access can select any other operator's identity. Relevant if the checklist concern about "multiple operators using the same device (shift changes)" is a production scenario.

**Finding 5.3 — Informational — Logout fallback path for offline sessions (DashboardFragment.java, lines 204–212)**

When `saveSessionEnd` fails and offline data exists (`SessionDb.hasOfflineData`), the app: marks the session finished locally, calls `WebData.instance().onSessionEnded()`, calls `WebData.instance().logout()`, and navigates to `LoginActivity`. This fallback path appears to correctly log out even under network failure. Noted as a positive finding for offline resilience.

No further authentication/session issues from these files — Section 5.

---

### Section 6 — Third-Party Libraries

No Gradle dependency declarations appear in these three fragment files. Third-party library use observed in these files:
- `io.realm.RealmChangeListener` and `io.realm.RealmResults` (DashboardFragment.java, lines 28–29) — Realm is used for local database access (`SessionDb`). Realm version and CVE status cannot be assessed from this file; flagged for the agent reviewing build.gradle.
- `com.yy.libcommon.ThemedSingleListDialog` (AddEquipmentFragment.java, line 29) — custom or third-party dialog library. Version and CVE status to be reviewed against build.gradle.

No issues determined from these files alone — Section 6.

---

### Section 7 — Google Play and Android Platform

**Finding 7.1 — Low — Deprecated support library imports (all three files)**

All three files import from `android.support.*` (e.g., `android.support.annotation.NonNull`, `android.support.v7.widget.LinearLayoutManager`, `android.support.v7.widget.RecyclerView`). The Android Support Library was superseded by AndroidX. Continued use of the legacy support library means the app cannot receive future library security fixes, which are published only to AndroidX artifacts. This also indicates the `targetSdkVersion` and migration status should be checked.

**Finding 7.2 — Informational — switch/case without break in DashboardFragment.onClick (line 133–152)**

In `onClick`, `case R.id.dashboard_incident_report:` at line 148 starts `IncidentActivity` but does not include a `break` statement before `default:`. In Java, this causes fall-through to the `default` case. The `default` case here is `break`, so there is no behavioral consequence in the current code. However, if a future case is inserted between `dashboard_incident_report` and `default`, unexpected fall-through may occur. This is a code quality note with low security relevance.

**Finding 7.3 — Informational — @SuppressLint("UseSparseArrays") on HashMap (AddEquipmentFragment.java, line 41)**

`HashMap<Integer, EquipmentTypeResultArray>` is annotated with `@SuppressLint("UseSparseArrays")` to suppress the lint warning recommending `SparseArray` for integer-keyed maps. This is a performance annotation suppression, not a security issue. Noted for completeness.

No further platform/API issues from these files — Section 7.

---

## Summary of Findings

| ID     | Severity      | File                          | Line(s)   | Description |
|--------|---------------|-------------------------------|-----------|-------------|
| 5.1 / 3.1 | Medium   | DashboardFragment.java        | 35, 49    | Static `Bitmap userPhotoBitmap` retains operator PII beyond session; not cleared at logout |
| 5.2 / 4.1 | Medium   | DriverListFragment.java       | 55–59     | Driver selection sets active user identity without credential challenge |
| 2.1    | Low           | AddEquipmentFragment.java     | 469–472   | HTTP 502 used to distinguish duplicate-record business error; fragile and leaks API structure |
| 7.1    | Low           | All three files               | various   | Deprecated `android.support.*` imports; should be migrated to AndroidX |
| 4.1    | Low           | DriverListFragment.java       | 55–59     | Physical device access permits identity impersonation at driver list screen |
| 2.2    | Informational | AddEquipmentFragment.java     | multiple  | `WebApi.async()` TLS/certificate validation not verifiable from these files; refer to network layer audit |
| 3.2    | Informational | DriverListFragment.java       | 56        | `CurrentUser` storage mechanism not verifiable from this file; refer to CurrentUser audit |
| 5.3    | Positive      | DashboardFragment.java        | 204–212   | Offline logout fallback correctly terminates session and clears user state |
| 7.2    | Informational | DashboardFragment.java        | 148–150   | Missing `break` in switch case (fall-through to no-op `default`; no current impact) |
| 6.1    | Informational | DashboardFragment.java        | 28–29     | Realm library version/CVE status to be checked in build.gradle audit |
