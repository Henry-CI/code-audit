# Pass 0: Process Review — ff-new (FleetIQ)

**Repo:** ff-new (FleetIQ)
**Branch:** `multi-customer-sync-to-master` (verified via `git branch --show-current`)
**Date:** 2026-03-01
**Audit run:** 2026-03-01-01

---

## Prior Audit Runs

Two prior Pass 0 runs exist for this branch:
- `audit/2026-02-25-01/pass0/process.md` — 8 findings (P0-1 through P0-8)
- `audit/2026-02-25-02/pass0/process.md` — 10 findings (P0-1 through P0-10)

No `triage.md` exists for either prior run. All prior findings remain PENDING.

No changes to any process document were committed between 2026-02-25 and 2026-03-01 (`git log --since=2026-02-25 -- "*.md" "CLAUDE*" "README*" "Jenkinsfile" "bitbucket-pipelines.yml" "web.xml"` returned no output).

---

## Documents Reviewed

### Documents found and read in full

**`.gitignore`** (8 lines)
- Exclusion entries: `.classpath`, `.settings/`, `/work/`, `/WEB-INF/classes/`, `/.idea/`, `/auReskinProjectMulti.iml`, `/pages/firebase.jsp`, `/excel_rpt/`

**`.project`** (18 lines — Eclipse project descriptor)
- Project name: `MULTI`
- Build command: `org.eclipse.jdt.core.javabuilder`
- Natures: `org.eclipse.jdt.core.javanature`, `com.sysdeo.eclipse.tomcat.tomcatnature`

**`.classpath`** (47 lines — Eclipse classpath)
- JRE: `jdk1.8.0_261`
- Source directory: `WEB-INF/src`
- Output directory: `WEB-INF/classes`
- 30 library JARs referenced in `WEB-INF/lib/` (including log4j-api-2.17.0, log4j-core-2.17.0, poi-3.9, commons-fileupload-1.1, httpclient-4.2.3, jbcrypt-0.3m, jsoup-1.12.1, gson-2.8.5, joda-time-2.10.4, jstl-1.2)
- Tomcat variables: `CATALINA_HOME/lib/jasper-el.jar`, `jasper.jar`, `jsp-api.jar`, `servlet-api.jar`, `mail.jar`

**`.tomcatplugin`** (11 lines — Sysdeo Tomcat plugin config)
- rootDir: `/`; webPath: `auReskinProject`; reloadable: `true`; exportSource: `false`

**`Jenkinsfile`** (0 bytes — empty file)

**`index.jsp`** (24 lines)
- Line 4: `<meta http-equiv="REFRESH" content="0;url=pages/login.jsp">` — meta-refresh redirect to login
- Line 5: `<title>FleetFocus</title>` — title says FleetFocus on the FleetIQ branch
- Line 10: `location.href(url)` — JavaScript error: `href` is a property, not a function
- Line 14: `<body onLoad="send()">` — `<head>` opened on line 3 never explicitly closed
- Line 22: `</div>` — closing tag with no matching opening `<div>`

**`WEB-INF/web.xml`** (209 lines — active Servlet 3.0 configuration)
- Servlet spec: `web-app_3_0.xsd` (Servlet 3.0)
- Description: `Linde Fleet Management SYSTEM`
- Servlets defined (10): `Frm_saveuser`, `Frm_security`, `Frm_login`, `Frm_upload`, `Frm_vehicle`, `Frm_customer`, `GetMessages`, `Import_Files`, `CustomUpload`, `BusinessInsight`, `GetFile`
- All mapped under `/servlet/<ServletName>`
- Session timeout: **360000 minutes** (~250 days) — line 165
- Security constraint (lines 169–177): `/pages/*` requires `CONFIDENTIAL` (HTTPS). Preceded by comment: `<!-- USE THIS FOR UK ONLY Require HTTPS for everything except /img (favicon) and /css. -->`
- Security constraint (lines 179–197): `*.ico`, `/img/*`, `/js/*`, `/css/*`, `/skin/js/*`, `/skin/css/*`, `/gps/*`, `/reports/*`, `/dyn_report/*`, `/includes/*`, `/images/*` — transport-guarantee `NONE`
- Filter: `UrlRewriteFilter` on `/*` (REQUEST + FORWARD dispatchers)
- No `<login-config>`, no `<auth-constraint>`, no `<security-role>` defined
- JSP encoding: UTF-8

