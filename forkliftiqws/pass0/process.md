# Pass 0: Process Review — forkliftiqws
**Date:** 2026-02-27
**Run:** 2026-02-27-01
**Auditor:** Claude Sonnet 4.6 (main conversation, no subagents)

---

## Documents Reviewed

### Audit process documents (C:/Projects/cig-audit/audit-skills/)

| File | Sections / structure |
|---|---|
| `SKILL-Audit-0Intro.md` | General intro; passes 0–4 overview; agent IDs; evidence requirements; output path formula; triage dispositions |
| `AUDIT-FRAMEWORK_legacy.md` | Repo mapping table; universal rules; Stack 1 (Elixir/Phoenix); Stack 2 (Java/Spring — forkliftiqws); Stack 3 (Java/JSP/Tomcat); Stack 4 (Android/Java); Stack 5 (C++/Qt); Node.js and Shell stacks (confirmed present, not fully read) |
| `SKILL-Audit-Pass0.md` | General rules; Pass 0 checks (ambiguity, compression fragility, missing defaults, inconsistencies) |
| `SKILL-Audit-Pass1.md` | General rules; security areas; Solidity-specific section (lines 44–57) |
| `SKILL-Audit-Pass2.md` | General rules; test coverage gap categories |
| `SKILL-Audit-Pass3.md` | General rules; documentation completeness and accuracy |
| `SKILL-Audit-Pass4.md` | General rules; style, abstractions, dead code, build warnings, dependency consistency |
| `SKILL-Audit-0Triagemd.md` | General rules; triage workflow; disposition statuses; one-at-a-time rule |
| `WALKTHROUGH-ff-new-Pass1.md` | 9-step walkthrough for ff-new; session-start prompt templates; common mistakes |
| `PASS1-CHECKLIST-forkliftiq-spring.md` | 7 sections covering both forkliftiqadmin and forkliftiqws: secrets, auth, injection, session/CSRF, data exposure, dependencies, build/CI |

### Repository process documents (forkliftiqws root)

| File | Status |
|---|---|
| `CLAUDE.md` | **Absent** |
| `README.md` | **Absent** |

---

## Findings

---

### P0-1 — HIGH
**Category:** Missing process document
**File:** `CLAUDE.md` (absent from repo root)

No `CLAUDE.md` exists anywhere in the `forkliftiqws` repository. Every audit skill document that handles project-specific guidance routes through CLAUDE.md:

- `SKILL-Audit-Pass1.md`: "Check CLAUDE.md for project-specific security concerns"
- `SKILL-Audit-Pass2.md`: "Check CLAUDE.md for project conventions on test file location and naming"
- `SKILL-Audit-Pass3.md`: "Check CLAUDE.md for project-specific documentation conventions"

All three instructions silently produce nothing because the file does not exist. Future audit sessions for passes 1–3 will skip project-specific checks entirely without realising it — there is no error, just a silent no-op.

The Java/Spring stack used by this repo has project-specific factors a future session needs: Cognito/AWS auth integration (visible in recent commits), Spring Security configuration choices, deployment target (the framework mentions Azure for forkliftiqadmin), and whether CSRF is disabled (common in JWT-based REST APIs). None of this is documented anywhere a session can find.

**Recommendation:** Create `CLAUDE.md` at the repo root documenting: tech stack and Java/Spring version, authentication scheme (Cognito JWT vs session), deployment environment, test naming conventions, and any project-specific security decisions a future auditor needs to understand before reviewing code.

---

### P0-2 — HIGH
**Category:** Skill file does not reference required checklist
**File:** `SKILL-Audit-Pass1.md` line 32

`SKILL-Audit-Pass1.md` instructs agents to "Check CLAUDE.md for project-specific security concerns." It does not mention the `PASS1-CHECKLIST-[repo].md` files at all. For forkliftiqws, the project-specific checklist is `PASS1-CHECKLIST-forkliftiq-spring.md`, which contains 7 structured sections covering Spring-specific vulnerabilities (Tomcat credentials in pom.xml, `WebSecurityConfigurerAdapter` filter chain, IDOR patterns, Jackson deserialization, etc.).

A session loading only `SKILL-Audit-Pass1.md` — and finding no CLAUDE.md — would proceed with the generic security checklist and miss every Spring-specific check. The checklist is only surfaced if the user manually includes it in the session-start prompt; no skill document guarantees that inclusion.

**Recommendation:** Add a line to `SKILL-Audit-Pass1.md` instructing agents to also check for and load the repo-specific `PASS1-CHECKLIST-[repo].md` if present.

---

### P0-3 — HIGH
**Category:** Broken file reference
**File:** `WALKTHROUGH-ff-new-Pass1.md` line 237

