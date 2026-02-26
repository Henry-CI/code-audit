# Pass 3 Documentation Audit — A81
**Audit run:** 2026-02-26-01
**Agent:** A81
**Files:** dao/TrainingDAO.java, dao/UnitDAO.java

---

## 1. Reading Evidence

### 1.1 TrainingDAO.java

**Class:** `TrainingDAO` — line 20

**Fields:**
| Field | Type | Line |
|---|---|---|
| `log` | `static Logger` | 21 |

**Methods (all public):**
| Method | Return type | Line |
|---|---|---|
| `getTrainingByDriver(Long driverId, String dateFormat)` | `List<DriverTrainingBean>` | 23 |
| `addTraining(DriverTrainingBean trainingBean, String dateFormat)` | `void` | 55 |
| `deleteTraining(Long trainingId)` | `void` | 70 |
| `sendTrainingExpiryDailyEmail()` | `void` | 76 |
| `sendTrainingExpiryWeeklyEmail()` | `void` | 119 |

No private or package-private methods.

---

### 1.2 UnitDAO.java

**Class:** `UnitDAO` — line 22

**Fields:**
| Field | Type | Line |
|---|---|---|
| `log` | `static Logger` | 23 |
| `theInstance` | `static UnitDAO` | 24 |
| `INSERT_UNIT_ASSIGNMENT` | `static final String` | 48 |
| `DELETE_UNIT_ASSIGNMENT` | `static final String` | 78 |
| `QUERY_ASSIGN_DATE_OVERLAP_CHECK` | `static final String` | 91 |
| `QUERY_COUNT_UNIT_BY_NAME` | `static final String` | 116 |
| `QUERY_COUNT_UNIT_BY_SERIAL_NO` | `static final String` | 146 |
| `QUERY_COUNT_UNIT_BY_MAC_ADDRESS` | `static final String` | 179 |
| `INSERT_UNIT_INFO` | `static final String` | 438 |
| `UPDATE_UNIT` | `static final String` | 467 |
| `UPDATE_UNIT_ACCESS` | `static final String` | 513 |
| `QUERY_IMPACT_BY_UNIT` | `static final String` | 817 |

**Methods:**
| Method | Visibility | Return type | Line |
|---|---|---|---|
| `getInstance()` | public static | `UnitDAO` | 26 |
| `UnitDAO()` (constructor) | private | — | 37 |
| `getAssignments(String sessCompId, String equipId, String dateFormat)` | public static | `List<UnitAssignmentBean>` | 40 |
| `addAssignment(String subCompanyId, String unitId, String startDate, String endDate, String dateFormat)` | public static | `void` | 52 |
| `deleteAssignment(String id)` | public static | `void` | 80 |
| `isAssignmentOverlapping(String unitId, Date startDate, Date endDate)` | public static | `boolean` | 98 |
| `checkUnitByNm(String compId, String name, String id, boolean activeStatus)` | public | `boolean` | 119 |
| `checkUnitBySerial(String serialNo, String id, boolean activeStatus, String compId)` | public | `boolean` | 149 |
| `checkUnitByMacAddr(String macAddr, String id)` | public | `boolean` | 182 |
| `getUnitBySerial(String serial_no, Boolean activeStatus)` | public | `ArrayList<UnitBean>` | 199 |
| `getAllUnitsByCompanyId(int compId)` | public static | `List<UnitBean>` | 242 |
| `getUnitMaxId()` | public | `int` | 252 |
| `getUnitById(String id)` | public static | `List<UnitBean>` | 288 |
| `getUnitNameByComp(String compId, Boolean activeStatus)` | public | `ArrayList<UnitBean>` | 293 |
| `delUnitById(String id)` | public | `void` | 340 |
| `getAllUnitType()` | public static | `ArrayList<UnitTypeBean>` | 364 |
| `getAllUnitFuelType()` | public | `ArrayList<UnitFuelTypeBean>` | 401 |
| `saveUnitInfo(UnitBean unitbean)` | public | `boolean` | 442 |
| `updateUnitInfo(UnitBean unitbean)` | private | `boolean` | 472 |
| `saveUnitAccessInfo(UnitBean unitbean)` | public static | `void` | 517 |
| `getTotalUnitByID(String id, Boolean activeStatus)` | public static | `String` | 530 |
| `getAllUnitAttachment()` | public | `ArrayList<AttachmentBean>` | 573 |
| `getType(String manu_id)` | public | `ArrayList<XmlBean>` | 610 |
| `getPower(String manu_id, String type_id)` | public | `ArrayList<XmlBean>` | 653 |
| `saveService(ServiceBean bean)` | public | `void` | 699 |
| `getServiceByUnitId(String unitId)` | public | `ArrayList<ServiceBean>` | 761 |
| `getImpactByUnitId(Long unitId)` | public | `List<ImpactBean>` | 822 |
| `getChecklistSettings(String unitId)` | public | `ArrayList<ChecklistBean>` | 833 |
| `resetCalibration(int equipId)` | public | `void` | 875 |
| `updateChecklistSettings(ChecklistBean bean)` | public | `void` | 879 |
| `getSessionHoursCalilbration(String reset_cal_date, String equipId)` | public | `double` | 909 |
| `getAllUnitSearch(String compId, Boolean activeStatus, String searchUnit)` | public | `List<UnitBean>` | 958 |

