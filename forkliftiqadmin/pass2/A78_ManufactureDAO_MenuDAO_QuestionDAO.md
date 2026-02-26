# Pass 2 – Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A78
**Files Audited:**
1. `src/main/java/com/dao/ManufactureDAO.java`
2. `src/main/java/com/dao/MenuDAO.java`
3. `src/main/java/com/dao/QuestionDAO.java`

**Test Directory Searched:** `src/test/java/`

---

## Test Directory Inventory

The test directory contains exactly four test files:

| File | Package |
|------|---------|
| `UnitCalibrationImpactFilterTest.java` | `com.calibration` |
| `UnitCalibrationTest.java` | `com.calibration` |
| `UnitCalibratorTest.java` | `com.calibration` |
| `ImpactUtilTest.java` | `com.util` |

All four test files are unrelated to the three DAO classes under audit. A grep search for `ManufactureDAO`, `MenuDAO`, `QuestionDAO`, `Manufacture`, `Menu`, and `Question` in the test directory returned **zero matches** in all cases.

---

## Reading Evidence

### 1. ManufactureDAO (`com.dao.ManufactureDAO`)

**Class name:** `ManufactureDAO`

**Fields:**

| Name | Line | Notes |
|------|------|-------|
| `log` | 19 | `private static Logger` |
| `QUERY_MANUFACTURE_SQL` | 21–22 | `private static final String` |
| `QUERY_VEHICLE_BY_MANUFACTURE_SQL` | 24–25 | `private static final String` |
| `theInstance` | 27 | `private static ManufactureDAO` (singleton) |

**Methods:**

| Method | Line | Visibility / Static |
|--------|------|---------------------|
| `getInstance()` | 29 | `public synchronized static` |
| `ManufactureDAO()` (constructor) | 37 | `private` |
| `getAllManufactures(String companyId)` | 40 | `public static` |
| `getManufactureById(String id)` | 60 | `public` (instance) |
| `delManufacturById(String id)` | 99 | `public static` |
| `checkManuByNm(String name, String id)` | 137 | `public` (instance) |
| `saveManufacturer(ManufactureBean)` | 174 | `public static` |
| `updateManufacturer(ManufactureBean)` | 210 | `public static` |
| `getManu_type_fuel_rel(String manuId)` | 247 | `public` (instance) |
| `checkManu_type_fuel_rel(ManuTypeFuleRelBean)` | 291 | `public` (instance) |
| `saveManu_type_fuel_rel(ManuTypeFuleRelBean)` | 335 | `public` (instance) |
| `delManu_type_fuel_rel(String relId)` | 373 | `public` (instance) |
| `isVehicleAssignedToManufacturer(String manufacturerId)` | 404 | `public static` |

---

### 2. MenuDAO (`com.dao.MenuDAO`)

**Class name:** `MenuDAO`

**Fields:**

| Name | Line | Notes |
|------|------|-------|
| `log` | 19 | `private static Logger` |

**Methods:**

| Method | Line | Visibility / Static |
|--------|------|---------------------|
| `getAllMenu(String lanCode)` | 21 | `public` (instance) |
| `getRoleMenu(ArrayList<String> arrRole, String lanCode)` | 66 | `public` (instance) |
| `saveRoleMenu(String roleId, String menuId)` | 112 | `public` (instance) |
| `delRoleMenu(String roleId)` | 139 | `public` (instance) |

---

### 3. QuestionDAO (`com.dao.QuestionDAO`)

**Class name:** `QuestionDAO`

**Fields:**

| Name | Line | Notes |
|------|------|-------|
| `log` | 26 | `private static Logger` |
| `unitDao` | 28 | `private UnitDAO` (instance field, set via `UnitDAO.getInstance()`) |

**Methods:**

