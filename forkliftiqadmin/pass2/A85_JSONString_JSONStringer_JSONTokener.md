# Pass 2 Test Coverage Audit — A85
**Audit Run:** 2026-02-26-01
**Agent ID:** A85
**Files Audited:**
1. `src/main/java/com/json/JSONString.java`
2. `src/main/java/com/json/JSONStringer.java`
3. `src/main/java/com/json/JSONTokener.java`

**Test Directory Searched:** `src/test/java/`

---

## Vendored Library Context

All three files are part of the `com.json` package, which is the `org.json` library (JSON.org) vendored directly into the application source tree under the `com.json` package namespace. The `com/json/` directory contains 15 files in total (CDL, Cookie, CookieList, HTTP, HTTPTokener, JSONArray, JSONException, JSONML, JSONObject, JSONString, JSONStringer, JSONTokener, JSONWriter, XML, XMLTokener). This is a wholesale copy of the org.json library, not a selective import.

License headers present in `JSONStringer.java` (copyright 2006 JSON.org) and `JSONTokener.java` (copyright 2002 JSON.org). `JSONString.java` has no license header — only a Javadoc comment, consistent with the org.json interface definition of the same period.

No application-specific modifications were identified in any of the three files: all code matches canonical org.json implementations. No custom logic, overrides, or project-specific additions are present.

---

## Reading Evidence

### File 1: `JSONString.java`

**Class:** `JSONString` (interface)

**Fields:** None.

**Methods:**

| Method | Line |
|--------|------|
| `toJSONString()` | 17 |

---

### File 2: `JSONStringer.java`

**Class:** `JSONStringer extends JSONWriter`

**Fields:** None declared in this class (all fields inherited from `JSONWriter`: `comma` line 66, `mode` line 76, `stack` line 81, `top` line 86, `writer` line 91 — as read in `JSONWriter.java`).

**Methods:**

| Method | Line |
|--------|------|
| `JSONStringer()` (constructor) | 63 |
| `toString()` | 75 |

---

### File 3: `JSONTokener.java`

**Class:** `JSONTokener`

**Fields:**

| Field | Line |
|-------|------|
| `character` (private long) | 43 |
| `eof` (private boolean) | 44 |
| `index` (private long) | 45 |
| `line` (private long) | 46 |
| `previous` (private char) | 47 |
| `reader` (private Reader) | 48 |
| `usePrevious` (private boolean) | 49 |

**Methods:**

| Method | Line |
|--------|------|
| `JSONTokener(Reader reader)` (constructor) | 57 |
| `JSONTokener(InputStream inputStream)` (constructor) | 73 |
| `JSONTokener(String s)` (constructor) | 83 |
| `back()` | 93 |
| `dehexchar(char c)` (static) | 110 |
| `end()` | 123 |
| `more()` | 133 |
| `next()` | 148 |
| `next(char c)` | 187 |
| `next(int n)` | 206 |
| `nextClean()` | 230 |
| `nextString(char quote)` | 251 |
| `nextTo(char delimiter)` | 308 |
| `nextTo(String delimiters)` | 329 |
| `nextValue()` | 353 |
| `skipTo(char to)` | 400 |
| `syntaxError(String message)` | 432 |
| `toString()` | 442 |

---

## Test Coverage Search Results

**Grep for `JSONString` in `src/test/java/`:** No matches found.
**Grep for `JSONStringer` in `src/test/java/`:** No matches found.
**Grep for `JSONTokener` in `src/test/java/`:** No matches found.

The test directory contains exactly 4 test files, none of which reference any class from the `com.json` package:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

---

## Findings

### A85-1 | Severity: HIGH | No test coverage for any of the three audited files

`JSONString`, `JSONStringer`, and `JSONTokener` have zero test coverage. No test class or method in `src/test/java/` references these types. The overall test suite contains only 4 test files covering calibration and utility logic; the entire `com.json` package is untested.

---

### A85-2 | Severity: HIGH | Entire vendored `com.json` library (15 files) has no test coverage

The absence of tests is not isolated to the three audited files. All 15 files in the `com.json` package are uncovered. While the upstream `org.json` library has its own test suite in its own repository, no tests for the vendored copy exist in this project. Any divergence introduced during vendoring (package rename from `org.json` to `com.json`, potential future patches) would go undetected.

---

### A85-3 | Severity: MEDIUM | `JSONStringer.toString()` returns `null` on incomplete JSON construction — no test verifies this contract

`JSONStringer.toString()` at line 76 returns `null` when `this.mode != 'd'` (i.e., when the JSON structure is not properly closed). This silent `null` return is a known footgun: callers who do not check the return value before using it in string concatenation or HTTP responses will produce the literal string `"null"` in output. No test in the project verifies the happy path, the `null`-return path, or any error propagation scenario.

