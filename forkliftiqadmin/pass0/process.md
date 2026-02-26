# Pass 0: Process Review — forkliftiqadmin
**Date:** 2026-02-26
**Run:** 01
**Branch audited:** master

---

## Files Reviewed

### CLAUDE.md
- Does not exist.

### README.md
- Does not exist.

### bitbucket-pipelines.yml (5 lines)
- Single `default` pipeline
- One step: `mvn -B verify`
- No named stages, no deployment step, no profile flag
- Image: `maven:3.6.1`

### pom.xml (384 lines)
- groupId: `com.collectiveintelligence`
- artifactId/name: `pandoraAdmin`
- version: `1.0.0-SNAPSHOT`
- packaging: `war`
- Profiles: `local` (not default), `dev` (not default), `uat` (**default**), `prod` (not default)
- Build filter: `environment.${env}.properties`
- Plugins: `maven-eclipse-plugin 2.9`, `maven-compiler-plugin 2.5.1` (source/target 1.8), `maven-war-plugin 3.2.2`, `tomcat7-maven-plugin 2.2`
- Framework dependencies: `struts-core 1.3.10`, `struts-taglib 1.3.10`, `struts-tiles 1.3.10`, `spring-web 4.0.2.RELEASE`
- 38 dependencies total

### settings.xml (17 lines)
- Two `<server>` entries: `TomcatServerUat` and `TomcatServerAzure`
- Both contain plaintext `<username>` and `<password>` values
- File is committed to the repository (not in .gitignore)

### .gitignore (4 lines)
- Ignores: `/target/`, `.idea/`, `*.iml`, `environment.local.properties`

### environment.dev.properties (1 line)
- `logDir=/var/local/pandora/logs`

### environment.prod.properties (1 line)
- `logDir=/var/local/pandora/logs`

### environment.uat.properties (1 line)
- `logDir=/var/local/pandora/logs`

### environment.local.properties.template (1 line)
- `logDir=/home/gmtp/pandora/logs`

### .project (Eclipse metadata)
- Project name: `pandoraadmin`
- Natures: JDT, Spring IDE, m2e, WTP (JavaScript, WEB, ModuleCore)

### .tomcatplugin (Tomcat IDE plugin config)
- `<webPath>/BHAG</webPath>`
- `<reloadable>true</reloadable>`
- `<updateXml>true</updateXml>`

---

## Findings

---

### P0-1 — HIGH: Stack mislabeled as Java/Spring; application is Apache Struts

**File:** `pom.xml` (lines 128–139) and AUDIT-FRAMEWORK_legacy.md mapping table

The audit framework mapping table categorises `forkliftiqadmin` as **Java/Spring** and directs auditors to use the Java/Spring stack section and `PASS1-CHECKLIST-forkliftiq-spring.md`. That checklist instructs auditors to look for `SecurityConfig`, `WebSecurityConfigurerAdapter`, `@RestController`, `@RequestMapping`, `@PreAuthorize`, JWT configuration, and Spring Security filter chains.

The actual framework declared in `pom.xml` is **Apache Struts 1.3.10** (`struts-core`, `struts-taglib`, `struts-tiles`). The only Spring dependency is `spring-web 4.0.2.RELEASE`. There is no Spring Security, no Spring MVC, and no Spring Boot. The security and architecture patterns for a Struts 1.x application are fundamentally different from a Spring application.

A future auditor following the checklist will spend time searching for artefacts that do not exist (Spring Security filter chains, JWT signing keys, `@Secured` annotations) and will likely miss the actual authentication mechanism, which will be in Struts `Action` classes and XML configuration (`struts-config.xml`, `web.xml`).

**Recommendation:** Update the audit framework mapping table to label `forkliftiqadmin` as **Java/Struts** and create a Struts-specific audit checklist. At minimum, add a note to the existing checklist that this application uses Struts, not Spring MVC/Security.

---

### P0-2 — HIGH: UAT is the active-by-default Maven profile

**File:** `pom.xml` (lines 39–48)

