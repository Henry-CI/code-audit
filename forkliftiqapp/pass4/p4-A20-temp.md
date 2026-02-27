# Pass 4 Code Quality Audit — Agent A20
**Audit run:** 2026-02-26-01
**Agent:** A20
**Date:** 2026-02-27

---

## Section 1: Reading Evidence

### File 1: `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/WebRequest.java`

**Class:** `WebRequest<T>` (extends `Request<T>` — Volley)

**Constants / Fields defined:**
| Name | Kind | Line |
|---|---|---|
| `WEBREQUEST_TIMEOUT_MS` | public static final int (30 000 ms) | 46 |
| `mHttpClient` | package-private field `HttpClient` | 47 |
| `mPriority` | private field `Priority` | 48 |
| `webClazz` | package-private final `Class<T>` | 49 |
| `webHeaders` | package-private final `Map<String,String>` | 50 |
| `msgId` | package-private `String` | 51 |
| `mUrlItem` | package-private `UrlItem` | 52 |
| `canceledByUser` | package-private `boolean` | 53 |
| `mRequestBody` | package-private `String` | 54 |
| `webListener` | package-private `WebListener<T>` | 55 |
| `cTimer` | package-private `CountDownTimer` | 56 |
| `isTimerRunning` | package-private `boolean` | 57 |
| `PROTOCOL_CHARSET` | static final `String` `"utf-8"` | 60 |
| `PROTOCOL_CONTENT_TYPE` | static final `String` | 63 |
| `isAuthMessage` | package-private `boolean` | 65 |

**Methods:**

| Method | Visibility | Line |
|---|---|---|
| `cancel()` | public (override) | 68 |
| `setPriority(Priority)` | public | 75 |
| `getPriority()` | public | 79 |
| `setHttpClient(HttpClient)` | public | 84 |
| `parseNetworkResponse(NetworkResponse)` | protected (override) | 89 |
| `getPostBodyContentType()` | public (override, @deprecated) | 111 |
| `getPostBody()` | public (override, @deprecated) | 119 |
| `getBodyContentType()` | public (override) | 124 |
| `getBody()` | public (override) | 129 |
| `WebRequest(UrlItem, WebServiceParameterPacket, Class<T>, WebListener<T>)` | public constructor | 143 |
| `getMsgId(String)` | package-private | 172 |
| `WebRequest(UrlItem, String, boolean, Class<T>, WebListener<T>)` | public constructor | 176 |
| `getHeaders()` | public (override) | 188 |
| `getMsgId()` | public | 192 |
| `onSucceed(T)` | public | 197 |
| `onConnectFailed(VolleyError)` | public | 211 |
| `removeRequest()` | package-private | 227 |
| `onRequestFailed(VolleyError)` | private | 233 |
| `onRequestFailed(WebResult)` | public | 239 |
| `ignoreResponse(T)` | package-private | 246 |
| `deliverResponse(T)` | protected (override) | 255 |
| `deliverError(VolleyError)` | public | 263 |
| `update()` | public | 274 |

**Annotations / Deprecated markers:**
- `getPostBodyContentType()` — marked `@deprecated` at line 108
- `getPostBody()` — marked `@deprecated` at line 116

---

### File 2: `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/WebResult.java`

**Class:** `WebResult`

**Fields:**
| Name | Kind | Line |
|---|---|---|
| `volleyError` | public `VolleyError` | 12 |

**Methods:**
| Method | Visibility | Line |
|---|---|---|
| `isBadGateway()` | public | 14 |
| `getStatusCode()` | public | 21 |

**Imports:**
- `javax.net.ssl.HttpsURLConnection` (line 5)

---

### File 3: `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/AnswerItem.java`

**Class:** `AnswerItem implements Serializable`

**Fields:**
| Name | Kind | Line |
|---|---|---|
| `question_id` | public `int` | 14 |
| `answer` | public `String` | 15 |

**Methods:**
| Method | Visibility | Line |
|---|---|---|
| `AnswerItem()` | public constructor | 17 |
| `AnswerItem(JSONObject)` | public constructor | 20 |

