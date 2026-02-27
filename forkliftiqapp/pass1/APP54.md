# Pass 1 Security Audit — forkliftiqapp
**Agent ID:** APP54
**Date:** 2026-02-27
**Stack:** Android/Java
**Branch audited:** master
**Checklist branch field:** main

---

## Branch Discrepancy

The checklist specifies `Branch: main`. The actual branch returned by `git branch --show-current` is `master`. The audit proceeds on `master` as instructed.

---

## Reading Evidence

### File 1: DriverStatsListAdapter.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.DriverStatsListAdapter`

**Superclass:** `ArrayAdapter<DriverStatsItem>`

**Fields and constants:**
| Name | Type | Visibility | Line |
|---|---|---|---|
| `JOYFUL_COLORS` | `int[]` (static final) | private | 30 |
| `context` | `Context` | private | 20 |
| `mData` | `ArrayList<DriverStatsItem>` | private | 21 |
| `colors` | `ArrayList<Integer>` | private | 39 |
| `maxValue` | `float` | private | 48 |

**Public methods (signature and line):**
| Method | Line |
|---|---|
| `DriverStatsListAdapter(Context context, ArrayList<DriverStatsItem> data)` (package-private constructor) | 23 |
| `View getView(int position, View convertView, @NonNull ViewGroup parent)` | 77 |
| `int getCount()` | 124 |
| `DriverStatsItem getItem(int i)` | 129 |

**Inner classes:**
- `ListHolder` (static, package-private) — ViewHolder pattern; fields: `name`, `status_bar`, `status_bar_layout`, `stub`, `status_text` (line 133)

**Activities / Fragments / Services / Receivers / Providers declared:** None (adapter class only).

---

### File 2: EquipmentConnectFragment.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.EquipmentConnectFragment`

**Superclass:** `FleetFragment` (extends Fragment)

**Fields and constants:**
| Name | Type | Visibility | Line |
|---|---|---|---|
| `loadingIV` | `ImageView` | private | 36 |
| `connecting_text` | `View` | private | 37 |
| `activity` | `Activity` | package-private | 38 |
| `loadingResIds` | `int[]` | private | 40 |
| `autoConnect` | `boolean` | public | 44 |
| `myHandler` | `Handler` | private | 45 |
| `operationFinished` | `boolean` (static) | private | 46 |
| `operationSucceeded` | `boolean` (static) | private | 47 |
| `permissionNotGranted` | `boolean` (static) | private | 48 |
| `runTime` | `int` (static) | private | 49 |
| `connect_button` | `View` | private | 101 |
| `abort_button` | `View` | private | 102 |
| `stoppingSession` | `boolean` | private | 206 |
| `REQUEST_ENABLE_BT` | `int` | private | 207 |
| `runnableAfterPermission` | `Runnable` | private | 284 |

**Public methods (signature and line):**
| Method | Line |
|---|---|
| `View onCreateView(@NonNull LayoutInflater, @Nullable ViewGroup, @Nullable Bundle)` | 84 |
| `void onActivityCreated(Bundle)` | 91 |
| `void initViews()` | 104 |
| `void onResume()` | 170 |
| `void onActivityResult(int, int, Intent)` | 210 |
| `void onDestroy()` | 60 |

**Activities / Fragments declared:** Fragment class only; invokes `SessionActivity` by cast.

---

### File 3: EquipmentListFragment.java

**Fully qualified class name:**
`au.com.collectiveintelligence.fleetiq360.ui.fragment.EquipmentListFragment`

**Superclass:** `FleetFragment`; implements `AbsRecyclerAdapter.OnItemClickListener`, `EquipmentSelectForkPresenter.ShowResultCallBack`

**Fields and constants:**
| Name | Type | Visibility | Line |
|---|---|---|---|
| `myAdapter` | `SelectForkAdapter` | private | 43 |
| `presenter` | `EquipmentSelectForkPresenter` | private | 44 |
| `urlList` | `List<String>` | public | 45 |
| `getEquipmentResultArray` | `GetEquipmentResultArray` (static) | public | 46 |
| `equipmentChanged` | `boolean` (static) | package-private | 47 |
| `equipmentSelected` | `int` (static) | package-private | 48 |
| `activity` | `EquipmentActivity` | package-private | 49 |