| Method | Line | Visibility / Static |
|--------|------|---------------------|
| `getQuesLanId(String compId)` | 30 | `public` (instance) |
| `getQuestionByUnitId(String unitId, String attchId, String compId, boolean barcode)` | 64 | `public` (instance) |
| `getQuestionByCategory(String manuId, String typeId, String fuelTypeId, String attchId, String compId)` | 128 | `public static` |
| `delQuestionById(String id)` | 174 | `public static` |
| `hideQuestionById(String id, String manuId, String typeId, String fuleTypeId, String compId, String attchId)` | 197 | `public static` |
| `showQuestionById(String id)` | 210 | `public static` |
| `copyQuestionToCompId(String id, String manuId, String typeId, String fuleTypeId, String compId, String attchId)` | 216 | `private static` |
| `getQuestionById(String id)` | 263 | `public static` |
| `getQuestionContentById(String qId, String lanId)` | 311 | `public` (instance) |
| `saveQuestionInfo(QuestionBean, String lanId, int compId)` | 363 | `public static` |
| `saveQuestionContent(QuestionContentBean)` | 436 | `public static` |
| `updateQuestionInfo(QuestionBean)` | 516 | `public static` |
| `getMaxQuestionId(String manuId, String typeId, String fuelTypeId, String compId)` | 555 | `public static` |
| `getAllAnswerType()` | 595 | `public static` |

---

## Findings

### ManufactureDAO Findings

**A78-1 | Severity: CRITICAL | ManufactureDAO has zero test coverage — no test file exists**
No test class for `ManufactureDAO` was found anywhere in `src/test/java/`. All 13 methods are completely untested. This class performs database mutations (INSERT, UPDATE, DELETE with explicit transaction control) and is entirely unverified by automated tests.

**A78-2 | Severity: CRITICAL | SQL injection in `getManufactureById` — no test verifies input is numeric**
Line 72: `String sql = "select id,name from manufacture where id = " + id;` — the `id` parameter is concatenated directly into the SQL string without validation or parameterisation. No test verifies rejection of non-numeric or malicious input.

**A78-3 | Severity: CRITICAL | SQL injection in `checkManuByNm` — no test covers injection via `name` parameter**
Lines 149–151: the `name` parameter is concatenated directly into SQL: `"select id from manufacture where name = '" + name + "'"`. A single-quote in `name` will break the query or allow injection. No test exercises this path.

**A78-4 | Severity: CRITICAL | SQL injection in `getManu_type_fuel_rel` — `manuId` concatenated directly**
Line 263: `" where manu_id = " + manuId` — `manuId` is not validated or bound as a parameter. No test covers this path.

**A78-5 | Severity: HIGH | `delManufacturById` rollback on null `conn` causes NullPointerException**
Line 127: `conn.rollback()` is called inside the catch block. If `DBUtil.getConnection(false)` fails and `conn` is null, a `NullPointerException` will be thrown, masking the original exception. No test covers the connection-failure path.

**A78-6 | Severity: HIGH | `saveManufacturer` and `updateManufacturer` do not close connection when `ps` is null**
Lines 201–204 and 237–240: `DBUtil.closeConnection(conn)` is placed inside `if (null != ps)` in the finally block. If `conn.prepareStatement()` throws before `ps` is assigned, the connection leaks. No test covers this path.

**A78-7 | Severity: HIGH | `checkManu_type_fuel_rel` returns `true` (duplicate exists) when `manuTypeFuleRelBean` is null**
Lines 319–321: the null-bean branch returns `true`, implying a duplicate. This is arguably a logic inversion (should be "no constraint to check" = false or an exception). No test covers the null-bean path.

**A78-8 | Severity: HIGH | `isVehicleAssignedToManufacturer` leaks `ResultSet` — `rs` is never closed**
Lines 417–429: `rs` is declared locally, assigned from `ps.executeQuery()`, used, but there is no `rs.close()` call in the finally block. No test covers this path to detect the leak.

**A78-9 | Severity: HIGH | Singleton `getInstance` mixed with static-method class design — untested and inconsistent**
`ManufactureDAO` exposes a singleton via `getInstance()` (line 29) but the majority of its non-trivial methods are `static` and do not require an instance. Instance methods (`getManufactureById`, `checkManuByNm`, `getManu_type_fuel_rel`, `checkManu_type_fuel_rel`, `saveManu_type_fuel_rel`, `delManu_type_fuel_rel`) are not accessible via the singleton pattern as it is currently used by callers. No test validates which access pattern is correct.

