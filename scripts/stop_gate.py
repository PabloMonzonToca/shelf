#!/usr/bin/env python3
"""Stop hook: the agent can't finish its turn while the test suite fails.

It is also a ratchet: the turn is blocked when fewer tests run than the
minimum in scripts/min_tests.txt, or when any test is skipped. Raise that
minimum by hand when the suite grows; never lower it.

Works as a Claude Code or Codex Stop hook. Standard library only.
"""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

MAX_BLOCKS = 3   # consecutive blocks before we let the agent stop and warn you
TAIL_LINES = 40  # lines of test output sent back to the agent

event = json.load(sys.stdin)

# Test the project the agent is working in. `cwd` follows it into worktrees.
here = Path(event.get("cwd") or ".").resolve()
root = next((p for p in (here, *here.parents) if (p / "pyproject.toml").exists()), None)
if root is None:
    sys.exit(0)  # not inside the project: nothing to check

result = subprocess.run(
    [sys.executable, "-m", "unittest"], cwd=root, capture_output=True, text=True
)
output = result.stdout + result.stderr
counter = Path(tempfile.gettempdir()) / f"stop-gate-{event.get('session_id', 'unknown')}"

# unittest prints "Ran N tests" and counts skipped tests as run, so check both.
ran = re.findall(r"^Ran (\d+) tests?", output, re.MULTILINE)
skipped = re.findall(r"skipped=(\d+)", output)
min_file = root / "scripts" / "min_tests.txt"
minimum = int(min_file.read_text().strip()) if min_file.exists() else 0

problems = []
if result.returncode != 0:
    problems.append("The test suite fails.")
if not ran:
    problems.append("Couldn't find the `Ran N tests` line, so the test count is unknown.")
elif int(ran[-1]) < minimum:
    problems.append(
        f"Only {ran[-1]} tests ran, but scripts/min_tests.txt requires at least {minimum}."
    )
if skipped and int(skipped[-1]) > 0:
    problems.append(f"{skipped[-1]} test(s) were skipped.")

if not problems:
    counter.unlink(missing_ok=True)
    sys.exit(0)  # silent success

# stop_hook_active is true when the agent is already continuing because a Stop hook blocked it.
blocks = int(counter.read_text()) if event.get("stop_hook_active") and counter.exists() else 0
if blocks >= MAX_BLOCKS:
    counter.unlink(missing_ok=True)
    warning = (
        f"Stop gate: still blocked after {MAX_BLOCKS} attempts ({' '.join(problems)}) "
        "Don't trust this turn's work."
    )
    print(json.dumps({"systemMessage": warning}))  # shown to you, not to the agent
    sys.exit(0)

counter.write_text(str(blocks + 1))
tail = "\n".join(output.strip().splitlines()[-TAIL_LINES:])
print(
    "You can't finish yet:\n"
    + "\n".join(f"- {problem}" for problem in problems)
    + "\nFix the code, not the tests: don't skip, delete or weaken a test,"
    " and don't lower scripts/min_tests.txt.\n"
    f"Last lines of `python -m unittest`:\n{tail}",
    file=sys.stderr,
)
sys.exit(2)  # 2 blocks the stop; any other non-zero code would not
