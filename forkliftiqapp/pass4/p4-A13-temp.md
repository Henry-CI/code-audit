# Audit Report — Pass 4: Code Quality
**Audit run:** 2026-02-26-01
**Agent:** A13
**Files reviewed:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/BLE/BleMachine.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/BLE/BleMachineService.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/BLE/BleModel.java`

---

## Section 1: Reading Evidence

### File 1 — BleMachine.java

**Class:** `BleMachine`
**Package:** `au.com.collectiveintelligence.fleetiq360.WebService.BLE`

**Fields:**
| Name | Type | Visibility | Line |
|---|---|---|---|
| `TAG` | `String` (final) | private | 18 |
| `mBleController` | `BleController` | package-private | 19 |
| `expectingRelayValue` | `int` | public | 20 |
| `expectingTimeItem` | `BleUtil.BleTimeItem` | public | 21 |
| `expectingImpactThreshold` | `int` | public | 22 |

**Methods:**
| Method | Visibility | Line |
|---|---|---|
| `BleMachine(BleController)` (constructor) | public | 24 |
| `authDevice()` | package-private | 28 |
| `onServiceFound()` | package-private | 46 |
| `onAuthDone()` | package-private | 76 |
| `disableShockNotification()` | package-private | 83 |
| `setShockNotification()` | package-private | 96 |
| `setRelay(boolean)` | package-private | 109 |
| `clearRelay()` | package-private | 133 |
| `logTime(String, BleUtil.BleTimeItem)` | package-private | 149 |
| `setTime()` | package-private | 155 |
| `setImpactThreshold()` | package-private | 174 |
| `setRelayTimeout()` | package-private | 198 |
| `setRelayTimeout(String)` (private overload) | private | 204 |
| `writeCharacteristic(BluetoothGattCharacteristic)` | package-private | 215 |
| `readCharacteristic(BluetoothGattCharacteristic)` | package-private | 222 |
| `onBleDataRead(Intent)` | package-private | 229 |
| `onGattServices(List<BluetoothGattService>)` | package-private | 289 |

**Types/constants defined:** None beyond fields above.

---

### File 2 — BleMachineService.java

**Class:** `BleMachineService extends Service`
**Inner class:** `LocalBinder extends Binder` (line 243)
**Package:** `au.com.collectiveintelligence.fleetiq360.WebService.BLE`

**Fields:**
| Name | Type | Visibility | Line |
|---|---|---|---|
| `TAG` | `String` (final static) | private | 43 |
| `mBluetoothManager` | `BluetoothManager` | private | 45 |
| `mBluetoothAdapter` | `BluetoothAdapter` | private | 46 |
| `mBleDeviceAddress` | `String` | private | 47 |
| `mBluetoothGatt` | `BluetoothGatt` | private | 48 |
| `mConnectionState` | `int` | private | 49 |
| `STATE_DISCONNECTED` | `int` (final static) | public | 51 |
| `STATE_CONNECTING` | `int` (final static) | private | 52 |
| `STATE_CONNECTED` | `int` (final static) | private | 53 |
| `ACTION_GATT_CONNECTED` | `String` (final static) | public | 55 |
| `ACTION_GATT_DISCONNECTED` | `String` (final static) | public | 56 |
| `ACTION_GATT_SERVICES_DISCOVERED` | `String` (final static) | public | 57 |
| `ACTION_DATA_AVAILABLE` | `String` (final static) | public | 58 |
| `ACTION_DATA_WRITE` | `String` (final static) | public | 59 |
| `ACTION_DATA_CHANGED` | `String` (final static) | public | 60 |
| `CHARA_UUID` | `String` (final static) | public | 61 |
| `EXTRA_DATA` | `String` (final static) | public | 62 |
| `DEVICE_ADDRESS` | `String` (final static) | public | 63 |
| `STATUS_CODE` | `String` (final static) | public | 64 |
| `mGattCallback` | `BluetoothGattCallback` (final) | private | 72 |
| `mBinder` | `IBinder` (final) | private | 260 |

**Methods:**
| Method | Visibility | Line |
|---|---|---|
| `discoverServices()` | public | 67 |
| `onConnectionStateChange(BluetoothGatt, int, int)` (callback) | public | 74 |
| `onServicesDiscovered(BluetoothGatt, int)` (callback) | public | 101 |
| `onCharacteristicRead(BluetoothGatt, BluetoothGattCharacteristic, int)` (callback) | public | 112 |
| `onCharacteristicChanged(BluetoothGatt, BluetoothGattCharacteristic)` (callback) | public | 121 |
| `onCharacteristicWrite(BluetoothGatt, BluetoothGattCharacteristic, int)` (callback) | public | 130 |
| `connect(String)` | public | 137 |
| `connect(BluetoothDevice)` | public | 155 |
| `startConnect(BluetoothDevice)` | package-private | 172 |
| `disconnect()` | public | 179 |
| `close()` | public | 187 |
| `readCharacteristic(BluetoothGattCharacteristic)` | public | 195 |
| `writeCharacteristic(BluetoothGattCharacteristic)` | public | 206 |
| `setCharacteristicNotification(BluetoothGattCharacteristic, boolean)` | public | 216 |
| `getSupportedGattServices()` | public | 237 |
| `LocalBinder.getService()` | package-private (inner class method) | 244 |
| `onBind(Intent)` | public | 250 |
| `onUnbind(Intent)` | public | 255 |
| `broadcastUpdate(String, String)` | private | 262 |
| `broadcastUpdate(boolean, String, String, BluetoothGattCharacteristic)` | private | 266 |
| `initialize()` | public | 282 |

---

### File 3 — BleModel.java

**Class:** `BleModel`
**Package:** `au.com.collectiveintelligence.fleetiq360.WebService.BLE`

**Constants (public final static String):**
| Name | Value summary | Line |
|---|---|---|
| `UUID_BLE_TIME` | `00002a2b-...` | 13 |
| `UUID_BLE_DEVICE_NAME` | `00002a00-...` | 14 |
| `UUID_BLE_MANUFACTURE` | `00002a29-...` | 15 |
| `UUID_BLE_MODEL` | `00002a24-...` | 16 |
| `UUID_SHOCK_COUNT` | `69dfccac-...` | 17 |
| `UUID_SHOCK_EVENT_ITEM` | `53535322-...` | 18 |
| `UUID_POP_SHOCK_EVENT` | `1642fcc6-...` | 19 |
| `UUID_SHOCK_THRESHOLD` | `6d3f3a08-...` | 20 |
| `UUID_RELAY_0` | `3cfd3551-...` | 21 |
| `UUID_RELAY_1` | `1ffbb954-...` | 22 |
| `UUID_TOKEN_AUTH` | `6d1e95a3-...` | 23 |
| `TOKEN_AUTH` | `"uS8MgpklMx"` | 24 |
| `UUID_RELAY_0_TIMEOUT` | `e4d93331-...` | 26 |
| `UUID_RELAY_1_TIMEOUT` | `465330b5-...` | 27 |
| `CLIENT_CHARACTERISTIC_CONFIG` | `00002902-...` | 29 |

**Package-private constants:**
| Name | Line |
|---|---|
| `basePath` | 32 |
| `PATH_VERSION_MAIN` | 33 |
| `PATH_VERSION_RADIO` | 34 |
| `PATH_SHOCK_EVENT_THRESHOLD` | 35 |
| `PATH_SHOCK_EVENT_POP` | 36 |
| `PATH_SHOCK_EVENT` | 37 |
| `PATH_SHOCK_EVENT_COUNT` | 38 |

**Fields:**
| Name | Type | Visibility | Line |
|---|---|---|---|
| `mapUuidForPath` | `HashMap<String,String>` | package-private | 39 |
| `ourInstance` | `BleModel` (static) | private | 41 |

**Methods:**
| Method | Visibility | Line |
|---|---|---|
| `instance()` | public static | 42 |
| `BleModel()` (constructor) | public | 52 |
| `getPrimaryRelayId()` | public | 56 |
| `getRelayId(int)` | public | 60 |
| `initUuids()` | private | 70 |
| `getPathExternalRelayKey(int)` | public | 85 |
| `getUUIDFromPath(String)` | public | 89 |

---

## Section 2 & 3: Findings

---

### A13-1 — CRITICAL: Authentication token stored as plaintext constant

**File:** `BleModel.java`, line 24
**Category:** Security / Build Warning

```java
public final static String TOKEN_AUTH = "uS8MgpklMx";
```

The BLE authentication token is hardcoded as a public static final String constant. It is committed directly in source and will appear verbatim in the compiled `.apk` (extractable with `strings` or a decompiler). Any actor with the `.apk` can replay the token against any ForkliftIQ360 BLE device.

---

### A13-2 — HIGH: Commented-out code block — authentication response handler removed

**File:** `BleMachine.java`, lines 243–249
**Category:** Commented-out code / Dead code

```java
//            Log.d(TAG,"auth device  return " + actionSucceed);
//            if(actionSucceed) {
//                pushStateMachine();
//            }
//            else {
//                authDevice();
//            }
```

This is the entire body of the `UUID_TOKEN_AUTH` branch in `onBleDataRead()`. It is commented out and the `if` block is now empty. The result is that authentication write responses are silently ignored: the code never verifies that authentication actually succeeded on the device side. Removing or ignoring the response means auth failures are never detected. The commented block should either be reinstated with appropriate logic or replaced with a deliberate alternative.

---

### A13-3 — HIGH: Commented-out code block — auto-reconnect listener

**File:** `BleControlService.java`, lines 64–73
**Category:** Commented-out code

```java
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

