# Pass 2 — Test Coverage Audit
**Audit Run:** 2026-02-26-01
**Agent ID:** A80
**Source Files Audited:**
1. `src/main/java/com/dao/SubscriptionDAO.java`
2. `src/main/java/com/dao/TimezoneDAO.java`
3. `src/main/java/com/dao/TrainingDAO.java`

**Test Directory:** `src/test/java/`

---

## Reading Evidence

### 1. SubscriptionDAO

**Class name:** `SubscriptionDAO`
**Package:** `com.dao`

**Fields:**
| Field | Line |
|---|---|
| `private static Logger log` | 22 |

**Methods:**
| Method | Line |
|---|---|
| `public ArrayList<SubscriptionBean> getAllReport(ArrayList<String> frequencies)` | 24 |
| `public String checkCompFleetAlert(String comId)` | 87 |
| `public boolean saveDefualtSubscription(int compId)` | 122 |
| `public static SubscriptionBean getSubscriptionByName(final String name)` | 154 |

**Test grep result for `SubscriptionDAO`:** No matches found in test directory.

---

### 2. TimezoneDAO

**Class name:** `TimezoneDAO`
**Package:** `com.dao`

**Fields:**
| Field | Line |
|---|---|
| `private static Logger log` | 17 |
| `private static TimezoneDAO theInstance` | 19 |

**Methods:**
| Method | Line |
|---|---|
| `public static TimezoneDAO getInstance()` | 21 |
| `private TimezoneDAO()` (constructor) | 33 |
| `public ArrayList<TimezoneBean> getAllTimezone()` | 37 |
| `public static List<TimezoneBean> getAll()` | 78 |
| `public static TimezoneBean getTimezone(int tzoneId)` | 119 |

**Test grep result for `TimezoneDAO`:** No matches found in test directory.

---

### 3. TrainingDAO

**Class name:** `TrainingDAO`
**Package:** `com.dao`

**Fields:**
| Field | Line |
|---|---|
| `private static Logger log` | 21 |

**Methods:**
| Method | Line |
|---|---|
| `public List<DriverTrainingBean> getTrainingByDriver(Long driverId, String dateFormat)` | 23 |
| `public void addTraining(DriverTrainingBean trainingBean, String dateFormat)` | 55 |
| `public void deleteTraining(Long trainingId)` | 70 |
| `public void sendTrainingExpiryDailyEmail()` | 76 |
| `public void sendTrainingExpiryWeeklyEmail()` | 119 |

**Test grep result for `TrainingDAO`:** No matches found in test directory.

---

## Findings

### SubscriptionDAO

**A80-1 | Severity: CRITICAL | SubscriptionDAO has zero test coverage — no test class exists**
No test file references `SubscriptionDAO` anywhere in `src/test/java/`. All four methods are completely untested. This is a data-access class performing SQL operations against a production database schema with no safety net.

**A80-2 | Severity: CRITICAL | `getAllReport` builds SQL by string concatenation — SQL injection, no test for injection path**
`getAllReport` (line 38-43) constructs the `WHERE` clause by iterating the `frequencies` list and appending raw string values: `extra += " frequency = '" + frequencies.get(i) + "' or"`. Any caller-supplied frequency string is embedded directly into SQL without parameterization. There is no test covering an injection payload in the frequency list, nor any test verifying that only safe values are accepted.

**A80-3 | Severity: CRITICAL | `checkCompFleetAlert` builds SQL by string concatenation — SQL injection, no test**
Line 99 embeds the `comId` parameter directly into the SQL string: `"... and c.comp_id ='" + comId + "'"`. No input sanitization or parameterized query is used. There is no test verifying behavior with a malicious `comId` value (e.g., `1' OR '1'='1`).

**A80-4 | Severity: HIGH | `getAllReport` — no test for empty `frequencies` list**
When `frequencies` is an empty list the `extra` string remains empty and the SQL executes without a frequency filter, potentially returning all report subscriptions. This edge case is untested.

**A80-5 | Severity: HIGH | `getAllReport` — no test for `null` `frequencies` argument**
The method signature accepts `ArrayList<String> frequencies` but performs no null check before iterating at line 38. A `null` argument causes a `NullPointerException` inside the try block, which is caught and re-thrown as a `SQLException`. This behavior is undocumented and untested.

