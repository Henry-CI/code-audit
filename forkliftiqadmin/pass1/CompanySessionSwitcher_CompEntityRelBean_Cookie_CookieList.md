# Pass 1 Audit — CompanySessionSwitcher / CompEntityRelBean / Cookie / CookieList

**Files:**
- `src/main/java/com/util/CompanySessionSwitcher.java`
- `src/main/java/com/bean/CompEntityRelBean.java`
- `src/main/java/com/json/Cookie.java`
- `src/main/java/com/json/CookieList.java`

**Date:** 2026-02-26

---

## Summary

These four files span three distinct functional areas of the application:

**CompanySessionSwitcher.java** is a utility class that overwrites all company-related session attributes after a company switch. It is called from two callers: `LoginAction` (at login time) and `SwitchCompanyAction` (when an authenticated super-admin or dealer switches context to another company). This is the highest-risk file in the batch. The switcher itself contains no authorization logic — it accepts a pre-vetted `CompanyBean` and blindly trusts it. The authorization work must therefore happen entirely in the caller (`SwitchCompanyAction`). Review of that caller reveals that the authorization check is present but has a NullPointerException flaw in unboxing and a silent no-op switch behavior, both of which are detailed below.

**CompEntityRelBean.java** is a plain data-transfer object (DTO) carrying five `String` fields (`id`, `comp_id`, `entity_id`, `entityname`, `compname`). It contains no logic and no annotations. The security risk from this file is entirely contingent on how its callers use it; however, the class itself exposes no validation, no type safety for IDs, and no protection against population from untrusted input. Because no callers were found in the codebase at the time of audit, the class appears to be an orphan DTO — a low-severity concern around dead code and data integrity.

**Cookie.java** and **CookieList.java** are vendored copies of the 2010-era `org.json` cookie helper utilities, relocated to the `com.json` package. They provide cookie-string-to-JSONObject conversion utilities. Analysis of the codebase confirms that `com.json.Cookie` and `com.json.CookieList` are **not imported or called anywhere** in the application's own code. The `Cookie.unescape` method is called only from within `CookieList.java` itself. The `javax.servlet.http.Cookie` class is used in actual cookie handling. These files are inert vendored code and carry low direct risk, but their presence introduces unnecessary attack surface and maintenance confusion.

**Overall risk level: HIGH**, driven primarily by the NullPointerException-via-unboxing vulnerability in `SwitchCompanyAction` that can be triggered against `CompanySessionSwitcher` by a regular (non-admin, non-dealer) authenticated user.

---

## Findings

---

### HIGH: NullPointerException / Application Crash via Unboxing of Unchecked Session Attributes in SwitchCompanyAction

**File:** `SwitchCompanyAction.java` (lines 27–31) — direct caller of `CompanySessionSwitcher`

**Description:**
`SwitchCompanyAction` retrieves `isSuperAdmin` and `isDealerLogin` from the session as `Boolean` (boxed) objects and immediately unboxes them in a conditional expression:

```java
Boolean isSuperAdmin = (Boolean) session.getAttribute("isSuperAdmin");
Boolean isDealerLogin = (Boolean) session.getAttribute("isDealerLogin");
...
if (!isSuperAdmin && !isDealerLogin) {
```

If either session attribute is `null` — which can happen if the session was created by a partial or tampered login flow, or if session attributes are cleared by another action — the unboxing of a null `Boolean` to a primitive `boolean` throws a `NullPointerException`. This crashes the request. In Struts 1.x, uncaught exceptions from `Action.execute()` typically result in a 500 response, which may expose stack traces depending on server configuration.

`PreFlightActionServlet` only checks that `sessCompId != null`. It does not guarantee that `isSuperAdmin` or `isDealerLogin` are present. A user with a valid `sessCompId` session attribute but absent role attributes (achievable through session manipulation or unusual login paths) can reliably crash this action.

**Risk:**
- Authenticated denial-of-service against the company-switch endpoint.
- Potential information disclosure via stack trace if error handling is not hardened.
- If a future code path sets `sessCompId` without setting the role attributes, this becomes exploitable without prior admin access.

**Recommendation:**
Replace unboxed Boolean comparisons with null-safe checks:
```java
boolean isSuperAdmin = Boolean.TRUE.equals(session.getAttribute("isSuperAdmin"));
boolean isDealerLogin = Boolean.TRUE.equals(session.getAttribute("isDealerLogin"));
```
Apply the same pattern to all session attribute reads that are unboxed to primitives throughout the application.

