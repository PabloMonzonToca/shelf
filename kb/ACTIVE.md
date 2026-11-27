# Active work

Last updated: 2026-11-27

## Objective

Get shelf ready for book clubs (S7, #12), starting with tags.

## Tracks

1. **C1, tags (#10).** Implement book tags with tests, and get the change ready to merge.
2. **C2, file format version 2 (#11).** Starts after C1 is merged. Version 2 includes `tags` from day one, with the migration from version 1 and its tests.
3. **Alignment.** Review open pull requests, merged changes and open issues so both tracks agree.

Order: C1 first, then C2. See `decisions/0001-c1-before-c2.md`.

## Done means

- `python3 -m unittest` passes.
- The Stop hook passes.
- Tag behaviour has tests that fail if the implementation is reverted.
- C1 is merged, and C2 can proceed with tags included in version 2.
