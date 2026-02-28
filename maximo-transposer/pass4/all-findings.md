# Pass 4: Code Quality — Audit Agent A02
**File:** `index.js`
**Date:** 2026-02-27
**Run:** 2026-02-27-01
**Branch:** master (verified)

---

## READING EVIDENCE

### Module / Class Name
- No class. Single CommonJS module. Entrypoint is an AWS Lambda handler exported on `exports.handler`.

### Exported Symbols
| Symbol | Line |
|--------|------|
| `exports.handler` | 9 |

### Functions / Methods
| Name | Line | Notes |
|------|------|-------|
| `exports.handler` (async) | 9 | Outer Lambda handler; contains all logic inline |
| `dateFormatChange(date)` | 3146 | Inner function defined inside handler; converts AU date format dd/mm/yyyy hh:ii:ss → ISO |

### Major Constants / Data Structures
| Name | Line | Description |
|------|------|-------------|
| `aws` | 2 | aws-sdk module |
| `nodemailer` | 3 | nodemailer module |
| `simpleParser` | 4 | mailparser module |
| `XLSX` | 5 | xlsx module |
| `s3` | 6 | AWS S3 client instance |
| `ses` | 7 | AWS SES client instance (region: us-west-2) |
| `asset_map` | 31 | Large object (lines 31–3103): maps vehicle-name keys to asset sub-objects per meter type |
| `column_map` | 3107 | Maps meter-type keys (RUNHRS, GANTRYHRS, etc.) to spreadsheet column names |
| `sesNotification` | 3118 | SES event record extracted from Lambda event |
| `params` | 3121 | S3 getObject params |
| `data` | 3126 | S3 object response |
| `email` | 3128 | Raw email string from S3 body |
| `parsed_mail` | 3130 | Parsed email object |
| `from` | 3131 | Sender address string (UNUSED — see findings) |
| `attachments` | 3132 | Email attachments array |
| `workbook` | 3134 | XLSX workbook |
| `sheetname` | 3139 | First sheet name |
| `sheetJSON` | 3141 | Sheet data as JSON array |
| `result` | 3161 | Array for first CSV output |
| `worksheet` | 3210 | XLSX worksheet from result |
| `csv` | 3211 | CSV string from worksheet |
| `csv_cleaned` | 3217 | CSV with trailing-comma fix |
| `timestamp` | 3221 | Unix timestamp for first S3 filename |
| `filename` | 3222 | First S3 upload filename |
| `fileParams` | 3223 | First S3 upload params |
| `cranes_rtgs` | 3288 | Map of vehicle names that require ENGINHRS calculation (defined inside loop — see findings) |
| `result_2` | 3259 | Array for second CSV output (ENGINHRS calculation variant) |
| `worksheet_2` | 3417 | XLSX worksheet from result_2 |
| `csv_2` | 3418 | CSV string from worksheet_2 |
| `csv_cleaned_2` | 3424 | Second CSV with trailing-comma fix |
| `timestamp_2` | 3428 | Unix timestamp for second S3 filename |
| `filename_2` | 3429 | Second S3 upload filename |
| `fileParams_2` | 3430 | Second S3 upload params |
| `transporter_2` | 3440 | Nodemailer transport |
| `mail_result_2` | 3459 | Email send result (returned) |

---

## FINDINGS

### Build Warnings

**[A02-1]** *(INFO)*
**Description:** `node --check index.js` passes with no errors or warnings. The file is syntactically valid.
**Fix:** No action required.
**Location:** index.js (whole file)

---

### Commented-Out Code

**[A02-2]** *(MEDIUM)*
**Description:** A complete test-email block (`transporter_test`, `console.log`, `mail_result_test`) is commented out at the very top of the handler. The surrounding `console.log("Test email sent.")` at line 26 remains active and prints a misleading message even though no email is sent. This is dead scaffolding from development.
**Fix:** Delete lines 10–24 (the commented-out test-email block) and delete or correct line 26.
**Location:** index.js:10–26

**[A02-3]** *(MEDIUM)*
**Description:** A complete production-send block for the first CSV (transporter + sendMail call targeting `dpw.upload@bpdzenith.com`) is commented out at lines 3233–3249. The first CSV is still uploaded to S3 (line 3229) but never emailed. It is unclear whether the first CSV output is intentionally silent or whether the comment-out was temporary.
**Fix:** Determine whether the first CSV is intentionally not emailed. If it is not needed, remove the entire first CSV generation block (lines 3161–3229). If it is needed, reinstate the send or add a comment explaining the deliberate omission.
**Location:** index.js:3232–3249

**[A02-4]** *(LOW)*
**Description:** A second variant of `mail_result_2 = await transporter_2.sendMail(...)` targeting a test address (`graham.oconnell@trackingsolutions.com.au`) is commented out at lines 3446–3457 immediately above the live send. This is leftover test scaffolding sitting directly adjacent to production code, creating confusion about which call is authoritative.
**Fix:** Delete lines 3446–3457.
**Location:** index.js:3446–3457

