# Pass 3 Documentation Audit — A86
**Audit run:** 2026-02-26-01
**Agent:** A86
**Files:**
- `src/main/java/com/json/JSONWriter.java`
- `src/main/java/com/json/XML.java`
- `src/main/java/com/json/XMLTokener.java`

**Note:** These are vendored/repackaged org.json library files (circa 2010–2012).

---

## 1. Reading Evidence

### 1.1 JSONWriter.java

**Class:** `JSONWriter` — line 59

**Fields:**

| Name | Type | Access | Line |
|------|------|--------|------|
| `maxdepth` | `int` (static final) | private | 60 |
| `comma` | `boolean` | private | 66 |
| `mode` | `char` | protected | 76 |
| `stack` | `JSONObject[]` (final) | private | 81 |
| `top` | `int` | private | 86 |
| `writer` | `Writer` | protected | 91 |

**Methods:**

| Name | Access | Line |
|------|--------|------|
| `JSONWriter(Writer w)` | public | 96 |
| `append(String string)` | private | 110 |
| `array()` | public | 141 |
| `end(char mode, char c)` | private | 158 |
| `endArray()` | public | 180 |
| `endObject()` | public | 190 |
| `key(String string)` | public | 202 |
| `object()` | public | 234 |
| `pop(char c)` | private | 254 |
| `push(JSONObject jo)` | private | 275 |
| `value(boolean b)` | public | 292 |
| `value(double d)` | public | 302 |
| `value(long l)` | public | 312 |
| `value(Object object)` | public | 324 |

---

### 1.2 XML.java

**Class:** `XML` — line 36

**Fields (public static final Character constants):**

| Name | Type | Line |
|------|------|------|
| `AMP` | `Character` | 39 |
| `APOS` | `Character` | 42 |
| `BANG` | `Character` | 45 |
| `EQ` | `Character` | 48 |
| `GT` | `Character` | 51 |
| `LT` | `Character` | 54 |
| `QUEST` | `Character` | 57 |
| `QUOT` | `Character` | 60 |
| `SLASH` | `Character` | 63 |

**Methods:**

| Name | Access | Line |
|------|--------|------|
| `escape(String string)` | public static | 76 |
| `noSpace(String string)` | public static | 109 |
| `parse(XMLTokener x, JSONObject context, String name)` | private static | 130 |
| `stringToValue(String string)` | public static | 303 |
| `toJSONObject(String string)` | public static | 365 |
| `toString(Object object)` | public static | 381 |
| `toString(Object object, String tagName)` | public static | 393 |

---

### 1.3 XMLTokener.java

**Class:** `XMLTokener extends JSONTokener` — line 33

**Fields:**

| Name | Type | Access | Line |
|------|------|--------|------|
| `entity` | `java.util.HashMap` (static final) | public | 39 |

**Methods:**

| Name | Access | Line |
|------|--------|------|
| `XMLTokener(String s)` | public | 54 |
| `nextCDATA()` | public | 63 |
| `nextContent()` | public | 92 |
| `nextEntity(char ampersand)` | public | 127 |
| `nextMeta()` | public | 154 |
| `nextToken()` | public | 219 |
| `skipPast(String to)` | public | 301 |

---

## 2. Findings

### A86-1 — [LOW] JSONWriter constructor: missing @param tag

**File:** `JSONWriter.java`
**Location:** Constructor `JSONWriter(Writer w)`, line 96
**Javadoc (lines 93–95):**
```java
/**
 * Make a fresh JSONWriter. It can be used to build one JSON text.
 */
```
The constructor takes parameter `w` (the target `Writer`) but the Javadoc has no `@param w` tag. The description is also minimal — it does not describe the parameter's role at all.

**Severity:** LOW (missing @param on documented method)

---

### A86-2 — [LOW] `value(boolean b)` — empty @throws tag body