The walkthrough references the triage skill as:
```
Read C:\Projects\cig-audit\audit-skills\SKILL-Audit-Triage.md
```

The actual file on disk is named `SKILL-Audit-0Triagemd.md`. The name `SKILL-Audit-Triage.md` does not exist. A session following the walkthrough step-by-step would get a file-not-found error at the triage step, with no indication of the correct filename. The mismatch is compounded by the anomalous embedded "md" in `SKILL-Audit-0Triagemd.md` — the filename itself appears to be a typo from a draft that was saved with the extension accidentally included in the stem.

**Recommendation:** Rename `SKILL-Audit-0Triagemd.md` to `SKILL-Audit-Triage.md` (or `SKILL-Audit-Pass0-Triage.md`) and update the reference in the walkthrough. Alternatively, fix only the walkthrough reference to use the current filename.

---

### P0-4 — MEDIUM
**Category:** Ambiguous instruction — branch name mismatch
**File:** `AUDIT-FRAMEWORK_legacy.md`, repo mapping table (line 28)

The framework mapping table states:

| Repository | Stack | Branch to audit |
|---|---|---|
| forkliftiqws | Java/Spring | **main** |

The actual default branch of the `forkliftiqws` repository is `master` (confirmed by `git status`; no `main` branch exists). The universal rule on branch verification reads: "Before beginning any pass, verify you are on the correct branch. If the branch column says 'main', use the repository's default branch." This sentence attempts to reconcile the discrepancy, but it introduces ambiguity: "main" is used both as a literal branch name in other rows (e.g., `api_server → main`) and as a synonym for "default branch" in the clarifying note. A future session must distinguish between the two uses, which is fragile under context compression.

**Recommendation:** Update the mapping table to list the actual branch name (`master`) for forkliftiqws. Alternatively, remove the "if the branch column says 'main'" hedge and simply list the real branch names for every repository.

---

