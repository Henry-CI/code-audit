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

**[A01-1]** *(HIGH)*
**Description:** The `.gitignore` does not exclude `.env` or `.env.*` files. If a developer creates a `.env` file containing AWS credentials, SES passwords, or Maximo API keys (a common practice during local development), that file will not be blocked from being committed to the repository. This is a systemic risk — the absence of this pattern provides no protection against accidental credential commits.
**Location:** `.gitignore` (entire file — pattern absent)
**Checklist item:** Section 1 — Secrets and Configuration: "Verify `.env` and `.env.*` are in `.gitignore`."

---

### A03 — package-lock.json

**[A03-1]** *(HIGH)*
**Description:** `xlsx@0.16.9` is a severely outdated and effectively abandoned version of the SheetJS library (circa early 2021). The npm package has since been deprecated by its maintainer. This version has known formula injection risks and no ongoing security maintenance. Any CVEs disclosed after the abandonment will never be patched in this version. The application uses this library to process untrusted email attachments, making this a high-severity concern.
**Location:** `package-lock.json` line 562-584 (`node_modules/xlsx`), line 1003-1019 (legacy `dependencies` block)
**Checklist item:** Section 5 — Dependencies: "Check for outdated packages with available security patches. Focus on: the XLSX/ExcelJS library (formula injection CVEs exist in some versions)."

**[A03-2]** *(MEDIUM)*
**Description:** `aws-cli@0.0.2` is a deprecated npm package (registry message: "Recommend using the official aws cli tools for python"). It is a runtime dependency (`dependencies`, not `devDependencies`), meaning it is bundled into the Lambda deployment package. It pulls in a nested `aws-sdk@2.0.31` (from approximately 2014) which receives no security updates. The aws-cli npm package is unnecessary for a Lambda function and adds attack surface and package size for no benefit.
**Location:** `package-lock.json` line 36-48 (`node_modules/aws-cli`), line 613-649 (legacy block)
**Checklist item:** Section 5 — Dependencies: "Check for outdated packages with available security patches."

**[A03-3]** *(MEDIUM)*
**Description:** `minimist@1.2.5` is resolved as a transitive dependency (`mailparser` → `html-to-text` → `minimist`). CVE-2021-44906 (prototype pollution) affects minimist versions before 1.2.6. An attacker who can influence the parsed arguments could pollute the Object prototype. Version 1.2.6 or later fixes this vulnerability.
**Location:** `package-lock.json` line 448-452 (`node_modules/minimist`), line 921-924 (legacy block)
**Checklist item:** Section 5 — Dependencies: "Check `package-lock.json` for known vulnerabilities."

---

### A05 — sample.json

**[A05-1]** *(LOW)*
**Description:** `sample.json` contains values that appear to be real operational data: a vehicle serial number (`"IR1872"`), a fleet asset name (`"QC001 - WST"`), and a hardware device identifier (`"4661425649"`). Committing real customer or operational asset identifiers to source control — even a private repository — is contrary to data minimisation principles. If the repository is or becomes accessible to third parties (e.g., during an audit, open-sourcing, or a repository exposure incident), this data is exposed. The file should use clearly fictional/placeholder values.
**Location:** `sample.json` lines 4 (`serialno`), 8 (`name`), 10 (`hardwareid`)
**Checklist item:** Section 1 — Secrets and Configuration (general principle of not committing real data to repositories).

---

### A06 — serverless.yml

**[A06-1]** *(LOW)*
**Description:** The S3 bucket name `maximo-transposer-bucket` is hardcoded as a custom variable in `serverless.yml` and exposed in source control. While not a credential, bucket names are a form of infrastructure enumeration data. Best practice is to parameterise bucket names via SSM Parameter Store or Serverless Framework parameters, particularly when the repository may be accessible to parties outside the team.
**Location:** `serverless.yml` line 7 (`custom.bucket`)
**Checklist item:** Section 1 — Secrets and Configuration: "Check `serverless.yml` for hardcoded credentials, API keys, SES credentials, S3 bucket names, or AWS account IDs."

**[A06-2]** *(MEDIUM)*
**Description:** `bitbucket-pipelines.yml` is absent from the repository. There is no CI/CD pipeline configuration. Deployments are presumably performed manually from a developer machine using `serverless deploy`. This means: (a) there is no automated security scanning gate before deployment; (b) deployment credentials are stored on individual developer machines rather than in a secrets-managed pipeline environment; (c) there is no audit trail of who triggered deployments and with what code state. The absence of a pipeline is itself a security control gap.
**Location:** Repository root — file not present
**Checklist item:** Section 1 — Bitbucket Pipelines: "Check `bitbucket-pipelines.yml` for hardcoded AWS credentials..." — note: file is absent, which is itself a finding.

