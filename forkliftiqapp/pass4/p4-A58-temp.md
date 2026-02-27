# Pass 4 Code Quality Audit — Agent A58
**Audit run:** 2026-02-26-01
**Agent:** A58
**Date completed:** 2026-02-27

---

## Section 1: Reading Evidence

### File 1 — `SelectForkAdapter.java`
**Full path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/adapter/SelectForkAdapter.java`
**Class:** `SelectForkAdapter` (extends `AbsRecyclerAdapter<String>`)

| # | Method | Line |
|---|--------|------|
| 1 | `setPresenter(EquipmentSelectForkPresenter presenter)` | 13 |
| 2 | `SelectForkAdapter(Context context, int resId)` — constructor | 17 |
| 3 | `bindDatas(MyViewHolder holder, String data, final int position)` — `@Override` | 22 |

**Fields:**
- `private EquipmentSelectForkPresenter presenter;` — line 11

**Types/constants/interfaces defined:** none beyond class declaration.

---

### File 2 — `MyApplication.java`
**Full path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/application/MyApplication.java`
**Class:** `MyApplication` (extends `MultiDexApplication`)

| # | Method | Line |
|---|--------|------|
| 1 | `onCreate()` | 49 |
| 2 | `initDataBase()` — private | 65 |
| 3 | `registerNetworkStatus()` — private | 77 |
| 4 | `onNetworkChanged()` — private | 89 |
| 5 | `onNetworkDisconnected()` — private | 106 |
| 6 | `onNetworkConnected()` — private | 109 |
| 7 | `getHandler()` — public static | 112 |
| 8 | `runOnMainThread(final Runnable runnable)` — public static | 116 |
| 9 | `runLater(final Runnable runnable, int time)` — public static | 122 |
| 10 | `initImageLoader(Context context)` — private static | 128 |
| 11 | `startLocationUpdate()` — public static | 140 |
| 12 | `SaveUnitLocation()` — private static | 165 |
| 13 | `getGPSProviderStatus()` — public static | 190 |
| 14 | `sendLocationUpdate()` — public static | 195 |
| 15 | `getContext()` — public static | 213 |

**Fields:**
- `@SuppressLint("StaticFieldLeak") private static Context context;` — line 41
- `private static Handler mHandler;` — line 42
- `private static SaveSingleGPSParameter GPSParam;` — line 43
- `Runnable runnable;` — line 45 (instance, package-private)
- `private static ScheduledExecutorService locationService;` — line 46
- `private boolean networkConnected = false;` — line 75

**Types/constants/interfaces defined:** none.

---

