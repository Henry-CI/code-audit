# Security Audit: AdminRegisterActionForm.java

**Repository:** forkliftiqadmin
**Branch:** master
**Audit Run:** audit/2026-02-26-01/
**Pass:** pass1
**File:** src/main/java/com/actionform/AdminRegisterActionForm.java
**Auditor:** Automated security audit (Claude)
**Date:** 2026-02-26
**Stack:** Apache Struts 1.3.10 — CSRF is a structural gap for all forms
**Endpoint exposure:** adminRegister.do is in the PreFlightActionServlet exclusion list (publicly accessible, no prior authentication required)

---

## 1. Reading Evidence

### 1.1 Package and Class

```
package com.actionform;
public final class AdminRegisterActionForm extends ValidatorForm
```

Extends `org.apache.struts.validator.ValidatorForm`, meaning declarative validation from `validation.xml` is wired in at the framework level. There is no `validate()` override. There is no `reset()` override.

### 1.2 All Fields (all are `String`, initialised to `null`)

| # | Field name       | Type   | Notes                                      |
|---|------------------|--------|--------------------------------------------|
| 1 | `id`             | String | Caller-supplied entity/company identifier  |
| 2 | `name`           | String | Company name                               |
| 3 | `address`        | String | Company address                            |
| 4 | `postcode`       | String | Postal code                                |
| 5 | `email`          | String | Primary email                              |
| 6 | `contact_no`     | String | Contact phone number                       |
| 7 | `contact_fname`  | String | Contact first name                         |
| 8 | `contact_lname`  | String | Contact last name                          |
| 9 | `password`       | String | Account password (plain String)            |
| 10| `pin`            | String | Numeric PIN (plain String)                 |
| 11| `refnm`          | String | Reference name                             |
| 12| `refno`          | String | Reference number                           |
| 13| `question`       | String | Security question                          |
| 14| `answer`         | String | Security answer (plain String)             |
| 15| `code`           | String | Activation / invite code                  |
| 16| `accountAction`  | String | Controls which action path is taken        |
| 17| `unit`           | String | Business unit                              |
| 18| `subemail`       | String | Subscription / secondary email            |
| 19| `timezone`       | String | Timezone selection                         |
| 20| `lan_id`         | String | Language ID                                |
| 21| `mobile`         | String | Mobile phone number                        |

### 1.3 validate() Details

No `validate()` override exists. The class relies entirely on declarative Commons Validator rules defined in `validation.xml`. Any validation logic that requires cross-field checks, business-rule checks, or server-side format enforcement beyond what Commons Validator provides is **absent**.

### 1.4 reset() Details

No `reset()` override exists. Struts will call `ValidatorForm.reset()` (the parent), which does **not** zero out these fields — it only resets Struts internal state. All 21 String fields persist their previous values across request reuse if the action is ever pooled or reused in a way that does not reinitialise the form bean. For a `request`-scoped form this is lower risk, but the absence of an explicit `reset()` leaves all sensitive fields (`password`, `pin`, `answer`, `id`) without guaranteed clearing.

### 1.5 Validation.xml Rules for adminRegisterActionForm (full verbatim quote)

```xml
<form name="adminRegisterActionForm">
    <field property="name" depends="required,minlength">
        <arg0 key="compName" />
        <arg1 key="${var:minlength}" resource="false" />
        <var>
            <var-name>minlength</var-name>
            <var-value>3</var-value>
        </var>
    </field>
    <field property="contact_name" depends="required">
        <arg0 key="contactName" />
    </field>
    <field property="email" depends="required,email">
        <arg0 key="email" />
    </field>
    <field property="contact_no" depends="integer">
        <arg0 key="contactNumber" />
    </field>
    <field property="password" depends="required,minlength">
        <arg0 key="password" />
        <arg1 key="${var:minlength}" resource="false" />
        <var>
            <var-name>minlength</var-name>
            <var-value>4</var-value>
        </var>
    </field>
</form>
```

Only **5 fields** have any rules. The form has **21 fields**. **16 fields have zero validation rules.**

---

## 2. Findings

---

