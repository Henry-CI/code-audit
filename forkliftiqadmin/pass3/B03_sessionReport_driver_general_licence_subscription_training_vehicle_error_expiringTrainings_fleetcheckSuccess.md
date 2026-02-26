# Pass 3 Documentation Audit - Agent B03
**Date:** 2026-02-26
**Files audited:** 9
**Agent:** B03

---

## Reading Evidence

---

### File 1: `html-jsp/dealer/sessionReport.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/dealer/sessionReport.jsp`

**Purpose:** Dealer-facing session report page. Displays a filterable table of forklift usage sessions, filtered by vehicle, driver, and date range. Includes a date-picker setup.

**JSP scriptlet blocks (`<% %>`):**
- Lines 4-6: Reads `sessDateFormat` from session and reformats it for JavaScript date picker (yyyy->yy, M->m).
- Lines 99-105: Conditionally emits JavaScript to initialise `start_date` from the `start_date` request parameter, converting it to ISO format via `DateUtil`.
- Lines 107-113: Conditionally emits JavaScript to initialise `end_date` from the `end_date` request parameter, same conversion.

**JSP expression blocks (`<%= %>`):**
- Line 102: `<%= DateUtil.stringToIsoNoTimezone(request.getParameter("start_date"), (String) session.getAttribute("sessDateFormat")) %>`
- Line 110: `<%= DateUtil.stringToIsoNoTimezone(request.getParameter("end_date"), (String) session.getAttribute("sessDateFormat")) %>`
- Line 114: `<%= dateFormat %>` (injected into `setupDatePicker` call)
- Line 115: `<%= dateFormat %>` (injected into `setupDatePicker` call)

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML form `action` attributes:**
- Line 21 (Struts `html:form`): `action="dealerSessionReport.do"` method POST

**Session attribute accesses:**
- Line 5: `session.getAttribute("sessDateFormat")` (in scriptlet)
- Line 102: `session.getAttribute("sessDateFormat")` (in expression, inside `<% if %>` block)
- Line 110: `session.getAttribute("sessDateFormat")` (in expression, inside `<% if %>` block)

**Significant JavaScript functions:**
- Anonymous jQuery `$(function() { ... })` (lines 95-116): Initialises date pickers for `#start_date` and `#end_date`, pre-populating from server-rendered dates when request parameters are present.

---

### File 2: `html-jsp/driver/general.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/driver/general.jsp`

**Purpose:** Driver add/edit modal fragment - "General" tab. Handles both adding a new driver and editing an existing driver's general information (name, mobile, username/email, PIN). Builds tab navigation URLs dynamically. Includes PIN validation (numeric-only, 4-8 digits) and MD5 hashing of the PIN before submission.

**JSP scriptlet blocks (`<% %>`):**
- Lines 4-39: Main logic block. Reads `action` and `driverId` from request parameters. Constructs tab navigation URLs (`generalUrl`, `trainingUrl`, `subscriptionUrl`, `vehicleUrl`) differently for add vs. edit mode. Sets `op_code` and `actionCode` based on mode. Handles `newDriverId` request attribute if `id` is blank. Reads `sessTimezone` from session to determine whether to label the training tab "Training" or "Licence".

**JSP expression blocks (`<%= %>`):**
- Line 43: `<%=generalUrl%>`
- Line 44: `<%=trainingUrl%>`, `<%=trainingtab %>`
- Line 45: `<%=vehicleUrl%>`
- Line 48 (form action): `<%=actionCode %>`
- Line 135 (hidden field value): `<%=id %>`
- Line 136 (hidden field value): `<%=op_code %>`
- Line 256 (inside JS): `<%=actionCode %>`

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ page import="org.apache.commons.lang.StringUtils" %>`
- Line 2: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML form `action` attributes:**
- Line 48 (Struts `html:form`): `action="<%=actionCode %>"` method POST — resolves to either `admindriveradd.do` (add mode) or `admindriveredit.do` (edit mode)

**Session attribute accesses:**
- Line 33: `session.getAttribute("sessTimezone")`

**Significant JavaScript functions:**
- `displayRequiredFields()` (lines 144-178): Validates that `first_name`, `last_name`, and `email_addr` are non-empty, and that `pass` and `cpass` match. Highlights invalid fields in red. Returns a boolean.
- `validateFields(valid)` (lines 180-214): Validates PIN is numeric-only, between 4 and 8 characters. If valid, computes MD5 hash of PIN into `pass_hash` hidden field. Shows/hides inline error messages. Disables submit button if invalid. Contains `console.log` debug statement.
- Anonymous `$(document).ready()` (lines 216-263): Calls validation on load, hooks `change` event on all inputs, manages `#accessYes`/`#accessNo` toggle state, preserves old email in `#old_email`, and calls `setupConfirmationPopups`.
- `#accessYes` click handler (lines 265-279): Sets `app_access` to `'t'` and updates button CSS classes.
- `#accessNo` click handler (lines 282-296): Sets `app_access` to `'f'` and updates button CSS classes.
- `email_addr` change handler (lines 298-319): Auto-enables app access (`app_access = 't'`) when an email is entered while access is currently `'f'`.

