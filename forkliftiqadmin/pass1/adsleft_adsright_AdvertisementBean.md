# Security Audit Report
## Files: adsleft.inc.jsp, adsright.inc.jsp, AdvertisementBean.java
**Repository:** forkliftiqadmin
**Branch:** master
**Audit Run:** audit/2026-02-26-01/
**Pass:** pass1
**Date:** 2026-02-26
**Auditor:** Automated Security Audit (Claude)
**Stack:** Apache Struts 1.3.10 (NOT Spring)

---

## 1. Files Audited

| # | File |
|---|------|
| 1 | `src/main/webapp/includes/adsleft.inc.jsp` |
| 2 | `src/main/webapp/includes/adsright.inc.jsp` |
| 3 | `src/main/java/com/bean/AdvertisementBean.java` |

---

## 2. Reading Evidence

### 2.1 adsleft.inc.jsp — Output Tags and Request Parameters

| Line | Tag / Expression | Property / Value | Notes |
|------|-----------------|------------------|-------|
| 4 | `<%@ page import="..." %>` | `com.util.RuntimeConf` | Static import of config class |
| 8 | `<logic:notEmpty name="sessAds">` | Session attribute `sessAds` | Guards iteration |
| 9 | `<logic:iterate name="sessAds" id="adsRecord" type="com.bean.AdvertisementBean" length="3">` | Session attribute `sessAds`, items 0–2 | Iterates session-scoped list |
| 11 | `<img src="<%=RuntimeConf.IMG_SRC%><bean:write property="pic" name="adsRecord"/>` | `adsRecord.pic` | **Unfiltered JSP expression + bean:write in HTML attribute context** |
| 14 | `<bean:write property="text" name="adsRecord" />` | `adsRecord.text` | **Unfiltered bean:write in HTML body context** |

No `<html:form>` tags, no `request.getParameter()` calls, no `<html:text>` or similar input tags present in this file.

### 2.2 adsright.inc.jsp — Output Tags and Request Parameters

| Line | Tag / Expression | Property / Value | Notes |
|------|-----------------|------------------|-------|
| 4 | `<%@ page import="..." %>` | `com.util.RuntimeConf` | Static import of config class |
| 7 | `<logic:notEmpty name="sessAds">` | Session attribute `sessAds` | Guards iteration |
| 8 | `<logic:iterate name="sessAds" id="adsRecord" type="com.bean.AdvertisementBean" length="3" offset="3">` | Session attribute `sessAds`, items 3–5 | Iterates session-scoped list |
| 10 | `<img src="<%=RuntimeConf.IMG_SRC%><bean:write property="pic" name="adsRecord"/>` | `adsRecord.pic` | **Unfiltered JSP expression + bean:write in HTML attribute context** |
| 13 | `<bean:write property="text" name="adsRecord" />` | `adsRecord.text` | **Unfiltered bean:write in HTML body context** |

No `<html:form>` tags, no `<html:text>` or similar input tags present in this file.

### 2.3 AdvertisementBean.java — Fields

| Field | Type | Getter | Setter | Notes |
|-------|------|--------|--------|-------|
| `id` | `String` | `getId()` | `setId(String)` | Primary key / database ID |
| `pic` | `String` | `getPic()` | `setPic(String)` | Image path/filename — rendered in `src` attribute |
| `text` | `String` | `getText()` | `setText(String)` | Ad display text — rendered in HTML body |
| `order_no` | `String` | `getOrder_no()` | `setOrder_no(String)` | Display ordering field; not rendered in these JSPs |

The class implements `java.io.Serializable` with a hardcoded `serialVersionUID = -2354229211604525787L`.

---

## 3. Findings

### FINDING-01
**Severity:** HIGH
**Category:** Cross-Site Scripting (XSS) — Stored, HTML Body Context
**Files:**
- `src/main/webapp/includes/adsleft.inc.jsp`, Line 14
- `src/main/webapp/includes/adsright.inc.jsp`, Line 13

