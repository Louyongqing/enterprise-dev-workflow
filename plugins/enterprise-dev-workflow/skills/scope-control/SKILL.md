---
name: scope-control
description: Use when a software task needs an explicit change boundary, contains non-goals, touches a dirty worktree, or reveals adjacent issues. Defines Must Do, May Do, and Must Not Do and prevents unauthorized cleanup or expansion.
---

# Scope Control

Lock the implementation boundary before editing:

```text
Must Do:
- work required by the acceptance criteria

May Do:
- directly necessary supporting changes

Must Not Do:
- explicit non-goals and unrelated changes
```

## Rules

- Derive the scope from the user's request, accepted design artifacts, repository constraints, and current evidence.
- Treat `May Do` as permission only when the supporting change is actually necessary.
- Preserve unrelated user changes in dirty worktrees.
- Do not broaden permissions, public contracts, dependencies, architecture, persistence, or external side effects without authority.
- If a new decision would materially change the requested result, stop and ask for that decision.
- If an adjacent problem does not block the task, record it under `Out-of-scope issues noticed` and continue.
- If an adjacent problem directly blocks safe completion, explain the evidence and the smallest decision needed from the user.

"While I am here" is not a valid reason to modify code. Scope control applies through final diff inspection, not only at task start.
