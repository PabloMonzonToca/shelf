import json
import unittest
from datetime import date

from shelf.commands.stats import count
from shelf.models import Book
from tests.support import ShelfTestCase


def book(book_id: int, status: str, finished_at: str | None = None) -> Book:
    return Book(
        id=book_id,
        title=f"Book {book_id}",
        author="Someone",
        status=status,
        added_at="2000-01-01T00:00:00+00:00",
        finished_at=finished_at,
    )


# The example from the issue, plus a book with a status stats does not know.
EXAMPLE_SHELF = [
    book(1, "to-read"),
    book(2, "to-read"),
    book(3, "reading"),
    book(4, "banana"),
    book(5, "done", "2026-01-01T00:00:00+00:00"),
    book(6, "done", "2026-03-01T10:00:00+00:00"),
    book(7, "done", "2025-12-31T23:59:59+00:00"),
]


class CountTest(unittest.TestCase):
    """The counting, with today's date fixed so the year never matters."""

    def test_counts_the_example_from_the_issue(self):
        self.assertEqual(count(EXAMPLE_SHELF, today=date(2026, 6, 15)), {
            "to-read": 2,
            "reading": 1,
            "done": 3,
            "finished this year": 2,
        })

    def test_an_empty_shelf_counts_zero_everywhere(self):
        self.assertEqual(count([], today=date(2026, 6, 15)), {
            "to-read": 0,
            "reading": 0,
            "done": 0,
            "finished this year": 0,
        })

    def test_a_book_finished_last_year_does_not_count_this_year(self):
        books = [
            book(1, "done", "2025-12-31T23:59:59+00:00"),
            book(2, "done", "2026-01-01T00:00:00+00:00"),
        ]

        stats = count(books, today=date(2026, 1, 1))

        self.assertEqual(stats["done"], 2)
        self.assertEqual(stats["finished this year"], 1)

    def test_a_done_book_without_a_readable_finished_at_is_done_but_not_this_year(self):
        books = [
            book(1, "done", None),
            book(2, "done", "not a date"),
        ]

        stats = count(books, today=date(2026, 6, 15))

        self.assertEqual(stats["done"], 2)
        self.assertEqual(stats["finished this year"], 0)

    def test_unknown_statuses_are_not_counted_on_any_line(self):
        books = [
            book(1, "banana"),
            book(2, "Done", "2026-03-01T10:00:00+00:00"),
        ]

        self.assertEqual(count(books, today=date(2026, 6, 15)), {
            "to-read": 0,
            "reading": 0,
            "done": 0,
            "finished this year": 0,
        })


class StatsCommandTest(ShelfTestCase):
    """The real command line. Every timestamp is from 2000, so 'finished this
    year' is 0 whatever year the tests run in."""

    def write_shelf(self, books: list[Book]) -> None:
        records = [b.to_dict() for b in books]
        self.shelf_path.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")

    def test_prints_exactly_four_lines_in_order(self):
        self.write_shelf([
            book(1, "to-read"),
            book(2, "to-read"),
            book(3, "reading"),
            book(4, "banana"),
            book(5, "done", "2000-01-01T00:00:00+00:00"),
            book(6, "done", "2000-03-01T10:00:00+00:00"),
            book(7, "done", "2000-12-31T23:59:59+00:00"),
        ])

        result = self.shelf("stats")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, (
            "to-read: 2\n"
            "reading: 1\n"
            "done: 3\n"
            "finished this year: 0\n"
        ))
        self.assertEqual(result.stderr, "")

    def test_an_empty_shelf_prints_four_zeros(self):
        result = self.shelf("stats")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, (
            "to-read: 0\n"
            "reading: 0\n"
            "done: 0\n"
            "finished this year: 0\n"
        ))
        self.assertFalse(self.shelf_path.exists())

    def test_stats_does_not_modify_the_shelf(self):
        self.write_shelf([
            book(1, "to-read"),
            book(2, "done", "2000-03-01T10:00:00+00:00"),
        ])
        before = self.shelf_path.read_bytes()

        result = self.shelf("stats")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.shelf_path.read_bytes(), before)
