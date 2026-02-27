# Pass 4 — Code Quality Audit
**Agent:** A43
**Audit Run:** 2026-02-26-01
**Date:** 2026-02-27

---

## Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/autoupdate/activity/ShowPackageAvailable.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/autoupdate/model/APKPackage.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/autoupdate/service/APKUpdateService.java`

---

## Step 1: Reading Evidence

### File 1: `ShowPackageAvailable.java`

**Class:** `ShowPackageAvailable extends Activity`
**Package:** `au.com.collectiveintelligence.fleetiq360.autoupdate.activity`

**Constants defined:**
| Name | Type | Value |
|------|------|-------|
| `TAG` | `private static final String` | `ShowPackageAvailable.class.getCanonicalName()` |
| `PACKAGE_EXTRA` | `private static final String` | `"apkPackage"` |
| `ANDROID_APK_MIME_TYPE` | `private static final String` | `"application/vnd.android.package-archive"` |

**Fields:**
| Name | Type | Visibility |
|------|------|------------|
| `service` | `APKUpdateService` | `private` |

**Methods (exhaustive):**
| Method | Line | Visibility |
|--------|------|------------|
| `ShowPackageAvailable()` (constructor) | 47 | `public` |
| `onCreate(Bundle)` | 52 | `protected` |
| `onStart()` | 59 | `protected` |
| `alertNewPackageAvailable(APKPackage)` | 88 | `private` |
| `haveStoragePermission()` | 103 | `private` |
| `downloadAndInstall(APKPackage)` | 120 | `private` |
| `writeResponseBodyToDisk(ResponseBody, File)` | 143 | `private` |
| `onKeyDown(int, KeyEvent)` | 153 | `public` |
| `raiseNotificationPackageReadyToInstall(File)` | 158 | `private` |
| `onRequestPermissionsResult(int, String[], int[])` | 174 | `public` |

**Interfaces/Types defined:** None (Activity subclass only)

**Anonymous inner classes:**
- `Callback<APKPackage>` (line 68) — Retrofit callback for update check
- `View.OnClickListener` (line 96) — download button listener
- `Callback<ResponseBody>` (line 122) — Retrofit callback for download

---

### File 2: `APKPackage.java`

**Class:** `APKPackage implements Serializable`
**Package:** `au.com.collectiveintelligence.fleetiq360.autoupdate.model`

**Fields:**
| Name | Type | Visibility |
|------|------|------------|
| `name` | `String` | `private` |
| `fileName` | `String` | `private` |
| `url` | `String` | `private` |
| `major` | `int` | `private` |
| `minor` | `int` | `private` |
| `patch` | `int` | `private` |

**Methods (exhaustive):**
| Method | Line | Visibility |
|--------|------|------------|
| `getName()` | 14 | `public` |
| `setName(String)` | 18 | `public` |
| `getFileName()` | 22 | `public` |
| `setFileName(String)` | 26 | `public` |
| `getUrl()` | 30 | `public` |
| `setUrl(String)` | 34 | `public` |
| `getMajor()` | 38 | `public` |
| `setMajor(int)` | 42 | `public` |
| `getMinor()` | 46 | `public` |
| `setMinor(int)` | 50 | `public` |
| `getPatch()` | 54 | `public` |
| `setPatch(int)` | 58 | `public` |

**Types/Interfaces implemented:** `java.io.Serializable`

---

### File 3: `APKUpdateService.java`

**Class:** `APKUpdateService` (interface)
**Package:** `au.com.collectiveintelligence.fleetiq360.autoupdate.service`

**Methods (exhaustive):**
| Method | Line | Annotations |
|--------|------|-------------|
| `getLatestAvailableUpdate(String pkgName, String version)` | 13 | `@GET("rest/apk/{pkgname}/update")`, `@Path("pkgname")`, `@Query("version")` |
| `downloadPackage(String packageUrl)` | 15 | `@GET`, `@Url` |

**Return types:** `Call<APKPackage>`, `Call<ResponseBody>`

---

## Step 2 & 3: Findings

---

