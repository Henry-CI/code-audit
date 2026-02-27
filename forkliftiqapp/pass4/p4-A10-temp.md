# Pass 4 – Code Quality Audit
**Agent:** A10
**Audit run:** 2026-02-26-01
**Date:** 2026-02-27

---

## Assigned Files

1. `LibCommon/src/main/java/com/yy/libcommon/Util.java`
2. `LibCommon/src/main/java/com/yy/libcommon/WebActivity.java`
3. `LibCommon/src/main/java/com/yy/libcommon/WebService/GsonHelper.java`

---

## Step 1: Reading Evidence

### File 1: `Util.java`

**Class:** `com.yy.libcommon.Util`

**Constants/Fields:**
- `public final static int MAX_UPLOAD_IMAGE_SIZE = 480` (line 44)

**Methods (exhaustive):**

| Line | Method Signature |
|------|-----------------|
| 46 | `public static ArrayList<String> arrayListFromStrings(String[] ar)` |
| 56 | `public static String generateDeviceId(Context pContext)` |
| 86 | `public static String colorToHexString(int color)` |
| 90 | `public static int dpToPx(int dp, Context pContext)` |
| 103 | `public static int dpToPx(float dp, Context pContext)` |
| 116 | `public static String getLastDigitSufix(int number)` |
| 126 | `public static String getRandomInstanceId()` |
| 134 | `public static String getRandomString()` |
| 150 | `public static int getRandomNumber()` |
| 168 | `public static boolean isStringEmpty(String input)` |
| 172 | `public static void setLayoutClickable(View view, boolean enabled)` |
| 190 | `public static Bitmap decodeFile(String path, int maxSize)` |
| 194 | `public static Bitmap decodeFile(File f, int maxSize)` |
| 236 | `public static byte[] preProcessBitmapToByteArray(String pathToOurFile)` |
| 257 | `public static Bitmap preProcessBitmap(Bitmap bitmap, ByteArrayOutputStream byteArrayOutputStream)` |
| 281 | `public static Bitmap decodeFileFixOrientation(String file)` |
| 309 | `public static String bigDecimalToPriceStr(BigDecimal bigDecimal)` |
| 313 | `public static boolean bigDecimalsAreTheSame(BigDecimal bd1, BigDecimal bd2)` |
| 340 | `public static boolean integersAreTheSame(Integer i1, Integer i2)` |
| 367 | `public static String getRealPathFromURI(Context context, Uri contentUri)` |

**Imports noted:**
- `java.util.LinkedList` — imported but never referenced in any method body
- `java.security.MessageDigest`, `java.security.NoSuchAlgorithmException` — imported but never referenced
- `java.io.ByteArrayInputStream` — imported but never referenced

**Annotations:** None.

**Commented-out code blocks:**
- Lines 91–92 inside `dpToPx(int, Context)` — two lines using `DisplayMetrics` commented out
- Lines 104–105 inside `dpToPx(float, Context)` — duplicate two lines using `DisplayMetrics` commented out

---

### File 2: `WebActivity.java`

**Class:** `com.yy.libcommon.WebActivity` extends `BaseActivity`

**Fields (instance, package-private):**
- `WebView webView` (line 15)
- `LineProgress line_progress_bar` (line 16)
- `String url` (line 17)
- `View failed_text` (line 18)

**Constants:**
- `static public final String URL_KEY = "com.webactivity.url"` (line 20)

**Methods (exhaustive):**

| Line | Method Signature |
|------|-----------------|
| 23 | `protected void onCreate(Bundle savedInstanceState)` |
| 32 | `void initWebView()` |

**Anonymous classes / overrides inside `initWebView()`:**

| Line | Override |
|------|---------|
| 50 | `public void onProgressChanged(WebView view, int progress)` (WebChromeClient) |
| 60 | `public boolean shouldOverrideUrlLoading(WebView view, String url)` (WebViewClient) |
| 66 | `public void onPageStarted(WebView view, String url, Bitmap favicon)` (WebViewClient) |
| 71 | `public void onPageFinished(WebView view, String url)` (WebViewClient) |
| 76 | `public void onReceivedError(WebView view, int errorCode, String description, String failingUrl)` (WebViewClient) |

