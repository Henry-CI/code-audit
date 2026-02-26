# Pass 3 Documentation Audit — A79
**Audit run:** 2026-02-26-01
**Files:** dao/QuestionDAO.java, dao/ResultDAO.java, dao/RoleDAO.java
**Agent:** A79

---

## 1. Reading Evidence

### 1.1 QuestionDAO.java
**Source:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/dao/QuestionDAO.java`

**Class:** `QuestionDAO` — line 24

**Fields:**

| Name | Type | Line |
|---|---|---|
| `log` | `static Logger` | 26 |
| `unitDao` | `UnitDAO` | 28 |

**Methods:**

| Method | Visibility | Static | Line |
|---|---|---|---|
| `getQuesLanId(String compId)` | public | no | 30 |
| `getQuestionByUnitId(String unitId, String attchId, String compId, boolean barcode)` | public | no | 64 |
| `getQuestionByCategory(String manuId, String typeId, String fuelTypeId, String attchId, String compId)` | public | yes | 128 |
| `delQuestionById(String id)` | public | yes | 174 |
| `hideQuestionById(String id, String manuId, String typeId, String fuleTypeId, String compId, String attchId)` | public | yes | 197 |
| `showQuestionById(String id)` | public | yes | 210 |
| `copyQuestionToCompId(String id, String manuId, String typeId, String fuleTypeId, String compId, String attchId)` | private | yes | 216 |
| `getQuestionById(String id)` | public | yes | 263 |
| `getQuestionContentById(String qId, String lanId)` | public | no | 311 |
| `saveQuestionInfo(QuestionBean questionBean, String lanId, int compId)` | public | yes | 363 |
| `saveQuestionContent(QuestionContentBean qeustionContentBean)` | public | yes | 436 |
| `updateQuestionInfo(QuestionBean questionBean)` | public | yes | 516 |
| `getMaxQuestionId(String manuId, String typeId, String fuelTypeId, String compId)` | public | yes | 555 |
| `getAllAnswerType()` | public | yes | 595 |

---

### 1.2 ResultDAO.java
**Source:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/dao/ResultDAO.java`

**Class:** `ResultDAO` — line 17

**Fields:**

| Name | Type | Line |
|---|---|---|
| `log` | `static Logger` | 18 |

**Methods:**

| Method | Visibility | Static | Line |
|---|---|---|---|
| `saveResult(ResultBean resultBean, String compId)` | public | no | 20 |
| `countResultsCompletedToday(Long compId, String timezone)` | public | no | 124 |
| `getPreOpsCheckReport(Long compId, PreOpsReportFilterBean filter, String dateFormat, String timezone)` | public | no | 128 |
| `getChecklistResultInc(Long driverId, Date sDate, Date eDate)` | public | no | 132 |
| `getChecklistResultById(int resultId)` | public | no | 166 |
| `getOverallStatus(Long resultId, String unitId)` | public | no | 202 |
| `printErrors(Long resultId, boolean pdfTag)` | public | no | 245 |
| `checkDuplicateResult(String driverId, String unitId, Timestamp time)` | public | no | 283 |

---

