# Pass 4 Code Quality Agent Instructions

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

### 4. Code Quality Analysis
For each source file, check for:

**Style Inconsistencies:**
- Naming convention violations (camelCase vs snake_case, inconsistent prefixes)
- Inconsistent formatting (brace placement, indentation, spacing)
- Mixed patterns for the same operation (e.g., using both StringBuffer and StringBuilder)
- Inconsistent error handling patterns

**Leaky Abstractions:**
- Internal implementation details exposed through public interfaces
- Tight coupling between components that should be independent
- Implementation concerns bleeding across module boundaries
- Direct field access instead of encapsulation

**Commented-Out Code:**
- Any block of commented-out code (not explanatory comments)
- Each instance should be flagged — commented code should be deleted or reinstated

**Dead Code:**
- Unused imports
- Unreachable code paths
- Unused variables, methods, or classes
- Methods that are defined but never called

**Build/Dependency Issues:**
- Deprecated API usage that would generate compiler warnings
- Unchecked/raw type usage
- Dependency version conflicts
- Hardcoded version strings that conflict with other files

### 5. Write Output
Write findings to the TEMP file path specified in the prompt.

Format:
```
# Agent [AGENT-ID] — Pass 4 Code Quality Audit
**Files reviewed:** [list]
**Branch verified:** multi-customer-sync-to-master

---
## Reading Evidence
[reading evidence for each file]

---
## Findings

### [AGENT-ID]-F01: [short title]
**Severity:** CRITICAL | HIGH | MEDIUM | LOW | INFO
**Description:** plain English explanation of the problem
**Fix:** specific recommended remediation
**File:** file path
**Line(s):** line numbers

[repeat for each finding]
```

### 6. Rules
- Report only — do NOT fix anything
- Every finding MUST use the exact format above with **Description:** and **Fix:** fields
- A finding must identify an actual problem — do not report "X follows conventions" as a finding
- Commented-out code: MEDIUM (clutters codebase, risk of accidental reactivation)
- Dead/unused code: LOW/MEDIUM
- Style inconsistencies: LOW
- Leaky abstractions: MEDIUM/HIGH
- Deprecated API usage: MEDIUM (build warnings are real problems)
