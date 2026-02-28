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

**[A01-1]** *(LOW)*
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

**[A04-1]** *(MEDIUM)*
**Description:** The `description` field value `"DPWorld Maximo export"` is too vague to convey what the service does. It names the client and data source but omits the actual function: ingesting Maximo export files from email attachments, processing them, and writing results to S3.
**Fix:** Update `description` to something accurate and specific, e.g. `"AWS Lambda service that processes DPWorld Maximo equipment export files received via email attachments and writes converted output to S3"`.
**Location:** `package.json:4`

**[A04-2]** *(HIGH)*
**Description:** No README file exists in the repository despite the `homepage` field referencing `...#readme`. There is no documentation explaining the purpose of the service, its architecture, how to deploy it, how to configure it, or what each dependency is for.
**Fix:** Create a `README.md` at the repository root covering: service overview, architecture diagram or description, deployment instructions (Serverless Framework commands), environment variable descriptions, dependency rationale, and local development setup.
**Location:** `package.json:27` (homepage field referencing absent README)

**[A04-3]** *(MEDIUM)*
**Description:** The `scripts.test` field retains the npm-init placeholder value `"echo \"Error: no test specified\" && exit 1"`. This signals that no tests have been written or documented, and provides no guidance on how to run tests or what the testing approach is.
**Fix:** Either implement a test script with a real test runner, or replace the placeholder with a comment in the README explaining the current test strategy (or lack thereof) and plans for future coverage.
**Location:** `package.json:16`

**[A04-4]** *(MEDIUM)*
**Description:** No documentation explains the rationale for including `aws-cli` (`^0.0.2`) as a runtime dependency. This is an unofficial, low-version npm package that wraps the AWS CLI binary. Its purpose alongside `aws-sdk` is ambiguous and unexplained.
**Fix:** Add an explanation in the README for why `aws-cli` is a dependency (or remove it if unused). If it is used, document what it does that `aws-sdk` cannot.
**Location:** `package.json:8`

**[A04-5]** *(LOW)*
**Description:** No documentation explains why both `nodemailer` and `mailparser` are present as dependencies. Their combined use suggests email send/receive functionality, but the direction and use-case are not explained anywhere.
**Fix:** In the README, document the email processing pipeline: which library handles inbound email parsing (`mailparser`) and whether `nodemailer` is used for outbound notifications or replies.
**Location:** `package.json:10-11`

**[A04-6]** *(LOW)*
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

**[A05-1]** *(HIGH)*
**Description:** The file `sample.json` has no accompanying documentation explaining its purpose. It is unclear whether this file represents: (a) a sample of the input payload received from an upstream API, (b) a test fixture, or (c) example output. No README or comment describes its role in the system.
**Fix:** Add a section to the README (once created per A04-2) titled "Sample Data" explaining that `sample.json` represents a sample payload from the upstream telematics API (e.g. Teletrac Navman), its structure, and how it is used in the Lambda function for development/testing.
**Location:** `sample.json:1`

**[A05-2]** *(MEDIUM)*
**Description:** Several field values in `sample.json` use opaque numeric codes with no legend or documentation: `hardware_type: 4`, `fleets[0].type: 0`, `dealer_id: 0`, `service_calculation_input: "0"`. Without documentation, their meaning cannot be determined from the file alone.
**Fix:** Document the enumeration values for `hardware_type`, `fleets[].type`, and `service_calculation_input` in the README or in a schema file accompanying `sample.json`.
**Location:** `sample.json:14,42,13,38`

**[A05-3]** *(MEDIUM)*
**Description:** Numeric usage fields (`this_week`, `this_month`, `average_weekly_usage_input_one`, `average_weekly_usage`, `average_daily_usage_input_one`, `average_daily_usage`, `hour_meter_offset`) carry no unit documentation. It is not documented whether values represent hours, kilometres, or another unit.
**Fix:** Document the units for all numeric measurement fields in the README or schema. Based on the `service_interval: 500` value alongside fleet/maintenance context, these are likely hours — confirm and document.
**Location:** `sample.json:11,21-26`

**[A05-4]** *(LOW)*
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

**[A06-1]** *(MEDIUM)*
**Description:** The Serverless Framework scaffolding comment on line 1, `# NOTE: update this with your service name`, was never removed after the service name was set. It is now misleading, implying the name still needs updating when `maximo-transposer` is already set.
**Fix:** Remove the scaffolding comment. Optionally replace it with a meaningful comment describing the service purpose, e.g. `# Serverless service for processing DPWorld Maximo export email attachments`.
**Location:** `serverless.yml:1`

**[A06-2]** *(HIGH)*
**Description:** The `email_handler` function has no `events` block. There is no documentation anywhere in the file explaining what triggers this Lambda function. The trigger mechanism (e.g. SES rule, S3 event, manual invocation) is completely absent from the infrastructure definition and undocumented.
**Fix:** Add the appropriate `events` trigger to the function definition. If the trigger is managed outside this Serverless configuration (e.g. an SES receipt rule configured separately), add a comment explicitly stating this and referencing where the trigger is configured.
**Location:** `serverless.yml:20-23`

**[A06-3]** *(MEDIUM)*
**Description:** The `email_handler` function has no comment explaining its purpose, inputs, or outputs. A reader cannot determine from the YAML alone what this handler does.
**Fix:** Add a YAML comment above the function definition, e.g.: `# email_handler: Triggered by SES/S3 on receipt of a Maximo export email. Parses the email attachment, converts the data, and writes the result to the S3 bucket.`
**Location:** `serverless.yml:20`

**[A06-4]** *(LOW)*
**Description:** The IAM statement granting `s3:GetObject` on the bucket has no comment explaining why this permission is required or what the Lambda reads from S3.
**Fix:** Add a comment above the IAM statement, e.g.: `# Allow Lambda to read raw email files stored in S3 by SES`
**Location:** `serverless.yml:13-17`

**[A06-5]** *(LOW)*
**Description:** The environment variable `BUCKET` passed to the Lambda has no comment explaining its purpose or expected value format.
**Fix:** Add a comment, e.g.: `# S3 bucket name where SES-delivered emails are stored and output files are written`
**Location:** `serverless.yml:22-23`

**[A06-6]** *(LOW)*
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
