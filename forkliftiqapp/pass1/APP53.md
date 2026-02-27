# Pass 1 Security Audit — APP53

**Agent ID:** APP53
**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Stack:** Android/Java

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy noted:** The checklist header states `Branch: main`. The actual active branch is `master`. Audit proceeds on `master` as instructed.

---

## Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/DriverStatsFragment1.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/DriverStatsFragment2.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/fragment/DriverStatsFragment3.java`

---

## Reading Evidence

### File 1 — DriverStatsFragment1.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.DriverStatsFragment1`

**Superclass:** `FleetFragment` (extends Fragment)

**Component type:** Fragment (not an Activity, Service, BroadcastReceiver, or ContentProvider — not directly declared in AndroidManifest)

**Fields / Constants:**
- `private final static String STATS_KEY_USAGE = "usage"` — line 23
- `private DriverStatsListAdapter listAdapter` — line 24
- `private ArrayList<DriverStatsItem> listServiceStatsData` — line 25
- `private GetDriverStatsResultArray driverStatsResultArray` — line 26

**Public methods (signature and line number):**
- `public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)` — line 30 (override)
- `public void initViews()` — line 35
- `public void onRightButton(View view)` — line 124 (override)

**Private methods:**
- `private void getUserDetail()` — line 54
- `private void loadData()` — line 59
- `private void setUserData()` — line 81
- `private void onData(GetDriverStatsResultArray resultArray)` — line 92

**Web API calls:**
- `WebApi.async().getDriverStats(WebData.instance().getUserId(), ...)` — line 66

**User data displayed (PII fields rendered to UI):**
- `user.getEmail()` — line 86
- `user.isContactPerson()` — line 87
- `user.getLicenseNumber()` — line 88

---

### File 2 — DriverStatsFragment2.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.DriverStatsFragment2`

**Superclass:** `FleetFragment`

**Component type:** Fragment

**Fields / Constants:**
- `private ServiceStatsListAdapter listAdapter` — line 25
- `private ArrayList<DriverStatsItem> listServiceStatsData` — line 26
- `private float preStartFailed = 0.0f` — line 27
- `private float preStartIncomplete = 0.0f` — line 28
- `private TextView user_name` — line 30
- `boolean fromProfile = true` — line 31 (package-private, no access modifier)
- `private GetDriverStatsResultArray driverStatsResultArray` — line 32
- `private ArrayList<TextView> views = new ArrayList<>()` — line 97
- `private PieChart mChart` — line 160
- `private final String LABEL_FAILED = "FAILED"` — line 176
- `private final String LABEL_INCOMPLETE = "INCOMPLETE"` — line 177
- `private final String LABEL_COMPLETED = "COMPLETED"` — line 178

**Public methods (signature and line number):**
- `public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)` — line 36 (override)
- `public void initViews()` — line 41
- `public void onRightButton(View view)` — line 243 (override)

**Private methods:**
- `private void setUserData()` — line 66
- `private void getUserDetail()` — line 70
- `private void loadData()` — line 75
- `private void initEquipmentViews()` — line 99
- `private void setUserEquipments()` — line 109
- `private void onData(GetDriverStatsResultArray resultArray)` — line 126
- `private void initServiceChart()` — line 162
- `private ArrayList<Integer> getColorForPieEntry(ArrayList<PieEntry> pieEntries)` — line 180
- `private ArrayList<PieEntry> getServicePieData()` — line 198
- `private void setData()` — line 218

**Web API calls:**
- `WebApi.async().getDriverStats(WebData.instance().getUserId(), ...)` — line 82

**User data displayed:**
- `CurrentUser.get().definedName()` — line 67

---

### File 3 — DriverStatsFragment3.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.DriverStatsFragment3`

**Superclass:** `FleetFragment`

**Component type:** Fragment

**Fields / Constants:**
- `private LineChart mChart` — line 38
- `private LinearLayout info_layout_1, info_layout_2` — line 39
- `private EquipmentStatsResultArray driverStatsResultArray` — line 40
- `public ArrayList<EquipmentStatsItem> arrayList = new ArrayList<>()` — line 41 (public field)
- `private int selectedType = 0` — line 50
- `private static final int[] mColors = { ... }` — lines 233–249 (15 hardcoded RGB colour values)

**Public methods (signature and line number):**
- `public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)` — line 44 (override)
- `public void initViews()` — line 52
- Inner class `public class MyValueFormatter implements IValueFormatter` — line 316; method `public String getFormattedValue(...)` — line 319
- Inner class `public static class MyAxisValueFormatter implements IAxisValueFormatter` — line 324; field `ArrayList<String> labelList` — line 325; method `public String getFormattedValue(...)` — line 328

