# Pass 4 Code Quality Audit — Agent A33
**Audit run:** 2026-02-26-01
**Agent:** A33
**Files reviewed:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SaveShockEventParameter.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SaveSingleGPSParameter.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/SessionEndParameter.java`

---

## Step 1: Reading Evidence

### File 1 — SaveShockEventParameter.java

**Class:** `SaveShockEventParameter`
- Extends: `WebServiceParameterPacket`
- Implements: `Serializable`
- Package: `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters`

**Fields:**
- Line 11: `public ArrayList<SaveShockEventItem> impactList`

**Methods:**
| Method | Line |
|---|---|
| `SaveShockEventParameter()` (constructor) | 13 |

**Types/Constants/Enums defined:** none

**Imports:**
- Line 3: `SaveShockEventItem`
- Line 4: `WebServiceParameterPacket`
- Line 6: `java.io.Serializable`
- Line 7: `java.util.ArrayList`

---

### File 2 — SaveSingleGPSParameter.java

**Class:** `SaveSingleGPSParameter`
- Extends: `WebServiceParameterPacket`
- Implements: `Serializable`
- Package: `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters`

**Fields:**
- Line 9:  `public int unit_id`
- Line 10: `public Double longitude`
- Line 11: `public Double latitude`
- Line 12: `public String gps_time`

**Methods:**
| Method | Line |
|---|---|
| `SaveSingleGPSParameter()` (constructor, empty body) | 14 |

**Types/Constants/Enums defined:** none

**Imports:**
- Line 3: `java.io.Serializable`
- Line 4: `WebServiceParameterPacket`

---

### File 3 — SessionEndParameter.java

**Class:** `SessionEndParameter`
- Extends: `WebServiceParameterPacket`
- Implements: `Serializable`
- Package: `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters`

**Fields:**
- Line 10: `public int id`
- Line 11: `public String finish_time`
- Line 12: `public boolean prestart_required`

**Methods:**
| Method | Line |
|---|---|
| `SessionEndParameter()` (no-arg constructor) | 14 |
| `SessionEndParameter(SessionResult result)` (copy constructor) | 17 |

**Types/Constants/Enums defined:** none

**Imports:**
- Line 3: `WebServiceParameterPacket`
- Line 4: `SessionResult` (results sub-package)
- Line 6: `java.io.Serializable`

---

## Step 2 & 3: Findings

### A33-1 — HIGH: All public fields expose mutable state with no encapsulation (leaky abstraction)

**Files:** All three files
**Lines:**
- `SaveShockEventParameter.java` line 11
- `SaveSingleGPSParameter.java` lines 9–12
- `SessionEndParameter.java` lines 10–12

All data-transfer fields in all three classes are declared `public` with no accessors or mutability control. While a plain DTO pattern can be intentional, the consequence here is a leaky abstraction: `LocationDb.saveNewLocation()`, `LocationDb.removeData()`, and multiple UI/presenter classes reach directly into `SaveSingleGPSParameter` internal fields (e.g. `saveSingleGPSParameter.unit_id`, `saveSingleGPSParameter.latitude`, etc.) to manipulate and copy state. The parameter classes are used as structural bags that callers write into directly, creating tight coupling between the serialization schema (field names) and every calling site. Any rename of a field (e.g. `unit_id`) requires changing all callers rather than updating a single accessor. The `prestart_required` field on `SessionEndParameter` is never set by the no-arg constructor paths used in the majority of call sites (see below, A33-3), which is a direct consequence of this exposure pattern.

---

### A33-2 — MEDIUM: Inconsistent import style across sibling parameter classes

**Files:** `SaveShockEventParameter.java` vs `SaveSingleGPSParameter.java`

`SaveShockEventParameter.java` (line 3–4) uses specific named imports in a non-standard import order: the project-local imports appear before the `java.*` standard library imports. In `SaveSingleGPSParameter.java` (lines 3–4) the order is reversed: `java.io.Serializable` appears before the project-local import. The Android/Java convention (enforced by most code style tools such as Google Java Style and Android Studio defaults) is: static imports, then `android.*`, then third-party, then `java.*`/`javax.*`. Both files deviate from this order in opposite directions, showing no consistent style is being enforced.

Additionally, `SaveSingleGPSParameter.java` has a blank line 6 (double blank line after imports) while `SaveShockEventParameter.java` has a single blank line — a minor but inconsistent whitespace pattern across the package.

---

### A33-3 — HIGH: `SessionEndParameter(SessionResult)` copy constructor is effectively unused; no-arg path silently omits `prestart_required`

**File:** `SessionEndParameter.java` lines 17–21
**Supporting evidence:** grep of all instantiation sites

The copy constructor `SessionEndParameter(SessionResult result)` (lines 17–21) is only called from `SessionTimeouter.java` (2 call sites). All other six call sites — in `JobsPresenter`, `EquipmentDriverAccessPresenter`, `FleetActivity` (×2), `DashboardFragment`, and `JobsFragment` — use the no-arg constructor and then manually assign only `id` and `finish_time`. None of those six sites ever set `prestart_required`. This means `prestart_required` defaults to `false` on every non-timeout session-end path, which may silently suppress pre-start check requirements for the majority of session end flows. The copy constructor exists precisely to avoid this omission, but its use is inconsistent. This is a correctness risk concealed as a code-quality divergence.

---

### A33-4 — MEDIUM: `SessionEndParameter` imports `SessionResult` from the `results` sub-package, creating a cross-direction dependency

**File:** `SessionEndParameter.java` line 4

`SessionEndParameter` is a request (outbound) parameter object. It imports and directly depends on `SessionResult`, which is a response (inbound) result object from `webserviceclasses.results`. This creates a coupling from the request layer to the response layer within the same web-service class hierarchy. The copy constructor (line 17) taking a `SessionResult` is the source of this coupling. Parameter classes should not depend on result classes; the mapping should happen in a service/presenter layer. This is a leaky abstraction in the package architecture.

---

### A33-5 — MEDIUM: `SaveSingleGPSParameter` uses boxed `Double` instead of primitive `double` for latitude/longitude

**File:** `SaveSingleGPSParameter.java` lines 10–11

`longitude` and `latitude` are declared as `Double` (boxed). The sibling DB model `LocationDb` declares the same fields as `Double` too (for Realm compatibility), but the parameter class has no such constraint. Using the boxed type introduces unnecessary autoboxing overhead on every assignment and read, and — more critically — creates a null-pointer risk: if either field is never assigned before serialization, the JSON serializer (Retrofit/Gson) will serialize them as JSON `null` rather than `0.0`, which may be rejected by the server. The primitive `double` type would fail fast at assignment rather than silently producing `null` in the payload.

---

### A33-6 — LOW: `SaveShockEventParameter` field named `impactList` while the API schema field is `impact_*`

**File:** `SaveShockEventParameter.java` line 11

All other fields across the parameter classes use `snake_case` to match server API field names (e.g. `unit_id`, `gps_time`, `finish_time`, `impact_time`, `impact_value`, `mac_address`). The list field in this class is named `impactList` in `camelCase`. If Gson/Retrofit serializes field names by their Java identifier (which is the default with no `@SerializedName` annotation), the server will receive `impactList` rather than a `snake_case` equivalent. Sibling list classes such as `SaveMultipleGPSParameter.gpsList` use `camelCase` as well, suggesting a `@SerializedName` annotation or custom `GsonBuilder` naming policy is relied upon globally, but this is not visible or enforced within these files, making the convention fragile and undocumented locally.

---

### A33-7 — LOW: Empty constructor bodies could be omitted or are redundant

**Files:**
- `SaveShockEventParameter.java` line 13–15 (constructor is not empty — it initialises `impactList`)
- `SaveSingleGPSParameter.java` lines 14–15 (body is genuinely empty)
- `SessionEndParameter.java` lines 14–15 (body is genuinely empty)

`SaveSingleGPSParameter()` and `SessionEndParameter()` define explicit no-arg constructors with empty bodies. Java generates a default no-arg constructor automatically when no other constructors are present (or when no-arg is the only constructor). For `SaveSingleGPSParameter` this is purely redundant. For `SessionEndParameter` the no-arg constructor is needed alongside the `SessionResult` overload to preserve default-construction, so it must exist — but with an empty body, a comment explaining its necessity would improve readability.

---

### A33-8 — INFO: Inconsistent brace placement style across the three files

**Files:** All three

`SaveShockEventParameter.java` and `SessionEndParameter.java` use Allman (opening brace on next line) style for the class body. `SaveSingleGPSParameter.java` uses K&R (opening brace same line) style for the class body (`public class SaveSingleGPSParameter extends ... {`). Within the same package all files should follow a single brace style. This is a minor style inconsistency consistent with findings observed in the broader codebase.

---

## Summary Table

| ID | Severity | File(s) | Issue |
|---|---|---|---|
| A33-1 | HIGH | All three | All public fields — leaky abstraction; tight coupling to callers |
| A33-2 | MEDIUM | SaveShockEventParameter, SaveSingleGPSParameter | Inconsistent import ordering |
| A33-3 | HIGH | SessionEndParameter | Copy constructor practically unused; `prestart_required` silently omitted in 6 of 8 call sites |
| A33-4 | MEDIUM | SessionEndParameter | Parameter class imports result class — cross-direction dependency |
| A33-5 | MEDIUM | SaveSingleGPSParameter | Boxed `Double` for lat/lon — nullable risk in serialisation |
| A33-6 | LOW | SaveShockEventParameter | `impactList` uses camelCase while all other API fields use snake_case |
| A33-7 | LOW | SaveSingleGPSParameter, SessionEndParameter | Redundant empty no-arg constructors |
| A33-8 | INFO | All three | Inconsistent brace placement style |
