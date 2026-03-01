# Repository Inventory — ff-new (FleetIQ)
**Branch:** multi-customer-sync-to-master
**Date:** 2026-03-01

---

## Directory Structure (first two levels)

```
fleetiq/                        (root)
├── .classpath                  (Eclipse IDE project file)
├── .project                    (Eclipse IDE project file)
├── Jenkinsfile                 (empty — 0 bytes)
├── index.jsp
├── RemoteSystemsTempFiles/     (Eclipse Remote Systems plugin artefact)
├── WEB-INF/
│   ├── lib/                    (38 committed JAR dependencies)
│   └── src/                    (Java source tree)
├── audit/                      (audit working directory — not application code)
│   ├── 2026-02-25-01/
│   ├── 2026-02-25-02/
│   └── 2026-03-01-01/
├── au_email/                   (JSP module — email)
├── au_excel/                   (JSP module — Excel export)
├── au_print/                   (JSP module — print)
├── css/                        (application stylesheets)
├── dashboard/
│   ├── css/
│   ├── js/
│   ├── jsp/
│   └── webfonts/
├── doc/                        (CSV/XLSX import templates and sample data)
├── dyn_report/                 (JSP dynamic report module)
├── exporter/                   (JSP exporter module)
├── files/                      (binary user-facing assets: PDF manuals, MP4 videos)
├── gps/                        (GPS-related JSP pages)
├── images/
│   ├── gpsIcons/
│   ├── linde/
│   └── pics/
├── impactimg/                  (impact image assets)
├── import_template/            (import template files)
├── includes/                   (shared JSP includes)
├── js/
│   ├── DataTables-1.10.1/
│   ├── blitzer/
│   ├── dataTables/
│   └── flot/
├── layout/                     (JSP layout templates)
├── master/                     (master/admin JSP pages)
├── menu/                       (JSP menu module)
├── pages/
│   ├── admin/
│   └── bundle/                 (i18n message bundles)
├── reports/                    (JSP report pages)
├── security/                   (JSP security/login pages)
├── sess/                       (session-related JSP pages)
├── skin/
│   ├── css/
│   ├── fonts/
│   ├── images/
│   └── js/
├── sql/                        (committed SQL scripts and stored procedures)
└── work/
    └── org/apache/jsp/         (2 pre-compiled Tomcat JSP .class files — stale artefacts)
```

---

## Binary Artifacts

### JAR files
38 JARs, all located under `WEB-INF/lib/`. No other JAR locations found.

| File | Size |
|------|------|
| WEB-INF/lib/poi-ooxml-schemas-3.9-20121203.jar | 4.6 MB |
| WEB-INF/lib/xmlbeans-2.3.0.jar | 2.6 MB |
| WEB-INF/lib/poi-3.9-20121203.jar | 1.8 MB |
| WEB-INF/lib/log4j-core-2.17.0.jar | 1.8 MB |
| WEB-INF/lib/itextpdf-5.4.2.jar | 1.9 MB |
| WEB-INF/lib/jfreechart-1.0.19.jar | 1.5 MB |
| WEB-INF/lib/javamelody.jar | 978 KB |
| WEB-INF/lib/poi-ooxml-3.9-20121203.jar | 915 KB |
| WEB-INF/lib/postgresql-8.3-603.jdbc4.jar | 464 KB |
| WEB-INF/lib/httpclient-4.2.3.jar | 423 KB |
| WEB-INF/lib/jsoup-1.12.1.jar | 388 KB |
| WEB-INF/lib/jstl-1.2.jar | 405 KB |
| WEB-INF/lib/urlrewritefilter-4.0.3.jar | 174 KB |
| WEB-INF/lib/log4j-api-2.17.0.jar | 295 KB |
| WEB-INF/lib/commons-lang-2.6.jar | 278 KB |
| WEB-INF/lib/dom4j-1.6.1.jar | 307 KB |
| WEB-INF/lib/commons-collections-3.1.jar | 547 KB |
| WEB-INF/lib/commons-codec-1.6.jar | 228 KB |
| WEB-INF/lib/commons-net-2.0.jar | 193 KB |
| WEB-INF/lib/commons-net-1.4.1.jar | 177 KB |
| WEB-INF/lib/charts4j-1.3.jar | 180 KB |
| WEB-INF/lib/gson-2.8.5.jar | 236 KB |
| WEB-INF/lib/joda-time-2.10.4.jar | 628 KB |
| WEB-INF/lib/json-20180813.jar | 64 KB |
| WEB-INF/lib/httpcore-4.2.2.jar | 219 KB |
| WEB-INF/lib/jcommon-0.9.5.jar | 322 KB |
| WEB-INF/lib/jfreesvg-2.0.jar | 50 KB |
| WEB-INF/lib/jfreechart-1.0.19-swt.jar | 78 KB |
| WEB-INF/lib/jbcrypt-0.3m.jar | 18 KB |
| WEB-INF/lib/stax-api-1.0.1.jar | 26 KB |
| WEB-INF/lib/taglibs-mailer.jar | 28 KB |
| WEB-INF/lib/taglibs-request.jar | 39 KB |
| WEB-INF/lib/trimflt.jar | 3.9 KB |
| WEB-INF/lib/commons-logging.jar | 52 KB |
| WEB-INF/lib/commons-logging-1.1.1.jar | 60 KB |
| WEB-INF/lib/commons-io-1.1.jar | 61 KB |
| WEB-INF/lib/commons-fileupload-1.1.jar | 32 KB |
| WEB-INF/lib/junit-3.8.1.jar | 119 KB |

