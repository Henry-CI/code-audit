# Security Audit Report — Executables, SQL, Tag Libraries, and Miscellaneous
**Agent:** A19
**Audit run:** 2026-02-25-01
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Date:** 2026-02-25

---

## STEP 2 — FILES EXAMINED

### A. Executables directory

| File | Size (approx) | Type |
|------|---------------|------|
| `C:\Projects\cig-audit\repos\fleetfocus\executables\gmtp_outgoing_queue\gmtp_outgoing_queue.sh` | ~2.5 KB | Bash shell script |

Note: the directory is named `executables/gmtp_outgoing_queue/` but contains only one file, which is a shell script — not a compiled binary. The directory name "executables" is misleading; however the script contains sensitive material (see findings below).

### B. SQL files

| File | Purpose |
|------|---------|
| `sql/AU-KION-FF-2003.sql` | State master table updates — timezone/locale data for SGP, IDN, THA, PHL, MYS, KHM, HKG |
| `sql/FF-1592.sql` | Index creation on FMS_USR_MST, FMS_USER_DEPT_REL, FMS_USR_VEHICLE_REL, FMS_USR_VEHICLE_REL_HISTORY, FMS_VEHICLE_MST, FMS_VER_STORE, fms_io_field_mst |
| `sql/FF-2064.sql` | DDL for danger_tag_settings, danger_tag_settings_history, vor_new_settings, vor_new_settings_history, fms_io_data_tech_lockout, fms_usage_data_tech_lockout, fms_seen_data_tech_lockout; inserts into FMS_FORM_MST_NEW |
| `sql/FF-2205.sql` | Index creation for danger_tag_settings_history, vor_new_settings_history, fms_io_data_tech_lockout |
| `sql/RELEASE_AU-FF_DEC2021_JAN2022.sql` | ALTER TABLE to add TECH_NUMBER column to FMS_SPARE_MODULES |
| `sql/RELEASE_AU-FF_MAR2023.sql` | ALTER TABLE to add SHOW_COMMENT and RANDOMISATION columns to FMS_VEHICLE_MST and FMS_OPCHK_QUEST_MST |
| `sql/RELEASE_AU-FF_OCT2021.sql` | Function definitions: sp_store_json, sp_store_msgrsp, sp_store_preop_comments; DDL for fms_canbus_data*, op_chk_checklistresult_comments |
| `sql/RELEASE_AU-FF_ThaiSupport.sql` | ALTER TABLE for Thai language support columns; DDL for FMS_CHCKLIST_LANG_SETTING |
| `sql/fleetfocus-schema-apr02-2025-dump.sql` | Full PostgreSQL schema dump (~large); all table/function definitions for production database. Dumped 2025-04-02 from PostgreSQL 11.20 by pg_dump 13.4 |
| `sql/fleetfocus-schema-apr02-2025-update.sql` | Appears identical in header to dump file; same schema — likely a second copy or update script |
| `sql/adhoctask/April232024/UnwantedCustomerSitesDeletionWoolworths.sql` | Ad-hoc customer data deletion script targeting customer "Woolworths" (CUST_CD 233), sites "zz- inactiveLarapinta BRDC 1" (LOC_CD 1126) and "zz- inactiveLarapinta BRDC 2" (LOC_CD 1138) |

**Tables referenced across SQL files:**
FMS_STATE_MST, FMS_USR_MST, FMS_USER_DEPT_REL, FMS_USR_VEHICLE_REL, FMS_USR_VEHICLE_REL_HISTORY, FMS_VEHICLE_MST, FMS_VER_STORE, fms_io_field_mst, danger_tag_settings, danger_tag_settings_history, vor_new_settings, vor_new_settings_history, fms_io_data_tech_lockout, fms_usage_data_tech_lockout, fms_seen_data_tech_lockout, FMS_FORM_MST_NEW, FMS_SPARE_MODULES, FMS_OPCHK_QUEST_MST, FMS_CHCKLIST_LANG_SETTING, fms_canbus_data, fms_canbus_data_cache, fms_canbus_data_dtl, fms_canbus_data_dtl_cache, fms_io_field_mst, op_chk_checklistresult_comments, broadcastmsg, FMS_LOC_MST, FMS_DEPT_MST, FMS_CUST_DEPT_REL, FMS_USR_CUST_REL.

