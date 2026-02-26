# Pass 3 Documentation Audit — Agent A84
**Audit run:** 2026-02-26-01
**Files:** json/JSONException.java · json/JSONML.java · json/JSONObject.java
**Note:** All three files are vendored/repackaged org.json library sources (circa 2010–2012).

---

## Reading Evidence

### JSONException.java

**Class:** `JSONException` — line 8 (extends `Exception`)

**Fields:**
| Name | Type | Line |
|------|------|------|
| `serialVersionUID` | `private static final long` | 9 |
| `cause` | `private Throwable` | 10 |

**Methods:**
| Method | Visibility | Line |
|--------|-----------|------|
| `JSONException(String message)` | public | 16 |
| `JSONException(Throwable cause)` | public | 20 |
| `getCause()` | public | 25 |

---

### JSONML.java

**Class:** `JSONML` — line 38 (utility class, all-static)

**Fields:** none (no instance or static fields)

**Methods:**
| Method | Visibility | Line |
|--------|-----------|------|
| `parse(XMLTokener x, boolean arrayForm, JSONArray ja)` | private static | 49 |
| `toJSONArray(String string)` | public static | 250 |
| `toJSONArray(XMLTokener x)` | public static | 267 |
| `toJSONObject(XMLTokener x)` | public static | 285 |
| `toJSONObject(String string)` | public static | 303 |
| `toString(JSONArray ja)` | public static | 314 |
| `toString(JSONObject jo)` | public static | 396 |

---

### JSONObject.java

**Class:** `JSONObject` — line 95

**Inner class:** `Null` (private static final) — line 102

**Fields:**
| Name | Type | Line |
|------|------|------|
| `map` | `private final Map` | 136 |
| `NULL` | `public static final Object` | 145 |

**Methods (public, unless noted):**
| Method | Visibility | Line |
|--------|-----------|------|
| `JSONObject()` | public | 151 |
| `JSONObject(JSONObject jo, String[] names)` | public | 165 |
| `JSONObject(JSONTokener x)` | public | 182 |
| `JSONObject(Map map)` | public | 240 |
| `JSONObject(Object bean)` | public | 274 |
| `JSONObject(Object object, String names[])` | public | 291 |
| `JSONObject(String source)` | public | 313 |
| `JSONObject(String baseName, Locale locale)` | public | 324 |
| `accumulate(String key, Object value)` | public | 374 |
| `append(String key, Object value)` | public | 404 |
| `doubleToString(double d)` | public static | 425 |
| `get(String key)` | public | 453 |
| `getBoolean(String key)` | public | 474 |
| `getDouble(String key)` | public | 497 |
| `getInt(String key)` | public | 518 |
| `getJSONArray(String key)` | public | 539 |
| `getJSONObject(String key)` | public | 557 |
| `getLong(String key)` | public | 575 |
| `getNames(JSONObject jo)` | public static | 593 |
| `getNames(Object object)` | public static | 614 |
| `getString(String key)` | public | 639 |
| `has(String key)` | public | 654 |
| `increment(String key)` | public | 668 |
| `isNull(String key)` | public | 694 |
| `keys()` | public | 704 |
| `length()` | public | 714 |
| `names()` | public | 725 |
| `numberToString(Number number)` | public static | 740 |
| `opt(String key)` | public | 768 |
| `optBoolean(String key)` | public | 781 |
| `optBoolean(String key, boolean defaultValue)` | public | 795 |
| `optDouble(String key)` | public | 813 |
| `optDouble(String key, double defaultValue)` | public | 828 |
| `optInt(String key)` | public | 846 |
| `optInt(String key, int defaultValue)` | public | 861 |
| `optJSONArray(String key)` | public | 878 |
| `optJSONObject(String key)` | public | 892 |
| `optLong(String key)` | public | 907 |
| `optLong(String key, long defaultValue)` | public | 922 |
| `optString(String key)` | public | 939 |
| `optString(String key, String defaultValue)` | public | 952 |
| `populateMap(Object bean)` | private | 958 |
| `put(String key, boolean value)` | public | 1014 |
| `put(String key, Collection value)` | public | 1028 |
| `put(String key, double value)` | public | 1042 |
| `put(String key, int value)` | public | 1056 |
| `put(String key, long value)` | public | 1070 |
| `put(String key, Map value)` | public | 1084 |
| `put(String key, Object value)` | public | 1101 |
| `putOnce(String key, Object value)` | public | 1124 |
| `putOpt(String key, Object value)` | public | 1145 |
| `quote(String string)` | public static | 1161 |
| `quote(String string, Writer w)` | public static | 1173 |
| `remove(String key)` | public | 1236 |
| `stringToValue(String string)` | public static | 1246 |
| `testValidity(Object o)` | public static | 1298 |
| `toJSONArray(JSONArray names)` | public | 1323 |
| `toString()` | public | 1346 |
| `toString(int indentFactor)` | public | 1367 |
| `valueToString(Object value)` | public static | 1395 |
| `wrap(Object object)` | public static | 1442 |
| `write(Writer writer)` | public | 1493 |
| `writeValue(Writer writer, Object value, int indentFactor, int indent)` | static final (pkg-private) | 1498 |
| `indent(Writer writer, int indent)` | static final (pkg-private) | 1531 |
| `write(Writer writer, int indentFactor, int indent)` | pkg-private | 1546 |

