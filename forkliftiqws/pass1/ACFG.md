# Pass 1 Security Review — forkliftiqws
**Agent:** ACFG
**Date:** 2026-02-27
**Branch:** master
**Scope:** Configuration and Build files (environment properties, pom.xml, settings.xml, Spring/security XML, logback.xml, web.xml, home.jsp)

---

## Reading Evidence

### environment.dev.properties

| Key | Value |
|-----|-------|
| imageURL | https://forklift360.canadaeast.cloudapp.azure.com:8443/fleetiq360ws/image/ |
| systemImageURL | https://forklift360.canadaeast.cloudapp.azure.com:8443/fleetiq360ws/image/ |
| uploadDir | /var/local/pandora/upload |
| imageDir | image |
| packageDir | /var/local/pandora/apk |
| logDir | /var/local/pandora/logs |
| flyway.baseline | false |
| flyway.enabled | true |
| splunk.host | 127.0.0.1 |
| splunk.port | 15000 |
| imagePrefix | dev- |
| cloudImagedDir | image/ |
| bucketName | forkliftiq360 |
| cognitoAPIPort | 9090 |
| cognitoAPIUsername | ciiadmin |
| cognitoAPIPassword | ciiadmin |

### environment.local.properties.template

| Key | Value |
|-----|-------|
| imageURL | https://localhost:8443/fleetiq360ws/image/ |
| systemImageURL | https://localhost:8443/fleetiq360ws/rest/image/ |
| uploadDir | /home/gmtp/pandora/upload |
| imageDir | image |
| logDir | /home/gmtp/pandora/logs |
| flyway.baseline | false |
| flyway.enabled | false |
| splunk.host | 127.0.0.1 |
| splunk.port | 15000 |
| imagePrefix | loc- |
| cloudImagedDir | image/ |
| bucketName | forkliftiq360 |
| packageDir | /home/gmtp/pandora/apk |
| cognitoAPIPort | 9090 |
| cognitoAPIUsername | ciiadmin |
| cognitoAPIPassword | ciiadmin |

Note: Despite being named `.template`, this file contains real credentials (same as dev) and is committed to git.

### environment.prod.properties

| Key | Value |
|-----|-------|
| imageURL | https://ec2-54-86-82-22.compute-1.amazonaws.com:8443/fleetiq360ws/image/ |
| systemImageURL | https://ec2-54-86-82-22.compute-1.amazonaws.com:8443/fleetiq360ws/image/ |
| uploadDir | /var/local/tomcat8/upload |
| imageDir | image |
| packageDir | /var/local/tomcat8/upload/apk |
| logDir | /var/log/pandora |
| flyway.baseline | false |
| flyway.enabled | false |
| splunk.host | 127.0.0.1 |
| splunk.port | 15000 |
| imagePrefix | uat- |
| cloudImagedDir | image/ |
| bucketName | forkliftiq360 |
| cognitoAPIPort | 9090 |
| cognitoAPIUsername | ciiadmin |
| cognitoAPIPassword | ciiadmin |

Note: `imagePrefix=uat-` in prod properties is anomalous; suggests this file was copied from UAT without being properly updated.

### environment.uat.properties

| Key | Value |
|-----|-------|
| imageURL | https://ec2-54-86-82-22.compute-1.amazonaws.com:8443/fleetiq360ws/image/ |
| systemImageURL | https://ec2-54-86-82-22.compute-1.amazonaws.com:8443/fleetiq360ws/image/ |
| uploadDir | /var/local/tomcat8/upload |
| imageDir | image |
| packageDir | /var/local/tomcat8/upload/apk |
| logDir | /var/log/pandora |
| flyway.baseline | false |
| flyway.enabled | false |
| splunk.host | 127.0.0.1 |
| splunk.port | 15000 |
| imagePrefix | uat- |
| cloudImagedDir | image/ |
| bucketName | forkliftiq360 |
| cognitoAPIPort | 9090 |
| cognitoAPIUsername | ciiadmin |
| cognitoAPIPassword | ciiadmin |

Note: environment.prod.properties and environment.uat.properties are byte-for-byte identical.

### pom.xml

**Properties:**
- `java-version`: 1.8
- `org.springframework-version`: 3.2.14.RELEASE
- `org.aspectj-version`: 1.7.4
- `org.slf4j-version`: 1.7.5
- `jackson.databind-version`: 2.6.7
- `project.build.sourceEncoding`: UTF-8
- `flyway.version`: 5.1.4

**Build profiles:**

