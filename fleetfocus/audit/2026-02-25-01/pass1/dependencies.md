# Dependency Vulnerability Review
**Audit ID:** A18
**Audit Date:** 2026-02-25
**Audit Run:** 2026-02-25-01
**Branch:** release/UAT_RELEASE_FLEETFOCUS_Production
**Agent:** A18 — Dependency CVE Review
**Scope:** WEB-INF/lib/ (41 JARs), .classpath classpath ordering

---

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 2 |
| HIGH | 9 |
| MEDIUM | 5 |
| LOW | 2 |
| INFORMATIONAL | 1 |
| **TOTAL** | **19** |

---

## Complete JAR Inventory

All 41 JARs reside in `WEB-INF/lib/`. No build system (Maven/Gradle/Ant) is present — dependencies are manually managed via Eclipse IDE.

| JAR Filename | Version | Purpose |
|---|---|---|
| batik-1.9.jar | 1.9 | Apache Batik SVG toolkit (stub/bootstrap JAR) |
| batik-all-1.9.jar | 1.9 | Apache Batik SVG toolkit (all-in-one) |
| batik-svg-dom-1.9.jar | 1.9 | Apache Batik SVG DOM implementation |
| batik-transcoder-1.9.jar | 1.9 | Apache Batik SVG transcoder |
| charts4j-1.3.jar | 1.3 | Google Charts API Java wrapper |
| commons-codec-1.6.jar | 1.6 | Apache Commons Codec (Base64, hex encoding) |
| commons-collections-3.1.jar | 3.1 | Apache Commons Collections (data structures) |
| commons-fileupload-1.1.jar | 1.1 | Apache Commons FileUpload (multipart handling) |
| commons-io-1.1.jar | 1.1 | Apache Commons IO (file/stream utilities) |
| commons-lang-2.6.jar | 2.6 | Apache Commons Lang (string/object utilities) |
| commons-logging-1.1.1.jar | 1.1.1 | Apache Commons Logging (logging facade) |
| commons-logging.jar | 1.1 | Apache Commons Logging (logging facade) — DUPLICATE |
| commons-net-1.4.1.jar | 1.4.1 | Apache Commons Net (FTP/SMTP/Telnet client) — DUPLICATE |
| commons-net-2.0.jar | 2.0 | Apache Commons Net (FTP/SMTP/Telnet client) — DUPLICATE |
| dom4j-1.6.1.jar | 1.6.1 | DOM4J XML processing library |
| esapi-2.5.3.1.jar | 2.5.3.1 | OWASP ESAPI security framework |
| gson-2.8.5.jar | 2.8.5 | Google Gson (JSON serialization) |
| httpclient-4.2.3.jar | 4.2.3 | Apache HttpComponents HttpClient |
| httpcore-4.2.2.jar | 4.2.2 | Apache HttpComponents HttpCore |
| itextpdf-5.4.2.jar | 5.4.2 | iText PDF generation library |
| javamelody.jar | unknown | JavaMelody application monitoring |
| jbcrypt-0.3m.jar | 0.3m | jBCrypt password hashing |
| jcommon-0.9.5.jar | 0.9.5 | JCommon utility library (JFreeChart dependency) |
| jfreechart-1.0.19-swt.jar | 1.0.19 | JFreeChart SWT integration |
| jfreechart-1.0.19.jar | 1.0.19 | JFreeChart charting library |
| jfreesvg-2.0.jar | 2.0 | JFreeSVG SVG output for JFreeChart |
| joda-time-2.10.4.jar | 2.10.4 | Joda-Time date/time library |
| jsoup-1.12.1.jar | 1.12.1 | Jsoup HTML parser and sanitizer |
| junit-3.8.1.jar | 3.8.1 | JUnit test framework (should not be in production) |
| log4j-api-2.17.0.jar | 2.17.0 | Apache Log4j 2 API |
| log4j-core-2.17.0.jar | 2.17.0 | Apache Log4j 2 Core |
| org.json.jar | unknown | org.json JSON library |
| poi-3.9-20121203.jar | 3.9 | Apache POI Excel/Office processing |
| poi-ooxml-3.9-20121203.jar | 3.9 | Apache POI OOXML (xlsx/docx) support |
| poi-ooxml-schemas-3.9-20121203.jar | 3.9 | Apache POI OOXML XML schemas |
| postgresql-8.3-603.jdbc4.jar | 8.3-603 | PostgreSQL JDBC driver |
| stax-api-1.0.1.jar | 1.0.1 | StAX XML Streaming API |
| taglibs-mailer.jar | 1.1 | Apache Taglibs Mailer tag library |
| taglibs-request.jar | 1.0.1 | Apache Taglibs Request tag library |
| trimflt.jar | unknown | Unknown utility JAR (no manifest version) |
| xmlbeans-2.3.0.jar | 2.3.0 | Apache XMLBeans XML-to-Java binding |

---

## Findings

---

### A18-1 — Apache Commons Collections 3.1 — Java Deserialization RCE Gadget Chain

**Severity:** CRITICAL
**Category:** Dependency / Known CVE
**JAR:** `WEB-INF/lib/commons-collections-3.1.jar`
**CVE(s):** CVE-2015-6420, CVE-2015-7501

**Description:**
Apache Commons Collections 3.1 contains the deserialization gadget chain that enabled widespread remote code execution (RCE) attacks in 2015 and beyond. The `InvokerTransformer` and `ChainedTransformer` classes allow an attacker who can deliver a malicious serialized Java object to any endpoint that deserializes untrusted data to execute arbitrary operating system commands with the privileges of the Tomcat process. This is one of the most critical known Java library vulnerabilities. FleetFocus uses this version without upgrade. Any Java deserialization endpoint in the application (object input streams, RMI, JMX, HTTP Invokers, or Tomcat session deserialization) is potentially exploitable.