### FINDING-01 — CRITICAL: Caller-Supplied `id` Field Enables Full IDOR / Tenant Injection

**Severity:** CRITICAL
**File:** `src/main/java/com/actionform/AdminRegisterActionForm.java`
**Line:** 9 (`private String id = null;`) / 121–126 (getter/setter)

**Description:**
The form exposes a writable `id` field that a caller can supply freely via a POST parameter. Given the endpoint name (`adminRegister.do`) and the multi-tenant nature of this application (companies, units, language IDs), this field almost certainly maps to a company or account identifier used during record creation. Because the endpoint is publicly accessible (no authentication gate via PreFlightActionServlet), an unauthenticated attacker can submit an arbitrary `id` value, potentially registering an admin account under a different company's tenant context.

**Evidence:**
- Line 9: `private String id = null;`
- Lines 121–126: public getter and setter exposed without restriction.
- `validation.xml`: no rule of any kind for `id`.
- No `validate()` override performs a business-rule check.
- Endpoint is in PreFlightActionServlet exclusion list (no authentication pre-check).

**Recommendation:**
The `id` field must NOT be populated from user-supplied HTTP input on a public registration endpoint. If a company/tenant `id` must be associated during registration it must be derived server-side (generated or resolved from an invite code). Remove the setter, or annotate the field as server-only and have the action class populate it directly. At minimum, add a server-side check in the action class that the supplied `id` is null/empty before use.

---

### FINDING-02 — CRITICAL: `accountAction` Field Allows Caller to Control Server-Side Action Routing

**Severity:** CRITICAL
**File:** `src/main/java/com/actionform/AdminRegisterActionForm.java`
**Line:** 24 (`private String accountAction = null;`) / 127–132 (getter/setter)

**Description:**
The `accountAction` field is a plain String with a public getter and setter, no whitelist validation, and no validation.xml rule. On a public endpoint, an attacker can supply arbitrary values for `accountAction`. If the action class uses this field to branch between code paths (e.g., `"create"`, `"update"`, `"delete"`, `"approve"`), an unauthenticated caller can steer the server into unintended code paths — potentially elevating privileges, bypassing invite/code checks, or triggering administrative operations.

**Evidence:**
- Line 24: `private String accountAction = null;`
- Lines 127–132: public getter/setter.
- `validation.xml`: no rule for `accountAction`.
- No `validate()` override.
- Endpoint is publicly accessible.

**Recommendation:**
If `accountAction` must be accepted from the client, it must be validated against an explicit server-side whitelist of permitted values before use. Consider whether this field should be accepted from the client at all for a public registration flow; for most registration endpoints the action is fixed and does not require client-supplied routing hints.

---

### FINDING-03 — CRITICAL: Password Stored and Exposed as Plain `String` with No Complexity Rule

**Severity:** CRITICAL
**File:** `src/main/java/com/actionform/AdminRegisterActionForm.java`
**Lines:** 17 (`private String password = null;`) / 79–84 (getter/setter)

**Description:**
The `password` field is declared as a `String`. Java `String` objects are immutable and interned — they cannot be zeroed from memory after use. A password held in a `String` will remain in the JVM heap until garbage collected and potentially in JVM string pools indefinitely. Any heap dump, crash dump, or memory inspection can expose the plaintext password. The correct pattern for Struts forms handling passwords is `char[]` with explicit zeroing in `reset()`.

Beyond memory safety, the `validation.xml` rule for `password` enforces only `required` and `minlength=4`. A four-character minimum is insufficient for an administrative account password on a publicly-accessible registration endpoint — it permits passwords such as `aaaa`, `1234`, and `pass`.

**Evidence:**
- Line 17: `private String password = null;`
- `validation.xml`: `depends="required,minlength"` with `minlength=4`.
- No `maxlength` rule (unbounded input — potential DoS vector for extremely long values).
- No complexity rule (no `mask` validator enforcing mixed-case, digit, or special character requirements).
- No `reset()` override to zero the field after use.

