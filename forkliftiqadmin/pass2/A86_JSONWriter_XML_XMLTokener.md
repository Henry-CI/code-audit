# Pass 2 Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A86
**Report Date:** 2026-02-26
**Files Audited:**
1. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/json/JSONWriter.java`
2. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/json/XML.java`
3. `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/json/XMLTokener.java`

**Test Directory Searched:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/`

---

## Vendored Library Note

All three classes belong to the `com.json` package, which is a vendored copy of the `org.json` library (JSON.org reference implementation). The package has been repackaged from `org.json` to `com.json`. Copyright headers in all three files read "Copyright (c) 2002/2006 JSON.org" with the standard JSON.org MIT-like licence. No application-specific logic or modifications are visible beyond the package rename. These classes are utility/infrastructure code, not business-domain code specific to the forkliftiqadmin application.

---

## Reading Evidence

### 1. JSONWriter.java

**Class name:** `JSONWriter`

**Fields:**

| Field Name | Line | Access | Type |
|---|---|---|---|
| `maxdepth` | 60 | `private static final` | `int` (value: 200) |
| `comma` | 66 | `private` | `boolean` |
| `mode` | 76 | `protected` | `char` |
| `stack` | 81 | `private final` | `JSONObject[]` |
| `top` | 86 | `private` | `int` |
| `writer` | 91 | `protected` | `Writer` |

**Methods:**

| Method Name | Line | Access |
|---|---|---|
| `JSONWriter(Writer w)` (constructor) | 96 | `public` |
| `append(String string)` | 110 | `private` |
| `array()` | 141 | `public` |
| `end(char mode, char c)` | 158 | `private` |
| `endArray()` | 180 | `public` |
| `endObject()` | 190 | `public` |
| `key(String string)` | 202 | `public` |
| `object()` | 234 | `public` |
| `pop(char c)` | 254 | `private` |
| `push(JSONObject jo)` | 275 | `private` |
| `value(boolean b)` | 292 | `public` |
| `value(double d)` | 302 | `public` |
| `value(long l)` | 312 | `public` |
| `value(Object object)` | 324 | `public` |

---

### 2. XML.java

**Class name:** `XML`

**Fields (public static final Character constants):**

| Field Name | Line | Value |
|---|---|---|
| `AMP` | 39 | `'&'` |
| `APOS` | 42 | `'\''` |
| `BANG` | 45 | `'!'` |
| `EQ` | 48 | `'='` |
| `GT` | 51 | `'>'` |
| `LT` | 54 | `'<'` |
| `QUEST` | 57 | `'?'` |
| `QUOT` | 60 | `'"'` |
| `SLASH` | 63 | `'/'` |

**Methods:**

| Method Name | Line | Access |
|---|---|---|
| `escape(String string)` | 76 | `public static` |
| `noSpace(String string)` | 109 | `public static` |
| `parse(XMLTokener x, JSONObject context, String name)` | 130 | `private static` |
| `stringToValue(String string)` | 303 | `public static` |
| `toJSONObject(String string)` | 365 | `public static` |
| `toString(Object object)` | 381 | `public static` |
| `toString(Object object, String tagName)` | 393 | `public static` |

---

### 3. XMLTokener.java

**Class name:** `XMLTokener`
**Extends:** `JSONTokener`

**Fields:**

| Field Name | Line | Access | Type |
|---|---|---|---|
| `entity` | 39 | `public static final` | `java.util.HashMap` (raw type) |

**Static initialiser (lines 41-48):** Populates `entity` map with 5 standard XML entity mappings: `amp`, `apos`, `gt`, `lt`, `quot`.

**Methods:**

| Method Name | Line | Access |
|---|---|---|
| `XMLTokener(String s)` (constructor) | 54 | `public` |
| `nextCDATA()` | 63 | `public` |
| `nextContent()` | 92 | `public` |
| `nextEntity(char ampersand)` | 127 | `public` |
| `nextMeta()` | 154 | `public` |
| `nextToken()` | 219 | `public` |
| `skipPast(String to)` | 301 | `public` |

---

## Test Coverage Search Results

Grep of `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/test/java/` for each class name:

- `JSONWriter` — **0 matches** (no test file references this class)
- `XML` (patterns: `com.json.XML`, `XMLTokener`, `class XML`) — **0 matches**
- `XMLTokener` — **0 matches**

The only test files in the project are:
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

None of these files reference `JSONWriter`, `XML`, or `XMLTokener`.

---

## Findings

**A86-1 | Severity: HIGH | Zero test coverage for all three vendored JSON/XML classes**

`JSONWriter`, `XML`, and `XMLTokener` have no test coverage whatsoever. The project's test suite contains only four test classes, all in the `com/calibration` and `com/util` packages. No test class references `com.json.JSONWriter`, `com.json.XML`, or `com.json.XMLTokener`. Although these are vendored third-party classes, the application relies on their correct behaviour for JSON serialisation and XML-to-JSON conversion; regressions introduced by package-level modifications or future vendored upgrades would go undetected.

**A86-2 | Severity: MEDIUM | Deprecated constructor usage: `new Double(d)` in JSONWriter.java (line 303)**

`JSONWriter.value(double d)` at line 303 calls `new Double(d)`, which is a deprecated constructor since Java 9 and removed in Java 17+. The preferred replacement is `Double.valueOf(d)`. Running this code on a modern JDK (17+) will cause a compilation error. There are no tests to catch this regression.

**A86-3 | Severity: MEDIUM | Deprecated constructor usage: `new Integer(0)` and `new Long(string)` in XML.java (lines 317, 337, 339)**

`XML.stringToValue()` uses `new Integer(0)` (line 317), `new Long(string)` (line 337), and `new Integer(myLong.intValue())` (line 339). These constructors are deprecated since Java 9 and removed in Java 17+. The preferred replacements are `Integer.valueOf(0)`, `Long.valueOf(string)`, and `Integer.valueOf(myLong.intValue())`. No tests exist to validate this method's behaviour or catch failures on newer JDKs.

**A86-4 | Severity: MEDIUM | Raw type `java.util.HashMap` used for `entity` field in XMLTokener.java (line 39)**

`XMLTokener.entity` is declared as a raw `java.util.HashMap` (no generic type parameters). This produces unchecked warnings at compile time and bypasses compile-time type safety. The field is `public static final`, meaning all callers can read it directly and could inadvertently interact with it as an untyped map. The correct declaration would be `HashMap<String, Object>` or `HashMap<String, Character>`.

**A86-5 | Severity: MEDIUM | `XML.parse()` silently discards malformed CDATA prefix: incomplete `<!-` comment never throws (XML.java lines 155-161)**

In `XML.parse()`, when the token is `BANG` and the next character is `-`, the code checks if the character after that is also `-` to detect `<!--`. If the second character is not `-`, `x.back()` is called and parsing continues into the generic `<!...>` scanning loop. A string like `<!-garbage>` is silently consumed rather than raising a syntax error. This is a correctness ambiguity with no test exercising the edge case.

**A86-6 | Severity: MEDIUM | `XMLTokener.nextContent()` trims leading whitespace but only skips to first non-whitespace before detecting end-of-input (XMLTokener.java lines 95-99)**

`nextContent()` loops `do { c = next(); } while (Character.isWhitespace(c))`. If the source consists entirely of whitespace, `next()` will eventually return the NUL character `0`, which then correctly returns `null`. However, content text that begins with whitespace has that leading whitespace stripped silently before the caller receives it, with no documented test confirming this intentional behaviour is exercised or regression-protected.

**A86-7 | Severity: LOW | `JSONWriter.maxdepth` increased to 200 from upstream default of 20**

The class-level Javadoc comment at line 52 states "Objects and arrays can be nested up to 20 levels deep," but the `maxdepth` field at line 60 is set to `200`. This is a discrepancy between documentation and implementation. It is unclear whether this value was intentionally changed (as a vendored modification) or is a copy-paste oversight. No tests validate deep nesting behaviour or the documented/actual limit.

**A86-8 | Severity: LOW | `XML.noSpace()` is `public` but only intended for internal XML tag validation; no tests guard its contract**

`XML.noSpace(String string)` is declared `public static` but its Javadoc describes it purely as an internal guard for tag names and attributes. It is called by `JSONML.java` but never tested. Its contract includes throwing `JSONException` for both empty strings and strings containing any whitespace character; neither branch has any automated test coverage.

**A86-9 | Severity: LOW | `XMLTokener.entity` map is mutable and public; callers can corrupt the entity table at runtime**

The `entity` field is `public static final java.util.HashMap`. The `final` modifier prevents reassignment of the reference but does not prevent callers from invoking `entity.put(...)` or `entity.remove(...)` to alter entity mappings at runtime. This could silently corrupt XML entity resolution for all subsequent uses of `XMLTokener` within the JVM. There are no tests and no defensive copying or unmodifiable-map wrapping in place.

**A86-10 | Severity: LOW | Vendored library version is outdated (version strings: 2011-11-24 and 2010-12-24 / 2011-02-11)**

`JSONWriter.java` carries version `2011-11-24`, `XML.java` carries `2011-02-11`, and `XMLTokener.java` carries `2010-12-24`. The org.json library has received numerous bug fixes and CVE patches since these dates (including fixes for XXE-adjacent parsing edge cases). Since the source is vendored rather than managed via a dependency tool (Maven/Gradle), updates require manual re-vendoring, and there is no automated mechanism to detect that the vendored copy has fallen behind. No tests exist to detect behavioural regressions that might arise from stale library code.

**A86-11 | Severity: INFO | These are vendored third-party classes with no application-specific modifications detected**

Beyond the package rename from `org.json` to `com.json`, no application-specific logic changes were found in any of the three files. All code matches the expected org.json reference implementation structure. The absence of modifications reduces the risk of bespoke bugs but does not eliminate the coverage gap for exercising the classes in context.

**A86-12 | Severity: INFO | `JSONWriter` is subclassed by `JSONStringer` in the same vendored package**

`JSONStringer` (also in `com/json/`) extends `JSONWriter` and overrides the `writer` field with a `StringWriter`. Neither `JSONWriter` nor `JSONStringer` has any test coverage in the project.

---

## Summary Table

| ID | Severity | Description |
|---|---|---|
| A86-1 | HIGH | Zero test coverage for all three classes |
| A86-2 | MEDIUM | `new Double(d)` deprecated constructor in JSONWriter (line 303) |
| A86-3 | MEDIUM | `new Integer()`/`new Long()` deprecated constructors in XML.stringToValue (lines 317, 337, 339) |
| A86-4 | MEDIUM | Raw `HashMap` type for `XMLTokener.entity` field (line 39) |
| A86-5 | MEDIUM | Silent consumption of malformed `<!-` (non-comment) in XML.parse() |
| A86-6 | MEDIUM | Leading whitespace silently stripped in XMLTokener.nextContent() with no tests |
| A86-7 | LOW | Javadoc says max depth 20 but implementation uses 200 in JSONWriter |
| A86-8 | LOW | `XML.noSpace()` is public but untested; contract not regression-protected |
| A86-9 | LOW | `XMLTokener.entity` is a mutable public static map; entity table can be corrupted at runtime |
| A86-10 | LOW | Vendored library dates from 2010-2011; no mechanism to detect or enforce updates |
| A86-11 | INFO | No application-specific modifications detected beyond package rename |
| A86-12 | INFO | `JSONWriter` is subclassed by `JSONStringer`; neither has tests |
