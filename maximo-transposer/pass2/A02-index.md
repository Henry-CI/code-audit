# A02 — Pass 2: Test Coverage
**File:** `index.js`
**Audit run:** 2026-02-27-01
**Date:** 2026-02-27
**Agent:** A02

---

## Pre-flight

Branch verified as `master`. Proceeding.

---

## Step 1 — Locate Test Files

### Glob results

| Pattern | Result |
|---|---|
| `**/*.test.js` | No files found |
| `**/*.spec.js` | No files found |
| `**/test/**` | No files found |
| `**/__tests__/**` | No files found |

### Grep for test framework references

A grep across the entire repository for the strings `jest`, `mocha`, `chai`, `tape`, `ava`, and `vitest` returned **zero matches in any source or configuration file**. The only matches were inside previously generated audit markdown files (which mention "jest" as a checklist suggestion), confirming no test framework is present or referenced in the codebase itself.

**Conclusion:** There are no test files of any kind in this repository. The codebase has 0% automated test coverage.

---

## Step 2 — Source File Read

`index.js` was read in full across multiple chunks (lines 1–3485). No line was skipped.

---

## Step 3 — Reading Evidence

### Module / export name

- **Module type:** AWS Lambda handler module (CommonJS, `"use strict"`)
- **Exported symbol:** `exports.handler` — the single Lambda entry point, defined at **line 9**

### Functions

| Function | Type | Line |
|---|---|---|
| `exports.handler` | async Lambda handler (arrow function) | 9 |
| `dateFormatChange(date)` | inner named function | 3146 |

No other named or anonymous functions are defined outside these two.

### Exported symbols

| Symbol | Line |
|---|---|
| `exports.handler` | 9 |

### `require()` statements

| Module | Variable | Line |
|---|---|---|
| `aws-sdk` | `aws` | 2 |
| `nodemailer` | `nodemailer` | 3 |
| `mailparser` (`.simpleParser`) | `simpleParser` | 4 |
| `xlsx` | `XLSX` | 5 |

### `process.env.X` accesses

**None.** No environment variables are read anywhere in the file. AWS credentials, bucket names, SES region, recipient addresses, and sender address are all hardcoded literals.

### Top-level side-effects at module load time

| Expression | Line |
|---|---|
| `new aws.S3()` — S3 client constructed | 6 |
| `new aws.SES({ region: "us-west-2" })` — SES client constructed | 7 |

### Data structures

| Name | Type | Lines |
|---|---|---|
| `asset_map` | Plain object (lookup table, ~200 asset entries) | 31–3103 |
| `column_map` | Plain object (7-entry lookup table) | 3107–3115 |
| `cranes_rtgs` | Plain object (inline lookup table rebuilt on every loop iteration) | 3288–3358 |

### Main logic flow and every branch / condition