**`WEB-INF/web - Copy.xml`** (92 lines — older Servlet 2.3 configuration)
- Servlet spec: `web-app_2_3.dtd` (Servlet 2.3 — two versions older than active web.xml)
- Description: `Linde Fleet Management SYSTEM`
- Contains `net.bull.javamelody.MonitoringFilter` on `/*` + `net.bull.javamelody.SessionListener` — not present in active `web.xml`
- Servlets defined (4 only): `Frm_saveuser`, `Frm_security`, `Frm_login`, `Frm_upload` — missing 7 servlets present in active web.xml
- Session timeout: **30 minutes** — line 79
- No security constraint, no HTTPS enforcement
- Contains `<taglib>` elements directly in `<web-app>` (valid in Servlet 2.3, deprecated since 2.4)

**`.gitattributes`** (1000+ lines — line ending and binary markers)
- Default: `* text=auto !eol`
- Explicitly lists hundreds of `.class` files under `WEB-INF/classes/` with `-text`
- Lists `vssver2.scc` files at: `WEB-INF/classes/META-INF/`, `WEB-INF/classes/com/torrent/surat/fms6/master/`, `.../reports/`, `.../security/`

### Documents searched for but not found

| Document | Purpose | Found? |
|---|---|---|
| `CLAUDE.md` | AI session instructions | No |
| `README.md` | Project overview, build, deploy | No |
| `CONTRIBUTING.md` | Workflow, branching, review process | No |
| `bitbucket-pipelines.yml` | CI/CD pipeline | No |
| `pom.xml` | Maven build manifest | No |
| `build.xml` | Ant build manifest | No |
| `build.gradle` | Gradle build manifest | No |
| `.editorconfig` | Editor formatting rules | No |
| `CODEOWNERS` | Code ownership | No |

---

## Findings

Findings P0-1 through P0-10 are carried forward from `audit/2026-02-25-02/pass0/process.md` unchanged — none have been addressed. P0-11 is a new finding identified in this run from full content comparison of both `web.xml` files.

---

### P0-1 — No CLAUDE.md

- **Severity:** MEDIUM
- **Category:** Process > Missing instructions
- **Status:** Carried forward from 2026-02-25-02 — unresolved
- **File:** (not present)
- **Description:** No `CLAUDE.md` exists in the repository. A future AI session has zero guidance on: project structure, naming conventions, multi-tenant architecture, build process, deployment targets, branch strategy, or the relationship between the FleetIQ and FleetFocus products. The branch name `multi-customer-sync-to-master` implies multi-customer architecture is central to this product, but nothing documents what that means, how tenant isolation works, or what conventions apply.
- **Recommendation:** Create a `CLAUDE.md` at the repo root documenting at minimum: project name and purpose, technology stack (Java/JSP/Tomcat, JDK 1.8), build process (Eclipse-dependent), deployment target (Tomcat), branch strategy (FleetIQ vs FleetFocus), multi-tenant data model, and directory layout.

---

### P0-2 — No README.md or project-level documentation