**A78-10 | Severity: MEDIUM | `getAllManufactures` — no test covers empty result set (no manufacturers for given companyId)**
The method returns an empty list when no rows match; this path is untested.

**A78-11 | Severity: MEDIUM | `getAllManufactures` — no test covers null or non-numeric `companyId` causing `Long.valueOf()` to throw `NumberFormatException`**
Line 47: `Long.valueOf(companyId)` will throw `NumberFormatException` for null or non-numeric input, which is then wrapped in `SQLException`. This edge case is untested.

**A78-12 | Severity: MEDIUM | `delManufacturById` — no test covers the case where the manufacture row does not exist (executeUpdate returns 0)**
Line 119: when `executeUpdate() != 1`, the method returns `false` without rolling back the already-executed delete of `manu_type_fuel_rel` rows, resulting in data inconsistency. This path is untested.

**A78-13 | Severity: MEDIUM | `saveManufacturer` — no test covers null `ManufactureBean` input**
Lines 185–194: null bean returns `false` but the finally block only closes the connection inside `if (null != ps)`, which will be false — so the connection acquired on line 183 leaks. No test covers this branch.

**A78-14 | Severity: MEDIUM | `updateManufacturer` — same null-bean connection-leak as `saveManufacturer` (line 229–232), untested**

**A78-15 | Severity: MEDIUM | `checkManuByNm` — no test covers the empty-string `id` branch vs. the non-empty `id` branch**
Line 150: `if (!id.equalsIgnoreCase(""))` selects between two query forms. Neither branch is tested.

**A78-16 | Severity: LOW | Log message in `delManufacturById` is misleading — says "LoginDAO" not "ManufactureDAO"**
Line 102: `log.info("Inside LoginDAO Method : delManufacturById")` — copy-paste error. Multiple other methods share this logging defect. No test would catch misleading log output.

---

### MenuDAO Findings

**A78-17 | Severity: CRITICAL | MenuDAO has zero test coverage — no test file exists**
No test class for `MenuDAO` was found anywhere in `src/test/java/`. All 4 methods are completely untested. This class performs database reads and writes for role-menu security relationships.

**A78-18 | Severity: CRITICAL | SQL injection in `getAllMenu` — `lanCode` concatenated into SQL string**
Line 35: `"...lan_code = '"+lanCode+"'"` — `lanCode` is user-influenced and concatenated directly. No test verifies sanitisation or rejection of malicious input.

**A78-19 | Severity: CRITICAL | SQL injection in `getRoleMenu` — `lanCode` and `arrRole` concatenated into SQL**
Lines 79–82: both `Util.ArraListToString(arrRole)` and `lanCode` are concatenated directly into the SQL string. No test verifies either parameter. A maliciously constructed role list could alter the query structure.

**A78-20 | Severity: CRITICAL | SQL injection in `saveRoleMenu` — both `roleId` and `menuId` concatenated directly**
Line 124: `"insert into role_menu_rel (role_id,menu_id) values ("+roleId+","+menuId+")"` — both parameters are directly concatenated with no validation or binding. No test exists.

**A78-21 | Severity: CRITICAL | SQL injection in `delRoleMenu` — `roleId` concatenated directly**
Line 151: `"delete from role_menu_rel where role_id\t="+roleId` — `roleId` concatenated without binding. No test exists. Note the embedded tab character between `role_id` and `=` is a code smell; it will parse correctly in SQL but is invisible in code review.

**A78-22 | Severity: HIGH | `saveRoleMenu` uses `CONCUR_READ_ONLY` statement for a write operation**
Line 122: `conn.createStatement(ResultSet.TYPE_SCROLL_SENSITIVE, ResultSet.CONCUR_READ_ONLY)` is used to execute an INSERT via `stmt.executeUpdate()`. The `CONCUR_READ_ONLY` hint is contradictory for a mutation and may cause driver-specific failures. No test validates that the insert actually succeeds.

**A78-23 | Severity: HIGH | `delRoleMenu` — `rs` is declared but never assigned; `rs.close()` in the finally block will always be skipped (null check saves it), but the dead variable is misleading**
Lines 143, 162: `ResultSet rs = null;` is declared but never used in `delRoleMenu`. The same pattern exists in `saveRoleMenu` (line 117, 133). No test would highlight this dead code.

