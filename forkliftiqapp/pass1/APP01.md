# Pass 1 Security Audit — APP01
**Agent ID:** APP01
**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Branch verified:** master

**Branch discrepancy:** Checklist states `Branch: main`; actual branch is `master`. Audit proceeds on `master`.

---

## Files Audited

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/BLE/BleControlService.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/BLE/BleController.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/BLE/BleDataService.java`

---

## Reading Evidence

### File 1: BleControlService.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.BLE.BleControlService`

**Extends:** `android.app.IntentService`

**Public fields / constants:**
| Name | Type | Line |
|---|---|---|
| `ACTION_AUTO_RECONNECT` | `public static String` | 22 |
| `ACTION_INIT_DEVICE` | `public static String` | 23 |
| `TAG` | `public static String` | 30 |
| `mBleMachine` (package-private static) | `static BleMachine` | 31 |

Note: `ACTION_AUTH_DEVICE`, `ACTION_SET_RELAY`, `ACTION_SET_TIME`, `ACTION_SET_IMPACT_THRESHOLD`, `ACTION_SET_RELAY_TIMEOUT`, `ACTION_ENABLE_SHOCK_NOTIFICATION` are `private static String` (lines 24–29).

**Public methods (signature : line):**
| Signature | Line |
|---|---|
| `public BleControlService()` | 33 |
| `public void processBleEvents(Intent intent)` | 38 |
| `public static void authDevice()` | 183 |
| `public static void sendData(Intent intent, String uuid)` | 187 |
| `public static void sendAction(String action)` | 210 |
| `public static void setRelayWithDelay()` | 215 |
| `public static void setRelayNoDelay()` | 224 |
| `public static void setTime()` | 228 |
| `public static void initDevice()` | 232 |
| `public static void setImpactThreshold()` | 237 |
| `public static void setRelayTimeout()` | 241 |
| `public static void setShockNotification()` | 245 |
| `public static void afterWriteAttribute(boolean r, final BluetoothGattCharacteristic characteristic, Runnable failedRunnable)` | 249 |

**Protected methods:**
| Signature | Line |
|---|---|
| `protected void onHandleIntent(Intent intent)` | 176 |

**Package-private methods:**
| Signature | Line |
|---|---|
| `boolean handleBleOperation(Intent intent)` | 102 |

**Android component type:** `IntentService` subclass (service).

---

### File 2: BleController.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.BLE.BleController`

**Extends:** `java.lang.Object` (no Android component base class — this is a plain singleton controller)

**Public fields / constants:**
| Name | Type | Line |
|---|---|---|
| `EQUIPMENT_CONNECT_CODE_BLE_NOT_ON` | `public final static int` | 49 |
| `EQUIPMENT_CONNECT_CODE_BLE_FAILED` | `public final static int` | 50 |
| `EQUIPMENT_CONNECT_CODE_BUSY` | `public final static int` | 51 |
| `EQUIPMENT_CONNECT_CODE_INVALID_DATA` | `public final static int` | 52 |
| `STATUS_NONE` | `public static int` | 55 |
| `STATUS_IDLE` | `public final static int` | 56 |
| `STATUS_CONNECTING` | `public final static int` | 57 |
| `STATUS_SERVICE_FOUND` | `public final static int` | 58 |
| `STATUS_AUTHENTICATED` | `public final static int` | 59 |
| `STATUS_SETUP_RELAY_DONE` | `public final static int` | 60 |
| `STATUS_SETUP_DONE` | `public final static int` | 61 |
| `ble_status` | `public int` | 62 |
| `SCAN_PERIOD` | `public static final int` | 68 |
| `CONNECT_PERIOD` | `public static final int` | 69 |
| `SCAN_TIMEOUT` | `public static final int` | 70 |
| `mBluetoothAdapter` | `public BluetoothAdapter` | 71 |
| `bleScanner` | `public BluetoothLeScanner` | 72 |
| `scanCallback` | `public Object` | 73 |
| `equipmentListener` | `public EquipmentListener` | 74 |
| `mScanning` | `public boolean` | 75 |
| `mBleService` | `public BleMachineService` | 76 |
| `mContext` | `public Context` | 78 |
| `mEquipmentItem` | `public EquipmentItem` | 79 |
| `mBleDeviceAddress` | `public String` | 80 |
| `mGattCharacteristics` | `public ArrayList<BluetoothGattCharacteristic>` | 82 |
| `bleTimeSynced` | `public boolean` | 83 |
| `bleThresholdSynced` | `public boolean` | 84 |
| `cachedBleDevices` | `public static ArrayList<BluetoothDevice>` | 117 |
| `myHandler` | `public Handler` | 732 |