**Description:**
The `<bean:write>` tag outputs the `text` property of `AdvertisementBean` directly into the HTML body without any HTML escaping. In Struts 1.x, `<bean:write>` does NOT escape HTML output by default unless the `filter="true"` attribute is explicitly set. If `filter` is omitted or set to `false`, any HTML or JavaScript stored in the `text` field is rendered verbatim in the browser.

Because the data originates from a session attribute (`sessAds`) that was presumably loaded from a database, any advertisement record whose `text` field contains malicious markup will execute in every authenticated user's browser that views these panels. This is a stored XSS vector: an attacker with write access to the advertisements table (e.g., a compromised admin account, a SQL injection vulnerability elsewhere, or insider threat) can persist a `<script>` payload that targets all users.

**Evidence:**
```jsp
<!-- adsleft.inc.jsp, line 14 -->
<bean:write property="text" name="adsRecord" />

<!-- adsright.inc.jsp, line 13 -->
<bean:write property="text" name="adsRecord" />
```
The `filter` attribute is absent. Struts 1.3.10 documentation states: `filter` — "If this attribute is true, sensitive characters in the value will be converted to the corresponding character entities (e.g., &lt; becomes &amp;lt;). Default value is false." Therefore output is unescaped.

**Recommendation:**
Add `filter="true"` to every `<bean:write>` tag that outputs data to an HTML context:
```jsp
<bean:write property="text" name="adsRecord" filter="true" />
```
If the `text` field is intended to store rich/HTML content (e.g., formatted ad copy), implement a server-side HTML sanitization library (e.g., OWASP Java HTML Sanitizer) before the value is stored, and use a strict allowlist of permitted tags/attributes. Do not rely solely on client-side or display-time escaping in that case.

---

### FINDING-02
**Severity:** HIGH
**Category:** Cross-Site Scripting (XSS) — Stored, HTML Attribute Context (src)
**Files:**
- `src/main/webapp/includes/adsleft.inc.jsp`, Line 11
- `src/main/webapp/includes/adsright.inc.jsp`, Line 10

**Description:**
The `pic` property of `AdvertisementBean` is injected into the `src` attribute of an `<img>` tag using a hybrid of a raw JSP scriptlet expression (`<%=RuntimeConf.IMG_SRC%>`) and an unescaped `<bean:write>`. The resulting HTML is:

```html
<img src="[static prefix][adsRecord.pic]" alt=""/>
```

Because `<bean:write>` lacks `filter="true"`, a `pic` value containing `" onerror="alert(1)` would break out of the attribute and inject an event handler. A `pic` value of `javascript:...` is also potentially exploitable in legacy or misconfigured browsers. This constitutes a stored XSS via attribute injection.

Additionally, there is no URL validation on the `pic` field — an absolute URL (e.g., `https://attacker.com/evil.jpg`) in `pic` would cause the browser to load an off-site resource, which could be leveraged for content-spoofing, mixed-content issues, or user tracking.

**Evidence:**
```jsp
<!-- adsleft.inc.jsp, line 11 -->
<img src="<%=RuntimeConf.IMG_SRC%><bean:write property="pic" name="adsRecord"/>" alt=""/>

<!-- adsright.inc.jsp, line 10 -->
<img src="<%=RuntimeConf.IMG_SRC%><bean:write property="pic" name="adsRecord"/>" alt=""/>
```

**Recommendation:**
Apply `filter="true"` on the `<bean:write>` for `pic` as a minimum:
```jsp
<img src="<%=RuntimeConf.IMG_SRC%><bean:write property="pic" name="adsRecord" filter="true"/>" alt=""/>
```
Additionally, enforce server-side validation on the `pic` field at time of storage: it should match a relative path pattern only (e.g., alphanumerics, slashes, dots, hyphens — no quotes, angle brackets, or protocol prefixes). Reject or sanitize values that do not conform.

