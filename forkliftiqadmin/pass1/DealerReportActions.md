# Pass 1 Audit — DealerImpactReportAction / DealerIncidentReportAction / DealerPreOpsReportAction / DealerSessionReportAction

**Files:**
- `src/main/java/com/action/DealerImpactReportAction.java`
- `src/main/java/com/action/DealerIncidentReportAction.java`
- `src/main/java/com/action/DealerPreOpsReportAction.java`
- `src/main/java/com/action/DealerSessionReportAction.java`

**Supporting files examined:**
- `src/main/java/com/actionform/ImpactReportSearchForm.java`
- `src/main/java/com/actionform/IncidentReportSearchForm.java`
- `src/main/java/com/actionform/PreOpsReportSearchForm.java`
- `src/main/java/com/actionform/SessionReportSearchForm.java`
- `src/main/java/com/actionform/ReportSearchForm.java`
- `src/main/java/com/service/ReportService.java`
- `src/main/java/com/dao/ImpactReportDAO.java`
- `src/main/java/com/dao/IncidentReportDAO.java`
- `src/main/java/com/dao/SessionDAO.java`
- `src/main/java/com/dao/ResultDAO.java`
- `src/main/java/com/querybuilder/impacts/ImpactsByCompanyIdQuery.java`
- `src/main/java/com/querybuilder/impacts/ImpactsReportByCompanyIdQuery.java`
- `src/main/java/com/querybuilder/incidents/IncidentReportByCompanyIdQuery.java`
- `src/main/java/com/querybuilder/preops/PreOpsByCompanyIdQuery.java`
- `src/main/java/com/querybuilder/preops/PreOpsReportByCompanyIdQuery.java`
- `src/main/java/com/querybuilder/session/SessionsByCompanyIdQuery.java`
- `src/main/java/com/querybuilder/filters/` (all filter handlers)
- `src/main/java/com/querybuilder/StatementPreparer.java`
- `src/main/java/com/bean/ReportFilterBean.java` and related filter beans
- `src/main/java/com/bean/SessionFilterBean.java`
- `src/main/java/com/dao/UnitDAO.java`
- `src/main/java/com/dao/DriverDAO.java`
- `src/main/java/com/dao/ManufactureDAO.java`
- `src/main/java/com/actionservlet/PreFlightActionServlet.java`
- `src/main/java/com/util/CompanySessionSwitcher.java`
- `src/main/webapp/WEB-INF/struts-config.xml`

**Date:** 2026-02-26

---

## Summary

All four dealer report actions share a structurally identical authentication pattern: they read `sessCompId` from the session and throw a `RuntimeException` if it is null. Beyond that single check there is **no dealer role verification** — any authenticated user who navigates to the dealer report URLs can invoke these actions regardless of whether they hold the `ROLE_DEALER` role or any other elevated privilege.

