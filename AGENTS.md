# shelf: contract for agents

A tiny reading-list command line. Python 3.10+, standard library only.

## Read first

1. `kb/ACTIVE.md`: the current objective, tracks and definition of done. Read it before anything else.
2. `kb/decisions/`: decisions already taken and why. Follow them; don't reopen one without asking.

## Where things live

- Commands: `shelf/commands/`, one module per command, discovered automatically
- Book fields and statuses: `shelf/models.py`
- Shelf file format, loading and saving: `shelf/store.py`
- Errors and exit codes: `shelf/cli.py`
- Test helpers (temporary shelf, real CLI in a subprocess): `tests/support.py`
- Stop hook and test-count minimum: `scripts/stop_gate.py`, `scripts/min_tests.txt`
- Practice issue IDs → GitHub numbers: `ISSUES.md` (S3 is #6, C1 is #10, C2 is #11)
- Design overview: `docs/architecture.md`

## Commands

- Run: `python3 -m shelf --help` (set `SHELF_PATH=/tmp/x.json` to keep your real shelf untouched)
- All tests: `./test` (same as `python3 -m unittest -q`)
- Some tests: `./test -k status`, `./test tests.test_store`

## Rules for every change

- Standard library only. No new dependencies, in code or in tests.
- Code must run on Python 3.10: nothing newer (no `tomllib`, no `datetime.fromisoformat` with `Z`).
- A new command is a new file in `shelf/commands/` with `register(subparsers)`. Don't add it to a shared list.
- Invalid input to a command is a usage error: `parser.error(...)`, exit 2. A command that fails is a `ShelfError`, exit 1.
- Validate input at the command line boundary (`shelf/commands/`), not in `models.py` or `store.py`.
- Tests subclass `ShelfTestCase` so they use a temporary `SHELF_PATH` and `HOME`. Never touch the real `~/.shelf.json`.
- Code, program messages and tests are in English. Issues are in Spanish.
- Don't list commands in README.md; `--help` is the reference.
- Never skip, delete or weaken a test to make the suite pass. Fix the code.
- Commits follow Conventional Commits (`feat(add): …`, `fix(store): …`).
- One branch and one pull request per issue; the PR says `Closes #N` using the GitHub number from `ISSUES.md`.
- Ask before `git push` or `gh pr create`.

## Done means

- `./test` passes, with no skipped tests.
- The Stop hook passes. If you added tests, raise `scripts/min_tests.txt` to the new count; never lower it.
- Every new behaviour has a test that fails when the implementation is reverted.
- Every acceptance criterion of the issue is met, or the PR says which one isn't and why.
- The PR description has What, Why, Testing, and "Not verified" for anything you couldn't check.
- `kb/ACTIVE.md` is updated if the change finishes a track or changes the plan.
