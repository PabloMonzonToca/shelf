---
id: D-0001
title: C1 (tags) before C2 (file format version)
status: accepted
decided_on: 2026-11-27
---

# D-0001: C1 (tags) before C2 (file format version)

## Context

C1 ([#10](https://github.com/PabloMonzonToca/shelf/issues/10)) and C2 ([#11](https://github.com/PabloMonzonToca/shelf/issues/11)) both change how books are stored, so one has to build on the other.

Evidence in the code:

- `tests/test_store.py:29-37` (`test_the_file_is_a_json_list_of_books`) pins the stored file exactly. It checks that the file is a JSON list (line 34), and that each book has exactly the fields `id`, `title`, `author`, `status`, `added_at` and `finished_at` (lines 35-37). Both issues must change this test: C1 adds `tags` to the field set, and C2 replaces the list with `{"version": 2, "books": [...]}`.
- `shelf/models.py:30-35`: `Book.to_dict` writes every dataclass field (`asdict`), and `Book.from_dict` passes every stored key to `Book(**data)`. A new field is saved automatically. A file without it loads only if the field has a default.
- `shelf/store.py:38-49`: `Store.load` expects a list and `Store.save` writes one. C2 changes both.

C2's acceptance criteria add a per-version field test that fails when a `Book` field changes without raising `SCHEMA_VERSION`. Whichever issue goes second has to fit into the format the first one leaves behind.

## Options considered

1. **C1 first, then C2 with `tags` in version 2.** Tags ship sooner, with one format version and one migration. Version 1 then covers unversioned files both with and without `tags`.
2. **C2 first, then C1 as version 3.** The first field change gets a version number, but tags ship later and need two versions and two migrations.

## Decision

Option 1: implement C1 first. C2 follows, and its version 2 includes `tags` from day one.

## Consequences

- C1 updates `tests/test_store.py:35-37` to include `tags`. Files written before C1 must still load, with no tags, so `tags` needs a default in `Book`.
- C2 updates the same test (line 34 and the field set) to the versioned object. Its version 2 fields include `tags`.
- C2's migration from version 1 accepts both kinds of unversioned list, with and without `tags`. Its version 1 fixture covers both.
- [#11](https://github.com/PabloMonzonToca/shelf/issues/11) must be updated before C2 starts: it still says version 2 books are the same objects the file contains today.
