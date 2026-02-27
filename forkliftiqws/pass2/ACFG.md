# ACFG - Pass 2: Test Coverage Audit (Configuration Files)
**Date:** 2026-02-27
**Agent:** ACFG
**Scope:** All configuration files — build, environment, properties, logging, web, Spring MVC, Spring Security

---

## Reading Evidence

### 1. pom.xml
**File Type:** Maven Project Object Model

**Build Properties:**
- `java-version`: 1.8
- `org.springframework-version`: 3.2.14.RELEASE
- `org.aspectj-version`: 1.7.4
- `org.slf4j-version`: 1.7.5
- `jackson.databind-version`: 2.6.7
- `flyway.version`: 5.1.4

**Maven Profiles (4 defined):**
| Profile | Active By Default | Flyway URL | Notes |
|---------|------------------|------------|-------|
| `local` | false | `jdbc:postgresql://localhost:5432/fleetiq360` | Duplicate `flyway.url` / `flyway.user` / `flyway.password` keys within same profile |
| `dev` | false | `jdbc:postgresql://forklift360.canadaeast.cloudapp.azure.com:5432/fleetiq360` | Azure |
| `prod` | false | `jdbc:postgresql://localhost:5432/postgres` | No flyway.user/password set |
| `uat` | **true** | `jdbc:postgresql://forkliftiq360.cmjwsurtk4tn.us-east-1.rds.amazonaws.com:5432/postgres` | AWS RDS |

**Key Dependencies:**
- Spring Framework 3.2.14.RELEASE (Spring MVC, JDBC, Context)
- Spring Security 3.1.1.RELEASE
- Spring Security OAuth2 1.0.0.RELEASE
- Logback Classic 1.2.3
- Flyway Core 5.1.4
- Jackson Databind 2.6.7
- JUnit 4.7 (test scope only)
- Lombok 1.18.0
- AWS Java SDK 1.11.163
- Braintree Java 2.53.0
- Passay 1.3.1
- Splunk Library JavaLogging 1.6.2
- commons-fileupload 1.3.1, Apache Tika 1.18

**No test frameworks beyond JUnit 4.7:** No Mockito, no spring-test, no mockito-core, no Hamcrest beyond what ships with JUnit 4.7.

**Build Plugins:**
- `maven-compiler-plugin` 2.5.1 — source/target Java 1.8, `-Xlint:all`
- `maven-war-plugin` 3.2.2
- `flyway-maven-plugin` 5.1.4 — `sqlMigrationSeparator: __`, locations `filesystem:src/main/resources/db/migration`
- `tomcat7-maven-plugin` 2.2 — deploys to configurable Tomcat URL/server

**Build Filter Mechanism:** `environment.${env}.properties` is applied as a Maven filter to `src/main/resources`, which causes placeholder substitution into `fleetiq360ws.properties`.

---

### 2. settings.xml
**File Type:** Maven Settings

**Server Credentials Defined:**
| Server ID | Username | Password |
|-----------|----------|----------|
| `TomcatServerUat` | `maven` | `C!1admin` |
| `TomcatServerAzure` | `maven` | `pyx1s!96` |

No repository mirrors, no proxy settings, no plugin groups defined.

---

### 3. environment.dev.properties
**File Type:** Maven build filter properties (dev environment)

| Key | Value |
|-----|-------|
| `imageURL` | `https://forklift360.canadaeast.cloudapp.azure.com:8443/fleetiq360ws/image/` |
| `systemImageURL` | `https://forklift360.canadaeast.cloudapp.azure.com:8443/fleetiq360ws/image/` |
| `uploadDir` | `/var/local/pandora/upload` |
| `imageDir` | `image` |
| `packageDir` | `/var/local/pandora/apk` |
| `logDir` | `/var/local/pandora/logs` |
| `flyway.baseline` | `false` |
| `flyway.enabled` | `true` |
| `splunk.host` | `127.0.0.1` |
| `splunk.port` | `15000` |
| `imagePrefix` | `dev-` |
| `cloudImagedDir` | `image/` |
| `bucketName` | `forkliftiq360` |
| `cognitoAPIPort` | `9090` |
| `cognitoAPIUsername` | `ciiadmin` |
| `cognitoAPIPassword` | `ciiadmin` |