| Step | Line(s) | Description |
|---|---|---|
| 1 | 3118 | `event.Records[0].ses` — assumes SNS/SES event structure exists, no guard |
| 2 | 3121–3124 | Build S3 `getObject` params using hardcoded bucket and `messageId` |
| 3 | 3126 | `await s3.getObject(params).promise()` — S3 fetch, no try/catch |
| 4 | 3128 | `data.Body.toString()` — no null-check on `data` or `data.Body` |
| 5 | 3130 | `await simpleParser(email)` — no try/catch |
| 6 | 3131 | `parsed_mail.from.text` — no null-check on `from` |
| 7 | 3132 | `parsed_mail.attachments` — no null/length check |
| 8 | 3134 | `attachments[0].content` — no bounds check; crashes if attachments is empty |
| 9 | 3134–3137 | `XLSX.read(...)` — no try/catch for malformed binary |
| 10 | 3139 | `workbook.SheetNames[0]` — no check for empty workbook |
| 11 | 3141 | `XLSX.utils.sheet_to_json(...)` — returns `[]` for empty sheet; handled implicitly by loop |
| 12 | 3176 | `for` loop over `sheetJSON` |
| 13 | 3178 | Read `sheetJSON[i]["Vehicle Name"]` — no check if key exists |
| 14 | 3180 | **Branch A:** `if (vehicle_name in asset_map)` — vehicle known |
| 15 | 3182 | `for...in` over `asset_map[vehicle_name].assets` |
| 16 | 3183 | **Branch B:** `if (asset_name in column_map)` — meter type is mapped |
| 17 | 3192 | `dateFormatChange(sheetJSON[i]["Last reported date"])` — no null-check on date field |
| 18 | 3195–3199 | **Branch C (else):** asset_name not in column_map — silently skipped, no logging |
| 19 | 3201–3206 | **Branch D (else):** vehicle_name not in asset_map — silently skipped, no logging |
| 20 | 3210–3211 | Build CSV via `aoa_to_sheet` / `sheet_to_csv` |
| 21 | 3217 | `csv.replace(",,,", "")` — simple string replace, no regex; only fixes first occurrence |
| 22 | 3229 | `await s3.upload(fileParams).promise()` — 1st S3 upload, no try/catch |
| 23 | 3274 | Second `for` loop over `sheetJSON` (duplicates loop logic) |
| 24 | 3278 | **Branch E:** `if (vehicle_name in asset_map)` (second pass) |
| 25 | 3281 | **Branch F:** `if (asset_name in column_map)` (second pass) |
| 26 | 3359 | **Branch G:** `if (asset_name == "ENGINHRS")` |
| 27 | 3360 | **Branch H:** `if (vehicle_name in cranes_rtgs)` — ENGINHRS crane/RTG path |
| 28 | 3365–3370 | Calculate `parent_hours` from individual meter readings — no NaN guard |
| 29 | 3380–3389 | **Branch I (else):** ENGINHRS for non-crane — push raw reading |
| 30 | 3391–3401 | **Branch J (else):** asset_name is not ENGINHRS — push raw reading |
| 31 | 3402–3406 | **Branch K (else):** asset_name not in column_map — silently skipped |
| 32 | 3408–3413 | **Branch L (else):** vehicle_name not in asset_map — silently skipped |
| 33 | 3417–3418 | Build second CSV |
| 34 | 3424 | `csv_2.replace(",,,", "")` — same single-occurrence replace limitation |
| 35 | 3436 | `await s3.upload(fileParams_2).promise()` — 2nd S3 upload, no try/catch |
| 36 | 3440–3442 | `nodemailer.createTransport({ SES: { ses, aws } })` |
| 37 | 3459–3473 | `await transporter_2.sendMail(...)` — SES send, no try/catch |
| 38 | 3483 | `return mail_result_2` |

### `dateFormatChange(date)` inner function branches

| Step | Line(s) | Description |
|---|---|---|
| 1 | 3148 | `date.split(" ")` — assumes space separator; no guard if `date` is undefined/null |
| 2 | 3149 | `arr[0].split("/")` — assumes slash separator |
| 3 | 3152 | **Branch:** `dates[1].length == 1` — zero-pad single-digit month |
| 4 | 3153 | **Branch:** `dates[0].length == 1` — zero-pad single-digit day |
| 5 | 3156 | Concatenate ISO-ish timestamp string |

---

## Step 4 — Coverage Gap Analysis

Since **no tests exist at all**, every function, branch, and path is a gap. The findings below are ordered by severity.

---

**[A02-1]** *(CRITICAL)*
**Description:** The entire codebase has zero automated tests. There is no test framework installed or configured (`package.json` lists no test script, no devDependencies for jest/mocha/chai/tape/ava/vitest). A Lambda function that processes financial/operational data for a port operator and sends emails to external parties has never been exercised in isolation.
**Fix:** Install a test framework (e.g., `jest`) and set `"test": "jest"` in `package.json`. Create a `__tests__/` directory. Mock `aws-sdk` (S3 + SES), `nodemailer`, `mailparser`, and `xlsx`. Write an integration test that drives `exports.handler` with a minimal synthetic SES event.
**Location:** `index.js:9` (`exports.handler`)

---

**[A02-2]** *(CRITICAL)*
**Description:** `attachments[0].content` is accessed at line 3134 without any check on whether `parsed_mail.attachments` exists or has at least one element. If the inbound email has no attachment, or the attachment array is empty, the Lambda throws `TypeError: Cannot read properties of undefined (reading 'content')` and the entire invocation fails with no actionable error message.
**Fix:** Add a test that calls the handler with an email that has zero attachments. The handler should either return a structured error response or throw a domain-specific error. The test should assert that the process fails gracefully rather than with an uncaught TypeError.
**Location:** `index.js:3134`

