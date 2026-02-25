# Pass 3 -- Documentation Audit: util package (G-Z)

**Auditor:** A20
**Date:** 2026-02-25
**Scope:** `WEB-INF/src/com/torrent/surat/fms6/util/` -- files G through Z (24 files)
**Branch:** `release/UAT_RELEASE_FLEETFOCUS_Production`

---

## Summary

| Severity | Count |
|----------|-------|
| HIGH     | 6     |
| MEDIUM   | 28    |
| LOW      | 16    |
| INFO     | 5     |

**Total Findings: 55**

All 24 files were read in full. No TODO/FIXME/HACK/XXX markers were found in any of the assigned files. The codebase exhibits a near-complete absence of Javadoc across all classes and public methods. The most critical gaps are around GDPR data deletion (no documentation of what data is deleted or the retention logic), password policy enforcement (no documentation of rules), and the migration utility (no schema documentation).

---

## File-by-File Findings

### 1. GdprDataDelete.java (143 lines)

**Reading Evidence:** Class with single public method `call_gdpr_delete_data()`. No class-level Javadoc. No method-level Javadoc. Deletes data from 6 tables: `fms_io_data_dtl`, `fms_io_data`, `fms_stat_data_dtl`, `fms_stat_data`, `fms_usage_data_dtl`, `fms_usage_data`, `op_chk_checklistanswer`, `op_chk_checklistresult`, `fms_unit_unlock_data`. Deletes records for inactive drivers (inactive > 30 days) based on a customer-configured `gdpr_data` retention period in years. Only targets drivers with `ACTIVE IS FALSE` and `inactive_date < current_date - interval '30 days'`.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 1 | HIGH | Class level | No class-level Javadoc. A GDPR deletion class MUST document: (a) what personal data is deleted, (b) the retention period logic, (c) eligibility criteria for deletion (inactive > 30 days), (d) the 6 master/detail table pairs affected. |
| 2 | HIGH | `call_gdpr_delete_data()` | No method Javadoc. This security-critical method performs irreversible deletion of personal data across 9 tables. Must document the deletion order (detail before master), the retention period source (`FMS_CUST_MST.gdpr_data`), and the inactive-driver filter. |
| 3 | INFO | Line 110 | Exception message references `send_timezone()` which is misleading -- this is `GdprDataDelete`. Copy-paste error in error message string. |

---

### 2. GetHtml.java (113 lines)

**Reading Evidence:** Utility class with 3 public methods: `getHTML(String, String)`, `getHTML1(String)`, `now(String)`. No class-level Javadoc. No method-level Javadoc. Contains a commented-out alternative `getHTML1` implementation using Apache HttpClient (lines 42-72).

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 4 | MEDIUM | Class level | No class-level Javadoc. Should document purpose (HTTP GET utility for report generation). |
| 5 | MEDIUM | `getHTML(String, String)` | No Javadoc. Should document parameters (URL base and parameter suffix), the 10-minute read timeout, and return value. |
| 6 | MEDIUM | `getHTML1(String)` | No Javadoc. Should document difference from `getHTML` (single URL parameter, 15-minute timeout, timing logs). |
| 7 | LOW | `now(String)` | No Javadoc on simple date formatting utility. |

---

### 3. ImportFiles.java (~1600+ lines)

**Reading Evidence:** HttpServlet (`@WebServlet("/servlet/Import_Files")`, `@MultipartConfig`) handling CSV file imports for drivers (standard, UK, AU), questions, questions-tab, and vehicles. Uses `doPost`. Contains many private validation helper methods. No class-level Javadoc. No method-level Javadoc on `doPost`.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 8 | MEDIUM | Class level | No class-level Javadoc. Should document the servlet purpose, supported import types (`drivers`, `driversUK`, `driversAU`, `questions`, `questions-tab`, `vehicles`), and the CSV format expectations for each. |
| 9 | MEDIUM | `doPost(...)` | No Javadoc on the main servlet entry point. Should document required request parameters (`src`, `customer`, `location`, `department`, `access_level`, `access_cust`, `access_site`, `access_dept`, `file`). |
| 10 | LOW | Private methods | Numerous private validation methods (`validateCSV`, `validateCSVIndividualD`, `validateCSVIndividual`, `validateCSVIndividualTab`, `validateQuestionLenghtTab`, `validateForMultiLangQstns`, `validateQstnPerLanguage`, `read`, `readQuestions`, `getFileName`) are undocumented, though being private reduces severity. |