- **Severity:** MEDIUM
- **Category:** Process > Missing documentation
- **Status:** Carried forward from 2026-02-25-02 — unresolved
- **File:** (not present)
- **Description:** There is no README.md or any project-level documentation. The `doc/` directory contains only CSV/XLSX sample data files. There is no documented way to build, run, test, or deploy this application. The only clues to the build process are the Eclipse IDE configuration files, which implicitly require Eclipse with the Sysdeo Tomcat plugin and a `CATALINA_HOME` Eclipse classpath variable. A new developer cannot determine the build or deploy process without tribal knowledge.
- **Recommendation:** Create a `README.md` documenting: prerequisites (JDK 1.8, Eclipse, Tomcat version, Sysdeo plugin), build steps, deployment steps, required environment variables, and how to run locally.

---

### P0-3 — No build system manifest (IDE-dependent build)

- **Severity:** MEDIUM
- **Category:** Process > Missing build definition
- **Status:** Carried forward from 2026-02-25-02 — unresolved
- **File:** `.classpath` (lines 1–47), `.project` (lines 1–18)
- **Description:** No `pom.xml`, `build.xml`, or `build.gradle` exists. The project can only be built via Eclipse using the `.classpath` file. Dependencies are vendored JARs in `WEB-INF/lib/` with no version management system. The `.classpath` references `CATALINA_HOME` as an Eclipse classpath variable (line 14), not a system environment variable, making the build unreproducible outside Eclipse and unscriptable for CI/CD.
- **Recommendation:** At minimum, document the Eclipse-specific build process. Ideally, introduce a `pom.xml` or `build.xml` so the project can be built from the command line.

---

### P0-4 — Empty Jenkinsfile

- **Severity:** LOW
- **Category:** Process > Ambiguous CI/CD state
- **Status:** Carried forward from 2026-02-25-02 — unresolved
- **File:** `Jenkinsfile` (0 bytes)
- **Description:** The `Jenkinsfile` exists but is completely empty. Its presence implies CI/CD via Jenkins was intended or started, but it contains no pipeline definition. A future developer or session could assume a CI pipeline exists and wonder why builds aren't running, or assume CI is not configured and miss that Jenkins infrastructure may exist elsewhere.
- **Recommendation:** Either populate the Jenkinsfile with a working pipeline, or delete it and document in a README that CI/CD is not configured.

---

### P0-5 — .gitignore inconsistencies with tracked IDE files

- **Severity:** LOW
- **Category:** Process > Inconsistent configuration
- **Status:** Carried forward from 2026-02-25-02 — unresolved
- **File:** `.gitignore` (line 1), `.classpath`, `.project`, `.tomcatplugin`
- **Description:** `.gitignore` lists `.classpath` as ignored, but the file is tracked in git. `.project` and `.tomcatplugin` are tracked but not listed in `.gitignore`. The IntelliJ `.idea/` directory and `auReskinProjectMulti.iml` are listed in `.gitignore`. This creates an inconsistent policy: some IDE config is ignored, some is tracked, and one ignored file is still tracked anyway. A future contributor cannot determine whether IDE config files are meant to be version-controlled.
- **Recommendation:** Decide a consistent policy: either track all IDE config (remove from `.gitignore`) or ignore all (use `git rm --cached` on tracked ones). Document the decision.

---

### P0-6 — Project identity inconsistency across five names

- **Severity:** LOW
- **Category:** Process > Ambiguous naming
- **Status:** Carried forward from 2026-02-25-02 — unresolved
- **File:** `.project:4`, `.tomcatplugin:10`, `.gitignore:6`, `index.jsp:5`, `WEB-INF/web.xml:8`
- **Description:** The project is referred to by at least five different names with no document explaining the canonical name or why they differ:
  1. `.project` line 4: project name **`MULTI`**
  2. `.tomcatplugin` line 10: webPath **`auReskinProject`**
  3. `.gitignore` line 6: IntelliJ module **`auReskinProjectMulti.iml`**
  4. `index.jsp` line 5: `<title>`**`FleetFocus`**`</title>` — on the FleetIQ branch
  5. `WEB-INF/web.xml` line 8: `<description>`**`Linde Fleet Management SYSTEM`**`</description>`

  The `index.jsp` title is particularly confusing: on the `multi-customer-sync-to-master` branch (FleetIQ), the landing page says "FleetFocus." A future session or developer could reasonably conclude they are on the wrong branch.