---

**[A02-3]** *(CRITICAL)*
**Description:** There is no try/catch anywhere in the handler. Failures in `s3.getObject` (non-existent key, permission denied, network error), `simpleParser` (malformed MIME), `XLSX.read` (non-xlsx binary), either `s3.upload` call, or `transporter_2.sendMail` all propagate as unhandled promise rejections and will cause Lambda to log an opaque error and retry the event indefinitely (depending on SQS/SNS configuration).
**Fix:** Add tests that mock each AWS/library call to reject. Assert the handler either catches and logs the error or re-throws a structured error. At minimum: (a) S3 getObject failure, (b) XLSX.read failure with a PDF attachment, (c) SES sendMail failure.
**Location:** `index.js:3126`, `index.js:3130`, `index.js:3134`, `index.js:3229`, `index.js:3436`, `index.js:3459`

---

**[A02-4]** *(HIGH)*
**Description:** `dateFormatChange(date)` is an untested inner function that implements a bespoke Australian date parser. It is called at lines 3192 and 3377/3387/3397 for every row in the spreadsheet. It silently produces garbage output (or throws) if `date` is `undefined`, `null`, an empty string, an ISO date string, a US-format date (mm/dd/yyyy), or missing the time component (no space in the string). There are no guards.
**Fix:** Extract `dateFormatChange` to a module-level export so it can be unit-tested independently. Write tests for: (a) valid Australian date `"31/12/2024 08:30:00"` → expect `"2024-12-31T08:30:00"`, (b) single-digit day and month `"1/3/2024 00:00:00"` → expect `"2024-03-01T00:00:00"`, (c) `undefined` input → expect a thrown error or empty string, (d) ISO-format input `"2024-12-31T08:30:00"` → document expected behaviour.
**Location:** `index.js:3146–3159`

---

**[A02-5]** *(HIGH)*
**Description:** The `cranes_rtgs` lookup object (lines 3288–3358) is rebuilt from scratch on **every iteration** of the inner `for...in` loop. This is a performance bug, but more importantly it is untested: the `ENGINHRS` branch (line 3359) and the crane vs. non-crane sub-branch (line 3360) have never been exercised. The `parent_hours` arithmetic at lines 3365–3370 (`GANTRY + HOIST + TROLLEY + BOOM - PRNT`) can produce `NaN` if any spreadsheet cell is empty or non-numeric, and `NaN` is silently written into the output CSV.
**Fix:** Add a test with a QC/RTG vehicle row where `ENGINHRS` is a field, numeric meter values are provided, and assert the calculated `parent_hours` is numerically correct. Add a second test with a missing/empty `"Boom Hour Meter"` cell and assert the row is either excluded or an error is raised instead of `NaN` being emitted.
**Location:** `index.js:3288–3378`

---

**[A02-6]** *(HIGH)*
**Description:** `event.Records[0].ses` (line 3118) is accessed without any guard. If the Lambda is invoked with a test event that has no `Records` array, or an empty `Records` array, or a record that is not an SES notification, the handler throws immediately. There is no input validation or schema check on the incoming event.
**Fix:** Add a test that passes a completely empty object `{}` as the event and asserts the handler returns a structured validation error rather than throwing a `TypeError`. Add a second test with a valid SES event shape but an empty `Records` array.
**Location:** `index.js:3118`

---

**[A02-7]** *(HIGH)*
**Description:** The `csv.replace(",,,", "")` calls at lines 3217 and 3424 use a plain string argument, not a regex with the global flag. `String.prototype.replace` with a string argument replaces only the **first** occurrence. If the generated CSV has multiple rows with trailing commas (which it will for any output with more than one row shorter than the maximum column count), all subsequent trailing commas remain. This logic is never tested, so the defect has never been caught.
**Fix:** Add a test that provides a spreadsheet with at least two rows that would produce trailing commas in the output CSV and assert that **all** trailing comma sequences are removed from the resulting string.
**Location:** `index.js:3217`, `index.js:3424`

---