**Total WEB-INF/lib: ~22 MB**

### WAR files
None found in the repository. The project deploys as an exploded web application directory, not a packaged WAR.

### CLASS files
2 pre-compiled JSP class files present (stale Tomcat work-directory artefacts committed to the repository):

| File | Size |
|------|------|
| work/org/apache/jsp/pages/admin/setting/driver_005fsettings_005fto_005funit_jsp.class | ~40 KB |
| work/org/apache/jsp/pages/admin/setting/driver_005flimiting_005fby_005ftruck_jsp.class | ~40 KB |

No compiled application classes exist under `WEB-INF/classes/`; compilation output directory is declared in `.classpath` but the directory contains no committed `.class` files.

### ZIP files
None found.

---

## Configuration Files

### Web Application Descriptors (WEB-INF/)
| File | Notes |
|------|-------|
| WEB-INF/web.xml | Primary servlet deployment descriptor; Servlet 3.0 schema (`web-app_3_0.xsd`); declares servlets mapped under `/servlet/*` |
| WEB-INF/web - Copy.xml | Apparent working copy / backup of web.xml — should not be committed |
| WEB-INF/urlrewrite.xml | Tuckey UrlRewriteFilter 4.0 rules |

No `context.xml` or `server.xml` present in the repository (these reside on the server, not in the webapp).

### Logging Configuration
| File | Notes |
|------|-------|
| WEB-INF/src/log4j.properties | Legacy Log4j 1.x properties file |
| WEB-INF/src/log4j2.properties | Log4j 2.x properties file (matches committed log4j-core-2.17.0.jar) |

### Internationalisation / Resource Bundles (.properties)
| File |
|------|
| WEB-INF/src/main/resource/Messages.properties |
| WEB-INF/src/main/resource/Messages_en.properties |
| WEB-INF/src/main/resource/Messages_en_US.properties |
| WEB-INF/src/main/resource/Messages_es.properties |
| WEB-INF/src/main/resource/Messages_zh.properties |
| WEB-INF/src/main/resource/Messages_zh_CN.properties |
| pages/bundle/Messages.properties |
| pages/bundle/Messages_en.properties |
| pages/bundle/Messages_en_US.properties |
| pages/bundle/Messages_es.properties |
| pages/bundle/Messages_zh.properties |
| pages/bundle/Messages_zh_CN.properties |

### IDE Project Files (not deployment configuration but relevant to build understanding)
| File | Notes |
|------|-------|
| .classpath | Eclipse classpath; references `CATALINA_HOME` variable for `jasper.jar`, `jsp-api.jar`, `servlet-api.jar`, `mail.jar`; JDK target: `jdk1.8.0_261` |
| .project | Eclipse project named "MULTI"; nature `com.sysdeo.eclipse.tomcat.tomcatnature` (Sysdeo Tomcat plugin) |