---

## Findings

### JSONException.java

---

**A84-1** — MEDIUM — Undocumented non-trivial public method: `JSONException(Throwable cause)` (line 20)

The constructor at line 20 has no Javadoc whatsoever. It is non-trivial: it both calls `super(cause.getMessage())` (extracting the message from the cause rather than storing it directly via `super(String, Throwable)`) and assigns to `this.cause` (shadowing `Exception.cause` with a local field instead of using the standard JDK facility). This design quirk is invisible to callers without documentation.

```java
// line 20 — no Javadoc
public JSONException(Throwable cause) {
    super(cause.getMessage());
    this.cause = cause;
}
```

---

**A84-2** — MEDIUM — Undocumented non-trivial public method: `getCause()` (line 25)

No Javadoc on the `getCause()` override. This is non-trivial because it overrides `Throwable.getCause()` to return the locally stored `this.cause` field (which was populated only by the `Throwable` constructor). A caller relying on the standard JDK `getCause()` contract (which would work via the `Throwable(Throwable)` super-constructor chain) needs to know about this local override.

```java
// line 25 — no Javadoc
public Throwable getCause() {
    return this.cause;
}
```

---

**A84-3** — HIGH — Inaccurate / dangerously wrong comment on `getCause()` (line 25, via `cause` field at line 10)

The `cause` field (line 10) is a private shadow of `Throwable.cause`. The `JSONException(Throwable cause)` constructor stores the throwable in the local `cause` field and calls `super(cause.getMessage())` — NOT `super(cause)` — meaning `Throwable.getCause()` (the JDK implementation) would return `null` for instances created via this constructor, while this class's `getCause()` override returns the locally stored value. This silent divergence from standard exception semantics is undocumented and constitutes a contract violation: code that uses `Throwable.getCause()` through a polymorphic reference (`Throwable t = new JSONException(ex)`) will get a different result than code using `JSONException.getCause()` directly, which is dangerously misleading. There is no comment anywhere warning of this behaviour.

---

### JSONML.java

**Class-level Javadoc:** Present (lines 30–37). Adequate.

---

**A84-4** — LOW — Missing `@param` for `indentFactor` on `toString(JSONArray)` Javadoc

Not applicable here — no `indentFactor` in `toString(JSONArray)`. However, review of the `@throws JSONException` style used throughout JSONML is noted: all public method Javadoc uses `@throws JSONException` with no descriptive text (e.g., line 47: `@throws JSONException`). This is technically present but provides no information about what conditions cause the exception.

---

**A84-5** — LOW — Bare `@throws JSONException` with no description on all public JSONML methods

All six public methods in JSONML carry `@throws JSONException` in their Javadoc with no explanatory text (lines 47, 248, 265, 281, 300, 312). While the tag is present, it conveys no information to the caller about what error conditions trigger the exception. Affected methods:
- `parse(...)` — line 47
- `toJSONArray(String)` — line 248
- `toJSONArray(XMLTokener)` — line 265
- `toJSONObject(XMLTokener)` — line 281
- `toJSONObject(String)` — line 300
- `toString(JSONArray)` — line 312

---

**A84-6** — MEDIUM — Inaccurate Javadoc on `toJSONObject(XMLTokener x)` (line 285)

The Javadoc block (lines 272–284) for `toJSONObject(XMLTokener x)` contains a blank line mid-paragraph (between lines 278 and 280), breaking the sentence "...and JsonML JSONObjects." from the sentence beginning "Comments, prologs...". This is a copy-paste artefact from the `toJSONObject(String)` overload immediately below. More importantly, the `@param` tag reads `@param x An XMLTokener of the XML source text.` — the phrase "of the XML source text" is inaccurate because the XMLTokener parameter wraps an already-constructed tokenizer, not necessarily a raw source text string. The corresponding `toJSONObject(String string)` overload more correctly documents the string parameter. This is low-severity in isolation but indicates inconsistency between the two sibling overloads.

---

**A84-7** — MEDIUM — `toString(JSONObject jo)` fallback behaviour undocumented (line 396)