| Profile | Key properties |
|---------|---------------|
| local | flyway.url=jdbc:postgresql://127.0.0.1/PreStart, flyway.user=postgres, flyway.password=gmtp-postgres (first block, then overridden); flyway.url=jdbc:postgresql://localhost:5432/fleetiq360, flyway.user=fleetiq360, flyway.password=fleetiq360 |
| dev | flyway.url=jdbc:postgresql://forklift360.canadaeast.cloudapp.azure.com:5432/fleetiq360, flyway.user=fleetiq360, flyway.password=fleetiq360, tomcat.url=http://forklift360.canadaeast.cloudapp.azure.com:8080/manager/text, tomcat.server=TomcatServerAzure |
| prod | flyway.url=jdbc:postgresql://localhost:5432/postgres, tomcat.url=(empty) |
| uat (activeByDefault=true) | flyway.url=jdbc:postgresql://forkliftiq360.cmjwsurtk4tn.us-east-1.rds.amazonaws.com:5432/postgres, flyway.user=dev_admin, flyway.password=C!1admin, tomcat.url=http://ec2-54-86-82-22.compute-1.amazonaws.com:8080/manager/text, tomcat.server=TomcatServerUat |

**Repository:**
- splunk-artifactory: `http://splunk.jfrog.io/splunk/ext-releases-local` (HTTP, not HTTPS)

**Dependencies (selected):**

| Artifact | Version |
|----------|---------|
| spring-jdbc | 3.2.14.RELEASE |
| spring-context | 3.2.14.RELEASE |
| spring-webmvc | 3.2.14.RELEASE |
| jackson-databind | 2.6.7 |
| aspectjrt | 1.7.4 |
| slf4j-api | 1.7.5 |
| logback-classic | 1.2.3 |
| logback-core | 1.2.3 |
| servlet-api | 2.5 (provided) |
| jsp-api | 2.1 (provided) |
| jstl | 1.2 |
| commons-io | 1.3.2 |
| jaxb-api | 2.3.1 |
| jaxb-core | 2.3.0.1 |
| jaxb-impl | 2.3.1 |
| activation | 1.1.1 |
| mail | 1.4.7 (provided) |
| commons-fileupload | 1.3.1 |
| lombok | 1.18.0 |
| tika-core | 1.18 |
| passay | 1.3.1 |
| guava | 27.0-jre |
| junit | 4.7 (test) |
| spring-security-web | 3.1.1.RELEASE |
| spring-security-config | 3.1.1.RELEASE |
| spring-security-oauth2 | 1.0.0.RELEASE |
| simple-xml | 2.7.1 |
| braintree-java | 2.53.0 |
| flyway-core | 5.1.4 |
| splunk-library-javalogging | 1.6.2 |
| commons-lang3 | 3.7 |
| aws-java-sdk | 1.11.163 |
| postgresql (flyway dep) | 9.1-901.jdbc3 |

**Plugins:**
- maven-eclipse-plugin 2.9
- maven-compiler-plugin 2.5.1 (`-Xlint:all`, showWarnings=true, showDeprecation=true)
- maven-war-plugin 3.2.2
- flyway-maven-plugin 5.1.4
- tomcat7-maven-plugin 2.2 (url=${tomcat.url}, server=${tomcat.server})

### settings.xml

**Servers:**

| Server ID | Username | Password |
|-----------|----------|----------|
| TomcatServerUat | maven | C!1admin |
| TomcatServerAzure | maven | pyx1s!96 |

### src/main/resources/META-INF/context.xml

Single element: `<context antiJARLocking="true" path="/fleetiq360ws"/>`

No JNDI DataSource defined here. (DataSource is expected from container via web.xml `<resource-ref>`.)

### src/main/resources/fleetiq360ws.properties

| Key | Value / Note |
|-----|-------------|
| userSetupMsg | Thanks for signing up with ForkliftIQ360... (literal string) |
| userSetupSubject | New User Account Registered |
| passResetSubject | ForkliftIQ360 APP Password Reset |
| driverRequestSubject | ForkliftIQ360 Driver Join Request |
| imageURL | ${imageURL} (filtered from environment properties) |
| systemImageURL | ${systemImageURL} |
| uploadDir | ${uploadDir} |
| imageDir | ${imageDir} |
| packageDir | ${packageDir} |
| acceptURL | https://pandora.fleetiq360.com/pandora/acceptDriver?token= (literal) |
| flyway.baseline | ${flyway.baseline} |
| flyway.enabled | ${flyway.enabled} |
| imagePrefix | ${imagePrefix} |
| cloudImagedDir | ${cloudImagedDir} |
| bucketName | ${bucketName} |
| cognitoAPIPort | ${cognitoAPIPort} |
| cognitoAPIUsername | ${cognitoAPIUsername} |
| cognitoAPIPassword | ${cognitoAPIPassword} |

### src/main/resources/logback.xml

**Appenders:**
- `FILE`: RollingFileAppender
  - file: `${logDir}/fleetiq360ws.log`
  - rollingPolicy: TimeBasedRollingPolicy, pattern `${logDir}/fleetiq360ws.%d.log`, totalSizeCap=3GB
  - encoder pattern: `%d%-4relative [%thread] %-5level %logger{0} - %msg%n`
