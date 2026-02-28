# A02 — Pass 1 Security Audit: index.js
**Auditor:** A02
**Date:** 2026-02-27
**Branch:** master
**File:** `index.js` (3484 lines)

---

## READING EVIDENCE

### File path
`C:/Projects/cig-audit/repos/maximo-transposer/index.js`

### Exported functions / objects
| Name | Line |
|------|------|
| `exports.handler` (async function, Lambda entry point) | 9 |

No other exports are present in this file.

### `require()` / `import` statements
| Module | Line |
|--------|------|
| `require("aws-sdk")` → `aws` | 2 |
| `require("nodemailer")` → `nodemailer` | 3 |
| `require("mailparser").simpleParser` → `simpleParser` | 4 |
| `require("xlsx")` → `XLSX` | 5 |

### `process.env.X` accesses
None. No `process.env` references appear anywhere in `index.js`.

---

## CHECKLIST REVIEW

### 1. Secrets and Configuration

**Finding A02-1 below covers hardcoded bucket name. Additional observations:**

- No AWS access keys (`AKIA...`) or secret access keys are present in source.
- No SES SMTP passwords are present in source.
- No Maximo API credentials are present in source.
- The S3 bucket name `"maximo-transposer-bucket"` is hardcoded at lines 3122 and 3224 and 3431. This is addressed in the finding below.
- The SES region `"us-west-2"` is hardcoded at line 7. This is configuration, not a secret, but it is inflexible and undocumented.
- No `package.json` scripts were examined in this file (out of scope for this file; covered by other agents).
- Email addresses for recipients are hardcoded in plain text at lines 3461–3462. These include internal distribution addresses (DP World and Collective Intelligence staff). This is addressed in finding A02-2.

**[A02-1]** *(LOW)*
**Description:** The S3 bucket name `"maximo-transposer-bucket"` is hardcoded directly in the source at three locations (lines 3122, 3224, 3431). If the bucket is renamed, the code must be changed. More significantly, hardcoding infrastructure names in source rather than in Lambda environment variables means the value cannot be changed between deployments (dev/staging/prod) without a code change, and it appears in version control history permanently. There are no secrets here, but the pattern is contrary to 12-factor and the serverless best practice of externalizing all configuration.
**Location:** index.js:3122, index.js:3224, index.js:3431
**Checklist item:** 1. Secrets and Configuration

**[A02-2]** *(MEDIUM)*
**Description:** Recipient email addresses — including DP World staff addresses and internal BCC addresses — are hardcoded in the Lambda source code at lines 3461–3462. These are operational configuration values that will change over time (staff changes, domain changes). Hardcoding them in source means changes require a code deployment rather than a configuration update, and the full recipient list is permanently recorded in version control history. Additionally, the BCC list at line 3462 includes `rhythmduwadi@collectiveintelligence.com.au` and `sidney@collectiveintelligence.com.au`, meaning internal consultants silently receive every processed report. This is a data-governance concern: DP World's equipment meter data is being silently forwarded to third-party consultants on every invocation, which may not be disclosed to the client.
**Location:** index.js:3461–3462
**Checklist item:** 1. Secrets and Configuration

---

### 2. IAM and AWS Permissions

IAM role statements are defined in `serverless.yml`, which is outside the scope of this file. No IAM-related code (e.g., `sts:AssumeRole`, `iam:` API calls) appears in `index.js`.

Checklist item 2. IAM and AWS Permissions: no issues found in this file. (IAM configuration reviewed separately via serverless.yml.)

---

### 3. Input Validation

**[A02-3]** *(HIGH)*
**Description:** No sender verification is performed. The Lambda processes any email that arrives, regardless of who sent it. At line 3131 the sender address is parsed into `from` but the variable is never used for any validation or allowlist check. Any actor who can send email to the SES-monitored address can trigger the full processing pipeline, including S3 writes and email dispatch to DP World and other recipients. A malicious sender could deliberately craft a payload to trigger downstream errors, exhaust Lambda execution time, or cause spam to be sent from the verified SES identity to all recipients.
**Location:** index.js:3131
**Checklist item:** 3. Input Validation — Sender verification

