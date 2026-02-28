# A02 Documentation Audit — index.js
**Audit run:** 2026-02-27-01
**Pass:** 3 (Documentation)
**Auditor:** A02
**File:** `C:/Projects/cig-audit/repos/maximo-transposer/index.js`
**Branch verified:** master
**Standard applied:** JSDoc (`/** ... */`)

---

## Reading Evidence

### Module/Class Name
- No named module or class. The file is an AWS Lambda handler module exporting a single `handler` function via `exports.handler`.

### Functions/Methods and Line Numbers

| Name | Type | Line |
|------|------|------|
| `exports.handler` | Exported async function (Lambda entry point) | 9 |
| `dateFormatChange` | Inner function (defined inside `handler`) | 3146 |

No other named functions, methods, or classes are present in the file.

### Exported Symbols and Line Numbers

| Symbol | Line |
|--------|------|
| `exports.handler` | 9 |

### Constants and Notable Variables (module-level or handler-level)

| Name | Line | Notes |
|------|------|-------|
| `aws` | 2 | `require("aws-sdk")` |
| `nodemailer` | 3 | `require("nodemailer")` |
| `simpleParser` | 4 | `require("mailparser").simpleParser` |
| `XLSX` | 5 | `require("xlsx")` |
| `s3` | 6 | `new aws.S3()` |
| `ses` | 7 | `new aws.SES({ region: "us-west-2" })` |
| `asset_map` | 31 | Large lookup object mapping vehicle-name keys (e.g. `"QC001 - AUPBT-C1"`) to asset metadata |
| `column_map` | 3107 | Maps internal meter key names (e.g. `RUNHRS`) to report column header strings (e.g. `"Crane on Hour Meter"`) |
| `sesNotification` | 3118 | SES event notification record |
| `params` | 3121 | S3 `getObject` parameters |
| `data` | 3126 | Raw S3 object result |
| `email` | 3128 | Email body as string |
| `parsed_mail` | 3130 | Parsed email from `simpleParser` |
| `from` | 3131 | Sender address (assigned but never used) |
| `attachments` | 3132 | Email attachments array |
| `workbook` | 3134 | XLSX workbook parsed from first attachment |
| `sheetname` | 3139 | Name of first worksheet |
| `sheetJSON` | 3141 | JSON rows from first worksheet |
| `result` | 3161 | Array-of-arrays for first CSV output (raw meter readings) |
| `worksheet` | 3210 | XLSX worksheet for first CSV |
| `csv` | 3211 | First CSV string |
| `csv_cleaned` | 3217 | First CSV with trailing comma fix applied |
| `timestamp` | 3221 | Unix timestamp string for first S3 filename |
| `filename` | 3222 | S3 key for first CSV upload (`*-formatted.csv`) |
| `fileParams` | 3223 | S3 upload parameters for first file |
| `result_2` | 3259 | Array-of-arrays for second CSV output (ENGINHRS-calculated readings) |
| `cranes_rtgs` | 3288 | Inline object listing all vehicle names that require the ENGINHRS calculation |
| `worksheet_2` | 3417 | XLSX worksheet for second CSV |
| `csv_2` | 3418 | Second CSV string |
| `csv_cleaned_2` | 3424 | Second CSV with trailing comma fix applied |
| `timestamp_2` | 3428 | Unix timestamp string for second S3 filename |
| `filename_2` | 3429 | S3 key for second CSV upload (`*-cleaned.csv`) |
| `fileParams_2` | 3430 | S3 upload parameters for second file |
| `transporter_2` | 3440 | nodemailer SES transporter |
| `mail_result_2` | 3459 | Result from `transporter_2.sendMail(...)` |

---

## Findings

---

