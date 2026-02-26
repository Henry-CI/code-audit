# Security Audit: RuntimeConf.java

**File:** `src/main/java/com/util/RuntimeConf.java`
**Audit Date:** 2026-02-26
**Auditor:** Automated Security Audit Pass 1
**Branch:** master

---

## Summary

`RuntimeConf.java` is the central configuration class for the entire `forkliftiqadmin` application. Every constant defined here is `public static`, meaning any class in the application can read it directly. Because this file is compiled into the deployable WAR/JAR, every value here is baked into the binary and stored in version control. There is no use of environment variables, a secrets manager, a properties file, or any other externalisation mechanism. This single file surfaces a dense cluster of high- and critical-severity findings.

---

## Findings

### CRITICAL: Hardcoded AWS EC2 Hostname Exposing Production Infrastructure

**File:** `RuntimeConf.java` (line 60)
**Description:**
```java
public static String APIURL = "http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/";
```
The AWS EC2 public DNS hostname `ec2-52-5-205-104.compute-1.amazonaws.com` encodes the public IPv4 address `52.5.205.104` directly in its name. Any person who reads this source file (or decompiles the WAR) knows the exact public IP of a production EC2 instance. Combined with the HTTP-only protocol (see next finding), this fully identifies the target server without any authentication on the transport layer.

**Risk:**
- Directly exposes a live production server IP to anyone with source or binary access, enabling targeted network reconnaissance, port scanning, and direct attack against the host.
- IP is discoverable from version control history even after rotation.
- Changing the IP requires a recompile and redeployment rather than a configuration change.

**Recommendation:**
Replace the hardcoded hostname with an environment variable or a JNDI/properties-file entry such as `api.pdf.url`. Use an internal hostname, load-balancer DNS name, or private VPC endpoint rather than a public EC2 DNS name. Rotate the EC2 instance and assign a new Elastic IP so the currently-exposed address is no longer in use.

---

### CRITICAL: API URL Uses HTTP — No Transport Encryption

**File:** `RuntimeConf.java` (line 60)
**Description:**
```java
public static String APIURL = "http://ec2-52-5-205-104.compute-1.amazonaws.com/api/export/pdf/";
```
The PDF export API endpoint uses plain `http://`. This is the same endpoint that `HttpDownloadUtility` calls while attaching the hardcoded bearer token `noCwHkr7lofpFL0ZAL2EzynUBLKN1Krcs8bSunismUE` in an `Authorization` header (identified in a prior audit pass). Over an unencrypted channel, the auth token, the PDF content, and all request metadata travel in cleartext and are trivially interceptable by any on-path observer (within AWS, within the data centre network, or between Tomcat and EC2).

**Risk:**
- Hardcoded auth token (identified separately) is exposed in plaintext on the wire on every API call.
- PDF report content — which may contain personal and operational data — is transmitted without encryption.
- Any network-level attacker can read or tamper with requests and responses.
- Violates PCI-DSS, HIPAA, and most enterprise security policies that mandate TLS for data in transit.

**Recommendation:**
Change the scheme to `https://` and ensure the target server presents a valid TLS certificate. Enforce TLS 1.2 minimum. Externalise the URL from source code as described above.

---

### CRITICAL: Hardcoded Application Base URL Using HTTP

**File:** `RuntimeConf.java` (line 8)
**Description:**
```java
public static String url = "http://prestart.collectiveintelligence.com.au/";
```
The application's own base URL is hardcoded as plain HTTP. This value is likely used to construct links in outgoing emails or redirects. Any link sent to users over HTTP is susceptible to SSL-stripping attacks. The domain `collectiveintelligence.com.au` is also an internal company domain embedded in source code.

**Risk:**
- Any email links generated using this URL will point to an unencrypted endpoint; credentials entered by users following those links traverse the wire in cleartext.
- Exposes the internal/canonical hostname used by the application.
- Cannot be changed per environment without a recompile.

**Recommendation:**
Change to `https://` and externalise via environment variable or properties file so that development, staging, and production environments can each specify their own URL without a code change.

---

### HIGH: Hardcoded Internal Receiver Email Address (Live Production)

**File:** `RuntimeConf.java` (line 16)
**Description:**
```java
public static String RECEIVER_EMAIL = "hui@ciifm.com"; //live
```
A production email address is hardcoded with an inline comment `//live` confirming this is the live production recipient. The domain `ciifm.com` appears to be an internal company domain. This address receives system-generated alert and notification emails.

**Risk:**
- The comment `//live` confirms the value is actively used in production, meaning any change requires a code change, rebuild, and redeployment — a high-risk operation just to update a notification address.
- If this person leaves the organisation, the address may become invalid or re-assigned to a new owner who receives sensitive operational data.
- Exposing internal staff email addresses in source code leaks organisational information to anyone with repository access.

