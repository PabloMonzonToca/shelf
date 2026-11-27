# 0001: C1 (tags) before C2 (file format version)

Date: 2026-11-27
Status: accepted

## Decision

Implement C1 (#10) before C2 (#11).

## Why

- Tags should ship sooner.
- With C1 merged first, C2's version 2 format includes `tags` from day one, so no extra migration is needed later.

## Consequences

- C1 changes the unversioned format (a JSON list) by adding `tags` to each book. Files written before C1 have no `tags` and must still load, with no tags (C1's acceptance criteria require this).
- C2's version 1 therefore covers unversioned lists both with and without `tags`. Its migration must accept both.
- C2's version 2 book fields include `tags`. Its version 1 fixture and its per-version field test must reflect that.

## Alternative considered

C2 first, then C1 as version 3. It gives the first format change a version number, but it means two format versions and two migrations before tags ship.
