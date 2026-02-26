# Pass 3 Documentation Audit — Agent B07
**Date:** 2026-02-26
**Auditor:** B07
**Scope:** users/subscription.jsp, vehicle/access.jsp, vehicle/adminUnitEdit.jsp, vehicle/assignment.jsp, vehicle/driver_job_details.jsp, vehicle/impact.jsp, vehicle/service.jsp, vehicle/view_job_details.jsp, includes/adsleft.inc.jsp

---

## Reading Evidence

---

### File 1: `html-jsp/users/subscription.jsp`

**Purpose:** Modal tab panel that manages driver alert subscription preferences. Allows an admin to enable/disable email and SMS notifications per driver (Red Impact Email, Red Impact SMS, Training Expiry Email). Part of the driver edit modal; this is the "Notification" tab.

**JSP Scriptlet blocks (`<% %>`)**
| Lines | Content |
|-------|---------|
| 3–7 | Reads `driverId` request parameter (defaults to `0` when absent); builds `generalUrl` for the General tab and `subscriptionUrl` for the Notification tab. |

**JSP Expression blocks (`<%= %>`)**
| Line | Expression |
|------|-----------|
| 11 | `<%=generalUrl%>` — href for General tab link |
| 12 | `<%=subscriptionUrl%>` — href for Notification tab link |

**`<%@ include %>` / `<jsp:include>` directives**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML form `action` attributes**
- Line 15: `action="admindriveredit.do"` (Struts `<html:form>`)

**Session attribute accesses**
- None directly in this file (session is used implicitly through Struts logic tags, e.g., `name="redImpactAlert"`, `name="redImpactSMSAlert"`, `name="driverDenyAlert"` reference request-scoped beans placed by the action class).

**Significant JavaScript functions**
- `isValid()` (lines 80–86): Validates that a mobile number is present when SMS alert checkbox is checked.
- `send()` (lines 88–95): Calls `isValid()`; if invalid shows SweetAlert error, otherwise submits the form `#adminDriverUpdateSubscription`.
- Anonymous `$(function(){})` (lines 97–106): Sets up AJAX confirmation popup for the subscription form.

---

### File 2: `html-jsp/vehicle/access.jsp`

**Purpose:** Vehicle (unit) edit modal — "Access" tab. Displays and saves access-control configuration for a vehicle: accessibility toggle, access type (Card/PIN), access ID, keypad reader brand, and facility code. The tab count differs depending on whether the user is a dealer (5 tabs) or not (4 tabs, no Assignment tab).

**JSP Scriptlet blocks (`<% %>`)**
| Lines | Content |
|-------|---------|
| 3–12 | Reads `id` request parameter; builds `urlGeneral` pointing to edit or add action based on whether `id` is empty. |

**JSP Expression blocks (`<%= %>`)**
| Line | Expression |
|------|-----------|
| 18 | `<%=urlGeneral %>` — General tab link (dealer branch) |
| 19 | `<%=id %>` — equipId in Service tab URL |
| 20 | `<%=id %>` — id in Access tab URL |
| 21 | `<%=id %>` — equipId in Impact tab URL |
| 22 | `<%=id %>` — equipId in Assignment tab URL |
| 27 | `<%=urlGeneral %>` — General tab link (non-dealer branch) |
| 28 | `<%=id %>` — equipId in Service tab URL |
| 29 | `<%=id %>` — id in Access tab URL |
| 30 | `<%=id %>` — equipId in Impact tab URL |

**`<%@ include %>` / `<jsp:include>` directives**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML form `action` attributes**
- Line 35: `action="adminunitaccess.do"` (Struts `<html:form>`)

**Session attribute accesses**
- None directly (Struts `<logic:equal value="true" name="isDealer">` reads the `isDealer` session-scoped bean implicitly).

**Significant JavaScript functions**
- Anonymous `$(document).ready()` (lines 107–113): Sets up AJAX confirmation popup for `#adminUnitEditFormAccess`.

---

### File 3: `html-jsp/vehicle/adminUnitEdit.jsp`

**Purpose:** Vehicle (unit) edit modal — "General" tab. Allows admins to create or edit a vehicle record with fields: name, serial number, manufacturer, type, power/fuel type, load capacity (with weight unit), expansion module flag, and MAC address. Includes inline duplicate-check AJAX calls for name, serial number, and MAC address. Tab navigation respects dealer vs. non-dealer context.