**Stored procedures defined in storeproc/ directory:**

| File | Function Name | Purpose |
|------|--------------|---------|
| sp_card_ext_message.sql | public.sp_card_ext_message | Driver card authentication with customer/site scoping |
| sp_cardmessage.sql | public.sp_cardmessage | Legacy driver card authentication |
| sp_driver_shock_message.sql | public.sp_driver_shock_message | Records forklift impact/shock events |
| sp_email_idle_alert.sql | public.sp_email_idle_alert | Sends idle-time email alerts |
| sp_email_invalid_driver.sql | public.sp_email_invalid_driver | Sends unauthorized driver email alerts |
| sp_email_invalid_driver_with_drivercd.sql | public.sp_email_invalid_driver_with_drivercd | Sends unauthorized driver alerts with driver code |
| sp_email_question_alert.sql | public.sp_email_question_alert | Sends critical checklist failure email alerts |
| sp_email_shock_alert.sql | public.sp_email_shock_alert | Sends impact threshold email alerts |
| sp_email_survey_timeout_alert.sql | public.sp_email_survey_timeout_alert | Sends pre-op survey timeout email alerts |
| sp_email_unknown_driver.sql | public.sp_email_unknown_driver | Sends unknown driver email alerts |
| sp_email_unknown_driver_custcd.sql | public.sp_email_unknown_driver_custcd | Unknown driver alerts scoped to customer code |
| sp_email_unknown_driver_custcd_sitecd.sql | public.sp_email_unknown_driver_custcd_sitecd | Unknown driver alerts scoped to customer and site |
| sp_eos_message.sql | public.sp_eos_message | Processes end-of-session (EOS) telemetry messages |
| sp_generic_gmtp_data_message.sql | public.sp_generic_gmtp_data_message | Routes generic GMTP protocol messages to specific handlers |
| sp_gpsemessage.sql | public.sp_gpsemessage | Stores GPS telemetry data |
| sp_opchks_response.sql | public.sp_opchks_response | Processes pre-operational checklist responses |
| sp_pstat_message.sql | public.sp_pstat_message | Stores vehicle status (PSTAT) telemetry |
| sp_store_danger_tag_msg.sql | public.sp_store_danger_tag_msg | Processes danger tag enable/disable messages |
| sp_store_lockout.sql | public.sp_store_lockout | Processes maintenance lockout (MAINT) messages |
| sp_store_mk3dbg.sql | public.sp_store_mk3dbg | Stores MK3 debug version information |
| sp_store_preop_lang.sql | public.sp_store_preop_lang | Stores unit language configuration |
| sp_store_prompt_type.sql | public.sp_store_prompt_type | Stores pre-op prompt type data |
| sp_store_seenmsg.sql | public.sp_store_seenmsg | Processes SEEN (seen-data) telemetry messages |
| sp_store_unit_params.sql | public.sp_store_unit_params | Stores unit parameters (PAR= message) |
| sp_store_usage_msg.sql | public.sp_store_usage_msg | Stores USAGE telemetry messages |
| sp_store_vor_new_msg.sql | public.sp_store_vor_new_msg | Processes VOR (Vehicle Off Road) status messages |
| sp_supermaster_message.sql | public.sp_supermaster_message | Processes SMAST (super-master) session data |
| sp_update_connection.sql | public.sp_update_connection | Records TCP connection open/close events |
| update_last_reported.sql | public.update_last_reported | Updates last-session timestamps on vehicles and users |

### C. WEB-INF Tag Library Files

**taglibs-mailer.tld** — Jakarta Apache Taglibs Mailer 1.1
TLD version: 1.1, JSP version: 1.1
URI: `http://jakarta.apache.org/taglibs/mailer-1.1`
Tags defined: `mail`, `server`, `message`, `header`, `setrecipient`, `addrecipient`, `replyto`, `from`, `attach`, `subject`, `send`, `error`
Security-relevant attributes on `mail` tag: `server` (rtexprvalue=yes), `user` (rtexprvalue=yes), `password` (rtexprvalue=yes), `to`, `from`, `cc`, `bcc`, `subject`, `authenticate`