### File 3 — `FleetActivity.java`
**Full path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/common/FleetActivity.java`
**Class:** `FleetActivity` (abstract, extends `BaseActivity`)
**Inner class:** `AbortSessionCallback` (public static, line 410)

| # | Method | Line |
|---|--------|------|
| 1 | `onCreate(Bundle savedInstanceState)` — `@Override` | 69 |
| 2 | `setLoadingView(View view)` — private | 76 |
| 3 | `setLoadingView()` — private (overload) | 80 |
| 4 | `showLoadingLayout()` — public | 84 |
| 5 | `hideLoadingLayout()` — public | 90 |
| 6 | `setContentView(int layoutId)` — `@Override` public | 97 |
| 7 | `setRootView(int layoutId)` — private | 101 |
| 8 | Anonymous `BroadcastReceiver.onReceive(Context, Intent)` | 118 (field `broadcastReceiver`, line 116) |
| 9 | `showImpactAlert()` — private | 134 |
| 10 | `getImpactLevelColourMessage(ShockEventsItem.ImpactLevel)` — private static | 156 |
| 11 | `onBleDeviceDisconnected(Intent intent)` — private | 169 |
| 12 | `showDeviceDisconnectedDialog()` — private | 187 |
| 13 | `onReconnectDevice(final int delayMillis)` — private | 217 |
| 14 | `checkDeviceConnectedLater(final int delayMillis)` — private | 224 |
| 15 | `checkEquipmentConnected()` — private | 235 |
| 16 | `runEquipmentConnectCheck()` — private, returns boolean | 239 |
| 17 | `reconnectEquipment(EquipmentItem equipmentItem)` — private | 247 |
| 18 | `onActivityResult(int, int, Intent)` — `@Override` public | 331 |
| 19 | `isAbortingSession()` — private | 349 |
| 20 | `onStopSessionByUser()` — private | 354 |
| 21 | `abortSessionWithCallback(SessionResult, AbortSessionCallback)` — protected static | 418 |
| 22 | `onResume()` — `@Override` protected | 441 |
| 23 | `onPause()` — `@Override` protected | 454 |
| 24 | `AbortSessionCallback.onSessionStopped()` — public | 411 |
| 25 | `AbortSessionCallback.onSessionStopFailed()` — public | 414 |

**Fields:**
- `private View mLoadingView;` — line 59
- `public boolean connectingDevice = false;` — line 60
- `private boolean isDismissed = false;` — line 61
- `LocationProvider mLocation;` — line 62 (package-private, never read after assignment)
- `SaveSingleGPSParameter GPSParam;` — line 63 (package-private, never assigned or read in this file)
- `Runnable runnable;` — line 65 (package-private, never used in this file)
- `ScheduledExecutorService service;` — line 66 (package-private, never used in this file)
- `private BroadcastReceiver broadcastReceiver` — line 116 (anonymous inner class field)
- `private int RECONNECT_REQUEST_ENABLE_BT = 100;` — line 328
- `public static int LOCATION_SETTINGS_REQUEST_GPS = 200;` — line 329

**Types/constants/interfaces defined:**
- Inner class `AbortSessionCallback` (public static) — line 410

---

## Section 2 & 3: Findings

---

### A58-1 — HIGH: Leaky abstraction — adapter directly reads internal presenter state via public field

**File:** `SelectForkAdapter.java` line 26–27
**File:** `EquipmentSelectForkPresenter.java` line 22

```java
// SelectForkAdapter.java:26
if ((presenter != null) && (position < presenter.ui.urlList.size())) {
    presenter.showImage(presenter.ui.urlList.get(position), iv);
}
```

```java
// EquipmentSelectForkPresenter.java:22
public EquipmentListFragment ui;
```

The adapter navigates two layers of internal structure (`presenter.ui.urlList`) to obtain a URL. `EquipmentListFragment ui` is exposed as a raw public field on the presenter, and `urlList` is accessed directly from the fragment's internals. This is a textbook leaky abstraction: the adapter couples itself to a concrete fragment type and to the presenter's internal UI reference. The presenter should expose a method such as `getImageUrlAt(int position)` so the adapter is decoupled from both the fragment type and the presenter's data structures.

---

### A58-2 — HIGH: Dead instance field — `Runnable runnable` in `MyApplication`

**File:** `MyApplication.java` line 45

```java
Runnable runnable;
```

This instance field is declared package-private but is never assigned or read anywhere in the class. The commented-out block (lines 144–162) once used a local `Runnable runnable` variable in `startLocationUpdate()`, not this instance field. The field is pure dead code and should be removed.

---

### A58-3 — HIGH: Dead static field — `ScheduledExecutorService locationService` in `MyApplication`

**File:** `MyApplication.java` line 46

```java
private static ScheduledExecutorService locationService;
```

All usage of `locationService` has been commented out (it was used in the commented block inside `startLocationUpdate()` at lines 155, 159, and in `sendLocationUpdate()` at lines 200–208). The field is never read or written in any live code path. It is dead code and should be removed together with the commented-out scheduler logic.

---

### A58-4 — HIGH: Large commented-out block — scheduler logic in `startLocationUpdate()`

**File:** `MyApplication.java` lines 144–162

```java
/*
if(!getGPSProviderStatus()) return;

int gps_frequency = CurrentUser.get().getGps_frequency();

Runnable runnable = new Runnable() {
    public void run() {
        SaveUnitLocation();
    }
};

locationService = Executors.newSingleThreadScheduledExecutor();

if (gps_frequency > 0) {
    LocationProvider.instance().beginUpdates();
    locationService.scheduleAtFixedRate(runnable, 0, gps_frequency, TimeUnit.SECONDS);
}
 */
```

This is a significant block of commented-out logic that represents a previous implementation of GPS frequency-based scheduling. It should either be reinstated (if the feature is still required) or deleted. Its presence alongside the active `SaveUnitLocation()` method and the now-unused imports (`Executors`, `ScheduledExecutorService`, `TimeUnit`, `Calendar`) causes confusion about intent.

---

### A58-5 — HIGH: Large commented-out block — scheduler teardown in `sendLocationUpdate()`

**File:** `MyApplication.java` lines 199–209

```java
/*
    locationService.shutdown();
    try {
        locationService.awaitTermination(5, TimeUnit.SECONDS);
        LocationProvider.instance().endUpdates();
    }
    catch (InterruptedException e) {
        e.printStackTrace();
    }
 */