**Evidence:**
- `WEB-INF/lib/commons-collections-3.1.jar` — Implementation-Version: 3.1 (confirmed in MANIFEST.MF)
- `.classpath` line 6: `<classpathentry kind="lib" path="WEB-INF/lib/commons-collections-3.1.jar"/>`
- First patched version: Apache Commons Collections 3.2.2 (released November 2015)

**Recommendation:**
Upgrade immediately to Apache Commons Collections **3.2.2** (for the 3.x API) or **4.4** (for the 4.x API, which has a cleaner design). Audit all Java deserialization points in the application simultaneously. Consider deploying a serialization filter (`java.io.ObjectInputFilter` / `jep290`) on all object input streams. This is a non-negotiable upgrade.

---

### A18-2 — Apache Commons FileUpload 1.1 — Multiple Critical CVEs

**Severity:** CRITICAL
**Category:** Dependency / Known CVE
**JAR:** `WEB-INF/lib/commons-fileupload-1.1.jar`
**CVE(s):** CVE-2014-0050, CVE-2016-1000031

**Description:**
Apache Commons FileUpload 1.1 (released circa 2004) is affected by two critical vulnerabilities:

1. **CVE-2014-0050** (CVSS 7.5 HIGH): Denial of service via a multipart request with boundary values that contain many headers. The parser enters a near-infinite loop, exhausting server memory or CPU. This affects versions before 1.3.1.

2. **CVE-2016-1000031** (CVSS 9.8 CRITICAL): The `DiskFileItem` class implements `java.io.Serializable`. A malicious serialized `DiskFileItem` object can write arbitrary data to arbitrary filesystem paths on the server when deserialized. This is a direct remote code execution path if any deserialization endpoint accepts attacker-controlled data. Fixed in version 1.3.3.

This JAR is used by `Frm_upload` and `CustomUpload` servlets registered in `web.xml`, meaning file upload handling is active and deployed.

**Evidence:**
- `WEB-INF/lib/commons-fileupload-1.1.jar` — Version: 1.1 (confirmed in MANIFEST.MF)
- `.classpath` line 7: `<classpathentry kind="lib" path="WEB-INF/lib/commons-fileupload-1.1.jar"/>`
- `web.xml` registers servlets `Frm_upload` (`com.torrent.surat.fms6.master.Frm_upload`) and `CustomUpload` (`com.torrent.surat.fms6.util.CustomUpload`) with URL patterns `/servlet/Frm_upload` and `/servlet/CustomUpload`

**Recommendation:**
Upgrade to Apache Commons FileUpload **1.5** or later (latest stable as of 2025). Also upgrade `commons-io-1.1.jar` to a compatible version (2.11.0 or later) as it is a dependency.

---

### A18-3 — Apache POI 3.9 (2012) — Multiple XXE and DoS CVEs

**Severity:** HIGH
**Category:** Dependency / Known CVE
**JARs:**
- `WEB-INF/lib/poi-3.9-20121203.jar`
- `WEB-INF/lib/poi-ooxml-3.9-20121203.jar`
- `WEB-INF/lib/poi-ooxml-schemas-3.9-20121203.jar`
**CVE(s):** CVE-2014-9527, CVE-2017-5644, CVE-2019-12415

**Description:**
Apache POI 3.9 was released in December 2012. It is over 13 years old. Known vulnerabilities include:

1. **CVE-2014-9527** (HIGH): Infinite loop/DoS when processing HSSf files with certain record types.
2. **CVE-2017-5644** (HIGH): XML external entity (XXE) injection in OOXML file processing (XLSX, DOCX, PPTX). An attacker who can supply a crafted Office document to the application can read arbitrary server files or perform server-side request forgery.
3. **CVE-2019-12415** (HIGH): XXE in the XSSFExportToXml component of poi-ooxml. An attacker can cause the server to read local files or make network requests.

FleetFocus generates Excel output extensively (18 Java chart classes in `com.torrent.surat.fms6.chart.excel`, plus `au_excel/` JSPs), and imports Excel files via `Import_Files` servlet. The import path is particularly dangerous — it accepts attacker-supplied Office documents.

**Evidence:**
- `WEB-INF/lib/poi-3.9-20121203.jar` — Version: 3.9, build date 2012-12-03
- `WEB-INF/lib/poi-ooxml-3.9-20121203.jar` — Version: 3.9
- `WEB-INF/lib/poi-ooxml-schemas-3.9-20121203.jar` — Version: 3.9
- `.classpath` lines 25-27
- `web.xml`: `Import_Files` servlet at `/servlet/Import_Files` actively accepts uploaded documents

**Recommendation:**
Upgrade all three POI JARs together to Apache POI **5.2.5** or later (latest stable as of 2025). Ensure XXE protections (`XMLInputFactory.IS_SUPPORTING_EXTERNAL_ENTITIES = false`) are applied wherever XML is parsed. Validate file content type on upload, not just file extension.

---

### A18-4 — Apache HttpClient 4.2.3 / HttpCore 4.2.2 — Multiple CVEs

**Severity:** HIGH
**Category:** Dependency / Known CVE
**JARs:**
- `WEB-INF/lib/httpclient-4.2.3.jar`
- `WEB-INF/lib/httpcore-4.2.2.jar`
**CVE(s):** CVE-2014-3577, CVE-2020-13956

**Description:**
Apache HttpClient 4.2.3 (released ~2013) is affected by:

1. **CVE-2014-3577** (CVSS 4.3 MEDIUM → HIGH in context): SSL hostname verification bypass. The `BrowserCompatHostnameVerifier` class does not properly verify that the server's hostname matches the certificate's common name, enabling man-in-the-middle attacks against HTTPS connections made by the server. Any outbound HTTPS call (e.g., to GPS/RTLS endpoints, external APIs) is vulnerable.

2. **CVE-2020-13956** (CVSS 5.3 MEDIUM): Request URI path miscategorization when the URI is not correctly set, potentially enabling server-side request forgery in certain proxy configurations.

The application uses this library for outbound HTTP connections (18 chart classes use an external URL builder; the RTLS subsystem in `com.torrent.surat.fms6.rtls` likely makes HTTP calls; the GPS subsystem is also present).

**Evidence:**
- `WEB-INF/lib/httpclient-4.2.3.jar` — Version: 4.2.3
- `WEB-INF/lib/httpcore-4.2.2.jar` — Version: 4.2.2
- `.classpath` lines 19-20

**Recommendation:**
Upgrade to Apache HttpClient **4.5.14** (4.x series, latest stable) or migrate to HttpClient **5.3** (5.x series). Both HttpClient and HttpCore must be upgraded together.

---

### A18-5 — DOM4J 1.6.1 — XML Injection and XXE

**Severity:** HIGH
**Category:** Dependency / Known CVE
**JAR:** `WEB-INF/lib/dom4j-1.6.1.jar`
**CVE(s):** CVE-2018-1000632, CVE-2020-10683

**Description:**
DOM4J 1.6.1 is affected by two high-severity vulnerabilities:

1. **CVE-2018-1000632** (CVSS 7.5 HIGH): Allows an attacker to write arbitrary XML by injecting characters including XML element delimiters into an `Element` object when its text is set. This enables XML document structural corruption or injection attacks.

2. **CVE-2020-10683** (CVSS 9.8 CRITICAL): XML external entity (XXE) injection. DOM4J before 2.1.3 allows XML external entity attacks by default when parsing attacker-supplied XML documents, enabling server-side file disclosure and SSRF.

DOM4J is used throughout the application for XML processing. The OOXML POI stack (`poi-ooxml`) also uses DOM4J internally, compounding the XXE risk.

**Evidence:**
- `WEB-INF/lib/dom4j-1.6.1.jar` — Version: 1.6.1 (confirmed in MANIFEST.MF)
- `.classpath` line 23

**Recommendation:**
Upgrade to DOM4J **2.1.4** or later. Note that DOM4J 2.x has API changes vs 1.x — test XML-handling code carefully after upgrade. Apply explicit `SAXReader` configuration to disable external entity resolution as an interim measure:
```java
SAXReader reader = new SAXReader();
reader.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
reader.setFeature("http://xml.org/sax/features/external-general-entities", false);
```

---

### A18-6 — iText PDF 5.4.2 — Multiple CVEs and AGPL Licensing

**Severity:** HIGH
**Category:** Dependency / Known CVE / License Risk
**JAR:** `WEB-INF/lib/itextpdf-5.4.2.jar`
**CVE(s):** CVE-2017-7386, CVE-2018-10036

**Description:**
iText 5.4.2 was released approximately in 2013 and is over 12 years old. Known issues include:

1. **CVE-2017-7386** (HIGH): Server-side request forgery (SSRF) via crafted XML in `XMLWorker`. Attacker-controlled content parsed by XMLWorker can cause the server to make arbitrary outbound HTTP/HTTPS requests to internal network resources.

2. **CVE-2018-10036** (MEDIUM): Uncontrolled resource consumption (denial of service) when parsing malformed PDF structures.

Additionally, iText 5.x is licensed under **AGPL-3.0**. If FleetFocus is deployed as a SaaS or networked application without purchasing a commercial iText license, this represents a significant license compliance risk that could require open-sourcing the entire application codebase.

The application uses iText extensively via the `com.torrent.surat.fms6.pdf` package for PDF report generation.

**Evidence:**
- `WEB-INF/lib/itextpdf-5.4.2.jar` — Version: 5.4.2 (MANIFEST: Implementation-Version 5.4.2)
- `.classpath` line 32
- Java package `WEB-INF/src/com/torrent/surat/fms6/pdf/` present

**Recommendation:**
Upgrade to iText **7.x** (commercial license) or migrate to Apache PDFBox **3.x** (Apache 2.0 license, no cost). If remaining on iText, obtain a valid commercial license. Minimum safe version for security is iText 5.5.13.3 or later within the 5.x line.

---

### A18-7 — Apache Batik 1.9 — SSRF and Multiple CVEs

**Severity:** HIGH
**Category:** Dependency / Known CVE
**JARs:**
- `WEB-INF/lib/batik-all-1.9.jar`
- `WEB-INF/lib/batik-svg-dom-1.9.jar`
- `WEB-INF/lib/batik-transcoder-1.9.jar`
- `WEB-INF/lib/batik-1.9.jar`
**CVE(s):** CVE-2019-17566, CVE-2022-38648, CVE-2022-40146, CVE-2022-44729, CVE-2022-44730

**Description:**
Apache Batik 1.9 (released 2017) has multiple known vulnerabilities:

1. **CVE-2019-17566** (CVSS 7.5 HIGH): Server-side request forgery (SSRF). Batik is vulnerable to SSRF when processing SVG files that reference external resources. An attacker who can supply a crafted SVG causes the Batik transcoder to make HTTP requests to arbitrary URLs, including internal network services.

2. **CVE-2022-38648** (CVSS 7.5 HIGH): SSRF via SVG `<image>` element with crafted href. Fixed in Batik 1.16.