- `socket`: TcpAppender (Splunk)
  - RemoteHost: `${splunk.host}`, Port: `${splunk.port}`
  - layout pattern: `%-4relative [%thread] %-5level %logger{0} - %msg%n`

**Loggers:**
- `com.journaldev.spring` — INFO, FILE appender
- `com.journaldev.spring.jdbc.controller.APKUpdaterController` — DEBUG, FILE appender (comment says "Temporary enable DEBUG to resolve issue in production environment")
- `com.journaldev.spring` (second, additivity=false) — INFO, socket (Splunk) appender
- root — INFO, FILE appender (line 28-30)
- root — INFO, socket appender (line 47-49) — duplicate root definition

### src/main/webapp/WEB-INF/spring/appServlet/servlet-context.xml

**Beans:**
- `context:property-placeholder` — location: `classpath:fleetiq360ws.properties`
- `annotation-driven` — enables Spring MVC annotation processing
- `resources` — mapping `/resources/**` to `/resources/`
- `InternalResourceViewResolver` — prefix `/WEB-INF/views/`, suffix `.jsp`
- `RequestMappingHandlerAdapter` — messageConverters: [jsonMessageConverter]
- `MappingJackson2HttpMessageConverter` — id=`jsonMessageConverter`
- `CommonsMultipartResolver` — id=`multipartResolver`, maxUploadSize=20971520 (20MB), maxInMemorySize=1048576 (1MB)
- `JndiObjectFactoryBean` — id=`dataSource`, jndiName=`java:comp/env/jdbc/PreStartDB`
- `context:component-scan` — base-package=`com.journaldev.spring.jdbc`

### src/main/webapp/WEB-INF/spring/spring-security.xml

**HTTP blocks:**
1. `/oauth/cache_approvals` — `security="none"` (no security)
2. `/oauth/uncache_approvals` — `security="none"` (no security)
3. `/oauth/token` — stateless, clientAuthenticationManager, IS_AUTHENTICATED_FULLY, http-basic, clientCredentialsTokenEndpointFilter
4. `/rest/**` — create-session="never", intercept-url rules:
   - `/rest/db/**` — ROLE_SYS_ADMIN
   - `/rest/apk/**` — ROLE_CLIENT
   - `/rest/**` — ROLE_DRIVER, ROLE_COMPANY_GROUP, ROLE_SYS_ADMIN, ROLE_CLIENT

**Beans:**
- `oauthAuthenticationEntryPoint` — OAuth2AuthenticationEntryPoint, realm=fleetiq360/client
- `clientAuthenticationEntryPoint` — OAuth2AuthenticationEntryPoint, realm=fleetiq360/client, type=Basic
- `oauthAccessDeniedHandler` — OAuth2AccessDeniedHandler
- `clientCredentialsTokenEndpointFilter` — ClientCredentialsTokenEndpointFilter
- `accessDecisionManager` — UnanimousBased with ScopeVoter, RoleVoter, AuthenticatedVoter
- `clientAuthenticationManager` — authentication-provider: clientDetailsUserService
- `userDetailsService` — UserDetailsServiceImpl
- `authenticationManager` — authentication-provider: userDetailsService, password-encoder hash="md5"
- `clientDetailsUserService` — ClientDetailsUserDetailsService(clientDetails)
- `tokenStore` — JdbcTokenStore(dataSource)
- `tokenServices` — DefaultTokenServices, tokenStore, supportRefreshToken=true, clientDetailsService=clientDetails
- `userApprovalHandler` — TokenServicesUserApprovalHandler(tokenServices)
- `authorization-server` — grant types: authorization_code, implicit, refresh_token, client_credentials, password
- `resourceServerFilter` — resource-id=fleetiq360ws, tokenServices
- `oauth:client-details-service` id=`clientDetails`:
  - client-id=`987654321`, grant-types=password/authorization_code/implicit, secret=`8752361E593A573E86CA558FFD39E`, authorities=ROLE_CLIENT, scope=read/write, access-token-validity=0
  - client-id=`fleetiq360`, grant-types=password/authorization_code/refresh_token/implicit, secret=`rihah8eey4faibuengaixo6leiL1awii`, authorities=ROLE_DRIVER/ROLE_COMPANY_GROUP/ROLE_SYS_ADMIN, scope=read/write, access-token-validity=300, refresh-token-validity=300
- `global-method-security` — pre-post-annotations=enabled, oauthExpressionHandler

### src/main/webapp/WEB-INF/views/home.jsp

- Taglib: `http://java.sun.com/jsp/jstl/core`, prefix `c`
- Page directive: `session="false"`
- No scriptlet blocks (`<% %>`)
- No `<%= %>` expressions
- No `<%@ include %>` directives
- EL expression: `${serverTime}` (line 12) — rendered directly without escaping via `<c:out>`
- No user-controlled input rendered