```

Same issue as A58-4. The body of `sendLocationUpdate()` now only calls `SaveUnitLocation()` conditionally, while the teardown path is commented out. The method name `sendLocationUpdate` no longer accurately describes what the live code does (it saves a single GPS sample, not "sends a location update" in a scheduling sense). This block must be reinstated or removed.

---

### A58-6 — MEDIUM: Dead instance fields — `GPSParam`, `Runnable runnable`, `ScheduledExecutorService service` in `FleetActivity`

**File:** `FleetActivity.java` lines 63, 65, 66

```java
SaveSingleGPSParameter GPSParam;   // line 63
Runnable runnable;                  // line 65
ScheduledExecutorService service;   // line 66
```

None of these three instance fields are assigned or read anywhere within `FleetActivity.java`. `GPSParam` is a distinct field from the static `GPSParam` in `MyApplication`; it is also never used here. `runnable` and `service` appear to be vestiges of an earlier GPS-scheduling design that was moved to `MyApplication` (or removed). All three are dead code.

---

### A58-7 — MEDIUM: Dead instance field — `LocationProvider mLocation` in `FleetActivity`

**File:** `FleetActivity.java` line 62

```java
LocationProvider mLocation;
```

This field is declared but never assigned or read within `FleetActivity`. `LocationProvider` is accessed exclusively via its singleton `LocationProvider.instance()`. The field is dead code.

---

### A58-8 — MEDIUM: Commented-out code — `onBleDeviceDisconnected` connection-retry logic

**File:** `FleetActivity.java` lines 179–184

```java
//        int connectionRetry = Objects.requireNonNull(SessionDb.readRunningSessionDb()).incrementConnectionRetry();
//        if (connectionRetry < 3) {
            onReconnectDevice(5000);
//        } else {
//            showDeviceDisconnectedDialog();
//        }
```

The retry-count guard and the disconnect dialog branch are commented out, leaving unconditional reconnect attempts with no upper bound. The `showDeviceDisconnectedDialog()` method (lines 187–215) is now unreachable dead code. Either the retry limit must be restored or the dead method and all commented lines must be removed.

---

### A58-9 — MEDIUM: Dead private method — `showDeviceDisconnectedDialog()`

**File:** `FleetActivity.java` lines 187–215

```java
private void showDeviceDisconnectedDialog() { ... }
```

This method is only ever called from the commented-out `else` branch in `onBleDeviceDisconnected()` (A58-8). With those lines commented out, this method is unreachable. It should either be reinstated (along with the retry logic) or deleted.

---

### A58-10 — MEDIUM: Commented-out code — multiple `//hideProgress()` and `//showProgress()` calls in `FleetActivity`

**File:** `FleetActivity.java` lines 255, 263, 282, 294, 304, 337, 359, 363

```java
//showProgress(null, "Connecting...");
...
//                hideProgress();
...
//                hideProgress();
...
//                    hideProgress();
...
//                    hideProgress();
...
//                hideProgress();
...
//                hideProgress();
```

Eight scattered single-line commented-out calls to `showProgress`/`hideProgress` appear throughout `reconnectEquipment()`, `onActivityResult()`, and `onStopSessionByUser()`. The active replacement in `reconnectEquipment()` is a `ProgressDialog` constructed manually (lines 256–268). The commented residue creates noise and implies the API may be partially or inconsistently replaced. All commented lines should be removed.

---

### A58-11 — MEDIUM: `@SuppressLint("StaticFieldLeak")` — static Context reference in `MyApplication`

**File:** `MyApplication.java` lines 40–41

```java
@SuppressLint("StaticFieldLeak")
private static Context context;
```

The `@SuppressLint` suppresses a legitimate lint warning: holding a static `Context` reference risks a memory leak if that context is ever an `Activity`. The field is assigned `getApplicationContext()` (line 51), which is safe in isolation, but the suppression hides the warning for the entire field declaration rather than documenting that the application context is intentionally used. The comment should at minimum state this intent, and the suppression annotation should be avoided if the field is always assigned from `getApplicationContext()`. (Using `MultiDexApplication.getApplicationContext()` directly from `getContext()` at call sites would eliminate the need for the static field and the suppression.)