- **Recommendation:** Document the canonical product name for each branch. Update `index.jsp` title to match the product on this branch. Explain in a README or CLAUDE.md why legacy names (`auReskinProject`, `MULTI`, `Linde`) exist.

---

### P0-7 — Ambiguous "USE THIS FOR UK ONLY" comment on active HTTPS constraint

- **Severity:** LOW
- **Category:** Process > Ambiguous instructions
- **Status:** Carried forward from 2026-02-25-02 — unresolved
- **File:** `WEB-INF/web.xml` (line 168)
- **Description:** Line 168 contains the comment `<!-- USE THIS FOR UK ONLY Require HTTPS for everything except /img (favicon) and /css. -->` directly above the active `<security-constraint>` that enforces HTTPS on `/pages/*`. This is ambiguous: (a) the constraint is not commented out, so it IS active — but the comment says it should only apply in UK; (b) there is no mechanism to conditionally apply it per deployment; (c) a future session modifying security constraints could misread this as "HTTPS is only required for UK deployments" and weaken transport security for other environments.
- **Recommendation:** Clarify whether HTTPS enforcement applies to all deployments or only UK. If all, remove the misleading comment. If deployment-specific, document the toggling mechanism.

---

### P0-8 — `web - Copy.xml` has materially different security configuration from active `web.xml`

- **Severity:** LOW
- **Category:** Process > Ambiguous artifacts
- **Status:** Enhanced from 2026-02-25-02 — prior run noted the file's existence; this run identifies its content diverges significantly
- **File:** `WEB-INF/web - Copy.xml`, `WEB-INF/web.xml`
- **Description:** `web - Copy.xml` is not a simple backup of `web.xml`. Detailed comparison shows they are substantively different configurations:

  | Property | `web.xml` (active) | `web - Copy.xml` |
  |---|---|---|
  | Servlet spec | Servlet 3.0 (`web-app_3_0.xsd`) | Servlet 2.3 (`web-app_2_3.dtd`) |
  | Session timeout | **360,000 minutes (~250 days)** | **30 minutes** |
  | Monitoring | None | `net.bull.javamelody.MonitoringFilter` on `/*` |
  | Servlets | 10 defined | 4 defined (Frm_vehicle, Frm_customer, GetMessages, Import_Files, CustomUpload, BusinessInsight, GetFile all absent) |
  | HTTPS constraint | Present (`/pages/*` → CONFIDENTIAL) | Absent |
  | Tag library config | Via `<jsp-config>` (Servlet 3.0 style) | Via `<taglib>` in `<web-app>` (Servlet 2.3 style) |

  The copy appears to be a significantly older version of the configuration. Its presence in version control with no documentation creates risk: the 250-day session timeout in active `web.xml` versus 30-minute timeout in the copy suggests the copy may reflect a prior intended configuration. There is no documented explanation for why the session timeout was changed from 30 to 360,000 minutes. A developer deploying in a hurry could accidentally use the wrong file.

- **Recommendation:** Compare the two files with intent. If the copy is historical only, delete it from version control and document why the session timeout is 250 days. If the copy represents a deployment variant, name it explicitly (e.g., `web-local.xml`) and document when each is used. At minimum, explain the 360,000-minute session timeout.

---

### P0-9 — No contributing or workflow documentation

- **Severity:** INFO
- **Category:** Process > Missing workflow guidance
- **Status:** Carried forward from 2026-02-25-02 — unresolved
- **File:** (not present)
- **Description:** No CONTRIBUTING.md or workflow documentation exists. There is no guidance on: branch naming conventions, commit message format, code review process, merge strategy, or how the two-branch model (FleetIQ / FleetFocus) is managed. The branch name `multi-customer-sync-to-master` is descriptive but no document explains the branching model or the relationship between branches.
- **Recommendation:** Document the branching strategy and contribution workflow, especially how changes are (or are not) synced between FleetIQ and FleetFocus branches.