**[A02-1]** *(CRITICAL)*
**Description:** The module has no top-level JSDoc comment. There is no description of what this Lambda function does, what triggers it, what it consumes, or what it produces. A reader must reverse-engineer the entire file to understand its purpose. The module processes DP World equipment-hour telemetry emails from Rayven via SES, transforms the data into Maximo-compatible CSV format, and distributes the result by email — none of which is stated anywhere in a comment.
**Fix:** Add a file-level JSDoc block at line 1, before `"use strict"`, for example:
```js
/**
 * @file maximo-transposer — AWS Lambda handler.
 *
 * Triggered by an SES email receipt event. Retrieves the inbound email from S3,
 * parses the first XLSX/CSV attachment (a Rayven equipment-hours report),
 * transforms the rows into Maximo meter-reading import format (AUMETERDATA),
 * uploads two CSV files to S3, and emails the second (ENGINHRS-adjusted) file
 * to the DP World Maximo upload address.
 *
 * @module maximo-transposer
 */
```
**Location:** index.js:1

---

**[A02-2]** *(HIGH)*
**Description:** `exports.handler` has no JSDoc comment. It is the sole exported symbol and the Lambda entry point. Its parameters (`event`, `context`), its async return value, its side-effects (S3 reads, two S3 writes, one email send), and its error behaviour are entirely undocumented.
**Fix:** Add a JSDoc block immediately above line 9:
```js
/**
 * AWS Lambda handler. Processes an inbound SES email event, parses the
 * attached Rayven XLSX equipment-hours report, and produces two Maximo
 * AUMETERDATA CSV outputs — one raw and one with ENGINHRS recalculated
 * as (GANTRYHRS + HOISTHRS + TROLLEYHRS + BOOMHRS − PRNT Hour Meter).
 * The second CSV is emailed to the DP World Maximo upload distribution list.
 *
 * @async
 * @param {Object} event   - AWS Lambda event object. Must contain
 *                           `event.Records[0].ses` with a valid SES
 *                           notification including `mail.messageId`.
 * @param {Object} context - AWS Lambda context object (unused).
 * @returns {Promise<Object>} Resolves with the nodemailer sendMail result
 *                            for the outbound equipment-status email.
 */
```
**Location:** index.js:9

---

**[A02-3]** *(HIGH)*
**Description:** `dateFormatChange` has no JSDoc comment. Its parameter name, type, expected format, return type, and return format are undocumented. The only documentation present is an inline comment (`// Date format is Australian: dd/mm/yyyy hh:ii:ss`) that partially describes the input but says nothing about the return value format, error behaviour on malformed input, or the fact that single-digit day/month values are zero-padded.
**Fix:** Add a JSDoc block immediately above line 3146:
```js
/**
 * Converts an Australian date-time string to ISO 8601 format.
 *
 * @param {string} date - Date-time string in Australian format:
 *                        `dd/mm/yyyy hh:mm:ss` (single-digit day or month
 *                        values are accepted and will be zero-padded).
 * @returns {string} Date-time string in the format `YYYY-MM-DDThh:mm:ss`,
 *                   suitable for use as a Maximo NEWREADINGDATE value.
 * @example
 * dateFormatChange("3/7/2025 09:15:00"); // returns "2025-07-03T09:15:00"
 */
```
**Location:** index.js:3146

---

**[A02-4]** *(HIGH)*
**Description:** `asset_map` is a large, complex data structure (spanning lines 31–3103) with no JSDoc or explanatory block comment describing its schema. A reader cannot understand the structure — the roles of `assets`, `assettag`, `assetnum`, and `assettype` fields, what the compound key format `"<assetId> - <siteId>"` means, or why `assettag` and `assetnum` sometimes differ (e.g. `"FL239 - AUPBT-C1"` uses `assettag: "FL239-HRS-ENG"` and `assetnum: "FL239-ENG"` while most assets use identical values) — without reading hundreds of lines of data.
**Fix:** Add a block comment immediately before line 31 explaining:
- The key format (`"<vehicleId> - <siteId>"`)
- The `assets` sub-object (keyed by Maximo meter name; each entry has `assettag` and `assetnum`)
- The `assettype` field (equipment category code)
- Why `assettag` and `assetnum` can differ from the vehicle ID
- A note that the map is the authoritative source for which vehicles and meters are in scope