A listener assignment (and a nested `sendActionWithDelay` comment within it) is commented out. This is referenced context for the `BleControlService.java` file read during evidence collection and is directly adjacent to the files under audit. The block indicates incomplete work on auto-reconnect behaviour after a `STATUS_SETUP_DONE` disconnect. This should be deleted or reinstated.

---

### A13-4 — HIGH: Null-pointer dereference risk in `setCharacteristicNotification`

**File:** `BleMachineService.java`, lines 228–232
**Category:** Dead code path / build warning

```java
BluetoothGattDescriptor descriptor = characteristic.getDescriptor(
        UUID.fromString(BleModel.CLIENT_CHARACTERISTIC_CONFIG));
descriptor.setValue(BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE);
return mBluetoothGatt.writeDescriptor(descriptor);
```

`characteristic.getDescriptor(...)` can return `null` if the descriptor is absent (e.g., for a custom characteristic). The returned reference is used immediately without a null check. A `NullPointerException` will crash the calling thread at runtime when the descriptor is not present. This is a latent crash bug.

---

### A13-5 — HIGH: Dead `boolean r` variable — result of `discoverServices()` silently dropped

**File:** `BleMachineService.java`, lines 68–71
**Category:** Dead code / Build warning

```java
public void discoverServices(){
    if(mBluetoothGatt != null){
        boolean r = mBluetoothGatt.discoverServices();
    }
}
```

