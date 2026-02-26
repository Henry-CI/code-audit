# Pass 2 Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A102
**Date:** 2026-02-26
**Source Files Audited:**
1. `src/main/java/com/util/actionSubmitForm.java`
2. `src/main/java/com/util/BarCode.java`
3. `src/main/java/com/util/BeanComparator.java`

**Test Directory:** `src/test/java/`

---

## Test Directory Inventory

The following test files exist in the test directory:

- `src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java`
- `src/test/java/com/calibration/UnitCalibrationTest.java`
- `src/test/java/com/calibration/UnitCalibratorTest.java`
- `src/test/java/com/util/ImpactUtilTest.java`

**Grep results for `actionSubmitForm` / `ActionSubmitForm` in test directory:** No matches found.
**Grep results for `BarCode` / `barcode` / `Barcode` in test directory:** No matches found.
**Grep results for `BeanComparator` in test directory:** No matches found.

---

## Source File 1: actionSubmitForm.java

### Reading Evidence

**Class name:** `actionSubmitForm`
**Package:** `com.util`
**Extends:** `org.apache.struts.taglib.html.FormTag`
**File comment (line 7):** `// Currently Unused because of introduce of watermaker jquery lib`

**Fields:**
| Field | Line | Type | Visibility |
|---|---|---|---|
| `log` | 9 | `Logger` (log4j) | `private static` |

**Methods:**
| Method | Line | Return Type | Visibility |
|---|---|---|---|
| `renderFormStartElement()` | 11 | `String` | `protected` |

**Inherited calls within `renderFormStartElement()`:**
- `renderName(results)` — line 16 (inherited from `FormTag`; exception caught and logged)
- `renderAttribute(results, "method", ...)` — line 21
- `renderAction(results)` — line 22
- `renderAttribute(results, "accept-charset", ...)` — line 23
- `renderAttribute(results, "class", ...)` — line 24
- `renderAttribute(results, "enctype", ...)` — line 25
- `renderAttribute(results, "onreset", ...)` — line 26
- `renderAttribute(results, "style", ...)` — line 28
- `renderAttribute(results, "target", ...)` — line 29
- `renderOtherAttributes(results)` — line 31

### Coverage Assessment

No test class exists for `actionSubmitForm`. Zero test coverage.

---

## Source File 2: BarCode.java

### Reading Evidence

**Class name:** `BarCode`
**Package:** `com.util`

**Fields (static constants):**
| Field | Line | Value |
|---|---|---|
| `log` | 30 | `Logger` (log4j), `private static` |
| `BARCODE_MSG` | 32 | `"msg"`, `public static final String` |
| `BARCODE_TYPE` | 34 | `"type"`, `public static final String` |
| `BARCODE_HEIGHT` | 36 | `"height"`, `public static final String` |
| `BARCODE_MODULE_WIDTH` | 38 | `"mw"`, `public static final String` |
| `BARCODE_WIDE_FACTOR` | 40 | `"wf"`, `public static final String` |
| `BARCODE_QUIET_ZONE` | 42 | `"qz"`, `public static final String` |
| `BARCODE_HUMAN_READABLE_POS` | 44 | `"hrp"`, `public static final String` |
| `BARCODE_FORMAT` | 46 | `"fmt"`, `public static final String` |
| `BARCODE_IMAGE_RESOLUTION` | 48 | `"res"`, `public static final String` |
| `BARCODE_IMAGE_GRAYSCALE` | 50 | `"gray"`, `public static final String` |
| `BARCODE_HUMAN_READABLE_SIZE` | 52 | `"hrsize"`, `public static final String` |
| `BARCODE_HUMAN_READABLE_FONT` | 54 | `"hrfont"`, `public static final String` |
| `BARCODE_HUMAN_READABLE_PATTERN` | 56 | `"hrpattern"`, `public static final String` |

**Methods:**
| Method | Line | Return Type | Visibility |
|---|---|---|---|
| `genBarCode(HttpServletRequest, String)` | 58 | `String` | `public` |
| `determineFormat(HttpServletRequest)` | 145 | `String` | `protected` |
| `buildCfg(HttpServletRequest)` | 162 | `Configuration` | `protected` |

### Coverage Assessment

No test class exists for `BarCode`. Zero test coverage.

---

## Source File 3: BeanComparator.java

### Reading Evidence

**Class name:** `BeanComparator`
**Package:** `com.util`
**Implements:** `java.util.Comparator` (raw type)

**Fields:**
| Field | Line | Type | Visibility |
|---|---|---|---|
| `EMPTY_CLASS_ARRAY` | 22 | `Class[]` | `private static final` |
| `EMPTY_OBJECT_ARRAY` | 23 | `Object[]` | `private static final` |
| `method` | 25 | `Method` | `private` |
| `isAscending` | 26 | `boolean` | `private` |
| `isIgnoreCase` | 27 | `boolean` | `private` |
| `isNullsLast` | 28 | `boolean` (default `true`) | `private` |

