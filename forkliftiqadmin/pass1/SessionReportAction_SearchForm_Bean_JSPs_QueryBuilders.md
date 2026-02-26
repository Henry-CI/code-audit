# Security Audit Report: SessionReport Feature
**Date:** 2026-02-26
**Auditor:** Automated Pass 1
**Branch:** master
**Scope:** SessionReportAction, SessionReportSearchForm, SessionReportBean, dealer/sessionReport.jsp, reports/sessionreport.jsp, SessionsByCompanyIdQuery, SessionUnitFilter, SessionUnitFilterHandler

---

## Files Audited

| # | File |
|---|------|
| 1 | `src/main/java/com/action/SessionReportAction.java` |
| 2 | `src/main/java/com/actionform/SessionReportSearchForm.java` |
| 3 | `src/main/java/com/bean/SessionReportBean.java` |
| 4 | `src/main/webapp/html-jsp/dealer/sessionReport.jsp` |
| 5 | `src/main/webapp/html-jsp/reports/sessionreport.jsp` |
| 6 | `src/main/java/com/querybuilder/session/SessionsByCompanyIdQuery.java` |
| 7 | `src/main/java/com/querybuilder/filters/SessionUnitFilter.java` |
| 8 | `src/main/java/com/querybuilder/filters/SessionUnitFilterHandler.java` |

---

## Findings

---

### HIGH: Missing dealer role check in DealerSessionReportAction

**File:** `src/main/java/com/action/DealerSessionReportAction.java` (lines 17–41)

**Description:**
`DealerSessionReportAction` — the action mapped to `/dealerSessionReport` — never verifies that the authenticated user actually holds the dealer role (`isDealerLogin` or `ROLE_DEALER`). The only gate applied is the generic `PreFlightActionServlet` check that `sessCompId != null`. Any authenticated non-dealer company user who knows the URL `/dealerSessionReport.do` can invoke this action and receive session-report data scoped to their own `sessCompId`.

The pattern used elsewhere in the codebase (e.g., `SwitchCompanyAction.java` line 31) makes the expected check explicit:

```java
// SwitchCompanyAction — correct pattern
Boolean isDealerLogin = (Boolean) session.getAttribute("isDealerLogin");
if (!isSuperAdmin && !isDealerLogin) {
    return mapping.findForward("failure");
}
```

`DealerSessionReportAction` performs no equivalent check:

```java
public ActionForward execute(...) {
    HttpSession session = request.getSession(false);
    String sessCompId = (String) session.getAttribute("sessCompId");
    if (sessCompId == null) throw new RuntimeException("Must have valid user logged in here");
    // No isDealerLogin / ROLE_DEALER check — proceeds immediately
    ...
    return mapping.findForward("report");
}
```

Note: The audit scope file `SessionReportAction.java` (the regular, non-dealer action at `/sessionreport.do`) does not itself need a dealer check — it is the standard company-user path. The confirmed missing-role-check defect is in `DealerSessionReportAction`, which is the peer dealer-prefixed action rendered by `dealer/sessionReport.jsp`.

**Risk:**
Any authenticated operator-company user can access the dealer report endpoint, bypassing the intended access segmentation between dealer accounts and their managed sub-companies. Because the data returned is still scoped to `sessCompId`, the direct data exposure is limited to the user's own company; however, the endpoint violates the authorization model and may have different business logic or UI surfaces (e.g., cross-company data aggregation in future iterations) that assume only dealers reach it.

**Recommendation:**
Add an `isDealerLogin` guard at the top of `DealerSessionReportAction.execute()` immediately after retrieving `sessCompId`, mirroring the pattern in `SwitchCompanyAction`:

```java
Boolean isDealerLogin = (Boolean) session.getAttribute("isDealerLogin");
Boolean isSuperAdmin  = (Boolean) session.getAttribute("isSuperAdmin");
if (!Boolean.TRUE.equals(isDealerLogin) && !Boolean.TRUE.equals(isSuperAdmin)) {
    return mapping.findForward("failure");
}
```

---

### HIGH: Reflected XSS via unescaped `start_date` / `end_date` in JavaScript — reports/sessionreport.jsp

**File:** `src/main/webapp/html-jsp/reports/sessionreport.jsp` (lines 99–113)

