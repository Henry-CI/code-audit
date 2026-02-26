# Pass 3 Documentation Audit — Agent A44
**Audit run:** 2026-02-26-01
**Files:** bean/CompEntityRelBean.java, bean/CompanyBean.java, bean/DateFormatBean.java

---

## 1. Reading Evidence

### 1.1 CompEntityRelBean.java

**Class:** `CompEntityRelBean` — line 3

**Fields:**

| Field | Type | Line |
|-------|------|------|
| `id` | `String` | 4 |
| `comp_id` | `String` | 5 |
| `entity_id` | `String` | 6 |
| `entityname` | `String` | 7 |
| `compname` | `String` | 8 |

**Methods (all public):**

| Method | Line |
|--------|------|
| `getId()` | 10 |
| `setId(String id)` | 13 |
| `getComp_id()` | 16 |
| `setComp_id(String comp_id)` | 19 |
| `getEntity_id()` | 22 |
| `setEntity_id(String entity_id)` | 25 |
| `getEntityname()` | 28 |
| `setEntityname(String entityname)` | 31 |
| `getCompname()` | 34 |
| `setCompname(String compname)` | 37 |

---

### 1.2 CompanyBean.java

**Class:** `CompanyBean` — line 13
**Annotations:** `@Data`, `@NoArgsConstructor`
**Implements:** `Serializable`

**Fields:**

| Field | Type | Line |
|-------|------|------|
| `serialVersionUID` | `static final long` | 15 |
| `id` | `String` | 17 |
| `name` | `String` | 18 |
| `address` | `String` | 19 |
| `suburb` | `String` | 20 |
| `postcode` | `String` | 21 |
| `email` | `String` | 22 |
| `contact_no` | `String` | 23 |
| `password` | `String` | 24 |
| `pin` | `String` | 25 |
| `refnm` | `String` | 26 |
| `refno` | `String` | 27 |
| `contact_fname` | `String` | 28 |
| `contact_lname` | `String` | 29 |
| `question` | `String` | 30 |
| `answer` | `String` | 31 |
| `unit` | `String` | 32 |
| `subemail` | `String` | 33 |
| `timezone` | `String` | 34 |
| `timezoneName` | `String` | 35 |
| `dateFormat` | `String` | 36 |
| `maxSessionLength` | `Integer` | 37 |
| `lan_id` | `String` | 38 |
| `privacy` | `boolean` | 39 |
| `template` | `String` | 40 |
| `authority` | `String` | 41 |
| `mobile` | `String` | 42 |
| `cognito_username` | `String` | 43 |
| `roleIds` | `String[]` | 46 (`@Deprecated`) |
| `roles` | `List<RoleBean>` | 48 |

**Methods:**

| Method | Visibility | Line | Notes |
|--------|-----------|------|-------|
| `CompanyBean(...)` (all-args builder constructor) | `private` | 51 | `@Builder` annotation |
| Lombok-generated getters/setters/equals/hashCode/toString | generated | — | Via `@Data` |
| Lombok-generated no-args constructor | generated | — | Via `@NoArgsConstructor` |

---

### 1.3 DateFormatBean.java

**Class:** `DateFormatBean` — line 13
**Annotations:** `@Data`, `@NoArgsConstructor`
**Implements:** `Serializable`

**Fields:**

| Field | Type | Line |
|-------|------|------|
| `serialVersionUID` | `static final long` | 14 |
| `format` | `String` | 16 |

**Methods:**

| Method | Visibility | Line | Notes |
|--------|-----------|------|-------|
| `DateFormatBean(String format)` | `private` | 19 | `@Builder` annotation |
| `getExample()` | `public` | 23 | Non-trivial; uses `Calendar` + `SimpleDateFormat` |
| Lombok-generated `getFormat()`, `setFormat()`, `equals()`, `hashCode()`, `toString()` | generated | — | Via `@Data` |
| Lombok-generated no-args constructor | generated | — | Via `@NoArgsConstructor` |

---

## 2. Findings

### A44-1 [LOW] CompEntityRelBean — No class-level Javadoc

**File:** `bean/CompEntityRelBean.java`, line 3
**Severity:** LOW

`CompEntityRelBean` has no class-level Javadoc comment. There is no description of what the class represents (a join/relationship between a company entity and a company record), the data it models, or its intended usage context.

---

### A44-2 [LOW] CompEntityRelBean — Undocumented getter/setter methods

**File:** `bean/CompEntityRelBean.java`, lines 10–38
**Severity:** LOW

All ten public accessor methods (`getId`, `setId`, `getComp_id`, `setComp_id`, `getEntity_id`, `setEntity_id`, `getEntityname`, `setEntityname`, `getCompname`, `setCompname`) lack Javadoc. These are trivial getters/setters, so the severity is LOW per audit norms.

---