**taglibs-request.tld** — Jakarta Apache Taglibs Request 1.0.1
TLD version: 1.0.1, JSP version: 1.1
URI: `http://jakarta.apache.org/taglibs/request-1.0`
Tags defined: `log`, `request`, `isSecure`, `isSessionFromCookie`, `isSessionFromUrl`, `isSessionValid`, `isUserInRole`, `attribute`, `attributes`, `equalsAttribute`, `existsAttribute`, `removeAttribute`, `setAttribute`, `cookie`, `cookies`, `equalsCookie`, `existsCookie`, `header`, `headers`, `equalsHeader`, `existsHeader`, `headerValues`, `parameter`, `parameters`, `equalsParameter`, `existsParameter`, `parameterValues`, `queryString`, `queryStrings`, `existsQueryString`

**vssver2.scc** — Visual SourceSafe binary metadata file
Binary file, approximately 200 bytes. Visible plaintext content: `$/WEB-INF taglibs-mailer.tld taglibs-request.tld web.xml web.xml1 .cvsignore` — reveals filenames tracked under the legacy VSS repository. The file itself is present at WEB-INF/vssver2.scc. The .gitattributes file also lists vssver2.scc files at: WEB-INF/classes/META-INF/vssver2.scc, WEB-INF/classes/com/torrent/surat/fms6/master/vssver2.scc, WEB-INF/classes/com/torrent/surat/fms6/reports/vssver2.scc, WEB-INF/classes/com/torrent/surat/fms6/security/vssver2.scc, WEB-INF/classes/com/torrent/surat/fms6/util/vssver2.scc, WEB-INF/src/META-INF/vssver2.scc, WEB-INF/src/com/torrent/surat/fms6/master/vssver2.scc, WEB-INF/src/com/torrent/surat/fms6/reports/vssver2.scc, WEB-INF/src/com/torrent/surat/fms6/security/vssver2.scc, WEB-INF/src/com/torrent/surat/fms6/util/vssver2.scc, WEB-INF/src/vssver2.scc, WEB-INF/lib/vssver2.scc, css/vssver2.scc, dyn_report/vssver2.scc, home/vssver2.scc, images/linde/vssver2.scc, images/linde/menu/vssver2.scc, images/pics/vssver2.scc, images/vssver2.scc.

### D. .class files outside WEB-INF/lib/ or work/

Two .class files were found outside WEB-INF/lib/, located in the `work/` directory:

- `C:\Projects\cig-audit\repos\fleetfocus\work\org\apache\jsp\pages\admin\setting\driver_005flimiting_005fby_005ftruck_jsp.class`
- `C:\Projects\cig-audit\repos\fleetfocus\work\org\apache\jsp\pages\admin\setting\driver_005fsettings_005fto_005funit_jsp.class`

Corresponding .java source files are also committed:
- `work\org\apache\jsp\pages\admin\setting\driver_005flimiting_005fby_005ftruck_jsp.java`
- `work\org\apache\jsp\pages\admin\setting\driver_005fsettings_005fto_005funit_jsp.java`

These are Tomcat-compiled JSP files (JSP servlet wrapper classes generated by Jasper). `git ls-files work/` confirms they are tracked by git. The `.gitignore` file contains `/work/` which should exclude this directory, but these files were committed before or despite the gitignore entry. Git history shows they originate from the "First Import" commit.

### E. .gitattributes

The `.gitattributes` file is approximately 700+ lines and enumerates nearly every file in the repository with `-text` to prevent CRLF/LF conversion. It also includes `svneol=unset#text/plain` on a small number of source files, indicating a multi-stage migration history (VSS → SVN → Git). The file itself is not security-sensitive in content, but its size and the legacy control system markers it contains are operationally relevant.

