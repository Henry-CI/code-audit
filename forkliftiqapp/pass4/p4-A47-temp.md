# Pass 4 Code Quality — Agent A47
**Audit run:** 2026-02-26-01
**Auditor:** A47
**Files audited:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/PreStartHistoryDb.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/PreStartQuestionDb.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/model/RealmInt.java`

---

## Step 1: Reading Evidence

### File 1 — PreStartHistoryDb.java

**Class:** `PreStartHistoryDb extends RealmObject`

**Fields:**
- Line 13: `public int userKey` (annotated `@SuppressWarnings("unused")`, field initializer `WebData.instance().getUserId()`)
- Line 15: `private String dateTime`
- Line 16: `public int driver_id`
- Line 17: `public int unit_id`

**Methods (exhaustive):**
| Line | Signature |
|------|-----------|
| 19 | `public static boolean hasPreStartDoneForToday(final int driver_id, final int unit_id)` |
| 33 | `static void setPreStartDone(final int driver_id, final int unit_id)` |

**Types / constants / enums / interfaces defined:** None.

**Imports used:**
- `android.support.annotation.NonNull`
- `au.com.collectiveintelligence.fleetiq360.WebService.WebData`
- `au.com.collectiveintelligence.fleetiq360.util.CommonFunc`
- `io.realm.Realm`, `io.realm.RealmObject`, `io.realm.RealmResults`
- `org.joda.time.DateTime`

---

### File 2 — PreStartQuestionDb.java

**Class:** `PreStartQuestionDb extends RealmObject`

**Fields:**
- Line 14–15: `public int userKey` (annotated `@SuppressWarnings("unused")`, field initializer `WebData.instance().getUserId()`)
- Line 17: `private long updateTime`
- Line 18: `private String prestartQuestionResultArray`
- Line 19–20: `private int equipmentId` (annotated `@SuppressWarnings("unused")`)

**Methods (exhaustive):**
| Line | Signature |
|------|-----------|
| 22 | `private boolean isExpired()` |
| 26 | `static boolean needToCache(final int equipmentId)` |
| 37 | `public static PreStartQuestionResultArray getQuestionResultArray(final int equipmentId)` |
| 53 | `public static void saveQuestions(final int equipmentId, final PreStartQuestionResultArray getEquipmentResultArray)` |

**Types / constants / enums / interfaces defined:** None.

**Imports used:**
- `android.support.annotation.NonNull`
- `au.com.collectiveintelligence.fleetiq360.WebService.WebData`
- `au.com.collectiveintelligence.fleetiq360.WebService.webserviceclasses.results.PreStartQuestionResultArray`
- `com.yy.libcommon.WebService.GsonHelper`
- `io.realm.Realm`, `io.realm.RealmObject`, `io.realm.RealmResults`
- `java.util.ArrayList`

---

### File 3 — RealmInt.java

**Class:** `RealmInt extends RealmObject`

**Fields:**
- Line 9: `int data` (package-private)

**Methods (exhaustive):** None.

**Types / constants / enums / interfaces defined:** None.

**Javadoc comment:** Line 5–7: `/** Created by steveyang on 1/10/16. */`

---

## Step 2 & 3: Findings

---

### A47-1 — HIGH — `userKey` field initializer calls live service singleton at object construction time

**Files:** `PreStartHistoryDb.java` line 13, `PreStartQuestionDb.java` lines 14–15

```java
// PreStartHistoryDb.java:13
@SuppressWarnings("unused")
public int userKey = WebData.instance().getUserId();

