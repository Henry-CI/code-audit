# Audit Report — Pass 4 (Code Quality)
**Audit Run:** 2026-02-26-01
**Agent:** A32
**Date:** 2026-02-27
**Files Audited:** 3

---

## Section 1 — Reading Evidence

### File 1: SaveServiceDurationParameter.java

**Full path:**
`app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SaveServiceDurationParameter.java`

**Class:** `SaveServiceDurationParameter`
- Extends: `WebServiceParameterPacket`
- Implements: `Serializable`
- Lines: 1–23

**Fields (all public):**
| Line | Name | Type |
|------|------|------|
| 14 | `unit_id` | `int` |
| 15 | `acc_hours` | `double` |
| 16 | `last_serv` | `int` |
| 17 | `service_type` | `String` |
| 18 | `serv_duration` | `int` |
| 19 | `driver_id` | `int` |

**Methods:**
| Line | Signature |
|------|-----------|
| 21–22 | `SaveServiceDurationParameter()` — no-arg constructor, empty body |

**Types / constants / enums defined:** None.

**Imports present (lines 3–10):**
- `org.json.JSONException` (line 3)
- `org.json.JSONObject` (line 4)
- `java.io.Serializable` (line 5)
- `org.json.JSONArray` (line 6)
- `java.util.ArrayList` (line 7)
- `java.math.BigDecimal` (line 8)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` (line 9)
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` (line 10)

---

### File 2: SaveServiceHoursParameter.java

**Full path:**
`app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SaveServiceHoursParameter.java`

**Class:** `SaveServiceHoursParameter`
- Extends: `WebServiceParameterPacket`
- Implements: `Serializable`
- Lines: 1–23

**Fields (all public):**
| Line | Name | Type |
|------|------|------|
| 14 | `unit_id` | `int` |
| 15 | `acc_hours` | `double` |
| 16 | `last_serv` | `int` |
| 17 | `service_type` | `String` |
| 18 | `next_serv` | `int` |
| 19 | `driver_id` | `int` |

**Methods:**
| Line | Signature |
|------|-----------|
| 21–22 | `SaveServiceHoursParameter()` — no-arg constructor, empty body |

**Types / constants / enums defined:** None.

**Imports present (lines 3–10):** Identical set to File 1.

---

### File 3: SaveSessionsParameter.java

**Full path:**
`app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SaveSessionsParameter.java`

**Class:** `SaveSessionsParameter`
- Extends: `WebServiceParameterPacket`
- Implements: `Serializable`
- Lines: 1–19

**Fields (all public):**
| Line | Name | Type |
|------|------|------|
| 14 | `sessions` | `SaveSessionItem` |
| 15 | `results` | `SavePreStartItem` |

**Methods:**
| Line | Signature |
|------|-----------|
| 17–18 | `SaveSessionsParameter()` — no-arg constructor, empty body |

**Types / constants / enums defined:** None.

**Imports present (lines 3–10):** Identical set to Files 1 and 2.

---

### Supporting Context Read

- **`WebServicePacket`** (base): implements `Serializable` at line 6.
- **`WebServiceParameterPacket`** (middle): extends `WebServicePacket`, also declares `implements Serializable`.
- **`SaveSessionItem`**: implements `Serializable`; fields: `id`, `driver_id`, `unit_id`, `start_time`, `finish_time`, `prestart_required`.
- **`SavePreStartItem`**: implements `Serializable`; fields: `start_time`, `finish_time`, `comment`, `session_id`, `arrAnswers`.
- Caller `SyncService.java` populates `SaveSessionsParameter.sessions` (a single `SaveSessionItem`) and `SaveSessionsParameter.results` (a single `SavePreStartItem`).
- Caller `ServiceEditFragment.java` populates `SaveServiceHoursParameter.next_serv` and `SaveServiceDurationParameter.serv_duration`.

---

## Section 2 — Findings

---

### A32-1 — MEDIUM: Massive unused import block across all three files (and the whole package)

**Affected files:**
- `SaveServiceDurationParameter.java` lines 3–10
- `SaveServiceHoursParameter.java` lines 3–10
- `SaveSessionsParameter.java` lines 3–10

