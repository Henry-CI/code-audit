# Security Audit Report
## Files: QuestionDAO.java / QuestionBean.java / QuestionContentBean.java
**Date:** 2026-02-26
**Auditor:** Automated Pass 1
**Branch:** master
**Application:** forkliftiqadmin (Apache Struts 1.3.10 / Tomcat)

---

## Scope

- `/src/main/java/com/dao/QuestionDAO.java`
- `/src/main/java/com/bean/QuestionBean.java`
- `/src/main/java/com/bean/QuestionContentBean.java`

Supporting context files reviewed:
- `com/util/DBUtil.java` — confirms the dangerous `queryForObject(String, ResultMapper)` two-arg overload (line 128) accepts a pre-built SQL string with no bind step.
- `com/action/FleetcheckAction.java`, `AdminFleetcheckDeleteAction.java`, `AdminFleetcheckShowAction.java`, `AdminFleetcheckHideAction.java`, `AdminFleetcheckEditAction.java`, `GetAjaxAction.java`, `FormBuilderAction.java` — caller chains for all DAO methods.
- Relevant ActionForm classes — confirm which fields are raw HTTP parameters with no type enforcement beyond non-empty checks.

---

## Findings

---

### CRITICAL: SQL Injection in `delQuestionById` — unauthenticated delete of any question row

**File:** `QuestionDAO.java` (line 183)

**Description:**
`delQuestionById` constructs a `DELETE` statement using a `java.sql.Statement` with direct string concatenation of the caller-supplied `id` parameter. No parameterisation, no integer cast, no whitelist check.

```java
// QuestionDAO.java line 182-185
String sql = "delete from question where id=" + id;
log.info(sql);
stmt.executeUpdate(sql);
```

The direct caller is `AdminFleetcheckDeleteAction.execute()` which reads `id` straight from the Struts action form (itself populated from the HTTP request parameter `id`):

```java
// AdminFleetcheckDeleteAction.java line 20
QuestionDAO.delQuestionById(adminFleetcheckDeleteActionForm.getId());
```

`AdminFleetcheckDeleteActionForm` extends `ValidateIdExistsAbstractActionForm`, whose sole validation is a non-empty check (`StringUtils.isEmpty`). Any non-empty string passes. There is no integer validation, no ownership check, and no `comp_id` filter in the DELETE statement.

A payload such as `id=1 OR 1=1` deletes the entire `question` table. A UNION/subquery payload can exfiltrate data via error channels depending on the database driver's error messages. A stacked-query payload (if the driver allows it) can execute arbitrary DDL.

Additionally the WHERE clause contains no `comp_id` predicate, so even if the `id` were a valid integer a tenant could delete any other tenant's questions.

**Risk:** Complete data destruction (all question rows deleted with `OR 1=1`), cross-tenant data tampering, potential arbitrary SQL execution. Because `AdminFleetcheckDeleteAction` returns `null` rather than checking the session guard return value, and `PreFlightActionServlet` only checks `sessCompId != null`, any authenticated tenant can reach this endpoint.

**Recommendation:** Replace `Statement` with a `PreparedStatement` using a `?` placeholder and `ps.setInt(1, Integer.parseInt(id))` (wrapping the parseInt in a try/catch to reject non-integers). Add `AND comp_id = ?` bound to the session `sessCompId` value and pass it through the action.

---

### CRITICAL: SQL Injection in `getQuestionById` — used as a read primitive by `FleetcheckAction`, `AdminFleetcheckEditAction`, and `FormBuilderAction`

**File:** `QuestionDAO.java` (line 275)

**Description:**
`getQuestionById` uses `java.sql.Statement` and concatenates the `id` parameter directly:

```java
// QuestionDAO.java line 275
String sql = "select id,content,expectedanswer,order_no,type_id,manu_id,fule_type_id," +
             "attachment_id,answer_type,comp_id, active from question where id = " + id;
```

This method has three distinct call sites, each with a different taint source:

1. **`FleetcheckAction` (line 59):** `qId` comes from `request.getParameter("qId")` — a raw HTTP query-string parameter with no validation whatsoever. It is passed directly to `getQuestionById`. This is the most dangerous call site: the user is authenticated (sessCompId check) but the `qId` is fully attacker-controlled.

2. **`AdminFleetcheckEditAction` (line 40):** `id` from the action form, which again has only a non-empty check.

3. **`FormBuilderAction` (line 54):** `qid` from `request.getParameter("qid")` — again raw with no validation.

In call site 1, the injection happens before any use of the result, meaning the payload executes regardless of whether `arrQues.get(0)` raises an index exception. There is also no `comp_id` filter, so a valid integer `id` belonging to a different tenant is returned without restriction (see IDOR finding below).

**Risk:** Data exfiltration from any table reachable via UNION injection; time-based blind injection for out-of-band data extraction; cross-tenant question content disclosure.

**Recommendation:** Parameterise with `PreparedStatement`. Add `AND comp_id = ?` bound to session `sessCompId`, or for truly global/shared questions, validate that the returned bean's `comp_id` equals `sessCompId` before use.

---

### CRITICAL: SQL Injection in `getQuestionByUnitId` — four injected parameters including `unitId`, `lanId`, `compId`, and `attchId`

**File:** `QuestionDAO.java` (lines 82–89)

**Description:**
`getQuestionByUnitId` builds its query using `java.sql.Statement` and interpolates four distinct tainted values:

```java
// QuestionDAO.java lines 82-89
String sql = "select question.id,question.content,expectedanswer,order_no,answer_type," +
    "question_content.content from question" +
    " left outer join question_content on question_content.question_id = question.id" +
    " and lan_id = " + lanId +                          // tainted: result of getQuesLanId(compId)
    " left outer join unit on unit.type_id = question.type_id" +
    " where unit.id = " + unitId +                      // tainted: direct HTTP parameter
    " and unit.fuel_type_id = question.fule_type_id" +
    " and unit.manu_id = question.manu_id" +
    " and (question.comp_id is null or question.comp_id = " + compId + ")";  // tainted

if (attchId.equalsIgnoreCase("0")) {
    sql += " and attachment_id is null ";
} else {
    sql += " and (attachment_id is null or attachment_id = " + attchId + ")";  // tainted
}
```

Call sites:
- `FleetcheckAction` line 78: `veh_id` and `att_id` both come from `FleetcheckActionForm` which is directly populated from HTTP form fields with no integer validation. `sessCompId` is from the session (trusted), but it is still injected via concatenation.
- `SearchAction` line 47: `searchActionForm.getVeh_id()` and `searchActionForm.getAttachment()` — both HTTP-sourced with no integer check.
- `RegisterAction` line 69: same pattern.
- `PrintAction` line 47: same pattern.
- `ResultDAO` line 213: calls with `unitId` from a DAO context; taint depends on the calling chain but the pattern is still concatenation.

Even though `sessCompId` is session-managed, because it is still concatenated into the SQL string a secondary injection point exists if any code path permits a non-integer `sessCompId` (e.g., session fixation or administrative session manipulation).

The `lanId` value is the return value of `getQuesLanId(compId)` — itself vulnerable (see below) — but since `lanId` is an `int` type returned from `rs.getInt(1)`, it provides accidental numeric safety for that slot alone. The other three injection points (`unitId`, `compId`, `attchId`) are injected as raw strings.

**Risk:** Full SQL injection exploitable by any authenticated user via `veh_id` or `att_id` form fields. Combined with the multi-tenant architecture, this allows reading question records across all companies.

**Recommendation:** Replace all four concatenations with `PreparedStatement` bind parameters.

---

### CRITICAL: SQL Injection in `getQuesLanId` — `compId` concatenated directly; called from `getQuestionByUnitId` with a partially-tainted argument

**File:** `QuestionDAO.java` (line 42)

**Description:**
`getQuesLanId` is a `Statement`-based query with direct concatenation:

```java
// QuestionDAO.java line 42
String sql = "select lan_id from company where id = " + compId;
```

