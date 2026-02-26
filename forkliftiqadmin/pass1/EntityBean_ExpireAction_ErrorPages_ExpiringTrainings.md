# Pass 1 Audit — EntityBean / EntityNotFoundException / ExpireAction / error pages / expiringTrainings.jsp

**Files:**
1. `src/main/java/com/bean/EntityBean.java`
2. `src/main/java/com/service/EntityNotFoundException.java`
3. `src/main/java/com/action/ExpireAction.java`
4. `src/main/webapp/error/error.html`
5. `src/main/webapp/html-jsp/error.jsp`
6. `src/main/webapp/html-jsp/expiringTrainings.jsp`

**Date:** 2026-02-26

---

## Summary

This batch covers two data beans, a session-expiry action, two error pages, and a dashboard panel
JSP.  The most significant issues are: a plaintext `password` field with a public getter on a
`Serializable` bean (`EntityBean`), a complete absence of session invalidation inside
`ExpireAction`, unescaped output of user-controlled strings in `expiringTrainings.jsp` (XSS), and
exception message propagation in `error.jsp` that can expose internal details to callers.  No CSRF
token is present on any form rendered in this batch, but `expiringTrainings.jsp` is a read-only
panel so the primary CSRF surface is low for this particular file.

`EntityNotFoundException` embeds a fully-qualified class name and a raw record ID in its message
string; if that message is ever surfaced to an HTTP response it constitutes information disclosure.

---

## Findings

---

### HIGH: Password stored and exposed as plaintext String field with public getter

**File:** `src/main/java/com/bean/EntityBean.java` (lines 13, 45–50)

**Description:**
`EntityBean` declares `private String password` with a standard `getPassword()` / `setPassword()`
accessor pair.  The field is stored as a plain `String` — there is no hashing, no masking, and no
`@JsonIgnore` / `@XmlTransient` annotation to prevent serialization.  Because the class implements
`java.io.Serializable` (line 6), any serialization of an `EntityBean` instance (HTTP session
persistence, JVM clustering, cache serialization) will write the cleartext password to the
serialized byte stream.  Lombok `@Data` is NOT used here (the accessors are hand-written), but the
risk is identical: any reflection-based framework (e.g., Struts BeanUtils, Jackson, JAXB) can read
the password through the public getter.

**Risk:**
If the serialized session or cache entry is stored on disk or transmitted over the network, the
password is exposed.  If `EntityBean` is ever returned via a REST or Struts result that auto-maps
bean properties to JSON/XML, the password field will be included in the response.

**Recommendation:**
- Remove the `password` field from `EntityBean` entirely, or replace `String` with `char[]` and
  clear it after use.
- If the field must remain, annotate it with `@JsonIgnore` (Jackson) and `@XmlTransient` (JAXB)
  and override `toString()` to redact the value.
- Never store credentials in a session-bound bean; pass them only transiently during authentication
  and then discard.
- Long-term: store a salted hash (bcrypt / Argon2) rather than the plaintext credential.

---

### HIGH: ExpireAction does not invalidate the HTTP session

**File:** `src/main/java/com/action/ExpireAction.java` (lines 32–50)

**Description:**
`ExpireAction` is the action invoked when `sessCompId` is null — i.e., when the application
detects that the user's session is no longer valid.  The action's `execute` method:

1. Adds an `ActionMessage` for `error.expire`.
2. Reads a language cookie and sets a locale attribute.
3. Loads advertisements into `request` scope.
4. Forwards to the `"logout"` forward.

At no point does the code call `request.getSession().invalidate()` or even
`request.getSession(false)` to destroy the existing session.  The session object therefore remains
alive on the server with all its attributes intact.  An attacker who obtains the session cookie
(e.g., via network sniffing or XSS) can continue to use it after the user has been redirected to
the expiry/logout page.

Additionally, the action does not instruct the browser to delete the session cookie: there is no
call to expire or clear the `JSESSIONID` cookie in the `HttpServletResponse`.

**Risk:**
Session fixation / session hijacking.  An attacker holding a copy of the session cookie can
continue to act as the authenticated user even after the legitimate user has been redirected to the
expiry page.