**A80-6 | Severity: HIGH | `getAllReport` applies `LIMIT 1` — potentially wrong business behavior, no test**
The SQL query at line 51 includes `limit 1`, meaning only one subscription record is ever returned regardless of how many match. The method returns an `ArrayList` implying multiple results are expected. There is no test confirming this constraint is intentional rather than a defect.

**A80-7 | Severity: HIGH | `getSubscriptionByName` — no test for `null` name (NullArgumentException path)**
Line 155-157 throws `NullArgumentException` when `name == null`. Although this is the only explicit guard in the class, it is completely untested. There is also no test verifying the exception type, message, or that callers handle it correctly.

**A80-8 | Severity: HIGH | `getSubscriptionByName` — no test for not-found case (EntityNotFoundException)**
Lines 165-167 throw `EntityNotFoundException` when the query returns no result. This error path is untested. The exception is constructed with `DriverBean.class` as the entity type despite the method belonging to `SubscriptionDAO`, which is a semantic bug that also goes undetected without a test.

**A80-9 | Severity: HIGH | `getSubscriptionByName` — no test for found/happy-path**
No test verifies that a valid subscription name returns a correctly populated `SubscriptionBean` with the expected `id` field set.

**A80-10 | Severity: HIGH | `saveDefualtSubscription` — method uses `ResultSet.CONCUR_READ_ONLY` on a write statement**
Line 131 creates a statement with `ResultSet.TYPE_SCROLL_SENSITIVE, ResultSet.CONCUR_READ_ONLY`, but line 135 calls `stmt.execute(sql)` to perform an `INSERT`. The ResultSet concurrency flag is mismatched for a write operation. There is no test that would catch a driver-level rejection or unexpected behavior from this mismatch.

**A80-11 | Severity: HIGH | `saveDefualtSubscription` — always returns `true`, failure indicated only by exception**
The method signature returns `boolean` but the body can only return `true` (line 136) or throw. A caller checking the return value for `false` to detect failure will never observe it. No test verifies this contract.

**A80-12 | Severity: MEDIUM | `checkCompFleetAlert` — no test for company with no fleet alert subscription (returns `null`)**
When the query returns no rows, `name` remains `null` and is returned to the caller (line 119). No test verifies this null-return behavior or that callers handle it safely.

**A80-13 | Severity: MEDIUM | `checkCompFleetAlert` — no test for happy-path (fleet alert exists)**
No test verifies that the method returns the subscription name when a matching row exists.

**A80-14 | Severity: MEDIUM | No test for `DBUtil.getConnection()` failure in any SubscriptionDAO method**
All four methods acquire a database connection from `DBUtil.getConnection()`. No test exercises the path where `getConnection()` throws an exception, verifying that the finally block still executes and resources are not leaked.

**A80-15 | Severity: LOW | Misspelled method name `saveDefualtSubscription` — not caught without test**
The method is named `saveDefualtSubscription` (line 122) instead of `saveDefaultSubscription`. No test references it by name, so there is no automated signal that would surface this typo to a reviewer performing refactoring.

---

### TimezoneDAO

**A80-16 | Severity: CRITICAL | TimezoneDAO has zero test coverage — no test class exists**
No test file references `TimezoneDAO` anywhere in `src/test/java/`. All public methods are completely untested.

**A80-17 | Severity: HIGH | `getInstance()` singleton — no test for thread-safety behavior**
`getInstance()` (lines 21-31) uses double-checked locking. While the idiom is structurally correct, `theInstance` is not declared `volatile`, which means the double-checked locking pattern is broken under the Java Memory Model prior to Java 5 and may be unreliable in some JVM configurations. There is no test for concurrent access, race conditions, or verifying that exactly one instance is returned across multiple threads.

**A80-18 | Severity: HIGH | `theInstance` is not `volatile` — broken double-checked locking**
The static field `private static TimezoneDAO theInstance` (line 19) lacks the `volatile` keyword required for correct double-checked locking under the Java Memory Model (JMM). Without `volatile`, a second thread may observe a partially constructed `TimezoneDAO` object. The absence of tests means this defect has never been exercised under concurrency.

