# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A47
**Files audited:**
- `src/main/java/com/bean/EmailSubscriptionBean.java`
- `src/main/java/com/bean/EntityBean.java`
- `src/main/java/com/bean/FormBuilderBean.java`

---

## 1. Reading-Evidence Blocks

### 1.1 EmailSubscriptionBean
**File:** `src/main/java/com/bean/EmailSubscriptionBean.java`
**Package:** `com.bean`
**Annotations:** `@Data`, `@NoArgsConstructor` (Lombok)

| Element | Kind | Line(s) |
|---|---|---|
| `EmailSubscriptionBean` | class | 9 |
| `id` | field (`Long`) | 11 |
| `driver_id` | field (`Long`) | 12 |
| `email_addr1` | field (`String`) | 13 |
| `email_addr2` | field (`String`) | 14 |
| `email_addr3` | field (`String`) | 15 |
| `email_addr4` | field (`String`) | 16 |
| `op_code` | field (`String`) | 17 |
| `EmailSubscriptionBean()` | constructor (no-arg, Lombok `@NoArgsConstructor`) | 8 (generated) |
| `EmailSubscriptionBean(Long, Long, String, String, String, String, String)` | constructor (`@Builder`, private) | 20–28 |
| Lombok-generated getters/setters for all 7 fields | methods (`@Data`) | generated |

**Notes:**
- `@Builder` is placed on the private all-args constructor. This is a non-standard Lombok pattern; the builder is accessible but the constructor itself is private.
- No-arg constructor and builder are the only construction paths.
- No validation, no `@NotNull`, no email-format enforcement on any `email_addr*` field.

---

### 1.2 EntityBean
**File:** `src/main/java/com/bean/EntityBean.java`
**Package:** `com.bean`
**Implements:** `java.io.Serializable`

| Element | Kind | Line(s) |
|---|---|---|
| `serialVersionUID` | field (`static final long`) | 10 |
| `id` | field (`String`, default `null`) | 11 |
| `name` | field (`String`, default `null`) | 12 |
| `password` | field (`String`, default `null`) | 13 |
| `email` | field (`String`, default `null`) | 14 |
| `arrRoleBean` | field (`ArrayList<RoleBean>`, initialized to empty list) | 15 |
| `getArrRoleBean()` | method | 17–19 |
| `setArrRoleBean(ArrayList<RoleBean>)` | method | 22–24 |
| `addArrRoleBean(RoleBean)` | method | 27–29 |
| `getId()` | method | 32–34 |
| `setId(String)` | method | 35–37 |
| `getName()` | method | 38–40 |
| `setName(String)` | method | 41–43 |
| `getPassword()` | method | 45–47 |
| `setPassword(String)` | method | 48–50 |
| `getEmail()` | method | 51–53 |
| `setEmail(String)` | method | 54–56 |

**Security note:** The `password` field (line 13) is a plain `String`. No hashing, encoding, or `char[]` hygiene is present. `getPassword()` (line 45–47) returns the plaintext password directly.

---

### 1.3 FormBuilderBean
**File:** `src/main/java/com/bean/FormBuilderBean.java`
**Package:** `com.bean`
**Implements:** `java.io.Serializable`

| Element | Kind | Line(s) |
|---|---|---|
| `serialVersionUID` | field (`static final long`) | 11 |
| `arrElementBean` | field (`ArrayList<FormElementBean>`, initialized to empty list) | 16 |
| `getArrElementBean()` | method | 18–20 |
| `setArrElementBean(ArrayList<FormElementBean>)` | method | 22–24 |
| `addArrElementBean(FormElementBean)` | method | 26–28 |

**Note:** `serialVersionUID` value (`3895903590422186042L`) is identical to the one in `EntityBean`. This is likely a copy-paste artifact.

---

## 2. Test-Directory Search Results

**Test directory searched:** `src/test/java/`

| Class searched | Files found in test directory |
|---|---|
| `EmailSubscriptionBean` | **None** |
| `EntityBean` | **None** |
| `FormBuilderBean` | **None** |

Existing test files in the project (all unrelated to the audited classes):

```
src/test/java/com/calibration/UnitCalibrationImpactFilterTest.java
src/test/java/com/calibration/UnitCalibrationTest.java
src/test/java/com/calibration/UnitCalibratorTest.java
src/test/java/com/util/ImpactUtilTest.java
```