### A43-1 — HIGH: `Log.e` used for non-error informational messages (style inconsistency in `haveStoragePermission`)

**File:** `ShowPackageAvailable.java`
**Lines:** 105, 110, 113

`Log.e` (error level) is used to log purely informational, non-error conditions:

```java
// Line 105 — informational "you already have permission" message logged at ERROR level
Log.e("Permission error", "You already have the permission");

// Line 110 — confirmation of granted permission logged at ERROR level
Log.e(TAG, "You have permission");

// Line 113 — permission request initiation logged at ERROR level
Log.e(TAG, "You have asked for permission");
```

Separately, line 105 uses the raw string literal `"Permission error"` as the TAG rather than the class-level `TAG` constant, which is inconsistent with all other log calls in the file. Debug- or info-level log messages logged as errors pollute crash reporting and logcat error filters. They mislead developers diagnosing real failures.

---

### A43-2 — HIGH: `PACKAGE_EXTRA` constant is dead code — the Intent extra is never put

**File:** `ShowPackageAvailable.java`
**Lines:** 42, 180

`PACKAGE_EXTRA` is defined at line 42 and consumed at line 180 inside `onRequestPermissionsResult`:

```java
downloadAndInstall((APKPackage) getIntent().getSerializableExtra(PACKAGE_EXTRA));
```

No code in the entire codebase puts the `"apkPackage"` extra into the Intent used to start `ShowPackageAvailable`. The activity fetches the `APKPackage` via its own network call in `onStart` and passes it directly to `alertNewPackageAvailable`/`downloadAndInstall` via closure, not via Intent extras. Consequently, when the permission grant callback fires, `getIntent().getSerializableExtra(PACKAGE_EXTRA)` will always return `null`, causing a `NullPointerException` inside `downloadAndInstall` at:

```java
service.downloadPackage(apkPackage.getUrl())  // NPE — apkPackage is null
```

The `PACKAGE_EXTRA` constant and the `getSerializableExtra` retrieval are effectively dead code that will crash at runtime if storage permission is ever requested and subsequently granted.

---

### A43-3 — HIGH: Deprecated `Uri.fromFile` used — will crash on Android 7+ (API 24+) due to `FileUriExposedException`

**File:** `ShowPackageAvailable.java`
**Line:** 160

```java
notificationIntent.setDataAndType(Uri.fromFile(apkPackageFile), ANDROID_APK_MIME_TYPE);
```

`Uri.fromFile` produces a `file://` URI. Since Android 7.0 (API 24), sharing a `file://` URI across process boundaries via an Intent raises `FileUriExposedException` at runtime, crashing the app. The correct approach is to use `FileProvider` to obtain a `content://` URI. The `#noinspection deprecation` suppression comment is present on the `Notification.Builder` usage (line 162) but not here; this issue lacks even that acknowledgement.

---

### A43-4 — HIGH: Deprecated `Notification.Builder` API without channel ID — silent on Android 8+ (API 26+)

**File:** `ShowPackageAvailable.java`
**Lines:** 162–168

```java
//noinspection deprecation
Notification notification = new Notification.Builder(this)
        .setContentTitle("ForkliftIQ360 App update available")
        .setContentText("Click to install")
        .setSmallIcon(R.mipmap.ic_launcher)
        .setContentIntent(pendingIntent)
        .setAutoCancel(true).build();
```

The single-argument `Notification.Builder(Context)` constructor is deprecated since API 26. On Android 8.0+, notifications built without a notification channel ID are silently dropped and never displayed to the user. The suppression comment acknowledges deprecation but does not resolve it — the update notification will simply not appear on the majority of Android devices in current use (API 26 is the `targetSdkVersion` for this app per `build.gradle` line 40 reference, meaning this breakage is not deferred).

---

### A43-5 — MEDIUM: `PendingIntent` created without `FLAG_IMMUTABLE` or `FLAG_MUTABLE` — crash on Android 12+ (API 31+)

**File:** `ShowPackageAvailable.java`
**Line:** 161

```java
PendingIntent pendingIntent = PendingIntent.getActivity(this, 0, notificationIntent, 0);
```