**[A02-5]** *(LOW)*
**Description:** Banner comments `// TEST WITH PRNT HOURS COMING FROM NEW CALCULATION` (lines 3251–3257) and `// END OF THE TEST` (lines 3475–3481) remain in the file. These indicate the second CSV/ENGINHRS block was added as a temporary test that was never promoted to permanent status. The banners are misleading noise in production code.
**Fix:** Remove the banner comment blocks at lines 3251–3257 and 3475–3481. If the second output block is permanent, treat it as such and name it appropriately.
**Location:** index.js:3251–3257 and 3475–3481

---

### Dead Code

**[A02-6]** *(MEDIUM)*
**Description:** The variable `from` is declared and assigned at line 3131 (`const from = parsed_mail.from.text;`) but is never read anywhere in the handler. It exists solely as unused code.
**Fix:** Delete line 3131, or use `from` in log output / validation logic if the sender identity is relevant to processing.
**Location:** index.js:3131

**[A02-7]** *(MEDIUM)*
**Description:** `json-2-csv` (package.json line 9) and `aws-cli` (package.json line 8) are declared as dependencies but are never `require()`d in `index.js`. They appear to be vestigial dependencies from earlier development.
**Fix:** Remove `json-2-csv` and `aws-cli` from `package.json` `dependencies` and regenerate `package-lock.json`. This also reduces the Lambda deployment bundle size.
**Location:** index.js (no require call exists); package.json:8–9

**[A02-8]** *(LOW)*
**Description:** The `else` block at lines 3195–3199 and the structurally identical block at lines 3402–3406 contain only a comment stating the problem but take no action. These are empty error-handling branches. Similarly, the `else` blocks at lines 3201–3206 and 3408–3413 are empty. None of these produce any log output, metric, or error throw; unmatched vehicles and unmatched meters silently disappear from the output.
**Fix:** Add at minimum a `console.warn` or `console.error` call in each empty else block so that missing vehicle/meter mappings surface in CloudWatch logs. Ideally, accumulate them and include in the outbound email or a dead-letter queue.
**Location:** index.js:3195–3199, 3201–3206, 3402–3406, 3408–3413

---

### Style Consistency

**[A02-9]** *(LOW)*
**Description:** Variable declaration keywords are mixed throughout the handler. The outer handler scope and first CSV block use `var` for `result`, `worksheet`, `csv`, `csv_cleaned`, and loop variables (`i`, `vehicle_name`, `asset_name`, `original_column_name`, `vehicle_split`). The second CSV block then switches to `var` for `result_2`, `worksheet_2`, etc., but uses `let` for `cranes_rtgs`, `parent_hours`, `transporter_2`, and `mail_result_2`. Meanwhile the S3/mail section of the first block uses `const` for `timestamp`, `filename`, `fileParams`. There is no consistent policy. In the same outer handler scope, `var`, `let`, and `const` all appear for similar declarations.
**Fix:** Adopt a consistent policy: use `const` for values that are never reassigned, `let` for variables that are reassigned, and eliminate `var` entirely. Apply uniformly across both CSV blocks.
**Location:** index.js:3161–3484 (throughout handler logic)

**[A02-10]** *(LOW)*
**Description:** The `SPREADERHRS` property inside every `ASC` asset sub-object is missing a trailing comma after `assetnum`, while every other property in every other asset sub-object in the file has one. This is a consistent formatting inconsistency across all 16 ASC entries (lines 2515, 2544, 2573, 2602, 2631, 2660, 2689, 2718, 2747, 2776, 2805, 2834, 2863, 2892, 2921, 2950).
**Fix:** Add trailing commas after `assetnum: "ASCxxx"` on each of the affected lines to make the style consistent with the rest of the file.
**Location:** index.js:2515, 2544, 2573, 2602, 2631, 2660, 2689, 2718, 2747, 2776, 2805, 2834, 2863, 2892, 2921, 2950

**[A02-11]** *(LOW)*
**Description:** In `ASC205 - AUFIS-C1`, the `OVLPHRS` sub-object has its properties in reversed order (`assetnum` before `assettag`) at lines 2634–2635, while every other asset sub-object in the entire file uses `assettag` first, then `assetnum`. This is a one-off inconsistency.
**Fix:** Swap the property order in the `OVLPHRS` block of `ASC205` to `assettag` first, then `assetnum`, to match the convention used everywhere else.
**Location:** index.js:2633–2636