**Methods:**
| Method | Line | Return Type | Visibility |
|---|---|---|---|
| `BeanComparator(Class<?>, String)` | 34 | constructor | `public` |
| `BeanComparator(Class<?>, String, boolean)` | 42 | constructor | `public` |
| `BeanComparator(Class<?>, String, boolean, boolean)` | 51 | constructor | `public` |
| `setAscending(boolean)` | 82 | `void` | `public` |
| `setIgnoreCase(boolean)` | 90 | `void` | `public` |
| `setNullsLast(boolean)` | 98 | `void` | `public` |
| `compare(Object, Object)` | 107 | `int` | `public` |

### Coverage Assessment

No test class exists for `BeanComparator`. Zero test coverage.

---

## Findings

### actionSubmitForm

**A102-1 | Severity: CRITICAL | `actionSubmitForm` has zero test coverage — no test class exists anywhere in the test suite**
The class `actionSubmitForm` (extending `org.apache.struts.taglib.html.FormTag`) has no corresponding test file. The single overridden method `renderFormStartElement()` is completely untested.

**A102-2 | Severity: HIGH | `renderFormStartElement()` exception path for `renderName()` (line 17-20) is untested**
The `JspException` catch block swallows the exception after logging it via `InfoLogger.logException`. There is no test verifying that this catch path executes correctly or that the method still returns a usable result after the exception — the output buffer may contain a partially constructed `<form>` element.

**A102-3 | Severity: HIGH | No test for `renderFormStartElement()` default method fallback — `getMethod() == null` branch (line 21) is untested**
The ternary `getMethod() == null ? "post" : getMethod()` at line 21 is untested. No test verifies the `null` case defaults to `"post"`, nor that a non-null method value is rendered correctly.

**A102-4 | Severity: MEDIUM | No test verifies the suppressed `onsubmit` attribute (line 27)**
The `onsubmit` attribute is intentionally commented out (line 27) while an inline `onsubmit='clearPlaceholders(this);'` is hard-coded into the opening `<form>` tag (line 13). No test confirms this hard-coded handler is present in the output and that the original Struts `getOnsubmit()` value is correctly suppressed.

**A102-5 | Severity: LOW | Class declared as "Currently Unused" (line 7) with no deprecation annotation or Javadoc**
The file comment states the class is unused. No `@Deprecated` annotation or `@deprecated` Javadoc tag is present. The class remains in the production source tree without documentation of the intended removal path.

---

### BarCode

**A102-6 | Severity: CRITICAL | `BarCode` has zero test coverage — no test class exists anywhere in the test suite**
All three methods (`genBarCode`, `determineFormat`, `buildCfg`) are completely untested.

**A102-7 | Severity: CRITICAL | Path traversal risk in `genBarCode()` — file path constructed from user-supplied `msg` parameter (lines 123-124) is untested**
The bitmap output path is constructed as `curerntDir + "/../../../../../images/barcode/" + img + ".png"` where `img` is derived directly from the request parameter `msg` after only superficial sanitisation (stripping a trailing `#`, stripping a leading `%`, and stripping a `$%` prefix). There is no test confirming that directory traversal sequences (e.g., `../`, `%2F`) in `msg` are blocked. This is both a security gap and a testing gap.

**A102-8 | Severity: CRITICAL | `genBarCode()` silently swallows all exceptions (lines 135-141) — no test exercises error return behaviour**
Both the `catch (Exception e)` and `catch (Throwable t)` blocks log and print the error but return `bout.toString()` — which at that point is an empty or partial string — with no indication to the caller that generation failed. No test verifies what is returned on failure, nor confirms logging occurs.

**A102-9 | Severity: HIGH | `genBarCode()` resolution validation branches (lines 98-105) are untested**
Two `IllegalArgumentException` throws guard resolutions above 2400 dpi and below 10 dpi. Neither boundary (exactly 2400, exactly 10, and out-of-range values) is tested. Because the exception is caught by the outer `catch (Exception e)` block, the caller receives an empty string with no exception propagation — this silent failure is also untested.

**A102-10 | Severity: HIGH | `genBarCode()` SVG format branch (lines 75-85) is untested**
The SVG code path instantiates `SVGCanvasProvider`, performs a DOM transformation, and serialises XML to `bout`. No test exists for this path, including transformer error handling.

**A102-11 | Severity: HIGH | `genBarCode()` EPS format branch (lines 86-89) is untested**
The EPS path (`EPSCanvasProvider`) and its `finish()` call are completely untested. No test verifies correct EPS output or handling of `finish()` failure.

