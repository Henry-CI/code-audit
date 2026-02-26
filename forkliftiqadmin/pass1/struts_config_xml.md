# Security Audit: struts-config.xml
**Application:** forkliftiqadmin (FleetIQ System)
**File:** `/src/main/webapp/WEB-INF/struts-config.xml`
**Date:** 2026-02-26
**Auditor:** Automated Pass 1
**Framework:** Apache Struts 1.3.10 on Tomcat

---

## 1. Complete Action Inventory

All action mappings extracted from `struts-config.xml`. The "Validate" column reflects the explicit `validate` attribute or the Struts 1.x default (which is `false` when no `validate` attribute is set AND no `name` attribute links a form bean; for actions that DO name a form bean but omit `validate`, the Struts 1.x default is also `false`).

The "Validation.xml Entry" column indicates whether a matching `<form>` element exists in `validation.xml` that would actually run field-level validators.

| # | Path | Action Class | Form Bean | validate= | validation.xml Entry | Auth-Excluded |
|---|------|--------------|-----------|-----------|----------------------|---------------|
| 1 | `/swithLanguage` | `com.action.SwitchLanguageAction` | none | (default=false) | No | Yes |
| 2 | `/welcome` | `com.action.WelcomeAction` | none | (default=false) | No | Yes |
| 3 | `/expire` | `com.action.ExpireAction` | none | (default=false) | No | Yes |
| 4 | `/login` | `com.action.LoginAction` | `loginActionForm` | **true** | **Yes** (`loginActionForm`) | Yes |
| 5 | `/switchCompany` | `com.action.SwitchCompanyAction` | `switchCompanyActionForm` | **true** | No | No |
| 6 | `/privacy` | `com.action.PrivacyAction` | none | (default=false) | No | No |
| 7 | `/search` | `com.action.SearchAction` | `searchActionForm` | **true** | No | No |
| 8 | `/goResetPass` | `com.action.GoResetPassAction` | none | (default=false) | No | Yes |
| 9 | `/resetpass` | `com.action.ResetPasswordAction` | none | (default=false) | No | Yes |
| 10 | `/register` | `com.action.RegisterAction` | `registerActionForm` | **true** | No | No |
| 11 | `/switchRegister` | `com.action.SwitchRegisterAction` | none | (default=false) | No | Yes |
| 12 | `/adminRegister` | `com.action.AdminRegisterAction` | `adminRegActionForm` (`AdminRegisterActionForm`) | **true** | **Yes** (`adminRegisterActionForm`) | Yes |
| 13 | `/sendMail` | `com.action.AdminSendMailAction` | `sendMailForm` | **true** | No | No |
| 14 | `/fleetcheck` | `com.action.FleetcheckAction` | `fleetcheckActionForm` | (default=false) | No | No |
| 15 | `/goSerach` | `com.action.GoSearchAction` | none | (default=false) | No | No |
| 16 | `/getXml` | `com.action.GetXmlAction` | none | (default=false) | No | No |
| 17 | `/getAjax` | `com.action.GetAjaxAction` | none | (default=false) | No | No |
| 18 | `/getAjaxGPS` | `com.action.GetAjaxAction` | none | (default=false) | No | No |
| 19 | `/logout` | `com.action.LogoutAction` | none | (default=false) | No | Yes |
| 20 | `/adminmenu` | `com.action.AdminMenuAction` | none | (default=false) | No | No |
| 21 | `/admindriver` | `com.action.AdminOperatorAction` | none | (default=false) | No | No |
| 22 | `/adminunit` | `com.action.AdminUnitAction` | none | (default=false) | No | No |
| 23 | `/adminalert` | `com.action.AdminAlertAction` | none | (default=false) | No | No |
| 24 | `/settings` | `com.action.AdminSettingsAction` | `AdminSettingsActionForm` | **false** (explicit) | No | No |
| 25 | `/manufacturers` | `com.action.AdminManufacturersAction` | `AdminManufacturersActionForm` | **false** (explicit) | No | No |
| 26 | `/trainings` | `com.action.AdminTrainingsAction` | `AdminTrainingsActionForm` | **false** (explicit) | No | No |
| 27 | `/adminAlertAdd` | `com.action.AdminAddAlertAction` | `adminAlertActionForm` | **true** | No | No |
| 28 | `/admindriveradd` | `com.action.AdminDriverAddAction` | `adminDriverAddForm` | **true** | No | No |
| 29 | `/admindriveredit` | `com.action.AdminDriverEditAction` | `adminDriverEditForm` | **true** | **Partial** (`AdminDriverEditForm` — note case mismatch) | No |
| 30 | `/admindriverlicencevalidateexist` | `com.action.AdminDriverEditAction` | `adminDriverEditForm` | **true** | **Partial** (same case mismatch) | No |
| 31 | `/adminunitedit` | `com.action.AdminUnitEditAction` | `adminUnitEditForm` | **true** | No | No |
| 32 | `/adminunitassign` | `com.action.AdminUnitAssignAction` | `adminUnitAssignForm` | **true** | No | No |
| 33 | `/unitnameexists` | `com.action.AdminUnitEditAction` | `adminUnitEditForm` | **false** (explicit) | No | No |
| 34 | `/serialnoexists` | `com.action.AdminUnitEditAction` | `adminUnitEditForm` | **false** (explicit) | No | No |
| 35 | `/macaddressexists` | `com.action.AdminUnitEditAction` | `adminUnitEditForm` | **false** (explicit) | No | No |
| 36 | `/assigndatesvalid` | `com.action.AdminUnitAssignAction` | `adminUnitAssignForm` | **false** (explicit) | No | No |
| 37 | `/fleetcheckedit` | `com.action.AdminFleetcheckEditAction` | `adminFleetcheckEditActionForm` | **true** | No | No |
| 38 | `/fleetcheckconf` | `com.action.AdminFleetcheckAction` | `adminFleetcheckActionForm` | **true** | No | No |
| 39 | `/fleetcheckshow` | `com.action.AdminFleetcheckShowAction` | `adminFleetcheckShowActionForm` | **true** | No | No |
| 40 | `/fleetcheckhide` | `com.action.AdminFleetcheckHideAction` | `adminFleetcheckHideActionForm` | **true** | No | No |
| 41 | `/fleetcheckdelete` | `com.action.AdminFleetcheckDeleteAction` | `adminFleetcheckDeleteActionForm` | **true** | No | No |
| 42 | `/dealerconvert` | `com.action.AdminDealerAction` | `adminDealerActionForm` | **true** | No | No |
| 43 | `/mailer` | `com.action.MailerAction` | none | (default=false) | No | **Yes** |
| 44 | `/api` | `com.action.AppAPIAction` | none | (default=false) | No | **Yes** |
| 45 | `/formBuilder` | `com.action.FormBuilderAction` | none | (default=false) | No | No |
| 46 | `/loadbarcode` | `com.action.BarCodeAction` | none | (default=false) | No | **Yes** |
| 47 | `/driverjob` | `com.action.DriverJobDetailsAction` | none | (default=false) | No | No |
| 48 | `/jobdetails` | `com.action.DriverJobDetailsAction` | none | (default=false) | No | No |
| 49 | `/driverjobreq` | `com.action.DriverJobDetailsAction` | `driverJobDetailsActionForm` | **true** | No | No |
| 50 | `/adminunitservice` | `com.action.AdminUnitServiceAction` | `adminUnitServiceForm` | **true** | No | No |
| 51 | `/adminunitimpact` | `com.action.AdminUnitImpactAction` | `adminUnitImpactForm` | **true** | No | No |
| 52 | `/adminunitaccess` | `com.action.AdminUnitAccessAction` | `adminUnitAccessForm` | **true** | No | No |
| 53 | `/preopsreport` | `com.action.PreOpsReportAction` | `preOpsReportSearchForm` | (default=false) | No | No |
| 54 | `/impactreport` | `com.action.ImpactReportAction` | `impactReportSearchForm` | **false** (explicit) | No | No |
| 55 | `/gpsreport` | `com.action.GPSReportAction` | `gpsReportSearchForm` | **false** (explicit) | No | No |
| 56 | `/dealercompanies` | `com.action.DealerCompaniesAction` | `dealerCompanyForm` | **true** | No | No |
| 57 | `/dealercompaniesAdd` | `com.action.DealerCompaniesAction` | none | (default=false) | No | No |
| 58 | `/incidentreport` | `com.action.IncidentReportAction` | `incidentReportSearchForm` | **false** (explicit) | No | No |
| 59 | `/dealerImpactReport` | `com.action.DealerImpactReportAction` | `impactReportSearchForm` | **false** (explicit) | No | No |
| 60 | `/dealerPreOpsReport` | `com.action.DealerPreOpsReportAction` | `preOpsReportSearchForm` | **false** (explicit) | No | No |
| 61 | `/dealerIncidentReport` | `com.action.DealerIncidentReportAction` | `incidentReportSearchForm` | **false** (explicit) | No | No |
| 62 | `/sessionreport` | `com.action.SessionReportAction` | `sessionReportSearchForm` | **false** (explicit) | No | No |
| 63 | `/dealerSessionReport` | `com.action.DealerSessionReportAction` | `sessionReportSearchForm` | **false** (explicit) | No | No |
| 64 | `/calibration` | `com.action.CalibrationAction` | none | (default=false) | No | No |