**Recommendation:**
Add the following before the `return mapping.findForward("logout")` call:

```java
HttpSession session = request.getSession(false);
if (session != null) {
    session.invalidate();
}
// Expire the JSESSIONID cookie
Cookie sessionCookie = new Cookie("JSESSIONID", "");
sessionCookie.setMaxAge(0);
sessionCookie.setPath(request.getContextPath());
sessionCookie.setHttpOnly(true);
sessionCookie.setSecure(true);
response.addCookie(sessionCookie);
```

---

### HIGH: XSS — unescaped bean:write output of user-controlled driver data

**File:** `src/main/webapp/html-jsp/expiringTrainings.jsp` (lines 40–51)

**Description:**
The JSP iterates over `arrExpiringTrainings` and renders six bean properties directly into HTML
table cells using `<bean:write>` tags without the `filter="true"` attribute:

```jsp
<bean:write property="first_name" name="training"/>
<bean:write property="last_name"  name="training"/>
<bean:write property="email"      name="training"/>
<bean:write property="unit_name"  name="training"/>
<bean:write property="training_date"   name="training"/>
<bean:write property="expiration_date" name="training"/>
```

In Struts 1.x, `<bean:write>` defaults to `filter="false"` when the attribute is omitted —
meaning HTML metacharacters in the bean property are written verbatim to the response without
HTML-entity encoding.  All of the above properties (`first_name`, `last_name`, `email`,
`unit_name`, `training_date`, `expiration_date`) originate from the database and may contain
values entered by users or administrators; if any of those values contain `<script>`, event
handler attributes, or other HTML, the browser will execute them.

The `DriverTrainingBean` (`@Data`, `@Builder`, `Serializable`) confirms these fields are plain
`String` values with no sanitization.

**Risk:**
Stored XSS.  Any authenticated user or administrator who can influence the `first_name`,
`last_name`, `email`, or `unit_name` values in the database can inject arbitrary JavaScript that
executes in the browsers of all users who view the dashboard panel.

**Recommendation:**
Add `filter="true"` to every `<bean:write>` tag in this file:

```jsp
<bean:write property="first_name" name="training" filter="true"/>
<bean:write property="last_name"  name="training" filter="true"/>
<bean:write property="email"      name="training" filter="true"/>
<bean:write property="unit_name"  name="training" filter="true"/>
<bean:write property="training_date"   name="training" filter="true"/>
<bean:write property="expiration_date" name="training" filter="true"/>
```

Verify that `filter="true"` is the default (or is explicitly set) on every `<bean:write>` tag
across the entire application.

---

### MEDIUM: EntityNotFoundException embeds fully-qualified class name and record ID in message

**File:** `src/main/java/com/service/EntityNotFoundException.java` (lines 5–7)

**Description:**
The exception constructor builds its message as:

```java
super(clazz.getName() + " with ID " + id + " not found ");
```

`clazz.getName()` returns the fully-qualified Java class name (e.g.,
`com.bean.DriverBean`).  If this `RuntimeException` is ever caught and its `getMessage()` is
written to an HTTP response — directly, via a Struts error mapping, via `error.jsp`'s
`throw new Exception(e.getMessage())` re-throw, or via an unhandled exception page — the response
will reveal internal package structure and a database record identifier to the client.

This finding is elevated because `error.jsp` (see next finding) already re-throws with
`e.getMessage()`, creating a plausible path from this exception to the HTTP response.

**Risk:**
Information disclosure.  Attackers learn internal class names, package structure, and record ID
formats.  Record IDs can assist in enumeration attacks against other endpoints.

**Recommendation:**
- Use a generic message that does not include class names or raw IDs:
  `super("The requested resource was not found");`
- Log the detailed message server-side at WARN/ERROR level rather than embedding it in the
  exception message.
- Ensure `EntityNotFoundException` is caught in a global Struts exception handler that maps it to
  a safe error forward rather than letting it propagate to the JSP layer.

---

### MEDIUM: error.jsp re-throws exception with getMessage() — leaks internal error detail

**File:** `src/main/webapp/html-jsp/error.jsp` (lines 17–24)