**Public methods (signature and line):**
| Method | Line |
|---|---|
| `View onCreateView(@NonNull LayoutInflater, ViewGroup, Bundle)` | 53 |
| `void onDestroy()` | 59 |
| `void initViews()` | 64 |
| `void onItemClick(View v, int position)` | 103 |
| `void selectEquipment(int position)` | 108 |
| `void uiUpdateEquipmentList(GetEquipmentResultArray resultArray)` | 191 |
| `void onRightButton(View view)` | 206 |
| `void onMiddleButton(View view)` | 216 |

**Activities / Fragments declared:** Fragment class only; references `EquipmentActivity`, `AddEquipmentFragment`, `DriverStatsFragment2`.

---

## Findings by Checklist Section

### 1. Signing and Keystores

No signing configuration, keystore files, Gradle files, `bitbucket-pipelines.yml`, or `gradle.properties` are present in the three assigned files. These are UI/adapter layer files only.

No issues found — Section 1 (Signing and Keystores) — not applicable to assigned files.

---

### 2. Network Security

No HTTP client usage, URL construction, TrustManager configuration, or network endpoint definitions appear in any of the three files. `EquipmentConnectFragment` communicates via `BleController` (Bluetooth Low Energy), not over HTTP/HTTPS.

No issues found — Section 2 (Network Security) — not applicable to assigned files.

---

### 3. Data Storage

**Finding DS-1 — Static mutable state holding session and equipment data (Medium)**

In `EquipmentConnectFragment`, four static fields hold operational state shared across all instances of the fragment:

```java
// EquipmentConnectFragment.java lines 46-49
private static boolean operationFinished = false;
private static boolean operationSucceeded = false;
private static boolean permissionNotGranted = true;
private static int runTime = 0;
```

Because these are `static`, their values persist for the lifetime of the process. If the device is used by multiple operators without a full process kill (common in shift-change scenarios), `operationSucceeded` and `operationFinished` could retain values from a previous operator's session. `onResume()` (line 170–177) acts directly on `operationSucceeded` and `operationFinished` without resetting them, meaning a new operator resuming the fragment could be routed into a succeeded or failed flow from the prior operator's BLE connection. This is relevant to the checklist's requirement that one operator's data is fully cleared before another logs in.

**Finding DS-2 — Public static equipment result array (Low)**

In `EquipmentListFragment`, the equipment list fetched from the server is stored as a public static field:

```java
// EquipmentListFragment.java line 46
public static GetEquipmentResultArray getEquipmentResultArray;
```

`public static` mutable state on a Fragment is accessible to any class in the application and persists until explicitly nulled (which only occurs in `onDestroy()`, line 61). During shift changes, if `onDestroy()` is not called between sessions, equipment data from a previous operator's session could be presented to the next operator without a fresh server fetch. The field is nulled in `onDestroy()` but not on logout; whether logout triggers `onDestroy()` depends on the activity lifecycle, which cannot be verified from these files alone.

**Finding DS-3 — Public mutable field `urlList` (Informational)**

```java
// EquipmentListFragment.java line 45
public List<String> urlList = new ArrayList<>();
```

This field is `public` and non-final. It is not populated in any code visible in this file. Its purpose is unclear. If it holds URLs constructed from server responses, making it public instance state is unnecessary and exposes it to external mutation. Flag for review to confirm it is not used to store sensitive server-side paths accessible from outside the fragment.

No issues found regarding external storage writes, `MODE_WORLD_READABLE`, `MODE_WORLD_WRITEABLE`, `EncryptedSharedPreferences`, or `Environment.getExternalStorageDirectory()` — not present in assigned files.

---

### 4. Input and Intent Handling

**Finding IH-1 — `startActivityForResult` used with implicit Intent for Bluetooth enable (Low / Deprecated API)**

In `EquipmentConnectFragment.connectEquipment()` (line 272–273):

```java
Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
```

`startActivityForResult` is deprecated as of Android API 30. More importantly, `BluetoothAdapter.ACTION_REQUEST_ENABLE` as a means to prompt Bluetooth enablement is deprecated from API 33 (Android 13); on API 33+ the system silently ignores this and the connection flow stalls silently. This may cause the BLE connection to never complete on modern devices without proper error handling for the deprecation path.

The `REQUEST_ENABLE_BT` field is declared as `int` (not `static final`), which is a minor code quality issue (line 207):

```java
private int REQUEST_ENABLE_BT = 100;
```

**Finding IH-2 — No validation on BLE equipment item passed from static field (Low)**

In `EquipmentConnectFragment.startConnect()` (line 190):

