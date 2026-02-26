# Pass 3 Documentation Audit — Agent A83
**Audit run:** 2026-02-26-01
**Files:** `json/HTTP.java`, `json/HTTPTokener.java`, `json/JSONArray.java`
**Note:** These are vendored/repackaged org.json library files (circa 2010-2012).

---

## 1. Reading Evidence

### 1.1 HTTP.java

**Class:** `HTTP` — line 34
**Package:** `com.json`

**Fields:**
| Name | Type | Modifier | Line |
|------|------|----------|------|
| `CRLF` | `String` | `public static final` | 37 |

**Methods:**
| Method | Modifier | Return Type | Line |
|--------|----------|-------------|------|
| `toJSONObject(String string)` | `public static` | `JSONObject` | 71 |
| `toString(JSONObject jo)` | `public static` | `String` | 127 |

---

### 1.2 HTTPTokener.java

**Class:** `HTTPTokener` — line 33 (extends `JSONTokener`)
**Package:** `com.json`

**Fields:** None declared (all inherited from `JSONTokener`)

**Methods:**
| Method | Modifier | Return Type | Line |
|--------|----------|-------------|------|
| `HTTPTokener(String string)` | `public` | — (constructor) | 39 |
| `nextToken()` | `public` | `String` | 49 |

---

### 1.3 JSONArray.java

**Class:** `JSONArray` — line 82
**Package:** `com.json`

**Fields:**
| Name | Type | Modifier | Line |
|------|------|----------|------|
| `myArrayList` | `ArrayList` | `private final` | 88 |

**Methods:**
| Method | Modifier | Return Type | Line |
|--------|----------|-------------|------|
| `JSONArray()` | `public` | — (constructor) | 94 |
| `JSONArray(JSONTokener x)` | `public` | — (constructor) | 103 |
| `JSONArray(String source)` | `public` | — (constructor) | 143 |
| `JSONArray(Collection collection)` | `public` | — (constructor) | 152 |
| `JSONArray(Object array)` | `public` | — (constructor) | 167 |
| `get(int index)` | `public` | `Object` | 188 |
| `getBoolean(int index)` | `public` | `boolean` | 206 |
| `getDouble(int index)` | `public` | `double` | 229 |
| `getInt(int index)` | `public` | `int` | 249 |
| `getJSONArray(int index)` | `public` | `JSONArray` | 269 |
| `getJSONObject(int index)` | `public` | `JSONObject` | 286 |
| `getLong(int index)` | `public` | `long` | 304 |
| `getString(int index)` | `public` | `String` | 323 |
| `isNull(int index)` | `public` | `boolean` | 337 |
| `join(String separator)` | `public` | `String` | 350 |
| `length()` | `public` | `int` | 369 |
| `opt(int index)` | `public` | `Object` | 380 |
| `optBoolean(int index)` | `public` | `boolean` | 395 |
| `optBoolean(int index, boolean defaultValue)` | `public` | `boolean` | 409 |
| `optDouble(int index)` | `public` | `double` | 426 |
| `optDouble(int index, double defaultValue)` | `public` | `double` | 440 |
| `optInt(int index)` | `public` | `int` | 457 |
| `optInt(int index, int defaultValue)` | `public` | `int` | 470 |
| `optJSONArray(int index)` | `public` | `JSONArray` | 485 |
| `optJSONObject(int index)` | `public` | `JSONObject` | 499 |
| `optLong(int index)` | `public` | `long` | 513 |
| `optLong(int index, long defaultValue)` | `public` | `long` | 526 |
| `optString(int index)` | `public` | `String` | 543 |
| `optString(int index, String defaultValue)` | `public` | `String` | 556 |
| `put(boolean value)` | `public` | `JSONArray` | 570 |
| `put(Collection value)` | `public` | `JSONArray` | 582 |
| `put(double value)` | `public` | `JSONArray` | 595 |
| `put(int value)` | `public` | `JSONArray` | 609 |
| `put(long value)` | `public` | `JSONArray` | 621 |
| `put(Map value)` | `public` | `JSONArray` | 633 |
| `put(Object value)` | `public` | `JSONArray` | 646 |
| `put(int index, boolean value)` | `public` | `JSONArray` | 661 |
| `put(int index, Collection value)` | `public` | `JSONArray` | 676 |
| `put(int index, double value)` | `public` | `JSONArray` | 692 |
| `put(int index, int value)` | `public` | `JSONArray` | 707 |
| `put(int index, long value)` | `public` | `JSONArray` | 722 |
| `put(int index, Map value)` | `public` | `JSONArray` | 737 |
| `put(int index, Object value)` | `public` | `JSONArray` | 755 |
| `remove(int index)` | `public` | `Object` | 778 |
| `toJSONObject(JSONArray names)` | `public` | `JSONObject` | 794 |
| `toString()` | `public` | `String` | 817 |
| `toString(int indentFactor)` | `public` | `String` | 837 |
| `write(Writer writer)` | `public` | `Writer` | 853 |
| `write(Writer writer, int indentFactor, int indent)` | package-private | `Writer` | 870 |