**[A02-4]** *(HIGH)*
**Description:** No content-type validation is performed on the email attachment before it is passed to `XLSX.read()`. At line 3134 the code unconditionally reads `attachments[0].content` into the XLSX parser regardless of the attachment MIME type. Any file type (PDF, executable, ZIP, script) will be fed to the XLSX parser. This may trigger parser vulnerabilities or unexpected behavior for non-XLSX content. The checklist requires verification that only `.xlsx` / `.xls` types are processed.
**Location:** index.js:3134
**Checklist item:** 3. Input Validation — Attachment validation

**[A02-5]** *(HIGH)*
**Description:** No attachment size limit is enforced before calling `XLSX.read()`. The entire attachment content is loaded into memory at once (line 3134). A large attachment sent by any email sender (there is no sender allowlist — see A02-3) will expand in Lambda memory during XLSX parsing. This is a denial-of-service and Lambda-timeout vector. The XLSX library performs in-memory decompression of the ZIP structure inside an XLSX file; a crafted ZIP bomb (small compressed size, enormous decompressed size) will exhaust Lambda memory.
**Location:** index.js:3134
**Checklist item:** 3. Input Validation — Attachment size limits; XLSX processing — zip bomb protection

**[A02-6]** *(HIGH)*
**Description:** No row or column count limit is enforced on the parsed XLSX sheet. At line 3176 and again at line 3274, the code iterates `for (var i = 0; i < sheetJSON.length; i++)` with no upper bound on `sheetJSON.length`. An attacker who can send a crafted XLSX file with hundreds of thousands of rows can drive the Lambda to timeout, accumulate very large `result` and `result_2` arrays in memory, and cause out-of-memory termination.
**Location:** index.js:3176, index.js:3274
**Checklist item:** 3. Input Validation — XLSX processing — maximum rows/columns

**[A02-7]** *(MEDIUM)*
**Description:** Cell values from the XLSX attachment are written directly into the output CSV rows without checking for formula injection characters. At lines 3191 and 3397, `sheetJSON[i][original_column_name]` (a numeric meter reading from the input sheet) is placed into the output without sanitization. At lines 3192 and 3377/3387/3397, `dateFormatChange(sheetJSON[i]["Last reported date"])` is placed into the output. If a cell in the input sheet contains a value starting with `=`, `+`, `-`, or `@`, it will survive into the output CSV and may execute as a formula when the recipient opens the file in Excel. The `dateFormatChange` function at line 3146 does basic string splitting but does not validate that the input actually conforms to the expected date format, so an injected formula could survive. The output is emailed to DP World staff who will open the CSV in Excel or a compatible application.
**Location:** index.js:3191, index.js:3192, index.js:3377, index.js:3387, index.js:3397
**Checklist item:** 3. Input Validation — XLSX processing — formula injection

**[A02-8]** *(LOW)*
**Description:** The S3 key for the stored output files is constructed from `Math.floor(Date.now() / 1000).toString()` (a Unix timestamp) at lines 3221 and 3428. This is derived from the Lambda's own clock, not from user-controlled data, so there is no path-traversal risk from email metadata in the S3 key construction. However, the input email is retrieved from S3 using the raw `sesNotification.mail.messageId` at line 3123 as the S3 key. The message ID originates from SES, which is under AWS control and not user-supplied in the usual sense. SES message IDs follow a fixed UUID-style format and are not user-controllable. No path traversal risk is present in this specific usage. This item is noted as clear.

Checklist item 3. Input Validation — S3 key sanitization: no issues found (S3 output keys are timestamp-based; input key is SES-generated message ID).

---

### 4. Runtime Security

**[A02-9]** *(MEDIUM)*
**Description:** The `dateFormatChange` function at lines 3146–3159 performs no input validation on the date string before calling `.split()` and constructing a formatted string. If the "Last reported date" cell is missing, empty, or not a string, calling `.split(" ")` on a non-string or undefined value will throw a TypeError. This error is not caught anywhere in the handler. Because the entire handler is a single `async` function with no try/catch block, any such exception will propagate as an unhandled Promise rejection from the Lambda handler. In the Node.js Lambda runtime, an unhandled rejection causes the invocation to fail, but the failure mode is not always obvious. More critically, the error message and stack trace (including internal file paths) may be surfaced in CloudWatch logs without sanitization, and depending on SES bounce configuration, error details could be returned to the email sender.
**Location:** index.js:3146–3159, index.js:9 (no try/catch in handler)
**Checklist item:** 4. Runtime Security — unhandled Promise rejections; error handling

