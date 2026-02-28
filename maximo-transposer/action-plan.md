# Action Plan — maximo-transposer
**Branch:** master
**Audit date:** 2026-02-27
**Run:** 01

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 9     |
| HIGH     | 30    |
| MEDIUM   | 47    |
| LOW      | 31    |
| INFO     | 12    |

## Pass 1 — Security

# Pass 1 Audit — A01, A03, A05, A06 Configuration Files
**Repo:** maximo-transposer
**Branch:** master (verified)
**Date:** 2026-02-27
**Auditor:** Security Audit Agent (A01/A03/A05/A06)
**Checklist:** PASS1-CHECKLIST-maximo-transposer.md

---

## Pre-flight

Branch confirmed as `master` via `git branch --show-current`.

---

## Reading Evidence

### A01 — `.gitignore`

**File path:** `/Projects/cig-audit/repos/maximo-transposer/.gitignore`
**Total lines:** 2 (plus trailing blank)

Patterns listed, verbatim:
1. `node_modules`
2. `__MACOSX/`

No other patterns present.

---

### A03 — `package-lock.json`

**File path:** `/Projects/cig-audit/repos/maximo-transposer/package-lock.json`
**Total lines:** 1035

**Top-level metadata:**
- `name`: `maximo-transposer`
- `version`: `1.0.0`
- `lockfileVersion`: `2`
- `requires`: `true`

**Direct dependencies declared in the root package entry (under `packages[""].dependencies`):**

| Package | Declared Range | Resolved Version |
|---|---|---|
| `aws-cli` | `^0.0.2` | `0.0.2` |
| `aws-sdk` | `^2.901.0` | `2.901.0` |
| `json-2-csv` | `^3.11.0` | `3.11.0` |
| `mailparser` | `^3.2.0` | `3.2.0` |
| `nodemailer` | `^6.6.0` | `6.6.0` |
| `xlsx` | `^0.16.9` | `0.16.9` |

**devDependencies:** none declared.

**Notable transitive dependency observations:**
- `aws-cli` pulls in a pinned ancient `aws-sdk@2.0.31` as a nested dependency (under `node_modules/aws-cli/node_modules/aws-sdk`).
- `uuid@3.3.2` is a transitive dependency of `aws-sdk@2.901.0`; the npm registry marks this version as deprecated (may use `Math.random()` for UUID generation in some circumstances).
- `querystring@0.2.0` is marked deprecated in the npm registry (Legacy API; use URLSearchParams instead).
- `minimist@1.2.5` is resolved as a transitive dependency of `html-to-text` (itself a transitive dependency of `mailparser`).
- `node_modules` is not committed to the repository (confirmed by directory listing).

---

### A05 — `sample.json`

**File path:** `/Projects/cig-audit/repos/maximo-transposer/sample.json`
**Total lines:** 51

**Top-level keys and value types:**

| Key | Type |
|---|---|
| `thing` | object |

**`thing` sub-keys and value types:**

| Key | Type | Notes |
|---|---|---|
| `vehicle` | object | Contains `serialno`, `product_type`, `product_code`, `product_class`, `name`, `model`, `make`, `hour_meter_offset`, `hardwareid`, `hardware_type`, `entered_fleet`, `description`, `dealer_id`, `date_into_service` |
| `usage` | object | Contains numeric usage metrics: `this_week`, `this_month`, `average_weekly_usage_input_one`, `average_weekly_usage`, `average_daily_usage_input_one`, `average_daily_usage` |
| `rentals` | array | Empty array `[]` |
| `organisation` | object | Contains `service_location`, `management_region`, `management_location` — all null |
| `maintenance` | object | Contains `services` (empty array), `service_type`, `service_offset`, `service_interval` (500), `service_calculation_input` ("0"), `next_service_type`, `impacts` (0) |
| `fleets` | array | One object: `{ "type": 0, "name": "Startup", "id": 1 }` |
| `customer` | string | Empty string `""` |
| `contract` | object | Contains `contract_type`, `contract_postcode`, `contract_name`, `contract_geofence` — all null |

**Notable `vehicle` field values (non-null):**
- `serialno`: `"IR1872"` (string — appears to be a real asset serial number)
- `name`: `"QC001 - WST"` (string — appears to be a real asset/fleet name)
- `hour_meter_offset`: `46106.0` (number)
- `hardwareid`: `"4661425649"` (string — appears to be a real hardware/device ID)
- `hardware_type`: `4` (number)
- `dealer_id`: `0` (number)

---

### A06 — `serverless.yml`

**File path:** `/Projects/cig-audit/repos/maximo-transposer/serverless.yml`
**Total lines:** 24

**Service name:** `maximo-transposer`

**Plugins:**
- `serverless-plugin-include-dependencies`

**Custom variables:**
- `bucket`: `maximo-transposer-bucket` (hardcoded string, not a reference to SSM or environment variable)

**Provider configuration:**
- `name`: `aws`
- `runtime`: `nodejs14.x`
- `region`: `us-east-1`

**IAM Role Statements:**

| Effect | Action | Resource |
|---|---|---|
| `Allow` | `s3:GetObject` | `arn:aws:s3:::maximo-transposer-bucket/*` |

**Functions defined:**

| Function name | Handler | Events |
|---|---|---|
| `email_handler` | `index.handler` | None defined in serverless.yml |

**Environment variables (function-level):**
- `BUCKET`: `${self:custom.bucket}` → resolves to `maximo-transposer-bucket`

**Timeout setting:** Not configured (no `timeout:` key present — AWS default of 3 seconds applies).

**Memory setting:** Not configured (no `memorySize:` key present — AWS default of 128 MB applies).

**SES trigger:** No `events:` block defined for `email_handler` in this file.

**No hardcoded AWS credentials, AKIA keys, secret access keys, or passwords found in serverless.yml.**

---

## Checklist Review

### Section 1: Secrets and Configuration

**Checklist item — .env files in .gitignore:**

The `.gitignore` file does NOT include `.env` or `.env.*` patterns. Only `node_modules` and `__MACOSX/` are excluded. If a developer creates a `.env` file, it would not be blocked from being committed.

**Finding: A01-1**

**Checklist item — hardcoded credentials in serverless.yml:**

No AWS access keys (`AKIA...`), secret access keys, SES SMTP passwords, or Maximo API credentials were found hardcoded in `serverless.yml`. The bucket name `maximo-transposer-bucket` is hardcoded as a custom variable rather than referencing SSM Parameter Store, but this is a configuration value rather than a credential. The `BUCKET` environment variable references the custom variable, not SSM.

**Finding: A06-1** (bucket name hardcoded — not a credential, but infrastructure detail exposed in source)

**Checklist item — Lambda environment variables referencing SSM/Secrets Manager:**

The sole environment variable `BUCKET` holds the S3 bucket name via a static custom variable. No secrets are in environment variables in this file. However, the application uses SES and S3 — any SES credentials or other runtime secrets would need to be checked in source (covered by other auditors). No SSM references present.

**Checklist item — package.json scripts with embedded credentials:**
Not directly in scope of assigned files. package-lock.json contains no script entries.

**Bitbucket Pipelines:**

`bitbucket-pipelines.yml` is **absent** from the repository. No CI/CD pipeline configuration file exists. This is itself a finding — there is no automated pipeline, which means deployments are presumably manual with no enforced credential-scanning or pipeline-level security controls.

**Finding: A06-2**

---

### Section 2: IAM and AWS Permissions

**Checklist item — iamRoleStatements least privilege analysis:**

The single IAM statement grants `s3:GetObject` on `arn:aws:s3:::maximo-transposer-bucket/*`.

Analysis:
- The action `s3:GetObject` is scoped correctly to read — it is a narrow permission.
- The resource is scoped to the specific named bucket with a wildcard on object keys (`/*`), which is acceptable for bucket-wide access.
- **However**, the function `email_handler` is described as an email intake handler that processes attachments and (based on the `nodemailer` dependency) sends email replies. The expected data flow is: SES → S3 (write inbound email) → Lambda reads from S3 → Lambda processes → Lambda writes output to S3 → Lambda sends via SES. The IAM policy grants **only** `s3:GetObject`. There is **no** `s3:PutObject` permission and **no** `ses:SendEmail` permission. This means either: (a) the Lambda cannot actually write output to S3 or send email at runtime — which would cause silent runtime failures — or (b) the Lambda relies on permissions granted by another mechanism not captured here (e.g., inline policy, managed policy attached outside Serverless Framework).
- **No** `"Action": "*"` or `"Resource": "*"` is present.
- **No** IAM permission grants exist for `iam:*`, so privilege escalation via IAM APIs is not possible from this configuration.

**Finding: A06-3** (missing s3:PutObject and ses:SendEmail — functional gap / least-privilege misconfiguration)

---

### Section 4: Runtime Security

**Checklist item — Node.js runtime version:**

`serverless.yml` line 11 declares `runtime: nodejs14.x`. Node.js 14 reached End of Life on **30 April 2023**. AWS Lambda also retired the `nodejs14.x` managed runtime — it is no longer receiving security updates. This is a critical finding.

**Finding: A06-4**

**Checklist item — eval(), new Function(), child_process:**
Not directly assessable from the four assigned files. These are source-code findings covered by other auditors.

---

### Section 5: Dependencies

**Checklist item — known vulnerabilities / outdated packages:**

Key observations from `package-lock.json`:

1. **`xlsx@0.16.9`**: This is a significantly outdated version of the SheetJS `xlsx` library. The SheetJS project (SheetJS CE / `xlsx` on npm) has had multiple security advisories. Version `0.16.9` is from approximately early 2021. The project later migrated to a CDN-only distribution model and the npm package was abandoned/deprecated. Known concerns with this version include prototype pollution and formula injection risks. This version should be treated as unmaintained.

2. **`aws-cli@0.0.2`**: Marked deprecated in the npm registry with the message "Recommend using the official aws cli tools for python". This package pulls in `aws-sdk@2.0.31` (from 2014) as a nested dependency — an extremely old SDK version with no security maintenance. The `aws-cli` npm package serves no purpose in a Lambda function and should not be a production dependency.

3. **`uuid@3.3.2`**: The npm registry marks this as deprecated: "Please upgrade to version 7 or higher. Older versions may use Math.random() in certain circumstances, which is known to be problematic." This is a transitive dependency of `aws-sdk@2.901.0`.

4. **`minimist@1.2.5`**: This version of minimist has a known prototype pollution vulnerability (CVE-2021-44906 affects versions before 1.2.6). It is a transitive dependency via `html-to-text` → `mailparser`.

5. **`aws-sdk@2.901.0`**: AWS SDK v2 is in maintenance mode as of 2023; AWS SDK v3 is the current supported version. Continued use of v2 is not a security vulnerability per se, but it is approaching end of active support.

6. **`node_modules` not committed**: Confirmed — directory listing shows no `node_modules` directory in the repository root. This checklist item passes.

**Finding: A03-1** (xlsx@0.16.9 — abandoned/unmaintained, formula injection risk)
**Finding: A03-2** (aws-cli@0.0.2 — deprecated package with ancient nested aws-sdk@2.0.31)
**Finding: A03-3** (minimist@1.2.5 — prototype pollution CVE-2021-44906)

---

### Section 6: Lambda and AWS Configuration

**Checklist item — timeout:**

No `timeout:` is set in `serverless.yml` at provider or function level. AWS Lambda defaults to **3 seconds**. For a function that processes email attachments (potentially multi-megabyte XLSX files) from S3, parses them, transforms data, and sends reply emails via SES/nodemailer, 3 seconds is likely insufficient. This will cause silent failures where Lambda times out mid-processing without a clear error to the caller.

**Finding: A06-5** (no timeout configured — 3-second default is insufficient for email/XLSX processing)

**Checklist item — memory:**

No `memorySize:` is set. AWS Lambda defaults to **128 MB**. For XLSX processing (potentially large spreadsheets), 128 MB may be insufficient and cause out-of-memory crashes. Lambda memory also controls CPU allocation.

**Finding: A06-6** (no memory configured — 128 MB default may be insufficient for XLSX processing)

**Checklist item — SES trigger configuration:**

No `events:` block is defined under `email_handler` in `serverless.yml`. This means the SES trigger is either: (a) configured outside Serverless Framework (e.g., manually in the AWS console or via a separate CloudFormation/CDK stack), or (b) missing entirely. The absence of an events block in serverless.yml means the trigger constraints (sender allow-listing, S3 bucket restrictions) cannot be audited from this file.

**Finding: A06-7** (SES event trigger absent from serverless.yml — trigger configuration cannot be audited; risk of open trigger accepting email from any sender)

**Checklist item — S3 bucket access controls:**

The bucket name `maximo-transposer-bucket` is referenced but no S3 bucket resource definition is present in `serverless.yml` (no `resources:` section). This means the bucket was either created manually or in a separate stack. Public access block settings, bucket ACLs, and versioning/lifecycle policies cannot be verified from this file.

**Finding: A06-8** (S3 bucket not defined in serverless.yml — cannot verify public access block, ACLs, versioning, or lifecycle policies from IaC)

**Checklist item — S3 versioning and lifecycle policies:**

Cannot be assessed from `serverless.yml` — no `resources:` section defines the bucket. See A06-8.

**Checklist item — /tmp cleanup:**

Not assessable from these four files — source-code concern for other auditors.

---

### Section 5 (additional) — sample.json data exposure

**Checklist item — sensitive data in sample/test files:**

`sample.json` contains what appear to be real operational data values:
- `serialno: "IR1872"` — likely a real vehicle serial number
- `name: "QC001 - WST"` — likely a real fleet asset name
- `hardwareid: "4661425649"` — likely a real IoT/telematics device hardware ID

While not credentials, committing real asset identifiers to a public or semi-public repository exposes fleet asset metadata. If the repository were public or the data is from a live customer system, this would constitute a data handling concern.

**Finding: A05-1** (sample.json contains what appear to be real asset identifiers — serialno, hardwareid, name)

---

## Summary of Findings

### A01 — .gitignore

