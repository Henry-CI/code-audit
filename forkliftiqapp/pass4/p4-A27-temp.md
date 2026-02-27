# Audit Report — Pass 4 (Code Quality)
**Agent:** A27
**Audit Run:** 2026-02-26-01
**Date:** 2026-02-27
**Assigned Files:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/ServiceRecordItem.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/ServiceSummaryItem.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/TrainingItem.java`

---

## Step 1: Reading Evidence

### File 1: ServiceRecordItem.java

**Class:** `ServiceRecordItem implements Serializable`

**Fields (all public):**
- `double acc_hours` (line 14)
- `String unit_name` (line 15)
- `double service_due` (line 16)
- `int last_serv` (line 17)
- `int next_serv` (line 18)
- `int serv_duration` (line 19)
- `String service_type` (line 20)
- `int unit_id` (line 21)

**Methods:**
- `ServiceRecordItem()` — no-arg constructor, line 23
- `ServiceRecordItem(JSONObject jsonObject) throws JSONException` — deserializing constructor, line 26

**Types / Constants / Enums / Interfaces:** None defined.

**Imports:**
- `org.json.JSONException` — used
- `org.json.JSONObject` — used
- `java.io.Serializable` — used
- `org.json.JSONArray` — NOT used in this file
- `java.util.ArrayList` — NOT used in this file
- `java.math.BigDecimal` — NOT used in this file
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` — wildcard, same package; nothing from this wildcard is referenced in this file
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` — wildcard; nothing from this wildcard is referenced in this file

---

### File 2: ServiceSummaryItem.java

**Class:** `ServiceSummaryItem implements Serializable`

**Fields (all public):**
- `int unit_id` (line 14)
- `int acc_hours` (line 15)
- `int service_due` (line 16)
- `int last_serv` (line 17)
- `int next_serv` (line 18)
- `int serv_duration` (line 19)
- `String unit_name` (line 20)
- `String service_type` (line 21)

**Methods:**
- `ServiceSummaryItem()` — no-arg constructor, line 23
- `ServiceSummaryItem(JSONObject jsonObject) throws JSONException` — deserializing constructor, line 26

**Types / Constants / Enums / Interfaces:** None defined.

**Imports:**
- `org.json.JSONException` — used
- `org.json.JSONObject` — used
- `java.io.Serializable` — used
- `org.json.JSONArray` — NOT used in this file
- `java.util.ArrayList` — NOT used in this file
- `java.math.BigDecimal` — NOT used in this file
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` — wildcard, same package; nothing from this wildcard is referenced in this file
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` — wildcard; nothing from this wildcard is referenced in this file

---

### File 3: TrainingItem.java

**Class:** `TrainingItem implements Serializable`

**Fields (all public):**
- `int manufacture_id` (line 10)
- `int type_id` (line 11)
- `int fuel_type_id` (line 12)
- `String training_date` (line 13)
- `String expiration_date` (line 14)

**Methods:**
- `TrainingItem()` — no-arg constructor, line 16
- `TrainingItem(JSONObject jsonObject) throws JSONException` — deserializing constructor, line 19

**Types / Constants / Enums / Interfaces:** None defined.

**Imports:**
- `org.json.JSONException` — used
- `org.json.JSONObject` — used
- `java.io.Serializable` — used

---

## Step 2 & 3: Findings

---

### A27-1 — HIGH: Type mismatch between sibling classes for `acc_hours` and `service_due`

**File:** `ServiceRecordItem.java` (lines 14, 16) vs `ServiceSummaryItem.java` (lines 15, 16)

`ServiceRecordItem` declares `acc_hours` and `service_due` as `double`. The sibling class `ServiceSummaryItem`, which represents the same conceptual domain (service scheduling data for the same JSON API), declares both as `int`.

Both fields are deserialized from the same JSON key names (`"acc_hours"`, `"service_due"`), implying the same API endpoint or the same data model.

**Impact:** The `ServiceRecordFragment.getStatus()` method (line 57) uses `ServiceRecordItem.acc_hours` and `service_due` in comparisons where the result is compared to `SERVICE_DUE_HOURS`. Arithmetic computed from `double` fields (e.g., `ServiceEditFragment` line 316, 324) will behave differently than `int` arithmetic. If `ServiceSummaryItem` values are ever substituted or compared, truncation silently discards fractional hours. This is a data-integrity defect: one class will silently drop precision that the other preserves, or one is wrong about what the API actually returns.

---

### A27-2 — MEDIUM: Unused imports in ServiceRecordItem.java and ServiceSummaryItem.java (five each)

**Files:**
- `ServiceRecordItem.java` lines 6–10
- `ServiceSummaryItem.java` lines 6–10

Both files import the following symbols that are never referenced anywhere in the file body:

| Import | Line |
|---|---|
| `org.json.JSONArray` | 6 |
| `java.util.ArrayList` | 7 |
| `java.math.BigDecimal` | 8 |
| `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` | 9 |
| `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` | 10 |

The wildcard import on line 9 is importing from the same package the class lives in; Java automatically resolves same-package names without an explicit import, making this redundant even if it were used. The wildcard on line 10 pulls in the entire `results` subpackage (22 classes) with no usage.

These imports generate IDE warnings and obscure which external types a class actually depends on. They are present in both `ServiceRecordItem` and `ServiceSummaryItem` identically, suggesting they were copy-pasted from a template or another file without cleanup.

`TrainingItem.java` does not have this problem.

---

### A27-3 — MEDIUM: All fields are public with no encapsulation across all three classes

**Files:** All three (`ServiceRecordItem.java`, `ServiceSummaryItem.java`, `TrainingItem.java`)

Every data field in all three classes is declared `public` with no getter/setter methods. These classes are `Serializable` data transfer objects, and public fields are common in simple DTOs. However, across the codebase callers mutate fields directly (e.g., `ServiceEditFragment` lines 315–316, 324 write back to `getCurrentRecordItem().service_due` and `acc_hours`). This means no validation, no change notification, and no ability to add logic without breaking all call sites. The pattern is at least consistent across all three classes, but it is a known leaky abstraction: internal JSON-mapped storage layout is fully exposed as the public API.

---

### A27-4 — MEDIUM: Inconsistent indentation style between files

**Files:** `ServiceRecordItem.java` / `ServiceSummaryItem.java` vs `TrainingItem.java`

`ServiceRecordItem.java` and `ServiceSummaryItem.java` use tab indentation with opening braces on the same line as the class declaration but a new line after method signatures (Allman-style for methods, K&R-style for the class). `TrainingItem.java` uses four-space indentation consistently throughout.

Specifically:
- `ServiceRecordItem` line 12: class brace on same line; method brace on new line (line 27 vs 26).
- `TrainingItem` line 8: class brace on same line; method brace on new line (line 20 vs 19) — uses spaces, not tabs.

Additionally, lines 30 and 35 in both `ServiceRecordItem` and `ServiceSummaryItem` contain a leading tab followed by a blank line (visible as a whitespace-only line 30 with `\t` prefix), whereas `TrainingItem` line 23 is a clean empty line. This is minor but indicates the two files were authored or generated differently from the third.

---

### A27-5 — LOW: Field declaration order differs between ServiceRecordItem and ServiceSummaryItem for shared fields

**Files:** `ServiceRecordItem.java` (lines 14–21) vs `ServiceSummaryItem.java` (lines 14–21)

Both classes have an identical set of eight fields (`unit_id`, `unit_name`, `acc_hours`, `service_due`, `last_serv`, `next_serv`, `serv_duration`, `service_type`). However, their declaration order differs:

`ServiceRecordItem` order:
`acc_hours`, `unit_name`, `service_due`, `last_serv`, `next_serv`, `serv_duration`, `service_type`, `unit_id`

`ServiceSummaryItem` order:
`unit_id`, `acc_hours`, `service_due`, `last_serv`, `next_serv`, `serv_duration`, `unit_name`, `service_type`

Inconsistent field ordering between structurally identical sibling classes makes cross-class comparison harder and suggests the classes evolved independently rather than from a shared model. This is a style inconsistency (same pattern done differently).

---

### A27-6 — LOW: `manufacture_id` is a misspelling of `manufacturer_id` in TrainingItem

**File:** `TrainingItem.java` line 10

The field `manufacture_id` maps to the JSON key `"manufacture_id"` (line 24). The intended concept is almost certainly a manufacturer identifier. The word "manufacture" is a verb; the noun form is "manufacturer". This misspelling propagates through all consumers (`LoginItem.java` line 64 and any UI code). If the server-side API corrects the key name to `"manufacturer_id"`, deserialization will silently stop populating this field with no compile-time error, because it is a string-key lookup.

---

## Summary Table

| ID | Severity | File(s) | Issue |
|---|---|---|---|
| A27-1 | HIGH | ServiceRecordItem.java, ServiceSummaryItem.java | `acc_hours` and `service_due` typed as `double` in one class, `int` in the other — same API fields |
| A27-2 | MEDIUM | ServiceRecordItem.java, ServiceSummaryItem.java | Five unused imports each, including wildcard same-package import and wildcard results subpackage import |
| A27-3 | MEDIUM | All three files | All fields are `public` with direct mutation at call sites — no encapsulation |
| A27-4 | MEDIUM | All three files | Inconsistent indentation style (tabs vs spaces) between the two Service*Item files and TrainingItem |
| A27-5 | LOW | ServiceRecordItem.java, ServiceSummaryItem.java | Shared fields declared in different order between sibling classes |
| A27-6 | LOW | TrainingItem.java | `manufacture_id` is a misspelling; should be `manufacturer_id` |