---

### P0-10 — Legacy Visual SourceSafe metadata committed

- **Severity:** INFO
- **Category:** Process > Legacy artifacts
- **Status:** Carried forward from 2026-02-25-02 — unresolved
- **File:** `.gitattributes` (lines 6, 22, 29, 33)
- **Description:** `.gitattributes` explicitly lists `vssver2.scc` files in four locations (`WEB-INF/classes/META-INF/`, `.../master/`, `.../reports/`, `.../security/`). These are Visual SourceSafe tracking files, indicating migration from VSS. The `com.torrent.surat.fms6` package namespace is itself a legacy artifact (Torrent company, Surat location) with no documented relationship to current product names (FleetIQ, FleetFocus, CIG).
- **Recommendation:** Remove `vssver2.scc` files from the repository and `.gitattributes`. Add `*.scc` to `.gitignore`. Consider documenting the migration history and legacy package naming in the README.

---

### P0-11 — `index.jsp` JavaScript fallback silently fails

- **Severity:** INFO
- **Category:** Process > Broken redirect logic in landing page
- **File:** `index.jsp` (line 10)
- **Description:** `index.jsp` uses two redirect mechanisms: a `<meta http-equiv="REFRESH">` on line 4 (works correctly) and a JavaScript fallback function `send()` called via `<body onLoad="send()">`. The JavaScript function contains `location.href(url)` on line 10. `location.href` is a string property, not a function — this call throws a `TypeError: location.href is not a function` at runtime in all browsers. The function body is unreachable past this error. The meta-refresh still works, so the page redirects correctly in practice, but any browser that processes the `onLoad` event before the meta-refresh fires will log a JavaScript error. Combined with the malformed HTML (`<head>` never explicitly closed, orphan `</div>` on line 22), the landing page has accumulated unaddressed defects. While these do not block operation today, they indicate the page has not been reviewed against the current state of the application.
- **Recommendation:** Fix `location.href(url)` to `location.href = url` or `window.location.replace(url)`. Fix malformed HTML. These are trivial to correct.

---

## Summary

| ID | Severity | Finding | Status |
|---|---|---|---|
| P0-1 | MEDIUM | No CLAUDE.md — future sessions have no project guidance | Carry-forward, unresolved |
| P0-2 | MEDIUM | No README.md — no build, run, or deployment documentation | Carry-forward, unresolved |
| P0-3 | MEDIUM | No build manifest — IDE-dependent build undocumented and unreproducible | Carry-forward, unresolved |
| P0-4 | LOW | Empty Jenkinsfile — ambiguous CI/CD state | Carry-forward, unresolved |
| P0-5 | LOW | .gitignore inconsistencies with tracked IDE files | Carry-forward, unresolved |
| P0-6 | LOW | Project identity inconsistency across five names | Carry-forward, unresolved |
| P0-7 | LOW | Ambiguous "USE THIS FOR UK ONLY" comment on active HTTPS constraint | Carry-forward, unresolved |
| P0-8 | LOW | `web - Copy.xml` vs `web.xml` have materially different security config (session timeout, servlet inventory, spec version) | Enhanced from prior run |
| P0-9 | INFO | No contributing or workflow documentation | Carry-forward, unresolved |
| P0-10 | INFO | Legacy VSS metadata and undocumented package namespace | Carry-forward, unresolved |
| P0-11 | INFO | `index.jsp` JavaScript fallback silently throws TypeError | New finding |

**Totals:** 0 CRITICAL, 0 HIGH, 3 MEDIUM, 4 LOW, 3 INFO

**Note:** No process documents were created or modified between the 2026-02-25 audit runs and this run. All MEDIUM and LOW findings from prior runs remain open.