Zero test coverage exists for `EmailSubscriptionBean`, `EntityBean`, or `FormBuilderBean`.

---

## 3. Coverage Gaps and Findings

### A47-1 | Severity: CRITICAL | EntityBean stores and exposes plaintext password

`EntityBean` declares `private String password` (line 13) and exposes it without any transformation through `getPassword()` (lines 45–47) and `setPassword(String)` (lines 48–50). The password is stored as a `String` object on the heap, making it subject to string-pool retention and heap-dump exposure. No hashing, salting, or `char[]` wiping is performed. There is no test asserting that this field is never serialized or logged in plaintext.

**Evidence:** `EntityBean.java` lines 13, 45–50.

---

### A47-2 | Severity: HIGH | Zero test coverage — EmailSubscriptionBean

No test class exists for `EmailSubscriptionBean`. The following behaviors are completely untested:

- Lombok `@NoArgsConstructor` produces a correctly initialized object (all fields `null`).
- Lombok `@Builder` (on private constructor, lines 20–28) produces objects with the correct field values.
- Lombok `@Data`-generated getters return the value that was set.
- Lombok `@Data`-generated setters mutate state correctly.
- `equals()` / `hashCode()` / `toString()` generated by `@Data` behave correctly (especially that `toString()` does not expose sensitive data — in this class that risk is lower, but still worth asserting).
- `op_code` field accepts and stores expected operational codes without silent truncation.
- `email_addr1` through `email_addr4` accept valid and reject invalid (or null) email addresses.

---

### A47-3 | Severity: HIGH | Zero test coverage — EntityBean

No test class exists for `EntityBean`. The following behaviors are completely untested:

- Default field values (`id`, `name`, `password`, `email` all `null`; `arrRoleBean` initialized to empty `ArrayList`).
- `addArrRoleBean(RoleBean)` correctly appends to the list (line 27–29).
- `setArrRoleBean(ArrayList<RoleBean>)` replaces the list reference (including accepting `null`, which would cause a `NullPointerException` on a subsequent `add` call).
- `getArrRoleBean()` returns the same list instance (not a defensive copy).
- Serialization round-trip preserves all field values (class implements `Serializable`).
- `getPassword()` / `setPassword(String)` — the absence of a test for password handling means the plaintext storage issue (A47-1) goes undetected by the test suite.
- No `equals()`, `hashCode()`, or `toString()` override exists; accidental logging via `toString()` would silently emit the default object identity string (not a data-leak risk here, but the absence of an intentional override is untested and undocumented).

---

### A47-4 | Severity: HIGH | Zero test coverage — FormBuilderBean

No test class exists for `FormBuilderBean`. The following behaviors are completely untested:

- Default `arrElementBean` is an initialized empty `ArrayList`, not `null`.
- `addArrElementBean(FormElementBean)` correctly appends an element (lines 26–28).
- `addArrElementBean(null)` behavior — `ArrayList.add(null)` succeeds silently; no null-guard is present.
- `setArrElementBean(null)` replaces the list with `null`; a subsequent `addArrElementBean` call would throw `NullPointerException`.
- `getArrElementBean()` returns the mutable internal list (not a defensive copy), allowing callers to modify internal state without going through `addArrElementBean`.
- Serialization round-trip preserves list contents.

---

### A47-5 | Severity: MEDIUM | Duplicate serialVersionUID across EntityBean and FormBuilderBean

`EntityBean` (line 10) and `FormBuilderBean` (line 11) both declare `serialVersionUID = 3895903590422186042L`. This is an unambiguous copy-paste error. While it does not cause runtime failures today (each class is its own type), it is a maintenance hazard: if either class is intentionally evolved and the UID is updated, a developer following the same pattern may update both, silently breaking deserialization of the other. No test validates the deserialization contract for either class.

**Evidence:** `EntityBean.java` line 10; `FormBuilderBean.java` line 11.

---

### A47-6 | Severity: MEDIUM | EmailSubscriptionBean — no input validation on email address fields