**Total mappings: 64**

---

## 2. Auth-Excluded Paths — Full List and Risk Assessment

The `excludeFromFilter()` method in `PreFlightActionServlet.java` returns `false` (i.e., skips the session check) for the following paths. Returning `false` means authentication IS NOT REQUIRED.

```java
// PreFlightActionServlet.java lines 100-114
if (path.endsWith("welcome.do"))      return false;   // No session check
if (path.endsWith("adminWelcome.do")) return false;   // No session check — NOT IN struts-config.xml
if (path.endsWith("login.do"))        return false;
if (path.endsWith("logout.do"))       return false;
if (path.endsWith("expire.do"))       return false;
if (path.endsWith("mailer.do"))       return false;
if (path.endsWith("api.do"))          return false;
if (path.endsWith("adminRegister.do"))return false;
if (path.endsWith("switchRegister.do"))return false;
if (path.endsWith("swithLanguage.do")) return false;
if (path.endsWith("resetpass.do"))    return false;
if (path.endsWith("goResetPass.do"))  return false;
if (path.endsWith("loadbarcode.do"))  return false;
if (path.endsWith("uploadfile.do"))   return false;   // NOT IN struts-config.xml — dead exclusion
```

### Auth-Excluded Actions and Risk Summary

| Path | Maps to | Risk Level | Notes |
|------|---------|------------|-------|
| `welcome.do` | `WelcomeAction` | INFO | Benign redirect to login page |
| `login.do` | `LoginAction` | INFO | Required to be public |
| `logout.do` | `LogoutAction` | INFO | Required to be public |
| `expire.do` | `ExpireAction` | INFO | Required to be public |
| `swithLanguage.do` | `SwitchLanguageAction` | LOW | Language selector, no data access |
| `switchRegister.do` | `SwitchRegisterAction` | LOW | Redirects to registration form |
| `goResetPass.do` | `GoResetPassAction` | MEDIUM | Triggers password reset flow via Cognito |
| `resetpass.do` | `ResetPasswordAction` | MEDIUM | Accepts new password + confirmation code |
| `adminRegister.do` | `AdminRegisterAction` | **HIGH** | Creates new company accounts; no auth required |
| `mailer.do` | `MailerAction` | **HIGH** | Triggers email delivery to all subscribed users |
| `api.do` | `AppAPIAction` | **MEDIUM** | Entire API endpoint body is commented out; returns empty response — currently inert but unauthenticated |
| `loadbarcode.do` | `BarCodeAction` | **HIGH** | Accepts barcode data, writes checklist results to database |
| `uploadfile.do` | (no struts-config.xml mapping) | **MEDIUM** | Dead exclusion — path is excluded from auth but no action is mapped; may indicate a removed or forgotten endpoint |
| `adminWelcome.do` | (no struts-config.xml mapping) | LOW | Dead exclusion — no action mapped |

