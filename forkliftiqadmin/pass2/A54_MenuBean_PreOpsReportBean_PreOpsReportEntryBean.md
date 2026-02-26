# Pass 2 Test-Coverage Audit
**Audit run:** 2026-02-26-01
**Agent ID:** A54
**Files audited:**
- `src/main/java/com/bean/MenuBean.java`
- `src/main/java/com/bean/PreOpsReportBean.java`
- `src/main/java/com/bean/PreOpsReportEntryBean.java`

---

## 1. Reading-Evidence Blocks

### 1.1 MenuBean

**File:** `src/main/java/com/bean/MenuBean.java`
**Class:** `com.bean.MenuBean`
**Implements:** `java.io.Serializable`

**Fields:**

| Field | Type | Default | Line |
|-------|------|---------|------|
| `id` | `String` | `null` | 6 |
| `name` | `String` | `null` | 7 |
| `description` | `String` | `null` | 8 |
| `icon` | `String` | `null` | 9 |
| `action` | `String` | `null` | 10 |

**Methods:**

| Method | Signature | Lines |
|--------|-----------|-------|
| `getAction()` | `public String getAction()` | 12–14 |
| `setAction(String)` | `public void setAction(String action)` | 15–17 |
| `getId()` | `public String getId()` | 18–20 |
| `setId(String)` | `public void setId(String id)` | 21–23 |
| `getName()` | `public String getName()` | 25–27 |
| `setName(String)` | `public void setName(String name)` | 28–30 |
| `getDescription()` | `public String getDescription()` | 31–33 |
| `setDescription(String)` | `public void setDescription(String description)` | 34–36 |
| `getIcon()` | `public String getIcon()` | 37–39 |
| `setIcon(String)` | `public void setIcon(String icon)` | 40–42 |

**Notes:** No-arg constructor is compiler-generated (no explicit constructor declared). No Lombok annotations; all accessors are hand-written.

---

### 1.2 PreOpsReportBean

**File:** `src/main/java/com/bean/PreOpsReportBean.java`
**Class:** `com.bean.PreOpsReportBean`
**Implements:** `java.io.Serializable`
**Annotations:** `@Data`, `@NoArgsConstructor`, `@AllArgsConstructor`

**Fields:**

| Field | Type | Default | Line |
|-------|------|---------|------|
| `serialVersionUID` | `static final long` | `-1805583864595923807L` | 16 |
| `entries` | `List<PreOpsReportEntryBean>` | `new ArrayList<>()` | 18 |

**Lombok-generated methods (via `@Data`):**

| Method | Notes |
|--------|-------|
| `getEntries()` | Getter for `entries` |
| `setEntries(List<PreOpsReportEntryBean>)` | Setter for `entries` |
| `equals(Object)` | Lombok-generated |
| `hashCode()` | Lombok-generated |
| `toString()` | Lombok-generated |

**Lombok-generated constructors:**

| Constructor | Source annotation |
|-------------|-------------------|
| `PreOpsReportBean()` | `@NoArgsConstructor` |
| `PreOpsReportBean(List<PreOpsReportEntryBean>)` | `@AllArgsConstructor` |

---

### 1.3 PreOpsReportEntryBean

**File:** `src/main/java/com/bean/PreOpsReportEntryBean.java`
**Class:** `com.bean.PreOpsReportEntryBean`
**Implements:** `java.io.Serializable`
**Annotations:** `@Data`, `@NoArgsConstructor`

**Fields:**

| Field | Type | Default | Line |
|-------|------|---------|------|
| `serialVersionUID` | `static final long` | `2880681360556430594L` | 14 |
| `unitName` | `String` | — | 16 |
| `manufacture` | `String` | — | 17 |
| `companyName` | `String` | — | 18 |
| `driverName` | `String` | — | 19 |
| `checkDateTime` | `String` | — | 20 |
| `failures` | `ArrayList<String>` | `new ArrayList<>()` | 21 |
| `duration` | `LocalTime` | — | 22 |
| `comment` | `String` | — | 23 |