---

### 4. InfoLogger.java (107 lines)

**Reading Evidence:** Logging utility that writes to both a file (`InfoLogs/fms.{date}.log`) and the `SEC_LOG_DETAILS` database table. Single public method `writelog(String)`. No class-level Javadoc. No method-level Javadoc.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 11 | MEDIUM | Class level | No class-level Javadoc. Should document dual logging (file + database). |
| 12 | MEDIUM | `writelog(String)` | No Javadoc. Should document the expected message format (`[uid/machineId] remarks`) which is parsed at lines 51-56, and the synchronized write behavior. |

---

### 5. LindeConfig.java (146 lines)

**Reading Evidence:** Configuration class that reads site settings from an XML file at `/home/gmtp/linde_config/settings.xml`. Many `public static` fields for site name, URLs, firmware settings, CSS paths, logo images. Constructor calls `readXMLFile()`. No class-level Javadoc. No method-level Javadoc.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 13 | MEDIUM | Class level | No class-level Javadoc. Should document that this is the site-specific configuration loader, the XML file location, and the supported site names (UK, AU, hiremech, westexe, MLA). |
| 14 | MEDIUM | `readXMLFile()` | No Javadoc. Should document the XML structure expected, file path fallback logic (`settings.xml` then `setting_au.xml`), and the static fields populated. |
| 15 | LOW | `now(String)` | No Javadoc on simple date formatting utility (duplicate of GetHtml.now). |

---

### 6. LogicBean_filter.java (475 lines)

**Reading Evidence:** JSP bean for report data retrieval with filters. Has a minimal block comment at class level: `"Business logic for retrival of data (based on filters) for the report 1."` Public methods: `clear_variables()`, `init()`, plus many getters/setters for ~25 ArrayList fields and string properties.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 16 | LOW | Class level | Existing block comment is minimal -- does not describe which report, the data source (`penom_database`), or the IO data fields. |
| 17 | LOW | `init()` | Inline comment `//Function called from the jsp page.` exists but is not Javadoc. Should be converted to Javadoc documenting DB connection and data fetch lifecycle. |
| 18 | LOW | `clear_variables()` | Has inline comment but no Javadoc. |
| 19 | LOW | Getters/setters | 25+ public getters undocumented. Low severity as they are simple bean accessors. |

---

### 7. LogicBean_filter1.java (782 lines)

**Reading Evidence:** Similar to LogicBean_filter but adds sorting and time conversion. Block comment: `"Business logic for retrival of data (based on filters and sort criteria set) for the report 2."` Additional public methods include sort-related setters and IO data total getters.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 20 | LOW | Class level | Existing block comment is minimal, same issue as LogicBean_filter. |
| 21 | LOW | `init()`, `clear_variables()` | Inline comments present but not Javadoc. |
| 22 | LOW | Getters/setters | 35+ public accessors undocumented. Low severity as simple bean properties. |

---

### 8. Menu_Bean.java (310 lines)

**Reading Evidence:** JSP bean that fetches menu modules and sub-modules based on user access rights. No class-level Javadoc. Public methods: `setOption`, `setemp_nm`, `setModule`, getters for `FormId`, `ApplicationPath`, `FormName`, `FormType`, `ModuleName`, `fetchform_rights`, `fetchMenuAttr1`, `fetchSubModule`, `clearVectors`, `init`, `getIcon_path`, `setSet_user_cd`, `getModuleDesc`.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 23 | MEDIUM | Class level | No class-level Javadoc. Should document that this bean provides menu/navigation data based on user group access rights. |
| 24 | MEDIUM | `fetchform_rights()` | No Javadoc. Security-relevant method that queries user group and form access rights. |
| 25 | MEDIUM | `fetchMenuAttr1()` | No Javadoc. Should document module fetching logic. |
| 26 | MEDIUM | `fetchSubModule()` | No Javadoc. Should document sub-module form fetching. |
| 27 | LOW | `init()` | No Javadoc. Entry point that dispatches to MOD or SUBMOD logic. |