---

## 3. Security Findings

---

### CRITICAL: `adminRegister.do` is Auth-Excluded and Creates Company Accounts

**Description:**
`/adminRegister` (`com.action.AdminRegisterAction`) is explicitly excluded from authentication in `PreFlightActionServlet.excludeFromFilter()`. Any unauthenticated HTTP client can POST to `/adminRegister.do` with `accountAction=register` and create a new top-level company account in the system. The action creates a Cognito user identity, inserts a record into the `company` table via `CompanyDAO.saveCompInfo()`, creates a default subscription record via `SubscriptionDAO.saveDefualtSubscription()`, and sends a confirmation email to the attacker-supplied address. No CAPTCHA, invite token, rate-limiting, or any other anti-abuse mechanism is present in the code.

Furthermore, when `accountAction=add`, the action calls `compDao.saveSubCompInfo(sessCompId, ...)`, which reads `sessCompId` from the session. If an attacker posts `accountAction=add` without a session, this will throw a NullPointerException at line 43 (`session.getAttribute("sessCompId")`), since `request.getSession(false)` may return `null`. However the `register` path is fully exploitable.

The form bean is `adminRegActionForm`, which is declared as type `com.actionform.AdminRegisterActionForm`. The `validation.xml` entry is `adminRegisterActionForm` (matching the form-bean *name* `adminRegisterActionForm`), but the action uses form-bean *name* `adminRegActionForm`. Struts validator looks up the form by the action's `name` attribute (`adminRegActionForm`), which does NOT match the `<form name="adminRegisterActionForm">` entry in `validation.xml`. Therefore **the validator silently skips validation entirely** for this action, even though `validate="true"` is declared.