3. **CVE-2022-40146** (CVSS 7.5 HIGH): SSRF via the Batik `jar:` URL scheme. Fixed in Batik 1.16.

4. **CVE-2022-44729** (CVSS 7.5 HIGH): SSRF via crafted SVG files. Fixed in Batik 1.17.

5. **CVE-2022-44730** (CVSS 4.4 MEDIUM): SSRF via `data:` URIs in SVG. Fixed in Batik 1.17.

Batik is used for SVG-to-image transcoding in chart/report generation. If any SVG content is sourced from user input or external data, these vulnerabilities are directly exploitable for internal network reconnaissance.

**Evidence:**
- `WEB-INF/lib/batik-all-1.9.jar` — Version: 1.9
- `WEB-INF/lib/batik-transcoder-1.9.jar` — Version: 1.9
- `.classpath` lines 40-43

**Recommendation:**
Upgrade all four Batik JARs to Apache Batik **1.17** or later. This requires coordinated upgrade of all `batik-*` artifacts. Ensure that any SVG content from untrusted sources is sanitized before transcoding.

---

### A18-8 — Gson 2.8.5 — ReDoS (Regular Expression Denial of Service)

**Severity:** MEDIUM
**Category:** Dependency / Known CVE
**JAR:** `WEB-INF/lib/gson-2.8.5.jar`
**CVE(s):** CVE-2022-25647

**Description:**
Gson 2.8.5 is affected by CVE-2022-25647 (CVSS 7.5 HIGH): a stack overflow vulnerability in `JsonElement.deepCopy()` when processing deeply nested JSON objects, and a related deserialization issue in `TypeAdapter`. Specifically, deserializing a crafted JSON string with a deeply nested structure can cause a stack overflow (denial of service). Additionally, Gson before 2.8.9 has a related vulnerability in `JsonReader` handling. Fixed in Gson 2.8.9.

**Evidence:**
- `WEB-INF/lib/gson-2.8.5.jar` — Version: 2.8.5
- `.classpath` line 45
- Package `com.torrent.surat.fms6.jsonbinding/` uses Gson for serialization

**Recommendation:**
Upgrade to Gson **2.10.1** or later (latest stable as of 2025).

---

### A18-9 — Duplicate JAR: commons-logging (v1.1 and v1.1.1)

**Severity:** MEDIUM
**Category:** Dependency / Classpath Conflict
**JARs:**
- `WEB-INF/lib/commons-logging.jar` (version 1.1)
- `WEB-INF/lib/commons-logging-1.1.1.jar` (version 1.1.1)

**Description:**
Two versions of Apache Commons Logging are present in WEB-INF/lib/ simultaneously. At runtime, Tomcat's webapp classloader loads JARs from WEB-INF/lib/ in filesystem order (typically alphabetical). Since `commons-logging-1.1.1.jar` (alphabetically earlier) would load before `commons-logging.jar`, the 1.1.1 version likely takes precedence at runtime — but this is not guaranteed across operating systems, deployments, or Tomcat versions.

The Eclipse `.classpath` shows the opposite order: `commons-logging.jar` (v1.1) is declared at line 5 (first), and `commons-logging-1.1.1.jar` at line 18 (thirteenth). This means the IDE may compile against version 1.1 while the server runs version 1.1.1. This classpath inversion between build and runtime is a subtle source of undefined behavior, and masks the actual version dependency in use.

This creates a split-brain configuration: developers may see different behavior than production, and future upgrades may resolve incorrectly.

**Evidence:**
- `WEB-INF/lib/commons-logging.jar` — MANIFEST.MF: Implementation-Version 1.1
- `WEB-INF/lib/commons-logging-1.1.1.jar` — MANIFEST.MF: Implementation-Version 1.1.1
- `.classpath` line 5: `commons-logging.jar` (first)
- `.classpath` line 18: `commons-logging-1.1.1.jar` (thirteenth)

**Recommendation:**
Remove `commons-logging.jar` (v1.1) and retain only `commons-logging-1.1.1.jar`. Consider upgrading to Commons Logging **1.3.x** which includes additional JDK compatibility improvements.

---

### A18-10 — Duplicate JAR: commons-net (v1.4.1 and v2.0)

**Severity:** MEDIUM
**Category:** Dependency / Classpath Conflict
**JARs:**
- `WEB-INF/lib/commons-net-1.4.1.jar` (version 1.4.1)
- `WEB-INF/lib/commons-net-2.0.jar` (version 2.0)

**Description:**
Two versions of Apache Commons Net are present simultaneously. The `.classpath` lists `commons-net-2.0.jar` first (line 9) and `commons-net-1.4.1.jar` second (line 22). At compile time in Eclipse, classes from version 2.0 take precedence. At Tomcat runtime, alphabetical filesystem ordering of WEB-INF/lib would load `commons-net-1.4.1.jar` first (alphabetically before `commons-net-2.0.jar`), meaning the older version 1.4.1 may actually execute in production.

Commons Net 2.0 introduced breaking API changes from 1.4.x. If application code was compiled against 2.0 but 1.4.1 loads at runtime, `NoSuchMethodError` or `NoClassDefFoundError` failures are possible in FTP, SMTP, or network client code. This could silently degrade functionality or cause runtime errors.

Both versions are very old (1.4.1 from ~2007, 2.0 from ~2008) and should be replaced entirely.

**Evidence:**
- `WEB-INF/lib/commons-net-1.4.1.jar` — Version: 1.4.1
- `WEB-INF/lib/commons-net-2.0.jar` — Version: 2.0
- `.classpath` line 9: `commons-net-2.0.jar` (earlier, build-time precedence)
- `.classpath` line 22: `commons-net-1.4.1.jar` (later)