**JSP Scriptlet blocks (`<% %>`)**
| Lines | Content |
|-------|---------|
| 2–25 | Reads `action` and `equipId` parameters; builds URLs for all five navigation tabs (General, Service, Access, Impact, Assignment) conditionally on whether action equals `"edit"`; reads `newId` from request attributes. |

**JSP Expression blocks (`<%= %>`)**
| Line | Expression |
|------|-----------|
| 29 | `<%=urlGeneral %>` — General tab link |
| 30 | `<%=urlService %>` — Service tab link |
| 31 | `<%=urlAccess %>` — Access tab link |
| 32 | `<%=urlImpact %>` — Impact tab link |
| 33 | `<%=urlAssignment %>` — Assignment tab link |
| 38 | `<%=urlGeneral %>` — General tab link (non-dealer) |
| 39 | `<%=urlService %>` — Service tab link (non-dealer) |
| 40 | `<%=urlAccess %>` — Access tab link (non-dealer) |
| 41 | `<%=urlImpact %>` — Impact tab link (non-dealer) |
| 170 | `<%=id %>` — value for hidden `oldId` field |
| 171 | `<%=newUnitId %>` — value for hidden `newId` field |
| 172 | `<%=action %>` — value for hidden `actionUnit` field |

**`<%@ include %>` / `<jsp:include>` directives**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML form `action` attributes**
- Line 46: `action="adminunitedit.do"` (Struts `<html:form>`)

**Session attribute accesses**
- None directly in scriptlet code; `isDealer` is accessed via Struts `<logic:equal/notEqual name="isDealer">` tags.

**Significant JavaScript functions**
- `checkIdValue()` (lines 183–188): Alerts user to save general data first if the service tab href is empty.
- `displayRequiredFields()` (lines 211–250): Checks mandatory fields (name, serial_no, manu_id, type_id, fuel_type_id) and disables submit if any are blank.
- `validateNameField()` (lines 252–256): AJAX call to `unitnameexists.do` to detect duplicate names.
- `validateSerialNoField()` (lines 258–262): AJAX call to `serialnoexists.do` to detect duplicate serial numbers.
- `validateMacAddressField()` (lines 264–268): AJAX call to `macaddressexists.do` to detect duplicate MAC addresses.
- `updateErrorDisplay()` (lines 270–273): Updates submit button disabled state based on existence flags.
- `wsValidation(url, divId)` (lines 275–291): Generic synchronous AJAX call; shows/hides an error div and returns boolean.
- Anonymous `$(document).ready()` (lines 293–321): Binds change handlers to selects/inputs and sets up confirmation popup.

---

### File 4: `html-jsp/vehicle/assignment.jsp`

**Purpose:** Vehicle (unit) edit modal — "Assignment" tab. Allows dealers to assign a vehicle to a company for a date range, and shows a table of existing assignments with a delete action. Validates company and start date before enabling the assign button; performs server-side date overlap validation via AJAX.

**JSP Scriptlet blocks (`<% %>`)**
| Lines | Content |
|-------|---------|
| 3–7 | Reads `sessDateFormat` session attribute; reformats the pattern for jQuery datepicker (replaces `yyyy`→`yy` and `M`→`m`); reads `equipId` request parameter; builds `urlGeneral`. |

**JSP Expression blocks (`<%= %>`)**
| Line | Expression |
|------|-----------|
| 14 | `<%=urlGeneral %>` — General tab link |
| 15 | `<%=id %>` — equipId in Service tab URL |
| 16 | `<%=id %>` — id in Access tab URL |
| 17 | `<%=id %>` — equipId in Impact tab URL |
| 19 | `<%=id %>` — equipId in Assignment tab URL |
| 72 | `<%=id %>` — hidden `unit_id` field value |
| 122 | `<%= dateFormat %>` — date format for start date picker |
| 123 | `<%= dateFormat %>` — date format for end date picker |

**`<%@ include %>` / `<jsp:include>` directives**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML form `action` attributes**
- Line 24: `action="adminunitassign.do"` (Struts `<html:form>`)

**Session attribute accesses**
- Line 4: `session.getAttribute("sessDateFormat")` — retrieves the user's preferred date format string.