---

### 9. Menu_Bean1.java (293 lines)

**Reading Evidence:** Nearly identical to Menu_Bean with minor differences (adds `form_desc` list, orders submodules by PRIORITY). No class-level Javadoc. Same public method set as Menu_Bean.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 28 | MEDIUM | Class level | No class-level Javadoc. Should document difference from Menu_Bean (priority ordering, form description). |
| 29 | MEDIUM | `fetchform_rights()`, `fetchMenuAttr1()`, `fetchSubModule()` | No Javadoc on any of these public methods. Same security-relevance as Menu_Bean. |
| 30 | INFO | Line 192 | Debug: `FormName.add(query1)` appends the raw SQL query string as a form name entry. Appears intentional for debugging but is undocumented and surprising. |

---

### 10. MigrateMaster.java (325 lines)

**Reading Evidence:** Single public method `callMigrateMaster()`. Migrates supervisor master data between two code level modes: SITE level (uses `FMS_LOC_OVERRIDE`) and DEPT level (uses `FMS_DEPT_OVERRIDE`). Reads from `FMS_CUST_MST`, `FMS_CUST_DEPT_REL`, `FMS_USR_VEHICLE_REL`, `FMS_VEHICLE_MST`, `FMS_VEHICLE_OVERRIDE`, `FMS_USR_MST`, `FMS_VER_STORE`. No class-level Javadoc. No method-level Javadoc.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 31 | HIGH | Class level | No class-level Javadoc. A migration utility MUST document: (a) the source and target schemas/tables, (b) the two migration modes (SITE vs DEPT level), (c) the data flow direction. |
| 32 | HIGH | `callMigrateMaster()` | No method Javadoc. Must document: (a) it processes all active customers, (b) SITE mode: copies first vehicle's override to `FMS_LOC_OVERRIDE`, (c) DEPT mode: populates `FMS_DEPT_OVERRIDE` from vehicle overrides, (d) max 40 supervisors per department, (e) sets `supervisor_access` to `'1&2&4'`. |
| 33 | INFO | Lines 202-230 | Large block of commented-out code for outgoing message insertion. Should be documented or removed. |

---

### 11. PasswordExpiryAlert.java (102 lines)

**Reading Evidence:** Single public method `checkExpiry()`, one private helper `isValid(String)`. No class-level Javadoc. No method-level Javadoc. Sends password expiry warning emails. Logic: finds users whose `last_pass_update` is within 7 days of 3-month expiry, where customer has `pword_restriction` enabled and `pword_alert_sent` is false.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 34 | HIGH | Class level | No class-level Javadoc. A password/security class MUST document the rules enforced: 3-month password lifetime, 7-day advance warning, customer-level `pword_restriction` toggle, one-time alert flag. |
| 35 | HIGH | `checkExpiry()` | No method Javadoc. Must document: (a) the 3-month expiry interval, (b) the 7-day warning window, (c) the email insertion to `email_outgoing` table, (d) the `pword_alert_sent` flag update to prevent duplicate alerts. |

---

### 12. PurgeData.java (5 lines)

**Reading Evidence:** Empty class. No fields, no methods, no Javadoc.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 36 | INFO | Class level | Empty class with no Javadoc. Should document whether this is a placeholder, deprecated, or pending implementation. |

---

### 13. RuntimeConf.java (156 lines)