**[P1-A01-1]** *(HIGH)*
**Description:** The `.gitignore` does not exclude `.env` or `.env.*` files. If a developer creates a `.env` file containing AWS credentials, SES passwords, or Maximo API keys (a common practice during local development), that file will not be blocked from being committed to the repository. This is a systemic risk — the absence of this pattern provides no protection against accidental credential commits.
**Location:** `.gitignore` (entire file — pattern absent)
**Checklist item:** Section 1 — Secrets and Configuration: "Verify `.env` and `.env.*` are in `.gitignore`."

---

### A03 — package-lock.json

**[P1-A03-1]** *(HIGH)*
**Description:** `xlsx@0.16.9` is a severely outdated and effectively abandoned version of the SheetJS library (circa early 2021). The npm package has since been deprecated by its maintainer. This version has known formula injection risks and no ongoing security maintenance. Any CVEs disclosed after the abandonment will never be patched in this version. The application uses this library to process untrusted email attachments, making this a high-severity concern.
**Location:** `package-lock.json` line 562-584 (`node_modules/xlsx`), line 1003-1019 (legacy `dependencies` block)
**Checklist item:** Section 5 — Dependencies: "Check for outdated packages with available security patches. Focus on: the XLSX/ExcelJS library (formula injection CVEs exist in some versions)."

**[P1-A03-2]** *(MEDIUM)*
**Description:** `aws-cli@0.0.2` is a deprecated npm package (registry message: "Recommend using the official aws cli tools for python"). It is a runtime dependency (`dependencies`, not `devDependencies`), meaning it is bundled into the Lambda deployment package. It pulls in a nested `aws-sdk@2.0.31` (from approximately 2014) which receives no security updates. The aws-cli npm package is unnecessary for a Lambda function and adds attack surface and package size for no benefit.
**Location:** `package-lock.json` line 36-48 (`node_modules/aws-cli`), line 613-649 (legacy block)
**Checklist item:** Section 5 — Dependencies: "Check for outdated packages with available security patches."

**[P1-A03-3]** *(MEDIUM)*
**Description:** `minimist@1.2.5` is resolved as a transitive dependency (`mailparser` → `html-to-text` → `minimist`). CVE-2021-44906 (prototype pollution) affects minimist versions before 1.2.6. An attacker who can influence the parsed arguments could pollute the Object prototype. Version 1.2.6 or later fixes this vulnerability.
**Location:** `package-lock.json` line 448-452 (`node_modules/minimist`), line 921-924 (legacy block)
**Checklist item:** Section 5 — Dependencies: "Check `package-lock.json` for known vulnerabilities."

---

### A05 — sample.json

**[P1-A05-1]** *(LOW)*
**Description:** `sample.json` contains values that appear to be real operational data: a vehicle serial number (`"IR1872"`), a fleet asset name (`"QC001 - WST"`), and a hardware device identifier (`"4661425649"`). Committing real customer or operational asset identifiers to source control — even a private repository — is contrary to data minimisation principles. If the repository is or becomes accessible to third parties (e.g., during an audit, open-sourcing, or a repository exposure incident), this data is exposed. The file should use clearly fictional/placeholder values.
**Location:** `sample.json` lines 4 (`serialno`), 8 (`name`), 10 (`hardwareid`)
**Checklist item:** Section 1 — Secrets and Configuration (general principle of not committing real data to repositories).

---

### A06 — serverless.yml

**[P1-A06-1]** *(LOW)*
**Description:** The S3 bucket name `maximo-transposer-bucket` is hardcoded as a custom variable in `serverless.yml` and exposed in source control. While not a credential, bucket names are a form of infrastructure enumeration data. Best practice is to parameterise bucket names via SSM Parameter Store or Serverless Framework parameters, particularly when the repository may be accessible to parties outside the team.
**Location:** `serverless.yml` line 7 (`custom.bucket`)
**Checklist item:** Section 1 — Secrets and Configuration: "Check `serverless.yml` for hardcoded credentials, API keys, SES credentials, S3 bucket names, or AWS account IDs."

**[P1-A06-2]** *(MEDIUM)*
**Description:** `bitbucket-pipelines.yml` is absent from the repository. There is no CI/CD pipeline configuration. Deployments are presumably performed manually from a developer machine using `serverless deploy`. This means: (a) there is no automated security scanning gate before deployment; (b) deployment credentials are stored on individual developer machines rather than in a secrets-managed pipeline environment; (c) there is no audit trail of who triggered deployments and with what code state. The absence of a pipeline is itself a security control gap.
**Location:** Repository root — file not present
**Checklist item:** Section 1 — Bitbucket Pipelines: "Check `bitbucket-pipelines.yml` for hardcoded AWS credentials..." — note: file is absent, which is itself a finding.

**[P1-A06-3]** *(HIGH)*
**Description:** The IAM role defined in `serverless.yml` grants only `s3:GetObject`. The `email_handler` function uses `nodemailer` (SES sending) and `mailparser` (email processing), and the standard flow for an SES-triggered Lambda writes output back to S3 and sends reply emails. The missing permissions are `s3:PutObject` (to write processed output) and `ses:SendEmail` / `ses:SendRawEmail` (to send replies). One of two conditions must hold: (1) the Lambda fails silently at runtime when attempting write operations or SES sends — a functional defect with security implications (undetected failure); or (2) additional permissions are granted outside this file (e.g., a manually attached managed policy or overly-broad `AdministratorAccess` policy), which would be an unauditable over-privilege condition. Either outcome is a security concern.
**Location:** `serverless.yml` lines 13-17 (`provider.iamRoleStatements`)
**Checklist item:** Section 2 — IAM and AWS Permissions: "Verify the function only has permissions for the specific actions it performs: `s3:GetObject`, `s3:PutObject`, `ses:SendEmail`."

**[P1-A06-4]** *(CRITICAL)*
**Description:** The Lambda runtime is `nodejs14.x`. Node.js 14 reached End of Life on 30 April 2023 and AWS Lambda retired the `nodejs14.x` managed runtime (it no longer receives AWS security patches or Node.js upstream patches). Running on an EOL runtime means all security vulnerabilities discovered in Node.js 14 after its EOL date are permanently unpatched in this deployment. The current supported LTS runtime is Node.js 20 (or 22). This must be updated immediately.
**Location:** `serverless.yml` line 11 (`provider.runtime: nodejs14.x`)
**Checklist item:** Section 4 — Runtime Security: "Check the Node.js runtime version in `serverless.yml`. Verify it is not end-of-life (Node.js 14 and 16 are EOL). Use Node.js 20 or later."

**[P1-A06-5]** *(MEDIUM)*
**Description:** No `timeout:` is configured at provider or function level. The AWS Lambda default timeout is 3 seconds. The `email_handler` function processes email attachments, parses XLSX files, transforms data, and sends reply emails via SES — operations that can easily take 10–60 seconds depending on attachment size and network latency to SES. With a 3-second timeout, legitimate large emails will cause silent Lambda timeouts. In Lambda, a timeout results in a failed invocation but SES may still have accepted the email — leaving the email unprocessed with no visible error to the sender (the sender receives no bounce). This is both a reliability and a security concern (denial of service via large attachments becomes trivially easy).
**Location:** `serverless.yml` — `timeout:` key absent at provider level (line 9-17) and function level (line 19-23)
**Checklist item:** Section 6 — Lambda and AWS Configuration: "Verify the Lambda function has an appropriate timeout configured."

**[P1-A06-6]** *(MEDIUM)*
**Description:** No `memorySize:` is configured at provider or function level. The AWS Lambda default memory is 128 MB. XLSX parsing of large spreadsheets, email MIME parsing via `mailparser`, and CSV generation via `json-2-csv` are all memory-intensive operations. Processing a multi-sheet XLSX with tens of thousands of rows at 128 MB is likely to cause out-of-memory Lambda crashes (exit code 137). Lambda memory also determines CPU allocation — low memory means slower processing and higher timeout risk. Recommended minimum for file-processing workloads is 512 MB; 1024 MB is common.
**Location:** `serverless.yml` — `memorySize:` key absent at provider level (line 9-17) and function level (line 19-23)
**Checklist item:** Section 6 — Lambda and AWS Configuration: "Check memory configuration."

**[P1-A06-7]** *(HIGH)*
**Description:** No `events:` block is defined for `email_handler` in `serverless.yml`. This means the SES receipt rule that triggers this Lambda is configured outside of Infrastructure-as-Code (manually or via another stack). The security consequence is that: (a) the trigger configuration — specifically any sender allow-listing, recipient filtering, or S3 action ordering — cannot be reviewed or enforced through code review or deployment pipelines; (b) there is no guarantee that the SES receipt rule restricts which senders can trigger the Lambda (the checklist item requires verifying the SES trigger "only accepts email from expected sources or domains, not from anyone"); (c) the trigger configuration may drift from the intended state with no IaC to enforce it. This is a high finding because an unrestricted SES trigger allows anyone on the internet to invoke this Lambda by sending an email to the configured address.
**Location:** `serverless.yml` lines 19-23 — no `events:` key under `email_handler`
**Checklist item:** Section 6 — Lambda and AWS Configuration: "Verify the SES trigger is configured to only accept email from expected sources or domains, not from anyone."

**[P1-A06-8]** *(MEDIUM)*
**Description:** The `serverless.yml` contains no `resources:` section. The S3 bucket `maximo-transposer-bucket` is referenced but not defined in IaC. This means the bucket's access controls (public access block, ACL, bucket policy), versioning, lifecycle policies, and encryption configuration cannot be verified from the IaC source. The bucket may have been created manually with incorrect settings (e.g., missing public access block, no encryption at rest, no versioning for Maximo data retention). Without IaC definition, there is no enforcement mechanism to prevent misconfiguration.
**Location:** `serverless.yml` — `resources:` section absent
**Checklist item:** Section 6 — Lambda and AWS Configuration: "Check whether the S3 bucket receiving output files has appropriate access controls — it must not be publicly readable. Check for S3 bucket versioning and lifecycle policies."

---

## Checklist Items With No Issues Found

- **Section 1 — No AWS access keys in serverless.yml:** No `AKIA...` patterns, secret access keys, SES SMTP passwords, or Maximo API credentials are present in `serverless.yml`. No issues found.
- **Section 1 — No credentials in package-lock.json:** `package-lock.json` contains only package metadata, resolved versions, and integrity hashes. No credentials present. No issues found.
- **Section 2 — No `Action: "*"` or `Resource: "*"` in iamRoleStatements:** The single IAM statement uses a specific action (`s3:GetObject`) and a scoped resource ARN. No wildcard actions or resources present. No issues found.
- **Section 2 — No IAM permissions for IAM APIs:** The Lambda role cannot modify its own execution role or call IAM APIs. No privilege escalation path via IAM present. No issues found.
- **Section 5 — node_modules not committed:** The `node_modules` directory is excluded by `.gitignore` and is not present in the repository. No issues found.
- **Section 5 — No packages installed globally in pipeline:** No `bitbucket-pipelines.yml` exists; no global package installation commands are present in any of the four audited files. No issues found from these files.

---

## Finding Index

| ID | Severity | File | Description |
|---|---|---|---|
| A01-1 | HIGH | `.gitignore` | `.env` and `.env.*` patterns absent — accidental credential commits not blocked |
| A03-1 | HIGH | `package-lock.json` | `xlsx@0.16.9` — abandoned/unmaintained, formula injection risk, no security patches |
| A03-2 | MEDIUM | `package-lock.json` | `aws-cli@0.0.2` — deprecated package with ancient `aws-sdk@2.0.31` as nested dependency |
| A03-3 | MEDIUM | `package-lock.json` | `minimist@1.2.5` — prototype pollution CVE-2021-44906 (fix: upgrade to >=1.2.6) |
| A05-1 | LOW | `sample.json` | Real operational asset identifiers committed to source (serialno, hardwareid, name) |
| A06-1 | LOW | `serverless.yml` | S3 bucket name hardcoded in source rather than parameterised via SSM |
| A06-2 | MEDIUM | (absent) | `bitbucket-pipelines.yml` absent — no CI/CD pipeline, no automated security gates |
| A06-3 | HIGH | `serverless.yml` | IAM role missing `s3:PutObject` and `ses:SendEmail` — functional gap or unauditable over-privilege |
| A06-4 | CRITICAL | `serverless.yml` | Runtime `nodejs14.x` is End of Life — permanently unpatched security vulnerabilities |
| A06-5 | MEDIUM | `serverless.yml` | No timeout configured — 3-second default will cause silent failures on real workloads |
| A06-6 | MEDIUM | `serverless.yml` | No memory configured — 128 MB default likely insufficient for XLSX/email processing |
| A06-7 | HIGH | `serverless.yml` | SES trigger absent from IaC — cannot verify sender restrictions; open trigger risk |
| A06-8 | MEDIUM | `serverless.yml` | S3 bucket not defined in IaC — cannot verify access controls, encryption, versioning |
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

**[P1-A02-1]** *(LOW)*
**Description:** The S3 bucket name `"maximo-transposer-bucket"` is hardcoded directly in the source at three locations (lines 3122, 3224, 3431). If the bucket is renamed, the code must be changed. More significantly, hardcoding infrastructure names in source rather than in Lambda environment variables means the value cannot be changed between deployments (dev/staging/prod) without a code change, and it appears in version control history permanently. There are no secrets here, but the pattern is contrary to 12-factor and the serverless best practice of externalizing all configuration.
**Location:** index.js:3122, index.js:3224, index.js:3431
**Checklist item:** 1. Secrets and Configuration

**[P1-A02-2]** *(MEDIUM)*
**Description:** Recipient email addresses — including DP World staff addresses and internal BCC addresses — are hardcoded in the Lambda source code at lines 3461–3462. These are operational configuration values that will change over time (staff changes, domain changes). Hardcoding them in source means changes require a code deployment rather than a configuration update, and the full recipient list is permanently recorded in version control history. Additionally, the BCC list at line 3462 includes `rhythmduwadi@collectiveintelligence.com.au` and `sidney@collectiveintelligence.com.au`, meaning internal consultants silently receive every processed report. This is a data-governance concern: DP World's equipment meter data is being silently forwarded to third-party consultants on every invocation, which may not be disclosed to the client.
**Location:** index.js:3461–3462
**Checklist item:** 1. Secrets and Configuration

---

### 2. IAM and AWS Permissions