**Significant JavaScript functions**
- `validateFields()` (lines 125–152): Disables assign button if company or start date is empty; performs synchronous AJAX call to `assigndatesvalid.do` to validate date range overlap and shows error if invalid.
- Inner `isInvalid()` (lines 149–151): Returns true if companyId or start_date is empty.
- Anonymous `$(function(){})` (lines 121–175): Sets up datepickers, change handlers, confirmation popup, datepicker show triggers, and keydown blocking on datepicker inputs.

---

### File 5: `html-jsp/vehicle/driver_job_details.jsp`

**Purpose:** Modal/panel for assigning a driver to a job for a specific vehicle and time range. Presents a driver select list, start/end time pickers, an instructions textarea, and Cancel/Assign buttons. Submits to `driverjobreq.do`. Contains several commented-out form fields (fromTime, toTime) and a commented-out text input originally for driver name.

**JSP Scriptlet blocks (`<% %>`)**
| Lines | Content |
|-------|---------|
| 2–6 | Reads `action`, `equipId`, and `job_id` request parameters, defaulting to empty strings. |

**JSP Expression blocks (`<%= %>`)**
| Line | Expression |
|------|-----------|
| 48 | `<%=jobId %>` — value for hidden `jobId` field |
| 49 | `<%=id %>` — value for hidden `equipId` field |

**`<%@ include %>` / `<jsp:include>` directives**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML form `action` attributes**
- Line 14: `action="driverjobreq.do"` (Struts `<html:form>`)

**Session attribute accesses**
- None directly.

**Significant JavaScript functions**
- Anonymous `$(document).ready()` (lines 64–81): Sets placeholder attributes on inputs and initialises jQuery datetimepicker on `.date_picker` fields.
- `fnsubmitAccount()` (lines 85–106): Validates a company registration form (`adminRegActionForm`) — appears to be dead/misplaced code unrelated to driver job assignment.
- `fnAssign()` (lines 108–119): Reads job title, description, and driver from the parent modal; hides the current modal; submits the `.assign_driver` form. Note: line 112 sets `$("#drivrId")` (typo — should be `#driverId`).
- `fnGoBackHome()` (lines 121–134): Hides the last modal. Contains multiple commented-out alternative approaches.

---

### File 6: `html-jsp/vehicle/impact.jsp`

**Purpose:** Vehicle (unit) edit modal — "Impact" tab. Displays sensor calibration status. If calibration is 100% complete, shows a table of G-force thresholds per impact level and a "RESET Calibration" button; otherwise shows a Bootstrap progress bar indicating calibration progress.

**JSP Scriptlet blocks (`<% %>`)**
| Lines | Content |
|-------|---------|
| 6–11 | Reads `equipId`; builds `urlGeneral`; reads `isDealer` from session; casts request attribute `impactBean` to `ImpactBean`. |

**JSP Expression blocks (`<%= %>`)**
| Line | Expression |
|------|-----------|
| 39 | `<%= isDealer ? "five" : "four" %>` — CSS class for tab count |
| 40 | `<%=urlGeneral %>` — General tab link |
| 41 | `<%=id %>` — equipId in Service URL |
| 42 | `<%=id %>` — id in Access URL |
| 43 | `<%=id %>` — equipId in Impact URL |
| 71 | `<%= String.format("%.1fg", impact.calculateGForceRequiredForImpact(impactLevel)) %>` — formatted G-force value |
| 74 | `<%= ImpactUtil.getCSSColor(impactLevel) %>` — CSS background colour for impact level |
| 85 | `<%=id %>` — hidden equipId field for reset form |

**`<%@ include %>` / `<jsp:include>` directives**
- Line 4: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML form `action` attributes**
- Line 82: `action="adminunitimpact.do"` (Struts `<html:form>`)

**Session attribute accesses**
- Line 9: `session.getAttribute("isDealer")` — direct session access to determine dealer status.

**Significant JavaScript functions**
- Anonymous `$(function(){})` (lines 111–133): Initialises a jQuery UI slider (`#slider`) with calibration value derived from `#FSSX_multiplicator` input; registers `setupConfirmationPopups` for the reset form.
- Line 109: `$('#calibration_slider').trigger('change')` — fires change on element that does not appear to exist in this page.

---

### File 7: `html-jsp/vehicle/service.jsp`

**Purpose:** Vehicle (unit) edit modal — "Service" tab. Shows current service status (status string, hours till next service, accumulated hours) and service scheduling settings (By Set Hours or By Interval). Allows editing accumulated hours, last service hours, next service due at hours, and service interval. Submits to `adminunitservice.do`.