**Risk:**
- Unauthenticated arbitrary company account creation, enabling unauthorized access to the multi-tenant application.
- Potential to exhaust database or external Cognito quota via automated account registration.
- Confirmation emails will be sent to attacker-controlled addresses, abusing the application's mail infrastructure.
- Data integrity compromise: fabricated companies could be used as staging for lateral movement within the multi-tenant dataset.

**Recommendation:**
1. Remove `adminRegister.do` from the exclusion list in `PreFlightActionServlet`. Self-registration, if required, must be protected by a separate unauthenticated registration flow with an invite token or CAPTCHA.
2. Fix the form-bean name mismatch: rename the action's `name="adminRegActionForm"` to `name="adminRegisterActionForm"` (or add a matching `<form name="adminRegActionForm">` entry in `validation.xml`) so that the declared `validate="true"` actually runs.
3. Add server-side enforcement (rate limiting, CAPTCHA, invite token) to any registration endpoint that must remain public.

---

### CRITICAL: `loadbarcode.do` is Auth-Excluded and Writes Operational Data to the Database

**Description:**
`/loadbarcode` (`com.action.BarCodeAction`) is excluded from authentication. It accepts two HTTP methods:

- `method=barcode` — accepts `serial`, `driver`, `quesIds[]`, `quesAns[]` parameters, looks up a unit record by serial number, resolves the company ID from that record, and calls `FleetcheckAction.saveResult()` to write a forklift checklist result directly to the database. It then triggers `sendFleetCheckAlert()`, which sends alert emails to company contacts.
- `method=loadbarcode` — accepts a raw `data` parameter containing a multi-record barcode dump. It parses the data, reconstructs checklist result objects, and bulk-inserts them via `FleetcheckAction.saveResultBarcode()`.

In both cases, there is no authentication, no CSRF protection, no input validation configured in `struts-config.xml` (no `name` or `validate` attribute on the action), and no server-side business-rule validation visible in the action code. An unauthenticated attacker can:

1. Submit fabricated checklist results for any unit whose serial number they can guess or enumerate.
2. Attribute those results to any driver ID they choose.
3. Trigger alert emails to company contacts for any company in the system.
4. Overwrite or poison historical inspection records, undermining safety audit trails.

**Risk:**
- Falsification of forklift safety inspection records across all tenants in the system.
- Regulatory and liability exposure if falsified records are relied upon for compliance reporting.
- Denial-of-service via flooding the result table or alert email queue.
- No duplicate-check bypass protection: the `checkDuplicateResult()` guard is only on the barcode path, not the `barcode` method path, and it can be defeated by varying the timestamp parameter.

**Recommendation:**
1. Remove `loadbarcode.do` from the authentication exclusion list. If barcode scanners must authenticate machine-to-machine, implement a token-based API authentication scheme (e.g., pre-shared API key validated in the action, or OAuth2 client credentials).
2. Add `validate="true"` and a form bean with server-side validation rules to both barcode action methods.
3. Restrict the `serial` parameter to numeric values and enforce that the resolved company matches the authenticated session's `sessCompId` before accepting data.

---

### HIGH: `mailer.do` is Auth-Excluded and Can Be Triggered by Unauthenticated Callers

