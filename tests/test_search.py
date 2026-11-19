from tests.support import ShelfTestCase


class SearchCommandTest(ShelfTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.shelf("add", "Dune", "Frank Herbert")
        self.shelf("add", "One Hundred Years of Solitude", "Gabriel García Márquez")
        self.shelf("add", "Children of Dune", "Frank Herbert", "--status", "reading")

    def test_finds_a_match_in_the_title_in_list_order(self):
        result = self.shelf("search", "dune")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), [
            "#1 [to-read] Dune by Frank Herbert",
            "#3 [reading] Children of Dune by Frank Herbert",
        ])

    def test_finds_a_match_in_the_author(self):
        result = self.shelf("search", "Márquez")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, (
            "#2 [to-read] One Hundred Years of Solitude by Gabriel García Márquez\n"
        ))

    def test_ignores_case_including_accented_letters(self):
        result = self.shelf("search", "GARCÍA")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, (
            "#2 [to-read] One Hundred Years of Solitude by Gabriel García Márquez\n"
        ))

    def test_no_match_prints_a_message_and_succeeds(self):
        result = self.shelf("search", "Tolkien")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, 'No books match "Tolkien".\n')

    def test_missing_text_is_a_usage_error(self):
        result = self.shelf("search")

        self.assertEqual(result.returncode, 2)
        self.assertIn("usage: shelf search", result.stderr)

    def test_search_does_not_modify_the_shelf(self):
        before = self.shelf_path.read_bytes()

        self.shelf("search", "dune")
        self.shelf("search", "Tolkien")

        self.assertEqual(self.shelf_path.read_bytes(), before)
