---
name: code-quality
description: Use while implementing or reviewing software structure, naming, comments, cohesion, coupling, SOLID decisions, directories, error handling, tests, and refactoring. Favors readable, local, sufficient solutions over speculative abstraction.
---

# Code Quality

Use the project's existing conventions first, then apply the standards below only where they improve the requested change.

## Core rules

- Prefer the smallest sufficient implementation.
- Keep one business capability cohesive and avoid unnecessary cross-module dependencies.
- Apply SOLID as guidance, not as a quota for interfaces, factories, strategies, or classes.
- Do not introduce an abstraction for a hypothetical second implementation.
- Extract a method when it expresses a meaningful operation, removes real duplication, simplifies difficult control flow, improves testability, or clarifies a boundary.
- Choose names that express business meaning. Avoid vague names such as `handle`, `process`, `data`, `info`, and `temp` when a clearer term exists.
- Create a directory or package only for a real business or architectural boundary.
- Reuse existing error handling instead of creating a parallel exception framework.
- Refactor only when the current task is a refactor, the implementation is otherwise unsafe, or directly relevant duplication blocks the change.

Read the detailed [coding standards](../../references/coding-standards.md), [comment rules](../../references/comments.md), and [testing rules](../../references/testing.md). Repository-specific rules take precedence.