// PreStartQuestionDb.java:15
@SuppressWarnings("unused")
public int userKey = WebData.instance().getUserId();
```

**Problem:** Realm calls the no-arg constructor when deserializing objects from disk. At that point `WebData.instance().getUserId()` is evaluated, which returns the ID of the **currently logged-in user** — not the user who originally wrote the record. If a different user is logged in (e.g. after an account switch or cold start before full authentication), the `userKey` stored on the deserialized object will silently be overwritten with the wrong user ID. The field is also marked `@SuppressWarnings("unused")`, indicating the team already noticed it cannot be safely referenced from Java, but it is critical as the Realm query key used by `DataBaseHelp.getRealmQuery()`.

The same pattern exists in `SessionDb.java` and `LocationDb.java` (out of scope but corroborating the systemic nature). The correct pattern used by `EquipmentDb` stores no such initializer — `userId` there is written only inside an explicit transaction.

**Classification:** HIGH — silent data corruption risk on deserialization.

---

### A47-2 — HIGH — Nested `realm.executeTransaction()` inside `SafeRealm.Execute(Action)` differs from `SafeRealm.executeTransaction()` used in `EquipmentDb`

**Files:** `PreStartHistoryDb.java` lines 34–50, `PreStartQuestionDb.java` lines 54–68
**Reference (correct pattern):** `EquipmentDb.java` line 46

```java
// PreStartHistoryDb.java — manual nested transaction
SafeRealm.Execute(new SafeRealm.Action() {      // opens Realm instance
    @Override
    public void Execute(Realm realm) {
        final RealmResults<...> histories = ...findAll();
        realm.executeTransaction(new Realm.Transaction() {  // transaction nested inside
            @Override
            public void execute(@NonNull Realm realm) { ... }
        });
    }
});

// PreStartQuestionDb.java — same manual nesting pattern
SafeRealm.Execute(new SafeRealm.Action() {
    @Override
    public void Execute(Realm realm) {
        final RealmResults<...> questions = ...findAll();
        realm.executeTransaction(new Realm.Transaction() {
            @Override
            public void execute(@NonNull Realm realm) { ... }
        });
    }
});

// EquipmentDb.java — uses SafeRealm.executeTransaction() (the correct helper)
SafeRealm.executeTransaction(new SafeRealm.Action() {
    @Override
    public void Execute(Realm realm) { ... }   // query AND write in single managed transaction
});
```

**Problem:** `SafeRealm.executeTransaction()` wraps the entire action in one `realm.executeTransaction()` call, which is the safe, idiomatic pattern. The two files under audit instead open a Realm via `SafeRealm.Execute(Action)` (which does **not** wrap in a transaction), perform a `findAll()` query, and then call `realm.executeTransaction()` manually inside it. This creates a two-phase pattern where the query result (`RealmResults`) may be invalidated between the outer open and the inner transaction begin, and reads a stale snapshot. It is also inconsistent with the established `SafeRealm.executeTransaction` helper already present in the codebase.

**Classification:** HIGH — style/safety inconsistency, potential stale-result usage across the query/write boundary.

---

### A47-3 — MEDIUM — Asymmetric null-check on `RealmResults` before `.size()` call

**Files:** `PreStartHistoryDb.java` lines 26, 43; `PreStartQuestionDb.java` line 61

```java
// PreStartHistoryDb.java:26 — null check present
if (preStartHistories == null || preStartHistories.size() == 0) return false;

// PreStartHistoryDb.java:43 — null check present
PreStartHistoryDb history = (histories == null || histories.size() == 0)
    ? realm.createObject(PreStartHistoryDb.class) : histories.get(0);

// PreStartQuestionDb.java:32 — NO null check (only size check)
return questions.size() == 0 || questions.get(0).isExpired();

// PreStartQuestionDb.java:43-44 — null check present
if (questions != null && questions.size() != 0)
    return GsonHelper.objectFromString(...);

// PreStartQuestionDb.java:61 — null check present
PreStartQuestionDb question = (questions == null || questions.size() == 0)
    ? realm.createObject(PreStartQuestionDb.class) : questions.get(0);