**Description:**
The JSP wraps its rendering logic in a try/catch block.  On any caught exception, it:

1. Logs the exception server-side (`InfoLogger.logException`).
2. Re-throws a new `Exception` constructed with `e.getMessage()`.

```java
throw new Exception(e.getMessage());
```

`e.getMessage()` may contain file paths, SQL error text, class names, or other internal
implementation details.  Because the re-thrown exception propagates up the Struts / servlet
container chain, its message may be rendered by the container's default error page (which often
includes the full exception message in the HTTP response body) unless a properly configured
`<error-page>` in `web.xml` catches it and redirects to a safe page.

If this exception is an `EntityNotFoundException` (see finding above), the message will contain
the fully-qualified class name and record ID.

**Risk:**
Information disclosure.  Internal error details, SQL messages, or file-system paths could be
exposed to the browser.

**Recommendation:**
- Replace `throw new Exception(e.getMessage())` with a generic `throw new
  ServletException("An internal error occurred");` that does not carry the original message.
- Ensure `web.xml` maps `java.lang.Exception` and HTTP 500 to the safe `error/error.html` page.
- Do not propagate raw exception messages to the HTTP response layer under any circumstances.

---

### MEDIUM: expiringTrainings.jsp — NullPointerException risk from unguarded session attribute

**File:** `src/main/webapp/html-jsp/expiringTrainings.jsp` (lines 3–8)

**Description:**
The scriptlet at the top of the file calls `session.getAttribute("sessTimezone")` and immediately
calls `.contains(...)` on the result without a null check:

```java
String timezone = (String) session.getAttribute("sessTimezone");
if (!timezone.contains("US/") && !timezone.contains("Canada/")) {
```

If `sessTimezone` is not present in the session — for example, on first login before the attribute
is set, or after session partial-invalidation — `timezone` will be `null` and
`timezone.contains(...)` will throw a `NullPointerException`.  This uncaught exception would
propagate to the error handling chain and, depending on configuration, could expose stack-trace
information (see `error.jsp` finding).

**Risk:**
Application error / potential information disclosure.  Repeated triggering could be used to force
error-page rendering that leaks stack traces if the error-page configuration is incomplete.

**Recommendation:**
Add a null guard:

```java
String timezone = (String) session.getAttribute("sessTimezone");
if (timezone == null) { timezone = ""; }
if (!timezone.contains("US/") && !timezone.contains("Canada/")) { ... }
```

---

### LOW: error.html loads external font over HTTP (mixed content / supply-chain)

**File:** `src/main/webapp/error/error.html` (line 9)

**Description:**
The error page loads a Google Fonts stylesheet over plain HTTP:

```html
<link href='http://fonts.googleapis.com/css?family=Open+Sans:400,600,700' .../>
```

Loading over HTTP rather than HTTPS on a page that may itself be served over HTTPS creates a
mixed-content warning and, on some browsers, blocks the resource.  More critically, an active
network attacker (MITM) can substitute the CSS response with a stylesheet containing
`expression()` payloads (Internet Explorer) or inject a `<link>` tag that fetches attacker-
controlled scripts.

**Risk:**
Low.  Mixed content on an error page is unlikely to be exploited in practice, but represents a
supply-chain dependency on an external third party that should be served from a trusted, controlled
origin.

**Recommendation:**
- Change the scheme to `https://` or, preferably, self-host the font files.
- Apply a strict `Content-Security-Policy` header to all pages.

---

### LOW: error.html references IE8 conditional comments and legacy CDN scripts

**File:** `src/main/webapp/error/error.html` (lines 2–3, 12)

**Description:**
The page includes IE8 conditional comments and loads `html5shiv` and `respond.js` from
`oss.maxcdn.com`:

```html
<!--[if lt IE 9]><script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
<script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script><![endif]-->
```

These libraries target Internet Explorer < 9, a browser that has been end-of-life since 2016.
Depending on an external CDN for script delivery creates a third-party dependency: if
`oss.maxcdn.com` is compromised or the domain expires and is re-registered, an attacker could
serve malicious JavaScript to any client that renders the page with the conditional-comment branch
active.  Although modern browsers do not process conditional comments, this dead code should be
removed.