---

### File 3: `html-jsp/driver/licence.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/driver/licence.jsp`

**Purpose:** Unknown — file is empty (zero bytes).

**JSP scriptlet blocks:** None (empty file).
**JSP expression blocks:** None.
**`<%@ include %>` directives:** None.
**HTML form `action` attributes:** None.
**Session attribute accesses:** None.
**JavaScript functions:** None.

---

### File 4: `html-jsp/driver/subscription.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/driver/subscription.jsp`

**Purpose:** Driver edit modal fragment - "Subscription" tab. Displays and allows editing of up to four email subscription addresses for a driver (used for notification purposes).

**JSP scriptlet blocks (`<% %>`):**
- Lines 3-15: Reads `driverId` from request parameters. Builds tab navigation URLs. Reads `sessTimezone` to determine training/licence tab label.

**JSP expression blocks (`<%= %>`):**
- Line 19: `<%=generalUrl%>`
- Line 20: `<%=trainingUrl%>`, `<%=trainingtab %>`
- Line 21: `<%=vehicleUrl%>`

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML form `action` attributes:**
- Line 24 (Struts `html:form`): `action="admindriveredit.do"` method POST

**Session attribute accesses:**
- Line 9: `session.getAttribute("sessTimezone")`

**Significant JavaScript functions:**
- Anonymous `$(function() { ... })` containing `$(document).ready()` (lines 86-94): Calls `setupConfirmationPopups` for form `#adminDriverUpdateSubscription`.

---

### File 5: `html-jsp/driver/training.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/driver/training.jsp`

**Purpose:** Driver edit modal fragment - "Training" (or "Licence") tab. Displays existing driver training records and provides inline controls to add new training entries (manufacturer, type, fuel type, training date, expiration date) or delete existing ones via AJAX calls to `trainings.do`.

**JSP scriptlet blocks (`<% %>`):**
- Lines 3-16: Reads `driverId` from request. Builds tab navigation URLs. Reads `sessDateFormat` and `sessTimezone` from session; determines training/licence tab label based on timezone.

**JSP expression blocks (`<%= %>`):**
- Line 20: `<%=generalUrl%>`
- Line 21: `<%=trainingUrl%>`, `<%=trainingtab %>`
- Line 22: `<%=vehicleUrl%>`
- Line 32: `<%=trainingtab %>` (panel title)
- Line 134: `<%=dateFormat%>` (date picker format)
- Line 138: `<%=dateFormat%>` (date picker format)

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML form `action` attributes:**
- Line 25 (Struts `html:form`): `action="admindriveredit.do"` method POST

**Session attribute accesses:**
- Line 9: `session.getAttribute("sessDateFormat")`
- Line 10: `session.getAttribute("sessTimezone")`

**Significant JavaScript functions:**
- Anonymous `$(document).ready()` (lines 126-139): Sets up `setupConfirmationPopups` on a selector `#adminDriverUpdateTraining` (note: form `styleId` is actually `adminDriverUpdateVehicle` — possible mismatch). Initialises date pickers for training date (today) and expiration date (one year from today).
- `addTraining(event)` (lines 141-158): Prevents default link action, POSTs to `trainings.do` with form field values, then triggers a tab reload on success or shows a SweetAlert error on failure.
- `deleteTraining(event, id)` (lines 160-169): Prevents default, GETs `trainings.do?action=delete&training=id`, reloads tab on success or shows SweetAlert error on failure.

---

### File 6: `html-jsp/driver/vehicle.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/driver/vehicle.jsp`