Example:
```js
// asset_map — lookup table for all in-scope DP World equipment.
// Key format: "<vehicleId> - <siteId>" (matches the "Vehicle Name" column in the Rayven report).
// Each value has:
//   assets   {Object} — sub-map keyed by Maximo meter name (e.g. RUNHRS, GANTRYHRS).
//                       Each entry contains:
//                         assettag {string} — Maximo asset tag for this meter.
//                         assetnum {string} — Maximo asset number for this meter.
//                       assettag and assetnum are often identical but may differ
//                       when DP World have reassigned asset records (see e.g. FL239-ENG).
//   assettype {string} — Equipment category code (QC, RTG, FL, GEN, TT, RS, ASC, SH, TVE).
//
// Note: DP World have made changes over time; assettags and assetnums
// do not necessarily correspond to current physical asset labels.
```
**Location:** index.js:31

---

**[A02-5]** *(MEDIUM)*
**Description:** `column_map` at line 3107 has a minimal inline comment (`// Map of existing report column names to the DP World asset names.`) but this description is slightly inaccurate: the keys are Maximo meter names (internal codes like `RUNHRS`), and the values are the corresponding column header strings in the incoming Rayven report — not "DP World asset names". The comment also does not mention that `RUNKM` (used by TVE-type assets) is absent from the map, meaning TVE assets will silently produce no output rows. No JSDoc is present.
**Fix:** Replace the existing comment with an accurate one:
```js
// column_map — maps Maximo meter names (used as keys in asset_map.assets)
// to the corresponding column headers in the incoming Rayven XLSX report.
// Only meters present here will be included in output rows; meters absent
// from this map (e.g. RUNKM used by TVE assets, SPREADERHRS used by ASC assets)
// will be silently skipped.
```
**Location:** index.js:3105

---

**[A02-6]** *(MEDIUM)*
**Description:** `cranes_rtgs` (lines 3288–3358) is a large inline object defined inside the `for` loop body on every iteration. It has no comment explaining why it exists as a separate data structure from `asset_map`, what the values represent (they are identical to the keys — the object is used purely as a set for membership testing), or why this list partially overlaps with but does not exactly mirror the QC/RTG entries in `asset_map` (e.g. `"RTG14 - AUFRE-C1"` is in `asset_map` but the key in `cranes_rtgs` line 3332 is `"RTG914 - AUFRE-C1"`, matching the internal asset tag rather than the map key). There is also no comment explaining that this object is recreated on every loop iteration, which is a performance concern.
**Fix:** Add a comment block before line 3288 explaining:
- That this object acts as a Set of vehicle names requiring ENGINHRS to be computed rather than read from the report column
- That the values are intentionally identical to the keys (membership test only)
- That it should ideally be hoisted outside the loop
**Location:** index.js:3285

---

**[A02-7]** *(MEDIUM)*
**Description:** The first processing loop (lines 3176–3207) and second processing loop (lines 3274–3414) are structurally near-identical but serve different purposes. The first loop produces `result` (raw meter readings as-reported by Rayven). The second loop produces `result_2` (with ENGINHRS recalculated). There is no comment explaining the distinction between the two outputs, why both are generated, or what `result` is ultimately used for given that its upload to S3 is the only use and the email sends only `result_2`.
**Fix:** Add a comment block before line 3176 explaining:
```js
// First pass: build result[] as a direct transcription of all meter readings
// from the Rayven report, with no recalculation. Uploaded to S3 as a
// "*-formatted.csv" archive file. NOT emailed.
```
And before line 3259:
```js
// Second pass: build result_2[] with the same records but with ENGINHRS
// recalculated for QC/RTG/ASC cranes as:
//   GANTRYHRS + HOISTHRS + TROLLEYHRS + BOOMHRS − PRNT Hour Meter
// This is the file that is emailed to the Maximo upload distribution list.
```
**Location:** index.js:3176 and index.js:3259