**Risk:**
Low in practice (IE < 9 is not in use), but represents unnecessary supply-chain exposure.

**Recommendation:**
Remove the IE8 conditional comment blocks and the associated CDN script tags entirely.

---

### LOW: ExpireAction does not set cache-control headers before forwarding

**File:** `src/main/java/com/action/ExpireAction.java` (lines 32–50)

**Description:**
After forwarding to `"logout"`, the browser may cache the authenticated page that was displayed
before the expiry action was triggered.  Without explicit `Cache-Control: no-store, no-cache` and
`Pragma: no-cache` headers, pressing the browser Back button after logout may display the
previously cached authenticated page from browser history.

**Risk:**
Low.  An attacker with physical access to the machine can view previously authenticated content
via the browser cache or history.

**Recommendation:**
Set cache-prevention headers before forwarding:

```java
response.setHeader("Cache-Control", "no-store, no-cache, must-revalidate");
response.setHeader("Pragma", "no-cache");
response.setDateHeader("Expires", 0);
```

---

### INFO: EntityBean implements Serializable without explicit serialVersionUID strategy

**File:** `src/main/java/com/bean/EntityBean.java` (lines 6, 10)

**Description:**
`EntityBean` implements `Serializable` and declares `serialVersionUID = 3895903590422186042L`.
The presence of a `password` field (see HIGH finding above) means that any serialized instance
contains the plaintext credential.  Beyond the password risk already noted, the class does not
implement `writeObject` / `readObject` to selectively exclude the password field from the
serialized form.

**Risk:**
Informational / supporting context for the HIGH password finding.

**Recommendation:**
Implement a custom `writeObject` that skips the `password` field, or remove the field from the
class entirely.

---

### INFO: EntityBean uses hand-written accessors — no Lombok @Data

**File:** `src/main/java/com/bean/EntityBean.java` (lines 17–56)

**Description:**
Unlike `DriverTrainingBean` (which uses Lombok `@Data`), `EntityBean` uses hand-written getters
and setters.  This is noted because the audit brief flagged Lombok `@Data` as a concern; `EntityBean`
does not use it, so Lombok-specific risks (auto-generated `toString()` that prints all fields
including `password`, `equals`/`hashCode` on mutable state) do not apply here as a Lombok issue.
However, the hand-written `getPassword()` produces the same exposure risk as Lombok `@Data` would.

**Risk:**
Informational.

**Recommendation:**
No action specific to Lombok.  See the HIGH password finding for remediation.

---

### INFO: DriverTrainingBean uses Lombok @Data — toString() will include email and comp_email

**File:** (referenced from expiringTrainings.jsp context) `src/main/java/com/bean/DriverTrainingBean.java`

**Description:**
`DriverTrainingBean` is annotated with `@Data`, which generates a `toString()` method that
includes all fields: `email`, `comp_email`, `first_name`, `last_name`, `driver_id`, `comp_id`, etc.
If an instance of this bean is ever logged (e.g., `log.debug(training.toString())`), all PII
fields will appear in the log file.  This is a data-privacy concern (GDPR / CCPA) as well as a
potential credential-adjacent information leak if logs are accessible.

**Risk:**
Informational / GDPR/CCPA compliance concern.

**Recommendation:**
Override `toString()` (or use Lombok `@ToString(exclude = {"email","comp_email"})`) to exclude PII
fields from log output.

---

## Finding Count

| Severity | Count |
|----------|-------|
| CRITICAL | 0     |
| HIGH     | 3     |
| MEDIUM   | 3     |
| LOW      | 3     |
| INFO     | 3     |

**Total findings: 12**

### High-priority remediation order
1. **[HIGH]** Remove / protect plaintext `password` field in `EntityBean` — risk of credential
   exposure via serialization, reflection, and framework auto-mapping.
2. **[HIGH]** Add `session.invalidate()` to `ExpireAction` — active sessions remain valid after
   the user is redirected to the expiry page.
3. **[HIGH]** Add `filter="true"` to all `<bean:write>` tags in `expiringTrainings.jsp` — stored
   XSS via driver name, email, and unit name fields.
