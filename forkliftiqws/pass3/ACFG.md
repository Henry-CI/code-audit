# Pass 3 – Documentation Audit: Configuration Files
**Agent:** ACFG
**Date:** 2026-02-27
**Scope:** All configuration files

---

## Files Audited

| # | File |
|---|------|
| 1 | `pom.xml` |
| 2 | `settings.xml` |
| 3 | `environment.dev.properties` |
| 4 | `environment.prod.properties` |
| 5 | `environment.uat.properties` |
| 6 | `src/main/resources/fleetiq360ws.properties` |
| 7 | `src/main/resources/logback.xml` |
| 8 | `src/main/resources/META-INF/context.xml` |
| 9 | `src/main/webapp/WEB-INF/web.xml` |
| 10 | `src/main/webapp/WEB-INF/spring/appServlet/servlet-context.xml` |
| 11 | `src/main/webapp/WEB-INF/spring/spring-security.xml` |

---

## Reading Evidence

### 1. `pom.xml`
**File type:** Maven Project Object Model (XML)

**Settings defined:**
- `<groupId>` / `<artifactId>` / `<version>`: `com.collectiveintelligence` / `fleetiq360ws` / `1.0.0`
- `<packaging>`: `war`
- **Version properties:** `java-version=1.8`, Spring `3.2.14.RELEASE`, AspectJ `1.7.4`, SLF4J `1.7.5`, Jackson `2.6.7`, Flyway `5.1.4`
- **Profiles:** `local` (not default), `dev` (not default), `prod` (not default), `uat` (**activeByDefault=true**)
  - Each profile supplies: `flyway.url`, `flyway.user`, `flyway.password`, `tomcat.url`, `tomcat.server`, `splunk.host`, `splunk.port`
- **Custom repository:** `splunk-artifactory` at `http://splunk.jfrog.io/splunk/ext-releases-local` (HTTP, not HTTPS)
- **Key dependencies (no comments/explanation):** Spring MVC, Spring Security 3.1.1, Spring Security OAuth2 1.0.0, Jackson, Logback 1.2.3, Flyway, Braintree gateway, AWS SDK 1.11.163, Passay, Tika, Lombok, JUnit 4.7
- **Build filters:** `environment.${env}.properties`
- **Maven Compiler Plugin:** source/target `1.8`, `-Xlint:all`, `showWarnings=true`, `showDeprecation=true`
- **Flyway plugin:** `sqlMigrationSeparator=__`, location `filesystem:src/main/resources/db/migration`
- **Tomcat7 Maven Plugin:** deploys via `${tomcat.url}` / `${tomcat.server}`

**Inline documentation:** None. No comments explain profile selection strategy, why `uat` is the default active profile, why specific library versions were pinned, or the purpose of any dependency.

---

### 2. `settings.xml`
**File type:** Maven Settings (XML)

**Settings defined:**
- Server `TomcatServerUat`: username `maven`, password `C!1admin` (plaintext)
- Server `TomcatServerAzure`: username `maven`, password `pyx1s!96` (plaintext)

**Inline documentation:** None.

---

### 3. `environment.dev.properties`
**File type:** Java properties (environment filter for `dev` profile)

**Settings defined:**
- `imageURL` / `systemImageURL`: Azure host `forklift360.canadaeast.cloudapp.azure.com:8443`
- `uploadDir`: `/var/local/pandora/upload`
- `imageDir`: `image`
- `packageDir`: `/var/local/pandora/apk`
- `logDir`: `/var/local/pandora/logs`
- `flyway.baseline`: `false`
- `flyway.enabled`: `true`
- `splunk.host`: `127.0.0.1`
- `splunk.port`: `15000`
- `imagePrefix`: `dev-`
- `cloudImagedDir`: `image/`
- `bucketName`: `forkliftiq360`
- `cognitoAPIPort`: `9090`
- `cognitoAPIUsername`: `ciiadmin`
- `cognitoAPIPassword`: `ciiadmin` (plaintext)