**A80-19 | Severity: HIGH | `getAllTimezone` and `getAll` are functionally identical — duplication untested**
`getAllTimezone()` (line 37) and `getAll()` (line 78) execute the exact same SQL (`select id,name,zone from timezone`), map the same columns to `TimezoneBean`, and share identical exception and cleanup logic. Neither method is tested, and no test would catch a future divergence or confirm that one is safe to delete.

**A80-20 | Severity: HIGH | `getTimezone` — no test for not-found case (returns empty bean)**
When `getTimezone(int tzoneId)` finds no matching row, it returns a `TimezoneBean` initialized with all-null fields (lines 127, 157) rather than throwing an exception or returning `null`/`Optional`. Callers receive a misleadingly non-null object. This behavior is untested.

**A80-21 | Severity: HIGH | `getTimezone` — SQL built by integer concatenation, no test for boundary values**
Line 133: `"select id,name,zone from timezone where id="+tzoneId`. While integer concatenation is less dangerous than string concatenation, there is no test for edge-case values such as `0`, `-1`, or `Integer.MIN_VALUE`.

**A80-22 | Severity: MEDIUM | `getAllTimezone` — no test for empty table (returns empty list)**
When the `timezone` table has no rows, the method returns an empty `ArrayList`. This is a valid result but is untested.

**A80-23 | Severity: MEDIUM | `getAll` log message is wrong — logs "getAllTimezone" instead of "getAll"**
Line 84 logs `"Inside TimezoneDAO Method : getAllTimezone"` inside `getAll()`. This copy-paste error produces misleading log output. There is no test that would assert on the method being invoked or catch this diagnostic discrepancy.

**A80-24 | Severity: MEDIUM | No test for `DBUtil.getConnection()` failure in any TimezoneDAO method**
All three query methods acquire a database connection with no test for the failure path or resource cleanup verification.

**A80-25 | Severity: LOW | `getInstance()` — no test confirming singleton contract (same reference returned)**
No test verifies that two successive calls to `getInstance()` return the identical object reference.

---

### TrainingDAO

**A80-26 | Severity: CRITICAL | TrainingDAO has zero test coverage — no test class exists**
No test file references `TrainingDAO` anywhere in `src/test/java/`. All five methods are completely untested.

**A80-27 | Severity: CRITICAL | `sendTrainingExpiryDailyEmail` silently swallows exceptions inside lambda**
Lines 106-115: the `forEach` lambda catches `SQLException`, `AddressException`, and `MessagingException` with only `e.printStackTrace()` — no re-throw, no logging via `InfoLogger`, no failure tracking. If email sending or a database call fails for one company, processing continues silently for all remaining companies and the caller receives no indication of partial failure. This behavior is completely untested.

**A80-28 | Severity: CRITICAL | `sendTrainingExpiryWeeklyEmail` silently swallows exceptions inside lambda**
Lines 158-167: identical silent swallowing pattern as `sendTrainingExpiryDailyEmail`. `SQLException`, `AddressException`, and `MessagingException` are all caught and discarded except for a stack trace print. This is untested.

**A80-29 | Severity: HIGH | `getTrainingByDriver` — no test for `null` driverId**
The method passes `driverId` directly to `stmt.setLong(1, driverId)` via unboxing. If `driverId` is `null`, a `NullPointerException` is thrown during unboxing. There is no null guard and no test for this path.

**A80-30 | Severity: HIGH | `getTrainingByDriver` — no test for driver with no training records (empty list)**
No test verifies the method returns an empty list when no `driver_training` rows match the given `driverId`.

**A80-31 | Severity: HIGH | `getTrainingByDriver` — no test for `null` or invalid `dateFormat`**
`DateUtil.sqlDateToString` is called with the caller-supplied `dateFormat` for both `training_date` and `expiration_date` (lines 50-51). No test exercises a null, empty, or malformed format string to verify exception propagation.

**A80-32 | Severity: HIGH | `addTraining` — no test for null `trainingBean` fields**
`addTraining` calls `trainingBean.getDriver_id()`, `getManufacture_id()`, `getType_id()`, `getFuel_type_id()`, `getTraining_date()`, and `getExpiration_date()` (lines 61-66). If any field is null or returns a type-incompatible value, the behavior is undefined. No test covers null or empty bean scenarios.