**Imports present:**
- `org.json.JSONException` (line 3) — used (throws declaration)
- `org.json.JSONObject` (line 4) — used
- `java.io.Serializable` (line 5) — used
- `org.json.JSONArray` (line 6) — NOT used
- `java.util.ArrayList` (line 7) — NOT used
- `java.math.BigDecimal` (line 8) — NOT used
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` (line 9) — wildcard, self-package
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` (line 10) — wildcard, unused

---

## Section 2: Code Quality Review

### WebRequest.java

**A20-1 — Overloaded `getMsgId()` name collision / dead overload**
Line 172 defines `String getMsgId(String url)` which takes a URL parameter and returns `url + System.currentTimeMillis()`. Line 192 defines `public String getMsgId()` which returns the stored `msgId` field. Both constructors call `getMsgId()` (no-arg) at lines 152 and 179, which returns `null` the first time it is called because `msgId` has not yet been assigned (the field initialises to `null`, and the no-arg accessor just returns `msgId`). The overload accepting `String url` is never called anywhere in the codebase. The result is that `msgId` is always stored as `null`, which propagates to Volley's request tagging in `HttpClient` at line 142.

**A20-2 — `CountDownTimer` started in first constructor but not in second constructor**
The first constructor (`WebRequest(UrlItem, WebServiceParameterPacket, Class<T>, WebListener<T>)`) at lines 157–167 starts `cTimer` and sets `isTimerRunning = true`. The second constructor (`WebRequest(UrlItem, String, boolean, Class<T>, WebListener<T>)`) at lines 176–185 does not start the timer or set `isTimerRunning`. The `onSucceed()` and `onConnectFailed()` methods at lines 198 and 212 guard timer cancellation with `if (true == isTimerRunning)`. Requests created via the second constructor will never start the timer, so the 30-second application-level timeout is silently absent for auth-message flows. The `if (true == boolVar)` Yoda-condition style is also a style inconsistency compared with the rest of the codebase.

**A20-3 — `update()` switch body is entirely dead**
`update()` at lines 274–283 contains a `switch` on `mUrlItem.method` with `case Method.POST` and `case Method.GET`, both with empty bodies (lines 276–281). The switch has no effect and should either be deleted or implemented. This appears to be placeholder code committed in an incomplete state.

**A20-4 — `parseNetworkResponse` does not parse the response body**
`WebRequest.parseNetworkResponse()` at line 91 constructs `T` via `webClazz.newInstance()` (default no-arg constructor) and ignores `networkResponse` entirely — the raw body bytes are never read. The subclass `GsonRequest` overrides this correctly. However, `WebRequest` itself is instantiated directly in callers that expect a populated result. Any direct `WebRequest` usage will silently return an empty/default object, which is a logic error that will not produce an exception and will be very difficult to diagnose.

**A20-5 — `getPostBodyContentType()` and `getPostBody()` are deprecated Volley overrides retained in production code**
Lines 110–121 override two methods marked `@deprecated` by Volley (`getPostBodyContentType()` and `getPostBody()`). The Javadoc comment on each says "Use `getBodyContentType()`" and "Use `getBody()`" respectively, and the implementations delegate to those modern methods. Retaining overrides of deprecated API in the final class causes build warnings and signals the class was written against an old Volley API and not fully updated.

**A20-6 — `PROTOCOL_CONTENT_TYPE` uses `String.format` with a redundant `Object[]` array**
Line 63: `String.format("application/json; charset=%s", new Object[]{"utf-8"})`. The `Object[]` wrapper is unnecessary; `String.format` is varargs. More importantly, the charset is also hardcoded in `PROTOCOL_CHARSET` on line 60 — the two constants are not linked, so a change to `PROTOCOL_CHARSET` would not propagate to `PROTOCOL_CONTENT_TYPE`.