**[A02-10]** *(INFO)*
**Description:** No `eval()`, `new Function()`, or `child_process` usage appears anywhere in `index.js`. The XLSX library is used for parsing but no dynamic code execution is performed with user-controlled data.

Checklist item 4. Runtime Security — eval/child_process: no issues found.

**[A02-11]** *(INFO)*
**Description:** The Node.js runtime version cannot be determined from `index.js` itself — it is declared in `serverless.yml`. This item is noted here for completeness and is covered by the serverless.yml audit agent.

Checklist item 4. Runtime Security — Node.js runtime version: not applicable to this file.

**[A02-12]** *(MEDIUM)*
**Description:** The entire Lambda handler body (lines 9–3484) is a single `async` function with no `try/catch` block and no error handling. Any of the following will cause an unhandled Promise rejection that silently fails the invocation without sending any notification: (a) S3 `getObject` failure if the message ID key does not exist; (b) `simpleParser` failure on malformed email; (c) `XLSX.read` failure on a non-XLSX attachment; (d) `attachments[0]` being undefined if the email has no attachments; (e) `dateFormatChange` receiving a non-string value; (f) any S3 `upload` failure; (g) any SES `sendMail` failure. There is no dead-letter queue, no alerting, and no error notification path. The email sender receives no bounce message on failure.
**Location:** index.js:9–3484
**Checklist item:** 4. Runtime Security — unhandled Promise rejections

---

### 5. Dependencies

Dependency analysis (package.json, package-lock.json, npm audit) is outside the scope of `index.js` and is assigned to a separate agent. Observations from this file:

- `aws-sdk` (v2 implied by API usage — `new aws.S3()`, `new aws.SES()`) is used. AWS SDK v2 is in maintenance-only mode; v3 is the current release.
- `xlsx` (SheetJS) is used. Several formula-injection CVEs exist in older versions of this library.
- `mailparser` (`simpleParser`) is used.
- `nodemailer` is used.

**[A02-13]** *(MEDIUM)*
**Description:** The code uses AWS SDK v2 (`require("aws-sdk")`), which was placed into maintenance-only mode in September 2023. AWS SDK v2 no longer receives feature updates and may not receive security patches. AWS SDK v3 is the supported replacement.
**Location:** index.js:2
**Checklist item:** 5. Dependencies — outdated packages

Checklist item 5. Dependencies — node_modules committed to repo: not assessable from index.js; covered by repo-level review.

---

### 6. Lambda and AWS Configuration

Lambda timeout, memory, SES trigger configuration, and S3 bucket ACL settings are defined in `serverless.yml` and are outside the scope of `index.js`. Observations from this file relevant to Lambda configuration:

**[A02-14]** *(LOW)*
**Description:** The Lambda does not write any files to `/tmp` and therefore has no `/tmp` cleanup obligation. However, the code holds the entire email body as a string (`var email = data.Body.toString()` at line 3128), the full parsed XLSX workbook in memory (line 3134–3137), and two full `result` / `result_2` arrays before serializing to CSV. All of this resides in Lambda heap memory. If the execution environment is reused (warm Lambda), these large in-memory allocations are garbage-collected by Node.js between invocations, but there is no explicit release. This is not a direct security vulnerability but is a resource-management concern that could become relevant if memory limits are tight.
**Location:** index.js:3128, 3134, 3161, 3259
**Checklist item:** 6. Lambda and AWS Configuration — /tmp cleanup; memory

**[A02-15]** *(INFO)*
**Description:** The S3 bucket name `"maximo-transposer-bucket"` is used for both input (reading the raw SES email) and output (writing the formatted CSV files). Whether this bucket is publicly accessible cannot be determined from `index.js`; it depends on the S3 bucket policy and ACL configured outside this file.

