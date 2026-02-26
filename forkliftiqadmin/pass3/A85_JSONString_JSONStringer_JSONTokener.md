# Pass 3 Documentation Audit — A85
**Audit run:** 2026-02-26-01
**Agent:** A85
**Files:**
- `src/main/java/com/json/JSONString.java`
- `src/main/java/com/json/JSONStringer.java`
- `src/main/java/com/json/JSONTokener.java`

**Note:** These are vendored/repackaged org.json library files (circa 2010–2012). All three files belong to `package com.json`.

---

## Reading Evidence

### JSONString.java

**Type:** interface

| Element | Kind | Line |
|---------|------|------|
| `JSONString` | interface declaration | 10 |
| `toJSONString()` | public method | 17 |

Fields: none (interface).

---

### JSONStringer.java

**Type:** class (extends `JSONWriter`)

| Element | Kind | Line |
|---------|------|------|
| `JSONStringer` | class declaration | 59 |
| `JSONStringer()` | public constructor | 63 |
| `toString()` | public method | 75 |

Fields declared in this class: none (all state is in parent `JSONWriter`).

Inherited field referenced: `this.mode` (type `char`, declared in `JSONWriter` at line 76 of JSONWriter.java) and `this.writer` (type `Writer`, declared in `JSONWriter` at line 91).

---

### JSONTokener.java

**Type:** class

| Element | Kind | Line |
|---------|------|------|
| `JSONTokener` | class declaration | 41 |
| `character` | private field, `long` | 43 |
| `eof` | private field, `boolean` | 44 |
| `index` | private field, `long` | 45 |
| `line` | private field, `long` | 46 |
| `previous` | private field, `char` | 47 |
| `reader` | private field, `Reader` | 48 |
| `usePrevious` | private field, `boolean` | 49 |
| `JSONTokener(Reader)` | public constructor | 57 |
| `JSONTokener(InputStream)` | public constructor | 73 |
| `JSONTokener(String)` | public constructor | 83 |
| `back()` | public method | 93 |
| `dehexchar(char)` | public static method | 110 |
| `end()` | public method | 123 |
| `more()` | public method | 133 |
| `next()` | public method | 148 |
| `next(char)` | public method | 187 |
| `next(int)` | public method | 206 |
| `nextClean()` | public method | 230 |
| `nextString(char)` | public method | 251 |
| `nextTo(char)` | public method | 308 |
| `nextTo(String)` | public method | 329 |
| `nextValue()` | public method | 353 |
| `skipTo(char)` | public method | 400 |
| `syntaxError(String)` | public method | 432 |
| `toString()` | public method | 442 |

---

## Findings

---

### A85-1 — JSONTokener: `InputStream` constructor missing `@param` tag
**File:** `JSONTokener.java`
**Location:** Line 72–75
**Severity:** LOW

The constructor `JSONTokener(InputStream inputStream)` has a Javadoc block, but the block contains only the summary sentence and no `@param` tag for the `inputStream` parameter. The other two constructors (`Reader` at line 52 and `String` at line 78) each include a `@param` tag.

```java
/**
 * Construct a JSONTokener from an InputStream.
 */
public JSONTokener(InputStream inputStream) throws JSONException {
```

Missing: `@param inputStream  An input stream.`
Also note: the Javadoc omits documentation of the checked `throws JSONException` (no `@throws` tag), which is inconsistent with several other methods that do document their throws inline.

---

### A85-2 — JSONTokener: `end()` method entirely undocumented
**File:** `JSONTokener.java`
**Location:** Line 123–125
**Severity:** MEDIUM

The public method `end()` has no Javadoc at all. It is a non-trivial method: it combines two state checks (`this.eof` and `!this.usePrevious`) to determine whether tokenising is truly finished, distinguishing the "used a back() lookahead and haven't consumed it yet" case from genuine end-of-input. This distinction is important for callers and deserves explanation.

```java
public boolean end() {
    return this.eof && !this.usePrevious;
}
```

No `/** ... */` block is present above this declaration.

---

### A85-3 — JSONTokener: `nextClean()` — `@throws` tag present but malformed/empty
**File:** `JSONTokener.java`
**Location:** Lines 225–237
**Severity:** LOW

The Javadoc for `nextClean()` contains a bare `@throws JSONException` tag with no descriptive text:

```java
/**
 * Get the next char in the string, skipping whitespace.
 * @throws JSONException
 * @return  A character, or 0 if there are no more characters.
 */
```

Additionally, the `@throws` tag is placed before `@return`, which is contrary to standard Javadoc ordering (description, `@param`, `@return`, `@throws`). The empty `@throws` provides no useful information about when the exception is thrown. The exception propagates from `next()`, which can throw if the underlying reader fails, but the Javadoc gives no indication of this.

---

### A85-4 — JSONTokener: `next(int n)` — `@throws` description is inaccurate / misleading
**File:** `JSONTokener.java`
**Location:** Lines 197–222
**Severity:** MEDIUM

The Javadoc states:

```java
/**
 * Get the next n characters.
 *
 * @param n     The number of characters to take.
 * @return      A string of n characters.
 * @throws JSONException
 *   Substring bounds error if there are not
 *   n characters remaining in the source string.
 */
```

The phrase "Substring bounds error" is the literal text of the exception message thrown by `syntaxError("Substring bounds error")`, not a meaningful description of the condition. A reader consulting the Javadoc cannot determine what "substring bounds error" means in terms of the method's contract without reading the source. The accurate description is: "thrown when the source has fewer than `n` characters remaining." This is a minor accuracy issue (the meaning is inferable) but is imprecise enough to warrant a MEDIUM finding as it could mislead a caller into thinking an array/string index exception type is involved rather than a JSON syntax exception.