**[A02-12]** *(LOW)*
**Description:** An extra blank line appears between `"QC003 - AUFRE-C1"` and `"QC004 - AUFRE-C1"` (line 1822) and between `"QC004 - AUFRE-C1"` and `"QC001 - AUMEL-C1"` (line 1852). No other entry-to-entry transition in the 3,000-line `asset_map` uses a blank separator line. These are minor whitespace inconsistencies.
**Fix:** Remove the extraneous blank lines at 1822 and 1852.
**Location:** index.js:1822, 1852

---

### Leaky Abstractions / Structure

**[A02-13]** *(HIGH)*
**Description:** The entire application — S3 fetch, email parse, XLSX parse, two complete CSV transform passes, two S3 uploads, and one email send — is implemented as a single monolithic async function (`exports.handler`, lines 9–3484). The function body is approximately 3,475 lines. There are no helper functions other than `dateFormatChange`. The two CSV generation loops (lines 3176–3207 and 3274–3414) are structural duplicates of each other; the second differs only in that it also handles an ENGINHRS calculation for a subset of assets.
**Fix:** Extract discrete responsibilities into named functions: (1) `fetchEmail(messageId)` for S3 retrieval and parsing, (2) `buildMeterDataRows(sheetJSON, assetMap, columnMap)` for the base CSV transform, (3) `buildEnginHrsRows(sheetJSON, assetMap, columnMap, cranesRtgs)` for the ENGINHRS variant, (4) `uploadToBucket(content, filename)` for S3 uploads, (5) `sendReport(csvContent)` for email dispatch. This also eliminates the code duplication between the two loops.
**Location:** index.js:9–3484

**[A02-14]** *(HIGH)*
**Description:** The `cranes_rtgs` object (lines 3288–3358) is declared and fully initialised inside the innermost `for...in` loop body (the loop over `asset_map[vehicle_name].assets`). This means the same large literal object is reconstructed on every iteration of the inner loop, which can be hundreds or thousands of times per invocation. The object is never modified; it is only checked with `in`.
**Fix:** Move `cranes_rtgs` out of the loops. It should be defined once at the same level as `asset_map` (or at the top of the handler), since its keys are a static subset of `asset_map` keys.
**Location:** index.js:3288–3358

**[A02-15]** *(MEDIUM)*
**Description:** The first CSV generation block (lines 3161–3229) produces a complete `result` array, converts it to CSV, cleans it, and uploads it to S3, but the result is never emailed and its upload is noted with the comment "Do we actually need a copy of the formatted file stored in S3?" (line 3219). The second block (lines 3259–3437) performs an almost identical operation plus the ENGINHRS logic. The existence of the first block, which costs a full S3 upload on every invocation, appears to be vestigial test output from when the ENGINHRS logic was being developed. The tight coupling between the two passes — sharing `sheetJSON`, `asset_map`, `column_map`, and `dateFormatChange` via closure without any explicit interface — makes it difficult to determine the intended relationship between them.
**Fix:** Confirm whether the first CSV output (uploaded as `*-formatted.csv`) still serves any purpose. If not, remove the entire first-pass block (lines 3161–3229). If it does serve a purpose, document it with a comment and add the email send.
**Location:** index.js:3161–3229

**[A02-16]** *(MEDIUM)*
**Description:** `dateFormatChange` (lines 3146–3159) is defined inside `exports.handler`, which means a new function object is allocated on every Lambda invocation. The function has no dependency on handler-scoped state and is pure. Defining it inside the handler also means it is defined after `asset_map` and `column_map` are constructed but before they are used, which is unconventional and creates a visual interrupt in the data → logic flow.
**Fix:** Move `dateFormatChange` to module scope (outside `exports.handler`), between the module-level requires and the handler export.
**Location:** index.js:3146–3159

---

### Data Integrity Issues (flagged as code quality concerns)

**[A02-17]** *(HIGH)*
**Description:** The `asset_map` key for the Brisbane RTG914 asset is `"RTG14 - AUFRE-C1"` (line 2081), but the internal `assettag` and `assetnum` values are both `"RTG914"`. This is a key-name typo: the leading `9` is missing from the map key. Consequently, if incoming spreadsheet data contains `Vehicle Name = "RTG914 - AUFRE-C1"`, it will not match any key in `asset_map` and will be silently dropped. The `cranes_rtgs` map (line 3332) correctly uses `"RTG914 - AUFRE-C1"`, so even if the ENGINHRS path were reached, the key mismatch in `asset_map` would prevent it from doing so.
**Fix:** Rename the `asset_map` key on line 2081 from `"RTG14 - AUFRE-C1"` to `"RTG914 - AUFRE-C1"` to match the asset tag values and the `cranes_rtgs` entry.
**Location:** index.js:2081