**Recommendation:**
Move to a configuration property (e.g., `notification.receiver.email`), loaded from a properties file or environment variable, and use a role/group address (e.g., `alerts@company.com`) rather than a personal one.

---

### HIGH: Hardcoded Debug/Internal Email Address

**File:** `RuntimeConf.java` (line 58)
**Description:**
```java
public static String debugEmailRecipet = "hui@collectiveintelligence.com.au";
```
A personal staff email address is hardcoded as the debug email recipient. The variable name `debugEmailRecipet` (note the typo) suggests this is used to send internal debug or error notifications directly to a developer's inbox.

**Risk:**
- Debug emails may contain stack traces, internal data, or sensitive operational details; delivering them to a single personal address is a data governance concern.
- Same rotation/departure risk as `RECEIVER_EMAIL`.
- Exposes internal staff identity and corporate email domain in source.

**Recommendation:**
Externalise to a configuration property. Route debug/error emails to a shared team mailbox or a structured logging/alerting platform (e.g., a SIEM or PagerDuty) rather than a personal inbox.

---

### HIGH: Hardcoded Brand Email Address — Linde/FleetIQ Tenant

**File:** `RuntimeConf.java` (line 7)
**Description:**
```java
public static String emailFromLinde = "info@fleetiq360.com";
```
A hardcoded "from" email address is used for communications sent under the Linde/FleetIQ branded tenant. The presence of a separate constant for this tenant's email (alongside `LINDEDB` pointing to a separate schema) confirms the multi-tenancy architecture is partially hardcoded rather than data-driven.

**Risk:**
- If the Linde brand email address needs to change (domain expiry, rebranding, deliverability), a code change, recompile, and redeployment is required.
- Hardcoding tenant-specific values in a shared configuration class means other tenants could potentially be impacted by changes to this constant.
- Exposes the existence and identity of the Linde/FleetIQ white-label tenant to anyone reading the source.

**Recommendation:**
Tenant-specific configuration (email addresses, branding, database schema names) must be stored in a tenant configuration table or a per-tenant properties file and loaded at runtime.

---

### HIGH: Hardcoded Application "From" Email Address

**File:** `RuntimeConf.java` (line 6)
**Description:**
```java
public static String emailFrom = "info@forkliftiq360.com";
```
The primary "from" address for all outgoing application email is hardcoded. This is the address users see as the sender on registration confirmations, password resets, and alert emails.

**Risk:**
- Any domain change, email infrastructure migration, or SPF/DKIM reconfiguration requires a recompile.
- Exposes the application's primary email domain in source.

**Recommendation:**
Externalise to `app.email.from` in a properties file or JNDI environment entry.

---

### HIGH: Hardcoded Secondary Database Schema Name (`LINDEDB`)

**File:** `RuntimeConf.java` (line 53)
**Description:**
```java
public static String LINDEDB = "fleeiq";
```
The database schema name `fleeiq` used for the Linde/FleetIQ secondary tenant is hardcoded. Any DAO or query that appends this schema name to build a fully-qualified table reference is tightly coupled to this value. Note the apparent typo in the value (`fleeiq` vs the expected `fleetiq`); if this is an unintentional truncation it could indicate the wrong schema is being referenced.

**Risk:**
- Schema names differ between development, staging, and production databases. Hardcoding forces developers to change code (not config) when deploying to different environments.
- A typo in the schema name (`fleeiq`) may cause silent data routing errors, directing queries to the wrong schema or throwing runtime SQL exceptions.
- Exposes the schema naming convention used in the production database to anyone reading the source.

**Recommendation:**
Store the schema name in a database configuration entry or JNDI environment variable. Verify whether `fleeiq` is intentional or a typo for `fleetiq`.

---

### HIGH: Hardcoded AWS S3 Bucket URL Exposing Bucket Name and Region

**File:** `RuntimeConf.java` (line 62)
**Description:**
```java
public static String cloudImageURL = "https://s3.amazonaws.com/forkliftiq360/image/";
```
The S3 bucket name `forkliftiq360` and its path prefix are hardcoded. While this URL uses HTTPS (unlike `APIURL`), the bucket name is a globally unique AWS identifier. Knowledge of the bucket name enables direct enumeration attempts against the bucket, especially if bucket ACLs are misconfigured.

**Risk:**
- Exposes the exact S3 bucket name and path structure, enabling targeted S3 enumeration, listing (if `s3:ListBucket` is not blocked), or direct access to object keys if the bucket is not fully private.
- Cannot be changed per environment without a recompile (development and staging may use different buckets).
- Path-style S3 URLs (`s3.amazonaws.com/bucket/`) are a legacy format that AWS has indicated it is deprecating.