**Purpose:** Driver edit modal fragment - "Vehicles" tab. Displays a list of all vehicles with checkboxes to assign/unassign them to the driver, plus read-only "Trained" and "Hours" columns.

**JSP scriptlet blocks (`<% %>`):**
- Lines 3-15: Reads `driverId` from request. Builds tab navigation URLs. Reads `sessTimezone` to determine training/licence tab label.

**JSP expression blocks (`<%= %>`):**
- Line 19: `<%=generalUrl%>`
- Line 20: `<%=trainingUrl%>`, `<%=trainingtab %>`
- Line 21: `<%=vehicleUrl%>`

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML form `action` attributes:**
- Line 24 (Struts `html:form`): `action="admindriveredit.do"` method POST

**Session attribute accesses:**
- Line 9: `session.getAttribute("sessTimezone")`

**Significant JavaScript functions:**
- Anonymous `$(document).ready()` (lines 82-88): Calls `setupConfirmationPopups` for form `#adminDriverUpdateVehicle`.

---

### File 7: `html-jsp/error.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/error.jsp`

**Purpose:** Generic error display page fragment. Renders Struts HTML errors, provides a "Previous" button that navigates back in browser history. Wraps rendering in a try/catch that logs exceptions via `InfoLogger` and re-throws them.

**JSP scriptlet blocks (`<% %>`):**
- Lines 3-6: Obtains an `InfoLogger` logger instance named `"com.error.html"` and opens a try block.
- Lines 17-24: Closes the try block with a catch that logs the exception and re-throws it as a new `Exception`.

**JSP expression blocks (`<%= %>`):** None.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp" %>`

**HTML form `action` attributes:** None.

**Session attribute accesses:** None.

**Significant JavaScript functions:**
- `previous()` (lines 27-29): Calls `history.back(-1)` to navigate to the previous page. Note: the `-1` argument to `history.back()` is non-standard; `history.back()` takes no meaningful argument in modern browsers.

---

### File 8: `html-jsp/expiringTrainings.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/expiringTrainings.jsp`

**Purpose:** Dashboard widget/panel displaying a table of drivers whose training (or licence, depending on locale) has expired or is expiring soon. Shows driver name, email, vehicle, training date, and expiration date.

**JSP scriptlet blocks (`<% %>`):**
- Lines 2-9: Reads `sessTimezone` from session. Sets `trainingtab` to `"training"` or `"licence"` based on whether the timezone is in `"US/"` or `"Canada/"` regions.

**JSP expression blocks (`<%= %>`):**
- Line 19: `<%=trainingtab %>` (used in panel subtitle text)

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp" %>`

**HTML form `action` attributes:** None.

**Session attribute accesses:**
- Line 3: `session.getAttribute("sessTimezone")`

**Significant JavaScript functions:** None.

---

### File 9: `html-jsp/fleetcheckSuccess.jsp`

**Full path:** `/mnt/c/Projects/cig-audit/repos/forkliftiqadmin/src/main/webapp/html-jsp/fleetcheckSuccess.jsp`

**Purpose:** Fleet check completion confirmation page. Displays a success message after a fleet check, shows a 10-second countdown timer, and then automatically redirects by submitting a hidden form (`goSerach.do`). Also provides a manual logout button.

**JSP scriptlet blocks (`<% %>`):** None.

**JSP expression blocks (`<%= %>`):** None.

**`<%@ include %>` / `<jsp:include>` directives:**
- Line 1: `<%@ include file="../includes/importLib.jsp" %>`

**HTML form `action` attributes:**
- Line 9: `action="goSerach.do"` method POST (form `name="searchForm"` — note typo: "goSerach" likely should be "goSearch")
- Line 11: `action="logout.do"` method POST (form `name="logoutForm"`)

**Session attribute accesses:** None.

**Significant JavaScript functions:**
- `init()` (lines 25-28): Starts a 1-second interval timer via `setInterval(countDown, 1000)`. Called via `document.onload = init()` (misuse: assigns the return value of `init()`, not the function reference).
- `countDown()` (lines 31-40): Decrements `time`, updates `#timer` display. Calls `redirect()` when `time` reaches 0.
- `redirect()` (lines 42-45): Submits `document.searchForm`, triggering navigation to `goSerach.do`.

---

## Findings

---

### B03-1 | LOW | dealer/sessionReport.jsp:1 | Missing page-level comment