**A78-24 | Severity: HIGH | `getAllMenu` — no test covers empty result (no menus for given language code)**
The method returns an empty list silently; callers depending on at least one menu item will fail. Untested.

**A78-25 | Severity: HIGH | `getRoleMenu` — no test covers empty `arrRole` list**
If `arrRole` is empty, `Util.ArraListToString(arrRole)` produces an empty or malformed IN-clause (`role_id in()`), which is invalid SQL in most databases. No test verifies this edge case.

**A78-26 | Severity: MEDIUM | `getAllMenu` — no test covers null or unrecognised `lanCode`**

**A78-27 | Severity: MEDIUM | `delRoleMenu` — no test verifies behaviour when `roleId` does not exist (zero rows deleted, but method returns `true`)**
Line 153–154: `stmt.executeUpdate(sql)` result is not checked; the method always returns `true` if no exception is thrown, even if no rows were deleted. No test covers this path.

**A78-28 | Severity: LOW | `MenuDAO` imports `java.lang.reflect.Array` (line 3) but never uses it — dead import, untested code quality**

---

### QuestionDAO Findings

**A78-29 | Severity: CRITICAL | QuestionDAO has zero test coverage — no test file exists**
No test class for `QuestionDAO` was found anywhere in `src/test/java/`. All 14 methods are completely untested. This class manages the core checklist/question data with complex branching logic.

**A78-30 | Severity: CRITICAL | SQL injection in `getQuesLanId` — `compId` concatenated directly**
Line 42: `"select lan_id from company where id = " + compId` — no input validation or parameter binding. No test exists.

**A78-31 | Severity: CRITICAL | SQL injection in `getQuestionByUnitId` — `unitId`, `lanId`, `compId`, `attchId` all concatenated**
Lines 83–89: multiple caller-controlled values are concatenated into the SQL string. No test exercises this method.

**A78-32 | Severity: CRITICAL | SQL injection in `delQuestionById` — `id` concatenated directly**
Line 183: `"delete from question where id=" + id` — no binding or numeric validation. No test exists.

**A78-33 | Severity: CRITICAL | SQL injection in `getQuestionById` — `id` concatenated directly**
Line 275: `"select ... where id = " + id` — this method is also called internally by `hideQuestionById`, `showQuestionById`, and `copyQuestionToCompId`, meaning injection in any caller of those methods propagates here as well. No test exists.

**A78-34 | Severity: CRITICAL | SQL injection in `getQuestionContentById` — `qId` and `lanId` concatenated**
Lines 328–330: both `qId` and `lanId` are concatenated into SQL strings across two branches. No test exists.

**A78-35 | Severity: HIGH | `hideQuestionById` — no test covers the three distinct logic branches**
Lines 201–207: three distinct execution paths exist:
  1. Global question with no `comp_id` and no `copied_from_id` → copy then mark inactive via `updateQuestionInfo`
  2. Question with a `comp_id` → mark active as `"f"` directly
  3. `comp_id == null` but `copied_from_id != null` → silent no-op (no else clause), meaning a copied-global question that was already hidden is silently ignored

The third (implicit) path is likely a bug. No test covers any of these paths.

**A78-36 | Severity: HIGH | `hideQuestionById` — `getQuestionById(id).get(0)` throws `IndexOutOfBoundsException` if question does not exist**
Line 198: if the question ID does not exist in the database, `getQuestionById` returns an empty list and `.get(0)` throws unchecked. The same defect exists in `showQuestionById` (line 211). No test covers missing-ID input.

**A78-37 | Severity: HIGH | `copyQuestionToCompId` connection never closed if `ps` is null after exception before `ps` assignment**
Lines 254–257: `DBUtil.closeConnection(conn)` is inside `if (null != ps)`. If `conn.prepareStatement()` throws, `ps` remains null and the connection leaks. No test covers this.