**[A02-18]** *(MEDIUM)*
**Description:** Six AUFRE-C1 entries with RTG-prefix keys (`RTG913`, `RTG914` via the typo key, `RTG915`, `RTG916`, `RTG917`, `RTG918`) are assigned `assettype: "QC"` (lines 2079, 2104, 2129, 2154, 2179, 2204). All other RTG assets in the file use `assettype: "RTG"`. The `assettype` field does not appear to be used in the CSV output logic, but the inconsistency suggests copy-paste from the QC block above without correction, and could break any future logic that branches on `assettype`.
**Fix:** Change `assettype` from `"QC"` to `"RTG"` for entries `RTG913` through `RTG918` under `AUFRE-C1`, if these are indeed RTG crane assets.
**Location:** index.js:2079, 2104, 2129, 2154, 2179, 2204

**[A02-19]** *(MEDIUM)*
**Description:** `TVE603 - AUFRE-C1` has `assetnum: "9054"` (line 2345) while `assettag: "TVE603"`. This is the only entry in the entire file where `assetnum` differs from `assettag` and also differs from the map key, and the value `"9054"` does not follow any recognisable naming convention used elsewhere. It may be a legacy Maximo numeric ID left after an asset-renumbering event, or it may be an error.
**Fix:** Verify with the client whether `assetnum: "9054"` is the intended Maximo asset number for TVE603 or whether it should be `"TVE603"`. Document the reason in an inline comment if the divergence is intentional.
**Location:** index.js:2341–2348

**[A02-20]** *(MEDIUM)*
**Description:** `TVE599 - AUFRE-C1` has `assettype: "TV"` (line 2312) while every other TVE asset uses `assettype: "TVE"`. This appears to be a truncation error.
**Fix:** Change `assettype: "TV"` to `assettype: "TVE"` for the `TVE599 - AUFRE-C1` entry, or confirm with the client whether `TV` is the correct type.
**Location:** index.js:2312

**[A02-21]** *(MEDIUM)*
**Description:** `TT36 - AUPBT-C1` (line 925) has `assettag: "TT136"` and `assetnum: "TT136"`, meaning the asset map key is missing the leading `1` compared to the internal asset values. If incoming data contains `Vehicle Name = "TT136 - AUPBT-C1"`, it will not match and will be silently dropped. If incoming data contains `"TT36 - AUPBT-C1"`, it will match but the output assetnum/assettag will be `TT136`, which may or may not be correct.
**Fix:** Verify whether the correct vehicle name in incoming data is `TT36` or `TT136`, and correct either the map key or the internal values accordingly.
**Location:** index.js:925–932

---

### Dependency Version Conflicts

**[A02-22]** *(INFO)*
**Description:** All six packages declared in `package.json` resolve to exactly the versions pinned (`aws-sdk@2.901.0`, `nodemailer@6.6.0`, `mailparser@3.2.0`, `xlsx@0.16.9`, `json-2-csv@3.11.0`, `aws-cli@0.0.2`). No version conflicts exist between `package.json` and `package-lock.json`.
**Fix:** No action required for version conflicts. Note however that `json-2-csv` and `aws-cli` are unused (see A02-7) and should be removed.
**Location:** package.json, package-lock.json

---

## SUMMARY TABLE

| ID | Severity | Category | Short Description |
|----|----------|----------|-------------------|
| A02-1 | INFO | Build warnings | Syntax check passes cleanly |
| A02-2 | MEDIUM | Commented-out code | Test email block (lines 10–24) + misleading console.log at line 26 |
| A02-3 | MEDIUM | Commented-out code | First CSV email send commented out (lines 3233–3249) |
| A02-4 | LOW | Commented-out code | Test sendMail block adjacent to live send (lines 3446–3457) |
| A02-5 | LOW | Commented-out code | TEST/END OF THE TEST banner comments (lines 3251–3257, 3475–3481) |
| A02-6 | MEDIUM | Dead code | `from` variable assigned but never read (line 3131) |
| A02-7 | MEDIUM | Dead code | `json-2-csv` and `aws-cli` declared but never required |
| A02-8 | LOW | Dead code | Empty else branches swallow mapping errors silently |
| A02-9 | LOW | Style consistency | Mixed var/let/const throughout handler |
| A02-10 | LOW | Style consistency | Missing trailing commas after `assetnum` in all SPREADERHRS blocks |
| A02-11 | LOW | Style consistency | Reversed property order (assetnum before assettag) in ASC205 OVLPHRS |
| A02-12 | LOW | Style consistency | Spurious blank lines between asset_map entries at lines 1822, 1852 |
| A02-13 | HIGH | Leaky abstractions | Monolithic 3,475-line handler with no sub-functions and duplicated loops |
| A02-14 | HIGH | Leaky abstractions | `cranes_rtgs` literal reconstructed on every inner-loop iteration |
| A02-15 | MEDIUM | Leaky abstractions | First CSV pass appears vestigial; unclear relationship to second pass |
| A02-16 | MEDIUM | Leaky abstractions | `dateFormatChange` defined inside handler; should be module-level |
| A02-17 | HIGH | Data integrity | asset_map key `"RTG14 - AUFRE-C1"` is a typo for `"RTG914 - AUFRE-C1"` |
| A02-18 | MEDIUM | Data integrity | RTG913–RTG918 under AUFRE-C1 have `assettype: "QC"` instead of `"RTG"` |
| A02-19 | MEDIUM | Data integrity | TVE603 has `assetnum: "9054"` — anomalous numeric ID |
| A02-20 | MEDIUM | Data integrity | TVE599 has `assettype: "TV"` instead of `"TVE"` |
| A02-21 | MEDIUM | Data integrity | `TT36 - AUPBT-C1` key likely typo for `TT136 - AUPBT-C1` |
| A02-22 | INFO | Dependency versions | No version conflicts in package-lock.json |
# Pass 4: Code Quality — Agent A04
**Audit date:** 2026-02-27
**Branch:** master (confirmed)
**Run directory:** audit/2026-02-27-01/