**Detail:**
All three files share an identical 8-import boilerplate block. Of those 8 imports, only `java.io.Serializable` (line 5) and the `webserviceclasses.*` wildcard (line 9) are actually used. The remaining five imports — `org.json.JSONException`, `org.json.JSONObject`, `org.json.JSONArray`, `java.util.ArrayList`, and `java.math.BigDecimal` — are never referenced in any of these three files. `SaveSessionsParameter` additionally does not directly use anything from the `results.*` wildcard import (line 10); `SaveServiceDurationParameter` and `SaveServiceHoursParameter` also do not reference any `results.*` type.

This boilerplate block appears to have been copy-pasted from a code generator or from data-bearing classes (like `SaveSessionItem`) that DO use JSON parsing and `ArrayList`. The parameter classes themselves contain no parsing logic and never reference these types.

**Risk:** Unused imports pollute the namespace, confuse IDEs, trigger compiler warnings (`-Xlint:imports`), and mislead future developers about which dependencies the class actually has. The `java.math.BigDecimal` import is particularly misleading for classes that hold only `int` and `double` fields.

**Recommendation:** Remove all imports except `java.io.Serializable` and the `webserviceclasses.*` wildcard (which provides `WebServiceParameterPacket`). For `SaveSessionsParameter`, `SaveSessionItem` and `SavePreStartItem` are in the `webserviceclasses` package so they are covered by the `webserviceclasses.*` wildcard; the `results.*` wildcard can be removed.

---

### A32-2 — MEDIUM: Redundant `implements Serializable` declaration at every level of the hierarchy

**Affected files:**
- `SaveServiceDurationParameter.java` line 12
- `SaveServiceHoursParameter.java` line 12
- `SaveSessionsParameter.java` line 12
- (context: also present in `WebServiceParameterPacket` and `WebServicePacket`)

**Detail:**
The inheritance chain is: `WebServicePacket implements Serializable` → `WebServiceParameterPacket extends WebServicePacket implements Serializable` → all three audited classes `extends WebServiceParameterPacket implements Serializable`. Because `Serializable` is already declared at the root (`WebServicePacket`), every subclass automatically inherits that interface. Re-declaring `implements Serializable` on every subclass is redundant, adds no semantic value, and creates a false impression that the serialization contract is a per-class decision rather than a hierarchy-wide one.

**Recommendation:** Remove the `implements Serializable` clause from the three audited classes and from `WebServiceParameterPacket`. The interface is already satisfied via `WebServicePacket`.

---

### A32-3 — MEDIUM: Asymmetric field naming between two sibling classes representing the same domain concept

**Affected files:**
- `SaveServiceDurationParameter.java` line 18: `public int serv_duration;`
- `SaveServiceHoursParameter.java` line 18: `public int next_serv;`

**Detail:**
`SaveServiceDurationParameter` and `SaveServiceHoursParameter` are sibling classes (same parent, same package, same caller) representing two variants of a service threshold: one expressed as a duration interval and one as an absolute next-service value. Five of their six fields are identical (`unit_id`, `acc_hours`, `last_serv`, `service_type`, `driver_id`). The sixth field — the only one that differs — uses inconsistent naming: `serv_duration` in one class versus `next_serv` in the other. The prefixes are from different naming systems (`serv_` vs the standalone `next_`), and neither name clearly signals the unit of measurement (hours? minutes?).

Confirmed in caller `ServiceEditFragment.java`:
- Line 288: `parameter.next_serv = serviceInterval;`
- Line 299: `parameter.serv_duration = serviceInterval;`

Both are assigned from the same local variable `serviceInterval`, making the intent of the naming difference especially unclear.

**Recommendation:** Adopt a single naming convention for the varying field across both classes, e.g., `service_interval` (for duration-based) and `next_service_hours` (for hours-based), and update callers accordingly.

---

### A32-4 — LOW: Misleading field name `results` in `SaveSessionsParameter`

**Affected file:** `SaveSessionsParameter.java` line 15

**Detail:**
The field `public SavePreStartItem results;` holds pre-start check results. The name `results` is extremely generic and collides conceptually with "results" returned *from* the web service (the project has a `results` sub-package for response types). Callers in `SyncService.java` (line 133) assign to it via `parameterItem.results = sessionDb.getPreStartResultsParameter()`, which partially clarifies intent, but the field name alone is ambiguous. The sibling field `sessions` is similarly named as a noun describing its content, but `sessions` holds a single `SaveSessionItem` (not a collection), adding a second naming inconsistency: the plural name implies a list but the type is a singular item.

