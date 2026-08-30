import unittest
from catalog import filter_rows, paginate


class ExistingTests(unittest.TestCase):
    def test_category(self):
        rows = [{"category": "book", "price": 10}, {"category": "game", "price": 20}]
        self.assertEqual(rows[:1], filter_rows(rows, "book"))

    def test_invalid_page(self):
        with self.assertRaises(ValueError):
            paginate([1, 2], 0)


if __name__ == "__main__":
    unittest.main()