```java
final EquipmentItem equipmentItem = MyCommonValue.currentEquipmentItem;
```

`MyCommonValue.currentEquipmentItem` is retrieved from what appears to be a global/static value holder. This value is set externally (in `EquipmentListFragment.goToCurrentEquipmentNext()`, line 177) and passed directly into `BleController.startConnect()` without null-checking or validation at the point of use in `startConnect()`. If `currentEquipmentItem` is null (e.g., due to a lifecycle race or intent replay), this results in a NullPointerException propagated into BLE layer code.

In `onActivityResult()` (line 214), `MyCommonValue.currentEquipmentItem` is also used directly without null-check:

```java
connectEquipment(MyCommonValue.currentEquipmentItem);
```

**Finding IH-3 — `autoConnect` is a public mutable field (Low)**

```java
// EquipmentConnectFragment.java line 44
public boolean autoConnect = false;
```

This field controls whether the fragment immediately initiates a BLE connection without user confirmation. It is set externally by callers. There is no access control on this field; any code in the application (including potentially injected code via a malicious dependency) can set `autoConnect = true` before the fragment is displayed and trigger an unsolicited BLE connection attempt.

No WebView, deep-link handlers, or exported component declarations appear in the assigned files.

No issues found regarding implicit intents carrying session tokens or operator IDs directly — not present in assigned files.

---

### 5. Authentication and Session

**Finding AS-1 — Static boolean flags survive operator session boundaries (Medium)**

As noted in DS-1, `operationFinished`, `operationSucceeded`, `permissionNotGranted`, and `runTime` in `EquipmentConnectFragment` are static. In `onResume()`:

```java
// EquipmentConnectFragment.java lines 170-177
@Override
public void onResume() {
    super.onResume();
    if (operationSucceeded) {
        showNext();
    } else if (operationFinished) {
        onConnectFailed();
    }
}
```

If `operationSucceeded` is `true` from a prior session and a new operator opens this fragment without a process restart, `showNext()` is called immediately, bypassing the BLE connection step and advancing the new operator's session as if the connection had already succeeded. This is a session boundary violation: the new operator's session is granted equipment access without a fresh authentication/connection handshake.

**Finding AS-2 — No evidence of credential clearing in assigned files (Informational)**

The assigned files do not contain logout logic. Whether credentials and session tokens are cleared on logout cannot be assessed from these files. This is noted as an observation to be assessed by agents reviewing authentication, logout, and session management code.

---

### 6. Third-Party Libraries

**Finding TL-1 — Legacy Android Support Library in use (Medium)**

All three files import from `android.support.*` rather than `androidx.*`:

```java
// DriverStatsListAdapter.java line 6
import android.support.annotation.NonNull;

// EquipmentConnectFragment.java lines 11-12
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;

// EquipmentListFragment.java lines 8-9
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
```

The Android Support Library (`com.android.support`) reached end-of-life and received its final release (28.0.0) in September 2018. It is no longer maintained and receives no security patches. Google has mandated migration to AndroidX. Continued use of the Support Library means the app cannot benefit from security fixes or updated APIs available in AndroidX equivalents. This also conflicts with `targetSdkVersion` 34+ requirements.

**Finding TL-2 — Third-party library `com.yy.libcommon` (Informational)**

`EquipmentConnectFragment` and `EquipmentListFragment` both import from `com.yy.libcommon`:

```java
// EquipmentConnectFragment.java line 19
import com.yy.libcommon.ErrorDialog;

// EquipmentListFragment.java lines 14-15
import com.yy.libcommon.ErrorDialog;
import com.yy.libcommon.YesNoDialog;
```

The package `com.yy.libcommon` is not a well-known public library. Its provenance, maintenance status, and CVE history cannot be assessed from these files alone. The build.gradle files must be reviewed to confirm the source, version, and integrity (hash pinning) of this dependency.

---

### 7. Google Play and Android Platform

**Finding GP-1 — Deprecated `startActivityForResult` (Low)**

As noted in IH-1, `startActivityForResult` is used at line 273 of `EquipmentConnectFragment`. This API is deprecated from `Activity` in favour of the Activity Result API (`ActivityResultLauncher`). While not a security vulnerability in isolation, it is flagged per checklist requirements.

**Finding GP-2 — Deprecated `onActivityCreated` (Informational)**