**Inline documentation:** None. No comments on any property.

---

### 4. `environment.prod.properties`
**File type:** Java properties (environment filter for `prod` profile)

**Settings defined:** Identical in structure to UAT:
- `imageURL` / `systemImageURL`: AWS EC2 host `ec2-54-86-82-22.compute-1.amazonaws.com:8443`
- `uploadDir`: `/var/local/tomcat8/upload`
- `packageDir`: `/var/local/tomcat8/upload/apk`
- `logDir`: `/var/log/pandora`
- `flyway.baseline`: `false`
- `flyway.enabled`: `false`
- `imagePrefix`: `uat-` **(mislabelled — says "uat-" in the prod file)**
- `splunk.host`: `127.0.0.1`
- `splunk.port`: `15000`
- `cognitoAPIUsername`: `ciiadmin`
- `cognitoAPIPassword`: `ciiadmin` (plaintext)

**Inline documentation:** None.

---

### 5. `environment.uat.properties`
**File type:** Java properties (environment filter for `uat` profile)

**Settings defined:** Byte-for-byte identical to `environment.prod.properties`.

**Inline documentation:** None.

---

### 6. `src/main/resources/fleetiq360ws.properties`
**File type:** Java properties (application master properties; values filtered from environment files at build)

**Settings defined:**
- Email message bodies/subjects: `userSetupMsg`, `userSetupSubject`, `passResetSubject`, `driverRequestSubject`
- Interpolated tokens for all environment-specific values: `imageURL`, `systemImageURL`, `uploadDir`, `imageDir`, `packageDir`, `flyway.baseline`, `flyway.enabled`, `imagePrefix`, `cloudImagedDir`, `bucketName`, `cognitoAPIPort`, `cognitoAPIUsername`, `cognitoAPIPassword`
- Hard-coded URL: `acceptURL=https://pandora.fleetiq360.com/pandora/acceptDriver?token=`
- Missing from filter delegation: `logDir` (defined in env files but not present in `fleetiq360ws.properties` as a passthrough token — it is referenced directly by logback.xml as a system property)

**Inline documentation:** None. No comments explain which values are filtered at build time vs. hard-coded, nor why `logDir` is excluded from the properties passthrough.

---

### 7. `src/main/resources/logback.xml`
**File type:** Logback XML configuration

**Settings defined:**
- **FILE appender:** `RollingFileAppender`, daily time-based rolling, `totalSizeCap=3GB`, pattern `%d%-4relative [%thread] %-5level %logger{0} - %msg%n`; log file: `${logDir}/fleetiq360ws.log`
- **Logger `com.journaldev.spring`** at `INFO` → FILE
- **Logger `com.journaldev.spring.jdbc.controller.APKUpdaterController`** at `DEBUG` → FILE (comment says "Temporary enable DEBUG to resolve issue in production environment")
- **Root logger** at `INFO` → FILE
- **socket appender (Splunk TCP):** `com.splunk.logging.TcpAppender`, `${splunk.host}:${splunk.port}`, pattern `%-4relative [%thread] %-5level %logger{0} - %msg%n`
- **Logger `com.journaldev.spring`** (duplicate name) at `INFO` with `additivity="false"` → socket
- **Root logger** (duplicate `<root>` declaration) at `INFO` → socket

**Inline documentation:** One substantive comment present: "Temporary enable DEBUG to resolve issue in production environment." Three boilerplate comments copied from documentation references.

---

### 8. `src/main/resources/META-INF/context.xml`
**File type:** Tomcat context descriptor (XML)

**Settings defined:**
- `antiJARLocking="true"`: prevents JAR file locking on Windows hosts
- `path="/fleetiq360ws"`: context path

**Inline documentation:** None. The non-obvious `antiJARLocking` attribute has no comment.

---

### 9. `src/main/webapp/WEB-INF/web.xml`
**File type:** Java EE Web Application Deployment Descriptor (XML 2.5)

