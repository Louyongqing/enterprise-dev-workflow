---
name: enterprise-delivery
description: Use for implementing, fixing, reviewing, refactoring, or preparing to deliver software. Enforces task understanding, reconnaissance, decomposition, scope control, selective skill routing, minimal implementation, quality checks, verification, and a strict stop condition.
---

# Enterprise Delivery

Follow this sequence for software changes:

```text
Understand -> Recon -> Decompose -> Scope Lock -> Skill Route
-> Implement -> Quality Check -> Verify -> STOP
```

Do not replace this sequence with a task rating. Difficult problems call for deeper reasoning, not automatically more code, more abstractions, or more process.

## Top-level principles

1. Simplicity first.
2. Prefer the smallest sufficient implementation.
3. Keep related behavior cohesive and dependencies intentional.
4. Apply SOLID pragmatically, not dogmatically.
5. Do not create abstractions for hypothetical future needs.
6. Reuse project conventions before introducing new patterns.
7. Comments explain why, not obvious code behavior.
8. Break large requirements into independently verifiable tasks.
9. Do not modify code outside the agreed scope.
10. Use only the skills required by the current task.
11. Preserve unrelated user changes.
12. Once acceptance criteria are satisfied and required verification passes, stop.

## 1. Understand

Identify the requested `Goal`, observable `Acceptance Criteria`, `Known Constraints`, and `Explicit Non-Goals`. Do not keep asking questions when the request and repository evidence already make the required result clear. Read-only requests authorize inspection and reporting, not implementation.

## 2. Recon

Before editing, inspect the nearest repository instructions, worktree state, relevant modules, existing boundaries, conventions, error handling, tests, and reusable capabilities. Reuse before creating. For an unfamiliar or high-impact codebase, route to `codebase-recon` when available.

## 3. Decompose

If the requirement contains multiple business capabilities, broad unknowns, or changes that cannot be independently verified, load [task-decomposition](../task-decomposition/SKILL.md). Keep a small, cohesive change as one task.

## 4. Scope Lock

For every implementation task, define `Must Do`, `May Do`, and `Must Not Do`. Load [scope-control](../scope-control/SKILL.md) when the boundary needs detailed handling. A discovered issue outside scope is reported, not fixed automatically.

## 5. Skill Route

Load only skills justified by actual work:

- Bug, regression, failing test, or unexplained behavior -> [systematic-debugging](../systematic-debugging/SKILL.md)
- Implementation quality, structure, naming, comments, or refactoring -> [code-quality](../code-quality/SKILL.md)
- UI design -> `frontend-design`
- Browser interaction or local web behavior -> `webapp-testing`
- API contract -> `api-design`
- Schema, query, index, migration, or data integrity -> `database-engineering`
- Real module or system architecture change -> `backend-architecture`
- Authentication, authorization, payment, secrets, sensitive data, unsafe input, files, commands, or another trust boundary -> `security-review`
- Final implementation evidence -> [verification](../verification/SKILL.md), plus `project-verification` when available and applicable

If a specialist skill is unavailable, apply the same bounded concern directly and report any resulting verification limitation. Never load every skill by default.

Before coding, keep a concise execution brief:

```text
Goal:
...

Plan:
1. ...

Scope:
Must Do: ...
May Do: ...
Must Not Do: ...

Skills Needed:
...

Verification:
...
```

## 6. Implement

Make the smallest change that satisfies the current acceptance criteria. Prefer local business code on the first demonstrated use. Generalize only after repeated, proven need or when an existing project boundary already requires it. Follow [coding standards](../../references/coding-standards.md) and the repository's more specific conventions.

## 7. Quality Check

Before verification, ask:

- Does this solve the requested problem?
- Is any code, abstraction, pattern, comment, test, or directory unnecessary?
- Did anything outside scope change?
- Are names clear, control flow readable, related code cohesive, and coupling reasonable?
- Could the implementation be simpler without reducing correctness?

Simplify only the changed solution. Do not turn this check into unrelated cleanup.

## 8. Verify

Load [verification](../verification/SKILL.md). Select the smallest set of checks that proves the acceptance criteria and protects the affected risk. Never claim an unrun check passed. Mark unavailable material checks as `NOT VERIFIED` with the exact reason.

## 9. STOP

When acceptance criteria are satisfied and required verification has passed, stop. Do not add speculative features, extra abstractions, unrelated refactors, unnecessary tests, or directory cleanup.

Report:

```text
Implemented:
...

Verified:
...

Out-of-scope issues noticed:
...

No additional unrelated changes made.
```