---

## 2. Findings

---

### A83-1 — MEDIUM — HTTP.java: Inaccurate @return tag in `toJSONObject`

**File:** `json/HTTP.java`
**Method:** `toJSONObject(String string)` — line 71
**Javadoc lines:** 39–70

**Issue:** The `@return` tag at line 67–68 reads:
```
@return A JSONObject containing the elements and attributes
of the XML string.
```
The phrase "of the XML string" is copied from an XML-related utility and is factually incorrect here. This method parses an **HTTP header string**, not an XML string. A reader relying on this Javadoc would be misled about the method's input domain.

**Actual behaviour (line 71–104):** Parses an HTTP request or response header string passed via `string`, extracts HTTP-specific fields (Method/Request-URI/HTTP-Version or HTTP-Version/Status-Code/Reason-Phrase) and all additional header name–value pairs, and returns them as a `JSONObject`.

**Severity rationale:** The wrong noun ("XML string" instead of "HTTP header string") contradicts the documented purpose of the entire class and could mislead a developer integrating this utility.

---

### A83-2 — LOW — HTTP.java: `@param` description for `toJSONObject` is incomplete

**File:** `json/HTTP.java`
**Method:** `toJSONObject(String string)` — line 71
**Javadoc line:** 66

**Issue:** The `@param string` tag says only "An HTTP header string." It does not specify that the string must begin with either a valid HTTP request line or a valid HTTP response line, nor that each subsequent header field must be in `Name: Value` format followed by a null terminator, nor what the expected line-ending format is. The body of the Javadoc comment (lines 42–65) gives good structural examples, but the `@param` tag itself adds no useful constraint description beyond the bare noun phrase.

This is a minor deficiency rather than an error; the omission does not mislead, but it leaves callers without a formal parameter contract in the tag itself.

---

### A83-3 — LOW — HTTP.java: `@throws JSONException` on `toJSONObject` has no condition description

**File:** `json/HTTP.java`
**Method:** `toJSONObject(String string)` — line 71
**Javadoc line:** 69

**Issue:** The tag `@throws JSONException` appears with no explanatory text at line 69. Callers cannot determine from the Javadoc under what conditions a `JSONException` is thrown (e.g. malformed token, unterminated string in `HTTPTokener.nextToken()`). The corresponding `toString` method (line 127) does provide a condition: "if the object does not contain enough information", setting a higher standard that `toJSONObject` fails to meet.

---

### A83-4 — LOW — HTTPTokener.java: `@throws` and `@return` tags are in non-standard order

**File:** `json/HTTPTokener.java`
**Method:** `nextToken()` — line 49
**Javadoc lines:** 44–48

**Issue:** The Javadoc for `nextToken()` lists `@throws JSONException` at line 47 before `@return A String.` at line 48. Standard Javadoc convention (and the order used throughout the org.json library itself, as seen in `HTTP.java` and `JSONArray.java`) places `@param` then `@return` then `@throws`. While this is a style issue and does not affect correctness, it deviates from the documented method's own sibling files and from Sun/Oracle Javadoc tag ordering guidelines.

---

