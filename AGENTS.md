<!-- Deliberately minimal. Lab 4 ("Context is infrastructure") asks you to improve this file. -->
# shelf

A tiny reading-list command line in Python 3.10+, standard library only.

- Run: `python -m shelf --help`
- Test: `./test` from this folder (quiet `python3 -m unittest -q`; pass unittest args, e.g. `./test -k status`).
- Issues: practice IDs (S1–S7, C1, C2) are not GitHub issue numbers. See `ISSUES.md` for the mapping (e.g. S3 is #6).
- The Stop hook (`scripts/stop_gate.py`) blocks a turn while tests fail, any test is skipped, or fewer than `scripts/min_tests.txt` tests run. Raise that number when the suite grows; never lower it.
