# Audit Report — Pass 4 (Code Quality)
**Agent:** A17
**Audit Run:** 2026-02-26-01
**Date:** 2026-02-27
**Scope:** WebService layer — HttpClient, ImagePostBackgroundTask, ImagePostRequest

---

## Section 1: Reading Evidence

### File 1: HttpClient.java
**Path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/HttpClient.java`
**Class:** `HttpClient`

**Fields:**
| Name | Type | Visibility | Line |
|---|---|---|---|
| `isSynchronous` | `boolean` | `public` | 40 |
| `DEFAULT_TIMEOUT_MS` | `static final int` | `public` | 42 |
| `LOGIN_TIMEOUT_MS` | `static final int` | `public` | 43 |
| `mRequestQueue` | `static RequestQueue` | `private static` | 48 |
| `mCurrentRequestDesc` | `String` | `private` | 52 |
| `mWebRequestQueue` | `ArrayDeque<Request>` | `private` | 54 |
| `mImageLoader` | `ImageLoader` | `private` | 58 |
| `TAG` | `static final String` | `public static` | 62 |

**Methods:**
| Method | Visibility | Return Type | Line |
|---|---|---|---|
| `HttpClient(Context context)` | `public` | constructor | 65 |
| `initRequestQueue(Context pContext)` | `public static` | `void` | 72 |
| `getRequestQueue()` | `public` | `RequestQueue` | 79 |
| `setCommonData(JSONObject jsonObject)` | `public static` | `void` | 92 |
| `jsonFromWebParam(Object object)` | `public static` | `JSONObject` | 104 |
| `sendRequest(WebRequest request)` | `private` | `void` | 110 |
| `addRequest(WebRequest request)` | `private` | `void` | 120 |
| `sendRequest(GsonRequest request)` | `private` | `void` | 131 |
| `removeRequest(WebRequest request)` | `public` | `void` | 149 |
| `enqueueRequest(GsonRequest webRequest)` | `public` | `void` | 154 |
| `syncSendRequest(GsonRequest gsonRequest)` | `void` (package-private) | `void` | 162 |
| `readStream(InputStream stream, int maxLength)` | `private static` | `String` | 225 |
| `retryOnAuthFail(WebRequest msg)` | `protected` | `void` | 248 |

**Types referenced:** `RequestQueue`, `ImageLoader`, `ArrayDeque<Request>`, `GsonRequest`, `WebRequest`, `GetTokenResult`, `WebListener`, `WebResult`

**Commented-out code:**
- Line 53: `//private Queue mCustomRequestQueue;`
- Lines 133–134: inline comment warning that timeout is not working

---

### File 2: ImagePostBackgroundTask.java
**Path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/ImagePostBackgroundTask.java`
**Class:** `ImagePostBackgroundTask extends AsyncTask<...>`

**Inner static classes:**
| Name | Type | Line |
|---|---|---|
| `ImageUploadParam` | `public static class` | 21 |
| `ImageUploadResult` | `public static class` | 30 |
| `ImageUploadCallBack` | `public static class` | 35 |

**Fields on ImagePostBackgroundTask:**
| Name | Type | Visibility | Line |
|---|---|---|---|
| `imageUploadParam` | `ImageUploadParam` | package-private | 18 |

**Fields on ImageUploadParam:**
| Name | Type | Visibility | Line |
|---|---|---|---|
| `url` | `String` | `public` | 22 |
| `imagePath` | `String` | `public` | 23 |
| `multiPathArray` | `ArrayList<String>` | `public` | 24 |
| `fileNames` | `ArrayList<String>` | `public` | 25 |
| `bitmap` | `Bitmap` | `public` | 26 |
| `callback` | `ImageUploadCallBack` | `public` | 27 |

**Fields on ImageUploadResult:**
| Name | Type | Visibility | Line |
|---|---|---|---|
| `imageParam` | `ImageUploadParam` | `public` | 31 |
| `succeed` | `boolean` | `public` | 32 |

**Methods:**
| Method | Visibility | Return Type | Line |
|---|---|---|---|
| `doInBackground(ImageUploadParam... params)` | `protected @Override` | `ImageUploadResult` | 42 |
| `onPostExecute(ImageUploadResult result)` | `protected @Override` | `void` | 65 |
| `uploadImage(ImageUploadParam param)` | `private static` | `void` | 72 |
| `uploadImage(String url, ArrayList<String>, ArrayList<String>, ImageUploadCallBack)` | `public static` | `void` | 77 |
| `uploadImage(String url, String path, ImageUploadCallBack)` | `public static` | `void` | 97 |
| `uploadImage(String url, Bitmap bitmap, ImageUploadCallBack)` | `public static` | `void` | 114 |
| `readFileData(String imagePath)` | `static` (package-private) | `byte[]` | 131 |
| `ImageUploadCallBack.onUploadResult(ImageUploadResult result)` | `public` | `void` | 36 |

**Imports unused:** `ByteArrayOutputStream` imported (line 10) — only used indirectly via `readFileData`.

---

### File 3: ImagePostRequest.java
**Path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/ImagePostRequest.java`
**Class:** `ImagePostRequest`