### A83-5 — LOW — HTTPTokener.java: `@return` tag is insufficiently descriptive for `nextToken()`

**File:** `json/HTTPTokener.java`
**Method:** `nextToken()` — line 49
**Javadoc line:** 48

**Issue:** The `@return` tag states only "A String." This conveys no semantic content about what the string represents. Callers cannot determine from the tag alone whether the returned string is the raw token as read, a trimmed version, whether quotes are stripped from quoted tokens, etc.

Examining the implementation (lines 49–76): leading whitespace is consumed, and if the token is quoted (`'` or `"`), the quote delimiters are stripped and the inner content is returned; otherwise, the whitespace-terminated token is returned as-is. Neither the stripping of quote characters nor the whitespace-skipping behaviour is described by the `@return` tag or the body of the Javadoc.

---

### A83-6 — MEDIUM — JSONArray.java: `JSONArray(Object array)` constructor missing `@param` tag

**File:** `json/JSONArray.java`
**Constructor:** `JSONArray(Object array)` — line 167
**Javadoc lines:** 163–166

**Issue:** The Javadoc comment present is:
```java
/**
 * Construct a JSONArray from an array
 * @throws JSONException If not an array.
 */
```
There is no `@param array` tag. This is a public constructor; callers need to know that `array` must be a Java array object (checked via `array.getClass().isArray()`). The absence of a `@param` tag on a non-trivial constructor that documents a `@throws` condition is a documentation gap.

---

### A83-7 — LOW — JSONArray.java: `length()` Javadoc contains a typo ("included" vs "including")

**File:** `json/JSONArray.java`
**Method:** `length()` — line 369
**Javadoc lines:** 364–368

**Issue:** The description reads "Get the number of elements in the JSONArray, included nulls." The word "included" is grammatically incorrect; the intended word is "including". While the meaning is clear from context, this is a text error in a public API description.

---

### A83-8 — LOW — JSONArray.java: `optString(int index)` Javadoc contains a typo ("coverted" vs "converted")

**File:** `json/JSONArray.java`
**Method:** `optString(int index)` — line 543
**Javadoc lines:** 535–542

**Issue:** The description reads "If the value is not a string and is not null, then it is coverted to a string." The word "coverted" is a misspelling of "converted". Minor but present in a public API doc.

---

### A83-9 — LOW — JSONArray.java: `write(Writer writer)` is missing a `@param` tag for `writer`

**File:** `json/JSONArray.java`
**Method:** `write(Writer writer)` — line 853
**Javadoc lines:** 844–852

**Issue:** The Javadoc present is:
```java
/**
 * Write the contents of the JSONArray as JSON text to a writer. For
 * compactness, no whitespace is added.
 * <p>
 * Warning: This method assumes that the data structure is acyclical.
 *
 * @return The writer.
 * @throws JSONException
 */
```
There is no `@param writer` tag. The `writer` parameter is the destination `Writer` to which the JSON text is written — a non-trivial parameter for a public method. The companion overload `write(Writer writer, int indentFactor, int indent)` at line 870 (package-private) does document `@param indentFactor` and `@param indent`, making the omission of `@param writer` on the public method inconsistent.

Additionally, `@throws JSONException` has no condition text (same pattern as finding A83-3).

---

### A83-10 — LOW — JSONArray.java: `toString(int indentFactor)` has bare `@throws JSONException` with no condition text

**File:** `json/JSONArray.java`
**Method:** `toString(int indentFactor)` — line 837
**Javadoc lines:** 826–836

**Issue:** The `@throws JSONException` tag at line 835 has no explanatory text. Callers cannot determine from the Javadoc under what conditions a `JSONException` is thrown. The implementation delegates to `write(sw, indentFactor, 0)` which can throw on IO errors or invalid number values; neither condition is mentioned.

---

### A83-11 — LOW — JSONArray.java: `write(Writer writer)` `@throws JSONException` has no condition text

**File:** `json/JSONArray.java`
**Method:** `write(Writer writer)` — line 853
**Javadoc lines:** 844–852

