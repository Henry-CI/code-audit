import subprocess
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

PROMPTS_DIR = 'C:/Projects/cig-audit/repos/fleetiq/audit/2026-03-01-01/pass1/prompts'
OUT_DIR = 'C:/Projects/cig-audit/repos/fleetiq/audit/2026-03-01-01/pass1'
MAX_WORKERS = 10

agent_ids = [
    'J01','J02','J03','J04','J05','J06','J07','J08','J09','J10',
    'J11','J12','J13','J14','J15','J16','J17','J18','J19','J20',
    'J21','J22','J23','J24','J25','J26','J27','J28','J29','J30',
    'J31','J32','J33','J34','J35','J36','J37','J38','J39','J40',
    'J41','J42','J43','J44','J45','J46','J47','J48','J49','J50',
    'J51','J52','J53','J54','J55','J56','J57','J58','J59','J60',
    'J61','J62','J63','J64','J65','J66','J67','J68','J69','J70',
    'J71','J72','J73','J74','J75','J76','J77','J78','J79','J80',
    'J81','J82','J83','J84','J85','J86','J87','J88','J89',
    'C01','C02','S01','S02','S03'
]

def run_agent(agent_id):
    prompt_file = os.path.join(PROMPTS_DIR, agent_id + '.txt')
    log_file = os.path.join(OUT_DIR, agent_id + '.log')

    with open(prompt_file, 'r') as f:
        prompt = f.read()

    start = time.time()
    try:
        result = subprocess.run(
            ['claude', '-p', prompt],
            capture_output=True,
            text=True,
            timeout=600
        )
        elapsed = time.time() - start

        with open(log_file, 'w') as f:
            f.write(f'=== {agent_id} (exit={result.returncode}, {elapsed:.1f}s) ===\n')
            f.write(result.stdout)
            if result.stderr:
                f.write('\n=== STDERR ===\n')
                f.write(result.stderr)

        return agent_id, result.returncode, elapsed
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        with open(log_file, 'w') as f:
            f.write(f'=== {agent_id} TIMEOUT after {elapsed:.1f}s ===\n')
        return agent_id, -1, elapsed
    except Exception as e:
        elapsed = time.time() - start
        with open(log_file, 'w') as f:
            f.write(f'=== {agent_id} ERROR: {e} ===\n')
        return agent_id, -2, elapsed

print(f'Starting {len(agent_ids)} agents with {MAX_WORKERS} parallel workers...')
start_total = time.time()

completed = 0
failed = []

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {executor.submit(run_agent, aid): aid for aid in agent_ids}
    for future in as_completed(futures):
        aid, code, elapsed = future.result()
        completed += 1
        status = 'OK' if code == 0 else f'FAIL({code})'
        print(f'[{completed}/{len(agent_ids)}] {aid}: {status} in {elapsed:.1f}s')
        if code != 0:
            failed.append(aid)

total_elapsed = time.time() - start_total
print(f'\nCompleted {completed} agents in {total_elapsed:.1f}s')
if failed:
    print(f'Failed: {failed}')
else:
    print('All agents completed successfully.')