**Methods:**
| Method | Visibility | Return Type | Line |
|---|---|---|---|
| `SendHttpImage(String urlServer, String pathToOurFile)` | `public static` | `boolean` | 24 |
| `SendHttpImage(String urlServer, byte[] imageByte)` | `public static` | `boolean` | 32 |
| `SendHttpImage(String urlServer, Bitmap bitmap)` | `public static` | `boolean` | 100 |
| `SendMultipartHttpImage(String urlServer, ArrayList<String>, ArrayList<String>)` | `public static` | `boolean` | 117 |
| `isMultiPart(String urlServer)` | `static` (package-private) | `boolean` | 107 |

**Commented-out code:**
- Lines 154–155:
  ```java
  //                outputStream.writeBytes("Content-Transfer-Encoding: binary;" + lineEnd);
  //                outputStream.writeBytes(lineEnd);
  ```

**Imports unused:**
- Line 15: `import static android.R.attr.src;` — this identifier (`src`) is never referenced anywhere in the file.

---

## Section 2: Findings

---

### A17-1 — CRITICAL: `setCommonData` is a complete no-op; silently swallows all exceptions
**File:** `HttpClient.java`, lines 92–102
**Category:** Dead code / Silent failure

```java
public static void setCommonData(JSONObject jsonObject){
    try {
        if (jsonObject != null) {
        }
    }catch (Exception e) {
        // swallowed silently
    }
}
```

The method body is entirely empty — the `if` block contains no statements. The catch block swallows every exception without logging or rethrowing. `setCommonData` is called by `jsonFromWebParam` (line 106) on every outbound request. Any intended mutation of common request fields (e.g., auth headers, device ID, app version) is absent. This is functional dead code at a critical integration point: every web request built through `jsonFromWebParam` silently skips whatever this method was supposed to do.

---

### A17-2 — HIGH: Deprecated `AsyncTask` used without suppression annotation
**File:** `ImagePostBackgroundTask.java`, line 15
**Category:** Build warning / Deprecated API

```java
public class ImagePostBackgroundTask extends AsyncTask<ImagePostBackgroundTask.ImageUploadParam, String, ImagePostBackgroundTask.ImageUploadResult>
```

`android.os.AsyncTask` was deprecated in API level 30 (Android 11). The class carries no `@SuppressWarnings("deprecation")` annotation. On minSdkVersion >= 30 builds the compiler emits a deprecation warning. More critically, `AsyncTask` has known thread-pool starvation behaviour and no built-in lifecycle awareness, creating a risk of leaked tasks when the host activity or fragment is destroyed before upload completes.

---

### A17-3 — HIGH: `isSynchronous` is a public mutable field on a class used as a dependency
**File:** `HttpClient.java`, line 40
**Category:** Leaky abstraction / Style inconsistency

```java
public boolean isSynchronous = false;
```

The execution path (`syncSendRequest` vs. `sendRequest`) is controlled by a raw public field rather than a constructor argument, factory method, or setter with validation. Any caller can flip the flag mid-request sequence, causing non-deterministic dispatch. A `public final` boolean set at construction or a private field with a controlled setter would prevent unintended mutation.

---

### A17-4 — HIGH: `syncSendRequest` does not close `HttpURLConnection` in a `finally` block; connection leak on exception
**File:** `HttpClient.java`, lines 162–219
**Category:** Resource leak

```java
HttpURLConnection connection = null;
...
try {
    connection = (HttpURLConnection) url.openConnection();
    ...
}
catch (Exception ex) {
    ex.printStackTrace();
}
gsonRequest.deliverResult(serverResponseCode, response);
```

