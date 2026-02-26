# Pass 2 Test Coverage Audit — A84
**Audit Run:** 2026-02-26-01
**Agent:** A84
**Files audited:**
1. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/json/JSONException.java`
2. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/json/JSONML.java`
3. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/json/JSONObject.java`

---

## Test Directory Search Results

Grep of `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/` for `JSONException`, `JSONML`, and `JSONObject` returned **no matches**. No test file in the entire test directory references any of these three classes, directly or indirectly (imports or usage patterns were also checked).

The only test files present in the test directory are:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

None of these test the JSON library classes.

---

## Reading Evidence

### 1. JSONException.java

**Class name:** `JSONException` (extends `Exception`)
**Package:** `com.json`
**Version stamp in Javadoc:** `2010-12-24`

**Fields:**
| Line | Field | Modifier |
|------|-------|----------|
| 9 | `serialVersionUID` | `private static final long` |
| 10 | `cause` | `private Throwable` |

**Methods:**
| Line | Method signature |
|------|-----------------|
| 16 | `JSONException(String message)` — constructor |
| 20 | `JSONException(Throwable cause)` — constructor |
| 25 | `getCause()` — returns `Throwable` |

---

### 2. JSONML.java

**Class name:** `JSONML`
**Package:** `com.json`
**Version stamp in Javadoc:** `2012-03-28`
**License header:** org.json "Good, not Evil" MIT-style license present (lines 3–25)

**Fields:** None (utility class; no instance fields)

**Methods:**
| Line | Method signature | Modifier |
|------|-----------------|----------|
| 49 | `parse(XMLTokener x, boolean arrayForm, JSONArray ja)` | `private static Object` |
| 250 | `toJSONArray(String string)` | `public static JSONArray` |
| 267 | `toJSONArray(XMLTokener x)` | `public static JSONArray` |
| 285 | `toJSONObject(XMLTokener x)` | `public static JSONObject` |
| 303 | `toJSONObject(String string)` | `public static JSONObject` |
| 314 | `toString(JSONArray ja)` | `public static String` |
| 396 | `toString(JSONObject jo)` | `public static String` |

---

### 3. JSONObject.java

**Class name:** `JSONObject`
**Package:** `com.json`
**Version stamp in Javadoc:** `2012-07-02`
**License header:** org.json "Good, not Evil" MIT-style license present (lines 3–25)

**Inner class:** `Null` (private static final, lines 102–130)
- Line 109: `clone()` — `protected final Object`
- Line 119: `equals(Object object)` — `public boolean`
- Line 127: `toString()` — `public String`

**Fields:**
| Line | Field | Modifier |
|------|-------|----------|
| 136 | `map` | `private final Map` |
| 145 | `NULL` | `public static final Object` |

**Constructors and Methods:**
| Line | Method signature | Modifier |
|------|-----------------|----------|
| 151 | `JSONObject()` | `public` |
| 165 | `JSONObject(JSONObject jo, String[] names)` | `public` |
| 182 | `JSONObject(JSONTokener x)` | `public` |
| 240 | `JSONObject(Map map)` | `public` |
| 274 | `JSONObject(Object bean)` | `public` |
| 291 | `JSONObject(Object object, String names[])` | `public` |
| 313 | `JSONObject(String source)` | `public` |
| 324 | `JSONObject(String baseName, Locale locale)` | `public` |
| 374 | `accumulate(String key, Object value)` | `public JSONObject` |
| 404 | `append(String key, Object value)` | `public JSONObject` |
| 425 | `doubleToString(double d)` | `public static String` |
| 453 | `get(String key)` | `public Object` |
| 474 | `getBoolean(String key)` | `public boolean` |
| 497 | `getDouble(String key)` | `public double` |
| 518 | `getInt(String key)` | `public int` |
| 539 | `getJSONArray(String key)` | `public JSONArray` |
| 557 | `getJSONObject(String key)` | `public JSONObject` |
| 575 | `getLong(String key)` | `public long` |
| 593 | `getNames(JSONObject jo)` | `public static String[]` |
| 614 | `getNames(Object object)` | `public static String[]` |
| 639 | `getString(String key)` | `public String` |
| 654 | `has(String key)` | `public boolean` |
| 668 | `increment(String key)` | `public JSONObject` |
| 694 | `isNull(String key)` | `public boolean` |
| 704 | `keys()` | `public Iterator` |
| 714 | `length()` | `public int` |
| 725 | `names()` | `public JSONArray` |
| 740 | `numberToString(Number number)` | `public static String` |
| 768 | `opt(String key)` | `public Object` |
| 781 | `optBoolean(String key)` | `public boolean` |
| 795 | `optBoolean(String key, boolean defaultValue)` | `public boolean` |
| 813 | `optDouble(String key)` | `public double` |
| 828 | `optDouble(String key, double defaultValue)` | `public double` |
| 846 | `optInt(String key)` | `public int` |
| 861 | `optInt(String key, int defaultValue)` | `public int` |
| 878 | `optJSONArray(String key)` | `public JSONArray` |
| 892 | `optJSONObject(String key)` | `public JSONObject` |
| 907 | `optLong(String key)` | `public long` |
| 922 | `optLong(String key, long defaultValue)` | `public long` |
| 939 | `optString(String key)` | `public String` |
| 952 | `optString(String key, String defaultValue)` | `public String` |
| 958 | `populateMap(Object bean)` | `private void` |
| 1014 | `put(String key, boolean value)` | `public JSONObject` |
| 1028 | `put(String key, Collection value)` | `public JSONObject` |
| 1042 | `put(String key, double value)` | `public JSONObject` |
| 1056 | `put(String key, int value)` | `public JSONObject` |
| 1070 | `put(String key, long value)` | `public JSONObject` |
| 1084 | `put(String key, Map value)` | `public JSONObject` |
| 1101 | `put(String key, Object value)` | `public JSONObject` |
| 1124 | `putOnce(String key, Object value)` | `public JSONObject` |
| 1145 | `putOpt(String key, Object value)` | `public JSONObject` |
| 1161 | `quote(String string)` | `public static String` |
| 1173 | `quote(String string, Writer w)` | `public static Writer` |
| 1236 | `remove(String key)` | `public Object` |
| 1246 | `stringToValue(String string)` | `public static Object` |
| 1298 | `testValidity(Object o)` | `public static void` |
| 1323 | `toJSONArray(JSONArray names)` | `public JSONArray` |
| 1346 | `toString()` | `public String` |
| 1367 | `toString(int indentFactor)` | `public String` |
| 1395 | `valueToString(Object value)` | `public static String` |
| 1442 | `wrap(Object object)` | `public static Object` |
| 1493 | `write(Writer writer)` | `public Writer` |
| 1498 | `writeValue(Writer writer, Object value, int indentFactor, int indent)` | `static final Writer` |
| 1531 | `indent(Writer writer, int indent)` | `static final void` |
| 1546 | `write(Writer writer, int indentFactor, int indent)` | `Writer` (package-private) |

---

## Findings

### A84-1 | Severity: HIGH | Zero test coverage for all three classes

No test file in `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/` references or exercises `JSONException`, `JSONML`, or `JSONObject` in any form. The grep search over the entire test source tree returned no matches. These three classes — constituting the core JSON parsing and serialization infrastructure used directly by `AdminUnitEditAction` and `AdminManufacturersAction` — are entirely untested.

---

### A84-2 | Severity: HIGH | JSONML is completely unused by the application and untested

`JSONML.java` provides XML-to-JSON and JSON-to-XML conversion via the JsonML transform. A full grep of application source files shows no `import com.json.JSONML` anywhere outside the `com.json` package itself. The class is vendored but dead code within this application. Its complex recursive `parse()` method (lines 49–235) handles multiple XML constructs and is therefore high-risk if it were ever activated. No test coverage exists.

---

### A84-3 | Severity: MEDIUM | JSONException shadows `Throwable.getCause()` with a broken implementation

`JSONException` declares a `private Throwable cause` field (line 10) and overrides `getCause()` (line 25) to return it. However, the `JSONException(String message)` constructor (line 16) does not set `this.cause`, leaving it `null` when that constructor is used and `getCause()` is called. The parent class `Exception` (via `Throwable`) also stores the cause internally. This shadow field is redundant for the `JSONException(Throwable cause)` constructor path and broken for the `JSONException(String message)` path. The `serialVersionUID` is set to the literal `0` (line 9), which is non-standard and prone to serialization conflicts if the class is ever evolved. No tests verify `getCause()` behavior.

---

### A84-4 | Severity: MEDIUM | JSONObject uses raw types throughout — type-safety gap unverifiable without tests

`JSONObject` was written against Java 1.4 generics-era conventions. The `map` field (line 136) is declared as `private final Map` (raw), and `Iterator` (lines 598, 704, 727, etc.) is also raw. Methods such as `keys()` (line 704) return a raw `Iterator`. The `put(String, Collection)` and `put(String, Map)` methods (lines 1028, 1084) accept raw `Collection` and `Map`. Because there are no unit tests, there is no regression safety net if this code is ever modernized, and ClassCastExceptions from incorrect type assumptions cannot be caught at build time.

---

### A84-5 | Severity: MEDIUM | Deprecated boxed constructor calls in JSONObject — silent correctness risk without tests

`JSONObject.put(String, double)` at line 1043 uses `new Double(value)`, `put(String, int)` at line 1057 uses `new Integer(value)`, and `put(String, long)` at line 1071 uses `new Long(value)`. The same pattern appears in `stringToValue()` at lines 1279–1281. These deprecated constructors have been removed in Java 17+. Because no tests exercise these code paths, a JDK upgrade would produce compile failures with no safety net. Application code in `AdminManufacturersAction` and `AdminUnitEditAction` calls these methods directly.

---

### A84-6 | Severity: MEDIUM | `optString` returns `""` (empty string) on null-stored keys — behavior untested and surprising

`optString(String key)` at line 939 delegates to `optString(key, "")`. The implementation at lines 952–955 returns `defaultValue` only when the stored value equals `JSONObject.NULL`. If the key is absent, `opt()` returns Java `null`, and `null.toString()` would be called — but this is pre-empted because `NULL.equals(null)` is true (the `Null.equals()` override at line 120 returns true when `object == null`). The subtle consequence is that a key that was explicitly stored as `JSONObject.NULL` and a key that simply does not exist both return `""`. This is a semantic ambiguity that is undocumented in any tests and could produce incorrect application behavior in callers such as `AdminManufacturersAction`.

---

### A84-7 | Severity: LOW | JSONML uses `StringBuffer` instead of `StringBuilder` — unnecessary synchronization overhead

`JSONML.toString(JSONArray)` at line 321 and `toString(JSONObject)` at line 397 both use `StringBuffer sb = new StringBuffer()`, which carries synchronized method overhead not needed in single-threaded local scope. This is a minor performance issue inherited from the original org.json codebase but is worth noting as the class is vendored and could be fixed. No tests benchmark or verify this code path.

---

### A84-8 | Severity: LOW | JSONObject.toString() silently returns `null` on serialization failure

`toString()` at lines 1346–1352 catches all exceptions and returns `null`. This means callers that assume `toString()` always returns a `String` (which is the general Java contract for `Object.toString()`) will receive a `null` reference. Callers in `AdminManufacturersAction` construct response bodies from JSONObject instances. No tests verify the failure-path behavior or document that callers must null-check the return value.

---

### A84-9 | Severity: LOW | No application-specific modifications detected in any of the three files

All three files appear to be verbatim copies of the upstream org.json library at the versions noted in their Javadoc (`JSONException` 2010-12-24, `JSONML` 2012-03-28, `JSONObject` 2012-07-02). The only application-level change is repackaging from `org.json` to `com.json`. There are no added methods, removed methods, overridden behaviors, or application-specific comments beyond the upstream source. This is informational: modifications to vendored libraries are a known risk vector, and here there are none to flag.

---

### A84-10 | Severity: INFO | Vendored library is significantly outdated (2012 vintage)

The newest file (`JSONObject`) carries a `@version 2012-07-02` stamp. The upstream org.json library has received numerous bug fixes, security hardening, and API improvements since 2012, including fixes to `JSONTokener` parsing edge cases and removal of deprecated boxed constructors. The vendored copy predates all of these. Because the library is inlined as source rather than managed as a Maven/Gradle dependency, no automated tooling (e.g., Dependabot, OWASP Dependency-Check) will flag it as outdated or vulnerable. The absence of any tests makes assessing behavioral divergence from upstream impossible.

---

## Summary Table

| ID | Severity | Class(es) | Description |
|----|----------|-----------|-------------|
| A84-1 | HIGH | All three | Zero test coverage across all three classes |
| A84-2 | HIGH | JSONML | Class is dead application code — never imported outside com.json package |
| A84-3 | MEDIUM | JSONException | `getCause()` returns `null` when `JSONException(String)` constructor used; `serialVersionUID = 0` is non-standard |
| A84-4 | MEDIUM | JSONObject | Pervasive raw types throughout; no regression safety for modernization |
| A84-5 | MEDIUM | JSONObject | Deprecated `new Double()`, `new Integer()`, `new Long()` constructors used; will fail on Java 17+ |
| A84-6 | MEDIUM | JSONObject | `optString()` returns same default for absent key and explicitly-null key — semantic ambiguity untested |
| A84-7 | LOW | JSONML | `StringBuffer` used in local-scope string building — unnecessary synchronization |
| A84-8 | LOW | JSONObject | `toString()` returns `null` on failure, violating `Object.toString()` contract; callers not tested |
| A84-9 | LOW | All three | No application-specific modifications found; repackaging only |
| A84-10 | INFO | All three | Vendored library is 2012-vintage; no dependency management tooling will detect it as outdated |
