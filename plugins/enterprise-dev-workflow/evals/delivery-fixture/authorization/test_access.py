import unittest
from access import can_read


class ExistingTests(unittest.TestCase):
    def test_owner(self):
        self.assertTrue(can_read({"id": "u1", "tenant_id": "a", "role": "member"},
                                 {"tenant_id": "a", "owner_id": "u1"}))

    def test_no_identity(self):
        self.assertFalse(can_read(None, {"tenant_id": "a", "owner_id": "u1"}))


if __name__ == "__main__":
    unittest.main()