**[A06-3]** *(HIGH)*
**Description:** The IAM role defined in `serverless.yml` grants only `s3:GetObject`. The `email_handler` function uses `nodemailer` (SES sending) and `mailparser` (email processing), and the standard flow for an SES-triggered Lambda writes output back to S3 and sends reply emails. The missing permissions are `s3:PutObject` (to write processed output) and `ses:SendEmail` / `ses:SendRawEmail` (to send replies). One of two conditions must hold: (1) the Lambda fails silently at runtime when attempting write operations or SES sends — a functional defect with security implications (undetected failure); or (2) additional permissions are granted outside this file (e.g., a manually attached managed policy or overly-broad `AdministratorAccess` policy), which would be an unauditable over-privilege condition. Either outcome is a security concern.
**Location:** `serverless.yml` lines 13-17 (`provider.iamRoleStatements`)
**Checklist item:** Section 2 — IAM and AWS Permissions: "Verify the function only has permissions for the specific actions it performs: `s3:GetObject`, `s3:PutObject`, `ses:SendEmail`."

**[A06-4]** *(CRITICAL)*
**Description:** The Lambda runtime is `nodejs14.x`. Node.js 14 reached End of Life on 30 April 2023 and AWS Lambda retired the `nodejs14.x` managed runtime (it no longer receives AWS security patches or Node.js upstream patches). Running on an EOL runtime means all security vulnerabilities discovered in Node.js 14 after its EOL date are permanently unpatched in this deployment. The current supported LTS runtime is Node.js 20 (or 22). This must be updated immediately.
**Location:** `serverless.yml` line 11 (`provider.runtime: nodejs14.x`)
**Checklist item:** Section 4 — Runtime Security: "Check the Node.js runtime version in `serverless.yml`. Verify it is not end-of-life (Node.js 14 and 16 are EOL). Use Node.js 20 or later."

**[A06-5]** *(MEDIUM)*
**Description:** No `timeout:` is configured at provider or function level. The AWS Lambda default timeout is 3 seconds. The `email_handler` function processes email attachments, parses XLSX files, transforms data, and sends reply emails via SES — operations that can easily take 10–60 seconds depending on attachment size and network latency to SES. With a 3-second timeout, legitimate large emails will cause silent Lambda timeouts. In Lambda, a timeout results in a failed invocation but SES may still have accepted the email — leaving the email unprocessed with no visible error to the sender (the sender receives no bounce). This is both a reliability and a security concern (denial of service via large attachments becomes trivially easy).
**Location:** `serverless.yml` — `timeout:` key absent at provider level (line 9-17) and function level (line 19-23)
**Checklist item:** Section 6 — Lambda and AWS Configuration: "Verify the Lambda function has an appropriate timeout configured."

**[A06-6]** *(MEDIUM)*
**Description:** No `memorySize:` is configured at provider or function level. The AWS Lambda default memory is 128 MB. XLSX parsing of large spreadsheets, email MIME parsing via `mailparser`, and CSV generation via `json-2-csv` are all memory-intensive operations. Processing a multi-sheet XLSX with tens of thousands of rows at 128 MB is likely to cause out-of-memory Lambda crashes (exit code 137). Lambda memory also determines CPU allocation — low memory means slower processing and higher timeout risk. Recommended minimum for file-processing workloads is 512 MB; 1024 MB is common.
**Location:** `serverless.yml` — `memorySize:` key absent at provider level (line 9-17) and function level (line 19-23)
**Checklist item:** Section 6 — Lambda and AWS Configuration: "Check memory configuration."

**[A06-7]** *(HIGH)*
**Description:** No `events:` block is defined for `email_handler` in `serverless.yml`. This means the SES receipt rule that triggers this Lambda is configured outside of Infrastructure-as-Code (manually or via another stack). The security consequence is that: (a) the trigger configuration — specifically any sender allow-listing, recipient filtering, or S3 action ordering — cannot be reviewed or enforced through code review or deployment pipelines; (b) there is no guarantee that the SES receipt rule restricts which senders can trigger the Lambda (the checklist item requires verifying the SES trigger "only accepts email from expected sources or domains, not from anyone"); (c) the trigger configuration may drift from the intended state with no IaC to enforce it. This is a high finding because an unrestricted SES trigger allows anyone on the internet to invoke this Lambda by sending an email to the configured address.
**Location:** `serverless.yml` lines 19-23 — no `events:` key under `email_handler`
**Checklist item:** Section 6 — Lambda and AWS Configuration: "Verify the SES trigger is configured to only accept email from expected sources or domains, not from anyone."

**[A06-8]** *(MEDIUM)*
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
