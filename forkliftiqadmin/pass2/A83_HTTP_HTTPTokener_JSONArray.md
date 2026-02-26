# Pass 2 Test Coverage Audit — A83
**Audit run:** 2026-02-26-01
**Agent:** A83
**Files audited:**
1. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/json/HTTP.java`
2. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/json/HTTPTokener.java`
3. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/json/JSONArray.java`

**Test directory searched:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`

---

## Vendored Library Context

All three files belong to the `com.json` package, which is a local vendored copy of the `org.json` reference implementation (JSON.org). The package contains 15 source files total. The copyright header in each file reads "Copyright (c) 2002 JSON.org" with the characteristic "The Software shall be used for Good, not Evil." clause. Versions are stamped in Javadoc (`@version 2010-12-24` for HTTP/HTTPTokener; `@version 2012-04-20` for JSONArray). No Maven/Gradle dependency declaration for `org.json` is used; the source is bundled directly in the application source tree under `com.json` instead of the upstream `org.json` package.

---

## Reading Evidence

### 1. HTTP.java

**Class name:** `HTTP`

**Fields:**

| Field | Line | Visibility | Type |
|-------|------|------------|------|
| `CRLF` | 37 | `public static final` | `String` |

**Methods:**

| Method | Line | Signature |
|--------|------|-----------|
| `toJSONObject` | 71 | `public static JSONObject toJSONObject(String string) throws JSONException` |
| `toString` | 127 | `public static String toString(JSONObject jo) throws JSONException` |

---

### 2. HTTPTokener.java

**Class name:** `HTTPTokener`
**Extends:** `JSONTokener`

**Fields:** None declared (all state inherited from `JSONTokener`).

**Methods:**

| Method | Line | Signature |
|--------|------|-----------|
| `HTTPTokener` (constructor) | 39 | `public HTTPTokener(String string)` |
| `nextToken` | 49 | `public String nextToken() throws JSONException` |

---

### 3. JSONArray.java

**Class name:** `JSONArray`

**Fields:**

| Field | Line | Visibility | Type |
|-------|------|------------|------|
| `myArrayList` | 88 | `private final` | `ArrayList` (raw type) |

**Methods:**

| Method | Line | Signature |
|--------|------|-----------|
| `JSONArray()` | 94 | `public JSONArray()` |
| `JSONArray(JSONTokener)` | 103 | `public JSONArray(JSONTokener x) throws JSONException` |
| `JSONArray(String)` | 143 | `public JSONArray(String source) throws JSONException` |
| `JSONArray(Collection)` | 152 | `public JSONArray(Collection collection)` |
| `JSONArray(Object)` | 167 | `public JSONArray(Object array) throws JSONException` |
| `get` | 188 | `public Object get(int index) throws JSONException` |
| `getBoolean` | 206 | `public boolean getBoolean(int index) throws JSONException` |
| `getDouble` | 229 | `public double getDouble(int index) throws JSONException` |
| `getInt` | 249 | `public int getInt(int index) throws JSONException` |
| `getJSONArray` | 269 | `public JSONArray getJSONArray(int index) throws JSONException` |
| `getJSONObject` | 286 | `public JSONObject getJSONObject(int index) throws JSONException` |
| `getLong` | 304 | `public long getLong(int index) throws JSONException` |
| `getString` | 323 | `public String getString(int index) throws JSONException` |
| `isNull` | 337 | `public boolean isNull(int index)` |
| `join` | 350 | `public String join(String separator) throws JSONException` |
| `length` | 369 | `public int length()` |
| `opt` | 380 | `public Object opt(int index)` |
| `optBoolean(int)` | 395 | `public boolean optBoolean(int index)` |
| `optBoolean(int, boolean)` | 409 | `public boolean optBoolean(int index, boolean defaultValue)` |
| `optDouble(int)` | 426 | `public double optDouble(int index)` |
| `optDouble(int, double)` | 440 | `public double optDouble(int index, double defaultValue)` |
| `optInt(int)` | 457 | `public int optInt(int index)` |
| `optInt(int, int)` | 470 | `public int optInt(int index, int defaultValue)` |
| `optJSONArray` | 485 | `public JSONArray optJSONArray(int index)` |
| `optJSONObject` | 499 | `public JSONObject optJSONObject(int index)` |
| `optLong(int)` | 513 | `public long optLong(int index)` |
| `optLong(int, long)` | 526 | `public long optLong(int index, long defaultValue)` |
| `optString(int)` | 543 | `public String optString(int index)` |
| `optString(int, String)` | 556 | `public String optString(int index, String defaultValue)` |
| `put(boolean)` | 570 | `public JSONArray put(boolean value)` |
| `put(Collection)` | 582 | `public JSONArray put(Collection value)` |
| `put(double)` | 595 | `public JSONArray put(double value) throws JSONException` |
| `put(int)` | 609 | `public JSONArray put(int value)` |
| `put(long)` | 621 | `public JSONArray put(long value)` |
| `put(Map)` | 633 | `public JSONArray put(Map value)` |
| `put(Object)` | 646 | `public JSONArray put(Object value)` |
| `put(int, boolean)` | 661 | `public JSONArray put(int index, boolean value) throws JSONException` |
| `put(int, Collection)` | 676 | `public JSONArray put(int index, Collection value) throws JSONException` |
| `put(int, double)` | 692 | `public JSONArray put(int index, double value) throws JSONException` |
| `put(int, int)` | 707 | `public JSONArray put(int index, int value) throws JSONException` |
| `put(int, long)` | 722 | `public JSONArray put(int index, long value) throws JSONException` |
| `put(int, Map)` | 737 | `public JSONArray put(int index, Map value) throws JSONException` |
| `put(int, Object)` | 755 | `public JSONArray put(int index, Object value) throws JSONException` |
| `remove` | 778 | `public Object remove(int index)` |
| `toJSONObject` | 794 | `public JSONObject toJSONObject(JSONArray names) throws JSONException` |
| `toString()` | 817 | `public String toString()` |
| `toString(int)` | 837 | `public String toString(int indentFactor) throws JSONException` |
| `write(Writer)` | 853 | `public Writer write(Writer writer) throws JSONException` |
| `write(Writer, int, int)` | 870 | `Writer write(Writer writer, int indentFactor, int indent) throws JSONException` (package-private) |