---

### 4. environment.prod.properties
**File Type:** Maven build filter properties (prod environment)

| Key | Value |
|-----|-------|
| `imageURL` | `https://ec2-54-86-82-22.compute-1.amazonaws.com:8443/fleetiq360ws/image/` |
| `systemImageURL` | `https://ec2-54-86-82-22.compute-1.amazonaws.com:8443/fleetiq360ws/image/` |
| `uploadDir` | `/var/local/tomcat8/upload` |
| `imageDir` | `image` |
| `packageDir` | `/var/local/tomcat8/upload/apk` |
| `logDir` | `/var/log/pandora` |
| `flyway.baseline` | `false` |
| `flyway.enabled` | `false` |
| `splunk.host` | `127.0.0.1` |
| `splunk.port` | `15000` |
| `imagePrefix` | `uat-` |
| `cloudImagedDir` | `image/` |
| `bucketName` | `forkliftiq360` |
| `cognitoAPIPort` | `9090` |
| `cognitoAPIUsername` | `ciiadmin` |
| `cognitoAPIPassword` | `ciiadmin` |

---

### 5. environment.uat.properties
**File Type:** Maven build filter properties (UAT environment)

Values are **byte-for-byte identical** to `environment.prod.properties` — same URLs, same `imagePrefix=uat-`, same `flyway.enabled=false`, same Cognito credentials.

---

### 6. src/main/resources/fleetiq360ws.properties
**File Type:** Spring application properties (filtered at build time)

**Settings Defined (all use Maven placeholders):**
| Key | Placeholder / Value |
|-----|---------------------|
| `userSetupMsg` | Literal: `Thanks for signing up with ForkliftIQ360. Your account has been created. Your account name is` |
| `userSetupSubject` | Literal: `New User Account Registered` |
| `passResetSubject` | Literal: `ForkliftIQ360 APP Password Reset` |
| `driverRequestSubject` | Literal: `ForkliftIQ360 Driver Join Request` |
| `imageURL` | `${imageURL}` |
| `systemImageURL` | `${systemImageURL}` |
| `uploadDir` | `${uploadDir}` |
| `imageDir` | `${imageDir}` |
| `packageDir` | `${packageDir}` |
| `acceptURL` | Literal: `https://pandora.fleetiq360.com/pandora/acceptDriver?token=` |
| `flyway.baseline` | `${flyway.baseline}` |
| `flyway.enabled` | `${flyway.enabled}` |
| `imagePrefix` | `${imagePrefix}` |
| `cloudImagedDir` | `${cloudImagedDir}` |
| `bucketName` | `${bucketName}` |
| `cognitoAPIPort` | `${cognitoAPIPort}` |
| `cognitoAPIUsername` | `${cognitoAPIUsername}` |
| `cognitoAPIPassword` | `${cognitoAPIPassword}` |

**Note:** `logDir` is used by `logback.xml` but is NOT listed in `fleetiq360ws.properties` — it is a Logback system property resolved separately via the environment filter.

**Configuration.java** (`com.journaldev.spring.jdbc.util.Configuration`) binds: `userSetupMsg`, `userSetupSubject`, `passResetSubject`, `imageURL`, `systemImageURL`, `acceptURL`, `driverRequestSubject`, `cognitoAPIPort`, `cognitoAPIUsername`, `cognitoAPIPassword` via `@Value`.

**BootstrapService.java** binds: `flyway.baseline`, `flyway.enabled` via `@Value`.

---

### 7. src/main/resources/logback.xml
**File Type:** Logback logging configuration

**Appenders:**
| Appender Name | Class | Details |
|--------------|-------|---------|
| `FILE` | `RollingFileAppender` | File: `${logDir}/fleetiq360ws.log`; rolling by time pattern `${logDir}/fleetiq360ws.%d.log`; totalSizeCap 3GB |
| `socket` | `com.splunk.logging.TcpAppender` | RemoteHost: `${splunk.host}`; Port: `${splunk.port}` |