IAM role statements are defined in `serverless.yml`, which is outside the scope of this file. No IAM-related code (e.g., `sts:AssumeRole`, `iam:` API calls) appears in `index.js`.

Checklist item 2. IAM and AWS Permissions: no issues found in this file. (IAM configuration reviewed separately via serverless.yml.)

---

### 3. Input Validation

**[P1-A02-3]** *(HIGH)*
**Description:** No sender verification is performed. The Lambda processes any email that arrives, regardless of who sent it. At line 3131 the sender address is parsed into `from` but the variable is never used for any validation or allowlist check. Any actor who can send email to the SES-monitored address can trigger the full processing pipeline, including S3 writes and email dispatch to DP World and other recipients. A malicious sender could deliberately craft a payload to trigger downstream errors, exhaust Lambda execution time, or cause spam to be sent from the verified SES identity to all recipients.
**Location:** index.js:3131
**Checklist item:** 3. Input Validation — Sender verification

**[P1-A02-4]** *(HIGH)*
**Description:** No content-type validation is performed on the email attachment before it is passed to `XLSX.read()`. At line 3134 the code unconditionally reads `attachments[0].content` into the XLSX parser regardless of the attachment MIME type. Any file type (PDF, executable, ZIP, script) will be fed to the XLSX parser. This may trigger parser vulnerabilities or unexpected behavior for non-XLSX content. The checklist requires verification that only `.xlsx` / `.xls` types are processed.
**Location:** index.js:3134
**Checklist item:** 3. Input Validation — Attachment validation

**[P1-A02-5]** *(HIGH)*
**Description:** No attachment size limit is enforced before calling `XLSX.read()`. The entire attachment content is loaded into memory at once (line 3134). A large attachment sent by any email sender (there is no sender allowlist — see A02-3) will expand in Lambda memory during XLSX parsing. This is a denial-of-service and Lambda-timeout vector. The XLSX library performs in-memory decompression of the ZIP structure inside an XLSX file; a crafted ZIP bomb (small compressed size, enormous decompressed size) will exhaust Lambda memory.
**Location:** index.js:3134
**Checklist item:** 3. Input Validation — Attachment size limits; XLSX processing — zip bomb protection

**[P1-A02-6]** *(HIGH)*
**Description:** No row or column count limit is enforced on the parsed XLSX sheet. At line 3176 and again at line 3274, the code iterates `for (var i = 0; i < sheetJSON.length; i++)` with no upper bound on `sheetJSON.length`. An attacker who can send a crafted XLSX file with hundreds of thousands of rows can drive the Lambda to timeout, accumulate very large `result` and `result_2` arrays in memory, and cause out-of-memory termination.
**Location:** index.js:3176, index.js:3274
**Checklist item:** 3. Input Validation — XLSX processing — maximum rows/columns

**[P1-A02-7]** *(MEDIUM)*
**Description:** Cell values from the XLSX attachment are written directly into the output CSV rows without checking for formula injection characters. At lines 3191 and 3397, `sheetJSON[i][original_column_name]` (a numeric meter reading from the input sheet) is placed into the output without sanitization. At lines 3192 and 3377/3387/3397, `dateFormatChange(sheetJSON[i]["Last reported date"])` is placed into the output. If a cell in the input sheet contains a value starting with `=`, `+`, `-`, or `@`, it will survive into the output CSV and may execute as a formula when the recipient opens the file in Excel. The `dateFormatChange` function at line 3146 does basic string splitting but does not validate that the input actually conforms to the expected date format, so an injected formula could survive. The output is emailed to DP World staff who will open the CSV in Excel or a compatible application.
**Location:** index.js:3191, index.js:3192, index.js:3377, index.js:3387, index.js:3397
**Checklist item:** 3. Input Validation — XLSX processing — formula injection

**[P1-A02-8]** *(LOW)*
**Description:** The S3 key for the stored output files is constructed from `Math.floor(Date.now() / 1000).toString()` (a Unix timestamp) at lines 3221 and 3428. This is derived from the Lambda's own clock, not from user-controlled data, so there is no path-traversal risk from email metadata in the S3 key construction. However, the input email is retrieved from S3 using the raw `sesNotification.mail.messageId` at line 3123 as the S3 key. The message ID originates from SES, which is under AWS control and not user-supplied in the usual sense. SES message IDs follow a fixed UUID-style format and are not user-controllable. No path traversal risk is present in this specific usage. This item is noted as clear.

Checklist item 3. Input Validation — S3 key sanitization: no issues found (S3 output keys are timestamp-based; input key is SES-generated message ID).

---

### 4. Runtime Security

**[P1-A02-9]** *(MEDIUM)*
**Description:** The `dateFormatChange` function at lines 3146–3159 performs no input validation on the date string before calling `.split()` and constructing a formatted string. If the "Last reported date" cell is missing, empty, or not a string, calling `.split(" ")` on a non-string or undefined value will throw a TypeError. This error is not caught anywhere in the handler. Because the entire handler is a single `async` function with no try/catch block, any such exception will propagate as an unhandled Promise rejection from the Lambda handler. In the Node.js Lambda runtime, an unhandled rejection causes the invocation to fail, but the failure mode is not always obvious. More critically, the error message and stack trace (including internal file paths) may be surfaced in CloudWatch logs without sanitization, and depending on SES bounce configuration, error details could be returned to the email sender.
**Location:** index.js:3146–3159, index.js:9 (no try/catch in handler)
**Checklist item:** 4. Runtime Security — unhandled Promise rejections; error handling

**[P1-A02-10]** *(INFO)*
**Description:** No `eval()`, `new Function()`, or `child_process` usage appears anywhere in `index.js`. The XLSX library is used for parsing but no dynamic code execution is performed with user-controlled data.

Checklist item 4. Runtime Security — eval/child_process: no issues found.

**[P1-A02-11]** *(INFO)*
**Description:** The Node.js runtime version cannot be determined from `index.js` itself — it is declared in `serverless.yml`. This item is noted here for completeness and is covered by the serverless.yml audit agent.

Checklist item 4. Runtime Security — Node.js runtime version: not applicable to this file.

**[P1-A02-12]** *(MEDIUM)*
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

**[P1-A02-13]** *(MEDIUM)*
**Description:** The code uses AWS SDK v2 (`require("aws-sdk")`), which was placed into maintenance-only mode in September 2023. AWS SDK v2 no longer receives feature updates and may not receive security patches. AWS SDK v3 is the supported replacement.
**Location:** index.js:2
**Checklist item:** 5. Dependencies — outdated packages

Checklist item 5. Dependencies — node_modules committed to repo: not assessable from index.js; covered by repo-level review.

---

### 6. Lambda and AWS Configuration

Lambda timeout, memory, SES trigger configuration, and S3 bucket ACL settings are defined in `serverless.yml` and are outside the scope of `index.js`. Observations from this file relevant to Lambda configuration:

**[P1-A02-14]** *(LOW)*
**Description:** The Lambda does not write any files to `/tmp` and therefore has no `/tmp` cleanup obligation. However, the code holds the entire email body as a string (`var email = data.Body.toString()` at line 3128), the full parsed XLSX workbook in memory (line 3134–3137), and two full `result` / `result_2` arrays before serializing to CSV. All of this resides in Lambda heap memory. If the execution environment is reused (warm Lambda), these large in-memory allocations are garbage-collected by Node.js between invocations, but there is no explicit release. This is not a direct security vulnerability but is a resource-management concern that could become relevant if memory limits are tight.
**Location:** index.js:3128, 3134, 3161, 3259
**Checklist item:** 6. Lambda and AWS Configuration — /tmp cleanup; memory

**[P1-A02-15]** *(INFO)*
**Description:** The S3 bucket name `"maximo-transposer-bucket"` is used for both input (reading the raw SES email) and output (writing the formatted CSV files). Whether this bucket is publicly accessible cannot be determined from `index.js`; it depends on the S3 bucket policy and ACL configured outside this file.

Checklist item 6. Lambda and AWS Configuration — S3 bucket access controls: not determinable from index.js alone.

Checklist item 6. Lambda and AWS Configuration — Lambda timeout and memory configuration: not present in index.js; covered by serverless.yml audit.

Checklist item 6. Lambda and AWS Configuration — SES trigger configuration: not present in index.js; covered by serverless.yml audit.

---

## ADDITIONAL FINDINGS (outside direct checklist items but material)

**[P1-A02-16]** *(MEDIUM)*
**Description:** At line 3134, the code accesses `attachments[0]` without checking that `attachments` is non-empty or that the array index exists. If an email arrives with no attachments (e.g., a test email, a spam trigger, or a malformed inbound message), `attachments[0]` will be `undefined`, and `.content` access will throw `TypeError: Cannot read properties of undefined`. This is not caught and will cause an unhandled rejection (see also A02-12).
**Location:** index.js:3134
**Checklist item:** 3. Input Validation — Attachment validation; 4. Runtime Security — unhandled Promise rejections

**[P1-A02-17]** *(LOW)*
**Description:** There is dead / commented-out code throughout the file. The test email block at lines 11–25 is fully commented out but `console.log("Test email sent.")` at line 26 remains active and executes unconditionally on every invocation, even though no test email is sent. The first send-email block (lines 3233–3249) is commented out. The second test send-email block (lines 3446–3457) is commented out. The active send at lines 3459–3473 dispatches to a large production recipient list. This inconsistent state (dead code, misleading log output, production send embedded in a section labelled "TEST") suggests the code has not been properly cleaned up, making auditing harder and increasing the risk that future changes may accidentally re-enable commented code.
**Location:** index.js:26, 3233–3249, 3446–3457, 3459–3473
**Checklist item:** 4. Runtime Security — error handling (misleading log output)

**[P1-A02-18]** *(LOW)*
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
# A04 — package.json Security Audit

**Auditor:** A04
**Date:** 2026-02-27
**Branch:** master
**File:** `package.json`
**Checklist:** PASS1-CHECKLIST-maximo-transposer.md

---

## Pre-flight

Branch verified as `master`. Proceeding.

---

## READING EVIDENCE

**File path:** `C:/Projects/cig-audit/repos/maximo-transposer/package.json`

### Dependencies (production)

| Package | Version spec |
|---|---|
| `aws-sdk` | `^2.901.0` |
| `aws-cli` | `^0.0.2` |
| `json-2-csv` | `^3.11.0` |
| `nodemailer` | `^6.6.0` |
| `mailparser` | `^3.2.0` |
| `xlsx` | `^0.16.9` |

### devDependencies

None declared (`"devDependencies": {}`).

### Scripts defined

| Script | Command |
|---|---|
| `test` | `echo "Error: no test specified" && exit 1` |

### process.env.X references

None. `package.json` contains no `process.env` references (scripts do not reference environment variables).

### Other notable fields

- `"repository"` URL embeds the author's Bitbucket username in the URL: `https://sidneyaulakh@bitbucket.org/cig-code/maximo-transposer.git` (line 20).
- `"main"`: `index.js`
- `"author"`: Sidney Aulakh
- `"license"`: ISC

---

## npm audit — Full Output

Run in: `C:/Projects/cig-audit/repos/maximo-transposer`
Command: `npm audit`

```
# npm audit report

aws-sdk  *
Severity: high
Prototype Pollution via file load in aws-sdk and @aws-sdk/shared-ini-file-loader - https://github.com/advisories/GHSA-rrc9-gqf8-8rwg
JavaScript SDK v2 users should add validation to the region parameter value in or migrate to v3 - https://github.com/advisories/GHSA-j965-2qgj-vjmq
Depends on vulnerable versions of xml2js
No fix available
node_modules/aws-cli/node_modules/aws-sdk
node_modules/aws-sdk
  aws-cli  *
  Depends on vulnerable versions of aws-sdk
  node_modules/aws-cli

minimist  1.0.0 - 1.2.5
Severity: critical
Prototype Pollution in minimist - https://github.com/advisories/GHSA-xvch-5gv4-984h
fix available via `npm audit fix`
node_modules/minimist

nodemailer  <=7.0.10
Severity: high
Header injection in nodemailer - https://github.com/advisories/GHSA-hwqf-gcqm-7353
nodemailer ReDoS when trying to send a specially crafted email - https://github.com/advisories/GHSA-9h6g-pr28-7cqp
Nodemailer: Email to an unintended domain can occur due to Interpretation Conflict - https://github.com/advisories/GHSA-mm7p-fcc7-pg87
Nodemailer's addressparser is vulnerable to DoS caused by recursive calls - https://github.com/advisories/GHSA-rcmh-qjqh-p98v
fix available via `npm audit fix`
node_modules/mailparser/node_modules/nodemailer
node_modules/nodemailer
  mailparser  2.3.1 - 3.6.6
  Depends on vulnerable versions of nodemailer
  node_modules/mailparser

xlsx  *
Severity: high
Denial of Service in SheetJS Pro - https://github.com/advisories/GHSA-g973-978j-2c3p
Denial of Service in SheetJS Pro - https://github.com/advisories/GHSA-3x9f-74h4-2fqr
Denial of Service in SheetsJS Pro - https://github.com/advisories/GHSA-8vcr-vxm8-293m
Prototype Pollution in sheetJS - https://github.com/advisories/GHSA-4r6h-8v6p-xvw6
SheetJS Regular Expression Denial of Service (ReDoS) - https://github.com/advisories/GHSA-5pgg-2g8v-p4x9
No fix available
node_modules/xlsx

xml2js  <0.5.0
Severity: moderate
xml2js is vulnerable to prototype pollution - https://github.com/advisories/GHSA-776f-qx25-q3cc
No fix available
node_modules/aws-cli/node_modules/xml2js
node_modules/xml2js

7 vulnerabilities (2 moderate, 4 high, 1 critical)

To address issues that do not require attention, run:
  npm audit fix

Some issues need review, and may require choosing
a different dependency.
```

**Summary:** 7 vulnerabilities total — 1 critical, 4 high, 2 moderate.

---

## FINDINGS

---