**Recommendation:** Rename `results` to `preStartResults` (or `prestart_results` to match the snake_case convention used elsewhere) and rename `sessions` to `session` to match the singular type.

---

### A32-5 — LOW: Plural field name `sessions` holds a singular object

**Affected file:** `SaveSessionsParameter.java` line 14

**Detail:**
`public SaveSessionItem sessions;` declares a field named with a plural noun but typed as a single `SaveSessionItem` (not a `List` or array). Callers confirm the singular assignment in `SyncService.java` lines 126–132:

```java
parameterItem.sessions = new SaveSessionItem();
parameterItem.sessions.prestart_required = sessionResult.prestart_required;
...
```

A reader encountering `SaveSessionsParameter.sessions` would reasonably expect a collection. The mismatch between the plural name and singular type increases cognitive load and risks misuse if a future developer attempts to iterate over it or assign a list.

**Recommendation:** Rename to `session` (singular) to match the actual type.

---

### A32-6 — LOW: All data fields are `public` with no encapsulation

**Affected files:** All three audited files (all fields on lines 14–19 in each file)

**Detail:**
All data fields across the three classes are declared `public`. While this is a common pattern in Android DTO/parameter objects used for direct JSON serialisation, the fields are also read and written directly by UI fragment code (`ServiceEditFragment`) and model-layer code (`SyncService`), creating tight coupling between layers. There are no getters, setters, or any validation. If a field's type ever needs to change (e.g., `serv_duration` from `int` to `long` for large durations), all callers must be updated with no compiler-enforced boundary.

This is consistent with the pattern used throughout the package (other parameter classes share the same approach), so this finding is rated LOW rather than MEDIUM in the context of this codebase. However, it represents a systemic design issue.

**Recommendation:** Consider whether JavaBean-style accessors or Lombok/AutoValue generation could provide a boundary without excessive boilerplate, at minimum for fields written by multiple layers.

---

### A32-7 — INFO: `WebServiceParameterPacket` JSONObject constructor is dead code relative to these parameter classes

**Affected files (context):** `WebServiceParameterPacket.java` line 18–25

**Detail:**
`WebServiceParameterPacket` provides a `WebServiceParameterPacket(JSONObject)` constructor with an empty `if (jsonObject != null)` body. None of the three audited parameter classes expose or use this constructor — they only inherit the no-arg constructor. The JSON-constructor pattern exists in `SaveSessionItem` and `SavePreStartItem` (which are received, not sent), but parameter classes are serialised *outbound*: they are constructed by Java and serialised to JSON by the web API layer, not parsed from JSON. The JSONObject constructor on the parameter side of the hierarchy appears to be vestigial scaffolding that will never be used for these classes.

**Recommendation:** Confirm no callers use `new SaveService*Parameter(jsonObject)`. If confirmed absent (as grep results indicate), consider removing the JSONObject constructor from `WebServiceParameterPacket` or documenting its intended use.

---

## Section 3 — Summary Table

| ID | Severity | File(s) | Issue |
|----|----------|---------|-------|
| A32-1 | MEDIUM | All 3 | Five unused imports per file (JSONException, JSONObject, JSONArray, ArrayList, BigDecimal); results.* wildcard also unused |
| A32-2 | MEDIUM | All 3 | Redundant `implements Serializable` — already declared in root ancestor `WebServicePacket` |
| A32-3 | MEDIUM | SaveServiceDurationParameter, SaveServiceHoursParameter | Asymmetric naming for the distinguishing field: `serv_duration` vs `next_serv` |
| A32-4 | LOW | SaveSessionsParameter | Generic field name `results` ambiguous; collides with result-package terminology |
| A32-5 | LOW | SaveSessionsParameter | Plural field name `sessions` holds a singular `SaveSessionItem` |
| A32-6 | LOW | All 3 | All fields are `public` with no encapsulation boundary between UI and model layers |
| A32-7 | INFO | (context: WebServiceParameterPacket) | JSONObject constructor is dead scaffolding relative to parameter classes |

**Total findings: 7** (0 CRITICAL, 0 HIGH, 3 MEDIUM, 3 LOW, 1 INFO)