**Loggers:**
| Logger Name | Level | Appender(s) | Additivity |
|-------------|-------|-------------|------------|
| `com.journaldev.spring` | INFO | FILE | (default: true) — duplicated entry (two loggers same name) |
| `com.journaldev.spring.jdbc.controller.APKUpdaterController` | **DEBUG** | FILE | default |
| `com.journaldev.spring` | INFO | socket | **false** |
| root | INFO | FILE | N/A |
| root | INFO | socket | N/A |

**Issues visible in configuration:**
- `com.journaldev.spring` logger is declared twice (once for FILE, once for socket); two separate `<root>` blocks are present.
- `APKUpdaterController` is permanently set to DEBUG level with a comment "Temporary enable DEBUG to resolve issue in production environment" — suggesting a debug setting was left enabled.
- `${logDir}` and `${splunk.host}` / `${splunk.port}` are resolved via Logback's own property lookup (from JVM system properties or environment), not Spring `@Value`.

---

### 8. src/main/resources/META-INF/context.xml
**File Type:** Tomcat context descriptor

**Settings:**
- `antiJARLocking="true"`
- `path="/fleetiq360ws"`

No `<Resource>` element for JDBC is present in this file — database connection pooling is expected to be configured at the Tomcat server level (server.xml / context.xml in Tomcat conf).

---

### 9. src/main/webapp/WEB-INF/web.xml
**File Type:** Java EE Web Application Descriptor (Servlet 2.5)

**Servlets:**
| Servlet Name | Class | Load-on-Startup | URL Pattern |
|-------------|-------|-----------------|-------------|
| `appServlet` | `org.springframework.web.servlet.DispatcherServlet` | 1 | `/` |

**Context Config Locations:** `/WEB-INF/spring/appServlet/servlet-context.xml` AND `/WEB-INF/spring/spring-security.xml` (loaded by `ContextLoaderListener`)

**Note:** The same `servlet-context.xml` appears both as the DispatcherServlet's `contextConfigLocation` init-param AND in the root `contextConfigLocation` param — this means `servlet-context.xml` is loaded twice, once as the root application context and once as the servlet context.

**Filters:**
| Filter Name | Class | URL Pattern |
|-------------|-------|-------------|
| `springSecurityFilterChain` | `DelegatingFilterProxy` | `/*` |

**JNDI Resource Reference:**
- `jdbc/PreStartDB` — `javax.sql.DataSource`, container-managed auth

**Security Constraint:**
- All URLs (`/*`) — `CONFIDENTIAL` transport guarantee (requires HTTPS/SSL)

---

### 10. src/main/webapp/WEB-INF/spring/appServlet/servlet-context.xml
**File Type:** Spring MVC Dispatcher Servlet Context (XML)

**Beans Defined:**
| Bean ID | Class | Key Properties |
|---------|-------|----------------|
| (anonymous) | `InternalResourceViewResolver` | prefix: `/WEB-INF/views/`, suffix: `.jsp` |
| (anonymous) | `RequestMappingHandlerAdapter` | messageConverters: [jsonMessageConverter] |
| `jsonMessageConverter` | `MappingJackson2HttpMessageConverter` | — |
| `multipartResolver` | `CommonsMultipartResolver` | maxUploadSize: 20971520 (20MB); maxInMemorySize: 1048576 (1MB) |
| `dataSource` | `JndiObjectFactoryBean` | jndiName: `java:comp/env/jdbc/PreStartDB` |

**Other Configuration:**
- `<annotation-driven />` — enables `@RequestMapping`, `@ResponseBody`, etc.
- `<context:property-placeholder location="classpath:fleetiq360ws.properties"/>` — loads the filtered properties file
- `<context:component-scan base-package="com.journaldev.spring.jdbc"/>` — scans all beans
- Static resources mapped: `/resources/**` → `/resources/`

---

### 11. src/main/webapp/WEB-INF/spring/spring-security.xml
**File Type:** Spring Security OAuth2 Configuration (XML)