---

### HIGH: Silent No-Op on Invalid Company Switch — No User Feedback, No Audit Log

**File:** `SwitchCompanyAction.java` (lines 35–38) — direct caller of `CompanySessionSwitcher`

**Description:**
The company-switch authorization pattern is a loop that checks whether the requested company ID (`loginActionForm.getCurrentCompany()`) is in the list of companies accessible to the current user:

```java
List<CompanyBean> companies = LoginDAO.getCompanies(isSuperAdmin, isDealerLogin, loggedInCompanyId);
for (CompanyBean company : companies)
    if (company.getId().equals(loginActionForm.getCurrentCompany()))
        CompanySessionSwitcher.UpdateCompanySessionAttributes(company, request, session);
```

If the requested company ID is not in the authorized list, the loop completes without updating the session — but the action proceeds to `successAdmin` regardless. This means:

1. The user's session is **silently left in its prior state** rather than receiving an explicit rejection. While this prevents unauthorized company access, it creates a confusing UX and, more importantly, produces no audit log entry indicating that an unauthorized switch attempt was made.
2. There is no `break` or `return` after the match, so if (due to data anomaly) a company appears multiple times in the list, `UpdateCompanySessionAttributes` is called multiple times in the same request, wasting database calls and potentially leading to inconsistent intermediate session state.
3. The requested company ID comes from the Struts form (`SwitchCompanyActionForm.currentCompany`), which is a raw, user-controlled `String`. No type validation (e.g., confirming it is a numeric integer) is performed before comparison against database-sourced IDs.

**Risk:**
- Failed unauthorized company-switch attempts are not logged, removing the ability to detect probing/enumeration attacks against company IDs.
- Repeated calls to `UpdateCompanySessionAttributes` per request may trigger multiple DB round-trips and can produce a corrupted `arrUnit` or other session cache if the method is not idempotent.

**Recommendation:**
- Add an explicit authorization-failure log entry (at WARN level) when the requested company is not found in the authorized list, including the requesting user ID and requested company ID.
- Return on the first match using `break` after the `UpdateCompanySessionAttributes` call.
- Validate that `currentCompany` is a non-null, non-empty, numeric string before use.
- Consider returning an explicit `failure` forward instead of `successAdmin` when no matching company is found.

---

### MEDIUM: No Session Invalidation and Re-Creation on Company Switch (Session Fixation Risk)

**File:** `CompanySessionSwitcher.java` (lines 27–44) and `SwitchCompanyAction.java` (line 25)

**Description:**
When a user switches company context, `UpdateCompanySessionAttributes` overwrites all company-related session attributes on the **existing session**. The session ID does not change. The same pattern occurs at login time in `LoginAction`: the session is obtained with `request.getSession(false)` (no new session is created at login), and then populated with identity and company attributes.

This means:
- The session ID in use after a company switch is the same ID that was valid before the switch. An attacker who obtained the old session ID (through network sniffing, log exposure, or referrer leakage) retains access to the elevated post-switch context.
- At login, if an attacker can plant a known session ID before authentication (classic session fixation), the session they control will be promoted to a fully authenticated company-admin session without the ID changing.

`PreFlightActionServlet` only validates `sessCompId != null` — it does not verify any session integrity token or check whether the session was legitimately created by a login event.

**Risk:**
- Session fixation at login: an attacker pre-seeds a session, victim logs in, attacker's known session ID now has full access.
- Post-switch session hijacking if the pre-switch session ID is compromised.

**Recommendation:**
- Call `session.invalidate()` followed by `request.getSession(true)` at login time, before writing any authenticated session attributes. Copy only necessary pre-login attributes (e.g., locale, ad list) to the new session.
- Consider issuing a new session ID on company switch as well, particularly when switching from a lower-privilege company context to a higher-privilege one (e.g., from a sub-company to a dealer parent).

---

### MEDIUM: CompanySessionSwitcher Performs No Input Validation on CompanyBean Fields Before Session Write

**File:** `CompanySessionSwitcher.java` (lines 21–44)

**Description:**
`UpdateCompanySessionAttributes` receives a `CompanyBean` that has already been fetched from the database, so under normal flow the data is trusted. However, the method writes multiple fields to the session and request without any null-checks or type validation:

- `Integer.parseInt(timezone)` at line 26 will throw `NumberFormatException` if `company.getTimezone()` is null or non-numeric (e.g., if a company record is misconfigured in the database). This exception propagates up as an unhandled `Exception` from the method.
- `Long.valueOf(comp_id)` at lines 39 and 41 will throw `NumberFormatException` for the same reason.
- There is no null-check on `tzone` (the result of `TimezoneDAO.getTimezone(...)`) before accessing `tzone.getId()` and `tzone.getZone()`. If the timezone ID does not exist in the reference table, `tzone` may be null, causing a NullPointerException.

Because `UpdateCompanySessionAttributes` is `public static` and accepts any `CompanyBean`, a future caller that constructs a `CompanyBean` from untrusted input (e.g., an API layer) could trigger these failures.

**Risk:**
- Misconfigured company records cause unhandled runtime exceptions, resulting in a broken session state or 500 error for the affected user.
- If a partial session write occurs (some attributes set before the exception), the session may be left in an inconsistent state that bypasses the `sessCompId != null` check in `PreFlightActionServlet`.

**Recommendation:**
- Validate that `timezone` is a non-null, parseable integer before calling `Integer.parseInt`.
- Add a null-check on the returned `TimezoneBean` with a meaningful exception or fallback.
- Add a null-check on `comp_id` before calling `Long.valueOf`.
- Alternatively, wrap the entire method body in a try-catch that ensures the session is not left partially written (e.g., by rolling back attribute changes on failure, or by only writing attributes after all computations succeed).

---

### MEDIUM: Dual Redundant Session Attributes for Current Company (`sessCompId` and `currentCompany`)

**File:** `CompanySessionSwitcher.java` (lines 27–29)

**Description:**
The method sets two separate session attributes to the same value:

```java
session.setAttribute("sessCompId", comp_id);
session.setAttribute("currentCompany", comp_id);
```

`sessCompId` is the attribute checked by `PreFlightActionServlet` as the authentication gate. `currentCompany` appears to be used by some JSP or action code. Because these are set together in this method, they should always be in sync. However, if any code path sets `currentCompany` without calling this method (or vice versa), the two attributes can diverge, creating an inconsistency between the security gate value and the operational value. Divergence could allow a user to manipulate `currentCompany` to a different company while `sessCompId` remains valid, bypassing authorization on features that check only `currentCompany`.

**Risk:**
- If any code path writes `currentCompany` independently of `sessCompId`, authorization checks relying on `currentCompany` become inconsistent with the auth gate.
- Confusion between attribute names for future developers increases the likelihood of such a divergence being introduced.

**Recommendation:**
- Consolidate to a single canonical attribute name for the current company ID. Audit all usages of both `sessCompId` and `currentCompany` across JSPs and action classes to identify any location that writes one without the other.
- Use only `sessCompId` as the authoritative company identifier throughout the codebase.

---

### LOW: CompEntityRelBean — No Input Validation, String-Typed IDs, No Usage Found

**File:** `CompEntityRelBean.java` (lines 1–43)

**Description:**
`CompEntityRelBean` is a plain Java bean with five `String` fields: `id`, `comp_id`, `entity_id`, `entityname`, and `compname`. All fields use `String` rather than typed numeric identifiers for what appear to be database primary/foreign keys. There is no validation in the setters, no `@NotNull` or size annotations, and no `equals`/`hashCode` implementation.

A search of the entire codebase found no usages of this class outside its own file. It is an orphan DTO.

**Risk:**
- Dead code increases the maintenance burden and creates ambiguity about what data model this class represents.
- If the class is brought into use in the future without adding validation, numeric IDs stored as `String` could be used in string comparisons where integer comparisons are intended, or concatenated into SQL without parameterization.
- Lack of `equals`/`hashCode` means instances cannot be reliably used in collections.

**Recommendation:**
- If the class is unused, remove it to reduce dead code.
- If it is intended for future use, type the ID fields as `Long` or `Integer`, add validation annotations, and implement `equals`/`hashCode` based on the primary key.

---

### LOW: Vendored 2010-Era `org.json` Cookie Utilities Are Unused Dead Code

**File:** `Cookie.java` (all lines), `CookieList.java` (all lines)

