# Audit Report — Pass 4 (Code Quality)
**Agent:** A29
**Audit Run:** 2026-02-26-01
**Date:** 2026-02-27
**Files Assigned:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/AddEquipmentParameter.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/GetTokenParameter.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/ImpactParameter.java`

---

## Step 1: Reading Evidence

### File 1: AddEquipmentParameter.java

**Full path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/AddEquipmentParameter.java`

**Package:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters`

**Class:** `AddEquipmentParameter` extends `WebServiceParameterPacket` implements `Serializable`

**Imports (lines 3–10):**
| Line | Import |
|------|--------|
| 3 | `org.json.JSONException` |
| 4 | `org.json.JSONObject` |
| 5 | `java.io.Serializable` |
| 6 | `org.json.JSONArray` |
| 7 | `java.util.ArrayList` |
| 8 | `java.math.BigDecimal` |
| 9 | `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.*` |
| 10 | `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.*` |

**Fields (all `public`, lines 14–20):**
| Line | Type | Name |
|------|------|------|
| 14 | `String` | `name` |
| 15 | `int` | `manu_id` |
| 16 | `int` | `type_id` |
| 17 | `int` | `fuel_type_id` |
| 18 | `String` | `serial_no` |
| 19 | `String` | `mac_address` |
| 20 | `int` | `comp_id` |

**Methods:**
| Lines | Visibility | Signature |
|-------|------------|-----------|
| 22–23 | `public` | `AddEquipmentParameter()` — no-arg constructor, empty body |

**Types / Constants / Enums / Interfaces defined:** None.

---

### File 2: GetTokenParameter.java

**Full path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/GetTokenParameter.java`