### P0-5 — MEDIUM
**Category:** Checklist filename inconsistency
**File:** Implied session-start template (evidenced by the user's opening message)

The implicit session-start prompt template uses `PASS1-CHECKLIST-[repo].md` as a placeholder. Substituting `[repo]` = `forkliftiqws` yields `PASS1-CHECKLIST-forkliftiqws.md`, which does not exist. The actual file is `PASS1-CHECKLIST-forkliftiq-spring.md`, and it covers **both** `forkliftiqadmin` and `forkliftiqws`. The dual-repo scope is documented only inside the checklist itself (line 5: "Use it for both forkliftiqadmin and forkliftiqws"), not in the filename.

This creates two problems:
1. A session filling in `[repo]` literally gets a file-not-found error.
2. Even if the correct file is loaded, the agent must remember to skip checklist items labelled `(forkliftiqadmin)` while reviewing `forkliftiqws` — a distinction that is vulnerable to context compression.

**Recommendation:** Rename the checklist to `PASS1-CHECKLIST-forkliftiqws.md` (and a separate copy or symlink for `forkliftiqadmin`), or document the correct filename explicitly in the session-start template for these repos.

---

### P0-6 — MEDIUM
**Category:** Inconsistency between documents — reading evidence format
**Files:** All `SKILL-Audit-Pass*.md` vs `AUDIT-FRAMEWORK_legacy.md` (Java/Spring section, lines 242–250)

The `SKILL-Audit-Pass*.md` files specify a three-item evidence format:
1. Module/class name
2. Every function/method name and its line number
3. Every type, error, and constant defined

The `AUDIT-FRAMEWORK_legacy.md` Java/Spring section specifies a six-item evidence format:
1. Fully qualified class name
2. Every public method with return type, parameters, and line number
3. Every annotation on class and each method
4. Every field with access modifier and type
5. Every interface implemented or class extended
6. For config files: every bean definition, every property key

The framework format is substantially more comprehensive. An agent loading only the skill file (and no CLAUDE.md to redirect it to the framework) would produce minimal evidence, potentially missing annotation-based security configurations (`@PreAuthorize`, `@CrossOrigin`, `@Transactional`) that are only visible when annotations are explicitly enumerated.

**Recommendation:** Either update `SKILL-Audit-Pass1.md` to include the full Java/Spring evidence format, or add an explicit instruction in the skill file to use the stack-specific format from `AUDIT-FRAMEWORK_legacy.md`.

---

### P0-7 — MEDIUM
**Category:** Two overlapping authoritative documents
**Files:** `SKILL-Audit-0Intro.md`, `AUDIT-FRAMEWORK_legacy.md`

Both documents claim to define the complete audit process:
- `SKILL-Audit-0Intro.md`: presents itself as the definitive audit skill covering all passes
- `AUDIT-FRAMEWORK_legacy.md`: presents itself as "the operating manual for auditing every CIG codebase"

They are mostly consistent, but differ in:
- Pass 0 is defined in `0Intro.md` but absent from the `AUDIT-FRAMEWORK_legacy.md` four-pass list (the framework defines only passes 1–4)
- Evidence requirements differ in specificity (see P0-6)
- The `_legacy` suffix on the framework filename implies it is superseded, but no replacement document exists and the framework contains the stack-specific content the skill files lack

A session that loads only one document misses requirements from the other. Currently the user mitigates this by explicitly asking that both be read at session start, but that dependency is not documented anywhere — it exists only in the user's personal workflow.

**Recommendation:** Clarify the relationship between the two documents. Either merge them into one authoritative source, or add a header to each explaining which document takes precedence and which is the companion.

---

### P0-8 — MEDIUM
**Category:** Missing process document
**File:** `README.md` (absent from repo root)

No README.md exists anywhere in the `forkliftiqws` repository. The framework's Pass 3 documentation check explicitly requires: "Verify the README.md documents: how to build (`mvn clean install`), how to run locally, required environment variables, deployment process." The absence means:

- Audit agents running Pass 3 will immediately find a README absence finding, but they will have no documentation to compare against the build and deployment process
- There is no on-ramp for new developers or auditors to understand how to work with the codebase
- The `environment.local.properties.template` file suggests the team knows environment variables must be configured, but the template file provides no instructions

**Recommendation:** Create `README.md` documenting at minimum: how to build (`mvn clean install`), how to configure environment properties for local development, and the deployment target.

---

### P0-9 — LOW
**Category:** Irrelevant content in generic skill file
**File:** `SKILL-Audit-Pass1.md` lines 44–57

The `SKILL-Audit-Pass1.md` generic Pass 1 skill contains a "Solidity-Specific Concerns" section covering EVM opcodes, reentrancy in ERC20/721 tokens, bytecode hash verification, and function pointer tables. For any non-Solidity repo (including all 10 CIG audit targets, which are Elixir, Java, Android, C++/Qt, Node.js, and Shell), this section is irrelevant.

While unlikely to cause false positives in practice, it occupies context window space and could confuse a future agent into searching Java code for EVM-related patterns. The section is not labelled as conditional on the stack.

**Recommendation:** Wrap the Solidity section with a conditional header such as "Solidity-Specific Concerns (skip for non-Solidity repos)" or move it to a separate `SKILL-Audit-Pass1-Solidity.md` skill file.

---

### P0-10 — LOW
**Category:** Fragile instruction under context compression
**Files:** All `SKILL-Audit-Pass*.md`, general rules section

Every pass skill file instructs: "glob for `audit/<YYYY-MM-DD>-*` and use one higher than the highest existing number, or 01 if none exist."

The "or 01 if none exist" clause is a single phrase in the middle of a longer sentence. Under context compression, an agent may see an empty glob result and treat it as unexpected rather than as the defined starting case. This is particularly likely on the first run of an audit for a newly cloned repository, where the audit directory itself may not exist and the glob returns nothing.

**Recommendation:** Make the empty-result case more prominent, e.g.: "If the glob returns no results (first audit run), use 01."

---

## Summary

| ID | Severity | Description |
|---|---|---|
| P0-1 | HIGH | `CLAUDE.md` absent; project-specific checks in all passes will silently no-op |
| P0-2 | HIGH | `SKILL-Audit-Pass1.md` does not reference `PASS1-CHECKLIST-*.md` files; checklist will be skipped if not manually included |
| P0-3 | HIGH | `WALKTHROUGH-ff-new-Pass1.md` references `SKILL-Audit-Triage.md` which does not exist (actual: `SKILL-Audit-0Triagemd.md`) |
| P0-4 | MEDIUM | Framework mapping table says branch `main`; actual branch is `master`; ambiguous clarifying note is fragile |
| P0-5 | MEDIUM | `PASS1-CHECKLIST-[repo].md` template does not resolve to a real filename for `forkliftiqws` |
| P0-6 | MEDIUM | Reading evidence format in skill files (3 items) is weaker than framework Java/Spring format (6 items); annotation-level details will be missed |
| P0-7 | MEDIUM | Two overlapping authoritative documents (`SKILL-Audit-0Intro.md` and `AUDIT-FRAMEWORK_legacy.md`) with no stated precedence; loading only one produces incomplete instructions |
| P0-8 | MEDIUM | `README.md` absent; Pass 3 documentation checks cannot compare against intended build/run process |
| P0-9 | LOW | `SKILL-Audit-Pass1.md` contains Solidity-specific section irrelevant to all CIG audit targets |
| P0-10 | LOW | "or 01 if none exist" clause in glob instruction is fragile under context compression |