**Recommendation:**
1. Minimum password length for an admin account should be at least 12 characters; enforce with a `minlength` of 12 and add a `maxlength` cap (e.g., 128) to prevent DoS.
2. Add a `mask` validator rule enforcing complexity (at least one digit, one uppercase, one special character).
3. In the action class, pass the password directly to a `char[]` and zero it immediately after hashing. Do not store it in a String longer than necessary.
4. Add a `reset()` override that sets `password = null` (and ideally `pin = null`, `answer = null`) immediately after validation.

---

### FINDING-04 — HIGH: `pin` Field — No Validation Rules, No Format Enforcement, No Length Limit

**Severity:** HIGH
**File:** `src/main/java/com/actionform/AdminRegisterActionForm.java`
**Line:** 18 (`private String pin = null;`) / 85–90 (getter/setter)

**Description:**
A `pin` field is present and publicly writable with no validation rules whatsoever. PINs are typically short numeric secrets used as secondary authentication factors. Without any validation the following are all possible: empty string, non-numeric characters, PINs of arbitrary length (DoS), and trivially guessable values (no minimum length). Like `password`, storing a PIN in a Java `String` is a memory-safety concern.

**Evidence:**
- Line 18: `private String pin = null;`
- `validation.xml`: no rule for `pin`.
- No `validate()` override.

**Recommendation:**
Add validation.xml rules: `required`, `mask` (digits only, e.g., `[0-9]+`), `minlength` (e.g., 4), and `maxlength` (e.g., 8). Apply the same memory-safety considerations as for `password`.

---

### FINDING-05 — HIGH: `answer` (Security Answer) — No Validation Rules, Plain String Memory Exposure

**Severity:** HIGH
**File:** `src/main/java/com/actionform/AdminRegisterActionForm.java`
**Line:** 22 (`private String answer = null;`) / 109–114 (getter/setter)

**Description:**
The security question answer is a shared secret equivalent in function to a secondary password. It has no validation rules in `validation.xml`, is stored as a plain `String` with all attendant memory-safety issues, and has no length enforcement. An attacker can supply an empty answer (stored without rejection), an excessively long answer (DoS), or an answer containing characters that are dangerous in downstream SQL or HTML contexts.

**Evidence:**
- Line 22: `private String answer = null;`
- `validation.xml`: no rule for `answer`.
- No `validate()` override.

**Recommendation:**
Add `required`, `minlength`, and `maxlength` rules. If the answer is stored hashed (as it should be), it must be hashed immediately in the action class and never persisted or logged in plaintext.

---

### FINDING-06 — HIGH: Phantom Field `contact_name` in validation.xml Does Not Exist in ActionForm

**Severity:** HIGH
**File:** `src/main/webapp/WEB-INF/validation.xml` (line 41) vs `src/main/java/com/actionform/AdminRegisterActionForm.java`

**Description:**
The validation.xml rule for `adminRegisterActionForm` specifies a `required` rule for a field named `contact_name`:

```xml
<field property="contact_name" depends="required">
    <arg0 key="contactName" />
</field>
```

The ActionForm class has no field named `contact_name`. It has `contact_fname` (line 15) and `contact_lname` (line 16), but no `contact_name`. Commons Validator will attempt to evaluate this rule against a property that does not exist on the bean. Depending on the Struts/Commons Validator version this silently passes (the field is treated as absent/null and the `required` check may not fire correctly against the actual fields), meaning the **required contact name validation is silently dead**. The actual contact name fields (`contact_fname`, `contact_lname`) have no validation rules at all.

**Evidence:**
- `validation.xml` line 41: `<field property="contact_name" depends="required">`
- ActionForm: no field `contact_name` exists anywhere in lines 1–158.
- ActionForm lines 15–16: `contact_fname`, `contact_lname` — neither has any validation rule.

**Recommendation:**
Fix the field name in validation.xml to match the actual bean property names (`contact_fname` and/or `contact_lname`), and add `required` rules to both. Audit all other validation.xml field references across all forms for similar phantom-field mismatches.

---

### FINDING-07 — HIGH: 16 of 21 Fields Entirely Unvalidated on a Public Endpoint

**Severity:** HIGH
**File:** `src/main/webapp/WEB-INF/validation.xml` / `src/main/java/com/actionform/AdminRegisterActionForm.java`