---

## Pre-flight
Branch confirmed: `master`

---

## Reading Evidence

### A01 — `.gitignore`
**File path:** `C:/Projects/cig-audit/repos/maximo-transposer/.gitignore`
**Patterns (all 2 lines):**
- Line 1: `node_modules`
- Line 2: `__MACOSX/`

---

### A03 — `package-lock.json`
**File path:** `C:/Projects/cig-audit/repos/maximo-transposer/package-lock.json`
**lockfileVersion:** 2
**Top-level name:** `maximo-transposer`
**Top-level version:** `1.0.0`
**Package count (node_modules entries):** 43 top-level packages in the `packages` section (counting unique `node_modules/` keys). The `dependencies` section (legacy v1 format also embedded) contains 37 entries.

**Packages with multiple resolved versions (nested vs top-level):**
1. `aws-sdk` — top-level: `2.901.0`; nested under `node_modules/aws-cli/node_modules/aws-sdk`: `2.0.31`
2. `xml2js` — top-level: `0.4.19`; nested under `node_modules/aws-cli/node_modules/xml2js`: `0.2.6`
3. `xmlbuilder` — top-level: `9.0.7`; nested under `node_modules/aws-cli/node_modules/xmlbuilder`: `0.4.2`
4. `sax` — top-level: `1.2.1`; nested under `node_modules/aws-cli/node_modules/sax`: `0.4.2`
5. `nodemailer` — top-level: `6.6.0`; nested under `node_modules/mailparser/node_modules/nodemailer`: `6.5.0`
6. `commander` — top-level: `2.17.1`; nested under `node_modules/codepage/node_modules/commander`: `2.14.1`

**Deprecated packages noted in lock:**
- `aws-cli@0.0.2`: "Recommend using the official aws cli tools for python"
- `querystring@0.2.0`: "The querystring API is considered Legacy. new code should use the URLSearchParams API instead."
- `uuid@3.3.2`: "Please upgrade to version 7 or higher. Older versions may use Math.random() in certain circumstances..."

---

### A04 — `package.json`
**File path:** `C:/Projects/cig-audit/repos/maximo-transposer/package.json`
**Fields:**
- `name`: "maximo-transposer"
- `version`: "1.0.0"
- `description`: "DPWorld Maximo export"
- `main`: "index.js"
- `scripts.test`: `echo "Error: no test specified" && exit 1`
- `repository.type`: "git"
- `repository.url`: "git+https://sidneyaulakh@bitbucket.org/cig-code/maximo-transposer.git"
- `author`: "Sidney Aulakh"
- `license`: "ISC"
- `bugs.url`: "https://bitbucket.org/cig-code/maximo-transposer/issues"
- `homepage`: "https://bitbucket.org/cig-code/maximo-transposer#readme"

**Dependencies (all with version specifiers):**
- `aws-sdk`: `^2.901.0`
- `aws-cli`: `^0.0.2`
- `json-2-csv`: `^3.11.0`
- `nodemailer`: `^6.6.0`
- `mailparser`: `^3.2.0`
- `xlsx`: `^0.16.9`

**devDependencies:** `{}` (empty)

---

### A05 — `sample.json`
**File path:** `C:/Projects/cig-audit/repos/maximo-transposer/sample.json`
**Top-level structure:** Single key `thing` (object), containing:
- `vehicle` (object): serialno, product_type, product_code, product_class, name, model, make, hour_meter_offset, hardwareid, hardware_type, entered_fleet, description, dealer_id, date_into_service
- `usage` (object): this_week, this_month, average_weekly_usage_input_one, average_weekly_usage, average_daily_usage_input_one, average_daily_usage
- `rentals` (array, empty)
- `organisation` (object): service_location, management_region, management_location
- `maintenance` (object): services (array, empty), service_type, service_offset, service_interval, service_calculation_input, next_service_type, impacts
- `fleets` (array of objects with type, name, id)
- `customer` (string, empty)
- `contract` (object): contract_type, contract_postcode, contract_name, contract_geofence