**[A02-8]** *(MEDIUM)*
**Description:** When a `vehicle_name` from the spreadsheet is not found in `asset_map` (Branch D, line 3201; Branch L, line 3408), the code silently continues. No error, no log beyond what is already printed, and the vehicle is simply absent from the output file. The customer (DP World) would receive an incomplete Maximo import CSV with no indication that records were dropped. This is untested.
**Fix:** Add a test that includes a spreadsheet row with a vehicle name not present in `asset_map` and assert either (a) the output contains a warning row, or (b) the handler raises a structured notification, or at minimum (c) a `console.warn` / `console.error` is called (spy on it). Document the chosen behaviour.
**Location:** `index.js:3201–3206`, `index.js:3408–3413`

---

**[A02-9]** *(MEDIUM)*
**Description:** When an `asset_name` from the asset map is not present in `column_map` (Branch C, line 3195; Branch K, line 3402), the hour meter reading is silently dropped. This is also untested. The `column_map` currently omits `RUNKM` (used by TVE assets) and `SPREADERHRS` (used by ASC assets) — those meter types will always silently fail the column_map lookup and be excluded from both output CSVs.
**Fix:** Add a test where an asset entry uses `RUNKM` or `SPREADERHRS` and assert the row either appears correctly or produces a warning. Separately, verify whether `RUNKM` and `SPREADERHRS` should be in `column_map`; if so, add them and test the output.
**Location:** `index.js:3107–3115` (`column_map`), `index.js:3183`, `index.js:3195–3199`

---

**[A02-10]** *(MEDIUM)*
**Description:** `parsed_mail.from.text` (line 3131) is read and stored in `from` but the variable is never used after that. This is dead code / a vestigial reference. More importantly, `parsed_mail.from` could be `null` if the email has no `From:` header (malformed email), which would throw `TypeError: Cannot read properties of null (reading 'text')`. This path is untested.
**Fix:** Add a test that passes a minimal raw email with no `From:` header and assert the handler does not crash on line 3131. Either add a null guard or remove the unused variable.
**Location:** `index.js:3131`

---

**[A02-11]** *(MEDIUM)*
**Description:** The S3 bucket name `"maximo-transposer-bucket"` and both output email addresses (lines 3461–3462) are hardcoded literals. There are no `process.env` reads. This means: (a) the bucket name cannot be changed for staging vs. production without a code deploy, (b) there is no way to test with a different bucket without modifying source, and (c) since there are no tests, the correctness of these literals has never been verified programmatically.
**Fix:** Add a test that asserts `s3.upload` is called with `Bucket: "maximo-transposer-bucket"` and `Key` matching the expected filename pattern (timestamp + `-formatted.csv`). This documents the hardcoded configuration as a deliberate contract. Recommend migrating bucket and recipients to `process.env` for testability and operational flexibility.
**Location:** `index.js:3122`, `index.js:3431`, `index.js:3461`

---

**[A02-12]** *(MEDIUM)*
**Description:** The `"Vehicle Name"` column key (line 3178, 3276) and `"Last reported date"` column key (lines 3192, 3377, 3387, 3397) are hardcoded strings that must exactly match the spreadsheet column headers sent by Rayven. There is no test that validates what happens if Rayven changes a column heading (e.g. capitalisation change, extra space). The row would silently produce `undefined` values in the output.
**Fix:** Add a test with a spreadsheet row that uses `"vehicle name"` (lowercase) as the column header and assert the handler either maps it correctly or emits a detectable error, rather than silently producing `undefined` in the output CSV.
**Location:** `index.js:3178`, `index.js:3192`

---

**[A02-13]** *(MEDIUM)*
**Description:** The second result loop (lines 3274–3414) is almost entirely duplicated from the first loop (lines 3176–3207), with the only addition being the `ENGINHRS` / `cranes_rtgs` branch. Both loops iterate `sheetJSON` and push to separate result arrays. Because neither loop is tested, the relationship between the two outputs is undefined by any specification. If the first loop is ever changed, the second may silently diverge.
**Fix:** Add separate tests for the first loop output (basic meter mapping) and the second loop output (ENGINHRS calculation). Assert that the row counts and content of both output CSVs are independently correct for the same input.
**Location:** `index.js:3176–3207`, `index.js:3274–3414`

---

