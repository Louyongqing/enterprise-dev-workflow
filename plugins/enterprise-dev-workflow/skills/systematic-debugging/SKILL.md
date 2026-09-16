---
name: systematic-debugging
description: Use for bugs, regressions, failing tests, crashes, or unexplained behavior. Reproduces the failure, traces evidence to a root cause, adds a valuable regression check, applies the smallest scoped fix, and verifies the original path.
---

# Systematic Debugging

Do not edit production code from a guess.

## Workflow

1. Reproduce the reported behavior or collect the closest available evidence.
2. State expected versus actual behavior and the narrowest failing boundary.
3. Trace data and control flow backward until the earliest demonstrated cause is found.
4. Distinguish facts, inferences, and unknowns. Test competing explanations when evidence is ambiguous.
5. Add or update a regression test when it usefully proves the failure and the project can run it.
6. Make the smallest fix at the cause, following existing project conventions.
7. Re-run the original reproduction and relevant regression checks.
8. Inspect scope. Report adjacent issues instead of fixing them automatically.

Do not use a bug as a reason to redesign the whole module. If the root cause cannot be established, report the evidence and uncertainty; do not present a speculative patch as verified.

Follow [testing rules](../../references/testing.md) and finish with [verification](../verification/SKILL.md).