**Description:**
`start_date` and `end_date` are read directly from the HTTP request via `request.getParameter(...)` and interpolated unescaped into a JavaScript string literal inside a `new Date("...")` constructor. No HTML or JavaScript encoding is applied. The `DateUtil.stringToIsoNoTimezone()` helper performs a date parse-and-reformat, but if the input cannot be parsed it will throw a `NullPointerException` (since `df.format(null)` will fail), or in certain implementations return an unmodified value. Even with the date reformatting, an attacker-controlled value that passes format parsing or exploits edge cases in `SimpleDateFormat` can still break out of the string context.

Vulnerable code:

```jsp
<%
    if (request.getParameter("start_date") != null) {
%>
start_date = new Date("<%= DateUtil.stringToIsoNoTimezone(request.getParameter("start_date"), (String) session.getAttribute("sessDateFormat")) %>")
<%
    }
%>
<%
    if (request.getParameter("end_date") != null) {
%>
end_date = new Date("<%= DateUtil.stringToIsoNoTimezone(request.getParameter("end_date"), (String) session.getAttribute("sessDateFormat")) %>")
<%
    }
%>
```

**Attack vector:** An attacker crafts a GET or POST request to `sessionreport.do` with a `start_date` parameter containing a JavaScript injection payload. Because the form is a plain POST with no CSRF token (see separate finding), the payload can also be delivered via a CSRF-triggered form submission. Even if `DateUtil.stringToIsoNoTimezone()` sanitises the value under the expected date format, format-confusion or null-path behaviour may allow bypass.

Example payload concept:
```
start_date="); alert(document.cookie); new Date("
```

This is the same pattern flagged for `impactReport.jsp` in prior audit findings.

**Risk:**
Reflected XSS allowing arbitrary JavaScript execution in the victim's browser session. An attacker can steal session cookies, perform actions as the victim, or redirect to a phishing page.

**Recommendation:**
1. Do not interpolate user-controlled values directly into JavaScript string literals in JSPs.
2. Server-side: compute the date value entirely in Java, store it as a request attribute, and expose it to the page via a safe mechanism (e.g., a JSON-encoded request attribute written with proper escaping).
3. If inline scriptlets cannot be avoided, use `ESAPI.encoder().encodeForJavaScript(...)` or equivalent to escape the value before interpolation.
4. As a defence-in-depth measure, set a `Content-Security-Policy` header that blocks inline scripts.

---

### HIGH: Reflected XSS via unescaped `start_date` / `end_date` in JavaScript — dealer/sessionReport.jsp

**File:** `src/main/webapp/html-jsp/dealer/sessionReport.jsp` (lines 99–113)

**Description:**
Identical vulnerability to the finding above. `dealer/sessionReport.jsp` is a near-exact copy of `reports/sessionreport.jsp` and contains the same unescaped scriptlet interpolation of `start_date` and `end_date` into a JavaScript `new Date("...")` call.

Vulnerable code (identical pattern):

```jsp
start_date = new Date("<%= DateUtil.stringToIsoNoTimezone(request.getParameter("start_date"), (String) session.getAttribute("sessDateFormat")) %>")
...
end_date = new Date("<%= DateUtil.stringToIsoNoTimezone(request.getParameter("end_date"), (String) session.getAttribute("sessDateFormat")) %>")
```

**Risk:** Same as the previous finding — reflected XSS in the dealer-facing session report page.

**Recommendation:** Same as above. Both JSP files must be remediated; they share duplicated logic and should ideally be refactored into a single template to prevent this class of divergence.

---

### MEDIUM: No CSRF protection on session report search forms (both JSPs)

**File:** `src/main/webapp/html-jsp/reports/sessionreport.jsp` (line 21); `src/main/webapp/html-jsp/dealer/sessionReport.jsp` (line 21)

**Description:**
Both session report forms use `html:form` with `method="POST"` and carry no synchronizer token. Struts 1.x provides a built-in CSRF token mechanism (`saveToken()` / `isTokenValid()`) but neither `SessionReportAction` nor `DealerSessionReportAction` calls `saveToken()` on GET, nor calls `isTokenValid()` on POST. No custom CSRF filter was found in the codebase (no matches for `saveToken`, `isTokenValid`, or `synchronizer` in any action or filter class).