**[A02-14]** *(LOW)*
**Description:** The `sheetJSON` array for an empty spreadsheet (header row only, zero data rows) results in `sheetJSON = []`. Both loops execute zero iterations, and two CSVs with only the two header rows are uploaded to S3 and emailed. This edge case is never tested and the stakeholder impact (receiving a valid-looking but empty Maximo import file) is not documented.
**Fix:** Add a test with an Excel workbook that has column headers but zero data rows. Assert the handler completes without error, the output CSVs contain exactly the two header rows, and the email is still sent.
**Location:** `index.js:3176`, `index.js:3274`

---

**[A02-15]** *(LOW)*
**Description:** `workbook.SheetNames[0]` (line 3139) assumes the workbook has at least one sheet. An empty workbook (saved with no sheets, which is technically invalid XLSX but producible) would return `undefined` and cause `workbook.Sheets[undefined]` to be `undefined`, followed by `XLSX.utils.sheet_to_json(undefined, {})` throwing or returning unexpected data.
**Fix:** Add a test with a valid XLSX buffer that has zero sheets (or simulate `workbook.SheetNames = []`) and assert the handler fails with a readable error rather than a cryptic downstream exception.
**Location:** `index.js:3139`

---

**[A02-16]** *(LOW)*
**Description:** The `"RTG14 - AUFRE-C1"` entry in `asset_map` (line 2081) maps to assets tagged `RTG914` / `RTG914`. This looks like a data-entry error (the key says `RTG14`, the values say `RTG914`). Additionally, `"RTG913 - AUFRE-C1"` and several other AUFRE RTGs have `assettype: "QC"` (lines 2079, 2104, 2129, 2154, 2179, 2204) despite being labelled RTG. These inconsistencies cannot be caught without tests that assert the lookup table shape.
**Fix:** Add a unit test that iterates every key in `asset_map` and asserts (a) the key suffix matches the `assetnum` in at least the first asset sub-entry, and (b) entries whose key starts with `RTG` have `assettype` of `"RTG"` (or document the exceptions explicitly). This would have caught the `RTG14` typo.
**Location:** `index.js:2081`, `index.js:2079`

---

**[A02-17]** *(INFO)*
**Description:** `nodemailer` is `require()`d (line 3), the first email-send block (`transporter_test`, lines 11–24) is entirely commented out, and the second email-send block (`transporter_2`) includes both a commented-out test variant and the live send. The commented code inflates the file and obscures the true execution path. No test verifies that the send is actually called, or that the correct recipient list is used.
**Fix:** Remove commented-out dead code. Add a test that stubs `transporter_2.sendMail` and asserts it is called exactly once with `to` containing the expected recipient addresses and an attachment named `maximo_equipment_status_report.csv`.
**Location:** `index.js:11–24`, `index.js:3446–3457`

---

## Summary Table

| ID | Severity | Short description |
|---|---|---|
| A02-1 | CRITICAL | No tests exist — 0% coverage |
| A02-2 | CRITICAL | No guard on empty attachments array |
| A02-3 | CRITICAL | No try/catch on any async operation |
| A02-4 | HIGH | `dateFormatChange` untested; crashes on null/malformed input |
| A02-5 | HIGH | ENGINHRS/cranes_rtgs branch untested; NaN silently emitted |
| A02-6 | HIGH | `event.Records[0]` accessed without input validation |
| A02-7 | HIGH | `replace(",,,", "")` only fixes first occurrence; untested |
| A02-8 | MEDIUM | Unknown vehicle silently dropped from output |
| A02-9 | MEDIUM | Unknown asset column silently dropped; RUNKM/SPREADERHRS excluded |
| A02-10 | MEDIUM | `parsed_mail.from` null path untested; `from` variable unused |
| A02-11 | MEDIUM | Hardcoded bucket name and recipients never verified by test |
| A02-12 | MEDIUM | Hardcoded column header strings never validated |
| A02-13 | MEDIUM | Two near-identical loops with no independent test coverage |
| A02-14 | LOW | Empty spreadsheet edge case untested |
| A02-15 | LOW | Empty workbook (zero sheets) edge case untested |
| A02-16 | LOW | `asset_map` data integrity errors undetectable without tests |
| A02-17 | INFO | Commented-out dead code; sendMail call never asserted |