**Description:**
`/mailer` (`com.action.MailerAction`) is in the authentication exclusion list. It is intended as an internal scheduled-task trigger, but it is reachable from the public internet over HTTP. Any unauthenticated request to `/mailer.do` will:

1. Query the database for all report subscriptions.
2. For each subscription, call an external `ReportAPI` to generate a PDF.
3. Send the generated PDF via email to subscribed users.

The `debug` parameter is accepted without authentication. When `debug=t` is passed, the email is redirected to `RuntimeConf.debugEmailRecipet` — an attacker-controlled parameter could potentially be used to exfiltrate report content if `debugEmailRecipet` is derived from request input (this requires further investigation of `RuntimeConf`).

Additionally, the hardcoded credentials string at line 102 of `MailerAction.java` is highly significant:

```java
String input = "{\"admin_password\":\"ciiadmin\",\"username\": \"hui\",\"filters\":[...]}";
```

This hardcoded `admin_password` value `ciiadmin` and username `hui` are embedded in the source and passed as a JSON payload to the internal `ReportAPI`. These appear to be credentials for the report generation backend service.

**Risk:**
- Unauthenticated callers can repeatedly trigger bulk email sends to all subscribed users, constituting mail abuse and potential DoS on the mail service.
- Hardcoded credentials (`ciiadmin` / `hui`) are visible in source and are transmitted to an internal service; if that service has broader access, this represents a credential-exposure vector.
- Resource exhaustion: PDF generation and email delivery for all subscriptions on every unauthenticated hit.

**Recommendation:**
1. Remove `mailer.do` from the public exclusion list. This endpoint should only be callable by an internal scheduler or with a secret token validated in the action.
2. Rotate and remove the hardcoded `admin_password` / `username` credentials from the source. Store them in externalized configuration (environment variables or a secrets manager) and reference them at runtime.
3. Add rate limiting and an IP allowlist for this endpoint if it must remain network-accessible.

---

### HIGH: `calibration.do` Is Authenticated But Has No Forward Path and Triggers Operational Job

**Description:**
The `/calibration` action (`com.action.CalibrationAction`) has no `<forward>` elements defined and explicitly calls `super.execute(mapping, form, request, response)` after running `CalibrationJob.calibrateAllUnits()`. The `super.execute()` call in `org.apache.struts.action.Action` returns `null`, which in Struts 1.x causes the framework to send a blank HTTP 200 response. This action is **not** in the exclusion list, so authentication is required. However:

1. **Any authenticated user** (any company, any role) can trigger a full calibration run across all units in the system via a GET or POST to `/calibration.do`. There is no role or permission check within the action.
2. There is no CSRF protection. A logged-in administrator could be tricked into triggering calibration via a cross-site request.
3. `CalibrationJob.calibrateAllUnits()` is a Quartz-scheduled job; invoking it on demand may cause data corruption, double-processing, or interference with the scheduled run.

**Risk:**
- Any authenticated session (regardless of company or role level) can trigger an uncontrolled system-wide calibration operation.
- Potential data corruption from concurrent or premature calibration runs.
- Denial of service if the calibration job is resource-intensive.

**Recommendation:**
1. Add a super-admin role check at the beginning of `CalibrationAction.execute()` before calling `calibrateAllUnits()`.
2. Add CSRF protection (synchronizer token pattern) to state-changing actions.
3. Add a proper `<forward>` element and return a meaningful response rather than falling through to `super.execute()`.

---

### HIGH: Widespread Missing Input Validation — 39 of 64 Actions Have No Effective Field Validation

**Description:**
Cross-referencing `struts-config.xml` with `validation.xml` reveals that only **3 form definitions** exist in `validation.xml`:

1. `loginActionForm` — validates `username` (required) and `password` (required).
2. `adminRegisterActionForm` — validates `name`, `contact_name`, `email`, `contact_no`, `password`. (Note: this entry is never actually triggered due to the form-bean name mismatch described in the CRITICAL finding above.)
3. `AdminDriverEditForm` — validates `first_name` and `last_name` as required. (Note: the form-bean name declared in `struts-config.xml` is `adminDriverEditForm` — lowercase 'a' — while `validation.xml` uses `AdminDriverEditForm` — uppercase 'A'. Struts validator name matching is case-sensitive. This means this validation rule also **never fires**.)