**Public methods (signature : line):**
| Signature | Line |
|---|---|
| `public BleController()` | 779 |
| `public static synchronized BleController instance()` | 770 |
| `public boolean isDeviceSetupDone(String address)` | 138 |
| `public boolean isDeviceDisconnected(String address)` | 146 |
| `public void autoReconnect()` | 227 |
| `public void startScan()` | 377 |
| `public void stopScan()` | 402 |
| `public void startConnect(boolean relaySet, boolean autoReconnect, EquipmentItem equipmentItem, EquipmentListener listener)` | 615 |
| `public void preStartCheck(boolean relaySet, final boolean autoReconnect, final EquipmentItem equipmentItem, final EquipmentListener listener)` | 530 |
| `public void stopConnection()` | 275 |
| `public void onBleServiceDisconnected()` | 187 |
| `public List<BluetoothGattService> getSupportedGattServices()` | 209 |
| `public void discoverServices()` | 217 |
| `public void startTimer()` | 744 |
| `public void init(Context context)` | 764 |

**Inner class:** `public static class EquipmentListener` (lines 659–668) with public methods `onSucceed()` (line 661) and `onFailed(int errorCode)` (line 665).

**Android component type:** Not an Android component directly; instantiated as a singleton, used by services.

---

### File 3: BleDataService.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.BLE.BleDataService`

**Extends:** `android.app.IntentService`

**Public fields / constants:**
| Name | Type | Line |
|---|---|---|
| `ACTION_READ_SHOCK_COUNT` | `public static String` | 18 |
| `TAG` | `public static String` | 19 |

**Package-private static fields:**
| Name | Type | Line |
|---|---|---|
| `mBleMachine` | `static BleMachine` | 20 |
| `mBleController` | `static BleController` | 21 |

**Public methods (signature : line):**
| Signature | Line |
|---|---|
| `public BleDataService()` | 23 |
| `public void processBleEvents(Intent intent)` | 27 |
| `public boolean readShockEvent()` | 78 |
| `public static void sendAction(String action)` | 69 |
| `public static void sendData(Intent intent)` | 206 |

**Protected methods:**
| Signature | Line |
|---|---|
| `protected void onHandleIntent(Intent intent)` | 58 |

**Android component type:** `IntentService` subclass (service).

---

## Security Review Findings

### Section 1 — Signing and Keystores

Not applicable to these files. No keystore files, `build.gradle`, `gradle.properties`, `bitbucket-pipelines.yml`, or signing configuration appear in the three assigned files.

No issues found — Section 1 (out of scope for assigned files).

---

### Section 2 — Network Security

Not applicable to these files. No HTTP client instantiation, no URL construction, no network security config references, and no hardcoded API endpoints appear in the three assigned files. These files deal exclusively with Bluetooth Low Energy (BLE) communication.

No issues found — Section 2 (out of scope for assigned files).

---

### Section 3 — Data Storage

**FINDING — DS-01 — Informational / Low**
**File:** `BleController.java`, line 80
**Description:** `mBleDeviceAddress` is a `public String` field on the singleton. While a MAC address is not a credential, it is persistent device-identifying data (PII under some regulatory frameworks). The field is never cleared until `clearConnection()` is called (line 290), which may or may not be invoked on logout. No finding is raised purely from this file, but it should be cross-referenced against session/logout handling audited in other files.

**FINDING — DS-02 — Informational**
**File:** `BleController.java`, line 79
**Description:** `mEquipmentItem` is a `public EquipmentItem` field on the singleton. The contents of `EquipmentItem` are not visible in this file, but it likely contains forklift assignment data (equipment ID, MAC address, operator assignment). It is held in a public field of a static singleton, meaning it persists for the application lifetime. It is cleared in `clearConnection()` (line 293). Cross-reference with logout/shift-change handling is required to confirm it is cleared on operator logout.

No issues found beyond the above informational items — Section 3.

---

### Section 4 — Input and Intent Handling

