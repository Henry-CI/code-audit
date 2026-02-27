# Pass 4 – Code Quality Audit
**Agent:** A70
**Audit run:** 2026-02-26-01
**Files reviewed:**
1. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/util/CompanyDateFormatter.java`
2. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/util/ComplianceAccepter.java`
3. `app/src/main/java/au/com/collectiveintelligence/fleetiq360/util/ServerDateFormatter.java`

---

## Step 1: Reading Evidence

### File 1: `CompanyDateFormatter.java`

**Class:** `CompanyDateFormatter`
**Package:** `au.com.collectiveintelligence.fleetiq360.util`

**Fields (all private instance):**
- `SimpleDateFormat timeFormat` (line 10)
- `SimpleDateFormat dateFormat` (line 11)
- `SimpleDateFormat dateTimeFormat` (line 12)

**Methods (exhaustive):**
| Method | Lines | Visibility |
|--------|-------|------------|
| `CompanyDateFormatter(String companyDateTimeFormatPattern)` | 14–22 | public constructor |
| `formatTime(Date date)` | 24–26 | public |
| `formatDate(Date date)` | 28–30 | public |
| `formatDateTime(Date date)` | 32–34 | public |
| `parseDate(String date)` | 36–38 | public |

**Types/constants/enums defined:** none

**Imports:** `ParsePosition`, `SimpleDateFormat`, `Date`, `Locale`, `TimeZone`

---

### File 2: `ComplianceAccepter.java`

**Class:** `ComplianceAccepter`
**Package:** `au.com.collectiveintelligence.fleetiq360.util`

**Fields (all private instance):**
- `Context context` (line 20)
- `User user` (line 21)

**Methods (exhaustive):**
| Method | Lines | Visibility |
|--------|-------|------------|
| `ComplianceAccepter(Context context)` | 23–26 | public constructor |
| `askForCompliance()` | 28–52 | public |

**Anonymous inner classes:**
- `DialogInterface.OnClickListener` – Accept button (lines 34–41)
- `DialogInterface.OnClickListener` – Refuse button (lines 43–49)

**Types/constants/enums defined:** none

**Imports:** `AlertDialog`, `Context`, `DialogInterface`, `Intent`, `R`, `WebApi`, `WebData`, `WebListener`, `UpdateUserParameter`, `CommonResult`, `LoginActivity`, `CurrentUser`, `User`, `Calendar`

---

### File 3: `ServerDateFormatter.java`

**Class:** `ServerDateFormatter`
**Package:** `au.com.collectiveintelligence.fleetiq360.util`

**Fields (all private instance):**
- `SimpleDateFormat dateFormat` (line 10)
- `SimpleDateFormat dateTimeFormat` (line 11)

**Methods (exhaustive):**
| Method | Lines | Visibility |
|--------|-------|------------|
| `ServerDateFormatter()` | 13–19 | public constructor |
| `formatDate(Date date)` | 21–23 | public |
| `formatDateTime(Date date)` | 25–27 | public |
| `parseDate(String date)` | 29–32 | public |
| `parseDateTime(String date)` | 34–36 | public |

**Types/constants/enums defined:** none

**Imports:** `ParsePosition`, `SimpleDateFormat`, `Date`, `Locale`, `TimeZone`

---

## Step 2 & 3: Findings

---

### A70-1 — HIGH — `SimpleDateFormat` is not thread-safe; instances are shared across calls without synchronization

**Files:** `CompanyDateFormatter.java` (lines 10–12), `ServerDateFormatter.java` (lines 10–11)

Both classes store `SimpleDateFormat` instances as mutable private fields initialized once in the constructor. `SimpleDateFormat` is explicitly documented as not thread-safe. Both formatters are used from multiple call sites across the codebase (UI fragments, presenters, model/database classes, application-level code). If two threads ever invoke `format()` or `parse()` on the same formatter instance concurrently, the internal calendar state becomes corrupted, silently producing wrong dates or throwing `NumberFormatException`.

`ServerDateFormatter` is particularly at risk because it is instantiated as a field (and therefore reused) in `PreStartCheckListPresenter`, `JobsPresenter`, `IncidentFragment`, `JobsFragment`, `EquipmentListFragment`, `SessionDb`, and `ShockEventsDb`, some of which interact with background threads (sync service, BLE event processing).

```java
// CompanyDateFormatter.java line 11-12 — shared mutable state
private SimpleDateFormat dateFormat;
private SimpleDateFormat dateTimeFormat;

// ServerDateFormatter.java line 10-11 — same pattern
private SimpleDateFormat dateFormat;
private SimpleDateFormat dateTimeFormat;
```

Neither class is documented as not thread-safe, and neither guards its methods with synchronization.

---

### A70-2 — HIGH — `ServerDateFormatter.parseDateTime` has no null/empty guard; `CompanyDateFormatter.parseDate` has no null/empty guard

**Files:** `ServerDateFormatter.java` (lines 34–36), `CompanyDateFormatter.java` (lines 36–38)

`ServerDateFormatter.parseDate` (line 30) correctly guards against null and empty input and returns `null`. However, the sibling method `parseDateTime` (line 34) applies no such guard:

```java
// ServerDateFormatter.java
public Date parseDate(String date) {
    if (date == null || date.isEmpty()) return null;   // guarded
    return dateFormat.parse(date, new ParsePosition(0));
}

public Date parseDateTime(String date) {
    return dateTimeFormat.parse(date, new ParsePosition(0));  // NO guard — NullPointerException if null
}
```

Similarly, `CompanyDateFormatter.parseDate` (line 36–38) has no null/empty check:

```java
// CompanyDateFormatter.java
public Date parseDate(String date) {
    return dateFormat.parse(date, new ParsePosition(0));  // NO guard
}
```

`SessionResult.java` calls `parseDateTime` on `finish_time` which is a server-supplied string field (lines 54, 61) — a missing or null value from the server would produce a NullPointerException at runtime.

---

### A70-3 — HIGH — Fire-and-forget API call swallows errors silently; compliance update may silently fail

**File:** `ComplianceAccepter.java` (line 40)

After the user accepts compliance, an `updateUser` API call is dispatched with a default (no-op) `WebListener`:

```java
WebApi.async().updateUser(user.getId(), parameter, new WebListener<CommonResult>());
```

`WebListener.onFailed()` is an empty method. If the server-side compliance update fails (network error, server error, auth expiry), the local user object has already been mutated (`user.updateCompliance(...)` on line 37) and persisted to the database (`UserDb.save(this)` inside `updateCompliance`). The server record will not reflect the acceptance, but the app will treat the user as having accepted. On next login the compliance dialog will not appear because `complianceIsValid()` returns true based on the local state. This creates a state divergence between device and server.

---

### A70-4 — MEDIUM — `ComplianceAccepter` constructs `ServerDateFormatter` on every dialog acceptance; inconsistent instantiation pattern

**File:** `ComplianceAccepter.java` (line 39)

```java
new ServerDateFormatter().formatDate(user.getComplianceDate())
```

A new `ServerDateFormatter` is constructed inline every time the Accept button is clicked. This is inconsistent with the pattern used by `IncidentFragment`, `JobsFragment`, and `JobsPresenter`, which store the formatter as a class field. More importantly, this shows a lack of a singleton or injected formatter throughout the codebase — there is no shared instance of `ServerDateFormatter`, making it impossible to replace the implementation (e.g., for testing or timezone policy changes) without touching every call site.

---

### A70-5 — MEDIUM — Format-string pattern stripping in `CompanyDateFormatter` is fragile and undocumented

**File:** `CompanyDateFormatter.java` (line 18)

```java
dateFormat = new SimpleDateFormat(companyDateTimeFormatPattern.replace(" HH:mm:ss", ""), Locale.US);
```

The date-only format is derived from the datetime pattern by a raw string replacement of the literal `" HH:mm:ss"`. This approach is fragile:

- If the server delivers a pattern with seconds in a different position, different separator, or without a leading space (e.g., `"dd/MM/yyyyHH:mm:ss"` or `"dd/MM/yyyy HH:mm"`), the replacement silently produces a malformed or unchanged pattern and `SimpleDateFormat` may throw or silently misbehave.
- The specific sentinel string `" HH:mm:ss"` is a hidden contract with the server's date-format API field — there is no comment, constant, or validation documenting this assumption.
- There is no fallback or validation of the resulting pattern.

---

### A70-6 — MEDIUM — `ComplianceAccepter` holds a long-lived `Context` reference without lifecycle management

**File:** `ComplianceAccepter.java` (lines 20, 23–26, 47)

`ComplianceAccepter` stores the `Context` passed to its constructor as a field (line 20). The class is instantiated in `DashboardFragment.onActivityCreated` as a transient object:

```java
new ComplianceAccepter(getContext()).askForCompliance();
```

While the transient instantiation is safe in isolation, the anonymous `OnClickListener` for the "Refuse" button captures `context` in its closure (line 47). If the hosting Activity is destroyed while the dialog is still showing (rotation, back-stack navigation), the listener holds a stale reference to the destroyed context and will call `context.startActivity(...)` on it, which can cause a `WindowManager$BadTokenException` or a leaked window.

---

### A70-7 — MEDIUM — `ComplianceAccepter` uses hard-coded English string literals for dialog button labels

**File:** `ComplianceAccepter.java` (lines 34, 43)

```java
.setPositiveButton("Accept", ...)
.setNegativeButton("Refuse", ...)
```

The dialog message text (`R.string.gdpr_compliance`) is correctly sourced from a string resource, but the two button labels are hard-coded English string literals. This breaks localization: if the app is configured to run in a non-English locale, all other UI strings will be translated but these buttons will remain in English. The pattern is inconsistent within the same `AlertDialog.Builder` chain.

---

### A70-8 — MEDIUM — `ServerDateFormatter` uses `"GMT"` string constant; should use `TimeZone.getTimeZone("UTC")`

**File:** `ServerDateFormatter.java` (line 14)

```java
TimeZone timeZone = TimeZone.getTimeZone("GMT");
```