When called from `getQuestionByUnitId` at line 80, `compId` is either the session value (trusted) or — when `compId.equalsIgnoreCase("")` is true (line 76) — it is replaced by the value from `unitDao.getUnitById(unitId).get(0).getComp_id()`. In that branch, `unitId` is HTTP-sourced and itself injectable (see prior finding). If the `getUnitById` query is also injectable, an attacker can control `compId` via a second-order injection path. Even if `getUnitById` is safe, the direct `compId` parameter path in `getQuesLanId` itself is still injectable when called directly from `ResultDAO`.

**Risk:** Data exfiltration from the `company` table (which likely contains tenant email, configuration, and potentially credential data); second-order injection when compId is derived from an injectable unitId lookup.

**Recommendation:** Use `PreparedStatement` with `ps.setLong(1, Long.parseLong(compId))`.

---

### CRITICAL: SQL Injection in `getQuestionContentById` — `qId` and `lanId` both concatenated; `qId` sourced directly from HTTP parameter in `GetAjaxAction`

**File:** `QuestionDAO.java` (lines 328–331)

**Description:**
Both branches of the language check concatenate user input directly:

```java
// QuestionDAO.java lines 328-331
if (lanId.equalsIgnoreCase("1")) {
    sql = "select content from question where id = " + qId;
} else {
    sql = "select content from question_content where question_id = " + qId
          + " and lan_id = " + lanId;
}
```

The caller is `GetAjaxAction` (line 40-43):

```java
// GetAjaxAction.java lines 40-43
String qus_id = request.getParameter("qus_id") == null ? "0" : request.getParameter("qus_id");
String lan_id  = request.getParameter("lan_id")  == null ? "0" : request.getParameter("lan_id");
QuestionDAO questionDAO = new QuestionDAO();
arrXml = questionDAO.getQuestionContentById(qus_id, lan_id);
```

Both `qus_id` and `lan_id` are taken verbatim from HTTP request parameters with no validation. No `comp_id` filter exists in either branch; an attacker can retrieve question content from any company by supplying arbitrary `qId` values, or extract arbitrary data via UNION injection.

`GetAjaxAction` does not appear to enforce any additional session attribute checks beyond the `PreFlightActionServlet` gate (`sessCompId != null`).

**Risk:** Cross-tenant question content disclosure. Blind and UNION-based injection into both `question` and `question_content` tables. Because these are SELECT statements the immediate impact is data exfiltration, not modification.

**Recommendation:** Use `PreparedStatement`. Add `AND comp_id = (SELECT comp_id FROM company WHERE id = ?)` or equivalent tenant scoping.

---

### HIGH: IDOR — `getQuestionById` has no `comp_id` filter; any authenticated tenant can read any question by ID

**File:** `QuestionDAO.java` (line 275)

**Description:**
The SELECT in `getQuestionById` retrieves a question row based solely on its primary key with no tenant scope:

```java
String sql = "select id,content,expectedanswer,order_no,type_id,manu_id,fule_type_id," +
             "attachment_id,answer_type,comp_id, active from question where id = " + id;
```

Even if the SQL injection vulnerability were fixed (i.e., the `id` were bound via a PreparedStatement), a tenant could still supply any integer `id` to retrieve another tenant's proprietary question records. The `comp_id` column is fetched in the result set but never compared to `sessCompId` before the data is returned and used.

Call sites in `AdminFleetcheckEditAction` (line 40) and `FormBuilderAction` (line 54) expose this data directly to the response.

**Risk:** Cross-tenant information disclosure. A malicious tenant can enumerate all question IDs and read proprietary checklist questions belonging to competitors.

**Recommendation:** Add `AND (comp_id = ? OR comp_id IS NULL)` with the session `sessCompId` bound as a parameter, or validate `bean.getComp_id().equals(sessCompId)` immediately after the fetch and reject mismatches.

---

### HIGH: IDOR — `delQuestionById` has no `comp_id` filter; any authenticated tenant can delete any question

**File:** `QuestionDAO.java` (line 183)

**Description:**
The DELETE statement contains no tenant ownership check:

```java
String sql = "delete from question where id=" + id;
```