**Issue:** Same pattern as A83-10. The `@throws JSONException` tag carries no condition text. (Tracked separately from A83-9 because it is a distinct tag deficiency on the same method.)

---

### A83-12 — LOW — JSONArray.java: `getJSONObject(int index)` uses vague `@param` description

**File:** `json/JSONArray.java`
**Method:** `getJSONObject(int index)` — line 286
**Javadoc lines:** 279–285

**Issue:** The `@param index` tag says only "subscript", with no description of valid range. All peer methods (`get`, `getBoolean`, `getDouble`, etc.) consistently document the range constraint as "The index must be between 0 and length() - 1." The single-word description "subscript" deviates from this established pattern and provides less information to the caller.

---

### A83-13 — LOW — JSONArray.java: `optDouble(int index, double defaultValue)` uses vague `@param index` description

**File:** `json/JSONArray.java`
**Method:** `optDouble(int index, double defaultValue)` — line 440
**Javadoc lines:** 431–439

**Issue:** The `@param index` tag says only "subscript". All other `optXxx(int index, T defaultValue)` overloads and the `getXxx` family describe the valid range explicitly. This single-word description is inconsistent with sibling methods in the same class.

---

### A83-14 — LOW — JSONArray.java: `optJSONArray(int index)` uses vague `@param index` description

**File:** `json/JSONArray.java`
**Method:** `optJSONArray(int index)` — line 485
**Javadoc lines:** 479–484

**Issue:** The `@param index` tag says only "subscript", consistent with findings A83-12 and A83-13.

---

## 3. Summary Table

| ID | File | Location | Severity | Issue |
|----|------|----------|----------|-------|
| A83-1 | HTTP.java | `toJSONObject` line 67–68 | MEDIUM | `@return` says "XML string" — should say "HTTP header string" |
| A83-2 | HTTP.java | `toJSONObject` line 66 | LOW | `@param string` tag has no constraint description |
| A83-3 | HTTP.java | `toJSONObject` line 69 | LOW | `@throws JSONException` has no condition text |
| A83-4 | HTTPTokener.java | `nextToken` lines 47–48 | LOW | `@throws` appears before `@return` (non-standard tag order) |
| A83-5 | HTTPTokener.java | `nextToken` line 48 | LOW | `@return` says only "A String." — quote-stripping and whitespace behaviour undocumented |
| A83-6 | JSONArray.java | `JSONArray(Object array)` line 167 | MEDIUM | No `@param array` tag on public constructor that also documents `@throws` |
| A83-7 | JSONArray.java | `length()` line 365 | LOW | Typo: "included nulls" should be "including nulls" |
| A83-8 | JSONArray.java | `optString(int index)` line 539 | LOW | Typo: "coverted" should be "converted" |
| A83-9 | JSONArray.java | `write(Writer writer)` line 853 | LOW | Missing `@param writer` tag on public method |
| A83-10 | JSONArray.java | `toString(int indentFactor)` line 835 | LOW | `@throws JSONException` has no condition text |
| A83-11 | JSONArray.java | `write(Writer writer)` line 852 | LOW | `@throws JSONException` has no condition text |
| A83-12 | JSONArray.java | `getJSONObject(int index)` line 283 | LOW | `@param index` says only "subscript", no range constraint |
| A83-13 | JSONArray.java | `optDouble(int index, double)` line 436 | LOW | `@param index` says only "subscript", no range constraint |
| A83-14 | JSONArray.java | `optJSONArray(int index)` line 482 | LOW | `@param index` says only "subscript", no range constraint |

**Total findings: 14** (2 MEDIUM, 12 LOW, 0 HIGH)

---

## 4. Notes on Scope

All three files are vendored copies of the org.json reference implementation (copyright JSON.org, circa 2002–2012). The documentation deficiencies listed above are inherited from the upstream library and were not introduced by the forkliftiqadmin project. No class-level Javadoc is missing: `HTTP` (line 29–33), `HTTPTokener` (line 27–32), and `JSONArray` (lines 36–81) all carry class-level `/** ... */` Javadoc blocks with `@author` and `@version` tags, so no LOW findings for absent class-level docs are raised.