**HTTP Security Chains:**
| Pattern | Session | Auth Manager | Notes |
|---------|---------|-------------|-------|
| `/oauth/cache_approvals` | — | none | `security="none"` — unprotected; comment says "Just for testing" |
| `/oauth/uncache_approvals` | — | none | `security="none"` — unprotected; comment says "Just for testing" |
| `/oauth/token` | stateless | clientAuthenticationManager | Requires `IS_AUTHENTICATED_FULLY`; Basic auth + client credentials filter |
| `/rest/db/**` | never | (resource server) | Requires `ROLE_SYS_ADMIN` only |
| `/rest/apk/**` | never | (resource server) | Requires `ROLE_CLIENT` only |
| `/rest/**` | never | (resource server) | Requires `ROLE_DRIVER`, `ROLE_COMPANY_GROUP`, `ROLE_SYS_ADMIN`, or `ROLE_CLIENT` |

**Beans Defined:**
| Bean ID | Class |
|---------|-------|
| `oauthAuthenticationEntryPoint` | `OAuth2AuthenticationEntryPoint` — realm: `fleetiq360/client` |
| `clientAuthenticationEntryPoint` | `OAuth2AuthenticationEntryPoint` — realm: `fleetiq360/client`, typeName: `Basic` |
| `oauthAccessDeniedHandler` | `OAuth2AccessDeniedHandler` |
| `clientCredentialsTokenEndpointFilter` | `ClientCredentialsTokenEndpointFilter` |
| `accessDecisionManager` | `UnanimousBased` — voters: ScopeVoter, RoleVoter, AuthenticatedVoter |
| `userDetailsService` | `UserDetailsServiceImpl` |
| `clientDetailsUserService` | `ClientDetailsUserDetailsService` |
| `tokenStore` | `JdbcTokenStore` — backed by `dataSource` |
| `tokenServices` | `DefaultTokenServices` — supportRefreshToken: true |
| `userApprovalHandler` | `TokenServicesUserApprovalHandler` |
| `resourceServerFilter` | `oauth:resource-server` — resource-id: `fleetiq360ws` |

**OAuth2 Clients (in-memory / hardcoded):**
| Client ID | Grant Types | Authorities | Scope | Access Token Validity |
|-----------|------------|-------------|-------|-----------------------|
| `987654321` | password, authorization_code, implicit | `ROLE_CLIENT` | read, write | `0` (never expires) |
| `fleetiq360` | password, authorization_code, refresh_token, implicit | `ROLE_DRIVER`, `ROLE_COMPANY_GROUP`, `ROLE_SYS_ADMIN` | read, write | 300s / 300s refresh |

**Authentication Manager:**
- `clientAuthenticationManager`: uses `clientDetailsUserService`
- `authenticationManager` (alias): uses `userDetailsService` with **MD5 password hashing**

**Authorization Server Grant Types:** authorization_code, implicit, refresh_token, client_credentials, password

---

## Test Coverage Analysis

### Test Files Found (3 files total in src/test/java/)

| Test Class | What It Tests | Configuration Relevance |
|-----------|---------------|------------------------|
| `PackageEntryTest` | `PackageEntry.compareTo()` version string comparison | None |
| `APKUpdaterServiceTest` | APK update logic — **all test methods are commented out** | `packageDir` property referenced in commented code only |
| `DateUtilTest` | `DateUtil.parseDateIso()` / `parseDateTimeIso()` | None |

**`src/test/resources/` directory:** Does not exist. No test properties, no test Spring contexts, no test logback configuration.

**Spring test infrastructure:** Zero usage of `@ContextConfiguration`, `@WebAppConfiguration`, `@RunWith(SpringJUnit4ClassRunner.class)`, `MockMvc`, `@SpringBootTest`, or any Spring test annotations across all test files.

**Configuration class coverage:** `Configuration.java`, `BootstrapService.java`, `UserDetailsServiceImpl.java` have zero test coverage.

---

## Findings

---

### ACFG-1
**Severity: CRITICAL**
**File:** `src/main/webapp/WEB-INF/spring/spring-security.xml`
**Finding: OAuth2 client secrets are hardcoded in plain text in source control**