`EquipmentConnectFragment.onActivityCreated(Bundle)` at line 91 is deprecated as of Fragment 1.3.0. The recommended replacement is `onViewCreated`. Deprecated lifecycle callbacks can cause subtle lifecycle bugs when combined with newer AndroidX behaviour.

**Finding GP-3 — `BluetoothAdapter.ACTION_REQUEST_ENABLE` deprecated on API 33+ (Low)**

As detailed in IH-1, on Android 13 (API 33) and above, this intent action is rejected. The app must use `BluetoothManager` and the appropriate runtime permission (`BLUETOOTH_CONNECT`) instead. On API 33+ devices this flow will silently fail to enable Bluetooth.

**Finding GP-4 — Runtime permission handling for Bluetooth is incomplete (Medium)**

`EquipmentConnectFragment` references a field `permissionNotGranted` (line 48) and displays a location-access message at line 227:

```java
String s = permissionNotGranted ? "Since location access has not been granted, this app will not be able to discover devices." : "Failed to connect the equipment, please retry later.";
```

However, `permissionNotGranted` is initialised to `true` and is only ever set to `false` on a non-BLE-off failure (line 275). There is no code in this file that requests runtime permissions for `ACCESS_FINE_LOCATION`, `BLUETOOTH_SCAN`, or `BLUETOOTH_CONNECT`. The field `runnableAfterPermission` (line 284) is allocated but its name implies it was intended to be run after a permission grant callback — yet `startConnect()` calls `runnableAfterPermission.run()` immediately (line 198) without actually requesting or checking any permission. This means:

1. The runtime permission flow is vestigial or broken — permissions are neither requested nor awaited.
2. If the required Bluetooth/location permission has not been granted, `BleController.startConnect()` is called anyway, which will fail silently or throw a `SecurityException` on API 23+.
3. The `permissionNotGranted` flag does not accurately reflect actual permission state, so the error message shown to the user may be incorrect.

**Finding GP-5 — `getResources().getColor()` without theme (Informational)**

In `DriverStatsListAdapter.initColors()` (line 42–43):

```java
colors.add(getContext().getResources().getColor(R.color.ci_green));
colors.add(getContext().getResources().getColor(R.color.ci_dark_blue));
```

`Resources.getColor(int)` without a `Theme` argument is deprecated from API 23. The replacement is `ContextCompat.getColor(context, id)` or `Resources.getColor(int, Theme)`. Not a security finding but flagged per checklist deprecation requirements.

---

## Summary of Findings

| ID | Severity | File | Description |
|---|---|---|---|
| DS-1 | Medium | EquipmentConnectFragment.java | Static boolean session-state fields persist across operator sessions |
| AS-1 | Medium | EquipmentConnectFragment.java | `operationSucceeded` static flag can advance new operator session without fresh BLE authentication |
| GP-4 | Medium | EquipmentConnectFragment.java | Runtime Bluetooth/location permission check is vestigial; `BleController.startConnect()` called without confirmed permission |
| TL-1 | Medium | All three files | Legacy `android.support.*` library (EOL 2018) used throughout; no security patches |
| DS-2 | Low | EquipmentListFragment.java | Public static equipment result array may survive operator session boundary |
| IH-1 | Low | EquipmentConnectFragment.java | `startActivityForResult` and `ACTION_REQUEST_ENABLE` deprecated; BLE enable flow broken on API 33+ |
| IH-2 | Low | EquipmentConnectFragment.java | No null-check on `MyCommonValue.currentEquipmentItem` before passing to BLE layer |
| IH-3 | Low | EquipmentConnectFragment.java | `autoConnect` is a public mutable field enabling unsolicited BLE connection |
| GP-1 | Low | EquipmentConnectFragment.java | `startActivityForResult` deprecated |
| GP-3 | Low | EquipmentConnectFragment.java | `ACTION_REQUEST_ENABLE` deprecated and silently fails on API 33+ |
| DS-3 | Informational | EquipmentListFragment.java | `urlList` is public mutable with unclear purpose |
| TL-2 | Informational | EquipmentConnectFragment.java, EquipmentListFragment.java | `com.yy.libcommon` — unknown provenance, version not visible in these files |
| AS-2 | Informational | All three files | No logout/credential-clearing logic in assigned files; deferred to other agents |
| GP-2 | Informational | EquipmentConnectFragment.java | `onActivityCreated` deprecated |
| GP-5 | Informational | DriverStatsListAdapter.java | `getResources().getColor()` without Theme deprecated from API 23 |