**JSP Scriptlet blocks (`<% %>`)**
| Lines | Content |
|-------|---------|
| 2–12 | Reads `action` and `equipId` parameters; builds `urlGeneral` for General tab link. |

**JSP Expression blocks (`<%= %>`)**
| Line | Expression |
|------|-----------|
| 17 | `<%=urlGeneral %>` — General tab link (dealer branch) |
| 18 | `<%=id %>` — equipId in Service tab URL |
| 19 | `<%=id %>` — id in Access tab URL |
| 20 | `<%=id %>` — equipId in Impact tab URL |
| 21 | `<%=id %>` — equipId in Assignment tab URL |
| 25 | `<%=urlGeneral %>` — General tab link (non-dealer branch) |
| 26 | `<%=id %>` — Service tab URL |
| 27 | `<%=id %>` — Access tab URL |
| 28 | `<%=id %>` — Impact tab URL |
| 181 | `<%=id %>` — hidden `oldId` field value |

**`<%@ include %>` / `<jsp:include>` directives**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML form `action` attributes**
- Line 34: `action="adminunitservice.do"` (Struts `<html:form>`)

**Session attribute accesses**
- None directly (dealer check via Struts `<logic:equal/notEqual name="isDealer">`).

**Significant JavaScript functions**
- Anonymous `$(document).ready()` (lines 201–207): Sets up AJAX confirmation popup for `#adminUnitEditFormService`.

---

### File 8: `html-jsp/vehicle/view_job_details.jsp`

**Purpose:** Read-only modal/panel listing job detail records for a vehicle. Iterates `arrJobDetails` (list of `JobDetailsBean`) and displays driver name, job number, status (1=Start, 2=Complete, 3=Pause), start time, end time, and duration. Contains no form submission.

**JSP Scriptlet blocks (`<% %>`)**
- None.

**JSP Expression blocks (`<%= %>`)**
- None.

**`<%@ include %>` / `<jsp:include>` directives**
- Line 1: `<%@ include file="../../includes/importLib.jsp" %>`

**HTML form `action` attributes**
- None.

**Session attribute accesses**
- None directly.

**Significant JavaScript functions**
- None.

---

### File 9: `html-jsp/includes/adsleft.inc.jsp`

**Purpose:** Reusable include fragment that renders a hidden left-panel advertisement sidebar. Iterates up to 3 records from the `sessAds` bean (session-scoped advertisement list), showing each ad's image (from `RuntimeConf.IMG_SRC` base path) and text.

**JSP Scriptlet blocks (`<% %>`)**
- None (uses expression inside `<img src="...">` via legacy `<%= %>` style).

**JSP Expression blocks (`<%= %>`)**
| Line | Expression |
|------|-----------|
| 11 | `<%=RuntimeConf.IMG_SRC%>` — base image path prepended to each ad image filename |

**`<%@ include %>` / `<jsp:include>` directives**
- None (this file is itself an include fragment; it declares taglib URIs directly).

**HTML form `action` attributes**
- None.

**Session attribute accesses**
- Struts `<logic:notEmpty name="sessAds">` and `<logic:iterate name="sessAds">` read the `sessAds` session-scoped bean (line 8–16).

**Significant JavaScript functions**
- None.

---

## Findings

### B07-1 | LOW | `html-jsp/users/subscription.jsp`:1 | Missing page-level comment

No HTML or JSP comment exists anywhere in the file describing the page's purpose, its role in the driver edit modal, or which controller action populates the `redImpactAlert`, `redImpactSMSAlert`, and `driverDenyAlert` beans. A reader must infer the purpose entirely from the bean names and form labels.

---

### B07-2 | LOW | `html-jsp/users/subscription.jsp`:74 | Magic string op_code without comment

The hidden field `op_code` is hard-coded to `"edit_subscription"` with no comment explaining that this value is used by the server-side action to discriminate between different driver-edit sub-operations. The string is not self-evident to a maintainer unfamiliar with the action dispatch pattern.

---

### B07-3 | LOW | `html-jsp/users/subscription.jsp`:101 | Typo in success message string (undocumented intent)