`email_addr1` through `email_addr4` (lines 13–16) are plain `String` fields with no `@Email`, `@Pattern`, `@NotNull`, or any other Bean Validation (`javax.validation`) constraint. No test verifies that invalid email strings (empty string, `null`, malformed addresses) are handled appropriately, either by the bean itself or by its callers.

---

### A47-7 | Severity: MEDIUM | EntityBean — no null-guard in addArrRoleBean

`addArrRoleBean(RoleBean roleBean)` (lines 27–29) calls `arrRoleBean.add(roleBean)` without a null check on the argument. `ArrayList.add(null)` succeeds silently, which can produce a list containing `null` entries that propagate to callers iterating the list. No test covers null-argument behavior.

---

### A47-8 | Severity: MEDIUM | FormBuilderBean — no null-guard in addArrElementBean

`addArrElementBean(FormElementBean formElementBean)` (lines 26–28) calls `arrElementBean.add(formElementBean)` without a null check. Same risk as A47-7. No test covers null-argument behavior.

---

### A47-9 | Severity: MEDIUM | FormBuilderBean — setArrElementBean(null) causes NullPointerException on next add

`setArrElementBean(ArrayList<FormElementBean> arrElementBean)` (lines 22–24) performs a plain field assignment with no null-guard. If a caller passes `null`, the field becomes `null` and the next call to `addArrElementBean` throws `NullPointerException` at line 27. This is a latent defect with no test to detect it.

**Same pattern exists in EntityBean.setArrRoleBean** (lines 22–24).

---

### A47-10 | Severity: LOW | EmailSubscriptionBean — @Builder on private constructor is non-idiomatic

Placing `@Builder` on a private constructor (line 19–20) while `@Data` and `@NoArgsConstructor` are present on the class is non-idiomatic Lombok usage. The generated builder class is public but the constructor it delegates to is private. This works at compile time via Lombok's code generation but can confuse developers maintaining the class and may behave unexpectedly under some Lombok versions or annotation processors. No test exercises the builder path to document expected construction behavior.

---

### A47-11 | Severity: LOW | EntityBean — mutable ArrayList returned by getArrRoleBean without defensive copy

`getArrRoleBean()` (lines 17–19) returns the internal `ArrayList` reference directly. Any caller can mutate the list (add, remove, clear) without going through `addArrRoleBean`. This breaks encapsulation. No test asserts that the returned list is unmodifiable or that modifications via the getter do not affect internal state.

Same issue exists in `FormBuilderBean.getArrElementBean()` (lines 18–20).

---

### A47-12 | Severity: INFO | No test exists for Lombok-generated equals/hashCode/toString on EmailSubscriptionBean

`@Data` generates `equals()`, `hashCode()`, and `toString()` based on all fields. `toString()` will include field names and values in its output. While no field in `EmailSubscriptionBean` is a password, the `email_addr*` fields are PII. If a `toString()` call appears in a log statement, four email addresses would be exposed. No test verifies `toString()` output or asserts that it is not used in logging contexts.

---

## 4. Summary Table

| Finding | Severity | Class | Description |
|---|---|---|---|
| A47-1 | CRITICAL | EntityBean | Plaintext password stored and exposed via getter |
| A47-2 | HIGH | EmailSubscriptionBean | Zero test coverage |
| A47-3 | HIGH | EntityBean | Zero test coverage |
| A47-4 | HIGH | FormBuilderBean | Zero test coverage |
| A47-5 | MEDIUM | EntityBean / FormBuilderBean | Duplicate serialVersionUID (copy-paste error) |
| A47-6 | MEDIUM | EmailSubscriptionBean | No input validation on email address fields |
| A47-7 | MEDIUM | EntityBean | No null-guard in addArrRoleBean |
| A47-8 | MEDIUM | FormBuilderBean | No null-guard in addArrElementBean |
| A47-9 | MEDIUM | FormBuilderBean / EntityBean | setArr*Bean(null) causes latent NPE on next add |
| A47-10 | LOW | EmailSubscriptionBean | Non-idiomatic @Builder on private constructor |
| A47-11 | LOW | EntityBean / FormBuilderBean | Mutable internal list returned without defensive copy |
| A47-12 | INFO | EmailSubscriptionBean | Lombok toString() exposes PII email fields; no test documents this |

---

*Report generated by Agent A47 — Pass 2 — Audit run 2026-02-26-01*