**[P1-A04-1]** *(CRITICAL)*
**Description:** The `minimist` package (a transitive dependency pulled in via `aws-cli`) contains a critical Prototype Pollution vulnerability (GHSA-xvch-5gv4-984h). Versions 1.0.0 through 1.2.5 are affected. Prototype pollution can allow an attacker to modify the prototype of base JavaScript objects, potentially leading to property injection, denial of service, or remote code execution depending on how the polluted properties are consumed by the application. A fix is available via `npm audit fix`.
**Location:** `package.json`:8 (`aws-cli` dependency)
**Checklist item:** Section 5 — Dependencies (known vulnerabilities)
**Advisory:** https://github.com/advisories/GHSA-xvch-5gv4-984h

---

**[P1-A04-2]** *(HIGH)*
**Description:** The `xlsx` package (SheetJS Community Edition, declared as `^0.16.9`) has five known high-severity vulnerabilities with no fix available in the npm registry for the community edition: three Denial of Service advisories (GHSA-g973-978j-2c3p, GHSA-3x9f-74h4-2fqr, GHSA-8vcr-vxm8-293m), one Prototype Pollution (GHSA-4r6h-8v6p-xvw6), and one Regular Expression Denial of Service (GHSA-5pgg-2g8v-p4x9). This package processes untrusted XLSX attachments from email — a denial-of-service or prototype pollution attack via a crafted attachment is a realistic and direct threat path for this application. No npm-registry fix is available; migration to an actively maintained alternative (e.g. ExcelJS) is required.
**Location:** `package.json`:12 (`xlsx` dependency)
**Checklist item:** Section 5 — Dependencies (known vulnerabilities, outdated packages with security patches, XLSX/ExcelJS library)
**Advisories:** GHSA-g973-978j-2c3p, GHSA-3x9f-74h4-2fqr, GHSA-8vcr-vxm8-293m, GHSA-4r6h-8v6p-xvw6, GHSA-5pgg-2g8v-p4x9

---

**[P1-A04-3]** *(HIGH)*
**Description:** The `nodemailer` package (declared as `^6.6.0`) has four known high-severity vulnerabilities: header injection (GHSA-hwqf-gcqm-7353), Regular Expression Denial of Service (GHSA-9h6g-pr28-7cqp), email routing to unintended domains via interpretation conflict (GHSA-mm7p-fcc7-pg87), and a DoS in the addressparser (GHSA-rcmh-qjqh-p98v). The header injection vulnerability is of particular concern in this application, which sends email to recipients. A crafted input could inject additional headers and redirect or blind-copy email. The `mailparser` package (declared as `^3.2.0`) bundles its own vulnerable copy of `nodemailer` (versions 2.3.1–3.6.6), compounding the exposure. A fix is available via `npm audit fix` (upgrade to nodemailer >=7.0.11).
**Location:** `package.json`:10 (`nodemailer`), `package.json`:11 (`mailparser`)
**Checklist item:** Section 5 — Dependencies (known vulnerabilities, email parsing libraries)
**Advisories:** GHSA-hwqf-gcqm-7353, GHSA-9h6g-pr28-7cqp, GHSA-mm7p-fcc7-pg87, GHSA-rcmh-qjqh-p98v

---

**[P1-A04-4]** *(HIGH)*
**Description:** The `aws-sdk` package (declared as `^2.901.0`, i.e. AWS SDK v2) has two known high-severity vulnerabilities: Prototype Pollution via INI file loading (GHSA-rrc9-gqf8-8rwg) and insufficient validation of the `region` parameter (GHSA-j965-2qgj-vjmq). AWS SDK v2 is in maintenance mode and no npm-registry fix is available for these advisories. AWS recommends migration to SDK v3 (`@aws-sdk/*`). Additionally, the `aws-cli` package (version `^0.0.2`) depends on its own vulnerable copy of `aws-sdk`, compounding the issue.
**Location:** `package.json`:7 (`aws-sdk`), `package.json`:8 (`aws-cli`)
**Checklist item:** Section 5 — Dependencies (known vulnerabilities, AWS SDK version)
**Advisories:** GHSA-rrc9-gqf8-8rwg, GHSA-j965-2qgj-vjmq

---

**[P1-A04-5]** *(HIGH)*
**Description:** The `aws-cli` npm package (`^0.0.2`) is an unofficial, third-party npm package that wraps the AWS CLI binary. It is not the official AWS CLI tool, has not been updated since 2014, is at version 0.0.2, and pulls in its own pinned (and vulnerable) copies of `aws-sdk` and `xml2js`. This package is almost certainly not required for a Lambda function — the Lambda runtime does not need an npm-wrapped AWS CLI. Its presence introduces unnecessary attack surface, additional vulnerable transitive dependencies, and the risk of supply-chain compromise from an unmaintained third-party package.
**Location:** `package.json`:8
**Checklist item:** Section 5 — Dependencies (outdated packages, known vulnerabilities)

---

**[P1-A04-6]** *(MEDIUM)*
**Description:** The `xml2js` package (a transitive dependency of both `aws-sdk` and `aws-cli`) at versions below 0.5.0 is vulnerable to Prototype Pollution (GHSA-776f-qx25-q3cc). No npm-registry fix is available for the copies pulled in by these packages. This is a secondary consequence of the `aws-sdk` v2 and `aws-cli` dependencies flagged in A04-4 and A04-5.
**Location:** `package.json`:7–8 (via transitive dependencies of `aws-sdk` and `aws-cli`)
**Checklist item:** Section 5 — Dependencies (known vulnerabilities)
**Advisory:** GHSA-776f-qx25-q3cc

---

**[P1-A04-7]** *(LOW)*
**Description:** The `repository.url` field embeds the author's Bitbucket username directly in the URL (`https://sidneyaulakh@bitbucket.org/cig-code/maximo-transposer.git`). This is a minor information disclosure — the username is embedded in a committed file and would be visible to anyone with read access to the repository. It does not constitute a credential, but it does disclose a personal account identifier. The standard form of the URL does not require a username prefix.
**Location:** `package.json`:20
**Checklist item:** Section 1 — Secrets and Configuration (credentials / identifiers in committed files)

---

**[P1-A04-8]** *(INFO)*
**Description:** No test framework is declared and the `test` script exits with an error (`exit 1`). This means `npm test` always fails. The absence of any automated testing infrastructure means there is no safety net to catch regressions introduced by dependency upgrades or security patches. This is an operational and quality concern; it increases the risk that security fixes cannot be validated before deployment.
**Location:** `package.json`:16
**Checklist item:** Section 5 — Dependencies (general dependency hygiene)

---

## CHECKLIST COVERAGE — Items With No Issues

**Checklist item — Section 1, Secrets and Configuration (scripts embedding credentials):** The single script defined (`test`) contains only a literal echo and exit command. No credentials, API keys, tokens, AWS access keys, or passwords are embedded in any script. No issues found.

**Checklist item — Section 5, node_modules not committed:** `git ls-files node_modules` returned no output, confirming that `node_modules` is not tracked in the repository. The `node_modules` directory does not exist on disk (it is not installed in the working tree). No issues found.

**Checklist item — Section 5, packages installed globally in pipeline not declared in package.json:** All packages consumed at runtime must be declared in `package.json`. The scripts defined in `package.json` do not invoke any globally installed tools beyond what npm itself provides. No issues found within the scope of `package.json` alone (pipeline YAML is out of scope for this file).

---

## SUMMARY TABLE

| Finding | Severity | Package(s) | Fix Available |
|---|---|---|---|
| A04-1 | CRITICAL | `minimist` (transitive via `aws-cli`) | Yes — `npm audit fix` |
| A04-2 | HIGH | `xlsx ^0.16.9` | No — migration required |
| A04-3 | HIGH | `nodemailer ^6.6.0`, `mailparser ^3.2.0` | Yes — `npm audit fix` |
| A04-4 | HIGH | `aws-sdk ^2.901.0`, `aws-cli ^0.0.2` | No — migrate to SDK v3 |
| A04-5 | HIGH | `aws-cli ^0.0.2` | No — remove package |
| A04-6 | MEDIUM | `xml2js` (transitive) | No — blocked on upstream |
| A04-7 | LOW | `package.json` metadata | Yes — edit URL |
| A04-8 | INFO | `scripts.test` | Yes — add test framework |

**Total npm audit vulnerabilities: 7 (1 critical, 4 high, 2 moderate)**

## Pass 2 — Test Coverage

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

**[P2-A02-1]** *(CRITICAL)*
**Description:** The entire codebase has zero automated tests. There is no test framework installed or configured (`package.json` lists no test script, no devDependencies for jest/mocha/chai/tape/ava/vitest). A Lambda function that processes financial/operational data for a port operator and sends emails to external parties has never been exercised in isolation.
**Fix:** Install a test framework (e.g., `jest`) and set `"test": "jest"` in `package.json`. Create a `__tests__/` directory. Mock `aws-sdk` (S3 + SES), `nodemailer`, `mailparser`, and `xlsx`. Write an integration test that drives `exports.handler` with a minimal synthetic SES event.
**Location:** `index.js:9` (`exports.handler`)

---

**[P2-A02-2]** *(CRITICAL)*
**Description:** `attachments[0].content` is accessed at line 3134 without any check on whether `parsed_mail.attachments` exists or has at least one element. If the inbound email has no attachment, or the attachment array is empty, the Lambda throws `TypeError: Cannot read properties of undefined (reading 'content')` and the entire invocation fails with no actionable error message.
**Fix:** Add a test that calls the handler with an email that has zero attachments. The handler should either return a structured error response or throw a domain-specific error. The test should assert that the process fails gracefully rather than with an uncaught TypeError.
**Location:** `index.js:3134`

---

**[P2-A02-3]** *(CRITICAL)*
**Description:** There is no try/catch anywhere in the handler. Failures in `s3.getObject` (non-existent key, permission denied, network error), `simpleParser` (malformed MIME), `XLSX.read` (non-xlsx binary), either `s3.upload` call, or `transporter_2.sendMail` all propagate as unhandled promise rejections and will cause Lambda to log an opaque error and retry the event indefinitely (depending on SQS/SNS configuration).
**Fix:** Add tests that mock each AWS/library call to reject. Assert the handler either catches and logs the error or re-throws a structured error. At minimum: (a) S3 getObject failure, (b) XLSX.read failure with a PDF attachment, (c) SES sendMail failure.
**Location:** `index.js:3126`, `index.js:3130`, `index.js:3134`, `index.js:3229`, `index.js:3436`, `index.js:3459`

---

**[P2-A02-4]** *(HIGH)*
**Description:** `dateFormatChange(date)` is an untested inner function that implements a bespoke Australian date parser. It is called at lines 3192 and 3377/3387/3397 for every row in the spreadsheet. It silently produces garbage output (or throws) if `date` is `undefined`, `null`, an empty string, an ISO date string, a US-format date (mm/dd/yyyy), or missing the time component (no space in the string). There are no guards.
**Fix:** Extract `dateFormatChange` to a module-level export so it can be unit-tested independently. Write tests for: (a) valid Australian date `"31/12/2024 08:30:00"` → expect `"2024-12-31T08:30:00"`, (b) single-digit day and month `"1/3/2024 00:00:00"` → expect `"2024-03-01T00:00:00"`, (c) `undefined` input → expect a thrown error or empty string, (d) ISO-format input `"2024-12-31T08:30:00"` → document expected behaviour.
**Location:** `index.js:3146–3159`

---

**[P2-A02-5]** *(HIGH)*
**Description:** The `cranes_rtgs` lookup object (lines 3288–3358) is rebuilt from scratch on **every iteration** of the inner `for...in` loop. This is a performance bug, but more importantly it is untested: the `ENGINHRS` branch (line 3359) and the crane vs. non-crane sub-branch (line 3360) have never been exercised. The `parent_hours` arithmetic at lines 3365–3370 (`GANTRY + HOIST + TROLLEY + BOOM - PRNT`) can produce `NaN` if any spreadsheet cell is empty or non-numeric, and `NaN` is silently written into the output CSV.
**Fix:** Add a test with a QC/RTG vehicle row where `ENGINHRS` is a field, numeric meter values are provided, and assert the calculated `parent_hours` is numerically correct. Add a second test with a missing/empty `"Boom Hour Meter"` cell and assert the row is either excluded or an error is raised instead of `NaN` being emitted.
**Location:** `index.js:3288–3378`

---

**[P2-A02-6]** *(HIGH)*
**Description:** `event.Records[0].ses` (line 3118) is accessed without any guard. If the Lambda is invoked with a test event that has no `Records` array, or an empty `Records` array, or a record that is not an SES notification, the handler throws immediately. There is no input validation or schema check on the incoming event.
**Fix:** Add a test that passes a completely empty object `{}` as the event and asserts the handler returns a structured validation error rather than throwing a `TypeError`. Add a second test with a valid SES event shape but an empty `Records` array.
**Location:** `index.js:3118`

---

**[P2-A02-7]** *(HIGH)*
**Description:** The `csv.replace(",,,", "")` calls at lines 3217 and 3424 use a plain string argument, not a regex with the global flag. `String.prototype.replace` with a string argument replaces only the **first** occurrence. If the generated CSV has multiple rows with trailing commas (which it will for any output with more than one row shorter than the maximum column count), all subsequent trailing commas remain. This logic is never tested, so the defect has never been caught.
**Fix:** Add a test that provides a spreadsheet with at least two rows that would produce trailing commas in the output CSV and assert that **all** trailing comma sequences are removed from the resulting string.
**Location:** `index.js:3217`, `index.js:3424`

---

**[P2-A02-8]** *(MEDIUM)*
**Description:** When a `vehicle_name` from the spreadsheet is not found in `asset_map` (Branch D, line 3201; Branch L, line 3408), the code silently continues. No error, no log beyond what is already printed, and the vehicle is simply absent from the output file. The customer (DP World) would receive an incomplete Maximo import CSV with no indication that records were dropped. This is untested.
**Fix:** Add a test that includes a spreadsheet row with a vehicle name not present in `asset_map` and assert either (a) the output contains a warning row, or (b) the handler raises a structured notification, or at minimum (c) a `console.warn` / `console.error` is called (spy on it). Document the chosen behaviour.
**Location:** `index.js:3201–3206`, `index.js:3408–3413`

---