Key security-relevant observations:
1. The `-text` attribute is applied to binary files (images, .class, .jar, .xlsx, .ico, .bmp, .db), which is appropriate to prevent corruption but has no diff-suppression effect on text files.
2. The `.gitattributes` does NOT use `diff=` or `filter=` directives on any file type that would suppress diffs or run smudge/clean filters. No entries appear designed to hide secrets.
3. Entries explicitly tracking `.class` files (lines 7-54) confirm that compiled class files under `WEB-INF/classes/` were committed. These paths are listed for binary treatment but those actual files may or may not be physically present (they are listed in .gitattributes but the WEB-INF/classes/ directory is in .gitignore).
4. The file lists `excelrpt/20140620102938-5b6ef784-b385-413d-951e-035f0ac920cd.xlsx` and `excelrpt/20140620104936-d436a7db-b399-438c-b730-ab33b2fa9dbb.xlsx` — Excel report files committed to the repository.
5. Multiple `vssver2.scc` files are explicitly listed as `-text`, indicating they were committed at initial import and recognized by git as binary.

---

## STEP 4 — SECURITY REVIEW ANALYSIS

### Executables (gmtp_outgoing_queue.sh)

The file is a Bash shell script, not a compiled binary. Its purpose is to monitor the GMTP outgoing message queue by telnetting to localhost port 9494, authenticating with hardcoded credentials, checking queue depth against a threshold, and sending alert emails if the threshold is exceeded.

**Critical finding:** The script contains:
- A hardcoded telnet username: `gmtp` (line 26: `send "gmtp\r"`)
- A hardcoded telnet password: `gmtp!telnet` (line 31: `send "gmtp!telnet\r"`)
- Three hardcoded internal staff email addresses: `hui@collectiveintelligence.com.au`, `roland@collectiveintelligence.com.au`, `dev@collectiveintelligence.com.au`

This script is committed to a Git repository. Anyone with read access to the repository now has the GMTP management interface credentials. The GMTP service management interface listens on localhost:9494 and this password would allow an attacker with local system access to interact directly with the GMTP message queue.

### SQL Scripts

**No hardcoded database connection strings or passwords were found** in the migration SQL files or stored procedure definitions. The schema dump correctly shows that the database user is `gmtp`, consistent with the application's database account, but no passwords are embedded.

**Schema dump in version control:** The files `sql/fleetfocus-schema-apr02-2025-dump.sql` and `sql/fleetfocus-schema-apr02-2025-update.sql` are full production database schema dumps including all table definitions, function bodies, sequence definitions, and constraints. The dump header confirms it was taken from production PostgreSQL 11.20 on 2025-04-02. Committing a full schema dump to a source repository exposes the complete database structure to anyone with repository access.

**Ad-hoc task script — customer data reference:** The file `sql/adhoctask/April232024/UnwantedCustomerSitesDeletionWoolworths.sql` explicitly names a real customer (`-- '233' is Customer Woolworths`) and their specific site codes and site names in comments. While this is a deletion script for decommissioned sites, it represents real operational data (customer identity, site IDs, internal codes) committed to version control with no obvious need for permanent retention.

**SQL Injection analysis — stored procedures:** All 29 stored procedures were reviewed. All use parameterized query patterns (PL/pgSQL function parameters $1, $2, etc.) throughout. None construct dynamic SQL strings via string concatenation that would be vulnerable to second-order SQL injection from within PL/pgSQL itself. Input data from messages is parsed using PostgreSQL built-in string functions (split_part, substring, string_to_array) and then used as values in INSERT/UPDATE/SELECT statements with typed parameters — this is the correct approach and does not create SQL injection vectors.

One minor note: several functions use `ILIKE` for case-insensitive matching on CARD_ID fields, which is correct business logic (card identifiers are hex strings) and does not create injection risk given the parameterized structure.

### Tag Libraries

**taglibs-mailer.tld:** This is a standard Apache Jakarta Taglibs Mailer 1.1 descriptor. It does not contain any hardcoded SMTP server addresses, credentials, or email addresses. The `password` attribute on the `<mail>` tag supports `rtexprvalue=yes`, meaning password values can be supplied at runtime via EL expressions — this is the intended design. The embedded documentation examples use placeholder addresses (foo@home.net, bar@home.net) only.