**FINDING — IH-01 — Medium**
**File:** `BleControlService.java`, lines 187–198 (`sendData` method) and lines 210–213 (`sendAction` method)
**Description:** The `sendAction(String action)` method (line 210) takes a caller-supplied action string and directly constructs an explicit `Intent` targeting `BleControlService`, then calls `startService()`. No validation of the `action` parameter is performed before use. While the callers within the codebase pass only internal constant strings, if this method were called with attacker-controlled input (e.g., via an exported component in another file that accepts untrusted Intents and forwards them), arbitrary service actions could be triggered — including `ACTION_AUTH_DEVICE`, `ACTION_SET_RELAY`, and `ACTION_INIT_DEVICE`. The risk depends on whether any exported component passes untrusted data to this method. Flag for cross-file review.

**FINDING — IH-02 — Low**
**File:** `BleControlService.java`, line 102–173 (`handleBleOperation`)
**Description:** The `ACTION_AUTH_DEVICE` path (line 110–124) calls `mBleMachine.authDevice()` twice on failure (lines 111, 113) without any input validation of the intent payload. The retry is unconditional — if `authDevice()` fails, it is called a second time immediately, which could represent a BLE authentication replay or race condition. This is a logic concern rather than a direct injection risk, but the absence of rate-limiting or intent payload validation is noted.

**FINDING — IH-03 — Low**
**File:** `BleController.java`, lines 530–557 (`preStartCheck`)
**Description:** When `equipmentItem` is `null`, the code at line 541 attempts `listener.onFailed(EQUIPMENT_CONNECT_CODE_INVALID_DATA)` and then proceeds to log `equipmentItem.mac_address` at line 545 — this is a null dereference that would throw a `NullPointerException` before the return statement at line 547 is reached. This is a logic bug rather than a pure security issue, but NPEs can be used to crash services. The guard at line 541 checks for null but then dereferences the null object on line 545 before returning.

```java
// Line 541-547 — null check followed by null dereference:
if(equipmentItem == null) {
    if(listener != null) {
        listener.onFailed(EQUIPMENT_CONNECT_CODE_INVALID_DATA);
    }
    Log.d(TAG,"start connect invalid data return device " + equipmentItem.mac_address); // NPE here
    return;
}
```

**FINDING — IH-04 — Informational**
**File:** `BleDataService.java`, lines 69–75 (`sendAction`) and lines 206–210 (`sendData`)
**Description:** Same pattern as IH-01 — `sendAction` in `BleDataService` also constructs explicit Intents with caller-supplied action strings without validation. Same cross-file review recommendation applies.

No further issues found — Section 4.

---

### Section 5 — Authentication and Session

**FINDING — AS-01 — Low**
**File:** `BleControlService.java`, lines 110–123 (`handleBleOperation`, AUTH_DEVICE branch)
**Description:** BLE device authentication (`mBleMachine.authDevice()`) is invoked unconditionally when `ACTION_AUTH_DEVICE` is received. There is no rate limiting, no session check, and no check that the caller is authorised to trigger re-authentication. Any code path that can enqueue an `ACTION_AUTH_DEVICE` intent to `BleControlService` will cause a BLE auth operation to execute. If the BLE auth carries any credential (PIN, key), repeated invocation could facilitate brute force. Depends on `BleMachine.authDevice()` implementation (not in scope for this pass).

**FINDING — AS-02 — Low**
**File:** `BleController.java`, line 62 and lines 289–296 (`clearConnection`)
**Description:** `ble_status` is a `public int` field (line 62), not a private field with accessor controls. Direct external mutation of this status field could allow the caller to bypass state machine guards (e.g., setting `ble_status = STATUS_SETUP_DONE` while not actually authenticated). All three files treat `ble_status` checks as security gates for relay control and shock data access. Public mutability of this field undermines those gates.

**FINDING — AS-03 — Informational**
**File:** `BleController.java`, lines 683–695 (`onSetupDone`) and lines 289–296 (`clearConnection`)
**Description:** `equipmentListener` is a `public EquipmentListener` field (line 74). It is nulled in `onSetupDone` and `onFailed` after callbacks, which is correct. However, it is also a `public` field, meaning any component can replace or null it, potentially suppressing failure callbacks. Low-severity design concern.

No further issues found — Section 5.

---

### Section 6 — Third-Party Libraries

Not applicable to these files. No dependency declarations appear in Java source files. Library audit requires `build.gradle`.