---

### A58-12 — MEDIUM: Instance field `RECONNECT_REQUEST_ENABLE_BT` declared as non-constant `int` instead of `static final`

**File:** `FleetActivity.java` line 328

```java
private int RECONNECT_REQUEST_ENABLE_BT = 100;
```

The field uses an ALL_CAPS name (Java constant convention) but is not declared `static final`. It is never mutated. It should be `private static final int RECONNECT_REQUEST_ENABLE_BT = 100;`. Contrast with line 329 where `LOCATION_SETTINGS_REQUEST_GPS` is `public static int` but also non-final.

---

### A58-13 — MEDIUM: `LOCATION_SETTINGS_REQUEST_GPS` declared `public static` (non-final, non-constant)

**File:** `FleetActivity.java` line 329

```java
public static int LOCATION_SETTINGS_REQUEST_GPS = 200;
```

The field is `public static` but not `final`, allowing external mutation of a value that is semantically a constant. It should be `public static final int LOCATION_SETTINGS_REQUEST_GPS = 200;`.

---

### A58-14 — MEDIUM: Empty lifecycle stub methods — `onNetworkDisconnected()` and `onNetworkConnected()`

**File:** `MyApplication.java` lines 106–110

```java
private void onNetworkDisconnected() {
}

private void onNetworkConnected() {
}
```

Both methods are private, have empty bodies, and are called from `onNetworkChanged()`. Their only observable effect is to mark call sites; no subclass can override them because they are `private` in a final-deployment `Application` class. Either they should have bodies (with logging at minimum to aid debugging) or they should be removed and the call sites eliminated.

---

### A58-15 — LOW: Unused imports in `MyApplication.java`

**File:** `MyApplication.java`

The following imports are used only by commented-out code and are no longer live:

- `java.util.Calendar` — used in `SaveUnitLocation()` (live), so retained — **not unused**
- `java.util.concurrent.Executors` — used only in commented-out block (line 155)
- `java.util.concurrent.ScheduledExecutorService` — used only in commented-out block
- `java.util.concurrent.TimeUnit` — used only in commented-out block

These three (`Executors`, `ScheduledExecutorService`, `TimeUnit`) are unreferenced by any live code and should be removed to eliminate compiler/IDE warnings.

---

### A58-16 — LOW: Unused import `ScheduledExecutorService` in `FleetActivity.java`

**File:** `FleetActivity.java` line 29

```java
import java.util.concurrent.ScheduledExecutorService;
```

The `ScheduledExecutorService service` field (line 66) is never used (see A58-6), making this import also dead. It should be removed.

---

### A58-17 — LOW: Deprecated API — `ProgressDialog` usage in `FleetActivity`

**File:** `FleetActivity.java` lines 256–268

```java
final ProgressDialog cancelDialog = new ProgressDialog(this);
cancelDialog.setTitle(null);
cancelDialog.setCancelable(false);
cancelDialog.setMessage("Connecting...");
cancelDialog.setButton("Dismiss", new DialogInterface.OnClickListener() { ... });
cancelDialog.show();
```

`android.app.ProgressDialog` has been deprecated since API 26 (Android 8.0). The setButton call using a bare `String` key is also deprecated (use `DialogInterface.BUTTON_POSITIVE` constant). The commented-out `showProgress()` / `hideProgress()` lines suggest a custom progress mechanism existed; if so, it should be used consistently.

---

### A58-18 — LOW: Deprecated API — `ConnectivityManager.CONNECTIVITY_ACTION` broadcast

**File:** `MyApplication.java` line 85

```java
IntentFilter filter = new IntentFilter(ConnectivityManager.CONNECTIVITY_ACTION);
registerReceiver(networkStateReceiver, filter);
```

`ConnectivityManager.CONNECTIVITY_ACTION` is deprecated from API 28 (Android 9). Apps targeting API 28+ should use `ConnectivityManager.registerNetworkCallback()` instead. This will generate a lint deprecation warning on modern build targets.

---

### A58-19 — LOW: Naming convention violation — method `SaveUnitLocation()` uses PascalCase

**File:** `MyApplication.java` line 165

```java
private static void SaveUnitLocation() { ... }
```

Java method naming convention requires lowerCamelCase. All other methods in this file follow the convention. The method should be `saveUnitLocation()`.