### src/main/webapp/WEB-INF/web.xml

- Servlet: `appServlet` — DispatcherServlet, contextConfigLocation=/WEB-INF/spring/appServlet/servlet-context.xml, load-on-startup=1
- Servlet-mapping: `appServlet` → `/`
- Context-param `contextConfigLocation`: /WEB-INF/spring/appServlet/servlet-context.xml, /WEB-INF/spring/spring-security.xml
- Listener: `ContextLoaderListener`
- Filter: `springSecurityFilterChain` — DelegatingFilterProxy
- Filter-mapping: `springSecurityFilterChain` → `/*`
- Resource-ref: `jdbc/PreStartDB`, javax.sql.DataSource, Container auth
- Security-constraint: all URLs (`/*`), transport-guarantee=CONFIDENTIAL (requires HTTPS/TLS)

---

## Findings

---

**ACFG-1** — CRITICAL
**Section:** 1. Secrets and Configuration
**File:** settings.xml:9
**Description:** Tomcat manager plaintext passwords committed to the repository. `settings.xml` is tracked in git and contains credentials for two Tomcat server instances (UAT and Azure dev). These credentials allow deployment of arbitrary WAR files to the Tomcat manager API.
**Evidence:**
```xml
<server>
    <id>TomcatServerUat</id>
    <username>maven</username>
    <password>C!1admin</password>
</server>
<server>
    <id>TomcatServerAzure</id>
    <username>maven</username>
    <password>pyx1s!96</password>
</server>
```

---

**ACFG-2** — CRITICAL
**Section:** 1. Secrets and Configuration
**File:** spring-security.xml:113-117
**Description:** OAuth2 client secrets are hardcoded in plaintext in a committed XML configuration file. Any developer or attacker with repository access can obtain these secrets and use them to obtain tokens. The client with `access-token-validity="0"` (client-id `987654321`) issues tokens that never expire.
**Evidence:**
```xml
<oauth:client client-id="987654321" authorized-grant-types="password,authorization_code,implicit"
              secret="8752361E593A573E86CA558FFD39E" authorities="ROLE_CLIENT" scope="read,write" access-token-validity="0"/>

<oauth:client client-id="fleetiq360" authorized-grant-types="password,authorization_code,refresh_token,implicit"
              secret="rihah8eey4faibuengaixo6leiL1awii" authorities="ROLE_DRIVER,ROLE_COMPANY_GROUP,ROLE_SYS_ADMIN" scope="read,write" access-token-validity="300" refresh-token-validity="300"/>
```

---

**ACFG-3** — CRITICAL
**Section:** 1. Secrets and Configuration
**File:** pom.xml:76
**Description:** Production/UAT database password hardcoded in pom.xml build profile. The Flyway UAT profile contains the plaintext password for the AWS RDS PostgreSQL instance, committed to the repository.
**Evidence:**
```xml
<flyway.url>jdbc:postgresql://forkliftiq360.cmjwsurtk4tn.us-east-1.rds.amazonaws.com:5432/postgres</flyway.url>
<flyway.user>dev_admin</flyway.user>
<flyway.password>C!1admin</flyway.password>
```

---

**ACFG-4** — CRITICAL
**Section:** 1. Secrets and Configuration
**File:** pom.xml:28-35
**Description:** Local and dev database passwords hardcoded in pom.xml build profiles. The local profile contains two sets of database credentials (one for `PreStart`, one for `fleetiq360`). The dev profile contains the Azure PostgreSQL password.
**Evidence:**
```xml
<!-- local profile -->
<flyway.password>gmtp-postgres</flyway.password>
...
<flyway.password>fleetiq360</flyway.password>

<!-- dev profile -->
<flyway.password>fleetiq360</flyway.password>
```

---

**ACFG-5** — HIGH
**Section:** 1. Secrets and Configuration
**File:** environment.dev.properties:15-16, environment.uat.properties:14-15, environment.prod.properties:14-15, environment.local.properties.template:14-15
**Description:** Cognito API credentials (`cognitoAPIUsername`/`cognitoAPIPassword`) are hardcoded as the literal value `ciiadmin`/`ciiadmin` across all four environment property files, all of which are tracked in git. This credential governs access to the Cognito API integration component.
**Evidence:**
```
cognitoAPIUsername=ciiadmin
cognitoAPIPassword=ciiadmin
```
(present identically in environment.dev.properties, environment.uat.properties, environment.prod.properties, and environment.local.properties.template)

---

