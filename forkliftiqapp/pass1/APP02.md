# Pass 1 Security Audit — Agent APP02
**Repository:** forkliftiqapp (Android/Java)
**Date:** 2026-02-27
**Agent:** APP02
**Scope:** BLE subsystem — BleMachine.java, BleMachineService.java, BleModel.java

---

## Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy recorded:** The checklist specifies `Branch: main`. The actual current branch is `master`. Proceeding on `master` as confirmed by git output.

---

## Reading Evidence

### File 1: BleMachine.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.BLE.BleMachine`

**Public fields (line numbers):**
- `public int expectingRelayValue` — line 20
- `public BleUtil.BleTimeItem expectingTimeItem` — line 21
- `public int expectingImpactThreshold` — line 22

**Public methods (signature and line number):**
- `public BleMachine(BleController bleController)` — line 24 (constructor)

**Package-private methods (accessible within the BLE package):**
- `boolean authDevice()` — line 28
- `void onServiceFound()` — line 46
- `void onAuthDone()` — line 76
- `boolean disableShockNotification()` — line 83
- `boolean setShockNotification()` — line 96
- `boolean setRelay(final boolean enable)` — line 109
- `boolean clearRelay()` — line 133
- `void logTime(String s, BleUtil.BleTimeItem bleTimeItem)` — line 149
- `boolean setTime()` — line 155
- `boolean setImpactThreshold()` — line 174
- `boolean setRelayTimeout()` — line 198
- `private boolean setRelayTimeout(String relayTimeoutUUID)` — line 204
- `boolean writeCharacteristic(BluetoothGattCharacteristic characteristic)` — line 215
- `boolean readCharacteristic(BluetoothGattCharacteristic characteristic)` — line 222
- `void onBleDataRead(Intent intent)` — line 229
- `void onGattServices(List<BluetoothGattService> gattServices)` — line 289

**Android component type:** Plain Java class (not a Service, Activity, BroadcastReceiver, or ContentProvider).

---

### File 2: BleMachineService.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.BLE.BleMachineService`

**Public constants (line numbers):**
- `public static final int STATE_DISCONNECTED = 0` — line 51
- `public final static String ACTION_GATT_CONNECTED = "com.fleetiq.bluetooth.le.ACTION_GATT_CONNECTED"` — line 55
- `public final static String ACTION_GATT_DISCONNECTED = "com.fleetiq.bluetooth.le.ACTION_GATT_DISCONNECTED"` — line 56
- `public final static String ACTION_GATT_SERVICES_DISCOVERED = "com.fleetiq.bluetooth.le.ACTION_GATT_SERVICES_DISCOVERED"` — line 57
- `public final static String ACTION_DATA_AVAILABLE = "com.fleetiq.bluetooth.le.ACTION_DATA_AVAILABLE"` — line 58
- `public final static String ACTION_DATA_WRITE = "com.fleetiq.bluetooth.le.ACTION_DATA_WRITE"` — line 59
- `public final static String ACTION_DATA_CHANGED = "com.fleetiq.bluetooth.le.ACTION_DATA_CHANGED"` — line 60
- `public final static String CHARA_UUID = "com.fleetiq.bluetooth.le.CHARA_UUID"` — line 61
- `public final static String EXTRA_DATA = "com.fleetiq.bluetooth.le.EXTRA_DATA"` — line 62
- `public final static String DEVICE_ADDRESS = "com.fleetiq.bluetooth.le.DEVICE_ADDRESS"` — line 63
- `public final static String STATUS_CODE = "com.fleetiq.bluetooth.le.STATUS_CODE"` — line 64

**Private fields:**
- `private BluetoothManager mBluetoothManager` — line 45
- `private BluetoothAdapter mBluetoothAdapter` — line 46
- `private String mBleDeviceAddress` — line 47
- `private BluetoothGatt mBluetoothGatt` — line 48
- `private int mConnectionState = STATE_DISCONNECTED` — line 49