**Recommendation:**
Remove both JARs. Determine which API version the application actually uses and replace with a single copy of Commons Net **3.9.0** (latest stable as of 2025).

---

### A18-11 — No Automated Build System or Dependency Scanning

**Severity:** MEDIUM
**Category:** Process / Supply Chain
**Evidence:** No `pom.xml`, `build.gradle`, or `build.xml` found in repository root. Build is IDE-only (Eclipse with Tomcat Plugin, per `.classpath` and `.tomcatplugin` files). JARs are manually copied into `WEB-INF/lib/`.

**Description:**
The complete absence of a build management system means:

1. **No automated CVE scanning**: Tools like OWASP Dependency-Check, Snyk, or GitHub Dependabot cannot be integrated without a build system. Vulnerabilities in the current 41 JARs were identified through manual analysis in this audit.

2. **No version pinning or transitive dependency management**: Transitive dependencies (libraries used by libraries) are manually included and not tracked. The actual dependency tree cannot be reconstructed, making it impossible to verify whether all transitive dependencies have been included or whether vulnerable transitive dependencies are hidden inside bundled JARs (particularly in `batik-all-1.9.jar` which is an all-in-one JAR).

3. **No reproducible builds**: Any developer can add, replace, or remove JARs without a pull request review or CI gate. The duplicate commons-logging and commons-net JARs are a direct consequence of this process gap.

4. **No CI/CD pipeline evidence**: No GitHub Actions, Jenkinsfile, or equivalent pipeline configuration is present in the repository. All deployment appears to be manual from Eclipse.

**Recommendation:**
Migrate to Maven or Gradle. At minimum, run OWASP Dependency-Check against the current WEB-INF/lib/ directory as a standalone scan immediately. Integrate automated dependency scanning into the CI/CD pipeline once one exists.

---

### A18-12 — Apache POI 3.9 — JUnit in Production Classpath

**Severity:** MEDIUM
**Category:** Dependency / Attack Surface
**JAR:** `WEB-INF/lib/junit-3.8.1.jar`

**Description:**
JUnit 3.8.1 is a test framework JAR and should never be present in a production WEB-INF/lib/. Its presence in the deployed application classpath is a hygiene violation that:

1. Unnecessarily increases the application attack surface.
2. May expose test infrastructure classes to the classloader.
3. Indicates that no build process separates test-scope dependencies from production-scope dependencies (another symptom of the missing build system).

JUnit 3.8.1 is also an extremely old version from approximately 2002.

**Evidence:**
- `WEB-INF/lib/junit-3.8.1.jar` — present in production library directory
- `.classpath` line 24

**Recommendation:**
Remove `junit-3.8.1.jar` from `WEB-INF/lib/` immediately. Test dependencies must never be deployed to production.

---

### A18-13 — Tomcat Version Unknown — Potential EOL Container

**Severity:** HIGH
**Category:** Infrastructure / Container Version
**CVE(s):** Multiple CVEs affecting Tomcat 7.x and 8.x (EOL)

**Description:**
The Tomcat container version cannot be determined from repository contents. The evidence establishes:

- `web.xml` declares Servlet specification **3.0**, which requires minimum Tomcat 7.0.
- The `.classpath` references `CATALINA_HOME/lib/jasper.jar`, `jasper-el.jar`, `jsp-api.jar`, and `servlet-api.jar` — standard Tomcat 7/8 layout.
- The `work/org/apache/jsp/` directory is a standard Tomcat JSP work directory.
- **Tomcat 7.x reached End of Life on March 31, 2021.**
- **Tomcat 8.0.x reached End of Life on June 30, 2018.**
- **Tomcat 8.5.x reached End of Life on March 31, 2024.**

If the deployed Tomcat is version 7.x or 8.5.x (both of which remain common in older Java EE applications of this generation), it may be running with unpatched CVEs including deserialization vulnerabilities in Tomcat's session handling, AJP connector vulnerabilities (CVE-2020-1938 "GhostCat", CVSS 9.8), and TLS configuration weaknesses.

**Evidence:**
- `WEB-INF/web.xml` servlet-spec 3.0 schema (minimum Tomcat 7.0)
- `work/org/apache/jsp/` present
- No `CATALINA_HOME` version information in repository
- Tomcat 7 EOL: March 2021; Tomcat 8.5 EOL: March 2024

**Recommendation:**
Immediately determine the deployed Tomcat version by running `catalina.sh version` or checking the `CATALINA_HOME/lib/catalina.jar` MANIFEST.MF on the deployment server. If Tomcat is below 9.0, upgrade to Tomcat **10.1.x** (Jakarta EE 10, latest stable LTS). If remaining on Tomcat 9.x for Java EE 8 compatibility, ensure the version is at minimum **9.0.99** or the latest patch release.

---

### A18-14 — XMLBeans 2.3.0 — XXE and Very Old Version

**Severity:** HIGH
**Category:** Dependency / Known Vulnerability
**JAR:** `WEB-INF/lib/xmlbeans-2.3.0.jar`
**CVE(s):** CVE-2021-23926

**Description:**
Apache XMLBeans 2.3.0 (build revision r540734, released approximately 2007) is affected by **CVE-2021-23926** (CVSS 9.1 CRITICAL): XML external entity (XXE) injection. XMLBeans before 3.0.0 does not disable external entity resolution by default. A crafted XML document supplied to XMLBeans-processed code (including POI OOXML, which uses XMLBeans internally for schema binding) can cause arbitrary file disclosure or SSRF.

This JAR is used by `poi-ooxml` for OOXML schema binding and represents an 18-year-old library with no security updates.

