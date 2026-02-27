# Pass 4 – Code Quality Audit: Agent A24
**Audit run:** 2026-02-26-01
**Agent:** A24
**Date completed:** 2026-02-27

---

## Assigned Files

1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/PreStartHelpItem.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/PreStartQuestionItem.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/RefreshTokenItem.java`

---

## Step 1: Reading Evidence

### File 1 – PreStartHelpItem.java

**Class:** `PreStartHelpItem implements Serializable`

**Methods (exhaustive):**
| Line | Method |
|------|--------|
| 22   | `PreStartHelpItem()` – no-arg constructor |
| 25   | `PreStartHelpItem(JSONObject jsonObject) throws JSONException` – JSON-deserialisation constructor |

**Fields (public):**
| Line | Field | Type |
|------|-------|------|
| 14   | `id` | `int` |
| 15   | `input_order` | `int` |
| 16   | `input_type` | `String` |
| 17   | `input_label` | `String` |
| 18   | `input_value` | `String` |
| 19   | `input_image` | `String` |
| 20   | `expected_answer` | `String` |

**Types / constants / enums / interfaces:** none beyond the class itself.

**Imports:**
- `org.json.JSONException` (used)
- `org.json.JSONObject` (used)
- `java.io.Serializable` (used)
- `org.json.JSONArray` (unused – nothing in this file reads a JSONArray)
- `java.util.ArrayList` (unused)
- `java.math.BigDecimal` (unused)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` (self-package wildcard – unused / redundant)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` (unused)

---

### File 2 – PreStartQuestionItem.java

**Class:** `PreStartQuestionItem implements Serializable`

**Methods (exhaustive):**
| Line | Method |
|------|--------|
| 18   | `PreStartQuestionItem()` – no-arg constructor |
| 21   | `PreStartQuestionItem(JSONObject jsonObject) throws JSONException` – JSON-deserialisation constructor |

**Fields (public):**
| Line | Field | Type |
|------|-------|------|
| 14   | `id` | `int` |
| 15   | `content` | `String` |
| 16   | `expectedanswer` | `String` |

**Types / constants / enums / interfaces:** none beyond the class itself.

**Imports:**
- `org.json.JSONException` (used)
- `org.json.JSONObject` (used)
- `java.io.Serializable` (used)
- `org.json.JSONArray` (unused)
- `java.util.ArrayList` (unused)
- `java.math.BigDecimal` (unused)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` (self-package wildcard – unused / redundant)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` (unused)

---

### File 3 – RefreshTokenItem.java

**Class:** `RefreshTokenItem implements Serializable`

**Methods (exhaustive):**
| Line | Method |
|------|--------|
| 17   | `RefreshTokenItem()` – no-arg constructor |
| 20   | `RefreshTokenItem(JSONObject jsonObject) throws JSONException` – JSON-deserialisation constructor |

**Fields (public):**
| Line | Field | Type |
|------|-------|------|
| 14   | `value` | `String` |
| 15   | `expiration` | `int` |

**Types / constants / enums / interfaces:** none beyond the class itself.

**Imports:**
- `org.json.JSONException` (used)
- `org.json.JSONObject` (used)
- `java.io.Serializable` (used)
- `org.json.JSONArray` (unused)
- `java.util.ArrayList` (unused)
- `java.math.BigDecimal` (unused)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` (self-package wildcard – unused / redundant)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` (unused)

---

## Step 2 & 3: Findings

---

### A24-1 · MEDIUM · Unused imports in all three files (build warnings)

**Affected files:** All three files, lines 6–10 of each.

Each file carries an identical block of five imports that are not referenced anywhere within the file body:

```java
import org.json.JSONArray;          // line 6 – unused
import java.util.ArrayList;         // line 7 – unused
import java.math.BigDecimal;        // line 8 – unused
import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*;   // line 9 – self-package wildcard, unused
import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*; // line 10 – unused
```

These five lines are identical across all three files. The Android build toolchain (and every Java IDE) flags unused imports as warnings. The self-package wildcard (`webserviceclasses.*` inside a class that already lives in `webserviceclasses`) is redundant. The `BigDecimal`, `ArrayList`, and `JSONArray` imports are vestiges of a copy-paste template never cleaned up. This pattern appears to be a project-wide copy-paste artefact (confirmed in `AnswerItem.java`, `CompanyItem.java`, `EquipmentStatsItem.java`, and others), indicating a systemic style problem rather than isolated mistakes.

---

### A24-2 · MEDIUM · All public fields expose mutable state directly (leaky abstraction / style)

**Affected files:** All three files.

Every field across all three classes is declared `public` with no accessor methods:

```java
// PreStartHelpItem.java lines 14-20
public int id;
public int input_order;
public String input_type;
public String input_label;
public String input_value;
public String input_image;
public String expected_answer;