The Javadoc also does not note that `n == 0` returns `""` immediately without consuming any input, which is a non-obvious short-circuit the caller may need to know.

---

### A85-5 — JSONTokener: `nextClean()` — `@return` description is inaccurate for whitespace-only input
**File:** `JSONTokener.java`
**Location:** Lines 225–237
**Severity:** MEDIUM

The Javadoc states:

```
@return  A character, or 0 if there are no more characters.
```

The method returns `char` `0` (null character, `'\0'`) not Java `int` `0`. While the return type is `char` so this is technically equivalent, the more substantive inaccuracy is that the method also returns `0` (i.e., terminates) if `next()` returns `0` — which per `next()`'s implementation occurs when the reader reaches end-of-stream (`c <= 0`). The description "no more characters" is correct in spirit, but the exact condition is "end of input stream" rather than "no more characters in source string," since `nextClean` is used in stream contexts as well as string contexts. This is a minor inaccuracy.

More importantly, the method skips ALL characters with code point `<= ' '` (i.e., all ASCII control characters and space), not just conventional whitespace (`\t`, `\n`, `\r`, ` `). The Javadoc says "skipping whitespace" but the implementation skips any character whose code point is 0x20 or below. This is an inaccuracy in the summary sentence.

```java
public char nextClean() throws JSONException {
    for (;;) {
        char c = this.next();
        if (c == 0 || c > ' ') {
            return c;
        }
    }
}
```

The condition `c > ' '` means any character with ordinal value 33 or above is returned, while characters 1–32 (all ASCII control codes) are skipped, not merely the four standard whitespace characters.

---

### A85-6 — JSONStringer: class-level Javadoc references `JSONWriter` method return type inconsistently
**File:** `JSONStringer.java`
**Location:** Lines 29–58
**Severity:** LOW

The class-level Javadoc states:

```
All of these methods return the JSONWriter instance, permitting cascade style.
```

Because `JSONStringer` extends `JSONWriter` and does not override `array()`, `endArray()`, `object()`, `endObject()`, `key()`, or `value()`, those methods return `JSONWriter` (the declared return type), not `JSONStringer`. The cascade example in the Javadoc calls `toString()` at the end, which is only valid because the variable is typed as `JSONStringer`. The statement is technically accurate — they do return `JSONWriter` instances — but the wording "return the JSONWriter instance" implies the caller gets a `JSONWriter` back, which means they would need to cast to call `JSONStringer.toString()` if the variable is declared as `JSONWriter`. This is not a dangerous inaccuracy but is potentially confusing for a user who stores the result of a chained call in a variable. Severity is LOW.

---

### A85-7 — JSONTokener: `syntaxError()` — `@return` description is incomplete
**File:** `JSONTokener.java`
**Location:** Lines 426–434
**Severity:** LOW

The Javadoc for `syntaxError` states:

```java
/**
 * Make a JSONException to signal a syntax error.
 *
 * @param message The error message.
 * @return  A JSONException object, suitable for throwing
 */
```

The `@return` tag says "suitable for throwing" but does not describe what is appended to the message (the `this.toString()` positional context). Callers do not know from the Javadoc that the returned exception's message will also include position information (index, character, line). This is a minor omission but reduces the usefulness of the documentation. The method body:

```java
return new JSONException(message + this.toString());
```

appends the tokener's current position, which is significant diagnostic information.

---

## Summary Table

| ID | File | Location | Severity | Description |
|----|------|----------|----------|-------------|
| A85-1 | JSONTokener.java | Line 72 | LOW | `JSONTokener(InputStream)` constructor missing `@param` tag |
| A85-2 | JSONTokener.java | Line 123 | MEDIUM | `end()` public method has no Javadoc at all |
| A85-3 | JSONTokener.java | Line 225 | LOW | `nextClean()` has empty `@throws` tag with no description |
| A85-4 | JSONTokener.java | Line 197 | MEDIUM | `next(int)` `@throws` description uses opaque literal error message text instead of meaningful condition; `n==0` short-circuit undocumented |
| A85-5 | JSONTokener.java | Line 225 | MEDIUM | `nextClean()` summary inaccurately says "skipping whitespace" — actually skips all characters with code point <= 0x20 (all ASCII control chars) |
| A85-6 | JSONStringer.java | Line 42 | LOW | Class Javadoc says methods "return the JSONWriter instance" which may confuse callers doing cascade chains typed as `JSONStringer` |
| A85-7 | JSONTokener.java | Line 426 | LOW | `syntaxError()` `@return` omits that position context is appended to the message |

**Total findings: 7** (3 MEDIUM, 4 LOW)

---

## No-Issue Notes

- **JSONString.java** — Class-level Javadoc is present and accurate. The single method `toJSONString()` has a Javadoc block with an `@return` tag. No `@param` is needed (no parameters). No findings.
- **JSONStringer constructor** (`JSONStringer()`, line 63) — Documented with a brief Javadoc. No parameters, no return value (constructor). No findings.
- **JSONStringer.toString()** (line 75) — Documented with Javadoc, `@return` tag present. The description that it returns `null` on construction error is accurate per the implementation (`this.mode == 'd'` check). No findings.
- **JSONTokener** — Class-level Javadoc is present (`@author`, `@version`, summary). Acceptable.
- All other `JSONTokener` public methods with Javadoc (`back`, `dehexchar`, `more`, `next()`, `next(char)`, `nextString`, `nextTo(char)`, `nextTo(String)`, `nextValue`, `skipTo`, `toString`) have `@param` and/or `@return` tags where applicable and the descriptions are sufficiently accurate.