**Settings defined:**
- `<display-name>`: `Spring Rest Application`
- **Servlet:** `appServlet` → `DispatcherServlet`, contextConfigLocation `/WEB-INF/spring/appServlet/servlet-context.xml`, `load-on-startup=1`
- **Servlet mapping:** `appServlet` → `/`
- **Context param:** `contextConfigLocation` loads both `servlet-context.xml` and `spring-security.xml`
- **Listener:** `ContextLoaderListener`
- **Filter:** `springSecurityFilterChain` → `DelegatingFilterProxy`, mapped to `/*`
- **Resource ref:** `jdbc/PreStartDB` (DataSource, Container auth) — description reads "DB Connection"
- **Security constraint:** all URLs (`/*`), `transport-guarantee=CONFIDENTIAL` (forces HTTPS)

**Inline documentation:** The `<description>DB Connection</description>` on the resource-ref is a placeholder rather than meaningful documentation. No comments on any element.

---

### 10. `src/main/webapp/WEB-INF/spring/appServlet/servlet-context.xml`
**File type:** Spring MVC application context (XML)

**Beans/settings defined:**
- `context:property-placeholder` → `classpath:fleetiq360ws.properties`
- `<annotation-driven />` — enables Spring MVC annotation support
- Static resource handler: `/resources/**` → `/resources/`
- `InternalResourceViewResolver`: prefix `/WEB-INF/views/`, suffix `.jsp`
- `RequestMappingHandlerAdapter` with single `jsonMessageConverter` message converter
- `MappingJackson2HttpMessageConverter` bean (`jsonMessageConverter`)
- `CommonsMultipartResolver` (`multipartResolver`): `maxUploadSize=20971520` (20 MB), `maxInMemorySize=1048576` (1 MB)
- `JndiObjectFactoryBean` (`dataSource`): JNDI name `java:comp/env/jdbc/PreStartDB`
- `context:component-scan` base-package `com.journaldev.spring.jdbc`

**Inline documentation:** Most beans have comments; the `maxUploadSize` and `maxInMemorySize` values are annotated with their byte equivalents (`<!-- 20MB -->`, `<!-- 1MB -->`). The JEE namespace comment `<!-- using JEE namespace for lookup -->` is present but appears after the bean definition rather than before. The `dataSource` bean JNDI name `PreStartDB` is an obsolete name inconsistent with the application name (`fleetiq360ws`) but carries no explanatory comment.

---

### 11. `src/main/webapp/WEB-INF/spring/spring-security.xml`
**File type:** Spring Security + OAuth2 application context (XML)

**Beans/settings defined:**
- Two `<http security="none">` patterns for `/oauth/cache_approvals` and `/oauth/uncache_approvals` (comment: "Just for testing...")
- `<http>` for `/oauth/token`: stateless, clientAuthenticationManager, HTTP Basic, custom filter `clientCredentialsTokenEndpointFilter` after BASIC_AUTH_FILTER
- `<http>` for `/rest/**`: session `never`, intercept-url rules:
  - `/rest/db/**` → `ROLE_SYS_ADMIN` only
  - `/rest/apk/**` → `ROLE_CLIENT` only
  - `/rest/**` → `ROLE_DRIVER, ROLE_COMPANY_GROUP, ROLE_SYS_ADMIN, ROLE_CLIENT`