Starting with Android 12 (API 31), `PendingIntent.getActivity` with a flags argument of `0` (neither `FLAG_IMMUTABLE` nor `FLAG_MUTABLE` set) throws an `IllegalArgumentException` at runtime. The flag `PendingIntent.FLAG_IMMUTABLE` should be specified.

---

### A43-6 — MEDIUM: Explicit public no-arg constructor in Activity initialises service field — fragile lifecycle pattern

**File:** `ShowPackageAvailable.java`
**Lines:** 47–49

```java
public ShowPackageAvailable() {
    service = APKUpdateServiceFactory.getService();
}
```

Android Activities must have a public no-arg constructor for the framework to instantiate them, but no logic should be performed there. The framework may create Activity instances without calling the constructor in certain restoration paths, and constructor-time service initialisation can fail silently or produce unpredictable behaviour if `BuildConfig` or static factory state is not yet ready. Service initialisation should occur in `onCreate`. The pattern is also non-testable without a running `APKUpdateServiceFactory`.

---

### A43-7 — MEDIUM: Hard-coded string in notification title — not localisable

**File:** `ShowPackageAvailable.java`
**Line:** 164

```java
.setContentTitle("ForkliftIQ360 App update available")
```

The notification title is a hard-coded string literal. It should be a string resource reference (`R.string.*`) to support localisation and to follow the project's own conventions (the rest of the UI is driven through layout XML resources). Similarly, `"Click to install"` at line 165 is hard-coded.

---

### A43-8 — MEDIUM: `onRequestPermissionsResult` boundary check is inverted — off-by-one allows out-of-bounds access

**File:** `ShowPackageAvailable.java`
**Lines:** 176–179

```java
if (grantResults.length <= 2 ||
        grantResults[0] != PackageManager.PERMISSION_GRANTED ||
        grantResults[1] != PackageManager.PERMISSION_GRANTED)
    return;
```

Two permissions are requested (`WRITE_EXTERNAL_STORAGE` and `READ_EXTERNAL_STORAGE`). The guard `grantResults.length <= 2` is wrong: a length of exactly 2 contains valid entries at indices 0 and 1. The correct guard is `grantResults.length < 2`. As written, the guard will always short-circuit and return early when both permissions are granted (length == 2), meaning `downloadAndInstall` is never reached — the bug compounds A43-2 in making the post-permission-grant flow entirely unreachable.

---

### A43-9 — MEDIUM: `APKPackage` exposes separate `major`/`minor`/`patch` integer fields with no version comparison logic

**File:** `APKPackage.java`
**Lines:** 10–12, 38–60

`APKPackage` exposes three discrete version component fields (`major`, `minor`, `patch`) but provides no method to compare versions, construct a version string, or determine whether the package represents a newer version than the currently installed one. All version comparison logic, if any exists, must be re-implemented by every consumer. The fields are set by Gson deserialization but appear unused by the activity (`ShowPackageAvailable`), which does not check version numbers before downloading — it downloads any non-null response unconditionally.

---

### A43-10 — LOW: `writeResponseBodyToDisk` does not null-check `response.body()` before use

**File:** `ShowPackageAvailable.java`
**Lines:** 127, 143–149

```java
writeResponseBodyToDisk(response.body(), apkPackageFile);
```

`response.body()` can return `null` for successful HTTP responses with no body (e.g., HTTP 204). Passing `null` as the `body` parameter to `writeResponseBodyToDisk` will cause a `NullPointerException` at `body.byteStream()` on line 144. There is no HTTP status code check on the response prior to this call.

---

### A43-11 — LOW: `getExternalStoragePublicDirectory` deprecated in API 29 — path constructed via string concatenation

**File:** `ShowPackageAvailable.java`
**Line:** 125

```java
final File apkPackageFile = new File(
    Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS)
        .getAbsolutePath() + "/" + apkPackage.getFileName());
```

`Environment.getExternalStoragePublicDirectory` is deprecated since API 29. The path is constructed with raw string concatenation (`+ "/"`) rather than `new File(directory, filename)`, which is fragile on edge cases where the filename may contain path separators. Both issues exist in the same statement.