**Explicit constructor:**

| Constructor | Annotation | Lines |
|-------------|------------|-------|
| `PreOpsReportEntryBean(String, String, String, String, String, LocalTime, ArrayList<String>, String)` | `@Builder` (private) | 26–42 |

**Lombok-generated methods (via `@Data`):**

| Method |
|--------|
| `getUnitName()` |
| `setUnitName(String)` |
| `getManufacture()` |
| `setManufacture(String)` |
| `getCompanyName()` |
| `setCompanyName(String)` |
| `getDriverName()` |
| `setDriverName(String)` |
| `getCheckDateTime()` |
| `setCheckDateTime(String)` |
| `getFailures()` |
| `setFailures(ArrayList<String>)` |
| `getDuration()` |
| `setDuration(LocalTime)` |
| `getComment()` |
| `setComment(String)` |
| `equals(Object)` |
| `hashCode()` |
| `toString()` |

**Lombok-generated builder (via `@Builder` on private constructor):**

| Artifact | Notes |
|----------|-------|
| `PreOpsReportEntryBean.builder()` | Static factory returning `PreOpsReportEntryBeanBuilder` |
| `PreOpsReportEntryBeanBuilder` inner class | Fluent setters for all 8 fields plus `build()` |

---

## 2. Test-Directory Search Results

**Test directory searched:** `src/test/java/`

**Existing test files found:**
- `com/calibration/UnitCalibrationImpactFilterTest.java`
- `com/calibration/UnitCalibrationTest.java`
- `com/calibration/UnitCalibratorTest.java`
- `com/util/ImpactUtilTest.java`

**Search results for audited classes:**

| Class name searched | Files with matches |
|---------------------|--------------------|
| `MenuBean` | None |
| `PreOpsReportBean` | None |
| `PreOpsReportEntryBean` | None |

**Conclusion:** Zero test coverage exists for all three audited classes.

---

## 3. Coverage Gaps and Findings

### MenuBean

A54-1 | Severity: HIGH | `MenuBean` has no test class. Zero of 10 hand-written methods (`getAction`, `setAction`, `getId`, `setId`, `getName`, `setName`, `getDescription`, `setDescription`, `getIcon`, `setIcon`) are covered by any unit test.

A54-2 | Severity: LOW | `MenuBean` has no `serialVersionUID` field despite implementing `Serializable`. This omits a stable serialization identifier and will trigger compiler/IDE warnings. No test validates serialization round-trip behaviour.

A54-3 | Severity: LOW | `MenuBean` has no `equals`, `hashCode`, or `toString` override. Collections and logging behaviour relying on value equality or string representation are untested and potentially incorrect.

---

### PreOpsReportBean

A54-4 | Severity: HIGH | `PreOpsReportBean` has no test class. No test exercises either the `@NoArgsConstructor` path (verifying `entries` initialises to an empty `ArrayList`) or the `@AllArgsConstructor` path (verifying a supplied list is stored and retrieved correctly).

A54-5 | Severity: MEDIUM | The default-value initialiser `entries = new ArrayList<>()` (line 18) is not tested. A test should assert that a newly constructed `PreOpsReportBean` returns a non-null, empty list from `getEntries()`, confirming Lombok's `@NoArgsConstructor` does not suppress field initialisers.

A54-6 | Severity: LOW | Lombok-generated `equals` and `hashCode` for `PreOpsReportBean` are untested. Two instances sharing the same `entries` list should be equal; no test verifies this contract.

A54-7 | Severity: LOW | Lombok-generated `toString` for `PreOpsReportBean` is untested. No test asserts the string representation includes the entries list content.

---

### PreOpsReportEntryBean

A54-8 | Severity: HIGH | `PreOpsReportEntryBean` has no test class. None of the 8 fields, 16 Lombok-generated accessors, or the `@Builder` construction path are covered by any unit test.

