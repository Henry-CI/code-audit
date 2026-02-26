# Audit Report: AdminDriverAddForm.java

**Repository:** forkliftiqadmin
**Branch:** master
**Audit Run:** audit/2026-02-26-01/
**File:** src/main/java/com/actionform/AdminDriverAddForm.java
**Auditor:** Claude (claude-sonnet-4-6)
**Date:** 2026-02-26

---

## READING EVIDENCE

### Full Class Name and Package

- **Package:** `com.actionform`
- **Full class name:** `com.actionform.AdminDriverAddForm`
- **Extends:** `org.apache.struts.action.ActionForm`
- **Lombok annotations:** `@Getter`, `@Setter`, `@NoArgsConstructor`, `@Slf4j`

---

### Every Field (Type and Name)

| Line | Type     | Field Name        | Notes                                      |
|------|----------|-------------------|--------------------------------------------|
| 22   | Long     | `id`              | Driver record ID; defaults to null         |
| 23   | String   | `first_name`      |                                            |
| 24   | String   | `last_name`       |                                            |
| 25   | String   | `licence_number`  |                                            |
| 26   | String   | `expiry_date`     | Free-form string, no date parsing          |
| 27   | String   | `security_number` | Sensitive — social/employee security ref   |
| 28   | String   | `address`         |                                            |
| 29   | String   | `app_access`      | Likely an access-level/role flag           |
| 30   | String   | `mobile`          |                                            |
| 31   | String   | `email_addr`      |                                            |
| 32   | String   | `pass`            | Plaintext password field                   |
| 33   | String   | `cpass`           | Plaintext confirm-password field           |
| 34   | String   | `location`        |                                            |
| 35   | String   | `department`      |                                            |
| 36   | String   | `op_code`         | Operator code; purpose unspecified         |

**Total fields: 15**

---

### validate() Method

**Exists:** Yes (lines 38–59).

**Checks performed:**

1. `first_name.equalsIgnoreCase("")` — rejects empty first name (line 41).
2. `last_name.equalsIgnoreCase("")` — rejects empty last name (line 47).
3. `!pass.equalsIgnoreCase(cpass)` — rejects mismatched password/confirm-password (line 53).

**Checks NOT performed (absent):**

- No null check on any field before calling methods on them (NullPointerException risk on `first_name`, `last_name`, `pass`, `cpass`).
- No length constraints on any field.
- No format/pattern validation on `email_addr`, `mobile`, `licence_number`, `expiry_date`, `security_number`.
- No whitelist validation on `app_access` or `op_code`.
- No minimum password length or complexity check.
- No validation of `id` (the Long ID field is never checked).
- `op_code` and `location`/`department` are completely unchecked.

---

### reset() Method

**Exists:** No. There is no `reset()` override. Struts will not clear fields between requests unless the form bean scope is `request` rather than `session`. If the form bean is session-scoped, stale values from a previous submission can persist.

---

### Type Conversion That Could Throw Exceptions

- **`id` field (Long, line 22):** Declared as `Long` (object wrapper). Struts 1 performs its own string-to-Long conversion when binding request parameters. If a user submits a non-numeric value for `id`, Struts will throw a `NumberFormatException` during form population, before `validate()` is ever called. There is no `validation.xml` rule for this field, and `validate()` does not guard against it.
- **`pass` / `cpass` (lines 32–33):** `pass.equalsIgnoreCase(cpass)` (line 53) — if either `pass` or `cpass` is `null` (not submitted in the request), this throws a `NullPointerException` at runtime.
- **`first_name` / `last_name` (lines 41, 47):** Same issue — `.equalsIgnoreCase("")` will throw `NullPointerException` if Struts does not bind the field (e.g., the parameter is absent from the request).

---

## AUDIT FINDINGS

### Category 1 — Input Validation

---

#### FINDING IV-1

**Severity:** HIGH
**File+Line:** `src/main/java/com/actionform/AdminDriverAddForm.java`, lines 41, 47, 53
**Description:** NullPointerException in validate() due to missing null guards before calling instance methods on String fields.
**Evidence:**
```java
// line 41
if( first_name.equalsIgnoreCase("") )

// line 47
if( last_name.equalsIgnoreCase("") )

// line 53
if (!pass.equalsIgnoreCase(cpass)) {
```
If `first_name`, `last_name`, `pass`, or `cpass` is absent from the HTTP request, Struts sets the field to `null`. Calling `.equalsIgnoreCase()` on a null reference throws `NullPointerException`, which in Struts 1 typically results in a 500 error rather than a validation error. This can be triggered intentionally by an attacker to cause application errors or bypass validation logic.
**Recommendation:** Add explicit null checks (e.g., `first_name == null || first_name.isEmpty()`) before invoking instance methods, or use a utility such as `StringUtils.isBlank()`. Mirror the same pattern for `pass` and `cpass`.

