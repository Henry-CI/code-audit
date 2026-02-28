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

**[A04-1]** *(CRITICAL)*
**Description:** The `minimist` package (a transitive dependency pulled in via `aws-cli`) contains a critical Prototype Pollution vulnerability (GHSA-xvch-5gv4-984h). Versions 1.0.0 through 1.2.5 are affected. Prototype pollution can allow an attacker to modify the prototype of base JavaScript objects, potentially leading to property injection, denial of service, or remote code execution depending on how the polluted properties are consumed by the application. A fix is available via `npm audit fix`.
**Location:** `package.json`:8 (`aws-cli` dependency)
**Checklist item:** Section 5 — Dependencies (known vulnerabilities)
**Advisory:** https://github.com/advisories/GHSA-xvch-5gv4-984h

---

**[A04-2]** *(HIGH)*
**Description:** The `xlsx` package (SheetJS Community Edition, declared as `^0.16.9`) has five known high-severity vulnerabilities with no fix available in the npm registry for the community edition: three Denial of Service advisories (GHSA-g973-978j-2c3p, GHSA-3x9f-74h4-2fqr, GHSA-8vcr-vxm8-293m), one Prototype Pollution (GHSA-4r6h-8v6p-xvw6), and one Regular Expression Denial of Service (GHSA-5pgg-2g8v-p4x9). This package processes untrusted XLSX attachments from email — a denial-of-service or prototype pollution attack via a crafted attachment is a realistic and direct threat path for this application. No npm-registry fix is available; migration to an actively maintained alternative (e.g. ExcelJS) is required.
**Location:** `package.json`:12 (`xlsx` dependency)
**Checklist item:** Section 5 — Dependencies (known vulnerabilities, outdated packages with security patches, XLSX/ExcelJS library)
**Advisories:** GHSA-g973-978j-2c3p, GHSA-3x9f-74h4-2fqr, GHSA-8vcr-vxm8-293m, GHSA-4r6h-8v6p-xvw6, GHSA-5pgg-2g8v-p4x9

---

**[A04-3]** *(HIGH)*
**Description:** The `nodemailer` package (declared as `^6.6.0`) has four known high-severity vulnerabilities: header injection (GHSA-hwqf-gcqm-7353), Regular Expression Denial of Service (GHSA-9h6g-pr28-7cqp), email routing to unintended domains via interpretation conflict (GHSA-mm7p-fcc7-pg87), and a DoS in the addressparser (GHSA-rcmh-qjqh-p98v). The header injection vulnerability is of particular concern in this application, which sends email to recipients. A crafted input could inject additional headers and redirect or blind-copy email. The `mailparser` package (declared as `^3.2.0`) bundles its own vulnerable copy of `nodemailer` (versions 2.3.1–3.6.6), compounding the exposure. A fix is available via `npm audit fix` (upgrade to nodemailer >=7.0.11).
**Location:** `package.json`:10 (`nodemailer`), `package.json`:11 (`mailparser`)
**Checklist item:** Section 5 — Dependencies (known vulnerabilities, email parsing libraries)
**Advisories:** GHSA-hwqf-gcqm-7353, GHSA-9h6g-pr28-7cqp, GHSA-mm7p-fcc7-pg87, GHSA-rcmh-qjqh-p98v

---

**[A04-4]** *(HIGH)*
**Description:** The `aws-sdk` package (declared as `^2.901.0`, i.e. AWS SDK v2) has two known high-severity vulnerabilities: Prototype Pollution via INI file loading (GHSA-rrc9-gqf8-8rwg) and insufficient validation of the `region` parameter (GHSA-j965-2qgj-vjmq). AWS SDK v2 is in maintenance mode and no npm-registry fix is available for these advisories. AWS recommends migration to SDK v3 (`@aws-sdk/*`). Additionally, the `aws-cli` package (version `^0.0.2`) depends on its own vulnerable copy of `aws-sdk`, compounding the issue.
**Location:** `package.json`:7 (`aws-sdk`), `package.json`:8 (`aws-cli`)
**Checklist item:** Section 5 — Dependencies (known vulnerabilities, AWS SDK version)
**Advisories:** GHSA-rrc9-gqf8-8rwg, GHSA-j965-2qgj-vjmq

---

**[A04-5]** *(HIGH)*
**Description:** The `aws-cli` npm package (`^0.0.2`) is an unofficial, third-party npm package that wraps the AWS CLI binary. It is not the official AWS CLI tool, has not been updated since 2014, is at version 0.0.2, and pulls in its own pinned (and vulnerable) copies of `aws-sdk` and `xml2js`. This package is almost certainly not required for a Lambda function — the Lambda runtime does not need an npm-wrapped AWS CLI. Its presence introduces unnecessary attack surface, additional vulnerable transitive dependencies, and the risk of supply-chain compromise from an unmaintained third-party package.
**Location:** `package.json`:8
**Checklist item:** Section 5 — Dependencies (outdated packages, known vulnerabilities)

---

**[A04-6]** *(MEDIUM)*
**Description:** The `xml2js` package (a transitive dependency of both `aws-sdk` and `aws-cli`) at versions below 0.5.0 is vulnerable to Prototype Pollution (GHSA-776f-qx25-q3cc). No npm-registry fix is available for the copies pulled in by these packages. This is a secondary consequence of the `aws-sdk` v2 and `aws-cli` dependencies flagged in A04-4 and A04-5.
**Location:** `package.json`:7–8 (via transitive dependencies of `aws-sdk` and `aws-cli`)
**Checklist item:** Section 5 — Dependencies (known vulnerabilities)
**Advisory:** GHSA-776f-qx25-q3cc

---

**[A04-7]** *(LOW)*
**Description:** The `repository.url` field embeds the author's Bitbucket username directly in the URL (`https://sidneyaulakh@bitbucket.org/cig-code/maximo-transposer.git`). This is a minor information disclosure — the username is embedded in a committed file and would be visible to anyone with read access to the repository. It does not constitute a credential, but it does disclose a personal account identifier. The standard form of the URL does not require a username prefix.
**Location:** `package.json`:20
**Checklist item:** Section 1 — Secrets and Configuration (credentials / identifiers in committed files)

---

**[A04-8]** *(INFO)*
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