If any exception is thrown after `openConnection()`, `connection.disconnect()` is never called. The same applies to the `InputStream` obtained at line 208 — it is never explicitly closed. On Android, leaked HTTP connections cause exhaustion of the underlying socket pool. The `outputStream` local variable at line 200 is declared outside the try block and also lacks a `finally`-close.

---

### A17-5 — HIGH: `SendHttpImage(byte[])` and `SendMultipartHttpImage` do not close `HttpURLConnection` in a `finally` block
**File:** `ImagePostRequest.java`, lines 32–98 and 117–178
**Category:** Resource leak

Both methods declare `connection` before the try block but never call `connection.disconnect()` in a `finally` clause. An exception thrown after `openConnection()` leaves the socket open. This mirrors A17-4 in the synchronous image upload path.

---

### A17-6 — HIGH: `SendMultipartHttpImage` silently swallows all exceptions
**File:** `ImagePostRequest.java`, lines 169–172
**Category:** Silent failure

```java
catch (Exception ex)
{
    //Exception handling
}
```

The catch block contains only a placeholder comment. When a network failure, malformed URL, or I/O error occurs, the caller receives `false` (because `serverResponseCode` remains 0) with no diagnostic information. This makes production upload failures invisible in logs. Compare with `SendHttpImage(byte[])` at line 88–91 which at least calls `ex.printStackTrace()` — inconsistent error handling within the same class.

---

### A17-7 — MEDIUM: `readFileData` in `ImagePostBackgroundTask` is dead code — never called
**File:** `ImagePostBackgroundTask.java`, lines 131–138
**Category:** Dead code

```java
static byte[] readFileData(String imagePath) {
    Bitmap bitmap = BitmapFactory.decodeFile(imagePath);
    ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
    Util.preProcessBitmap(bitmap, byteArrayOutputStream);
    byte[] byteData = byteArrayOutputStream.toByteArray();
    return byteData;
}
```

This method duplicates the logic already present in `ImagePostRequest.SendHttpImage(String, String)` (which also decodes via `BitmapFactory.decodeFile` and delegates to `Util.preProcessBitmap`). `readFileData` is package-private and has no callers within the class or (visibly) from other files. It is unreferenced dead code and a maintenance hazard because any future divergence in pre-processing logic will be invisible.

---

### A17-8 — MEDIUM: Commented-out code left in production source
**Files and lines:**
- `HttpClient.java` line 53: `//private Queue mCustomRequestQueue;`
- `ImagePostRequest.java` lines 154–155: `Content-Transfer-Encoding` header lines

These blocks represent abandoned design decisions. The `mCustomRequestQueue` comment is directly adjacent to the `mWebRequestQueue` field that replaced it — the intent of the original queue type and why it was removed is undocumented. The `Content-Transfer-Encoding` lines in `SendMultipartHttpImage` suggest an intentional protocol change that was never confirmed or cleaned up. Commented-out code should be removed; version history provides the record if recovery is needed.

---

### A17-9 — MEDIUM: `isMultiPart` uses hard-coded URL substring matching to determine request format
**File:** `ImagePostRequest.java`, lines 107–115
**Category:** Leaky abstraction / fragile logic

```java
static boolean isMultiPart(String urlServer){
    if(urlServer.contains("driveraccess") || urlServer.contains("appuser/photo")
            || urlServer.contains("impactimage")){
        return true;
    }
    ...
}
```

The multipart/binary decision is driven by pattern-matching URL strings rather than a caller-supplied parameter or strategy. This couples the request-formatting logic to specific API path names. Adding a new endpoint that requires multipart encoding requires modifying `ImagePostRequest` — violating the Open/Closed Principle and making the call sites opaque (callers cannot determine from the call signature whether their request will be multipart). The method is also package-private, making it untestable from outside the package.

---

### A17-10 — MEDIUM: `sendRequest(WebRequest)` adds the request to the queue twice — once via `addRequest` and once directly
**File:** `HttpClient.java`, lines 110–118
**Category:** Logic error / style inconsistency

```java
private void sendRequest(WebRequest request){
    request.setHttpClient(this);
    addRequest(request);          // calls getRequestQueue().add(request) — line 128
    mWebRequestQueue.push(request); // also pushed to internal deque — line 116
}
```

`addRequest` itself (line 120–129) also calls `request.setHttpClient(this)` on line 126, making the `setHttpClient` call at line 112 redundant. More significantly, `sendRequest(GsonRequest)` calls `mWebRequestQueue.push` before `addRequest` (line 144 then 146), while `sendRequest(WebRequest)` calls `addRequest` before the push (line 114 then 116). The order is inconsistent between the two overloads and could matter if `addRequest` or the Volley queue immediately begins dispatching.