The tag library itself does not introduce email injection risk through its TLD definition. Whether email injection is possible depends on how JSP pages use the tags — specifically whether `to`, `cc`, `bcc`, and `subject` attributes are populated with unsanitized user input. This is outside the scope of the TLD file itself.

**taglibs-request.tld:** Standard Apache Jakarta Taglibs Request 1.0.1. Contains no hardcoded values. The `isUserInRole` tag (`role` attribute, required) could be security-relevant if role names are constructed dynamically from user input in JSP pages, but the tag library definition itself is safe. The `attribute`, `setAttribute`, `removeAttribute` tags manipulate request attributes — their security impact depends on JSP-level usage, not the TLD.

### Visual SourceSafe Files

Multiple `vssver2.scc` files are present in the repository and tracked by git. The WEB-INF/vssver2.scc file was directly read; its binary content reveals filenames from the original VSS repository (`$/WEB-INF taglibs-mailer.tld taglibs-request.tld web.xml web.xml1 .cvsignore`). The VSS path `$/WEB-INF` reveals the legacy project root path structure. No VSS server addresses, usernames, or passwords were visible in the decoded content of the one file read; however, vssver2.scc files can contain additional binary-encoded metadata.

### .gitattributes (70 KB)

The file is large because it enumerates nearly every committed file individually with the `-text` attribute. This was typical practice for repositories migrated from VSS or SVN where binary/text handling was managed explicitly. The security implications:

1. No `filter=` or `smudge/clean` attributes are used, so there is no risk of secret injection via git attributes.
2. No `diff=` override entries are present that would suppress showing diffs for specific file types in code review.
3. The file explicitly lists compiled `.class` files under `WEB-INF/classes/` — confirming these were committed at project inception, though the current `.gitignore` excludes that directory.
4. The explicit listing of two `.xlsx` files (`excelrpt/`) in .gitattributes confirms they were committed to git.
5. From a security-review standpoint, the file does not contain any content that would prevent detection of secrets committed via normal `git diff` or `git log` operations.

### Compiled JSP files in work/

The `work/` directory contains Tomcat/Jasper-generated intermediate JSP compilation artifacts that were committed at the initial project import ("First Import" commit). These are:
- `driver_005flimiting_005fby_005ftruck_jsp.class` and `.java` (the `%5f` URL-encoded characters represent underscores, making the file name `driver_limiting_by_truck_jsp`)
- `driver_005fsettings_005fto_005funit_jsp.class` and `.java`

Although `.gitignore` lists `/work/`, this was applied after initial import, so these files remain tracked. The `.java` files expose server-side JSP implementation details. The `.class` files are compiled bytecode that could be decompiled to recover JSP logic for pages in `pages/admin/setting/`.

---

## STEP 5 — FINDINGS

---

### A19-1 — Hardcoded Credentials in Monitoring Script

**File:** `C:\Projects\cig-audit\repos\fleetfocus\executables\gmtp_outgoing_queue\gmtp_outgoing_queue.sh`
**Location:** Lines 26, 31
**Severity:** HIGH
**Category:** Hardcoded Credentials / Secrets in Version Control

**Description:**
The GMTP queue monitoring script contains hardcoded credentials for the GMTP management interface, committed in plaintext to the Git repository. The telnet username `gmtp` and password `gmtp!telnet` are embedded in the script body. Any person with read access to this repository (developers, CI/CD systems, audit tools, third-party integrators) now has credentials for the GMTP service management interface.

**Evidence:**
```bash
# Lines 26, 31 of gmtp_outgoing_queue.sh:
send "gmtp\r"
...
send "gmtp!telnet\r"
```
The script connects to `localhost:9494` using these credentials to execute a `status` command on the GMTP listener.