---

## 2. Findings

### TrainingDAO.java

#### A81-1 — LOW — No class-level Javadoc (TrainingDAO)
**Location:** `TrainingDAO.java`, line 20
**Detail:** The class `TrainingDAO` has no class-level `/** ... */` Javadoc comment. There is no description of the class purpose, its role in the data-access layer, or the underlying database table (`driver_training`) it manages.

#### A81-2 — MEDIUM — No Javadoc on `getTrainingByDriver`
**Location:** `TrainingDAO.java`, line 23
**Signature:** `public List<DriverTrainingBean> getTrainingByDriver(Long driverId, String dateFormat) throws SQLException`
**Detail:** Non-trivial public method with no Javadoc. The method executes a multi-table JOIN across `driver_training`, `manufacture`, `type`, and `fuel_type`, formats dates using `dateFormat`, and returns a mapped list of beans. The query logic, parameter semantics, and date-format contract are undocumented.

#### A81-3 — MEDIUM — No Javadoc on `addTraining`
**Location:** `TrainingDAO.java`, line 55
**Signature:** `public void addTraining(DriverTrainingBean trainingBean, String dateFormat) throws SQLException`
**Detail:** Non-trivial public method with no Javadoc. Inserts a new `driver_training` row and parses date strings using the supplied `dateFormat`. The date-format dependency and required non-null fields on `trainingBean` are undocumented.

#### A81-4 — MEDIUM — No Javadoc on `deleteTraining`
**Location:** `TrainingDAO.java`, line 70
**Signature:** `public void deleteTraining(Long trainingId) throws SQLException`
**Detail:** Public method with no Javadoc. Although the body is simple, the deletion is permanent (hard delete from `driver_training`) and the behaviour on a non-existent `trainingId` (silent no-op) is worth documenting. Classified MEDIUM because it is a destructive operation.