**[P2-A02-9]** *(MEDIUM)*
**Description:** When an `asset_name` from the asset map is not present in `column_map` (Branch C, line 3195; Branch K, line 3402), the hour meter reading is silently dropped. This is also untested. The `column_map` currently omits `RUNKM` (used by TVE assets) and `SPREADERHRS` (used by ASC assets) — those meter types will always silently fail the column_map lookup and be excluded from both output CSVs.
**Fix:** Add a test where an asset entry uses `RUNKM` or `SPREADERHRS` and assert the row either appears correctly or produces a warning. Separately, verify whether `RUNKM` and `SPREADERHRS` should be in `column_map`; if so, add them and test the output.
**Location:** `index.js:3107–3115` (`column_map`), `index.js:3183`, `index.js:3195–3199`

---

**[P2-A02-10]** *(MEDIUM)*
**Description:** `parsed_mail.from.text` (line 3131) is read and stored in `from` but the variable is never used after that. This is dead code / a vestigial reference. More importantly, `parsed_mail.from` could be `null` if the email has no `From:` header (malformed email), which would throw `TypeError: Cannot read properties of null (reading 'text')`. This path is untested.
**Fix:** Add a test that passes a minimal raw email with no `From:` header and assert the handler does not crash on line 3131. Either add a null guard or remove the unused variable.
**Location:** `index.js:3131`

---

**[P2-A02-11]** *(MEDIUM)*
**Description:** The S3 bucket name `"maximo-transposer-bucket"` and both output email addresses (lines 3461–3462) are hardcoded literals. There are no `process.env` reads. This means: (a) the bucket name cannot be changed for staging vs. production without a code deploy, (b) there is no way to test with a different bucket without modifying source, and (c) since there are no tests, the correctness of these literals has never been verified programmatically.
**Fix:** Add a test that asserts `s3.upload` is called with `Bucket: "maximo-transposer-bucket"` and `Key` matching the expected filename pattern (timestamp + `-formatted.csv`). This documents the hardcoded configuration as a deliberate contract. Recommend migrating bucket and recipients to `process.env` for testability and operational flexibility.
**Location:** `index.js:3122`, `index.js:3431`, `index.js:3461`

---

**[P2-A02-12]** *(MEDIUM)*
**Description:** The `"Vehicle Name"` column key (line 3178, 3276) and `"Last reported date"` column key (lines 3192, 3377, 3387, 3397) are hardcoded strings that must exactly match the spreadsheet column headers sent by Rayven. There is no test that validates what happens if Rayven changes a column heading (e.g. capitalisation change, extra space). The row would silently produce `undefined` values in the output.
**Fix:** Add a test with a spreadsheet row that uses `"vehicle name"` (lowercase) as the column header and assert the handler either maps it correctly or emits a detectable error, rather than silently producing `undefined` in the output CSV.
**Location:** `index.js:3178`, `index.js:3192`

---

**[P2-A02-13]** *(MEDIUM)*
**Description:** The second result loop (lines 3274–3414) is almost entirely duplicated from the first loop (lines 3176–3207), with the only addition being the `ENGINHRS` / `cranes_rtgs` branch. Both loops iterate `sheetJSON` and push to separate result arrays. Because neither loop is tested, the relationship between the two outputs is undefined by any specification. If the first loop is ever changed, the second may silently diverge.
**Fix:** Add separate tests for the first loop output (basic meter mapping) and the second loop output (ENGINHRS calculation). Assert that the row counts and content of both output CSVs are independently correct for the same input.
**Location:** `index.js:3176–3207`, `index.js:3274–3414`

---

**[P2-A02-14]** *(LOW)*
**Description:** The `sheetJSON` array for an empty spreadsheet (header row only, zero data rows) results in `sheetJSON = []`. Both loops execute zero iterations, and two CSVs with only the two header rows are uploaded to S3 and emailed. This edge case is never tested and the stakeholder impact (receiving a valid-looking but empty Maximo import file) is not documented.
**Fix:** Add a test with an Excel workbook that has column headers but zero data rows. Assert the handler completes without error, the output CSVs contain exactly the two header rows, and the email is still sent.
**Location:** `index.js:3176`, `index.js:3274`

---

**[P2-A02-15]** *(LOW)*
**Description:** `workbook.SheetNames[0]` (line 3139) assumes the workbook has at least one sheet. An empty workbook (saved with no sheets, which is technically invalid XLSX but producible) would return `undefined` and cause `workbook.Sheets[undefined]` to be `undefined`, followed by `XLSX.utils.sheet_to_json(undefined, {})` throwing or returning unexpected data.
**Fix:** Add a test with a valid XLSX buffer that has zero sheets (or simulate `workbook.SheetNames = []`) and assert the handler fails with a readable error rather than a cryptic downstream exception.
**Location:** `index.js:3139`

---

**[P2-A02-16]** *(LOW)*
**Description:** The `"RTG14 - AUFRE-C1"` entry in `asset_map` (line 2081) maps to assets tagged `RTG914` / `RTG914`. This looks like a data-entry error (the key says `RTG14`, the values say `RTG914`). Additionally, `"RTG913 - AUFRE-C1"` and several other AUFRE RTGs have `assettype: "QC"` (lines 2079, 2104, 2129, 2154, 2179, 2204) despite being labelled RTG. These inconsistencies cannot be caught without tests that assert the lookup table shape.
**Fix:** Add a unit test that iterates every key in `asset_map` and asserts (a) the key suffix matches the `assetnum` in at least the first asset sub-entry, and (b) entries whose key starts with `RTG` have `assettype` of `"RTG"` (or document the exceptions explicitly). This would have caught the `RTG14` typo.
**Location:** `index.js:2081`, `index.js:2079`

---

**[P2-A02-17]** *(INFO)*
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
# A04 — Pass 2: Test Coverage Audit
**Audit run:** 2026-02-27-01
**Agent:** A04
**Branch verified:** master

---

## Pre-flight

Branch confirmed as `master`. Proceeding.

---

## Step 1 & 2 — Reading Evidence

### File: `package.json`

**Path:** `package.json`

**dependencies (6 total):**
| Package | Version Spec |
|---|---|
| aws-sdk | ^2.901.0 |
| aws-cli | ^0.0.2 |
| json-2-csv | ^3.11.0 |
| nodemailer | ^6.6.0 |
| mailparser | ^3.2.0 |
| xlsx | ^0.16.9 |

**devDependencies:** `{}` — empty, none declared.

**scripts:**
| Script | Command |
|---|---|
| test | `echo "Error: no test specified" && exit 1` |

**Test framework presence:** None. No jest, mocha, jasmine, tap, ava, vitest, or any other test runner is listed in dependencies or devDependencies.

---

### File: `.gitignore`

**Path:** `.gitignore`

**Patterns (2 total):**
1. `node_modules`
2. `__MACOSX/`

---

### File: `package-lock.json`

**Path:** `package-lock.json`

- **lockfileVersion:** 2
- **packages section entries:** 61 (includes the root package `""` plus all transitive dependencies)
- **top-level `dependencies` section entries:** 54

---

### File: `sample.json`

**Path:** `sample.json`

**Top-level keys (1):**
- `thing`

**Keys under `thing`:**
- `vehicle`
- `usage`
- `rentals`
- `organisation`
- `maintenance`
- `fleets`
- `customer`
- `contract`

---

### File: `serverless.yml`

**Path:** `serverless.yml`

**Service name:** `maximo-transposer`

**Plugins:**
- `serverless-plugin-include-dependencies`

**Custom variables:**
- `bucket`: `maximo-transposer-bucket`

**Provider:**
- name: `aws`
- runtime: `nodejs14.x`
- region: `us-east-1`
- IAM Role Statement: `s3:GetObject` on `arn:aws:s3:::maximo-transposer-bucket/*`

**Functions (1):**
| Function | Handler | Events |
|---|---|---|
| `email_handler` | `index.handler` | (none declared) |

**Environment variables (1, scoped to `email_handler`):**
| Variable | Value |
|---|---|
| BUCKET | `${self:custom.bucket}` → `maximo-transposer-bucket` |

---

## Step 3 — Coverage Gap Analysis for `package.json`

### 3.1 — Is a test framework declared in dependencies or devDependencies?

**No.** `devDependencies` is an empty object `{}`. No test runner (jest, mocha, jasmine, ava, vitest, tap, etc.) appears anywhere in either `dependencies` or `devDependencies`.

### 3.2 — Is there a test script that actually runs tests?

**No.** The `scripts.test` value is:
```
echo "Error: no test specified" && exit 1
```
This is the npm default stub. It explicitly exits with code 1 and runs nothing. Running `npm test` will always fail immediately without executing any tests.

### 3.3 — Is there a test configuration file?

Glob searches were performed for:
- `jest.config*` — **No files found**
- `.mocharc*` — **No files found**

No test configuration file of any kind exists in the repository.

### 3.4 — Are there any test files anywhere in the repo?

Glob searches were performed for:
- `**/*.test.js` — **No files found**
- `**/*.spec.js` — **No files found**
- `**/test/**` — **No files found**
- `**/__tests__/**` — **No files found**

The repository contains zero test files.

### 3.5 — Does `scripts.test` reference a real runner?

**No.** The test script is the npm-generated stub `echo "Error: no test specified" && exit 1`. It does not reference jest, mocha, or any other real test runner.

---

## Step 4 — Config Files: No Testable Logic

**.gitignore** — Configuration file defining version-control exclusion patterns. Contains no executable logic. No test coverage is applicable or possible.

**package-lock.json** — Auto-generated dependency lock file. Contains no executable logic. No test coverage is applicable or possible.

**sample.json** — Static data fixture representing a single vehicle record structure from an upstream API. Contains no executable logic. No test coverage is applicable or possible.

**serverless.yml** — Infrastructure-as-code configuration for AWS Lambda deployment via the Serverless Framework. Contains no executable logic (all values are static strings or framework-interpolated variables). No test coverage is applicable or possible.

---

## Step 5 — Audit Run Number

Glob of `C:/Projects/cig-audit/repos/maximo-transposer/audit/2026-02-27-*` confirmed a single directory: `2026-02-27-01`. The highest existing NN is **01**. This output is written to `2026-02-27-01/pass2/A04-package.md` accordingly.

---

## Findings

---