**Imports noted:** All imports used.

---

### File 3: `GsonHelper.java`

**Class:** `com.yy.libcommon.WebService.GsonHelper`

**Methods (exhaustive):**

| Line | Method Signature |
|------|-----------------|
| 13 | `public static <T> T objectFromString(String data, Class<T> dataClass)` |
| 17 | `private static JSONObject fromObjectNoNamePolicy(Object object)` |
| 30 | `public static JSONObject fromObject(Object object)` |
| 43 | `public static String stringFromObjectNoPolicy(Object object)` |

**Imports noted:** All imports used.

---

## Step 2 & 3: Findings

---

### A10-1 — HIGH: Unused imports in `Util.java` (dead code / build warnings)

**File:** `LibCommon/src/main/java/com/yy/libcommon/Util.java`
**Lines:** 19, 29, 27–28

Three imports are present that have no corresponding usage anywhere in the file:

```java
import java.io.ByteArrayInputStream;   // line 19 — never used
import java.util.LinkedList;            // line 30 — never used
import java.security.MessageDigest;     // line 27 — never used
import java.security.NoSuchAlgorithmException; // line 28 — never used
```

`MessageDigest` and `NoSuchAlgorithmException` together strongly suggest a hashing utility was partially implemented or removed, but the imports were left behind. `LinkedList` and `ByteArrayInputStream` are similarly orphaned. These generate IDE/compiler warnings and are dead code. The presence of `MessageDigest` specifically suggests deleted or missing functionality (e.g., MD5/SHA hashing of device identifiers).

**Classification:** HIGH — dead imports reveal deleted logic; `MessageDigest` suggests a security-relevant method was removed without audit.

---

### A10-2 — MEDIUM: Commented-out code duplicated across two overloads of `dpToPx` in `Util.java`

**File:** `LibCommon/src/main/java/com/yy/libcommon/Util.java`
**Lines:** 91–92 and 104–105

Identical two-line commented blocks appear in both `dpToPx(int, Context)` and `dpToPx(float, Context)`:

```java
//DisplayMetrics displayMetrics = pContext.getResources().getDisplayMetrics();
//int px = Math.round(dp * (displayMetrics.xdpi / DisplayMetrics.DENSITY_DEFAULT));
```

These lines use `xdpi` (the physical X DPI), which is different from the density-independent calculation that replaced it. The comments were never removed after the implementation was corrected. Both must be deleted; the duplication doubles the noise.

**Classification:** MEDIUM — commented-out code in two locations; the alternative implementation using `xdpi` is known incorrect (device-DPI-specific, not density-independent) which suggests why it was replaced, making reinstatement inappropriate.

---

### A10-3 — HIGH: Null-pointer risk in `generateDeviceId` — `WifiManager` not checked for null

**File:** `LibCommon/src/main/java/com/yy/libcommon/Util.java`
**Lines:** 60–63

```java
WifiManager wifiMan = (WifiManager) pContext.getSystemService(Context.WIFI_SERVICE);
WifiInfo wifiInf = wifiMan.getConnectionInfo();
macAddr = wifiInf.getMacAddress();
```

`getSystemService` can return `null` if the service is unavailable. `wifiMan` is never null-checked before calling `wifiMan.getConnectionInfo()`. If `wifiMan` is null this throws a `NullPointerException` at line 61 — outside the `try/catch` block, so the emulator fallback at line 72 is never reached in that scenario. Additionally, on Android 6+ `WifiInfo.getMacAddress()` always returns `"02:00:00:00:00:00"` for privacy reasons, making the UUID derived from MAC address useless and non-unique on modern devices.

**Classification:** HIGH — unguarded null dereference outside the catching block; additionally produces non-unique device IDs on Android 6+ (API 23+), a functional regression affecting all supported devices.

---

### A10-4 — MEDIUM: `getRandomNumber()` has flawed off-by-one logic and `_CHAR` constant duplicated between methods

**File:** `LibCommon/src/main/java/com/yy/libcommon/Util.java`
**Lines:** 150–166 and 136–137

`_CHAR` is a string constant defined identically in both `getRandomString()` (line 136) and `getRandomNumber()` (line 152). It is not extracted to a class-level constant despite being referenced in two related methods.