The `setupConfirmationPopups` call at line 101 passes the success message `'Notifcation information successfully updated.'` (missing letter 'i' in "Notification"). There is no comment, and no indication this is intentional. While not a logic error, it represents an undocumented, unremedied defect in visible user-facing text.

---

### B07-4 | LOW | `html-jsp/vehicle/access.jsp`:1 | Missing page-level comment

No comment at the top of the file describes the Access tab's purpose, which action populates the form bean, or what the access type values (`"card"`, `"pin"`) or keypad reader brand values (`"ROSLARE"`, `"KERI"`, `"SMART"`, `"HID_ICLASS"`) represent. These hard-coded option values appear with no explanation.

---

### B07-5 | LOW | `html-jsp/vehicle/access.jsp`:77–81 | Magic keypad reader brand strings without comment

The `<html:select>` for `keypad_reader` hard-codes four vendor strings (`ROSLARE`, `KERI`, `SMART`, `HID_ICLASS`) with no comment explaining what system or database table they correspond to, or that they must match a back-end enumeration. A maintainer adding or removing a supported reader type has no guidance.

---

### B07-6 | LOW | `html-jsp/vehicle/adminUnitEdit.jsp`:1 | Missing page-level comment

The file has no leading comment explaining it is the General tab of the vehicle edit modal, the significance of the `newId`/`oldId`/`actionUnit` hidden fields, or the overall add-versus-edit flow controlled by the `action` parameter.

---

### B07-7 | MEDIUM | `html-jsp/vehicle/adminUnitEdit.jsp`:2–25 | Complex scriptlet with no comment

The opening scriptlet (24 lines) initialises six URL strings, conditionally populates them only when `action.equalsIgnoreCase("edit")`, and reads a `newId` from request attributes. The logic of leaving URL strings empty for the add case (so that non-General tabs show blank hrefs, prompting a save-first alert) is non-obvious and has no explanatory comment. A maintainer could inadvertently break the save-first guard by initialising the URLs unconditionally.

---

### B07-8 | LOW | `html-jsp/vehicle/adminUnitEdit.jsp`:170–172 | Magic hidden field names without comment

Three hidden inputs — `oldId`, `newId`, and `actionUnit` — carry no comment explaining their purpose in the add/edit lifecycle or how the server uses them to correlate a newly created record with its follow-on edits.

---

### B07-9 | LOW | `html-jsp/vehicle/assignment.jsp`:1 | Missing page-level comment

No comment describes that this tab is dealer-only (though the tab count hints at it), or explains the assignment business rules enforced by the date-range validation.

---

### B07-10 | MEDIUM | `html-jsp/vehicle/assignment.jsp`:4 | Non-obvious session attribute key `sessDateFormat` with transformation logic, no comment

Line 4 reads `session.getAttribute("sessDateFormat")`, then applies two chained `replaceAll` transformations to convert it from a Java `SimpleDateFormat` pattern to a jQuery UI datepicker pattern. The transformation is non-trivial (case-sensitive replacements that must fire in a specific order) and is entirely uncommented. A future change to the stored format or the datepicker library could silently produce wrong date parsing.

---

### B07-11 | LOW | `html-jsp/vehicle/assignment.jsp`:73 | Magic hidden action value `"add"` without comment

The hidden `action` field is hard-coded to `"add"` with no comment explaining whether this could ever be `"edit"` or `"delete"`, or how this value interacts with the server-side action class dispatch.

---

### B07-12 | LOW | `html-jsp/vehicle/driver_job_details.jsp`:1 | Missing page-level comment

No comment describes the page's purpose, which modal context it appears in, or the relationship between `equipId`, `job_id`, and the parent view job details modal.

---

### B07-13 | MEDIUM | `html-jsp/vehicle/driver_job_details.jsp`:85–106 | Dead/misplaced function `fnsubmitAccount()` with no comment

The function `fnsubmitAccount()` (22 lines) validates a company registration form (`adminRegActionForm`) referencing fields `pin`, `cpassword`, `name`, and `email` — none of which exist in this file. It is never called anywhere on this page. There is no comment explaining why it is here, whether it is intentionally retained, or whether it is leftover copy-paste. Its presence is misleading.

---

### B07-14 | MEDIUM | `html-jsp/vehicle/driver_job_details.jsp`:112 | Typo in JavaScript element ID selector — silent bug, no comment