**Public methods (signature and line number):**
- `public void discoverServices()` — line 67
- `public boolean connect(final String address)` — line 137
- `public boolean connect(final BluetoothDevice device)` — line 155
- `public void disconnect()` — line 179
- `public void close()` — line 187
- `public boolean readCharacteristic(BluetoothGattCharacteristic characteristic)` — line 195
- `public boolean writeCharacteristic(BluetoothGattCharacteristic characteristic)` — line 206
- `public boolean setCharacteristicNotification(BluetoothGattCharacteristic characteristic, boolean enabled)` — line 216
- `public List<BluetoothGattService> getSupportedGattServices()` — line 237
- `public IBinder onBind(Intent intent)` — line 250 (Service override)
- `public boolean onUnbind(Intent intent)` — line 255 (Service override)
- `public boolean initialize()` — line 282

**Inner classes:**
- `public class LocalBinder extends Binder` — line 243; inner method `BleMachineService getService()` (package-private) — line 244

**Android component type:** `android.app.Service` (bound service providing GATT communication to BLE forklift hardware).

---

### File 3: BleModel.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.BLE.BleModel`

**Public constants (line numbers):**
- `public final static String UUID_BLE_TIME = "00002a2b-0000-1000-8000-00805f9b34fb"` — line 13
- `public final static String UUID_BLE_DEVICE_NAME = "00002a00-0000-1000-8000-00805f9b34fb"` — line 14
- `public final static String UUID_BLE_MANUFACTURE = "00002a29-0000-1000-8000-00805f9b34fb"` — line 15
- `public final static String UUID_BLE_MODEL = "00002a24-0000-1000-8000-00805f9b34fb"` — line 16
- `public final static String UUID_SHOCK_COUNT = "69dfccac-59b7-ef3e-5309-db222d1c2d09"` — line 17
- `public final static String UUID_SHOCK_EVENT_ITEM = "53535322-e7fc-8229-b470-89d9fda99e46"` — line 18
- `public final static String UUID_POP_SHOCK_EVENT = "1642fcc6-bcc9-63f5-039a-721e9acbfb93"` — line 19
- `public final static String UUID_SHOCK_THRESHOLD = "6d3f3a08-06dd-4c11-6add-00c0c2443c77"` — line 20
- `public final static String UUID_RELAY_0 = "3cfd3551-3e85-7cfa-7425-9b54c464c6b1"` — line 21
- `public final static String UUID_RELAY_1 = "1ffbb954-2443-c7c4-f98d-78e9abdd54de"` — line 22
- `public final static String UUID_TOKEN_AUTH = "6d1e95a3-12bf-1107-705e-16edf5954aba"` — line 23
- `public final static String TOKEN_AUTH = "uS8MgpklMx"` — line 24
- `public final static String UUID_RELAY_0_TIMEOUT = "e4d93331-cd59-9f70-4490-7f3adda0784d"` — line 26
- `public final static String UUID_RELAY_1_TIMEOUT = "465330b5-8bc7-ed83-d3c5-a6601946b503"` — line 27
- `public static String CLIENT_CHARACTERISTIC_CONFIG = "00002902-0000-1000-8000-00805f9b34fb"` — line 29

**Package-private constants:**
- `final static String basePath = "au.com.collectiveintelligence.characteristic."` — line 32
- `final static String PATH_VERSION_MAIN = "system.version_main"` — line 33
- `final static String PATH_VERSION_RADIO = "system.version_radio"` — line 34
- `final static String PATH_SHOCK_EVENT_THRESHOLD = "shock_detection.shock_magnitude_threshold"` — line 35
- `final static String PATH_SHOCK_EVENT_POP = "shock_detection.pop_shock_event"` — line 36
- `final static String PATH_SHOCK_EVENT = "shock_detection.shock_event"` — line 37
- `final static String PATH_SHOCK_EVENT_COUNT = "shock_detection.shock_event_count"` — line 38

**Instance fields:**
- `HashMap<String,String> mapUuidForPath` — line 39 (package-private)
- `private static BleModel ourInstance` — line 41

