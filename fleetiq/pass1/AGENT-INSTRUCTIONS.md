# Pass 1 Security Agent Instructions

## Repository
- Path: C:/Projects/cig-audit/repos/fleetiq
- Branch: multi-customer-sync-to-master

## Steps

### 1. Verify Branch
Run: `git -C "C:/Projects/cig-audit/repos/fleetiq" branch --show-current`
If NOT `multi-customer-sync-to-master`, STOP immediately and report error.

### 2. Read Assigned Files
Read each file IN FULL using the Read tool. No skimming. No summaries of unread content.

### 3. Produce Reading Evidence FIRST
Before any findings, output reading evidence for each file:

**Java files:**
- Fully qualified class name
- Every public method: return type, parameter types, line number
- Every annotation on the class and each method
- Every field: access modifier, type, name
- Every `import` statement (flag wildcard imports)

**JSP files:**
- File path
- Every `<%@ page import="..." %>` directive
- Every `<jsp:useBean>` declaration
- Every scriptlet block: line numbers + brief description
- Every `<%= ... %>` expression — note if value could be user-controlled
- Every `<%@ include file="..." %>` or `<jsp:include>` directive

**XML/properties/config files:**
- Every servlet, filter, listener defined
- Every security-constraint, login-config
- Every environment entry or resource reference
- Every context parameter

**SQL files:**
- Every CREATE, ALTER, DROP statement
- Every stored procedure/function
- Every GRANT/REVOKE
- Flag any hardcoded credentials or IP addresses

### 4. Review Against Checklist
Read the checklist: C:/Projects/cig-audit/audit-skills/PASS1-CHECKLIST-ff-new.md
Check each relevant section. The key sections are:
1. Secrets and Credentials
2. Authentication and Authorization
3. Injection Vulnerabilities (SQL injection, XSS, file inclusion, command injection, SSRF)
4. Session and CSRF
5. Data Exposure and Privacy
6. Transport Security
7. Dependency Vulnerabilities

### 5. Write Output
Write findings to: `C:/Projects/cig-audit/repos/fleetiq/audit/2026-03-01-01/pass1/[AGENT-ID].md`

Format:
```
# Agent [AGENT-ID] — Pass 1 Security Audit
**Files reviewed:** [list]
**Branch verified:** multi-customer-sync-to-master

---
## Reading Evidence
[reading evidence for each file]

---
## Findings

### [AGENT-ID]-F01: [short title]
**Description:** plain English explanation
**Severity:** CRITICAL | HIGH | MEDIUM | LOW | INFO
**Checklist item:** section number and name from checklist
**Evidence:** exact code snippet with line numbers
**File:** file path
**Line(s):** line numbers

[repeat for each finding]

---
## Checklist Items With No Issues
[List checklist items reviewed that had no findings, explicitly]
```

### 6. Rules
- Report only — do NOT fix anything
- State explicitly when a checklist item has no issues
- Every finding MUST use the exact format above
- Include exact code snippets with line numbers as evidence
- Flag SQL string concatenation, unescaped JSP expressions, hardcoded credentials, missing auth checks, IDOR vulnerabilities
- Pay special attention to multi-tenant data isolation (customer_id scoping)