---

## Test Coverage Search Results

Grep performed against all files under `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/` for each class name:

| Class | Test references found |
|-------|-----------------------|
| `HTTP` | None |
| `HTTPTokener` | None |
| `JSONArray` | None |

The test directory contains exactly four test files, all in the `com.calibration` and `com.util` packages:
- `UnitCalibrationImpactFilterTest.java`
- `UnitCalibrationTest.java`
- `UnitCalibratorTest.java`
- `ImpactUtilTest.java`

None of these reference `HTTP`, `HTTPTokener`, or `JSONArray`.

---

## Findings

### HTTP.java

**A83-1 | Severity: HIGH | Zero test coverage for HTTP class**
`HTTP` has no test class anywhere in the test source tree. Both static methods (`toJSONObject` and `toString`) are completely untested. The class is a request/response HTTP header parser; defects in it would silently corrupt HTTP header data processed by the application.

**A83-2 | Severity: MEDIUM | Vendored source uses outdated version (2010-12-24)**
`HTTP.java` carries `@version 2010-12-24`, making it approximately 14 years old at audit date. The upstream `org.json` library has received multiple bug-fix and security-relevant updates since then. Because the source is vendored rather than managed via a dependency, those fixes have not been incorporated.

**A83-3 | Severity: MEDIUM | Raw Iterator without generics in toString (line 128)**
`Iterator keys = jo.keys();` at line 128 uses a raw `Iterator` type. While not a runtime failure on its own, it suppresses compiler type-safety and is inconsistent with modern Java practices. This is carried over verbatim from the upstream 2010 version.

**A83-4 | Severity: LOW | StringBuffer used instead of StringBuilder in toString (line 130)**
`StringBuffer sb = new StringBuffer();` at line 130 incurs unnecessary synchronization overhead. `StringBuilder` is the correct replacement in single-threaded contexts. This is a vanilla library issue, not an application modification, but it has not been updated.

**A83-5 | Severity: INFO | No application-specific modifications detected in HTTP.java**
The file is a byte-for-byte match of the standard org.json `HTTP` class (2010-12-24 vintage) with the package declaration changed from `org.json` to `com.json`. No custom logic, added methods, or removed methods were observed.

---

### HTTPTokener.java

**A83-6 | Severity: HIGH | Zero test coverage for HTTPTokener class**
`HTTPTokener` has no test class or test reference in the entire test source tree. The `nextToken()` method contains a quoted-string parsing loop with an off-by-one-style early return: when a closing quote `q` is encountered at line 63-64, the method returns `sb.toString()` without appending the character that caused the exit, which is correct behaviour, but the interaction with the inherited `JSONTokener` state (position tracking, `syntaxError` path at line 61) is not verified.

**A83-7 | Severity: MEDIUM | Vendored source uses outdated version (2010-12-24)**
Same issue as A83-2. `HTTPTokener.java` is pinned to the 2010-12-24 org.json release with no mechanism to receive upstream patches.

**A83-8 | Severity: INFO | No application-specific modifications detected in HTTPTokener.java**
The file is the standard org.json `HTTPTokener` class with the package declaration changed from `org.json` to `com.json`. No custom logic or structural changes were found.