Checklist item 6. Lambda and AWS Configuration — S3 bucket access controls: not determinable from index.js alone.

Checklist item 6. Lambda and AWS Configuration — Lambda timeout and memory configuration: not present in index.js; covered by serverless.yml audit.

Checklist item 6. Lambda and AWS Configuration — SES trigger configuration: not present in index.js; covered by serverless.yml audit.

---

## ADDITIONAL FINDINGS (outside direct checklist items but material)

**[A02-16]** *(MEDIUM)*
**Description:** At line 3134, the code accesses `attachments[0]` without checking that `attachments` is non-empty or that the array index exists. If an email arrives with no attachments (e.g., a test email, a spam trigger, or a malformed inbound message), `attachments[0]` will be `undefined`, and `.content` access will throw `TypeError: Cannot read properties of undefined`. This is not caught and will cause an unhandled rejection (see also A02-12).
**Location:** index.js:3134
**Checklist item:** 3. Input Validation — Attachment validation; 4. Runtime Security — unhandled Promise rejections

**[A02-17]** *(LOW)*
**Description:** There is dead / commented-out code throughout the file. The test email block at lines 11–25 is fully commented out but `console.log("Test email sent.")` at line 26 remains active and executes unconditionally on every invocation, even though no test email is sent. The first send-email block (lines 3233–3249) is commented out. The second test send-email block (lines 3446–3457) is commented out. The active send at lines 3459–3473 dispatches to a large production recipient list. This inconsistent state (dead code, misleading log output, production send embedded in a section labelled "TEST") suggests the code has not been properly cleaned up, making auditing harder and increasing the risk that future changes may accidentally re-enable commented code.
**Location:** index.js:26, 3233–3249, 3446–3457, 3459–3473
**Checklist item:** 4. Runtime Security — error handling (misleading log output)

**[A02-18]** *(LOW)*
**Description:** The `csv.replace(",,,", "")` call at line 3217 (and `csv_2.replace(",,,", "")` at line 3424) uses `String.prototype.replace()` without the global flag. This means only the first occurrence of `",,,"`  in the CSV is removed. If the first data row (which has fewer columns) generates a trailing `",,,"`  that is removed, but subsequent rows with the same issue are not cleaned, the output CSV will be malformed. This is a logic bug that can produce incorrect data being sent to Maximo and to DP World recipients. This is a data-integrity rather than security finding, but malformed data in a Maximo import can cause incorrect meter readings to be applied to physical assets.
**Location:** index.js:3217, index.js:3424
**Checklist item:** 4. Runtime Security (data integrity / logic error)

---

## SUMMARY TABLE

| ID | Severity | Title |
|----|----------|-------|
| A02-1 | LOW | Hardcoded S3 bucket name |
| A02-2 | MEDIUM | Hardcoded recipient email list with silent BCC to consultants |
| A02-3 | HIGH | No sender verification — any sender can trigger processing |
| A02-4 | HIGH | No attachment content-type validation |
| A02-5 | HIGH | No attachment size limit / zip-bomb protection |
| A02-6 | HIGH | No row/column count limit on XLSX input |
| A02-7 | MEDIUM | No formula injection sanitization on output CSV cells |
| A02-8 | LOW | S3 key sanitization — no issue (timestamp-based keys) |
| A02-9 | MEDIUM | dateFormatChange has no input validation; errors not caught |
| A02-10 | INFO | No eval/child_process usage — no issue |
| A02-11 | INFO | Runtime version not determinable from this file |
| A02-12 | MEDIUM | Entire handler has no try/catch — all errors are unhandled rejections |
| A02-13 | MEDIUM | AWS SDK v2 used — maintenance-only since Sept 2023 |
| A02-14 | LOW | Large in-memory allocations; no /tmp usage (clean) |
| A02-15 | INFO | S3 bucket ACL not determinable from this file |
| A02-16 | MEDIUM | No guard on attachments[0] — crashes if email has no attachment |
| A02-17 | LOW | Misleading console.log and dead code throughout |
| A02-18 | LOW | csv.replace(",,,","") non-global — only removes first occurrence |