**Package:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters`

**Class:** `GetTokenParameter` extends `WebServiceParameterPacket` implements `Serializable`

**Imports (lines 3–10):** Identical block to `AddEquipmentParameter.java` — see table above.

**Fields (all `public`, lines 14–18):**
| Line | Type | Name |
|------|------|------|
| 14 | `String` | `grant_type` |
| 15 | `String` | `client_id` |
| 16 | `String` | `client_secret` |
| 17 | `String` | `username` |
| 18 | `String` | `password` |

**Methods:**
| Lines | Visibility | Signature |
|-------|------------|-----------|
| 20–21 | `public` | `GetTokenParameter()` — no-arg constructor, empty body |

**Types / Constants / Enums / Interfaces defined:** None.

---

### File 3: ImpactParameter.java

**Full path:** `app/src/main/java/au/com/collectiveintelligence/fleetiq360/WebService/webserviceclasses/parameters/ImpactParameter.java`

**Package:** `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.parameters`

**Class:** `ImpactParameter` extends `WebServiceParameterPacket` implements `Serializable`

**Imports (lines 3–10):** Identical block to `AddEquipmentParameter.java` — see table above.

**Fields (all `public`, lines 14–24):**
| Line | Type | Name |
|------|------|------|
| 14 | `String` | `injury_type` |
| 15 | `String` | `description` |
| 16 | `String` | `witness` |
| 17 | `String` | `report_time` |
| 18 | `String` | `event_time` |
| 19 | `boolean` | `injury` |
| 20 | `boolean` | `near_miss` |
| 21 | `boolean` | `incident` |
| 22 | `String` | `location` |
| 23 | `int` | `driver_id` |
| 24 | `int` | `unit_id` |

**Methods:**
| Lines | Visibility | Signature |
|-------|------------|-----------|
| 26–27 | `public` | `ImpactParameter()` — no-arg constructor, empty body |

**Types / Constants / Enums / Interfaces defined:** None.

---

### Supporting context gathered

**`WebServiceParameterPacket.java`** (parent class, lines 1–26):
- Extends `WebServicePacket implements Serializable`
- Has a no-arg constructor (line 15–16) and a `WebServiceParameterPacket(JSONObject)` constructor (lines 18–25) whose body contains only an empty `if (jsonObject != null) {}` block — the JSON constructor does nothing beyond calling `super(jsonObject)`.
- Carries the same dead-import block (lines 3–10) as the three assigned files.

**Confirmed call sites:**
- `AddEquipmentParameter` is instantiated at `AddEquipmentFragment.java:425` and passed to `WebApi.addEquipment()` (line 59 of `WebApi.java`).
- `ImpactParameter` is instantiated at `IncidentActivity.java:25` (fields set directly on lines 26–29) and passed to `WebApi.saveImpact()` (line 337 of `WebApi.java`).
- `GetTokenParameter` has no instantiation site in the application source. The OAuth2 token request is assembled differently inside `WebData`.

---

## Step 2 & 3: Findings

---

### A29-1 — HIGH — All three files: seven unused imports copied verbatim from a code-generation template

**Files:**
- `AddEquipmentParameter.java` lines 3–10
- `GetTokenParameter.java` lines 3–10
- `ImpactParameter.java` lines 3–10

**Detail:**
Every assigned file — and their parent class `WebServiceParameterPacket.java` — shares an identical eight-line import block:

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

Of these, only `java.io.Serializable` is actually used (by the `implements Serializable` declaration). The remaining seven imports — `JSONException`, `JSONObject`, `JSONArray`, `ArrayList`, `BigDecimal`, the wildcard `webserviceclasses.*`, and the wildcard `results.*` — are completely unreferenced in the class bodies of all three files.

The mechanical duplication across every parameter class and their parent class confirms this is a code-generation template artefact, not an intentional design choice. Android Lint flags unused imports as warnings (`UnusedImport`). The wildcard imports additionally suppress IDE and tool visibility into the actual dependency surface.

**Severity rationale:** The unused wildcard `results.*` import in all three parameter classes means the compiler resolves `results.*` in every parameter file, pulling in all result types into scope unnecessarily. Any name collision introduced in `results.*` (e.g., a class named `String` or a name matching a field) would produce a silent compile-time scope resolution error. This is beyond a cosmetic issue.

---

### A29-2 — HIGH — GetTokenParameter: dead class with OAuth2 credential fields — unreachable but present in compiled APK

**File:** `GetTokenParameter.java` lines 12–22

**Detail:**
A codebase-wide search found no instantiation of `GetTokenParameter` in any application source file. The OAuth2 token request is assembled in `WebData` via a separate mechanism (`getTokenFormData()`), not through this class. `GetTokenParameter` is therefore dead code.

Despite being unused at runtime, the class compiles into the APK. It declares five `public String` fields — including `client_secret` and `password` — which mirror the same credential names used in the live token request. The class implements `Serializable` without marking any field `transient`, meaning any future developer who wires up this class (e.g., during a refactor) would unknowingly introduce a path where OAuth2 credentials are serialised to disk by Android's instance-state save mechanism or passed across process boundaries in an `Intent`.

The combination of dead-but-compiled credential DTO, no `transient` guards, and no documentation warning against use makes this a latent security trap.

**Evidence of deadness:** The grep over the entire `app/src/main/java` tree returned only the class's own definition lines for `GetTokenParameter`.

---

### A29-3 — MEDIUM — All three files: all public fields use snake_case, violating Java naming conventions (inconsistency within the package)

**Files:**
- `AddEquipmentParameter.java` lines 14–20: `manu_id`, `type_id`, `fuel_type_id`, `serial_no`, `mac_address`, `comp_id`
- `GetTokenParameter.java` lines 14–18: `grant_type`, `client_id`, `client_secret`
- `ImpactParameter.java` lines 14–24: `injury_type`, `near_miss`, `report_time`, `event_time`, `driver_id`, `unit_id`

**Detail:**
Java field naming conventions (JLS §6.1, Android code style) require `lowerCamelCase` for instance fields. All three classes use `snake_case` throughout. This is consistent within these three files but inconsistent with the rest of the codebase (e.g., `IncidentActivity` fields `impactParameter`, `impactResult`, `signaturePath`, `mCurrentPhotoPath` all use lowerCamelCase).

The rationale is almost certainly Gson field serialisation matching a REST API that uses snake_case JSON keys. However, this design decision is nowhere documented, and no `@SerializedName` annotation is used to make the intent explicit. The absence of `@SerializedName` means that:

1. Any field rename during refactoring silently breaks the API contract.
2. ProGuard/R8 minification will rename the fields unless exclusion rules exist, breaking serialisation in release builds.
3. Code readers cannot distinguish "this name is intentionally snake_case for Gson" from a style error.

**Note:** This finding is distinct from security; it is a maintainability and correctness risk.

---

### A29-4 — MEDIUM — ImpactParameter: `report_time` and `event_time` typed as `String` instead of a structured temporal type

**File:** `ImpactParameter.java` lines 17–18

**Detail:**
`report_time` (line 17) and `event_time` (line 18) represent timestamps but are declared as `public String`. There is no format constraint, no validation, and no documentation of the expected format (ISO-8601, Unix epoch, etc.). The caller (`IncidentActivity`) sets these fields directly via plain string assignment with no format enforcement.

Using raw `String` for temporal data in a parameter object that maps directly to a web service request means:
- The server may silently reject or misparse mal-formatted timestamp strings.
- There is no compile-time safety preventing an accidentally swapped `report_time`/`event_time` assignment (both are `String`).
- Gson serialises these fields as opaque string values with no structural validation.

The same issue applies to `AddEquipmentParameter.serial_no` and `mac_address` (untyped strings with domain constraints enforced elsewhere), but the temporal fields carry higher risk because server-side temporal parsing errors are typically silent or produce wrong data rather than a rejection.

---

### A29-5 — MEDIUM — ImpactParameter: `injury` field initialised twice in caller; no default values in DTO

**File:** `ImpactParameter.java` line 19; `IncidentActivity.java` lines 27 and 30

**Detail:**
In `IncidentActivity.onCreate()`:
```java
impactParameter.injury = false;   // line 27
impactParameter.injury = false;   // line 30 — duplicate assignment
```
`injury` is assigned `false` twice. The second assignment on line 30 is functionally dead. While the DTO itself is not the source of the bug, the DTO's design (public fields, no constructor parameters, no default-value documentation) invites this kind of subtle caller error. A constructor that accepts required fields, or at minimum Javadoc on each field stating the default assumption, would prevent redundant or contradictory initialisation.

**Severity rationale:** Currently harmless (both assignments set the same value), but this pattern masks the risk that a future change sets a different value on line 27 and a developer fails to notice the second assignment on line 30 resets it.

---

### A29-6 — LOW — All three files: `Serializable` without `serialVersionUID`

**Files:**
- `AddEquipmentParameter.java` line 12
- `GetTokenParameter.java` line 12
- `ImpactParameter.java` line 12

**Detail:**
All three classes implement `java.io.Serializable` but none declares a `private static final long serialVersionUID`. Java's serialisation mechanism computes a default `serialVersionUID` from the class's structure (fields, methods, superclass chain). Any change to a field — adding, removing, or changing a type — will alter the computed UID, causing `InvalidClassException` if a serialised instance from an older version of the app is deserialised by a newer version (e.g., during Android's Activity restoration from saved state after an app update).

Android Lint flags this as `serial` warning. The parent class `WebServiceParameterPacket` also lacks `serialVersionUID`, compounding the risk across the entire DTO hierarchy.

---

### A29-7 — LOW — AddEquipmentParameter: `mac_address` is a plain public `String` with no encapsulation

**File:** `AddEquipmentParameter.java` line 19

**Detail:**
`mac_address` is a device hardware identifier. It is declared as a bare `public String` with no validation, no `@NonNull`/`@Nullable` annotation, and no length or format constraint. The validation logic (`WebData.isValidMacAddress()`) is enforced in the caller, not in the DTO. Because the field is public, any caller can bypass validation by writing directly to the field:
```java
parameter.mac_address = "invalid";  // compiles and serialises without error
```
This is a leaky abstraction: the DTO's public contract implies acceptance of any string, while the actual contract (17-character colon-separated MAC format) is enforced only by convention in one caller.

---

### A29-8 — LOW — All three files: empty constructors are unnecessary

**Files:**
- `AddEquipmentParameter.java` lines 22–23
- `GetTokenParameter.java` lines 20–21
- `ImpactParameter.java` lines 26–27

**Detail:**
Each class declares an explicit no-arg constructor with an empty body:
```java
public ClassName() {
}
```
Because no other constructor is defined, Java supplies an identical no-arg constructor automatically. The explicit empty constructor adds no behaviour and no documentation. It contributes to the visual bulk of the file while suggesting (incorrectly) that some initialisation might be needed or that constructors with arguments may exist elsewhere.

**Note:** This is a style issue only. The constructors are not harmful.

---

### A29-9 — INFO — GetTokenParameter: `Serializable` with credential fields not marked `transient`

**File:** `GetTokenParameter.java` lines 16 (`client_secret`), 18 (`password`)

**Detail:**
This finding is conditional on A29-2 (the class being dead). If `GetTokenParameter` were ever wired into active use, `client_secret` and `password` — both declared `public String` without `transient` — would be included in any `ObjectOutputStream` serialisation. Android's OS-managed state saving (e.g., `onSaveInstanceState` with `putSerializable`) would write credentials to disk. This is noted as INFO because the class is currently unreachable; the risk is latent, not active.

---

## Step 4: Summary Table

| ID | Severity | File(s) | Description |
|----|----------|---------|-------------|
| A29-1 | HIGH | All three | Seven unused template imports in every file; wildcards suppress dependency visibility and generate Lint warnings |
| A29-2 | HIGH | GetTokenParameter.java | Class is dead (no instantiation site); compiled into APK with latent credential serialisation risk |
| A29-3 | MEDIUM | All three | `snake_case` field names violate Java conventions; no `@SerializedName`; ProGuard/R8 will break Gson serialisation in release builds |
| A29-4 | MEDIUM | ImpactParameter.java | `report_time`/`event_time` typed as `String` with no format contract; swappable without compile-time error |
| A29-5 | MEDIUM | ImpactParameter.java (caller: IncidentActivity.java) | `injury` field assigned `false` twice in caller; DTO design invites redundant/conflicting initialisation |
| A29-6 | LOW | All three | `Serializable` without `serialVersionUID`; field changes will break deserialisation of persisted instances |
| A29-7 | LOW | AddEquipmentParameter.java | `mac_address` public with no encapsulation; validation enforced only by convention in one caller |
| A29-8 | LOW | All three | Explicit empty no-arg constructors are redundant; Java provides identical default constructors automatically |
| A29-9 | INFO | GetTokenParameter.java | Credential fields `client_secret`, `password` not `transient`; latent risk if class is ever activated |
