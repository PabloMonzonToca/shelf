"""shelf stats"""

from __future__ import annotations

import argparse
from datetime import date, datetime, timezone

from shelf.models import STATUSES, Book
from shelf.store import Store

FINISHED_THIS_YEAR = "finished this year"


def register(subparsers) -> None:
    parser = subparsers.add_parser("stats", help="count your books by status")
    parser.set_defaults(handler=run)


def finished_year(book: Book) -> int | None:
    """The UTC year in which the book was finished, or None if unknown.

    Stored timestamps are UTC. One without an offset is read as UTC too.
    """
    if not isinstance(book.finished_at, str):
        return None
    try:
        finished = datetime.fromisoformat(book.finished_at)
    except ValueError:
        return None
    if finished.tzinfo is None:
        finished = finished.replace(tzinfo=timezone.utc)
    return finished.astimezone(timezone.utc).year


def count(books: list[Book], today: date | None = None) -> dict[str, int]:
    """Books per known status, and done books finished in today's UTC year.

    Books with a status outside STATUSES are not counted on any line.
    """
    if today is None:
        today = datetime.now(timezone.utc).date()
    stats = {status: 0 for status in STATUSES}
    stats[FINISHED_THIS_YEAR] = 0
    for book in books:
        if book.status not in STATUSES:
            continue
        stats[book.status] += 1
        if book.status == "done" and finished_year(book) == today.year:
            stats[FINISHED_THIS_YEAR] += 1
    return stats


def run(args: argparse.Namespace, store: Store) -> int:
    for label, number in count(store.load()).items():
        print(f"{label}: {number}")
    return 0