**ACFG-6** — HIGH
**Section:** 1. Secrets and Configuration
**File:** environment.prod.properties (entire file), environment.uat.properties (entire file), environment.dev.properties (entire file)
**Description:** All environment-specific property files — including the production file — are tracked in git and not listed in `.gitignore`. The `.gitignore` only excludes `environment.local.properties`. Any of these files reaching a public or semi-public repository exposes server hostnames, bucket names, and credentials for all environments simultaneously.
**Evidence:**
```
# .gitignore contents — only excludes local:
environment.local.properties

# git ls-files confirms all others are tracked:
environment.dev.properties
environment.local.properties.template
environment.prod.properties
environment.uat.properties
settings.xml
```

---

**ACFG-7** — HIGH
**Section:** 1. Secrets and Configuration
**File:** environment.prod.properties:1-2
**Description:** Production server public IP address (`ec2-54-86-82-22.compute-1.amazonaws.com`) is committed to the repository. This reveals the exact AWS EC2 instance serving production traffic, reducing the effort required for targeted network attacks.
**Evidence:**
```
imageURL=https://ec2-54-86-82-22.compute-1.amazonaws.com:8443/fleetiq360ws/image/
systemImageURL=https://ec2-54-86-82-22.compute-1.amazonaws.com:8443/fleetiq360ws/image/
```

---

**ACFG-8** — HIGH
**Section:** 1. Secrets and Configuration
**File:** pom.xml:73-74
**Description:** Production AWS RDS hostname committed to the repository. The full RDS endpoint `forkliftiq360.cmjwsurtk4tn.us-east-1.rds.amazonaws.com` reveals the AWS account region and RDS instance identifier.
**Evidence:**
```xml
<flyway.url>jdbc:postgresql://forkliftiq360.cmjwsurtk4tn.us-east-1.rds.amazonaws.com:5432/postgres</flyway.url>
```

---

**ACFG-9** — HIGH
**Section:** 2. Authentication and Authorization
**File:** spring-security.xml:74
**Description:** MD5 is used as the password hashing algorithm for user authentication. MD5 is cryptographically broken; it is not a password hashing function (no salt, no cost factor). Passwords can be cracked trivially with rainbow tables or GPU-based attacks.
**Evidence:**
```xml
<authentication-provider user-service-ref="userDetailsService">
    <password-encoder hash="md5"/>
</authentication-provider>
```

---

**ACFG-10** — HIGH
**Section:** 2. Authentication and Authorization
**File:** spring-security.xml:113-114
**Description:** The OAuth2 client `987654321` has `access-token-validity="0"`. In Spring Security OAuth2 1.x, a value of `0` means the token never expires. Any access token issued for this client remains valid indefinitely, eliminating the benefit of short-lived token rotation.
**Evidence:**
```xml
<oauth:client client-id="987654321" authorized-grant-types="password,authorization_code,implicit"
              secret="8752361E593A573E86CA558FFD39E" authorities="ROLE_CLIENT" scope="read,write" access-token-validity="0"/>
```

---

**ACFG-11** — HIGH
**Section:** 2. Authentication and Authorization
**File:** spring-security.xml:13-14
**Description:** Two OAuth endpoints are exposed with `security="none"` and are labelled "Just for testing..." in a comment. These endpoints (`/oauth/cache_approvals`, `/oauth/uncache_approvals`) are completely unauthenticated. Test-only infrastructure left enabled in a production codebase.
**Evidence:**
```xml
<!-- Just for testing... -->
<http pattern="/oauth/cache_approvals" security="none" xmlns="http://www.springframework.org/schema/security" />
<http pattern="/oauth/uncache_approvals" security="none" xmlns="http://www.springframework.org/schema/security" />
```

---

**ACFG-12** — HIGH
**Section:** 2. Authentication and Authorization
**File:** spring-security.xml:28-35
**Description:** The `/rest/**` security block has no CSRF protection configured (no `<csrf>` element). While the `create-session="never"` setting implies stateless API operation, the absence of explicit CSRF configuration combined with Spring Security 3.1.1 (which does not enable CSRF by default) means there is no CSRF protection on any REST endpoint.
**Evidence:**
```xml
<http pattern="/rest/**" create-session="never" entry-point-ref="oauthAuthenticationEntryPoint" xmlns="http://www.springframework.org/schema/security">
    <anonymous enabled="false" />
    <intercept-url pattern="/rest/db/**" access="ROLE_SYS_ADMIN" />
    <intercept-url pattern="/rest/apk/**" access="ROLE_CLIENT" />
    <intercept-url pattern="/rest/**" access="ROLE_DRIVER,ROLE_COMPANY_GROUP,ROLE_SYS_ADMIN,ROLE_CLIENT" />
    <custom-filter ref="resourceServerFilter" before="PRE_AUTH_FILTER" />
    <access-denied-handler ref="oauthAccessDeniedHandler" />
</http>
```

---