No issues found — Section 6 (out of scope for assigned files).

---

### Section 7 — Google Play and Android Platform

**FINDING — GP-01 — Medium**
**File:** `BleControlService.java` (line 3) and `BleDataService.java` (line 3)
**Description:** Both services extend `android.app.IntentService`. `IntentService` was deprecated in Android API level 30 (Android 11). Google Play requires `targetSdkVersion` 34+ for app updates. At `targetSdkVersion` 34, using a deprecated `IntentService` is not blocked but represents technical debt and may generate Lint warnings in the build pipeline. The recommended replacement is `WorkManager` or a `JobIntentService` for background work. This should be cross-referenced with the `targetSdkVersion` declared in `build.gradle`.

**FINDING — GP-02 — Medium**
**File:** `BleController.java`, lines 379, 403, 561 (three distinct `AsyncTask.execute()` / `new AsyncTask()` usages)
**Description:** `android.os.AsyncTask` is imported (line 17) and used in three locations:
- Line 379: `AsyncTask.execute(new Runnable() {...})` inside `startScan()`
- Line 403: `AsyncTask.execute(new Runnable() {...})` inside `stopScan()`
- Line 561: `new AsyncTask(){...}.execute()` inside `preStartCheck()`

`AsyncTask` was deprecated in Android API level 30. Continued use at `targetSdkVersion` 34+ will generate deprecation warnings and may cause issues. The recommended replacement is `java.util.concurrent.Executor` or Kotlin coroutines.

**FINDING — GP-03 — Low**
**File:** `BleController.java`, lines 485–486 (`scanDeviceFunc`)
**Description:** `mBluetoothAdapter.startLeScan(mLeScanCallback)` (line 486) is called in the `else` branch for API levels below `LOLLIPOP` (API 21). `BluetoothAdapter.startLeScan(LeScanCallback)` was deprecated in API 21. Since `minSdkVersion` is unknown from these files alone, it should be confirmed whether pre-Lollipop support is still required. If `minSdkVersion >= 21`, this branch is dead code and can be removed.

**FINDING — GP-04 — Informational**
**File:** `BleController.java`, lines 386–387 and 442–443
**Description:** A null-check ordering bug exists in two separate scan callbacks:
```java
if((mBluetoothAdapter.getState() != BluetoothAdapter.STATE_ON) &&
        (mBluetoothAdapter != null)){
```
The null check on `mBluetoothAdapter` (right side of `&&`) comes *after* the dereference of `mBluetoothAdapter.getState()`. If `mBluetoothAdapter` is null, a `NullPointerException` will be thrown before the null check is evaluated. This is a logic/reliability bug that could cause the scan to crash without graceful handling.

No further issues found — Section 7.

---

## Summary of Findings

| ID | Severity | File | Line(s) | Title |
|---|---|---|---|---|
| IH-01 | Medium | BleControlService.java | 210–213 | Unvalidated action string passed to startService |
| IH-02 | Low | BleControlService.java | 110–124 | Unconditional double-invocation of authDevice on failure |
| IH-03 | Low | BleController.java | 541–547 | Null dereference after null guard in preStartCheck |
| IH-04 | Informational | BleDataService.java | 69–75, 206–210 | Unvalidated action string in sendAction / sendData |
| DS-01 | Informational | BleController.java | 80 | MAC address in public singleton field; verify cleared on logout |
| DS-02 | Informational | BleController.java | 79 | EquipmentItem in public singleton field; verify cleared on logout |
| AS-01 | Low | BleControlService.java | 110–123 | No rate limiting on BLE auth trigger |
| AS-02 | Low | BleController.java | 62 | ble_status is public-mutable; used as security gate |
| AS-03 | Informational | BleController.java | 74 | equipmentListener is public field |
| GP-01 | Medium | BleControlService.java, BleDataService.java | 3 | IntentService deprecated at API 30 |
| GP-02 | Medium | BleController.java | 379, 403, 561 | AsyncTask deprecated at API 30 |
| GP-03 | Low | BleController.java | 485–486 | Deprecated pre-Lollipop LeScan API may be dead code |
| GP-04 | Informational | BleController.java | 386–387, 442–443 | Null check after dereference in scan callbacks |

**Branch discrepancy recorded:** Checklist specifies `Branch: main`; actual branch is `master`. Audit completed on `master`.