---

### A58-20 — LOW: `bindDatas` method name is grammatically non-standard

**File:** `SelectForkAdapter.java` line 22 (and `AbsRecyclerAdapter.java` line 58)

```java
public abstract void bindDatas(MyViewHolder holder, T data, int position);
```

The method is named `bindDatas` (plural noun suffix) rather than the standard Android RecyclerView convention `onBindViewHolder` or a descriptive verb form like `bindData`. This is a style issue inherited from the abstract base but propagates to every concrete adapter. It is a style inconsistency with the Android ecosystem convention and should be tracked for future refactoring.

---

### A58-21 — INFO: `public boolean connectingDevice` — internal state exposed as public field

**File:** `FleetActivity.java` line 60

```java
public boolean connectingDevice = false;
```

This mutable boolean is declared `public`, allowing any external class to read or modify the BLE connection state of an activity. A `isConnectingDevice()` accessor (or at minimum `protected`) would be more appropriate. No immediate breakage risk but violates encapsulation.

---

### A58-22 — INFO: `SSLCertificateHandler.nuke()` called on every image load

**File:** `EquipmentSelectForkPresenter.java` line 71

```java
UserPhotoFragment.SSLCertificateHandler.nuke();
```

Referenced during context-reading; not in an assigned file but directly exercised by `SelectForkAdapter` via `presenter.showImage(...)`. Each call to `showImage()` disables SSL certificate validation globally for the JVM. This is a security concern surfaced here because `SelectForkAdapter` indirectly triggers it. Flagged INFO for cross-file awareness; a dedicated finding may be raised by whichever agent covers `UserPhotoFragment`.

---

## Summary Table

| ID | Severity | File | Short description |
|----|----------|------|-------------------|
| A58-1 | HIGH | SelectForkAdapter.java | Adapter directly traverses `presenter.ui.urlList` — leaky abstraction |
| A58-2 | HIGH | MyApplication.java | Dead instance field `Runnable runnable` |
| A58-3 | HIGH | MyApplication.java | Dead static field `ScheduledExecutorService locationService` |
| A58-4 | HIGH | MyApplication.java | Large commented-out scheduler block in `startLocationUpdate()` |
| A58-5 | HIGH | MyApplication.java | Large commented-out teardown block in `sendLocationUpdate()` |
| A58-6 | MEDIUM | FleetActivity.java | Three dead instance fields: `GPSParam`, `runnable`, `service` |
| A58-7 | MEDIUM | FleetActivity.java | Dead instance field `LocationProvider mLocation` |
| A58-8 | MEDIUM | FleetActivity.java | Commented-out retry logic leaves unconditional reconnect loop |
| A58-9 | MEDIUM | FleetActivity.java | Unreachable dead method `showDeviceDisconnectedDialog()` |
| A58-10 | MEDIUM | FleetActivity.java | Eight scattered commented-out `showProgress`/`hideProgress` calls |
| A58-11 | MEDIUM | MyApplication.java | `@SuppressLint("StaticFieldLeak")` on static Context field |
| A58-12 | MEDIUM | FleetActivity.java | `RECONNECT_REQUEST_ENABLE_BT` declared as non-final instance `int` |
| A58-13 | MEDIUM | FleetActivity.java | `LOCATION_SETTINGS_REQUEST_GPS` declared `public static` non-final |
| A58-14 | MEDIUM | MyApplication.java | Empty private stub methods `onNetworkDisconnected`/`onNetworkConnected` |
| A58-15 | LOW | MyApplication.java | Three unused imports from commented-out scheduler code |
| A58-16 | LOW | FleetActivity.java | Unused import `ScheduledExecutorService` |
| A58-17 | LOW | FleetActivity.java | Deprecated `ProgressDialog` API usage |
| A58-18 | LOW | MyApplication.java | Deprecated `CONNECTIVITY_ACTION` broadcast registration |
| A58-19 | LOW | MyApplication.java | Method `SaveUnitLocation` uses PascalCase — convention violation |
| A58-20 | LOW | SelectForkAdapter.java | `bindDatas` non-standard method name |
| A58-21 | INFO | FleetActivity.java | `public boolean connectingDevice` — mutable state exposed publicly |
| A58-22 | INFO | SelectForkAdapter.java | `SSLCertificateHandler.nuke()` triggered on every image load |