**A20-7 — Inconsistent access modifiers across related fields**
All of the following fields perform the same structural role (they are data needed by the request), yet they have no consistent access modifier policy:
- `webClazz`, `webHeaders`, `msgId`, `mUrlItem`, `canceledByUser`, `mRequestBody`, `webListener`, `cTimer`, `isTimerRunning`, `isAuthMessage` are all package-private (no modifier).
- `mHttpClient` is package-private.
- `mPriority` is `private`.
No consistent convention explains why `mPriority` is `private` while the rest are package-private. Fields accessed by the subclass `GsonRequest` in the same package (e.g., `webClazz`, `mUrlItem`, `webHeaders`, `isAuthMessage`, `mRequestBody`, `webListener`) need package-private access, but `mPriority` appears to have no such access need from outside either.

**A20-8 — `onConnectFailed` passes `null` to `onRequestFailed(VolleyError)` via CountDownTimer**
`CountDownTimer.onFinish()` at line 165 calls `onRequestFailed((VolleyError) null)`. `onRequestFailed(VolleyError)` at lines 233–237 constructs a `WebResult` with `webResult.volleyError = null` and passes it to `onRequestFailed(WebResult)`. This means callers in `onFailed()` receive a `WebResult` where `volleyError` is `null`. `WebResult.isBadGateway()` and `getStatusCode()` both guard against null, so they will silently return `false`/`0` for a timeout. There is no way for a listener to distinguish a network timeout from a non-network failure. This is a design defect rather than a crash risk.

---

### WebResult.java

**A20-9 — `HttpsURLConnection` imported for HTTP status code constant; wrong class**
Line 5: `import javax.net.ssl.HttpsURLConnection`. The constant used is `HttpsURLConnection.HTTP_BAD_GATEWAY` (line 15). `HTTP_BAD_GATEWAY` (502) is inherited from `java.net.HttpURLConnection`, which is the conventional class to import for HTTP status constants. Using `HttpsURLConnection` for a plain HTTP status constant is misleading; it implies HTTPS-specific behaviour when none is present. `WebRequest.java` uses `java.net.HttpURLConnection` for its `HTTP_UNAUTHORIZED` check (line 218), creating an inconsistency across the two files in the same package.

**A20-10 — `volleyError` is a public mutable field**
`WebResult.volleyError` at line 12 is declared `public`. This is a leaky abstraction: callers can directly read and write the internal Volley error object, coupling every error-handling site to Volley's API. The class provides no encapsulation. If Volley is ever replaced, every caller touching `webResult.volleyError` must be updated. `WebRequest.onRequestFailed(VolleyError)` writes to this field directly at line 235 (`webResult.volleyError = volleyError`).

---

### AnswerItem.java

**A20-11 — Three unused imports**
Lines 6–8:
- `import org.json.JSONArray;` — no `JSONArray` usage in this file.
- `import java.util.ArrayList;` — no `ArrayList` usage in this file.
- `import java.math.BigDecimal;` — no `BigDecimal` usage in this file.

These appear to be copy-paste artifacts from a code-generation template (the same pattern, including the same three unused imports, appears in `SavePreStartItem.java`).

**A20-12 — Wildcard self-import and unused wildcard import of results package**
Line 9: `import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*;` — this is a wildcard import of the class's own package. In Java this is entirely redundant; classes in the same package are always visible without an import.
Line 10: `import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*;` — nothing from the `results` sub-package is referenced anywhere in `AnswerItem`. This is dead import code. Both lines are template noise.

**A20-13 — Public mutable fields violate encapsulation**
`question_id` (line 14) and `answer` (line 15) are both `public` with no getter/setter. This makes `AnswerItem` a plain data bag with no control over mutation. While acceptable as a simple DTO, the class implements `Serializable` (implying persistence or IPC use) and the fields are written to by both JSON deserialization and directly by UI adapter code (`PrestartCheckListAdapter.java`). Having a `Serializable` class with raw public fields and no `serialVersionUID` is a build warning and a latent serialization-compatibility hazard (see A20-14).

