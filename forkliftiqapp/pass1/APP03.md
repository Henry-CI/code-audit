# Pass 1 Security Audit — APP03
**Agent:** APP03
**Date:** 2026-02-27
**Repo:** forkliftiqapp
**Stack:** Android/Java

---

## Step 1 — Branch Verification

Command run: `git -C /c/Projects/cig-audit/repos/forkliftiqapp branch --show-current`
Result: `master`

**Discrepancy:** The checklist states `Branch: main`. The actual current branch is `master`. Audit proceeds on `master`.

---

## Step 2 — Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/BLE/BleUtil.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/BLE/ShockEventService.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/BLE/ShockEventsDb.java`

Supporting files read for context:
- `app/src/main/java/au/com/collectiveintelligence/fleetiq360/ui/application/MyApplication.java` (Realm initialisation)
- `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/SafeRealm.java` (Realm wrapper)
- `app/build.gradle` (dependencies, signing config, build config fields)

---

## Step 3 — Reading Evidence

### File 1: BleUtil.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.BLE.BleUtil`

**Public methods (signature and line number):**
- `BleUtil()` — constructor, line 24
- `public static BleTimeItem parseBleTime(byte[] data)` — line 43
- `public static boolean isTimeSetSucceed(BleTimeItem bleTimeItem, BleTimeItem expectItem)` — line 63
- `public static byte[] getTimeData()` — line 91
- `public static boolean isTheSameByteArray(byte[] a1, byte[] a2)` — line 127
- `public static String bytesToHexStr(byte[] bytes)` — line 151
- `static public int unsignedByteToInt(byte b)` — line 164
- `static public int unsignedBytesToInt(byte b0, byte b1)` — line 171
- `static public int unsignedBytesToInt(byte b0, byte b1, byte b2, byte b3)` — line 178
- `static public float bytesToFloat(byte b0, byte b1)` — line 186
- `static public float bytesToFloat(byte b0, byte b1, byte b2, byte b3)` — line 196
- `static public int unsignedToSigned(int unsigned, int size)` — line 207
- `static public int intToSignedBits(int i, int size)` — line 217
- `static public Integer getIntValue(byte[] data, int formatType)` — line 231
- `static public Integer getIntValue(byte[] data, int formatType, int offset)` — line 234

**Public fields/constants (package-private static):**
- `static byte UPDATE_REASON_UNKNOWN = 0` — line 26
- `static byte UPDATE_REASON_MANUAL = 1` — line 27
- `static byte UPDATE_REASON_EXTERNAL_REF = (1 << 1)` — line 28
- `static byte UPDATE_REASON_TIME_ZONE_CHANGE = (1 << 2)` — line 29
- `static byte UPDATE_REASON_DAYLIGHT_SAVING = (1 << 3)` — line 30

**Inner classes:** `public static class BleTimeItem` — line 33 (fields: `int year`, `int month`, `int day`, `int hour`, `int minute`, `int second`, `int dayOfWeek`)

**Android component type:** None — pure utility class.

---

### File 2: ShockEventService.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.BLE.ShockEventService`

**Extends:** `android.app.IntentService`

**Public methods (signature and line number):**
- `ShockEventService()` — constructor, line 28
- `protected void onHandleIntent(Intent intent)` — line 33 (override)
- `public static void startService()` — line 102

**Package-private methods:**
- `static void sendData(Intent intent)` — line 109

**Public static fields:**
- `public static String TAG = "CI_BLE_SHOCK_EVENT" + ShockEventService.class.getSimpleName()` — line 26
- `public static final String IMPACT = "com.ShockEventService.IMPACT"` — line 144
- `public static ShockEventsItem lastImpactEvent = null` — line 145

**Android component type:** Service (`IntentService` subclass).

---

### File 3: ShockEventsDb.java

**Fully qualified class name:** `au.com.collectiveintelligence.fleetiq360.WebService.BLE.ShockEventsDb`

**Extends:** `io.realm.RealmObject`