**ACFG-13** — HIGH
**Section:** 6. Dependencies
**File:** pom.xml:12
**Description:** Spring Framework 3.2.14.RELEASE is end-of-life and has numerous known CVEs including remote code execution vulnerabilities. This version has not received security patches since 2016. Notable CVEs include CVE-2018-1270 (RCE via STOMP), CVE-2018-1271 (path traversal), CVE-2018-1272 (privilege escalation).
**Evidence:**
```xml
<org.springframework-version>3.2.14.RELEASE</org.springframework-version>
```
Applied to: spring-jdbc, spring-context, spring-webmvc.

---

**ACFG-14** — HIGH
**Section:** 6. Dependencies
**File:** pom.xml:231-237
**Description:** Spring Security 3.1.1.RELEASE is severely outdated (released ~2012, EOL). Multiple critical CVEs affect this version, including CVE-2014-3527 (authentication bypass), CVE-2016-9879 (RegexRequestMatcher bypass). This is over 10 major minor versions behind the current 6.x line.
**Evidence:**
```xml
<groupId>org.springframework.security</groupId>
<artifactId>spring-security-web</artifactId>
<version>3.1.1.RELEASE</version>
...
<groupId>org.springframework.security</groupId>
<artifactId>spring-security-config</artifactId>
<version>3.1.1.RELEASE</version>
```

---

**ACFG-15** — HIGH
**Section:** 6. Dependencies
**File:** pom.xml:15
**Description:** Jackson Databind 2.6.7 has multiple critical deserialization CVEs. This version is affected by CVE-2017-7525, CVE-2017-15095, CVE-2018-7489, CVE-2019-14379, and many others that allow remote code execution via polymorphic type handling.
**Evidence:**
```xml
<jackson.databind-version>2.6.7</jackson.databind-version>
```
Applied to: jackson-databind 2.6.7.

---

**ACFG-16** — HIGH
**Section:** 6. Dependencies
**File:** pom.xml:239-242
**Description:** Spring Security OAuth2 1.0.0.RELEASE is the initial release of this library (circa 2012) and is no longer maintained. CVE-2018-15758 (open redirect) and other vulnerabilities affect the 1.x line. The Spring Security OAuth project reached EOL in 2022.
**Evidence:**
```xml
<groupId>org.springframework.security.oauth</groupId>
<artifactId>spring-security-oauth2</artifactId>
<version>1.0.0.RELEASE</version>
```

---

**ACFG-17** — HIGH
**Section:** 6. Dependencies
**File:** pom.xml:199-202
**Description:** commons-fileupload 1.3.1 is affected by CVE-2016-3092 (DDoS via Multipart), CVE-2014-0050 (DoS), and CVE-2023-24998 (DoS via resource exhaustion). Version 1.3.1 is significantly behind the patched releases.
**Evidence:**
```xml
<groupId>commons-fileupload</groupId>
<artifactId>commons-fileupload</artifactId>
<version>1.3.1</version>
```

---

**ACFG-18** — MEDIUM
**Section:** 4. Session and CSRF
**File:** spring-security.xml (entire file)
**Description:** No security headers are configured anywhere in the Spring Security XML. The `<headers>` element (X-Frame-Options, X-Content-Type-Options, Strict-Transport-Security, X-XSS-Protection) is absent from all HTTP blocks. While web.xml enforces TLS via `CONFIDENTIAL`, HSTS is not set.
**Evidence:** No `<headers>` element present in any `<http>` block in spring-security.xml. The web.xml `<transport-guarantee>CONFIDENTIAL</transport-guarantee>` enforces HTTPS at the servlet container level but does not emit HSTS headers.

---

**ACFG-19** — MEDIUM
**Section:** 4. Session and CSRF
**File:** spring-security.xml (entire file)
**Description:** No CORS configuration is present in the Spring Security XML or servlet-context.xml. CORS behaviour is therefore determined entirely by individual `@CrossOrigin` annotations in controllers (not reviewed in this pass) or defaults to the browser same-origin policy. The absence of a centrally enforced CORS policy is an architectural gap.
**Evidence:** No `<cors>` element or `CorsRegistry` configuration found in any reviewed configuration file.

---

**ACFG-20** — MEDIUM
**Section:** 1. Secrets and Configuration
**File:** environment.prod.properties:12
**Description:** `environment.prod.properties` contains `imagePrefix=uat-`, which is identical to the UAT property file. This indicates the production configuration file was copied directly from UAT without being updated, raising questions about whether other prod-specific values were also incorrectly set from UAT values. This is a configuration integrity issue.
**Evidence:**
```
# environment.prod.properties
imagePrefix=uat-

# environment.uat.properties
imagePrefix=uat-
```

---

**ACFG-21** — MEDIUM
**Section:** 7. Build and CI
**File:** pom.xml:68-70
**Description:** The `uat` Maven profile is set as `activeByDefault=true`. This means a plain `mvn` invocation without specifying a profile will activate the UAT profile, which includes the UAT RDS database URL and credentials. Developers building locally without specifying `-Plocal` will by default target the UAT RDS instance for Flyway migrations.
**Evidence:**
```xml
<profile>
    <id>uat</id>
    <activation>
        <activeByDefault>true</activeByDefault>
    </activation>
```