There is no HTML or JSP comment near the top of `sessionReport.jsp` describing the page's purpose, the expected session attributes, or its role in the dealer module. The first line is an include directive with no accompanying documentation.

---

### B03-2 | MEDIUM | dealer/sessionReport.jsp:4-6 | Complex session-attribute transformation without comment

The scriptlet at lines 4-6 silently reformats the session date format string for JavaScript consumption — stripping century from years (`yyyy` → `yy`) and converting month notation (`M` → `m`). This transformation is non-obvious and has no comment explaining why the format must be adapted or what JavaScript library convention is being satisfied.

```jsp
<%
    String dateFormat = ((String) session.getAttribute("sessDateFormat")).replaceAll("yyyy", "yy").replaceAll("M", "m");
%>
```

---

### B03-3 | LOW | dealer/sessionReport.jsp:5 | Non-obvious session attribute key `sessDateFormat`

The key `"sessDateFormat"` is accessed without any comment documenting what format string it contains, who sets it, or what its expected values are. The same observation applies to the duplicate access at lines 102 and 110.

---

### B03-4 | MEDIUM | dealer/sessionReport.jsp:99-113 | Scriptlet blocks interleaved with JavaScript with no comment

The scriptlet/expression blocks at lines 99-113 intermix Java conditionals with JavaScript variable initialisation to optionally pre-populate date variables from request parameters. This pattern (Java `if` block opening, then closing, around a JavaScript statement) is confusing and has no comment explaining the intent (i.e., "pre-fill the date pickers with the previously submitted search values if present").

---

### B03-5 | LOW | driver/general.jsp:1 | Missing page-level comment

`general.jsp` has no page-level comment describing it as the "General" tab fragment of the driver add/edit modal, its relationship to the other tab fragments, or the dual add/edit mode it supports.

---

### B03-6 | MEDIUM | driver/general.jsp:4-39 | Large scriptlet with dual-mode URL construction logic and no comment

The 35-line scriptlet at lines 4-39 contains non-trivial branching logic: it switches between add and edit modes, constructs multiple tab navigation URLs, selects the appropriate `op_code` and `actionCode`, handles the `newDriverId` request attribute (a cross-request hand-off), and determines locale-sensitive tab labelling. None of this logic has a comment explaining the mode-switching mechanism, what `newDriverId` is for, or why `op_code` changes between `add_general` and `edit_general`.

---

### B03-7 | LOW | driver/general.jsp:20-21 | Magic string op_codes `add_general` / `edit_general` undocumented

The string literals `"add_general"` and `"edit_general"` at lines 20 and 25 are hard-coded operation codes presumably consumed by server-side action classes. There is no comment explaining what these codes mean, the full set of allowed values, or where they are processed.

---

### B03-8 | MEDIUM | driver/general.jsp:180-214 | `validateFields` contains `console.log` debug statement with no comment

The `validateFields` function at line 210 contains `console.log("valid:"+valid)`. This is a debug artifact that should have been removed before production. Its presence is undocumented and will leak validation state to the browser console for any user with dev tools open.

```javascript
console.log("valid:"+valid);
```

---

### B03-9 | MEDIUM | driver/general.jsp:190 | Magic PIN bypass sentinel `"******"` with no comment

Line 190 contains:

```javascript
if( isnum == false && pass != "******"){
```

The literal `"******"` appears to be a sentinel value representing a masked/unchanged password (i.e., the server rendered this placeholder to indicate the PIN is already set and not being changed). This is a non-obvious magic string with significant security implications and has no comment explaining its origin, what it means, or that it is a server-rendered placeholder.

---

### B03-10 | HIGH | driver/general.jsp:190 | Numeric-only PIN validation bypassed for sentinel `"******"` — bypass not clearly documented

Combined with B03-9: the bypass `pass != "******"` exempts the six-asterisk sentinel from the numeric-only and length checks at lines 190-208. There is no comment documenting that this sentinel is server-generated (implying it cannot be user-typed under normal circumstances), nor any server-side re-validation context provided. A developer maintaining this code could misunderstand the bypass as a security hole rather than a display artifact, or could inadvertently remove/change the sentinel without realising the implications.

---

### B03-11 | LOW | driver/licence.jsp:— | Zero-byte / empty file