---

#### FINDING IV-2

**Severity:** HIGH
**File+Line:** `src/main/java/com/actionform/AdminDriverAddForm.java`, lines 29, 36
**Description:** `app_access` and `op_code` accept arbitrary user-supplied strings with no whitelist validation.
**Evidence:**
```java
private String app_access = null;   // line 29
private String op_code    = null;   // line 36
```
`app_access` appears to be an access-level or role flag. `op_code` is an operator code. Neither field is checked in `validate()`, nor is either covered by `validation.xml`. An attacker can submit any string value, potentially elevating privileges (by setting `app_access` to an admin-level value) or injecting unexpected data into the operator-code field.
**Recommendation:** Validate both fields against an explicit whitelist of permitted values in `validate()`. If `app_access` carries access-level semantics, see also FINDING SF-1 below.

---

#### FINDING IV-3

**Severity:** MEDIUM
**File+Line:** `src/main/java/com/actionform/AdminDriverAddForm.java`, lines 31, 30, 25, 26, 27
**Description:** No format or length validation on `email_addr`, `mobile`, `licence_number`, `expiry_date`, or `security_number`.
**Evidence:** The `validate()` method (lines 38–59) contains no checks for these fields. The `validation.xml` file contains no entry for `AdminDriverAddForm` at all. All five fields accept arbitrary-length, arbitrary-content strings.
**Consequences:**
- Oversized inputs can cause database truncation errors or silent data corruption.
- Malformed email addresses are accepted and stored.
- `expiry_date` is a free-form string; malformed dates can cause downstream parsing failures.
- `security_number` is sensitive and should at minimum be length-constrained.
**Recommendation:** Add `required`/`maxlength`/`email`/`mask` rules to `validation.xml` for this form, or add explicit checks in `validate()`.

---

#### FINDING IV-4

**Severity:** MEDIUM
**File+Line:** `src/main/java/com/actionform/AdminDriverAddForm.java`, line 32
**Description:** No minimum password length or complexity validation.
**Evidence:**
```java
if (!pass.equalsIgnoreCase(cpass)) {   // line 53 — only checks match, not strength
```
The sole password check is equality of `pass` and `cpass`. There is no minimum length, no complexity requirement, and no maximum length cap (which would mitigate bcrypt-DoS if hashing is applied downstream). A driver account can be created with an empty string password as long as both fields are submitted empty.
**Recommendation:** Add a minimum length check (e.g., 8 characters) and optionally a complexity rule. Add a maximum length cap (e.g., 72 characters) to guard against hashing-layer DoS.

---

#### FINDING IV-5

**Severity:** LOW
**File+Line:** `src/main/webapp/WEB-INF/validation.xml` (absence of entry)
**Description:** `AdminDriverAddForm` has no entry in `validation.xml`.
**Evidence:** `validation.xml` defines rules for `loginActionForm`, `adminRegisterActionForm`, and `AdminDriverEditForm` only. `AdminDriverAddForm` is absent.
**Recommendation:** Add a `<form name="AdminDriverAddForm">` block to `validation.xml` covering at minimum `first_name` (required), `last_name` (required), `email_addr` (required, email format), `mobile` (mask/integer), and length constraints on all string fields.

---

### Category 2 — Type Safety

---

#### FINDING TS-1

**Severity:** HIGH
**File+Line:** `src/main/java/com/actionform/AdminDriverAddForm.java`, line 22
**Description:** The `id` field is typed as `Long`; Struts 1's BeanUtils binding throws `NumberFormatException` (wrapped as a Struts `ActionError`) when the submitted value is non-numeric. However, the form has no validation guard for this field, and a malformed value bypasses the normal validate() path, potentially causing unhandled exceptions depending on Struts error-handling configuration.
**Evidence:**
```java
private Long id = null;   // line 22
```
Struts 1 uses `BeanUtils.populate()` to bind request parameters. A non-numeric string submitted for `id` causes a conversion exception. Because `validate()` never checks `id`, any downstream code that calls `getDriverBean()` and passes the (null or garbage) `id` to a persistence layer may behave unexpectedly.
**Recommendation:** Add a numeric check in `validate()` for `id` if it is expected to be provided by the user. If `id` should be server-generated, remove it from the form entirely (see FINDING IDOR-1).