The return value of `discoverServices()` is captured into a local variable `r` that is never read. Modern Android linters (`lint`, Android Studio inspections) will flag this as an unused variable. The same pattern appears inside `onConnectionStateChange` at line 83 where `boolean r = mBluetoothGatt.discoverServices()` is also discarded without logging or error handling. Discovery failures are silently lost.

---

### A13-6 — HIGH: Dead `boolean r` variable in `onConnectionStateChange`

**File:** `BleMachineService.java`, line 83
**Category:** Dead code / Build warning

```java
boolean r = mBluetoothGatt.discoverServices();
Log.i(TAG, "Attempting to startConnect service discovery:" + r);
```

In `onConnectionStateChange` the result `r` is logged. However, in `discoverServices()` (line 69), an identical `boolean r` is silently dropped with no log and no error path. These two call-sites for the same method follow inconsistent error-handling patterns (one logs, one does not). See also A13-5.

---

### A13-7 — HIGH: Dead-code null check after guaranteed non-null

**File:** `BleMachineService.java`, lines 155–168
**Category:** Dead code

```java
public boolean connect(final BluetoothDevice device) {
    if (mBluetoothAdapter == null || device == null) {   // device null-checked here
        ...
        return false;
    }

    mBleDeviceAddress = device.getAddress();
    if (device == null) {                                 // device checked again — always false
        Log.w(TAG, "Device not found.  Unable to connect.");
        return false;
    }
    ...
}
```