Two OAuth2 clients are defined inline in `spring-security.xml` with their secrets in plain text:
- Client `987654321` with secret `8752361E593A573E86CA558FFD39E`
- Client `fleetiq360` with secret `rihah8eey4faibuengaixo6leiL1awii`

These secrets are committed to the repository and visible to anyone with source access. There are no tests verifying that a secrets-externalization mechanism works correctly, and no integration test validating that token issuance with invalid credentials is rejected.

---

### ACFG-2
**Severity: CRITICAL**
**File:** `settings.xml`
**Finding: Deployment credentials stored in plain text in committed settings.xml**

`settings.xml` contains plain-text passwords for two Tomcat deployment servers:
- `TomcatServerUat` password: `C!1admin`
- `TomcatServerAzure` password: `pyx1s!96`

The UAT password (`C!1admin`) also matches the `flyway.password` defined in `pom.xml` for the UAT profile, suggesting credential reuse across database migration and deployment. This file is committed to the repository. No test verifies that build-time credential handling is secure or isolated.

---

### ACFG-3
**Severity: CRITICAL**
**File:** `src/main/webapp/WEB-INF/spring/spring-security.xml`
**Finding: MD5 used as password hashing algorithm**

The `authenticationManager` configures `<password-encoder hash="md5"/>`. MD5 is a cryptographically broken hash function unsuitable for password storage (no salt, trivially reversible via rainbow tables). There are no tests verifying authentication behavior, no tests confirming rejection of known-bad credentials, and no test for the behavior of `UserDetailsServiceImpl` under any scenario.

---

### ACFG-4
**Severity: CRITICAL**
**File:** `src/main/webapp/WEB-INF/spring/spring-security.xml`
**Finding: OAuth2 client `987654321` has access-token-validity=0 (tokens never expire)**

Client ID `987654321` is granted `access-token-validity="0"`, meaning access tokens issued to this client never expire. Combined with hardcoded credentials and `ROLE_CLIENT` authority (including access to `/rest/apk/**`), this represents an indefinitely valid credential. No test verifies token expiry behavior or validates that expired tokens are rejected.

---

### ACFG-5
**Severity: HIGH**
**File:** `src/main/webapp/WEB-INF/spring/spring-security.xml`
**Finding: `/oauth/cache_approvals` and `/oauth/uncache_approvals` are unsecured in production configuration**

These two URL patterns are annotated with a comment "Just for testing..." and are configured with `security="none"`, meaning they receive no authentication or authorization check. If these endpoints exist in deployed code, they are completely unprotected. There are no tests asserting that access to these endpoints does or does not expose sensitive functionality.

---

### ACFG-6
**Severity: HIGH**
**File:** `src/main/webapp/WEB-INF/web.xml`
**Finding: servlet-context.xml is loaded twice — as root context and as DispatcherServlet context**

`web.xml` specifies `servlet-context.xml` in both:
1. The `<init-param>` of the `appServlet` DispatcherServlet (`contextConfigLocation`)
2. The root `<context-param>` `contextConfigLocation` loaded by `ContextLoaderListener`

This causes all beans defined in `servlet-context.xml` (including `dataSource`, `multipartResolver`, `jsonMessageConverter`, `component-scan`) to be instantiated twice — once in the root context and once in the servlet context. No test exercises the Spring context loading to detect this double-instantiation.

---

### ACFG-7
**Severity: HIGH**
**File:** `src/main/resources/logback.xml`
**Finding: APKUpdaterController is permanently set to DEBUG log level with a comment indicating it is temporary**

The comment in `logback.xml` states: "Temporary enable DEBUG to resolve issue in production environment" but the DEBUG configuration for `com.journaldev.spring.jdbc.controller.APKUpdaterController` remains in the file. DEBUG logging in production risks exposing sensitive request/response data in logs. No test validates the logging configuration or asserts log level behavior.

---

### ACFG-8
**Severity: HIGH**
**File:** `src/main/resources/logback.xml`
**Finding: Duplicate logger declarations and duplicate root elements create undefined log routing**

