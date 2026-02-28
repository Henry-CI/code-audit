# Pass 0: Process Review — gmtpserver
**Date:** 2026-02-28
**Run:** 01
**Branch audited:** master

---

## Documents reviewed

### Audit framework and skill files (external to repo)

- `/Projects/cig-audit/audit-skills/SKILL-Audit-0Intro.md`
  - Defines: audit pass structure, agent partitioning, reading evidence requirements, finding severity levels, output path convention `audit/<YYYY-MM-DD>-<NN>/pass<M>/<FileName>.md`, triage path `audit/<YYYY-MM-DD>-<NN>/triage.md`, finding ID format `A03-1`
- `/Projects/cig-audit/audit-skills/SKILL-Audit-Pass0.md`
  - Defines: Pass 0 scope (process documents only), output path `audit/<YYYY-MM-DD>-<NN>/pass0/process.md`, four check categories
- `/Projects/cig-audit/audit-skills/AUDIT-FRAMEWORK_legacy.md`
  - Defines: repo-to-stack mapping table (including branch column), universal rules, per-stack audit checklists (Passes 1–4), triage path `audit/<repo-name>/<YYYY-MM-DD>/triage.md`, finding ID format `API-A03-2`, Appendices A–D

### Repo process documents

- `CLAUDE.md` — **does not exist**
- `README.md` — **does not exist**
- `install.sh` — empty file (0 bytes); no content to review
- `startup.sh` — Linux service wrapper script; operational, not a process document
- `build.xml` — NetBeans Ant build file; operational, not a process document
- `nbproject/project.xml` — NetBeans project descriptor; operational
- `nbproject/project.properties` — NetBeans build properties; operational

---

## Findings

### P0-1 — No CLAUDE.md in repository

**Severity:** MEDIUM
**Category:** Missing process document

The repository has no `CLAUDE.md` file. Per audit framework universal rules, auditors check `CLAUDE.md` for project-specific security concerns, test file naming/location conventions, documentation conventions, and any instructions that override framework defaults.

Without a `CLAUDE.md`, every future AI session operating on this repo has no project-specific context. Auditors must guess at conventions (e.g., where test files live, whether any checks are intentionally skipped). The framework explicitly calls out CLAUDE.md as the primary source for project overrides — its absence creates a systematic blind spot across all four passes.

**Recommendation:** Create `CLAUDE.md` documenting at minimum: the project's purpose, build system (NetBeans/Ant), test directory location (`test/`), config file locations and their roles, deployment procedure, and any security-relevant notes (e.g., which config files hold credentials).

---

### P0-2 — No README.md in repository

**Severity:** LOW
**Category:** Missing process document

The repository has no `README.md`. There is no documentation of what `gmtpserver`/`GmtpMina` is, what it does, what it connects to, how to build it, how to configure it, or how to deploy it. The only build instruction is implied by the NetBeans project structure (`build.xml`).

This is distinct from P0-1: CLAUDE.md provides auditor/AI context; README provides developer onboarding context. Both are absent.

**Recommendation:** Create `README.md` covering: project purpose, prerequisites, build steps (`ant jar` or via NetBeans), configuration file descriptions, deployment procedure, and any runtime dependencies.

---

### P0-3 — Branch mismatch between audit framework and actual repository

**Severity:** HIGH
**Category:** Inconsistency between process documents

`AUDIT-FRAMEWORK_legacy.md` (mapping table, line 25) specifies that `gmtpserver` must be audited on branch **`main`**:

```
| gmtpserver | Java (general — use Java/Spring section, skip Spring-specific items) | main |
```

The repository's current and only tracked branch is **`master`**. A future session following the framework literally would attempt to check out `main`, either fail (if the branch doesn't exist) or audit a different branch. The framework states: *"Auditing the wrong branch invalidates all findings."*

This ambiguity is actively harmful: a compliant auditor following the framework would be directed to the wrong branch, and an auditor who checks out `master` instead would be deviating from the documented instruction without explicit justification.

**Recommendation:** Update the mapping table in `AUDIT-FRAMEWORK_legacy.md` to specify `master` for gmtpserver, matching the actual default branch.

---

### P0-4 — "Spring-specific items" not defined for Java/general stack

**Severity:** MEDIUM
**Category:** Ambiguous instruction / undefined term

The mapping table entry for `gmtpserver` instructs auditors to use the *Java/Spring section* of the framework but *skip Spring-specific items*:

```
Java (general — use Java/Spring section, skip Spring-specific items)
```

The Java/Spring section (Pass 1, Pass 4) does not identify which checklist items are Spring-specific vs general Java. Two auditors applying this instruction independently would make different decisions. For example:

- Is checking for `@PreAuthorize`/`@Secured` Spring-specific? (Yes, clearly.)
- Is checking CSRF protection Spring-specific? (Spring Security enables it by default, but the concern exists in any framework.)
- Is checking for field injection (`@Autowired`) Spring-specific? (Yes.)
- Is checking for empty catch blocks Spring-specific? (No — general Java.)
- Is checking for `e.printStackTrace()` Spring-specific? (No — general Java.)

Without an explicit list, the instruction is fragile under context compression: a session that has lost earlier context about the project will not know which items to skip.

**Recommendation:** Add a parenthetical note or a separate section in the framework that explicitly lists which Java/Spring checklist items are Spring-framework-specific (e.g., Spring Security configuration, `@Autowired`/`@Service`/`@Repository` annotations, `@Transactional`, Spring CSRF defaults) vs general Java items that always apply.

---

### P0-5 — Triage file path format inconsistent across process documents

**Severity:** MEDIUM
**Category:** Inconsistency between process documents

The two primary process documents specify different path formats for the triage file:

**`SKILL-Audit-0Intro.md`:**
```
audit/<YYYY-MM-DD>-<NN>/triage.md
```

**`AUDIT-FRAMEWORK_legacy.md` (Appendix A):**
```
audit/<repo-name>/<YYYY-MM-DD>/triage.md
```

These formats differ in two ways:
1. The run-number suffix `-<NN>` (present in SKILL-Audit-0Intro.md, absent in AUDIT-FRAMEWORK_legacy.md)
2. The repo-name prefix subdirectory (present in AUDIT-FRAMEWORK_legacy.md, absent in SKILL-Audit-0Intro.md)

A future session with only one document in context would create triage files in a different location than sessions using the other document, breaking the "file is the record of truth" guarantee. Finding IDs in commit messages or issue trackers could reference triage entries that are not where a reader expects them.

**Recommendation:** Align both documents on a single canonical triage path. Given that the skill files govern execution and `SKILL-Audit-0Intro.md` defines the `audit/<YYYY-MM-DD>-<NN>/` namespace consistently with the per-pass output paths, that format is the more coherent choice. Update `AUDIT-FRAMEWORK_legacy.md` Appendix A to match.

---

### P0-6 — Finding ID format inconsistent across process documents

**Severity:** LOW
**Category:** Inconsistency between process documents

The two primary process documents specify different finding ID formats:

**`SKILL-Audit-0Intro.md`:**
> Each agent prefixes its findings with its ID (e.g., A03-1, A03-2).

**`AUDIT-FRAMEWORK_legacy.md` (Appendix A):**
> Finding IDs use the format `<repo-abbreviation>-<agent-id>-<finding-number>` (e.g., `API-A03-2`)

The framework format includes a repo-abbreviation prefix; the skill file does not. If findings from different sessions use different ID formats, references in commit messages, issue trackers, or triage files become ambiguous. A finding referenced as `A03-2` by one session and `GMTP-A03-2` by another is the same finding with two identifiers.

**Recommendation:** Standardize on one format across both documents. If the repo prefix is desired (it adds useful disambiguation when findings from multiple repos are discussed together), update `SKILL-Audit-0Intro.md` to require it. If not, remove it from `AUDIT-FRAMEWORK_legacy.md` Appendix A.

---

## Summary

| ID   | Severity | Description |
|------|----------|-------------|
| P0-1 | MEDIUM   | No CLAUDE.md — missing project-specific auditor/AI context |
| P0-2 | LOW      | No README.md — missing developer onboarding documentation |
| P0-3 | HIGH     | Branch mismatch: framework says `main`, repo is on `master` |
| P0-4 | MEDIUM   | "Spring-specific items" undefined — ambiguous skip instruction |
| P0-5 | MEDIUM   | Triage file path format differs between SKILL-Audit-0Intro.md and AUDIT-FRAMEWORK_legacy.md |
| P0-6 | LOW      | Finding ID format differs between SKILL-Audit-0Intro.md and AUDIT-FRAMEWORK_legacy.md |
