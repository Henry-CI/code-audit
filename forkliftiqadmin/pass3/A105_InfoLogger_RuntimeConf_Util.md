# Pass 3 Documentation Audit — A105
**Audit run:** 2026-02-26-01
**Agent:** A105
**Files:** util/InfoLogger.java, util/RuntimeConf.java, util/Util.java

---

## 1. Reading Evidence

### 1.1 InfoLogger.java
- **Class:** `InfoLogger` (line 14)
- **Fields:** none declared as instance/static fields; static initialiser block at lines 15-24
- **Methods:**
  - `getFileURL(final String s)` — public instance, line 26
  - `getLogger(final String c)` — public static, line 35
  - `logException(Logger log, final Exception e)` — public static, line 44

### 1.2 RuntimeConf.java
- **Class:** `RuntimeConf` (line 3)
- **Fields (all `public static`):**

| Name | Type | Line |
|------|------|------|
| `projectTitle` | String | 4 |
| `database` | String | 5 |
| `emailFrom` | String | 6 |
| `emailFromLinde` | String | 7 |
| `url` | String | 8 |
| `ERROR_PAGE` | String | 9 |
| `EXPIRE_PAGE` | String | 10 |
| `DEFAUTL_TIMEZONE` | String | 11 |
| `HOUR_METER` | String | 12 |
| `REGISTER_SUBJECT` | String | 13 |
| `UPDATE_APP_SUBJECT` | String | 14 |
| `UPGRADE_CONTENT` | String | 15 |
| `RECEIVER_EMAIL` | String | 16 |
| `EMAIL_IMPORT_TITLE` | String | 17 |
| `EMAIL_RESET_TITLE` | String | 18 |
| `EMAIL_COMMENT_TITLE` | String | 19 |
| `EMAIL_DIGANOSTICS_TITLE` | String | 20 |
| `API_LOGIN` | String | 22 |
| `API_VEHICLE` | String | 23 |
| `API_DRIVER` | String | 24 |
| `API_ATTACHMENT` | String | 25 |
| `API_QUESTION` | String | 26 |
| `API_RESULT` | String | 27 |
| `API_PDFRPT` | String | 28 |
| `API_BARCODE` | String | 29 |
| `API_INVALID` | String | 30 |
| `Load_BARCODE` | String | 31 |
| `UPLOAD_FOLDER` | String | 32 |
| `BROCHURE_FOLDER` | String | 33 |
| `XML_FOLDER` | String | 34 |
| `IMG_SRC` | String | 35 |
| `COMP` | String | 36 |
| `PDF_FOLDER` | String | 37 |
| `RESULT_FAIL` | String | 40 |
| `RESULT_OK` | String | 41 |
| `RESULT_INCOMPLETE` | String | 42 |
| `ROLE_COMP` | String | 44 |
| `ROLE_SYSADMIN` | String | 45 |
| `ROLE_DEALER` | String | 46 |
| `ROLE_SUBCOMP` | String | 47 |
| `ROLE_SITEADMIN` | String | 48 |
| `CHECKLIST_SECONDS` | long | 50 |
| `DEFAULT_SCANNERTIME` | String | 51 |
| `LINDEDB` | String | 53 |
| `LINDERPTTITLE` | String | 54 |
| `EMPTYLOGO` | String | 55 |
| `emailContent` | String | 57 |
| `debugEmailRecipet` | String | 58 |
| `APIURL` | String | 60 |
| `file_type` | String | 61 |
| `cloudImageURL` | String | 62 |
| `v_user` | String (final) | 64 |
| `HTTP_OK` | Integer (final) | 66 |

- **Methods:** none

### 1.3 Util.java
- **Class:** `Util` (line 30)
- **Fields:** none declared
- **Methods:**