Even if parameterised, the absence of `AND comp_id = ?` means any authenticated user can delete questions owned by other tenants. This is compounded by the SQL injection vulnerability documented above, but it is a standalone IDOR even with a valid integer `id`.

**Risk:** Cross-tenant data destruction. A tenant can silently erase another tenant's checklist questions, corrupting their inspection workflows.

**Recommendation:** Add `AND comp_id = ?` bound to session `sessCompId`. The action layer must retrieve `sessCompId` from the session and pass it through to the DAO.

---

### HIGH: IDOR — `showQuestionById` and `hideQuestionById` operate on questions without verifying tenant ownership

**File:** `QuestionDAO.java` (lines 197–213); `AdminFleetcheckShowAction.java` (line 20); `AdminFleetcheckHideAction.java` (line 33)

**Description:**
Both `showQuestionById` and `hideQuestionById` call `getQuestionById(id)` — which has no `comp_id` filter — and then call `updateQuestionInfo` on the resulting bean. The hide flow also calls `copyQuestionToCompId` which writes the attacker's `sessCompId` as `comp_id` into the new row, creating a cross-tenant ownership transfer.

```java
// QuestionDAO.java lines 197-208
public static void hideQuestionById(String id, ..., String compId, ...) throws Exception {
    QuestionBean question = QuestionDAO.getQuestionById(id).get(0);  // no tenant filter
    if (question.getComp_id() == null && question.getCopied_from_id() == null) {
        QuestionBean newQuestion = QuestionDAO.copyQuestionToCompId(id, manuId, typeId,
                                      fuleTypeId, attchId, compId);  // compId is sessCompId
        QuestionDAO.updateQuestionInfo(newQuestion);
    } else if (question.getComp_id() != null) {
        question.setActive("f");
        QuestionDAO.updateQuestionInfo(question);  // modifies another tenant's question
    }
}
```

`AdminFleetcheckShowAction` does not retrieve `sessCompId` at all before calling `showQuestionById`; it passes only `id` from the form:

```java
// AdminFleetcheckShowAction.java line 20
QuestionDAO.showQuestionById(adminFleetcheckActionForm.getId());
```

`showQuestionById` calls `updateQuestionInfo` which sets `active = 't'` with no tenant check in the UPDATE WHERE clause either (see `updateQuestionInfo` finding below).

**Risk:** Cross-tenant data manipulation. Attacker can toggle the active/visible state of another tenant's questions, disrupting their inspection checklist. The `hideQuestionById` path can additionally duplicate another tenant's global question into the attacker's tenant scope.

**Recommendation:** Pass `sessCompId` through both actions to the DAO. In `getQuestionById`, add a `comp_id` filter. In `updateQuestionInfo`, add `AND comp_id = ?` to the WHERE clause.

---

### HIGH: IDOR — `updateQuestionInfo` WHERE clause contains no `comp_id` predicate

**File:** `QuestionDAO.java` (lines 527–540)

**Description:**
The UPDATE statement filters only on `id`:

```java
// QuestionDAO.java lines 527-536
String sql = "update question set content = ?, expectedanswer = ?, answer_type = ?, active = ?" +
             " where id = ?";
ps = conn.prepareStatement(sql);
ps.setString(1, questionBean.getContent());
ps.setString(2, questionBean.getExpectedanswer());
ps.setInt(3, Integer.parseInt(questionBean.getAnswer_type()));
ps.setBoolean(4, questionBean.getActive().equalsIgnoreCase("t"));
ps.setInt(5, Integer.parseInt(questionBean.getId()));
```

While this method correctly uses `PreparedStatement` (no SQL injection), the absence of `AND comp_id = ?` means it can be weaponised through the `hideQuestionById` / `showQuestionById` call chains to update any question in the database, regardless of tenant.

**Risk:** Cross-tenant data modification (content, expected answers, active status) for any question whose integer ID is known or guessed.

**Recommendation:** Add `AND comp_id = ?` with `ps.setInt(...)` bound to the `comp_id` from the session or from the `QuestionBean` after validating it against the session.

---

### HIGH: SQL Injection in `getQuestionContentById` enables access to question data with no tenant scoping (reinforcement of CRITICAL finding)