**Recommendation:**
Externalise the S3 base URL to a configuration property. Ensure the `forkliftiq360` bucket has a bucket policy that denies public `s3:GetObject` and `s3:ListBucket` unless required. Consider using a CloudFront distribution URL instead of a direct S3 URL to decouple the CDN origin from source code.

---

### HIGH: Hardcoded Cognito View/Table Name Exposing Database Schema

**File:** `RuntimeConf.java` (line 64)
**Description:**
```java
public static final String v_user = "v_cognitousers";
```
The database view name `v_cognitousers` used for Cognito user data is hardcoded. The `v_` prefix naming convention confirms this is a database view, and the name `cognitousers` reveals that the application stores or mirrors AWS Cognito user records in a local database view.

**Risk:**
- Confirms to an attacker that the application uses AWS Cognito for identity management and that Cognito user data is accessible via a local database view, narrowing the attack surface for SQL injection targeting user/auth data.
- Exposes the database object naming convention.
- Cannot be changed per environment without a recompile.

**Recommendation:**
Externalise to a configuration property. Review whether the `v_cognitousers` view exposes more Cognito user attributes (e.g., sub, email, groups) than is strictly necessary for the queries that use it.

---

### MEDIUM: Hardcoded Application Title Leaking Internal Project Name

**File:** `RuntimeConf.java` (line 4)
**Description:**
```java
public static String projectTitle = "PreStart";
```
The internal project code name "PreStart" is hardcoded. This value likely appears in page titles, email subjects, or UI labels. More importantly, it may be inconsistent with the branded product name (`ForkliftIQ`/`FleetIQ`) shown to external users.

**Risk:**
- Leaks the internal development project name to end users if used directly in UI elements or emails.
- Inconsistency between internal code names and external brand names can cause confusion in phishing analysis (emails saying "PreStart" may be flagged as suspicious by recipients expecting "ForkliftIQ").

**Recommendation:**
Externalise to a `app.title` configuration property so that each branded tenant can supply its own title.

---

### MEDIUM: Hardcoded JNDI DataSource Name

**File:** `RuntimeConf.java` (line 5)
**Description:**
```java
public static String database = "jdbc/PreStartDB";
```
The JNDI datasource lookup name is hardcoded. While JNDI names are typically less sensitive than credentials, hardcoding the datasource name tightly couples application code to the server configuration.

**Risk:**
- The datasource name `jdbc/PreStartDB` exposes the internal naming convention used on the Tomcat server.
- If the JNDI name needs to change (e.g., for multi-tenancy, environment promotion, or renaming), a code change and recompile is required.
- Low direct risk but indicative of a broader pattern of configuration-in-code rather than externalisation.

**Recommendation:**
Externalise to a `datasource.jndi.name` property. Consider using Spring (or a dependency injection framework appropriate for the stack) to inject the datasource rather than performing JNDI lookups by hardcoded name.

---

### MEDIUM: Hardcoded Default Timezone

**File:** `RuntimeConf.java` (line 11)
**Description:**
```java
public static String DEFAUTL_TIMEZONE = "Australia/Sydney";
```
The application timezone is hardcoded to `Australia/Sydney`. The constant name also contains a typo (`DEFAUTL_TIMEZONE`). For a multi-tenant application potentially serving users in different regions, this forces all date/time display through a single server timezone.

**Risk:**
- Incorrect timezone handling can cause timestamp discrepancies in audit logs, alert times, and report data — a compliance concern for applications that log safety-critical forklift pre-start check results.
- Cannot be changed per deployment environment or per tenant without a code change.

**Recommendation:**
Externalise to a `app.default.timezone` configuration property. For a multi-tenant application, store timezone preference per tenant in the database. Fix the typo (`DEFAUTL` -> `DEFAULT`).

---

### MEDIUM: Internal Company Name Hardcoded

**File:** `RuntimeConf.java` (line 36)
**Description:**
```java
public static String COMP = "COLLECTIVE INTELLIGENCE";
```
The internal/vendor company name is hardcoded. If this string appears in UI elements, PDF reports, or emails generated for end customers, it exposes the white-label vendor identity to clients who may be under the impression they are using a product from a different brand.

**Risk:**
- Potential commercial/contractual breach if white-label clients have agreements that prevent disclosure of the underlying software vendor.
- Cannot be updated without a recompile.

**Recommendation:**
Move company branding to a per-tenant configuration table or a configurable properties file.

---

### MEDIUM: Hardcoded Email Subject Lines — Possible Legacy Brand Exposure