**Reading Evidence:** Configuration constants class. All fields are `public static` (some `final`, some not). Contains database JNDI names, FTP credentials, firmware paths, SMS API credentials, UI constants, and feature-flag form codes. No class-level Javadoc. No method-level Javadoc (no methods).

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 37 | MEDIUM | Class level | No class-level Javadoc. Should document that this is the central runtime configuration with JNDI datasource names, firmware server settings, SMS API config, and feature constants. |
| 38 | MEDIUM | Fields | No Javadoc on any of the ~80+ public static fields. Many have inline comments but no formal documentation. Especially important for security-sensitive fields like `PASSWORD`, `firmwarepass`, `USERNAME`, `API_ID`. |

---

### 14. SendMessage.java (242 lines)

**Reading Evidence:** SMS sending utility using Clickatell API. Public method: `init()`. Private methods: `send_all_sms()`, `send_sms_message(...)`, `readLines(...)`. The private `send_all_sms` has a Javadoc comment (`"Retrieves all outgoing email and send"`). The private `send_sms_message` has a Javadoc comment with param descriptions.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 39 | MEDIUM | Class level | No class-level Javadoc. Should document that this sends SMS messages via Clickatell API from the `sms_outgoing` table. |
| 40 | MEDIUM | `init()` | No Javadoc on the public entry point. Should document that it connects to DB and dispatches all pending SMS. |
| 41 | INFO | `send_sms_message(...)` (private) | Has Javadoc but describes params using PHP-style `@param integer $id` instead of Java-style `@param id`. Inaccurate documentation style. |

---

### 15. SupervisorMasterHelper.java (446 lines)

**Reading Evidence:** Three public methods: `deleteSupervisorByUser(...)`, `deleteSupervisor(...)`, `deleteSuperMaster(...)`. No class-level Javadoc. No method-level Javadoc. Manages supervisor master list deletion at site and department levels, sending IDMAST/IDSMAST commands to vehicles via the `outgoing` table.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 42 | MEDIUM | Class level | No class-level Javadoc. Should document that this helper manages supervisor override deletion and vehicle communication. |
| 43 | MEDIUM | `deleteSupervisorByUser(String, String, String, String, String)` | No Javadoc. Should document: 5 parameters (user, cust_cd, loc_cd, dept_cd, access_user), site vs dept level deletion, supervisor_access reset to '0&0&0', IDMAST messaging. |
| 44 | MEDIUM | `deleteSupervisor(String, String, String, String, String)` | No Javadoc. Should document: slot-based deletion, master_code_level lookup, difference from `deleteSupervisorByUser`. |
| 45 | MEDIUM | `deleteSuperMaster(int, String)` | No Javadoc. Should document: super_master_override table deletion, IDSMAST command difference from IDMAST. |

---

### 16. UtilBean.java (413 lines)

**Reading Evidence:** JSP utility bean with date/time retrieval, customer settings lookup, and CLD (Customer/Location/Department) lookup. Has a minimal block comment: `"This DataBean retrives date and provides functionality to get days in a given month"`. Public methods: `getGen_dt/setGen_dt`, `getDays(int, int)`, `getLocalTime(String, String)`, `init()`, `getCustomerSettingByUser(String)`, `getCustomerSetting(String)`, `getCustLocDeptBeanByUser(String)`, `template()`, plus additional getters/setters.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 46 | MEDIUM | Class level | Existing block comment is incomplete -- does not mention customer settings, local time conversion, or CLD lookup. |
| 47 | MEDIUM | `getLocalTime(String, String)` | No Javadoc. Should document timezone conversion via `time_zone_impl` DB function. |
| 48 | MEDIUM | `getCustomerSettingByUser(String)` | No Javadoc. Should document that it retrieves password policy settings for a user's customer. |
| 49 | MEDIUM | `getCustomerSetting(String)` | No Javadoc. Should document that it retrieves password policy directly by customer code. |
| 50 | LOW | `getDays(int, int)` | Has inline comment but no Javadoc. |
| 51 | LOW | `template()` | Has inline comment `//TEMPLATE FOR DB UTILS` but no Javadoc explaining this is a code template, not functional code. |

---