**File:** `QuestionDAO.java` (lines 328–331)

**Description:**
This finding amplifies the CRITICAL injection finding above with an explicit IDOR dimension. Even with numeric-only `qId`, there is no `comp_id` column in either query branch:

```java
sql = "select content from question where id = " + qId;
// OR
sql = "select content from question_content where question_id = " + qId + " and lan_id = " + lanId;
```

Neither query restricts the returned content to the authenticated tenant's questions.

**Risk:** Any authenticated user can enumerate question content across all tenants by iterating integer `qId` values.

**Recommendation:** Add a sub-query or join to enforce `comp_id` scoping.

---

### MEDIUM: Exception swallowing in `DBUtil.queryForObjects` and `DBUtil.queryForObject` — SQL errors silently suppressed, callers receive empty results

**File:** `DBUtil.java` (lines 75–77, 140–142)

**Description:**
The two-argument `queryForObject(String, ResultMapper)` overload (line 128) and all `queryForObjects` variants catch `SQLException` and call only `e.printStackTrace()` without rethrowing:

```java
// DBUtil.java lines 140-142
} catch (SQLException e) {
    e.printStackTrace();
}
```

`getQuestionByCategory` at `QuestionDAO.java` line 151 calls `DBUtil.queryForObjects` and relies on the returned list. If a SQL error occurs (including an injection attempt that causes a parse error), the method silently returns an empty list. The callers (`AdminFleetcheckAction`, `AdminFleetcheckEditAction`) do not distinguish between "no questions exist" and "the query failed." A security decision — whether to show the question list — is therefore made on a failed query result.

This also means that injection payloads that cause syntax errors produce no visible exception to the caller, making error-based injection attempts harder to detect in logs (the stack trace goes only to stdout/stderr, not to the application log).

**Risk:** Silent query failures allow the application to continue in an undefined state. An attacker probing injection points receives no explicit error signal from the application layer, reducing the difficulty of blind injection. Security-relevant decisions (e.g., "is this question visible to this tenant?") are made based on potentially corrupt empty results.

**Recommendation:** Rethrow `SQLException` in all `DBUtil` catch blocks, or at minimum log at ERROR level via the InfoLogger framework and propagate a typed exception so callers can distinguish failure from empty results.

---

### MEDIUM: SQL logged before execution — full injection payload written to application log

**File:** `QuestionDAO.java` (lines 43, 96, 184, 275, 329–330)

**Description:**
Multiple methods call `log.info(sql)` with the fully-assembled SQL string (including any injected payload) immediately before or after execution:

```java
// Examples:
log.info(sql);  // QuestionDAO.java line 43 — getQuesLanId
log.info(sql);  // QuestionDAO.java line 96 — getQuestionByUnitId
log.info(sql);  // QuestionDAO.java line 184 — delQuestionById
log.info(sql);  // QuestionDAO.java line 275 — getQuestionById
```

If an attacker is probing for SQL injection, the exact SQL sent to the database (including their payload) is written to the log file. If logs are accessible (e.g., through a log viewer, a path traversal vulnerability, or exposed admin interface), this reveals both the injection surface and the database schema to the attacker.

Conversely, if logs are only available to defenders, this aids forensics — but the primary concern is schema disclosure if logs are exposed.

**Risk:** Database schema disclosure if logs are accessible. Confirmation of injection success/failure patterns through log content if the attacker can read logs.

**Recommendation:** Log only the parameterised SQL template (not the assembled string), or log the template and bind-parameter values separately at DEBUG level. Never log user-supplied data at INFO level.

---

### MEDIUM: `saveQuestionContent` — no tenant ownership check before updating question content

**File:** `QuestionDAO.java` (lines 453–489)

**Description:**
`saveQuestionContent` accepts a `QuestionContentBean` and updates `question` or `question_content` rows filtered only by `question_id` (and optionally `lan_id`). No `comp_id` check is performed on the target row:

```java
// QuestionDAO.java lines 453-457
sql = "update question set content =? where id =?";
ps = conn.prepareStatement(sql);
ps.setString(1, qeustionContentBean.getContent());
ps.setInt(2, Integer.parseInt(qeustionContentBean.getQuestion_id()));
```

The caller `AdminFleetcheckEditAction.update()` (line 89) passes `questionContentBean.question_id` which is the `bean.getId()` value from the request. While `sessCompId` is used for other purposes in that action, it is not passed to `saveQuestionContent` and is not checked in the DAO.

**Risk:** Cross-tenant content modification. An authenticated user can overwrite the content of another tenant's question by supplying a foreign `question_id`.

**Recommendation:** Add a WHERE clause condition `AND comp_id = ?` or verify ownership with a preliminary SELECT before the UPDATE.

---

### LOW: `QuestionBean` — Lombok `@Data` generates `toString()` that includes all fields, including `comp_id` and `copied_from_id`; `Serializable` with no `transient` fields

**File:** `QuestionBean.java` (lines 10–46)

**Description:**
`@Data` generates `toString()`, `equals()`, `hashCode()`, and all getters/setters. The generated `toString()` will emit all fields including `comp_id` (tenant identifier), `copied_from_id` (internal question lineage), `expectedanswer`, and `active`. If `QuestionBean` instances are ever logged (e.g., `log.info(questionBean)` elsewhere in the codebase) or serialised to a session store, all of these values are exposed.

```java
@Data
@NoArgsConstructor
public class QuestionBean implements Serializable {
    private String comp_id = null;        // tenant identifier — in toString()
    private String copied_from_id = null; // internal lineage — in toString()
    private String expectedanswer = null; // checklist answer key — in toString()
    private String active = null;         // visibility flag — in toString()
    // ... all other fields
}
```

`QuestionBean` implements `Serializable`. All fields are non-transient. If the class is stored in an HTTP session (which is serialised to disk/database in clustered Tomcat deployments), the full bean graph including `comp_id` is persisted. If session storage is compromised, complete question metadata is exposed.

No fields are particularly credential-sensitive (no passwords or tokens), but `comp_id` is a multi-tenancy boundary identifier and `expectedanswer` is an inspection audit key.

**Risk:** Information disclosure via logging or serialised session storage. Low severity because there are no password/secret fields, but `comp_id` leakage from logs could assist tenant enumeration attacks.

**Recommendation:** Annotate `comp_id`, `copied_from_id`, and `expectedanswer` with `@ToString.Exclude` (Lombok). Consider marking them `transient` if session serialisation is not required. If session storage is required, ensure the session store itself is encrypted at rest.

---

### LOW: `QuestionContentBean` — `@Builder` annotation without `@NoArgsConstructor` breaks Struts ActionForm compatibility; missing `toString()` control

**File:** `QuestionContentBean.java` (lines 9–19)

**Description:**
`QuestionContentBean` uses `@Builder` but not `@Data` or `@NoArgsConstructor`. The Lombok `@Builder` generates an all-args constructor and suppresses the no-arg constructor. This means Struts 1.x's `BeanUtils.populate()` — which requires a no-arg constructor — cannot instantiate the bean directly from an HTTP request if it were used as an ActionForm or in BeanUtils-based population. The class is currently only used as a DAO transfer object built explicitly in `AdminFleetcheckEditAction`, so this is not an active runtime defect, but it creates a future-use trap.

No `toString()` is generated (no `@Data` or `@ToString`), which is actually the safer choice — accidental logging of the bean will call `Object.toString()` and only expose the class name and hash.

`language_id` is exposed via `@Getter`/`@Setter` and is non-transient in the `Serializable` class. There are no sensitive fields here.

**Risk:** Low — no current runtime defect, but the missing no-arg constructor is a latent bug if the bean is ever used outside of the builder pattern. No security-sensitive fields are exposed.

**Recommendation:** Add `@NoArgsConstructor` if the bean may be used in any reflective population context. This finding is informational from a security perspective.

---

### INFO: `getQuestionByCategory` — correctly uses `PreparedStatement` with full parameterisation and `comp_id` scoping

**File:** `QuestionDAO.java` (lines 128–172)

