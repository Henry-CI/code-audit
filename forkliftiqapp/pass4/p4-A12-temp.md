# Pass 4 – Code Quality Audit
**Audit Run:** 2026-02-26-01
**Agent:** A12
**Date Completed:** 2026-02-27

---

## Section 1: Reading Evidence

### File 1: BleControlService.java
**Full path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/BLE/BleControlService.java`
**Class:** `BleControlService extends IntentService`

**Constants / Fields defined:**
| Name | Visibility | Type | Line |
|---|---|---|---|
| `ACTION_AUTO_RECONNECT` | `public static` | `String` | 22 |
| `ACTION_INIT_DEVICE` | `public static` | `String` | 23 |
| `ACTION_AUTH_DEVICE` | `private static` | `String` | 24 |
| `ACTION_SET_RELAY` | `private static` | `String` | 25 |
| `ACTION_SET_TIME` | `private static` | `String` | 26 |
| `ACTION_SET_IMPACT_THRESHOLD` | `private static` | `String` | 27 |
| `ACTION_SET_RELAY_TIMEOUT` | `private static` | `String` | 28 |
| `ACTION_ENABLE_SHOCK_NOTIFICATION` | `private static` | `String` | 29 |
| `TAG` | `public static` | `String` | 30 |
| `mBleMachine` | `static` (package-private) | `BleMachine` | 31 |

**Methods:**
| Method | Visibility | Line |
|---|---|---|
| `BleControlService()` constructor | `public` | 33 |
| `processBleEvents(Intent)` | `public` | 38 |
| `handleBleOperation(Intent)` | package-private | 102 |
| `onHandleIntent(Intent)` | `protected` (override) | 176 |
| `authDevice()` | `public static` | 183 |
| `sendData(Intent, String)` | `public static` | 187 |
| `sendActionWithDelay(String, int)` | `private static` | 200 |
| `sendAction(String)` | `public static` | 210 |
| `setRelayWithDelay()` | `public static` | 215 |
| `setRelayNoDelay()` | `public static` | 224 |
| `setTime()` | `public static` | 228 |
| `initDevice()` | `public static` | 232 |
| `setImpactThreshold()` | `public static` | 237 |
| `setRelayTimeout()` | `public static` | 241 |
| `setShockNotification()` | `public static` | 245 |
| `afterWriteAttribute(boolean, BluetoothGattCharacteristic, Runnable)` | `public static` | 249 |

**Types/Interfaces defined:** None (extends `IntentService`)

---

### File 2: BleController.java
**Full path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/BLE/BleController.java`
**Class:** `BleController`
**Inner class:** `BleController.EquipmentListener` (static, `public static class`)

