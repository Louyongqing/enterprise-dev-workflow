# Comment Standards

Comments explain why a decision or constraint exists, not what the next line visibly does.

Useful comments include:

- business-rule reasons;
- compatibility with an older client or data format;
- surprising third-party behavior;
- non-obvious algorithms;
- idempotency, security, or performance reasons;
- a temporary workaround and the condition for removing it;
- a TODO with concrete context and ownership criteria.

Avoid comments that translate code, narrate loops, repeat names, add empty documentation to accessors, or mechanically decorate every method. Keep comments accurate when behavior changes; delete stale comments rather than preserving misleading history.
