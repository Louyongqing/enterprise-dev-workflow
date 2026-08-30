"""Independent acceptance checks for trusted local copies of seeded fixtures."""
import argparse
import importlib.util
from pathlib import Path


def load_module(path):
    spec = importlib.util.spec_from_file_location("evaluated_fixture", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_catalog(root):
    module = load_module(root / "catalog.py")
    assert module.paginate([1, 2, 3, 4, 5], 1, 2) == [1, 2]
    assert module.paginate([1, 2, 3, 4, 5], 2, 2) == [3, 4]
    assert module.paginate([1, 2, 3], 4, 2) == []
    for page, size in ((0, 2), (1, 0)):
        try:
            module.paginate([1], page, size)
        except ValueError:
            pass
        else:
            raise AssertionError("pagination validation was lost")
    rows = [{"category": "book", "price": -1}, {"category": "book", "price": 0},
            {"category": "book", "price": 10}, {"category": "game", "price": 10}]
    snapshot = [dict(row) for row in rows]
    assert module.filter_rows(rows, min_price=0) == rows[1:]
    assert module.filter_rows(rows, category="book", min_price=10) == rows[2:3]
    assert module.filter_rows(rows, min_price=None) == rows
    assert module.filter_rows([], min_price=0) == []
    assert rows == snapshot


def check_authorization(root):
    module = load_module(root / "access.py")
    doc = {"tenant_id": "a", "owner_id": "u1"}
    for actor, expected in (
        ({"id": "u1", "tenant_id": "a", "role": "member"}, True),
        ({"id": "u2", "tenant_id": "a", "role": "admin"}, True),
        ({"id": "u1", "tenant_id": "b", "role": "member"}, False),
        ({"id": "u2", "tenant_id": "b", "role": "admin"}, False),
        ({"id": "u2", "tenant_id": "a", "role": "member"}, False),
        ({"id": "u1", "tenant_id": "a", "role": "unknown"}, False),
        ({"id": "", "tenant_id": "a", "role": "admin"}, False),
        ({"role": "admin"}, False), (None, False),
    ):
        assert module.can_read(actor, doc) is expected, (actor, expected)
    actor = {"id": "u1", "tenant_id": "a", "role": "admin"}
    for malformed in ({}, {"tenant_id": "a"}, {"tenant_id": "", "owner_id": "u1"}):
        assert module.can_read(actor, malformed) is False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=("catalog", "authorization"))
    parser.add_argument("fixture", type=Path)
    args = parser.parse_args()
    (check_catalog if args.kind == "catalog" else check_authorization)(args.fixture)
    print(f"PASS: {args.kind} independent acceptance checks")


if __name__ == "__main__":
    main()