---

### A06 — `serverless.yml`
**File path:** `C:/Projects/cig-audit/repos/maximo-transposer/serverless.yml`
**service:** `maximo-transposer`
**Provider settings:**
- `name`: aws
- `runtime`: nodejs14.x
- `region`: us-east-1
- `iamRoleStatements`: Allow s3:GetObject on `arn:aws:s3:::${self:custom.bucket}/*`

**Plugins:**
- `serverless-plugin-include-dependencies`

**Custom variables:**
- `bucket`: `maximo-transposer-bucket`

**Functions:**
- `email_handler`: handler = `index.handler`, environment: `BUCKET: ${self:custom.bucket}`

---

## Findings

### Style Consistency

**[A04-1]** *(LOW)*
**Description:** All six `dependencies` entries in `package.json` use the `^` (caret) semver specifier, which is consistent within itself. However, the `devDependencies` block is present but empty. The `serverless-plugin-include-dependencies` plugin declared in `serverless.yml` is a deploy-time plugin that belongs in `devDependencies` in `package.json`, yet it appears nowhere in `package.json` at all (see A06-1). The version specifier style is uniform across all declared dependencies — no mixed `~`/`^` issue.
**Fix:** No specifier inconsistency to fix. See A06-1 for the missing devDependency.
**Location:** `package.json:6-13`

**[A06-1]** *(MEDIUM)*
**Description:** `serverless.yml` declares `serverless-plugin-include-dependencies` as a plugin, but this plugin is not present in `package.json` (neither in `dependencies` nor `devDependencies`), and is absent from `package-lock.json`. This means the plugin is either globally installed on the developer's machine or will cause a deploy failure on any clean environment. This is a broken dependency declaration and a leaky abstraction — deploy infrastructure relies on an implicit global tool state.
**Fix:** Add `serverless-plugin-include-dependencies` to `devDependencies` in `package.json` and run `npm install` to lock it.
**Location:** `serverless.yml:4` / `package.json` (missing)

**[A06-2]** *(LOW)*
**Description:** The YAML indentation and quoting in `serverless.yml` is consistent (2-space indentation throughout). The inline comment on line 1 (`# NOTE: update this with your service name`) is a stale boilerplate comment — the service name has been set to `maximo-transposer` and the note is no longer actionable.
**Fix:** Remove the boilerplate comment on line 1.
**Location:** `serverless.yml:1`

---

### Commented-Out Code

**[A06-3]** *(MEDIUM)*
**Description:** `index.js` (the handler referenced from `serverless.yml`) contains a large block of commented-out code at lines 11–24 that represents a "send test email" flow complete with transporter creation, sendMail call, addresses, subject, html body, and attachments. While index.js is not a directly assigned file, it is the sole handler wired to the function in `serverless.yml`, so this finding is attributed to the serverless.yml deployment unit. Commented-out code of this scope is dead weight that obscures intent, increases cognitive load, and risks being mistaken for active logic.
**Fix:** Remove lines 11–24 of `index.js` (the commented-out test email block). Use version control history to recover this code if needed.
**Location:** `index.js:11-24` (referenced from `serverless.yml:21`)

---

### Dead / Unused Configuration

**[A04-2]** *(HIGH)*
**Description:** `json-2-csv` is declared as a production dependency in `package.json` (`^3.11.0`) and is resolved in `package-lock.json`, but the package is never `require()`d anywhere in `index.js`. Searching `index.js` for `json-2-csv`, `json2csv`, or any related import returns zero matches. This is dead dependency — it adds installation weight and surface area with no functional benefit.
**Fix:** Remove `json-2-csv` from `dependencies` in `package.json`, then run `npm install` to update `package-lock.json`.
**Location:** `package.json:9`

**[A04-3]** *(HIGH)*
**Description:** `aws-cli` (`^0.0.2`) is declared as a production dependency in `package.json`. It is never `require()`d in `index.js`. This package is an unofficial, deprecated npm wrapper around the AWS CLI for Python (the package itself carries a deprecation notice: "Recommend using the official aws cli tools for python"). It is not used in the codebase in any way — not imported, not called as a subprocess, not referenced. Its presence introduces a severely outdated nested `aws-sdk@2.0.31` (see A03-2), multiplied package versions, and deprecated transitive dependencies.
**Fix:** Remove `aws-cli` from `dependencies` in `package.json`, then run `npm install` to update `package-lock.json`.
**Location:** `package.json:8`

