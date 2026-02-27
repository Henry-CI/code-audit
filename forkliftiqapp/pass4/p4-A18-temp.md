# Pass 4 – Code Quality Audit
**Agent:** A18
**Audit run:** 2026-02-26-01
**Files reviewed:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/JSONObjectParser.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/URLBuilder.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/UrlItem.java`

---

## Step 1: Reading Evidence

### File 1: JSONObjectParser.java

**Class:** `JSONObjectParser`
**Package:** `au.com.collectiveintelligence.fleetiq360.WebService`

**Fields:**
- `private JSONObject object` (line 8)

**Methods (exhaustive):**
| Line | Method |
|------|--------|
| 10 | `public JSONObjectParser(JSONObject object)` — constructor |
| 14 | `public String getString(String propertyName) throws JSONException` |
| 18 | `public int getInt(String propertyName) throws JSONException` |
| 22 | `public long getLong(String propertyName) throws JSONException` |
| 26 | `public Boolean getBoolean(String propertyName) throws JSONException` |
| 30 | `public JSONArray getJSONArray(String propertyName) throws JSONException` |

**Types/constants/enums/interfaces defined:** None beyond the class itself.

**Imports:** `org.json.JSONArray`, `org.json.JSONException`, `org.json.JSONObject`

---

### File 2: URLBuilder.java

**Class:** `URLBuilder`
**Package:** `au.com.collectiveintelligence.fleetiq360.WebService`

**Constants (fields):**
| Line | Declaration |
|------|-------------|
| 17 | `public final static int EQUIPMENT_FRONT = 1` |
| 18 | `public final static int EQUIPMENT_LEFT = 2` |
| 19 | `public final static int EQUIPMENT_RIGHT = 3` |
| 20 | `public final static int EQUIPMENT_BACK = 4` |
| 22 | `final static String baseUrl = BuildConfig.BASE_URL` |
| 24 | `final static String baseDataUrl = baseUrl+"/rest"` |
| 26 | `final static String baseUrlForPreStartHelp = "https://pandora.fleetiq360.com/pandora"` |

**Methods (exhaustive):**
| Line | Method |
|------|--------|
| 29 | `public static UrlItem urlSaveSession()` |
| 36 | `public static UrlItem urlAbortSession(int sessionId)` |
| 44 | `public static UrlItem urlUploadImpactImage(int impactId)` |
| 55 | `public static UrlItem urlUploadImpactSignature(int impactId)` |
| 66 | `public static UrlItem urlResendReport(int uid, int rid)` |
| 78 | `public static UrlItem urlSaveShockEvent()` |
| 86 | `public static UrlItem urlUpdateUser(int uid)` |
| 95 | `public static UrlItem urlDeleteCompany(int permissionId)` |
| 104 | `public static UrlItem urlGetUserDetail(int uid)` |
| 113 | `public static UrlItem urlGetEquipment()` → `urlAddEquipment()` |
| 122 | `public static UrlItem urlGetEmails(int uid)` |
| 132 | `public static UrlItem urlGetEquipmentStatsYearly(int uid)` |
| 143 | `public static UrlItem urlGetEquipmentStatsMonthly(int uid)` |
| 155 | `public static UrlItem urlGetEquipmentStatsWeekly(int uid)` |
| 167 | `public static UrlItem urlSaveImpactPhoto(int impid)` |
| 179 | `public static UrlItem urlGetReports(int uid)` |
| 189 | `public static UrlItem urlGetDriverStats(int uid)` |
| 199 | `public static UrlItem urlSaveService()` |
| 208 | `public static UrlItem urlSaveImpact()` |
| 217 | `public static UrlItem urlResetPassword()` |
| 226 | `public static UrlItem urlGetServiceRecord(int uid)` |
| 236 | `public static UrlItem urlGetDiagnosis(int eid)` |
| 244 | `public static UrlItem urlGetUniversity(int eid)` |
| 253 | `public static UrlItem urlGetFuelType(int mtype, int etype)` |
| 265 | `public static UrlItem urlGetEquipmentType(int mtype)` |
| 275 | `public static UrlItem urlGetManufacture()` |
| 284 | `public static UrlItem urlSaveLicense()` |
| 294 | `public static UrlItem urlUserRegister()` |
| 303 | `public static UrlItem urlSaveSingleGPSLocation()` |
| 312 | `public static UrlItem urlSaveMultipleGPSLocation()` |
| 322 | `public static UrlItem urlLogin()` |
| 331 | `public static UrlItem urlSetEmails()` |
| 340 | `public static UrlItem urlUploadUserPhoto(int userId)` |
| 352 | `public static UrlItem urlUploadEquipmentPhoto(int sid, int imageno)` |
| 366 | `public static UrlItem urlJoinCompany()` |
| 376 | `public static UrlItem urlSearchCompany(String search)` |
| 388 | `public static UrlItem urlGetCompanyList(int userId)` |
| 398 | `public static UrlItem urlGetEquipmentList(int userId)` |
| 408 | `public static UrlItem urlGetCompanyDriversList(int userId)` |
| 419 | `public static UrlItem urlGetPreStartQuestions(int equipmentId)` |
| 429 | `public static UrlItem urlSavePreStartResult()` |
| 439 | `public static UrlItem urlSessionStart()` |
| 448 | `public static UrlItem urlSessionEnd()` |
| 457 | `public static UrlItem urlGetToken()` |
| 462 | `public static String getUrl()` |

**Imports:** `android.net.Uri`, `com.android.volley.Request`, `au.com.collectiveintelligence.fleetiq360.BuildConfig`

---

### File 3: UrlItem.java

**Class:** `UrlItem`
**Package:** `au.com.collectiveintelligence.fleetiq360.WebService`

**Fields:**
| Line | Declaration |
|------|-------------|
| 9 | `public int method` |
| 10 | `public String url` |

**Methods (exhaustive):**
| Line | Method |
|------|--------|
| 12 | `public UrlItem(int httpMethod, String webUrl)` — constructor |

**Types/constants/enums/interfaces defined:** None.

---

## Step 2 & 3: Findings

---

### A18-1 — MEDIUM — URLBuilder: HTTP verb semantics wrong on `urlUploadImpactImage` and `urlUploadImpactSignature`

**File:** `URLBuilder.java`, lines 44–64

Both `urlUploadImpactImage` and `urlUploadImpactSignature` return `Request.Method.GET`, yet their names clearly indicate an upload (write) operation, and they are called from `IncidentPart2Fragment` in a context that sends binary data:

```java
// line 52
return new UrlItem(Request.Method.GET, builder.toString());  // urlUploadImpactImage