**A102-12 | Severity: HIGH | `genBarCode()` bitmap format branch (lines 90-130) is untested**
The bitmap path performs `FileOutputStream` creation, bitmap generation, and `provider.finish()`. No test verifies: successful file creation, correct pixel format (`TYPE_BYTE_GRAY`), correct dpi, or I/O error handling.

**A102-13 | Severity: HIGH | `genBarCode()` msg string manipulation logic (lines 108-121) is untested**
Three sequential string mutations are applied to `msg` before file creation:
- Trailing `#` stripped (line 110)
- `$%` prefix handling (line 115): uses `img.indexOf("%")+1` which would return index 0 if `%` is not found (since `indexOf` returns -1, +1 = 0), silently producing wrong output
- Leading `%` stripped (line 119)
None of these branches, including the off-by-one risk at line 115, has any test coverage.

**A102-14 | Severity: HIGH | `genBarCode()` null/empty `msg` early-return branch (lines 67-69) is untested**
The early return of `""` for a null or blank `msg` is untested. No test confirms that an empty message produces an empty string rather than attempting barcode generation.

**A102-15 | Severity: MEDIUM | `determineFormat()` (lines 145-153) is untested**
No tests cover: a null `fmt` parameter (should default to SVG), a valid `fmt` value that `MimeTypes.expandFormat()` recognises, or an unrecognised `fmt` value whose expansion returns null.

**A102-16 | Severity: MEDIUM | `buildCfg()` optional parameter assembly (lines 162-242) is entirely untested**
The method conditionally builds `height`, `module-width`, `wide-factor`, `quiet-zone`, `human-readable` (with `pattern`, `font-size`, `font-name`, `placement`) sub-configurations based on the presence of request parameters. No test verifies that parameters present in the request are reflected in the returned `Configuration`, nor that absent parameters are correctly omitted.

**A102-17 | Severity: MEDIUM | `buildCfg()` quiet-zone `"disable"` prefix branch (line 195) is untested**
The branch `if (quietZone.startsWith("disable"))` sets `enabled="false"` as an XML attribute rather than a value. No test confirms this special sentinel value is handled correctly vs. a numeric quiet-zone value.

**A102-18 | Severity: MEDIUM | `buildCfg()` default barcode type fallback `"code128"` (line 167) is untested**
No test verifies that when the `type` request parameter is absent, the default `"code128"` type is used as the root child configuration element.

**A102-19 | Severity: LOW | `typo in variable name` `curerntDir` (line 123) — no test would catch silent misspelling**
The variable `curerntDir` (should be `currentDir`) does not cause a runtime error, but no test exercises the file path construction, so this defect would not be caught by tests.

**A102-20 | Severity: LOW | `genBarCode()` orientation is hard-coded to `0` (line 63) with no way to configure it via request parameters — untested and undocumented limitation**
The orientation value is always `0` regardless of any request parameter. No test confirms this constraint or documents it as intentional.

---

### BeanComparator

**A102-21 | Severity: CRITICAL | `BeanComparator` has zero test coverage — no test class exists anywhere in the test suite**
All constructors, setters, and the `compare()` method are completely untested.

**A102-22 | Severity: HIGH | Constructor validation — `NoSuchMethodException` path (lines 62-66) is untested**
When a non-existent method name is supplied, the constructor wraps the `NoSuchMethodException` in an `IllegalArgumentException`. No test verifies this exception is thrown with the correct message format (`methodName + "() method does not exist"`).

**A102-23 | Severity: HIGH | Constructor validation — void return type rejection (lines 70-76) is untested**
When the resolved method has a `void` return type, the constructor throws `IllegalArgumentException`. No test exercises this guard.

**A102-24 | Severity: HIGH | `compare()` reflection invocation exception path (lines 117-120) is untested**
If `method.invoke()` throws (e.g., `IllegalAccessException`, `InvocationTargetException`), the code rethrows it wrapped in `RuntimeException`. No test exercises this path.

**A102-25 | Severity: HIGH | `compare()` null-handling with `isNullsLast=false` (line 138-140) is untested**
The `setNullsLast(false)` configuration inverts null ordering. No test verifies that setting `isNullsLast` to `false` reverses the position of null values in the sort output.

**A102-26 | Severity: HIGH | `compare()` descending sort order (lines 153-156) is untested**
The swap of `c1`/`c2` when `isAscending=false` reverses sort order. No test confirms that descending sort produces the correct inverted ordering.

**A102-27 | Severity: HIGH | `compare()` case-sensitive String comparison path (lines 161-164) is untested**
When `isIgnoreCase=false` and both values are `String`, the code falls into the `((Comparable)c1).compareTo(c2)` branch (not `compareToIgnoreCase`). No test verifies case-sensitive ordering.

**A102-28 | Severity: MEDIUM | `compare()` non-Comparable type path (lines 166-172) is untested**
For objects that do not implement `Comparable`, the code falls back to `toString()` comparison. No test exercises this path with a type that is not `Comparable`.