---

**[A02-8]** *(MEDIUM)*
**Description:** Dead / commented-out code occupies significant space throughout the file and has no explanatory comments clarifying intent:
- Lines 10–25: A fully commented-out test email send. The `console.log("Test email sent.")` at line 26 is live but refers to an email send that is commented out, making the log message actively misleading.
- Lines 3232–3249: A fully commented-out production email send (`dpw.upload@bpdzenith.com`) with no explanation of why it was disabled or whether it should be reinstated.
- Lines 3446–3457: A fully commented-out test `sendMail` call inside the live code path, with no explanation.
- Lines 3251–3257 and 3475–3481: Banners reading `TEST WITH PRNT HOURS COMING FROM NEW CALCULATION` and `END OF THE TEST`. These suggest the entire second result block was a temporary experiment that was never cleaned up.

None of these blocks have comments explaining their status (intentionally disabled, superseded, pending removal, etc.).
**Fix:** Each commented-out block should carry a one-line explanation: why it is disabled, whether it is safe to delete, and (for the `console.log` at line 26) the log message should either be removed or corrected to accurately reflect what happened.
**Location:** index.js:10, index.js:26, index.js:3232, index.js:3251, index.js:3446, index.js:3475

---

**[A02-9]** *(MEDIUM)*
**Description:** The `csv.replace(",,,", "")` calls at lines 3217 and 3424 are explained by adjacent comments, but the comments are imprecise. The comment states "the first row has trailing commas" but the fix is applied to the entire CSV string, not just the first row. Additionally, the regex is a literal string that replaces only the first occurrence of exactly three consecutive commas, which may not generalise correctly to all cases (e.g. four commas, or a row with different trailing column counts). The comment does not acknowledge this limitation.
**Fix:** Amend the comment to accurately describe what the replacement actually does:
```js
// The Maximo import header row ("AUMTRSYS","AUMETERDATA","AddChange","EN")
// has 4 columns, while the data rows have 7. The XLSX library pads all rows
// to the same width, resulting in trailing commas on the header row.
// This replacement removes the first occurrence of ",,," from the CSV.
// Note: this is a minimal fix — it removes only one occurrence. If the data
// itself contains ",,," this could produce incorrect output.
```
**Location:** index.js:3213

---

**[A02-10]** *(LOW)*
**Description:** The variable `from` at line 3131 (`const from = parsed_mail.from.text;`) is assigned but never used anywhere in the function. There is no comment explaining why it is captured (e.g. for future use, for logging, for validation).
**Fix:** Either add a comment explaining the intent (`// captured for future sender-validation use`) or remove the assignment. No JSDoc change is needed but the absence of any comment makes the dead assignment confusing.
**Location:** index.js:3131

---

**[A02-11]** *(LOW)*
**Description:** The `context` parameter of `exports.handler` (line 9) is received but never referenced anywhere in the function body. There is no comment explaining this. While it is conventional in Lambda to accept `context` even when unused, a comment or JSDoc `@param` noting it is unused (or intentionally reserved) would prevent future maintainers from wondering whether it was accidentally omitted from use.
**Fix:** Document in the JSDoc for `exports.handler` (see A02-2) with `@param {Object} context - AWS Lambda context object (unused).`
**Location:** index.js:9

---