The core reporting logic is sound in one respect: each action passes only `sessCompId` (the dealer's own company ID sourced from the server-side session) as the tenancy anchor to the query layer. The query builders apply that ID via parameterised `PreparedStatement` bindings, so the company boundary itself is not injectable.

However, several significant issues exist around authorization scope, IDOR for filter parameters, CSRF protection, input validation gaps, a dangerous string-comparison bug, a broken singleton double-checked locking pattern, and an unhandled NPE risk on session attribute access. The most operationally serious finding is the missing dealer role gate, which means any logged-in company user — including regular operators — could invoke these four endpoints if they craft the correct URL.

---

## Findings

### HIGH: No Dealer Role Verification in Any of the Four Actions

**Files:**
- `DealerImpactReportAction.java` (lines 24–25)
- `DealerIncidentReportAction.java` (lines 24–25)
- `DealerPreOpsReportAction.java` (lines 24–25)
- `DealerSessionReportAction.java` (lines 24–25)

**Description:**
Each action checks only that `sessCompId != null` before proceeding. There is no check against `session.getAttribute("isDealer")` or `session.getAttribute("isDealerLogin")`. Both of these session flags are set during login and during company-context switches (`CompanySessionSwitcher`). The struts-config entries for all four actions use `validate="false"`, so no declarative role guard fires either. Any authenticated user — including a regular company operator — can navigate to `/dealerImpactReport.do`, `/dealerIncidentReport.do`, `/dealerPreOpsReport.do`, or `/dealerSessionReport.do` and receive cross-company report data for their own `sessCompId`.

**Risk:**
An operator-role user logged in to a non-dealer company can enumerate the dealer report endpoints. If an administrator later switches a company's context or if `isDealer` is `false` in the session, the report executes anyway. In multi-tenant SaaS deployments this exposes aggregated impact, incident, pre-ops, and session data to users who should be restricted to single-company views.

**Recommendation:**
Add an explicit role gate at the top of each action's `execute()` method, immediately after the `sessCompId` null check, before any data access:

```java
Boolean isDealer = (Boolean) session.getAttribute("isDealer");
if (isDealer == null || !isDealer) {
    return mapping.findForward("accessDenied");
}
```

Alternatively, introduce a shared `DealerBaseAction` superclass that performs this check, and extend it for all four actions.

---

### HIGH: IDOR via Unvalidated `vehicle_id` and `driver_id` Filter Parameters in DealerSessionReportAction

**File:** `DealerSessionReportAction.java` (lines 34–37); `SessionReportSearchForm.java` (lines 25–26); `SessionsByCompanyIdQuery.java` (lines 41–42)

**Description:**
`DealerSessionReportAction` populates the `vehicles` and `drivers` drop-down lists using the dealer's own `companyId` (lines 34–35). However, the `vehicle_id` and `driver_id` values submitted in the search form arrive via HTTP request parameters (bound by Struts to `SessionReportSearchForm`) and are passed directly to `SessionFilterBean` without any check that those IDs belong to the dealer's company or any of its sub-companies. The query in `SessionsByCompanyIdQuery.getQuery()` does apply a `WHERE (unit_owner_company_id = ? OR unit_assigned_company_id = ?)` clause anchored to `sessCompId`, but it then adds an unchecked `AND unit_id = ?` or `AND driver_id = ?` clause via `SessionUnitFilterHandler` and `SessionDriverFilterHandler`. If a vehicle or driver is shared across multiple companies (e.g., assigned to a sub-company that is also visible to another dealer), a dealer could filter by an ID they do not own to confirm whether data exists — a boolean oracle. Even without cross-tenancy, the filter narrows the result set to a specific resource without ownership confirmation.

**Risk:**
An authenticated dealer can submit arbitrary `vehicle_id` or `driver_id` values that do not belong to their company to probe for session data associated with other companies' vehicles or drivers. The database-level `WHERE` clause partially mitigates full data leakage, but does not eliminate enumeration or oracle attacks.

**Recommendation:**
Before building the filter bean, verify that the submitted `vehicle_id` and `driver_id` values belong to the dealer's company or one of its sub-companies:

```java
if (form.getVehicle_id() != null) {
    // confirm unit belongs to dealer or sub-company
}
```

The existing `UnitDAO.getAllUnitsByCompanyId(companyId)` call already retrieves the authorised unit list. Cross-reference the submitted ID against that list server-side rather than relying solely on the database predicate.

---

### HIGH: IDOR via Unvalidated `manu_id` and `type_id` Filter Parameters Across All Four Actions

**Files:**
- `ImpactReportSearchForm.java` (lines 34–35)
- `IncidentReportSearchForm.java` (lines 17–18)
- `PreOpsReportSearchForm.java` (lines 29–30)
- `SessionReportSearchForm.java` — not applicable (no manufacturer/type filters)

**Description:**
The `manu_id` (manufacturer ID) and `type_id` (unit type ID) filter values are HTTP request parameters bound by Struts to the form bean and passed directly into the filter beans. The filter handlers `UnitManufactureFilterHandler` and `UnitTypeFilterHandler` emit `AND manufacture_id = ?` / `AND type_id = ?` using parameterised statements, preventing SQL injection. However, no check is performed to confirm that the submitted manufacturer or type ID is valid, active, or associated with units visible to the requesting dealer. A dealer could submit arbitrary integer IDs to enumerate whether any impacts, incidents, or pre-ops results exist for a given manufacturer or type combination that crosses company boundaries — a form of boolean IDOR oracle.

**Risk:**
Enumeration of cross-company data by probing manufacturer and type IDs. The impact is lower than a full data disclosure but can reveal tenancy information (e.g., "company X uses manufacturer Y").

**Recommendation:**
Validate submitted `manu_id` values against `ManufactureDAO.getAllManufactures(sessCompId)` — which the action already calls to populate the drop-down — and reject any submitted value not in that list. Apply the same pattern for `type_id` against the unit type list.

---

### MEDIUM: No CSRF Protection on Any of the Four Report Search Forms

**Files:**
- `struts-config.xml` (lines 555–581, `validate="false"` on all four action mappings)
- `DealerImpactReportAction.java`, `DealerIncidentReportAction.java`, `DealerPreOpsReportAction.java`, `DealerSessionReportAction.java`

**Description:**
All four action mappings in `struts-config.xml` are defined with `validate="false"`. None of the action classes inspect a CSRF token. Apache Struts 1.x has no built-in CSRF protection. While these are read-only report actions (no state mutation), CSRF can force a dealer's browser to submit a crafted search query — including a forged `vehicle_id`, `manu_id`, or date range — and the resulting page response (visible via the browser) could leak data. Combined with the absence of `SameSite=Strict` cookies (not confirmed in this audit but typical of legacy Struts 1 deployments), this is a real attack surface.

**Risk:**
An attacker who can induce a dealer to visit a malicious page can submit crafted report filter requests on behalf of the dealer. If the response page is subsequently loaded in a cross-origin context (e.g., via `<img>` or form submission), the attacker may be able to extract report data.

**Recommendation:**
Introduce a synchronised CSRF token: generate a random token at session creation, store it in the session, render it as a hidden field in all report search forms, and validate it in each action before processing. For Struts 1.x, this requires manual implementation in a shared base action or a servlet filter.

---

### MEDIUM: `SessionFilterBean.start()` and `SessionFilterBean.end()` Default to Current Timestamp When No Date Is Supplied

**File:** `SessionFilterBean.java` (lines 23–30)

**Description:**
The `start()` and `end()` methods in `SessionFilterBean` return `Calendar.getInstance().getTime()` as a default when the respective field is null. `DateBetweenFilterHandler.filterBetweenTwoDates()` returns `true` when **both** `start()` and `end()` are non-null. Because these methods never return null (they fall back to the current time), `filterBetweenTwoDates()` will always be `true`, meaning the `BETWEEN ? AND ?` clause is always appended when no date range is provided by the user. This means an unfiltered session report request silently scopes to the current instant at the time of query construction rather than returning all sessions. A dealer submitting the form without date filters will receive an empty or near-empty result set rather than a full history, with no indication that a date filter is being applied.

By contrast, `ReportFilterBean` (used by Impact, Incident, and PreOps forms) uses the same defaulting pattern but those actions store dates that can be null in the filter bean builder (the builder sets `null` when blank), so the DateBetweenFilterHandler correctly skips the clause when both are null. The inconsistency is isolated to `SessionFilterBean`.

**Risk:**
Data integrity / correctness: dealers relying on an unfiltered session report will silently receive an incorrect (empty) result. This is a functional bug with a secondary security implication — a dealer may incorrectly believe there are no sessions for their fleet, masking operational visibility.

**Recommendation:**
Change `SessionFilterBean.start()` and `SessionFilterBean.end()` to return `null` when the field is null, consistent with the pattern in `ReportFilterBean`. The caller (`DateBetweenFilterHandler`) already handles the null case — `ignoreFilter()` returns `true` when the filter itself is null, and `filterBetweenTwoDates()` correctly gates on both being non-null.

---

### MEDIUM: Timezone Input Accepted from Client Without Validation

**Files:**
- `ImpactReportSearchForm.java` (line 39)
- `PreOpsReportSearchForm.java` (line 33)
- `SessionReportSearchForm.java` (line 29)
- `IncidentReportSearchForm.java` (line 21)
- `DateBetweenFilterHandler.java` (lines 22, 29)

**Description:**
All four search forms accept a `timezone` field from the HTTP request. The value is passed through the filter bean and into `DateBetweenFilterHandler.prepareStatement()` as a string parameter bound with `preparer.addString(filter.timezone())`. It is ultimately used in SQL expressions of the form `timezone(?, field at time zone 'UTC')`. While this value is correctly parameterised (no SQL injection risk), no validation is performed to confirm the submitted string is a valid IANA timezone identifier. An attacker can submit an invalid timezone string, causing a database-level error that propagates up as an unhandled `SQLException` — leaking internal error details in the response depending on the application's error handling. Additionally, `ImpactReportSearchForm` accepts timezone from the form even though the action also retrieves `timezone` from the session attribute `sessTimezone` (line 29 of `DealerImpactReportAction.java`) — creating an ambiguous dual-source pattern.

**Risk:**
Malformed timezone strings cause server-side database errors with potential stack trace disclosure. The dual-source timezone (session vs. form field) creates an inconsistency risk where the form field may silently override the trusted session value.

**Recommendation:**
Validate the submitted timezone string against `java.util.TimeZone.getAvailableIDs()` or a trusted allow-list before use. For the impact report, remove the `timezone` field from `ImpactReportSearchForm` entirely and rely exclusively on the server-side `sessTimezone` session attribute.

---

### MEDIUM: Broken Double-Checked Locking in `ReportService` Singleton

**File:** `ReportService.java` (lines 20–27)

**Description:**
The `getInstance()` method uses the outer `if (theInstance == null)` check outside the `synchronized` block but only a single assignment inside — without a second null check inside the synchronized block:

```java
public static ReportService getInstance() {
    if (theInstance == null) {
        synchronized (ReportService.class) {
            theInstance = new ReportService();  // no inner null check
        }
    }
    return theInstance;
}
```

Without the inner null check, two threads that both pass the outer `if` concurrently can each enter the synchronized block sequentially and create two instances, with the second overwriting the first. The `theInstance` field is also not declared `volatile`, so the Java Memory Model does not guarantee visibility of the write across threads without the `volatile` keyword, making the outer check fundamentally unsafe.

`ImpactReportDAO.getInstance()` implements the correct double-checked locking pattern (with the inner null check); `ReportService.getInstance()` does not.

**Risk:**
Under concurrent load, multiple `ReportService` instances may be created. Each holds its own `resultDAO` and `impactReportDAO` references. If any instance-level state is accumulated (e.g., connection or cache state in `ResultDAO`), concurrent creation could cause data inconsistency or resource leaks.

**Recommendation:**
Add `volatile` to the `theInstance` field declaration and add the inner null check:

```java
private static volatile ReportService theInstance;

public static ReportService getInstance() {
    if (theInstance == null) {
        synchronized (ReportService.class) {
            if (theInstance == null) {
                theInstance = new ReportService();
            }
        }
    }
    return theInstance;
}
```

---

### LOW: Null Session Dereference Risk When `session.getAttribute("sessDateFormat")` Returns Null

**Files:**
- `DealerImpactReportAction.java` (lines 27–29)
- `DealerIncidentReportAction.java` (lines 27–29)
- `DealerPreOpsReportAction.java` (lines 28–30)
- `DealerSessionReportAction.java` (lines 27–29)

**Description:**
All four actions read `sessDateFormat`, `sessDateTimeFormat`, and `sessTimezone` from the session without null checks. These attributes are set by `CompanySessionSwitcher.UpdateCompanySessionAttributes()` at login and on company context switch, but they are not set by `PreFlightActionServlet`. If a session exists (so `sessCompId != null`) but the additional attributes are absent — possible if the session was partially populated, if a failover occurred, or if a developer test session was manually constructed — the `String` variables will be null. These null values are then passed into `DateUtil.stringToUTCDate()` as the `format` argument and into `ReportService` methods as `timezone`, where they are used without null checks, potentially causing `NullPointerException` or silent formatting errors.

**Risk:**
Application error (500 response) with possible stack trace disclosure. Not directly exploitable but reduces robustness of the auth gate.

**Recommendation:**
Add null checks for `sessDateFormat`, `sessDateTimeFormat`, and `sessTimezone` after reading them from the session. If any are null, redirect to the expiry/error page rather than proceeding.

---

### LOW: String Identity Comparison Used for Empty-String Check in `PreOpsReportSearchForm`

**File:** `PreOpsReportSearchForm.java` (line 33)

**Description:**
The timezone field null/empty check uses reference equality (`== ""`):

```java
.timezone(this.timezone == null || this.timezone == "" ? null : this.timezone)
```

In Java, `==` on `String` compares object identity, not value. A non-null, non-interned empty string submitted from an HTTP request will not be `==` to the string literal `""`. As a result, an empty string timezone value will be passed to `DateBetweenFilterHandler` rather than converted to null, causing a downstream database error when PostgreSQL evaluates `timezone('', ...)`.

The same form's siblings (`ImpactReportSearchForm` line 39, `IncidentReportSearchForm` line 21, `SessionReportSearchForm` line 29) correctly use `StringUtils.isBlank()` for this check. The defect is isolated to `PreOpsReportSearchForm`.

**Risk:**
An empty `timezone` form submission on the Pre-Ops report causes a database-level error. This is a denial-of-service vector for the Pre-Ops report endpoint (a dealer can trigger it by submitting an empty timezone field, which is the default for browsers that do not send the field).

**Recommendation:**
Replace the reference comparison with `StringUtils.isBlank()`, consistent with the other three search forms:

```java
.timezone(StringUtils.isBlank(this.timezone) ? null : this.timezone)
```

---

### LOW: `getSession(false)` Can Return Null If No Session Exists; Subsequent Attribute Access Throws NPE

**Files:**
- `DealerImpactReportAction.java` (lines 23–24)
- `DealerIncidentReportAction.java` (lines 23–24)
- `DealerPreOpsReportAction.java` (lines 23–24)
- `DealerSessionReportAction.java` (lines 23–24)

**Description:**
All four actions call `request.getSession(false)` and then immediately dereference the returned `HttpSession` object without a null check:

```java
HttpSession session = request.getSession(false);
String sessCompId = (String) session.getAttribute("sessCompId");
```

`getSession(false)` returns `null` when no session exists. `PreFlightActionServlet` (the custom `ActionServlet` subclass) does check for a null session and redirects to the expiry page, so in the normal request path a session is always present. However, the filter only fires for `doGet`/`doPost` requests routed through the servlet. Any path that bypasses `PreFlightActionServlet` (e.g., a direct dispatcher forward, an include, or a filter misconfiguration) would deliver a null session to the action, causing a `NullPointerException` at `session.getAttribute(...)`.

**Risk:**
Unhandled `NullPointerException` causing a 500 error. In a misconfigured or forked deployment the NPE occurs before the `sessCompId` null check, bypassing the authentication check entirely (though the NPE itself terminates the request).

**Recommendation:**
Add a null check immediately after `getSession(false)` and handle it gracefully:

```java
HttpSession session = request.getSession(false);
if (session == null) {
    return mapping.findForward("expire");
}
```

---

### INFO: All Four Actions Use `validate="false"` — No Struts ActionForm Validation Defined

**File:** `struts-config.xml` (lines 555–581)

**Description:**
All four dealer report action mappings specify `validate="false"`, disabling Struts declarative validation. No `validate()` methods are overridden in any of the four ActionForm subclasses. Date range, manufacturer ID, type ID, vehicle ID, and driver ID are all accepted from the request without any format or range validation at the form layer. Date parsing is delegated to `DateUtil.stringToUTCDate()`, which silently returns `null` on parse failure (falling back to `dd/MM/yyyy` format before giving up). This means a malformed date string does not produce a user-visible error — it simply results in the date filter being silently ignored, returning a broader-than-expected result set.

**Risk:**
Informational / UX: malformed date input is silently dropped, potentially misleading dealers about the scope of the report they are viewing.

**Recommendation:**
Implement `validate()` in each form class (or a shared `ReportSearchForm.validate()`) to check date format, numeric range of IDs, and required fields. Return `ActionErrors` to display user-facing validation messages rather than silently ignoring bad input.

---

### INFO: `ManufactureDAO.getAllManufactures()` Called on Every Request With No Caching

**Files:**
- `DealerImpactReportAction.java` (line 33)
- `DealerIncidentReportAction.java` (line 33)
- `DealerPreOpsReportAction.java` (line 33)

**Description:**
Each invocation of the impact, incident, and pre-ops report actions calls `ManufactureDAO.getAllManufactures(sessCompId)` to populate the manufacturer drop-down. `UnitDAO.getAllUnitType()` is called similarly. These are database queries executed synchronously on every page load (including non-search, initial display requests). If these lists change infrequently, this is unnecessary database load. `ManufactureDAO` has a singleton instance available (`ManufactureDAO.getInstance()`) but the static method `getAllManufactures` does not use any caching.

**Risk:**
Performance / scalability concern, not a security issue. Included for completeness.

**Recommendation:**
Consider caching the manufacturer and unit type lists (e.g., in the session or in the DAO singleton with a short TTL) to reduce per-request database load.

---

### INFO: `IncidentReportDAO.getInstance()` Has a Copy-Paste Defect in Its Synchronized Block

**File:** `IncidentReportDAO.java` (line 17)

**Description:**
The `getInstance()` method in `IncidentReportDAO` synchronizes on `ImpactReportDAO.class` instead of `IncidentReportDAO.class`:

```java
synchronized (ImpactReportDAO.class) {   // wrong class
```

This means that concurrent creation of `IncidentReportDAO` and `ImpactReportDAO` singletons share the same lock object, creating unintended lock coupling. While this does not introduce a security vulnerability directly, it is a correctness defect that could cause lock contention between unrelated DAO initializations and would cause confusion for developers maintaining the locking logic.

**Risk:**
Informational / correctness. Not a security finding.

**Recommendation:**
Change the synchronized class reference to `IncidentReportDAO.class`.

---

## Finding Count

| Severity | Count |
|----------|-------|
| CRITICAL | 0 |
| HIGH     | 3 |
| MEDIUM   | 4 |
| LOW      | 3 |
| INFO     | 3 |
| **Total**| **13** |