The second `if (device == null)` guard at line 162 is unreachable: the method already returned at line 157–160 if `device` was null. The dead branch and its log message ("Device not found. Unable to connect.") are copy-paste residue from the `connect(String)` overload. It misleads readers and will never execute.

---

### A13-8 — MEDIUM: Inconsistent visibility of `STATE_DISCONNECTED` vs `STATE_CONNECTING` / `STATE_CONNECTED`

**File:** `BleMachineService.java`, lines 51–53
**Category:** Style inconsistency / Leaky abstraction

```java
public static final int STATE_DISCONNECTED = 0;
private static final int STATE_CONNECTING = 1;
private static final int STATE_CONNECTED = 2;
```

`STATE_DISCONNECTED` is `public` while the other two state constants are `private`. No external caller in the audited codebase references `STATE_DISCONNECTED` by name (it is accessed via the `mConnectionState` field, which is itself private). Exposing one of three tightly related internal state constants is inconsistent and leaks implementation detail.

---

### A13-9 — MEDIUM: Inconsistent boolean negation / inverted success semantics in `authDevice()`

**File:** `BleMachine.java`, lines 28–44
**Category:** Style inconsistency

```java
boolean authDevice() {
    if (mBleController.ble_status != BleController.STATUS_SERVICE_FOUND) {
        return true;   // "true" when precondition fails (nothing written)
    }
    ...
    boolean r = writeCharacteristic(characteristic);
    return r;          // "true" when write succeeds
}
```

Callers in `onServiceFound()` (line 63) interpret the return value as follows:

```java
if (authDevice()) {
    MyApplication.runLater(... onAuthDone() ..., 200);
} else {
    BleControlService.authDevice();
}
```

The method returns `true` both when the status precondition is not met (nothing was sent to device) AND when the write succeeded. The `else` branch (retry via `BleControlService.authDevice()`) is only reached when the write failed. A precondition-fail case silently behaves like success and triggers `onAuthDone()`. This inverted / overloaded boolean meaning makes the control flow incorrect and difficult to reason about.

The same inverted pattern appears in `disableShockNotification()` (line 89), `setShockNotification()` (line 101), `setRelay()` (line 113, 120), `clearRelay()` (line 134, 139), `setTime()` (line 165), `setImpactThreshold()` (line 187), and `setRelayTimeout()` (line 134) — returning `true` on both success and silent no-op.

---

### A13-10 — MEDIUM: Broken conditional in `disableShockNotification` / `setShockNotification`

**File:** `BleMachine.java`, lines 83–107
**Category:** Dead code / Logic bug

```java
boolean disableShockNotification() {
    if (mBleController.ble_status < mBleController.STATUS_SETUP_DONE)
        Log.d(TAG, "disableShockNotification enter");   // no braces — only Log is guarded
    BluetoothGattCharacteristic characteristic = ...    // always executes
```

The `if` at line 84 has no curly braces. Only the `Log.d` call on line 85 is inside the condition; the characteristic lookup and all subsequent logic on lines 86–94 execute unconditionally. The developer almost certainly intended to early-return if status is below `STATUS_SETUP_DONE`, as all peer methods (`setRelay`, `clearRelay`, `setTime`, `setImpactThreshold`) do. The identical bug appears in `setShockNotification()` (lines 97–98). Both methods will attempt GATT operations regardless of state.

---

### A13-11 — MEDIUM: Hardcoded magic constant for relay timeout value

**File:** `BleMachine.java`, line 210
**Category:** Style / maintainability

```java
relayTimeout.setValue(60, BluetoothGattCharacteristic.FORMAT_UINT16, 0);
```

The timeout value `60` is a bare literal with no explanation of units (seconds? minutes?). Every other numeric sentinel in the file is either given a name (`BleController.STATUS_SETUP_DONE`, format constants) or explained in a comment. This value should be extracted to a named constant.

---

### A13-12 — MEDIUM: Hardcoded magic constant for default impact threshold

**File:** `BleMachine.java`, line 182
**Category:** Style / maintainability

```java
temp_impact_threshold = 80000;
```

When `impact_threshold` is zero the code silently substitutes `80000` without any constant name or unit annotation. The rationale for this specific fallback value is undocumented.

---

