# Pass 0: Process Review — FleetFocus
**Repo:** ff-new
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Date:** 2026-02-25
**Auditor:** Claude (main session, no subagents)

---

## Files Reviewed

The following process documents were sought and their presence or absence confirmed:

| File | Status |
|---|---|
| `CLAUDE.md` | **ABSENT** |
| `README.md` (repo root) | **ABSENT** |
| `CONTRIBUTING.md` | **ABSENT** |
| `bitbucket-pipelines.yml` | **ABSENT** |
| `.gitignore` | Present — 5 lines |
| `.project` | Present — Eclipse project descriptor |
| `.classpath` | Present — Eclipse classpath with 33 library entries |
| `.tomcatplugin` | Present — Sysdeo Eclipse Tomcat plugin config |
| `.settings/org.eclipse.core.resources.prefs` | Present — 3 encoding declarations |
| `.settings/org.eclipse.jdt.core.prefs` | Present — Java compiler settings (target: 1.8) |
| `doc/` directory | Present — contains CSV/XLSX test data only, no documentation |

No `pom.xml`, `build.xml`, or `build.gradle` was found anywhere in the repository root.
No Markdown files exist in the repository root or in any non-vendored location.
The only `.md` files in the repo are inside `js/DataTables-1.10.1/` (a vendored third-party library).

---

## Evidence of Thorough Reading

**`.gitignore`** (5 lines)
- Line 1: `.classpath` — ignore Eclipse classpath file
- Line 2: `/work/` — ignore the work/ directory
- Line 3: `/WEB-INF/classes/` — ignore compiled class output
- Line 4: `!classpath/sql/` — un-ignore classpath/sql/ (negation)
- Line 5: `!classpath/files/` — un-ignore classpath/files/ (negation)

**`.project`**
- Project name: `auReskinProject`
- Build spec: `org.eclipse.jdt.core.javabuilder`
- Natures: `org.eclipse.jdt.core.javanature`, `com.sysdeo.eclipse.tomcat.tomcatnature`

**`.classpath`**
- Source path: `WEB-INF/src`
- Output path: `WEB-INF/classes`
- JRE container: `jdk1.8.0_261`
- 28 library entries in `WEB-INF/lib/` (see Pass 1 for CVE analysis)
- 3 variable-path entries resolving via `CATALINA_HOME`

**`.tomcatplugin`**
- Root dir: `/`; webPath: `auReskinProject`; reloadable: `true`; updateXml: `true`

**`.settings/org.eclipse.core.resources.prefs`**
- encoding//layout/header.jsp = UTF-8
- encoding//pages/admin/BootStrap.jsp = UTF-8
- encoding//pages/admin/Vtest.jsp = UTF-8

**`.settings/org.eclipse.jdt.core.prefs`**
- Compliance/source/target: 1.8
- inlineJsrBytecode: enabled; unusedLocal: preserve; debug info: full

---

## Findings

### P0-1 — No CLAUDE.md: AI sessions have no project-specific guidance
**Severity:** HIGH
**Category:** Missing process document

There is no `CLAUDE.md` in the repository. Any AI-assisted session working on this codebase has no project-specific instructions and must infer everything from source code alone. This creates the following concrete risks for future sessions:

- No guidance on which branch to work on. The repository hosts two products (FleetIQ and FleetFocus) on different branches. A session not already briefed on this will have no way to know it is on the wrong branch, or that two products share one repo.
- No guidance on the build process. The build is Eclipse IDE-dependent with no alternative documented. A session attempting a command-line build will have no documented path.
- No guidance on security-sensitive areas, known technical debt, or areas requiring special care.
- No guidance on coding conventions, commit message format, or branching strategy.
- No guidance on the deployment target (Tomcat version, server environment).

Without CLAUDE.md, every AI session starts blind. Any instructions passed in the chat are lost on context compaction, and there is no durable fallback.

**Recommendation:** Create `CLAUDE.md` at the repo root. At minimum it should cover: the two-product/two-branch structure, how to build and deploy, which Tomcat version is targeted, coding conventions, and any areas requiring special caution during AI-assisted editing.

---

### P0-2 — No README.md: No developer onboarding or build documentation
**Severity:** HIGH
**Category:** Missing process document

There is no `README.md` at the repository root. The `doc/` directory exists but contains only CSV and XLSX test data files — no written documentation. The only documentation of the project's structure is the Eclipse IDE configuration files.

Consequences for future sessions and new developers:
- No explanation of what the application does or what the two products (FleetIQ vs FleetFocus) are.
- No build instructions. The build is Eclipse + Sysdeo Tomcat Plugin-dependent (inferred from `.project` and `.tomcatplugin`). There is no Maven, Ant, or Gradle file. A developer without Eclipse cannot build the project from documented steps.
- No documented requirements (Java version, Tomcat version, database, environment variables).
- No deployment instructions.
- No description of the directory structure (`WEB-INF/`, `pages/`, `gps/`, `reports/`, etc.).

**Recommendation:** Create `README.md` covering: project purpose, prerequisites (Eclipse version, JDK 1.8, Tomcat version, DB), build steps, local setup, environment variables or connection string configuration, and deployment procedure.

---

### P0-3 — No CI/CD pipeline: Build and deployment process entirely undocumented and manual
**Severity:** MEDIUM
**Category:** Missing process document