The `uat` Maven profile has `<activeByDefault>true</activeByDefault>`. Running any Maven lifecycle command without an explicit `-P` flag (e.g., `mvn clean install`, `mvn package`, `mvn verify`) will activate the UAT profile. This has two consequences:

1. **Unintended deployment risk:** The UAT profile sets `tomcat.url` to a live UAT server URL (`http://ec2-54-86-82-22.compute-1.amazonaws.com:8080/manager/text`) and `tomcat.server` to `TomcatServerUat`. An AI session instructed to "build and deploy the application" using standard Maven commands will deploy to the live UAT server without any warning.

2. **CI pipeline deploys to UAT by default:** `bitbucket-pipelines.yml` runs `mvn -B verify` with no profile flag, so CI builds operate against the UAT profile silently.

There is no documentation noting this behaviour.

**Recommendation:** Remove `<activeByDefault>true</activeByDefault>` from the `uat` profile. Default to `local` or omit a default entirely and require explicit profile selection. Document the profile selection requirement in a README.

---

### P0-3 — HIGH: `settings.xml` committed to repository contains plaintext Tomcat credentials

**File:** `settings.xml` (lines 8–15)

`settings.xml` contains plaintext passwords for two Tomcat server entries:
- `TomcatServerUat`: `username=maven`, `password=C!1admin`
- `TomcatServerAzure`: `username=maven`, `password=pyx1s!96`

Maven's `settings.xml` is a local developer configuration file (conventionally at `~/.m2/settings.xml`). Committing it to the repository exposes credentials in version history to anyone with repository access.

This file is not listed in `.gitignore`. A future AI session working on build or deployment tasks will read this file and have unreviewed access to these credentials. *(Primary remediation belongs in Pass 1; flagged here as a process concern because the workflow implicitly requires committing credentials.)*

**Recommendation:** Remove `settings.xml` from the repository, add it to `.gitignore`, and supply credentials via environment variables or a secrets manager injected at build time.

---

### P0-4 — MEDIUM: No CLAUDE.md — no project-specific guidance for AI sessions

**File:** none (absent)

There is no `CLAUDE.md` in the repository. The audit framework assumes a `CLAUDE.md` exists and instructs auditors to "Check CLAUDE.md for project-specific security concerns" (SKILL-Audit-0Intro.md, Pass 1 section) and "Check CLAUDE.md for project conventions on test file location" (Pass 2 section).

Without a `CLAUDE.md`, future AI sessions have no project-specific context:
- No description of the application's purpose, expected users, or trust model
- No note that the framework is Struts 1.x, not Spring
- No deployment conventions or environment guidance
- No known security constraints or sensitive data categories
- No test conventions or known gaps

Audit instructions referencing `CLAUDE.md` will silently find nothing and proceed without the context those instructions assume exists.

**Recommendation:** Create `CLAUDE.md` documenting the application's purpose, tech stack (Struts 1.x on Tomcat), deployment environments, test conventions, and any known security-sensitive areas.

---

### P0-5 — MEDIUM: No README.md — no setup or workflow documentation

**File:** none (absent)

There is no `README.md`. There is no documented explanation of:
- What the application does
- How to build it (`mvn clean install -P local`)
- Which Maven profile to use for local development
- How environment properties files work
- How to configure a local `settings.xml`
- What `environment.local.properties` should contain

An AI session asked to "set up and build the project" has no starting point and will have to reverse-engineer the build process from `pom.xml`.

**Recommendation:** Add a README documenting build steps, profile usage, local configuration, and deployment workflow.

---

### P0-6 — MEDIUM: Branch name `master` does not match audit framework specification `main`

**File:** AUDIT-FRAMEWORK_legacy.md (mapping table row for `forkliftiqadmin`)

The audit framework specifies: *"Before beginning any pass, verify you are on the correct branch. Auditing the wrong branch invalidates all findings."* The mapping table lists `main` as the branch for `forkliftiqadmin`. The repository's actual branch is `master`.