**File:** `JSONWriter.java`
**Location:** Method `value(boolean b)`, lines 285–293
**Javadoc (lines 285–291):**
```java
/**
 * Append either the value <code>true</code> or the value
 * <code>false</code>.
 * @param b A boolean.
 * @return this
 * @throws JSONException
 */
```
The `@throws JSONException` tag has no explanatory text. Although a `JSONException` can propagate from the underlying `append()` call (if the value is out of sequence), the tag provides no description of the condition triggering it. The sibling methods `value(double d)` (line 300) and `value(long l)` (line 308) also have bare `@throws JSONException` tags with no description.

**Severity:** LOW (missing description on @throws; consistent with org.json convention but non-compliant with Javadoc norms)

---

### A86-3 — [LOW] `value(long l)` — empty @throws tag body

**File:** `JSONWriter.java`
**Location:** Method `value(long l)`, lines 307–314
**Javadoc (lines 307–311):**
```java
/**
 * Append a long value.
 * @param l A long.
 * @return this
 * @throws JSONException
 */
```
Same issue as A86-2: the `@throws JSONException` tag carries no descriptive text. Unlike `value(double d)` — which documents "If the number is not finite" — this tag is completely bare.

**Severity:** LOW (missing description on @throws)

---

### A86-4 — [MEDIUM] `value(boolean b)` and `value(long l)` — `@throws JSONException` is misleading / inaccurate

**File:** `JSONWriter.java`
**Location:** `value(boolean b)` line 292; `value(long l)` line 312

Both methods delegate directly to `append()`. The `append()` method throws `JSONException` only if the writer is in neither 'o' nor 'a' mode (i.e., "Value out of sequence"), or if an `IOException` occurs. For `value(boolean b)` and `value(long l)` the listed `@throws JSONException` is technically accurate but the absence of any condition description means it is functionally misleading — a reader cannot distinguish whether the exception is "if not finite" (as documented for `value(double d)`) or "if out of sequence" (the actual cause). For `value(double d)`, the comment "If the number is not finite" is correct and more precise.

More critically, the class-level Javadoc at line 54 states "Objects and arrays can be nested up to 20 levels deep" — but the actual `maxdepth` constant (line 60) is **200**, not 20. This is a factual error left over from an older version of the class.

**Severity:** MEDIUM (inaccurate comment — stated nesting limit of 20 contradicts the implemented limit of 200)

---

### A86-5 — [MEDIUM] Class-level Javadoc for `JSONWriter` states nesting limit of 20, but implementation uses 200

**File:** `JSONWriter.java`
**Location:** Class Javadoc, line 52; field `maxdepth`, line 60
**Javadoc text:**
```
* Objects and arrays can be nested up to 20 levels deep.
```
**Implementation:**
```java
private static final int maxdepth = 200;
```
The documented limit (20) is an order of magnitude smaller than the enforced limit (200). Any caller relying on this documentation to understand the nesting ceiling will be given incorrect information.

**Severity:** MEDIUM (inaccurate comment)

---

### A86-6 — [LOW] `XML.noSpace()` — @param tag has no description text

**File:** `XML.java`
**Location:** Method `noSpace(String string)`, lines 103–110
**Javadoc (lines 103–108):**
```java
/**
 * Throw an exception if the string contains whitespace.
 * Whitespace is not allowed in tagNames and attributes.
 * @param string
 * @throws JSONException
 */
```
Both the `@param string` and `@throws JSONException` tags lack descriptive text. The `@param` should describe what the string represents (a tag name or attribute value to validate). The `@throws` should say "If `string` is empty or contains a whitespace character."

**Severity:** LOW (missing @param description; missing @throws description)

---

### A86-7 — [MEDIUM] `XML.escape()` — Javadoc omits apostrophe escape from the documented table, yet the implementation escapes it