The logic in `getRandomNumber()` is also questionable:

```java
randomInt = random.nextInt(_CHAR.length());  // returns [0, 35]
if (randomInt - 1 == -1) {                   // i.e., if randomInt == 0
    return randomInt;                         // returns 0
} else {
    return randomInt - 1;                     // returns [0, 34], biasing toward lower indices
}
```

- Index 35 (the last character, `'0'`) can never be returned: when `randomInt == 35`, `35 - 1 == 34` is returned, making `'0'` unreachable.
- The method effectively draws from indices [0, 34] with index 0 having double probability (returned both when `randomInt == 0` and when... wait — index 0 is returned only when `randomInt == 0`; otherwise `randomInt - 1` is returned, mapping `randomInt == 1` to index 0 as well). So index 0 (`'A'`) has twice the probability of any other character.

**Classification:** MEDIUM — logic defect producing biased/truncated output; duplicated inline constant is a style/maintainability issue.

---

### A10-5 — MEDIUM: `isStringEmpty` has inverted semantics (returns `false` for null)

**File:** `LibCommon/src/main/java/com/yy/libcommon/Util.java`
**Line:** 168–170

```java
public static boolean isStringEmpty(String input){
    return (input != null && input.length() == 0);
}
```

This returns `false` when `input` is `null`, contrary to the conventional meaning of "isEmpty" in Android/Java (`TextUtils.isEmpty` returns `true` for both null and empty). Any caller relying on this to guard against null input will receive incorrect results — a null string is not considered empty, so null is silently accepted where an empty string would be rejected, or vice versa.

**Classification:** MEDIUM — semantic inversion of null check; any caller testing `isStringEmpty(str)` expecting null-safety will have a latent null dereference.

---

### A10-6 — LOW: `arrayListFromStrings` reimplements `Arrays.asList` without adding value

**File:** `LibCommon/src/main/java/com/yy/libcommon/Util.java`
**Lines:** 46–53

```java
public static ArrayList<String> arrayListFromStrings(String[] ar){
    ArrayList<String> list = new ArrayList<>();
    for(String s : ar ){
        list.add(s);
    }
    return list;
}
```

This is a manual reimplementation of `new ArrayList<>(Arrays.asList(ar))`. No additional logic justifies the custom loop. It also does not null-check `ar`, so passing null crashes with a `NullPointerException` inside the enhanced `for` loop.

**Classification:** LOW — unnecessary boilerplate; could be replaced with a single standard-library call; missing null guard.

---

### A10-7 — HIGH: Deprecated API usage in `WebActivity.java` — `onReceivedError` four-argument form and `shouldOverrideUrlLoading` String-based form

**File:** `LibCommon/src/main/java/com/yy/libcommon/WebActivity.java`
**Lines:** 60, 76

Two `WebViewClient` overrides use APIs deprecated in API 23 (Android 6.0):

```java
// Deprecated in API 23; replacement takes WebResourceRequest second parameter
public boolean shouldOverrideUrlLoading(WebView view, String url) { ... }

// Deprecated in API 23; replacement takes WebResourceRequest + WebResourceError
public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) { ... }
```

On devices running Android 6+ the deprecated form of `onReceivedError` may not be called for all error conditions (e.g., sub-resource errors); the replacement `onReceivedError(WebView, WebResourceRequest, WebResourceError)` is required. This means load errors on modern devices may silently not show the `failed_text` view.

**Classification:** HIGH — deprecated API may silently fail to trigger error UI on modern OS versions; the four-argument `onReceivedError` is specifically documented as unreliable on API 23+.

---

### A10-8 — MEDIUM: `WebActivity.java` — instance field `url` (line 17) is unused; local variable shadows it

**File:** `LibCommon/src/main/java/com/yy/libcommon/WebActivity.java`
**Lines:** 17, 34

The class declares an instance field `String url` at line 17. Inside `initWebView()` a local variable with the same name is declared at line 34:

```java
String url = getIntent().getStringExtra(URL_KEY);
```

This local variable shadows the instance field entirely. The instance field is never assigned or read. It is dead code, and the shadowing relationship is error-prone.

**Classification:** MEDIUM — dead instance field; name shadowing between field and local variable is a latent source of confusion.