---

### A17-11 — MEDIUM: `mWebRequestQueue` (internal deque) is populated but never drained; grows without bound
**File:** `HttpClient.java`, lines 54, 116, 144, 149–152
**Category:** Memory leak / dead code

Requests are pushed onto `mWebRequestQueue` in both `sendRequest` overloads. `removeRequest` (line 149) removes only `WebRequest` items. `GsonRequest` items are pushed but have no removal path. The deque is never iterated or cleared anywhere in this file. If `HttpClient` is a long-lived object (it is constructed early and its `mRequestQueue` is static), this deque accumulates every issued request for the lifetime of the process, preventing GC of completed request objects and their payloads.

---

### A17-12 — MEDIUM: `syncSendRequest` is package-private but is part of the functional dispatch path
**File:** `HttpClient.java`, line 162
**Category:** Leaky abstraction / visibility inconsistency

`syncSendRequest` is the actual executor when `isSynchronous == true`, called from the public `enqueueRequest`. It is package-private (no modifier), making it callable by any class in the same package — but the intent appears to be that it is an implementation detail. All other internal helpers in this class are `private`. The inconsistent visibility exposes an implementation detail to package-peers.

---

### A17-13 — MEDIUM: `mCurrentRequestDesc` is declared but never written or read
**File:** `HttpClient.java`, line 52
**Category:** Dead code / unused field

```java
private String mCurrentRequestDesc;
```

The field is initialised to `null` by default and is never assigned or accessed anywhere in the class. The Javadoc comment directly above `mRequestQueue` (lines 47–49) describes it as "the description of the current request passed back to the triggering activity", implying a feature that was designed but never implemented.

---

### A17-14 — MEDIUM: `mImageLoader` is declared but never initialised or used
**File:** `HttpClient.java`, line 58
**Category:** Dead code / unused field

```java
private ImageLoader mImageLoader;
```

`ImageLoader` is imported (line 15) and the field is declared, but it is never initialised in the constructor or any method, and never accessed. This is dead code that imports an additional Volley dependency unnecessarily.

---

### A17-15 — LOW: `import static android.R.attr.src` is unused
**File:** `ImagePostRequest.java`, line 15
**Category:** Build warning / dead import

```java
import static android.R.attr.src;
```

The identifier `src` from `android.R.attr` is never referenced in the file. This static import was likely a copy-paste artefact. Most IDE lint checks (Android Studio, Checkstyle) flag this as an unused import warning.

---

### A17-16 — LOW: Method naming convention violates Java standards (`SendHttpImage`, `SendMultipartHttpImage`)
**File:** `ImagePostRequest.java`, lines 24, 32, 100, 117
**Category:** Style inconsistency