**Public fields:**
- `public String mac_address` — line 15
- `public Date time` — line 16
- `public long magnitude` — line 17

**Package-private static methods (signature and line number):**
- `static RealmResults<ShockEventsDb> readData(Realm realm)` — line 19
- `static void removeData(Realm realm, SaveShockEventParameter parameter)` — line 23
- `static boolean alreadySaved(final ShockEventsItem result)` — line 36
- `static void saveData(final ShockEventsItem result)` — line 46

**Android component type:** None — Realm model/DAO class.

---

### Supporting evidence: Realm initialisation (MyApplication.java lines 65-73)

```java
private void initDataBase() {
    Realm.init(context);
    RealmConfiguration config = new RealmConfiguration.Builder()
            .schemaVersion(4)
            .deleteRealmIfMigrationNeeded()
            .build();
    Realm.setDefaultConfiguration(config);
}
```

No `.encryptionKey(...)` call is present. The Realm database is opened without encryption.

---

## Step 4 — Checklist Review

### Section 1 — Signing and Keystores

No `.jks`, `.keystore`, or `.p12` files were examined in this assignment. `app/build.gradle` (read for context on dependencies and BASE_URL) shows `signingConfigs` referencing variables `DEV_STORE_FILE`, `DEV_STORE_PASSWORD`, `DEV_KEY_ALIAS`, `DEV_KEY_PASSWORD`, `UAT_*`, and `RELEASE_*`. These are variable references, not inline literals, and are consistent with injection from a properties file or Gradle properties.

No issues found in assigned files — Section 1.

---

### Section 2 — Network Security

No network client code, URL construction, or SSL/TLS configuration is present in the three assigned files. `BleUtil.java` is a pure Bluetooth byte-parsing utility. `ShockEventsDb.java` is a Realm model. `ShockEventService.java` calls `WebApi.sync().saveShockEvent(...)` to upload queued shock events, but the network implementation is in `WebApi`, which is outside this agent's assigned scope.

No issues found in assigned files — Section 2.

---

### Section 3 — Data Storage

**Finding — Medium: Realm database stored without encryption**

`ShockEventsDb` is a Realm model storing BLE impact event data: device MAC address (`mac_address`), event timestamp (`time`), and impact magnitude (`magnitude`). The Realm instance is initialised in `MyApplication.initDataBase()` using `RealmConfiguration.Builder` with no `.encryptionKey()` call. The resulting Realm database file is stored unencrypted on-device.

- MAC address is a device hardware identifier. Persistent storage of MAC addresses in plaintext can enable tracking of specific forklifts or operators over time.
- Magnitude data constitutes operational telemetry.
- Any process or tool with access to the app's data directory (rooted device, ADB backup if `allowBackup` is not set to `false`) can read this data without further authentication.

Realm supports AES-256 encryption via a 64-byte key passed to `.encryptionKey()`. This is not configured.

Relevant code:
- `ShockEventsDb.java` lines 15-17 — fields stored
- `ShockEventsDb.java` lines 46-66 — `saveData()` writes to Realm
- `MyApplication.java` lines 65-73 — Realm initialised without encryption key

**Finding — Low: `deleteRealmIfMigrationNeeded()` in production configuration**

`MyApplication.initDataBase()` (line 70) calls `.deleteRealmIfMigrationNeeded()`. This configuration silently drops the entire Realm database on schema migration instead of migrating data. In a production context this means shock event records that have not yet been uploaded to the server (buffered in the local Realm) would be permanently lost on any app update that increments `schemaVersion`. This is a data integrity concern that can result in impact events being dropped rather than uploaded. This same configuration governs `ShockEventsDb`.

No other data storage issues found in assigned files — Section 3.

---

### Section 4 — Input and Intent Handling

**Finding — Low: `ShockEventService` extends deprecated `IntentService`**

`ShockEventService` extends `android.app.IntentService` (line 25). `IntentService` was deprecated in Android API level 30 (Android 11). The recommended replacement is `WorkManager` or `JobIntentService`. Deprecated components may be removed from future API levels and can behave unexpectedly at high `targetSdkVersion` values.