### 17. call_mail.java (~1100+ lines)

**Reading Evidence:** Email sending utility with multiple public methods: `Ename(String)`, `call_email_au()`, `call_email()`, `call_alertemail()`, `calibrate_impact()`, `sendMail(...)`, `sendMail1(...)`, `now(String)`, `callLindeReports()`, plus getters/setters for `email` and `debug`. No class-level Javadoc. No method-level Javadoc.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 52 | MEDIUM | Class level | No class-level Javadoc. Should document the email dispatch system, supported email types (scheduled reports, alerts), and the email_outgoing table processing. |
| 53 | MEDIUM | `call_email_au()`, `call_email()` | No Javadoc. Should document scheduled email report generation and dispatch. |
| 54 | MEDIUM | `call_alertemail()` | No Javadoc. Should document alert email processing. |
| 55 | MEDIUM | `calibrate_impact()` | No Javadoc. Name is misleading for a method in an email class -- should document its actual purpose. |
| 56 | MEDIUM | `sendMail(...)`, `sendMail1(...)` | No Javadoc. Should document the SMTP sending mechanism. |
| 57 | MEDIUM | `callLindeReports()` | No Javadoc. Should document Linde-specific report generation. |

---

### 18. escapeSingleQuotes.java (19 lines)

**Reading Evidence:** Single public method `replaceSingleQuotes(String)`. No class-level Javadoc. No method-level Javadoc. Doubles single quotes for SQL escaping.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 58 | LOW | Class level | No Javadoc. Simple utility class, low severity. Class name violates Java naming conventions (lowercase). |
| 59 | LOW | `replaceSingleQuotes(String)` | No Javadoc. Should document that it escapes single quotes by doubling them (SQL injection prevention). |

---

### 19. fix_department.java (388 lines)

**Reading Evidence:** Two public methods: `show_cust_dept()`, `fix_dept(String, String, String)`. Plus getters/setters for ArrayLists (customers, sites, departments, user_cds, loc_cds, dept_cds) and a `msg` field. No class-level Javadoc. No method-level Javadoc. Fixes duplicate department codes by creating new department entries and updating ~12 related tables.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 60 | MEDIUM | Class level | No class-level Javadoc. Should document that this is a data repair utility for fixing shared/duplicate department codes across multiple customers. |
| 61 | MEDIUM | `fix_dept(String, String, String)` | No Javadoc. Should document the 12 tables updated (`FMS_CUST_DEPT_REL`, `FMS_OPCHK_QUEST_MST`, `FMS_USER_DEPT_REL`, `FMS_USR_VEHICLE_REL`, `dayhours`, `fms_can_input_settings`, `fms_impact_month_cache`, `fms_impact_month_driver_cache`, `fms_monthly_rpt_subscription`, `mymessages_users`, `FMS_EMAIL_CONF`, `site_settings_by_hour`). |
| 62 | LOW | `show_cust_dept()` | No Javadoc. Should document that it populates the department listing for display. |

---

### 20. mail.java (311 lines)

**Reading Evidence:** Email utility class. Public methods: `Ename(String)`, `sendMail(String, String, String, String, String, String)` (instance), `sendMail(String, String, String, String, String, String, String, String)` (static, with attachment), `sendMailAttachment(...)` (static). No class-level Javadoc. No method-level Javadoc.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 63 | MEDIUM | Class level | No class-level Javadoc. Should document the email sending utility and supported modes (plain, with attachment, auto-CSV-from-HTML). |
| 64 | MEDIUM | `sendMail(...)` (instance) | No Javadoc. Should document the JNDI mail session lookup and plain HTML email sending. |
| 65 | MEDIUM | `sendMail(...)` (static, 8 params) | No Javadoc. Should document the file attachment variant. |
| 66 | MEDIUM | `sendMailAttachment(...)` | No Javadoc. Should document the HTML-table-to-CSV auto-attachment feature using Jsoup parsing. |

---

### 21. password_life.java (187 lines)

