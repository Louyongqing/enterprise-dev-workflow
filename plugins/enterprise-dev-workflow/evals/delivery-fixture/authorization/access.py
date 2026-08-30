"""Deliberately defective authorization evaluation fixture; do not deploy."""


def can_read(actor, document):
    if not actor or not document:
        return False
    return actor.get("role") == "admin" or (
        actor.get("tenant_id") == document.get("tenant_id")
        and actor.get("id") == document.get("owner_id")
    )