`ShockEventService` is a Service component. Its exported status is determined by `AndroidManifest.xml` (outside this agent's scope). If it is declared without `android:exported="false"` — or if it has an `<intent-filter>` — it would be invocable by any app on the device.

Within the code itself: `onHandleIntent` dispatches on `intent.getAction()` and `intent.getStringExtra()`. Input arriving via `sendData()` or `startService()` from within the same process uses `LocalBroadcastManager` and explicit intents, which is appropriate. However, if the service is exported, external callers can pass arbitrary actions and extras. The `onShockDataRead` path reads `EXTRA_DATA` as a raw byte array and passes it to `saveShockEvent`, which calls `BleUtil.getIntValue` — this is safe as `getIntValue` performs a bounds check (line 236 of `BleUtil.java`). No privileged operations are triggered solely by external intent data arriving in this path.

**Observation — Info: `lastImpactEvent` is a public static field**

`public static ShockEventsItem lastImpactEvent = null` (line 145 of `ShockEventService.java`). Storing state as a static field on a Service class is an application-lifetime singleton pattern. If `ShockEventsItem` carries MAC address or telemetry data, this field persists in memory across operator sessions. If operator session change is not handled by clearing this field, the prior operator's impact event may be surfaced to the next operator. This intersects with Section 5 (Authentication and Session).

No other input/intent handling issues found in assigned files — Section 4.

---

### Section 5 — Authentication and Session

**Observation — Info: Static `lastImpactEvent` and `lastShockEventsItem` retained across sessions**

`ShockEventService` holds two static references that persist for the lifetime of the process:
- `private static ShockEventsItem lastShockEventsItem` (line 115) — used for deduplication
- `public static ShockEventsItem lastImpactEvent = null` (line 145) — used to surface impact alerts to UI

If operators share a device (shift changes), these fields are not cleared on logout. A new operator logging in would inherit the previous operator's last shock event in memory. The `lastImpactEvent` field is public, accessible from any class in the app. This is a minor session isolation concern.

No credential storage, token handling, or authentication logic is present in the three assigned files — Section 5.

---

### Section 6 — Third-Party Libraries

From `app/build.gradle`, the Realm dependency is applied as a plugin (`apply plugin: 'realm-android'`); version is not visible in `app/build.gradle` — the classpath version would be in the root `build.gradle` (outside this agent's scope). The Realm plugin version determines whether CVEs apply.

No third-party library dependency declarations are in the three assigned source files themselves — Section 6.

---

### Section 7 — Google Play and Android Platform

**Finding — Low: `IntentService` deprecated (API 30)**

As noted in Section 4, `ShockEventService extends IntentService` (line 25). `IntentService` is deprecated at API 30. If `targetSdkVersion` is 30 or higher, usage of `IntentService` generates lint warnings and may affect future platform compatibility.

No runtime permission requests, WebView usage, or manifest declarations are present in the three assigned files — Section 7.

---

## Summary of Findings

| ID | Severity | File | Description |
|----|----------|------|-------------|
| APP03-01 | Medium | ShockEventsDb.java / MyApplication.java | Realm database initialised without encryption; MAC address and telemetry data stored in plaintext |
| APP03-02 | Low | MyApplication.java (supporting) | `deleteRealmIfMigrationNeeded()` in production Realm config can silently drop unuploaded shock event records on schema migration |
| APP03-03 | Low | ShockEventService.java line 25 | `ShockEventService` extends deprecated `android.app.IntentService` (deprecated API 30) |
| APP03-04 | Info | ShockEventService.java lines 115, 145 | Static fields `lastShockEventsItem` and `lastImpactEvent` persist in memory across operator sessions; public `lastImpactEvent` not cleared on logout |

---

## Discrepancy Log

| Item | Checklist Value | Actual Value |
|------|----------------|--------------|
| Branch | main | master |