**File:** `XML.java`
**Location:** Method `escape(String string)`, lines 65–101
**Javadoc (lines 65–75):**
```java
/**
 * Replace special characters with XML escapes:
 * <pre>
 * &amp; <small>(ampersand)</small> is replaced by &amp;amp;
 * &lt; <small>(less than)</small> is replaced by &amp;lt;
 * &gt; <small>(greater than)</small> is replaced by &amp;gt;
 * &quot; <small>(double quote)</small> is replaced by &amp;quot;
 * </pre>
 * @param string The string to be escaped.
 * @return The escaped string.
 */
```
The implementation (lines 92–95) also escapes the apostrophe/single-quote character `'` as `&apos;`, but this case is completely absent from the Javadoc table. A caller reading only the documentation would not know that apostrophes are transformed, which could matter when the caller is attempting to predict or round-trip the output.

**Severity:** MEDIUM (inaccurate/incomplete comment — documented behaviour does not match implementation)

---

### A86-8 — [LOW] `XML.toString(Object object)` — @return tag text is vague; no mention of wrapping tag behaviour

**File:** `XML.java`
**Location:** Method `toString(Object object)`, lines 375–383
**Javadoc:**
```java
/**
 * Convert a JSONObject into a well-formed, element-normal XML string.
 * @param object A JSONObject.
 * @return  A string.
 * @throws  JSONException
 */
```
The `@return` tag says only "A string." The overloaded `toString(Object object, String tagName)` at line 386 is more useful but still terse. Additionally the `@param` says "A JSONObject" but the implementation actually accepts any `Object` (including `JSONArray`, raw arrays, primitives via boxing, or `null`-safe objects) — the @param description is therefore misleading.

**Severity:** LOW for vague @return; but the @param inaccuracy ("A JSONObject" when any Object is accepted) is also present in the two-arg overload.

---

### A86-9 — [MEDIUM] `XML.toString(Object object, String tagName)` — @param `object` described as "A JSONObject" but any Object is accepted

**File:** `XML.java`
**Location:** Method `toString(Object object, String tagName)`, lines 386–393
**Javadoc:**
```java
/**
 * Convert a JSONObject into a well-formed, element-normal XML string.
 * @param object A JSONObject.
 * @param tagName The optional name of the enclosing tag.
 * @return A string.
 * @throws JSONException
 */
```
The implementation (lines 393–507) handles `JSONObject`, `JSONArray`, raw Java arrays (converted via `new JSONArray(object)`), and scalar values. Describing the parameter as "A JSONObject" is inaccurate and narrows the apparent contract. Callers passing other valid types may be surprised.

**Severity:** MEDIUM (inaccurate @param description)

---

### A86-10 — [LOW] `XML.toJSONObject()` — bare `@throws JSONException` with no description

**File:** `XML.java`
**Location:** Method `toJSONObject(String string)`, lines 351–372
**Javadoc (line 363):**
```java
 * @throws JSONException
```
No condition is described. The method can throw for many reasons (malformed XML, unclosed tags, mismatched tags, etc.). The omission provides no guidance.

**Severity:** LOW (missing @throws description)

---

### A86-11 — [LOW] `XMLTokener` — `entity` field uses raw `HashMap` type (no generics); Javadoc comment style is non-standard

**File:** `XMLTokener.java`
**Location:** Field `entity`, lines 36–39
**Comment (lines 36–38):**
```java
/** The table of entity values. It initially contains Character values for
 * amp, apos, gt, lt, quot.
 */
public static final java.util.HashMap entity;
```
The field-level documentation opens with `/**` on the same line as the text (single-line `/** ... */` wrapped across lines), which is valid Javadoc but non-standard formatting. More substantively, the type is raw `java.util.HashMap` without generics, and the documentation does not mention the key type (`String`) or value type (`Character` or `Object`). This is a minor documentation gap rather than an inaccuracy.

**Severity:** LOW (incomplete field documentation)

---

### A86-12 — [LOW] `XMLTokener.skipPast()` — missing @return tag in Javadoc