---

## Build System

**IDE-dependent (Eclipse + Sysdeo Tomcat Plugin)**

There is no `pom.xml` (Maven), `build.xml` (Ant), `build.gradle` (Gradle), or any other standalone build script present. The project is built exclusively through the Eclipse IDE using:

- `org.eclipse.jdt.core.javabuilder` (Java incremental compiler)
- `com.sysdeo.eclipse.tomcat.tomcatnature` (Sysdeo Eclipse Tomcat Plugin for direct deployment to a local Tomcat server)
- `.classpath` manually enumerates all 38 library JARs and references `CATALINA_HOME` for server-provided libraries

The `Jenkinsfile` is present but is empty (0 bytes), providing no CI/CD pipeline definition.

The Eclipse project name is "MULTI", consistent with the branch name `multi-customer-sync-to-master`.

---

## Size Breakdown

| Category | Contents | Approximate Size |
|----------|----------|-----------------|
| **Binary assets (user-facing)** | `files/` — PDF manuals, MP4 training videos | ~137 MB |
| **Binary assets (UI)** | `skin/` — fonts, images, bundled JS/CSS | ~28 MB |
| **Images** | `images/` — GPS icons, product images | ~31 MB |
| **Third-party JARs** | `WEB-INF/lib/` (38 JARs) | ~22 MB |
| **JavaScript libraries** | `js/` — DataTables, Flot, jQuery, dataTables | ~12 MB |
| **Java source code** | `WEB-INF/src/` (268 .java files) | ~7 MB |
| **JSP pages** | All modules (728 .jsp files across pages/, master/, reports/, dashboard/, etc.) | ~15 MB (est. from directory totals) |
| **Data / templates** | `doc/` + `sql/` — CSV/XLSX templates, SQL scripts, stored procedures | ~2 MB |
| **Compiled artefacts** | `work/` — 2 stale JSP .class files | <1 MB |
| **Total repository** | | ~444 MB |

**Summary:**
- Source code (Java + JSP): ~22 MB (~5% of total)
- Third-party library JARs: ~22 MB (~5%)
- Binary / media assets (PDF, MP4, images, fonts): ~196 MB (~44%)
- Front-end libraries and CSS (skin, js): ~40 MB (~9%)
- Data and SQL files: ~2 MB (<1%)
- Remaining (misc modules, config): ~162 MB (~37%)

The repository is dominated by committed binary assets (training videos and PDFs in `files/`) and image/font assets — atypical for source control and inflating the repository significantly.

---

## Tomcat Version

**Not determinable precisely from committed files; estimated Tomcat 8.x or 9.x.**

Indicators:

1. **`web.xml` declares Servlet 3.0** (`web-app_3_0.xsd`). Servlet 3.0 is supported by Tomcat 7.x and later.
2. **`.classpath` references `CATALINA_HOME/lib/jasper.jar`** — the Jasper JSP compiler is bundled with Tomcat and provided at runtime, not committed.
3. **`.project` uses `com.sysdeo.eclipse.tomcat.tomcatnature`** — the Sysdeo plugin supports Tomcat 5.5 through 9.x; no version-pinning is present.
4. **`work/org/apache/jsp/`** — this is Tomcat's standard JSP work-directory layout; the two committed `.class` files are Tomcat-compiled JSPs. No version string is embedded in the class file bytecode in a readable form.
5. **No `server.xml`, `catalina.sh`, or Tomcat distribution** is committed to the repository.
6. **JDK target is `jdk1.8.0_261`** (Java 8), which is compatible with Tomcat 8.5 or 9.0; Tomcat 10+ requires Java 11+.

**Best estimate: Tomcat 8.5 or 9.0**, based on Servlet 3.0/3.1 descriptor, Java 8 JDK target, and absence of Jakarta EE namespace migration (which would be required for Tomcat 10+). The exact version cannot be confirmed without examining the server installation or deployment documentation.