| Name | Signature | Line |
|------|-----------|------|
| `sendMail` (6-arg) | public static boolean | 32 |
| `sendMail` (8-arg, with attachment) | public static boolean | 73 |
| `getHTML` | public static String | 134 |
| `genPass` | public static String | 159 |
| `checkedValueRadio` | public static String | 179 |
| `checkedValueCheckbox` | public static String | 191 |
| `ArraListToString` | public static String @Deprecated | 204 |
| `selectRoleBox` | public static String | 210 |
| `getBarcodeTimeLst` | public static ArrayList<String> | 230 |
| `generateRadomName` | public static String | 258 |
| `nthOccurrence` | public static int | 268 |

---

## 2. Findings

### A105-1 — InfoLogger: no class-level Javadoc
**Severity:** LOW
**File:** util/InfoLogger.java, line 14
**Detail:** The block at lines 3-6 is a standard block comment (`/* ... */`), not a Javadoc comment (`/** ... */`). It will not be picked up by Javadoc tooling and does not appear above the class declaration (it precedes the import statements). The class has no Javadoc description of its purpose or thread-safety characteristics.

---

### A105-2 — InfoLogger.getFileURL: undocumented non-trivial public method
**Severity:** MEDIUM
**File:** util/InfoLogger.java, line 26
**Detail:** `getFileURL(final String s)` is a public method with no Javadoc. It is not a simple getter; it resolves a classpath-relative resource name to a `URL` using the class loader. There is no documentation of the expected format of the `s` parameter, what is returned when the resource is not found (returns `null` silently), or that the method is only used internally by the static initialiser. Additionally, the parameter name `s` is uninformative and undocumented.

---

### A105-3 — InfoLogger.getLogger: minor typo in @param description
**Severity:** LOW
**File:** util/InfoLogger.java, lines 31-34
**Detail:** The @param tag reads `@param c ClassName` (line 32). The word "ClassName" is not a description — it merely restates the type. More importantly, the Javadoc does not note that the method delegates directly to `Logger.getLogger(String)`, and the @return tag says only `Logger` with no elaboration (e.g., whether it can return null, whether a new Logger is created, etc.). The documentation is present but minimally useful.

---

### A105-4 — InfoLogger.logException: comment describes behaviour inaccurately
**Severity:** MEDIUM
**File:** util/InfoLogger.java, lines 39-43
**Detail:** The Javadoc states the exception is printed "to the log file". In reality the implementation calls both `e.printStackTrace(new PrintWriter(sw))` and `e.printStackTrace()` (line 47). The second call prints the stack trace to standard error (`System.err`), which is unrelated to the log file. The Javadoc fails to document this side-effect. Callers who rely solely on the documented behaviour may miss that the stack trace is also emitted to stderr in production.

---

### A105-5 — InfoLogger.logException: @return tag missing (method is void — acceptable), but @param type for `e` is overly restrictive
**Severity:** LOW
**File:** util/InfoLogger.java, lines 39-43
**Detail:** The parameter `e` is declared as `final Exception e`. The @param tag documents it as "Exception to be logged", which is accurate. However, many runtime errors extend `RuntimeException` or `Error` rather than `Exception`; the narrow signature means `Throwable` subclasses outside `Exception` cannot be passed. This is a design concern surfaced by documentation review, not a documentation inaccuracy per se, but is worth recording.

---

### A105-6 — RuntimeConf: no class-level Javadoc
**Severity:** LOW
**File:** util/RuntimeConf.java, line 3
**Detail:** The class has no Javadoc comment. There is no description of the class purpose, no note that all fields are mutable public statics (presenting a global-state concern), and no documentation of how or where these values are expected to be overridden at runtime.

---

### A105-7 — RuntimeConf: no field-level Javadoc on any field
**Severity:** LOW
**File:** util/RuntimeConf.java, lines 4-66
**Detail:** None of the 50 public static fields carries a Javadoc comment. Several fields have inline comments (e.g., `//live` on line 16, `//Super ADMIN` on line 45, `/*API method parameters*/` on line 21), but these are not Javadoc and will not appear in generated API documentation. Fields whose names contain obvious typos (see findings A105-8 and A105-9) are particularly in need of documentation to clarify intent.

---

### A105-8 — RuntimeConf: multiple typos in field names and values that represent semi-permanent API contracts
**Severity:** MEDIUM
**File:** util/RuntimeConf.java
**Detail:** The following identifiers contain spelling errors that are now baked into the public API surface of the class:

| Field | Line | Error |
|-------|------|-------|
| `DEFAUTL_TIMEZONE` | 11 | Should be `DEFAULT_TIMEZONE` |
| `UPGRADE_CONTENT` value `"Upgarde Request"` | 15 | Value misspelled: "Upgarde" |
| `EMAIL_DIGANOSTICS_TITLE` | 20 | Should be `DIAGNOSTICS` |
| `debugEmailRecipet` | 58 | Should be `debugEmailRecipient` |
| `generateRadomName` (Util.java, line 258) | — | See A105-17 |

Because these names are `public static` and referenced by name throughout the codebase, renaming them is a breaking change. The absence of any Javadoc noting the canonical/intended name amplifies the problem.

---

### A105-9 — RuntimeConf.DEFAUTL_TIMEZONE: value may not match application intent
**Severity:** LOW
**File:** util/RuntimeConf.java, line 11
**Detail:** The field `DEFAUTL_TIMEZONE = "Australia/Sydney"` hard-codes a timezone. There is no Javadoc explaining whether this is overridable at deployment, whether it is used as a fallback only, or which parts of the system consume it. The value itself may be technically correct for the original deployment target but constitutes undocumented configuration.

---

### A105-10 — RuntimeConf.CHECKLIST_SECONDS: no documentation of unit or purpose
**Severity:** LOW
**File:** util/RuntimeConf.java, line 50
**Detail:** `public static long CHECKLIST_SECONDS = 600` (10 minutes). There is no Javadoc or comment explaining what this timeout governs, whether 600 is seconds (as the name implies) or milliseconds, and whether it is configurable. The name implies seconds but the absence of documentation leaves this ambiguous for future maintainers.

---

### A105-11 — RuntimeConf.APIURL: hardcoded AWS EC2 hostname with no documentation
**Severity:** MEDIUM
**File:** util/RuntimeConf.java, line 60
**Detail:** `APIURL = "http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/"` is a hardcoded, non-TLS URL pointing to a specific EC2 instance. There is no Javadoc explaining what service is hosted there, that the URL should be overridden for different environments (dev/staging/production), or that the connection is unencrypted (HTTP, not HTTPS). This is a documentation gap with security implications.

---

### A105-12 — Util: no class-level Javadoc
**Severity:** LOW
**File:** util/Util.java, line 30
**Detail:** The `Util` class has no Javadoc comment. There is no description of its purpose, no note that all methods are static utilities, and no guidance on thread safety.

---

### A105-13 — Util.sendMail (6-arg): undocumented non-trivial public method
**Severity:** MEDIUM
**File:** util/Util.java, line 32
**Detail:** No Javadoc. The method sends an HTML email via JNDI-looked-up mail session. Notable undocumented behaviours:
- `rName` and `sName` parameters are accepted but never used in the implementation (dead parameters). Callers may waste effort constructing these values.
- Returns `false` if recipient parsing fails, but returns `true` even when `Transport.send()` throws (the exception is swallowed and the method still returns `true` from line 70). This asymmetric error-return behaviour is not documented.
- The `sEmail` null check at line 41 silently calls `message.setFrom()` (no-arg) rather than raising an error.

---

### A105-14 — Util.sendMail (8-arg, with attachment): undocumented non-trivial public method; different error-return behaviour from 6-arg overload
**Severity:** MEDIUM
**File:** util/Util.java, line 73
**Detail:** No Javadoc. In addition to the issues listed for the 6-arg overload, this variant differs in a significant undocumented way: when recipient parsing fails (line 90-92), it does NOT return `false` — it silently continues and attempts to send a message with no recipient. The 6-arg overload returns `false` in the same situation. This inconsistency between the two overloads is a potential defect that is invisible to callers because neither method is documented. The `attachment` parameter triggers a NullPointerException if passed as `null` (line 108 calls `attachment.equalsIgnoreCase("")`); this is not documented.

---