A54-9 | Severity: HIGH | The `@Builder`-annotated private constructor (lines 26–42) is the only explicit constructor. No test exercises the builder to verify that all 8 fields (`unitName`, `manufacture`, `companyName`, `driverName`, `checkDateTime`, `duration`, `failures`, `comment`) are assigned correctly through `PreOpsReportEntryBean.builder().build()`.

A54-10 | Severity: MEDIUM | The `failures` field is initialised to `new ArrayList<>()` at the field level (line 21) but the private `@Builder` constructor does NOT call `this.failures = new ArrayList<>()` as a default — it accepts the caller-supplied value which may be `null`. No test validates that a builder invocation with no `failures()` call produces a non-null failures list. This is a latent `NullPointerException` risk at call sites that invoke `getFailures()` after builder construction without supplying failures.

A54-11 | Severity: MEDIUM | `PreOpsReportEntryBean` uses `LocalTime` for `duration` (line 22). No test validates construction, storage, or retrieval of this field, including boundary values (midnight `LocalTime.MIN`, end-of-day `LocalTime.MAX`) and `null`.

A54-12 | Severity: LOW | Lombok-generated `equals` and `hashCode` for `PreOpsReportEntryBean` are untested. The generated `equals` includes the `ArrayList<String> failures` field; no test confirms two beans with identical failure lists are considered equal.

A54-13 | Severity: LOW | Lombok-generated `toString` for `PreOpsReportEntryBean` is untested. No test asserts the string representation includes all field values, which could mask logging defects.

A54-14 | Severity: INFO | `PreOpsReportEntryBean` mixes Lombok (`@Data`, `@NoArgsConstructor`) with a hand-written private `@Builder` constructor. The private visibility of the builder constructor means it cannot be subclassed or directly instantiated outside the builder — no test documents or asserts this design intent.

A54-15 | Severity: INFO | The field name `manufacture` (line 17) appears to be a misspelling of `manufacturer`. No test exercises or documents this field name, so the misspelling is not caught at the test layer. This may cause confusion at integration points (JSP EL, JSON serialisation keys, database column mapping).

---

## 4. Summary Table

| Finding | Severity | Class | Description |
|---------|----------|-------|-------------|
| A54-1 | HIGH | MenuBean | No test class; 10 hand-written methods completely uncovered |
| A54-2 | LOW | MenuBean | Missing `serialVersionUID`; no serialization round-trip test |
| A54-3 | LOW | MenuBean | No `equals`/`hashCode`/`toString`; value equality untested |
| A54-4 | HIGH | PreOpsReportBean | No test class; constructors and accessor uncovered |
| A54-5 | MEDIUM | PreOpsReportBean | Default `entries` initialisation not verified by any test |
| A54-6 | LOW | PreOpsReportBean | Lombok `equals`/`hashCode` contract untested |
| A54-7 | LOW | PreOpsReportBean | Lombok `toString` output untested |
| A54-8 | HIGH | PreOpsReportEntryBean | No test class; all fields and accessors uncovered |
| A54-9 | HIGH | PreOpsReportEntryBean | Builder construction path completely untested |
| A54-10 | MEDIUM | PreOpsReportEntryBean | Builder with no `failures()` call may yield null list (NPE risk) |
| A54-11 | MEDIUM | PreOpsReportEntryBean | `LocalTime duration` field untested including null/boundary cases |
| A54-12 | LOW | PreOpsReportEntryBean | Lombok `equals`/`hashCode` with `ArrayList` field untested |
| A54-13 | LOW | PreOpsReportEntryBean | Lombok `toString` output untested |
| A54-14 | INFO | PreOpsReportEntryBean | Private builder constructor design intent undocumented by tests |
| A54-15 | INFO | PreOpsReportEntryBean | Field name `manufacture` likely a misspelling of `manufacturer` |

**Total findings: 15**
HIGH: 4 | MEDIUM: 3 | LOW: 5 | INFO: 2