**[P2-A04-1]** *(CRITICAL)*
**Description:** The repository has no test framework installed. `devDependencies` is entirely empty. There is no jest, mocha, jasmine, ava, vitest, or any other test runner present anywhere in `package.json`. The project cannot execute automated tests in its current state.
**Fix:** Install a test framework as a devDependency. For example: `npm install --save-dev jest`. Add jest (or equivalent) to `devDependencies` in `package.json`. Update `scripts.test` to `"jest"` (or the chosen runner's CLI command).
**Location:** package.json:14

---

**[P2-A04-2]** *(CRITICAL)*
**Description:** The `scripts.test` entry is the npm default stub `echo "Error: no test specified" && exit 1`. Running `npm test` always exits with a non-zero code immediately. No tests are ever invoked. CI pipelines or any process relying on `npm test` will fail before any test logic could run.
**Fix:** Replace the stub with a real test runner invocation, e.g. `"test": "jest"` or `"test": "mocha 'test/**/*.js'"`. This requires also installing the corresponding runner (see A04-1).
**Location:** package.json:16

---

**[P2-A04-3]** *(CRITICAL)*
**Description:** Zero test files exist anywhere in the repository. Searches for `**/*.test.js`, `**/*.spec.js`, `**/test/**`, and `**/__tests__/**` all returned no results. The entire codebase — including the Lambda handler (`index.js`), all transformation logic, email parsing, S3 interaction, and spreadsheet generation — has no unit or integration test coverage whatsoever.
**Fix:** Create a `test/` or `__tests__/` directory and write unit tests for all modules. At minimum, cover: the Lambda handler entry point (`index.handler`), email parsing logic, CSV/spreadsheet transformation functions, and any S3 interaction wrappers. Use mocking (e.g. `jest.mock('aws-sdk')`) for external service calls.
**Location:** (repository root — no test directory exists)

---

**[P2-A04-4]** *(HIGH)*
**Description:** No test configuration file exists (`jest.config.js`, `jest.config.ts`, `.mocharc.js`, `.mocharc.yml`, etc.). Even if a test runner were installed, there is no configuration specifying test file patterns, coverage thresholds, reporters, or environment settings (e.g. `testEnvironment: 'node'` appropriate for a Lambda function).
**Fix:** After installing a test framework (A04-1), create an appropriate configuration file. For jest, create `jest.config.js` at the repository root specifying at minimum: `testEnvironment: 'node'`, `collectCoverage: true`, and `coverageThreshold` with a meaningful minimum (e.g. 80% lines/branches/functions/statements).
**Location:** (repository root — no jest.config.js or .mocharc exists)

---

**[P2-A04-5]** *(MEDIUM)*
**Description:** The runtime declared in `serverless.yml` is `nodejs14.x`, which reached AWS end-of-life in November 2023. No test suite exercises the Lambda handler against a current Node.js LTS runtime. The absence of tests means there is no regression safety net to validate behaviour after a necessary runtime upgrade.
**Fix:** Upgrade the `runtime` in `serverless.yml` to `nodejs20.x` (current AWS LTS as of 2026). Write integration tests that exercise the handler locally (e.g. using `lambda-local` or jest's module system) to catch any runtime-compatibility regressions during the upgrade.
**Location:** serverless.yml:11

---

**[P2-A04-6]** *(INFO)*
**Description:** `devDependencies` is an empty object. In a project of this nature (Lambda function processing emails and generating reports), typical development tooling would include a test runner, a linter (eslint), a type checker or JSDoc validator, and potentially a local invocation tool (`serverless-offline`, `lambda-local`). None of these are present.
**Fix:** Establish a baseline developer toolchain. Recommended additions: `jest` (testing), `eslint` (linting), `serverless-offline` (local Lambda emulation), and optionally `@types/node` for IDE support. Document the setup in a README.
**Location:** package.json:14

---

## Summary Table

| Finding | Severity | Subject |
|---|---|---|
| A04-1 | CRITICAL | No test framework installed in devDependencies |
| A04-2 | CRITICAL | `scripts.test` is the npm default exit-1 stub |
| A04-3 | CRITICAL | Zero test files exist anywhere in the repository |
| A04-4 | HIGH | No test configuration file (jest.config.js / .mocharc etc.) |
| A04-5 | MEDIUM | EOL runtime (nodejs14.x) with no tests to guard upgrade |
| A04-6 | INFO | devDependencies entirely empty; no developer toolchain |

## Pass 3 — Documentation

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

**[P3-A02-1]** *(CRITICAL)*
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

**[P3-A02-2]** *(HIGH)*
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

**[P3-A02-3]** *(HIGH)*
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

**[P3-A02-4]** *(HIGH)*
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

**[P3-A02-5]** *(MEDIUM)*
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

**[P3-A02-6]** *(MEDIUM)*
**Description:** `cranes_rtgs` (lines 3288–3358) is a large inline object defined inside the `for` loop body on every iteration. It has no comment explaining why it exists as a separate data structure from `asset_map`, what the values represent (they are identical to the keys — the object is used purely as a set for membership testing), or why this list partially overlaps with but does not exactly mirror the QC/RTG entries in `asset_map` (e.g. `"RTG14 - AUFRE-C1"` is in `asset_map` but the key in `cranes_rtgs` line 3332 is `"RTG914 - AUFRE-C1"`, matching the internal asset tag rather than the map key). There is also no comment explaining that this object is recreated on every loop iteration, which is a performance concern.
**Fix:** Add a comment block before line 3288 explaining:
- That this object acts as a Set of vehicle names requiring ENGINHRS to be computed rather than read from the report column
- That the values are intentionally identical to the keys (membership test only)
- That it should ideally be hoisted outside the loop
**Location:** index.js:3285

---

**[P3-A02-7]** *(MEDIUM)*
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

**[P3-A02-8]** *(MEDIUM)*
**Description:** Dead / commented-out code occupies significant space throughout the file and has no explanatory comments clarifying intent:
- Lines 10–25: A fully commented-out test email send. The `console.log("Test email sent.")` at line 26 is live but refers to an email send that is commented out, making the log message actively misleading.
- Lines 3232–3249: A fully commented-out production email send (`dpw.upload@bpdzenith.com`) with no explanation of why it was disabled or whether it should be reinstated.
- Lines 3446–3457: A fully commented-out test `sendMail` call inside the live code path, with no explanation.
- Lines 3251–3257 and 3475–3481: Banners reading `TEST WITH PRNT HOURS COMING FROM NEW CALCULATION` and `END OF THE TEST`. These suggest the entire second result block was a temporary experiment that was never cleaned up.

None of these blocks have comments explaining their status (intentionally disabled, superseded, pending removal, etc.).
**Fix:** Each commented-out block should carry a one-line explanation: why it is disabled, whether it is safe to delete, and (for the `console.log` at line 26) the log message should either be removed or corrected to accurately reflect what happened.
**Location:** index.js:10, index.js:26, index.js:3232, index.js:3251, index.js:3446, index.js:3475

---

**[P3-A02-9]** *(MEDIUM)*
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

**[P3-A02-10]** *(LOW)*
**Description:** The variable `from` at line 3131 (`const from = parsed_mail.from.text;`) is assigned but never used anywhere in the function. There is no comment explaining why it is captured (e.g. for future use, for logging, for validation).
**Fix:** Either add a comment explaining the intent (`// captured for future sender-validation use`) or remove the assignment. No JSDoc change is needed but the absence of any comment makes the dead assignment confusing.
**Location:** index.js:3131

---

**[P3-A02-11]** *(LOW)*
**Description:** The `context` parameter of `exports.handler` (line 9) is received but never referenced anywhere in the function body. There is no comment explaining this. While it is conventional in Lambda to accept `context` even when unused, a comment or JSDoc `@param` noting it is unused (or intentionally reserved) would prevent future maintainers from wondering whether it was accidentally omitted from use.
**Fix:** Document in the JSDoc for `exports.handler` (see A02-2) with `@param {Object} context - AWS Lambda context object (unused).`
**Location:** index.js:9

---

**[P3-A02-12]** *(LOW)*
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

**[P3-A02-13]** *(LOW)*
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

**[P3-A02-14]** *(INFO)*
**Description:** The `column_map` does not include `SPREADERHRS`, which is defined in all ASC asset entries (lines 2495–2958). ASC assets have SPREADERHRS as one of their meter keys, but because SPREADERHRS is not in `column_map`, it will be silently skipped in both output loops (same mechanism as A02-13 for TVE/RUNKM). The comment at lines 3105–3106 does not mention this.
**Fix:** Add `SPREADERHRS: "Spreader Hour Meter"` to `column_map` if Spreader readings are required, or add an explicit exclusion comment if intentional.
**Location:** index.js:3107

---

**[P3-A02-15]** *(INFO)*
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
# Pass 3: Documentation Audit — Agent A04
**Repo:** maximo-transposer
**Branch:** master
**Date:** 2026-02-27
**Run:** 2026-02-27-01
**Assigned files:** A01 `.gitignore`, A03 `package-lock.json`, A04 `package.json`, A05 `sample.json`, A06 `serverless.yml`

---

## Reading Evidence

### A01 — `.gitignore`

**File path:** `.gitignore`

Patterns listed (all patterns, line by line):
| Line | Pattern |
|------|---------|
| 1 | `node_modules` |
| 2 | `__MACOSX/` |

Total: 2 patterns.

---

### A03 — `package-lock.json`

**File path:** `package-lock.json`

| Field | Value |
|-------|-------|
| `name` | `maximo-transposer` |
| `version` | `1.0.0` |
| `lockfileVersion` | `2` |

This is a machine-generated file. No documentation is applicable.

---

### A04 — `package.json`

**File path:** `package.json`

**Top-level fields present:**
- `name`
- `version`
- `description`
- `main`
- `dependencies`
- `devDependencies`
- `scripts`
- `repository`
- `author`
- `license`
- `bugs`
- `homepage`

**`description` field value:** `"DPWorld Maximo export"`

**Scripts:**
| Script | Value |
|--------|-------|
| `test` | `echo "Error: no test specified" && exit 1` |

**Dependencies:**
| Package | Version |
|---------|---------|
| `aws-sdk` | `^2.901.0` |
| `aws-cli` | `^0.0.2` |
| `json-2-csv` | `^3.11.0` |
| `nodemailer` | `^6.6.0` |
| `mailparser` | `^3.2.0` |
| `xlsx` | `^0.16.9` |

**devDependencies:** empty object `{}`

---

### A05 — `sample.json`

**File path:** `sample.json`

**Top-level key:** `thing`

**`thing` sub-keys:**
- `vehicle`
- `usage`
- `rentals`
- `organisation`
- `maintenance`
- `fleets`
- `customer`
- `contract`

**`vehicle` fields:** `serialno`, `product_type`, `product_code`, `product_class`, `name`, `model`, `make`, `hour_meter_offset`, `hardwareid`, `hardware_type`, `entered_fleet`, `description`, `dealer_id`, `date_into_service`

**`usage` fields:** `this_week`, `this_month`, `average_weekly_usage_input_one`, `average_weekly_usage`, `average_daily_usage_input_one`, `average_daily_usage`

**`rentals`:** empty array `[]`

**`organisation` fields:** `service_location`, `management_region`, `management_location`

**`maintenance` fields:** `services`, `service_type`, `service_offset`, `service_interval`, `service_calculation_input`, `next_service_type`, `impacts`

**`fleets`:** array with one object `{ "type": 0, "name": "Startup", "id": 1 }`

**`customer`:** empty string `""`

**`contract` fields:** `contract_type`, `contract_postcode`, `contract_name`, `contract_geofence`

---

### A06 — `serverless.yml`

**File path:** `serverless.yml`

| Field | Value |
|-------|-------|
| Service name | `maximo-transposer` |
| Runtime | `nodejs14.x` |
| Region | `us-east-1` |
| Plugin | `serverless-plugin-include-dependencies` |

**Custom variables:**
| Key | Value |
|-----|-------|
| `bucket` | `maximo-transposer-bucket` |

**Functions:**
| Function name | Handler | Events | Environment variables |
|---------------|---------|--------|-----------------------|
| `email_handler` | `index.handler` | *(none defined)* | `BUCKET: ${self:custom.bucket}` |

**IAM Role Statements:**
| Effect | Action | Resource |
|--------|--------|----------|
| Allow | `s3:GetObject` | `arn:aws:s3:::maximo-transposer-bucket/*` |

**Line 1 scaffolding comment:** `# NOTE: update this with your service name` — remains present alongside the actual service name `maximo-transposer`.

---

## Documentation Assessment and Findings

### A01 — `.gitignore`

#### Assessment
The file contains two patterns: `node_modules` (self-explanatory) and `__MACOSX/` (a macOS artifact directory created by Archive Utility when zipping on macOS). The `__MACOSX/` pattern is not obvious to developers unfamiliar with macOS archive behaviour; it warrants a comment. Neither pattern has any inline comment.

**[P3-A01-1]** *(LOW)*
**Description:** The `.gitignore` pattern `__MACOSX/` is not self-explanatory to developers unfamiliar with macOS archive artefacts. No comment explains why this directory is excluded.
**Fix:** Add an inline comment: `__MACOSX/  # macOS Archive Utility metadata directory; excluded to prevent committing OS artefacts`
**Location:** `.gitignore:2`

---

### A03 — `package-lock.json`

This is a machine-generated file managed by npm. No documentation is applicable. No findings.

---

### A04 — `package.json`

#### Assessment

**`description` field:** The value `"DPWorld Maximo export"` is vague. It names the client (DPWorld) and the data source (Maximo) but does not explain what the service does: it receives emails containing Maximo export files, processes them, converts them, and writes the output to S3. The description fails to convey the system's function.

**README:** The `homepage` field references `...#readme` implying a README should exist at the repository root. No README.md is present in the repository. The npm `scripts.test` is the default placeholder ("Error: no test specified"), indicating no test framework has been set up or documented.

**Dependencies — rationale:** JSON does not support comments so no inline rationale is possible; however no external document (README, ADR, wiki) explains the choice of each dependency. Specifically:
- `aws-cli` at `^0.0.2` is an unofficial, unmaintained npm shim for the AWS CLI. Its inclusion alongside `aws-sdk` without explanation is confusing and potentially misleading (see also Pass 2 findings).
- `nodemailer` and `mailparser` together suggest email sending/parsing but no documentation explains which direction (send vs. receive) or why both are needed.
- `xlsx` is present but its role in the pipeline is undocumented.
- `json-2-csv` is present but its role is undocumented.

**[P3-A04-1]** *(MEDIUM)*
**Description:** The `description` field value `"DPWorld Maximo export"` is too vague to convey what the service does. It names the client and data source but omits the actual function: ingesting Maximo export files from email attachments, processing them, and writing results to S3.
**Fix:** Update `description` to something accurate and specific, e.g. `"AWS Lambda service that processes DPWorld Maximo equipment export files received via email attachments and writes converted output to S3"`.
**Location:** `package.json:4`

**[P3-A04-2]** *(HIGH)*
**Description:** No README file exists in the repository despite the `homepage` field referencing `...#readme`. There is no documentation explaining the purpose of the service, its architecture, how to deploy it, how to configure it, or what each dependency is for.
**Fix:** Create a `README.md` at the repository root covering: service overview, architecture diagram or description, deployment instructions (Serverless Framework commands), environment variable descriptions, dependency rationale, and local development setup.
**Location:** `package.json:27` (homepage field referencing absent README)

**[P3-A04-3]** *(MEDIUM)*
**Description:** The `scripts.test` field retains the npm-init placeholder value `"echo \"Error: no test specified\" && exit 1"`. This signals that no tests have been written or documented, and provides no guidance on how to run tests or what the testing approach is.
**Fix:** Either implement a test script with a real test runner, or replace the placeholder with a comment in the README explaining the current test strategy (or lack thereof) and plans for future coverage.
**Location:** `package.json:16`

**[P3-A04-4]** *(MEDIUM)*
**Description:** No documentation explains the rationale for including `aws-cli` (`^0.0.2`) as a runtime dependency. This is an unofficial, low-version npm package that wraps the AWS CLI binary. Its purpose alongside `aws-sdk` is ambiguous and unexplained.
**Fix:** Add an explanation in the README for why `aws-cli` is a dependency (or remove it if unused). If it is used, document what it does that `aws-sdk` cannot.
**Location:** `package.json:8`

**[P3-A04-5]** *(LOW)*
**Description:** No documentation explains why both `nodemailer` and `mailparser` are present as dependencies. Their combined use suggests email send/receive functionality, but the direction and use-case are not explained anywhere.
**Fix:** In the README, document the email processing pipeline: which library handles inbound email parsing (`mailparser`) and whether `nodemailer` is used for outbound notifications or replies.
**Location:** `package.json:10-11`

**[P3-A04-6]** *(LOW)*
**Description:** No documentation explains the roles of `json-2-csv` and `xlsx` in the data pipeline. It is not documented what format(s) the Maximo export arrives in, what transformations are applied, or what output format is produced.
**Fix:** Document the data flow in the README: input format (e.g. Excel/XLSX from Maximo), transformation steps, and output format (e.g. CSV written to S3).
**Location:** `package.json:9,12`

---

### A05 — `sample.json`

#### Assessment

The file is a JSON document with no inline documentation capability. No README or other document explains:
- What system produces this JSON (the structure suggests a telematics/fleet management API, likely Teletrac Navman based on field names like `hardwareid`, `hardware_type`, `hour_meter_offset`).
- Whether this is an input sample, an output sample, or a fixture for testing.
- What the `thing` root key represents (a vehicle/asset entity).
- What units `hour_meter_offset`, `this_week`, `this_month`, `average_weekly_usage` etc. are expressed in (hours? kilometres?).
- What `hardware_type: 4` means (an enum with no legend).
- What `service_calculation_input: "0"` represents.
- Why many fields are `null` and whether that is intentional representative data or incomplete sample data.
- What `impacts: 0` represents (collision/impact events?).
- What `fleets[].type: 0` represents.

**[P3-A05-1]** *(HIGH)*
**Description:** The file `sample.json` has no accompanying documentation explaining its purpose. It is unclear whether this file represents: (a) a sample of the input payload received from an upstream API, (b) a test fixture, or (c) example output. No README or comment describes its role in the system.
**Fix:** Add a section to the README (once created per A04-2) titled "Sample Data" explaining that `sample.json` represents a sample payload from the upstream telematics API (e.g. Teletrac Navman), its structure, and how it is used in the Lambda function for development/testing.
**Location:** `sample.json:1`

**[P3-A05-2]** *(MEDIUM)*
**Description:** Several field values in `sample.json` use opaque numeric codes with no legend or documentation: `hardware_type: 4`, `fleets[0].type: 0`, `dealer_id: 0`, `service_calculation_input: "0"`. Without documentation, their meaning cannot be determined from the file alone.
**Fix:** Document the enumeration values for `hardware_type`, `fleets[].type`, and `service_calculation_input` in the README or in a schema file accompanying `sample.json`.
**Location:** `sample.json:14,42,13,38`

**[P3-A05-3]** *(MEDIUM)*
**Description:** Numeric usage fields (`this_week`, `this_month`, `average_weekly_usage_input_one`, `average_weekly_usage`, `average_daily_usage_input_one`, `average_daily_usage`, `hour_meter_offset`) carry no unit documentation. It is not documented whether values represent hours, kilometres, or another unit.
**Fix:** Document the units for all numeric measurement fields in the README or schema. Based on the `service_interval: 500` value alongside fleet/maintenance context, these are likely hours — confirm and document.
**Location:** `sample.json:11,21-26`

**[P3-A05-4]** *(LOW)*
**Description:** The field `average_weekly_usage_input_one` and `average_daily_usage_input_one` use an ambiguous suffix `_input_one`. It is not documented what "input one" refers to — whether it is a different measurement source, a calculation method variant, or a legacy field name.
**Fix:** Document the distinction between the `_input_one` variant and the base `average_weekly_usage` / `average_daily_usage` fields. If the distinction comes from the upstream API, reference the upstream API documentation.
**Location:** `sample.json:23,25`

---

### A06 — `serverless.yml`

#### Assessment

**Service-level comments:** The file has one comment: the Serverless Framework scaffolding comment on line 1 (`# NOTE: update this with your service name`). This comment was generated by `serverless create` and has never been removed. The service name has been set to `maximo-transposer`, making the note misleading — it implies the name still needs to be updated when it has already been set.

**Function documentation:** The sole function `email_handler` has no comment explaining: what event triggers it (no `events` block is defined — the trigger is entirely undocumented at the YAML level), what it processes, or what it produces.

**IAM permission documentation:** The single IAM statement (`s3:GetObject` on the bucket) has no comment explaining why the Lambda needs S3 read access or what it reads.

**Environment variable documentation:** `BUCKET` is passed to the Lambda but there is no comment explaining what it is used for within the function.

**Missing trigger:** The `email_handler` function defines no `events` block. How this Lambda is invoked (SES, S3 event notification, API Gateway, manual) is entirely undocumented at the infrastructure-as-code level. This is both a configuration gap and a documentation gap.

**Region:** `us-east-1` is hardcoded with no comment explaining why this region is required (e.g. SES may require us-east-1 for email receiving functionality).

**[P3-A06-1]** *(MEDIUM)*
**Description:** The Serverless Framework scaffolding comment on line 1, `# NOTE: update this with your service name`, was never removed after the service name was set. It is now misleading, implying the name still needs updating when `maximo-transposer` is already set.
**Fix:** Remove the scaffolding comment. Optionally replace it with a meaningful comment describing the service purpose, e.g. `# Serverless service for processing DPWorld Maximo export email attachments`.
**Location:** `serverless.yml:1`

**[P3-A06-2]** *(HIGH)*
**Description:** The `email_handler` function has no `events` block. There is no documentation anywhere in the file explaining what triggers this Lambda function. The trigger mechanism (e.g. SES rule, S3 event, manual invocation) is completely absent from the infrastructure definition and undocumented.
**Fix:** Add the appropriate `events` trigger to the function definition. If the trigger is managed outside this Serverless configuration (e.g. an SES receipt rule configured separately), add a comment explicitly stating this and referencing where the trigger is configured.
**Location:** `serverless.yml:20-23`

**[P3-A06-3]** *(MEDIUM)*
**Description:** The `email_handler` function has no comment explaining its purpose, inputs, or outputs. A reader cannot determine from the YAML alone what this handler does.
**Fix:** Add a YAML comment above the function definition, e.g.: `# email_handler: Triggered by SES/S3 on receipt of a Maximo export email. Parses the email attachment, converts the data, and writes the result to the S3 bucket.`
**Location:** `serverless.yml:20`

**[P3-A06-4]** *(LOW)*
**Description:** The IAM statement granting `s3:GetObject` on the bucket has no comment explaining why this permission is required or what the Lambda reads from S3.
**Fix:** Add a comment above the IAM statement, e.g.: `# Allow Lambda to read raw email files stored in S3 by SES`
**Location:** `serverless.yml:13-17`

**[P3-A06-5]** *(LOW)*
**Description:** The environment variable `BUCKET` passed to the Lambda has no comment explaining its purpose or expected value format.
**Fix:** Add a comment, e.g.: `# S3 bucket name where SES-delivered emails are stored and output files are written`
**Location:** `serverless.yml:22-23`

**[P3-A06-6]** *(LOW)*
**Description:** The region is hardcoded as `us-east-1` with no comment explaining why this specific region is required. If this is mandated by SES email receiving (which is only available in certain regions), that context is absent.
**Fix:** Add a comment, e.g.: `# us-east-1 required: SES inbound email receiving is only available in us-east-1, eu-west-1, and ap-southeast-2`
**Location:** `serverless.yml:12`

---

## Summary Table

| Finding ID | File | Severity | Brief Description |
|------------|------|----------|-------------------|
| A01-1 | `.gitignore` | LOW | `__MACOSX/` pattern has no explanatory comment |
| A04-1 | `package.json` | MEDIUM | `description` field is vague and inaccurate |
| A04-2 | `package.json` | HIGH | No README exists despite homepage field referencing one |
| A04-3 | `package.json` | MEDIUM | `test` script is npm-init placeholder; no test documentation |
| A04-4 | `package.json` | MEDIUM | `aws-cli` dependency purpose is unexplained |
| A04-5 | `package.json` | LOW | `nodemailer` + `mailparser` roles are undocumented |
| A04-6 | `package.json` | LOW | `json-2-csv` and `xlsx` roles in data pipeline are undocumented |
| A05-1 | `sample.json` | HIGH | File purpose (input sample, fixture, output?) is undocumented |
| A05-2 | `sample.json` | MEDIUM | Opaque numeric enum codes have no legend |
| A05-3 | `sample.json` | MEDIUM | Numeric measurement fields have no unit documentation |
| A05-4 | `sample.json` | LOW | `_input_one` field suffix meaning is undocumented |
| A06-1 | `serverless.yml` | MEDIUM | Stale scaffolding comment is misleading |
| A06-2 | `serverless.yml` | HIGH | No trigger (`events`) defined or documented for `email_handler` |
| A06-3 | `serverless.yml` | MEDIUM | `email_handler` function has no explanatory comment |
| A06-4 | `serverless.yml` | LOW | IAM statement has no explanatory comment |
| A06-5 | `serverless.yml` | LOW | `BUCKET` environment variable has no explanatory comment |
| A06-6 | `serverless.yml` | LOW | Hardcoded region has no rationale comment |

**Totals:** 17 findings — 0 CRITICAL, 3 HIGH, 5 MEDIUM, 9 LOW, 0 INFO

## Pass 4 — Code Quality

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

**[P4-A02-1]** *(INFO)*
**Description:** `node --check index.js` passes with no errors or warnings. The file is syntactically valid.
**Fix:** No action required.
**Location:** index.js (whole file)

---

### Commented-Out Code

**[P4-A02-2]** *(MEDIUM)*
**Description:** A complete test-email block (`transporter_test`, `console.log`, `mail_result_test`) is commented out at the very top of the handler. The surrounding `console.log("Test email sent.")` at line 26 remains active and prints a misleading message even though no email is sent. This is dead scaffolding from development.
**Fix:** Delete lines 10–24 (the commented-out test-email block) and delete or correct line 26.
**Location:** index.js:10–26

**[P4-A02-3]** *(MEDIUM)*
**Description:** A complete production-send block for the first CSV (transporter + sendMail call targeting `dpw.upload@bpdzenith.com`) is commented out at lines 3233–3249. The first CSV is still uploaded to S3 (line 3229) but never emailed. It is unclear whether the first CSV output is intentionally silent or whether the comment-out was temporary.
**Fix:** Determine whether the first CSV is intentionally not emailed. If it is not needed, remove the entire first CSV generation block (lines 3161–3229). If it is needed, reinstate the send or add a comment explaining the deliberate omission.
**Location:** index.js:3232–3249

**[P4-A02-4]** *(LOW)*
**Description:** A second variant of `mail_result_2 = await transporter_2.sendMail(...)` targeting a test address (`graham.oconnell@trackingsolutions.com.au`) is commented out at lines 3446–3457 immediately above the live send. This is leftover test scaffolding sitting directly adjacent to production code, creating confusion about which call is authoritative.
**Fix:** Delete lines 3446–3457.
**Location:** index.js:3446–3457

**[P4-A02-5]** *(LOW)*
**Description:** Banner comments `// TEST WITH PRNT HOURS COMING FROM NEW CALCULATION` (lines 3251–3257) and `// END OF THE TEST` (lines 3475–3481) remain in the file. These indicate the second CSV/ENGINHRS block was added as a temporary test that was never promoted to permanent status. The banners are misleading noise in production code.
**Fix:** Remove the banner comment blocks at lines 3251–3257 and 3475–3481. If the second output block is permanent, treat it as such and name it appropriately.
**Location:** index.js:3251–3257 and 3475–3481

---

### Dead Code

**[P4-A02-6]** *(MEDIUM)*
**Description:** The variable `from` is declared and assigned at line 3131 (`const from = parsed_mail.from.text;`) but is never read anywhere in the handler. It exists solely as unused code.
**Fix:** Delete line 3131, or use `from` in log output / validation logic if the sender identity is relevant to processing.
**Location:** index.js:3131

**[P4-A02-7]** *(MEDIUM)*
**Description:** `json-2-csv` (package.json line 9) and `aws-cli` (package.json line 8) are declared as dependencies but are never `require()`d in `index.js`. They appear to be vestigial dependencies from earlier development.
**Fix:** Remove `json-2-csv` and `aws-cli` from `package.json` `dependencies` and regenerate `package-lock.json`. This also reduces the Lambda deployment bundle size.
**Location:** index.js (no require call exists); package.json:8–9

**[P4-A02-8]** *(LOW)*
**Description:** The `else` block at lines 3195–3199 and the structurally identical block at lines 3402–3406 contain only a comment stating the problem but take no action. These are empty error-handling branches. Similarly, the `else` blocks at lines 3201–3206 and 3408–3413 are empty. None of these produce any log output, metric, or error throw; unmatched vehicles and unmatched meters silently disappear from the output.
**Fix:** Add at minimum a `console.warn` or `console.error` call in each empty else block so that missing vehicle/meter mappings surface in CloudWatch logs. Ideally, accumulate them and include in the outbound email or a dead-letter queue.
**Location:** index.js:3195–3199, 3201–3206, 3402–3406, 3408–3413

---

### Style Consistency

**[P4-A02-9]** *(LOW)*
**Description:** Variable declaration keywords are mixed throughout the handler. The outer handler scope and first CSV block use `var` for `result`, `worksheet`, `csv`, `csv_cleaned`, and loop variables (`i`, `vehicle_name`, `asset_name`, `original_column_name`, `vehicle_split`). The second CSV block then switches to `var` for `result_2`, `worksheet_2`, etc., but uses `let` for `cranes_rtgs`, `parent_hours`, `transporter_2`, and `mail_result_2`. Meanwhile the S3/mail section of the first block uses `const` for `timestamp`, `filename`, `fileParams`. There is no consistent policy. In the same outer handler scope, `var`, `let`, and `const` all appear for similar declarations.
**Fix:** Adopt a consistent policy: use `const` for values that are never reassigned, `let` for variables that are reassigned, and eliminate `var` entirely. Apply uniformly across both CSV blocks.
**Location:** index.js:3161–3484 (throughout handler logic)

**[P4-A02-10]** *(LOW)*
**Description:** The `SPREADERHRS` property inside every `ASC` asset sub-object is missing a trailing comma after `assetnum`, while every other property in every other asset sub-object in the file has one. This is a consistent formatting inconsistency across all 16 ASC entries (lines 2515, 2544, 2573, 2602, 2631, 2660, 2689, 2718, 2747, 2776, 2805, 2834, 2863, 2892, 2921, 2950).
**Fix:** Add trailing commas after `assetnum: "ASCxxx"` on each of the affected lines to make the style consistent with the rest of the file.
**Location:** index.js:2515, 2544, 2573, 2602, 2631, 2660, 2689, 2718, 2747, 2776, 2805, 2834, 2863, 2892, 2921, 2950

**[P4-A02-11]** *(LOW)*
**Description:** In `ASC205 - AUFIS-C1`, the `OVLPHRS` sub-object has its properties in reversed order (`assetnum` before `assettag`) at lines 2634–2635, while every other asset sub-object in the entire file uses `assettag` first, then `assetnum`. This is a one-off inconsistency.
**Fix:** Swap the property order in the `OVLPHRS` block of `ASC205` to `assettag` first, then `assetnum`, to match the convention used everywhere else.
**Location:** index.js:2633–2636

**[P4-A02-12]** *(LOW)*
**Description:** An extra blank line appears between `"QC003 - AUFRE-C1"` and `"QC004 - AUFRE-C1"` (line 1822) and between `"QC004 - AUFRE-C1"` and `"QC001 - AUMEL-C1"` (line 1852). No other entry-to-entry transition in the 3,000-line `asset_map` uses a blank separator line. These are minor whitespace inconsistencies.
**Fix:** Remove the extraneous blank lines at 1822 and 1852.
**Location:** index.js:1822, 1852

---

### Leaky Abstractions / Structure

**[P4-A02-13]** *(HIGH)*
**Description:** The entire application — S3 fetch, email parse, XLSX parse, two complete CSV transform passes, two S3 uploads, and one email send — is implemented as a single monolithic async function (`exports.handler`, lines 9–3484). The function body is approximately 3,475 lines. There are no helper functions other than `dateFormatChange`. The two CSV generation loops (lines 3176–3207 and 3274–3414) are structural duplicates of each other; the second differs only in that it also handles an ENGINHRS calculation for a subset of assets.
**Fix:** Extract discrete responsibilities into named functions: (1) `fetchEmail(messageId)` for S3 retrieval and parsing, (2) `buildMeterDataRows(sheetJSON, assetMap, columnMap)` for the base CSV transform, (3) `buildEnginHrsRows(sheetJSON, assetMap, columnMap, cranesRtgs)` for the ENGINHRS variant, (4) `uploadToBucket(content, filename)` for S3 uploads, (5) `sendReport(csvContent)` for email dispatch. This also eliminates the code duplication between the two loops.
**Location:** index.js:9–3484

**[P4-A02-14]** *(HIGH)*
**Description:** The `cranes_rtgs` object (lines 3288–3358) is declared and fully initialised inside the innermost `for...in` loop body (the loop over `asset_map[vehicle_name].assets`). This means the same large literal object is reconstructed on every iteration of the inner loop, which can be hundreds or thousands of times per invocation. The object is never modified; it is only checked with `in`.
**Fix:** Move `cranes_rtgs` out of the loops. It should be defined once at the same level as `asset_map` (or at the top of the handler), since its keys are a static subset of `asset_map` keys.
**Location:** index.js:3288–3358

**[P4-A02-15]** *(MEDIUM)*
**Description:** The first CSV generation block (lines 3161–3229) produces a complete `result` array, converts it to CSV, cleans it, and uploads it to S3, but the result is never emailed and its upload is noted with the comment "Do we actually need a copy of the formatted file stored in S3?" (line 3219). The second block (lines 3259–3437) performs an almost identical operation plus the ENGINHRS logic. The existence of the first block, which costs a full S3 upload on every invocation, appears to be vestigial test output from when the ENGINHRS logic was being developed. The tight coupling between the two passes — sharing `sheetJSON`, `asset_map`, `column_map`, and `dateFormatChange` via closure without any explicit interface — makes it difficult to determine the intended relationship between them.
**Fix:** Confirm whether the first CSV output (uploaded as `*-formatted.csv`) still serves any purpose. If not, remove the entire first-pass block (lines 3161–3229). If it does serve a purpose, document it with a comment and add the email send.
**Location:** index.js:3161–3229

**[P4-A02-16]** *(MEDIUM)*
**Description:** `dateFormatChange` (lines 3146–3159) is defined inside `exports.handler`, which means a new function object is allocated on every Lambda invocation. The function has no dependency on handler-scoped state and is pure. Defining it inside the handler also means it is defined after `asset_map` and `column_map` are constructed but before they are used, which is unconventional and creates a visual interrupt in the data → logic flow.
**Fix:** Move `dateFormatChange` to module scope (outside `exports.handler`), between the module-level requires and the handler export.
**Location:** index.js:3146–3159

---

### Data Integrity Issues (flagged as code quality concerns)

**[P4-A02-17]** *(HIGH)*
**Description:** The `asset_map` key for the Brisbane RTG914 asset is `"RTG14 - AUFRE-C1"` (line 2081), but the internal `assettag` and `assetnum` values are both `"RTG914"`. This is a key-name typo: the leading `9` is missing from the map key. Consequently, if incoming spreadsheet data contains `Vehicle Name = "RTG914 - AUFRE-C1"`, it will not match any key in `asset_map` and will be silently dropped. The `cranes_rtgs` map (line 3332) correctly uses `"RTG914 - AUFRE-C1"`, so even if the ENGINHRS path were reached, the key mismatch in `asset_map` would prevent it from doing so.
**Fix:** Rename the `asset_map` key on line 2081 from `"RTG14 - AUFRE-C1"` to `"RTG914 - AUFRE-C1"` to match the asset tag values and the `cranes_rtgs` entry.
**Location:** index.js:2081

**[P4-A02-18]** *(MEDIUM)*
**Description:** Six AUFRE-C1 entries with RTG-prefix keys (`RTG913`, `RTG914` via the typo key, `RTG915`, `RTG916`, `RTG917`, `RTG918`) are assigned `assettype: "QC"` (lines 2079, 2104, 2129, 2154, 2179, 2204). All other RTG assets in the file use `assettype: "RTG"`. The `assettype` field does not appear to be used in the CSV output logic, but the inconsistency suggests copy-paste from the QC block above without correction, and could break any future logic that branches on `assettype`.
**Fix:** Change `assettype` from `"QC"` to `"RTG"` for entries `RTG913` through `RTG918` under `AUFRE-C1`, if these are indeed RTG crane assets.
**Location:** index.js:2079, 2104, 2129, 2154, 2179, 2204

**[P4-A02-19]** *(MEDIUM)*
**Description:** `TVE603 - AUFRE-C1` has `assetnum: "9054"` (line 2345) while `assettag: "TVE603"`. This is the only entry in the entire file where `assetnum` differs from `assettag` and also differs from the map key, and the value `"9054"` does not follow any recognisable naming convention used elsewhere. It may be a legacy Maximo numeric ID left after an asset-renumbering event, or it may be an error.
**Fix:** Verify with the client whether `assetnum: "9054"` is the intended Maximo asset number for TVE603 or whether it should be `"TVE603"`. Document the reason in an inline comment if the divergence is intentional.
**Location:** index.js:2341–2348

**[P4-A02-20]** *(MEDIUM)*
**Description:** `TVE599 - AUFRE-C1` has `assettype: "TV"` (line 2312) while every other TVE asset uses `assettype: "TVE"`. This appears to be a truncation error.
**Fix:** Change `assettype: "TV"` to `assettype: "TVE"` for the `TVE599 - AUFRE-C1` entry, or confirm with the client whether `TV` is the correct type.
**Location:** index.js:2312

**[P4-A02-21]** *(MEDIUM)*
**Description:** `TT36 - AUPBT-C1` (line 925) has `assettag: "TT136"` and `assetnum: "TT136"`, meaning the asset map key is missing the leading `1` compared to the internal asset values. If incoming data contains `Vehicle Name = "TT136 - AUPBT-C1"`, it will not match and will be silently dropped. If incoming data contains `"TT36 - AUPBT-C1"`, it will match but the output assetnum/assettag will be `TT136`, which may or may not be correct.
**Fix:** Verify whether the correct vehicle name in incoming data is `TT36` or `TT136`, and correct either the map key or the internal values accordingly.
**Location:** index.js:925–932

---

### Dependency Version Conflicts

**[P4-A02-22]** *(INFO)*
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

**[P4-A04-1]** *(LOW)*
**Description:** All six `dependencies` entries in `package.json` use the `^` (caret) semver specifier, which is consistent within itself. However, the `devDependencies` block is present but empty. The `serverless-plugin-include-dependencies` plugin declared in `serverless.yml` is a deploy-time plugin that belongs in `devDependencies` in `package.json`, yet it appears nowhere in `package.json` at all (see A06-1). The version specifier style is uniform across all declared dependencies — no mixed `~`/`^` issue.
**Fix:** No specifier inconsistency to fix. See A06-1 for the missing devDependency.
**Location:** `package.json:6-13`

**[P4-A06-1]** *(MEDIUM)*
**Description:** `serverless.yml` declares `serverless-plugin-include-dependencies` as a plugin, but this plugin is not present in `package.json` (neither in `dependencies` nor `devDependencies`), and is absent from `package-lock.json`. This means the plugin is either globally installed on the developer's machine or will cause a deploy failure on any clean environment. This is a broken dependency declaration and a leaky abstraction — deploy infrastructure relies on an implicit global tool state.
**Fix:** Add `serverless-plugin-include-dependencies` to `devDependencies` in `package.json` and run `npm install` to lock it.
**Location:** `serverless.yml:4` / `package.json` (missing)

**[P4-A06-2]** *(LOW)*
**Description:** The YAML indentation and quoting in `serverless.yml` is consistent (2-space indentation throughout). The inline comment on line 1 (`# NOTE: update this with your service name`) is a stale boilerplate comment — the service name has been set to `maximo-transposer` and the note is no longer actionable.
**Fix:** Remove the boilerplate comment on line 1.
**Location:** `serverless.yml:1`

---

### Commented-Out Code

**[P4-A06-3]** *(MEDIUM)*
**Description:** `index.js` (the handler referenced from `serverless.yml`) contains a large block of commented-out code at lines 11–24 that represents a "send test email" flow complete with transporter creation, sendMail call, addresses, subject, html body, and attachments. While index.js is not a directly assigned file, it is the sole handler wired to the function in `serverless.yml`, so this finding is attributed to the serverless.yml deployment unit. Commented-out code of this scope is dead weight that obscures intent, increases cognitive load, and risks being mistaken for active logic.
**Fix:** Remove lines 11–24 of `index.js` (the commented-out test email block). Use version control history to recover this code if needed.
**Location:** `index.js:11-24` (referenced from `serverless.yml:21`)

---

### Dead / Unused Configuration

**[P4-A04-2]** *(HIGH)*
**Description:** `json-2-csv` is declared as a production dependency in `package.json` (`^3.11.0`) and is resolved in `package-lock.json`, but the package is never `require()`d anywhere in `index.js`. Searching `index.js` for `json-2-csv`, `json2csv`, or any related import returns zero matches. This is dead dependency — it adds installation weight and surface area with no functional benefit.
**Fix:** Remove `json-2-csv` from `dependencies` in `package.json`, then run `npm install` to update `package-lock.json`.
**Location:** `package.json:9`

**[P4-A04-3]** *(HIGH)*
**Description:** `aws-cli` (`^0.0.2`) is declared as a production dependency in `package.json`. It is never `require()`d in `index.js`. This package is an unofficial, deprecated npm wrapper around the AWS CLI for Python (the package itself carries a deprecation notice: "Recommend using the official aws cli tools for python"). It is not used in the codebase in any way — not imported, not called as a subprocess, not referenced. Its presence introduces a severely outdated nested `aws-sdk@2.0.31` (see A03-2), multiplied package versions, and deprecated transitive dependencies.
**Fix:** Remove `aws-cli` from `dependencies` in `package.json`, then run `npm install` to update `package-lock.json`.
**Location:** `package.json:8`

**[P4-A06-4]** *(HIGH)*
**Description:** `serverless.yml` declares the environment variable `BUCKET: ${self:custom.bucket}` for the `email_handler` function. However, `index.js` never references `process.env.BUCKET`. The S3 bucket name is hardcoded at three locations in `index.js` as the string literal `"maximo-transposer-bucket"` (lines 3122, 3224, 3431). The environment variable injection is entirely dead — it never reaches the application logic. This creates a false sense of configurability and means a change to `custom.bucket` in `serverless.yml` would have no effect on the actual S3 calls.
**Fix:** Replace the three hardcoded `"maximo-transposer-bucket"` string literals in `index.js` with `process.env.BUCKET`. This will make the environment variable injection actually effective.
**Location:** `serverless.yml:23` / `index.js:3122`, `index.js:3224`, `index.js:3431`

---

### Dependency Version Conflicts

**[P4-A03-1]** *(MEDIUM)*
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

**[P4-A03-2]** *(HIGH)*
**Description:** `aws-cli` pulls in `aws-sdk@2.0.31` (from 2015) as a nested dependency, while the project also uses `aws-sdk@2.901.0` at the top level. The extremely old `aws-sdk@2.0.31` carries known prototype-pollution vulnerabilities (CVSS 7.3, `GHSA-rrc9-gqf8-8rwg`) and is pulled into the install purely because of the dead `aws-cli` dependency. This adds vulnerable code to the deployed Lambda package.
**Fix:** Remove `aws-cli` from `package.json`. This eliminates the vulnerable `aws-sdk@2.0.31` from the tree entirely.
**Location:** `package-lock.json:49-81`

**[P4-A03-3]** *(INFO)*
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

**[P4-A03-4]** *(MEDIUM)*
**Description:** npm version on the audit machine is `10.9.2`. `package-lock.json` uses `lockfileVersion: 2`, which is compatible with npm 7 and above. No lockfileVersion compatibility issue exists. However, `npm install --dry-run` produces no explicit warnings, but `npm audit` reveals three vulnerability categories against the installed tree:
1. `minimist@1.2.5` — **CRITICAL** Prototype Pollution (GHSA-xvch-5gv4-984h, CVSS 9.8) — pulled in transitively by `html-to-text` via `mailparser`
2. `aws-sdk` (both versions) — **HIGH** Prototype Pollution (GHSA-rrc9-gqf8-8rwg, CVSS 7.3) and SDK v2 region validation (GHSA-j965-2qgj-vjmq, CVSS 3.7)
3. `mailparser@3.2.0` — **MODERATE** — via its pinned `nodemailer@6.5.0`

The `minimist` issue is fixed by upgrading to `>=1.2.6`; the `mailparser` fix is available via package update. The `aws-sdk` v2 vulnerability has no fix available at v2.
**Fix:** (1) Upgrade `mailparser` to `>=3.6.7` to pull in a `minimist` version `>=1.2.6`. (2) Evaluate migrating from `aws-sdk` v2 to `@aws-sdk/client-s3` and `@aws-sdk/client-ses` (v3). (3) Remove `aws-cli` to eliminate the vulnerable `aws-sdk@2.0.31`.
**Location:** `package-lock.json:448-452` (minimist), `package-lock.json:82-101` (aws-sdk)

---

### Leaky Abstractions

**[P4-A06-5]** *(MEDIUM)*
**Description:** `serverless.yml` defines `custom.bucket: maximo-transposer-bucket` and correctly references it via `${self:custom.bucket}` in both the IAM role statement and the function environment. The variable reference style is consistent (all `${self:custom.*}` pattern). However, as noted in A06-4, the actual application code (index.js) does not consume the injected `BUCKET` environment variable — it uses the literal string instead. This creates a leaky abstraction: the infrastructure file implies the bucket name is a managed configuration parameter, but the application bypasses that contract entirely.
**Fix:** Fix the application side (see A06-4) so the abstraction is honoured.
**Location:** `serverless.yml:7`, `serverless.yml:17`, `serverless.yml:23`

**[P4-A05-1]** *(INFO)*
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