`fnAssign()` at line 112 writes `$("#drivrId").val(...)` where the actual hidden field has `styleId="driverId"` (line 53). The typo silently selects nothing, meaning the `driverId` field is never populated by this path. There is no comment acknowledging the discrepancy. (Note: the select element itself also carries the ID `name` while a separate hidden field has `styleId="driverId"`, compounding the confusion.)

---

### B07-15 | LOW | `html-jsp/vehicle/driver_job_details.jsp`:21–35 | Commented-out code blocks with no explanation

Lines 21 and 29–35 contain commented-out HTML/JSP for a driver name text input and `fromTime`/`toTime` fields. No comment explains why they were removed, whether they will return, or whether the server-side action still expects those parameter names.

---

### B07-16 | LOW | `html-jsp/vehicle/driver_job_details.jsp`:65–70 | Commented-out placeholder line with no explanation

Line 65 contains `// $("#name").attr('placeholder', 'Driver Name')` inside the ready function. The driver selector now uses a `<select>` element (ID `name`) so the placeholder no longer applies, but the commented line is left with no note.

---

### B07-17 | LOW | `html-jsp/vehicle/impact.jsp`:1 | Missing page-level comment

No comment at the top of the file explains the Impact tab's purpose, the calibration lifecycle, or the significance of `percentage == 100.0` as the threshold between showing calibration progress and showing the G-force table.

---

### B07-18 | MEDIUM | `html-jsp/vehicle/impact.jsp`:6–11 | Scriptlet mixes session direct access with no comment, inconsistent with other tabs

Line 9 calls `session.getAttribute("isDealer").equals("true")` directly in a scriptlet — the only vehicle tab page that does this rather than relying exclusively on Struts `<logic:equal name="isDealer">`. No comment explains the reason for the deviation. Additionally, this call will throw a `NullPointerException` if `isDealer` is absent from the session; there is no null guard and no comment acknowledging the assumption.

---

### B07-19 | LOW | `html-jsp/vehicle/impact.jsp`:84 | Magic action string `"reset_calibration"` without comment

The hidden `action` input on the reset form is hard-coded to `"reset_calibration"` with no comment linking it to the server-side action dispatch logic.

---

### B07-20 | LOW | `html-jsp/vehicle/impact.jsp`:109 | Dead JavaScript trigger with no comment

`$('#calibration_slider').trigger('change')` (line 109) references an element `#calibration_slider` that does not exist anywhere in this file. There is no comment explaining whether this refers to an element in a parent page, whether the feature is deprecated, or whether this is dead code.

---

### B07-21 | LOW | `html-jsp/vehicle/impact.jsp`:112 | Magic slider range values without comment

The jQuery UI slider is initialised with `min: -95`, `max: 100`, `step: 5` and a computed `calValue` derived from `#FSSX_multiplicator`. None of these numeric constants are explained. The element ID `FSSX_multiplicator` is cryptic and undocumented.

---

### B07-22 | LOW | `html-jsp/vehicle/service.jsp`:1 | Missing page-level comment

No comment explains the Service tab's purpose, the two service type modes (`setHrs` vs `setIntval`), or how the hidden `servType` field interacts with the UI toggle.

---

### B07-23 | MEDIUM | `html-jsp/vehicle/service.jsp`:89–171 | Complex service-type conditional display logic with no comment

The service settings section uses four pairs of `<logic:equal/notEqual>` blocks to conditionally show or hide "Next Service Due At" and "Perform Service Every" input groups based on `servType`. The logic is spread across approximately 80 lines of interleaved open/closed `<div>` tags and Struts tags, making the structure very difficult to follow. There is no comment explaining the intended layout or which inputs are visible for which service type. Additionally, line 160 and 167 contain `data-serv-type="setHrs"` duplicated on elements whose `data-serv-type` is also `"interval"` — a likely bug, with no comment acknowledging it.

---

### B07-24 | LOW | `html-jsp/vehicle/view_job_details.jsp`:1 | Missing page-level comment

No comment explains the page's purpose, which action populates `arrJobDetails`, or the meaning of numeric status codes (1=Start, 2=Complete, 3=Pause) beyond what is visible in the template.

---

### B07-25 | LOW | `html-jsp/vehicle/view_job_details.jsp`:30–38 | Magic status integer codes without comment

Status values `1`, `2`, and `3` are hard-coded directly in `<logic:equal>` comparisons with no comment mapping them to named constants or linking them to a database enum. A maintainer adding a status (e.g., 4=Cancelled) has no guidance.