### A105-15 — Util.getHTML: undocumented non-trivial public method; undocumented timeout
**Severity:** MEDIUM
**File:** util/Util.java, line 134
**Detail:** No Javadoc. The method fetches the full body of an HTTP URL as a string. Notable undocumented behaviours:
- Read timeout is hardcoded to 900000 ms (15 minutes) with no connect timeout set.
- Returns an empty string `""` on any exception (all exceptions silently swallowed).
- Performs naive string concatenation in a loop (`result += line + "\n"`) rather than a StringBuilder, which is a performance concern for large responses; undocumented size limits.
- No documentation on whether HTTP redirects are followed.

---

### A105-16 — Util.genPass: undocumented non-trivial public method; misleading method name and undocumented return contract
**Severity:** MEDIUM
**File:** util/Util.java, line 159
**Detail:** No Javadoc. The method name `genPass` suggests password generation, but the implementation generates a hex substring of an MD5 digest seeded from random bytes. Notable undocumented behaviours:
- Returns `null` if MD5 is unavailable (line 167); callers are not warned.
- The `chars` parameter is an offset into the hex string; if `chars` exceeds the length of the hex string (max 32 for MD5), the method will throw `StringIndexOutOfBoundsException`. There is no validation or documentation of valid range.
- MD5 is cryptographically broken; using this for password generation is a security concern that should be documented or the method should carry a deprecation warning.

---

### A105-17 — Util.checkedValueRadio: undocumented public method (inline comment only)
**Severity:** LOW
**File:** util/Util.java, line 179
**Detail:** The method has an inline comment `//for radio box` (line 178) rather than Javadoc. The comment is non-Javadoc and will not appear in generated API docs. The method returns `"checked"` or `""` for use in HTML attribute rendering; the return contract is not documented.

---

### A105-18 — Util.checkedValueCheckbox: partial inline comment, no Javadoc
**Severity:** LOW
**File:** util/Util.java, line 191
**Detail:** The inline comment at line 190 ("Used to check mutiple selection by default in a HTML form") contains a typo ("mutiple"). No Javadoc is present. The method returns `"checked"` or `""`.

---

### A105-19 — Util.ArraListToString: @Deprecated without Javadoc explanation
**Severity:** LOW
**File:** util/Util.java, line 204
**Detail:** The method carries `@Deprecated` (line 203) but has no Javadoc comment explaining why it is deprecated, what the replacement is, or since which version it was deprecated. Standard Javadoc practice requires a `@deprecated` tag in the Javadoc comment describing the replacement. The method name itself contains a typo (`ArraList` instead of `ArrayList`).

---

### A105-20 — Util.selectRoleBox: undocumented public method (inline comment only)
**Severity:** LOW
**File:** util/Util.java, line 210
**Detail:** The inline comment at line 209 ("Used to check multiple selection by default in a HTML form") does not constitute Javadoc. No documentation of the `value`/`dbValue` parameter semantics or return value (`"selected"` or `""`).

---

### A105-21 — Util.getBarcodeTimeLst: undocumented non-trivial public method; fragile contract
**Severity:** MEDIUM
**File:** util/Util.java, line 230
**Detail:** No Javadoc. The method parses a date-time string and returns a list of barcode-encoded time components. Notable undocumented behaviours:
- The `time` parameter must be in exactly the format `"dd/MM/yyyy HH:mm"` (two space-separated tokens, date with `/` delimiters, time with `:` delimiters). Any deviation causes an `ArrayIndexOutOfBoundsException` or incorrect output with no documented validation.
- The method accesses substrings of individual day/month/hour/minute components (e.g., `month.substring(0,1)`), implicitly requiring zero-padded two-digit values. Single-digit months or days will cause incorrect encoding with no error.
- The year extraction uses `year.substring(2,3)` and `year.substring(3,4)`, implying a four-digit year is required.
- Returns exactly 10 elements always; this is not documented.

---

### A105-22 — Util.generateRadomName: undocumented public method; typo in method name
**Severity:** LOW
**File:** util/Util.java, line 258
**Detail:** No Javadoc. Method name is misspelled (`generateRadomName` instead of `generateRandomName`). The method combines a formatted timestamp with a UUID; the return format (`"yyyyMMddHHmmss-UUID"`) is not documented.

