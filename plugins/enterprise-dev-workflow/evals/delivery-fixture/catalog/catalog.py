"""Deliberately incomplete local evaluation fixture; never production code."""


def paginate(rows, page=1, page_size=2):
    if page < 1 or page_size < 1:
        raise ValueError("positive pagination values required")
    start = page * page_size
    return rows[start:start + page_size]


def filter_rows(rows, category=None):
    return [row for row in rows if category is None or row["category"] == category]