**Constants / Fields defined:**
| Name | Visibility | Type | Line |
|---|---|---|---|
| `TAG` | `private final` | `String` | 35 |
| `mHandler` | `private` | `Handler` | 38 |
| `mIsScanning` | `private` | `boolean` | 39 |
| `mList` | `private` | `List<BluetoothGattService>` | 40 |
| `mDevicesDiscovered` | package-private | `ArrayList<BluetoothDevice>` | 41 |
| `mLEScanner` | `private` | `BluetoothLeScanner` | 42 |
| `mStartScanTime` | `private` | `long` | 43 |
| `mThread` | `private` | `Thread` | 44 |
| `mThreadDismiss` | `private` | `boolean` | 45 |
| `mPushStateMachineCtr` | `private` | `int` | 46 |
| `EQUIPMENT_CONNECT_CODE_NONE` | `private static` | `int` | 48 |
| `EQUIPMENT_CONNECT_CODE_BLE_NOT_ON` | `public final static` | `int` | 49 |
| `EQUIPMENT_CONNECT_CODE_BLE_FAILED` | `public final static` | `int` | 50 |
| `EQUIPMENT_CONNECT_CODE_BUSY` | `public final static` | `int` | 51 |
| `EQUIPMENT_CONNECT_CODE_INVALID_DATA` | `public final static` | `int` | 52 |
| `STATUS_NONE` | `public static` | `int` | 55 |
| `STATUS_IDLE` | `public final static` | `int` | 56 |
| `STATUS_CONNECTING` | `public final static` | `int` | 57 |
| `STATUS_SERVICE_FOUND` | `public final static` | `int` | 58 |
| `STATUS_AUTHENTICATED` | `public final static` | `int` | 59 |
| `STATUS_SETUP_RELAY_DONE` | `public final static` | `int` | 60 |
| `STATUS_SETUP_DONE` | `public final static` | `int` | 61 |
| `ble_status` | `public` | `int` | 62 |
| `relaySetDone` | package-private | `boolean` | 65 |
| `SCAN_PERIOD` | `public static final` | `int` | 68 |
| `CONNECT_PERIOD` | `public static final` | `int` | 69 |
| `SCAN_TIMEOUT` | `public static final` | `int` | 70 |
| `mBluetoothAdapter` | `public` | `BluetoothAdapter` | 71 |
| `bleScanner` | `public` | `BluetoothLeScanner` | 72 |
| `scanCallback` | `public` | `Object` | 73 |
| `equipmentListener` | `public` | `EquipmentListener` | 74 |
| `mScanning` | `public` | `boolean` | 75 |
| `mBleService` | `public` | `BleMachineService` | 76 |
| `mBleMachine` | package-private | `BleMachine` | 77 |
| `mContext` | `public` | `Context` | 78 |
| `mEquipmentItem` | `public` | `EquipmentItem` | 79 |
| `mBleDeviceAddress` | `public` | `String` | 80 |
| `mBleDevice` | package-private | `BluetoothDevice` | 81 |
| `mGattCharacteristics` | `public` | `ArrayList<BluetoothGattCharacteristic>` | 82 |
| `bleTimeSynced` | `public` | `boolean` | 83 |
| `bleThresholdSynced` | `public` | `boolean` | 84 |
| `bluetoothEnableReceiver` | package-private | `BroadcastReceiver` (anonymous) | 86 |
| `cachedBleDevices` | `public static` | `ArrayList<BluetoothDevice>` | 117 |
| `mServiceConnection` | `private final` | `ServiceConnection` (anonymous) | 163 |
| `clearRelayRetryTime` | `static` | `int` | 287 |
| `scanRetryCount` | `static` | `int` | 358 |
| `mStopRunnable` | `private` | `Runnable` (anonymous) | 430 |
| `leScanCallback` | `private` | `ScanCallback` (anonymous) | 437 |
| `mLeScanCallback` | `private` | `BluetoothAdapter.LeScanCallback` (anonymous) | 510 |
| `myHandler` | `public` | `Handler` | 732 |
| `timerDuration` | package-private | `int` | 733 |
| `timerRunnable` | package-private | `Runnable` (anonymous) | 734 |
| `ourInstance` | `private static` | `BleController` | 769 |

**Methods:**
| Method | Visibility | Line |
|---|---|---|
| `registerBluetoothEnableCallback()` | package-private | 104 |
| `unRegisterBluetoothEnable()` | package-private | 108 |
| `addDevice(BluetoothDevice)` | package-private | 118 |
| `getCachedDevice(String)` | package-private | 129 |
| `isDeviceSetupDone(String)` | `public` | 138 |
| `isDeviceDisconnected(String)` | `public` | 146 |
| `stillNeedToConnectEquipment()` | package-private | 155 |
| `onBleServiceConnected(IBinder)` | package-private | 179 |
| `onBleServiceDisconnected()` | `public` | 187 |
| `isBroadcastNeedToHandle(Intent)` | package-private | 192 |
| `getSupportedGattServices()` | `public` | 209 |
| `discoverServices()` | `public` | 217 |
| `autoReconnect()` | `public` | 227 |
| `startBleService()` | `private` | 237 |
| `startBleService(BluetoothDevice)` | `private` | 247 |
| `stopBleService()` | package-private | 268 |
| `stopConnection()` | `public` | 275 |
| `clearConnection()` | package-private | 289 |
| `clearRelay()` | package-private | 298 |
| `stopScanLeDevice()` | package-private | 324 |
| `stopScanner()` | package-private | 331 |
| `scanLeDevice()` | `private` | 342 |
| `scanDeviceFunc()` | package-private | 461 |
| `startScan()` | `public` | 377 |
| `stopScan()` | `public` | 402 |
| `preStartCheck(boolean, boolean, EquipmentItem, EquipmentListener)` | `public` | 530 |
| `preStart(EquipmentItem, EquipmentListener)` | package-private | 605 |
| `startConnect(boolean, boolean, EquipmentItem, EquipmentListener)` | `public` | 615 |
| `discoverDevice(boolean, EquipmentItem, EquipmentListener)` | package-private | 622 |
| `onSetupTimeout()` | package-private | 649 |
| `onFailed()` | package-private | 670 |
| `onSetupDone()` | package-private | 683 |
| `pushStateMachine()` | package-private | 697 |
| `onRelaySetDone()` | package-private | 724 |
| `startTimer()` | `public` | 744 |
| `getCharacteristic(String)` | package-private | 750 |
| `init(Context)` | `public` | 764 |
| `instance()` | `public static synchronized` | 770 |
| `BleController()` | `public` | 779 |