// line 63
return new UrlItem(Request.Method.GET, builder.toString());  // urlUploadImpactSignature
```

Uploading image data with GET violates HTTP semantics (GET must be idempotent and carry no body). The actual Volley request in `IncidentPart2Fragment` (lines 198 and 216) consumes the `UrlItem.method` field, so the wrong verb is transmitted to the server. Compare with the analogous `urlSaveImpactPhoto` (line 167) and `urlUploadEquipmentPhoto` (line 352) which correctly use `POST`/`PUT`. This is a protocol correctness bug, not merely a style issue.

---

### A18-2 — MEDIUM — URLBuilder: Misspelled URL path segment `"frequencey"` baked into three endpoints

**File:** `URLBuilder.java`, lines 138, 149, 161

The path segment `"frequencey"` (misspelling of "frequency") appears in all three equipment-stats endpoints:

```java
builder.appendPath("frequencey");   // urlGetEquipmentStatsYearly  (line 138)
builder.appendPath("frequencey");   // urlGetEquipmentStatsMonthly (line 149)
builder.appendPath("frequencey");   // urlGetEquipmentStatsWeekly  (line 161)
```

If the server path is correct (also `"frequencey"`), the calls succeed only because the server also has the typo. Any server-side correction would silently break all three callers. The misspelling should be extracted into a named constant so it can be corrected in one place, and aligned with the actual server path.

---

### A18-3 — MEDIUM — URLBuilder: Misspelled URL path segment `"fuletype"` in `urlGetFuelType`

**File:** `URLBuilder.java`, line 256

```java
builder.appendPath("fuletype");   // should be "fueltype"
```

Same category as A18-2. The path segment omits the letter `e`. Any server-side normalisation would expose this bug. No other callers use this path string directly, so it is silently load-bearing on a server-side typo.

---

### A18-4 — LOW — URLBuilder: Commented-out hardcoded IP addresses left in production code

**File:** `URLBuilder.java`, lines 171 and 355

Two commented-out `Uri.Builder` initialisations using a private LAN IP address remain in the file:

```java
// line 171, inside urlSaveImpactPhoto:
//        Uri.Builder builder = Uri.parse("https://192.168.1.7/fleetiq360ws/rest").buildUpon();