---

**ACFG-22** — MEDIUM
**Section:** 7. Build and CI
**File:** pom.xml:88-90
**Description:** The Splunk artifact repository uses HTTP (not HTTPS). Dependency resolution over plain HTTP is vulnerable to man-in-the-middle attacks that could substitute malicious artifacts. Maven 3.8.1+ blocks HTTP repositories by default, but this pom.xml does not enforce that.
**Evidence:**
```xml
<repository>
    <id>splunk-artifactory</id>
    <name>Splunk Releases</name>
    <url>http://splunk.jfrog.io/splunk/ext-releases-local</url>
</repository>
```

---

**ACFG-23** — MEDIUM
**Section:** 6. Dependencies
**File:** pom.xml:271-273
**Description:** AWS Java SDK 1.11.163 is outdated. Version 1.11.163 was released in 2017 and numerous CVEs have been filed against old 1.11.x releases. The 1.x SDK is also in maintenance mode; AWS has released the 2.x SDK. This version predates fixes for credential exposure issues in older SDK versions.
**Evidence:**
```xml
<groupId>com.amazonaws</groupId>
<artifactId>aws-java-sdk</artifactId>
<version>1.11.163</version>
```

---

**ACFG-24** — MEDIUM
**Section:** 6. Dependencies
**File:** pom.xml:208-210
**Description:** Apache Tika 1.18 is affected by CVE-2018-1335 (header injection via SMTP) and CVE-2019-10094 (excessive processing). Tika 1.18 was released in 2018 and has since received security patches up through the 2.x line.
**Evidence:**
```xml
<groupId>org.apache.tika</groupId>
<artifactId>tika-core</artifactId>
<version>1.18</version>
```

---

**ACFG-25** — MEDIUM
**Section:** 5. Data Exposure
**File:** logback.xml:21-23
**Description:** A DEBUG logger is enabled for `APKUpdaterController` with a comment stating "Temporary enable DEBUG to resolve issue in production environment." DEBUG logging in production may emit detailed request parameters, stack traces, and internal state that should not appear in production logs. This configuration appears to have been left in place after the debugging session.
**Evidence:**
```xml
<!-- Temporary enable DEBUG to resolve issue in production environment -->
<logger name="com.journaldev.spring.jdbc.controller.APKUpdaterController" level="DEBUG">
    <appender-ref ref="FILE" />
</logger>
```

---

**ACFG-26** — MEDIUM
**Section:** 6. Dependencies
**File:** pom.xml:335-338
**Description:** The Flyway Maven plugin uses PostgreSQL JDBC driver version 9.1-901.jdbc3, which is an extremely old version (circa 2011). This version lacks security patches applied over the following decade and does not support modern PostgreSQL authentication protocols (SCRAM-SHA-256).
**Evidence:**
```xml
<dependency>
    <groupId>postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <version>9.1-901.jdbc3</version>
</dependency>
```

---

**ACFG-27** — LOW
**Section:** 4. Session and CSRF
**File:** web.xml:38-46
**Description:** The `<security-constraint>` with `CONFIDENTIAL` transport guarantee enforces HTTPS at the container level, which is positive. However, the Spring Security configuration does not enforce `requires-channel="https"`, meaning the HTTPS enforcement depends entirely on the container configuration and could be bypassed if the app is deployed without the constraint active.
**Evidence:**
```xml
<security-constraint>
    <web-resource-collection>
        <web-resource-name>Rest Application</web-resource-name>
        <url-pattern>/*</url-pattern>
    </web-resource-collection>
    <user-data-constraint>
        <transport-guarantee>CONFIDENTIAL</transport-guarantee>
    </user-data-constraint>
</security-constraint>
```

---

**ACFG-28** — LOW
**Section:** 3. Input Validation and Injection
**File:** src/main/webapp/WEB-INF/views/home.jsp:12
**Description:** The EL expression `${serverTime}` is rendered without using `<c:out>` escaping. While `serverTime` is likely a server-generated timestamp (not user input), this pattern is worth flagging as the unescaped EL pattern could become a risk if the attribute name or binding changes. No scriptlet blocks or `<%= %>` expressions were found.
**Evidence:**
```jsp
<P>  The time on the server is ${serverTime}. </P>
```

---

**ACFG-29** — LOW
**Section:** 7. Build and CI
**File:** pom.xml (entire file)
**Description:** No Bitbucket Pipelines configuration file (`bitbucket-pipelines.yml`) is present in the repository. There is no evidence of automated CI/CD with enforced test execution. Build, test, and deployment steps cannot be audited for `-DskipTests` or secret injection practices.
**Evidence:** `bitbucket-pipelines.yml` not found via repository file listing.