---

#### FINDING TS-2

**Severity:** LOW
**File+Line:** `src/main/java/com/actionform/AdminDriverAddForm.java`, line 53
**Description:** Password comparison uses `equalsIgnoreCase()`, making password matching case-insensitive.
**Evidence:**
```java
if (!pass.equalsIgnoreCase(cpass)) {   // line 53
```
Using a case-insensitive comparison for passwords reduces the effective keyspace. A password set as `"Secret1"` will match `"secret1"`, `"SECRET1"`, etc., which weakens credential security.
**Recommendation:** Replace with `pass.equals(cpass)` (strict case-sensitive comparison).

---

### Category 3 — IDOR Risk

---

#### FINDING IDOR-1

**Severity:** HIGH
**File+Line:** `src/main/java/com/actionform/AdminDriverAddForm.java`, line 22
**Description:** The `id` field is a user-controllable Long that is passed directly into the `DriverBean` via `getDriverBean()` with no authorization check.
**Evidence:**
```java
private Long id = null;   // line 22 — bound from HTTP request parameter

// lines 62–78: passed directly to DriverBean
DriverBean driverBean = DriverBean.builder()
    .id(id)
    ...
    .build();
```
On an "Add" form, the driver `id` should be server-generated (typically by the database). Exposing it as a form field means an attacker can submit an arbitrary `id` value, potentially causing the persistence layer to overwrite an existing driver record belonging to a different company rather than inserting a new one — a classic IDOR/forced-write scenario.
**Recommendation:** Remove the `id` field from the form. The `id` for a newly created record should be assigned by the database. If an `id` is legitimately needed (e.g., for updates routed through this form), validate that the `id` belongs to the authenticated user's company before any persistence operation.

---

### Category 4 — Data Integrity

---

#### FINDING DI-1

**Severity:** HIGH
**File+Line:** `src/main/java/com/actionform/AdminDriverAddForm.java`, line 29
**Description:** `app_access` accepts arbitrary free-form input with no whitelist enforcement, creating a data integrity risk for access-control semantics.
**Evidence:**
```java
private String app_access = null;   // line 29
```
If `app_access` controls whether the driver has access to the mobile application (or controls access level within it), accepting any string means an attacker can inject values outside the intended domain (e.g., `"admin"`, `"superuser"`, or SQL/injection payloads). There is no validation in `validate()` and no `validation.xml` rule.
**Recommendation:** Constrain `app_access` to a server-side whitelist (e.g., `"Y"/"N"` or defined role codes). Reject any value not on the whitelist in `validate()`.

---

#### FINDING DI-2

**Severity:** MEDIUM
**File+Line:** `src/main/java/com/actionform/AdminDriverAddForm.java`, line 36
**Description:** `op_code` is unconstrained and not validated, risking data integrity for operator assignment logic.
**Evidence:**
```java
private String op_code = null;   // line 36
```
`op_code` likely references an operator or operational category. Without whitelist validation, arbitrary strings can be submitted, potentially corrupting operator assignment logic or enabling injection via the field value downstream.
**Recommendation:** Validate `op_code` against a known set of valid codes. If codes are dynamic, validate existence against the database server-side (with company-scoping to prevent cross-tenant injection).

---

### Category 5 — Sensitive Fields

---

#### FINDING SF-1

**Severity:** CRITICAL
**File+Line:** `src/main/java/com/actionform/AdminDriverAddForm.java`, line 29
**Description:** `app_access` — a field that appears to govern whether the driver has access to the application — is accepted entirely from user input with no server-side authority check.
**Evidence:**
```java
private String app_access = null;   // line 29 — bound from HTTP request
```
The form passes `app_access` directly into `DriverBean` (line 74 via builder). If this field controls application access or access level, allowing the form submitter to freely set it means any admin user (or attacker who bypasses the session check) can grant arbitrary access levels when creating a driver. There is no server-side enforcement that the submitted value is within the range the acting admin is permitted to assign.
**Recommendation:** Remove `app_access` from client-controlled input. Set it server-side based on business logic, or if the admin must choose a value, enforce a whitelist and verify the acting admin has authority to assign the chosen level.

---

#### FINDING SF-2

