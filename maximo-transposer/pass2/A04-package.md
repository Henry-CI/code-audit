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

**[A04-1]** *(CRITICAL)*
**Description:** The repository has no test framework installed. `devDependencies` is entirely empty. There is no jest, mocha, jasmine, ava, vitest, or any other test runner present anywhere in `package.json`. The project cannot execute automated tests in its current state.
**Fix:** Install a test framework as a devDependency. For example: `npm install --save-dev jest`. Add jest (or equivalent) to `devDependencies` in `package.json`. Update `scripts.test` to `"jest"` (or the chosen runner's CLI command).
**Location:** package.json:14

---

**[A04-2]** *(CRITICAL)*
**Description:** The `scripts.test` entry is the npm default stub `echo "Error: no test specified" && exit 1`. Running `npm test` always exits with a non-zero code immediately. No tests are ever invoked. CI pipelines or any process relying on `npm test` will fail before any test logic could run.
**Fix:** Replace the stub with a real test runner invocation, e.g. `"test": "jest"` or `"test": "mocha 'test/**/*.js'"`. This requires also installing the corresponding runner (see A04-1).
**Location:** package.json:16

---

**[A04-3]** *(CRITICAL)*
**Description:** Zero test files exist anywhere in the repository. Searches for `**/*.test.js`, `**/*.spec.js`, `**/test/**`, and `**/__tests__/**` all returned no results. The entire codebase — including the Lambda handler (`index.js`), all transformation logic, email parsing, S3 interaction, and spreadsheet generation — has no unit or integration test coverage whatsoever.
**Fix:** Create a `test/` or `__tests__/` directory and write unit tests for all modules. At minimum, cover: the Lambda handler entry point (`index.handler`), email parsing logic, CSV/spreadsheet transformation functions, and any S3 interaction wrappers. Use mocking (e.g. `jest.mock('aws-sdk')`) for external service calls.
**Location:** (repository root — no test directory exists)

---

**[A04-4]** *(HIGH)*
**Description:** No test configuration file exists (`jest.config.js`, `jest.config.ts`, `.mocharc.js`, `.mocharc.yml`, etc.). Even if a test runner were installed, there is no configuration specifying test file patterns, coverage thresholds, reporters, or environment settings (e.g. `testEnvironment: 'node'` appropriate for a Lambda function).
**Fix:** After installing a test framework (A04-1), create an appropriate configuration file. For jest, create `jest.config.js` at the repository root specifying at minimum: `testEnvironment: 'node'`, `collectCoverage: true`, and `coverageThreshold` with a meaningful minimum (e.g. 80% lines/branches/functions/statements).
**Location:** (repository root — no jest.config.js or .mocharc exists)

---

**[A04-5]** *(MEDIUM)*
**Description:** The runtime declared in `serverless.yml` is `nodejs14.x`, which reached AWS end-of-life in November 2023. No test suite exercises the Lambda handler against a current Node.js LTS runtime. The absence of tests means there is no regression safety net to validate behaviour after a necessary runtime upgrade.
**Fix:** Upgrade the `runtime` in `serverless.yml` to `nodejs20.x` (current AWS LTS as of 2026). Write integration tests that exercise the handler locally (e.g. using `lambda-local` or jest's module system) to catch any runtime-compatibility regressions during the upgrade.
**Location:** serverless.yml:11

---

**[A04-6]** *(INFO)*
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