- `oauthAuthenticationEntryPoint`: realm `fleetiq360/client`
- `clientAuthenticationEntryPoint`: realm `fleetiq360/client`, type `Basic`
- `oauthAccessDeniedHandler`
- `clientCredentialsTokenEndpointFilter`
- `accessDecisionManager` (`UnanimousBased`): voters — `ScopeVoter`, `RoleVoter`, `AuthenticatedVoter`
- `clientAuthenticationManager` (authentication-manager)
- `userDetailsService` → `UserDetailsServiceImpl`
- `authenticationManager` (alias): provider uses `userDetailsService`, password-encoder `md5`
- `clientDetailsUserService`
- `tokenStore` → `JdbcTokenStore` (previously `InMemoryTokenStore`, commented out)
- `tokenServices` (`DefaultTokenServices`): `supportRefreshToken=true`
- `userApprovalHandler` (`TokenServicesUserApprovalHandler`)
- `oauth:authorization-server`: all grant types enabled — `authorization_code`, `implicit`, `refresh_token`, `client_credentials`, `password`
- `oauth:resource-server`: resource-id `fleetiq360ws`
- `oauth:client-details-service` with two hard-coded in-memory clients:
  - client `987654321`: grant types `password,authorization_code,implicit`, secret `8752361E593A573E86CA558FFD39E`, role `ROLE_CLIENT`, `access-token-validity=0` (never expires)
  - client `fleetiq360`: grant types `password,authorization_code,refresh_token,implicit`, secret `rihah8eey4faibuengaixo6leiL1awii`, roles `ROLE_DRIVER,ROLE_COMPANY_GROUP,ROLE_SYS_ADMIN`, `access-token-validity=300`, `refresh-token-validity=300`
- `sec:global-method-security`: `pre-post-annotations=enabled`, `proxy-target-class=true`

**Inline documentation:** Sparse. A few comments are present (`<!-- Just for testing... -->`, one comment about InMemoryTokenStore, one about persistence responsibility of TokenStore, one about authorization-server, one about ClientDetailsService) but the most security-critical settings (client secrets, MD5 password hashing, token validity, open grant types, unauthenticated OAuth endpoints) carry no explanatory documentation.

---

## Findings

---

### ACFG-1
**Severity:** CRITICAL
**File:** `settings.xml` (lines 9, 14)
**Issue:** Plaintext server deployment passwords committed to source control.
`TomcatServerUat` has password `C!1admin` and `TomcatServerAzure` has password `pyx1s!96` stored in plaintext in `settings.xml`, which is tracked in version control. Maven supports encrypted passwords via `mvn --encrypt-password`; none are used here. No comment or documentation acknowledges this as a known risk or interim measure.

---

### ACFG-2
**Severity:** CRITICAL
**File:** `environment.dev.properties` (line 16), `environment.prod.properties` (line 16), `environment.uat.properties` (line 16)
**Issue:** Plaintext Cognito API credentials (`cognitoAPIUsername=ciiadmin`, `cognitoAPIPassword=ciiadmin`) committed to source control in all three environment property files. No comment documents the nature of the Cognito API, the permissions held by this account, or an intention to rotate credentials. The same credential value appears across all three environments with no differentiation.

---

### ACFG-3
**Severity:** CRITICAL
**File:** `spring-security.xml` (lines 113–114, 116–117)
**Issue:** OAuth2 client secrets and client IDs are hard-coded in plaintext inside the XML configuration file committed to version control. Client `987654321` carries secret `8752361E593A573E86CA558FFD39E`; client `fleetiq360` carries secret `rihah8eey4faibuengaixo6leiL1awii`. There is no comment acknowledging the risk, referencing a rotation procedure, or explaining why an in-XML client store is used rather than a database-backed one. This is compounded by the comment `<!-- ClientsDeailsService: Entry Point to clients database (given is in memory implementation) -->` which is inaccurate — the secrets are in XML, not in-memory at runtime in the database sense.

---

### ACFG-4
**Severity:** CRITICAL
**File:** `pom.xml` (lines 28–32)
**Issue:** Duplicate `flyway.url` and `flyway.user`/`flyway.password` keys in the `local` profile. Lines 27–29 define `flyway.url=jdbc:postgresql://127.0.0.1/PreStart`, `flyway.user=postgres`, `flyway.password=gmtp-postgres`; lines 30–32 immediately override with `fleetiq360` database and credentials. Only the last definition takes effect. The first set of properties (including the password `gmtp-postgres`) is dead configuration. There is no comment explaining this duplication or indicating which set is correct. The stale values represent abandoned credentials that should not persist in the file.