---

### A105-23 — Util.nthOccurrence: undocumented non-trivial public method; off-by-one behaviour undocumented
**Severity:** MEDIUM
**File:** util/Util.java, line 268
**Detail:** No Javadoc. The method finds the position of the nth occurrence of character `c` in `str`. Notable undocumented behaviours:
- The loop condition is `n-- > 0`, which means `n=0` returns the first occurrence (index of the 1st match), `n=1` returns the second occurrence, etc. This zero-based counting is non-obvious and not documented.
- Returns `-1` if fewer than `n+1` occurrences exist; not documented.
- No null check on `str`; passing `null` throws `NullPointerException`.

---

## 3. Summary Table

| ID | File | Location | Severity | Description |
|----|------|----------|----------|-------------|
| A105-1 | InfoLogger.java | line 14 | LOW | No class-level Javadoc (block comment is not Javadoc) |
| A105-2 | InfoLogger.java | line 26 | MEDIUM | `getFileURL` undocumented; null return and parameter format unspecified |
| A105-3 | InfoLogger.java | lines 31-34 | LOW | `getLogger` Javadoc present but content trivially thin |
| A105-4 | InfoLogger.java | lines 39-43 | MEDIUM | `logException` Javadoc inaccurate: omits stderr side-effect from `e.printStackTrace()` |
| A105-5 | InfoLogger.java | lines 39-43 | LOW | `logException` parameter `e` narrowly typed as `Exception`; not noted in docs |
| A105-6 | RuntimeConf.java | line 3 | LOW | No class-level Javadoc |
| A105-7 | RuntimeConf.java | lines 4-66 | LOW | No field-level Javadoc on any of the 50 public static fields |
| A105-8 | RuntimeConf.java | lines 11,15,20,58 | MEDIUM | Typos in field names/values baked into public API with no corrective documentation |
| A105-9 | RuntimeConf.java | line 11 | LOW | `DEFAUTL_TIMEZONE` hardcoded; no docs on overridability |
| A105-10 | RuntimeConf.java | line 50 | LOW | `CHECKLIST_SECONDS` unit and purpose undocumented |
| A105-11 | RuntimeConf.java | line 60 | MEDIUM | `APIURL` hardcoded HTTP EC2 URL; no docs on environment override or lack of TLS |
| A105-12 | Util.java | line 30 | LOW | No class-level Javadoc |
| A105-13 | Util.java | line 32 | MEDIUM | `sendMail` (6-arg) undocumented; dead params, asymmetric error-return undocumented |
| A105-14 | Util.java | line 73 | MEDIUM | `sendMail` (8-arg) undocumented; inconsistent error-return vs 6-arg; NPE on null attachment |
| A105-15 | Util.java | line 134 | MEDIUM | `getHTML` undocumented; 15-min timeout, silent exception swallow, string concat in loop |
| A105-16 | Util.java | line 159 | MEDIUM | `genPass` undocumented; null return, no range guard on `chars`, uses broken MD5 |
| A105-17 | Util.java | line 179 | LOW | `checkedValueRadio` inline comment only, not Javadoc |
| A105-18 | Util.java | line 191 | LOW | `checkedValueCheckbox` inline comment only; typo in comment |
| A105-19 | Util.java | line 204 | LOW | `@Deprecated` with no Javadoc `@deprecated` tag or replacement guidance |
| A105-20 | Util.java | line 210 | LOW | `selectRoleBox` inline comment only, not Javadoc |
| A105-21 | Util.java | line 230 | MEDIUM | `getBarcodeTimeLst` undocumented; requires strict date format, no validation |
| A105-22 | Util.java | line 258 | LOW | `generateRadomName` undocumented; method name misspelled |
| A105-23 | Util.java | line 268 | MEDIUM | `nthOccurrence` undocumented; non-obvious zero-based `n`, NPE on null input |

**Totals: 23 findings — 9 MEDIUM, 14 LOW, 0 HIGH**