---

### A10-9 — LOW: `WebActivity.java` — `onPageStarted` override is empty and adds no value

**File:** `LibCommon/src/main/java/com/yy/libcommon/WebActivity.java`
**Lines:** 66–68

```java
@Override
public void onPageStarted(WebView view, String url, Bitmap favicon) {
    super.onPageStarted(view, url, favicon);
}
```

This override only calls `super` and performs no additional action. It is dead code that should either be removed (to reduce noise) or given an intentional body (e.g., showing the progress bar, which is set up redundantly at lines 82–83 outside the client anyway).

**Classification:** LOW — no-op override; add logic or remove.

---

### A10-10 — LOW: `WebActivity.java` — progress bar shown redundantly at lines 82–83 after WebChromeClient is registered

**File:** `LibCommon/src/main/java/com/yy/libcommon/WebActivity.java`
**Lines:** 36–37, 82–83

`line_progress_bar.setVisibility(View.VISIBLE)` is called at line 37 (correct initial setup) and then again at line 83 after the WebViewClient is already set and immediately before `webView.loadUrl(url)`. The second call at line 83 is redundant since line 37 already made it visible and nothing in the intervening code changes that.

**Classification:** LOW — redundant visibility call.

---

### A10-11 — MEDIUM: `GsonHelper.java` — `fromObjectNoNamePolicy` is `private` but its only caller is `stringFromObjectNoPolicy`; coupling and naming are inconsistent with `fromObject`

**File:** `LibCommon/src/main/java/com/yy/libcommon/WebService/GsonHelper.java`
**Lines:** 17, 30, 43

The two JSON serialization paths have inconsistent access visibility and naming:

| Method | Access | Naming style |
|--------|--------|--------------|
| `fromObjectNoNamePolicy` (line 17) | `private` | verb+Object+qualifier |
| `fromObject` (line 30) | `public` | verb+Object |
| `stringFromObjectNoPolicy` (line 43) | `public` | returnType+verb+Object+qualifier |

`stringFromObjectNoPolicy` is the only public entry-point that uses the no-policy path; `fromObjectNoNamePolicy` exists solely as a private helper yet callers cannot opt into the same `JSONObject`-returning variant without the naming policy. The naming convention (`fromObject` vs `stringFromObjectNoPolicy`) is inconsistent: one is named by operation, the other by return type + operation.

There is also no corresponding `stringFromObject` (with policy) method, leaving the public API asymmetric.

**Classification:** MEDIUM — naming inconsistency and asymmetric public API; the private helper could be inlined into its single call site.

---

### A10-12 — LOW: `GsonHelper.java` — silent exception swallowing in `stringFromObjectNoPolicy`

**File:** `LibCommon/src/main/java/com/yy/libcommon/WebService/GsonHelper.java`
**Lines:** 47–49

```java
try {
    s = Objects.requireNonNull(jsonObject).toString();
} catch (Exception ignored) {
}
```

`catch (Exception ignored)` silently swallows all exceptions including `NullPointerException` (thrown by `requireNonNull` when `fromObjectNoNamePolicy` returns null due to a `JSONException` in the private helper). The method returns `""` without any logging, making serialization failures completely invisible. The `e.printStackTrace()` in the private helper (line 24) provides some signal but only to the console; the public method gives callers no indication of failure.

**Classification:** LOW — silent failure; callers receive an empty string with no indication that serialization failed.

---

### A10-13 — MEDIUM: `Util.java` — `decodeFile(File, int)` does not close streams in the success path and uses deprecated `inPurgeable`

**File:** `LibCommon/src/main/java/com/yy/libcommon/Util.java`
**Lines:** 204–222, 218

Two `FileInputStream` instances are opened. Both are explicitly closed (`fis.close()`) at lines 206 and 222. However, these close calls are not inside `finally` blocks or try-with-resources. If `BitmapFactory.decodeStream` throws an unchecked exception, the stream at line 220 would be leaked.

Additionally, `BitmapFactory.Options.inPurgeable` at line 218 has been deprecated since API 21 (Android 5.0) with no direct replacement (memory management was improved in the runtime). Using it generates a build warning on modern compile targets.