---

### ACFG-5
**Severity:** HIGH
**File:** `pom.xml` (lines 75–76)
**Issue:** UAT profile contains the Flyway database password `C!1admin` in plaintext in the POM. The POM is committed to version control. No comment acknowledges this or references a mechanism for externalising credentials. Note: the same value (`C!1admin`) is also used as the Tomcat manager password in `settings.xml`.

---

### ACFG-6
**Severity:** HIGH
**File:** `spring-security.xml` (line 74)
**Issue:** The `authenticationManager` is configured with `<password-encoder hash="md5"/>`. MD5 is a cryptographically broken hash function unsuitable for password storage. This is not documented with any comment explaining why MD5 is in use, whether it is a legacy constraint, or whether a migration to a stronger algorithm (BCrypt, Argon2) is planned.

---

### ACFG-7
**Severity:** HIGH
**File:** `spring-security.xml` (line 114)
**Issue:** OAuth2 client `987654321` has `access-token-validity="0"`. A value of `0` means the token never expires. This is undocumented — there is no comment explaining whether `0` means infinite validity, which client this ID represents, or why non-expiring tokens are acceptable for this client. The numeric client-id `987654321` is also opaque with no accompanying comment naming the consumer.

---

### ACFG-8
**Severity:** HIGH
**File:** `spring-security.xml` (lines 13–14)
**Issue:** Two URL patterns — `/oauth/cache_approvals` and `/oauth/uncache_approvals` — are configured with `security="none"` (completely unauthenticated). The only inline comment is `<!-- Just for testing... -->`. There is no documentation indicating whether these endpoints are intentionally present in a production build, what they do, or whether they pose a security exposure. The comment implies they are test scaffolding that has never been removed.

---

### ACFG-9
**Severity:** HIGH
**File:** `logback.xml` (lines 22–24)
**Issue:** A logger for `com.journaldev.spring.jdbc.controller.APKUpdaterController` is set to `DEBUG` level with the inline comment "Temporary enable DEBUG to resolve issue in production environment." This indicates a temporary diagnostic change was committed and never reverted. The comment was not updated to record when the issue was resolved or whether the DEBUG level should be retained. DEBUG logging in production may expose sensitive data in log output.

---

### ACFG-10
**Severity:** HIGH
**File:** `environment.prod.properties` (line 11)
**Issue:** The `imagePrefix` property in `environment.prod.properties` is set to `uat-`. This is a production environment file; the prefix should almost certainly be `prod-` (the dev environment file uses `dev-` and the UAT file uses `uat-`). There is no comment explaining why the production prefix matches the UAT value. This is either a copy-paste error that was never documented or an inaccurate configuration.

---

### ACFG-11
**Severity:** HIGH
**File:** `environment.prod.properties` and `environment.uat.properties`
**Issue:** Both files are byte-for-byte identical in all settings including `imageURL`, `systemImageURL`, `uploadDir`, `packageDir`, `logDir`, `imagePrefix`, `cognitoAPIPort`, `cognitoAPIUsername`, and `cognitoAPIPassword`. There is no comment in either file explaining whether this is intentional (i.e., prod and UAT share infrastructure) or an error. If they share an environment, this should be documented; if they are meant to differ, the duplication indicates a missing prod configuration.

---

### ACFG-12
**Severity:** HIGH
**File:** `pom.xml` (lines 60–61)
**Issue:** The `prod` profile defines `<flyway.url>jdbc:postgresql://localhost:5432/postgres</flyway.url>` but provides no `flyway.user` or `flyway.password`. This means Flyway migrations in the prod profile will run with no credentials unless they happen to be inherited or externally supplied. No comment explains how prod database credentials are provided, nor why the `postgres` system database (rather than an application-specific database) is targeted. The missing credentials and unexpected database name are entirely uncommented.

---