`logback.xml` declares the `com.journaldev.spring` logger twice (lines 16 and 43) with different appenders and additivity settings. Two `<root>` elements are also declared (lines 28 and 47). XML parsing behavior for duplicate elements is undefined in Logback — the effective configuration depends on parser implementation. The second root declaration (appending to `socket`) may silently override the first (appending to `FILE`), or both may apply. No test validates actual log output routing.

---

### ACFG-9
**Severity: HIGH**
**File:** `pom.xml` (local profile)
**Finding: Duplicate Flyway property keys in the local Maven profile**

The `local` profile in `pom.xml` defines `flyway.url`, `flyway.user`, and `flyway.password` twice each:
- First: `jdbc:postgresql://127.0.0.1/PreStart` / `postgres` / `gmtp-postgres`
- Second (overrides): `jdbc:postgresql://localhost:5432/fleetiq360` / `fleetiq360` / `fleetiq360`

Maven resolves this by using the last defined value. The first set (referencing `PreStart` DB and `gmtp-postgres` password) appears to be leftover from a prior system. No test validates which database target is used in a local build.

---

### ACFG-10
**Severity: HIGH**
**File:** `environment.prod.properties` vs `environment.uat.properties`
**Finding: prod and uat environment property files are identical**

Both `environment.prod.properties` and `environment.uat.properties` contain byte-for-byte identical content, including:
- Same AWS EC2 IP address (`ec2-54-86-82-22.compute-1.amazonaws.com`) as `imageURL` and `systemImageURL`
- Same `imagePrefix=uat-` (not `prod-`)
- Same Cognito credentials

This strongly suggests that a production-specific `environment.prod.properties` was never created. The `prod` Maven profile exists in `pom.xml` but resolves to the UAT environment. No test validates environment-specific configuration values.

---

### ACFG-11
**Severity: HIGH**
**File:** `pom.xml`
**Finding: Spring Framework 3.2.14.RELEASE and Spring Security 3.1.1.RELEASE are end-of-life**

The declared framework versions are significantly outdated:
- Spring Framework 3.2.14.RELEASE — EOL since December 2016
- Spring Security 3.1.1.RELEASE — EOL, predates Spring Security 4.x
- Spring Security OAuth2 1.0.0.RELEASE — EOL; the entire spring-security-oauth project reached end-of-life in May 2022
- Jackson Databind 2.6.7 — EOL, known CVEs (e.g., CVE-2018-7489, CVE-2019-14439)
- JUnit 4.7 — released 2009, missing many later fixes; current is 4.13.x

No tests exercise dependency compatibility or flag version-specific security behaviors.

---

### ACFG-12
**Severity: HIGH**
**File:** `pom.xml`
**Finding: No Spring test dependency or Mockito in test scope — integration tests are structurally impossible**

The only test-scoped dependency is `junit:junit:4.7`. There is no:
- `spring-test` artifact
- `mockito-core` or `mockito-all`
- `h2` or other in-memory database for integration tests
- `httpcomponents` or MockMvc support

Without `spring-test`, no `@ContextConfiguration` or `MockMvc`-based tests can be written or compiled. All existing tests are plain JUnit unit tests with no Spring context. Configuration beans (`Configuration.java`, `BootstrapService.java`, `UserDetailsServiceImpl.java`, all XML-defined beans) cannot be tested with the current dependency set.

---

### ACFG-13
**Severity: HIGH**
**File:** `src/main/webapp/WEB-INF/spring/spring-security.xml`
**Finding: JdbcTokenStore relies on database tables with no test validation of schema**

`tokenStore` is configured as `JdbcTokenStore` backed by the JNDI `dataSource`. The OAuth2 token tables (`oauth_access_token`, `oauth_refresh_token`) must pre-exist in the database. The Flyway migration system (`BootstrapService`) manages schema, but `flyway.enabled=false` in both UAT and prod environments means migrations do not run automatically on those environments. No test validates that the token store schema exists or that token operations succeed.

---

### ACFG-14
**Severity: MEDIUM**
**File:** `src/main/resources/META-INF/context.xml`
**Finding: No JNDI DataSource Resource defined in context.xml**