**Severity:** HIGH
**File+Line:** `src/main/java/com/actionform/AdminDriverAddForm.java`, line 27
**Description:** `security_number` is a potentially sensitive identifier (employee security number or government ID) accepted as free-form, unconstrained user input.
**Evidence:**
```java
private String security_number = null;   // line 27
```
There is no length constraint, format mask, or validation of any kind on this field. Depending on what this number represents (e.g., a national insurance number, SSN, or employee ID), storing arbitrary input without validation risks both data quality problems and injection attacks downstream.
**Recommendation:** Apply a format mask (e.g., alphanumeric only, maximum length matching the expected identifier format) in `validate()` or `validation.xml`. Treat this field as sensitive and ensure it is not logged (note `log.debug("driverBean : " + driverBean)` on line 80 — if `DriverBean.toString()` includes `security_number`, this will be written to debug logs in plaintext).

---

#### FINDING SF-3

**Severity:** HIGH
**File+Line:** `src/main/java/com/actionform/AdminDriverAddForm.java`, lines 32–33
**Description:** `pass` and `cpass` are plaintext password fields on the form object. The Lombok `@Getter`/`@Setter` annotations generate public accessors for them, and they are passed into `DriverBean` (lines 75–76). The debug log on line 80 may expose passwords in plaintext if `DriverBean.toString()` includes them.
**Evidence:**
```java
private String pass  = null;   // line 32
private String cpass = null;   // line 33
...
.pass(pass)    // line 75
.cpass(cpass)  // line 76
...
log.debug("driverBean : " + driverBean);   // line 80
```
**Recommendation:** Ensure `DriverBean.toString()` (likely Lombok-generated) explicitly excludes `pass` and `cpass` using `@ToString.Exclude`. Passwords should be hashed at the earliest possible point — ideally in the action class before the bean is constructed — rather than carried through the bean in plaintext. Add `@ToString.Exclude` to the `pass`/`cpass` fields in this form as well to prevent accidental logging.

---

#### FINDING SF-4

**Severity:** INFO
**File+Line:** `src/main/java/com/actionform/AdminDriverAddForm.java`, lines 61–83
**Description:** `comp_id` is correctly sourced from the session (`sessCompId` parameter) rather than from user input, which is the appropriate pattern. This is a positive finding and confirms company isolation at the form level for this specific field.
**Evidence:**
```java
public DriverBean getDriverBean(String sessCompId) {
    ...
    .comp_id(sessCompId)   // line 77 — sourced from session, not form field
    ...
}
```
**Recommendation:** No action required for this field. Document this as the expected pattern for all tenant-scoping fields across the application.

---

### Category 6 — CSRF

**Note (structural):** As documented in the stack context, there is no CSRF protection anywhere in this application. This form, like all mutation forms in the codebase, is vulnerable to cross-site request forgery. Any admin authenticated to the application can be tricked into submitting this form by a malicious third-party page. This is a structural gap and is recorded here for completeness rather than as a new finding specific to this file. See the application-level CSRF finding in the access audit.

---

## SUMMARY TABLE

| ID       | Severity | Title                                                              |
|----------|----------|--------------------------------------------------------------------|
| IV-1     | HIGH     | NullPointerException in validate() — missing null guards           |
| IV-2     | HIGH     | app_access and op_code accept arbitrary strings — no whitelist     |
| IV-3     | MEDIUM   | No format/length validation on email, mobile, licence, date, security_number |
| IV-4     | MEDIUM   | No password minimum length or complexity check                     |
| IV-5     | LOW      | AdminDriverAddForm absent from validation.xml                      |
| TS-1     | HIGH     | Long id field throws NumberFormatException on non-numeric input    |
| TS-2     | LOW      | Password comparison uses case-insensitive equalsIgnoreCase()       |
| IDOR-1   | HIGH     | User-controllable id field passed directly to DriverBean — forced overwrite risk |
| DI-1     | HIGH     | app_access free-form — no whitelist, data integrity risk           |
| DI-2     | MEDIUM   | op_code unconstrained — data integrity risk                        |
| SF-1     | CRITICAL | app_access governs app access but is fully user-controlled         |
| SF-2     | HIGH     | security_number is sensitive, unconstrained, potentially logged    |
| SF-3     | HIGH     | pass/cpass carried in plaintext through DriverBean, at risk of debug log exposure |
| SF-4     | INFO     | comp_id correctly sourced from session — positive finding          |

---

## FINDING COUNT BY SEVERITY

| Severity | Count |
|----------|-------|
| CRITICAL | 1     |
| HIGH     | 7     |
| MEDIUM   | 3     |
| LOW      | 2     |
| INFO     | 1     |
| **TOTAL**| **14**|