**Inner class `EquipmentListener` methods:**
| Method | Visibility | Line |
|---|---|---|
| `onSucceed()` | `public` | 661 |
| `onFailed(int)` | `public` | 665 |

---

### File 3: BleDataService.java
**Full path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/BLE/BleDataService.java`
**Class:** `BleDataService extends IntentService`

**Constants / Fields defined:**
| Name | Visibility | Type | Line |
|---|---|---|---|
| `ACTION_READ_SHOCK_COUNT` | `public static` | `String` | 18 |
| `TAG` | `public static` | `String` | 19 |
| `mBleMachine` | `static` (package-private) | `BleMachine` | 20 |
| `mBleController` | `static` (package-private) | `BleController` | 21 |

**Methods:**
| Method | Visibility | Line |
|---|---|---|
| `BleDataService()` constructor | `public` | 23 |
| `processBleEvents(Intent)` | `public` | 27 |
| `onHandleIntent(Intent)` | `protected` (override) | 58 |
| `sendAction(String)` | `public static` | 69 |
| `readShockEvent()` | `public` | 78 |
| `popShockEvent()` | package-private | 100 |
| `onShockDataRead(String, Intent)` | package-private | 119 |
| `onShockCountRead(Integer)` | package-private | 157 |
| `readShockCount()` | package-private | 175 |
| `sendData(Intent)` | `public static` | 206 |

**Types/Interfaces defined:** None (extends `IntentService`)

---

## Section 2 & 3: Findings

---

### A12-1 — HIGH — Deprecated `IntentService` in both service classes

**Files:** `BleControlService.java` line 20, `BleDataService.java` line 16

`IntentService` was deprecated in API level 30 (Android 11). Both service classes extend it without any `@SuppressWarnings` or migration note. Since the project's minimum SDK and target SDK are not visible in these files, this will produce build warnings at minimum and, on Android 14+ (API 34+) devices, may behave unexpectedly due to foreground service type requirements.

```java
// BleControlService.java:20
public class BleControlService extends IntentService {

// BleDataService.java:16
public class BleDataService extends IntentService {
```

Both also share the identical constructor argument `"ShockEventService"` as the worker thread name, which makes log attribution ambiguous when both are active simultaneously.

```java
// BleControlService.java:34
super("ShockEventService");

// BleDataService.java:24
super("ShockEventService");
```

---

### A12-2 — HIGH — Deprecated `BluetoothAdapter.LeScanCallback` and `startLeScan`/`stopLeScan`

**File:** `BleController.java` lines 338, 486, 510–511

`BluetoothAdapter.LeScanCallback`, `startLeScan()`, and `stopLeScan()` were deprecated in API 21 (Android 5.0 / Lollipop). The code has a modern `ScanCallback` path for API ≥ 21 in `scanDeviceFunc()`, but `mLeScanCallback` and its callers at lines 338 and 486 still use the old API for the pre-Lollipop fallback path. However, the same legacy callback is also used inside the modern `ScanCallback` at line 477 by delegating to `mLeScanCallback.onLeScan(...)`, creating a maintenance hazard even on modern devices. Given Android's minimum supported API has been well above 21 for years, the entire legacy path is dead weight.

```java
// BleController.java:510-511
private BluetoothAdapter.LeScanCallback mLeScanCallback =
        new BluetoothAdapter.LeScanCallback() {

// BleController.java:486
mBluetoothAdapter.startLeScan(mLeScanCallback);

// BleController.java:338
mBluetoothAdapter.stopLeScan(mLeScanCallback);
```

---

### A12-3 — HIGH — Deprecated `AsyncTask` used for BLE scan operations

**File:** `BleController.java` lines 17, 379, 403, 561

`AsyncTask` was deprecated in API level 30. It is used in `startScan()` (line 379), `stopScan()` (line 403), and `preStartCheck()` (line 561). The raw `new AsyncTask()` at line 561 uses the raw/unchecked form without type parameters, which also produces an unchecked-cast compiler warning. No `@SuppressWarnings` annotation is present.

```java
// BleController.java:561
new AsyncTask(){
    @Override
    protected Object doInBackground(Object[] params) {
```

---

### A12-4 — HIGH — `Thread.sleep()` called on IntentService worker thread and on static method callers

**Files:** `BleControlService.java` lines 117, 217, 252; `BleDataService.java` lines 81, 104, 186

Seven `Thread.sleep()` calls are scattered across the BLE logic. In `BleControlService` the sleeps (200 ms, 2000 ms, 1000 ms) occur inside `handleBleOperation()` and `afterWriteAttribute()`, which run on the `IntentService` worker thread — blocking the single-threaded queue and preventing any subsequent intent from being processed during the sleep. In `BleDataService`, `readShockEvent()`, `popShockEvent()`, and `readShockCount()` each sleep for 1000 ms, again on the worker thread. Additionally, `setRelayWithDelay()` (line 215–222, BleControlService) is a `public static` method that calls `Thread.sleep(2000)` directly — callers cannot know this will block their thread.

```java
// BleControlService.java:215-221
public static void setRelayWithDelay() {
    try {
        Thread.sleep(2*1000);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    mBleMachine.setRelay(true);
}
```

All `InterruptedException` catches only call `e.printStackTrace()`, swallowing the interrupt signal and never restoring the interrupt flag (proper pattern: `Thread.currentThread().interrupt()`).

---

### A12-5 — HIGH — Duplicate retry call in `handleBleOperation` on auth failure — incorrect retry logic

**File:** `BleControlService.java` lines 111–113

When `mBleMachine.authDevice()` returns `false`, the code calls `mBleMachine.authDevice()` a second time immediately without any back-off or state check. This is not routed through a delay mechanism (unlike all other operation retries in the same method), making it an inconsistent one-shot immediate retry that may collide with ongoing BLE operations.

```java
// BleControlService.java:110-114
if(action.equals(ACTION_AUTH_DEVICE)){
    result = mBleMachine.authDevice();
    if(!result){
        mBleMachine.authDevice();   // immediate retry, result discarded
    }
    else {
```

The return value of the retry call at line 113 is also discarded, so a second failure is silently ignored.

---

### A12-6 — HIGH — Null pointer risk: `equipmentItem` accessed after null check at `preStartCheck`

**File:** `BleController.java` lines 541–547

The null-check for `equipmentItem` at line 541 is performed correctly, but if `equipmentItem` is `null`, the code inside the `if` block attempts to call `equipmentItem.mac_address` (line 545) to produce the log message, causing an immediate `NullPointerException` before the method can return.

```java
// BleController.java:541-547
if(equipmentItem == null) {
    if(listener != null) {
        listener.onFailed(EQUIPMENT_CONNECT_CODE_INVALID_DATA);
    }
    Log.d(TAG,"start connect invalid data return device " + equipmentItem.mac_address); // NPE here
    return;
}
```

---

### A12-7 — HIGH — Null pointer risk: `mBluetoothAdapter` checked after dereference in `startScan`, `stopScan`, and `leScanCallback`

**File:** `BleController.java** lines 386–387, 410–411, 442–443

In all three locations the condition is written as:
```java
if((mBluetoothAdapter.getState() != BluetoothAdapter.STATE_ON) &&
        (mBluetoothAdapter != null)){
```
The null check is on the right side of `&&`, so `mBluetoothAdapter.getState()` is called first. If `mBluetoothAdapter` is `null`, this throws a `NullPointerException` before the null guard is evaluated. The correct order is `mBluetoothAdapter != null && mBluetoothAdapter.getState() != ...`.

---

### A12-8 — MEDIUM — Large block of commented-out code in `BleController.java`

**File:** `BleController.java`

Multiple substantial blocks of commented-out code remain in the file. They represent alternative implementation strategies that were abandoned but never deleted:

- Lines 419–424: timeout-based scan failure path inside `stopScan()`.
- Lines 453–457: alternative scan-timeout path in `leScanCallback`.
- Lines 489–505: scan retry loop with `MyApplication.runLater` in `scanDeviceFunc()` (~17 lines).
- Lines 582–601: alternative `MyApplication.runOnAsyncTask` block in `preStartCheck()` (~20 lines).
- Lines 627–646: alternative cached-device / `scanLeDevice()` / setup-timeout path in `discoverDevice()` (~20 lines).

Example:
```java
// BleController.java:489-505
//        MyApplication.runLater(new Runnable() {
//            @Override
//            public void run() {
//                if(mScanning){
//                    stopScanLeDevice();
//                    scanRetryCount++;
//                    ...
//                }
//            }
//        },4000);
```

---

### A12-9 — MEDIUM — Commented-out code in `BleControlService.java`

**File:** `BleControlService.java` lines 64–73

A multi-line anonymous `EquipmentListener` instantiation is commented out inside the `ACTION_GATT_DISCONNECTED` handler, representing an abandoned auto-reconnect strategy. The surrounding comment (`// do not autoreconnect, notify user to choose instead`) indicates intent, but leaving 10 lines of dead code in place is not acceptable.

```java
// BleControlService.java:63-73
// do not autoreconnect, notify user to choose instead
//                    BleController.instance().equipmentListener = new BleController.EquipmentListener(){
//                        @Override
//                        public void onSucceed() {
//                        }
//
//                        @Override
//                        public void onFailed(int errorCode) {
//                            //sendActionWithDelay(ACTION_AUTO_RECONNECT,5000);
//                        }
//                    };
```

---

### A12-10 — MEDIUM — `scanCallback` field typed as `Object` — leaky internal abstraction

**File:** `BleController.java** line 73

The field `scanCallback` is declared `public Object scanCallback`. Its actual runtime type is `ScanCallback` (set at line 473 and cast back at line 334 and 482). Callers outside the class must know this internal convention and perform unchecked casts. The field should be typed as `ScanCallback` (or at minimum marked private).

```java
// BleController.java:73
public Object scanCallback;

// Usage at line 334:
bleScanner.stopScan((ScanCallback) scanCallback);
```

---

### A12-11 — MEDIUM — `ble_status` is a `public` mutable field; STATUS constants initialized via mutable side-effects

**File:** `BleController.java** lines 55–62

The status constants are initialized using the pre-increment pattern on a mutable static field:
```java
public static int STATUS_NONE = 0;
public final static int STATUS_IDLE = ++STATUS_NONE;     // STATUS_NONE is now 1
public final static int STATUS_CONNECTING = ++STATUS_NONE; // STATUS_NONE is now 2
...
```
`STATUS_NONE` is not `final`, so it can be modified externally, potentially corrupting the values of the already-initialized `final` fields or causing unexpected behavior if class loading is re-triggered. The same pattern is used for `EQUIPMENT_CONNECT_CODE_NONE` at line 48. Additionally, `ble_status` at line 62 is `public` and directly mutated by callers in other classes (e.g., `BleControlService.java` lines 74, 78), bypassing any encapsulation.

---

### A12-12 — MEDIUM — Excessive public surface area on `BleController` singleton

**File:** `BleController.java`

The following fields that represent internal BLE state are declared `public`, exposing them to all consumers and making the class impossible to refactor safely:
- `mBluetoothAdapter` (line 71)
- `bleScanner` (line 72)
- `scanCallback` (line 73) — also typed `Object`; see A12-10
- `equipmentListener` (line 74)
- `mScanning` (line 75)
- `mBleService` (line 76)
- `mContext` (line 78)
- `mEquipmentItem` (line 79)
- `mBleDeviceAddress` (line 80)
- `mGattCharacteristics` (line 82)
- `bleTimeSynced` (line 83)
- `bleThresholdSynced` (line 84)
- `myHandler` (line 732)

Fourteen internal-state fields are `public`, which is a severe abstraction leak.

---

### A12-13 — MEDIUM — `TAG` fields are `public static` in service classes; inconsistent visibility and naming

**Files:** `BleControlService.java` line 30, `BleDataService.java` line 19; `BleController.java` line 35

In `BleControlService`, `TAG` is `public static String` (not `final`). In `BleDataService`, `TAG` is also `public static String` (not `final`). In `BleController`, `TAG` is `private final String` (correct). Log tags should be `private static final String`. The non-`final` declarations allow external modification of log tags at runtime.

```java
// BleControlService.java:30
public static String TAG = "CI_BLE_" + BleControlService.class.getSimpleName();

// BleDataService.java:19
public static String TAG = "CI_BLE_SHOCK_EVENT" + BleDataService.class.getSimpleName();

// BleController.java:35
private final String TAG = "CI_BLE"; // correct pattern but not static
```

---

### A12-14 — MEDIUM — `mBleMachine` is a `static` field in both services; unsafe cross-service state sharing

**Files:** `BleControlService.java` line 31, `BleDataService.java` line 20

Both `BleControlService.mBleMachine` and `BleDataService.mBleMachine` are `static` fields lazily initialized in `onHandleIntent`. Because `IntentService` uses a single worker thread per service instance, these statics are initialized once and then permanently retained. If the `BleController` singleton is ever replaced or reset, these statics become stale references to the old `BleMachine` instance. There is no synchronization on the write, only a null check:

```java
// BleControlService.java:177-179
if(null == mBleMachine){
    mBleMachine = BleController.instance().mBleMachine;
}
```

`BleDataService` also caches `BleController.instance()` itself as a static:
```java
// BleDataService.java:21
static BleController mBleController = null;
```
This defeats the singleton pattern's update path if the controller is ever re-created.

---

### A12-15 — MEDIUM — `readShockCount()` recursive self-call with no depth limit

**File:** `BleDataService.java` lines 199–201

`readShockCount()` calls itself recursively on failure with a 1000 ms sleep before each attempt, but there is no guard against infinite recursion:

```java
// BleDataService.java:196-203
boolean r = mBleMachine.readCharacteristic(characteristic);
...
if(!r){
    readShockCount();
}
return r;
```

On a persistently broken BLE connection this will grow the call stack unboundedly until `StackOverflowError`. The same pattern is present in `onShockCountRead()` at line 167 which can call `readShockCount()` → `readShockEvent()` → `readShockCount()` in a cycle.

---

### A12-16 — MEDIUM — `stopConnection()` is missing disconnect from `BleService`; inconsistent teardown

**File:** `BleController.java` lines 275–285

`stopConnection()` handles scan teardown but does not call `stopBleService()` or `clearConnection()`. The disconnect is only called from `clearRelay()`, which `stopConnection()` calls — but `clearRelay()` dispatches `clearConnection()` asynchronously with a 5-second delay. This means there is a 5-second window during which the GATT connection is held open after the caller expects the connection to be stopped.

```java
// BleController.java:275-285
public void stopConnection() {
    clearRelay();
    unRegisterBluetoothEnable();
    //stopScanLeDevice();
    if(mIsScanning) {
        mIsScanning = false;
        mLEScanner.stopScan(leScanCallback);
    }
}
```

The commented-out `stopScanLeDevice()` at line 279 also leaves the `mScanning` field (the `scanDeviceFunc` scanner) potentially stuck as `true` after `stopConnection()`.

---

### A12-17 — MEDIUM — `scanLeDevice()` is `private` and unreachable; dead method

**File:** `BleController.java** lines 342–356

`scanLeDevice()` is a `private` method that initializes the `mLEScanner`-based scan. It is never called from within the class (all active call sites instead call `startScan()` or `scanDeviceFunc()`). It is referenced only inside commented-out blocks in `discoverDevice()` (lines 635–636). It is effectively dead code.

```java
// BleController.java:342
private void scanLeDevice() {
```

---

### A12-18 — MEDIUM — `mThread`, `mThreadDismiss`, `mPushStateMachineCtr`, `mList`, `mBleDevice` are unused private/package-private fields

**File:** `BleController.java` lines 40, 44, 45, 46, 81

The following fields are declared but never written or read anywhere within the file (beyond their declaration):
- `mList` (line 40) — set to `null` in `initializeVariables` at line 364 but never otherwise used
- `mThread` (line 44) — set to `null` in `initializeVariables` at line 372 but never used
- `mThreadDismiss` (line 45) — set to `false` in `initializeVariables` at line 373 but never read
- `mPushStateMachineCtr` (line 46) — set to `0` in `initializeVariables` at line 374 but never read
- `mBleDevice` (line 81) — assigned `null` at declaration, never written or read again
- `scanRetryCount` (line 358) — set to `0` in `scanLeDevice()` at line 354; `scanLeDevice()` is itself dead (see A12-17); the only other write is inside commented-out code (line 496)

---

### A12-19 — MEDIUM — `onSetupTimeout()` is never called; dead method

**File:** `BleController.java` lines 649–657

`onSetupTimeout()` is only referenced inside commented-out code in `discoverDevice()` (line 644). No live code path calls it.

```java
// BleController.java:649
void onSetupTimeout() {
```

---

### A12-20 — LOW — `address.toLowerCase().equalsIgnoreCase(...)` redundant double case-fold

**File:** `BleController.java` line 202

```java
if(address == null || !address.toLowerCase().equalsIgnoreCase(mBleDeviceAddress)){
```

`equalsIgnoreCase` is already case-insensitive; calling `toLowerCase()` first is redundant. The same pattern is referenced consistently with correct `equalsIgnoreCase` elsewhere (lines 122, 449, 519), making this an inconsistency.

---

### A12-21 — LOW — `getCharacteristic()` uses `s.toLowerCase().equalsIgnoreCase(uuid)` redundant double case-fold

**File:** `BleController.java` line 757

```java
String s = characteristic.getUuid().toString();
if(s.toLowerCase().equalsIgnoreCase(uuid)){
```

Same redundant pattern as A12-20.

---

### A12-22 — LOW — Action string namespacing inconsistency: `ACTION_SET_TIME` is missing `ACTION_` prefix in its value

**File:** `BleControlService.java` line 26

All action constants follow the pattern `"com.BleDataService.ACTION_<NAME>"` except `ACTION_SET_TIME`:
```java
private static String ACTION_SET_TIME = "com.BleDataService.SET_TIME"; // missing ACTION_
```
All others use `"com.BleDataService.ACTION_*"`. This is a style inconsistency that could cause confusion if the string value is ever matched externally.

---

### A12-23 — LOW — `unRegisterBluetoothEnable` swallows all exceptions silently

**File:** `BleController.java` lines 108–115

```java
void unRegisterBluetoothEnable(){
    try {
        LocalBroadcastManager.getInstance(MyApplication.getContext()).unregisterReceiver(bluetoothEnableReceiver);
    }
    catch (Exception e){

    }
}
```

The catch block is completely empty — no log, no re-throw, no handling. This masks all failures during receiver unregistration.

---

### A12-24 — LOW — `stopBleService()` calls `mBleService.onUnbind(new Intent())`

**File:** `BleController.java` lines 268–273

```java
void stopBleService(){
    if(mBleService != null){
        mBleService.disconnect();
        mBleService.onUnbind(new Intent());
    }
}
```

`onUnbind()` is a lifecycle callback on `Service` intended to be called by the Android framework, not by application code. Calling it manually may interfere with the framework's own lifecycle management, especially since the service was bound via `bindService()`. The correct approach is to call `mContext.unbindService(mServiceConnection)`.

---

### A12-25 — LOW — `mBleController.STATUS_SETUP_DONE` accessed as instance field rather than class constant

**File:** `BleDataService.java` lines 88, 121, 160, 180

`STATUS_SETUP_DONE` and `STATUS_IDLE` are `public static final` constants on `BleController`, but they are accessed through the instance reference `mBleController.STATUS_SETUP_DONE` / `mBleController.ble_status != mBleController.STATUS_SETUP_DONE`. This generates IDE/lint warnings and obscures that these are class-level constants.

```java
// BleDataService.java:88
if(mBleController.ble_status != mBleController.STATUS_SETUP_DONE) {
```

---

### A12-26 — INFO — `getCachedDevice()` and `addDevice()` accumulate `cachedBleDevices` unboundedly

**File:** `BleController.java** lines 117–136

`cachedBleDevices` is a `public static ArrayList` that is never cleared (no call to `clear()` except for `mDevicesDiscovered` at line 378). Every scanned BLE device address is permanently added. On busy BLE environments this list will grow indefinitely for the lifetime of the process.

---

### A12-27 — INFO — Constructor argument `"ShockEventService"` duplicated across both service classes

**Files:** `BleControlService.java` line 34, `BleDataService.java` line 24

Both classes pass the identical string `"ShockEventService"` to `IntentService`'s constructor as the worker-thread name. This makes it impossible to distinguish log output from the two threads.

---

## Section 4: Summary Table

| ID | Severity | File(s) | Description |
|---|---|---|---|
| A12-1 | HIGH | BleControlService.java, BleDataService.java | Both extend deprecated `IntentService` (API 30+); identical worker thread name |
| A12-2 | HIGH | BleController.java | Deprecated `BluetoothAdapter.LeScanCallback`, `startLeScan`, `stopLeScan` |
| A12-3 | HIGH | BleController.java | Deprecated `AsyncTask` used in scan and pre-start logic |
| A12-4 | HIGH | BleControlService.java, BleDataService.java | `Thread.sleep()` on worker threads; interrupt signals swallowed |
| A12-5 | HIGH | BleControlService.java | Auth-device retry calls `authDevice()` immediately with discarded result |
| A12-6 | HIGH | BleController.java | NPE in `preStartCheck()` when `equipmentItem` is null (log call before return) |
| A12-7 | HIGH | BleController.java | Null-before-guard: `mBluetoothAdapter.getState()` checked before null guard in 3 locations |
| A12-8 | MEDIUM | BleController.java | ~70 lines of commented-out code across 5 blocks |
| A12-9 | MEDIUM | BleControlService.java | 10 lines of commented-out anonymous `EquipmentListener` |
| A12-10 | MEDIUM | BleController.java | `scanCallback` typed as `Object`, requiring unchecked casts |
| A12-11 | MEDIUM | BleController.java | `STATUS_NONE` / `EQUIPMENT_CONNECT_CODE_NONE` are mutable statics; `ble_status` is public |
| A12-12 | MEDIUM | BleController.java | 14 internal-state fields declared `public` |
| A12-13 | MEDIUM | BleControlService.java, BleDataService.java | `TAG` is `public static` non-`final`; inconsistent with `BleController` |
| A12-14 | MEDIUM | BleControlService.java, BleDataService.java | `static` `mBleMachine` / `mBleController` caches may become stale |
| A12-15 | MEDIUM | BleDataService.java | `readShockCount()` recursion with no depth limit; potential `StackOverflowError` |
| A12-16 | MEDIUM | BleController.java | `stopConnection()` leaves scan state dirty; 5-second GATT teardown delay |
| A12-17 | MEDIUM | BleController.java | `scanLeDevice()` is dead (private, never called from live code) |
| A12-18 | MEDIUM | BleController.java | 6 unused fields: `mList`, `mThread`, `mThreadDismiss`, `mPushStateMachineCtr`, `mBleDevice`, `scanRetryCount` |
| A12-19 | MEDIUM | BleController.java | `onSetupTimeout()` is dead (only referenced in commented-out code) |
| A12-20 | LOW | BleController.java | Redundant `.toLowerCase().equalsIgnoreCase()` in `isBroadcastNeedToHandle()` |
| A12-21 | LOW | BleController.java | Redundant `.toLowerCase().equalsIgnoreCase()` in `getCharacteristic()` |
| A12-22 | LOW | BleControlService.java | `ACTION_SET_TIME` value missing `ACTION_` prefix unlike all peers |
| A12-23 | LOW | BleController.java | Empty catch block in `unRegisterBluetoothEnable()` |
| A12-24 | LOW | BleController.java | `mBleService.onUnbind()` called directly by application code |
| A12-25 | LOW | BleDataService.java | Static constants accessed via instance reference `mBleController.STATUS_SETUP_DONE` |
| A12-26 | INFO | BleController.java | `cachedBleDevices` grows unboundedly; never cleared |
| A12-27 | INFO | BleControlService.java, BleDataService.java | Identical worker thread name `"ShockEventService"` in both services |

**Total findings: 27** (7 HIGH, 12 MEDIUM, 5 LOW, 2 INFO)