`context.xml` sets only `antiJARLocking="true"` and `path="/fleetiq360ws"`. The JNDI name `java:comp/env/jdbc/PreStartDB` referenced in `web.xml` (resource-ref) and `servlet-context.xml` (JndiObjectFactoryBean) has no corresponding `<Resource>` element in `context.xml`. The datasource must be configured at the Tomcat server level, outside of version control. No test validates that the JNDI lookup succeeds or that the DataSource is correctly bound.

---

### ACFG-15
**Severity: MEDIUM**
**File:** `src/test/java/com/journaldev/spring/jdbc/service/APKUpdaterServiceTest.java`
**Finding: All substantive test methods in APKUpdaterServiceTest are commented out**

`APKUpdaterServiceTest` contains two test methods (`getAvailablePackage` and `getAvailablePackageWhenAlreadyHaveLatest`) that are entirely commented out. The `@Before` setup method is also commented out. The class compiles to an effectively empty test class. The `packageDir` property (sourced from `environment.*.properties` via `fleetiq360ws.properties`) is exercised only in the commented-out code. No effective tests remain.

---

### ACFG-16
**Severity: MEDIUM**
**File:** `src/main/resources/logback.xml`
**Finding: No test-scoped logback configuration — test log output goes to production log targets**

There is no `src/test/resources/` directory and no `logback-test.xml`. When tests execute, Logback will use the production `logback.xml`, which configures a `RollingFileAppender` writing to `${logDir}/fleetiq360ws.log` and a Splunk TCP appender sending events to `${splunk.host}:${splunk.port}`. If `${logDir}` or the Splunk connection is unavailable during test execution, Logback will emit internal errors but tests will still run — however, test runs may inadvertently send log events to a production Splunk instance.

---

### ACFG-17
**Severity: MEDIUM**
**File:** `src/main/webapp/WEB-INF/spring/appServlet/servlet-context.xml`
**Finding: CommonsMultipartResolver has no test coverage for size limit enforcement**

`multipartResolver` is configured with `maxUploadSize=20971520` (20MB) and `maxInMemorySize=1048576` (1MB). No test validates that uploads exceeding the limit are rejected with an appropriate HTTP response, or that uploads within the limit are accepted. The handling of `MaxUploadSizeExceededException` is untested.

---

### ACFG-18
**Severity: MEDIUM**
**File:** `fleetiq360ws.properties` / `Configuration.java`
**Finding: Configuration.java has zero test coverage — all @Value-injected properties are untested**

`Configuration.java` (`com.journaldev.spring.jdbc.util.Configuration`) exposes 10 `@Value`-injected properties used throughout the application (email subjects, URLs, Cognito credentials). There is no test that:
- Verifies the property file contains all required keys
- Validates that `@Value` bindings resolve correctly
- Tests behavior when a required property is missing (Spring context startup failure)

---

### ACFG-19
**Severity: MEDIUM**
**File:** `src/main/webapp/WEB-INF/spring/spring-security.xml`
**Finding: No test coverage for role-based access control on REST endpoints**

The security configuration defines distinct role requirements for three URL namespaces (`/rest/db/**` → ROLE_SYS_ADMIN only; `/rest/apk/**` → ROLE_CLIENT only; `/rest/**` → four roles). No integration test verifies that:
- A ROLE_DRIVER token cannot access `/rest/db/**`
- A ROLE_CLIENT token cannot access general `/rest/**` endpoints restricted to other roles
- An unauthenticated request is rejected with 401
- An authenticated but unauthorized request returns 403

---

### ACFG-20
**Severity: MEDIUM**
**File:** `pom.xml`
**Finding: Flyway migration SQL separator `__` (double-underscore) is non-default and untested**

`pom.xml` configures `<sqlMigrationSeparator>__</sqlMigrationSeparator>` for the Flyway plugin. The default Flyway separator is `__` so this is consistent, but with `flyway.enabled=false` on both UAT and prod environments, migrations never run automatically on deployed environments. No test exercises Flyway migration execution or validates the migration scripts against a test database.