### A13-13 — MEDIUM: `BleModel` singleton is not thread-safe

**File:** `BleModel.java`, lines 41–50
**Category:** Style inconsistency / concurrency

```java
private static BleModel ourInstance;
public static BleModel instance() {
    if (ourInstance == null){
        ourInstance = new BleModel();
    }
    return ourInstance;
}
```

The singleton is initialized with a simple null check and no synchronization. BLE callbacks arrive on the GATT thread while UI operations occur on the main thread; concurrent first-access from two threads can produce two instances, with one discarded, or leave `ourInstance` partially constructed and visible to the second thread. The field is neither `volatile` nor is the block `synchronized`.

---

### A13-14 — MEDIUM: `CLIENT_CHARACTERISTIC_CONFIG` is not `final`

**File:** `BleModel.java`, line 29
**Category:** Style inconsistency

```java
public static String CLIENT_CHARACTERISTIC_CONFIG = "00002902-0000-1000-8000-00805f9b34fb";
```

Every other UUID constant in the same class is declared `public final static String`. `CLIENT_CHARACTERISTIC_CONFIG` omits `final`, making it mutable. Any code holding a reference to `BleModel.CLIENT_CHARACTERISTIC_CONFIG` can reassign it, breaking notification subscription for the entire session. This is inconsistent and dangerous.

---

### A13-15 — MEDIUM: Deprecated `IntentService` used in `BleControlService`

**File:** Context from `BleControlService.java`, line 20
**Category:** Build warning / deprecated API

```java
public class BleControlService extends IntentService {
```

`IntentService` was deprecated in API level 30 (Android 11). The `BleMachineService` and `BleMachine` classes under audit are tightly coupled to `BleControlService` via static method calls (`BleControlService.authDevice()`, `BleControlService.afterWriteAttribute()`, etc.). The deprecation of the underlying service impacts the audited files transitively.

---

### A13-16 — MEDIUM: `sendBroadcast` replaced by static call — architecture comment left in code

**File:** `BleMachineService.java`, line 278
**Category:** Commented-out code

```java
//sendBroadcast(intent);
BleControlService.sendData(intent,uuid);
```

The standard Android `sendBroadcast` call is commented out and replaced by a direct static method call on `BleControlService`. The commented-out line is dead code that should be removed. Its presence also documents a design change: the service now routes data through a static singleton method instead of the standard broadcast bus, which is a leaky abstraction — `BleMachineService` (a standard `Service`) should not directly call static methods on a sibling service implementation class.

---

### A13-17 — LOW: Inconsistent UUID comparison — `equalsIgnoreCase` applied redundantly

**File:** `BleMachine.java`, line 250
**Category:** Style inconsistency

```java
} else if (uuid.toLowerCase().equalsIgnoreCase(BleModel.instance().getPrimaryRelayId())) {
```

`uuid.toLowerCase()` already produces a lowercase string; calling `.equalsIgnoreCase()` on it is redundant. All other UUID comparisons in the same method use plain `.equals()`. This line should use `.equals()` after lowercasing both sides, or simply `equalsIgnoreCase()` without the prior `toLowerCase()`.

---

### A13-18 — LOW: `writeResult` intermediate variable serves no purpose

**File:** `BleMachine.java`, lines 211–212
**Category:** Style

```java
boolean writeResult = writeCharacteristic(relayTimeout);
return writeResult;
```

The variable `writeResult` is assigned and immediately returned. All peer methods return `writeCharacteristic(...)` directly. The intermediate variable is unnecessary and inconsistent.

---

### A13-19 — LOW: `mBleDeviceAddress` field written but never read in `BleMachineService`

**File:** `BleMachineService.java`, lines 47, 143, 161
**Category:** Dead code

```java
private String mBleDeviceAddress;
...
mBleDeviceAddress = address;          // connect(String), line 143
mBleDeviceAddress = device.getAddress(); // connect(BluetoothDevice), line 161
```

`mBleDeviceAddress` is written in both `connect` overloads but is never subsequently read within `BleMachineService`. The address is available from `mBluetoothGatt.getDevice().getAddress()` wherever needed (as done in the callbacks). The field is dead.

---

### A13-20 — LOW: Package name inconsistency — `WebService.BLE` mixed-case in Java source tree