---

### A43-12 — LOW: `onKeyDown` override is redundant — back key already finishes Activity by default

**File:** `ShowPackageAvailable.java`
**Lines:** 153–156

```java
@Override
public boolean onKeyDown(int keyCode, KeyEvent event) {
    if ((keyCode == KeyEvent.KEYCODE_BACK)) finish();
    return super.onKeyDown(keyCode, event);
}
```

The default `Activity.onKeyDown` implementation already calls `finish()` when `KEYCODE_BACK` is pressed. This override duplicates that behaviour, calls `finish()` twice (once explicitly, then the `super` call triggers it again), and adds no value. It is dead / redundant code.

---

### A43-13 — LOW: `APKPackage` implements `Serializable` but defines no `serialVersionUID`

**File:** `APKPackage.java`
**Line:** 5

```java
public class APKPackage implements Serializable {
```

No `private static final long serialVersionUID` is declared. Java will auto-generate a serialVersionUID based on class structure; any field or method change will silently change this ID, causing `InvalidClassException` when deserialising previously stored instances (e.g., if the object is ever stored in a Bundle/SharedPreference/file). This is a build warning in most IDEs.

---

### A43-14 — INFO: `@SuppressWarnings` via `//noinspection deprecation` suppresses warning without documenting workaround plan

**File:** `ShowPackageAvailable.java`
**Line:** 162

```java
//noinspection deprecation
Notification notification = new Notification.Builder(this)
```

The inline suppression silences the IDE warning for the deprecated single-argument `Notification.Builder` constructor but leaves no comment explaining why the API 26+ `Notification.Builder(Context, String channelId)` form is not used, nor any tracking issue reference. Combined with A43-4, this suppression actively hides a functional defect.

---

## Summary Table

| ID | Severity | File | Line(s) | Issue |
|----|----------|------|---------|-------|
| A43-1 | HIGH | ShowPackageAvailable.java | 105, 110, 113 | `Log.e` used for non-error informational messages; inconsistent TAG literal |
| A43-2 | HIGH | ShowPackageAvailable.java | 42, 180 | `PACKAGE_EXTRA` is dead code; Intent extra never put; NPE when permission granted |
| A43-3 | HIGH | ShowPackageAvailable.java | 160 | `Uri.fromFile` causes `FileUriExposedException` crash on API 24+ |
| A43-4 | HIGH | ShowPackageAvailable.java | 162–168 | Deprecated `Notification.Builder` without channel ID; notification silently dropped on API 26+ |
| A43-5 | MEDIUM | ShowPackageAvailable.java | 161 | `PendingIntent` missing `FLAG_IMMUTABLE`/`FLAG_MUTABLE`; crash on API 31+ |
| A43-6 | MEDIUM | ShowPackageAvailable.java | 47–49 | Service initialised in Activity constructor — fragile lifecycle pattern |
| A43-7 | MEDIUM | ShowPackageAvailable.java | 164–165 | Hard-coded string literals in notification; not localisable |
| A43-8 | MEDIUM | ShowPackageAvailable.java | 176–179 | Off-by-one in `grantResults.length` guard makes post-permission path unreachable |
| A43-9 | MEDIUM | APKPackage.java | 10–12 | Version fields with no comparison logic; version not checked before download |
| A43-10 | LOW | ShowPackageAvailable.java | 127, 143 | No null-check on `response.body()` before use; NPE on HTTP 204 |
| A43-11 | LOW | ShowPackageAvailable.java | 125 | Deprecated `getExternalStoragePublicDirectory` (API 29+); string-concatenated path |
| A43-12 | LOW | ShowPackageAvailable.java | 153–156 | `onKeyDown` override is redundant; duplicates default back-key behaviour |
| A43-13 | LOW | APKPackage.java | 5 | `Serializable` without `serialVersionUID`; build warning |
| A43-14 | INFO | ShowPackageAvailable.java | 162 | `//noinspection deprecation` suppresses warning with no documented plan |
