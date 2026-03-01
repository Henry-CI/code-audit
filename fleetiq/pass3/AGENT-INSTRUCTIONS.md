# Pass 3 Documentation Agent Instructions

## Repository
- Path: C:/Projects/cig-audit/repos/fleetiq
- Branch: multi-customer-sync-to-master

## Steps

### 1. Verify Branch
Run: `git -C "C:/Projects/cig-audit/repos/fleetiq" branch --show-current`
If NOT `multi-customer-sync-to-master`, STOP immediately and report error.

### 2. Read Assigned Source Files
Read each assigned source file IN FULL using the Read tool. No skimming.

### 3. Produce Reading Evidence FIRST
Before any findings, output reading evidence for each source file:

**Java files:**
- Fully qualified class name
- Every public method: return type, parameter types, line number
- Every field: access modifier, type, name

**JSP files:**
- File path
- Every scriptlet block: line numbers + brief description
- Every function/method invoked
- Every form action and parameter

**XML/properties/config files:**
- Every setting, servlet, filter, listener defined

**SQL files:**
- Every CREATE, ALTER, DROP statement
- Every stored procedure/function

### 4. Documentation Analysis
For each source file:
- Enumerate every public function/method
- Check if a doc comment (Javadoc `/** ... */` for Java, or equivalent comment block for other file types) exists for each
- If a doc comment exists, verify it is accurate against the implementation:
  - Does it describe what the method actually does?
  - Are all parameters documented with `@param`?
  - Is the return value documented with `@return`?
  - Are thrown exceptions documented with `@throws`?
  - Does the description match the actual behavior?
- If no doc comment exists, report it as a finding

### 5. Report Documentation Gaps
For each source file, report:
- Every public method/function with NO doc comment
- Every doc comment that is inaccurate or misleading
- Every doc comment missing `@param`, `@return`, or `@throws` tags
- Class-level documentation missing or inaccurate

### 6. Write Output
Write findings to: `C:/Projects/cig-audit/repos/fleetiq/audit/2026-03-01-01/pass3/[AGENT-ID].md`

Format:
```
# Agent [AGENT-ID] — Pass 3 Documentation Audit
**Files reviewed:** [list]
**Branch verified:** multi-customer-sync-to-master

---
## Reading Evidence
[reading evidence for each file]

---
## Documentation Analysis

### [source file name]
**Public methods total:** N
**Documented methods:** N
**Undocumented methods:** N

---
## Findings

### [AGENT-ID]-F01: [short title]
**Severity:** CRITICAL | HIGH | MEDIUM | LOW | INFO
**Description:** plain English explanation of the problem
**Fix:** specific recommended remediation
**File:** file path
**Line(s):** line numbers
**Method:** [method name if applicable]

[repeat for each finding]
```

### 7. Rules
- Report only — do NOT fix anything
- Every finding MUST use the exact format above with **Description:** and **Fix:** fields
- A finding must identify an actual gap — do not report "X is documented" as a finding
- Prioritize: undocumented security-critical methods (auth, input validation, data access) as HIGH
- Inaccurate/misleading doc comments as MEDIUM/HIGH (could cause misuse)
- Missing parameter/return docs as MEDIUM
- Undocumented utility/helper methods as LOW
- Missing class-level docs as LOW/INFO