### ACFG-13
**Severity:** MEDIUM
**File:** `pom.xml` (line 69)
**Issue:** The `uat` profile is the default active profile (`<activeByDefault>true</activeByDefault>`). This is a non-standard and potentially dangerous default — a developer running `mvn install` without specifying a profile will silently target the UAT environment (including UAT Flyway credentials and Tomcat deployment URL). There is no comment explaining this choice or warning developers about this default.

---

### ACFG-14
**Severity:** MEDIUM
**File:** `pom.xml` (line 88)
**Issue:** The Splunk Artifactory repository URL uses plain HTTP (`http://splunk.jfrog.io/splunk/ext-releases-local`) rather than HTTPS. This exposes the build to dependency substitution attacks (man-in-the-middle). There is no comment acknowledging this or explaining why HTTPS is not used.

---

### ACFG-15
**Severity:** MEDIUM
**File:** `logback.xml` (lines 43–45, 47–49)
**Issue:** The logger name `com.journaldev.spring` is declared twice — once routing to the FILE appender (line 16) and again with `additivity="false"` routing to the socket (Splunk) appender (lines 43–45). Duplicate `<root>` declarations also appear (lines 28–30 and 47–49). In Logback, the last `<root>` or duplicate `<logger>` wins; the first `<root>` and first `com.journaldev.spring` logger declaration are effectively dead. No comment explains the intended routing strategy or acknowledges the duplication.

---

### ACFG-16
**Severity:** MEDIUM
**File:** `spring-security.xml` (lines 99–106)
**Issue:** The `oauth:authorization-server` enables all five OAuth2 grant types simultaneously: `authorization_code`, `implicit`, `refresh_token`, `client_credentials`, and `password`. Enabling grant types not required by the application increases the attack surface. There is no comment documenting which clients use which grant types, why all are enabled, or what the intended flow is. The `implicit` grant type in particular is deprecated in OAuth 2.1 and inherently insecure.

---

### ACFG-17
**Severity:** MEDIUM
**File:** `servlet-context.xml` (line 57)
**Issue:** The JNDI DataSource bean references `java:comp/env/jdbc/PreStartDB`. The name `PreStartDB` does not correspond to the application name (`fleetiq360ws`) and appears to be a legacy name from a prior project (`PreStart`). The same stale name appears in `web.xml` (line 31). There is no comment explaining the provenance of this name or confirming it is intentional. This creates confusion about which database is actually targeted.

---

### ACFG-18
**Severity:** MEDIUM
**File:** `fleetiq360ws.properties` (line 10)
**Issue:** The `acceptURL` property is hard-coded to `https://pandora.fleetiq360.com/pandora/acceptDriver?token=` directly in the application properties file rather than being provided via environment filter tokens. This means the driver-accept URL is the same in all environments (dev, UAT, prod). There is no comment explaining whether this is intentional or an oversight, nor documenting which service hosts this endpoint.

---

### ACFG-19
**Severity:** MEDIUM
**File:** `pom.xml` (lines 12–17)
**Issue:** No dependency versions are documented with rationale. Notably: Spring Framework `3.2.14.RELEASE` and Spring Security `3.1.1.RELEASE` are both end-of-life versions with known CVEs. Jackson `2.6.7` is similarly outdated. AWS SDK `1.11.163` is a very old version of a rapidly updated library. There are no comments explaining why these versions are pinned, referencing a version upgrade plan, or acknowledging the EOL status.

---

### ACFG-20
**Severity:** MEDIUM
**File:** `spring-security.xml` (lines 83–86)
**Issue:** The `InMemoryTokenStore` is commented out and replaced with `JdbcTokenStore`. The comment reads: `<!-- Used for the persistenceof tokens (currently an in memory implementation) -->` — but this comment is now inaccurate; the implementation is JDBC, not in-memory. The stale comment was not updated when the implementation was changed.

---

### ACFG-21
**Severity:** LOW
**File:** `pom.xml` (line 61)
**Issue:** The `prod` profile defines `<tomcat.url></tomcat.url>` as an empty string. There is no comment explaining how production deployments are performed if not through the Tomcat Maven plugin, nor whether this is intentional (manual deployment, CI pipeline) or an unfinished placeholder.