**[A06-4]** *(HIGH)*
**Description:** `serverless.yml` declares the environment variable `BUCKET: ${self:custom.bucket}` for the `email_handler` function. However, `index.js` never references `process.env.BUCKET`. The S3 bucket name is hardcoded at three locations in `index.js` as the string literal `"maximo-transposer-bucket"` (lines 3122, 3224, 3431). The environment variable injection is entirely dead — it never reaches the application logic. This creates a false sense of configurability and means a change to `custom.bucket` in `serverless.yml` would have no effect on the actual S3 calls.
**Fix:** Replace the three hardcoded `"maximo-transposer-bucket"` string literals in `index.js` with `process.env.BUCKET`. This will make the environment variable injection actually effective.
**Location:** `serverless.yml:23` / `index.js:3122`, `index.js:3224`, `index.js:3431`

---

### Dependency Version Conflicts

**[A03-1]** *(MEDIUM)*
**Description:** `package-lock.json` (lockfileVersion 2) contains six packages that appear at multiple resolved versions due to nested resolution caused by `aws-cli`'s own dependency tree:
1. `aws-sdk` — `2.901.0` (top-level) vs `2.0.31` (nested under `node_modules/aws-cli`)
2. `xml2js` — `0.4.19` (top-level) vs `0.2.6` (nested under `node_modules/aws-cli`)
3. `xmlbuilder` — `9.0.7` (top-level) vs `0.4.2` (nested under `node_modules/aws-cli`)
4. `sax` — `1.2.1` (top-level) vs `0.4.2` (nested under `node_modules/aws-cli`)
5. `nodemailer` — `6.6.0` (top-level) vs `6.5.0` (nested under `node_modules/mailparser`)
6. `commander` — `2.17.1` (top-level) vs `2.14.1` (nested under `node_modules/codepage`)

The root cause for most conflicts (aws-sdk, xml2js, xmlbuilder, sax) is the dead `aws-cli` dependency identified in A04-3. Removing it would eliminate four of the six conflicts. The `nodemailer` conflict is inherent to `mailparser@3.2.0`'s pinned sub-dependency. The `commander` conflict is inherent to `xlsx`'s codepage sub-dependency.
**Fix:** Remove `aws-cli` from `package.json` (see A04-3). The nodemailer and commander version splits are unavoidable without upgrading the parent packages.
**Location:** `package-lock.json:49-81` (aws-cli nested modules), `package-lock.json:430-437` (mailparser nested nodemailer)

**[A03-2]** *(HIGH)*
**Description:** `aws-cli` pulls in `aws-sdk@2.0.31` (from 2015) as a nested dependency, while the project also uses `aws-sdk@2.901.0` at the top level. The extremely old `aws-sdk@2.0.31` carries known prototype-pollution vulnerabilities (CVSS 7.3, `GHSA-rrc9-gqf8-8rwg`) and is pulled into the install purely because of the dead `aws-cli` dependency. This adds vulnerable code to the deployed Lambda package.
**Fix:** Remove `aws-cli` from `package.json`. This eliminates the vulnerable `aws-sdk@2.0.31` from the tree entirely.
**Location:** `package-lock.json:49-81`

**[A03-3]** *(INFO)*
**Description:** Cross-checking `package.json` declared ranges against `package-lock.json` resolved versions — all six direct dependencies resolve within their declared ranges:
- `aws-sdk ^2.901.0` → resolved `2.901.0` (exact lower bound, acceptable)
- `aws-cli ^0.0.2` → resolved `0.0.2` (exact lower bound, acceptable)
- `json-2-csv ^3.11.0` → resolved `3.11.0` (exact lower bound, acceptable)
- `nodemailer ^6.6.0` → resolved `6.6.0` (exact lower bound, acceptable)
- `mailparser ^3.2.0` → resolved `3.2.0` (exact lower bound, acceptable)
- `xlsx ^0.16.9` → resolved `0.16.9` (exact lower bound, acceptable)

No range/resolution mismatches found. All resolved versions are at exactly the lower bound of their declared ranges, suggesting no `npm update` has been run since initial install.
**Fix:** No action required for version range compliance. Consider running `npm update` periodically to pick up patch/minor fixes within declared ranges.
**Location:** `package.json:6-13` / `package-lock.json:11-19`

---

### Build / Deploy Warnings

**[A03-4]** *(MEDIUM)*
**Description:** npm version on the audit machine is `10.9.2`. `package-lock.json` uses `lockfileVersion: 2`, which is compatible with npm 7 and above. No lockfileVersion compatibility issue exists. However, `npm install --dry-run` produces no explicit warnings, but `npm audit` reveals three vulnerability categories against the installed tree:
1. `minimist@1.2.5` — **CRITICAL** Prototype Pollution (GHSA-xvch-5gv4-984h, CVSS 9.8) — pulled in transitively by `html-to-text` via `mailparser`
2. `aws-sdk` (both versions) — **HIGH** Prototype Pollution (GHSA-rrc9-gqf8-8rwg, CVSS 7.3) and SDK v2 region validation (GHSA-j965-2qgj-vjmq, CVSS 3.7)
3. `mailparser@3.2.0` — **MODERATE** — via its pinned `nodemailer@6.5.0`

