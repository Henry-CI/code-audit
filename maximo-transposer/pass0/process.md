# Pass 0: Process Review — maximo-transposer
**Date:** 2026-02-27
**Run:** 01
**Branch audited:** master

---

## Documents reviewed

| File | Present | Notes |
|---|---|---|
| `CLAUDE.md` | No | Absent from repo |
| `README.md` | No | Absent from repo |
| `serverless.yml` | Yes | Deployment configuration |
| `package.json` | Yes | Project metadata |

**Audit framework documents consulted:**
- `/Projects/cig-audit/audit-skills/SKILL-Audit-0Intro.md`
- `/Projects/cig-audit/audit-skills/AUDIT-FRAMEWORK_legacy.md`
- `/Projects/cig-audit/audit-skills/PASS1-CHECKLIST-maximo-transposer.md`

---

## Evidence of thorough reading

### serverless.yml (full content reviewed)
- Service name: `maximo-transposer`
- Plugin: `serverless-plugin-include-dependencies`
- Custom variable: `bucket: maximo-transposer-bucket`
- Provider: AWS, runtime `nodejs14.x`, region `us-east-1`
- IAM role statement: `s3:GetObject` on `arn:aws:s3:::maximo-transposer-bucket/*`
- Function defined: `email_handler` (handler: `index.handler`)
- Environment variable: `BUCKET: ${self:custom.bucket}`
- No events configured, no timeout, no memory setting, no SES trigger defined

### package.json (full content reviewed)
- Name: `maximo-transposer`, version `1.0.0`
- Description: `"DPWorld Maximo export"`
- Main: `index.js`
- Dependencies: `aws-sdk ^2.901.0`, `aws-cli ^0.0.2`, `json-2-csv ^3.11.0`, `nodemailer ^6.6.0`, `mailparser ^3.2.0`, `xlsx ^0.16.9`
- devDependencies: none
- Scripts: `test` → `echo "Error: no test specified" && exit 1`
- Author: Sidney Aulakh, License: ISC
- No types, constants, or functions defined (metadata file only)

---

## Findings

### P0-1 — MEDIUM: No CLAUDE.md exists in the repo

Every pass in both `SKILL-Audit-0Intro.md` and `AUDIT-FRAMEWORK_legacy.md` includes the instruction "Check CLAUDE.md for project-specific concerns." The PASS1 checklist similarly assumes CLAUDE.md is present. Because no CLAUDE.md exists, a future audit session following these instructions will silently skip project-specific checks without any indication that the file is missing. There is also no process guidance for Claude sessions working interactively in this repo — no conventions, no constraints, no deployment instructions.

**Impact:** All project-specific audit checks become no-ops. A session may report "no project-specific concerns found" when none were ever documented.

---

### P0-2 — MEDIUM: Branch name mismatch between framework and repo

`AUDIT-FRAMEWORK_legacy.md` (repository table, row for `maximo-transposer`) specifies the branch to audit as `main`. The actual default branch in the repo is `master`. A future session following the framework will attempt to audit branch `main`, which either does not exist or is a different branch than the one in active use.

**Impact:** Future audit sessions may target the wrong branch or fail with a ref-not-found error. The current audit was run against `master` following the user's confirmation — but the framework document remains incorrect.

---

### P0-3 — LOW: No README.md or any project documentation

The repo contains no README, no architecture notes, no operational runbook, and no description of expected inputs and outputs beyond the one-line `package.json` description (`"DPWorld Maximo export"`). Audit sessions and future developers have no baseline from which to judge whether observed behaviour is correct or intentional.

**Impact:** Without a documented description of intended behaviour (expected senders, attachment types, S3 output structure, downstream consumers), auditors cannot distinguish a design decision from a defect. Pass 1 and Pass 3 are particularly affected.

---

### P0-4 — INFO: Scaffolding comment not removed from serverless.yml

`serverless.yml` line 1 reads:
```
service: maximo-transposer # NOTE: update this with your service name
```

The comment is boilerplate from the Serverless Framework scaffold and was not removed when the project was named. The service name `maximo-transposer` appears correct and is used consistently elsewhere, but the comment implies it may still be provisional. A future session reading this file could interpret the comment as an instruction to change the service name.

**Impact:** Low risk of misinterpretation; the service name is consistent with all other references. Mostly cosmetic but could confuse automated tooling or future contributors.
