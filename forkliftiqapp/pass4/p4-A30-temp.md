# Pass 4 Code Quality Audit — Agent A30
**Audit run:** 2026-02-26-01
**Auditor:** A30
**Files assigned:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/JoinCompanyParameter.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/LoginParameter.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/ResetPasswordParameter.java`

---

## Step 1: Reading Evidence

### File 1 — JoinCompanyParameter.java (19 lines)

**Class:** `JoinCompanyParameter`
- Extends: `WebServiceParameterPacket`
- Implements: `Serializable`
- Package: `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters`

**Fields (all public):**
- `public int driver_id` — line 14
- `public int comp_id` — line 15

**Methods:**
- `JoinCompanyParameter()` — no-arg constructor, line 17–18

**Types / Constants / Enums / Interfaces:** none

**Imports (lines 3–10):**
```
org.json.JSONException          (line 3)
org.json.JSONObject             (line 4)
java.io.Serializable            (line 5)
org.json.JSONArray              (line 6)
java.util.ArrayList             (line 7)
java.math.BigDecimal            (line 8)
au...webserviceclasses.*        (line 9)
au...webserviceclasses.results.*(line 10)
```

---

### File 2 — LoginParameter.java (19 lines)

**Class:** `LoginParameter`
- Extends: `WebServiceParameterPacket`
- Implements: `Serializable`
- Package: `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters`

**Fields (all public):**
- `public String email` — line 14
- `public String password` — line 15

**Methods:**
- `LoginParameter()` — no-arg constructor, line 17–18

**Types / Constants / Enums / Interfaces:** none

**Imports (lines 3–10):** identical set to JoinCompanyParameter.java

---

### File 3 — ResetPasswordParameter.java (18 lines)

**Class:** `ResetPasswordParameter`
- Extends: `WebServiceParameterPacket`
- Implements: `Serializable`
- Package: `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters`

**Fields (all public):**
- `public String email` — line 14

**Methods:**
- `ResetPasswordParameter()` — no-arg constructor, line 16–17

**Types / Constants / Enums / Interfaces:** none

**Imports (lines 3–10):** identical set to JoinCompanyParameter.java

---

### Supporting context gathered

- `WebServiceParameterPacket` extends `WebServicePacket implements Serializable` — both base classes have only empty-body constructors; no field population occurs in the hierarchy.
- All sibling parameter classes in the `parameters/` package carry the same identical block of six unused imports (lines 3–8).
- `CurrentUser.java` (the sole caller of `LoginParameter`) assigns fields directly:
  ```java
  loginParameter.email    = CommonFunc.MD5_Hash(loginEmail); // line 82
  loginParameter.password = loginPassword;                   // line 83
  ```
- `WebApi.java` exposes `joinCompany` via `URLBuilder.urlJoinCompany()` and `resetPassword` via `URLBuilder.urlResetPassword()`, but no call-site that constructs and populates a `JoinCompanyParameter` was found in the source tree (the class is referenced only in its own file and in audit artefacts).

---

## Step 2–3: Findings

---

### A30-1 — HIGH — `LoginParameter.password` stored and transmitted as plain-text `String`

**File:** `LoginParameter.java`, line 15
**Severity:** HIGH

`password` is declared as `public String`. Java `String` objects are immutable and interned; a plain-text password assigned to a `String` field remains in the heap and in the string pool until GC clears it, which may never happen deterministically. The field is populated without any obfuscation by the caller (`CurrentUser.java` line 83: `loginParameter.password = loginPassword`), meaning the raw credential is alive for the duration of the network request lifecycle. Sensitive credentials should be held in a `char[]` that can be explicitly zeroed after use, or the transport layer should be responsible for hashing/tokenising before the value is bound to any DTO. Compare: `email` receives `MD5_Hash()` treatment at the call site (line 82) but `password` receives none.

---

### A30-2 — HIGH — `JoinCompanyParameter` has no call site — potential dead class

**File:** `JoinCompanyParameter.java`
**Severity:** HIGH

A full-codebase search for `JoinCompanyParameter`, `joinCompany` (method-name form), and `join_company` finds no instantiation or use of this class outside the class file itself and audit artefacts. `URLBuilder.urlJoinCompany()` exists, and `JoinCompanyResult` exists, but `WebApi.java` exposes no `joinCompany(JoinCompanyParameter, ...)` method and no activity or fragment constructs a `JoinCompanyParameter`. The class is either dead code that was never wired up, or an unfinished feature whose call path was removed without removing the supporting DTO. Dead parameter DTOs contribute to maintenance confusion and inflate the attack surface via serializable classes that carry no protection.

---

### A30-3 — MEDIUM — Identical block of unused imports copy-pasted into every parameter class

**Files:** `JoinCompanyParameter.java` lines 3–10, `LoginParameter.java` lines 3–10, `ResetPasswordParameter.java` lines 3–10 (and all other siblings in the package)
**Severity:** MEDIUM

Every parameter class in the package carries the identical six-import block:
```java
import org.json.JSONException;
import org.json.JSONObject;
import java.io.Serializable;
import org.json.JSONArray;
import java.util.ArrayList;
import java.math.BigDecimal;
import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*;
import au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*;
```
None of `JSONException`, `JSONObject`, `JSONArray`, `ArrayList`, or `BigDecimal` are referenced in any of the three audited files (or in most siblings). `java.io.Serializable` is used via the `implements` clause. The wildcard imports for `webserviceclasses.*` and `webserviceclasses.results.*` are also unnecessary since the only needed type (`WebServiceParameterPacket`) is inherited via the extends chain and does not need to be imported. This block was clearly templated and pasted verbatim. The unused imports produce build warnings and indicate the classes were generated from a template that was never cleaned up.

---

### A30-4 — MEDIUM — `Serializable` implemented redundantly in subclasses that already inherit it

**Files:** All three files, `implements Serializable` clause
**Severity:** MEDIUM

`WebServicePacket` implements `Serializable`. `WebServiceParameterPacket extends WebServicePacket implements Serializable`. Each concrete parameter class then again declares `implements Serializable`. Because `Serializable` is inherited transitively, every explicit `implements Serializable` declaration in the concrete parameter classes and in `WebServiceParameterPacket` is redundant. This is noise that signals the pattern was copy-pasted rather than designed. While harmless at runtime, it degrades readability and suggests the developers were unaware of inheritance-based `Serializable` propagation.

---

### A30-5 — MEDIUM — All fields are `public` with no encapsulation

**Files:** All three files
**Severity:** MEDIUM

Every data field across all three classes is declared `public`:
- `JoinCompanyParameter`: `public int driver_id`, `public int comp_id`
- `LoginParameter`: `public String email`, `public String password`
- `ResetPasswordParameter`: `public String email`

There are no getters, setters, or validation guards. Any code with a reference to these objects can freely mutate fields, including the sensitive `password` field. For a DTO pattern used solely for serialisation this is a recognised trade-off, but the absence of encapsulation is especially problematic when combined with a plain-text password field (see A30-1). For `LoginParameter.password` in particular, a package-private or method-scoped scope with builder-pattern construction would eliminate the window in which the credential can be read by arbitrary code.

---

### A30-6 — LOW — Field naming uses `snake_case` inconsistent with Java convention

**Files:** `JoinCompanyParameter.java` lines 14–15, and the `email`/`password` names in the other two files are camelCase
**Severity:** LOW

`JoinCompanyParameter` declares fields named `driver_id` and `comp_id` using `snake_case`. Java coding conventions (and the Android style guide) require `lowerCamelCase` for field names. The other two audited files use camelCase names (`email`, `password`) that comply with convention. `driver_id` and `comp_id` are consistent with the server-side JSON key names, which suggests they are named for Gson field matching rather than Java idiom, but neither class uses a `@SerializedName` annotation to make the intent explicit. Mixing naming conventions across the parameter package creates style inconsistency; the preferred approach is camelCase Java names with `@SerializedName("driver_id")` annotations.

---

### A30-7 — LOW — No `serialVersionUID` declared despite implementing `Serializable`

**Files:** All three files
**Severity:** LOW

All three classes implement `Serializable` (directly or by inheritance) but none declares a `serialVersionUID`. The JVM will auto-generate a `serialVersionUID` based on class structure; any change to the class (field add/remove, method rename) silently changes the generated UID, causing `InvalidClassException` if previously serialised instances are deserialised. IDE tools and static analysis (e.g. Android Lint rule `serial`) flag this as a warning. A declared `private static final long serialVersionUID = 1L;` would suppress the warning and make versioning explicit.

---

## Summary Table

| ID    | Severity | File(s)                        | Issue                                                              |
|-------|----------|--------------------------------|--------------------------------------------------------------------|
| A30-1 | HIGH     | LoginParameter.java            | Plain-text `String password` field — no zeroing possible           |
| A30-2 | HIGH     | JoinCompanyParameter.java      | No call site found — likely dead/unfinished class                  |
| A30-3 | MEDIUM   | All three files                | Unused boilerplate import block copy-pasted into every class       |
| A30-4 | MEDIUM   | All three files                | Redundant `implements Serializable` already inherited from base    |
| A30-5 | MEDIUM   | All three files                | All fields public, no encapsulation; critical for password field   |
| A30-6 | LOW      | JoinCompanyParameter.java      | `snake_case` field names without `@SerializedName` annotation      |
| A30-7 | LOW      | All three files                | Missing `serialVersionUID` on `Serializable` classes               |