```jsp
<!-- No token field present -->
<html:form action="sessionreport.do" method="POST" styleClass="checklist_from">
```

**Risk:**
A CSRF attack against the session report action itself is low-impact because the action only reads and displays data — it does not mutate state. However, the combination of this form being submittable cross-origin AND the XSS findings above means a CSRF-triggered POST can be used to deliver the XSS payload (the reflected XSS in the `new Date(...)` constructor fires on POST response). This elevates the CSRF finding as an XSS delivery vector even though the action itself is read-only.

**Recommendation:**
1. Call `saveToken(request)` in the initial (GET) render path of both actions, and call `isTokenValid(request, true)` at the start of the POST-handling path; return an error forward if the token is invalid.
2. Consider a servlet filter or Struts plugin to enforce CSRF tokens application-wide.
3. As a partial mitigation, verify the `Referer` / `Origin` header matches the application's own host.

---

### MEDIUM: `vehicle_id` filter is not validated against the authenticated company — potential cross-company IDOR via filter parameter

**File:** `src/main/java/com/actionform/SessionReportSearchForm.java` (lines 17, 25); `src/main/java/com/querybuilder/session/SessionsByCompanyIdQuery.java` (lines 23–27, 40–48)

**Description:**
A user can submit any arbitrary `vehicle_id` (Long) value in the POST body. `SessionReportSearchForm` accepts it without validation:

```java
private Long vehicle_id;
...
.vehicleId(this.vehicle_id == null || this.vehicle_id == 0 ? null : this.vehicle_id)
```

`SessionsByCompanyIdQuery` then passes this value straight to `SessionUnitFilterHandler` which appends `AND unit_id = ?` to the WHERE clause:

```java
// SessionsByCompanyIdQuery.getQuery()
query.append("from v_sessions where (unit_owner_company_id = ? or unit_assigned_company_id = ?)");
...
new SessionUnitFilterHandler(filter, "unit_id")
```

The WHERE clause structure is:
```sql
WHERE (unit_owner_company_id = ? OR unit_assigned_company_id = ?)
AND unit_id = ?
```

The company-ID anchor (`unit_owner_company_id = ?`) is present, so the query does enforce that results belong to the authenticated company. **However**, the `vehicles` dropdown populated by `UnitDAO.getAllUnitsByCompanyId(compId)` scopes the UI, but the submitted `vehicle_id` is not re-validated server-side against that company-scoped list. An attacker who bypasses the UI dropdown (e.g., by modifying the POST parameter) and submits a `vehicle_id` belonging to a different company will get zero results (the company filter blocks cross-company rows), so there is no direct data leakage.

The residual risk is an **oracle attack**: by iterating `vehicle_id` values an attacker can enumerate which unit IDs exist globally (a non-empty result set implies the submitted unit_id belongs to the authenticated company; an empty result set is ambiguous but repeated probing could leak existence of IDs). More importantly, if the `v_sessions` view or the `unit_assigned_company_id` logic has any edge case where a unit is temporarily visible to a second company, the absence of server-side vehicle ownership validation provides no safety net.

**Risk:**
Low direct data leakage due to the company-ID WHERE clause. Elevated oracle/enumeration risk and no defensive validation should the view logic change. Violates the principle of server-side authorisation of all user-supplied IDs.

**Recommendation:**
Before using `vehicle_id` in the query, verify that the submitted ID belongs to the authenticated company:
```java
// In SessionReportAction / DealerSessionReportAction, before building the filter:
if (sessionReportFilter.getVehicle_id() != null) {
    List<UnitBean> ownedUnits = UnitDAO.getAllUnitsByCompanyId(compId);
    boolean validUnit = ownedUnits.stream()
        .anyMatch(u -> u.getId().equals(sessionReportFilter.getVehicle_id()));
    if (!validUnit) { /* reject or clear the filter */ }
}
```
Alternatively, add a JOIN or sub-select in `SessionsByCompanyIdQuery` that ties `unit_id` back to the company:
```sql
AND unit_id IN (SELECT id FROM units WHERE owner_company_id = ?)
```

---