```

**Problem:** In `needToCache()` (line 32 of `PreStartQuestionDb`) the `RealmResults` reference `questions` is dereferenced directly without a null guard, while every other call site in both files uses `questions == null || ...` or `questions != null && ...`. Although `RealmResults` returned by `findAll()` is documented as non-null, the inconsistency violates the defensive convention already established by the surrounding code, and any future refactor that introduces a nullable path would not be caught by this call site.

**Classification:** MEDIUM — defensive coding inconsistency.

---

### A47-4 — MEDIUM — `hasPreStartDoneForToday` only checks `get(0)` when multiple matching records may exist

**File:** `PreStartHistoryDb.java` lines 23–29

```java
final RealmResults<PreStartHistoryDb> preStartHistories = DataBaseHelp.getRealmQuery(realm, PreStartHistoryDb.class)
        .equalTo("driver_id", driver_id).equalTo("unit_id", unit_id).findAll();

if (preStartHistories == null || preStartHistories.size() == 0) return false;
DateTime dateTime = DateTime.parse(preStartHistories.get(0).dateTime);
return dateTime != null && CommonFunc.isCurrentDay(dateTime);
```

**Problem:** There is no ordering clause on the `findAll()` query. If multiple history records exist for the same `(driver_id, unit_id)` pair — which can happen because `setPreStartDone` uses upsert logic but is not transactionally atomic across the outer `SafeRealm.Execute` and inner `executeTransaction` (see A47-2) — the code reads `get(0)`, which is the first result in an unspecified Realm iteration order. If that first record holds a stale (yesterday's) `dateTime`, the check incorrectly returns `false` even though a more-recent record exists. The equivalent logic in `PreStartQuestionDb.needToCache()` has the same ordering gap but is less safety-critical.

**Classification:** MEDIUM — logical defect under race or duplicate-record conditions.

---

### A47-5 — MEDIUM — `@SuppressWarnings("unused")` on `equipmentId` field suppresses legitimate Realm warning

**File:** `PreStartQuestionDb.java` lines 19–20

```java
@SuppressWarnings("unused")
private int equipmentId;
```

**Problem:** `equipmentId` is a Realm-persisted field that is written inside `saveQuestions()` (line 62) and queried by string name `"equipmentId"` in all three methods. The annotation hides IDE "unused" warnings but the field is logically used — it cannot be removed. Suppressing warnings on genuinely-used fields masks the actual rationale (that Realm reads the field reflectively, never from Java code). There is no explanatory comment, and the annotation gives the false impression the field is expendable. The `@SuppressWarnings("unused")` on `userKey` has the same problem in both files.

**Classification:** MEDIUM — misleading suppression annotation without justification comment, makes the field appear removable.

---

### A47-6 — MEDIUM — `setPreStartDone` has package-private visibility but `hasPreStartDoneForToday` is public; visibility asymmetry is not documented

**File:** `PreStartHistoryDb.java` lines 19, 33

```java
public static boolean hasPreStartDoneForToday(final int driver_id, final int unit_id) { ... }  // line 19
static void setPreStartDone(final int driver_id, final int unit_id) { ... }                     // line 33
```

**Problem:** The read method is `public` (called from `WebApi` and `WebData` in the `WebService` package), while the write method is package-private. The write method is legitimately called only from `SessionDb` within the same `model` package. However, the design means an external caller can observe pre-start state but cannot clear or reset it — the asymmetry is not documented and could surprise maintainers who try to reset state from outside the model package, potentially leading to workarounds that bypass the intended access pattern.

**Classification:** MEDIUM — visibility asymmetry without documentation creates a leaky abstraction (read is public, write is package-private).

---

### A47-7 — MEDIUM — `saveQuestions` parameter name `getEquipmentResultArray` is a method-name style identifier

**File:** `PreStartQuestionDb.java` line 53

```java
public static void saveQuestions(final int equipmentId, final PreStartQuestionResultArray getEquipmentResultArray) {
```

**Problem:** The parameter is named `getEquipmentResultArray`, which starts with `get`, a Java convention reserved for getter methods. This name is inherited unchanged from the calling context in `EquipmentDb` (where it names a local variable in the same way), but as a formal parameter name in a public API it is confusing. It suggests to readers that it is a method reference or returns something. The name should be something like `questionResultArray` or `resultArray`. This is also inconsistent with `EquipmentDb.saveEquipmentResultArray(int, GetEquipmentResultArray getEquipmentResultArray)` which has the same issue but is out of scope.

**Classification:** MEDIUM — misleading identifier naming in public API signature.

---

### A47-8 — LOW — `RealmInt` class is entirely unused across the codebase

**File:** `RealmInt.java` lines 1–10

```java
public class RealmInt extends RealmObject {
    int data;
}
```

**Problem:** A comprehensive search of all Java source files under `app/src/main/java` finds zero references to `RealmInt` other than its own declaration. The class carries a creation comment (`Created by steveyang on 1/10/16`) dating it to October 2016. It has never gained any methods, access modifiers on its field, or usages. It is dead code and contributes to the Realm schema unnecessarily (Realm registers all `RealmObject` subclasses it finds on the classpath at startup, adding a useless table to the database schema).

**Classification:** LOW — dead class, adds unnecessary overhead to Realm schema.

---

### A47-9 — LOW — `android.support.annotation.NonNull` used instead of `androidx.annotation.NonNull`

**Files:** `PreStartHistoryDb.java` line 3, `PreStartQuestionDb.java` line 3

```java
import android.support.annotation.NonNull;
```

**Problem:** The Android Support Library was superseded by AndroidX. Using `android.support.annotation.NonNull` is deprecated; the migration target is `androidx.annotation.NonNull`. This also appears in `SafeRealm.java` (line 3) and `LocationDb.java` (line 3), indicating the migration has not been done for the model package. While functional today, it will cause build issues if the project migrates other modules to AndroidX (mixed Support/AndroidX is disallowed within a single compile unit without the `android.useAndroidX` + `android.enableJetifier` flags).

**Classification:** LOW — deprecated Support Library annotation import.

---

### A47-10 — INFO — Stale authorship comment in `RealmInt`

**File:** `RealmInt.java` lines 5–7

```java
/**
 * Created by steveyang on 1/10/16.
 */
```

**Problem:** Auto-generated IDE authorship Javadoc. It carries no semantic value, references a specific developer by personal name rather than a role, and is stale (2016). It is inconsistent — no other model class in the same package carries this comment. Not a defect, but clutter.

**Classification:** INFO — stale IDE-generated authorship comment.

---

## Summary Table

| ID | Severity | File | Description |
|----|----------|------|-------------|
| A47-1 | HIGH | PreStartHistoryDb.java, PreStartQuestionDb.java | `userKey` field initializer calls `getUserId()` at Realm deserialization time — wrong user ID written on object load |
| A47-2 | HIGH | PreStartHistoryDb.java, PreStartQuestionDb.java | Manual `realm.executeTransaction()` nesting inside `SafeRealm.Execute(Action)` instead of `SafeRealm.executeTransaction()` — inconsistent and unsafe pattern |
| A47-3 | MEDIUM | PreStartQuestionDb.java | Asymmetric null-check: `needToCache()` dereferences `RealmResults` without null guard unlike all other call sites |
| A47-4 | MEDIUM | PreStartHistoryDb.java | `hasPreStartDoneForToday` reads `get(0)` from unordered `findAll()` — stale record could return wrong result |
| A47-5 | MEDIUM | PreStartHistoryDb.java, PreStartQuestionDb.java | `@SuppressWarnings("unused")` on Realm-persisted fields without explanatory comment |
| A47-6 | MEDIUM | PreStartHistoryDb.java | `hasPreStartDoneForToday` public / `setPreStartDone` package-private — asymmetry undocumented |
| A47-7 | MEDIUM | PreStartQuestionDb.java | Parameter `getEquipmentResultArray` uses getter-style naming in a public method signature |
| A47-8 | LOW | RealmInt.java | Class is entirely unused (dead code) and adds unnecessary table to Realm schema |
| A47-9 | LOW | PreStartHistoryDb.java, PreStartQuestionDb.java | `android.support.annotation.NonNull` — deprecated Support Library, should be `androidx` |
| A47-10 | INFO | RealmInt.java | Stale IDE-generated authorship Javadoc comment |