A future auditor following the framework strictly will attempt to check out `main`, find it does not exist, and either fail or proceed on the wrong branch. The instruction "if the branch column says 'main', use the repository's default branch" (AUDIT-FRAMEWORK_legacy.md, Universal rules) partially mitigates this, but only if the auditor reads that caveat carefully — under context compression this distinction may be lost.

**Recommendation:** Update the audit framework mapping table to specify `master` for `forkliftiqadmin`, or rename the branch in the repository.

---

### P0-7 — LOW: Repository name, Eclipse project name, and Maven artifact name are all different

**Files:** `.project` (line 3), `pom.xml` (lines 7–8), repository directory name

- Repository directory: `forkliftiqadmin`
- Eclipse project name (`.project`): `pandoraadmin`
- Maven artifactId/name (`pom.xml`): `pandoraAdmin`
- Tomcat web path (`.tomcatplugin`): `/BHAG`

A future AI session searching for references to the application by its git directory name (`forkliftiq`) will find nothing in source files, which all use `pandora`. Conversely, a session searching for `pandora` will not immediately connect it to the `forkliftiqadmin` repo.

**Recommendation:** Document the `pandora` internal name in `CLAUDE.md` and `README.md`. Align names if a refactor is planned.

---

### P0-8 — LOW: `prod` Maven profile has an empty `<tomcat.url>`

**File:** `pom.xml` (lines 52–58)

The `prod` profile defines `<tomcat.url></tomcat.url>` (empty string). Running a Maven deploy with `-P prod` will attempt to deploy to an empty URL and fail with a confusing error rather than a clear "production deployment not configured" message.

There is no documentation noting that prod deployment is intentionally unconfigured or explaining how it is performed.

**Recommendation:** Either populate the prod URL, remove the `<tomcat.url>` property from the prod profile if prod deployment is handled separately, or add a comment explaining why it is empty.

---

### P0-9 — LOW: `environment.dev.properties`, `environment.prod.properties`, and `environment.uat.properties` are identical

**Files:** `environment.dev.properties`, `environment.prod.properties`, `environment.uat.properties` (line 1 of each)

All three environment-specific property files contain the same single value:
```
logDir=/var/local/pandora/logs
```

This makes them functionally identical. A future session (or developer) reading these files cannot determine whether the identical content is intentional (the log path genuinely does not vary) or whether the dev/uat/prod files are stale copies that were never differentiated. The purpose of the environment profile system is to inject environment-specific configuration — having three identical files suggests the system is not being used as intended.

**Recommendation:** Add a comment to each file confirming the identical path is intentional, or differentiate the paths if they should be different.

---

### P0-10 — LOW: `bitbucket-pipelines.yml` is an unmodified Atlassian template

**File:** `bitbucket-pipelines.yml` (lines 1–4)

The file retains the Atlassian template comment "This is a sample build configuration for Java (Maven)" and "Modify the commands below to build your repository." The build step (`mvn -B verify`) matches the template default exactly. There is no deployment step, no profile flag, no branch-conditional logic, and no notification or artifact step.

This suggests the pipeline was never properly configured. A future session asked to "check if CI is set up correctly" may conclude it is, since the file exists and `mvn verify` is a valid command — but the pipeline has no deployment capability and will use the UAT profile silently (see P0-2).

**Recommendation:** Replace the template with a configured pipeline: correct Maven profile, a deployment stage for UAT/prod, and removal of the template boilerplate comments.

---

### P0-11 — INFO: Eclipse IDE files committed and not gitignored

**Files:** `.project`, `.classpath`, `.settings/`, `.tomcatplugin`

Eclipse project metadata files are committed to the repository. They are not excluded by `.gitignore`. These files:
- Encode developer-specific Eclipse paths and project configuration
- Contain the project name `pandoraadmin` which conflicts with other names (P0-7)
- Include the Tomcat web path `/BHAG` (`.tomcatplugin`) which is not documented anywhere
- Can cause merge conflicts for developers using different Eclipse versions

**Recommendation:** Add `.project`, `.classpath`, `.settings/`, and `.tomcatplugin` to `.gitignore`. Document the web path (`/BHAG`) in README.