// line 355, inside urlUploadEquipmentPhoto:
//        Uri.Builder builder = Uri.parse("https://192.168.1.7/fleetiq360ws/rest").buildUpon();
```

These are development/debugging remnants. They expose a private server IP address and create noise. They should be deleted.

---

### A18-5 — LOW — URLBuilder: Dead constants `EQUIPMENT_FRONT/LEFT/RIGHT/BACK` with no usages

**File:** `URLBuilder.java`, lines 17–20

```java
public final static int EQUIPMENT_FRONT = 1;
public final static int EQUIPMENT_LEFT  = 2;
public final static int EQUIPMENT_RIGHT = 3;
public final static int EQUIPMENT_BACK  = 4;
```

A project-wide search finds zero usages of `URLBuilder.EQUIPMENT_FRONT`, `EQUIPMENT_LEFT`, `EQUIPMENT_RIGHT`, or `EQUIPMENT_BACK` anywhere outside this class declaration. The constants are `public` but never referenced, making them dead code. They are also semantically misplaced in a URL-building utility class; equipment image positions belong in a domain model or enum.

---

### A18-6 — LOW — URLBuilder: `getUrl()` is a trivial public wrapper over a package-private field

**File:** `URLBuilder.java`, lines 22–24, 462–464

```java
final static String baseDataUrl = baseUrl + "/rest";  // package-private

public static String getUrl() {
    return baseDataUrl;                                // public wrapper
}
```

`baseDataUrl` is package-private (no access modifier), while `getUrl()` exposes it publicly. The method adds no logic and provides no encapsulation benefit because the field could simply be `public static final`. This is inconsistent with how `baseUrl` and `baseUrlForPreStartHelp` are accessed directly inside the class without a wrapper. It also creates a false impression that `getUrl()` might perform dynamic logic (e.g., environment switching).

---

### A18-7 — LOW — URLBuilder: `urlSearchCompany` appends a spurious empty path segment

**File:** `URLBuilder.java`, lines 376–385

```java
public static UrlItem urlSearchCompany(String search) {
    Uri.Builder builder = Uri.parse(getUrl()).buildUpon();
    builder.appendPath("company");
    builder.appendPath("search");
    builder.appendPath(search);
    builder.appendPath("");           // line 382 — produces trailing slash
    return new UrlItem(Request.Method.GET, builder.toString());
}
```

`appendPath("")` causes `Uri.Builder` to append a trailing slash to the URL (e.g., `.../company/search/ACME//`). This is the only method in the class that does this. If the trailing slash matters to the server it should be documented; if not, this line is spurious noise.

---

### A18-8 — LOW — URLBuilder: Inconsistent `appendPath` call style across methods

**File:** `URLBuilder.java`, throughout

Two distinct styles are mixed freely throughout the file:

**Style A — chained calls (single statement):**
```java
// urlAbortSession, line 39
builder.appendPath("session").appendPath("abort").appendPath("session")
        .appendPath(String.valueOf(sessionId));
```

**Style B — separate statements per segment:**
```java
// urlUploadImpactImage, lines 47–51
builder.appendPath("impactimage");
builder.appendPath("impid");
builder.appendPath(String.valueOf(impactId));
builder.appendPath("type");
builder.appendPath("image");
```

Both styles appear within the same class with no rule governing which to use. The inconsistency makes the code harder to scan and review. A single style should be adopted throughout.

---

### A18-9 — LOW — URLBuilder: `urlGetToken` bypasses `getUrl()` and concatenates the path with string addition

**File:** `URLBuilder.java`, line 459

```java
public static UrlItem urlGetToken() {
    return (new UrlItem(Request.Method.POST, baseUrl + "/oauth/token"));
}
```