The Javadoc for `toString(JSONObject jo)` (lines 387–395) states "The JSONObject must contain a 'tagName' property." but does not document what happens when it does not. The implementation at lines 409–412 silently falls back to `XML.escape(jo.toString())` rather than throwing an exception. A caller reading only the Javadoc would expect an error; instead they receive escaped JSON. This discrepancy between the stated precondition ("must contain") and the actual behaviour (silent fallback) is inaccurate documentation.

```java
// line 409-412
tagName = jo.optString("tagName");
if (tagName == null) {
    return XML.escape(jo.toString());  // silent fallback — undocumented
}
```

---

### JSONObject.java

**Class-level Javadoc:** Present (lines 41–94). Thorough and accurate.

---

**A84-8** — LOW — Missing `@param` on `getNames(JSONObject jo)` (line 593)

The Javadoc (lines 588–592) documents `@return` but omits `@param jo`.

```java
/**
 * Get an array of field names from a JSONObject.
 *
 * @return An array of field names, or null if there are no names.
 */
public static String[] getNames(JSONObject jo) {
```

---

**A84-9** — LOW — Missing `@param` on `getNames(Object object)` (line 614)

The Javadoc (lines 609–613) documents `@return` but omits `@param object`.

```java
/**
 * Get an array of field names from an Object.
 *
 * @return An array of field names, or null if there are no names.
 */
public static String[] getNames(Object object) {
```

---

**A84-10** — LOW — Missing `@param` and `@return` on `putOnce(String key, Object value)` (line 1124)

The Javadoc (lines 1115–1123) mentions `@param key` and `@param value` in descriptive text inline but has no formal `@param` tags. The `@return` tag is present but reads `@return his.` — a typo for `@return this.`

```java
/**
 * ...
 * @param key
 * @param value
 * @return his.        <-- typo: should be "this."
 * @throws JSONException if the key is a duplicate
 */
public JSONObject putOnce(String key, Object value) throws JSONException {
```

The `@param key` and `@param value` tags exist at lines 1119–1120 but have no descriptive text. Per standard Javadoc norms this is LOW; the typo in `@return` is also LOW.

---

**A84-11** — MEDIUM — Undocumented public method: `quote(String string, Writer w)` (line 1173)

The overload `public static Writer quote(String string, Writer w)` at line 1173 has no Javadoc at all. It is non-trivial: it writes a properly JSON-escaped, double-quoted string to a `Writer` and returns that writer. The companion `quote(String string)` overload at line 1161 is documented. This method is public and part of the API surface.

```java
// line 1173 — no Javadoc
public static Writer quote(String string, Writer w) throws IOException {
```

---

**A84-12** — MEDIUM — Undocumented public method: `write(Writer writer)` (line 1493)

The method `public Writer write(Writer writer)` at line 1493 does have a Javadoc block (lines 1484–1492), but that block contains no `@param writer` tag and no `@return` description. The comment body ("Write the contents of the JSONObject as JSON text to a writer. For compactness, no whitespace is added.") is adequate prose, but `@param` and `@return` are both absent. It also uses `@return The writer.` only in the package-private overload at line 1537, not here.

Correction: re-reading lines 1484–1492:
```
/**
 * Write the contents of the JSONObject as JSON text to a writer.
 * For compactness, no whitespace is added.
 * <p>
 * Warning: This method assumes that the data structure is acyclical.
 *
 * @return The writer.
 * @throws JSONException
 */
```
`@return` is present but `@param writer` is missing. `@throws JSONException` has no description. Severity: LOW (missing @param) + LOW (bare @throws).

---

**A84-13** — LOW — Missing `@param writer` on `write(Writer writer)` (line 1493)

As noted above, the Javadoc for `write(Writer writer)` is missing the `@param writer` tag.

---

**A84-14** — LOW — Bare `@throws JSONException` (no description) on multiple JSONObject methods

The following public methods carry `@throws JSONException` or `@throws JSONException If...` in their Javadoc but the ones listed below use the bare form with no condition description:
- `put(String key, Collection value)` — line 1021–1027: `@throws JSONException` (no text)
- `put(String key, Map value)` — line 1076–1083: `@throws JSONException` (no text)
- `write(Writer writer)` — line 1491: `@throws JSONException` (no text)

---

**A84-15** — MEDIUM — Inaccurate `@return` description on `optDouble(String key)` (line 813)

The Javadoc `@return` at line 811 reads: `@return An object which is the value.` but the method signature returns `double` (a primitive), not an `Object`. The copy-paste error is present in several `opt*` single-argument methods:

| Method | Line | Incorrect @return text |
|--------|------|------------------------|
| `optDouble(String key)` | 813 | `@return An object which is the value.` |
| `optDouble(String key, double defaultValue)` | 828 | `@return An object which is the value.` |
| `optInt(String key)` | 846 | `@return An object which is the value.` |
| `optInt(String key, int defaultValue)` | 861 | `@return An object which is the value.` |
| `optLong(String key)` | 907 | `@return An object which is the value.` |
| `optLong(String key, long defaultValue)` | 922 | `@return An object which is the value.` |

All six return primitive numeric types but the `@return` tag says "An object". This is a misleading copy-paste error across the numeric `opt*` family.

---

**A84-16** — MEDIUM — Inaccurate Javadoc on `valueToString(Object value)` (line 1395)

The `@return` description (lines 1388–1393) reads:
> "a printable, displayable, transmittable representation of the object, beginning with `{` (left brace) and ending with `}` (right brace)."

This description is copied from the `toString()` methods and is incorrect for `valueToString`. The method serialises any JSON value — strings are returned quoted, numbers as numerics, arrays as `[...]`, and only objects as `{...}`. The brace framing in the return description is inaccurate for the majority of inputs.

```java
/**
 * ...
 * @return a printable, displayable, transmittable
 *  representation of the object, beginning
 *  with <code>{</code>&nbsp;<small>(left brace)</small> and ending
 *  with <code>}</code>&nbsp;<small>(right brace)</small>.
 * @throws JSONException If the value is or contains an invalid number.
 */
public static String valueToString(Object value) throws JSONException {
```

---

**A84-17** — LOW — `toString()` (line 1346) has no `@return` tag

The Javadoc block (lines 1334–1345) for the zero-argument `toString()` override provides a prose description and a `@return` in the body text but uses no formal `@return` tag. Compare with `toString(int indentFactor)` (line 1367) which has a proper `@return` tag.

---

## Summary Table

| ID | File | Line(s) | Severity | Description |
|----|------|---------|----------|-------------|
| A84-1 | JSONException.java | 20 | MEDIUM | No Javadoc on `JSONException(Throwable)` constructor |
| A84-2 | JSONException.java | 25 | MEDIUM | No Javadoc on `getCause()` override |
| A84-3 | JSONException.java | 10, 20, 25 | HIGH | Silent deviation from `Throwable.getCause()` contract completely undocumented; shadow field and non-standard super() call create dangerous semantic difference |
| A84-4 | JSONML.java | 47,248,265,281,300,312 | LOW | Bare `@throws JSONException` (no descriptive text) on all public methods |
| A84-5 | JSONML.java | 47,248,265,281,300,312 | LOW | (duplicate of A84-4 — consolidated above) |
| A84-6 | JSONML.java | 272–286 | MEDIUM | Inaccurate `@param x` description on `toJSONObject(XMLTokener x)`; copy-paste formatting defect breaking paragraph |
| A84-7 | JSONML.java | 387–412 | MEDIUM | `toString(JSONObject jo)` states "must contain tagName" but silently falls back on missing tagName — undocumented behaviour |
| A84-8 | JSONObject.java | 588–593 | LOW | Missing `@param jo` on `getNames(JSONObject jo)` |
| A84-9 | JSONObject.java | 609–614 | LOW | Missing `@param object` on `getNames(Object object)` |
| A84-10 | JSONObject.java | 1115–1124 | LOW | `@return his.` typo in `putOnce`; bare `@param` tags without descriptions |
| A84-11 | JSONObject.java | 1173 | MEDIUM | No Javadoc at all on public `quote(String, Writer)` overload |
| A84-12 | JSONObject.java | 1484–1493 | LOW | Missing `@param writer` on `write(Writer writer)` |
| A84-13 | JSONObject.java | 1491 | LOW | Bare `@throws JSONException` (no description) on `write(Writer writer)` |
| A84-14 | JSONObject.java | 1021,1076 | LOW | Bare `@throws JSONException` on `put(String,Collection)` and `put(String,Map)` |
| A84-15 | JSONObject.java | 811,825,844,859,905,920 | MEDIUM | `@return` says "An object" for all numeric `optDouble`/`optInt`/`optLong` methods which return primitives |
| A84-16 | JSONObject.java | 1375–1395 | MEDIUM | `valueToString` `@return` incorrectly says result is `{`…`}` brace-wrapped (copied from `toString` Javadoc) |
| A84-17 | JSONObject.java | 1334–1346 | LOW | Zero-arg `toString()` missing formal `@return` tag |

**Total findings:** 16 unique (A84-1 through A84-17, with A84-4/A84-5 consolidated)
- HIGH: 1 (A84-3)
- MEDIUM: 7 (A84-1, A84-2, A84-6, A84-7, A84-11, A84-15, A84-16)
- LOW: 9 (A84-4, A84-8, A84-9, A84-10, A84-12, A84-13, A84-14, A84-17)