**Private methods:**
- `private void getUserDetail()` — line 102
- `private void onWeekView()` — line 107
- `private void onMonthView()` — line 112
- `private void onYearView()` — line 117
- `private void loadData()` — line 122
- `private void setUserData()` — line 145
- `private void onData(EquipmentStatsResultArray resultArray)` — line 156
- `private void showInfo()` — line 168
- `private void showItem(int color, EquipmentStatsItem equipmentStatsItem, View view)` — line 206
- `private void initChar()` — line 214
- `private void clearChartData()` — line 251
- `private void initChartData(EquipmentStatsResultArray equipmentStatsResultArray)` — line 257
- `private ArrayList<String> getColumnLabels(EquipmentStatsResultArray resultArray)` — line 292
- `private MyAxisValueFormatter getXAixsFormatter(EquipmentStatsResultArray resultArray)` — line 309

**Web API calls:**
- `WebApi.async().getEquipmentStats(WebData.instance().getUserId(), selectedType, ...)` — line 130

**User data displayed:**
- `user.getEmail()` — line 150
- `user.isContactPerson()` — line 151
- `user.getLicenseNumber()` — line 152

---

## Checklist Review

### Section 1 — Signing and Keystores

These files are Fragment UI classes. They contain no signing configuration, keystore references, storePassword, keyPassword, or keyAlias values, and no references to Bitbucket Pipelines or credentials.

No issues found — Section 1.

---

### Section 2 — Network Security

**Finding — LOW/INFORMATIONAL: User ID passed as plain parameter to API calls over unverified transport.**

All three fragments pass `WebData.instance().getUserId()` as a parameter to web API calls:
- `DriverStatsFragment1.java` line 66: `WebApi.async().getDriverStats(WebData.instance().getUserId(), ...)`
- `DriverStatsFragment2.java` line 82: `WebApi.async().getDriverStats(WebData.instance().getUserId(), ...)`
- `DriverStatsFragment3.java` line 130: `WebApi.async().getEquipmentStats(WebData.instance().getUserId(), selectedType, ...)`

The transport security of `WebApi` itself is not defined in these files. These fragments assume the caller (`WebApi.async()`) enforces HTTPS; they do not enforce it themselves. This is an architectural observation — the full verdict depends on `WebApi` implementation reviewed by another agent. No direct cleartext traffic issue is introduced here.

No hardcoded API endpoints, server URLs, or IP addresses found in these files.

No WebView usage found in any of the three files.

No TrustAllCertificates, hostnameVerifier overrides, or SSLContext customisation found.

No issues found — Section 2 (within scope of these files).

---

### Section 3 — Data Storage

**Finding — LOW/INFORMATIONAL: PII rendered to UI without visible sanitisation.**

All three fragments display operator PII directly in TextViews:
- `DriverStatsFragment1.java` line 86: `user.getEmail()` rendered as `"Contact: %s"`
- `DriverStatsFragment1.java` line 88: `user.getLicenseNumber()` rendered as `"License No: %s"`
- `DriverStatsFragment3.java` lines 150–152: same pattern — email, role, and license number rendered

These are UI display operations. The concern is not storage per se in these fragments, but they confirm that email and license number (PII) flow through the `CurrentUser.get()` singleton into UI. If `CurrentUser` persists this data insecurely (in plain SharedPreferences, for example), it would be a storage issue — but that is outside the scope of these files.

No SharedPreferences access found in any of the three files.

No file I/O, SQLite, or external storage access found.

No `MODE_WORLD_READABLE` or `MODE_WORLD_WRITEABLE` found.

No issues found — Section 3 (within scope of these files).

---

### Section 4 — Input and Intent Handling

**Finding — LOW: Package-private field `fromProfile` on DriverStatsFragment2 is directly accessible.**

`DriverStatsFragment2.java` line 31: `boolean fromProfile = true;` — this field has no access modifier (package-private). It is directly set by the navigation code in `DriverStatsFragment2.java` line 246: `fragment.fromProfile = false;`. While Fragments are not exported Android components and therefore not accessible from outside the app, the use of a package-private field rather than a Bundle argument or setter method bypasses normal Android Fragment construction patterns (i.e. arguments passed via `Fragment.setArguments(Bundle)`). This is a code quality and robustness issue: if the Fragment is recreated by the system (e.g. after process death), the field will revert to its default value of `true`, silently changing the navigation behaviour. This is not directly a security vulnerability in these files but could lead to unexpected privilege or data exposure if the `fromProfile` flag gates data access or actions.