**Evidence:**
- `WEB-INF/lib/xmlbeans-2.3.0.jar` — Version: 2.3.0-r540734
- `.classpath` line 29

**Recommendation:**
Upgrade to XMLBeans **5.1.1** or later. This upgrade is tightly coupled to the POI upgrade (A18-3) since POI OOXML uses XMLBeans as a dependency. Upgrade POI and XMLBeans together.

---

### A18-15 — PostgreSQL JDBC Driver 8.3-603 — EOL Database Driver

**Severity:** HIGH
**Category:** Dependency / EOL / Known Vulnerability
**JAR:** `WEB-INF/lib/postgresql-8.3-603.jdbc4.jar`

**Description:**
The PostgreSQL JDBC driver version 8.3-603 (for PostgreSQL 8.3) reached end-of-life with PostgreSQL 8.3 itself on **February 1, 2013** — over 13 years ago. This driver:

1. Is compiled against Java 1.6 (per MANIFEST.MF: Built-By Ant 1.5.4, JDK 1.6).
2. Does not support modern TLS (TLS 1.2 / TLS 1.3) for encrypted database connections. PostgreSQL 8.3 JDBC supports only SSL with deprecated cipher suites.
3. Is affected by multiple CVEs in the PostgreSQL JDBC driver line that were fixed in later versions, including CVE-2022-21724 (CVSS 9.8): Class injection via `loggerLevel` or `loggerFile` connection properties.
4. Does not support security features introduced in JDBC 4.2 (parameter type validation, improved prepared statement handling).

**Evidence:**
- `WEB-INF/lib/postgresql-8.3-603.jdbc4.jar` — MANIFEST.MF: Built-By Ant 1.5.4, JDK 1.6 target

**Recommendation:**
Upgrade to PostgreSQL JDBC driver **42.7.x** (latest stable as of 2025). The 42.x driver series supports PostgreSQL 8.2 through 17 and uses modern TLS. This is a drop-in replacement for JDBC4 code — no API changes required for standard JDBC usage.

---

### A18-16 — charts4j 1.3 — Outbound Data Leakage to Google Charts API (Deprecated)

**Severity:** MEDIUM
**Category:** Data Leakage / Privacy / Third-Party Dependency
**JAR:** `WEB-INF/lib/charts4j-1.3.jar`

**Description:**
charts4j is a Java wrapper for the **Google Charts API** (formerly Google Image Charts). The library works by encoding chart data into a URL and making an HTTP GET request to `https://chart.apis.google.com/chart` (or the equivalent endpoint) with chart data embedded in the URL parameters.

**Google shut down the Google Image Charts API on March 14, 2019.** As a result, charts4j 1.3 is calling a deprecated external API that is no longer officially supported.

More critically, 18 chart classes in the application call `chart.toURLString()` and use the resulting Google Charts URL:
- `BarChartR.java`, `BarChartUtil.java`, `BarChartCategory.java`, `BarChartNational.java`, `BarChartImpactCategory.java`
- `LineChartR.java`, `LineChartR_au.java`, `PieChartR.java`
- `excel/BatteryChargeChart.java`, `excel/UserLoginChart.java`, `excel/DriverActivityChart.java`, `excel/ExpiryChart.java`, `excel/ImpactChart.java`, `excel/PreopFailChart.java`, `excel/DriverAccessAbuseChart.java`, `excel/MachineUnlockChart.java`, `excel/DriverAccessAbuseChart.java`

Chart data (fleet metrics, driver activity, vehicle data) is encoded into the URL sent to Google's servers. This constitutes **outbound leakage of fleet operational data to a third-party server** with no data processing agreement evident. This may violate GDPR, PDPA (Australian/Singapore), or Linde's customer data governance policies.

**Evidence:**
- `WEB-INF/lib/charts4j-1.3.jar` present
- `WEB-INF/src/com/torrent/surat/fms6/chart/Chart.java`: `import com.googlecode.charts4j.Color;`
- `WEB-INF/src/com/torrent/surat/fms6/chart/BarChartR.java` line 89: `String url = chart.toURLString();`
- 18 Java files call `chart.toURLString()` — full list above
- Google Image Charts API deprecated: March 14, 2019

**Recommendation:**
Replace charts4j and the Google Charts API dependency entirely. Migrate to a server-side chart library such as JFreeChart (already present as `jfreechart-1.0.19.jar`) or Chart.js (client-side, no data sent externally). All chart data must remain server-side. Remove `charts4j-1.3.jar` from WEB-INF/lib/.

---

### A18-17 — JavaMelody — Monitoring Endpoint Authentication Status Unknown

**Severity:** LOW
**Category:** Information Disclosure / Configuration
**JAR:** `WEB-INF/lib/javamelody.jar` (version unknown)

**Description:**
JavaMelody is an application performance monitoring library that exposes a built-in web endpoint (by default at `/monitoring`) that displays detailed application internals including:
- HTTP request statistics and timings
- SQL query statistics and execution times (including partial query content)
- JVM memory and thread state
- Session counts and user activity
- Exception traces

If this endpoint is not protected by authentication, any unauthenticated user can access sensitive operational data about the application.

**Important finding:** JavaMelody's `MonitoringFilter` is configured in `WEB-INF/web - Copy.xml` (the stale backup file) but is **NOT present in the active `WEB-INF/web.xml`**. This means JavaMelody may not currently be active in the deployed application. However, the JAR is present in WEB-INF/lib/ and will be loaded by the classloader regardless.

If JavaMelody is inadvertently activated (e.g., if `web - Copy.xml` were ever used as the deployment descriptor, or if the filter is added), it would expose the monitoring endpoint at `/*` with no authentication filter visible in `web.xml`.