**Recommendation:**
1. Rotate the GMTP management interface password immediately on all environments.
2. Remove the hardcoded credentials from the script. Store them in an environment variable, a secrets manager (e.g., HashiCorp Vault), or a credentials file with appropriate filesystem permissions that is excluded from version control.
3. Purge the credentials from Git history using `git filter-repo` or BFG Repo Cleaner, or treat the current credential as permanently compromised.
4. Consider whether the GMTP management interface telnet endpoint requires password authentication at all if it only binds to localhost; if so, evaluate additional controls.

---

### A19-2 — Internal Staff Email Addresses in Version Control

**File:** `C:\Projects\cig-audit\repos\fleetfocus\executables\gmtp_outgoing_queue\gmtp_outgoing_queue.sh`
**Location:** Lines 9–11
**Severity:** LOW
**Category:** Information Disclosure / PII in Version Control

**Description:**
Three personal email addresses of Collective Intelligence staff are hardcoded in the monitoring script and committed to the repository: `hui@collectiveintelligence.com.au`, `roland@collectiveintelligence.com.au`, `dev@collectiveintelligence.com.au`. While these are work email addresses (not personal), their presence in version control unnecessarily exposes personnel information and makes updating the notification list require a code change and deployment.

**Evidence:**
```bash
ADMIN1="hui@collectiveintelligence.com.au"
ADMIN2="roland@collectiveintelligence.com.au"
ADMIN3="dev@collectiveintelligence.com.au"
```

**Recommendation:**
Move alert recipient configuration to an environment variable or external configuration file excluded from version control. This also allows changing on-call recipients without a code change.

---

### A19-3 — Production Database Schema Dump Committed to Version Control

**File:** `C:\Projects\cig-audit\repos\fleetfocus\sql\fleetfocus-schema-apr02-2025-dump.sql`
**File:** `C:\Projects\cig-audit\repos\fleetfocus\sql\fleetfocus-schema-apr02-2025-update.sql`
**Severity:** MEDIUM
**Category:** Sensitive Information / Schema Exposure in Version Control

**Description:**
Two files in `sql/` are full PostgreSQL database schema dumps generated by `pg_dump` from the production database (PostgreSQL 11.20, Ubuntu, dumped 2025-04-02). These files contain:
- All table definitions including column names and data types for the entire FleetFocus schema
- All stored function bodies
- All sequence definitions, constraints, and foreign keys
- All index definitions
- Confirmation that the database uses `plperl` and `plperlu` extensions (Perl-based procedural language)
- The database owner username (`gmtp`)

Committing a full schema dump provides attackers or unauthorized individuals with a complete blueprint of the production database, significantly aiding any SQL injection or privilege escalation attempts.

**Evidence:**
```sql
-- Dumped from database version 11.20 (Ubuntu 11.20-1.pgdg18.04+1)
-- Dumped by pg_dump version 13.4
-- Started on 2025-04-02 15:50:33
...
ALTER PROCEDURAL LANGUAGE plperlu OWNER TO gmtp;
```

**Recommendation:**
1. Remove the schema dump files from the repository and from git history.
2. If schema documentation is needed, maintain a sanitized DDL migration history (the incremental SQL scripts already present in `sql/` serve this purpose) rather than full dumps.
3. Evaluate whether `plperlu` (untrusted PL/Perl) is required. Untrusted Perl stored procedures can execute arbitrary OS commands as the PostgreSQL process owner — this is a significant privilege that should be audited separately.

---

### A19-4 — Ad-hoc Customer Data Deletion Script Names Real Customer in Comments

**File:** `C:\Projects\cig-audit\repos\fleetfocus\sql\adhoctask\April232024\UnwantedCustomerSitesDeletionWoolworths.sql`
**Severity:** LOW
**Category:** Information Disclosure / Customer Data Reference in Version Control

**Description:**
An ad-hoc task SQL script permanently committed to the repository explicitly identifies a real customer by name ("Woolworths"), their internal customer code (CUST_CD 233), and internal site identifiers (LOC_CD 1126, 1138, DEPT_CD 1437, 1465) and site names ("zz- inactiveLarapinta BRDC 1", "zz- inactiveLarapinta BRDC 2") in SQL comments. While the script itself performs a deletion of decommissioned data, its presence in perpetuity in version control constitutes an unnecessary retention of identifiable customer operational data that may conflict with data minimisation obligations under applicable privacy legislation (e.g., the Australian Privacy Act 1988).