---

**ACFG-30** — LOW
**Section:** 5. Data Exposure
**File:** logback.xml:4-50
**Description:** The log pattern `%msg%n` logs the full message string with no field-level filtering. If any application code logs operator names, equipment serial numbers, GPS coordinates, or other PII/sensitive telemetry at INFO or DEBUG level, those values will appear verbatim in both the file log and the Splunk TCP stream. No PII-scrubbing pattern or masking appender is configured.
**Evidence:**
```xml
<pattern>%d%-4relative [%thread] %-5level %logger{0} - %msg%n</pattern>
```

---

**ACFG-31** — INFO
**Section:** 1. Secrets and Configuration
**File:** environment.local.properties.template:1-16
**Description:** The file is named `.template` but contains real credential values (`cognitoAPIUsername=ciiadmin`, `cognitoAPIPassword=ciiadmin`) rather than placeholder tokens (e.g., `${COGNITO_API_PASSWORD}`). A template file should contain only placeholder values to be safe to commit; this one commits working credentials.
**Evidence:**
```
cognitoAPIUsername=ciiadmin
cognitoAPIPassword=ciiadmin
```

---

**ACFG-32** — INFO
**Section:** 2. Authentication and Authorization
**File:** spring-security.xml:116-117
**Description:** The `fleetiq360` OAuth2 client has `refresh-token-validity="300"` (5 minutes). This is an unusually short refresh token lifetime and may cause excessive re-authentication friction for mobile clients, potentially leading developers to work around the auth layer. Noted for review rather than as a vulnerability.
**Evidence:**
```xml
<oauth:client client-id="fleetiq360" ... access-token-validity="300" refresh-token-validity="300"/>
```

---

## Summary Table

| ID | Severity | Section | File |
|----|----------|---------|------|
| ACFG-1 | CRITICAL | Secrets and Configuration | settings.xml:9 |
| ACFG-2 | CRITICAL | Secrets and Configuration | spring-security.xml:113-117 |
| ACFG-3 | CRITICAL | Secrets and Configuration | pom.xml:76 |
| ACFG-4 | CRITICAL | Secrets and Configuration | pom.xml:28-35 |
| ACFG-5 | HIGH | Secrets and Configuration | environment.*.properties:14-16 |
| ACFG-6 | HIGH | Secrets and Configuration | .gitignore / git ls-files |
| ACFG-7 | HIGH | Secrets and Configuration | environment.prod.properties:1-2 |
| ACFG-8 | HIGH | Secrets and Configuration | pom.xml:73-74 |
| ACFG-9 | HIGH | Authentication and Authorization | spring-security.xml:74 |
| ACFG-10 | HIGH | Authentication and Authorization | spring-security.xml:113-114 |
| ACFG-11 | HIGH | Authentication and Authorization | spring-security.xml:13-14 |
| ACFG-12 | HIGH | Authentication and Authorization | spring-security.xml:28-35 |
| ACFG-13 | HIGH | Dependencies | pom.xml:12 |
| ACFG-14 | HIGH | Dependencies | pom.xml:231-237 |
| ACFG-15 | HIGH | Dependencies | pom.xml:15 |
| ACFG-16 | HIGH | Dependencies | pom.xml:239-242 |
| ACFG-17 | HIGH | Dependencies | pom.xml:199-202 |
| ACFG-18 | MEDIUM | Session and CSRF | spring-security.xml (entire) |
| ACFG-19 | MEDIUM | Session and CSRF | spring-security.xml (entire) |
| ACFG-20 | MEDIUM | Secrets and Configuration | environment.prod.properties:12 |
| ACFG-21 | MEDIUM | Build and CI | pom.xml:68-70 |
| ACFG-22 | MEDIUM | Build and CI | pom.xml:88-90 |
| ACFG-23 | MEDIUM | Dependencies | pom.xml:271-273 |
| ACFG-24 | MEDIUM | Dependencies | pom.xml:208-210 |
| ACFG-25 | MEDIUM | Data Exposure | logback.xml:21-23 |
| ACFG-26 | MEDIUM | Dependencies | pom.xml:335-338 |
| ACFG-27 | LOW | Session and CSRF | web.xml:38-46 |
| ACFG-28 | LOW | Input Validation and Injection | home.jsp:12 |
| ACFG-29 | LOW | Build and CI | (file absent) |
| ACFG-30 | LOW | Data Exposure | logback.xml:4-50 |
| ACFG-31 | INFO | Secrets and Configuration | environment.local.properties.template |
| ACFG-32 | INFO | Authentication and Authorization | spring-security.xml:116-117 |

**Totals:** 4 CRITICAL, 9 HIGH, 9 MEDIUM, 3 LOW, 2 INFO