---

### ACFG-22
**Severity:** LOW
**File:** `context.xml`
**Issue:** The file is a single-line element `<context antiJARLocking="true" path="/fleetiq360ws"/>` with no comments. The `antiJARLocking` attribute, which prevents Tomcat from locking JAR files on Windows, is a non-obvious platform-specific setting that warrants an explanatory comment.

---

### ACFG-23
**Severity:** LOW
**File:** `web.xml` (line 31)
**Issue:** The `<resource-ref>` description reads "DB Connection" — an entirely generic placeholder that provides no useful documentation about what database is being connected to, what schema it contains, or how the JNDI resource is configured on the container side.

---

### ACFG-24
**Severity:** LOW
**File:** `servlet-context.xml` (line 62)
**Issue:** The component scan base-package is `com.journaldev.spring.jdbc`. The prefix `com.journaldev` is the package namespace of a well-known Java tutorial blog (JournalDev). This strongly indicates the application was built from a tutorial template and the package name was never updated to reflect the actual organisation (`com.collectiveintelligence`). There is no comment acknowledging this or explaining the naming discrepancy. This is also observed in `logback.xml` logger names (lines 16, 43).

---

### ACFG-25
**Severity:** LOW
**File:** `environment.dev.properties` (line 12)
**Issue:** The property key is `cloudImagedDir` (with a `d` — likely a typo for `cloudImageDir`). This same misspelling appears in all three environment property files and in `fleetiq360ws.properties`. No comment acknowledges this as an intentional name or a known typo.

---

### ACFG-26
**Severity:** LOW
**File:** `logback.xml` (line 9)
**Issue:** `totalSizeCap` is set to `3GB` with no documentation explaining how this value was chosen, what happens to logs when the cap is reached (oldest logs are deleted), or whether `3GB` is appropriate for the deployment environment's disk capacity.

---

### ACFG-27
**Severity:** INFO
**File:** `spring-security.xml` (lines 88–93)
**Issue:** The comment on the `tokenServices` bean contains a typographical error and unclear phrasing: "Used to save token and and every thing about them except for their persistence that is reposibility of TokenStore (Given here is a default implementation)". The word "and" is doubled, "reposibility" is misspelt, and the parenthetical is grammatically ambiguous. While minor, this undermines the usefulness of the comment as documentation.

---

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 4 (ACFG-1, ACFG-2, ACFG-3, ACFG-4) |
| HIGH | 8 (ACFG-5 through ACFG-12) |
| MEDIUM | 8 (ACFG-13 through ACFG-20) |
| LOW | 6 (ACFG-21 through ACFG-26) |
| INFO | 1 (ACFG-27) |
| **Total** | **27** |

### Key Themes

1. **Credentials in source control (CRITICAL/HIGH):** Plaintext passwords and secrets appear in `settings.xml`, all three environment property files, and `spring-security.xml`. None are documented with risk acknowledgement or rotation procedures.

2. **Broken/weak security with no documentation (HIGH):** MD5 password hashing, non-expiring OAuth tokens, unauthenticated test endpoints left in production configuration, and all OAuth grant types enabled — all without any explanatory comment.

3. **Inaccurate documentation (MEDIUM/HIGH):** The `environment.prod.properties` file contains `imagePrefix=uat-`, the `tokenServices` comment still says "in memory", and the `PreStartDB` JNDI name is a legacy artefact — none have comments acknowledging or explaining the discrepancy.

4. **Missing environment differentiation (HIGH):** `environment.prod.properties` and `environment.uat.properties` are identical, with no comment confirming intent.

5. **Stale and temporary configuration committed permanently (HIGH/MEDIUM):** DEBUG logging marked as "temporary," commented-out code with inaccurate accompanying comments, and dead duplicate property definitions in the `local` profile.
