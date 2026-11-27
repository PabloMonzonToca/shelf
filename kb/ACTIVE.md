# Active work

State as of 2026-11-27, checked with `gh issue list` and `gh pr list`.

## Current objective

Get shelf ready for book clubs ([S7, #12](https://github.com/PabloMonzonToca/shelf/issues/12)), starting with tags. C1 goes before C2 ([decision 0001](decisions/0001-c1-before-c2.md)).

## Next step

Start C1: branch from `main`, implement tags in [#10](https://github.com/PabloMonzonToca/shelf/issues/10) with tests that fail if the implementation is reverted, and open the PR.

## Active tracks

| Track | Issue | PR | State | Next gate |
| --- | --- | --- | --- | --- |
| C1: book tags | [#10](https://github.com/PabloMonzonToca/shelf/issues/10) | none yet | Not started | PR open, tests and Stop hook pass |
| C2: file format version 2, with `tags` | [#11](https://github.com/PabloMonzonToca/shelf/issues/11) | none yet | Waiting for C1 | C1 merged, #11 updated to include `tags` |
| Alignment: PRs, merges and issues agree | none | none | Ongoing | Review before each track's PR merges |
| Agent contract and this kb | none | [#20](https://github.com/PabloMonzonToca/shelf/pull/20) | Open, ready for review | Review and merge |

## Blockers

- C2 can't start until C1 is merged.
- [#11](https://github.com/PabloMonzonToca/shelf/issues/11) still assumes the book fields don't change before C2. It needs `tags` in version 2, and a migration from version 1 that accepts files with and without `tags`.

## Links

- Practice IDs → GitHub numbers: [ISSUES.md](../ISSUES.md)
- Rules and definition of done: [AGENTS.md](../AGENTS.md)
- Decisions: [kb/decisions/](decisions/)
- Track done: `python3 -m unittest` passes, the Stop hook passes, tag tests fail if the implementation is reverted, C1 merged so C2 can include `tags` in version 2.