There is no `bitbucket-pipelines.yml` or equivalent CI/CD configuration. There is no automated build, no automated test execution, and no documented deployment pipeline. Combined with the absence of a build script (P0-2), the entire path from source code to deployed application is undocumented.

This means:
- Future sessions cannot verify whether a change builds cleanly.
- There is no automated gate preventing broken code from being deployed.
- Deployment steps are held in individual developers' knowledge, not in the repository.
- The PASS1 checklist for ff-new specifically asks to check `bitbucket-pipelines.yml` for hardcoded credentials; there is nothing to check, but this also means there is no pipeline to enforce security controls.

**Recommendation:** Add a `bitbucket-pipelines.yml` that at minimum documents the build steps, even if it does not yet run automated tests.

---

### P0-4 — .gitignore lists `.classpath` as ignored but the file is committed
**Severity:** LOW
**Category:** Inconsistency between process documents

Line 1 of `.gitignore` is `.classpath`, which should prevent the Eclipse classpath file from being tracked. However, `.classpath` is present and committed in the repository (it is a real tracked file with 33 library entries and a source path declaration).

This inconsistency arises because `.gitignore` rules only affect untracked files. If `.classpath` was committed before the ignore rule was added, git will continue tracking it despite the rule. The practical consequence:

- A developer seeing `.classpath` in `.gitignore` would expect the file not to be tracked. They may be confused when `git status` shows modifications to it.
- An AI session reading `.gitignore` and expecting `.classpath` to be absent will be misled when it finds the file exists and is tracked.
- Changes to `.classpath` (e.g., adding a library) will be included in commits unintentionally, since the developer believes the file is ignored.

**Recommendation:** Either (a) remove `.classpath` from `.gitignore` and commit it intentionally as the project's build configuration, acknowledging the Eclipse dependency, or (b) remove `.classpath` from git tracking (`git rm --cached .classpath`) so the ignore rule takes effect. Option (a) is more appropriate given that `.classpath` is the only build definition for this project.

---

### P0-5 — Partial and inconsistent encoding declarations in Eclipse settings
**Severity:** INFO
**Category:** Incomplete process document / inconsistency

`.settings/org.eclipse.core.resources.prefs` declares explicit UTF-8 encoding for exactly three files:
- `layout/header.jsp`
- `pages/admin/BootStrap.jsp`
- `pages/admin/Vtest.jsp`

The repository contains hundreds of JSP files. The remaining files have no explicit encoding declaration, meaning they inherit the Eclipse workspace default (typically the OS default encoding, which may be CP1252 on Windows). This creates a risk that:

- A future session or tool assumes all JSP files are UTF-8 when only three have explicit declarations.
- A developer on a system with a different default encoding will read or write non-UTF-8 files differently from the three declared files.
- The three declared files suggest someone noticed encoding issues with those specific files and fixed them individually, rather than setting a project-wide default.

**Recommendation:** Set a project-wide default encoding in `.settings/org.eclipse.core.resources.prefs` (`encoding/<project>=UTF-8`) rather than per-file declarations. Verify all JSP files are actually encoded in UTF-8.

---

### P0-6 — IDE-exclusive project metadata committed with no tool-agnostic alternative
**Severity:** INFO
**Category:** Missing defaults / fragile process

All project configuration is Eclipse-specific:
- `.project` — Eclipse project descriptor referencing the Sysdeo Tomcat plugin
- `.classpath` — Eclipse classpath referencing `CATALINA_HOME` as an Eclipse variable
- `.tomcatplugin` — Sysdeo Eclipse Tomcat Plugin configuration
- `.settings/` — Eclipse compiler and resource preferences

There is no tool-agnostic build file (Maven `pom.xml`, Ant `build.xml`, Gradle `build.gradle`). The `CATALINA_HOME` variable in `.classpath` is an Eclipse workspace variable, not an environment variable, so it cannot be resolved outside Eclipse.

For future AI-assisted sessions, this means:
- Attempts to compile or run the project with `javac`, `mvn`, or `gradle` will fail with no documented resolution.
- The classpath (and therefore the full dependency list) is only readable by interpreting Eclipse XML — a session must know to look at `.classpath` for the dependency list rather than a standard manifest.
- Library versions are partly declared in `.classpath` (e.g., `commons-collections-3.1.jar`) but the canonical source of truth for what JARs are in `WEB-INF/lib/` is the directory itself, not a dependency management file.

**Recommendation:** Add a `pom.xml` or `build.xml` so the project can be built without Eclipse. If Eclipse dependency is unavoidable, document this explicitly in README.md.

---

## Summary

| ID | Severity | Finding |
|---|---|---|
| P0-1 | HIGH | No CLAUDE.md — AI sessions have no project-specific guidance |
| P0-2 | HIGH | No README.md — no build, deployment, or onboarding documentation |
| P0-3 | MEDIUM | No CI/CD pipeline — build and deployment process is undocumented and manual |
| P0-4 | LOW | .gitignore lists `.classpath` as ignored but the file is committed |
| P0-5 | INFO | Encoding declarations cover only 3 of hundreds of JSP files |
| P0-6 | INFO | All project metadata is Eclipse-specific with no tool-agnostic build alternative |

The dominant finding of this pass is the complete absence of developer-facing documentation at the repository level. There is no CLAUDE.md, no README, no contributing guide, no CI/CD pipeline, and no build script. The only process artifacts are Eclipse IDE configuration files, which are partially contradicted by the .gitignore. Any future session — human or AI — must reconstruct all project context from source code and IDE config alone.