**[A02-12]** *(LOW)*
**Description:** The inline comment at line 3196 inside the first loop reads:
```js
// That's a problem. No map for this hour meter.
// So, the asset will be missing from the output
// but the file will continue to process
```
This comment appears twice (lines 3196–3199 and lines 3402–3406) and in both cases describes a silent failure — an asset meter with no `column_map` entry is silently skipped, with no logging, no error, and no notification. Similarly, lines 3201–3206 and 3408–3413 describe a vehicle missing from `asset_map` with a comment that says "Do some sort of error logging / notification" — indicating the error handling was never implemented. These comments accurately describe the gaps but have been present without action; they are effectively TODOs masquerading as explanations.
**Fix:** Convert to explicit `// TODO:` markers so they are discoverable by tooling:
```js
// TODO: No column_map entry for this meter name. The reading will be silently
//       omitted from the output. Add a console.error or SES notification here.
```
```js
// TODO: Vehicle not found in asset_map. The vehicle will be silently omitted.
//       Add console.error or notification logic here.
```
**Location:** index.js:3196 and index.js:3201

---

**[A02-13]** *(LOW)*
**Description:** The `RUNKM` meter key (used by all TVE-type assets: TVE585 through TVE603, lines 2207–2349) is not present in `column_map` (line 3107–3115). This means all TVE vehicles will be silently skipped during output construction (the `else` branch at line 3195 is hit for every TVE row). There is no comment on `asset_map` or `column_map` acknowledging this. This is a data-correctness gap, but from the documentation perspective the absence of any comment explaining the exclusion is the finding.
**Fix:** Add a comment to `column_map` noting the omission:
```js
// Note: RUNKM (used by TVE assets) is intentionally excluded here because
// the Maximo import format for kilometre meters differs from hour meters.
// TVE assets will produce no output rows until RUNKM handling is implemented.
```
Or if the exclusion is a bug, note it as such. Either way it must be documented.
**Location:** index.js:3107

---

**[A02-14]** *(INFO)*
**Description:** The `column_map` does not include `SPREADERHRS`, which is defined in all ASC asset entries (lines 2495–2958). ASC assets have SPREADERHRS as one of their meter keys, but because SPREADERHRS is not in `column_map`, it will be silently skipped in both output loops (same mechanism as A02-13 for TVE/RUNKM). The comment at lines 3105–3106 does not mention this.
**Fix:** Add `SPREADERHRS: "Spreader Hour Meter"` to `column_map` if Spreader readings are required, or add an explicit exclusion comment if intentional.
**Location:** index.js:3107

---

**[A02-15]** *(INFO)*
**Description:** The `assettype` field for entries `"RTG913 - AUFRE-C1"` through `"RTG918 - AUFRE-C1"` (lines 2056–2205) is set to `"QC"` rather than `"RTG"`. These entries have RTG-prefixed keys and RTG-prefixed asset tags/nums, but their `assettype` is `"QC"`. There is no comment explaining whether this is intentional (i.e. these RTGs are classified as QC in Maximo at Fremantle). This is a data ambiguity with no documentation.
**Fix:** Add an inline comment on the affected entries:
```js
assettype: "QC", // Classified as QC in Maximo despite RTG vehicle prefix
```
**Location:** index.js:2079 (first occurrence, pattern repeats through line 2204)

---

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 1 |
| HIGH | 3 |
| MEDIUM | 5 |
| LOW | 4 |
| INFO | 2 |
| **Total** | **15** |

### Key themes
1. **No documentation exists at any level.** The module, the exported handler, and the only named inner function (`dateFormatChange`) all have zero JSDoc. This is the most severe systemic gap.
2. **Large data structures are undescribed.** `asset_map` (3000+ lines of data) and `cranes_rtgs` (a 60-entry inline object rebuilt on every loop iteration) have no schema documentation.
3. **Commented-out code with no status explanation** creates confusion about what is intentional, what is disabled, and what is a leftover experiment.
4. **Silent failure paths have placeholder comments** (`"Do some sort of error logging"`) that have never been implemented, with no TODO markers to make them discoverable.
5. **Data gaps** (TVE/RUNKM and ASC/SPREADERHRS excluded from `column_map`, RTG assets mis-typed as QC) are undocumented.