Every other action that declares `validate="true"` will execute the validator, but with no matching `<form>` entry in `validation.xml`, the validator silently passes without checking any fields. The following actions declare `validate="true"` but have no effective validation:

`/switchCompany`, `/search`, `/register`, `/sendMail`, `/adminAlertAdd`, `/admindriveradd`, `/admindriveredit`, `/admindriverlicencevalidateexist`, `/adminunitedit`, `/adminunitassign`, `/fleetcheckedit`, `/fleetcheckconf`, `/fleetcheckshow`, `/fleetcheckhide`, `/fleetcheckdelete`, `/dealerconvert`, `/driverjobreq`, `/adminunitservice`, `/adminunitimpact`, `/adminunitaccess`, `/dealercompanies`

Actions that explicitly set `validate="false"` or use no form bean also receive no validation: `/settings`, `/manufacturers`, `/trainings`, `/unitnameexists`, `/serialnoexists`, `/macaddressexists`, `/assigndatesvalid`, `/impactreport`, `/gpsreport`, `/incidentreport`, `/dealerImpactReport`, `/dealerPreOpsReport`, `/dealerIncidentReport`, `/sessionreport`, `/dealerSessionReport`, `/preopsreport`

**Risk:**
- SQL injection and XSS vectors are unmitigated at the framework layer across virtually the entire application. Input sanitization is entirely dependent on DAO-layer and action-layer code, which must be audited separately.
- Malformed data (oversized strings, invalid types, null values) can reach the database layer unchecked.

**Recommendation:**
1. Add `<form>` entries in `validation.xml` for every action that accepts user input.
2. Fix the two broken name-match bugs immediately (`adminRegActionForm` vs `adminRegisterActionForm`, and `adminDriverEditForm` vs `AdminDriverEditForm`).
3. At minimum, add `required`, `maxlength`, and appropriate type checks for all user-supplied fields.

---

### MEDIUM: `goResetPass.do` and `resetpass.do` Are Auth-Excluded and Accept Unauthenticated Username Input

**Description:**
Both `/goResetPass` and `/resetpass` are excluded from authentication and accept a `username` parameter from the HTTP request without any validation or rate-limiting.

`GoResetPassAction` passes the attacker-supplied `username` directly to `RestClientService.resetPassword()`, which triggers a Cognito password reset flow for that username. An unauthenticated attacker can invoke this with any valid username to:
1. Spam Cognito password-reset emails to any registered user.
2. Potentially lock out accounts if the Cognito user pool has lockout policies on failed reset attempts.

`ResetPasswordAction` accepts `username`, `npass` (new password), and `code` (confirmation code) and passes them to `RestClientService.confirmResetPassword()`. There is no validation that the `username` was the one that initiated the reset flow in the current session (no session token binding).

**Risk:**
- Account enumeration: sending a reset request for an unknown username may produce a different Cognito response, revealing whether the account exists.
- User harassment via unsolicited password-reset emails.
- If confirmation codes are guessable or leaked via another vector, arbitrary password resets are possible.

**Recommendation:**
1. Add rate limiting (by IP and by username) to both endpoints.
2. Bind the reset flow to the session: store the `username` in the session during `goResetPass` and validate it against the submitted `username` in `resetpass` rather than trusting the POST parameter.
3. Ensure the Cognito user pool is configured to return identical responses for valid and invalid usernames to prevent account enumeration.

---

### MEDIUM: `api.do` Is Auth-Excluded With Entire Implementation Commented Out

**Description:**
`/api` (`com.action.AppAPIAction`) is excluded from authentication. The entire action body — which included API key validation via `compKey`, driver data retrieval, vehicle data retrieval, checklist submission, and PDF report generation — has been commented out with `////` prefixes. The current action simply calls `return mapping.findForward("apiXml")`, rendering `/html-jsp/apiXml.jsp` without any data.

This is a dead endpoint that is nevertheless reachable by unauthenticated callers. The commented-out code reveals the full intended API contract (including an `admin_password` credential mechanism via `compKey`) which could assist an attacker in understanding the data model. Furthermore, if the commented-out code is ever re-enabled without restoring the authentication exclusion review, the endpoint would immediately expose significant data retrieval and write capabilities to unauthenticated callers.