**Description:**
Both files are verbatim copies of the 2010-12-24 version of the `org.json` cookie helper classes, relocated to the `com.json` package. A search of the entire codebase confirms that neither class is imported or called from any application code. The only calls to `Cookie.unescape` and `Cookie.escape` are within `CookieList.java` itself. Actual HTTP cookie handling in the application uses `javax.servlet.http.Cookie` directly.

The `Cookie.unescape` method (lines 150–168 of `Cookie.java`) deserves specific note: it performs `%hh` percent-decoding using a character-by-character loop. The decoding produces raw `char` values and does not account for multi-byte UTF-8 sequences or multi-byte Unicode characters. This is a known limitation of the 2010-era org.json implementation. If the method were ever called on cookie values containing multi-byte-encoded characters (e.g., `%C3%A9` for `é`), the result would be a broken two-character string rather than a single character. However, since the method is not called from application code, this is not currently exploitable.

**Risk:**
- Dead code that could be mistakenly used in the future, with the character-encoding limitation silently producing incorrect unescaping.
- The org.json 2010-era code base contains historical issues tracked in later library versions; vendoring prevents receiving upstream fixes.
- The `Cookie.toString(JSONObject)` method does not set `HttpOnly` or `SameSite` attributes, meaning any cookie serialized through this path would lack those security attributes.

**Recommendation:**
- Remove `Cookie.java` and `CookieList.java` (and any other unreferenced files in the `com.json` package) if they are confirmed to be unused.
- If cookie-to-JSON conversion is needed, use a current, maintained JSON library dependency via Maven rather than vendored 2010-era code.

---

### LOW: `Cookie.escape` Does Not Escape `HttpOnly`, `SameSite`, or `\r\n` Characters

**File:** `Cookie.java` (lines 47–63, 118–140)

**Description:**
The `escape` method encodes `+`, `%`, `=`, `;`, and control characters below ASCII 32. The `toString(JSONObject)` method constructs a cookie header string from a JSONObject. This method does not escape or validate the `expires` field value (line 126: `sb.append(jo.getString("expires"))`), which is appended raw without passing through `escape`. An attacker who could control the `expires` value in the JSONObject could inject `\r\n` sequences into the cookie header, enabling HTTP response splitting. Additionally, `toString` does not emit `HttpOnly` or `SameSite` attributes even when constructing security-sensitive cookies.

Because this class is not used in application code, the risk is theoretical but should be noted for any future adoption.

**Risk:**
- If `Cookie.toString` were ever used for response-header cookie construction with user-controlled data, the unescaped `expires` field could enable HTTP response splitting.
- Cookies constructed via this utility would lack `HttpOnly` and `SameSite` protections.

**Recommendation:**
- Remove the class (preferred, per the previous finding).
- If retained, apply `escape()` to the `expires` value and add `HttpOnly` and `SameSite=Strict` (or `Lax`) to the emitted cookie string.

---

### INFO: `CompanySessionSwitcher` Method Name Violates Java Naming Conventions

**File:** `CompanySessionSwitcher.java` (line 17)

**Description:**
The method is named `UpdateCompanySessionAttributes` with an uppercase first letter, violating the Java convention that method names begin with a lowercase letter. This is a code quality issue, not a security issue, but it suggests the class was written without code review and may indicate broader quality gaps in the utility layer.

**Recommendation:**
Rename to `updateCompanySessionAttributes` and update all callers accordingly. Apply a checkstyle rule to enforce naming conventions.

---

### INFO: `LoginDAO.checkLogin` Is Dead Code — Login Now Delegates to Cognito

**File:** `LoginDAO.java` (lines 47–57) — context for `CompanySessionSwitcher` call chain

**Description:**
`LoginAction` now authenticates via a Cognito REST service (`RestClientService.authenticationRequest`). The local `LoginDAO.checkLogin` method, which verifies credentials against an MD5-hashed password column, appears to no longer be called from the login flow. If `checkLogin` is still reachable from any other path, it represents a secondary authentication bypass risk (MD5 is cryptographically broken). This is noted here as context for the `CompanySessionSwitcher` call chain review.

**Recommendation:**
Confirm whether `LoginDAO.checkLogin` is called anywhere. If not, remove it. If it is reachable, replace MD5 with bcrypt or Argon2.

---

## Finding Count

| Severity | Count |
|----------|-------|
| CRITICAL | 0 |
| HIGH     | 2 |
| MEDIUM   | 3 |
| LOW      | 3 |
| INFO     | 2 |
| **Total**| **10** |