The `minimist` issue is fixed by upgrading to `>=1.2.6`; the `mailparser` fix is available via package update. The `aws-sdk` v2 vulnerability has no fix available at v2.
**Fix:** (1) Upgrade `mailparser` to `>=3.6.7` to pull in a `minimist` version `>=1.2.6`. (2) Evaluate migrating from `aws-sdk` v2 to `@aws-sdk/client-s3` and `@aws-sdk/client-ses` (v3). (3) Remove `aws-cli` to eliminate the vulnerable `aws-sdk@2.0.31`.
**Location:** `package-lock.json:448-452` (minimist), `package-lock.json:82-101` (aws-sdk)

---

### Leaky Abstractions

**[A06-5]** *(MEDIUM)*
**Description:** `serverless.yml` defines `custom.bucket: maximo-transposer-bucket` and correctly references it via `${self:custom.bucket}` in both the IAM role statement and the function environment. The variable reference style is consistent (all `${self:custom.*}` pattern). However, as noted in A06-4, the actual application code (index.js) does not consume the injected `BUCKET` environment variable — it uses the literal string instead. This creates a leaky abstraction: the infrastructure file implies the bucket name is a managed configuration parameter, but the application bypasses that contract entirely.
**Fix:** Fix the application side (see A06-4) so the abstraction is honoured.
**Location:** `serverless.yml:7`, `serverless.yml:17`, `serverless.yml:23`

**[A05-1]** *(INFO)*
**Description:** `sample.json` represents a single asset record (`thing`) from what appears to be a fleet telematics API response. The file is at an appropriate abstraction level for its apparent purpose as a test fixture or documentation sample of the upstream data shape. Many fields are `null` (product_type, product_code, product_class, model, make, entered_fleet, description, date_into_service, organisation fields, maintenance service_type/offset, contract fields) and the `services` and `rentals` arrays are empty. This means the sample does not exercise the full code path — null-handling and array-iteration branches are untested by this fixture.
**Fix:** Supplement `sample.json` with a more complete fixture that includes populated values for all nullable fields and at least one entry in `services`, `rentals`, and `fleets`.
**Location:** `sample.json:1-51`

---

### Checks with No Issues

- **A01 (.gitignore) style:** The two-pattern `.gitignore` is minimal but correct. `node_modules` is excluded (no trailing slash, which is valid — git treats it as a directory pattern). `__MACOSX/` (with trailing slash) correctly excludes macOS archive artefacts. No issues.
- **A06 YAML style:** Indentation is consistently 2 spaces throughout `serverless.yml`. No tab/space mixing. Quoting is applied only where necessary (the ARN string on line 17 is correctly double-quoted due to the `${}` interpolation). No issues.
- **A06 variable reference consistency:** All Serverless Framework variable references use the canonical `${self:custom.*}` form. No mixing with `${env:}`, `${ssm:}`, or other reference styles. No issues.
- **Commented-out code in config files:** No commented-out code found in `package.json`, `package-lock.json`, `.gitignore`, or `sample.json`. The single comment in `serverless.yml` (line 1) is a stale boilerplate note, not commented-out code — covered under A06-2.

---

## Summary Table

| ID      | Severity | File             | Issue                                                        |
|---------|----------|------------------|--------------------------------------------------------------|
| A04-1   | LOW      | package.json     | Version specifier style consistent; note missing devDep (see A06-1) |
| A06-1   | MEDIUM   | serverless.yml   | Plugin `serverless-plugin-include-dependencies` not in package.json |
| A06-2   | LOW      | serverless.yml   | Stale boilerplate comment on line 1                          |
| A06-3   | MEDIUM   | index.js (via serverless.yml) | Large commented-out test email block (lines 11–24)  |
| A04-2   | HIGH     | package.json     | `json-2-csv` declared but never imported in index.js         |
| A04-3   | HIGH     | package.json     | `aws-cli` declared but never used; deprecated package        |
| A06-4   | HIGH     | serverless.yml   | `BUCKET` env var declared but never consumed; bucket hardcoded |
| A03-1   | MEDIUM   | package-lock.json | 6 packages appear at multiple resolved versions              |
| A03-2   | HIGH     | package-lock.json | `aws-sdk@2.0.31` (vulnerable) pulled in by dead `aws-cli` dep |
| A03-3   | INFO     | package-lock.json | All resolved versions within declared ranges — no mismatches |
| A03-4   | MEDIUM   | package-lock.json | npm audit shows CRITICAL (minimist), HIGH (aws-sdk) vulns     |
| A06-5   | MEDIUM   | serverless.yml   | Bucket abstraction bypassed by hardcoded literal in app code |
| A05-1   | INFO     | sample.json      | Sample fixture incomplete — mostly null values, empty arrays  |
