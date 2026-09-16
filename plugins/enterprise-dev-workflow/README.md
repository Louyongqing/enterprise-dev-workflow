# Enterprise Dev Workflow

Enterprise Dev Workflow 2.0 is a self-contained Codex plugin for disciplined software delivery. It helps Codex write less unnecessary code by controlling scope, reusing existing project conventions, routing only relevant skills, and stopping as soon as the requested result is verified.

## Core workflow

```text
Understand -> Recon -> Decompose -> Scope Lock -> Skill Route
-> Implement -> Quality Check -> Verify -> STOP
```

The workflow begins with the user's goal, observable acceptance criteria, known constraints, and explicit non-goals. It inspects the existing codebase before creating new structure, breaks large requirements into independently verifiable business tasks, and records each task's `Must Do`, `May Do`, and `Must Not Do` boundary.

Implementation follows the smallest sufficient change. SOLID is applied pragmatically, related business code stays cohesive, cross-module dependencies remain intentional, and abstractions are introduced only for a demonstrated need. Out-of-scope problems are reported instead of being fixed automatically.

## Skill routing

The bundled skills are intentionally small:

- `enterprise-delivery` is the only implicit entry point.
- `task-decomposition` splits large or cross-cutting requirements.
- `scope-control` locks authorized changes and handles discoveries outside scope.
- `code-quality` applies the coding, naming, cohesion, comments, and structure rules.
- `systematic-debugging` establishes a root cause before a bug fix.
- `verification` selects proportionate checks and guards completion claims.

Specialized work is routed to an available specialist skill only when the task actually needs it: UI, browser behavior, APIs, databases, architecture, security boundaries, codebase reconnaissance, or project verification. The plugin does not choose execution models and does not turn every task into a heavyweight process.

## Engineering standards

The reusable standards live under `references/`:

- `coding-standards.md`
- `comments.md`
- `testing.md`
- `task-template.md`

The guiding rule is: difficult problems deserve deeper reasoning, not automatically more code.

## Verification

Completion claims require current-environment evidence. Applicable checks may include build, typecheck, lint, unit/integration/E2E tests, browser behavior, API compatibility, migrations, security-sensitive paths, and final diff/status review.

Unavailable checks are reported explicitly:

```text
NOT VERIFIED: <check>
Reason: <exact reason>
```

## Installation

This package is distributed through the `enterprise-dev-workflow` GitHub marketplace:

```powershell
codex plugin marketplace add https://github.com/Louyongqing/enterprise-dev-workflow
codex plugin add enterprise-dev-workflow@enterprise-dev-workflow
```

Restart Codex or start a new task after installation so skill discovery uses the installed package.

Runtime behavior is not considered validated until the representative cases in `evals/workflow-cases.json` have been exercised in a fresh task.

## Development checks

```powershell
python -B -m unittest discover -s tests -v
python -B scripts/validate_workflow_contract.py .
```

Package and schema tests do not certify agent behavior. The evaluation set covers small changes, large requirements, bugs, UI, APIs, databases, architecture, security-sensitive work, dirty worktrees, unavailable tests, and scope expansion.

See `docs/verification.md` for package evidence, behavioral-evaluation boundaries, and limitations.

## License

Original plugin content is MIT licensed. Vendored and adapted Superpowers content retains its upstream MIT terms; see `THIRD_PARTY_NOTICES.md`.