**File:** `XMLTokener.java`
**Location:** Method `skipPast(String to)`, lines 295–364
**Javadoc (lines 295–300):**
```java
/**
 * Skip characters until past the requested string.
 * If it is not found, we are left at the end of the source with a result of false.
 * @param to A string to skip past.
 * @throws JSONException
 */
```
The method returns `boolean` — `true` if the target string was found and skipped past, `false` if end-of-input was reached first. While the behaviour is partially described in the prose, there is no `@return` tag. The `@throws JSONException` is also bare (no condition given), though in practice this method does not appear to throw `JSONException` internally — it delegates to `next()` from the parent class. The declared `@throws JSONException` may be residual from the parent class signature rather than meaningful for this method.

**Severity:** LOW (missing @return tag; bare/potentially superfluous @throws tag)

---

### A86-13 — [LOW] `XMLTokener.nextContent()` — bare `@throws JSONException` with no description

**File:** `XMLTokener.java`
**Location:** Method `nextContent()`, lines 83–117
**Javadoc (line 90):**
```java
 * @throws JSONException
```
No condition is described. The method can throw from `next()` or `nextEntity()`.

**Severity:** LOW (missing @throws description)

---

## 3. Summary Table

| ID | File | Location | Severity | Description |
|----|------|----------|----------|-------------|
| A86-1 | JSONWriter.java | Constructor `JSONWriter(Writer)` line 96 | LOW | Missing `@param w` tag |
| A86-2 | JSONWriter.java | `value(boolean b)` line 292 | LOW | Bare `@throws JSONException` — no condition described |
| A86-3 | JSONWriter.java | `value(long l)` line 312 | LOW | Bare `@throws JSONException` — no condition described |
| A86-4 | JSONWriter.java | `value(boolean b)`, `value(long l)` | MEDIUM | Undescribed @throws creates misleading contrast with `value(double d)` which does describe its condition |
| A86-5 | JSONWriter.java | Class Javadoc line 52; `maxdepth` field line 60 | MEDIUM | Class doc states nesting limit of 20; implementation enforces 200 |
| A86-6 | XML.java | `noSpace(String)` line 109 | LOW | `@param string` and `@throws` both have no descriptive text |
| A86-7 | XML.java | `escape(String)` line 76 | MEDIUM | Javadoc table omits apostrophe→`&apos;` escape that the implementation performs |
| A86-8 | XML.java | `toString(Object)` line 381 | LOW | `@return` is "A string"; `@param object` incorrectly says "A JSONObject" |
| A86-9 | XML.java | `toString(Object, String)` line 393 | MEDIUM | `@param object` says "A JSONObject" but any Object is accepted |
| A86-10 | XML.java | `toJSONObject(String)` line 365 | LOW | Bare `@throws JSONException` — no condition described |
| A86-11 | XMLTokener.java | `entity` field line 39 | LOW | Key/value types not documented; raw HashMap |
| A86-12 | XMLTokener.java | `skipPast(String)` line 301 | LOW | Missing `@return` tag; bare `@throws JSONException` |
| A86-13 | XMLTokener.java | `nextContent()` line 92 | LOW | Bare `@throws JSONException` — no condition described |

**Total findings: 13**
- HIGH: 0
- MEDIUM: 4 (A86-4, A86-5, A86-7, A86-9)
- LOW: 9 (A86-1, A86-2, A86-3, A86-6, A86-8, A86-10, A86-11, A86-12, A86-13)

---

## 4. Notes on Vendored Code

All three files are vendored copies of the org.json library (circa 2002–2011). The documentation issues found are inherited from the upstream library and are not the result of local modification. The most actionable finding for maintainers is **A86-5** (the stated nesting depth of 20 vs. actual 200), which could affect callers who consult the Javadoc to understand API limits. The **A86-7** omission of the apostrophe escape from `XML.escape()`'s documented table is the next most likely to cause a real integration misunderstanding.