---

### A85-4 | Severity: MEDIUM | `JSONTokener.nextString()` uses `StringBuffer` instead of `StringBuilder` — thread-safety overhead with no benefit

At line 253, `nextString(char quote)` allocates a `StringBuffer`. `JSONTokener` is not thread-safe (mutable fields, no synchronization), so the synchronized `StringBuffer` provides no benefit over `StringBuilder` and imposes unnecessary overhead. The same pattern appears in `nextTo(char)` at line 309 and `nextTo(String)` at line 331, and in `nextValue()` at line 378. With zero test coverage there is no regression safety net around these methods.

---

### A85-5 | Severity: MEDIUM | `JSONTokener(InputStream)` constructor declares `throws JSONException` unnecessarily

The constructor at line 73 declares `throws JSONException`, but its body only delegates to `this(new InputStreamReader(inputStream))`, which does not throw `JSONException`. This is a misleading signature inherited from the upstream library. No test verifies the constructor's actual behaviour or its exception declaration.

---

### A85-6 | Severity: MEDIUM | `JSONTokener.skipTo()` uses a hardcoded `mark(1000000)` buffer limit

At line 406, `this.reader.mark(1000000)` is called with a fixed 1 MB lookahead limit. If the character being sought does not appear within the next 1,000,000 characters of input, the `reset()` call at line 411 may throw `IOException` (mark invalidated), which would propagate as `JSONException`. This edge case is not covered by any test.

---

### A85-7 | Severity: LOW | `JSONString` interface has no license header

`JSONString.java` (line 1–18) contains only a package declaration and Javadoc, with no copyright or license header. The other vendored files (`JSONStringer.java`, `JSONTokener.java`, and `JSONWriter.java`) all carry the JSON.org MIT-style license block. The omission is inconsistent and may matter for license compliance audits. Not a code-correctness issue.

---

### A85-8 | Severity: LOW | `JSONStringer` inherits a 200-level nesting depth from `JSONWriter` with no documentation in `JSONStringer` Javadoc

`JSONWriter` declares `private static final int maxdepth = 200` at line 60 of `JSONWriter.java`. The `JSONStringer` class Javadoc (line 53) still references the original org.json limit of "20 levels deep," which is now inaccurate — the vendored `JSONWriter` was updated to 200 but the `JSONStringer` Javadoc was not updated to match. No test verifies nesting-depth enforcement in either direction.

---

### A85-9 | Severity: LOW | `JSONTokener.nextValue()` accepts single-quoted strings, which is non-standard JSON — no application-level test guards this behaviour

At lines 358–360, `nextValue()` treats `'` (single quote) as a valid string delimiter, routing to `nextString('\'')`. The JSON specification (RFC 8259) does not permit single-quoted strings. This lenient parsing may accept malformed input silently. Because there are no tests, it is unknown whether application code that feeds tokens into `JSONTokener` depends on or is surprised by this permissiveness.

---

### A85-10 | Severity: INFO | Vendored library package rename (`org.json` → `com.json`) creates a maintenance burden with no compensating test safety net

The upstream library is available via Maven (`org.json:json`). Vendoring it by renaming the package to `com.json` means the project must manually track upstream patches (security fixes, bug fixes). With zero tests, any future patch application cannot be verified for correctness. This is an architectural observation, not a code defect in the audited files themselves.

---

## Summary Table

| ID | Severity | Description |
|----|----------|-------------|
| A85-1 | HIGH | No test coverage for `JSONString`, `JSONStringer`, or `JSONTokener` |
| A85-2 | HIGH | Entire `com.json` vendored library (15 files) has no test coverage |
| A85-3 | MEDIUM | `JSONStringer.toString()` silent `null` return path untested |
| A85-4 | MEDIUM | `StringBuffer` used in non-thread-safe class (should be `StringBuilder`); unchecked by tests |
| A85-5 | MEDIUM | `JSONTokener(InputStream)` misleadingly declares `throws JSONException` |
| A85-6 | MEDIUM | Hardcoded 1 MB mark limit in `skipTo()` creates untested edge case |
| A85-7 | LOW | `JSONString.java` missing license header (inconsistent with rest of `com.json`) |
| A85-8 | LOW | `JSONStringer` Javadoc says 20-level nesting limit; actual limit is 200 (stale doc) |
| A85-9 | LOW | Non-standard single-quote string parsing in `nextValue()` is untested and undocumented at the application level |
| A85-10 | INFO | Vendored package rename creates ongoing maintenance burden with no test safety net |