**Description:**
Of the 21 fields on this form, only 5 have any validation rules, and one of those rules references a non-existent field (see FINDING-06). The following fields have zero validation rules and accept arbitrary input from the public internet:

`id`, `address`, `postcode`, `contact_fname`, `contact_lname`, `pin`, `refnm`, `refno`, `question`, `answer`, `code`, `accountAction`, `unit`, `subemail`, `timezone`, `lan_id`, `mobile`

Each of these can receive:
- Empty strings (no `required` check)
- Arbitrarily long strings (no `maxlength`, potential DoS)
- Special characters dangerous in SQL, HTML, LDAP, or OS contexts
- Unexpected types or formats

For a publicly-accessible registration endpoint this represents a broad attack surface for injection, DoS, and business logic abuse.

**Evidence:**
- 16 fields with no rules in `validation.xml`.
- No `validate()` override providing programmatic checks.
- Endpoint is unauthenticated.

**Recommendation:**
Every field that will be persisted or processed must have at minimum a `maxlength` rule to prevent DoS. Fields with known formats (`postcode`, `mobile`, `contact_no`, `timezone`, `lan_id`, `refno`) must have `mask` validators enforcing those formats. Fields not used in every code path should still be bounded. Fields that must be present in certain action paths should have `required` rules, using Struts validator page/indexedListProperty scoping if needed.

---

### FINDING-08 — HIGH: `contact_no` Validator Uses `integer` — Rejects Valid Phone Numbers

**Severity:** HIGH
**File:** `src/main/webapp/WEB-INF/validation.xml`
**Line:** 47

**Description:**
The validation rule for `contact_no` is:

```xml
<field property="contact_no" depends="integer">
    <arg0 key="contactNumber" />
</field>
```

The Commons Validator `integer` rule validates that the value parses as a Java `int` (32-bit signed integer, maximum value 2,147,483,647). Phone numbers are not integers:
- They may contain leading zeros (e.g., `0161...`), which are semantically meaningful.
- They may contain `+`, `-`, spaces, or parentheses.
- An international number such as `+447700900123` cannot be represented as a Java `int`.
- Even a 10-digit number such as `07700900123` overflows a 32-bit integer.

Additionally, the `integer` validator is not `required`, meaning an empty `contact_no` passes validation — but a legitimate 11-digit UK number fails. The rule is simultaneously too strict (rejects valid numbers) and too permissive (allows empty).

**Evidence:**
- `validation.xml` line 47: `depends="integer"`.
- No `required`, no `mask`, no `maxlength`.

**Recommendation:**
Replace the `integer` rule with a `mask` rule matching the expected phone number format (e.g., `^[0-9+\-\s()]{7,20}$`). Add `maxlength` to cap input length.

---

### FINDING-09 — MEDIUM: No `maxlength` on Any Field — Unbounded Input DoS Risk

**Severity:** MEDIUM
**File:** `src/main/webapp/WEB-INF/validation.xml` / `src/main/java/com/actionform/AdminRegisterActionForm.java`

**Description:**
Not a single field in the `adminRegisterActionForm` validation ruleset has a `maxlength` constraint. This is a public endpoint. An attacker can submit requests with megabyte-length values for any of the 21 String fields. These values will be bound by Struts into the form bean and passed to the action class, potentially:
- Overloading database write operations.
- Causing excessive memory allocation per request.
- Triggering buffer/string length issues in downstream libraries.
- Bypassing fixed-width database column constraints at the application layer (resulting in truncation errors or silent data corruption rather than clean rejection).

**Evidence:**
- `validation.xml`: no `maxlength` rule on any field for `adminRegisterActionForm`.
- All fields are unbounded `String` with no annotation or programmatic length cap.

**Recommendation:**
Add `maxlength` rules to every field. Appropriate values: `name` ≤ 100, `email` ≤ 254 (RFC 5321), `password` ≤ 128, `address` ≤ 255, `postcode` ≤ 10, `contact_no`/`mobile` ≤ 20, `pin` ≤ 8, `answer` ≤ 255, `code` ≤ 64, `timezone` ≤ 64, `lan_id` ≤ 10.

---