**File:** `RuntimeConf.java` (line 13)
**Description:**
```java
public static String REGISTER_SUBJECT = "Pandora Registration Successful";
```
The registration email subject contains the name "Pandora" — apparently a legacy project or product name that predates the ForkliftIQ branding. If this subject line is still used in outgoing emails, users receive correspondence referencing an unrecognised product name.

**Risk:**
- Recipients receiving an email titled "Pandora Registration Successful" may treat it as phishing.
- Leaks the internal development history and legacy project name.

**Recommendation:**
Update the subject line to use the current product name and externalise it to a configuration property to avoid future brand mismatches.

---

### LOW: Hardcoded File System Paths

**File:** `RuntimeConf.java` (lines 32–34, 37)
**Description:**
```java
public static String UPLOAD_FOLDER = "/doc/";
public static String BROCHURE_FOLDER = "/doc/brochure.pdf";
public static String XML_FOLDER = "configue.xml";
public static String PDF_FOLDER = "/temp/";
```
Upload, brochure, XML configuration, and temporary PDF paths are all hardcoded as relative or absolute path strings. The path `/temp/` is particularly notable — on Linux this resolves to a top-level `/temp/` directory which may or may not exist, rather than the standard `/tmp/`. Also note the typo in `XML_FOLDER` (`configue.xml` instead of `configure.xml` or `config.xml`).

**Risk:**
- Hardcoded paths prevent different environments from using different file system layouts.
- Writing to `/temp/` (if it resolves as an absolute path) may fail or succeed depending on the OS configuration, potentially causing silent failures when generating PDF reports.
- The typo in `XML_FOLDER` could cause the application to fail to locate its configuration XML at runtime.

**Recommendation:**
Externalise file paths to configuration properties. Use `java.io.tmpdir` (the JVM's platform-independent temp directory) rather than a hardcoded `/temp/` path. Fix the typo in `configue.xml`.

---

### INFO: Role Name Constants Defined in Shared Configuration

**File:** `RuntimeConf.java` (lines 44–48)
**Description:**
```java
public static String ROLE_COMP = "ROLE_COMPANY_GROUP";
public static String ROLE_SYSADMIN = "ROLE_SYS_ADMIN";
public static String ROLE_DEALER = "ROLE_DEALER";
public static String ROLE_SUBCOMP = "ROLE_SUBCOMP";
public static String ROLE_SITEADMIN = "ROLE_SITE_ADMIN";
```
Role name strings are defined here as mutable (`non-final`) public static fields. Because they are not `final`, any code in the application could theoretically overwrite them at runtime (e.g., `RuntimeConf.ROLE_SYSADMIN = "ROLE_USER"`), which could silently break authorisation checks.

**Risk:**
- Mutable public static role name strings are a subtle authorisation integrity risk. If any code path overwrites a role constant, every subsequent authorisation check using that constant would use the modified value.
- Low probability but high impact if exploited.

**Recommendation:**
Declare all role constants as `public static final String`. This is a one-line change per constant and eliminates the mutability risk entirely.

---

### INFO: Checklist Session Timeout Hardcoded

**File:** `RuntimeConf.java` (line 50)
**Description:**
```java
public static long CHECKLIST_SECONDS = 600;
```
The checklist session timeout (600 seconds / 10 minutes) is hardcoded. This is not a security credential, but it is a security-relevant configuration value: if this timeout is too long it could allow a logged-in forklift operator session to be hijacked after the operator has walked away from the terminal.

**Risk:**
- Safety-critical application context: a 10-minute unattended session on a forklift pre-start terminal is operationally significant.
- Cannot be tuned per deployment without a code change.

**Recommendation:**
Externalise to a `checklist.session.timeout.seconds` configuration property so that different operational environments can set appropriate timeouts.

---

## Cross-Reference with Previously Identified Issues

| Previously Identified Issue | Status in This File |
|---|---|
| `APIURL` is HTTP not HTTPS | Confirmed — line 60, marked CRITICAL |
| `LINDEDB` references secondary schema | Confirmed — line 53, marked HIGH |
| `emailFromLinde` hardcoded email | Confirmed — line 7, marked HIGH |
| Cognito service reference | Confirmed — `v_cognitousers` view name on line 64, marked HIGH |
| Hardcoded API auth token `noCwHkr7lofpFL0ZAL2EzynUBLKN1Krcs8bSunismUE` | NOT present in this file — identified previously in `HttpDownloadUtility`; transmitted over the HTTP `APIURL` defined here |

---

## Finding Count

```
CRITICAL: 3 / HIGH: 6 / MEDIUM: 5 / LOW: 1 / INFO: 2
```