// PreStartQuestionItem.java lines 14-16
public int id;
public String content;
public String expectedanswer;

// RefreshTokenItem.java lines 14-15
public String value;
public int expiration;
```

Callers can freely mutate these fields after construction, bypassing any intended invariants. While this pattern is common in DTO/value-object classes in this project (confirmed by inspection of sibling classes), it contradicts the Java convention of using private fields with accessors and makes future refactoring (e.g., adding validation, caching, or serialisation annotations) difficult without breaking the API. This is a leaky abstraction: the internal JSON key mapping (snake_case keys such as `input_order`, `input_type`) is now part of the public surface.

---

### A24-3 · MEDIUM · Inconsistent field naming convention between sister classes

**Affected files:** `PreStartHelpItem.java` and `PreStartQuestionItem.java`.

`PreStartHelpItem` uses `expected_answer` (snake_case, mirroring the JSON key directly):
```java
// PreStartHelpItem.java line 20
public String expected_answer;
```

`PreStartQuestionItem` stores the semantically equivalent concept as `expectedanswer` (all-lowercase, no separator):
```java
// PreStartQuestionItem.java line 16
public String expectedanswer;
```

Neither follows the Java camelCase convention (`expectedAnswer`). The inconsistency between snake_case in one class and run-together lowercase in the other makes it harder to search across the codebase and violates the Java coding standard (JLS §6.1). The corresponding JSON key in `PreStartQuestionItem` is also `"expectedanswer"` (line 36), meaning the JSON API itself uses a non-standard naming scheme that has leaked into the field names.

---

### A24-4 · LOW · `expiration` typed as `int` may silently truncate a Unix timestamp

**Affected file:** `RefreshTokenItem.java`, line 15.

```java
public int expiration;
// ...
expiration = jsonObject.getInt("expiration");   // line 32
```

OAuth refresh-token expiration values are typically Unix epoch timestamps (seconds since 1970-01-01). A signed 32-bit `int` overflows on 19 January 2038 (the Y2K38 problem). If the server ever returns a timestamp larger than `Integer.MAX_VALUE` (2,147,483,647), `JSONObject.getInt()` will throw a `JSONException` or silently truncate the value depending on the org.json version in use. A `long` would be the safe choice. Note that the field is populated in `GetTokenResult` but no downstream caller was found that reads `refreshToken.expiration` directly, so the runtime impact is currently nil, but the latent defect exists.

---

### A24-5 · LOW · `PreStartHelpItem` class with its `PreStartHelpResultArray` container appears unused at the UI layer

**Affected file:** `PreStartHelpItem.java`.

A codebase-wide search found that `PreStartHelpItem` is only referenced inside `PreStartHelpResultArray.java` (its result container). `PreStartHelpResultArray` itself is never imported or referenced outside its own definition file. There is no UI fragment, adapter, or service that invokes the web-service call that would return this type. This suggests that either the "pre-start help" feature was planned but not yet implemented in the UI, or the call site was removed and the DTO is now dead code.

---

### A24-6 · LOW · Trailing whitespace on blank separator lines inside constructors

**Affected files:** All three files.

The blank lines used as visual separators between `if`-blocks inside the JSON-deserialisation constructors contain trailing whitespace (a single tab character, visible in the raw source at e.g. `PreStartHelpItem.java` lines 29, 34, 39, 44, 49, 54, 59). This is a style/hygiene issue that causes unnecessary noise in diffs and may trigger lint or pre-commit hooks.

---

## Summary Table

| ID     | Severity | File(s)                               | Description |
|--------|----------|---------------------------------------|-------------|
| A24-1  | MEDIUM   | All three files (lines 6–10 each)     | Five identical unused/redundant imports in every file – build warnings |
| A24-2  | MEDIUM   | All three files                       | All fields public and mutable – leaky abstraction, no encapsulation |
| A24-3  | MEDIUM   | PreStartHelpItem, PreStartQuestionItem | Inconsistent naming: `expected_answer` vs `expectedanswer` – neither is camelCase |
| A24-4  | LOW      | RefreshTokenItem.java line 15         | `expiration` as `int` will overflow for post-2038 Unix timestamps |
| A24-5  | LOW      | PreStartHelpItem.java                 | Class and its result container appear unreachable from any UI caller (potential dead code) |
| A24-6  | LOW      | All three files                       | Trailing whitespace on blank separator lines inside constructors |

No CRITICAL or HIGH findings. No commented-out code blocks were present. No `@SuppressWarnings` annotations were present. No deprecated API usage was identified within these files. No TODO/FIXME markers were present.