### A44-3 [LOW] CompanyBean — No class-level Javadoc

**File:** `bean/CompanyBean.java`, line 13
**Severity:** LOW

`CompanyBean` has no class-level Javadoc. The class carries a broad set of company-related fields (authentication credentials, contact details, session settings, locale configuration, roles), and a brief description of its purpose and usage context is absent.

---

### A44-4 [LOW] CompanyBean — @Deprecated field `roleIds` has no deprecation explanation

**File:** `bean/CompanyBean.java`, line 46
**Severity:** LOW

The field `String[] roleIds` is annotated `@Deprecated` but carries no Javadoc comment explaining why it was deprecated, what supersedes it (presumably the `List<RoleBean> roles` field at line 48), or whether it is scheduled for removal. Without documentation, callers cannot safely reason about migration.

---

### A44-5 [MEDIUM] CompanyBean — Builder constructor parameter name mismatch for `dateFormat` and `maxSessionLength`

**File:** `bean/CompanyBean.java`, lines 51–79
**Severity:** MEDIUM

The `@Builder`-annotated private constructor uses parameter names `date_format` (line 51) and `max_session_length` (line 51) which are assigned to fields `this.dateFormat` (line 74) and `this.maxSessionLength` (line 75) respectively. All other parameters use camelCase names identical to their corresponding fields. This inconsistency between the builder parameter names and the field names they populate is undocumented and can confuse callers constructing `CompanyBean` via the Lombok builder. There is no Javadoc explaining the discrepancy or noting the builder parameter names that must be used.

---

### A44-6 [LOW] DateFormatBean — No class-level Javadoc

**File:** `bean/DateFormatBean.java`, line 13
**Severity:** LOW

`DateFormatBean` has no class-level Javadoc. A brief description of the class's role (holding a date-format pattern string and providing a formatted example date) would aid callers.

---

### A44-7 [MEDIUM] DateFormatBean.getExample() — Undocumented non-trivial public method

**File:** `bean/DateFormatBean.java`, lines 23–31
**Severity:** MEDIUM

`getExample()` is a public, non-trivial method with no Javadoc. The method:
- Constructs a `Calendar` instance and hard-codes a specific reference date (December 31, hour 23, minute 59, second 59).
- Applies `this.format` (a `SimpleDateFormat` pattern) to that fixed date.
- Returns the resulting formatted string.

The absence of documentation leaves several questions unanswered:
1. There is no `@return` tag explaining what is returned or that the example is always based on December 31.
2. The year component of the example date is whatever `Calendar.getInstance()` produces for the current year — the year is never explicitly set. This means the returned example string is year-sensitive when the format pattern includes a year token (e.g., `yyyy`). This subtle behaviour is not documented.
3. The method uses `Calendar.HOUR` (12-hour clock, 0–11) rather than `Calendar.HOUR_OF_DAY`. Setting `HOUR` to 23 will silently wrap to 11 (23 mod 12 = 11). Any format using `HH` (24-hour) will therefore show `11:59:59`, not `23:59:59`. This is likely a latent bug, but at minimum the undocumented behaviour qualifies as MEDIUM — a documented intent of "23:59:59" that silently produces "11:59:59" for 24-hour patterns borders on HIGH. Raising as MEDIUM pending confirmation of intent.

---

### A44-8 [LOW] DateFormatBean — Undocumented `format` field

**File:** `bean/DateFormatBean.java`, line 16
**Severity:** LOW

The field `format` has no Javadoc. A note that it holds a `SimpleDateFormat`-compatible pattern string would aid users of the Lombok-generated `setFormat` and the `getExample` method.

---

## 3. Summary Table

| ID | File | Element | Severity | Issue |
|----|------|---------|----------|-------|
| A44-1 | CompEntityRelBean.java | Class | LOW | No class-level Javadoc |
| A44-2 | CompEntityRelBean.java | All 10 getters/setters | LOW | No Javadoc on trivial accessor methods |
| A44-3 | CompanyBean.java | Class | LOW | No class-level Javadoc |
| A44-4 | CompanyBean.java | `roleIds` field (line 46) | LOW | `@Deprecated` with no explanation or migration guidance |
| A44-5 | CompanyBean.java | Builder constructor (line 51) | MEDIUM | Undocumented parameter-name mismatch (`date_format`, `max_session_length`) vs. field names |
| A44-6 | DateFormatBean.java | Class | LOW | No class-level Javadoc |
| A44-7 | DateFormatBean.java | `getExample()` (lines 23–31) | MEDIUM | Undocumented non-trivial public method; latent `HOUR` vs. `HOUR_OF_DAY` bug undocumented; year not fixed |
| A44-8 | DateFormatBean.java | `format` field (line 16) | LOW | No Javadoc on field holding `SimpleDateFormat` pattern |

**Totals:** 2 MEDIUM, 6 LOW
