# Pass 0: Process Review — calamp-scripts
**Date:** 2026-02-27
**Run:** 01
**Branch:** main
**Auditor:** Claude Sonnet 4.6

---

## Documents Reviewed

| File | Exists | Notes |
|---|---|---|
| `CLAUDE.md` | No | Absent from repository |
| `README.md` | Yes | Only project process document |
| `.gitignore` | Yes | Auto-generated template |
| `AUDIT-FRAMEWORK_legacy.md` | Yes (audit skill) | Workflow guide for all repos |
| `PASS1-CHECKLIST-calamp-scripts.md` | Yes (audit skill) | Pass 1 checklist for this repo |

---

## Evidence of Thorough Reading

### README.md
- Document type: Markdown documentation file (no classes, functions, or types)
- Sections: "What is this repository for?" (lines 3–7), "How do I get set up?" (lines 9–13), "Who do I talk to?" (lines 15–17)
- No code, constants, errors, or types defined

### .gitignore
- Document type: Git ignore ruleset
- Entries: `node_modules/`, `dist/` (×2), `*.class`, `*.py[cod]`, `*.log`, `*.jar`, `target/`, `.idea/`, `TEST*.xml`, `.DS_Store`, `Thumbs.db`, `*.app`, `*.exe`, `*.war`, `*.mp4`, `*.tiff`, `*.avi`, `*.flv`, `*.mov`, `*.wmv`
- No entries specific to this project's actual file types

### AUDIT-FRAMEWORK_legacy.md (workflow guide)
- Sections: Universal rules, Stack 1 (Elixir/Phoenix), Stack 2 (Java/Spring), Stack 3 (Java/JSP/Tomcat), Stack 4 (Android/Java), Stack 5 (C++/Qt), Stack 6 (Node.js/Lambda), Stack 7 (Shell scripts), Appendix A (Triage), Appendix B (Cross-repo), Appendix C (Severity), Appendix D (Agent prompt template)
- Repo mapping table at lines 19–30 lists calamp-scripts as stack "C#", branch "main"
- No C# stack section exists in the document

### PASS1-CHECKLIST-calamp-scripts.md (workflow guide)
- Stack declared: C# (.NET)
- Sections: 1. Secrets and Credentials, 2. AWS Credentials and Permissions, 3. Inbound Device Data Handling, 4. Network and Transport Security, 5. Error Handling and Information Disclosure, 6. Dependency and Platform Security, 7. Server and Deployment
- All sections assume a running C# server application

---

## Actual Repository Contents (for context)

The repository contains no C# source code. Actual contents:

- **CSV files** — CalAmp LMU device configuration scripts (30 files across `Aus Script/`, `UK Script/`, `US Script/`, `8bit Script/`, `Demo Script/`)
- **CALAMP APPS/** — LMU Manager software bundle: `LMUMgr_8.9.10.7.zip`, `LMUToolbox_V41/` (XML config files), `AppendCRC16ToBin/x.bin`
- **URL & PORTS.xlsx** — Excel file in repository root (purpose undocumented)
- **README.md**, **.gitignore**

No `.cs`, `.csproj`, `.sln`, `packages.config`, `appsettings.json`, or any other C# artifact is present.

---

## Findings

---

### P0-1 — Stack misidentified as C# in audit framework
**Severity:** HIGH
**File:** `AUDIT-FRAMEWORK_legacy.md`, repo mapping table

The framework lists calamp-scripts as stack "C# | main". The actual repository contains no C# source code of any kind — no `.cs` files, no `.csproj`, no NuGet packages, no `appsettings.json`, no AWS SDK references. The repository is a collection of CalAmp LMU device configuration scripts in CSV format.

A future audit session following this framework will spend all of Pass 1 searching for C# constructs (hardcoded `BasicAWSCredentials`, `BinaryFormatter`, `AmazonS3Client`, NuGet package versions, etc.) that do not exist. This will produce zero findings not because the code is secure but because the wrong pass is being run against the wrong kind of artifact.

No C# stack section exists anywhere in `AUDIT-FRAMEWORK_legacy.md`, so a future session cannot fall back to a correct checklist even if it notices the mismatch.

---

### P0-2 — PASS1-CHECKLIST is entirely inapplicable to actual repository content
**Severity:** HIGH
**File:** `PASS1-CHECKLIST-calamp-scripts.md`

The checklist opens with: *"calamp-scripts is a C# application that sits between CalAmp GPS devices and AWS. It receives inbound device data (likely over TCP/UDP or HTTP), processes or transforms it, and forwards it upstream to AWS."*

This description does not match the repository. There is no server application. All 7 checklist sections are predicated on this incorrect premise:

- Section 1 checks for `AmazonS3Client`, `AmazonSQSClient`, `BasicAWSCredentials` — none exist
- Section 2 checks for IAM role configuration and AWS SDK usage — none exist
- Section 3 checks for `BinaryFormatter`, socket buffer handling, TCP/UDP deserialization — none exist
- Section 4 checks for TLS certificate validation and `ServerCertificateValidationCallback` — none exist
- Section 5 checks for unhandled C# exceptions and empty `catch` blocks — none exist
- Section 6 checks NuGet packages and `.NET Framework` version — no NuGet packages exist
- Section 7 checks deployment scripts and Bitbucket Pipelines YAML — no pipeline file exists

The checklist is 100% inapplicable. Running Pass 1 using this checklist will produce no findings for reasons of architectural mismatch, not security correctness.

---

### P0-3 — README references undefined "registers" with no definition or location
**Severity:** MEDIUM
**File:** `README.md`, line 12

The README states: *"For any new scripts you wish to create there should be a different version name and it should be register in the 'registers'."*

No file, directory, external system, or document named "registers" exists anywhere in the repository. A future session or new contributor following this instruction cannot comply — there is no indication of where to register a script, what format to use, or what the register is.

---

### P0-4 — README version naming convention is undefined
**Severity:** LOW
**File:** `README.md`, line 12

The README states scripts "should have a different version name" but provides no convention. The actual files use a numeric prefix pattern (e.g., `50.131`, `61.61`, `61.140`, `69.005`) but the README does not document what these numbers represent, how they increment, or what rules distinguish valid from invalid version names. A new contributor cannot determine whether `61.142` and `61.143` are sequential, or whether `69.007` is valid for a different customer than `69.006`.

---

### P0-5 — README single point of contact with no fallback
**Severity:** LOW
**File:** `README.md`, lines 15–17

The "Who do I talk to?" section names only a single individual (Rhythm Duwadi) with no email address, team name, or escalation path. If this person is unavailable, there is no documented alternative. Process instructions that depend on a single named individual are fragile under any personnel change.

---

### P0-6 — No CLAUDE.md — no project-specific process instructions exist
**Severity:** LOW
**File:** (absent)

The repository has no `CLAUDE.md`. Future AI-assisted sessions (including future audit passes) have no project-specific context: no description of the CSV format, no version numbering convention, no deployment process, no list of customers, no description of what Rayven, CI, Telstra, Monogoto, Pod, or DataMono mean. Without this, future sessions must infer all context from filenames and the sparse README.

---

### P0-7 — .gitignore is a generic template irrelevant to this project
**Severity:** LOW
**File:** `.gitignore`

The `.gitignore` is an auto-generated Atlassian template covering Node.js, Java, Python, and application binary types — none of which this project produces. The actual project artifacts that should be evaluated for gitignore inclusion (e.g., the Excel file `URL & PORTS.xlsx`, the zip `LMUMgr_8.9.10.7.zip`, the binary `x.bin`) are all tracked in version control without any documented rationale. The template gives a false impression of the project's technology stack to any session that reads it without also reading the repository contents.

---

### P0-8 — URL & PORTS.xlsx is committed as a binary with no documented purpose
**Severity:** INFO
**File:** `URL & PORTS.xlsx`

An Excel file named "URL & PORTS.xlsx" is committed to the repository root. The README does not mention it, describe its contents, explain who maintains it, or indicate when it should be updated. Binary files cannot be diffed in version history. If this file contains server addresses, port numbers, or credentials (as its name implies), those values are opaque to version control review and to any automated audit tooling.

---

## Summary

| ID | Severity | Description |
|---|---|---|
| P0-1 | HIGH | Stack misidentified as C# in audit framework — repository contains no C# code |
| P0-2 | HIGH | PASS1-CHECKLIST entirely inapplicable — all 7 sections assume a C# server app that does not exist |
| P0-3 | MEDIUM | README references undefined "registers" — no such file, directory, or system exists |
| P0-4 | LOW | Version naming convention undefined — no guidance on the numeric prefix scheme used in filenames |
| P0-5 | LOW | Single point of contact with no fallback or contact details |
| P0-6 | LOW | No CLAUDE.md — no project-specific process context for future sessions |
| P0-7 | LOW | .gitignore is a generic template — no entries relevant to actual project artifacts |
| P0-8 | INFO | URL & PORTS.xlsx committed as binary with no documented purpose |