**Evidence:**
```sql
-- '233' is Customer Woolworths
-- '1126' is Site zz- inactiveLarapinta BRDC 1
-- '1138' is Site zz- inactiveLarapinta BRDC 2
DELETE FROM "FMS_DEPT_MST" where "DEPT_CD" in ('1437', '1465');
```

**Recommendation:**
1. Review whether ad-hoc task scripts containing customer-identifiable information should be retained in version control, or should only exist in a separate, access-controlled internal operations repository.
2. Consider anonymising customer identifiers in comments (use "Customer A" or reference the ticket number) in future scripts.
3. Evaluate whether the `sql/adhoctask/` directory should remain in the main application repository or be moved to a separate operations runbook repository with stricter access controls.

---

### A19-5 — Compiled JSP Class Files Committed to Version Control

**Files:**
- `C:\Projects\cig-audit\repos\fleetfocus\work\org\apache\jsp\pages\admin\setting\driver_005flimiting_005fby_005ftruck_jsp.class`
- `C:\Projects\cig-audit\repos\fleetfocus\work\org\apache\jsp\pages\admin\setting\driver_005fsettings_005fto_005funit_jsp.class`
(and corresponding .java files)
**Severity:** LOW
**Category:** Binary Artifacts in Version Control

**Description:**
Two Tomcat/Jasper-compiled JSP class files and their generated Java source files are tracked by git in the `work/` directory. These are runtime artifacts generated by the Tomcat JSP compiler from `pages/admin/setting/driver_limiting_by_truck.jsp` and `pages/admin/setting/driver_settings_to_unit.jsp`. They were committed at initial project import ("First Import") and persist despite a `/work/` entry in `.gitignore` (added after the initial commit).

Although the content of these specific files does not appear to contain secrets, committing compiled class files to version control is problematic because: (a) the class file may differ from the current JSP source, introducing confusion about which version is deployed; (b) class files can be decompiled to recover implementation details; and (c) the presence of compiled artifacts indicates the developer's working Tomcat directory was inadvertently committed.

**Evidence:**
Git history: commit `a579fabf`, `3fadbf95`, `a337ab80` ("First Import") shows these files have been tracked since initial repository creation.
`.gitignore` line 2: `/work/` — this entry did not retroactively untrack already-committed files.

**Recommendation:**
1. Run `git rm --cached work/org/apache/jsp/pages/admin/setting/driver_005flimiting_005fby_005ftruck_jsp.class work/org/apache/jsp/pages/admin/setting/driver_005flimiting_005fby_005ftruck_jsp.java work/org/apache/jsp/pages/admin/setting/driver_005fsettings_005fto_005funit_jsp.class work/org/apache/jsp/pages/admin/setting/driver_005fsettings_005fto_005funit_jsp.java` to untrack these files.
2. Verify the entire `work/` directory is not tracked by running `git ls-files work/` and removing any remaining entries.

---

### A19-6 — Visual SourceSafe Metadata Files Present in Repository

**File:** `C:\Projects\cig-audit\repos\fleetfocus\WEB-INF\vssver2.scc` (and ~19 additional vssver2.scc files listed in .gitattributes across the repository)
**Severity:** INFO
**Category:** Legacy Version Control Metadata / Information Disclosure

**Description:**
Multiple `vssver2.scc` files from Microsoft Visual SourceSafe are present and committed in the repository. These are binary metadata files generated by the VSS version control client. Their presence indicates the codebase was originally managed in Visual SourceSafe and migrated to Git without fully cleaning up the legacy metadata. The file at `WEB-INF/vssver2.scc` reveals the VSS project path structure (`$/WEB-INF`) and file names tracked in the original VSS repository.

While these files do not contain authentication credentials for the VSS server in the readable portion examined, vssver2.scc files can contain binary-encoded server path information and in some versions historical revision metadata. Their presence unnecessarily documents legacy infrastructure details.