---

### FINDING-03
**Severity:** MEDIUM
**Category:** Information Disclosure — Internal Path Prefix via RuntimeConf
**Files:**
- `src/main/webapp/includes/adsleft.inc.jsp`, Line 11
- `src/main/webapp/includes/adsright.inc.jsp`, Line 10

**Description:**
`RuntimeConf.IMG_SRC` is a static constant rendered directly into the `src` attribute of every `<img>` tag via a JSP scriptlet expression. Depending on the value of `IMG_SRC`, this could expose internal infrastructure details in the rendered HTML: for example, an internal server hostname, a non-public CDN path, an S3 bucket name, or a directory structure that aids attackers in mapping the server layout.

Even if the value is a public-facing URL today, it is a hardcoded constant in a configuration class, meaning any future change to infrastructure is visible in all rendered pages immediately and without further access control review.

**Evidence:**
```jsp
<img src="<%=RuntimeConf.IMG_SRC%><bean:write property="pic" name="adsRecord"/>" alt=""/>
```
The value of `RuntimeConf.IMG_SRC` is not visible in these files; the risk level depends on its actual value. This finding is raised because the pattern warrants review.

**Recommendation:**
Review the value of `RuntimeConf.IMG_SRC` to confirm it does not expose internal hostnames, bucket names, or directory structures in rendered HTML. If the prefix is sensitive, move it server-side and serve images through an application-controlled proxy endpoint rather than constructing public `src` URLs with internal prefixes.

---

### FINDING-04
**Severity:** MEDIUM
**Category:** Insecure Deserialization Risk (Serializable Bean with Hardcoded serialVersionUID)
**File:** `src/main/java/com/bean/AdvertisementBean.java`, Lines 5, 10

**Description:**
`AdvertisementBean` implements `java.io.Serializable`. In Struts 1.x applications, action forms and beans stored in the HTTP session are serialized when session persistence is enabled (e.g., distributed sessions, session replication in a cluster, persistent session managers in Tomcat). The hardcoded `serialVersionUID = -2354229211604525787L` ensures Java deserialization will accept any bytes with that UID without version mismatch errors.

If an attacker can influence the contents of the `sessAds` session attribute — either by manipulating session storage directly or by exploiting a separate deserialization endpoint — they could inject a malicious object graph. While `AdvertisementBean` itself contains only String fields and is not a gadget, the broader pattern of storing arbitrary serializable objects in session scope warrants review of the full session handling chain.

This is also relevant if the application uses Java serialization in any remoting layer, caching layer (e.g., Memcached with Java serialization), or file-based session persistence.

**Evidence:**
```java
public class AdvertisementBean implements Serializable {
    private static final long serialVersionUID = -2354229211604525787L;
    private String id = null;
    private String pic = null;
    private String text = null;
    private String order_no = null;
```

**Recommendation:**
Verify whether session persistence or replication is enabled. If so, ensure that only trusted, validated data is placed into session scope. Ensure the deserialization path for session objects is protected. Consider implementing `readObject()` with strict validation if the class must remain serializable. If the class does not need to be serialized, remove the `Serializable` interface.

---

### FINDING-05
**Severity:** LOW
**Category:** Missing Input Validation — No Field-Level Constraints on Bean
**File:** `src/main/java/com/bean/AdvertisementBean.java`, Lines 12–15

**Description:**
All four fields (`id`, `pic`, `text`, `order_no`) are plain `String` fields with no length constraints, format validation, or null-safety annotations. The setters accept any value without validation. While validation may occur elsewhere (e.g., in a Struts `ActionForm` or a DAO layer), the absence of any defensive validation in the bean itself means that if a caller bypasses the normal population path, unconstrained values (including extremely long strings, SQL metacharacters, or markup) will be stored and subsequently rendered.