All other methods use `Uri.parse(getUrl()).buildUpon()` + `appendPath(...)`. `urlGetToken` directly concatenates a raw string `baseUrl + "/oauth/token"`. This bypasses proper URI encoding, is inconsistent with every other builder method, and would silently produce a malformed URL if `baseUrl` ever lacks or gains a trailing slash. The surrounding parentheses on the `new` expression are also unnecessary noise.

---

### A18-10 — LOW — UrlItem: Public mutable fields instead of encapsulated accessors

**File:** `UrlItem.java`, lines 9–10

```java
public int method;
public String url;
```

Both fields are `public` and non-`final`, meaning any caller can mutate the method or URL after construction. There are no setters that validate state. This is a leaky abstraction; the `UrlItem` is effectively a dumb struct. The fields should be `private final` with read-only getters. `url` being mutable `String` is lower risk but `method` mutation could silently send the wrong HTTP verb.

---

### A18-11 — INFO — JSONObjectParser: `getBoolean` returns boxed `Boolean`, inconsistent with `getInt`/`getLong` returning primitives

**File:** `JSONObjectParser.java`, line 26

```java
public Boolean getBoolean(String propertyName) throws JSONException { ... }
// vs.
public int  getInt(String propertyName) throws JSONException { ... }   // line 18
public long getLong(String propertyName) throws JSONException { ... }  // line 22
```

`getInt` and `getLong` return primitive types; `getBoolean` returns a boxed `Boolean`. This is a style inconsistency within the same class. The consequence is that callers of `getBoolean` receive a nullable reference where a `false` return (when the property is absent — see null-return logic in `getInt`/`getLong`) would instead be a `Boolean.FALSE` value, making the null-vs-false distinction impossible to detect. Using a primitive `boolean` would be consistent and remove the spurious boxing.

---

### A18-12 — INFO — URLBuilder: `baseUrl`, `baseDataUrl`, `baseUrlForPreStartHelp` lack `public`/`private` access modifiers

**File:** `URLBuilder.java`, lines 22–26

```java
final static String baseUrl = BuildConfig.BASE_URL;
final static String baseDataUrl = baseUrl + "/rest";
final static String baseUrlForPreStartHelp = "https://pandora.fleetiq360.com/pandora";
```

All three are package-private (default access). The `EQUIPMENT_*` constants on lines 17–20 are `public`. There is no consistent access-modifier policy for the fields of this class. `baseUrl` and `baseDataUrl` are effectively internal implementation details and should be `private`; `baseUrlForPreStartHelp` is also only used internally. The lack of explicit modifiers is ambiguous.

---

## Summary Table

| ID | Severity | File | Issue |
|----|----------|------|-------|
| A18-1 | MEDIUM | URLBuilder.java | `urlUploadImpactImage` and `urlUploadImpactSignature` use `GET` for upload operations |
| A18-2 | MEDIUM | URLBuilder.java | Misspelled URL path `"frequencey"` in three stats endpoints |
| A18-3 | MEDIUM | URLBuilder.java | Misspelled URL path `"fuletype"` in `urlGetFuelType` |
| A18-4 | LOW | URLBuilder.java | Commented-out hardcoded LAN IP in two methods |
| A18-5 | LOW | URLBuilder.java | Dead constants `EQUIPMENT_FRONT/LEFT/RIGHT/BACK` (zero usages) |
| A18-6 | LOW | URLBuilder.java | `getUrl()` is a trivial, unnecessary wrapper over a package-private field |
| A18-7 | LOW | URLBuilder.java | `urlSearchCompany` appends spurious empty path segment (trailing slash) |
| A18-8 | LOW | URLBuilder.java | Inconsistent `appendPath` chaining style across methods |
| A18-9 | LOW | URLBuilder.java | `urlGetToken` uses string concatenation instead of `Uri.Builder` |
| A18-10 | LOW | UrlItem.java | Public mutable fields expose internal state; no encapsulation |
| A18-11 | INFO | JSONObjectParser.java | `getBoolean` returns boxed `Boolean` while `getInt`/`getLong` return primitives |
| A18-12 | INFO | URLBuilder.java | Field access modifiers absent/inconsistent (`final static` without `public`/`private`) |