**Risk:**
- Information disclosure: the commented-out code is compiled into the JAR/WAR and visible in decompiled form; it reveals internal API operations, parameter names, and data structures.
- The exclusion creates a permanently open door that would be dangerous if code is re-enabled without re-audit.

**Recommendation:**
1. Remove the `api.do` exclusion from `PreFlightActionServlet` if the API endpoint is not currently in production use.
2. If the API will be re-enabled, implement proper API key or OAuth2 authentication before doing so.
3. Delete commented-out production code from the source rather than leaving it in place.

---

### MEDIUM: `uploadfile.do` Is Auth-Excluded But Has No Action Mapping

**Description:**
`PreFlightActionServlet.excludeFromFilter()` contains an exclusion for `uploadfile.do` (line 113), but there is no corresponding `<action path="/uploadfile" ...>` entry in `struts-config.xml`. This means:

1. A request to `/uploadfile.do` bypasses authentication.
2. Struts cannot find a mapping and returns a 400 or forwards to the error page.

This is a "dead exclusion" that indicates a file-upload endpoint previously existed and was removed from the struts config but not from the auth filter. If a new `/uploadfile` action is ever added to `struts-config.xml` — even inadvertently — it will immediately be unauthenticated.

**Risk:**
- The exclusion represents a latent unauthenticated file upload path that could be accidentally re-activated.
- The prior existence of an unauthenticated file upload endpoint should be investigated through git history to understand what it did.

**Recommendation:**
1. Remove the `uploadfile.do` exclusion from `excludeFromFilter()` since no action is mapped.
2. Review git history to understand what `uploadfile.do` did and whether its removal was intentional.
3. If file upload functionality is needed, implement it behind authentication with strict file type and size validation.

---

### MEDIUM: `adminWelcome.do` Is Auth-Excluded But Has No Action Mapping

**Description:**
`PreFlightActionServlet.excludeFromFilter()` excludes `adminWelcome.do` (line 101), but no `<action path="/adminWelcome" ...>` entry exists in `struts-config.xml`. This is another dead exclusion similar to `uploadfile.do`. While currently benign (Struts cannot dispatch the request), it creates the same latent risk of accidental re-activation without authentication.

**Risk:** Low. Latent unauthenticated path if an action is added for this path in the future.

**Recommendation:** Remove the `adminWelcome.do` exclusion from `excludeFromFilter()`.

---

### MEDIUM: Validation.xml Form Name Case Mismatch Silently Disables Driver Validation

**Description:**
The action `/admindriveredit` and `/admindriverlicencevalidateexist` both declare `validate="true"` and reference form-bean name `adminDriverEditForm` (lowercase 'a'). The `validation.xml` file defines a form as `AdminDriverEditForm` (uppercase 'A'). Struts `ValidatorPlugIn` performs a case-sensitive lookup using the form-bean name. The names do not match, so no validator rules fire.

The result is that first name and last name required-field checks declared in `validation.xml` are silently skipped for driver edit operations, contradicting the apparent intent of the developer.

**Risk:**
- Null or empty driver first/last names can be saved to the database, causing display errors and potentially breaking reports.
- The broken validation state gives a false sense of security — developers reviewing the config see `validate="true"` and assume fields are being checked.

**Recommendation:**
Align the form name in `validation.xml` to exactly match the form-bean name `adminDriverEditForm` (lowercase 'a'):
```xml
<form name="adminDriverEditForm">
```

---

### LOW: `dealerconvert` Action Uses Session Scope for Form Bean

**Description:**
The `/dealerconvert` action declares `scope="session"` for its form bean (`adminDealerActionForm`). Using session scope for form beans in Struts 1.x means the form data persists across requests. This can cause stale data from a previous request to be silently submitted in a new request if the form is not explicitly cleared. In a multi-user or tabbed-browser context, session-scoped form beans can also lead to one user's data being processed under another user's session.

**Risk:**
- Data integrity: previous form field values may carry forward unintentionally.
- In concurrent tab scenarios, data from one tab operation may contaminate another.

**Recommendation:** Change `scope="session"` to `scope="request"` for this action.

---

### LOW: Typo in Action Path `/swithLanguage` (Missing 'c')

**Description:**
The action path is declared as `/swithLanguage` (missing the letter 'c' — should be `/switchLanguage`). The corresponding exclusion in `PreFlightActionServlet` also uses `swithLanguage.do`. The typo is consistent so the feature works, but it creates confusion and makes auditing harder.