### FINDING-10 — MEDIUM: `password` Minimum Length of 4 is Dangerously Weak for Admin Accounts

**Severity:** MEDIUM
**File:** `src/main/webapp/WEB-INF/validation.xml`
**Lines:** 50–57

**Description:**
(Noted also under FINDING-03; called out separately at MEDIUM for tracking the specific validation.xml policy deficiency.)

The `password` field rule:

```xml
<field property="password" depends="required,minlength">
    <arg0 key="password" />
    <arg1 key="${var:minlength}" resource="false" />
    <var>
        <var-name>minlength</var-name>
        <var-value>4</var-value>
    </var>
</field>
```

A four-character minimum allows trivially brute-forceable passwords. This is the registration form for an **admin** account, and the endpoint is publicly accessible. A `minlength` of 4 combined with no complexity requirement and no rate-limiting at the form-validation layer represents a policy-level failure.

**Evidence:**
- `validation.xml` lines 50–57: `minlength=4`.
- No `mask` complexity rule.
- No `maxlength`.

**Recommendation:**
Raise `minlength` to at least 12. Add a `mask` rule enforcing at least one uppercase letter, one digit, and one special character. Add a `maxlength` of 128.

---

### FINDING-11 — MEDIUM: No `reset()` Override — Sensitive Fields Not Zeroed

**Severity:** MEDIUM
**File:** `src/main/java/com/actionform/AdminRegisterActionForm.java`
**Line:** 1–158 (absence)

**Description:**
The class has no `reset()` override. In Struts, `reset()` is called before the form is populated from the HTTP request on each request cycle. Without an explicit `reset()`, residual values from a previous request cycle (if the bean is session-scoped or pooled) can persist. The fields of highest concern are `password` (line 17), `pin` (line 18), and `answer` (line 22). Even in request scope, defensive coding practice requires explicit zeroing of credentials in `reset()`.

**Evidence:**
- No `reset()` method anywhere in lines 1–158.

**Recommendation:**
Add a `reset()` override that sets `password = null`, `pin = null`, and `answer = null` at minimum. Verify the form bean scope in struts-config.xml to determine actual risk level.

---

### FINDING-12 — MEDIUM: `code` Field (Invite/Activation Code) Has No Validation

**Severity:** MEDIUM
**File:** `src/main/java/com/actionform/AdminRegisterActionForm.java`
**Line:** 23 (`private String code = null;`) / 115–120 (getter/setter)

**Description:**
The `code` field almost certainly represents an invite or activation code used to gate public registration. There are no validation rules for this field — not `required`, not `mask`, not `minlength`, not `maxlength`. If the intent is for this code to gate who can register, its absence of validation means:
- Empty codes pass form validation (enforcement deferred entirely to the action class, which may or may not implement it correctly).
- No format constraint limits the attack surface for code enumeration or injection attacks against the code-checking logic.

**Evidence:**
- Line 23: `private String code = null;`
- `validation.xml`: no rule for `code`.

**Recommendation:**
Add `required` and a `mask` rule matching the expected code format (e.g., alphanumeric, fixed or bounded length). This reduces the attack surface for injection and provides a fast-fail before the action class performs any database lookup.

---

### FINDING-13 — LOW: `timezone` and `lan_id` Accept Arbitrary Values — No Whitelist

**Severity:** LOW
**File:** `src/main/java/com/actionform/AdminRegisterActionForm.java`
**Lines:** 27–36 (`timezone`, `lan_id`)

**Description:**
Both `timezone` and `lan_id` are selection-type fields that in a well-formed UI would come from a controlled dropdown. Without server-side whitelist validation they accept arbitrary string values. If these values are used in file path construction, locale lookups, or dynamic queries, they can serve as injection vectors.

**Evidence:**
- Lines 27–28: `private String timezone = null;` / `private String lan_id = null;`
- `validation.xml`: no rule for either field.

**Recommendation:**
Validate both fields server-side against an explicit whitelist of allowed values (all valid Java/IANA timezone IDs for `timezone`; all supported language codes for `lan_id`). Add this check in `validate()` or in the action class before use.

---