---

### B07-26 | LOW | `html-jsp/includes/adsleft.inc.jsp`:1 | Missing file-level comment

The fragment has no comment at the top stating it is a reusable sidebar include, what `sessAds` contains, the `length="3"` cap on displayed ads, or that the `display:none` on the container is intentional (presumably revealed by JavaScript elsewhere).

---

### B07-27 | LOW | `html-jsp/includes/adsleft.inc.jsp`:6 | `display:none` on ad container undocumented

The outer `<div id="adsleft" style="display:none">` is always hidden on page load. No comment explains whether JavaScript elsewhere is expected to make it visible, under what conditions, or whether this is intentional dead UI.

---

### B07-28 | LOW | `html-jsp/includes/adsleft.inc.jsp`:9 | Session key `sessAds` is cryptic and undocumented

The bean name `sessAds` is an abbreviated session key. No comment in this file or nearby explains what it holds (a list of `AdvertisementBean`), how it is populated, or which action/filter is responsible for setting it.

---

## Summary Table

| ID | Severity | File:Line | Short Description |
|----|----------|-----------|-------------------|
| B07-1 | LOW | subscription.jsp:1 | Missing page-level comment |
| B07-2 | LOW | subscription.jsp:74 | Magic `op_code` string `"edit_subscription"` undocumented |
| B07-3 | LOW | subscription.jsp:101 | Typo in user-visible success message, unacknowledged |
| B07-4 | LOW | access.jsp:1 | Missing page-level comment |
| B07-5 | LOW | access.jsp:77–81 | Magic keypad reader brand strings undocumented |
| B07-6 | LOW | adminUnitEdit.jsp:1 | Missing page-level comment |
| B07-7 | MEDIUM | adminUnitEdit.jsp:2–25 | Complex scriptlet (URL init + newId logic) with no comment |
| B07-8 | LOW | adminUnitEdit.jsp:170–172 | Hidden fields `oldId`/`newId`/`actionUnit` undocumented |
| B07-9 | LOW | assignment.jsp:1 | Missing page-level comment |
| B07-10 | MEDIUM | assignment.jsp:4 | `sessDateFormat` read and non-obvious transformation, no comment |
| B07-11 | LOW | assignment.jsp:73 | Magic hidden `action` value `"add"` undocumented |
| B07-12 | LOW | driver_job_details.jsp:1 | Missing page-level comment |
| B07-13 | MEDIUM | driver_job_details.jsp:85–106 | Dead/misplaced `fnsubmitAccount()` function, no comment |
| B07-14 | MEDIUM | driver_job_details.jsp:112 | Typo `#drivrId` silently misses hidden field, no comment |
| B07-15 | LOW | driver_job_details.jsp:21–35 | Commented-out form fields with no explanation |
| B07-16 | LOW | driver_job_details.jsp:65 | Commented-out placeholder JS line with no explanation |
| B07-17 | LOW | impact.jsp:1 | Missing page-level comment |
| B07-18 | MEDIUM | impact.jsp:6–11 | Direct session access with no null guard or comment; inconsistent with sibling tabs |
| B07-19 | LOW | impact.jsp:84 | Magic action string `"reset_calibration"` undocumented |
| B07-20 | LOW | impact.jsp:109 | Dead JS trigger on non-existent `#calibration_slider`, no comment |
| B07-21 | LOW | impact.jsp:112–121 | Magic slider constants and cryptic `FSSX_multiplicator` ID undocumented |
| B07-22 | LOW | service.jsp:1 | Missing page-level comment |
| B07-23 | MEDIUM | service.jsp:89–171 | Complex conditional display logic with no comment; duplicate `data-serv-type` attributes likely a bug |
| B07-24 | LOW | view_job_details.jsp:1 | Missing page-level comment |
| B07-25 | LOW | view_job_details.jsp:30–38 | Magic status integer codes (1/2/3) undocumented |
| B07-26 | LOW | adsleft.inc.jsp:1 | Missing file-level comment |
| B07-27 | LOW | adsleft.inc.jsp:6 | `display:none` on ad container undocumented |
| B07-28 | LOW | adsleft.inc.jsp:9 | Session key `sessAds` cryptic and undocumented |

**Total findings: 28** (6 MEDIUM, 22 LOW, 0 HIGH)