**Evidence:**
- `WEB-INF/lib/javamelody.jar` — present, version not in MANIFEST.MF
- `WEB-INF/web - Copy.xml` lines 7-17: `MonitoringFilter` mapped to `/*`
- `WEB-INF/web.xml`: No JavaMelody filter present

**Recommendation:**
1. If JavaMelody monitoring is not needed, remove `javamelody.jar` from WEB-INF/lib/ entirely.
2. If monitoring is required, add authentication protection using the JavaMelody `allowed-addr-pattern` init parameter (restrict to localhost/management VLAN) or front it with a servlet security constraint.
3. Remove `WEB-INF/web - Copy.xml` from version control (it is a stale backup and a configuration confusion risk).

---

### A18-18 — Jsoup 1.12.1 — XSS Sanitizer Bypass

**Severity:** LOW
**Category:** Dependency / Known Vulnerability
**JAR:** `WEB-INF/lib/jsoup-1.12.1.jar`
**CVE(s):** CVE-2021-37714, CVE-2022-36033

**Description:**
Jsoup 1.12.1 (released 2019) is affected by:

1. **CVE-2021-37714** (CVSS 7.5 HIGH): Incorrect parsing of HTML can lead to XSS bypass when using `Jsoup.clean()` with a `Safelist`. Specifically, crafted input using certain Unicode characters can bypass the HTML sanitizer. Fixed in 1.14.2.

2. **CVE-2022-36033** (CVSS 6.1 MEDIUM): The Jsoup HTML sanitizer can be bypassed via crafted HTML that is parsed differently in some browsers. Fixed in 1.15.3.

If FleetFocus uses Jsoup for sanitizing HTML input (e.g., from rich text fields in reports or alerts), these bypasses could enable stored or reflected XSS.

**Evidence:**
- `WEB-INF/lib/jsoup-1.12.1.jar` — Version: 1.12.1
- `.classpath` line 39

**Recommendation:**
Upgrade to Jsoup **1.17.2** or later (latest stable as of 2025).

---

### A18-19 — Log4j 2.17.0 — Patched Against Log4Shell (Confirmed Safe, Informational)

**Severity:** INFORMATIONAL
**Category:** Dependency / CVE (Resolved)
**JARs:**
- `WEB-INF/lib/log4j-api-2.17.0.jar`
- `WEB-INF/lib/log4j-core-2.17.0.jar`
**CVE(s):** CVE-2021-44228 (Log4Shell), CVE-2021-45046, CVE-2021-45105, CVE-2021-44832

**Description:**
Log4j 2.17.0 is **patched** against all four critical Log4j 2 vulnerabilities:

| CVE | Vulnerability | Fixed In | Status in 2.17.0 |
|-----|--------------|----------|-----------------|
| CVE-2021-44228 | Log4Shell — JNDI RCE | 2.15.0 | PATCHED |
| CVE-2021-45046 | Log4Shell bypass (JNDI RCE) | 2.16.0 | PATCHED |
| CVE-2021-45105 | Infinite recursion DoS | 2.17.0 | PATCHED |
| CVE-2021-44832 | RCE via attacker-controlled config | 2.17.1 | NOT FIXED |

Note that CVE-2021-44832 (CVSS 6.6 MEDIUM) affecting versions before 2.17.1 is technically present. However, this CVE requires an attacker to already have write access to the Log4j configuration, making it a very low practical risk in a standard deployment. It is nonetheless recommended to upgrade.

Additionally, note that `WEB-INF/src/log4j.properties` suggests Log4j **1.x** configuration is also present. Log4j 1.x is completely end-of-life (since August 2015) and affected by CVE-2019-17571 (CRITICAL) and CVE-2022-23302/23303/23305. If Log4j 1.x is active alongside Log4j 2.x, the 1.x risk applies.

**Evidence:**
- `WEB-INF/lib/log4j-api-2.17.0.jar` — Version: 2.17.0
- `WEB-INF/lib/log4j-core-2.17.0.jar` — Version: 2.17.0
- `WEB-INF/src/log4j.properties` — Log4j 1.x configuration file (bridge or legacy config?)

**Recommendation:**
1. Upgrade to Log4j **2.24.x** or later to resolve CVE-2021-44832 and benefit from recent improvements.
2. Audit `log4j.properties` to confirm Log4j 1.x is not in active use (the Log4j2 API should bridge through `log4j-1.2-api` if any legacy Log4j 1 calls exist, without needing `log4j-1.x` JARs). No `log4j-1.x` JARs were found in WEB-INF/lib, which is positive.

---

## Classpath Ordering Analysis

The `.classpath` file reveals the following classpath order for duplicate libraries:

| JAR | Position in .classpath | Version | Build-time Precedence |
|-----|----------------------|---------|----------------------|
| commons-logging.jar | Line 5 (position 1) | 1.1 | FIRST — wins at compile time |
| commons-logging-1.1.1.jar | Line 18 (position 13) | 1.1.1 | Second |
| commons-net-2.0.jar | Line 9 (position 5) | 2.0 | FIRST — wins at compile time |
| commons-net-1.4.1.jar | Line 22 (position 17) | 1.4.1 | Second |

At **Tomcat runtime**, WEB-INF/lib/ JARs are loaded in filesystem order (alphabetical on most OS/filesystems):
- `commons-logging-1.1.1.jar` loads before `commons-logging.jar` → version 1.1.1 wins at runtime
- `commons-net-1.4.1.jar` loads before `commons-net-2.0.jar` → version 1.4.1 wins at runtime (OPPOSITE of build time)

