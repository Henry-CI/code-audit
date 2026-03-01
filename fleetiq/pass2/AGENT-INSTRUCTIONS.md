# Pass 2 Test Coverage Agent Instructions

## Repository
- Path: C:/Projects/cig-audit/repos/fleetiq
- Branch: multi-customer-sync-to-master

## Steps

### 1. Verify Branch
Run: `git -C "C:/Projects/cig-audit/repos/fleetiq" branch --show-current`
If NOT `multi-customer-sync-to-master`, STOP immediately and report error.

### 2. Read Assigned Source Files
Read each assigned source file IN FULL using the Read tool. No skimming.

### 3. Search for Test Files
For each source file:
- Look for a corresponding test file (e.g., `FooTest.java` for `Foo.java`)
- Grep the entire repo for test references: class names, method names
- Check for indirect coverage in any test-like file

### 4. Produce Reading Evidence FIRST
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

### 5. Report Coverage Gaps
For each source file, report:
- Whether a corresponding test file exists
- Functions/methods with no test exercising them
- Error/failure paths with no test triggering them
- Missing edge case coverage: null inputs, empty inputs, boundary values, off-by-one

### 6. Write Output
Write findings to: `C:/Projects/cig-audit/repos/fleetiq/audit/2026-03-01-01/pass2/[AGENT-ID].md`

Format:
```
# Agent [AGENT-ID] — Pass 2 Test Coverage Audit
**Files reviewed:** [list]
**Branch verified:** multi-customer-sync-to-master

---
## Reading Evidence
[reading evidence for each file]

---
## Test Coverage Analysis

### [source file name]
**Test file found:** Yes/No
**Indirect test coverage:** [describe or "None found"]

---
## Findings

### [AGENT-ID]-F01: [short title]
**Severity:** CRITICAL | HIGH | MEDIUM | LOW | INFO
**Description:** plain English explanation of the problem
**Fix:** specific recommended remediation
**File:** file path
**Line(s):** line numbers
**Untested function:** [function name if applicable]

[repeat for each finding]
```

### 7. Rules
- Report only — do NOT fix anything
- Every finding MUST use the exact format above with **Description:** and **Fix:** fields
- A finding must identify an actual gap — do not report "X is tested" as a finding
- Prioritize: untested security-critical functions (auth, input validation, data access) as CRITICAL/HIGH
- Untested utility/helper methods as MEDIUM/LOW
- Missing edge cases as LOW/INFO