### MEDIUM: `driver_id` filter is not validated against the authenticated company — same IDOR pattern

**File:** `src/main/java/com/actionform/SessionReportSearchForm.java` (line 18); `src/main/java/com/querybuilder/session/SessionsByCompanyIdQuery.java` (line 27)

**Description:**
The same issue applies to `driver_id`. The value is accepted from the POST body, placed into the filter bean's `driverId` field, and passed to `SessionDriverFilterHandler` which appends `AND driver_id = ?`. There is no server-side check that the supplied `driver_id` belongs to the authenticated company. The company-ID WHERE clause again limits what rows can be returned, but no ownership validation of the `driver_id` value itself is performed.

```java
private Long driver_id;
...
.driverId(this.driver_id == null || this.driver_id == 0 ? null : this.driver_id)
```

**Risk:** Same as vehicle_id: low direct leakage, moderate enumeration/oracle risk, and absence of defence in depth.

**Recommendation:** Mirror the vehicle_id recommendation. Validate that `driver_id` is in the set returned by `DriverDAO.getAllDriver(sessCompId, true)` before using it as a query filter.

---

### LOW: Missing space before `ORDER BY` clause in `SessionsByCompanyIdQuery.getQuery()` — latent SQL syntax error

**File:** `src/main/java/com/querybuilder/session/SessionsByCompanyIdQuery.java` (lines 42–46)

**Description:**
The query builder appends the `ORDER BY` clause without a leading space:

```java
query.append("from v_sessions where (unit_owner_company_id = ? or unit_assigned_company_id = ?)");

for (FilterHandler handler : filterHandlers) query.append(handler.getQueryFilter());

query.append("order by session_start_time desc");
```

When all three filter handlers return an empty string (i.e., no vehicle filter, no driver filter, and no date filter is active), the constructed SQL becomes:

```sql
select ... from v_sessions where (unit_owner_company_id = ? or unit_assigned_company_id = ?)order by session_start_time desc
```

The missing space between `)` and `order` produces an invalid SQL token `?)order`. Most JDBC drivers will reject this with a `SQLException`. The issue may be masked in practice because the date filter (`DateBetweenFilterHandler`) always returns a non-empty fragment when `start` or `end` are non-null — but since `SessionFilterBean.start()` defaults to `Calendar.getInstance().getTime()` (the current time) when `startDate` is null, this means a date clause is nearly always injected. The defect is therefore currently latent but may surface under specific conditions (e.g., if `DateBetweenFilterHandler.ignoreFilter()` is triggered, which requires `filter == null` — currently not reachable through normal paths but could become reachable under refactoring).

**Risk:** Potential `SQLException` / 500 error causing denial of service for affected requests if the filter combination is reached.

**Recommendation:** Add a leading space to the `ORDER BY` append:

```java
query.append(" order by session_start_time desc");
```

---

### LOW: `SessionReportBean` exposes a mutable `List` reference via Lombok `@Data` getter

**File:** `src/main/java/com/bean/SessionReportBean.java` (lines 14–18)

**Description:**
`SessionReportBean` is annotated with `@Data` (Lombok), which generates a `getSessions()` method returning the internal `ArrayList<SessionBean>` directly. Any caller holding the bean can mutate the list in place:

```java
@Data
public class SessionReportBean implements Serializable {
    private List<SessionBean> sessions = new ArrayList<>();
}
```