**File:** All three files
**Category:** Style inconsistency

All three files are in package `au.com.collectiveintelligence.fleetiq360.WebService.BLE`. Java package naming convention (per Google Java Style and Android convention) requires all-lowercase package components (`webservice.ble`). Mixed-case components (`WebService`, `BLE`) compile correctly but violate convention, may confuse tools, and are inconsistent with other packages in the project.

---

### A13-21 — INFO: `BleModel` exposes `mapUuidForPath` with package-private visibility

**File:** `BleModel.java`, line 39
**Category:** Leaky abstraction

```java
HashMap<String,String> mapUuidForPath = new HashMap<>();
```

The internal cache `mapUuidForPath` has no access modifier (package-private). It is a mutable `HashMap` returned by reference. Any class in the same package can directly manipulate the cache, bypassing `getUUIDFromPath`'s logic. It should be `private`.

---

### A13-22 — INFO: `BleModel` public constructor alongside singleton `instance()` method

**File:** `BleModel.java`, lines 42–54
**Category:** Style inconsistency / Leaky abstraction

```java
public static BleModel instance() { ... }
public BleModel() { initUuids(); }
```

The class exposes both a public constructor and a singleton accessor. Any caller can create independent `BleModel` instances using `new BleModel()`, bypassing the singleton and creating independent UUID caches. If singleton semantics are required, the constructor should be `private`.

---

## Summary Table

| ID | Severity | File | Issue |
|---|---|---|---|
| A13-1 | CRITICAL | BleModel.java:24 | Auth token hardcoded as public plaintext constant |
| A13-2 | HIGH | BleMachine.java:243–249 | Auth response handler entirely commented out; auth failures undetected |
| A13-3 | HIGH | BleControlService.java:64–73 | Auto-reconnect listener block commented out |
| A13-4 | HIGH | BleMachineService.java:229–232 | Possible NPE — `getDescriptor()` result not null-checked |
| A13-5 | HIGH | BleMachineService.java:68–71 | `discoverServices()` return value silently dropped |
| A13-6 | HIGH | BleMachineService.java:83 | Inconsistent error handling for `discoverServices()` across two call sites |
| A13-7 | HIGH | BleMachineService.java:162 | Unreachable null check — dead code, misleading log |
| A13-8 | MEDIUM | BleMachineService.java:51–53 | `STATE_DISCONNECTED` public; siblings private — inconsistent visibility |
| A13-9 | MEDIUM | BleMachine.java:28–44 | Inverted/overloaded boolean return semantics across all state-machine methods |
| A13-10 | MEDIUM | BleMachine.java:83–107 | Missing braces makes `if` guard ineffective in both notification methods |
| A13-11 | MEDIUM | BleMachine.java:210 | Magic number `60` for relay timeout — no name, no unit |
| A13-12 | MEDIUM | BleMachine.java:182 | Magic number `80000` for default impact threshold — undocumented |
| A13-13 | MEDIUM | BleModel.java:41–50 | Singleton not thread-safe — no `volatile` / `synchronized` |
| A13-14 | MEDIUM | BleModel.java:29 | `CLIENT_CHARACTERISTIC_CONFIG` missing `final` — mutable constant |
| A13-15 | MEDIUM | BleControlService.java:20 | `IntentService` deprecated (API 30); audited files tightly coupled to it |
| A13-16 | MEDIUM | BleMachineService.java:278 | `sendBroadcast` commented out; static inter-service call is leaky abstraction |
| A13-17 | LOW | BleMachine.java:250 | Redundant `toLowerCase()` before `equalsIgnoreCase()` |
| A13-18 | LOW | BleMachine.java:211–212 | Unnecessary intermediate variable `writeResult` |
| A13-19 | LOW | BleMachineService.java:47,143,161 | `mBleDeviceAddress` field written but never read — dead field |
| A13-20 | LOW | All three files | Package names `WebService.BLE` violate all-lowercase convention |
| A13-21 | INFO | BleModel.java:39 | `mapUuidForPath` package-private — internal cache unnecessarily exposed |
| A13-22 | INFO | BleModel.java:42–54 | Public constructor coexists with singleton accessor — breaks singleton contract |