### 1.3 RoleDAO.java
**Source:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/java/com/dao/RoleDAO.java`

**Class:** `RoleDAO` — line 15

**Fields:**

| Name | Type | Line |
|---|---|---|
| `log` | `static Logger` | 17 |

**Methods:**

| Method | Visibility | Static | Line |
|---|---|---|---|
| `getRoles()` | public | no | 19 |

---

## 2. Findings

### A79-1 [LOW] — QuestionDAO: No class-level Javadoc
**File:** QuestionDAO.java, line 24
**Detail:** The `QuestionDAO` class has no `/** ... */` Javadoc comment above its declaration. There is no description of the class's purpose, its role as the data-access layer for the `question` and `question_content` tables, or the thread-safety implications of mixing instance and static methods.

---

### A79-2 [MEDIUM] — QuestionDAO.getQuesLanId: Undocumented non-trivial public method
**File:** QuestionDAO.java, line 30
**Signature:** `public int getQuesLanId(String compId) throws Exception`
**Detail:** No Javadoc at all. The method queries the `company` table to look up a `lan_id` by company ID. This is non-trivial: it performs a raw SQL query (no parameterization, SQL injection risk), wraps any exception in a `SQLException`, and returns `0` as a default if no row is found. None of this is documented. Additionally, the log message inside the method incorrectly names the owning class as `"LoginDAO"` instead of `"QuestionDAO"` — a copy-paste artifact present in several methods across this class.

---

### A79-3 [MEDIUM] — QuestionDAO.getQuestionByUnitId: Undocumented non-trivial public method
**File:** QuestionDAO.java, line 64
**Signature:** `public ArrayList<QuestionBean> getQuestionByUnitId(String unitId, String attchId, String compId, boolean barcode) throws Exception`
**Detail:** No Javadoc. The method builds a complex multi-join SQL query that selects questions for a unit filtered by attachment, company, and optionally limited to barcode-type (`answer_type = 1`) questions. The `compId` derivation path (resolved from unit when blank), the `attchId = "0"` sentinel meaning "no attachment", and the `barcode` flag filtering to `answer_type = 1` are all undocumented behaviours.

---

### A79-4 [MEDIUM] — QuestionDAO.getQuestionByCategory: Undocumented non-trivial public method
**File:** QuestionDAO.java, line 128
**Signature:** `public static List<QuestionBean> getQuestionByCategory(String manuId, String typeId, String fuelTypeId, String attchId, String compId) throws SQLException`
**Detail:** No Javadoc. The method uses a UNION query to merge company-specific questions with global questions (all nullable FKs) while excluding globals that have already been copied to the company. It also validates all required parameters with `IllegalArgumentException`. This logic is entirely undocumented.

---

### A79-5 [MEDIUM] — QuestionDAO.delQuestionById: Undocumented non-trivial public method
**File:** QuestionDAO.java, line 174
**Signature:** `public static void delQuestionById(String id) throws Exception`
**Detail:** No Javadoc. The method executes a hard `DELETE` via unparameterized SQL (SQL injection risk on `id`). There is no documentation of preconditions, the lack of cascading-delete safety checks, or the SQL injection risk.

---

### A79-6 [MEDIUM] — QuestionDAO.hideQuestionById: Undocumented non-trivial public method
**File:** QuestionDAO.java, line 197
**Signature:** `public static void hideQuestionById(String id, String manuId, String typeId, String fuleTypeId, String compId, String attchId) throws Exception`
**Detail:** No Javadoc. The method implements a non-obvious three-branch strategy: (1) if the question is global (no comp_id and no copied_from_id), copy it to the company and set `active = false`; (2) if it already belongs to the company, set `active = false`; (3) implicitly, if `comp_id == null` but `copied_from_id != null`, nothing is done. This conditional logic and the copy-then-hide pattern are completely undocumented.

---

### A79-7 [MEDIUM] — QuestionDAO.showQuestionById: Undocumented non-trivial public method
**File:** QuestionDAO.java, line 210
**Signature:** `public static void showQuestionById(String id) throws Exception`
**Detail:** No Javadoc. Sets `active = "t"` for the given question. While simpler than `hideQuestionById`, it is the complementary operation and is also the only entry point that re-enables a previously hidden question. The relationship to `hideQuestionById` and the fact that it applies unconditionally to any question (including global ones) is undocumented.

---

### A79-8 [MEDIUM] — QuestionDAO.getQuestionById: Undocumented non-trivial public method
**File:** QuestionDAO.java, line 263
**Signature:** `public static ArrayList<QuestionBean> getQuestionById(String id) throws Exception`
**Detail:** No Javadoc. Returns a list despite the semantics suggesting a single record is expected; callers (e.g., `hideQuestionById`, `showQuestionById`, `copyQuestionToCompId`) use `.get(0)` without bounds checking. This can cause `IndexOutOfBoundsException` if no record exists. The unparameterized SQL also carries a SQL injection risk. Neither the list-vs-optional semantic nor the risk is documented.

---

### A79-9 [MEDIUM] — QuestionDAO.getQuestionContentById: Undocumented non-trivial public method
**File:** QuestionDAO.java, line 311
**Signature:** `public ArrayList<XmlBean> getQuestionContentById(String qId, String lanId) throws Exception`
**Detail:** No Javadoc. The method has an important branch: when `lanId` equals `"1"` (English default), it reads from the `question` table; otherwise it reads from `question_content`. If no content is found, it synthesises a placeholder `XmlBean` with content `" "` to guarantee a non-empty list. This fallback behaviour, the language-ID semantics, and the XmlBean population are undocumented.

---

### A79-10 [MEDIUM] — QuestionDAO.saveQuestionInfo: Undocumented non-trivial public method
**File:** QuestionDAO.java, line 363
**Signature:** `public static boolean saveQuestionInfo(QuestionBean questionBean, String lanId, int compId) throws SQLException`
**Detail:** No Javadoc. The method performs a two-phase insert: it first fetches the next sequence value from `question_id_seq` (non-atomic with the insert), then inserts the question row, and conditionally inserts a `question_content` row when `lanId != "1"`. Returns `false` if any insert affects other than one row. The non-atomic ID generation, the language-conditioned secondary insert, and the return semantics are all undocumented.

---

### A79-11 [MEDIUM] — QuestionDAO.saveQuestionContent: Undocumented non-trivial public method
**File:** QuestionDAO.java, line 436
**Signature:** `public static boolean saveQuestionContent(QuestionContentBean qeustionContentBean) throws SQLException`
**Detail:** No Javadoc. The method upserts question content: for English (`language_id = "1"`) it updates the `question` table directly; for other languages it checks `question_content` and performs either an `UPDATE` or `INSERT`. This three-way routing is entirely undocumented. Also note the parameter name `qeustionContentBean` is a persistent typo.

---

### A79-12 [MEDIUM] — QuestionDAO.updateQuestionInfo: Undocumented non-trivial public method
**File:** QuestionDAO.java, line 516
**Signature:** `public static boolean updateQuestionInfo(QuestionBean questionBean) throws SQLException`
**Detail:** No Javadoc. The method updates `content`, `expectedanswer`, `answer_type`, and `active` on the question row. Notably, it does NOT update `order_no`, `type_id`, `manu_id`, `fule_type_id`, `attachment_id`, or `comp_id` — callers relying on a full update would be silently wrong. The partial-update scope is undocumented.

---

### A79-13 [MEDIUM] — QuestionDAO.getMaxQuestionId: Undocumented non-trivial public method
**File:** QuestionDAO.java, line 555
**Signature:** `public static int getMaxQuestionId(String manuId, String typeId, String fuelTypeId, String compId) throws Exception`
**Detail:** No Javadoc. Despite the name, the method does not return the maximum question ID — it returns `max(order_no)`, which is an ordering value. The misleading name combined with the absence of documentation is a documentation accuracy issue: a caller reading only the signature would assume the return value is an identifier, not an ordering key. Returns `1` (not `0`) when the result set has no rows, which is also undocumented default behaviour.

---

### A79-14 [MEDIUM] — QuestionDAO.getAllAnswerType: Undocumented non-trivial public method
**File:** QuestionDAO.java, line 595
**Signature:** `public static ArrayList<AnswerTypeBean> getAllAnswerType() throws Exception`
**Detail:** No Javadoc. Queries the `answer_type` table ordered by `id` and returns all rows. The log message inside the method incorrectly reads `"Inside LoginDAO Method : getQuestionByUnitId"` — a copy-paste error referring to a different method in the same class.

---

### A79-15 [MEDIUM] — ResultDAO: No class-level Javadoc; all public methods undocumented
**File:** ResultDAO.java, line 17
**Detail (class):** `ResultDAO` has no class-level Javadoc comment.

The following 8 public methods in `ResultDAO` all lack Javadoc and are individually non-trivial. They are grouped here for conciseness but each constitutes a MEDIUM finding:

| Sub-ID | Method | Line | Key undocumented behaviour |
|---|---|---|---|
| A79-15a | `saveResult` | 20 | Multi-table transactional insert (result + answers); compensating DELETE on any failure; hour-meter update side-effect; returns `result_id` on success or `0` on failure. No documented contract. |
| A79-15b | `countResultsCompletedToday` | 124 | Delegates entirely to `PreOpsByCompanyIdQuery.count`. The timezone parameter's effect and what "today" means relative to it are undocumented. |
| A79-15c | `getPreOpsCheckReport` | 128 | Delegates to `PreOpsByCompanyIdQuery.report`. The interaction between `filter`, `dateFormat`, and `timezone`, and the contents of the returned `PreOpsReportBean`, are undocumented. |
| A79-15d | `getChecklistResultInc` | 132 | Returns results for a driver between two dates; date range is inclusive on both ends (uses `>=` and `<=`); timestamp is formatted `dd/mm/yyyy HH24:MI:SS` in the query. Undocumented. |
| A79-15e | `getChecklistResultById` | 166 | Retrieves a single result by ID but returns a list; odometer stored as `double` but surfaced as `String` via concatenation (`+ ""`). Undocumented. |
| A79-15f | `getOverallStatus` | 202 | Computes INCOMPLETE / FAIL / OK based on answer count vs. question count and wrong answers on `answer_type = 1` questions only. The three-state semantics and the barcode-only failure logic are undocumented. |
| A79-15g | `printErrors` | 245 | Returns a two-element `String[]` where `[0]` is formatted question/answer text and `[1]` is faulty-component text; `pdfTag` controls whether `\n` or `<br/>` is used as line separator; returns `"N/A"` when there are no errors. Undocumented. |
| A79-15h | `checkDuplicateResult` | 283 | Returns `true` if a result row already exists for the same driver, unit, and exact timestamp. Timestamp comparison uses string embedding (potential format mismatch). Undocumented. |

---

### A79-16 [LOW] — RoleDAO: No class-level Javadoc
**File:** RoleDAO.java, line 15
**Detail:** The `RoleDAO` class has no `/** ... */` Javadoc comment. Its single responsibility (fetching all non-admin roles from the `roles` table) is nowhere described.

---

### A79-17 [MEDIUM] — RoleDAO.getRoles: Undocumented non-trivial public method
**File:** RoleDAO.java, line 19
**Signature:** `public ArrayList<RoleBean> getRoles() throws Exception`
**Detail:** No Javadoc. The method silently filters out the `'CIIFM Admin'` role from results. This is a significant and non-obvious access-control decision that callers need to know about (e.g. a caller assuming all roles are returned would have a security gap if admin-role handling is ever needed). The filter and the sort order (`order by name`) are undocumented.

---

### A79-18 [MEDIUM] — QuestionDAO.getMaxQuestionId: Inaccurate method name
**File:** QuestionDAO.java, line 555
**Detail:** The method is named `getMaxQuestionId` but queries `max(order_no)`, not `max(id)`. The return type is `int`. A developer reading the method name would expect the maximum primary-key value of the `question` table, not the maximum ordering index. This naming inaccuracy creates a risk of misuse. Severity is MEDIUM (inaccurate rather than dangerously wrong in most usage contexts, since callers in context likely use it for `order_no` assignment).

---

### A79-19 [MEDIUM] — Systematic log message copy-paste errors across QuestionDAO
**File:** QuestionDAO.java
**Detail:** Multiple methods contain log messages that identify the wrong class or method name, copied from `LoginDAO` and from other methods:

| Method | Line | Erroneous log string |
|---|---|---|
| `getQuesLanId` | 35 | `"Inside LoginDAO Method : getQuesLanId"` |
| `getQuestionByUnitId` | 69 | `"Inside LoginDAO Method : getQuestionByUnitId"` |
| `delQuestionById` | 177 | `"Inside LoginDAO Method : delQuestionById"` |
| `getQuestionById` | 267 | `"Inside LoginDAO Method : getQuestionById"` |
| `getQuestionContentById` | 316 | `"Inside LoginDAO Method : getQuestionById"` (wrong method name too) |
| `saveQuestionInfo` | 369 | `"Inside LoginDAO Method : saveQuestionInfo"` |
| `saveQuestionContent` | 443 | `"Inside LoginDAO Method : saveQuestionContent"` |
| `updateQuestionInfo` | 521 | `"Inside LoginDAO Method : updateQuestionInfo"` |
| `getMaxQuestionId` | 560 | `"Inside LoginDAO Method : getMaxQuestionId"` |
| `getAllAnswerType` | 600 | `"Inside LoginDAO Method : getQuestionByUnitId"` (wrong class AND wrong method) |

While these are runtime log strings and not Javadoc, they constitute inaccurate inline documentation that will mislead anyone reading logs or the source. Severity MEDIUM.

---

## 3. Summary Table

| ID | File | Element | Severity | Category |
|---|---|---|---|---|
| A79-1 | QuestionDAO.java | Class `QuestionDAO` | LOW | No class-level Javadoc |
| A79-2 | QuestionDAO.java | `getQuesLanId` | MEDIUM | Undocumented non-trivial public method |
| A79-3 | QuestionDAO.java | `getQuestionByUnitId` | MEDIUM | Undocumented non-trivial public method |
| A79-4 | QuestionDAO.java | `getQuestionByCategory` | MEDIUM | Undocumented non-trivial public method |
| A79-5 | QuestionDAO.java | `delQuestionById` | MEDIUM | Undocumented non-trivial public method |
| A79-6 | QuestionDAO.java | `hideQuestionById` | MEDIUM | Undocumented non-trivial public method |
| A79-7 | QuestionDAO.java | `showQuestionById` | MEDIUM | Undocumented non-trivial public method |
| A79-8 | QuestionDAO.java | `getQuestionById` | MEDIUM | Undocumented non-trivial public method |
| A79-9 | QuestionDAO.java | `getQuestionContentById` | MEDIUM | Undocumented non-trivial public method |
| A79-10 | QuestionDAO.java | `saveQuestionInfo` | MEDIUM | Undocumented non-trivial public method |
| A79-11 | QuestionDAO.java | `saveQuestionContent` | MEDIUM | Undocumented non-trivial public method |
| A79-12 | QuestionDAO.java | `updateQuestionInfo` | MEDIUM | Undocumented non-trivial public method |
| A79-13 | QuestionDAO.java | `getMaxQuestionId` | MEDIUM | Undocumented non-trivial public method |
| A79-14 | QuestionDAO.java | `getAllAnswerType` | MEDIUM | Undocumented non-trivial public method |
| A79-15 | ResultDAO.java | Class + all 8 public methods | LOW + MEDIUM | No class-level Javadoc; all methods undocumented |
| A79-16 | RoleDAO.java | Class `RoleDAO` | LOW | No class-level Javadoc |
| A79-17 | RoleDAO.java | `getRoles` | MEDIUM | Undocumented non-trivial public method |
| A79-18 | QuestionDAO.java | `getMaxQuestionId` | MEDIUM | Inaccurate method name vs. implementation |
| A79-19 | QuestionDAO.java | 10 log strings | MEDIUM | Inaccurate inline documentation (wrong class/method names) |

**Totals:** 3 LOW, 16 MEDIUM, 0 HIGH