**Public methods (signature and line number):**
- `public static BleModel instance()` — line 42 (singleton accessor)
- `public BleModel()` — line 52 (public constructor — see Finding 5b)
- `public String getPrimaryRelayId()` — line 56
- `public String getRelayId(int index)` — line 60
- `public String getPathExternalRelayKey(int index)` — line 85
- `public String getUUIDFromPath(String path)` — line 89

**Android component type:** Plain Java class (singleton model, not an Android component).

---

## Checklist Section Findings

### 1. Signing and Keystores

These three files contain no keystore references, no `build.gradle` content, no `signingConfigs`, and no `storePassword`, `keyPassword`, or `keyAlias` values. Signing configuration is outside the scope of the assigned files.

**No issues found — Section 1.**

---

### 2. Network Security

These files implement Bluetooth Low Energy (BLE/GATT) communication exclusively. No HTTP clients, OkHttp, Retrofit, `HttpURLConnection`, TLS/SSL configuration, server URLs, or IP addresses are present in any of the three files.

**No issues found — Section 2.**

---

### 3. Data Storage

No `SharedPreferences`, `EncryptedSharedPreferences`, SQLite, file I/O, `getExternalStorageDirectory()`, `openFileOutput()`, or external storage operations are present in any of these three files.

**No issues found — Section 3.**

---

### 4. Input and Intent Handling

**FINDING 4a — Implicit broadcast action strings use unowned namespace; commented-out `sendBroadcast` is a latent risk**
Severity: Low-Medium
File: `BleMachineService.java`, lines 55–64, 278–279

The intent action string constants all use the namespace `com.fleetiq.bluetooth.le`, which is not the app's own declared package (`au.com.collectiveintelligence.fleetiq360`):

```java
// BleMachineService.java lines 55–64
public final static String ACTION_GATT_CONNECTED    = "com.fleetiq.bluetooth.le.ACTION_GATT_CONNECTED";
public final static String ACTION_GATT_DISCONNECTED = "com.fleetiq.bluetooth.le.ACTION_GATT_DISCONNECTED";
public final static String ACTION_GATT_SERVICES_DISCOVERED = "com.fleetiq.bluetooth.le.ACTION_GATT_SERVICES_DISCOVERED";
public final static String ACTION_DATA_AVAILABLE    = "com.fleetiq.bluetooth.le.ACTION_DATA_AVAILABLE";
public final static String ACTION_DATA_WRITE        = "com.fleetiq.bluetooth.le.ACTION_DATA_WRITE";
public final static String ACTION_DATA_CHANGED      = "com.fleetiq.bluetooth.le.ACTION_DATA_CHANGED";
```

The current routing bypasses the system broadcast bus via `BleControlService.sendData(intent, uuid)` (line 279). However, line 278 contains a commented-out `sendBroadcast(intent)`:

```java
// BleMachineService.java lines 278–279
//sendBroadcast(intent);
BleControlService.sendData(intent,uuid);
```

If `sendBroadcast` were re-enabled — by any future developer unfamiliar with the reason it was commented out — any app that registered for these unowned action strings could receive BLE characteristic data including relay state and impact threshold values. The commented line is a latent risk that should be removed rather than left as dead code.

**FINDING 4b — No null/bounds check on `EXTRA_DATA` byte array in `onBleDataRead()`**
Severity: Low
File: `BleMachine.java`, lines 239, 254, 279

`BleMachine.onBleDataRead(Intent intent)` reads a byte array from the intent and passes it to `BleUtil.getIntValue()` without checking for null or minimum length:

```java
// BleMachine.java lines 239, 254, 279
byte[] data = intent.getByteArrayExtra(BleMachineService.EXTRA_DATA);
// ...
int value = BleUtil.getIntValue(data, BluetoothGattCharacteristic.FORMAT_UINT8);
// ...
int value = BleUtil.getIntValue(data, BluetoothGattCharacteristic.FORMAT_UINT32, 0);
```

If `data` is `null` or shorter than the format requires, the result is a `NullPointerException` or `ArrayIndexOutOfBoundsException`. A malformed BLE response could cause the BLE state machine to crash.

**No issues found in Section 4 for:** exported components, WebView, or deep-link intent filters — none are present in the three assigned files.