---

### ACFG-21
**Severity: LOW**
**File:** `pom.xml` — `uat` profile
**Finding: UAT profile is activeByDefault=true, meaning builds without an explicit profile activate UAT**

The `uat` Maven profile has `<activeByDefault>true</activeByDefault>`. A developer running `mvn package` without specifying `-P local` or `-P dev` will build a WAR containing UAT environment configuration, including the UAT AWS RDS URL and UAT Cognito credentials. This is a misconfiguration risk if a developer accidentally deploys a locally built WAR. No CI test enforces correct profile selection.

---

### ACFG-22
**Severity: LOW**
**File:** `fleetiq360ws.properties`
**Finding: `acceptURL` is hardcoded to a production domain and not environment-parameterized**

`acceptURL=https://pandora.fleetiq360.com/pandora/acceptDriver?token=` is a literal value not fed through the Maven filter mechanism, meaning dev and UAT environments send driver acceptance emails containing links to the production Pandora service. This cross-environment URL contamination is not tested.

---

### ACFG-23
**Severity: LOW**
**File:** `environment.dev.properties`
**Finding: Cognito API credentials are default/weak values identical across all environments**

`cognitoAPIUsername=ciiadmin` and `cognitoAPIPassword=ciiadmin` (identical username and password) appear in both `environment.dev.properties` and `environment.uat.properties` / `environment.prod.properties`. These are the same credentials across all environments. No test validates Cognito API authentication behavior or tests failure scenarios for invalid credentials.

---

## Summary Table

| ID | Severity | Config File | Issue |
|----|----------|-------------|-------|
| ACFG-1 | CRITICAL | spring-security.xml | OAuth2 client secrets hardcoded in plain text |
| ACFG-2 | CRITICAL | settings.xml | Deployment passwords in plain text, committed to repo |
| ACFG-3 | CRITICAL | spring-security.xml | MD5 used for password hashing |
| ACFG-4 | CRITICAL | spring-security.xml | OAuth2 client with non-expiring access tokens |
| ACFG-5 | HIGH | spring-security.xml | "Testing" URLs left unsecured in production config |
| ACFG-6 | HIGH | web.xml | servlet-context.xml loaded twice (root + servlet context) |
| ACFG-7 | HIGH | logback.xml | DEBUG logging permanently left enabled for controller |
| ACFG-8 | HIGH | logback.xml | Duplicate logger/root declarations — undefined routing |
| ACFG-9 | HIGH | pom.xml | Duplicate Flyway property keys in local profile |
| ACFG-10 | HIGH | environment.prod.properties | prod and uat property files are identical |
| ACFG-11 | HIGH | pom.xml | EOL framework versions (Spring 3.x, Security 3.x, OAuth 1.x, Jackson 2.6.x) |
| ACFG-12 | HIGH | pom.xml | No spring-test or Mockito — integration tests structurally impossible |
| ACFG-13 | HIGH | spring-security.xml | JdbcTokenStore schema never validated; Flyway disabled on deployed envs |
| ACFG-14 | MEDIUM | context.xml | JNDI DataSource Resource not defined in version-controlled context.xml |
| ACFG-15 | MEDIUM | APKUpdaterServiceTest | All test methods commented out |
| ACFG-16 | MEDIUM | logback.xml | No test logback config — tests may emit to production Splunk |
| ACFG-17 | MEDIUM | servlet-context.xml | Multipart upload size limits untested |
| ACFG-18 | MEDIUM | fleetiq360ws.properties | Configuration.java @Value bindings have zero test coverage |
| ACFG-19 | MEDIUM | spring-security.xml | Role-based access control on REST endpoints untested |
| ACFG-20 | MEDIUM | pom.xml | Flyway migrations disabled on deployed environments, never integration-tested |
| ACFG-21 | LOW | pom.xml | UAT profile is activeByDefault — accidental UAT config in local builds |
| ACFG-22 | LOW | fleetiq360ws.properties | acceptURL hardcoded to production domain across all environments |
| ACFG-23 | LOW | environment.*.properties | Cognito credentials identical across all environments (username = password) |