**A102-29 | Severity: MEDIUM | `compare()` empty-string-treated-as-null behaviour (lines 124-132) is untested**
The logic that converts empty `String` fields to `null` before comparison is untested. No test confirms that an empty-string field sorts identically to a `null` field.

**A102-30 | Severity: MEDIUM | `compare()` both-null case returning `0` (line 136) is untested**
No test verifies that two objects with null (or empty-string) fields compare as equal.

**A102-31 | Severity: MEDIUM | Three-constructor chain delegation (lines 34-45) is untested**
The two-argument and three-argument constructors delegate to the four-argument constructor with default values. No test confirms that the defaults (`isAscending=true`, `isIgnoreCase=true`, `isNullsLast=true`) are correctly applied when using the shorter constructors.

**A102-32 | Severity: MEDIUM | `setAscending()`, `setIgnoreCase()`, `setNullsLast()` post-construction mutation is untested**
All three setters allow changing sort properties after construction. No test verifies that mutating these properties after construction and before sorting correctly affects `compare()` output.

**A102-33 | Severity: LOW | Raw `Comparator` type (line 20) suppresses generic type safety — untested behaviour with mixed types**
`BeanComparator implements Comparator` uses a raw type, meaning the compiler cannot enforce type safety. A `ClassCastException` at line 162 (`(String)c2` when `c1` is `String` but `c2` is not) would only be caught at runtime. No test exercises mixed-type invocations.

**A102-34 | Severity: LOW | `compare()` non-Comparable, case-sensitive String fallback (line 171) is untested**
When a non-Comparable type with `isIgnoreCase=false` is compared, the code uses `c1.toString().compareTo(c2.toString())`. This path is not reachable via the `Comparable` branch and requires a specific non-Comparable type with case-significant `toString()` output; it is untested.

---

## Summary Table

| Finding | Class | Severity | Category |
|---|---|---|---|
| A102-1 | actionSubmitForm | CRITICAL | No test class |
| A102-2 | actionSubmitForm | HIGH | Untested exception path |
| A102-3 | actionSubmitForm | HIGH | Untested null branch |
| A102-4 | actionSubmitForm | MEDIUM | Untested suppressed attribute |
| A102-5 | actionSubmitForm | LOW | Missing deprecation marking |
| A102-6 | BarCode | CRITICAL | No test class |
| A102-7 | BarCode | CRITICAL | Path traversal, untested sanitisation |
| A102-8 | BarCode | CRITICAL | Silent exception swallow, untested |
| A102-9 | BarCode | HIGH | Untested resolution boundary guards |
| A102-10 | BarCode | HIGH | Untested SVG branch |
| A102-11 | BarCode | HIGH | Untested EPS branch |
| A102-12 | BarCode | HIGH | Untested bitmap/file I/O branch |
| A102-13 | BarCode | HIGH | Untested msg string mutations, off-by-one risk |
| A102-14 | BarCode | HIGH | Untested null/empty msg early return |
| A102-15 | BarCode | MEDIUM | Untested determineFormat() |
| A102-16 | BarCode | MEDIUM | Untested buildCfg() optional parameters |
| A102-17 | BarCode | MEDIUM | Untested quiet-zone disable sentinel |
| A102-18 | BarCode | MEDIUM | Untested default type fallback |
| A102-19 | BarCode | LOW | Typo in variable name, no test coverage |
| A102-20 | BarCode | LOW | Hard-coded orientation, untested |
| A102-21 | BeanComparator | CRITICAL | No test class |
| A102-22 | BeanComparator | HIGH | Untested NoSuchMethodException constructor path |
| A102-23 | BeanComparator | HIGH | Untested void-return-type constructor guard |
| A102-24 | BeanComparator | HIGH | Untested reflection invoke exception |
| A102-25 | BeanComparator | HIGH | Untested isNullsLast=false behaviour |
| A102-26 | BeanComparator | HIGH | Untested descending sort |
| A102-27 | BeanComparator | HIGH | Untested case-sensitive String comparison |
| A102-28 | BeanComparator | MEDIUM | Untested non-Comparable fallback path |
| A102-29 | BeanComparator | MEDIUM | Untested empty-string-as-null treatment |
| A102-30 | BeanComparator | MEDIUM | Untested both-null equals-zero case |
| A102-31 | BeanComparator | MEDIUM | Untested constructor chaining defaults |
| A102-32 | BeanComparator | MEDIUM | Untested post-construction setter mutation |
| A102-33 | BeanComparator | LOW | Raw Comparator type, mixed-type ClassCastException untested |
| A102-34 | BeanComparator | LOW | Untested non-Comparable case-sensitive toString path |

**Total findings: 34**
- CRITICAL: 6
- HIGH: 15
- MEDIUM: 10
- LOW: 5