All four public methods in `ImagePostRequest` use `UpperCamelCase` (PascalCase) rather than the Java standard `lowerCamelCase` for method names. Every other method in the audited codebase (`sendRequest`, `addRequest`, `enqueueRequest`, `uploadImage`, `readFileData`, etc.) follows the standard convention. This inconsistency suggests `ImagePostRequest` was ported from another language (possibly C# or Objective-C) without renaming.

---

### A17-17 — LOW: Inline comment contains HTML entity `&amp;` instead of `&`
**Files:**
- `HttpClient.java`, line 173: `// Allow Inputs &amp; Outputs.`
- `ImagePostRequest.java`, line 48: `// Allow Inputs &amp; Outputs.`

The comment text `Allow Inputs &amp; Outputs.` contains an HTML entity. This suggests the comment was copied from HTML documentation or a web-based editor. While cosmetically minor, it indicates copy-paste provenance and that both methods share a common template origin — further evidence that one of them duplicates the other.

---

### A17-18 — LOW: `syncSendRequest` comment at line 173 mismatches the actual max-length value
**File:** `HttpClient.java`, lines 211–212
**Category:** Misleading comment

```java
// Converts Stream to String with max length of 500.
response = readStream(inputStream, 1024*1024);
```

The comment states "max length of 500" but the actual argument is `1024 * 1024` (1 MiB). The comment is a stale copy from an earlier version where the limit was 500 characters.

---

### A17-19 — LOW: Boundary string in `SendHttpImage(byte[])` is a weak literal `"*****"`
**File:** `ImagePostRequest.java`, line 37
**Category:** Protocol correctness / style inconsistency

```java
String boundary = "*****";
```

`SendMultipartHttpImage` (line 122) uses a UUID-format boundary (`B0EC8D07-EBF1-4EA7-966C-E492A9F2C36E`), which is the correct approach. `SendHttpImage(byte[])` uses a five-asterisk literal. Per RFC 2046, the boundary must not appear in the body content. A static `"*****"` boundary can collide with JPEG data, corrupting the upload silently. The inconsistency between the two methods in the same class is also a style issue.

---

### A17-20 — INFO: `DEFAULT_TIMEOUT_MS` constant is declared but never used within `HttpClient`
**File:** `HttpClient.java`, line 42
**Category:** Unused constant / informational

```java
public static final int DEFAULT_TIMEOUT_MS = 30000; //30 seconds
```

`LOGIN_TIMEOUT_MS` is applied at line 135. `DEFAULT_TIMEOUT_MS` is never referenced in this file. It may be consumed by other classes, but its presence here without local use suggests it is either unused or was intended for the `GsonRequest` retry policy and was overlooked.

---

## Section 3: Summary Table

| ID | Severity | File | Line(s) | Category | Summary |
|---|---|---|---|---|---|
| A17-1 | CRITICAL | HttpClient.java | 92–102 | Dead code / Silent failure | `setCommonData` is empty; silently swallows exceptions; every request is affected |
| A17-2 | HIGH | ImagePostBackgroundTask.java | 15 | Deprecated API | `AsyncTask` deprecated in API 30; no suppression; lifecycle leak risk |
| A17-3 | HIGH | HttpClient.java | 40 | Leaky abstraction | `isSynchronous` is a raw public mutable field controlling dispatch |
| A17-4 | HIGH | HttpClient.java | 162–219 | Resource leak | `HttpURLConnection` and `InputStream` not closed in `finally` |
| A17-5 | HIGH | ImagePostRequest.java | 32–98, 117–178 | Resource leak | `HttpURLConnection` not closed in `finally` in both image-send methods |
| A17-6 | HIGH | ImagePostRequest.java | 169–172 | Silent failure | `SendMultipartHttpImage` catch block swallows all exceptions silently |
| A17-7 | MEDIUM | ImagePostBackgroundTask.java | 131–138 | Dead code | `readFileData` is never called; duplicates logic in `ImagePostRequest` |
| A17-8 | MEDIUM | HttpClient.java, ImagePostRequest.java | 53, 154–155 | Commented-out code | Two blocks of commented-out code left in production source |
| A17-9 | MEDIUM | ImagePostRequest.java | 107–115 | Leaky abstraction | `isMultiPart` uses hard-coded URL substring matching for format decision |
| A17-10 | MEDIUM | HttpClient.java | 110–118 | Logic error | `setHttpClient` called twice; push/add order differs between `sendRequest` overloads |
| A17-11 | MEDIUM | HttpClient.java | 54, 116, 144, 149 | Memory leak | `mWebRequestQueue` grows without bound; `GsonRequest` items never removed |
| A17-12 | MEDIUM | HttpClient.java | 162 | Leaky abstraction | `syncSendRequest` is package-private instead of `private` |
| A17-13 | MEDIUM | HttpClient.java | 52 | Dead code | `mCurrentRequestDesc` declared, never written or read |
| A17-14 | MEDIUM | HttpClient.java | 58 | Dead code | `mImageLoader` declared, never initialised or used |
| A17-15 | LOW | ImagePostRequest.java | 15 | Unused import | `import static android.R.attr.src` is never referenced |
| A17-16 | LOW | ImagePostRequest.java | 24, 32, 100, 117 | Style inconsistency | Method names use PascalCase instead of Java lowerCamelCase |
| A17-17 | LOW | HttpClient.java, ImagePostRequest.java | 173, 48 | Misleading comment | HTML entity `&amp;` in source code comments |
| A17-18 | LOW | HttpClient.java | 211–212 | Misleading comment | Comment says "max length of 500" but actual value is 1 MiB |
| A17-19 | LOW | ImagePostRequest.java | 37 | Protocol correctness | Weak static boundary `"*****"` risks collision with JPEG body content |
| A17-20 | INFO | HttpClient.java | 42 | Unused constant | `DEFAULT_TIMEOUT_MS` declared but not used locally |

**Total findings: 20** (1 CRITICAL, 5 HIGH, 7 MEDIUM, 6 LOW, 1 INFO)