**Evidence:**
Binary content of `WEB-INF/vssver2.scc` includes plaintext fragment: `$/WEB-INF taglibs-mailer.tld taglibs-request.tld web.xml web.xml1 .cvsignore`
The `.gitattributes` file lists approximately 20 distinct `vssver2.scc` file paths across the repository tree.

**Recommendation:**
1. Remove all `vssver2.scc` files from the repository using `git rm` and commit the removal.
2. Add `vssver2.scc` to `.gitignore` to prevent future accidental commits.
3. Low priority for remediation given the VSS migration is historical, but should be included in the next repository cleanup cycle.

---

### A19-7 — .gitattributes File of Unusual Size Indicates Non-Standard Repository Hygiene

**File:** `C:\Projects\cig-audit\repos\fleetfocus\.gitattributes`
**Severity:** INFO
**Category:** Repository Hygiene / Configuration

**Description:**
The `.gitattributes` file is approximately 700+ lines and individually enumerates nearly every file in the repository with `-text` attribute. This structure is characteristic of repositories that were automatically migrated from VSS or SVN using a tool that generated a per-file attribute entry. The file also contains `svneol=unset#text/plain` entries on some Java source files, confirming an intermediate SVN stage in the migration history.

While the file does not contain secrets or introduce security vulnerabilities, its size and structure indicate the repository was never properly cleaned up after migration. The proliferation of explicit binary entries for common web assets (images, CSS, JS) is non-standard and complicates repository maintenance. No entries were found that suppress diffs or enable filter operations that could be used to hide committed secrets.

The file explicitly references `excelrpt/` Excel files and committed `.class` files, providing a historical record of artifacts that should not be in version control.

**Evidence:**
Line 1: `* text=auto !eol` (global default)
Lines 7–54: Explicit `-text` entries for `.class` files under `WEB-INF/classes/`
Lines 60–88: Explicit `-text` entries for `.jar` files under `WEB-INF/lib/`
Lines 208–210: `excelrpt/*.xlsx` and `excelrpt/*.png` entries
Line 92: `svneol=unset#text/plain` attribute on `DayhoursBean.java`

**Recommendation:**
1. Replace the per-file attribute entries with generic type-based rules (e.g., `*.class -text`, `*.jar -text`, `*.png -text`) and remove the large per-file enumeration.
2. Undertake a full repository audit to identify and remove all committed binary artifacts (compiled classes, Excel files, images that are not part of the application UI) using `git filter-repo`.
3. Low operational priority but should be addressed as part of a repository cleanup sprint.

---

## Summary

| Finding ID | Severity | Category | File |
|------------|----------|----------|------|
| A19-1 | HIGH | Hardcoded Credentials | executables/gmtp_outgoing_queue/gmtp_outgoing_queue.sh |
| A19-2 | LOW | PII in Version Control | executables/gmtp_outgoing_queue/gmtp_outgoing_queue.sh |
| A19-3 | MEDIUM | Schema Exposure | sql/fleetfocus-schema-apr02-2025-dump.sql, sql/fleetfocus-schema-apr02-2025-update.sql |
| A19-4 | LOW | Customer Data Reference | sql/adhoctask/April232024/UnwantedCustomerSitesDeletionWoolworths.sql |
| A19-5 | LOW | Binary Artifacts | work/org/apache/jsp/pages/admin/setting/*.class, *.java |
| A19-6 | INFO | Legacy VCS Metadata | WEB-INF/vssver2.scc (and ~19 others) |
| A19-7 | INFO | Repository Hygiene | .gitattributes |

**Total findings: 7**
(1 HIGH, 1 MEDIUM, 2 LOW, 2 INFO — with A19-2 counted separately from A19-1 as a distinct category)

**No findings:**
- No SQL injection vulnerabilities found in stored procedures (all use parameterized PL/pgSQL patterns).
- No hardcoded database credentials found in SQL files.
- No hardcoded SMTP credentials found in TLD files.
- The .gitattributes file does not suppress diffs or use filter attributes in ways that could hide committed secrets.
- The taglibs-request.tld and taglibs-mailer.tld files are standard library descriptors with no embedded sensitive configuration.