#### A81-5 — MEDIUM — No Javadoc on `sendTrainingExpiryDailyEmail`
**Location:** `TrainingDAO.java`, line 76
**Signature:** `public void sendTrainingExpiryDailyEmail() throws SQLException`
**Detail:** Non-trivial public method with no Javadoc. The method orchestrates multiple DAO calls, applies locale-dependent terminology ("training" vs "licence" based on the company timezone's geographic prefix), sends email alerts, and silently swallows `AddressException` and `MessagingException` via `printStackTrace()`. All of this behaviour is undocumented.

#### A81-6 — MEDIUM — No Javadoc on `sendTrainingExpiryWeeklyEmail`
**Location:** `TrainingDAO.java`, line 119
**Signature:** `public void sendTrainingExpiryWeeklyEmail() throws SQLException`
**Detail:** Non-trivial public method with no Javadoc. Behaviour is similar to `sendTrainingExpiryDailyEmail` but covers drivers with training expired or expiring within 30 days. The 30-day window, locale-sensitive label selection, null-expiry handling, and silent exception suppression are all undocumented.

---

### UnitDAO.java

#### A81-7 — LOW — No class-level Javadoc (UnitDAO)
**Location:** `UnitDAO.java`, line 22
**Detail:** The class `UnitDAO` has no class-level `/** ... */` Javadoc comment. There is no description of the singleton pattern employed, the database entities it manages (`unit`, `unit_company`, `unit_service`, etc.), or thread-safety considerations.

#### A81-8 — MEDIUM — No Javadoc on `getInstance`
**Location:** `UnitDAO.java`, line 26
**Signature:** `public static UnitDAO getInstance()`
**Detail:** Non-trivial public method with no Javadoc. Implements a double-checked locking singleton. The thread-safety guarantee and the fact that the instance is lazily initialised are undocumented.

#### A81-9 — MEDIUM — No Javadoc on `getAssignments`
**Location:** `UnitDAO.java`, line 40
**Signature:** `public static List<UnitAssignmentBean> getAssignments(String sessCompId, String equipId, String dateFormat) throws SQLException`
**Detail:** Non-trivial public method with no Javadoc. Delegates to `AssignmentByCompanyAndUnitIdQuery`. The string-to-long conversion assumption on both ID parameters, the date-format contract, and the query semantics are undocumented.

#### A81-10 — MEDIUM — No Javadoc on `addAssignment`
**Location:** `UnitDAO.java`, line 52
**Signature:** `public static void addAssignment(String subCompanyId, String unitId, String startDate, String endDate, String dateFormat) throws SQLException`
**Detail:** Non-trivial public method with no Javadoc. Inserts into `unit_company`. Null/empty handling for `startDate` and `endDate` (stored as SQL NULL) is undocumented. Callers cannot know the accepted date-string format without reading the implementation.

#### A81-11 — MEDIUM — No Javadoc on `deleteAssignment`
**Location:** `UnitDAO.java`, line 80
**Signature:** `public static void deleteAssignment(String id) throws SQLException`
**Detail:** Public destructive method (hard delete from `unit_company`) with no Javadoc. Behaviour on a non-existent `id` is undocumented.

#### A81-12 — MEDIUM — No Javadoc on `isAssignmentOverlapping`
**Location:** `UnitDAO.java`, line 98
**Signature:** `public static boolean isAssignmentOverlapping(String unitId, Date startDate, Date endDate) throws SQLException`
**Detail:** Non-trivial public method with no Javadoc. The SQL query uses a partial overlap check that also treats a NULL `end_date` as an open-ended assignment. The `startDate` parameter is asserted non-null via `Objects.requireNonNull` (throwing NPE, not SQLException) but this is undocumented. The interpretation of `endDate == null` (meaning no end date on the candidate range) is undocumented.

#### A81-13 — MEDIUM — No Javadoc on `checkUnitByNm`
**Location:** `UnitDAO.java`, line 119
**Signature:** `public boolean checkUnitByNm(String compId, String name, String id, boolean activeStatus) throws Exception`
**Detail:** Non-trivial public method with no Javadoc. The method builds a dynamic query; the semantics of `id` (when non-null, excludes the given unit from the duplicate check — i.e., for edit scenarios) and `activeStatus` (restricts search to active units only) are undocumented.

#### A81-14 — MEDIUM — No Javadoc on `checkUnitBySerial`
**Location:** `UnitDAO.java`, line 149
**Signature:** `public boolean checkUnitBySerial(String serialNo, String id, boolean activeStatus, String compId) throws Exception`
**Detail:** Non-trivial public method with no Javadoc. Dynamic query building with four optional filter conditions; same edit-exclusion semantics for `id` as `checkUnitByNm`, plus optional company scope via `compId`. All undocumented.

#### A81-15 — MEDIUM — No Javadoc on `checkUnitByMacAddr`
**Location:** `UnitDAO.java`, line 182
**Signature:** `public boolean checkUnitByMacAddr(String macAddr, String id) throws Exception`
**Detail:** Non-trivial public method with no Javadoc. Query always filters `active = true`; the edit-exclusion role of `id` is undocumented.

#### A81-16 — MEDIUM — No Javadoc on `getUnitBySerial`
**Location:** `UnitDAO.java`, line 199
**Signature:** `public ArrayList<UnitBean> getUnitBySerial(String serial_no, Boolean activeStatus) throws Exception`
**Detail:** Non-trivial public method with no Javadoc. Uses string concatenation to build the SQL query (SQL injection risk at the data-access layer), returns only `id` and `comp_id` fields in the bean (not a full unit), and silently returns an empty list when `serial_no` is blank. These non-obvious behaviours are entirely undocumented.

#### A81-17 — MEDIUM — Inaccurate log statement in `getUnitBySerial`
**Location:** `UnitDAO.java`, line 203
**Detail:** The log message reads `"Inside LoginDAO Method : getUnitBySerial"`. The containing class is `UnitDAO`, not `LoginDAO`. This copy-paste error will mislead anyone reading log output trying to trace this method's execution. The same inaccuracy recurs in several methods listed below.

**Inaccurate `LoginDAO` log strings across UnitDAO (same root cause, grouped under this finding):**
- Line 203: `getUnitBySerial` logs `"Inside LoginDAO Method : getUnitBySerial"`
- Line 256: `getUnitMaxId` logs `"Inside LoginDAO Method : getAllUnit"`
- Line 289: `getUnitById` logs `"Inside LoginDAO Method : getUnitById"`
- Line 297: `getUnitNameByComp` logs `"Inside LoginDAO Method : getUnitNameByComp"`
- Line 343: `delUnitById` logs `"Inside LoginDAO Method : delUnitById"`
- Line 368: `getAllUnitType` logs `"Inside LoginDAO Method : getAllUnitType"`
- Line 405: `getAllUnitFuelType` logs `"Inside LoginDAO Method : getAllUnitFuelType"`
- Line 443: `saveUnitInfo` logs `"Inside LoginDAO Method : saveUnitInfo"`
- Line 478: `updateUnitInfo` logs `"Inside LoginDAO Method : updateUnitInfo"`
- Line 534: `getTotalUnitByID` logs `"Inside LoginDAO Method : getTotalUnitByID"`
- Line 577: `getAllUnitAttachment` logs `"Inside LoginDAO Method : getAllUnitAttachment"`
- Line 614: `getType` logs `"Inside LoginDAO Method : getAllUnitAttachment"` (wrong method name too)
- Line 657: `getPower` logs `"Inside LoginDAO Method : getAllUnitAttachment"` (wrong method name too)

#### A81-18 — MEDIUM — Inaccurate log statement in `getType` and `getPower`
**Location:** `UnitDAO.java`, lines 614 and 657
**Detail:** Both `getType` and `getPower` log `"Inside LoginDAO Method : getAllUnitAttachment"`. The wrong class name and the wrong method name are both used. This is more severely misleading than the other `LoginDAO` errors because the method name is also wrong, making it nearly impossible to correlate log output with source code without reading both files. Classified MEDIUM (inaccurate comment) rather than HIGH because these are informational log messages rather than logic guards, but they are nevertheless harmful to operational diagnostics.

#### A81-19 — MEDIUM — Inaccurate log statement in `getUnitMaxId`
**Location:** `UnitDAO.java`, line 256
**Detail:** `getUnitMaxId` logs `"Inside LoginDAO Method : getAllUnit"`. The method name in the log string is `getAllUnit`, which does not match the actual method `getUnitMaxId`. The class name is also wrong (`LoginDAO`). Two simultaneous inaccuracies.

#### A81-20 — MEDIUM — Inaccurate log statement in `getSessionHoursCalilbration`
**Location:** `UnitDAO.java`, line 910
**Detail:** `getSessionHoursCalilbration` logs `"Inside UnitDAO Method : getImpactByUnitId"`. The class name is correct (`UnitDAO`) but the method name is wrong — it copies the log string from `getImpactByUnitId`. A caller tracing calibration session-hours behaviour via logs will be misdirected to the impact method.

#### A81-21 — MEDIUM — No Javadoc on `getAllUnitsByCompanyId`
**Location:** `UnitDAO.java`, line 242
**Signature:** `public static List<UnitBean> getAllUnitsByCompanyId(int compId) throws SQLException`
**Detail:** Non-trivial public method with no Javadoc. Always returns active units only (`.activeUnitsOnly()`) ordered by name ascending — a constraint not evident from the method signature.

#### A81-22 — MEDIUM — No Javadoc on `getUnitMaxId`
**Location:** `UnitDAO.java`, line 252
**Signature:** `public int getUnitMaxId() throws SQLException`
**Detail:** Non-trivial public method with no Javadoc. Returns `max(id) + 1`, i.e., a candidate next ID, rather than the actual maximum ID. The semantics (an optimistic next-ID hint, not the true maximum) are undocumented and the method name implies `max(id)` not `max(id)+1`.

#### A81-23 — MEDIUM — No Javadoc on `getUnitById`
**Location:** `UnitDAO.java`, line 288
**Signature:** `public static List<UnitBean> getUnitById(String id) throws SQLException`
**Detail:** Public method with no Javadoc. The return type is a `List` for a single ID lookup; callers need to understand whether this can ever return more than one result.

#### A81-24 — MEDIUM — No Javadoc on `getUnitNameByComp`
**Location:** `UnitDAO.java`, line 293
**Signature:** `public ArrayList<UnitBean> getUnitNameByComp(String compId, Boolean activeStatus) throws Exception`
**Detail:** Non-trivial public method with no Javadoc. Behaviour expands to include sub-company units when the company has `ROLE_DEALER`, which is a significant undocumented side-effect. Returned beans contain only `id` and `name`.

#### A81-25 — MEDIUM — No Javadoc on `delUnitById`
**Location:** `UnitDAO.java`, line 340
**Signature:** `public void delUnitById(String id) throws Exception`
**Detail:** Non-trivial public method with no Javadoc. Despite the name suggesting deletion, this is a soft delete: it sets `active = false`. The difference between a soft and hard delete is critical operational information that is completely undocumented.

#### A81-26 — MEDIUM — No Javadoc on `getAllUnitType`
**Location:** `UnitDAO.java`, line 364
**Signature:** `public static ArrayList<UnitTypeBean> getAllUnitType() throws Exception`
**Detail:** Public method with no Javadoc. Queries the `type` table and returns all records ordered by name. Straightforward, but public API with no documentation.

#### A81-27 — MEDIUM — No Javadoc on `getAllUnitFuelType`
**Location:** `UnitDAO.java`, line 401
**Signature:** `public ArrayList<UnitFuelTypeBean> getAllUnitFuelType() throws Exception`
**Detail:** Public method with no Javadoc. Queries the `fuel_type` table ordered by name.

#### A81-28 — MEDIUM — No Javadoc on `saveUnitInfo`
**Location:** `UnitDAO.java`, line 442
**Signature:** `public boolean saveUnitInfo(UnitBean unitbean) throws Exception`
**Detail:** Non-trivial public method with no Javadoc. Acts as a combined insert/update: if `unitbean.getId()` is null it inserts; otherwise it delegates to `updateUnitInfo`. The `boolean` return value (true = success, false = update matched zero rows) is undocumented. The insert path always returns true when `rowUpdate > 0`.

#### A81-29 — MEDIUM — No Javadoc on `saveUnitAccessInfo`
**Location:** `UnitDAO.java`, line 517
**Signature:** `public static void saveUnitAccessInfo(UnitBean unitbean) throws Exception`
**Detail:** Non-trivial public method with no Javadoc. Updates access-control columns (`accessible`, `access_type`, `access_id`, `keypad_reader`, `facility_code`) for a unit. The subset of fields updated (not the whole unit) is undocumented.

#### A81-30 — MEDIUM — No Javadoc on `getTotalUnitByID`
**Location:** `UnitDAO.java`, line 530
**Signature:** `public static String getTotalUnitByID(String id, Boolean activeStatus) throws Exception`
**Detail:** Non-trivial public method with no Javadoc. The parameter `id` is a company ID (not a unit ID as the method name could suggest). For dealer-role companies the count spans all sub-companies. The result is returned as a `String` rather than a numeric type, which is non-obvious.

#### A81-31 — MEDIUM — No Javadoc on `getAllUnitAttachment`
**Location:** `UnitDAO.java`, line 573
**Signature:** `public ArrayList<AttachmentBean> getAllUnitAttachment() throws Exception`
**Detail:** Public method with no Javadoc. Returns all attachment types from the `attachment` lookup table. No filtering by unit or company.

#### A81-32 — MEDIUM — No Javadoc on `getType`
**Location:** `UnitDAO.java`, line 610
**Signature:** `public ArrayList<XmlBean> getType(String manu_id) throws Exception`
**Detail:** Non-trivial public method with no Javadoc. Queries `manu_type_fuel_rel` filtered by manufacturer; empty string is coerced to `"0"` to match all manufacturers. The coercion and the join semantics are undocumented.

#### A81-33 — MEDIUM — No Javadoc on `getPower`
**Location:** `UnitDAO.java`, line 653
**Signature:** `public ArrayList<XmlBean> getPower(String manu_id, String type_id) throws Exception`
**Detail:** Non-trivial public method with no Javadoc. Returns fuel types for a given manufacturer optionally filtered by type. An empty `type_id` string means "all types". The result bean type (`XmlBean`) and its fields (`id`, `name`) are not documented.

#### A81-34 — MEDIUM — No Javadoc on `saveService`
**Location:** `UnitDAO.java`, line 699
**Signature:** `public void saveService(ServiceBean bean) throws Exception`
**Detail:** Non-trivial public method with no Javadoc. Implements upsert logic for `unit_service`: checks for existence first, then inserts or updates. The upsert semantics are undocumented.

#### A81-35 — MEDIUM — No Javadoc on `getServiceByUnitId`
**Location:** `UnitDAO.java`, line 761
**Signature:** `public ArrayList<ServiceBean> getServiceByUnitId(String unitId) throws Exception`
**Detail:** Non-trivial public method with no Javadoc. The SQL normalises `setDur` to `setIntval` for `service_type` (line 790), a silent data transformation that callers cannot anticipate without reading the implementation.

#### A81-36 — MEDIUM — No Javadoc on `getImpactByUnitId`
**Location:** `UnitDAO.java`, line 822
**Signature:** `public List<ImpactBean> getImpactByUnitId(Long unitId) throws Exception`
**Detail:** Public method with no Javadoc. Returns a `List` for a single unit ID; the join to `unit_service` means the list may be empty if no service record exists.

#### A81-37 — MEDIUM — No Javadoc on `getChecklistSettings`
**Location:** `UnitDAO.java`, line 833
**Signature:** `public ArrayList<ChecklistBean> getChecklistSettings(String unitId) throws Exception`
**Detail:** Public method with no Javadoc. Returns a list for a single unit (may contain zero or one element). Only retrieves the `driver_based` flag.

#### A81-38 — MEDIUM — No Javadoc on `resetCalibration`
**Location:** `UnitDAO.java`, line 875
**Signature:** `public void resetCalibration(int equipId) throws SQLException`
**Detail:** Non-trivial public method with no Javadoc. Delegates entirely to `UnitCalibrationStarterInDatabase.startCalibration()`. What "resetting calibration" entails (what data is written, what state is cleared) is opaque without Javadoc.

#### A81-39 — MEDIUM — No Javadoc on `updateChecklistSettings`
**Location:** `UnitDAO.java`, line 879
**Signature:** `public void updateChecklistSettings(ChecklistBean bean) throws SQLException`
**Detail:** Public method with no Javadoc. Updates only the `driver_based` column on the `unit` table.

#### A81-40 — MEDIUM — No Javadoc on `getSessionHoursCalilbration`
**Location:** `UnitDAO.java`, line 909
**Signature:** `public double getSessionHoursCalilbration(String reset_cal_date, String equipId) throws Exception`
**Detail:** Non-trivial public method with no Javadoc. Computes total session hours since a calibration reset date by summing `(finish_servertime - start_servertime)` across sessions. The truncation to whole hours (`diff / 3600000`) loses sub-hour precision — a significant accuracy limitation that is undocumented. The method name contains a typo (`Calilbration` instead of `Calibration`).

#### A81-41 — MEDIUM — No Javadoc on `getAllUnitSearch`
**Location:** `UnitDAO.java`, line 958
**Signature:** `public List<UnitBean> getAllUnitSearch(String compId, Boolean activeStatus, String searchUnit) throws Exception`
**Detail:** Non-trivial public method with no Javadoc. `searchUnit` triggers a `containing()` filter only when non-empty; when empty all units are returned. The relationship between this method and `getAllUnitsByCompanyId` (which always filters active-only) is undocumented.

---

## 3. Summary Table

| ID | Severity | File | Location | Description |
|---|---|---|---|---|
| A81-1 | LOW | TrainingDAO.java | line 20 | No class-level Javadoc |
| A81-2 | MEDIUM | TrainingDAO.java | line 23 | No Javadoc on `getTrainingByDriver` |
| A81-3 | MEDIUM | TrainingDAO.java | line 55 | No Javadoc on `addTraining` |
| A81-4 | MEDIUM | TrainingDAO.java | line 70 | No Javadoc on `deleteTraining` (destructive, undocumented) |
| A81-5 | MEDIUM | TrainingDAO.java | line 76 | No Javadoc on `sendTrainingExpiryDailyEmail` |
| A81-6 | MEDIUM | TrainingDAO.java | line 119 | No Javadoc on `sendTrainingExpiryWeeklyEmail` |
| A81-7 | LOW | UnitDAO.java | line 22 | No class-level Javadoc |
| A81-8 | MEDIUM | UnitDAO.java | line 26 | No Javadoc on `getInstance` |
| A81-9 | MEDIUM | UnitDAO.java | line 40 | No Javadoc on `getAssignments` |
| A81-10 | MEDIUM | UnitDAO.java | line 52 | No Javadoc on `addAssignment` |
| A81-11 | MEDIUM | UnitDAO.java | line 80 | No Javadoc on `deleteAssignment` (destructive, undocumented) |
| A81-12 | MEDIUM | UnitDAO.java | line 98 | No Javadoc on `isAssignmentOverlapping` |
| A81-13 | MEDIUM | UnitDAO.java | line 119 | No Javadoc on `checkUnitByNm` |
| A81-14 | MEDIUM | UnitDAO.java | line 149 | No Javadoc on `checkUnitBySerial` |
| A81-15 | MEDIUM | UnitDAO.java | line 182 | No Javadoc on `checkUnitByMacAddr` |
| A81-16 | MEDIUM | UnitDAO.java | line 199 | No Javadoc on `getUnitBySerial` |
| A81-17 | MEDIUM | UnitDAO.java | lines 203, 256, 289, 297, 343, 368, 405, 443, 478, 534, 577, 614, 657 | Pervasive "LoginDAO" copy-paste in log strings throughout UnitDAO |
| A81-18 | MEDIUM | UnitDAO.java | lines 614, 657 | `getType` and `getPower` log wrong class AND wrong method name |
| A81-19 | MEDIUM | UnitDAO.java | line 256 | `getUnitMaxId` logs wrong class and wrong method name |
| A81-20 | MEDIUM | UnitDAO.java | line 910 | `getSessionHoursCalilbration` logs wrong method name (`getImpactByUnitId`) |
| A81-21 | MEDIUM | UnitDAO.java | line 242 | No Javadoc on `getAllUnitsByCompanyId` |
| A81-22 | MEDIUM | UnitDAO.java | line 252 | No Javadoc on `getUnitMaxId`; method name implies max ID but returns max+1 |
| A81-23 | MEDIUM | UnitDAO.java | line 288 | No Javadoc on `getUnitById` |
| A81-24 | MEDIUM | UnitDAO.java | line 293 | No Javadoc on `getUnitNameByComp`; dealer-expansion behaviour undocumented |
| A81-25 | MEDIUM | UnitDAO.java | line 340 | No Javadoc on `delUnitById`; soft delete disguised as deletion undocumented |
| A81-26 | MEDIUM | UnitDAO.java | line 364 | No Javadoc on `getAllUnitType` |
| A81-27 | MEDIUM | UnitDAO.java | line 401 | No Javadoc on `getAllUnitFuelType` |
| A81-28 | MEDIUM | UnitDAO.java | line 442 | No Javadoc on `saveUnitInfo`; insert/update duality undocumented |
| A81-29 | MEDIUM | UnitDAO.java | line 517 | No Javadoc on `saveUnitAccessInfo` |
| A81-30 | MEDIUM | UnitDAO.java | line 530 | No Javadoc on `getTotalUnitByID`; param `id` is a company ID, not a unit ID |
| A81-31 | MEDIUM | UnitDAO.java | line 573 | No Javadoc on `getAllUnitAttachment` |
| A81-32 | MEDIUM | UnitDAO.java | line 610 | No Javadoc on `getType` |
| A81-33 | MEDIUM | UnitDAO.java | line 653 | No Javadoc on `getPower` |
| A81-34 | MEDIUM | UnitDAO.java | line 699 | No Javadoc on `saveService` |
| A81-35 | MEDIUM | UnitDAO.java | line 761 | No Javadoc on `getServiceByUnitId`; silent `setDur`->`setIntval` coercion |
| A81-36 | MEDIUM | UnitDAO.java | line 822 | No Javadoc on `getImpactByUnitId` |
| A81-37 | MEDIUM | UnitDAO.java | line 833 | No Javadoc on `getChecklistSettings` |
| A81-38 | MEDIUM | UnitDAO.java | line 875 | No Javadoc on `resetCalibration` |
| A81-39 | MEDIUM | UnitDAO.java | line 879 | No Javadoc on `updateChecklistSettings` |
| A81-40 | MEDIUM | UnitDAO.java | line 909 | No Javadoc on `getSessionHoursCalilbration`; truncation to whole hours undocumented; method name typo |
| A81-41 | MEDIUM | UnitDAO.java | line 958 | No Javadoc on `getAllUnitSearch` |

**Totals:** 2 LOW, 39 MEDIUM, 0 HIGH