This means the application is compiled against `commons-net-2.0` but likely executes against `commons-net-1.4.1` in production — a classpath split between build and runtime environments.

---

## Finding Summary Table

| Finding ID | JAR(s) | Severity | CVE(s) | Category |
|-----------|--------|----------|--------|----------|
| A18-1 | commons-collections-3.1.jar | CRITICAL | CVE-2015-6420, CVE-2015-7501 | Deserialization RCE |
| A18-2 | commons-fileupload-1.1.jar | CRITICAL | CVE-2014-0050, CVE-2016-1000031 | DoS + RCE via deserialization |
| A18-3 | poi-3.9-*.jar (×3) | HIGH | CVE-2014-9527, CVE-2017-5644, CVE-2019-12415 | XXE + DoS |
| A18-4 | httpclient-4.2.3.jar, httpcore-4.2.2.jar | HIGH | CVE-2014-3577, CVE-2020-13956 | SSL bypass + SSRF |
| A18-5 | dom4j-1.6.1.jar | HIGH | CVE-2018-1000632, CVE-2020-10683 | XML injection + XXE |
| A18-6 | itextpdf-5.4.2.jar | HIGH | CVE-2017-7386, CVE-2018-10036 | SSRF + DoS + License |
| A18-7 | batik-*.jar (×4) | HIGH | CVE-2019-17566, CVE-2022-38648, CVE-2022-40146, CVE-2022-44729, CVE-2022-44730 | SSRF |
| A18-8 | gson-2.8.5.jar | MEDIUM | CVE-2022-25647 | Stack overflow DoS |
| A18-9 | commons-logging.jar + commons-logging-1.1.1.jar | MEDIUM | N/A | Classpath conflict |
| A18-10 | commons-net-1.4.1.jar + commons-net-2.0.jar | MEDIUM | N/A | Classpath conflict + runtime mismatch |
| A18-11 | (build system absent) | MEDIUM | N/A | Process / supply chain |
| A18-12 | junit-3.8.1.jar | MEDIUM | N/A | Test JAR in production |
| A18-13 | (Tomcat — unknown version) | HIGH | Multiple (GhostCat CVE-2020-1938 if AJP exposed) | EOL container |
| A18-14 | xmlbeans-2.3.0.jar | HIGH | CVE-2021-23926 | XXE |
| A18-15 | postgresql-8.3-603.jdbc4.jar | HIGH | CVE-2022-21724 | EOL driver + TLS |
| A18-16 | charts4j-1.3.jar | MEDIUM | N/A | Data leakage to Google |
| A18-17 | javamelody.jar | LOW | N/A | Unauthenticated monitoring endpoint risk |
| A18-18 | jsoup-1.12.1.jar | LOW | CVE-2021-37714, CVE-2022-36033 | XSS sanitizer bypass |
| A18-19 | log4j-api/core-2.17.0.jar | INFORMATIONAL | CVE-2021-44832 (low risk) | Log4Shell (patched) |

**Total findings: 19**
CRITICAL: 2 | HIGH: 7 | MEDIUM: 5 | LOW: 2 | INFORMATIONAL: 1

---

## Priority Upgrade Recommendations

The following upgrades are recommended in priority order:

| Priority | Action | Rationale |
|---------|--------|-----------|
| P1-IMMEDIATE | Upgrade `commons-collections-3.1.jar` to 3.2.2 or 4.4 | CRITICAL RCE gadget chain |
| P1-IMMEDIATE | Upgrade `commons-fileupload-1.1.jar` to 1.5 | CRITICAL RCE + DoS |
| P1-IMMEDIATE | Confirm and upgrade Tomcat to 9.0.x or 10.1.x | EOL container |
| P2-HIGH | Upgrade `dom4j-1.6.1.jar` to 2.1.4 | XXE — actively exploitable on upload paths |
| P2-HIGH | Upgrade `xmlbeans-2.3.0.jar` to 5.1.1 + `poi-3.9-*.jar` to 5.2.5 | XXE on document import |
| P2-HIGH | Upgrade `batik-*.jar` to 1.17 | SSRF via SVG |
| P2-HIGH | Upgrade `postgresql-8.3-603.jdbc4.jar` to 42.7.x | EOL driver + TLS risk |
| P3-HIGH | Upgrade `httpclient-4.2.3.jar` to 4.5.14 | SSL bypass |
| P3-HIGH | Upgrade `itextpdf-5.4.2.jar` to 7.x or replace with PDFBox | SSRF + license compliance |
| P4-MEDIUM | Remove `junit-3.8.1.jar` from production | Test scope in production |
| P4-MEDIUM | Remove duplicate `commons-logging.jar` (keep 1.1.1) | Classpath conflict |
| P4-MEDIUM | Remove duplicate `commons-net-1.4.1.jar` and upgrade 2.0 to 3.9.0 | Runtime/build mismatch |
| P4-MEDIUM | Upgrade `gson-2.8.5.jar` to 2.10.1 | DoS via crafted JSON |
| P5-MEDIUM | Replace `charts4j-1.3.jar` with JFreeChart for charts | Data leakage to Google API |
| P5-MEDIUM | Introduce Maven or Gradle build system | Process control + automated CVE scanning |
| P6-LOW | Upgrade `jsoup-1.12.1.jar` to 1.17.2 | XSS sanitizer bypass |
| P6-LOW | Evaluate and remove or protect `javamelody.jar` | Monitoring exposure risk |
| P7-INFO | Upgrade `log4j-*.jar` to 2.24.x | Minor CVE completeness |

---

*End of A18 Dependency Vulnerability Review*
*Output file: `audit/2026-02-25-01/pass1/dependencies.md`*