`licence.jsp` is a completely empty file (0 bytes). It is referenced as a conceptual counterpart to `training.jsp` and `general.jsp` in the driver tab system (based on the tab label logic in other files that switches to "Licence" for non-US/Canada timezones), but contains no content whatsoever. No comment explains whether this file is intentionally empty, a placeholder, deprecated, or should redirect to `training.jsp`.

---

### B03-12 | LOW | driver/subscription.jsp:1 | Missing page-level comment

`subscription.jsp` has no page-level comment describing its purpose (driver email subscription management tab), its relationship to the other driver tab fragments, or the bean names it depends on (`arrAdminDriverEmails`, `driverEmails`).

---

### B03-13 | LOW | driver/subscription.jsp:3-15 | Non-obvious session attribute key `sessTimezone` used for tab label switching with no comment

Lines 11-14 use `sessTimezone` to switch the training/licence tab label. This locale-detection logic (checking for `"US/"` or `"Canada/"` in the timezone string) is duplicated across at least four files (`general.jsp`, `subscription.jsp`, `training.jsp`, `vehicle.jsp`, `expiringTrainings.jsp`) and is never documented. No comment explains what regions qualify as "US/Canada" or why those regions use "Training" vs. "Licence" terminology.

---

### B03-14 | LOW | driver/training.jsp:1 | Missing page-level comment

`training.jsp` has no page-level comment. Given that it is also used as the "Licence" tab for non-US/Canada locales, documentation of this dual role is especially important.

---

### B03-15 | HIGH | driver/training.jsp:127 | `setupConfirmationPopups` targets non-existent form ID `#adminDriverUpdateTraining`

Line 127 calls:

```javascript
setupConfirmationPopups('#adminDriverUpdateTraining', ...);
```

However, the `html:form` on line 25 has `styleId="adminDriverUpdateVehicle"`. The selector `#adminDriverUpdateTraining` does not match any element on this page. This means the confirmation popup wiring silently fails — no comment acknowledges this mismatch. This is functionally incorrect code with no documentation noting the discrepancy, and it represents an inaccurate/misleading code comment situation (the code implies the popup is wired up, but it is not).

---

### B03-16 | LOW | driver/vehicle.jsp:1 | Missing page-level comment

`vehicle.jsp` has no page-level comment describing its purpose (vehicle assignment tab for a driver), the bean names it relies on (`driverVehicle`), or the `op_code = "edit_vehicle"` it submits.

---

### B03-17 | LOW | driver/vehicle.jsp:75 | Magic string op_code `edit_vehicle` undocumented

Line 75 hard-codes `value="edit_vehicle"` as the `op_code` hidden field with no comment explaining what operation this code triggers or where it is consumed server-side.

---

### B03-18 | LOW | error.jsp:1 | Missing page-level comment

`error.jsp` has no page-level comment describing its role as the generic error display fragment, the logger category `"com.error.html"` it uses, or the try/catch re-throw pattern it employs.

---

### B03-19 | LOW | error.jsp:4 | Magic logger name `"com.error.html"` undocumented

The string literal `"com.error.html"` on line 4 is the logger category name passed to `InfoLogger.getLogger(...)`. There is no comment explaining this naming convention or where logs for this category are routed.

---

### B03-20 | LOW | error.jsp:28 | Non-standard `history.back(-1)` argument undocumented

Line 28 calls `history.back(-1)`. The `-1` argument is ignored by all modern browsers (the standard `history.back()` always goes back exactly one step). There is no comment acknowledging this, explaining the intent of the argument, or noting that it is equivalent to `history.back()`.

---

### B03-21 | LOW | expiringTrainings.jsp:1 | Missing page-level comment

`expiringTrainings.jsp` has no page-level comment describing it as a dashboard widget, the bean it expects (`arrExpiringTrainings`), or what "expiring soon" means in terms of the time window.

---

### B03-22 | LOW | expiringTrainings.jsp:3 | `sessTimezone` locale-detection logic duplicated with no comment

This file repeats the same undocumented timezone-based tab label logic found in four other files (see B03-13). None of the copies have a comment. The duplication itself is undocumented.

---

### B03-23 | LOW | fleetcheckSuccess.jsp:1 | Missing page-level comment

`fleetcheckSuccess.jsp` has no page-level comment describing the fleet check completion flow, the purpose of the auto-redirect timer, or the destination `goSerach.do`.

---

### B03-24 | LOW | fleetcheckSuccess.jsp:9 | Apparent typo in form action `goSerach.do` undocumented