While this is not a direct external security vulnerability (the bean is only set as a request attribute and consumed by the JSP's `<logic:iterate>`), it is a data integrity concern in a multi-threaded servlet environment if the same bean instance were ever shared or cached.

**Risk:** Low — no direct external exploit vector given current usage pattern; however, mutable shared state in beans is a code quality risk.

**Recommendation:** Return a defensive copy in the getter, or annotate with `@Getter(onMethod_ = {@JsonIgnore})` and provide an unmodifiable view. Alternatively, ensure the bean is constructed fresh per request (it currently is).

---

### INFO: `SessionReportSearchForm` does not validate or sanitise `start_date` / `end_date` format before date parsing

**File:** `src/main/java/com/actionform/SessionReportSearchForm.java` (lines 27–28)

**Description:**
`start_date` and `end_date` are passed to `DateUtil.stringToUTCDate(this.start_date, dateFormat)` without any length check, character whitelist, or format pre-validation. If `stringToDate` fails to parse the value it catches `ParseException` and returns `null`, effectively silently ignoring an invalid or malicious value. This is not exploitable for SQL injection (the resulting `null` simply skips the date filter) but it means malformed input is silently dropped rather than rejected.

```java
.startDate(this.start_date == null ? null : DateUtil.stringToUTCDate(this.start_date, dateFormat))
.endDate(this.end_date == null ? null : DateUtil.stringToUTCDate(this.end_date, dateFormat))
```

**Risk:** Informational — silent failure may mask data integrity issues or user errors; not directly exploitable.

**Recommendation:** Add input validation in `getSessionReportFilter()` (or in a Struts `validate()` method on the form): reject values that do not conform to the expected date format and surface an `ActionError` to the user rather than silently discarding them.

---

### INFO: `bean:write` tags in both JSPs use default HTML-escaping (safe)

**File:** `src/main/webapp/html-jsp/reports/sessionreport.jsp` (lines 81–84); `src/main/webapp/html-jsp/dealer/sessionReport.jsp` (lines 81–84)

**Description:**
All four `<bean:write>` tags in the session report table body use the default `filter="true"` (Struts default), which HTML-encodes output:

```jsp
<td><bean:write property="unitName" name="sessionEntry"/></td>
<td><bean:write property="driverName" name="sessionEntry"/></td>
<td><bean:write property="startTime" name="sessionEntry"/></td>
<td><bean:write property="finishTime" name="sessionEntry"/></td>
```

No `filter="false"` attributes are present. This means stored XSS via unit name, driver name, or date/time fields rendered in the table is mitigated at the JSP layer.

**Risk:** None — this is a positive finding confirming safe rendering practice for table data.

**Recommendation:** No action required. Document this as a correctly implemented control for future maintainers.

---

### INFO: Query tenant isolation relies on `v_sessions` view definition for `unit_assigned_company_id`

**File:** `src/main/java/com/querybuilder/session/SessionsByCompanyIdQuery.java` (line 42)

**Description:**
The tenant isolation WHERE clause is:

```sql
WHERE (unit_owner_company_id = ? OR unit_assigned_company_id = ?)
```

The security of multi-tenant data isolation depends critically on the correctness of the `v_sessions` database view — specifically that `unit_assigned_company_id` is populated accurately and cannot be manipulated by tenant-controlled data. This is outside the Java codebase scope of this audit but should be verified in a database-layer review.

**Risk:** Informational — no Java-layer defect found; DB schema review recommended.

**Recommendation:** Include `v_sessions` view definition in a subsequent database audit pass to confirm that `unit_assigned_company_id` cannot be influenced by user-controlled input.

---

## Summary

| Finding | Severity | File(s) |
|---------|----------|---------|
| Missing dealer role check in DealerSessionReportAction | HIGH | DealerSessionReportAction.java |
| Reflected XSS via `start_date`/`end_date` in JS — reports/sessionreport.jsp | HIGH | reports/sessionreport.jsp |
| Reflected XSS via `start_date`/`end_date` in JS — dealer/sessionReport.jsp | HIGH | dealer/sessionReport.jsp |
| No CSRF protection on session report forms | MEDIUM | both JSPs |
| `vehicle_id` not validated against authenticated company | MEDIUM | SessionReportSearchForm.java, SessionsByCompanyIdQuery.java |
| `driver_id` not validated against authenticated company | MEDIUM | SessionReportSearchForm.java, SessionsByCompanyIdQuery.java |
| Missing space before ORDER BY — latent SQL syntax error | LOW | SessionsByCompanyIdQuery.java |
| Mutable List exposed by SessionReportBean @Data getter | LOW | SessionReportBean.java |
| Silent discard of invalid date input in form | INFO | SessionReportSearchForm.java |
| `bean:write` uses safe HTML-escaping (positive) | INFO | both JSPs |
| Tenant isolation relies on v_sessions view correctness | INFO | SessionsByCompanyIdQuery.java |

**CRITICAL: 0 / HIGH: 3 / MEDIUM: 3 / LOW: 2 / INFO: 3**