### FINDING-14 — LOW: `refnm` and `refno` Accept Arbitrary Values

**Severity:** LOW
**File:** `src/main/java/com/actionform/AdminRegisterActionForm.java`
**Lines:** 19–20 (`refnm`, `refno`)

**Description:**
Reference name and reference number fields have no validation rules. Their exact usage is unknown without inspecting the action class, but reference identifiers are frequently used in database lookups. Without format constraints these fields can carry injection payloads.

**Evidence:**
- Lines 19–20.
- `validation.xml`: no rules.

**Recommendation:**
Add `maxlength` at minimum. If `refno` is numeric, add a `mask` or `integer`/`long` rule. If `refnm` is alphanumeric, add a `mask` rule.

---

### FINDING-15 — INFO: No `validate()` Override — All Logic Relies on Commons Validator

**Severity:** INFO
**File:** `src/main/java/com/actionform/AdminRegisterActionForm.java`

**Description:**
The form has no programmatic `validate()` override. The class relies entirely on Commons Validator declarative rules. For a registration form with cross-field dependencies (e.g., password confirmation, business-rule checks on `code`, conditional `required` fields depending on `accountAction`) a programmatic `validate()` override would allow richer, context-aware validation that declarative XML cannot express. This is not an immediate vulnerability but is a design limitation that contributes to the gaps identified above.

**Recommendation:**
Consider adding a `validate()` override to implement: cross-field checks, `code` verification logic (or at minimum non-empty assertion), whitelist checks for `accountAction`, `timezone`, and `lan_id`.

---

## 3. Summary Table

| ID            | Severity | Title                                                                 |
|---------------|----------|-----------------------------------------------------------------------|
| FINDING-01    | CRITICAL | Caller-supplied `id` enables IDOR / tenant injection                  |
| FINDING-02    | CRITICAL | `accountAction` allows caller-controlled server-side routing          |
| FINDING-03    | CRITICAL | `password` as plain `String`, minlength=4, no complexity              |
| FINDING-04    | HIGH     | `pin` — no validation rules whatsoever                               |
| FINDING-05    | HIGH     | `answer` (security secret) — no validation, plain String             |
| FINDING-06    | HIGH     | Phantom `contact_name` field in validation.xml — rule is dead        |
| FINDING-07    | HIGH     | 16 of 21 fields entirely unvalidated on public endpoint              |
| FINDING-08    | HIGH     | `contact_no` uses `integer` validator — rejects valid phone numbers  |
| FINDING-09    | MEDIUM   | No `maxlength` on any field — unbounded input DoS                    |
| FINDING-10    | MEDIUM   | Password minlength=4 is dangerously weak for admin accounts          |
| FINDING-11    | MEDIUM   | No `reset()` — sensitive fields not zeroed between requests          |
| FINDING-12    | MEDIUM   | `code` (invite gate) has no validation rules                         |
| FINDING-13    | LOW      | `timezone`/`lan_id` accept arbitrary values, no whitelist            |
| FINDING-14    | LOW      | `refnm`/`refno` accept arbitrary values, no format constraint        |
| FINDING-15    | INFO     | No `validate()` override — all logic deferred to declarative XML     |

---

## 4. Finding Count by Severity

| Severity | Count |
|----------|-------|
| CRITICAL | 3     |
| HIGH     | 5     |
| MEDIUM   | 4     |
| LOW      | 2     |
| INFO     | 1     |
| **TOTAL**| **15**|

---

## 5. Categories With No Issues

No categories are entirely clear. All five audit categories have at least one finding:

- **Input Validation:** Multiple findings (FINDING-06, FINDING-07, FINDING-08, FINDING-09, FINDING-10).
- **Type Safety:** FINDING-03, FINDING-04, FINDING-05 (all sensitive fields stored as `String`).
- **IDOR Risk:** FINDING-01 (direct caller control of `id`).
- **Sensitive Fields:** FINDING-03 (`password`), FINDING-04 (`pin`), FINDING-05 (`answer`), FINDING-11 (no reset/zeroing).
- **Data Integrity / Caller-Supplied Role or CompanyId:** FINDING-01 (`id`), FINDING-02 (`accountAction`).