---

### JSONArray.java

**A83-9 | Severity: HIGH | Zero test coverage for JSONArray class**
`JSONArray` is the most feature-rich of the three files (49 methods across 5 constructors, 14 getters, 14 opt methods, 13 put overloads, remove, toJSONObject, toString overloads, and write overloads). None of these methods have a single test. `JSONArray` is a core data structure used throughout the application's JSON processing; untested behaviour here can lead to silent data corruption, unexpected exceptions swallowed by `opt*` methods, or incorrect serialization output.

**A83-10 | Severity: MEDIUM | Vendored source uses outdated version (2012-04-20)**
`JSONArray.java` carries `@version 2012-04-20`, approximately 14 years old at audit date. Upstream changes to `org.json` since 2012 include correctness fixes, generics adoption, and API additions that are absent here.

**A83-11 | Severity: MEDIUM | Raw types used pervasively throughout JSONArray (multiple lines)**
`ArrayList`, `Collection`, `Iterator`, and `Map` are all used as raw types (no generic type parameters). This disables compile-time type checking across the entire class. Affected lines include: 88 (`ArrayList myArrayList`), 152 (`Collection collection`), 155 (`Iterator iter`), 582 (`Collection value`), 633 (`Map value`), and all indexed put overloads using `Collection` and `Map`. This is an upstream library issue carried forward unchanged.

**A83-12 | Severity: MEDIUM | Deprecated constructor usage: `new Double(value)`, `new Integer(value)`, `new Long(value)`**
Lines 596 (`new Double(value)`), 610 (`new Integer(value)`), 611 (`new Integer(value)`  — via `put(int)`), 622 (`new Long(value)`), 693 (`new Double(value)`), 708 (`new Integer(value)`), 723 (`new Long(value)`) all use boxing constructors deprecated since Java 9 and removed in Java 16+ in terms of preferred usage. These are flagged by modern compilers. The application may be running on a JVM version that still tolerates them, but they represent a forward-compatibility risk.

**A83-13 | Severity: LOW | toString() silently returns null on serialization error (line 817-823)**
The `toString()` override catches all exceptions and returns `null` rather than throwing or returning a meaningful error indicator. Callers that concatenate the result without a null check will produce the literal string `"null"` in output. This is standard org.json behaviour but is a known defect and is not guarded by any test.

**A83-14 | Severity: LOW | write(Writer, int, int) is package-private (line 870)**
The `write(Writer writer, int indentFactor, int indent)` method has package-private visibility (no access modifier), while the public `toString(int)` and `write(Writer)` methods delegate to it. This is intentional in the upstream design but the inconsistency in visibility could be misleading to maintainers, and the method is not directly testable from outside the package.

**A83-15 | Severity: LOW | StringBuffer used instead of StringBuilder in join (line 352)**
Same unnecessary synchronization issue as A83-4 in `HTTP.toString`. `join()` at line 352 constructs a `StringBuffer` in a single-threaded context.

**A83-16 | Severity: INFO | No application-specific modifications detected in JSONArray.java**
The file matches the standard org.json `JSONArray` class at the 2012-04-20 version with the package declaration changed from `org.json` to `com.json`. No custom fields, methods, or altered logic were observed.

---

## Summary Table

| ID | Severity | Class | Description |
|----|----------|-------|-------------|
| A83-1 | HIGH | HTTP | Zero test coverage |
| A83-2 | MEDIUM | HTTP | Vendored at 2010-12-24; no upstream patches |
| A83-3 | MEDIUM | HTTP | Raw Iterator in toString |
| A83-4 | LOW | HTTP | StringBuffer instead of StringBuilder |
| A83-5 | INFO | HTTP | No app-specific modifications |
| A83-6 | HIGH | HTTPTokener | Zero test coverage |
| A83-7 | MEDIUM | HTTPTokener | Vendored at 2010-12-24; no upstream patches |
| A83-8 | INFO | HTTPTokener | No app-specific modifications |
| A83-9 | HIGH | JSONArray | Zero test coverage (49 methods) |
| A83-10 | MEDIUM | JSONArray | Vendored at 2012-04-20; no upstream patches |
| A83-11 | MEDIUM | JSONArray | Pervasive raw types |
| A83-12 | MEDIUM | JSONArray | Deprecated boxing constructors |
| A83-13 | LOW | JSONArray | toString() silently returns null on error |
| A83-14 | LOW | JSONArray | write(Writer,int,int) package-private visibility |
| A83-15 | LOW | JSONArray | StringBuffer instead of StringBuilder in join |
| A83-16 | INFO | JSONArray | No app-specific modifications |

**Total findings: 16**
**HIGH: 3 | MEDIUM: 6 | LOW: 4 | INFO: 3**