**Evidence:**
```java
public void setPic(String pic) {
    this.pic = pic;
}
public void setText(String text) {
    this.text = text;
}
```

**Recommendation:**
Add length and format validation at the point of data entry (Struts `ActionForm.validate()`) and enforce similar constraints in the DAO/persistence layer. Consider documenting expected formats (e.g., `pic` is a relative path, `text` is plain text up to N characters) in the bean or a companion validator.

---

### FINDING-06
**Severity:** LOW
**Category:** Unconventional Field Naming (order_no) — Minor Code Quality / Maintainability Risk
**File:** `src/main/java/com/bean/AdvertisementBean.java`, Lines 15, 35–39

**Description:**
The field `order_no` uses an underscore in its name, which is non-standard Java naming convention (Java convention is camelCase: `orderNo`). The getter `getOrder_no()` is also non-standard. In Struts 1.x, bean property names must match JavaBeans conventions for introspection to work correctly (`getOrderNo()` for field `orderNo`). If `order_no` is referenced via Struts tag expressions elsewhere, the inconsistency could produce silent failures (null output) rather than clear errors, making security-relevant behavior harder to reason about during audits.

This is a low-severity code quality issue that increases audit complexity and could mask a binding bug.

**Evidence:**
```java
private String order_no = null;

public String getOrder_no() {
    return order_no;
}
public void setOrder_no(String order_no) {
    this.order_no = order_no;
}
```

**Recommendation:**
Rename field to `orderNo` and getters/setters to `getOrderNo()` / `setOrderNo()`. Ensure any database mapping or Struts form property references are updated consistently.

---

## 4. Category Summary

| Category | Status | Finding IDs |
|----------|--------|-------------|
| XSS — Unescaped Output (HTML Body) | ISSUES FOUND | FINDING-01 |
| XSS — Unescaped Output (HTML Attribute) | ISSUES FOUND | FINDING-02 |
| CSRF — Forms Present | NO ISSUES — no `<html:form>` or `<form>` tags exist in these three files | — |
| Information Disclosure | ISSUES FOUND | FINDING-03 |
| Sensitive Data in Bean Fields | NO ISSUES — fields are advertisement display data only (image path, text, ordering); no PII, credentials, or tokens | — |
| Insecure Deserialization | ISSUES FOUND | FINDING-04 |
| Input Validation | ISSUES FOUND | FINDING-05 |
| Code Quality / Naming | ISSUES FOUND | FINDING-06 |

**CSRF Note:** These include files contain no forms whatsoever. The CSRF structural gap documented in the stack-level assessment applies to other files in the application (action-dispatching forms), not to these display-only fragments.

**Sensitive Data Note:** `AdvertisementBean` fields (`id`, `pic`, `text`, `order_no`) represent advertisement metadata only. No passwords, tokens, PII, financial data, or credentials are present.

---

## 5. Finding Count by Severity

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 0 | — |
| HIGH | 2 | FINDING-01, FINDING-02 |
| MEDIUM | 2 | FINDING-03, FINDING-04 |
| LOW | 2 | FINDING-05, FINDING-06 |
| INFO | 0 | — |
| **TOTAL** | **6** | |

---

## 6. Prioritised Remediation Order

1. **FINDING-01** (HIGH) — Add `filter="true"` to `<bean:write property="text">` in both JSPs.
2. **FINDING-02** (HIGH) — Add `filter="true"` to `<bean:write property="pic">` in both JSPs; add server-side path validation.
3. **FINDING-03** (MEDIUM) — Review and if necessary redact `RuntimeConf.IMG_SRC` from rendered HTML.
4. **FINDING-04** (MEDIUM) — Review session persistence configuration and serialization exposure.
5. **FINDING-05** (LOW) — Add field-level validation in `ActionForm.validate()` and the DAO layer.
6. **FINDING-06** (LOW) — Rename `order_no` to `orderNo` per Java naming conventions.

---

*End of report.*