**Classification:** MEDIUM — stream resource not guaranteed to close on exceptional paths; deprecated `inPurgeable` field.

---

### A10-14 — MEDIUM: `Util.java` — `getRealPathFromURI` does not guard against null cursor or empty cursor result

**File:** `LibCommon/src/main/java/com/yy/libcommon/Util.java`
**Lines:** 367–382

```java
cursor = context.getContentResolver().query(...);
int column_index = cursor.getColumnIndexOrThrow(...);  // NPE if cursor is null
cursor.moveToFirst();                                   // no check that row exists
return cursor.getString(column_index);                  // undefined if moveToFirst returns false
```

`ContentResolver.query()` can return null (e.g., if the provider is unavailable). Additionally `moveToFirst()` returns `false` when the cursor is empty, but the return value is ignored; `cursor.getString(column_index)` in that case returns undefined/null behavior.

**Classification:** MEDIUM — two null/empty cases unguarded, both crashable on real devices (e.g., when media scanner has not indexed the file yet).

---

### A10-15 — INFO: `Util.java` — `getLastDigitSufix` has a typo in its name ("Sufix" should be "Suffix")

**File:** `LibCommon/src/main/java/com/yy/libcommon/Util.java`
**Line:** 116

```java
public static String getLastDigitSufix(int number) {
```

"Sufix" is a misspelling of "Suffix". This is a public API method name so renaming would be a breaking change for all callers. The typo should be corrected and all callers updated simultaneously.

**Classification:** INFO — cosmetic; public API typo that requires coordinated rename across callers.

---

### A10-16 — INFO: `Util.java` — `static public` modifier order on `URL_KEY` in `WebActivity.java` is non-standard

**File:** `LibCommon/src/main/java/com/yy/libcommon/WebActivity.java`
**Line:** 20

```java
static public final String URL_KEY = "com.webactivity.url";
```

The Java Language Specification and Google Java Style Guide both require the order `public static final`. `static public` is valid but non-standard and will trigger warnings from most style linters/checkstyle.

**Classification:** INFO — cosmetic style issue.

---

## Summary Table

| ID | Severity | File | Description |
|----|----------|------|-------------|
| A10-1 | HIGH | Util.java | Unused imports including `MessageDigest`/`NoSuchAlgorithmException`, suggesting deleted security logic |
| A10-2 | MEDIUM | Util.java | Commented-out `DisplayMetrics` code duplicated in both `dpToPx` overloads |
| A10-3 | HIGH | Util.java | `WifiManager` not null-checked in `generateDeviceId`; MAC address non-unique on API 23+ |
| A10-4 | MEDIUM | Util.java | `getRandomNumber()` off-by-one logic; `_CHAR` duplicated as inline literal |
| A10-5 | MEDIUM | Util.java | `isStringEmpty` returns `false` for null — inverted semantics vs. Android convention |
| A10-6 | LOW | Util.java | `arrayListFromStrings` reimplements `Arrays.asList`; missing null guard |
| A10-7 | HIGH | WebActivity.java | Deprecated `onReceivedError` (4-arg) and `shouldOverrideUrlLoading` (String) — may silently skip error UI on API 23+ |
| A10-8 | MEDIUM | WebActivity.java | Dead instance field `url` shadowed by local variable in `initWebView()` |
| A10-9 | LOW | WebActivity.java | No-op `onPageStarted` override; should be removed or given intent |
| A10-10 | LOW | WebActivity.java | Redundant `setVisibility(View.VISIBLE)` call on progress bar |
| A10-11 | MEDIUM | GsonHelper.java | Inconsistent naming/access between serialization methods; asymmetric public API |
| A10-12 | LOW | GsonHelper.java | `catch (Exception ignored)` silently swallows all serialization failures |
| A10-13 | MEDIUM | Util.java | `decodeFile` streams not closed in try-with-resources; deprecated `inPurgeable` |
| A10-14 | MEDIUM | Util.java | `getRealPathFromURI` unguarded null cursor and empty-cursor result |
| A10-15 | INFO | Util.java | Public method name typo `getLastDigitSufix` (should be `getSuffix`) |
| A10-16 | INFO | WebActivity.java | Non-standard `static public` modifier order on `URL_KEY` |