**Description:**
This method is a positive example within the file. It uses `DBUtil.queryForObjects(String, PreparedStatementHandler, ResultMapper)` — the three-argument safe overload — and binds all parameters via `stmt.setLong(...)`. The WHERE clause includes `comp_id = ?` for tenant scoping. Parameters are validated as non-empty before use and parsed to `long` to enforce integer type.

```java
// QuestionDAO.java lines 151-171
return DBUtil.queryForObjects(query, stmt -> {
    int index = 0;
    for(int i = 0; i < 2; i++) {
        stmt.setLong(++index, Long.parseLong(manuId));
        stmt.setLong(++index, Long.parseLong(typeId));
        stmt.setLong(++index, Long.parseLong(fuelTypeId));
        stmt.setLong(++index, Long.parseLong(compId));
        if (StringUtils.isNotBlank(attchId)) {
            stmt.setLong(++index, Long.parseLong(attchId));
        }
    }
}, rs -> QuestionBean.builder()...build());
```

Note: This method still relies on `DBUtil.queryForObjects` which swallows `SQLException` silently (see MEDIUM finding).

**Risk:** None from SQL injection or IDOR for this specific method. The exception-swallowing issue in DBUtil still applies.

**Recommendation:** No changes needed for the SQL construction itself. Address the DBUtil exception swallowing.

---

### INFO: `saveQuestionInfo`, `copyQuestionToCompId`, `getMaxQuestionId` — correctly use `PreparedStatement`

**File:** `QuestionDAO.java` (lines 363–433, 216–261, 555–593)

**Description:**
These three methods use `PreparedStatement` with proper bind parameters for all user-supplied values. `saveQuestionInfo` binds `compId` from the `int` method parameter (not a String concatenation). `copyQuestionToCompId` correctly uses `ps.setNull()` for optional attachment IDs. `getMaxQuestionId` uses a PreparedStatement for all four category parameters.

**Risk:** None from SQL injection for these methods individually. IDOR concerns still apply at the business logic layer (e.g., `saveQuestionInfo` trusts the `compId` passed by the caller, which in `AdminFleetcheckEditAction` is `Integer.parseInt(bean.getComp_id())` where `comp_id` was set to `sessCompId` — this is correct).

**Recommendation:** No changes needed for the SQL construction in these methods.

---

## Summary Table

| Method | SQL Injection | IDOR | Notes |
|---|---|---|---|
| `getQuesLanId` | CRITICAL (Statement + concat) | Partial | compId concatenated |
| `getQuestionByUnitId` | CRITICAL (Statement + 4 concat) | Yes — no exclusive comp_id | unitId, attchId, compId all injectable |
| `getQuestionByCategory` | None — PreparedStatement | No — comp_id scoped | Safe pattern |
| `delQuestionById` | CRITICAL (Statement + concat) | CRITICAL — no comp_id filter | Delete any row |
| `hideQuestionById` | Indirect via getQuestionById | HIGH — no ownership check | Delegates to injectable method |
| `showQuestionById` | Indirect via getQuestionById | HIGH — no ownership check | Delegates to injectable method |
| `copyQuestionToCompId` | None — PreparedStatement | Low — compId from session | Safe SQL |
| `getQuestionById` | CRITICAL (Statement + concat) | HIGH — no comp_id filter | 3 injectable call sites |
| `getQuestionContentById` | CRITICAL (Statement + 2 concat) | HIGH — no comp_id filter | Both branches injectable |
| `saveQuestionInfo` | None — PreparedStatement | Acceptable | compId from int param |
| `saveQuestionContent` | None — PreparedStatement | MEDIUM — no ownership check | question_id unchecked |
| `updateQuestionInfo` | None — PreparedStatement | HIGH — no comp_id in WHERE | Updates any question |
| `getMaxQuestionId` | None — PreparedStatement | Acceptable | Safe pattern |
| `getAllAnswerType` | None — static query, no user input | N/A | Safe |

---

## Totals

**CRITICAL: 5 / HIGH: 6 / MEDIUM: 3 / LOW: 2 / INFO: 2**
