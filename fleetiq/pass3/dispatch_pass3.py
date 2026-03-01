#!/usr/bin/env python3
"""Dispatch Pass 3 (Documentation) audit agents."""

import subprocess
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

REPO = "C:/Projects/cig-audit/repos/fleetiq"
OUT = f"{REPO}/audit/2026-03-01-01/pass3"
INSTRUCTIONS = f"{REPO}/audit/2026-03-01-01/pass3/AGENT-INSTRUCTIONS.md"
MAX_WORKERS = 15

# Parse partition files
def parse_agents(filepath):
    agents = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Format: "J01: A002 path/file.java A003 path/file2.java"
            match = re.match(r'^(\w+):\s+(.*)', line)
            if match:
                agent_id = match.group(1)
                rest = match.group(2)
                # Extract file paths (skip Axxx IDs)
                files = re.findall(r'(?:A\d+\s+)(\S+)', rest)
                agents[agent_id] = files
    return agents

def build_prompt(agent_id, files):
    file_list = "\n".join(files)
    return f"""Audit agent {agent_id} — Pass 3 Documentation. Repository: C:/Projects/cig-audit/repos/fleetiq. Branch: multi-customer-sync-to-master.
1. Verify branch: run git -C "C:/Projects/cig-audit/repos/fleetiq" branch --show-current — must be multi-customer-sync-to-master. STOP if wrong.
2. Read: {INSTRUCTIONS}
3. Read EACH source file IN FULL (paths relative to C:/Projects/cig-audit/repos/fleetiq/):
{file_list}
4. Produce reading evidence for every source file FIRST (class name, all public methods with line numbers, all fields).
5. For each public method/function, check:
   - Does a doc comment (Javadoc /** ... */ for Java) exist immediately before the method?
   - If yes, is it accurate? Does it describe what the method actually does?
   - Are all parameters documented with @param?
   - Is the return value documented with @return?
   - Are thrown exceptions documented with @throws?
6. Report every documentation gap as a finding:
   - Every public method with NO doc comment
   - Every doc comment that is inaccurate or misleading vs. actual implementation
   - Every doc comment missing @param, @return, or @throws tags
   - Missing or inaccurate class-level documentation
7. Each finding must use exactly this format:
   **Severity:** CRITICAL | HIGH | MEDIUM | LOW | INFO
   **Description:** plain English explanation of the problem
   **Fix:** specific recommended remediation
   **File:** file path
   **Line(s):** line numbers
   **Method:** method name (if applicable)
8. Write output to: C:/Projects/cig-audit/repos/fleetiq/audit/2026-03-01-01/pass3/{agent_id}.md
Report only — do NOT fix anything."""

def dispatch_agent(agent_id, files):
    prompt = build_prompt(agent_id, files)
    log_path = f"{OUT}/{agent_id}.log"
    start = time.time()
    print(f"[START] {agent_id} ({len(files)} files)")

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    try:
        result = subprocess.run(
            ["claude.cmd", "--model", "claude-sonnet-4-5", "-p", "--dangerously-skip-permissions"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=600,
            env=env,
            cwd=REPO
        )
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(result.stdout)
            if result.stderr:
                f.write("\n\n--- STDERR ---\n")
                f.write(result.stderr)
        elapsed = time.time() - start
        # Check if output file was created
        md_path = f"{OUT}/{agent_id}.md"
        status = "OK" if os.path.exists(md_path) else "NO_OUTPUT"
        print(f"[DONE] {agent_id} — {status} — {elapsed:.0f}s")
        return agent_id, status
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        print(f"[TIMEOUT] {agent_id} — {elapsed:.0f}s")
        with open(log_path, 'w') as f:
            f.write("TIMEOUT after 600s")
        return agent_id, "TIMEOUT"
    except Exception as e:
        elapsed = time.time() - start
        print(f"[ERROR] {agent_id} — {e} — {elapsed:.0f}s")
        with open(log_path, 'w') as f:
            f.write(f"ERROR: {e}")
        return agent_id, "ERROR"

def main():
    all_agents = {}

    # Load Java agents
    java_path = f"{REPO}/audit/java_agents.txt"
    all_agents.update(parse_agents(java_path))

    # Load JSP agents
    jsp_path = f"{REPO}/audit/jsp_agents.txt"
    all_agents.update(parse_agents(jsp_path))

    # Add Config agents manually
    all_agents["C01"] = ["Jenkinsfile", "WEB-INF/src/log4j.properties", "WEB-INF/src/log4j2.properties"]
    all_agents["C02"] = [
        "WEB-INF/src/main/resource/Messages.properties",
        "WEB-INF/src/main/resource/Messages_en.properties",
        "WEB-INF/src/main/resource/Messages_en_US.properties"
    ]

    # Add SQL agents manually
    all_agents["S01"] = [
        "sql/FLEETIQ_AUG_2022.sql", "sql/FLEETIQ_JAN_2022.sql",
        "sql/FLEETIQ_JAN_2023.sql", "sql/FLEETIQ_JUN_2022.sql",
        "sql/FLEETIQ_MAR_2022.sql", "sql/FLEETIQ_MAY_2022.sql",
        "sql/FLEETIQ_NOV_2022.sql", "sql/FLEETIQ_SEPT_2022.sql"
    ]
    all_agents["S02"] = [
        "sql/check_firmware_idauth_driver_name.sql",
        "sql/disable_unit_preop_perday_perdriver.sql",
        "sql/equipment_bypass.sql"
    ]
    all_agents["S03"] = [
        "sql/sp_equipment_bypass_alert.sql",
        "sql/sp_get_driver_name.sql",
        "sql/sp_opchks_response.sql"
    ]

    total = len(all_agents)
    print(f"Dispatching {total} agents with {MAX_WORKERS} concurrent workers...")
    print(f"Output dir: {OUT}")
    print()

    results = {"OK": 0, "NO_OUTPUT": 0, "TIMEOUT": 0, "ERROR": 0}

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(dispatch_agent, aid, files): aid
            for aid, files in sorted(all_agents.items())
        }
        for future in as_completed(futures):
            aid, status = future.result()
            results[status] = results.get(status, 0) + 1

    print()
    print(f"=== COMPLETE ===")
    print(f"Total: {total}")
    for status, count in sorted(results.items()):
        print(f"  {status}: {count}")

if __name__ == "__main__":
    main()