The Java `TimeZone.getTimeZone(String)` method silently returns `GMT` for any unrecognized ID. The canonical UTC identifier for `TimeZone` is `"UTC"`. Although `"GMT"` and `"UTC"` represent the same offset, using `"GMT"` is a minor style inconsistency given that the standard Java/Android convention is `"UTC"`. More importantly, if the string `"GMT"` were accidentally typo'd, the API would still silently return GMT without any error, masking the mistake. The `ZoneOffset.UTC` constant (API 26+) or `TimeZone.getTimeZone("UTC")` is the conventional form.

---

### A70-9 — MEDIUM — `parseDateTime` in `ServerDateFormatter` silently returns `null` on parse failure with no indication to caller

**File:** `ServerDateFormatter.java` (lines 34–36)

`SimpleDateFormat.parse(String, ParsePosition)` returns `null` on a parse failure (it does not throw). The caller has no way to distinguish a null input from a malformed-input parse failure because both yield `null` return values. The `parseDate` guard (line 30) returns `null` for null/empty input before even attempting the parse, and the parse itself can also return null — two distinct failure modes map to the same return value. This applies to both `parseDate` and `parseDateTime`, and to `CompanyDateFormatter.parseDate` as well.

---

### A70-10 — LOW — Style inconsistency: `dateFormat` field name is identical across both formatter classes but `timeFormat` exists only in `CompanyDateFormatter`

**Files:** `CompanyDateFormatter.java` (lines 10–12), `ServerDateFormatter.java` (lines 10–11)

`CompanyDateFormatter` exposes `formatTime` / `formatDate` / `formatDateTime` plus `parseDate`.
`ServerDateFormatter` exposes `formatDate` / `formatDateTime` plus `parseDate` / `parseDateTime`.

There is no `parseTime` in `CompanyDateFormatter` and no `parseDateTime` counterpart. The two classes are structurally similar but do not follow a common interface or base class, making it impossible for callers to work with either formatter polymorphically. This is a design omission that will cause copy-paste drift as the classes evolve independently.

---

### A70-11 — LOW — `ComplianceAccepter` directly couples UI dialog logic with network and persistence side-effects

**File:** `ComplianceAccepter.java` (lines 36–48)

`askForCompliance()` contains three concerns in one method:
1. UI decision (show dialog)
2. Persistence (`user.updateCompliance` → `UserDb.save`)
3. Network call (`WebApi.async().updateUser(...)`)
4. Navigation (`WebData.instance().logout()` + `startActivity`)

This tight coupling makes the compliance-acceptance logic untestable without a running Android runtime. There is no abstraction layer separating UI from business logic. This is a structural issue affecting testability and future maintainability.

---

### A70-12 — LOW — `WebListener` `TAG` field is unused

**Context file:** `WebService/WebListener.java` (line 9)

```java
private static final String TAG = "WebListener";
```

This field is declared but never referenced in any method of `WebListener`. It would generate a compiler warning in most IDEs. While not in the directly assigned files, `ComplianceAccepter` passes `new WebListener<CommonResult>()` directly and the unused TAG leaks into every instantiation site.  *(Informational — in scope because the instantiation is in an assigned file.)*

---

## Summary Table

| ID | Severity | File | Summary |
|----|----------|------|---------|
| A70-1 | HIGH | CompanyDateFormatter.java, ServerDateFormatter.java | `SimpleDateFormat` instances not thread-safe; shared mutable state across concurrent callers |
| A70-2 | HIGH | ServerDateFormatter.java, CompanyDateFormatter.java | `parseDateTime` and `CompanyDateFormatter.parseDate` lack null/empty guard; NPE risk on null input |
| A70-3 | HIGH | ComplianceAccepter.java | Fire-and-forget API call with no-op error handler; compliance state diverges between device and server on network failure |
| A70-4 | MEDIUM | ComplianceAccepter.java | Inline `new ServerDateFormatter()` instantiation inconsistent with field-stored instances elsewhere; no shared/injectable formatter |
| A70-5 | MEDIUM | CompanyDateFormatter.java | Fragile literal string replacement to derive date-only format pattern; undocumented server contract |
| A70-6 | MEDIUM | ComplianceAccepter.java | Stored `Context` reference in listener closure; stale context risk after Activity destruction |
| A70-7 | MEDIUM | ComplianceAccepter.java | Hard-coded English button labels break localization; inconsistent with resource-based dialog message |
| A70-8 | MEDIUM | ServerDateFormatter.java | `"GMT"` used instead of canonical `"UTC"` for timezone ID |
| A70-9 | MEDIUM | ServerDateFormatter.java, CompanyDateFormatter.java | Parse failure and null input both return `null`; caller cannot distinguish failure modes |
| A70-10 | LOW | CompanyDateFormatter.java, ServerDateFormatter.java | No shared interface/base class; structural drift between two similar formatter classes |
| A70-11 | LOW | ComplianceAccepter.java | UI, persistence, and network concerns mixed in single method; not unit-testable |
| A70-12 | LOW | (WebListener.java via ComplianceAccepter.java) | `TAG` field declared but never used in `WebListener` |