No exported Activities, Services, or BroadcastReceivers are defined in these files (all are Fragments, not manifest-registered components).

No implicit intents carrying sensitive data found.

No WebView usage found.

No deep link handlers found.

No issues found — Section 4 (no direct security vulnerability; code quality note recorded above).

---

### Section 5 — Authentication and Session

**Finding — INFORMATIONAL: `WebData.instance().getUserId()` is called directly from Fragment layer.**

All three fragments invoke `WebData.instance().getUserId()` to supply the user ID to API calls. This is a singleton data accessor. If `WebData` stores the user ID or session token in plain SharedPreferences or a non-encrypted store, there is a session security risk. The implementation of `WebData` is outside the scope of these files. The pattern itself — user ID embedded in API request parameters rather than derived from a server-side session token — may indicate that the user ID acts as an authentication proxy, which could be exploitable if enumerable. This observation should be cross-referenced with the agent reviewing `WebData`.

No token expiry handling is visible in these files; all API call failure paths show a generic error dialog and do not attempt re-authentication.

No logout or credential clearing logic found in these files (appropriate — these are stats display fragments, not authentication screens).

No issues found — Section 5 (within scope of these files; cross-reference concern noted).

---

### Section 6 — Third-Party Libraries

**Finding — INFORMATIONAL: MPAndroidChart library imported via non-version-pinned wildcard import.**

`DriverStatsFragment2.java` and `DriverStatsFragment3.java` import MPAndroidChart (`com.github.mikephil.charting.*`). The version used is not determinable from these source files alone; it must be verified in `build.gradle`. MPAndroidChart is a charting library that renders local data only (no network access from the library). No known high-severity CVEs have been attributed to MPAndroidChart as of the knowledge cutoff. Version pinning should be confirmed in Gradle.

No other third-party library imports found in these files beyond MPAndroidChart and the standard Android support library.

No issues found — Section 6 (within scope of these files; MPAndroidChart version should be confirmed in build.gradle review).

---

### Section 7 — Google Play and Android Platform

**Finding — LOW: Deprecated `android.support.*` imports used instead of AndroidX.**

All three fragments use `android.support.annotation.NonNull`, `android.support.annotation.Nullable` (lines 4–5 in each file). The Android Support Library was superseded by AndroidX. Google deprecated the Support Library in 2018 and it no longer receives security patches. While annotations themselves carry no runtime security risk, continued use of the Support Library indicates the project has not migrated to AndroidX, which may mean other support library components in the broader codebase are also outdated.

**Finding — INFORMATIONAL: No runtime permission requests in these files.**

These fragments make API calls that use `WebData.instance().getUserId()`. No dangerous permissions (CAMERA, LOCATION, READ_CONTACTS) are requested or handled in these fragments. This is appropriate for stats display fragments; permission handling would be expected upstream.

**Finding — INFORMATIONAL: `AsyncTask`-style deprecated API pattern may be in use via `WebApi.async()`.**

`WebApi.async()` is called in all three fragments. The implementation of `WebApi` is outside scope, but if it uses `AsyncTask` internally (deprecated in API 30), this would be a platform compliance issue. Should be cross-referenced with the agent reviewing `WebApi`.

No `startActivityForResult` usage found.

No issues found — Section 7 (within scope of these files; deprecated Support Library import is the only direct finding).

---

## Summary of Findings

| # | Severity | Section | File | Description |
|---|----------|---------|------|-------------|
| 1 | Low | 7 — Platform | All three files | Deprecated `android.support.*` imports; project not migrated to AndroidX |
| 2 | Low | 4 — Input Handling | DriverStatsFragment2.java line 31 | Package-private `fromProfile` field; should use `Fragment.setArguments(Bundle)` to survive system-recreated Fragment lifecycle |
| 3 | Informational | 3 — Data Storage | DriverStatsFragment1.java lines 86–88; DriverStatsFragment3.java lines 150–152 | PII (email, license number) rendered to UI from `CurrentUser` singleton; storage security of `CurrentUser` should be verified |
| 4 | Informational | 2 — Network | All three files | `WebData.instance().getUserId()` used as API parameter; transport security and token model dependent on `WebApi` / `WebData` implementations |
| 5 | Informational | 5 — Auth/Session | All three files | No token expiry or re-authentication handling in API failure paths; generic error dialog only |
| 6 | Informational | 6 — Libraries | DriverStatsFragment2.java, DriverStatsFragment3.java | MPAndroidChart version not verifiable from source; should be pinned and checked in build.gradle |

No Critical or High findings in these three files.