**A78-38 | Severity: HIGH | `saveQuestionInfo` uses `nextval('question_id_seq')` on all rows in the `question` table**
Line 376: `"select nextval('question_id_seq') from question"` — `nextval` is called once per existing row in the `question` table, not once total. Only the first value is used (line 378), but sequence values are consumed and wasted for every existing row. This is a correctness bug under load. No test covers sequence exhaustion or the one-vs-many row distinction.

**A78-39 | Severity: HIGH | `saveQuestionContent` — no test covers the three-way branch: English update vs. non-English update vs. non-English insert**
Lines 451–491: the method branches on `language_id == "1"` (update question table) or on whether an existing `question_content` row exists (update vs. insert). All three paths are untested.

**A78-40 | Severity: HIGH | `updateQuestionInfo` — NullPointerException if `questionBean.getActive()` is null**
Line 534: `questionBean.getActive().equalsIgnoreCase("t")` — if `active` field is null, this throws NPE. No test covers null `active` value.

**A78-41 | Severity: HIGH | `getQuestionByCategory` — no test covers the `attchId` blank vs. non-blank branching in parameter binding**
Lines 139–162: the conditional attachment filter is applied twice in the query (once per UNION leg) and the parameter-binding loop iterates twice. The index math (`++index`) is fragile; if `attchId` is blank in one iteration and non-blank in another (impossible here but structurally risky), the prepared statement index would be wrong. No test validates parameter count or binding correctness.

**A78-42 | Severity: HIGH | `getMaxQuestionId` — returns `1` as default when no rows match or `max()` returns NULL**
Line 562: `int id = 1;` is the default. When the query returns SQL NULL (no matching rows), `rs.getInt(1)` returns `0`, but the code does not distinguish between "no result" and "result is NULL" — it overwrites `id` with `0`. A new question would then be inserted with `order_no = 0`. No test covers the no-rows case.

**A78-43 | Severity: MEDIUM | `getQuestionByUnitId` — `arrUnit.get(0)` throws `IndexOutOfBoundsException` if `unitId` does not exist**
Line 78: if `unitDao.getUnitById(unitId)` returns an empty list, `.get(0)` throws unchecked. No test covers an invalid `unitId`.

**A78-44 | Severity: MEDIUM | `getQuestionByCategory` — throws `IllegalArgumentException` for empty params but `getQuestionByUnitId` does not — inconsistent validation contract across the class**
Lines 131–134 vs. lines 64–125: no test enforces or documents the intended validation policy for the class.

**A78-45 | Severity: MEDIUM | `getQuestionContentById` — sentinel XmlBean with `name = " "` silently returned when no content found**
Lines 340–345: when the result set is empty, a placeholder bean with a space is returned rather than an empty list or an exception. Callers cannot distinguish "no translation" from "translation is a space". No test documents this contract.

**A78-46 | Severity: MEDIUM | `saveQuestionInfo` — no test covers null `QuestionBean` input**
Lines 383–415: if `questionBean` is null, the outer `if` block is skipped, the method returns `true` (line 432), and no insert is performed. A silent success on null input is incorrect. No test covers this.

**A78-47 | Severity: MEDIUM | `saveQuestionContent` — no test covers null `QuestionContentBean` input**
Lines 450+: if `qeustionContentBean` is null, the method returns `true` silently. Same defect as A78-46.

**A78-48 | Severity: MEDIUM | `copyQuestionToCompId` — `attchId` empty-string check uses `StringUtils.isNotEmpty` (line 234) but `getQuestionByCategory` uses `StringUtils.isNotBlank` (line 139) for the same semantic — inconsistent treatment of whitespace-only attachment ID**
No test validates boundary behaviour of whitespace-only `attchId` values.

**A78-49 | Severity: LOW | Logger name typo: `"com.dao.QuesionDAO"` (missing 't') at line 26 of QuestionDAO**
This causes log output to appear under an incorrect category name, making production log tracing difficult. No test would catch this.

**A78-50 | Severity: LOW | Multiple methods log `"Inside LoginDAO Method"` instead of `"Inside QuestionDAO Method"` — copy-paste log pollution across QuestionDAO**
Affected methods: `getQuesLanId` (line 35), `getQuestionByUnitId` (line 69), `delQuestionById` (line 177), `getQuestionById` (line 267), `getQuestionContentById` (line 316), `saveQuestionInfo` (line 369), `saveQuestionContent` (line 442), `updateQuestionInfo` (line 521), `getMaxQuestionId` (line 560), `getAllAnswerType` (line 600). No test would detect this.