**Reading Evidence:** Decompiled class (header comment: "Decompiled by DJ v3.9.9.91"). Manages password lifetime checks. Public methods: `clear_variables()`, `setUser(String)`, `setIp(String)`, `setLogindate(String)`, `setLogintime(String)`, `loadDefaultValues()`, `getCount()`, `getDiff()`, `getLogin_status()`, `getCount1()`, `getRem()`, `init()`. Uses Oracle SQL syntax (`nvl`, `sysdate`, `decode`, `sign`). No Javadoc.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 67 | MEDIUM | Class level | No class-level Javadoc. Password security class should document: Oracle-specific password lifecycle checking, the `fms_password_life` configuration table, and the expiry/reminder calculation logic. |
| 68 | MEDIUM | `loadDefaultValues()` | No Javadoc. Should document: password reset flag check, lifetime retrieval from `fms_password_life`, expiry date calculation, login status recording. |
| 69 | LOW | Getters | `getCount()`, `getDiff()`, `getRem()`, `getCount1()` have no Javadoc. Names are cryptic -- `getCount()` returns whether password is expired, `getDiff()` returns days until expiry, `getRem()` returns reminder threshold, `getCount1()` returns reset flag. |

---

### 22. password_policy.java (159 lines)

**Reading Evidence:** Manages password policy constraints (username/password min/max lengths). Public methods: `clear_variables()`, `setUser(String)`, `setIp(String)`, `setLogindate(String)`, `setLogintime(String)`, `loadDefaultValues()`, `getUmin()`, `getUmax()`, `getPmin()`, `getPmax()`, `init()`. Uses Oracle SQL syntax (`sysdate`). No Javadoc.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 70 | HIGH | Class level | No class-level Javadoc. A password policy class MUST document the rules enforced: username length min/max (`u_min`/`u_max`), password length min/max (`p_min`/`p_max`), the source table (`fms_password_life`), and the effective-date lookup logic. |
| 71 | MEDIUM | `loadDefaultValues()` | No Javadoc. Should document: effective-date-based policy lookup, the 4 policy fields retrieved (userid_min, userid_max, password_min, password_max). |
| 72 | LOW | `getUmin()`, `getUmax()`, `getPmin()`, `getPmax()` | No Javadoc. Names are abbreviated and unclear without documentation. |

---

### 23. send_timezone.java (417 lines)

**Reading Evidence:** Three public methods: `call_send_timezone()`, `call_send_timezone_test()`, `call_send_timezone_au()`. Sends TZONE messages to vehicle units during DST transitions. UK logic: last Sunday of March (TZONE=60) and October (TZONE=0). AU logic: first Sunday of October and April, with AEDT and ACDT variants. No class-level Javadoc. No method-level Javadoc.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 73 | MEDIUM | Class level | No class-level Javadoc. Should document the DST timezone synchronization for vehicle fleet units. |
| 74 | MEDIUM | `call_send_timezone()` | No Javadoc. Should document: UK DST transitions, TZONE message format, England-only vehicle targeting, `FMS_STATE_MST.DST` update. |
| 75 | MEDIUM | `call_send_timezone_au()` | No Javadoc. Should document: AU DST transitions for AEDT (NSW/VIC/ACT/TAS) and ACDT (SA) zones, state-based vehicle filtering. |
| 76 | LOW | `call_send_timezone_test()` | No Javadoc. Appears to be a test/debug variant of `call_send_timezone()` with relaxed conditions (line 152 removes the DST check for October). |

---

### 24. send_updatepreop.java (601 lines)

