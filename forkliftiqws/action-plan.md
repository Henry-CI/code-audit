# Action Plan — forkliftiqws

| Field | Value |
|-------|-------|
| **Repository** | forkliftiqws |
| **Branch** | master |
| **Audit Date** | 2026-02-27 |
| **Audit Namespace** | 2026-02-27-01 |

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 186 |
| HIGH | 537 |
| MEDIUM | 573 |
| LOW | 386 |
| INFO | 109 |
| **Total** | **1791** |

---

## Pass 1 — Security


[P1-ACFG-1] CRITICAL | File: settings.xml | Line: 9
Description: Tomcat manager plaintext passwords committed to the repository. settings.xml contains credentials for two Tomcat server instances (UAT and Azure dev), enabling deployment of arbitrary WAR files.
Fix: Remove settings.xml from version control. Add to .gitignore. Store Tomcat manager credentials in CI/CD secrets or a vault. Rotate both passwords immediately.

[P1-ACFG-2] CRITICAL | File: spring-security.xml | Line: 113-117
Description: OAuth2 client secrets hardcoded in plaintext in committed XML. Client 987654321 has access-token-validity=0 (tokens never expire).
Fix: Move client secrets to externalized configuration (environment variables or vault). Rotate both client secrets. Set a finite access-token-validity on all clients.

[P1-ACFG-3] CRITICAL | File: pom.xml | Line: 76
Description: Production/UAT database password (C!1admin) for AWS RDS PostgreSQL hardcoded in pom.xml build profile.
Fix: Remove database credentials from pom.xml. Use environment variables or Maven settings with encrypted passwords. Rotate the RDS password immediately.

[P1-ACFG-4] CRITICAL | File: pom.xml | Line: 28-35
Description: Local and dev database passwords hardcoded in pom.xml build profiles (gmtp-postgres, fleetiq360).
Fix: Remove all database credentials from pom.xml. Use Maven settings.xml (excluded from VCS) or environment variables for all profiles.

[P1-ACFG-5] HIGH | File: environment.*.properties | Line: 15-16
Description: Cognito API credentials (ciiadmin/ciiadmin) hardcoded identically across all four environment property files, all tracked in git.
Fix: Externalize Cognito credentials to a secrets manager or environment variables. Use unique credentials per environment. Remove from VCS.

[P1-ACFG-6] HIGH | File: .gitignore
Description: All environment-specific property files (dev, prod, uat) are tracked in git. Only environment.local.properties is excluded. This exposes server hostnames, bucket names, and credentials for all environments.
Fix: Add environment.dev.properties, environment.prod.properties, environment.uat.properties, and settings.xml to .gitignore. Use git filter-branch or BFG to purge from history.

[P1-ACFG-7] HIGH | File: environment.prod.properties | Line: 1-2
Description: Production server public IP address (ec2-54-86-82-22.compute-1.amazonaws.com) committed to the repository, revealing the exact AWS EC2 instance.
Fix: Use a load balancer or DNS alias instead of direct EC2 hostname. Remove production infrastructure details from committed config.

[P1-ACFG-8] HIGH | File: pom.xml | Line: 73-74
Description: Production AWS RDS hostname (forkliftiq360.cmjwsurtk4tn.us-east-1.rds.amazonaws.com) committed, revealing AWS account region and RDS instance identifier.
Fix: Move database connection URLs to externalized configuration. Remove from pom.xml profiles.

[P1-ACFG-9] HIGH | File: spring-security.xml | Line: 74
Description: MD5 used as password hashing algorithm. MD5 is cryptographically broken with no salt or cost factor. Passwords can be cracked trivially with rainbow tables.
Fix: Migrate to bcrypt or Argon2id password encoder. Re-hash all stored passwords on next user login.

[P1-ACFG-10] HIGH | File: spring-security.xml | Line: 113-114
Description: OAuth2 client 987654321 has access-token-validity=0, meaning tokens never expire. Eliminates benefit of short-lived token rotation.
Fix: Set a finite token validity (e.g., 3600 seconds). Implement token refresh flow for long-lived sessions.

[P1-ACFG-11] HIGH | File: spring-security.xml | Line: 13-14
Description: Two OAuth endpoints (/oauth/cache_approvals, /oauth/uncache_approvals) exposed with security="none", labelled "Just for testing." Test infrastructure left enabled in production.
Fix: Remove or secure these endpoints. If needed for testing, gate behind a feature flag or separate profile.

[P1-ACFG-12] HIGH | File: spring-security.xml | Line: 28-35
Description: No CSRF protection configured on any REST endpoint. Spring Security 3.1.1 does not enable CSRF by default.
Fix: For stateless OAuth2 bearer-token APIs, CSRF is typically not required if no cookie-based auth is used. Verify no cookie auth exists; if it does, enable CSRF protection.

[P1-ACFG-13] HIGH | File: pom.xml | Line: 12
Description: Spring Framework 3.2.14.RELEASE is EOL (no patches since 2016). Affected by CVE-2018-1270 (RCE), CVE-2018-1271 (path traversal), CVE-2018-1272 (privilege escalation).
Fix: Upgrade to Spring Framework 6.x (or at minimum 5.3.x LTS). This requires Java 17+ and significant migration effort.

[P1-ACFG-14] HIGH | File: pom.xml | Line: 231-237
Description: Spring Security 3.1.1.RELEASE is severely outdated (~2012). Affected by CVE-2014-3527 (auth bypass), CVE-2016-9879 (matcher bypass).
Fix: Upgrade to Spring Security 6.x alongside the Spring Framework upgrade.

[P1-ACFG-15] HIGH | File: pom.xml | Line: 15
Description: Jackson Databind 2.6.7 has multiple critical deserialization RCE CVEs (CVE-2017-7525, CVE-2017-15095, CVE-2018-7489, CVE-2019-14379).
Fix: Upgrade to Jackson Databind 2.17.x or later. Enable default typing restrictions.

[P1-ACFG-16] HIGH | File: pom.xml | Line: 239-242
Description: Spring Security OAuth2 1.0.0.RELEASE (circa 2012) is unmaintained. Affected by CVE-2018-15758 (open redirect). Project reached EOL in 2022.
Fix: Migrate to Spring Security 6.x built-in OAuth2 resource server support.

[P1-ACFG-17] HIGH | File: pom.xml | Line: 199-202
Description: commons-fileupload 1.3.1 is affected by CVE-2016-3092 (DDoS), CVE-2014-0050 (DoS), CVE-2023-24998 (resource exhaustion).
Fix: Upgrade to commons-fileupload 1.5+ or migrate to Spring built-in multipart handling.

[P1-ACFG-18] MEDIUM | File: spring-security.xml
Description: No security headers configured (X-Frame-Options, X-Content-Type-Options, HSTS, X-XSS-Protection). HSTS not set despite TLS enforcement in web.xml.
Fix: Add <headers> element to Spring Security HTTP blocks with defaults-enabled, or add HSTS, X-Frame-Options, X-Content-Type-Options explicitly.

[P1-ACFG-19] MEDIUM | File: spring-security.xml
Description: No centralized CORS configuration. CORS behavior depends entirely on individual @CrossOrigin annotations or browser same-origin policy.
Fix: Add a centralized CORS configuration bean or <cors> element defining allowed origins, methods, and headers.

[P1-ACFG-20] MEDIUM | File: environment.prod.properties | Line: 12
Description: Production config contains imagePrefix=uat-, identical to UAT. Indicates prod config was copied from UAT without update.
Fix: Audit all prod property values against UAT. Set imagePrefix to prod- or appropriate value.

[P1-ACFG-21] MEDIUM | File: pom.xml | Line: 68-70
Description: UAT Maven profile is activeByDefault=true. A plain mvn invocation targets the UAT RDS instance for Flyway migrations.
Fix: Remove activeByDefault. Require explicit profile selection (-P) for all environments.

[P1-ACFG-22] MEDIUM | File: pom.xml | Line: 88-90
Description: Splunk artifact repository uses HTTP (not HTTPS), vulnerable to MITM attacks substituting malicious artifacts.
Fix: Change repository URL to https://splunk.jfrog.io/... or use a secure internal mirror.

[P1-ACFG-23] MEDIUM | File: pom.xml | Line: 271-273
Description: AWS Java SDK 1.11.163 (2017) is outdated and in maintenance mode. Pre-dates security fixes in later 1.11.x releases.
Fix: Upgrade to AWS SDK 2.x. If not feasible, upgrade to latest 1.11.x.

[P1-ACFG-24] MEDIUM | File: pom.xml | Line: 208-210
Description: Apache Tika 1.18 is affected by CVE-2018-1335 (header injection) and CVE-2019-10094 (excessive processing).
Fix: Upgrade to Tika 2.x.

[P1-ACFG-25] MEDIUM | File: logback.xml | Line: 21-23
Description: DEBUG logger left enabled for APKUpdaterController with comment "Temporary enable DEBUG to resolve issue in production." May emit sensitive request details.
Fix: Remove or set to INFO. Use dynamic log level management for future debugging needs.

[P1-ACFG-26] MEDIUM | File: pom.xml | Line: 335-338
Description: PostgreSQL JDBC driver 9.1-901.jdbc3 (circa 2011) in Flyway plugin. Lacks modern auth protocols (SCRAM-SHA-256).
Fix: Upgrade to org.postgresql:postgresql 42.7.x.

[P1-ACFG-27] LOW | File: web.xml | Line: 38-46
Description: HTTPS enforcement relies solely on container-level transport-guarantee. Spring Security does not enforce requires-channel="https".
Fix: Add requires-channel="https" to Spring Security intercept-url patterns as defense-in-depth.

[P1-ACFG-28] LOW | File: home.jsp | Line: 12
Description: EL expression ${serverTime} rendered without <c:out> escaping. Currently server-generated but pattern could become risky if binding changes.
Fix: Wrap in <c:out value="${serverTime}"/> for defense-in-depth.

[P1-ACFG-29] LOW | File: (absent)
Description: No CI/CD pipeline configuration (bitbucket-pipelines.yml) exists. Build, test, and deployment steps cannot be audited.
Fix: Create a CI/CD pipeline enforcing test execution, static analysis, and secret scanning.

[P1-ACFG-30] LOW | File: logback.xml | Line: 4-50
Description: Log pattern logs full message with no field-level PII filtering. If code logs PII at INFO/DEBUG, it appears verbatim in file and Splunk.
Fix: Add a PII-masking pattern or filter appender. Audit log statements for sensitive data.

[P1-ACFG-31] INFO | File: environment.local.properties.template
Description: Template file contains real credentials (ciiadmin/ciiadmin) instead of placeholder tokens.
Fix: Replace values with placeholders like ${COGNITO_API_PASSWORD}.

[P1-ACFG-32] INFO | File: spring-security.xml | Line: 116-117
Description: OAuth2 client fleetiq360 has refresh-token-validity=300 (5 minutes), unusually short for mobile clients.
Fix: Review token lifetimes against UX requirements. Consider longer refresh tokens with rotation.

[P1-B01-1] CRITICAL | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 113
Description: OAuth2 client secrets are hardcoded in plaintext in a committed configuration file, granting repository readers working credentials with the highest roles.
Fix: Move OAuth2 client secrets to environment variables or a secrets manager and reference them via property placeholders. Rotate all exposed secrets immediately.

[P1-B01-2] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 74
Description: The authentication provider uses MD5 as the password hashing algorithm, which is cryptographically broken with no salt and trivially reversed via rainbow tables.
Fix: Replace MD5 with bcrypt or Argon2 via a modern Spring Security PasswordEncoder. Rehash all stored passwords on next login.

[P1-B01-3] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 13
Description: Two OAuth approval endpoints are configured with security="none" and a comment stating they are for testing, leaving them fully unauthenticated in production.
Fix: Remove the security="none" declarations for /oauth/cache_approvals and /oauth/uncache_approvals, or remove the endpoints entirely.

[P1-B01-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 37
Description: IDOR vulnerability where GET /rest/company/get/{uid} passes the uid path variable directly to the DAO without verifying the authenticated user's identity matches uid.
Fix: Extract the authenticated principal's identity and verify it matches or has authority over the requested uid before returning data.

[P1-B01-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 44
Description: IDOR vulnerability where GET /rest/company/owner/{uid}/drivers returns all drivers for any company owner without an ownership check.
Fix: Verify the authenticated user is the company owner or belongs to the same organisation before returning driver data.

[P1-B01-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 148
Description: IDOR vulnerability where PUT /rest/company/accept/{pid} unconditionally enables any permission record without verifying ownership.
Fix: Add an ownership check verifying the permission record belongs to a company administered by the authenticated user.

[P1-B01-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 163
Description: IDOR vulnerability where PUT /rest/company/delete/{pid} deletes any permission record by ID without ownership verification.
Fix: Add an ownership check verifying the permission record belongs to the authenticated user's company before deletion.

[P1-B01-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: 38
Description: findByName uses the wrong JdbcTemplate.queryForObject overload, causing a runtime ClassCastException that indicates the method has never been tested.
Fix: Replace the scalar-type overload with a RowMapper-based overload that maps the result set to a Driver object.

[P1-B01-9] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: 28
Description: checkKey() always returns true regardless of the supplied key, meaning any API key check relying on this method provides no access control.
Fix: Implement actual API key validation against the database, or remove the method if it is not needed.

[P1-B01-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 87
Description: The company search endpoint returns matching companies from the entire database with no tenant scoping, allowing any authenticated user to enumerate all company data.
Fix: Add an organisation/tenant filter to the search query so users can only see companies they are authorised to view.

[P1-B01-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: N/A
Description: No input validation annotations (@Valid, @NotNull, @Size) are applied to any DAO method parameters or model classes, allowing unbounded or null inputs.
Fix: Add JSR-303/JSR-380 constraint annotations to model classes and @Valid annotations to controller method parameters.

[P1-B01-12] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 121
Description: The web-based company acceptance token is a predictable MD5 hash of the permission ID and creation timestamp, allowing token forgery.
Fix: Replace the MD5-based token with a cryptographically random token (e.g., SecureRandom) or an HMAC with a server-side secret key.

[P1-B01-13] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Company.java | Line: 23
Description: The Company model includes a password field with no @JsonIgnore, causing MD5-hashed passwords to be included in all JSON API responses.
Fix: Add @JsonIgnore to the password field in Company.java, or exclude the password column from SELECT queries used in API responses.

[P1-B01-14] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 25
Description: The Driver model exposes password, securityno (social security number), and licno (licence number) fields with no @JsonIgnore in JSON responses.
Fix: Add @JsonIgnore to the password, securityno, and licno fields, or use a response DTO that excludes sensitive fields.

[P1-B01-15] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Permissions.java | Line: 28
Description: The Permissions model exposes the gsm_token (mobile push notification token) field with no @JsonIgnore in company lookup responses.
Fix: Add @JsonIgnore to the gsm_token field in the Permissions model.

[P1-B01-16] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 154
Description: CompanyResultResetExtractor calls setArrRoles on a potentially null object when the query returns zero rows, causing a NullPointerException and possible stack trace leakage.
Fix: Add a null check on the company object before calling setArrRoles, and return null or Optional.empty() for empty result sets.

[P1-B01-17] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: 29
Description: The checkKey method logs the full API key value at INFO level on every invocation, exposing secrets in production logs.
Fix: Remove the API key value from log statements, or log only a masked/truncated representation.

[P1-B02-1] HIGH | File: environment.dev.properties | Line: 15
Description: Cognito API credentials are hardcoded as literal values in all three environment property files committed to source control.
Fix: Move credentials to a secrets manager or environment variables. Add environment property files to .gitignore and remove from git history.

[P1-B02-2] HIGH | File: pom.xml | Line: 28
Description: Database passwords are hardcoded in Maven build profile properties for local and UAT environments, committed to source control.
Fix: Remove database credentials from pom.xml. Use environment variables or Maven settings.xml with encrypted passwords.

[P1-B02-3] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 117
Description: The OAuth2 client secret for the fleetiq360 client is hardcoded in the Spring Security XML configuration committed to source control.
Fix: Externalize OAuth2 client secrets using property placeholders resolved from environment variables or a secrets manager.

[P1-B02-4] MEDIUM | File: pom.xml | Line: 73
Description: The production AWS RDS hostname is hardcoded in the UAT Flyway URL, leaking infrastructure topology to anyone with repository access.
Fix: Remove the RDS hostname from pom.xml. Use environment-specific property substitution or a secrets manager for database URLs.

[P1-B02-5] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 107
Description: IDOR vulnerability where findByID looks up a driver record using only the supplied userId with no organisation filter, allowing any authenticated user to retrieve full PII for any driver.
Fix: Add organisation scoping to the query and verify the authenticated user belongs to the same company as the requested driver.

[P1-B02-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 151
Description: IDOR vulnerability where findAllTraining queries driver_training using only driver_id with no company scoping, exposing training records for any driver.
Fix: Add a company ownership check to ensure the caller can only access training records for drivers in their organisation.

[P1-B02-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 132
Description: IDOR vulnerability where uploadProfile and uploadProfileAPP update any driver's photo_url using the uid path variable without verifying caller identity.
Fix: Verify the authenticated user's identity matches the uid parameter before allowing the photo update.

[P1-B02-8] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 235
Description: IDOR vulnerability where saveLicence updates licence number, expiry date, address, and security number for any driver using user.getId() from the request body without ownership verification.
Fix: Verify the authenticated user's identity matches the target driver ID before allowing PII updates.

[P1-B02-9] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 253
Description: IDOR vulnerability where updateDrivers modifies first_name, last_name, and compliance_date for any driver using driver.getId() from the request body without ownership check.
Fix: Verify the authenticated user owns the target driver record before allowing updates.

[P1-B02-10] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 187
Description: IDOR vulnerability where saveEmails and getEmails operate on driver_emails using driver_id from the request body or uid from the path without ownership verification.
Fix: Add ownership checks to verify the authenticated user is the target driver before allowing email read or write operations.

[P1-B02-11] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 108
Description: IDOR vulnerability where acceptDrivers and declineDriver operate on permission records by ID with no check that the authenticated user administers the associated company.
Fix: Verify the authenticated user has administrative authority over the company associated with each permission record.

[P1-B02-12] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 89
Description: The password reset endpoint allows any authenticated driver to trigger a password reset for any other driver's account by supplying their email address.
Fix: Require the caller to be the account owner or an administrator, or implement a self-service reset flow that sends a reset link to the account's own email.

[P1-B02-13] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 75
Description: The driver registration endpoint is accessible to any authenticated user including ROLE_DRIVER, allowing regular drivers to register new accounts without admin approval.
Fix: Restrict the registration endpoint to ROLE_SYS_ADMIN or ROLE_COMPANY_GROUP using @PreAuthorize.

[P1-B02-14] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 56
Description: The deprecated authentication endpoint POST /rest/appuser/validate is still mapped and reachable at runtime, using MD5-hashed authentication.
Fix: Remove the deprecated endpoint from the codebase entirely, not just annotate it @Deprecated.

[P1-B02-15] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 114
Description: OAuth2 client 987654321 is configured with access-token-validity="0", meaning tokens never expire and a compromised token remains permanently valid.
Fix: Set a reasonable access token validity (e.g., 300 seconds) and implement token revocation support.

[P1-B02-16] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: N/A
Description: No @Valid annotation is present on any @RequestBody parameter in DriverController, and the Driver model has no JSR-303 constraint annotations.
Fix: Add @Valid to all @RequestBody parameters and add constraint annotations (@NotNull, @Size, @Pattern) to model fields.

[P1-B02-17] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 74
Description: Passwords are stored and compared using unsalted MD5, which is cryptographically broken and trivially reversible via rainbow tables.
Fix: Migrate to bcrypt or Argon2 password hashing. Rehash stored passwords on next user login.

[P1-B02-18] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: N/A
Description: No HTTP security headers (X-Frame-Options, X-Content-Type-Options, Strict-Transport-Security) are configured in the Spring Security XML.
Fix: Add a headers element to the Spring Security configuration or upgrade to a version that provides these headers by default.

[P1-B02-19] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 25
Description: The Driver model serializes password and securityno fields in all JSON responses due to missing @JsonIgnore annotations.
Fix: Add @JsonIgnore to the password and securityno fields in Driver.java, or use a response DTO.

[P1-B02-20] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 70
Description: SQLException messages include driver IDs and email addresses, which may be exposed to clients if no global exception handler sanitizes them.
Fix: Use generic error messages in exceptions. Log the detailed error server-side and return a generic error response to clients.

[P1-B02-21] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 60
Description: Multiple controller methods log the full Gson-serialized Driver request body at INFO level, including password, email, licno, securityno, and addr.
Fix: Remove sensitive fields from log output. Use a logging DTO or redact sensitive fields before serialization.

[P1-B02-22] CRITICAL | File: pom.xml | Line: 13
Description: Spring Framework 3.2.14.RELEASE is end-of-life since December 2016 and affected by multiple critical CVEs.
Fix: Upgrade Spring Framework to a currently supported version (e.g., Spring 6.x with Spring Boot 3.x).

[P1-B02-23] CRITICAL | File: pom.xml | Line: 231
Description: Spring Security 3.1.1.RELEASE is end-of-life since 2016 and contains multiple known vulnerabilities.
Fix: Upgrade Spring Security to a currently supported version (e.g., Spring Security 6.x).

[P1-B02-24] HIGH | File: pom.xml | Line: 15
Description: Jackson Databind 2.6.7 is affected by numerous deserialization CVEs that can allow remote code execution.
Fix: Upgrade Jackson Databind to the latest 2.x release (currently 2.17+).

[P1-B02-25] HIGH | File: pom.xml | Line: 241
Description: Spring Security OAuth2 1.0.0.RELEASE is extremely old with known vulnerabilities including CVE-2018-15758.
Fix: Migrate to Spring Authorization Server or upgrade to the latest supported Spring Security OAuth2 version.

[P1-B02-26] MEDIUM | File: pom.xml | Line: 272
Description: AWS Java SDK 1.11.163 is significantly outdated (circa 2017) with multiple security advisories.
Fix: Upgrade to the latest AWS SDK v2 or at minimum the latest v1 release.

[P1-B02-27] MEDIUM | File: pom.xml | Line: 199
Description: commons-fileupload 1.3.1 is affected by CVE-2016-3092 (DoS) and CVE-2014-0050.
Fix: Upgrade commons-fileupload to version 1.5 or later.

[P1-B02-28] MEDIUM | File: pom.xml | Line: 88
Description: The Splunk dependency is fetched from a third-party JFrog repository over plain HTTP, vulnerable to MITM artifact substitution.
Fix: Change the repository URL to use HTTPS.

[P1-B03-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 14
Description: Third-party API credentials (Clickatell SMS username, password, API ID) and a Google Cloud Messaging server key are hardcoded as public static fields committed to source control.
Fix: Move all credentials to a secrets manager or environment variables. Remove from source code and rotate compromised credentials.

[P1-B03-2] HIGH | File: pom.xml | Line: 27
Description: Flyway database credentials are hardcoded in Maven profiles and committed to source control, including UAT RDS credentials.
Fix: Remove credentials from pom.xml and use environment variables or encrypted Maven settings.

[P1-B03-3] HIGH | File: environment.dev.properties | Line: 15
Description: Cognito API credentials are committed in plaintext in all three environment property files tracked by git.
Fix: Move credentials to a secrets manager. Add environment property files to .gitignore.

[P1-B03-4] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 113
Description: OAuth2 in-memory client secrets are hardcoded in a committed configuration file.
Fix: Externalize client secrets via property placeholders resolved from environment variables or a secrets manager.

[P1-B03-5] MEDIUM | File: pom.xml | Line: 44
Description: Azure VM FQDNs, AWS EC2 instance DNS names, and the production AWS RDS endpoint are hardcoded and committed, exposing infrastructure topology.
Fix: Externalize all infrastructure hostnames to environment-specific configuration not tracked in version control.

[P1-B03-6] INFO | File: N/A | Line: N/A
Description: No bitbucket-pipelines.yml found, preventing assessment of CI/CD pipeline configuration and secrets management.
Fix: Create a CI/CD pipeline configuration with proper secrets management.

[P1-B03-7] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 34
Description: IDOR vulnerability where GET /rest/equipment/get/{uid} returns any driver's equipment list without verifying the authenticated caller is that user.
Fix: Verify the authenticated principal matches or has authority over the requested uid before returning equipment data.

[P1-B03-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 122
Description: IDOR vulnerability where GET /rest/service/get/{uid} passes caller-supplied uid into a permission subquery without verifying authenticated session identity.
Fix: Verify the authenticated user's identity matches the uid parameter.

[P1-B03-9] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 83
Description: IDOR vulnerability where saveImpactIMAGE and saveImpactIMAGEAPP accept impId from the URL and update any incident's image or signature without ownership check.
Fix: Verify the incident identified by impId belongs to the authenticated user's organisation before allowing updates.

[P1-B03-10] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 59
Description: IDOR vulnerability where saveIncident inserts an incident record with driver_id and unit_id from the request body without verifying they belong to the caller's company.
Fix: Verify driver_id and unit_id belong to the authenticated user's organisation before inserting the incident.

[P1-B03-11] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 49
Description: IDOR vulnerability where the UPDATE branch of addEquipment modifies any equipment record by id from the request body with no company ownership check.
Fix: Verify the equipment record belongs to the authenticated user's company before allowing updates.

[P1-B03-12] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 142
Description: SaveService accepts unit_id from the request body and performs INSERT/UPDATE to service records without verifying unit ownership.
Fix: Verify the unit belongs to the authenticated user's company before allowing service record modifications.

[P1-B03-13] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 74
Description: MD5 is used as the password hashing algorithm, which is cryptographically broken for password storage.
Fix: Replace MD5 with bcrypt or Argon2 and rehash passwords on next user login.

[P1-B03-14] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 113
Description: OAuth2 client 987654321 is configured with access-token-validity="0", meaning tokens never expire.
Fix: Set a reasonable token expiry (e.g., 300 seconds) and implement token revocation.

[P1-B03-15] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 44
Description: No @Valid annotation or JSR-303 constraint annotations are applied to any @RequestBody parameters in ImpactController or EquipmentController.
Fix: Add @Valid to all @RequestBody parameters and add constraint annotations to model classes.

[P1-B03-16] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: N/A
Description: Spring Security 3.1.1 does not enable CSRF protection by default and no explicit CSRF configuration was found.
Fix: Explicitly configure CSRF posture. For stateless APIs with bearer tokens, document the intentional CSRF exemption.

[P1-B03-17] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: N/A
Description: No X-Frame-Options, X-Content-Type-Options, or Strict-Transport-Security HTTP response headers are configured.
Fix: Add security response headers via Spring Security configuration or a servlet filter.

[P1-B03-18] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java | Line: 75
Description: Operator PII (full name, email, phone) and forklift identifiers are written to application logs at INFO level, forwarded to Splunk.
Fix: Remove PII from log statements or use structured logging with PII redaction.

[P1-B03-19] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 107
Description: e.printStackTrace() is called in multiple catch blocks, writing full stack traces to System.err which may reveal internal details.
Fix: Replace e.printStackTrace() with structured logger calls (e.g., logger.error("message", e)).

[P1-B03-20] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 45
Description: Full request body content including MAC addresses, driver IDs, and serial numbers is serialized to JSON and logged at INFO level.
Fix: Remove or redact sensitive fields from log output.

[P1-B03-21] CRITICAL | File: pom.xml | Line: 13
Description: Spring Framework 3.2.14.RELEASE is end-of-life and falls within the affected range for multiple critical CVEs.
Fix: Upgrade Spring Framework to a currently supported version.

[P1-B03-22] CRITICAL | File: pom.xml | Line: 230
Description: Spring Security 3.1.1.RELEASE is severely outdated (circa 2012) and EOL, lacking numerous security controls.
Fix: Upgrade Spring Security to a currently supported version.

[P1-B03-23] CRITICAL | File: pom.xml | Line: 239
Description: Spring Security OAuth2 1.0.0.RELEASE is severely outdated and EOL, predating all subsequent security patches.
Fix: Migrate to Spring Authorization Server or the latest supported OAuth2 implementation.

[P1-B03-24] HIGH | File: pom.xml | Line: 98
Description: Jackson Databind 2.6.7 has numerous known deserialization CVEs that should be addressed by upgrading.
Fix: Upgrade Jackson Databind to the latest 2.x release.

[P1-B03-25] HIGH | File: pom.xml | Line: 197
Description: commons-fileupload 1.3.1 is vulnerable to CVE-2016-3092 (DoS) and CVE-2014-0050, used directly by CommonsMultipartResolver.
Fix: Upgrade commons-fileupload to version 1.5 or later.

[P1-B03-26] MEDIUM | File: pom.xml | Line: 269
Description: AWS Java SDK 1.11.163 is from 2017 and severely outdated; AWS SDK v1 is in maintenance mode.
Fix: Upgrade to AWS SDK v2 or the latest v1 release.

[P1-B03-27] MEDIUM | File: pom.xml | Line: 86
Description: The Splunk logging library is fetched over plain HTTP from a third-party JFrog Artifactory, allowing MITM artifact substitution.
Fix: Change the repository URL to use HTTPS.

[P1-B03-28] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 117
Description: The type path variable in saveImpactIMAGEAPP is not validated against an allowlist, permitting unauthorized file uploads to S3 with no database record.
Fix: Validate the type parameter against an allowlist (e.g., "image", "signature") and reject unrecognized values.

[P1-B03-29] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 90
Description: The signatureFile Base64 parameter is decoded without enforcing a maximum length, risking excessive heap allocation.
Fix: Enforce a maximum length on the Base64 input before decoding.

[P1-B03-30] INFO | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 13
Description: Two test-only OAuth endpoints are left with security="none" in the production security configuration.
Fix: Remove these test endpoints from the production security configuration.

[P1-B04-1] CRITICAL | File: environment.dev.properties | Line: 15
Description: Plaintext Cognito API credentials committed to the repository and tracked by git across dev, uat, and prod environment files.
Fix: Move credentials to a secrets manager. Add all environment property files to .gitignore and remove from git history.

[P1-B04-2] HIGH | File: pom.xml | Line: 76
Description: Production/UAT database credentials committed in plaintext in pom.xml under the uat Maven profile.
Fix: Remove database credentials from pom.xml. Use environment variables or encrypted Maven settings.

[P1-B04-3] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 113
Description: OAuth2 client secrets hardcoded in plain XML committed to the repository.
Fix: Externalize OAuth2 client secrets to environment variables or a secrets manager.

[P1-B04-4] MEDIUM | File: pom.xml | Line: 27
Description: Additional database passwords committed in the local Maven profile with two conflicting flyway.password entries.
Fix: Remove credentials from pom.xml. Fix the duplicate entry and use environment variables.

[P1-B04-5] MEDIUM | File: pom.xml | Line: 88
Description: Splunk dependency is fetched from a third-party JFrog repository over plain HTTP, creating a MITM risk.
Fix: Change the repository URL to use HTTPS.

[P1-B04-6] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/UserController.java | Line: 22
Description: The /rest/admin/user endpoint is accessible to any authenticated user including ROLE_DRIVER because no specific intercept rule exists for /rest/admin/**.
Fix: Add an intercept-url rule restricting /rest/admin/** to ROLE_SYS_ADMIN, or add @PreAuthorize("hasRole('SYS_ADMIN')") to the controller method.

[P1-B04-7] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 74
Description: MD5 is configured as the password hashing algorithm, which is trivially reversed via rainbow tables and GPU cracking.
Fix: Replace MD5 with bcrypt or Argon2 password hashing.

[P1-B04-8] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 13
Description: Two token-management endpoints are marked security="none" with a comment acknowledging they are for testing.
Fix: Remove or secure these endpoints in the production configuration.

[P1-B04-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/UserController.java | Line: 23
Description: The email request parameter is not validated for format, length, or content before being passed to the DAO.
Fix: Add @Pattern and @Size constraints to the email parameter.

[P1-B04-10] INFO | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: N/A
Description: No HTTP security response headers (X-Frame-Options, X-Content-Type-Options, Strict-Transport-Security) are configured.
Fix: Configure security response headers in Spring Security or via a servlet filter.

[P1-B04-11] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/UserController.java | Line: 27
Description: The /rest/admin/user endpoint returns the full serialized User object including the password hash in the HTTP response body.
Fix: Add @JsonIgnore to the password field in User.java, or use a response DTO that excludes the password.

[P1-B04-12] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 31
Description: UserDAO.findByName performs a global lookup across all organisations with no company scope, enabling cross-organisation user enumeration.
Fix: Add organisation scoping to the query, or restrict the calling endpoint to admin-only access.

[P1-B04-13] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/ManufacturerDAOImpl.java | Line: 33
Description: The manufacturer query returns all records where company_id IS NULL unconditionally, potentially exposing company-private data cross-organisation.
Fix: Confirm whether NULL company_id records are intentionally global. If not, restrict the query to only company-scoped records.

[P1-B04-14] INFO | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 31
Description: The v_apiusers view is referenced but not defined in any tracked Flyway migration scripts, creating a schema governance gap.
Fix: Add the view definition to Flyway migrations to ensure schema is fully tracked in version control.

[P1-B04-15] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: 29
Description: APIDAOImpl.checkKey() logs the raw API key value at INFO level before performing any validation.
Fix: Remove the API key from log output or log only a masked representation.

[P1-B04-16] CRITICAL | File: pom.xml | Line: 12
Description: Core framework dependencies are severely end-of-life: Spring 3.2.14, Spring Security 3.1.1, and Spring Security OAuth2 1.0.0 are all unsupported.
Fix: Upgrade all framework dependencies to currently supported versions.

[P1-B04-17] HIGH | File: pom.xml | Line: 99
Description: Jackson Databind 2.6.7 has multiple published CVEs related to polymorphic deserialization.
Fix: Upgrade Jackson Databind to the latest 2.x release.

[P1-B04-18] HIGH | File: pom.xml | Line: 130
Description: Logback 1.2.3 is vulnerable to CVE-2021-42550, a JNDI injection vulnerability. Fixed in version 1.2.9.
Fix: Upgrade logback-classic and logback-core to version 1.2.13 or later.

[P1-B04-19] MEDIUM | File: pom.xml | Line: 198
Description: commons-fileupload 1.3.1 is vulnerable to CVE-2016-3092 (DoS via crafted multipart request).
Fix: Upgrade commons-fileupload to version 1.5 or later.

[P1-B04-20] MEDIUM | File: N/A | Line: N/A
Description: No bitbucket-pipelines.yml or equivalent CI/CD configuration is present in the repository, meaning no automated build/test/deploy pipeline.
Fix: Create a CI/CD pipeline configuration with automated builds, tests, and security gates.

[P1-B05-1] CRITICAL | File: environment.uat.properties | Line: 15
Description: Production/UAT Cognito API credentials are hardcoded in properties files committed to the repository and not excluded by .gitignore.
Fix: Move credentials to a secrets manager. Add environment files to .gitignore and remove from git history.

[P1-B05-2] HIGH | File: pom.xml | Line: 76
Description: UAT database password hardcoded in pom.xml for the AWS RDS instance.
Fix: Remove credentials from pom.xml and use environment variables or a secrets manager.

[P1-B05-3] HIGH | File: pom.xml | Line: 29
Description: Database credentials hardcoded in pom.xml for local and dev profiles with plaintext passwords.
Fix: Remove credentials from pom.xml. Use environment variables or encrypted Maven settings.

[P1-B05-4] MEDIUM | File: environment.dev.properties | Line: 1
Description: AWS EC2 public DNS hostname and Azure hostname hardcoded in committed property files, exposing infrastructure topology.
Fix: Externalize infrastructure hostnames to configuration not tracked in version control.

[P1-B05-5] MEDIUM | File: environment.dev.properties | Line: 1
Description: Environment property files with credentials are tracked by git; only environment.local.properties is excluded by .gitignore.
Fix: Add all environment property files to .gitignore and inject configuration at deployment time.

[P1-B05-6] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 113
Description: OAuth2 client credentials are hardcoded in the Spring Security XML configuration committed to source control.
Fix: Externalize OAuth2 client secrets to environment variables or a secrets manager.

[P1-B05-7] MEDIUM | File: src/main/resources/fleetiq360ws.properties | Line: 10
Description: A hardcoded production URL for the accept driver feature is committed as a literal string.
Fix: Parameterize the URL by environment using property placeholders.

[P1-B05-8] LOW | File: pom.xml | Line: 87
Description: A third-party Maven repository is referenced over plain HTTP, vulnerable to MITM substitution.
Fix: Change the repository URL to use HTTPS.

[P1-B05-9] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java | Line: 38
Description: The APK update check endpoint is protected only by ROLE_CLIENT with non-expiring tokens and hardcoded client credentials, allowing anyone with the committed secrets to enumerate and download APK packages.
Fix: Implement per-device authentication for APK endpoints. Set token expiry for the ROLE_CLIENT OAuth2 client.

[P1-B05-10] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 148
Description: IDOR vulnerability where companyAccept unconditionally enables any permission record by ID with no ownership check.
Fix: Add ownership verification ensuring the permission belongs to the authenticated user's company.

[P1-B05-11] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 163
Description: IDOR vulnerability where companyDelete unconditionally deletes any permission record by ID with no ownership verification.
Fix: Add ownership verification before deletion.

[P1-B05-12] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 37
Description: IDOR vulnerability where getCompany returns company data for any driver ID without verifying the caller's identity.
Fix: Verify the authenticated principal matches or has authority over the requested uid.

[P1-B05-13] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 44
Description: IDOR vulnerability where getCompanyDrivers returns all drivers for any company owner without verifying caller identity.
Fix: Verify the authenticated user is the company owner.

[P1-B05-14] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 52
Description: searchCompany returns cross-tenant company data without organisation scoping for any authenticated user.
Fix: Add tenant filtering to ensure users only see companies in their organisation.

[P1-B05-15] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 74
Description: MD5 is used as the password hashing algorithm, which is broken, unsalted, and trivially reversible.
Fix: Replace MD5 with bcrypt or Argon2 password hashing.

[P1-B05-16] INFO | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 12
Description: Two OAuth2 endpoints are declared with security="none" with a comment acknowledging they are for testing.
Fix: Remove or secure these endpoints in the production configuration.

[P1-B05-17] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java | Line: 56
Description: Path traversal vulnerability where pkgname and version from HTTP request are used directly in Paths.resolve() without sanitization or path containment check.
Fix: Normalize the resolved path and verify it starts with the packageDir base directory. Validate pkgname and version against an allowlist pattern.

[P1-B05-18] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java | Line: 38
Description: No input validation on pkgname or version parameters in either APK endpoint.
Fix: Add @Pattern and @Size constraints to pkgname and version parameters.

[P1-B05-19] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 62
Description: The addCompany endpoint accepts @RequestBody with no @Valid annotation, and the Permissions model has no constraint annotations.
Fix: Add @Valid to the parameter and constraint annotations to the Permissions model.

[P1-B05-20] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 52
Description: The searchCompany endpoint has no length limit on the keyword, enabling DoS via expensive ilike pattern matching.
Fix: Add @Size constraint to limit keyword length.

[P1-B05-21] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 97
Description: Driver name and email are concatenated into an email message body without sanitization, potentially enabling social engineering.
Fix: Sanitize user-supplied name values before including them in email messages.

[P1-B05-22] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 28
Description: CSRF protection is not explicitly configured for state-changing endpoints.
Fix: Explicitly document and configure CSRF posture for the API.

[P1-B05-23] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: N/A
Description: No security response headers (X-Frame-Options, X-Content-Type-Options, HSTS) are configured anywhere in the application.
Fix: Configure security response headers via Spring Security or a servlet filter.

[P1-B05-24] INFO | File: src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java | Line: N/A
Description: No @CrossOrigin annotations are present on either controller, which is acceptable (default same-origin policy applies).
Fix: No action required. Document CORS policy for future reference.

[P1-B05-25] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java | Line: 43
Description: Error handling in getAvailablePackage swallows exceptions silently and returns null with a TODO comment indicating unfinished error handling.
Fix: Implement proper error handling that returns an appropriate error response to the client.

[P1-B05-26] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java | Line: 62
Description: FileNotFoundException includes the full server-side filesystem path in its message, which may be exposed to the client.
Fix: Use a generic error message in the exception. Log the detailed path server-side only.

[P1-B05-27] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 183
Description: The mapCompany method maps the password column into the Company model, causing password hashes to be returned in API responses.
Fix: Remove password from the SELECT query or add @JsonIgnore to the password field in Company.java.

[P1-B05-28] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 103
Description: Driver PII (email address and full name) is logged at INFO level in production logs.
Fix: Remove PII from log statements or redact sensitive fields.

[P1-B05-29] CRITICAL | File: pom.xml | Line: 231
Description: Spring Security 3.1.1.RELEASE is end-of-life and contains multiple known critical CVEs.
Fix: Upgrade Spring Security to a currently supported version.

[P1-B05-30] CRITICAL | File: pom.xml | Line: 239
Description: Spring Security OAuth2 1.0.0.RELEASE is end-of-life with known vulnerabilities.
Fix: Migrate to Spring Authorization Server or upgrade to a supported version.

[P1-B05-31] HIGH | File: pom.xml | Line: 12
Description: Spring Framework 3.2.14.RELEASE is end-of-life with known CVEs.
Fix: Upgrade Spring Framework to a currently supported version.

[P1-B05-32] HIGH | File: pom.xml | Line: 15
Description: Jackson Databind 2.6.7 has multiple known critical CVEs related to unsafe deserialization.
Fix: Upgrade Jackson Databind to the latest 2.x release.

[P1-B05-33] HIGH | File: pom.xml | Line: 199
Description: commons-fileupload 1.3.1 is vulnerable to CVE-2016-3092 (DoS).
Fix: Upgrade commons-fileupload to version 1.5 or later.

[P1-B05-34] MEDIUM | File: pom.xml | Line: 168
Description: commons-io 1.3.2 is an ancient version from 2008.
Fix: Upgrade to commons-io 2.16 or later with the correct groupId/artifactId.

[P1-B05-35] MEDIUM | File: pom.xml | Line: 267
Description: aws-java-sdk 1.11.163 is a very old version from 2017 with AWS SDK v1 in maintenance mode.
Fix: Upgrade to AWS SDK v2 or the latest v1 release.

[P1-B05-36] LOW | File: pom.xml | Line: 11
Description: The project targets Java 1.8 which has reached end-of-life for free public updates.
Fix: Upgrade to a current Java LTS version (Java 17 or 21).

[P1-B05-37] HIGH | File: N/A | Line: N/A
Description: No CI/CD pipeline configuration file was found in the repository, with no automated build, test, or deployment pipeline.
Fix: Create a CI/CD pipeline with automated builds, tests, and security scanning.

[P1-B05-38] MEDIUM | File: pom.xml | Line: 343
Description: The tomcat7-maven-plugin deployment configuration uses a plain HTTP Tomcat manager URL for UAT deployment.
Fix: Change the Tomcat manager URL to use HTTPS. Store deployment credentials securely.

[P1-B06-1] CRITICAL | File: environment.dev.properties | Line: 15
Description: Cognito API credentials are hardcoded with the same trivial value in all three environment property files committed to git.
Fix: Move credentials to a secrets manager. Remove environment files from git and add to .gitignore.

[P1-B06-2] CRITICAL | File: pom.xml | Line: 29
Description: Database credentials are committed in plaintext inside Maven profile definitions for local, dev, and UAT environments.
Fix: Remove credentials from pom.xml. Use environment variables or a secrets manager.

[P1-B06-3] CRITICAL | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 113
Description: OAuth2 client secrets are hardcoded in plaintext in a configuration file committed to git.
Fix: Externalize client secrets to environment variables or a secrets manager.

[P1-B06-4] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 74
Description: The authentication provider uses MD5 as the password hashing algorithm, which is unsalted, fast, and trivially reversible.
Fix: Replace MD5 with bcrypt or Argon2 password hashing.

[P1-B06-5] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 113
Description: OAuth2 client 987654321 has access-token-validity="0" meaning tokens never expire, granting permanent access if compromised.
Fix: Set a reasonable token expiry and implement token revocation.

[P1-B06-6] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 13
Description: Two OAuth approval endpoints are configured with security="none" and labeled as testing endpoints in the production branch.
Fix: Remove or properly secure these endpoints.

[P1-B06-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DatabaseController.java | Line: 88
Description: The deleteCompanies method constructs SQL by string concatenation of a Long value, which is an unsafe pattern even though the value is currently database-sourced.
Fix: Use a parameterized SimpleJdbcCall or PreparedStatement instead of string concatenation.

[P1-B06-8] HIGH | File: pom.xml | Line: 99
Description: Jackson Databind 2.6.7 has multiple known critical CVEs for deserialization attacks that can result in remote code execution.
Fix: Upgrade Jackson Databind to the latest 2.x release.

[P1-B06-9] HIGH | File: pom.xml | Line: 229
Description: Spring Framework 3.2.14, Spring Security 3.1.1, and Spring Security OAuth2 1.0.0 are all end-of-life with unpatched vulnerabilities.
Fix: Upgrade all framework dependencies to currently supported versions.

[P1-B06-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DatabaseCleanupException.java | Line: 6
Description: DatabaseCleanupException annotated with @ResponseStatus without a reason attribute causes the exception message to be forwarded to the HTTP client.
Fix: Add a fixed reason attribute to @ResponseStatus, or implement a @ControllerAdvice that sanitizes exception messages.

[P1-B06-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DatabaseController.java | Line: 66
Description: The companies list is declared null and only assigned inside a try block; if the query fails, a NullPointerException will occur when passed to deleteCompanies.
Fix: Initialize the list as an empty list, or add a null check before calling deleteCompanies.

[P1-B06-12] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DatabaseController.java | Line: 18
Description: Real customer email addresses and device MAC addresses are hardcoded as plaintext literals in production source code, constituting PII in the codebase.
Fix: Move the whitelist to a database table or external configuration file. Remove PII from source code.

[P1-B06-13] MEDIUM | File: pom.xml | Line: 199
Description: commons-fileupload 1.3.1 is vulnerable to CVE-2016-3092 (DoS).
Fix: Upgrade commons-fileupload to version 1.5 or later.

[P1-B06-14] MEDIUM | File: pom.xml | Line: 86
Description: The Splunk JFrog repository URL uses plain HTTP, susceptible to MITM artifact substitution.
Fix: Change the repository URL to use HTTPS.

[P1-B06-15] MEDIUM | File: environment.prod.properties | Line: 1
Description: AWS EC2 instance hostname and AWS RDS endpoint are committed in plaintext to git, revealing cloud infrastructure topology.
Fix: Externalize infrastructure hostnames to environment-specific configuration not tracked in version control.

[P1-B06-16] MEDIUM | File: pom.xml | Line: 77
Description: The UAT Tomcat manager URL uses plain HTTP, exposing WAR deployments and credentials to network interception.
Fix: Change the Tomcat manager URL to use HTTPS.

[P1-B06-17] LOW | File: pom.xml | Line: 130
Description: logback-classic and logback-core 1.2.3 are vulnerable to CVE-2021-42550 (JNDI injection).
Fix: Upgrade logback to version 1.2.13 or later.

[P1-B06-18] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/DatabaseController.java | Line: 64
Description: The /rest/db/cleanup endpoint has no method-level @PreAuthorize annotation; role enforcement is solely through URL-pattern matching.
Fix: Add @PreAuthorize("hasRole('SYS_ADMIN')") to the cleanup() method for defence-in-depth.

[P1-B06-19] LOW | File: src/main/webapp/WEB-INF/web.xml | Line: N/A
Description: No HTTP security response headers are configured in any reviewed configuration file.
Fix: Configure security response headers via Spring Security or a servlet filter.

[P1-B06-20] INFO | File: N/A | Line: N/A
Description: No bitbucket-pipelines.yml is present; CI/CD pipeline configuration is absent from the repository.
Fix: Create a CI/CD pipeline with automated builds, tests, and security gates.

[P1-B07-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 14
Description: Multiple hardcoded credentials including a GCM server key, Clickatell SMS API password, and internal service coordinates are committed as public static fields.
Fix: Move all credentials to a secrets manager or environment variables. Rotate all compromised credentials.

[P1-B07-2] CRITICAL | File: environment.uat.properties | Line: 16
Description: Cognito API credentials committed in plaintext across all environment property files, with the same weak credential reused across environments.
Fix: Move credentials to a secrets manager. Add environment files to .gitignore.

[P1-B07-3] HIGH | File: pom.xml | Line: 29
Description: Database credentials committed in plaintext in Maven profile definitions for local and UAT environments.
Fix: Remove credentials from pom.xml. Use environment variables or encrypted Maven settings.

[P1-B07-4] HIGH | File: pom.xml | Line: 88
Description: A third-party Maven repository is configured using plain HTTP, susceptible to MITM supply chain attacks.
Fix: Change the repository URL to use HTTPS.

[P1-B07-5] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 228
Description: IDOR vulnerability where GET /rest/appuser/get/{uid} fetches a complete driver record including PII without verifying the authenticated principal matches uid.
Fix: Verify the authenticated user's identity matches or has authority over the requested uid.

[P1-B07-6] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 132
Description: IDOR vulnerability where uploadProfile and uploadProfileAPP accept file uploads to overwrite any driver's profile image by uid without ownership check.
Fix: Verify the authenticated user is the owner of uid before allowing the photo update.

[P1-B07-7] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 253
Description: IDOR vulnerability where updateDrivers uses driver.getId() from the request body (not the path variable) to update any driver's name and compliance date.
Fix: Extract the authenticated principal's ID and use it instead of the request body ID, or verify ownership.

[P1-B07-8] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 235
Description: IDOR vulnerability where saveLicence overwrites licence number, security number, and address for any driver using the attacker-controlled request body ID.
Fix: Verify the authenticated user's identity matches the target driver ID before allowing PII updates.

[P1-B07-9] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 187
Description: IDOR vulnerability where saveEmails allows any authenticated user to redirect impact notification emails for any driver by supplying an arbitrary driver_id.
Fix: Verify the authenticated user owns the specified driver_id.

[P1-B07-10] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 209
Description: IDOR vulnerability where getEmails returns notification email addresses for any driver by uid without ownership check.
Fix: Verify the authenticated user's identity matches uid.

[P1-B07-11] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 108
Description: IDOR vulnerability where acceptDrivers and declineDriver operate on permission records by caller-supplied IDs with no company ownership verification.
Fix: Verify the authenticated user has administrative authority over the company associated with each permission record.

[P1-B07-12] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 34
Description: IDOR vulnerability where getEquipmentByUser returns all equipment for any driver by uid without verifying the requesting user is that driver or in the same organisation.
Fix: Verify the authenticated principal matches or has authority over uid.

[P1-B07-13] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 122
Description: IDOR vulnerability where getService retrieves service schedules for equipment at all companies linked to any driver uid without verifying identity.
Fix: Verify the authenticated user's identity matches uid.

[P1-B07-14] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 142
Description: IDOR vulnerability where SaveService updates service records for any unit_id and attributes service actions to any driver_id from the request body.
Fix: Verify the authenticated user has authority over the specified unit and driver records.

[P1-B07-15] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 42
Description: IDOR vulnerability where addEquipment modifies any unit's MAC address by ID or registers equipment under any company ID from the request body.
Fix: Verify the authenticated user has authority over the target equipment or company.

[P1-B07-16] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 57
Description: The deprecated getLoginAuth endpoint is still mapped and reachable, using MD5 authentication and returning the full Driver object including password hash.
Fix: Remove the deprecated endpoint entirely from the codebase.

[P1-B07-17] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 75
Description: registerDrivers has no input validation and returns the driver object (potentially including plaintext password) in error response bodies.
Fix: Add @Valid annotation, add model constraints, and use a response DTO that excludes sensitive fields.

[P1-B07-18] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: N/A
Description: No @Valid annotation is present on any @RequestBody parameter across DriverController and EquipmentController, with no constraint annotations on model classes.
Fix: Add @Valid to all @RequestBody parameters and constraint annotations to model fields.

[P1-B07-19] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 60
Description: getLoginAuth and registerDrivers log the full JSON-serialized Driver object at INFO level, including the plaintext password field.
Fix: Remove sensitive fields from log output or use a logging DTO that excludes passwords.

[P1-B07-20] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 154
Description: e.printStackTrace() is called in the uploadProfile exception handler, writing stack traces to System.err instead of the structured logger.
Fix: Replace e.printStackTrace() with logger.error("message", e).

[P1-B07-21] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 57
Description: The getLoginAuth response returns the full Driver object including the MD5 password hash with no @JsonIgnore suppression.
Fix: Add @JsonIgnore to the password field in Driver.java or use a response DTO.

[P1-B07-22] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: N/A
Description: No security response headers (X-Frame-Options, X-Content-Type-Options, Strict-Transport-Security) are configured.
Fix: Configure security response headers in Spring Security or via a servlet filter.

[P1-B07-23] HIGH | File: pom.xml | Line: 231
Description: Spring Framework 3.2.14, Spring Security 3.1.1, Spring Security OAuth 1.0.0, Jackson 2.6.7, and commons-fileupload 1.3.1 are all end-of-life with known CVEs.
Fix: Upgrade all dependencies to currently supported versions.

[P1-B07-24] LOW | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 13
Description: Two OAuth cache approval endpoints are explicitly marked security="none" and should not be present in production.
Fix: Remove or secure these endpoints.

[P1-B07-25] LOW | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 111
Description: OAuth2 client credentials are hardcoded in the Spring Security XML configuration tracked in git.
Fix: Externalize client secrets to environment variables or a secrets manager.

[P1-B07-26] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 30
Description: An internal AWS EC2 API URL is hardcoded in a static public field, disclosing infrastructure topology.
Fix: Externalize the URL to environment configuration.

[P1-B07-27] INFO | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 56
Description: The deprecated getLoginAuth endpoint is still active at runtime despite being annotated @Deprecated, using broken MD5 hashing.
Fix: Remove the endpoint from the codebase entirely.

[P1-B07-28] INFO | File: N/A | Line: N/A
Description: No bitbucket-pipelines.yml or CI/CD pipeline configuration is present in the repository.
Fix: Create a CI/CD pipeline with automated build, test, and security analysis steps.

[P1-B08-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 31
Description: Hardcoded AWS IAM access key ID and secret access key committed to source control, granting S3 bucket access to anyone with repository read access.
Fix: Remove hardcoded credentials. Use IAM roles, environment variables, or the AWS credentials provider chain.

[P1-B08-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 66
Description: Hardcoded AWS IAM credentials for SES SMTP committed to source control, allowing unauthorized email sending.
Fix: Remove hardcoded credentials. Use IAM roles or environment variables for SMTP authentication.

[P1-B08-3] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 14
Description: Multiple third-party API credentials (GCM server key, Clickatell SMS username/password/API ID) hardcoded as public static fields.
Fix: Move all credentials to a secrets manager or environment variables. Rotate compromised credentials.

[P1-B08-4] CRITICAL | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 113
Description: OAuth2 client credentials committed in plaintext with client 987654321 having non-expiring tokens.
Fix: Externalize secrets, set reasonable token expiry, and implement token revocation.

[P1-B08-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ImageController.java | Line: 30
Description: Path traversal vulnerability where the fileName path variable accepts any string including ".." sequences, with no verification that the resolved path stays within the image storage directory.
Fix: After resolving and normalizing the path, verify it starts with the base image storage directory. Reject requests with ".." or absolute paths.

[P1-B08-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 83
Description: IDOR vulnerability where saveImpactIMAGE and saveImpactIMAGEAPP update any incident's image or signature evidence by impid without ownership check.
Fix: Verify the incident belongs to the authenticated user's organisation before allowing updates.

[P1-B08-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 59
Description: IDOR vulnerability where saveIncident accepts driver_id and unit_id in the request body without validating they belong to the caller's organisation.
Fix: Verify driver_id and unit_id belong to the authenticated user's organisation.

[P1-B08-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java | Line: 53
Description: IDOR vulnerability where saveGPSLocation and saveGPSLocations accept unit_id from the request body and write GPS coordinates without ownership check.
Fix: Verify the unit belongs to the authenticated user's company before allowing GPS data writes.

[P1-B08-9] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java | Line: 35
Description: IDOR vulnerability where getGPSLocation uses the caller-supplied uid path variable without verifying the authenticated principal matches uid.
Fix: Verify the authenticated user's identity matches uid.

[P1-B08-10] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 83
Description: Unrestricted file upload where both impact image endpoints accept MultipartFile uploads with no MIME type or extension validation.
Fix: Implement a strict allowlist of permitted MIME types and file extensions. Validate file content matches the declared type.

[P1-B08-11] HIGH | File: pom.xml | Line: 76
Description: Database credentials for the UAT RDS PostgreSQL instance committed in plaintext in pom.xml.
Fix: Remove credentials from pom.xml. Use environment variables or a secrets manager.

[P1-B08-12] HIGH | File: pom.xml | Line: 231
Description: Spring Security 3.1.1, Spring Security OAuth2 1.0.0, and Spring Framework 3.2.14 are all critically out of date with numerous known CVEs.
Fix: Upgrade all framework dependencies to currently supported versions.

[P1-B08-13] HIGH | File: pom.xml | Line: 99
Description: jackson-databind 2.6.7 is affected by numerous critical deserialization CVEs that can lead to remote code execution.
Fix: Upgrade Jackson Databind to the latest 2.x release.

[P1-B08-14] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 74
Description: The legacy authentication manager uses MD5 as the password hashing algorithm, which is broken and trivially reversible.
Fix: Replace MD5 with bcrypt or Argon2 password hashing.

[P1-B08-15] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 60
Description: The full incident request body is serialized to JSON and logged at INFO level, including sensitive fields like driver ID, injury description, and witness names.
Fix: Remove sensitive fields from log output or use structured logging with PII redaction.

[P1-B08-16] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java | Line: 73
Description: Full GPS payload including unit IDs, latitude, and longitude is logged at INFO level on every batch GPS update.
Fix: Remove GPS telemetry data from INFO-level log statements.

[P1-B08-17] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 189
Description: The IllegalArgumentException message including internal MAC address values is returned verbatim in the HTTP response body.
Fix: Return a generic error message to the client. Log detailed error information server-side only.

[P1-B08-18] MEDIUM | File: environment.dev.properties | Line: 15
Description: Cognito API credentials committed to the repository for all environments with production EC2 hostname exposed.
Fix: Move credentials to a secrets manager. Remove environment files from git.

[P1-B08-19] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: N/A
Description: No HTTP security response headers configured; the image endpoint serves files without X-Content-Type-Options: nosniff.
Fix: Configure security response headers including X-Content-Type-Options: nosniff.

[P1-B08-20] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 13
Description: Two OAuth endpoints are granted security="none" with a comment "Just for testing" and are unauthenticated in production.
Fix: Remove or secure these endpoints.

[P1-B08-21] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 59
Description: No @Valid annotation on any @RequestBody parameter in ImpactController or LocationController, with no constraint annotations on model classes.
Fix: Add @Valid to all @RequestBody parameters and constraint annotations to model fields.

[P1-B08-22] MEDIUM | File: pom.xml | Line: 200
Description: commons-fileupload 1.3.1 is affected by CVE-2016-3092 (DoS) and CVE-2014-0050, directly used by multipart upload endpoints.
Fix: Upgrade commons-fileupload to version 1.5 or later.

[P1-B08-23] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 108
Description: e.printStackTrace() is called in catch blocks instead of using the structured logger, bypassing Splunk log aggregation.
Fix: Replace e.printStackTrace() with logger.error("message", e).

[P1-B08-24] LOW | File: pom.xml | Line: 87
Description: A third-party Maven repository is declared using plain HTTP, vulnerable to MITM artifact substitution.
Fix: Change the repository URL to use HTTPS.

[P1-B08-25] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java | Line: 26
Description: The LocationController class javadoc states "Not in Use" but all three endpoints are live and accessible, creating a misleading comment.
Fix: Remove the misleading comment. If the controller is truly unused, remove it entirely.

[P1-B08-26] INFO | File: pom.xml | Line: 209
Description: Apache Tika version 1.18 (2018) is used for MIME type detection and has known CVEs related to XML/ZIP processing.
Fix: Upgrade Apache Tika to the latest 2.x version.

[P1-B09-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 13
Description: GCM server API key, Clickatell SMS API credentials, and phone number are hardcoded as public static fields in source code.
Fix: Move all credentials to a secrets manager. Rotate compromised credentials.

[P1-B09-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 109
Description: A hardcoded bearer token is committed to source and used to authenticate every call to the internal PDF export API.
Fix: Externalize the token to a secrets manager or environment variable. Rotate the compromised token.

[P1-B09-3] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 322
Description: Hardcoded admin username and password for the backend PDF report API are embedded in source code and logged at INFO level.
Fix: Externalize the credentials to a secrets manager. Remove from log output.

[P1-B09-4] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 410
Description: Same hardcoded admin credentials as B09-3 also appear in the sendReportList method.
Fix: Externalize the credentials to a secrets manager.

[P1-B09-5] HIGH | File: environment.dev.properties | Line: 15
Description: Environment property files containing Cognito API credentials are committed to the repository for all non-local environments.
Fix: Move credentials to a secrets manager. Add environment files to .gitignore.

[P1-B09-6] HIGH | File: pom.xml | Line: 29
Description: Flyway database credentials for local, dev, and UAT environments are hardcoded in pom.xml and committed to source control.
Fix: Remove credentials from pom.xml. Use environment variables or encrypted Maven settings.

[P1-B09-7] MEDIUM | File: pom.xml | Line: 87
Description: A Maven dependency repository is configured using plain HTTP, susceptible to MITM artifact substitution.
Fix: Change the repository URL to use HTTPS.

[P1-B09-8] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 13
Description: Two URL patterns are configured with security="none" as a testing artefact, making them fully unauthenticated in production.
Fix: Remove or secure these endpoints.

[P1-B09-9] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 367
Description: The sendReportList endpoint is reachable by any authenticated role and triggers bulk report dispatch across the entire customer base with no admin check or rate limiting.
Fix: Restrict the endpoint to ROLE_SYS_ADMIN using @PreAuthorize. Add rate limiting and idempotency controls.

[P1-B09-10] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 35
Description: IDOR vulnerability across four endpoints where the uid path variable is accepted without verifying it matches the authenticated caller's identity.
Fix: Verify the authenticated principal's identity matches the requested uid for all four affected endpoints.

[P1-B09-11] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 74
Description: The authentication provider uses MD5 password hashing, which has no work factor, is GPU-acceleratable, and has existing rainbow tables.
Fix: Replace MD5 with bcrypt or Argon2 password hashing.

[P1-B09-12] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 113
Description: OAuth2 client secrets are hardcoded in a committed XML configuration file.
Fix: Externalize client secrets to environment variables or a secrets manager.

[P1-B09-13] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 113
Description: OAuth2 client 987654321 is configured with access-token-validity="0", meaning tokens never expire.
Fix: Set a reasonable token expiry and implement token revocation.

[P1-B09-14] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 314
Description: JSON for the PDF export API is built by string concatenation rather than a JSON serialization library, with unescaped string fields.
Fix: Use a JSON serialization library (Jackson/Gson) to construct the JSON payload.

[P1-B09-15] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: N/A
Description: No HTTP security headers are configured; Spring Security 3.1.1 does not add them by default.
Fix: Configure security response headers via Spring Security or a servlet filter.

[P1-B09-16] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 323
Description: The full JSON payload sent to the PDF export API, including plaintext admin credentials, is written to INFO-level logs forwarded to Splunk.
Fix: Remove credentials from log output. Log only non-sensitive metadata.

[P1-B09-17] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 353
Description: Exceptions are handled exclusively via e.printStackTrace(), bypassing the structured SLF4J logging framework.
Fix: Replace e.printStackTrace() with logger.error("message", e).

[P1-B09-18] CRITICAL | File: pom.xml | Line: 13
Description: Spring Framework 3.2.14.RELEASE is end-of-life since December 2016 with numerous unpatched CVEs.
Fix: Upgrade Spring Framework to a currently supported version.

[P1-B09-19] CRITICAL | File: pom.xml | Line: 231
Description: Spring Security 3.1.1.RELEASE is critically out of date and end-of-life, lacking security patches since approximately 2013.
Fix: Upgrade Spring Security to a currently supported version.

[P1-B09-20] CRITICAL | File: pom.xml | Line: 238
Description: Spring Security OAuth2 1.0.0.RELEASE is vulnerable to CVE-2016-4977 (SpEL injection allowing unauthenticated RCE).
Fix: Migrate to Spring Authorization Server or upgrade to a patched version.

[P1-B09-21] HIGH | File: pom.xml | Line: 99
Description: jackson-databind 2.6.7 is vulnerable to multiple critical deserialization gadget chain CVEs enabling remote code execution.
Fix: Upgrade Jackson Databind to the latest 2.x release.

[P1-B09-22] HIGH | File: pom.xml | Line: 199
Description: commons-fileupload 1.3.1 is vulnerable to CVE-2016-1000031 (RCE via DiskFileItem deserialization).
Fix: Upgrade commons-fileupload to version 1.5 or later.

[P1-B09-23] LOW | File: pom.xml | Line: 168
Description: The dependency org.apache.commons:commons-io:1.3.2 uses a groupId/artifactId combination that does not exist in Maven Central, creating a build reproducibility risk.
Fix: Change the dependency coordinates to the standard commons-io:commons-io artifact.

[P1-B09-24] MEDIUM | File: pom.xml | Line: 68
Description: The UAT Maven profile is configured as activeByDefault=true, meaning default Maven commands connect Flyway to the live UAT/production RDS instance.
Fix: Remove activeByDefault from the UAT profile. Require explicit profile selection.

[P1-B09-25] INFO | File: src/main/java/com/journaldev/spring/jdbc/controller/RestURIConstants.java | Line: 5
Description: Two URI constants for bulk permission operations are marked "unused" in comments but may still be mapped by controllers.
Fix: Verify whether any controller maps to these paths. If truly unused, remove the constants.

[P1-B09-26] INFO | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 30
Description: The internal PDF export API URL uses plain HTTP, meaning all traffic including admin credentials travels unencrypted.
Fix: Change the URL to use HTTPS. Verify the PDF export service supports TLS.

[P1-B10-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 13
Description: A GCM server API key, Clickatell SMS API username and password, and API ID are hardcoded as public static fields committed to the repository.
Fix: Move all credentials to a secrets manager or environment variables. Rotate compromised credentials.

[P1-B10-2] HIGH | File: pom.xml | Line: 28
Description: Database credentials for local and UAT environments are hardcoded in pom.xml with the UAT RDS endpoint also exposed.
Fix: Remove credentials from pom.xml. Use environment variables or a secrets manager.

[P1-B10-3] HIGH | File: environment.dev.properties | Line: 15
Description: All three environment properties files contain hardcoded Cognito API credentials committed to the repository.
Fix: Move credentials to a secrets manager. Add environment files to .gitignore.

[P1-B10-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 30
Description: A plain HTTP URL referencing an AWS EC2 instance is hardcoded, exposing infrastructure topology and using unencrypted transport.
Fix: Change to HTTPS. Externalize the URL to environment configuration.

[P1-B10-5] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 111
Description: OAuth2 client secrets are hardcoded in the Spring Security XML configuration committed to the repository.
Fix: Externalize client secrets to environment variables or a secrets manager.

[P1-B10-6] INFO | File: pom.xml | Line: 84
Description: The Splunk dependency is fetched from a third-party JFrog Artifactory repository over plain HTTP.
Fix: Change the repository URL to use HTTPS.

[P1-B10-7] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/UserController.java | Line: 22
Description: The /rest/admin/user endpoint is accessible to any authenticated user including ROLE_DRIVER because no specific intercept rule exists for /rest/admin/**.
Fix: Add an intercept-url rule for /rest/admin/** restricted to ROLE_SYS_ADMIN.

[P1-B10-8] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 353
Description: IDOR vulnerability where abortSessions deletes any session by ID with no verification of ownership.
Fix: Verify the session belongs to the authenticated user or their company before deletion.

[P1-B10-9] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 229
Description: IDOR vulnerability where startSessions accepts driver_id and unit_id from the request body without verifying they belong to the authenticated user.
Fix: Verify the authenticated user's identity matches driver_id and unit_id belongs to their company.

[P1-B10-10] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 299
Description: IDOR vulnerability where endSessions closes any session by ID from the request body without ownership verification.
Fix: Verify the session belongs to the authenticated user before allowing closure.

[P1-B10-11] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 62
Description: IDOR vulnerability where driverAccess uploads images to any session ID without verifying the caller owns the session.
Fix: Verify the session belongs to the authenticated user before allowing image uploads.

[P1-B10-12] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 113
Description: OAuth2 client 987654321 has access-token-validity="0" meaning tokens never expire.
Fix: Set a reasonable token expiry and implement token revocation.

[P1-B10-13] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 116
Description: The fleetiq360 client has refresh-token-validity equal to access-token-validity (both 300s), making refresh tokens ineffective, and the password grant type is enabled.
Fix: Set a longer refresh token validity or consider migrating away from the password grant type.

[P1-B10-14] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 97
Description: getQuestion returns checklist questions for any equipment ID without validating it against the caller's company.
Fix: Verify the equipment belongs to the authenticated user's company.

[P1-B10-15] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 12
Description: Two OAuth endpoints are marked security="none" with a testing comment, completely unauthenticated in production.
Fix: Remove or secure these endpoints.

[P1-B10-16] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 74
Description: Passwords are hashed using MD5, which is broken, unsalted, and trivially reversible.
Fix: Replace MD5 with bcrypt or Argon2 password hashing.

[P1-B10-17] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 172
Description: saveResults accepts @RequestBody with no @Valid annotation, allowing unvalidated date strings and unbounded comment fields to reach the database.
Fix: Add @Valid to the parameter and constraint annotations to the Result model.

[P1-B10-18] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 229
Description: startSessions accepts @RequestBody with no @Valid annotation, allowing unvalidated fields to reach SQL queries.
Fix: Add @Valid to the parameter and constraint annotations to the Sessions model.

[P1-B10-19] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/UserController.java | Line: 23
Description: The email request parameter is not validated for format or length before being passed to the DAO.
Fix: Add @Pattern and @Size constraints to the email parameter.

[P1-B10-20] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 154
Description: The searchForm method contains broken SQL syntax, indicating a dead code path that has never been tested.
Fix: Fix or remove the broken query. Add integration tests for all SQL queries.

[P1-B10-21] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 28
Description: No CSRF protection configuration is present in the Spring Security filter chain.
Fix: Explicitly configure CSRF posture. Document the stateless API exemption.

[P1-B10-22] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: N/A
Description: No security response headers configured anywhere in the application.
Fix: Configure security response headers via Spring Security or a servlet filter.

[P1-B10-23] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/UserController.java | Line: 23
Description: getUserByEmail returns the full User object including the password hash in the HTTP response body to any authenticated caller.
Fix: Add @JsonIgnore to the password field in User.java, or use a response DTO excluding the password.

[P1-B10-24] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 172
Description: saveResults logs the full Result request body as JSON at INFO level, including operator safety inspection responses and comments.
Fix: Remove sensitive fields from log output or redact before logging.

[P1-B10-25] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 229
Description: startSessions, endSessions, and saveOffline all log full request bodies at INFO level, including driver IDs and unit IDs.
Fix: Remove or redact sensitive fields from log statements.

[P1-B10-26] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 88
Description: e.printStackTrace() is called in the driverAccess exception handler, writing stack traces to System.err.
Fix: Replace e.printStackTrace() with logger.error("message", e).

[P1-B10-27] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 342
Description: endSessions logs the full serialized Sessions object at ERROR level when an EmptyResultDataAccessException occurs.
Fix: Log only non-sensitive metadata (e.g., session ID) at error level.

[P1-B10-28] CRITICAL | File: pom.xml | Line: 230
Description: Spring Security 3.1.1.RELEASE is over 10 years old with numerous known CVEs and no security patches available.
Fix: Upgrade Spring Security to a currently supported version.

[P1-B10-29] CRITICAL | File: pom.xml | Line: 238
Description: Spring Security OAuth2 1.0.0.RELEASE is the initial release, extremely old with known vulnerabilities and deprecated.
Fix: Migrate to Spring Authorization Server or upgrade to a supported version.

[P1-B10-30] HIGH | File: pom.xml | Line: 10
Description: Spring Framework 3.2.14.RELEASE is end-of-life since December 2016 with numerous known CVEs.
Fix: Upgrade Spring Framework to a currently supported version.

[P1-B10-31] HIGH | File: pom.xml | Line: 98
Description: Jackson Databind 2.6.7 has numerous known deserialization CVEs enabling arbitrary code execution.
Fix: Upgrade Jackson Databind to the latest 2.x release.

[P1-B10-32] HIGH | File: pom.xml | Line: 198
Description: commons-fileupload 1.3.1 is vulnerable to CVE-2016-1000031 (arbitrary file write via DiskFileItem deserialization).
Fix: Upgrade commons-fileupload to version 1.5 or later.

[P1-B10-33] MEDIUM | File: pom.xml | Line: 336
Description: The Flyway plugin uses the PostgreSQL JDBC driver at version 9.1-901.jdbc3, an extremely old version from circa 2011.
Fix: Upgrade the PostgreSQL JDBC driver to a current version (e.g., 42.7+).

[P1-B10-34] MEDIUM | File: N/A | Line: N/A
Description: No bitbucket-pipelines.yml is present; there is no automated CI/CD pipeline for builds, tests, or security gates.
Fix: Create a CI/CD pipeline with automated builds, tests, and security scanning.

[P1-B10-35] INFO | File: pom.xml | Line: 44
Description: The dev profile specifies a Tomcat Manager URL over plain HTTP for WAR deployment.
Fix: Change the Tomcat manager URL to use HTTPS.

[P1-B11-1] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/APIConnections.java | Line: 16
Description: No Bean Validation constraints on APIConnectionKey, accepting null and unbounded-length strings when used as @RequestBody.
Fix: Add @NotNull and @Size constraints to the APIConnectionKey field.

[P1-B11-2] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Answers.java | Line: 13
Description: No Bean Validation constraints on the answer or question_id fields, allowing null, empty, or out-of-range values.
Fix: Add @NotNull, @Size, and @Min constraints to the fields.

[P1-B11-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationRequest.java | Line: 17
Description: No Bean Validation constraints on any field of the authentication DTO, meaning empty or null credentials can reach downstream service code.
Fix: Add @NotNull and @Size constraints to username, password, newPassword, and accessToken fields.

[P1-B11-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/APIConnections.java | Line: 24
Description: APIConnectionKey is a credential field with a public getter and no @JsonIgnore, causing raw key values to appear in JSON responses.
Fix: Add @JsonIgnore to the APIConnectionKey field or its getter.

[P1-B11-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationRequest.java | Line: 9
Description: Lombok @Data generates a toString() method that includes password, newPassword, and accessToken in plaintext, which will leak credentials in any log or debug output.
Fix: Add @ToString.Exclude to the password, newPassword, and accessToken fields, or provide a custom toString() override.

[P1-B11-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationRequest.java | Line: 17
Description: The password, newPassword, and accessToken fields have no @JsonIgnore annotation, meaning they would be included if the object is serialized into a response.
Fix: Add @JsonIgnore to password, newPassword, and accessToken fields to prevent serialization in responses.
[P1-B12-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Company.java | Line: 23
Description: The Company model contains a password field with no @JsonIgnore annotation. Lombok @Data generates a public getPassword() method, causing the password value to be included in every JSON API response that serialises a Company object.
Fix: Add @JsonIgnore to the password field in Company.java, or use @JsonProperty(access = JsonProperty.Access.WRITE_ONLY) to prevent serialisation while still allowing deserialisation.

[P1-B12-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Company.java | Line: 33
Description: The @Builder constructor copies Driver.password into Company.password, propagating a credential from the Driver object into the Company object where it is then exposed via the Lombok-generated getter in API responses.
Fix: Remove the password copy from the builder constructor (line 48). Company should never hold a password sourced from Driver.

[P1-B12-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationResponse.java | Line: 19
Description: AuthenticationResponse exposes a sessionToken field with no @JsonIgnore. Returning a session token alongside an access token in the login response doubles the credential surface exposed to the client.
Fix: Add @JsonIgnore to the sessionToken field, or remove it from the response model. If a session token is needed for MFA challenge flows, return it only in that specific context via a separate DTO.

[P1-B12-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Company.java | Line: 20
Description: The Company model exposes an internal database primary key (id, type Long) directly in API responses with no obfuscation. Combined with the unprotected searchCompany endpoint, this enables harvesting of internal IDs for use in IDOR attacks.
Fix: Suppress the internal id field from API responses using @JsonIgnore and expose a non-sequential external identifier instead. Apply tenant-scoping to the searchCompany query.

[P1-B12-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationResponse.java | Line: 13
Description: AuthenticationResponse extends ResponseWrapper which declares Object-typed data and metadata fields. These raw Object fields can hold arbitrary objects whose sensitive fields will be fully serialised to the client with no type-level guard.
Fix: Replace the Object type for data and metadata in ResponseWrapper with concrete, well-defined DTOs that explicitly control which fields are serialised.

[P1-B12-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 25
Description: Driver.password has no @JsonIgnore and is serialised in getCompanyDrivers API responses. Additionally, Driver.securityno (line 29) and Driver.licno (line 27) are both serialised without restriction, representing significant PII exposure.
Fix: Add @JsonIgnore to password, securityno, and licno fields in Driver.java. Alternatively, create a response DTO that excludes these fields.

[P1-B12-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Charts.java | Line: 16
Description: Charts exposes unit_id (the internal database primary key for equipment) in API responses. The snake_case name matches the DB column, confirming it is a raw DB identifier that enables enumeration of equipment across tenants.
Fix: Add @JsonIgnore to the unit_id field, or replace it with a non-sequential external identifier in the response.

[P1-B12-8] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationResponse.java | Line: 21
Description: AuthenticationResponse returns both actualDate and expirationDate as plain strings alongside expiresIn, which is redundant and leaks server-side time information. Clients should use the expiry embedded in the JWT itself.
Fix: Remove actualDate and expirationDate fields from AuthenticationResponse, or document their intended use and ensure they do not diverge from the JWT-embedded expiry.

[P1-B13-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 25
Description: The password field has no @JsonIgnore annotation and no write-only configuration. Lombok @Data generates a public getPassword() getter, causing Jackson to include the password in every JSON API response that serialises a Driver object, leaking credentials to any authenticated caller.
Fix: Add @JsonIgnore to the password field, or apply @JsonProperty(access = JsonProperty.Access.WRITE_ONLY) to allow inbound deserialisation while preventing outbound serialisation.

[P1-B13-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 30
Description: The securityno field (a government-issued identifier such as SIN/SSN) has no @JsonIgnore and is serialised in all API responses containing a Driver. Government-issued security numbers are the highest-sensitivity PII category.
Fix: Add @JsonIgnore to the securityno field. Only expose this field via a separate, access-controlled endpoint with explicit role-based authorisation.

[P1-B13-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 27
Description: The licno field stores the driver's licence number, a regulated PII identifier. No @JsonIgnore is present, so the licence number is serialised into every API response returning a Driver.
Fix: Add @JsonIgnore to the licno field. If needed for specific use cases, expose it through a dedicated endpoint with role-based access control.

[P1-B13-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 1
Description: The Driver model declares no Bean Validation constraints on any field. Fields like password, email, phone, licno, securityno, gps_frequency, and max_session_length have no @NotNull, @Size, @Pattern, @Email, @Min, or @Max annotations.
Fix: Add JSR-303 Bean Validation annotations to all fields. Add @Email to email, @Size and @Pattern to licno and securityno, @Min/@Max to gps_frequency and max_session_length. Ensure @Valid is used at the controller layer.

[P1-B13-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/DriverEmails.java | Line: 1
Description: The DriverEmails model declares four email address fields (email_addr1 through email_addr4) with no @Email, @Size, or @Pattern constraints. Malformed or excessively long values will pass through to the database layer without validation.
Fix: Add @Email and @Size constraints to each email address field. Ensure @Valid is used at the controller layer when this model is bound from request input.

[P1-B13-6] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 1
Description: The Driver model is used as both a request deserialisation target and a response serialisation source with no separation between write-only and read-only fields. All PII fields are returned indiscriminately in all response contexts.
Fix: Implement a request/response DTO separation pattern, or use @JsonProperty(access = ...) annotations to control field directionality.

[P1-B13-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Equipment.java | Line: 14
Description: The mac_address field of Equipment is inherited by DriverEquipment and serialised into all API responses with no @JsonIgnore. A hardware MAC address discloses equipment network topology to API consumers.
Fix: Add @JsonIgnore to the mac_address field in Equipment.java. If MAC address display is needed, expose it only through a dedicated admin endpoint.

[P1-B13-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Equipment.java | Line: 15
Description: The url field of Equipment is inherited by DriverEquipment and serialised into all API responses with no @JsonIgnore. If this contains an internal device endpoint or MQTT broker address, it reveals internal infrastructure topology.
Fix: Add @JsonIgnore to the url field in Equipment.java. Internal device endpoints should not be exposed to client-facing API responses.

[P1-B13-9] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 34
Description: The comp_id (company/organisation identifier) is returned in all Driver API responses, informing callers of their exact comp_id value and creating a precondition for IDOR attacks if controller-level scoping is not enforced.
Fix: Verify that all controller endpoints enforce tenant-scoping based on the authenticated user's comp_id. Consider suppressing comp_id from Driver responses if not needed by clients.

[P1-B13-10] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 1
Description: Lombok @Data generates a toString() method that includes every field including password, securityno, licno, email, phone, and addr. If a Driver object is logged, all PII and credentials will be written to application logs in plain text.
Fix: Add @ToString.Exclude to the password, securityno, licno, email, phone, and addr fields in Driver.java.

[P1-B14-1] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java | Line: 23
Description: The training_date and expiration_date fields are plain String with no Bean Validation constraint. No @Pattern annotation enforces a valid date format, so malformed values will not be rejected at the model layer.
Fix: Add @Pattern annotations with an ISO 8601 date regex to both training_date and expiration_date fields, or change the field types to java.time.LocalDate with appropriate format annotations.

[P1-B14-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/EmailLayout.java | Line: 13
Description: The subject and message fields are unbounded String fields with no @Size constraint. An attacker can supply arbitrarily large strings, creating a potential denial-of-service vector via oversized payloads.
Fix: Add @Size(max = ...) annotations to subject and message fields with appropriate maximum lengths.

[P1-B14-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Equipment.java | Line: 27
Description: The url field is a plain String with no @Pattern or URL validation constraint. If this value is used to make outbound HTTP requests, it is an SSRF surface allowing attacker-controlled URLs such as internal network addresses.
Fix: Add a @Pattern annotation restricting the url field to a whitelist of allowed URL schemes and hosts, or validate the URL at the service layer before making any outbound requests.

[P1-B14-4] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java | Line: 14
Description: All three model classes (DriverTraining, EmailLayout, Equipment) implement java.io.Serializable with no readObject() override. If these objects are ever deserialized from untrusted input, they become part of the deserialization gadget attack surface.
Fix: Remove Serializable from classes that do not require Java serialization. If Serializable is required, add a readObject() method with validation logic.

[P1-B14-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java | Line: 12
Description: DriverTraining exposes all fields including internal database foreign-key IDs (manufacture_id, type_id, fuel_type_id) in API responses via Lombok @Data-generated getters with no @JsonIgnore annotation.
Fix: Add @JsonIgnore to internal FK fields (manufacture_id, type_id, fuel_type_id) or create a response DTO that excludes them.

[P1-B14-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Equipment.java | Line: 26
Description: The Equipment model exposes serial_no, mac_address, and url via Lombok-generated public getters with no @JsonIgnore. serial_no enables equipment enumeration, mac_address discloses hardware identifiers, and url discloses internal device/telemetry endpoint addresses.
Fix: Add @JsonIgnore to serial_no, mac_address, and url fields. If needed, expose them through dedicated admin endpoints with appropriate role-based access control.

[P1-B14-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Equipment.java | Line: 9
Description: Lombok @Data generates a toString() method that includes all fields of Equipment, including serial_no, mac_address, and url. If any Equipment instance is logged, hardware identifiers and internal endpoint URLs will appear in plaintext in logs.
Fix: Add @ToString.Exclude to the serial_no, mac_address, and url fields in Equipment.java.

[P1-B14-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/EmailLayout.java | Line: 14
Description: The message field holds the body of system email templates. If email templates contain operator names or safety alert content, returning EmailLayout objects in API responses without filtering exposes this content to any authenticated caller.
Fix: Add @JsonIgnore to the message field if it should not be returned in API responses, or implement role-based access control on the endpoint returning EmailLayout objects.

[P1-B14-9] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java | Line: 6
Description: Two unused imports are present (Roles.RolesBuilder and java.util.Date), indicating the class may have been assembled via copy-paste without thorough review.
Fix: Remove the unused imports to improve code clarity and maintainability.

[P1-B15-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java | Line: 17
Description: The expected_answer field in FormDtl is included in the SQL SELECT in getForm() and serialised to the HTTP response. Returning the expected/correct answer to the client undermines the integrity of operator pre-use safety inspections, allowing callers to submit correct answers without actually performing physical checks.
Fix: Add @JsonIgnore to the expected_answer field in FormDtl.java. Perform expected-answer validation server-side only and never return it in client responses.

[P1-B15-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/ErrorMessage.java | Line: 18
Description: ErrorMessage has a detail field that is fully serialised to clients with no @JsonIgnore. The field is generic and caller-determined. If any call site assigns exception messages, SQL error text, or stack traces to detail, that information will be returned verbatim to the client.
Fix: Add @JsonIgnore to the detail field, or ensure that all call sites sanitise the content before assigning it. Implement a global @ControllerAdvice exception handler to standardise error responses.

[P1-B15-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java | Line: N/A
Description: FormDtl has no JSR-303 validation constraints on any field. While currently populated from database results rather than direct user input, the absence of constraints means it could be used unsafely as a @RequestBody in future endpoints.
Fix: Add appropriate @NotNull, @Size, and @Pattern constraints to fields, especially input_type, input_label, and input_value.

[P1-B15-4] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/EquipmentType.java | Line: N/A
Description: EquipmentType has no JSR-303 validation constraints on any field. As a reference data model, the risk is low but the absence of constraints is a hygiene concern.
Fix: Add @NotNull and @Size constraints to the name and icon fields.

[P1-B16-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 14
Description: GCM server API key is hardcoded as a public static string literal in source code. Anyone with read access to the repository can use this key to send push notifications to any registered device in the application.
Fix: Remove the hardcoded key from source code. Store it in an environment variable or a secrets manager and inject it via application properties or Spring configuration.

[P1-B16-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 18
Description: Clickatell SMS gateway credentials (username, plaintext password, and API ID) are hardcoded as public static string literals. These credentials authorise SMS sending on behalf of the application's account and are exposed in any repository clone or build artifact.
Fix: Remove all hardcoded credentials from source code. Store them in environment variables or a secrets manager and inject them via application properties or Spring configuration. Rotate the compromised credentials immediately.

[P1-B16-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/GCMDataPermission.java | Line: 12
Description: The GCM push notification payload embeds a complete Permissions object including internal database IDs (id, driver_id, comp_id), driver name, enabled state, and the device's own gsm_token. GCM payloads should carry only the minimum data necessary for the notification.
Fix: Create a minimal notification DTO containing only the fields needed to render the notification. Remove internal IDs and the gsm_token from the push notification payload.

[P1-B16-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GCMData.java | Line: 5
Description: The to field (GCM device registration token) is protected with no @JsonIgnore. If GCMData instances are returned in API responses or logged, the device token is exposed, enabling targeted push notification delivery to that device.
Fix: Add @JsonIgnore to the to field to prevent it from being serialised in any API response. Restrict access modifier to private.

[P1-B16-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Permissions.java | Line: N/A
Description: The Permissions class is used directly as a @RequestBody in CompanyController.addCompany() with no Bean Validation constraints on any field and no @Valid annotation on the controller method. Null or malformed values will reach the database layer.
Fix: Add @NotNull and @Size constraints to Permissions fields. Add @Valid to the @RequestBody parameter in CompanyController.addCompany().

[P1-B17-1] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GCMResponse.java | Line: 6
Description: GCMResponse implements java.io.Serializable without documented justification. This expands the gadget surface for Java deserialization attacks if deserialization of this type from untrusted input occurs anywhere in the application.
Fix: Remove Serializable unless there is a confirmed need for Java object serialization. If required, add a readObject() method with validation.

[P1-B17-2] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GPS.java | Line: 5
Description: GPS implements java.io.Serializable without documented justification. GPS objects carry precise location data; if a deserialization endpoint accepts GPS objects from untrusted sources, an attacker could inject arbitrary coordinate or timestamp data.
Fix: Remove Serializable unless there is a confirmed need. If required, add a readObject() method with validation logic.

[P1-B17-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GPS.java | Line: 12
Description: The GPS model exposes all location fields (latitude, longitude, timestamp, unit ID, unit name) via public getters with no @JsonView or @JsonIgnore annotations. The full location profile of a forklift is returned to any authenticated caller, including the internal database record ID.
Fix: Add @JsonIgnore to the id field. Consider implementing @JsonView to scope which fields are returned based on the caller's role. Create a response DTO that excludes internal identifiers.

[P1-B17-4] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GCMResponse.java | Line: 11
Description: GCMResponse mirrors the raw GCM server response and includes multicast_id, canonical_ids, and a results list. If returned directly to API clients, it leaks GCM infrastructure identifiers and potentially device token rotation data.
Fix: Confirm GCMResponse is used only internally and never serialised into REST responses. If it is returned to clients, create a filtered DTO that omits GCM infrastructure details.

[P1-B17-5] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/GCMEntity.java | Line: 8
Description: The msg_type field is declared protected rather than private, widening its accessibility to subclasses and same-package classes without requiring getter/setter use, contrary to standard encapsulation practice.
Fix: Change the access modifier of msg_type from protected to private.

[P1-B18-1] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Impact.java | Line: 16
Description: The Impact model carries no JSR-303 validation constraints on any field. When deserialized from @RequestBody ImpactList, no bean validation is triggered. mac_address can be null or arbitrarily long, impact_time can be malformed, and impact_value has no declared bounds. This allows malformed safety-critical event payloads to be accepted.
Fix: Add @NotBlank and @Size to mac_address, @NotBlank and @Pattern (ISO 8601) to impact_time, and @Min/@Max to impact_value. Add @Valid to the @RequestBody parameter in ImpactController.saveImpactData().

[P1-B18-2] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/Impact.java | Line: 16
Description: The Impact model (safety-critical event model) contains no fields for operator identity, forklift serial number, site ID, or severity classification. Clients must re-implement threshold logic independently, creating a risk of inconsistent safety classification.
Fix: Add a severity classification field to the Impact model populated server-side during event processing. Consider adding operator and unit reference fields for complete audit trails.

[P1-B18-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Impact.java | Line: 18
Description: The mac_address field in Impact has no @JsonIgnore annotation. Lombok @Data generates a public getter, so the MAC address will be serialised into any JSON response that uses Impact as a response body, facilitating device fingerprinting.
Fix: Add @JsonIgnore to the mac_address field, or use @JsonProperty(access = WRITE_ONLY) so it is accepted on input but never echoed in responses.

[P1-B18-4] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java | Line: 16
Description: The backing list fields in both ImpactList and GPSList are package-private (no access modifier) instead of private. Any class within the same package can read or replace the list directly, bypassing the public setter and any future validation logic.
Fix: Change the access modifier of impactList in ImpactList.java and gpsList in GPSList.java from package-private to private.

[P1-B18-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Impact.java | Line: 10
Description: Lombok @Data on Impact generates a toString() that includes all fields including mac_address. ImpactController logs the full incoming ImpactList at INFO level via Gson, causing every inbound impact event's MAC address and timestamp to appear in production logs.
Fix: Add @ToString.Exclude to the mac_address field. Remove or redact the full-payload Gson logging in ImpactController, or reduce it to DEBUG level with MAC address masking.

[P1-B18-6] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/GPSList.java | Line: 12
Description: GPSList wraps GPS objects that carry longitude, latitude, gps_time, current_location, unit_id (internal DB primary key), and unit_name. No field carries @JsonIgnore. The internal unit_id is exposed in GPS API responses, enabling enumeration attacks.
Fix: Add @JsonIgnore to the id and unit_id fields in GPS.java, or create a response DTO that excludes internal identifiers.

[P1-B19-1] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactNotification.java | Line: 17
Description: The email and mobile fields on ImpactNotification carry no Bean Validation constraints. If this model is bound from a request body, malformed email addresses or phone numbers including excessively long strings will pass through to the notification dispatch layer.
Fix: Add @Email and @Size constraints to the email field, and @Pattern and @Size constraints to the mobile field.

[P1-B19-2] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Incidents.java | Line: 5
Description: Incidents implements java.io.Serializable with no custom readObject() guard. The class contains byte[] fields (signature, image) that could carry arbitrarily large payloads if deserialized from an untrusted source.
Fix: Remove Serializable if not required. If required, add a readObject() method with size validation for the byte[] fields.

[P1-B19-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactNotification.java | Line: 17
Description: ImpactNotification includes operator PII fields email and mobile directly in the notification model. If this model is serialised to a REST response or logged, operator contact details are exposed. Notification routing fields should be separated from content data.
Fix: Separate routing fields (email, mobile) into a distinct internal DTO that is never serialised to API responses. Add @JsonIgnore to email and mobile if separation is not immediately feasible.

[P1-B19-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Incidents.java | Line: 13
Description: The signature and image fields are byte[] with public getters and no @JsonIgnore. Jackson will serialize both as Base64 strings in any JSON response. Signature data is biometric-adjacent PII and should not be included in list/summary responses.
Fix: Add @JsonIgnore to both signature and image fields. Expose them only through a dedicated endpoint that returns a single incident's binary data on explicit request.

[P1-B19-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Incidents.java | Line: 21
Description: Raw internal database foreign-key identifiers driver_id and unit_id are exposed via public getters with no masking. These sequential integer IDs enable enumeration of drivers and forklift units across the system.
Fix: Add @JsonIgnore to driver_id and unit_id, or replace them with non-sequential external identifiers in API responses.

[P1-B19-6] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Incidents.java | Line: 16
Description: The witness field is an unbounded free-text String that likely contains third-party PII (witness names, contact details). It is exposed via a public getter with no length constraint or @JsonIgnore.
Fix: Add @Size(max = ...) to constrain the witness field length. Consider whether the witness field should be excluded from list endpoint responses via @JsonIgnore.

[P1-B19-7] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactNotification.java | Line: 11
Description: driver_name (operator PII) is included in ImpactNotification alongside company_name, unit_name, and impact_time. If this object is logged via Lombok @Data toString() during notification dispatch, operator identity linked to a safety event will appear in production logs.
Fix: Add @ToString.Exclude to driver_name, email, and mobile fields in ImpactNotification.java.

[P1-B20-1] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Permissions.java | Line: 27
Description: The enabled field, which controls whether a driver-company permission link is active, is typed as String rather than Boolean. Unexpected values (e.g. "t", "1", null, empty string) may cause downstream authorisation checks to behave incorrectly.
Fix: Change the enabled field type from String to Boolean. Update the DAO mapping and SQL queries to use proper boolean types.

[P1-B20-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Permissions.java | Line: 29
Description: The gsm_token field in Permissions is accepted as caller-supplied input in the addCompany request body and written to the database without validation. An attacker can register an arbitrary device token as another driver's gsm_token to receive their push notifications.
Fix: Validate that the gsm_token belongs to the authenticated user's device. Do not accept gsm_token from the addCompany request body; instead, use a separate authenticated endpoint for device token registration.

[P1-B20-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 148
Description: The companyAccept endpoint (PUT /rest/company/accept/{pid}) sets enabled=true for any permission row by caller-supplied pid with no ownership check. Any authenticated user can enable any permission record, granting themselves or others access to any company.
Fix: Add an ownership check to verify the authenticated user is the company owner or intended recipient of the permission before enabling it.

[P1-B20-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 162
Description: The companyDelete endpoint (PUT /rest/company/delete/{pid}) deletes any permission row by caller-supplied pid with no ownership check. Any authenticated user can revoke any driver's access across the entire platform.
Fix: Add an ownership check to verify the authenticated user owns the company associated with the permission before allowing deletion.

[P1-B20-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Permissions.java | Line: N/A
Description: Neither Permissions nor PackageEntry carries any JSR-303/Bean Validation constraints. All fields are unconstrained and controllers using these models as @RequestBody do not use @Valid. Any values including nulls, overlong strings, or unexpected characters are accepted.
Fix: Add @NotNull, @Size, and @Pattern constraints to all fields on both models. Add @Valid to all controller method parameters that bind these models.

[P1-B20-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java | Line: 56
Description: The APK download endpoint constructs a filesystem path using caller-supplied pkgname and version via Path.resolve(). If pkgname or version contains ../ sequences, the resolved path escapes packageDir and can serve arbitrary files from the server filesystem (path traversal).
Fix: Canonicalise the resolved path and verify it starts with the packageDir prefix before serving the file. Alternatively, validate pkgname and version against a strict whitelist pattern (alphanumeric, dots, hyphens only).

[P1-B20-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java | Line: 33
Description: The PackageEntry.url field is constructed using a baseUrl derived from the incoming HTTP request's Host header. An attacker who sends a crafted Host header can inject an arbitrary base URL into the response, directing mobile clients to download APK updates from a malicious server.
Fix: Derive the base URL from a server-side configuration property rather than the request's Host header. Alternatively, validate the Host header against an allowlist of known hostnames.

[P1-B20-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Permissions.java | Line: 29
Description: The gsm_token field (FCM/GCM push notification device registration token) has no @JsonIgnore and is serialised into every JSON response that includes a Permissions object. Any authenticated user retrieving company data can harvest push tokens for all drivers, enabling arbitrary push notification delivery.
Fix: Add @JsonIgnore to the gsm_token field in Permissions.java. The token should never be exposed in API responses.

[P1-B20-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java | Line: 23
Description: The env field of PackageEntry exposes the deployment environment label (e.g. prod, staging, dev) in API responses. Combined with fileName, this reveals internal APK versioning and naming conventions.
Fix: Add @JsonIgnore to the env field, or filter it from the response if the deployment environment is not needed by clients.

[P1-B20-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java | Line: 62
Description: When a requested package file is not found, the exception message includes the full server-side filesystem path. If this exception propagates to the HTTP response, it discloses the packageDir value and the absolute filesystem path to the caller.
Fix: Replace the detailed filesystem path in the exception message with a generic user-facing error. Log the full path server-side at ERROR level but return only a sanitised message to the client.

[P1-B21-1] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Questions.java | Line: 5
Description: All three model classes (Questions, ReportLists, Reports) implement java.io.Serializable with explicitly declared serialVersionUID values. No JSR-303 field-level validation constraints are present on any field. This creates a latent deserialization gadget-chain attack surface.
Fix: Remove Serializable from classes that do not require Java object serialization. If required, add a readObject() method with validation.

[P1-B21-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Questions.java | Line: 12
Description: No JSR-303/380 validation annotations are present on any field in Questions, ReportLists, or Reports. If used as @RequestBody targets, oversized strings, null values, or malformed inputs will pass through to the persistence layer unchecked.
Fix: Add @NotNull and @Size constraints to string fields. Add @Min/@Max to integer fields. Ensure @Valid is applied at the controller layer.

[P1-B21-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java | Line: 17
Description: ReportLists exposes comp_id (the tenant/company discriminator) via a public getter with no @JsonIgnore. If a controller returns ReportLists collections without filtering by the authenticated user's comp_id, all tenant report subscriptions will be disclosed. Additionally, file_name may reveal multi-tenant storage layout conventions.
Fix: Add @JsonIgnore to comp_id and file_name. Ensure all queries returning ReportLists are scoped to the authenticated user's comp_id.

[P1-B21-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Reports.java | Line: 12
Description: Reports uses a generic key/value/object triple (field, object, value) as its data model. This makes it structurally impossible to apply field-level access control or data classification at the model layer, as any data including operator PII can appear in the value field at runtime.
Fix: Replace the generic Reports model with purpose-specific DTOs that enforce data classification. At minimum, ensure all queries populating Reports enforce tenant isolation.

[P1-B21-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Questions.java | Line: 14
Description: Questions contains an expectedanswer field with a fully public getter and no @JsonIgnore. Pre-op safety checklist expected answers are transmitted in API responses to operator-facing clients, allowing operators to read and submit correct answers without genuine knowledge, defeating the safety check.
Fix: Add @JsonIgnore to the expectedanswer field. Validate expected answers exclusively server-side and never return them in client-facing responses.

[P1-B22-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 13
Description: RuntimeConfig contains multiple hardcoded production credentials: a GCM server API key, a Clickatell SMS gateway username and plaintext password, and an SMS API ID. These are committed to the repository and exposed to anyone with read access.
Fix: Remove all hardcoded credentials from source code immediately. Store them in environment variables or a secrets manager. Rotate all compromised credentials (GCM key, Clickatell username/password/API ID).

[P1-B22-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/ResponseWrapper.java | Line: 18
Description: ResponseWrapper.data and ResponseWrapper.metadata are both declared as raw java.lang.Object. If Jackson's global default typing is enabled, these fields become polymorphic deserialization sinks that could allow gadget-chain attacks. Even without default typing, Object fields represent a latent deserialization risk.
Fix: Replace Object with concrete, well-defined DTO types for data and metadata fields. If generic typing is required, use bounded wildcards or a sealed type hierarchy.

[P1-B22-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Results.java | Line: 14
Description: The Results.error field carries raw Exception.getMessage() content directly to API responses. In ImpactController, IllegalArgumentException messages contain internal data including MAC addresses and timestamps. This leaks internal data model details and hardware identifiers in error responses.
Fix: Sanitise all error messages before assigning them to Results.error. Return generic, user-facing error messages and log detailed exceptions server-side only. Implement a global @ControllerAdvice exception handler.

[P1-B22-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Results.java | Line: 14
Description: Results exposes a String error field with no length constraint or sanitisation. ErrorMessage exposes a String detail field. Neither class uses @JsonInclude(NON_NULL), so populated fields are serialised verbatim. There is no global @ControllerAdvice exception handler to intercept unhandled exceptions.
Fix: Add @JsonInclude(NON_NULL) to both Results and ErrorMessage. Implement a global @ControllerAdvice exception handler that standardises error responses and prevents internal details from reaching clients.

[P1-B22-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/ResponseWrapper.java | Line: 18
Description: Because ResponseWrapper.data and ResponseWrapper.metadata are java.lang.Object, any object placed into these fields will be serialised in full by Jackson, including fields not excluded with @JsonIgnore. If a DAO entity with sensitive fields is passed directly to data, those fields will appear in the API response.
Fix: Never pass raw DAO entities to ResponseWrapper.data or metadata. Always use a DTO projection that includes only the fields intended for client consumption.
[P1-B23-1] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Sessions.java | Line: N/A
Description: No Bean Validation constraints (@NotNull, @Size, @Min, @Max, @Pattern) on any field of Sessions or Services model classes, allowing arbitrary values including negative IDs, blank timestamps, or overlong strings to reach the data access layer.
Fix: Add JSR-303 Bean Validation annotations to all fields on Sessions and Services, and enforce @Valid on controller @RequestBody parameters.

[P1-B23-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Sessions.java | Line: 12
Description: Sessions exposes four photo URL fields and driver_id with no @JsonIgnore annotations; Services also exposes driver_id without suppression. All fields are serialized in every JSON response containing these objects.
Fix: Add @JsonIgnore or @JsonView annotations to restrict sensitive fields from being serialized in API responses where they are not needed.

[P1-B23-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Roles.java | Line: 9
Description: Lombok @Data generates a toString() that includes all fields including the authority string. If a Roles object is passed to a logger, the authority value is emitted in log output.
Fix: Add @ToString.Exclude to the authority field, or override toString() to omit sensitive fields.

[P1-B23-4] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Roles.java | Line: 20
Description: The authority field on Roles has no @JsonIgnore annotation. If Roles objects are returned in API responses, the raw Spring Security authority string is exposed to clients.
Fix: Add @JsonIgnore or @JsonProperty(access = WRITE_ONLY) to the authority field.

[P1-B23-5] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/Roles.java | Line: 31
Description: The Roles.RoleId enum defines only one role (ROLE_COMPANY_GROUP), meaning all authenticated users share the same authority with no finer-grained role hierarchy.
Fix: Confirm this flat role model is intentional and verify that endpoints requiring elevated privileges enforce additional access controls beyond ROLE_COMPANY_GROUP membership.

[P1-B23-6] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/Sessions.java | Line: 1
Description: No @JsonTypeInfo annotation on Sessions, Services, or Roles. Global Jackson default typing cannot be assessed from model files alone.
Fix: Verify that global ObjectMapper configuration does not enable default typing (enableDefaultTyping or activateDefaultTyping).

[P1-B24-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/User.java | Line: 25
Description: The password field on the User domain model has no @JsonIgnore or @JsonProperty(access = WRITE_ONLY) protection. Lombok @Data generates a public getPassword() getter, so if any controller returns a User object directly, the password is serialized into the JSON response.
Fix: Add @JsonIgnore or @JsonProperty(access = JsonProperty.Access.WRITE_ONLY) to the password field immediately.

[P1-B24-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/User.java | Line: 17
Description: The internal database primary key id (Long) is exposed via Lombok-generated getter with no @JsonIgnore. If User is serialized to a response, the raw numeric database ID enables sequential enumeration attacks.
Fix: Add @JsonIgnore to the id field or use an opaque external identifier in API responses.

[P1-B24-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/User.java | Line: 30
Description: The roles field (Set<Roles>) is exposed via Lombok-generated getter with no @JsonIgnore. If User is serialized, the complete internal role structure including authority strings is returned to the client.
Fix: Add @JsonIgnore to the roles field to prevent role structure leakage in API responses.

[P1-B24-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/UserResponse.java | Line: 23
Description: UserResponse includes userStatus which carries raw Cognito account lifecycle state strings (e.g., FORCE_CHANGE_PASSWORD, UNCONFIRMED) useful for targeting accounts in a weakened state.
Fix: Map Cognito userStatus to a sanitized application-level status value before including it in API responses, or omit the field.

[P1-B24-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/UserResponse.java | Line: 27
Description: UserResponse exposes phoneNumber (PII) with no access control at the model layer, which may violate data minimization requirements under GDPR and PIPEDA.
Fix: Add @JsonIgnore to phoneNumber or implement controller-layer checks to ensure it is only returned when the caller has a legitimate need.

[P1-B24-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/User.java | Line: 13
Description: User implements Serializable with no readObject() override performing field validation. All fields including password, roles, and id are accepted unconditionally during Java object deserialization.
Fix: Add a readObject() method with field validation, or add JSR-303 constraints to fields and enforce them during deserialization.

[P1-B24-7] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/User.java | Line: 13
Description: User does not implement UserDetails or any Spring Security interface, yet carries password and roles fields, creating ambiguity about whether a local authentication path exists alongside Cognito JWT auth.
Fix: Clarify whether User is used in any local authentication path. If not, remove the password field. If so, audit that path separately.

[P1-B24-8] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/UserResponse.java | Line: 13
Description: UserResponse is correctly designed as a safe external DTO omitting password, id, and roles. The risk is that if any code path returns User instead of UserResponse, all protections are bypassed.
Fix: Perform a code-wide search for controllers returning User directly to ensure UserResponse is always used for API responses.

[P1-B25-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 31
Description: AWS IAM Access Key ID and Secret Access Key are hardcoded as static field initializers in source code and permanently recorded in git history, granting access to the forkliftiq360 S3 bucket.
Fix: Immediately revoke and rotate these credentials in AWS IAM. Replace with IAM instance roles, environment variables, or AWS Secrets Manager.

[P1-B25-2] HIGH | File: environment.dev.properties | Line: 15
Description: Environment property files containing Cognito API credentials (cognitoAPIUsername/cognitoAPIPassword) and infrastructure identifiers are tracked in git across all three environments (dev, prod, uat).
Fix: Add environment.dev.properties, environment.prod.properties, and environment.uat.properties to .gitignore. Rotate credentials and inject them via environment variables or a secrets manager.

[P1-B25-3] HIGH | File: pom.xml | Line: 29
Description: Plaintext database credentials are committed in pom.xml Maven build profiles, including UAT RDS PostgreSQL password for dev_admin and local profile passwords.
Fix: Remove credentials from pom.xml. Use environment variables or Maven settings.xml with encrypted passwords for Flyway configuration.

[P1-B25-4] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 113
Description: OAuth2 client secrets for clients 987654321 and fleetiq360 are hardcoded in plaintext in the Spring Security XML configuration tracked in git.
Fix: Move OAuth2 client secrets to environment variables or a secrets manager. Rotate both client secrets.

[P1-B25-5] MEDIUM | File: pom.xml | Line: 88
Description: The Splunk Maven repository is configured with a plain HTTP URL, exposing the build to man-in-the-middle artifact substitution attacks.
Fix: Change the repository URL to use HTTPS (https://splunk.jfrog.io/splunk/ext-releases-local).

[P1-B25-6] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 113
Description: OAuth2 client 987654321 has access-token-validity="0", meaning tokens issued to this client never expire, creating a permanent authentication foothold if compromised.
Fix: Set a reasonable access-token-validity (e.g., 300 seconds) and configure refresh tokens for this client.

[P1-B25-7] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 74
Description: User passwords are hashed with MD5, a cryptographically broken hash function with no salt, making stored passwords trivially recoverable via rainbow tables or GPU brute force.
Fix: Replace MD5 with bcrypt, scrypt, or Argon2. Migrate existing password hashes by re-hashing on next successful login.

[P1-B25-8] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 13
Description: Two OAuth approval-management endpoints are configured with security="none" with a comment "Just for testing", exposing unauthenticated manipulation of OAuth approval state.
Fix: Remove or protect these endpoints. If not needed in production, delete the configuration entries entirely.

[P1-B25-9] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java | Line: 55
Description: Path traversal vulnerability in loadPackageAsResource where unsanitized pkgname and version parameters from HTTP path/query variables are used to construct a filesystem path with no normalize() or boundary check.
Fix: Validate pkgname and version against a strict allowlist regex, call normalize(), and verify the resolved path starts with packageDir before serving the resource.

[P1-B25-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 40
Description: The S3 key file extension is derived from MIME type detection on the raw bytes of the uploaded stream, allowing an attacker to influence the extension by crafting file content.
Fix: Validate that the detected MIME type is in an allowlist of expected image types before using the extension.

[P1-B25-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java | Line: 28
Description: The baseUrl passed to getAvailablePackage is constructed from request.getRequestURL() which reflects the HTTP Host header, enabling a crafted Host header to redirect Android devices to download APK updates from an attacker-controlled server.
Fix: Validate the Host header against a whitelist of allowed hostnames, or use a server-side configured base URL instead of deriving it from the request.

[P1-B25-12] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java | Line: 62
Description: When a requested APK file is not found, the exception message includes the full absolute filesystem path of the expected file location, leaking the server's directory structure to API clients.
Fix: Return a generic error message without internal path details. Log the full path server-side only.

[P1-B25-13] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 63
Description: The S3 bucket name and full local filesystem path of every uploaded file are written to the log at INFO level, exposing infrastructure identifiers in log aggregation systems.
Fix: Reduce the log level to DEBUG or remove infrastructure details from the log message.

[P1-B25-14] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 72
Description: Every object uploaded to S3 is set to CannedAccessControlList.PublicRead, making all uploaded images world-readable without authentication.
Fix: Remove the PublicRead ACL. Serve images through the application with proper authentication, or use S3 pre-signed URLs with expiration.

[P1-B25-15] HIGH | File: pom.xml | Line: 13
Description: Multiple severely outdated dependencies with known CVEs: Spring 3.2.14 (EOL 2016), Spring Security 3.1.1, spring-security-oauth2 1.0.0, Jackson-databind 2.6.7, commons-fileupload 1.3.1, aws-java-sdk 1.11.163.
Fix: Upgrade all dependencies to current supported versions. Prioritize Spring Framework, Spring Security, Jackson-databind, and commons-fileupload due to known RCE CVEs.

[P1-B26-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 66
Description: AWS SES SMTP credentials (IAM access key ID AKIA**REDACTED** and secret key) are hardcoded in source code, granting anyone with repo access the ability to send arbitrary email as the application's identity.
Fix: Immediately rotate these credentials. Replace with environment variable injection or AWS Secrets Manager lookup.

[P1-B26-2] HIGH | File: environment.dev.properties | Line: 15
Description: Cognito API service account credentials (ciiadmin/ciiadmin) are hardcoded with identical values across all three environment property files tracked in git, representing a trivially guessable weak shared credential.
Fix: Rotate credentials per environment, inject at deploy time via secrets manager, and remove from source control.

[P1-B26-3] HIGH | File: pom.xml | Line: 76
Description: Production (UAT) database credentials for RDS PostgreSQL instance are hardcoded in pom.xml in the uat Maven build profile, which is also marked activeByDefault.
Fix: Remove credentials from pom.xml. Use environment variables or CI/CD pipeline variables for Flyway configuration.

[P1-B26-4] HIGH | File: pom.xml | Line: 29
Description: Local and dev database credentials are hardcoded in pom.xml build profiles committed in plain text.
Fix: Remove credentials from pom.xml. Use local Maven settings.xml or environment variables.

[P1-B26-5] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 113
Description: OAuth2 client secrets for two clients are hardcoded in spring-security.xml tracked in git. Client 987654321 also has non-expiring tokens (access-token-validity="0").
Fix: Move client secrets to externalized configuration. Rotate both secrets. Set a finite token validity.

[P1-B26-6] MEDIUM | File: .gitignore | Line: 6
Description: The .gitignore only excludes environment.local.properties while dev, uat, and prod environment files containing credentials are tracked by git.
Fix: Add environment.dev.properties, environment.uat.properties, and environment.prod.properties to .gitignore and remove them from tracking.

[P1-B26-7] MEDIUM | File: pom.xml | Line: 44
Description: The dev Azure database URL with full hostname (forklift360.canadaeast.cloudapp.azure.com) is hardcoded in pom.xml, revealing infrastructure topology.
Fix: Remove infrastructure hostnames from pom.xml. Use environment variables for database URLs.

[P1-B26-8] LOW | File: pom.xml | Line: 84
Description: The Splunk artifact repository is referenced over plain HTTP, making dependency fetches susceptible to man-in-the-middle substitution attacks.
Fix: Change the repository URL to use HTTPS.

[P1-B26-9] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: 30
Description: CognitoService performs no JWT validation whatsoever -- no signature verification, no issuer check, no audience check, no expiry check. On authentication failure, it silently returns an empty AuthenticationResponse.
Fix: Implement proper JWT validation with JWKS endpoint fetch, signature verification, issuer/audience claims checks, and expiry validation. Throw an authentication exception on failure rather than returning empty responses.

[P1-B26-10] CRITICAL | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 113
Description: OAuth2 client 987654321 has access-token-validity="0" meaning tokens never expire. Combined with the client secret being in source control, an attacker with the secret has permanent irrevocable access.
Fix: Set a finite access-token-validity and configure token refresh. Revoke any existing non-expiring tokens in the token store.

[P1-B26-11] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: 48
Description: The username parameter is appended directly into the internal HTTP URL via string concatenation with no URL encoding or sanitization, enabling HTTP request parameter injection.
Fix: URL-encode the username parameter before embedding it in the URL, or use a proper URI builder.

[P1-B26-12] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: 48
Description: All calls from CognitoService to the internal Cognito proxy use plain HTTP, transmitting credentials and access tokens in cleartext.
Fix: Change internal proxy calls to use HTTPS, even for localhost connections, or use a Unix domain socket.

[P1-B26-13] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 74
Description: The authenticationManager uses MD5 as the password hashing algorithm, which is cryptographically broken, unsalted, and trivially reversible.
Fix: Replace with bcrypt, scrypt, or Argon2. Migrate existing hashes via re-hashing on next successful login.

[P1-B26-14] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 13
Description: Two OAuth endpoints are explicitly unprotected with security="none" with a "Just for testing" comment, exposing unauthenticated manipulation of OAuth approval state.
Fix: Remove these entries from the production security configuration entirely.

[P1-B26-15] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 300
Description: The JdbcTokenStore persists tokens in the database with no visible cleanup or TTL enforcement, allowing non-expiring tokens to accumulate indefinitely.
Fix: Implement a scheduled token cleanup job. Ensure all clients have finite token validity.

[P1-B26-16] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java | Line: 55
Description: MIME type detection for uploaded files relies solely on URLConnection.guessContentTypeFromStream() with a silent fallback to .jpg, allowing polyglot file uploads with no content-type allowlist validation.
Fix: Add an allowlist of permitted MIME types (image/jpeg, image/png, etc.) and reject uploads that do not match.

[P1-B26-17] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java | Line: 65
Description: The file path constructed from imageStorageLocation.resolve(fileName) has no normalize() plus startsWith() boundary check, creating a low-probability path traversal risk via the extension.
Fix: Add a startsWith(imageStorageLocation) check after resolve and normalize to ensure the path stays within the intended directory.

[P1-B26-18] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java | Line: 72
Description: The FileStorageException thrown from saveImage() includes the server-generated fileName in the message, which may propagate to HTTP responses depending on exception handler configuration.
Fix: Use a generic error message in the exception. Log the specific filename server-side only.

[P1-B26-19] INFO | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 28
Description: The /rest/** security block uses create-session="never", which is appropriate for stateless REST APIs using OAuth2 bearer tokens. CSRF is not applicable.
Fix: No action required. This is a positive observation.

[P1-B26-20] INFO | File: src/main/webapp/WEB-INF/web.xml | Line: 38
Description: Transport security (CONFIDENTIAL) is enforced at the servlet container level, but there is no evidence of Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options, or Content-Security-Policy headers.
Fix: Add security response headers via a servlet filter or Spring Security configuration.

[P1-B26-21] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: 62
Description: CognitoService uses e.printStackTrace() in both catch blocks, writing to System.err rather than the logging framework, potentially exposing internal class names, hostnames, and request details in production logs.
Fix: Replace e.printStackTrace() with structured logging via the SLF4J logger at ERROR level.

[P1-B26-22] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/BootstrapService.java | Line: 55
Description: BootstrapService.FlywayBean.migrate() uses System.out.println() which bypasses log level configuration and log routing controls.
Fix: Replace System.out.println with the SLF4J logger.

[P1-B26-23] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 81
Description: The sendMail() method outputs SMTP exception details to System.out and silently swallows Transport.send() exceptions via e.printStackTrace() only, meaning mail delivery failures are not propagated to callers.
Fix: Replace System.out.println with structured logging. Propagate mail delivery exceptions to callers.

[P1-B26-24] CRITICAL | File: pom.xml | Line: 13
Description: Spring Framework 3.2.14.RELEASE (EOL December 2016) and Spring Security 3.1.1.RELEASE are severely end-of-life with numerous known CVEs including remote code execution vulnerabilities.
Fix: Upgrade to a currently supported Spring Framework and Spring Security version (Spring 6.x / Spring Security 6.x or at minimum 5.x).

[P1-B26-25] HIGH | File: pom.xml | Line: 99
Description: Jackson Databind 2.6.7 has multiple known critical deserialization CVEs (CVE-2017-7525, CVE-2019-14379, and others).
Fix: Upgrade Jackson Databind to the latest 2.17.x or newer release.

[P1-B26-26] HIGH | File: pom.xml | Line: 199
Description: commons-fileupload 1.3.1 is affected by CVE-2016-3092 (Denial of Service via malicious multipart requests).
Fix: Upgrade commons-fileupload to 1.5 or later.

[P1-B26-27] HIGH | File: pom.xml | Line: 168
Description: commons-io is declared as org.apache.commons:commons-io:1.3.2 which is not a valid Apache Commons IO artifact ID, potentially resolving to an incorrect or unmaintained artefact.
Fix: Change the Maven coordinate to commons-io:commons-io and upgrade to version 2.15.x or later.

[P1-B26-28] MEDIUM | File: pom.xml | Line: 246
Description: braintree-java 2.53.0 is a very old version of a payment gateway library (current is 3.x), and its presence in a forklift management system warrants scrutiny.
Fix: Confirm whether Braintree is actually required. If so, upgrade to the latest 3.x version.

[P1-B26-29] MEDIUM | File: pom.xml | Line: 334
Description: The PostgreSQL JDBC driver version 9.1-901.jdbc3 is EOL and likely mismatched with the production database version.
Fix: Upgrade to a current PostgreSQL JDBC driver version (42.x).

[P1-B26-30] INFO | File: pom.xml | Line: N/A
Description: No bitbucket-pipelines.yml was found in the repository, preventing verification of CI/CD pipeline security, test execution, or deployment controls.
Fix: Establish a CI/CD pipeline with automated testing, security scanning, and controlled deployment stages.

[P1-B26-31] LOW | File: pom.xml | Line: 68
Description: The uat Maven profile is configured with activeByDefault=true, meaning a developer running mvn without specifying a profile will use UAT credentials and potentially target the production database.
Fix: Remove activeByDefault from the uat profile. Require explicit profile selection for non-local environments.

[P1-B27-1] CRITICAL | File: pom.xml | Line: 29
Description: Hardcoded PostgreSQL database credentials (username postgres, password gmtp-postgres) in the local Maven profile committed to version control.
Fix: Remove credentials from pom.xml. Use Maven settings.xml or environment variables.

[P1-B27-2] CRITICAL | File: pom.xml | Line: 76
Description: Hardcoded UAT RDS credentials (dev_admin / C!1admin) for the production RDS instance committed to version control.
Fix: Remove from pom.xml immediately. Use CI/CD pipeline variables or a secrets manager.

[P1-B27-3] CRITICAL | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 113
Description: Two OAuth2 client secrets are hardcoded in Spring Security XML configuration committed to version control, allowing anyone with repo access to obtain bearer tokens.
Fix: Move secrets to externalized configuration and rotate both client secrets.

[P1-B27-4] CRITICAL | File: environment.dev.properties | Line: 15
Description: Cognito API credentials (ciiadmin/ciiadmin) are hardcoded and committed in all three environment property files with the same weak credential pair across dev, UAT, and prod.
Fix: Rotate credentials per environment. Inject at deploy time. Remove files from version control.

[P1-B27-5] HIGH | File: pom.xml | Line: 88
Description: The Splunk JFrog Artifactory repository is configured over plain HTTP, enabling man-in-the-middle artifact substitution during builds.
Fix: Change the URL to HTTPS.

[P1-B27-6] HIGH | File: environment.dev.properties | Line: 14
Description: Identical weak Cognito API credentials (ciiadmin/ciiadmin) are used across all environments with no environment separation, and prod property files are tracked in git.
Fix: Use unique, strong credentials per environment. Inject via environment variables or secrets manager at deploy time.

[P1-B27-7] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 66
Description: registerDriver() and resetPassword() perform no organisation-scoping -- the caller can register a driver under another organisation or reset any driver's password by supplying an arbitrary email address.
Fix: Extract the authenticated principal's organisation from the security context and verify it matches the target driver's organisation before processing.

[P1-B27-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 52
Description: The deprecated authenticate() method remains reachable via POST /rest/appuser/validate with no organisation-scoping, allowing any authenticated user to validate credentials for drivers in other organisations.
Fix: Remove or disable the deprecated endpoint. If retained, add organisation-scoping checks.

[P1-B27-9] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 99
Description: resetPassword() accepts any email address and immediately generates, stores, and emails a new password with no verification of caller identity or organisation membership -- any bearer token holder can reset any driver's password.
Fix: Verify the authenticated caller is authorized to reset the target driver's password (e.g., same organisation, admin role).

[P1-B27-10] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 113
Description: OAuth2 client 987654321 has access-token-validity="0" meaning tokens never expire, dramatically increasing the impact of any token compromise.
Fix: Set a finite access-token-validity and configure refresh tokens.

[P1-B27-11] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 66
Description: registerDriver() and resetPassword() perform no input validation on Driver object fields -- no @Valid annotations, no length checks, no pattern constraints on email, name, phone, or password.
Fix: Add JSR-303 validation annotations to the Driver model and enforce @Valid at the service or controller layer.

[P1-B27-12] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 55
Description: Passwords are stored using MD5 in SQL (md5(?)) and configured via password-encoder hash="md5" in Spring Security. MD5 is broken for password storage with no salt and no work factor.
Fix: Replace MD5 with bcrypt, scrypt, or Argon2. Migrate existing hashes on next successful login.

[P1-B27-13] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 69
Description: DriverAlreadyExistException message includes the driver's email address, enabling account enumeration if the exception message is serialized into an API response.
Fix: Use a generic error message that does not include the email address.

[P1-B27-14] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 59
Description: DriverServiceException from authenticate() includes the driver's email address in the message, constituting PII exposure if propagated to a client or logs.
Fix: Use a generic error message without PII.

[P1-B27-15] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 115
Description: DriverServiceException from resetPassword() includes the driver's email address in the message.
Fix: Use a generic error message without PII.

[P1-B27-16] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 110
Description: resetPassword() logs the email address using string concatenation at INFO level. The generated plaintext password is in an adjacent variable, and the fragile logging pattern risks accidental credential exposure.
Fix: Use parameterized SLF4J logging and ensure the plaintext password is never logged.

[P1-B27-17] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 60
Description: DriverController logs the full Driver object serialized as JSON via gson.toJson() at INFO level, including the plaintext password field, for multiple endpoints.
Fix: Exclude the password field from JSON serialization in log statements. Use a separate DTO or Gson exclusion strategy for logging.

[P1-B27-18] CRITICAL | File: pom.xml | Line: 12
Description: Spring Framework 3.2.14.RELEASE reached end-of-life December 2016 and is affected by numerous CVEs including CVE-2018-1270 (RCE) and CVE-2022-22965 (Spring4Shell).
Fix: Upgrade to a currently supported Spring Framework version.

[P1-B27-19] CRITICAL | File: pom.xml | Line: 230
Description: Spring Security 3.1.1.RELEASE is severely end-of-life with multiple CVEs including CVE-2018-1199 (authentication bypass) and CVE-2014-3625 (path traversal).
Fix: Upgrade to a currently supported Spring Security version.

[P1-B27-20] HIGH | File: pom.xml | Line: 238
Description: spring-security-oauth2 1.0.0.RELEASE is the initial release (circa 2012), end-of-life, and predates fixes for CVE-2019-3778 (open redirect).
Fix: Upgrade to a supported OAuth2 implementation (Spring Security OAuth2 Resource Server in Spring Security 6.x).

[P1-B27-21] HIGH | File: pom.xml | Line: 98
Description: jackson-databind 2.6.7 is affected by multiple high and critical CVEs including CVE-2017-7525, CVE-2018-5968, and CVE-2019-14379 enabling remote code execution.
Fix: Upgrade to the latest Jackson 2.17.x or newer.

[P1-B27-22] CRITICAL | File: pom.xml | Line: 199
Description: commons-fileupload 1.3.1 is affected by CVE-2016-1000031 (remote code execution via file upload), and this dependency is actively exercised by controller endpoints.
Fix: Upgrade to commons-fileupload 1.5 or later.

[P1-B27-23] MEDIUM | File: pom.xml | Line: 86
Description: The Splunk JFrog Artifactory repository is declared using a plain HTTP URL, enabling supply-chain attacks via artifact substitution.
Fix: Change the URL to HTTPS.

[P1-B28-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 31
Description: AWS IAM access key ID and secret access key are hardcoded as a static field initializer and committed to source control, granting anyone with repo access the ability to read, write, and delete S3 objects.
Fix: Immediately revoke and rotate. Replace with IAM instance roles or environment variable injection.

[P1-B28-2] HIGH | File: environment.dev.properties | Line: 15
Description: Cognito API credentials (ciiadmin/ciiadmin) are committed in plaintext across all three environment property files with the same credential shared across all environments.
Fix: Rotate credentials per environment. Remove files from version control and inject secrets at deploy time.

[P1-B28-3] MEDIUM | File: environment.prod.properties | Line: 1
Description: Production and UAT environment files contain specific AWS EC2 public DNS hostnames and IP addresses, disclosing production server topology and cloud provider region.
Fix: Remove infrastructure hostnames from committed files. Use environment variable injection for URLs.

[P1-B28-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/LocalFileStorageService.java | Line: 19
Description: Path traversal in loadImageAsResource where the fileName from a URL @PathVariable is resolved against imageStorageLocation with normalize() but no startsWith() boundary check, allowing directory escape.
Fix: Add a startsWith(imageStorageLocation) check after normalize(). Validate fileName against a strict character allowlist.

[P1-B28-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java | Line: 56
Description: Path traversal in loadPackageAsResource where both pkgname and version are user-supplied and interpolated into a filesystem path with no sanitization or boundary check.
Fix: Validate pkgname and version against strict allowlist regex. Add normalize() and startsWith(packageDir) boundary check.

[P1-B28-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/LocalFileStorageService.java | Line: 24
Description: FileNotFoundException message includes the full absolute server filesystem path, which is serialized into HTTP responses due to @ResponseStatus annotation and absence of a global exception handler.
Fix: Return a generic error message. Add a @ControllerAdvice exception handler that strips internal details.

[P1-B28-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ImageController.java | Line: 29
Description: The /image/{fileName} endpoint serves files from the server filesystem with no authentication or authorization check, and no Spring Security URL pattern covers this path.
Fix: Add authentication requirements for /image/** in spring-security.xml or add @PreAuthorize to the controller method.

[P1-B28-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/EntityNotFoundException.java | Line: 7
Description: EntityNotFoundException message includes internal database primary keys and driver email addresses, which leak to API clients via @ResponseStatus without a reason attribute.
Fix: Set a generic reason attribute on @ResponseStatus or add a @ControllerAdvice handler that strips internal details from error responses.

[P1-B29-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 66
Description: Hardcoded AWS SES SMTP access key ID (AKIA**REDACTED**) and secret key are committed to source. These are long-term IAM credentials that do not expire unless rotated.
Fix: Immediately rotate in AWS IAM. Replace with environment variables or AWS Secrets Manager.

[P1-B29-2] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 113
Description: OAuth2 client secrets for two clients are hardcoded in Spring Security XML committed to source control.
Fix: Move to externalized configuration. Rotate both client secrets.

[P1-B29-3] HIGH | File: environment.dev.properties | Line: 15
Description: Cognito API credentials (ciiadmin/ciiadmin) are committed to source in all three environment files, using identical weak credentials.
Fix: Rotate credentials per environment. Remove files from version control.

[P1-B29-4] HIGH | File: pom.xml | Line: 76
Description: UAT database credentials (dev_admin/C!1admin) and local credentials (fleetiq360/fleetiq360) are committed in pom.xml, with the UAT profile set as activeByDefault.
Fix: Remove credentials from pom.xml. Use environment variables or CI/CD pipeline variables.

[P1-B29-5] MEDIUM | File: pom.xml | Line: 88
Description: A third-party Maven repository is referenced using plain HTTP, enabling man-in-the-middle artifact substitution.
Fix: Change to HTTPS.

[P1-B29-6] CRITICAL | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 74
Description: MD5 is configured as the password hashing algorithm, which is entirely unsuitable for password storage -- no salting, trivially brute-forced, with widely available rainbow tables.
Fix: Replace with bcrypt, scrypt, or Argon2.

[P1-B29-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 31
Description: The user lookup SQL query allows authentication using either the plaintext username OR its MD5 hash, enabling an attacker who knows the MD5 of a username to authenticate as that user.
Fix: Remove the md5(u.name) = ? alternative from the SQL query. Accept only the plaintext username for lookup.

[P1-B29-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java | Line: 38
Description: The buildUserFromUserEntity() method hardcodes enabled, accountNonExpired, and credentialsNonExpired to true, preventing administrators from disabling accounts through these Spring Security flags.
Fix: Map these flags to corresponding database fields on the User entity to allow account disablement and credential expiry.

[P1-B29-9] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 113
Description: OAuth2 client 987654321 has access-token-validity="0" meaning tokens never expire, providing a permanent authentication foothold if compromised.
Fix: Set a reasonable finite access-token-validity and configure refresh tokens.

[P1-B29-10] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 13
Description: Two test OAuth2 endpoints are configured with security="none" with a "Just for testing" comment, left enabled in production configuration.
Fix: Remove these entries from production security configuration.

[P1-B29-11] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ImageController.java | Line: 29
Description: The /image/{fileName} endpoint is not covered by any security rule in spring-security.xml, allowing unauthenticated access to server-stored images including operator and forklift images.
Fix: Add /image/** to the Spring Security intercept-url patterns with appropriate role requirements.

[P1-B29-12] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/LocalFileStorageService.java | Line: 19
Description: Path traversal vulnerability where loadImageAsResource() resolves a caller-supplied fileName with normalize() but no startsWith() boundary check. Combined with unauthenticated /image/ endpoint, this is exploitable without credentials.
Fix: Add filePath.startsWith(imageStorageLocation) check after normalize(). Add character allowlist validation.

[P1-B29-13] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ImageController.java | Line: 30
Description: No input validation is applied to the fileName path variable before passing to loadImageAsResource() -- no character allowlist, no max length check, no path separator rejection.
Fix: Add a regex constraint to the @PathVariable or validate fileName against [a-zA-Z0-9._-]+ before processing.

[P1-B29-14] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/LocalFileStorageService.java | Line: 24
Description: The 404 error message includes the full absolute filesystem path of the server's storage directory, available to any unauthenticated requester since /image/ has no auth.
Fix: Return a generic "file not found" message. Log the full path server-side only.

[P1-B29-15] CRITICAL | File: pom.xml | Line: 12
Description: Spring Framework 3.2.14.RELEASE and Spring Security 3.1.1.RELEASE are both severely end-of-life (since 2016) with multiple unpatched CVEs including RCE vulnerabilities.
Fix: Upgrade to currently supported Spring and Spring Security versions.

[P1-B29-16] CRITICAL | File: pom.xml | Line: 99
Description: Jackson Databind 2.6.7, commons-fileupload 1.3.1, and Spring OAuth2 1.0.0.RELEASE are all end-of-life with known critical CVEs including deserialization RCE and DoS.
Fix: Upgrade all three dependencies to current supported versions.

[P1-B29-17] LOW | File: pom.xml | Line: 168
Description: The commons-io dependency uses groupId org.apache.commons which is incorrect for Apache Commons IO (should be commons-io:commons-io), potentially resolving to an incorrect artifact.
Fix: Change the Maven coordinate to commons-io:commons-io and upgrade to version 2.15.x or later.

[P1-B29-18] MEDIUM | File: pom.xml | Line: 69
Description: The uat Maven profile is marked activeByDefault=true, meaning a plain mvn invocation will use UAT configuration including production-equivalent database credentials.
Fix: Remove activeByDefault from the uat profile. Require explicit -P selection.

[P1-B29-19] INFO | File: N/A | Line: N/A
Description: No bitbucket-pipelines.yml file is present in the repository. There is no automated CI/CD pipeline for build verification, test execution, or controlled deployment.
Fix: Establish a CI/CD pipeline with automated testing, security scanning, and deployment gates.

[P1-B30-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 109
Description: A bearer/API authentication token (X-AUTH-TOKEN) is hardcoded as a string literal in source code and committed to the repository, providing any reader with API access.
Fix: Move the token to environment variables or a secrets manager. Rotate the token immediately.

[P1-B30-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 14
Description: A Google Cloud Messaging (GCM/FCM) server API key is hardcoded as a public static field, granting the ability to send push notifications to all registered devices.
Fix: Move the key to a secrets manager or environment variable. Rotate or restrict the key in the Google Cloud Console.

[P1-B30-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 18
Description: Clickatell SMS gateway credentials (username, password, and API ID) are hardcoded as public static fields, allowing arbitrary SMS sending billed to the organisation's account.
Fix: Move credentials to a secrets manager. Rotate the Clickatell password.

[P1-B30-4] HIGH | File: environment.dev.properties | Line: 15
Description: Cognito API credentials (ciiadmin/ciiadmin) are committed in plaintext in all three environment property files with identical weak credentials across all environments.
Fix: Rotate credentials per environment. Remove files from version control.

[P1-B30-5] HIGH | File: pom.xml | Line: 29
Description: Database credentials for Flyway migrations (including production RDS password C!1admin) are hardcoded in pom.xml profiles committed to the repository.
Fix: Remove credentials from pom.xml. Use environment variables or CI/CD pipeline variables.

[P1-B30-6] MEDIUM | File: .gitignore | Line: 6
Description: The .gitignore only excludes environment.local.properties while dev, uat, and prod environment files containing credentials are tracked in git.
Fix: Add all environment.*.properties files to .gitignore and remove from tracking.

[P1-B30-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 31
Description: downloadFile() constructs a URL from the fileURL parameter with no scheme validation, no host whitelist, and no block on private/link-local addresses (e.g., 169.254.169.254 AWS metadata), enabling full SSRF if called with user-controlled input.
Fix: Validate the URL scheme (allow only https), maintain a hostname allowlist, and block private/link-local IP ranges before opening connections.

[P1-B30-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 100
Description: sendPost() constructs a URL by concatenating a hardcoded base URL with the unsanitized fname parameter over plain HTTP (not HTTPS), exposing request body and response PDF data to network interception.
Fix: Sanitize fname for path traversal characters. Change the transport to HTTPS.

[P1-B30-9] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 50
Description: Path traversal in downloadFile() where the filename used for the file write path is taken from the HTTP Content-Disposition response header or URL with no sanitization, allowing a malicious server to write files to arbitrary paths.
Fix: Sanitize the filename by stripping path separators and traversal sequences. Verify the resolved save path stays within saveDir.

[P1-B30-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 130
Description: Path traversal in sendPost() where the fname parameter is concatenated directly into the file save path without sanitization for path traversal characters.
Fix: Sanitize fname to remove path separators and traversal sequences. Verify the resolved path stays within saveDir.

[P1-B30-11] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 19
Description: saveFilePath and fileName are private static mutable fields causing a race condition in multi-threaded Tomcat where concurrent requests can read the file path set by another request, leading to cross-user data leakage.
Fix: Replace static fields with local variables returned from the method, or use ThreadLocal, or restructure to return the path from the method.

[P1-B30-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/DateUtil.java | Line: 21
Description: The exception message in parseDate includes the raw user-supplied dateString value, which could be reflected in HTTP error responses.
Fix: Use a generic error message in the exception without echoing user input.

[P1-B30-13] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 120
Description: Report request payloads (potentially containing operator and forklift identifiers), file paths, and API URLs are logged to System.out (Tomcat stdout) at production verbosity.
Fix: Replace System.out.println with structured logging at DEBUG level only.

[P1-B30-14] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 86
Description: Exceptions are silently swallowed after e.printStackTrace() to stderr, meaning callers receive no indication of download failure while stack traces expose internal class structure.
Fix: Propagate exceptions to callers. Replace e.printStackTrace() with structured logging.

[P1-B30-15] HIGH | File: pom.xml | Line: 87
Description: The Splunk Maven repository is configured with a plaintext HTTP URL, enabling network-level artifact substitution during builds.
Fix: Change the URL to HTTPS.

[P1-B31-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/util/SMTPAuthenticator.java | Line: 9
Description: AWS IAM Access Key ID and Secret Access Key are hardcoded as string literals in the getPasswordAuthentication() method and committed to the repository since the initial commit.
Fix: Immediately rotate these credentials in AWS IAM. Replace with environment variable injection or AWS Secrets Manager.

[P1-B31-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 19
Description: Clickatell SMS gateway password (OVLOaICXccaNUS), username (ciclickatell), and API ID (3629505) are hardcoded as public static fields, providing full access to the SMS sending account.
Fix: Move to a secrets manager. Rotate the Clickatell password immediately.

[P1-B31-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 14
Description: A Google Cloud Messaging (GCM/FCM) server API key is hardcoded as a public static field, enabling arbitrary push notifications to all registered operator devices.
Fix: Move to a secrets manager or environment variable. Restrict or rotate the key.

[P1-B31-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 30
Description: An internal AWS EC2 instance hostname is hardcoded with a plain HTTP URL for the PDF export API, exposing infrastructure topology and transmitting PDF content without encryption.
Fix: Change to HTTPS. Move the URL to environment configuration.

[P1-B31-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/SendEmail.java | Line: 31
Description: Email header injection vulnerability where mailTo is passed directly to InternetAddress.parse() with strict=false and subject is set without sanitization. Crafted inputs with newlines could inject additional SMTP headers.
Fix: Validate and sanitize mailTo and subject by stripping \r and \n characters before use.

[P1-B31-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/SendEmail.java | Line: 33
Description: All exception handling in sendMail() routes to System.out.println or e.printStackTrace(), exposing internal class names and potentially recipient email addresses (PII) in production logs.
Fix: Replace with structured SLF4J logging. Avoid logging recipient email addresses.

[P1-B31-7] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/RuntimeConf.java | Line: 4
Description: RuntimeConf.database is a public mutable static field (not final), meaning any class can overwrite the JNDI database name at runtime, potentially redirecting database operations.
Fix: Change to public static final to prevent runtime mutation.

[P1-B31-8] INFO | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 5
Description: Email-related fields in RuntimeConfig (host, port, sfport, sfclass) are commented as "unused" but remain as public mutable static fields with default values that could configure an unauthenticated local MTA if referenced.
Fix: Remove the dead code fields entirely.

[P1-B31-9] INFO | File: src/main/java/com/journaldev/spring/jdbc/util/SMTPAuthenticator.java | Line: N/A
Description: It is unclear whether SMTPAuthenticator is actually wired into the JNDI mail session or is dead code. Regardless, the hardcoded AWS credentials remain exposed in the repository.
Fix: Confirm whether SMTPAuthenticator is in use. If not, remove it. If so, externalize credentials.

[P1-B32-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 66
Description: AWS SES SMTP credentials (IAM access key ID AKIA**REDACTED** and 40-character secret key) are hardcoded inside a PasswordAuthentication anonymous class and committed to version control.
Fix: Immediately rotate credentials. Replace with environment variable injection or AWS Secrets Manager.

[P1-B32-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 14
Description: A Google Cloud Messaging (GCM/FCM) server API key is hardcoded as a public static field, enabling push notification spam or social engineering of forklift operators.
Fix: Move to a secrets manager. Restrict or rotate the key.

[P1-B32-3] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 18
Description: Clickatell SMS gateway credentials (username, cleartext password, API ID) are hardcoded as public static fields, enabling unauthorized SMS sending billed to the organisation.
Fix: Move to a secrets manager. Rotate credentials immediately.

[P1-B32-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 112
Description: The mobile_no parameter is split and inserted directly into the Clickatell API URL without URL encoding, enabling HTTP parameter injection that could redirect SMS to arbitrary recipients or alter the message.
Fix: URL-encode each mobile number element before embedding it in the API URL.

[P1-B32-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 154
Description: The readLines method opens a URL connection with no scheme validation or hostname allowlist. RuntimeConfig.LOCATION is public, non-final, and mutable at runtime, meaning any code that modifies it creates a full SSRF primitive.
Fix: Make RuntimeConfig.LOCATION final. Add URL scheme validation and hostname allowlist checks before opening connections.

[P1-B32-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 100
Description: The attachment parameter of sendMail is passed directly to FileDataSource without any path validation or canonicalization, allowing path traversal to attach arbitrary server-side files to outbound emails.
Fix: Validate the attachment path against an allowlist of permitted directories. Canonicalize and verify the resolved path stays within allowed bounds.

[P1-B32-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 30
Description: An AWS EC2 instance hostname with public IP is hardcoded with a plain HTTP URL for the PDF export API, exposing infrastructure topology and transmitting data without encryption.
Fix: Change to HTTPS. Move the URL to environment-injected configuration.

[P1-B32-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 48
Description: The init method logs the full mobile number (PII) and complete SMS message body at INFO level, which will appear in production log files.
Fix: Redact or mask the mobile number and message body in log statements.

[P1-B32-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 134
Description: Successful sends log the full destination mobile number at INFO level; authentication failures log the verbatim API response which may contain session tokens or account information.
Fix: Mask mobile numbers in logs. Avoid logging raw API responses that may contain tokens.

[P1-B32-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 79
Description: The rEmail parameter is passed to InternetAddress.parse() with strict=false and no prior format validation, allowing malformed addresses that cause silent send failures since exceptions are swallowed.
Fix: Validate rEmail against an email format regex or @Email annotation before passing to InternetAddress.parse.

[P1-B32-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 13
Description: All credential and configuration fields in RuntimeConfig are declared public static non-final, meaning any class can mutate GCM key, Clickatell password, SMTP credentials, and SMS gateway URL at runtime.
Fix: Change all credential and configuration fields to public static final.

[P1-B32-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 53
Description: Both SendMessage and Util use e.printStackTrace() and System.out.println() for exception reporting rather than the SLF4J logger, bypassing log-level filtering and exposing internal class structure.
Fix: Replace all e.printStackTrace() and System.out.println with structured SLF4J logging.

[P1-B32-13] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 36
Description: The init method accepts mobile_no with no validation that the caller is authorized to trigger SMS delivery to that number -- no authentication context check, no rate limiting, no organisation verification.
Fix: Add caller authorization checks and rate limiting before SMS dispatch.

[P1-B32-14] INFO | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 163
Description: DataInputStream.readLine() has been deprecated since Java 1.1 due to incorrect multi-byte character handling and is used to read Clickatell API responses.
Fix: Replace DataInputStream.readLine() with BufferedReader.readLine() using explicit character encoding.

---

## Pass 2 — Test Coverage

[P2-ACFG-1] CRITICAL | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: N/A
Description: OAuth2 client secrets are hardcoded in plain text in source control. Two OAuth2 clients (987654321 and fleetiq360) have their secrets committed to the repository in spring-security.xml.
Fix: Externalize OAuth2 client secrets to an encrypted secrets manager or environment variables and remove them from source control.

[P2-ACFG-2] CRITICAL | File: settings.xml | Line: N/A
Description: Deployment credentials for two Tomcat servers (TomcatServerUat and TomcatServerAzure) are stored in plain text in a committed settings.xml file. The UAT password also matches the Flyway password, indicating credential reuse.
Fix: Remove settings.xml from version control, use a local untracked settings.xml or CI/CD secret injection for deployment credentials, and eliminate credential reuse.

[P2-ACFG-3] CRITICAL | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: N/A
Description: The authenticationManager uses MD5 as the password hashing algorithm. MD5 is cryptographically broken, unsalted, and trivially reversible via rainbow tables.
Fix: Replace MD5 password hashing with bcrypt or Argon2 using Spring Security's BCryptPasswordEncoder and migrate existing password hashes.

[P2-ACFG-4] CRITICAL | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: N/A
Description: OAuth2 client 987654321 has access-token-validity set to 0, meaning tokens issued to this client never expire. Combined with hardcoded credentials and ROLE_CLIENT authority, this creates an indefinitely valid credential.
Fix: Set a finite access-token-validity (e.g., 300 seconds) for all OAuth2 clients and implement token rotation.

[P2-ACFG-5] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: N/A
Description: The endpoints /oauth/cache_approvals and /oauth/uncache_approvals are configured with security="none" and annotated with a comment "Just for testing." They are completely unprotected in the production configuration.
Fix: Remove or secure these test endpoints. If they are not needed, delete the security configuration entries entirely.

[P2-ACFG-6] HIGH | File: src/main/webapp/WEB-INF/web.xml | Line: N/A
Description: servlet-context.xml is loaded twice, once as the root application context via ContextLoaderListener and once as the DispatcherServlet context, causing all beans to be instantiated twice.
Fix: Remove servlet-context.xml from the root context-param and keep it only as the DispatcherServlet's contextConfigLocation. Load spring-security.xml separately.

[P2-ACFG-7] HIGH | File: src/main/resources/logback.xml | Line: N/A
Description: APKUpdaterController is permanently set to DEBUG log level with a comment indicating this was a temporary change to resolve a production issue. DEBUG logging in production risks exposing sensitive data.
Fix: Set APKUpdaterController log level to INFO or WARN and remove the temporary DEBUG configuration.

[P2-ACFG-8] HIGH | File: src/main/resources/logback.xml | Line: N/A
Description: The com.journaldev.spring logger is declared twice with different appenders and additivity settings, and two root elements are also present. This creates undefined log routing behavior.
Fix: Consolidate duplicate logger declarations into single entries with multiple appender-refs and use a single root element.

[P2-ACFG-9] HIGH | File: pom.xml | Line: N/A
Description: The local Maven profile defines flyway.url, flyway.user, and flyway.password twice each. Maven uses the last-defined value, silently overriding the first set which references a different database.
Fix: Remove the duplicate Flyway property definitions in the local profile and keep only the correct database target.

[P2-ACFG-10] HIGH | File: environment.prod.properties | Line: N/A
Description: The prod and uat environment property files are byte-for-byte identical, including the same AWS EC2 IP, imagePrefix=uat- (not prod-), and the same Cognito credentials. A production-specific configuration was never created.
Fix: Create a distinct environment.prod.properties with production-specific URLs, image prefix, and credentials.

[P2-ACFG-11] HIGH | File: pom.xml | Line: N/A
Description: Spring Framework 3.2.14.RELEASE, Spring Security 3.1.1.RELEASE, Spring Security OAuth2 1.0.0.RELEASE, Jackson Databind 2.6.7, and JUnit 4.7 are all end-of-life with known CVEs.
Fix: Upgrade to supported framework versions: Spring Framework 5.x/6.x, Spring Security 5.x/6.x, Jackson 2.15+, and JUnit 4.13+ or JUnit 5.

[P2-ACFG-12] HIGH | File: pom.xml | Line: N/A
Description: The only test-scoped dependency is JUnit 4.7. There is no spring-test, mockito-core, or in-memory database dependency, making integration tests structurally impossible.
Fix: Add spring-test, mockito-core, and an in-memory database (H2) to test-scoped dependencies in pom.xml.

[P2-ACFG-13] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: N/A
Description: JdbcTokenStore relies on OAuth2 token tables that must pre-exist in the database, but Flyway is disabled on both UAT and prod environments, so migrations never run automatically.
Fix: Enable Flyway migrations on all environments or implement a separate schema management process to ensure token store tables exist.

[P2-ACFG-14] MEDIUM | File: src/main/resources/META-INF/context.xml | Line: N/A
Description: No JNDI DataSource Resource is defined in the version-controlled context.xml. The datasource must be configured at the Tomcat server level, outside of version control.
Fix: Either define the JNDI Resource in context.xml or document the required Tomcat server-level configuration and add deployment verification.

[P2-ACFG-15] MEDIUM | File: src/test/java/com/journaldev/spring/jdbc/service/APKUpdaterServiceTest.java | Line: N/A
Description: All substantive test methods in APKUpdaterServiceTest are commented out, leaving the class as an effectively empty test with no active assertions.
Fix: Uncomment and fix the test methods or rewrite them to properly test APKUpdaterService.

[P2-ACFG-16] MEDIUM | File: src/main/resources/logback.xml | Line: N/A
Description: No test-scoped logback configuration exists. Tests use the production logback.xml which may send log events to a production Splunk instance via the TCP appender.
Fix: Create src/test/resources/logback-test.xml with console-only appenders to prevent test log output from reaching production systems.

[P2-ACFG-17] MEDIUM | File: src/main/webapp/WEB-INF/spring/appServlet/servlet-context.xml | Line: N/A
Description: CommonsMultipartResolver is configured with a 20MB maxUploadSize and 1MB maxInMemorySize but there is no test validating that oversized uploads are rejected.
Fix: Add integration tests that verify uploads exceeding the size limit are rejected with an appropriate HTTP error response.

[P2-ACFG-18] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/Configuration.java | Line: N/A
Description: Configuration.java has zero test coverage. All 10 @Value-injected properties used throughout the application are untested for correct binding and missing-property behavior.
Fix: Add a Spring context integration test that loads Configuration with a test properties file and asserts all @Value bindings resolve correctly.

[P2-ACFG-19] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: N/A
Description: No integration test verifies the role-based access control rules on REST endpoints (/rest/db/**, /rest/apk/**, /rest/**).
Fix: Add MockMvc or Spring Security integration tests that verify each role can only access its authorized endpoints and that unauthorized access returns 401/403.

[P2-ACFG-20] MEDIUM | File: pom.xml | Line: N/A
Description: Flyway migrations are disabled on UAT and prod environments and no integration test exercises migration execution or validates migration scripts.
Fix: Add integration tests that run Flyway migrations against an in-memory database to validate the migration scripts.

[P2-ACFG-21] LOW | File: pom.xml | Line: N/A
Description: The UAT Maven profile has activeByDefault=true, so builds without an explicit profile selection will use UAT configuration including AWS RDS URLs and Cognito credentials.
Fix: Remove activeByDefault from the UAT profile or set it on a safe default profile (e.g., local).

[P2-ACFG-22] LOW | File: src/main/resources/fleetiq360ws.properties | Line: N/A
Description: The acceptURL property is hardcoded to the production domain and not parameterized through Maven filters, causing dev and UAT environments to send driver acceptance emails with production links.
Fix: Replace the literal acceptURL value with a Maven placeholder (${acceptURL}) and define environment-specific values in each environment properties file.

[P2-ACFG-23] LOW | File: environment.dev.properties | Line: N/A
Description: Cognito API credentials (cognitoAPIUsername=ciiadmin, cognitoAPIPassword=ciiadmin) are identical weak values across all environments.
Fix: Use unique, strong credentials for each environment and externalize them from version-controlled property files.

[P2-A01-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: N/A
Description: No tests exist for APIDAO, APIDAOImpl, or CompanyDAO. The entire test suite contains zero references to any class name, method name, or bean qualifier from these three files.
Fix: Create unit and integration tests for all DAO methods covering happy paths, empty results, and error conditions.

[P2-A01-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: 28
Description: The checkKey method is a stub that always returns true regardless of input. The SQL query that should implement the check is commented out. Any caller assumes the API key is valid when no actual validation occurs.
Fix: Implement the actual API key validation logic or remove the method if it is no longer needed. Add tests to verify correct key validation behavior.

[P2-A01-3] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: 40
Description: findByName uses queryForObject with Driver.class as a RowMapper, but this overload is intended for scalar types only. It will throw IncorrectResultSetColumnCountException at runtime because Driver is a multi-field POJO.
Fix: Replace Driver.class with a BeanPropertyRowMapper<Driver>(Driver.class) or a custom RowMapper implementation.

[P2-A01-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: 36
Description: findByName does not catch EmptyResultDataAccessException when queryForObject returns no rows. Callers receive an unhandled Spring DAO exception instead of a controlled null or Optional.empty() result.
Fix: Wrap queryForObject in a try/catch for EmptyResultDataAccessException and return null or Optional.empty() when no user is found.

[P2-A01-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: 36
Description: findByName does not handle IncorrectResultSizeDataAccessException when multiple users match the MD5 email query, which could occur due to MD5 collisions or data anomalies.
Fix: Add error handling for IncorrectResultSizeDataAccessException and log a warning if multiple rows match.

[P2-A01-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 154
Description: CompanyResultResetExtractor throws NullPointerException when the result set is empty because cie remains null and cie.setArrRoles(roles) is called unconditionally.
Fix: Add a null check for cie before calling setArrRoles, and return null or an empty result when the query returns no rows.

[P2-A01-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 36
Description: CompanyDAO.save is not annotated with @Transactional despite performing four separate SQL write operations. A failure partway through leaves the database in a partially written state with no rollback.
Fix: Add @Transactional annotation to the save method to ensure atomicity of the multi-statement write operation.

[P2-A01-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 92
Description: findAllByKeyword concatenates the keyword directly into a LIKE pattern without escaping LIKE metacharacters (% and _), allowing wildcard injection that can return far more rows than intended.
Fix: Escape LIKE metacharacters in the keyword before binding it as a parameter.

[P2-A01-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 87
Description: If keyword is null, the expression "%"+null+"%" evaluates to "%null%", performing a literal search for the text "null" instead of failing or returning all records.
Fix: Add a null guard for keyword and either throw IllegalArgumentException or return an empty list.

[P2-A01-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 110
Description: CompaniesResultResetExtractor uses reference equality (!=) to compare Long objects. For Long values outside the JVM cached range (-128 to 127), two distinct Long objects with the same value will not be ==, causing duplicate Company entries.
Fix: Replace companyId != previousCompanyId with !companyId.equals(previousCompanyId).

[P2-A01-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 111
Description: CompaniesResultResetExtractor fails to attach roles to a company when its roles list is empty, leaving arrRoles as null. Callers iterating arrRoles without a null check would throw NPE.
Fix: Call setArrRoles unconditionally for each company, passing an empty list when no roles are found.

[P2-A01-12] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: 37
Description: findByName logs the username at INFO level with a misleading message label saying "Start checkKey for" when the method is actually findByName, indicating a copy-paste error.
Fix: Correct the log message to reference findByName and review whether the username should be logged at INFO level.

[P2-A01-13] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAO.java | Line: 10
Description: APIDAO interface declares checkKey but the implementation is a permanent stub returning true. Neither the interface nor the implementation has any documentation describing expected behavior.
Fix: Add Javadoc to the interface methods describing expected behavior, error conditions, and return value semantics, and implement or remove checkKey.

[P2-A01-14] LOW | File: src/test/java/com/journaldev/spring/jdbc/service/APKUpdaterServiceTest.java | Line: 17
Description: APKUpdaterServiceTest has its only meaningful tests commented out, leaving the test class with no active test methods and contributing no assertions.
Fix: Uncomment and fix the test methods or rewrite them to provide active test coverage.

[P2-A02-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: N/A
Description: No test coverage exists for DriverDAO or DriverDAOImpl. All ten methods in this class are completely untested across the entire test suite.
Fix: Create comprehensive unit and integration tests for all DriverDAOImpl methods covering happy paths, not-found cases, and error conditions.

[P2-A02-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/DAO/EmailLayoutDAO.java | Line: N/A
Description: No test coverage exists for EmailLayoutDAO. Neither the constructor nor the only public method has any test coverage.
Fix: Create tests for EmailLayoutDAO, particularly verifying that getEmailLayoutByType returns actual database data.

[P2-A02-3] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/DAO/EmailLayoutDAO.java | Line: 21
Description: getEmailLayoutByType is a stub that always returns an empty EmailLayout object without querying the database. The type parameter is accepted but never used. Any caller relying on this method receives an empty object.
Fix: Implement the actual database query in getEmailLayoutByType or remove the method if email layouts are no longer needed.

[P2-A02-4] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 66
Description: The update method uses the wrong column name "iduser" in the WHERE clause, but all other methods in the class use "id". This causes the update to always affect 0 rows and always throw SQLException.
Fix: Change "where iduser = ?" to "where id = ?" in the update SQL statement.

[P2-A02-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 120
Description: findByEmailAndPassword is @Deprecated but remains in the interface and implementation with no migration path. It silently returns Optional.empty() on EmptyResultDataAccessException, which is indistinguishable from "driver not found."
Fix: Identify and remove all callers, then remove the deprecated method from both the interface and implementation.

[P2-A02-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 40
Description: isDriverExist is not tested for null email, empty string, or edge cases. A null email binds as SQL NULL, silently indicating the driver does not exist rather than raising an error.
Fix: Add a null/empty guard for the email parameter and throw IllegalArgumentException for invalid inputs.

[P2-A02-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 48
Description: The save method has no error handling for DataAccessException. Failures such as duplicate email, sequence exhaustion, or constraint violations propagate as unchecked exceptions with no meaningful message.
Fix: Add appropriate exception handling in save to provide meaningful error messages for common failure scenarios.

[P2-A02-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 90
Description: updatePassword uses MD5 hashing via SQL md5() function with no validation that null or empty passwords are rejected before reaching the database.
Fix: Add null/empty validation for the password parameter before executing the SQL update, and plan migration from MD5 to bcrypt.

[P2-A02-9] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 138
Description: findAllByCompanyOwner returns an empty list silently for unknown ownerId with no way for the caller to distinguish a valid empty result from a bad owner ID.
Fix: Add validation for ownerId (e.g., reject zero or negative values) and add tests covering boundary conditions.

[P2-A02-10] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 151
Description: findAllTraining logs "Start findAllByCompanyOwner for ownerId" which is a copy-paste error from findAllByCompanyOwner. The logged method name and parameter label are incorrect.
Fix: Correct the log message to reference findAllTraining and the driverId parameter.

[P2-A02-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 110
Description: findByID uses the deprecated Object[] vararg API for queryForObject and passes url as the first positional parameter. No test verifies that BeanPropertyRowMapper correctly maps all fields including aliased columns.
Fix: Migrate to the non-deprecated queryForObject overload and add tests verifying correct field mapping.

[P2-A02-12] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/EmailLayoutDAO.java | Line: 11
Description: EmailLayoutDAO has no Spring stereotype annotation (@Repository, @Component) and is not declared as a @Bean, so it cannot be autowired consistently.
Fix: Add @Repository annotation to EmailLayoutDAO or declare it as a @Bean in a configuration class.

[P2-A02-13] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 77
Description: updateLastLoginTime throws SQLException when driver.getId() does not match any row, but unlike findByID it does not filter on active status, so an inactive driver's login time could be updated.
Fix: Add an active status filter to the updateLastLoginTime query and add tests for the driver-not-found path.

[P2-A02-14] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 23
Description: BASE_QUERY_DRIVER duplicates the p.enabled = true predicate in both the join condition and the WHERE clause added by findAllByCompanyOwner.
Fix: Remove the redundant p.enabled = true predicate from either the base query join or the findAllByCompanyOwner WHERE clause.

[P2-A02-15] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 129
Description: findByEmailAndPassword catches only EmptyResultDataAccessException but not other DataAccessException subtypes, causing connection failures to propagate differently from not-found results.
Fix: Broaden the catch to DataAccessException or add specific handling for other expected exception types.

[P2-A03-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java | Line: N/A
Description: No test coverage exists for EquipmentDAOImpl or EquipmentDAO interface. All three interface methods (getEquipmentByUser, getEquipmentIdByMacAddress, getEquipmentByMacAddress) are entirely untested.
Fix: Create unit and integration tests for all EquipmentDAOImpl methods.

[P2-A03-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java | Line: N/A
Description: No test coverage exists for ImpactDAO. All three public methods (save, isImpactRecorded, sendImpactNotification) are entirely untested despite being the core business logic of impact event recording and alerting.
Fix: Create comprehensive tests for ImpactDAO covering save, duplicate detection, and notification dispatch.

[P2-A03-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java | Line: 53
Description: Both getEquipmentByMacAddress and getEquipmentIdByMacAddress call queryForObject which throws EmptyResultDataAccessException when no row matches a MAC address. Neither exception is caught within the DAO.
Fix: Add try/catch for EmptyResultDataAccessException and return null or Optional.empty() for not-found MAC addresses.

[P2-A03-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java | Line: 39
Description: ImpactDAO.save silently discards any impact event where impact_value is less than 80000 with a bare return and no logging. The threshold is a hard-coded magic number with no documentation.
Fix: Extract the threshold to a named constant or configuration property, add logging for discarded events, and add tests for boundary values.

[P2-A03-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java | Line: 46
Description: ImpactDAO.save throws SQLException when the INSERT returns zero rows affected, but this error path is never tested and the error message composition could fail with a secondary exception if impact fields are null.
Fix: Add null guards for error message fields and add tests covering the zero-rows-affected path.

[P2-A03-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java | Line: 64
Description: sendImpactNotification contains two untested notification branches (Red Impact Alert email and Red Impact SMS) with no test covering either happy path or failure scenarios.
Fix: Add tests for both notification branches, including valid notifications, null phone numbers, and unrecognized subscription names.

[P2-A03-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java | Line: 66
Description: If CognitoService.getUser fails and returns an empty UserResponse, null fields will cause NullPointerException in string concatenation, terminating processing of all remaining notifications.
Fix: Add null checks on UserResponse fields before building email/SMS content and handle CognitoService failures gracefully.

[P2-A03-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java | Line: 47
Description: getEquipmentByUser does not validate that configuration.getSystemImageURL() is non-null/non-empty before using it as a SQL query parameter, which would produce malformed URL values in every result row.
Fix: Add a null/empty guard for systemImageURL and throw an appropriate exception if the configuration value is missing.

[P2-A03-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java | Line: 75
Description: ImpactDAO references logger.info() but declares no logger field. JdbcDaoSupport does not expose a public logger. The class is not annotated with @Slf4j. This may be a latent compile-time defect.
Fix: Add a private static final Logger field or add the @Slf4j annotation to the class.

[P2-A03-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java | Line: 54
Description: Three queryForObject calls use the deprecated Object[] API which will break on Spring 6.x migration.
Fix: Migrate to the non-deprecated varargs form of queryForObject.

[P2-A03-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java | Line: 54
Description: isImpactRecorded does not guard against null impact_time. A null timestamp causes the duplicate detection query to always return zero matches due to SQL NULL comparison semantics, allowing duplicate impacts to be saved.
Fix: Add a null check for impact_time before executing the duplicate detection query and reject events with null timestamps.

[P2-A03-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java | Line: 53
Description: getEquipmentIdByMacAddress is defined in the interface but never called in production code. The controller uses getEquipmentByMacAddress instead, making this method dead code.
Fix: Remove getEquipmentIdByMacAddress from both the interface and implementation if it is confirmed unused.

[P2-A03-13] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java | Line: 49
Description: Configuration.getSystemImageURL() is not validated before use as a query binding parameter. A missing or blank property would produce malformed URLs in every row.
Fix: Add validation for systemImageURL at application startup or in the DAO method before use.

[P2-A04-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/DAO/ManufacturerDAOImpl.java | Line: 26
Description: No unit or integration tests exist for getManufacturersForUser, the sole implementation of ManufacturerDAO. The method is called at runtime in EquipmentController.getManufactureList() and is entirely untested.
Fix: Create tests for getManufacturersForUser verifying correct SQL result mapping and behavior for various inputs.

[P2-A04-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 33
Description: No tests exist for UserDAO.findByName, which is the Spring Security authentication entry point called by UserDetailsServiceImpl.loadUserByUsername(). The ResultSetExtractor lambda, multi-role accumulation, and Optional.empty() return are all untested.
Fix: Create tests for findByName covering single-role users, multi-role users, and not-found cases.

[P2-A04-3] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 61
Description: No tests exist for UserDAO.findByAuthority, which is called during driver registration. The Optional.empty() branch, BeanPropertyRowMapper mapping, and non-existent authority case are all untested.
Fix: Create tests for findByAuthority covering existing authorities, missing authorities, and duplicate authority scenarios.

[P2-A04-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 61
Description: findByAuthority calls queryForObject which throws EmptyResultDataAccessException for zero rows, making the null-check on the result unreachable. The Optional.empty() return path can never be exercised.
Fix: Wrap queryForObject in a try/catch for EmptyResultDataAccessException and return Optional.empty() in the catch block.

[P2-A04-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 61
Description: findByAuthority does not handle IncorrectResultSizeDataAccessException if the roles table contains duplicate authority values. There is no unique-constraint validation in the DAO.
Fix: Add error handling for multiple-row results and consider adding a unique constraint on the authority column.

[P2-A04-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/ManufacturerDAOImpl.java | Line: 29
Description: The SQL query passes username as both bind parameters but no test verifies the correct ordering. A null or empty username could produce a SQL error or unintended full-table scan.
Fix: Add a null/empty guard for username and add tests verifying correct parameter binding order.

[P2-A04-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/ManufacturerDAOImpl.java | Line: 31
Description: The SQL query string concatenation has a missing space before "or company_id in", producing potentially malformed SQL that may fail depending on the SQL parser.
Fix: Add the missing space in the SQL string concatenation between the subquery close parenthesis and the "or" keyword.

[P2-A04-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 31
Description: QUERY_USER_BY_NAME matches on both u.name = ? and md5(u.name) = ?, but no test verifies that passing an MD5-formatted string correctly resolves a user or that plain names do not accidentally match MD5 column values.
Fix: Add tests covering both plain-name and MD5-hashed-name lookup paths.

[P2-A04-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 36
Description: The ResultSetExtractor lambda initializes user to null and accumulates roles from subsequent rows, but no test verifies the multi-role accumulation or the behavior for users with zero, one, or multiple roles.
Fix: Add tests verifying correct role accumulation for users with varying numbers of roles.

[P2-A04-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 23
Description: UserDAO declares a Logger field that is never invoked in any method. The absence of logging in the security-critical authentication lookup path makes diagnosis of authentication failures impossible.
Fix: Either add diagnostic logging to findByName and findByAuthority or remove the unused logger field.

[P2-A04-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/ManufacturerDAOImpl.java | Line: 27
Description: The method logs the username (which is an email address) at INFO level unconditionally, exposing PII in application logs.
Fix: Remove or redact the username from the INFO-level log statement, or reduce the log level to DEBUG.

[P2-A04-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/ManufacturerDAO.java | Line: N/A
Description: The interface declares a single method with no Javadoc. The contract for null inputs is undefined and no guard exists in the implementation.
Fix: Add Javadoc documenting expected behavior, parameters, return values, and null-handling contract.

[P2-A04-13] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/ManufacturerDAOImpl.java | Line: 21
Description: Both ManufacturerDAOImpl and UserDAO @Autowired datasource-injection methods are completely untested. Datasource misconfiguration is only discovered at application startup.
Fix: Add Spring context integration tests that verify the datasource bean wiring.

[P2-A04-14] INFO | File: src/test/java/com/journaldev/spring/jdbc/service/APKUpdaterServiceTest.java | Line: N/A
Description: The entire test suite contains only three test files, none of which test any DAO class. There is no test infrastructure for database-layer testing (no in-memory database, no @JdbcTest, no mock JdbcTemplate).
Fix: Establish database testing infrastructure with an in-memory database and Spring test slices.

[P2-A05-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java | Line: N/A
Description: All three controllers (APKUpdaterController, CompanyController, ConfigurationController) have zero test coverage. No unit tests, MockMvc tests, or integration tests exist for any controller.
Fix: Create MockMvc or integration tests for all controller endpoints covering happy paths and error conditions.

[P2-A05-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java | Line: 56
Description: downloadPackage propagates uncaught APKUpdaterException and FileNotFoundException to the container, resulting in a generic 500 error with no controlled response body.
Fix: Add exception handlers for APKUpdaterException and FileNotFoundException, returning appropriate HTTP status codes and error messages.

[P2-A05-3] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java | Line: 43
Description: getAvailablePackage catches MalformedURLException and returns null with HTTP 200, misleading the client into believing the request succeeded. A TODO comment acknowledges this is unresolved.
Fix: Return a ResponseEntity with an appropriate error status code (e.g., 400 or 500) instead of returning null with HTTP 200.

[P2-A05-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 148
Description: companyAccept and companyDelete perform blind database mutations with no existence validation and always return HTTP 200 regardless of whether any rows were affected.
Fix: Check the return value of the JDBC update and return 404 if zero rows were affected.

[P2-A05-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 112
Description: CompanyController uses HttpStatus.BAD_GATEWAY (502) for business logic rejections (duplicate association, self-association, already-accepted token) instead of semantically correct codes like 409 or 400.
Fix: Replace HttpStatus.BAD_GATEWAY with HttpStatus.CONFLICT (409) or HttpStatus.BAD_REQUEST (400) for business rule violations.

[P2-A05-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 62
Description: addCompany contains embedded raw SQL with five distinct statements executed via JdbcTemplate with no transaction boundary. A failure after the initial insert leaves the database in a partially committed state.
Fix: Wrap the addCompany logic in a @Transactional method or move the SQL operations into a transactional DAO/service layer.

[P2-A05-7] HIGH | File: src/test/java/com/journaldev/spring/jdbc/service/APKUpdaterServiceTest.java | Line: 17
Description: All APKUpdaterServiceTest test methods are commented out, leaving APKUpdaterService with zero test coverage. Service-level bugs are not caught before surfacing through the controller.
Fix: Uncomment and fix the test methods or rewrite them with proper mocking to test APKUpdaterService.

[P2-A05-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java | Line: 65
Description: downloadPackage calls resource.getFilename() without a null guard. Resource.getFilename() can return null, which would produce an incorrect Content-Disposition header.
Fix: Add a null check for resource.getFilename() and provide a fallback filename.

[P2-A05-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 62
Description: addCompany accepts a @RequestBody Permissions object with no field validation (@Valid, @NotNull, null checks). Null or zero values for driver_id and comp_id reach the database layer directly.
Fix: Add Bean Validation annotations to the Permissions model and @Valid to the controller parameter.

[P2-A05-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 52
Description: searchCompany accepts an unconstrained keyword path variable with no length limit, sanitization, or pagination, enabling full table scans with single-character or wildcard keywords.
Fix: Add input validation (minimum length, maximum length) and pagination to the search endpoint.

[P2-A05-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 37
Description: getCompany binds {uid} to Long while getCompanyDrivers binds the same {uid} to int, creating an undetected truncation risk for IDs exceeding Integer.MAX_VALUE.
Fix: Use a consistent type (Long) for all ID path variables across sibling methods.

[P2-A05-12] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ConfigurationController.java | Line: 17
Description: ConfigurationController is annotated @Controller on an abstract class, creating ambiguous Spring bean registration. The annotation is non-standard on an abstract class.
Fix: Remove @Controller from the abstract class; the subclass annotations are sufficient for Spring registration.

[P2-A05-13] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 103
Description: addCompany silently swallows email-send failures because SendEmail.sendMail() internally catches all exceptions and calls printStackTrace(). The caller always returns HTTP 200 regardless of email delivery.
Fix: Refactor SendEmail.sendMail() to propagate exceptions or return a status, and log email failures in the controller.

[P2-A05-14] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java | Line: 28
Description: getURLBase is a private helper with non-trivial URL construction logic (port handling, path truncation) that is never independently testable and can only be exercised through getAvailablePackage.
Fix: Extract getURLBase into a package-private or utility method to enable direct unit testing.

[P2-A05-15] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 13
Description: RuntimeConfig declares API credentials and keys as public static non-final mutable fields. MSGID_LOGICERRORR and MSGID_CODEE_DUPLICATE_VEHICLE share the same value "3", creating ambiguous status IDs.
Fix: Make all fields final, externalize credentials, and assign unique values to distinct message ID constants.

[P2-A06-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/DatabaseController.java | Line: N/A
Description: DatabaseController, DatabaseCleanupException, and DriverController have zero test coverage. The three files collectively contain 14 public methods plus one constructor, all completely untested.
Fix: Create MockMvc or integration tests for all endpoints and exception classes.

[P2-A06-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/DatabaseController.java | Line: 94
Description: The deleteCompanies retry logic is broken. errors.clear() is called immediately before passing errors as both the accumulator and the companies list to the recursive call, meaning retry passes always process zero companies.
Fix: Create a new list from errors before clearing, and pass the new list as the companies parameter to the recursive call.

[P2-A06-3] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/DatabaseController.java | Line: 66
Description: If the JDBC query in cleanup() throws an exception, companies remains null. Execution falls through to deleteCompanies which calls companies.forEach(), causing a guaranteed NullPointerException.
Fix: Initialize companies to an empty list or add an early return in the catch block when the query fails.

[P2-A06-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DatabaseCleanupException.java | Line: 8
Description: DatabaseCleanupException constructor and its @ResponseStatus(INTERNAL_SERVER_ERROR) annotation are never tested.
Fix: Add a test verifying that the exception preserves the message and produces HTTP 500 in a Spring MVC context.

[P2-A06-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: N/A
Description: All DriverController error response paths (getLoginAuth, registerDrivers, resetPassword, uploadProfile, uploadProfileAPP) return BAD_GATEWAY and are completely untested.
Fix: Add tests for each error path verifying the correct HTTP status and response body.

[P2-A06-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: N/A
Description: Six DriverController methods (acceptDrivers, declineDriver, saveEmails, getEmails, saveLicence, updateDrivers) have no exception handling and are entirely untested. Any DataAccessException produces an uncontrolled 500 response.
Fix: Add exception handling to each method and create tests covering both happy paths and error conditions.

[P2-A06-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 59
Description: getLoginAuth is marked @Deprecated but remains an active endpoint (POST /rest/appuser/validate) with no test coverage and no documented migration plan.
Fix: Add deprecation documentation with a removal timeline, verify no active callers remain, and then remove the endpoint.

[P2-A06-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 238
Description: saveLicence and updateDrivers call DateUtil.parseDateIso() on user-controlled date strings with no error handling. Invalid dates throw IllegalArgumentException which propagates as an uncontrolled 500 response.
Fix: Add try/catch for IllegalArgumentException around date parsing and return HTTP 400 with a descriptive error message.

[P2-A06-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 154
Description: uploadProfile uses e.printStackTrace() instead of the @Slf4j-injected logger, causing the exception to appear on stdout/stderr rather than in the structured application log.
Fix: Replace e.printStackTrace() with log.error("message", e).

[P2-A06-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 140
Description: The base64 crop-image path in uploadProfile is entirely untested, including empty cropImage, valid base64, malformed base64, and strings with no comma separator.
Fix: Add tests for the base64 decoding branch covering valid, empty, and malformed inputs.

[P2-A06-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 187
Description: saveEmails insert/update branch logic is untested for both paths. The queryForObject count result could return null, causing a NullPointerException on auto-unbox.
Fix: Add null handling for the count query result and add tests for both the insert and update paths.

[P2-A06-12] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 209
Description: getEmails returns an empty DriverEmails object when no record is found, always with HTTP 200, which may mask a not-found condition.
Fix: Return HTTP 404 when no email record exists for the given UID, and add tests for both empty and populated result paths.

[P2-A06-13] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DatabaseController.java | Line: 45
Description: QUERY_COMPANIES_TO_DELETE SQL constant contains a duplicate MAC address entry ('00:07:80:AD:99:D0' appears twice in the IN-list).
Fix: Remove the duplicate MAC address from the SQL constant.

[P2-A06-14] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 108
Description: acceptDrivers and declineDriver always return the hard-coded integer 1 regardless of how many rows were actually affected. The JDBC update return value is discarded.
Fix: Return the actual number of affected rows or return a meaningful response indicating how many records were processed.

[P2-A06-15] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: N/A
Description: RuntimeConfig contains hardcoded credentials (PASSWORD, GCMKEY, API_ID) exposed in source code with no runtime override mechanism.
Fix: Externalize credentials to environment variables or a secrets manager and remove them from source code.

[P2-A07-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: N/A
Description: Zero test coverage for all 7 methods in EquipmentController, which contains non-trivial business logic including duplicate detection, conditional insert/update branches, and service history deduplication.
Fix: Create MockMvc or integration tests for all EquipmentController methods.

[P2-A07-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/ImageController.java | Line: N/A
Description: Zero test coverage for ImageController.downloadFile. The IOException fallback path and file-not-found behavior are untested.
Fix: Create tests for downloadFile covering successful downloads, missing files, and IOException handling.

[P2-A07-3] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: N/A
Description: Zero test coverage for all 4 methods in ImpactController. Three methods contain exception-handling branches with distinct HTTP response codes that are entirely untested.
Fix: Create tests for all ImpactController methods covering happy paths, error paths, and edge cases.

[P2-A07-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 39
Description: getEquipmentByUser returns HTTP 400 BAD_REQUEST when the equipment list is empty, which is an unusual and incorrect use of 400 for a not-found condition.
Fix: Return HTTP 404 NOT_FOUND or HTTP 200 with an empty list when no equipment is found.

[P2-A07-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 59
Description: The duplicate detection branch in addEquipment returns HTTP 502 BAD_GATEWAY for a logical duplicate error, which is semantically incorrect.
Fix: Return HTTP 409 CONFLICT for duplicate detection and add tests verifying the duplicate check logic.

[P2-A07-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 57
Description: When serial number is null or empty, the duplicate check query is skipped entirely, allowing two units with null serial numbers and the same name to be inserted without conflict detection.
Fix: Add duplicate detection for null/empty serial numbers based on the equipment name alone.

[P2-A07-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 150
Description: SaveService contains a 2x2 matrix of branches (update-setHrs, update-duration, insert-setHrs, insert-duration) plus a service history deduplication check, all entirely untested.
Fix: Add tests for all four SaveService branches and the deduplication check.

[P2-A07-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 83
Description: saveImpactIMAGE and saveImpactIMAGEAPP IOException paths are untested. saveImpactIMAGEAPP has an unhandled case where type is neither "image" nor "signature", resulting in a silent no-op with success returned.
Fix: Add validation for the type parameter and return an error for unrecognized values. Add tests for both IOException and invalid-type paths.

[P2-A07-9] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 152
Description: Three distinct error paths in saveImpactData (null equipment, IncorrectResultSizeDataAccessException, SQLException from save) are untested. The notification threshold branch is also untested.
Fix: Add tests for all exception paths and the notification threshold boundary.

[P2-A07-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 92
Description: getTypeList uses two different SQL queries depending on whether mid equals zero, but neither branch is tested.
Fix: Add tests for both the mid==0 and mid!=0 query branches.

[P2-A07-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 111
Description: getFuelTypeList executes an unfiltered query when manuId==0 or typeID==0 and a filtered query otherwise. Neither branch is tested.
Fix: Add tests for both the unfiltered and filtered query branches.

[P2-A07-12] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 164
Description: When an impact is already recorded, the event is silently skipped and the response still returns MSGID_SUCCESS, potentially masking data loss.
Fix: Return a distinct status code or message for duplicate impacts so clients can distinguish between saved and deduplicated events.

[P2-A07-13] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 68
Description: saveIncident calls DateUtil.parseDateTimeIso() on request body date fields with no try/catch. Malformed dates throw an uncaught IllegalArgumentException, producing an uncontrolled 500 response.
Fix: Add try/catch for IllegalArgumentException around date parsing and return HTTP 400 with an error message.

[P2-A07-14] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ImageController.java | Line: 30
Description: downloadFile always returns HTTP 200 regardless of whether the resource exists. The IOException fallback only assigns a default content type without altering the response status.
Fix: Return HTTP 404 when the requested file does not exist.

[P2-A07-15] LOW | File: src/test/java/com/journaldev/spring/jdbc/service/APKUpdaterServiceTest.java | Line: N/A
Description: All APKUpdaterServiceTest test methods are commented out, indicating a pattern of disabled tests and possibly broken test infrastructure.
Fix: Investigate why tests were commented out, fix the underlying issue, and re-enable the tests.

[P2-A07-16] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 127
Description: saveImpactIMAGEAPP silently returns success for unknown type values (not "image" or "signature") without performing any database update.
Fix: Add validation for the type parameter and return HTTP 400 for invalid values.

[P2-A07-17] INFO | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 44
Description: The logger is initialized using ConfigurationController.class instead of ImpactController.class, causing all log output to appear under the wrong logger name.
Fix: Change the logger initialization to use ImpactController.class.

[P2-A08-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java | Line: N/A
Description: Zero test coverage for LocationController. All three mapped endpoints are completely untested. The class-level Javadoc states "Not in Use" but the endpoints are actively mapped and referenced by RestURIConstants.
Fix: Create tests for all three endpoints, and either remove the controller if truly unused or update the misleading Javadoc.

[P2-A08-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java | Line: N/A
Description: Zero test coverage for ReportAPI. All methods including the constructor, downloadPDF, getExportDir, and all accessors are untested. The class orchestrates external HTTP communication and filesystem writes.
Fix: Create unit tests for ReportAPI with mocked HTTP dependencies, covering PDF download, export directory resolution, and error conditions.

[P2-A08-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java | Line: 57
Description: saveGPSLocation silently discards GPS records when both latitude and longitude are zero, returning HTTP 200 with MSGID_SUCCESS. Valid coordinates at (0.0, 0.0) on the prime meridian/equator are also silently discarded. Same defect in saveGPSLocations at line 78.
Fix: Use a more specific validity check (e.g., null check or explicit invalid marker) rather than treating (0,0) as invalid.

[P2-A08-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java | Line: 84
Description: DateUtil.parseDateTimeIso() is called inside a forEach lambda with no try/catch in saveGPSLocations. A malformed gps_time in any entry aborts the entire batch with partially committed data and no rollback.
Fix: Add try/catch around the date parsing inside the forEach loop and wrap the batch in a transaction.

[P2-A08-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java | Line: 34
Description: getExportDir computes a path from the class's code-source location at line 35, but line 43 overwrites this entirely with "/" + dirctory, making the computation dead code. The method always returns "/temp/" when the directory parameter is empty.
Fix: Remove the dead code-source computation and fix the directory resolution logic to use the correct deployment path.

[P2-A08-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java | Line: 25
Description: downloadPDF is declared throws Exception with no attempt to catch or categorize exceptions from HttpDownloadUtility.sendPost. Callers cannot distinguish network errors from I/O errors.
Fix: Replace the broad throws Exception with specific exception types and add appropriate error handling.

[P2-A08-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java | Line: 35
Description: getGPSLocation accepts a raw int uid from the URL path variable with no controller-level check verifying that the authenticated user is permitted to query for the given uid.
Fix: Add authorization checks to verify the authenticated user is permitted to access the requested uid's GPS data.

[P2-A08-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java | Line: 53
Description: Both GPS save methods execute two sequential JDBC operations (UPDATE to clear current_location, then INSERT) with no @Transactional annotation. A failed INSERT leaves the unit with no current GPS record.
Fix: Add @Transactional annotation to both save methods to ensure atomicity.

[P2-A08-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/RestURIConstants.java | Line: 5
Description: Constants ACCEPT_USRS and DECLINE_USRS are marked with an "unused" comment but not removed, creating maintenance risk.
Fix: Remove unused constants after verifying they have no active references.

[P2-A08-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/RestURIConstants.java | Line: 50
Description: Multiple constant values contain typos: GET_SERVICEDTL has "sericedetail" (should be "servicedetail"), RESUME_EQUIPMENT has "frequencey" (should be "frequency"), and DRIVRR_ACCESS has "DRIVRR".
Fix: Correct the typos in both constant names and URL values, updating all references accordingly.

[P2-A08-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/RestURIConstants.java | Line: N/A
Description: RestURIConstants is a utility constants class with no private constructor, allowing unnecessary instantiation.
Fix: Add a private constructor to prevent instantiation of the utility class.

[P2-A08-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java | Line: 32
Description: A Gson instance is created as a class field but only used in a log statement, causing unnecessary serialization work when INFO logging is disabled.
Fix: Use lazy evaluation for the Gson serialization (e.g., check log level before serializing) or remove the unnecessary Gson field.

[P2-A08-13] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java | Line: N/A
Description: The Util class is imported but never called within ReportAPI, indicating a dead import from an incomplete implementation.
Fix: Remove the unused import.

[P2-A09-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: N/A
Description: No test coverage for any of the 5 ResumeController endpoints (getResumeDriver, getResumeEquipment, getReportList, generateReport, sendReportList). These perform multiple raw SQL queries and control report generation and email dispatch.
Fix: Create tests for all five endpoints covering happy paths, empty results, and error conditions.

[P2-A09-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: N/A
Description: Every method in SessionController (9 public endpoints plus 2 private helpers) is entirely untested. These are the core transactional operations of the application (session lifecycle, pre-op result persistence, offline sync).
Fix: Create comprehensive tests for all SessionController methods, prioritizing startSessions, endSessions, saveResults, and saveOffline.

[P2-A09-3] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 342
Description: endSessions catches EmptyResultDataAccessException but always returns HTTP 200 OK with MSGID_SUCCESS. When a session record cannot be found, the unit_service table is never updated and the caller has no indication the operation silently failed.
Fix: Return an error status (e.g., HTTP 404) when the session is not found instead of swallowing the exception and returning success.

[P2-A09-4] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: N/A
Description: RuntimeConfig contains hardcoded plaintext credentials including a Google Cloud Messaging API key, Clickatell SMS password/username/API ID, and an internal AWS EC2 URL. All fields are public static and non-final.
Fix: Externalize all credentials to environment variables or a secrets manager, make fields final, and remove sensitive values from source code.

[P2-A09-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 72
Description: driverAccess silently no-ops when imageno is outside the range 1-4, returning HTTP 200 OK without saving the image or notifying the caller of the invalid input.
Fix: Return HTTP 400 BAD_REQUEST for invalid imageno values and add validation.

[P2-A09-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 163
Description: searchForm contains a broken SQL query with syntax error "where u. l.question_id = question_id = ?" which cannot execute. The keyword parameter is never used in the query. This endpoint is effectively non-functional.
Fix: Rewrite the SQL query with correct syntax and incorporate the keyword parameter.

[P2-A09-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 323
Description: generateReport and sendReportList log the full report API input at INFO level, which includes a hardcoded password ("ciiadmin") in the JSON payload, causing credentials to appear in application logs.
Fix: Remove the password from the logged output or redact sensitive fields before logging.

[P2-A09-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 481
Description: saveOffline catches Exception, logs it, and re-throws it, causing an uncontrolled 500 response instead of a structured error body.
Fix: Return a structured error response (e.g., HTTP 500 with a JSON error body) instead of re-throwing the exception.

[P2-A09-9] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 25
Description: MSGID_CODEE_DUPLICATE_VEHICLE and MSGID_LOGICERRORR share the same string value "3", making it impossible for clients or logging infrastructure to distinguish between a duplicate vehicle error and a logic error.
Fix: Assign unique values to each message ID constant.

[P2-A09-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 58
Description: getResumeDriver uses integer division for percentage calculations (failed*100/total), silently truncating fractional results (e.g., 1/3 becomes "33" not "33.3").
Fix: Use floating-point or BigDecimal arithmetic for percentage calculations and define the desired precision.

[P2-A09-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 246
Description: startSessions has a commented-out concurrent usage check that would detect another driver using the same unit. The removal is undocumented and untested.
Fix: Document the decision to remove the concurrent usage check and add a test confirming the intended behavior.

[P2-A09-12] MEDIUM | File: src/test/java/com/journaldev/spring/jdbc/service/APKUpdaterServiceTest.java | Line: 17
Description: APKUpdaterServiceTest has its only two test methods fully commented out, leaving APKUpdaterService with zero measured test coverage despite scaffolded test infrastructure.
Fix: Uncomment and fix the tests or rewrite them to provide active coverage.

[P2-A09-13] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/RestURIConstants.java | Line: N/A
Description: The RESUME_EQUIPMENT URI constant and method parameter both use the misspelled "frequencey" instead of "frequency", creating a latent API contract defect.
Fix: Correct the spelling in both the URI constant and the method parameter, coordinating with API clients.

[P2-A09-14] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 292
Description: generateReport does not validate that perList is non-empty before processing. If the driver has no permission entries, the method returns HTTP 200 as if the report was generated.
Fix: Return an appropriate error response when perList is empty to indicate no report could be generated.

[P2-A09-15] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 377
Description: sendReportList silently defaults to "Daily" for any frequency value that is not "w" or "m", with no validation error or logging.
Fix: Add input validation for the frequency parameter and return HTTP 400 for invalid values.

[P2-A09-16] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 5
Description: Dead configuration fields (emailContent as empty string, host/port/sfport/sfclass marked as unused) remain in a public mutable class with no guards against accidental use or mutation.
Fix: Remove dead fields or mark them as final and private.

[P2-A09-17] INFO | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 289
Description: The private toString(Serializable) method is only called in the untested EmptyResultDataAccessException catch block of endSessions. Its serialization and Base64 encoding logic has never been exercised.
Fix: Add test coverage for the endSessions error path which exercises this method.

[P2-A10-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/UserController.java | Line: N/A
Description: UserController.getUserByEmail has zero test coverage. This is the sole HTTP endpoint of the class and represents an untested entry point into the application's user-lookup logic.
Fix: Create MockMvc tests for getUserByEmail covering both the happy path (user found) and the not-found path.

[P2-A10-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/UserController.java | Line: 30
Description: The not-found branch returns HttpStatus.BAD_GATEWAY (502) instead of an appropriate status like 404 NOT_FOUND. Clients will misinterpret this as an infrastructure failure rather than a missing resource.
Fix: Replace HttpStatus.BAD_GATEWAY with HttpStatus.NOT_FOUND (404) for the user-not-found response.

[P2-A10-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/UserController.java | Line: 23
Description: getUserByEmail accepts an unconstrained String email with no null-check, blank-check, or format validation. No Bean Validation annotation is applied.
Fix: Add @NotBlank and @Email validation annotations to the email parameter and add @Valid processing.

[P2-A10-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/UserController.java | Line: 25
Description: If userDao.findByName(email) throws a DataAccessException, it propagates unhandled, resulting in a 500 Internal Server Error with a stack trace.
Fix: Add try/catch for DataAccessException and return an appropriate error response, or add a global @ExceptionHandler.

[P2-A10-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/APIConnections.java | Line: N/A
Description: APIConnections has zero test coverage and is not referenced by any other production class, making it dead or orphaned code.
Fix: Remove APIConnections if confirmed unused, or add tests if it is needed for future functionality.

[P2-A10-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Answers.java | Line: N/A
Description: Answers has zero test coverage. While imported by SessionController, no test exercises the SessionController path that uses Answers objects.
Fix: Add tests for Answers as part of SessionController test coverage.

[P2-A10-7] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/APIConnections.java | Line: N/A
Description: APIConnections implements Serializable but defines no equals(), hashCode(), or toString() override, causing object identity semantics when used in collections.
Fix: Add equals(), hashCode(), and toString() implementations based on the ID field.

[P2-A10-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Answers.java | Line: N/A
Description: Answers implements Serializable but provides no equals(), hashCode(), or toString(). The answer field can be null after default construction with no downstream null handling.
Fix: Add equals(), hashCode(), and toString() implementations and document null-handling expectations.

[P2-A10-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/APIConnections.java | Line: N/A
Description: APIConnections is never imported or instantiated outside its own source file. It appears to be dead code with no production consumers.
Fix: Remove the class if confirmed unused.

[P2-A10-10] INFO | File: src/test/java/com/journaldev/spring/jdbc/service/APKUpdaterServiceTest.java | Line: N/A
Description: APKUpdaterServiceTest contains two meaningful tests that were commented out, leaving APKUpdaterService with zero test coverage.
Fix: Uncomment and fix the test methods or rewrite them to restore test coverage.
[P2-A11-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationRequest.java | Line: N/A
Description: AuthenticationRequest has zero test coverage; no unit tests exist for construction, accessors, equals, hashCode, toString, or serialization.
Fix: Create a dedicated unit test class covering builder construction, no-arg constructor with setters, equals/hashCode contract, and serialization round-trip.

[P2-A11-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationResponse.java | Line: N/A
Description: AuthenticationResponse has zero test coverage; no tests verify field access, JSON serialization with @JsonInclude(NON_NULL), or the @EqualsAndHashCode(callSuper=true) contract.
Fix: Create a unit test class covering no-arg construction, JSON round-trip with null field suppression, equals/hashCode with superclass fields, and serialization.

[P2-A11-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Charts.java | Line: N/A
Description: Charts has zero test coverage; the hand-written addUsageList mutating method and BeanPropertyRowMapper compatibility are completely untested.
Fix: Create a unit test class covering addUsageList, setUsageList(null) followed by addUsageList, default state, and BeanPropertyRowMapper column mapping.

[P2-A11-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Charts.java | Line: 41
Description: Calling setUsageList(null) then addUsageList() causes an unguarded NullPointerException because no null check exists on the list field.
Fix: Add a null guard in setUsageList to reject null or reinitialize to an empty list, and add a test for this error path.

[P2-A11-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationRequest.java | Line: 18
Description: The password field is included in Lombok @Data-generated toString() output, exposing plaintext credentials in logs.
Fix: Add @ToString.Exclude on the password field to prevent credential leakage in toString output.

[P2-A11-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationResponse.java | Line: 18
Description: The accessToken and sessionToken fields are included in Lombok @Data-generated toString() output, exposing security tokens in logs.
Fix: Add @ToString.Exclude on both accessToken and sessionToken fields.

[P2-A11-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationRequest.java | Line: 22
Description: @Builder is placed on a private constructor alongside @NoArgsConstructor and @Data, creating two inconsistent and untested construction paths.
Fix: Add tests verifying that builder-constructed and setter-constructed objects are equivalent via equals(), or consolidate to a single construction path.

[P2-A11-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Charts.java | Line: 43
Description: The field unit_id uses snake_case with getter getUnit_id(), violating JavaBean conventions and potentially breaking BeanPropertyRowMapper column mapping.
Fix: Rename the field to unitId with getter getUnitId(), or add a test confirming BeanPropertyRowMapper maps the column correctly with the current naming.

[P2-A11-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Charts.java | Line: 40
Description: The method addUsageList(Usage) is misleadingly named; it adds a single Usage item, not a list.
Fix: Rename the method to addUsage(Usage) to accurately describe its behavior.

[P2-A11-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationResponse.java | Line: 20
Description: The date/time fields expiresIn, actualDate, and expirationDate are typed as String with no format validation or temporal type.
Fix: Change these fields to a temporal type such as Instant or LocalDateTime, or add @JsonFormat and validation annotations.

[P2-A11-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Charts.java | Line: N/A
Description: Charts has no equals(), hashCode(), or toString() methods, making it unusable in sets, as map keys, or in value-based assertions.
Fix: Add Lombok @Data annotation or implement equals(), hashCode(), and toString() manually.

[P2-A12-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/Company.java | Line: N/A
Description: Company, Driver, and DriverEmails all have zero test coverage; no unit, integration, or indirect tests exist for any of these model classes carrying credentials and PII.
Fix: Create dedicated test classes for each model covering construction, accessors, equals/hashCode, and serialization.

[P2-A12-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Company.java | Line: 44
Description: The builder constructor's contactDriver != null branch silently overwrites name, email, and password fields from the Driver object, and this logic is completely untested.
Fix: Add tests covering both the contactDriver non-null path (field override) and the null path (explicit values retained).

[P2-A12-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Company.java | Line: 46
Description: String concatenation of contactDriver.getFirst_name() and getLast_name() produces literal "null" strings when either name is null, with no validation or test.
Fix: Add null guards before concatenation and add tests for null first_name and last_name scenarios.

[P2-A12-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 23
Description: The equals/hashCode contract is restricted to the email field only via @EqualsAndHashCode(onlyExplicitlyIncluded=true), meaning drivers with different IDs but the same email are considered equal, and this is untested.
Fix: Add tests verifying same-email equality, different-email inequality, null-email behavior, and correct Set/Map behavior.

[P2-A12-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/DriverEmails.java | Line: N/A
Description: DriverEmails is a hand-written POJO with no equals(), hashCode(), or toString() and no tests, making value-based comparison and collection operations incorrect.
Fix: Add Lombok @Data or implement equals/hashCode/toString manually, and create unit tests.

[P2-A12-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Company.java | Line: 33
Description: The builder accepts a null password without validation; when contactDriver is non-null, contactDriver.getPassword() (which may also be null) silently replaces the password field.
Fix: Add null validation for password in the builder constructor and add tests for null password scenarios.

[P2-A12-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 41
Description: The self-referential drivers list field has no tested semantics; it is absent from the builder and can only be set via setDrivers(), with no tested interaction with the contactperson flag.
Fix: Add tests verifying default null state after builder construction and behavior when contactperson is true vs false with varying drivers list states.

[P2-A12-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/DriverEmails.java | Line: N/A
Description: DriverEmails implements Serializable with an explicit serialVersionUID but has no serialization round-trip test to verify faithful reconstruction.
Fix: Add a serialization round-trip test covering all four nullable email address fields.

[P2-A12-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Company.java | Line: N/A
Description: Both Company and Driver implement Serializable with Lombok-generated code, but no test verifies serialization/deserialization round-trips for either class.
Fix: Add serialization round-trip tests for both Company and Driver.

[P2-A12-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Company.java | Line: 33
Description: The @Singular annotation on arrRoles builder parameter creates an immutable list, but no test verifies empty-list default, role accumulation, or immutability post-construction.
Fix: Add tests confirming empty roles list when none added, correct getter access, and UnsupportedOperationException on mutation.

[P2-A12-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 65
Description: The @Singular annotation on arrDriverTrainings builder parameter produces an immutable list, but the empty-list default and immutability are untested.
Fix: Add tests for empty-list default and post-construction immutability of the training list.

[P2-A12-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 32
Description: Primitive boolean fields contactperson and driver_based default to false via the no-arg constructor, and post-construction default state is untested.
Fix: Add a test verifying all field defaults after no-arg construction.

[P2-A12-13] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/DriverEmails.java | Line: N/A
Description: DriverEmails is a hand-written POJO inconsistent with the Lombok pattern used by Company and Driver, increasing the risk of missing methods and copy-paste errors.
Fix: Consider migrating DriverEmails to use Lombok @Data for consistency, or add thorough tests to guard against regressions.

[P2-A13-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/DriverEquipment.java | Line: N/A
Description: DriverEquipment has zero test coverage; no test verifies field-to-column binding via BeanPropertyRowMapper, no-arg constructor, or getter/setter correctness.
Fix: Create a unit test class covering reflective instantiation, field binding for hours and trained columns, and accessor round-trips.

[P2-A13-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java | Line: N/A
Description: DriverTraining has zero test coverage; no test verifies field name matching for BeanPropertyRowMapper, no-arg constructor, or builder construction.
Fix: Create a unit test class covering no-arg construction, builder construction, and field name alignment with database columns.

[P2-A13-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/EmailLayout.java | Line: N/A
Description: EmailLayout has zero test coverage and its only DAO method (getEmailLayoutByType) is an unimplemented stub that returns an empty object.
Fix: Create a unit test for EmailLayout and fix or remove the stub DAO method.

[P2-A13-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/EmailLayoutDAO.java | Line: 21
Description: getEmailLayoutByType() is an unimplemented stub that returns an empty EmailLayout without executing any SQL or using the type parameter, causing silent data loss.
Fix: Implement the method with proper SQL query execution, or remove it and its callers if no longer needed.

[P2-A13-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/DriverEquipment.java | Line: 9
Description: @EqualsAndHashCode(callSuper=false) silently excludes all 18 inherited Equipment fields from equality comparison, so two objects with different Equipment data but same hours and trained values are considered equal.
Fix: Change to @EqualsAndHashCode(callSuper=true) to include parent Equipment fields in equality, and add tests.

[P2-A13-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/DriverEquipment.java | Line: 13
Description: The hours (Integer) and trained (Boolean) fields are nullable boxed types; callers auto-unboxing a null getTrained() will get a NullPointerException.
Fix: Add null checks before unboxing in callers, or document the nullability contract and add tests for null field behavior.

[P2-A13-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java | Line: 23
Description: Date fields training_date and expiration_date are declared as String with no format validation; the unused java.util.Date import suggests an abandoned refactoring.
Fix: Change to a temporal type like LocalDate, or add format validation annotations and tests for invalid date strings.

[P2-A13-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java | Line: 27
Description: The @Builder constructor is private and the builder is the only non-default construction path, but BeanPropertyRowMapper uses the no-arg constructor and setters, making the builder dead code in production.
Fix: Remove the unused builder or add tests verifying builder construction if it is intended to be used.

[P2-A13-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/EmailLayout.java | Line: N/A
Description: EmailLayout has no equals(), hashCode(), or toString() implementations; it inherits Object defaults, making value comparison and logging uninformative.
Fix: Add Lombok @Data annotation or implement equals/hashCode/toString manually.

[P2-A13-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java | Line: 6
Description: Unused import of com.journaldev.spring.jdbc.model.Roles.RolesBuilder introduces an unnecessary coupling dependency.
Fix: Remove the unused import.

[P2-A13-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java | Line: 4
Description: Unused import of java.util.Date, a leftover from an incomplete refactoring where date fields were likely intended to be typed as Date.
Fix: Remove the unused import.

[P2-A13-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java | Line: 14
Description: Inline Javadoc comment is misplaced on the class declaration line, potentially causing IDE and documentation tool misinterpretation.
Fix: Move the Javadoc block to a separate line before the class declaration.

[P2-A13-13] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/DriverEquipment.java | Line: N/A
Description: All three model classes are populated via BeanPropertyRowMapper at runtime, but no integration tests with an in-memory database exist to validate field-to-column name mappings.
Fix: Add Spring integration tests using an in-memory database (e.g., H2) to verify BeanPropertyRowMapper column binding for all three classes.

[P2-A14-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/Equipment.java | Line: N/A
Description: Equipment has zero test coverage despite being central to the application; all 18 Lombok-generated getter/setter pairs, builder, equals/hashCode/toString, and BeanPropertyRowMapper bindings are untested.
Fix: Create a comprehensive unit test covering builder construction, field defaults, BeanPropertyRowMapper compatibility, and equals/hashCode/toString.

[P2-A14-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/EquipmentType.java | Line: N/A
Description: EquipmentType has zero test coverage and is not referenced anywhere in the production codebase outside its own file, indicating it may be dead code.
Fix: Determine if EquipmentType is needed; if so, wire it into the application and add tests. If not, remove it.

[P2-A14-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/ErrorMessage.java | Line: N/A
Description: ErrorMessage has zero test coverage despite being the primary error-reporting vehicle returned inside ResponseWrapper.errors to API consumers.
Fix: Create unit tests covering construction, field access, equals/hashCode/toString, and null-field behavior.

[P2-A14-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Equipment.java | Line: 34
Description: The @Builder constructor accepts 18 parameters but no test validates that all fields are correctly assigned or that builder output matches BeanPropertyRowMapper output.
Fix: Add tests asserting all 18 fields are correctly set via builder and that the builder-constructed object matches a BeanPropertyRowMapper-constructed one.

[P2-A14-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/EquipmentType.java | Line: N/A
Description: EquipmentType appears to be dead code with no production wiring; no DAO, controller, service, or mapper uses it.
Fix: Confirm whether EquipmentType is needed. If dead code, remove it. If needed, implement the missing DAO/service layer and add tests.

[P2-A14-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Equipment.java | Line: 27
Description: mac_address is used as the primary lookup key in EquipmentDAOImpl but has no null-safety tests; a null value will produce a SQL error rather than a controlled application error.
Fix: Add null validation for mac_address in the DAO lookup methods and add tests for null and empty mac_address values.

[P2-A14-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Equipment.java | Line: 29
Description: impact_threshold is a long with no boundary tests; the combination of alert_enabled=true with impact_threshold=0 could trigger alerts on every event.
Fix: Add validation for impact_threshold range and add tests for boundary values including 0, negative, and Long.MAX_VALUE.

[P2-A14-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/ErrorMessage.java | Line: N/A
Description: ErrorMessage has no validation or constraint annotations on its three nullable String fields; fully null ErrorMessage objects may result in incomplete error responses to API clients.
Fix: Add @NotNull or @NotBlank annotations on required fields (at minimum message), and add tests for null-field combinations.

[P2-A14-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/EquipmentType.java | Line: N/A
Description: EquipmentType is missing @Data or equivalent Lombok annotation, so it has no equals/hashCode override and falls back to Object identity comparison.
Fix: Add Lombok @Data or implement equals/hashCode manually if the class is retained.

[P2-A14-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Equipment.java | Line: 16
Description: Snake_case field names (type_id, comp_id, manu_id, etc.) deviate from Java conventions and are untested for JSON and BeanPropertyRowMapper serialization.
Fix: Add serialization round-trip tests verifying that snake_case fields map correctly through Jackson and BeanPropertyRowMapper.

[P2-A14-11] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/Equipment.java | Line: N/A
Description: All three model classes implement Serializable with explicit serialVersionUID but none have serialization round-trip tests.
Fix: Add serialization/deserialization round-trip tests for Equipment, EquipmentType, and ErrorMessage.

[P2-A15-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java | Line: N/A
Description: FormDtl has zero test coverage; all 14 methods (7 getters, 7 setters) and the BeanPropertyRowMapper binding in two production endpoints are completely untested.
Fix: Create a unit test class covering all getter/setter round-trips, default field values, and BeanPropertyRowMapper compatibility.

[P2-A15-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/FuelType.java | Line: N/A
Description: FuelType has zero test coverage; all 4 methods are untested and the BeanPropertyRowMapper binding for the REST endpoint is unverified.
Fix: Create a unit test class covering getter/setter round-trips and BeanPropertyRowMapper compatibility.

[P2-A15-3] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/GCMData.java | Line: N/A
Description: GCMData has zero test coverage; neither GCMData nor its subclass GCMDataPermission appears in any test file.
Fix: Create unit tests for GCMData covering the to field getter/setter and serialization behavior through the subclass.

[P2-A15-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java | Line: N/A
Description: FormDtl is missing equals(), hashCode(), and toString() overrides; value-based equality comparisons fall back to identity comparison producing incorrect results.
Fix: Add Lombok @Data or implement equals/hashCode/toString manually.

[P2-A15-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/FuelType.java | Line: N/A
Description: FuelType is missing equals(), hashCode(), and toString() overrides; tests or callers comparing FuelType objects by value will silently use identity comparison.
Fix: Add Lombok @Data or implement equals/hashCode/toString manually.

[P2-A15-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/GCMData.java | Line: N/A
Description: GCMData does not implement Serializable while its subclass GCMDataPermission does; the inherited to field will silently be null after a serialize/deserialize round-trip.
Fix: Add implements Serializable to GCMData, or add a serialization test that documents the expected loss of the to field.

[P2-A15-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java | Line: 11
Description: Primitive int fields id and input_order will throw NullPointerException when BeanPropertyRowMapper maps a database NULL value due to unboxing failure.
Fix: Change id and input_order to Integer (boxed type) to safely handle database NULLs, and add tests for NULL column mapping.

[P2-A15-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/FuelType.java | Line: 12
Description: The primitive int field id will throw NullPointerException when BeanPropertyRowMapper maps a database NULL value due to unboxing failure.
Fix: Change id to Integer (boxed type) or ensure the database column is NOT NULL, and add a test for this mapping.

[P2-A15-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java | Line: N/A
Description: No constructor other than the implicit default is provided; no test verifies that all fields default to expected zero/null values relied upon by BeanPropertyRowMapper.
Fix: Add a test verifying default field values after default construction.

[P2-A15-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GCMData.java | Line: 5
Description: The to field is declared protected rather than private, exposing it directly to subclasses and same-package classes without going through accessors.
Fix: Change the to field visibility to private to enforce encapsulation through accessor methods.

[P2-A15-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GCMData.java | Line: 11
Description: No validation is performed in setTo(); a null or empty GCM registration token will cause the push notification API call to fail at runtime.
Fix: Add null/blank validation in setTo() and add tests for null and empty string inputs.

[P2-A15-12] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java | Line: 10
Description: The serialVersionUID appears to be auto-generated; no serialization round-trip test exists to catch deserialization failures after field changes.
Fix: Add a serialization round-trip test for FormDtl.

[P2-A15-13] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/FuelType.java | Line: 10
Description: The serialVersionUID appears to be auto-generated; no serialization round-trip test exists to catch deserialization failures after field changes.
Fix: Add a serialization round-trip test for FuelType.

[P2-A15-14] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java | Line: N/A
Description: Fields and methods use snake_case naming (e.g., input_type, getInput_type) rather than Java standard camelCase, which may cause issues with frameworks expecting standard JavaBean naming.
Fix: Rename fields to camelCase or add a test verifying JSON serialization produces the expected key names.

[P2-A15-15] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java | Line: N/A
Description: The overall test suite is critically sparse with only 3 test files (2 effective) for the entire application; model classes have 0% coverage.
Fix: Establish a testing strategy and create unit tests for all model classes as a baseline.

[P2-A16-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/GCMDataPermission.java | Line: N/A
Description: GCMDataPermission has zero test coverage; no test verifies getData/setData round-trip, inherited to field access, or Serializable correctness.
Fix: Create a unit test class covering data field accessors, inherited to field, and serialization round-trip.

[P2-A16-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/GCMEntity.java | Line: N/A
Description: GCMEntity has zero test coverage; no test verifies getMsg_type/setMsg_type behavior.
Fix: Create a unit test class covering msg_type getter/setter and default state.

[P2-A16-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/GCMResponse.java | Line: N/A
Description: GCMResponse has zero test coverage; none of the ten methods across five fields are tested.
Fix: Create a unit test class covering all getter/setter pairs and results list handling.

[P2-A16-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/GCMDataPermission.java | Line: N/A
Description: All three GCM classes (GCMDataPermission, GCMEntity, GCMResponse) are dead code with no production usages found anywhere in the codebase.
Fix: Remove all three dead GCM model classes and related RuntimeConfig GCM constants, or document why they are retained.

[P2-A16-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GCMResponse.java | Line: 12
Description: The success, failure, and canonical_ids fields are typed as String despite representing numeric counts in the GCM/FCM API, causing silent type unsafety.
Fix: Change these fields to int or long to match the GCM/FCM API response format, and add tests for deserialization.

[P2-A16-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GCMEntity.java | Line: N/A
Description: GCMEntity does not implement Serializable unlike sibling GCM classes; if ever serialized, a NotSerializableException would be thrown at runtime.
Fix: Add implements Serializable to GCMEntity for consistency, or remove the class if it is dead code.

[P2-A16-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GCMDataPermission.java | Line: 18
Description: setData(null) is never tested; a null Permissions data field could produce a malformed push notification message silently.
Fix: Add a null guard in setData or add tests for null data handling.

[P2-A16-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GCMResponse.java | Line: 41
Description: getResults() returns a List with no null check; callers iterating without null-guarding will throw NullPointerException when results is null.
Fix: Initialize the results field to an empty list or add a null guard in the getter, and add tests for null and empty results.

[P2-A16-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GCMEntity.java | Line: 8
Description: The msg_type field and its accessors use non-standard snake_case naming, violating Java naming conventions and potentially breaking standard JavaBean tooling.
Fix: Rename to msgType with getters getMsgType/setMsgType, or add Jackson @JsonProperty annotation for explicit mapping.

[P2-A16-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GCMDataPermission.java | Line: N/A
Description: None of the three GCM classes override equals(), hashCode(), or toString(), making logging uninformative and collection operations incorrect.
Fix: Add Lombok @Data or implement equals/hashCode/toString manually on all three classes.

[P2-A16-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GCMDataPermission.java | Line: 10
Description: The serialVersionUID values in GCMDataPermission and GCMResponse appear auto-generated with no deserialization regression tests.
Fix: Add serialization round-trip tests or remove Serializable if the classes are dead code.

[P2-A16-12] INFO | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 13
Description: RuntimeConfig contains a hardcoded legacy GCM endpoint URL (gcm-http.googleapis.com) which was shut down by Google in June 2024; the dead GCM model classes are consistent with this decommissioned endpoint.
Fix: Remove the legacy GCM endpoint constant and the associated dead model classes, or migrate to the FCM HTTP v1 API.

[P2-A17-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/GPS.java | Line: N/A
Description: GPS, GPSList, and Impact all have zero unit test coverage; no test file references or instantiates any of these classes.
Fix: Create dedicated unit test classes for GPS, GPSList, and Impact covering all accessors, constructors, and edge cases.

[P2-A17-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/GPS.java | Line: 14
Description: GPS longitude and latitude are boxed Float (nullable); LocationController auto-unboxes them in a != 0 comparison, causing NullPointerException if either field is null.
Fix: Add null checks before comparing longitude and latitude in LocationController, and add tests for null coordinate handling.

[P2-A17-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Impact.java | Line: 21
Description: The private @Builder constructor coexists with a public @NoArgsConstructor; no-arg construction yields impact_time=null which propagates to DateUtil.parseDateTimeIso(null) and silently inserts null into the database.
Fix: Add validation for impact_time in ImpactDAO.save() and add tests for default-constructed Impact objects.

[P2-A17-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Impact.java | Line: N/A
Description: ImpactDAO.save() silently discards impacts with impact_value below 80000 without logging or notifying the caller, while the controller always reports success.
Fix: Add logging for discarded impacts and return a distinct response code, and add tests for the threshold boundary.

[P2-A17-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/GPSList.java | Line: 20
Description: setGpsList(null) nullifies the internal list; subsequent getGpsList().forEach() in LocationController causes NullPointerException with no null guard.
Fix: Add a null guard in setGpsList to reject null or reinitialize to an empty list, and add tests for null list handling.

[P2-A17-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GPS.java | Line: N/A
Description: GPS has no equals(), hashCode(), or toString() overrides; two GPS instances with identical fields are not considered equal and logging produces uninformative output.
Fix: Add Lombok @Data or implement equals/hashCode/toString manually.

[P2-A17-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GPSList.java | Line: N/A
Description: GPSList has no equals(), hashCode(), or toString() overrides; inherits reference equality from Object.
Fix: Add Lombok @Data or implement equals/hashCode/toString manually.

[P2-A17-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Impact.java | Line: 16
Description: Negative impact_value passes the 80000 threshold check (since -1 < 80000 is true) and would be silently written to the database as a semantically invalid value.
Fix: Add range validation rejecting negative impact_value in ImpactDAO.save() and add boundary tests.

[P2-A17-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GPS.java | Line: 16
Description: gps_time is an unvalidated raw String; DateUtil.parseDateTimeIso() throws IllegalArgumentException for unparseable input, which propagates as an unhandled 500 error from saveGPSLocations.
Fix: Add try-catch for date parsing in LocationController.saveGPSLocations and add tests for invalid timestamp strings.

[P2-A17-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Impact.java | Line: 18
Description: mac_address is not validated for format or nullity; downstream DAO queries use it directly as a JDBC parameter, risking incorrect SQL matches or misleading error messages.
Fix: Add @NotNull and format validation for mac_address, and add tests for null and malformed MAC address handling.

[P2-A17-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GPS.java | Line: N/A
Description: LocationController is marked "Not in Use" in a comment but remains @Controller-annotated with three live HTTP endpoints that bind GPS and GPSList models.
Fix: Either remove the controller and its endpoints if truly unused, or remove the misleading comment and add tests.

[P2-A17-12] LOW | File: src/test/java/com/journaldev/spring/jdbc/service/APKUpdaterServiceTest.java | Line: N/A
Description: APKUpdaterServiceTest has all test methods commented out, making it a dead test class with zero effective coverage.
Fix: Uncomment and fix the tests, or remove the dead test class.

[P2-A18-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java | Line: N/A
Description: ImpactList, ImpactNotification, and Incidents all have zero test coverage; no direct or indirect tests exist for any of these model classes used in impact event processing and incident reporting.
Fix: Create dedicated unit test classes for each model covering construction, accessors, and edge cases.

[P2-A18-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java | Line: 23
Description: setImpactList(null) is not guarded; calling getImpactList().forEach() in ImpactController after setting null throws NullPointerException at runtime.
Fix: Add a null guard in setImpactList to reject null or reinitialize to an empty list, and add tests for null and empty list scenarios.

[P2-A18-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactNotification.java | Line: N/A
Description: ImpactNotification uses @Builder and @NoArgsConstructor alongside BeanPropertyRowMapper with snake_case field names; a column name mismatch would silently produce objects with null fields causing blank notifications.
Fix: Add tests verifying no-arg construction with setters, builder construction, and that field names match SQL column aliases.

[P2-A18-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Incidents.java | Line: N/A
Description: Incidents has no explicit constructor and no Lombok; default-constructed objects have all fields at zero/null defaults with no test verifying safe initial state or JSON deserialization round-trip.
Fix: Add tests verifying default construction state and JSON deserialization for the saveIncident endpoint.

[P2-A18-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Incidents.java | Line: 18
Description: Three Boolean fields (injury, near_miss, incident) are boxed and can be null; if JSON omits them, auto-unboxing by downstream code throws NullPointerException.
Fix: Add null checks in any code that auto-unboxes these fields, or use primitive boolean with default false, and add tests for null Boolean handling.

[P2-A18-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Incidents.java | Line: 13
Description: The byte[] fields signature and image have no size constraints; they accept data from HTTP request bodies with no protection against very large payloads.
Fix: Add size validation at the controller or model layer, and add tests for null, empty, and oversized byte arrays.

[P2-A18-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java | Line: 13
Description: ImpactList and Incidents implement Serializable with explicit serialVersionUID but have no serialization round-trip tests.
Fix: Add serialization round-trip tests for both ImpactList and Incidents.

[P2-A18-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Incidents.java | Line: N/A
Description: Incidents has no equals(), hashCode(), or toString(); deduplication and logging are unreliable with Object identity semantics.
Fix: Add Lombok @Data or implement equals/hashCode/toString manually.

[P2-A18-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactNotification.java | Line: N/A
Description: ImpactNotification does not implement Serializable, inconsistent with other model classes in the same package; serialization would fail at runtime with NotSerializableException.
Fix: Add implements Serializable to ImpactNotification for consistency.

[P2-A18-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Incidents.java | Line: 43
Description: Fields description, report_time, event_time, and job_number are declared mid-class after getter/setter methods for other fields, indicating organic growth without refactoring.
Fix: Reorganize the class to declare all fields together at the top, followed by all methods.

[P2-A19-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/Manufacturer.java | Line: N/A
Description: Manufacturer has zero test coverage; all four accessor methods and the serialization contract are completely unverified.
Fix: Create a unit test class covering getter/setter round-trips, default construction state, and serialization.

[P2-A19-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/OfflineSessions.java | Line: N/A
Description: OfflineSessions has zero test coverage; the correct assembly and retrieval of composed Sessions and Result objects is never verified.
Fix: Create a unit test class covering getter/setter round-trips and null-assignment edge cases.

[P2-A19-3] HIGH | File: src/test/java/com/journaldev/spring/jdbc/service/APKUpdaterServiceTest.java | Line: 17
Description: APKUpdaterServiceTest is entirely commented out; the intended indirect coverage of PackageEntry builder, initVersion, URL formatting, and field getters is dead.
Fix: Uncomment and fix the APKUpdaterServiceTest tests, or create replacement tests for PackageEntry builder construction.

[P2-A19-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java | Line: 39
Description: PackageEntry.initVersion has no test for the non-matching branch; version strings without a hyphen silently leave major, minor, patch, and env at defaults.
Fix: Add tests for version strings without a hyphen, empty strings, and strings with a hyphen but missing numeric segments.

[P2-A19-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java | Line: 57
Description: PackageEntry.compareTo equality case (returning 0 for identical versions) is not tested; the Comparable contract for equality is unverified.
Fix: Add a test verifying that compareTo returns 0 for two PackageEntry instances with identical version components.

[P2-A19-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java | Line: 58
Description: The compareTo null-argument branch (returns 1 when o is null) exists but is not tested.
Fix: Add a test calling compareTo(null) and asserting the result is greater than 0.

[P2-A19-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java | Line: 29
Description: Builder constructor fields fileName, name, and url are never asserted in any active test; the URL format string is entirely unverified.
Fix: Add tests for getFileName(), getName(), and getUrl() with varying baseUrl, name, and version combinations.

[P2-A19-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java | Line: 42
Description: The initVersion partial-group branches for blank minor, patch, and env segments are not tested; only fully-populated version strings are exercised.
Fix: Add tests with version strings that have missing minor, patch, or env segments.

[P2-A19-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java | Line: 13
Description: Lombok-generated equals, hashCode, and toString methods are not tested; the @JsonIgnore exclusion of the pattern field from equality is an untested behavioral contract.
Fix: Add tests for equals/hashCode behavior including verifying that the pattern field is excluded.

[P2-A19-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Manufacturer.java | Line: 10
Description: Both Manufacturer and OfflineSessions declare explicit serialVersionUID values but have no serialization round-trip tests.
Fix: Add serialization round-trip tests for both classes.

[P2-A20-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/Permissions.java | Line: N/A
Description: Permissions, Questions, and ReportLists all have zero test coverage; none of the three test files reference or exercise these classes despite their central role in REST APIs and database mapping.
Fix: Create dedicated unit test classes for each model covering construction, accessors, equality, and serialization.

[P2-A20-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Permissions.java | Line: N/A
Description: Permissions equals() silently excludes security-relevant fields (id, driver_name, enabled, gsm_token) due to @EqualsAndHashCode(onlyExplicitlyIncluded=true); two objects differing in enabled status are considered equal.
Fix: Add tests verifying the contracted equality behavior, and consider whether enabled should be included in the equality check.

[P2-A20-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Permissions.java | Line: N/A
Description: BeanPropertyRowMapper is used against Permissions with Lombok-generated snake_case setters, but no test verifies that column mapping succeeds or handles null database values.
Fix: Add integration or unit tests verifying BeanPropertyRowMapper correctly maps comp_id and other columns to Permissions fields.

[P2-A20-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Questions.java | Line: N/A
Description: Questions and ReportLists have no equals(), hashCode(), or toString() methods; both use Object identity for equality which is incorrect for value-carrying DTOs.
Fix: Add Lombok @Data or implement equals/hashCode/toString manually on both classes.

[P2-A20-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java | Line: 13
Description: The id field is defined in ReportLists but the SQL queries selecting into it omit id, so getId() always returns 0 (the int default); no test verifies this omission.
Fix: Either add id to the SQL SELECT columns or remove the field if it is not needed, and add a test documenting the intended behavior.

[P2-A20-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Questions.java | Line: 12
Description: Questions.id is a primitive int; BeanPropertyRowMapper silently sets it to 0 for SQL NULL, and SessionController passes this zero directly as a query parameter causing incorrect lookups.
Fix: Change id to Integer (boxed type) or add validation to reject zero/null id values before use in queries.

[P2-A20-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Permissions.java | Line: 31
Description: The private builder constructor is the only non-default construction path and is entirely untested; no test verifies correct assignment of all six fields or that omitted fields default to null.
Fix: Add tests verifying builder construction with all fields, partial fields, and that defaults are correct.

[P2-A20-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Permissions.java | Line: 27
Description: The enabled field is typed as String rather than boolean; no validation or enumeration restricts it to valid values like "Y"/"N", and null handling is untested.
Fix: Change enabled to boolean or add validation constraining valid values, and add tests for null and unexpected string values.

[P2-A20-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Questions.java | Line: 14
Description: Questions.expectedanswer and ReportLists.frequency are unvalidated strings; null values could cause NullPointerException in SessionController answer evaluation and ResumeController report dispatch.
Fix: Add null guards in consuming code and add tests for null/empty field values.

[P2-A20-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Permissions.java | Line: 15
Description: All three classes declare explicit serialVersionUID values but have no serialization round-trip tests to catch deserialization breakage.
Fix: Add serialization round-trip tests for Permissions, Questions, and ReportLists.

[P2-A20-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java | Line: N/A
Description: The class name ReportLists is plural but each instance represents a single report subscription record, making List<ReportLists> read as "list of report-lists" which is misleading.
Fix: Rename the class to ReportSubscription or ReportListEntry to accurately represent a single record.

[P2-A21-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Reports.java | Line: N/A
Description: Reports has zero test coverage; all six public methods are untested and field-level behavior (null acceptance, empty string handling) is completely unverified.
Fix: Create a unit test class covering all getter/setter round-trips and null/empty string behavior.

[P2-A21-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Result.java | Line: N/A
Description: Result has zero test coverage; all twelve public methods are untested despite being the direct @RequestBody deserialization target for inbound JSON from mobile clients.
Fix: Create a unit test class covering all getter/setter round-trips, default arrAnswers initialization, and JSON deserialization.

[P2-A21-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/ResponseWrapper.java | Line: N/A
Description: ResponseWrapper has zero test coverage despite being the base API envelope type; Lombok-generated equals/hashCode/toString and Jackson @JsonInclude(NON_NULL) behavior are unverified.
Fix: Create a unit test class covering field accessors, JSON serialization with null field suppression, and equals/hashCode/toString.

[P2-A21-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Result.java | Line: 13
Description: Primitive int fields id and session_id silently default to 0 when missing from JSON; zero is indistinguishable from unset and produces invalid foreign-key references.
Fix: Change to Integer (boxed type) or add validation rejecting zero/null values, and add tests for missing JSON fields.

[P2-A21-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Result.java | Line: 15
Description: start_time and finish_time are untyped String fields with no format validation; arbitrary strings accepted through @RequestBody could propagate to SQL queries causing runtime errors.
Fix: Change to a temporal type or add format validation, and add tests for invalid, null, and empty timestamp strings.

[P2-A21-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Reports.java | Line: N/A
Description: Reports has no equals, hashCode, or toString overrides; two Reports instances with identical field values are not equal, which is incorrect for a DTO.
Fix: Add Lombok @Data or implement equals/hashCode/toString manually.

[P2-A21-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Result.java | Line: N/A
Description: Result has no equals, hashCode, or toString overrides; reference-based equality could produce silent bugs when comparing or deduplicating Result objects.
Fix: Add Lombok @Data or implement equals/hashCode/toString manually.

[P2-A21-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/ResponseWrapper.java | Line: 18
Description: The data and metadata fields are typed as raw Object with no type safety; any type can be assigned and Jackson serialization behavior for polymorphic types is untested.
Fix: Consider using generics (ResponseWrapper<T>) for type safety, and add tests verifying JSON serialization for different concrete types.

[P2-A21-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/ResponseWrapper.java | Line: N/A
Description: AuthenticationResponse uses @EqualsAndHashCode(callSuper=true) calling ResponseWrapper's Lombok-generated equals, but no test verifies the inherited equality chain including data, metadata, and errors fields.
Fix: Add tests verifying equals/hashCode behavior across the ResponseWrapper-AuthenticationResponse hierarchy.

[P2-A21-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Reports.java | Line: 13
Description: The field named object is a String but its name shadows java.lang.Object conceptually; its intended meaning (unit name, equipment identifier) is undocumented.
Fix: Rename the field to a more descriptive name (e.g., objectName or entityName), and add tests for null and special character content.

[P2-A21-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Result.java | Line: 18
Description: The arrAnswers field exposes the concrete ArrayList type instead of the List interface in both field declaration and getter/setter signatures, constraining future refactoring.
Fix: Change the field type and accessor signatures to List<Answers> instead of ArrayList<Answers>.

[P2-A21-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Reports.java | Line: N/A
Description: All three classes implement Serializable with explicit serialVersionUID but have no round-trip serialization tests to catch deserialization failures after field changes.
Fix: Add serialization/deserialization round-trip tests for Reports, ResponseWrapper, and Result.
[P2-A22-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/Results.java, src/main/java/com/journaldev/spring/jdbc/model/Roles.java, src/main/java/com/journaldev/spring/jdbc/model/Services.java | Line: N/A
Description: Results, Roles, and Services model classes have zero test coverage. No test file references any of these classes by import, instantiation, or usage, despite being actively used in production controller paths.
Fix: Create unit tests for all three model classes covering construction, getter/setter round-trips, and serialization behavior.

[P2-A22-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/Roles.java | Line: 44
Description: Roles.RoleId.fromId(String) throws IllegalArgumentException on no match, but both the happy path and error path have no test coverage. A regression in loop logic or enum constant naming would go undetected.
Fix: Add unit tests for fromId with a valid role ID, an invalid role ID (verifying IllegalArgumentException), and verify the error message content.

[P2-A22-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Roles.java | Line: 44
Description: Roles.RoleId.fromId(String) has no null-guard. Passing null relies on String.equals returning false, ultimately throwing IllegalArgumentException with message "Name null is not valid role identifier". This behavior is undocumented and untested.
Fix: Add an explicit null check at the top of fromId or document the behavior, and add a test case for null input.

[P2-A22-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Results.java | Line: N/A
Description: Results is a hand-written POJO with no equals, hashCode, or toString overrides. Tests cannot assert state equality between two Results instances without reflection, making state-level assertions impossible.
Fix: Add equals, hashCode, and toString methods (or use Lombok @Data), and write tests to verify field-level equality.

[P2-A22-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Services.java | Line: N/A
Description: Services is a hand-written POJO with nine fields and no equals, hashCode, or toString overrides. Field deserialization correctness and equality cannot be asserted in unit tests.
Fix: Add equals, hashCode, and toString methods (or use Lombok @Data), and write tests to verify field-level equality.

[P2-A22-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Services.java | Line: 16
Description: BigDecimal fields acc_hours and service_due are nullable objects while other numeric fields are primitive int. No tests verify behavior when these fields are null, zero, negative, or very large. Callers risk NullPointerException.
Fix: Add null-safety checks or document nullable contract, and add boundary-value tests for both BigDecimal fields.

[P2-A22-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Roles.java | Line: 31
Description: RoleId enum contains only one constant (ROLE_COMPANY_GROUP). The fromId loop iteration logic is untested for multi-value scenarios, so adding future constants has no regression safety net.
Fix: Add tests that exercise fromId with both matching and non-matching values, and add a multi-constant test if additional roles are defined.

[P2-A22-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Results.java | Line: 13
Description: The field message_id uses snake_case naming, producing non-standard getter getMessage_id(). No test verifies the JSON serialization key, so a refactor to standard camelCase naming would silently change the wire format.
Fix: Add a JSON serialization test that asserts the expected key name "message_id" in the output, or add @JsonProperty annotation to lock the contract.

[P2-A22-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Services.java | Line: 13
Description: All nine fields in Services use snake_case naming with matching non-standard getter names. Jackson serialization behavior is tied to these names but no test verifies the serialized output or RequestBody deserialization round-trip.
Fix: Add a JSON serialization/deserialization test that asserts correct key names, or add @JsonProperty annotations to lock the wire format.

[P2-A22-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Roles.java | Line: N/A
Description: Lombok @Data generates equals, hashCode, and toString for Roles based on all four fields, but no test confirms field-level equality semantics or builder behavior. The builder is used in production DAOs but never exercised in tests.
Fix: Add tests verifying equals/hashCode contract and builder construction for the Roles class.

[P2-A22-11] LOW | File: src/test/java/com/journaldev/spring/jdbc/service/APKUpdaterServiceTest.java | Line: 17
Description: APKUpdaterServiceTest contains two test methods that are entirely commented out. The class compiles but executes zero assertions, providing false confidence in test coverage.
Fix: Either restore and fix the commented-out tests or remove the dead test class entirely.

[P2-A23-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/Sessions.java, src/main/java/com/journaldev/spring/jdbc/model/Types.java, src/main/java/com/journaldev/spring/jdbc/model/Usage.java | Line: N/A
Description: Sessions, Types, and Usage model classes have zero test coverage. No test file references any of these classes directly or indirectly. They are persistence/serialization contracts used throughout the application with no regression safety net.
Fix: Create unit tests for all three model classes covering construction, getter/setter behavior, and serialization contracts.

[P2-A23-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Sessions.java, src/main/java/com/journaldev/spring/jdbc/model/Types.java, src/main/java/com/journaldev/spring/jdbc/model/Usage.java | Line: N/A
Description: Sessions, Types, and Usage all implement Serializable but provide no equals() or hashCode() overrides. Object.equals uses reference identity, which is incorrect for value-bearing model objects used in collections.
Fix: Add equals and hashCode overrides (or use Lombok @Data) to all three classes and add tests verifying the contract.

[P2-A23-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Sessions.java, src/main/java/com/journaldev/spring/jdbc/model/Types.java, src/main/java/com/journaldev/spring/jdbc/model/Usage.java | Line: N/A
Description: None of the three classes override toString(). Log statements and debugging output print opaque reference addresses instead of useful field values.
Fix: Add toString overrides (or use Lombok @ToString) to all three classes.

[P2-A23-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Sessions.java | Line: 62
Description: Sessions holds four String photo URL fields and two timestamp fields. All setters accept null without constraint. Consumers that assume non-null values risk NullPointerException at runtime, and no tests verify null or empty-string behavior.
Fix: Add input validation or null checks to setters, and write tests for null, empty-string, and malformed URL inputs.

[P2-A23-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Sessions.java | Line: 50
Description: start_time and finish_time are stored as raw Strings with no temporal ordering enforcement. A session where finish_time precedes start_time can be constructed without error, potentially corrupting reports or calculations.
Fix: Use proper temporal types (e.g., Instant or LocalDateTime) and add validation ensuring finish_time is after start_time. Add tests for this constraint.

[P2-A23-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Usage.java | Line: 14
Description: The usage field is initialized inline to new BigDecimal(0) but no test verifies this default. setUsage(null) accepts null without guard, overwriting the safe default and exposing subsequent arithmetic to NullPointerException.
Fix: Add a null guard to setUsage or document the nullable contract, and add tests for default value and null assignment.

[P2-A23-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Sessions.java | Line: 29
Description: Primitive int fields (id, driver_id, unit_id) default to 0 on construction. No tests verify sentinel or boundary behavior. If 0 is a valid database ID, distinguishing unset from valid becomes impossible.
Fix: Add tests verifying default values and boundary conditions (Integer.MAX_VALUE, negative values) for all int fields.

[P2-A23-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Sessions.java | Line: 23
Description: The prestart_required boolean defaults to false via Java primitive initialization. No test verifies the default value or toggling behavior.
Fix: Add tests verifying the default false value and correct toggling via setter.

[P2-A23-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Types.java | Line: 25
Description: Types.setName and Types.setUrl accept null and empty strings without validation. Null name breaks display/comparison logic and null/malformed url breaks HTTP clients.
Fix: Add input validation for null and empty strings in setters, and add tests for these edge cases.

[P2-A23-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Usage.java | Line: 19
Description: Usage.setTime(String) accepts null without validation. A freshly constructed Usage returns null from getTime(). No test verifies this default or exercises null/empty-string downstream behavior.
Fix: Add null validation or document the nullable contract, and add tests for null and empty-string time values.

[P2-A23-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Sessions.java, src/main/java/com/journaldev/spring/jdbc/model/Types.java, src/main/java/com/journaldev/spring/jdbc/model/Usage.java | Line: N/A
Description: All three classes implement Serializable with explicit serialVersionUID constants but no test performs a serialize-then-deserialize round-trip. A field change without updating serialVersionUID causes InvalidClassException at runtime.
Fix: Add serialization round-trip tests for each class to verify field values survive the cycle and serialVersionUID stability.

[P2-A23-12] LOW | File: src/test/java/com/journaldev/spring/jdbc/service/APKUpdaterServiceTest.java | Line: 17
Description: APKUpdaterServiceTest contains two entirely commented-out test methods. The class compiles and appears in the test suite but contributes zero assertions, creating a false impression of coverage.
Fix: Restore and fix the commented-out tests, or remove the dead test class.

[P2-A24-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/User.java | Line: N/A
Description: User class has zero test coverage. The Lombok-generated lifecycle (constructor, builder, getters/setters, equals, hashCode, toString) and the explicit addRoles method are entirely untested.
Fix: Create a comprehensive test class for User covering construction, builder, addRoles, and Lombok-generated methods.

[P2-A24-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/User.java | Line: 41
Description: User.addRoles delegates to HashSet. Adding a duplicate Roles object silently does nothing and adding null is permitted but may cause downstream issues. Neither edge case is tested.
Fix: Add tests for duplicate role addition, null role addition, multiple distinct roles, and verify getRoles reflects additions.

[P2-A24-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/User.java | Line: 33
Description: The @Builder constructor assigns id, name, email, password, and active but never sets roles. The field initializer (new HashSet<>()) behavior with Lombok builder is unverified. No test confirms builder-created users have a non-null empty roles set.
Fix: Add a test verifying that User.builder().build().getRoles() returns a non-null empty set.

[P2-A24-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/User.java | Line: 23
Description: User.equals/hashCode is restricted to the email field only via @EqualsAndHashCode(onlyExplicitlyIncluded = true). Two users with identical emails but different passwords compare as equal. This security-sensitive design choice is untested.
Fix: Add tests verifying the email-only equality contract and document the design decision.

[P2-A24-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/UserResponse.java | Line: N/A
Description: UserResponse class has zero test coverage. As a serializable DTO with @JsonInclude(NON_NULL), the serialization contract is never exercised.
Fix: Create tests for UserResponse covering construction, all field accessors, and JSON serialization with null/non-null fields.

[P2-A24-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/UserResponse.java | Line: 12
Description: The @JsonInclude(NON_NULL) annotation suppresses null fields in JSON output, but no test verifies this behavior. A fully populated, partially populated, or all-null instance serialization is untested.
Fix: Add JSON serialization tests verifying null-field suppression behavior.

[P2-A24-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterException.java | Line: 5
Description: APKUpdaterException has zero test coverage. Neither the one-arg nor two-arg constructor is tested. No test verifies message propagation via getMessage() or cause chaining via getCause().
Fix: Add unit tests for both constructors verifying message and cause propagation.

[P2-A24-8] HIGH | File: src/test/java/com/journaldev/spring/jdbc/service/APKUpdaterServiceTest.java | Line: 17
Description: APKUpdaterServiceTest is entirely commented out. The IOException error path in APKUpdaterService that uses APKUpdaterException(String, Throwable) is never exercised. Cause wrapping is unverified.
Fix: Restore and update the commented-out tests, or write new tests covering the IOException wrapping path.

[P2-A24-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterException.java | Line: 9
Description: The one-arg constructor is used at APKUpdaterService line 66 inside a catch(IOException e) block, but the caught exception e is not passed as the cause. The root cause is silently dropped. No test detects this cause-loss.
Fix: Change the call site to use the two-arg constructor passing the IOException as cause, and add a test verifying cause preservation.

[P2-A24-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/User.java, src/main/java/com/journaldev/spring/jdbc/model/UserResponse.java | Line: N/A
Description: User and UserResponse declare explicit serialVersionUID constants but no test verifies deserialization round-trips or UID stability across refactors. These are network-transmitted user models containing passwords and PII.
Fix: Add serialization round-trip tests for both classes.

[P2-A24-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/UserResponse.java | Line: 25
Description: The field lastname does not follow camelCase convention (should be lastName). The Lombok-generated getter is getLastname() rather than getLastName(), producing a lowercase JSON key that may silently mismatch consumer expectations.
Fix: Rename the field to lastName or add @JsonProperty("lastname") to lock the serialized key, and add a serialization test.

[P2-A25-1] CRITICAL | File: src/test/java/com/journaldev/spring/jdbc/service/APKUpdaterServiceTest.java | Line: 17
Description: All APKUpdaterService tests are commented out. The setUp block and both @Test methods are wrapped in block comments. The test runner discovers the class but executes zero test methods. Neither getAvailablePackage nor loadPackageAsResource is tested.
Fix: Restore and update the commented-out tests or write new tests covering both methods and their error paths.

[P2-A25-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: N/A
Description: AWSFileStorageService and AbstractFileStorageService have zero test coverage. No test references these classes or any FileStorageService interface methods. The entire file-storage subsystem is untested.
Fix: Create unit tests for both classes, mocking AWS S3 client and filesystem operations, covering all public methods and error paths.

[P2-A25-3] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 31
Description: Hardcoded AWS Access Key ID (AKIA**REDACTED**) and Secret Access Key are embedded directly in source code and committed to version control. No test validates that credentials are loaded from a secure external source.
Fix: Remove hardcoded credentials and use AWS IAM roles, environment variables, or a secrets manager. Rotate the exposed keys immediately. Add a test verifying credential injection from configuration.

[P2-A25-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java | Line: 66
Description: The IOException error path in loadPackageAsResource is untested and the error message is malformed (missing space before "version" producing "version1.0.0-local"). No test validates exception message content.
Fix: Fix the error message formatting and add tests exercising both the FileNotFoundException and APKUpdaterException paths.

[P2-A25-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 75
Description: uploadObject silently swallows AmazonServiceException on S3 put failure. The exception is logged but not re-thrown, so the saveImage caller believes the upload succeeded when it actually failed.
Fix: Re-throw the exception or return a failure indicator, and add tests verifying that S3 upload failures propagate to callers.

[P2-A25-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 46
Description: loadImageAsResource is a permanent stub that unconditionally returns null. Any caller invoking this method will encounter NullPointerException. This violates the FileStorageService interface contract.
Fix: Implement S3 resource retrieval or throw UnsupportedOperationException, and add a test documenting the expected behavior.

[P2-A25-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java | Line: 49
Description: The IOException catch block wrapping Files.list(Paths.get(packageDir)) is never exercised by any test. No test provides a non-existent or inaccessible packageDir to trigger this branch.
Fix: Add a test that triggers IOException by providing an invalid packageDir, verifying APKUpdaterException is thrown with the correct message and cause.

[P2-A25-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java | Line: 47
Description: PackageEntry.compareTo only compares version fields (major, minor, patch), not the package name. A newer version of a different application package could be returned as the correct package. No test covers multi-package directory scenarios.
Fix: Add name-field filtering before version comparison and add tests with directories containing multiple differently-named packages.

[P2-A25-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java | Line: 60
Description: MIME detection failure silently falls back to .jpg extension. Non-image content (PDF, binary) will be stored with a .jpg extension without any test verifying this fallback behavior.
Fix: Add tests for undetectable MIME types, non-image streams, and null content-type returns to verify fallback behavior.

[P2-A25-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java | Line: 47
Description: The @PostConstruct initialize() method throws FileStorageException if Files.createDirectories fails, but no test triggers this path. The error message is also misleading ("save the directory" instead of "create the directory").
Fix: Add a test triggering directory creation failure and fix the error message wording.

[P2-A25-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java | Line: 33
Description: When packageDir contains no files, getAvailablePackage returns Optional.empty(). While likely acceptable, this behavior is undocumented by any test.
Fix: Add a test for the empty directory scenario verifying Optional.empty() is returned.

[P2-A25-12] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 50
Description: connectAWSS3 and the bucket-existence/creation paths in uploadObject have no test coverage. Failures in client construction or bucket creation propagate as uncaught runtime exceptions.
Fix: Add mock-based tests for S3 client construction, bucket-exists check, and bucket-creation paths.

[P2-A25-13] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 74
Description: S3 upload sets CannedAccessControlList.PublicRead on every uploaded object, making all images publicly accessible without authentication. No test asserts or flags this policy.
Fix: Make the ACL configurable via a property and add a test verifying the expected ACL is applied. Review whether public-read is the correct policy.

[P2-A25-14] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 55
Description: AWS region is hardcoded to US_EAST_1 with no @Value injection and no test verifying region configurability.
Fix: Externalize the region to a configuration property and add a test verifying correct region selection.

[P2-A25-15] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java | Line: 25
Description: The compiled regex pattern for APK filename matching uses non-greedy quantifiers and allows empty captures. Files with unusual names may match or not match in unexpected ways. The only tests for this regex are commented out.
Fix: Add unit tests for the regex covering edge cases such as missing name, missing env suffix, and unusual version formats.

[P2-A25-16] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java | Line: 65
Description: The method call Util.generateRadomName() contains a typo ("Radom" instead of "Random"). No test documents or verifies the generated filename format.
Fix: Correct the method name typo in Util and all call sites, and add tests for the filename generation.

[P2-A25-17] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java | Line: 36
Description: targetLocation and fileName are protected mutable instance fields written by saveImage and read by the AWSFileStorageService subclass. Concurrent calls on the singleton bean cause a race condition. No test exercises concurrent invocations.
Fix: Refactor to use local variables or method return values instead of shared mutable fields, and add concurrency tests.

[P2-A26-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/BootstrapService.java | Line: N/A
Description: BootstrapService and its inner FlywayBean class have zero test coverage. The @Bean method with initMethod="migrate" contains a conditional branch on flyway.enabled. FlywayBean.migrate() has a null-guard branch and can propagate FlywayException. None of these paths are tested.
Fix: Create tests covering both enabled/disabled Flyway branches, migrate() with null and non-null Flyway, and FlywayException propagation.

[P2-A26-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: N/A
Description: CognitoService has zero test coverage. Both public methods (getUser and authenticationRequest) make outbound HTTP calls via a non-injected RestTemplate. No test exercises any HTTP response scenario.
Fix: Refactor RestTemplate to be injectable, then create tests covering HTTP 200, non-200, and exception paths for both methods.

[P2-A26-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: 36
Description: RestTemplate is constructed inline via new RestTemplate() in both methods rather than injected, making unit testing impossible without real network calls.
Fix: Inject RestTemplate as a bean or constructor parameter to enable mocking in tests.

[P2-A26-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/DriverAlreadyExistException.java | Line: 9
Description: The two-arg constructor (message, Throwable) is never called anywhere in the codebase and has no test coverage. The single-arg constructor used at DriverService line 69 also has no unit test.
Fix: Add tests for both constructors verifying message and cause propagation. Remove the two-arg constructor if it is confirmed dead code.

[P2-A26-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: 60
Description: Both getUser and authenticationRequest silently swallow all exceptions. On any failure, the method returns an empty default-constructed response object with no error indicator. Callers receive structurally valid but empty objects, creating a silent data corruption risk.
Fix: Propagate exceptions or return an error-indicating response type, and add tests verifying caller behavior on failures.

[P2-A26-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: 34
Description: When authenticationRequest() fails and returns an empty AuthenticationResponse, getSessionToken() returns null. This null is concatenated into the URL as the literal string "null", producing a request with "&accessToken=null".
Fix: Add a null check for sessionToken before constructing the URL, and add a test exercising the failed-authentication path.

[P2-A26-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/BootstrapService.java | Line: 55
Description: BootstrapService imports Logger/LoggerFactory but never uses them. FlywayBean.migrate() uses System.out.println instead of the logging framework, bypassing log aggregation and monitoring.
Fix: Replace System.out.println with SLF4J logger calls and remove unused imports.

[P2-A26-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: 48
Description: Both methods construct URLs with hardcoded "http://localhost:" scheme and host. Only the port is configurable. The protocol is plaintext HTTP with no TLS, and no test validates URL construction.
Fix: Externalize the full base URL to a configuration property and add tests verifying URL construction.

[P2-A26-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/BootstrapService.java | Line: 40
Description: FlywayBean is a non-static inner class, implicitly holding a reference to the enclosing BootstrapService instance. This prevents independent instantiation for unit testing.
Fix: Make FlywayBean a static nested class or a top-level class to improve testability.

[P2-A26-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/DriverAlreadyExistException.java | Line: N/A
Description: DriverAlreadyExistException has no serialVersionUID. Neither it nor its parent DriverServiceException declares one. Serialization across distributed boundaries could fail after recompilation.
Fix: Add serialVersionUID to both DriverAlreadyExistException and DriverServiceException.

[P2-A27-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: N/A
Description: DriverService has zero test coverage. All four methods (authenticate, registerDriver, resetPassword, generateRandomPassword) containing authentication, registration, and password reset business logic are completely untested.
Fix: Create a comprehensive test class for DriverService covering all methods and their error paths with mocked DAO dependencies.

[P2-A27-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 58
Description: The authenticate() method catches SQLException from driverDAO.updateLastLoginTime() and re-throws as DriverServiceException. This error path is never exercised in any test.
Fix: Add a test that mocks driverDAO.updateLastLoginTime() to throw SQLException and verifies the DriverServiceException wrapping.

[P2-A27-3] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 74
Description: registerDriver() calls orElseThrow(IllegalStateException::new) when ROLE_COMPANY_GROUP is not found in the database. This unchecked exception propagates through the @Transactional boundary with no test coverage or documentation.
Fix: Add a test for the missing-role scenario and consider using a more descriptive exception with a message.

[P2-A27-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 73
Description: The contact-person branch in registerDriver() (company creation, role assignment) and the non-contact-person branch are both untested. Any regression in company creation would go undetected.
Fix: Add tests covering both the contact-person and non-contact-person registration paths.

[P2-A27-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 86
Description: SendEmail.sendMail() is called unconditionally during registration with no test mocking or verification. Any unit test would attempt to send a real email. Email content correctness is never asserted.
Fix: Refactor SendEmail to be injectable/mockable and add tests verifying the correct email subject, body, and recipient.

[P2-A27-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 114
Description: The resetPassword() method catches SQLException from driverDAO.updatePassword() and wraps it in DriverServiceException. This catch block is never exercised by any test.
Fix: Add a test that mocks updatePassword to throw SQLException and verifies the exception wrapping.

[P2-A27-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 111
Description: resetPassword() sends email with the new plaintext password in the message body. No test verifies the correct password, subject line, or recipient address is used.
Fix: Mock the email sending and add tests asserting correct email content including the generated password.

[P2-A27-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 51
Description: authenticate() is marked @Deprecated but remains in active use by DriverController.getLoginAuth(). No test verifies the deprecated path still functions correctly, and there is no evidence of a tested replacement.
Fix: Add tests for the deprecated method and create a migration plan to a replacement authentication mechanism.

[P2-A27-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 119
Description: generateRandomPassword() applies four CharacterRule constraints and a fixed length of 8 but no test verifies the generated password satisfies these rules or has the correct length.
Fix: Add tests verifying password length, character composition rules, and randomness properties.

[P2-A27-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/DriverServiceException.java | Line: 9
Description: The two-arg constructor with cause chaining is used at multiple throw sites but no test verifies getCause() returns the original exception.
Fix: Add tests for both constructors verifying message and cause propagation.

[P2-A27-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/EntityNotFoundException.java | Line: 9
Description: EntityNotFoundException is annotated with @ResponseStatus(HttpStatus.NOT_FOUND) but no test verifies the annotation produces an HTTP 404 response when the exception is thrown from a controller.
Fix: Add a Spring MVC integration test verifying that throwing EntityNotFoundException results in HTTP 404.

[P2-A27-12] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/DriverAlreadyExistException.java | Line: 9
Description: The two-arg constructor (message, Throwable) is never called anywhere in the codebase. It is untested dead code.
Fix: Remove the unused constructor or add tests if future use is planned.

[P2-A27-13] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 68
Description: registerDriver() calls driver.getEmail() without null guards on either the driver parameter or driver.getEmail(). A null argument produces NullPointerException before any validation.
Fix: Add explicit null checks at method entry and add tests for null driver and null email inputs.

[P2-A27-14] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 79
Description: new Long(compId) uses the Long(int) constructor which was deprecated in Java 9 and removed in Java 17. No test catches this as a failure on newer JDKs.
Fix: Replace new Long(compId) with Long.valueOf(compId).

[P2-A27-15] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 88
Description: Commented-out SMS notification code remains without a tracking ticket or explanation. If SMS capability is restored, it would lack test scaffolding.
Fix: Remove the dead commented-out code or create a ticket to properly implement SMS with tests.

[P2-A28-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/FileStorageService.java | Line: 8
Description: FileStorageService.saveImage(InputStream) is the core write path for all image uploads, invoked from at least four controller endpoints. The concrete implementation contains MIME detection, filesystem operations, and two error paths, but no test covers any condition.
Fix: Create comprehensive tests for saveImage covering happy path, MIME detection failure, IOException during copy, and null/empty InputStream.

[P2-A28-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/FileStorageService.java | Line: 10
Description: FileStorageService.loadImageAsResource(String) is the primary read path. LocalFileStorageService has three distinct outcomes (found, not found, malformed URL) and AWSFileStorageService returns null unconditionally. No test covers any branch.
Fix: Create tests covering resource found, resource not found (FileNotFoundException), MalformedURLException, null filename, and path traversal attempts.

[P2-A28-3] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 46
Description: AWSFileStorageService.loadImageAsResource unconditionally returns null with no test, no marker, and no documentation. Callers will encounter NullPointerException. The FileStorageService interface contract is silently violated.
Fix: Implement actual S3 resource retrieval, or throw UnsupportedOperationException, and add a test documenting the behavior.

[P2-A28-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/FileStorageException.java | Line: 11
Description: The two-arg constructor (message, Throwable) for cause chaining is used in production but no test verifies the cause is correctly propagated via getCause().
Fix: Add a unit test verifying both constructors and cause chain propagation.

[P2-A28-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/FileNotFoundException.java | Line: 7
Description: FileNotFoundException carries @ResponseStatus(HttpStatus.NOT_FOUND) but no test verifies the constructor passes the message correctly or that Spring resolves the annotation to HTTP 404.
Fix: Add tests verifying constructor message propagation and the @ResponseStatus 404 mapping.

[P2-A28-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java | Line: 43
Description: The @PostConstruct initialize() method throws FileStorageException if Files.createDirectories fails. No test exercises startup failure behavior with corrupt or inaccessible uploadDir.
Fix: Add a test triggering directory creation failure and verifying the FileStorageException is thrown.

[P2-A28-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/FileStorageService.java | Line: N/A
Description: The FileStorageService interface is not tested via any mock or integration harness. No controller test verifies correct invocation, return value handling, or exception propagation.
Fix: Add @WebMvcTest or @SpringBootTest integration tests for controllers that inject FileStorageService.

[P2-A28-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/FileStorageException.java | Line: 7
Description: The single-arg constructor of FileStorageException is untested. Error messages are interpolated with dynamic filenames in production, making the message content observable by clients.
Fix: Add a unit test verifying getMessage() returns the expected message.

[P2-A28-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java | Line: 54
Description: MIME-type detection silent-fallback to .jpg means non-image binary payloads, corrupted streams, or unsupported types silently produce .jpg-named files. No test verifies this fallback behavior.
Fix: Add tests for non-image content, corrupted streams, and null content-type scenarios.

[P2-A28-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/FileStorageException.java | Line: 5
Description: FileStorageException declares serialVersionUID but is used exclusively as a runtime exception and is never serialized. Future field additions without updating the UID could cause incompatible serial forms.
Fix: Add a serialization round-trip test or remove the explicit serialVersionUID if serialization is not intended.

[P2-A28-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/FileStorageService.java | Line: N/A
Description: The FileStorageService interface has no null-safety annotations on method parameters or return values. AWSFileStorageService legally returns null from loadImageAsResource under the current contract.
Fix: Add @NonNull annotations to both parameters and return types, and add tests asserting null-safety preconditions.

[P2-A28-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/FileNotFoundException.java | Line: N/A
Description: FileNotFoundException does not declare serialVersionUID, unlike its parent FileStorageException. The JVM-computed UID will change if the class structure changes.
Fix: Add an explicit serialVersionUID to FileNotFoundException.

[P2-A29-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/LocalFileStorageService.java | Line: N/A
Description: LocalFileStorageService and its parent AbstractFileStorageService have zero test coverage. The class is the sole concrete implementation for persisting and retrieving user-uploaded images. All branches (file found, file not found, malformed URL, MIME failure, copy failure, directory creation failure) are uncovered.
Fix: Create comprehensive tests for all branches including happy path, FileNotFoundException, FileStorageException, MIME fallback, and directory creation failure.

[P2-A29-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java | Line: N/A
Description: UserDetailsServiceImpl is the Spring Security authentication entry point for the entire application. Every authenticated API call flows through loadUserByUsername. The class has zero test coverage for user found, user not found, DataAccessException, zero roles, multiple roles, and account locked scenarios.
Fix: Create comprehensive tests mocking UserDAO to cover all authentication paths including success, user-not-found, database failure, and role assignment.

[P2-A29-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/SaveFileInfo.java | Line: N/A
Description: SaveFileInfo is a Lombok @Data @Builder DTO with no test validating the serialization contract, builder pattern, or equals/hashCode/toString behavior. It is part of a public API contract.
Fix: Add tests for builder construction, field accessors, equals/hashCode, and JSON serialization round-trip.

[P2-A29-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java | Line: 38
Description: buildUserFromUserEntity hard-codes enabled=true, accountNonExpired=true, and credentialsNonExpired=true regardless of user entity state. Only accountNonLocked uses the actual isActive() value. Disabled or expired accounts cannot be signaled to Spring Security.
Fix: Map security flags from user entity fields and add tests verifying each flag independently.

[P2-A29-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java | Line: 26
Description: loadUserByUsername declares throws DataAccessException but contains no catch block. Database unavailability causes the exception to propagate uncontrolled through the Spring Security filter chain, producing a 500 response instead of a controlled auth failure.
Fix: Add a catch block for DataAccessException with appropriate error handling, and add a test verifying behavior on database failure.

[P2-A29-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/LocalFileStorageService.java | Line: 19
Description: loadImageAsResource resolves the caller-supplied fileName against imageStorageLocation and calls normalize(), but does not validate that the resulting path stays within the storage directory. A crafted fileName like "../../etc/passwd" could escape the intended boundary.
Fix: Add path-prefix validation after normalization to ensure the resolved path is within imageStorageLocation. Add tests with adversarial filenames.

[P2-A29-7] MEDIUM | File: src/test/java/com/journaldev/spring/jdbc/service/APKUpdaterServiceTest.java | Line: 17
Description: APKUpdaterServiceTest has two test methods that are fully commented out. The class runs but executes nothing, reducing the effective test count for the service package to zero.
Fix: Restore and fix the tests or remove the dead test class.

[P2-A29-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java | Line: 60
Description: The MIME detection failure catch block logs a warning and continues with the default .jpg extension. No test verifies the warning is emitted, the .jpg suffix is applied, or the returned filename uses the fallback extension.
Fix: Add tests for MIME detection failure verifying the warning log and .jpg fallback behavior.

[P2-A29-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java | Line: 36
Description: buildUserFromUserEntity uses userEntity.getEmail() as the Spring Security principal name. The User model permits email to be null, which would cause IllegalArgumentException or an empty principal in the Spring Security User constructor.
Fix: Add a null check for email before constructing the UserDetails, and add a test for a null-email user entity.

[P2-A29-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/FileNotFoundException.java | Line: 9
Description: FileNotFoundException only has a single-arg constructor with no cause-chaining variant. If rethrown with a cause in the future, the original exception would be silently dropped.
Fix: Add a two-arg constructor (message, Throwable) matching the pattern in FileStorageException.

[P2-A29-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/SaveFileInfo.java | Line: 17
Description: The size field is primitive long (not boxed Long). When serialized, an omitted field defaults to 0L instead of null. No test validates the JSON serialization round-trip of SaveFileInfo.
Fix: Add a JSON serialization test verifying the behavior of the size field when present and when omitted.

[P2-A30-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: N/A
Description: HttpDownloadUtility has zero test coverage across all six methods. The class is called from production code in ReportAPI.java but has no unit or integration tests.
Fix: Create unit tests for downloadFile and sendPost covering happy path, error conditions, and accessor methods.

[P2-A30-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 109
Description: A hardcoded API authentication token ("w6_zaejLjssvw02XqIiKdVmv7kP6nOHAw2Ve5mj-qug") is embedded in production source code and committed to version control. No test validates credential externalization.
Fix: Move the token to a configuration property or secrets manager and add a test verifying injection from configuration.

[P2-A30-3] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 103
Description: sendPost uses plain HTTP instead of HTTPS for file transfer to an AWS EC2 instance. The HTTPS line is commented out. Authentication tokens and downloaded payloads are transmitted in clear text.
Fix: Restore the HTTPS connection and remove the commented-out code. Add a test validating TLS is used.

[P2-A30-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 84
Description: Both downloadFile and sendPost catch Exception in the I/O block and call only e.printStackTrace(). The caller receives no indication of failure. getSaveFilePath() can return a path to a non-existent or partially written file.
Fix: Re-throw exceptions or return error indicators, and add tests verifying error propagation to callers.

[P2-A30-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 91
Description: Non-200 HTTP responses produce only a System.out.println message. No exception is thrown and saveFilePath is unchanged. Callers cannot distinguish a failed download from a successful one.
Fix: Throw an exception or return a failure indicator on non-200 responses, and add tests for non-200 status codes.

[P2-A30-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 19
Description: saveFilePath and fileName are private static mutable fields shared across all invocations. Concurrent calls create a race condition where one thread's state corrupts another's.
Fix: Refactor to use return values instead of static mutable state. Make methods return the file path and name directly.

[P2-A30-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/Configuration.java | Line: N/A
Description: Configuration has zero test coverage. No @SpringBootTest or @TestPropertySource test validates that all ten @Value-injected properties bind correctly at startup. A missing or misnamed property key will only be discovered at runtime.
Fix: Add a Spring integration test verifying all property bindings and correct getter behavior.

[P2-A30-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/DateUtil.java | Line: 43
Description: parseDateTimeWithSlashes has no test coverage. The method performs a two-step parse/reformat/re-parse conversion. Ambiguous dates where month and day are interchangeable could silently produce wrong results.
Fix: Add tests for valid input, null/empty input, invalid input, and ambiguous month/day dates.

[P2-A30-9] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/DateUtil.java | Line: 49
Description: getStartDate has no test coverage. All frequency branches (Daily, Weekly, Monthly, default), case-insensitivity, and null-argument NPE paths are untested.
Fix: Add tests for each frequency value, case variations, unrecognized frequency strings, and null arguments.

[P2-A30-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/DateUtil.java | Line: 64
Description: getCurrentDate has no test coverage. The return value format and correctness are unverified.
Fix: Add a test verifying the return value matches "yyyy-MM-dd" format and represents today's date.

[P2-A30-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/DateUtil.java | Line: 68
Description: getYesterdayDateString has no test coverage. The method is called from ResumeController in production but format and correctness are unverified.
Fix: Add a test verifying the return value matches "yyyy-MM-dd" format and represents yesterday's date.

[P2-A30-12] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/DateUtil.java | Line: 74
Description: dateToString has no test coverage. Valid Date input and null input behavior are both unverified.
Fix: Add tests for valid Date input and null input.

[P2-A30-13] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/DateUtil.java | Line: 35
Description: Empty-string input is not tested for parseDateIso and parseDateTimeIso. While StringUtils.isEmpty handles both null and empty string, the empty-string path is not explicitly asserted.
Fix: Add test cases for empty-string input to both parse methods.

[P2-A30-14] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/DateUtil.java | Line: 39
Description: The test parseDateTimeIsoShouldReturnNullWithEmptyDate only passes null. An empty string is a separate valid null-equivalent path that is untested.
Fix: Add a test case for parseDateTimeIso with empty-string input.

[P2-A30-15] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 29
Description: The method parameter fileName shadows the static class field fileName. Assignments inside the method go to the local parameter, not the static field. getFileName() after calling downloadFile returns stale/empty values.
Fix: Rename the parameter to avoid shadowing and add tests verifying accessor state after method calls.

[P2-A30-16] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/Configuration.java | Line: 4
Description: Unused XML serialization imports (org.simpleframework.xml.Element and Root) are present but never applied. These suggest a removed feature with no cleanup.
Fix: Remove the unused imports.

[P2-A30-17] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 130
Description: The dependency call Util.generateRadomName() contains a typo ("Radom" instead of "Random"). No test validates the generated name format or uniqueness.
Fix: Correct the method name in Util and all call sites.

[P2-A30-18] LOW | File: src/test/java/com/journaldev/spring/jdbc/util/DateUtilTest.java | Line: 52
Description: The test helper assertDateEquals compares year, month, date, hour, minute, and second but omits milliseconds. While not currently a defect, the omission could mask failures if formats change.
Fix: Add millisecond comparison to the assertDateEquals helper or document the intentional omission.

[P2-A31-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/util/SMTPAuthenticator.java | Line: 9
Description: getPasswordAuthentication() contains a hardcoded AWS IAM Access Key ID (AKIA**REDACTED**) and Secret Access Key committed in plaintext to version control. The AKIA prefix indicates long-term IAM user credentials. Any repository reader can extract and use these credentials.
Fix: Remove the hardcoded credentials immediately, rotate the exposed keys, and use environment variables or a secrets manager. Add a test validating credential injection from a secure source.

[P2-A31-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/util/SMTPAuthenticator.java | Line: N/A
Description: SMTPAuthenticator is dead code never instantiated or referenced anywhere. SendEmail uses JNDI for session lookup, bypassing this authenticator entirely. The class exists solely as an exposed credential store with no operational justification.
Fix: Delete the class entirely after rotating the exposed credentials.

[P2-A31-3] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/util/RuntimeConf.java | Line: 4
Description: RuntimeConf.database is never referenced anywhere in the source tree. The active class RuntimeConfig defines an identical field production_database with the same JNDI value. The unreferenced duplicate creates confusion about the authoritative configuration source.
Fix: Delete RuntimeConf.java. Ensure all JNDI references use RuntimeConfig.production_database.

[P2-A31-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/SendEmail.java | Line: 14
Description: SendEmail.sendMail() is invoked from three production call sites (DriverService, ImpactDAO, CompanyController) but has zero test coverage. The method performs JNDI lookups, MIME message construction, and email dispatch with no automated verification.
Fix: Refactor to support dependency injection of the mail Session and create tests covering the happy path and all error paths.

[P2-A31-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/SendEmail.java | Line: 29
Description: The setRecipients exception is silently swallowed. If InternetAddress.parse throws for a malformed address, the MimeMessage has no recipients set. Execution proceeds to Transport.send which also fails silently. The net result is completely silent email delivery failure.
Fix: Re-throw the exception or abort the send on recipient-parsing failure. Add tests for malformed email addresses.

[P2-A31-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/SendEmail.java | Line: 17
Description: JNDI lookup failure (NamingException) is caught by the outer Throwable catch and silently swallowed. All three production callers have no way to detect that the email was never sent. User-facing operations (account setup, password reset, impact alerts) fail silently.
Fix: Propagate the exception or return a success/failure indicator. Add tests for JNDI lookup failure.

[P2-A31-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/SendEmail.java | Line: 45
Description: Transport.send() exception is caught and only stack-traced to stderr. SMTP delivery failures (auth failure, connection timeout, relay rejection) are not re-thrown or logged via a framework logger. The method always returns normally.
Fix: Re-throw the exception or return a failure indicator. Replace printStackTrace with SLF4J logging. Add tests for send failures.

[P2-A31-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/SendEmail.java | Line: 14
Description: The mailTo parameter is passed directly to InternetAddress.parse without null or empty-string validation. Null causes NullPointerException (silently swallowed). Empty string results in no recipients and silent send failure.
Fix: Add null and empty-string validation for mailTo at method entry. Add tests for null and empty recipient.

[P2-A31-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/SendEmail.java | Line: 37
Description: The subject and msg parameters are not validated for null. Passing null to setSubject or setContent causes MessagingException or NullPointerException, both silently caught.
Fix: Add null validation for subject and msg parameters. Add tests for null inputs.

[P2-A31-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/SendEmail.java | Line: 33
Description: All four exception-handling sites use System.out.println or e.printStackTrace instead of a structured logger. In containerized deployments, stdout may not be captured or monitored.
Fix: Replace all println/printStackTrace calls with SLF4J logger calls at appropriate severity levels.

[P2-A31-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/RuntimeConf.java | Line: 4
Description: The field is named database in RuntimeConf but production_database in RuntimeConfig. Both hold the same JNDI value. No test enforces consistency. A change to one without the other would go undetected.
Fix: Delete RuntimeConf.java to eliminate the inconsistency. If both must exist, add a test asserting value equality.

[P2-A31-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/SMTPAuthenticator.java | Line: 7
Description: Even ignoring the security issues, getPasswordAuthentication() has no test asserting it returns a non-null PasswordAuthentication or that the returned object carries a username.
Fix: Delete the class (preferred) or add a baseline structural test if the class is retained.

[P2-A31-13] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/SendEmail.java | Line: N/A
Description: No test covers the happy path (successful send) for SendEmail. Without a baseline smoke test using a mocked Session and Transport, no regression protection exists for any future change.
Fix: Add a test using a mocked mail Session and Transport verifying successful message construction and send.

[P2-A32-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 66
Description: Hardcoded AWS SES SMTP credentials (IAM access key ID and secret) are embedded as string literals in source code and committed to version control. The AKIA prefix indicates exploitable long-term IAM credentials.
Fix: Remove hardcoded credentials, rotate the exposed keys, and use environment variables or a secrets manager. Add a test verifying credential injection from configuration.

[P2-A32-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 18
Description: Clickatell SMS gateway username, password, and API ID are hardcoded as public static fields consumed by SendMessage.send_sms_message. No test verifies these values come from an external source.
Fix: Externalize Clickatell credentials to configuration properties or a secrets manager. Add tests verifying injection.

[P2-A32-3] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: N/A
Description: SendMessage has zero test coverage across all three methods (init, send_sms_message, readLines). Live SMS messages are sent in production via ImpactDAO with no test harness or mocking.
Fix: Create tests for SendMessage with mocked HTTP connections and JNDI context, covering success and failure paths.

[P2-A32-4] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: N/A
Description: Util.sendMail has zero test coverage. The method dispatches real email through AWS SES and is called from ResumeController. No mock Transport or integration test exists. Failures are silently swallowed.
Fix: Refactor to support Transport mocking and create tests covering success and failure paths.

[P2-A32-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 119
Description: sendMail always returns true regardless of success or failure. When Transport.send throws or recipient parsing fails, the exception is caught but true is still returned. The boolean return type provides a broken success/failure contract.
Fix: Return false on failure or throw an exception. Add tests verifying the return value under failure conditions.

[P2-A32-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 98
Description: If the attachment parameter is null, attachment.equalsIgnoreCase("") throws NullPointerException. The NPE bubbles to the Throwable catch, is silently swallowed, and the method returns true as though mail was sent.
Fix: Add a null check for the attachment parameter before the equalsIgnoreCase call. Add tests for null attachment.

[P2-A32-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 114
Description: If the Clickatell auth or send endpoint returns an empty HTTP body, readLines returns an empty array. Accessing array_ret[0] throws ArrayIndexOutOfBoundsException. The outer catch absorbs it without logging the failure reason.
Fix: Add bounds checking on array_ret before accessing index 0. Add tests for empty HTTP response bodies.

[P2-A32-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 102
Description: The null check on array_mobile_no is dead code because String.split() never returns null. The actual edge case (empty mobile_no producing [""]) is unguarded and would send SMS to an empty address.
Fix: Replace the null check with an empty-string check on array elements. Add tests for empty mobile_no input.

[P2-A32-9] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java, src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: N/A
Description: Both Util.sendMail and SendMessage.init silently swallow all exceptions using printStackTrace or System.out.println. Errors are not propagated to callers or logged via SLF4J. No test verifies failure surfaces to calling code.
Fix: Replace exception swallowing with proper logging and exception propagation. Add tests verifying error handling.

[P2-A32-10] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 31
Description: The ResultSet field rset is declared as an instance field but never assigned anywhere. The finally block that attempts rset.close() is dead code. This suggests incomplete implementation or a copy-paste remnant.
Fix: Remove the unused rset field and the dead finally-block close code.

[P2-A32-11] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 32
Description: The instance field query is declared but never read or written anywhere in SendMessage. It is dead code.
Fix: Remove the unused query field.

[P2-A32-12] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 27
Description: generateRadomName is a pure testable utility method with zero test coverage. No test verifies the output format (timestamp + UUID), uniqueness, or timestamp format. The method name also contains a typo ("Radom" instead of "Random").
Fix: Add tests verifying output format and uniqueness. Rename the method to generateRandomName.

[P2-A32-13] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 29
Description: JDBC resources (conn, stmt, rset) are instance-level fields rather than local variables. If a SendMessage instance were shared across threads, concurrent calls to init would race on these fields. Currently per-call instantiation avoids this, but the design is fragile.
Fix: Refactor conn, stmt, and rset to be local variables within the init method.

[P2-A32-14] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 163
Description: DataInputStream.readLine() is deprecated since Java 1.1 and does not handle character encoding correctly, treating all bytes as ISO-8859-1. The Clickatell API may return UTF-8 responses.
Fix: Replace DataInputStream.readLine with BufferedReader using an explicit charset. Add tests verifying correct encoding handling.

[P2-A32-15] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 78
Description: If InternetAddress.parse throws for a malformed rEmail, execution continues to Transport.send with no recipient set. The send fails silently and true is returned. No test covers the malformed recipient path.
Fix: Abort the send on recipient-parse failure and return false or throw. Add tests for malformed recipient email.

[P2-A32-16] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 24
Description: Util has only static methods but is an instantiable class with no private constructor. It can be instantiated via new Util() which violates the utility class pattern.
Fix: Add a private no-arg constructor to prevent instantiation and declare the class final.

[P2-A32-17] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 25
Description: A Logger is declared but never invoked within Util. All error reporting uses System.out.println and e.printStackTrace. The logging framework integration is incomplete.
Fix: Replace all println/printStackTrace calls with logger calls and remove the unused logger if it remains unused.

[P2-A32-18] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 36
Description: Parameters rName (recipient name) and sName (sender name) are accepted by sendMail but never referenced in the method body. All callers pass "unknown" for both. These unused parameters pollute the API.
Fix: Remove the unused parameters from the method signature and update all call sites.

[P2-A32-19] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 44
Description: All SMTP connection properties (host, port, TLS settings, socket factory class) are hardcoded string literals. There is no mechanism to override these values for testing or environment-specific deployment.
Fix: Externalize SMTP configuration to injectable properties and add tests verifying configurability.

[P2-A32-20] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 78
Description: The Javadoc for send_sms_message says "sending out email", uses PHP parameter syntax ($id, $mobile_no), and includes parameters that do not exist in the Java method signature. The documentation was copied from another codebase without review.
Fix: Rewrite the Javadoc to accurately describe the Java method, its parameters, and its behavior.

---

## Pass 3 — Documentation

[P3-ACFG-1] CRITICAL | File: settings.xml | Line: 9, 14
Description: Plaintext server deployment passwords are committed to source control. TomcatServerUat and TomcatServerAzure have passwords stored in cleartext with no encryption or documentation acknowledging the risk.
Fix: Use Maven encrypted passwords via mvn --encrypt-password and store the encrypted values in settings-security.xml. Remove plaintext passwords from version control and rotate the exposed credentials.

[P3-ACFG-2] CRITICAL | File: environment.dev.properties, environment.prod.properties, environment.uat.properties | Line: 16
Description: Plaintext Cognito API credentials (ciiadmin/ciiadmin) are committed to source control in all three environment property files with no differentiation across environments.
Fix: Externalize credentials using a secrets manager or environment variables. Remove plaintext credentials from version-controlled files and rotate the exposed credentials.

[P3-ACFG-3] CRITICAL | File: spring-security.xml | Line: 113-114, 116-117
Description: OAuth2 client secrets and client IDs are hard-coded in plaintext inside the XML configuration file committed to version control.
Fix: Move client secrets to a database-backed ClientDetailsService or externalized secure configuration. Rotate the exposed secrets immediately.

[P3-ACFG-4] CRITICAL | File: pom.xml | Line: 28-32
Description: Duplicate flyway.url, flyway.user, and flyway.password keys in the local profile cause the first set of credentials to be dead configuration while still exposing the stale password in version control.
Fix: Remove the duplicate/stale property block and its abandoned credentials. Ensure only one set of Flyway properties exists per profile.

[P3-ACFG-5] HIGH | File: pom.xml | Line: 75-76
Description: The UAT profile contains the Flyway database password in plaintext in the POM committed to version control.
Fix: Externalize database credentials from the POM using Maven settings encryption or environment variables.

[P3-ACFG-6] HIGH | File: spring-security.xml | Line: 74
Description: The authentication manager uses MD5 for password hashing, which is cryptographically broken and unsuitable for password storage.
Fix: Migrate to a strong adaptive hashing algorithm such as BCrypt or Argon2. Plan a credential re-hash migration for existing users.

[P3-ACFG-7] HIGH | File: spring-security.xml | Line: 114
Description: OAuth2 client 987654321 has access-token-validity set to 0, meaning tokens never expire, with no documentation explaining this decision.
Fix: Set an appropriate token expiry value. If non-expiring tokens are required, document the business justification and add compensating controls.

[P3-ACFG-8] HIGH | File: spring-security.xml | Line: 13-14
Description: Two OAuth endpoints (cache_approvals and uncache_approvals) are configured with security=none, completely unauthenticated. An inline comment says "Just for testing" suggesting they are test scaffolding left in production.
Fix: Remove the unauthenticated test endpoints from the production configuration or apply appropriate security constraints.

[P3-ACFG-9] HIGH | File: logback.xml | Line: 22-24
Description: A logger for APKUpdaterController is set to DEBUG level with a comment marking it as temporary. This was never reverted and DEBUG logging in production may expose sensitive data.
Fix: Revert the logger level to INFO or WARN. Remove the stale temporary comment.

[P3-ACFG-10] HIGH | File: environment.prod.properties | Line: 11
Description: The imagePrefix property in the production environment file is set to "uat-" instead of "prod-", which is almost certainly a copy-paste error.
Fix: Correct the imagePrefix value to "prod-" in environment.prod.properties.

[P3-ACFG-11] HIGH | File: environment.prod.properties, environment.uat.properties | Line: N/A
Description: The prod and UAT environment property files are byte-for-byte identical, with no documentation confirming whether they intentionally share infrastructure or whether the prod configuration is missing.
Fix: Differentiate the prod and UAT property files with correct environment-specific values, or add documentation confirming intentional sharing.

[P3-ACFG-12] HIGH | File: pom.xml | Line: 60-61
Description: The prod profile defines a Flyway URL targeting the postgres system database with no flyway.user or flyway.password, leaving credentials unspecified with no documentation explaining how they are provided.
Fix: Provide correct Flyway credentials for the prod profile pointing to the application database, or document the external credential injection mechanism.

[P3-ACFG-13] MEDIUM | File: pom.xml | Line: 69
Description: The UAT profile is set as the default active Maven profile, meaning running mvn install without specifying a profile silently targets the UAT environment.
Fix: Remove activeByDefault from the UAT profile. Require explicit profile selection and document the intended build-time profile strategy.

[P3-ACFG-14] MEDIUM | File: pom.xml | Line: 88
Description: The Splunk Artifactory repository URL uses plain HTTP instead of HTTPS, exposing the build to dependency substitution attacks.
Fix: Change the repository URL to HTTPS.

[P3-ACFG-15] MEDIUM | File: logback.xml | Line: 43-45, 47-49
Description: Duplicate logger declarations for com.journaldev.spring and duplicate root logger declarations exist, with earlier declarations being effectively dead configuration.
Fix: Remove the duplicate logger and root declarations. Consolidate the intended routing strategy into a single set of declarations.

[P3-ACFG-16] MEDIUM | File: spring-security.xml | Line: 99-106
Description: All five OAuth2 grant types are enabled simultaneously including the deprecated implicit grant, increasing the attack surface with no documentation of which clients use which grant types.
Fix: Disable unused grant types. Document which clients require which grant types. Remove the implicit grant type per OAuth 2.1 guidance.

[P3-ACFG-17] MEDIUM | File: servlet-context.xml | Line: 57
Description: The JNDI DataSource references "PreStartDB", a legacy name from a prior project that does not correspond to the current application name (fleetiq360ws), creating confusion about which database is targeted.
Fix: Rename the JNDI resource to match the current application name, or add documentation explaining the legacy name.

[P3-ACFG-18] MEDIUM | File: fleetiq360ws.properties | Line: 10
Description: The acceptURL property is hard-coded to a production URL rather than being provided via environment filter tokens, meaning the same URL is used across all environments.
Fix: Parameterize the acceptURL via environment-specific property tokens so each environment uses the correct URL.

[P3-ACFG-19] MEDIUM | File: pom.xml | Line: 12-17
Description: Dependency versions for Spring Framework 3.2.14, Spring Security 3.1.1, Jackson 2.6.7, and AWS SDK 1.11.163 are all end-of-life or severely outdated with known CVEs, and no rationale is documented.
Fix: Upgrade all dependencies to current supported versions. Document version pinning rationale where specific versions are required.

[P3-ACFG-20] MEDIUM | File: spring-security.xml | Line: 83-86
Description: A comment on the tokenServices bean still says "in memory implementation" but the code was changed to JdbcTokenStore, making the comment inaccurate.
Fix: Update the comment to accurately reflect the current JDBC-based token store implementation.

[P3-ACFG-21] LOW | File: pom.xml | Line: 61
Description: The prod profile defines an empty tomcat.url with no documentation explaining how production deployments are performed.
Fix: Document the production deployment mechanism or populate the tomcat.url value.

[P3-ACFG-22] LOW | File: context.xml | Line: N/A
Description: The antiJARLocking attribute is a non-obvious platform-specific Tomcat setting with no explanatory comment.
Fix: Add an inline comment explaining the purpose of antiJARLocking and the platform it targets.

[P3-ACFG-23] LOW | File: web.xml | Line: 31
Description: The resource-ref description reads "DB Connection", which is an entirely generic placeholder providing no useful information about the target database.
Fix: Replace with a meaningful description identifying the database and schema.

[P3-ACFG-24] LOW | File: servlet-context.xml | Line: 62
Description: The component scan base-package is com.journaldev.spring.jdbc, a namespace from a tutorial blog (JournalDev) rather than the organisation namespace (com.collectiveintelligence), indicating the application was built from a tutorial template that was never updated.
Fix: Refactor the package namespace to the organisation's actual namespace, or document the historical reason for the tutorial-derived package name.

[P3-ACFG-25] LOW | File: environment.dev.properties | Line: 12
Description: The property key cloudImagedDir contains a typo ("Imaged" instead of "ImageDir"). The misspelling is consistent across all environment files and the application properties.
Fix: Correct the property name to cloudImageDir across all files if no external dependency relies on the misspelled key, or document it as intentional.

[P3-ACFG-26] LOW | File: logback.xml | Line: 9
Description: The totalSizeCap is set to 3GB with no documentation explaining how this value was chosen or whether it is appropriate for the deployment environment.
Fix: Add a comment documenting the rationale for the 3GB cap and confirm it is appropriate for the target deployment disk capacity.

[P3-ACFG-27] INFO | File: spring-security.xml | Line: 88-93
Description: The comment on the tokenServices bean contains doubled words, a misspelling ("reposibility"), and grammatically ambiguous phrasing that undermines its usefulness as documentation.
Fix: Correct the comment text to fix the typos and clarify the phrasing.

[P3-A01-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAO.java | Line: 8
Description: The APIDAO interface has no class-level Javadoc describing its purpose or the domain concept it models.
Fix: Add class-level Javadoc describing the interface's role as an API key and authentication DAO.

[P3-A01-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAO.java | Line: 10
Description: The public interface method checkKey has no Javadoc describing what constitutes a valid API key, what true/false indicates, or null handling. The parameter name differs between interface (APIkey) and implementation (key).
Fix: Add Javadoc with @param and @return tags clarifying the key validation contract and reconcile parameter naming.

[P3-A01-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAO.java | Line: 11
Description: The public interface method findByName has no Javadoc. The implementation reveals the username parameter is actually an MD5-hashed email, not a name.
Fix: Add Javadoc with @param and @return tags clarifying the expected input format (MD5 hash of email) and return behavior.

[P3-A01-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: 18
Description: The APIDAOImpl class has no class-level Javadoc describing its role, Spring bean name, transactional scope, or data store.
Fix: Add class-level Javadoc documenting the bean name ("apiDao"), the @Transactional scope, and the underlying data store.

[P3-A01-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: 24
Description: The public @Autowired setter setDbDataSource has no Javadoc explaining its purpose as a Spring injection entry point.
Fix: Add Javadoc describing the Spring DataSource injection method and qualifier.

[P3-A01-6] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: 28
Description: The checkKey method always returns true with the only SQL commented out, meaning API key validation is completely bypassed. No documentation warns callers that this is an unimplemented stub.
Fix: Either implement the API key check or add prominent Javadoc and a TODO warning that the method is a non-functional stub bypassing security validation.

[P3-A01-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: 36
Description: The findByName method name implies a lookup by name but the implementation queries by MD5 hash of email. The logger message incorrectly says "Start checkKey for" due to a copy-paste error.
Fix: Add Javadoc clarifying that the parameter is an MD5 hash of email. Rename the method or add documentation explaining the naming discrepancy. Fix the logger message.

[P3-A01-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 25
Description: The CompanyDAO class has no class-level Javadoc describing the repository's purpose or the five database tables it touches.
Fix: Add class-level Javadoc documenting the class purpose, database tables (company, permission, compnay_role_rel, driver, roles), and dependencies.

[P3-A01-9] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 32
Description: The public @Autowired setter setDbDataSource has no Javadoc.
Fix: Add Javadoc describing the Spring DataSource injection method and qualifier.

[P3-A01-10] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 36
Description: The save method has no Javadoc. The returned int (generated company ID), the role of each parameter, the MD5 password storage, and the multi-table atomic operation are all undocumented.
Fix: Add Javadoc with @param and @return tags documenting the return value, parameter roles, and multi-table write behavior.

[P3-A01-11] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 62
Description: The findById method has no Javadoc. The Optional return semantics, multi-table join, image URL resolution, and potential NullPointerException in the result extractor on empty result sets are undocumented.
Fix: Add Javadoc documenting the Optional return contract, the join strategy, and the NPE risk on empty results.

[P3-A01-12] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 74
Description: The findAllByDriverId method has no Javadoc. The filtering logic (companies the driver belongs to but does not own) is entirely undocumented.
Fix: Add Javadoc explaining the membership-not-ownership filter semantics and return behavior.

[P3-A01-13] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 87
Description: The findAllByKeyword method has no Javadoc. The searched fields (company name and email via ilike substring match) and case-insensitivity are undocumented.
Fix: Add Javadoc describing the search semantics including matched fields, wildcard behavior, and case insensitivity.

[P3-A01-14] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 98
Description: The inner class CompaniesResultResetExtractor has no Javadoc, its name is misspelled ("Reset" instead of "Result"), and its row-grouping logic is undocumented.
Fix: Rename the class to CompaniesResultSetExtractor and add Javadoc documenting the row-grouping logic.

[P3-A01-15] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 136
Description: The inner class CompanyResultResetExtractor has no Javadoc, its name is misspelled ("Reset" instead of "Result"), and it will throw a NullPointerException if the result set is empty.
Fix: Rename the class to CompanyResultSetExtractor, add Javadoc, and add a null guard for empty result sets.

[P3-A01-16] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 160
Description: The private helper mapCompany uses a fragile mix of column-index-based and column-name-based ResultSet access with no documentation.
Fix: Add an inline comment or Javadoc explaining the dual-access strategy and the expected column ordering.

[P3-A01-17] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 52
Description: The BASE_QUERY_COMPANY SQL constant joins five tables with a conditional photo_url expression and positional parameters, but has no explanatory comment.
Fix: Add an inline comment documenting the join structure, parameter positions, and which methods extend this base query.

[P3-A01-18] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: 37
Description: The logger message inside findByName reads "Start checkKey for" which is a copy-paste error that misidentifies the operation.
Fix: Correct the logger message to accurately reference findByName.

[P3-A02-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAO.java | Line: 12-22
Description: All nine public methods in the DriverDAO interface lack Javadoc. This is the primary contract for driver data access and callers have no documented parameter semantics, return values, or exception conditions.
Fix: Add Javadoc with @param, @return, and @throws tags to all nine interface methods.

[P3-A02-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAO.java | Line: 21-22
Description: The findByEmailAndPassword method is annotated @Deprecated but has no @deprecated Javadoc tag explaining the deprecation reason or replacement.
Fix: Add a @deprecated Javadoc tag documenting why the method is deprecated and what the replacement is.

[P3-A02-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 33-37
Description: The public Spring injection setter setDbDataSource has no Javadoc explaining its role or the expected qualifier.
Fix: Add Javadoc describing the Spring DataSource injection purpose and qualifier.

[P3-A02-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 152
Description: The findAllTraining method log statement uses the wrong method name ("findAllByCompanyOwner") and wrong parameter label ("ownerId"), producing misleading log output.
Fix: Correct the log statement to reference findAllTraining and driverId.

[P3-A02-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 79
Description: The updateLastLoginTime log message reads "Start update." which was copy-pasted from the update() method without being changed.
Fix: Correct the log message to "Start updateLastLoginTime."

[P3-A02-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 66
Description: The update() method SQL uses column name "iduser" while all other queries use "d.id" or "id". This inconsistency is undocumented and may indicate either dual columns or a latent bug.
Fix: Verify the correct column name and add documentation explaining the discrepancy, or correct the SQL to use the consistent column name.

[P3-A02-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 125-126
Description: The inline comment in findByEmailAndPassword claims both password and email are already hashed, but only the email is hashed client-side. The password is compared directly to the stored hash.
Fix: Correct the inline comment to accurately describe the hashing behavior: email is pre-hashed by the caller, password is compared directly.

[P3-A02-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 40-158
Description: All nine public override methods in DriverDAOImpl lack Javadoc or @inheritDoc tags, leaving implementation-specific behavior (SQL semantics, MD5 hashing, sequence usage) undocumented.
Fix: Add Javadoc or @inheritDoc tags to all public override methods, documenting implementation-specific behavior.

[P3-A02-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/EmailLayoutDAO.java | Line: 21-29
Description: The getEmailLayoutByType method is a stub that returns an empty EmailLayout without executing any SQL or using the type parameter, with no Javadoc or TODO comment.
Fix: Either implement the method or add Javadoc and a TODO comment marking it as an unimplemented stub.

[P3-A02-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/EmailLayoutDAO.java | Line: 16-18
Description: The public constructor EmailLayoutDAO(DataSource) has no Javadoc describing the required parameter or class purpose.
Fix: Add Javadoc documenting the constructor and its DataSource parameter.

[P3-A02-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/EmailLayoutDAO.java | Line: 11
Description: The EmailLayoutDAO class has no class-level Javadoc and lacks a Spring stereotype annotation unlike similar DAOs in the same package.
Fix: Add class-level Javadoc documenting the class purpose and add a @Repository annotation if appropriate.

[P3-A02-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAO.java, src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 11, 22
Description: Neither the DriverDAO interface nor the DriverDAOImpl class has class-level Javadoc documenting the DAO purpose, model relationships, or infrastructure requirements.
Fix: Add class-level Javadoc to both the interface and the implementation class.

[P3-A03-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAO.java | Line: 8-11
Description: The EquipmentDAO interface has no class-level Javadoc and none of its three contract methods have method-level Javadoc, leaving consumers with no documented input, return, or exception behavior.
Fix: Add class-level and method-level Javadoc with @param, @return, and @throws tags for all three interface methods.

[P3-A03-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java | Line: 19, 43, 47, 53, 58
Description: The EquipmentDAOImpl class has no class-level Javadoc and none of its four public methods have Javadoc. The Spring bean name, JDBC datasource qualifier, and configuration dependency are unrecorded.
Fix: Add class-level and method-level Javadoc documenting the bean name, dependencies, and method contracts.

[P3-A03-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java | Line: 47
Description: The getEquipmentByUser method is missing the @Override annotation and the parameter is renamed from userId (interface) to uid (implementation), creating an undocumented inconsistency.
Fix: Add the @Override annotation and reconcile the parameter name to match the interface, or add documentation explaining the difference.

[P3-A03-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java | Line: 24, 30, 37, 53, 64
Description: The ImpactDAO class has no class-level or method-level Javadoc on any of its four public methods. The 80,000 impact threshold, idempotency check, notification subscription names, and Cognito lookup behavior are completely undocumented.
Fix: Add class-level and method-level Javadoc documenting business rules, thresholds, notification triggers, and external service dependencies.

[P3-A03-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java | Line: 37
Description: The magic constant 80000 used as the minimum impact-value threshold for persistence has no comment, no named constant, and no Javadoc explanation. Impacts below this threshold are silently discarded.
Fix: Extract the value to a named constant with a descriptive identifier and add documentation explaining the business rule.

[P3-A03-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java | Line: 64-93
Description: The sendImpactNotification method declares throws SQLException but the actual exception risks are from email/SMS dispatch, not SQL. The declared exception is misleading.
Fix: Update the throws clause to reflect actual exception behavior and add Javadoc @throws tags clarifying failure modes.

[P3-A03-7] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java | Line: 75, 77
Description: The field logger is referenced in sendImpactNotification but is not declared anywhere in ImpactDAO.java, indicating an undeclared-reference defect that is invisible without documentation.
Fix: Declare the logger field in the class or add documentation explaining the intended inheritance or import strategy.

[P3-A04-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/ManufacturerDAO.java | Line: 7-8
Description: The ManufacturerDAO interface has no class-level Javadoc and its sole contract method getManufacturersForUser has no Javadoc, leaving the parameter semantics and return contract undescribed.
Fix: Add class-level and method-level Javadoc with @param and @return tags documenting the manufacturer access model.

[P3-A04-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/ManufacturerDAOImpl.java | Line: 16, 26-36
Description: The ManufacturerDAOImpl class has no class-level Javadoc and the getManufacturersForUser override has no Javadoc. The SQL merges three distinct result sets (driver permission, company ownership, global) which is non-trivial and completely undocumented.
Fix: Add class-level and method-level Javadoc documenting the three-predicate SQL access model.

[P3-A04-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/ManufacturerDAOImpl.java | Line: 19-23
Description: The public Spring @Autowired/@Qualifier datasource wiring method setDbDataSource has no Javadoc.
Fix: Add Javadoc documenting the Spring wiring entry point and its delegation to JdbcDaoSupport.

[P3-A04-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 22, 33-58
Description: UserDAO has no class-level Javadoc and findByName has no Javadoc. The method accepts both plain username and MD5 hash, only returns active users, and aggregates multiple role rows -- none of which is documented.
Fix: Add class-level and method-level Javadoc documenting the dual-accept parameter, active filter, and role aggregation behavior.

[P3-A04-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 61-65
Description: The findByAuthority method has no Javadoc. It promises Optional<Roles> but uses queryForObject which throws EmptyResultDataAccessException on no match, making the Optional.empty() branch unreachable. No documentation warns callers of this discrepancy.
Fix: Add Javadoc documenting the exception behavior. Fix the method to catch EmptyResultDataAccessException and return Optional.empty(), or document the propagating exception.

[P3-A04-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 25-29
Description: The public Spring wiring method setDbDataSource is undocumented.
Fix: Add Javadoc documenting the Spring wiring delegation.

[P3-A04-7] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 22
Description: UserDAO does not implement an interface and has no class-level Javadoc, meaning there is no contract-level documentation layer at all for this security-domain DAO.
Fix: Add class-level Javadoc documenting the class's role in the authentication/security domain, or introduce an interface contract.

[P3-A04-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 31, 60
Description: Both SQL query constants (QUERY_USER_BY_NAME and QUERY_ROLE_BY_AUTHORITY) are complex with no inline comment explaining their intent, target view (v_apiusers), or the MD5 secondary match criterion.
Fix: Add inline comments explaining the query intent, target view, and match criteria.

[P3-A05-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java | Line: 22
Description: No class-level Javadoc on APKUpdaterController. The controller's purpose (APK update and download for Android clients), dependencies, and consumers are entirely undocumented.
Fix: Add class-level Javadoc describing the controller's purpose, endpoints, and intended consumers.

[P3-A05-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java | Line: 38
Description: The getAvailablePackage REST endpoint method has no Javadoc. Parameters, return value, and the silent null return on MalformedURLException are undocumented.
Fix: Add Javadoc with @param, @return, and @throws tags documenting the endpoint contract and error behavior.

[P3-A05-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java | Line: 56
Description: The downloadPackage REST endpoint method has no Javadoc. Parameters, return type, content-type behavior, and failure modes are undocumented.
Fix: Add Javadoc documenting the endpoint contract, content type, and error handling.

[P3-A05-4] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 20-22
Description: The class-level Javadoc reads "Handles requests for the Employee JDBC Service" which is factually inaccurate. The class handles Company and Driver permission operations, not employee operations. This is a stale copy-paste artefact.
Fix: Replace the class-level Javadoc with an accurate description of the CompanyController's actual responsibilities.

[P3-A05-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 37
Description: The getCompany REST endpoint has no Javadoc. The uid parameter represents a driver ID (not a company ID), which is non-obvious from the method name.
Fix: Add Javadoc clarifying that uid is a driver ID and documenting the return value.

[P3-A05-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 44
Description: The getCompanyDrivers REST endpoint has no Javadoc. The uid parameter type (int) is inconsistent with getCompany (Long) with no documentation explaining why.
Fix: Add Javadoc documenting the parameter and reconcile or explain the type inconsistency.

[P3-A05-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 53
Description: The searchCompany REST endpoint has no Javadoc. The keyword matching semantics (prefix, substring, case sensitivity) are undocumented.
Fix: Add Javadoc documenting the search semantics and result behavior.

[P3-A05-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 62
Description: The addCompany REST endpoint has no Javadoc. This is the most complex method in the file with conditional permission insert, multiple SQL queries, email dispatch, and dual HTTP 502 error paths -- all entirely undocumented.
Fix: Add comprehensive Javadoc documenting business rules, guards, SQL operations, email dispatch, and error responses.

[P3-A05-9] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 121
Description: The companyAcceptWeb REST endpoint has no Javadoc. The MD5 token validation mechanism derived from createdat and id is security-sensitive and entirely undocumented.
Fix: Add Javadoc documenting the token generation and validation mechanism and its security properties.

[P3-A05-10] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 148
Description: The companyAccept REST endpoint has no Javadoc. The pid parameter (permission ID), return status, and absence of existence validation are undocumented.
Fix: Add Javadoc documenting the parameter, return status, and validation behavior.

[P3-A05-11] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 163
Description: The companyDelete REST endpoint has no Javadoc. The destructive operation is mapped to HTTP PUT rather than DELETE with no documentation explaining this REST convention deviation.
Fix: Add Javadoc documenting the parameter and explaining the HTTP method choice. Consider changing to HTTP DELETE.

[P3-A05-12] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ConfigurationController.java | Line: 13-15
Description: The existing class Javadoc is partially inaccurate -- it mentions only the configuration injection but the class also injects a dataSource bean which is not mentioned.
Fix: Update the class Javadoc to describe both protected injected fields (configuration and dataSource).

[P3-A05-13] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java, CompanyController.java, ConfigurationController.java | Line: N/A
Description: No @author, @since, or @version Javadoc tags are present in any of the three files, impeding traceability.
Fix: Add @author, @since, and @version tags to all class-level Javadoc blocks.

[P3-A05-14] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java | Line: 48
Description: An inline TODO Handle error comment marks an unresolved error-handling gap where MalformedURLException is silently caught and null is returned (HTTP 200 with null body).
Fix: Implement proper error handling for MalformedURLException and remove the stale TODO.

[P3-A06-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DatabaseController.java | Line: 16, 64
Description: No class-level or method-level Javadoc on DatabaseController or its cleanup() method, which performs a destructive multi-pass database deletion using hardcoded whitelists with no documentation of scope, trigger conditions, or error behavior.
Fix: Add class-level and method-level Javadoc documenting the destructive operation scope, whitelist criteria, idempotency, and error behavior.

[P3-A06-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 42
Description: No class-level Javadoc and no method-level Javadoc on any of the 12 public REST endpoint methods covering authentication, registration, password reset, file upload, licence management, and driver updates.
Fix: Add class-level and method-level Javadoc documenting all 12 endpoint contracts, parameters, return types, and error conditions.

[P3-A06-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 59
Description: The getLoginAuth method is annotated @Deprecated with no @deprecated Javadoc tag explaining the reason or migration path.
Fix: Add a @deprecated Javadoc tag documenting the deprecation reason and recommended replacement.

[P3-A06-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 209-210
Description: The getEmails method log statement reads "Start saveEmails" which is an inaccurate copy-paste that will mislead operators in production logs.
Fix: Correct the log statement to reference getEmails.

[P3-A06-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/DatabaseCleanupException.java | Line: 7-8
Description: No class-level or constructor-level Javadoc on the custom exception. The conditions under which it is thrown and the meaning of the message parameter are undocumented.
Fix: Add Javadoc documenting the exception purpose and usage conditions.

[P3-A06-6] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/DatabaseController.java | Line: 18-60
Description: A 43-line private SQL constant encodes business logic via hardcoded email and MAC address whitelists with no explanatory comment.
Fix: Add a block comment explaining the whitelist criteria, approval history, and last review date.

[P3-A06-7] INFO | File: src/main/java/com/journaldev/spring/jdbc/controller/DatabaseCleanupException.java, DatabaseController.java, DriverController.java | Line: N/A
Description: None of the three classes have @since, @version, or @author tags.
Fix: Add @since, @version, and @author tags to all class-level Javadoc blocks.

[P3-A07-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 23
Description: No class-level Javadoc on EquipmentController. The controller's seven REST endpoints for equipment lifecycle, manufacturer lookup, and service management are entirely undocumented.
Fix: Add class-level Javadoc describing the controller's purpose, REST base path, authentication requirements, and security posture.

[P3-A07-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 36
Description: The getEquipmentByUser endpoint has no Javadoc. It returns HTTP 400 BAD_REQUEST for an empty result set, which is atypical -- an empty list is not an error.
Fix: Add Javadoc documenting the parameters, return type, and non-standard status code semantics.

[P3-A07-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 44
Description: The addEquipment endpoint has no Javadoc. It performs dual-purpose logic (UPDATE if id > 0, else duplicate-check then INSERT) and returns HTTP 502 BAD_GATEWAY on duplicate detection, all undocumented.
Fix: Add Javadoc documenting the branching behavior, preconditions, and error responses.

[P3-A07-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 78
Description: The getManufactureList endpoint has no Javadoc. The dependency on the authenticated principal's username for filtering is undocumented.
Fix: Add Javadoc documenting the authentication dependency and filtering behavior.

[P3-A07-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 86
Description: The getTypeList endpoint has no Javadoc. When mid is 0 all types are returned, otherwise types are filtered by manufacturer -- this branching is undocumented.
Fix: Add Javadoc documenting the mid parameter semantics and branching behavior.

[P3-A07-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 105
Description: The getFuelTypeList endpoint has no Javadoc. Conditional logic where 0 values return all results is undocumented.
Fix: Add Javadoc documenting the parameter semantics and conditional filtering.

[P3-A07-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 123
Description: The getService endpoint has no Javadoc. The computed service_due column semantics and permission-based scoping are undocumented.
Fix: Add Javadoc documenting the service schedule data model and permission-based scoping.

[P3-A07-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 142
Description: The SaveService method has no Javadoc, violates Java naming conventions (PascalCase), and its log message reads "Start addEquipment" which is an incorrect copy-paste.
Fix: Rename to saveService, add Javadoc, and fix the log message.

[P3-A07-9] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ImageController.java | Line: 23
Description: No class-level Javadoc on ImageController. The storage backend, URL pattern, and supported content types are not documented.
Fix: Add class-level Javadoc describing the image serving purpose, storage backend, and URL pattern.

[P3-A07-10] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ImageController.java | Line: 30
Description: The downloadFile endpoint has no Javadoc. File loading, MIME type detection, fallback to application/octet-stream, and error conditions are undocumented.
Fix: Add Javadoc documenting the fileName parameter, MIME detection, fallback behavior, and error handling.

[P3-A07-11] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 39-41
Description: The class-level Javadoc reads "Handles requests for the Employee JDBC Service" which is inaccurate. The class handles impact events, incident reports, and image uploads with no relation to employees.
Fix: Replace the class-level Javadoc with an accurate description of ImpactController's actual responsibilities.

[P3-A07-12] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 59
Description: The saveIncident endpoint has no Javadoc. The sequence ID allocation, ISO datetime parsing, and all request/response fields are undocumented.
Fix: Add Javadoc documenting the request body structure, sequence dependency, datetime parsing, and response format.

[P3-A07-13] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 83
Description: The saveImpactIMAGE endpoint has no Javadoc. The Base64 data-URL stripping logic, AWS storage dependency, and multipart parameters are undocumented. The informal // comment block at lines 73-80 is not Javadoc.
Fix: Add proper Javadoc documenting all parameters, the Base64 processing, AWS storage, and error behavior.

[P3-A07-14] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 117
Description: The saveImpactIMAGEAPP endpoint has no Javadoc. If the type parameter is neither "image" nor "signature", no column is updated but HTTP 200 is still returned -- a silent no-op that is undocumented.
Fix: Add Javadoc documenting valid type values and the behavior for unrecognized types.

[P3-A07-15] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 152
Description: The saveImpactData endpoint has no Javadoc. The deduplication strategy, impact threshold calculation, notification trigger, and two distinct error paths are all undocumented.
Fix: Add Javadoc documenting the deduplication, threshold logic, notification triggers, and error handling.

[P3-A07-16] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 44
Description: The logger is instantiated with ConfigurationController.class instead of ImpactController.class, causing all log output to be misattributed.
Fix: Change the logger to use ImpactController.class.

[P3-A08-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java | Line: 24-26
Description: The class-level Javadoc reads "Not in Use" but the class defines three active @RequestMapping endpoints that are compiled into the application. The comment is factually inaccurate and could lead maintainers to incorrectly delete or ignore the controller.
Fix: Replace the class-level Javadoc with an accurate description, or if the controller is truly unused, remove it from the codebase.

[P3-A08-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java | Line: 35, 53, 72
Description: All three public controller methods (getGPSLocation, saveGPSLocation, saveGPSLocations) lack Javadoc. HTTP method, URI, request body format, and response semantics are not documented.
Fix: Add Javadoc with @param and @return tags to all three methods.

[P3-A08-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java | Line: 1-6
Description: No class-level Javadoc on ReportAPI. The class purpose, responsibilities, and relationship with HttpDownloadUtility and RuntimeConfig are entirely undocumented.
Fix: Add class-level Javadoc documenting the class purpose, dependencies, and usage pattern.

[P3-A08-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java | Line: 24-25
Description: The downloadPDF() method uses a block comment (/* */) instead of Javadoc (/** */). The comment claims the method sends email but it only calls HttpDownloadUtility.sendPost and returns a file path with no email logic. The method also declares throws Exception with no documentation.
Fix: Convert the block comment to Javadoc, correct the inaccurate email claim, and add @return and @throws tags.

[P3-A08-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java | Line: 17-22
Description: The public constructor ReportAPI(String name, String input) lacks Javadoc. The purpose and expected format of the input parameter are undocumented.
Fix: Add Javadoc with @param tags for both constructor parameters.

[P3-A08-6] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java | Line: 47-102
Description: All 14 public accessor/mutator methods lack Javadoc. The non-standard naming of getsEmail/setsEmail/getrEmail/setrEmail departs from JavaBeans conventions without documentation.
Fix: Add field-level Javadoc clarifying what sEmail (sender email) and rEmail (recipient email) represent.

[P3-A08-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/RestURIConstants.java | Line: 1-3
Description: No class-level Javadoc on RestURIConstants, a public constants class with 32 URI path constants used across the application.
Fix: Add class-level Javadoc describing the class purpose and scope.

[P3-A08-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/RestURIConstants.java | Line: 5-6
Description: Two public constants (ACCEPT_USRS, DECLINE_USRS) are marked "unused" by inline comment but remain in the public API with no @Deprecated annotation or Javadoc explaining their status.
Fix: Add @Deprecated annotations and Javadoc explaining the deprecated status, or remove the constants.

[P3-A08-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/RestURIConstants.java | Line: 5-60
Description: None of the 32 public URI constants have Javadoc. Purpose, path variable semantics, and HTTP method associations are not documented.
Fix: Add Javadoc to each constant documenting its purpose, HTTP method, and path variable semantics.

[P3-A08-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/RestURIConstants.java | Line: 52
Description: The RESUME_EQUIPMENT constant contains a misspelled path variable "frequencey" (should be "frequency") baked into the public URI surface with no documentation.
Fix: If clients depend on the misspelled URI, document it as intentional. Otherwise correct the spelling in the constant and all references.

[P3-A08-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/RestURIConstants.java | Line: 50
Description: The GET_SERVICEDTL constant contains a misspelled path segment "sericedetail" (missing "v", should be "servicedetail") with no documentation.
Fix: If clients depend on the misspelled URI, document it as intentional. Otherwise correct the spelling in the constant and all references.

[P3-A09-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 26-28
Description: The class-level Javadoc reads "Handles requests for the Product JDBC Service" which is inaccurate. The class provides resume/reporting endpoints for driver summaries, equipment charts, and report generation.
Fix: Replace the class-level Javadoc with an accurate description of the ResumeController's actual responsibilities.

[P3-A09-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 47-49
Description: The class-level Javadoc reads "Handles requests for the Employee JDBC Service" which is inaccurate. The class manages forklift session lifecycle, pre-start inspections, and offline sync.
Fix: Replace the class-level Javadoc with an accurate description of SessionController's actual responsibilities.

[P3-A09-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 35, 120, 262, 283, 369
Description: All five public endpoint methods lack Javadoc. These REST endpoints contain non-trivial business logic, complex queries, and external service calls with no documentation.
Fix: Add Javadoc to all five methods documenting parameters, return types, business logic, and error behavior.

[P3-A09-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 63, 97, 138, 154, 172, 229, 299, 353, 379
Description: All nine public endpoint methods lack Javadoc. The controller handles session lifecycle, inspection results, and offline sync with no documentation of any endpoint contract.
Fix: Add Javadoc to all nine methods documenting parameters, return types, business logic, and error behavior.

[P3-A09-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: N/A
Description: The class has no class-level Javadoc and none of its 19 public static fields have field-level Javadoc. As a central configuration constants class, the purpose and valid values of each constant are entirely undocumented.
Fix: Add class-level Javadoc and field-level Javadoc to all 19 public static fields.

[P3-A09-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 4
Description: The inline comment "email settings, unused" is factually inaccurate. The fields emailContent and mailFrom from this block are actively referenced in ResumeController.generateReport.
Fix: Remove or correct the inaccurate "unused" comment.

[P3-A09-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 120
Description: The parameter name "frequencey" is a misspelling of "frequency" that propagates through all internal variable names and log output. In the absence of Javadoc, the misspelled name is the only documentation of the parameter's purpose.
Fix: Correct the parameter name to "frequency" in the method signature and all references.

[P3-A09-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 116, 143, 152, 170, 187, 229
Description: Numerous stale TODO comments from 2017 contain no description of what is outstanding or what action is required. They contribute noise rather than documentation.
Fix: Either resolve the TODOs and remove the comments, or update them with actionable descriptions.

[P3-A09-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 225-251
Description: Commented-out code representing a removed business rule about preventing concurrent vehicle use has a brief comment with a spelling error and no explanation of why the rule was removed.
Fix: Remove the commented-out code and add a comment documenting the architectural decision, or restore the business rule.

[P3-A09-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 53
Description: The logger is instantiated with ConfigurationController.class instead of SessionController.class, causing all log output to be misattributed in log aggregation systems.
Fix: Change the logger to use SessionController.class.

[P3-A10-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/UserController.java | Line: 23
Description: The only public method getUserByEmail has no Javadoc. This is an admin-level HTTP endpoint handling user lookup by email with no documentation of the HTTP contract, parameter, or response codes.
Fix: Add Javadoc documenting the endpoint contract, parameter, response codes, and security context.

[P3-A10-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/UserController.java | Line: 17
Description: The UserController class has no class-level Javadoc. For a controller under the /rest/admin/ path, the scope, responsibilities, and security context are entirely undescribed.
Fix: Add class-level Javadoc documenting the controller's admin purpose and security requirements.

[P3-A10-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/UserController.java | Line: 31
Description: The method returns HTTP 502 BAD_GATEWAY when a user is not found, which is semantically incorrect (should be 404). There is no documentation explaining this choice.
Fix: Change the response to HTTP 404 NOT_FOUND or add documentation justifying the 502 status code.

[P3-A10-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/UserController.java | Line: 25
Description: The request parameter is an email address but the DAO method called is findByName(email), creating an undocumented semantic mismatch between the parameter type and the DAO method name.
Fix: Add Javadoc explaining the email-to-findByName mapping, or rename the DAO method to match its actual behavior.

[P3-A10-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/APIConnections.java | Line: 5
Description: The APIConnections class has no class-level Javadoc. The class name does not communicate which API or connection model it represents.
Fix: Add class-level Javadoc documenting which API and what connection model this entity represents.

[P3-A10-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Answers.java | Line: 5
Description: The Answers class has no class-level Javadoc. The plural class name representing a singular record and the question_id foreign key are unexplained.
Fix: Add class-level Javadoc documenting the class purpose and its relationship to the question/survey domain.

[P3-A10-7] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/APIConnections.java | Line: 18, 21, 24, 27
Description: All four public accessor/mutator methods lack Javadoc. Non-standard Pascal-case field names (IDAPIConnection, APIConnectionKey) make the meaning non-obvious without documentation.
Fix: Add Javadoc to the accessors/mutators or add field-level Javadoc explaining the naming convention.

[P3-A10-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Answers.java | Line: 16, 19, 22, 25, 29, 32
Description: All six public accessor/mutator methods lack Javadoc. The getQuestion_id and setQuestion_id methods use non-standard snake_case naming with no documentation explaining the convention.
Fix: Add Javadoc or field-level documentation explaining the naming convention and field semantics.

[P3-A10-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/APIConnections.java | Line: 9-11
Description: The serialVersionUID field carries an IDE-generated empty Javadoc stub ("/** * */") that communicates nothing and is a meaningless placeholder.
Fix: Either remove the empty stub Javadoc or replace it with a meaningful comment.

[P3-A10-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Answers.java | Line: 7-9
Description: The serialVersionUID field carries an identical IDE-generated empty Javadoc stub ("/** * */") that is a meaningless placeholder.
Fix: Either remove the empty stub Javadoc or replace it with a meaningful comment.
[P3-A11-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationRequest.java | Line: 11
Description: No class-level Javadoc on AuthenticationRequest, a security-sensitive model carrying password and access token fields with no documented purpose, lifecycle, or security contract.
Fix: Add class-level Javadoc describing the class purpose, which fields are required per operation, and security constraints such as not logging password fields.

[P3-A11-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationRequest.java | Line: 17
Description: No field-level Javadoc on any field. The semantics of newPassword (password-change flow only?) and accessToken (token refresh or re-authentication?) are undocumented, and callers cannot determine which fields are required vs optional.
Fix: Add Javadoc to each field describing its purpose, which operations use it, and whether it is required or optional.

[P3-A11-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationRequest.java | Line: 13
Description: The Javadoc comment block on serialVersionUID is a generated empty stub with no content, constituting misleading documentation.
Fix: Remove the empty Javadoc stub or replace it with meaningful content.

[P3-A11-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationResponse.java | Line: 13
Description: No class-level Javadoc on the primary authentication response model. The meaning of actualDate vs expirationDate, the distinction between sessionToken and accessToken, and when message vs errors is used are all undocumented.
Fix: Add class-level Javadoc explaining the response structure, field semantics, and the relationship between message and the inherited errors list.

[P3-A11-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationResponse.java | Line: 21
Description: Fields expiresIn, actualDate, expirationDate, and message have non-obvious semantics and no Javadoc. The unit of expiresIn (String type) and date formats/timezones are undocumented.
Fix: Add field-level Javadoc specifying the unit and format for expiresIn, date format and timezone for date fields, and when message is populated.

[P3-A11-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationResponse.java | Line: 14
Description: The Javadoc comment on serialVersionUID is an empty generated stub with no content.
Fix: Remove the empty Javadoc stub or replace it with meaningful content.

[P3-A11-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Charts.java | Line: 9
Description: No class-level Javadoc on Charts. The purpose and usage context are entirely undocumented; it is unclear what "unit" refers to, what total aggregates, or what the relationship to Usage objects is.
Fix: Add class-level Javadoc describing the domain purpose, what unit and total represent, and the Charts-to-Usage relationship.

[P3-A11-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Charts.java | Line: 40
Description: The method addUsageList has no Javadoc. Its name is misleading as it suggests adding a list but actually adds a single Usage item to the internal list.
Fix: Add Javadoc with a @param tag describing the usage argument, and consider renaming the method to addUsage for clarity.

[P3-A11-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Charts.java | Line: 21
Description: None of the 9 hand-written public methods carry any Javadoc. The non-standard addUsageList method and the snake_case getUnit_id/setUnit_id methods especially need documentation.
Fix: Add Javadoc to all public methods, prioritizing non-trivial methods and those with non-standard naming.

[P3-A11-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Charts.java | Line: 11
Description: Empty Javadoc stub on serialVersionUID and no field-level Javadoc. The semantics of unit_id vs unit and the purpose of total are not documented.
Fix: Remove the empty stub and add field-level Javadoc explaining each field.

[P3-A11-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Charts.java | Line: 43
Description: Method names getUnit_id and setUnit_id violate Java camelCase naming conventions, breaking standard JavaBeans introspection. No Javadoc clarifies the naming anomaly.
Fix: Rename methods to getUnitId/setUnitId or add Javadoc explaining why snake_case is used and any introspection implications.

[P3-A12-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Company.java | Line: 13
Description: No class-level Javadoc on Company. The business entity it represents, its lifecycle, its relationship to Driver (contact person), and the semantics of fields like arrRoles, permission, and maxSessionLength are undocumented.
Fix: Add class-level Javadoc describing the Company entity, its purpose, and field semantics.

[P3-A12-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/Company.java | Line: 44
Description: The builder constructor silently overwrites Company name, email, and password with values from the Driver object when contactDriver is non-null. This side-effect is completely undocumented and invisible to callers using the builder.
Fix: Add Javadoc to the class and/or builder documenting this field-overwrite behavior, and consider making the behavior explicit rather than implicit.

[P3-A12-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Company.java | Line: N/A
Description: All 25 Lombok-generated public methods have no Javadoc. Of particular concern are getPassword/setPassword which expose credentials with no documentation of encoding, hashing state, or security constraints.
Fix: Add field-level Javadoc on all fields, especially password, to document encoding and security handling expectations.

[P3-A12-4] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Company.java | Line: 15
Description: The existing Javadoc on serialVersionUID is an empty auto-generated stub with only whitespace, conveying no information.
Fix: Remove the empty stub or replace with meaningful content.

[P3-A12-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 15
Description: No class-level Javadoc on Driver, which contains 19 fields including security-sensitive ones (password, securityno, licno) and operationally significant ones (contactperson, driver_based, gps_frequency, compliance_date).
Fix: Add class-level Javadoc explaining the Driver entity and documenting the purpose and constraints of security-sensitive and operational fields.

[P3-A12-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 41
Description: The field drivers carries a meaningful inline comment about the contactperson relationship, but it is not a Javadoc comment and does not appear in generated API documentation. The business rule linking contactperson to the drivers list is undocumented in Javadoc.
Fix: Convert the inline comment to a proper Javadoc comment and add Javadoc to the contactperson field explaining the business rule.

[P3-A12-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: N/A
Description: All 46 Lombok-generated public methods have no Javadoc. Equality is based solely on email due to @EqualsAndHashCode(onlyExplicitlyIncluded=true), and getPassword/getSecurityno expose credentials and government IDs with no documentation.
Fix: Add field-level Javadoc on all fields, especially documenting the email-only equality contract, password encoding, and securityno handling requirements.

[P3-A12-8] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 14
Description: The equals and hashCode contract is restricted to the email field only via @EqualsAndHashCode(onlyExplicitlyIncluded=true). Two Driver objects with the same email but different IDs or names are considered equal. This non-standard contract is not documented anywhere.
Fix: Add class-level Javadoc explicitly documenting that equality is based solely on the email field and explaining the rationale.

[P3-A12-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 19
Description: Multiple fields use snake_case naming (first_name, last_name, comp_id, photo_url, etc.) in violation of Java naming conventions. No documentation explains whether this is intentional for ORM column mapping or is a legacy convention.
Fix: Add a class-level comment explaining the naming convention, or refactor field names to camelCase with @Column annotations for ORM mapping.

[P3-A12-10] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/DriverEmails.java | Line: 5
Description: No class-level Javadoc on DriverEmails. The purpose of the four separate email_addr fields rather than a list, and the relationship between driver_id and Driver.id, are not documented.
Fix: Add class-level Javadoc explaining what the four email slots represent, when each is used, and how driver_id relates to the Driver entity.

[P3-A12-11] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/DriverEmails.java | Line: 20
Description: All 12 hand-written public getter and setter methods have no Javadoc. The purpose and distinction between email_addr1 through email_addr4 is not documented, and it is unknown whether ordering is significant or null values are permitted.
Fix: Add Javadoc to all public methods documenting the purpose of each email address slot and null handling.

[P3-A12-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/DriverEmails.java | Line: 7
Description: The existing Javadoc on serialVersionUID is an empty auto-generated stub providing no information.
Fix: Remove the empty stub or replace with meaningful content.

[P3-A12-13] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Company.java | Line: 23
Description: Sensitive fields (password, securityno) have no Javadoc indicating whether values are plaintext, hashed, or encrypted. The @Data-generated toString on both Company and Driver will include these fields, potentially exposing credentials in logs.
Fix: Add Javadoc documenting the encoding state of sensitive fields and add @ToString.Exclude on password and securityno to prevent log exposure.

[P3-A13-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/EmailLayout.java | Line: 5
Description: No class-level Javadoc on EmailLayout. The purpose of the class, the meaning of the type field (email template discriminator?), and the expected format of message (plain text vs HTML vs template) are entirely undocumented.
Fix: Add class-level Javadoc describing the class purpose, valid values for type, and expected format of message.

[P3-A13-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/EmailLayout.java | Line: 17
Description: All 8 hand-written public methods lack Javadoc. These are the primary public API surface of the class with no @param, @return, or descriptive text.
Fix: Add Javadoc to all public methods with appropriate @param and @return tags.

[P3-A13-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java | Line: 5
Description: No class-level Javadoc on DriverTraining. The domain purpose (recording driver equipment training certification), relationship to equipment records, and significance of expiration_date for compliance tracking are not documented.
Fix: Add class-level Javadoc explaining the training record purpose, compliance implications, and entity relationships.

[P3-A13-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/DriverEquipment.java | Line: 10
Description: No class-level Javadoc on DriverEquipment. The semantic meaning of the class representing the driver-equipment association with hours operated and trained status is not documented.
Fix: Add class-level Javadoc describing the driver-equipment relationship and the meaning of hours and trained fields.

[P3-A13-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/DriverEquipment.java | Line: 13
Description: Fields hours and trained have no Javadoc. It is unclear whether hours represents cumulative hours operated or training hours, and whether trained being null is semantically different from false (typed as nullable Boolean).
Fix: Add field-level Javadoc specifying what hours measures and the semantics of null vs false for the trained field.

[P3-A13-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/DriverEquipment.java | Line: 9
Description: @EqualsAndHashCode(callSuper=false) is used with no explanatory comment. This causes DriverEquipment equality to ignore all Equipment parent-class fields, so two instances with different equipment identities will compare as equal if hours and trained match.
Fix: Add a class-level or annotation-level comment explaining why parent fields are excluded from equality and the intended equality semantics.

[P3-A13-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java | Line: 23
Description: Fields training_date and expiration_date are declared as String despite an unused import of java.util.Date. No documentation specifies the expected date format or explains why String was chosen over a temporal type.
Fix: Add field-level Javadoc specifying the expected date format, or refactor to use a proper temporal type. Remove the unused Date import.

[P3-A13-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java | Line: 19
Description: Integer foreign-key fields manufacture_id, type_id, and fuel_type_id have no documentation indicating which database tables or domain entities they reference.
Fix: Add field-level Javadoc specifying the referenced entity or table for each foreign key field.

[P3-A13-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java | Line: 14
Description: The serialVersionUID Javadoc comment is an empty stub placed inline on the same line as the class opening brace, indicating a structural formatting defect from careless copy-paste.
Fix: Remove the empty stub or reformat it properly on its own line with meaningful content.

[P3-A13-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/EmailLayout.java | Line: 7
Description: The serialVersionUID Javadoc is an empty stub with no content, implying documentation intent that was never completed.
Fix: Remove the empty Javadoc stub or replace with meaningful content.

[P3-A13-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java | Line: 4
Description: java.util.Date and Roles.RolesBuilder are imported but never used. The presence of Date alongside String-typed date fields is misleading and suggests incomplete refactoring.
Fix: Remove the unused imports and add a comment on the date fields explaining the String type choice if intentional.

[P3-A13-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/EmailLayout.java | Line: 15
Description: The field type has no documentation indicating its valid values. It likely serves as a discriminator for email template categories but valid values are not enumerated anywhere.
Fix: Add field-level Javadoc listing the valid values for type or referencing the governing constant class.

[P3-A14-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Equipment.java | Line: 11
Description: No class-level Javadoc on Equipment, the core domain model with 18 fields. Fields like driver_based, alert_enabled, impact_threshold, url, and the paired id/name fields (type/type_id, manu/manu_id, comp/comp_id) have non-obvious semantics left entirely undocumented.
Fix: Add class-level Javadoc describing the Equipment entity, its role in the domain, and the conventions for paired id/name fields.

[P3-A14-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Equipment.java | Line: 34
Description: The 18-parameter @Builder constructor has no Javadoc. Many parameters share the same type and the purpose of non-obvious parameters like impact_threshold (unit unspecified), url (target unknown), and attachment_id are undocumented.
Fix: Add Javadoc with @param tags for each constructor parameter, specifying units, valid values, and referenced entities.

[P3-A14-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Equipment.java | Line: 14
Description: No field-level Javadoc on any of the 18 fields. Fields url, impact_threshold, driver_based, attachment_id, and abbreviated fields comp/manu have ambiguous semantics without documentation.
Fix: Add field-level Javadoc to all fields, specifying units for impact_threshold, the URL target, and expanding abbreviations.

[P3-A14-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Equipment.java | Line: N/A
Description: All 39+ Lombok-generated public methods have no Javadoc. The equality behavior (based on all fields including mac_address) is not documented at the class level.
Fix: Add field-level Javadoc so Lombok-generated methods have context, and add a class-level note about the equality contract.

[P3-A14-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/EquipmentType.java | Line: 5
Description: No class-level Javadoc on EquipmentType. Its relationship to Equipment.type_id and the semantics of the icon field (CSS class, file path, URL, or other identifier) are undocumented.
Fix: Add class-level Javadoc describing the entity, its relationship to Equipment, and the format of the icon field.

[P3-A14-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/EquipmentType.java | Line: 7
Description: The Javadoc block on serialVersionUID is an empty auto-generated stub with no content, creating a false impression of documentation coverage.
Fix: Remove the empty Javadoc stub or replace with meaningful content.

[P3-A14-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/EquipmentType.java | Line: 16
Description: None of the six manually-written public accessor methods have Javadoc. The getIcon and setIcon methods especially warrant documentation explaining the icon value format.
Fix: Add Javadoc to all public methods, particularly documenting the icon field format.

[P3-A14-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/ErrorMessage.java | Line: 10
Description: No class-level Javadoc on ErrorMessage, the standardized API error response structure. The distinction between message, code, and detail is undocumented, and whether code is an HTTP status, application error code, or other scheme is unknown.
Fix: Add class-level Javadoc documenting the error response contract, the code scheme, and the intended audience for each field.

[P3-A14-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/ErrorMessage.java | Line: 12
Description: The Javadoc block on serialVersionUID is an empty auto-generated stub with no content, implying intentional documentation review that never occurred.
Fix: Remove the empty Javadoc stub or replace with meaningful content.

[P3-A14-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/ErrorMessage.java | Line: 16
Description: No field-level Javadoc on message, code, or detail. The code field is typed as String rather than int, and the expected format or value set is unspecified.
Fix: Add field-level Javadoc specifying the code format, whether detail is for end-user display or internal logging, and valid value patterns.

[P3-A14-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/ErrorMessage.java | Line: N/A
Description: All Lombok-generated public methods have no Javadoc. The equality contract (based on all three fields) is not stated anywhere in the source.
Fix: Add field-level Javadoc and a class-level note about the equality contract.

[P3-A14-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Equipment.java | Line: N/A
Description: None of the three classes (Equipment, EquipmentType, ErrorMessage) carry @author, @since, or @version Javadoc tags. There is no authorship or versioning metadata in the documentation.
Fix: Add @since tags to each class to track API version introduction.

[P3-A15-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java | Line: 5
Description: No class-level Javadoc on FormDtl. There is no description of the domain entity it models (form detail for inspection checklists), its role in the application, or usage notes for its 7 fields and 14 accessors.
Fix: Add class-level Javadoc describing the form detail entity, its role in inspection checklists, and the meaning of its fields.

[P3-A15-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/FuelType.java | Line: 5
Description: No class-level Javadoc on FuelType. There is no description of what a fuel type represents, how it maps to the database, or how it is consumed by higher-level components.
Fix: Add class-level Javadoc describing the FuelType entity and its relationships.

[P3-A15-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/GCMData.java | Line: 3
Description: No class-level Javadoc on GCMData. The acronym GCM (Google Cloud Messaging, now Firebase Cloud Messaging) is not explained anywhere in the file, and the class purpose and lifecycle are undocumented.
Fix: Add class-level Javadoc explaining GCM/FCM, the class purpose in push notification delivery, and its relationship to the messaging hierarchy.

[P3-A15-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java | Line: 20
Description: All 14 public methods lack Javadoc. Fields input_type (valid values unknown), input_image (URL, file path, or Base64?), expected_answer (matching rules unknown), and input_order (sort convention unknown) have non-obvious semantics.
Fix: Add Javadoc to all methods, specifying valid values for input_type, the format of input_image, matching rules for expected_answer, and the sort convention for input_order.

[P3-A15-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/FuelType.java | Line: 16
Description: All 4 public methods lack Javadoc. The id field has no documentation of whether it is a database primary key, enum ordinal, or application-assigned identifier.
Fix: Add Javadoc to all methods and specify the nature of the id field.

[P3-A15-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GCMData.java | Line: 7
Description: Both public methods getTo and setTo lack Javadoc. The field to represents a GCM/FCM device registration token or topic address, which is a non-trivial value requiring format documentation.
Fix: Add Javadoc describing the expected format (device token or /topics/name), validation requirements, and consequences of invalid values.

[P3-A15-7] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java | Line: 7
Description: The auto-generated Javadoc stub for serialVersionUID is empty, giving a false impression that documentation exists.
Fix: Remove the empty stub or replace with meaningful content.

[P3-A15-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/FuelType.java | Line: 7
Description: The auto-generated Javadoc stub for serialVersionUID is empty and provides no value.
Fix: Remove the empty stub or replace with meaningful content.

[P3-A15-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GCMData.java | Line: 5
Description: The field to is declared protected rather than private with no documented rationale. There is no indication that subclassing is intended or why protected visibility was chosen.
Fix: Add Javadoc explaining the visibility choice or change the field to private if subclass access is not needed.

[P3-A15-10] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/GCMData.java | Line: 3
Description: GCMData does not implement Serializable unlike other model classes. If instances are placed in HTTP sessions or caches requiring serialization, a NotSerializableException will occur. The absence of Serializable is not documented as intentional.
Fix: Either implement Serializable or add a class-level comment documenting that serialization is intentionally unsupported and why.

[P3-A16-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/GCMDataPermission.java | Line: 5
Description: No class-level Javadoc on GCMDataPermission. The purpose of wrapping a Permissions data payload within the GCM message hierarchy is completely undocumented.
Fix: Add class-level Javadoc explaining the class purpose, its role in GCM messaging, and the relationship to GCMData and Permissions.

[P3-A16-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GCMDataPermission.java | Line: 14
Description: Both public methods getData and setData(Permissions) lack Javadoc. There is no documentation of what the Permissions object represents in this context, valid values, or null semantics.
Fix: Add Javadoc to both methods describing the Permissions payload and null handling.

[P3-A16-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GCMDataPermission.java | Line: 7
Description: The serialVersionUID field carries an empty Javadoc stub with no informational content, creating noise without documentation value.
Fix: Remove the empty Javadoc stub or replace with meaningful content.

[P3-A16-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GCMEntity.java | Line: 3
Description: The class-level Javadoc reads "Send back message type to the clients via GCM" which is inaccurate. GCMEntity is a data POJO and does not itself send anything; the description conflates the data-holding role with the sending operation.
Fix: Rewrite the class Javadoc to accurately describe GCMEntity as a data model representing a GCM message type, not as an active sender.

[P3-A16-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GCMEntity.java | Line: 3
Description: The class Javadoc uses the acronym GCM without expansion. No @since, @author, or @version tags are present.
Fix: Expand GCM to Google Cloud Messaging (or note its successor Firebase Cloud Messaging) on first use and add @since tag.

[P3-A16-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GCMEntity.java | Line: 10
Description: Both public methods getMsg_type and setMsg_type lack Javadoc. The underscore naming convention is unexplained and the expected values or format of msg_type are not documented.
Fix: Add Javadoc documenting the expected values of msg_type and explain the naming convention (e.g., matching a GCM protocol field name).

[P3-A16-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/GCMResponse.java | Line: 6
Description: No class-level Javadoc on GCMResponse. This class models the GCM server HTTP response payload, and the absence of any documentation linking it to the external GCM/FCM API specification is a significant gap.
Fix: Add class-level Javadoc describing the GCM response format, linking to the external API specification, and explaining the mapping between class fields and the JSON response.

[P3-A16-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GCMResponse.java | Line: 17
Description: All ten public accessor methods lack Javadoc. Fields success and failure are typed as String rather than numeric types, canonical_ids carries domain-specific GCM meaning, and results contains a List whose per-element structure is undocumented.
Fix: Add Javadoc to all methods, specifying why success/failure are Strings, explaining canonical_ids in GCM context, and documenting the Results list elements.

[P3-A16-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GCMResponse.java | Line: 7
Description: The serialVersionUID field carries an empty Javadoc stub with no informational content.
Fix: Remove the empty Javadoc stub or replace with meaningful content.

[P3-A16-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GCMResponse.java | Line: 11
Description: Fields use underscore-separated names (multicast_id, canonical_ids, etc.) violating Java naming conventions. No comment or @JsonProperty annotation explains that the names align with the GCM JSON response schema.
Fix: Add @JsonProperty annotations or a class-level comment explaining the naming convention matches the GCM API JSON schema.

[P3-A17-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/GPS.java | Line: 5
Description: No class-level Javadoc on GPS, and all 14 public methods are undocumented. The expected format of gps_time (a String), the null semantics of Float-typed longitude and latitude, and the meaning of current_location are not documented.
Fix: Add class-level Javadoc and field-level Javadoc specifying the time format, null semantics for coordinates, and the meaning of current_location.

[P3-A17-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GPS.java | Line: 7
Description: A Javadoc comment block on serialVersionUID contains only whitespace, constituting a misleading empty documentation artifact.
Fix: Remove the empty Javadoc stub or replace with meaningful content.

[P3-A17-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/GPSList.java | Line: 7
Description: No class-level Javadoc on GPSList and neither public method is documented. The purpose of this wrapper class (serialization, REST payload binding, or legacy compatibility) is entirely undocumented.
Fix: Add class-level Javadoc explaining why a dedicated wrapper exists rather than using List<GPS> directly.

[P3-A17-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GPSList.java | Line: 12
Description: The field gpsList has no access modifier (package-private), inconsistent with the private fields of GPS.java. No documentation explains whether this is intentional or an oversight.
Fix: Either make the field private and add proper Javadoc, or document why package-private visibility is intended.

[P3-A17-5] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/Impact.java | Line: 16
Description: The field impact_value (type long) in a safety-critical impact/collision model has no documentation of units (milliG, raw ADC counts, severity level), valid ranges, thresholds, or how the value is produced or consumed.
Fix: Add field-level Javadoc specifying the unit of measurement, valid range, threshold semantics, and the data source producing this value.

[P3-A17-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Impact.java | Line: 12
Description: No class-level Javadoc on Impact. The Lombok @Data and @Builder annotations generate a substantial public API surface, but no source-level documentation exists to flow into the generated members.
Fix: Add class-level Javadoc describing the impact event model and field-level Javadoc on all fields.

[P3-A17-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Impact.java | Line: 8
Description: Unused import java.util.Date suggests impact_time was previously a Date field before being changed to String, with no documentation of the rationale for using String for a timestamp.
Fix: Remove the unused import and add field-level Javadoc on impact_time explaining the timestamp format and why String was chosen.

[P3-A17-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Impact.java | Line: 17
Description: impact_time has no documentation specifying the date/time format, timezone, or locale. mac_address has no documentation identifying which hardware device the address belongs to in a multi-device IoT system.
Fix: Add field-level Javadoc specifying the timestamp format and timezone for impact_time, and which device mac_address refers to.

[P3-A17-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GPS.java | Line: 26
Description: Method names use non-standard snake_case derived from field names (getUnit_id, isCurrent_location, getGps_time). No documentation explains this deviation from Java Bean convention or warns of potential issues with reflection-based tools.
Fix: Add a class-level comment explaining the naming convention or refactor to camelCase with appropriate serialization annotations.

[P3-A17-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GPS.java | Line: N/A
Description: None of the three model classes (GPS, GPSList, Impact) has @since, @version, or @author tags, nor any class-level Javadoc. There is no ownership, versioning, or historical context.
Fix: Add class-level Javadoc with at minimum a @since tag to each class.

[P3-A18-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java | Line: 8
Description: No class-level Javadoc on any of the three public classes ImpactList, ImpactNotification, and Incidents. There is no description of purpose, domain context, thread-safety, or lifecycle for any of them.
Fix: Add class-level Javadoc to ImpactList, ImpactNotification, and Incidents describing their domain purpose and relationships.

[P3-A18-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Incidents.java | Line: 24
Description: All 30 public getter/setter methods on Incidents have no Javadoc. Safety-critical fields like injury, near_miss, incident, signature (byte[]), and image (byte[]) are ambiguous without documentation of encoding, size, nullability, and time formats.
Fix: Add Javadoc to all public methods, prioritizing safety-critical fields with encoding, format, and constraint specifications.

[P3-A18-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java | Line: 16
Description: No Javadoc on either public method. The field impactList has no access modifier (package-private) and no documentation explaining whether this visibility is intentional or an oversight.
Fix: Add Javadoc to both public methods, make the field private, and document the wrapper class purpose.

[P3-A18-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactNotification.java | Line: 21
Description: No Javadoc on the explicit @Builder all-args constructor. The 8 String parameters' meaning, format constraints, and nullability are undocumented, including impact_time format and mobile number format.
Fix: Add Javadoc with @param tags for each constructor parameter specifying formats and constraints.

[P3-A18-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java | Line: 10
Description: Both ImpactList and Incidents contain empty auto-generated serialVersionUID Javadoc stubs that provide no information and give a false impression of documentation coverage.
Fix: Remove the empty stubs or replace with meaningful content.

[P3-A18-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactNotification.java | Line: 7
Description: The Lombok annotation combination (@Data + @NoArgsConstructor + @Builder on explicit constructor) is a non-standard pattern whose intent is undocumented. A future maintainer could inadvertently break this arrangement.
Fix: Add a class-level comment explaining the Lombok annotation pattern and why @Builder is on the constructor rather than the class.

[P3-A18-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Incidents.java | Line: 44
Description: Temporal fields report_time and event_time are typed as String with no format documentation. Callers cannot reliably populate or parse these fields without knowing the expected format.
Fix: Add field-level Javadoc specifying the expected date/time format and timezone convention.

[P3-A18-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Incidents.java | Line: 13
Description: Binary fields signature (byte[]) and image (byte[]) have no documentation of encoding, expected format (JPEG, PNG, PKCS#7, raw bitmap), or size constraints. These are safety-critical in an incident management context.
Fix: Add field-level Javadoc specifying the binary format, encoding, maximum size, and nullability for signature and image.

[P3-A18-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Incidents.java | Line: 12
Description: All fields and accessor methods use snake_case naming (driver_id, injury_type, near_miss, etc.) violating Java naming conventions. No documentation rationalizes the deviation.
Fix: Add a class-level comment explaining the naming convention or refactor to camelCase with @Column annotations.

[P3-A18-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactNotification.java | Line: 11
Description: All 8 fields and their Lombok-generated accessors use snake_case naming in violation of Java conventions. No documentation justifies the deviation.
Fix: Add a class-level comment explaining the naming convention or refactor to camelCase.

[P3-A18-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java | Line: 8
Description: No documentation explains why a List<Impact> wrapper class exists rather than using the list directly. The wrapper pattern justification (serialization, JSON binding, etc.) is unknown.
Fix: Add class-level Javadoc explaining why the wrapper class exists and its intended use.

[P3-A18-12] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactNotification.java | Line: 7
Description: Lombok @Data generates toString() including email and mobile fields, which are PII. No documentation warns of PII exposure risk via toString() and no @ToString.Exclude is used.
Fix: Add @ToString.Exclude on email and mobile fields, or add class-level Javadoc warning about PII in toString output.

[P3-A19-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Manufacturer.java | Line: 5
Description: No class-level Javadoc on Manufacturer. There is no description of the class purpose, its role in the domain model, or any notes about serialization.
Fix: Add class-level Javadoc describing the Manufacturer entity and its relationships to other domain objects.

[P3-A19-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Manufacturer.java | Line: 14
Description: All four public accessor methods lack Javadoc. No @param, @return, or descriptive sentences exist on any method.
Fix: Add Javadoc to all public methods with @param and @return tags.

[P3-A19-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Manufacturer.java | Line: 7
Description: The serialVersionUID field carries an empty auto-generated Javadoc stub that implies documentation exists when it does not.
Fix: Remove the empty stub or replace with meaningful content.

[P3-A19-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/OfflineSessions.java | Line: 5
Description: No class-level Javadoc on OfflineSessions. The class aggregates Sessions and Result objects, but the concept of an "offline session" and the relationship between these types is entirely undocumented.
Fix: Add class-level Javadoc explaining what an offline session represents and the relationship between Sessions and Result.

[P3-A19-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/OfflineSessions.java | Line: 14
Description: All four public accessor methods lack Javadoc. The types Sessions and Result are non-primitive domain objects whose semantics require explanation.
Fix: Add Javadoc to all methods describing the contained domain objects and their relationships.

[P3-A19-6] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/OfflineSessions.java | Line: 7
Description: An empty auto-generated Javadoc stub on serialVersionUID provides no information while implying documentation coverage.
Fix: Remove the empty stub or replace with meaningful content.

[P3-A19-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java | Line: 15
Description: No class-level Javadoc on PackageEntry. The class represents a versioned software package with structured version parsing and implements Comparable, but its purpose, version string format, and field semantics are undocumented.
Fix: Add class-level Javadoc describing the package versioning model, expected version format, and Comparable contract.

[P3-A19-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java | Line: 57
Description: The compareTo method is undocumented and contains non-standard behavior: it returns 1 for null arguments (violating the Comparable contract that requires NullPointerException) and excludes the env field from comparison. Neither behavior is documented.
Fix: Add Javadoc documenting the comparison logic, the null-tolerance deviation from the Comparable contract, and which fields participate in ordering.

[P3-A19-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java | Line: 17
Description: All fields backing the Lombok-generated public accessors have no field-level Javadoc. The semantics of env (environment tag), pattern (compiled regex), and the version integer fields are not described.
Fix: Add field-level Javadoc to all fields describing their purpose, especially env and pattern.

[P3-A19-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java | Line: 28
Description: The @Builder annotation on a private constructor generates a public builder as the only intended construction path for parameterized instances. The expected format of the version parameter is not documented anywhere.
Fix: Add Javadoc or class-level documentation specifying the expected version string format accepted by the builder.

[P3-A19-11] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java | Line: 36
Description: The private initVersion method contains a non-obvious regex pattern with no inline or Javadoc comment explaining the group-index semantics. While private, the lack of documentation makes maintenance difficult.
Fix: Add an inline comment explaining the regex pattern and the meaning of each capture group.

[P3-A20-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Permissions.java | Line: 13
Description: No class-level Javadoc on Permissions. There is no explanation of what entity this class models, what database table or domain concept it corresponds to, or its relationship to drivers and companies.
Fix: Add class-level Javadoc describing the Permissions entity, its domain role, and relationships.

[P3-A20-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Questions.java | Line: 5
Description: No class-level Javadoc on Questions. The class name is plural but models a single question record, and there is no explanation of what expectedanswer represents in a forklift inspection context.
Fix: Add class-level Javadoc explaining the entity, addressing the plural naming, and describing the inspection question workflow.

[P3-A20-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java | Line: 5
Description: No class-level Javadoc on ReportLists. An inline comment "// subscription table" on line 10 is a remnant note about the backing table but is misplaced and carries no useful context about report generation or subscription management.
Fix: Add class-level Javadoc describing the entity purpose and its role in report scheduling/subscription management.

[P3-A20-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Questions.java | Line: 17
Description: All 16 public getter/setter methods across Questions and ReportLists have no Javadoc. No method describes return values, parameter constraints, or side effects for the public API consumed by service and DAO layers.
Fix: Add Javadoc to all public methods in both classes with @param and @return tags.

[P3-A20-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Permissions.java | Line: 17
Description: All Lombok-generated public methods and the builder entry point are undocumented. None of the six fields have Javadoc, so the entire generated public surface including the builder is undocumented.
Fix: Add field-level Javadoc to all fields so Lombok-generated methods have documentation context.

[P3-A20-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Permissions.java | Line: 27
Description: Field enabled is typed as String despite implying a boolean state. No documentation specifies valid values (Y/N, true/false, 1/0), the default state, or why boolean type was not used.
Fix: Add field-level Javadoc specifying valid string values for enabled, or refactor to a boolean type.

[P3-A20-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Permissions.java | Line: 29
Description: Field gsm_token has no documentation of its purpose, format, or security sensitivity. The @Data-generated toString will expose this token value in plain text.
Fix: Add field-level Javadoc describing the token purpose, format, and lifecycle. Add @ToString.Exclude to prevent exposure in logs.

[P3-A20-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Questions.java | Line: 7
Description: Empty auto-generated Javadoc stubs for serialVersionUID in both Questions and ReportLists provide no documentation while giving the appearance of coverage.
Fix: Remove the empty stubs or replace with meaningful content in both files.

[P3-A20-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java | Line: 7
Description: Empty Javadoc stub followed by misplaced inline comment "// subscription table" creates ambiguous and misleading documentation that visually associates the comment with serialVersionUID rather than the class.
Fix: Remove the empty stub, move the subscription table comment to a proper class-level Javadoc, and expand it with meaningful context.

[P3-A20-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java | Line: 19
Description: Public methods getComp_id, setComp_id, getFile_name, and setFile_name use snake_case violating Java bean naming conventions. This breaks standard introspection tools like Jackson and Spring MVC binding. The same pattern applies to Permissions.java fields.
Fix: Refactor to camelCase with @JsonProperty annotations for serialization compatibility, or add class-level documentation explaining the convention.

[P3-A20-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java | Line: 16
Description: Field frequency has no documentation of valid values or format. It likely accepts constrained values like DAILY, WEEKLY, or MONTHLY, but accepted values, case sensitivity, and behavior on unrecognized values are unspecified.
Fix: Add field-level Javadoc listing the valid frequency values or referencing the governing enum/constant class.

[P3-A20-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Questions.java | Line: 14
Description: Field expectedanswer deviates from camelCase naming (should be expectedAnswer) and has no documentation describing what values it holds in a forklift inspection context.
Fix: Rename to expectedAnswer or document the naming deviation, and add Javadoc describing valid answer values and matching semantics.

[P3-A20-13] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Permissions.java | Line: 13
Description: No documentation of the Serializable contract or serialVersionUID rationale in Permissions, Questions, or ReportLists. Why these classes are serializable and the consequences of structural changes are undocumented.
Fix: Add class-level Javadoc noting the serialization contract and the implications of modifying the class structure.

[P3-A21-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Reports.java | Line: 5
Description: No class-level Javadoc on Reports. The class purpose and the semantic meaning of its three fields (field, object, value) are entirely absent. The field named object is particularly ambiguous, shadowing the Java concept of Object.
Fix: Add class-level Javadoc describing the Reports entity and the domain meaning of field, object, and value.

[P3-A21-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Reports.java | Line: 16
Description: All six public accessor methods lack Javadoc. No @param, @return, or descriptive text is present on any method.
Fix: Add Javadoc to all public methods with @param and @return tags.

[P3-A21-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Reports.java | Line: 7
Description: The auto-generated Javadoc stub on serialVersionUID is empty and conveys no information, creating noise in documentation tooling.
Fix: Remove the empty stub or replace with meaningful content.

[P3-A21-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/ResponseWrapper.java | Line: 13
Description: No class-level Javadoc on ResponseWrapper, the primary API response envelope. The intended use of data vs metadata vs errors, the @JsonInclude(NON_NULL) serialization policy, and which endpoints use it are undocumented.
Fix: Add class-level Javadoc describing the response envelope structure, the serialization policy, and the contract for data, metadata, and errors.

[P3-A21-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/ResponseWrapper.java | Line: 18
Description: All Lombok-generated public methods are undocumented with no field-level Javadoc to compensate. The semantic contract of data, metadata, and errors fields is unknown.
Fix: Add field-level Javadoc describing each field's purpose, expected type, and nullability.

[P3-A21-6] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/ResponseWrapper.java | Line: 13
Description: The serialVersionUID Javadoc stub is placed on the same source line as the class opening brace, a structural formatting defect that renders incorrectly in documentation tools.
Fix: Reformat the stub to its own line and either remove it or replace with meaningful content.

[P3-A21-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Result.java | Line: 6
Description: No class-level Javadoc on Result. The domain meaning (inspection session result), the relationship to session_id, the format of time fields, and the purpose of arrAnswers are unknown without reading dependent code.
Fix: Add class-level Javadoc describing the Result entity, its relationship to sessions, and the role of arrAnswers.

[P3-A21-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Result.java | Line: 32
Description: Time fields start_time and finish_time are stored as String with no Javadoc documenting the expected format (ISO-8601, database timestamp, Unix epoch). Consumers must inspect database schemas or caller code to determine valid values.
Fix: Add field-level Javadoc specifying the expected date/time format and timezone convention.

[P3-A21-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Result.java | Line: 19
Description: All twelve public accessor methods on Result lack Javadoc. No @param, @return, or descriptive text is present on any method.
Fix: Add Javadoc to all public methods with @param and @return tags.

[P3-A21-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Result.java | Line: 8
Description: The auto-generated Javadoc stub on serialVersionUID is empty, identical to the same defect found across multiple model classes.
Fix: Remove the empty stub or replace with meaningful content.
[P3-A22-1] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Results.java | Line: 5
Description: The only class-level comment on Results is an inline comment with a typo, not a Javadoc comment. The class purpose as a serializable DTO for web service responses is entirely undocumented at the Javadoc level.
Fix: Add a class-level Javadoc comment describing the purpose of Results as a web service response DTO carrying a message ID and error string.

[P3-A22-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Results.java | Line: 16
Description: All four public methods (getMessage_id, setMessage_id, getError, setError) lack Javadoc. There is no documentation describing what message_id or error represent, nor any @param or @return tags.
Fix: Add Javadoc with @param and @return tags to all four accessor methods, documenting the format and semantics of message_id and error.

[P3-A22-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Roles.java | Line: 11
Description: The Roles class has no class-level Javadoc. The class models a role/authority entity using Lombok annotations that generate a substantial public API surface, but consumers have no guidance on its purpose or field semantics.
Fix: Add class-level Javadoc describing the purpose of Roles, its fields (id, name, authority, description), and how the Lombok-generated API surface should be used.

[P3-A22-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Roles.java | Line: 44
Description: The static factory method RoleId.fromId(String id) is entirely undocumented. It throws IllegalArgumentException if no match is found but has no @param, @return, or @throws tags. The exception message references "Name" instead of "ID", which is misleading.
Fix: Add Javadoc with @param id, @return, and @throws IllegalArgumentException tags to RoleId.fromId(). Fix the misleading exception message to reference "ID" instead of "Name".

[P3-A22-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Roles.java | Line: 31
Description: The inner enum RoleId and its constant ROLE_COMPANY_GROUP have no Javadoc. The enum's purpose as a type-safe representation of role identifier strings is undocumented.
Fix: Add Javadoc to the RoleId enum and its constants explaining the purpose and meaning of each role identifier.

[P3-A22-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Roles.java | Line: 9
Description: Lombok annotations @Data and @NoArgsConstructor generate a significant public API surface but none of the fields (id, name, authority, description) have Javadoc to carry through into generated accessor documentation.
Fix: Add field-level Javadoc to all four fields documenting their semantics, especially clarifying the distinction between name and authority.

[P3-A22-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Services.java | Line: 6
Description: The Services class has no class-level Javadoc. The domain meaning and units or conventions for its numeric fields (acc_hours, last_serv, next_serv, serv_duration) are entirely opaque to API readers.
Fix: Add class-level Javadoc describing the Services model as a forklift service record and documenting the units and conventions for all numeric fields.

[P3-A22-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Services.java | Line: 29
Description: The four public methods for BigDecimal fields acc_hours and service_due lack Javadoc. Without documentation, the precision, scale, and unit conventions for these values are unknown, risking incorrect service scheduling logic.
Fix: Add Javadoc to getAcc_hours, setAcc_hours, getService_due, and setService_due documenting the unit of measure, expected precision/scale, and relationship between the two values.

[P3-A22-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Services.java | Line: 47
Description: The six public methods for last_serv, next_serv, and serv_duration (all int) lack Javadoc. The unit of measure and the relationship between these fields are undocumented.
Fix: Add Javadoc documenting the unit of measure for each integer field and the relationship between last_serv, next_serv, and serv_duration.

[P3-A22-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Services.java | Line: 23
Description: The six public methods for driver_id, unit_id, and unit_name lack Javadoc. There is no documentation of whether IDs are internal surrogate keys or external references.
Fix: Add Javadoc with @return and @param tags documenting the nature and format of driver_id, unit_id, and unit_name.

[P3-A22-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Services.java | Line: 65
Description: The accessor pair for service_type lacks Javadoc. The valid values for this string field are not documented.
Fix: Add Javadoc documenting the valid values for service_type and whether it is a free-text label or constrained to an enumerated set.

[P3-A22-12] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/Results.java | Line: 9
Description: All three model files (Results.java, Roles.java, Services.java) contain auto-generated empty Javadoc stubs on the serialVersionUID field, indicating IDE-generated scaffolding was never reviewed.
Fix: Either remove the empty Javadoc stubs or replace them with meaningful content as part of a documentation review pass.

[P3-A23-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Sessions.java | Line: 5
Description: The Sessions class has no class-level Javadoc. There is no description of what a session represents in the domain, its lifecycle, field constraints, or format expectations for start_time/finish_time.
Fix: Add class-level Javadoc describing the Sessions domain model, its lifecycle, the expected format for time fields, and whether photo URL fields are optional.

[P3-A23-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Sessions.java | Line: 23
Description: All 20 public methods have no Javadoc. Critical semantic details are missing including the string format for start_time and finish_time, whether photo URL fields are nullable, and the domain meaning of unit_id versus driver_id.
Fix: Add Javadoc with @param and @return tags to all accessor methods, specifying string formats for temporal fields and nullability for URL fields.

[P3-A23-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Sessions.java | Line: 7
Description: The only Javadoc-style block comment in the file is an empty stub on serialVersionUID containing no content. It implies documentation was intended but never written.
Fix: Remove the empty Javadoc stub or replace it with meaningful content.

[P3-A23-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Types.java | Line: 5
Description: The Types class has no class-level Javadoc. The domain concept of a "type" is ambiguous and could refer to equipment types, incident types, or other classifications. Consumers cannot determine its intended use.
Fix: Add class-level Javadoc explaining what domain concept Types represents and how it is used in the forklift IQ system.

[P3-A23-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Types.java | Line: 16
Description: All 6 public methods have no Javadoc. The url field is semantically opaque without documentation, as it is unclear what kind of resource it represents.
Fix: Add Javadoc to all accessor methods, especially documenting what the url field represents (image URL, documentation link, etc.).

[P3-A23-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Types.java | Line: 7
Description: Empty auto-generated Javadoc stub on serialVersionUID with no content, providing no meaningful documentation value.
Fix: Remove the empty Javadoc stub or replace it with meaningful content.

[P3-A23-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Usage.java | Line: 6
Description: The Usage class has no class-level Javadoc. "Usage" is highly generic and there is no documentation indicating whether this represents fuel usage, operating-hour usage, battery charge, or another metric. The unit of measure for the BigDecimal field is undocumented.
Fix: Add class-level Javadoc describing what Usage represents, the unit of measure, and the significance of the BigDecimal type for the usage field.

[P3-A23-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Usage.java | Line: 16
Description: All 4 public methods have no Javadoc. The expected format of the time String field and the unit of measure, valid range, scale, and default-zero significance for the usage BigDecimal field are all undocumented.
Fix: Add Javadoc documenting the time field format, the usage field unit of measure, valid range, scale, and the meaning of the zero default.

[P3-A23-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Usage.java | Line: 8
Description: Empty auto-generated Javadoc stub on serialVersionUID with no content, consistent with the pattern in Sessions.java and Types.java.
Fix: Remove the empty Javadoc stub or replace it with meaningful content.

[P3-A23-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Usage.java | Line: 14
Description: The field usage shares its name with the enclosing class Usage, creating a naming collision that can confuse developers. The lack of documentation exacerbates the ambiguity.
Fix: Add field-level Javadoc distinguishing the field concept from the class concept, or rename the field to be more specific (e.g., usageValue).

[P3-A23-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Sessions.java | Line: N/A
Description: Public accessor methods across all three files use snake_case suffixes (e.g., getDriver_id, getStart_time) rather than standard Java camelCase, deviating from Java naming conventions with no documentation acknowledging the deviation.
Fix: Add a class-level or package-level Javadoc note explaining the naming convention (e.g., derived from database column names), or refactor to standard camelCase.

[P3-A23-12] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/Sessions.java | Line: N/A
Description: All three classes implement Serializable with explicit serialVersionUID values but there is no class-level Javadoc explaining the serialization purpose (session caching, HTTP response serialization, message queue payloads, etc.).
Fix: Add class-level Javadoc documenting the serialization purpose and contract for each class.

[P3-A24-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/User.java | Line: 13
Description: The User class has no class-level Javadoc. This is a core domain model representing an authenticated system user with security-sensitive fields (password, roles, active) whose lifecycle and security constraints are entirely undocumented.
Fix: Add class-level Javadoc describing User as an authenticated system user model, documenting security-sensitive fields, their constraints, and the intended lifecycle.

[P3-A24-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/User.java | Line: 41
Description: The only explicitly written public method addRoles(Roles role) has no Javadoc. There is no documentation on null-safety or that duplicate roles are silently ignored due to HashSet semantics.
Fix: Add Javadoc with @param tag documenting null-safety, duplicate handling via HashSet semantics, and the method's behavior.

[P3-A24-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/User.java | Line: 17
Description: None of the domain model fields carry Javadoc. The password field's storage format, the active field's meaning, and the roles field's default initialization to an empty HashSet are undocumented.
Fix: Add field-level Javadoc documenting the password storage format, active field semantics, and roles initialization behavior.

[P3-A24-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/UserResponse.java | Line: 13
Description: The UserResponse class has no class-level Javadoc. It is undocumented which API endpoint or external system populates this DTO or what the @JsonInclude(NON_NULL) policy implies for API consumers.
Fix: Add class-level Javadoc describing the API endpoint this DTO serves, the external system that populates it, and the implications of the NON_NULL inclusion policy.

[P3-A24-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/UserResponse.java | Line: 15
Description: The serialVersionUID field carries an empty Javadoc stub that suggests documentation exists when it does not. An empty Javadoc block is worse than no Javadoc because it implies intentional documentation was left incomplete.
Fix: Remove the empty Javadoc stub or replace it with meaningful content.

[P3-A24-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/UserResponse.java | Line: 19
Description: None of the eight response fields carry Javadoc. The temporal fields userCreateDate and lastModifiedDate are typed as String with no documented format. The distinction between username and name/lastname is ambiguous.
Fix: Add field-level Javadoc documenting the expected format for date string fields and clarifying the distinction between username, name, and lastname.

[P3-A24-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterException.java | Line: 4
Description: APKUpdaterException has no class-level Javadoc. There is no description of the conditions under which it is thrown, which component raises it, or what consumers should do when they catch it.
Fix: Add class-level Javadoc documenting the exception's purpose, the conditions that trigger it, and the expected handling approach for callers.

[P3-A24-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterException.java | Line: 5
Description: The single-argument constructor has no Javadoc. There is no @param message tag and no guidance on expected message format or content.
Fix: Add Javadoc with @param message tag documenting the expected message format and content conventions.

[P3-A24-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterException.java | Line: 9
Description: The two-argument constructor has no Javadoc. There is no @param message or @param cause tag, and no description distinguishing when this constructor should be preferred over the single-argument form.
Fix: Add Javadoc with @param tags for both parameters and a description of when to use the cause-wrapping constructor.

[P3-A24-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/User.java | Line: 33
Description: The @Builder annotation generates a public User.UserBuilder class, but nothing in the source documents the builder's intended use, required fields, or invariants such as whether email must be unique or non-null.
Fix: Add documentation on the builder pattern usage, required fields, and any invariants that must hold before calling build().

[P3-A25-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 31
Description: Hardcoded AWS credentials (access key ID and secret access key) are embedded as string literals in a static field initializer with no documentation indicating they are placeholders or referencing externalized credential configuration. The credentials must be treated as compromised.
Fix: Immediately rotate the compromised AWS credentials. Remove hardcoded credentials and replace with externalized configuration (e.g., AWS SDK default credential chain, environment variables, or AWS Secrets Manager). Add documentation for the credential configuration mechanism.

[P3-A25-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 45
Description: loadImageAsResource(String fileName) is a public method that unconditionally returns null with no Javadoc, no @deprecated tag, no TODO, and no explanation. Null returns without documentation will cause NullPointerException at call sites.
Fix: Either implement the method properly or add @deprecated annotation with Javadoc explaining the stub status and expected timeline for implementation. At minimum add a TODO comment.

[P3-A25-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java | Line: 28
Description: getAvailablePackage(String baseUrl, String pkgName, String currentVersion) has no Javadoc. This non-trivial public method with three parameters, an Optional return type, and two exception pathways is entirely undocumented.
Fix: Add Javadoc with @param, @return, and @throws tags documenting all three parameters, the Optional return semantics, and both exception pathways.

[P3-A25-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java | Line: 54
Description: loadPackageAsResource(String pkgname, String version) has no Javadoc. The method throws two different custom exceptions, neither documented. The expected filename format is undocumented.
Fix: Add Javadoc with @param, @return, and @throws tags documenting the expected filename format and both exception types.

[P3-A25-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java | Line: 53
Description: saveImage(InputStream inputStream) in the abstract base class has no Javadoc. The method has undocumented side effects writing to protected instance fields targetLocation and fileName that subclasses depend on, creating a hidden coupling invisible to subclass authors.
Fix: Add Javadoc documenting the side effects on targetLocation and fileName fields, the contract for subclasses, @param inputStream, @return, and @throws tags.

[P3-A25-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 38
Description: saveImage(InputStream inputStream) override has no Javadoc. The behavioral addition of AWS S3 upload is not described anywhere.
Fix: Add Javadoc documenting the S3 upload behavior added by this override, with @param, @return, and @throws tags.

[P3-A25-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java | Line: 43
Description: initialize(), annotated @PostConstruct, has no Javadoc. The lifecycle semantics and failure mode (throws FileStorageException) are undocumented.
Fix: Add Javadoc documenting the @PostConstruct lifecycle, the directory creation behavior, and the FileStorageException failure mode.

[P3-A25-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java | Line: 19
Description: No class-level Javadoc on APKUpdaterService. The purpose, dependency on the packageDir configuration property, and expected filename convention are undocumented.
Fix: Add class-level Javadoc describing the service purpose, the required packageDir configuration property, and the expected APK filename convention.

[P3-A25-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 24
Description: No class-level Javadoc on AWSFileStorageService. The purpose, required configuration properties (cloudImagedDir, bucketName), and hardcoded AWS region (US_EAST_1) are undocumented.
Fix: Add class-level Javadoc describing the S3 storage implementation, required configuration properties, and the hardcoded AWS region.

[P3-A25-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java | Line: 23
Description: No class-level Javadoc on AbstractFileStorageService. The shared image-storage lifecycle, configuration properties consumed, and contract imposed on subclasses are undocumented.
Fix: Add class-level Javadoc describing responsibilities, configuration properties (uploadDir, imageDir, imagePrefix), and the subclass contract.

[P3-A25-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 58
Description: Inline comments describing the uploadObject method parameters use incorrect identifiers. Comments reference bucketName, key, and file, but actual parameter names are key_name and file_path. These comments are misleading.
Fix: Correct the inline comments to match the actual parameter names, or replace them with proper Javadoc using accurate parameter references.

[P3-A25-12] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java | Line: 34
Description: Six protected fields (imageStorageLocation, targetLocation, fileName, imageExt, uploadDir, imageDir) have no documentation. These fields form part of the subclass API surface but their semantics, lifecycle, and mutability constraints are undocumented.
Fix: Add Javadoc to all six protected fields documenting their intended semantics, which lifecycle method initializes them, and mutability constraints.

[P3-A25-13] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 25
Description: The @Value property key cloudImagedDir contains a typographic error ("Imaged" instead of "Image") with no comment documenting this as intentional or noting the discrepancy.
Fix: Correct the property key to cloudImageDir in both the code and the configuration file, or add a comment explaining the intentional naming.

[P3-A25-14] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java | Line: 25
Description: The compiled Pattern field used to parse APK filenames is entirely undocumented. The regex and expected filename format are not described.
Fix: Add a Javadoc or inline comment on the pattern field describing the expected APK filename format and the named capture groups.

[P3-A25-15] INFO | File: src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java | Line: 23
Description: The class is declared with package-private visibility yet implements a presumably public interface. The intentional scoping decision is undocumented.
Fix: Add a comment or Javadoc note explaining the deliberate choice of package-private visibility.

[P3-A26-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/BootstrapService.java | Line: 16
Description: Neither BootstrapService nor the inner class FlywayBean has class-level Javadoc. The purpose of conditionally bootstrapping Flyway database migrations, the two controlling properties (flyway.enabled, flyway.baseline), and the non-obvious FlywayBean wrapper pattern are entirely undocumented.
Fix: Add class-level Javadoc to both BootstrapService and FlywayBean describing the conditional migration bootstrapping, the controlling properties, and the wrapper pattern for Spring initMethod.

[P3-A26-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/BootstrapService.java | Line: 28
Description: No Javadoc on the sole @Bean method getFlyway(). The conditional logic gated on flyway.enabled, the automatic invocation of migrate() via initMethod, and the silent skip behavior when disabled are all undocumented.
Fix: Add Javadoc documenting the conditional bean creation logic, the initMethod lifecycle, and the behavior when Flyway is disabled.

[P3-A26-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/BootstrapService.java | Line: 51
Description: No Javadoc on migrate(). The method declares throws FlywayException and returns an int, but there are no @return or @throws descriptions. The dual semantics of return value 0 (zero migrations applied vs. Flyway disabled) are a correctness documentation gap.
Fix: Add Javadoc with @return and @throws tags, explicitly documenting the dual semantics of a zero return value.

[P3-A26-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/BootstrapService.java | Line: 44
Description: Both FlywayBean constructors are public and undocumented. The no-arg constructor produces a disabled/no-op state but this is not indicated by its signature or any comment.
Fix: Add Javadoc to both constructors, especially documenting that the no-arg constructor produces a no-op FlywayBean.

[P3-A26-5] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: 25
Description: No class-level or method-level Javadoc anywhere in CognitoService. The getUser method appends the accessToken as a plain query-string parameter in the URL, exposing it in server access logs, browser history, and HTTP referrer headers. There is no security warning documentation.
Fix: Move the accessToken from the URL query string to an Authorization header. Add class and method-level Javadoc with an @apiNote or @implNote warning about token handling. Document the security implications.

[P3-A26-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: 69
Description: No Javadoc on authenticationRequest(). The method is public but functions as an internal helper. The silent-failure contract (returns empty AuthenticationResponse on any exception rather than throwing) is undocumented.
Fix: Reduce visibility to private or package-private. Add Javadoc documenting @return, the silent-failure contract, and the intended caller scope.

[P3-A26-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: 30
Description: No Javadoc on getUser(String username). Missing @param username, @return description, and the silent-failure contract where any exception results in an empty UserResponse rather than throwing.
Fix: Add Javadoc with @param, @return, and documentation of the silent-failure contract so callers can distinguish a valid empty response from an error.

[P3-A26-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/DriverAlreadyExistException.java | Line: 3
Description: No class-level or constructor-level Javadoc on the exception class. The semantic meaning (a driver record already exists), which service throws it, and the unchecked exception hierarchy are undocumented.
Fix: Add class-level Javadoc documenting the exception semantics, the throwing service, and the inheritance chain. Add constructor Javadoc with @param tags.

[P3-A26-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/BootstrapService.java | Line: 55
Description: When Flyway is disabled, the migrate() method uses System.out.println rather than SLF4J with no documentation explaining the choice, leaving the intent ambiguous for maintainers.
Fix: Replace System.out.println with SLF4J logging for consistency, or add an @implNote comment explaining the deliberate choice.

[P3-A26-10] INFO | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: 54
Description: Log messages contain a misspelling "HttpStatus Succuss" (should be "Success") in both methods, indicating logging statements were never reviewed.
Fix: Correct the spelling in log messages to "HttpStatus Success".

[P3-A27-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 27
Description: The DriverService class has no class-level Javadoc. This Spring @Service implements core business logic for authentication, driver registration, and password reset, but its purpose, responsibilities, and transactional scope are undocumented.
Fix: Add class-level Javadoc describing the service purpose, responsibilities, transactional scope, and collaborating DAOs.

[P3-A27-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 52
Description: The authenticate(String email, String password) method has no Javadoc. Parameters, return value (Optional<Driver>), the side-effect of updating last login time, and the exception pathway are all undocumented. The method is also @Deprecated without a corresponding @deprecated Javadoc tag.
Fix: Add Javadoc with @param, @return, @throws, and @deprecated tags documenting all behaviors, side effects, and the deprecation reason with replacement guidance.

[P3-A27-3] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 51
Description: The @Deprecated annotation on authenticate is not accompanied by a @deprecated Javadoc tag, no @see reference to a replacement, and no explanation of why the method was deprecated. This actively misleads consumers about the method's state.
Fix: Add a @deprecated Javadoc tag explaining the reason for deprecation and providing a @see reference to the replacement authentication mechanism.

[P3-A27-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 66
Description: registerDriver(Driver driver) has no Javadoc. Significant undocumented behavior includes throwing DriverAlreadyExistException for duplicate emails, conditionally creating a Company entity, sending a confirmation email as a side effect, and returning a mutated Driver object.
Fix: Add Javadoc with @param, @return, and @throws tags documenting the duplicate check, conditional company creation, email side effect, and the mutated return object.

[P3-A27-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 99
Description: resetPassword(Driver driver) has no Javadoc. The throws DriverServiceException clause, the side effect of sending a plaintext password email, and the password generation mechanism are undocumented.
Fix: Add Javadoc with @param, @throws, and documentation of the password reset email side effect and generation mechanism.

[P3-A27-6] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 37
Description: The Javadoc on PASSWORD_LENGTH contains a @see tag referencing the private method generateRandomPassword(), which is non-functional in generated Javadoc. The more appropriate reference would be the public method resetPassword.
Fix: Change the @see reference from generateRandomPassword() to resetPassword(Driver) so it resolves in generated Javadoc.

[P3-A27-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/DriverServiceException.java | Line: 3
Description: The DriverServiceException class has no class-level Javadoc. As a public exception type in the service API, consumers need to understand when it is thrown, what conditions it represents, and whether it is recoverable.
Fix: Add class-level Javadoc documenting the exception's purpose, the conditions it represents, and recoverability guidance.

[P3-A27-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/DriverServiceException.java | Line: 5
Description: Both public constructors of DriverServiceException have no Javadoc. The message and cause parameters are undocumented.
Fix: Add Javadoc with @param tags to both constructors documenting the expected message content and cause usage.

[P3-A27-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/EntityNotFoundException.java | Line: 7
Description: EntityNotFoundException has no class-level Javadoc. This exception is annotated with @ResponseStatus(HttpStatus.NOT_FOUND) and directly influences HTTP response behavior, but the HTTP semantics and usage pattern are undocumented.
Fix: Add class-level Javadoc documenting the HTTP 404 mapping, the types of entities whose absence triggers this exception, and the intended usage pattern.

[P3-A27-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/EntityNotFoundException.java | Line: 9
Description: The single public constructor has no Javadoc. The message parameter, which typically becomes part of the HTTP response body, is undocumented.
Fix: Add Javadoc with @param message tag documenting the expected content and its role in the HTTP response body.

[P3-A28-1] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/FileNotFoundException.java | Line: 7
Description: No class-level Javadoc on FileNotFoundException. The class carries @ResponseStatus(HttpStatus.NOT_FOUND) making its HTTP contract significant, but when it is thrown and its HTTP 404 mapping are undocumented.
Fix: Add class-level Javadoc documenting the HTTP 404 mapping, when the exception is thrown, and that it is an unchecked exception.

[P3-A28-2] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/FileNotFoundException.java | Line: 9
Description: No Javadoc on constructor FileNotFoundException(String message). The message parameter is undocumented with no @param tag.
Fix: Add Javadoc with @param message tag describing the intended content.

[P3-A28-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/FileStorageException.java | Line: 3
Description: No class-level Javadoc on FileStorageException. As the base exception for the file storage subsystem, its purpose, hierarchy, and the category of errors it represents are undocumented.
Fix: Add class-level Javadoc documenting the exception's role as the base for file storage errors and its position in the exception hierarchy.

[P3-A28-4] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/FileStorageException.java | Line: 7
Description: No Javadoc on constructor FileStorageException(String message). The message parameter is undocumented.
Fix: Add Javadoc with @param message tag.

[P3-A28-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/FileStorageException.java | Line: 11
Description: No Javadoc on constructor FileStorageException(String message, Throwable cause). Both parameters are undocumented. This cause-wrapping constructor is important for diagnostic purposes.
Fix: Add Javadoc with @param tags for both message and cause, documenting when to use the cause-wrapping form.

[P3-A28-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/FileStorageService.java | Line: 7
Description: No class-level Javadoc on the public FileStorageService interface. This is the primary service contract for file storage operations but has no specification of the overall contract, expected implementations, threading guarantees, or lifecycle considerations.
Fix: Add interface-level Javadoc describing the file storage contract, known implementations, threading guarantees, and lifecycle considerations.

[P3-A28-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/FileStorageService.java | Line: 8
Description: No Javadoc on saveImage(InputStream inputStream). There is no @param documenting stream expectations or closure behavior, no @return documenting what the returned String represents, and no @throws documentation.
Fix: Add Javadoc with @param (format, nullability, stream closure), @return (what the String represents), and @throws tags.

[P3-A28-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/FileStorageService.java | Line: 10
Description: No Javadoc on loadImageAsResource(String fileName). There is no @param documenting the expected format, no @return documenting the Resource, and no @throws specifying that FileNotFoundException is thrown when absent.
Fix: Add Javadoc with @param (expected format, relationship to saveImage return value), @return, and @throws tags.

[P3-A29-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/LocalFileStorageService.java | Line: 13
Description: The LocalFileStorageService class has no class-level Javadoc. Its purpose as the local-filesystem implementation of FileStorageService and its Spring bean qualifier name are undocumented.
Fix: Add class-level Javadoc describing the class as the local filesystem implementation, its Spring bean name, and how it differs from other storage backends.

[P3-A29-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/LocalFileStorageService.java | Line: 16
Description: The sole public method loadImageAsResource has no Javadoc. There is no @param, @return, or @throws for FileNotFoundException or FileStorageException. Both exceptions are undiscoverable without reading the implementation.
Fix: Add Javadoc with @param fileName, @return, and @throws tags for both FileNotFoundException and FileStorageException.

[P3-A29-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/SaveFileInfo.java | Line: 10
Description: The SaveFileInfo class has no class-level Javadoc. Its role as a DTO for file-save response payloads and the context in which it is constructed are undocumented.
Fix: Add class-level Javadoc describing SaveFileInfo as a file upload response DTO and the context in which it is used.

[P3-A29-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/SaveFileInfo.java | Line: 14
Description: None of the four fields carry Javadoc. The semantic distinctions between fileName and fileDownloadUri are not documented. The unit of size (bytes implied but not stated) is undocumented.
Fix: Add field-level Javadoc documenting the semantics of each field, especially distinguishing fileName from fileDownloadUri and stating the unit of size.

[P3-A29-5] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java | Line: 26
Description: The loadUserByUsername method has no Javadoc. This is the primary security authentication entry point. The parameter accepts either a plaintext username or its MD5 hash. The returned UserDetails principal name is the email field, not the username argument, creating an undocumented identity transformation. Declared exceptions UsernameNotFoundException and DataAccessException are undocumented.
Fix: Add Javadoc with @param (noting MD5 hash acceptance), @return (noting the email-as-principal transformation), @throws for both exceptions, and a note about the @Transactional(readOnly) behavior.

[P3-A29-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java | Line: 20
Description: The UserDetailsServiceImpl class has no class-level Javadoc. Its role as the Spring Security UserDetailsService implementation, its dependency on UserDAO, and the database-backed authentication model are undocumented.
Fix: Add class-level Javadoc describing the Spring Security integration, the database-backed authentication model, the UserDAO dependency, and the bean qualifier name.

[P3-A29-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java | Line: 38
Description: The private buildUserFromUserEntity method hardcodes enabled=true, accountNonExpired=true, and credentialsNonExpired=true with no documentation. Callers of loadUserByUsername have no way to know that account expiry and credential expiry are not enforced.
Fix: Document in the loadUserByUsername Javadoc that account expiry and credential expiry checks are not enforced (always true), and add inline comments on the hardcoded values in buildUserFromUserEntity.

[P3-A29-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/FileStorageService.java | Line: 8
Description: The FileStorageService interface methods saveImage and loadImageAsResource have no Javadoc. Interface-level Javadoc is the canonical location for contract documentation that @Override implementations inherit.
Fix: Add Javadoc to the interface methods so implementations inherit the contract documentation.

[P3-A30-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 29
Description: The Javadoc on downloadFile documents only two of three parameters (fileURL and saveDir). The first parameter fileName has no @param entry. Additionally, the method internally overrides fileName in most execution paths, making the parameter's role misleading without documentation.
Fix: Add the missing @param fileName entry and document that the parameter value may be overridden by Content-Disposition header or URL-derived filename.

[P3-A30-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 29
Description: The Javadoc declares @throws IOException but the stream-handling block catches all exceptions silently via printStackTrace. The declared exception only covers connection-level errors, making the Javadoc inaccurate regarding the actual exception contract.
Fix: Correct the @throws documentation to accurately describe which exceptions are propagated versus suppressed, or fix the exception handling to propagate stream errors as declared.

[P3-A30-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 98
Description: sendPost(String fname, String input, String saveDir) has no Javadoc. The URL construction from RuntimeConfig.APIURL, the hardcoded X-AUTH-TOKEN header, file output behavior, and exception suppression are all entirely undocumented.
Fix: Add Javadoc with @param tags for all three parameters, documenting the RuntimeConfig dependency, authentication token, file output location, and exception handling behavior.

[P3-A30-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/DateUtil.java | Line: 43
Description: parseDateTimeWithSlashes(String oldDateString) has no Javadoc. The method performs a non-obvious two-step format conversion that swaps month and day positions, which is entirely undocumented and will surprise callers.
Fix: Add Javadoc documenting the month/day transposition behavior, expected input format (MM/dd/yyyy HH:mm:ss), and output format.

[P3-A30-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/DateUtil.java | Line: 49
Description: getStartDate(Date date, String frequency) has no Javadoc. The accepted frequency values (Daily, Weekly, Monthly) are undocumented. Invalid values silently default to -1 day, which is undocumented behavior.
Fix: Add Javadoc documenting the accepted frequency values, the computation for each, and the silent default behavior for unrecognized values.

[P3-A30-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/DateUtil.java | Line: 35
Description: All seven public methods in DateUtil lack Javadoc. No class-level Javadoc is present. Parameters, return values, thrown exceptions, and expected date formats are entirely undocumented.
Fix: Add Javadoc to all public methods documenting parameters, return values, date format expectations, and thrown exceptions. Add class-level Javadoc.

[P3-A30-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 158
Description: All four public accessor/mutator methods (getSaveFilePath, setSaveFilePath, getFileName, setFileName) lack Javadoc. The fields they access are mutable static state, meaning concurrent calls will overwrite values. This thread-safety implication is undocumented.
Fix: Add Javadoc to all four methods documenting their purpose and adding a thread-safety warning about the static mutable state.

[P3-A30-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/Configuration.java | Line: 1
Description: No class-level Javadoc and no field-level documentation. The purpose of configuration values, property key bindings, and sensitivity of fields such as cognitoAPIPassword are not documented.
Fix: Add class-level Javadoc describing the configuration component and add field-level Javadoc noting the property keys and sensitivity of credential fields.

[P3-A30-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/Configuration.java | Line: 3
Description: Unused imports for org.simpleframework.xml.Element and org.simpleframework.xml.Root with no comment explaining whether this is reserved for future use or accidental dead code.
Fix: Remove the unused imports or add a comment explaining their intended future use.

[P3-A30-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 19
Description: No class-level Javadoc on HttpDownloadUtility. The class purpose, thread-safety contract for static mutable state, and relationship to RuntimeConfig are undocumented.
Fix: Add class-level Javadoc describing the utility's purpose, thread-safety limitations, and RuntimeConfig dependency.

[P3-A30-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/DateUtil.java | Line: 10
Description: No class-level Javadoc on DateUtil. The date formats used, timezone assumptions (JVM default), and per-call SimpleDateFormat instantiation are undocumented.
Fix: Add class-level Javadoc documenting supported date formats, timezone assumptions, and thread-safety characteristics.

[P3-A30-12] INFO | File: src/main/java/com/journaldev/spring/jdbc/util/DateUtil.java | Line: 14
Description: The private parseDate method uses StringUtils.isEmpty(String) from Spring which is deprecated as of Spring 5.3. No comment notes this deprecation or the intended migration path.
Fix: Replace StringUtils.isEmpty with the recommended alternative (e.g., ObjectUtils.isEmpty or StringUtils.hasLength) and add a note if keeping the deprecated usage temporarily.

[P3-A31-1] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/RuntimeConf.java | Line: 3
Description: The RuntimeConf class has no Javadoc. Its purpose of providing a runtime-accessible JNDI datasource name constant is undocumented.
Fix: Add class-level Javadoc describing the purpose of RuntimeConf as a holder for the JNDI datasource name constant.

[P3-A31-2] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/RuntimeConf.java | Line: 4
Description: The public static field database has no Javadoc. As a mutable public static field, its expected format, valid values, and whether mutation is intended or safe are undocumented.
Fix: Add Javadoc to the database field documenting its purpose, expected format, and whether it should be treated as immutable. Consider making it final if mutation is not intended.

[P3-A31-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/SMTPAuthenticator.java | Line: 5
Description: The SMTPAuthenticator class has no class-level Javadoc. There is no documentation explaining that it supplies hardcoded SMTP credentials or directing maintainers to an alternative configuration mechanism.
Fix: Add class-level Javadoc describing the authenticator's purpose and noting the need to externalize credentials.

[P3-A31-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/SMTPAuthenticator.java | Line: 7
Description: The overridden public method getPasswordAuthentication() has no Javadoc. No documentation warns that credentials are hardcoded, making it non-obvious that this method is the sole place credentials reside.
Fix: Add Javadoc with a warning that credentials are currently hardcoded and should be externalized to configuration.

[P3-A31-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/SendEmail.java | Line: 13
Description: The SendEmail class has no class-level Javadoc. The JNDI session lookup dependency, RuntimeConfig.mailFrom requirement, and threading/scope model are undocumented.
Fix: Add class-level Javadoc describing the JNDI dependency (mail/Session), the RuntimeConfig.mailFrom precondition, and threading considerations.

[P3-A31-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/SendEmail.java | Line: 14
Description: The sendMail(String subject, String msg, String mailTo) method has no Javadoc. The HTML content expectation for msg, comma-separated address support for mailTo, silent exception swallowing, and JNDI precondition are all undocumented.
Fix: Add Javadoc with @param tags documenting the HTML content expectation, multi-address support, silent-failure behavior, and the JNDI precondition.

[P3-A31-7] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/SMTPAuthenticator.java | Line: 9
Description: Hardcoded AWS IAM credentials appear in plain source code with no documentation warning that these are sensitive values or that they should be replaced by an environment/configuration-based mechanism. The documentation deficiency makes the security risk invisible to future developers.
Fix: Remove hardcoded credentials and externalize them to environment variables or a secrets manager. Add Javadoc documenting the credential configuration mechanism and security requirements.

[P3-A32-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 36
Description: The sole public method init(String msg, String mobile_no) has no Javadoc. It performs JNDI datasource lookup, database connection, SMS dispatch delegation, and resource cleanup, none of which is documented.
Fix: Add Javadoc with @param tags for msg and mobile_no, documenting the JNDI dependency, database connection lifecycle, SMS dispatch behavior, and resource cleanup.

[P3-A32-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 78
Description: The Javadoc on send_sms_message() states "This function is responsible for sending out email" when the method actually sends SMS messages via an HTTP-based SMS gateway. This is a direct factual contradiction that would actively mislead any reader.
Fix: Rewrite the Javadoc to accurately describe the method as sending SMS messages via an HTTP-based SMS gateway, not email.

[P3-A32-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 78
Description: All @param tags in the Javadoc use PHP syntax (@param integer $id, @param string $mobile_no) which is invalid Java Javadoc. The tags document parameters that do not exist in the Java method signature. The actual Java parameters (msg, mobile_no) are not documented.
Fix: Replace PHP-style @param tags with valid Java Javadoc @param tags matching the actual method parameters msg and mobile_no.

[P3-A32-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 78
Description: The method declares throws SQLException, IOException but the Javadoc contains no @throws tags. Callers cannot determine from the documentation which checked exceptions may propagate.
Fix: Add @throws SQLException and @throws IOException tags documenting the conditions under which each exception is thrown.

[P3-A32-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 36
Description: sendMail() is a public static utility method with 8 parameters and no Javadoc. The semantics of rName vs sName, the expected format of attachment, and the fact that the method unconditionally returns true regardless of success or failure are all undocumented.
Fix: Add Javadoc with @param tags for all 8 parameters, @return documenting the always-true return behavior, and document the email sending mechanism.

[P3-A32-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 27
Description: generateRadomName() has no Javadoc. The format of the generated name (timestamp prefix followed by UUID) and intended use for unique resource naming are undocumented.
Fix: Add Javadoc documenting the generated name format, intended use, and uniqueness guarantees.

[P3-A32-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 25
Description: The SendMessage class has no class-level Javadoc. Its purpose, lifecycle expectations for instance-level JDBC resources held as fields, and threading constraints are undocumented.
Fix: Add class-level Javadoc describing the class purpose, JDBC resource lifecycle, and threading constraints.

[P3-A32-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 24
Description: The Util class has no class-level Javadoc. Its role as a static utility class for email dispatch and name generation is undocumented.
Fix: Add class-level Javadoc describing the utility class purpose and its static utility method design.

[P3-A32-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 39
Description: Three lines of commented-out code performing a JNDI mail session lookup are present with no explanatory comment about why the approach was abandoned or whether it is intended to be re-enabled.
Fix: Remove the commented-out code or add a comment explaining why the JNDI approach was abandoned and whether it may be restored.

[P3-A32-10] INFO | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 27
Description: The method name generateRadomName contains a spelling error ("Radom" instead of "Random"). No Javadoc, @deprecated annotation, or inline comment acknowledges the typo, which is silently propagated to all call sites.
Fix: Rename the method to generateRandomName and update all call sites, or add a correctly-named wrapper method and deprecate the misspelled one.

---

## Pass 4 — Code Quality

[P4-A01-1] MEDIUM | File: `src/main/java/com/journaldev/spring/jdbc/DAO/APIDAO.java` (entire file), `src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java` (entire file) | Line: N/A
Description: Neither APIDAO nor APIDAOImpl nor the Spring bean apiDao is referenced anywhere outside these two files.
Fix: Should be removed to reduce confusion and context-scan noise

[P4-A01-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: 28-34
Description: The checkKey method logs the provided key and unconditionally returns true without performing any actual key validation.
Fix: Review and remediate the identified issue

[P4-A01-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: 30
Description: Line 30 contains a commented-out SQL INSERT statement: //String sql = "INSERT INTO CUSTOMER (CUST_ID, NAME, AGE) VALUES (?, ?, ?)";.
Fix: Should be removed

[P4-A01-4] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: 37
Description: The log message reads "Start checkKey for : {}" but the method is findByName. This is a copy-paste error from checkKey() that would make log analysis confusing when debugging.
Fix: Should reference findByName

[P4-A01-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: 40
Description: getJdbcTemplate().queryForObject(sql, Driver.class, username) uses the queryForObject(String, Class<T>, Object...) overload which expects a SingleColumnRowMapper.
Fix: Review and remediate the identified issue

[P4-A01-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: 38
Description: The method is named findByName and accepts a parameter called username, but the SQL query is select * from tblusers where md5(email) = ?.
Fix: Should reflect what the query actually does

[P4-A01-7] INFO | File: src/main/java/com/journaldev/spring/jdbc/DAO/APIDAOImpl.java | Line: 17
Description: The class-level @Transactional(readOnly = true) annotation applies to all methods, but checkKey() does not interact with the database at all, and findByName() queries tblusers which is a different table/view than what CompanyDAO uses.
Fix: Review and remediate the identified issue

[P4-A01-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 11-12
Description: BeanPropertyRowMapper (line 11) and JdbcTemplate (line 12) are imported but never used directly in the file.
Fix: Should be removed

[P4-A01-9] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 139-157
Description: In CompanyResultResetExtractor.extractData(), if the ResultSet is empty (no rows), the while loop never executes, cie remains null, and line 154 (cie.setArrRoles(roles)) will throw a NullPointerException.
Fix: Should guard against cie == null before calling setArrRoles

[P4-A01-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 98-134
Description: In CompaniesResultResetExtractor, when the result set contains only one company, previousCompanyId starts as null and companyId != previousCompanyId is always true on the first row (due to Long object comparison via !=).
Fix: Should use !companyId.equals(previousCompanyId)

[P4-A01-11] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 41
Description: The SQL insert into company ... md5(?) uses the PostgreSQL md5() function to hash the password. MD5 is cryptographically broken and unsuitable for password storage.
Fix: Should use bcrypt, scrypt, or Argon2

[P4-A01-12] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 36-50
Description: The save() method performs four distinct database operations (sequence fetch, company insert, role-relation inserts in a loop, permission insert).
Fix: Should be checked to see if a transaction is managed upstream, but at the DAO level this is a gap

[P4-A01-13] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 42, 47, 67, 80, 92
Description: Multiple calls use the new Object[] { ... } form to pass parameters to JdbcTemplate methods (e.g., getJdbcTemplate().update(sql, new Object[] {...})).
Fix: Use the new Object[] { ... } form to pass parameters to JdbcTemplate methods (e.g., getJdbcTemplate().update(sql, new Object[] {...}))

[P4-A01-14] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 98, 136
Description: The inner classes are named CompaniesResultResetExtractor and CompanyResultResetExtractor. The word "Reset" appears to be a typo for "Result" (as in "ResultSet Extractor").
Fix: Review and remediate the identified issue

[P4-A01-15] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/CompanyDAO.java | Line: 160-195
Description: The mapCompany method accesses Driver fields by column name (e.g., rs.getString("first_name")) but accesses Company fields by column index (e.g., rs.getLong(1), rs.getString(2)).
Fix: Should use named columns for maintainability

[P4-A02-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 66
Description: The update() method's SQL WHERE clause references iduser (where iduser = ?), while every other method in the class and the table's schema (inferred from save() at line 55 and updateLastLoginTime() at line 80) use id as the primary key column name.
Fix: Use id as the primary key column name

[P4-A02-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/EmailLayoutDAO.java | Line: 21-28
Description: The method accepts a type parameter but never uses it. It creates a new EmailLayout(), executes no query, populates no fields, and returns the empty object.
Fix: Review and remediate the identified issue

[P4-A02-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAO.java | Line: 21-22
Description: The interface method is annotated @Deprecated but provides no since or forRemoval attributes (Java 9+), no @deprecated Javadoc tag, and no indication of the replacement API.
Fix: Use this method with no compiler deprecation warning from the implementation side

[P4-A02-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 27, 142
Description: BASE_QUERY_DRIVER already includes inner join permission p on p.driver_id = d.id and p.enabled = true (line 27).
Fix: Use is updated but not the other

[P4-A02-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 110, 130, 146, 157
Description: Multiple calls to getJdbcTemplate().queryForObject() and getJdbcTemplate().query() use the explicit new Object[]{...} form (e.g., line 110: new Object[]{url, userId}).
Fix: Should be migrated to the varargs form or the newer queryForObject(sql, rowMapper, args...) signature

[P4-A02-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/EmailLayoutDAO.java | Line: 11-13
Description: Unlike DriverDAOImpl which uses @Repository and Lombok @Slf4j, EmailLayoutDAO is a plain class with manual LoggerFactory.getLogger().
Fix: Review and remediate the identified issue

[P4-A02-7] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java | Line: 152
Description: The log message reads "Start findAllByCompanyOwner for ownerId : {}" but the method is findAllTraining and the parameter is driverId.
Fix: Review and remediate the identified issue

[P4-A02-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAO.java | Line: 17-19
Description: The DriverDAO interface methods update, updateLastLoginTime, and updatePassword declare throws SQLException.
Fix: Declare throws SQLException

[P4-A02-9] LOW | File: `src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAO.java`, `src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAOImpl.java` | Line: N/A
Description: The interface declares save(Driver user) and update(Driver user) with the parameter name user, but the implementation uses user for save (line 48) and driver for update (line 63).
Fix: Update (line 63)

[P4-A02-10] INFO | File: src/main/java/com/journaldev/spring/jdbc/DAO/DriverDAO.java | Line: 12
Description: The method is named isDriverExist but the conventional Java naming would be doesDriverExist or isDriverExisting or simply driverExists.
Fix: Review and remediate the identified issue

[P4-A03-1] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java | Line: 5
Description: The import com.journaldev.spring.jdbc.model.Roles is never referenced in the class body. This is dead code that generates compiler warnings and clutters the import section.
Fix: Should be removed

[P4-A03-2] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java | Line: 47
Description: The method getEquipmentByUser(int uid) implements EquipmentDAO.getEquipmentByUser(int userId) but lacks the @Override annotation, while the other two interface methods at lines 52-53 and 57-58 do have it.
Fix: Review and remediate the identified issue

[P4-A03-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java | Line: 57-60
Description: The getEquipmentByMacAddress method (lines 57-60) uses tab indentation while getEquipmentByUser (lines 47-50) and getEquipmentIdByMacAddress (lines 52-55) use space indentation.
Fix: Use space indentation

[P4-A03-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java | Line: 54, 59
Description: The queryForObject(String sql, Object[] args, ...) overload has been deprecated in Spring Framework 5.3+ in favor of varargs alternatives.
Fix: Use the varargs overload directly (e.g., queryForObject(sql, Long.class, macAddress))

[P4-A03-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java | Line: 8
Description: The import com.journaldev.spring.jdbc.service.DriverService is never referenced in the class. This is dead import code that should be removed.
Fix: Should be removed

[P4-A03-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java | Line: 64-93
Description: The sendImpactNotification method performs email sending (SendEmail.sendMail) and SMS sending (SendMessage.init) directly from within a DAO class.
Fix: Should be extracted to a service layer class

[P4-A03-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java | Line: 24
Description: Unlike EquipmentDAOImpl which implements the EquipmentDAO interface, ImpactDAO is a concrete class with no corresponding interface.
Fix: Review and remediate the identified issue

[P4-A03-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java | Line: 39
Description: The value 80000 is used as a hard-coded threshold to determine whether an impact event should be saved.
Fix: Should be extracted to a named constant (e.g., RED_IMPACT_THRESHOLD) or made configurable, especially since the threshold value is a business rule that may need adjustment

[P4-A03-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java | Line: 54, 59
Description: JdbcTemplate.queryForObject() throws EmptyResultDataAccessException when the query returns zero rows, and IncorrectResultSizeDataAccessException when it returns more than one row.
Fix: Should use query() with result checking instead

[P4-A03-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java | Line: 36
Description: The query QUERY_EQUIPMENT_BY_MAC_ADDRESS uses select * which couples the query to the table schema. If columns are added or removed from the unit table, this could silently break BeanPropertyRowMapper mappings or return unnecessary data.
Fix: Review and remediate the identified issue

[P4-A03-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java | Line: 75, 77
Description: The logger.info(...) calls use string concatenation ("Start Sending Email to " + userResponse.getEmail()).
Fix: Use string concatenation ("Start Sending Email to " + userResponse.getEmail())

[P4-A03-12] LOW | File: `src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java` (line 18), `ImpactDAO.java` (line 23) | Line: N/A
Description: EquipmentDAOImpl is annotated with @Component("equipmentDAO") while ImpactDAO is annotated with @Repository.
Fix: Correct annotation for DAOs as it also provides automatic exception translation from JDBC exceptions to Spring's DataAccessException hierarchy

[P4-A03-13] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java | Line: 64
Description: The method sendImpactNotification declares throws SQLException in its signature, but the method body does not contain any code that throws SQLException.
Fix: Use is misleading and forces callers to handle a checked exception that will never be thrown from this method

[P4-A03-14] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java | Line: 25-26
Description: The Configuration field is @Autowired but never referenced in any method of ImpactDAO. This is dead code / unused dependency injection that should be removed.
Fix: Should be removed

[P4-A03-15] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/ImpactDAO.java | Line: 66-86
Description: In the sendImpactNotification lambda, cognitoService.getUser(notification.getEmail()) could return null if the user is not found in Cognito, but the result userResponse is used without null checking on lines 67-86 (e.g., userResponse.getName(), userResponse.getEmail()).
Fix: Use NPE on line 67's .equalsIgnoreCase() call

[P4-A03-16] INFO | File: src/main/java/com/journaldev/spring/jdbc/DAO/EquipmentDAOImpl.java | Line: 20
Description: EquipmentDAOImpl declares its own private static final Logger logger (SLF4J) on line 20, which shadows the protected final Log logger inherited from DaoSupport (via JdbcDaoSupport).
Fix: Review and remediate the identified issue

[P4-A04-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/DAO/ManufacturerDAOImpl.java | Line: 29-33
Description: The SQL query is constructed via string concatenation across multiple lines, but there are missing whitespace gaps between concatenated segments.
Fix: Review and remediate the identified issue

[P4-A04-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 22
Description: ManufacturerDAOImpl follows the pattern of implementing a separate interface (ManufacturerDAO), which is consistent with several other DAOs in the project (e.g., EquipmentDAO/EquipmentDAOImpl, DriverDAO/DriverDAOImpl, APIDAO/APIDAOImpl).
Fix: Review and remediate the identified issue

[P4-A04-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 10
Description: The import org.springframework.beans.factory.annotation.Value is declared but never used anywhere in the class.
Fix: Review and remediate the identified issue

[P4-A04-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 62
Description: The findByAuthority method uses getJdbcTemplate().queryForObject(...) which throws EmptyResultDataAccessException when no rows are returned.
Fix: Use queryForObject never returns null; it throws an exception instead

[P4-A04-5] LOW | File: `src/main/java/com/journaldev/spring/jdbc/DAO/ManufacturerDAOImpl.java`, `src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java` | Line: N/A
Description: ManufacturerDAOImpl uses @Component("manufacturerDAO") while UserDAO uses @Component (no qualifier).
Fix: Review and remediate the identified issue

[P4-A04-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/ManufacturerDAOImpl.java | Line: 27
Description: The getManufacturersForUser method logs the username parameter at INFO level: logger.info("getManufacturersForUser. username={}", username).
Fix: Consider logging at DEBUG level or masking the value

[P4-A04-7] LOW | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 23
Description: The logger field is initialized at line 23 but is never referenced in any method of UserDAO. Neither findByName nor findByAuthority log anything.
Fix: Review and remediate the identified issue

[P4-A04-8] INFO | File: src/main/java/com/journaldev/spring/jdbc/DAO/ManufacturerDAOImpl.java | Line: 29
Description: The SQL query selects from manufacture (singular), while the Java model class is named Manufacturer and the DAO is ManufacturerDAO.
Fix: Review and remediate the identified issue

[P4-A04-9] INFO | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 51-53
Description: There are three consecutive blank lines (lines 51-53) inside the ResultSetExtractor lambda in the findByName method, between the while-loop body and the return user statement.
Fix: Review and remediate the identified issue

[P4-A04-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 21
Description: UserDAO is annotated with @Transactional at the class level, but both methods (findByName and findByAuthority) are read-only queries.
Fix: Should be @Transactional(readOnly = true)

[P4-A04-11] HIGH | File: src/main/java/com/journaldev/spring/jdbc/DAO/UserDAO.java | Line: 31
Description: The QUERY_USER_BY_NAME query includes md5(u.name) = ? as an alternative lookup condition: where u.active = true and (u.name = ? or md5(u.name) = ?).
Fix: Should be reviewed and, if not strictly necessary, removed

[P4-A05-1] CRITICAL | File: `src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java` (referenced by `CompanyController.java`) | Line: 14, 19, 20
Description: RuntimeConfig contains hardcoded secrets in plain-text static fields: a GCM API key (GCMKEY = "key=AIzaSyDDuQUYLcXkutyIxRToLAeBPHBQNLfayzs"), Clickatell SMS credentials (USERNAME, PASSWORD), and an SMS API ID.
Fix: Should be externalized to environment variables, a secrets manager, or at minimum Spring property files excluded from version control

[P4-A05-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 64-117
Description: The controller directly instantiates JdbcTemplate and executes raw SQL queries (SELECT, INSERT, UPDATE, DELETE) within HTTP handler methods.
Fix: Should be moved to the DAO/repository layer

[P4-A05-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 97-98, 127-128, 131-132
Description: The permission acceptance mechanism relies on an MD5 hash of a timestamp concatenated with an ID (md5(to_char(createdat, 'DDMMYYYYHH12MI:SS')||id)), computed in SQL.
Fix: Should be stored and compared instead

[P4-A05-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 112, 116, 141
Description: The addCompany and companyAcceptWeb methods return HttpStatus.BAD_GATEWAY (502) for business-logic conditions such as "permission already exists" or "self-association attempted" or "token not found/already used." HTTP 502 means "the server, acting as a gateway, received an invalid response from an upstream server," which is semantically incorrect.
Fix: Review and remediate the identified issue

[P4-A05-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 162
Description: The companyDelete method executes DELETE FROM permission WHERE id = ? but is mapped to RequestMethod.PUT.
Fix: Should use RequestMethod.DELETE

[P4-A05-6] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 148-158, 162-174
Description: The companyAccept and companyDelete endpoints take a permission ID directly as a path variable and execute UPDATE/DELETE without any authentication or authorization check.
Fix: Delete permissions for any company

[P4-A05-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java | Line: 44, 49
Description: getAvailablePackage returns null both when the service returns an empty Optional (line 44, .orElse(null)) and when a MalformedURLException occurs (line 49).
Fix: Should be used instead

[P4-A05-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java | Line: 48
Description: A // TODO Handle error comment exists in the catch block for MalformedURLException. This indicates known incomplete error handling that was never addressed.
Fix: Should be resolved with proper error-response handling

[P4-A05-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java | Line: 61-67
Description: The downloadPackage method calls apkUpdaterService.loadPackageAsResource(pkgname, version) and immediately calls resource.getFilename() on the result (line 65) without null-checking.
Fix: Review and remediate the identified issue

[P4-A05-10] MEDIUM | File: `src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java`, `src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java` | Line: N/A
Description: APKUpdaterController uses Lombok's @Slf4j annotation (which generates a log field), while CompanyController manually declares private static final Logger logger = LoggerFactory.getLogger(...).
Fix: Should standardize on one approach

[P4-A05-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 46, 103, 105
Description: Line 46 uses parameterized logging (logger.info("Start Sending Email to " + email) on lines 103 and 105) which performs string concatenation regardless of whether the log level is enabled.
Fix: Should use parameterized placeholders ({}) to avoid unnecessary string concatenation overhead

[P4-A05-12] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ConfigurationController.java | Line: 16-17
Description: ConfigurationController is declared abstract but is annotated with @Controller. While Spring will not instantiate an abstract class, the @Controller annotation is misleading and unnecessary on an abstract base class.
Fix: Review and remediate the identified issue

[P4-A05-13] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ConfigurationController.java | Line: 19-24
Description: Both configuration and dataSource use field injection (@Autowired on protected fields) and are exposed to subclasses via protected access.
Fix: Use field injection (@Autowired on protected fields) and are exposed to subclasses via protected access

[P4-A05-14] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 20-22
Description: The Javadoc states "Handles requests for the Employee JDBC Service," but this class handles Company-related operations, not Employee operations.
Fix: Review and remediate the identified issue

[P4-A05-15] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 64, 124, 151, 166
Description: Multiple methods create new JdbcTemplate(dataSource) as a local variable on every request. While functionally harmless (JdbcTemplate is thread-safe and lightweight), it is wasteful and unconventional.
Fix: Should be created once (e.g., as a bean or initialized in a @PostConstruct method) and reused

[P4-A05-16] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 37
Description: getCompany accepts @PathVariable("uid") Long uid (boxed Long), while getCompanyDrivers accepts @PathVariable("uid") int uid (primitive int) for what appears to be the same kind of identifier.
Fix: Use confusion and unexpected behavior (e.g., null handling differences between Long and int)

[P4-A05-17] INFO | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: 6
Description: import com.journaldev.spring.jdbc.model.* uses a wildcard import. While not an error, wildcard imports can obscure which classes are actually used, may pull in unintended types, and make it harder to track dependencies during code review.
Fix: Review and remediate the identified issue

[P4-A05-18] INFO | File: src/main/java/com/journaldev/spring/jdbc/controller/CompanyController.java | Line: N/A
Description: The file uses inconsistent indentation, mixing tabs and varying levels of indentation. For example, searchCompany body has extra leading whitespace compared to getCompany.
Fix: Review and remediate the identified issue

[P4-A05-19] INFO | File: src/main/java/com/journaldev/spring/jdbc/controller/APKUpdaterController.java | Line: 22
Description: Unlike most other controllers in this package (CompanyController, DriverController, LocationController, etc.), APKUpdaterController does not extend ConfigurationController.
Fix: Review and remediate the identified issue

[P4-A06-01] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/DatabaseController.java | Line: 94-97
Description: In deleteCompanies(), when a retry pass is triggered, errors.clear() is called on line 96, and then errors is passed as both the errors parameter and the companies parameter on line 97: deleteCompanies(jdbcTemplate, ++pass, errors, errors).
Fix: Review and remediate the identified issue

[P4-A06-02] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/DatabaseController.java | Line: 66-77
Description: On line 66, companies is initialized to null. If the query on line 69 throws an exception, the catch block on lines 71-73 only logs an error but does not return or rethrow.
Fix: Review and remediate the identified issue

[P4-A06-03] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DatabaseController.java | Line: 18-60
Description: The QUERY_COMPANIES_TO_DELETE constant embeds 14 email addresses and 22 MAC addresses directly in the source code.
Fix: Should be externalized to configuration, a database table, or at minimum a properties file

[P4-A06-04] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/DatabaseCleanupException.java | Line: 7
Description: DatabaseCleanupException extends RuntimeException (which implements Serializable) but does not declare a serialVersionUID field.
Fix: Use deserialization issues if the class structure changes between JVM versions

[P4-A06-05] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 71, 83, 99, 157, 181
Description: Multiple endpoints return HttpStatus.BAD_GATEWAY (502) for authentication failures (line 71), registration errors (line 83), password reset failures (line 99), and file upload IO errors (lines 157, 181).
Fix: Should use 400 BAD_REQUEST, 401 UNAUTHORIZED, 409 CONFLICT, or 500 INTERNAL_SERVER_ERROR as appropriate

[P4-A06-06] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 60, 78, 92, 188, 236, 254
Description: Multiple methods log the full JSON serialization of Driver objects using gson.toJson(driverExample).
Fix: Review and remediate the identified issue

[P4-A06-07] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 154
Description: In uploadProfile(), the IOException catch block uses e.printStackTrace() which writes to System.err rather than using the SLF4J logger (log) that is available via the @Slf4j annotation.
Fix: Review and remediate the identified issue

[P4-A06-08] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 18, 142
Description: The import org.springframework.security.crypto.codec.Base64 on line 18 references a class that has been deprecated in Spring Security since version 4.x in favor of java.util.Base64 (available since Java 8).
Fix: Review and remediate the identified issue

[P4-A06-09] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 54
Description: The gson field is declared without an access modifier (Gson gson = new Gson();), giving it package-private visibility.
Fix: Should be private (and ideally private static final since Gson instances are thread-safe and reusable)

[P4-A06-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 111, 123, 135, 165, 190, 212, 237, 256
Description: Eight methods in DriverController (and one in DatabaseController line 65) create a new JdbcTemplate instance on every request via new JdbcTemplate(dataSource).
Fix: Should be a @Bean or an @Autowired field, or initialized once in a @PostConstruct method

[P4-A06-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 113, 125, 146, 171, 193, 196, 199, 213, 241, 245, 260
Description: The controller layer directly constructs and executes raw SQL queries in at least 11 locations. This violates separation of concerns — SQL and data access logic should reside in DAO/Repository classes, not in controllers.
Fix: Should reside in DAO/Repository classes, not in controllers

[P4-A06-12] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 139-148, 168-173
Description: In uploadProfile(), the BufferedInputStream created on line 139 may be replaced by a ByteArrayInputStream on line 142, but the original BufferedInputStream is never closed in that branch.
Fix: Should use try-with-resources

[P4-A06-13] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 58-73
Description: The getLoginAuth() method is annotated @Deprecated but is still mapped to an active REST endpoint (/rest/appuser/validate).
Fix: Review and remediate the identified issue

[P4-A06-14] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 210
Description: The getEmails() method logs "Start saveEmails." which is a copy-paste error. It should log "Start getEmails.".
Fix: Should log "Start getEmails."

[P4-A06-15] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 121
Description: The log message reads "Start delineUsers." which should be "Start declineUsers." or "Start declineDriver." to match the method name.
Fix: Should be "Start declineUsers." or "Start declineDriver." to match the method name

[P4-A06-16] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/DriverController.java | Line: 215
Description: The call jdbcTemplate.query(query, new Object[]{uid}, ...) uses the deprecated query(String, Object[], RowMapper) overload.
Fix: Review and remediate the identified issue

[P4-A06-17] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/DatabaseController.java | Line: 88
Description: The SQL statement "select delete_company("+ c +")" concatenates the company ID directly into the SQL string.
Fix: Should be used consistently

[P4-A07-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 44
Description: The logger is created with LoggerFactory.getLogger(ConfigurationController.class) instead of LoggerFactory.getLogger(ImpactController.class).
Fix: Correct and misleading

[P4-A07-2] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 17
Description: org.springframework.transaction.annotation.Transactional is imported but never used anywhere in the class.
Fix: Review and remediate the identified issue

[P4-A07-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 46, 89, 108, 126, 144
Description: Multiple methods create new JdbcTemplate(dataSource) locally instead of using a Spring-managed @Autowired JdbcTemplate bean or delegating to a DAO.
Fix: Should not contain raw SQL

[P4-A07-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 50, 59, 64, 93, 96-97, 112, 115, 127-135, 146, 152, 155, 160, 163, 168, 172
Description: Controllers contain extensive raw SQL (SELECT, INSERT, UPDATE) with string concatenation. This is a leaky abstraction that couples the controller layer directly to the database schema.
Fix: Should be encapsulated in DAO/repository classes

[P4-A07-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 32
Description: Gson gson = new Gson() is declared with default (package-private) access and is not final. Since Gson instances are thread-safe and immutable, this should be declared private static final to clearly communicate its intent, prevent accidental reassignment, and avoid unnecessary per-instance allocation.
Fix: Should be declared private static final to clearly communicate its intent, prevent accidental reassignment, and avoid unnecessary per-instance allocation

[P4-A07-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 18, 92
Description: org.springframework.security.crypto.codec.Base64 has been deprecated since Spring Security 4.x. The recommended replacement is java.util.Base64 (available since Java 8).
Fix: Review and remediate the identified issue

[P4-A07-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 89-102
Description: In saveImpactIMAGE, imagfis and sigfis are opened but only closed in the happy path (lines 101-102).
Fix: Should use try-with-resources blocks to ensure proper cleanup

[P4-A07-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 108, 142
Description: Exception handling in saveImpactIMAGE and saveImpactIMAGEAPP uses e.printStackTrace() which writes to System.err instead of the configured logging framework.
Fix: Should use logger.error("message", e) instead

[P4-A07-9] INFO | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 39-41
Description: The class-level Javadoc reads "Handles requests for the Employee JDBC Service." This is clearly a leftover from a template or copy-paste and does not describe the actual purpose of the ImpactController, which handles impact event and incident data.
Fix: Review and remediate the identified issue

[P4-A07-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 73-80
Description: A block of commented-out HTTP request documentation (multipart form-data boundary example) is left in the source.
Fix: Should be removed or moved to proper API documentation to keep the source clean

[P4-A07-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 142
Description: The method SaveService starts with an uppercase letter, violating Java method naming conventions (camelCase).
Fix: Should be saveService

[P4-A07-12] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ImpactController.java | Line: 180, 185, 191
Description: In saveImpactData, new ResponseEntity(results, ...) is used without the generic type parameter (raw type).
Fix: Should be new ResponseEntity<>(results, ...) or new ResponseEntity<Results>(results, ...) to match the method return type ResponseEntity<Results>

[P4-A07-13] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 39
Description: getEquipmentByUser returns HttpStatus.BAD_REQUEST when the equipment list is empty. An empty result set is not a client error — it is a valid response.
Fix: Review and remediate the identified issue

[P4-A07-14] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/ImageController.java | Line: 35-44
Description: URLConnection.guessContentTypeFromStream() can return null if it cannot determine the type. While the catch block sets a fallback to "application/octet-stream", the normal (non-exception) path does not handle a null return from guessContentTypeFromStream.
Fix: Should also cover the null return case outside the catch block

[P4-A07-15] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 143
Description: The log message reads "Start addEquipment." but the method is SaveService. This is a copy-paste error from the addEquipment method.
Fix: Review and remediate the identified issue

[P4-A07-17] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 87
Description: The log message reads "Start getFuelTypeList." but the method is getTypeList. This is a copy-paste error from the getFuelTypeList method below it.
Fix: Review and remediate the identified issue

[P4-A07-18] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 71
Description: When a duplicate equipment record is detected, the response returns HttpStatus.BAD_GATEWAY (502). HTTP 502 means the server, acting as a gateway, received an invalid response from an upstream server.
Fix: Review and remediate the identified issue

[P4-A07-19] INFO | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 6
Description: import com.journaldev.spring.jdbc.model.* uses a wildcard import. While functional, this reduces code clarity by hiding which specific model classes are used.
Fix: Review and remediate the identified issue

[P4-A07-20] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/EquipmentController.java | Line: 36, 44, 86, 105, 123, 142
Description: None of the @RequestBody parameters use Bean Validation (@Valid/@Validated) and none of the @PathVariable parameters are validated for range/sanity.
Fix: Use Bean Validation (@Valid/@Validated) and none of the @PathVariable parameters are validated for range/sanity

[P4-A08-1] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java | Line: 24-93
Description: The Javadoc on line 25 explicitly states /** Not in Use */, and grep confirms LocationController is not referenced anywhere in the source code.
Fix: Should either be removed or, at minimum, have its @Controller annotation removed to prevent endpoint registration

[P4-A08-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java | Line: 38, 55, 74
Description: Each request handler creates new JdbcTemplate(dataSource) on every invocation. While functionally correct, JdbcTemplate is a thread-safe, reusable object designed to be a singleton.
Fix: Should be a field initialized once (e.g., via @Autowired or in a @PostConstruct method)

[P4-A08-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java | Line: 59-63, 80-84
Description: Both saveGPSLocation and saveGPSLocations perform a two-step SQL operation: first UPDATE all rows to set current_location = false, then INSERT a new row with current_location = true.
Fix: UPDATE and INSERT (or a concurrent request interleaves), the data will be left in an inconsistent state with no current location for that unit

[P4-A08-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java | Line: 57-64
Description: The update-then-insert SQL pattern is copy-pasted between saveGPSLocation (single GPS) and saveGPSLocations (batch).
Fix: Should be extracted into a common private method or service

[P4-A08-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java | Line: 4
Description: The Util class is imported but never used in active code. The only reference is inside commented-out code on line 37 (Util.nthOccurrence).
Fix: Review and remediate the identified issue

[P4-A08-6] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java | Line: 36-38
Description: Three lines of code are commented out within getExportDir. The original logic for parsing the classpath directory is commented out and replaced by a different approach, but the old code remains as noise.
Fix: Should be removed; version control preserves history

[P4-A08-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java | Line: 35, 43
Description: In getExportDir, line 35 computes dir from the class's code source location via getProtectionDomain().getCodeSource().getLocation() and performs a substring(6).
Fix: Use line 43 unconditionally reassigns dir = "/" + dirctory

[P4-A08-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java | Line: 34
Description: The parameter is named dirctory instead of directory. While this has no runtime impact, it signals rushed or careless coding and reduces readability.
Fix: Review and remediate the identified issue

[P4-A08-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/RestURIConstants.java | Line: 4-6
Description: The comment //unused on line 4 suggests ACCEPT_USRS and DECLINE_USRS are not referenced. However, both are actively used in DriverController.java (lines 106 and 118 respectively).
Fix: Delete these constants during cleanup, breaking the application

[P4-A08-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/RestURIConstants.java | Line: 50
Description: The constant GET_SERVICEDTL maps to URL /rest/sericedetail/get/{userid} (note: "serice" instead of "service").
Fix: Use the misspelled URL

[P4-A08-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/RestURIConstants.java | Line: 35, 40, 52
Description: Several constants contain spelling errors in both names and URL paths: - Line 35: GET_FUELTYPE maps to /rest/fuletype/get/... ("fuletype" instead of "fueltype") - Line 40: DRIVRR_ACCESS — name contains "DRIVRR" instead of "DRIVER" - Line 52: RESUME_EQUIPMENT maps to path with {frequencey} instead of {frequency} These are actively used (verified ...
Fix: Should be noted as technical debt

[P4-A08-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/RestURIConstants.java | Line: 3
Description: RestURIConstants is a constants-only class with all public static final fields. It can be instantiated (new RestURIConstants()) even though doing so is meaningless.
Fix: Should be declared final

[P4-A08-13] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java | Line: 7-15
Description: All eight fields (subject, title, content, sEmail, rEmail, fileURL, name, input) are declared protected, suggesting the class is designed for inheritance.
Fix: Should be private with access through the existing getters/setters

[P4-A08-14] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java | Line: 27-31
Description: The downloadPDF() method calls HttpDownloadUtility.sendPost(name, input, ...) using the current value of this.name, then immediately overwrites this.name with HttpDownloadUtility.getFileName() on line 29.
Fix: Review and remediate the identified issue

[P4-A08-15] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java | Line: 73
Description: saveGPSLocations logs gson.toJson(gpsList) at INFO level, serializing the entire GPS list payload on every request.
Fix: Review and remediate the identified issue

[P4-A08-16] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/LocationController.java | Line: 36, 54, 73, 77
Description: All logging statements use string concatenation (e.g., "Start getGPSLocation." + " UID:" + uid). SLF4J supports parameterized messages (logger.info("Start getGPSLocation.
Fix: Use string concatenation (e.g., "Start getGPSLocation." + " UID:" + uid)

[P4-A08-17] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ReportAPI.java | Line: 35
Description: The method getExportDir calls this.getClass().getProtectionDomain().getCodeSource().getLocation() to determine a directory path.
Fix: Review and remediate the identified issue

[P4-A09-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 14, 18-21, 30
Description: The file contains multiple hardcoded credentials and API keys in plain text: - Line 14: Google GCM API key (GCMKEY = "key=AIzaSyDDuQUYLcXkutyIxRToLAeBPHBQNLfayzs") - Line 18: Clickatell username (USERNAME = "ciclickatell") - Line 19: Clickatell password (PASSWORD = "OVLOaICXccaNUS") - Line 21: Clickatell API ID (API_ID = "3629505")
Fix: Review and remediate the identified issue

[P4-A09-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 322, 410
Description: Admin credentials are hardcoded directly in JSON strings used for report API calls: - Line 322: "admin_password\":\"ciiadmin\", \"username\": \"hui\"" - Line 410: "admin_password\":\"ciiadmin\", \"username\": \"hui\""
Fix: Review and remediate the identified issue

[P4-A09-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 323, 411
Description: The report API input payload, which includes admin_password and username, is logged at INFO level: logger.info("Input URL is:" + input).
Fix: Review and remediate the identified issue

[P4-A09-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 5-32
Description: Every field in RuntimeConfig is declared public static but not final. This means any code in the application can modify these "configuration" values at runtime, leading to unpredictable behavior.
Fix: Should be managed via Spring's property injection mechanism rather than mutable statics

[P4-A09-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 53
Description: The logger is initialized as LoggerFactory.getLogger(ConfigurationController.class) instead of LoggerFactory.getLogger(SessionController.class).
Fix: Review and remediate the identified issue

[P4-A09-6] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 163
Description: The SQL query on line 163 contains syntactically broken SQL: " where u. l.question_id = question_id = ? and type ilike ?) ".
Fix: Review and remediate the identified issue

[P4-A09-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 116, 143, 152, 170, 187, 229
Description: Multiple TODO comments dated from June-July 2017 are scattered through the code, e.g., // TODO inserted [15 Jun 2017,4:32:27 pm] and // TODO [19 Jun 2017,9:06:09 pm].
Fix: Should either be resolved or removed

[P4-A09-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 246-251
Description: A block of commented-out code exists in the startSessions method, preceded by the comment //No need ot check other driver uses it.
Fix: Should be preserved as a plain comment if needed

[P4-A09-9] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 38, 123, 265, 288, 374
Description: Every controller method creates a new JdbcTemplate instance via new JdbcTemplate(dataSource). JdbcTemplate is designed to be thread-safe and reusable; Spring best practice is to create it once (typically via @Autowired or in a @PostConstruct method) and reuse the same instance.
Fix: Use the same instance

[P4-A09-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 4
Description: Line 4 uses a wildcard import: import com.journaldev.spring.jdbc.model.*. This obscures which model classes are actually used by the controller and can cause unexpected compilation issues if new classes are added to the model package.
Fix: Use unexpected compilation issues if new classes are added to the model package

[P4-A09-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 353, 421
Description: Exception handling uses e.printStackTrace() which writes to standard error rather than the application's configured logging framework.
Fix: Should be logged via logger.error("message", e) instead

[P4-A09-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 25, 27
Description: MSGID_CODEE_DUPLICATE_VEHICLE (line 25) and MSGID_LOGICERRORR (line 27) both have the value "3". This creates ambiguity in error handling since the same message ID maps to two different error conditions.
Fix: Review and remediate the identified issue

[P4-A09-13] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 120
Description: The path variable and parameter are consistently named frequencey (with a stray 'e') instead of frequency.
Fix: Use a runtime bug, it propagates a spelling error into the public REST API path (/rest/driverresume/get/{uid}/frequencey/{frequencey}), which becomes part of the API contract and is harder to fix later

[P4-A09-14] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 332-350
Description: The generateReport method contains four near-identical blocks checking and sending emails to email_addr1 through email_addr4.
Fix: Should be collected into a list and iterated

[P4-A09-15] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 30
Description: The APIURL field uses plain HTTP: "http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/".
Fix: Review and remediate the identified issue

[P4-A09-16] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java | Line: 13-14
Description: GCMSERVER references https://gcm-http.googleapis.com/gcm/send, which is Google Cloud Messaging. GCM was officially deprecated by Google in April 2018 and shut down in May 2019.
Fix: Review and remediate the identified issue

[P4-A09-17] INFO | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 27-28
Description: ResumeController's Javadoc says "Handles requests for the Product JDBC Service" and SessionController's says "Handles requests for the Employee JDBC Service." Neither description matches the actual content of the respective controller.
Fix: Review and remediate the identified issue

[P4-A09-18] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 154
Description: The searchForm method accepts a @PathVariable("keyword") String keyword parameter, but this variable is never used in the query or passed as a parameter to jdbcTemplate.query() on line 165.
Fix: Review and remediate the identified issue

[P4-A09-19] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 289-295
Description: The private toString(Serializable o) method serializes an object to Base64. While it does not technically override Object.toString() (different signature), the name is confusing and misleading.
Fix: Review and remediate the identified issue

[P4-A09-20] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 281
Description: Both generateReport and sendReportList are mapped as RequestMethod.GET but perform state-changing side effects: they generate PDF reports and send emails.
Fix: Should be safe and idempotent)

[P4-A09-21] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/ResumeController.java | Line: 35, 120, 262, 283
Description: None of the controller methods validate their path variable inputs. For example, uid, eid, sid, qid, and rid are used directly in SQL queries without checking for valid ranges (e.g., positive integers).
Fix: Use EmptyResultDataAccessException or NullPointerException from queryForObject returning null, leading to unhandled 500 errors

[P4-A09-22] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 316
Description: In endSessions, queryForObject on line 316 retrieves acc_hour as BigDecimal. If the session's finish_time - start_time produces NULL (e.g., if the update on line 312-313 sets a null finish_time), queryForObject can return null, and subsequent operations on acc_hour will throw NullPointerException.
Fix: Update on line 312-313 sets a null finish_time), queryForObject can return null, and subsequent operations on acc_hour will throw NullPointerException

[P4-A09-23] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/SessionController.java | Line: 90, 108, 221
Description: HttpStatus.BAD_GATEWAY (502) is used for application-level errors such as "equipment not found" (line 108), "IOException during file upload" (line 90), and "duplicate result" (line 221).
Fix: Review and remediate the identified issue

[P4-A10-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/controller/UserController.java | Line: 30
Description: When a user is not found by email, the controller returns HttpStatus.BAD_GATEWAY (502). HTTP 502 indicates a server acting as a gateway received an invalid response from an upstream server — it has no semantic relationship to "entity not found." The correct status would be HttpStatus.NOT_FOUND (404) or potentially HttpStatus.NO_CONTENT (204).
Fix: Correct status would be HttpStatus.NOT_FOUND (404) or potentially HttpStatus.NO_CONTENT (204)

[P4-A10-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/controller/UserController.java | Line: 23-25
Description: The controller method parameter is named email and the request parameter annotation is @RequestParam("email"), but the DAO method invoked is userDao.findByName(email).
Fix: Should be findByEmail) or a logic bug in the controller (wrong DAO method called)

[P4-A10-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/UserController.java | Line: 16, 23
Description: The class uses @Controller at class level and @ResponseBody on the method return type. The idiomatic Spring approach since Spring 4.0 is to use @RestController which combines both annotations, reducing boilerplate and making the intent clearer.
Fix: Use @RestController which combines both annotations, reducing boilerplate and making the intent clearer

[P4-A10-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/APIConnections.java | Line: 15-16
Description: Fields IDAPIConnection and APIConnectionKey start with uppercase letters, violating the Java naming convention that instance fields should begin with a lowercase letter (e.g., idApiConnection, apiConnectionKey).
Fix: Should begin with a lowercase letter (e.g., idApiConnection, apiConnectionKey)

[P4-A10-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/APIConnections.java | Line: 21-22, 27-28
Description: The setter methods in APIConnections assign to the field without using the this. qualifier (e.g., IDAPIConnection = iDAPIConnection).
Fix: Use of this. in setters is a defensive best practice

[P4-A10-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Answers.java | Line: 14, 29, 32
Description: The field question_id and its getter/setter (getQuestion_id, setQuestion_id) use snake_case, which violates Java naming conventions.
Fix: Should be questionId with methods getQuestionId() and setQuestionId()

[P4-A10-7] LOW | File: `src/main/java/com/journaldev/spring/jdbc/model/APIConnections.java`, `src/main/java/com/journaldev/spring/jdbc/model/Answers.java` | Line: N/A
Description: Both model classes contain empty Javadoc comment blocks (just /** */ with no content) above serialVersionUID.
Fix: Add visual noise without conveying information

[P4-A10-8] LOW | File: `src/main/java/com/journaldev/spring/jdbc/model/Answers.java`, `src/main/java/com/journaldev/spring/jdbc/model/APIConnections.java` | Line: N/A
Description: Both model classes use plural names (Answers, APIConnections) but each instance represents a single entity (one answer, one API connection).
Fix: Use singular names (Answer, APIConnection)

[P4-A10-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/controller/UserController.java | Line: 19-20
Description: The userDao dependency is injected using field injection (@Autowired on a private field). Constructor injection is the recommended approach in modern Spring as it makes dependencies explicit, supports immutability, simplifies testing (no reflection needed), and allows the compiler to enforce required dependencies.
Fix: Review and remediate the identified issue

[P4-A11-1] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Charts.java | Line: 9-51
Description: AuthenticationRequest and AuthenticationResponse both use Lombok @Data to auto-generate getters, setters, toString, equals, and hashCode.
Fix: Should either use @Data (consistent with the rest of the codebase) or, at minimum, implement equals/hashCode to honour the Serializable contract

[P4-A11-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Charts.java | Line: 16, 43, 46
Description: The field unit_id and its corresponding accessors getUnit_id() / setUnit_id(int) use snake_case naming, which violates the standard Java camelCase naming convention (should be unitId, getUnitId(), setUnitId()).
Fix: Should be unitId, getUnitId(), setUnitId())

[P4-A11-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Charts.java | Line: 33-34, 36-38
Description: getUsageList() returns a direct reference to the internal ArrayList. External callers can mutate the list without going through the class API, bypassing the addUsageList() method.
Fix: Should be returned if the intent of addUsageList() is to control list modification

[P4-A11-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationRequest.java | Line: 17-20
Description: The password and newPassword fields are plain String fields with no @JsonIgnore on output, no transient keyword, and no @ToString.Exclude annotation.
Fix: Should be applied to password and newPassword

[P4-A11-5] LOW | File: `src/main/java/com/journaldev/spring/jdbc/model/AuthenticationRequest.java`, `AuthenticationResponse.java`, `Charts.java` | Line: N/A
Description: All three files contain empty Javadoc-style comment blocks (/** * */) directly above the serialVersionUID field.
Fix: Should either be removed or replaced with meaningful documentation

[P4-A11-6] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationResponse.java | Line: 25
Description: AuthenticationResponse extends ResponseWrapper which already contains a List<ErrorMessage> errors field for communicating error/status information.
Fix: Should be consolidated

[P4-A11-7] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationResponse.java | Line: 20-22
Description: expiresIn, actualDate, and expirationDate are all declared as String. Using String for date/time values loses type safety, allows invalid date strings, and requires manual parsing at every usage site.
Fix: Use these values may originate from an external API (e.g., Cognito) and may be intentionally stored as-is

[P4-A11-8] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/AuthenticationRequest.java | Line: 5, 22-28
Description: The @Builder annotation is applied to the private all-args constructor rather than at the class level.
Fix: Review and remediate the identified issue

[P4-A12-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 25, 30
Description: The Driver class uses @Data which generates public getPassword() and getSecurityno() getters/setters.
Fix: Review and remediate the identified issue

[P4-A12-2] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/Company.java | Line: 23
Description: The password field on Company is a plain String exposed via Lombok @Data getters/setters and toString().
Fix: Review and remediate the identified issue

[P4-A12-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Company.java | Line: 44-49
Description: The builder constructor first sets this.name, this.email, and this.password from the explicit parameters (lines 35-37), then immediately overwrites them if contactDriver is not null (lines 46-48).
Fix: Review and remediate the identified issue

[P4-A12-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 41
Description: The drivers field (List<Driver>) is declared as an instance field (line 41) but is not included as a parameter in the @Builder constructor (lines 47-65).
Fix: Use infinite recursion or StackOverflowError if any driver in the list also has a non-null drivers list

[P4-A12-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/DriverEmails.java | Line: 5-59
Description: DriverEmails manually defines all getters and setters (12 methods for 6 fields), while the sibling classes Company and Driver in the same package both use Lombok @Data to auto-generate them.
Fix: Use Lombok @Data to auto-generate them

[P4-A12-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/DriverEmails.java | Line: 14-17
Description: The DriverEmails class models multiple email addresses as four distinct fields (email_addr1 through email_addr4) rather than using a List<String> or similar collection.
Fix: Review and remediate the identified issue

[P4-A12-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 19-20, 28-39
Description: Multiple fields in Driver use snake_case naming (first_name, last_name, photo_url, comp_id, driver_based, date_format, max_session_length, compliance_date, gps_frequency).
Fix: Use issues with frameworks that rely on standard property naming (e.g., Jackson, Spring BeanPropertyRowMapper)

[P4-A12-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 28, 38
Description: The fields expirydt (line 28) and compliance_date (line 38) represent dates but are declared as String.
Fix: Should be used for date fields

[P4-A12-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Company.java | Line: 6
Description: The lombok.Singular import is used on the @Singular annotation on the builder constructor parameter arrRoles (line 33).
Fix: Should be verified

[P4-A12-10] LOW | File: `src/main/java/com/journaldev/spring/jdbc/model/Company.java`, `src/main/java/com/journaldev/spring/jdbc/model/DriverEmails.java` | Line: N/A
Description: Both Company.java and DriverEmails.java have empty Javadoc comments (/** */) above the serialVersionUID field.
Fix: Should either be removed or populated with meaningful content

[P4-A12-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/DriverEmails.java | Line: 12-13
Description: DriverEmails uses primitive int for id and driver_id, while Company and Driver use Long for their id fields.
Fix: Use subtle bugs when checking whether an entity has been persisted

[P4-A12-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Driver.java | Line: 14, 22-23
Description: The @EqualsAndHashCode(onlyExplicitlyIncluded = true) annotation restricts equality to only the email field (line 23).
Fix: Review and remediate the identified issue

[P4-A13-1] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/DriverEquipment.java | Line: 9-10
Description: DriverEquipment extends Equipment which contains 17 fields including id, name, serial_no, and mac_address.
Fix: Should use callSuper = true instead

[P4-A13-2] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java | Line: 6
Description: import com.journaldev.spring.jdbc.model.Roles.RolesBuilder is imported but never referenced anywhere in the DriverTraining class.
Fix: Review and remediate the identified issue

[P4-A13-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java | Line: 4
Description: import java.util.Date is imported but never used. The training_date and expiration_date fields are declared as String rather than Date.
Fix: Use proper date types but switched to String without cleaning up

[P4-A13-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java | Line: 23-24
Description: training_date and expiration_date are declared as String rather than java.util.Date, java.time.LocalDate, or another temporal type.
Fix: Use proper date typing

[P4-A13-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java | Line: 20-24
Description: Fields manufacture_id, type_id, fuel_type_id, training_date, and expiration_date use snake_case naming, which violates standard Java naming conventions (camelCase).
Fix: Should still be noted as a quality concern

[P4-A13-6] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/DriverTraining.java | Line: 14
Description: The class declaration and the serialVersionUID Javadoc comment are merged on the same line: public class DriverTraining implements Serializable {/.
Fix: Review and remediate the identified issue

[P4-A13-7] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/EmailLayout.java | Line: 5-40
Description: EmailLayout uses manually written getter/setter boilerplate (8 methods across lines 17-39), while sibling model classes in the same package (DriverEquipment, DriverTraining, Equipment, Roles, Driver, etc.) use Lombok's @Data annotation to auto-generate these same methods.
Fix: Should use @Data to be consistent with the rest of the project

[P4-A13-8] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/EmailLayout.java | Line: 41-45
Description: There are 4 unnecessary blank lines at the end of the class body before the closing brace. While functionally harmless, this is a minor formatting issue that suggests the file was not cleaned up.
Fix: Review and remediate the identified issue

[P4-A13-9] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/EmailLayout.java | Line: 5-46
Description: Unlike DriverTraining and Equipment which provide a @Builder pattern, EmailLayout only has the default no-arg constructor and setters.
Fix: Review and remediate the identified issue

[P4-A13-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/DriverEquipment.java | Line: 10-15
Description: DriverEquipment extends Equipment which has a @Builder constructor, but DriverEquipment does not define its own @Builder.
Fix: Use the parent builder (which cannot set hours/trained)

[P4-A14-1] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/EquipmentType.java | Line: 1-35
Description: EquipmentType is not imported or referenced anywhere else in the codebase. A project-wide search for "EquipmentType" returns only its own class declaration.
Fix: Should either be removed or wired into relevant services/DAOs if it was intended to be used

[P4-A14-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/EquipmentType.java | Line: 5, 16-33
Description: EquipmentType uses manually written getters and setters, while the sibling models Equipment and ErrorMessage (and every other model in the package) use Lombok @Data to generate them.
Fix: Review and remediate the identified issue

[P4-A14-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Equipment.java | Line: 16-17, 19-21, 24, 26-27, 29-31
Description: Java convention (and the project's own Lombok-generated accessor convention) requires camelCase for field names.
Fix: Rename fields to camelCase (e.g., typeId, compId, fuelTypeId) and use @JsonProperty or column-mapping annotations if needed for database/JSON mapping

[P4-A14-4] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Equipment.java | Line: 3, 33
Description: The @Builder annotation is imported and placed on the all-args constructor, but a project-wide search for Equipment.builder returns zero matches.
Fix: Review and remediate the identified issue

[P4-A14-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Equipment.java | Line: 14-31
Description: The field declarations (lines 14-31) use 4-space indentation, while the constructor body (lines 34-56) uses tab indentation.
Fix: Use 4-space indentation, while the constructor body (lines 34-56) uses tab indentation

[P4-A14-6] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/EquipmentType.java | Line: 7-9
Description: There is an empty Javadoc comment block (/** * */) above serialVersionUID. This is auto-generated boilerplate from Eclipse's "Add generated serial version ID" action.
Fix: Should be removed

[P4-A14-7] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Equipment.java | Line: 14, 16-17, 19-21
Description: Using primitive int for ID and foreign-key fields (id, type_id, comp_id, manu_id, fuel_type_id, attachment_id) means they default to 0 rather than null.
Fix: Review and remediate the identified issue

[P4-A14-8] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/ErrorMessage.java | Line: 8-19
Description: Unlike Equipment and other models in the package which provide @Builder and all-args constructors, ErrorMessage only has the Lombok-generated no-args constructor.
Fix: Review and remediate the identified issue

[P4-A14-9] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/EquipmentType.java | Line: 5
Description: The class declaration reads implements Serializable{ with no space before the opening brace. Standard Java style requires a space: implements Serializable {.
Fix: Review and remediate the identified issue

[P4-A15-1] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java | Line: 12-17, 23-61
Description: All field names use snake_case (input_type, input_label, input_value, input_image, input_order, expected_answer) and the corresponding getter/setter methods follow the same pattern (e.g., getInput_type(), setInput_value()).
Fix: Should be used instead of leaking DB naming into Java code

[P4-A15-2] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java | Line: 5
Description: The class name FormDtl uses a non-standard abbreviation for "Detail." Java naming conventions favor full, readable names (e.g., FormDetail).
Fix: Review and remediate the identified issue

[P4-A15-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java | Line: 5-63
Description: The model class implements Serializable but does not override equals(), hashCode(), or toString(). If instances are placed in collections (e.g., HashSet, HashMap), the default identity-based equals/hashCode from Object will produce incorrect behavior.
Fix: Correct behavior

[P4-A15-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/FuelType.java | Line: 5-30
Description: Same issue as A15-3. FuelType is a Serializable model but lacks equals(), hashCode(), and toString() overrides.
Fix: Review and remediate the identified issue

[P4-A15-5] LOW | File: `src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java`, `src/main/java/com/journaldev/spring/jdbc/model/FuelType.java` | Line: N/A
Description: Both files contain an auto-generated empty Javadoc block (/** * */) above serialVersionUID. These serve no documentation purpose and are dead comment noise, likely left by IDE template generation.
Fix: Should be removed or replaced with meaningful documentation

[P4-A15-6] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GCMData.java | Line: 3
Description: Both FormDtl and FuelType in the same package implement Serializable, but GCMData does not. If model objects in this package are expected to be serializable (e.g., for session storage, caching, or message passing), this inconsistency could cause a NotSerializableException at runtime.
Fix: Use a NotSerializableException at runtime

[P4-A15-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GCMData.java | Line: 5
Description: The field to is declared protected rather than private. Since the class provides a public getter and setter, the field should be private to maintain proper encapsulation.
Fix: Should be private to maintain proper encapsulation

[P4-A15-8] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/GCMData.java | Line: 3
Description: The class name GCMData references Google Cloud Messaging (GCM), which was deprecated by Google in April 2018 and shut down in May 2019, fully replaced by Firebase Cloud Messaging (FCM).
Fix: Review and remediate the identified issue

[P4-A15-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GCMData.java | Line: 3-17
Description: GCMData lacks equals(), hashCode(), and toString() overrides. While this is a simpler model, the absence still hinders debugging and collection usage.
Fix: Review and remediate the identified issue

[P4-A15-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java | Line: 20-61
Description: The getter for id appears at line 20, but its setter does not appear until line 35. Meanwhile, input_type's getter/setter pair is at lines 23-28, and input_value's pair at lines 29-34.
Fix: Should be grouped together or fields and accessors should follow a consistent order

[P4-A15-11] LOW | File: `src/main/java/com/journaldev/spring/jdbc/model/FormDtl.java`, `src/main/java/com/journaldev/spring/jdbc/model/FuelType.java` | Line: N/A
Description: The id field is declared as primitive int (default value 0) rather than Integer. If a model instance has not yet been persisted to the database, id will silently be 0 instead of null, making it impossible to distinguish between "not yet assigned" and "assigned as 0." Using Integer would allow null to represent an unset ID.
Fix: Review and remediate the identified issue

[P4-A16-1] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GCMEntity.java | Line: 1-19
Description: GCMEntity is never imported, extended, or referenced anywhere in the codebase. No other class extends it (confirmed by grep), it does not appear in any XML/YAML/properties configuration, and it is not used via reflection patterns.
Fix: Review and remediate the identified issue

[P4-A16-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GCMResponse.java | Line: 1-52
Description: GCMResponse is never imported or referenced anywhere else in the codebase. No controller, service, or DAO class uses it.
Fix: Review and remediate the identified issue

[P4-A16-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GCMDataPermission.java | Line: 1-23
Description: GCMDataPermission is never imported or referenced anywhere in the codebase outside its own definition.
Fix: Review and remediate the identified issue

[P4-A16-4] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GCMEntity.java | Line: 8, 10, 14
Description: All three files use snake_case for field names and getter/setter method names (e.g., msg_type, getMsg_type(), multicast_id, getMulticast_id(), canonical_ids, getCanonical_ids()).
Fix: Use camelCase in Java with @JsonProperty annotations for serialization mapping

[P4-A16-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GCMEntity.java | Line: 7
Description: GCMEntity does not implement Serializable, while other model classes in the same package (GCMDataPermission, GCMResponse, Permissions, Results) do.
Fix: Implement Serializable, while other model classes in the same package (GCMDataPermission, GCMResponse, Permissions, Results) do

[P4-A16-6] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GCMDataPermission.java | Line: 5
Description: GCMDataPermission declares implements Serializable, but its parent class GCMData does not implement Serializable.
Fix: Use GCMData itself is not Serializable — only the subclass is

[P4-A16-7] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GCMResponse.java | Line: 41-42
Description: getResults() returns the internal List<Results> reference directly. Callers can modify the internal state of GCMResponse by adding/removing elements from the returned list.
Fix: Review and remediate the identified issue

[P4-A16-8] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/GCMDataPermission.java | Line: 7-9
Description: Both files contain an auto-generated empty Javadoc comment (/** * */) above the serialVersionUID field.
Fix: Should either be removed or replaced with meaningful documentation

[P4-A16-9] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/GCMResponse.java | Line: 47-51
Description: The file has four consecutive blank lines before the closing brace. Standard style guides (Google Java Style, Sun conventions) recommend at most one blank line between members and no excessive trailing whitespace inside a class body.
Fix: Review and remediate the identified issue

[P4-A17-1] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Impact.java | Line: 8
Description: The import java.util.Date is declared but never referenced. The impact_time field is typed as String, not Date.
Fix: Should be removed to eliminate the build warning

[P4-A17-2] MEDIUM | File: `src/main/java/com/journaldev/spring/jdbc/model/GPS.java` (entire file) vs `Impact.java` | Line: N/A
Description: Impact.java leverages Lombok @Data and @NoArgsConstructor to auto-generate getters, setters, equals(), hashCode(), and toString().
Fix: Should be migrated to Lombok for consistency and to gain the missing equals/hashCode/toString implementations

[P4-A17-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GPS.java | Line: 5-63
Description: The GPS class implements Serializable and is used as a model object returned from REST endpoints and stored in lists, but it does not override equals(), hashCode(), or toString().
Fix: Use object identity rather than value equality

[P4-A17-4] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GPSList.java | Line: 7-26
Description: Same as A17-3 but for GPSList. The class is a thin wrapper around List<GPS> and is used as a @RequestBody parameter.
Fix: Review and remediate the identified issue

[P4-A17-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/GPSList.java | Line: 12
Description: The field List<GPS> gpsList is declared without an access modifier, giving it package-private visibility.
Fix: Should be declared private to match standard JavaBean conventions and align with how fields are declared in GPS.java and Impact.java

[P4-A17-6] MEDIUM | File: `src/main/java/com/journaldev/spring/jdbc/model/GPS.java` (line 16), `src/main/java/com/journaldev/spring/jdbc/model/Impact.java` (line 17) | Line: N/A
Description: Both gps_time in GPS and impact_time in Impact represent temporal values but are typed as String. Callers must manually parse these strings via DateUtil.parseDateTimeIso() at every usage site (confirmed in LocationController.java line 84 and ImpactDAO.java lines 43, 54).
Fix: Review and remediate the identified issue

[P4-A17-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/GPS.java | Line: 14-15
Description: Latitude and longitude are stored as Float (boxed wrapper of 32-bit IEEE 754 float). A 32-bit float provides approximately 7 significant decimal digits of precision, which corresponds to roughly 1.1 meters of positional accuracy at the equator.
Fix: Review and remediate the identified issue

[P4-A17-8] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/GPS.java | Line: 14-15
Description: The longitude and latitude fields are declared as boxed Float (nullable). In LocationController.java lines 57 and 78, they are compared with !=0 which triggers auto-unboxing.
Fix: Should be used in the controller

[P4-A17-9] LOW | File: `src/main/java/com/journaldev/spring/jdbc/model/GPS.java` (lines 13, 16-18), `src/main/java/com/journaldev/spring/jdbc/model/Impact.java` (lines 16-18) | Line: N/A
Description: Fields like unit_id, gps_time, current_location, unit_name, impact_value, impact_time, and mac_address use snake_case naming, violating standard Java naming conventions (unitId, gpsTime, currentLocation, etc.).
Fix: Use it is a pervasive codebase-wide convention rather than an isolated mistake

[P4-A17-10] LOW | File: `src/main/java/com/journaldev/spring/jdbc/model/GPSList.java` (line 9), `src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java` (line 13) | Line: N/A
Description: Both GPSList and ImpactList share the identical serialVersionUID value 3101512981283324426L. While serialVersionUID only needs to be unique within a class hierarchy for serialization compatibility, sharing the exact same value across unrelated classes suggests a copy-paste origin.
Fix: Use confusion during debugging of serialization issues and indicates careless code duplication

[P4-A17-11] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/GPS.java | Line: 7-9
Description: An empty Javadoc block (/** */) precedes the serialVersionUID field declaration. This is auto-generated IDE boilerplate that adds no value and should be removed for cleanliness.
Fix: Should be removed for cleanliness

[P4-A17-12] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/GPSList.java | Line: 7-26
Description: GPSList is a trivial wrapper around List<GPS> with only a getter and setter, created solely to work around Java type erasure for JSON deserialization of @RequestBody List<GPS>.
Fix: Review and remediate the identified issue

[P4-A18-1] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java | Line: 13
Description: ImpactList uses serialVersionUID = 3101512981283324426L, which is identical to the value used in GPSList.java (line 9).
Fix: Should have its own unique UID

[P4-A18-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java | Line: 16
Description: The field List<Impact> impactList is declared with default (package-private) access instead of private.
Fix: Should be declared private

[P4-A18-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java | Line: 19-21
Description: getImpactList() returns a direct reference to the internal mutable ArrayList. Callers can modify the list (add, remove, clear) without going through the owning object.
Fix: Review and remediate the identified issue

[P4-A18-4] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java | Line: 1-28
Description: ImpactList manually defines getters and setters and does not use Lombok, while its closely related sibling class Impact (which it wraps in a list) uses @Data and @NoArgsConstructor.
Fix: Should be applied consistently

[P4-A18-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java | Line: 8-28
Description: The class implements Serializable and is used as a @RequestBody parameter in the controller, but does not override equals(), hashCode(), or toString().
Fix: Use subtle issues if instances are ever compared or placed in collections

[P4-A18-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactNotification.java | Line: 11-18
Description: All fields use snake_case naming (driver_name, unit_name, manufacturer_name, etc.) instead of Java-standard camelCase.
Fix: Use camelCase fields with @Column annotations or a custom RowMapper to handle the mapping

[P4-A18-7] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/ImpactNotification.java | Line: 9
Description: Unlike ImpactList, Impact, and Incidents which all implement Serializable, ImpactNotification does not.
Fix: Implement Serializable, ImpactNotification does not

[P4-A18-8] INFO | File: `src/main/java/com/journaldev/spring/jdbc/model/ImpactList.java`, `src/main/java/com/journaldev/spring/jdbc/model/Incidents.java` | Line: N/A
Description: Both files contain empty Javadoc comment blocks (/** */) above the serialVersionUID field. These are IDE-generated placeholders that serve no documentation purpose and should either be removed or replaced with meaningful content.
Fix: Should either be removed or replaced with meaningful content

[P4-A18-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Incidents.java | Line: 12-46
Description: Field declarations are split into two groups separated by getter/setter methods. Fields id through unit_id are declared on lines 12-22, then getters/setters for driver_id, unit_id, and incident appear on lines 24-42, followed by more field declarations (description, report_time, event_time, job_number) on lines 43-46, and then more getters/setters.
Fix: Declare all fields first, then all constructors, then all methods

[P4-A18-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Incidents.java | Line: 73-84
Description: The getSignature() and getImage() methods return direct references to internal byte[] arrays, and the setters store the passed references without copying.
Fix: Should store a copy

[P4-A18-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Incidents.java | Line: 18-20
Description: The fields injury, near_miss, and incident are declared as Boolean (wrapper type) rather than boolean (primitive).
Fix: Should be documented and callers must perform null-checks

[P4-A18-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Incidents.java | Line: 15-22
Description: Some fields use tab indentation (e.g., signature on line 13, image on line 14) while others use space indentation (e.g., injury_type on line 15, witness on line 16).
Fix: Use diff noise and merge conflicts

[P4-A18-13] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/Incidents.java | Line: 5
Description: The class is named Incidents (plural) but represents a single incident record (the controller parameter is @RequestBody Incidents incident).
Fix: Review and remediate the identified issue

[P4-A18-14] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Incidents.java | Line: 5-122
Description: The Incidents class has 16 fields and 32 manual getter/setter methods spanning 122 lines. The sibling classes Impact and ImpactNotification in the same package use Lombok @Data to eliminate this boilerplate.
Fix: Use Lombok @Data to eliminate this boilerplate

[P4-A18-15] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/Incidents.java | Line: 13-14
Description: The signature and image fields (both byte[]) are defined in the Incidents model class, but the saveIncident method in ImpactController.java (line 67-68) does not include them in the INSERT statement.
Fix: Review and remediate the identified issue

[P4-A19-1] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Manufacturer.java | Line: 26
Description: The field name is declared at line 26, after its getter getName() (line 20) and setter setName() (line 23).
Fix: Should be grouped together before methods

[P4-A19-2] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Manufacturer.java | Line: 5-28
Description: Manufacturer is a Serializable model class with id and name fields but does not override equals(), hashCode(), or toString().
Fix: Use Lombok @Data to generate these; this class uses manual getters/setters with no such override

[P4-A19-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/OfflineSessions.java | Line: 5-30
Description: Same as A19-2. OfflineSessions implements Serializable and contains two domain object fields (Sessions, Result) but does not override equals(), hashCode(), or toString().
Fix: Review and remediate the identified issue

[P4-A19-4] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/Manufacturer.java | Line: 7-9
Description: The Javadoc comment block /** * */ above serialVersionUID is empty and provides no documentation value.
Fix: Should either be removed or filled with meaningful content

[P4-A19-5] MEDIUM | File: `src/main/java/com/journaldev/spring/jdbc/model/Manufacturer.java`, `OfflineSessions.java`, `PackageEntry.java` | Line: N/A
Description: The model package has a significant style inconsistency: PackageEntry uses Lombok annotations (@Data, @NoArgsConstructor, @Builder) and 4-space indentation, while Manufacturer and OfflineSessions use hand-written getters/setters and tab indentation.
Fix: Use hand-written getters/setters and tab indentation

[P4-A19-6] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/OfflineSessions.java | Line: 5
Description: The class declaration public class OfflineSessions implements Serializable{ is missing a space before the opening brace {.
Fix: Review and remediate the identified issue

[P4-A19-7] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/OfflineSessions.java | Line: 27-29
Description: There are three unnecessary blank lines at the end of the class body (lines 27-29) before the closing brace.
Fix: Review and remediate the identified issue

[P4-A19-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java | Line: 25-26
Description: The Pattern object is compiled as an instance field on every PackageEntry object. Since the regex "(\\d*)\\.?(\\d*)?\\.?(\\d*)?\\-(\\w*)" is a constant, the compiled Pattern should be a private static final field to avoid recompilation on every instantiation and reduce memory overhead.
Fix: Should be a private static final field to avoid recompilation on every instantiation and reduce memory overhead

[P4-A19-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java | Line: 36-54
Description: The initVersion(String version) method passes version directly to pattern.matcher(version) at line 38 without a null check.
Fix: Review and remediate the identified issue

[P4-A19-10] HIGH | File: src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java | Line: 26, 40
Description: The regex pattern (\\d*)\\.?(\\d*)?\\.?(\\d*)?\\-(\\w*) uses \\d* (zero or more digits) for the first capture group.
Fix: Should be added before parsing

[P4-A19-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/PackageEntry.java | Line: 57-68
Description: The compareTo method compares only major, minor, and patch fields, but Lombok's @Data annotation generates equals() using all fields (including name, fileName, url, env, and the Pattern instance).
Fix: Should imply x.equals(y))

[P4-A20-1] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Permissions.java | Line: 27
Description: The enabled field is declared as String, but the database schema (V1__create_baseline_schema.sql, line 1499) defines permission.enabled as boolean DEFAULT false.
Fix: Should be boolean (or Boolean) for type safety and clarity

[P4-A20-2] MEDIUM | File: `src/main/java/com/journaldev/spring/jdbc/model/Questions.java`, `src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java` | Line: N/A
Description: The project has a clear pattern (visible in Permissions.java, Driver.java, Company.java) of using Lombok @Data to generate getters, setters, toString, equals, and hashCode.
Fix: Use hand-written getters and setters and have no Lombok annotations at all

[P4-A20-3] MEDIUM | File: `src/main/java/com/journaldev/spring/jdbc/model/Questions.java`, `src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java` | Line: N/A
Description: Both classes implement Serializable and are used in List collections (e.g., List<Questions> in SessionController.java, List<ReportLists> in ResumeController.java), but neither overrides equals() or hashCode().
Fix: Implement Serializable and are used in List collections (e.g., List<Questions> in SessionController.java, List<ReportLists> in ResumeController.java), but neither overrides equals() or hashCode()

[P4-A20-4] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Questions.java | Line: 12
Description: The id field is declared as int (primitive). In the database, question.id is an auto-generated integer.
Fix: Use Long for ID fields

[P4-A20-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java | Line: 13, 17
Description: Same issue as A20-4. Both id and comp_id are declared as primitive int, while the project convention for similar model classes (Permissions, Driver, Company) is to use boxed Long or Integer.
Fix: Use boxed Long or Integer

[P4-A20-6] LOW | File: `src/main/java/com/journaldev/spring/jdbc/model/Permissions.java`, `src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java` | Line: N/A
Description: Fields like driver_id, comp_id, gsm_token, driver_name (in Permissions) and file_name, comp_id (in ReportLists) use snake_case, which violates standard Java naming conventions (camelCase).
Fix: Should be documented and ideally standardized

[P4-A20-7] INFO | File: `src/main/java/com/journaldev/spring/jdbc/model/Questions.java`, `src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java` | Line: N/A
Description: Both files contain an empty Javadoc comment block (/** */) above serialVersionUID, which appears to be auto-generated IDE boilerplate.
Fix: Should be removed for cleanliness

[P4-A20-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java | Line: 5, 10
Description: The class is named ReportLists but the comment on line 10 says // subscription table and queries in ResumeController.java (line 268) show it maps to the subscription table.
Fix: Review and remediate the identified issue

[P4-A20-9] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java | Line: 5-51
Description: No toString() method is defined. When ReportLists instances appear in logs (as they do in ResumeController), only the default Object.toString() (class name + hash) is shown, providing no useful information for debugging.
Fix: Review and remediate the identified issue

[P4-A20-10] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/Permissions.java | Line: 22
Description: The driver_name field does not exist in the permission database table. In CompanyDAO.java (line 177), it is populated by concatenating first_name and last_name from a joined query: .driver_name(rs.getString("first_name") + " " + rs.getString("last_name")).
Fix: Review and remediate the identified issue

[P4-A20-11] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/ReportLists.java | Line: 5
Description: The class declaration reads public class ReportLists implements Serializable{ (no space before {). Standard Java style requires a space before the opening brace: Serializable {.
Fix: Review and remediate the identified issue

[P4-A21-1] MEDIUM | File: `src/main/java/com/journaldev/spring/jdbc/model/Reports.java`, `src/main/java/com/journaldev/spring/jdbc/model/Result.java` | Line: N/A
Description: The codebase uses Lombok @Data on many model classes (e.g., ResponseWrapper, AuthenticationResponse, Driver, Company, Equipment, ErrorMessage, and at least 15 others), but Reports and Result use manually written getters and setters.
Fix: Should adopt @Data and @NoArgsConstructor to match the project convention

[P4-A21-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/ResponseWrapper.java | Line: 18-19
Description: The fields data and metadata are declared as Object, which completely erases type information. This is a leaky abstraction: consumers must cast the returned data, which bypasses compile-time type checking and can cause ClassCastException at runtime.
Fix: Use ClassCastException at runtime

[P4-A21-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/ResponseWrapper.java | Line: 13-15
Description: The class declaration and Javadoc open on the same line: public class ResponseWrapper implements Serializable {/.
Fix: Should either be removed (since it is empty) or moved above the class declaration with proper formatting

[P4-A21-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Result.java | Line: 15-17, 32-48
Description: Fields start_time, finish_time, and session_id use snake_case, which violates the Java naming convention (camelCase).
Fix: Use @JsonProperty annotations to map between conventions rather than encoding database naming into Java field names

[P4-A21-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Result.java | Line: 18, 50, 53
Description: The field arrAnswers is declared as ArrayList<Answers> and the getter/setter use ArrayList<Answers> rather than the List<Answers> interface.
Fix: Should also be used instead of new ArrayList<Answers>() to reduce redundancy (Java 7+)

[P4-A21-6] LOW | File: `src/main/java/com/journaldev/spring/jdbc/model/Reports.java`, `src/main/java/com/journaldev/spring/jdbc/model/Result.java` | Line: N/A
Description: Neither Reports nor Result override toString(), equals(), or hashCode(). This means they inherit Object's identity-based implementations, which makes debugging harder (no meaningful string representation) and prevents correct behavior in collections that rely on value equality (e.g., HashSet, HashMap).
Fix: Should either adopt Lombok or add explicit implementations

[P4-A21-7] INFO | File: `src/main/java/com/journaldev/spring/jdbc/model/Reports.java`, `src/main/java/com/journaldev/spring/jdbc/model/ResponseWrapper.java`, `src/main/java/com/journaldev/spring/jdbc/model/Result.java` | Line: N/A
Description: All three files contain an empty Javadoc block (/** */) above the serialVersionUID field. These appear to be IDE-generated placeholder comments that were never filled in.
Fix: Should be removed to reduce noise

[P4-A21-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Reports.java | Line: 5
Description: The class Reports represents a single report entry with fields field, object, and value. However, the plural name Reports suggests a collection.
Fix: Review and remediate the identified issue

[P4-A21-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/ResponseWrapper.java | Line: 18-19
Description: A search across the entire src directory for calls to setData(), getData(), setMetadata(), or getMetadata() returned zero results.
Fix: Should be removed to avoid confusion

[P4-A21-10] INFO | File: src/main/java/com/journaldev/spring/jdbc/model/Reports.java | Line: 12-14
Description: The field names field, object, and value are extremely generic and do not convey domain meaning. In particular, object shadows the concept of java.lang.Object, which can be confusing in code review and IDE autocompletion.
Fix: Review and remediate the identified issue

[P4-A22-1] MEDIUM | File: `src/main/java/com/journaldev/spring/jdbc/model/Results.java`, `src/main/java/com/journaldev/spring/jdbc/model/Services.java` | Line: N/A
Description: The Roles class uses Lombok annotations (@Data, @NoArgsConstructor, @Builder) to auto-generate getters, setters, equals, hashCode, and toString.
Fix: Use Lombok while the rest do not

[P4-A22-2] MEDIUM | File: `src/main/java/com/journaldev/spring/jdbc/model/Results.java`, `src/main/java/com/journaldev/spring/jdbc/model/Services.java` | Line: N/A
Description: Fields and methods use snake_case naming (e.g., message_id, getMessage_id(), unit_id, getUnit_id(), acc_hours, service_due, last_serv, next_serv, serv_duration, driver_id).
Fix: Use messageId, getMessageId(), unitId, getUnitId(), etc

[P4-A22-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Results.java | Line: 5
Description: The comment reads //for the web service return return with the word "return" duplicated. This is a minor copy-paste typo.
Fix: Review and remediate the identified issue

[P4-A22-4] MEDIUM | File: `src/main/java/com/journaldev/spring/jdbc/model/Results.java`, `src/main/java/com/journaldev/spring/jdbc/model/Services.java` | Line: N/A
Description: Both Results and Services implement Serializable and are used as data transfer objects but lack equals(), hashCode(), and toString() overrides.
Fix: Implement Serializable and are used as data transfer objects but lack equals(), hashCode(), and toString() overrides

[P4-A22-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Services.java | Line: 6
Description: The class declaration public class Services implements Serializable{ is missing a space before the opening brace {.
Fix: Correct formatting with a space before {

[P4-A22-6] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Roles.java | Line: 31-53
Description: The RoleId enum currently contains only one constant (ROLE_COMPANY_GROUP), yet the fromId() method iterates over values() and throws IllegalArgumentException for unrecognized names.
Fix: Review and remediate the identified issue

[P4-A22-7] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Roles.java | Line: 44-52
Description: A search across the entire src directory reveals no call sites for Roles.RoleId.fromId(). The only usage of the RoleId enum is the static import of ROLE_COMPANY_GROUP and its getId() method in DriverService.java (line 22 and 74).
Fix: Review and remediate the identified issue

[P4-A22-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Roles.java | Line: 18-21
Description: Roles.java uses a mix of tab-based indentation (matching the rest of the codebase) and space-based indentation within the @Builder constructor parameter alignment.
Fix: Review and remediate the identified issue

[P4-A22-9] INFO | File: `src/main/java/com/journaldev/spring/jdbc/model/Results.java`, `src/main/java/com/journaldev/spring/jdbc/model/Roles.java`, `src/main/java/com/journaldev/spring/jdbc/model/Services.java` | Line: N/A
Description: All three files contain empty Javadoc comment blocks (/** */) immediately above the serialVersionUID field.
Fix: Add visual noise without providing any documentation value

[P4-A22-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Roles.java | Line: 34
Description: The id field in the RoleId enum is declared as private String id without the final modifier. Since enum constants are inherently immutable singletons, their fields should be final to prevent accidental mutation.
Fix: Should be final to prevent accidental mutation

[P4-A22-11] INFO | File: `src/main/java/com/journaldev/spring/jdbc/model/Results.java`, `src/main/java/com/journaldev/spring/jdbc/model/Roles.java`, `src/main/java/com/journaldev/spring/jdbc/model/Services.java` | Line: N/A
Description: All three model classes use plural names (Results, Roles, Services) even though each instance represents a single entity (one result, one role, one service record).
Fix: Use plural names (Results, Roles, Services) even though each instance represents a single entity (one result, one role, one service record)

[P4-A23-1] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Sessions.java | Line: 13-21, 23-82
Description: All field names and their corresponding getter/setter methods use snake_case (driver_id, unit_id, start_time, finish_time, photo_left_url, photo_right_url, photo_front_url, photo_back_url, prestart_required) instead of the standard Java camelCase convention (driverId, unitId, startTime, etc.).
Fix: Use snake_case (driver_id, unit_id, start_time, finish_time, photo_left_url, photo_right_url, photo_front_url, photo_back_url, prestart_required) instead of the standard Java camelCase convention (driverId, unitId, startTime, etc.)

[P4-A23-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Sessions.java | Line: 15-16
Description: The start_time and finish_time fields are typed as String rather than java.time.LocalDateTime, java.time.Instant, java.sql.Timestamp, or similar temporal types.
Fix: Review and remediate the identified issue

[P4-A23-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/Usage.java | Line: 13
Description: The time field is typed as String rather than an appropriate date/time type. Same concern as A23-2.
Fix: Review and remediate the identified issue

[P4-A23-4] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Usage.java | Line: 14
Description: The field initializer new BigDecimal(0) creates a new object each time a Usage instance is constructed.
Fix: Review and remediate the identified issue

[P4-A23-5] LOW | File: `src/main/java/com/journaldev/spring/jdbc/model/Sessions.java`, `Types.java`, `Usage.java` | Line: N/A
Description: None of the three model classes override toString(), equals(), or hashCode(). No model class in the entire model package (43 classes examined) overrides any of these methods.
Fix: Review and remediate the identified issue

[P4-A23-6] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Sessions.java | Line: 5
Description: The class name Sessions (plural) represents a single session entity, not a collection. Usage in SessionController confirms this: ResponseEntity<Sessions> returns one session, and List<Sessions> is used for collections.
Fix: Review and remediate the identified issue

[P4-A23-7] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Types.java | Line: 5
Description: Same issue as A23-6. Types represents a single equipment type (with id, name, url fields).
Fix: Review and remediate the identified issue

[P4-A23-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/Types.java | Line: 5
Description: The name Types is extremely generic and provides no domain context about what kind of type it represents.
Fix: Review and remediate the identified issue

[P4-A23-9] INFO | File: `src/main/java/com/journaldev/spring/jdbc/model/Sessions.java`, `Types.java`, `Usage.java` | Line: N/A
Description: All three files contain an empty block Javadoc comment (/** * */) immediately above the serialVersionUID field.
Fix: Review and remediate the identified issue

[P4-A23-10] INFO | File: `src/main/java/com/journaldev/spring/jdbc/model/Types.java`, `Usage.java` | Line: N/A
Description: Types.java and Usage.java declare class Types implements Serializable{ and class Usage implements Serializable{ with no space before the opening brace.
Fix: Declare class Types implements Serializable{ and class Usage implements Serializable{ with no space before the opening brace

[P4-A23-11] INFO | File: `src/main/java/com/journaldev/spring/jdbc/model/Sessions.java`, `Types.java` | Line: N/A
Description: The id, driver_id, and unit_id fields in Sessions, and id in Types, use primitive int rather than Integer.
Fix: Use primitive int rather than Integer

[P4-A24-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/model/User.java | Line: 25
Description: The password field has no @JsonIgnore annotation and Lombok's @Data generates a public getter for it.
Fix: Should return a DTO that excludes the password

[P4-A24-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/User.java | Line: 3
Description: The import lombok.* is a wildcard import. This obscures which Lombok annotations are actually in use (@Data, @NoArgsConstructor, @EqualsAndHashCode, @ToString, @Builder) and can hide unused-import warnings.
Fix: Use (@Data, @NoArgsConstructor, @EqualsAndHashCode, @ToString, @Builder) and can hide unused-import warnings

[P4-A24-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/UserResponse.java | Line: 15-27
Description: UserResponse.java uses tab indentation while User.java and APKUpdaterException.java use 4-space indentation.
Fix: Should standardize on one style (the majority appears to be 4 spaces)

[P4-A24-4] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/UserResponse.java | Line: 15-17
Description: There is an empty Javadoc block (/** */) above serialVersionUID. This is auto-generated IDE boilerplate that adds no informational value.
Fix: Should either be removed or replaced with a meaningful comment

[P4-A24-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/UserResponse.java | Line: 13
Description: The class declaration reads implements Serializable{ with no space before the opening brace. Standard Java formatting requires a space: implements Serializable {.
Fix: Review and remediate the identified issue

[P4-A24-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/UserResponse.java | Line: 21, 23
Description: userCreateDate and lastModifiedDate are declared as String. Using String for date/time values loses type safety — callers cannot perform date arithmetic, comparison, or formatting without first parsing these strings.
Fix: Should be java.time.Instant, java.time.LocalDateTime, or java.util.Date with appropriate Jackson serialization annotations (e.g., @JsonFormat)

[P4-A24-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/model/User.java | Line: 30, 32-39
Description: The roles field is initialized to new HashSet<>() at declaration (line 30), but the @Builder constructor (lines 32-39) does not accept or set roles.
Fix: Use @Builder on the class level or if the @AllArgsConstructor pattern is introduced, roles could silently become null

[P4-A24-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/model/User.java | Line: 41
Description: The method addRoles(Roles role) takes a single Roles parameter but uses the plural name addRoles. The conventional naming would be addRole(Role role).
Fix: Should be addRole(Role role)

[P4-A24-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterException.java | Line: 4
Description: APKUpdaterException extends RuntimeException (which is Serializable) but does not declare a serialVersionUID.
Fix: Use deserialization failures if the class changes between JVM versions

[P4-A24-10] INFO | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterException.java | Line: 1
Description: APKUpdaterException resides in the service package alongside APKUpdaterService. While this is not incorrect, exception classes are often placed in a dedicated exception package or alongside the model layer for better separation.
Fix: Change is strictly needed

[P4-A25-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 31-34
Description: AWS access key ID (AKIA**REDACTED**) and secret access key (****REDACTED****) are hardcoded as a static field.
Fix: Should be supplied via environment variables, IAM roles, AWS Secrets Manager, or the default credential provider chain

[P4-A25-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 73-74
Description: Every uploaded file is given CannedAccessControlList.PublicRead permission, making all uploaded objects publicly accessible on the internet.
Fix: Should be set to private unless there is an explicit, documented business requirement for public access

[P4-A25-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java | Line: 36-40
Description: The fields targetLocation, fileName, and imageExt are protected mutable instance fields on a Spring singleton bean.
Fix: Should be local variables returned/passed rather than shared mutable state

[P4-A25-4] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 44-47
Description: The loadImageAsResource override returns null unconditionally. This is a contract violation of the FileStorageService interface.
Fix: Should either throw UnsupportedOperationException with a descriptive message or be properly implemented to load resources from S3

[P4-A25-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 75-77
Description: The AmazonServiceException in uploadObject is caught and only logged. The method returns normally, and saveImage() returns the filename as if the upload succeeded.
Fix: Should be propagated or the method should return a success/failure indicator

[P4-A25-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 67-70
Description: AmazonS3.doesBucketExist(String) has been deprecated in favor of doesBucketExistV2. More importantly, automatically creating an S3 bucket at upload time is a dangerous pattern: it can create buckets with incorrect permissions, in the wrong region, or without required encryption/logging policies.
Fix: Should be handled by infrastructure provisioning (e.g., Terraform/CloudFormation), not application code

[P4-A25-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/AWSFileStorageService.java | Line: 50-56, 65
Description: connectAWSS3() builds a new AmazonS3 client on every call to uploadObject. The AmazonS3Client is designed to be created once and reused; it manages its own internal HTTP connection pool.
Fix: Should be initialized once (e.g., in a @PostConstruct method or as a @Bean)

[P4-A25-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java | Line: 66
Description: In the catch (IOException e) block at line 65-67, the APKUpdaterException is constructed with only a message string but not the caught IOException cause.
Fix: Should be new APKUpdaterException("...", e)

[P4-A25-9] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java | Line: 39-43
Description: The builder chain inside the lambda has inconsistent indentation. .fileName(filename) (line 40), .baseUrl(baseUrl) (line 41), .version(version) (line 42), and .name(name) (line 43) each have different indentation levels.
Fix: Should be aligned consistently

[P4-A25-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java | Line: 65
Description: The method Util.generateRadomName() contains a typo ("Radom" instead of "Random"). While this is technically a finding in Util.java, the call site is in AbstractFileStorageService.
Fix: Should be renamed to generateRandomName()

[P4-A25-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java | Line: 25
Description: The Pattern object is compiled from a constant regex string and is immutable/thread-safe. It should be declared as private static final Pattern PATTERN = ... rather than an instance field.
Fix: Should be declared as private static final Pattern PATTERN = ... rather than an instance field

[P4-A25-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java | Line: 46-47
Description: The lambda in the map() call returns null when the filename does not match the pattern (line 46). While the subsequent .filter(p -> p != null ...) guards against the null, returning null from a map() operation is an anti-pattern in Java streams.
Fix: Use flatMap with Optional to avoid null values in the stream entirely

[P4-A25-13] INFO | File: `src/main/java/com/journaldev/spring/jdbc/service/APKUpdaterService.java` (references `APKUpdaterException.java`) | Line: N/A
Description: APKUpdaterException extends RuntimeException (which is Serializable) but does not declare a serialVersionUID.
Fix: Use deserialization issues if the class structure changes

[P4-A25-14] INFO | File: src/main/java/com/journaldev/spring/jdbc/service/AbstractFileStorageService.java | Line: 40, 58
Description: The field imageExt is initialized to ".jpg" at line 40. If saveImage successfully determines the MIME type, it overwrites imageExt at line 58.
Fix: Use whatever extension was set by the last successful detection, not ".jpg"

[P4-A26-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/BootstrapService.java | Line: 30-33
Description: The code uses new Flyway() and then calls flyway.setBaselineOnMigrate(), flyway.setDataSource(), and flyway.setLocations().
Fix: Review and remediate the identified issue

[P4-A26-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/BootstrapService.java | Line: 55
Description: The migrate() method in the inner FlywayBean class uses System.out.println("Flyway is disabled, database migration ignored...") instead of the SLF4J logger.
Fix: Review and remediate the identified issue

[P4-A26-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/BootstrapService.java | Line: 5-6
Description: Logger and LoggerFactory are imported but never used anywhere in the class. No logger field is declared.
Fix: Review and remediate the identified issue

[P4-A26-4] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/BootstrapService.java | Line: 40
Description: FlywayBean is declared as a public non-static inner class. This means every FlywayBean instance holds a hidden reference to the enclosing BootstrapService instance, preventing the BootstrapService (and its DataSource) from being garbage-collected as long as the FlywayBean Spring bean is alive.
Fix: Should be declared static (or extracted to a top-level class)

[P4-A26-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: 48
Description: In getUser(), the access token is appended directly to the URL as a query parameter: "...&accessToken="+accessToken.
Fix: Should be passed in an Authorization header (e.g., Bearer <token>) instead

[P4-A26-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: 62, 101
Description: Both getUser() and authenticationRequest() call e.printStackTrace() before logging the error with SLF4J. printStackTrace() writes to System.err, which bypasses the logging framework, produces unstructured output, and duplicates the error information.
Fix: Should be removed and replaced with log.error(method + " error:", e) to include the full stack trace in the structured log

[P4-A26-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: 36, 77
Description: Both getUser() and authenticationRequest() create a new RestTemplate instance on each invocation. RestTemplate is thread-safe and designed to be reused.
Fix: Should be injected as a Spring bean or at minimum declared as a class-level field

[P4-A26-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: 60, 99
Description: Both methods catch Exception (the broadest checked+unchecked type), log the message, and then return a default-constructed empty response object.
Fix: Should propagate to callers, since getUser() unconditionally calls authResponse.getSessionToken() (line 34) on the potentially empty result, which could return null and lead to "null" being embedded in the URL

[P4-A26-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: 48, 89
Description: Both methods construct URLs using "http://localhost:" hardcoded as the host. While the port is configurable via configuration.getCognitoAPIPort(), the host and protocol (http vs https) are not.
Fix: Should be externalized to configuration

[P4-A26-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: 38-42
Description: In getUser(), an ArrayList<MediaType> and HttpHeaders object are created and configured (lines 38-42), but headers is never passed to the RestTemplate call on line 50 (restTemplate.getForEntity(uri, UserResponse.class) does not accept headers).
Fix: Should be removed

[P4-A26-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: 32, 71
Description: Both methods manually construct a String method variable via this.getClass().getName() + " : methodName " and prepend it to every log message.
Fix: Review and remediate the identified issue

[P4-A26-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: 54, 93
Description: Both getUser() and authenticationRequest() log "HttpStatus Succuss" instead of "HttpStatus Success".
Fix: Review and remediate the identified issue

[P4-A26-13] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/DriverAlreadyExistException.java | Line: 3
Description: DriverAlreadyExistException (and its parent DriverServiceException) extend RuntimeException (which is Serializable) but do not declare a serialVersionUID.
Fix: Use deserialization failures if the class structure changes between versions

[P4-A26-14] INFO | File: src/main/java/com/journaldev/spring/jdbc/service/DriverAlreadyExistException.java | Line: 3
Description: The class name DriverAlreadyExistException is grammatically awkward; the standard English and Java convention would be DriverAlreadyExistsException (third-person singular).
Fix: Review and remediate the identified issue

[P4-A26-15] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/CognitoService.java | Line: N/A
Description: CognitoService.java uses a mix of tabs and spaces for indentation. For example, the class-level field declaration (line 28) uses spaces, while method bodies (lines 31-67) predominantly use tabs.
Fix: Review and remediate the identified issue

[P4-A27-1] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 79
Description: driver.setComp_id(new Long(compId)) uses the Long(int) constructor, which was deprecated in Java 9 and removed in Java 16+.
Fix: Use a compilation failure if the project is built against JDK 16 or later

[P4-A27-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 88-93
Description: A six-line block of commented-out code exists in registerDriver(). It appears to be remnant SMS-sending logic (SendMessage.sendMail).
Fix: Should be removed

[P4-A27-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 85-87
Description: In registerDriver() (lines 85, 87) the code correctly uses SLF4J parameterized logging: log.info("Start Sending Email to {}", email).
Fix: Should use parameterized {} placeholders

[P4-A27-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 108
Description: The reset password is embedded in a plain-text email message string: "Your ForkliftIQ360 Account Password is reset to " + pass.
Fix: Should use a time-limited token/link rather than sending the actual password

[P4-A27-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 86, 111
Description: SendEmail.sendMail(...) is a static utility call. This makes the DriverService class impossible to unit-test in isolation without a real email subsystem (or bytecode-level mocking via PowerMock/Mockito inline).
Fix: Should be abstracted behind an interface and injected, consistent with the Spring DI pattern already used for userDAO, companyDAO, etc

[P4-A27-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 39-49
Description: All four dependencies (userDAO, companyDAO, configuration, driverDAO) use field injection via @Autowired.
Fix: Use it: (a) makes dependencies explicit, (b) enables immutability (final fields), (c) allows the class to be instantiated in tests without a Spring context, and (d) prevents the class from being in a partially-constructed state

[P4-A27-7] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 54-63
Description: The authenticate method calls driverDAO.findByEmailAndPassword(email, password).orElse(null) to extract the value, performs a null check, and then re-wraps in Optional.ofNullable(driver).
Fix: Use Optional.ifPresent() or Optional.map() to perform the side-effect (updating last login time) and return the Optional directly, e.g.: java Optional<Driver> opt = driverDAO.findByEmailAndPassword(email, password); opt.ifPresent(d -> { try { driverDAO.updateLastLoginTime(d); } ... }); return opt;

[P4-A27-8] LOW | File: `src/main/java/com/journaldev/spring/jdbc/service/DriverServiceException.java`, `EntityNotFoundException.java` | Line: N/A
Description: DriverServiceException and EntityNotFoundException both extend RuntimeException (which is Serializable), but neither declares a serialVersionUID.
Fix: Change between compiler versions and break serialization compatibility

[P4-A27-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/EntityNotFoundException.java | Line: 6
Description: EntityNotFoundException resides in the service package and is thrown from the DAO layer (DriverDAOImpl), yet it carries @ResponseStatus(HttpStatus.NOT_FOUND) — a Spring Web annotation.
Fix: Should be handled by a @ControllerAdvice or at the controller level

[P4-A27-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/EntityNotFoundException.java | Line: 9
Description: EntityNotFoundException only provides a single-argument constructor (String message). It lacks a (String message, Throwable cause) constructor, unlike DriverServiceException which provides both.
Fix: Review and remediate the identified issue

[P4-A27-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 37
Description: The generated password length is 8 characters. While the password does include upper, lower, digit, and special character rules, NIST SP 800-63B and OWASP guidelines recommend a minimum of 12-15 characters for randomly generated passwords/passphrases.
Fix: Review and remediate the identified issue

[P4-A27-12] INFO | File: src/main/java/com/journaldev/spring/jdbc/service/DriverService.java | Line: 26
Description: The @Transactional annotation is applied at the class level, meaning every public method (including authenticate, which is read-only, and generateRandomPassword, which touches no data) will open a transaction.
Fix: Consider using @Transactional(readOnly = true) at the class level and overriding with @Transactional on mutating methods, or applying @Transactional only on methods that require it

[P4-A28-1] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/FileNotFoundException.java | Line: 7
Description: FileNotFoundException extends FileStorageException (which itself extends RuntimeException), making it Serializable.
Fix: Use InvalidClassException if the class structure changes between serialization and deserialization (e.g., across distributed systems or session stores)

[P4-A28-2] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/FileNotFoundException.java | Line: 7
Description: The custom class com.journaldev.spring.jdbc.service.FileNotFoundException shares the simple name FileNotFoundException with java.io.FileNotFoundException.
Fix: Consider renaming to something more descriptive such as FileResourceNotFoundException or StorageFileNotFoundException to avoid ambiguity

[P4-A28-3] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/FileNotFoundException.java | Line: 9-11
Description: FileNotFoundException only provides a single-argument (String message) constructor, while its parent FileStorageException provides both (String message) and (String message, Throwable cause) constructors.
Fix: Review and remediate the identified issue

[P4-A28-4] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/FileStorageService.java | Line: 7-11
Description: The FileStorageService interface defines the public contract for file storage operations but has no Javadoc on the interface itself or on either method.
Fix: Review and remediate the identified issue

[P4-A28-5] INFO | File: src/main/java/com/journaldev/spring/jdbc/service/FileNotFoundException.java | Line: 6
Description: The @ResponseStatus(HttpStatus.NOT_FOUND) annotation on FileNotFoundException relies on Spring's DefaultHandlerExceptionResolver to translate the exception into an HTTP 404 response.
Fix: Review and remediate the identified issue

[P4-A28-6] INFO | File: `src/main/java/com/journaldev/spring/jdbc/service/FileNotFoundException.java`, `src/main/java/com/journaldev/spring/jdbc/service/FileStorageException.java` | Line: N/A
Description: Both exception classes reside in com.journaldev.spring.jdbc.service alongside service interfaces and implementations.
Fix: Review and remediate the identified issue

[P4-A28-7] INFO | File: src/main/java/com/journaldev/spring/jdbc/service/FileStorageException.java | Line: 3
Description: FileStorageException extends RuntimeException, making it an unchecked exception. This is an intentional design choice consistent with Spring conventions (Spring generally favors unchecked exceptions).
Fix: Review and remediate the identified issue

[P4-A29-1] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java | Line: 26
Description: The loadUserByUsername method implements the UserDetailsService interface but does not use the @Override annotation.
Fix: Use the @Override annotation

[P4-A29-2] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java | Line: 27
Description: The method signature declares throws UsernameNotFoundException, DataAccessException, but the DataAccessException is a Spring unchecked exception (extends RuntimeException) and does not need to be declared.
Fix: Use it implies a checked exception contract

[P4-A29-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java | Line: 38
Description: In buildUserFromUserEntity, the enabled flag is hardcoded to true rather than being derived from the User entity.
Fix: Use active for account disabling, the semantics are inverted: accountNonLocked (line 42) is being used for what is typically an enabled check, while enabled is unconditionally true

[P4-A29-4] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java | Line: 40-41
Description: Both accountNonExpired and credentialsNonExpired are hardcoded to true. These flags exist in Spring Security's User constructor to support account expiration and credential rotation policies.
Fix: Should explain why they are always true

[P4-A29-5] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java | Line: 34, 49
Description: On line 34, the method parameter type is com.journaldev.spring.jdbc.model.User (fully qualified) even though User is already imported at line 5.
Fix: Rename the domain model class reference

[P4-A29-6] INFO | File: src/main/java/com/journaldev/spring/jdbc/service/LocalFileStorageService.java | Line: 24
Description: The call filePath.toString() inside the string concatenation is redundant. Java's string concatenation with + automatically calls toString() on objects.
Fix: Review and remediate the identified issue

[P4-A29-7] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/SaveFileInfo.java | Line: 8-10
Description: The class uses @Data and @Builder together. @Builder generates an all-args constructor and makes it package-private, while @Data generates a no-args constructor only if no other constructors exist.
Fix: Review and remediate the identified issue

[P4-A29-8] INFO | File: src/main/java/com/journaldev/spring/jdbc/service/SaveFileInfo.java | Line: 17
Description: The size field uses primitive long while all other fields are reference types (String). With @Builder, the size field will default to 0 if not explicitly set, which could mask missing data.
Fix: Review and remediate the identified issue

[P4-A29-9] HIGH | File: src/main/java/com/journaldev/spring/jdbc/service/LocalFileStorageService.java | Line: 13
Description: LocalFileStorageService is a Spring @Service (singleton by default) and inherits mutable instance fields from AbstractFileStorageService: targetLocation (line 36), fileName (line 38), and imageExt (line 40).
Fix: Should be local variables within saveImage(), not instance fields

[P4-A29-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java | Line: 22-23
Description: The dao field uses field injection (@Autowired on a private field). Modern Spring best practice recommends constructor injection, which makes dependencies explicit, supports immutability (final fields), simplifies testing (no reflection needed to inject mocks), and enables compile-time dependency validation.
Fix: Review and remediate the identified issue

[P4-A29-11] INFO | File: src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java | Line: 44
Description: The collection is instantiated as new ArrayList<GrantedAuthority>() rather than using the diamond operator new ArrayList<>().
Fix: Review and remediate the identified issue

[P4-A29-12] INFO | File: src/main/java/com/journaldev/spring/jdbc/service/UserDetailsServiceImpl.java | Line: 49
Description: The Spring Security User construction on line 49 is a single line with 7 constructor arguments spanning well beyond 120 characters.
Fix: Should be broken across multiple lines for clarity

[P4-A30-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 109
Description: The sendPost method sets a hardcoded X-AUTH-TOKEN header value ("w6_zaejLjssvw02XqIiKdVmv7kP6nOHAw2Ve5mj-qug").
Fix: Should be externalized to configuration (e.g., Spring @Value injection, environment variable, or a secrets manager)

[P4-A30-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 19-20, 52-58, 72, 130-131
Description: The class uses private static String saveFilePath and private static String fileName as shared mutable state across all callers.
Fix: Should be local variables or returned in a result object

[P4-A30-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 69-87
Description: In both downloadFile and sendPost, InputStream and FileOutputStream are opened inside a try block but are closed with explicit .close() calls in the happy path only.
Fix: Review and remediate the identified issue

[P4-A30-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 84-87, 145-148
Description: Both downloadFile and sendPost catch Exception broadly and call only e.printStackTrace(). This swallows all exceptions silently from the caller's perspective: the method completes normally, "File downloaded" is printed (line 89/150), and the caller has no indication that the file write failed.
Fix: Should propagate

[P4-A30-5] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 61-64, 73, 89, 91, 120-122, 133, 150, 152
Description: The class uses System.out.println extensively for diagnostic output. In a Spring/server application, stdout output bypasses the logging framework, cannot be filtered by log level, has no timestamps or contextual metadata, and may interleave unpredictably with other output.
Fix: Should use SLF4J or the project's configured logging framework

[P4-A30-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/Configuration.java | Line: 4-5
Description: The imports org.simpleframework.xml.Element and org.simpleframework.xml.Root are present but neither @Element nor @Root annotations appear anywhere in the class.
Fix: Should be removed

[P4-A30-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 12
Description: HttpsURLConnection is imported but never used in active code. Its only reference is in commented-out code on line 102.
Fix: Should be removed along with the commented-out line

[P4-A30-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 8
Description: java.io.OutputStream is imported but never used. The variable os on line 113 is typed as the concrete OutputStream returned by getOutputStream(), but the declared import is for the abstract class which is redundant since FileOutputStream (already imported) is the concrete type used elsewhere.
Fix: Should be removed

[P4-A30-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 42-45, 97, 102
Description: Several blocks of commented-out code remain: - Lines 42-45: Commented-out debug notes (//Content-Type = application/pdf, etc.) that appear to be leftover from development/debugging. - Line 97: // HTTP POST request -- this is a comment, not commented-out code, but line 102 is: // HttpsURLConnection con = (HttpsURLConnection) obj.openConnection();...
Fix: Should be removed and tracked through version control history if needed

[P4-A30-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/DateUtil.java | Line: 43-47
Description: The method parseDateTimeWithSlashes parses the input string with format "MM/dd/yyyy HH:mm:ss", then immediately reformats the resulting Date with "dd/MM/yyyy HH:mm:ss", then parses that reformatted string again.
Fix: Should be simplified to a single parse

[P4-A30-11] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/DateUtil.java | Line: 12, 26
Description: SimpleDateFormat is instantiated on every call to parseDate and formatDate. While this avoids the well-known thread-safety issue of shared SimpleDateFormat instances, it is unnecessarily wasteful.
Fix: Use java.time APIs (LocalDate, LocalDateTime) instead of the legacy java.util.Date and Calendar APIs

[P4-A30-12] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/DateUtil.java | Line: 3, 14
Description: org.springframework.util.StringUtils.isEmpty(Object) is deprecated as of Spring Framework 5.3. The recommended replacement is ObjectUtils.isEmpty or !StringUtils.hasLength(String).
Fix: Review and remediate the identified issue

[P4-A30-13] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/Configuration.java | Line: 13-41
Description: The @Value annotations use tab indentation while the field declarations use space indentation. For example, line 13 (@Value) uses a tab while line 14 (private String userSetupMsg) uses spaces.
Fix: Use space indentation

[P4-A30-14] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: N/A
Description: The downloadFile method body (lines 29-94) uses primarily space-based indentation, while sendPost (lines 98-156) uses tab-based indentation.
Fix: Should be applied

[P4-A30-15] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/Configuration.java | Line: 40-41
Description: The cognitoAPIPassword field is injected via @Value("${cognitoAPIPassword}"). While the value itself is externalized (better than hardcoding), this design stores the Cognito API password as a plain String in a Spring bean that lives for the entire application lifecycle.
Fix: Should be encrypted (e.g., using Jasypt or Spring Cloud Vault)

[P4-A30-16] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 98
Description: The sendPost method declares throws Exception, which is the broadest possible checked exception signature.
Fix: Should declare specific exceptions (e.g., throws IOException, MalformedURLException) to communicate the actual failure modes

[P4-A30-17] INFO | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 105
Description: The comment reads //add reuqest header instead of //add request header. Minor typo.
Fix: Add request header

[P4-A30-18] INFO | File: src/main/java/com/journaldev/spring/jdbc/util/HttpDownloadUtility.java | Line: 121
Description: The debug output reads "Post jason data : " instead of "Post JSON data : ". This is a typo that would appear in logs/stdout.
Fix: Review and remediate the identified issue

[P4-A31-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/util/SMTPAuthenticator.java | Line: 9-10
Description: AWS AKIAJ-prefixed access key ID and secret key are hardcoded directly in the source file as plaintext strings.
Fix: Review and remediate the identified issue

[P4-A31-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/SMTPAuthenticator.java | Line: 1-14
Description: A codebase-wide search for SMTPAuthenticator returns only its own class declaration. No other file imports or references this class.
Fix: Should be rotated immediately since they have been exposed in version control history

[P4-A31-3] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/RuntimeConf.java | Line: 1-5
Description: A codebase-wide search for RuntimeConf (excluding RuntimeConfig) returns only its own class declaration.
Fix: Should be removed

[P4-A31-4] MEDIUM | File: `src/main/java/com/journaldev/spring/jdbc/util/RuntimeConf.java` and `src/main/java/com/journaldev/spring/jdbc/controller/RuntimeConfig.java` | Line: N/A
Description: Two classes with nearly identical names exist in different packages: RuntimeConf (in util) and RuntimeConfig (in controller).
Fix: Should be consolidated

[P4-A31-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/SendEmail.java | Line: 32-34, 47-49, 50-51, 52-54
Description: The sendMail method has four exception catch blocks, and all of them handle errors by either calling e.printStackTrace() or System.out.println().
Fix: Should use a proper logging framework (e.g., SLF4J/Logback) and either rethrow a checked exception or return a boolean success indicator

[P4-A31-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/SendEmail.java | Line: 52-54
Description: The outer try-catch catches Throwable, which includes Error subclasses such as OutOfMemoryError and StackOverflowError.
Fix: Should be narrowed to Exception at most, and the caught MessagingException on line 50 already covers the mail-specific case

[P4-A31-7] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/SendEmail.java | Line: 4, 6, 7
Description: The file uses wildcard imports (java.util.*, javax.mail.*, javax.mail.internet.*). Wildcard imports reduce code clarity by making it impossible to see at a glance which specific classes are used, and they can cause ambiguous type resolution if classes with the same simple name exist in multiple imported packages.
Fix: Should be preferred

[P4-A31-8] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/SMTPAuthenticator.java | Line: 5
Description: The class declaration uses extends javax.mail.Authenticator with a fully-qualified name, despite javax.mail.PasswordAuthentication being imported on line 3.
Fix: Use the simple name in the extends clause

[P4-A31-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/RuntimeConf.java | Line: 4
Description: RuntimeConf.database is a public static non-final field. Any code in the application can reassign this value at any time, creating unpredictable behavior and making the system hard to reason about.
Fix: Should be accessed through a method with appropriate synchronization or encapsulated in a proper configuration management pattern

[P4-A31-10] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/SendEmail.java | Line: 29-34
Description: The setRecipients call on line 30-31 is wrapped in its own try-catch that catches Exception broadly and only prints to stdout.
Fix: Should either rethrow or abort the method to avoid the cascading failure

[P4-A32-1] CRITICAL | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 65-66
Description: AWS SES SMTP credentials (AKIA**REDACTED** / ****REDACTED****) are hardcoded directly in the getPasswordAuthentication() method.
Fix: Should be rotated immediately since they are already committed to the repository

[P4-A32-2] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 112
Description: The SMS sending URL is constructed by concatenating RuntimeConfig.USERNAME, RuntimeConfig.PASSWORD, and RuntimeConfig.API_ID directly into a query string.
Fix: Review and remediate the identified issue

[P4-A32-3] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 119
Description: The sendMail method always returns true even when Transport.send() throws an exception (caught and printed at line 112-114) or when any other Throwable is caught (line 116-118).
Fix: Review and remediate the identified issue

[P4-A32-4] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 163
Description: DataInputStream.readLine() has been deprecated since JDK 1.1 because it does not properly convert bytes to characters.
Fix: Should be replaced with BufferedReader(new InputStreamReader(is, StandardCharsets.UTF_8))

[P4-A32-5] HIGH | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 29-32
Description: Connection, Statement, ResultSet, and query are declared as instance fields with package-private (default) access.
Fix: Should be local variables within the init() method

[P4-A32-6] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 54, 61, 66, 71
Description: Both classes declare an SLF4J logger but then use e.printStackTrace() and System.out.println() for error reporting in catch blocks.
Fix: Should use logger.error(...) with the exception as the second argument

[P4-A32-7] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 20
Description: The wildcard import java.io.* is used instead of explicit imports. This hides the actual dependencies of the class (which are InputStream, DataInputStream, BufferedInputStream, and IOException), can cause ambiguous class resolution if multiple packages export the same name, and violates standard Java style guides.
Fix: Use ambiguous class resolution if multiple packages export the same name, and violates standard Java style guides

[P4-A32-8] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 78-88
Description: The Javadoc block above send_sms_message uses PHP-style parameter annotations (@param integer $id, @param string $mobile_no, @param string $event_name, etc.) that do not correspond to the actual method parameters (String msg, String mobile_no).
Fix: Review and remediate the identified issue

[P4-A32-9] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 36, 90, 97
Description: Java naming conventions are violated in multiple places. Method names use snake_case (send_sms_message, init) instead of camelCase.
Fix: Should be "Random"

[P4-A32-10] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 154-168
Description: The readLines method opens a URL stream and wraps it in a DataInputStream, but if an exception occurs between openStream() (line 161) and dis.close() (line 166), the stream is leaked.
Fix: Should cascade, relying on this without explicit structure is fragile

[P4-A32-11] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 46-58
Description: The SMTP host (email-smtp.us-east-1.amazonaws.com), port (465), and all connection properties are hardcoded.
Fix: Should be externalized to application configuration

[P4-A32-12] MEDIUM | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 116
Description: The outer catch block in sendMail catches Throwable rather than Exception. This will catch Error subclasses like OutOfMemoryError and StackOverflowError, which should generally be allowed to propagate.
Fix: Should target Exception (or more specific mail-related exceptions) instead

[P4-A32-13] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 32
Description: The String query field is declared but never assigned or read anywhere in the class. This is dead code and should be removed.
Fix: Should be removed

[P4-A32-14] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 25
Description: The logger field is declared but never used in any method of Util.java. All error handling goes through System.out.println and e.printStackTrace() instead.
Fix: Should be used (replacing the stdout/stderr calls) or removed to eliminate the dead field and its import

[P4-A32-15] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 36-37
Description: The sendMail method accepts rName (recipient name) and sName (sender name) parameters, but neither is used in the method body.
Fix: Add confusion to the API and callers pass dummy values like "unknown"

[P4-A32-16] LOW | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 98
Description: The attachment parameter is checked using attachment.equalsIgnoreCase("") but if attachment is null, this will throw a NullPointerException.
Fix: Review and remediate the identified issue

[P4-A32-17] INFO | File: src/main/java/com/journaldev/spring/jdbc/util/Util.java | Line: 39-41
Description: Three lines of JNDI-based session lookup code are commented out. This appears to be a remnant of a prior implementation where the mail session was configured via the application server's JNDI context.
Fix: Should be removed; version control preserves history if it is ever needed again

[P4-A32-18] INFO | File: src/main/java/com/journaldev/spring/jdbc/util/SendMessage.java | Line: 1-169
Description: The file uses a mix of tabs and spaces for indentation, and indentation levels are inconsistent throughout.
Fix: Review and remediate the identified issue

[P4-ACFG-1] CRITICAL | File: settings.xml | Line: 9, 14
Description: The Maven settings.xml file contains plaintext server passwords for TomcatServerUat (C!1admin) and TomcatServerAzure (pyx1s!96).
Fix: Should never be checked into a project repository

[P4-ACFG-2] CRITICAL | File: pom.xml | Line: 29, 32, 46, 76
Description: Flyway database passwords are hardcoded in plaintext inside Maven profiles: gmtp-postgres (local, line 29), fleetiq360 (local, line 32; dev, line 46), and C!1admin (UAT, line 76).
Fix: Should be externalized to environment variables or a secrets manager and injected at build time, not stored in pom.xml

[P4-ACFG-3] HIGH | File: `environment.dev.properties`, `environment.prod.properties`, `environment.uat.properties` | Line: 15-16
Description: All three environment property files contain cognitoAPIUsername=ciiadmin and cognitoAPIPassword=ciiadmin in plaintext.
Fix: Should be externalized via a secrets manager or environment variables, and the prod/UAT environments should use distinct, strong credentials

[P4-ACFG-4] CRITICAL | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 113-117
Description: OAuth2 client secrets are hardcoded in the Spring Security configuration: client 987654321 with secret 8752361E593A573E86CA558FFD39E and client fleetiq360 with secret rihah8eey4faibuengaixo6leiL1awii.
Fix: Should be externalized or stored in a database with hashing, not in XML config files

[P4-ACFG-5] CRITICAL | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 74
Description: The authentication manager uses <password-encoder hash="md5"/>. MD5 is a cryptographically broken hash function unsuitable for password storage.
Fix: Should use bcrypt, scrypt, or Argon2 for password hashing

[P4-ACFG-6] MEDIUM | File: pom.xml | Line: 27-32
Description: The local Maven profile defines flyway.url, flyway.user, and flyway.password twice. Lines 27-29 set them to jdbc:postgresql://127.0.0.1/PreStart with user postgres and password gmtp-postgres.
Fix: Use the last-defined value, making the first set dead code

[P4-ACFG-7] MEDIUM | File: pom.xml | Line: 57-64
Description: The prod Maven profile defines flyway.url but omits flyway.user and flyway.password. If the Flyway migration plugin is invoked with the prod profile, it will use unresolved ${flyway.user} and ${flyway.password} properties (no default in the top-level <properties> block), resulting in a build failure or authentication error.
Fix: Use unresolved ${flyway.user} and ${flyway.password} properties (no default in the top-level <properties> block), resulting in a build failure or authentication error

[P4-ACFG-8] MEDIUM | File: pom.xml | Line: 69
Description: The uat profile has <activeByDefault>true</activeByDefault>. Running mvn without explicitly specifying a profile will use UAT settings, including the UAT database URL and credentials.
Fix: Use a developer who forgets to specify -Plocal or -Pdev will inadvertently point Flyway migrations or Tomcat deployments at the UAT environment

[P4-ACFG-9] HIGH | File: `environment.prod.properties`, `environment.uat.properties` | Line: N/A
Description: These two files are byte-for-byte identical. Both use imageURL pointing to ec2-54-86-82-22.compute-1.amazonaws.com, the same upload/package/log paths, and critically imagePrefix=uat- in both files.
Fix: Should be documented with a comment in each file

[P4-ACFG-10] HIGH | File: environment.prod.properties | Line: 11
Description: The imagePrefix property in the prod environment file is set to uat- instead of an expected prod- prefix.
Fix: Review and remediate the identified issue

[P4-ACFG-11] MEDIUM | File: pom.xml | Line: 88
Description: The Splunk artifact repository is configured with http://splunk.jfrog.io/splunk/ext-releases-local (plain HTTP).
Fix: Should be changed to https://

[P4-ACFG-12] MEDIUM | File: pom.xml | Line: 12, 231, 236
Description: The Spring Framework version is 3.2.14.RELEASE but Spring Security is 3.1.1.RELEASE. The Spring Security 3.1.x line is designed for Spring Framework 3.1.x, not 3.2.x.
Fix: Should be managed via a property variable for consistency

[P4-ACFG-13] HIGH | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 114
Description: The OAuth2 client 987654321 has access-token-validity="0", which means tokens never expire. A non-expiring access token is a security risk: if a token is compromised, it remains valid indefinitely.
Fix: Should have a reasonable expiry period

[P4-ACFG-14] MEDIUM | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 13-14
Description: The endpoints /oauth/cache_approvals and /oauth/uncache_approvals are configured with security="none" and accompanied by the comment <!-- Just for testing... -->.
Fix: Should be removed from production configuration or protected behind an admin role

[P4-ACFG-15] LOW | File: src/main/resources/logback.xml | Line: 28-30, 47-49
Description: The logback configuration defines two <root> elements. The first (line 28) attaches the FILE appender, and the second (line 47) attaches the socket appender.
Fix: Should be under a single <root> element

[P4-ACFG-16] LOW | File: src/main/resources/logback.xml | Line: 21-24
Description: A DEBUG-level logger for com.journaldev.spring.jdbc.controller.APKUpdaterController is explicitly left in with the comment "Temporary enable DEBUG to resolve issue in production environment." This temporary debug setting has not been reverted and will produce verbose debug output for that controller in all environments.
Fix: Should be removed after the issue is resolved

[P4-ACFG-17] LOW | File: src/main/resources/logback.xml | Line: 16, 43
Description: The logger name com.journaldev.spring is defined twice: once on line 16 (level=INFO, appender=FILE) and again on line 43 (level=INFO, additivity=false, appender=socket).
Fix: Should be consolidated into a single logger definition with both appender-refs if both outputs are desired

[P4-ACFG-18] MEDIUM | File: src/main/webapp/WEB-INF/web.xml | Line: 9, 19
Description: The file servlet-context.xml is referenced both as the DispatcherServlet's contextConfigLocation (line 9) and in the root context's contextConfigLocation (line 19).
Fix: Should load MVC-specific beans

[P4-ACFG-19] LOW | File: src/main/resources/fleetiq360ws.properties | Line: 10
Description: The acceptURL property is hardcoded to https://pandora.fleetiq360.com/pandora/acceptDriver?token= and is not parameterized via Maven resource filtering like other URL properties.
Fix: Use different frontend domains, this creates a cross-environment leak where driver acceptance links in dev/UAT emails point to the production domain

[P4-ACFG-20] LOW | File: src/main/resources/META-INF/context.xml | Line: 2
Description: The antiJARLocking="true" attribute on the <context> element was deprecated in Tomcat 7.0.x and removed in Tomcat 8.0.9.
Fix: Should be removed to avoid confusion, or replaced with the current equivalent if JAR locking avoidance is still needed

[P4-ACFG-21] LOW | File: `src/main/webapp/WEB-INF/web.xml` (line 30), `src/main/webapp/WEB-INF/spring/appServlet/servlet-context.xml` (line 57) | Line: N/A
Description: The JNDI DataSource name jdbc/PreStartDB does not correspond to the application name (fleetiq360ws) and is a leftover from a prior project called "PreStart" (also visible in the duplicated local profile flyway.url on pom.xml line 27).
Fix: Should either be renamed or documented with an explanatory comment

[P4-ACFG-22] LOW | File: pom.xml | Line: 269-272
Description: The project depends on com.amazonaws:aws-java-sdk:1.11.163, which is the full AWS SDK bundle containing hundreds of service modules.
Fix: Should be replaced with specific module dependencies such as aws-java-sdk-s3 and aws-java-sdk-cognitoidp

[P4-ACFG-23] LOW | File: pom.xml | Line: 167-170
Description: The commons-io dependency uses groupId org.apache.commons with version 1.3.2. The canonical groupId for Commons IO is commons-io (not org.apache.commons).
Fix: Use confusion or classpath conflicts if another dependency transitively pulls in commons-io:commons-io

[P4-ACFG-24] INFO | File: src/main/webapp/WEB-INF/spring/spring-security.xml | Line: 82-83
Description: Line 83 contains a commented-out InMemoryTokenStore bean with the surrounding comment (line 82) still referencing "currently an in memory implementation" despite the active configuration using JdbcTokenStore.
Fix: Should both be removed

[P4-ACFG-25] INFO | File: Multiple (logback.xml, servlet-context.xml, spring-security.xml) | Line: N/A
Description: Configuration files show inconsistent indentation styles: logback.xml mixes 4-space and 3-space indentation; servlet-context.xml mixes tabs and spaces (tab-indented bean definitions next to space-indented multipart resolver); spring-security.xml mixes tabs and spaces.
Fix: Review and remediate the identified issue

[P4-ACFG-26] MEDIUM | File: pom.xml | Line: 335-338
Description: The Flyway Maven plugin embeds postgresql:postgresql:9.1-901.jdbc3, which uses the old postgresql groupId (replaced by org.postgresql since 2014) and targets JDBC 3 for PostgreSQL 9.1.
Fix: Should be updated to org.postgresql:postgresql with a current version

[P4-ACFG-27] MEDIUM | File: pom.xml | Line: 60-61
Description: The prod profile defines an empty <tomcat.url></tomcat.url> (line 61) and does not define flyway.user or flyway.password.
Fix: Review and remediate the identified issue