**A80-33 | Severity: HIGH | `addTraining` — no test for happy-path (record inserted)**
No test verifies that a valid `DriverTrainingBean` results in a successfully inserted row.

**A80-34 | Severity: HIGH | `deleteTraining` — no test for `null` trainingId**
`trainingId` is a `Long` (boxed). Passing `null` causes a `NullPointerException` during unboxing at `stmt.setLong(1, trainingId)`. There is no null guard and no test.

**A80-35 | Severity: HIGH | `deleteTraining` — no test for non-existent ID (silent no-op)**
Deleting a training record that does not exist produces no exception and no indication of zero rows affected. The caller cannot distinguish a successful delete from a no-op. This behavior is untested.

**A80-36 | Severity: HIGH | `sendTrainingExpiryDailyEmail` — timezone logic (`US/` or `Canada/` prefix) untested**
Lines 86-92 branch on whether `UserCompRelBean.getTimezone()` contains `"US/"` or `"Canada/"` to determine whether the content says "training" or "licence". No test covers either branch, nor the case where `getTimezone()` returns `null` (which would cause a `NullPointerException` on `String.contains()`).

**A80-37 | Severity: HIGH | `sendTrainingExpiryWeeklyEmail` — same timezone branch logic untested**
Lines 130-135: identical `US/`/`Canada/` timezone branching as the daily method, with the same untested null risk.

**A80-38 | Severity: HIGH | `sendTrainingExpiryWeeklyEmail` — null expiration date handling untested**
Lines 143-149 check `driverTrainingBean.getExpiration_date() == null` and substitute `"None"`. No test verifies this null substitution or that the `None` string appears correctly in the generated email content.

**A80-39 | Severity: MEDIUM | `sendTrainingExpiryDailyEmail` — no test when `getUserAlert` returns bean with null `alert_id`**
Line 82 calls `getAlert_id()` and checks for non-null. No test covers the case where `getUserAlert` returns a bean whose `alert_id` is null (the else/skip path is entirely untested), nor the case where `getUserAlert` itself throws.

**A80-40 | Severity: MEDIUM | `sendTrainingExpiryWeeklyEmail` — same `getUserAlert` null-check path untested**
Line 126: identical untested path as A80-39.

**A80-41 | Severity: MEDIUM | `sendTrainingExpiryDailyEmail` and `sendTrainingExpiryWeeklyEmail` — no test when `expiredCompLst` is empty**
When `DriverDAO.getInstance().getExpiredTrainigsComp()` or `getExpiringTrainigsComp()` returns an empty list, the `forEach` lambda never executes and no emails are sent. This is a valid and important path (no expiring drivers) that is untested.

**A80-42 | Severity: MEDIUM | TrainingDAO SQL query in `getTrainingByDriver` has a missing space before JOIN clause**
Line 35: `"FROM driver_training dt"` is immediately followed by `"    LEFT OUTER JOIN manufacture m ..."` without a newline or space separation. The resulting SQL is `"FROM driver_training dt    LEFT OUTER JOIN ..."`. While most SQL parsers tolerate multiple spaces, the concatenation is fragile. No test validates the generated SQL structure or query execution against a real or in-memory database.

**A80-43 | Severity: LOW | `sendTrainingExpiryDailyEmail` — `throws SQLException` declared but exceptions are swallowed internally**
The method declares `throws SQLException` in its signature (line 76) but all `SQLException`s are caught and swallowed inside the lambda (line 106). The declared checked exception can never propagate to the caller, making the declaration misleading. No test verifies actual exception propagation behavior.

**A80-44 | Severity: LOW | `sendTrainingExpiryWeeklyEmail` — same misleading `throws SQLException` declaration**
Same issue as A80-43 at line 119.

---

## Summary Table

