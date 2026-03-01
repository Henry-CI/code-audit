#!/bin/bash
# Run all 94 security audit agents using claude CLI
# Each agent reads its prompt from a file

REPO="C:/Projects/cig-audit/repos/fleetiq"
OUT="C:/Projects/cig-audit/repos/fleetiq/audit/2026-03-01-01/pass1"
PROMPTS="${OUT}/prompts"
mkdir -p "$PROMPTS"

run_agent() {
  local ID="$1"
  local PROMPT_FILE="${PROMPTS}/${ID}.txt"
  local LOG_FILE="${OUT}/${ID}.log"
  echo "[$(date '+%H:%M:%S')] Starting ${ID}..."
  claude --model claude-sonnet-4-5 -p "$(cat "$PROMPT_FILE")" > "$LOG_FILE" 2>&1
  local EXIT=$?
  echo "[$(date '+%H:%M:%S')] ${ID} finished (exit=${EXIT})"
}

export -f run_agent
export OUT PROMPTS

# Run all in parallel using xargs or background jobs
PIDS=()
for ID in J01 J02 J03 J04 J05 J06 J07 J08 J09 J10 \
           J11 J12 J13 J14 J15 J16 J17 J18 J19 J20 \
           J21 J22 J23 J24 J25 J26 J27 J28 J29 J30 \
           J31 J32 J33 J34 J35 J36 J37 J38 J39 J40 \
           J41 J42 J43 J44 J45 J46 J47 J48 J49 J50 \
           J51 J52 J53 J54 J55 J56 J57 J58 J59 J60 \
           J61 J62 J63 J64 J65 J66 J67 J68 J69 J70 \
           J71 J72 J73 J74 J75 J76 J77 J78 J79 J80 \
           J81 J82 J83 J84 J85 J86 J87 J88 J89 \
           C01 C02 S01 S02 S03; do
  if [ -f "${PROMPTS}/${ID}.txt" ]; then
    run_agent "$ID" &
    PIDS+=($!)
    # Throttle: max 15 parallel
    while [ $(jobs -r | wc -l) -ge 15 ]; do
      sleep 2
    done
  else
    echo "WARNING: No prompt file for ${ID}"
  fi
done

echo "Waiting for all agents to complete..."
wait
echo "All done."