---

## Summary Table

| Finding | Severity | Class | Category |
|---------|----------|-------|----------|
| A78-1 | CRITICAL | ManufactureDAO | Zero coverage |
| A78-2 | CRITICAL | ManufactureDAO | SQL injection |
| A78-3 | CRITICAL | ManufactureDAO | SQL injection |
| A78-4 | CRITICAL | ManufactureDAO | SQL injection |
| A78-5 | HIGH | ManufactureDAO | NPE / error path |
| A78-6 | HIGH | ManufactureDAO | Resource leak |
| A78-7 | HIGH | ManufactureDAO | Logic defect |
| A78-8 | HIGH | ManufactureDAO | Resource leak |
| A78-9 | HIGH | ManufactureDAO | Design inconsistency |
| A78-10 | MEDIUM | ManufactureDAO | Edge case |
| A78-11 | MEDIUM | ManufactureDAO | Edge case / exception |
| A78-12 | MEDIUM | ManufactureDAO | Data inconsistency |
| A78-13 | MEDIUM | ManufactureDAO | Resource leak / null |
| A78-14 | MEDIUM | ManufactureDAO | Resource leak / null |
| A78-15 | MEDIUM | ManufactureDAO | Branch coverage |
| A78-16 | LOW | ManufactureDAO | Log correctness |
| A78-17 | CRITICAL | MenuDAO | Zero coverage |
| A78-18 | CRITICAL | MenuDAO | SQL injection |
| A78-19 | CRITICAL | MenuDAO | SQL injection |
| A78-20 | CRITICAL | MenuDAO | SQL injection |
| A78-21 | CRITICAL | MenuDAO | SQL injection |
| A78-22 | HIGH | MenuDAO | Statement mode |
| A78-23 | HIGH | MenuDAO | Dead code |
| A78-24 | HIGH | MenuDAO | Edge case |
| A78-25 | HIGH | MenuDAO | Edge case |
| A78-26 | MEDIUM | MenuDAO | Edge case |
| A78-27 | MEDIUM | MenuDAO | Silent failure |
| A78-28 | LOW | MenuDAO | Dead import |
| A78-29 | CRITICAL | QuestionDAO | Zero coverage |
| A78-30 | CRITICAL | QuestionDAO | SQL injection |
| A78-31 | CRITICAL | QuestionDAO | SQL injection |
| A78-32 | CRITICAL | QuestionDAO | SQL injection |
| A78-33 | CRITICAL | QuestionDAO | SQL injection |
| A78-34 | CRITICAL | QuestionDAO | SQL injection |
| A78-35 | HIGH | QuestionDAO | Logic / branch |
| A78-36 | HIGH | QuestionDAO | IndexOutOfBounds |
| A78-37 | HIGH | QuestionDAO | Resource leak |
| A78-38 | HIGH | QuestionDAO | Correctness / sequence |
| A78-39 | HIGH | QuestionDAO | Branch coverage |
| A78-40 | HIGH | QuestionDAO | NPE |
| A78-41 | HIGH | QuestionDAO | Parameter binding |
| A78-42 | HIGH | QuestionDAO | Default value defect |
| A78-43 | MEDIUM | QuestionDAO | IndexOutOfBounds |
| A78-44 | MEDIUM | QuestionDAO | Inconsistent contract |
| A78-45 | MEDIUM | QuestionDAO | Sentinel value |
| A78-46 | MEDIUM | QuestionDAO | Null / silent success |
| A78-47 | MEDIUM | QuestionDAO | Null / silent success |
| A78-48 | MEDIUM | QuestionDAO | Inconsistent validation |
| A78-49 | LOW | QuestionDAO | Logger typo |
| A78-50 | LOW | QuestionDAO | Log pollution |

**Total findings: 50**
CRITICAL: 14 | HIGH: 20 | MEDIUM: 12 | LOW: 4