**Risk:** Low — cosmetic issue; no direct security impact but suggests low code quality discipline.

**Recommendation:** Correct the typo to `/switchLanguage` in both `struts-config.xml` and `PreFlightActionServlet.java` atomically.

---

### LOW: Global Exception Handlers Forward to `errorDefinition` (Tile) Which Resolves to a Static HTML File

**Description:**
The `<global-exceptions>` block maps `java.sql.SQLException`, `java.io.IOException`, and `javax.servlet.ServletException` to `errorDefinition`. The `tiles-defs.xml` maps `errorDefinition` to `/error/error.html` — a static HTML file. This means unhandled SQL exceptions will produce an HTML error page without sanitizing any exception detail that might have been added to request attributes.

While the static HTML file itself will not render Java stack traces, the Struts exception handling chain may log exception messages or set request attributes that could be rendered in unexpected ways.

**Risk:** Low — stack traces are not directly exposed through this path, but the error handling should be reviewed to ensure no exception detail leaks into the HTTP response.

**Recommendation:** Verify that `error.html` does not render any request attributes. Confirm that Tomcat's default error handling is also configured to suppress stack traces.

---

### INFO: `formBuilder.do` Is Authenticated But Has No Dedicated Forward for Error Cases

**Description:**
`/formBuilder` (`com.action.FormBuilderAction`) has only a single `<forward name="success">` to `/html-jsp/formBuilder.jsp`. There is no failure, error, or input forward defined. If the action throws an exception or returns a forward name other than `success`, Struts will invoke the global exception handler.

**Risk:** Informational — potential for unhandled error paths; no direct security impact identified at the config level.

**Recommendation:** Review `FormBuilderAction` to confirm all code paths return `"success"` or investigate whether additional forward names are needed.

---

### INFO: `calibration.do` Returns No Forward — Calls `super.execute()` Which Returns `null`

**Description:**
`/calibration` has no `<forward>` elements defined in `struts-config.xml`. The action calls `super.execute(mapping, form, request, response)` which returns `null` in Struts 1.x base `Action`. When Struts receives a `null` forward, it does not redirect and the response is committed with whatever was written to the output stream (likely empty). This will produce an HTTP 200 with empty body.

**Risk:** Informational at the configuration level. The operational risk (unauthenticated calibration trigger) is covered in the HIGH finding above.

**Recommendation:** Add an explicit `<forward name="success">` and return it from the action.

---

## 4. Summary of Auth-Excluded Path Risk Ratings

| Excluded Path | Risk | Finding |
|---------------|------|---------|
| `adminRegister.do` | CRITICAL | Unauthenticated company account creation |
| `loadbarcode.do` | CRITICAL | Unauthenticated write of operational inspection data |
| `mailer.do` | HIGH | Unauthenticated bulk email trigger + hardcoded credentials |
| `goResetPass.do` | MEDIUM | Unauthenticated Cognito password reset initiation |
| `resetpass.do` | MEDIUM | Unauthenticated password confirmation |
| `api.do` | MEDIUM | Dead endpoint with unauthenticated access; latent risk |
| `uploadfile.do` | MEDIUM | Dead exclusion — no mapped action; latent risk |
| `adminWelcome.do` | MEDIUM | Dead exclusion — no mapped action; latent risk |
| `welcome.do` | INFO | Benign |
| `login.do` | INFO | Required public endpoint |
| `logout.do` | INFO | Required public endpoint |
| `expire.do` | INFO | Required public endpoint |
| `swithLanguage.do` | LOW | Language toggle; no data access |
| `switchRegister.do` | LOW | Redirects to registration form only |

---

## 5. Key Configuration File Cross-Reference

| File | Location |
|------|----------|
| Struts config | `/src/main/webapp/WEB-INF/struts-config.xml` |
| Validation rules | `/src/main/webapp/WEB-INF/validation.xml` |
| Tiles definitions | `/src/main/webapp/WEB-INF/tiles-defs.xml` |
| Web deployment descriptor | `/src/main/webapp/WEB-INF/web.xml` |
| Auth filter servlet | `/src/main/java/com/actionservlet/PreFlightActionServlet.java` |

---

## Finding Count

CRITICAL: 2 / HIGH: 3 / MEDIUM: 6 / LOW: 3 / INFO: 2