| Finding | Severity | Class | Description |
|---|---|---|---|
| A80-1 | CRITICAL | SubscriptionDAO | Zero test coverage — no test class |
| A80-2 | CRITICAL | SubscriptionDAO | SQL injection via frequency list concatenation |
| A80-3 | CRITICAL | SubscriptionDAO | SQL injection via comId concatenation |
| A80-4 | HIGH | SubscriptionDAO | Empty frequencies list edge case untested |
| A80-5 | HIGH | SubscriptionDAO | Null frequencies argument causes NPE, untested |
| A80-6 | HIGH | SubscriptionDAO | LIMIT 1 on multi-row result, potentially wrong |
| A80-7 | HIGH | SubscriptionDAO | Null name guard (NullArgumentException) untested |
| A80-8 | HIGH | SubscriptionDAO | EntityNotFoundException path untested; wrong entity class used |
| A80-9 | HIGH | SubscriptionDAO | Happy-path for getSubscriptionByName untested |
| A80-10 | HIGH | SubscriptionDAO | CONCUR_READ_ONLY on INSERT statement |
| A80-11 | HIGH | SubscriptionDAO | saveDefualtSubscription always returns true |
| A80-12 | MEDIUM | SubscriptionDAO | checkCompFleetAlert null-return path untested |
| A80-13 | MEDIUM | SubscriptionDAO | checkCompFleetAlert happy-path untested |
| A80-14 | MEDIUM | SubscriptionDAO | DBUtil.getConnection() failure path untested |
| A80-15 | LOW | SubscriptionDAO | Misspelled method name saveDefualtSubscription |
| A80-16 | CRITICAL | TimezoneDAO | Zero test coverage — no test class |
| A80-17 | HIGH | TimezoneDAO | getInstance() thread-safety untested |
| A80-18 | HIGH | TimezoneDAO | theInstance not volatile — broken double-checked locking |
| A80-19 | HIGH | TimezoneDAO | getAllTimezone and getAll are identical — duplication untested |
| A80-20 | HIGH | TimezoneDAO | getTimezone returns empty bean for not-found, untested |
| A80-21 | HIGH | TimezoneDAO | getTimezone boundary values (0, -1) untested |
| A80-22 | MEDIUM | TimezoneDAO | getAllTimezone empty table path untested |
| A80-23 | MEDIUM | TimezoneDAO | getAll logs wrong method name "getAllTimezone" |
| A80-24 | MEDIUM | TimezoneDAO | DBUtil.getConnection() failure path untested |
| A80-25 | LOW | TimezoneDAO | getInstance singleton contract not verified by test |
| A80-26 | CRITICAL | TrainingDAO | Zero test coverage — no test class |
| A80-27 | CRITICAL | TrainingDAO | sendTrainingExpiryDailyEmail silently swallows exceptions |
| A80-28 | CRITICAL | TrainingDAO | sendTrainingExpiryWeeklyEmail silently swallows exceptions |
| A80-29 | HIGH | TrainingDAO | getTrainingByDriver null driverId causes NPE, untested |
| A80-30 | HIGH | TrainingDAO | getTrainingByDriver empty result set untested |
| A80-31 | HIGH | TrainingDAO | getTrainingByDriver null/invalid dateFormat untested |
| A80-32 | HIGH | TrainingDAO | addTraining null bean fields untested |
| A80-33 | HIGH | TrainingDAO | addTraining happy-path untested |
| A80-34 | HIGH | TrainingDAO | deleteTraining null trainingId causes NPE, untested |
| A80-35 | HIGH | TrainingDAO | deleteTraining non-existent ID silent no-op untested |
| A80-36 | HIGH | TrainingDAO | sendTrainingExpiryDailyEmail timezone branch untested |
| A80-37 | HIGH | TrainingDAO | sendTrainingExpiryWeeklyEmail timezone branch untested |
| A80-38 | HIGH | TrainingDAO | sendTrainingExpiryWeeklyEmail null expiration date untested |
| A80-39 | MEDIUM | TrainingDAO | sendTrainingExpiryDailyEmail getUserAlert null alert_id untested |
| A80-40 | MEDIUM | TrainingDAO | sendTrainingExpiryWeeklyEmail getUserAlert null alert_id untested |
| A80-41 | MEDIUM | TrainingDAO | Empty expiredCompLst path untested in both email methods |
| A80-42 | MEDIUM | TrainingDAO | Missing space in SQL JOIN concatenation, no query test |
| A80-43 | LOW | TrainingDAO | Misleading throws SQLException on sendTrainingExpiryDailyEmail |
| A80-44 | LOW | TrainingDAO | Misleading throws SQLException on sendTrainingExpiryWeeklyEmail |

**Total findings: 44**
- CRITICAL: 8
- HIGH: 24
- MEDIUM: 9
- LOW: 3