---

### 5. Authentication and Session

**FINDING 5a — Hardcoded BLE authentication token compiled into APK**
Severity: Critical
File: `BleModel.java`, line 24; used at `BleMachine.java`, line 40

`BleModel.java` declares a `public static final` authentication token:

```java
// BleModel.java line 24
public final static String TOKEN_AUTH = "uS8MgpklMx";
```

This constant is written directly to the BLE authentication characteristic in `BleMachine.authDevice()`:

```java
// BleMachine.java line 40
characteristic.setValue(BleModel.TOKEN_AUTH);
```

Consequences:

1. The token is compiled into every APK release. Decompilation with `jadx` or `apktool` immediately recovers it in plaintext.
2. The token cannot be rotated without a full app update and a coordinated firmware update across all deployed BLE devices.
3. The token is the sole authentication mechanism between the app and BLE-connected forklift hardware. Any attacker within Bluetooth range who possesses the extracted token can authenticate to any device accepting it.
4. Physical safety impact: relay control (`setRelay`, `clearRelay` in `BleMachine.java` lines 109 and 133) directly maps to enabling or disabling forklift ignition. Unauthorized relay control is a physical safety risk.

This token must be treated as permanently compromised and rotated in BLE firmware and all released APK versions.

**FINDING 5b — Public constructor bypasses singleton pattern**
Severity: Low
File: `BleModel.java`, lines 42–54

`BleModel` implements a singleton via `instance()` but the constructor is declared `public`, allowing callers to create independent instances:

```java
// BleModel.java lines 42–54
public static BleModel instance() {
    if (ourInstance == null) {
        ourInstance = new BleModel();
    }
    return ourInstance;
}

public BleModel() {   // should be private
    initUuids();
}
```

A second instance created via `new BleModel()` has a separate `mapUuidForPath` cache. While `getPrimaryRelayId()` returns a constant, UUID-from-path caching could diverge between instances. The constructor should be `private`.

**FINDING 5c — Non-thread-safe singleton**
Severity: Low
File: `BleModel.java`, lines 42–49

The `instance()` singleton check is not synchronized:

```java
// BleModel.java lines 42–49
public static BleModel instance() {
    if (ourInstance == null) {
        ourInstance = new BleModel();
    }
    return ourInstance;
}
```

BLE callbacks in Android arrive on system threads separate from the UI thread. Two threads could concurrently observe `ourInstance == null` and both construct a `BleModel`, resulting in a data race. The standard remediation is `volatile` on `ourInstance` combined with double-checked locking, or initialization-on-demand holder idiom.

**No issues found in Section 5 for:** token expiry handling, logout clearing, or multi-operator session management — these concerns are outside the scope of the three BLE subsystem files reviewed.

---

### 6. Third-Party Libraries

No third-party library dependencies are imported or referenced in any of the three assigned files. All imports are `android.*`, `java.*`, and the app's own packages.

**No issues found — Section 6.**

---

### 7. Google Play and Android Platform

**FINDING 7a — `BluetoothGattDescriptor.setValue()` deprecated in API 33**
Severity: Low
File: `BleMachineService.java`, line 231

`setCharacteristicNotification()` calls the deprecated `BluetoothGattDescriptor.setValue(byte[])`:

```java
// BleMachineService.java line 231
descriptor.setValue(BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE);
return mBluetoothGatt.writeDescriptor(descriptor);
```