**Reading Evidence:** Pre-operational checklist synchronization utility. Public methods: `updatepreop()`, `resyncPreop(List<String>)`, `intToByteArray(int)`. No class-level Javadoc. No method-level Javadoc. Generates binary PREOP.TXT/PREOP100.TXT/PREOP150.TXT files and sends FTP upload commands to vehicles.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| 77 | MEDIUM | Class level | No class-level Javadoc. Should document: pre-op checklist file generation, binary format specification, firmware version-dependent file selection. |
| 78 | MEDIUM | `updatepreop()` | No Javadoc. Should document: historical checklist answer correction from 2019-04-01 onward, the question matching logic. |
| 79 | MEDIUM | `resyncPreop(List<String>)` | No Javadoc. Should document: the vehTCds list format (`vehicleType,customer,location,department`), FTP upload command generation, three file format variants (PREOP.TXT for legacy/50 chars, PREOP100.TXT for MK2 v2.1.70+/100 chars, PREOP150.TXT for MK3 v5.2.x/150 chars). |
| 80 | LOW | `intToByteArray(int)` | No Javadoc. Should document little-endian byte conversion for the binary file format. |

---

## Accuracy Issues in Existing Documentation

| # | File | Location | Issue |
|---|------|----------|-------|
| A1 | GdprDataDelete.java | Line 110 | Exception message says `"Exception in the send_timezone() Method..."` but this is the GDPR delete class. Misleading. |
| A2 | fix_department.java | Line 64, 276 | Exception message says `"Exception in the send_timezone() Method..."` but this is the fix_department class. Same copy-paste error. |
| A3 | LogicBean_filter.java | Line 208 | Exception message references `"LogicBean_LoginAlerter"` but this is `LogicBean_filter`. |
| A4 | LogicBean_filter1.java | Line 398 | Exception message references `"LogicBean_LoginAlerter"` but this is `LogicBean_filter1`. |
| A5 | password_policy.java | Line 94 | Error message says `"Exception in the loadDefaultvalues() Method of password_life..."` but this is `password_policy`. |
| A6 | password_policy.java | Line 137 | Error message says `"password_life in..."` but this is `password_policy.init()`. |
| A7 | SendMessage.java | Lines 100-110 | Private method `send_sms_message` has Javadoc comment describing it as "sending out email" when it actually sends SMS. |

---

## Special Attention Areas

### GDPR Deletion (GdprDataDelete.java)
**Data deleted (UNDOCUMENTED):**
- `fms_io_data_dtl` / `fms_io_data` -- IO telemetry data (detail/master)
- `fms_stat_data_dtl` / `fms_stat_data` -- Statistical data (detail/master)
- `fms_usage_data_dtl` / `fms_usage_data` -- Usage data (detail/master)
- `op_chk_checklistanswer` / `op_chk_checklistresult` -- Pre-op checklist results
- `fms_unit_unlock_data` -- Unit unlock records

**Eligibility:** Inactive drivers (`ACTIVE IS FALSE`, `inactive_date < current_date - 30 days`) belonging to customers with non-zero `gdpr_data` setting. Retention period: customer-defined in years via `FMS_CUST_MST.gdpr_data`.

### Password Policy (password_policy.java, password_life.java, PasswordExpiryAlert.java)
**Rules enforced (UNDOCUMENTED):**
- `password_policy`: Username length (min/max), password length (min/max) from `fms_password_life` table
- `password_life`: Password lifetime in days, reminder period in days, reset flag check, all from `fms_password_life`
- `PasswordExpiryAlert`: 3-month expiry interval, 7-day advance email warning, customer-level `pword_restriction` toggle, one-time `pword_alert_sent` flag

### Migration (MigrateMaster.java)
**Schemas/tables involved (UNDOCUMENTED):**
- Source: `FMS_CUST_MST`, `FMS_CUST_DEPT_REL`, `FMS_USR_VEHICLE_REL`, `FMS_VEHICLE_MST`, `FMS_VEHICLE_OVERRIDE`, `FMS_USR_MST`, `FMS_VER_STORE`
- Target (SITE mode): `FMS_LOC_OVERRIDE`
- Target (DEPT mode): `FMS_DEPT_OVERRIDE`
- Updated: `FMS_USR_MST.supervisor_access`

---

## TODO/FIXME/HACK/XXX Markers

**None found** in any of the 24 assigned files.

---

*End of Pass 3 audit for util package (G-Z). Report only -- no fixes applied.*