**A20-14 — `Serializable` class missing `serialVersionUID`**
`AnswerItem implements Serializable` at line 12 declares no `serialVersionUID`. The Java serialization specification requires a `serialVersionUID` to be explicitly declared to ensure stable deserialization across class changes. Without it, the JVM auto-generates one based on class structure; any refactoring (adding/removing fields or methods) will silently break deserialization of previously stored instances. This will produce a compiler/IDE warning (`serializable class has no definition of serialVersionUID`). The same template-generated issue exists in `SavePreStartItem.java`.

---

## Section 3: Classified Findings

| ID | Severity | File | Line(s) | Description |
|---|---|---|---|---|
| A20-1 | HIGH | WebRequest.java | 152, 172, 179, 192 | `getMsgId(String)` overload is dead (never called); no-arg `getMsgId()` returns `null` because `msgId` is assigned from the no-arg call before `msgId` is set — request tagging is always `null`. |
| A20-2 | HIGH | WebRequest.java | 143–167, 176–185 | `CountDownTimer` started only in first constructor; second constructor (used for auth and by `GsonRequest`) silently omits the application-level timeout. |
| A20-3 | MEDIUM | WebRequest.java | 275–281 | `update()` switch is entirely dead code — both `case POST` and `case GET` bodies are empty; no behavior is implemented. |
| A20-4 | HIGH | WebRequest.java | 89–105 | `parseNetworkResponse` ignores `networkResponse` body, always returning an empty default-constructed `T`; any non-`GsonRequest` usage of `WebRequest` silently returns blank data. |
| A20-5 | LOW | WebRequest.java | 108–121 | Two deprecated Volley method overrides retained in production code, generating build warnings. |
| A20-6 | LOW | WebRequest.java | 60, 63 | `PROTOCOL_CONTENT_TYPE` uses `String.format` with a redundant `new Object[]` wrapper, and its hardcoded charset is not linked to `PROTOCOL_CHARSET`, creating a change-drift risk. |
| A20-7 | LOW | WebRequest.java | 47–65 | Inconsistent access modifiers across fields of identical structural role (`mPriority` is `private`; all others are package-private) without documented rationale. |
| A20-8 | MEDIUM | WebRequest.java | 163–166, 233–237 | Timer-triggered timeout passes `null` `VolleyError` into `WebResult`; listeners cannot distinguish timeout from other failures; `isBadGateway()`/`getStatusCode()` silently return default values. |
| A20-9 | LOW | WebResult.java | 5, 15 | Wrong import used for HTTP status constant: `javax.net.ssl.HttpsURLConnection` instead of `java.net.HttpURLConnection`; inconsistent with `WebRequest.java` which uses `HttpURLConnection`. |
| A20-10 | MEDIUM | WebResult.java | 12 | `volleyError` is a public mutable field, exposing Volley internals through the public API and coupling all error-handling callers to the Volley library. |
| A20-11 | LOW | AnswerItem.java | 6–8 | Three unused imports: `JSONArray`, `ArrayList`, `BigDecimal` — copy-paste template noise. |
| A20-12 | LOW | AnswerItem.java | 9–10 | Wildcard import of own package (redundant in Java) and wildcard import of `results.*` (nothing from that package is used). |
| A20-13 | LOW | AnswerItem.java | 14–15 | Public mutable fields on a `Serializable` class used as a DTO; no encapsulation for a class shared across UI adapter and network layers. |
| A20-14 | MEDIUM | AnswerItem.java | 12 | `Serializable` class lacks `serialVersionUID`; auto-generated UID will change on any structural refactor, silently breaking deserialization of persisted instances. |

---

## Section 4: Summary Statistics

| Severity | Count |
|---|---|
| CRITICAL | 0 |
| HIGH | 3 (A20-1, A20-2, A20-4) |
| MEDIUM | 4 (A20-3, A20-8, A20-10, A20-14) |
| LOW | 7 (A20-5, A20-6, A20-7, A20-9, A20-11, A20-12, A20-13) |
| **Total** | **14** |