Line 9 references `action="goSerach.do"`. "Serach" appears to be a misspelling of "Search". There is no comment acknowledging this as an intentional internal route name or flagging it as a known typo. A future developer may not know whether this is intentional or a defect.

---

### B03-25 | MEDIUM | fleetcheckSuccess.jsp:23 | `document.onload` misuse — assigns return value of `init()` instead of function reference

Line 23:

```javascript
document.onload = init();
```

This assigns the *return value* of `init()` (which is `undefined`) to `document.onload`, not a function reference. As a result, `document.onload` is never actually set as an event handler in the conventional sense; `init()` is called immediately at script parse time (as a side effect of the expression), which happens to work in practice but is unintentional and fragile. No comment explains this pattern or acknowledges the deviation from standard `window.onload = init` or `document.addEventListener('load', init)`.

---

## Summary Table

| ID     | Severity | File                                     | Line(s)  | Issue                                                                      |
|--------|----------|------------------------------------------|----------|----------------------------------------------------------------------------|
| B03-1  | LOW      | dealer/sessionReport.jsp                 | 1        | Missing page-level comment                                                 |
| B03-2  | MEDIUM   | dealer/sessionReport.jsp                 | 4-6      | Date format transformation without explanatory comment                     |
| B03-3  | LOW      | dealer/sessionReport.jsp                 | 5        | Non-obvious session key `sessDateFormat` undocumented                      |
| B03-4  | MEDIUM   | dealer/sessionReport.jsp                 | 99-113   | Java/JS interleaved scriptlets with no comment on intent                   |
| B03-5  | LOW      | driver/general.jsp                       | 1        | Missing page-level comment                                                 |
| B03-6  | MEDIUM   | driver/general.jsp                       | 4-39     | Large dual-mode scriptlet with no comment                                  |
| B03-7  | LOW      | driver/general.jsp                       | 20, 25   | Magic op_code strings `add_general`/`edit_general` undocumented            |
| B03-8  | MEDIUM   | driver/general.jsp                       | 210      | Leftover `console.log` debug statement undocumented                        |
| B03-9  | MEDIUM   | driver/general.jsp                       | 190      | Magic sentinel `"******"` for PIN bypass undocumented                      |
| B03-10 | HIGH     | driver/general.jsp                       | 190-208  | PIN validation bypass for `"******"` sentinel with no security comment     |
| B03-11 | LOW      | driver/licence.jsp                       | —        | Zero-byte / empty file with no comment or explanation                      |
| B03-12 | LOW      | driver/subscription.jsp                  | 1        | Missing page-level comment                                                 |
| B03-13 | LOW      | driver/subscription.jsp                  | 11-14    | `sessTimezone` locale-label logic undocumented (also in 4 other files)     |
| B03-14 | LOW      | driver/training.jsp                      | 1        | Missing page-level comment                                                 |
| B03-15 | HIGH     | driver/training.jsp                      | 127      | `setupConfirmationPopups` targets non-existent form ID (`#adminDriverUpdateTraining` vs `adminDriverUpdateVehicle`) |
| B03-16 | LOW      | driver/vehicle.jsp                       | 1        | Missing page-level comment                                                 |
| B03-17 | LOW      | driver/vehicle.jsp                       | 75       | Magic op_code `edit_vehicle` undocumented                                  |
| B03-18 | LOW      | error.jsp                                | 1        | Missing page-level comment                                                 |
| B03-19 | LOW      | error.jsp                                | 4        | Magic logger category name `"com.error.html"` undocumented                 |
| B03-20 | LOW      | error.jsp                                | 28       | Non-standard `history.back(-1)` argument undocumented                      |
| B03-21 | LOW      | expiringTrainings.jsp                    | 1        | Missing page-level comment                                                 |
| B03-22 | LOW      | expiringTrainings.jsp                    | 3        | Duplicated `sessTimezone` locale-detection logic undocumented               |
| B03-23 | LOW      | fleetcheckSuccess.jsp                    | 1        | Missing page-level comment                                                 |
| B03-24 | LOW      | fleetcheckSuccess.jsp                    | 9        | Apparent typo `goSerach.do` — no comment acknowledging or explaining it    |
| B03-25 | MEDIUM   | fleetcheckSuccess.jsp                    | 23       | `document.onload = init()` — assigns return value, not function reference  |

**Totals:** 2 HIGH, 7 MEDIUM, 16 LOW