`BluetoothGattDescriptor.setValue()` was deprecated in Android API 33 (Android 13). The replacement is to pass the value directly to `BluetoothGatt.writeDescriptor(BluetoothGattDescriptor, byte[])`. Depending on the `targetSdkVersion` declared in `build.gradle` (outside this agent's scope), this may trigger lint warnings or behave differently on Android 13+ devices.

**FINDING 7b — No null check on `characteristic.getDescriptor()` return value**
Severity: Low
File: `BleMachineService.java`, lines 229–232

Immediately after retrieving the descriptor, the code calls methods on it without a null check:

```java
// BleMachineService.java lines 229–232
BluetoothGattDescriptor descriptor = characteristic.getDescriptor(
        UUID.fromString(BleModel.CLIENT_CHARACTERISTIC_CONFIG));
descriptor.setValue(BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE);
return mBluetoothGatt.writeDescriptor(descriptor);
```

`characteristic.getDescriptor()` returns `null` if the descriptor UUID is not present on the remote GATT server. A null `descriptor` causes a `NullPointerException` at line 231, crashing the BLE service. A malformed or unexpected BLE peripheral can trigger this crash path.

**FINDING 7c — Unreachable null check (dead code) in `connect(BluetoothDevice)`**
Severity: Informational
File: `BleMachineService.java`, lines 155–169

In the `connect(final BluetoothDevice device)` overload, a second null check on `device` at line 162 is unreachable because `device.getAddress()` is called on line 161 — if `device` were null, the NPE would already have occurred:

```java
// BleMachineService.java lines 155–169
public boolean connect(final BluetoothDevice device) {
    if (mBluetoothAdapter == null || device == null) {  // line 156
        return false;
    }
    mBleDeviceAddress = device.getAddress();             // line 161
    if (device == null) {                                // line 162 — unreachable
        Log.w(TAG, "Device not found.  Unable to connect.");
        return false;
    }
    startConnect(device);
    return true;
}
```

This is dead code that indicates reduced review rigor for this class. It is not a security finding in isolation but contributes to maintenance risk.

**No issues found in Section 7 for:** permissions, `targetSdkVersion`/`minSdkVersion`, runtime permission handling, ProGuard/R8 — these are in `AndroidManifest.xml` and `build.gradle`, which are outside the scope of the three assigned files.

---

## Summary of Findings

| # | Severity | File | Line(s) | Finding |
|---|----------|------|---------|---------|
| 1 | Critical | BleModel.java | 24 | Hardcoded BLE auth token `TOKEN_AUTH = "uS8MgpklMx"` is `public static final`, compiled into APK; allows APK decompiler to extract it and authenticate to forklift BLE hardware; relay control maps to physical forklift ignition |
| 2 | Low-Medium | BleMachineService.java | 55–64, 278–279 | Intent action strings use unowned namespace `com.fleetiq.bluetooth.le`; commented-out `sendBroadcast` at line 278 is a latent interception risk if re-enabled |
| 3 | Low | BleMachine.java | 239, 254, 279 | No null/bounds check on `EXTRA_DATA` byte array before passing to `BleUtil.getIntValue()`; malformed BLE response can cause NPE or AIOOBE |
| 4 | Low | BleModel.java | 52 | `public` constructor alongside singleton pattern allows bypass of `instance()` and creation of independent divergent instances |
| 5 | Low | BleModel.java | 42–49 | Non-thread-safe singleton; concurrent BLE and UI threads can both observe `ourInstance == null` and construct two instances (data race) |
| 6 | Low | BleMachineService.java | 231 | `BluetoothGattDescriptor.setValue()` deprecated in API 33; replacement is `BluetoothGatt.writeDescriptor(descriptor, value)` |
| 7 | Low | BleMachineService.java | 229–232 | No null check on `characteristic.getDescriptor()` return; null descriptor causes NPE and BLE service crash on malformed peripheral |
| 8 | Info | BleMachineService.java | 162 | Unreachable null check on `device` after `device.getAddress()` already invoked at line 161 — dead code |

---

## Notes for Subsequent Passes

- Finding 1 (hardcoded `TOKEN_AUTH`) is the highest-priority finding in this file set. The token is permanently compromised as a compile-time constant in any distributed APK. Remediation requires coordinating a firmware-side token rotation with an app update. A Pass 2 reviewer should confirm whether the same token appears in any other class, server-side configuration, or BLE firmware source in scope.
- Finding 2 (commented-out `sendBroadcast`) should be confirmed as intentionally disabled. The commented line should be removed from source control to prevent accidental re-introduction.
- Findings 6 and 7 should be cross-referenced with `targetSdkVersion` in `build.gradle` to determine API 33 compliance urgency and whether shock notification is functioning correctly on Android 13+ devices.
